---
id: RESEARCH-GEN-0002
technique_id: GEN-0002
title: "Historical Oric collision grid: cell semantics and caller contracts"
category: collision
cpu: ["6502"]
machines: ["oric-1", "oric-atmos"]
status: analyzed
source_analyses: ["../analyses/laigle-dor/overview.md"]
tags: [collision, semantic-map, packed-world, perspective]
promoted_to: "../../docs/common/semantic-collision-grid.md"
promotion_decision: "general-principle-promoted; historical implementation remains analyzed"
integration_review: "../analyses/laigle-dor/integration-review.md"
---

# Semantic collision grid separate from pixels

## Summary

This record retains the **historical Oric implementation observations** and
unresolved contracts. The general representation principle is now canonical
[GEN-0002](../../docs/common/semantic-collision-grid.md), validated only for
bounded cell lookup independent of display data. The game's three-row mapping,
cell taxonomy and movement behavior remain `analyzed` here.

## Problem and context

- **Problem being solved:** apply room/door/object rules without reading and
  interpreting a bitmap or repeatedly reconstructing geometry.
- **Typical use cases:** constrained perspective rooms and coarse movement.
- **Assumptions / preconditions:** graphics and semantic map generated from
  consistent room state; actor positions satisfy the map's coarse movement model.
- **CPU variants and target machines:** general algorithm; original decoder and
  probes use documented NMOS 6502 on Oric.

## Provenance

| Field | Value |
| --- | --- |
| Original program | L'Aigle d'Or, AIGLEDOR.2 |
| Author / publisher | Loader credits ROCQUES Louis-Marie; Loriciels, March 1984 |
| Source URL / archive | Download origin unknown; [local TAP](<../sources/Oric/L'Aigle d'Or/Aigle D'or, Le (1984)(Loriciels).tap>) |
| License / usage conditions | No license grant found; reproduction restriction in loader |
| Source revision / checksum | TAP SHA-256 `7f01e1a3d05825aab887952cd5711bea69d6525730aba5c1e25c814334fe77d7` |
| File and routine | B2 map clear `$3F14`; BASIC 5, 600–940; classification `$4B82–$4BA9`, pointer `$4CB6–$4CDC`, probes `$4BAD–$4CB2` |
| Line range / symbols / address | Classifier TAP `$0080E8–$00810F`; pointer `$00821C–$008242`; BASIC line locations retained in [listing](../analyses/laigle-dor/extracted/aigledor.2.basic.txt) |
| First analysis | [State/memory architecture](../analyses/laigle-dor/architecture.md#runtime-ownership-and-allocations) |

## Original implementation

Original assembler dialect is unknown. The reconstructed relationship is:

```text
packed room records -> room fields -> image construction
                                   -> 3 x 40 semantic cells at $0400-$0477
actor x/y + facing -> map pointer -> directional span probes -> result flags
```

The map is cleared when decoding a room. BASIC line 5 writes three consecutive
cells at `X+1 ... X+3`, and room/object routines mark specific spans. This is
not a pixel-perfect collision mask or a uniformly sampled 200-line tile map.

## Technical explanation

The live pointer helper begins at `$0400`, adds `$50` if actor y is `$8C`, adds
`$28` if y is `$A0`, then adds the actor's byte-column x. Other y values retain
the base row. This peculiar mapping follows the room's constrained perspective
movement positions; it must not be generalized as `row = y / constant`.

Directional routines inspect small spans and special door positions. The cell
classifier marks high-bit values blocked, treats `$A0` specially depending on
treasure state `$048F`, and sets feature flag `$04C4` for cell `$01`. `$04C0`
communicates collision; other fields carry door/obstacle state. The `$A0` path
loads X=`$02` but stores A=`$A0` into `$04C0`, not 2. Nonzero may suffice for
its callers, but exact result semantics need tracing.

The first BPL at `$4B85` consumes the caller's N flag: the preceding STA at
`$4B82` does not set it. Identified directional call sites load the cell with
LDA immediately before JSR, establishing N from A. A new caller cannot assume
passing A alone supplies this contract; the general guideline avoids it.

The likely motivation is separating visual detail from gameplay decisions while
keeping the collision state small. Packed persistent records and the regenerated
map have different jobs: the former retain room state, the latter accelerate
current-room queries.

## CPU-specific considerations

- **Registers and flags:** X adds grid offsets; A classifies cells; Y steps
  probe spans. The initial negative test requires caller N to match A's bit 7.
- **Addressing modes:** pointer `$78/$79` with `(zp),Y`, absolute actor/door state.
- **Instruction compatibility:** documented NMOS instructions; replace with
  equivalent indexed accesses on another CPU.
- **Page boundaries, branch timing, interrupts:** probe length/branches vary;
  no cycle benchmark or constant-time contract is asserted.
- **Code and data alignment:** map starts at `$0400`, but probes still require
  direction-specific bounds; aligned storage alone does not prove safety.

## Machine-specific considerations

The original x units match Oric six-pixel byte columns. Separating the map avoids
having to interpret ink/paper attributes and sprite pixels as obstacles. The
three-row perspective mapping is game-specific, not a requirement of Oric.

## Performance and resource costs

| Metric | Original | Alternative | Evidence / method |
| --- | --- | --- | --- |
| CPU cycles | Not measured; small directional probes | Pixel testing / object list not measured | Static paths |
| Code size | Multiple shared probe/door helpers; no isolated total asserted | Unknown | `$4B40–$4DC4` includes other work |
| RAM / zero-page usage | 120 map bytes; shared two-byte pointer plus result/state | Unknown | Clear loop and address helper |
| ROM usage | BASIC helps construct rooms; machine probes make no direct ROM call | Unknown | Source paths |

## Advantages

- Collision rules remain stable when artwork or color attributes change.
- Small current-room map avoids scanning an 8,000-byte display.
- Semantic values carry object/door meaning in addition to blocked/free state.

## Limitations and risks

- Coarse cells cannot resolve detailed silhouettes or arbitrary y positions.
- Graphics, packed state and grid can diverge after object changes.
- Hard-coded door locations and noncanonical result values complicate reuse.
- Bounds and special-case handling need execution across all room classes.

## Alternatives

Use an object list for few interactables, tile flags for a regular world, or
separate coarse movement and fine sprite masks. Choose resolution from gameplay
rules; derive graphics and collision from one authoritative scene description.

## Validation record

- **Current status:** analyzed for this historical implementation; the narrower
  platform-independent recommendation is validated in the canonical guideline.
- **Source-based evidence:** map initialization/population, live pointer helper,
  directional probes, result writes and door-state checks.
- **Theoretical analysis:** cell representation and special y mapping decoded.
- **Benchmark setup / commands / environment:** none; static inspection through
  the supplied TAP inspection tool.
- **Expected result versus actual result:** decoded pointer/classifier behavior
  matches the descriptions; all rooms/actions were not runtime-tested.
- **Real-hardware confirmation:** none.
- **Outstanding questions:** complete cell taxonomy, stale-map updates,
  bounds at room edges, `$A0` result contract and older inactive helper `$4B50`.

## Recommendation for new projects

Follow [GEN-0002](../../docs/common/semantic-collision-grid.md) for the general
map design. Do not transplant this implementation's perspective mapping,
implicit N contract or `$A0` result handling without additional verification.

## References and related techniques

- [Room packing and state](../analyses/laigle-dor/architecture.md#packed-room-data).
- [Collision routine inventory](../analyses/laigle-dor/routines.md#6502-room-animation-enemies-and-collision).
- [Suspicious instruction sequences](../analyses/laigle-dor/cpu-techniques.md#c07-branch-flags-signed-ranges-and-suspicious-sequences).
- [Integration decision and validation scope](../analyses/laigle-dor/integration-review.md).
- No equivalent repository record existed; semantic collision maps are
  established practice elsewhere and are not claimed as a new invention.
