import json


def saveJson(path: str, content: list) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=3)


def loadJson(path: str) -> list:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)
