from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import subprocess
import requests

from prometheus_bot import mon_cpu_picture

OPERATOR_AGENT_URL = "http://localhost:8000/exec"  # 你本機跑的控制 API

async def handle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    if user_input.startswith("/mon_"):
        await update.message.reply_text("🧪 這是監控指令，由本容器處理")
        # TODO: 加上本地處理邏輯（CPU, RAM 等）
    
    elif user_input.startswith("/op_"):
        await update.message.reply_text("🛠️ 這是操作指令，轉送給 operator agent")
        try:
            # 呼叫本機 operator agent 的 API（需先啟動 Flask app）
            res = requests.post(OPERATOR_AGENT_URL, json={"cmd": user_input})
            await update.message.reply_text(res.text)
        except Exception as e:
            await update.message.reply_text(f"❌ 呼叫操作 agent 失敗：{e}")
    
    else:
        await update.message.reply_text("🤔 不明指令格式，請用 /mon_ 或 /op_ 作為開頭")

# 建立 bot 應用
app = ApplicationBuilder().token("<Yourtoken>").build()
app.add_handler(CommandHandler("mon_status", handle_command))
app.add_handler(CommandHandler("op_stop", handle_command))
app.add_handler(CommandHandler("op_exec", handle_command))
app.add_handler(CommandHandler("mon_cpu_picture", mon_cpu_picture))
app.run_polling()
