import anthropic
import base64
import json
import re
from PIL import Image
import io


def analyze_shelf_image(image_bytes: bytes, planogram: dict, api_key: str) -> dict:
    client = anthropic.Anthropic(api_key=api_key, base_url="https://api.aiprimetech.io")

    img = Image.open(io.BytesIO(image_bytes))
    if img.mode != "RGB":
        img = img.convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    img_b64 = base64.standard_b64encode(buf.getvalue()).decode("utf-8")

    planogram_desc = f"Планограмма '{planogram['name']}':\n"
    for shelf in planogram["shelves"]:
        products_str = " | ".join([f"{i+1}. {p}" for i, p in enumerate(shelf["products"])])
        planogram_desc += f"- {shelf['name']}: {products_str}\n"

    all_products = []
    for s in planogram["shelves"]:
        all_products.extend(s["products"])
    products_list = ", ".join(set(all_products))

    prompt = f"""Ты — система анализа выкладки товаров на полках магазина.

ПЛАНОГРАММА:
{planogram_desc}

Проанализируй фото прилавка. Для каждой полки определи товары и порядок (слева направо).
Сравни с планограммой.

Ответь ТОЛЬКО JSON без пояснений:
{{"shelves_detected":N,"shelves":[{{"shelf_number":1,"name":"...","products_found":["..."],"order_correct":true,"missing_products":["..."],"extra_products":["..."],"wrong_order_details":"...","confidence":"high"}}],"overall_compliance":85,"critical_violations":["..."],"summary":"резюме на русском"}}"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": img_b64}},
                {"type": "text", "text": prompt}
            ]
        }]
    )

    raw = response.content[0].text.strip()
    raw = re.sub(r'^```(?:json)?\s*', '', raw)
    raw = re.sub(r'\s*```$', '', raw)
    return json.loads(raw)


def resize_image_for_display(image_bytes: bytes, max_size: int = 800) -> bytes:
    img = Image.open(io.BytesIO(image_bytes))
    try:
        exif = img._getexif()
        if exif:
            orientation = exif.get(0x112)
            rotate_map = {3: 180, 6: 270, 8: 90}
            if orientation in rotate_map:
                img = img.rotate(rotate_map[orientation], expand=True)
    except Exception:
        pass

    img.thumbnail((max_size, max_size), Image.LANCZOS)

    if img.mode in ("RGBA", "P", "LA"):
        background = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode == "P":
            img = img.convert("RGBA")
        background.paste(img, mask=img.split()[-1] if img.mode in ("RGBA", "LA") else None)
        img = background
    elif img.mode != "RGB":
        img = img.convert("RGB")

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return buf.getvalue()