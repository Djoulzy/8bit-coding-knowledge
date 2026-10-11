---
id: "ANALYSIS-APPLE2-KARATEKA-FINDINGS"
program: "Karateka"
cpu: ["6502"]
machines: ["apple-iie"]
analysis_status: complete
source_revision: "d02edc77fa0a02d3f679af22456ca1c762c305dc"
analysis_date: "2026-10-11"
---

# Findings, existing knowledge and research candidates

Original program: Karateka, Jordan Mechner / Broderbund, 1984 identification;
exact supplied disk edition and license unknown. [Overview](overview.md) records
the image SHA-256 and repository baseline. Addresses and `DSK` offsets refer
to [the original image](<../../sources/Apple IIe/Karateka/Karateka (1984)(Broderbund).dsk>),
with reconstructed evidence in [selected disassembly](extracted/selected-disassembly.txt).
No original source lines/symbols exist in this input.

## Finding index

| Candidate | Level | Precise evidence | Technical result / trade-off | Status / decision |
| --- | --- | --- | --- | --- |
| K01 | common; CPU implementation | `$7071–$70A5`, `DSK=$004871–$0048A5`; caller `$B584`, `DSK=$008D84` | Common 16-byte actor window permits fixed field accesses; consumes 16 extra ZP bytes and copying | analyzed; new GEN-0006 |
| K02 | machine | `$1A84–$1AEA`, `DSK=$009284–$0092EA`; mirror `$1AF4–$1C5A`, `DSK=$0092F4–$00945A`; table `$0980`, `DSK=$00A180` | Runtime seven-bit phase splitting plus reversal table; shares assets across phase/facing at a runtime cost | analyzed locally; new APPLE2-0003 |
| K03 | CPU | `$1965`, `DSK=$009165`; sites `$19E6/$1BF2`, `DSK=$0091E6/$0093F2` | Equal-width NOP/ORA/AND selection; shared loop, non-atomic RAM patches | analyzed; existing CPU6502-0001, no new fiche |
| K04 | common | `$6400–$648A`, `DSK=$005C00–$005C8A`, controls through `$653F` | Retained parallel animation cursors and token dispatch; unchecked byte indices/restarts | analyzed local decoder; related GEN-0001, no new fiche |
| K05 | common + machine | `$678F–$680E`, first `DSK=$005F8F`; `$A316–$A344`, `DSK=$001B16–$001B44` | Repair scene regions using older geometry across alternating pages; layer order/bounds remain complex | analyzed locally; related GEN-0003, no new fiche |
| K06 | CPU + machine | Startup `$2100`, `DSK=$009900`; `$7609`, `DSK=$004E09`; `$0786/$774B`, `DSK=$009F86/$004F4B` | Lifetime-based relocation and separate page-copy/flip operations; consumes two 8 KiB pages, ROM/banking dependencies | analyzed selected loops; retain report, no broad guideline |
| K07 | machine + CPU | `$0D00–$0DA5`, `DSK=$00A500–$00A5A5`; `$0DC0–$0DF9`, `DSK=$00A5C0–$00A5F9` | Foreground command/counter and packed-bit speaker output; CPU-bound timing, patched code | analyzed locally; timing/complete stream contracts pending |
| K08 | machine | `$0300–$03ED`, `DSK=$009B00–$009BED`; low transition `$020C`, `DSK=$009A0C` | Disk-ROM copying, raw reads, whole-ZP exchange; complete scene/protection protocol unknown | observed; no standalone fiche yet |

## New provisional fiches

- [GEN-0006: fixed actor work window](../../findings/GEN-0006-fixed-actor-work-window.md).
  The generic load/process/commit organization is distinct from storing program
  state in code operands. The implementation's 6502 timing and ZP allocations
  are explicit instance costs, not requirements on every CPU.
- [APPLE2-0003: runtime sprite shift and reflection](../../findings/APPLE2-0003-runtime-sprite-shift-and-reflection.md).
  Its 103-byte shifter and 128-byte reflection table are distinct from the
  seven-phase pointer/pair tables in APPLE2-0002. Local shift/reversal behavior
  is understood; complete clipping/composition and displayed colors are untested.

## Existing techniques confirmed or given related evidence

| Existing record | Karateka contribution | Qualification |
| --- | --- | --- |
| [CPU6502-0001](../../findings/CPU6502-0001-two-byte-render-patches.md) | Native code selects copy/OR/AND with equal-width two-byte sites | Existing Oric provenance remains unchanged; this is additional Apple II evidence |
| [GEN-0001](../../findings/GEN-0001-resumable-animation-streams.md) | Retained cursors select frames/movement and control commands across updates | Different grammar and stepping; all sequence termination/bounds not proven |
| [GEN-0003](../../findings/GEN-0003-clipped-scene-recomposition.md) | Limited-region scene repair and redraw instead of an assumed saved-background image per actor | Direct alternating HGR pages, not that record's exact scratch/occlusion design |
| [APPLE2-0001](../../findings/APPLE2-0001-paired-hires-background-masks.md) | AND-mask then OR-image composition is present | Related operator pattern only; its saved-baseline contract is not confirmed here |
| [APPLE2-0002](../../findings/APPLE2-0002-seven-phase-sprite-tables.md) | Supplies a concrete phase-table alternative for comparison | No duplicate; code/data/cycle formats differ |
| [CPU6502-0004](../../../docs/cpu/6502/descending-page-copy.md) | Comparator for page-sized transfer analysis | Startup here ascends and patches absolute operands; not the same loop |

Searches covered existing IDs and descriptions across `docs/` and
`research/findings/` before allocating GEN-0006 and APPLE2-0003. Existing
records and guidelines were not edited; no automatic promotion occurred.

## Verification, limitations and possible optimizations

[Static verifier](tools/verify_analysis.py) checks source identity, extracted
hashes, sector mappings, relocation, record-loop bytes, tables and translated
shift/join algebra. [Results](verification.json) include 3,584 shifter and
114,688 fragment-join cases. Status is **analyzed**, not benchmarked or validated.
No historical code was executed. Calculated copy-loop timing is documented in
[C01](cpu-techniques.md#c01-fixed-actor-fields-through-a-copied-work-record).

Potential optimizations: remove duplicate mode loads, dispatch phase once per
draw, compare compact lookup/pre-shifted rows, specialize opaque mode and compare
indexed actor records with copied work records. Their concrete trade-offs are
listed in [CPU hypotheses](cpu-techniques.md#optimization-hypotheses-and-validation-priorities).
No implementation or measured speedup is claimed.

## Unresolved technical questions

- Initial boot/DOS read execution, media edition, later disk overlays and protection.
- Complete vertical/zero-size clipping, all mask/image pairs, scene/page repair bounds.
- Exact CPU/ROM/banking configuration, decimal mode, ZP and patch ownership, stack use.
- Full action/AI/combat grammar, all animation streams and input calibration.
- Foreground audio frequency/latency and complete sound pointer initialization.

The next investigation should trace boot, one normal actor exchange and page
flips on a named Apple IIe ROM, then exhaustively compare renderer edge cases
with a pixel reference. Broader performance conclusions require representative
workloads and reproducible timing, not table-entry tests alone.

