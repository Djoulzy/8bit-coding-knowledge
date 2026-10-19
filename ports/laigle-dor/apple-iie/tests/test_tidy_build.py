"""Cleanup must preserve executable releases, evidence and unrelated files."""
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from tools.tidy_build import candidates, tidy


class TidyBuildTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.build = self.root / 'build'
        self.build.mkdir()

    def write(self, relative):
        path = self.build / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b'retain or remove deliberately')
        return path

    def test_preserves_full_games_test_assets_and_evidence(self):
        kept = [
            'game/laigle-dor-dhgr-color.do', 'game/laigle-dor.nib',
            'game/game.bin', 'game/game.lbl', 'game/game.map',
            'game/aux-assets.bin', 'game/resources/generated.inc',
            'game/resources/title.dhgr', 'game/game-test-results.json',
            'game-mono/laigle-dor-hgr-mono.do', 'game-mono/game.bin',
            'game-mono/resources/maps.bin', 'game-mono/input-profile.json',
            'latency-baseline/dhgr/game.bin', 'latency-baseline/dhgr/game.lbl',
            'latency-baseline/dhgr/laigle-dor.do', 'latency-baseline/mono/game.lst',
            'dhgr/virtualii-actor-left-y180.png', 'dhgr/test-results.json',
            'dhgr/revisions/palette-v1/verification-snapshot.json',
            'notes.txt', 'custom/experiment.do',
        ]
        snapshots = {self.write(name): b'retain or remove deliberately' for name in kept}
        removed = [
            'game.o', 'color/game.bin', 'color/resources/generated.inc',
            'dhgr/game.lbl', 'dhgr/revisions/palette-v1/laigle-dor.do',
            'dhgr/actor-review/index.html', 'dhgr/detail-review/index.html',
            'resources/world-initial.bin', 'game/game.o', 'game/game.lst',
            'game/virtualii-final.do', 'game/.DS_Store', 'game-mono/boot.o',
        ]
        obsolete = [self.write(name) for name in removed]
        with redirect_stdout(StringIO()):
            tidy(self.build)
        for path, content in snapshots.items():
            self.assertEqual(path.read_bytes(), content, path)
        self.assertFalse(any(path.exists() for path in obsolete))
        self.assertEqual(candidates(self.build), [])

    def test_dry_run_preserves_selected_files(self):
        artifact = self.write('dhgr/game.bin')
        with redirect_stdout(StringIO()):
            count, _ = tidy(self.build, dry_run=True)
        self.assertEqual(count, 1)
        self.assertTrue(artifact.is_file())

    def test_does_not_follow_symlinked_directories(self):
        outside = self.root / 'outside'
        outside.mkdir()
        resource = outside / 'resources'
        resource.mkdir()
        sentinel = resource / 'game.bin'
        sentinel.write_bytes(b'outside build')
        (self.build / 'color').symlink_to(outside, target_is_directory=True)
        (self.build / 'game').symlink_to(outside, target_is_directory=True)
        with redirect_stdout(StringIO()):
            tidy(self.build)
        self.assertEqual(sentinel.read_bytes(), b'outside build')
        self.assertTrue((self.build / 'color').is_symlink())
        self.assertTrue((self.build / 'game').is_symlink())

    def test_rejects_symlinked_build_root(self):
        alias = self.root / 'build-alias'
        alias.symlink_to(self.build, target_is_directory=True)
        with self.assertRaises(ValueError):
            candidates(alias)
