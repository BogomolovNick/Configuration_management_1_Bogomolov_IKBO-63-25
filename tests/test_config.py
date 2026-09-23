
import tempfile
import unittest
from pathlib import Path

from src.config import parse_args, run_script
from src.shell import Result, execute


class ConfigTests(unittest.TestCase):

    def test_paths(self) -> None:
        args = parse_args(["--vfs", "data.csv", "--script", "start.txt"])
        self.assertEqual(args.vfs, Path("data.csv"))
        self.assertEqual(args.script, Path("start.txt"))

    def test_script_continues_after_error_and_stops_at_exit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "start.txt"
            path.write_text("bad\nls ok\nexit\nls skipped\n")
            seen = []

            def run(line: str) -> Result:
                seen.append((line, execute(line)))
                return seen[-1][1]

            had_errors = run_script(path, run)
        self.assertTrue(had_errors)
        self.assertEqual([item[0] for item in seen], ["bad", "ls ok", "exit"])
        self.assertTrue(seen[0][1].error)
        self.assertEqual(seen[1][1].output, "ls: ['ok']")

    def test_demo_script_reports_errors(self) -> None:
        path = Path(__file__).resolve().parents[1] / "examples/demo.script"
        self.assertTrue(run_script(path, execute))

    def test_valid_script_has_no_errors(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "start.txt"
            path.write_text('ls "моя папка"\ncd\n', encoding="utf-8")
            self.assertFalse(run_script(path, execute))

    def test_missing_script(self) -> None:
        with self.assertRaises(FileNotFoundError):
            run_script(Path("missing-script-12345"), execute)


if __name__ == "__main__":
    unittest.main()
