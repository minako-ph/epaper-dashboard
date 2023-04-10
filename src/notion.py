import os
from notion_client import Client
from dotenv import load_dotenv
import datetime
from util import is_time_in_range

# .envファイルの読み込み
load_dotenv()


def get_daily_task_items():
    # Notion APIキーの設定
    notion = Client(auth=os.getenv("NOTION_API_KEY"))
    # データベースIDの設定
    database_id = os.getenv("DAILY_TASK_DATABASE_ID")

    # データベースからアイテムを取得
    results = notion.databases.query(
        **{
            "database_id": database_id,
            "filter": {
                "or": [
                    {
                        "property": "タスクの状態",
                        "formula": {
                            "string": {
                                "equals": "今日"
                            }
                        }
                    },
                    {
                        "property": "タスクの状態",
                        "formula": {
                            "string": {
                                "equals": "過去の未確認タスク"
                            }
                        }
                    }
                ]
            }
        }
    )
    result = {}
    # 結果を表示
    for item in results['results']:
        # json_str = json.dumps(item, indent=4, ensure_ascii=False)
        # print(json_str)
        key = item['properties']['タスクの状態']['formula']['string']
        title = item['properties']['name']['title'][0]['plain_text']
        status = item['properties']['ステータス']['status']['name']
        if key in result:
            result[key].append({
                'title': title,
                'status': status,
            })
        else:
            result[key] = [
                {
                    'title': title,
                    'status': status,
                }
            ]
    return result


def get_calendar_items():
    # Notion APIキーの設定
    notion = Client(auth=os.getenv("NOTION_API_KEY"))
    # データベースIDの設定
    database_id = os.getenv("CALENDAR_DATABASE_ID")

    today = datetime.date.today().isoformat()

    # データベースからアイテムを取得
    results = notion.databases.query(
        **{
            "database_id": database_id,
            "filter": {
                "and": [
                    {
                        "property": "start dt",
                        "date": {
                            "on_or_after": today
                        }
                    },
                    {
                        "property": "end dt",
                        "date": {
                            "on_or_before": today
                        }
                    },
                    {
                        "property": "is deleted",
                        "checkbox": {
                            "equals": False
                        }
                    }
                ],
            },
            "sorts": [
                {
                    "property": "start dt",
                    "direction": "ascending"
                }
            ]
        }
    )

    result = []
    # 結果を表示
    for item in results['results']:
        # json_str = json.dumps(item, indent=4)
        # print(json_str)
        start_at_str = item['properties']['start dt']['date']['start']
        end_at_str = item['properties']['end dt']['date']['start']
        start_at = datetime.datetime.fromisoformat(
            start_at_str).strftime("%#H:%M")
        end_at = datetime.datetime.fromisoformat(end_at_str).strftime("%#H:%M")
        is_now = is_time_in_range(start_at, end_at)
        result.append({
            'title': item['properties']['Name']['title'][0]['plain_text'],
            'start_at': start_at,
            'end_at': end_at,
            'is_now': is_now
        })
    return result
