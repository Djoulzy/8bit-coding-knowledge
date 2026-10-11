#!/usr/bin/env python3
"""Read-only inspection of the supplied Lode Runner sector image.

No imported machine code is executed. This snapshot stores DOS logical sectors
in ProDOS image order, despite the .dsk suffix. Original assembler/symbols are
unknown. Disassembly uses the repository's documented-NMOS opcode decoder;
linear decoding does not establish reachability or distinguish code from data.
"""
import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[4]
SOURCE = ROOT / 'research/sources/Apple IIe/Lode Runner/Lode Runner (1983)(broderbund)[cr].dsk'
OUTPUT = Path(__file__).resolve().parents[1] / 'extracted'
EXPECTED_SHA256 = 'cbc048a55c2835f1b3b54696660e8902c84c25dac44a6dc94b13a7e8f81379ec'
DOS_TO_SLOT = (0, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 15)

# Reviewed local analysis utility; its main() is not invoked by this import.
spec = importlib.util.spec_from_file_location('nmos_decoder',
    ROOT / 'research/analyses/laigle-dor/tools/inspect_tape.py')
decoder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(decoder)

def disk_offset(track, sector, order=DOS_TO_SLOT):
    if not (0 <= track < 35 and 0 <= sector < 16):
        raise ValueError(f'Invalid DOS track/sector {track}/{sector}')
    return (track * 16 + order[sector]) * 256

def parse(data, order=DOS_TO_SLOT):
    if len(data) != 35 * 16 * 256:
        raise ValueError('Unexpected geometry')
    def sector(track, number):
        off = disk_offset(track, number, order)
        return data[off:off+256]
    vtoc = sector(17, 0)
    if (vtoc[0x34], vtoc[0x35], int.from_bytes(vtoc[0x36:0x38], 'little')) != (35, 16, 256):
        raise ValueError('VTOC geometry mismatch')
    files, deleted, catalog_sectors = [], [], []
    t, s = vtoc[1:3]
    seen_catalog = set()
    while t:
        if (t, s) in seen_catalog:
            raise ValueError('Catalog cycle')
        seen_catalog.add((t, s))
        catalog_sectors.append([t, s])
        cat = sector(t, s)
        for index in range(7):
            pos = 11 + index * 35
            entry = cat[pos:pos+35]
            if entry[0] == 0:
                continue
            record = dict(name=bytes(c & 0x7f for c in entry[3:33]).decode('ascii').rstrip(),
                type=entry[2] & 0x7f, locked=bool(entry[2] & 0x80),
                catalog_offset=disk_offset(t, s, order)+pos,
                catalog_sector_count=int.from_bytes(entry[33:35], 'little'))
            if entry[0] == 255:
                deleted.append(record)
                continue
            track, number = entry[:2]
            lists, pages, seen_lists, seen_pages = [], {}, set(), set()
            while track:
                if (track, number) in seen_lists:
                    raise ValueError('T/S list cycle')
                seen_lists.add((track, number))
                sec = sector(track, number)
                start = int.from_bytes(sec[5:7], 'little')
                lists.append(dict(track=track, sector=number,
                    dsk_offset=disk_offset(track, number, order), file_sector_index=start))
                for i in range(122):
                    dt, ds = sec[12+2*i:14+2*i]
                    if (dt, ds) == (0, 0):
                        continue
                    if start+i in pages or (dt, ds) in seen_pages:
                        raise ValueError('Repeated file data sector')
                    seen_pages.add((dt, ds))
                    pages[start+i] = dict(track=dt, sector=ds,
                        dsk_offset=disk_offset(dt, ds, order), file_sector_index=start+i)
                track, number = sec[1:3]
            if sorted(pages) != list(range(len(pages))):
                raise ValueError('Sparse file not supported by this snapshot extractor')
            if len(lists)+len(pages) != record['catalog_sector_count']:
                raise ValueError('Catalog sector count mismatch')
            mapping = [pages[i] for i in sorted(pages)]
            raw = b''.join(sector(p['track'], p['sector']) for p in mapping)
            if record['type'] == 4:
                load, length = int.from_bytes(raw[:2], 'little'), int.from_bytes(raw[2:4], 'little')
                header = 4
                record['load_address'] = load
            elif record['type'] == 2:
                length, header = int.from_bytes(raw[:2], 'little'), 2
            else:
                raise ValueError('Unexpected live file type')
            if header+length > len(raw):
                raise ValueError('File length exceeds allocation')
            record.update(length=length, header_bytes=header, ts_lists=lists,
                sector_map=mapping, allocated_bytes=len(raw),
                sha256=hashlib.sha256(raw[header:header+length]).hexdigest(),
                data=raw[header:header+length], raw=raw)
            files.append(record)
        t, s = cat[1:3]
    return dict(catalog_sectors=catalog_sectors, deleted_entries=deleted, files=files,
        vtoc=dict(track=17, sector=0, dsk_offset=disk_offset(17, 0, order),
                  version=vtoc[3], volume=vtoc[6], tracks=35, sectors=16, sector_bytes=256))

def payload_offset(record, position):
    index, offset = divmod(position+record['header_bytes'], 256)
    return record['sector_map'][index]['dsk_offset'] + offset

def listing(record, start, end):
    block = dict(start=record['load_address'], data=record['data'], payload_offset=0)
    address = start
    while address <= end:
        ins = decoder.decode(block, address)
        # Each instruction byte may cross into a nonconsecutive disk sector.
        offsets = [payload_offset(record, address-block['start']+i) for i in range(len(ins['raw']))]
        yield f'{address:04X}  DSK=${offsets[0]:06X}  {ins["raw"].hex(" "):8}  {ins["mnemonic"]} {ins["operand"]}'.rstrip()
        address += len(ins['raw'])

def runtime_model(record):
    """Model the three observed loader copies; retain unknown source bytes.

    This is byte copying only, not 6502 emulation. Writes at $C000/$C001 are
    hardware accesses, not RAM. Loader loop endpoints follow post-increment
    comparisons, which intentionally includes two bytes beyond the DOS file.
    """
    memory = bytearray(65536)
    origins = [None] * 65536
    for i, value in enumerate(record['data']):
        address = record['load_address']+i
        memory[address] = value
        origins[address] = payload_offset(record, i)
    for begin, end, delta, step in [(0x8f04,0x9701,-0x8f00,1),
                                   (0x3a00,0x5f01,0x6100,1),
                                   (0x3a00,0x0900,0x0600,-1)]:
        for address in range(begin, end+step, step):
            dest = address+delta
            if dest < 0xc000:
                memory[dest], origins[dest] = memory[address], origins[address]
    return memory, origins

def runtime_listing(record, start, end):
    memory, origins = runtime_model(record)
    block = dict(start=0, data=memory, payload_offset=0)
    address = start
    while address <= end:
        ins = decoder.decode(block, address)
        if any(origins[address+i] is None for i in range(len(ins['raw']))):
            raise ValueError(f'Unknown runtime byte at ${address:04X}')
        yield f'{address:04X}  DSK=${origins[address]:06X}  {ins["raw"].hex(" "):8}  {ins["mnemonic"]} {ins["operand"]}'.rstrip()
        address += len(ins['raw'])

def snapshot():
    data = SOURCE.read_bytes()
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        raise ValueError('Source snapshot changed; review before regenerating')
    return data, parse(data)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--extract', action='store_true')
    parser.add_argument('--disassemble', nargs=2, metavar=('START_HEX', 'END_HEX'))
    parser.add_argument('--runtime', action='store_true', help='apply observed loader RAM copies')
    args = parser.parse_args()
    data, model = snapshot()
    game = next(f for f in model['files'] if f['name'] == 'LODE RUNNER')
    if args.disassemble:
        fn = runtime_listing if args.runtime else listing
        print('\n'.join(fn(game, *(int(v, 16) for v in args.disassemble))))
    if args.extract:
        OUTPUT.mkdir(parents=True, exist_ok=True)
        for record in model['files']:
            name = 'lode-runner' if record['name'] == 'LODE RUNNER' else 'hello'
            record['payload_file'] = name+'.bin'
            (OUTPUT/record['payload_file']).write_bytes(record['data'])
        manifest = dict(source=str(SOURCE.relative_to(ROOT)), sha256=EXPECTED_SHA256,
            image_bytes=len(data), sector_order='ProDOS image slots for DOS logical sectors',
            dos_sector_to_image_slot=list(DOS_TO_SLOT),
            **{k:v for k,v in model.items() if k != 'files'},
            files=[{k:v for k,v in f.items() if k not in ('data','raw')} for f in model['files']])
        (OUTPUT/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
        for name, ranges, fn in [
            ('loader',[(0x07fd,0x07ff),(0x5a00,0x5a22),(0x5f00,0x5fa1)],listing),
            ('startup',[(0x6000,0x6055),(0x6056,0x6146),(0x6178,0x6213)],runtime_listing),
            ('level',[(0x6238,0x64bc)],runtime_listing),
            ('renderer',[(0x79ad,0x7a07),(0x7a25,0x7b83),(0x82aa,0x8327),
                         (0x8336,0x8437),(0x8438,0x84c0)],runtime_listing),
            ('input-audio',[(0x6a12,0x6b58),(0x8631,0x86bd),(0x86ce,0x8744),
                            (0x8746,0x884a),(0x884b,0x8889)],runtime_listing),
            ('scheduler',[(0x6c82,0x6ca6),(0x6cdb,0x6d60),(0x75ce,0x75f3),
                          (0x75f4,0x7715)],runtime_listing),
            ('movement',[(0x64bd,0x65c4),(0x6b85,0x6c81)],runtime_listing),
            ('editor',[(0x7b84,0x7bc1),(0x7c16,0x7c1e),(0x7c29,0x7c4c),
                       (0x7c60,0x7c62),(0x7c71,0x7c8d),(0x8106,0x8115),
                       (0x8148,0x8161),(0x817b,0x819f)],runtime_listing),
            ('disk',[(0x0023,0x0025),(0x0600,0x065c),(0x8e50,0x8e52),
                     (0xb7b5,0xb7c1)],runtime_listing)]:
            lines = []
            for start,end in ranges:
                lines += list(fn(game,start,end))
            (OUTPUT/(name+'.asm.txt')).write_text('\n'.join(lines)+'\n')
        memory, origins = runtime_model(game)
        tables = [(0x1a85,192,'hgr_row_low'),(0x1b45,192,'hgr_row_high_without_page'),
            (0x1c05,48,'logical_rows_low_dynamic_high_terrain_high'),
            (0x1c35,28,'tile_x_half_pixels'),(0x1c51,16,'tile_y_scanline'),
            (0x1c62,56,'tile_x_byte_and_phase'),(0x1c9a,280,'half_pixel_x_byte_and_phase'),
            (0x6ca7,27,'three_phase_guard_update_quotas'),(0x8328,14,'edge_masks'),
            (0x84c1,7,'phase_table_high_bytes'),(0xa200,7*256,'phase_pointer_tables'),
            (0xa900,1024,'shared_pixel_pairs'),(0xad00,22*104,'sprite_row_token_slices')]
        lines = ['# Reconstructed runtime tables. CPU address / original DSK offset / bytes.',
                 '# No original symbols are known; labels below are analytical.']
        for address,size,label in tables:
            lines.append(f'# {label}: ${address:04X}, {size} bytes')
            for i in range(0,size,16):
                a=address+i
                lines.append(f'{a:04X}  DSK=${origins[a]:06X}  {memory[a:a+min(16,size-i)].hex(" ")}')
        (OUTPUT/'tables.hex.txt').write_text('\n'.join(lines)+'\n')
        levels=[]
        for index in range(150):
            track,sector=3+index//16,index%16
            off=disk_offset(track,sector)
            packed=data[off:off+224]
            cells=[value for byte in packed for value in (byte & 15,byte >> 4)]
            levels.append(dict(level=index+1,track=track,sector=sector,dsk_offset=off,
                sha256_sector=hashlib.sha256(data[off:off+256]).hexdigest(),
                tile_counts={str(v):cells.count(v) for v in sorted(set(cells))},
                values_above_9=sum(v>9 for v in cells), player_markers=cells.count(9)))
        (OUTPUT/'level-audit.json').write_text(json.dumps(levels,indent=2)+'\n')
        hello=next(f for f in model['files'] if f['name']=='HELLO')
        (OUTPUT/'hello.basic.txt').write_text(
            '# Analytical Applesoft decoding; original BASIC file is hello.bin.\n'
            f'# DOS payload starts at DSK=${payload_offset(hello,0):06X}.\n'
            '10 TEXT: HOME: HTAB 15: PRINT "LODE RUNNER": '
            'PRINT "\\x04BRUN LODE RUNNER": NEW\n'
            '# The final payload byte $05 after the zero link is preserved in hello.bin.\n')
        print(json.dumps({f['name']:{k:f[k] for k in ('length','sha256')} for f in model['files']}, indent=2))

if __name__ == '__main__':
    main()
