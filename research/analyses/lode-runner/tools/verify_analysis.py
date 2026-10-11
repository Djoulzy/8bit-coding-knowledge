#!/usr/bin/env python3
"""Verify extraction and analytical models; no historical code is executed.

These are byte/properties checks, not emulation, performance benchmarks or a
proof that the cracked disk boots. Run from any directory with Python 3.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
import inspect_disk as disk

BASE = Path(__file__).resolve().parents[1]

def main():
    data, model = disk.snapshot()
    try:
        disk.parse(data, tuple(range(16)))
    except ValueError:
        pass
    else:
        raise AssertionError('Identity/DOS image order unexpectedly parsed')
    game = next(f for f in model['files'] if f['name'] == 'LODE RUNNER')
    assert (game['load_address'],game['length']) == (0x7fd,0x8f03)
    assert game['data'][:3] == bytes.fromhex('4c005a')
    manifest=json.loads((BASE/'extracted/manifest.json').read_text())
    for record,saved in zip(model['files'],manifest['files']):
        assert (BASE/'extracted'/saved['payload_file']).read_bytes() == record['data']
        assert saved['sector_map'] == record['sector_map']
    # Independent reconstruction by explicit manifest sector offsets.
    for saved in manifest['files']:
        allocated=b''.join(data[p['dsk_offset']:p['dsk_offset']+256] for p in saved['sector_map'])
        payload=allocated[saved['header_bytes']:saved['header_bytes']+saved['length']]
        assert hashlib.sha256(payload).hexdigest() == saved['sha256']
    memory,origins=disk.runtime_model(game)
    assert origins[0x800] is None and origins[0x801] is None
    assert memory[0x600:0x609] == bytes.fromhex('4c09064c5d064cd606')
    assert memory[0x8e50:0x8e53] == bytes.fromhex('4cb5b7')
    assert memory[0xb7b5:0xb7b8] == bytes.fromhex('087820')
    assert memory[0x23:0x26] == bytes.fromhex('4c0017')
    # Every known runtime byte still maps to its original disk byte.
    for address,offset in enumerate(origins):
        if offset is not None:
            assert memory[address] == data[offset]
    # Split scanline and coordinate tables versus independent arithmetic.
    for y in range(192):
        actual=memory[0x1a85+y]+256*memory[0x1b45+y]
        expected=(y&7)*1024+((y>>3)&7)*128+(y>>6)*40
        assert actual == expected
        page1=actual|0x2000
        assert (page1^0x6000) == actual|0x4000
    for row in range(16):
        low=memory[0x1c05+row]
        assert low+256*memory[0x1c15+row] == 0x800+28*row
        assert low+256*memory[0x1c25+row] == 0xa00+28*row
        assert memory[0x1c51+row] == 11*row
    for col in range(28):
        assert memory[0x1c35+col] == 5*col
        assert memory[0x1c62+col] == (10*col)//7
        assert memory[0x1c7e+col] == (10*col)%7
    for x in range(140):
        assert memory[0x1c9a+x] == (2*x)//7
        assert memory[0x1d26+x] == (2*x)%7
    # 7 phases x 128 row patterns. Low-byte +1 cannot carry for these pairs.
    pointers=set()
    for phase in range(7):
        for token in range(128):
            ptr=memory[0xa200+phase*256+token]+256*memory[0xa280+phase*256+token]
            assert 0xa900 <= ptr <= 0xacfe and ptr%256 != 255
            pointers.add(ptr)
            assert memory[ptr] == 0x80 | ((token<<phase)&127)
            assert memory[ptr+1] == 0x80 | ((token<<phase)>>7)
    # A rectangular 22 x 104 token interpretation has two anomalous entries.
    # Their use as live sprite IDs is not established by this static census.
    token_anomalies=[]
    for slice_index in range(22):
        for sprite_id in range(104):
            address=0xad00+slice_index*104+sprite_id
            if memory[address] > 127:
                token_anomalies.append(dict(slice=slice_index, sprite_id=sprite_id,
                    address=f'${address:04X}', value=f'${memory[address]:02X}',
                    dsk_offset=origins[address]))
    assert [(a['slice'],a['sprite_id'],a['value']) for a in token_anomalies] == [
        (21,102,'$81'),(21,103,'$A8')]
    # Nibble decoder and its inverse, independently of CPU execution.
    for value in range(256):
        low,high=value&15,value>>4
        assert low|(high<<4) == value
    # Scheduler model: leading-one quotas update consecutive actors, wrapping.
    quotas=memory[0x6ca7:0x6cc2]
    assert set(quotas) == {0,1,3,7}
    for count in range(1,6):
        for previous in range(count+1):
            for mask in quotas:
                cursor,events,remaining=previous,[],mask
                while remaining:
                    carry=remaining&1
                    remaining >>= 1
                    if carry:
                        cursor=cursor+1 if cursor<count else 1
                        events.append(cursor)
                assert len(events)==mask.bit_count()
                assert all(1<=event<=count for event in events)
    audit=json.loads((BASE/'extracted/level-audit.json').read_text())
    anomalies=[a['level'] for a in audit if a['values_above_9'] or a['player_markers']!=1]
    assert anomalies == [136]
    # Decoded listing starts: check bytes through the provenance map, including
    # instructions which straddle nonconsecutive sectors. Loader uses load map.
    checked=0
    for path in (BASE/'extracted').glob('*.asm.txt'):
        for line in path.read_text().splitlines():
            match=re.match(r'^([0-9A-F]{4})  DSK=\$([0-9A-F]{6})  ((?:[0-9a-f]{2} ?){1,3})\s+\S',line)
            assert match, (path,line)
            address,offset=int(match[1],16),int(match[2],16)
            raw=bytes.fromhex(match[3])
            if path.name=='loader.asm.txt':
                pos=address-game['load_address']
                assert disk.payload_offset(game,pos)==offset
                assert game['data'][pos:pos+len(raw)]==raw
            else:
                assert origins[address]==offset
                assert memory[address:address+len(raw)]==raw
            checked+=1
    result=dict(source_sha256=disk.EXPECTED_SHA256,
        checks='static byte reconstruction and analytical properties; no imported code execution',
        live_files=len(model['files']), game_bytes=game['length'],
        game_data_sectors=len(game['sector_map']), game_ts_lists=len(game['ts_lists']),
        listing_instructions_checked=checked,hgr_rows_checked=192,
        phase_pattern_pairs_checked=7*128,unique_expansion_pairs=len(pointers),
        token_slice_entries_checked=22*104,token_anomalies=token_anomalies,
        level_records_audited=150,level_anomalies=anomalies,
        unknown_loader_source_bytes=['$9700','$9701'],
        unresolved_level_disk_entry='$0023 -> $1700',
        emulator_used=False,hardware_used=False,benchmarked=False)
    (BASE/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__ == '__main__':
    main()
