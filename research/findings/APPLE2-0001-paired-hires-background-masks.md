---
id: "APPLE2-0001"
title: "Restore and compare sprites against a paired Apple II HGR terrain page"
category: "graphics"
cpu: ["6502"]
machines: ["apple-ii-family", "apple-iie-variant-unknown"]
status: analyzed
source_analyses: ["../analyses/lode-runner/overview.md"]
tags: ["hgr", "background", "masked-restore", "overlap", "paired-pages"]
---

# Restore and compare sprites against a paired Apple II HGR terrain page


## Summary

Keep a complete terrain image in HGR page 2 while drawing actors into page 1.
The sprite mask restores old pixels from that baseline, and masked differences
between foreground and baseline detect overlap before the next OR draw.

## Problem and context

- **Problem:** remove actor pixels and detect foreground overlap while retaining terrain.
- **Use cases:** small OR-drawn sprites over a persistent tile background.
- **Preconditions:** synchronized baseline, matching byte/phase conventions, bounded coordinates and an explicitly managed actor erase/draw order.
- **Applicability:** Apple II family conventional HGR and documented NMOS 6502 implementation. Exact IIe bank/80STORE, ROM and physical CPU state remain untested.

## Provenance

| Field | Value |
| --- | --- |
| Original program | Lode Runner; supplied 1983-marked cracked Apple II disk |
| Author / publisher | Doug Smith / Brøderbund, corroborated by the publisher manual in overview; individual routine authorship and publisher-original equivalence unknown |
| Source / archive | research/sources/Apple IIe/Lode Runner/Lode Runner (1983)(broderbund)[cr].dsk; download/archive provenance unknown |
| License / usage | No license supplied; no redistribution grant established |
| Source revision | Repository baseline d02edc77fa0a02d3f679af22456ca1c762c305dc; historical image is gitignored |
| Image SHA-256 | cbc048a55c2835f1b3b54696660e8902c84c25dac44a6dc94b13a7e8f81379ec |
| File / routine / addresses | [level.asm.txt:L187–L317](../analyses/lode-runner/extracted/level.asm.txt), CPU $63B3–$64BC, first instruction DSK $013CBA; [renderer.asm.txt:L50–L58](../analyses/lode-runner/extracted/renderer.asm.txt), CPU $7A3E–$7A50, first instruction DSK $015345; [renderer.asm.txt:L282–L417](../analyses/lode-runner/extracted/renderer.asm.txt), CPU $8336–$8437, first instruction DSK $015D3D |
| First analysis | [Lode Runner overview](../analyses/lode-runner/overview.md) |

The input has no source labels or original assembler syntax. Generated listing
lines and CPU addresses are analytical evidence. DSK offsets map them to the
pinned historical input; [extraction conventions](../analyses/lode-runner/extracted/README.md)
explain modeled relocation and unknown runtime dependencies.


## Original implementation

Board preprocessing draws terrain in $4000–$5FFF, then removes actor images from
that page in play mode. Gameplay uses $2000–$3FFF as the foreground display.
This is a terrain baseline; the examined loop does not alternate displayed pages.

For each of eleven rows, $7A3E obtains matching page pointers.
The restore routine $8336 and draw routine $83A7 choose two or three screen bytes
according to horizontal phase. Analytical byte operations are:

~~~text
D = displayed foreground byte
B = terrain baseline byte
M = expanded sprite-mask byte

restore: D = (D & (M XOR $7F)) OR B
draw:    overlap = overlap OR ((D XOR B) & M)
         D = D OR M
~~~

$52 accumulates overlap across the sprite. A player caller combines it with
other state before clearing the alive flag:
[movement.asm.txt:L187–L194](../analyses/lode-runner/extracted/movement.asm.txt), CPU $6C02–$6C12, first instruction DSK $014509. Movement also consults the logical grids.

## Technical explanation

The row table provides a page-independent offset. OR $20 gives the page-1 high
byte; EOR $60 maps $20–$3F to $40–$5F, producing the page-2 pointer with the same
low byte. The paired addresses do not require a second scanline lookup.

All checked expansion bytes have bit 7 set. EOR $7F inverts their seven pixel
bits while keeping bit 7 set. The restore operation clears pixels selected by M,
then ORs the baseline back in. Unlike conventional masked selection, B is ORed
**without** an additional M mask: equivalence outside the sprite depends on the
OR-rendering invariant that baseline pixels are already present in D.

When baseline and foreground match, D XOR B is zero. Additional actor pixels
inside M create an overlap value before the new sprite is drawn. Equal bit-7
conventions keep the phase bit out of this difference; inconsistent phase bits
can produce false overlap.

Erasing M can remove another actor's pixels in their shared area. Correct final
composition and detection depend on actor order or reapplication, especially
overlaps and changing terrain. The local formulas do not prove an entire frame
or a universal collision policy.

## CPU-specific considerations

The renderer uses (zp),Y with $0C/$0D and $0E/$0F, and a 33-byte zero-page
workspace $DF–$FF. X advances three scratch bytes per row, including skipped
third bytes in the two-byte screen path. $1B/$1C/$1D track scanline, byte column
and remaining rows; $71 saves phase.

Address and mask helpers are not reentrant: they share pointers, workspace and
the operand-patching decoder. IRQ/NMI code must preserve that ownership.
Only documented NMOS instructions are observed; physical 65C02 operation has
not been tested. Cycles depend on path, indirect-read crossings, decoder setup,
mask and caller costs; no whole-sprite timing is claimed.

## Machine-specific considerations

This implementation depends on conventional Apple II HGR page addresses,
seven pixel bits per byte and paired non-linear scanline addresses. The
[hardware report](../analyses/lode-runner/hardware-techniques.md) links the Apple
primary reference and records switch/IIe limits.

Page 2 cannot simultaneously serve as an independently composed animation
frame without replacing the baseline contract. World changes such as hidden
ladders, digging and hole closure must coordinate logical state and pixel baseline.
The two logical grids need not be identical: the reviewed dig commit clears
occupancy while retaining the terrain-grid brick.

## Performance and resource costs

| Metric | Original | Alternative | Evidence |
| --- | --- | --- | --- |
| Additional full baseline | 8 KiB HGR allocation | Per-sprite saved backgrounds or scene recomposition | $4000–$5FFF ownership |
| Shared expanded workspace | 33 bytes, 11 × 3 | Pre-expanded sprites spend more asset memory | Decoder/caller operands |
| Shared scanline table | 384 bytes, 192 low/high entries | Arithmetic or another address lookup | Static table check |
| CPU cycles / display quality | Not measured | Not measured | No emulator/hardware benchmark |

The same workspace/row tables also serve other renderers; these are not costs
exclusive to restoration.

## Advantages

- A complete terrain reference is available for both restoration and difference tests.
- Matched page pointers share one scanline lookup.
- Old-position background need not be saved per moving actor.

## Limitations and risks

Two pages spend significant RAM. Baseline consistency, OR-only composition,
sprite overlap order, bounds and phase bits are part of correctness.
Masked pixel differences alone do not distinguish actor identity or terrain
changes. No flicker, gameplay collision accuracy or real-screen output was measured.

## Alternatives

Save the covered background per sprite, redraw affected tiles/actors, or
recompose a clipped scene region. Full frame buffering can simplify composition
when memory and bandwidth allow it, with a different ownership model.

## Validation record

- **Current status:** analyzed; provisional.
- **Evidence:** terrain initialization, paired pointers, restore/draw formulas and a player caller.
- **Static checks:** all 192 paired row addresses and 896 expansion pairs match the stated formula/convention; listing bytes match the pinned image.
- **Reproducer:** [verify_analysis.py](../analyses/lode-runner/tools/verify_analysis.py), [results](../analyses/lode-runner/verification.json).
- **Benchmark / real hardware:** none; no imported code execution.
- **Open:** actor order/overlap traces, every terrain update, coordinate bounds and actual IIe display/bank state.

## Recommendation for new projects

Consider a full baseline when background queries/restoration are frequent and
8 KiB is affordable. Establish composition and terrain-update invariants before
using pixel differences as overlap evidence. Use logical collision maps for
game rules and test intersecting sprites, rather than treating the byte formula
as complete collision validation.

## References and related techniques

- [APPLE2-0002](APPLE2-0002-seven-phase-sprite-tables.md), shared phase expansion.
- [GEN-0002](GEN-0002-semantic-collision-grid.md), independent logical collision representation.
- [GEN-0003](GEN-0003-clipped-scene-recomposition.md), clipped scene reconstruction.
- [ORIC-0001](ORIC-0001-background-pages-with-position-metadata.md), position-tagged per-sprite saved pages rather than a complete terrain baseline.
