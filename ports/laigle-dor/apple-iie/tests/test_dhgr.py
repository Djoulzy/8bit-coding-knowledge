"""DHGR layout, MMU contracts and executed cross-bank pixel writes."""
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools import dhgr
from tools.common import Source, build_dir, video_mode, write_json, digest
from tools.machine import Machine
from tools.resources import sprite
from tools.video_layout import source_y


class LayoutTests(unittest.TestCase):
    def test_four_bytes_represent_seven_colors(self):
        # Known raw patterns: aux0, main0, aux1, main1 = $10,$64,$50,$0A.
        # Their low-first four-bit groups are 0,1,2,3,4,5,1 -> palette 0,2,4,6,8,5,2.
        main, aux = bytearray(8192), bytearray(8192)
        for x, color in enumerate([0, 2, 4, 6, 8, 5, 2]):
            dhgr.put_cell(main, aux, x, 0, color)
        serial = bytes([aux[0], main[0], aux[1], main[1]])
        # Literal independently packed from 0|1<<4|2<<8|3<<12|4<<16|5<<20|1<<24.
        self.assertEqual(serial, bytes([0x10, 0x64, 0x50, 0x0A]))
        self.assertEqual(dhgr.cells(main, aux, 0)[:7], [0, 2, 4, 6, 8, 5, 2])

    def test_palette_patterns_and_neighbors(self):
        codes = [0, 8, 1, 9, 2, 5, 3, 11, 4, 12, 10, 13, 6, 14, 7, 15]
        for color, code in enumerate(codes):
            self.assertEqual(dhgr.pattern(color), code)
            main, aux = bytearray(8192), bytearray(8192)
            for x in range(140):
                dhgr.put_cell(main, aux, x, 1, color)
            self.assertEqual(dhgr.cells(main, aux, 1), [color] * 140)
            dhgr.put_cell(main, aux, 3, 1, 15 - color)
            expected = [color] * 140; expected[3] = 15 - color
            self.assertEqual(dhgr.cells(main, aux, 1), expected)
        with self.assertRaises(ValueError):
            dhgr.put_cell(main, aux, 140, 0, 0)

    def test_sprite_pair_retains_each_dot_and_its_opacity(self):
        for sid in [40, 46, 64]:
            source = sprite(Source(), sid)
            converted = dhgr.target_sprite(source)
            self.assertEqual(converted['cell_width'], source['width_bytes'] * 3)
            for row, mask, status, policy in zip(source['pixels'], source['masks'],
                                                converted['statuses'], converted['cell_policies']):
                if policy != 'fine':
                    continue  # explicitly adapted art is checked separately
                for x, value in enumerate(status):
                    opacity = dhgr.status_mask(value)
                    self.assertEqual(opacity & 3, 3 if mask[x * 2] else 0)
                    self.assertEqual(opacity & 12, 12 if mask[x * 2 + 1] else 0)
                    if value in (10, 15):
                        self.assertEqual(row[x * 2:x * 2 + 2], [1, 1])
                    for color in (2, 5, 8, 11, 12, 13, 15):
                        rendered = dhgr.status_pattern(value, dhgr.pattern(color))
                        # Full color pairs may contain no set bit in one half;
                        # a mixed pair must retain its foreground half and hole.
                        if value not in (10, 15):
                            self.assertEqual(bool(rendered & 3), bool(row[x * 2]))
                            self.assertEqual(bool(rendered & 12), bool(row[x * 2 + 1]))
                            self.assertEqual(rendered & ~opacity, 0)
                    self.assertIn(value, (0, 1, 3, 4, 5, 7, 10, 12, 13, 15))

    def test_mixed_pairs_do_not_become_solid_blocks(self):
        source = {'id': 64, 'width_bytes': 1, 'height': 1,
                  'pixels': [[0, 1, 1, 0, 1, 1]], 'masks': [[1] * 6]}
        converted = dhgr.target_sprite(source)
        self.assertEqual(converted['statuses'], [[13, 7, 10]])
        self.assertEqual([dhgr.status_pattern(c, 15) for c in converted['statuses'][0]], [12, 3, 15])

    def test_requested_material_palette_and_anatomical_bands(self):
        self.assertEqual(dhgr.SCENE_COLORS, {3: 15, 4: 15, 5: 5, 7: 5, 8: 5,
                                           14: 8, 15: 8, 21: 13})
        self.assertEqual([dhgr.actor_color(40, y) for y in (0, 4, 5, 11, 12, 30)],
                         [13, 13, 11, 11, 12, 12])
        self.assertEqual([dhgr.actor_color(43, y) for y in (8, 9, 11, 12)],
                         [13, 11, 11, 12])
        self.assertEqual([dhgr.actor_color(64, y) for y in (9, 10, 16)], [12, 11, 11])
        for sid in range(46, 62):
            first_boot = 16 if sid < 58 else 11
            self.assertEqual(dhgr.target_sprite(sprite(Source(), sid))['colors'],
                             [2] * first_boot + [8] * (sprite(Source(), sid)['height'] - first_boot))

    def test_hair_and_legs_use_whole_color_cells(self):
        source = Source()
        for sid in [40, 41, 42, 43] + list(range(46, 62)):
            target = dhgr.target_sprite(sprite(source, sid))
            for row, policy in zip(target['statuses'], target['cell_policies']):
                if policy != 'fine':
                    self.assertTrue(set(row) <= {0, 5, 15}, sid)
                    self.assertTrue(all(dhgr.status_mask(c) in (0, 15) for c in row))
        # The original front head's checker pattern now has a solid yellow
        # crown; the opaque gap between the standing legs stays black.
        head = dhgr.target_sprite(sprite(source, 40))
        self.assertEqual(head['statuses'][2][4:8], [15] * 4)
        legs = dhgr.target_sprite(sprite(source, 46))
        self.assertEqual(legs['statuses'][6][3:9], [15, 15, 5, 15, 15, 15])
        self.assertEqual(legs['colors'][15:18], [2, 8, 8])

    def test_face_tunic_and_hands_keep_fine_opacity_and_palette(self):
        for sid in [40, 41, 42, 43, 64, 65, 67]:
            source = sprite(Source(), sid)
            target = dhgr.target_sprite(source)
            for y, material in enumerate(target['materials']):
                if material == 'hair':
                    continue
                if sid == 42 and material == 'skin':
                    continue  # explicit user-requested left-profile retouch
                self.assertEqual(target['cell_policies'][y], 'fine')
                self.assertEqual(target['colors'][y], 11 if material == 'skin' else 12)
                for k, code in enumerate(target['statuses'][y]):
                    self.assertEqual(dhgr.status_mask(code),
                                     (3 if source['masks'][y][2 * k] else 0) |
                                     (12 if source['masks'][y][2 * k + 1] else 0))

    def test_left_profile_has_uniform_skin_and_explicit_eye_mouth(self):
        target = dhgr.target_sprite(sprite(Source(), 42))
        self.assertEqual(target['statuses'][7][4:8], [15, 5, 15, 15])
        self.assertEqual(target['statuses'][10][4:8], [5, 15, 15, 15])
        for y in range(5, 13):
            self.assertEqual(target['colors'][y], 11)
            self.assertEqual(target['cell_policies'][y], 'solid')
            self.assertTrue(set(target['statuses'][y]) <= {0, 5, 15})

    def test_material_color_keeps_small_black_details_and_nonzero_marks(self):
        # Green tunic, pink skin, yellow hair, dark-blue trousers. A full
        # foreground pair takes the requested phase; an opaque black stays 0.
        for color, expected in [(12, 6), (11, 13), (13, 14), (2, 1)]:
            for code in (10, 15):
                self.assertEqual(dhgr.status_pattern(code, dhgr.pattern(color)), expected)
            self.assertEqual(dhgr.status_pattern(5, expected), 0)
            for code, visible, hole in [(7, 3, 12), (13, 12, 3)]:
                p = dhgr.status_pattern(code, expected)
                self.assertNotEqual(p & visible, 0)
                self.assertEqual(p & hole, 0)

    def test_static_materials_use_stable_color_and_keep_enclosed_dark_marks(self):
        image = [[0] * 240 for _ in range(200)]
        image[40][20:26] = [15, 0, 0, 15, 5, 5]
        image[41][20:26] = [5, 5, 5, 0, 5, 5]
        main, aux = dhgr.image_pages(image)
        y = source_y(40)
        self.assertEqual(dhgr.serial_samples(main, aux, y)[80:92],
                         [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0])
        self.assertEqual(dhgr.cells(main, aux, source_y(41))[20:23], [5, 0, 5])

    def test_signal_preview_preserves_subcell_sample_boundaries(self):
        main, aux = bytearray(8192), bytearray(8192)
        dhgr.put_pattern(main, aux, 1, 0, 3)
        self.assertEqual(dhgr.serial_samples(main, aux, 0)[4:8], [1, 1, 0, 0])
        signal = dhgr.scanline_rgb(main, aux, 0)
        # The signal model permits a fringe, but does not fill the whole cell.
        self.assertNotEqual(signal[4 * 3:6 * 3], bytes(6))
        self.assertEqual(signal[7 * 3:8 * 3], bytes(3))
        palette = dhgr.scanline_rgb(main, aux, 0, 'palette')
        self.assertNotEqual(palette[6 * 3:8 * 3], bytes(6))
        mono = dhgr.scanline_rgb(main, aux, 0, 'mono')
        self.assertEqual(mono[4 * 3:8 * 3], bytes([255] * 6 + [0] * 6))


class BankingTests(unittest.TestCase):
    def setUp(self):
        self.bus = Machine().bus

    def test_independent_read_write_and_main_zp_stack(self):
        bus = self.bus
        bus.ram[0x4000], bus.aux[0x4000] = 0x12, 0x34
        bus[0xC003] = 0
        self.assertEqual(bus[0x4000], 0x34)
        bus[0x4000] = 0x56  # RAMWRT remains main
        self.assertEqual(bus.ram[0x4000], 0x56)
        self.assertEqual(bus.aux[0x4000], 0x34)
        bus[0xC005] = 0
        bus[0x4000] = 0x78
        self.assertEqual(bus.aux[0x4000], 0x78)
        for a in (0x40, 0x80, 0x1FF):
            bus[a] = 0xA5
            self.assertEqual(bus.ram[a], 0xA5)
            self.assertEqual(bus.aux[a], 0)
        bus[0xC008] = 0
        bus[0xC009] = 0
        bus[0x80] = 0x66
        self.assertEqual(bus.aux[0x80], 0x66)

    def test_80store_override_is_limited_to_page1(self):
        bus = self.bus
        bus[0xC001] = 0; bus[0xC055] = 0; bus[0xC057] = 0
        for a in (0x400, 0x7FF, 0x2000, 0x3FFF):
            bus[a] = 0xA5
            self.assertEqual(bus.aux[a], 0xA5)
            self.assertEqual(bus.ram[a], 0)
        for a in (0x800, 0x4000, 0x6000):
            bus[a] = 0x55
            self.assertEqual(bus.ram[a], 0x55)
        self.assertEqual(bus.display_page_index(), 0)
        bus[0xC000] = 0
        self.assertEqual(bus.display_page_index(), 1)

    def test_ramrd_banks_application_fetch_too(self):
        bus = self.bus
        bus.ram[0x6000], bus.aux[0x6000] = 0xA9, 0x00
        bus[0xC003] = 0
        self.assertEqual(bus[0x6000], 0x00)
        bus[0xC002] = 0
        self.assertEqual(bus[0x6000], 0xA9)


class NativeDhgrTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = Machine(video='dhgr')
        cls.m.boot()
        cls.checked_cells = 0
        cls.checked_partial_cells = 0

    def call(self, routine):
        self.m.cpu.sp = 255
        self.m.cpu.stPushWord(0x01FF)
        self.m.cpu.pc = self.m.symbols[routine]
        self.m.until(0x200, 100000)
        self.assertEqual(self.m.cpu.sp, 255)

    def test_palette_writes_all_phases_and_both_pages(self):
        m = self.m
        m.bus.switches['TEXT'] = 1
        checked = 0
        for page in (0x2000, 0x4000):
            for x in list(range(14)) + [139]:
                for color in range(16):
                    main = bytes((i * 11 + 9) & 127 for i in range(8192))
                    aux = bytes((i * 17 + 21) & 127 for i in range(8192))
                    m.bus.ram[page:page + 8192] = main
                    m.bus.aux[page:page + 8192] = aux
                    m.bus.ram[m.symbols['dst_ptr']] = 0
                    m.bus.ram[m.symbols['dst_ptr'] + 1] = page >> 8
                    m.bus.ram[m.symbols['cell_x']] = x
                    m.bus.ram[m.symbols['cell_color']] = dhgr.pattern(color)
                    self.call('draw_cell')
                    em, ea = bytearray(main), bytearray(aux)
                    dhgr.put_cell(em, ea, x, 0, color)
                    self.assertEqual(bytes(m.bus.ram[page:page + 8192]), em)
                    self.assertEqual(bytes(m.bus.aux[page:page + 8192]), ea)
                    self.assertEqual(m.bus.switches['RAMRD'], 0)
                    self.assertEqual(m.bus.switches['RAMWRT'], 0)
                    checked += 1
        type(self).checked_cells = checked

    def test_bank_workers_execute_from_main_zero_page(self):
        m = self.m
        self.assertTrue(m.ramrd_fetch_pcs)
        self.assertTrue(all(0x40 <= pc < 0x60 for pc in m.ramrd_fetch_pcs))
        self.assertEqual(m.bus.aux[0x6000:0xA000], bytes(0x4000))
        self.assertEqual(m.symbols['aux_read_src'], 0x40)
        self.assertGreaterEqual(m.symbols['aux_read_dst'], 0x40)
        self.assertLess(m.symbols['aux_read_dst'], 0x60)

    def test_partial_cell_dots_and_opacity_preserve_siblings(self):
        m = self.m
        m.bus.switches['TEXT'] = 1
        checked = 0
        for page in (0x2000, 0x4000):
            for x in list(range(14)) + [139]:
                for opacity in (3, 12):
                    for code in (0, opacity):
                        main = bytes((i * 11 + 9) & 127 for i in range(8192))
                        aux = bytes((i * 17 + 21) & 127 for i in range(8192))
                        m.bus.ram[page:page + 8192] = main
                        m.bus.aux[page:page + 8192] = aux
                        m.bus.ram[m.symbols['dst_ptr']] = 0
                        m.bus.ram[m.symbols['dst_ptr'] + 1] = page >> 8
                        m.bus.ram[m.symbols['cell_x']] = x
                        m.bus.ram[m.symbols['cell_color']] = code
                        m.bus.ram[m.symbols['cell_mask']] = opacity
                        self.call('draw_masked_cell')
                        em, ea = bytearray(main), bytearray(aux)
                        dhgr.put_pattern(em, ea, x, 0, code, opacity)
                        self.assertEqual(bytes(m.bus.ram[page:page + 8192]), em)
                        self.assertEqual(bytes(m.bus.aux[page:page + 8192]), ea)
                        checked += 1
        type(self).checked_partial_cells = checked

    @classmethod
    def tearDownClass(cls):
        write_json(build_dir('dhgr') / 'dhgr-pixel-verification.json', {
            'method': 'executed NMOS draw_cell plus safe auxiliary-read workers',
            'palette_boundary_cases': cls.checked_cells,
            'partial_cell_cases': cls.checked_partial_cells,
            'ramrd_fetch_pcs': sorted(cls.m.ramrd_fetch_pcs),
            'mirrored_application_code': False,
            'program_sha256': digest((build_dir('dhgr') / 'game.bin').read_bytes()),
            'real_hardware': 'not tested'})


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    for cls in (LayoutTests, BankingTests):
        suite.addTests(loader.loadTestsFromTestCase(cls))
    if video_mode() == 'dhgr':
        suite.addTests(loader.loadTestsFromTestCase(NativeDhgrTests))
    return suite
