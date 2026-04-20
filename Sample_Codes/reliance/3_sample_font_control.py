## @brief Demonstrates font styling and orientation for Reliance printers.
#  @details Focuses on text rotation (90° and 180°), reverse printing, and style combinations.
#  @see Font Controlling Commands
from Menu.util import find_port
from Printer.reliance_printer import ReliancePrinter
from commands import RelianceCommands
import sys
import os

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def run_font_orientation_sample():
    ports = find_port()
    if not ports:
        print("No printer found.")
        return

    printer = ReliancePrinter(ports[0].device)

    try:
        # Initialize
        printer.send_command(RelianceCommands.INIT)

        # --- NORMAL ORIENTATION & STYLES ---
        printer.send_command(b"NORMAL ORIENTATION:\n")
        printer.send_command(b"Standard Text\n")

        # Bold (Emphasis)
        # @see [Reliance Emphasis Commands] (https://escpos.readthedocs.io/en/latest/font_cmds.html#emphasis-mode-1b-45-rel-phx)
        printer.send_command(RelianceCommands.EMPHASIS_MODE + b'\x01')
        printer.send_command(b"Bold Text\n")
        printer.send_command(RelianceCommands.EMPHASIS_MODE + b'\x00')

        # Underline
        # @see [Reliance Underline Commands] (https://escpos.readthedocs.io/en/latest/font_cmds.html#underline-mode-1b-2d-rel-phx)
        printer.send_command(RelianceCommands.UNDERLINE_MODE + b'\x01')
        printer.send_command(b"Underlined Text\n")
        printer.send_command(RelianceCommands.UNDERLINE_MODE + b'\x00')

        # --- 90 DEGREE ROTATION ---
        # @see [Reliance Rotation Commands](https://escpos.readthedocs.io/en/latest/font_cmds.html#rotation-1b-56-rel)
        printer.send_command(b"\nROTATION SAMPLES:\n")

        # Turn 90° Clockwise ON
        # @see [Reliance Rotate 90° Commands](https://escpos.readthedocs.io/en/latest/font_cmds.html#rotation-1b-56-rel)
        printer.send_command(RelianceCommands.ROTATE_90_DEGREES + b'\x01')
        printer.send_command(b"Rotated 90 Degrees\n")
        # Turn 90° Clockwise OFF
        printer.send_command(RelianceCommands.ROTATE_90_DEGREES + b'\x00')

        # --- UPSIDE DOWN MODE (180°) ---
        # @see [Reliance Upside Down Commands](https://escpos.readthedocs.io/en/latest/font_cmds.html#upside-down-mode-1b-7b-rel)
        printer.send_command(b"\nUPSIDE DOWN SAMPLE:\n")

        # Turn Upside Down ON (Effective at the start of a line)
        printer.send_command(RelianceCommands.UPSIDE_DOWN_MODE + b'\x01')
        printer.send_command(b"This is Upside Down\n")
        # Turn Upside Down OFF
        printer.send_command(RelianceCommands.UPSIDE_DOWN_MODE + b'\x00')

        # --- REVERSE PRINT (WHITE ON BLACK) ---
        # @see [Reliance Reverse Print Commands](https://escpos.readthedocs.io/en/latest/font_cmds.html#reverse-print-mode-1d-42-rel-phx)
        printer.send_command(b"\nREVERSE MODE:\n")
        printer.send_command(RelianceCommands.REVERSE_PRINT_MODE + b'\x01')
        printer.send_command(b"  WHITE ON BLACK  \n")
        printer.send_command(RelianceCommands.REVERSE_PRINT_MODE + b'\x00')

        # --- COMBINING SIZE & ROTATION ---
        printer.send_command(b"\nLARGE ROTATED:\n")
        # Double Width + Double Height
        printer.send_command(RelianceCommands.SELECT_CHAR_SIZE + b'\x11')
        printer.send_command(RelianceCommands.ROTATE_90_DEGREES + b'\x01')
        printer.send_command(b"BIG ROT\n")

        # Reset to Default
        printer.send_command(RelianceCommands.INIT)

        # Eject and Cut
        printer.send_command(b"\n\nFont Orientation Complete\n\n")
        printer.send_command(RelianceCommands.EJECTOR + b'\x05')

    except Exception as e:
        print(f"Font sample failed: {e}")
    finally:
        printer.close()


if __name__ == "__main__":
    run_font_orientation_sample()