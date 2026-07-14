from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.screen import Screen
from textual.widgets import Footer, OptionList, Static
from textual.widgets.option_list import Option

from ...content import shared


class TitleScreen(Screen):
    def compose(self) -> ComposeResult:
        with Vertical(id="page"):
            with Vertical(id="titleblock"):
                yield Static("TERMINAL RPG", id="titleword")
                yield Static(shared.TAGLINE, id="tagline")
                with Center():
                    yield OptionList(
                        Option("Start game", id="start"),
                        Option("Info", id="info"),
                        Option("Quit", id="quit"),
                        id="mainmenu",
                    )
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#mainmenu", OptionList).focus()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        from .info import InfoScreen
        from .primer import PrimerScreen

        if event.option.id == "start":
            self.app.push_screen(PrimerScreen())
        elif event.option.id == "info":
            self.app.push_screen(InfoScreen())
        elif event.option.id == "quit":
            self.app.exit()
