#  @brief Basic Command Execution for Reliance printers.
#  @details This sample demonstrates how to initialize the printer, print text, and trigger a full cut using ESC/POS constants.
import sys
import os

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Printer.reliance_printer import ReliancePrinter
from commands import RelianceCommands
from Menu.util import find_port
## Illustrates the standard "Initialize -> Action -> Cut" workflow.
#  @see [Phoenix Paper Movement Commands](https://escpos.readthedocs.io/en/latest/paper_movement.html)
def run_basic_print():
    ports = find_port()
    if not ports:
        print("No printer found.")
        return

    # Use the correct port index based on your setup. Here we use ports[0] as in previous samples.
    printer = ReliancePrinter(ports[0].device)

    try:
        # Initialize
        printer.send_command(RelianceCommands.INIT)

        # Send Text Data
        print("Sending text...")
        printer.send_command(b"Reliance Sample Print\n")
        printer.send_command(b"--------------------\n\n\n\n\n")
        printer.send_command(b"Command Sample\n\n")

        # Cut and Eject Paper
        # @see [Reliance Ejector Commands](https://escpos.readthedocs.io/en/latest/paper_movement.html#ejector-1d-65-rel)
        print("Cutting paper...")
        printer.send_command(RelianceCommands.EJECTOR +b'\x05')


    except Exception as e:
        print(f"Failed to send command: {e}")
    finally:
        printer.close()

if __name__ == "__main__":
    run_basic_print()