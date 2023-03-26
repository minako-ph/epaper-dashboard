import os

from weather import get_contents_coordinates, get_weather_icon
from lib import epd5in65f
from PIL import Image, ImageFont, ImageDraw
import datetime
from util import get_japanese_weekday

epd = epd5in65f.EPD()
picdir = '../image'

font40 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 40)
font16 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 16)
font14 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 14)
font10 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 10)


def display_weather_dashboard(weathers, today):
    image = Image.open(os.path.join(picdir, 'page-0.jpg'))
    combined_image = Image.new('RGB', (epd.width, epd.height),
                               0xffffff)  # 255: clear the frame
    combined_image.paste(image, (0, 0))
    draw = ImageDraw.Draw(combined_image)

    # 日付
    today = datetime.date.today()
    day = get_japanese_weekday(today)
    date_str = today.strftime(f'%Y年%m月%d日 ({day})')
    draw.text((140, 100), date_str, font=font40, fill='#6F6F6F', spacing=8)

    # 座標
    coordinates = get_contents_coordinates()

    for index, weather in enumerate(weathers):
        coordinate = coordinates[index]
        # 天気アイコン
        image_coordinate = coordinate['image']
        weather_id = weather['weather_id']
        icon = get_weather_icon(weather_id)
        icon_path = os.path.join(picdir, icon)
        icon_image = Image.open(icon_path)
        combined_image.paste(
            icon_image, (image_coordinate['x'], image_coordinate['y']))
        # 曜日
        day_coordinate = coordinate['day']
        day = weather['day']
        draw.text((day_coordinate['x'], day_coordinate['y']), day,
                  font=font14, fill=epd.BLACK, spacing=8)
        # 気温
        temperature_coordinate = coordinate['temperature']
        max_temp = weather["max_temp"]
        min_temp = weather["min_temp"]
        temp = f'{min_temp}°/{max_temp}°'
        draw.text(
            (temperature_coordinate['x'], temperature_coordinate['y']),
            temp,
            font=font14,
            fill=epd.BLACK,
            spacing=8
        )

    epd.display(epd.getbuffer(combined_image))


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
    # 初期化
    epd = epd5in65f.EPD()
    epd.init()
    epd.Clear()
    # 背景画像の描画
    image = Image.open(os.path.join(picdir, 'page-2.jpg'))
    epd.display(epd.getbuffer(image))


def display_milestone_dashboard():
    # 初期化
    epd = epd5in65f.EPD()
    epd.init()
    epd.Clear()
    image = Image.open(os.path.join(picdir, 'page-3.jpg'))
    epd.display(epd.getbuffer(image))

