from py_esc_pos.printer import base_printer
from py_esc_pos.commands import RelianceCommands
import time

class ReliancePrinter(base_printer.BasePrinter):
    def __init__(self, port):
        super().__init__(port, 9600)
        self.printer_type = "ReliancePrinter"

        time.sleep(1)
        self.ser.reset_input_buffer()

    def verify_logic_link(self):
        self.ser.reset_input_buffer()
        self.ser.write(RelianceCommands.REAL_TIME_STATUS + RelianceCommands.RT_OFFLINE)
        time.sleep(0.25)

        if self.ser.in_waiting > 0:
            res = self.ser.read(1)[0]
            if res == 0xAC:
                return "CONNECTED_BUT_MANGLED (Check Parity/Stop Bits)"

            is_online = (res & 0x08) == 0x08
            return "ONLINE" if is_online else "OFFLINE"
        return "NO_RESPONSE"