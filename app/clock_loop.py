# app/clock_loop.py
import time
from datetime import datetime
from .renderer import render_clock


def run_clock(display, width, height):
    """
    自動更新電子紙時鐘。
    interval：每幾秒更新一次（預設 60 秒）
    """
    print(f"[Clock] Starting clock loop, update interval = 60 sec")

    display.clear()   # 上電第一次先清一次

    last_key = None

    while True:
        now = datetime.now()
        key = now.strftime("%Y-%m-%d %H:%M")

        if key != last_key:
            # 時間「字串」變了 → 需要重畫
            img = render_clock(width, height)
            display.show_image(img)
            print(f"[Clock] Updated display at {key}")
            last_key = key

        # 小睡一下，避免狂燒 CPU
        time.sleep(0.5)
