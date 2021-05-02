import package
import myos
if __name__ == '__main__':
    cmds = package.tasks["build"]["cmds"]
    for cmd in cmds:
        print("run "+cmd)
        myos.system(cmd)