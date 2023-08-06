from rich.console import Console


class RichOutputCallBack:
    console = Console()

    def print_header(self, line):
        self.console.rule(f"", style="cyan")
        self.console.rule(f"{line}", style="cyan")
        self.console.rule(f"", style="cyan")

    def print_line(self, line):
        self.console.print(line, end="")
