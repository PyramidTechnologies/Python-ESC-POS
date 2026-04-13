import serial
import time

class BasePrinter:
    def __init__(self, port, baudrate, parity):
        self.ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=parity,
            stopbits=serial.STOPBITS_ONE,
            timeout=1.5,
            xonxoff=False,
            rtscts=False,
            dsrdtr=False
        )
        time.sleep(1)
        self.ser.reset_input_buffer()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def send_command(self, cmd: bytes):
        self.ser.write(cmd)

    def close(self):
        if hasattr(self, 'ser') and self.ser.is_open:
            self.ser.close()