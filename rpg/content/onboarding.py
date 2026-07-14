QUEST = {
    "id": "onboarding-01",
    "title": "ONBOARDING : First day on the desk",
    "host": "training-01",
    "user": "root",
    "summary": "6 objectives | est.15 min",
    "requires": None,
    "available": True,
    "xp_per_objective": 20,
    "hint_threshold": 6,
    "hint_offer": "soc-lead: take a hint. Nobody is timing you and nobody is watching.",
    "promotion": "Tier 1 Analyst",
    "welcome": "Connected to training-01 as root. F1 hint, F2 ticket, F3 rulebook, F4 notes.",
    "replay_notice": (
        "You have done this one. Do it again if you like. There is no xp in a rerun."
    ),
    "ticket_headers": [
        ("From", "soc-lead@hati.internal"),
        ("To", "analyst@hati.internal"),
        ("Subject", "First day. Read this before you touch anything."),
        ("Date", "Today, 08:55"),
        ("Priority", "NORMAL"),
    ],
    "ticket_body": """Welcome to the desk.

Before you go near any live host I want you to train here for an hour. It is a
box we keep for exactly this. Nothing on it matters and you can break it.

You have six objectives. They are not difficult and they are not a test. They are the six
things you will do a hundred times a week for the rest of your career, and I
would rather you fumble them here than on a production machine.

Write your answers into your case file as you go. It is a directory, ~/case, and
it is how anything gets recorded on this team:
  echo "<what you found>" > ~/case/<name of the task>.txt

The rulebook is on F3. It is not cheating to read it. Nobody memorises this and
the people who pretend they did are lying.

Enter takes you to the shell.""",
    "facts": [
        {"key": "desk", "label": "desk", "value": None},
        {"key": "handover", "label": "handover", "value": None},
        {"key": "alerts", "label": "alerts", "value": None},
    ],
    "objectives": [
        {
            "title": "Find the training directory",
            "hint": "pwd tells you where you are. ls tells you what is here. cd moves you.",
            "lead": "soc-lead: this is it. Half this job is knowing where you are standing.",
            "state": "current",
            "attempts": 0,
            "evidence": None,
            "condition": {"type": "path_reached", "path": "/root/training"},
        },
        {
            "title": "Read your orientation and record your desk number",
            "hint": (
                "cat prints a file. The desk number is in orientation.txt. "
                "Write it down with: echo \"<number>\" > ~/case/desk.txt"
            ),
            "lead": "soc-lead: D-14. The one under the broken AC. Sorry.",
            "state": "locked",
            "attempts": 0,
            "evidence": {"key": "desk", "label": "desk", "value": "D-14"},
            "condition": {
                "type": "file_contains",
                "path": "/root/case/desk.txt",
                "contains": "D-14",
            },
        },
        {
            "title": "Search the shift log for who handed over to you",
            "hint": (
                "shift.log is long and you do not want to read all of it. "
                "grep prints only the lines that match: grep handover shift.log"
            ),
            "lead": "soc-lead: Zelda. She works at night and she is better than me. Ask her when you meet her.",
            "state": "locked",
            "attempts": 0,
            "evidence": {"key": "handover", "label": "handover", "value": "zelda"},
            "condition": {
                "type": "file_contains",
                "path": "/root/case/handover.txt",
                "contains": "zelda",
            },
        },
        {
            "title": "Count how many alerts were there",
            "hint": (
                "Two commands, joined. grep finds the lines, wc -l counts them: "
                "grep alert shift.log | wc -l"
            ),
            "lead": (
                "soc-lead: 47. On a quiet night. Now you understand why we do not read "
                "every one by hand."
            ),
            "state": "locked",
            "attempts": 0,
            "evidence": {"key": "alerts", "label": "alerts", "value": "47"},
            "condition": {
                "type": "file_contains",
                "path": "/root/case/alerts.txt",
                "contains": "47",
            },
        },
        {
            "title": "Lock your case file so nobody else can read it",
            "hint": (
                "Permissions are three digits: owner, group, everyone. "
                "chmod 700 ~/case gives everything to you and nothing to anyone else."
            ),
            "lead": (
                "soc-lead: good. Half the breaches I have worked started with a file "
                "somebody left readable."
            ),
            "state": "locked",
            "attempts": 0,
            "evidence": None,
            "condition": {
                "type": "permission_equals",
                "path": "/root/case",
                "mode": "700",
            },
        },
        {
            "title": "Delete the scratch file the last trainee left behind",
            "hint": "rm deletes a file. It is called scratch.tmp and it is in your home directory.",
            "lead": (
                "soc-lead: thank you. That thing has been there since May.\n"
                "soc-lead: that is everything. Go and get a coffee, the shift is long."
            ),
            "state": "locked",
            "attempts": 0,
            "evidence": None,
            "condition": {
                "type": "file_absent",
                "path": "/root/scratch.tmp",
            },
        },
    ],
}
