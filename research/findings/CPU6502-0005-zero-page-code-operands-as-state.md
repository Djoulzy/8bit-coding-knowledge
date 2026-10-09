---
id: CPU6502-0005
title: "Zero-page executable operands used as IRQ state"
category: memory
cpu: ["6502"]
machines: ["oric-unspecified"]
status: analyzed
source_analyses: ["../analyses/vip4-demo/overview.md"]
tags: [zero-page, self-modifying-code, interrupts, audio]
---

# Zero-page executable operands used as IRQ state

## Summary

**Classification: CPU technique.** Relocate a small IRQ player to private zero
page, then address its operand bytes as ordinary zero-page variables. Vip4 uses
an absolute-load operand as the sample pointer and immediate operands as cached
data, a phase counter and a saved accumulator. Its advantage is compact direct
state access, not faster instruction fetching merely because code is in page zero.

## Problem and context

- **Problem:** reduce state storage and pointer/save overhead in frequent IRQs.
- **Use cases:** small, nonreentrant RAM interrupt bodies with exclusive workspace.
- **Preconditions:** fixed layout, writable code, private operands, no nested
  execution or concurrent modification; IRQ status restoration through RTI.
- **CPU/machine:** documented NMOS 6502 code in an Oric disk demo; later CPUs
  and firmware coexistence are not tested.

## Provenance

| Field | Value |
| --- | --- |
| Program | Local Vip4 Demo image, consistent with Quintessential |
| Author | Defence Force participants named in the [overview](../analyses/vip4-demo/overview.md); routine author unknown |
| Archive / license | Exact download source and license unknown |
| Original source | `research/sources/Oric/Vip4 Demo/vip4.dsk` |
| Revision | Git baseline `a04d227fbbc9252d9dda01641581f4f0dc49a8e3`; image untracked/ignored |
| SHA-256 | `555e811187069b29bfc6cf657be7f19f8c49aa8d25fbbeeb8ab4718ad2577558` |
| Locations | M02 CPU `$9D4A–$9D6E` relocation; `$9D87–$9DD5` IRQ templates, DSK start `$013D88`; M13 CPU `$609B–$60CA`, DSK start `$06FF36` |
| Exact mapping | [sample relocated listing](../analyses/vip4-demo/extracted/sample-zp.asm.txt), [ending relocated listing](../analyses/vip4-demo/extracted/final-zp.asm.txt), [manifest](../analyses/vip4-demo/extracted/manifest.json) |
| First analysis | [C01](../analyses/vip4-demo/cpu-techniques.md#c01-operand-bytes-as-persistent-state-in-zero-page-code) |

Binary offsets replace unavailable source lines. Listings map relocated addresses
back to original template offsets; runtime initialization changes some operands.

## Original implementation

Original assembler dialect and symbols are unknown. The sample's source template
at `$9D87` is copied into all of `$0000–$00FF`. Runtime LDA at `$09` has operand
bytes `$0A/$0B`, initialized to `$1000`. IRQ at `$25` increments these bytes.
The first IRQ also patches the second IRQ's immediate byte at `$2F`.

The ending copies 56 bytes to `$10–$47`; the executable IRQ body is `$10–$3F`.
Its sample pointer is the LDA operand at `$18/$19`; `$26` is the immediate phase
byte; `$3E` is the immediate accumulator restore byte. Short reconstructed
instructions illustrate the save mechanism (analytical syntax, no original labels):

```asm
; Ending IRQ, executed at $0010:
STA $3E         ; patch the operand of the final LDA immediate
; ... body does not modify X or Y ...
; $003D: LDA #saved_A
; $003F: RTI
```

## Technical explanation

The absolute sample load reads directly from its patched address. Incrementing
its low operand with INC sets Z; BNE skips high-operand INC except on wrap.
The pair therefore advances as an unsigned 16-bit pointer without a separate
indirect pointer. The ending wraps at `$8000` to `$67BF` using the high-byte N
flag, so its stream is restricted to that address interval.

`LSR $26` transforms phase 2→1→0. Carry selects low/high nibble. The LDA using
that same byte controls whether BNE skips advancement: the zero phase falls
through, resets to 2 and advances. The byte is state and an immediate operand
at the same time. Saving A into `$3E` lets the final LDA restore it; RTI restores
the interrupted P, including N/Z changed by the load and shifts.

## CPU-specific considerations

- **Registers/flags:** ending preserves A, never touches X/Y, restores P with
  RTI. The two-handler player reserves X/Y constants in its foreground loop.
- **Addressing:** absolute sample read; zero-page state writes and RMW.
- **Compatibility:** documented NMOS instructions; no undocumented opcode trick.
- **Branches/interrupts:** nonnested IRQ required; low-pointer wrap adds work.
  An NMI or another writer can corrupt saved A or operand state.
- **Alignment:** all live state operands fit zero page; sample loads themselves
  do not incur indexed-read page crossing. Branch placement remains relevant.

## Machine-specific considerations

The original sample relocation destroys all firmware zero-page workspace. The
ending's smaller body still overlaps interpreter variables. ROM services cannot
be used safely without explicit reservations/restoration. Oric PSG programming,
upper-RAM vectors and timer ownership belong to the
[hardware report](../analyses/vip4-demo/hardware-techniques.md), not to generic
6502 operand semantics.

## Performance and resource costs

| Metric | Original mechanism | Alternative | Evidence / method |
| --- | --- | --- | --- |
| Sample load | Absolute LDA: 3 bytes, 4 cycles | LDA `(zp),Y`: 2 bytes, 5 cycles plus crossing; needs Y contract | MOS instruction-table calculation only |
| Pointer low/high INC | ZP INC: 2 bytes, 5 cycles each | Absolute INC: 3 bytes, 6 cycles each | Addressing comparison; full IRQ not benchmarked |
| A save + restore | STA zp + LDA immediate: 4 bytes, 5 cycles | PHA + PLA: 2 bytes, 7 cycles | Excludes RTI and body; shared state makes nesting unsafe |
| Executable workspace | Sample copies 256 bytes; ending copies 56, with a 48-byte IRQ body | Separate state requires additional RAM; exact total unknown | Decoded setup loops |
| ROM requirement | None for CPU mechanism | Firmware coexistence depends on reservation | No general firmware guarantee |

These are static operation costs, not measured speedups. Maintaining layout,
initialization, pointer wrap and extra code space may erase local savings.

## Advantages

- Operand bytes double as state, avoiding duplicate variables.
- Pointer/state updates can use compact zero-page instructions.
- Ending save/restore keeps X/Y untouched and avoids stack accesses for A.

## Limitations and risks

- Code/state is nonreentrant and demands exclusive zero page.
- Instruction edits or relocation alter every state-byte address.
- Interrupts must not execute half-patched operands during setup.
- The apparent saved-A optimization spends two more instruction bytes than
  PHA/PLA and cannot preserve nested invocations independently.

## Alternatives

Private indirect sample pointer with reserved Y; absolute code plus separate
state; PHA/PLA for nested accumulator saves; generated code with checked labels
for operand locations. Compare complete IRQ costs and ownership, not only LDA.

## Validation record

- **Status:** analyzed.
- **Source evidence:** relocation, operand patches, nibble/phase/pointer paths.
- **Theory:** pointer and phase models checked in
  [verify_analysis.py](../analyses/vip4-demo/tools/verify_analysis.py).
- **Benchmark/emulator/hardware:** none.
- **Actual result:** byte/state arithmetic agrees with decoded operations;
  no sound, elapsed rate or firmware compatibility established.
- **Open:** real IRQ timing, all startup state, NMI ownership and audio fidelity.

## Recommendation for new projects

Consider this for small fixed-layout, exclusive RAM IRQs after comparing separate
state. Avoid it with ROM code, shared interpreter workspace or nested interrupt
requirements. Reserve each operand byte symbolically, initialize it before CLI,
and verify pointer boundaries and register/status contracts.

## References and related techniques

- [MOS instruction summary](https://ftpmirror.your.org/pub/misc/bitsavers/components/mosTechnology/6502_Instruction_Set_Summary.pdf).
- [CPU6502-0001: equal-width operation patches](CPU6502-0001-two-byte-render-patches.md): related self-modification, distinct state-storage mechanism.
- [Vip4 routine map](../analyses/vip4-demo/routines.md).
