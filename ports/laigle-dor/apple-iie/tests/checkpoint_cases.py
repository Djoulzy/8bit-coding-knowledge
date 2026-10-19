"""Checkpoint integration cases mixed into both real native game profiles."""
import binascii
from tools.common import ROOT
from tools.machine import Machine
from tools import checkpoint


class CheckpointTests:
    def read_code(self,machine=None):
        m=machine or self.m;a=m.symbols['code_ascii']
        return bytes(m.bus.ram[a:a+18]).decode('ascii')

    def enter_code(self,code,machine=None):
        m=machine or self.m
        for ch in code:m.frame(ord(ch))

    def test_checkpoint_codec_native_vectors_and_corruption(self):
        m=self.m
        for segment in ['PASSCODE','PASSUI','PASSTAIL']:
            start=m.symbols['__%s_LOAD__'%segment]-0x6000
            run=m.symbols['__%s_RUN__'%segment];size=m.symbols['__%s_SIZE__'%segment]
            self.assertLess(size,256)
            self.assertEqual(bytes(m.bus.ram[run:run+size]),
                             (self.directory/'game.bin').read_bytes()[start:start+size])
        self.assertEqual(checkpoint.encode({'room':12}),'260000-000000-1CEDA0')
        counts=[0,1,9,15,16,99,255]
        vectors=[]
        for room in range(64):
            slot=room%6;held=checkpoint.ITEMS[slot]
            vector={'room':room,'held_item':held,'vials':counts[room%7],
                    'torches':counts[(room+1)%7],'ropes':counts[(room+2)%7],
                    'crowbars':counts[(room+3)%7],'possessions':room&15,
                    'scrolls':room&7,'objectives':(room>>2)&7}
            if slot==1:vector['torches']=max(1,vector['torches'])
            if slot==2:vector['possessions']|=1
            if slot==3:vector['possessions']|=2
            if slot==4:vector['vials']=max(1,vector['vials'])
            if slot==5:vector['crowbars']=max(1,vector['crowbars'])
            vectors.append(vector)
        for vector in vectors:
            self.set('current_room',vector['room']);self.set('held_item',vector['held_item'])
            for field in ['vials','torches','ropes','crowbars','possessions','scrolls','objectives']:
                self.set(field,vector[field])
            state=bytes(m.bus.ram[0x1000:0x1340]);self.call('full_code_encode')
            expected=checkpoint.encode(vector).replace('-','')
            self.assertEqual(self.read_code(),expected)
            self.assertEqual(checkpoint.decode(expected),vector)
            self.call('full_code_decode')
            self.assertEqual(m.cpu.p&1,0)
            values=bytes(m.bus.ram[m.symbols['code_fields']:m.symbols['code_fields']+11])
            self.assertEqual(list(values),[1,vector['room'],checkpoint.ITEMS.index(vector['held_item']),
                             *[vector[f] for f in ['vials','torches','ropes','crowbars','possessions','scrolls','objectives']],0])
            self.assertEqual(bytes(m.bus.ram[0x1000:0x1340]),state)
        # Flip every bit, including each CRC octet. No rejected decode mutates
        # game state, even when the payload had otherwise valid field values.
        valid=bytes.fromhex(checkpoint.encode({'room':63}).replace('-',''))
        before=bytes(m.bus.ram[0x0C00:0x0C1D])+bytes(m.bus.ram[0x1000:0x1340])
        a=m.symbols['code_ascii']
        for bit in range(72):
            corrupt=bytearray(valid);corrupt[bit//8]^=1<<(bit%8)
            m.bus.ram[a:a+18]=corrupt.hex().upper().encode('ascii')
            self.call('full_code_decode');self.assertEqual(m.cpu.p&1,1,bit)
            self.assertEqual(bytes(m.bus.ram[0x0C00:0x0C1D])+bytes(m.bus.ram[0x1000:0x1340]),before)
        # CRC-valid but unsupported/noncanonical/inconsistent payloads.
        def raw(fields):
            bits=0
            for value,(_,width) in zip(fields,checkpoint.FIELDS):bits=bits<<width|value
            payload=bits.to_bytes(7,'big')
            return (payload+binascii.crc_hqx(payload,0xFFFF).to_bytes(2,'big')).hex().upper()
        for offset,value in [(0,2),(10,1),(10,2),(10,3),(2,6),(2,7),
                             (2,1),(2,2),(2,3),(2,4),(2,5)]:
            fields=[1,12,0,0,0,0,0,0,0,7,0];fields[offset]=value
            m.bus.ram[a:a+18]=raw(fields).encode('ascii')
            self.call('full_code_decode');self.assertEqual(m.cpu.p&1,1,(offset,value))
        for bad in ['','0'*17,'Z'*18,'0'*19]:
            with self.assertRaises(ValueError):checkpoint.decode(bad)
        for bad in [{'room':64},{'room':-1},{'room':12,'vials':256},
                    {'room':12,'held_item':1},{'room':12,'possessions':16}]:
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
        code=self.read_code();self.assertEqual(checkpoint.decode(code)['held_item'],1)
        formatted='-'.join(code[i:i+6] for i in range(0,18,6))
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

    def test_checkpoint_entry_errors_editing_cancel_and_help(self):
        for key in b'Nina\r':self.m.frame(key)
        before=self.m.state();world=bytes(self.m.bus.ram[0x1000:0x1300])
        self.m.frame(ord('4'));self.assertEqual(self.m.state()['game_mode'],17)
        self.m.frame(13);self.assertEqual(self.m.bus.ram[self.m.symbols['code_error']],1)
        self.assertIn('Code invalide',self.debug_text())
        self.m.frame(ord('Z'));self.assertEqual(self.m.bus.ram[self.m.symbols['code_error']],3)
        self.m.frame(ord('A'));self.assertEqual(self.m.bus.ram[self.m.symbols['checkpoint_count']],0)
        self.m.frame(8)
        code=checkpoint.encode({'room':12}).replace('-','')
        wrong=code[:-1]+('0' if code[-1]!='0' else '1')
        self.enter_code(wrong.lower());self.m.frame(13)
        self.assertEqual(self.m.bus.ram[self.m.symbols['code_error']],2)
        self.assertEqual(self.m.state()['game_mode'],17)
        self.m.frame(8);self.m.frame(ord(code[-1]))
        self.m.frame(ord('0')) # 19th digit must not silently truncate a valid code
        self.assertEqual(self.m.bus.ram[self.m.symbols['code_error']],4)
        self.m.frame(13);self.assertEqual(self.m.state()['game_mode'],17)
        saved=self.read_code();count=self.m.bus.ram[self.m.symbols['checkpoint_count']]
        self.m.frame(ord('?'));self.assertEqual(self.m.state()['game_mode'],10)
        self.m.frame(32);self.assertEqual(self.m.state()['game_mode'],17)
        self.assertEqual((self.read_code(),self.m.bus.ram[self.m.symbols['checkpoint_count']]),(saved,count))
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
        # Generate in an oubliette in this edition, then boot the other edition
        # afresh and type a different name before entering its exterior menu.
        for key in b'Elise\r1':self.m.frame(key)
        source={'room':23,'held_item':1,'vials':255,'torches':2,'ropes':16,
                'crowbars':9,'possessions':15,'scrolls':5,'objectives':3}
        self.set('current_room',23)
        for key,value in source.items():
            if key!='room':self.set(key,value)
        self.set('in_pit',1);self.set('pit_wait',1);self.word('torch_life',200)
        self.word('gold',1234);self.word('points',4321);self.word('energy',5000)
        self.m.bus.ram[0x1000]^=0x30 # excluded mutable world state
        self.m.frame(ord('C'));code=self.read_code()
        self.assertEqual(checkpoint.decode(code),source)
        target_mode='mono' if self.video=='dhgr' else 'dhgr'
        directory=ROOT/('build/game-mono' if target_mode=='mono' else 'build/game')
        target=Machine(directory=directory,video=target_mode);target.boot()
        target.frame(13);target.frame(13)
        for key in b'Paul\r4':target.frame(key)
        self.assertEqual(target.state()['game_mode'],17)
        self.enter_code('-'.join(code[i:i+6] for i in range(0,18,6)).lower(),target)
        (directory/('checkpoint-entry-from-%s.png'%self.video)).write_bytes(target.screen_png())
        target.frame(13)
        state=target.state()
        self.assertEqual(state['game_mode'],0)
        self.assertEqual(state['current_room'],23)
        for key,value in source.items():
            if key!='room':self.assertEqual(state[key],value,key)
        a=target.symbols['player_name'];self.assertEqual(bytes(target.bus.ram[a:a+6]),b'Paul  ')
        self.assertEqual((state['gold'],state['points'],state['energy']),(500,0,10000))
        self.assertEqual((state['in_pit'],state['action_kind'],state['walking'],state['facing'],state['actor_y']),(0,0,0,0,180))
        self.assertEqual(target.bus.ram[0x1200+state['actor_x']+2],0)
        self.assertEqual(bytes(target.bus.ram[0x1000:0x1200]),self.world)
        self.assertEqual(bytes(target.bus.ram[0x12A0:0x12E0]),bytes(64))
        self.assertTrue(200<=state['torch_life']<=299)
        self.assertTrue(20<=target.bus.ram[target.symbols['bar_life']]<=39)
        self.assertEqual((target.bus.switches['TEXT'],target.bus.switches['MIXED'],target.bus.switches['80COL']),
                         (0,1,int(target_mode=='dhgr')))
        for _ in range(2):target.frame()
        (directory/('checkpoint-restored-from-%s.png'%self.video)).write_bytes(target.screen_png())
        self.assertFalse(target.bus.visible_write_violations)
        self.assertFalse(target.bus.visible_text_write_violations)
