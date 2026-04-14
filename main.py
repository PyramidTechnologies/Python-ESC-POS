import serial.tools.list_ports as port_list
import phoenix_printer as phoenix
import time

if __name__ == "__main__":
    ports = port_list.comports()
    if not ports:
        print("No serial ports found.")
        exit(1)

    device_port = ports[1].device

    with phoenix.PhoenixPrinter(device_port) as printer:
        print(f"Connection Logic Check: {printer.verify_logic_link()}")

        print(f"Paper Status: {printer.get_paper_status()}")