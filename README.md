# TerminalRPG

An interactive, story-driven terminal RPG that teaches cybersecurity and CLI through Linux challenges. Every quest takes place inside an isolated sandbox, allowing players to solve problems using real Bash commands while progressing through a detective-style narrative.



## About

TerminalRPG started as part of my MSc Cybersecurity dissertation exploring **Meaningful Gamification** in cybersecurity education.

Unlike traditional educational games that rely on streaks, and leaderboards to maintain engagment. TerminalRPG focuses on intrinsic motivation by integrating game mechanics directly into the narrative and learning experience. The project demonstrates how storytelling, player agency, and exploration can make cybersecurity learning more engaging.

Each quest runs inside a Docker-based Linux sandbox, giving players access to a real shell where they can use almost any Bash command safely without affecting the host system.




## Requirements

- Docker  
- Python 3.12+
- uv 

## Installation 
Clone the repository and run:

### Linux/Mac & Windows

```
uv sync

docker build --no-cache --network=none -t terminal-rpg-sandbox rpg/sandbox/image

uv run play.py
```

`uv` automatically manages the Python virtual environment and project dependencies. You do not need to manually create or activate a virtual environment or install dependencies with pip.

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
