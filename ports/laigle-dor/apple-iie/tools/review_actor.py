"""Execute all 16 linked actor frames; optional before/after art comparison.

Renderer fixtures explicitly select frame IDs at x19/y180, then execute the
native compositor and presentation. This is not a recorded gameplay sequence.
"""
import argparse
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.common import Source, build_dir, digest, write_json, labels
from tools.machine import Machine
from tools.preview import png
from tools.resources import sprite
from tools import dhgr


def capture(directory, output, name):
    machine = Machine(video='dhgr', directory=directory)
    machine.boot()
    results = []
    for frame in range(16):
        facing = frame % 4 if frame < 8 else (frame - 8) // 2
        state = {'actor_x': 19, 'actor_y': 180, 'frame_id': frame,
                 'facing': facing, 'pose': frame if frame < 8 else facing,
                 'walking': int(frame >= 8), 'walk_phase': (frame - 8) % 2 if frame >= 8 else 0}
        for label, value in state.items():
            machine.bus.ram[machine.symbols[label]] = value
        for routine in ('draw_scene', 'present_frame'):
            machine.cpu.sp = 255
            machine.cpu.stPushWord(0x01FF)
            machine.cpu.pc = machine.symbols[routine]
            machine.until(0x200, 2000000)
            assert machine.cpu.sp == 255
        file = '%s-%02d.png' % (name, frame)
        (output / file).write_bytes(png(machine.displayed_page(), machine.text_rows(), 'dhgr'))
        results.append({'frame': frame, 'file': file, 'page': machine.bus.switches['PAGE2']})
    assert not machine.bus.visible_write_violations
    assert not machine.bus.visible_text_write_violations
    return {'program_sha256': digest((directory / 'game.bin').read_bytes()),
            'frames': results, 'visible_write_violations': 0}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseline', type=Path)
    args = parser.parse_args()
    output = build_dir('dhgr') / 'actor-review'
    output.mkdir(exist_ok=True)
    variants = {}
    unchanged_fine_rows = 0
    if args.baseline:
        variants['before'] = capture(args.baseline.resolve(), output, 'before')
        before = (args.baseline / 'game.bin').read_bytes()
        after = (build_dir('dhgr') / 'game.bin').read_bytes()
        old_labels, new_labels = labels(args.baseline), labels(build_dir('dhgr'))
        for sid in [40, 41, 42, 43, 64, 65, 67]:
            target = dhgr.target_sprite(sprite(Source(), sid))
            a, b = old_labels['sprite_%d' % sid] - 0x6000, new_labels['sprite_%d' % sid] - 0x6000
            assert before[a:a + 16] == after[b:b + 16]
            stride = after[b + 2]
            for y, policy in enumerate(target['cell_policies']):
                if policy == 'fine':
                    start = 16 + y * stride
                    assert before[a + start:a + start + stride] == after[b + start:b + start + stride]
                    unchanged_fine_rows += 1
        for name in ['room12.hgr', 'room12-aux.hgr']:
            assert (args.baseline / name).read_bytes() == (build_dir('dhgr') / 'resources' / name).read_bytes()
    variants['current'] = capture(build_dir('dhgr'), output, 'current')
    html = '''<!doctype html><meta charset="utf-8"><title>DHGR actor review</title>
<style>body{background:#181818;color:white;font:16px system-ui}img{width:560px;image-rendering:pixelated}
figure{display:inline-block;margin:8px;vertical-align:top}h2{font-size:18px}</style>
<h1>Native renderer fixtures · all 16 actor frames · x19/y180</h1>
<p>Digital previews of actual main/aux bytes; not Virtual II or a calibrated CRT.</p>'''
    for frame in range(16):
        html += '<h2>Frame %d</h2>' % frame
        for name in variants:
            html += '<figure><figcaption>%s</figcaption><img src="%s-%02d.png"></figure>' % (name, name, frame)
    (output / 'index.html').write_text(html)
    write_json(output / 'verification.json', {
        'method': 'executed NMOS compositor/presentation with explicit frame-ID fixtures',
        'gameplay_sequence': False, 'display': 'sample-aware digital approximation',
        'variants': variants, 'unchanged_face_tunic_hand_resource_rows': unchanged_fine_rows,
        'terrain_banks_unchanged': True if args.baseline else 'not compared',
        'physical_hardware': 'not tested'})
    print('%d renderer fixtures captured: %s' % (16 * len(variants), output))


if __name__ == '__main__':
    main()
