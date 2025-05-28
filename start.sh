#!/bin/bash
echo "🔧 啟動 Prometheus 監控服務..."
cd prometheus
docker compose up -d



echo "🤖 啟動 Telegram Bot..."
cd ..
docker compose up -d

echo "🛠️ 啟動 Operation 操作..."
cd control
python3 op.py &


echo "⚠️ 啟動 Alert 操作..."
cd ..
cd monitor
sudo python3 login_alert.py


