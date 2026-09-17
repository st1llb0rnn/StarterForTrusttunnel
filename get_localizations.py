import json
from pathlib import Path

from for_create_localization_file import for_en_file as f_en_f
from for_create_localization_file import for_ru_file as f_ru_f
from for_create_localization_file import for_status_file as f_s_f
from for_create_localization_file import for_settings_file as f_set_f

# Все пути считаем от папки со скриптом, а не от текущей рабочей директории.
# Иначе приложение ломается, если запустить его не из корня проекта.
BASE_DIR = Path(__file__).resolve().parent
LOCALIZATION_DIR = BASE_DIR / "localization"
SETTINGS_PATH = BASE_DIR / "settings.json"


def _save_json(path: Path, data: dict) -> None:
    """Записывает словарь в json-файл (папку создаёт при необходимости)"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        file.write(json.dumps(data, indent=4, ensure_ascii=False))


def _load_json(path: Path, defaults: dict) -> dict:
    """Читает json-файл. Если его нет или он битый - создаёт из defaults.
    Если в файле не хватает ключей (старая версия файла) - дописывает их."""
    data = {}
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as file:
                loaded = json.load(file)
            if isinstance(loaded, dict):
                data = loaded
        except (json.JSONDecodeError, OSError):
            data = {}

    # Значения из файла важнее дефолтных, но недостающие ключи добавляются
    merged = {**defaults, **data}
    if merged != data:
        _save_json(path, merged)
    return merged


def out_en() -> dict:
    """Английская локализация"""
    return _load_json(LOCALIZATION_DIR / "en.json", f_en_f())


def out_ru() -> dict:
    """Русская локализация"""
    return _load_json(LOCALIZATION_DIR / "ru.json", f_ru_f())


def file_with_status(do: str = "get", edit_status: str | None = None) -> dict:
    """do="get" - прочитать текущий язык, do="edit" - сохранить новый"""
    path = LOCALIZATION_DIR / "status.json"
    if do == "edit":
        data = {"Status": edit_status}
        _save_json(path, data)
        return data
    return _load_json(path, f_s_f())


def choise_language(l_: str) -> dict:
    """Возвращает словарь строк для указанного языка"""
    if l_ == "russian":
        return out_ru()
    # english и любое непонятное значение -> английский
    return out_en()


def get_settings() -> dict:
    """Читает сохранённые настройки (путь к папке и имя конфига)"""
    return _load_json(SETTINGS_PATH, f_set_f())


def save_settings(path_to_folder: str, config_name: str) -> dict:
    """Сохраняет настройки в settings.json"""
    data = {
        "PathToFolder": path_to_folder,
        "ConfigName": config_name,
    }
    _save_json(SETTINGS_PATH, data)
    return data
