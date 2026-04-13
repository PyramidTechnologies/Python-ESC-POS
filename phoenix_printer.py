import base_printer
import serial
import commands
import time


def interpret_status(n, hex_val):
    if not hex_val: return "No Response"
    val = int(hex_val, 16)

    if n == 1:
        # Bit 3: Off=Online (00), On=Offline (08)
        return "Offline" if (val & 0x08) else "Online"

    if n == 4:
        # Per docs: 72 = Not present, 1E = Low
        if val == 0x72: return "Paper Not Present"
        if val == 0x1E: return "Paper Low"
        if val == 0x00 or val == 0x10: return "Paper OK"

    return f"Unknown ({hex_val})"


class PhoenixPrinter(base_printer.BasePrinter):
    def __init__(self, port):
        super().__init__(port, 9600, serial.PARITY_EVEN)

    def print_coin_test(self):
        self.send_command(commands.PhoenixCommands.TEST_COIN_IN)

    def get_real_time_status(self, n=1):
        self.ser.reset_input_buffer()
        self.ser.write(commands.PhoenixCommands.RT_STATUS + bytes([n]))
        time.sleep(0.25)

        if self.ser.in_waiting > 0:
            return interpret_status(n, self.ser.read(1).hex().upper())
        return None

