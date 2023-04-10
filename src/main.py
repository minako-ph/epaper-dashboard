from concurrent.futures import ThreadPoolExecutor
import time
import evdev
from weather import get_weather
from lib import epd5in65f
import logging
import datetime
from deepdiff import DeepDiff

from epaper import display_task_dashboard, display_weather_dashboard
from notion import get_daily_task_items, get_calendar_items

logging.basicConfig(level=logging.DEBUG)
picdir = "../image"


def doProcess(currentIndex):
    try:
        if currentIndex == 0:
            today = datetime.date.today()
            weathers = get_weather()
            display_weather_dashboard(weathers, today)

            # 5分ごとにアイテムを取得
            while True:
                time.sleep(300)
                new_weathers = get_weather()
                new_today = datetime.date.today()
                if (
                    set(new_weathers) != set(weathers)
                    or today.date() != new_today.date()
                ):
                    # 差分があった場合もしくは日付が変わった場合は再描画
                    weathers = new_weathers
                    display_weather_dashboard(weathers, today)
                else:
                    continue

        if currentIndex == 1:
            # Notion itemの取得
            tasks = get_daily_task_items()
            items = get_calendar_items()
            # 初回実行
            display_task_dashboard(tasks, items)

            # 5分ごとにアイテムを取得
            while True:
                time.sleep(300)
                new_tasks = get_daily_task_items()
                new_items = get_calendar_items()
                has_diff_tasks = 'values_changed' in DeepDiff(new_tasks, tasks)
                has_diff_items = 'values_changed' in DeepDiff(new_items, items)
                if has_diff_tasks or has_diff_items:
                    # 差分があった場合は再描画
                    tasks = new_tasks
                    items = new_items
                    display_task_dashboard(tasks, items)
                else:
                    continue
    except IOError as e:
        logging.error(f"IO error occurred: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    except KeyboardInterrupt:
        logging.error("ctrl + c:")
        epd5in65f.epdconfig.module_exit()
        exit()


def getKeyEvent(currentIndex):
    device = None
    while True:
        try:
            if device is None:
                device = evdev.InputDevice("/dev/input/event0")
            for event in device.read_loop():
                print("evdev.ecodes.KEY[event.code]")
                print(evdev.ecodes.KEY[event.code])

                if event.type == evdev.ecodes.EV_KEY:
                    if event.value == 1:  # 0:KEYUP, 1:KEYDOWN, 2: LONGDOWN
                        if event.code == evdev.ecodes.KEY_A:
                            # 天気ダッシュボードの表示
                            currentIndex = 0
                            doProcess(currentIndex)
                        if event.code == evdev.ecodes.KEY_B:
                            # タスクダッシュボードの表示
                            currentIndex = 1
                            doProcess(currentIndex)
                        if event.code == evdev.ecodes.KEY_C:
                            # リロード
                            doProcess(currentIndex)
        except OSError as e:
            logging.error(f"Device error: {e}")
            if device:
                device.close()
                device = None
            time.sleep(1)  # 少し待ってから再試行


if __name__ == "__main__":
    # 初期化
    epd = epd5in65f.EPD()
    epd.init()
    epd.Clear()

    # 初回実行
    with ThreadPoolExecutor() as executor:
        currentIndex = 0
        executor.submit(doProcess, currentIndex)
        executor.submit(getKeyEvent, currentIndex)
