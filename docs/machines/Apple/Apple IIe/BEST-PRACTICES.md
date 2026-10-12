---
record_type: machine-guidelines
manufacturer: Apple
machines: ["apple-iie"]
cpu: ["6502"]
status: mixed
review_date: "2026-10-12"
---

# Apple IIe — Development best practices

## Supported hardware and assumptions

The [machine profile](README.md) registers the requested IIe target while keeping
its exact CPU, enhancement status, ROM, memory expansions and video configuration
unresolved. The historical corpus contains Apple II family code, not a verified
compatibility certificate for every IIe configuration.

The CPU recommendations below retain their **documented NMOS 6502** scope.
Other processors need separate instruction, bus, timing and interrupt checks.
The graphics discussion concerns ordinary HGR, not a demonstrated double-HGR
or auxiliary-memory renderer. Firmware, display banking and memory ownership
are prerequisites, not assumed reset defaults.

## Quick-start rules

1. **Define the complete target and ownership profile first.** Record the CPU,
   ROM, RAM/banks, firmware services, video output, storage and IRQ/NMI owners.
   This is a compatibility prerequisite; see
   [portability](guidelines/portability.md#establish-the-target-profile-first).
2. **Use a bounded logical collision map when movement is cell-based.** Keep
   scene properties independent of artwork and synchronize changes explicitly.
   This does not validate pixel collision or a speed advantage; see
   [GEN-0002](../../../common/semantic-collision-grid.md) and the
   [Apple adaptation](guidelines/graphics.md#keep-logical-collision-state-independent-of-hgr).
3. **Use carry-stream extraction only for its four-field two-bit contract.**
   Clear A for each field and consume a private writable byte; this is not a
   general decoder for every packed format. See
   [CPU6502-0003](../../../cpu/6502/carry-stream-field-extraction.md) and
   [CPU and memory](guidelines/cpu-and-memory.md#extract-four-high-to-low-two-bit-fields).
4. **Use descending page copies only for full, aligned, disjoint ordinary RAM.**
   Establish stable bank mappings and exclusive pointer/code/stack ownership.
   This is neither `memmove` nor an I/O copy or a fastest-copy claim; see
   [CPU6502-0004](../../../cpu/6502/descending-page-copy.md) and
   [CPU and memory](guidelines/cpu-and-memory.md#copy-complete-disjoint-ram-pages).
5. **Make the display address and bit-7 contract explicit.** Page allocation,
   visible-row addressing, composition and actual bank state need separate
   checks. A captured renderer's `$80` convention is not universal color advice;
   see [graphics constraints](guidelines/graphics.md#documented-display-constraints).
6. **Keep historical optimizations experimental until their full contracts pass.**
   Local static models do not certify complete clipping, page repair, reentry,
   audio timing or disk execution. See the candidate index below and the
   [test matrix](guidelines/portability.md#minimum-validation-matrix).

Rules 2–4 reuse existing validated general/CPU records without extending their
scope. The other items are evidence/compatibility constraints, not newly
validated optimizations. No Apple-specific finding is promoted by this guide.

## Topic guides

- [CPU, memory, bank and caller contracts](guidelines/cpu-and-memory.md)
- [HGR representation and renderer experiments](guidelines/graphics.md)
- [Portability, firmware, storage and test matrix](guidelines/portability.md)

## Porting an existing program

- Select an exact CPU/ROM/memory configuration rather than inferring one from
  the `Apple IIe` directory name.
- Reallocate zero page, stack, vectors and writable code against all retained
  firmware/OS owners; include bank state in the allocation contract.
- Adapt the renderer's address generation, pixel/bit-7 encoding, bounds and
  page role; changing a base address alone is insufficient.
- Isolate monitor, BASIC, disk and input services behind revision-specific
  interfaces with known clobbers and restoration behavior.
- Separate foreground audio, input polling and actor quotas when measuring
  pace; no current record establishes a fixed frame rate.
- Authenticate image layout and edition before interpreting a loader anomaly
  as original program behavior. Exercise boot, scene loading and error paths.
- Test output and ownership first, then compare equivalent complete workloads.
  Keep emulation and real-hardware measurements distinct.

The detailed boundaries are in [portability.md](guidelines/portability.md).

## Evidence and status

| Published recommendation | Status | Exact scope |
| --- | --- | --- |
| [GEN-0002](../../../common/semantic-collision-grid.md) | validated | Bounded logical cell queries independent of display pixels; no pixel-precision or speed claim |
| [CPU6502-0003](../../../cpu/6502/carry-stream-field-extraction.md) | validated | Four high-to-low two-bit fields under the documented NMOS 6502 source/register contract |
| [CPU6502-0004](../../../cpu/6502/descending-page-copy.md) | validated | Complete aligned disjoint ordinary-RAM pages; no overlap, I/O or performance ranking |

Their proof/functional-model decisions are recorded in the
[integration review](../../../../research/analyses/laigle-dor/integration-review.md).
The [Lode Runner](../../../../research/analyses/lode-runner/overview.md) and
[Karateka](../../../../research/analyses/karateka/overview.md) dossiers contribute
Apple-specific evidence and comparisons, not new validation of those games.
Their recorded verification uses static bytes and translated models; no CPU
execution benchmark, complete emulator trace or real-hardware result is present.

## Candidates requiring validation

All rows below are `analyzed` research, **not current best practices**.

| Candidate / evidence | Potential use | Required before recommendation |
| --- | --- | --- |
| [APPLE2-0001](../../../../research/findings/APPLE2-0001-paired-hires-background-masks.md) | Persistent HGR terrain baseline and masked restoration/overlap | Prove terrain/actor order, bounds, bit-7 agreement and actual page/bank state |
| [APPLE2-0002](../../../../research/findings/APPLE2-0002-seven-phase-sprite-tables.md) | Precomputed phase outputs for packed rows | Establish used token/ID/width domain; compare direct outputs with pointer-plus-dictionary storage and complete caller cost |
| [APPLE2-0003](../../../../research/findings/APPLE2-0003-runtime-sprite-shift-and-reflection.md) | Runtime phase splitting and reflection with shared assets | Exhaust clipping, phase, mirror, composition and color cases; benchmark equivalent outputs |
| [GEN-0005](../../../../research/findings/GEN-0005-bit-quota-round-robin.md) | Actor quotas with a persistent selection cursor | Bound callback work and audit every cursor writer, early exit and repeated selection |
| [GEN-0006](../../../../research/findings/GEN-0006-fixed-actor-work-window.md) | Shared actor routines through a load/process/commit window | Prove ownership and commit lifetimes; compare full copied-window and indexed-record workloads |
| [CPU6502-0007](../../../../research/findings/CPU6502-0007-inline-stream-return-address.md) | Immutable parameters placed after JSR | Bound data and restore the exact return frame; test nesting, IRQ/NMI and pointer ownership |

Karateka also supplies additional evidence for equal-width patches, retained
animation cursors and scene-region repair. Those related records remain
experimental; see the topic guides rather than duplicating their fiches.
