import os
import subprocess
import sys
from pathlib import Path

from get_localizations import out_en, out_ru, choise_language, get_settings, save_settings
from get_localizations import file_with_status as fws

from textual import work
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import (
    Header, Footer, Static, Button, Link, Collapsible, Input, RichLog
)
from pyfiglet import figlet_format

# Variables for changing the language in the application
l_en = out_en()  # English
l_ru = out_ru()  # Russian
l_ = fws("get")["Status"]
cl = choise_language(l_)

# Имя исполняемого файла Trusttunnel
EXE_NAME = "trusttunnel_client.exe" if sys.platform == "win32" else "trusttunnel_client"


class StarterForTrusttunnel(App):
    CSS_PATH = "style.tcss"  # Styles for app
    BINDINGS = [("c", "choise_lang", "Choise language")]  # Binds for app

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Текущий язык интерфейса (словарь строк) и его название ("english"/"russian")
        self.current_lang_name = l_
        self.current_lang = cl
        # Запущенный процесс туннеля и флаг его состояния
        self.process: subprocess.Popen | None = None
        self.tunnel_is_running = False

    def compose(self) -> ComposeResult:
        l = self.current_lang
        yield Header()
        yield Container(
            Container(
                Static(figlet_format(text=l["MainTitle"], font="rectangles"), classes="main_title"),
                Horizontal(
                    Button(l["ButtonForStart"], id="start_btn", classes="button"),
                    Button(l["ButtonForOpenFolder"], id="open_folder_btn", classes="button"),
                    classes="buttons",
                ),
                classes="block",
            ),
            Container(
                Collapsible(
                    Horizontal(
                        Input(placeholder=l["PathToFolder"], id="path_to_folder", classes="input"),
                        Input(placeholder=l["ConfigName"], id="config_name", classes="input"),
                        classes="inputs"
                    ),
                    Container(
                        Button(l["Confirm"], id="confirm_settings", classes="button btn_confirm"),
                        classes="block_for_button_confirm"
                    ),
                    collapsed=True,
                    title=l["SettingsTitle"],
                    id="settings_collapsible",
                    classes="collapsible"
                ),
                Collapsible(
                    RichLog(id="logs", classes="logs", markup=False, highlight=False, wrap=True, max_lines=2000),
                    Container(
                        Button(l["ClearLogs"], id="clear_logs_btn", classes="button btn_confirm"),
                        classes="block_for_button_confirm"
                    ),
                    collapsed=True,
                    title=l["LogsTitle"],
                    id="logs_collapsible",
                    classes="collapsible"
                ),
                Horizontal(
                    Link("GitHub", url="https://github.com/st1llb0rnn/StarterForTrusttunnel"),
                    Link("Forgejo", url="https://forgejo.st1llb0rn.ru.net/st1llb0rn/StarterForTrusttunnel"),
                    classes="links",
                ),
                classes="block",
            ),
            classes="container",
        )
        yield Footer()

    def on_mount(self) -> None:
        """Подставляем сохранённые настройки в поля ввода при запуске"""
        settings = get_settings()
        self.query_one("#path_to_folder", Input).value = settings.get("PathToFolder", "")
        self.query_one("#config_name", Input).value = settings.get("ConfigName", "")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start_btn":
            # Одна кнопка на запуск и остановку
            if self.tunnel_is_running:
                self.stop_tunnel()
            else:
                self.start_tunnel()
        elif event.button.id == "open_folder_btn":
            self.open_tt_folder()
        elif event.button.id == "confirm_settings":
            self.confirm_settings()
        elif event.button.id == "clear_logs_btn":
            self.query_one("#logs", RichLog).clear()

    # ---------- Логи ----------

    def write_log(self, text: str) -> None:
        """Пишет строку в Collapsible с логами"""
        self.query_one("#logs", RichLog).write(text)

    # ---------- Запуск / остановка туннеля ----------

    def start_tunnel(self) -> None:
        l = self.current_lang

        if self.process is not None and self.process.poll() is None:
            self.notify(l["AlreadyRunning"])
            return

        folder = self.query_one("#path_to_folder", Input).value.strip().strip('"')
        config = self.query_one("#config_name", Input).value.strip()

        if not folder or not config:
            self.notify(l["FillSettings"], severity="warning")
            self.query_one("#settings_collapsible", Collapsible).collapsed = False
            return

        exe = Path(folder).expanduser() / EXE_NAME
        if not exe.exists():
            message = f'{l["ExeNotFound"]} {exe}'
            self.notify(message, severity="error")
            self.write_log(message)
            self.query_one("#logs_collapsible", Collapsible).collapsed = False
            return

        # Разворачиваем логи, чтобы вывод было видно сразу
        self.query_one("#logs_collapsible", Collapsible).collapsed = False
        self.write_log(f'$ "{exe}" -c {config}')
        self.notify(l["StartTunnel"])

        self.run_tunnel_process(exe, config)

    @work(thread=True, exclusive=True, group="tunnel")
    def run_tunnel_process(self, exe: Path, config: str) -> None:
        """Запускает процесс в отдельном потоке и построчно шлёт его вывод в логи"""
        l = self.current_lang

        # На Windows прячем отдельное консольное окно процесса
        creationflags = 0
        if sys.platform == "win32":
            creationflags = subprocess.CREATE_NO_WINDOW

        try:
            process = subprocess.Popen(
                [str(exe), "-c", config],
                cwd=str(exe.parent),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # ошибки идут в тот же поток, что и вывод
                stdin=subprocess.DEVNULL,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1,  # построчная буферизация, чтобы логи шли в реальном времени
                creationflags=creationflags,
            )
        except OSError as e:
            # 740 - процессу нужны права администратора
            if getattr(e, "winerror", None) == 740:
                self.call_from_thread(self.write_log, l["NeedAdmin"])
                self.call_from_thread(self.notify, l["NeedAdmin"], severity="error")
            else:
                message = f'{l["FailedToStart"]} {e}'
                self.call_from_thread(self.write_log, message)
                self.call_from_thread(self.notify, message, severity="error")
            return

        self.process = process
        self.call_from_thread(self.set_running_state, True)

        # Читаем вывод построчно, пока процесс жив
        if process.stdout is not None:
            for line in process.stdout:
                self.call_from_thread(self.write_log, line.rstrip())

        code = process.wait()
        self.process = None
        self.call_from_thread(self.set_running_state, False)
        self.call_from_thread(self.write_log, f'{l["ProcessExited"]} {code}')

    def stop_tunnel(self) -> None:
        """Мягко останавливает процесс, при необходимости убивает"""
        l = self.current_lang
        process = self.process
        if process is None or process.poll() is not None:
            self.set_running_state(False)
            return

        try:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
        except OSError as e:
            self.write_log(f"{e}")

        self.notify(l["Disconnected"])

    def set_running_state(self, running: bool) -> None:
        """Переключает состояние кнопки между 'Подключиться' и 'Отключиться'"""
        self.tunnel_is_running = running
        l = self.current_lang
        button = self.query_one("#start_btn", Button)
        button.label = l["ButtonForStop"] if running else l["ButtonForStart"]
        if running:
            self.notify(l["Connected"])

    def on_unmount(self) -> None:
        """При закрытии приложения не оставляем процесс висеть"""
        process = self.process
        if process is not None and process.poll() is None:
            try:
                process.terminate()
            except OSError:
                pass

    # ---------- Папка и настройки ----------

    def open_tt_folder(self) -> None:
        # Открываем папку из настроек, а если она не задана - папку со скриптом
        folder_value = self.query_one("#path_to_folder", Input).value.strip().strip('"')
        folder = Path(folder_value).expanduser() if folder_value else Path(__file__).parent
        try:
            if sys.platform == "win32":
                os.startfile(folder)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", folder])
            else:
                subprocess.Popen(["xdg-open", folder])
        except Exception as e:
            self.notify(f'{self.current_lang["FailedToOpenFolder"]} {e}', severity="error")

    def confirm_settings(self) -> None:
        """Сохраняет введённые данные в settings.json"""
        folder = self.query_one("#path_to_folder", Input).value.strip().strip('"')
        config = self.query_one("#config_name", Input).value.strip()
        save_settings(folder, config)
        self.notify(self.current_lang["SettingsSaved"])
        self.query_one("#settings_collapsible", Collapsible).collapsed = True

    # ---------- Язык ----------

    def action_choise_lang(self) -> None:
        # Переключаем язык на противоположный
        new_lang_name = "russian" if self.current_lang_name == "english" else "english"

        # Сохраняем выбор в status.json, чтобы при следующем запуске приложение
        # открылось сразу на этом языке
        fws("edit", new_lang_name)

        self.current_lang_name = new_lang_name
        self.current_lang = choise_language(new_lang_name)

        self.refresh_texts()

    def refresh_texts(self) -> None:
        """Обновляет все видимые тексты интерфейса на self.current_lang"""
        l = self.current_lang

        self.query_one(".main_title", Static).update(
            figlet_format(text=l["MainTitle"], font="rectangles")
        )
        # Надпись на кнопке зависит от того, запущен ли сейчас туннель
        self.query_one("#start_btn", Button).label = (
            l["ButtonForStop"] if self.tunnel_is_running else l["ButtonForStart"]
        )
        self.query_one("#open_folder_btn", Button).label = l["ButtonForOpenFolder"]
        self.query_one("#path_to_folder", Input).placeholder = l["PathToFolder"]
        self.query_one("#config_name", Input).placeholder = l["ConfigName"]
        self.query_one("#confirm_settings", Button).label = l["Confirm"]
        self.query_one("#clear_logs_btn", Button).label = l["ClearLogs"]
        self.query_one("#settings_collapsible", Collapsible).title = l["SettingsTitle"]
        self.query_one("#logs_collapsible", Collapsible).title = l["LogsTitle"]


if __name__ == "__main__":
    app = StarterForTrusttunnel()
    app.run()
