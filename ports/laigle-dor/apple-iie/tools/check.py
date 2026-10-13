"""Execute the project tests and write an aggregate result without hiding failures."""
from pathlib import Path
import argparse
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.common import ROOT, digest, write_json, build_dir, video_mode, select_video


def main():
    for name in ['test-results.json', 'cpu-verification.json']:
        (build_dir() / name).unlink(missing_ok=True)
    suite = unittest.defaultTestLoader.discover(str(ROOT / 'tests'))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    write_json(build_dir() / 'test-results.json', {
        'success': result.wasSuccessful(), 'tests_run': result.testsRun,
        'failures': [case.id() for case, _ in result.failures],
        'errors': [case.id() for case, _ in result.errors],
        'skipped': [case.id() for case, _ in result.skipped],
        'program_sha256': digest((build_dir() / 'game.bin').read_bytes()),
        'video_profile': video_mode(),
        'execution': 'py65 functional CPU plus independent resource/rule models',
        'original_oric_runtime': 'not tested', 'real_apple_hardware': 'not tested'})
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    select_video(argparse.ArgumentParser())
    sys.exit(main())
