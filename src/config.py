"""Параметры запуска и чтение стартового скрипта."""

import argparse
from pathlib import Path
from typing import Callable


DEFAULT_VFS = Path("demo.vfs")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Прочитать пути VFS и стартового скрипта из командной строки."""
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


def run_script(path: Path, run_command: Callable[[str], bool]) -> None:
    """Выполнить строки скрипта по порядку до exit или конца файла."""
    with path.open(encoding="utf-8") as script:
        for line in script:
            if run_command(line.rstrip("\r\n")):
                break
