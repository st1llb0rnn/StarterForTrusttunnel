from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Button, Link

class StarterForTrusttunnel (App):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

        self.main_title = Static("Trusttunnel")
        self.start_button = Button("Start")
        self.open_tt_folder = Button("Open Folder")
        self.link_for_gitea = Link(text="Gitea", url="https://gitea.st1llb0rn.ru.net/st1llb0rn/StarterForTrusttunnel")
        self.link_for_github = Link(text="GitHub", url="https://github.com/st1llb0rnn/StarterForTrusttunnel")

        yield self.main_title
        yield self.start_button
        yield self.open_tt_folder

    # def on_mount(self) -> None:


if __name__ == "__main__":
    app = StarterForTrusttunnel()
    app.run()
