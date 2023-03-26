from concurrent.futures import ThreadPoolExecutor
import time
import evdev
from lib import epd5in65f
import logging

from epaper import display_task_dashboard, display_weather_dashboard
from notion import get_daily_task_items, get_calendar_items
logging.basicConfig(level=logging.DEBUG)
picdir = '../image'


def doProcess(currentIndex):
    try:
        if currentIndex == 0:
            display_weather_dashboard()
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

                if set(new_tasks) != set(tasks) or set(new_items) != set(items):
                    # 差分があった場合は再描画
                    display_task_dashboard(new_tasks, new_items)
                    tasks = new_tasks
                    items = new_items
    except IOError as e:
        logging.info(e)
    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd5in65f.epdconfig.module_exit()
        exit()


def getKeyEvent(currentIndex):
    while True:
        try:
            device = evdev.InputDevice('/dev/input/event0')
            for event in device.read_loop():

                print('evdev.ecodes.KEY[event.code]')
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
                            # TODO: リロード
                            # もし差分があれば実行
                            doProcess(currentIndex)
        except:
            print('Retry...')
            time.sleep(1)


if __name__ == '__main__':
    # 初期化
    epd = epd5in65f.EPD()
    epd.init()
    epd.Clear()

    # 初回実行
    with ThreadPoolExecutor() as executor:
        currentIndex = 1
        executor.submit(doProcess, currentIndex)
        executor.submit(getKeyEvent, currentIndex)
