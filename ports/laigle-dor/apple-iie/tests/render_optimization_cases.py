"""Pixel equivalence, per-page cache invalidation and sampled wear-clock tests."""
from tools.common import Source
from tools.game_resources import native_artwork
from tools import dhgr, mono
from tools.resources import sprite


class RenderOptimizationTests:
    def test_partial_departure_keeps_compact_text_layout_and_live_gold(self):
        for mode, first, second in [
                (7,'Fin du voyage','Vous quittez le chateau')]:
            self.set('game_mode',mode);self.word('gold',12345)
            self.m.frame()
            rows=[self.decode_text(row) for row in self.m.text_rows(all_rows=True)]
            self.assertTrue(rows[4].startswith("L'Aigle d'Or"))
            self.assertEqual(rows[4][28:33],'12345')
            self.assertEqual(rows[8].strip(),first)
            self.assertEqual(rows[9].strip(),second)
            self.assertEqual(rows[10].strip(),'O ou Entree: nouvel essai')
            self.assertEqual((self.m.bus.switches['TEXT'],self.m.bus.switches['80COL']),(1,0))

    def test_native_blitter_all_actors_all_horizontal_phases(self):
        native, _, _, _ = native_artwork(Source(), self.video)
        actors = [s for s in native if 'statuses' in s]
        for index, s in enumerate(actors):
            for x in range(1, 8):
                page_index = x & 1
                page = 0x4000 if page_index else 0x2000
                self.m.bus.ram[page:page+8192] = bytes([0x55])*8192
                self.m.bus.aux[page:page+8192] = bytes([0x2A])*8192
                expected = (bytearray([0x55])*8192, bytearray([0x2A])*8192)
                if self.video == 'mono':
                    mono.actor_layer(expected[0], sprite(Source(), s['id']), x, 140)
                else:
                    dhgr.reference_layer(*expected, s, x, 140)
                for name, value in [('actor_x', x), ('actor_y', 140),
                        ('sprite_index', index), ('dx', 0), ('dy', 0),
                        ('draw_page_hi', page >> 8), ('render_page_index', page_index),
                        ('static_draw', 0), ('scene_additive', 0)]:
                    self.set(name, value)
                self.call('draw_sprite')
                self.assertEqual(self.m.bus.ram[page:page+8192], expected[0], (s['id'], x, 'MAIN'))
                self.assertEqual(self.m.bus.aux[page:page+8192], expected[1], (s['id'], x, 'AUX'))

    def test_actor_cache_matches_forced_composition_on_both_pages(self):
        extra=(self.directory/'extra-assets.bin').read_bytes()
        self.m.frame(13); self.m.frame(ord('1')); self.m.frame()
        for x, held, enemy, pit, cacheable in [
                (19,0,0,0,True), (8,0,0,0,True), (27,0,0,0,True),
                (7,0,0,0,False), (28,0,0,0,False), (19,1,0,0,False),
                (19,0,1,0,False), (19,0,0,1,False), (19,0,0,0,True)]:
            for name, value in [('actor_x',x), ('actor_y',140), ('held_item',held),
                    ('enemy_kind',enemy), ('enemy_x',15), ('enemy_y',140),
                    ('in_pit',pit), ('walking',0), ('frame_id',0), ('facing',0)]:
                self.set(name,value)
            for _ in range(4):
                self.call('draw_scene'); self.call('present_frame')
            for _ in range(2):
                self.m.pcs.clear()
                self.call('draw_scene')
                self.assertEqual(self.m.symbols['draw_sprite'] not in self.m.pcs, cacheable)
                page_hi=self.m.state()['draw_page_hi'];page=page_hi*256
                before=(bytes(self.m.bus.ram[page:page+8192]),bytes(self.m.bus.aux[page:page+8192]))
                self.m.bus.ram[self.m.symbols['cache_frame']+int(page_hi==0x40)]=255
                self.call('draw_scene')
                actual=(bytes(self.m.bus.ram[page:page+8192]),bytes(self.m.bus.aux[page:page+8192]))
                delta=[(bank,offset,a,b) for bank in range(2) for offset,(a,b)
                       in enumerate(zip(actual[bank],before[bank])) if a!=b]
                self.assertFalse(delta, (x,held,enemy,pit,cacheable,page_hi,delta[:12]))
                self.assertEqual(bytes(self.m.bus.aux[0xC00:0xC00+len(extra)]),extra)
                self.call('present_frame')
        self.assertFalse(self.m.bus.visible_write_violations)
        self.set('room_light',0)
        self.m.pcs.clear();self.call('draw_scene')
        self.assertIn(self.m.symbols['full_dark_text_draw'],self.m.pcs)

    def test_wear_clock_counts_refreshes_and_pauses_in_menus(self):
        self.m.frame(13); self.m.frame(ord('1')); self.m.frame()
        self.set('held_item',1); self.set('torches',3); self.word('torch_life',1000)
        self.call('clock_reset')
        start=self.m.cpu.processorCycles;before=self.m.state()
        for _ in range(12):self.m.frame()
        end=self.m.cpu.processorCycles;after=self.m.state()
        elapsed=(end-192*65)//(262*65)-(start-192*65)//(262*65)
        losses=before['energy']-after['energy']
        self.assertEqual(before['torch_life']-after['torch_life'],losses)
        self.assertEqual(losses*18+self.m.bus.ram[self.m.symbols['clock_vbls']],elapsed)
        self.m.frame(ord('H'));paused=self.m.state()
        for _ in range(6):self.m.frame()
        self.assertEqual(self.m.state()['energy'],paused['energy'])
        self.assertEqual(self.m.state()['torch_life'],paused['torch_life'])
        self.assertEqual(self.m.bus.ram[self.m.symbols['clock_vbls']],0)
        self.m.frame(32)
        self.assertEqual(self.m.state()['energy'],paused['energy'])
        self.assertEqual(self.m.state()['torch_life'],paused['torch_life'])
