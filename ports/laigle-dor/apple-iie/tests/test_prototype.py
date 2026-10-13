import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.common import ROOT, Source, digest, write_json, build_dir, video_mode
from tools.disk import offset, make_disk, nibble_tracks
from tools.machine import Machine
from tools.preview import reference_page, png
from tools.resources import frames, row_offset, sprite
from tools.hgr_color import target_sprite
from tools import dhgr
from tools.video_layout import source_y, text_address, BASELINE, HGR_HEIGHT, STATE, EVENT_LOG
from model.world import Room
from model.movement import Actor, probe, room12_grid


class ResourceTests(unittest.TestCase):
    def test_pinned_inputs_and_export_references(self):
        source = Source()
        manifest = json.loads((build_dir() / 'resources/manifest.json').read_text())
        for entry in manifest['exports']:
            data = (build_dir() / 'resources' / entry['file']).read_bytes()
            self.assertEqual(digest(data), entry['sha256'])
            if 'cpu_start' in entry:
                self.assertEqual(data, source.read(entry['cpu_start'], entry['length'], entry['source_block']))
        self.assertEqual(len((build_dir() / 'resources/world-initial.bin').read_bytes()), 512)
        self.assertEqual((build_dir() / 'resources/scroll2.bin').read_bytes()[-1], 92)

    def test_room_fields_and_links(self):
        snapshot = Source().read(0x5600, 512)
        room = Room.decode(snapshot, 12)
        self.assertEqual((room.geometry, room.light, room.furnishing, room.fields[:4]),
                         (1, 3, 2, (1, 0, 3, 0)))
        self.assertEqual([room.transition(i) for i in range(4)], [(12, 0), (11, 1), (0, 3), (0, 3)])
        self.assertEqual(sum(r.treasure > 0 for r in [Room.decode(snapshot, i) for i in range(64)]) > 0, True)
        with self.assertRaises(ValueError):
            Room.decode(snapshot, 64)

    def test_rows_and_viewport(self):
        addresses = {row_offset(y) + x for y in range(192) for x in range(40)}
        self.assertEqual(len(addresses), 7680)
        self.assertLess(max(addresses), 8192)
        self.assertEqual({source_y(y) for y in range(35, 200)}, set(range(160)))
        self.assertIsNone(source_y(34))
        self.assertEqual(source_y(199), 159)
        self.assertEqual([text_address(y) for y in range(20, 24)], [0x650, 0x6D0, 0x750, 0x7D0])
        self.assertEqual([text_address(y, 1) for y in range(20, 24)], [0xA50, 0xAD0, 0xB50, 0xBD0])
        with self.assertRaises(ValueError):
            row_offset(192)

    def test_atlas_control_and_motion_domain(self):
        source = Source()
        self.assertEqual(len(frames(source)), 16)
        for f in frames(source):
            self.assertIn(f['event'], [20, 22])
        # $22 has bit 5 set: graphic data, not an ink attribute.
        atlas = sprite(source, 48)
        raw = source.read(atlas['source_start'], atlas['width_bytes'] * atlas['height'])
        row, column = divmod(raw.index(0x22), atlas['width_bytes'])
        self.assertEqual(atlas['pixels'][row][column * 6:column * 6 + 6], [1, 0, 0, 0, 1, 0])
        with self.assertRaises(ValueError):
            sprite(source, 39)

    def test_ink_independence_and_native_attribute_transparency(self):
        source = Source()
        atlas = sprite(source, 40)
        pointer, width, height = atlas['source_start'], atlas['width_bytes'], atlas['height']
        # Change only actual ink controls in a private copy of the payload.
        # This must not change either Apple pixels or their opacity.
        original = source.read(pointer, width * height)
        data = bytearray(source.blocks[2])
        for i, value in enumerate(original):
            if not value & 0x60 and value < 8:
                data[pointer - 0x501 + i] = 0
                y, column = divmod(i, width)
                self.assertEqual(atlas['masks'][y][column * 6:column * 6 + 6], [0] * 6)
        source.blocks[2] = bytes(data)
        converted = sprite(source, 40)
        self.assertEqual(converted['pixels'], atlas['pixels'])
        self.assertEqual(converted['masks'], atlas['masks'])
        self.assertTrue(any(not v for row in atlas['masks'] for v in row))

    def test_disk_order_and_capacity(self):
        disk = (build_dir() / 'laigle-dor.do').read_bytes()
        data = (build_dir() / 'game.bin').read_bytes()
        reconstructed = b''.join(disk[offset(*divmod(i, 16)):offset(*divmod(i, 16)) + 256]
                                 for i in range(1, (len(data) + 255) // 256 + 1))
        self.assertEqual(reconstructed[:len(data)], data)
        self.assertEqual(len(disk), 143360)
        self.assertEqual(len((build_dir() / 'laigle-dor.nib').read_bytes()), 35 * 6656)
        with self.assertRaises(ValueError):
            make_disk(bytes(256), data)
        with self.assertRaises(ValueError):
            make_disk(b'\x01' + bytes(255), bytes(0x6001))


class ExecutedCpuTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = Machine()
        cls.m.until(0x6000)
        cls.loaded = bytes(cls.m.bus.ram[0x6000:0x6000 + len((build_dir() / 'game.bin').read_bytes())])
        cls.boot_instructions = cls.m.instructions
        cls.m.until(cls.m.symbols['main_loop'])
        cls.initial_page = cls.m.displayed_page()
        cls.initial_text = cls.m.text_rows()
        cls.snapshot = Source().read(0x5600, 512)
        cls.room = Room.decode(cls.snapshot, 12)
        cls.grid = room12_grid(cls.room)
        cls.baseline = bytes(cls.m.bus.ram[BASELINE:BASELINE + 8192])
        cls.program = (build_dir() / 'game.bin').read_bytes()
        cls.completed_collision_cases = 0
        cls.completed_sprite_cases = 0
        cls.boot_ram = bytes(cls.m.bus.ram)
        cls.boot_aux = bytes(cls.m.bus.aux)
        cls.aux_baseline = bytes(cls.m.bus.aux[BASELINE:BASELINE + 8192])
        cls.boot_switches = dict(cls.m.bus.switches)
        cls.hidden_frame_count = 0
        cls.largest_frame_graphics_write_set = 0

    def setUp(self):
        self.m.bus.ram[:] = self.boot_ram
        self.m.bus.aux[:] = self.boot_aux
        self.m.bus.switches = dict(self.boot_switches)
        self.m.bus.key, self.m.bus.strobe = 0, False
        self.m.bus.io.clear()
        self.m.bus.page_flips.clear()
        self.m.bus.writes.clear()
        self.m.bus.frame_graphics_writes.clear()
        self.m.bus.bank_graphics_writes.clear()
        self.m.bus.bank_writes.clear()
        self.m.bus.visible_write_violations.clear()
        self.m.bus.visible_text_write_violations.clear()
        self.m.cpu.sp = 255
        self.m.cpu.p &= ~self.m.cpu.DECIMAL
        self.call('game_reset')
        self.m.cpu.pc = self.m.symbols['main_loop']

    def call(self, name):
        self.m.cpu.stPushWord(0x01FF)  # RTS target $0200 sentinel
        self.m.cpu.pc = self.m.symbols[name]
        self.m.until(0x0200, 1000000)
        self.assertEqual(self.m.cpu.sp, 255)

    def put(self, name, value):
        self.m.bus.ram[self.m.symbols[name]] = value

    def test_actual_boot0_and_loader(self):
        self.assertEqual(self.loaded, self.program)
        self.assertIn(0xC600, self.m.pcs)
        self.assertIn(0x0801, self.m.pcs)
        self.assertGreater(self.boot_instructions, 0)
        self.assertFalse(self.m.bus.motor)
        self.assertEqual(self.initial_page, reference_page(19, 140, 0))
        self.assertEqual(self.baseline, (build_dir() / 'resources/room12.hgr').read_bytes())
        for name in ['80STORE', 'RAMRD', 'RAMWRT', 'ALTZP', 'TEXT']:
            self.assertEqual(self.m.bus.switches[name], 0)
        self.assertEqual(self.m.bus.switches['80COL'], int(video_mode() == 'dhgr'))
        if video_mode() == 'dhgr':
            self.assertEqual(self.aux_baseline, (build_dir() / 'resources/room12-aux.hgr').read_bytes())
            self.assertEqual(self.m.bus.switches['DHIRES'], 1)
        self.assertEqual(self.m.bus.switches['MIXED'], 1)
        self.assertEqual(self.m.bus.switches['PAGE2'], 1)
        self.assertEqual(self.m.bus.switches['HIRES'], 1)

    def test_keyboard_controller_and_no_key_continuation(self):
        actor = Actor()
        events = []
        trace = [10, None, None, None, None, 32, 21, 21, None, None, None, None, None, None,
                 65, 8, 32, 8, 8, None, None, None, None, 32, 11, 11, None, 32, 0x3E]
        normalized = {10: 0, 11: 3, 8: 2, 21: 1, 32: 4, 65: 5}
        for tick, key in enumerate(trace, 1):
            events.extend(actor.tick(normalized.get(key), self.grid, self.room))
            state = self.m.frame(key)
            for name, expected in [('actor_x', actor.x), ('actor_y', actor.y),
                                   ('facing', actor.facing), ('pose', actor.pose),
                                   ('walking', actor.walking), ('walk_phase', actor.phase),
                                   ('frame_id', actor.frame)]:
                self.assertEqual(state[name], expected, (tick, key, name))
            self.assertEqual(self.m.displayed_page(),
                             reference_page(actor.x, actor.y, actor.frame), (tick, key))
            self.assertFalse(self.m.bus.strobe)
        self.assertEqual([e['kind'] for e in self.m.events()], events)
        self.assertIn(3, events)  # reaches right-room portal
        self.assertIn(4, events)  # floor/blocked wall
        self.assertEqual(self.m.bus.speaker_accesses, 0)
        (build_dir() / 'test-screen.png').write_bytes(png(self.m.displayed_page(), self.m.text_rows()))

    def test_collision_cpu_against_bounded_oracle(self):
        count = 0
        for x in range(3, 38, 2):
            for y in [140, 150, 160, 170, 180]:
                for facing in range(4):
                    self.put('actor_x', x); self.put('actor_y', y); self.put('facing', facing)
                    self.call('collision_probe')
                    b, d, o = probe(self.grid, self.room, x, y, facing)
                    state = self.m.state()
                    self.assertEqual((state['blocked'], state['door_status'], state['object_status']),
                                     (int(b), d, o), (x, y, facing))
                    count += 1
        self.assertEqual(count, 360)
        type(self).completed_collision_cases = count
        self.put('actor_x', 255); self.call('collision_probe')
        self.assertEqual(self.m.state()['blocked'], 1)

    def test_masks_phases_and_right_bottom_clipping(self):
        fs = frames(Source())
        used = sorted({r[0] for f in fs for r in f['layers']})
        checked = 0
        for sid in used:
            for page_address in [0x2000, 0x4000]:
                for x, y in [(i, 140) for i in range(7)] + [(39, 199), (0, 34), (0, 0)]:
                    if video_mode() == 'dhgr':
                        self.m.bus.switches['TEXT'] = 1
                        main = bytes((i * 13 + (i >> 6)) & 127 for i in range(8192))
                        aux = bytes((i * 19 + (i >> 5)) & 127 for i in range(8192))
                        self.m.bus.ram[page_address:page_address + 8192] = main
                        self.m.bus.aux[page_address:page_address + 8192] = aux
                        self.put('draw_page_hi', page_address >> 8)
                        self.put('render_page_index', int(page_address == 0x4000))
                        self.put('actor_x', x); self.put('actor_y', y)
                        self.put('sprite_index', used.index(sid)); self.put('dx', 0); self.put('dy', 0)
                        expected_main, expected_aux = bytearray(main), bytearray(aux)
                        dhgr.reference_layer(expected_main, expected_aux,
                                             dhgr.target_sprite(sprite(Source(), sid)), x, y)
                        self.call('draw_sprite')
                        self.assertEqual(bytes(self.m.bus.ram[page_address:page_address + 8192]),
                                         expected_main, ('main', sid, x, y))
                        self.assertEqual(bytes(self.m.bus.aux[page_address:page_address + 8192]),
                                         expected_aux, ('aux', sid, x, y))
                        checked += 1
                        continue
                    # Draw just one layer over nonuniform bytes to catch edge-mask bugs.
                    page = bytes((i * 13 + (i >> 6)) & (255 if video_mode() == 'color' else 127)
                                 for i in range(8192))
                    self.m.bus.switches['TEXT'] = 1  # isolated worker, no active presentation
                    self.m.bus.ram[page_address:page_address + 8192] = page
                    self.put('draw_page_hi', page_address >> 8)
                    self.m.bus.ram[self.m.symbols['render_page_index']] = int(page_address == 0x4000)
                    self.put('actor_x', x); self.put('actor_y', y)
                    self.m.bus.ram[self.m.symbols['sprite_index']] = used.index(sid)
                    self.m.bus.ram[self.m.symbols['dx']] = self.m.bus.ram[self.m.symbols['dy']] = 0
                    s = target_sprite(sprite(Source(), sid), video_mode())
                    expected = bytearray(page)
                    left = 20 + (x + 1) * 6
                    for j, row in enumerate(s['pixels']):
                        ty = source_y(y + j)
                        if ty is None:
                            continue
                        base = row_offset(ty)
                        for k, v in enumerate(row):
                            if not s['masks'][j][k]:
                                continue
                            tx = left + k
                            if tx >= 280:
                                continue
                            a, bit = base + tx // 7, 1 << (tx % 7)
                            expected[a] = expected[a] | bit if v else expected[a] & (255 ^ bit)
                            if video_mode() == 'color':
                                expected[a] = (expected[a] & 127) | s['color_phase']
                    self.call('draw_sprite')
                    self.assertEqual(bytes(self.m.bus.ram[page_address:page_address + 8192]),
                                     bytes(expected), (page_address, sid, x, y))
                    checked += 1
        self.assertEqual(checked, 460)
        type(self).completed_sprite_cases = checked

    def test_aliases_case_and_reset(self):
        self.m.frame(ord('k')); self.assertEqual(self.m.state()['facing'], 1)
        self.m.frame(ord('k')); self.assertEqual(self.m.state()['walking'], 1)
        self.m.frame(ord('a')); self.assertEqual(self.m.state()['pose'], 5)
        self.m.frame(ord('r')); self.assertEqual(self.m.state()['actor_x'], 19)
        self.assertEqual(self.m.state()['actor_y'], 140)
        self.assertEqual(self.m.state()['event_count'], 0)

    def test_memory_ownership_event_ring_and_tick_wrap(self):
        self.m.bus.writes.clear()
        self.put('tick_lo', 255)
        self.m.frame(32)
        self.assertEqual(self.m.state()['tick_hi'], 1)
        for i in range(70):
            self.m.cpu.a = 1
            self.call('log_event')
        self.assertEqual(len(self.m.events()), 64)
        self.assertEqual(self.m.state()['event_overflow'], 6)
        self.assertEqual(bytes(self.m.bus.ram[0x6000:0x6000 + len(self.program)]), self.program)
        self.assertEqual(bytes(self.m.bus.ram[BASELINE:BASELINE + 8192]), self.baseline)
        if video_mode() == 'dhgr':
            self.assertEqual(bytes(self.m.bus.aux[BASELINE:BASELINE + 8192]), self.aux_baseline)
            for bank, a in self.m.bus.bank_writes:
                if bank:
                    self.assertTrue(0x2000 <= a < 0x6000 or
                                    any(text_address(row, p) <= a < text_address(row, p) + 40
                                        for p in [0, 1] for row in range(20, 24)), ('Aux ownership', a))
        for a in self.m.bus.writes:
            self.assertTrue(0x80 <= a <= (0xB6 if video_mode() == 'dhgr' else 0xAA) or 0x100 <= a < 0x200 or
                            STATE <= a <= STATE + 28 or (video_mode() == 'dhgr' and 0xE00 <= a < 0xE28) or EVENT_LOG <= a < EVENT_LOG + 256 or
                            0x2000 <= a < 0x6000 or
                            any(text_address(row, p) <= a < text_address(row, p) + 40
                                for p in [0, 1] for row in range(20, 24)),
                            'Unowned runtime write $%04X' % a)

    def test_double_buffer_dirty_repair_and_vblank_presentation(self):
        # Repeated per-page repairs across walking, turning, crouch, portal and
        # restart. A full redraw oracle catches trails on either older frame.
        keys = [10, None, None, None, 32, 21, 21, None, None, None, None, None,
                65, 8, 32, 8, 8, None, None, 82] * 3
        for key in keys:
            previous = self.m.bus.switches['PAGE2']
            visible_base = 0x4000 if previous else 0x2000
            old_graphics = self.m.displayed_page()
            old_text = self.m.text_rows()
            self.m.bus.frame_graphics_writes.clear()
            self.m.bus.bank_graphics_writes.clear()
            self.m.bus.writes.clear()
            self.m.bus.press(key) if key is not None else None
            self.m.step()
            self.m.until(self.m.symbols['present_flip'])
            self.assertEqual(self.m.displayed_page(), old_graphics)
            self.assertEqual(self.m.text_rows(), old_text)
            hidden_base = 0x2000 if previous else 0x4000
            self.assertTrue(all(hidden_base <= a < hidden_base + 8192
                                for a in self.m.bus.frame_graphics_writes))
            write_count = len(self.m.bus.bank_graphics_writes)
            self.assertLess(write_count, 2048 if video_mode() == 'dhgr' else 1024)
            type(self).largest_frame_graphics_write_set = max(
                self.largest_frame_graphics_write_set, write_count)
            self.m.until(self.m.symbols['main_loop'])
            self.assertEqual(self.m.bus.switches['PAGE2'], previous ^ 1)
            self.assertTrue(self.m.bus.page_flips[-1]['in_vblank'])
            for name in ('RAMRD', 'RAMWRT', 'ALTZP', '80STORE'):
                self.assertEqual(self.m.bus.switches[name], 0, name)
            s = self.m.state()
            self.assertEqual(self.m.displayed_page(), reference_page(s['actor_x'], s['actor_y'], s['frame_id']))
            type(self).hidden_frame_count += 1
        self.assertFalse(self.m.bus.visible_write_violations)
        self.assertFalse(self.m.bus.visible_text_write_violations)
        self.assertEqual(bytes(self.m.bus.ram[BASELINE:BASELINE + 8192]), self.baseline)

    def test_native_mixed_text_follows_selected_page(self):
        for key in [None, 10, None, 65, 32, 82]:
            s = self.m.frame(key)
            width = 80 if video_mode() == 'dhgr' else 40
            lines = [bytes(c & 127 for c in row).decode() for row in self.m.text_rows()]
            self.assertEqual(lines[0], 'FORCES:100% POINTS:00000 OR:00500'.ljust(width))
            self.assertEqual(lines[1], ('SALLE:12 X:%02d Y:%03d MAIN:VIDE' %
                                      (s['actor_x'], s['actor_y'])).ljust(width))
            self.assertEqual(lines[3], 'FLECHES:MARCHE A:ACCROUPI ESPACE:STOP'.ljust(width))
            self.assertTrue(all(code >= 128 for row in self.m.text_rows() for code in row))
            self.assertNotIn(STATE, range(0x400, 0xC00))
            self.assertNotIn(EVENT_LOG, range(0x400, 0xC00))

    def test_presentation_waits_for_fresh_blank_when_already_blank(self):
        self.m.cpu.processorCycles = 192 * 65 + 100
        self.put('draw_page_hi', 0x20)
        self.call('present_frame')
        flip = self.m.bus.page_flips[-1]
        self.assertTrue(flip['in_vblank'])
        self.assertGreaterEqual(flip['cycles'], 262 * 65 + 192 * 65)

    @classmethod
    def tearDownClass(cls):
        write_json(build_dir() / 'cpu-verification.json', {
            'method': 'executed py65 NMOS CPU, stock Disk II BOOT0, simplified device bus',
            'video_profile': video_mode(),
            'boot_instructions': cls.boot_instructions,
            'checked_collision_cases': cls.completed_collision_cases,
            'checked_sprite_phase_edge_cases': cls.completed_sprite_cases,
            'runtime_speaker_accesses': cls.m.bus.speaker_accesses,
            'minimum_stack_pointer': cls.m.min_sp,
            'hidden_frames_checked': cls.hidden_frame_count,
            'largest_distinct_frame_graphics_write_set': cls.largest_frame_graphics_write_set,
            'page_flip_sync': 'fresh blank edge in simplified NTSC RDVBLBAR model',
            'program_sha256': digest(cls.program),
            'coverage': 'subset harness; not real hardware or original Oric gameplay'})
