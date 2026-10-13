"""Execute both built video variants with identical input; compare game state."""
from pathlib import Path
import argparse
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.common import build_dir, digest, write_json
from tools.machine import Machine


def main(video='color'):
    machines = [Machine(video=mode) for mode in ('mono', video)]
    for machine in machines:
        machine.boot()
    keys = [10, None, None, None, None, 32, 21, 21, None, None, None, None,
            None, None, 65, 32, 8, 8, None, None, 32, 11, 11, None, 32, 82]
    trace = []
    for key in keys:
        states = [machine.frame(key) for machine in machines]
        if states[0] != states[1] or machines[0].events() != machines[1].events():
            raise AssertionError('Video variants changed game behavior at frame %d' % (len(trace) + 1))
        trace.append({'key': key, 'state': states[0]})
    variants = {}
    for machine in machines:
        if machine.bus.visible_write_violations or machine.bus.visible_text_write_violations:
            raise AssertionError('Visible page modified during construction: ' + machine.video)
        variants[machine.video] = {
            'program_sha256': digest((machine.directory / 'game.bin').read_bytes()),
            'speaker_accesses': machine.bus.speaker_accesses,
            'visible_graphics_writes': len(machine.bus.visible_write_violations),
            'visible_text_writes': len(machine.bus.visible_text_write_violations),
        }
    report = build_dir(video) / 'comparison.json'
    write_json(report, {'success': True, 'frames_compared': len(keys), 'trace': trace,
                        'variants': variants, 'method': 'two executed NMOS binaries; functional bus',
                        'color_quality': 'not compared with a physical monitor'})
    print('%d frames: identical game states/events in mono and %s; %s' % (len(keys), video, report))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--video', choices=['color', 'dhgr'], default='color')
    main(parser.parse_args().video)
