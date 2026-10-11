#!/usr/bin/env python3
"""Static extraction of the supplied Karateka image; no historical code execution.

The custom DOS-style loader reads track 1..10, sectors 15..0, into pages A7..08.
Image slots match DOS logical sectors for the internally consistent code map.
No DOS filesystem is assumed. Symbols and assembler dialect are unknown.
"""
import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[4]
BASE = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'research/sources/Apple IIe/Karateka/Karateka (1984)(Broderbund).dsk'
SHA256 = '4399db1c5469299f6a519abd890456ba1bbba70596d72096f1db4a84e5669370'
spec = importlib.util.spec_from_file_location('nmos_decoder',
    ROOT / 'research/analyses/laigle-dor/tools/inspect_tape.py')
decoder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(decoder)

def snapshot():
    data = SOURCE.read_bytes()
    if len(data) != 35*16*256 or hashlib.sha256(data).hexdigest() != SHA256:
        raise ValueError('Input snapshot/geometry changed; review before extraction')
    return data

def sector_offset(track,sector):
    if not (0 <= track < 35 and 0 <= sector < 16):
        raise ValueError('Invalid track/sector')
    return (16*track+sector)*256

def initial_model(data):
    memory = bytearray(65536)
    origins = [None]*65536
    # Standard boot assumptions plus observed descending page/sector loader.
    for address,offset,size in [(0x800,0,256),(0xb600,0,10*256)]:
        for i in range(size):
            memory[address+i],origins[address+i]=data[offset+i],offset+i
    pages=[]
    page=0xa7
    for track in range(1,11):
        for sector in range(15,-1,-1):
            off=sector_offset(track,sector)
            address=page*256
            memory[address:address+256]=data[off:off+256]
            origins[address:address+256]=range(off,off+256)
            pages.append(dict(track=track,sector=sector,dsk_offset=off,address=address))
            page-=1
    assert page==7
    return memory,origins,pages

def runtime_model(data):
    """Byte-provenance copies at $2100; excludes dynamic state/code patches.

    Clear operations are represented by constant bytes and unknown-source
    provenance. This is not a CPU/stack/ROM/Disk-II emulator.
    """
    memory,origins,pages=initial_model(data)
    for source,dest,size in [(0x2800,0xa800,0x1800),(0x2000,0,0x800)]:
        memory[dest:dest+size]=memory[source:source+size]
        origins[dest:dest+size]=origins[source:source+size]
    memory[0x2000:0x6000]=bytes([0x80])*0x4000
    origins[0x2000:0x6000]=[None]*0x4000
    return memory,origins,pages

def listing(memory,origins,start,end):
    block=dict(start=0,data=memory,payload_offset=0)
    address=start
    while address<=end:
        ins=decoder.decode(block,address)
        if any(origins[address+i] is None for i in range(len(ins['raw']))):
            raise ValueError(f'Unknown original byte at ${address:04X}')
        yield f'{address:04X}  DSK=${origins[address]:06X}  {ins["raw"].hex(" "):8}  {ins["mnemonic"]} {ins["operand"]}'.rstrip()
        address+=len(ins['raw'])

def evidence_exports(data,out):
    """Selected instruction spans only; original bytes precede runtime patches."""
    initial,initial_origins,_=initial_model(data)
    memory,origins,_=runtime_model(data)
    boot=bytearray(65536)
    boot_origins=[None]*65536
    boot[0x800:0x900]=data[:256]
    boot_origins[0x800:0x900]=range(256)
    sections=[('Boot-sector code',boot,boot_origins,[(0x801,0x84c),(0x85e,0x878)]),
        ('Initial DOS-style loader',initial,initial_origins,[(0xb715,0xb749),(0xb7b5,0xb7c2)]),
        ('Initial relocation',initial,initial_origins,[(0x2100,0x2169)]),
        ('Low resident helpers',memory,origins,[(0x153,0x169),(0x200,0x25d),(0x300,0x33a),
            (0x348,0x3ed),(0x780,0x7e3),(0xabf,0xaf7),(0xb00,0xc25),
            (0xc40,0xcbd),(0xd00,0xda5),(0xdc0,0xdf9)]),
        ('Renderer',memory,origins,[(0x1900,0x1a33),(0x1a42,0x1c79)]),
        ('Sequence and actor drawing',memory,origins,[(0x6400,0x653f),(0x6780,0x6a74),
            (0x6b00,0x6b9a),(0x7000,0x70c5)]),
        ('Page and input service',memory,origins,[(0x7600,0x7720),(0x774b,0x77a6)]),
        ('Resident high controller',memory,origins,[(0xa300,0xa349),(0xad00,0xad2f),
            (0xb0c0,0xb119),(0xb400,0xb763),
            (0xb77c,0xb925),(0xb960,0xb96a),(0xbc00,0xbc7f)])]
    lines=['; Derived NMOS 6502 listing; descriptive headings are analyst names.',
        '; CPU addresses are phase-specific; DSK offsets are zero-based image bytes.',
        '; Linear spans are evidence aids, not whole-program reachability proof.',
        '; Historical symbols, assembler dialect, ROM and dynamic patches unknown.']
    for title,mem,org,spans in sections:
        lines.append('\n; '+title)
        for start,end in spans:
            lines.append(f'; span ${start:04X}..${end:04X}')
            lines.extend(listing(mem,org,start,end))
    (out/'selected-disassembly.txt').write_text('\n'.join(lines)+'\n')
    tables=dict(row_low=dict(address=0x800,offset=origins[0x800],bytes=list(memory[0x800:0x8c0])),
        row_high=dict(address=0x8c0,offset=origins[0x8c0],bytes=list(memory[0x8c0:0x980])),
        reverse7=dict(address=0x980,offset=origins[0x980],bytes=list(memory[0x980:0xa00])),
        leading_masks=dict(address=0x1a34,offset=origins[0x1a34],bytes=list(memory[0x1a34:0x1a3b])),
        trailing_masks=dict(address=0x1a3b,offset=origins[0x1a3b],bytes=list(memory[0x1a3b:0x1a42])))
    (out/'tables.json').write_text(json.dumps(tables,indent=2)+'\n')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--extract',action='store_true')
    parser.add_argument('--disassemble',nargs=2,metavar=('START_HEX','END_HEX'))
    parser.add_argument('--initial',action='store_true',help='before $2100 copies/clears')
    args=parser.parse_args()
    data=snapshot()
    memory,origins,pages=(initial_model if args.initial else runtime_model)(data)
    if args.disassemble:
        print('\n'.join(listing(memory,origins,*(int(x,16) for x in args.disassemble))))
    if args.extract:
        out=BASE/'extracted'
        out.mkdir(parents=True,exist_ok=True)
        initial,initial_origins,pages=initial_model(data)
        files=[('boot-sector.bin',data[:256],0x800),
               ('boot-dos.bin',data[:0xa00],0xb600),
               ('core-initial.bin',initial[0x800:0xa800],0x800),
               ('resident-low.bin',memory[:0x800],0),
               ('resident-high.bin',memory[0xa800:0xc000],0xa800)]
        records=[]
        for name,payload,address in files:
            (out/name).write_bytes(payload)
            records.append(dict(file=name,address=address,length=len(payload),
                sha256=hashlib.sha256(payload).hexdigest()))
        manifest=dict(source=str(SOURCE.relative_to(ROOT)),source_sha256=SHA256,
            image_bytes=len(data),geometry=dict(tracks=35,sectors=16,sector_bytes=256),
            sector_order='DOS logical-sector image slots; inferred from loader/code consistency',
            cpu_emulation=False,core_sector_map=pages,files=records,
            copies=[dict(source=0x2800,dest=0xa800,length=0x1800),
                    dict(source=0x2000,dest=0,length=0x800)],
            limitations=['ROM/boot/DOS calls not executed','dynamic patches/state not modeled',
                'CPU/IIe/ROM revision and whole-program correctness untested'])
        (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
        evidence_exports(data,out)
        print(json.dumps(records,indent=2))

if __name__=='__main__':
    main()
