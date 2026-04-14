import base_printer
import time
from commands import PhoenixCommands

## @class PhoenixPrinter
#  @brief Implementation for the Pyramid Phoenix Thermal Printer.
#  @details This class handles hardware-specific handshaking and status parsing.
#  @see [Phoenix Status Documentation](https://escpos.readthedocs.io/en/latest/phoenix_status.html)
class PhoenixPrinter(base_printer.BasePrinter):
    def __init__(self, port):
        super().__init__(port, 9600)
        self.ser.dtr = True
        self.ser.rts = True

        time.sleep(1)
        self.ser.reset_input_buffer()

    ## @brief Requests the Paper Roll Status (n=4).
    #  @return String description of paper state.
    def get_paper_status(self):
        self.ser.reset_input_buffer()
        self.ser.write(PhoenixCommands.RT_STATUS + PhoenixCommands.RT_PAPER)
        time.sleep(0.25)

        if self.ser.in_waiting > 0:
            res = self.ser.read(1)[0]

            if res == 0x72: return "Paper Empty"
            if res == 0x1E: return "Paper Low"
            if (res & 0x12) == 0x12: return "Paper OK"

            return f"Unknown Status: {hex(res)}"
        return "No Response"

    ## @brief Verifies the logic link between the printer and host.
    #  @return String description of connection status.
    def verify_logic_link(self):
        self.ser.reset_input_buffer()
        self.ser.write(PhoenixCommands.RT_STATUS + PhoenixCommands.RT_PAPER)
        time.sleep(0.25)

        if self.ser.in_waiting > 0:
            res = self.ser.read(1)[0]

            if res == 0xAC:
                return "CONNECTED_BUT_MANGLED (Check Parity/Stop Bits and/or RJ45 Wiring)"

            is_online = (res & 0x08) == 0
            return "ONLINE" if is_online else "OFFLINE"

        return "NO_RESPONSE"

    def print_rtc(self):
        self.send_command(b'\x1b\x40')

        self.send_command(b'\x1b\x54')
        self.send_command(b'PHOENIX' + b'\x0a')

        self.send_command(b'\x1b\x50')
        self.send_command(b'Standard Font A Test' + b'\x0a')

        self.send_command(b'\x1b\x45\x01')
        self.send_command(b'BOLD TEXT ENABLED' + b'\x0a')
        self.send_command(b'\x1b\x45\x00')

        self.send_command(b'\x0a\x0a\x0a')
        self.send_command(b'\x1b\x6d')
        time.sleep(0.25)

        if self.ser.in_waiting > 0:
            print (f"Data available, reading response... {self.ser.in_waiting} bytes")
            res = self.ser.read(self.ser.in_waiting)
            print(f"RTC Response: {res.hex().upper()}")

            return res.hex().upper()
        return "No Response"