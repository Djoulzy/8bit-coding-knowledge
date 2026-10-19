"""Profile native input-to-flip latency without changing the game binaries.

CPU counts come from py65. Device/video timing is the functional bus model;
conversion at exactly 1 MHz is an estimate, not a Virtual II measurement.
"""
import argparse
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.common import ROOT, digest, write_json
from tools.machine import Machine


ROUTINES = (
    'keyboard_poll', 'game_tick', 'full_clock', 'world_load_scene',
    'draw_scene', 'full_prepare_page', 'repair_rectangle', 'full_draw_torches',
    'draw_sprite', 'full_draw_equipment', 'full_draw_entities',
    'full_hud_draw', 'full_text_draw', 'present_frame',
    'draw_native_sprite', 'actor_cache', 'clock_sample',
)


def trace(m, label, key=None, after_poll=False):
    """Run one loop, or two when injecting a key just after the first poll.

    Routine counts are inclusive: nested routines must not be added together.
    Track return PC AND stack depth to handle tail calls/shared return sites.
    """
    assert m.cpu.pc == m.symbols['main_loop']
    start = m.cpu.processorCycles
    initial = m.state()
    entries = {m.symbols[name]: name for name in ROUTINES if name in m.symbols}
    scopes = []
    totals = defaultdict(int)
    calls = defaultdict(int)
    loops, consumed, injected, visible = 0, None, None, None
    polls, flips = [], []
    if key is not None and not after_poll:
        m.bus.press(key)
        injected = 0
    for _ in range(6000000):
        now = m.cpu.processorCycles - start
        pc, sp = m.cpu.pc, m.cpu.sp
        remaining = []
        for name, returned, depth, began in scopes:
            if pc == returned and sp == depth:
                totals[name] += now - began
            else:
                remaining.append((name, returned, depth, began))
        scopes = remaining
        if pc == m.symbols['main_loop'] and now:
            loops += 1
            if loops == (2 if after_poll else 1):
                break
        if after_poll and injected is None and pc == m.symbols['game_tick']:
            m.bus.press(key)
            injected = now
        if pc == m.symbols['keyboard_poll']:
            polls.append(now)
        if pc in entries:
            name = entries[pc]
            lo = m.bus.ram[0x100 + ((sp + 1) & 255)]
            hi = m.bus.ram[0x100 + ((sp + 2) & 255)]
            invocation = (name, ((hi << 8) + lo + 1) & 65535, (sp + 2) & 255)
            # Some public entry labels are also loop headers (repair scanlines,
            # VBL polling). A branch back to that PC is not a new invocation.
            if not any(scope[:3] == invocation for scope in scopes):
                scopes.append((*invocation, now))
                calls[name] += 1
        strobe, flip_count = m.bus.strobe, len(m.bus.page_flips)
        m.step()
        if strobe and not m.bus.strobe:
            consumed = m.cpu.processorCycles - start
        if len(m.bus.page_flips) != flip_count:
            when = m.cpu.processorCycles - start
            flips.append(when)
            if consumed is not None and visible is None:
                visible = when
    else:
        raise TimeoutError('Profiling did not return to main_loop')
    assert not scopes, scopes
    assert all(value <= m.cpu.processorCycles - start for value in totals.values())
    if key is not None:
        assert injected is not None and consumed is not None and visible is not None
    return {
        'scenario': label, 'key': key, 'loops': loops,
        'total_cycles': m.cpu.processorCycles - start,
        'keyboard_poll_offsets': polls, 'page_flip_offsets': flips,
        'key_injected_offset': injected, 'key_consumed_offset': consumed,
        'input_to_consume_cycles': None if consumed is None else consumed - injected,
        'input_to_next_flip_cycles': None if visible is None else visible - injected,
        'inclusive_routine_cycles': dict(sorted(totals.items())),
        'routine_calls': dict(sorted(calls.items())),
        'before': initial, 'after': m.state(),
    }


def profile(video, directory=None):
    directory = directory or ROOT / ('build/game-mono' if video == 'mono' else 'build/game')
    m = Machine(directory=directory, video=video)
    m.boot()
    for key in [13, 13, 13, ord('1')]:
        m.frame(key)  # title, intro, name, exterior -> room 12
    m.frame()
    m.frame()  # both hidden pages have their terrain; exclude initial construction
    assert m.state()['current_room'] == 12 and m.state()['game_mode'] == 0
    assert m.bus.ram[m.symbols['terrain_pending']] == 0
    m.bus.visible_write_violations.clear()
    m.bus.visible_text_write_violations.clear()
    results = [trace(m, 'room12_idle_%d' % n) for n in range(4)]
    results += [
        trace(m, 'turn_left_arriving_just_after_idle_poll', 0x08, after_poll=True),
        trace(m, 'turn_right', 0x15),
        trace(m, 'start_walking_right', 0x15),
        trace(m, 'stop_arriving_just_after_poll', 32, after_poll=True),
        trace(m, 'crouch', ord('A')),
        trace(m, 'stand', 32),
        trace(m, 'open_inventory', ord('I')),
        trace(m, 'inventory_idle'),
        trace(m, 'close_inventory', 32),
    ]
    # Ensure the timing trace actually exercised the intended controls.
    by_name = {row['scenario']: row for row in results}
    assert by_name['turn_right']['after']['facing'] == 1
    assert by_name['start_walking_right']['after']['walking'] == 1
    assert by_name['stop_arriving_just_after_poll']['after']['walking'] == 0
    assert by_name['crouch']['after']['pose'] == 5
    assert by_name['open_inventory']['after']['game_mode'] == 3
    assert by_name['close_inventory']['after']['game_mode'] == 0
    assert not m.bus.visible_write_violations
    assert not m.bus.visible_text_write_violations
    report = {
        'video': video, 'program_sha256': digest((directory / 'game.bin').read_bytes()),
        'disk_sha256': digest((directory / 'laigle-dor.do').read_bytes()),
        'execution': 'py65 NMOS 6502; functional bus; simplified NTSC VBL model',
        'time_conversion': 'cycles / 1000 = estimated milliseconds at exactly 1 MHz',
        'limits': ['Not measured in Virtual II or on hardware',
                   'No host keyboard, keyboard-repeat or monitor latency modeled',
                   'Steady room 12 only; no disk or room-construction timing',
                   'Routine cycles include nested calls; do not sum overlapping scopes',
                   'Next flip marks submission, not physical display scanout'],
        'scenarios': results,
    }
    output = directory / 'input-profile.json'
    write_json(output, report)
    print(output.relative_to(ROOT), flush=True)
    for row in results:
        print('%-35s %7d cycles  input->flip: %s' %
              (row['scenario'], row['total_cycles'], row['input_to_next_flip_cycles']), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--video', choices=['dhgr', 'mono'], required=True)
    parser.add_argument('--directory', type=Path, help='Optional archived build with disk and labels')
    args=parser.parse_args()
    profile(args.video, args.directory.resolve() if args.directory else None)
