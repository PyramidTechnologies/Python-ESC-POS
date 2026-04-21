##  @brief Demonstrates both Standard and Simplified logo printing for Reliance.
#  @details Standard allows for partial logo printing, while Simplified uses flash dimensions.
#  @see [Images and Barcode](https://escpos.readthedocs.io/en/latest/imaging.html#images-and-barcode)

from py_esc_pos.printer.reliance_printer import ReliancePrinter
from py_esc_pos.commands import RelianceCommands
from py_esc_pos.menu.util import find_port

def run_logo_print():
    ports = find_port()
    if not ports:
        print("No printer found.")
        return

    printer = ReliancePrinter(ports[0].device)

    try:
        # Initialize
        printer.send_command(RelianceCommands.INIT)

        # --- METHOD 1: PRINT LOGO (SIMPLIFIED) ---
        # Prints logo 'n' using the dimensions already stored in flash.
        # @see [Print Graphic Bank/Logo (Simplified)](https://escpos.readthedocs.io/en/latest/imaging.html#print-graphic-bank-logo-simplified-1c-79-rel)
        logo_index = b'\x01'
        reserved = b'\x00'  # Must be zero

        printer.send_command(b"Logo (Simplified):\n")
        printer.send_command(RelianceCommands.PRINT_GRAPHIC_BANK_LOGO_SIMPLIFIED + logo_index + reserved)
        printer.send_command(b"End of Logo (Simplified)\n")
        printer.send_command(RelianceCommands.LINE_FEED * 2)

        # --- METHOD 2: PRINT LOGO (STANDARD) ---
        # Format: n + xH + xL + yH + yL
        # xH/xL: Starting dotline (0 in this case)
        # yH/yL: Number of dotlines to print (200 in this case, hex 0xC8)
        # @see [Print Graphic Bank/Logo](https://escpos.readthedocs.io/en/latest/imaging.html#print-graphic-bank-logo-1b-fa)
        start_line = b'\x00\x00'  # xH, xL
        line_count = b'\x00\xc8'  # yH, yL (200 dots)

        printer.send_command(b"Logo (Standard):\n")
        printer.send_command(RelianceCommands.PRINT_GRAPHIC_BANK_LOGO + logo_index + start_line + line_count)
        printer.send_command(b"End of Logo (Standard)\n")

        # Cut and Eject Paper
        printer.send_command(RelianceCommands.LINE_FEED * 4)
        printer.send_command(RelianceCommands.EJECTOR + b'\x05')
        print("Logo samples sent successfully.")

    except Exception as e:
        print(f"Failed to send command: {e}")
    finally:
        printer.close()

if __name__ == "__main__":
    run_logo_print()