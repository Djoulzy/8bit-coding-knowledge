"""Apple mixed-HGR layout and declared room-12 viewport, independent of game rules."""
HGR_HEIGHT = 160
SOURCE_HEIGHT = 200
CROP_TOP = 35  # B2 690 clears this entire band in room 12.
BASELINE = 0xA000
STATE = 0x0C00
EVENT_LOG = 0x0D00


def source_y(y):
    if not CROP_TOP <= y < SOURCE_HEIGHT:
        return None
    return (y - CROP_TOP) * HGR_HEIGHT // (SOURCE_HEIGHT - CROP_TOP)


def text_offset(row):
    if not 0 <= row < 24:
        raise ValueError('Text row outside 24-row display')
    return (row & 7) * 128 + (row >> 3) * 40


def text_address(row, page=0):
    if page not in [0, 1]:
        raise ValueError('Text page must be 0 or 1')
    return 0x400 + page * 0x400 + text_offset(row)
