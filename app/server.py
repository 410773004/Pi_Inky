# app/server.py
from flask import Blueprint, request, jsonify, redirect, url_for ,send_from_directory
from pathlib import Path
import os
from .renderer import render_album
from threading import Event
import threading
from .clock_loop import run_clock

bp = Blueprint("web", __name__)

# 專案目錄
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# 將由 main.py 注入
display = None
disp_width = None
disp_height = None

clock_stop_event = Event()
clock_thread = None

current_mode = "none"



def init_routes(_display, _w, _h):
    global display, disp_width, disp_height
    display = _display
    disp_width = _w
    disp_height = _h


# ------------------------------------------------------
# 首頁（網頁 UI）
# ------------------------------------------------------
HTML = """
<h1>📟 Pi 電子紙控制面板</h1>

<h2>切換模式</h2>
<a href="/mode/clock">📅 時鐘模式</a><br>
<a href="/mode/album">🖼 相簿模式（上傳圖片）</a><br><br>
<a href="/mode/message">🖼 留言模式）</a><br><br>

<h2>相簿上傳</h2>
<form action="/upload" method="post" enctype="multipart/form-data">
  <input type="file" name="image">
  <button type="submit">上傳圖片並顯示</button>
</form>

<h2>相簿列表</h2>
<a href="/album">查看相簿 JSON</a>
"""

@bp.route("/")
def index():
    mode_info = f"<p>目前模式：{current_mode}</p>"
    if current_mode == "message":
        mode_info += '<a href="/message">➡ 前往留言頁面</a><br><br>'
    return HTML + mode_info

    return HTML


# ------------------------------------------------------
# 模式切換
# ------------------------------------------------------
@bp.route("/mode/clock")
def mode_clock():
    global clock_thread

    # 停止現有時鐘
    if clock_thread and clock_thread.is_alive():
        clock_stop_event.set()
        clock_thread.join()

    clock_stop_event.clear()
    clock_thread = threading.Thread(
        target=run_clock,
        args=(display, disp_width, disp_height, clock_stop_event),
        daemon=True
    )
    clock_thread.start()

    return redirect(url_for("web.index"))


@bp.route("/mode/album")
def mode_album():
    global clock_thread

    # 停止現有時鐘
    if clock_thread and clock_thread.is_alive():
        clock_stop_event.set()
        clock_thread.join()

    return redirect(url_for("web.index"))


# ------------------------------------------------------
# 上傳相片
# ------------------------------------------------------
@bp.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("image")
    if not file:
        return "沒有收到圖片", 400

    filename = file.filename
    save_path = UPLOAD_DIR / filename
    file.save(save_path)

    img = render_album(str(save_path), disp_width, disp_height)

    clock_stop_event.set()
    display.clear()
    display.show_image(img)

    return redirect(url_for("web.index"))


# ------------------------------------------------------
# 相簿列表
# ------------------------------------------------------
@bp.route("/album")
def album():
    return jsonify(os.listdir(UPLOAD_DIR))


@bp.route("/image/<filename>")
def get_image(filename):
    return send_from_directory(UPLOAD_DIR, filename)

@bp.route("/mode/message")
def mode_message():
    global current_mode

    # 停時鐘（你原本已有）
    if clock_thread and clock_thread.is_alive():
        clock_stop_event.set()
        clock_thread.join()

    current_mode = "message"   # ← ★ 新增這行，啟用留言模式

    return redirect(url_for("web.index"))


@bp.route("/message")
def message_page():
    return """
    <h2>留言模式</h2>
    <form action='/api/send_message' method='POST'>
        <textarea name='text' rows='4' cols='40'></textarea><br><br>
        <button type='submit'>送出</button>
    </form>
    <br>
    <a href="/">回首頁</a>
    """

from .renderer import load_font
from PIL import Image, ImageDraw

@bp.route("/api/send_message", methods=["POST"])
def send_message():
    global disp_width, disp_height, display

    text = request.form.get("text", "").strip()
    if not text:
        return "訊息不能為空", 400

    img = Image.new("RGB", (disp_width, disp_height), "black")
    draw = ImageDraw.Draw(img)
    font = load_font(40)

    # 使用 textbbox 取得寬高（新版 Pillow 用法）
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    # 置中
    draw.text(
        ((disp_width - w) // 2, (disp_height - h) // 2),
        text,
        fill="white",
        font=font
    )

    display.clear()
    display.show_image(img)

    return redirect("/message")

