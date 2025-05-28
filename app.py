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
    ["/op_exec who", "/op_port", "/op_stop -p 80"],
    ["/mon_cpu", "/mon_cpu_picture", "/mon_cpu_picture 20"],
    ["/mon_mem", "/mon_mem_picture", "/mon_mem_picture 20"],
    ["/mon_disk", "/mon_disk_picture", "/mon_disk_picture 20"],
    ["/more"]
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


# /start 指令時顯示自訂鍵盤
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
            "這裡是 SeeServerHealth，請選擇指令，下為指令說明: \n mon_cpu 為看當前cpu usage %數",
        reply_markup=reply_markup
    )


# 指令註冊
# app.add_handler(CommandHandler("op_exec", op_exec))
# app.add_handler(CommandHandler("op_stop", op_stop))
# app.add_handler(cpu_picture_handler())  # /cpu_picture

app.add_handler(CommandHandler("start", start))

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
