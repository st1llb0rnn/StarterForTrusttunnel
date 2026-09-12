from multiprocessing import Array
import os
import subprocess
import sys
from pathlib import Path

from get_localizations import out_en, out_ru, choise_language
from get_localizations import file_with_status as fws

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Header, Footer, Static, Button, Link, Collapsible, Input
from pyfiglet import figlet_format

# Variables for changing the language in the application
l_en = out_en() # English
l_ru = out_ru() # Russian
l_ = fws("get")["Status"]
cl = choise_language(l_)


class StarterForTrusttunnel(App):
    CSS_PATH = "style.tcss" # Styles for app
    BINDINGS = [("c", "choise_lang", "Choise language")] # Binds for app

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Текущий язык интерфейса (словарь строк) и его название ("english"/"russian")
        self.current_lang_name = l_
        self.current_lang = cl

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

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start_btn":
            self.start_tunnel()
        elif event.button.id == "open_folder_btn":
            self.open_tt_folder()

    def start_tunnel(self) -> None:
        # сюда логику запуска трастаннеля, например:
        # subprocess.Popen(["./trusttunnel"], cwd=self.tunnel_dir)
        self.notify(self.current_lang["StartTunnel"])
        self.notify(self.current_lang["Connected"])

    def open_tt_folder(self) -> None:
        folder = Path(__file__).parent  # поменяй на нужную папку с trusttunnel
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
        pass

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
        self.query_one("#start_btn", Button).label = l["ButtonForStart"]
        self.query_one("#open_folder_btn", Button).label = l["ButtonForOpenFolder"]
        self.query_one("#path_to_folder", Input).placeholder = l["PathToFolder"]
        self.query_one("#config_name", Input).placeholder = l["ConfigName"]
        self.query_one("#confirm_settings", Button).label = l["Confirm"]
        self.query_one(Collapsible).title = l["SettingsTitle"]


if __name__ == "__main__":
    app = StarterForTrusttunnel()
    app.run()
