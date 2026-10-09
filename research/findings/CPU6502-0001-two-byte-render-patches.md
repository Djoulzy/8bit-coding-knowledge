---
id: CPU6502-0001
title: "Equal-width NOP/ORA patches for a shared pixel loop"
category: graphics
cpu: ["6502"]
machines: ["oric-1", "oric-atmos"]
status: analyzed
source_analyses: ["../analyses/laigle-dor/overview.md"]
tags: [self-modifying-code, compositing, instruction-selection]
promotion_decision: deferred
integration_review: "../analyses/laigle-dor/integration-review.md"
---

# Equal-width patches in a pixel loop

## Summary

**Classification: MOS 6502 technique.** A two-byte site inside a copy loop holds
either two one-byte NOPs or `ORA (screen_pointer),Y`. Switching those bytes
selects opaque copying or OR composition while preserving instruction layout
and avoiding a mode test on every pixel byte.

## Problem and context

- **Problem being solved:** share row traversal between two composition modes.
- **Typical use cases:** writable machine-code renderers with infrequent mode
  changes and many byte transfers.
- **Assumptions / preconditions:** code in RAM, no concurrent execution while
  patching, compatible source/destination encoding, stable two-byte layout.
- **CPU variants and target machines:** documented NMOS 6502 on Oric; the idea
  is CPU-specific, while Oric byte attributes constrain this instance.

## Provenance

| Field | Value |
| --- | --- |
| Original program | L'Aigle d'Or, AIGLEDOR.2 |
| Author / publisher | Loader credits ROCQUES Louis-Marie; Loriciels, March 1984 |
| Source URL / archive | Download origin unknown; [local TAP](<../sources/Oric/L'Aigle d'Or/Aigle D'or, Le (1984)(Loriciels).tap>) |
| License / usage conditions | No license grant found; original reproduction restriction |
| Source revision / checksum | TAP SHA-256 `7f01e1a3d05825aab887952cd5711bea69d6525730aba5c1e25c814334fe77d7` |
| File and routine | B2 BASIC 3/4; renderer `$3E52–$3E77` |
| Line range / symbols / address | BASIC records `$054E/$0561`, TAP `$003AB4/$003AC7`; patch `$3E56–$3E57`, TAP `$0073BC–$0073BD` |
| First analysis | [CPU audit C02](../analyses/laigle-dor/cpu-techniques.md#c02-two-byte-patch-sites-in-hot-loops) |

## Original implementation

Assembler dialect and historical symbols are unknown. The observed bytes are
summarized rather than copying a source section:

| BASIC value written little-endian | Bytes | Decoded operation |
| --- | --- | --- |
| `$EAEA` | `$EA,$EA` | NOP; NOP |
| `$6211` | `$11,$62` | ORA using zero-page pointer `$62/$63`, indexed by Y |

The site follows a source load and precedes the destination store. Width is
in `$64`; the loop copies Y offsets `width ... 1`. The loaded image initially
contains the NOP pair.

## Technical explanation

In opaque mode A remains the source byte. In OR mode A becomes source OR
existing destination. Both modes then execute the same store, countdown and
row-pointer updates. Equal instruction length preserves every following address
and relative branch. A likely reason is code sharing without per-byte dispatch;
the bytes do not establish that this is the fastest possible renderer.

`$3E80` is a second NOP pair reset by BASIC 105 with decimal 60138 (`$EAEA`).
No active branch substitution at that second site was found; it is not evidence
of another enabled composition mode.

## CPU-specific considerations

- **Registers and flags:** A is transformed; ORA updates N/Z, leaves C/V;
  NOPs leave flags. DEY supplies the loop branch's Z flag.
- **Addressing modes:** source and optional screen reads use `(zp),Y`, as does
  the destination store.
- **Instruction compatibility:** these opcode values are documented NMOS 6502;
  later processors were not tested.
- **Page boundaries, branch timing, interrupts:** indexed reads add a cycle
  on crossing; store is fixed-cycle; same-page taken BNE adds one cycle.
- **Code and data alignment:** the observed inner-loop branch stays in page
  `$3E`; data alignment varies with the rectangle's position.

## Machine-specific considerations

Oric HIRES bytes contain pixel/control bits. OR is additive bit composition,
not general masked transparency; ORing serial attributes can alter their
meaning. Writable code resides in application RAM; scratch pointers overlap
firmware workspace. No custom IRQ renderer was identified, but patch safety
must be checked against the actual firmware/extensions.

## Performance and resource costs

| Metric | Original | Alternative | Evidence / method |
| --- | --- | --- | --- |
| CPU cycles per taken pixel iteration | Opaque `20 + source_read_cross`; OR `21 + source_read_cross + screen_read_cross` | Separate loops or mode branch not measured | MOS table calculation for `$3E54–$3E5C`; excludes LDY and row updates |
| CPU cycles final pixel | One less than the corresponding taken iteration | Not measured | BNE not taken |
| Patch-site size | 2 bytes | Two dedicated loops require more code; exact size unknown | Observed bytes |
| RAM / zero-page usage | Shared pointers `$60–$63`, dimensions `$64/$65` | Unknown | Existing renderer arguments, no mode variable in inner loop |
| ROM usage | None in the inner loop | Unknown | Static instruction path |

The opaque NOPs themselves cost four cycles per byte; a dedicated opaque loop
could remove that cost. Patching/setup, BASIC overhead and interrupts are
excluded. These are theoretical counts, not measured speedups.

## Advantages

- Shares the traversal and pointer updates.
- Keeps binary layout stable between modes.
- Avoids testing a composition flag for each byte.

## Limitations and risks

- Two stores do not make an atomic two-byte patch; interrupted execution can
  observe an inconsistent opcode/operand pair.
- Code must be writable and the two modes must share correct flag contracts.
- The NOP mode retains work that a dedicated loop can eliminate.
- OR composition does not implement erase, alpha or arbitrary color blending.

## Alternatives

Use separate opaque/OR workers selected once per rectangle, patch a wrapper's
call target, or branch once per row. Compare code space, setup cost and bytes
drawn, including source/destination alignment.

## Validation record

- **Current status:** analyzed.
- **Source-based evidence:** two BASIC DOKEs, exact patch bytes and surrounding
  load/store/countdown instructions.
- **Theoretical analysis:** decoded instruction lengths, flag effects and
  conditional instruction-table counts.
- **Benchmark setup / commands / environment:** none; static byte assertions in
  `python3 research/analyses/laigle-dor/tools/verify_analysis.py`.
- **Expected result versus actual result:** the byte values decode to the two
  specified modes; no rendered frame or runtime performance was measured.
- **Real-hardware confirmation:** none.
- **Outstanding questions:** all patch/draw ordering, attribute safety and
  concurrent firmware behavior.

## Recommendation for new projects

Use equal-width patches only where writable code and exclusive execution are
deliberate constraints, after comparing a once-per-rectangle dispatch. Avoid
them for ROM code, reentrant rendering or unverified concurrent callers. Define
the flag contract and check both operand encodings before use.

## References and related techniques

- [MOS Technology instruction summary](https://ftpmirror.your.org/pub/misc/bitsavers/components/mosTechnology/6502_Instruction_Set_Summary.pdf).
- [Oric attribute constraints](../analyses/laigle-dor/hardware-techniques.md#h02-attributes-emitted-beside-sprite-rows).
- [6502 analysis instructions](../../docs/cpu/6502/AGENTS.md).
- No equivalent repository record existed at initialization; self-modifying
  code itself is an established technique, not a new invention claimed here.
