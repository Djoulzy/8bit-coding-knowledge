"""Compile shared seven-bit mask/pixel scanlines for the native byte blitter."""
from tools import dhgr


FAST_FLAMES = {36, 37, 72, 73}
EXTRA_SECTOR = 336  # after the three full-screen HGR maps
EXTRA_CAPACITY = 0x0800  # AUX $0C00..$13FF, outside BOTH AUX text pages


def compile_sprites(sprites, mode):
    bits = 1 if mode == 'mono' else 4
    rows, names, lines = {}, {}, []
    for s in sprites:
        width = (s['cell_width'] * bits + 6) // 7
        if not 0 < width <= 64:
            raise ValueError('Native sprite row exceeds MAIN $0280-$02FF scratch')
        if s.get('force_black') or s['id'] in FAST_FLAMES and any(
                status > 3 for row in s['tile_rows'] for status in row):
            raise ValueError('Unsupported native flame metadata')
        header = [s['cell_width'], s['height'], 2]
        header += [(s['cell_width'] * bits + p + 6) // 7 for p in range(7)]
        header += [2, 0, 0, width, 0, 0]
        lines += ['sprite_%d:' % s['id'], '    .byte ' + ','.join(map(str, header))]
        for row, color in zip(s.get('statuses', s.get('tile_rows')), s['colors']):
            mask = pixel = 0
            for x, status in enumerate(row):
                if 'tile_rows' in s:
                    m = 15 if status else 0
                    p = (dhgr.pattern(s.get('accent', 0)) if status == 3 else
                         dhgr.pattern(color) if status == 2 else 0)
                else:
                    m = dhgr.status_mask(status)
                    p = dhgr.status_pattern(status, dhgr.pattern(color))
                if bits == 1:
                    m, p = int(bool(m)), int(bool(p))
                # Transparent detail codes do not write even if their pattern
                # has bits set. Never allow a pixel to escape its opacity mask.
                mask |= m << (x * bits)
                pixel |= (p & m) << (x * bits)
            data = bytes(v for x in range(width) for v in
                         ((mask >> (7*x)) & 127, (pixel >> (7*x)) & 127))
            if data not in names:
                names[data] = 'native_row_%d' % len(names)
                rows[names[data]] = data
            lines += ['    .word ' + names[data]]
    extra_size = 0
    for name, data in rows.items():
        extra = mode == 'dhgr' and extra_size + len(data) <= EXTRA_CAPACITY
        if extra:
            extra_size += len(data)
        lines += ['.segment "%s"' % ('ASSETEXTRA' if extra else 'ASSETS'),
                  name + ':', '    .byte ' + ','.join('$%02X' % v for v in data)]
    lines += ['.segment "ASSETS"']
    return lines, {'format': 'shared native 7-bit mask/pixel rows; runtime horizontal shift',
                   'sprites': [s['id'] for s in sprites], 'unique_rows': len(rows),
                   'row_bytes': sum(map(len, rows.values())),
                   'extra_bytes': extra_size, 'extra_sector': EXTRA_SECTOR}
