import datetime


def is_time_in_range(start: str, end: str) -> bool:
    current_time = datetime.datetime.now().time()
    start_time = datetime.datetime.strptime(start, '%H:%M').time()
    end_time = datetime.datetime.strptime(end, '%H:%M').time()

    if start_time < end_time:
        return start_time <= current_time <= end_time
    else:  # 時間範囲が翌日にまたがる場合
        return start_time <= current_time or current_time <= end_time
