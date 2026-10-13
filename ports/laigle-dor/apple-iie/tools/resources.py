"""Deterministic, evidence-linked export and monochrome W05 conversion."""
import argparse
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.common import Source, ROOT, digest, write_json, B1_SHA, B2_SHA
from model.world import Room
from model.movement import room12_grid
from tools.video_layout import source_y, HGR_HEIGHT


def row_offset(y):
    if not 0 <= y < 192:
        raise ValueError('HGR y outside viewport')
    return (y & 7) * 1024 + ((y >> 3) & 7) * 128 + (y >> 6) * 40


def sprite(source, i):
    w, h = source.byte(0x9400 + i), source.byte(0x9500 + i)
    pointer = source.byte(0x9600 + i) + 256 * source.byte(0x9700 + i)
    if not w or not h or not 0x6523 <= pointer or pointer + w * h > 0x9400:
        raise ValueError('Invalid atlas descriptor: %d' % i)
    raw = source.read(pointer + 1, w * h)
    pixels, masks = [], []
    for y in range(h):
        row, graphic = [], []
        for v in raw[y * w:(y + 1) * w]:
            if v & 0x60:
                bits = (v & 63) ^ (63 if v & 128 else 0)
                row.extend(int(bool(bits & (32 >> x))) for x in range(6))
                graphic.extend([1] * 6)
            else:
                if (v & 31) >= 24:
                    raise ValueError('Text/mode control in selected atlas sprite')
                # Serial ink/paper cells have no Apple geometry or opacity.
                row.extend([0] * 6)
                graphic.extend([0] * 6)
        occupied = [x for x, value in enumerate(row) if value]
        mask = [int(bool(occupied) and occupied[0] <= x <= occupied[-1] and graphic[x])
                for x in range(w * 6)]
        pixels.append(row)
        masks.append(mask)
    return {'id': i, 'pointer': pointer, 'width_bytes': w, 'height': h,
            'source_start': pointer + 1, 'tap_offset': pointer + 1 + 0x3566,
            'sha256': digest(raw), 'pixels': pixels, 'masks': masks,
            'mask_policy': 'native monochrome row-span silhouette; attribute cells transparent; ink ignored'}


def motion(source, i, count=1):
    pointer = source.word(0x4200 + 2 * i)
    cursor = 1  # historical pre-increment / skipped prefix
    frames = []
    for _ in range(count):
        records, delta = [], [0, 0]
        for command in range(64):
            v = source.byte(pointer + cursor)
            cursor += 1
            if v >= 128:
                continue  # full-room redraw replaces source restore slots
            if v == 0:
                delta = list(source.read(pointer + cursor, 2)); cursor += 2
            elif v in [20, 22]:
                frames.append({'layers': records, 'delta': delta, 'event': v,
                               'pointer': pointer, 'cursor': cursor - 1})
                break
            elif v in [21, 23]:
                raise ValueError('Delay/chain outside selected W06 motion subset')
            else:
                dx, dy, sid = source.read(pointer + cursor, 3); cursor += 3
                records.append([sid, dx, dy])
        else:
            raise ValueError('No bounded yield in motion %d' % i)
    return frames


def frames(source):
    result = []
    for i in range(8):
        result.append(motion(source, i)[0])
    for i in range(8, 12):
        result.extend(motion(source, i, 2))
    for index, frame in enumerate(result):
        facing = index % 4 if index < 8 else (index - 8) // 2
        p = source.word(0x4400 + facing * 2)
        cursor = 1
        for _ in range(16):
            cmd = source.byte(p + cursor); cursor += 1
            if cmd == 20:
                break
            dx, dy, sid = source.read(p + cursor, 3); cursor += 3
            if 4 <= index < 8:
                dy = (dy + 10) & 255
            frame['layers'].append([sid, dx, dy])
        else:
            raise ValueError('Unbounded equipment stream')
        frame['source_motion'] = index if index < 8 else 8 + (index - 8) // 2
    return result


def mono_room12(source, variation):
    """Translate B2 100/300/390/600–699 for the checked room-12 fields."""
    room = Room.decode(source.read(0x5600, 512), 12)
    if (room.geometry, room.light, room.furnishing, room.treasure, room.features,
            room.fields[:4]) != (1, 3, 2, 0, (0, 0, 0, 0), (1, 0, 3, 0)):
        raise ValueError('Unexpected room 12; translator requires review')
    image = [[0] * 240 for _ in range(200)]
    operations = []

    def line(x0, y0, x1, y1, evidence):
        operations.append(['line', x0, y0, x1, y1, evidence])
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx, sy, err = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1), dx + dy
        while True:
            if 0 <= x0 < 240 and 0 <= y0 < 200:
                image[y0][x0] = 1
            if x0 == x1 and y0 == y1:
                break
            e = 2 * err
            if e >= dy:
                err += dy; x0 += sx
            if e <= dx:
                err += dx; y0 += sy

    def stamp(i, x, y, additive, evidence):
        s = sprite(source, i)
        # $3EBD uses the ROM cursor byte; $3E52 copies offsets width..1.
        left = (x // 6 + 1) * 6
        operations.append(['sprite', i, left, y, 'or' if additive else 'opaque', evidence])
        for j, row in enumerate(s['pixels']):
            for k, value in enumerate(row):
                if 0 <= y + j < 200 and 0 <= left + k < 240:
                    if additive:
                        image[y + j][left + k] |= value
                    elif s['masks'][j][k]:
                        image[y + j][left + k] = value

    line(12, 199, 60, 119, 'B2 100/390')
    line(60, 119, 191, 119, 'B2 390')
    line(191, 119, 239, 199, 'B2 390')
    stamp(5, 99, 49, False, 'B2 395')
    for y in [102, 85, 68, 51, 34, 17]:
        stamp(4, 48, y, True, 'B2 304/310')
    for y in [101, 83, 65, 47, 29, 11]:
        stamp(3, 179, y, True, 'B2 315')
    stamp(8, 105, 59, True, 'B2 325/330; V=$0482=1')
    stamp(7, 204, 105, False, 'B2 130/135; V=$0484=3')
    stamp(21, 80 if variation > 128 else 147, 36 if variation > 128 else 45,
          False, 'B2 720/722/725; M=ROM[$D00C]')
    stamp(14, 18, 80, False, 'B2 780/782')
    stamp(15, 214, 80, False, 'B2 780/782')
    image[:35] = [[0] * 240 for _ in range(35)]  # B2 690: clear upper band
    operations.append(['clear_top', 35, 'B2 690; paper hue intentionally omitted'])
    return image, operations, room


def hgr_image(image):
    """Crop only room 12's cleared header; resample remaining 165 into 160 rows."""
    page = bytearray(8192)
    for y, row in enumerate(image):
        target_y = source_y(y)
        if target_y is None:
            continue
        offset = row_offset(target_y)
        page[offset:offset + 40] = bytes(40)
        for x, value in enumerate(row):
            if value:
                tx = x + 20
                page[row_offset(target_y) + tx // 7] |= 1 << (tx % 7)
    return bytes(page)


def rle(data):
    result = bytearray()
    start = 0
    while start < len(data):
        end = start + 1
        while end < len(data) and data[end] == data[start] and end - start < 255:
            end += 1
        result.extend([end - start, data[start]])
        start = end
    result.append(0)
    return bytes(result)


def export(oric_rom=None):
    source = Source()
    dest = ROOT / 'build/resources'
    dest.mkdir(parents=True, exist_ok=True)
    exported = []

    def save(name, data, address=None, block=2, **metadata):
        (dest / name).write_bytes(data)
        record = {'file': name, 'length': len(data), 'sha256': digest(data), **metadata}
        if address is not None:
            record.update(source_block=block, cpu_start=address,
                          tap_offset=(address + 0x3566 if block == 2 else address - 0x501 + 24))
        exported.append(record)

    rom_record = {'status': 'missing', 'provisional_table': '64 zero bytes',
                  'consumer': 'B2 607; room-12 M=$D00C; B2 720/722'}
    variation = bytes(64)
    if oric_rom:
        rom = Path(oric_rom).read_bytes()
        if len(rom) != 16384:
            raise ValueError('Expected 16 KiB Oric ROM mapped at $C000–$FFFF')
        variation = rom[0x1000:0x1040]
        rom_record = {'status': 'supplied_not_runtime_verified', 'sha256': digest(rom),
                      'mapping': '$C000–$FFFF', 'capture': '$D000–$D03F'}
    save('room-variation.bin', variation, provisional=not bool(oric_rom))
    save('world-initial.bin', source.read(0x5600, 512), 0x5600)
    save('title-oric.bin', source.read(0x1801, 8000, 1), 0x1801, block=1)
    save('font-captured.bin', source.read(0x9800, 2048), 0x9800,
         limitation='Captured font, not the final ROM-adjusted runtime glyph state')
    for name, start, length in [('descriptions', 0x5A00, 204), ('scroll1', 0x5ACC, 50),
                                 ('scroll2', 0x5C31, 57), ('scroll3', 0x5B37, 65),
                                 ('book', 0x5B78, 68), ('victory', 0x5B11, 34)]:
        data = source.read(start, length)
        if name != 'descriptions' and data[-1] != 92:
            raise ValueError('Missing message sentinel: ' + name)
        save(name + '.bin', data, start)
    save('motion-pointer-table.bin', source.read(0x4200, 256), 0x4200,
         limitation='Raw table; unused entries are not validated motion pointers')
    save('equipment-pointer-table.bin', source.read(0x4400, 52), 0x4400)
    fs = frames(source)
    used = sorted({r[0] for f in fs for r in f['layers']})
    sprites = [sprite(source, i) for i in used]
    for s in sprites:
        raw = source.read(s['source_start'], s['width_bytes'] * s['height'])
        save('sprite-%03d-oric.bin' % s['id'], raw, s['source_start'], sprite_id=s['id'])
    image, operations, room = mono_room12(source, variation[12])
    page = hgr_image(image)
    save('room12.hgr', page, conversion='native monochrome masks; x+20; cleared header cropped; 165->160 last-row')
    save('room12.rle', rle(page))
    save('room12-collision.bin', room12_grid(room), evidence='B2 600/605; no M-dependent features in room 12')
    save('room12-source.pbm', b'P1\n240 200\n' + '\n'.join(' '.join(map(str, row)) for row in image).encode() + b'\n',
         limitation='Translated image, not an Oric runtime capture')
    write_json(dest / 'frames.json', fs)
    write_json(dest / 'room12-operations.json', operations)
    write_json(dest / 'rooms.json', [Room.decode(source.read(0x5600, 512), i).__dict__ for i in range(64)])
    generate_include(dest, sprites, fs, room)
    write_json(dest / 'manifest.json', {'source_payloads': {'B1': B1_SHA, 'B2': B2_SHA},
                                       'oric_rom': rom_record, 'room12': room.__dict__,
                                       'exports': exported, 'frames': fs,
                                       'video': {'mode': 'mixed HGR', 'graphic_rows': HGR_HEIGHT,
                                                 'text_rows': 4, 'page_strategy': 'alternating frames',
                                                 'baseline': '$A000', 'attribute_policy': 'discarded; transparent cells'},
                                       'sprites': [{k: v for k, v in s.items() if k not in ['pixels', 'masks']} for s in sprites]})
    return dest


def generate_include(dest, sprites, fs, room):
    lines = ['; Generated by tools/resources.py; historical input is read-only.']

    def emit(label, data):
        lines.append(label + ':')
        for pos in range(0, len(data), 16):
            lines.append('    .byte ' + ','.join('$%02X' % v for v in data[pos:pos + 16]))

    lines += ['room12_rle: .incbin "room12.rle"',
              'room12_grid: .incbin "room12-collision.bin"',
              'initial_world: .incbin "world-initial.bin"']
    emit('y_map', [source_y(y) if source_y(y) is not None else 255 for y in range(200)])
    emit('row_lo', [(0x2000 + row_offset(y)) & 255 for y in range(HGR_HEIGHT)])
    emit('row_hi', [(0x2000 + row_offset(y)) >> 8 for y in range(HGR_HEIGHT)])
    emit('x_byte', [(20 + (x + 1) * 6) // 7 for x in range(40)])
    emit('x_phase', [(20 + (x + 1) * 6) % 7 for x in range(40)])
    lines += ['.align 256', 'shift_table:']
    for phase in range(7):
        emit('shift_%d' % phase, [((v << phase) & 127) for v in range(128)] +
             [v >> (7 - phase) if phase else 0 for v in range(128)])
    lookup = {s['id']: i for i, s in enumerate(sprites)}
    lines += ['sprite_lo: .byte ' + ','.join('<sprite_%d' % s['id'] for s in sprites),
              'sprite_hi: .byte ' + ','.join('>sprite_%d' % s['id'] for s in sprites),
              'frame_lo: .byte ' + ','.join('<frame_%d' % i for i in range(len(fs))),
              'frame_hi: .byte ' + ','.join('>frame_%d' % i for i in range(len(fs)))]
    for index, frame in enumerate(fs):
        emit('frame_%d' % index, [len(frame['layers'])] +
             [v for sid, dx, dy in frame['layers'] for v in [lookup[sid], dx, dy]])
    for s in sprites:
        width = s['width_bytes'] * 6
        cw = (width + 6) // 7
        output_widths = [(width + p + 6) // 7 for p in range(7)]
        end_masks = [(1 << ((width + p) % 7)) - 1 if (width + p) % 7 else 127 for p in range(7)]
        packed = []
        for row, mask in zip(s['pixels'], s['masks']):
            for j in range(0, width, 7):
                packed += [sum(v << k for k, v in enumerate(row[j:j + 7])),
                           sum(v << k for k, v in enumerate(mask[j:j + 7]))]
        emit('sprite_%d' % s['id'], [cw, s['height']] + output_widths + end_masks + packed)
    (dest / 'generated.inc').write_text('\n'.join(lines) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--oric-rom', help='Local 16 KiB reference ROM; not redistributed')
    export(parser.parse_args().oric_rom)
