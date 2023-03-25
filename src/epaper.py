import os

from lib import epd5in65f
from PIL import Image, ImageFont, ImageDraw

epd = epd5in65f.EPD()
picdir = '../image'

font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 16)


def display_page_1(tasks, items):
    # 背景画像の描画
    image = Image.open(os.path.join(picdir, 'page-2.jpg'))
    draw = ImageDraw.Draw(image)

    # Notionアイテムを描画
    for index, item in enumerate(tasks):
        status = item['status']
        title = item['title']
        draw.text((325, 100 + index * 24),
                  f'{status}:{title}', font=font, fill=epd.BLACK)

    for index, item in enumerate(items):
        title = item['title']
        start_at = item['start_at']
        end_at = item['end_at']
        draw.text((10, 120 + index * 24),
                  f'{start_at} - {end_at}: {title}', font=font, fill=epd.BLACK)

    epd.display(epd.getbuffer(image))
