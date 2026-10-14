"""Standalone project/service tests: no optional adapter imports."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from project_format import validate_project as validate_workspace


class StandaloneTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_portable_server_without_repository(self):
        editor = Path(__file__).resolve().parents[1]
        for name in ('server.py', 'project_format.py'):
            shutil.copy(editor/name, self.root/name)
        a = dict(key='custom/test', kind='screen', mode='mono', main=[0]*8192)
        project = self.root/'generic.json'
        project.write_text(json.dumps({'schema': 'a2-artwork-v1', 'assets': [a]}))
        result = subprocess.run([sys.executable, str(self.root/'server.py'), '--check', str(project)],
                                cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Valid project', result.stdout)
        result = subprocess.run([sys.executable, '-c', "import server,sys; assert 'tools.common' not in sys.modules"],
                                cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_workspace_reference_validation(self):
        a = dict(key='custom/test', kind='screen', mode='mono', main=[0]*8192)
        d = dict(id='doc1', name='Generic', asset=a, sources=[dict(type='native', asset=a)],
                 reference=0, frozen=False, variants={}, archives=[])
        p = dict(schema='a2-workspace-v2', documents=[d])
        validate_workspace(p)
        d['reference']=1
        with self.assertRaises(ValueError):
            validate_workspace(p)
        d['reference'] = 0
        d['linkedModes'] = True
        validate_workspace(p)
        d['linkedModes'] = 'yes'
        with self.assertRaises(ValueError):
            validate_workspace(p)

    def test_dhgr_mono_requires_both_banks(self):
        a = dict(key='custom/dhgr-mono', kind='screen', mode='dhgr-mono',
                 main=[0]*8192, aux=[0]*8192)
        p = dict(schema='a2-artwork-v1', assets=[a])
        validate_workspace(p)
        a['aux'] = [0]*8191
        with self.assertRaises(ValueError):
            validate_workspace(p)

    def test_local_edit_references(self):
        before = dict(key='custom/local', kind='screen', mode='color', main=[0]*8192)
        after = dict(before, main=[1]+[0]*8191)
        edit = dict(type='edit', base=0, before=before, after=after)
        d = dict(id='local', name='Local edits', asset=after,
                 sources=[dict(type='native', asset=before), edit], reference=1,
                 frozen=True, linkedModes=True, variants={'color': after}, archives=[])
        p = dict(schema='a2-workspace-v2', documents=[d])
        validate_workspace(p)
        for base in (-1, 1, 2, True):
            edit['base'] = base
            with self.assertRaises(ValueError):
                validate_workspace(p)
        edit['base'] = 0
        edit['after'] = dict(after, mode='mono')
        with self.assertRaises(ValueError):
            validate_workspace(p)
