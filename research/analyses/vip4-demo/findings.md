---
id: ANALYSIS-ORIC-0002-FINDINGS
program: "Vip4 Demo / Quintessential"
cpu: ["6502"]
machines: ["oric-unspecified", "microdisc"]
analysis_status: draft
source_revision: "sha256:555e811187069b29bfc6cf657be7f19f8c49aa8d25fbbeeb8ab4718ad2577558"
analysis_date: "2026-10-09"
---

# Finding index

## 5. Evidence and classifications

All locations refer to `research/sources/Oric/Vip4 Demo/vip4.dsk` using the
[binary reference convention](overview.md#references-and-precise-location-convention).
[routines.md](routines.md) and selected listings give exact disk offsets.
`Confirmed by source` means confirmed by bytes; no original symbols or runtime
observations are implied. `Analyzed` describes explained operations and their
constraints, not validated recommendations or proven whole-program behavior.

| Candidate / ID | Level | Original locations | Evidence / status | Trade-off / comparison | Next validation |
| --- | --- | --- | --- | --- | --- |
| [CPU6502-0005](../../findings/CPU6502-0005-zero-page-code-operands-as-state.md) | cpu | M02 `$9D4A–$9DD5`, relocated `$00–$4E`; M13 `$609B–$60CA`, relocated `$10–$3F` | Confirmed by source; analyzed | Fast ZP writes, no separate pointer/saved-A storage; writable code and exclusive ZP required | Trace operand writes, samples, A/X/Y and IRQ boundaries |
| [CPU6502-0006](../../findings/CPU6502-0006-irq-frame-discard-and-rts.md) | cpu | Boot `$A869–$A876`; R `$FA7F–$FA8D`; vector setup `$FAA5–$FAAC` | Confirmed configured handlers; analyzed CPU semantics; live activation unknown | Nonlocal return through nearest JSR; loses P and interrupted work; I masks this path | Controlled IRQ injection with known stack and controller state |
| [ORIC-0002](../../findings/ORIC-0002-masked-charset-bank-animation.md) | machine | M13 `$60DE–$6112`, `$6127–$61C7` | Confirmed by source; analyzed byte composition | 256 glyph stores update fixed character codes; shared glyph effects and bank/ZP ownership risks | Render exact charset/text with traced `$02`, bank and mask state |
| V04: Sector descriptors and slot overlays | common + machine | R `$F800–$F987`, `$FA9F–$FAF6`, arrays `$FC19–$FC89` | Confirmed by source; analyzed | Small name-free loading table and reused RAM; hard-coded disk layout and lifetimes | Trace load order and checksums of loaded regions |
| V05: Patched absolute row addressing | cpu | M01 `$1000–$1030`; M06 `$114C–$117C`; R `$FA73/$FAF7` | Confirmed by source; analyzed | Related to existing self-modification, including CPU6502-0001; no duplicate generic fiche | Compare indirect addressing with equal outputs, reset contracts and setup costs |
| V06: Parallel lookup arrays and phase carry | cpu + common | R descriptors; M0B `$883B–$8971` | Confirmed by source; analyzed selected operations | Split table bytes avoid record multiplication; carry/fraction contracts and table footprint | Recover tables, phase range and full effect call sequence |
| V07: Full-page countdown with overlapping tail fill | cpu | R `$FB08–$FB86` | Confirmed by source; analyzed | CPU6502-0004 counter idiom; duplicated stores avoid a tail loop but spend cycles | Compare exact-tail clear with the same byte union |
| V08: Sparse scanline rendering and dancer overwrite | machine | M0B `$883B–$88A1`, `$89D9–$8A18` | Confirmed strides; analyzed transfers; visual explanation is likely inference | Fewer row transfers; display attributes, missing rows and background restore constraints | Frame capture and real-hardware appearance |
| V09: Two packed-volume IRQ players | machine + cpu | M02 `$9D0D–$9DD5`; M13 `$609B–$60CA`, `$61C8–$6238` | Confirmed by source; analyzed nibble/state flow | Half-byte packing; AY nonlinear amplitude and timer/control ownership; linked CPU6502-0005 | Trace AY writes and time; decode actual audio |
| V10: Music IRQ trampoline / score engine | machine | R `$F9C6–$FA12`; M00 `$C000–$C0BC` | Confirmed interface; analyzed; complete score decode partial | Shared sound engine survives lower overlays; state and ZP reservations matter | Reconstruct score/effect interpreter and measure IRQ budget |

V04–V10 stay in these reports: familiar patterns, composite candidates or
insufficiently distinct/complete variants do not justify additional fiches.
CPU namespace IDs 0003/0004 already exist in `docs/`; the new IDs start at 0005.
ORIC-0001 already covers per-object saved backgrounds and is not duplicated.

## Risks and unresolved observations

| Observation | Precise evidence | Interpretation boundary |
| --- | --- | --- |
| Metadata describes a different program | `research/sources/Oric/Vip4 Demo/metadata.md:L1-L3` | Left unchanged; identity/date/platform use separate evidence |
| Descriptor `$0C` leaves available tracks | Arrays at R `$FC25/$FC3C/$FC53/$FC6A/$FC80`; loader rollover `$FA13–$FA39` | Only five pages recovered; absent main call; do not splice side 1 into it |
| Disk escape masked | R `$FA9F` SEI, no CLI before `$FAF6` RTS | Configured code does not prove live IRQ handling |
| Resident attempt count unused | R `$FA8E–$FA9E` | No demonstrated retry/status branch |
| Silence vector appears byte-swapped | R `$F98D–$F994`; RTI at `$FC8A` | Installs `$8AFC`; target and two-store transition dangerous if IRQ enabled; runtime consequence unknown |
| Odd decrement-by-two loop | M01 `$1038–$103C` | Cannot terminate; no call from the reviewed picture entry |
| Image reveal overlaps row boundary | M0D `$1026–$102F` | Copies 41 bytes at stride 40; first pass reaches `$BF40`; intention unresolved |
| Final bank pointer low not initialized | M13 `$60CB–$60DE`, `$6197–$61C7` | Aligned bank interpretation requires `$02=0` from prior state |
| Carry and decimal mode inherited | R `$FBDA`; M13 `$60F3`; no CLD in inspected entries | Model arithmetic is binary; inherited flags require execution proof |

## 6. Verification and benchmark proposals

All CRC checks, mapped-byte assertions and small arithmetic models passed as
recorded in [verification.json](verification.json). None constitutes a CPU
emulator test, a rendered frame, an audible result or a benchmark. No status
is `benchmarked` or `validated`.

Proposed comparisons: row-address patches versus private indirect pointers;
32-store overlap clear versus 31 pages plus tail; opcode operands versus
separate IRQ state. Before measuring speed, establish correct sector loads,
IRQ-vector transitions and byte-for-byte image/audio output on a known ROM.

## 7–10. Documentation and next investigation

Created the six reports, three new fiches and the extraction/verification
artifacts linked from [overview.md](overview.md). Sources, prior findings and
validated guidelines were not edited. The next investigation should trace the
actual disk, with particular attention to the `$8AFC` vector, `$0C` dormancy,
Timer 1 startup, executable zero page and ending bank state.
