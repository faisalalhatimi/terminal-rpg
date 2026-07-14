QUEST = {
    "id": "incident-0101",
    "title": "INCIDENT-0101 : Unauthorised access on web-03",
    "host": "web-03",
    "user": "root",
    "summary": "6 objectives | est.25 min",
    "requires": "onboarding-01",
    "available": True,
    "xp_per_objective": 40,
    "hint_threshold": 6,
    "hint_offer": "soc-lead: stuck? F1 and I will help you.",
    "promotion": "Tier 2 Analyst",
    "welcome": "Connected to web-03 as root. F1 hint, F2 ticket, F3 rulebook, F4 notes.",
    "replay_notice": (
        "This case is already closed. Work it again if you like. "
        "There is no xp in a rerun."
    ),
    "ticket_headers": [
        ("From", "soc-lead@hati.internal"),
        ("To", "analyst@hati.internal"),
        ("Subject", "INCIDENT-0101 : Unauthorised access on web-03"),
        ("Date", "Today, 07:42"),
        ("Priority", "HIGH"),
    ],
    "ticket_body": """The IDS flagged an authenticated SSH session on web-03 at 02:14 this morning,
from 198.51.100.7. That address has no business reason to touch that box. The
session lasted eleven minutes. Nobody was on call.

web-03 is a public facing web server. It should have no interactive logins
outside a change window, and there was no change window last night.

What I need from you:
  1. Confirm how they got in and which account they used.
  2. Find out what they left behind.
  3. Shut it down and lock the account out.

You have a root shell on the host. That is not a privilege, it is a
responsibility. Everything you type happens.

Write what you find into your case file as you go. One fact per file, no
commentary:
  echo "<what you found>" > ~/case/<name of the task>.txt

The rulebook is on F3.

Enter takes you to the shell.""",
    "facts": [
        {"key": "logpath", "label": "log", "value": None},
        {"key": "account", "label": "account", "value": None},
        {"key": "source", "label": "source", "value": None},
        {"key": "process", "label": "process", "value": None},
    ],
    "objectives": [
        {
            "title": "Find the authentication log",
            "hint": "Every login on a Linux host is written down. The writing happens under /var/log.",
            "lead": "soc-lead: that is the one. Every login on this server is in there.",
            "state": "current",
            "attempts": 0,
            "evidence": {"key": "logpath", "label": "log", "value": "/var/log/auth.log"},
            "condition": {
                "type": "file_contains",
                "path": "/root/case/log.txt",
                "contains": "/var/log/auth.log",
            },
        },
        {
            "title": "Record the compromised account",
            "hint": (
                "The log line for an accepted session names the account it accepted. "
                "Search the log for the word accepted."
            ),
            "lead": (
                "soc-lead: svc-deploy? That is for deployment. It has no business holding "
                "an interactive session at two in the morning."
            ),
            "state": "locked",
            "attempts": 0,
            "evidence": {"key": "account", "label": "account", "value": "svc-deploy"},
            "condition": {
                "type": "file_contains",
                "path": "/root/case/account.txt",
                "contains": "svc-deploy",
            },
        },
        {
            "title": "Record where the session came from",
            "hint": "The same log file that names the account names the address it came from.",
            "lead": "soc-lead: not one of ours. I will get it blocked.",
            "state": "locked",
            "attempts": 0,
            "evidence": {"key": "source", "label": "source", "value": "198.51.100.7"},
            "condition": {
                "type": "file_contains",
                "path": "/root/case/source.txt",
                "contains": "198.51.100.7",
            },
        },
        {
            "title": "Record the process they left running",
            "hint": (
                "Something is running that should not be. List every process on the "
                "host and read the names carefully."
            ),
            "lead": (
                "soc-lead: kworkerd. Note the spelling. The real process is kworker. This is "
                "someone counting on you not looking twice."
            ),
            "state": "locked",
            "attempts": 0,
            "evidence": {"key": "process", "label": "process", "value": "kworkerd"},
            "condition": {
                "type": "file_contains",
                "path": "/root/case/process.txt",
                "contains": "kworkerd",
            },
        },
        {
            "title": "Stop the process",
            "hint": "A process is stopped by its number, not its name. The process list gives you the number.",
            "lead": "soc-lead: gone. Now revoke their access.",
            "state": "locked",
            "attempts": 0,
            "evidence": None,
            "condition": {"type": "process_absent", "name": "kworkerd"},
        },
        {
            "title": "Revoke the attacker's SSH key",
            "hint": (
                "A key that lets someone in is a line in a file. Look in the account's "
                ".ssh directory."
            ),
            "lead": "soc-lead: that is the door shut. Good work.",
            "state": "locked",
            "attempts": 0,
            "evidence": None,
            "condition": {
                "type": "file_absent",
                "path": "/home/svc-deploy/.ssh/authorized_keys",
            },
        },
    ],
}
