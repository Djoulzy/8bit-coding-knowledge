---
record_type: machine-topic-guide
topic: graphics
machines: ["apple-iie"]
cpu: ["6502"]
status: mixed
review_date: "2026-10-12"
---

# Apple IIe HGR representation and renderer experiments

Scope: ordinary HGR under an explicitly established IIe configuration. Neither
historical dossier proves complete renderer execution, auxiliary-bank state or
artifact-color output. Double-HGR and other video modes need separate evidence.

## Documented display constraints

**Constraint:** Ordinary HGR separates seven displayed pixel bits from bit 7,
which affects color interpretation. Visible rows have 40 bytes, but scanline
addressing is not linear; an 8 KiB page allocation is not a contiguous array of
visible scanlines. Define addresses, bounds and bit-7 behavior independently.

**Evidence:** [Apple II Reference Manual](https://www.applelogic.org/files/AIIREF.pdf),
printed p. 19, and the checked row tables in
[Lode Runner H01](../../../../../research/analyses/lode-runner/hardware-techniques.md#h01--scanline-tables-and-paired-page-pointers-analyzed-machine)
and [Karateka H01](../../../../../research/analyses/karateka/hardware-techniques.md#h01-page-relative-hgr-addressing).
The latter analyses record `$2000–$3FFF` and `$4000–$5FFF` paths, not a proof
of active bank state on every IIe. See [mapping constraints](cpu-and-memory.md#documented-mapping-constraints).

**Adaptation and trade-offs:** A row table spends RAM to simplify addressing;
arithmetic or sequential row pointers have different setup/access costs.
Preserving boundary pixels and bit-7 conventions adds mask work. The captured
`OR $80` convention is not a universal palette recommendation; compare actual
output for the selected monitor, phase and model. No fastest renderer is validated.

## Validated representation rule

### Keep logical collision state independent of HGR

**Recommendation:** For cell-based movement, query bounded logical properties
derived from authoritative world state rather than displayed HGR bytes.

**Why:** Artwork, page repair and composition need not encode actor identity or
gameplay rules. The canonical proof validates bounded cell lookup and display
independence, not historical collision behavior or fine-pixel intersection.

**Prerequisites:** Explicit cell dimensions, coordinate conversion, index width,
boundary policy and synchronization when terrain or occupancy changes.

**Trade-offs:** A byte map costs `width * height` bytes and update work; coarse
cells alone do not establish silhouette or swept collision. Sparse object lists,
tile flags or a second fine test may suit another workload better.

**Porting/adaptation:** Lode Runner keeps distinct terrain/occupancy grids.
Their meanings, special values and update ordering are game-specific. Do not
replace that logical state with the renderer's masked foreground difference.

**Evidence:** [GEN-0002](../../../../common/semantic-collision-grid.md),
[integration review](../../../../../research/analyses/laigle-dor/integration-review.md#gen-0002-semantic-collision-map),
[Lode Runner comparison](../../../../../research/analyses/lode-runner/findings.md#comparison-and-duplicate-review).

## Candidates requiring validation

The following are **experimental choices**, not current best practices.

### Persistent baseline versus alternating frame pages

| Observed organization | Evidence | Main contract / proposed test |
| --- | --- | --- |
| Page 1 foreground, page 2 retained terrain | [APPLE2-0001](../../../../../research/findings/APPLE2-0001-paired-hires-background-masks.md) | Additional 8 KiB baseline; terrain updates, OR-composition invariant and actor restore/draw order must agree |
| Alternating draw/display pages with retained repair geometry | [Karateka H04](../../../../../research/analyses/karateka/hardware-techniques.md#h04-alternating-pages-and-retained-repair-geometry) | Every page's older positions and scene layers need correct dirty bounds and repair before its next display |

These are different owners of the second page. The captured Lode Runner path
is not ordinary alternating-frame double buffering. Its unmasked baseline OR
depends on baseline pixels already being present outside the sprite mask;
local byte algebra does not prove overlapping actors or changing terrain.
Karateka's repair path is related to `GEN-0003`, not evidence of the same
baseline invariant. Test both against a reference scene before comparing cost.

### Phase tables versus runtime shifts and reflection

- [APPLE2-0002](../../../../../research/findings/APPLE2-0002-seven-phase-sprite-tables.md)
  uses seven pointer-table pages plus a shared pair dictionary. Recorded data
  total 2,816 bytes versus 1,792 bytes for direct two-byte outputs over the
  same checked domain. That difference is a data-layout hypothesis excluding
  decoder changes, not a whole-engine saving or measured speedup. Used IDs,
  tokens `$00–$7F`, phases `$00–$06` and the two-byte/three-byte screen paths
  still need a complete caller/data census.
- [APPLE2-0003](../../../../../research/findings/APPLE2-0003-runtime-sprite-shift-and-reflection.md)
  shares packed rows across phase and facing, using runtime shifts and a
  128-byte reflection table. Its checked seven-bit algebra excludes a universal
  bit-7/color contract; clipping, zero sizes, reflected anchors and composition
  need whole-image tests. Component sizes are not the full engine cost.

Neither source demonstrates a fair end-to-end benchmark of these alternatives.
Oric's six-pixel data and in-band attributes require different tables/masks;
`ORIC-0003` is a comparison, not an interchangeable phase decoder.

### Composition patches and retained animation cursors

[Karateka C02](../../../../../research/analyses/karateka/cpu-techniques.md#c02-equal-width-composition-patches)
provides NOP/ORA/AND instances related to `CPU6502-0001`. Two-byte patches are
not atomic, and mode selection alone does not prove correct shifted masks,
layer order or colors. Compare dedicated workers after output/reentry checks.

[Karateka C06](../../../../../research/analyses/karateka/cpu-techniques.md#c06-retained-token-cursors-and-movement-sign)
adds retained horizontal/vertical streams related to `GEN-0001`. Restarts and
byte cursor wrap leave the per-call work bound unresolved. Its grammar is not
the Oric animation interpreter's grammar and is not a one-token-per-frame proof.

## Renderer validation matrix

- Test every phase `$00–$06`, both facing directions and all composition modes.
- Cover zero/minimum/maximum sizes, all edges and legal source-token/ID bounds.
- Compare pixels and bit-7/color results separately on the stated display output.
- Test overlapping actors, terrain changes and both page repair histories.
- Record actual page/bank state, scratch/code owners and patch ordering.
- Trace any display polling wait; a returning wait alone does not prove a new
  frame edge, sufficient drawing time or an IRQ-based animation system.
- Include complete code, tables, scratch, setup and draw workload in comparisons.
- Establish equivalent output before cycle measurements; retain emulator and
  real-hardware results separately. No current record completes this matrix.
