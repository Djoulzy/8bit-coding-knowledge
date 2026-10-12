---
record_type: machine-guidelines
manufacturer: Tangerine
machines: ["oric-1", "oric-atmos"]
cpu: ["6502"]
status: mixed
review_date: "2026-10-11"
---

# Oric — Development best practices

## Supported hardware and assumptions

This guide covers Oric-1 and Oric Atmos programs using the documented NMOS
6502 instruction set. It does **not** assume that ROM entry points, free
zero-page locations, interrupt state or storage hardware are interchangeable
between the two models.

The current evidence comes from three different environments:

- *L'Aigle d'Or*: 48 KiB, tape, BASIC/ROM services, Oric-1 with an observed
  ROM-entry adaptation intended to cover another ROM;
- *Space: 1999*: Atmos, Microdisc-compatible overlay RAM, private IRQ, direct
  sector I/O and OSDK/XA source;
- *Vip4 / Quintessential*: an exact model and ROM revision are unresolved, but
  the examined disk uses Microdisc-compatible registers and writable upper RAM.

These are separate compatibility profiles. A mechanism observed in one profile
is not automatically valid in the others. See the
[portability guide](guidelines/portability.md) for the evidence matrix.

## Quick-start rules

1. **Define a complete target profile before assigning memory or calling ROM.**
   Record the model, ROM revision, RAM, display mode, storage interface and
   interrupt owner. This is a platform constraint, not an optimization; see
   [portability](guidelines/portability.md#establish-the-target-profile-first).
2. **Treat Oric display bytes as either pixel data or serial control data.**
   Ink, paper and charset attributes are in the display stream and may affect
   later cells on the same row. Do not apply pixel OR/mask operations to an
   attribute byte without an explicit encoding contract; see
   [graphics](guidelines/graphics.md#preserve-the-pixelattribute-distinction).
3. **Use a separate semantic collision map when movement is cell-based.** This
   is validated for display-independent bounded lookup, not for performance or
   fine-pixel collision. Define bounds and dynamic-update ownership; see
   [GEN-0002](../../../common/semantic-collision-grid.md) and the
   [Oric adaptation](guidelines/graphics.md#keep-cell-collision-state-independent-of-display-bytes).
4. **Use carry-stream extraction only under its proved two-bit contract.** A
   private writable source byte is consumed and A/flags are clobbered; the
   technique is not a general packed-field decoder. See
   [CPU6502-0003](../../../cpu/6502/carry-stream-field-extraction.md) and
   [CPU and memory](guidelines/cpu-and-memory.md#extract-four-high-to-low-two-bit-fields-through-carry).
5. **Use the descending page-copy idiom only for complete, aligned, disjoint
   RAM pages.** It is not `memmove`, an empty-length convention or an I/O copy,
   and it is not proved fastest. See
   [CPU6502-0004](../../../cpu/6502/descending-page-copy.md) and
   [CPU and memory](guidelines/cpu-and-memory.md#copy-complete-disjoint-ram-pages-with-an-explicit-contract).
6. **Give zero page, stack, writable code and IRQ state explicit owners.** The
   historical programs deliberately take over low memory in incompatible ways;
   their addresses are evidence, not reusable allocations. See
   [CPU and memory](guidelines/cpu-and-memory.md#reserve-low-memory-and-interrupt-state-explicitly).
7. **Keep every `analyzed` rendering, audio or interrupt mechanism behind an
   experiment boundary.** Reproduce output first, then compare alternatives
   with the same ROM, memory map and interrupt conditions. The current
   [candidate inventory](#candidates-requiring-validation) is not normative.

The first, second and sixth rules are hardware/ownership constraints. Rules
three through five are the only validated technique recommendations currently
applicable here, each within the linked scope. There is no validated claim that
an Oric-specific renderer, disk path, audio driver or IRQ scheme is fastest.

## Topic guides

- [CPU, memory and interrupt contracts](guidelines/cpu-and-memory.md)
- [Graphics, attributes and redraw strategies](guidelines/graphics.md)
- [Portability across Oric models and configurations](guidelines/portability.md)

## Porting an existing program

- Confirm NMOS 6502 compatibility; do not infer 65C02 timing or behavior.
- Replace source-machine zero-page and stack assumptions with an Oric ownership
  map that includes ROM, BASIC, DOS and IRQ users retained by the port.
- Convert the renderer around the Oric's 40-byte HIRES scanline, six pixel bits
  per graphic byte and in-band attributes; do not merely change the base address.
- Decide whether TEXT, HIRES and charset regions have exclusive or phased
  ownership before allocating buffers in their overlapping ranges.
- Isolate ROM calls behind a model/revision adapter and document registers,
  flags, workspace and interrupt side effects.
- Select tape, Microdisc-compatible disk or another storage path explicitly;
  controller register maps and overlay RAM are not interchangeable.
- Test keyboard and AY-3-8912 access together when sharing VIA/PSG state.
- Record emulator and real-hardware conditions separately; no current
  Oric-specific technique has real-hardware validation in this repository.

The full checklist and a minimum test matrix are in
[portability.md](guidelines/portability.md#minimum-porting-test-matrix).

## Evidence and status

| Published item | Status | Validated scope |
| --- | --- | --- |
| [GEN-0002](../../../common/semantic-collision-grid.md) | validated | Bounded logical cell lookup independent of display pixels; no speed claim |
| [CPU6502-0003](../../../cpu/6502/carry-stream-field-extraction.md) | validated | Four high-to-low two-bit fields using documented NMOS 6502 semantics |
| [CPU6502-0004](../../../cpu/6502/descending-page-copy.md) | validated | Complete aligned disjoint RAM pages; no overlap, I/O or fastest-copy claim |
| Oric pixel/attribute distinction | documented hardware constraint | Atmos manual plus source analyses; not an algorithmic performance claim |

The validation decision and functional-model results are recorded in the
[L'Aigle d'Or integration review](../../../../research/analyses/laigle-dor/integration-review.md).
The [Space: 1999](../../../../research/analyses/space-1999/overview.md) and
[Vip4](../../../../research/analyses/vip4-demo/overview.md) dossiers add
source evidence and conflicts without promoting their findings.

The [Lode Runner](../../../../research/analyses/lode-runner/overview.md) and
[Karateka](../../../../research/analyses/karateka/overview.md) dossiers were
also reviewed for general and NMOS 6502 transfer candidates. Their Apple HGR,
firmware, banking and device assumptions are **not** Oric evidence. The
[portability guide](guidelines/portability.md#cross-platform-research-boundary)
delimits these comparisons; no recommendation's validated scope is widened.

No current evidence includes an Oric CPU execution benchmark, a complete
emulator trace of these programs or a real-hardware measurement. Instruction
cycle figures in linked documents are theoretical and state their conditions.

## Candidates requiring validation

The following are useful research directions, **not current best practices**:

| Candidate | Status and scope | Required before recommendation |
| --- | --- | --- |
| [GEN-0001 animation streams](../../../../research/findings/GEN-0001-resumable-animation-streams.md) | analyzed; Oric-1/Atmos historical implementation | Bound stream length/work per call; trace yields, cursor wrap and restore order |
| [CPU6502-0001 equal-width patches](../../../../research/findings/CPU6502-0001-two-byte-render-patches.md) | analyzed; writable NMOS 6502 code | Prove exclusive patch execution and attribute-safe output; compare separate workers |
| [ORIC-0001 position-bearing backgrounds](../../../../research/findings/ORIC-0001-background-pages-with-position-metadata.md) | analyzed; Oric-1/Atmos save-under | Test buffer lifetimes, clipping, overlap, zero dimensions and attribute restoration |
| [GEN-0003 clipped scene recomposition](../../../../research/findings/GEN-0003-clipped-scene-recomposition.md) | analyzed; Atmos implementation | Exhaust dirty bounds and occlusion cases; compare cost with saved backgrounds |
| [GEN-0004 pair-grammar decoder](../../../../research/findings/GEN-0004-stack-driven-pair-grammar.md) | analyzed; Atmos implementation | Measure total stack headroom with calls/IRQs and validate decoded output |
| [CPU6502-0005 executable operands as IRQ state](../../../../research/findings/CPU6502-0005-zero-page-code-operands-as-state.md) | analyzed; exact Oric model unresolved | Trace IRQ nesting, initialization and firmware coexistence; compare separate state |
| [CPU6502-0006 IRQ-frame discard](../../../../research/findings/CPU6502-0006-irq-frame-discard-and-rts.md) | analyzed; active published Atmos disk path, Vip4 activation unresolved | Verify every stack shape, IRQ source/acknowledgement and partial-work recovery |
| [ORIC-0002 charset-bank animation](../../../../research/findings/ORIC-0002-masked-charset-bank-animation.md) | analyzed; exact model and bank state unresolved | Render known frames; establish bank pointer, charset and synchronization ownership |
| [ORIC-0003 parity-compressed pixel tables](../../../../research/findings/ORIC-0003-parity-compressed-pixel-tables.md) | analyzed; screen arithmetic modeled for Oric-1/Atmos | Execute the routine and benchmark against full tables at controlled alignments |
| [GEN-0005 actor work quotas](../../../../research/findings/GEN-0005-bit-quota-round-robin.md) | analyzed; common algorithm observed in Apple II code, not tested on Oric | Bound callback cost and shared cursor writes; test early exits and repeated actor selection |
| [GEN-0006 fixed actor work window](../../../../research/findings/GEN-0006-fixed-actor-work-window.md) | analyzed; common organization observed in Apple II code, not tested on Oric | Own the scratch window and load/process/commit lifetime; compare complete copy and indexed-access workloads |
| [CPU6502-0007 inline parameter streams](../../../../research/findings/CPU6502-0007-inline-stream-return-address.md) | analyzed; NMOS 6502 calling mechanism observed in Apple II code, not tested on Oric | Prove bounds, restored return address, nesting and ROM/IRQ scratch ownership; compare an explicit pointer interface |

[CPU6502-0002](../../../../research/findings/CPU6502-0002-rts-in-basic-line-header.md)
is retained as a historical layout-analysis lesson and is explicitly not
recommended for new code.
