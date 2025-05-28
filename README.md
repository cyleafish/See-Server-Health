# See-Server-Health
[TOC]
## 專案動機
在日常網站或伺服器管理中，管理人員不見得能隨時攜帶電腦，而一旦系統出現異常可能就已經錯過第一時間處理的最佳時機！為了解決這個問題，我們建立了一套整合 Telegram Bot 的監控與操作系統，能讓使用者能得到系統資源使用狀況（如 CPU、記憶體），並提供控制指令，也提供遠端控制網頁兩種方案做選擇，協助管理人員隨時掌握服務狀態並立即做出反應。
另外，也有即時警告，當有新的登入行為，將即時傳送給管理者，
> FIXME:異常警告

以下為其主要功能：
- 操作控制：能按指令關閉指定 port 或執行 shell 命令
- 資源監控：對 CPU 與 Memory 使用率輸出圖表
- 即時警告：一旦有新的登入行為，即時傳送給管理者
> FIXME: 異常警告：對比歷史資料，若偵測到異常流量，將會交給 AI 做判斷並給予操作建議
## 流程圖
> FIXME
## 專案結構
- `app.py`：Telegram Bot 的主程式，處理指令與回應。
- `monitor/`：包含 `login_alert.py`，用於監控 `/var/log/auth.log`，偵測登入行為並發送警告。
- `control/`：包含 `op.py`，提供遠端操作功能。
- `prometheus/`：Prometheus 的設定檔，用於收集 Server 指標。
- `utils/`：包含 `whitelist.py`，用於管理能使用此 Bot 的使用者清單。
- `docker-compose.yml`：定義了 Telegrame Bot 服務的容器設定，方便部署。
- `requirements.txt`：列出專案所需的 Python 套件。
- `start.sh`：啟動腳本，用於一次自動開啟各個服務。

## 使用方法
### Prerequisites
Docker & Docker Compose
Python 3.9+
Telegram Bot Token
> FIXME: 待補

###  Environment
請在根目錄下新增 .env，內容包括：
```
BOT_TOKEN=<your_bot_token>
ALLOWED_USER_IDS=<your_telegram_id>
chat_id=<your_telegram_id>
```
ℹ️ 如何獲得上述 token 與 id，這邊教你如何新增自己的 Telegram Bot 🏃
- 打開 Telegram，搜尋 @BotFather
![image](https://hackmd.io/_uploads/Syc9dXXCyx.png)
- 傳送指令 /start、然後 /newbot
- 根據提示輸入：
    - Bot 名稱（例如：MyMonitorBot）
    - 使用者名稱（結尾需是 bot，如：my_monitor_bot）
- 你會拿到一個 Bot Token：
![image](https://hackmd.io/_uploads/rkJ124KC1x.png)
- 找到你的 bot 輸入 /start
![image](https://hackmd.io/_uploads/H1Vg_7XR1e.png)
- 在瀏覽器輸入
`https://api.telegram.org/bot<YourBotToken>/getUpdates` 並找出 id
![image](https://hackmd.io/_uploads/rkFLn4tRJe.png)
- 把 toker 與 id 輸入
`https://api.telegram.org/bot<YourBotToken>/sendMessage?chat_id=<ChatID>&text=HelloAlert`
![image](https://hackmd.io/_uploads/ry0ZG_5C1g.png)
- 得到通知(確認 Telegram Bot 有正確執行)
![image](https://hackmd.io/_uploads/H1ib9mmAyg.png)

### Usage
1. 下載 repo
2. 進入資料夾並執行 `./start.sh`

> FIXME:寫詳細？
開啟 Telegram Bot 後輸入 `/start` 就可以輸入指令啦！

## DEMO
> FIXXME:寫詳細
### Telegram 按按鈕指令
#### 操作指令系列
- `/op_exec <cmd>` 執行任何 shell 指令(除了 sudo 指令)
- `/op_stop -p <port>` 關閉指定 port
- `/more` 開啟瀏覽器的 terminal 以更方便的控制 server (FIXME: 待完成)
#### 資源監控圖表
- CPU：
    - `/mon_cpu` 顯示當下的 CPU 使用率 
    - `/mon_cpu_picture ` 用圖表顯示 5 分鐘前到現在的 CPU 使用率
    - `/mon_cpu_picture <參數> ` 用圖表顯示 <?> 分鐘前到現在的 CPU 使用率
    - `/mon_cpu_picture <時間> <參數> ` 用圖表顯示 <時間> 前後 <?> 分鐘前到現在的 CPU 使用率
- MEMORY：
    - `/mon_mem_picture ` 用圖表顯示 5 分鐘前到現在的 Memory 使用率
    - `/mon_mem_picture <參數> ` 用圖表顯示 <?> 分鐘前到現在的 Memory 使用率
    - `/mon_mem_picture <時間> <參數> ` 用圖表顯示 <時間> 前後 <?> 分鐘前到現在的 Memory 使用率
- DISK：
    - `/mon_disk_picture ` 用圖表顯示 5 分鐘前到現在的 Disk 使用率
    - `/mon_disk_picture <參數> ` 用圖表顯示 <?> 分鐘前到現在的 Disk 使用率
    - `/mon_disk_picture <時間> <參數> ` 用圖表顯示 <時間> 前後 <?> 分鐘前到現在的 Disk 使用率
#### 自動監測通報
- 登入警告
  - 當有人登入 Server (ssh...)，Telegram Bot 將自動傳送告訊

### 未來展望

### 小紀錄
- pip install python-telegram-bot requests
