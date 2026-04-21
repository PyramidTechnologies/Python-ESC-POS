#  @brief This sample demonstrates how to establish a link with the Phoenix printer.

from py_esc_pos.printer.phoenix_printer import PhoenixPrinter
from py_esc_pos.menu.util import find_port

## Connects to the first available printer and checks status.
#  @returns A PhoenixPrinter instance if successful.
def simple_connect():
    ports = find_port()
    if ports:
        # Initialize printer on the first found port
        printer = PhoenixPrinter(ports[0].device)

        # verify_logic_link is the 'handshake'
        status = printer.verify_logic_link()
        print(f"Printer Status: {status}")
        return printer

if __name__ == "__main__":
    simple_connect()