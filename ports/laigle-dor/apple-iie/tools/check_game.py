"""Separate native-world checks; do not mix their evidence with W06 graphics."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from tools.common import ROOT,write_json,digest


def main():
    for name in ['game-test-results.json','room-verification.json']:
        (ROOT/'build/game'/name).unlink(missing_ok=True)
    suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'),pattern='world_port.py')
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    write_json(ROOT/'build/game/game-test-results.json',{'success':result.wasSuccessful(),
        'tests_run':result.testsRun,'failures':[c.id() for c,_ in result.failures],
        'errors':[c.id() for c,_ in result.errors],
        'program_sha256':digest((ROOT/'build/game/game.bin').read_bytes()),
        'execution':'py65 functional 6502 / real Disk II BOOT0; no ROM cold-start',
        'original_oric_runtime':'not tested','real_hardware':'not tested'})
    return 0 if result.wasSuccessful() else 1


if __name__=='__main__':sys.exit(main())
