#!/usr/bin/env python3
"""Static byte and translated-model checks. Does not execute game instructions."""
import hashlib
import json
import re
import sys
from pathlib import Path
sys.dont_write_bytecode = True
import inspect_disk as disk

BASE=Path(__file__).resolve().parents[1]

def shifted(byte,phase,carry):
    """Translate the accumulator paths at $1A84..$1AEA; flags only as used."""
    a=byte
    def op(kind):
        nonlocal a,carry
        if kind=='ASL': a,carry=(a<<1)&255,a>>7
        elif kind=='ROL': a,carry=((a<<1)|carry)&255,a>>7
        elif kind=='ROR': a,carry=(a>>1)|(carry<<7),a&1
    if phase==0: return a,0
    if phase==1:
        op('ASL'); x=a; op('ASL'); op('ROL'); return x,a&1
    if phase==2:
        op('ASL'); op('ASL'); x=a
        op('ROL'); op('ROL'); return x,a&3
    sequence={3:['ASL','ASL','ROL'],4:['ASL','ASL','ROL','ROL'],
              5:['ROR']*4,6:['ROR']*3}[phase]
    for kind in sequence: op(kind)
    x=a
    op('ROL'); op('ROL')
    return x & ((255<<phase)&255), a & ((1<<phase)-1)

def reverse7(value):
    return sum(((value>>bit)&1)<<(6-bit) for bit in range(7))

def main():
    source=disk.snapshot()
    memory,origins,pages=disk.runtime_model(source)
    initial,initial_origins,_=disk.initial_model(source)
    manifest=json.loads((BASE/'extracted/manifest.json').read_text())
    for item in manifest['files']:
        payload=(BASE/'extracted'/item['file']).read_bytes()
        assert len(payload)==item['length']
        assert hashlib.sha256(payload).hexdigest()==item['sha256']
    assert len(pages)==160
    assert {p['address'] for p in pages}==set(range(0x800,0xa800,256))
    for item in pages:
        assert item['address']==(0xa8-16*item['track']+item['sector'])*256
        a,o=item['address'],item['dsk_offset']
        assert initial[a:a+256]==source[o:o+256]
    assert memory[:0x800]==initial[0x2000:0x2800]
    assert memory[0xa800:0xc000]==initial[0x2800:0x4000]
    # Relocation loop operands and transfer target in original code.
    assert initial[0x2102:0x2108]==bytes.fromhex('bd00289d00a8')
    assert initial[0x213a:0x2140]==bytes.fromhex('bd00209d0000')
    assert initial[0x2150:0x2153]==bytes.fromhex('4c5301')
    # Documented state-copy loops; X ranges 0..15, source and target disjoint.
    loops=[(0x7071,0x20,0x70),(0x707d,0x70,0x20),
           (0x708d,0x20,0x60),(0x7099,0x60,0x20)]
    for a,s,d in loops:
        assert memory[a:a+11]==bytes([0xa2,0,0xb5,s,0x95,d,0xe8,0xe0,0x10,0xd0,0xf7])
    # HGR row tables contain page-relative offsets, not absolute addresses.
    for y in range(192):
        expected=(y%8)*1024+(y//8%8)*128+(y//64)*40
        actual=memory[0x800+y]+256*memory[0x8c0+y]
        assert actual==expected
        assert memory[0x800+y]+39<256
    for b in range(128):
        assert memory[0x980+b]==(0x80|reverse7(b))
    assert memory[0xaf1:0xaf8]==bytes.fromhex('b10029bf910060')
    cleanup={page*256+low+39 for page in range(0x20,0x40)
             for low in (0,0x80,0x28,0xa8,0x50,0xd0)}
    visible_right_edge={0x2000+memory[0x800+y]+256*memory[0x8c0+y]+39
                        for y in range(192)}
    assert cleanup==visible_right_edge and len(cleanup)==192
    assert memory[0x1a34:0x1a42]==bytes.fromhex('808183878f9fbffffefcf8f0e0c0')
    # Pin the translated shifter to the exact source byte span.
    shifter_hash=hashlib.sha256(memory[0x1a84:0x1aeb]).hexdigest()
    cases=0
    for phase in range(7):
        for b in range(256):
            for c in range(2):
                low,high=shifted(b,phase,c)
                assert low&127==((b&127)<<phase)&127
                assert high==((b&127)<<phase)>>7
                cases+=1
    # Exhaust all two-byte joins; EOR and OR agree on disjoint pixel fields.
    joins=0
    for phase in range(7):
        for previous in range(128):
            for current in range(128):
                low,high=shifted(current,phase,0)
                tail=((previous<<phase)>>7)
                assert low&127&tail==0
                assert ((low^tail)&127)==(((current<<phase)|tail)&127)
                joins+=1
    # Validate each listed instruction against its phase-specific byte model.
    boot=bytearray(65536); boot[0x800:0x900]=source[:256]
    boot_origins=[None]*65536; boot_origins[0x800:0x900]=range(256)
    mem,org=boot,boot_origins
    instructions=0
    for line in (BASE/'extracted/selected-disassembly.txt').read_text().splitlines():
        if line=='; Initial DOS-style loader' or line=='; Initial relocation':
            mem,org=initial,initial_origins
        elif line=='; Low resident helpers': mem,org=memory,origins
        match=re.match(r'^([0-9A-F]{4})  DSK=\$([0-9A-F]{6})  ([0-9a-f ]{8})  ',line)
        if not match: continue
        a,o=int(match[1],16),int(match[2],16)
        raw=bytes.fromhex(match[3])
        assert org[a]==o and mem[a:a+len(raw)]==raw
        assert all(source[org[a+i]]==b for i,b in enumerate(raw))
        instructions+=1
    report=dict(method='Static byte assertions and translated Python models; no CPU execution',
        source_sha256=disk.SHA256,extracted_hashes_checked=5,core_sectors_checked=160,
        relocation_copies_checked=2,state_copy_loops_checked=4,row_table_entries_checked=192,
        reversal_table_entries_checked=128,right_edge_addresses_checked=192,
        shift_input_cases=cases,join_input_cases=joins,
        listed_instruction_records_checked=instructions,shifter_sha256=shifter_hash,
        copy_loop_cycles_calculated=dict(core=241,with_rts=247,with_jsr=253),
        benchmark=False,hardware_test=False,
        limits=['Boot ROM/RWTS, IRQ/stack and later disk paths not executed',
                'Full clipping, compositor, actor AI, audio timing and frame rate untested',
                'Translated models verify local algebra, not full binary correctness'])
    (BASE/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()
