#  @brief Demonstrates supported positioning and alignment for Phoenix printers.
#  @details Focuses on Justification (Left/Center/Right) and Line Spacing,
#  as Phoenix uses these for layout over coordinate-based positioning.
#  @see [Layout Commands](https://escpos.readthedocs.io/en/latest/layout_cmds.html)
from Printer.phoenix_printer import PhoenixPrinter
from commands import PhoenixCommands
from Menu.util import find_port

def run_phoenix_positioning():
    ports = find_port()
    if not ports:
        print("No printer found.")
        return

    # Use the correct port index based on your setup. Here we use ports[1] as in previous samples.
    printer = PhoenixPrinter(ports[1].device)

    try:
        printer.send_command(PhoenixCommands.INIT)

        # Left (Default)
        # @see [Phoenix Justification Commands] (https://escpos.readthedocs.io/en/latest/layout.html#b61)
        printer.send_command(PhoenixCommands.SELECT_JUSTIFICATION + PhoenixCommands.LEFT)
        printer.send_command(b"Left Aligned Text\n")

        # Center
        printer.send_command(PhoenixCommands.SELECT_JUSTIFICATION + PhoenixCommands.CENTER)
        printer.send_command(b"Centered Text")
        printer.send_command(PhoenixCommands.LINE_FEED)

        # Right
        printer.send_command(PhoenixCommands.SELECT_JUSTIFICATION + PhoenixCommands.RIGHT)
        printer.send_command(b"Right Aligned Text")
        printer.send_command(PhoenixCommands.LINE_FEED)

        # Reset to Left
        printer.send_command(PhoenixCommands.SELECT_JUSTIFICATION + PhoenixCommands.LEFT)
        printer.send_command(b"New Line After Reset.")
        printer.send_command(b"No Line Feed / Next Line")
        printer.send_command(PhoenixCommands.LINE_FEED)

        # Final Cut
        printer.send_command(PhoenixCommands.FULL_CUT)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        printer.close()

if __name__ == "__main__":
    run_phoenix_positioning()