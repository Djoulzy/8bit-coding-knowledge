---
id: "ANALYSIS-ORIC-SPACE1999-FINDINGS"
program: "Space: 1999"
cpu: ["6502"]
machines: ["oric-atmos"]
analysis_status: complete
source_revision: "upstream c81612082482d1f497638ada14ad4640c5e4f1ec; local disk SHA-256 9d85e1d75d9f1e548f4d1e3bc3750085e7c8c125bb6cd110fb604ba86ba3e851"
analysis_date: "2026-10-09"
---

# Space: 1999 finding index

## 1–3. Scope, provenance and status

Findings derive from the pinned published source and explicitly identified local byte comparisons. Authors, input hashes, unknown license and binary-version limits are in [overview](overview.md). All new fiches are **analyzed**: behavior is explained, but neither benchmarked nor validated as a recommendation.

## 4–5. New reusable techniques

| ID / fiche | Level | Evidence | Trade-off / validation still needed |
| --- | --- | --- | --- |
| [GEN-0003: clipped scene recomposition](../../findings/GEN-0003-clipped-scene-recomposition.md) | Common algorithm; Oric implementation | [upstream `game source/WHITE/white.s:L775–L783`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/WHITE/white.s#L775-L783); [upstream `game source/NOISE/spritemov.s:L71–L208`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/NOISE/spritemov.s#L71-L208); [upstream `game source/NOISE/clipping.s:L386–L473`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/NOISE/clipping.s#L386-L473) | Tiny scratch memory; repeated scene/occlusion work and strict clip capacity. Measure against saved backgrounds and broader redraw |
| [GEN-0004: stack-driven binary-pair grammar](../../findings/GEN-0004-stack-driven-pair-grammar.md) | Common compression; 6502 stack implementation | [upstream `game source/sp1999.s:L4235–L4264`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/sp1999.s#L4235-L4264); [upstream `game source/stringsc.s:L1903–L2032`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/stringsc.s#L1903-L2032) | 256-byte grammar and no recursive expansion calls; shared stack and token/literal restrictions. Verify printing and worst combined stack |
| [ORIC-0003: parity-compressed pixel tables](../../findings/ORIC-0003-parity-compressed-pixel-tables.md) | Machine-specific | [upstream `game source/NOISE/groutines.s:L97–L175`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/NOISE/groutines.s#L97-L175); [upstream `game source/NOISE/noise-tail.s:L13–L37`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/NOISE/noise-tail.s#L13-L37) | 440-byte tables; odd-coordinate branches and fixed bounds. Arithmetic model passes all 48000 legal coordinates; timing unmeasured |

## 6. Verification strength

The map and grammar match the disk exactly. The disk-handler signature also occurs in it. The parity model reads the published tables and checks their address/mask results; it is not assembled instruction execution. No complete executable match, build, emulator trace or hardware benchmark exists. See [verification.json](verification.json) and the reproducer commands in overview.

## 7. Existing techniques corroborated

| Existing ID | Relationship | Action |
| --- | --- | --- |
| [CPU6502-0006](../../findings/CPU6502-0006-irq-frame-discard-and-rts.md) | Same three-byte IRQ disposal + RTS to pending JSR; enabled in published disk path, [upstream `game source/disk.s:L170–L245`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/disk.s#L170-L245) | Cross-reference only; existing fiche/status unchanged |
| [CPU6502-0001](../../findings/CPU6502-0001-two-byte-render-patches.md) | Related fixed-width executable patching; here three NOPs become a JSR | Record width/call difference in CPU report; no duplicate |
| [GEN-0002](../../findings/GEN-0002-semantic-collision-grid.md) | Layered logical geometry/collision distinct from displayed masks | Corroboration, not identity of map format |
| [ORIC-0001](../../findings/ORIC-0001-background-pages-with-position-metadata.md) | Alternative saved-background method | Compare with scene recomposition; do not describe Space 1999 as a snapshot renderer |

GEN-0001 animation streams and ORIC-0002 charset animation were inspected and are not exact equivalents of WHITE's image-pointer frame stepping. General shift/add arithmetic and changed-AY-register submission are documented in topical reports, without an unnecessary new fiche for each occurrence.

## 8. Documentation changes

Created six analysis reports, three research fiches, evidence collector/fetcher and manifests. No `docs/` promotion; no imported-source changes; no update of existing findings' validation statuses.

## 9. Potential improvements and unresolved questions

- Test map clearing's 101 writes into 100-byte arrays and the final overwrite of `_ink_colour`.
- Test the library's early collision-callback exit with X=0; it bypasses a saved-byte PLA. The game's normal callback returns X=1, so applicability to gameplay is limited.
- Investigate TimerCounter lost updates, long foreground stalls and inherited IRQ frequency.
- Compare the actual 512-byte save span with live-state labels; add corruption/version checks and explicit disk-error handling in a modern reproduction.
- Bound room lookup for an unknown ID, dirty-region capacity and all occlusion geometry assumptions.
- Audit V before the source's “always” BVC and D before foreground arithmetic.
- Verify AY envelope retriggers before generalizing write suppression.

These are source-based concerns or optimization hypotheses, not fixes applied to historical files or proven defects in the supplied executable.

## 10. Recommended next investigation

Recover the French executable's linked memory map and establish code correspondence, then run a bounded Atmos/Microdisc emulator trace covering movement/redraw and disk IRQ handover. That resolves version uncertainty before timing or hardware conclusions are promoted.
