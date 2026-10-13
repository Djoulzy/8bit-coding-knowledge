"""35-track, 16-sector DOS-order images and independent standard 6-and-2 encoding.

Reference: Apple Disk II BOOT0 and apple2js format_utils.ts (physical->DOS map).
No DOS filesystem/OS is embedded. Sector payloads are private to this loader.
"""
PHYSICAL_TO_DOS = [0, 7, 14, 6, 13, 5, 12, 4, 11, 3, 10, 2, 9, 1, 8, 15]
GCR = bytes([0x96,0x97,0x9A,0x9B,0x9D,0x9E,0x9F,0xA6,
             0xA7,0xAB,0xAC,0xAD,0xAE,0xAF,0xB2,0xB3,
             0xB4,0xB5,0xB6,0xB7,0xB9,0xBA,0xBB,0xBC,
             0xBD,0xBE,0xBF,0xCB,0xCD,0xCE,0xCF,0xD3,
             0xD6,0xD7,0xD9,0xDA,0xDB,0xDC,0xDD,0xDE,
             0xDF,0xE5,0xE6,0xE7,0xE9,0xEA,0xEB,0xEC,
             0xED,0xEE,0xEF,0xF2,0xF3,0xF4,0xF5,0xF6,
             0xF7,0xF9,0xFA,0xFB,0xFC,0xFD,0xFE,0xFF])


def offset(track, sector):
    if not 0 <= track < 35 or not 0 <= sector < 16:
        raise ValueError('Disk address outside 35x16 geometry')
    return (track * 16 + PHYSICAL_TO_DOS[sector]) * 256


def make_disk(boot, program):
    if len(boot) != 256 or boot[0] != 1 or not program or len(program) > 0x6000:
        raise ValueError('Invalid boot or application size')
    disk = bytearray(35 * 16 * 256)
    disk[:256] = boot
    for index, start in enumerate(range(0, len(program), 256), 1):
        track, sector = divmod(index, 16)
        a = offset(track, sector)
        block = program[start:start + 256]
        disk[a:a + 256] = block.ljust(256, b'\0')
    return bytes(disk)


def four_four(v):
    return bytes([(v >> 1) | 0xAA, v | 0xAA])


def encode_sector(data, track, sector, volume=254):
    if len(data) != 256:
        raise ValueError('Sector must contain 256 bytes')
    def swapped(v):
        return ((v & 1) << 1) | ((v >> 1) & 1)
    low = [swapped(data[i]) | (swapped(data[(i + 86) % 256]) << 2) |
           (swapped(data[(i + 172) % 256]) << 4) for i in range(86)]
    values = low + [v >> 2 for v in data]
    encoded = bytearray()
    previous = 0
    for value in values:
        encoded.append(GCR[previous ^ value])
        previous = value
    encoded.append(GCR[previous])
    header = b'\xD5\xAA\x96' + b''.join(four_four(v) for v in
                 [volume, track, sector, volume ^ track ^ sector]) + b'\xDE\xAA\xEB'
    return b'\xFF' * 40 + header + b'\xFF' * 8 + b'\xD5\xAA\xAD' + encoded + b'\xDE\xAA\xEB'


def nibble_tracks(disk):
    if len(disk) != 143360:
        raise ValueError('Expected DOS-order 140 KiB image')
    tracks = []
    for t in range(35):
        track = b''.join(encode_sector(disk[offset(t, s):offset(t, s) + 256], t, s)
                         for s in range(16))
        if len(track) > 6656:
            raise ValueError('Nibble track overflow')
        tracks.append(track.ljust(6656, b'\xFF'))
    return tracks
