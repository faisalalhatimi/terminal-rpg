TAGLINE = "Invistigate security incidents using a real shell."


PRIMER = """BEFORE YOU START

You are a junior analyst in a security operations centre. 
Your boss hands you a host and a problem, and you work out what happened.
 It is a detective game with a Linux shell.

THE SHELL IS REAL

Commands run against a real Linux system. Nothing is simulated and no output is invented.
If a command works on Linux, it works here.

YOU WRITE YOUR OWN ANSWERS DOWN

Objectives in this games often do not tick themselves when you read the right file. 
Finding a thing is not the same as recording it.
When you learn something, write it into your case file:

  echo "svc-deploy" > ~/case/account.txt

This is the objective. The game reads what is on the host,
not what you typed to get there, so any route to get the answer is valid.

THERE IS A STORY YOU ARE NOT BEING TOLD

Somewhere on these hosts are secret files nobody has asked you to open.
Some of them hold a cipher, a short string that means nothing on its own.
No objective sends you to them and no XP is paid for finding them.

Copy anything strange into your notes on F4. Your notes come
out of the quest with you. Back at the desk, once you have the rank for it, you can read what the
ciphers say, and you will find out what actually happened here.

Nobody will mention it. Look anyway.

enter to go to your desk."""

INFO = """ABOUT
TBR"""

RULEBOOK_NOTE = (
    "The shell accepts any command Linux accepts. This is a reference, not a "
    "list of what is allowed. If you know a better way, use it."
)

RULEBOOK = """READING FILES AND LOGS

  cat <file>                  print a whole file
  grep <text> <file>          print only the lines containing text
  grep -i <text> <file>       the same, ignoring case
  grep -r <text> <dir>        search every file under a directory

MOVING AROUND

  pwd                         current directory
  ls -la                      list everything with hidden files 
  cd <dir>                    change directory
  cd ..                       go up one level
  find <dir> -name <name>     search a directory tree for a name

PROCESSES

  ps aux                      every process on the host
  ps aux | grep <text>        only the ones matching text
  kill <pid>                  ask a process to stop
  kill -9 <pid>               stop it without asking

FILES AND PERMISSIONS

  stat <file>                 size, owner, permissions, timestamps
  ls -l <file>                owner and permissions, briefly
  chmod <mode> <file>         change permissions, e.g. chmod 600
  rm <file>                   delete a file

CHAINING AND WRITING

  <command> | grep <text>     feed one command's output to another
  <command> > <file>          write output to a file, replacing it
  <command> >> <file>         add to the end of a file
  echo "<text>" > <file>      write a line you typed yourself

WRITING UP THE CASE

  Your case file is a directory: ~/case
  One fact per file. The name of the file is the quest case file
  which you find on the left below objectives.

    For example: case file is account and the answer is svc-web.
    echo "svc-web" > ~/case/account.txt

  How you get the text in there is up to you. Type it, pipe it,
  cut it out of a log. The case file cares what it says, not how
  it got there.

NOT AVAILABLE 

  Interactive tools need a full screen terminal, which this
  session does not provide. vim, nano, less, more, man, top
  and watch will not run. 
  Everything else will."""

SECRET_NOTES = [
    {
        "id": "note1",
        "name": "Secret note 1",
        "unlock_xp": 40,
        "seeded_at": "/root/training/.evidence",
        "ciphertext": "n7pi-NUFH-DS1",
        "story": (
            "found on the training box, of all places.\n\n"
            "somebody hid this where a new analyst would trip over it on their\n"
            "first ls -la. maybe that was the point. read the rest of them and\n"
            "you will understand why this exists."
        ),
    },
    {
        "id": "note2",
        "name": "Secret note 2",
        "unlock_xp": 100,
        "seeded_at": "/var/log/.note",
        "ciphertext": "q24p-NUFH-DS2",
        "story": (
            "TBR\n"
        ),
    },
    {
        "id": "note3",
        "name": "Secret note 3",
        "unlock_xp": 160,
        "seeded_at": "/home/svc-deploy/.note",
        "ciphertext": "pbce-NUFH-DS3",
        "story": (
            "TBR\n"
        ),
    },
    {
        "id": "note4",
        "name": "Secret note 4",
        "unlock_xp": 240,
        "seeded_at": "/home/svc-deploy/.ssh/.note",
        "ciphertext": "283m-NUFH-DS4",
        "story": (
            "TBR\n"
        ),
    },
    {
        "id": "note5",
        "name": "Secret note 5",
        "unlock_xp": 320,
        "seeded_at": "/opt/build/.note",
        "ciphertext": "g4eg-NUFH-DS5",
        "story": (
            "TBR\n"
        ),
    },
]

SECRET_PROMPT = "Paste the string you have. If it is a cipher, this will unlock it."
SECRET_WRONG = "That is not for this note or it is just a string."
SECRET_LOCKED = "Locked. Close cases and it comes with the rank."
SECRET_READY = "Ready. Find ciphers in quests"


STARTING_RANK = "Trainee"
