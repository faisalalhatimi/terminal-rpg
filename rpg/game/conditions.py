import shlex

from ..sandbox.base import Runner


async def _ran(runner: Runner, script: str) -> bool:
    code, _ = await runner.inspect(["/bin/sh", "-c", script])
    return code == 0


async def file_exists(runner: Runner, condition: dict, cwd: str) -> bool:
    return await _ran(runner, f"test -e {shlex.quote(condition['path'])}")


async def file_absent(runner: Runner, condition: dict, cwd: str) -> bool:
    return not await file_exists(runner, condition, cwd)


async def file_contains(runner: Runner, condition: dict, cwd: str) -> bool:
    path = shlex.quote(condition["path"])
    needle = shlex.quote(condition["contains"])
    return await _ran(runner, f"grep -qF -- {needle} {path}")


async def process_absent(runner: Runner, condition: dict, cwd: str) -> bool:
    name = shlex.quote(condition["name"])
    return not await _ran(runner, f"pgrep -x {name} >/dev/null")


async def permission_equals(runner: Runner, condition: dict, cwd: str) -> bool:
    path = shlex.quote(condition["path"])
    mode = str(condition["mode"])
    code, out = await runner.inspect(["/bin/sh", "-c", f"stat -c %a {path}"])
    return code == 0 and out.strip() == mode


async def path_reached(runner: Runner, condition: dict, cwd: str) -> bool:
    return cwd.rstrip("/") == condition["path"].rstrip("/")


CONDITIONS = {
    "file_exists": file_exists,
    "file_absent": file_absent,
    "file_contains": file_contains,
    "process_absent": process_absent,
    "permission_equals": permission_equals,
    "path_reached": path_reached,
}


async def satisfied(runner: Runner, condition: dict, cwd: str) -> bool:
    check = CONDITIONS.get(condition["type"])
    if check is None:
        raise ValueError(f"unknown condition type: {condition['type']}")
    return await check(runner, condition, cwd)
