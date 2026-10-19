"""Run with python3 -m unittest discover -s tools/apple-iie-editor/tests -v."""
import copy
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import subprocess
import shutil
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import server as standalone_server
try:
    server = standalone_server.load_adapter("laigle-dor")
except FileNotFoundError:
    server = None
if server is not None:
    from tools import artwork, resources, game_resources, title_resources, dhgr


@unittest.skipIf(server is None, "Optional game adapter unavailable in standalone copy")
class EditorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.env = patch.dict(os.environ, {'LAIGLE_ARTWORK': '', 'LAIGLE_VIDEO': 'dhgr'})
        self.env.start()
        self.addCleanup(self.env.stop)
        local = patch.object(server, 'PROJECT_FILE', self.root / 'saved-artwork.json')
        local.start()
        self.addCleanup(local.stop)

    def project(self, *assets):
        path = self.root / 'art.json'
        path.write_text(json.dumps({'schema': artwork.SCHEMA, 'assets': assets}))
        os.environ['LAIGLE_ARTWORK'] = str(path)
        return path

    def test_catalog_without_build_or_rom(self):
        items = list(server.assets().values())
        self.assertEqual(len(items), 301)
        self.assertIn('laigle/game/mono/atlas/48', server.assets())
        artwork.validate_project({'schema': artwork.SCHEMA, 'assets': items})
        self.assertTrue(any(a.get('encoding') == 'tile' for a in items))
        self.assertEqual({a['mode'] for a in items}, {'mono', 'color', 'dhgr'})

    def test_invalid_projects_fail_closed(self):
        a = copy.deepcopy(server.assets()['laigle/game/dhgr/title'])
        for edit in ({'main': [0]}, {'aux': [256]*8192}, {'mode': 'rgb'}, {'mixed': 1}):
            with self.subTest(edit=list(edit)):
                with self.assertRaises(ValueError):
                    artwork.validate_asset(dict(a, **edit))
        with self.assertRaises(ValueError):
            artwork.validate_project({'schema': artwork.SCHEMA, 'assets': [a, a]})

    def test_default_compiler_stays_byte_identical(self):
        rom = self.root / 'fixture.rom'
        rom.write_bytes(bytes(16384))
        with patch.object(game_resources, 'room_variation', return_value=(bytes(64), {'file': str(rom)})), patch.object(resources, 'build_dir', return_value=self.root):
            dest, _ = game_resources.export_game()
        # Optimized native-row fixture: zero room variation and no overrides.
        self.assertEqual(hashlib.sha256((dest/'generated.inc').read_bytes()).hexdigest(),
                         '06687e997443c6fa01fc5ee73242c1cb640a339ff1ab489f6c193cd139a70573')
        self.assertEqual((dest/'title.dhgr').read_bytes(), b''.join(title_resources.title_pages(False)))

    def test_sprite_edit_reaches_assembler(self):
        a = copy.deepcopy(server.assets()['laigle/game/dhgr/atlas/40'])
        a['colors'][0] = 1
        a['statuses'][0][0] = 15
        self.project(a)
        rom = self.root / 'fixture.rom'
        rom.write_bytes(bytes(16384))
        with patch.object(game_resources, 'room_variation', return_value=(bytes(64), {'file': str(rom)})), patch.object(resources, 'build_dir', return_value=self.root):
            dest, _ = game_resources.export_game()
        text = (dest/'generated.inc').read_text()
        lines = text.split('sprite_40:\n')[1].splitlines()
        # Native format 2 has shared mask/pixel rows, not the old cell decoder.
        row_name = lines[1].split()[-1]
        row = text.split(row_name + ':\n')[1].splitlines()[0].split('.byte ')[1]
        mask, pixels = [int(v.strip()[1:], 16) for v in row.split(',')[:2]]
        self.assertEqual(mask & 15, 15)
        self.assertEqual(pixels & 15, dhgr.pattern(1) & 15)
        self.assertEqual(json.loads((dest/'artwork-overrides.json').read_text())['applied'], [a['key']])

    def test_sprite_contract_rejects_size_change(self):
        native, _, _, _ = game_resources.native_artwork(server.Source())
        a = copy.deepcopy(server.assets()['laigle/game/dhgr/atlas/40'])
        a['width'] -= 1
        a['statuses'] = [r[:-1] for r in a['statuses']]
        self.project(a)
        with self.assertRaisesRegex(ValueError, 'dimensions'):
            artwork.override_sprites(native, 'laigle/game/dhgr/atlas/', 'dhgr')

    def test_title_edit_and_flash_round_trip(self):
        a = copy.deepcopy(server.assets()['laigle/game/dhgr/title'])
        # Visible pixel outside the lightning delta, and an unaddressed hole.
        a['main'][dhgr.row_offset(180)] ^= 63
        a['aux'][0x1fff] = 0xab
        self.project(a)
        title_resources.export_title(self.root)
        saved = (self.root/'title.dhgr').read_bytes()
        self.assertEqual(saved, bytes(a['main'] + a['aux']))
        patch_data = (self.root/'title-flash.bin').read_bytes()
        flashed = bytearray(saved)
        for i in range(0, len(patch_data)-2, 4):
            lo, hi, on, off = patch_data[i:i+4]
            index = (hi>>7)*8192 + ((hi&127)<<8) + lo
            self.assertEqual(saved[index], off)
            flashed[index] = on
        self.assertEqual(flashed[dhgr.row_offset(180)], a['main'][dhgr.row_offset(180)])
        self.assertEqual(flashed[-1], 0xab)

    def test_prototype_page_override_precedes_rle(self):
        for mode in ('mono', 'color', 'dhgr'):
            a = copy.deepcopy(server.assets()['laigle/prototype/'+mode+'/room12'])
            a['main'][0] ^= 63
            if mode == 'dhgr':
                a['aux'][0] ^= 17
            self.project(a)
            os.environ['LAIGLE_VIDEO'] = mode
            folder = self.root / mode
            with patch.object(resources, 'build_dir', return_value=folder):
                dest = resources.export()
            self.assertEqual((dest/'room12.hgr').read_bytes(), bytes(a['main']))
            self.assertEqual((dest/'room12.rle').read_bytes(), resources.rle(bytes(a['main'])))
            if mode == 'dhgr':
                self.assertEqual((dest/'room12-aux.rle').read_bytes(), resources.rle(bytes(a['aux'])))

    def test_hgr_mask_override_and_phase(self):
        a = copy.deepcopy(next(a for a in server.assets().values() if a['kind']=='sprite' and a['mode']=='color'))
        sid = a['source']['atlas_id']
        native = server.target_sprite(server.sprite(server.Source(), sid), 'color')
        a['pixels'][0][0], a['masks'][0][0], a['phase'] = 1, 1, 128
        self.project(a)
        edited = artwork.override_sprites([native], 'laigle/prototype/color/sprite/', 'color')[0]
        self.assertEqual((edited['pixels'][0][0], edited['masks'][0][0], edited['color_phase']), (1, 1, 128))
        a['masks'][0][0] = 0
        with self.assertRaisesRegex(ValueError, 'opaque'):
            artwork.validate_asset(a)



if __name__ == '__main__':
    unittest.main()
