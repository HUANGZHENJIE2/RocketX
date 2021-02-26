import os
from resources import Resources


def _start_forward_server_thread(cmd, status):
    os.system(cmd)
    return status


def setWebProxy(proxyServer, bypass: str):
    bypass = bypass.replace(" ", "").replace("\n", "")
    cmd = f'{Resources.getLibPath()}\\sysproxy.exe global {proxyServer} {bypass}'
    print(cmd)
    os.system(cmd)


def setAutoProxyUrl(url):
    cmd = f'{Resources.getLibPath()}\\sysproxy.exe pac {url}'
    print(cmd)
    os.system(cmd)


def off():
    cmd = f'{Resources.getLibPath()}\\sysproxy.exe off'
    print(cmd)
    os.system(cmd)
