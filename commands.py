class PhoenixCommands:
    INIT = b'\x1b\x40'
    PAPER_STATUS = b'\x1b\x76'
    RT_STATUS = b'\x1b\x04'
    TEST_COIN_IN = b'\x60'
    TEST_NOTE_IN = b'\x61'


class RelianceCommands:
    INIT = b'\x1b\x40'
    FULL_STATUS = b'\x10\x04\x20'
    CUT_FULL = b'\x1d\x56\x00'