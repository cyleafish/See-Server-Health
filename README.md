# See-Server-Health

- pip install python-telegram-bot requests


# prometheus docker
- 執行
    - `sudo docker-compose up -d`
- prometheus_bot.py
    - telegram bot 的檔案
    - port :
        - 3000: granfana
        - 9090: prometheus
        - 9093: alertmanager
        - 9100: node exproter
