import copy
import time
from dataclasses import dataclass, field

from ..sandbox.base import Runner
from . import conditions
from .player import Player

DONE = "done"
CURRENT = "current"
LOCKED = "locked"


@dataclass
class Latch:
    title: str
    lead: str
    evidence: dict | None
    xp: int
    final: bool


@dataclass
class Turn:
    output: str = ""
    cwd: str = ""
    exit_code: int = 0
    blocked: bool = False
    hint_offer: str | None = None
    latches: list[Latch] = field(default_factory=list)


class QuestSession:
    def __init__(self, quest, player, runner, analytics=None):
        self.quest = quest
        self.player = player
        self.runner = runner

        self.objectives = copy.deepcopy(quest["objectives"])
        self.facts = copy.deepcopy(quest["facts"])

        self.current = 0
        self.hints_used = 0
        self.xp_earned = 0
        self.started_at = time.monotonic()

        self.replay = player.has_closed(quest["id"])

        self.analytics = analytics
        self.attempt_id = None
        self.command_seq = 0
        if analytics is not None:
            self.attempt_id = analytics.start_attempt(quest["id"], self.replay)

    @property
    def objective(self) -> dict | None:
        if self.current >= len(self.objectives):
            return None
        return self.objectives[self.current]

    @property
    def complete(self) -> bool:
        return self.current >= len(self.objectives)

    @property
    def elapsed(self) -> int:
        return int(time.monotonic() - self.started_at)

    @property
    def attempts_total(self) -> int:
        return sum(o["attempts"] for o in self.objectives)

    @property
    def objectives_done(self) -> int:
        return sum(1 for o in self.objectives if o["state"] == DONE)

    async def start(self) -> str:
        return await self.runner.start()

    async def stop(self) -> None:
        await self.runner.stop()

    async def submit(self, command: str) -> Turn:
        result = await self.runner.run(command)

        turn = Turn(
            output=result.output,
            cwd=result.cwd,
            exit_code=result.exit_code,
            blocked=result.blocked,
        )

        self.command_seq += 1
        if self.analytics is not None:
            self.analytics.command(
                self.attempt_id, self.command_seq, command,
                result.exit_code, result.cwd, result.blocked,
            )

        if self.complete:
            return turn

        turn.hint_offer = self.record_attempt()

        while not self.complete and await conditions.satisfied(
            self.runner, self.objective["condition"], turn.cwd
        ):
            index = self.current
            attempts_here = self.objectives[index]["attempts"]
            turn.latches.append(self.latch())
            if self.analytics is not None:
                self.analytics.objective(self.attempt_id, index, attempts_here)

        return turn

    def record_attempt(self) -> str | None:
        objective = self.objective
        objective["attempts"] += 1

        if objective["attempts"] == self.quest["hint_threshold"] and not objective.get(
            "offered"
        ):
            objective["offered"] = True
            if self.analytics is not None:
                self.analytics.hint(self.attempt_id, self.current, requested=False)
            return self.quest["hint_offer"]
        return None

    def take_hint(self) -> str:
        self.hints_used += 1
        if self.analytics is not None and self.objective is not None:
            self.analytics.hint(self.attempt_id, self.current, requested=True)
        return self.objective["hint"] if self.objective else ""

    def latch(self) -> Latch:
        objective = self.objective
        objective["state"] = DONE

        evidence = objective.get("evidence")
        if evidence:
            for fact in self.facts:
                if fact["key"] == evidence["key"]:
                    fact["value"] = evidence["value"]

        xp = 0 if self.replay else self.quest["xp_per_objective"]
        self.xp_earned += xp

        self.current += 1
        if not self.complete:
            self.objectives[self.current]["state"] = CURRENT

        return Latch(
            title=objective["title"],
            lead=objective["lead"],
            evidence=evidence,
            xp=xp,
            final=self.complete,
        )

    def close(self) -> bool:
        if self.analytics is not None:
            self.analytics.end_attempt(self.attempt_id, "completed", self.xp_earned)
        return self.player.close_case(
            self.quest["id"], self.xp_earned, self.quest["promotion"]
        )

    def abandon(self) -> None:
        if self.analytics is not None:
            self.analytics.end_attempt(self.attempt_id, "abandoned", self.xp_earned)
