import argparse
import wave
import ruifan_packet
import ruifan_wave

def color_normalization(rgb_tuple):
    r, g, b = rgb_tuple
    color_sum = sum(rgb_tuple)
    if color_sum > 255:
        return tuple(map(lambda x: round(x / color_sum * 255), rgb_tuple))
    return rgb_tuple

def colors_to_packets(colors, no_normalization=False):
    packets = []
    for n, color_set in enumerate(colors):
        *rgb, w, y = color_set
        if not no_normalization:
            rgb = color_normalization(rgb)
        packets.append(ruifan_packet.ruifan_memory_packet(n, rgb, w))
    packets.append(ruifan_packet.ruifan_eof1_packet(len(colors)))
    packets.append(ruifan_packet.ruifan_eof2_packet(len(colors)))
    return packets

def generate_wave(fname, packets, invert=False):
    wf: wave.Wave_write = wave.open(fname, 'w')
    wf.setframerate(48000)
    wf.setnchannels(2)
    wf.setsampwidth(2)

    ruifan_wave.ruifan_wave_pause(wf)
    ruifan_wave.ruifan_wave_preamble(wf, invert)

    for packet in packets:
        ruifan_packet.ruifan_encode(packet)
        ruifan_wave.ruifan_wave_encode_packet(wf, packet, invert)
        ruifan_wave.ruifan_wave_pause(wf)

    wf.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="\"UNTESTED\" Proof of concept Kingblade X10III tuning wavefile generator")
    parser.add_argument('colorfile', help="QR code data from official app")
    parser.add_argument('-o', '--output', help="Write wavefile to OUTPUT")
    parser.add_argument('--invert', action='store_true', help="Invert output signal")
    parser.add_argument('--no-normalization', action='store_true', help="Skip color normalization")
    args = parser.parse_args()

    colors = []
    name = ''

    try:
        with open(args.colorfile) as f:
            lc = 1
            if not f.readline().startswith('Copyright RUIFAN'):
                raise ValueError
            name = f.readline().strip()
            lc = 3
            for l in f.readlines():
                colors.append(bytes.fromhex(l.strip()))
                lc += 1
    except ValueError:
        print(f"{args.colorfile} is not a penlight color file")
        if lc > 2:
            print(f"Error found at line {lc}")
        exit(1)
    except OSError:
        print(f"Cannot open file {args.colorfile}")
        exit(1)

    generate_wave(f'{args.output if args.output else f"{name}.wav"}',
        colors_to_packets(colors, args.no_normalization), args.invert)
