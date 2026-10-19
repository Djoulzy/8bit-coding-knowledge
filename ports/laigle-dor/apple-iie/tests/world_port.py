"""Executed full-build integration tests, separate from the accepted prototype."""
from pathlib import Path
import json
import unittest
from tools.common import Source, ROOT, digest, write_json
from tools.machine import Machine
from tools.roms import room_variation
from tools.world_scene import Constructor
from tools.world_reference import scene_pages
from tools import dhgr
from model.world import Room
from tools.resources import sprite, row_offset
from tests.checkpoint_cases import CheckpointTests
from tests.render_optimization_cases import RenderOptimizationTests
from tests.interaction_geometry_cases import InteractionGeometryTests
from tests.action_feedback_cases import ActionFeedbackTests, OUTCOME_WORDS


class NativeWorldTests(CheckpointTests, RenderOptimizationTests, InteractionGeometryTests, ActionFeedbackTests, unittest.TestCase):
    video = 'dhgr'
    directory = ROOT/'build/game'

    @classmethod
    def setUpClass(cls):
        cls.machine=Machine(directory=cls.directory,video=cls.video)
        cls.machine.boot()
        cls.cold_ram=bytes(cls.machine.bus.ram);cls.cold_aux=bytes(cls.machine.bus.aux)
        cls.cold_switches=dict(cls.machine.bus.switches)
        cls.machine.frame(13) # title -> original textual introduction
        cls.machine.frame(13) # introduction -> name entry
        cls.ram=bytes(cls.machine.bus.ram);cls.aux=bytes(cls.machine.bus.aux)
        cls.switches=dict(cls.machine.bus.switches)
        cls.disk_state={n:getattr(cls.machine.bus,n) for n in ('half_track','coil','nibble','motor')}
        cls.world=Source().read(0x5600,512)
        cls.variation=room_variation()[0]
        cls.constructor=Constructor(Source())

    def setUp(self):
        self.m=self.machine
        self.m.bus.ram[:]=self.ram;self.m.bus.aux[:]=self.aux
        self.m.cpu.pc=self.m.symbols['main_loop'];self.m.cpu.sp=255
        self.m.bus.switches.update(self.switches)
        # RAM includes the loader's tracked head position. Restore the matching
        # drive state too: map tests now perform reads after the startup preload.
        for name,value in self.disk_state.items():setattr(self.m.bus,name,value)
        self.m.bus.strobe=False
        self.m.bus.visible_write_violations.clear();self.m.bus.visible_text_write_violations.clear()

    def set(self,name,value):
        self.m.bus.ram[self.m.symbols[name]]=value

    def word(self,name,value):
        a=self.m.symbols[name];self.m.bus.ram[a:a+2]=value.to_bytes(2,'little')

    @staticmethod
    def decode_text(row):
        return ''.join(chr(v+64 if v<32 else v&127) for v in row)

    def call(self,name,budget=3000000):
        self.m.cpu.stPushWord(0x1EFF);self.m.cpu.pc=self.m.symbols[name]
        self.m.until(0x1F00,budget)
        self.m.cpu.pc=self.m.symbols['main_loop']

    def test_boot_preloads_shared_atlas_and_keeps_program_main(self):
        start=self.m.symbols['__EXTRACODE_LOAD__']-0x6000
        size=self.m.symbols['__EXTRACODE_SIZE__']
        self.assertEqual(self.aux[0xE30:0xF00],self.cold_aux[0xE30:0xF00])
        self.assertEqual(self.ram[0xE30:0xE30+size],(self.directory/'game.bin').read_bytes()[start:start+size])
        self.assertLessEqual(size,0xD0)
        atlas=(self.directory/'aux-assets.bin').read_bytes()
        self.assertEqual(self.aux[0x6000:0x6000+len(atlas)],atlas)
        text=(self.directory/'text-assets.bin').read_bytes()
        self.assertEqual(self.aux[0x1400:0x1400+len(text)],text)
        self.assertLessEqual(len(text),0xC00)
        self.assertEqual(self.m.state()['game_mode'],8)
        self.assertEqual(self.m.state()['gold'],500)
        worker_size=self.m.symbols['__AUXREAD_SIZE__']
        self.assertLessEqual(worker_size,0x40)
        self.assertTrue(self.m.ramrd_fetch_pcs <= set(range(0x40,0x40+worker_size)))
        extra=(self.directory/'extra-assets.bin').read_bytes()
        self.assertEqual(bytes(self.m.bus.aux[0xC00:0xC00+len(extra)]),extra)
        self.assertFalse(self.m.bus.motor)
        resource=self.directory/'resources'
        report=json.loads((resource/'game-resources.json').read_text())
        self.assertEqual((report['room_bitmaps'],report['geometry_templates']),(0,4))
        self.assertFalse(list(resource.glob('room12*')))
        self.assertFalse((resource/'world-archive.bin').exists())
        self.assertEqual((resource/'room-variation.bin').read_bytes(),self.variation)

    def test_approved_actor_pixels_survive_auxiliary_and_compact_storage(self):
        ids=json.loads((self.directory/'resources/game-resources.json').read_text())['actor_sprite_ids']
        approved=[40,41,42,43,*range(46,62),64,65,67]
        source=Source()
        for sid in approved:
            converted=dhgr.target_sprite(sprite(source,sid))
            for page_index,page in enumerate([0x2000,0x4000]):
                for x,y in [(19,140),(1,20),(38,190)]:
                    self.m.bus.ram[page:page+8192]=bytes([0x55])*8192
                    self.m.bus.aux[page:page+8192]=bytes([0x2A])*8192
                    self.set('actor_x',x);self.set('actor_y',y)
                    self.set('draw_page_hi',page>>8)
                    self.m.bus.ram[0x99]=ids.index(sid)
                    self.m.bus.ram[0x9A:0x9C]=bytes(2)
                    self.m.bus.ram[0x9E]=page_index
                    expected=(bytearray([0x55]*8192),bytearray([0x2A]*8192))
                    dhgr.reference_layer(*expected,converted,x,y)
                    self.call('draw_sprite')
                    self.assertEqual(self.m.bus.ram[page:page+8192],expected[0],(sid,page,x,y))
                    self.assertEqual(self.m.bus.aux[page:page+8192],expected[1],(sid,page,x,y))

    def test_all_64_rooms_use_the_same_constructor_and_grid(self):
        results=[]
        self.set('game_mode',0);self.set('held_item',1) # permit graphical preparation even in dark rooms
        for room in range(64):
            if room%16==0:print('  Native room constructor: %d/64'%room,flush=True)
            self.set('current_room',room)
            previous=self.m.displayed_page();text_mode=self.m.bus.switches['TEXT']
            self.call('world_load_scene')
            self.assertEqual(self.m.displayed_page(),previous,'visible terrain during construction')
            self.assertEqual(self.m.bus.switches['TEXT'],text_mode)
            self.assertEqual(self.m.bus.ram[self.m.symbols['terrain_pending']],3)
            image,grid,ops,r=self.constructor.scene(self.world,room,self.variation)
            self.assertEqual(self.m.bus.ram[0x1200:0x1278],grid,room)
            actual=(bytes(self.m.bus.ram[0xA000:0xC000]),bytes(self.m.bus.aux[0xA000:0xC000]))
            expected=scene_pages(self.constructor,ops)
            self.assertEqual(actual,expected,'operation-level room %d'%room)
            for _ in range(2):
                page=self.m.state()['display_page_hi']^0x60
                self.set('draw_page_hi',page)
                self.m.bus.ram[0x9E]=int(page==0x40)
                self.call('full_prepare_page')
                page*=256
                self.assertEqual(bytes(self.m.bus.ram[page:page+8192]),actual[0])
                self.assertEqual(bytes(self.m.bus.aux[page:page+8192]),actual[1])
                self.call('present_frame')
            self.assertEqual(self.m.bus.ram[self.m.symbols['terrain_pending']],0)
            raster=dhgr.image_pages(image)
            delta=sum(a!=b for y in range(160) for a,b in zip(dhgr.cells(*actual,y),dhgr.cells(*raster,y)))
            results.append({'room':room,'geometry':r.geometry,'collision_match':True,
                            'native_matches_layer_oracle':True,'completed_raster_policy_different_cells':delta})
        write_json(self.directory/'room-verification.json',{'rooms':results,
                   'program_sha256':digest((self.directory/'game.bin').read_bytes()),
                   'execution':'py65 actual NMOS instructions; not original Oric runtime or real Apple hardware'})
        self.assertFalse(self.m.bus.visible_write_violations)

    def test_name_exterior_merchant_and_resume(self):
        for k in b'ANNA\r':self.m.frame(k)
        self.assertEqual(self.m.state()['game_mode'],1)
        self.assertEqual((self.m.bus.switches['TEXT'],self.m.bus.switches['80COL']),(1,0))
        def screen():return ''.join(bytes(v&127 for v in row).decode('ascii') for row in self.m.text_rows(all_rows=True))
        self.assertIn('ANNA, tu peux :',screen())
        (self.directory/'exterior.png').write_bytes(self.m.screen_png())
        self.m.frame(ord('3'));self.assertEqual(self.m.state()['game_mode'],2)
        self.assertIn("Pieces d'or:   500",screen())
        self.m.frame(ord('2'))
        self.assertEqual((self.m.state()['torches'],self.m.state()['gold']),(1,310))
        self.assertIn("Pieces d'or:   310",screen())
        self.m.frame(ord('3'))
        self.assertEqual((self.m.state()['ropes'],self.m.state()['gold']),(1,200))
        self.assertIn("Pieces d'or:   200",screen())
        (self.directory/'merchant.png').write_bytes(self.m.screen_png())
        self.m.frame(ord('1')) # denied, insufficient funds
        self.assertEqual((self.m.state()['vials'],self.m.state()['gold']),(0,200))
        self.assertIn("Impossible: pas assez d'or !",screen())
        self.m.frame(ord('0'));self.m.frame(ord('1'))
        self.assertEqual((self.m.bus.switches['TEXT'],self.m.bus.switches['80COL'],self.m.bus.switches['MIXED']),(0,int(self.video=='dhgr'),1))
        self.assertNotIn('Impossible',screen())
        self.m.frame(ord('I'));energy=self.m.state()['energy']
        self.m.frame();self.assertEqual(self.m.state()['energy'],energy)
        self.m.frame(32);self.assertEqual(self.m.state()['game_mode'],0)

    def test_inventory_spaced_layout_live_values_and_modal_return(self):
        self.m.frame(13);self.m.frame(ord('1'));self.m.frame(ord('i'))
        self.assertEqual(self.m.state()['game_mode'],3)
        self.assertEqual((self.m.bus.switches['TEXT'],self.m.bus.switches['80COL']),(1,0))
        def rows():return [self.decode_text(r) for r in self.m.text_rows(all_rows=True)]
        self.assertEqual(rows()[1].strip(),'Inventaire')
        self.assertEqual(rows()[3].strip(),'En main : Vide')
        (self.directory/'inventory-empty.png').write_bytes(self.m.screen_png())
        counts=[0,1,9,10,99,100,255]
        hand_choices=[(0,'Vide'),(1,'Torche'),(9,'Clef en fer'),(8,'Clef en or'),
                      (10,'Une fiole'),(6,'Pied de biche')]
        # Walk every possession bit and both objective polarities. Inventory
        # is a view: even extreme stock values leave quantities, energy and
        # position intact. The pre-existing controller tick still increments.
        for flags in range(16):
            stocks=[counts[(flags+i)%len(counts)] for i in range(4)]
            for name,value in zip(['vials','torches','ropes','crowbars'],stocks):self.set(name,value)
            self.set('possessions',flags);self.set('objectives',flags&7)
            self.set('scrolls',(flags+1)&7)
            held,label=hand_choices[flags%len(hand_choices)];self.set('held_item',held)
            before=self.m.state()
            for _ in range(2):
                self.m.frame()
                screen=rows()
                self.assertEqual(screen[3].strip(),'En main : '+label)
                for r in [0,2,4,6,8,10,12,14,16,18,20,21]:
                    self.assertEqual(screen[r],' '*40,'blank separator row %d'%r)
                for row,value in zip([7,9,11,13],stocks):
                    self.assertEqual(screen[row][17:20],'%3d'%value)
                    self.assertEqual(screen[row][20:22],'  ')
                for row,bit in zip([7,9,11,13],[1,2,4,8]):
                    self.assertEqual(screen[row][36:39],'oui' if flags&bit else 'non')
                for row,col,bit in [(17,17,1),(17,36,2),(19,17,4)]:
                    self.assertEqual(screen[row][col:col+3],'non' if flags&bit else 'oui')
                self.assertEqual(screen[19][36:39],'%d/3'%bin((flags+1)&7).count('1'))
                for name in ['energy','torch_life','actor_x','actor_y','gold','points',
                             'held_item','possessions','objectives','vials','torches','ropes','crowbars']:
                    self.assertEqual(self.m.state()[name],before[name],name)
        for name in ['vials','torches','ropes','crowbars']:self.set(name,9)
        self.set('possessions',15);self.set('objectives',0);self.set('scrolls',7)
        self.set('held_item',8);self.m.frame()
        (self.directory/'inventory-full.png').write_bytes(self.m.screen_png())
        inventory=rows()
        self.m.frame(ord('h'));self.assertEqual(self.m.state()['game_mode'],10)
        self.m.frame(32);self.assertEqual(self.m.state()['game_mode'],3)
        self.assertEqual(rows(),inventory)
        for close in [32,13,27]:
            self.m.frame(close)
            self.assertEqual((self.m.state()['game_mode'],self.m.bus.switches['TEXT']),(0,0))
            self.m.frame(ord('i'))
            self.assertEqual(rows(),inventory)
        self.assertFalse(self.m.bus.visible_write_violations)
        self.assertFalse(self.m.bus.visible_text_write_violations)

    def test_lowercase_name_text_codes_and_preview_inverse(self):
        from tools.text_font import glyph,text_cell
        for key in b'Jules\r':self.m.frame(key)
        self.assertIn('Jules, tu peux :',self.debug_text())
        for row in self.m.text_rows(all_rows=True):
            self.assertTrue(all(code>=0x80 for code in row))
        # All lowercase letters have distinct preview glyphs, and inverse
        # lowercase is a full-cell complement only with ALTCHAR enabled.
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            self.assertNotEqual(glyph(letter),glyph('?'))
            self.assertNotEqual(glyph(letter),glyph(letter.upper()))
            normal=text_cell(ord(letter)|0x80,True)
            inverse=text_cell(ord(letter),True)
            self.assertEqual(inverse,[bytes(255-v for v in row) for row in normal])
            self.assertEqual(text_cell(ord(letter),False),normal)
        self.m.frame(ord('1'));self.m.frame(ord('p'))
        self.assertEqual(self.m.bus.switches['ALTCHAR'],1)
        self.assertEqual(self.m.text_rows()[0][-10:],b'\x09mpossible')
        self.assertFalse(any(0x40<=v<0x60 for row in self.m.text_rows() for v in row))
        self.assertFalse(self.m.bus.visible_text_write_violations)

    def hud_frame(self):
        """Execute the formatter and flip, checking only the hidden page is written."""
        page = self.m.state()['display_page_hi'] ^ 0x60
        self.set('draw_page_hi', page)
        self.set('render_page_index', int(page == 0x40))
        self.call('full_hud_draw')
        self.call('present_frame')
        rows = [self.decode_text(row) for row in self.m.text_rows()]
        for index,row in enumerate(rows):
            word = OUTCOME_WORDS.get(self.m.bus.ram[self.m.symbols['message_id']], '')
            suffix=(word.rjust(40) if index==0 and self.m.state()['game_mode']==0 else ' '*40)
            self.assertEqual(row[40:],suffix if self.video=='dhgr' else '')
        self.assertFalse(self.m.bus.visible_text_write_violations)
        return [row[:40] for row in rows]

    def test_gameplay_hud_original_room_descriptions(self):
        self.set('game_mode', 0);self.set('room_light', 3)
        source = Source()
        def phrase(address):return source.read(address, 40).split(b'\\', 1)[0].decode('ascii')
        def expected(number, geometry, pit):
            # Independent transcription of B2 4150-4170, including NP=1 priority.
            special = (23051 if number == 1 else 23219 if pit else
                       23090 if number == 63 else 23074 if number in (62, 33) else None)
            if special:return ['Vous etes ' + phrase(special), '']
            kind = {0:23111, 1:23128, 3:23143}.get(geometry)
            floor = 23160 if number < 9 else 23181 if number > 57 else 23199
            return ['Vous etes ' + (phrase(kind) if kind else ''), phrase(floor)]
        cases = [(n, Room.decode(self.world, n).geometry, 0) for n in range(64)]
        cases += [(n, 3, 1) for n in (1, 12, 33, 63)]
        for number, geometry, pit in cases:
            self.set('current_room', number);self.set('room_geometry', geometry);self.set('in_pit', pit)
            self.set('message_id',0)
            for _ in range(2):
                rows = self.hud_frame()
                self.assertEqual(rows[:2], [r.ljust(40) for r in expected(number, geometry, pit)],
                                 (number, geometry, pit))
            original=expected(number,geometry,pit)
            feedback=([original[0][:10].ljust(30)+'Impossible',original[0][10:].ljust(40)]
                      if not original[1] else
                      [original[0].ljust(30)+'Impossible',original[1].ljust(40)])
            if self.video=='dhgr':feedback=[line.ljust(40) for line in original]
            self.set('message_id',1)
            for _ in range(2):
                self.assertEqual(self.hud_frame()[:2],feedback,(number,geometry,pit))
                self.assertEqual(self.m.text_rows()[0][-10:],b'\x09mpossible')

    def test_gameplay_hud_stats_and_hand_names(self):
        self.m.frame(13);self.m.frame(ord('1'))
        hands = [(6, 'Pied de biche'), (9, 'Clef en fer'), (8, 'Clef en or'),
                 (10, 'Une fiole'), (1, 'Torche'), (0, '')]
        for energy, points, gold in [(10000, 0, 500), (9999, 17, 310), (100, 1000, 200),
                                     (99, 65535, 65535), (0, 0, 0), (-1, 0, 0)]:
            self.word('energy', energy & 65535);self.word('points', points);self.word('gold', gold)
            for item, name in hands:
                self.set('held_item', item)
                for _ in range(2):
                    rows = self.hud_frame()
                    self.assertEqual(rows[2], ('Force: %3d%%    Points: %5d' %
                                              (max(energy, 0)//100, points)).ljust(40))
                    self.assertEqual(rows[3], ("Pieces d'or: %5d  Main: %s" % (gold, name)).ljust(40))
                    self.assertEqual(rows[:2], ['Vous etes dans une salle'.ljust(40),
                                               'au rez-de-chaussee.'.ljust(40)])
        self.word('energy', 9900);self.word('gold', 500)
        self.m.frame()
        (self.directory/'room12-hud.png').write_bytes(self.m.screen_png())

    def test_impossible_actions_persist_until_next_command(self):
        self.m.frame(13);self.m.frame(ord('1'))
        def rows():
            return [self.decode_text(row[:40]) for row in self.m.text_rows()]
        description = rows()[0]
        # Room 12, empty inventory and neutral facing: none of these actions
        # can succeed. Exercise real keyboard dispatch, including lower case.
        for key in 'pOBGSLT123456':
            with self.subTest(key=key):
                self.m.frame(ord(key))
                self.assertEqual(self.m.state()['last_event'],7)
                pages=set()
                for _ in range(3):
                    text=rows();pages.add(self.m.state()['display_page_hi'])
                    first=description if self.video=='dhgr' else description[:30]+'Impossible'
                    self.assertEqual(text[:2],[first,'au rez-de-chaussee.'.ljust(40)])
                    self.assertEqual(self.m.text_rows()[0][-10:],b'\x09mpossible')
                    self.assertIn('Force:',text[2]);self.assertIn('Points:',text[2])
                    self.assertEqual(text[3],"Pieces d'or:   500  Main:".ljust(40))
                    self.m.frame() # no key must not dismiss the feedback
                self.assertEqual(pages,{0x20,0x40})
                self.m.frame(32)
                for _ in range(2):
                    self.assertEqual(rows()[1],'au rez-de-chaussee.'.ljust(40))
                    self.assertEqual(rows()[0],description)
                    self.assertNotIn('Impossible',self.debug_text())
                    self.m.frame()
        self.m.frame(ord('P'))
        (self.directory/'action-impossible.png').write_bytes(self.m.screen_png())
        self.m.frame(ord('H'));self.m.frame();self.m.frame(32)
        self.assertEqual(self.m.text_rows()[0][-10:],b'\x09mpossible') # help pauses feedback too
        self.m.frame(ord('0')) # successful empty-hand selection dismisses it
        self.assertEqual(rows()[1],'au rez-de-chaussee.'.ljust(40))
        self.assertEqual(self.m.bus.ram[self.m.symbols['message_id']],0)
        self.assertFalse(self.m.bus.visible_write_violations)
        self.assertFalse(self.m.bus.visible_text_write_violations)

    def test_impossible_feedback_in_special_rooms_and_darkness(self):
        self.set('game_mode',0)
        for number,pit in [(1,0),(33,0),(62,0),(63,0),(23,1),(9,0)]:
            with self.subTest(room=number,pit=pit):
                self.set('current_room',number);self.set('in_pit',pit)
                self.set('message_id',0);self.set('pit_wait',0)
                self.call('world_load_scene');self.call('draw_scene');self.call('present_frame')
                def rows():
                    text=[self.decode_text(row[:40])
                          for row in self.m.text_rows(all_rows=True)]
                    return text[8:12] if self.m.bus.switches['TEXT'] else text[20:24]
                description=rows()[:2]
                self.m.frame(ord('G')) # no rope: also refused inside an oubliette
                for _ in range(2):
                    expected=([description[0][:10].ljust(30)+'Impossible',description[0][10:].strip().ljust(40)]
                              if not description[1].strip() else
                              [description[0][:30]+'Impossible',description[1]])
                    if self.m.bus.switches['80COL']:expected=description
                    self.assertEqual(rows()[:2],expected)
                    raw=self.m.text_rows(all_rows=True)[8 if self.m.bus.switches['TEXT'] else 20]
                    self.assertEqual(raw[-10:],b'\x09mpossible')
                    self.assertIn('Force:',rows()[2]);self.assertIn("Pieces d'or:",rows()[3])
                    self.m.frame()
                if number==9:
                    self.assertEqual(self.m.bus.switches['TEXT'],1)
                    self.assertIn('Il fait noir ici !',self.debug_text())
                self.m.frame(ord('0'))
                self.assertNotIn('Impossible',''.join(rows()))
        self.assertFalse(self.m.bus.visible_write_violations)
        self.assertFalse(self.m.bus.visible_text_write_violations)

    def test_light_feedback_distinguishes_request_from_automatic_attempt(self):
        self.m.frame(13);self.m.frame(ord('1'))
        self.m.frame(ord('T')) # no torch and not beside a wall fixture
        self.assertIn('Impossible',self.debug_text())
        self.set('actor_x',7);self.set('actor_y',141);self.set('facing',2)
        self.set('held_item',1);self.set('torches',1);self.word('torch_life',250)
        self.m.frame(ord('T'))
        self.assertEqual(self.m.bus.ram[0x12A0+12]&1,1)
        self.assertEqual(self.m.bus.ram[self.m.symbols['message_id']],6)
        self.assertNotIn('Impossible',self.debug_text())
        # A later failed request must not inherit the previous success marker.
        self.set('actor_x',19)
        self.m.frame(ord('T'))
        self.assertIn('Impossible',self.debug_text())
        self.m.frame(32)
        events=len(self.m.events())
        self.call('full_light') # automatic jump-apex probe: failure is harmless
        self.assertEqual(self.m.bus.ram[self.m.symbols['message_id']],0)
        self.assertEqual(len(self.m.events()),events)
        self.m.frame()
        self.assertNotIn('Impossible',self.debug_text())
        self.assertFalse(self.m.bus.visible_write_violations)
        self.assertFalse(self.m.bus.visible_text_write_violations)

    def test_help_pauses_walking_and_staged_actions(self):
        self.m.frame(13);self.m.frame(ord('1'));self.m.frame()
        names = ['actor_x','actor_y','facing','pose','walking','walk_phase','frame_id',
                 'tick_lo','tick_hi','action_kind','action_phase','enemy_phase',
                 'pit_wait','held_item','torch_life','energy','rng_state']
        def snapshot():
            return ({n:self.m.bus.ram[self.m.symbols[n]] for n in names},
                    bytes(self.m.bus.ram[0x1000:0x1340]))
        for action in [0,3]:
            self.set('action_kind',action);self.set('action_phase',1)
            self.set('walking',int(action==0));self.set('held_item',1)
            self.word('torch_life',250)
            self.call('draw_scene');self.call('present_frame')
            graphics=self.m.displayed_page();before=snapshot()
            self.m.frame(ord('H'))
            self.assertEqual(self.m.state()['game_mode'],10)
            self.assertEqual((self.m.bus.switches['TEXT'],self.m.bus.switches['80COL']),(1,0))
            text=''.join(bytes(v&127 for v in row).decode('ascii') for row in self.m.text_rows(all_rows=True))
            for command in ['Commandes','Espace: Arret','Q: Suicide','T: Allumer',
                            'Clef en fer','Clef en or','Pied de biche']:
                self.assertIn(command,text)
            (self.directory/'help.png').write_bytes(self.m.screen_png())
            for _ in range(3):self.m.frame()
            # R must dismiss help, not trigger the legacy reset shortcut.
            self.m.frame(ord('R'))
            self.assertEqual(self.m.state()['game_mode'],0)
            after=snapshot()
            self.assertEqual(before[0],after[0])
            # UI bookkeeping/raw key are outside the gameplay comparison.
            for start,end in [(0x1000,0x1301),(0x1302,0x1333),(0x1334,0x133E)]:
                self.assertEqual(self.m.bus.ram[start:end],before[1][start-0x1000:end-0x1000])
            self.assertEqual(self.m.displayed_page(),graphics)
            self.assertEqual((self.m.bus.switches['TEXT'],self.m.bus.switches['MIXED']),(0,1))
        self.assertFalse(self.m.bus.visible_write_violations)
        self.assertFalse(self.m.bus.visible_text_write_violations)

    def test_help_returns_to_each_modal_page_and_name_input(self):
        for mode in [1,2,3,4,5,6,7,8,9,11]:
            with self.subTest(mode=mode):
                self.set('game_mode',mode);self.set('reading_page',1)
                self.call('draw_scene');self.call('present_frame')
                before=(self.m.state()['gold'],self.m.state()['current_room'],
                        self.m.bus.ram[self.m.symbols['reading_page']],
                        self.m.bus.ram[self.m.symbols['name_count']])
                self.m.frame(ord('?'))
                self.assertEqual(self.m.state()['game_mode'],10)
                self.m.frame(ord('1')) # consumed, no purchase/entry/reading advance
                self.assertEqual(self.m.state()['game_mode'],mode)
                after=(self.m.state()['gold'],self.m.state()['current_room'],
                       self.m.bus.ram[self.m.symbols['reading_page']],
                       self.m.bus.ram[self.m.symbols['name_count']])
                self.assertEqual(after,before)
                self.assertEqual(self.m.bus.switches['TEXT'],int(mode!=9))
        self.set('game_mode',8)
        self.m.frame(ord('H'))
        self.assertEqual(self.m.state()['game_mode'],8)
        self.assertEqual(self.m.bus.ram[self.m.symbols['player_name']],ord('H'))
        self.assertFalse(self.m.bus.visible_write_violations)
        self.assertFalse(self.m.bus.visible_text_write_violations)

    def test_help_in_darkness_and_during_oubliette_recovery(self):
        for pit in [0,1]:
            self.set('game_mode',0);self.set('current_room',23 if pit else 9)
            self.set('in_pit',pit);self.set('pit_wait',pit);self.set('held_item',0)
            self.call('world_load_scene');self.call('draw_scene');self.call('present_frame')
            before=bytes(self.m.bus.ram[0x1300:0x1333])
            self.m.frame(ord('?'));self.m.frame();self.m.frame(ord('A'))
            self.assertEqual(self.m.state()['game_mode'],0)
            self.assertEqual(bytes(self.m.bus.ram[0x1300:0x1333]),before)
            self.assertEqual(self.m.bus.switches['TEXT'],int(not pit))
            self.assertEqual(self.m.bus.ram[self.m.symbols['pit_wait']],pit)
        self.assertFalse(self.m.bus.visible_write_violations)
        self.assertFalse(self.m.bus.visible_text_write_violations)

    def debug_text(self):
        return '\n'.join(self.decode_text(row)
                         for row in self.m.text_rows(all_rows=True))

    def map_expected(self, page, number):
        from tools.resources import row_offset
        from tools.text_font import glyph
        data=(self.directory/('resources/map-%d.bin'%page)).read_bytes()
        main=bytearray(data)
        if 9<=number<58:
            actual_page=0;x=14+35*(6-(number-9)%7);y=19+20*((number-9)//7)
        elif number<9:
            actual_page=1
            cx,cy={8:(0,0),1:(1,0),2:(2,0),7:(0,1),0:(1,1),3:(2,1),6:(0,2),5:(1,2),4:(2,2)}[number]
            x,y=14+35*cx,25+28*cy
        else:
            actual_page=1;x=14+35*(4+(number-58)%3);y=25+28*((number-58)//3)
        if page==actual_page:
            # Independent transcription: filled face, black eyes and smile.
            smiley=['0011100','0111110','1101011','1111111','1011101',
                    '1100011','1111111','0111110','0011100']
            for j,row in enumerate(smiley):
                for i,value in enumerate(row):
                    if value=='1':
                        xx=x+21+i;main[row_offset(y+2+j)+xx//7]|=1<<(xx%7)
        pit=self.m.bus.ram[self.m.symbols['in_pit']]
        for col,ch in [(14,str(number//10)),(15,str(number%10)),(35,'X' if pit else '-')]:
            for j,bits in enumerate(glyph(ch)):
                main[row_offset(164+j)+col]=sum(1<<i for i in range(5) if bits&(16>>i))
        return bytes(main)

    def test_debug_map_all_rooms_initial_content_and_live_position(self):
        self.m.frame(13);self.m.frame(ord('1'));self.m.frame(4)
        world=bytes(self.m.bus.ram[0x1000:0x1200])
        report=json.loads((self.directory/'resources/maps.json').read_text())
        cells=report['cells'];self.assertEqual([c['room'] for c in cells],list(range(64)))
        self.assertEqual(report['marker']['kind'],'smiley')
        for n,item in {1:'book',13:'vial',28:'ring',30:'iron_key',35:'scroll',58:'gold',59:'lead_eagle',61:'gold_key',62:'diamond',63:'golden_eagle'}.items():
            self.assertEqual(cells[n]['item'],item,n)
        self.assertTrue(all(cells[n]['secret'] for n in [0,11,38,49,51,63]))
        self.assertTrue(cells[23]['trap']);self.assertTrue(cells[27]['dark'])
        pairs={tuple(pair) for pair in report['drawn_door_pairs']}
        self.assertEqual(len(pairs),58)
        for edge in report['directed_links']:
            room=Room.decode(self.world,edge['from']);facing=edge['facing']
            target,arrival=room.transition(facing)
            self.assertEqual(edge['lock'],room.fields[9-facing])
            self.assertEqual(edge['arrival'],arrival)
            if edge['exterior']:
                self.assertEqual((room.number,facing,edge['to']),(12,3,None))
                continue
            self.assertEqual(edge['to'],target)
            if 9<=room.number<58 and 9<=target<58 and edge['type']!='secret':
                self.assertIn(tuple(sorted((room.number,target))),pairs)
        for pair in pairs:
            self.assertTrue(any(tuple(sorted((e['from'],e['to'])))==pair
                                for e in report['directed_links'] if e['to'] is not None))
        self.assertEqual(report['bytes'],3*8192)
        self.assertIn('280x192',report['video'])
        for page in range(3):
            raster=(self.directory/('resources/map-%d.bin'%page)).read_bytes()
            self.assertEqual(len(raster),8192)
            self.assertFalse(any(v&128 for v in raster))
            self.assertTrue(any(raster[row_offset(191):row_offset(191)+40]))
        for c in cells:
            self.assertEqual((c['x']+21)%7,0)
            raster=(self.directory/('resources/map-%d.bin'%c['page'])).read_bytes()
            for y in range(c['y']+2,c['y']+11):
                self.assertEqual(raster[row_offset(y)+(c['x']+21)//7],0,
                                 'smiley must not obscure numbers, contents or doorways')
        aux_frames=bytes(self.m.bus.aux[0x2000:0x6000])
        # All pages use full-screen MAIN HGR, even in the DHGR game edition.
        self.m.frame(ord('3'))
        for page,name in enumerate(['ground','other','legend']):
            if page:self.m.frame(ord('1')+page)
            for _ in range(2):
                self.assertEqual(self.m.displayed_page(),self.map_expected(page,12))
                self.assertEqual((self.m.bus.switches['TEXT'],self.m.bus.switches['MIXED'],
                                  self.m.bus.switches['80COL'],self.m.bus.switches['DHIRES']),(0,0,0,0))
                self.assertEqual(bytes(self.m.bus.aux[0x2000:0x6000]),aux_frames)
                self.m.frame()
            (self.directory/('debug-map-%s.png'%name)).write_bytes(self.m.screen_png())
            # Both hidden buffers now contain this static page: no more disk or
            # graphics writes are needed while it remains open.
            self.m.bus.io.clear();self.m.bus.bank_graphics_writes.clear();self.m.frame()
            self.assertFalse(self.m.bus.motor)
            self.assertFalse(self.m.bus.bank_graphics_writes)
        # Exercise the native marker for all 64 positions without re-reading the
        # same disk sectors 64 times. Base images are the packaged native bytes.
        for number in range(64):
            page=0 if 9<=number<58 else 1
            data=(self.directory/('resources/map-%d.bin'%page)).read_bytes()
            self.set('current_room',number);self.set('game_mode',13+page)
            hidden=self.m.state()['display_page_hi']^0x60
            self.set('draw_page_hi',hidden);self.set('render_page_index',int(hidden==0x40))
            self.m.bus.ram[hidden*256:hidden*256+8192]=data[:8192]
            self.call('full_map_mark');self.call('present_frame')
            self.assertEqual(self.m.displayed_page(),self.map_expected(page,number),number)
        self.m.frame(27);self.m.frame(ord('1'));self.m.frame(ord('3'))
        self.assertEqual(self.m.state()['objectives'],0)
        self.assertEqual(self.m.displayed_page(),self.map_expected(1,63))
        self.assertEqual(bytes(self.m.bus.ram[0x1000:0x1200]),world)
        self.assertFalse(self.m.bus.visible_write_violations)
        self.assertFalse(self.m.bus.visible_text_write_violations)

    def test_debug_map_navigation_pauses_and_returns_to_menu_or_game(self):
        self.m.frame(13);self.m.frame(ord('1'));self.m.frame()
        self.set('held_item',1);self.word('torch_life',250);self.set('walking',1)
        before=self.m.state();world=bytes(self.m.bus.ram[0x1000:0x1300])
        baseline=bytes(self.m.bus.ram[0xA000:0xC000]);aux=bytes(self.m.bus.aux[0x6000:0xC000])
        self.m.frame(4);self.m.frame(ord('3'))
        self.assertEqual((self.m.state()['game_mode'],self.m.bus.switches['TEXT']),(13,0))
        self.assertEqual((self.m.bus.switches['MIXED'],self.m.bus.switches['80COL'],
                          self.m.bus.switches['DHIRES']),(0,0,0))
        for key,mode in [(32,14),(13,15),(32,13),(ord('R'),13),(None,13),(27,12)]:
            self.m.frame(key);self.assertEqual(self.m.state()['game_mode'],mode)
        self.m.frame(ord('3'));self.m.frame(4)
        self.assertEqual((self.m.bus.switches['MIXED'],self.m.bus.switches['80COL'],
                          self.m.bus.switches['DHIRES']),(1,int(self.video=='dhgr'),int(self.video=='dhgr')))
        after=self.m.state()
        for name in before.keys()-{'display_page_hi','draw_page_hi','key_action'}:
            self.assertEqual(after[name],before[name],name)
        self.assertEqual(bytes(self.m.bus.ram[0x1000:0x1300]),world)
        self.assertEqual(bytes(self.m.bus.ram[0xA000:0xC000]),baseline)
        self.assertEqual(bytes(self.m.bus.aux[0x6000:0xC000]),aux)
        # Both normal frame buffers must be rebuilt; returning must not expose
        # any map pixels or alter a pit/action to force a room reconstruction.
        images=[]
        for _ in range(2):
            self.call('draw_scene');self.call('present_frame');images.append(self.m.displayed_page())
        self.assertEqual(images[0],images[1])
        self.assertEqual(self.m.bus.ram[self.m.symbols['terrain_pending']],0)
        self.set('current_room',23);self.set('in_pit',1);self.set('pit_wait',1)
        self.call('world_load_scene');pit_baseline=bytes(self.m.bus.ram[0xA000:0xC000])
        self.m.frame(4);self.m.frame(ord('3'))
        self.assertEqual(self.m.displayed_page(),self.map_expected(0,23))
        self.assertEqual(self.m.state()['in_pit'],1)
        self.m.frame(32);self.assertEqual(self.m.state()['game_mode'],14)
        self.assertEqual(self.m.displayed_page(),self.map_expected(1,23))
        self.m.frame(27);self.assertEqual(self.m.state()['game_mode'],12)
        self.m.frame(4)
        self.assertEqual(self.m.state()['in_pit'],1)
        self.assertEqual(bytes(self.m.bus.ram[0xA000:0xC000]),pit_baseline)
        # Darkness resumes its ordinary text panel; a later torch display still
        # obtains a complete game frame, never the previously cached map.
        self.set('in_pit',0);self.set('pit_wait',0);self.set('current_room',9)
        self.set('held_item',0);self.set('walking',0)
        self.call('world_load_scene');self.call('draw_scene');self.call('present_frame')
        self.assertEqual(self.m.bus.switches['TEXT'],1)
        self.m.frame(4);self.m.frame(ord('3'));self.m.frame(4)
        self.assertEqual(self.m.bus.switches['TEXT'],1)
        self.set('held_item',1)
        for _ in range(2):self.call('draw_scene');self.call('present_frame')
        self.assertEqual(self.m.bus.switches['TEXT'],0)
        self.assertEqual(self.m.bus.ram[self.m.symbols['terrain_pending']],0)
        self.assertFalse(self.m.bus.visible_write_violations)
        self.assertFalse(self.m.bus.visible_text_write_violations)

    def test_debug_menu_is_hidden_modal_and_freezes_gameplay(self):
        # The shortcut cannot skip title/name/exterior setup.
        self.m.frame(4)
        self.assertEqual(self.m.state()['game_mode'],8)
        self.m.frame(13);self.m.frame(4)
        self.assertEqual(self.m.state()['game_mode'],1)
        self.m.frame(ord('1'));self.m.frame()
        self.set('walking',1);self.set('action_kind',3);self.set('action_phase',2)
        self.set('held_item',1);self.word('torch_life',250)
        self.call('update_frame')
        for _ in range(2):
            self.call('draw_scene');self.call('present_frame')
        before=self.m.state();world=bytes(self.m.bus.ram[0x1000:0x1300])
        def graphics_hash():
            page=self.m.displayed_page()
            return digest(b''.join(page) if isinstance(page,tuple) else page)
        graphics=graphics_hash()
        self.m.frame(4)
        self.assertEqual((self.m.state()['game_mode'],self.m.bus.switches['TEXT'],
                          self.m.bus.switches['80COL']),(12,1,0))
        self.assertIn('Menu de test',self.debug_text())
        self.assertIn('Salle actuelle: 12',self.debug_text())
        for key in [None,ord('R'),ord('?'),ord('H'),32]:self.m.frame(key)
        self.assertEqual(self.m.state()['game_mode'],12)
        self.m.frame(27)
        after=self.m.state()
        for name in before.keys()-{'display_page_hi','draw_page_hi','key_action'}:
            self.assertEqual(after[name],before[name],name)
        self.assertEqual(bytes(self.m.bus.ram[0x1000:0x1300]),world)
        self.assertEqual(graphics_hash(),graphics)
        self.assertEqual((self.m.bus.switches['TEXT'],self.m.bus.switches['MIXED']),(0,1))
        self.assertFalse(self.m.bus.visible_write_violations)
        self.assertFalse(self.m.bus.visible_text_write_violations)

    def test_debug_grants_every_inventory_category_without_economy_changes(self):
        self.m.frame(13);self.m.frame(ord('1'));self.m.frame()
        before={n:self.m.state()[n] for n in ['gold','points','energy','held_item','drain']}
        world=bytes(self.m.bus.ram[0x1000:0x1200])
        self.m.frame(4);self.m.frame(ord('1'))
        state=self.m.state()
        self.assertEqual([state[n] for n in ['vials','torches','ropes','crowbars']],[9]*4)
        self.assertEqual((state['possessions'],state['scrolls'],state['objectives']),(15,7,0))
        self.assertTrue(200<=state['torch_life']<=299)
        self.assertTrue(20<=self.m.bus.ram[self.m.symbols['bar_life']]<=39)
        self.assertEqual({n:state[n] for n in before},before)
        self.assertEqual(bytes(self.m.bus.ram[0x1000:0x1200]),world)
        self.assertEqual(state['room_dirty'],0)
        self.assertEqual(self.m.bus.ram[self.m.symbols['terrain_pending']],3)
        self.assertIn('Tous les objets ajoutes.',self.debug_text())
        (self.directory/'debug-menu.png').write_bytes(self.m.screen_png())
        self.m.frame(4)
        for code,held in zip(b'012345',[0,1,9,8,10,6]):
            self.m.frame(code)
            self.assertEqual(self.m.state()['held_item'],held)
        # Acquiring all quest objects deliberately enables the normal victory test.
        self.set('facing',3);self.call('full_transition')
        self.assertEqual(self.m.state()['game_mode'],6)
        self.assertFalse(self.m.bus.visible_write_violations)
        self.assertFalse(self.m.bus.visible_text_write_violations)

    def test_debug_room_input_rejects_invalid_and_supports_editing(self):
        self.m.frame(13);self.m.frame(ord('1'));self.m.frame()
        self.m.frame(4);self.m.frame(ord('2'))
        world=bytes(self.m.bus.ram[0x1000:0x1200])
        for keys in [b'\r',b'64\r',b'\x08\x0899\r',b'\x08\x08012\r']:
            for key in keys:self.m.frame(key)
            self.assertEqual((self.m.state()['game_mode'],self.m.state()['current_room']),(12,12))
            self.assertIn('Salle invalide',self.debug_text())
            self.assertEqual(bytes(self.m.bus.ram[0x1000:0x1200]),world)
        # Third digit was rejected. Backspace twice, R is ignored, zero is valid.
        for key in b'\x08\x08R0':self.m.frame(key)
        self.assertIn('Destination: 0_',self.debug_text())
        self.m.frame(13)
        self.assertEqual((self.m.state()['game_mode'],self.m.state()['current_room']),(0,0))
        self.assertEqual((self.m.state()['pose'],self.m.state()['walking'],self.m.state()['frame_id']),(0,0,0))
        # Cancel a partial request without changing room; Ctrl+D also closes.
        for key in [4,ord('2'),ord('6'),27,4,4]:self.m.frame(key)
        self.assertEqual((self.m.state()['game_mode'],self.m.state()['current_room']),(0,0))
        self.assertFalse(self.m.bus.visible_write_violations)
        self.assertFalse(self.m.bus.visible_text_write_violations)

    def test_debug_teleport_clears_transients_preserves_world_and_prepares_both_pages(self):
        # Independently check the bounded spawn scan has a clear foot cell in
        # every source room, including the six with an occupied center cell.
        for number in range(64):
            _,grid,_,_=self.constructor.scene(self.world,number,self.variation)
            self.assertIn(0,grid[21:35],number)
        self.m.frame(13);self.m.frame(ord('1'));self.m.frame()
        # A permanent lock/loot edit must survive teleportation.
        self.m.bus.ram[0x1100+14*4]=0
        for room in [6,7,23,63]:
            with self.subTest(room=room):
                self.set('in_pit',1);self.set('pit_wait',1)
                self.set('action_kind',3);self.set('action_phase',2)
                self.set('held_item',0);self.set('saved_item',1) # jump's saved torch
                self.set('enemy_kind',1);self.set('enemy_contact',1)
                self.set('hazard_active',1);self.set('walking',1)
                self.word('torch_life',250)
                before={n:self.m.state()[n] for n in ['energy','gold','points','rng_state']}
                world=bytes(self.m.bus.ram[0x1000:0x1200])
                self.m.frame(4);self.m.frame(ord('2'))
                for key in str(room).encode()+b'\r':self.m.frame(key)
                state=self.m.state()
                self.assertEqual((state['game_mode'],state['current_room'],state['held_item']),(0,room,1))
                self.assertEqual([state[n] for n in ['in_pit','action_kind','action_phase','enemy_kind','walking','pose','frame_id']],[0]*7)
                for name in ['pit_wait','enemy_contact','hazard_active']:
                    self.assertEqual(self.m.bus.ram[self.m.symbols[name]],0,name)
                self.assertEqual({n:state[n] for n in before},before)
                self.assertEqual(bytes(self.m.bus.ram[0x1000:0x1200]),world)
                _,grid,_,_=self.constructor.scene(world,room,self.variation)
                self.assertEqual(self.m.bus.ram[0x1200:0x1278],grid)
                self.assertEqual((state['actor_y'],grid[state['actor_x']+2]),(180,0))
                self.assertGreaterEqual(state['actor_x'],19)
                self.assertLessEqual(state['actor_x'],32)
                self.assertEqual(self.m.bus.switches['TEXT'],0)
                self.assertIn(self.m.bus.ram[self.m.symbols['terrain_pending']],[1,2])
                self.m.frame()
                self.assertEqual(self.m.bus.ram[self.m.symbols['terrain_pending']],0)
                if room==23:(self.directory/'debug-teleport-room23.png').write_bytes(self.m.screen_png())
        self.assertFalse(self.m.bus.visible_write_violations)
        self.assertFalse(self.m.bus.visible_text_write_violations)

    def test_transition_uses_original_link_and_arrival_bits(self):
        for number in range(64):
            room=Room.decode(self.world,number)
            for facing in range(4):
                self.set('current_room',number);self.set('facing',facing)
                self.set('game_mode',0)
                oldxy=(self.m.state()['actor_x'],self.m.state()['actor_y'])
                self.call('full_transition')
                if number==12 and facing==3:
                    self.assertEqual(self.m.state()['game_mode'],1)
                    continue
                dest,arrival=room.transition(facing)
                self.assertEqual(self.m.state()['current_room'],dest,(number,facing))
                self.assertEqual(self.m.state()['facing'],0 if arrival==3 else arrival,(number,facing))
                if arrival==3:
                    self.assertEqual((self.m.state()['actor_x'],self.m.state()['actor_y']),oldxy)

    def test_one_shot_rewards_and_quest_eagle_prerequisite(self):
        self.set('current_room',14)
        self.m.bus.ram[0x1000+256+14*4]=(5<<3)
        self.call('world_load_scene')
        for k,v in [('actor_x',5),('actor_y',160),('facing',1),('pose',5)]:self.set(k,v)
        self.call('full_pickup');self.assertEqual(self.m.state()['vials'],1)
        self.assertEqual(self.m.state()['points'],7)
        self.call('full_pickup');self.assertEqual(self.m.state()['vials'],1)
        self.set('current_room',63);self.call('world_load_scene')
        for k,v in [('actor_x',27),('actor_y',160),('facing',1),('pose',1),('held_item',0)]:self.set(k,v)
        self.call('full_pickup');self.assertEqual(self.m.state()['objectives'],7)
        self.assertEqual(self.m.bus.ram[self.m.symbols['hazard_active']],1)
        self.set('possessions',8);self.call('full_pickup')
        self.assertEqual(self.m.state()['objectives'],3)
        self.assertEqual(self.m.state()['possessions'],0)
        self.assertEqual(self.m.state()['points'],1007)

    def test_walking_flips_restore_without_visible_writes(self):
        self.m.frame(13);self.m.frame(ord('1'))
        for k in [ord('K'),ord('K'),None,32,ord('A'),ord('N'),32]:self.m.frame(k)
        self.assertFalse(self.m.bus.visible_write_violations)
        self.assertFalse(self.m.bus.visible_text_write_violations)
        self.assertEqual(self.m.bus.speaker_accesses,0)

    def test_clues_display_original_content_and_advance(self):
        self.m.frame(13);self.m.frame(ord('1'))
        self.set('scrolls',7);self.set('objectives',6)
        self.m.frame(ord('L'))
        self.assertEqual(self.m.state()['game_mode'],4)
        def text():return ''.join(bytes(v&127 for v in row).decode('ascii') for row in self.m.text_rows(all_rows=True))
        self.assertIn('Der Reif',text())
        self.m.frame(32);self.assertIn('Der goldene',text())
        self.m.frame(32);self.assertIn('Der Adler',text())
        self.m.frame(32);self.assertIn('Stern',text())
        self.m.frame(32);self.assertEqual(self.m.state()['game_mode'],0)

    def test_room23_trap_recovery_rope_and_return(self):
        self.set('game_mode',0);self.set('current_room',23)
        self.call('world_load_scene')
        ordinary=bytes(self.m.bus.ram[0xA000:0xC000])
        for name,value in [('actor_x',7),('actor_y',180),('facing',1),('pose',1)]:self.set(name,value)
        self.m.frame(ord('K'))
        self.assertEqual((self.m.state()['actor_x'],self.m.state()['in_pit']),(8,0))
        self.m.frame()
        self.assertEqual(self.m.state()['current_room'],23)
        self.assertEqual(self.m.state()['in_pit'],1)
        self.assertEqual(self.m.state()['frame_id'],27)
        self.assertEqual(self.m.bus.ram[self.m.symbols['pit_wait']],1)
        self.assertNotEqual(bytes(self.m.bus.ram[0xA000:0xC000]),ordinary)
        expected=bytearray(120);expected[11:14]=expected[29:32]=bytes([128]*3);expected[41:72]=bytes([255]*31)
        self.assertEqual(self.m.bus.ram[0x1200:0x1278],expected)
        self.assertTrue(self.m.bus.ram[0x1000+256+23*4]&64)
        self.assertGreater(self.m.state()['drain'],1) # multiply before cent rounding
        (self.directory/'room23-pit.png').write_bytes(self.m.screen_png())
        self.m.frame(32);self.assertEqual(self.m.state()['frame_id'],27)
        self.m.frame(ord('A'));self.assertEqual(self.m.bus.ram[self.m.symbols['pit_wait']],0)
        self.m.frame(32);self.assertEqual((self.m.state()['pose'],self.m.state()['frame_id']),(3,3))
        self.m.frame(ord('G'));self.assertEqual(self.m.state()['action_kind'],0)
        self.set('ropes',1);self.m.frame(ord('G'))
        for _ in range(7):self.m.frame()
        self.assertEqual((self.m.state()['in_pit'],self.m.state()['current_room'],self.m.state()['ropes']),(0,23,0))
        self.assertEqual((self.m.state()['actor_x'],self.m.state()['actor_y']),(13,180))
        self.assertNotEqual(self.m.bus.ram[0x1200:0x1278],expected)
        self.assertFalse(self.m.bus.visible_write_violations)
        self.assertFalse(self.m.bus.visible_text_write_violations)

    def test_half_steps_and_continuous_depth_bands(self):
        self.set('current_room',12);self.set('game_mode',0)
        self.call('world_load_scene')
        for facing,dx,dy in [(0,0,5),(1,1,0),(2,-1,0),(3,0,-5)]:
            for name,value in [('actor_x',19),('actor_y',160),('facing',facing),('pose',facing),
                               ('walking',1),('key_action',255),('raw_key',255)]:self.set(name,value)
            self.call('game_tick')
            self.assertEqual((self.m.state()['actor_x'],self.m.state()['actor_y']),(19+dx,160+dy))
        # A formerly skipped y=165 must see the same furniture as y=160.
        self.m.bus.ram[0x1200:0x1278]=bytes(120)
        self.m.bus.ram[0x1200+40+22]=151
        for y in [155,160,165,170]:
            self.set('actor_x',19);self.set('actor_y',y);self.set('facing',1)
            self.call('collision_probe');self.assertEqual(self.m.state()['blocked'],1,y)
        for y in [150,175,180]:
            self.set('actor_y',y);self.call('collision_probe')
            self.assertEqual(self.m.state()['blocked'],0,y)

    def test_portals_require_approaching_the_visible_door(self):
        self.set('current_room',12);self.set('game_mode',0);self.call('world_load_scene')
        for name,value in [('actor_x',31),('actor_y',180),('facing',1),('pose',1),
                           ('walking',1),('raw_key',255),('key_action',255)]:self.set(name,value)
        for x in [32,33,34]:
            self.call('game_tick')
            self.assertEqual((self.m.state()['current_room'],self.m.state()['actor_x']),(12,x))
        self.call('game_tick')
        self.assertEqual((self.m.state()['current_room'],self.m.state()['actor_x']),(11,2))
        self.set('current_room',23);self.call('world_load_scene')
        for name,value in [('actor_x',7),('actor_y',180),('facing',2),('pose',2),('walking',1)]:self.set(name,value)
        for x in [6,5,4,3,2]:
            self.call('game_tick')
            self.assertEqual((self.m.state()['current_room'],self.m.state()['actor_x']),(23,x))
        self.call('game_tick');self.assertEqual(self.m.state()['current_room'],24)
        # A locked upper door can only be opened near its visible threshold.
        self.set('current_room',12);self.set('game_mode',0);self.call('world_load_scene')
        self.set('actor_x',19);self.set('actor_y',140);self.set('facing',3)
        self.call('full_open');self.assertEqual(self.m.state()['game_mode'],0)
        self.set('walking',1)
        for y in [135,130,125]:
            self.call('game_tick');self.assertEqual(self.m.state()['actor_y'],y)
        self.call('game_tick');self.assertEqual(self.m.state()['walking'],0)
        self.call('full_open');self.assertEqual(self.m.state()['game_mode'],1)
        # Source action heights need clamping rather than skipping the new plane.
        self.set('game_mode',0);self.set('actor_y',126);self.set('walking',1)
        self.call('game_tick');self.assertEqual(self.m.state()['actor_y'],125)

    def test_walk_up_to_and_pick_up_all_floor_treasures(self):
        for treasure in range(1,8):
            for facing,start_x,start_y,expected_x,expected_y in [(1,4,160,5,160),
                    (2,16,160,12 if treasure==7 else 9,160),(0,7,145,7,150)]:
                with self.subTest(treasure=treasure,facing=facing):
                    # Real room 35, with only its item kind varied; walls/furniture
                    # and the original semantic marks are constructed natively.
                    self.set('current_room',35);self.set('game_mode',0)
                    self.m.bus.ram[0x1100+35*4]=4|(treasure<<3)
                    self.set('held_item',0);self.call('world_load_scene')
                    for name,value in [('actor_x',start_x),('actor_y',start_y),('facing',facing),
                            ('pose',facing),('walking',1),('raw_key',255),('key_action',255)]:self.set(name,value)
                    for _ in range(20):
                        self.call('game_tick')
                        if not self.m.state()['walking']:break
                    self.assertEqual((self.m.state()['actor_x'],self.m.state()['actor_y']),
                                     (expected_x,expected_y))
                    self.m.frame(ord('A'));self.m.frame(ord('P'))
                    self.assertEqual(self.m.bus.ram[0x1100+35*4]&56,0)
                    self.assertEqual(self.m.bus.ram[self.m.symbols['room_treasure']],0)

    def test_narrow_probes_cannot_escape_the_perspective_walls(self):
        self.set('current_room',12);self.set('game_mode',0);self.call('world_load_scene')
        # Clear semantic sentinels: the geometric envelope must still confine feet.
        self.m.bus.ram[0x1200:0x1278]=bytes(120)
        self.set('actor_x',3);self.set('actor_y',175);self.set('facing',3)
        self.call('collision_probe');self.assertEqual(self.m.state()['blocked'],1)
        self.set('actor_x',33);self.call('collision_probe');self.assertEqual(self.m.state()['blocked'],1)
        self.set('actor_x',19);self.call('collision_probe');self.assertEqual(self.m.state()['blocked'],0)

    def test_chest_and_quest_remain_reachable_with_reduced_clearance(self):
        self.set('current_room',1);self.set('game_mode',0);self.call('world_load_scene')
        for name,value in [('actor_x',30),('actor_y',165),('facing',1),('pose',1)]:self.set(name,value)
        self.call('full_pickup');self.assertEqual(self.m.state()['objectives'],6)
        self.set('actor_x',26);self.set('objectives',7)
        self.call('full_pickup');self.assertEqual(self.m.state()['objectives'],7)
        self.set('current_room',35)
        self.m.bus.ram[0x1100+35*4]=7|(2<<3)
        self.call('world_load_scene');self.set('actor_x',30);self.set('actor_y',160)
        self.set('held_item',6);self.set('crowbars',1);self.set('bar_life',30)
        self.call('full_open');self.assertEqual(self.m.bus.ram[self.m.symbols['chest_open']],1)
        self.call('full_pickup');self.assertEqual(self.m.bus.ram[0x1100+35*4]&56,0)

    def test_secret_passages_open_and_traverse_all_source_links(self):
        from tools import mono
        from tools.video_layout import source_y
        for number,destination in [(0,63),(11,51),(38,49),(49,38),(51,11),(63,0)]:
            with self.subTest(room=number,destination=destination):
                for name,value in [('game_mode',0),('current_room',number),('passage',0),
                                   ('in_pit',0),('walking',0),('pose',3),('facing',3),
                                   ('actor_x',19),('actor_y',160),('possessions',2),('held_item',0)]:self.set(name,value)
                self.call('world_load_scene')
                closed=[bytearray(self.m.bus.ram[0xA000:0xC000])]
                if self.video=='dhgr':closed.append(bytearray(self.m.bus.aux[0xA000:0xC000]))
                world=bytes(self.m.bus.ram[0x1000:0x1200])
                self.m.frame(0x0B)
                for _ in range(3):self.m.frame() # approach from y=160 to y=140
                self.m.frame(32)
                self.assertEqual((self.m.state()['actor_x'],self.m.state()['actor_y']),(19,140))
                self.m.frame(ord('3'));self.assertEqual(self.m.state()['held_item'],8)
                self.m.frame(ord('O'))
                self.assertEqual(self.m.bus.ram[self.m.symbols['passage']],1)
                self.assertEqual(self.m.state()['current_room'],number)
                self.assertNotIn('Impossible',self.debug_text())
                expected=[bytearray(bank) for bank in closed]
                # Independent final-opening raster: source bounds from B2 10980,
                # target fills the intervening scanlines rather than animating them.
                for sy in range(98,121):
                    y=source_y(sy)
                    if source_y(sy+1)==y:continue
                    for x in range(114,131):
                        if self.video=='mono':mono.put(expected[0],x,y,int(sy==98))
                        else:dhgr.put_cell(*expected,10+x//2,y,15 if sy==98 else 0)
                actual=[bytes(self.m.bus.ram[0xA000:0xC000])]
                if self.video=='dhgr':actual.append(bytes(self.m.bus.aux[0xA000:0xC000]))
                self.assertEqual(actual,[bytes(bank) for bank in expected])
                self.assertNotEqual(actual,[bytes(bank) for bank in closed])
                self.assertEqual(bytes(self.m.bus.ram[0x1000:0x1200]),world)
                def margin(banks):
                    # This left edge of the opening is outside the actor's x>=120
                    # footprint: compare actual displayed pixels on both pages.
                    if self.video=='dhgr':
                        return [dhgr.cells(*banks,source_y(y))[67:70] for y in range(98,121)]
                    from tools.resources import row_offset
                    return [bool(banks[0][row_offset(source_y(y))+(x+20)//7] & (1<<((x+20)%7)))
                            for y in range(98,121) for x in range(114,120)]
                for _ in range(2):
                    self.m.frame()
                    self.assertEqual(self.m.state()['possessions'],2) # key is not consumed
                    displayed=self.m.displayed_page()
                    self.assertEqual(margin(displayed if self.video=='dhgr' else [displayed]),margin(expected))
                self.m.frame(ord('O')) # already open: keep it open without a second attempt
                self.assertIn('Deja fait',self.debug_text())
                self.assertEqual(self.m.bus.ram[self.m.symbols['passage']],1)
                self.m.frame(ord('H'));self.m.frame(32)
                self.assertEqual(self.m.bus.ram[self.m.symbols['passage']],1)
                self.m.frame(0x0B) # standing: approach only, never traverse
                self.assertEqual(self.m.state()['current_room'],number)
                self.m.frame(32)
                if number==11:(self.directory/'secret-passage-open.png').write_bytes(self.m.screen_png())
                self.m.frame(ord('A'));self.m.frame(0x0B)
                state=self.m.state()
                self.assertEqual((state['current_room'],state['actor_x'],state['actor_y'],state['pose']),
                                 (destination,19,140,4))
                self.assertEqual(self.m.bus.ram[self.m.symbols['passage']],0)
                self.assertEqual(bytes(self.m.bus.ram[0x1000:0x1200]),world)
                ops=self.constructor.scene(world,destination,self.variation)[2]
                target=(bytes(self.m.bus.ram[0xA000:0xC000]),bytes(self.m.bus.aux[0xA000:0xC000]))
                if self.video=='mono':self.assertEqual(target[0],mono.scene_page(self.constructor,ops))
                else:self.assertEqual(target,scene_pages(self.constructor,ops))
        self.assertFalse(self.m.bus.visible_write_violations)
        self.assertFalse(self.m.bus.visible_text_write_violations)

    def test_secret_passage_guards_and_original_anchor(self):
        self.set('game_mode',0)
        cases=[(11,0,19,140,3),(11,9,19,140,3),(11,8,19,140,0),
               (11,8,13,140,3),(11,8,21,140,3),(11,8,19,120,3),(11,8,19,150,3),
               (9,8,19,140,3),(20,8,19,140,3),(46,8,19,140,3)]
        for number,item,x,y,facing in cases:
            with self.subTest(room=number,item=item,x=x,y=y,facing=facing):
                self.set('current_room',number);self.set('passage',0);self.call('world_load_scene')
                for name,value in [('held_item',item),('actor_x',x),('actor_y',y),('facing',facing)]:self.set(name,value)
                self.call('full_open')
                self.assertEqual(self.m.bus.ram[self.m.symbols['message_id']],1)
                self.assertEqual(self.m.bus.ram[self.m.symbols['passage']],0)
                self.assertEqual(self.m.state()['room_dirty'],0)
        self.set('current_room',11);self.call('world_load_scene')
        self.set('actor_x',19);self.set('actor_y',140);self.set('facing',3);self.set('pose',7)
        self.m.frame(0x0B) # closed fireplace cannot be traversed even while crouched
        self.assertEqual(self.m.state()['current_room'],11)
        self.set('actor_x',15);self.set('actor_y',140);self.set('held_item',8)
        self.m.frame(ord('O')) # exact original gold-key pose remains accepted
        self.assertEqual(self.m.bus.ram[self.m.symbols['passage']],1)
        self.m.frame(0x0B) # keyhole side is outside the central entry window
        self.assertEqual(self.m.state()['current_room'],11)
        self.assertFalse(self.m.bus.visible_write_violations)
        self.assertFalse(self.m.bus.visible_text_write_violations)

    def test_source_torch_flames_animate_on_both_pages_without_trails(self):
        self.set('current_room',12);self.set('game_mode',0);self.call('world_load_scene')
        original_rng=self.m.state()['rng_state'];baseline=(bytes(self.m.bus.ram[0xA000:0xC000]),bytes(self.m.bus.aux[0xA000:0xC000]))
        seen={0x2000:{},0x4000:{}}
        from tools.scenery import tile
        from tools.video_layout import source_y
        for tick in range(8):
            self.set('tick_lo',tick);self.call('draw_scene')
            page=self.m.state()['draw_page_hi']*256
            expected=[bytearray(v) for v in baseline]
            sid=36+((tick>>1)&1)
            s=tile(sprite(Source(),sid),13)
            for left in [24,210]:
                for j,row in enumerate(s['tile_rows']):
                    y=64+j;ty=source_y(y)
                    if source_y(y+1)==ty:continue
                    for k,v in enumerate(row):
                        if v:dhgr.put_cell(*expected,10+left//2+k,ty,0 if v==1 else 13 if v==2 else 9)
            for y in range(source_y(64),source_y(81)+1):
                for left in [22,115]:
                    actual=dhgr.cells(bytes(self.m.bus.ram[page:page+8192]),bytes(self.m.bus.aux[page:page+8192]),y)
                    wanted=dhgr.cells(*expected,y)
                    self.assertEqual(actual[left:left+9],wanted[left:left+9],(page,tick,y,left))
            image=(bytes(self.m.bus.ram[page:page+8192]),bytes(self.m.bus.aux[page:page+8192]))
            phase=(tick>>1)&1
            if phase in seen[page]:self.assertEqual(image,seen[page][phase])
            seen[page][phase]=image
            self.call('present_frame')
        self.assertTrue(all(len(v)==2 for v in seen.values()))
        self.assertEqual(self.m.state()['rng_state'],original_rng)
        self.assertEqual((bytes(self.m.bus.ram[0xA000:0xC000]),bytes(self.m.bus.aux[0xA000:0xC000])),baseline)
        self.assertFalse(self.m.bus.visible_write_violations)
        (self.directory/'room12-flames.png').write_bytes(self.m.screen_png())
        # An unlit fixture gets no flame; the carried torch still gets one.
        self.set('room_light',1);self.set('held_item',1);self.set('actor_y',180)
        self.call('world_load_scene');self.set('room_light',1)
        hand=[]
        for tick in [0,2,4]:
            self.set('tick_lo',tick);self.call('draw_scene');self.call('present_frame')
            hand.append(self.m.displayed_page())
        self.assertNotEqual(hand[0],hand[1]);self.assertEqual(hand[0],hand[2])

    def test_secret_cue_and_grille_padlocks_are_visible(self):
        from tools.video_layout import source_y
        from tools.scenery import SECRET
        self.set('current_room',0);self.set('game_mode',0);self.call('world_load_scene')
        main,aux=bytes(self.m.bus.ram[0xA000:0xC000]),bytes(self.m.bus.aux[0xA000:0xC000])
        x=10+((SECRET['curset_x']//6+1)*6)//2
        self.assertEqual(dhgr.cells(main,aux,source_y(106))[x:x+4],[0]*4)
        self.assertEqual(dhgr.cells(main,aux,source_y(103))[x:x+4],[5]*4)
        self.set('actor_y',180)
        self.call('draw_scene');self.call('present_frame')
        (self.directory/'room0-secret-grille.png').write_bytes(self.m.screen_png())
        self.set('current_room',20);self.call('world_load_scene')
        a,b=bytes(self.m.bus.ram[0xA000:0xC000]),bytes(self.m.bus.aux[0xA000:0xC000])
        self.assertNotEqual(dhgr.cells(a,b,source_y(106))[x:x+4],[0]*4)
        # Native golden lock body plus a black keyhole on a white grille.
        cells=dhgr.cells(a,b,source_y(119+29+5))
        left=10+216//2
        self.assertEqual(cells[left:left+4],[13,13,0,13])
        self.assertIn(15,dhgr.cells(a,b,source_y(140))[left:left+9])
        self.call('draw_scene');self.call('present_frame')
        (self.directory/'room20-grille.png').write_bytes(self.m.screen_png())

    def test_lighting_does_not_leave_an_unanimated_fixture(self):
        from tools.video_layout import source_y
        for room,both in [(12,True),(9,False)]:
            self.set('current_room',room);self.set('game_mode',0);self.call('world_load_scene')
            for name,value in [('actor_x',7),('actor_y',141),('facing',2),('pose',2),('held_item',1)]:self.set(name,value)
            self.call('full_light')
            self.assertEqual(self.m.bus.ram[0x12A0+room],1)
            baseline=(bytes(self.m.bus.ram[0xA000:0xC000]),bytes(self.m.bus.aux[0xA000:0xC000]))
            # Move the actor away so fixture checks cannot include the hand flame.
            self.set('actor_x',19);self.set('actor_y',180)
            phases=[]
            for tick in range(4):
                self.set('tick_lo',tick);self.call('draw_scene');self.call('present_frame')
                a,b=self.m.displayed_page()
                regions=[]
                for left in [22,115]:
                    regions.append(tuple(tuple(dhgr.cells(a,b,y)[left:left+9])
                                         for y in range(source_y(64),source_y(81)+1)))
                phases.append(regions)
                if not both:
                    expected=tuple(tuple(dhgr.cells(*baseline,y)[115:124])
                                   for y in range(source_y(64),source_y(81)+1))
                    self.assertEqual(regions[1],expected)
            self.assertNotEqual(phases[0][0],phases[2][0])
            if both:self.assertNotEqual(phases[0][1],phases[2][1])
            self.assertEqual(phases[0],phases[1]);self.assertEqual(phases[2],phases[3])

    def test_room_change_keeps_graphics_until_hidden_pair_is_complete(self):
        self.m.frame(13);self.m.frame(ord('3'));self.m.frame(ord('0'));self.m.frame(ord('1'));self.m.frame()
        self.assertEqual(self.m.bus.switches['TEXT'],0)
        previous=self.m.displayed_page()
        for name,value in [('actor_x',34),('actor_y',180),('facing',1),('pose',1),
                           ('walking',1),('key_action',255),('raw_key',255)]:self.set(name,value)
        self.call('game_tick');self.assertEqual(self.m.state()['current_room'],11)
        start=len(self.m.bus.io)
        self.call('world_load_scene')
        self.assertEqual(self.m.displayed_page(),previous)
        self.assertEqual(self.m.bus.switches['TEXT'],0)
        self.assertFalse(any(io[1]==0xC051 for io in self.m.bus.io[start:]))
        self.call('draw_scene')
        self.assertEqual(self.m.displayed_page(),previous,'hidden construction must preserve old frame')
        self.call('present_frame');new=self.m.displayed_page()
        self.assertNotEqual(new,previous)
        self.assertEqual(self.m.bus.switches['TEXT'],0)
        self.assertIn(self.m.bus.ram[self.m.symbols['terrain_pending']],[1,2])
        self.call('draw_scene');self.call('present_frame')
        self.assertEqual(self.m.displayed_page(),new,'second pair must match, without old-room trails')
        self.assertEqual(self.m.bus.ram[self.m.symbols['terrain_pending']],0)
        self.assertFalse(self.m.bus.visible_write_violations)
        self.assertFalse(self.m.bus.visible_text_write_violations)

    def test_darkness_panel_replaces_merchant_and_defers_graphics_preparation(self):
        self.m.frame(13);self.m.frame(ord('3'));self.m.frame(ord('0'));self.m.frame(ord('1'));self.m.frame()
        self.set('current_room',9);self.set('held_item',0);self.set('walking',0)
        self.call('world_load_scene')
        old=self.m.displayed_page()
        self.call('draw_scene');self.assertEqual(self.m.displayed_page(),old)
        self.call('present_frame')
        self.assertEqual((self.m.bus.switches['TEXT'],self.m.bus.switches['80COL'],self.m.bus.switches['MIXED']),(1,0,0))
        text=''.join(bytes(v&127 for v in row).decode('ascii') for row in self.m.text_rows(all_rows=True))
        self.assertIn('Il fait noir ici !',text)
        self.assertNotIn('marchand',text)
        self.assertEqual(self.m.bus.ram[self.m.symbols['terrain_pending']],3)
        self.set('held_item',1)
        for _ in range(2):self.call('draw_scene');self.call('present_frame')
        self.assertEqual((self.m.bus.switches['TEXT'],self.m.bus.switches['80COL'],self.m.bus.switches['MIXED']),(0,int(self.video=='dhgr'),1))
        self.assertEqual(self.m.bus.ram[self.m.symbols['terrain_pending']],0)
        self.assertFalse(self.m.bus.visible_write_violations)
        self.assertFalse(self.m.bus.visible_text_write_violations)

    def test_title_lightning_reveal_and_text_transition(self):
        self.m.bus.ram[:]=self.cold_ram;self.m.bus.aux[:]=self.cold_aux
        self.m.bus.switches.update(self.cold_switches)
        self.assertEqual(self.m.state()['game_mode'],9)
        self.assertEqual(self.m.bus.switches['MIXED'],0)
        off=(self.directory/'resources/title.dhgr').read_bytes()
        self.assertEqual(self.cold_ram[0xA000:0xC000]+self.cold_aux[0xA000:0xC000],off)
        from tools.title_resources import title_pages
        for _ in range(4):self.m.frame()
        displayed=self.m.displayed_page();on=title_pages(True)
        for y in range(110):
            a=dhgr.row_offset(y)
            for bank in range(2):self.assertEqual(displayed[bank][a:a+40],on[bank][a:a+40])
        (self.directory/'title-lightning.png').write_bytes(self.m.screen_png())
        for _ in range(70):self.m.frame()
        self.assertEqual(self.m.bus.ram[self.m.symbols['title_stage']],1)
        self.assertEqual(self.m.bus.ram[self.m.symbols['title_pages_ready']],3)
        self.assertEqual(self.m.displayed_page(),(off[:8192],off[8192:]))
        (self.directory/'title-complete.png').write_bytes(self.m.screen_png())
        self.m.frame(13)
        self.assertEqual(self.m.state()['game_mode'],11)
        self.assertEqual((self.m.bus.switches['TEXT'],self.m.bus.switches['80COL']),(1,0))
        text=''.join(bytes(v&127 for v in row).decode('ascii') for row in self.m.text_rows(all_rows=True))
        self.assertIn('Apres plusieurs jours de cheval',text)
        self.assertIn('Wesphalie.',text)
        self.assertIn('Fortune, Sagesse et Puissance',' '.join(text.split()))
        (self.directory/'introduction.png').write_bytes(self.m.screen_png())
        self.m.frame(13)
        self.assertEqual(self.m.state()['game_mode'],8)
        self.assertFalse(self.m.bus.visible_write_violations)


if __name__=='__main__':unittest.main(verbosity=2)
