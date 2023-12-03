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
            logging.info("Fetching initial weather data.")
            today = datetime.date.today()
            weathers = get_weather()
            logging.info("Displaying initial weather dashboard.")
            display_weather_dashboard(weathers, today)

            # 5分ごとにアイテムを取得
            while True:
                time.sleep(300)
                logging.info("Fetching new weather data.")
                new_weathers = get_weather()
                new_today = datetime.date.today()
                
                if today != new_today:  # 日付が変わったかを確認
                    logging.info("Date changed, redrawing dashboard")
                    today = new_today
                    display_weather_dashboard(weathers, today)
                elif set(new_weathers) != set(weathers):  # 天気データが変わったかを確認
                    logging.info("Weather data changed, redrawing dashboard")
                    weathers = new_weathers
                    display_weather_dashboard(weathers, today)
                else:
                    logging.info("No changes detected in weather data, no update needed.")

        if currentIndex == 1:
            # Notion itemの取得
            logging.info("Fetching initial Notion items for tasks and calendar.")
            tasks = get_daily_task_items()
            items = get_calendar_items()
            # 初回実行
            logging.info("Displaying initial task dashboard.")
            display_task_dashboard(tasks, items)

            # 5分ごとにアイテムを取得
            while True:
                time.sleep(300)
                logging.info("Fetching new Notion items for tasks and calendar.")
                new_tasks = get_daily_task_items()
                new_items = get_calendar_items()
                
                # DeepDiffを使用してタスクとアイテムの差分を検出
                has_diff_tasks = 'values_changed' in DeepDiff(new_tasks, tasks)
                has_diff_items = 'values_changed' in DeepDiff(new_items, items)
                
                if has_diff_tasks or has_diff_items:
                    # 差分があった場合は再描画
                    logging.info("Changes detected, updating task dashboard.")
                    tasks = new_tasks
                    items = new_items
                    display_task_dashboard(tasks, items)
                else:
                    logging.info("No changes detected, no update needed.")
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
                logging.info("Attempting to open input device.")
                device = evdev.InputDevice("/dev/input/event0")
            for event in device.read_loop():
                logging.info(f"Key event detected: {evdev.ecodes.KEY[event.code]}, value: {event.value}")

                if event.type == evdev.ecodes.EV_KEY:
                    if event.value == 1:  # 0:KEYUP, 1:KEYDOWN, 2: LONGDOWN
                        if event.code == evdev.ecodes.KEY_A:
                            # 天気ダッシュボードの表示
                            logging.info("KEY_A pressed, switching to weather dashboard.")
                            currentIndex = 0
                            doProcess(currentIndex)
                        if event.code == evdev.ecodes.KEY_B:
                            # タスクダッシュボードの表示
                            logging.info("KEY_B pressed, switching to task dashboard.")
                            currentIndex = 1
                            doProcess(currentIndex)
                        if event.code == evdev.ecodes.KEY_C:
                            # リロード
                            logging.info("KEY_C pressed, reloading current dashboard.")
                            doProcess(currentIndex)
        except OSError as e:
            logging.error(f"Device error: {e}")
            if device:
                device.close()
                device = None
            logging.info("Retrying to open input device after 1 second.")
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
