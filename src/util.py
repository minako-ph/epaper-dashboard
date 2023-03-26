import datetime


def is_time_in_range(start: str, end: str) -> bool:
    current_time = datetime.datetime.now().time()
    start_time = datetime.datetime.strptime(start, '%H:%M').time()
    end_time = datetime.datetime.strptime(end, '%H:%M').time()

    if start_time < end_time:
        return start_time <= current_time <= end_time
    else:  # 時間範囲が翌日にまたがる場合
        return start_time <= current_time or current_time <= end_time


def get_japanese_weekday(dt: datetime.datetime) -> str:
    japanese_weekdays = ["月", "火", "水", "木", "金", "土", "日"]
    weekday = dt.weekday()  # 0:月曜日, 1:火曜日, ..., 6:日曜日
    return japanese_weekdays[weekday]
