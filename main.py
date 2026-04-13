import serial.tools.list_ports as port_list
import phoenix_printer as phoenix

if __name__ == "__main__":
    ports = port_list.comports()
    if not ports:
        print("No serial ports found.")
        exit(1)

    device_port = ports[0].device
    with phoenix.PhoenixPrinter(device_port) as printer:
        status = printer.get_real_time_status(1)
        print(f"Phoenix Status (n=1): {status}")
        paper = printer.get_real_time_status(4)
        print(f"Paper Status (n=4): {paper}")