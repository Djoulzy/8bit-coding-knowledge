---
id: ANALYSIS-ORIC-0001
program: "L'Aigle d'Or"
cpu: ["6502"]
machines: ["oric-1", "oric-atmos"]
analysis_status: draft
source_revision: "sha256:7f01e1a3d05825aab887952cd5711bea69d6525730aba5c1e25c814334fe77d7"
analysis_date: "2026-10-09"
---

# Source-code analysis: L'Aigle d'Or

## 1. Objective and scope

Extract reusable programming knowledge from the complete supplied cassette
image: its loader, BASIC game, machine-code routines, tables and assets. **No
original assembler source is present.** This is a static binary and tokenized
BASIC analysis, not a review of an original assembly listing. Original symbols,
assembler dialect, build process and programmer intent cannot be recovered
reliably from these bytes.

All BASIC records were decoded and all image regions inspected. Significant
machine routines were followed from BASIC calls, machine calls and animation
streams. The region ledger in [architecture.md](architecture.md) distinguishes
code, interpreted data, assets, captured interpreter state and unresolved bytes.
This does not establish complete runtime reachability or every possible state.
No game, imported build script, emulator or real machine was run.

At analysis time, the requested one-level Oric instruction path was absent.
The [Oric instructions](../../../docs/machines/Tangerine/Oric/AGENTS.md), now
located in the canonical brand/machine hierarchy,
were applied together with [6502 instructions](../../../docs/cpu/6502/AGENTS.md)
and the root instructions. This six-document dossier adapts
[the analysis template](../../../templates/analysis.md); standalone findings use
[the technique template](../../../templates/technique.md).

## 2. Source provenance

| Field | Value / evidence |
| --- | --- |
| Selected program | L'Aigle d'Or; the only program found, including ignored files |
| Purpose | Graphical castle adventure with equipment, hazards and treasure collection; loader story lines 1620–1680, game object handlers 10700–10799 and success test at 3000 |
| Selection evidence | `rg --files --hidden --no-ignore -g '!.git/**'`; no competing program |
| Author | Loader BASIC line 100, CPU `$06E9`, TAP `$000200`, attributes ROCQUES Louis-Marie |
| Publisher / date | Loader lines 3–4, CPU `$0520–$056A`, TAP `$000037–$000081`: Loriciels, March 1984, reproduction restriction |
| Image version | Filename says 1984; no revision or release identifier recovered |
| Local image | [Original TAP](<../../sources/Oric/L'Aigle d'Or/Aigle D'or, Le (1984)(Loriciels).tap>) |
| Local metadata | [metadata.md](<../../sources/Oric/L'Aigle d'Or/metadata.md>), lines 1–3: Oric 1, cassette, Wikipedia link |
| Original archive / importer | Unknown; metadata links an article, not the actual image's download origin |
| License | No grant found; original contains a reproduction restriction. Local extraction is user-authorized; it does not establish redistribution rights |
| Git baseline | `cb74431`; baseline `.gitignore` ignored `research/` and this image has no addition commit |
| Local recency | TAP modification `2026-10-09T14:12:07+02:00`, metadata modification `2026-10-09T14:34:11+02:00`; filesystem timestamps are not historical release or import evidence |
| SHA-256 | `7f01e1a3d05825aab887952cd5711bea69d6525730aba5c1e25c814334fe77d7` |
| Language | Oric tokenized BASIC plus documented NMOS 6502 machine code; original assembler/toolchain unknown |

Both tape headers have type byte `$00` and autorun byte `$C7`. The loader calls
`CLOAD"AIGLEDOR.2"` at BASIC line 1350, CPU `$0A2C`, TAP `$000543`. The image
contains two named load stages in one file. A physical cassette side boundary
cannot be inferred from this envelope and is not represented as audio timing.

| Block | TAP header / payload offset | Loaded range, inclusive | Bytes | Linked BASIC records |
| --- | --- | --- | ---: | ---: |
| AIGLEDOR.1 | `$000000` / `$000018` | `$0501–$3F37` | 14,903 | 78, including two anomalous tail records |
| AIGLEDOR.2 | `$003A4F` / `$003A67` | `$0501–$9FFF` | 39,679 | 464, including the real fallback line 21845 |

All 54,630 image bytes are accounted for by two headers and two payloads, with
no trailing bytes. The first stage is overwritten by the second, not retained
as an additional 14,903-byte allocation.

### Precise reference convention

`B1` and `B2` below designate these blocks. CPU ranges are inclusive unless
stated otherwise. Tape offsets are zero-based, hexadecimal, and stable for the
given checksum. Convert any loaded address `a` with:

- B1: `TAP(a) = $000018 + (a - $0501)`.
- B2: `TAP(a) = $003A67 + (a - $0501) = a + $3566`.

The extracted BASIC text prints original BASIC line numbers, CPU addresses and
TAP offsets. Analytical machine routine names in this dossier are newly assigned
descriptions, not recovered historical labels. Reconstruction uses `$` for
hexadecimal addresses and `#` for immediate operands; Oric BASIC uses `#` for
hexadecimal values. These are different syntax conventions.

## 3. Target environment

- **Processor:** instructions examined fit the documented NMOS 6502 set. There
  is no established use of 65C02 extensions or undocumented opcodes.
- **RAM:** 48K configuration required. B2 loads to `$9FFF` and drawing uses
  `$A000` and higher. The metadata's Oric-1 target is consistent with this.
  Loaded payload size is not the same as total runtime RAM consumption.
- **Models:** Oric-1 is directly named locally. B2 line 42 tests `$FFF9` and
  patches the ROM call from `$F89B` to `$F8D0` when the byte is `$01`. This is
  evidence of intended ROM adaptation, not proof this exact image works on
  every Oric-1/Atmos ROM. A contemporary [Tilt review](https://www.oric.org/ftp/ceo/ceomag/downloads/tilt/1984/Tilt-12ocr.pdf)
  describes the release as Oric-1/Atmos software, independently of this dump.
- **ROM:** BASIC interpreter, cassette loading, graphics primitives, keyboard
  service, sound commands and system interrupt timers remain dependencies.
  Exact ROM binaries were not supplied or executed.
- **Video:** HIRES room views and software sprites; TEXT for introduction,
  shop, inventory and darkness sequences; HIRES text rows for status.
- **Audio/input:** stock sound/keyboard circuitry through ROM BASIC commands;
  no game-owned AY register writer or keyboard matrix scanner identified.
- **Storage/extensions:** standard tape input is explicit. No disk, joystick,
  overlay RAM or other extension requirement was found in the examined paths.
- **Verification:** byte parsing, static control/data analysis and narrow
  arithmetic models; no emulator trace, real-hardware measurement or benchmark.

## 4. Program architecture

For the program-specific Apple IIe adaptation inventory, rule/state mapping,
resource dependencies and reproduction/acceptance checklist, see
[portage.md](portage.md). It is a porting plan, not an implemented conversion.

The first stage displays an 8,000-byte bitmap using two tiny routines generated
from hexadecimal BASIC strings, adds attribute effects and ROM-generated sound,
then presents story and controls before loading the main stage.

The main stage retains the BASIC interpreter as its controller. BASIC owns
quests, inventory, money, fatigue, room transitions, text and sound decisions.
6502 routines own packed room decoding, image copying/compositing, saved
backgrounds, animation interpretation, coarse collisions and enemy movement.
Shared state lives below BASIC at `$0400–$04D0`; scratch pointers live in zero
page; persistent room records and graphics occupy RAM above the BASIC heap.

The loop at BASIC 5000–5990 repeatedly advances machine animation and enemy
logic, polls `KEY$`, dispatches through a line-number table and updates status.
Timing depends on the executed BASIC path and VIA timer configuration. This is
not an established fixed-frame or video-synchronized engine.

See [architecture.md](architecture.md) for the memory ledger, command format,
room representation, state ownership and execution graph; see
[routines.md](routines.md) for entry points and relationships.

## 5. Analysis findings

The most useful discoveries are the resumable animation command language,
two-byte inline rendering patches, and saved-background buffers carrying their
own coordinates. The separate semantic collision grid and an `RTS` borrowed
from a BASIC line-number byte are also recorded. Detailed advantages,
limitations, comparisons and validation states are in
[findings.md](findings.md), [cpu-techniques.md](cpu-techniques.md) and
[hardware-techniques.md](hardware-techniques.md).

## 6. Performance and verification

Reproduce from the repository root with Python 3.9 or newer:

```sh
python3 research/analyses/laigle-dor/tools/inspect_tape.py
python3 research/analyses/laigle-dor/tools/verify_analysis.py
```

| Check | Method | Result / limit |
| --- | --- | --- |
| Original preservation | SHA-256 and exact block/payload comparison | Original hash unchanged; both standalone `.tap` blocks and `.bin` payloads match the original |
| BASIC structure | Follow and verify each next-line pointer | 78 B1 / 464 B2 linked records; semantic anomalies explicitly retained |
| Multiply `$3E00` | Binary arithmetic model tied to exact bytes | All 65,536 unsigned byte pairs agree with multiplication; no decimal-mode or IRQ modeling |
| Address `$3E21` | Model all 40 byte columns × 200 rows | All 8,000 addresses equal `$A000 + 40*y + x` |
| Carry unpack `$3F0B` | Model 256 byte values × both incoming carry states | All 512 cases emit the four original high-to-low two-bit fields |
| Saved-background capacity | Loaded descriptor inspection | Six active buffer slots fit pixel data below their two coordinate bytes |
| Performance | MOS instruction-table calculation | Conditional theoretical values only; detailed assumptions in CPU analysis |

[verification.json](verification.json) records the results. A modeled arithmetic
check is neither an emulator observation nor a performance benchmark. Findings
remain `analyzed`, never `benchmarked` or `validated` on this evidence.

## 7. Comparison with the knowledge base

The subsequent [integration review](integration-review.md) records current
promotion decisions. It validates selected representation/algorithm contracts;
it does not upgrade the game's full runtime or the other initial findings.

The initial `docs/common/`, CPU and machine directories contain no technique
records or validated guidelines, only instructions. `research/analyses/` and
`research/findings/` initially contain no analyses/findings. Therefore there are
**no existing repository techniques to confirm or improve**. Familiar patterns
such as zero-page pointers, shift/add multiplication and packed records are
recognized without inventing existing IDs or claiming global novelty.

## 8. Documentation created

The requested six Markdown documents are this overview, architecture, routine
inventory, CPU techniques, hardware techniques and findings. Five selective
research records link back here. The user-authorized extraction is stored under
[extracted/](extracted/README.md), including standalone tape blocks, original-byte payloads, analytical
BASIC text and a manifest; inspection and verification scripts are under
`tools/`. No validated guideline or historical source was modified.

The current `.gitignore` ignores `research/sources/`; analyses, findings and
extractions are visible as untracked files. At initialization it ignored all of
`research/`; that file changed independently during the work. This analysis did
not edit ignore rules, stage files or make a commit.

## 9. Open questions and next tests

1. Run both stages with identified ROM 1.0 and 1.1 images, recording hashes,
   the `$FFF9` test and the `$F89B/$F8D0` call effects.
2. Trace animation streams, overlap restoration and input-buffer zero-page
   ownership while interrupts remain active.
3. Check the unusual comparison/storage sequences and inactive remnants
   identified in the CPU report before proposing fixes.
4. Compare multiply-by-40 with shifts/adds and a scanline table; compare the
   patched renderer with separate entry points under equivalent conditions.
5. Recover original assembler source and a cassette/manual provenance if
   available; preserve all imported material unchanged.

## 10. Summary

The reusable value is the division of labor between BASIC and machine code,
compact animation and room data, bounded background preservation and direct
use of the Oric byte-oriented display. Layout-dependent code reuse and signed
flag shortcuts illustrate historical compromises rather than universal advice.
Runtime compatibility, visual correctness and measured speed remain open.

## References

- [Original payload manifest](extracted/manifest.json), [loader reconstruction](extracted/aigledor.1.basic.txt), [game reconstruction](extracted/aigledor.2.basic.txt).
- [Oric Atmos Manual, Ian Adamson](https://library.defence-force.org/books/content/manual_atmos.pdf), chapters 7–8 and appendices 5, 8–12. Manufacturer-issued manual; scanned OCR contains errors.
- [MOS Technology MCS6500 Instruction Set Summary](https://ftpmirror.your.org/pub/misc/bitsavers/components/mosTechnology/6502_Instruction_Set_Summary.pdf), instruction table and page-crossing footnotes.
- [Oric-1/Atmos Service Manual](https://www.cpcwiki.eu/imgs/7/70/Oric_-_Service_manual.pdf), hardware descriptions and circuit documentation.
- [Oricutron tape implementation](https://github.com/pete-gordon/oricutron/blob/master/tape.c), `tape_setup_header` and `tapsections`, for independently checking TAP envelope parsing.
- [Oricutron ULA implementation](https://github.com/pete-gordon/oricutron/blob/master/ula.c), `ula_decode_attr` and `ula_renderscreen`; corroborating implementation evidence, not a hardware test.
