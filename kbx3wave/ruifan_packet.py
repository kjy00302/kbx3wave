import random


MAGIC = b'&015$2#8)@_!(D^."'

def ruifan_encode(wave_data: bytearray, nonce: int = None):
    if nonce is None:
        nonce = random.randrange(256)
    for i in range(1, 12):
        wave_data[i] = wave_data[i] ^ nonce ^ MAGIC[i - 1 + nonce % 5]
    wave_data[12] = MAGIC[wave_data[1] & 0xf] ^ nonce
    swap_addr = wave_data[1] % 10 + 2
    wave_data[swap_addr], wave_data[12] = wave_data[12], wave_data[swap_addr]

def ruifan_decode(wave_data: bytearray):
    swap_addr = wave_data[1] % 10 + 2
    wave_data[swap_addr], wave_data[12] = wave_data[12], wave_data[swap_addr]
    nonce = wave_data[12] ^ MAGIC[wave_data[1] & 0xf]
    for i in range(1, 12):
        wave_data[i] = wave_data[i] ^ nonce ^ MAGIC[i - 1 + nonce % 5]

def ruifan_packet(cmd: int, data: bytes) -> bytearray:
    wave_data = bytearray(14)
    wave_data[0] = 0xaa
    wave_data[1] = cmd
    wave_data[2:2+len(data)] = data
    wave_data[13] = 0x55
    return wave_data

# memory: preamble, memory0, memory1, ... memoryN, eof1, eof2
def ruifan_memory_packet(cnt: int, rgb: tuple[int, int, int], w: int) -> bytearray:
    return ruifan_packet(0x80 + cnt, bytes([*rgb, w]))


# preview: preamble, previewpacket
def ruifan_preview_packet(rgb: tuple[int, int, int], w: int) -> bytearray:
    return ruifan_packet(0x41, bytes([*rgb, w]))

def ruifan_eof1_packet(cnt: int) -> bytearray:
    return ruifan_packet(0x9e, bytes([cnt]))

def ruifan_eof2_packet(cnt: int) -> bytearray:
    return ruifan_packet(0x9f, bytes([cnt]))
