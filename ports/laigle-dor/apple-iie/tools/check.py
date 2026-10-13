"""Execute the project tests and write an aggregate result without hiding failures."""
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.common import ROOT, digest, write_json


def main():
    for name in ['test-results.json', 'cpu-verification.json']:
        (ROOT / 'build' / name).unlink(missing_ok=True)
    suite = unittest.defaultTestLoader.discover(str(ROOT / 'tests'))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    write_json(ROOT / 'build/test-results.json', {
        'success': result.wasSuccessful(), 'tests_run': result.testsRun,
        'failures': [case.id() for case, _ in result.failures],
        'errors': [case.id() for case, _ in result.errors],
        'skipped': [case.id() for case, _ in result.skipped],
        'program_sha256': digest((ROOT / 'build/game.bin').read_bytes()),
        'execution': 'py65 functional CPU plus independent resource/rule models',
        'original_oric_runtime': 'not tested', 'real_apple_hardware': 'not tested'})
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(main())
