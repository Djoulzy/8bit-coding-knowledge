---
id: "ANALYSIS-APPLE2-LODE-RUNNER-FINDINGS"
program: "Lode Runner (local cracked disk)"
cpu: ["6502"]
machines: ["apple-ii-family", "apple-iie-variant-unknown"]
analysis_status: draft
source_revision: "d02edc77fa0a02d3f679af22456ca1c762c305dc"
analysis_date: "2026-10-10"
---

# Lode Runner finding index

## Snapshot and status

The [overview](overview.md) records hash, author, cracked edition, unknown
assembler/license and git baseline. CPU addresses and original DSK mappings
replace unavailable source lines. All four new fiches are provisional/analyzed.
Property checks support local transforms, not whole-program correctness or timing.

## New records

| ID | Applicability | Evidence | Contribution / remaining validation |
| --- | --- | --- | --- |
| [GEN-0005](../../findings/GEN-0005-bit-quota-round-robin.md) | Common; 6502 implementation | [scheduler.asm.txt:L1–L18](extracted/scheduler.asm.txt), CPU $6C82–$6CA6, first instruction at DSK $014589; [scheduler.asm.txt:L19–L25](extracted/scheduler.asm.txt), CPU $6CDB–$6CE9, first instruction at DSK $0145E2 | Quota vs actor selection; trace bounds, early exits and pacing |
| [CPU6502-0007](../../findings/CPU6502-0007-inline-stream-return-address.md) | CPU | [input-audio.asm.txt:L225–L242](extracted/input-audio.asm.txt), CPU $86E0–$86FF, first instruction at DSK $016FE7; [input-audio.asm.txt:L353–L378](extracted/input-audio.asm.txt), CPU $87E1–$8810, first instruction at DSK $0161E8 | Inline parameters/synthetic return; verify nested ownership and malformed streams |
| [APPLE2-0001](../../findings/APPLE2-0001-paired-hires-background-masks.md) | Machine | [renderer.asm.txt:L50–L58](extracted/renderer.asm.txt), CPU $7A3E–$7A50, first instruction at DSK $015345; [renderer.asm.txt:L282–L417](extracted/renderer.asm.txt), CPU $8336–$8437, first instruction at DSK $015D3D | Paired baseline/display masks; trace actor order/terrain/bounds |
| [APPLE2-0002](../../findings/APPLE2-0002-seven-phase-sprite-tables.md) | Machine plus CPU | [renderer.asm.txt:L418–L480](extracted/renderer.asm.txt), CPU $8438–$84C0, first instruction at DSK $015E3F; $A200–$ACFF tables | Seven pixel phases/shared pairs; verify used domain and alternatives |

## Other candidates retained in reports

| Candidate | Level / status | Source | Trade-off / open issue |
| --- | --- | --- | --- |
| Low-first nibble levels | Common/CPU; analyzed | $627E–$629E, $62C7–$630D | 224 bytes vs 448; unpacked grids spend RAM |
| Occupancy/terrain grids | Common; analyzed | $6269–$6278, $63B3–$64BC | Independent logic/display; keep updates synchronized |
| Synthetic RTS dispatch | CPU; analyzed | $6A2B–$6A48, $7C29–$7C4C | Avoids pointer; stack/target−1 contract |
| Patched title stream | CPU/common; analyzed fragment | $600B–$6045 | Column/row controls; full stream bounds unreviewed |
| BCD score | CPU; analyzed fragment | $7A92–$7AA9 | Direct digits; decimal state/overflow |
| Foreground audio/delay | Machine/common; analyzed fragment | $87BA–$884A | Compact; precise timing depends on sound |
| Timed holes/parallel arrays | Common; analyzed fragment | $6C39–$6C81, $75F4–$7715 | Fixed capacity; full array scans |
| Threshold-swap axis inversion | Common/machine; analyzed | $6A9E–$6AB9 | Configuration changes replace per-sample work |
| Loader edges | CPU; observed risk | $5F00–$5FA1 | Unknown overread and I/O writes; no recommendation |

Established patterns and incompletely explored contracts do not each need a fiche.

## Comparison and duplicate review

| Existing record | Relationship / decision |
| --- | --- |
| [GEN-0002](../../../docs/common/semantic-collision-grid.md) and [historical record](../../findings/GEN-0002-semantic-collision-grid.md) | Separate semantic grids confirmed; no duplicate or widened validation |
| [CPU6502-0003](../../../docs/cpu/6502/carry-stream-field-extraction.md) | Carry survives loads; order/width/destructive-state contracts differ |
| [CPU6502-0004](../../../docs/cpu/6502/descending-page-copy.md) | Full-page traversal; local order/ownership does not inherit validation |
| [CPU6502-0001](../../findings/CPU6502-0001-two-byte-render-patches.md) | Related patches; pointer operands instead of NOP/ORA choice |
| [CPU6502-0005](../../findings/CPU6502-0005-zero-page-code-operands-as-state.md) | Absolute-code decoding operands, not ZP IRQ state |
| [CPU6502-0006](../../findings/CPU6502-0006-irq-frame-discard-and-rts.md) | Inline JSR parameters use no IRQ-frame discard |
| [GEN-0004](../../findings/GEN-0004-stack-driven-pair-grammar.md) | Grammar work stack differs from return-pointer parsing |
| [GEN-0003](../../findings/GEN-0003-clipped-scene-recomposition.md) | Terrain baseline differs from clipped scene redraw |
| [ORIC-0001](../../findings/ORIC-0001-background-pages-with-position-metadata.md) | Whole HGR baseline differs from per-sprite saved pages |
| [ORIC-0003](../../findings/ORIC-0003-parity-compressed-pixel-tables.md) | Seven 7-bit phases/pair pointers differ from parity-compressed 6-bit tables |

GEN 1–4 and CPU6502 1–6 were checked across docs/findings, including promoted IDs.
No prior APPLE2 record was found. New IDs: GEN-0005, CPU6502-0007,
APPLE2-0001 and APPLE2-0002.

## Verification and next investigation

[verification.json](verification.json) records static checks, no emulation,
hardware or benchmark. The two out-of-domain sprite tokens, $0023 vector and
level 136 stay open. No historical bytes were repaired.

Best next step: exact-image cold-boot trace, then trusted-edition comparison.
After resolving memory provenance, compare direct phase tables and overlapping
actors. Only reproducible measurements can justify benchmarked status.

## Outputs

Six reports, four linked fiches and [extraction support](extracted/README.md).
Original sources and validated guidelines are unchanged.
