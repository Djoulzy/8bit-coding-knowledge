"""Native grille-trap sequencing and a consistent bottom HUD in dark rooms."""
from tools.resources import row_offset


class RoomHazardTests:
    def test_compact_clue_rows_blank_fullwidth_and_page_carry(self):
        # Controlled formatter input in the mutable WORLD buffer; no world
        # rules run here. Exercise the terminating NUL across a source page.
        for content in (b'', b'Abcd', b'A'*40):
            source,destination=0x10F8,0x800
            self.m.bus.ram[source:source+len(content)+1]=content+b'\0'
            self.m.bus.ram[destination:destination+41]=bytes([0xA5])*41
            self.word('menu_ptr',source); self.word('dst_ptr',destination)
            self.m.cpu.y=0
            self.call('full_hud_clue_row')
            expected=bytes(c|0x80 for c in content)+b'\xA0'*(40-len(content))
            self.assertEqual(self.m.bus.ram[destination:destination+40],expected)
            self.assertEqual(self.m.bus.ram[destination+40],0xA5,'no write past the row')
            a=self.m.symbols['menu_ptr']
            self.assertEqual(int.from_bytes(self.m.bus.ram[a:a+2],'little'),source+len(content)+1)

    def gate_room(self, room=36, x=19, facing=0):
        self.m.bus.ram[0x1000:0x1200] = self.world
        for name, value in [('game_mode',0), ('current_room',room), ('actor_x',x),
                ('actor_y',180), ('facing',facing), ('pose',facing), ('walking',0),
                ('in_pit',0), ('action_kind',0), ('action_phase',0), ('gate_jump',0),
                ('held_item',1), ('torches',1), ('room_dirty',0), ('message_id',0)]:
            self.set(name, value)
        self.word('energy',10000); self.word('drain',0); self.word('torch_life',250)
        self.call('world_load_scene')

    def test_room36_grille_falls_on_both_pages_before_death_and_pauses_with_help(self):
        self.gate_room()
        self.set('held_item',0)
        self.call('draw_scene'); self.call('present_frame')
        self.assertEqual(self.m.bus.switches['TEXT'],1)
        self.m.frame(ord('1'))
        self.assertEqual(self.m.bus.switches['TEXT'],0)
        self.assertEqual(self.m.bus.ram[self.m.symbols['gate_side']],27)
        self.m.frame(0x15); self.m.frame(0x15)
        for _ in range(10):
            if self.m.state()['action_kind']==5: break
            self.m.frame()
        self.assertEqual((self.m.state()['actor_x'],self.m.state()['action_kind']), (27,5))
        self.assertEqual(self.m.state()['game_mode'],0,'do not hide the falling gate with the death page')
        self.assertEqual(self.m.bus.ram[0x1100+4*36]&128,128)
        baseline=(bytes(self.m.bus.ram[0xA000:0xC000]),bytes(self.m.bus.aux[0xA000:0xC000]))
        frozen=(self.m.state()['energy'],self.m.state()['torch_life'],self.m.state()['rng_state'])
        phase=self.m.state()['action_phase']
        self.m.frame(ord('H')); self.m.frame(); self.m.frame(32)
        self.assertEqual(self.m.state()['action_phase'],phase)
        self.assertEqual(self.m.state()['game_mode'],0)
        images={}; pages=set()
        for _ in range(12):
            if self.m.state()['action_kind']!=5: break
            state=self.m.state(); phase=state['action_phase']
            self.assertEqual((state['actor_x'],state['actor_y'],state['walking']), (27,180,0))
            self.assertEqual(self.m.bus.switches['TEXT'],0)
            self.assertEqual((state['energy'],state['torch_life'],state['rng_state']),frozen)
            self.assertEqual((bytes(self.m.bus.ram[0xA000:0xC000]),bytes(self.m.bus.aux[0xA000:0xC000])),baseline)
            image=self.m.displayed_page()
            banks=image if self.video=='dhgr' else (image,)
            # Crop to the gate side: independent from the flames and text HUD.
            images[phase]=b''.join(bank[row_offset(y)+24:row_offset(y)+34]
                                  for bank in banks for y in range(5,125))
            pages.add(state['display_page_hi'])
            if phase in (1,4,8):
                (self.directory/('room36-grille-stage-%d.png'%phase)).write_bytes(self.m.screen_png())
            self.m.frame(ord('P'))  # commands are consumed by the active fall
        self.assertEqual(set(images),set(range(1,10)))
        self.assertEqual(pages,{0x20,0x40})
        self.assertGreaterEqual(len(set(images.values())),6,'the falling gate must visibly progress')
        self.assertEqual(images[8],images[9],'show the complete grille on both pages before death')
        self.assertEqual(self.m.state()['game_mode'],5)
        self.assertGreater(self.m.state()['energy'],0,'death is the trap, not darkness or depleted strength')
        self.assertEqual(self.m.state()['last_event'],10)
        self.assertEqual(self.m.displayed_page(),self.ending_expected(5))
        self.assertEqual((self.m.bus.switches['TEXT'],self.m.bus.switches['MIXED']),(0,0))
        self.assertFalse(self.m.bus.visible_write_violations)
        self.assertFalse(self.m.bus.visible_text_write_violations)

    def test_jumps_latch_both_grille_sides_and_parities_until_the_fall_finishes(self):
        # Original rooms 4/36 provide left/right traps. Controlled approach
        # positions exercise both old odd coordinates and the new even steps.
        for room,side,approaches in [(4,11,[(7,1),(8,1),(15,2),(16,2)]),
                                    (36,27,[(21,1),(22,1),(31,2),(32,2)])]:
            for x,facing in approaches:
                with self.subTest(room=room,x=x,facing=facing):
                    self.gate_room(room,x,facing)
                    self.assertEqual(self.m.bus.ram[self.m.symbols['gate_side']],side)
                    self.set('raw_key',ord('S')); self.set('key_action',255)
                    self.call('game_tick'); self.call('full_clock')
                    self.assertEqual(self.m.state()['action_kind'],3)
                    self.set('raw_key',255)
                    for _ in range(8):
                        self.call('game_tick'); self.call('full_clock')
                        if self.m.state()['action_kind']==5: break
                    self.assertEqual(self.m.state()['action_kind'],5)
                    self.assertEqual(self.m.bus.ram[self.m.symbols['gate_jump']],1)
                    self.assertEqual(self.m.state()['held_item'],1)
                    landing=x+(8 if facing==1 else -8)
                    self.assertEqual((self.m.state()['actor_x'],self.m.state()['actor_y']), (landing,180))
                    for _ in range(12):
                        self.call('game_tick'); self.call('full_clock')
                        if self.m.state()['action_kind']==0: break
                    self.assertEqual(self.m.state()['game_mode'],0)
                    self.assertEqual(self.m.state()['action_kind'],0)
                    self.assertEqual(self.m.bus.ram[self.m.symbols['gate_jump']],0)
                    self.assertEqual(self.m.bus.ram[0x1100+4*room]&128,128)
                    self.call('world_load_scene')
                    self.assertEqual(self.m.bus.ram[self.m.symbols['gate_side']],0)
                    # The already closed trap does not kill on a later visit.
                    self.set('actor_x',side); self.call('full_clock')
                    self.assertEqual(self.m.state()['game_mode'],0)

    def test_dark_rooms_keep_lit_hud_rows_and_center_only_the_darkness_message(self):
        self.m.frame(13); self.m.frame(ord('3')) # seed an old merchant screen
        self.m.frame(ord('0')); self.m.frame(ord('1'))
        for room in (9,36):
            self.gate_room(room)
            for _ in range(2): self.call('draw_scene'); self.call('present_frame')
            lit=[self.decode_text(row) for row in self.m.text_rows()]
            self.set('held_item',0)
            pages=set()
            for _ in range(3):
                self.call('draw_scene'); self.call('present_frame')
                pages.add(self.m.state()['display_page_hi'])
                self.assertEqual((self.m.bus.switches['TEXT'],self.m.bus.switches['80COL'],self.m.bus.switches['MIXED']),
                                 (1,int(self.video=='dhgr'),0))
                text=[self.decode_text(row) for row in self.m.text_rows(all_rows=True)]
                self.assertEqual(text[20:23],lit[:3])
                self.assertEqual(text[23],lit[3].replace('Torche','      '))
                width=80 if self.video=='dhgr' else 40
                self.assertEqual(text[11], 'Il fait noir ici !'.center(width))
                self.assertTrue(all(not line.strip() for i,line in enumerate(text[:20]) if i!=11))
            self.assertEqual(pages,{0x20,0x40})
            if room==36:
                (self.directory/'room36-dark-hud.png').write_bytes(self.m.screen_png())
            self.m.frame(ord('H')); self.m.frame(32)
            self.assertEqual(self.m.bus.switches['TEXT'],1)
            self.m.frame(ord('1')); self.m.frame()
            self.assertEqual(self.m.bus.switches['TEXT'],0)
            self.assertEqual(self.m.bus.switches['80COL'],int(self.video=='dhgr'))
        self.assertFalse(self.m.bus.visible_write_violations)
        self.assertFalse(self.m.bus.visible_text_write_violations)
