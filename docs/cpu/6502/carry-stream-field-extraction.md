---
id: CPU6502-0003
title: "Extracting high-to-low packed fields through carry"
category: bit-manipulation
cpu: ["6502"]
machines: []
status: validated
validation_scope: "Correct extraction of four two-bit fields from a byte, using the documented NMOS 6502 instruction semantics"
source_analyses: ["../../../research/analyses/laigle-dor/overview.md"]
tags: [carry, rotation, packed-data, register-preservation]
review_date: "2026-10-09"
---

# Extracting packed fields through carry

## Summary

Alternate a left rotation of a source byte with a left rotation of a cleared
accumulator to collect the source's high bits. The analyzed two-bit helper
correctly extracts four fields in high-to-low order while preserving X and Y.
This validates a bit-decoding option, not its superiority over masks and shifts.

## Problem and context

- **Problem being solved:** unpack consecutive high-to-low fields while retaining
  an index register needed by the record decoder.
- **Typical use cases:** fixed two-bit fields in compact byte records.
- **Assumptions / preconditions:** writable private source byte in zero page;
  A cleared before each field; uninterrupted carry/register/scratch ownership.
- **CPU variants and target machines:** documented NMOS 6502; other variants must
  have their instruction/bus timing checked separately.

## Provenance

| Field | Value |
| --- | --- |
| Original program | L'Aigle d'Or, AIGLEDOR.2 |
| Author / publisher | Loader credits ROCQUES Louis-Marie; Loriciels, March 1984 |
| Source URL / archive | Download origin unknown; [local TAP](<../../../research/sources/Oric/L'Aigle d'Or/Aigle D'or, Le (1984)(Loriciels).tap>) |
| License / usage conditions | No license grant found; original reproduction restriction |
| Source revision / checksum | TAP SHA-256 `7f01e1a3d05825aab887952cd5711bea69d6525730aba5c1e25c814334fe77d7` |
| File and routine | B2 helper `$3F0B–$3F13`, called by room decoder `$3F14` |
| Line range / symbols / address | Helper TAP `$007471–$007479`; analytical observation C04 |
| First analysis | [CPU audit C04](../../../research/analyses/laigle-dor/cpu-techniques.md#c04-carry-stream-unpacking) |

## Original implementation

The original assembler dialect is unknown. The helper clears A, then performs
two pairs of `ROL` on zero-page byte `$71` and `ROL A`, and returns. This brief
behavioral description replaces an original source excerpt; its nine exact
bytes are asserted by the verification tools.

## Technical explanation

The first source rotation emits original bit 7 into C; the next accumulator
rotation appends it. The second pair appends original bit 6, giving
`A = 2*bit7 + bit6`. Incoming C enters the source's low end and cannot reach
the extracted high bits within those two source rotations.

Call this helper four times, clearing A each time. The successive results are
`(original >> 6)&$03`, `(original >> 4)&$03`, `(original >> 2)&$03` and
`original&$03`. These eight source rotations consume all original bits before
the initially injected carry could emerge. The source is destroyed; its final
value can depend on incoming carry. It is not guaranteed to become zero.

For wider/general fields, prove separately that the result fits and injected
bits cannot contaminate the extracted span. When accumulating into an existing
destination byte, clear it first or define its previous content explicitly.

## CPU-specific considerations

- **Registers and flags:** A returns `$00–$03`; X/Y are preserved. Final C=0,
  N=0, Z reflects A; V/D/I are unchanged. The source byte is modified.
- **Addressing modes:** zero-page read-modify-write plus accumulator rotation.
- **Instruction compatibility:** only documented NMOS instructions; decimal mode
  does not affect ROL, so no CLD is needed for this helper itself.
- **Page boundaries, branch timing, interrupts:** no branch or indexed access
  inside the helper. IRQ/NMI must preserve live registers/status and not modify
  scratch; saving processor status alone does not preserve A/X/Y.
- **Code and data alignment:** no code-page timing requirement; source must be
  safe writable RAM, not an I/O register or firmware-owned concurrent workspace.

The [MOS Technology instruction summary](https://ftpmirror.your.org/pub/misc/bitsavers/components/mosTechnology/6502_Instruction_Set_Summary.pdf)
defines the rotation/flag behavior and instruction costs used here.

## Machine-specific considerations

None for the algorithm. `$71` is the historical address, not a generally free
Oric zero-page allocation. Verify each machine's ROM/interrupt ownership before
choosing scratch storage. Room field meanings belong to the original game.

## Performance and resource costs

| Metric | Original | Alternative | Evidence / method |
| --- | --- | --- | --- |
| CPU cycles per field | 22 including RTS, excluding caller JSR; 28 including JSR | Mask/shift sequences not benchmarked | `2 + 2*(5+2) + 6`; uninterrupted NMOS table calculation |
| Code size | 9 bytes | Depends on inline masking and register requirements | Exact helper range |
| RAM / zero-page usage | One destructive source byte; A result, normal return stack | May preserve original data at extra cost | Instruction operands |
| ROM usage | None | None required | Pure CPU algorithm |

## Advantages

- Decodes high-to-low fields with one shared helper.
- Preserves X/Y for indexing the current record.
- Does not require a known incoming carry for these four two-bit fields.

## Limitations and risks

- Destroys the packed source; save it if later users need the original.
- Clearing the result is essential; arbitrary field widths need a new proof.
- Repeated calls cost time and stack nesting; inline masks may be preferable.
- Shared scratch and unpreserved interrupt registers break the contract.

## Alternatives

Use LSR/masks for a few fixed fields, specialized inline decoding for hot paths,
or a lookup table when its memory cost is justified. Compare actual register
contracts and code plus table space before making a speed recommendation.

## Validation record

- **Current status:** validated for the stated two-bit algorithm and clobbers.
- **Source-based evidence:** exact helper bytes and callers in the room decoder.
- **Theoretical analysis:** carry-flow proof plus documented ISA/flag semantics.
- **Benchmark setup / commands / environment:** no benchmark; run
  `python3 research/analyses/laigle-dor/tools/verify_integration.py`.
- **Expected result versus actual result:** all 512 single-call cases and 512
  four-field sequences agree with independent mask/shift oracles for every byte
  and both incoming C states; [results](../../../research/analyses/laigle-dor/integration-verification.json).
- **Real-hardware confirmation:** none; models do not execute the processor.
- **Outstanding questions:** comparative speed, game IRQ ownership and the full
  room decoder remain outside this validation.

## Recommendation for new projects

Use this as a decoding option when consuming high-to-low two-bit fields and
preserving X/Y matter. Allocate private scratch and document clobbers. Avoid it
when the source must survive or benchmarked mask/shift code better fits the hot
path. Generalize only after proving bit order and field width.

## References and related techniques

- [Packed room representation](../../../research/analyses/laigle-dor/architecture.md#packed-room-data).
- [Integration review](../../../research/analyses/laigle-dor/integration-review.md).
- [Functional verification tool](../../../research/analyses/laigle-dor/tools/verify_integration.py).
