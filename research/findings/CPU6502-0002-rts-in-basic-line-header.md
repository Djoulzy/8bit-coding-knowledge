---
id: CPU6502-0002
title: "An RTS entry aliased onto a BASIC line-number byte"
category: code-layout
cpu: ["6502"]
machines: ["oric-1", "oric-atmos"]
status: analyzed
source_analyses: ["../analyses/laigle-dor/overview.md"]
tags: [code-data-aliasing, basic, absolute-address, historical-anomaly]
promotion_decision: not-recommended
integration_review: "../analyses/laigle-dor/integration-review.md"
---

# RTS entry in a BASIC line header

## Summary

**Classification: MOS 6502 technique / historical layout anomaly.** A BASIC
CALL targets an existing `$60` byte in another BASIC line's number field. As a
6502 entry that byte is RTS and immediately returns; its behavior is established,
while deliberate optimization versus leftover code is unresolved.

## Problem and context

- **Problem being solved:** unknown; the observed effect is a no-op machine entry
  without allocating another instruction byte.
- **Typical use cases:** historical binary analysis and diagnosing odd CALLs;
  no general new-project use is recommended.
- **Assumptions / preconditions:** exact absolute BASIC layout, line number and
  standard CALL return convention must remain intact.
- **CPU variants and target machines:** documented NMOS 6502 RTS opcode on Oric;
  data-layout dependency belongs to this tokenized BASIC image.

## Provenance

| Field | Value |
| --- | --- |
| Original program | L'Aigle d'Or, AIGLEDOR.2 |
| Author / publisher | Loader credits ROCQUES Louis-Marie; Loriciels, March 1984 |
| Source URL / archive | Download origin unknown; [local TAP](<../sources/Oric/L'Aigle d'Or/Aigle D'or, Le (1984)(Loriciels).tap>) |
| License / usage conditions | No license grant found; original reproduction restriction |
| Source revision / checksum | TAP SHA-256 `7f01e1a3d05825aab887952cd5711bea69d6525730aba5c1e25c814334fe77d7` |
| File and routine | B2 BASIC 8205 CALL 8835; target in BASIC line 6240's header |
| Line range / symbols / address | Caller record CPU `$294B`, TAP `$005EB1`; header CPU `$2281`, TAP `$0057E7`; entry CPU `$2283`, TAP `$0057E9` |
| First analysis | [CPU audit C08](../analyses/laigle-dor/cpu-techniques.md#c08-tail-jumps-and-unusual-machine-entry-in-basic-data) |

## Original implementation

No assembler source/dialect exists for this byte alias. The BASIC record at
`$2281` contains a two-byte next-line pointer, followed at `$2283/$2284` by
little-endian line number 6240 = `$1860`. Therefore `$2283` holds `$60`.
The BASIC 8205 record contains decimal CALL 8835 = CPU `$2283` before calling
the actual enemy routine `$4976`.

## Technical explanation

The processor does not distinguish BASIC data from machine instructions. On
entry at `$2283`, the first opcode is documented RTS; it consumes the normal
return address from the stack and returns to the CALL machinery. No BASIC
RETURN token is being executed as machine code: the instruction is the **line
number's low byte**. The distinction matters when reconstructing the target.

This rules out treating the CALL as automatically invalid merely because it
points inside BASIC. It does not prove that the author deliberately reused the
byte. A removed helper, accidental surviving address or intentional no-op remain
possible explanations. No original source revision establishes which one.

## CPU-specific considerations

- **Registers and flags:** RTS preserves A/X/Y and arithmetic flags while
  adjusting SP and PC according to the existing return address.
- **Addressing modes:** implied RTS; the CALL target is a fixed absolute value.
- **Instruction compatibility:** `$60` is documented NMOS RTS; compatible later
  variants were not tested with the surrounding ROM.
- **Page boundaries, branch timing, interrupts:** no branch/read-index penalty
  in RTS itself; CALL interpreter overhead and IRQ interference remain.
- **Code and data alignment:** one exact byte location, not an aligned routine;
  inserting/editing BASIC lines can relocate it.

## Machine-specific considerations

Oric tokenized lines carry absolute link pointers and little-endian line numbers.
The game's load base `$0501` and exact preceding records fix this entry's
address. A BASIC text export/reload or renumber operation need not preserve it.
The original binary must remain the reference artifact.

## Performance and resource costs

| Metric | Original | Alternative | Evidence / method |
| --- | --- | --- | --- |
| CPU cycles | RTS itself: 6 theoretical cycles; total CALL not measured | Removing the no-op CALL / explicit stub not measured | MOS instruction table |
| Code size | One existing data byte; zero extra routine bytes allocated | Explicit stub requires at least one instruction byte | Exact header byte |
| RAM / zero-page usage | Normal return stack; no dedicated scratch in this byte | Unknown | RTS semantics; ROM CALL internals not modeled |
| ROM usage | BASIC CALL implementation remains necessary | Unknown | Source caller |

Zero extra routine bytes do not make the whole operation faster than omitting
the call. No speed optimization is claimed.

## Advantages

- The existing binary has a valid immediate-return target at the odd address.
- It demonstrates why unusual references must be checked against exact bytes.

## Limitations and risks

- Strong coupling to BASIC record order, load base and line numbering.
- No named symbol or source evidence documenting the intended contract.
- An edit can transform the target into unrelated instructions or operands.
- Static correctness of the byte does not establish runtime reachability.

## Alternatives

Omit a no-op CALL, use an explicit labeled RTS stub, or represent an optional
callback with a documented dispatch mechanism. These choices avoid accidental
dependence on language data layout.

## Validation record

- **Current status:** analyzed for byte behavior; author intent remains observed
  and unresolved.
- **Source-based evidence:** CALL operand, linked BASIC header and `$60` byte.
- **Theoretical analysis:** documented RTS and normal CALL return behavior.
- **Benchmark setup / commands / environment:** no benchmark; exact byte assertion
  in `python3 research/analyses/laigle-dor/tools/verify_analysis.py`.
- **Expected result versus actual result:** the target byte is `$60`; no runtime
  trace of BASIC 8205 has been captured.
- **Real-hardware confirmation:** none.
- **Outstanding questions:** deliberate trick or remnant, original helper history,
  runtime reachability and caller's reason for retaining a no-op.

## Recommendation for new projects

Do not reproduce this incidental data alias as a general coding recommendation.
Use it as an analysis lesson: establish exact bytes and call semantics before
labeling an odd entry invalid or optimized. For new code use explicit symbols.

## References and related techniques

- [BASIC reconstruction](../analyses/laigle-dor/extracted/aigledor.2.basic.txt).
- [MOS Technology instruction summary](https://ftpmirror.your.org/pub/misc/bitsavers/components/mosTechnology/6502_Instruction_Set_Summary.pdf).
- [Verification result](../analyses/laigle-dor/verification.json).
- No repository duplicate existed; no claim of original invention is made.
