from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
import serial.tools.list_ports as port_list
import phoenix_printer
import reliance_printer
from commands import PhoenixCommands, RelianceCommands

console = Console()

def select_port():
    ports = list(port_list.comports())
    if not ports:
        console.print("[bold red]No ports found.[/bold red]")
        return None

    ports_str = ""
    for i, p in enumerate(ports):
       ports_str += f"\n  {i}: [green]{p.device}[/green] ({p.description})"
    console.print(Panel(ports_str, title="Serial Ports"))

    choice = Prompt.ask("Use port index to select port")
    return ports[int(choice)].device

def verify_printer_connection(printer):
    status = printer.verify_logic_link()
    if "ONLINE" in status:
        console.print(f"[bold green]Connected![/bold green]")
        return True
    else:
        console.print(f"[bold red]Connection failed:[/bold red] {status}")
        return False

class PrinterMenu:
    def __init__(self):
        self.printer = None

    def connect(self):
        port = select_port()
        if not port: return False

        printer_type = Prompt.ask(
            "\nSelect Printer Type",
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
        """Main interaction loop."""
        if not self.connect(): return

        while True:
            is_phoenix = isinstance(self.printer, phoenix_printer.PhoenixPrinter)

            menu_text = "[bold yellow]General Commands[/bold yellow]\n"
            menu_text += "1. Paper Status\n2. Datetime\n"

            if is_phoenix:
                menu_text += "\n[bold magenta]Phoenix Specific[/bold magenta]\n"
                menu_text += "3. Coin Test\n4. Note Test\n5. Print RTC"
            else:
                menu_text += "\n[bold magenta]Reliance Specific[/bold magenta]\n"
                menu_text += "3. Full Status (6-byte)\n4. Full Cut"

            console.print(Panel(menu_text, title="Main Menu"))
            choice = Prompt.ask("Action", choices=["0", "1", "2", "3", "4", "5", "6"], default="0")

            if choice == "0": break
            self.handle_choice(choice, is_phoenix)

    def handle_choice(self, choice, is_phoenix):
        if choice == "1":
            console.print(f"Paper: [bold]{self.printer.get_paper_status()}[/bold]")
        elif choice == "2":
            console.print(f"Datetime {self.printer.send_command(PhoenixCommands.GET_DATETIME)}")
        elif is_phoenix:
            if choice == "3": self.printer.send_command(PhoenixCommands.TEST_COIN_IN)
            if choice == "4": self.printer.send_command(PhoenixCommands.TEST_NOTE_IN)
            if choice == "5": self.printer.send_command(PhoenixCommands.PRINT_RTC + b'\x00\x0a')
            if choice == "6": console.print(f"Printer ID: {self.printer.print_rtc()}")
        else:
            # Reliance logic
            if choice == "3": console.print(self.printer.get_full_status())
