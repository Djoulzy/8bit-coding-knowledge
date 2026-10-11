---
id: "ANALYSIS-APPLE2-LODE-RUNNER-OVERVIEW"
program: "Lode Runner (local cracked disk)"
cpu: ["6502"]
machines: ["apple-ii-family", "apple-iie-variant-unknown"]
analysis_status: draft
source_revision: "d02edc77fa0a02d3f679af22456ca1c762c305dc"
analysis_date: "2026-10-10"
---

# Binary-code analysis: Lode Runner

## 1. Objective and scope

Full-mode static analysis of the requested directory. The sole historical input
is a sector image, not assembly source. Original labels and assembler dialect are
unknown; all routine names below are analytical. No imported code was executed.

Architecture and subsystem entry points are mapped. Level packing, logical maps,
graphics address tables, sprite expansion/compositing, guard scheduling,
inline text/audio streams and score arithmetic were examined in depth.
Complete guard route selection, every editor command, disk formatting, boot DOS,
all sound sequences and every movement transition remain outside detailed coverage.

## 2. Source provenance

| Field | Value |
| --- | --- |
| Program / date | Lode Runner; filename indicates 1983 |
| Original author / publisher | Doug Smith / Brøderbund, corroborated by the [publisher's manual](https://mirrors.apple2.org.za/ftp.apple.asimov.net/documentation/applications/misc/Broderbund_Lode_Runner_manual.pdf), cover and copyright page |
| Local edition | Filename marks a crack; CPU $5A30 contains a cracker credit; publisher-original equivalence unknown |
| Download / archive provenance | Unknown |
| License / distribution terms | No license supplied; no redistribution grant established |
| Historical input | research/sources/Apple IIe/Lode Runner/Lode Runner (1983)(broderbund)[cr].dsk |
| Image SHA-256 | cbc048a55c2835f1b3b54696660e8902c84c25dac44a6dc94b13a7e8f81379ec |
| Git baseline | d02edc77fa0a02d3f679af22456ca1c762c305dc |
| Working-tree context | Clean tracked baseline at start; historical images are ignored by the repository's research/sources/ rule |
| Language / toolchain | Applesoft HELLO plus documented NMOS 6502 instructions in examined code; original assembler/build unknown |

The image is 143,360 bytes, 35 tracks × 16 sectors × 256 bytes.
It contains a DOS 3.3 filesystem in **ProDOS image-sector order**.
Identity/DOS image-slot order fails the file-chain checks. See the
[manifest](extracted/manifest.json) for the verified permutation and every sector.

| Active file | Catalog type | Header / payload | Allocation |
| --- | --- | --- | --- |
| LODE RUNNER | Locked binary, $84 | Load $07FD; $8F03 = 36,611 bytes through $96FF | 144 data sectors + 2 T/S list sectors |
| HELLO | Applesoft, $02 | 53 payload bytes; BASIC line 10 starts the binary | 1 data sector + 1 T/S list sector |

Deleted Ultima entries and residual Ultima BASIC are present. Their contents were
not treated as Lode Runner code. Custom game sectors are referenced separately
from catalog file ownership.

## 3. Target environment

- **CPU:** examined instructions fit the documented NMOS 6502 ISA.
  Physical CPU and enhanced IIe/65C02 behavior have not been tested.
- **Machine:** Apple II family interfaces are confirmed. The folder says IIe;
  original/nonenhanced/enhanced IIe and ROM revision remain unknown.
- **Memory:** assets and DOS/RWTS occupy main RAM through $BFFF;
  48 KiB main memory is the working requirement. Auxiliary RAM/language-card
  requirements are not established.
- **Display:** paired HGR regions $2000–$3FFF and $4000–$5FFF; the mapped
  gameplay path displays page 1 and retains terrain in page 2.
- **Devices:** keyboard, two analog axes/buttons, speaker, DOS-style RWTS and
  an inherited disk-I/O vector.
- **Verification:** Python static extraction/property checks; no emulator,
  original machine, cycle trace or build.

Hardware names were checked in Apple's [Reference Manual](https://downloads.reactivemicro.com/Apple%20II%20Items/Documentation/Manuals/Apple%20II%20Reference%20Manual%20-%20The%20Red%20Book/2023-04-27%20-%20Apple%20II%20Redbook.pdf), printed
pp. 137–138 and monitor equates. IIe bank/80STORE state remains a question.

## 4. Program architecture

HELLO → DOS BRUN → $07FD → cracked front end $5A00 → relocation $5F00 →
game $6000. The foreground loop combines player update $64BD, timed holes
$75F4, guard scheduler $6C82 and sound/delay service $8811.
See [architecture](architecture.md) and [routine inventory](routines.md).

## 5. Analysis findings

Four new provisional records are indexed in [findings](findings.md):

- GEN-0005: work quotas with persistent round-robin actor selection.
- CPU6502-0007: inline parameters consumed by rewriting a JSR return address.
- APPLE2-0001: paired HGR pages for masked restoration and overlap detection.
- APPLE2-0002: seven alignment tables expanding row tokens into pixel pairs.

GEN-0002 is confirmed by separate occupancy/terrain grids. Carry-based field
selection and full-page traversal corroborate existing CPU principles within
different caller contracts.

## 6. Performance and verification

[verification.json](verification.json) records extraction equality, source mapping,
192 HGR rows, 896 phase/pattern pairs, coordinate tables, quota models and a
150-sector level audit. These support narrow analyzed behavior, not bootability,
gameplay or performance. No finding is benchmarked.

~~~sh
python3 research/analyses/lode-runner/tools/inspect_disk.py --extract
python3 research/analyses/lode-runner/tools/verify_analysis.py
~~~

## 7. Comparison with the knowledge base

The [findings index](findings.md#comparison-and-duplicate-review) records duplicate
checks. The HGR baseline differs from per-sprite saved backgrounds and clipped
scene recomposition; seven-phase tables differ from Oric parity-compressed tables.

## 8. Documentation created

Six reports: overview, architecture, routines, cpu-techniques,
hardware-techniques and findings. Supporting extraction, sector manifest,
selected listings, table dumps, level audit and verification tools are under
this directory. Four fiches are under research/findings/. Historical files
and docs guidelines were left unchanged.

## 9. Open questions and next tests

1. **First priority:** trace cold boot and the first level read. $630E calls
   $0023, whose reconstructed bytes jump to $1700; that destination currently
   contains graphics data. No intervening patch/overlay has been established.
   The metadata path reaches a coherent DOS/RWTS shim.
2. Relocation reads $9700/$9701 outside the declared payload, copying unknown
   bytes to $0800/$0801, and attempts writes to $C000/$C001.
3. Candidate level 136, logical track $0B/sector $07, contains out-of-range
   nibbles and multiple player markers, unlike the other 149 sectors. This is
   an anomaly, not proof of corruption or original game behavior.
4. Confirm token bounds for every used sprite. Last-row positions for apparent
   IDs $66/$67 contain two out-of-domain bytes in the captured payload.
5. Trace actor overlaps, changing terrain, IRQ ownership, ROM assumptions and
   NTSC/PAL/accelerated-machine timing before recommendations.

## 10. Summary

The strongest results concern byte representation and local control flow.
Potential optimizations include direct phase-output tables, conventional page
copies for the cracked loader and bounded audio interfaces; see
[cpu-techniques](cpu-techniques.md). Captured loader/state anomalies must not be
attributed to Doug Smith's original design without a trusted-edition comparison.

## References

- [Extraction conventions](extracted/README.md).
- [MOS instruction summary](https://ftpmirror.your.org/pub/misc/bitsavers/components/mosTechnology/6502_Instruction_Set_Summary.pdf), instruction/flag/timing reference.
- [Publisher manual](https://mirrors.apple2.org.za/ftp.apple.asimov.net/documentation/applications/misc/Broderbund_Lode_Runner_manual.pdf), printed pp. 2–9 for modes and tile vocabulary.
