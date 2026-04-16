from PIL import Image, ImageOps
import serial.tools.list_ports as port_list

from commands import PhoenixCommands

def find_port():
    return list(port_list.comports())

def get_raster_blob(image_path, printer_width_pixels=384):
    img = Image.open(image_path).convert('1')

    img = ImageOps.invert(img.convert('L')).convert('1')

    w_percent = (printer_width_pixels / float(img.size[0]))
    h_size = int((float(img.size[1]) * float(w_percent)))
    img = img.resize((printer_width_pixels, h_size), Image.NEAREST)

    width_in_bytes = printer_width_pixels // 8

    xL, xH = width_in_bytes % 256, width_in_bytes // 256
    yL, yH = h_size % 256, h_size // 256

    header = PhoenixCommands.RASTER_IMAGE + b'\x00' + bytes([xL, xH, yL, yH])

    return header + img.tobytes()

def verify_printer_connection(printer):
    status = printer.verify_logic_link()
    if "ONLINE" in status:
        return True
    else:
        return False