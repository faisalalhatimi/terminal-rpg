from . import incident, onboarding

QUESTS = [onboarding.QUEST, incident.QUEST]

BY_ID = {q["id"]: q for q in QUESTS}


def get(quest_id: str) -> dict:
    return BY_ID[quest_id]


def is_locked(quest: dict, closed: set[str]) -> bool:
    if not quest.get("available", True):
        return True
    required = quest.get("requires")
    return bool(required) and required not in closed
