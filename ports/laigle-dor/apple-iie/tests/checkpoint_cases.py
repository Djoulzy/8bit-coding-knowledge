"""Native v2 checkpoints in both editions: codec, UI, disk and world semantics."""
import binascii
from tools.common import ROOT
from tools.machine import Machine
from tools.disk import offset
from tools import checkpoint


class CheckpointTests:
    def read_code(self,machine=None):
        m=machine or self.m;a=m.symbols['code_ascii']
        return bytes(m.bus.ram[a:a+24]).decode('ascii')

    def enter_code(self,code,machine=None):
        m=machine or self.m
        for ch in code:m.frame(ord(ch))

    def checkpoint_world(self,mask):
        world=bytearray(self.world)
        for bit,room in enumerate(checkpoint.PICKUP_ROOMS):
            if mask&(1<<bit):world[256+4*room]&=0xC7
        return world

    def test_checkpoint_codec_native_vectors_and_corruption(self):
        m=self.m
        resident=bytes(m.bus.ram[0x6000:0xA000]);aux=bytes(m.bus.aux)
        self.call('checkpoint_load',budget=10000000)
        module=(self.directory/'checkpoint.bin').read_bytes()
        self.assertLessEqual(len(module),checkpoint.CAPACITY)
        self.assertEqual(bytes(m.bus.ram[0xA000:0xA000+len(module)]),module)
        self.assertEqual(bytes(m.bus.ram[0x6000:0xA000]),resident)
        self.assertEqual(bytes(m.bus.aux),aux)
        disk=(self.directory/'laigle-dor.do').read_bytes()
        slot=b''.join(disk[offset(34,s):offset(34,s)+256] for s in range(16))
        self.assertEqual(slot,module.ljust(4096,b'\0'))
        self.assertEqual(checkpoint.pickup_rooms(self.world),checkpoint.PICKUP_ROOMS)
        self.assertEqual(sum(width for _,width in checkpoint.FIELDS),80)
        # Untouched room 12: missing quest flags 7, gold 500, strength tag E4.
        self.assertEqual(checkpoint.encode({'room':12}),'0000E0-C01F40-00E400-00550B')
        golds=[0,1,255,256,7142,65535];scores=[0,1,255,256,2630,4095]
        forces=[0,1,49,50,99,100]
        for room in range(64):
            mask=[0,0xFFFF,0xAAAA,0x5555,1<<(room%16)][room%5]
            vector={'room':room,'vials':room%8,'torches':(room+1)%8,
                    'ropes':(room+2)%8,'crowbars':(room+3)%8,
                    'possessions':room&15,'scrolls':room&7,'objectives':(room>>2)&7,
                    'gold':golds[room%6],'points':scores[room%6],
                    'force':forces[room%6],'pickups':mask}
            self.set('current_room',room);self.set('held_item',1)
            for field in ['vials','torches','ropes','crowbars','possessions','scrolls','objectives']:
                self.set(field,vector[field])
            for field in ['gold','points']:self.word(field,vector[field])
            # The saved percentage floors fractional hundredths (no rounding up).
            self.word('energy',vector['force']*100+(37 if vector['force']<100 else 0))
            m.bus.ram[0x1000:0x1200]=self.checkpoint_world(mask)
            state=bytes(m.bus.ram[0x1000:0x1340]);self.call('full_code_encode')
            self.assertEqual(m.cpu.p&1,0,vector)
            expected=checkpoint.encode(vector).replace('-','')
            self.assertEqual(self.read_code(),expected,vector)
            self.assertEqual(checkpoint.decode(expected.lower()),vector)
            self.call('full_code_decode');self.assertEqual(m.cpu.p&1,0)
            values=bytes(m.bus.ram[m.symbols['code_fields']:m.symbols['code_fields']+15])
            self.assertEqual(list(values),[
                vector['vials'],vector['torches'],vector['ropes'],vector['crowbars'],
                vector['possessions'],vector['objectives'],vector['scrolls'],room,
                vector['gold']>>8,vector['gold']&255,vector['points']>>8,vector['points']&255,
                0x80|vector['force'],mask>>8,mask&255])
            self.assertEqual(bytes(m.bus.ram[0x1000:0x1340]),state)
        valid=bytes.fromhex(checkpoint.encode({'room':63}).replace('-',''))
        before=bytes(m.bus.ram[0x0C00:0x0C1D])+bytes(m.bus.ram[0x1000:0x1340])
        a=m.symbols['code_ascii']
        for bit in range(96):
            corrupt=bytearray(valid);corrupt[bit//8]^=1<<(bit%8)
            text=corrupt.hex().upper()
            m.bus.ram[a:a+24]=text.encode('ascii')
            self.call('full_code_decode');self.assertEqual(m.cpu.p&1,1,bit)
            with self.assertRaises(ValueError):checkpoint.decode(text)
            self.assertEqual(bytes(m.bus.ram[0x0C00:0x0C1D])+bytes(m.bus.ram[0x1000:0x1340]),before)
        # CRC-valid invalid format tags / percentages: tag is payload byte 7.
        for tag in [0,1,100,127,0xE5,0xFF]:
            payload=bytearray(valid[:10]);payload[7]=tag
            text=(payload+binascii.crc_hqx(payload,0xFFFF).to_bytes(2,'big')).hex().upper()
            m.bus.ram[a:a+24]=text.encode('ascii')
            self.call('full_code_decode');self.assertEqual(m.cpu.p&1,1,tag)
            with self.assertRaises(ValueError):checkpoint.decode(text)
        for bad in ['','0'*18,'Z'*24,'0'*23,'0'*25]:
            with self.assertRaises(ValueError):checkpoint.decode(bad)
        for bad in [{'room':64},{'room':-1},{'room':12,'vials':8},
                    {'room':12,'held_item':1},{'room':12,'possessions':16},
                    {'room':12,'gold':65536},{'room':12,'points':4096},
                    {'room':12,'force':101},{'room':12,'pickups':65536}]:
            with self.assertRaises(ValueError):checkpoint.encode(bad)

    def test_checkpoint_save_pauses_help_and_consumes_close_keys(self):
        self.m.frame(13);self.m.frame(ord('1'));self.m.frame()
        self.set('torches',2);self.word('torch_life',250)
        self.set('held_item',0);self.set('saved_item',1);self.set('action_kind',3)
        self.set('action_phase',1);self.set('walking',1)
        before=self.m.state();world=bytes(self.m.bus.ram[0x1000:0x1300])
        self.m.frame(ord('c'))
        self.assertEqual(self.m.state()['game_mode'],16)
        self.assertEqual((self.m.bus.switches['TEXT'],self.m.bus.switches['80COL']),(1,0))
        code=self.read_code();decoded=checkpoint.decode(code)
        self.assertEqual(decoded['torches'],2);self.assertNotIn('held_item',decoded)
        formatted='-'.join(code[i:i+6] for i in range(0,24,6))
        self.assertIn(formatted,self.debug_text())
        (self.directory/'checkpoint-save.png').write_bytes(self.m.screen_png())
        for key in [None,ord('R'),ord('I'),None]:self.m.frame(key)
        self.assertEqual(self.read_code(),code)
        self.m.frame(ord('H'));self.assertEqual(self.m.state()['game_mode'],10)
        self.m.frame(32);self.assertEqual(self.m.state()['game_mode'],16)
        self.assertEqual(self.read_code(),code)
        for close in [32,13,27]:
            self.m.frame(close)
            self.assertEqual(self.m.state()['game_mode'],0)
            for field in before.keys()-{'game_mode','display_page_hi','draw_page_hi','key_action'}:
                self.assertEqual(self.m.state()[field],before[field],field)
            self.m.frame(ord('C'))
        self.assertEqual(bytes(self.m.bus.ram[0x1000:0x1300]),world)
        self.assertFalse(self.m.bus.visible_write_violations)
        self.assertFalse(self.m.bus.visible_text_write_violations)

    def test_checkpoint_rejects_unrepresentable_stocks_without_changing_game_limits(self):
        self.m.frame(13);self.m.frame(ord('1'))
        for field,value in [('vials',8),('torches',9),('ropes',255),('crowbars',8),
                            ('points',4096),('energy',10001),('energy',65535)]:
            old=self.m.state()[field]
            (self.word if field in ['points','energy'] else self.set)(field,value)
            before=self.m.state()
            self.m.frame(ord('C'))
            self.assertEqual(self.m.state()['game_mode'],16)
            self.assertEqual(self.m.bus.ram[self.m.symbols['code_error']],5,(field,value))
            self.assertEqual(self.m.bus.ram[self.m.symbols['checkpoint_count']],0)
            self.assertIn('Stock >7',self.debug_text())
            (self.directory/'checkpoint-range-error.png').write_bytes(self.m.screen_png())
            self.m.frame(27)
            self.assertEqual(self.m.state()[field],before[field])
            for name in ['gold','points','energy','vials','torches','ropes','crowbars']:
                self.assertEqual(self.m.state()[name],before[name])
            (self.word if field in ['points','energy'] else self.set)(field,old)
        self.assertFalse(self.m.bus.visible_write_violations)
        self.assertFalse(self.m.bus.visible_text_write_violations)

    def test_checkpoint_entry_errors_editing_cancel_and_help(self):
        for key in b'Nina\r':self.m.frame(key)
        before=self.m.state();world=bytes(self.m.bus.ram[0x1000:0x1300])
        self.m.frame(ord('4'));self.assertEqual(self.m.state()['game_mode'],17)
        self.m.frame(13);self.assertEqual(self.m.bus.ram[self.m.symbols['code_error']],1)
        self.assertIn('Code invalide',self.debug_text())
        self.m.frame(ord('Z'));self.assertEqual(self.m.bus.ram[self.m.symbols['code_error']],3)
        self.m.frame(ord('A'));self.assertEqual(self.m.bus.ram[self.m.symbols['checkpoint_count']],0)
        self.m.frame(8)
        # A legacy v1 packet produces an explicit, actionable error.
        self.enter_code('260000-000000-1CEDA0');self.m.frame(13)
        self.assertEqual(self.m.bus.ram[self.m.symbols['code_error']],6)
        self.assertIn('18 caracteres incompatible',self.debug_text())
        for _ in range(18):self.m.frame(8)
        code=checkpoint.encode({'room':12}).replace('-','')
        wrong=code[:-1]+('0' if code[-1]!='0' else '1')
        self.enter_code(wrong.lower());self.m.frame(13)
        self.assertEqual(self.m.bus.ram[self.m.symbols['code_error']],2)
        self.assertEqual(self.m.state()['game_mode'],17)
        self.m.frame(8);self.m.frame(ord(code[-1]))
        self.m.frame(ord('0')) # 25th digit must not silently truncate a valid code
        self.assertEqual(self.m.bus.ram[self.m.symbols['code_error']],4)
        self.m.frame(13);self.assertEqual(self.m.state()['game_mode'],17)
        saved=self.read_code();count=self.m.bus.ram[self.m.symbols['checkpoint_count']]
        self.m.frame(ord('?'));self.assertEqual(self.m.state()['game_mode'],10)
        self.m.frame(32);self.assertEqual(self.m.state()['game_mode'],17)
        self.assertEqual((self.read_code(),self.m.bus.ram[self.m.symbols['checkpoint_count']]),(saved,count))
        self.assertIn('-'.join(saved[i:i+6] for i in range(0,24,6)),self.debug_text())
        (self.directory/'checkpoint-entry-error.png').write_bytes(self.m.screen_png())
        self.m.frame(8);self.m.frame(27)
        self.assertEqual(self.m.state()['game_mode'],1)
        for field in ['current_room','held_item','vials','torches','ropes','crowbars',
                      'possessions','scrolls','objectives','gold','points','energy','rng_state']:
            self.assertEqual(self.m.state()[field],before[field],field)
        self.assertEqual(bytes(self.m.bus.ram[0x1000:0x1300]),world)
        self.assertEqual(bytes(self.m.bus.ram[self.m.symbols['player_name']:self.m.symbols['player_name']+6]),b'Nina  ')
        self.assertFalse(self.m.bus.visible_write_violations)
        self.assertFalse(self.m.bus.visible_text_write_violations)

    def test_checkpoint_cold_cross_profile_resume_preserves_new_name(self):
        # Save in an oubliette, then boot the other edition and type a new name.
        for key in b'Elise\r1':self.m.frame(key)
        source={'room':23,'vials':7,'torches':2,'ropes':6,'crowbars':3,
                'possessions':15,'scrolls':5,'objectives':3,'gold':7142,
                'points':2630,'force':50,'pickups':0xA55A}
        self.set('current_room',23);self.set('held_item',1)
        for key in ['vials','torches','ropes','crowbars','possessions','scrolls','objectives']:
            self.set(key,source[key])
        self.set('in_pit',1);self.set('pit_wait',1);self.word('torch_life',200)
        self.word('gold',source['gold']);self.word('points',source['points']);self.word('energy',5099)
        self.m.bus.ram[0x1000:0x1200]=self.checkpoint_world(source['pickups'])
        self.m.bus.ram[0x1000]^=0x30 # excluded room/door mutation
        self.m.frame(ord('C'));code=self.read_code()
        self.assertEqual(checkpoint.decode(code),source)
        target_mode='mono' if self.video=='dhgr' else 'dhgr'
        directory=ROOT/('build/game-mono' if target_mode=='mono' else 'build/game')
        target=Machine(directory=directory,video=target_mode);target.boot()
        target.frame(13);target.frame(13)
        for key in b'Paul\r4':target.frame(key)
        self.assertEqual(target.state()['game_mode'],17)
        self.enter_code('-'.join(code[i:i+6] for i in range(0,24,6)).lower(),target)
        (directory/('checkpoint-entry-from-%s.png'%self.video)).write_bytes(target.screen_png())
        target.frame(13)
        state=target.state()
        self.assertEqual(state['game_mode'],0)
        self.assertEqual(state['current_room'],23)
        for key in ['vials','torches','ropes','crowbars','possessions','scrolls','objectives','gold','points']:
            self.assertEqual(state[key],source[key],key)
        a=target.symbols['player_name'];self.assertEqual(bytes(target.bus.ram[a:a+6]),b'Paul  ')
        self.assertEqual((state['held_item'],state['energy']),(0,5000))
        self.assertEqual((state['in_pit'],state['action_kind'],state['walking'],state['facing'],state['actor_y']),(0,0,0,0,180))
        self.assertEqual(target.bus.ram[0x1200+state['actor_x']+2],0)
        self.assertEqual(bytes(target.bus.ram[0x1000:0x1200]),self.checkpoint_world(source['pickups']))
        self.assertEqual(bytes(target.bus.ram[0x12A0:0x12E0]),bytes(64))
        self.assertTrue(200<=state['torch_life']<=299)
        self.assertTrue(20<=target.bus.ram[target.symbols['bar_life']]<=39)
        self.assertEqual((target.bus.switches['TEXT'],target.bus.switches['MIXED'],target.bus.switches['80COL']),
                         (0,1,int(target_mode=='dhgr')))
        # Save immediately again: no held torch, no duplicate pickup or economy.
        target.frame(ord('C'))
        self.assertEqual(checkpoint.decode(self.read_code(target)),source)
        target.frame(27)
        for _ in range(2):target.frame()
        (directory/('checkpoint-restored-from-%s.png'%self.video)).write_bytes(target.screen_png())
        self.assertFalse(target.bus.visible_write_violations)
        self.assertFalse(target.bus.visible_text_write_violations)

    def test_checkpoint_removed_treasures_cannot_award_twice(self):
        for key in b'Paul\r4':self.m.frame(key)
        source={'room':52,'gold':65535,'points':4095,'force':0,'pickups':0xFFFF}
        self.enter_code(checkpoint.encode(source));self.m.frame(13)
        state=self.m.state()
        self.assertEqual((state['gold'],state['points'],state['energy']),(65535,4095,0))
        self.assertEqual(bytes(self.m.bus.ram[0x1000:0x1200]),self.checkpoint_world(0xFFFF))
        # Actually open the original bag chest and attempt P from its reachable
        # front; an invalid far-away action would not test duplicate rewards.
        self.set('actor_x',28);self.set('actor_y',170);self.set('facing',3)
        self.set('pose',3);self.set('held_item',6);self.set('crowbars',1)
        self.set('bar_life',30);self.call('full_open')
        self.assertEqual(self.m.bus.ram[self.m.symbols['chest_open']],1)
        opened_world=bytes(self.m.bus.ram[0x1000:0x1200])
        self.set('held_item',0)
        for _ in range(2):
            self.call('full_pickup')
            self.assertEqual(self.m.bus.ram[self.m.symbols['message_id']],7) # Vide
        after=self.m.state()
        self.assertEqual((after['gold'],after['points']),(65535,4095))
        self.assertEqual(self.m.bus.ram[self.m.symbols['room_treasure']],0)
        self.assertEqual(bytes(self.m.bus.ram[0x1000:0x1200]),opened_world)

    def test_checkpoint_close_rebuilds_room_and_retains_gate_and_pit_state(self):
        self.m.frame(13);self.m.frame(ord('1'))
        for room,pit,action,side in [(36,0,5,27),(23,1,0,0),(26,0,0,0)]:
            self.set('current_room',room);self.set('in_pit',pit)
            self.set('held_item',1);self.set('torches',2)
            self.set('pit_wait',pit);self.set('action_kind',action)
            self.set('action_phase',3);self.call('world_load_scene')
            self.set('gate_side',side)
            # A live falling-grille frame has already stamped its collision
            # cells. Establish that state without advancing controller time.
            self.call('draw_scene');self.call('present_frame')
            world=bytes(self.m.bus.ram[0x1000:0x1300])
            main=bytes(self.m.bus.ram[0xA000:0xC000]);aux=bytes(self.m.bus.aux[0xA000:0xC000])
            state=self.m.state()
            for field in ['pit_wait','gate_side']:state[field]=self.m.bus.ram[self.m.symbols[field]]
            self.m.frame(ord('C'));self.m.frame(ord('?'));self.m.frame(32);self.m.frame(27)
            for field in ['current_room','in_pit','pit_wait','action_kind','action_phase','gate_side','energy','tick_lo','tick_hi']:
                value=self.m.bus.ram[self.m.symbols[field]] if field in ['pit_wait','gate_side'] else self.m.state()[field]
                self.assertEqual(value,state[field],(room,field))
            changed=[hex(0x1000+i) for i,(a,b) in enumerate(zip(world,self.m.bus.ram[0x1000:0x1300])) if a!=b]
            self.assertEqual(changed,[],(room,changed))
            self.assertEqual(bytes(self.m.bus.ram[0xA000:0xC000]),main)
            self.assertEqual(bytes(self.m.bus.aux[0xA000:0xC000]),aux)
        self.assertFalse(self.m.bus.visible_write_violations)
        self.assertFalse(self.m.bus.visible_text_write_violations)
