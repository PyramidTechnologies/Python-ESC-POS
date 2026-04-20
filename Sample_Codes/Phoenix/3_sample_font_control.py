#  @brief Demonstrates font styling and selection on Phoenix printers.
#  @details This sample covers bold, underline, and switching between Font A (12x24) and Font B (9x17).
#  @see [Font Controlling Commands](https://escpos.readthedocs.io/en/latest/font_cmds.html)
from Printer.phoenix_printer import PhoenixPrinter
from commands import PhoenixCommands
from Menu.util import find_port
import sys
import os

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def run_font_sample():
    ports = find_port()
    if not ports:
        print("No printer found.")
        return

    # Use the first detected printer port by default.
    printer = PhoenixPrinter(ports[0].device)

    try:
        # Initialize
        printer.send_command(PhoenixCommands.INIT)

        # Emphasis (Bold) Mode
        # @see [Phoenix Emphasis Command] (https://escpos.readthedocs.io/en/latest/font_cmds.html#emphasis-mode-1b-45)
        printer.send_command(b"Standard Text")
        printer.send_command(PhoenixCommands.EMPHASIS_MODE + PhoenixCommands.ON)
        printer.send_command(b"Emphasized (Bold) Text")
        printer.send_command(PhoenixCommands.LINE_FEED)
        printer.send_command(PhoenixCommands.EMPHASIS_MODE + PhoenixCommands.OFF)

        # Underline Mode
        # @see [Phoenix Underline Command] (https://escpos.readthedocs.io/en/latest/font_cmds.html#underline-mode-1b-2d)
        printer.send_command(PhoenixCommands.UNDERLINE_MODE + PhoenixCommands.ON)
        printer.send_command(b"Underlined Text")
        printer.send_command(PhoenixCommands.LINE_FEED)
        printer.send_command(PhoenixCommands.UNDERLINE_MODE + PhoenixCommands.OFF)

        # Font Selection
        # Font A is standard (12w x 24h), Font B is condensed (9w x 17h)
        # @see [Phoenix Font A Command] (https://escpos.readthedocs.io/en/latest/font_cmds.html#select-character-font-1b-4d)
        printer.send_command(b"This is Font A")
        printer.send_command(PhoenixCommands.LINE_FEED)
        printer.send_command(PhoenixCommands.SELECT_FONT_B)
        printer.send_command(b"This is Font B (Condensed)")
        printer.send_command(PhoenixCommands.LINE_FEED)
        printer.send_command(PhoenixCommands.SELECT_FONT_A)

        # Feed and Cut
        printer.send_command(PhoenixCommands.LINE_FEED * 2)  # Feed some lines to clear the cutter
        printer.send_command(PhoenixCommands.FULL_CUT)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        printer.close()


if __name__ == "__main__":
    run_font_sample()