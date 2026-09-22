"""Проверки параметров и выполнения стартового скрипта."""

import tempfile
import unittest
from pathlib import Path

from src.config import parse_args, run_script
from src.shell import execute


class ConfigTests(unittest.TestCase):
    """Проверить параметры и продолжение после ошибок."""

    def test_paths(self) -> None:
        """Проверить передачу обоих путей через параметры запуска."""
        args = parse_args(["--vfs", "data.csv", "--script", "start.txt"])
        self.assertEqual(args.vfs, Path("data.csv"))
        self.assertEqual(args.script, Path("start.txt"))

    def test_script_continues_after_error_and_stops_at_exit(self) -> None:
        """Проверить продолжение после ошибки и остановку на exit."""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "start.txt"
            path.write_text("bad\nls ok\nexit\nls skipped\n")
            seen = []

            def run(line: str) -> bool:
                """Сохранить результат команды и признак завершения."""
                seen.append((line, execute(line)))
                return seen[-1][1].should_exit

            run_script(path, run)
        self.assertEqual([item[0] for item in seen], ["bad", "ls ok", "exit"])
        self.assertTrue(seen[0][1].error)
        self.assertEqual(seen[1][1].output, "ls: ['ok']")

    def test_missing_script(self) -> None:
        """Проверить ошибку открытия отсутствующего скрипта."""
        with self.assertRaises(FileNotFoundError):
            run_script(Path("missing-script-12345"), lambda _: False)


if __name__ == "__main__":
    unittest.main()
