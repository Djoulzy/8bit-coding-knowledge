"""Capture actual binaries at identical position/pose; review conversion loss."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.common import Source, build_dir, write_json, digest
from tools.machine import Machine
from tools.preview import png
from tools.resources import sprite, frames
from tools import dhgr


def main():
    output = build_dir('dhgr') / 'detail-review'
    output.mkdir(exist_ok=True)
    cases = [('hgr', Machine(video='mono')),
             ('dhgr-flat', Machine(video='dhgr', directory=build_dir('dhgr') / 'revisions/flat-v1')),
             ('dhgr-detail', Machine(video='dhgr', directory=build_dir('dhgr') / 'revisions/detail-v1')),
             ('dhgr-palette', Machine(video='dhgr', directory=build_dir('dhgr') / 'revisions/palette-v1')),
             ('dhgr-actor', Machine(video='dhgr'))]
    results = {}
    for name, machine in cases:
        machine.boot()
        for key in [10, None, None, None, 32]:
            machine.frame(key)
        state = machine.state()
        assert (state['actor_x'], state['actor_y'], state['frame_id']) == (19, 180, 0), state
        page, text = machine.displayed_page(), machine.text_rows()
        view = 'color' if name == 'hgr' else 'dhgr'
        (output / (name + '-color.png')).write_bytes(png(page, text, view))
        (output / (name + '-mono.png')).write_bytes(png(page, text, 'mono' if name == 'hgr' else 'dhgr', 'mono'))
        results[name] = {'state': state, 'program_sha256': digest((machine.directory / 'game.bin').read_bytes()),
                         'page': machine.bus.switches['PAGE2'],
                         'visible_write_violations': len(machine.bus.visible_write_violations)}
    assert all(r['state'] == results['hgr']['state'] for r in results.values())
    source = Source()
    ids = sorted({r[0] for f in frames(source) for r in f['layers']})
    mixed = tinted = preserved = adapted = 0
    for sid in ids:
        s = sprite(source, sid); target = dhgr.target_sprite(s)
        for row, codes, policy in zip(s['pixels'], target['statuses'], target['cell_policies']):
            for x, code in enumerate(codes):
                pair = row[x * 2:x * 2 + 2]
                if pair[0] != pair[1]:
                    mixed += 1
                    if policy == 'fine':
                        for color in set(target['colors']):
                            p = dhgr.status_pattern(code, dhgr.pattern(color))
                            assert bool(p & 3) == bool(pair[0])
                            assert bool(p & 12) == bool(pair[1])
                        preserved += 1
                    else:
                        assert code in (0, 5, 15)
                        adapted += 1
                tinted += code in (10, 15)
    write_json(output / 'verification.json', {
        'method': 'executed flat, detail, material-palette, actor-refinement and monochrome binaries; same input/pose',
        'results': results, 'source_sprite_ids': ids, 'mixed_pairs_flat_conversion_merged': mixed,
        'mixed_pairs_fine_conversion_preserved': preserved,
        'mixed_pairs_native_color_adapted': adapted, 'colored_full_foreground_pairs': tinted,
        'display': 'digital signal approximation; not Virtual II or a physical CRT capture'})
    html = '''<!doctype html><meta charset="utf-8"><title>DHGR detail review</title>
<style>body{background:#181818;color:white;font:16px system-ui}img{width:560px;image-rendering:pixelated}
section{display:inline-block;margin:10px;vertical-align:top}h2{font-size:18px}</style>
<h1>Executed binaries · x19 / y180 / frame 0</h1>
<p>Digital previews. Compare with Virtual II color captures; no CRT accuracy is claimed.</p>'''
    for name in results:
        html += '<section><h2>' + name + '</h2><img src="' + name + '-color.png"><p>Raw monochrome dots</p><img src="' + name + '-mono.png"></section>'
    (output / 'index.html').write_text(html)
    print('%d mixed pairs retained fine, %d adapted to material cells; report: %s' % (preserved, adapted, output))


if __name__ == '__main__':
    main()
