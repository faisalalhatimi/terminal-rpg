from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Footer, Static

from ...content import shared


class RulebookScreen(Screen):
    BINDINGS = [Binding("escape,f3,enter", "back", "Close")]

    def compose(self) -> ComposeResult:
        with Vertical(id="page"):
            with Vertical(id="book"):
                yield Static("H A T I   S O C   R U L E B O O K", id="bookhead")
                yield Static(shared.RULEBOOK_NOTE, id="booknote")
                with VerticalScroll():
                    yield Static(shared.RULEBOOK, id="bookbody")
        yield Footer()

    def action_back(self) -> None:
        self.app.pop_screen()
