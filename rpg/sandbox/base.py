from dataclasses import dataclass

BLOCKED_PROGRAMS = frozenset(
    {
        "vi",
        "vim",
        "nvim",
        "nano",
        "pico",
        "emacs",
        "less",
        "more",
        "man",
        "top",
        "htop",
        "watch",
        "tmux",
        "screen",
    }
)

TIMEOUT_SECONDS = 15


@dataclass(slots=True)
class CommandResult:
    output: str
    exit_code: int
    cwd: str
    blocked: bool = False
    timed_out: bool = False


class Runner:
    async def start(self) -> str:
        raise NotImplementedError

    async def run(self, command: str) -> CommandResult:
        raise NotImplementedError

    async def stop(self) -> None:
        raise NotImplementedError

    async def inspect(self, argv: list[str]) -> tuple[int, str]:
        raise NotImplementedError

    @staticmethod
    def blocked_program(command: str) -> str | None:
        tokens = command.strip().split()
        if not tokens:
            return None
        name = tokens[0].rsplit("/", 1)[-1]
        return name if name in BLOCKED_PROGRAMS else None
