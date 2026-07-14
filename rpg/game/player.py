from dataclasses import dataclass, field


@dataclass
class Player:
    rank: str
    xp: int = 0
    closed: set[str] = field(default_factory=set)
    secrets_read: set[str] = field(default_factory=set)
    notes: str = ""

    def has_closed(self, quest_id: str) -> bool:
        return quest_id in self.closed

    def close_case(self, quest_id: str, xp: int, promotion: str) -> bool:
        if self.has_closed(quest_id):
            self.closed.add(quest_id)
            return False

        self.closed.add(quest_id)
        self.xp += xp
        promoted = self.rank != promotion
        self.rank = promotion
        return promoted

    @property
    def cases_closed(self) -> int:
        return len(self.closed)

    def can_read(self, note: dict) -> bool:
        return self.xp >= note["unlock_xp"]

    def has_read(self, note_id: str) -> bool:
        return note_id in self.secrets_read

    def mark_read(self, note_id: str) -> None:
        self.secrets_read.add(note_id)
