"""Проверки команд прототипа без графического дисплея."""

import unittest

from src.shell import execute


class ShellTests(unittest.TestCase):
    """Основные варианты интерактивных команд."""

    def test_quoted_arguments(self) -> None:
        self.assertEqual(
            execute('ls "папка с пробелами"').output,
            "ls: ['папка с пробелами']",
        )

    def test_errors(self) -> None:
        for line in ('bad', 'cd a b', 'exit now', 'ls "unfinished'):
            with self.subTest(line=line):
                self.assertTrue(execute(line).error)

    def test_exit(self) -> None:
        self.assertTrue(execute("exit").should_exit)

    def test_empty_line(self) -> None:
        self.assertEqual(execute("   ").output, "")


if __name__ == "__main__":
    unittest.main()
