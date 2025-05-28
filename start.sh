#!/bin/bash
echo "🔧 啟動 Prometheus 監控服務..."
cd prometheus
docker compose up 

echo "🤖 啟動 Telegram Bot..."
cd ..
docker compose up

echo "🤖 啟動 Operation 操作..."
cd control
python3 op.py


