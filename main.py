import os
import json
import time
import crawler
from crawler import Crawler
from dotenv import load_dotenv


load_dotenv()
import requests

# .env로 설정해야 하는 부분.
token = os.getenv("token")
chat_id = os.getenv("chat_id")


def send_telegram_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    response = requests.post(url, data=payload)
    return response


user_arr = []

i = 1
while True:
    user_key = f"USER{i}"
    user_json = os.getenv(user_key)
    if user_json is None:
        # 더 이상 유저 데이터가 없으면 종료
        break

    try:
        user_data = json.loads(user_json)
    except json.JSONDecodeError:
        print(f"{user_key} JSON 디코딩 실패")
        i += 1
        continue

    user_name = user_data["name"]
    user_id = user_data["id"]
    user_passwd = user_data["passwd"]

    user_arr.append(Crawler(user_id, user_passwd, user_name))
    i += 1

while True:
    print("🔍 새 데이터 확인 시작")

    for crawler in user_arr:

        new_subjects = crawler.craw()  # 새로 생긴 과목 리스트 반환
        if new_subjects:
            message = f"📢 [{crawler.get_user_name()}]님! 새로운 과목이 성적 등록되었습니다:\n"
            message += "\n".join(f"• {subject}" for subject in new_subjects)
            send_telegram_message(token, chat_id, message)
        print(new_subjects)

    time.sleep(60 * 60 * 3)  # 3분
