#  @brief This sample demonstrates how to establish a link with the Phoenix printer.
from Printer.phoenix_printer import PhoenixPrinter
from Menu.util import find_port

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