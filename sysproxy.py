import ctypes
import os
import subprocess
import winreg

import win32con

from resources import Resources


def _start_forward_server_thread(cmd, status):
    call(cmd)
    return status


def setWebProxy(proxyServer, bypass: str):
    bypass = bypass.replace(" ", "").replace("\n", "")
    cmd = f'{Resources.getLibPath("sysproxy.exe")} global {proxyServer} {bypass}'
    print(cmd)
    call(cmd)


def setAutoProxyUrl(url):
    cmd = f'{Resources.getLibPath("sysproxy.exe")} pac {url}'
    call(cmd)


def off():
    cmd = f'{Resources.getLibPath("sysproxy.exe")} set 1'
    call(cmd)


def call(cmd):
    print(cmd)
    os.system(cmd)

