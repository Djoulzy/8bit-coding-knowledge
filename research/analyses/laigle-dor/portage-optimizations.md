---
record_type: porting-optimization-workbook
program: "L'Aigle d'Or — native Apple IIe port"
cpu: ["6502"]
machines: ["apple-iie"]
status: analyzed
benchmark_scope: "Matched instruction-cycle workloads in the functional Apple bus; no hardware timing measurement"
implementation_revision: "97c6f0dc78e9d3836e32f1a8880446f4c6e87b86"
review_date: "2026-10-19"
source_analyses: ["portage.md", "../../../ports/laigle-dor/apple-iie/docs/renderer-optimization.md", "../../../ports/laigle-dor/apple-iie/docs/input-responsiveness.md"]
tags: [porting, profiling, graphics, auxiliary-memory, caching, timing]
---

# Reusing the Apple IIe port's optimization mechanisms

## Scope and evidence

This companion to the [porting workbook](portage.md) explains how to reuse the
optimization process and mechanisms in another project. These are adaptations
implemented in the **modern Apple port**, not techniques attributed to the
original Oric author. The historical inputs remain unchanged.

The implementation uses ca65/ld65 syntax, documented NMOS 6502 instructions,
128 KiB with MAIN/AUX RAM, two alternating frame pages and a retained terrain
baseline. HGR mono and DHGR share rules but have different packing and resource
budgets. See the [project profile and build chain](../../../ports/laigle-dor/apple-iie/README.md)
and [exact renderer allocation](../../../ports/laigle-dor/apple-iie/docs/renderer-optimization.md).
Addresses below identify this implementation; they are not free-memory
recommendations for another game, loader or operating system.

The mechanisms are **analyzed**. The combined renderer change is
**benchmarked within the functional model** using matched instruction-cycle
workloads. Individual mechanisms were not benchmarked in isolation. These
results do not establish a universally fastest renderer or promote a new
validated guideline. Binary/disk hashes and executed checks are pinned in the
[verification record](../../../ports/laigle-dor/apple-iie/docs/renderer-verification.json).
No new Virtual II or physical-machine timing run was made in that pass.

## A repeatable optimization workflow

1. **Freeze the comparison.** Preserve the old binary, disk, linker labels,
   asset hashes, configuration and profiler. Record the intended visual and
   gameplay behavior before changing its representation.
2. **Measure the complete response.** Record input arrival, strobe consumption,
   state update and first affected page flip separately. Inject commands both
   before and just after polling; cover idle, walking, equipment and modal
   screens. Separate steady-room cost from loading and scene construction.
3. **Choose the expensive work.** Profile setup, decoding, bank transfers,
   composition, restoration, HUD and synchronization. Routine totals may be
   inclusive: do not add a renderer's time to the time of its children.
4. **Budget the alternative before implementing it.** Include executable code,
   headers, pointers, masks, shared rows, alignment, scratch, both display pages,
   baselines and loader/firmware ownership. Select a subset of hot assets if
   converting everything would exceed the budget.
5. **Prove equivalent output, then compare cycles.** Retain an independent
   reference compositor; exercise all phases, clipping, both banks, overlaps,
   page history and modal returns. Check gameplay cadence as well as pixels.
6. **Record what improved and what remains.** Archive the new reports with
   hashes, the exact scenarios, memory costs and untested environments. A
   component-level speed claim needs a separate controlled comparison.

In this case the original stationary room-12 renderer consumed about 97–98%
of the loop, while command decoding was a small fraction. Optimizing keyboard
decoding alone would therefore leave most of the delay. Double buffering hides
construction but does not execute rendering and polling concurrently. The
[input report](../../../ports/laigle-dor/apple-iie/docs/input-responsiveness.md)
contains the original diagnosis and the executable profiler.

## Reusable mechanisms

### 1. Compile source graphics into native masked rows

**Level:** general preprocessing technique, with Apple-specific output packing.
**Implementation:** [`compile_sprites`](../../../ports/laigle-dor/apple-iie/tools/native_sprites.py)
and [`draw_native_sprite`](../../../ports/laigle-dor/apple-iie/src/apple/native-sprites.s).

Move source-format interpretation to the host build. Emit interleaved mask/pixel
fragments in the target's seven-bit pixel field, with `pixels & ~mask == 0`.
For those pixel bits, composition is `(destination & ~mask) | pixels`; bit 7
and color interpretation retain their separate target contract. Identical
mask/pixel scanlines share immutable records. Each sprite row references its
record through a two-byte pointer; source row order remains explicit.

This removes repeated cell/status decoding without storing a complete image
for every room or horizontal phase. It suits frequently drawn sprites with
repeated rows. Pointer traffic, masks and headers can outweigh deduplication
for small or mostly unique data; compare **total linked size**, not just the
number of unique rows. Shared records must never be modified while composing.

The port converts all 60 mono actors, but only DHGR actor IDs 40–61 and flame
IDs 36/37/72/73. Other DHGR actor/equipment/enemy images retain the compact cell
decoder to fit AUX memory. This mixed representation is intentional. Fast flames
serve the existing non-additive wall/hand paths; additive scenery retains its
general renderer. Source-row overlap and flame row sampling must remain
equivalent when replacing a decoder.

**Reuse gate:** compare every live frame, transparency/color status, phase and
edge against a reference that does not decode the new native asset format.
Record bounds and reject oversized rows in the compiler; this implementation
limits an interleaved row to 128 bytes of scratch.

### 2. Replace repeated shifts with a small phase-specific table

**Level:** MOS 6502 lookup-table technique specialized to Apple seven-bit pixels.
**Implementation:** `draw_native_sprite`, `@power` / `@table` in
[`native-sprites.s`](../../../ports/laigle-dor/apple-iie/src/apple/native-sprites.s).

For a horizontal phase `p` in 0–6, build one 128-entry seven-bit rotation table.
Let `step = 1 << p`; start at zero, then advance by `step`, subtracting 127
whenever the sum reaches 128. This retains both zero and the distinct all-one
value `$7F`. For token `t` in 0–127, the result is:

```text
r = ((t << p) | (t >> (7 - p))) & $7F
spill_mask = (1 << p) - 1
current_byte_part = r & ($7F XOR spill_mask)
next_byte_part    = r & spill_mask
```

Apply the split to both opacity and pixels, joining the previous fragment's
spill with the next fragment. Rebuilding the table once per sprite replaces
repeated bit/cell shifting with indexed byte lookups. The table occupies MAIN
`$0200–$027F`; its alignment and bounded indices keep those indexed table reads
within one page. The implementation uses binary ADC/SBC, so D must be clear;
registers, flags and scratch are local renderer state, not a reentrant API.

The setup cost can dominate tiny sprites. Alternatives include keeping tables
for several phases, phase-specialized code or fully pre-shifted frames. Each
spends different code/data/setup costs. The present table is rebuilt each call,
so reuse of its scratch by disk operations cannot leave a stale phase table.
Caching it would require a new invalidation contract.

**Reuse gate:** check all 128 tokens and seven phases, zero/all-one endpoints,
adjacent-byte joins, mask spill and output edges. Seven-bit packing is essential;
an Oric six-pixel format or another target needs different algebra. Exhaustive
scalar algebra checks are a useful additional test for an extracted library;
the current port's executed coverage is the actor/phase and edge matrix below.

### 3. Batch transfers across a bank boundary

**Level:** general batching principle; this worker is Apple IIe-specific.
**Implementation:** `aux_read_row` / `aux_copy_span` in
[`dhgr.s`](../../../ports/laigle-dor/apple-iie/src/apple/dhgr.s), segment `AUXREAD`.

Copy an entire source row from AUX to MAIN scratch, then compose from MAIN.
This amortizes the bank-switch and call overhead that a per-resource-byte read
would pay repeatedly. The worker executes in MAIN zero page with ALTZP off,
keeping its code, pointers and stack accessible while RAMRD selects AUX.
`aux_read_row` leaves writes in MAIN and fills `$0280–$02FF`.

For AUX-to-AUX background copies, `aux_copy_span` selects AUX reads and writes
for the span, then restores both to MAIN. The renderer establishes 80STORE off;
bank/address state is part of the interface. The zero-page workers start at
`$0040`, remain below `$0080`, and are reinstalled after each BOOT0 disk read.
The loader also owns low-memory scratch, so a one-time installation is unsafe.

**Reuse gate:** document entry/exit bank state, code/stack/pointer locations,
maximum transfer size, loader clobbers and interrupt/reentry policy. Verify
actual mappings, not just distinct numeric addresses. The functional execution
does not validate arbitrary firmware or interrupt coexistence. Reallocate this
worker for a new environment instead of copying its addresses blindly.

### 4. Restore contiguous spans, keeping each page's history

**Level:** general dirty-region restoration with Apple DHGR bank splitting.
**Implementation:** `repair_rectangle` in
[`dhgr.s`](../../../ports/laigle-dor/apple-iie/src/apple/dhgr.s).

Retain the terrain baseline and restore only each hidden page's previous dirty
rectangle before drawing its changed actors. For a DHGR half-open serial-byte
interval `[left, right)`, even serial indices belong to AUX and odd ones to MAIN:

| Bank | Contiguous half-open byte interval |
| --- | --- |
| MAIN | `[floor(left / 2), floor(right / 2))` |
| AUX | `[ceil(left / 2), ceil(right / 2))` |

Copy the two spans separately and skip empty spans. This avoids selecting a
bank for each alternating serial byte. Mono uses an ordinary contiguous MAIN
span. Rows still use the target scanline mapping; these formulas do not make
the whole HGR screen linear or make overlapping copies safe.

**Reuse gate:** test odd/even endpoints, single-byte and empty spans, all edges
and both frame histories. A retained baseline must be updated when terrain
changes. Restore/draw ordering must account for every overlapping actor/effect.
The visible page, hidden page and baseline are three different owners.

### 5. Cache unchanged composition per display page

**Level:** general rendering technique.
**Implementation:** [`actor_cache`](../../../ports/laigle-dor/apple-iie/src/apple/actor-cache.s).

A double-buffered screen contains two different histories. Cache x, y, facing
and frame **for each page**, and reuse only the page whose pixels and scene
dependencies still match. A hit skips actor repair and redraw but retains the
dirty rectangle needed for its next movement. Flame and HUD work continues.

The actual eight-byte cache is deliberately conservative: play mode, stationary,
empty hand, no staged action, enemy, hazard or pit; illuminated scene, valid
dirty history and no pending terrain update on that page. The actor must be in
`8 <= x < 28`, excluding overlap with the two wall flames in this game's layout.
That coordinate guard is **not portable geometry**. For another scene, derive
an overlap/dependency test or reject reuse whenever an intersecting layer changes.

**Reuse gate:** compare cached output with forced recomposition over alternating
pages. Invalidate for terrain changes, lighting, new equipment, overlaps and
any modal/map screen that overwrites or changes the meaning of the page. An
unchanged actor is insufficient if another writer touched its pixels. HUD
caching and a generalized multi-actor cache are not implemented here.

### 6. Prevent faster rendering from accelerating periodic game costs

**Level:** general scheduling separation; the sampled clock is Apple IIe-specific.
**Implementation:** `clock_sample` / `clock_reset` in
[`service-clock.s`](../../../ports/laigle-dor/apple-iie/src/apple/service-clock.s),
consumed by `full_clock` in
[`full-core.s`](../../../ports/laigle-dor/apple-iie/src/game/full-core.s).

When resource wear is charged once per rendered loop, a faster renderer changes
gameplay. This port charges ordinary energy drain and held-torch wear every
**18 observed refreshes**, approximately 300 ms at 60 Hz. It samples RDVBLBAR
`$C019` at rendering service points, counts entry into blank, keeps the remainder
and caps pending refreshes at 35. Menus/help discard pending time; room loading
resets the clock, avoiding a resource penalty during those operations.

This is a target cadence, not recovered Oric timing or a complete fixed-step
simulation. Walking, staged actions, enemy/hazard logic and flame phase still
advance per controller loop and can speed up. Refresh-based durations also vary
with video standard. Sampled state cannot recover unobserved transitions: long
blocking operations or missed blank intervals require their own policy. The cap
deliberately bounds catch-up rather than guaranteeing all elapsed time is kept.

`clock_sample` preserves A/X/Y but not flags. Service calls must not interrupt a
live carry/comparison chain; D remains a caller contract for subsequent binary
arithmetic. The next project should decide separately which systems use elapsed
time, which react immediately, and which pause in menus or loading.

**Reuse gate:** compare counted refresh crossings with resource decrements and
remaining ticks, then test pauses and return. Test longer draws, sound/disk
blocking, alternate refresh rates and accelerators before a broader timing claim.

### 7. Recover memory by representation and lifetime, not assumed free addresses

**Level:** general allocation discipline, with Apple bank/firmware constraints.
**Implementation:** [`full-memory.inc`](../../../ports/laigle-dor/apple-iie/src/game/full-memory.inc),
[`game_resources.py`](../../../ports/laigle-dor/apple-iie/tools/game_resources.py),
[`full.cfg`](../../../ports/laigle-dor/apple-iie/src/full.cfg) and
[`full-mono.cfg`](../../../ports/laigle-dor/apple-iie/src/full-mono.cfg).

The native format was fitted by selecting hot DHGR sprites, sharing identical
rows, removing unused pointer slots/raw clue copies and moving compact end-screen
text to the existing AUX text-script engine. These reduce representation costs
without introducing per-room rendered images. They do not prove that arbitrary
unused-looking bytes or pointer IDs are safe to remove.

Maintain an ownership ledger with **bank, address, length, lifetime, writer,
clobbering service and reload policy**. Here MAIN `$0200–$02FF` is temporary
table/row scratch, while the DHGR extra row pool occupies AUX `$0C00–$13FF`.
Both AUX text pages `$0400–$0BFF` are excluded from resource storage. The MAIN
BOOT0 workspace/GCR table is also preserved. Linker separation alone cannot
catch a runtime HUD, firmware or loader write to an immutable asset.

**Reuse gate:** test resource immutability after HUD/menu/map/disk operations,
check actual linked bounds and preserve a loader contract. End-screen layout
and live gold checks ensure the text relocation preserves visible behavior.

## Relationship to existing knowledge

This is a port-specific reuse guide, not a set of duplicate technique records.

| Existing record | Relationship and boundary |
| --- | --- |
| [GEN-0002: semantic collision grid](../../../docs/common/semantic-collision-grid.md) | Validated separation of logical state and display. Renderer changes must preserve this separation; pixel equivalence alone does not prove gameplay equivalence. |
| [GEN-0003: clipped recomposition](../../findings/GEN-0003-clipped-scene-recomposition.md) | Related analyzed dirty-region approach. It recomposes intersecting scene content; this port restores a retained baseline and conservatively reuses actor pixels per page. |
| [APPLE2-0001: paired background masks](../../findings/APPLE2-0001-paired-hires-background-masks.md) | Related analyzed terrain/mask invariant. Its historical second-page role differs from two alternating display pages plus a separate baseline. |
| [APPLE2-0002: seven-phase tables](../../findings/APPLE2-0002-seven-phase-sprite-tables.md) / [APPLE2-0003: runtime shifts](../../findings/APPLE2-0003-runtime-sprite-shift-and-reflection.md) | Analyzed alternatives to the small rebuilt rotation table. Their token formats, reflection and setup differ; the present measurements do not rank those historical engines. |
| [CPU6502-0004: descending page copy](../../../docs/cpu/6502/descending-page-copy.md) | Validated only for its complete disjoint-page contract. It does not prove partial span copies or changing bank mappings. |
| [Apple memory guide](<../../../docs/machines/Apple/Apple IIe/guidelines/cpu-and-memory.md>) / [graphics guide](<../../../docs/machines/Apple/Apple IIe/guidelines/graphics.md>) | Existing bank ownership, phase, page-history and verification constraints. This port provides additional scoped execution evidence, without changing their validation status. |

## Measured outcomes and acceptance tests

The same thirteen scenarios ran against archived and optimized builds. The
following values are **executed CPU instruction cycles**, including the modeled
VBL wait. At exactly 1 MHz, dividing by 1,000 gives estimated milliseconds.
They exclude host keyboard delay, monitor scanout and room/disk construction.
Page flip marks image submission, not the time each pixel becomes visible.

| Scenario | DHGR before → after | HGR mono before → after |
| --- | ---: | ---: |
| Warm room-12 stationary loop, first sample | 289,516 → 85,134 | 306,546 → 51,108 |
| Turn arriving just after idle polling, to affected flip | 595,931 → 340,435 | 647,024 → 204,201 |
| Turn right already pending, to flip | 272,391 → 221,215 | 289,424 → 136,094 |
| Stop arriving just after walking polling, to flip | 544,840 → 459,640 | 595,928 → 272,340 |

Idle loops improved more than moving frames because the actor cache applies
only under its restrictive conditions. These samples are not worst-case bounds
and cannot assign a separate speedup to each mechanism.

| Acceptance condition | Executed evidence from this port |
| --- | --- |
| Native and fallback drawing preserve the chosen artwork | All 60 actors × seven phases per edition (420 comparisons), plus existing edge/flame tests |
| Cached pages equal forced recomposition | Both page histories, cache boundaries, equipment/enemy/pit exclusions, darkness and AUX pool immutability |
| No writes to the displayed graphics/text page | Functional bus write checks during draw/presentation scenarios |
| Room construction and gameplay remain covered | 64 room constructors per edition and full-game rule/UI regressions |
| Wear follows the clock and pauses | Refresh crossings versus energy/torch loss and remainder; help entry/idle/exit |
| Data relocation preserves UI | End panels retain text placement and current gold |

The [new rendering tests](../../../ports/laigle-dor/apple-iie/tests/render_optimization_cases.py)
are mixed into [the full-game suite](../../../ports/laigle-dor/apple-iie/tests/world_port.py).
The recorded pass comprised **45 DHGR and 46 mono full-suite tests**, then
three supplemental tests per edition including later assertions. A later
collection can therefore contain more cases than those archived full reports.
This is executed py65/functional-bus evidence, including Disk II BOOT0
instructions; the comparison with historical rules still has its own limits.

### Reproduction

From `ports/laigle-dor/apple-iie/`, with the prerequisites and pinned inputs in
the project README:

```sh
make games
python3 tools/check_game.py --video dhgr
python3 tools/check_game.py --video mono
python3 tools/profile_input.py --video dhgr
python3 tools/profile_input.py --video mono
python3 tools/profile_input.py --video dhgr --directory build/latency-baseline/dhgr
python3 tools/profile_input.py --video mono --directory build/latency-baseline/mono
```

The last two commands require the archived baseline directories, including
their own `game.bin`, `game.lbl` and `laigle-dor.do`. Do not replace the old
binary with a rebuild of the optimized source. Keep the original twelve-scenario
diagnostic reports separate from the matched thirteen-scenario comparison.
Reprofiling a later revision produces new evidence; it does not reproduce the
archived hashes by definition. The profiler writes reports, not game binaries
or disk images.

### Next experiments for another project

- Benchmark compact decoding, native rows and pre-shifted frames on identical
  scenes, including setup, bank traffic, code size and all asset/scratch bytes.
- Expand cache eligibility only after overlap and invalidation tests; measure
  whether a HUD cache provides enough benefit to justify its extra state.
- Consider buffered input at bounded service points, defining repeat, overflow,
  modal return and staged-action policies. This port has no new input queue.
- Separate the remaining simulation systems from rendering if stable gameplay
  pace is required, with an explicit source-versus-target timing decision.
- Measure input response and verify displayed colors/tearing on the identified
  emulator and hardware configuration. Functional cycle counts alone do not
  establish that result.
