#!/usr/bin/env python3
"""Evidence checks and small static models; no 6502/device code is executed."""
import hashlib
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
import inspect_disk as disk

HERE = Path(__file__).resolve().parents[1]
ROOT = disk.ROOT
checks = []


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)


def main():
    source = disk.SOURCE.read_bytes()
    check('original disk checksum unchanged', hashlib.sha256(source).hexdigest() == disk.EXPECTED_SHA256)
    metadata = (disk.SOURCE.parent / 'metadata.md').read_bytes()
    check('original metadata checksum unchanged', hashlib.sha256(metadata).hexdigest() ==
          '4a3ef22b69447d2084e07bc1e453e5a404feba5e7c4ebb1b7d30429898b1f23a')
    sectors, logical, resident, modules = disk.models(source)
    check('1428 unique standard sectors', len(sectors) == 1428)
    check('all ID and data CRCs match', all(s['id_crc_ok'] and s['data_crc_ok'] for s in sectors.values()))
    check('container and payload accounting', len(source) == 537856 and len(logical) == 365568
          and len(source)-len(logical) == 172288)
    manifest = json.loads((HERE / 'extracted/manifest.json').read_text())
    check('manifest source identity and module count', manifest['sha256'] == disk.EXPECTED_SHA256
          and len(manifest['modules']) == 22)
    check('resident extraction exact', (HERE / 'extracted/resident.bin').read_bytes() == resident)
    check('boot sector and relocation exact',
          (HERE / 'extracted/boot-sector.bin').read_bytes() == logical[0x100:0x200] and
          (HERE / 'extracted/boot-relocated.bin').read_bytes() == logical[0x140:0x1e7])

    for mod, recorded in zip(modules, manifest['modules']):
        data = (HERE / 'extracted' / mod['filename']).read_bytes()
        check(f'descriptor {mod["index"]:02X} extraction, size and digest', data == mod['data']
              and len(data) == mod['recovered_pages']*256
              and hashlib.sha256(data).hexdigest() == recorded['sha256'])
        for page, sector in enumerate(recorded['sector_map']):
            off = sector['dsk_offset']
            check(f'descriptor {mod["index"]:02X} page {page} maps to original DSK',
                  source[off:off+256] == data[page*256:page*256+256])
    check('unused descriptor 0C is not spliced onto side 1',
          modules[12]['recovered_pages'] == 5 and modules[12]['pages'] == 133
          and modules[12]['missing_sector'] == [0,42,1])
    check('all other descriptors fully recoverable', all(m['recovered_pages'] == m['pages']
          for m in modules if m['index'] != 12))

    # Source-level assertions for conclusions, not guesses based on labels.
    r = lambda a, n: resident[a-0xf800:a-0xf800+n]
    check('silence vector really encodes 8AFC', r(0xf98d,10) == bytes.fromhex('a9fc8dfeffa98a8dffff'))
    check('resident candidate RTI at FC8A', r(0xfc8a,1) == b'\x40')
    check('IRQ escape has three PLA and RTS', r(0xfa7f,3) == b'\x68'*3 and r(0xfa8d,1) == b'\x60')
    address = 0xfa9f
    load_instructions = []
    block = dict(start=0xf800, data=resident, payload_offset=0)
    while address <= 0xfaf6:
        instruction = disk.decode(block, address)
        load_instructions.append(instruction)
        address += len(instruction['raw'])
    check('load entry SEI and no linear-body CLI', load_instructions[0]['mnemonic'] == 'SEI'
          and all(i['mnemonic'] != 'CLI' for i in load_instructions))

    address, loads = 0xf800, []
    while address <= 0xf987:
        instruction = disk.decode(block, address)
        if instruction['mnemonic'] == 'LDX' and instruction['mode'] == 'imm':
            following = disk.decode(block, address+2)
            if following['mnemonic'] == 'JSR' and following['target'] == 0xfa9f:
                loads.append(instruction['raw'][1])
        address += len(instruction['raw'])
    expected = [0x14,0,1,2,3,4,5,6,7,8,9,10,11,13,14,15,16,17,18,19,21]
    check('literal main descriptor load order and dormant 0C', loads == expected)
    check('picture blitter prefixes agree, assets not assumed identical', all(
          m['data'][:0x31] == modules[1]['data'][:0x31] for m in
          [modules[3],modules[9],modules[15],modules[20]]))
    check('sample IRQ templates agree between 02 and 04',
          modules[2]['data'][0x9d87-0xffd:0x9dd6-0xffd] ==
          modules[4]['data'][0x9d87-0xffd:0x9dd6-0xffd])

    # Every generated analytical instruction location maps to original bytes.
    # The sample relocated view has precisely two initialization-patched bytes.
    count = 0
    pattern = re.compile(r'^([0-9A-F]{4})  DSK=\$([0-9A-F]{6})  ((?:[0-9a-f]{2} ?)+)  ')
    for path in sorted((HERE / 'extracted').glob('*.asm.txt')):
        for line in path.read_text().splitlines():
            match = pattern.match(line)
            check('valid listing row ' + path.name, bool(match))
            addr, off, raw = int(match[1],16), int(match[2],16), bytes.fromhex(match[3])
            if path.name == 'sample-zp.asm.txt':
                mod, relative = modules[2], 0x9d87-0xffd+addr
                expected_raw = bytearray(mod['data'][relative:relative+len(raw)])
                for index, value in ((0x0a,0x00),(0x0b,0x10)):
                    if addr <= index < addr+len(raw):
                        expected_raw[index-addr] = value
            elif path.name == 'final-zp.asm.txt':
                mod, relative = modules[19], 0x609b-0xffd+addr-0x10
                expected_raw = mod['data'][relative:relative+len(raw)]
            elif path.name == 'boot-relocated.asm.txt':
                mod = None
                relative = 0x140+addr-0xa7d0
                expected_raw = logical[relative:relative+len(raw)]
            elif path.name == 'resident.asm.txt':
                mod = None
                relative = 0x400+addr-0xf800
                expected_raw = logical[relative:relative+len(raw)]
            else:
                index = int(path.name.split('-')[1],16)
                mod = modules[index]
                relative = addr-mod['load_address']
                expected_raw = mod['data'][relative:relative+len(raw)]
            logical_off = relative + (mod['logical_offset'] if mod is not None else 0)
            actual_off = sectors[sorted(sectors)[logical_off//256]]['dsk_offset']+logical_off%256
            check('listing original location and decoded bytes', off == actual_off and raw == expected_raw)
            count += 1

    # Tiny independent mathematical models. These are not CPU-emulator tests.
    x, order = 0, []
    while True:
        order.append(x)
        x = (x-1) & 255
        if x == 0:
            break
    check('zero countdown visits every byte exactly once', len(order) == 256 and set(order) == set(range(256)))
    valid_widths = []
    for width in range(256):
        x, copied = (width-1)&255, []
        while True:
            copied.append(x)
            x = (x-1)&255
            if x & 128:
                break
        if copied == list(range(width-1,-1,-1)):
            valid_widths.append(width)
    check('DEX before load then DEX/BPL supports widths 1 to 129', valid_widths == list(range(1,130)))

    bases = list(range(0xa000,0xbf00,256)) + [0xbe40]
    stores = [base+x for x in order for base in bases]
    check('HIRES fill covers exact 8000-byte union with 192 duplicates',
          len(stores) == 8192 and set(stores) == set(range(0xa000,0xbf40)))
    text_bases = [0xbb80,0xbc80,0xbd80,0xbe80,0xbee0]
    text_stores = [base+x for x in order for base in text_bases]
    check('text fill preserves BFE0 and higher', len(text_stores) == 1280 and
          set(text_stores) == set(range(0xbb80,0xbfe0)))
    destinations = [0xb8f0+y for y in range(0x20,256)] + [0xb900+y for y in range(16)] + [0xb9f0+y for y in range(16)]
    check('glyph compositor covers B900 to B9FF exactly once', len(destinations) == 256
          and len(set(destinations)) == 256 and set(destinations) == set(range(0xb900,0xba00)))
    check('41-byte reveal first pass reaches BF40', max(0xa000+row*40+x
          for row in range(200) for x in range(41)) == 0xbf40)

    for value in range(65536):
        low, high = value & 255, value >> 8
        low = (low+1) & 255
        if low == 0:
            high = (high+1) & 255
        assert low+(high<<8) == (value+1) & 65535
    check('operand pointer increment for all 65536 values', True)
    for value in range(256):
        phase, result, pointer_advances = 2, [], 0
        for _ in range(2):
            carry, phase = phase & 1, phase >> 1
            result.append((value >> 4 if carry else value) & 15)
            if phase == 0:
                phase = 2
                pointer_advances += 1
        assert result == [value & 15, value >> 4] and pointer_advances == 1
    check('ending phase operand yields low/high then one pointer increment', True)
    odd_values, x = set(), 0x4f
    while x not in odd_values:
        odd_values.add(x)
        x = (x-2) & 255
    check('dormant odd decrement-by-two cannot terminate', len(odd_values) == 128 and 0 not in odd_values)
    for value in range(256):
        actual = value
        for _ in range(2):
            carry = int(actual >= 128)
            actual = ((actual<<1)|carry) & 255
        assert actual == ((value<<2)|(value>>6)) & 255
    check('CMP 80 plus ROL twice implements rotate-left-two', True)
    # IRQ/JSR conceptual top-first stack. No CPU or device execution implied.
    stack = [0x24,0x23,0x81,0x02,0x90]
    stack = stack[3:]
    return_pc = ((stack[0] | stack[1]<<8)+1) & 65535
    check('discard IRQ frame exposes nearest JSR return', return_pc == 0x9003)
    cycles_fill = 4 + 256*(32*5+2) + 255*3 + 2 + 6
    cycles_delay = 13 + 2 + 256*(2+(255*13+12)+2) + 255*3+2 + 16+6
    check('theoretical fill and delay sums', cycles_fill == 42249 and cycles_delay == 853540)

    # Validate newly written documentation fields, IDs, binary references/links.
    files = list(HERE.glob('*.md')) + [HERE/'extracted/README.md'] + list(
        (ROOT/'research/findings').glob('*000[56]-*.md')) + [
        ROOT/'research/findings/ORIC-0002-masked-charset-bank-animation.md']
    required = {'id','program','cpu','machines','analysis_status','source_revision','analysis_date'}
    for path in files:
        body = path.read_text()
        if path.name != 'README.md':
            front = body.split('---',2)[1]
            fields = set(re.findall(r'^([a-z_]+):',front,re.M))
            fields_required = required if path.parent == HERE else {
                'id','title','category','cpu','machines','status','source_analyses','tags'}
            check('frontmatter fields ' + path.name, fields_required <= fields)
            check('no promoted status ' + path.name, not re.search(r'^status: (validated|benchmarked)$',front,re.M))
        for target in re.findall(r'\]\(([^\n]+?)\)',body):
            if target.startswith(('http:','https:','#')):
                continue
            target = target.strip('<>').split('#',1)[0]
            check('local link ' + target, (path.parent/target).exists() or
                  (path.parent/target).resolve() == HERE/'verification.json')
    for identifier in ['CPU6502-0005','CPU6502-0006','ORIC-0002']:
        owners = []
        for path in list((ROOT/'docs').rglob('*.md')) + list((ROOT/'research/findings').glob('*.md')):
            if re.search(r'^id: '+identifier+r'\s*$',path.read_text(),re.M):
                owners.append(path)
        check('new technique ID unique ' + identifier, len(owners) == 1)
    report = dict(method='Static extraction, byte assertions and mathematical models; no CPU/device execution',
        source_sha256=disk.EXPECTED_SHA256,check_count=len(checks),
        listing_instructions_checked=count,sector_count=1428,crc_mismatches=0,
        recovered_descriptor_count=22,complete_descriptor_count=21,
        incomplete_descriptor='0C: 5 of 133 pages; missing side 0 track 42 sector 1; uninvoked in main',
        model_cases=dict(pointer_increment=65536,nibble_phase=256,circular_shift=256),
        theoretical_cycles=dict(hires_clear_including_RTS=cycles_fill,delay_including_RTS=cycles_delay),
        all_checks_passed=True,benchmark=False,emulator=False,real_hardware=False,
        check_categories=['source identity','sector integrity','payload mappings','listing byte locations',
            'load sequence','static hazards','loop/address/state models','frontmatter and local links','new IDs'])
    (HERE/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
