---
record_type: machine-topic-guide
topic: cpu-and-memory
machines: ["oric-1", "oric-atmos"]
cpu: ["6502"]
status: mixed
review_date: "2026-10-11"
---

# Oric CPU, memory and interrupt contracts

This guide applies validated general/NMOS 6502 rules to Oric projects and keeps
historical low-level experiments separate. It does not define a universal Oric
zero-page map or certify a ROM, DOS or interrupt configuration.

## Validated rules

### Extract four high-to-low two-bit fields through carry

**Recommendation:** Use the validated carry-stream helper only when consuming
exactly four high-to-low two-bit fields from a private writable byte and when
destroying that byte is acceptable.

**Why:** Two `ROL` pairs per call move the source's current top two bits into a
cleared accumulator. Across four calls, exhaustive functional checks cover all
256 source bytes and both incoming carry states.

**Prerequisites:** Documented NMOS 6502 instructions; binary-independent `ROL`
semantics; A cleared by the helper; one private writable zero-page source byte;
an IRQ contract that preserves registers/status and does not modify the source.
The historical `$71` address is **not** a generally free Oric allocation.

**Trade-offs:** The source is destroyed and each helper call costs stack/call
overhead. The recorded 22 cycles per field including RTS are a documented
instruction-table calculation, not a benchmark against masks or lookup tables.

**Porting/adaptation:** Allocate the scratch byte through the program's own
Oric/ROM/DOS memory map. Re-prove the carry flow for other field widths or bit
orders and compare complete caller costs before treating it as an optimization.

**Evidence:** [CPU6502-0003](../../../../cpu/6502/carry-stream-field-extraction.md),
[integration review](../../../../../research/analyses/laigle-dor/integration-review.md),
[historical CPU analysis](../../../../../research/analyses/laigle-dor/cpu-techniques.md#c04-carry-stream-unpacking).

### Copy complete disjoint RAM pages with an explicit contract

**Recommendation:** Use the descending-counter page loop only for one or more
complete, aligned, disjoint RAM pages after validating all source, destination,
pointer and page-count ranges.

**Why:** Starting Y at zero and applying `DEY` visits every byte offset exactly
once. Functional models confirm snapshot-equivalent copies for the stated
disjoint-RAM contract.

**Prerequisites:** NMOS 6502; readable/writable ordinary RAM; page-aligned
buffers; no overlap or address wrap; explicit nonzero page count; private
zero-page pointers; no alias with code, stack, screen owner or live state.

**Trade-offs:** This is not overlap-safe, not an empty-length convention and
not a device-copy primitive. Its unusual order may be less convenient than an
ascending loop. The published cycle totals are theoretical and do not prove it
faster than alternatives.

**Porting/adaptation:** On Oric, first exclude ROM/overlay windows, display and
charset regions, firmware workspace and peripheral registers. Select traversal
order from the actual alias/I/O contract, not from historical precedent.

**Evidence:** [CPU6502-0004](../../../../cpu/6502/descending-page-copy.md),
[integration review](../../../../../research/analyses/laigle-dor/integration-review.md),
[historical CPU analysis](../../../../../research/analyses/laigle-dor/cpu-techniques.md#c06-countdown-indexing-and-row-layout).

## Machine constraints

### Reserve low memory and interrupt state explicitly

**Recommendation:** Produce a phase-by-phase ownership table before using zero
page, page `$01`, pages `$02/$04`, ROM workspace or writable interrupt vectors.
Reserve code-patch sites and their operands as state when self-modification is
under evaluation.

**Why:** The evidence contains mutually incompatible ownership models:

- *L'Aigle d'Or* borrows BASIC/ROM workspace and zero-page pointer blocks while
  retaining ROM keyboard, timer and sound services.
- *Space: 1999* takes over low-memory scratch, uses the hardware stack as both
  call/IRQ storage and a token work list, and installs private vectors in
  overlay RAM.
- Vip4 copies an entire sample handler over page zero in one phase and a smaller
  IRQ body over `$0010–$0047` in another.

Addresses that are safe during one takeover phase may corrupt another program
that retains BASIC, ROM, DOS, keyboard, audio or nested interrupts.

**Prerequisites:** Exact model, ROM/DOS/storage configuration, interrupt sources,
NMI policy, call depth and module lifetimes. Vector replacement must be atomic
with respect to every enabled source.

**Trade-offs:** Exclusive takeover can simplify and shorten code but removes
firmware coexistence. Saving/restoring workspaces costs RAM/time and still needs
a defined failure/reset path.

**Porting/adaptation:** Use symbolic allocations and assertions. Measure stack
high-water use with the worst interrupt/output nesting. If firmware services
remain active, verify their documented workspace instead of copying historical
addresses.

**Evidence:** [L'Aigle d'Or architecture](../../../../../research/analyses/laigle-dor/architecture.md),
[Space: 1999 architecture](../../../../../research/analyses/space-1999/architecture.md),
[Vip4 architecture](../../../../../research/analyses/vip4-demo/architecture.md).

### State arithmetic and flag preconditions at API boundaries

**Recommendation:** Every helper that depends on D, C, V, N or an incoming
register value should publish that dependency as part of its calling contract.

**Why:** The analyzed programs contain bounded carry reuse, foreground ADC/SBC
that assumes binary mode, an allegedly unconditional `BVC` without a local V
producer and branch decisions that consume a caller's N flag. These behaviors
may be correct in their complete call paths but are unsafe as implicit reusable
interfaces.

**Prerequisites:** Complete caller/callee flag trace, interrupt policy and the
exact numeric domain. An RTI restores interrupted P; an RTS after IRQ-frame
discard does not.

**Trade-offs:** Explicit `CLC`, `CLD` or comparisons cost bytes/cycles, while an
implicit contract costs auditability and narrows reuse. No universal choice is
validated here.

**Evidence:** [L'Aigle d'Or CPU analysis](../../../../../research/analyses/laigle-dor/cpu-techniques.md#c07-branch-flags-signed-ranges-and-suspicious-sequences),
[Space: 1999 CPU analysis](../../../../../research/analyses/space-1999/cpu-techniques.md#decimal-and-flag-contracts),
[Vip4 CPU analysis](../../../../../research/analyses/vip4-demo/cpu-techniques.md#c05-carry-and-byte-arithmetic-contracts).

## Candidates requiring validation

The mechanisms below are **not yet recommended**.

| Candidate | Potential use | Principal risk | Validation gate |
| --- | --- | --- | --- |
| [CPU6502-0001](../../../../../research/findings/CPU6502-0001-two-byte-render-patches.md) | Select a shared renderer operation without a per-byte mode branch | Multi-byte patches are not atomic; writable/reentrant code and Oric attributes | Trace patch/call exclusion and output, then compare dedicated workers |
| [GEN-0004](../../../../../research/findings/GEN-0004-stack-driven-pair-grammar.md) | Compact repeated text with an explicit LIFO work list | Shares page `$01` with JSR/IRQ frames; malformed grammar can exhaust it | Validate output and worst total stack depth, or use a bounded private stack |
| [CPU6502-0005](../../../../../research/findings/CPU6502-0005-zero-page-code-operands-as-state.md) | Reuse executable operands as compact IRQ state | Nonreentrant code, firmware destruction, initialization and NMI races | Trace complete IRQ execution and compare separate-state design |
| [CPU6502-0006](../../../../../research/findings/CPU6502-0006-irq-frame-discard-and-rts.md) | Escape a polling subroutine on one controlled IRQ | Return target depends on exact stack; P and interrupted work are discarded | Verify every interruptible point, source acknowledgement and rollback path |
| [GEN-0005](../../../../../research/findings/GEN-0005-bit-quota-round-robin.md) | Separate an actor-update quota from a persistent round-robin cursor | Quotas count requests, not elapsed work; callbacks, early exits and other cursor writers affect distribution | Bound complete callback work and cursor ownership; compare scalar counts and test repeated selections |
| [GEN-0006](../../../../../research/findings/GEN-0006-fixed-actor-work-window.md) | Let shared actor routines use a fixed load/process/commit window | Additional scratch and copying; nested selection or IRQ users can destroy unpublished state | Allocate an Oric-owned window, trace every commit and compare complete updates with indexed/indirect records |
| [CPU6502-0007](../../../../../research/findings/CPU6502-0007-inline-stream-return-address.md) | Associate immutable parameters with a JSR through its stacked return address | Missing terminators, shared-pointer reentry and malformed return frames; the observed consumer excludes return page zero and address wrap | Trace every caller and IRQ/NMI interaction, bound data, and compare an explicit pointer or length-prefixed interface |

`CPU6502-0006` has stronger activation evidence in the published
*Space: 1999* disk path than in Vip4, but that does not remove its stack and
device contracts. The [Space analysis](../../../../../research/analyses/space-1999/cpu-techniques.md#disk-irq-completion-returns-out-of-a-polling-function)
keeps the mechanism `analyzed`.

The last three candidates come from Apple II programs, not Oric execution.
[Lode Runner's finding index](../../../../../research/analyses/lode-runner/findings.md)
locates the scheduler at `$6C82–$6CA6` and inline consumers at
`$86E0–$86FF` / `$87E1–$8810`.
[Karateka C01](../../../../../research/analyses/karateka/cpu-techniques.md#c01-fixed-actor-fields-through-a-copied-work-record)
locates the record-transfer workers at `$7071–$70A5`. These are source-program
addresses, not proposed Oric allocations. All three remain `analyzed`;
their original zero-page addresses, firmware assumptions and timing are not
portable defaults. Inline parameter consumption is distinct from both
resumable animation cursors and IRQ-frame discard.

[CPU6502-0002](../../../../../research/findings/CPU6502-0002-rts-in-basic-line-header.md)
is not a candidate for new software. Its value is diagnostic: confirm exact
bytes before declaring a call into tokenized data invalid or intentional.

## Validation backlog

1. Record zero-page, stack, vector and overlay ownership for each supported
   Oric-1/Atmos ROM and storage configuration.
2. Trace D/C/V/N across startup, foreground arithmetic and all IRQ paths.
3. Measure stack high-water use with pair-grammar expansion, printing and the
   maximum gameplay IRQ nesting.
4. Compare patched versus parameterized/dedicated workers using identical
   output, page placement and interrupt conditions.
5. Inject disk completion and failure IRQs at every polling/call depth before
   considering a nonlocal RTS design.
6. For actor quotas, measure worst-case callback work and trace every writer of
   the cursor, including early exits and quotas larger than the actor count.
7. For a fixed actor window, trace all loads/commits and IRQ users; compare the
   complete copy/context/update cost with indexed or indirect record access.
8. For inline parameters, test bounded termination, page crossings, nesting,
   malformed data and restored return addresses under the chosen Oric IRQ/ROM
   contract. No cross-platform candidate above has an Oric execution benchmark.
