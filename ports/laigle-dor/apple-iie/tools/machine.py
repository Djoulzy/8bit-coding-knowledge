"""Functional Apple IIe subset around py65, with executed Disk II BOOT0.

Not a cycle/bus accurate Apple emulator: no floating bus, full video clock,
NMI/IRQ, analog drive, write channel, ROM cold-start or real-time certification.
Nibble reads advance one byte per access, sufficient to exercise real BOOT0
decoding/loader code. ROM is loaded read-only, keyboard latches/strobe modeled.
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.common import ROOT, load_py65, labels, digest, build_dir, video_mode
from tools.disk import nibble_tracks
from tools.video_layout import text_address, EVENT_LOG


class Bus:
    def __init__(self, disk, system_rom=None):
        self.ram = bytearray(65536)
        self.aux = bytearray(65536)  # functional 64 KiB extended 80-column bank
        self.diskrom = (ROOT / 'local/roms/disk2.rom').read_bytes()
        self.rom = system_rom if system_rom is not None else (ROOT / 'local/roms/apple2e.rom').read_bytes()
        if digest(self.diskrom) != 'de1e3e035878bab43d0af8fe38f5839c527e9548647036598ee6fe7ec74d2a7d':
            raise ValueError('Unexpected Disk II ROM')
        if digest(self.rom) not in ('1fb812584c6633fa16b77b20915986ed1178d1e6fc07a647f7ee8d4e6ab9d40b',
                'aab38a03ca8deabbb2f868733148c2efd6f655a59cd9c5d058ef3e0b7aa86a1a'):
            raise ValueError('Unexpected Apple IIe ROM')
        self.tracks = nibble_tracks(disk)
        self.half_track, self.coil, self.nibble = 0, 0, 0
        self.motor = False
        self.key = 0
        self.strobe = False
        self.writes = set()
        self.io = []
        self.switches = {'80STORE': 0, 'RAMRD': 0, 'RAMWRT': 0, 'ALTZP': 0,
                         '80COL': 0, 'ALTCHAR': 0, 'PAGE2': 0, 'HIRES': 0,
                         'MIXED': 1, 'TEXT': 1, 'INTCXROM': 0, 'SLOTC3ROM': 0,
                         'DHIRES': 0}
        self.speaker_accesses = 0
        self.clock = lambda: 0
        self.page_flips = []
        self.frame_graphics_writes = set()
        self.visible_write_violations = []
        self.visible_text_write_violations = []
        self.vblank_reads = 0
        self.bank_writes = set()
        self.bank_graphics_writes = set()

    def dhgr_active(self):
        return self.switches['DHIRES'] and self.switches['80COL'] and self.switches['HIRES']

    def display_page_index(self):
        return 0 if self.switches['80STORE'] else self.switches['PAGE2']

    def memory_bank(self, address, write=False):
        if address < 0x200:
            return self.switches['ALTZP']
        if self.switches['80STORE'] and (0x400 <= address < 0x800 or
                self.switches['HIRES'] and 0x2000 <= address < 0x4000):
            return self.switches['PAGE2']
        return self.switches['RAMWRT' if write else 'RAMRD']

    def in_vblank(self):
        # Simplified NTSC phase model, not a complete IOU video scanner.
        return self.clock() % (262 * 65) >= 192 * 65

    def press(self, key):
        if self.strobe:
            raise ValueError('Keyboard latch still pending')
        self.key, self.strobe = key & 127, True

    def access(self, address, write=False):
        if address == 0xC000 and not write:
            return self.key | (128 if self.strobe else 0)
        if address == 0xC010:
            self.strobe = False
            return 0
        if address == 0xC019:
            self.vblank_reads += 1
            return 0 if self.in_vblank() else 128  # IIe RDVBLBAR
        if address == 0xC030:
            self.speaker_accesses += 1
        mapping = {0xC000: ('80STORE', 0), 0xC001: ('80STORE', 1),
                   0xC002: ('RAMRD', 0), 0xC003: ('RAMRD', 1),
                   0xC004: ('RAMWRT', 0), 0xC005: ('RAMWRT', 1),
                   0xC006: ('INTCXROM', 0), 0xC007: ('INTCXROM', 1),
                   0xC008: ('ALTZP', 0), 0xC009: ('ALTZP', 1),
                   0xC00A: ('SLOTC3ROM', 0), 0xC00B: ('SLOTC3ROM', 1),
                   0xC00C: ('80COL', 0), 0xC00D: ('80COL', 1),
                   0xC00E: ('ALTCHAR', 0), 0xC00F: ('ALTCHAR', 1),
                   0xC050: ('TEXT', 0), 0xC051: ('TEXT', 1),
                   0xC052: ('MIXED', 0), 0xC053: ('MIXED', 1),
                   0xC054: ('PAGE2', 0), 0xC055: ('PAGE2', 1),
                   0xC056: ('HIRES', 0), 0xC057: ('HIRES', 1),
                   0xC05E: ('DHIRES', 1), 0xC05F: ('DHIRES', 0)}
        if address in mapping and (write or address >= 0xC050):
            name, value = mapping[address]
            self.switches[name] = value
            self.io.append(('write' if write else 'read', address, name, value))
            if address in [0xC054, 0xC055]:
                self.page_flips.append({'page': value, 'cycles': self.clock(),
                                        'in_vblank': self.in_vblank()})
        if 0xC0E0 <= address <= 0xC0E7:
            new = (address - 0xC0E0) // 2
            if address & 1:
                delta = (new - self.coil) % 4
                if delta in [1, 3]:
                    old_track = self.half_track // 2
                    self.half_track = max(0, min(68, self.half_track + (1 if delta == 1 else -1)))
                    if old_track != self.half_track // 2:
                        self.nibble = 0
                self.coil = new
        if address == 0xC0E8:
            self.motor = False
        if address == 0xC0E9:
            self.motor = True
        if address == 0xC0EC:
            if not self.motor:
                return 0
            track = self.tracks[self.half_track // 2]
            result = track[self.nibble]
            self.nibble = (self.nibble + 1) % len(track)
            return result
        return 0

    def __getitem__(self, address):
        if isinstance(address, slice):
            return bytes(self[i] for i in range(*address.indices(65536)))
        if 0xC000 <= address < 0xC100:
            return self.access(address)
        if 0xC600 <= address < 0xC700:
            return self.diskrom[address - 0xC600]
        if address >= 0xC100:
            return self.rom[address - 0xC000]
        return (self.aux if self.memory_bank(address) else self.ram)[address]

    def __setitem__(self, address, value):
        if 0xC000 <= address < 0xC100:
            self.access(address, True)
        elif address >= 0xC100:
            raise ValueError('Unexpected ROM write $%04X' % address)
        else:
            bank = self.memory_bank(address, True)
            if self.switches['MIXED'] and not self.switches['TEXT']:
                for row in range(20, 24):
                    start = text_address(row, self.display_page_index())
                    if start <= address < start + 40 and (not bank or self.switches['80COL']):
                        self.visible_text_write_violations.append((bank, address))
            if 0x2000 <= address < 0x6000:
                self.frame_graphics_writes.add(address)
                self.bank_graphics_writes.add((bank, address))
                visible = 0x4000 if self.display_page_index() else 0x2000
                if not self.switches['TEXT'] and visible <= address < visible + 8192 and (not bank or self.dhgr_active()):
                    self.visible_write_violations.append((bank, address))
            (self.aux if bank else self.ram)[address] = value
            self.writes.add(address)
            self.bank_writes.add((bank, address))


class Machine:
    def __init__(self, disk=None, video=None, directory=None):
        self.video = video or video_mode()
        self.directory = Path(directory) if directory is not None else build_dir(self.video)
        self.symbols = labels(self.directory)
        system_rom=None
        if 'world_load_scene' in self.symbols:
            from tools.roms import supplied_rom
            system_rom=supplied_rom('apple')[0]
        self.bus = Bus(disk if disk is not None else (self.directory / 'laigle-dor.do').read_bytes(),system_rom)
        self.cpu = load_py65()(memory=self.bus, pc=0xC600)
        self.bus.clock = lambda: self.cpu.processorCycles
        self.instructions = 0
        self.min_sp = 255
        self.pcs = set()
        self.ramrd_fetch_pcs = set()

    def step(self):
        if self.bus.switches['RAMRD']:
            self.ramrd_fetch_pcs.add(self.cpu.pc)
        opcode = self.bus[self.cpu.pc]
        if self.cpu.disassemble[opcode][0] == '???':
            raise ValueError('Undocumented opcode $%02X at $%04X' % (opcode, self.cpu.pc))
        self.pcs.add(self.cpu.pc)
        self.cpu.step()
        self.instructions += 1
        self.min_sp = min(self.min_sp, self.cpu.sp)

    def until(self, address, budget=10000000):
        for _ in range(budget):
            if self.cpu.pc == address:
                return
            self.step()
        raise TimeoutError('CPU budget exceeded; PC=$%04X track=%d sector=%d' %
                           (self.cpu.pc, self.bus.half_track // 2, self.bus.ram[0x3D]))

    def boot(self):
        self.until(self.symbols['main_loop'])
        return self.state()

    def frame(self, key=None):
        if key is not None:
            self.bus.press(key)
        self.step()  # currently at main_loop
        self.until(self.symbols['main_loop'], 3000000 if 'world_load_scene' in self.symbols else 1000000)
        return self.state()

    def state(self):
        names = ['actor_x', 'actor_y', 'facing', 'pose', 'walking', 'walk_phase',
                 'tick_lo', 'tick_hi', 'last_event', 'event_head', 'event_count',
                 'event_overflow', 'frame_id', 'blocked', 'door_status', 'object_status',
                 'display_page_hi', 'draw_page_hi']
        if 'world_load_scene' in self.symbols:
            names += ['current_room','game_mode','room_dirty','held_item','objectives',
                      'room_geometry','room_light','room_treasure','room_furnishing',
                      'possessions','scrolls','vials','torches','ropes','crowbars',
                      'in_pit','action_kind','action_phase','enemy_kind']
        result={name: self.bus.ram[self.symbols[name]] for name in names}
        if 'world_load_scene' in self.symbols:
            for name in ['gold','points','energy','drain','torch_life','rng_state']:
                a=self.symbols[name];value=int.from_bytes(self.bus.ram[a:a+2],'little')
                result[name]=value-65536 if name=='energy' and value>=32768 else value
        return result

    def events(self):
        state = self.state()
        head, count = state['event_head'], state['event_count']
        result = []
        for n in range(count):
            a = EVENT_LOG + ((head - count + n) & 63) * 4
            kind, lo, hi, arg = self.bus.ram[a:a + 4]
            result.append({'kind': kind, 'tick': lo + 256 * hi, 'argument': arg})
        return result

    def displayed_page(self):
        address = 0x4000 if self.bus.display_page_index() else 0x2000
        main = bytes(self.bus.ram[address:address + 8192])
        return (main, bytes(self.bus.aux[address:address + 8192])) if self.bus.dhgr_active() else main

    def text_rows(self, all_rows=False):
        page = self.bus.display_page_index()
        result = []
        for row in range(24) if all_rows else range(20,24):
            address = text_address(row, page)
            main = self.bus.ram[address:address + 40]
            if self.bus.switches['80COL']:
                aux = self.bus.aux[address:address + 40]
                result.append(bytes(v for pair in zip(aux, main) for v in pair))
            else:
                result.append(bytes(main))
        return result

    def screen_png(self, monitor='color'):
        from tools.preview import png,text_png
        if self.bus.switches['TEXT']:
            return text_png(self.text_rows(all_rows=True))
        return png(self.displayed_page(),self.text_rows() if self.bus.switches['MIXED'] else None,
                   self.video,monitor)
