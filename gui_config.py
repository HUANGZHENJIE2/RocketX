import json

from utils.resources import Resources


class GuiConfig:
    def __init__(self, configPath: str = Resources.getConfigPath('gui-config.json')):
        self.guiConfig: dict = None
        self.configPath = configPath
        self.load()

    def load(self):
        with open(self.configPath, encoding="utf-8") as guiConfig:
            self.guiConfig = json.load(guiConfig)
        return

    def write(self):
        with open(self.configPath, 'w', encoding="utf-8") as guiConfig:
            json.dump(self.guiConfig, guiConfig, ensure_ascii=False)
        return

    def writeNewJsonFile(self, key, file):
        value = self.guiConfig[key]
        with open(Resources.getConfigPath(file), 'w', encoding="utf-8") as guiConfig:
            json.dump(value, guiConfig, ensure_ascii=False)
        return

    def __str__(self):
        print(f"config load {self.configPath}")