from telegram import Update,ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import subprocess
import requests

from monitor.cpu import mon_cpu_picture, mon_cpu
from monitor.mem import mon_mem_picture, mon_mem
from monitor.disk import mon_disk_picture, mon_disk
from utils.whitelist import is_user_allowed
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
app = ApplicationBuilder().token(BOT_TOKEN).build()

OPERATOR_URL = "http://host.docker.internal:8000/exec"

#按鈕
custom_keyboard = [
    ["/op_exec ps", "/op_port", "/op_stop"],
    ["/more"],
    ["/mon_cpu", "/mon_cpu_picture", "/mon_cpu_picture 20"],
    ["/mon_mem", "/mon_mem_picture", "/mon_mem_picture 20"],
    ["/mon_disk", "/mon_disk_picture", "/mon_disk_picture 20"],
    ["/more_info_GitHub"]
]

reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)


# /op_exec 指令
async def op_exec(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_user_allowed(update.effective_user.id):
        await update.message.reply_text("🚫 沒有權限")
        return

    cmd = "/op_exec " + " ".join(context.args)
    try:
        response = requests.post(OPERATOR_URL, json={"cmd": cmd})
        result = response.json().get("result", "❓ 沒有回應內容")
        await update.message.reply_text(result)
    except Exception as e:
        await update.message.reply_text(f"❌ 呼叫控制 API 失敗：{e}")

# /op_stop 指令
async def op_stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_user_allowed(update.effective_user.id):
        await update.message.reply_text("🚫 沒有權限")
        return

    if not context.args:
        await update.message.reply_text("⚠️ 請指定 port，例如 /op_stop 8080")
        return

    cmd = f"/op_stop -p {context.args[0]}"
    try:
        response = requests.post(OPERATOR_URL, json={"cmd": cmd})
        result = response.json().get("result", "❓ 沒有回應內容")
        await update.message.reply_text(result)
    except Exception as e:
        await update.message.reply_text(f"❌ 呼叫控制 API 失敗：{e}")

# /op_port 指令
async def op_port(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_user_allowed(update.effective_user.id):
        await update.message.reply_text("🚫 沒有權限")
        return

    cmd = "/op_port"
    try:
        response = requests.post(OPERATOR_URL, json={"cmd": cmd})
        result = response.json().get("result", "❓ 沒有回應內容")
        await update.message.reply_text(result)
    except Exception as e:
        await update.message.reply_text(f"❌ 呼叫控制 API 失敗：{e}")

start_test="""
這裡是 SeeServerHealth，在這裡你可以即時監控與操作自己的 Server ，我們提供以下功能：\n
Server 控制
- /op_exec <cmd> 執行任何 shell 指令(除了 sudo 指令) 
- /op_port  查看目前有開啟的 port
- /op_stop <port> 關閉指定 port
- /more 開啟網頁終端機，可以操作更多功能\n
監控數據
- /mon_cpu 顯示當下的 CPU 使用率
- /mon_cpu_picture  用圖表顯示 5 分鐘前到現在的 CPU 使用率
- /mon_cpu_picture <參數>  用圖表顯示 ? 分鐘前到現在的 CPU 使用率
- /mon_cpu_picture <時間> <參數>  用圖表顯示 <時間> 前後 ? 分鐘前到現在的 CPU 使用率
其中 cpu 可以換成 mem 或 disk 可以查看記憶體與磁碟使用率 
"""

# /start 指令時顯示自訂鍵盤
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
            start_test,
        reply_markup=reply_markup
    )

# server terminal
async def more(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_user_allowed(update.effective_user.id):
        await update.message.reply_text("🚫 沒有權限")
        return

    web_terminal_url = "https://573a-2001-e10-6840-107-e453-e7ba-3530-6c08.ngrok-free.app"
    out_text = "🔗 請點以下網址開啟並登入\n" + web_terminal_url
    await update.message.reply_text(
        out_text,
        reply_markup=reply_markup
    )

#GitHub link
async def more_info_GitHub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    web_terminal_url="https://github.com/cyleafish/See-Server-Health/tree/main"
    out_text= "請點以下網址查看 GitHub\n"+web_terminal_url
    await update.message.reply_text(
            out_text,
        reply_markup=reply_markup
    )

# 指令註冊
# app.add_handler(CommandHandler("op_exec", op_exec))
# app.add_handler(CommandHandler("op_stop", op_stop))
# app.add_handler(cpu_picture_handler())  # /cpu_picture

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("more", more))
app.add_handler(CommandHandler("more_info_GitHub", more_info_GitHub))

app.add_handler(CommandHandler("op_exec", op_exec))
app.add_handler(CommandHandler("op_stop", op_stop))
app.add_handler(CommandHandler("op_port", op_port))

app.add_handler(CommandHandler("mon_cpu", mon_cpu))
app.add_handler(CommandHandler("mon_cpu_picture", mon_cpu_picture))

app.add_handler(CommandHandler("mon_mem", mon_mem))
app.add_handler(CommandHandler("mon_mem_picture", mon_mem_picture))

app.add_handler(CommandHandler("mon_disk", mon_disk))
app.add_handler(CommandHandler("mon_disk_picture", mon_disk_picture))

if __name__ == "__main__":
    print("✅ Bot 開始運行")
    app.run_polling()
