from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Footer, Static

from ...content import shared


class PrimerScreen(Screen):
    BINDINGS = [Binding("enter", "go", "Case load")]

    def compose(self) -> ComposeResult:
        with Vertical(id="page"):
            with VerticalScroll(id="primer"):
                yield Static(shared.PRIMER, id="primertext")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#primer", VerticalScroll).focus()

    def action_go(self) -> None:
        from .hub import HubScreen

        self.app.switch_screen(HubScreen())
