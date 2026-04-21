#  @brief Demonstrates image and barcode generation for Phoenix printers.
#  @details Covers 2D Barcodes (QR Codes) and Raster Image printing.
#  @see [Images and Barcode Commands](https://escpos.readthedocs.io/en/latest/imaging.html)

from py_esc_pos.printer.phoenix_printer import PhoenixPrinter
from py_esc_pos.commands import PhoenixCommands
from py_esc_pos.menu.util import find_port, get_raster_blob

IMAGE_PATH = r"sample_image.png"  # Replace with your image path

def run_image_barcode_sample():
    ports = find_port()
    if not ports:
        print("No printer found.")
        return

    # Use the first detected port by default so the sample works when only one printer port is available.
    printer = PhoenixPrinter(ports[0].device)

    try:
        raster_blob = get_raster_blob(IMAGE_PATH)
        qr_data = "https://pyramidacceptors.com"
        # pL calculation: Data length (28) + 3 overhead bytes (cn, fn, m) = 31 (0x1F)
        pL = bytes([len(qr_data) + 3])
        pH = b"\x00"
        pL2 = b"\03"
        pH2 = b"\x00"

        # Store the data (Function 180)
        # cn=49 (0x31), fn=80 (0x50), m=48 (0x31)
        function180 = b"\x31\x50\x31"
        # Print the stored data (Function 181)
        # cn=49 (0x31), fn=81 (0x51), m=48 (0x31)
        function181 = b"\x31\x51\x31"

        # --- RASTER IMAGE SAMPLES ---
        # @see [Raster Image](https://escpos.readthedocs.io/en/latest/imaging.html#raster-image-1d-76-30-m-xl-xh-yl-yh-d1-dk-rel-phx)
        printer.send_command(b"PRINTING RASTER IMAGE:\n")
        printer.send_command(PhoenixCommands.LINE_FEED)
        printer.send_command(raster_blob)
        printer.send_command(PhoenixCommands.LINE_FEED)
        printer.send_command(b"Raster image printed successfully.\n")
        printer.send_command(PhoenixCommands.LINE_FEED)

        # --- 2D BARCODE (QR CODE) SAMPLES ---
        # @see [Dynamic 2D Barcode](https://escpos.readthedocs.io/en/latest/imaging.html#dynamic-2d-barcode-1d-28-6b-phx)
        printer.send_command(PhoenixCommands.INIT)
        printer.send_command(b"2D BARCODE (QR CODE):\n")

        # Send the commands to store and print the QR code
        printer.send_command(PhoenixCommands.DYNAMIC_2D_BARCODE)
        printer.send_command(pL + pH)
        printer.send_command(function180)
        printer.send_command(qr_data.encode('utf-8'))

        # The printer will print the stored QR code when it receives the print command.
        printer.send_command(PhoenixCommands.DYNAMIC_2D_BARCODE)
        printer.send_command(pL2 + pH2)
        printer.send_command(function181)
        printer.send_command(PhoenixCommands.LINE_FEED)
        printer.send_command(b"Complete QR code sample\n")
        printer.send_command(PhoenixCommands.LINE_FEED * 2)  # Feed some lines to clear the cutter
        printer.send_command(PhoenixCommands.FULL_CUT)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_image_barcode_sample()