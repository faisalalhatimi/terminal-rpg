from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Footer, OptionList, Static
from textual.widgets.option_list import Option


class ConfirmScreen(ModalScreen[bool]):
    BINDINGS = [Binding("escape", "cancel", "Cancel")]

    def __init__(self, question: str, warning: str) -> None:
        super().__init__()
        self.question = question
        self.warning = warning

    def compose(self) -> ComposeResult:
        with Vertical(id="confirm"):
            yield Static(self.question, id="confirmq")
            yield Static(self.warning, id="confirmwarn")
            yield OptionList(
                Option("Keep working", id="no"),
                Option("Abandon the quest", id="yes"),
                id="confirmchoice",
            )
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#confirmchoice", OptionList).focus()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        self.dismiss(event.option.id == "yes")

    def action_cancel(self) -> None:
        self.dismiss(False)
