---
id: "ANALYSIS-APPLE2-KARATEKA"
program: "Karateka (supplied 1984 Broderbund disk image)"
cpu: ["6502"]
machines: ["apple-iie"]
analysis_status: complete
source_revision: "d02edc77fa0a02d3f679af22456ca1c762c305dc"
analysis_date: "2026-10-11"
---

# Source analysis: Karateka

## 1. Objective and scope

Reconstruct the initial loading path and examine animation, rendering, state,
memory use, input and sound in the supplied Apple II disk. **The input is a
binary disk image, not historical assembly source.** All routine names below
are descriptive analyst names; original labels and assembler syntax are unknown.

Full-mode reports cover the architecture and major modules, with detailed
analysis of the sprite renderer and actor work records. This is a completed
static investigation within that scope, not an exhaustive disassembly or a
runtime verification of the entire game. Later scene loads, complete opponent
decisions, combat rules, all assets and disk protection remain partially mapped.

## 2. Source provenance

| Field | Value |
| --- | --- |
| Program / version | Filename identifies Karateka, 1984, Broderbund; exact disk edition unknown |
| Author / publisher | Jordan Mechner / Broderbund; [author's account](https://www.jordanmechner.com/en/games-movies/karateka/) supports identity and Apple II origin |
| Local input | [Karateka (1984)(Broderbund).dsk](<../../sources/Apple IIe/Karateka/Karateka (1984)(Broderbund).dsk>) |
| Inventory | One `.dsk`, 143,360 bytes; no assembly, includes, build scripts, README or license |
| Archive / importer / original media | Unknown |
| Distribution terms | Unknown; no license grant inferred from repository presence |
| SHA-256 | `4399db1c5469299f6a519abd890456ba1bbba70596d72096f1db4a84e5669370` |
| Repository baseline | `d02edc77fa0a02d3f679af22456ca1c762c305dc`; input has no tracked working-tree changes |
| Language / dialect | Documented NMOS 6502 instructions in inspected code; original assembler/toolchain unknown |

The file has 35 tracks, 16 sector slots per track and 256 bytes per slot. A
DOS-style loader is present, but a usable DOS catalog is not: the nominal
track `$11`, sector `$00` VTOC region contains filler. Extraction follows the
loader rather than treating the disk as a filesystem. The DOS logical-sector
slot interpretation is inferred from internally consistent code and data,
not authenticated media metadata. Whether this loader is an original release
loader, a conversion or a later modification is unresolved.

## 3. Target environment

- **CPU:** inspected routines use the original NMOS 6502 instruction set. The
  folder identifies Apple IIe, but exact motherboard, CPU and ROM revision are
  not encoded in trustworthy provenance. Enhanced 65C02 compatibility is untested.
- **RAM:** reconstructed code and data use main RAM through `$BFFF`, including
  both HGR pages. The inspected core fits the 48 KiB main-memory address range;
  this is not a proof of the whole game's minimum configuration.
- **Video:** ordinary seven-pixel-byte HGR, drawing into `$2000–$3FFF` and
  `$4000–$5FFF`; no demonstrated auxiliary-memory or double-HGR renderer.
- **ROM / devices:** monitor calls, keyboard, buttons/paddles, speaker, Disk II
  boot/read machinery. The later disk path copies slot-6 ROM from `$C600`.
- **IIe-specific path:** `$FBB3 == $06` enables a `$C019` polling wait. This is
  the actual code condition, not a universal machine-identification guarantee.
- **Verification environment:** Python 3.13 static extraction and translated
  arithmetic models; no CPU emulator, real machine or historical binary execution.
- **Assumptions:** ordinary main-RAM video banking, usable monitor/Disk II ROM,
  binary arithmetic for coordinate ADC/SBC and exclusive ownership of scratch
  memory and patch sites. Reset/ROM state has not been traced end to end.

## 4. Program architecture

The boot sector invokes disk firmware, loads DOS-style code and transfers to
`$B715`. That initial loader reads 160 sectors into `$0800–$A7FF`, then jumps
to `$2100`. Startup copies `$2800–$3FFF` to `$A800–$BFFF` and `$2000–$27FF`
to `$0000–$07FF`, clears the two video pages and enters relocated title code
at `$B77C`. `$B400` initializes gameplay and repeatedly updates actors, repairs
and draws scene regions, flips the page and handles audio/input.

The core uses two 16-byte actor records and a common 16-byte work window,
retained animation cursors, table-selected sprite layers, self-modifying
composition loops and foreground sound. No custom IRQ/NMI handler has been
established in the reviewed paths. Boot-time interrupt masking does not prove
runtime exclusion of interrupts.

See [architecture](architecture.md) for phase-specific allocations and loading
relationships, and [routine inventory](routines.md) for inputs, effects and
confidence. CPU addresses reused by different phases must not be conflated.

## 5. Analysis findings

| Finding | Result | Status / detail |
| --- | --- | --- |
| K01: common actor work window | Load a record into fixed addresses, process it with shared routines, commit it | analyzed; new [GEN-0006](../../findings/GEN-0006-fixed-actor-work-window.md) |
| K02: runtime seven-bit shifts and reflection | Shift packed sprite bytes, join fragments and reflect via a 128-byte table | analyzed locally; new [APPLE2-0003](../../findings/APPLE2-0003-runtime-sprite-shift-and-reflection.md) |
| K03: equal-width operation patches | NOP/NOP, ORA and AND alternatives at two renderer sites | analyzed; confirms [CPU6502-0001](../../findings/CPU6502-0001-two-byte-render-patches.md) |
| K04: retained animation cursors | Separate horizontal/vertical token streams update fixed actor fields | analyzed for inspected dispatch; related [GEN-0001](../../findings/GEN-0001-resumable-animation-streams.md) |
| K05: repair and redraw of scene regions | Clear old actor spans and redraw layers; retain older geometry across page flips | analyzed locally; related [GEN-0003](../../findings/GEN-0003-clipped-scene-recomposition.md) |
| K06: page reuse and transitions | Relocate loader data, flip pages, copy two-row-shifted or column-wise images | analyzed for inspected loops; hardware report |
| K07: foreground speaker synthesis | Busy loops produce speaker transitions; stream commands patch timing code | analyzed locally; timing and audible result untested |
| K08: later disk/scene path | Slot ROM copying, zero-page exchange and raw disk reads | observed; exact protection/overlay protocol unresolved |

All locations, applicability levels and trade-offs are indexed in
[findings](findings.md). These are discoveries in this repository, not claims
that the algorithms were historically invented here or are always optimal.

## 6. Performance and verification

Run from the repository root:

~~~sh
python3 research/analyses/karateka/tools/inspect_disk.py --extract
python3 research/analyses/karateka/tools/verify_analysis.py
~~~

[Verification record](verification.json) reports five extracted hashes,
160 sector mappings, two relocation copies, four state-copy loops, 192 row
addresses, 128 reflection values, 3,584 shifter cases, 114,688 fragment joins
and 2,812 listed byte records checked. Translated models validate local
algebra; they do not execute the program or prove clipping/composition correct.

The 16-byte copy core takes **241 cycles by instruction-table calculation**,
247 including RTS, 253 including the caller's JSR, under the stated same-page
branch/no-interrupt conditions. Load helpers have extra classification/distance
work. No frame rate, audio frequency, whole-routine speedup or benchmark result
is reported. See [CPU analysis](cpu-techniques.md).

## 7. Comparison with the knowledge base

Searched existing `docs/` and `research/findings/` for record copying, context
windows, stream animation, patches, clipping and seven-phase HGR rendering.
Existing L'Aigle d'Or, Space: 1999 and Lode Runner records were retained.
K03–K05 receive cross-links rather than duplicate fiches. K02 differs from
Lode Runner's [APPLE2-0002](../../findings/APPLE2-0002-seven-phase-sprite-tables.md):
Karateka uses accumulator paths rather than that program's seven phase tables.
No guideline under `docs/` was changed or automatically promoted.

## 8. Documentation changes

Created this report plus [architecture](architecture.md), [routines](routines.md),
[CPU techniques](cpu-techniques.md), [hardware techniques](hardware-techniques.md)
and [findings](findings.md); added two provisional fiches under
`research/findings/`. [Derived-artifact notes](extracted/README.md), binaries,
manifest, selected listing, tables, two inspection tools and `verification.json`
make the evidence reproducible. Historical source files remain unchanged.

## 9. Open questions and next tests

- [ ] Trace a bounded boot/title/gameplay session with a specified Apple IIe ROM,
  log the relocation, `$07` changes, actor commits and both patch sites.
- [ ] Test all phase/edge/mode combinations against a pixel reference renderer,
  including zero sizes, offscreen rows and overlapping AND/OR sprite layers.
- [ ] Resolve later disk transfers and protection provenance before treating
  the initial memory map as valid for every scene.
- [ ] Measure stack high-water use, decimal flag state and interrupt behavior.
- [ ] Compare calculated shifts, small lookup tables and pre-shifted frames for
  representative sprite sizes, with identical clipping and composition.
- [ ] Complete combat/AI, all sequence tokens and foreground audio timing.

## 10. Summary

The strongest reusable results are a fixed actor work window and a compact
seven-bit shift/reflection renderer. Equal-width patches, animation streams
and scene recomposition provide additional evidence for existing findings.
Writable code, reserved zero page, unchecked dimensions and ROM assumptions
are material constraints. The best next investigation is a bounded emulator
trace of startup and one gameplay exchange, followed by renderer edge tests.

## References

- [Original disk](<../../sources/Apple IIe/Karateka/Karateka (1984)(Broderbund).dsk>),
  cited throughout by zero-based `DSK` byte offset and phase-specific CPU address.
- [Jordan Mechner: Karateka](https://www.jordanmechner.com/en/games-movies/karateka/),
  identity, author, Apple II origin and Broderbund; consulted 2026-10-11.
- [Apple II Reference Manual, Red Book](https://downloads.reactivemicro.com/Apple%20II%20Items/Documentation/Manuals/Apple%20II%20Reference%20Manual%20-%20The%20Red%20Book/2023-04-27%20-%20Apple%20II%20Redbook.pdf),
  monitor listing and I/O equates, printed pp. 137–138.
- [Apple IIe Technical Reference Manual, chapter 7, printed p. 157](https://www.applelogic.org/files/AIIETECHREF3.pdf),
  `$C019` low-bit-7 interval; searchable excerpt consulted, full fetch timed out.
- [MOS Technology instruction summary](https://ftpmirror.your.org/pub/misc/bitsavers/components/mosTechnology/6502_Instruction_Set_Summary.pdf),
  documented opcodes and conditional timing.

