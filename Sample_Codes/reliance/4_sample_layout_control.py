## @brief Demonstrates layout and positioning for Reliance printers.
#  @details Focuses on Justification, Line Spacing, Margins, and Character Spacing.
#  Reliance printers support advanced layout control via motion units.
#  @see [Layout Commands](https://escpos.readthedocs.io/en/latest/layout.html)
from Menu.util import find_port
from Printer.reliance_printer import ReliancePrinter
from commands import RelianceCommands

def run_layout_sample():
    ports = find_port()
    if not ports:
        print("No printer found.")
        return

    printer = ReliancePrinter(ports[0].device)

    try:
        # Initialize
        printer.send_command(RelianceCommands.INIT)

        # --- JUSTIFICATION SAMPLES ---
        # @see [Reliance Justification Commands](https://escpos.readthedocs.io/en/latest/layout.html#select-justification-1b-61-rel-phx)
        printer.send_command(b"JUSTIFICATION:\n")

        # Left (Default)
        printer.send_command(RelianceCommands.SELECT_JUSTIFICATION + RelianceCommands.LEFT)
        printer.send_command(b"This is Left Aligned\n")

        # Center
        printer.send_command(RelianceCommands.SELECT_JUSTIFICATION + RelianceCommands.CENTER)
        printer.send_command(b"This is Centered\n")

        # Right
        printer.send_command(RelianceCommands.SELECT_JUSTIFICATION + RelianceCommands.RIGHT)
        printer.send_command(b"This is Right Aligned\n\n")

        # Reset to Left for further tests
        printer.send_command(RelianceCommands.SELECT_JUSTIFICATION + RelianceCommands.LEFT)

        # --- LINE SPACING SAMPLES ---
        printer.send_command(b"LINE SPACING:\n")

        # Tight Spacing (1/8 inch)
        # @see [Reliance Line Spacing Commands](https://escpos.readthedocs.io/en/latest/layout.html#select-1-8-inch-line-spacing-1b-30-rel)
        printer.send_command(RelianceCommands.SELECT_1_8_INCH_LINE_SPACING)
        printer.send_command(b"Line 1: 1/8 inch spacing\n")
        printer.send_command(b"Line 2: 1/8 inch spacing\n")

        # Standard Spacing (1/6 inch)
        # @see [Reliance Line Spacing Commands](https://escpos.readthedocs.io/en/latest/layout.html#select-1-6-inch-line-spacing-1b-32-rel)
        printer.send_command(RelianceCommands.SELECT_1_6_INCH_LINE_SPACING)
        printer.send_command(b"Line 3: 1/6 inch spacing\n")

        # Custom Large Spacing (ESC 3 n) - Let's set n=100
        # @see [Reliance Line Spacing Commands](https://escpos.readthedocs.io/en/latest/layout.html#line-spacing-1b-33-rel)
        printer.send_command(RelianceCommands.LINE_SPACING + b'\x64')
        printer.send_command(b"Line 4: Custom Large Spacing\n")

        # Back to default
        printer.send_command(RelianceCommands.SELECT_1_6_INCH_LINE_SPACING)
        printer.send_command(b"\n")

        # --- MARGINS & CHARACTER SPACING ---
        printer.send_command(b"MARGINS & SPACING:\n")

        # Right Side Character Spacing (ESC SP n) - Adds space between characters
        # Setting n=4
        # @see [Reliance Character Spacing Commands](https://escpos.readthedocs.io/en/latest/layout.html#right-side-character-spacing-1b-20-rel)
        printer.send_command(RelianceCommands.RIGHT_SIDE_CHAR_SPACING + b'\x04')
        printer.send_command(b"Widened Character Spacing\n")
        printer.send_command(RelianceCommands.RIGHT_SIDE_CHAR_SPACING + b'\x00')  # Reset

        # Left Margin (GS L nL nH)
        # To set a ~1-inch margin (depending on motion units), we use nL=80, nH=0
        # @see [Reliance Left Margin Commands](https://escpos.readthedocs.io/en/latest/layout.html#left-margin-1d-4c-rel)
        printer.send_command(RelianceCommands.LEFT_MARGIN + b'\x50\x00')
        printer.send_command(b"This text has a left margin.\n")

        # Reset to Default
        printer.send_command(RelianceCommands.INIT)

        # Eject and Cut
        printer.send_command(b"\n\nLayout Sample Complete\n\n")
        printer.send_command(RelianceCommands.EJECTOR + b'\x05')

    except Exception as e:
        print(f"Layout command failed: {e}")
    finally:
        printer.close()

if __name__ == "__main__":
    run_layout_sample()