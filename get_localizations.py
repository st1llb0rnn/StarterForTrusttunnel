import json

def out_en():
    with open("./localization/en.json", "r", encoding="utf-8") as file:
        return json.load(file)

def out_ru():
    with open("./localization/ru.json", "r", encoding="utf-8") as file:
        return json.load(file)
