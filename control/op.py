from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route("/exec", methods=["POST"])
def exec_cmd():
    data = request.json
    cmd = data.get("cmd", "")
    
    if "/op_stop" in cmd and "-p" in cmd:
        port = cmd.split("-p")[1].strip()
        try:
            pid = subprocess.check_output(f"lsof -ti tcp:{port}", shell=True).decode().strip()
            if pid:
                subprocess.run(f"kill -9 {pid}", shell=True)
                return jsonify({"result": f"✅ 已關閉 port {port}（PID: {pid})"})
            else:
                return jsonify({"result": f"⚠️ port {port} 無對應程序"})
        except Exception as e:
            return jsonify({"result": f"❌ 無法關閉 port：{e}"})

    if "/op_exec" in cmd:
        try:
            shell_cmd = cmd.replace("/op_exec", "").strip()
            output = subprocess.check_output(shell_cmd, shell=True).decode()
            return jsonify({"result": f"✅ 執行結果：\n{output}"})
        except subprocess.CalledProcessError as e:
            return jsonify({"result": f"❌ 錯誤：{e.output.decode()}"})
        except Exception as e:
            return jsonify({"result": f"❌ 其他錯誤：{e}"})
    
    if "/op_port" in cmd:
        try:
            output = subprocess.check_output("ss -tuln", shell=True).decode()
            ports = []
            for line in output.splitlines()[1:]:
                parts = line.split()
                if len(parts) >= 5:
                    addr_port = parts[4]
                    port = addr_port.split(":")[-1]
                    if port.isdigit():
                        ports.append(port)
            ports = sorted(set(ports), key=int)
            
            if ports:
                message = "📡 目前系統有以下 port 正在監聽：\n"
                for port in ports:
                    message += f"- Port {port}\n"
            else:
                message = "⚠️ 沒有偵測到任何正在監聽的 port"

            return jsonify({"result": message})
        except Exception as e:
            return jsonify({"result": f"❌ 查詢錯誤：{e}"})

    return jsonify({"result": "❓ 未知操作"})
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

