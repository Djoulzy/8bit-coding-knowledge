#!/usr/bin/env python3
"""Read-only Oric TAP inspection; no game code or build scripts are executed.

Addresses are loaded CPU addresses; TAP offsets are zero-based. Reconstructed
6502 syntax is analytical, not evidence of the original assembler dialect.
The opcode matrix contains documented NMOS instructions only. A linear listing
does not establish that bytes are executable. BASIC strings/REM/DATA are kept
literal, with nonprinting bytes escaped. Output is intentionally opt-in.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SOURCE = ROOT / "research/sources/Oric/L'Aigle d'Or/Aigle D'or, Le (1984)(Loriciels).tap"
TOKENS = dict(enumerate([
    'END', 'EDIT', 'STORE', 'RECALL', 'TRON', 'TROFF', 'POP', 'PLOT',
    'PULL', 'LORES', 'DOKE', 'REPEAT', 'UNTIL', 'FOR', 'LLIST', 'LPRINT',
    'NEXT', 'DATA', 'INPUT', 'DIM', 'CLS', 'READ', 'LET', 'GOTO',
    'RUN', 'IF', 'RESTORE', 'GOSUB', 'RETURN', 'REM', 'HIMEM', 'GRAB',
    'RELEASE', 'TEXT', 'HIRES', 'SHOOT', 'EXPLODE', 'ZAP', 'PING', 'SOUND',
    'MUSIC', 'PLAY', 'CURSET', 'CURMOV', 'DRAW', 'CIRCLE', 'PATTERN', 'FILL',
    'CHAR', 'PAPER', 'INK', 'STOP', 'ON', 'WAIT', 'CLOAD', 'CSAVE',
    'DEF', 'POKE', 'PRINT', 'CONT', 'LIST', 'CLEAR', 'GET', 'CALL',
    '!', 'NEW', 'TAB(', 'TO', 'FN', 'SPC(', '@', 'AUTO',
    'ELSE', 'THEN', 'NOT', 'STEP', '+', '-', '*', '/',
    '^', 'AND', 'OR', '>', '=', '<', 'SGN', 'INT',
    'ABS', 'USR', 'FRE', 'POS', 'HEX$', '&', 'SQR', 'RND', 'LN', 'EXP',
    'COS', 'SIN', 'TAN', 'ATN', 'PEEK', 'DEEK', 'LOG', 'LEN',
    'STR$', 'VAL', 'ASC', 'CHR$', 'PI', 'TRUE', 'FALSE', 'KEY$',
    'SCRN', 'POINT', 'LEFT$', 'RIGHT$', 'MID$', 'GO',
], 0x80))

# Each cell is mnemonic:addressing mode, '--' is undocumented on NMOS 6502.
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
assert len(MATRIX) == 256
LENGTH = dict(imp=1, acc=1, imm=2, zp=2, zpx=2, zpy=2, inx=2,
              iny=2, rel=2, abs=3, abx=3, aby=3, ind=3)


def parse_tape(data):
    blocks, pos = [], 0
    while pos < len(data):
        begin = pos
        while pos < len(data) and data[pos] == 0x16:
            pos += 1
        if pos - begin < 3 or pos >= len(data) or data[pos] != 0x24:
            raise ValueError(f'Invalid leader at TAP ${begin:06X}')
        pos += 1
        if pos + 9 > len(data):
            raise ValueError('Truncated header')
        h = data[pos:pos+9]
        pos += 9
        stop = data.index(0, pos)
        name = data[pos:stop].decode('ascii')
        pos = stop + 1
        end, start = int.from_bytes(h[4:6], 'big'), int.from_bytes(h[6:8], 'big')
        size = end - start + 1
        if size <= 0 or pos + size > len(data):
            raise ValueError('Invalid payload length')
        payload = data[pos:pos+size]
        blocks.append(dict(name=name, header_offset=begin, payload_offset=pos,
                           header=h.hex(), start=start, end=end, size=size,
                           sha256=hashlib.sha256(payload).hexdigest(), data=payload))
        pos += size
    return blocks


def basic_lines(block):
    data, pos = block['data'], 0
    while pos + 2 <= len(data):
        nxt = int.from_bytes(data[pos:pos+2], 'little')
        if nxt == 0:
            return
        if pos + 4 > len(data):
            raise ValueError('Truncated BASIC line')
        number = int.from_bytes(data[pos+2:pos+4], 'little')
        end = data.index(0, pos+4)
        expected = block['start'] + end + 1
        if nxt != expected:
            raise ValueError(f'Broken BASIC link at ${block["start"]+pos:04X}: ${nxt:04X} != ${expected:04X}')
        yield dict(number=number, address=block['start']+pos,
                   offset=block['payload_offset']+pos, next=nxt,
                   raw=data[pos+4:end], end_address=block['start']+end)
        pos = end + 1


def detokenize(raw):
    quoted, literal, rem = False, False, False
    out = []
    for c in raw:
        if c == 0x22:
            quoted = not quoted
        if c >= 0x80 and not quoted and not literal:
            out.append(TOKENS.get(c, f'<${c:02X}>'))
            if c in (0x91, 0x9D):
                literal = True
                rem = c == 0x9D
        elif 0x20 <= c <= 0x7E:
            out.append(chr(c))
        else:
            out.append(f'\\x{c:02X}')
        # DATA is literal until an unquoted colon; REM remains literal.
        if literal and c == 0x3A and not quoted and not rem:
            literal = False
    return ''.join(out)


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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=SOURCE)
    parser.add_argument('--block', type=int, choices=(1, 2), default=2)
    parser.add_argument('--basic', action='store_true')
    parser.add_argument('--extract', type=Path, metavar='DIRECTORY', help='save exact TAP blocks/payloads, analytical BASIC text and manifest')
    parser.add_argument('--disassemble', nargs=2, metavar=('START', 'END'), help='inclusive hex addresses; linear, unclassified')
    args = parser.parse_args()
    data = args.source.read_bytes()
    blocks = parse_tape(data)
    block = blocks[args.block-1]
    if args.extract:
        args.extract.mkdir(parents=True, exist_ok=True)
        manifest = dict(source=str(args.source.relative_to(ROOT)) if args.source.is_relative_to(ROOT) else str(args.source),
                        size=len(data), sha256=hashlib.sha256(data).hexdigest(), blocks=[])
        for b in blocks:
            filename = b['name'].lower()
            (args.extract / (filename + '.bin')).write_bytes(b['data'])
            envelope = data[b['header_offset']:b['payload_offset']+b['size']]
            (args.extract / (filename + '.tap')).write_bytes(envelope)
            lines = list(basic_lines(b))
            text = ['# Analytical BASIC reconstruction; not original source.',
                    '# CPU addresses and zero-based TAP offsets refer to the original image.',
                    '# Nonprinting bytes are escaped. Linked tail records can be nonsemantic.']
            text.extend(f'{line["number"]:5d} CPU ${line["address"]:04X} TAP ${line["offset"]:06X} | {detokenize(line["raw"])}' for line in lines)
            (args.extract / (filename + '.basic.txt')).write_text('\n'.join(text)+'\n', encoding='utf-8')
            manifest['blocks'].append({**{k:v for k,v in b.items() if k != 'data'},
                                      'payload_file':filename+'.bin', 'basic_file':filename+'.basic.txt',
                                      'tape_file':filename+'.tap', 'tape_size':len(envelope),
                                      'tape_sha256':hashlib.sha256(envelope).hexdigest(),
                                      'basic_line_count':len(lines), 'basic_sentinel_address':lines[-1]['end_address']+1})
        (args.extract / 'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
        print(f'Extracted {len(blocks)} blocks to {args.extract}')
    elif args.basic:
        for line in basic_lines(block):
            print(f'{line["number"]:5d} CPU ${line["address"]:04X} TAP ${line["offset"]:06X} | {detokenize(line["raw"])}')
    elif args.disassemble:
        address, end = (int(v.removeprefix('$'), 16) for v in args.disassemble)
        while address <= end:
            inst = decode(block, address)
            print(f'${address:04X} TAP ${inst["offset"]:06X} {inst["raw"].hex(" ").upper():8} {inst["mnemonic"]:4} {inst["operand"]}')
            address += len(inst['raw'])
    else:
        summary = []
        for b in blocks:
            lines = list(basic_lines(b))
            summary.append({**{k:v for k,v in b.items() if k != 'data'},
                            'basic_line_count':len(lines),
                            'basic_sentinel_address':lines[-1]['end_address']+1})
        print(json.dumps(dict(source=str(args.source.relative_to(ROOT)) if args.source.is_relative_to(ROOT) else str(args.source),
                              size=len(data), sha256=hashlib.sha256(data).hexdigest(), blocks=summary), indent=2))


if __name__ == '__main__':
    main()
