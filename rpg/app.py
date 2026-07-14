from textual.app import App
from textual.binding import Binding

from . import content
from .content import shared
from .game.player import Player
from .game.session import QuestSession
from .interface.screens.title import TitleScreen
from .sandbox.base import Runner
from .sandbox.docker import DockerRunner, docker_ready, sweep_orphans


class TerminalRPG(App):
    CSS_PATH = "interface/app.tcss"
    TITLE = "TerminalRPG"
    ENABLE_COMMAND_PALETTE = False
    BINDINGS = [Binding("ctrl+q", "quit", "Quit")]

    def __init__(self) -> None:
        super().__init__()
        self.player = Player(rank=shared.STARTING_RANK)

    def on_mount(self) -> None:
        self.dark = True
        self.push_screen(TitleScreen())

    def make_runner(self, quest: dict) -> Runner:
        return DockerRunner(quest["id"], quest["host"])

    def start_quest(self, quest_id: str) -> QuestSession:
        quest = content.get(quest_id)
        return QuestSession(
            quest, self.player, self.make_runner(quest)
        )


def prestart_check() -> bool:
    ok, message = docker_ready()
    if not ok:
        print("TerminalRPG cannot start.\n")
        print(message)
        return False
    removed = sweep_orphans()
    if removed:
        print(f"cleared {removed} leftover containers from a previous run")
    return True


def main() -> None:
    if not prestart_check():
        raise SystemExit(1)
    TerminalRPG().run()


if __name__ == "__main__":
    main()