import logging
import os

from epaper import display_page_1
from notion import get_daily_task_items, get_calendar_items
from lib import epd5in65f
from PIL import Image
import evdev
import time


logging.basicConfig(level=logging.DEBUG)
picdir = '../image'


def doProcess(idx):
    try:
        if idx == 0:
            Page_1 = Image.open(os.path.join(picdir, 'page-1.jpg'))
            epd.display(epd.getbuffer(Page_1))
        if idx == 1:
            # Notion itemの取得
            tasks = get_daily_task_items()
            items = get_calendar_items()
            # 初回実行
            display_page_1(tasks, items)

            # 5分ごとにアイテムを取得
            while True:
                time.sleep(300)
                new_tasks = get_daily_task_items()
                new_items = get_calendar_items()
        if idx == 2:
            page_3 = Image.open(os.path.join(picdir, 'page-3.jpg'))
            epd.display(epd.getbuffer(page_3))
        if idx == 3:
            page_3 = Image.open(os.path.join(picdir, 'page-4.jpg'))
            epd.display(epd.getbuffer(page_3))
    except IOError as e:
        logging.info(e)
    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd5in65f.epdconfig.module_exit()
        exit()


if __name__ == '__main__':
    # 初期化
    epd = epd5in65f.EPD()
    epd.init()
    epd.Clear()

    # 初回実行
    currentIndex = 1
    doProcess(currentIndex)

    while True:
        try:
            device = evdev.InputDevice('/dev/input/event0')
            for event in device.read_loop():

                print('evdev.ecodes.KEY[event.code]')
                print(evdev.ecodes.KEY[event.code])

                if event.type == evdev.ecodes.EV_KEY:
                    if event.value == 1:  # 0:KEYUP, 1:KEYDOWN, 2: LONGDOWN
                        if event.code == evdev.ecodes.KEY_A:
                            # トップページを表示
                            doProcess(0)
                        if event.code == evdev.ecodes.KEY_B:
                            # 次のページに移動
                            if currentIndex < 3:
                                currentIndex = currentIndex + 1
                            else:
                                currentIndex = 0

                            # 新しいプロセスの取得
                            doProcess(currentIndex)

                        if event.code == evdev.ecodes.KEY_C:
                            # TODO: リロード
                            # もし差分があれば実行
                            doProcess(currentIndex)
        except:
            print('Retry...')
            time.sleep(1)
