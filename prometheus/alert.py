from datetime import datetime, timedelta
import requests
import time
import os
import threading
import socket
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

PROMETHEUS_HOST = "host.docker.internal"  # 或 "prometheus" 若與其同一個 network
PROMETHEUS_PORT = 9090
# PROMETHEUS_URL = f"http://{PROMETHEUS_HOST}:{PROMETHEUS_PORT}"
PROMETHEUS_URL = "http://prometheus:9090"
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
CHAT_ID = os.getenv("ALLOWED_USER_IDS", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

def send_tg_msg(text):
    try:
        requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            params={"chat_id": CHAT_ID, "text": text}
        )
    except Exception as e:
        print(f"❌ Telegram 發送失敗：{e}")

def wait_for_prometheus(host="host.docker.internal", port=9090, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection((host, port), timeout=5):
                print("✅ Prometheus is up.")
                return True
        except Exception:
            print("⌛ 等待 Prometheus 開啟...")
            time.sleep(3)
    raise RuntimeError("❌ 等待 Prometheus 超時")

def get_prometheus_value(query, start, end, step=60):
    try:
        r = requests.get(f"{PROMETHEUS_URL}/api/v1/query_range", params={
            "query": query,
            "start": start.timestamp(),
            "end": end.timestamp(),
            "step": step
        })
        data = r.json()
        if data["status"] == "success" and data["data"]["result"]:
            values = data["data"]["result"][0]["values"]
            return [float(v[1]) for v in values if v[1] != "NaN"]
    except Exception as e:
        print(f"❌ Prometheus 查詢錯誤：{e}")
    return []

def call_gemini(prompt):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        return result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "❓ AI 回應失敗")
    except Exception as e:
        return f"❌ Gemini 呼叫失敗：{e}"

def check_anomaly():
    now = datetime.utcnow()
    five_minutes_ago = now - timedelta(minutes=5)
    one_hour_ago = now - timedelta(hours=1)

    # CPU 查詢
    cpu_query = '100 - (avg by(instance)(rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)'
    cpu_recent = get_prometheus_value(cpu_query, five_minutes_ago, now)
    cpu_history = get_prometheus_value(cpu_query, one_hour_ago, now)

    # 網路流量查詢（總進出流量）
    net_query = 'rate(node_network_receive_bytes_total[1m]) + rate(node_network_transmit_bytes_total[1m])'
    net_recent = get_prometheus_value(net_query, five_minutes_ago, now)
    net_history = get_prometheus_value(net_query, one_hour_ago, now)

    alerts = []

    if cpu_recent and cpu_history:
        recent_avg = sum(cpu_recent) / len(cpu_recent)
        history_avg = sum(cpu_history) / len(cpu_history)
        if recent_avg > history_avg * 2.5:
            alerts.append(f"CPU 使用率異常（近 5 分鐘 {recent_avg:.2f}% > 歷史平均 {history_avg:.2f}%）")

    if net_recent and net_history:
        recent_avg = sum(net_recent) / len(net_recent)
        history_avg = sum(net_history) / len(net_history)
        if recent_avg > history_avg * 3:
            alerts.append(f"網路流量異常（近 5 分鐘 {recent_avg:.2f} bytes/sec > 歷史平均 {history_avg:.2f}）")

    if alerts:
        prompt = "伺服器偵測到以下異常情形，請分析可能原因並提出操作建議：\n" + "\n".join(alerts)
        result = call_gemini(prompt)
        send_tg_msg(f"⚠️ 異常偵測！\n\n{prompt}\n\n🤖 Gemini 建議：\n{result}")

def schedule_loop():
    wait_for_prometheus(PROMETHEUS_HOST, PROMETHEUS_PORT)
    while True:
        check_anomaly()
        time.sleep(300)

if __name__ == "__main__":
    print("📡 啟動定時異常偵測...")
    thread = threading.Thread(target=schedule_loop)
    thread.start()
