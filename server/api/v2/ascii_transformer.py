import base64
import os
from io import BytesIO
from sre_parse import GROUPREF_IGNORE

import numpy as np
import requests
import resvg_py
from PIL import Image, ImageDraw, ImageFont


def gif_to_ascii(response, bg_color, ASCII, size: int = 50):
    img = Image.open(BytesIO(response.content))
    frames = []
    durations = []
    for frame in range(img.n_frames if img.n_frames < 5 else 4):
        img.seek(frame)
        frame_img = img.convert("RGB")
        out_image = processar_frame_ascii(frame_img, bg_color, ASCII, size)
        frames.append(out_image)
        durations.append(img.info.get('duration', 100))
    return pil_para_base64_gif(frames, durations)

def processar_frame_ascii(frame_img, bg_color, ASCII, size: int = 50):
    img = frame_img.convert("RGB")
    width, height = img.size
    if width > size or height > size:
        img = img.resize((size, size))
        width, height = img.size

    try:
        size_fonte = 12
        fonte = ImageFont.truetype("courier.ttf", size_fonte)
    except IOError:
        print("Aviso: Fonte 'courier.ttf' não encontrada. Usando fonte padrão.")
        fonte = ImageFont.load_default()

    # Sizes
    bbox = fonte.getbbox('A')
    w_caractere, h_caractere = bbox[2] - bbox[0], bbox[3] - bbox[1]

    out_width = int(width * w_caractere)
    out_height = int(height * h_caractere)
    out_image = Image.new('RGB', (out_width, out_height), color=(bg_color))
    draw = ImageDraw.Draw(out_image)

    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            draw.text((x * w_caractere, y * h_caractere), ASCII[gray * (len(ASCII) - 1) // 255], font=fonte, fill=(r, g, b))

    return out_image

def pil_para_base64_gif(frames, durations, loop=0):
    buffered = BytesIO()
    frames[0].save(
        buffered,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=loop,
    )
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:image/gif;base64,{img_str}"

def pil_para_base64(imagem_pil):
    buffered = BytesIO()
    imagem_pil.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{img_str}"

def image_to_ascii(image_input,bg_color, ascii_type, size: int = 50):

    if ascii_type == "focus-white":
        ASCII = " .'`\"^;:-!i><~+_-?1ftjrxnuvczXYUJCLQ0OZmwqpdbkhaoy*#MW&8%B@$"
    else:
        ASCII = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrftj1?-_+~<>i!lI;:,\"^`'. "

    # Handle HTTP / HTTPS URLs
    if isinstance(image_input, str) and image_input.startswith(("http://", "https://")):
        response = requests.get(image_input, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        if "image/svg" in response.headers.get(
            "Content-Type", ""
        ) or image_input.endswith(".svg"):
            img = Image.open(BytesIO(resvg_py.svg_to_bytes(response.content.decode("utf-8"))))
        elif image_input.endswith(".gif"):
            return gif_to_ascii(response, bg_color, ASCII, size)
        else:
            img = Image.open(BytesIO(response.content))


    # Handle Base64 Strings or Data URIs
    elif isinstance(image_input, str):
        # Strip data URI header if present
        if "base64," in image_input:
            image_input = image_input.split("base64,")[1]

        # Fix missing Base64 padding if stripped
        missing_padding = len(image_input) % 4
        if missing_padding:
            image_input += "=" * (4 - missing_padding)

        image_bytes = base64.b64decode(image_input.strip())

        if image_bytes.strip().startswith(b"<svg"):
            svg_str = image_bytes.decode("utf-8")
            img = Image.open(BytesIO(resvg_py.svg_to_bytes(svg_str)))
        else:
            img = Image.open(BytesIO(image_bytes))

    # Process standard image conversion
    img = img.convert("RGB")
    width, height = img.size
    if width > size or height > size:
        img = img.resize((size, size))
        width, height = img.size

    try:
        size_fonte = 12
        fonte = ImageFont.truetype("courier.ttf", size_fonte)
    except IOError:
        print("Aviso: Fonte 'courier.ttf' não encontrada. Usando fonte padrão.")
        fonte = ImageFont.load_default()

    # Sizes
    bbox = fonte.getbbox('A')
    w_caractere, h_caractere = bbox[2] - bbox[0], bbox[3] - bbox[1]

    out_width = int(width * w_caractere)
    out_height = int(height * h_caractere)
    out_image = Image.new('RGB', (out_width, out_height), color=(bg_color))
    draw = ImageDraw.Draw(out_image)

    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            draw.text((x * w_caractere, y * h_caractere), ASCII[gray * (len(ASCII) - 1) // 255], font=fonte, fill=(r, g, b))

    return pil_para_base64(out_image)
