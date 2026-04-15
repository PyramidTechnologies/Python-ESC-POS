import serial
import time

class BasePrinter:
    def __init__(self, port, baudrate):
        self.ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
        )

        time.sleep(1)
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def send_command(self, cmd: bytes):
        self.ser.write(cmd)

    def close(self):
        if hasattr(self, 'ser') and self.ser.is_open:
            self.ser.close()

    def read_response(self, timeout=1.0):
        self.ser.timeout = timeout
        response = self.ser.read_all()
        return response