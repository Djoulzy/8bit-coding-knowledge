#!/usr/bin/env python3
"""Functional evidence for narrowly scoped guidelines, not a CPU benchmark.

The models below are new analytical code. They do not execute the historical
game, emulate the 6502, validate Oric ROMs, or measure execution performance.
Independent oracles check representation, field ordering and memory effects.
"""
import json
import inspect_tape as tape
import verify_analysis


def semantic_grid(width, height, blocked, hazards, objects):
    """Illustrative generic encoding; these are NOT the historical cell values."""
    assert width > 0 and height > 0
    cells = bytearray(width * height)
    for row in range(height):
        for column in range(width):
            position = (row, column)
            cells[row * width + column] = (int(position in blocked)
                                          | (int(position in hazards) << 1)
                                          | (int(position in objects) << 2))
    return cells


def probe(cells, width, height, row, column):
    # Bounds are checked before multiplication/indexing; no display dependency.
    if not (0 <= row < height and 0 <= column < width):
        return True, False, False
    value = cells[row * width + column]
    return bool(value & 1), bool(value & 2), bool(value & 4)


def check_grid():
    queries = changes = 0
    for width, height in ((1, 1), (40, 1), (40, 3), (8, 8)):
        positions = {(r, c) for r in range(height) for c in range(width)}
        blocked = {(r, c) for r, c in positions if (r + c) % 3 == 0}
        hazards = {(r, c) for r, c in positions if (2*r + c) % 5 == 0}
        objects = {(r, c) for r, c in positions if c % 7 == 0}
        cells = semantic_grid(width, height, blocked, hazards, objects)
        for phase in range(2):
            # Oracle uses logical sets, not the packed byte/bit representation.
            expected = {}
            for r in range(-1, height + 1):
                for c in range(-1, width + 1):
                    p = (r, c)
                    expected[p] = ((p in blocked, p in hazards, p in objects)
                                   if p in positions else (True, False, False))
            # Replacing every visual byte must leave every collision result intact.
            for visual_value in (0x00, 0x0A, 0x40, 0xFF):
                display = bytearray([visual_value] * (width * height))
                for p, result in expected.items():
                    assert probe(cells, width, height, *p) == result
                    queries += 1
                assert display == bytearray([visual_value] * len(display))
            if phase == 0:
                # A logical change requires rebuilding/updating the semantic map.
                chosen = (height - 1, width - 1)
                blocked.symmetric_difference_update({chosen})
                hazards.symmetric_difference_update({chosen})
                objects.symmetric_difference_update({chosen})
                old = bytes(cells)
                cells = semantic_grid(width, height, blocked, hazards, objects)
                assert old != bytes(cells)
                changes += 1
    return dict(query_cases=queries, logical_update_cases=changes,
                display_patterns=["$00", "$0A", "$40", "$FF"],
                scope="bounded cell lookup, independent of display; not historical collision semantics")


def rol(value, carry):
    return ((value << 1) | carry) & 255, (value >> 7) & 1


def extract_pair(work, carry):
    accumulator = 0
    for _ in range(2):
        work, carry = rol(work, carry)
        accumulator, carry = rol(accumulator, carry)
    return accumulator, work, carry


def check_carry():
    single = sequences = 0
    for original in range(256):
        for incoming_carry in (0, 1):
            value, _, outgoing = extract_pair(original, incoming_carry)
            assert value == original >> 6 and outgoing == 0
            single += 1
            work, carry = original, incoming_carry
            actual = []
            for _ in range(4):
                value, work, carry = extract_pair(work, carry)
                actual.append(value)
            expected = [(original >> shift) & 3 for shift in (6, 4, 2, 0)]
            assert actual == expected
            sequences += 1
    return dict(single_call_cases=single, four_field_sequence_cases=sequences,
                scope="byte values and both incoming C states; ISA model, not CPU execution")


def copy_pages(memory, source, destination, pages):
    # Generalized model of Y wraparound and DEX/BPL, with explicit preconditions.
    if (source % 256 or destination % 256 or not 1 <= pages <= 128
            or source < 0 or destination < 0
            or source + pages*256 > len(memory)
            or destination + pages*256 > len(memory)
            or not (source + pages*256 <= destination
                    or destination + pages*256 <= source)):
        raise ValueError("Requires aligned, disjoint, in-range pages and count 1..128")
    x, transfers, visited = pages - 1, 0, []
    while True:
        y = 0
        row = []
        while True:
            memory[destination + y] = memory[source + y]
            row.append(y)
            transfers += 1
            y = (y - 1) & 255
            if y == 0:
                break
        assert len(row) == len(set(row)) == 256
        visited.append(row)
        source += 256
        destination += 256
        x = (x - 1) & 255
        if x & 0x80:  # final DEX/BPL exit
            break
    return dict(transfers=transfers, x=x, y=y, visited=visited)


def check_copy():
    cases = rejected = 0
    for source, destination, pages in ((0x5600, 0x5000, 2),
                                       (0x2000, 0x4000, 1),
                                       (0x4000, 0x2000, 3),
                                       (0x0000, 0x8000, 128)):
        for pattern in range(4):
            memory = bytearray(((i * (37 + pattern) + (i >> 8) + pattern) & 255)
                               for i in range(65536))
            before = bytes(memory)
            expected = bytearray(before)
            end = destination + pages*256
            expected[destination:end] = before[source:source + pages*256]
            result = copy_pages(memory, source, destination, pages)
            assert memory == expected  # includes no writes outside destination
            assert result['transfers'] == pages*256
            assert result['x'] == 255 and result['y'] == 0
            assert all(row == [0] + list(range(255, 0, -1)) for row in result['visited'])
            cases += 1
    for source, destination, pages in ((0x2001, 0x4000, 1),
                                       (0x2000, 0x4001, 1),
                                       (0x2000, 0x4000, 0),
                                       (0x2000, 0x4000, 129),
                                       (0x2000, 0x2100, 2),
                                       (0x2000, 0x2000, 1),
                                       (0xFF00, 0x2000, 2)):
        try:
            copy_pages(bytearray(65536), source, destination, pages)
        except ValueError:
            rejected += 1
        else:
            raise AssertionError("Invalid precondition accepted")
    return dict(copy_cases=cases, invalid_contract_cases=rejected,
                page_counts=[1, 2, 3, 128],
                scope="RAM model and traversal; no I/O, overlap, CPU or IRQ emulation")


def verify():
    baseline = verify_analysis.verify()
    block = tape.parse_tape(tape.SOURCE.read_bytes())[1]
    def raw(address, size):
        return block['data'][address - block['start']:address - block['start'] + size]
    assert raw(0x3F0B, 9).hex() == 'a90026712a26712a60'
    assert raw(0x4DDD, 33).hex() == 'a201a90085708572a9508571a9568573a000b172917088d0f9e671e673ca10f060'
    assert raw(0x4B82, 7).hex() == '8dc5041005a201'  # STA does not set the N used by BPL
    return dict(method="source checks, independent functional oracles and stated invariants; no performance measurement",
                original_sha256=baseline['original_sha256'],
                baseline_checks="pass", semantic_grid=check_grid(),
                carry_field_extraction=check_carry(), descending_page_copy=check_copy(),
                historical_runtime_validated=False, irq_or_rom_validated=False)


if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
