from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table

from py_esc_pos.commands import PhoenixCommands, RelianceCommands, Commands
from py_esc_pos.printer import phoenix_printer, reliance_printer

from print_menu import PrintMenu
from util import get_raster_blob, find_port, verify_printer_connection

console = Console()

def select_port():
    ports = find_port()
    if not ports:
        console.print("[bold red]No ports found.[/bold red]")
        return None

    ports_list = ""
    for i, p in enumerate(ports):
        ports_list += f"     {i}: [green]{p.device}[/green] ({p.description})        "
        if i != len(ports)-1 : ports_list += "\n"

    console.print(Panel(ports_list, title="Available Ports", expand=False))
    choice = Prompt.ask("Use port index to select port")

    return ports[int(choice)].device

class MainMenu:
    def __init__(self):
        self.printer = None

    def connect(self):
        port = select_port()
        if not port: return False

        printer_type = Prompt.ask(
            "\nSelect printer Type",
            choices=["phoenix", "reliance"]
        ).lower()

        if printer_type == "phoenix":
            self.printer = phoenix_printer.PhoenixPrinter(port)
        elif printer_type == "reliance":
            self.printer = reliance_printer.ReliancePrinter(port)
        else:
            console.print("[bold red]Invalid printer type selected.[/bold red]")
            return False

        return verify_printer_connection(self.printer)

    def run(self):
        if not self.connect():
            console.print("[bold red]Failed to connect to printer. Exiting.[/bold red]")
            return

        self.menu()

    def menu(self):
        while True:
            menu_text = (
                "1. [bold cyan]Print menu[/bold cyan] (Text, Font, Style)\n"
                "2. [bold cyan]Print image[/bold cyan] \n"
                "3. [bold magenta]Send Raw Input[/bold magenta]\n"
                "4. [bold green]View Command List[/bold green]\n"
                "0. Exit"
            )

            console.print(Panel(menu_text, title="Main menu", expand=False))
            choice = Prompt.ask("Action", choices=["0", "1", "2", "3", "4"], default="0")

            if choice == "0":
                self.printer.close()
                break

            self.handle_choice(choice)

    def handle_choice(self, choice):
        if choice == "1":
            PrintMenu(self.printer)
        elif choice == "2":
            self.handle_print_image()
        elif choice == "3":
            self.handle_raw_input()
        elif choice == "4":
            self.display_commands()

    def handle_print_image(self):
        path = Prompt.ask("Enter image path")
        try:
            raster_blob = get_raster_blob(path)
            if self.printer.get_type() == "PhoenixPrinter":
                self.printer.send_command(PhoenixCommands.INIT)
                self.printer.send_command(raster_blob)
                self.printer.send_command(PhoenixCommands.FULL_CUT)
            elif self.printer.get_type() == "ReliancePrinter":
                self.printer.send_command(RelianceCommands.INIT)
                self.printer.send_command(raster_blob)
                self.printer.send_command(RelianceCommands.EJECTOR + b'\x05')
            else:
                console.print("[bold red]Unsupported printer type for image printing.[/bold red]")
                return
            console.print("[bold green]Image sent successfully![/bold green]")
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

    def handle_raw_input(self):
        raw_cmd = Prompt.ask("\nEnter ESCPOS hex")
        byte_data = bytes.fromhex(raw_cmd)
        console.print(f"Sending bytes: [blue]{byte_data}[/blue]")
        self.printer.send_command(byte_data)
        response = self.printer.read_response(timeout=2.0)
        hex_response = " ".join(f"{b:02X}" for b in response)
        if hex_response:
            console.print(f"printer response (hex): [green]{hex_response}[/green]")
        console.print(f"printer response: [green]00[/green]")

    def display_commands(self):
        is_phoenix = self.printer.get_type() == "PhoenixPrinter"
        cmds = PhoenixCommands if is_phoenix else RelianceCommands

        table = Table(title=f"{cmds.__name__} List", show_header=True, header_style="bold magenta")
        table.add_column("Command Name", style="cyan")
        table.add_column("Hex Value", style="green", justify="right")

        commands_to_show = {cmds_name: cmds_bytes for cmds_name, cmds_bytes in cmds.__dict__.items() if cmds_name.isupper()}
        commands_to_show.update({cmds_name: cmds_bytes for cmds_name, cmds_bytes in Commands.__dict__.items() if cmds_name.isupper()})

        for name, value in sorted(commands_to_show.items()):
            hex_val = " ".join(f"{b:02X}" for b in value) if isinstance(value, bytes) else str(value)
            table.add_row(name, hex_val)

        console.print(table)
        Prompt.ask("\nPress [bold]Enter[/bold] to return to Main menu")
