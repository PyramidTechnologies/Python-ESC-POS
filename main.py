import phoenix_printer as phoenix
import serial.tools.list_ports as port_list
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

console = Console()

def select_printer_port():
    ports = list(port_list.comports())

    if not ports:
        console.print("[bold red]Error:[/bold red] No serial ports detected. Check your USB cable.")
        return None

    # Create a simple table for selection
    table = Table(title="Available Serial Ports", header_style="bold cyan")
    table.add_column("Index", justify="center")
    table.add_column("Port", style="green")
    table.add_column("Description")

    for i, p in enumerate(ports):
        table.add_row(str(i), p.device, p.description)

    console.print(table)

    choice = Prompt.ask(
        "Select the port index for your Phoenix Printer",
        choices=[str(i) for i in range(len(ports))],
        default="0"
    )

    selected_port = ports[int(choice)].device
    console.print(f"Selected: [bold magenta]{selected_port}[/bold magenta]\n")
    return selected_port
if __name__ == "__main__":

    device_port = select_printer_port()

    with phoenix.PhoenixPrinter(device_port) as printer:
        print(f"Connection Logic Check: {printer.verify_logic_link()}")

        print(f"Paper Status: {printer.get_paper_status()}")