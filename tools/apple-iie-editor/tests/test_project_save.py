"""Persist edits into compiler inputs through the same-origin local API."""
import copy
import http.client
import json
import os
from pathlib import Path
import sys
import tempfile
from threading import Thread
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import server as service


class ProjectSaveTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.adapter = service.load_adapter('laigle-dor')
        from tools import artwork
        self.artwork = artwork
        self.file = self.root / 'resources/artwork.json'
        for target in (self.adapter, artwork):
            context = patch.object(target, 'PROJECT_FILE', self.file)
            context.start()
            self.addCleanup(context.stop)
        context = patch.dict(os.environ, {'LAIGLE_ARTWORK': ''})
        context.start()
        self.addCleanup(context.stop)

    def asset(self, key='laigle/game/dhgr/atlas/40'):
        return copy.deepcopy(self.adapter.base_assets()[key])

    def workspace(self, *assets):
        return {'schema': 'a2-workspace-v2', 'documents': [dict(
            id=a['key'], name=a['name'], asset=a,
            sources=[{'type': 'native', 'asset': self.asset(a['key'])}],
            reference=0, frozen=False, linkedModes=True,
            variants={a['mode']: copy.deepcopy(a)}, archives=[]) for a in assets]}

    def start_server(self, adapter=True):
        httpd = service.ThreadingHTTPServer(('127.0.0.1', 0), service.Handler)
        httpd.adapter = self.adapter if adapter else None
        thread = Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        def stop():
            httpd.shutdown()
            httpd.server_close()
            thread.join()
        self.addCleanup(stop)
        return httpd.server_port

    def request(self, port, method, data=None, origin=True, content_type='application/json'):
        connection = http.client.HTTPConnection('127.0.0.1', port, timeout=5)
        headers = {'Content-Type': content_type}
        if origin:
            headers['Origin'] = 'http://127.0.0.1:%d' % port
        connection.request(method, '/api/project', json.dumps(data) if data is not None else None, headers)
        response = connection.getresponse()
        result = response.status, json.loads(response.read())
        connection.close()
        return result

    def test_http_save_reload_and_default_compiler_input(self):
        a = self.asset()
        a['colors'][0], a['statuses'][0][0] = 1, 15
        workspace = self.workspace(a)
        port = self.start_server()
        status, result = self.request(port, 'POST', workspace)
        self.assertEqual(status, 200, result)
        self.assertEqual(result['saved'], 1)
        self.assertEqual(self.adapter.assets()[a['key']], a)
        self.assertEqual(self.request(port, 'GET')[1], workspace)
        # No environment override is needed for the normal compilation path.
        del os.environ['LAIGLE_ARTWORK']
        data, report = self.artwork.configured()
        self.assertEqual(data['assets'], [a])
        self.assertEqual(report['file'], str(self.file.resolve()))
        from tools.game_resources import native_artwork
        native = self.artwork.override_sprites(native_artwork(self.adapter.Source())[0],
                                               'laigle/game/dhgr/atlas/', 'dhgr')
        first = next(s for s in native if s['id'] == 40)
        self.assertEqual((first['colors'][0], first['statuses'][0][0]), (1, 15))
        os.environ['LAIGLE_ARTWORK'] = ''
        self.assertIsNone(self.artwork.configured())

    def test_partial_save_keeps_closed_resources_and_source_history(self):
        a = self.asset()
        a['colors'][0] = 1
        self.adapter.save_project(self.workspace(a))
        b = self.asset('laigle/game/dhgr/title')
        b['main'][0] ^= 1
        self.adapter.save_project(self.workspace(b))
        saved = json.loads(self.file.read_text())
        self.assertEqual({x['key'] for x in saved['assets']}, {a['key'], b['key']})
        self.assertEqual(len(saved['workspace']['documents']), 2)
        self.assertEqual(saved['workspace']['documents'][0]['sources'][0]['asset'], self.asset())

    def test_old_mono_prototype_edits_reach_full_game(self):
        a = self.asset('laigle/prototype/mono/sprite/48')
        a['pixels'][0][0], a['masks'][0][0] = 1, 1
        result = self.adapter.save_project(self.workspace(a))
        target = 'laigle/game/mono/atlas/48'
        self.assertEqual(result['mirrored'], [target])
        self.assertEqual(self.adapter.assets()[target]['pixels'], a['pixels'])
        del os.environ['LAIGLE_ARTWORK']
        from tools.game_resources import native_artwork
        native = self.artwork.override_sprites(native_artwork(self.adapter.Source(), 'mono')[0],
                                               'laigle/game/mono/atlas/', 'mono')
        sprite = next(s for s in native if s['id'] == 48)
        self.assertEqual(sprite['statuses'][0][0], 10)
        self.assertEqual(sprite['pixels'][0][0], 1)

    def test_native_mono_tiles_and_title_are_compiler_inputs(self):
        a = self.asset('laigle/game/mono/atlas/161')
        a['pixels'][0][0], a['masks'][0][0] = 1, 1
        title = self.asset('laigle/game/mono/title')
        title['main'][8191] = 65
        self.adapter.save_project(self.workspace(a, title))
        del os.environ['LAIGLE_ARTWORK']
        from tools.game_resources import native_artwork
        native = self.artwork.override_sprites(native_artwork(self.adapter.Source(), 'mono')[0],
                                               'laigle/game/mono/atlas/', 'mono')
        self.assertEqual(next(s for s in native if s['id'] == 161)['tile_rows'][0][0], 2)
        from tools.title_resources import export_title
        export_title(self.root, 'mono')
        self.assertEqual((self.root/'title.hgr').read_bytes(), bytes(title['main']))

    def test_invalid_or_failed_write_keeps_previous_project(self):
        self.adapter.save_project(self.workspace(self.asset()))
        before = self.file.read_bytes()
        bad = self.asset()
        bad['height'] -= 1
        bad['statuses'].pop()
        bad['colors'].pop()
        with self.assertRaises(ValueError):
            self.adapter.save_project(self.workspace(bad))
        with patch.object(self.adapter.os, 'replace', side_effect=OSError('disk full')):
            with self.assertRaises(OSError):
                self.adapter.save_project(self.workspace(self.asset()))
        self.assertEqual(self.file.read_bytes(), before)
        self.assertFalse(list(self.file.parent.glob('.artwork-*.tmp')))

    def test_conflicting_native_documents_do_not_overwrite(self):
        a = self.asset()
        b = self.asset()
        b['colors'][0] ^= 1
        workspace = self.workspace(a, b)
        workspace['documents'][1]['id'] += '-copy'
        with self.assertRaisesRegex(ValueError, 'même ressource'):
            self.adapter.save_project(workspace)
        self.assertFalse(self.file.exists())

    def test_conflicting_mono_aliases_are_explicit(self):
        a = self.asset('laigle/prototype/mono/sprite/48')
        b = self.asset('laigle/game/mono/atlas/48')
        a['pixels'][0][0], a['masks'][0][0] = 1, 1
        b['pixels'][0][0], b['masks'][0][0] = 0, 0
        with self.assertRaisesRegex(ValueError, 'copies prototype et jeu mono'):
            self.adapter.save_project(self.workspace(a, b))
        self.assertFalse(self.file.exists())

    def test_write_endpoint_requires_adapter_origin_and_json(self):
        port = self.start_server()
        workspace = self.workspace(self.asset())
        self.assertEqual(self.request(port, 'POST', workspace, origin=False)[0], 403)
        self.assertEqual(self.request(port, 'POST', workspace, content_type='text/plain')[0], 415)
        self.assertEqual(self.request(port, 'POST', {'schema': 'invalid'})[0], 400)
        generic = self.start_server(adapter=False)
        self.assertEqual(self.request(generic, 'POST', workspace)[0], 405)
        self.assertFalse(self.file.exists())


if __name__ == '__main__':
    unittest.main()
