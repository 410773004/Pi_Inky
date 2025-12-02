from datetime import datetime
import time
from .renderer import render_clock
def run_clock(display, width, height, stop_event):
    """
    可停止的時鐘循環（用 stop_event 控制）
    每秒檢查一次分鐘是否改變，只有變化時才重新繪製。
    """
    print(f"[Clock] Starting clock loop (60 sec update)")

    display.clear()   # 上電第一次清除

    last_key = None

    while not stop_event.is_set():
        now = datetime.now()
        key = now.strftime("%Y-%m-%d %H:%M")   # 只看到 "分鐘"

        if key != last_key:
            # 分鐘變了 → 需要重畫
            img = render_clock(width, height)
            display.show_image(img)
            print(f"[Clock] Updated at {key}")
            last_key = key

        # 小睡一下（0.5秒），避免 CPU 狂跑
        time.sleep(0.5)

    print("[Clock] Clock loop stopped.")

