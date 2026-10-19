"""Full game in HGR; inherit rule/UI scenarios, replace color-specific oracles."""
import json
from tests import world_port
from tools.common import ROOT, Source, digest, write_json
from tools.resources import sprite, row_offset
from tools import mono
from tools.video_layout import source_y
from tools.title_resources import mono_title_page


class MonoWorldTests(world_port.NativeWorldTests):
    video = 'mono'
    directory = ROOT/'build/game-mono'

    def test_all_64_rooms_use_the_same_constructor_and_grid(self):
        self.set('game_mode',0);self.set('held_item',1)
        archive=bytes(self.m.bus.aux[0x6000:0xC000]);results=[]
        for number in range(64):
            if number%16==0:print('  HGR source room constructor: %d/64'%number,flush=True)
            self.set('current_room',number);old=self.m.displayed_page()
            self.call('world_load_scene')
            self.assertEqual(self.m.displayed_page(),old)
            _,grid,ops,room=self.constructor.scene(self.world,number,self.variation)
            expected=mono.scene_page(self.constructor,ops)
            self.assertEqual(self.m.bus.ram[0x1200:0x1278],grid,number)
            self.assertEqual(bytes(self.m.bus.ram[0xA000:0xC000]),expected,number)
            for _ in range(2):
                page=self.m.state()['display_page_hi']^0x60
                self.set('draw_page_hi',page);self.set('render_page_index',int(page==0x40))
                self.call('full_prepare_page')
                self.assertEqual(bytes(self.m.bus.ram[page*256:page*256+8192]),expected)
                self.call('present_frame')
            self.assertEqual(self.m.bus.ram[self.m.symbols['terrain_pending']],0)
            self.assertEqual(bytes(self.m.bus.aux[0x6000:0xC000]),archive)
            results.append({'room':number,'geometry':room.geometry,'collision_match':True,
                            'original_dot_layer_oracle_match':True,'both_main_frames_match':True})
        write_json(self.directory/'room-verification.json',{'rooms':results,
            'program_sha256':digest((self.directory/'game.bin').read_bytes()),
            'execution':'actual NMOS instructions in py65 functional Apple bus; no original Oric runtime'})
        self.assertFalse(self.m.bus.visible_write_violations)

    def test_approved_actor_pixels_survive_auxiliary_and_compact_storage(self):
        ids=json.loads((self.directory/'resources/game-resources.json').read_text())['actor_sprite_ids']
        source=Source()
        for sid in [40,41,42,43,*range(46,62),64,65,67]:
            original=sprite(source,sid)
            for index,page in enumerate([0x2000,0x4000]):
                for x,y in [(19,140),(1,20),(38,190)]:
                    self.m.bus.ram[page:page+8192]=bytes([0x55])*8192
                    before=bytes(self.m.bus.aux[page:page+8192])
                    expected=bytearray([0x55])*8192
                    mono.actor_layer(expected,original,x,y)
                    for name,value in [('actor_x',x),('actor_y',y),('draw_page_hi',page>>8),
                                       ('sprite_index',ids.index(sid)),('dx',0),('dy',0),('render_page_index',index)]:
                        self.set(name,value)
                    self.call('draw_sprite')
                    self.assertEqual(bytes(self.m.bus.ram[page:page+8192]),expected,(sid,x,y))
                    self.assertEqual(bytes(self.m.bus.aux[page:page+8192]),before)

    def flame_region(self,image,side):
        left,right=(6,10) if side==0 else (32,36)
        return b''.join(image[row_offset(y)+left:row_offset(y)+right]
                        for y in range(source_y(64),source_y(81)+1))

    def test_source_torch_flames_animate_on_both_pages_without_trails(self):
        self.set('current_room',12);self.set('game_mode',0);self.call('world_load_scene')
        baseline=bytes(self.m.bus.ram[0xA000:0xC000]);rng=self.m.state()['rng_state']
        seen={0x20:{},0x40:{}}
        for tick in range(8):
            self.set('tick_lo',tick);self.call('draw_scene')
            page=self.m.state()['draw_page_hi'];phase=(tick>>1)&1
            actual=bytes(self.m.bus.ram[page*256:page*256+8192])
            # Independent source-dot composition in each flame region.
            expected=bytearray(baseline);s=sprite(Source(),36+phase)
            for left in [24,210]:
                for j,(row,masks) in enumerate(zip(s['pixels'],s['masks'])):
                    sy=64+j;ty=source_y(sy)
                    if source_y(sy+1)==ty:continue
                    for k,(bit,mask) in enumerate(zip(row,masks)):
                        if mask:mono.put(expected,left+k,ty,bit)
            for side in [0,1]:self.assertEqual(self.flame_region(actual,side),self.flame_region(expected,side))
            if phase in seen[page]:self.assertEqual(actual,seen[page][phase])
            seen[page][phase]=actual;self.call('present_frame')
        self.assertTrue(all(len(v)==2 for v in seen.values()))
        self.assertEqual(bytes(self.m.bus.ram[0xA000:0xC000]),baseline)
        self.assertEqual(self.m.state()['rng_state'],rng)
        (self.directory/'room12-flames.png').write_bytes(self.m.screen_png())
        self.set('held_item',1);self.set('actor_y',180)
        images=[]
        for tick in [0,2,4]:
            self.set('tick_lo',tick);self.call('draw_scene');self.call('present_frame')
            images.append(self.m.displayed_page())
        self.assertNotEqual(images[0],images[1]);self.assertEqual(images[0],images[2])
        self.assertFalse(self.m.bus.visible_write_violations)

    def test_secret_cue_and_grille_padlocks_are_visible(self):
        for number in [0,20]:
            self.set('current_room',number);self.set('game_mode',0);self.set('held_item',1)
            self.call('world_load_scene')
            ops=self.constructor.scene(self.world,number,self.variation)[2]
            self.assertEqual(bytes(self.m.bus.ram[0xA000:0xC000]),mono.scene_page(self.constructor,ops))
            self.set('actor_y',180);self.call('draw_scene');self.call('present_frame')
            (self.directory/('room%d-original-grille.png'%number)).write_bytes(self.m.screen_png())

    def test_lighting_does_not_leave_an_unanimated_fixture(self):
        for number,mask,both in [(12,1,True),(9,1,False),(9,2,False)]:
            self.set('current_room',number);self.set('game_mode',0)
            self.call('world_load_scene');self.set('room_light',3)
            self.m.bus.ram[0x12A0+number]=mask
            phases=[]
            for tick in range(4):
                self.set('tick_lo',tick);self.call('draw_scene');self.call('present_frame')
                phases.append(tuple(self.flame_region(self.m.displayed_page(),s) for s in [0,1]))
            for side in [0,1]:
                if both or mask&(1<<side):self.assertNotEqual(phases[0][side],phases[2][side])
                else:self.assertEqual(phases[0][side],phases[2][side])
            self.assertEqual(phases[0],phases[1]);self.assertEqual(phases[2],phases[3])

    def test_title_lightning_reveal_and_text_transition(self):
        self.m.bus.ram[:]=self.cold_ram;self.m.bus.aux[:]=self.cold_aux
        self.m.bus.switches.update(self.cold_switches)
        off=mono_title_page(False);on=mono_title_page(True)
        self.assertEqual(self.cold_ram[0xA000:0xC000],off)
        for _ in range(4):self.m.frame()
        for y in range(110):
            a=row_offset(y);self.assertEqual(self.m.displayed_page()[a:a+40],on[a:a+40])
        (self.directory/'title-lightning.png').write_bytes(self.m.screen_png())
        for _ in range(70):self.m.frame()
        self.assertEqual(self.m.displayed_page(),off)
        (self.directory/'title-complete.png').write_bytes(self.m.screen_png())
        self.m.frame(13);self.assertEqual(self.m.state()['game_mode'],11)
        (self.directory/'introduction.png').write_bytes(self.m.screen_png())
        self.m.frame(13);self.assertEqual(self.m.state()['game_mode'],8)
        self.assertFalse(self.m.bus.visible_write_violations)

    def test_hgr_only_main_frames_and_zero_phase_bits(self):
        self.m.frame(13);self.m.frame(ord('1'))
        for key in [ord('N'),None,None,None,32,ord('H'),32]:self.m.frame(key)
        self.assertEqual((self.m.bus.switches['80COL'],self.m.bus.switches['DHIRES']),(0,0))
        self.assertFalse(any(bank for bank,address in self.m.bus.bank_graphics_writes))
        for page in [0x2000,0x4000,0xA000]:
            self.assertFalse(any(v&128 for y in range(160)
                                 for v in self.m.bus.ram[page+row_offset(y):page+row_offset(y)+40]))
        (self.directory/'room12-mono.png').write_bytes(self.m.screen_png())
