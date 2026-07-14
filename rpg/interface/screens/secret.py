from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Footer, Input, Static

from ...content import shared


class SecretNoteScreen(Screen):
    BINDINGS = [Binding("escape", "back", "Back")]

    def __init__(self, note_id: str) -> None:
        super().__init__()
        self.note = next(n for n in shared.SECRET_NOTES if n["id"] == note_id)
        self.attempts = 0

    @property
    def already_read(self) -> bool:
        return self.app.player.has_read(self.note["id"])

    def compose(self) -> ComposeResult:
        read = self.already_read
        with Vertical(id="page"):
            with Vertical(id="secret"):
                yield Static(self.note["name"].upper(), id="secrethead")
                with VerticalScroll(id="secretscroll"):
                    yield Static(
                        self.note["story"] if read else shared.SECRET_PROMPT,
                        id="secrettext",
                    )
                if not read:
                    yield Input(placeholder="string", id="secretinput")
                    yield Static("", id="secreterror")
        yield Footer()

    def on_mount(self) -> None:
        if self.already_read:
            self.query_one("#secretscroll", VerticalScroll).focus()
        else:
            self.query_one("#secretinput", Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        entered = event.value.strip().upper()
        event.input.value = ""
        if not entered:
            return
        self.attempts += 1
        if entered != self.note["ciphertext"].upper():
            self.query_one("#secreterror", Static).update(shared.SECRET_WRONG)
            return

        self.app.player.mark_read(self.note["id"])
        self.app.analytics.secret(self.note["id"], self.attempts)
        self.query_one("#secrettext", Static).update(self.note["story"])
        self.query_one("#secretinput", Input).remove()
        self.query_one("#secreterror", Static).remove()
        self.query_one("#secretscroll", VerticalScroll).focus()

    def action_back(self) -> None:
        self.app.pop_screen()
