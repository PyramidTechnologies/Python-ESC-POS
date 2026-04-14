## @class PhoenixCommands
class PhoenixCommands:
    INIT = b'\x1b\x40'
    RT_STATUS = b'\x10\x04'

    # RT Status Arguments (n)
    RT_PRINTER = b'\x01'
    RT_OFFLINE = b'\x02'
    RT_ERROR = b'\x03'
    RT_PAPER = b'\x04'

    # Actions
    TEST_COIN_IN = b'\x60'
    TEST_NOTE_IN = b'\x61'
    PRINT_RTC = b'\x1c\x7d\x70'

class RelianceCommands:
    INIT = b'\x1b\x40'
    FULL_STATUS = b'\x10\x04\x20'
    CUT_FULL = b'\x1d\x56\x00'