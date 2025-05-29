# See-Server-Health
[TOC]
## 專案動機
在日常網站或伺服器管理中，管理人員不見得能隨時攜帶電腦，而一旦系統出現異常可能就已經錯過第一時間處理的最佳時機！為了解決這個問題，我們建立了一套整合 Telegram Bot 的監控與操作系統，能讓使用者能得到系統資源使用狀況（如 CPU、記憶體），並提供控制指令，也提供遠端控制網頁兩種方案做選擇，協助管理人員隨時掌握服務狀態並立即做出反應。
另外，也有即時警告，當有新的登入行為，將即時傳送給管理者，

以下為其主要功能：
- 操作控制：能按指令關閉指定 port 或執行 shell 命令
- 資源監控：對 CPU 與 Memory 使用率輸出圖表
- 即時警告：一旦有新的登入行為，即時傳送給管理者


## 流程圖
![image](https://hackmd.io/_uploads/S10sm_Bfel.png)


## 專案結構
```bash
See-Server-Health/
├── app.py                       
├── docker-compose.yml
├── requirements.txt
├── monitor/
│   ├── __init__.py
│   ├── cpu.py
│   └── ...
├── promethues/
│   ├── docker-compose.yml # 跑 promethues 相關的容器設定 
│   └── ...
├── control/
│   ├── __init__.py
│   ├── operator_agent.py
│   └── ...
└── utils/
    ├── __init__.py
    └── whitelist.py            
```
- `app.py`：Telegram Bot 的主程式，處理指令與回應。
- `docker-compose.yml`：定義了 Telegrame Bot 服務的容器設定，方便部署。
- `requirements.txt`：列出專案所需的 Python 套件。
- `monitor/`：包含 `login_alert.py`，用於監控 `/var/log/auth.log`，偵測登入行為並發送警告。
- `prometheus/`：Prometheus 的設定檔，用於收集 Server 指標。
- `control/`：包含 `op.py`，提供遠端操作功能。
- `utils/`：包含 `whitelist.py`，用於管理能使用此 Bot 的使用者清單。
- `start.sh`：啟動腳本，用於一次自動開啟各個服務。


## 使用方法
### Prerequisites
- Docker & Docker Compose
- Python 3.9+
- Telegram Bot Token
- 此專案會使用到的 port(使用時需避免撞到):
    - 3000: granfana
    - 8000: op.py
    - 9090: prometheus
    - 9093: alertmanager
    - 9100: node exproter

###  Environment
請在根目錄下新增 .env，內容包括：
```
BOT_TOKEN=<your_bot_token>
ALLOWED_USER_IDS=<your_telegram_id>
chat_id=<your_telegram_id>
```

#### Telegram Bot 教學
 :information_source: 如何獲得上述 `<your_bot_token>` 與 `your_telegram_id`，這邊教你如何新增自己的 Telegram Bot 
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

#### 網頁終端機架設教學
1. 去 https://ngrok.com/downloads/linux 下載 ngrok-v3-stable-windows-amd64
    - ![image](https://hackmd.io/_uploads/Hkan3FrGxg.png)
2. 解壓縮(通常在 Downloads/ 裡面)：`tar -xzvf ngrok-v3-stable-linux-amd64.tgz`
3. 在系統上安裝 ngrok:
    ```bash
    curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \ | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
  && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
  | sudo tee /etc/apt/sources.list.d/ngrok.list \
  && sudo apt update \
  && sudo apt install ngrok
    ```
4. 註冊 ngrok

### Usage
1. 下載 repo `git clone https://github.com/cyleafish/See-Server-Health.git`
2. `cd `進入資料夾並執行 `./start.sh`
3. 在 Telegram Bot 輸入 `/start` 得到通知(確認 Telegram Bot 有正確執行)
![image](https://hackmd.io/_uploads/H1GY2FSGle.png)

## DEMO 
### Telegram 按按鈕指令
#### 操作指令系列
- `/op_exec <cmd>` 執行任何 shell 指令(除了 sudo 指令)
    ![image](https://hackmd.io/_uploads/BJOr7kSzll.png)
    - 在訊息框輸入`/op_exec `後面接上要打的指令就會回傳結果 
- `/op_port` 查看目前有開啟的 port
    ![image](https://hackmd.io/_uploads/BkOq71HGxx.png)
    - 為了方便觀看，只會列出有開啟的 port，若要更詳細的資料可使用`/op_exec netstat -ntupl`來看
- `/op_stop <port>` 關閉指定 port
    ![image](https://hackmd.io/_uploads/Byj-VkBflx.png)

- `/more` 開啟瀏覽器的 terminal 以更方便的控制 server (FIXME: 待完成)
#### 資源監控
- CPU：
    - `/mon_cpu` 顯示當下的 CPU 使用率 
    - `/mon_cpu_picture ` 用圖表顯示 5 分鐘前到現在的 CPU 使用率
    - `/mon_cpu_picture <參數> ` 用圖表顯示 ? 分鐘前到現在的 CPU 使用率
        -  ![image](https://hackmd.io/_uploads/B1KnyJSGee.png)
    - `/mon_cpu_picture <時間> <參數> ` 用圖表顯示 <時間> 前後 ? 分鐘前到現在的 CPU 使用率


- MEMORY：
    - `/mon_mem` 顯示當下的 Memory 使用率 
    - `/mon_mem_picture ` 用圖表顯示 5 分鐘前到現在的 Memory 使用率
        - ![image](https://hackmd.io/_uploads/SkDJxJrzge.png)
    - `/mon_mem_picture <參數> ` 用圖表顯示 ? 分鐘前到現在的 Memory 使用率
    - `/mon_mem_picture <時間> <參數>` 用圖表顯示 <時間> 前後 ? 分鐘前到現在的 Memory 使用率
        
- DISK：
    - `/mon_disk` 顯示當下的 Disk 使用率 
    - `/mon_disk_picture ` 用圖表顯示 5 分鐘前到現在的 Disk 使用率
    - `/mon_disk_picture <參數> ` 用圖表顯示 ? 分鐘前到現在的 Disk 使用率
    - `/mon_disk_picture <時間> <參數> ` 用圖表顯示 <時間> 前後 ? 分鐘前到現在的 Disk 使用率
    ![image](https://hackmd.io/_uploads/SyAzg1SGgx.png)

#### 自動監測通報
- 登入警告
  - 當有人登入 Server (ssh...)，Telegram Bot 將自動傳送警告登入的訊息
     ![image](https://hackmd.io/_uploads/BJsNNyBfgg.png)
     
### 
`sudo apt update`
`sudo apt install ttyd`
`ttyd -p 8090 bash`
先去自己的虛擬機上開網頁輸入
http://<VM_IP>:8090
可以進入terminal畫面就可以了
去https://ngrok.com/downloads/linux下載ngrok-v3-stable-windows-amd64
在Downloads解壓縮
`curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \   | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \   && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \   | sudo tee /etc/apt/sources.list.d/ngrok.list \   && sudo apt update \   && sudo apt install ngrok`
ngrok config add-authtoken <token>`
>(這段token要去ngrok註冊拿)

`ngrok http 8090`(不能關)
開新視窗輸入
`sudo ttyd -p 8090 login`
在ngrok官網找到universal gateway->endpoints
裡面會有一串網址
帳號是虛擬機的帳號名，密碼就是密碼
## 未來展望
- 資安問題：因做的比較及時，並沒有考慮到太多資安問題(如：op_exec 權限太大)，應該要限制只能打那些指令，或給予特定的低權限使用者帳號。
- 更完整的操作介面與警告功能：可以從 telegram bot 介面設定當 CPU、Memory、Disk 使用率高達多少的時候通知
- 更詳細的資訊：例如 Disk 使用率過高，可以顯示是最
- AI 分析結果： 對比歷史資料，若偵測到異常流量，將會交給 AI 做判斷並給予操作建議。


## 資料來源
- [Prometheus Docker](https://github.com/vegasbrianc/prometheus)


## 小紀錄
- pip install python-telegram-bot requests

### /start
```
這裡是 SeeServerHealth，在這裡你可以即時監控與操作自己的 Server ，我們提供以下功能：

Server 控制
- /op_exec <cmd> 執行任何 shell 指令(除了 sudo 指令) 
- /op_port  查看目前有開啟的 port
- /op_stop <port> 關閉指定 port
- /more 開啟網頁終端機，可以操作更多功能

監控數據
 - /mon_cpu 顯示當下的 CPU 使用率
- /mon_cpu_picture  用圖表顯示 5 分鐘前到現在的 CPU 使用率
- /mon_cpu_picture <參數>  用圖表顯示 ? 分鐘前到現在的 CPU 使用率
- /mon_cpu_picture <時間> <參數>  用圖表顯示 <時間> 前後 ? 分鐘前到現在的 CPU 使用率

其中 cpu 可以換成 mem 或 disk 可以查看記憶體與磁碟使用率 
```
