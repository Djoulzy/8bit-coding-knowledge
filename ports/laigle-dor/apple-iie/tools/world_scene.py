"""Source-backed room constructor, B2 BASIC 100-1110.

Pure target resource generation: native colors are new art, Oric attributes
are ignored. Vector rasterization and captured glyph use retain their declared
prototype limitations. ROM variation is supplied separately and hash-pinned.
"""
from functools import lru_cache
from tools.resources import sprite
from tools import dhgr
from model.world import Room
from tools.scenery import SECRET

# Native material choices for additional room artwork, not historical ink.
COLORS = {1:15, 2:15, 3:15, 4:15, 5:5, 6:5, 7:5, 8:5, 9:15,
          10:5, 11:15, 12:5, 13:15, 14:8, 15:8, 16:8, 17:5, 18:5,
          20:5, 21:13, 22:13, 23:8, 24:8, 25:8, 26:8, 27:8, 28:13,
          30:13, 31:6, 32:13, 33:5, 34:11, 35:13, 38:13, 90:8, 93:8}


class Constructor:
    def __init__(self, source):
        self.source = source
        self.font = source.read(0x9800, 2048)

    @lru_cache(None)
    def atlas(self, sid):
        return sprite(self.source, sid)

    def scene(self, world, number, variation, objectives=7, ring=False):
        room = Room.decode(world, number)
        image = [[0] * 240 for _ in range(200)]
        grid = bytearray(120)
        operations = []
        cursor = [12, 199]

        def line(x0, y0, x1, y1, evidence):
            operations.append(['line', x0, y0, x1, y1, evidence])
            dx, dy = abs(x1 - x0), -abs(y1 - y0)
            sx, sy, err = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1), dx + dy
            while True:
                if 0 <= x0 < 240 and 0 <= y0 < 200:
                    image[y0][x0] = 15
                if (x0, y0) == (x1, y1): break
                e = err * 2
                if e >= dy: err += dy; x0 += sx
                if e <= dx: err += dx; y0 += sy

        def draw(dx, dy, evidence):
            x, y = cursor
            line(x, y, x + dx, y + dy, evidence)
            cursor[:] = [x + dx, y + dy]

        def stamp(sid, x, y, additive=False, evidence='B2 room constructor'):
            s = self.atlas(sid)
            left = (x // 6 + 1) * 6
            color = COLORS[sid]
            cursor[:] = [x, y]
            operations.append(['sprite', sid, left, y, additive, x, evidence])
            for j, row in enumerate(s['pixels']):
                for k, v in enumerate(row):
                    if 0 <= y + j < 200 and 0 <= left + k < 240:
                        if additive:
                            if v: image[y + j][left + k] = color
                        elif s['masks'][j][k]:
                            image[y + j][left + k] = color if v else 0

        def glyph(code, x, y):
            operations.append(['captured_glyph', code, x, y, 'B2 CHAR; runtime font unverified'])
            for j, bits in enumerate(self.font[code * 8:code * 8 + 8]):
                for k in range(6):
                    if bits & (32 >> k) and 0 <= x + k < 240 and 0 <= y + j < 200:
                        image[y + j][x + k] = 13

        def cells(address, value, count=3):
            first = address - 1024 + 1  # B2 line 5 pre-increments V
            if not 0 <= first or first + count > 120: raise ValueError('Bad collision cells')
            grid[first:first + count] = bytes([value]) * count

        sp, far, left, right = room.geometry, room.fields[0], room.fields[1], room.fields[2]
        if sp == 0:
            draw(36, -60, 'B2 200'); draw(155, 0, 'B2 200'); draw(36, 60, 'B2 200')
            if far: stamp(5, 99, 69)
            for y in range(122, 122 - 7 * 17, -17): stamp(4, 36, y, True)
            for y in range(121, 121 - 7 * 18, -18): stamp(3, 191, y, True)
            if far not in (0, 3): stamp(7 + far, 105, 79, True)
        elif sp in (1, 2):
            draw(48, -80, 'B2 390'); draw(131, 0, 'B2 390'); draw(48, 80, 'B2 390')
            if far: stamp(5, 99, 49)
            if room.furnishing == 1 or number == 63:
                stamp(20, 99, 76)
                if room.fields[3] & 1:
                    operations.append(['secret_marker', SECRET['curset_x'], SECRET['y'], SECRET['evidence']])
                    marker_left = (SECRET['curset_x']//6+1)*6
                    for j,row in enumerate(SECRET['rows']):
                        for k,v in enumerate(row):
                            image[SECRET['y']+j][marker_left+2*k:marker_left+2*k+2] = [5 if v=='g' else 0]*2
            if sp == 1:
                for y in range(102, 102 - 6 * 17, -17): stamp(4, 48, y, True)
                for y in range(101, 101 - 6 * 18, -18): stamp(3, 179, y, True)
            else:
                for x in (58, 73, 178, 193): line(x, 119, x, 19, 'B2 400/410')
                for x in (50, 169): stamp(1, x, 19); stamp(2, x, 112)
            if far not in (0, 3): stamp(7 + far, 105, 59, True)
        else:
            draw(31, -50, 'B2 500'); draw(165, 0, 'B2 500'); draw(31, 50, 'B2 500')
            line(43, 149, 43, 39, 'B2 500')
            cursor[:] = [43,39]
            for dx,dy in [(-8,-13),(-8,-7),(-8,24),(-7,40),(0,115)]: draw(dx,dy,'B2 510')
            line(208,149,208,39,'B2 520'); cursor[:] = [208,39]
            for dx,dy in [(8,-13),(8,-7),(8,24),(7,40),(0,115)]: draw(dx,dy,'B2 520/530')
        if left:
            stamp(6,6,105)
            if left != 3: stamp(left + 9,12,114 + (4 if left == 2 else 0),True)
        if right:
            stamp(7,204,105)
            if right != 3: stamp(right + 11,210,115 + (4 if right == 2 else 0),True)
        # B2 150 repeats the left border for geometry 3 after side doors.
        if sp == 3:
            line(43,149,43,39,'B2 150'); cursor[:] = [43,39]
            for dx,dy in [(-8,-13),(-8,-7),(-8,24),(-7,40),(0,115)]: draw(dx,dy,'B2 510')
        for address in (1065,1100,1109,1136): cells(address,128)
        grid[3],grid[37] = 128 + left,128 + right
        m = variation[number]
        f = room.furnishing
        if f == 2: stamp(21,80 if m > 128 else 147,36 if m > 128 else 45)
        elif f == 3: stamp(22,80,45)  # literal V=room from line 607, not M
        elif f == 4:
            stamp(23,165,97 if sp in (1,2) else 120); cells(1131 if sp in (1,2) else 1092,151)
        elif f == 5:
            stamp(25,165 if sp == 0 else 159,130 if sp == 0 else 107)
            address = 1092 if sp == 0 else 1132
            cells(address,153); cells(address + 3,153)
        elif f == 6 and sp in (1,2): stamp(24,189,122); cells(1096,152)
        elif f == 7:
            opened = room.fields[10] == 3
            stamp(27 if opened else 26,177,126 if opened else 136); cells(1096,154)
        if room.light: stamp(14,18,80); stamp(15,214,80)
        if room.features[0]:
            address = ((m & 31) * 4 // 31) * 4 + 1034
            cells(address,1); n = 6 * (address - 1025)
            if room.floor: stamp(16,n,172)
            elif not ring:
                r = (m & 63) * 5 // 63
                positions = {1:(n,176),2:(n+18,170),3:(n+36,176),4:(n+18,184)}
                if r in positions: cursor[:] = positions[r]
                glyph(33+r,*cursor)
        if room.features[1]:
            if room.gate:
                sx = 158 if m > 200 else 68
                for y in range(10,10+7*19,19): stamp(18 if m > 200 else 17,sx,y,True)
                for y in range(0,8*20,20): stamp(18 if m > 200 else 17,sx+6 if m > 200 else sx-6,y,True)
                for address in ((1051,1091) if m > 200 else (1035,1075)): cells(address,128)
            elif room.fields[3] <= 1 and not ring:
                if m > 200:
                    line(164,40,164,110,'B2 990'); line(162,80,162,130,'B2 990')
                else:
                    for j in range(4): line(95-7*j,133+15*j,88-7*j,148+15*j,'B2 964')
        if room.features[2] and room.fields[3] <= 1 and sp != 3 and not ring: glyph(39,42,100)
        tr = room.treasure
        if sp != 3 and f != 7:
            positions = {1:(35,36,153),2:(32,42,153),3:(33,30,153),4:(33,30,153),
                         5:(34,36,143),6:(38,36,153),7:(30,42,140)}
            if tr: stamp(*positions[tr]); cells(1071,160,6 if tr == 7 else 3)
        if room.fields[3] > 1:
            address = m * 4 // 256 * 4 + 1035
            cells(address,156); cells(address+4,156); stamp(28,6*(address-1025),169)
        if number == 63 and objectives & 4: stamp(30,183,107)
        if number == 62 and objectives & 2: stamp(31,183,104)
        if number == 1 and objectives & 1: stamp(93,183,120)
        if number == 62: glyph(40,122,154)
        if number == 36: glyph(41,220,110)
        if number == 63: stamp(16,78,172)
        image[:35] = [[0] * 240 for _ in range(35)]
        return image, bytes(grid), operations, room
