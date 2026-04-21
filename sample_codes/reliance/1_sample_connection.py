#  @brief This sample demonstrates how to establish a link with the Reliance printer.

from py_esc_pos.printer.reliance_printer import ReliancePrinter
from py_esc_pos.menu.util import find_port
## Connects to the first available printer and checks status.
#  @returns A ReliancePrinter instance if successful.
def simple_connect():
    ports = find_port()
    if ports:
        # Initialize printer on the first found port
        printer = ReliancePrinter(ports[0].device)

        # verify_logic_link is the 'handshake'
        status = printer.verify_logic_link()
        print(f"Printer Status: {status}")
        return printer

if __name__ == "__main__":
    simple_connect()