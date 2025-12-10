import os
import json
import time
import crawler
from crawler import Crawler
from dotenv import load_dotenv
import requests

load_dotenv()

# 웹훅 URL 읽기
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# ================================
# Discord Webhook 전송 함수
# ================================
def send_discord_message(webhook_url, user_name, subjects):
    embed = {
        "title": "📘 새로운 성적이 등록되었습니다!",
        "description": f"**{user_name}님**, 아래 과목이 새롭게 등록되었습니다:\n\n[확인하러가기](https://sso.daegu.ac.kr/dgusso/ext/tigersstd/login_form.do?Return_Url=https://tigersstd.daegu.ac.kr/nxrun/ssoLogin.jsp) \n\n"
                       + "\n".join(f"• **{subject}**" for subject in subjects),
        "color": 0x2ecc71  # 초록색
    }

    payload = {
        "embeds": [embed]
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
    return response


# ================================
# 사용자 목록 로딩 (.env 기반)
# ================================
user_arr = []

i = 1
while True:
    user_key = f"USER{i}"
    user_json = os.getenv(user_key)
    if user_json is None:
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


# ================================
# 메인 루프
# ================================
while True:
    print("🔍 새 데이터 확인 시작")

    for crawler in user_arr:

        new_subjects = crawler.craw()  # 새로 생긴 과목 리스트 반환
        if new_subjects:
            message = f"📢 **[{crawler.get_user_name()}]님! 새로운 성적이 등록되었습니다!**\n"
            message += "\n".join(f"• {subject}" for subject in new_subjects)

            send_discord_message(WEBHOOK_URL, crawler.get_user_name(), new_subjects)

        print(new_subjects)

    time.sleep(60 * 60 * 3)  # 3시간 간격
