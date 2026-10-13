"""Native HGR pattern contracts, separate from executed sprite byte comparisons."""
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.common import Source, build_dir, video_mode
from tools.hgr_color import RGB, target_sprite, scanline_rgb, write_cell
from tools.resources import sprite, row_offset
from tools.preview import png


class ColorTests(unittest.TestCase):
    def test_native_palette_patterns_and_byte_parity(self):
        # Expected literals: alternating byte parity follows seven dots per byte.
        patterns = {1: (0x55, 0x2A), 2: (0x2A, 0x55), 3: (0x7F, 0x7F),
                    5: (0xAA, 0xD5), 6: (0xD5, 0xAA), 0: (0x00, 0x00)}
        for color, pattern in patterns.items():
            page = bytearray(8192)
            for x in range(0, 280, 2):
                write_cell(page, 0, x, color)
            self.assertEqual(bytes(page[:40]), bytes(pattern) * 20, color)
            decoded = scanline_rgb(page[:40])
            if color not in (0, 3):
                parity = 0 if color in (1, 6) else 1
                for x in range(parity, 280, 2):
                    self.assertEqual(tuple(decoded[x * 3:x * 3 + 3]), RGB[color], (color, x))
            else:
                self.assertEqual(decoded, bytes(RGB[color]) * 280)

    def test_color_white_neighbors_include_byte_boundary(self):
        row = bytearray(40)
        row[0], row[1] = 0x40, 0x01  # global dots 6 and 7, crossing the byte edge
        data = scanline_rgb(row)
        self.assertEqual(data[6 * 3:8 * 3], bytes((255, 255, 255)) * 2)
        row[0], row[1] = 0xC0, 0x00  # isolated even dot, high phase: blue
        data = scanline_rgb(row)
        self.assertEqual(tuple(data[18:21]), RGB[6])
        self.assertEqual(data[21:24], bytes(3))

    def test_pair_conversion_preserves_ink_transparency_and_color(self):
        source = Source()
        for sid in [40, 46, 64]:
            raw = sprite(source, sid)
            colored = target_sprite(raw, 'color')
            self.assertEqual(colored['color_phase'], 0x80)
            for row, mask, converted, opacity in zip(raw['pixels'], raw['masks'], colored['pixels'], colored['masks']):
                for x in range(0, len(row), 2):
                    self.assertEqual(opacity[x:x + 2], [int(any(mask[x:x + 2]))] * 2)
                    expected = [1, 0] if sid == 46 else [0, 1]
                    self.assertEqual(converted[x:x + 2], expected if any(row[x:x + 2]) else [0, 0])

    def test_selected_build_profile_and_native_color_data(self):
        directory = build_dir()
        manifest = json.loads((directory / 'resources/manifest.json').read_text())
        self.assertEqual(manifest['video']['profile'], video_mode())
        page = (directory / 'resources/room12.hgr').read_bytes()
        if video_mode() == 'color':
            self.assertTrue(any(v & 128 for v in page))
            colors = {tuple(c) for y in range(160)
                      for c in zip(*[iter(scanline_rgb(page[row_offset(y):row_offset(y) + 40]))] * 3)}
            for color in [1, 2, 5, 6]:
                self.assertIn(RGB[color], colors)
        else:
            self.assertFalse(any(v & 128 for v in page))
        if video_mode() == 'dhgr':
            page = (page, (directory / 'resources/room12-aux.hgr').read_bytes())
        image = png(page)
        self.assertEqual(image[25], 2 if video_mode() != 'mono' else 0)


if __name__ == '__main__':
    unittest.main()
