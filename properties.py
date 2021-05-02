from utils.resources import Resources


class Properties:

    def __init__(self, propertiesPath: str = Resources.getValuesPath('strings')):
        self.properties: dict = None
        self.propertiesPath = propertiesPath
        self.load()

    def load(self):
        with open(self.propertiesPath, encoding="utf-8") as properties:
            self.toDict(properties)

        return

    def toDict(self, properties):
        for line in properties.readlines():
            line = line.strip().replace("\n", "")

            if line.find("#") != -1:
                line = line[0:line.find('#')]

            if line.find("=") > 0:
                strs = line.split('=')
                strs[1] = line[len(strs[0]) + 1:]

                if self.properties is None:
                    self.properties = {}
                strs[1] = strs[1].replace("\\n", "\n")
                self.properties[strs[0]] = strs[1]

    def __str__(self):
        print(f"properties load {self.propertiesPath}")
