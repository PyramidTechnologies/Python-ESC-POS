from py_esc_pos.printer import base_printer
from py_esc_pos.commands import PhoenixCommands
import time

## @class PhoenixPrinter
#  @brief Implementation for the Pyramid phoenix Thermal printer.
#  @details This class handles hardware-specific handshaking and status parsing.
#  @see [phoenix Status Documentation](https://escpos.readthedocs.io/en/latest/phoenix_status.html)
class PhoenixPrinter(base_printer.BasePrinter):
    def __init__(self, port):
        super().__init__(port, 9600)
        self.printer_type = "PhoenixPrinter"

        time.sleep(1)
        self.ser.reset_input_buffer()

    ## @brief Verifies the logic link between the printer and host.
    #  @details Sends a DLE EOT (Real Time Status) command to check if the printer is responsive and online.
    #  @return String description of connection status.
    #  @see [phoenix Real Time Status Documentation](https://escpos.readthedocs.io/en/latest/phoenix_status.html#p1004)
    #  @note A response of 0xAC typically indicates a hardware communication error such as incorrect parity or a wiring fault.
    def verify_logic_link(self):
        self.ser.reset_input_buffer()
        self.ser.write(PhoenixCommands.REAL_TIME_STATUS + PhoenixCommands.RT_PAPER)
        time.sleep(0.25)

        if self.ser.in_waiting > 0:
            res = self.ser.read(1)[0]

            if res == 0xAC:
                return "CONNECTED_BUT_MANGLED (Check Parity/Stop Bits and/or RJ45 Wiring)"

            is_online = (res & 0x08) == 0
            return "ONLINE" if is_online else "OFFLINE"

        return "NO_RESPONSE"
