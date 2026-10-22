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

### Setup

Clone the repository and navigate to the project directory.

```bash
git clone https://github.com/faisalalhatimi/terminal-rpg.git
cd terminal-rpg
```

Install the project dependencies:

```bash
uv sync
```

Build the Docker image used by the game:

```bash
docker build --no-cache --network=none -t terminal-rpg-sandbox rpg/sandbox/image
```

Start the game:

```bash
uv run play.py
```

`uv` manages the Python virtual environment and project dependencies. You do not need to create or activate a virtual environment manually or install dependencies using `pip`.

## Manual Installation

If you prefer to install the dependencies manually, follow these steps.

1. Install Python 3.12 or later and Docker.
2. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment.

   **Windows:**

   ```powershell
   .venv\Scripts\activate
   ```

   **Linux/macOS:**

   ```bash
   source .venv/bin/activate
   ```

4. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Build the Docker image:

   ```bash
   docker build --no-cache --network=none -t terminal-rpg-sandbox rpg/sandbox/image
   ```

6. Start the game:

   ```bash
   python play.py
   ```
   
## Known Problems

### Docker network error while building

If Docker cannot download the base image, pull it manually first:
```
docker pull debian:12-slim
```

Then rebuild the image.



## Architecture

- TODO
