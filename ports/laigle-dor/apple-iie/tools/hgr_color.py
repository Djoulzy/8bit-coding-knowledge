"""Experimental standard HGR artwork policy, independent of game rules.

Color is encoded in real HGR bits. RGB values below are a development display
palette, not a calibrated composite monitor measurement.
"""
BLACK, VIOLET, GREEN, WHITE, ORANGE, BLUE = 0, 1, 2, 3, 5, 6
RGB = {
    BLACK: (0, 0, 0), VIOLET: (255, 68, 253), GREEN: (20, 245, 60),
    WHITE: (255, 255, 255), ORANGE: (255, 106, 60), BLUE: (20, 207, 253),
}
BITS = {BLACK: (0, 0), VIOLET: (1, 0), GREEN: (0, 1),
        WHITE: (1, 1), ORANGE: (0, 1), BLUE: (1, 0)}

# New port palette choices, never inferred from historical ink values.
SCENE_COLORS = {3: BLUE, 4: BLUE, 5: GREEN, 7: ORANGE, 8: VIOLET,
                14: ORANGE, 15: ORANGE, 21: GREEN}


def actor_color(sid):
    return BLUE if 46 <= sid <= 61 else ORANGE


def phase_bit(color):
    return 0x80 if color in (ORANGE, BLUE) else 0


def target_sprite(s, mode):
    """Pair-aligned colored silhouette; six-dot source anchors are always even."""
    if mode == 'mono':
        return dict(s, color_phase=0)
    color = actor_color(s['id'])
    pixels, masks = [], []
    for row, mask in zip(s['pixels'], s['masks']):
        p, m = [], []
        for x in range(0, len(row), 2):
            occupied = any(row[x:x + 2])
            opaque = any(mask[x:x + 2])
            p.extend(BITS[color] if occupied else (0, 0))
            m.extend((int(opaque), int(opaque)))
        pixels.append(p)
        masks.append(m)
    return dict(s, pixels=pixels, masks=masks, color=color,
                color_phase=phase_bit(color),
                mask_policy='two-dot silhouette; transparent attribute cells; native HGR phase')


def write_cell(page, base, x, color):
    """Write an even-aligned two-dot cell; the last chromatic write owns bit 7."""
    if x % 2 or not 0 <= x < 280:
        raise ValueError('Color cells must start on an even HGR dot')
    for k, value in enumerate(BITS[color]):
        address, bit = base + (x + k) // 7, 1 << ((x + k) % 7)
        page[address] = (page[address] | bit) if value else (page[address] & (255 ^ bit))
        if color not in (BLACK, WHITE):
            page[address] = (page[address] & 127) | phase_bit(color)


def scanline_rgb(row):
    """Digital artifact approximation with neighbors across seven-bit bytes.

    Lit neighbors become white; isolated dots use global parity and bit 7.
    Gaps between alternating dots receive dim chroma. No analog filtering,
    half-dot phase displacement or PAL/RGB-card emulation is claimed.
    """
    dots = [bool(row[x // 7] & (1 << (x % 7))) for x in range(280)]
    result = bytearray()
    for x, lit in enumerate(dots):
        before, after = (dots[x - 1] if x else False), (dots[x + 1] if x < 279 else False)
        high = bool(row[x // 7] & 128)
        color = (ORANGE if x & 1 else BLUE) if high else (GREEN if x & 1 else VIOLET)
        if lit:
            rgb = RGB[WHITE if before or after else color]
        elif before and after:
            opposite = (BLUE if x & 1 else ORANGE) if high else (VIOLET if x & 1 else GREEN)
            rgb = tuple(v // 2 for v in RGB[opposite])
        else:
            rgb = RGB[BLACK]
        result.extend(rgb)
    return bytes(result)
