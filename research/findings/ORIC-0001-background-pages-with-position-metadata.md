---
id: ORIC-0001
title: "Page-sized saved backgrounds with coordinates in the last two bytes"
category: graphics
cpu: ["6502"]
machines: ["oric-1", "oric-atmos"]
status: analyzed
source_analyses: ["../analyses/laigle-dor/overview.md"]
tags: [software-sprites, memory-ownership, attributes, save-under]
promotion_decision: deferred
integration_review: "../analyses/laigle-dor/integration-review.md"
---

# Saved backgrounds carrying their own position

## Summary

**Classification: Oric-specific implementation of a general 8-bit technique.**
A page-sized sprite background buffer stores tightly packed old screen bytes
and retains its original x/y in its last two bytes. A shared image descriptor
lets the ordinary blitter restore that buffer at the recorded position.

## Problem and context

- **Problem being solved:** erase a moving layer without redrawing an entire
  room or keeping separate coordinate globals for each background.
- **Typical use cases:** small byte-aligned actors on a mostly static screen.
- **Assumptions / preconditions:** valid nonzero dimensions, dedicated live
  buffer, pixel area below metadata, known draw/restore order.
- **CPU variants and target machines:** original NMOS 6502 Oric implementation;
  embedded metadata is general, while display stride/attributes are Oric-specific.

## Provenance

| Field | Value |
| --- | --- |
| Original program | L'Aigle d'Or, AIGLEDOR.2 |
| Author / publisher | Loader credits ROCQUES Louis-Marie; Loriciels, March 1984 |
| Source URL / archive | Download origin unknown; [local TAP](<../sources/Oric/L'Aigle d'Or/Aigle D'or, Le (1984)(Loriciels).tap>) |
| License / usage conditions | No license grant found; loader reproduction restriction |
| Source revision / checksum | TAP SHA-256 `7f01e1a3d05825aab887952cd5711bea69d6525730aba5c1e25c814334fe77d7` |
| File and routine | B2 save-position `$4140–$415B`, save-under `$3ECF–$3EF0`/`$3E78–$3EAE`, restore `$4574–$458C` |
| Line range / symbols / address | TAP `$0076A6–$0076C1`, `$007435–$007456`, `$0073DE–$007414`, `$007ADA–$007AF2` |
| First analysis | [Descriptor and buffer architecture](../analyses/laigle-dor/architecture.md#sprite-descriptors-and-saved-backgrounds) |

## Original implementation

No source assembler/dialect is available. The observed page layout is:

```text
offset $00          pointer-before-data prefix, not copied
offset $01 ... W*H  packed old screen bytes
remaining gap       unused for this saved rectangle
offset $FE          old byte-column x
offset $FF          old scanline y
```

Descriptor ID `$6B` selects a save page through source-low/high tables at
`$9600/$9700`. `$4140` stores x/y at `$FE/$FF`, decrements x for the renderer's
pointer convention, then enters `$3ECF`. That path records the sprite's width
and height into the save slot's descriptor before copying.

## Technical explanation

The save-under loop reads each old display byte into the buffer, then overwrites
the display from the sprite. Screen rows advance by 40 bytes; saved rows advance
by width. The restore loads the saved slot as if it were an image, reads its
metadata, recalculates the screen pointer and invokes `$3E52`.

Loaded save slots `$F3–$F6,$F9,$FA` point to `$5200–$5500,$5800,$5900`.
Their initial pixel sizes are 124, 104, 24, 28, 45 and 95 bytes. Because copying
starts at offset 1, `W*H <= 253` is the capacity condition below metadata; all
six initial descriptors satisfy it. Runtime resizing and simultaneous ownership
still need checking. The likely benefit is treating saved backgrounds as normal
images while making each slot self-describing for restoration.

## CPU-specific considerations

- **Registers and flags:** A/Y transfer bytes; X resolves descriptor fields;
  pointer/dimension arguments are destructive and not reentrant.
- **Addressing modes:** page-aligned absolute,X descriptor reads, `(zp),Y`
  image/screen/buffer accesses.
- **Instruction compatibility:** documented NMOS 6502; layout idea does not
  require this CPU, but the original implementation has not been ported.
- **Page boundaries, branch timing, interrupts:** source/screen reads can cross
  pages; costs depend on width, height and position. Concurrent scratch use is unsafe.
- **Code and data alignment:** buffer page bases permit fixed `$FE/$FF` indexing;
  spare space is a capacity constraint, not automatically reusable RAM.

## Machine-specific considerations

One byte moves six HIRES pixels. Old bytes include serial attributes, so erasing
also restores color control and can affect the rest of a scanline. The attribute
variant `$4840` uses the same coordinate layout but draws through `$408E`.
`$5900` is reused for a 256-byte charset save during darkness transitions:
these owners must have disjoint live intervals.

## Performance and resource costs

| Metric | Original | Alternative | Evidence / method |
| --- | --- | --- | --- |
| CPU cycles | Not measured; proportional to rectangle bytes plus row/setup work | Full room redraw / dirty regions not measured | Static loops only |
| Code size | Shared descriptor/blitter plus metadata wrappers; no isolated total asserted | Unknown | Multiple shared entries |
| RAM / zero-page usage | Six 256-byte pages = 1,536 bytes; two metadata bytes per page; pointers `$60–$67` shared | Separate positions use extra state; exact alternative unknown | Loaded descriptors and loop operands |
| ROM usage | No direct ROM call in save/restore worker | Unknown | Established instructions |

Saving and restoring each pixel entails additional RAM traffic. No measured
speed advantage over redraw is established; the balance depends on scene cost.

## Advantages

- Small moving regions can be erased without reconstructing room geometry.
- Each slot retains its own restoration position.
- A single descriptor format and copy worker handle images and backgrounds.
- Old attributes are retained together with pixel bytes.

## Limitations and risks

- Saved content can erase newer overlapping objects; order must be controlled.
- Fixed pages waste space when sprites are small and cap rectangle size.
- Zero dimensions execute wrapping countdown loops, not empty copies.
- Buffer reuse, clipped/partial rows and current renderer patch mode affect erase.

## Alternatives

Use explicit layer objects with positions, redraw dirty regions from immutable
room data, or keep a full background image if RAM permits. For more overlap,
consider a defined reverse restore order and forward draw order, with tests.

## Validation record

- **Current status:** analyzed.
- **Source-based evidence:** metadata stores/loads, shared descriptor writes,
  copy loops and six initial buffer pointers/dimensions.
- **Theoretical analysis:** capacity and byte layout understood.
- **Benchmark setup / commands / environment:** no benchmark; capacity assertions
  in `python3 research/analyses/laigle-dor/tools/verify_analysis.py`.
- **Expected result versus actual result:** all six loaded rectangles fit;
  runtime overlapping sprites and changed descriptors were not exercised.
- **Real-hardware confirmation:** none.
- **Outstanding questions:** mode-dependent `$5900` ownership, live descriptor
  mutations, attribute stopping and restoration order.

## Recommendation for new projects

Use position-bearing buffers for bounded, mostly independent layers when page
allocation is affordable. Avoid unrestricted overlap or oversized sprites.
Prove capacity, nonzero dimensions and ownership first, and define whether
restoration must force opaque mode irrespective of drawing composition.

## References and related techniques

- [Hardware analysis H02–H04](../analyses/laigle-dor/hardware-techniques.md).
- [GEN-0001 animation streams](GEN-0001-resumable-animation-streams.md).
- [CPU6502-0001 rendering patch](CPU6502-0001-two-byte-render-patches.md).
- [Verification results](../analyses/laigle-dor/verification.json).
- No equivalent repository record existed; save-under itself is conventional.
