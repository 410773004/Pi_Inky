# app/main.py
import os
import argparse
from PIL import Image

from .display_base import BaseDisplay
from .display_waveshare import WaveshareEPDDisplay
from .display_mock import MockEPDDisplay
from .renderer import render_album,render_clock
from .clock_loop import run_clock



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
                        default=os.environ.get("EPD_MODE", "mock"))
    parser.add_argument("--screen", choices=["album", "clock"], default="clock")
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

    if args.screen == "album":
        img = render_album("assets/images/confuse.png", width, height)
        display.clear()
        display.show_image(img)
        display.sleep()
    elif args.screen == "clock":
        run_clock(display, width, height)

if __name__ == "__main__":
    main()