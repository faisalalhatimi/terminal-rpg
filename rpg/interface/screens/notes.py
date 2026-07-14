from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Footer, Static, TextArea


class NotesScreen(ModalScreen[str]):
    BINDINGS = [Binding("escape", "close", "Save and close")]

    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = text

    def compose(self) -> ComposeResult:
        with Vertical(id="notes"):
            yield Static("NOTES", id="noteshead")
            yield Static(
                "Pssst...this is yours. Nobody reads this but you, use it to store ciphers. Escape saves and closes.",
                id="notesnote",
            )
            yield TextArea(self.text, id="notesarea")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#notesarea", TextArea).focus()

    def action_close(self) -> None:
        self.dismiss(self.query_one("#notesarea", TextArea).text)
