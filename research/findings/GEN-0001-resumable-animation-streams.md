---
id: GEN-0001
title: "Resumable animation streams with draw, restore and event commands"
category: animation
cpu: ["6502"]
machines: ["oric-1", "oric-atmos"]
status: analyzed
source_analyses: ["../analyses/laigle-dor/overview.md"]
tags: [bytecode, animation, cooperative-execution, save-under]
promotion_decision: deferred
integration_review: "../analyses/laigle-dor/integration-review.md"
---

# Resumable animation streams

## Summary

**Classification: General 8-bit technique.** A compact command stream describes
movement, layer restoration, drawing and event boundaries. A retained byte cursor
lets each machine-code call continue the animation, then return control to BASIC
without a dedicated routine for every frame.

## Problem and context

- **Problem being solved:** coordinate several visual operations while keeping
  the high-level controller responsive at defined animation boundaries.
- **Typical use cases:** small scripted actors, equipment poses, staged actions.
- **Assumptions / preconditions:** trusted finite streams, valid sprite/save IDs,
  explicit yield commands, consistent background restoration order.
- **CPU variants and target machines:** original implementation uses NMOS 6502
  on Oric; the command/cursor architecture is portable to other 8-bit CPUs.

## Provenance

| Field | Value |
| --- | --- |
| Original program | L'Aigle d'Or, AIGLEDOR.2 |
| Author / publisher | Loader credits ROCQUES Louis-Marie; Loriciels, March 1984 |
| Source URL / archive | Original download origin unknown; [local TAP](<../sources/Oric/L'Aigle d'Or/Aigle D'or, Le (1984)(Loriciels).tap>) |
| License / usage conditions | No license grant found; reproduction restriction in loader; analysis is separate |
| Source revision / checksum | TAP SHA-256 `7f01e1a3d05825aab887952cd5711bea69d6525730aba5c1e25c814334fe77d7` |
| File and routine | B2 motion interpreter `$4500–$4570`, delta `$4590–$45A9`, equipment `$45AA–$45FB` |
| Line range / symbols / address | TAP `$007A66–$007AD6`, `$007AF6–$007B0F`, `$007B10–$007B61`; BASIC 6, 5017, 5020, 5025 |
| First analysis | [Architecture and grammar](../analyses/laigle-dor/architecture.md#animation-command-language) |

## Original implementation

No assembler source or dialect survives in the supplied image. The following
is explanatory pseudocode, not an original source excerpt:

```text
select stream from motion-ID pointer table
fetch at ++retained_cursor
restore / add actor deltas / draw a layer: continue interpreting
yield command: publish event, process equipment stream, return to BASIC
chain command: select new motion ID, clear cursor, restart
```

The stream's offset-zero prefix is skipped by pre-incrementing the cursor.
Movement opcodes are `$00` (two deltas), `$14/$16` (yield/event), `$15` (delay),
`$17` (chain) and `$80–$FF` (restore ID). Other positive command bytes introduce
four-byte records: slot offset, x offset, y offset, sprite ID. The equipment
decoder has a smaller grammar; its `$14` ends the current call.

## Technical explanation

`$0498` selects a little-endian pointer from `$4200`; `$04A0` retains progress.
The equipment path uses `$04A3`, `$4400` and cursor `$04A9`. Both share the
zero-page stream pointer `$74/$75`. Draw records retain their ending cursor
before invoking renderers that overwrite Y. Relative coordinates are added to
actor position modulo 256, permitting signed byte offsets within valid bounds.
Yield values are stored in `$04A7`; BASIC checks `$16` for an action/event and
`$14` for another continuation decision.

This likely reduces repeated frame-specific code and makes visual sequences
editable as data. Several commands can run in one call, so a command is not
automatically a frame and the controller does not have a verified fixed rate.

## CPU-specific considerations

- **Registers and flags:** A decodes commands, Y indexes stream fields, X indexes
  pointer tables; drawing clobbers them. ADC deltas require decimal mode clear.
- **Addressing modes:** absolute,X pointer-table reads and `(zp),Y` stream reads.
- **Instruction compatibility:** documented NMOS instructions; other CPU ports
  need equivalent byte arithmetic, not this exact binary.
- **Page boundaries, branch timing, interrupts:** stream reads can cross data
  pages; execution time depends on commands, drawing and active ROM interrupts.
- **Code and data alignment:** pointer tables are page-aligned; cursors wrap at
  256 and doubled byte IDs address at most 128 motion pointers.

## Machine-specific considerations

Oric rendering uses six-pixel byte columns, 40-byte scanlines and page save
slots. These are rendering callbacks' dependencies rather than requirements of
the general interpreter. Exact zero-page ownership is shared with BASIC/ROM.

## Performance and resource costs

| Metric | Original | Alternative | Evidence / method |
| --- | --- | --- | --- |
| CPU cycles | Not measured; command-dependent | Separate per-frame code not measured | Static decoder inspection only |
| Code size | Interpreter/helper region `$4500–$45FB`: 252 bytes including gaps | Unknown | Inclusive address range; rendering code excluded |
| RAM / zero-page usage | Two retained cursors; shared two-byte stream pointer plus IDs/event/state | Unknown | `$04A0/$04A9`, `$74/$75`; not total engine RAM |
| ROM usage | Caller remains BASIC; no direct ROM call inside this region | Unknown | Identified machine paths |

## Advantages

- Encodes relative motion and layered drawing together.
- Returns to the controller at explicit event boundaries.
- Shares an interpreter across many sequences and keeps equipment state separate.

## Limitations and risks

- No length checks, invalid-command recovery or execution budget was identified.
- Cursor wrap, chaining without yields or `$15` delays can block progress.
- Slot reuse and overlapping restores can corrupt the visual result.
- A high-bit **command byte** means restore; the fourth draw field remains an
  unrestricted byte sprite ID. The roles must be distinguished.

## Alternatives

Use a frame table for simple fixed sequences, dedicated routines for a few hot
actions, or a state machine with an explicit per-call command budget. Compare
total code plus data size and worst-case latency before choosing bytecode.

## Validation record

- **Current status:** analyzed.
- **Source-based evidence:** decoded instructions, referenced pointer tables and
  BASIC event/cursor accesses; exact byte locations above.
- **Theoretical analysis:** grammar and register/cursor lifetime reconstructed.
- **Benchmark setup / commands / environment:** no benchmark; inspect with
  `python3 research/analyses/laigle-dor/tools/inspect_tape.py --disassemble 4500 45fb`.
- **Expected result versus actual result:** static bytes implement the stated
  dispatch; complete runtime sequence traversal has not been observed.
- **Real-hardware confirmation:** none.
- **Outstanding questions:** all reachable streams, delay reachability, yield
  latency, interrupted zero-page ownership and overlapping layer behavior.

## Recommendation for new projects

Use this architecture when animation consists of reusable scripted operations
and controller events. Avoid its unchecked byte cursor for arbitrary data or
strictly bounded latency. Define a grammar, bounds and per-call work limit;
verify draw/restore ownership before adding more layers.

## References and related techniques

- [Routine inventory](../analyses/laigle-dor/routines.md).
- [ORIC-0001: position-bearing backgrounds](ORIC-0001-background-pages-with-position-metadata.md).
- [MOS 6502 audit](../analyses/laigle-dor/cpu-techniques.md).
- Initial repository search found no existing equivalent technique record;
  this is new repository knowledge, not a claim of global invention.
