import asyncio
import os
import pty
import select
import shutil
import subprocess
import time
import uuid
from pathlib import Path

from .base import TIMEOUT_SECONDS, CommandResult, Runner

IMAGE = "terminal-rpg-sandbox"
LABEL = "terminal-rpg"
IMAGE_DIR = Path(__file__).parent / "image"
RS = "\x1e"
SENTINEL = f"printf '\\036%s\\036%s\\036' \"$?\" \"$PWD\""


class SandboxError(RuntimeError):
    pass


def _docker() -> str:
    found = shutil.which("docker")
    if not found:
        raise SandboxError("docker is not installed, or is not on PATH.")
    return found


def _sh(argv: list[str], timeout: int = 120) -> subprocess.CompletedProcess:
    return subprocess.run(
        argv, capture_output=True, text=True, timeout=timeout, check=False
    )


def docker_ready() -> tuple[bool, str]:
    found = shutil.which("docker")
    if not found:
        return False, "Docker is not installed, or not on PATH."
    info = _sh([found, "info"], timeout=20)
    if info.returncode != 0:
        return False, (
            "Docker is installed but the daemon is not running.\n"
            "Start Docker Desktop"
        )
    return True, ""


def image_exists() -> bool:
    return _sh([_docker(), "image", "inspect", IMAGE]).returncode == 0


def _ensure_image() -> None:
    if image_exists():
        return
    built = _sh([_docker(), "build", "-t", IMAGE, str(IMAGE_DIR)], timeout=600)
    if built.returncode != 0:
        raise SandboxError(f"could not build the sandbox image:\n{built.stderr[-800:]}")


def sweep_orphans() -> int:
    listed = _sh(
        [_docker(), "ps", "-aq", "--filter", f"label={LABEL}"], timeout=30
    )
    ids = [line for line in listed.stdout.split() if line]
    if ids:
        _sh([_docker(), "rm", "-f", *ids], timeout=60)
    return len(ids)


class DockerRunner(Runner):
    def __init__(self, quest_id: str, host: str) -> None:
        self.quest_id = quest_id
        self.host = host
        self.name = f"rpg-{uuid.uuid4().hex[:12]}"
        self.cwd = "/root"
        self.master: int | None = None
        self.proc: subprocess.Popen | None = None

    async def start(self) -> str:
        await asyncio.to_thread(self._boot)
        return self.cwd

    async def stop(self) -> None:
        await asyncio.to_thread(self._teardown)

    async def run(self, command: str) -> CommandResult:
        blocked = self.blocked_program(command)
        if blocked:
            return CommandResult(
                output=(
                    f"{blocked}: interactive programs are not available in this session."
                ),
                exit_code=126,
                cwd=self.cwd,
                blocked=True,
            )
        return await asyncio.to_thread(self._exchange, command)

    async def inspect(self, argv: list[str]) -> tuple[int, str]:
        return await asyncio.to_thread(self._inspect, argv)

    def _boot(self) -> None:
        _ensure_image()

        created = _sh(
            [
                _docker(), "run", "-d", "--rm",
                "--name", self.name,
                "--label", LABEL,
                "--hostname", self.host,
                "--network", "none",
                "--memory", "512m",
                "--pids-limit", "256",
                IMAGE,
                "sleep", "infinity",
            ]
        )
        if created.returncode != 0:
            raise SandboxError(f"could not start the sandbox:\n{created.stderr[-800:]}")

        seeded = _sh(
            [_docker(), "exec", self.name, "/bin/bash", f"/opt/seed/{self.quest_id}.sh"]
        )
        if seeded.returncode != 0:
            self._teardown()
            raise SandboxError(f"could not seed the host:\n{seeded.stderr[-800:]}")

        self.master, slave = pty.openpty()
        self.proc = subprocess.Popen(
            [
                _docker(), "exec", "-it", self.name,
                "/bin/bash", "--norc", "--noprofile",
            ],
            stdin=slave,
            stdout=slave,
            stderr=slave,
            close_fds=True,
        )
        os.close(slave)

        self._write(
            "stty -echo cols 400 rows 100\n"
            "export PS1='' PS2='' PAGER=cat TERM=dumb\n"
            "cd /root\n"
        )
        self._exchange_raw("")

    def _teardown(self) -> None:
        if self.proc is not None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.proc.kill()
            self.proc = None
        if self.master is not None:
            os.close(self.master)
            self.master = None
        _sh([_docker(), "rm", "-f", self.name], timeout=30)

    def _inspect(self, argv: list[str]) -> tuple[int, str]:
        done = _sh([_docker(), "exec", self.name, *argv], timeout=10)
        return done.returncode, (done.stdout + done.stderr)

    def _write(self, text: str) -> None:
        os.write(self.master, text.encode())

    def _exchange(self, command: str) -> CommandResult:
        try:
            return self._exchange_raw(command)
        except TimeoutError:
            os.write(self.master, b"\x03")
            try:
                interrupted = self._read_until(deadline=time.monotonic() + 5)
                _, _, cwd = self._split(interrupted)
                self.cwd = cwd or self.cwd
            except TimeoutError:
                pass
            return CommandResult(
                output=f"[interrupted after {TIMEOUT_SECONDS}s]",
                exit_code=130,
                cwd=self.cwd,
                timed_out=True,
            )

    def _exchange_raw(self, command: str) -> CommandResult:
        self._write(f"{command}\n{SENTINEL}\n")
        text = self._read_until(deadline=time.monotonic() + TIMEOUT_SECONDS)
        output, code, cwd = self._split(text)
        self.cwd = cwd or self.cwd
        return CommandResult(output=output, exit_code=code, cwd=self.cwd)

    MAX_OUTPUT_BYTES = 256 * 1024

    def _read_until(self, deadline: float) -> str:
        buffer = b""
        truncated = False
        while buffer.count(b"\x1e") < 3:
            if time.monotonic() > deadline:
                raise TimeoutError
            ready, _, _ = select.select([self.master], [], [], 0.1)
            if not ready:
                if self.proc is not None and self.proc.poll() is not None:
                    raise SandboxError("the sandbox exited unexpectedly.")
                continue
            chunk = os.read(self.master, 65536)
            if not chunk:
                break
            buffer += chunk
            if len(buffer) > self.MAX_OUTPUT_BYTES and not truncated:
                truncated = True
        text = buffer.decode("utf-8", errors="replace")
        if truncated:
            head, _, tail = text.partition("\x1e")
            text = head[: self.MAX_OUTPUT_BYTES] + "\n[output truncated]\n\x1e" + tail
        return text

    @staticmethod
    def _split(text: str) -> tuple[str, int, str]:
        parts = text.split(RS)
        if len(parts) < 3:
            return text.replace("\r\n", "\n").strip("\n"), 0, ""
        output = parts[0].replace("\r\n", "\n").strip("\n")
        try:
            code = int(parts[1].strip())
        except ValueError:
            code = 0
        cwd = parts[2].strip()
        return output, code, cwd
