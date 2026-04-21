#  @brief Basic Command Execution for phoenix Printers.
#  @details This sample demonstrates how to initialize the printer, print text, and trigger a full cut using ESC/POS constants.

from py_esc_pos.printer.phoenix_printer import PhoenixPrinter
from py_esc_pos.commands import PhoenixCommands
from py_esc_pos.menu.util import find_port
## Illustrates the standard "Initialize -> Action -> Cut" workflow.
#  @see [phoenix Paper Movement Commands](https://escpos.readthedocs.io/en/latest/paper_movement.html)
def run_basic_print():
    ports = find_port()
    if not ports:
        print("No printer found.")
        return

    # Use the first detected printer port by default.
    printer = PhoenixPrinter(ports[0].device)

    try:
        # Initialize
        printer.send_command(PhoenixCommands.INIT)

        # Send Text Data
        print("Sending text...")
        printer.send_command(b"phoenix Sample Print\n")
        printer.send_command(b"--------------------\n")
        printer.send_command(b"Command Sample\n\n")

        # Feed and Cut (GS V)
        # We feed a bit of paper so the text clears the cutter blade
        print("Cutting paper...")
        printer.send_command(PhoenixCommands.FULL_CUT)

    except Exception as e:
        print(f"Failed to send command: {e}")
    finally:
        printer.close()

if __name__ == "__main__":
    run_basic_print()