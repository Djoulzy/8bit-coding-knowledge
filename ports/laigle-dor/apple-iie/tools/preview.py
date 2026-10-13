"""Independent pixel reference and PNG export; Python standard library only."""
import json
import struct
import zlib
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.common import ROOT, Source
from tools.resources import sprite, row_offset
from tools.video_layout import source_y, HGR_HEIGHT


def reference_page(x, y, frame):
    source = Source()
    frames = json.loads((ROOT / 'build/resources/frames.json').read_text())
    page = bytearray((ROOT / 'build/resources/room12.hgr').read_bytes())
    for sid, dx, dy in frames[frame]['layers']:
        s = sprite(source, sid)
        cx, cy = (x + dx) & 255, (y + dy) & 255
        if cx >= 40:
            continue
        left = 20 + (cx + 1) * 6
        for j, row in enumerate(s['pixels']):
            sy = (cy + j) & 255
            target_y = source_y(sy)
            if target_y is None:
                continue
            base = row_offset(target_y)
            for k, v in enumerate(row):
                if not s['masks'][j][k]:
                    continue
                tx = left + k
                if not 0 <= tx < 280:
                    continue
                address = base + tx // 7
                mask = 1 << (tx % 7)
                page[address] = (page[address] | mask) if v else (page[address] & (127 ^ mask))
    return bytes(page)


def pixels(page, text_rows=None):
    data = bytearray(255 if page[row_offset(y) + x // 7] & (1 << (x % 7)) else 0
                     for y in range(192) for x in range(280))
    if text_rows is not None:
        from tools.text_font import glyph
        data[HGR_HEIGHT * 280:] = bytes((192 - HGR_HEIGHT) * 280)
        for row, codes in enumerate(text_rows):
            for column, code in enumerate(codes):
                for y, bits in enumerate(glyph(chr(code & 127))):
                    for x in range(5):
                        if bits & (16 >> x):
                            data[(HGR_HEIGHT + row * 8 + y) * 280 + column * 7 + x + 1] = 255
    return bytes(data)


def png(page, text_rows=None):
    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data))
    data = pixels(page, text_rows)
    rows = b''.join(b'\0' + data[y * 280:(y + 1) * 280] for y in range(192))
    return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', 280, 192, 8, 0, 0, 0, 0)) + \
        chunk(b'IDAT', zlib.compress(rows)) + chunk(b'IEND', b'')
