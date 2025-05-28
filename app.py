from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import subprocess
import requests
from monitor.cpu import cpu_picture_handler
from utils.whitelist import is_user_allowed
import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
app = ApplicationBuilder().token(BOT_TOKEN).build()
OPERATOR_URL = "http://host.docker.internal:8000/exec"

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

# 指令註冊
app.add_handler(CommandHandler("op_exec", op_exec))
app.add_handler(CommandHandler("op_stop", op_stop))
app.add_handler(cpu_picture_handler())  # /cpu_picture

if __name__ == "__main__":
    print("✅ Bot 開始運行")
    app.run_polling()
