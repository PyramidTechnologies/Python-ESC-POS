from Printer import base_printer
import time

class ReliancePrinter(base_printer.BasePrinter):
    def __init__(self, port):
        super().__init__(port, 9600)
        self.ser.dtr = True
        self.ser.rts = True

        time.sleep(1)
        self.ser.reset_input_buffer()