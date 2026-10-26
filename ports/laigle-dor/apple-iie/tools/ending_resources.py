"""Recompose the B2 victory and five-attempt memorial from historical assets.

No historical data is changed. The target uses full-screen HGR/DHGR with
native-height lettering below a 240x176 -> 240x160 picture adaptation.
"""
from tools.common import Source, digest, write_json
from tools.resources import sprite, row_offset
from tools.title_resources import ORIC_COLORS
from tools import dhgr

END_SECTOR = 352  # after the AUX scanline archive, which ends before sector 344


def victory_records(source):
    records = []
    for i in range(6):
        address = 0x5B00 + 2*i
        code = source.read(0x4E2A + 17*i, 17)
        sid = code[11]
        expected = bytes([0xAD, address & 255, address >> 8, 0x85, 0x69,
                          0xAD, (address+1) & 255, (address+1) >> 8, 0x85, 0x6A,
                          0xA9, sid, 0x85, 0x68, 0x20, 0xC6, 0x3E])
        if code != expected:
            raise ValueError('Changed victory composition at $%04X' % (0x4E2A+17*i))
        records.append((sid, source.byte(address), source.byte(address+1)))
    if source.byte(0x4E90) != 0x60:
        raise ValueError('Missing victory RTS')
    return records


def source_canvas(source, kind, attempt=1):
    raw = bytearray([64]*8000)
    for y in range(200):raw[40*y] = 0 if kind == 'dead' else 7
    def stamp(sid, column, y):
        s = sprite(source, sid); w, h = s['width_bytes'], s['height']
        data = source.read(s['source_start'], w*h)
        for row in range(h):
            offset = (y+row)*40 + column+1  # $3E52 writes Y=width..1
            raw[offset:offset+w] = data[row*w:(row+1)*w]
    if kind == 'win':
        for sid, column, y in victory_records(source):stamp(sid, column, y)
    elif kind == 'dead' and 1 <= attempt <= 5:
        for n in range(1, attempt+1):stamp(112, source.byte(23485+n)//6, 100)
        stamp(113, 40//6, 30)
        for y in range(79):raw[40*y] = 20
        for y in range(80, 200):raw[40*y+1] = 7
    else:raise ValueError((kind, attempt))
    return raw


def ending_image(source, kind, attempt=1, monochrome=False):
    raw = source_canvas(source, kind, attempt)
    image = [[0]*240 for _ in range(192)]
    # Native-height captions and names occupy rows 164..191. Keep the complete
    # source sprites (through y=171) in the first 160 target scanlines.
    for y in range(160):
        sy = y*176//160; ink, paper = 7, 0
        for bx, value in enumerate(raw[40*sy:40*sy+40]):
            if value & 0x60:
                for bit in range(6):
                    on = bool(value & (32 >> bit))
                    image[y][bx*6+bit] = int(on) if monochrome else ORIC_COLORS[ink if on else paper]
            else:
                if value < 8:ink = value
                elif 16 <= value < 24:paper = value-16
                elif not 8 <= value < 16:raise ValueError('Unexpected ending attribute')
                image[y][bx*6:bx*6+6] = [0 if monochrome else ORIC_COLORS[paper]]*6
    font = source.read(0x9800, 1024)
    def text(message, x, y):
        for i, char in enumerate(message):
            for row, bits in enumerate(font[ord(char)*8:ord(char)*8+8]):
                for bit in range(6):
                    if bits & (32 >> bit):image[y+row][x+i*6+bit] = 1 if monochrome else 15
    if kind == 'win':
        motto = source.read(0x5B11, 34).split(b'\\', 1)[0].decode('ascii')
        text(motto, 6, 164)
        text('Vous avez GAGNE !', 72, 176)
    else:
        text('Veux-tu rejouer ? (O/N)', 54, 176)
    text('O / Entree: nouvel essai', 48, 184)
    return image


def ending_pages(source, kind, attempt=1, mode='dhgr'):
    image = ending_image(source, kind, attempt, mode == 'mono')
    main, aux = bytearray(8192), bytearray(8192)
    for y, row in enumerate(image):
        if mode == 'mono':
            for x, bit in enumerate(row):
                if bit:main[row_offset(y)+(x+20)//7] |= 1 << ((x+20)%7)
        else:
            for x in range(0, 240, 2):
                a, b = row[x:x+2]
                # Complete color cells, as on the title. Prefer foreground to
                # blue sky at a boundary; this is a target color adaptation.
                color = next((c for c in (a,b) if c not in (0,2)), a or b)
                dhgr.put_pattern(main, aux, 10+x//2, y, dhgr.pattern(color))
    return bytes(main) + (bytes(aux) if mode != 'mono' else b'')


def pack(data):
    """Count/value pairs, 1..255 bytes per run; output size bounds the decoder."""
    encoded = bytearray(); i = 0
    while i < len(data):
        n = 1
        while n < 255 and i+n < len(data) and data[i+n] == data[i]:n += 1
        encoded.extend((n, data[i])); i += n
    return bytes(encoded)


def ending_runs(source, kind, attempt, mode):
    image = ending_image(source, kind, attempt, mode == 'mono')
    result = bytearray()
    for row in image:
        if mode == 'mono':cells = [15 if bit else 0 for bit in row]
        else:
            cells = [0]*10
            for x in range(0,240,2):
                a,b = row[x:x+2]
                color = next((c for c in (a,b) if c not in (0,2)), a or b)
                cells.append(dhgr.pattern(color))
            cells += [0]*10
        result.extend(pack(cells))
    return bytes(result)


def export_endings(dest, mode):
    source = Source()
    (dest/'ending-font.bin').write_bytes(source.read(0x9800,1024))
    (dest/'ending-positions.bin').write_bytes(source.read(23486,5))
    scenes = []
    for index,(kind,attempt) in enumerate([('win',1)]+[('dead',i) for i in range(1,6)]):
        name = 'ending-win' if kind == 'win' else 'ending-dead-%d'%attempt
        runs = ending_runs(source,kind,attempt,mode)
        (dest/(name+'.rle')).write_bytes(runs)
        raster = ending_pages(source,kind,attempt,mode)
        (dest/(name+('.hgr' if mode=='mono' else '.dhgr'))).write_bytes(raster)
        scenes.append({'kind':kind,'attempt':attempt if kind=='dead' else None,
                       'name':name,'sector':END_SECTOR+32*index,
                       'rle_bytes':len(runs),'rle_sha256':digest(runs),
                       'raster_sha256':digest(raster)})
    def provenance(sid):
        s = sprite(source,sid)
        return {k:s[k] for k in ['id','source_start','width_bytes','height','sha256']}
    report = {'source_block':'B2','victory':'3080-3092; $4E2A-$4E90; $5B00-$5B0B',
              'death':'9000-9050; sprites 112/113; x positions $5BBE-$5BC2',
              'victory_records':victory_records(source),
              'assets':[provenance(sid) for sid in [31,29,30,40,46,64,112,113]],
              'font':'captured standard HIRES $9800-$9BFF; source CHAR runtime not compared',
              'conversion':'source rows 0..175 sampled into target 0..159; names/motto at 164, outcome at 176, replay instruction at 184',
              'palette':'monochrome Oric foreground dots' if mode=='mono' else 'source INK/PAPER mapped to Apple palette; whole color cells',
              'replay':'O or Return starts a new attempt, retained target convenience; original victory is terminal',
              'disk_sector':END_SECTOR,'slot_sectors':32,'scenes':scenes}
    write_json(dest/'ending-manifest.json',report)
    return report
