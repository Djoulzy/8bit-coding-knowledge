---
id: ANALYSIS-ORIC-0002
program: "Vip4 Demo / Quintessential"
cpu: ["6502"]
machines: ["oric-unspecified", "microdisc"]
analysis_status: draft
source_revision: "sha256:555e811187069b29bfc6cf657be7f19f8c49aa8d25fbbeeb8ab4718ad2577558"
analysis_date: "2026-10-09"
---

# Source-code analysis: Vip4 Demo

## 1. Objective and scope

Analyze the supplied disk image without running it. There is **no historical
assembly or C source** in the input directory, including ignored files. This
is static binary analysis with reconstructed NMOS 6502 syntax. Historical
symbols, compiler, assembler dialect and build options are unknown.

The image is consistent with Quintessential, the Defence Force VIP4 demo:
the binary contains VIP4 end text and the participants' account describes
the same combination of samples, music, images and dancers. Exact equivalence
to a published release has not been established by comparing checksums.
The group's [historical index](https://www.defence-force.org/computing/oric/dbug/index.htm)
dates its VIP4 demo to 2002. [Romu's participant account](https://romualdl.oric.org/vip4/vip4.html)
identifies Quintessential and its contributors: Dbug, Jede, Twilighte, Exocet,
Mooze, Romu and Spider. Routine-level attribution remains unknown.

Coverage: all disk sector envelopes and CRCs; all resident loader instructions
and descriptors; initialization and IRQ interface of the music block; sample
relocation and both sample interrupt implementations; image blitters; selected
interference/dancer workers; final charset compositor. Large compiler-style
modules are only partly mapped. Their full algorithms, graphics, music score
and all runtime paths are not decoded. No emulation, hardware measurement,
historical build script or imported executable was run.

## 2. Source provenance

| Field | Value |
| --- | --- |
| Input | [vip4.dsk](<../../sources/Oric/Vip4 Demo/vip4.dsk>), 537,856 bytes |
| Container | `MFM_DISK`, two sides, 42 tracks per side, geometry 1 |
| Original archive / importer / exact version | Unknown |
| Author / publisher | Defence Force attribution from the external participant account; no routine ownership established |
| License | Unknown; no redistribution license supplied |
| Local metadata | [metadata.md](<../../sources/Oric/Vip4 Demo/metadata.md>), lines 1–3 |
| Metadata conflict | Says Oric 1, cassette and links L'Aigle d'Or; unsuitable evidence for this image's identity and medium |
| Image SHA-256 | `555e811187069b29bfc6cf657be7f19f8c49aa8d25fbbeeb8ab4718ad2577558` |
| Git baseline | `a04d227fbbc9252d9dda01641581f4f0dc49a8e3` |
| Working tree at start | Clean; source directory ignored by `.gitignore`, with no tracked source revision |
| Language / toolchain | Machine code and data; compiler-style software frames in several blocks are an inference, not a compiler identification |

Sources and validated guidelines were left unchanged. Root policy,
[6502 policy](../../../docs/cpu/6502/AGENTS.md) and the actual
[Oric policy location](../../../docs/machines/Tangerine/Oric/AGENTS.md)
were read. The dossier distributes the sections of
[analysis.md](../../../templates/analysis.md) across six reports; provisional
fiches follow [technique.md](../../../templates/technique.md).

## 3. Target environment

- **CPU:** documented NMOS 6502 instructions in the examined executable spans.
  No claim that every data byte is an instruction or that all code was inspected.
- **Machine:** Oric with Microdisc-compatible register decoding and writable
  upper RAM. Exact Oric-1/Atmos model and ROM revision are unknown.
- **Memory:** application code at `$F800`, music at `$C000`, large asset bank at
  `$D000`, writable `$FFFE/$FFFF`, and overlapping effect load slots.
- **Display:** HIRES and TEXT/charset memory; serial attributes must be retained.
- **Audio:** AY register writes through VIA; Timer 1 IRQs and software delays.
- **Storage:** direct sector reads; Sedoric strings and a synthetic directory
  coexist with the custom loader and do not prove that Sedoric runs the effects.
- **Compatibility:** the participant account advertises several Oric variants,
  but this image's compatibility has not been exercised. It also reports an
  Atmos-ROM dependency for the ending; the examined ending contains a local
  IRQ player. The precise relationship between versions remains unresolved.

## 4. Program architecture

See [architecture.md](architecture.md) for the stage sequence, descriptor table,
memory lifetimes and dependency boundaries, and [routines.md](routines.md) for
the indexed routine map. The main sequence is linear orchestration in resident
code, not an inferred universal effect engine or a continuous disk stream.

## 5. Analysis findings

Three distinct provisional fiches were added:

- [CPU6502-0005](../../findings/CPU6502-0005-zero-page-code-operands-as-state.md):
  executing code in zero page so instruction operands also serve as pointer,
  saved-accumulator and phase state.
- [CPU6502-0006](../../findings/CPU6502-0006-irq-frame-discard-and-rts.md):
  discarding the hardware IRQ frame and returning with RTS to a subroutine's
  caller. The handler is configured but remains masked on the traced load path.
- [ORIC-0002](../../findings/ORIC-0002-masked-charset-bank-animation.md):
  composing changing character glyphs from a bank and masks while retaining
  the text screen. Bank initialization and visual intent are unresolved.

Further candidates, related established techniques, limitations and potential
optimizations are indexed in [findings.md](findings.md). CPU and hardware details
are in [cpu-techniques.md](cpu-techniques.md) and
[hardware-techniques.md](hardware-techniques.md). No guideline promotion occurred.

## 6. Performance and verification

`python3 research/analyses/vip4-demo/tools/inspect_disk.py --extract`
regenerates derived files only. All 1,428 sector ID CRCs and all 1,428 data CRCs
match. All sectors are 256 bytes, with IDs 1–17 on every track. Payload totals
365,568 bytes. Container overhead accounts for the other 172,288 bytes.
The unused `$0C` descriptor cannot be fully extracted by following the loader:
only five requested pages exist before it requests side 0, track 42, sector 1.
The extractor deliberately stops rather than joining the next image side.

`python3 research/analyses/vip4-demo/tools/verify_analysis.py` checks extraction
identity, descriptor boundaries, listing addresses and small arithmetic/state
models. Results are in [verification.json](verification.json). These checks
do not execute a 6502 or prove visual/audio correctness. Cycle counts are
instruction-table calculations, never measured benchmarks.

## 7. Comparison with the knowledge base

The existing self-modifying renderer, carry extraction and descending page
copy records were consulted. Vip4 supplies related evidence with different
contracts; none is silently promoted or broadened. Ordinary lookup tables,
screen copying and module overlays are recorded in the dossier without new
duplicate fiches.

## 8. Documentation created

Six analysis reports, three technique fiches, two inspection/verification tools,
a verification record, and an `extracted/` directory with exact recovered
payloads, selected analytical listings, a manifest and extraction notes.
Derived payloads are local research artifacts, not a license grant.

## 9. Open questions and next tests

- Trace boot, VIA counter state and every vector change in a controlled Oric
  emulator; then compare disk/audio behavior on hardware.
- Confirm exact release, original compiler/assembler, licenses and contributor
  ownership against an authoritative source archive.
- Recover complete call graphs and table semantics for effects `$07/$0B/$0E`.
- Explain unused descriptor `$0C`, masked disk IRQ escape, absent resident
  retry checks, the `$8AFC` silence vector versus resident RTI at `$FC8A`, and
  the nonterminating dormant image delay.
- Establish zero-page `$02` and carry state entering the final display setup,
  and determine whether overlay bytes or ROM are intended as glyph sources.

## 10. Summary

The strongest reusable evidence is the loader's explicit overlays, self-modified
addressing in render loops and code/state reuse in zero-page IRQ players. The
most useful next investigation is an execution trace of the supplied disk with
known ROM and Microdisc configuration, logging IRQ vectors, I flag, Timer 1
counter/latches, sector requests and writes to executable operands.

## References and precise location convention

No original source lines or symbols exist. A reference such as `R:$FA9F` means
resident loaded CPU address `$FA9F`; `M02:$9D0D` means descriptor `$02` loaded
address `$9D0D`. These names are analytical. All original bytes are in
`research/sources/Oric/Vip4 Demo/vip4.dsk`.

Selected listings print each instruction's CPU address and **original DSK byte
offset**. Use the [manifest](extracted/manifest.json) sector maps for any other
payload byte: `DSK = sector.dsk_offset + byte_in_sector`. CPU spans crossing
sectors are not contiguous DSK spans because gaps and CRC bytes intervene.
`sample-zp.asm.txt` prints the relocated CPU addresses and original source
offsets; its `$000A/$000B` operands reflect the verified initialization patch,
not the untouched source values. `final-zp.asm.txt` is a relocated view of the
48-byte IRQ body; setup copies 56 bytes including eight trailing bytes.
