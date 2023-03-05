import requests
import time
import socket
import os
from termcolor import colored
server_ip = socket.gethostbyname(socket.gethostname())
path = "~/"
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def send_command(cmd):
    global path
    if "cd" in cmd:
        if cmd == "cd ~" or cmd == "cd":
            path = "~/"
            return
        if cmd == "cd ..":
            path = path.strip().split("/")[:-1]
            path.pop()
            path = "/".join(path)
            path += "/"
            return
        else:
            path += cmd.split(" ")[1] + "/"
        return
    if path:
        cmd = f"cd {path} && {cmd}"
    requests.post(f"http://{server_ip}:8080/commands", data=cmd)


def get_result():
    res = requests.get(f"http://{server_ip}:8080/results").text
    if res: 
        return res
    time.sleep(1)
    return get_result()

def menu():
    print(
    """
    1. Start Shell
    2. Exit
    """
)

def beautify_shell():
    global user, hostname, path
    print(colored("[*] Beautifying shell...", "white", attrs=["bold"]))
    send_command("whoami")
    user = get_result().strip()
    send_command("hostname")
    hostname = get_result().strip()
    clear()
    print(colored("IMPORTANT: ", "red", attrs=['bold']), "This is not a real shell, and it is relatively unstable. Be careful :)", sep="")
    print("A list of custom commands is available by using the command ", colored("`$help`", "green", attrs=['bold']), ".\n", sep="")
    welcome_msg = f"[*] Welcome {colored(f'{user}@', 'green')}{colored(hostname, 'green')}"
    prompt = f"{colored(f'{user}@', 'green')}{colored(hostname, 'green')}{colored(':$ ', 'white')}"
    print(welcome_msg)
    print("[*] Type 'exit' to quit\n")
    return prompt

def shell():
    prompt = beautify_shell()
    while True:
        if path:
            prompt = f"{colored(f'{user}@', 'green')}{colored(hostname, 'green')}{colored(f':{path}$ ', 'white')}"
        cmd = input(prompt)
        if cmd == "exit":
            break
        if "cd" in cmd:
            send_command(cmd)
        else:
            send_command(cmd)
            result = get_result()
            print(colored(result, 'cyan'))
        
if(__name__ == "__main__"):
    while True:
        menu()
        choice = input(">> ")
        match choice:
            case "1":
                shell()
            case "2":
                break
