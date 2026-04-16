from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from commands import PhoenixCommands, RelianceCommands, Commands

console = Console()

def add_font_type(print_buffer, font_type):
    if not print_buffer:
        console.print("[bold red]No lines to set font for![/bold red]")
        return
    type_map = {"A": PhoenixCommands.SELECT_FONT_A, "B": PhoenixCommands.SELECT_FONT_B, "C": PhoenixCommands.SELECT_FONT_C}
    print_buffer[-1]["type"] = type_map[font_type]

def add_font_style(print_buffer, style):
    if not print_buffer:
        console.print("[bold red]No lines to set font for![/bold red]")
        return
    style_map = {"bold": PhoenixCommands.EMPHASIS_MODE, "italic": PhoenixCommands.ITALIC_MODE,
                 "underline": PhoenixCommands.UNDERLINE_MODE}
    print_buffer[-1]["style_on"] = style_map[style] + PhoenixCommands.ON
    print_buffer[-1]["style_off"] = style_map[style] + PhoenixCommands.OFF

def remove_last_line(print_buffer):
    if not print_buffer:
        console.print("[bold red]No lines to remove![/bold red]")
        return
    removed = print_buffer.pop()
    console.print(f"[yellow]Removed:[/yellow] {removed['text']}")

class PrintMenu:
    def __init__(self, printer):
        self.printer = printer
        self.menu_print_settings()

    def menu_print_settings(self):
        print_buffer = []
        while True:
            preview_table = Table(title="[bold cyan]Print Spooler[/bold cyan]", expand=True)
            preview_table.add_column("Line", style="dim", width=4)
            preview_table.add_column("Content", style="white")
            preview_table.add_column("Format", style="green")

            for i, line in enumerate(print_buffer):
                is_working = (i == len(print_buffer) - 1)
                pointer = ">> " if is_working else f"{i + 1} "
                row_style = "bold yellow" if is_working else "white"

                fmt = []
                if line.get("type"): fmt.append("Type")
                if line.get("style_on"): fmt.append("Style")
                fmt_str = "+".join(fmt) if fmt else "None"

                preview_table.add_row(
                    pointer,
                    line['text'],
                    fmt_str,
                    style=row_style
                )

            menu_text = (
                "1. [bold cyan]Input Text Line[/bold cyan]\n"
                "2. [bold cyan]Set Font Type[/bold cyan] (Last Line)\n"
                "3. [bold cyan]Set Font Style[/bold cyan] (Last Line)\n"
                "4. [red]Remove Last Line[/red]\n"
                "5. [bold magenta]PROCESS PRINT JOB[/bold magenta]\n"
                "6. [yellow]Back to Main Menu[/yellow]\n"
                "0. Exit"
            )
            menu_panel = Panel(menu_text, title="Print Settings", expand=False)

            console.print(Columns([menu_panel, preview_table]))

            choice = Prompt.ask("Action", choices=["0", "1", "2", "3", "4", "5", "6"], default="6")
            if choice == "6": break

            self.handle_choice(choice, print_buffer)


    def handle_choice(self, choice, print_buffer=None):
        if choice == "0": exit()

        if choice == "1":
            text = Prompt.ask("Enter text to print")
            print_buffer.append({
                "text": text,
                "type": b'',
                "style_on": b'',
                "style_off": b''
            })
        elif choice == "2":
            style_type = Prompt.ask("Enter font type", choices=["A", "B", "C"])
            add_font_type(print_buffer, style_type)
        elif choice == "3":
            style = Prompt.ask("Style", choices=["bold", "italic", "underline", "normal"])
            add_font_style(print_buffer, style)
        elif choice == "4":
            remove_last_line(print_buffer)
        elif choice == "5":
            self.print_job(print_buffer)
            print_buffer.clear()

    def print_job(self, print_buffer):
        if not print_buffer:
            console.print("[bold red]No lines to remove![/bold red]")
            return
        self.printer.send_command(PhoenixCommands.INIT)
        for line in print_buffer:
            if line["type"]:
                self.printer.send_command(line["type"])
            if line["style_on"]:
                self.printer.send_command(line["style_on"])

            self.printer.send_command(line["text"].encode('ascii') + PhoenixCommands.LINE_FEED)

            if line["style_off"]:
                self.printer.send_command(line["style_off"])

        self.printer.send_command(PhoenixCommands.LINE_FEED)
        self.printer.send_command(PhoenixCommands.FULL_CUT)
        print_buffer.clear()
