---
id: "ANALYSIS-APPLE2-LODE-RUNNER-HARDWARE-TECHNIQUES"
program: "Lode Runner (local cracked disk)"
cpu: ["6502"]
machines: ["apple-ii-family", "apple-iie-variant-unknown"]
analysis_status: draft
source_revision: "d02edc77fa0a02d3f679af22456ca1c762c305dc"
analysis_date: "2026-10-10"
---

# Lode Runner: Apple II hardware techniques

## Target and reference limits

Ordinary Apple II family HGR, keyboard, game I/O, speaker and disk addresses
are present. Exact IIe/ROM/CPU revision and auxiliary-bank/80STORE state are
unknown. Apple's [Reference Manual](https://downloads.reactivemicro.com/Apple%20II%20Items/Documentation/Manuals/Apple%20II%20Reference%20Manual%20-%20The%20Red%20Book/2023-04-27%20-%20Apple%20II%20Redbook.pdf), monitor equates and printed
pp. 137–138, supports these names: $C000 keyboard, $C010 strobe, $C030 speaker,
$C050 graphics, $C052 full graphics, $C054 page 1, $C057 HGR, $C061/$C062
buttons, $C064/$C065 analog timers, $C070 trigger. Behavior below is derived
from the local binary.

## H01 — Scanline tables and paired page pointers (analyzed, machine)

[renderer.asm.txt:L44–L58](extracted/renderer.asm.txt), CPU $7A31–$7A50, first instruction at DSK $015338. $1A85/$1B45 contain 192 low/high entries. Checked offset:

~~~text
offset(y) = (y & 7) × $0400
          + ((y >> 3) & 7) × $0080
          + (y >> 6) × $0028
~~~

$7A31 ORs page selector $1F into the high byte. $7A3E creates page 1 with OR
$20 and page 2 with EOR $60; XOR $20 would not transform $20 into $40.
Tables cost 384 bytes; y must be $00–$BF. All pairs match the formula.

Coordinate tables yield 10 pixels per board column and 11 scanlines per row:
28 × 16 cells cover 280 × 176 pixels. Subcell x uses two-pixel units, with
floor(2x/7) and 2x mod 7 tables. Complete animation tracing remains open.

## H02 — Baseline, masked restoration and overlap (analyzed, APPLE2-0001)

[level.asm.txt:L187–L317](extracted/level.asm.txt), CPU $63B3–$64BC, first instruction at DSK $013CBA establishes page 2 without actor images in play mode.
[renderer.asm.txt:L282–L341](extracted/renderer.asm.txt), CPU $8336–$83A6, first instruction at DSK $015D3D restores old pixels using a three-byte-row mask.
[renderer.asm.txt:L342–L417](extracted/renderer.asm.txt), CPU $83A7–$8437, first instruction at DSK $015DAE accumulates overlap before drawing. With D foreground,
B baseline and M sprite:

~~~text
restore: D' = (D & (M XOR $7F)) OR B
draw:    overlap |= (D XOR B) & M
         D' = D OR M
~~~

The checked dictionary sets bit 7 in every byte; XOR $7F inverts pixel bits
while retaining that phase-bit convention. Player callers combine $52 with
state and may mark death: [movement.asm.txt:L187–L194](extracted/movement.asm.txt), CPU $6C02–$6C12, first instruction at DSK $014509. Movement also queries logical grids.

A persistent baseline costs a second 8 KiB page and needs terrain updates.
It is not per-sprite saved background. ORing B unmasked assumes baseline
pixels are already present in D outside M. Difference under a mask is not a universal
collision rule: actor ordering, overlap and stale baseline matter. No frame rate,
flicker or actual display was measured.

## H03 — Seven-phase row expansion (analyzed, APPLE2-0002)

[renderer.asm.txt:L418–L480](extracted/renderer.asm.txt), CPU $8438–$84C0, first instruction at DSK $015E3F selects pointer pages $A2–$A8. Each has 128 low/128 high
entries addressing 512 shared pairs at $A900–$ACFF. For 7-bit token t, phase p:

~~~text
pair.low  = $80 OR ((t << p) & $7F)
pair.high = $80 OR ((t << p) >> 7)
~~~

All 896 selections match and avoid pair page crossing. Two row tokens merge
into three bytes. Phase 5 separates two-byte from three-byte screen operations.
The decoder avoids per-row shifting at the cost of tables and mutable code.

This is not net dictionary compression: a pointer is as large as an output
pair, so adding the dictionary costs more than direct two-byte output tables.
Two apparent IDs $66/$67 have last-row tokens outside the checked domain;
their live use remains unknown. The fiche defines the narrow preconditions.

## H04 — Keyboard and analog polling (analyzed fragment, machine)

[input-audio.asm.txt:L1–L35](extracted/input-audio.asm.txt), CPU $6A12–$6A55, first instruction at DSK $014319 reads/clears keyboard and dispatches control keys.
[input-audio.asm.txt:L273–L291](extracted/input-audio.asm.txt), CPU $8746–$876C, first instruction at DSK $01614D triggers timers and counts negative samples separately
in $65/$66 until expiration or a counter-sign limit.
[input-audio.asm.txt:L292–L313](extracted/input-audio.asm.txt), CPU $876D–$8797, first instruction at DSK $016174 checks central range $12 ≤ value < $3B and buttons.

Axis inversion swaps threshold bytes: [input-audio.asm.txt:L70–L79](extracted/input-audio.asm.txt), CPU $6A9E–$6AB9, first instruction at DSK $0143A5.
Thresholds/calibration depend on actual loop timing. Startup detection has a
timeout but inherits Y. Counts are loop units, not guaranteed microseconds.

## H05 — Speaker service also delays gameplay (analyzed fragment, machine)

[input-audio.asm.txt:L333–L346](extracted/input-audio.asm.txt), CPU $87BA–$87D4, first instruction at DSK $0161C1 reads $C030 only if $99 permits sound, then runs counters.
Muting retains the loop but skips a local four-cycle absolute read.
$8811 pops events from parallel arrays and applies speed-dependent delays;
the main loop calls it repeatedly.

Audio, polling and pace are coupled. No IRQ audio driver was established here.
Accelerators or loop changes alter pitch/duration/pace. No elapsed timing,
frequency or hardware benchmark is claimed.

## H06 — RWTS and edition differences (observed/analyzed interface)

[level.asm.txt:L147–L163](extracted/level.asm.txt), CPU $6359–$6381, first instruction at DSK $013C60 selects logical track $0C/sector $0F into $1F00.
[level.asm.txt:L163–L180](extracted/level.asm.txt), CPU $6381–$63A4, first instruction at DSK $013C88 checks an 11-byte high-bit ASCII signature and a final flag.
JMP ($0036) reaches $8E50 → $B7B5 → $BD00 in the reconstructed state.

Level reads instead use $0023 → $1700, unexplained after relocation.
The legacy $0609 reader polls $C08C,X and decodes paired bytes, but its live
use in this converted edition is unproved. Original protection is not inferred.

Editor write/format paths were not executed or exhausted. A sector image cannot
preserve original magnetic bit timing or validate nibble protection behavior.

## Next hardware investigation

Trace read-only cold boot and writes to $0023–$0025, $0036/$0037 and $1700
around metadata/first-level I/O. Record CPU/ROM/switch state, compare a trusted
edition, then investigate level 136 and measure sprites.
