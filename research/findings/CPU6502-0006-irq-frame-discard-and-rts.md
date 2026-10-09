---
id: CPU6502-0006
title: "Discarding an IRQ frame to return through an existing JSR frame"
category: interrupts
cpu: ["6502"]
machines: ["oric-unspecified", "microdisc"]
status: analyzed
source_analyses: ["../analyses/vip4-demo/overview.md"]
tags: [stack, interrupts, nonlocal-return, storage]
---

# Discard an IRQ frame and return through JSR

## Summary

**Classification: CPU technique.** Three PLA instructions discard the hardware
IRQ frame; RTS then consumes the interrupted subroutine's existing JSR frame.
Vip4 configures two such disk handlers, but SEI masks them on the traced loading
paths. The stack mechanism is explained; live activation is not established.

## Problem and context

- **Problem:** leave a polling subroutine on an interrupt without returning to
  the interrupted PC or maintaining an explicit completion flag.
- **Potential use:** a carefully controlled nonlocal abort to the nearest caller.
- **Preconditions:** exactly one hardware IRQ frame above an appropriate JSR
  frame, no handler pushes remaining, no intervening PHA/data frames, known IRQ
  source and acknowledge behavior. The chosen caller must accept partial work.
- **CPU:** NMOS 6502 stack/IRQ/RTS semantics. Oric disk register effects are separate.

## Provenance

| Field | Value |
| --- | --- |
| Program | Vip4 Demo, consistent with Quintessential |
| Author / license / exact archive | Routine author, license and download origin unknown; Defence Force program attribution in overview |
| Original source | `research/sources/Oric/Vip4 Demo/vip4.dsk` |
| Git baseline | `a04d227fbbc9252d9dda01641581f4f0dc49a8e3`; image ignored/untracked |
| SHA-256 | `555e811187069b29bfc6cf657be7f19f8c49aa8d25fbbeeb8ab4718ad2577558` |
| Boot handler | Relocated CPU `$A869–$A876`, original DSK start `$0003DB` |
| Resident handler | CPU `$FA7F–$FA8D`, original DSK start `$000A7F` |
| Configuration / caller | R `$FA9F–$FAF6`, especially vector writes `$FAA9/$FAAC` and SEI `$FA9F` |
| Mapping / first analysis | [Listings](../analyses/vip4-demo/extracted/README.md), [C02](../analyses/vip4-demo/cpu-techniques.md#c02-irq-frame-discard-followed-by-rts) |

No original line numbers, symbols or assembler dialect are available.

## Original implementation

Both handlers start with the following short decoded sequence:

```asm
PLA
PLA
PLA
; controller control/status operations
; RTS ends the handler, rather than RTI
```

The resident version ORs the selected side bit into controller control, reads
status and returns. The boot version additionally masks status with `$7C`.

## Technical explanation

With an otherwise clean active JSR frame, the stack top on IRQ entry is:
P, interrupted PC low, interrupted PC high, JSR return low, JSR return high.
PLA three times removes the first three bytes. RTS pulls the remaining low/high
address and adds one, resuming at the caller's instruction after JSR.

This does not unwind all calls. If IRQ occurs inside the nested controller
wait at `$FAFB`, RTS returns inside its caller `$FA13`, not necessarily to
`$FA8E`. A data push above that frame invalidates the scheme. Restoring IRQ
P with RTI would instead resume the interrupted PC, which this code bypasses.

The traced resident path starts SEI, sets the vector, invokes the page/sector
workers and never clears I before returning. Maskable disk IRQ activation
therefore cannot be inferred. The same restriction applies to the boot path.
Do not describe the demo as a working IRQ-aborted loader based on the handler's
presence. An external I-clear caller or different revision would need evidence.

## CPU-specific considerations

- **Registers/flags:** PLA replaces A; controller status becomes the result.
  X/Y are untouched by the handler. Interrupted P is discarded; I remains set.
- **Addressing:** ordinary stack operations plus absolute device accesses.
- **Compatibility:** documented NMOS instructions; no stack trick requiring
  an undocumented opcode. Other CPU interrupt frames are not covered.
- **Timing:** no branch/page-cross dependency in the handlers themselves;
  hardware IRQ entry latency and device behavior are separate.
- **Alignment:** no special code alignment; stack must contain the expected frame.

## Machine-specific considerations

The original routines write Microdisc control at `$0314` and read status at
`$0310`. Device acknowledge/completion semantics and IRQ enable routing require
controller documentation and tracing. A different IRQ source must never enter
this handler without matching the intended abort contract. Firmware IRQ or NMI
services may have a different prologue/frame and cannot be substituted casually.

## Performance and resource costs

| Metric | Original | Alternative | Evidence / method |
| --- | --- | --- | --- |
| Resident handler body | 15 bytes, 32 theoretical cycles | Normal register save/RTI + completion flag not measured | Decoded `$FA7F–$FA8D`; excludes IRQ entry/device delay |
| Boot handler body | 14 bytes, 30 theoretical cycles | Unknown | Decoded `$A869–$A876`; excludes IRQ entry |
| Stack use | Hardware IRQ frame 3 bytes; existing JSR frame 2 bytes | Ordinary IRQ retains interrupted frame until RTI | CPU frame semantics |
| RAM / ROM | Resident RAM code; no extra completion variable in these bodies | Separate flag may simplify control and preserve context | Not a complete memory/speed comparison |

## Advantages

- Explains a compact, flag-free path to the interrupted subroutine's caller.
- Can intentionally abandon a polling loop under tightly controlled stack state.

## Limitations and risks

- Actual Vip4 load-path activation is unproven and masked in reviewed code.
- Discards flags and partially completed execution; no automatic rollback.
- Depends on nearest frame, stack contents and exclusive IRQ ownership.
- A nested wait, extra push or changed handler prologue changes the target.

## Alternatives

Use a normal IRQ handler ending RTI and a completion flag polled by foreground;
use controller DRQ/status polling with explicit timeout; or provide a structured
abort path with a saved known stack pointer. Compare correctness and recoverability
before considering cycle savings.

## Validation record

- **Status:** analyzed stack semantics; observed configured code, runtime use unknown.
- **Source evidence:** two three-PLA/RTS bodies, vector writes and SEI path.
- **Theory:** stack-shape model in
  [verify_analysis.py](../analyses/vip4-demo/tools/verify_analysis.py).
- **Benchmark / emulator / real hardware:** none; no IRQ was injected.
- **Result:** the abstract frame returns to the nearest caller; code activation,
  device success and error recovery remain untested.

## Recommendation for new projects

Prefer explicit completion/abort state unless stack and IRQ ownership are part
of a documented low-level contract. Consider this only after verifying every
interruptible instruction and caller frame, device acknowledgement and partial
work recovery. Do not copy the historical handler as a standalone safe routine.

## References and related techniques

- [MOS instruction summary](https://ftpmirror.your.org/pub/misc/bitsavers/components/mosTechnology/6502_Instruction_Set_Summary.pdf).
- [Disk and interrupt limitations](../analyses/vip4-demo/hardware-techniques.md#h01-custom-sector-loader-and-overlay-ram).
- [Vip4 source provenance](../analyses/vip4-demo/overview.md).
