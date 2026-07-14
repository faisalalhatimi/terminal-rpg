# TerminalRPG

An interactive, story-driven terminal RPG that teaches cybersecurity and CLI through Linux challenges. Every quest takes place inside an isolated sandbox, allowing players to solve problems using real Bash commands while progressing through a detective-style narrative.



## About

TerminalRPG started as part of my MSc Cybersecurity dissertation exploring **Meaningful Gamification** in cybersecurity education.

Unlike traditional educational games that rely on streaks, and leaderboards to maintain engagment. TerminalRPG focuses on intrinsic motivation by integrating game mechanics directly into the narrative and learning experience. The project demonstrates how storytelling, player agency, and exploration can make cybersecurity learning more engaging.

Each quest runs inside a Docker-based Linux sandbox, giving players access to a real shell where they can use almost any Bash command safely without affecting the host system.




## Requirements

- Docker  
- Python 3.12+
- Textual
- Rich

## Installation 

### Linux/Mac

```
python3.12 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

docker build --no-cache --network=none -t terminal-rpg-sandbox rpg/sandbox/image

python3.12 play.py
```

### Windows

```
python -m venv .venv

.venv\Scripts\activate

python pip install -r requirements.txt

docker build --no-cache --network=none -t terminal-rpg-sandbox rpg/sandbox/image

python play.py
```
## Manual Installation 

- Run Docker
- Make a virtual environment `venv` using python 3.12+
- Activate the virtual environment using `.venv\Scripts\activate`(Windows) or `source .venv/bin/activate`(Linux/Mac)
- Install dependencies using `pip install -r requirements.txt`
- Build a docker image using the `Dockerfile` from `rpg/sandbox/image` use `--no-cache` and `--network=none` flags 
-  Run the game using `play.py`

## Known Problems

### Docker network error while building

If Docker cannot download the base image, pull it manually first:
```
docker pull debian:12-slim
```

Then rebuild the image.



## Architecture

- TODO
