#!/usr/bin/env python3
"""Reproduce extraction checks and narrow binary-arithmetic models.

This is not a 6502 emulator or a performance benchmark. Models below express
the decoded binary-mode instruction semantics; no historical code is executed.
"""
import hashlib
import json
from pathlib import Path
import inspect_tape as tape


def multiply_model(multiplicand, multiplier):
    accumulator, low = 0, 0
    for _ in range(8):
        carry = multiplier & 1
        multiplier >>= 1
        if carry:
            result = accumulator + multiplicand  # CLC; ADC $70
            accumulator, carry = result & 255, int(result > 255)
        next_carry = accumulator & 1
        accumulator = (accumulator >> 1) | (carry << 7)
        low = (low >> 1) | (next_carry << 7)
    return accumulator * 256 + low


def verify():
    original = tape.SOURCE.read_bytes()
    digest = hashlib.sha256(original).hexdigest()
    assert digest == '7f01e1a3d05825aab887952cd5711bea69d6525730aba5c1e25c814334fe77d7'
    blocks = tape.parse_tape(original)
    extracted = Path(__file__).resolve().parents[1] / 'extracted'
    for b in blocks:
        assert (extracted / (b['name'].lower()+'.bin')).read_bytes() == b['data']
        envelope = original[b['header_offset']:b['payload_offset']+b['size']]
        split = (extracted / (b['name'].lower()+'.tap')).read_bytes()
        assert split == envelope
        restored = tape.parse_tape(split)
        assert len(restored) == 1 and restored[0]['data'] == b['data']
        list(tape.basic_lines(b))  # validate every pointer, terminator and record
    b = blocks[1]
    def raw(a, n):
        return b['data'][a-b['start']:a-b['start']+n]
    # Tie the arithmetic model and patch interpretation to this exact artifact.
    assert raw(0x3E00, 24).hex() == 'a9008572a208467190031865706a6672cad0f38573a47260'
    assert raw(0x3E21, 26).hex() == 'a56a8570a928857120003e1869a0856398656985629002e66360'
    assert raw(0x3F0B, 9).hex() == 'a90026712a26712a60'
    assert raw(0x3E56, 2) == b'\xEA\xEA'
    assert raw(0x3E80, 2) == b'\xEA\xEA'
    assert (0x6211).to_bytes(2, 'little') == b'\x11\x62'
    assert (60138).to_bytes(2, 'little') == b'\xEA\xEA'
    assert raw(0x2283, 1) == b'\x60'
    assert raw(0x4EF8, 3) == b'\x20\x9B\xF8'
    assert raw(0x4DDD, 0x21).hex() == 'a201a90085708572a9508571a9568573a000b172917088d0f9e671e673ca10f060'
    assert raw(0x4EEA, 14).hex() == 'a200bdf0b89d0059cad0f74c004e'
    assert raw(0x4EF8, 15).hex() == '209bf8a200bd00599df0b8cad0f760'
    cases = 0
    for m in range(256):
        for n in range(256):
            assert multiply_model(m, n) == m*n, (m, n)
            cases += 1
    address_cases = 0
    for y in range(200):
        for x in range(40):
            product = multiply_model(y, 40)
            high = (product >> 8) + 0xA0
            assert high <= 0xFF  # first ADC cannot leak carry into low-byte add
            low = (product & 255) + x
            address = (high + (low >> 8))*256 + (low & 255)
            assert address == 0xA000 + 40*y + x
            address_cases += 1
    buffers = []
    for index in (243, 244, 245, 246, 249, 250):
        width, height = raw(0x9400+index, 1)[0], raw(0x9500+index, 1)[0]
        pointer = raw(0x9600+index, 1)[0] + 256*raw(0x9700+index, 1)[0]
        assert pointer & 255 == 0
        assert width > 0 and height > 0 and width*height <= 253
        buffers.append(dict(index=index, pointer=f'${pointer:04X}', width=width,
                            height=height, bytes=width*height))
    # Copy traversal starts at zero, wraps down through 255, ends at 1.
    indices = [0] + list(range(255, 0, -1))
    assert len(indices) == len(set(indices)) == 256
    unpack_cases = 0
    for value in range(256):
        for initial_carry in (0, 1):
            work, carry = value, initial_carry
            groups = []
            for _ in range(4):
                accumulator = 0  # LDA #$00 preserves carry
                for _ in range(2):
                    next_carry = work >> 7
                    work = ((work << 1) | carry) & 255  # ROL $71
                    carry = next_carry
                    next_carry = accumulator >> 7
                    accumulator = ((accumulator << 1) | carry) & 255  # ROL A
                    carry = next_carry
                groups.append(accumulator)
            assert groups == [(value >> shift) & 3 for shift in (6, 4, 2, 0)]
            unpack_cases += 1
    # Conditional static cycle counts from MOS instruction tables, not measurements.
    multiply_base = (2+3+2) + 8*(5+3+2+5+2) + (7*3+2) + (3+3+6)
    by_40 = multiply_base + 4*2  # replacing taken BCC with CLC/ADC costs +4 per set bit
    address_base = (3+3+2+3+6) + by_40 + (2+2+3+2+3+3+3+6)
    reset = (2+2+3+3+2+3+2+3) + 2*(2+256*(5+6+2)+(255*3+2)+5+5+2) + (3+2) + 6
    save = 2 + 256*(4+5+2) + (255*3+2) + 240 + 3
    restore = 2 + 256*(4+5+2) + (255*4+2) + 6
    cycles = dict(multiply_min=multiply_base, multiply_max=multiply_base+4*8,
                  multiply_by_40=by_40,
                  address_by_40_no_low_carry=address_base,
                  address_by_40_low_carry=address_base-3+2+5,
                  reset_512_bytes=reset,
                  save_256_bytes_before_clear=save,
                  restore_256_bytes_after_rom=restore)
    assert list(cycles.values()) == [178, 210, 186, 227, 231, 8249, 3828, 3846]
    return dict(method='static checks and binary arithmetic model; no hardware/emulator run',
                original_sha256=digest, blocks_verified=len(blocks),
                standalone_tap_blocks_verified=len(blocks),
                linked_basic_records=[len(list(tape.basic_lines(k))) for k in blocks],
                multiply_cases=cases, hires_address_cases=address_cases,
                carry_unpack_cases=unpack_cases,
                restore_buffers=buffers, theoretical_cycles=cycles)


if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
