"""Standard DHGR serial packing: auxiliary seven bits, then main seven bits.

Palette numbers use the usual lores order. Serial patterns use a separate
mapping (including the two named gray patterns). Preview RGB is illustrative.
"""
# Preview palette/edge classification adapted from Apple2js canvas.ts,
# copyright (c) 2010-2021 Will Scullin and contributors, MIT license.
# See docs/apple2js-license.txt. This notice does not license historical assets.
import json
from pathlib import Path
from tools.video_layout import source_y

RGB = [(0, 0, 0), (227, 30, 96), (96, 78, 189), (255, 68, 253),
       (0, 163, 96), (156, 156, 156), (20, 207, 253), (208, 195, 255),
       (96, 114, 3), (255, 106, 60), (156, 156, 156), (255, 160, 208),
       (20, 245, 60), (208, 221, 141), (114, 255, 208), (255, 255, 255)]
ART_PALETTE = json.loads((Path(__file__).resolve().parents[1] /
                          'resources/dhgr-palette.json').read_text())
MATERIAL_COLORS = ART_PALETTE['colors']
SCENE_COLORS = {int(sid): MATERIAL_COLORS[material]
                for sid, material in ART_PALETTE['scene_materials'].items()}
SERIAL_TO_PALETTE = [0, 2, 4, 6, 8, 5, 12, 14, 1, 3, 10, 7, 9, 11, 13, 15]
PALETTE_TO_SERIAL = [SERIAL_TO_PALETTE.index(c) for c in range(16)]


def pattern(color):
    if not 0 <= color < 16:
        raise ValueError('DHGR color outside palette')
    return PALETTE_TO_SERIAL[color]


def palette(code):
    return SERIAL_TO_PALETTE[code]


def row_offset(y):
    return (y & 7) * 1024 + ((y >> 3) & 7) * 128 + (y >> 6) * 40


def put_cell(main, aux, x, y, color):
    put_pattern(main, aux, x, y, pattern(color))


def put_pattern(main, aux, x, y, code, opacity=15):
    if not 0 <= x < 140 or not 0 <= y < 192:
        raise ValueError('DHGR cell outside screen')
    for bit in range(4):
        if not opacity & (1 << bit):
            continue
        serial, shift = divmod(x * 4 + bit, 7)
        bank = main if serial & 1 else aux
        address = row_offset(y) + serial // 2
        mask = 1 << shift
        bank[address] = (bank[address] & (255 ^ mask)) | (((code >> bit) & 1) << shift)


def cells(main, aux, y):
    result = []
    for x in range(140):
        code = 0
        for bit in range(4):
            serial, shift = divmod(x * 4 + bit, 7)
            bank = main if serial & 1 else aux
            code |= ((bank[row_offset(y) + serial // 2] >> shift) & 1) << bit
        result.append(palette(code))
    return result


def serial_samples(main, aux, y):
    base = row_offset(y)
    return [((main if serial & 1 else aux)[base + serial // 2] >> bit) & 1
            for serial in range(80) for bit in range(7)]


def scanline_rgb(main, aux, y, monitor='color'):
    """Sample-aware digital preview, not a calibrated Virtual II/CRT emulator.

    Standard-DHGR edge classification follows the neighbor/white-run approach
    in Apple2js canvas.ts (pinned ee0aed25...). Pure palette mode is explicitly
    separate: it hides subcell luminance and is unsuitable for detail review.
    """
    codes = [pattern(c) for c in cells(main, aux, y)]
    if monitor == 'palette':
        return bytes(v for code in codes for _ in range(4) for v in RGB[palette(code)])
    dots = serial_samples(main, aux, y)
    if monitor == 'mono':
        return bytes(v for dot in dots for v in (255 * dot,) * 3)
    if monitor != 'color':
        raise ValueError('Unknown DHGR preview monitor')
    result = bytearray()
    for x in range(560):
        cell, bit = divmod(x, 4)
        code = codes[cell]
        before = codes[cell - 1] if cell else 0
        after = codes[cell + 1] if cell < 139 else 0
        window = (before | (code << 4) | (after << 8)) >> bit
        color = RGB[palette(code)]
        if code != before and code != after and any(
                window & mask == mask for mask in (0x1C, 0x70, 0x38)):
            color = RGB[15]
        elif window & 0x38 or code == before or code == after:
            pass
        elif window & 0x28:
            color = tuple(v // 2 for v in color)
        else:
            color = RGB[0]
        result.extend(color)
    return bytes(result)


def image_pages(image):
    main, aux = bytearray(8192), bytearray(8192)
    for y, row in enumerate(image):
        ty = source_y(y)
        if ty is None:
            continue
        # Same last-source-row viewport policy as the monochrome milestone.
        for x in range(0, len(row), 2):
            pair = row[x:x + 2]
            color = pair[0] or pair[1]
            # Static materials use complete, phase-aligned palette cells.
            # Retain enclosed dark marks instead of the old any(pair) fill:
            # a mixed pair bracketed by the same material becomes a dark cut.
            # This is explicit target art adaptation at 140 color columns.
            dark_cut = (bool(color) and not all(pair) and x > 0 and x + 2 < len(row)
                        and row[x - 1] == color and row[x + 2] == color)
            code = 0 if dark_cut else pattern(color)
            put_pattern(main, aux, 10 + x // 2, ty, code)
    return bytes(main), bytes(aux)


def target_sprite(s):
    statuses, colors, materials, policies = [], [], [], []
    for y, (row, mask) in enumerate(zip(s['pixels'], s['masks'])):
        material = s['target_materials'][y] if 'target_materials' in s else actor_material(s['id'], y)
        policy = ART_PALETTE.get('sprite_material_policies', {}).get(str(s['id']), {}).get(
            material, ART_PALETTE['actor_cell_policies'].get(material, 'fine'))
        if 'target_policies' in s: policy = s['target_policies'][y]
        codes = []
        for x in range(0, len(row), 2):
            code = (mask[x] | (row[x] << 1)) | ((mask[x + 1] | (row[x + 1] << 1)) << 2)
            if policy != 'fine':
                # Selected target art uses stable, complete palette cells.
                # Keep whole black pairs and (for legs) enclosed dark cuts;
                # round the opacity out to the existing four-sample footprint.
                pair = row[x:x + 2]
                cut = (policy == 'dark-cuts' and bool(any(pair)) and not all(pair)
                       and x > 0 and x + 2 < len(row) and row[x - 1] and row[x + 2])
                code = 15 if any(pair) and not cut else (5 if any(mask[x:x + 2]) else 0)
            elif code == 15:
                solid = (x > 0 and x + 2 < len(row) and row[x - 1] and row[x + 2]
                         and y > 0 and y + 1 < s['height']
                         and all(s['pixels'][y - 1][x:x + 2]) and all(s['pixels'][y + 1][x:x + 2]))
                if not solid:
                    code = 10  # legacy detail-edge marker; now uses the row material
            codes.append(code)
        for edit in ART_PALETTE.get('cell_overrides', {}).get(str(s['id']), []):
            if edit['row'] == y:
                if not 0 <= edit['cell'] < len(codes) or codes[edit['cell']] == 0:
                    raise ValueError('DHGR target-art edit outside occupied sprite')
                codes[edit['cell']] = edit['status']
        statuses.append(codes)
        colors.append(MATERIAL_COLORS[material])
        materials.append(material)
        policies.append(policy)
    return dict(s, statuses=statuses, colors=colors, materials=materials, cell_policies=policies,
                cell_width=s['width_bytes'] * 3,
                mask_policy='fine face/tunic/hands except retouched left profile; native-cell hair/legs; dark cuts')


def actor_material(sid, y):
    if sid in ART_PALETTE['lower_body_ids']:
        return 'boots' if y >= ART_PALETTE['boot_start_rows'][str(sid)] else 'trousers'
    bands = ART_PALETTE['actor_bands'].get(str(sid))
    if not bands:
        raise ValueError('Missing DHGR material map for atlas %d' % sid)
    material = bands[0][1]
    for start, name in bands:
        if y < start:
            break
        material = name
    return material


def actor_color(sid, y):
    return MATERIAL_COLORS[actor_material(sid, y)]


def colored_detail(detail, foreground):
    """Keep source holes; never erase a fine mark at an unfavorable color phase.

    A two-sample mark cannot express every palette hue. Its fallback retains
    the original bright mark rather than dropping it or filling its sibling.
    """
    return (detail & foreground) or detail


def status_mask(code):
    return 15 if code == 10 else ((3 if code & 1 else 0) | (12 if code & 4 else 0))


def status_pattern(code, foreground):
    if code in (10, 15):
        return foreground
    detail = (3 if code & 2 else 0) | (12 if code & 8 else 0)
    return colored_detail(detail, foreground)


def reference_layer(main, aux, s, x, y):
    if not 0 <= x < 40 or not 0 <= y < 200:
        return
    left = 10 + (x + 1) * 3
    for j, row in enumerate(s['statuses']):
        ty = source_y(y + j)
        if ty is None:
            continue
        for k, status in enumerate(row):
            if status_mask(status) and left + k < 140:
                put_pattern(main, aux, left + k, ty,
                            status_pattern(status, pattern(s['colors'][j])), status_mask(status))


def generate_include(dest, sprites, fs, compact_cells=False, graphics_rows=160, cell_bits=4, emit_sprites=True, skip_sprites=()):
    def emit(label, data):
        lines.append(label + ':')
        for pos in range(0, len(data), 16):
            lines.append('    .byte ' + ','.join('$%02X' % v for v in data[pos:pos + 16]))
    lines = ['; Generated DHGR resources; historical inputs are read-only.',
             'room12_rle: .incbin "room12.rle"',
             'room12_aux_rle: .incbin "room12-aux.rle"',
             'room12_grid: .incbin "room12-collision.bin"',
             'initial_world: .incbin "world-initial.bin"']
    emit('y_map', [source_y(y) if source_y(y) is not None else 255 for y in range(200)])
    emit('row_lo', [row_offset(y) & 255 for y in range(graphics_rows)])
    emit('row_hi', [0x20 + (row_offset(y) >> 8) for y in range(graphics_rows)])
    if cell_bits == 1:
        emit('actor_cell_x', [(x + 1) * 6 for x in range(40)])
        emit('x_byte', [(20 + (x + 1) * 6) // 7 for x in range(40)])
        emit('x_phase', [(20 + (x + 1) * 6) % 7 for x in range(40)])
        emit('cell_byte', [(20+x)//7 for x in range(240)])
        emit('cell_phase', [1 << ((20+x)%7) for x in range(240)])
    else:
        emit('actor_cell_x', [10 + (x + 1) * 3 for x in range(40)])
        emit('x_byte', [(40 + (x + 1) * 12) // 7 for x in range(40)])
        emit('x_phase', [(40 + (x + 1) * 12) % 7 for x in range(40)])
        emit('cell_byte', [x * 4 // 7 for x in range(140)])
        emit('cell_phase', [x * 4 % 7 * 16 for x in range(140)])
    emit('cell_mask_lo', [(15 << p) & 127 for p in range(7)])
    emit('cell_mask_hi', [15 >> (7 - p) if p else 0 for p in range(7)])
    emit('cell_color_lo', [((c << p) & 127) for p in range(7) for c in range(16)])
    emit('cell_color_hi', [c >> (7 - p) if p else 0 for p in range(7) for c in range(16)])
    emit('sprite_status_mask', [status_mask(code) for code in range(16)])
    emit('sprite_status_pattern', [status_pattern(code, 15) for code in range(16)])
    lookup = {s['id']: i for i, s in enumerate(sprites)}
    lines += ['sprite_lo: .byte ' + ','.join('<sprite_%d' % s['id'] for s in sprites),
              'sprite_hi: .byte ' + ','.join('>sprite_%d' % s['id'] for s in sprites),
              'frame_lo: .byte ' + ','.join('<frame_%d' % i for i in range(len(fs))),
              'frame_hi: .byte ' + ','.join('>frame_%d' % i for i in range(len(fs)))]
    for i, f in enumerate(fs):
        emit('frame_%d' % i, [len(f['layers'])] +
             [v for sid, dx, dy in f['layers'] for v in (lookup[sid], dx, dy)])
    for s in sprites if emit_sprites else []:
        if s['id'] in skip_sprites:
            continue
        w = s['cell_width']
        packed = compact_cells and {v for row in s['statuses'] for v in row} <= {0,5,10,15}
        group = 4 if packed else 2
        stride = 1 + (w + group - 1) // group
        data = [w, s['height'], stride] + [(w * cell_bits + p + 6) // 7 for p in range(7)] + [int(packed)] + [0]*5
        for row, color in zip(s['statuses'], s['colors']):
            data.append(pattern(color))
            codes = [{0:0,5:1,10:2,15:2}[v] for v in row] if packed else row
            data.extend(sum(v << (k * (2 if packed else 4)) for k, v in enumerate(codes[j:j + group]))
                        for j in range(0, w, group))
        emit('sprite_%d' % s['id'], data)
    (dest / 'generated.inc').write_text('\n'.join(lines) + '\n')
