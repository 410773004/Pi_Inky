# app/renderer.py
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import os



def load_font(size: int = 28):
    font_file = os.path.join(
        os.path.dirname(__file__), "..", "fonts", "NotoSansTC-VariableFont_wght.ttf"
    )

    try:
        return ImageFont.truetype(font_file, size)
    except Exception as e:
        print("Font load failed:", e)
        return ImageFont.load_default()

def optimize_image(img: Image.Image) -> Image.Image:
    """
    直接接收一張 Image 物件並優化，使其適合 7.3 六色 e-paper。
    """

    TARGET_W, TARGET_H = 800, 480

    # Step 1：保持比例縮放
    img = img.copy()
    img.thumbnail((TARGET_W, TARGET_H))

    # Step 2：對比提升
    img = ImageEnhance.Contrast(img).enhance(1.1)

    # Step 3：亮度微調
    img = ImageEnhance.Brightness(img).enhance(1.0)

    # Step 4：銳化
    img = img.filter(ImageFilter.SHARPEN)

    # Step 5：降低彩度
    img = ImageEnhance.Color(img).enhance(0.9)

    # Step 6：六色量化
    PALETTE = [
        (255, 255, 255),  # white
        (0, 0, 0),        # black
        (255, 0, 0),      # red
        (255, 255, 0),    # yellow
        (0, 255, 0),      # green
        (0, 0, 255)       # blue
    ]

    palette_img = Image.new('P', (1, 1))
    flat_palette = sum(PALETTE, ())
    palette_img.putpalette(flat_palette * 42)

    img = img.quantize(palette=palette_img, dither=Image.FLOYDSTEINBERG).convert("RGB")

    # Step 7：置中畫布
    canvas = Image.new("RGB", (TARGET_W, TARGET_H), "white")
    x = (TARGET_W - img.width) // 2
    y = (TARGET_H - img.height) // 2
    canvas.paste(img, (x, y))

    return canvas



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
    canvas = optimize_image(canvas)
    return canvas

def render_clock(width: int, height: int) -> Image.Image:
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    font_big = load_font(80)
    font_small = load_font(32)

    # 時間
    now = datetime.now()
    time_str = now.strftime("%H:%M")
    date_str = now.strftime("%Y-%m-%d (%a)")

    # 時鐘置中
    bbox_time = draw.textbbox((0, 0), time_str, font=font_big)
    bbox_date = draw.textbbox((0, 0), date_str, font=font_small)

    w_time = bbox_time[2] - bbox_time[0]
    h_time = bbox_time[3] - bbox_time[1]

    w_date = bbox_date[2] - bbox_date[0]
    h_date = bbox_date[3] - bbox_date[1]

    center_y = height // 2

    draw.text(
        ((width - w_time) // 2, center_y - h_time - 20),
        time_str,
        fill="black",
        font=font_big
    )

    draw.text(
        ((width - w_date) // 2, center_y + 20),
        date_str,
        fill="black",
        font=font_small
    )

    return img