import argparse
from pathlib import Path
from typing import Callable

from .shell import Result


DEFAULT_VFS = Path("demo.vfs")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Графический эмулятор оболочки"
    )
    parser.add_argument(
        "--vfs",
        type=Path,
        default=DEFAULT_VFS,
        help="путь к физическому расположению VFS",
    )
    parser.add_argument(
        "--script",
        type=Path,
        help="путь к стартовому скрипту",
    )
    return parser.parse_args(argv)

def run_script(path: Path, run_command: Callable[[str], Result]) -> bool:
    had_errors = False
    with path.open(encoding="utf-8") as script:
        for line in script:
            result = run_command(line.rstrip("\r\n"))
            had_errors = had_errors or result.error
            if result.should_exit:
                break
    return had_errors
