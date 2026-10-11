---
id: "CPU6502-0007"
title: "Consume inline parameter streams by replacing the JSR return address"
category: "control-flow"
cpu: ["6502"]
machines: ["apple-ii-family"]
status: analyzed
source_analyses: ["../analyses/lode-runner/overview.md"]
tags: ["jsr", "rts", "inline-data", "hardware-stack", "zero-page"]
---

# Consume inline parameter streams by replacing the JSR return address


## Summary

A callee removes its JSR return address, uses it to find parameters immediately
following the call, and replaces it with the terminator address. RTS then
continues after the data. Lode Runner uses this for text and audio event streams.

## Problem and context

- **Problem:** associate compact constant data with a call without loading an explicit pointer at every site.
- **Use cases:** fixed zero-terminated text and small inline command sequences.
- **Preconditions:** direct JSR, balanced stack, well-formed resident data, exclusive or saved stream pointer and appropriate terminator.
- **Applicability:** 6502 calling convention; observed documented NMOS code on Apple II family hardware, exact physical CPU/ROM unknown.

## Provenance

| Field | Value |
| --- | --- |
| Original program | Lode Runner; supplied 1983-marked cracked Apple II disk |
| Author / publisher | Doug Smith / Brøderbund, corroborated by the publisher manual linked in overview; individual routine authorship and publisher-original equivalence unknown |
| Source / archive | research/sources/Apple IIe/Lode Runner/Lode Runner (1983)(broderbund)[cr].dsk; download/archive provenance unknown |
| License / usage | No license supplied; no redistribution grant established |
| Source revision | Repository baseline d02edc77fa0a02d3f679af22456ca1c762c305dc; historical image is gitignored |
| Image SHA-256 | cbc048a55c2835f1b3b54696660e8902c84c25dac44a6dc94b13a7e8f81379ec |
| File / routine / addresses | [input-audio.asm.txt:L225–L242](../analyses/lode-runner/extracted/input-audio.asm.txt), CPU $86E0–$86FF, first instruction DSK $016FE7; [input-audio.asm.txt:L353–L378](../analyses/lode-runner/extracted/input-audio.asm.txt), CPU $87E1–$8810, first instruction DSK $0161E8; [editor.asm.txt:L29–L29](../analyses/lode-runner/extracted/editor.asm.txt), CPU $7BBF–$7BC1, first instruction DSK $0154C6 |
| First analysis | [Lode Runner overview](../analyses/lode-runner/overview.md) |

The input has no assembly source or original labels. Generated listing lines,
CPU addresses and original image offsets replace unavailable source-line
references. The [extraction conventions](../analyses/lode-runner/extracted/README.md)
explain relocation, byte provenance and unresolved runtime dependencies.


## Original implementation

Original assembler syntax is unknown. Pseudocode names denote analytical roles:

~~~text
returnLow  = pop()
returnHigh = pop()
ptr = returnLow + 256 * returnHigh
ptr += 1
consume data until ptr addresses the zero terminator
push(high(ptr))
push(low(ptr))
RTS
~~~

The text consumer calls character renderer $7B64 for each nonzero byte.
The audio consumer reads nonzero duration, then pitch, and appends an event
to parallel arrays. A zero duration terminates that stream. Playback later
uses LIFO order; stream collection alone does not imply FIFO playback.

A short **new illustrative** call layout, not a historical excerpt, is:

~~~asm
    JSR print_inline
    .byte $C8, $C9, $00  ; example text bytes and terminator
resume:
~~~

Here .byte is illustrative assembler syntax; the imported assembler is unknown.

## Technical explanation

JSR pushes the address of its last operand byte, high then low. PLA therefore
retrieves low then high; parameter data starts one byte after that address.
RTS adds one to the restored address, so pushing the **terminator's address**
resumes at the byte after it.

Both observed consumers initially branch on the loaded return high byte to
their pointer-increment code. Therefore that byte must be nonzero; a call whose
stacked return is in page $00 would take a different path and read the JSR byte
as data. Pointer INC propagates low-byte wrap to high. The loops do not support
a stream wrapping the entire 16-bit address space.

Text advances once per output byte. Audio advances twice per duration/pitch
pair, including page carry. A pitch may be zero; only duration is the sentinel.
The terminating read does not append an event.

## CPU-specific considerations

The shared pointer is $10/$11. PLA/STA/INC modify A and flags; text and audio
also use Y, and audio uses X/depth $54. There is no general register/flag
preservation contract. The pointer uses (zp),Y reads; their cycle cost can
increase on a read page crossing.

The return address is temporarily absent from the hardware stack. Output
callbacks may use balanced JSR/RTS but must not overwrite $10/$11. A nested
inline consumer needs explicit pointer preservation. IRQ/NMI code must preserve
registers and shared state and balance its own stack; arbitrary reentry is unsafe.
Total stack headroom depends on callers, output helpers and interrupt frames.

Only documented NMOS instructions are used. JSR/RTS stack semantics support the
mechanism on 6502-compatible targets, but this is not a tested 65C02 build.
INC pointer arithmetic does not depend on D; invoked rendering/audio helpers
have their own arithmetic and decimal-mode contracts.

## Machine-specific considerations

The mechanism is independent of Apple II HGR and speaker encoding. The example
consumers connect it to those services and reserve ZP $10/$11 themselves;
another platform may already own these addresses. Data and executable bytes
are interleaved, which complicates linear disassembly and code relocation.

## Performance and resource costs

| Metric | Original | Alternative | Evidence |
| --- | --- | --- | --- |
| Call site | 3-byte JSR plus inline stream | Pointer setup plus JSR and separately placed stream | 6502 encoding; no complete linker comparison |
| Shared stream pointer | 2 ZP bytes | Explicit pointer convention may use the same space | Operand references |
| Consumer bodies | Text 32 bytes; audio 48 bytes | Helper-dependent | $86E0–$86FF and $87E1–$8810 inclusive |
| CPU cycles / total stack maximum | Not measured; input/helper/interrupt-dependent | Not measured | No execution or benchmark |

Do not infer a whole-program byte saving from the JSR size alone: compare
consumer code, alignment, duplicated literals, pointer setup and relocation.

## Advantages

- Data stays adjacent to its use.
- Callers need no separately loaded stream address.
- The consumer skips the embedded data through the ordinary RTS mechanism.

## Limitations and risks

Missing terminators can make the consumer read instructions or unrelated memory.
The caller must use JSR with the expected frame; JMP is incompatible.
Malformed audio data can overrun unbounded event arrays. Nested calls and
interrupts can corrupt the shared pointer. The observed initial high-byte
branch and address-wrap behavior are specific restrictions, not universal
properties of every inline-stream design.

## Alternatives

Pass a pointer in registers/ZP, use indexed immutable message tables, or make
the inline interface length-prefixed with explicit bounds. An explicit pointer
is preferable when reentrancy, relocation tooling or static code/data separation
matters more than local call-site compactness.

## Validation record

- **Current status:** analyzed; provisional.
- **Evidence:** both consumers, callers and character/audio helpers in selected listings.
- **Analysis:** stack byte order, JSR last-byte convention, terminator address and pointer carry were traced from instructions against the MOS reference.
- **Checks:** all listing bytes map to the pinned image; no CPU execution or stack trace.
- **Reproducer:** [extraction instructions](../analyses/lode-runner/extracted/README.md), [verification](../analyses/lode-runner/verification.json).
- **Benchmark / real hardware:** none.
- **Open:** every caller's data bounds, maximum event depth and complete IRQ/NMI/ZP ownership.

## Recommendation for new projects

Consider inline streams for small immutable data under a controlled calling
convention. State bounds, push order, terminator semantics, pointer ownership
and reentrancy rules. Avoid this observed implementation when the return page
can be zero or the stream can wrap; use an explicit bounded interface for
untrusted or dynamically generated data.

## References and related techniques

- [MOS instruction summary](https://ftpmirror.your.org/pub/misc/bitsavers/components/mosTechnology/6502_Instruction_Set_Summary.pdf), JSR/RTS and stack operations.
- [CPU report](../analyses/lode-runner/cpu-techniques.md).
- [CPU6502-0002](CPU6502-0002-rts-in-basic-line-header.md): embedding RTS in a BASIC header is a different layout technique.
- [CPU6502-0006](CPU6502-0006-irq-frame-discard-and-rts.md): discards an IRQ frame rather than consuming JSR-adjacent parameters.
- [GEN-0004](GEN-0004-stack-driven-pair-grammar.md): pending-symbol stack rather than return-address parsing.
