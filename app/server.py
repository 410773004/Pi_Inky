# app/server.py
from flask import Flask, request, render_template_string
from pathlib import Path
import argparse
import os

from PIL import Image
from .renderer import render_album
from .display_waveshare import WaveshareEPDDisplay
from .display_mock import MockEPDDisplay


# -----------------------
# 建立 Flask App
# -----------------------
app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


# -----------------------
# 顯示器選擇
# -----------------------
def create_display(mode: str):
    if mode == "real":
        print("[Server] 使用 REAL 電子紙")
        return WaveshareEPDDisplay(rotation=0)
    else:
        print("[Server] 使用 MOCK 模擬器")
        return MockEPDDisplay(size=(800, 480))


# -----------------------
# HTML 頁面
# -----------------------
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Pi 電子紙上傳</title>
</head>
<body>
    <h1>上傳圖片到電子紙</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="image" accept="image/*">
        <button type="submit">上傳並顯示</button>
    </form>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML_PAGE)


# -----------------------
# 上傳圖片路由
# -----------------------
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("image")

    if not file:
        return "沒有收到圖片", 400

    save_path = UPLOAD_DIR / "latest.jpg"
    file.save(save_path)

    print(f"[Server] 已收到圖片：{save_path}")

    # 建立顯示圖片
    img = render_album(str(save_path), app.width, app.height)

    # 推到 display
    app.display.clear()
    app.display.show_image(img)
    app.display.sleep()

    return f"已顯示！（mode={app.mode}）"


# -----------------------
# 主程式入口
# -----------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["real", "mock"],
                        default=os.environ.get("EPD_MODE", "mock"))
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()

    app.mode = args.mode
    app.display = create_display(args.mode)
    app.display.init()

    # 取得螢幕尺寸
    app.width, app.height = app.display.size

    print(f"[Server] Web 伺服器啟動中，mode={args.mode}")
    print(f"[Server] 螢幕尺寸：{app.width} x {app.height}")

    # 啟動 web server
    app.run(host="0.0.0.0", port=args.port)


if __name__ == "__main__":
    main()
