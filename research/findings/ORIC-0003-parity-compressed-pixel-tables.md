---
id: "ORIC-0003"
title: "Store even-coordinate tables and reconstruct odd Oric pixels"
category: "graphics"
cpu: ["6502"]
machines: ["oric-1","oric-atmos"]
status: analyzed
source_analyses: ["../analyses/space-1999/overview.md"]
tags: ["hires","lookup-tables","parity","screen-addressing"]
---

# Store even-coordinate tables and reconstruct odd Oric pixels

## Summary

Store row offsets for even scanlines and quotient/mask pairs for even X coordinates. Derive odd rows by adding one 40-byte stride and odd-X masks by shifting the corresponding even mask. This halves the table footprint compared with all-coordinate tables using the same representation.

## Problem and context

- **Problem:** obtain a HIRES byte address and bit mask without general multiplication/division and without full tables.
- **Use cases:** random pixel/sprite addressing with scarce resident memory.
- **Preconditions:** X in 0…239, Y in 0…199; HIRES `$A000`, stride 40; graphics-byte layout is six visible pixel bits; binary arithmetic and correct carry handling.
- **Applicability:** documented NMOS 6502 instructions and Oric HIRES organization shared by Oric-1 and Atmos. The complete Space 1999 game requires Atmos; this narrower address calculation does not require its ROM routines.

## Provenance

| Field | Value |
| --- | --- |
| Original program | Space: 1999, Oric game; supplied French disk, README version 1.00 / February 2008 |
| Author / publisher | Chema Enguita, principal game code; Twilighte and Dbug, collaborators. Individual routine authorship not separately established |
| Archive | Published Oric Software archive, commit `c81612082482d1f497638ada14ad4640c5e4f1ec` |
| License / usage | No explicit code license identified; no copied large code excerpts or source mirror |
| Supplied disk SHA-256 | `9d85e1d75d9f1e548f4d1e3bc3750085e7c8c125bb6cd110fb604ba86ba3e851` |
| File / symbols / lines | [upstream `game source/NOISE/groutines.s:L97–L175`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/NOISE/groutines.s#L97-L175) (`pixel_address` screen path); [upstream `game source/NOISE/noise-tail.s:L13–L37`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/NOISE/noise-tail.s#L13-L37) (`tab_scan`, `tab_mod06`) |
| First analysis | [Space 1999](../analyses/space-1999/overview.md) |

Assembly evidence is **supplementary published source**, not an ASM file supplied under `research/sources/`. Exact full executable correspondence remains unproven. Original byte hashes and line counts are retained in [upstream manifest](../analyses/space-1999/upstream-manifest.json).

## Original implementation

OSDK/XA. `tab_scan` holds 100 little-endian offsets `0,80,…,7920`. The row number doubles as a byte index into those words. For even Y, the low/high bytes are at Y/Y+1. For odd Y, the preceding even row's high/low bytes are at Y/Y−1, then 40 is added with carry into the high byte.

`tab_mod06` holds 120 quotient/mask pairs, one for each even X. For odd X the code indexes X−1, retrieves the same quotient and shifts its even mask right once. ASL after parity-testing LSR clears the low bit of the original odd value; the comment that this sequence computes “(A/2)−1” is misleading. Algebraically it reconstructs `X−1`.

## Technical explanation

For X=2k+1, `floor(X/6) = floor(2k/6)`. The even remainders 0,2,4 yield masks `$20,$08,$02`; the next odd positions yield `$10,$04,$01`. Therefore address `$A000 + 40Y + floor(X/6)` and mask `$20 >> (X mod 6)` are recovered without a separate odd-coordinate table.

In the odd-row path LSR followed by ROL restores the original row index, while its outgoing carry is clear for legal byte coordinates; ADC #40 then adds the correct stride. The later X mask/shift path supplies clear carry for final address addition in the legal screen case. This flag reasoning is local to that path, not a proof of the scratch-relative negative-X path.

## CPU-specific considerations

A holds coordinates/data, X indexes quotient/mask pairs, Y indexes row bytes; zero-page temporary pointers receive the result. Loads and branches do not universally clear carry. Indexed table reads and branch page crossings make timing alignment-dependent. The code uses documented NMOS instructions and writable temporary state; it is not inherently reentrant.

## Machine-specific considerations

The six-bit mask relates to [Oric HIRES organization](https://library.defence-force.org/books/content/manual_atmos.pdf), graphics chapter. Embedded attributes still occupy screen bytes, so a calculated address does not guarantee that ORing a bit there is a valid drawing operation. Preserve the pixel/control-byte distinction. Porting to another packed display requires new formulas and bounds.

## Performance and resource costs

| Metric | Parity tables | All-coordinate tables with same layout | Evidence |
| --- | ---: | ---: | --- |
| Row offsets | 100×2 = 200 bytes | 200×2 = 400 bytes | Source table entries / arithmetic |
| X quotient and mask | 120×2 = 240 bytes | 240×2 = 480 bytes | Source table entries / arithmetic |
| Total | 440 bytes | 880 bytes | 440-byte reduction; excludes code and temporaries |
| Addressing cycles | Not measured; parity-dependent | Not measured | No speedup claim |

## Advantages

- Saves 440 table bytes relative to that explicit baseline.
- Still uses direct lookup for most coordinate work.
- Encodes address and mask together for the six-pixel format.

## Limitations and risks

Additional parity branches and mask adjustment can cost more cycles. No out-of-range checks are present in this helper. Complete game compatibility, scratch addressing, negative coordinates and attribute-safe writes require separate validation.

## Alternatives

Full tables, split low/high tables, iterative pointer updates for sequential pixels, or shift/add addressing with quotient lookup. A smaller quotient-only helper may be sufficient when the caller does not need a mask.

## Validation record

- **Status:** analyzed.
- **Checks:** source table lengths and contents; arithmetic model checks every one of 48000 legal coordinate pairs against the direct formula.
- **Reproducer:** [inspect_inputs.py](../analyses/space-1999/tools/inspect_inputs.py); results in [verification.json](../analyses/space-1999/verification.json).
- **Limit:** model reads tables and implements explained arithmetic; no assembled CPU execution, table-binary identity proof, benchmark or real-hardware test.
- **Next:** compare actual routine results and timing with full tables at multiple alignments, including interrupts.

## Recommendation for new projects

Consider parity reconstruction when table memory matters and coordinate bounds are fixed. Benchmark both representations before optimizing for speed. Use sequential pointer stepping where traversal already provides a cheaper address recurrence.

## References and related techniques

[Hardware analysis](../analyses/space-1999/hardware-techniques.md), [CPU analysis](../analyses/space-1999/cpu-techniques.md). This pixel-address technique is distinct from ORIC-0001 saved backgrounds and ORIC-0002 charset bank animation.
