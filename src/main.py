#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
picdir = '../image'

import sys
sys.path.append('../')
import logging
from lib import epd5in65f
from PIL import Image,ImageDraw,ImageFont
import evdev
import subprocess
import time

logging.basicConfig(level=logging.DEBUG)

def doProcess(idx):
    try:
        if idx == 0:
            Page_1 = Image.open(os.path.join(picdir, 'page-1.jpg'))
            epd.Clear()
            epd.display(epd.getbuffer(Page_1))
        if idx == 1:
            Page_2 = Image.open(os.path.join(picdir, 'page-2.jpg'))
            epd.display(epd.getbuffer(Page_2))
        if idx == 2:
            Page_3 = Image.open(os.path.join(picdir, 'page-3.jpg'))
            epd.display(epd.getbuffer(Page_3))
        if idx == 3:
            Page_3 = Image.open(os.path.join(picdir, 'page-4.jpg'))
            epd.display(epd.getbuffer(Page_3))
        
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

    # 初回実行
    currentIndex = 0
    doProcess(currentIndex)

    while True:
        try:
            device = evdev.InputDevice('/dev/input/event0')
            for event in device.read_loop():
                print('evdev.ecodes.KEY[event.code]')
                print(evdev.ecodes.KEY[event.code])
                if event.type == evdev.ecodes.EV_KEY:
                    if event.value == 1: # 0:KEYUP, 1:KEYDOWN, 2: LONGDOWN
                        if event.code == evdev.ecodes.KEY_A:
                            doProcess(0)
                        if event.code == evdev.ecodes.KEY_B:
                            # 参照するプロセスのIndexを更新
                            if currentIndex < 3:
                                currentIndex = currentIndex + 1
                            else :
                                currentIndex = 0

                            # 新しいプロセスの取得
                            doProcess(currentIndex)

                        if event.code == evdev.ecodes.KEY_C:
                            # 参照するプロセスのIndexを更新
                            if currentIndex > 0:
                                currentIndex = currentIndex - 1
                            else :
                                currentIndex = 3

                            # 新しいプロセスの取得
                            doProcess(currentIndex)

        except:
            print('Retry...')
            time.sleep(1)
  