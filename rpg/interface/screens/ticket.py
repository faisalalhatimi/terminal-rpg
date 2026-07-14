from rich.text import Text
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Footer, Static

from ... import content


class TicketScreen(Screen):
    BINDINGS = [
        Binding("enter", "accept", "Continue"),
        Binding("escape", "back", "Back"),
    ]

    def __init__(self, quest_id: str, modal: bool = False) -> None:
        super().__init__()
        self.quest_id = quest_id
        self.quest = content.get(quest_id)
        self.modal = modal

    def compose(self) -> ComposeResult:
        with Vertical(id="page"):
            with Vertical(id="mailbox"):
                yield Static(self.headers(), id="mailheaders")
                yield Static("─" * 74, id="mailrule")
                with VerticalScroll(id="mailscroll"):
                    yield Static(self.quest["ticket_body"], id="mailbody")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#mailscroll", VerticalScroll).focus()

    def headers(self) -> Text:
        block = Text()
        for label, value in self.quest["ticket_headers"]:
            block.append(f"{label + ':':<10}", style="#767676")
            style = "bold #f14c4c" if label == "Priority" else "#cccccc"
            block.append(f"{value}\n", style=style)
        return block

    def action_accept(self) -> None:
        from .play import PlayScreen

        if self.modal:
            self.app.pop_screen()
        else:
            session = self.app.start_quest(self.quest_id)
            self.app.switch_screen(PlayScreen(session))

    def action_back(self) -> None:
        self.app.pop_screen()
