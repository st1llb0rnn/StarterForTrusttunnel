import os
import json
from for_create_localization_file import for_en_file as f_en_f
from for_create_localization_file import for_ru_file as f_ru_f
from for_create_localization_file import for_status_file as f_s_f

def out_en():
    path = "./localization/en.json" # Path of file
    data = f_en_f() # Data for create file
    # If not exists file, create en.json
    if not os.path.exists(path):
        create_file = json.dumps(data, indent=4)
        # Create file in ./localization
        with open(path, "w") as file:
            file.write(create_file)

        # Read file
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        # Read file
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

def out_ru():
    path = "./localization/ru.json" # Path of file
    data = f_ru_f() # Data for create file
    # If not exists file, create ru.json
    if not os.path.exists(path):
        create_file = json.dumps(data, indent=4)
        # Create file in ./localization
        with open(path, "w") as file:
            file.write(create_file)

        # Read file
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        # Read file
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

def get_file_with_status():
    path = "./localization/status.json" # Path of file
    data = f_s_f() # Data for create file
    # If not exists file, create status.json
    if not os.path.exists(path):
        create_file = json.dumps(data, indent=4)
        # Create file in ./localization
        with open(path, "w") as file:
            file.write(create_file)

        # Read file
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        # Read file
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

def choise_language(l_):
    if l_ == "english":
        return out_en()
    elif l_ == "russian":
        return out_ru()
