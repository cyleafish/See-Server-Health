# See-Server-Health
## 專案動機
在日常網站或伺服器管理中，管理人員不見得能隨時攜帶電腦，而一旦系統出現異常可能就已經錯過第一時間處理的最佳時機！為了解決這個問題，我們建立了一套整合 Telegram Bot 的監控與操作系統，能讓使用者能得到系統資源使用狀況（如 CPU、記憶體），並提供控制指令，也提供遠端控制網頁兩種方案做選擇，協助管理人員隨時掌握服務狀態並立即做出反應。
另外，也有即時警告，當有新的登入行為，將即時傳送給管理者，
FIXME:異常警告



以下為其主要功能：
- 操作控制：能按指令關閉指定 port 或執行 shell 命令
- 資源監控：對 CPU 與 Memory 使用率輸出圖表
- 即時警告：一旦有新的登入行為，即時傳送給管理者
- FIXME: 異常警告：對比歷史資料，若偵測到異常流量，將會交給 AI 做判斷並給予操作建議

## Prerequisites
Docker & Docker Compose
Python 3.9+
Telegram Bot Token
FIXME: 待補

##  Environment
請在根目錄下新增 .env，內容包括：
```
BOT_TOKEN=<your_bot_token>
ALLOWED_USER_IDS=<your_telegram_id>
chat_id=<your_telegram_id>
```


## 使用方法
### Telegram 按按鈕指令
#### 操作指令系列
- `/op_exec <cmd>` 執行任何 shell 指令(除了 sudo 指令)
- `/op_stop -p <port>` 關閉指定 port 

#### 資源監控圖表
- `/mon_cpu_picture ` 用圖表顯示 CPU 情況
- `/mon_mem_picture ` 用圖表顯示 Memory 情況

#### 登入監控訊息
當有人登入 Linux 系統 (ssh...)，Telegram Bot 將自動傳送告訊


### 小紀錄
- pip install python-telegram-bot requests
