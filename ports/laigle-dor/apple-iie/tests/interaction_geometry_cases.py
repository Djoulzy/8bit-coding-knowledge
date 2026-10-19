"""Native execution checks for carried flames and furnishing foot footprints."""
from tools import dhgr, mono
from tools.artwork import override_sprites
from tools.common import Source
from tools.game_resources import native_artwork
from tools.video_layout import source_y


class InteractionGeometryTests:
    def test_room26_chest_opens_from_front_with_crowbar(self):
        for name,value in [('game_mode',0),('current_room',26),('in_pit',0),
                ('actor_x',28),('actor_y',170),('facing',3),('pose',3),('walking',0),
                ('held_item',0),('crowbars',1),('bar_life',30)]:
            self.set(name,value)
        self.call('world_load_scene');self.call('draw_scene');self.call('present_frame')
        (self.directory/'room26-chest-closed.png').write_bytes(self.m.screen_png())
        self.m.frame(ord('5'));self.assertEqual(self.m.state()['held_item'],6)
        before=self.m.state()
        self.m.frame(ord('O'))
        self.assertEqual(self.m.bus.ram[self.m.symbols['chest_open']],1,
                         'the chest must open from the reachable front stopping point')
        self.assertEqual(self.m.bus.ram[0x1000+4*26+3]&0x30,0x30)
        self.assertEqual(self.m.bus.ram[self.m.symbols['bar_life']],29)
        self.assertEqual(self.m.state()['current_room'],26)
        (self.directory/'room26-chest-open.png').write_bytes(self.m.screen_png())
        self.m.frame(ord('P'))
        self.assertEqual((self.m.state()['gold'],self.m.state()['points']),
                         (before['gold'],before['points']))  # original room 26 is empty
        self.assertFalse(self.m.bus.visible_write_violations)
        self.assertFalse(self.m.bus.visible_text_write_violations)

    def test_all_chests_block_rear_and_top_and_keep_opening_and_rewards_reachable(self):
        for number,geometry,treasure in [(4,0,5),(13,1,5),(26,0,0),(52,0,2),(58,1,2),(60,1,5)]:
            with self.subTest(room=number):
                for name,value in [('game_mode',0),('current_room',number),('in_pit',0),
                        ('held_item',6),('crowbars',1),('bar_life',30),('action_kind',0)]:
                    self.set(name,value)
                self.call('world_load_scene')
                self.assertEqual(self.m.state()['room_furnishing'],7)
                self.assertEqual(self.m.state()['room_treasure'],treasure)
                grid=bytes(self.m.bus.ram[0x1200:0x1278])
                self.assertEqual(grid[73:76],bytes([154])*3)
                def walk(x,y,facing):
                    for name,value in [('actor_x',x),('actor_y',y),('facing',facing),
                            ('pose',facing),('walking',1),('raw_key',255),('key_action',255)]:
                        self.set(name,value)
                    for _ in range(40):
                        self.call('game_tick')
                        if not self.m.state()['walking']:
                            return self.m.state()['actor_x'],self.m.state()['actor_y']
                    self.fail('walking did not stop')
                for opened in (False,True):
                    self.assertEqual(bool(self.m.bus.ram[self.m.symbols['chest_open']]),opened)
                    self.assertEqual(walk(28,180,3),(28,170))
                    self.assertEqual(walk(20,160,1),(26,160))
                    rear=145 if geometry==0 else 125
                    self.assertEqual(walk(20,rear,1),(26,rear))
                    for x,facing in [(28,1),(31,2)]:
                        self.set('actor_x',x);self.set('actor_y',170);self.set('facing',facing)
                        self.call('collision_probe');self.assertEqual(self.m.state()['blocked'],0)
                    self.assertEqual(bytes(self.m.bus.ram[0x1200:0x1278]),grid)
                    if not opened:
                        # A wrong item and empty hands cannot open these six
                        # real chests (all source ROM variation values >100).
                        self.set('actor_x',26);self.set('actor_y',160);self.set('facing',1)
                        for item in (0,8,9):
                            self.set('held_item',item);self.call('full_open')
                            self.assertEqual(self.m.bus.ram[self.m.symbols['chest_open']],0)
                        self.set('held_item',6);self.call('full_open')
                        self.assertEqual(self.m.bus.ram[self.m.symbols['chest_open']],1)
                        self.call('world_load_scene')  # persistent open bits rebuild the same body/grid
                # P uses the same reachable front window, facing the chest.
                self.set('actor_x',28);self.set('actor_y',170);self.set('facing',3)
                before=self.m.state();self.call('full_pickup');after=self.m.state()
                self.assertEqual(after['room_treasure'],0)
                self.assertEqual(after['vials']-before['vials'],int(treasure==5))
                self.assertEqual(after['points']-before['points'],{0:0,2:10,5:7}[treasure])
                self.call('full_pickup')
                self.assertEqual((self.m.state()['vials'],self.m.state()['points'],self.m.state()['gold']),
                                 (after['vials'],after['points'],after['gold']))

    def test_room18_25_arch_round_trip_at_visible_center(self):
        for name,value in [('current_room',18),('game_mode',0),('held_item',0),('in_pit',0)]:
            self.set(name,value)
        self.call('world_load_scene')
        world=bytes(self.m.bus.ram[0x1000:0x1200])
        # Atlas 5 is anchored at source x=102. At its bottom the clear opening
        # spans 109..136; actor x=17 has a stable foot base at 114..125.
        self.set('actor_x',17);self.set('actor_y',145);self.set('facing',3)
        self.call('collision_probe')
        self.assertEqual(self.m.state()['blocked'],0,'visible center of the arch must be accessible')
        self.assertEqual(self.m.state()['door_status'],3)
        for x in (16,17,18,19,20,21):
            self.set('actor_x',x);self.call('collision_probe')
            self.assertEqual(self.m.state()['blocked'],int(x in (16,21)),x)
        for name,value in [('actor_x',17),('actor_y',180),('facing',0),('pose',0),('walking',0)]:
            self.set(name,value)
        self.call('draw_scene');self.call('present_frame')
        self.m.frame(0x0B)  # turn Up, then start walking, then release the key
        self.m.frame(0x0B)
        for _ in range(8):
            if self.m.state()['current_room']==25:
                break
            self.m.frame()
        self.assertEqual((self.m.state()['current_room'],self.m.state()['actor_x'],
                          self.m.state()['actor_y'],self.m.state()['facing']),(25,34,180,2))
        (self.directory/'room25-return-right.png').write_bytes(self.m.screen_png())
        # Original link 25/right returns to 18; 25/far is a different door.
        self.m.frame(0x15);self.m.frame(0x15)
        self.assertEqual((self.m.state()['current_room'],self.m.state()['actor_x'],
                          self.m.state()['actor_y'],self.m.state()['facing']),(18,19,145,0))
        self.assertEqual(bytes(self.m.bus.ram[0x1000:0x1200]),world)
        self.assertFalse(self.m.bus.visible_write_violations)
        self.assertFalse(self.m.bus.visible_text_write_violations)

    def test_room25_grille_to26_rejects_keys_and_accepts_crowbar(self):
        for name,value in [('current_room',25),('game_mode',0),('held_item',0),('in_pit',0),
                ('actor_x',19),('actor_y',145),('facing',3),('pose',3),('walking',0),
                ('possessions',3),('crowbars',1),('bar_life',30)]:
            self.set(name,value)
        self.call('world_load_scene');self.call('draw_scene');self.call('present_frame')
        fields=self.m.symbols['room_fields']
        self.assertEqual((self.m.bus.ram[fields],self.m.bus.ram[fields+6]),(2,2))
        world=bytes(self.m.bus.ram[0x1000:0x1200])
        for key,item in [('2',9),('3',8)]:
            self.m.frame(ord(key));self.assertEqual(self.m.state()['held_item'],item)
            self.m.frame(ord('O'))
            self.assertEqual(self.m.state()['current_room'],25)
            self.assertEqual(self.m.bus.ram[self.m.symbols['message_id']],11)
            self.assertEqual(self.m.bus.ram[self.m.symbols['bar_life']],30)
        (self.directory/'room25-grille.png').write_bytes(self.m.screen_png())
        self.m.frame(ord('5'));self.assertEqual(self.m.state()['held_item'],6)
        self.word('rng_state',0xACE1)  # repeatable native attempts, not a forced success
        for attempt in range(1,21):
            self.m.frame(ord('O'))
            self.assertEqual(self.m.bus.ram[self.m.symbols['bar_life']],30-attempt)
            if self.m.state()['current_room']!=25:
                break
        self.assertEqual(self.m.state()['current_room'],26)
        self.assertEqual(bytes(self.m.bus.ram[0x1000:0x1200]),world)
        self.assertFalse(self.m.bus.visible_write_violations)
        self.assertFalse(self.m.bus.visible_text_write_violations)

    def test_tables_block_rear_route_and_keep_front_approach(self):
        # Atlas 25 is the wide table (furnishing 5); atlas 23 is the high-backed
        # chair. Exercise the actual table rooms with their complete scene grids.
        for number, geometry in [(15,1),(17,0),(21,0),(56,0),(61,1)]:
            with self.subTest(room=number):
                for name,value in [('game_mode',0),('current_room',number),
                        ('held_item',1),('in_pit',0),('action_kind',0)]:
                    self.set(name,value)
                self.call('world_load_scene')
                self.assertEqual(self.m.bus.ram[self.m.symbols['room_furnishing']],5)
                self.assertEqual(self.m.bus.ram[self.m.symbols['room_geometry']],geometry)
                grid=bytes(self.m.bus.ram[0x1200:0x1278])
                anchor=69 if geometry==0 else 109
                self.assertEqual(grid[anchor:anchor+6],bytes([153])*6)

                def walk(x,y,facing,limit=40):
                    for name,value in [('actor_x',x),('actor_y',y),('facing',facing),
                            ('pose',facing),('walking',1),('key_action',255),('raw_key',255)]:
                        self.set(name,value)
                    for _ in range(limit):
                        self.call('game_tick')
                        if not self.m.state()['walking']:
                            return self.m.state()['actor_x'],self.m.state()['actor_y']
                    self.fail('walking did not reach an obstacle')

                rear_y=145 if geometry==0 else 125
                # Reproduce the reported route along the rear wall. The old
                # three-band grid allowed crossing behind/on the table here.
                self.assertEqual(walk(20,rear_y,1),(24 if geometry==0 else 23,rear_y))
                if number==17:
                    self.call('draw_scene');self.call('present_frame')
                    (self.directory/'table-rear-blocked.png').write_bytes(self.m.screen_png())
                # It must still be possible to walk right across its front and
                # to approach closely enough without touching its top surface.
                front_y=170 if geometry==0 else 145
                self.assertEqual(walk(28,180,3),(28,front_y))
                if number==17:
                    self.call('draw_scene');self.call('present_frame')
                    (self.directory/'table-front-approach.png').write_bytes(self.m.screen_png())
                for facing,x in [(1,23),(2,31 if geometry==0 else 30)]:
                    self.set('actor_x',x);self.set('actor_y',front_y);self.set('facing',facing)
                    self.call('collision_probe');self.assertEqual(self.m.state()['blocked'],0)
                self.assertEqual(walk(23,180,3),(23,rear_y))
                self.assertEqual(bytes(self.m.bus.ram[0x1200:0x1278]),grid)

    def test_carried_flame_tracks_torch_head_in_every_direction_and_pose(self):
        native, _, equipment, _ = native_artwork(Source(), self.video)
        atlas = {s['id']: s for s in override_sprites(
            native, 'laigle/game/' + self.video + '/atlas/', self.video)}

        def layer(pages, sid, dx, dy):
            s = atlas[sid]
            x, y = (19 + dx) & 255, (175 + dy) & 255
            if self.video == 'mono':
                mono.actor_layer(pages[0], s, x, y)
            elif 'statuses' in s:
                dhgr.reference_layer(*pages, s, x, y)
            else:
                for j, row in enumerate(s['tile_rows']):
                    ty = source_y(y + j)
                    if ty is None:
                        continue
                    for k, status in enumerate(row):
                        if status:
                            color = (s.get('accent', 0) if status == 3 else
                                     s['colors'][j] if status == 2 else 0)
                            dhgr.put_cell(*pages, 10 + (x + 1)*3 + k, ty, color)

        for pose_base in (0, 4, 8):  # standing, crouching, walking
            for facing in range(4):
                for phase in range(2):
                    for page_index, page in enumerate((0x2000, 0x4000)):
                        with self.subTest(pose=pose_base + facing, phase=phase, page=page):
                            pages = [bytearray([0x55])*8192, bytearray([0x2A])*8192]
                            self.m.bus.ram[page:page+8192] = pages[0]
                            self.m.bus.aux[page:page+8192] = pages[1]
                            crouch = 10 if pose_base == 4 else 0
                            # Independent actor-relative anchors: flame is over
                            # the head of torch 68/69/70, at the anchor of 71.
                            for dx, dy, sid in equipment[4 + facing]:
                                layer(pages, sid, dx, dy + crouch)
                            layer(pages, 72 + phase, (0, 3, 0, 3)[facing],
                                  (197, 197, 197, 199)[facing] + crouch)
                            for name, value in [('held_item',1), ('actor_x',19),
                                    ('actor_y',175), ('facing',facing),
                                    ('pose',pose_base + facing), ('action_kind',0),
                                    ('in_pit',0), ('tick_lo',phase*2),
                                    ('draw_page_hi',page >> 8), ('render_page_index',page_index)]:
                                self.set(name,value)
                            self.call('full_draw_equipment')
                            self.assertEqual(self.m.bus.ram[page:page+8192], pages[0], 'MAIN')
                            self.assertEqual(self.m.bus.aux[page:page+8192], pages[1], 'AUX')

        self.set('current_room',12); self.set('game_mode',0)
        self.call('world_load_scene')
        for facing in range(4):
            self.set('actor_y',175); self.set('facing',facing); self.set('pose',facing)
            self.set('walking',0); self.set('tick_lo',0)
            self.call('draw_scene'); self.call('present_frame')
            (self.directory/('hand-torch-%d.png'%facing)).write_bytes(self.m.screen_png())

    def test_chair_footprint_blocks_surface_but_allows_front_and_sides(self):
        # Real chair rooms, followed by synthetic coverage of the other two
        # geometry branches. Do not change the source-backed constructor grid.
        cases = [(18,0), (28,1), (35,1), (53,0), (55,0), (18,2), (18,3)]
        for number, geometry in cases:
            self.set('game_mode',0); self.set('current_room',number); self.set('in_pit',0)
            a = 0x1000 + 4*number
            self.m.bus.ram[a] = (self.m.bus.ram[a] & 63) | geometry << 6
            self.call('world_load_scene')
            self.assertEqual(self.m.bus.ram[self.m.symbols['room_furnishing']],4)
            grid = bytes(self.m.bus.ram[0x1200:0x1278])
            anchor = 69 if geometry in (0,3) else 108
            self.assertEqual(grid[anchor:anchor+3],bytes([151])*3)
            # Isolate this furnishing; keep its original coarse marks present
            # to catch accidental blocking on its accessible front/side lanes.
            self.m.bus.ram[0x1200:0x1278] = bytes(v if v == 151 else 0 for v in grid)
            inside_y = (150,135,135,160)[geometry]
            front_y = (165,140,140,165)[geometry]
            for x in (24,25,28,29):
                for y in (inside_y,front_y):
                    for facing, dx, dy in ((0,0,5),(1,1,0),(2,-1,0),(3,0,-5)):
                        with self.subTest(room=number, geometry=geometry, x=x, y=y, facing=facing):
                            self.set('actor_x',x-dx); self.set('actor_y',y-dy)
                            self.set('facing',facing); self.call('collision_probe')
                            self.assertEqual((self.m.bus.ram[self.m.symbols['move_x']],
                                              self.m.bus.ram[self.m.symbols['move_y']]),(x,y))
                            # Chair drawn at source dots 168..185, down to
                            # row 137 or 160; stable actor foot base is 12 dots.
                            overlaps = (6*(x+2) < 186 and 6*(x+4) > 168 and
                                        y < (161 if geometry in (0,3) else 138))
                            self.assertEqual(self.m.state()['blocked'],int(overlaps))

        self.set('current_room',18)
        self.m.bus.ram[0x1000+4*18] &= 63
        self.call('world_load_scene')
        for x,y,facing,blocked in ((24,150,1,True), (26,165,3,True),
                                  (29,165,2,False), (26,170,3,False)):
            for name,value in [('actor_x',x),('actor_y',y),('facing',facing),
                    ('pose',facing),('walking',1),('key_action',255),('raw_key',255)]:
                self.set(name,value)
            self.call('game_tick')
            expected = (x,y) if blocked else (x+(facing==1)-(facing==2),y-5*(facing==3))
            self.assertEqual((self.m.state()['actor_x'],self.m.state()['actor_y']),expected)

        # Pits have neither furnishing barrier; ordinary 151/153 obstacles in
        # rooms with other furnishings must still use the semantic grid.
        self.set('in_pit',1)
        for furnishing in (4,5,7):
            self.set('room_furnishing',furnishing)
            self.set('move_x',26); self.set('move_y',130)
            self.call('full_furniture_overlap'); self.assertEqual(self.m.cpu.p & 1,0)
        self.set('in_pit',0);self.set('room_furnishing',2)
        self.m.bus.ram[0x1200:0x1278]=bytes(120)
        self.set('actor_x',19);self.set('actor_y',160);self.set('facing',1)
        for marker in (151,153,154):
            self.m.bus.ram[0x1200+40+22]=marker
            self.call('collision_probe');self.assertEqual(self.m.state()['blocked'],1)
