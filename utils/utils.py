cache = {}


def read_text_file(filePath:str):
    text = ""
    key = filePath.replace("/", "_",1000).replace("\\","_",1000)
    if key in cache:
        return cache[key]
    with open(filePath, encoding="utf-8") as textFile:
        print(f"read text from {filePath}")
        for line in textFile.readlines():
            text = text + line
    cache[key] = text
    return text

def write_text_file():
    pass