---
id: ANALYSIS-ORIC-0002-CPU
program: "Vip4 Demo / Quintessential"
cpu: ["6502"]
machines: ["oric-unspecified", "microdisc"]
analysis_status: draft
source_revision: "sha256:555e811187069b29bfc6cf657be7f19f8c49aa8d25fbbeeb8ab4718ad2577558"
analysis_date: "2026-10-09"
---

# CPU techniques

## 5. Findings and compatibility

Locations use the [overview's binary convention](overview.md#references-and-precise-location-convention).
The [routine index](routines.md) supplies original disk offsets; generated
listings supply each instruction offset. Source is always the unchanged
`research/sources/Oric/Vip4 Demo/vip4.dsk`. All discussed instructions are
documented NMOS 6502 instructions. No later-CPU performance or portability test
was performed. Decimal-mode assumptions are explicit wherever ADC/SBC is used.

### C01: Operand bytes as persistent state in zero-page code

**Analyzed; CPU6502-0005.** M02:$9D4A–$9D6E copies a full page from `$9D87`
to `$0000`, after patching the source LDA operand to `$1000`. Executed at zero,
the LDA at `$09` has operand bytes `$0A/$0B`; the second handler increments
those bytes with zero-page INC. The first handler stores its byte at `$2F`,
the operand of `LDA #value` in the second handler. Separate pointer/state
variables and an indirect read are avoided by reusing executable bytes.

M13:$609B–$60CA extends this scheme. Relocated `$0018/$0019` hold the absolute
sample address, `$26` is both the operand of `LDA #phase` and the value shifted
by `LSR $26`, and `$3E` is a saved-A immediate operand. The IRQ begins `STA $3E`
and ends `LDA #saved_A; RTI`. It does not touch X/Y. The first LSR changes phase
2 to 1 (C=0); the next changes 1 to 0 (C=1), selects the high nibble, then falls
through the now-zero LDA/BNE to reset phase to 2 and advance the pointer.
The branch's changing condition follows from its patched immediate operand.

The advantage comes from zero-page **writes to state**, not from fetching code
in zero page: an absolute LDA still takes four cycles. Safe use needs private
writable code/state, nonnested execution and no concurrent operand writes.
The sample setup overwrites all 256 zero-page bytes, including firmware workspace.
See the [dedicated fiche](../../findings/CPU6502-0005-zero-page-code-operands-as-state.md).

### C02: IRQ frame discard followed by RTS

**Analyzed instruction semantics; activation unresolved; CPU6502-0006.**
Boot:$A869–$A876 and R:$FA7F–$FA8D contain three PLA instructions, hardware
control/status access and RTS. IRQ pushes PC high, PC low and P. Three pulls
discard these, leaving the interrupted subroutine's JSR return address for
RTS. This returns to its caller rather than the interrupted PC. P is not
restored, I remains set, and the nearest active JSR frame determines the target.
An IRQ inside a nested wait helper would escape that helper, not necessarily
the entire sector reader.

However, R:$FA9F starts SEI, installs the handler, calls its load workers and
returns without CLI. The byte polling loop has no CLI either. Thus a maskable
disk IRQ cannot reach this escape handler on that traced path. Boot loading is
also entered with SEI. The mechanism is configured historical code with clear
CPU semantics, **not evidence of a functioning interrupt-driven disk transfer**.
No NMI linkage or unexamined external caller establishes activation. See
[CPU6502-0006](../../findings/CPU6502-0006-irq-frame-discard-and-rts.md).

### C03: Patched absolute addressing and calls

**Analyzed, established self-modification pattern; no new generic fiche.**
R:$FAAF–$FAC0 patches the JSR at `$FAF7` and STA absolute,Y at `$FA73` from
parallel address arrays. R:$FA96 increments only the store operand's high byte
between pages. Low load bytes `$00` and `$FD` both occur. Loading `$0FFD` with
256-byte sectors is valid: every page retains low `$FD`, giving contiguous
loaded bytes despite unaligned stores. Absolute indexed stores have fixed
instruction timing, including their dummy bus access; this is RAM, not an
arbitrary I/O destination contract.

M01:$1000–$1030 (also `$03/$09/$0F/$14`) patches its absolute source and screen
operands after each row. Width and height are bytes at `$104A/$104B`; this
instance is 40 by 200. X traverses width-1 down to zero using BPL. A hot taken
iteration costs `14 + read_cross` cycles and the final costs `13 + read_cross`:
LDA absolute,X, STA absolute,X, DEX, BPL. The branch stays within page `$10`.
These counts exclude row setup and address patching. Comparable indirect-indexed
load/store operations alone cost two extra cycles per byte but use smaller
instructions; full routine performance also includes pointer setup.

The signed countdown only handles widths 1–129: width 129 first visits X=`$80`, then X=`$7F...$00`.
Width 0 or greater than 129 does not implement a general unsigned rectangle copy. Height 0 causes
256 rows. The source and destination operands remain advanced after return;
reentry requires a reset or reload. This differs from
[CPU6502-0001](../../findings/CPU6502-0001-two-byte-render-patches.md), which changes
the operation itself while preserving a two-byte patch site's layout.

### C04: Partial unrolling and overlapping tail stores

**Analyzed; related to CPU6502-0004.** R:$FB23–$FB84 performs 32 absolute,X
stores per index. X begins zero, then DEX/BNE visits `0,255,...,1`, a full page.
Most stores target page-aligned bases `$A000` through `$BE00`; the final base is
`$BE40`. This fills exactly `$A000–$BF3F`: 8,000 unique bytes with 8,192 stores.
Overwriting 192 bytes twice avoids a separate 64-byte tail loop.

For fixed 32 stores, DEX and same-page BNE, the routine totals **42,249 cycles**
including initial LDA/LDX and RTS, excluding caller JSR and IRQs. The final
branch is not taken. Stores never acquire a read-style page-cross penalty.
This is a constant-fill specialization, not a memmove or proof of fastest clear.
Compare a 31-page fill plus tail, indirect fill or generated unroll with equal
screen boundaries and code space. The existing
[descending-page-copy guideline](../../../docs/cpu/6502/descending-page-copy.md)
covers the counter idiom and disjoint RAM constraints; copying and filling are
not interchangeable benchmark results.

### C05: Carry and byte arithmetic contracts

M0B:$88B5–$88C7 uses `CMP #$80; ROL A` twice. Each compare places the original
high bit in carry, so the rotations are circular left rotations of A, not
ordinary shifts through arbitrary incoming carry. The low/high fields then
form a split increment at `$87EC/$87ED`. This confirms deliberate carry use
related to [CPU6502-0003](../../../docs/cpu/6502/carry-stream-field-extraction.md)
without duplicating that destructive field-extraction algorithm.

M0B:$883B–$88A1 combines low/high lookup tables, patches a source address and
copies a 29-byte row to a patched destination. Destination stride `$78` is
120 bytes, or three Oric scanlines. It repeats 66 rows. A fractional phase
accumulator at `$87EF` contributes carry to `$87F0`, producing a fixed-point
table traversal. Tables and destination patching remove repeated multiplication;
their exact phase/texture semantics are not completely decoded.

Potentially fragile carry uses include R:$FBDA–$FBE2 (ADC `$7D` with no CLC)
and M13:$60F1–$60FB (row stride ADC `$28` with no local CLC). Neither should be
silently translated as an unconditional ordinary addition. The latter's entry
carry is unresolved. R:$FB87's first fill covers `$A000–$BFFF`; its later fill
uses 64 chunks of 125 bytes. Carry variation changes chunk placement, so its
first fill is relevant when assessing resulting initialization coverage.
None of the inspected entry sequences establishes CLD explicitly: binary
arithmetic relies on inherited D=0 unless an unexamined path establishes it.

### C06: Static anomalies and optimization hypotheses

- M01:$1038–$103C initializes X to `$4F` and decrements twice per iteration.
  An odd value remains odd modulo 256, so it never becomes zero. No call to
  this delay was found in the inspected picture entry, which returns at `$1030`.
  This is a dormant hazard, not a demonstrated demo hang.
- R:$FA8E writes 4 into `$FC8E` for each page, but `$FA93–$FA9E` does not inspect
  status, decrement that counter or retry. The name "retry" cannot be inferred
  from a variable alone. Boot's separate helper does inspect status and decrement
  its attempt variable; its initial value comes from A (5 on the entry path),
  while `LDY #$04` is overwritten by the transfer.
- R:$FBE8–$FC00 preserves A/X/Y and runs 256 by 256 countdown loops with four
  NOPs in the inner body. It costs **853,540 theoretical cycles**, including
  register save/restore and RTS, excluding caller JSR and any interrupts.
  It is not a frame-synchronization primitive; IRQs stretch elapsed time.
- M0D:$1026–$102F starts X=`$28` and copies offsets 40 down to 0, **41 bytes**.
  The extra byte overlaps the next 40-byte row. Its first pass has 200 rows,
  so the last store reaches `$BF40`. A local width reduction could eliminate
  that overlap, but intended border/attribute behavior must be checked first.

## 6. Performance and verification

The [MOS instruction summary](https://ftpmirror.your.org/pub/misc/bitsavers/components/mosTechnology/6502_Instruction_Set_Summary.pdf)
is the timing/flag reference. Calculations count addressing modes, taken and
final branches, and indexed-read page crossings. No whole-demo timing, loader
throughput or frame-rate benchmark is claimed. Verification models test byte
arithmetic, loop coverage and stack shape; they do not simulate hardware.

## 7–9. Comparisons, proposed changes and next tests

Retain the existing renderer, carry and page-copy IDs; add only C01/C02 fiches.
Before optimizing, trace interrupt ownership, live operand modifications and
render outputs. Useful controlled comparisons are absolute patched versus
indirect row copies, unrolled-overlap versus exact-tail clears, and independent
pointer/state versus executable operand storage. Measure code bytes, setup,
page placement, scratch ownership, frame consistency and IRQ interference.
