import os
import subprocess
import sys
from pathlib import Path

from get_localizations import out_en, out_ru

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Header, Footer, Static, Button, Link, Collapsible, Input
from pyfiglet import figlet_format

l_en = out_en()
l_ru = out_ru()
l_ = None


class StarterForTrusttunnel(App):
    CSS_PATH = "style.tcss"
    BINDINGS = [("c", "choise_lang", "Choise language")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Container(
                Static(figlet_format(text=l_en["MainTitle"], font="rectangles"), classes="main_title"),
                Horizontal(
                    Button(l_en["ButtonForStart"], id="start_btn", classes="button"),
                    Button(l_en["ButtonForOpenFolder"], id="open_folder_btn", classes="button"),
                    classes="buttons",
                ),
                classes="block",
            ),
            Container(
                Collapsible(
                    Horizontal(
                        Input(placeholder=l_en["PathToFolder"], id="path_to_folder", classes="input"),
                        Input(placeholder=l_en["ConfigName"], id="config_name", classes="input"),
                        classes="inputs"
                    ),
                    Container(
                        Button(l_en["Confirm"], id="confirm_settings", classes="button btn_confirm"),
                        classes="block_for_button_confirm"
                    ),
                    collapsed=True,
                    title=l_en["SettingsTitle"],
                    classes="collapsible"
                ),
                Horizontal(
                    Link("GitHub", url="https://github.com/st1llb0rnn/StarterForTrusttunnel"),
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
        self.notify(l_en["StartTunnel"])
        self.notify(l_en["Connected"])

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
            self.notify(f"Не удалось открыть папку: {e}", severity="error")

    def confirm_settings(self) -> None:
        pass

    def action_choise_lang(self) -> None:
       self.notify("action_choise_lang")


if __name__ == "__main__":
    app = StarterForTrusttunnel()
    app.run()
