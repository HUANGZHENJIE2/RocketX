import ctypes
import subprocess
import platform
from utils.resources import Resources
from myos import system
import os

def _start_forward_server_thread(cmd, status):
    system.call(cmd)
    return status


def setWebProxy(proxyServer, bypass: str):
    osname = platform.system()
    if osname in 'Windows':
        bypass = bypass.replace(" ", "").replace("\n", "")
        cmd = f'{Resources.getLibPath("sysproxy.exe")} global {proxyServer} {bypass}'
        system.call(cmd)
        return
    if osname in 'Darwin':
        # TODO : MAC OS 系列适配
        proxyServer = proxyServer.split(":")
        cmd = f"networksetup -setwebproxy Wi-Fi {proxyServer[0]} {proxyServer[1]}\n"
        cmd2 = f"networksetup -setproxybypassdomains Wi-Fi {bypass}"
        os.system(cmd)
        os.system(cmd2)
        return
    if osname in 'Linux':
        # TODO : Linux 系列适配
        bypass = bypass.replace(" ", "").replace("\n", "")
        proxyServer = proxyServer.split(":")
        off()
        cmd = f'gsettings set org.gnome.system.proxy.http host \'{proxyServer[0]}\' &' \
              f'gsettings set org.gnome.system.proxy.http port {proxyServer[1]} &' \
              f'gsettings set org.gnome.system.proxy mode \'manual\''
        system.call(cmd)
        return


def setAutoProxyUrl(url):
    osname = platform.system()
    if osname in 'Windows':
        cmd = f'{Resources.getLibPath("sysproxy.exe")} pac {url}'
        system.call(cmd)
        return
    if osname in 'Darwin':
        # TODO : MAC OS 系列适配
        cmd = f"networksetup -setautoproxyurl Wi-Fi {url}"
        os.system(cmd)
        return
    if osname in 'Linux':
        # TODO : Linux 系列适配
        off()
        cmd = f'gsettings set org.gnome.system.proxy autoconfig-url {url} &' \
              f'gsettings set org.gnome.system.proxy mode \'auto\''
        system.call(cmd)
        return


def off():
    osname = platform.system()
    if osname in 'Windows':
        cmd = f'{Resources.getLibPath("sysproxy.exe")} set 1'
        system.call(cmd)
        return
    if osname in 'Darwin':
        # TODO : MAC OS 系列适配
        cmd = "networksetup -setwebproxystate Wi-Fi off"
        os.system(cmd)
        return
    if osname in 'Linux':
        # TODO : Linux 系列适配
        cmd = 'gsettings set org.gnome.system.proxy mode \'none\''
        system.call(cmd)
        return

