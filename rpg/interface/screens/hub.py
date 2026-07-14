from rich.text import Text
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Footer, OptionList, Static
from textual.widgets.option_list import Option

from ... import content
from ...content import shared


class HubScreen(Screen):
    BINDINGS = [Binding("escape", "back", "Back")]

    def compose(self) -> ComposeResult:
        yield Static(" CASE LOAD", id="header")
        with Horizontal(id="hubbody"):
            with Vertical(id="hubside"):
                yield Static(self.record(), id="record")
            with Vertical(id="hubmain"):
                yield OptionList(*self.entries(), id="questlist")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#questlist", OptionList).focus()

    def entries(self) -> list:
        items: list = []
        for quest in content.QUESTS:
            locked = content.is_locked(quest, self.app.player.closed)
            closed = self.app.player.has_closed(quest["id"])
            label = Text()

            if locked:
                label.append(f"{quest['title']}\n", style="#4a4a52")
                label.append(f"  {quest['summary']}", style="#4a4a52")
            elif closed:
                label.append("[x] ", style="#23d18b")
                label.append(f"{quest['title']}\n", style="#23d18b")
                label.append("  Closed. You can work it again, no xp.", style="#767676")
            else:
                label.append(f"{quest['title']}\n", style="bold #cccccc")
                label.append(f"  {quest['summary']}", style="#767676")

            items.append(Option(label, id=quest["id"], disabled=locked))

        items.append(self.rule())

        for note in shared.SECRET_NOTES:
            unlocked = self.app.player.can_read(note)
            read = self.app.player.has_read(note["id"])
            entry = Text()
            entry.append(
                f"{note['name']}\n",
                style="bold #f5f543" if unlocked else "#4a4a52",
            )
            if read:
                entry.append("  Read.", style="#767676")
            elif unlocked:
                entry.append(f"  {shared.SECRET_READY}", style="#23d18b")
            else:
                need = note["unlock_xp"] - self.app.player.xp
                entry.append(f"  {shared.SECRET_LOCKED} ({need} xp)", style="#4a4a52")
            items.append(Option(entry, id=note["id"], disabled=not unlocked))

        items.append(self.rule())

        notes = Text()
        notes.append("Your notes\n", style="bold #cccccc")
        chars = len(self.app.player.notes.strip())
        notes.append(f"  {chars} characters" if chars else "  empty", style="#767676")
        items.append(Option(notes, id="notes"))

        return items

    @staticmethod
    def rule() -> Option:
        return Option(Text("─" * 46, style="#2a2a30"), disabled=True)

    def record(self) -> Text:
        player = self.app.player
        block = Text()
        block.append("ANALYST\n\n", style="bold #23d18b")
        for key, value in (
            ("rank", player.rank),
            ("xp", player.xp),
            ("closed", player.cases_closed),
        ):
            block.append(f"{key:<9}", style="#767676")
            block.append(f"{value}\n", style="#cccccc")
        return block

    def refresh_entries(self) -> None:
        listing = self.query_one("#questlist", OptionList)
        listing.clear_options()
        listing.add_options(self.entries())
        self.query_one("#record", Static).update(self.record())

    def on_screen_resume(self) -> None:
        self.refresh_entries()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        from .notes import NotesScreen
        from .secret import SecretNoteScreen
        from .ticket import TicketScreen

        chosen = event.option.id
        if chosen == "notes":
            self.app.push_screen(NotesScreen(self.app.player.notes), self.on_notes_closed)
        elif any(n["id"] == chosen for n in shared.SECRET_NOTES):
            self.app.push_screen(SecretNoteScreen(chosen))
        else:
            self.app.push_screen(TicketScreen(chosen))

    def on_notes_closed(self, text: str) -> None:
        self.app.player.notes = text
        self.refresh_entries()

    def action_back(self) -> None:
        self.app.pop_screen()
