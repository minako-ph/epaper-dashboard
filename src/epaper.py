import os

from lib import epd5in65f
from PIL import Image, ImageFont, ImageDraw

epd = epd5in65f.EPD()
picdir = '../image'

font16 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 16)
font14 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 14)
font10 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 10)


def display_weather_dashboard():
    image = Image.open(os.path.join(picdir, 'page-0.jpg'))
    epd.display(epd.getbuffer(image))


def display_task_dashboard(tasks, items):
    # 背景画像の描画
    image = Image.open(os.path.join(picdir, 'page-1.jpg'))
    draw = ImageDraw.Draw(image)

    # アイテムを分割, 時間でソートされている前提
    before_now_items_str_list = []
    now_item_str = ''
    after_now_items_str_list = []
    for item in items:
        title = item['title']
        start_at = item['start_at']
        end_at = item['end_at']
        is_now = item['is_now']
        if is_now:
            now_item_str = f'{start_at}-{end_at}: {title}'
        elif now_item_str == '':
            before_now_items_str_list.append(f'{start_at}-{end_at}: {title}')
        else:
            after_now_items_str_list.append(f'{start_at}-{end_at}: {title}')
    # 文字列にする
    before_now_items_str = '\n'.join(before_now_items_str_list)
    after_now_items_str = '\n'.join(after_now_items_str_list)
    # それぞれの座標を取得
    before_box = draw.textbbox((10, 120), before_now_items_str,
                               font=font14, spacing=8)
    now_box = draw.textbbox((10, before_box[3] + 8), now_item_str,
                            font=font14, spacing=8)
    # 描画
    draw.text((10, 120), before_now_items_str,
              font=font14, fill=epd.BLACK, spacing=8)
    draw.text((10, before_box[3] + 8), now_item_str,
              font=font14, fill=epd.RED, spacing=8)
    draw.text((10, now_box[3] + 8), after_now_items_str,
              font=font14, fill=epd.BLACK, spacing=8)

    # 今日のタスク
    tasks_str_list = []
    for state in tasks.keys():
        tasks_str_list.append(f'【{state}】')
        items = tasks[state]
        for item in items:
            title = item['title']
            status = item['status']
            tasks_str_list.append(f'{status}:{title}')
    tasks_str = '\n'.join(tasks_str_list)
    draw.text((320, 100), tasks_str, font=font14, fill=epd.BLACK, spacing=8)

    epd.display(epd.getbuffer(image))


def display_goal_dashboard():
    # 背景画像の描画
    image = Image.open(os.path.join(picdir, 'page-2.jpg'))
    epd.display(epd.getbuffer(image))


def display_milestone_dashboard():
    image = Image.open(os.path.join(picdir, 'page-3.jpg'))
    epd.display(epd.getbuffer(image))
