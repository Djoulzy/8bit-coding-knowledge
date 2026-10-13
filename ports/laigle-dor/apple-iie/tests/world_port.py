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
from tools.resources import sprite


class NativeWorldTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.machine=Machine(directory=ROOT/'build/game',video='dhgr')
        cls.machine.boot()
        cls.cold_ram=bytes(cls.machine.bus.ram);cls.cold_aux=bytes(cls.machine.bus.aux)
        cls.cold_switches=dict(cls.machine.bus.switches)
        cls.machine.frame(13) # skip title -> name entry
        cls.ram=bytes(cls.machine.bus.ram);cls.aux=bytes(cls.machine.bus.aux)
        cls.switches=dict(cls.machine.bus.switches)
        cls.world=Source().read(0x5600,512)
        cls.variation=room_variation()[0]
        cls.constructor=Constructor(Source())

    def setUp(self):
        self.m=self.machine
        self.m.bus.ram[:]=self.ram;self.m.bus.aux[:]=self.aux
        self.m.cpu.pc=self.m.symbols['main_loop'];self.m.cpu.sp=255
        self.m.bus.switches.update(self.switches)
        self.m.bus.strobe=False
        self.m.bus.visible_write_violations.clear();self.m.bus.visible_text_write_violations.clear()

    def set(self,name,value):
        self.m.bus.ram[self.m.symbols[name]]=value

    def word(self,name,value):
        a=self.m.symbols[name];self.m.bus.ram[a:a+2]=value.to_bytes(2,'little')

    def call(self,name,budget=3000000):
        self.m.cpu.stPushWord(0x1EFF);self.m.cpu.pc=self.m.symbols[name]
        self.m.until(0x1F00,budget)
        self.m.cpu.pc=self.m.symbols['main_loop']

    def test_boot_preloads_shared_atlas_and_keeps_program_main(self):
        atlas=(ROOT/'build/game/aux-assets.bin').read_bytes()
        self.assertEqual(self.aux[0x6000:0x6000+len(atlas)],atlas)
        self.assertEqual(self.m.state()['game_mode'],8)
        self.assertEqual(self.m.state()['gold'],500)
        self.assertTrue(self.m.ramrd_fetch_pcs <= set(range(0x40,0x52)))
        self.assertFalse(self.m.bus.motor)
        resource=ROOT/'build/game/resources'
        report=json.loads((resource/'game-resources.json').read_text())
        self.assertEqual((report['room_bitmaps'],report['geometry_templates']),(0,4))
        self.assertFalse(list(resource.glob('room12*')))
        self.assertFalse((resource/'world-archive.bin').exists())
        self.assertEqual((resource/'room-variation.bin').read_bytes(),self.variation)

    def test_approved_actor_pixels_survive_auxiliary_and_compact_storage(self):
        ids=json.loads((ROOT/'build/game/resources/game-resources.json').read_text())['actor_sprite_ids']
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
        write_json(ROOT/'build/game/room-verification.json',{'rooms':results,
                   'program_sha256':digest((ROOT/'build/game/game.bin').read_bytes()),
                   'execution':'py65 actual NMOS instructions; not original Oric runtime or real Apple hardware'})
        self.assertFalse(self.m.bus.visible_write_violations)

    def test_name_exterior_merchant_and_resume(self):
        for k in b'ANNA\r':self.m.frame(k)
        self.assertEqual(self.m.state()['game_mode'],1)
        self.assertEqual((self.m.bus.switches['TEXT'],self.m.bus.switches['80COL']),(1,0))
        self.m.frame(ord('3'));self.assertEqual(self.m.state()['game_mode'],2)
        def screen():return ''.join(bytes(v&127 for v in row).decode('ascii') for row in self.m.text_rows(all_rows=True))
        self.assertIn('OR:00500',screen())
        self.m.frame(ord('2'))
        self.assertEqual((self.m.state()['torches'],self.m.state()['gold']),(1,310))
        self.assertIn('OR:00310',screen())
        self.m.frame(ord('3'))
        self.assertEqual((self.m.state()['ropes'],self.m.state()['gold']),(1,200))
        self.assertIn('OR:00200',screen())
        self.m.frame(ord('1')) # denied, insufficient funds
        self.assertEqual((self.m.state()['vials'],self.m.state()['gold']),(0,200))
        self.m.frame(ord('0'));self.m.frame(ord('1'))
        self.assertEqual((self.m.bus.switches['TEXT'],self.m.bus.switches['80COL'],self.m.bus.switches['MIXED']),(0,1,1))
        self.m.frame(ord('I'));energy=self.m.state()['energy']
        self.m.frame();self.assertEqual(self.m.state()['energy'],energy)
        self.m.frame(32);self.assertEqual(self.m.state()['game_mode'],0)

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
        self.assertIn('DER REIF',text())
        self.m.frame(32);self.assertIn('DER GOLDENE',text())
        self.m.frame(32);self.assertIn('DER ADLER',text())
        self.m.frame(32);self.assertIn('STERN',text())
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
        (ROOT/'build/game/room23-pit.png').write_bytes(self.m.screen_png())
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
        (ROOT/'build/game/room12-flames.png').write_bytes(self.m.screen_png())
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
        (ROOT/'build/game/room0-secret-grille.png').write_bytes(self.m.screen_png())
        self.set('current_room',20);self.call('world_load_scene')
        a,b=bytes(self.m.bus.ram[0xA000:0xC000]),bytes(self.m.bus.aux[0xA000:0xC000])
        self.assertNotEqual(dhgr.cells(a,b,source_y(106))[x:x+4],[0]*4)
        # Native golden lock body plus a black keyhole on a white grille.
        cells=dhgr.cells(a,b,source_y(119+29+5))
        left=10+216//2
        self.assertEqual(cells[left:left+4],[13,13,0,13])
        self.assertIn(15,dhgr.cells(a,b,source_y(140))[left:left+9])
        self.call('draw_scene');self.call('present_frame')
        (ROOT/'build/game/room20-grille.png').write_bytes(self.m.screen_png())

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
        self.assertIn('IL FAIT NOIR ICI !',text)
        self.assertNotIn('MARCHAND',text)
        self.assertEqual(self.m.bus.ram[self.m.symbols['terrain_pending']],3)
        self.set('held_item',1)
        for _ in range(2):self.call('draw_scene');self.call('present_frame')
        self.assertEqual((self.m.bus.switches['TEXT'],self.m.bus.switches['80COL'],self.m.bus.switches['MIXED']),(0,1,1))
        self.assertEqual(self.m.bus.ram[self.m.symbols['terrain_pending']],0)
        self.assertFalse(self.m.bus.visible_write_violations)
        self.assertFalse(self.m.bus.visible_text_write_violations)

    def test_title_lightning_reveal_and_text_transition(self):
        self.m.bus.ram[:]=self.cold_ram;self.m.bus.aux[:]=self.cold_aux
        self.m.bus.switches.update(self.cold_switches)
        self.assertEqual(self.m.state()['game_mode'],9)
        self.assertEqual(self.m.bus.switches['MIXED'],0)
        off=(ROOT/'build/game/resources/title.dhgr').read_bytes()
        self.assertEqual(self.cold_ram[0xA000:0xC000]+self.cold_aux[0xA000:0xC000],off)
        from tools.title_resources import title_pages
        for _ in range(4):self.m.frame()
        displayed=self.m.displayed_page();on=title_pages(True)
        for y in range(110):
            a=dhgr.row_offset(y)
            for bank in range(2):self.assertEqual(displayed[bank][a:a+40],on[bank][a:a+40])
        (ROOT/'build/game/title-lightning.png').write_bytes(self.m.screen_png())
        for _ in range(70):self.m.frame()
        self.assertEqual(self.m.bus.ram[self.m.symbols['title_stage']],1)
        self.assertEqual(self.m.bus.ram[self.m.symbols['title_pages_ready']],3)
        self.assertEqual(self.m.displayed_page(),(off[:8192],off[8192:]))
        (ROOT/'build/game/title-complete.png').write_bytes(self.m.screen_png())
        self.m.frame(13)
        self.assertEqual(self.m.state()['game_mode'],8)
        self.assertEqual((self.m.bus.switches['TEXT'],self.m.bus.switches['80COL']),(1,0))
        self.assertFalse(self.m.bus.visible_write_violations)


if __name__=='__main__':unittest.main(verbosity=2)
