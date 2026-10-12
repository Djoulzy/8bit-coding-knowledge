---
record_type: machine-topic-guide
topic: graphics
machines: ["oric-1", "oric-atmos"]
cpu: ["6502"]
status: mixed
review_date: "2026-10-11"
---

# Oric graphics, attributes and redraw strategies

This guide separates documented display constraints and one validated general
representation rule from historical rendering candidates. It does not claim a
validated fastest sprite, clipping, charset-animation or buffering method.

## Documented display constraints

### Preserve the pixel/attribute distinction

**Recommendation:** Classify every display byte handled by a renderer as pixel
data, a serial attribute or deliberately opaque preserved data. Keep attribute
columns and frame/control cells outside generic pixel composition unless their
encoding is an explicit part of the operation.

**Why:** Oric HIRES uses 40 bytes per scanline over 200 bitmap scanlines. A
graphic byte carries six visible pixel bits, while low-valued serial attributes
change ink, paper, charset or other interpretation for following cells. A byte
OR that is valid for two pixel values can turn a control byte into a different
control value.

**Prerequisites:** Known display mode, row layout, attribute placement and
clipping rules. Confirm whether the selected ROM/setup leaves bottom text rows
or charset regions live.

**Trade-offs:** Reserving attribute columns reduces drawable width and can add
mask/branch work. Treating complete bytes opaquely is simpler but can propagate
unintended color or charset state across a row.

**Porting/adaptation:** A renderer from a planar, bitmap-only or character-cell
machine needs a new byte classifier and row contract, not only a new screen
base. Conversely, Oric control values must not be copied as pixels to another
format.

**Evidence:** [Atmos-manual-backed hardware analysis](../../../../../research/analyses/laigle-dor/hardware-techniques.md#h01-byte-column-coordinates-and-six-pixel-alignment),
[attribute interaction](../../../../../research/analyses/laigle-dor/hardware-techniques.md#h02-attributes-emitted-beside-sprite-rows),
[independent Space: 1999 analysis](../../../../../research/analyses/space-1999/hardware-techniques.md#embedded-attributes-are-part-of-rendering).

### Plan TEXT, HIRES and charset memory by lifetime

**Recommendation:** Model screen, bottom text rows, character definitions,
saved backgrounds and overlay assets as phase-dependent owners. Do not count
overlapping display ranges as independent free buffers.

**Why:** The historical programs switch modes and reuse parts of the display,
charset and saved-background regions. *L'Aigle d'Or* reuses `$5900` for a
sprite background in one phase and a 256-byte charset save in another. Vip4
changes glyph data while fixed text codes remain visible. Correctness depends
on lifetime separation rather than the addresses merely being RAM.

**Prerequisites:** Exact mode transitions, ROM calls, charset selection,
interrupt activity and every concurrent buffer owner.

**Trade-offs:** Aggressive overlays save RAM but raise reset/error complexity
and make isolated routines non-reentrant. Dedicated buffers cost RAM but make
ownership and tests simpler.

**Evidence:** [L'Aigle d'Or display lifetimes](../../../../../research/analyses/laigle-dor/hardware-techniques.md#h04-texthires-overlays-and-charset-lifetimes),
[Vip4 memory ledger](../../../../../research/analyses/vip4-demo/architecture.md#memory-allocations-and-lifetime-reuse).

## Validated representation rule

### Keep cell collision state independent of display bytes

**Recommendation:** For cell-based movement, store named collision properties
in a bounded logical map derived from authoritative scene state. Rebuild or
update it under an explicit ownership contract when doors/objects change.

**Why:** Display pixels and serial attributes are not reliable gameplay state.
The canonical rule is validated for representation independence and bounded
row-major lookup; it makes no speed or pixel-precision claim.

**Prerequisites:** Defined cell dimensions, coordinate conversion, boundary
policy, index width and synchronization between scene changes and map readers.

**Trade-offs:** A byte map costs `width * height` bytes and can become stale.
Coarse cells do not replace silhouette or swept collision when gameplay needs
them.

**Porting/adaptation:** Select cell resolution from game rules, not the Oric's
six-pixel byte packing. The historical three-row perspective layout, special
cell values and caller flag contract are not reusable defaults.

**Evidence:** [GEN-0002](../../../../common/semantic-collision-grid.md),
[historical Oric record](../../../../../research/findings/GEN-0002-semantic-collision-grid.md),
[integration review](../../../../../research/analyses/laigle-dor/integration-review.md#gen-0002-semantic-collision-map).

## Candidates requiring validation

All items in this section are **experimental choices**, not best practices.

### Saved backgrounds versus scene recomposition

Two analyzed strategies solve different overlap problems:

| Strategy | Evidence | Potential benefit | Main constraints and required test |
| --- | --- | --- | --- |
| Position-bearing save-under pages | [ORIC-0001](../../../../../research/findings/ORIC-0001-background-pages-with-position-metadata.md) | Restore small moving layers without rebuilding a room; attributes saved with pixels | Six 256-byte pages in the historical design; `W*H <= 253`; test clipping, zero sizes, overlap order, buffer lifetimes and opaque restoration |
| Dirty-region scene recomposition | [GEN-0003](../../../../../research/findings/GEN-0003-clipped-scene-recomposition.md) | Recreate current overlaps/occlusion from scene state with 480 bytes of historical scratch | Dirty bounds and draw order must be exhaustive; historical six-byte stride/four-layer geometry is specialized; compare work in sparse and dense scenes |

Do not combine their recorded RAM figures into a speed conclusion. Compare
identical scenes, correctness oracles, maximum dirty areas, attribute handling
and total scene-state memory.

Apple II research supplies comparisons, not drop-in Oric renderers.
[Lode Runner H02](../../../../../research/analyses/lode-runner/hardware-techniques.md#h02--baseline-masked-restoration-and-overlap-analyzed-apple2-0001)
uses a persistent terrain page rather than per-sprite save-under.
[Karateka H04](../../../../../research/analyses/karateka/hardware-techniques.md#h04-alternating-pages-and-retained-repair-geometry)
retains repair geometry across alternating pages, unlike Space: 1999's small
offscreen recomposition area. Adapting either organization would require an
Oric memory-capacity and attribute-restoration experiment; Apple page addresses,
mask encoding and page-switch behavior cannot be reused as Oric assumptions.

### Parity-compressed screen-address tables

[ORIC-0003](../../../../../research/findings/ORIC-0003-parity-compressed-pixel-tables.md)
stores even-row offsets and even-X quotient/mask pairs, deriving odd coordinates.
The mathematical model covers all 48,000 legal pixel coordinates and the table
footprint is 440 bytes versus 880 for the stated full-table baseline. The actual
6502 routine, timing, out-of-range behavior and attribute-safe store remain
unvalidated. Benchmark it against full tables and sequential pointer stepping
at controlled code/data alignments before choosing it for speed.

### Shared-glyph charset animation

[ORIC-0002](../../../../../research/findings/ORIC-0002-masked-charset-bank-animation.md)
updates 256 glyph bytes while leaving 32 fixed text codes on screen. It may suit
repeated tiles or text effects, but all occurrences of a glyph change together.
The historical source bank, pointer low byte, overlay contents and display
synchronization are unresolved. A new design needs explicit charset ownership,
both pointer bytes initialized, a known frame bank and tear testing.

### Equal-width renderer patches

[CPU6502-0001](../../../../../research/findings/CPU6502-0001-two-byte-render-patches.md)
switches between two NOPs and `ORA (screen_pointer),Y`. It keeps following code
at stable addresses but retains four NOP cycles in opaque mode and cannot safely
patch while a consumer might execute either byte. Oric attribute bytes make OR
composition an additional machine-level risk. Compare one-dispatch separate
workers under identical pixel/attribute inputs before adopting it.

[Karateka C02](../../../../../research/analyses/karateka/cpu-techniques.md#c02-equal-width-composition-patches)
adds another analyzed instance: two-byte NOP, ORA and AND choices at two
renderer sites. This corroborates the patch-layout mechanism, not safe Oric
composition or atomic patching. Its seven-pixel HGR masks differ from Oric
six-pixel data and serial attributes; compare complete Oric output and patch
ownership before drawing a portability or performance conclusion.

### Resumable animation streams

[GEN-0001](../../../../../research/findings/GEN-0001-resumable-animation-streams.md)
combines draw, restore, relative movement and event commands with retained
cursors. The architecture is reusable, but the historical interpreter lacks
proved length checks and a per-call budget. Validate every reachable stream,
cursor wrap, chain/yield latency and layer ownership; specify a bounded grammar
for new data.

[Karateka C06](../../../../../research/analyses/karateka/cpu-techniques.md#c06-retained-token-cursors-and-movement-sign)
also retains horizontal/vertical token cursors, but restart commands and byte
index wrap leave the per-call work bound unresolved. This supports investigating
the general organization without validating either program's stream grammar.

## Graphics validation matrix

For every candidate renderer, record at least:

- Oric-1 versus Atmos and the exact ROM/mode initialization;
- all six sub-byte X phases where applicable, both mirror states and edge clips;
- pixel bytes adjacent to each relevant ink/paper/charset attribute;
- zero, minimum and maximum dimensions plus capacity failures;
- overlapping actors in both restore/draw orders or every scene layer order;
- mode/charset transitions and every aliased buffer lifetime;
- interrupt state, tearing/frame capture and emulator versus real hardware;
- code bytes, tables, scratch RAM, setup cost and elapsed cycles only after
  byte- or pixel-identical output is established.

No existing record completes this matrix.
