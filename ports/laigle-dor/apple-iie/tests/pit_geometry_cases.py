"""Executed marker-bank and oubliette-floor regressions for both editions."""
from fractions import Fraction
from tools import dhgr, mono
from tools.common import Source
from tools.video_layout import source_y


# Pinned B2 $9D08..$9D4F, independent of the exporter's font-bank constant.
GLYPHS = dict(zip(range(33, 42), map(bytes.fromhex, (
    'f0f0f00000000000', '0400080800000200', '0000182100000000',
    '1008000400000800', '0000000118000000', '000000040a0a0400',
    '0000000814140800', '00000004150e1504', '0000110a040a1201'))))


class PitGeometryTests:
    def glyph_pages(self, code, x, y):
        main, aux = bytearray(8192), bytearray(8192)
        for row, bits in enumerate(GLYPHS[code]):
            ty = source_y(y + row)
            if ty is None or source_y(y + row + 1) == ty:
                continue
            if self.video == 'mono':
                for col in range(6):
                    if bits & (32 >> col): mono.put(main, x + col, ty, 1)
            else:
                for col in range(3):
                    if bits & (48 >> (2 * col)):
                        dhgr.put_cell(main, aux, 10 + x // 2 + col, ty, 13)
        return bytes(main), bytes(aux)

    def clear_glyph_page(self, page):
        # Isolated raster worker checks run with TEXT visible, so neither
        # graphics page is displayed while the worker writes it.
        self.m.bus.switches['TEXT'] = 1
        self.m.bus.ram[page:page + 8192] = bytes(8192)
        self.m.bus.aux[page:page + 8192] = bytes(8192)
        self.set('draw_page_hi', page >> 8)

    def assert_glyph_page(self, page, expected):
        self.assertEqual(bytes(self.m.bus.ram[page:page + 8192]), expected[0])
        self.assertEqual(bytes(self.m.bus.aux[page:page + 8192]), expected[1])

    def test_alternate_hint_glyphs_render_captured_bytes_on_both_pages(self):
        source = Source()
        self.assertEqual(source.read(0x9948, 8).hex(), '0804020202040800',
                         'standard code 41 is the erroneous right parenthesis')
        for code, raw in GLYPHS.items():
            self.assertEqual(source.read(0x9C00 + 8 * code, 8), raw)
            self.assertEqual(self.constructor.font[8 * code:8 * code + 8], raw)
            # Include non-byte-aligned anchors and a statically skipped row.
            for x, y in ((101, 170), (220, 110)):
                for page in (0x2000, 0x4000):
                    with self.subTest(code=code, x=x, y=y, page=page):
                        self.clear_glyph_page(page)
                        # room-builder.s scene_x/y/id private parameter ABI.
                        self.m.bus.ram[0xEA:0xEC] = bytes((x, y))
                        self.m.bus.ram[0xEE] = 128 + code
                        self.call('scene_glyph')
                        self.assert_glyph_page(page, self.glyph_pages(code, x, y))

    def test_floor_hints_keep_source_anchors_and_ring_hides_only_unopened_hints(self):
        # Explicit B2 anchors for R=1..4; target floor anchors for R=0/5.
        rooms = (0, 5, 7, 23, 28, 32, 40, 41, 53, 55, 61, 62)
        cases = [(room,self.variation[room]) for room in rooms] + [(55,63)]
        for room,m in cases:
            self.m.bus.ram[0x1000:0x1200] = self.world
            for name, value in [('current_room',room), ('in_pit',0),
                                ('game_mode',0), ('possessions',0)]:
                self.set(name, value)
            self.call('world_load_scene')
            # M=63 is a controlled R=5 edge case, absent from the initial world.
            self.m.bus.ram[0x1292] = m
            r = (m & 63) * 5 // 63
            n = 6 * (9 + ((m & 31) * 4 // 31) * 4)
            x, y = {1:(n,176), 2:(n+18,170), 3:(n+36,176),
                    4:(n+18,184)}.get(r, (n+18,176))
            for ring in (0,4):
                for page in (0x2000, 0x4000):
                    with self.subTest(room=room, ring=ring, page=page):
                        self.clear_glyph_page(page)
                        self.set('possessions', ring)
                        self.m.bus.ram[0xEA:0xEC] = bytes((214,80))
                        self.call('scene_floor')
                        expected = (bytes(8192),bytes(8192)) if ring else self.glyph_pages(33+r,x,y)
                        self.assert_glyph_page(page, expected)
            # An already opened trap stays visible with the ring. Compare
            # complete isolated hatch rasters, independent of user retouches.
            self.m.bus.ram[0x1294] = 1  # full-memory.inc room_floor decode
            hatch = []
            for ring in (0,4):
                self.clear_glyph_page(0x2000); self.set('possessions',ring)
                self.call('scene_floor')
                hatch.append((bytes(self.m.bus.ram[0x2000:0x4000]),
                              bytes(self.m.bus.aux[0x2000:0x4000])))
            self.assertEqual(hatch[0], hatch[1])
            self.assertTrue(any(hatch[0][0]) or any(hatch[0][1]))

    def test_room55_and_implicit_variants_show_floor_hints_on_both_buffers(self):
        # Integration regression: the previous isolated test accepted (214,80),
        # hiding R=0 in the right wall torch. Inspect actual floor pixels after
        # the complete constructor and both page flips, without owning the ring.
        for room in (55,5,53,61,62):
            self.m.bus.ram[0x1000:0x1200] = self.world
            for name,value in [('current_room',room),('in_pit',0),('game_mode',0),
                    ('actor_x',19),('actor_y',160),('facing',0),('pose',0),
                    ('frame_id',0),('walking',0),('held_item',0),('action_kind',0)]:
                self.set(name,value)
            m = self.variation[room]
            self.assertEqual((m&63)*5//63,0)
            n = 6 * (9 + ((m&31)*4//31)*4)
            expected = self.glyph_pages(33,n+18,176)
            self.assertTrue(any(expected[0]) or any(expected[1]))
            for ring in (4,0):
                self.set('possessions',ring)
                self.call('world_load_scene')
                pages = set()
                for _ in range(2):
                    self.call('draw_scene'); self.call('present_frame')
                    page = self.m.state()['display_page_hi']*256
                    pages.add(page)
                    for bank,mask in zip((self.m.bus.ram,self.m.bus.aux),expected):
                        for offset,bits in enumerate(mask):
                            if not bits: continue
                            with self.subTest(room=room,ring=ring,page=page,offset=offset):
                                self.assertEqual(bank[0xA000+offset]&bits,0 if ring else bits,'baseline floor hint')
                                self.assertEqual(bank[page+offset]&bits,0 if ring else bits,'displayed floor hint')
                self.assertEqual(pages,{0x2000,0x4000})
                if room==55:
                    filename='room55-trap-%s.png'%('ring' if ring else 'hint')
                    (self.directory/filename).write_bytes(self.m.screen_png())
        self.assertFalse(self.m.bus.visible_write_violations)
        self.assertFalse(self.m.bus.visible_text_write_violations)

    def test_pit_walk_probes_fit_the_drawn_floor_and_never_use_room_portals(self):
        self.set('current_room',23); self.call('world_load_scene')
        self.set('in_pit',1); self.call('world_load_scene')
        grid = bytes(self.m.bus.ram[0x1200:0x1278])
        accepted = 0
        # Derive expectations from the source outline, not the assembly table.
        # Each target band uses the floor's narrowest (back) five-row edge.
        for y in range(155,201):
            back = 160 + 5 * ((y - 160) // 5)
            left = (104 - Fraction(23*(back-159),20) if back <= 179
                    else 81 - Fraction(9*(back-179),20))
            right = 238 - left
            for x in range(40):
                fits = (160 <= y <= 195 and 6*(x+2) >= left and 6*(x+4)-1 <= right)
                accepted += fits
                for facing, dx, dy in ((0,0,5),(1,1,0),(2,-1,0),(3,0,-5)):
                    self.set('actor_x',(x-dx)&255); self.set('actor_y',(y-dy)&255)
                    self.set('facing',facing)
                    self.call('collision_probe')
                    self.assertEqual((self.m.bus.ram[self.m.symbols['move_x']],
                                      self.m.bus.ram[self.m.symbols['move_y']]),(x,y))
                    self.assertEqual(self.m.state()['blocked'],int(not fits),(x,y,facing))
                    self.assertEqual((self.m.state()['door_status'],self.m.state()['object_status']),(4,0))
        self.assertGreater(accepted,200,'the pit floor must remain walkable')
        self.assertEqual(bytes(self.m.bus.ram[0x1200:0x1278]),grid)
        self.assertEqual((self.m.state()['current_room'],self.m.state()['in_pit']),(23,1))

    def test_pit_horizontal_jumps_require_a_landing_inside_the_floor(self):
        self.set('current_room',23); self.call('world_load_scene')
        self.set('in_pit',1); self.call('world_load_scene')
        for x,y,facing,allowed in ((12,180,1,True), (22,180,1,False),
                (22,180,2,True), (16,160,1,False), (18,160,2,False),
                (11,195,1,True), (23,195,2,True)):
            with self.subTest(x=x,y=y,facing=facing):
                for name,value in [('actor_x',x),('actor_y',y),('facing',facing),
                        ('pose',facing),('walking',0),('held_item',1),
                        ('action_kind',0),('action_phase',0),('message_id',0)]:
                    self.set(name,value)
                self.call('full_start_jump')
                self.assertEqual(self.m.state()['action_kind'],3 if allowed else 0)
                if allowed:
                    for _ in range(5):self.call('full_action_tick')
                    self.assertEqual((self.m.state()['actor_x'],self.m.state()['actor_y']),
                                     (x+(8 if facing==1 else -8),y))
                    self.assertEqual(self.m.state()['action_kind'],0)
                else:
                    self.assertEqual((self.m.state()['actor_x'],self.m.state()['actor_y']),(x,y))
                    self.assertEqual(self.m.bus.ram[self.m.symbols['message_id']],1)
                self.assertEqual(self.m.state()['held_item'],1)
                self.assertEqual((self.m.state()['current_room'],self.m.state()['in_pit']),(23,1))

    def test_room36_marker_and_pit_walk_routes_are_visible_without_wall_escape(self):
        self.gate_room()
        self.set('possessions',0)
        self.call('world_load_scene'); self.call('draw_scene'); self.call('present_frame')
        (self.directory/'room36-marker.png').write_bytes(self.m.screen_png())
        # Verify its actual room-constructor placement, including the baseline.
        expected = self.glyph_pages(41,220,110)
        self.assertTrue(any(expected[0]) or any(expected[1]))
        for bank, bits in zip((self.m.bus.ram,self.m.bus.aux),expected):
            self.assertTrue(all((bank[0xA000+i]&v)==v for i,v in enumerate(bits)))

        self.set('current_room',23); self.set('held_item',0)
        self.call('world_load_scene'); self.call('draw_scene'); self.call('present_frame')
        (self.directory/'room23-trap-hint.png').write_bytes(self.m.screen_png())
        self.call('full_fall'); self.call('world_load_scene')
        self.m.frame(ord('A')); self.m.frame(32)
        self.assertEqual(self.m.state()['in_pit'],1)

        def walk(x,y,facing,expected):
            for name,value in [('actor_x',x),('actor_y',y),('facing',facing),
                    ('pose',facing),('walking',1),('raw_key',255),('key_action',255)]:
                self.set(name,value)
            for _ in range(40):
                self.call('game_tick')
                if not self.m.state()['walking']:break
            else:self.fail('pit walking did not stop at a wall')
            self.assertEqual((self.m.state()['actor_x'],self.m.state()['actor_y']),expected)
            self.assertEqual((self.m.state()['current_room'],self.m.state()['in_pit']),(23,1))

        walk(22,180,2,(12,180)); walk(12,180,1,(22,180))
        walk(17,180,0,(17,195)); walk(17,195,3,(17,160))
        walk(17,160,1,(18,160)); walk(18,160,2,(16,160))
        walk(11,195,3,(11,190))
        self.set('actor_x',17); self.set('actor_y',180)
        self.set('facing',3); self.set('pose',3); self.set('walking',0)
        for _ in range(2):self.call('draw_scene'); self.call('present_frame')
        (self.directory/'pit-floor-walking.png').write_bytes(self.m.screen_png())
        self.assertFalse(self.m.bus.visible_write_violations)
        self.assertFalse(self.m.bus.visible_text_write_violations)
