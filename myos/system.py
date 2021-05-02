import platform
import os
import subprocess
from utils.utils import write_text_file


def call(cmd):
    print(cmd)
    osname = platform.system()
    if osname in 'Windows':
        subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, shell=False,
                         creationflags=subprocess.CREATE_NO_WINDOW)
        return
    if osname in 'Darwin':
        # TODO : MAC OS 系列适配
        os.system(cmd)
        return
    if osname in 'Linux':
        # TODO : Linux 系列适配
        os.system(cmd)
        return


def setStartBoot():
    cmd = ""
    osname = platform.system()
    if osname in 'Windows':
        # TODO widows
        return
    if osname in 'Darwin':
        # TODO : MAC OS 系列适配
        os.system(cmd)
        return
    if osname in 'Linux':
        # TODO : Linux 系列适配
        # write_text_file(
        #     f'{os.os.getcwd()}/start.sh',
        #
        # )
        return
