# prometheus_bot.py

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

#chinese
import matplotlib.font_manager as fm

# 設定中文字體
plt.rcParams['font.family'] = 'Noto Sans CJK JP'
plt.rcParams['axes.unicode_minus'] = False  # 避免負號顯示錯誤
BOT_TOKEN = ''

PROMETHEUS_URL = 'http://localhost:9090'

def parse_cpu_picture_args(args):
    now = datetime.now()
    
    if not args:
        # 沒有參數，預設抓「現在 - 5分鐘」到「現在」
        end = now
        start = now - timedelta(minutes=5)
    elif len(args) == 1:
        # 一個參數：/cpu_picture 1940
        center = datetime.strptime(args[0], "%H%M").replace(
            year=now.year, month=now.month, day=now.day
        )
        start = center - timedelta(minutes=5)
        end = center + timedelta(minutes=5)
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

async def cpu_picture(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 查詢 CPU 使用率的圖片
    try:
        args = context.args
        start, end = parse_cpu_picture_args(args)

        # 傳給 Prometheus 查詢，畫圖
        chart_path = draw_cpu_usage_chart(start, end)

        update.message.reply_photo(photo=open(chart_path, 'rb'))

    except Exception as e:
        update.message.reply_text(f"⚠️ 指令錯誤：{e}")

    query = '100 - (avg by (instance)(rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)'
    response = requests.get(
        f"{PROMETHEUS_URL}/api/v1/query_range",
        params={
            "query": query,
            "start": start.timestamp(),
            "end": end.timestamp(),
            "step": 15
        }
    )

    data = response.json()['data']['result']
    if not data:
        await update.message.reply_text("找不到 CPU 資料，請確認 Prometheus 有啟動並且抓到 node_exporter。")
        return

    timestamps = [datetime.fromtimestamp(float(x[0])) for x in data[0]['values']]
    values = [float(x[1]) for x in data[0]['values']]

    # 繪圖
    plt.figure(figsize=(10, 4))
    plt.plot(timestamps, values, label='CPU Usage %', color='green', linewidth=3, linestyle='--')
    plt.title('CPU 使用率 ')
    plt.xlabel('時間')
    plt.ylabel('%')
    plt.ylim(0, 100)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('cpu_usage.png')
    plt.close()
    # 發送圖片
    await update.message.reply_photo(photo=open('cpu_usage.png', 'rb'))

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("cpu_picture", cpu_picture))

print("✅ Telegram Bot 開始運行")
app.run_polling()
