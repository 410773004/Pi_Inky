# app/main.py
import argparse
import os
from flask import Flask
from .display_waveshare import WaveshareEPDDisplay
from .display_mock import MockEPDDisplay
from .server import bp, init_routes

def create_display(mode):
    if mode == "real":
        return WaveshareEPDDisplay(rotation=0)
    else:
        return MockEPDDisplay(size=(800, 480), rotation=0)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["real", "mock"],default="mock")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()

    display = create_display(args.mode)
    display.init()

    width, height = display.size
    print("[MAIN] Display:", width, "x", height)

    # 啟動 Flask
    app = Flask(__name__)

    # 把 display 注入 Flask 路由
    init_routes(display, width, height)

    # 註冊 Blueprint（路由）
    app.register_blueprint(bp)

    # 啟動 Web server
    app.run(host="0.0.0.0", port=args.port)


if __name__ == "__main__":
    main()
