---
id: CPU6502-0004
title: "Full-page copying with a descending byte counter"
category: memory
cpu: ["6502"]
machines: []
status: validated
validation_scope: "Full 256-byte traversal and disjoint aligned RAM copying; no memmove, I/O or fastest-copy claim"
source_analyses: ["../../../research/analyses/laigle-dor/overview.md"]
tags: [memory-copy, page-alignment, countdown, bounds]
review_date: "2026-10-09"
---

# Full-page copying with a descending counter

## Summary

Initializing Y to zero and decrementing after each transfer visits
`$00,$FF,$FE,...,$01`, then exits with Y zero. This is a valid full-page copy
for disjoint aligned RAM buffers; zero means 256 transfers, not an empty copy.
Neither overlap safety nor performance superiority is implied.

## Problem and context

- **Problem being solved:** cover a complete 256-byte page with an 8-bit counter.
- **Typical use cases:** reset snapshots and fixed page-sized RAM blocks.
- **Assumptions / preconditions:** aligned readable/writable disjoint buffers;
  no address wrap; exclusive pointers; buffers must not overwrite code, active
  stack, pointer storage or other live state. Ordinary RAM only.
- **CPU variants and target machines:** documented NMOS 6502; allocation and
  bus behavior belong to the target machine.

## Provenance

| Field | Value |
| --- | --- |
| Original program | L'Aigle d'Or, AIGLEDOR.2 |
| Author / publisher | Loader credits ROCQUES Louis-Marie; Loriciels, March 1984 |
| Source URL / archive | Download origin unknown; [local TAP](<../../../research/sources/Oric/L'Aigle d'Or/Aigle D'or, Le (1984)(Loriciels).tap>) |
| License / usage conditions | No license grant found; original reproduction restriction |
| Source revision / checksum | TAP SHA-256 `7f01e1a3d05825aab887952cd5711bea69d6525730aba5c1e25c814334fe77d7` |
| File and routine | B2 replay copy `$4DDD–$4DFD` |
| Line range / symbols / address | TAP `$008343–$008363`; analytical observation C06 |
| First analysis | [CPU audit C06](../../../research/analyses/laigle-dor/cpu-techniques.md#c06-countdown-indexing-and-row-layout) |

## Original implementation

The original copies `$5600–$57FF` to `$5000–$51FF`. It initializes aligned
source/destination pointers, uses LDY/DEY/BNE for each page, increments pointer
high bytes and uses X=`$01` with DEX/BPL to perform two pages. No original
assembler dialect is known; exact routine bytes are checked by the tools.

## Technical explanation

For transfer number `k` from zero through 255, Y is `(-k) modulo 256`. These
256 values are distinct, so every byte is read and written once. The next DEY
returns Y to zero and ends the loop. Since buffers are disjoint, earlier stores
cannot destroy a later source byte; the result equals a source snapshot copied
to the destination.

Illustrative assembler-neutral 6502 notation: `$` is hexadecimal, `#` is
immediate, and labels use a colon. SRC/DST are symbolic zero-page addresses to
resolve in the chosen assembler. This is newly written, not historical source:

```asm
        LDY #$00
copy:   LDA (SRC),Y     ; SRC is a private two-byte zero-page pointer
        STA (DST),Y     ; DST is another private pointer; low bytes both zero
        DEY
        BNE copy
        RTS
```

For multiple pages, advance both high bytes only after completing a page. An
X=`page_count-1` / DEX/BPL outer loop requires `1 <= page_count <= 128`;
zero is not a supported empty request and counts above 128 need another
termination scheme. Check complete ranges and wrap before starting.

## CPU-specific considerations

- **Registers and flags:** the example clobbers A/Y and N/Z, leaves C/V/D
  unchanged; Y returns zero. The historical outer loop also clobbers X/pointers.
- **Addressing modes:** `(zp),Y` source and destination; place each two-byte
  pointer wholly within zero page and reserve it against concurrent use.
- **Instruction compatibility:** documented NMOS instructions only; decimal
  mode does not affect this algorithm.
- **Page boundaries, branch timing, interrupts:** aligned source gives no indexed
  read crossing. Same-page branch means the target and PC **after** BNE share
  a page. IRQ time/clobbers require a separate contract.
- **Code and data alignment:** data alignment simplifies addressing and timing;
  code alignment remains an independent condition.

Timing rules use the [MOS Technology instruction summary](https://ftpmirror.your.org/pub/misc/bitsavers/components/mosTechnology/6502_Instruction_Set_Summary.pdf).

## Machine-specific considerations

There is no ROM requirement. Actual buffers must be RAM and avoid firmware,
screen owners, hardware registers and the routine's live storage. The abstract
model's 128-page case proves counter traversal, not that a machine has 64 KiB
available for two buffers and execution state.

## Performance and resource costs

| Metric | Original | Alternative | Evidence / method |
| --- | --- | --- | --- |
| CPU cycles | Historical two-page routine: 8,249 including setup/RTS, excluding caller JSR and IRQs | Other copy orders/unrolled code not benchmarked | Static instruction-table sum |
| Inner page loop | 4,095 with same-page BNE; add 255 if every taken BNE crosses a code page | Not measured | `256*(5+6+2) + 255*3 + 2`; excludes LDY/RTS and outer loop |
| Code size | Historical routine: 33 bytes; illustrative one-page worker: 10 bytes | Implementation-dependent | Instruction/address sizes |
| RAM / zero-page usage | Historical four pointer bytes plus A/X/Y; copy itself needs no data buffer | Unknown | Source operands |
| ROM usage | None | None required | Pure RAM copy |

All costs above are theoretical. They do not include device wait behavior or
demonstrate that this order is faster than ascending indexing.

## Advantages

- Uses an 8-bit counter to cover every byte in a page.
- Has a simple page-aligned pointer contract and explicit termination.
- Needs no extra temporary page for disjoint RAM copying.

## Limitations and risks

- Not a memmove: nonmonotonic order can corrupt overlapping sources.
- Zero dimensions/counts can become unintended nonempty work.
- I/O and volatile memory may care about access order and bus reads/writes.
- Destination aliases with pointers/code/stack break the algorithm.

## Alternatives

Use INY/BNE for ascending full-page traversal, an explicitly counted loop for
partial pages, or a direction-aware copy for overlap. Benchmark unrolling and
absolute-address loops only after preserving equivalent output and contracts.

## Validation record

- **Current status:** validated for traversal and copying under these conditions.
- **Source-based evidence:** exact historical routine, page addresses and replay
  caller; source/destination ranges are disjoint.
- **Theoretical analysis:** modular-index coverage proof, independent source
  snapshot oracle, documented load/store/branch semantics.
- **Benchmark setup / commands / environment:** no benchmark; run
  `python3 research/analyses/laigle-dor/tools/verify_integration.py`.
- **Expected result versus actual result:** 16 abstract-RAM cases agree with a
  snapshot copy and preserve all other bytes; seven invalid contracts rejected.
  Counts 1, 2, 3 and 128 tested; [results](../../../research/analyses/laigle-dor/integration-verification.json).
- **Real-hardware confirmation:** none; model pointers/counters are external to
  its RAM array, so it cannot prove execution-state placement or IRQ safety.
- **Outstanding questions:** comparative performance and target-machine storage
  ownership require separate measurements/review.

## Recommendation for new projects

Use for explicitly full-page, disjoint RAM operations after proving allocation,
count and scratch ownership. Avoid for partial/empty requests, overlapping
buffers or I/O. Choose traversal order and any unrolling from measured needs;
`validated` means correct under this contract, not fastest.

## References and related techniques

- [Original memory ledger](../../../research/analyses/laigle-dor/architecture.md#complete-loaded-region-ledger).
- [Integration review](../../../research/analyses/laigle-dor/integration-review.md).
- [Functional checks](../../../research/analyses/laigle-dor/tools/verify_integration.py).
