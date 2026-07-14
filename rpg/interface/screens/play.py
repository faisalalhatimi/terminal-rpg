from rich.text import Text
from textual import on, work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Footer, Static

from ...game.session import QuestSession, Turn
from ..widgets.sidebar import AnalystPanel, CaseFile, QuestLog, TimerPanel
from ..widgets.terminal import Terminal


class PlayScreen(Screen):
    BINDINGS = [
        Binding("f1", "hint", "Hint"),
        Binding("f2", "ticket", "Ticket"),
        Binding("f3", "rulebook", "Rulebook"),
        Binding("f4", "notes", "Notes"),
        Binding("f10", "abandon", "Abandon Quest"),
    ]

    def __init__(self, session: QuestSession) -> None:
        super().__init__()
        self.session = session

    def compose(self) -> ComposeResult:
        yield Static(f" {self.session.quest['title']}", id="header")
        with Horizontal(id="body"):
            with Vertical(id="sidebar"):
                yield QuestLog(self.session.objectives)
                yield CaseFile(self.session.facts)
                yield AnalystPanel(self.session.player.xp)
                yield TimerPanel()
            yield Terminal(id="terminal")
        yield Footer()

    async def on_mount(self) -> None:
        self.set_interval(1.0, self.tick)
        self.tick()
        terminal = self.query_one(Terminal)
        terminal.set_busy(True)
        terminal.write_event("Building the host. This takes a moment.", "system")
        try:
            cwd = await self.session.start()
        except Exception as error:
            terminal.write_event(str(error), "error")
            terminal.write_event("Press F10 to go back.", "error")
            return
        terminal.prompt = self.prompt(cwd)
        terminal.write_event(self.session.quest["welcome"], "system")
        if self.session.replay:
            terminal.write_event(self.session.quest["replay_notice"], "system")
        terminal.set_busy(False)

    def tick(self) -> None:
        self.query_one(TimerPanel).show(self.session.elapsed)

    def prompt(self, cwd: str) -> str:
        user = self.session.quest.get("user", "analyst")
        mark = "#" if user == "root" else "$"
        return f"{user}@{self.session.quest['host']}:{cwd}{mark} "

    @on(Terminal.CommandSubmitted)
    def _dispatch(self, message: Terminal.CommandSubmitted) -> None:
        self.execute(message.command)

    @work(exclusive=True)
    async def execute(self, command: str) -> None:
        terminal = self.query_one(Terminal)
        terminal.set_busy(True)

        try:
            turn = await self.session.submit(command)
        except Exception as error:
            terminal.write_event(str(error), "error")
            terminal.write_event("The host is gone. Press F10 to leave the case.", "error")
            terminal.set_busy(False)
            return
        self.render_turn(turn)

        terminal.prompt = self.prompt(turn.cwd)
        terminal.set_busy(False)

    def render_turn(self, turn: Turn) -> None:
        terminal = self.query_one(Terminal)

        if turn.blocked:
            terminal.write_event(turn.output, "error")
        else:
            terminal.write_output(turn.output)

        if turn.hint_offer:
            terminal.write_event(turn.hint_offer, "story")

        for latch in turn.latches:
            self.draw_latch(latch)

    def draw_latch(self, latch) -> None:
        terminal = self.query_one(Terminal)

        if latch.evidence:
            self.query_one(CaseFile).confirm(
                latch.evidence["key"], latch.evidence["value"]
            )
        self.query_one(QuestLog).redraw()

        terminal.write_event(f"objective complete . {latch.title}", "reward")
        terminal.write_event(latch.lead, "story")
        if latch.xp:
            self.query_one(AnalystPanel).award(latch.xp)
            terminal.write_event(f"+{latch.xp} xp", "reward")

        terminal.focus_input()

        if latch.final:
            promoted = self.session.close()
            self.teardown()
            self.app.push_screen(DebriefScreen(self.session, promoted))

    def action_hint(self) -> None:
        hint = self.session.take_hint()
        self.query_one(AnalystPanel).record_hint()
        terminal = self.query_one(Terminal)
        terminal.write_event(f"hint: {hint}", "hint")
        terminal.focus_input()

    def action_ticket(self) -> None:
        from .ticket import TicketScreen

        self.app.push_screen(TicketScreen(self.session.quest["id"], modal=True))

    def action_rulebook(self) -> None:
        from .rulebook import RulebookScreen

        self.app.push_screen(RulebookScreen())

    def action_notes(self) -> None:
        from .notes import NotesScreen

        self.app.push_screen(
            NotesScreen(self.session.player.notes), self.on_notes_closed
        )

    def on_notes_closed(self, text: str) -> None:
        self.session.player.notes = text
        self.query_one(Terminal).focus_input()

    def action_abandon(self) -> None:
        from .confirm import ConfirmScreen

        self.app.push_screen(
            ConfirmScreen(
                f"Abandon {self.session.quest['id'].upper()}?",
                "Objectives, case file and quest XP are lost. The host is rebuilt "
                "from scratch. Your notes are yours and you keep them.",
            ),
            self.on_abandon_answer,
        )

    def on_abandon_answer(self, abandon: bool) -> None:
        if not abandon:
            self.query_one(Terminal).focus_input()
            return
        self.session.abandon()
        self.teardown()
        self.app.pop_screen()

    @work(exclusive=False)
    async def teardown(self) -> None:
        await self.session.stop()

class DebriefScreen(Screen):
    BINDINGS = [Binding("enter", "back_to_hub", "Back to case load")]

    def __init__(self, session: QuestSession, promoted: bool) -> None:
        super().__init__()
        self.session = session
        self.promoted = promoted

    def compose(self) -> ComposeResult:
        s = self.session

        body = Text()
        body.append("CASE CLOSED\n\n", style="bold #23d18b")
        body.append(f"{s.quest['id'].upper()} . {s.quest['host']}\n\n", style="#767676")

        body.append("FILED\n", style="bold #cccccc")
        for fact in s.facts:
            body.append(f"  {fact['label']:<10}", style="#767676")
            body.append(f"{fact['value'] or 'not established'}\n", style="#cccccc")

        body.append("\nRECORD\n", style="bold #cccccc")
        for label, value in (
            ("time", f"{s.elapsed // 60:02d}:{s.elapsed % 60:02d}"),
            ("objectives", f"{s.objectives_done} of {len(s.objectives)}"),
            ("commands", str(s.attempts_total)),
            ("hints", str(s.hints_used)),
            ("xp", "none, rerun" if s.replay else f"+{s.xp_earned}"),
        ):
            body.append(f"  {label:<10}", style="#767676")
            body.append(f"{value}\n", style="#cccccc")

        if self.promoted:
            body.append(
                "\nsoc-lead: host is clean and the write up stands on its own.\n",
                style="italic #d670d6",
            )
            body.append("You are ", style="#cccccc")
            body.append(f"{s.player.rank}", style="bold #f5f543")
            body.append(".\n", style="#cccccc")

        body.append("\nenter to return to the case load.", style="#767676")

        with Vertical(id="page"):
            yield Static(body, id="debrief")
        yield Footer()

    def action_back_to_hub(self) -> None:
        self.app.pop_screen()
        self.app.pop_screen()
