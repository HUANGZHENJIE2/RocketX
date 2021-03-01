
tasks = {
    "build": {
        "cmds": [
            # "pyinstaller -F -w -i resources/app.ico main.py",
            "mv .values/** dist/",
            "mv .packages/** dist/"
        ]
    },
    "run": {klkkghgggfddssa `    
        "cmds": [
            "py main.py"
        ]
    },
    "install": {
        "cmds": [

        ]
    }
}

