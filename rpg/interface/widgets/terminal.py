from rich.text import Text
from textual import on
from textual.containers import Horizontal, Vertical
from textual.message import Message
from textual.reactive import reactive
from textual.widgets import Input, RichLog, Static

EVENT_STYLES = {
    "reward": "bold green",
    "hint": "bold yellow",
    "story": "italic magenta",
    "error": "bold red",
    "system": "dim cyan",
}


class Terminal(Vertical):
    prompt = reactive("$ ", init=False)

    class CommandSubmitted(Message):
        def __init__(self, command: str) -> None:
            self.command = command
            super().__init__()

    def compose(self):
        yield RichLog(id="scrollback", wrap=True, markup=False, auto_scroll=True)
        with Horizontal(id="inputline"):
            yield Static(self.prompt, id="promptlabel")
            yield Input(id="cmdline")

    def on_mount(self) -> None:
        self.focus_input()

    def watch_prompt(self, value: str) -> None:
        label = self.query("#promptlabel")
        if label:
            label.first(Static).update(value)

    @on(Input.Submitted, "#cmdline")
    def _on_submit(self, event: Input.Submitted) -> None:
        command = event.value
        event.input.value = ""
        self.echo(command)
        if command.strip():
            self.post_message(self.CommandSubmitted(command))

    def echo(self, command: str) -> None:
        self._write(Text(f"{self.prompt}{command}", style="dim"))

    def write_output(self, text: str) -> None:
        if text:
            self._write(Text(text))

    def write_event(self, text: str, kind: str = "system") -> None:
        self._write(Text(text, style=EVENT_STYLES.get(kind, "bold")))

    def _write(self, renderable) -> None:
        self.query_one("#scrollback", RichLog).write(renderable)

    def set_busy(self, busy: bool) -> None:
        field = self.query_one("#cmdline", Input)
        field.disabled = busy
        if not busy:
            field.focus()

    def focus_input(self) -> None:
        self.query_one("#cmdline", Input).focus()
