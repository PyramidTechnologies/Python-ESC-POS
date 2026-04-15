from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table
from PIL import Image, ImageOps
from commands import PhoenixCommands, RelianceCommands, Commands
import serial.tools.list_ports as port_list
import phoenix_printer
import reliance_printer

console = Console()

def select_port():
    ports = list(port_list.comports())
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

def verify_printer_connection(printer):
    status = printer.verify_logic_link()
    if "ONLINE" in status:
        console.print(f"[bold green]Connected![/bold green]")
        return True
    else:
        console.print(f"[bold red]Connection failed:[/bold red] {status}")
        return False

def get_raster_blob(image_path, printer_width_pixels=384):
    img = Image.open(image_path).convert('1')

    img = ImageOps.invert(img.convert('L')).convert('1')

    w_percent = (printer_width_pixels / float(img.size[0]))
    h_size = int((float(img.size[1]) * float(w_percent)))
    img = img.resize((printer_width_pixels, h_size), Image.NEAREST)

    width_in_bytes = printer_width_pixels // 8

    xL, xH = width_in_bytes % 256, width_in_bytes // 256
    yL, yH = h_size % 256, h_size // 256

    header = PhoenixCommands.RASTER_IMAGE + b'\x00' + bytes([xL, xH, yL, yH])

    return header + img.tobytes()

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
        if not self.connect(): return

        while True:
            menu_text = (
                "1. [bold cyan]Print Menu[/bold cyan] (Text, Font, Style)\n"
                "2. [bold cyan]Print image[/bold cyan] \n"
                "3. [bold magenta]Send Raw Input[/bold magenta]\n"
                "4. [bold green]View Command List[/bold green]\n"
                "0. Exit"
            )

            console.print(Panel(menu_text, title="Main Menu", expand=False))
            choice = Prompt.ask("Action", choices=["0", "1", "2", "3", "4"], default="0")

            if choice == "0":
                self.printer.close()
                break

            self.handle_choice(choice)

    def handle_choice(self, choice):
        if choice == "1":
            self.menu_print_settings()
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
            self.printer.send_command(PhoenixCommands.INIT)
            self.printer.send_command(raster_blob)
            self.printer.send_command(b'\x0a\x0a')  # Feed
            self.printer.send_command(PhoenixCommands.FULL_CUT)
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
            console.print(f"Printer response (hex): [green]{hex_response}[/green]")
        console.print(f"Printer response: [green]00[/green]")

    def display_commands(self):
        is_phoenix = "Phoenix" in str(type(self.printer))
        phoenix_cmds = PhoenixCommands if is_phoenix else RelianceCommands

        table = Table(title=f"{phoenix_cmds.__name__} List", show_header=True, header_style="bold magenta")
        table.add_column("Command Name", style="cyan")
        table.add_column("Hex Value", style="green", justify="right")

        commands_to_show = {cmds_name: cmds_bytes for cmds_name, cmds_bytes in phoenix_cmds.__dict__.items() if cmds_name.isupper()}
        commands_to_show.update({cmds_name: cmds_bytes for cmds_name, cmds_bytes in Commands.__dict__.items() if cmds_name.isupper()})

        for name, value in sorted(commands_to_show.items()):
            hex_val = " ".join(f"{b:02X}" for b in value) if isinstance(value, bytes) else str(value)
            table.add_row(name, hex_val)

        console.print(table)
        Prompt.ask("\nPress [bold]Enter[/bold] to return to Main Menu")

    def menu_print_settings(self):
        print_buffer = []
        while True:
            print_text = (
                "1. Input Text Line\n"
                "2. Set Font Type for Last Line\n"
                "3. Set Font Style for Last Line\n"
                "4. [red]Remove Last Line[/red]\n"
                "5. [bold magenta]PROCESS PRINT JOB[/bold magenta]\n"
                "6. [yellow]Back to Main Menu[/yellow]\n"
                "0. Exit"
            )
            console.print(Panel(print_text, title="Print Settings", expand=False))
            choice = Prompt.ask("Action", choices=["0", "1", "2", "3", "4", "5", "6"], default="6")

            if choice == "6": break
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
                if not print_buffer:
                    console.print("[bold red]No lines to set font for![/bold red]")
                    continue
                size = Prompt.ask("Enter font type", choices=["A", "B", "C"])
                size_map = {"A": PhoenixCommands.SELECT_FONT_A, "B": PhoenixCommands.SELECT_FONT_B, "C": PhoenixCommands.SELECT_FONT_C}
                print_buffer[-1]["size"] = size_map[size]
            elif choice == "3":
                if not print_buffer:
                    console.print("[bold red]No lines to set font for![/bold red]")
                    continue
                style = Prompt.ask("Style", choices=["bold", "italic", "underline", "normal"])
                style_map = {"bold": PhoenixCommands.EMPHASIS_MODE, "italic": PhoenixCommands.ITALIC_MODE, "underline": PhoenixCommands.UNDERLINE_MODE}
                print_buffer[-1]["style_on"] = style_map[style] + b'\x01'
                print_buffer[-1]["style_off"] = style_map[style] + b'\x00'
            elif choice == "4":
                if print_buffer:
                    removed = print_buffer.pop()
                    console.print(f"[yellow]Removed:[/yellow] {removed['text']}")
            elif choice == "5":
                if not print_buffer:
                    console.print("[bold red]No lines to remove![/bold red]")
                    return
                self.print_job(print_buffer)
                print_buffer.clear()

    def print_job(self, print_buffer):
        console.print("[bold green]Sending job to printer...[/bold green]")
        console.print(print_buffer)
        self.printer.send_command(PhoenixCommands.INIT)
        for line in print_buffer:
            if line["type"]:
                self.printer.send_command(line["size"])
            if line["style_on"]:
                self.printer.send_command(line["style_on"])
            self.printer.send_command(line["text"].encode('ascii') + PhoenixCommands.LINE_FEED)
            if line["style_off"]:
                self.printer.send_command(line["style_off"])

        self.printer.send_command(PhoenixCommands.LINE_FEED)
        self.printer.send_command(PhoenixCommands.FULL_CUT)
        print_buffer.clear()