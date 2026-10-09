---
id: "GEN-0004"
title: "Expand binary-pair text tokens with an explicit work stack"
category: "compression"
cpu: ["6502"]
machines: ["oric-atmos"]
status: analyzed
source_analyses: ["../analyses/space-1999/overview.md"]
tags: ["pair-grammar","text","hardware-stack"]
---

# Expand binary-pair text tokens with an explicit work stack

## Summary

A high-bit byte identifies a pair of earlier symbols. Expand tokens with an explicit LIFO work list, pushing the second child before the first; emit low nonzero bytes directly. Space 1999 uses the 6502 hardware stack for this work list, avoiding recursive grammar-expansion calls.

## Problem and context

- **Problem:** store repeated text fragments compactly with a small decoder.
- **Use cases:** static messages with reusable byte pairs and constrained RAM.
- **Preconditions:** acyclic grammar, nonzero leaves, reserved high-bit token range, sufficient work-stack capacity and a literal-output callback that balances its own stack.
- **Applicability:** common compression/decoder structure; PHA/PLA implementation is 6502-specific. No inherent Oric video dependency.

## Provenance

| Field | Value |
| --- | --- |
| Original program | Space: 1999, Oric game; supplied French disk, README version 1.00 / February 2008 |
| Author / publisher | Chema Enguita, principal game code; Twilighte and Dbug, collaborators. Individual routine authorship not separately established |
| Archive | Published Oric Software archive, commit `c81612082482d1f497638ada14ad4640c5e4f1ec` |
| License / usage | No explicit code license identified; no copied large code excerpts or source mirror |
| Supplied disk SHA-256 | `9d85e1d75d9f1e548f4d1e3bc3750085e7c8c125bb6cd110fb604ba86ba3e851` |
| File / symbols / lines | [upstream `game source/sp1999.s:L4235–L4264`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/sp1999.s#L4235-L4264) (`decomp`); [upstream `game source/stringsc.s:L1903–L2032`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/stringsc.s#L1903-L2032) (`Grammar`) |
| First analysis | [Space 1999](../analyses/space-1999/overview.md) |

Assembly evidence is **supplementary published source**, not an ASM file supplied under `research/sources/`. Exact full executable correspondence remains unproven. Original byte hashes and line counts are retained in [upstream manifest](../analyses/space-1999/upstream-manifest.json).

## Original implementation

OSDK/XA, byte tokens `$80–$FF`, 128 two-byte entries (256 bytes). `decomp` pushes a zero sentinel and the input symbol. Each PLA yields either the sentinel, a literal for `put_code`, or a token whose index is `2 * (symbol & $7F)`. It pushes Grammar[index+1], then Grammar[index], making the first child the next popped symbol.

The outer print loop handles the zero-terminated compressed message one byte at a time, [upstream `game source/sp1999.s:L4206–L4219`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/sp1999.s#L4206-L4219). Literal zero cannot also appear as normal output. High-bit literal characters need another encoding; the grammar shown does not provide an escape opcode.

## Technical explanation

This is depth-first traversal of a binary grammar, using pending symbols instead of recursive call frames. For a pair A,B, LIFO pushes B then A, thus emitting the expansion of A before B. A token can expand to other tokens. A cycle would prevent completion and can exhaust/wrap the hardware stack; checking acyclicity is essential.

The actual grammar's 256 bytes match the disk exactly at logical offset `$1D3C3`. Every token references smaller-valued symbols; all leaves are nonzero literals. Modeling all 128 tokens gives a longest expansion of eight bytes and at most four pending symbols. These are data properties, not CPU-stack measurements.

## CPU-specific considerations

PHA/PLA share `$0100–$01FF` with return addresses and IRQ frames. Sentinel plus modeled pending symbols require at most five bytes of explicit decoder work storage for one input token; add the decoder's JSR return, any caller frames, output-function stack use and interrupt activity. A, Y and flags are decoder state; the output call must preserve the outer print-loop's required registers.

Only documented NMOS instructions are involved. Byte ASL computes the index in `$00–$FE`; absolute indexed grammar reads can cross a page. Timing depends on token depth, literals, output and interrupts; no constant decode-time claim is made.

## Machine-specific considerations

Oric-specific printing is separate from the grammar algorithm. IRQ register preservation supports foreground use but does not prove worst-case stack safety. The active source leaves GRAMMAR2PAGE4 disabled; a `$0400` grammar allocation is a conditional alternative, not the observed default.

## Performance and resource costs

| Metric | Original | Alternative | Evidence |
| --- | --- | --- | --- |
| Grammar | 256 bytes | Uncompressed text needs no grammar | Source and exact disk match |
| Explicit work storage | At most 5 stack bytes for this grammar, including sentinel | Dedicated work buffer or recursive call frames | Mathematical model; total runtime stack unknown |
| Longest token expansion | 8 output bytes | Input-dependent | All actual grammar tokens modeled |
| Compression ratio / cycles | Not measured for this French build | Not measured | README English-text figure cannot be substituted |

## Advantages

- Small static decoder structure.
- No recursive subroutine call per expanded token.
- Work-storage bounds can be computed from an acyclic grammar.

## Limitations and risks

Shared hardware-stack overflow, malformed/cyclic tokens and reserved byte ranges limit safety and portability. Compression effectiveness depends on the text corpus. Pair substitution here does not imply an LZ sliding window or general-purpose archive format.

## Alternatives

Uncompressed strings, a dedicated explicit stack, dictionary words, bounded recursion or another text codec. A separate work buffer isolates decoder storage from IRQ/return-address usage.

## Validation record

- **Status:** analyzed.
- **Source/data checks:** exact grammar byte match, acyclicity, nonzero leaves, all token expansions and maximum pending count.
- **Reproducer:** [inspect_inputs.py](../analyses/space-1999/tools/inspect_inputs.py), using pinned reference files as described in overview.
- **Benchmark / hardware:** none. Printing and complete stack depth have not been executed.
- **Next:** compare independently decoded messages with expected French text; trace SP under output plus worst IRQ load.

## Recommendation for new projects

Consider binary-pair grammar for static repeated messages. Bound expansion and reserve token values explicitly. Prefer a separate bounded work stack when interruption or output nesting makes hardware-stack headroom uncertain.

## References and related techniques

[CPU analysis](../analyses/space-1999/cpu-techniques.md), [verification](../analyses/space-1999/verification.json). GEN-0001 is a resumable animation stream, not this text codec.
