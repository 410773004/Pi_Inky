# app/renderer.py
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def load_font(size: int = 28) -> ImageFont.FreeTypeFont:
    # 你可以放自己的中文字型，先簡單用內建
    try:
        return ImageFont.truetype("arial.ttf", size)
    except:
        return ImageFont.load_default()


def render_album(image_path: str, width: int, height: int) -> Image.Image:
    """
    讀取一張圖片並自動縮放到電子紙尺寸
    """
    p = Path(image_path)
    if not p.exists():
        # 找不到圖片 → 畫一張錯誤圖
        img = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(img)
        font = load_font(28)
        draw.text((30, 30), f"圖片不存在：\n{image_path}", fill="black", font=font)
        return img

    img = Image.open(p).convert("RGB")

    # 自動縮放比到畫面最大
    img.thumbnail((width, height))

    # 中心對齊
    canvas = Image.new("RGB", (width, height), "white")
    x = (width - img.width) // 2
    y = (height - img.height) // 2
    canvas.paste(img, (x, y))
    return canvas