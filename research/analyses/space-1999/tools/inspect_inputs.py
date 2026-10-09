#!/usr/bin/env python3
"""Read-only Space 1999 evidence collector. Never runs historical code.

Optional --upstream names the text download directory described in overview.md.
The deliberately small data reader accepts decimal .byte/.byt values, names,
and bitwise OR only; it is not an assembler. No eval or build scripts are used.
"""
import argparse
import binascii
import hashlib
import json
import re
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'research/sources/Oric/Space 1999'
EXPECTED = '9d85e1d75d9f1e548f4d1e3bc3750085e7c8c125bb6cd110fb604ba86ba3e851'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def sectors(data):
    assert data[:8] == b'MFM_DISK'
    assert struct.unpack_from('<III', data, 8) == (1, 30, 1)
    assert len(data) == 256 + 30 * 6400
    result = []
    for track_id in range(30):
        offset = 256 + track_id * 6400
        track = data[offset:offset + 6400]
        pos, found = 0, []
        while True:
            ident = track.find(bytes.fromhex('a1a1a1fe'), pos)
            if ident < 0:
                break
            c, h, r, n = track[ident + 4:ident + 8]
            assert (c, h, n) == (track_id, 0, 1)
            mark = track.find(bytes.fromhex('a1a1a1fb'), ident + 10)
            assert mark >= 0 and mark + 262 <= len(track)
            payload = track[mark + 4:mark + 260]
            found.append(r)
            result.append(dict(side=h, track=c, sector=r,
                logical_sector=c * 17 + r - 1,
                dsk_offset=offset + mark + 4, data=payload,
                sha256=sha(payload),
                id_crc_ok=binascii.crc_hqx(track[ident:ident + 8], 0xffff)
                    == int.from_bytes(track[ident + 8:ident + 10], 'big'),
                data_crc_ok=binascii.crc_hqx(track[mark:mark + 260], 0xffff)
                    == int.from_bytes(track[mark + 260:mark + 262], 'big')))
            pos = mark + 262
        assert sorted(found) == list(range(1, 18))
    return sorted(result, key=lambda s: s['logical_sector'])


def byte_data(text, names):
    result = bytearray()
    for line in text.splitlines():
        line = line.split(';')[0].strip()
        if not line.startswith(('.byte ', '.byt ')):
            continue
        for expr in line.split(None, 1)[1].split(','):
            value = 0
            for term in expr.split('|'):
                term = term.strip()
                value |= int(term) if term.isdecimal() else names[term]
            assert 0 <= value <= 255
            result.append(value)
    return bytes(result)


def upstream_checks(base, logical):
    game = base / 'game source'
    manifest = json.loads((HERE / 'upstream-manifest.json').read_text())
    used = {'world/picdef.h', 'world/world.s', 'stringsc.s', 'NOISE/noise-tail.s'}
    for record in manifest['files']:
        relative = record['path'].split('/Sources/', 1)[1]
        if relative.startswith('game source/') and relative[len('game source/'):] in used:
            assert sha((base / relative).read_bytes()) == record['sha256'], 'Reference revision changed'
    names = {'INVERT': 64, 'SPECIAL': 128}
    for line in (game / 'world/picdef.h').read_text(encoding='latin1').splitlines():
        match = re.match(r'#define\s+(\w+)\s+(\d+)', line)
        if match:
            names[match[1]] = int(match[2])
    world = byte_data((game / 'world/world.s').read_text(encoding='latin1'), names)
    grammar_text = (game / 'stringsc.s').read_text(encoding='latin1')
    grammar = byte_data(grammar_text.split('\nGrammar\n')[-1], {})
    # read_text normalizes CRLF, while hashes in the manifest use original bytes.
    grammar_positions = [m.start() for m in re.finditer(re.escape(grammar), logical)]
    assert len(grammar) == 256
    expansions, peak_pending = [], 0
    for code in range(128, 256):
        pending, output = [code], []
        while pending:
            peak_pending = max(peak_pending, len(pending))
            token = pending.pop()
            if token < 128:
                assert token != 0
                output.append(token)
            else:
                first, second = grammar[2 * (token - 128):2 * (token - 128) + 2]
                assert first < token and second < token, 'Grammar must be acyclic'
                pending.extend([second, first])
        expansions.append(len(output))
    # Source table structure: even-row words; even-x quotient/mask pairs.
    tables = (game / 'NOISE/noise-tail.s').read_text(encoding='latin1')
    row_text = tables.split('\ntab_scan\n')[1].split('\ntab_mod06\n')[0]
    rows = [int(v.strip()) for line in row_text.splitlines()
            if line.strip().startswith('.word')
            for v in line.strip().split(None, 1)[1].split(',')]
    pair_text = tables.split('\ntab_mod06\n')[1].split('#ifndef')[0]
    pair_bytes = byte_data(pair_text, {})
    pairs = list(zip(pair_bytes[::2], pair_bytes[1::2]))
    assert len(rows) == 100 and len(pairs) == 120
    for y in range(200):
        row = rows[y // 2] + (40 if y & 1 else 0)
        for x in range(240):
            quotient, mask = pairs[x // 2]
            if x & 1:
                mask >>= 1
            assert 0xa000 + row + quotient == 0xa000 + y * 40 + x // 6
            assert mask == 0x20 >> (x % 6)
    world_pos = 104 * 256
    rooms, cursor = [], 0
    while cursor < len(world):
        rooms.append(world[cursor])
        length = world[cursor + 1]
        assert length > 0
        cursor += length
    assert cursor == len(world)
    # Binary pattern for disk.s fdc_irq; relocation-dependent operands masked.
    irq = re.escape(bytes.fromhex('68 68 68 ad')) + b'..' + re.escape(bytes.fromhex('8d 14 03 ad 10 03 29 7c 8d')) + b'..' + re.escape(bytes.fromhex('60'))
    irq_positions = [m.start() for m in re.finditer(irq, logical, re.DOTALL)]
    return dict(world=dict(bytes=len(world), sha256=sha(world), room_count=len(rooms),
        unique_room_ids=len(set(rooms)), logical_offset=world_pos,
        matches_disk=logical[world_pos:world_pos + len(world)] == world),
        grammar=dict(bytes=len(grammar), sha256=sha(grammar), logical_offsets=grammar_positions,
            all_tokens_acyclic=True, longest_expansion=max(expansions),
            max_pending_tokens=peak_pending, stack_sentinel_bytes=1),
        parity_table_model=dict(coordinates_checked=240 * 200, table_bytes=200 + 240,
            note='Arithmetic model, not CPU execution or performance measurement'),
        reference_files_hash_checked=len(used),
        fdc_irq_signature_logical_offsets=irq_positions)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--upstream', type=Path)
    parser.add_argument('--output', type=Path, default=HERE / 'verification.json')
    args = parser.parse_args()
    disk = (SOURCE / 'space1999-fr.dsk').read_bytes()
    assert sha(disk) == EXPECTED, 'Input revision changed'
    records = sectors(disk)
    logical = b''.join(s['data'] for s in records)
    report = dict(inputs=[dict(path=str(p.relative_to(ROOT)), bytes=p.stat().st_size,
        sha256=sha(p.read_bytes())) for p in sorted(SOURCE.iterdir()) if p.is_file()],
        header=dict(sides=1, tracks=30, geometry=1, track_bytes=6400),
        sector_count=len(records), logical_bytes=len(logical),
        id_crc_mismatches=sum(not s['id_crc_ok'] for s in records),
        data_crc_mismatches=sum(not s['data_crc_ok'] for s in records),
        logical_sha256=sha(logical),
        sectors=[{k: v for k, v in s.items() if k != 'data'} for s in records])
    if args.upstream:
        report['upstream_comparison'] = upstream_checks(args.upstream, logical)
        def raw_spans(start, length):
            spans = []
            while length:
                index, within = divmod(start, 256)
                amount = min(length, 256 - within)
                spans.append(dict(logical_offset=start,
                    dsk_offset=records[index]['dsk_offset'] + within, bytes=amount))
                start += amount
                length -= amount
            return spans
        comparison = report['upstream_comparison']
        world = comparison['world']
        world['dsk_spans'] = raw_spans(world['logical_offset'], world['bytes'])
        grammar = comparison['grammar']
        grammar['dsk_spans'] = [raw_spans(start, grammar['bytes']) for start in grammar['logical_offsets']]
        comparison['fdc_irq_signature_dsk_spans'] = [raw_spans(start, 18)
            for start in comparison['fdc_irq_signature_logical_offsets']]
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    summary = {k: v for k, v in report.items() if k not in ('sectors', 'inputs', 'upstream_comparison')}
    if args.upstream:
        summary['upstream_comparison'] = dict(world_bytes=world['bytes'],
            room_count=world['room_count'], world_matches_disk=world['matches_disk'],
            grammar_offsets=grammar['logical_offsets'],
            all_tokens_acyclic=grammar['all_tokens_acyclic'],
            coordinates_checked=comparison['parity_table_model']['coordinates_checked'])
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
