
import _thread

from myos import system
from myos import sysproxy
from utils.resources import Resources
import time
from services import pac_server
import subprocess
import platform

def _start_server_thread(cmd, status):
    system.call(cmd)
    return status


def start_forward_server():
    kill_forward_server()
    time.sleep(1)
    osname = platform.system()
    if osname in 'Windows':
        _thread.start_new_thread(_start_server_thread,
                                 (Resources.getLibPath("xray.exe") + ' -c ./config/config.json', 0))
        return
    if osname in 'Darwin':
        # TODO : MAC OS 系列适配
        _thread.start_new_thread(_start_server_thread,
                                 (Resources.getLibPath("xray") + ' -c ./config/config.json', 0))
        return
    if osname in 'Linux':
        # TODO : Linux 系列适配
        _thread.start_new_thread(_start_server_thread,
                                 (Resources.getLibPath("xray") + ' -c ./config/config.json', 0))
        return



def start_pac_server(host, port):
    _thread.start_new_thread(
        pac_server.start_,
        (host, port)
    )


def kill_forward_server():
    cmd = "taskkill /F /IM xray.exe"
    osname = platform.system()
    if osname in 'Windows':
        cmd = "taskkill /F /IM xray.exe"

    if osname in 'Darwin':
        cmd = "kill -9 $(pidof xray)"

    if osname in 'Linux':
        cmd = "kill -9 $(pidof xray)"
    system.call(cmd)

