# See-Server-Health
`sudo apt update`  
`sudo apt install ttyd`  
`ttyd -p 8090 bash`  
先去自己的虛擬機上開網頁輸入  
http://<VM_IP>:8090  
可以進入terminal畫面就可以了  
去https://ngrok.com/downloads/linux下載ngrok-v3-stable-windows-amd64  
在Downloads解壓縮  
`curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \  
  | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \  
  && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \  
  | sudo tee /etc/apt/sources.list.d/ngrok.list \  
  && sudo apt update \  
  && sudo apt install ngrok`   
`ngrok config add-authtoken <token>`(這段token要去ngrok註冊拿)  
`ngrok http 8090`(不能關)  
開新視窗輸入  
`sudo ttyd -p 8090 login`  
在ngrok官網找到universal gateway->endpoints  
裡面會有一串網址  
帳號是虛擬機的帳號名，密碼就是密碼  
