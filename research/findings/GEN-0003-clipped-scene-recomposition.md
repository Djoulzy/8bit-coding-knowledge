---
id: "GEN-0003"
title: "Recompose only the scene region affected by movement"
category: "graphics"
cpu: ["6502"]
machines: ["oric-atmos"]
status: analyzed
source_analyses: ["../analyses/space-1999/overview.md"]
tags: ["dirty-rectangles","occlusion","scratch-buffer"]
---

# Recompose only the scene region affected by movement

## Summary

Rebuild a small affected rectangle from scene data when a sprite moves, then copy that rectangle to the display. This avoids retaining a background image for each moving object while allowing the redraw to incorporate other objects and occlusion.

## Problem and context

- **Problem:** erase the previous position and draw the next without repainting a full frame or using a stale saved background.
- **Use cases:** sparse movement in a mostly static scene with cheaply enumerable intersecting objects.
- **Preconditions:** dirty bounds cover both old and new images; compositing order and masks reconstruct the correct scene; the rectangle fits scratch storage.
- **Applicability:** common algorithm. The historical implementation uses NMOS 6502 on Atmos; other CPUs/machines need their own renderer and display encoding.

## Provenance

| Field | Value |
| --- | --- |
| Original program | Space: 1999, Oric game; supplied French disk, README version 1.00 / February 2008 |
| Author / publisher | Chema Enguita, principal game code; Twilighte and Dbug, collaborators. Individual routine authorship not separately established |
| Archive | Published Oric Software archive, commit `c81612082482d1f497638ada14ad4640c5e4f1ec` |
| License / usage | No explicit code license identified; no copied large code excerpts or source mirror |
| Supplied disk SHA-256 | `9d85e1d75d9f1e548f4d1e3bc3750085e7c8c125bb6cd110fb604ba86ba3e851` |
| File / symbols / lines | [upstream `game source/NOISE/spritemov.s:L71–L208`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/NOISE/spritemov.s#L71-L208); [upstream `game source/WHITE/white.s:L775–L783`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/WHITE/white.s#L775-L783); [upstream `game source/NOISE/clipping.s:L386–L473`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/NOISE/clipping.s#L386-L473) |
| First analysis | [Space 1999](../analyses/space-1999/overview.md) |

Assembly evidence is **supplementary published source**, not an ASM file supplied under `research/sources/`. Exact full executable correspondence remains unproven. Original byte hashes and line counts are retained in [upstream manifest](../analyses/space-1999/upstream-manifest.json).

## Original implementation

OSDK/XA source defines SCRBUFFSAVE, six-byte scratch rows and 240-byte image/occlusion buffers. [upstream `game source/NOISE/noise-start.s:L14–L25`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/NOISE/noise-start.s#L14-L25); [upstream `game source/NOISE/noise-start.s:L96–L114`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/NOISE/noise-start.s#L96-L114). `_move_sprite` computes direction-dependent bounds using either the old or updated coordinates and expands width/height for the movement. `_white_update` clears the active rectangle, draws intersecting room content and copies it to screen.

“Double buffer” in the source is a local scratch rectangle, not two complete frames. No source excerpt is needed to reproduce the algorithm:

```text
affected = bounds covering the old image and the new image
clear scratch(affected)
compose intersecting scene objects with their masks
copy scratch(affected) to the visible display
```

## Technical explanation

The room/layer/object model provides the background anew. The compositor considers screen intersection and foreground occlusion, so an overlapping object need not be erased to a saved image from an earlier instant. Source-specific occlusion corrections assume selected neighboring cells, four layers and layer height eight: [upstream `game source/NOISE/occlusions.s:L78–L181`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/NOISE/occlusions.s#L78-L181). Generalizing the algorithm does not justify generalizing this geometric shortcut.

## CPU-specific considerations

A/X/Y and shared zero-page pointers are reused across helper calls. Scratch and screen strides differ; self-modified SBC immediates select the destination stride. Indexed indirect reads, stores, loop branches and IRQ interruptions affect timing. Writable-code and non-reentrancy assumptions belong to this implementation. No page-alignment or exact-cycle benefit is claimed.

## Machine-specific considerations

Atmos scratch is `$0200–$02EF`; occlusion scratch is `$0400–$04EF`. Six bytes × 40 rows is the nominal capacity of each 240-byte buffer. A larger padded rectangle can exceed it. Screen stride is 40 bytes, with six pixel bits and embedded attributes; dirty bounds must preserve control columns/frame. Neither reserved low pages nor ROM independence should be assumed in a program sharing the system environment.

## Performance and resource costs

| Metric | Implementation | Alternative | Evidence |
| --- | --- | --- | --- |
| Scratch image + occlusion | 480 bytes | Full screen scratch: 8000 bytes per 200×40 image | Source reservations / arithmetic; not measured live occupancy |
| Redraw work | Intersecting scene and masks, then rectangle copy | Saved backgrounds or complete room redraw | Source control flow; CPU cycles unmeasured |
| Extra scene state | Layer maps, object data, location cache | Format-dependent | Architecture report; excluded from 480-byte scratch figure |

## Advantages

- Small scratch working set.
- Scene state remains the authority for recomposition.
- Avoids stale background snapshots when objects overlap or change.

## Limitations and risks

Repeated movement may redraw overlapping rectangles more than once. Dense scenes and expensive occlusion can make recomputation costly. Capacity, movement bounds, draw ordering and attributes are correctness requirements; no tear-free synchronization was established.

## Alternatives

Save and restore each object's background; merge dirty rectangles; redraw larger tiles; or draw full frames when memory/CPU permit. [ORIC-0001](ORIC-0001-background-pages-with-position-metadata.md) is a historical saved-background comparison, not this implementation.

## Validation record

- **Status:** analyzed, source-based.
- **Checks:** inspected movement bounds, update/copy routines and buffer definitions.
- **Benchmark / hardware:** none; no measured speedup or emulator execution.
- **Outstanding:** exhaustive edge/sub-byte/mirror/stacked-object tests; capacity assertions; compare elapsed cycles with saved backgrounds.

## Recommendation for new projects

Consider this when dirty areas stay small and scene reconstruction is inexpensive. Avoid adopting the historical occlusion shortcuts or low-memory allocations without adapting them. Confirm bounds and composition correctness before comparing performance.

## References and related techniques

[Architecture](../analyses/space-1999/architecture.md), [hardware analysis](../analyses/space-1999/hardware-techniques.md), [GEN-0002](GEN-0002-semantic-collision-grid.md).
