---
id: "APPLE2-0002"
title: "Expand seven-bit sprite tokens through seven phase tables and shared pixel pairs"
category: "graphics"
cpu: ["6502"]
machines: ["apple-ii-family", "apple-iie-variant-unknown"]
status: analyzed
source_analyses: ["../analyses/lode-runner/overview.md"]
tags: ["hgr", "alignment", "lookup-tables", "self-modifying-code", "sprite-tokens"]
---

# Expand seven-bit sprite tokens through seven phase tables and shared pixel pairs


## Summary

Precompute the two-byte expansion of a seven-bit row token for each of seven
pixel phases, and select the pair through split pointer tables. Lode Runner
combines two such expansions into a three-byte row workspace, replacing runtime
bit shifting with table reads and patched absolute loads.

## Problem and context

- **Problem:** align sprite rows with seven-pixel HGR byte boundaries.
- **Use cases:** small repeated row patterns and frequent phase-dependent drawing.
- **Preconditions:** phase 0..6, token 0..127, valid pair pointers, writable exclusively owned decoder code/workspace and binary arithmetic mode.
- **Applicability:** Apple II family HGR representation; the pointer-patching implementation uses documented NMOS 6502 instructions. Physical CPU/IIe revision remains unknown.

## Provenance

| Field | Value |
| --- | --- |
| Original program | Lode Runner; supplied 1983-marked cracked Apple II disk |
| Author / publisher | Doug Smith / Brøderbund, corroborated by the publisher manual in overview; individual routine authorship and publisher-original equivalence unknown |
| Source / archive | research/sources/Apple IIe/Lode Runner/Lode Runner (1983)(broderbund)[cr].dsk; download/archive provenance unknown |
| License / usage | No license supplied; no redistribution grant established |
| Source revision | Repository baseline d02edc77fa0a02d3f679af22456ca1c762c305dc; historical image is gitignored |
| Image SHA-256 | cbc048a55c2835f1b3b54696660e8902c84c25dac44a6dc94b13a7e8f81379ec |
| File / routine / addresses | [renderer.asm.txt:L418–L480](../analyses/lode-runner/extracted/renderer.asm.txt), CPU $8438–$84C0, first instruction DSK $015E3F; [tables.hex.txt:L70–L181](../analyses/lode-runner/extracted/tables.hex.txt), CPU $A200–$A8FF, first byte DSK $00DA07 |
| First analysis | [Lode Runner overview](../analyses/lode-runner/overview.md) |

The input has no source labels or original assembler syntax. Generated listing
lines and CPU addresses are analytical evidence. DSK offsets map them to the
pinned historical input; [extraction conventions](../analyses/lode-runner/extracted/README.md)
explain modeled relocation and unknown runtime dependencies.


## Original implementation

Original assembler dialect is unknown. $84C1 selects high bytes $A2–$A8, patched
into four absolute indexed table reads. Each table page contains 128 low-pointer
bytes at offset $00 and 128 high-pointer bytes at $80.

A token indexes a pointer to a shared two-byte pair at $A900–$ACFF. The decoder
patches two absolute LDA operands to that pair and pair+1. It repeats for the
second row token, ORs its first byte with the previous pair's second byte, and
stores its second byte in the third workspace position.

The token bank starts at $AD00 and uses a $68-byte slice stride. Each row consumes
two slices; eleven rows consume 22 slices. Within a slice, $1E selects a sprite
ID. X advances by three through $DF–$FF. These are reconstructed layouts,
not recovered original symbols.

## Technical explanation

For token t in 0..127 and phase p in 0..6, every checked pointer selects:

~~~text
low  = $80 OR ((t << p) & $7F)
high = $80 OR ((t << p) >> 7)
~~~

The seven tables make 896 selections covering 512 distinct output pairs.
Two tokens t0/t1 produce byte rows equivalent to adjoining their seven-bit
patterns, shifted by p:

~~~text
row[0] = pair(t0,p).low
row[1] = pair(t0,p).high OR pair(t1,p).low
row[2] = pair(t1,p).high
~~~

All pointer starts are even and their low byte is not $FF. Incrementing only the
patched low operand by one is therefore safe for this dictionary. It is not a
general 16-bit pointer increment.

The renderer chooses two screen bytes for phases 0..4 and three for 5..6, although
the decoder always produces three workspace bytes. The coordinate grid advances
ten pixels per cell. Arbitrary two-token patterns can contain more than ten
significant pixels; the full used-sprite data/width contract is not yet proven.
Do not generalize the two-byte screen path to arbitrary 14-bit patterns.

## CPU-specific considerations

A phase patches high operand bytes; each token patches pair operands low/high.
Code must reside in writable RAM, and interruption/reentry cannot expose
partially updated operands or scratch. Shared pointers are $0A/$0B; counters
include $1D/$1E and X; A/Y/flags are scratch.

The pointer increments and low-byte +1 use ADC, so D must be clear. Indirect
token reads can cross a page. Table indexed reads remain within their half-page
for the checked 7-bit token domain; an out-of-range token violates that contract.

Only documented NMOS instructions are used. Absolute reads avoid indirect Y
addressing during pair fetch, but patch setup is work too. See the
[CPU report](../analyses/lode-runner/cpu-techniques.md) for conditional instruction
costs; no complete cycle improvement is measured.

## Machine-specific considerations

Seven phases correspond to the checked HGR pixel-byte packing. Bit 7 follows the
captured expansion convention and is preserved/set by composition; the exact
display-color result was not rendered or measured. Porting to another pixel-byte
width requires new tables and mask contracts.

An apparent 104-ID rectangular token census has two exceptions: slice 21,
IDs $66/$67, addresses $B5EE/$B5EF, values $81/$A8, original DSK offsets
$012DF5/$012DF6. Their live use as sprite tokens is unknown; they may lie outside
the actual used-ID set or overlap other captured state. No corruption or repair
is asserted.

## Performance and resource costs

| Metric | Original | Direct output tables | Evidence |
| --- | --- | --- | --- |
| Phase pointer tables | 7 × 256 = 1,792 bytes | 7 × 128 × 2 = 1,792 bytes total output data | Exact bounded table domain |
| Shared pair dictionary | 512 × 2 = 1,024 bytes additional | None required for those same pair outputs | 512 unique checked pointers |
| Token bank rectangular extent | 22 × 104 = 2,288 bytes, two domain exceptions | Can remain shared | Static slice census, not proof of used IDs |
| Workspace | 33 bytes | Depends on new decoder | Actual operands |
| CPU cycles / code size comparison | Not measured | Not implemented/measured | No benchmark |

Pointer tables plus dictionary total 2,816 bytes. The same checked outputs could
occupy 1,792 direct-table bytes, a **1,024-byte data-saving hypothesis** excluding
decoder changes. Dictionary sharing here is not net compression because each
pointer already costs as much as a two-byte result.

## Advantages

- Every supported phase/pattern result is explicit and reproducible.
- Runtime row shifting is replaced by lookups.
- Tokenized source rows remain shared across horizontal phases.

## Limitations and risks

The captured tables spend more data bytes than direct output tables.
Mutable code limits reentrancy and ROM placement. Phase/token/ID bounds and
screen-width assumptions need enforcement. Bit-7 conventions are tied to
the renderer and baseline, not a universal HGR color algorithm.

## Alternatives

Use two direct output-byte tables per phase, pre-shift whole sprite frames, or
shift rows at runtime. An indirect pointer decoder removes operand mutation
but changes setup, registers and per-read costs. Compare full code/data/cycles
under actual sprite IDs and target display conditions.

## Validation record

- **Current status:** analyzed; provisional.
- **Evidence:** linked decoder, pointer/pair/token tables and its callers.
- **Static checks:** 896 full-byte outputs, 512 distinct valid pair pointers, no pair beginning at low byte $FF, 2,288 interpreted token entries and two explicit exceptions.
- **Reproducer:** [verify_analysis.py](../analyses/lode-runner/tools/verify_analysis.py), [results](../analyses/lode-runner/verification.json).
- **Benchmark / real hardware:** none; the decoder was not executed.
- **Open:** used-ID census, ten-pixel width contract, complete cycles, D-state and IRQ ownership, direct-table experiment and displayed phase/color behavior.

## Recommendation for new projects

Consider precomputed phase outputs when alignment work dominates rendering.
Compare direct tables before adding a pair dictionary; count the pointer storage.
Bound every phase/token/ID and keep code/scratch exclusively owned. Choose
runtime shifts when asset memory is more important than repeated decode work.

## References and related techniques

- Dictionary data: [tables.hex.txt:L183–L246](../analyses/lode-runner/extracted/tables.hex.txt), CPU $A900–$ACFF, first byte DSK $012107.
- Token data: [tables.hex.txt:L248–L390](../analyses/lode-runner/extracted/tables.hex.txt), CPU $AD00–$B5EF, first byte DSK $012507.
- [APPLE2-0001](APPLE2-0001-paired-hires-background-masks.md), consumer mask/baseline contract.
- [ORIC-0003](ORIC-0003-parity-compressed-pixel-tables.md), six-bit parity-compressed tables with different encoding.
- [CPU6502-0001](CPU6502-0001-two-byte-render-patches.md), instruction-choice patch rather than dictionary pointer operands.
