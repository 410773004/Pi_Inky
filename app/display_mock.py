# app/display_mock.py
import os
import time
from pathlib import Path
from PIL import Image
from .display_base import BaseDisplay


class MockEPDDisplay(BaseDisplay):
    def __init__(self, size=(800, 480), out_dir="sim_output", rotation: int = 0):
        self.size = size
        self.out_dir = Path(out_dir)
        self.rotation = rotation
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self.frame_id = 0

    def init(self) -> None:
        print("[MockEPD] init")

    def clear(self) -> None:
        print("[MockEPD] clear (no-op)")

    def show_image(self, img: Image.Image) -> None:
        w, h = self.size
        img = img.convert("RGB").resize((w, h))
        img.show()

    def sleep(self) -> None:
        print("[MockEPD] sleep")