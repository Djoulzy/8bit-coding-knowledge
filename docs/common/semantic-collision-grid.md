---
id: GEN-0002
title: "Semantic collision grids independent of display pixels"
category: collision
cpu: []
machines: []
status: validated
validation_scope: "Bounded cell lookup and separation of logical collision state from display data; no speed or historical-engine claim"
source_analyses: ["../../research/analyses/laigle-dor/overview.md"]
tags: [collision, semantic-map, bounds, state-ownership]
review_date: "2026-10-09"
---

# Semantic collision grids

## Summary

Store collision properties in a logical cell map independently of the image
being displayed. This is a validated representation choice for cell-based
movement: changing artwork cannot change collision results unless logical state
also changes. Performance superiority and pixel-perfect collision are outside
this recommendation's scope.

## Problem and context

- **Problem being solved:** visual bytes, colors and animation layers are poor
  authoritative representations of doors, obstacles and interactable objects.
- **Typical use cases:** rooms, tile worlds and movement on defined coarse cells.
- **Assumptions / preconditions:** positive dimensions, representable indices,
  allocated map storage, explicit coordinate conversion and synchronized updates.
- **CPU variants and target machines:** processor-independent; cell size and
  address arithmetic must fit the chosen implementation.

## Provenance

| Field | Value |
| --- | --- |
| Original program | L'Aigle d'Or, AIGLEDOR.2 |
| Author / publisher | Loader credits ROCQUES Louis-Marie; Loriciels, March 1984 |
| Source URL / archive | Download origin unknown; [local TAP](<../../research/sources/Oric/L'Aigle d'Or/Aigle D'or, Le (1984)(Loriciels).tap>) |
| License / usage conditions | No license grant found; original loader contains a reproduction restriction |
| Source revision / checksum | TAP SHA-256 `7f01e1a3d05825aab887952cd5711bea69d6525730aba5c1e25c814334fe77d7` |
| File and routine | B2 map clear `$3F14`; BASIC 5, 600–940; probes `$4BAD–$4CB2` |
| Line range / symbols / address | Classifier `$4B82–$4BA9`, TAP `$0080E8–$00810F`; pointer `$4CB6–$4CDC`, TAP `$00821C–$008242` |
| First analysis | [Architecture](../../research/analyses/laigle-dor/architecture.md#runtime-ownership-and-allocations) and [integration review](../../research/analyses/laigle-dor/integration-review.md) |

## Original implementation

The original uses three rows of 40 semantic bytes at `$0400–$0477`, populated
while rendering a room. Its special perspective y mapping, door rules and
noncanonical result values remain historical research. No assembler source or
dialect is available. See the [routine inventory](../../research/analyses/laigle-dor/routines.md#6502-room-animation-enemies-and-collision)
for those machine-specific details; do not import their constants into a new map.

## Technical explanation

Define cell properties from authoritative world state. Give collision queries
only the cell map and necessary logical state, not the display buffer. For a
row-major map, a valid cell has index `row * width + column`:

```text
if row < 0 or row >= height or column < 0 or column >= width:
    return BLOCKED                 # one explicit boundary policy
index = row * width + column       # arithmetic wide enough for width*height
return classify(cells[index])
```

Check bounds before forming an address. For valid coordinates the index is
between zero and `width*height - 1`, and each cell has a unique index. Since
the query's inputs exclude artwork, changing graphic bytes cannot affect its
result. Choose a different explicit boundary policy if gameplay needs it.

Use named properties and result types rather than relying on incidental values
being nonzero. Update or rebuild the map when a door/object changes. If queries
can run during rebuilding, define an update phase, snapshot or version contract
so readers do not observe a partly updated scene.

## CPU-specific considerations

- **Registers and flags:** not prescribed; they are implementation choices.
- **Addressing modes:** direct indexing, row pointers or row-offset tables.
- **Instruction compatibility:** no CPU-specific instruction requirement.
- **Page boundaries, branch timing, interrupts:** implementation-dependent;
  interrupt users must obey the same update/ownership contract.
- **Code and data alignment:** optional; allocation and integer width must cover
  the complete map without address wrap.

## Machine-specific considerations

Select cell resolution from gameplay, not from a display's attribute encoding.
On Oric this separates collisions from ink/paper attributes and software sprites.
The historical six-pixel x units and three perspective rows are not general rules.

## Performance and resource costs

| Metric | Original | Alternative | Evidence / method |
| --- | --- | --- | --- |
| CPU cycles | Not measured | Pixel masks/object lists not measured | No speed recommendation |
| Code size | Shared historical probe helpers; isolated size not asserted | Implementation-dependent | Source inventory |
| RAM / zero-page usage | Historical map: 120 bytes; example byte map: `width*height` bytes | Bitmaps or object lists may be smaller | Representation size, not a benchmark |
| ROM usage | Historical room construction uses BASIC | No ROM requirement for the general technique | Architecture separation |

## Advantages

- Visual changes do not implicitly alter gameplay rules.
- Properties can distinguish obstacles, hazards and interactable objects.
- Cell queries and boundary behavior can be tested independently of rendering.

## Limitations and risks

- Coarse cells cannot prove silhouette-level collisions or swept movement safety.
- Dynamic changes can leave the map stale if update rules are incomplete.
- Extra storage and rebuild work may outweigh the benefit for a few objects.
- A bounded lookup does not validate the coordinate conversion or movement rules.

## Alternatives

Use an object list for sparse interactions, bit masks for fine silhouettes, or
tile flags where the world is already a tile map. Combine coarse and fine tests
when gameplay requires both. Compare memory and query/update workload before
claiming a performance advantage.

## Validation record

- **Current status:** validated for representation and bounded cell queries.
- **Source-based evidence:** the original constructs a separate semantic map and
  reads it in movement probes; historical classifier behavior is not promoted.
- **Theoretical analysis:** unique in-range row-major indexing, data-dependency
  proof of display independence and an explicit update contract.
- **Benchmark setup / commands / environment:** no benchmark; run
  `python3 research/analyses/laigle-dor/tools/verify_integration.py`.
- **Expected result versus actual result:** 3,560 queries agree with independent
  logical-set oracles across four map sizes, four visual patterns and two states;
  four logical updates change the map. See [results](../../research/analyses/laigle-dor/integration-verification.json).
- **Real-hardware confirmation:** none; the validated property is independent
  of a CPU or video system.
- **Outstanding questions:** the game's exact cell taxonomy, flag/result contracts
  and all-room movement remain research. Platform cost requires benchmarking.

## Recommendation for new projects

Use a separate semantic map when movement rules are cell-based and should remain
independent of artwork. Define coordinate conversion, boundaries, named values
and dynamic updates first. Do not use this coarse representation alone for
fine collision or fast movement that can skip cells. No performance ranking is
implied by `validated`.

## References and related techniques

- [Historical finding/promotion record](../../research/findings/GEN-0002-semantic-collision-grid.md).
- [GEN-0001: animation streams, still research](../../research/findings/GEN-0001-resumable-animation-streams.md).
- [Source-based verification](../../research/analyses/laigle-dor/verification.json).
- [Reproducible functional checks](../../research/analyses/laigle-dor/tools/verify_integration.py).
