from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
import requests, matplotlib.pyplot as plt
from datetime import datetime, timedelta
from utils.whitelist import is_user_allowed

PROMETHEUS_URL = "http://host.docker.internal:9090"


def parse_cpu_picture_args(args):
    now = datetime.now()
    if not args:
        end = now
        start = now - timedelta(minutes=5)
    else:
        center = datetime.strptime(args[0], "%H%M").replace(
            year=now.year, month=now.month, day=now.day)
        offset = int(args[1]) if len(args) > 1 else 5
        start = center - timedelta(minutes=offset)
        end = center + timedelta(minutes=offset)
    return start, end

async def cpu_picture(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        plt.title('CPU 使用率')
        plt.xlabel('時間')
        plt.ylabel('%')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("cpu.png")
        plt.close()
        await update.message.reply_photo(photo=open("cpu.png", "rb"))
    except Exception as e:
        await update.message.reply_text(f"❌ 發生錯誤：{e}")

def cpu_picture_handler():
    return CommandHandler("cpu_picture", cpu_picture)
