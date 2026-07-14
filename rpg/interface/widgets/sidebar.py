from rich.text import Text
from textual.widgets import Static

DONE = "done"
CURRENT = "current"
LOCKED = "locked"

MARKS = {DONE: "[x]", CURRENT: "[>]", LOCKED: "[ ]"}
STYLES = {DONE: "#23d18b", CURRENT: "bold #cccccc", LOCKED: "#4a4a52"}


class QuestLog(Static):
    def __init__(self, objectives: list[dict]) -> None:
        super().__init__()
        self.objectives = objectives
        self.border_title = "quest log"

    def on_mount(self) -> None:
        self.redraw()

    def redraw(self) -> None:
        body = Text()
        for objective in self.objectives:
            state = objective["state"]
            body.append(f"{MARKS[state]} ", style=STYLES[state])
            body.append(f"{objective['title']}\n", style=STYLES[state])
        self.update(body)

    def bump(self, index: int) -> None:
        self.objectives[index]["attempts"] += 1

    def complete(self, index: int) -> None:
        self.objectives[index]["state"] = DONE
        for objective in self.objectives:
            if objective["state"] == LOCKED:
                objective["state"] = CURRENT
                break
        self.redraw()


class CaseFile(Static):
    def __init__(self, facts: list[dict]) -> None:
        super().__init__()
        self.facts = facts
        self.border_title = "case file"

    def on_mount(self) -> None:
        self.redraw()

    def redraw(self) -> None:
        body = Text()
        for fact in self.facts:
            body.append(f"{fact['label']:<9}", style="#767676")
            if fact["value"] is None:
                body.append("empty\n", style="#4a4a52")
            else:
                body.append(f"{fact['value']}\n", style="#cccccc")
        self.update(body)

    def confirm(self, key: str, value: str) -> None:
        for fact in self.facts:
            if fact["key"] == key:
                fact["value"] = value
        self.redraw()

    def report(self) -> Text:
        body = Text()
        for fact in self.facts:
            body.append(f"  {fact['label']:<9}", style="#767676")
            body.append(f"{fact['value'] or 'not established'}\n", style="#cccccc")
        return body


class AnalystPanel(Static):
    def __init__(self, xp: int = 0) -> None:
        super().__init__()
        self.xp = xp
        self.hints_used = 0
        self.border_title = "analyst"

    def on_mount(self) -> None:
        self.redraw()

    def redraw(self) -> None:
        body = Text()
        body.append(f"{'xp':<9}", style="#767676")
        body.append(f"{self.xp}\n", style="#cccccc")
        body.append(f"{'hints':<9}", style="#767676")
        body.append(f"{self.hints_used} used\n", style="#cccccc")
        self.update(body)

    def award(self, amount: int) -> None:
        self.xp += amount
        self.redraw()

    def record_hint(self) -> None:
        self.hints_used += 1
        self.redraw()


class TimerPanel(Static):
    def __init__(self) -> None:
        super().__init__()
        self.border_title = "time"

    def show(self, seconds: int) -> None:
        self.update(Text(f"{seconds // 60:02d}:{seconds % 60:02d}", style="#cccccc"))
