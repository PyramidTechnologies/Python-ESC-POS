## @brief Demonstrates image and barcode generation for Reliance printers.
#  @details Covers 1D Barcodes, 2D Barcodes (QR Codes), and Raster Image printing.
#  @see [Images and Barcode Commands](https://escpos.readthedocs.io/en/latest/imaging.html#)

from py_esc_pos.menu.util import find_port, get_raster_blob
from py_esc_pos.printer.reliance_printer import ReliancePrinter
from py_esc_pos.commands import RelianceCommands

IMAGE_PATH = r"sample_image.png"  # Replace with your image path

def run_imaging_sample():
    ports = find_port()
    if not ports:
        print("No printer found.")
        return

    # Use the correct port index based on your setup.
    printer = ReliancePrinter(ports[0].device)

    try:
        # 2. Initialize
        print("Initializing printer...")
        printer.send_command(RelianceCommands.INIT)

        # --- 1D BARCODE SAMPLES ---
        # @see [Barcode Generator](https://escpos.readthedocs.io/en/latest/imaging.html#barcode-generator-1-1d-6b-m-d1-dk-00-rel)
        printer.send_command(b"1D BARCODE (CODE 39):\n")

        # Set Barcode Height to 100 dots and Width Multiplier to 2
        printer.send_command(RelianceCommands.SET_1D_BARCODE_HEIGHT + b'\x64')
        printer.send_command(RelianceCommands.SET_1D_BARCODE_WIDTH_MULT + b'\x02')

        # Set HRI (Human Readable Interpretation) to print below the barcode
        printer.send_command(RelianceCommands.SET_HRI_PRINTING_POSITION + b'\x02')

        # Print Code 39 Barcode (System m=4, ends with NULL)
        printer.send_command(RelianceCommands.BARCODE_GENERATOR + b'\x04' + b"RELIANCE123" + b'\x00')
        printer.send_command(b"\n\n")

        # --- 2D BARCODE (QR CODE) SAMPLES ---
        # @see [2D Barcode Generator](https://escpos.readthedocs.io/en/latest/imaging.html#d-barcode-generator-1c-7d-25-k-d1-dk-rel)
        printer.send_command(b"2D BARCODE (QR CODE):\n")

        # Set QR Code size (3 to 8 dots per cell)
        # @see [Set 2D Barcode Size](https://escpos.readthedocs.io/en/latest/imaging.html#set-2d-barcode-size-1c-7d-74-k-rel)
        printer.send_command(RelianceCommands.SET_2D_BARCODE_SIZE + b'\x06')

        # Command must be enclosed by Line Feeds
        qr_data = b"https://pyramidacceptors.com"
        qr_len = len(qr_data).to_bytes(1, 'little')

        printer.send_command(RelianceCommands.LINE_FEED)
        printer.send_command(RelianceCommands.BARCODE_GENERATOR_2D + qr_len + qr_data)
        printer.send_command(RelianceCommands.LINE_FEED)
        printer.send_command(b"\n")

        # --- RASTER IMAGE SAMPLES ---
        # @see [Raster Image](https://escpos.readthedocs.io/en/latest/imaging.html#raster-image-1d-76-30-m-xl-xh-yl-yh-d1-dk-rel-phx)
        printer.send_command(b"IMAGE FROM FILE:\n")
        try:
            # Generate the blob using the helper function
            image_blob = get_raster_blob(IMAGE_PATH, printer_width_pixels=384)
            printer.send_command(image_blob)
        except Exception as img_err:
            print(f"Image processing failed: {img_err}")
            printer.send_command(b"[Image Load Error]\n")

        # 3. Finalization
        # Reset to Default
        printer.send_command(RelianceCommands.INIT)

        # 4. Cut and Eject Paper
        printer.send_command(b"\n\nImaging Sample Complete\n\n")
        printer.send_command(RelianceCommands.EJECTOR + b'\x05')

    except Exception as e:
        print(f"Imaging command failed: {e}")
    finally:
        printer.close()

if __name__ == "__main__":
    run_imaging_sample()