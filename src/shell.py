"""Разбор и выполнение команд прототипа оболочки."""

import shlex
from dataclasses import dataclass


MAX_CD_ARGS = 1


@dataclass(frozen=True)
class Result:
    """Результат выполнения одной строки."""

    output: str = ""
    should_exit: bool = False
    error: bool = False


def execute(line: str) -> Result:
    """Выполнить одну строку, сохраняя ls и cd заглушками."""
    try:
        parts = shlex.split(line)
    except ValueError:
        return Result("Ошибка: незакрытая кавычка", error=True)
    if not parts:
        return Result()

    command, *args = parts
    if command == "ls":
        return Result(f"ls: {args!r}")
    if command == "cd":
        if len(args) > MAX_CD_ARGS:
            return Result(
                "Ошибка: cd: ожидается не более одного аргумента",
                error=True,
            )
        return Result(f"cd: {args!r}")
    if command == "exit":
        if args:
            return Result("Ошибка: exit: аргументы не допускаются", error=True)
        return Result(should_exit=True)
    return Result(f"Ошибка: неизвестная команда: {command}", error=True)
