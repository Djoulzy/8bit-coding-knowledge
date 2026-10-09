---
id: REVIEW-ORIC-0001-INTEGRATION
program: "L'Aigle d'Or"
review_date: "2026-10-09"
source_revision: "sha256:7f01e1a3d05825aab887952cd5711bea69d6525730aba5c1e25c814334fe77d7"
review_scope: "Five finding records and all additional observations in findings.md"
---

# Knowledge-base integration review

## Decision and evidence standard

Promote three narrowly specified recommendations: a display-independent semantic
collision map, two-bit carry-stream extraction, and descending full-page RAM
copying. Keep animation streams, rendering patches, position-bearing background
buffers and the BASIC-header RTS alias under research. The historical collision
classifier also stays there; only its general representation principle moves
to validated guidance.

`validated` here means a recommendation supported for the explicit contract in
its document. It does not mean fastest, benchmarked, Oric-compatible in every
ROM, or validated as part of the complete game. Evidence combines source-byte
checks, documented CPU semantics where applicable, invariants proving the stated
behavior, independent functional oracles and an applicability/alternatives review.
No status was changed merely because a model passed.

The instructions in root AGENTS.md, `docs/cpu/6502/AGENTS.md` and the existing
`docs/machines/brand/Tangerine/Oric/AGENTS.md` were applied. No machine guideline
is promoted into the requested `docs/machines/oric/` destination this round;
the hardware/firmware conditions are unresolved. There is no reason to duplicate
the existing machine instructions or create speculative guidance there.

## Existing knowledge and duplication check

Inventory used `rg --files --hidden --no-ignore` and a topic search over `docs/`
and `templates/`. At review start, docs contained only the CPU and machine
AGENTS files; there were no technique guidelines to update, supersede or confirm.
The five research records and the original dossier were the relevant knowledge.
These techniques are new to this repository, not claimed historical inventions.

Canonical validated records now are:

| ID | Level / canonical document | Validated scope |
| --- | --- | --- |
| GEN-0002 | General 8-bit: [semantic-collision-grid.md](../../../docs/common/semantic-collision-grid.md) | Logical cell representation, bounded lookup and display independence |
| CPU6502-0003 | MOS 6502: [carry-stream-field-extraction.md](../../../docs/cpu/6502/carry-stream-field-extraction.md) | Four high-to-low two-bit fields; private destructive source and documented ISA |
| CPU6502-0004 | MOS 6502: [descending-page-copy.md](../../../docs/cpu/6502/descending-page-copy.md) | Full-page traversal/copy with aligned disjoint RAM and explicit count/state constraints |

GEN-0002 remains the technique's canonical ID. Its historical research record
has ID `RESEARCH-GEN-0002` and `technique_id: GEN-0002`, preserving unresolved
source observations without creating a second canonical guideline. CPU IDs
0003/0004 are assigned to previously documented C04/C06 observations; no duplicate
research technique descriptions were created. Navigation is in [docs/README.md](../../../docs/README.md).

## Review of each original finding

### GEN-0001: resumable animation streams

**Correctness:** the pointer selection, pre-incremented byte cursors, draw/restore
records, delta command and `$14/$16` event handoff match `$4500–$45FB`. The
equipment grammar differs from the movement grammar. A high-bit command byte
means restore; a high-bit sprite ID in the fourth draw field remains valid.

**Reuse and limitations:** the command/cursor architecture is reusable, but this
implementation has no proven bounds or per-call work limit. Cursor/ID wrap,
chaining without yielding, blocking `$15` delay, scratch reuse and drawing-layer
ownership remain material issues. A functional specification of a safer bounded
interpreter would be a separate implementation, not evidence this engine has it.

**Similar knowledge / level:** no prior docs equivalent. It relates to researched
save-under rendering but is an independent general 8-bit control architecture.
**Decision:** retain `analyzed` in [GEN-0001](../../findings/GEN-0001-resumable-animation-streams.md).
Trace reachable streams and worst-case return latency before promoting guidance
around this concrete implementation; benchmark only if recommending its cost.

### CPU6502-0001: two-byte rendering patches

**Correctness:** `$EAEA` gives two NOPs; `$6211` gives ORA through `$62/$63`,Y.
Both span two bytes, so later layout is stable. The following DEY defines the
inner-loop branch condition despite the modes' different N/Z effects. Conditional
read/page and branch cycle calculations remain theoretical.

**Reuse and limitations:** equal-width patching is a reusable CPU mechanism,
but neither exclusive execution during the two stores nor safe composition of
all Oric graphic/attribute bytes has been traced. The opaque NOPs retain four
cycles per byte that a dedicated loop could remove; no best-performance claim
is justified.

**Similar knowledge / level:** no prior equivalent; aligned tables/copy loops
do not replace its concurrency contract. CPU mechanics belong in 6502 docs,
with an Oric cross-reference for attribute restrictions. **Decision:** retain
`analyzed` in [CPU6502-0001](../../findings/CPU6502-0001-two-byte-render-patches.md).
Verify execution/patch order and output first, then compare equivalent renderers.

### ORIC-0001: position-bearing background pages

**Correctness:** metadata stores/loads at `$FE/$FF`, shared descriptors and
pointer-before-data traversal match the bytes. The six initial areas have
124/104/24/28/45/95 pixel bytes; offset 1 means capacity is at most 253 bytes
below metadata. Initial capacity alone does not prove every runtime resize safe.

**Reuse and limitations:** the embedded-position idea is general, but the full
implementation relies on Oric six-pixel columns, scanline stride and attributes.
Overlap restoration, composition mode during erase, `$0A` partial-row stopping,
zero height and `$5900` charset-buffer ownership remain unresolved.

**Similar knowledge / level:** related to GEN-0001, but neither the semantic
collision map nor the validated disjoint copy proves screen-layer correctness.
The original combination belongs at the Oric level, cross-referencing CPU
mechanisms; a future generic save-under record should avoid duplicating it.
**Decision:** retain [ORIC-0001](../../findings/ORIC-0001-background-pages-with-position-metadata.md)
as `analyzed`. Trace buffer lifetimes, overlap and attribute restoration on both
identified ROMs before hardware guidance or redraw benchmarks.

### GEN-0002: semantic collision map

**Correctness:** the 120-byte map is cleared/populated separately from the image;
the live pointer helper and movement probes read it. Review adds an implicit
flag contract: STA at `$4B82` preserves N, so BPL at `$4B85` consumes the caller's
N. Identified directional callers use LDA immediately before JSR. Passing A
alone is not a complete interface. The `$A0` result store after LDX=`$02` and
special y mapping also remain source-specific, not generic rules.

**Reuse and limitations:** independently defined cell properties decouple gameplay
from colors/artwork. Boundaries, index width, cell resolution and dynamic update
ownership must be explicit; coarse lookup cannot prove fine/swept collision.
This representation recommendation needs no timing benchmark because it makes
no speed ranking. An independently specified map is checked against logical-set
oracles, including boundaries, visual changes and logical updates.

**Similar knowledge / level:** no prior docs equivalent; rendering/animation
records concern different state. **Decision:** promote the bounded general
principle to [GEN-0002](../../../docs/common/semantic-collision-grid.md), `validated`.
Keep the historical semantics/flag/result questions in
[RESEARCH-GEN-0002](../../findings/GEN-0002-semantic-collision-grid.md), `analyzed`.

### CPU6502-0002: RTS in a BASIC header

**Correctness:** CALL 8835 targets `$2283`, which holds `$60`, the low byte of
line number 6240=`$1860`. RTS semantics explain the immediate return under the
normal CALL convention. The bytes do not prove deliberate optimization.

**Reuse and limitations:** no robust reusable recommendation is established.
Renumbering or relocating BASIC can change the instruction; retaining a no-op
CALL has unmeasured overhead and is unnecessary if it can simply be omitted.

**Similar knowledge / level:** no duplicate; this is a CPU instruction/data-layout
analysis example with an Oric BASIC dependency. **Decision:** retain
[CPU6502-0002](../../findings/CPU6502-0002-rts-in-basic-line-header.md) as `analyzed`
and not recommended. Recover original source/history or trace reachability to
resolve intent; a benchmark would not make the alias a sound guideline.

## Additional dossier observations: individual decisions

These observations already existed under research before this review. The two
CPU promotions below do not imply the rest of their larger routines is validated.
All rows have no pre-existing docs equivalent; related knowledge refers to the
records above or the new canonical documents.

| Observation / appropriate level | Correctness, reuse and main limitation | Decision / related knowledge |
| --- | --- | --- |
| BASIC controller / machine workers — General | Division of work established; reusable, but interpreter overhead and shared ABI unmeasured | Keep analyzed; related GEN-0001 |
| Fixed phase-dependent ownership — General | Address/lifetime ledger useful; complete live overlap and heap peaks untraced | Keep analyzed; related ORIC-0001 |
| Packed room records — General | 64 × 8 bytes and bit extraction established; several field meanings/transitions still game-specific | Keep analyzed; CPU6502-0003 covers only extraction |
| Replay snapshot — General | Room-page transfer understood; full replay state depends on BASIC initialization | Keep analyzed usage; copy worker covered by CPU6502-0004 |
| Zero-page pointer arguments — MOS 6502 | Indexed pointer mechanics correct; reentrancy and firmware ownership unverified | Keep analyzed; no blanket address-allocation advice |
| Four aligned field arrays — MOS 6502 | Page/index bound and 37-cycle descriptor lookup understood; memory/alternative trade-off unmeasured | Keep analyzed; could later validate a scoped table-layout recommendation |
| Carry-stream extraction — MOS 6502 | Two rotations per field, destructive source; incoming C cannot contaminate the four original fields | Promote CPU6502-0003 with exact bit/flag/ownership scope |
| Shift/add multiply — MOS 6502 | Binary model exhaustive; D requirement and constant-stride cost constrain use | Keep analyzed; compare constant-specific alternatives before speed guidance |
| Bounded ADC carry reuse — MOS 6502 | High sum cannot overflow, TYA preserves C; proof depends on the exact operand domain | Keep analyzed; needs a separate scoped record before promotion |
| Full-page countdown copy — MOS 6502 | Unique 256-byte traversal and disjoint copying proven; zero/count/alias rules essential | Promote CPU6502-0004; sprite row/clipping loops remain analyzed |
| Tail-jump wrappers — MOS 6502 | Normal return-stack behavior understood; live argument/clobber contracts matter | Keep analyzed; no standalone guideline prepared this round |
| Sign-flag range shortcuts — MOS 6502 | Byte behavior understood; N after CMP is not a universal comparison predicate | Keep analyzed; caller ranges require checking |
| Charset loop branch crossing — MOS 6502 | 255 taken-page penalties established theoretically; relocation benefit not measured | Keep analyzed; benchmark a separate experimental image |
| Six-pixel sprites — Oric | Byte units/stride documented; unclipped writes and full display paths need tracing | Keep analyzed; future destination `docs/machines/oric/` |
| Attribute column / `$0A` stop — Oric | Stores and stop test established; partial-row/zero-height effects unresolved | Keep analyzed; related ORIC-0001 |
| Charset preservation / mode overlays — Oric | Exact 256-byte save/restore ranges known; ROM effects and buffer ownership unresolved | Keep analyzed; related ORIC-0001 |
| VIA latch changes — Oric | Register writes are latch updates; ACR/phase/IRQ frequency and pacing effects untraced | Keep analyzed; no frame-rate recommendation |
| Firmware sound — Oric | BASIC command use established; timing, ROM clobbers and direct-driver comparison absent | Keep analyzed; no custom AY optimization to promote |
| Key / line-number table dispatch — General plus Oric input | Table contains BASIC line numbers, default 21845 is real; key domain and total dispatch cost untested | Keep analyzed; distinguish from machine jump table |
| ROM-entry adaptation — Oric | One-byte `$F89B`→`$F8D0` patch established; exact ROM compatibility unverified | Keep analyzed; test both firmware checksums |
| Two-byte saved hazard — General strategy / Oric pixels | Local byte traffic understood; overlap and visible inverse-data effect state-dependent | Keep analyzed; related ORIC-0001 |
| Sentinel message strings — General | Backslash termination understood; scanning/bounds/escaping and CHAR costs constrain reuse | Keep analyzed; no duplicate record needed |

## Why the CPU recommendations qualify

For CPU6502-0003, the source-byte chain is checked, documented ROL semantics
support a bit-flow proof, and all 256 input bytes with either incoming C are
compared against independent mask/shift expressions for a single field and all
four fields. The guideline defines scratch/flag clobbers and alternatives; it
does not claim measured superiority or validate the entire room decoder.

For CPU6502-0004, documented load/store/DEY/branch semantics and the modulo-256
index bijection prove complete traversal. Whole-array comparisons with a source
snapshot verify copy effects and absence of outside writes in the abstract RAM
model. Contract checks reject overlap, zero/oversized count, misalignment and
range wrap. On real hardware, pointers/code/stack/IRQ ownership are additional
explicit preconditions, not properties the model claims to establish.

## Verification and reproducibility

Run from the repository root using Python 3.9+:

```sh
python3 research/analyses/laigle-dor/tools/verify_integration.py
```

The command reruns the original preservation/arithmetic checks, ties new models
to exact helper bytes, and reports:

| Evidence | Result |
| --- | --- |
| Original TAP/extractions and baseline checks | Pass; original SHA-256 unchanged |
| Semantic-grid queries | 3,560 cases; four layouts, four visual patterns, two logical states, boundary checks |
| Logical map updates | Four cases |
| Carry extraction | 512 single-call cases and 512 complete four-field sequences |
| Full-page copy | 16 cases; page counts 1/2/3/128, four data patterns, whole-RAM snapshot comparisons |
| Invalid copy contracts | Seven rejected |
| Historical game / CPU emulator / real hardware | Not executed |
| IRQ, ROM and comparative performance | Not validated or measured |

[integration-verification.json](integration-verification.json) stores results.
These are functional models and proofs, not benchmarks. CPU timing figures in
the guidelines remain instruction-table calculations with explicit conditions.

## Documentation changes and remaining work

Three template-based English guidelines were created, with provenance and links
to this dossier. Existing research records gained review decisions; GEN-0002
now distinguishes historical evidence from its canonical general guideline.
The classifier's implicit N contract was added to its record and CPU/routine
analysis. The overview/findings now link this later review. Existing policy
instructions and the user's `.gitignore` were not edited.

Priorities remain identified-ROM execution, animation latency/reachability,
zero-page and buffer ownership, overlap/attribute frames, then matched renderer
and constant-stride arithmetic benchmarks. Keep experiments separate from the
original TAP. Recover original source if possible to resolve dormant fragments
and the BASIC-header RTS intent. No source-code compatibility or performance
recommendation should be inferred from these three scoped promotions.
