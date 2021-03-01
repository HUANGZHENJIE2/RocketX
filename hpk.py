import package
import os
if __name__ == '__main__':
    cmds = package.tasks["build"]["cmds"]
    for cmd in cmds:
        print("run "+cmd)
        os.system(cmd)