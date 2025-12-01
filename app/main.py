# app/main.py
import os
import argparse
from PIL import Image

from .display_base import BaseDisplay
from .display_waveshare import WaveshareEPDDisplay
from .display_mock import MockEPDDisplay
from .renderer import render_album


def create_display(mode: str) -> BaseDisplay:
    mode = mode.lower()
    if mode == "real":
        return WaveshareEPDDisplay(rotation=0)
    elif mode == "mock":
        # 解析度可以改成你螢幕的，或直接看 datasheet / epd.width/height
        return MockEPDDisplay(size=(800, 480), rotation=0)
    else:
        raise ValueError(f"Unknown mode: {mode}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["real", "mock"],
                        default=os.environ.get("EPD_MODE", "mock"),
                        help="real=樹莓派電子紙, mock=模擬器")
    args = parser.parse_args()

    display = create_display(args.mode)
    display.init()

    # 決定螢幕尺寸
    if args.mode == "real":
        # 真機用 epd 的尺寸
        assert isinstance(display, WaveshareEPDDisplay)
        width, height = display.size
    else:
        # 模擬用設定好的 size
        assert isinstance(display, MockEPDDisplay)
        width, height = display.size

    img = render_album("images/confuse.png",width, height)

    # 顯示
    display.clear()
    display.show_image(img)
    display.sleep()


if __name__ == "__main__":
    main()