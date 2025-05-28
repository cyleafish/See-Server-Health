import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv("BOT_TOKEN", "")
chat_id = os.getenv("chat_id", "")

def send_tg_msg(text):
    res = requests.get(
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        params={
            "chat_id": chat_id,
            "text": text
        }
    )
    print(res.text)  # 印出回應，方便 debug

with open("/var/log/auth.log", "r") as f:
    f.seek(0, 2)  # 移到檔案結尾（追蹤模式）
    while True:
        line = f.readline()
        if any(kw in line for kw in ["Accepted password", "session opened", "New session", "sudo: pam_unix"]):
            send_tg_msg(f"⚠️ 有人登入：\n{line.strip()}")
        time.sleep(1)
