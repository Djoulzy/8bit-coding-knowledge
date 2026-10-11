---
id: "APPLE2-0003"
title: "Shift and reflect seven-bit HGR sprite rows at runtime"
category: "graphics"
cpu: ["6502"]
machines: ["apple-iie"]
status: analyzed
source_analyses: ["../analyses/karateka/overview.md"]
tags: ["hgr", "pixel-phase", "reflection", "packed-pixels", "runtime-shifts"]
---

# Shift and reflect seven-bit HGR sprite rows at runtime

## Summary

Keep packed sprite rows in one form, split each byte into phase-shifted pixel
fragments at draw time and reflect the resulting seven-bit fields with a small
lookup table. Karateka combines specialized accumulator shifts with a 128-byte
reflection table and reversed destination traversal. This exchanges runtime
work for sharing source rows across pixel alignment and facing directions.

## Problem and context

- **Problem:** align and mirror seven-pixel-byte images without storing every
  phase and facing as separate complete sprites.
- **Use cases:** memory-constrained HGR engines drawing reusable packed layers.
- **Preconditions:** phase 0..6, valid nonzero image dimensions/source extent,
  legal row coordinates, known screen bit-7/mask convention and exclusive
  ownership of scratch and composition patches.
- **Applicability:** Apple II ordinary HGR packing. The inspected implementation
  uses NMOS 6502 instructions; exact IIe/CPU/ROM variant and displayed colors
  are untested. Other pixel-byte formats require adapted shifts/masks/tables.

## Provenance

| Field | Value |
| --- | --- |
| Original program | Karateka; supplied 1984/Broderbund-marked disk |
| Author / publisher | Jordan Mechner / Broderbund; individual routine authorship unknown |
| Archive / license | Import origin and license grant unknown |
| Original file | [Karateka (1984)(Broderbund).dsk](<../sources/Apple IIe/Karateka/Karateka (1984)(Broderbund).dsk>) |
| Repository baseline | `d02edc77fa0a02d3f679af22456ca1c762c305dc` |
| Image SHA-256 | `4399db1c5469299f6a519abd890456ba1bbba70596d72096f1db4a84e5669370` |
| Shifter | CPU `$1A84–$1AEA`, `DSK=$009284–$0092EA` |
| Normal / reflected workers | `$1927–$1A33`, `DSK=$009127–$009233`; `$1AF4–$1C5A`, `DSK=$0092F4–$00945A` |
| Reflection table | `$0980–$09FF`, `DSK=$00A180–$00A1FF` |
| Source lines / dialect | Unavailable; binary-only input, no original symbols or assembler |
| First analysis | [Karateka overview](../analyses/karateka/overview.md) |

The [selected listing](../analyses/karateka/extracted/selected-disassembly.txt)
and [table export](../analyses/karateka/extracted/tables.json) retain exact byte
evidence. The [author's account](https://www.jordanmechner.com/en/games-movies/karateka/)
corroborates game provenance, not this disk's original-edition equivalence.

## Original implementation

Original source syntax is unknown. The following is an analyst-written pixel
model, not recovered historical assembly:

~~~text
pixels = source_byte AND $7F
low = (pixels << phase) AND $7F
overflow = (pixels << phase) >> 7
joined = low OR previous_overflow
screen_byte = joined OR $80
~~~

The worker actually uses EOR for the fragment join, because its pixel fields
are disjoint. It then executes the mode-selected OR/AND/NOP operation and stores
the byte. Boundary handling retains pixels outside the shifted sprite span.

## Technical explanation

`$1A61` reads record height then byte width and advances `$03/$04` past the
two-byte header. `$1927` keeps the original row stride while adjusting visible
width/source skip for horizontal clipping. A byte shifts through `$1A84` using
phase `$10`; returned A supplies current low pixels and `$1A` the next fragment.
The previous fragment occupies the low p bits; the current fragment occupies
bits p..6. Thus their EOR is equal to OR under the legal phase contract.

The shifter has separate paths. Phase zero returns the input and clears the
fragment. Small phases use ASL/ROL; phases five/six use ROR sequences followed
by ROL and masks. Incoming carry may enter those RORs, but masked pixel fields
are independent of it. Source bit 7 is excluded from the verified pixel contract;
returned A bit 7 is not uniformly preserved. The worker supplies `$80` afterward.

For reflection, `$1AF4` saves phase/anchor. Nonzero phase becomes `7−phase`;
zero phase decrements the byte anchor instead. Source bytes are still read in
ascending order; destination byte offsets decrease. Before lookup, the worker
forces bit 7 and indexes `$0900,X`, so X is `$80..$FF` and only the upper half
is used: `$0980–$09FF`. All entries are `reverse7(X AND $7F) OR $80`.
The lower half of the nominal `$0900` base overlaps the row-high table and is
never a reflection entry for these forced-bit-7 accesses.

The two seven-entry mask arrays at `$1A34/$1A3B` preserve leading/trailing
pixels and support the composition edges. The reverse worker restores phase
and anchor; the wrappers restore source pointer. This local explanation does
not prove the complete clipped mirrored image for every argument combination.

## CPU-specific considerations

- **Registers/flags:** A is the byte; X dispatches phase and holds intermediate
  values; `$1A` is overflow. Incoming C is accounted for, outgoing flags/X are
  scratch. X/Y are restored by the enclosing draw worker, not the shifter.
- **Addressing:** source/destination use `(zp),Y`; row and reversal reads use
  absolute indexed access. Source reads can cross data pages.
- **Compatibility:** documented NMOS shifts/rotates; no 65C02-only instruction.
- **Alignment:** `$0900,X` with X≥`$80` stays in the same page, so this table
  read has no indexed-read page-crossing penalty.
- **Interrupts/code:** enclosing loops patch composition opcodes and use shared
  scratch. See [CPU6502-0001](CPU6502-0001-two-byte-render-patches.md) for the
  distinct equal-width patch mechanism and reentry risks.
- **Arithmetic:** source/coordinate ADC/SBC paths need binary decimal-mode state;
  shifts themselves are independent of D.

## Machine-specific considerations

This instance targets seven displayed pixel bits per HGR byte with bit 7 treated
separately, consistent with the [Apple II reference manual](https://www.applelogic.org/files/AIIREF.pdf).
Setting bit 7 is the captured renderer convention, not a universal rule for
all HGR palettes, colored edges or video revisions. Row lookup arrays are
page-relative; `$07` chooses `$2000` or `$4000` page base. An invalid vertical
coordinate can read non-row data: a full vertical clip was not established.

## Performance and resource costs

| Metric | Original mechanism | Alternative / evidence |
| --- | --- | --- |
| Shifter code | 103 bytes | Inclusive `$1A84–$1AEA`; includes dispatch/returns |
| Reflection data | 128 bytes | Exact forced-bit-7 domain, all entries checked |
| Boundary masks | 14 bytes | Two seven-entry arrays `$1A34–$1A41` |
| Shared row-address data | 384 bytes | 192 low + 192 high; renderer dependency, not phase variants |
| Full worker/code cost | Not isolated for comparison | Wrappers/clipping/composition included elsewhere |
| Per-phase direct output tables | Not used in this instance | 7 × 128 × 2 = 1,792 bytes for low/high pixel outputs alone |
| Pre-shifted/pre-reflected frames | Not used by this worker | Asset count, padding and format determine expansion |
| CPU time | Not measured; phase/clip/mode dependent | No benchmark or full-cycle speed comparison |

The 103/128/14-byte figures describe components, not the entire graphics engine
or a demonstrated net saving over another implementation. A table path still
needs joins, clipping and composition. Compare equivalent outputs and complete
code/data footprints before concluding which representation is smaller or faster.

## Advantages

- Shares source rows across pixel phase and facing direction.
- Small reflection table reverses exactly the displayed pixel field.
- Specialized paths exploit the bounded phase domain rather than a general shifter.

## Limitations and risks

- Repeated dispatch/shift work costs CPU time for each source byte.
- Phase/width/height assumptions are unchecked or only partially clipped.
- Byte-anchor adjustment, overflow and boundary masks are easy to generalize incorrectly.
- Bit 7/color and AND/OR layer contracts require target-specific verification.
- Shared scratch and mutable code prevent unqualified reentrant use.

## Alternatives

Use direct low/high output tables per phase, pre-shift complete frames, generate
reflected assets offline, or dispatch to a phase-specific worker once per draw.
[APPLE2-0002](APPLE2-0002-seven-phase-sprite-tables.md) is a concrete seven-phase
pointer/pair-table comparison from Lode Runner; its token and width contracts
differ, so copying its total costs directly is not a fair benchmark.

## Validation record

- **Current status:** analyzed locally; provisional.
- **Byte evidence:** header, shift/mirror workers, masks and all reversal entries.
- **Static models:** 3,584 inputs across byte/phase/carry combinations; 114,688
  two-token joins; 128 reversal values and 192 row addresses.
- **Reproducer:** `python3 research/analyses/karateka/tools/verify_analysis.py`;
  [verification results](../analyses/karateka/verification.json).
- **Expected/actual:** all modeled seven-bit splits, disjoint joins and table
  values match the stated equations. This does not execute historical instructions.
- **Benchmark / hardware:** none; no displayed frame/color confirmation.
- **Outstanding:** full pixel-reference clipping/mode/reflection tests, legal
  source/size census, patch/IRQ ordering and measured alternative renderers.

## Recommendation for new projects

Consider runtime phase/reflection work when sprite memory is scarce and draw
volume leaves sufficient CPU time. Prefer precomputed variants or output tables
when repeated alignment dominates. Define seven-bit/bit-7 and boundary contracts,
test every phase and edge, and measure complete workloads before choosing.

## References and related techniques

- [Hardware H02](../analyses/karateka/hardware-techniques.md#h02-shifted-and-mirrored-packed-rows),
  [CPU C03](../analyses/karateka/cpu-techniques.md#c03-specialized-shifts-with-masked-carry-history).
- [APPLE2-0002](APPLE2-0002-seven-phase-sprite-tables.md), table expansion alternative.
- [APPLE2-0001](APPLE2-0001-paired-hires-background-masks.md), a distinct saved-background mask contract.
- [ORIC-0003](ORIC-0003-parity-compressed-pixel-tables.md), different six-pixel representation.

