from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Footer, Static

from ...content import shared


class InfoScreen(Screen):
    BINDINGS = [Binding("escape,enter", "back", "Back")]

    def compose(self) -> ComposeResult:
        with Vertical(id="page"):
            yield Static(shared.INFO, id="info")
        yield Footer()

    def action_back(self) -> None:
        self.app.pop_screen()
