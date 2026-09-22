"""Графический интерфейс эмулятора."""

import tkinter as tk

from .config import parse_args, run_script
from .shell import execute


VFS_NAME = "demo.vfs"


class ShellWindow:
    """Окно с историей диалога и полем ввода."""

    def __init__(self, root: tk.Tk, vfs_name: str = VFS_NAME) -> None:
        self.root = root
        root.title(f"Эмулятор — {vfs_name}")
        root.geometry("720x420")
        self.output = tk.Text(root, state="disabled", wrap="word")
        self.output.pack(fill="both", expand=True, padx=8, pady=8)
        self.entry = tk.Entry(root)
        self.entry.pack(fill="x", padx=8, pady=(0, 8))
        self.entry.bind("<Return>", self.submit)
        self.entry.focus_set()

    def write(self, message: str) -> None:
        """Добавить строку в область диалога."""
        self.output.configure(state="normal")
        self.output.insert("end", message + "\n")
        self.output.configure(state="disabled")
        self.output.see("end")

    def run_command(self, line: str) -> bool:
        """Показать ввод и результат; вернуть признак завершения."""
        self.write(f"$ {line}")
        result = execute(line)
        if result.output:
            self.write(result.output)
        if result.should_exit:
            self.root.after_idle(self.root.destroy)
        return result.should_exit

    def submit(self, _event: tk.Event) -> None:
        """Выполнить строку из поля ввода."""
        line = self.entry.get()
        self.entry.delete(0, "end")
        self.run_command(line)


def main() -> None:
    """Запустить интерактивное окно."""
    args = parse_args()
    root = tk.Tk()
    window = ShellWindow(root, args.vfs.name)
    window.write(f"VFS: {args.vfs}")
    window.write(f"Стартовый скрипт: {args.script or 'не задан'}")
    if args.script is not None:
        try:
            run_script(args.script, window.run_command)
        except (OSError, UnicodeError) as error:
            window.write(f"Ошибка стартового скрипта: {error}")
    root.mainloop()


if __name__ == "__main__":
    main()
