#!/usr/bin/env python3
"""Static Vip4 MFM extraction; never executes imported code.

Only this image's standard 17 x 256-byte sectors and geometry 1 are supported.
Disassembly is analytical NMOS 6502 syntax, with no claim of original symbols.
A linear listing is not a reachability proof. CRC mismatches are reported.
"""
import argparse
import binascii
import hashlib
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SOURCE = ROOT / "research/sources/Oric/Vip4 Demo/vip4.dsk"
OUTPUT = Path(__file__).resolve().parents[1] / "extracted"
EXPECTED_SHA256 = "555e811187069b29bfc6cf657be7f19f8c49aa8d25fbbeeb8ab4718ad2577558"

MATRIX = '''
BRK:imp ORA:inx -- -- -- ORA:zp ASL:zp -- PHP:imp ORA:imm ASL:acc -- -- ORA:abs ASL:abs --
BPL:rel ORA:iny -- -- -- ORA:zpx ASL:zpx -- CLC:imp ORA:aby -- -- -- ORA:abx ASL:abx --
JSR:abs AND:inx -- -- BIT:zp AND:zp ROL:zp -- PLP:imp AND:imm ROL:acc -- BIT:abs AND:abs ROL:abs --
BMI:rel AND:iny -- -- -- AND:zpx ROL:zpx -- SEC:imp AND:aby -- -- -- AND:abx ROL:abx --
RTI:imp EOR:inx -- -- -- EOR:zp LSR:zp -- PHA:imp EOR:imm LSR:acc -- JMP:abs EOR:abs LSR:abs --
BVC:rel EOR:iny -- -- -- EOR:zpx LSR:zpx -- CLI:imp EOR:aby -- -- -- EOR:abx LSR:abx --
RTS:imp ADC:inx -- -- -- ADC:zp ROR:zp -- PLA:imp ADC:imm ROR:acc -- JMP:ind ADC:abs ROR:abs --
BVS:rel ADC:iny -- -- -- ADC:zpx ROR:zpx -- SEI:imp ADC:aby -- -- -- ADC:abx ROR:abx --
-- STA:inx -- -- STY:zp STA:zp STX:zp -- DEY:imp -- TXA:imp -- STY:abs STA:abs STX:abs --
BCC:rel STA:iny -- -- STY:zpx STA:zpx STX:zpy -- TYA:imp STA:aby TXS:imp -- -- STA:abx -- --
LDY:imm LDA:inx LDX:imm -- LDY:zp LDA:zp LDX:zp -- TAY:imp LDA:imm TAX:imp -- LDY:abs LDA:abs LDX:abs --
BCS:rel LDA:iny -- -- LDY:zpx LDA:zpx LDX:zpy -- CLV:imp LDA:aby TSX:imp -- LDY:abx LDA:abx LDX:aby --
CPY:imm CMP:inx -- -- CPY:zp CMP:zp DEC:zp -- INY:imp CMP:imm DEX:imp -- CPY:abs CMP:abs DEC:abs --
BNE:rel CMP:iny -- -- -- CMP:zpx DEC:zpx -- CLD:imp CMP:aby -- -- -- CMP:abx DEC:abx --
CPX:imm SBC:inx -- -- CPX:zp SBC:zp INC:zp -- INX:imp SBC:imm NOP:imp -- CPX:abs SBC:abs INC:abs --
BEQ:rel SBC:iny -- -- -- SBC:zpx INC:zpx -- SED:imp SBC:aby -- -- -- SBC:abx INC:abx --
'''.split()

LENGTH = dict(imp=1, acc=1, imm=2, zp=2, zpx=2, zpy=2, inx=2,
              iny=2, rel=2, abs=3, abx=3, aby=3, ind=3)

def decode(block, address):
    pos = address - block['start']
    if not 0 <= pos < len(block['data']):
        raise ValueError(f'Address ${address:04X} outside block')
    op = block['data'][pos]
    cell = MATRIX[op]
    if cell == '--':
        return dict(address=address, offset=block['payload_offset']+pos,
                    raw=bytes([op]), mnemonic='.byte', mode='data', operand=f'${op:02X}', target=None)
    mnemonic, mode = cell.split(':')
    raw = block['data'][pos:pos+LENGTH[mode]]
    if len(raw) != LENGTH[mode]:
        raise ValueError('Truncated instruction')
    operand, target = '', None
    if len(raw) == 2:
        v = raw[1]
        operand = f'${v:02X}'
        if mode == 'imm': operand = '#' + operand
        elif mode == 'zpx': operand += ',X'
        elif mode == 'zpy': operand += ',Y'
        elif mode == 'inx': operand = '(' + operand + ',X)'
        elif mode == 'iny': operand = '(' + operand + '),Y'
        elif mode == 'rel':
            target = (address+2+(v if v < 128 else v-256)) & 0xFFFF
            operand = f'${target:04X}'
    elif len(raw) == 3:
        v = int.from_bytes(raw[1:], 'little')
        operand = f'${v:04X}'
        if mode == 'abx': operand += ',X'
        elif mode == 'aby': operand += ',Y'
        elif mode == 'ind': operand = '(' + operand + ')'
        if mnemonic in ('JSR', 'JMP') and mode == 'abs': target = v
    elif mode == 'acc': operand = 'A'
    return dict(address=address, offset=block['payload_offset']+pos,
                raw=raw, mnemonic=mnemonic, mode=mode, operand=operand, target=target)

def parse_disk(data):
    assert data[:8] == b'MFM_DISK'
    sides, tracks, geometry = struct.unpack_from('<III', data, 8)
    assert (sides, tracks, geometry) == (2, 42, 1)
    assert len(data) == 256 + sides * tracks * 6400
    sectors = {}
    for ti in range(sides * tracks):
        track_offset = 256 + ti * 6400
        track = data[track_offset:track_offset + 6400]
        pos, found = 0, []
        while True:
            ident = track.find(bytes.fromhex('a1a1a1fe'), pos)
            if ident < 0:
                break
            c, h, r, n = track[ident+4:ident+8]
            assert (h, c) == divmod(ti, tracks) and n == 1
            mark = track.find(bytes.fromhex('a1a1a1fb'), ident+10)
            assert mark >= 0 and mark+262 <= len(track)
            key = (h, c, r)
            assert key not in sectors
            payload = track[mark+4:mark+260]
            stored_id = int.from_bytes(track[ident+8:ident+10], 'big')
            stored_data = int.from_bytes(track[mark+260:mark+262], 'big')
            sectors[key] = dict(side=h, track=c, sector=r,
                dsk_offset=track_offset+mark+4, data=payload,
                id_crc_ok=binascii.crc_hqx(track[ident:ident+8], 0xffff)==stored_id,
                data_crc_ok=binascii.crc_hqx(track[mark:mark+260], 0xffff)==stored_data)
            found.append(r)
            pos = mark+262
        assert sorted(found) == list(range(1,18))
    return sectors


def models(data):
    sectors = parse_disk(data)
    order = sorted(sectors)
    logical = b''.join(sectors[k]['data'] for k in order)
    resident = logical[0x400:0xc00]
    modules = []
    for index in range(22):
        sector, encoded_track, pages, low, high = [resident[a-0xf800+index]
            for a in (0xfc19,0xfc30,0xfc47,0xfc5e,0xfc74)]
        side, track = encoded_track >> 7, encoded_track & 0x7f
        begin = (side*42*17+track*17+sector-1)*256
        # Follow the LOADER's track rollover ($80), not the host image's
        # 42-track side boundary. Unused descriptor $0C runs off side 0.
        maps, missing = [], None
        read_side, read_track, read_sector = side, track, sector
        for page in range(pages):
            key = (read_side, read_track, read_sector)
            if key not in sectors:
                missing = list(key)
                break
            maps.append(sectors[key])
            read_sector += 1
            if read_sector == 18:
                read_sector = 1
                read_track += 1
            if read_track == 128:
                read_side, read_track, read_sector = 1, 0, 1
        payload = b''.join(sec['data'] for sec in maps)
        modules.append(dict(index=index, side=side, track=track, sector=sector,
            pages=pages, recovered_pages=len(maps), missing_sector=missing,
            load_address=low+(high<<8), logical_offset=begin,
            data=payload, filename=(f'module-{index:02x}.bin' if missing is None
                else f'descriptor-{index:02x}-prefix.bin'), sector_map=maps))
    return sectors, logical, resident, modules


def listing(payload, base, start, end, mapping):
    block = dict(start=base, data=payload, payload_offset=0)
    addr = start
    while addr <= end:
        i = decode(block, addr)
        offset = addr-base
        rawoff = mapping(offset)
        yield f'{addr:04X}  DSK=${rawoff:06X}  {i["raw"].hex(" "):8}  {i["mnemonic"]} {i["operand"]}'.rstrip()
        addr += len(i['raw'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--extract', action='store_true')
    parser.add_argument('--module', type=lambda x:int(x,16))
    parser.add_argument('--disassemble', nargs=2, metavar=('START_HEX','END_HEX'))
    args = parser.parse_args()
    data = SOURCE.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    assert digest == EXPECTED_SHA256, 'Source snapshot differs; review before regenerating'
    sectors, logical, resident, modules = models(data)
    def raw(logoff):
        key = sorted(sectors)[logoff//256]
        return sectors[key]['dsk_offset'] + logoff%256
    if args.extract:
        OUTPUT.mkdir(parents=True, exist_ok=True)
        records = []
        for mod in modules:
            (OUTPUT/mod['filename']).write_bytes(mod['data'])
            entry = {k:v for k,v in mod.items() if k not in ('data','sector_map')}
            entry['sha256'] = hashlib.sha256(mod['data']).hexdigest()
            entry['sector_map'] = [{k:v for k,v in sec.items() if k!='data'} for sec in mod['sector_map']]
            records.append(entry)
        (OUTPUT/'resident.bin').write_bytes(resident)
        (OUTPUT/'boot-sector.bin').write_bytes(logical[0x100:0x200])
        (OUTPUT/'boot-relocated.bin').write_bytes(logical[0x140:0x1e7])
        (OUTPUT/'resident.asm.txt').write_text('\n'.join(listing(resident,0xf800,0xf800,0xfc00,lambda p:raw(p+0x400)))+'\n')
        (OUTPUT/'boot-relocated.asm.txt').write_text('\n'.join(listing(logical[0x140:0x1e7],0xa7d0,0xa7d0,0xa876,lambda p:raw(p+0x140)))+'\n')
        manifest = dict(source=str(SOURCE.relative_to(ROOT)),sha256=digest,
            header=dict(sides=2,tracks=42,geometry=1,track_bytes=6400),
            sector_count=len(sectors),logical_bytes=len(logical),
            id_crc_mismatches=sum(not s['id_crc_ok'] for s in sectors.values()),
            data_crc_mismatches=sum(not s['data_crc_ok'] for s in sectors.values()),
            resident=dict(logical_offset=0x400,load_address=0xf800,bytes=2048,
                sha256=hashlib.sha256(resident).hexdigest(),
                sector_map=[{k:v for k,v in sectors[key].items() if k!='data'} for key in sorted(sectors)[4:12]]),
            modules=records)
        spans = {
            0:[(0xc000,0xc0bc)], 1:[(0x1000,0x1049)],
            2:[(0x9d0d,0x9dd5)], 5:[(0x1000,0x106b)],
            6:[(0x1000,0x117c)], 8:[(0x1000,0x1084)],
            0x0b:[(0x0600,0x0610),(0x0741,0x0790),(0x87fe,0x883a),(0x883b,0x88a1),(0x88b2,0x8971),(0x89d9,0x8a18),(0x8ae4,0x8aff)],
            0x0d:[(0x1000,0x1045)],
            0x13:[(0x60cb,0x6238)], 0x14:[(0x1000,0x1049)]}
        for index, ranges in spans.items():
            mod = modules[index]
            lines = []
            for start,end in ranges:
                lines.extend(listing(mod['data'],mod['load_address'],start,end,
                    lambda p, mod=mod:raw(mod['logical_offset']+p)))
            (OUTPUT/f'module-{index:02x}-selected.asm.txt').write_text('\n'.join(lines)+'\n')
        sample = modules[2]
        sample_offset = 0x9d87-sample['load_address']
        zp = bytearray(sample['data'][sample_offset:sample_offset+256])
        zp[0x0a:0x0c] = bytes([0x00,0x10])
        (OUTPUT/'sample-zp.asm.txt').write_text('\n'.join(listing(zp,0,0,0x4e,
            lambda p:raw(sample['logical_offset']+sample_offset+p)))+'\n')
        final = modules[0x13]
        final_offset = 0x609b-final['load_address']
        (OUTPUT/'final-zp.asm.txt').write_text('\n'.join(listing(
            final['data'][final_offset:final_offset+56],0x10,0x10,0x3f,
            lambda p:raw(final['logical_offset']+final_offset+p)))+'\n')
        (OUTPUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
        print(json.dumps({k:v for k,v in manifest.items() if k not in ('modules','resident')}))
    if args.disassemble:
        start,end = [int(v,16) for v in args.disassemble]
        if args.module is None:
            payload,base,logoff=resident,0xf800,0x400
        else:
            mod=modules[args.module]
            payload,base,logoff=mod['data'],mod['load_address'],mod['logical_offset']
        print('\n'.join(listing(payload,base,start,end,lambda p:raw(p+logoff))))
    if not args.extract and not args.disassemble:
        for mod in modules:
            print(f'{mod["index"]:02X}: side {mod["side"]}, track {mod["track"]}, sector {mod["sector"]}; {mod["pages"]} requested pages, {mod["recovered_pages"]} recovered, at ${mod["load_address"]:04X}')

if __name__ == '__main__':
    main()
