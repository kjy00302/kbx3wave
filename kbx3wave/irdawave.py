import wave

FRAME_HIGH_16BIT = b'\x00\x80\xff\x7f'
FRAME_MIDDLE_16BIT = b'\x00\x00\x00\x00'
FRAME_LOW_16BIT = b'\xff\x7f\x00\x80'

def _write_bit(wf: wave.Wave_write, b: bool, invert=False):
    for _ in range(4):
        wf.writeframesraw(FRAME_LOW_16BIT if b ^ invert else FRAME_HIGH_16BIT)
    for _ in range(16):
        wf.writeframesraw(FRAME_HIGH_16BIT if invert else FRAME_LOW_16BIT)

def write_packet(wf: wave.Wave_write, packet: bytes, invert=False):
    for c in packet:
        _write_bit(wf, False, invert)
        for i in range(8):
            _write_bit(wf, bool(c & (1 << i)), invert)
        _write_bit(wf, True, invert)

def write_preamble(wf: wave.Wave_write, invert=False):
    for _ in range(9600): # 200ms preamble
        wf.writeframesraw(FRAME_HIGH_16BIT if invert else FRAME_LOW_16BIT)

def write_pause(wf: wave.Wave_write):
    for _ in range(4800): # 100ms blank
        wf.writeframesraw(FRAME_MIDDLE_16BIT)
