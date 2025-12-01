# app/display_waveshare.py
from typing import Optional
from PIL import Image
from .display_base import BaseDisplay


class WaveshareEPDDisplay(BaseDisplay):
    def __init__(self, rotation: int = 0):
        # rotation: 0 / 90 / 180 / 270
        from waveshare_epd import epd7in3e  # 只在 Pi 上 import

        self.epd_module = epd7in3e
        self.epd: Optional[epd7in3e.EPD] = None
        self.rotation = rotation

    def init(self) -> None:
        self.epd = self.epd_module.EPD()
        self.epd.init()
        self.epd.Clear()

    @property
    def size(self) -> tuple[int, int]:
        assert self.epd is not None
        return (self.epd.width, self.epd.height)

    def clear(self) -> None:
        assert self.epd is not None
        self.epd.Clear()

    def show_image(self, img: Image.Image) -> None:
        assert self.epd is not None
        # 依照螢幕尺寸縮放
        w, h = self.size
        img = img.convert("RGB").resize((w, h))

        if self.rotation:
            img = img.rotate(self.rotation, expand=True)

        self.epd.display(self.epd.getbuffer(img))

    def sleep(self) -> None:
        assert self.epd is not None
        self.epd.sleep()