import asyncio

from shemes.cli import CLIResult


async def run_cmd(cmd: str) -> CLIResult:
    """Функция выполняет команду и возвращает ответ."""
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    return CLIResult(
        status_code=proc.returncode if proc.returncode is not None else 1,
        stdout=stdout.decode("utf-8"),
        stderr=stderr.decode("utf-8"),
    )
