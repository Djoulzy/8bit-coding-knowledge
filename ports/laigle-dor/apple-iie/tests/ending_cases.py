"""Graphical ending integration and an independent original-6502 blit oracle."""
import json
from tools.common import Source, load_py65
from tools.resources import row_offset
from tools import dhgr
from tools.ending_resources import source_canvas


class EndingTests:
    def ending_expected(self, mode, attempt=None):
        attempt = attempt or self.m.bus.ram[self.m.symbols['session_attempt']]
        name = 'ending-win' if mode == 6 else 'ending-dead-%d'%attempt
        data = (self.directory/'resources'/(name+('.hgr' if self.video=='mono' else '.dhgr'))).read_bytes()
        main, aux = bytearray(data[:8192]), bytearray(data[8192:])
        if mode == 5:
            source = Source(); font = source.read(0x9800,1024)
            for n in range(attempt):
                left = source.byte(23486+n)
                for col, code in enumerate(self.m.bus.ram[0x1380+6*n:0x1386+6*n]):
                    for dy,bits in enumerate(font[(code&127)*8:(code&127)*8+8]):
                        if self.video=='mono':
                            for bit in range(6):
                                if bits&(32>>bit):
                                    x=20+left+6*col+bit
                                    main[row_offset(164+dy)+x//7] |= 1<<(x%7)
                        else:
                            for pair in range(3):
                                color = 15 if bits&(48>>(2*pair)) else 0
                                dhgr.put_pattern(main,aux,10+left//2+3*col+pair,164+dy,color)
        return bytes(main) if self.video=='mono' else (bytes(main),bytes(aux))

    def test_ending_source_canvas_matches_executed_original_6502_blitter(self):
        source=Source();cpu=load_py65()()
        cpu.memory[0x501:0x501+len(source.blocks[2])]=source.blocks[2]
        def call(address):
            cpu.sp=255;cpu.stPushWord(0x02FE);cpu.pc=address
            for _ in range(100000):
                if cpu.pc==0x02FF:return
                cpu.step()
            self.fail('Original ending blitter did not return')
        for kind,attempt in [('win',1)]+[('dead',n) for n in range(1,6)]:
            raw=bytearray([64]*8000)
            for y in range(200):raw[40*y]=0 if kind=='dead' else 7
            cpu.memory[0xA000:0xBF40]=raw
            if kind=='win':call(0x4E2A)
            else:
                for n in range(1,attempt+1):
                    cursor=0xA000+100*40+source.byte(23485+n)//6
                    cpu.memory[0x10:0x12]=[cursor&255,cursor>>8]
                    cpu.memory[0x68]=112;call(0x3EBD)
                cursor=0xA000+30*40+40//6
                cpu.memory[0x10:0x12]=[cursor&255,cursor>>8]
                cpu.memory[0x68]=113;call(0x3EBD)
                for y in range(79):cpu.memory[0xA000+40*y]=20
                for y in range(80,200):cpu.memory[0xA001+40*y]=7
            self.assertEqual(bytes(cpu.memory[0xA000:0xBF40]),
                             bytes(source_canvas(source,kind,attempt)),(kind,attempt))

    def ending_check_pair(self, mode):
        expected=self.ending_expected(mode)
        for _ in range(2):
            self.m.frame()
            self.assertEqual(self.m.displayed_page(),expected)
            self.assertEqual((self.m.bus.switches['TEXT'],self.m.bus.switches['MIXED']),(0,0))
            self.assertEqual(self.m.bus.switches['80COL'],int(self.video=='dhgr'))
            self.assertEqual(self.m.bus.switches['DHIRES'],int(self.video=='dhgr'))
        self.assertFalse(self.m.bus.visible_write_violations)
        self.assertFalse(self.m.bus.visible_text_write_violations)
        self.m.bus.bank_graphics_writes.clear();self.m.bus.io.clear()
        self.m.frame()
        self.assertFalse(self.m.bus.motor)
        self.assertFalse(self.m.bus.bank_graphics_writes)
        self.assertFalse(any(0xC0E0<=entry[1]<=0xC0EF for entry in self.m.bus.io))
        return expected

    def test_graphical_victory_requires_all_three_objectives_on_exit_and_caches_both_pages(self):
        for missing in range(8):
            self.set('game_mode',0);self.set('current_room',12);self.set('facing',3)
            self.set('objectives',missing);self.call('full_transition')
            self.assertEqual(self.m.state()['game_mode'],1 if missing else 6)
        self.set('game_mode',0);self.set('objectives',0);self.call('full_transition')
        world=bytes(self.m.bus.ram[0x1000:0x1200]);energy=self.m.state()['energy']
        atlas=bytes(self.m.bus.aux[0x6000:0xC000])
        self.ending_check_pair(6)
        (self.directory/'ending-victory.png').write_bytes(self.m.screen_png())
        self.assertEqual(bytes(self.m.bus.ram[0x1000:0x1200]),world)
        self.assertEqual(bytes(self.m.bus.aux[0x6000:0xC000]),atlas)
        self.assertEqual(self.m.state()['energy'],energy)
        self.m.frame(ord('H'));self.assertEqual(self.m.state()['game_mode'],10)
        self.m.frame(32);self.ending_check_pair(6)
        self.m.frame(13);self.assertEqual(self.m.state()['game_mode'],8)
        self.m.frame(13);self.m.frame(ord('1'));self.m.frame()
        self.assertEqual((self.m.state()['game_mode'],self.m.state()['current_room']),(0,12))
        self.assertEqual(self.m.state()['objectives'],7)
        self.assertEqual(self.m.bus.switches['MIXED'],1)
        self.assertFalse(self.m.bus.visible_write_violations)

    def test_graphical_death_retains_five_names_then_wraps_and_replays(self):
        names=[b'ALICE ',b'BOB   ',b'cHarLe',b'DAVID ',b'ELISE ']
        for attempt,name in enumerate(names,1):
            self.assertEqual(self.m.state()['game_mode'],8)
            self.assertEqual(self.m.bus.ram[self.m.symbols['session_attempt']],attempt)
            address=self.m.symbols['player_name'];self.m.bus.ram[address:address+6]=name
            self.set('name_count',6);self.m.frame(13);self.m.frame(ord('1'))
            self.word('energy',65535);self.m.frame()
            self.assertEqual(self.m.state()['game_mode'],5)
            expected=self.ending_check_pair(5)
            self.assertEqual(bytes(self.m.bus.ram[0x1380:0x1380+attempt*6]),b''.join(names[:attempt]))
            if attempt in [1,5]:
                (self.directory/('ending-death-%d.png'%attempt)).write_bytes(self.m.screen_png())
            self.m.frame(ord('?'));self.m.frame(32);self.ending_check_pair(5)
            self.assertEqual(self.m.displayed_page(),expected)
            self.m.frame(ord('O'))
        self.assertEqual(self.m.bus.ram[self.m.symbols['session_attempt']],1)
        self.assertEqual(self.m.state()['game_mode'],8)
        self.assertFalse(self.m.bus.visible_write_violations)

    def test_ending_disk_slots_and_overlay_leave_resident_code_and_aux_assets_intact(self):
        report=json.loads((self.directory/'resources/ending-manifest.json').read_text())
        self.assertEqual([s['sector'] for s in report['scenes']],[352,384,416,448,480,512])
        self.assertTrue(all(s['overlay_bytes']<=8192 for s in report['scenes']))
        resident=bytes(self.m.bus.ram[0x6000:0xA000])
        aux=bytes(self.m.bus.aux[0x0C00:0x2000]+self.m.bus.aux[0x6000:0xC000])
        self.set('game_mode',6);self.ending_check_pair(6)
        self.assertEqual(bytes(self.m.bus.ram[0x6000:0xA000]),resident)
        self.assertEqual(bytes(self.m.bus.aux[0x0C00:0x2000]+self.m.bus.aux[0x6000:0xC000]),aux)
