import os
import _thread

import sysproxy
from resources import Resources
import time
import pac_server
import subprocess


def _start_server_thread(cmd, status):
    sysproxy.call(cmd)
    return status


def start_forward_server():
    kill_forward_server()
    time.sleep(1)
    _thread.start_new_thread(_start_server_thread,
                             (Resources.getLibPath("xray.exe") + ' -c ./config/config.json', 0))


def start_pac_server(host, port):
    _thread.start_new_thread(
        pac_server.start_,
        (host, port)
    )


def kill_forward_server():
    cmd = "taskkill /F /IM xray.exe"
    sysproxy.call(cmd)

