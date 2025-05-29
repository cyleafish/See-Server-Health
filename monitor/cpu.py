# cpu.py

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from utils.whitelist import is_user_allowed

#chinese
import matplotlib.font_manager as fm

# 設定中文字體
plt.rcParams['font.family'] = 'Noto Sans CJK JP'
plt.rcParams['axes.unicode_minus'] = False  # 避免負號顯示錯誤



PROMETHEUS_URL = "http://host.docker.internal:9090"


def parse_cpu_picture_args(args):
    now = datetime.now()

    if not args:
        # 沒有參數，預設抓「現在 - 5分鐘」到「現在」
        end = now
        start = now - timedelta(minutes=5)
    elif len(args) == 1:
        # 一個參數：/cpu_picture 40
        end = now
        start = now - timedelta(minutes=int(args[0]))
    elif len(args) == 2:
        # 兩個參數：/cpu_picture 1940 10
        center = datetime.strptime(args[0], "%H%M").replace(
            year=now.year, month=now.month, day=now.day
        )
        offset = int(args[1])
        start = center - timedelta(minutes=offset)
        end = center + timedelta(minutes=offset)
    else:
        raise ValueError("參數格式錯誤")

    return start, end

#當下的 cpu usage
async def mon_cpu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = '100 - (avg by (instance)(rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)'
    response = requests.get(
        f"{PROMETHEUS_URL}/api/v1/query",
        params={"query": query}
    )

    result = response.json().get('data', {}).get('result', [])
    if not result:
        return "⚠️ 找不到即時 CPU 使用資料"

    # 可能有多個 instance，這邊只取第一個
    value = float(result[0]['value'][1])
    timestamp = datetime.fromtimestamp(float(result[0]['value'][0]))
    await update.message.reply_text(f"🖥️ 即時 CPU 使用率：{value:.2f}%（時間：{timestamp.strftime('%H:%M:%S')}）")


async def mon_cpu_picture(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_user_allowed(update.effective_user.id):
        await update.message.reply_text("🚫 你沒有權限使用此功能")
        return

    try:
        start, end = parse_cpu_picture_args(context.args)
        response = requests.get(f"{PROMETHEUS_URL}/api/v1/query_range", params={
            "query": '100 - (avg by (instance)(rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)',
            "start": start.timestamp(),
            "end": end.timestamp(),
            "step": 15
        })
        result = response.json()['data']['result']
        if not result:
            await update.message.reply_text("Prometheus 沒有資料")
            return
        timestamps = [datetime.fromtimestamp(float(x[0])) for x in result[0]['values']]
        values = [float(x[1]) for x in result[0]['values']]
        plt.figure(figsize=(10, 4))
        plt.plot(timestamps, values, label='CPU Usage %', color='green')
        plt.title('CPU Usage')
        plt.xlabel('time')
        plt.ylabel('%')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("cpu.png")
        plt.close()
        await update.message.reply_photo(photo=open("cpu.png", "rb"))
    except Exception as e:
        await update.message.reply_text(f"❌ 發生錯誤：{e}")

def cpu_picture_handler():
    return CommandHandler("mon_cpu_picture", mon_cpu_picture)
