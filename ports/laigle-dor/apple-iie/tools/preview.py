"""Independent pixel reference and PNG export; Python standard library only."""
import json
import struct
import zlib
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.common import ROOT, Source, build_dir, video_mode
from tools.resources import sprite, row_offset
from tools.hgr_color import target_sprite, scanline_rgb
from tools import dhgr
from tools.video_layout import source_y, HGR_HEIGHT


def reference_page(x, y, frame):
    source = Source()
    frames = json.loads((build_dir() / 'resources/frames.json').read_text())
    page = bytearray((build_dir() / 'resources/room12.hgr').read_bytes())
    if video_mode() == 'dhgr':
        aux = bytearray((build_dir() / 'resources/room12-aux.hgr').read_bytes())
        for sid, dx, dy in frames[frame]['layers']:
            dhgr.reference_layer(page, aux, dhgr.target_sprite(sprite(source, sid)),
                                 (x + dx) & 255, (y + dy) & 255)
        return bytes(page), bytes(aux)
    for sid, dx, dy in frames[frame]['layers']:
        s = target_sprite(sprite(source, sid), video_mode())
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
                page[address] = (page[address] | mask) if v else (page[address] & (255 ^ mask))
                if video_mode() == 'color':
                    page[address] = (page[address] & 127) | s['color_phase']
    return bytes(page)


def pixels(page, text_rows=None, alternate=False):
    data = bytearray(255 if page[row_offset(y) + x // 7] & (1 << (x % 7)) else 0
                     for y in range(192) for x in range(280))
    if text_rows is not None:
        from tools.text_font import text_cell
        data[HGR_HEIGHT * 280:] = bytes((192 - HGR_HEIGHT) * 280)
        for row, codes in enumerate(text_rows):
            for column, code in enumerate(codes):
                for y, cell in enumerate(text_cell(code, alternate)):
                    pos=(HGR_HEIGHT+row*8+y)*280+column*7
                    data[pos:pos+7]=cell
    return bytes(data)


def png(page, text_rows=None, video=None, monitor='color', alternate=False):
    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data))
    mode = video or video_mode()
    if mode == 'dhgr':
        main, aux = page
        height = HGR_HEIGHT if text_rows is not None else 192
        data = bytearray(b''.join(dhgr.scanline_rgb(main, aux, y, monitor) for y in range(height)))
        data.extend(bytes((192 - height) * 560 * 3))
        if text_rows is not None:
            from tools.text_font import text_cell
            for row, codes in enumerate(text_rows):
                for column, code in enumerate(codes):
                    for y, cell in enumerate(text_cell(code, alternate)):
                        pos=((160+row*8+y)*560+column*7)*3
                        data[pos:pos+21]=bytes(v for intensity in cell for v in (intensity,)*3)
        # Double scanlines preserve screen aspect: four sample dots per color,
        # two preview scanlines per native scanline; native mode remains 140x160.
        stride = 560 * 3
        rows = b''.join((b'\0' + data[y * stride:(y + 1) * stride]) * 2 for y in range(192))
        return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', 560, 384, 8, 2, 0, 0, 0)) + \
            chunk(b'IDAT', zlib.compress(rows)) + chunk(b'IEND', b'')
    color = mode == 'color'
    if color:
        graphics_height = HGR_HEIGHT if text_rows is not None else 192
        data = b''.join(scanline_rgb(page[row_offset(y):row_offset(y) + 40]) for y in range(graphics_height))
        if text_rows is not None:
            mono = pixels(bytes(8192), text_rows, alternate)[HGR_HEIGHT * 280:]
            data += bytes(v for intensity in mono for v in (intensity,) * 3)
    else:
        data = pixels(page, text_rows, alternate)
    stride = 280 * (3 if color else 1)
    rows = b''.join(b'\0' + data[y * stride:(y + 1) * stride] for y in range(192))
    return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', 280, 192, 8, 2 if color else 0, 0, 0, 0)) + \
        chunk(b'IDAT', zlib.compress(rows)) + chunk(b'IEND', b'')


def text_png(rows, alternate=False):
    """Functional text-font preview; the real emulator uses the Apple charset."""
    from tools.text_font import text_cell
    columns=len(rows[0]);width=columns*7;data=bytearray(width*192)
    for row,codes in enumerate(rows):
        for column,code in enumerate(codes):
            for y,cell in enumerate(text_cell(code, alternate)):
                pos=(row*8+y)*width+column*7
                data[pos:pos+7]=cell
    def chunk(kind,data):
        return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data))
    raster=b''.join(b'\0'+data[y*width:(y+1)*width] for y in range(192))
    return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',width,192,8,0,0,0,0))+chunk(b'IDAT',zlib.compress(raster))+chunk(b'IEND',b'')
