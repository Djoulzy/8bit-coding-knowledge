---
id: ANALYSIS-ORIC-0001-CPU
program: "L'Aigle d'Or"
cpu: ["6502"]
machines: ["oric-1", "oric-atmos"]
analysis_status: draft
source_revision: "sha256:7f01e1a3d05825aab887952cd5711bea69d6525730aba5c1e25c814334fe77d7"
analysis_date: "2026-10-09"
---

# MOS 6502 techniques and optimization audit

## Evidence and applicability

All findings below are `analyzed` unless explicitly marked `observed`. References
use B2 addresses and the [TAP mapping](overview.md#precise-reference-convention).
The reconstructed instructions are documented NMOS 6502 instructions. The
original assembler syntax is unknown. There are no existing repository technique
guidelines to confirm; these are new local research observations, not claims of
invention or globally optimal implementations.

Subsequent integration promoted the narrowly specified C04 field extractor and
C06 full-page copy into [CPU6502-0003](../../../docs/cpu/6502/carry-stream-field-extraction.md)
and [CPU6502-0004](../../../docs/cpu/6502/descending-page-copy.md). The broader
historical runtime claims remain analyzed; see [the review](integration-review.md).

Opcode/flag and cycle references use the primary
[MOS Technology instruction summary](https://ftpmirror.your.org/pub/misc/bitsavers/components/mosTechnology/6502_Instruction_Set_Summary.pdf).
Counts are theoretical CPU cycles, exclude CALL/BASIC overhead and interrupts,
and require binary arithmetic where ADC/SBC is involved. No wall-clock or
benchmark result is claimed.

## C01: Zero-page parameter blocks and register roles

`$3E3B–$3E77` transfers descriptor fields into `$60–$65`, then uses `(zp),Y`
loads/stores for arbitrary image and display addresses. `$66/$67` adds a saved
background pointer; `$74/$75` indexes animation streams. A carries pixel/data
bytes, Y traverses rows or stream fields, and X selects a descriptor or counts
multiply iterations. The code avoids general register preservation when the
caller already knows these values are disposable.

Benefits are short pointer accesses and reusable loops. Costs are destructive
argument updates and non-reentrancy. The region `$35–$84` is also a BASIC input
buffer/workspace according to the [Atmos manual](https://library.defence-force.org/books/content/manual_atmos.pdf),
chapter 10. The fact these calls borrow its bytes does not reserve them against
ROM, keyboard, expression or interrupt use. Test ownership across each ROM call.
CPU-generic pointer use is reusable; the exact addresses are Oric/BASIC-specific.

## C02: Two-byte patch sites in hot loops

BASIC 3/4 writes `$EAEA` or `$6211` at `$3E56`. In little-endian memory these
are `$EA,$EA` (two NOPs) or `$11,$62` (`ORA ($62),Y`). Both occupy two bytes,
leaving subsequent addresses and relative branches stable. Thus `$3E52` can
copy pixels directly or OR the source with the screen without testing a mode
flag for every byte. The image currently holds NOPs. `$3E80` is another NOP
pair reset by BASIC 105 using decimal 60138, which is `$EAEA`; no active branch
patch there was found.

The NOP pair costs 4 cycles. The ORA costs 5 plus a destination read page-crossing
cycle. Opaque pixel iterations of `$3E54–$3E5C` cost 20 cycles plus source
crossing when the branch is taken; the final pixel costs 19 plus crossing.
OR iterations cost 21 plus source and destination read-crossing penalties, or
20 on the final pixel. These values exclude LDY, pointer updates and row control.

This is genuine self-modifying code, not just modifying pointer data. Its
probable motivation is sharing the renderer while avoiding a per-pixel dispatch.
Dedicated renderer entry points could eliminate the opaque NOP overhead at the
cost of more code. Patching is not atomic as a pair of byte stores; it is safe
only when no concurrent path executes the changed instructions. No game IRQ
renderer is identified, but absence alone does not prove this precondition for
all firmware/extensions. See [CPU6502-0001](../../findings/CPU6502-0001-two-byte-render-patches.md).

## C03: Page-aligned field arrays

`$3E3B–$3E51` loads high source, low source, height and width using X at `$9700`,
`$9600`, `$9500`, `$9400`. Splitting fields into aligned pages means a byte index
can directly select each field without multiplying a record index or carrying
to another page. These four LDA absolute,X reads never cross a page for X in
`$00–$FF`. Including LDX zero-page, four LDA absolute,X / STA zero-page pairs
and RTS, the loader is 37 cycles and 23 bytes.

Advantages: simple constant indexed-read timing and a shared descriptor format
for assets and mutable background buffers. Limitations: 1,024 bytes allocated
to four pages, many entries unused, and mutable descriptors mixing dimensions
with buffer lifetime. An interleaved structure can be denser for a small atlas
but needs different indexing. This familiar technique is explained here without
creating a redundant standalone record.

## C04: Carry-stream unpacking

`$3F0B–$3F13` clears A and alternates `ROL $71` with `ROL A` twice. Each memory
rotation emits a high bit into carry; the next accumulator rotation appends it
to the result. Incoming carry changes the low end of `$71` but does not affect
the extracted high bits during these two iterations. Four consecutive calls
therefore extract the original byte's four high-to-low two-bit fields correctly.
The routine preserves X, used as the record index, and costs 22 cycles excluding
JSR. Larger decode sequences use single-bit rotations into cleared absolute
destinations. Clearing the destination state at `$3F14` is an essential invariant.

This saves explicit masks/shifts for different field positions, but the helper
destroys its input and repeated JSR overhead may be slower than specialized
masking. No optimality claim follows. `$3FB6–$3FCF` extends the pattern to two
flags and two three-bit fields for packed room state. CPU applicability is NMOS
6502 carry/rotation semantics; room meanings belong to this game.

## C05: General multiplication used for a constant stride

`$3E00–$3E17` is unsigned 8×8 → 16 multiplication. `$71` is shifted right to
test multiplier bits; conditional addition enters A; ROR A/ROR `$72` shifts the
partial product down while retaining addition carry. `$73:$72` holds the result,
also returned as A:Y. It uses eight iterations, four zero-page bytes `$70–$73`,
and A/X/Y. The shifted multiplier is destroyed.

`$3E21` sets the multiplier to `$28`, computes `40*y`, adds `$A0` to the high
byte, then adds byte-column x to the low byte with final carry propagation.
Adding high first is valid here because `(40*y >> 8) + $A0` cannot overflow
for byte-valued y. That ADC therefore leaves carry clear; TYA preserves it,
allowing the low-byte ADC to omit a second CLC. This is an implicit optimization
based on the bounded operands and A:Y multiply result. Arbitrary 16-bit base
addition cannot blindly use this order or carry assumption.

The multiplication model passed all 65,536 unsigned byte pairs; address arithmetic
passed all 8,000 visible byte positions. These are static binary-mode models,
not CPU-emulator executions. Decimal mode must be clear; the helpers do not
issue CLD themselves. The binary environment is a firmware precondition.

| Routine | Theoretical cycles / code size | Conditions |
| --- | --- | --- |
| `$3E00` multiply | `178 + 4*popcount(initial $71)`; 178–210 / 24 bytes | Same-page branches; no interrupts; count includes RTS, excludes caller JSR |
| Multiply with `$71=$28` | 186 | Two set multiplier bits; operand values do not change this count |
| `$3E21` address | 227 or 231 / 26 bytes | Includes internal multiply JSR and RTS; low-byte addition without/with carry |

For this constant stride a shift/add sequence or scanline address table may beat
the generic multiply. Count their setup, zero-page, table space and clobbers
before comparing. This is a potential optimization, not a measured recommendation.

## C06: Countdown indexing and row layout

Graphics rows use `LDY width` then `DEY/BNE`, copying offsets `width ... 1`.
The pointer-before-data convention avoids adding/subtracting one on every load
but requires consistent callers. Source is tightly packed, display stride is
`$28`, and saved backgrounds are tightly packed. Width zero traverses 256 bytes
rather than none; height zero executes 256 rows. These are invalid normal inputs,
not empty rectangles.

`$4DDD–$4DFD` uses the related page-copy idiom `LDY #$00`, then DEY/BNE, visiting
`0,255,254,...,1`, all 256 positions exactly once. X starts at 1; DEX/BPL handles
two pages. Source/destination low bytes are zero, so indexed reads never cross
their page. Copying `$5600–$57FF` to `$5000–$51FF` costs 8,249 theoretical cycles
including initialization and RTS. A zero initial counter means a full page here,
unlike an empty high-level loop.

The nonmonotonic order is harmless for disjoint RAM but is not a memmove or an
appropriate generic I/O-copy primitive. Page alignment makes this case simple;
ordinary sprite source/screen pointers often incur indexed-read penalties.

## C07: Branch flags, signed ranges and suspicious sequences

The code frequently uses N immediately after CMP rather than C: `$45E1–$45E7`,
enemy bounds and `$4C00/$4C32/$4C6B`. This is cheap when operand/result ranges
stay within a signed half-range. N alone is not a general signed less-than test
when overflow occurs, and it is not unsigned less-than. For example CMP `$80` /
BPL in `$4AD6–$4ADD` distinguishes timer-byte halves through wraparound; it must
be read as exact byte behavior, not translated naively to a signed comparison.

Several sequences merit scrutiny:

- `$4B50–$4B5E` loads A=`$04` then compares `$8C`; the equality path is impossible
  in these bytes. `$4CB6` is the live pointer helper and correctly reads actor y.
- `$4B8C–$4B94` loads X=`$02` but stores **A**, still `$A0`, into collision result
  `$04C0`. This may still satisfy a nonzero-blocked contract; do not silently
  describe it as storing the constant 2 or assume it breaks gameplay.
- `$4B82–$4B85` stores A then tests N; STA leaves N unchanged. Identified
  directional callers establish N with LDA before JSR. This is an implicit
  caller flag contract, not a self-contained sign test on an arbitrary A input.
- `$3EF5` jumps to `$3EC5`, an operand byte of another JMP, not the ordinary
  draw entry `$3EC6`. No live caller was found; retain as an unresolved remnant.
- `$4AF4–$4AF6` has SEC/SBC `$00`, an arithmetic no-op in binary mode. It may be
  a leftover operand patch point or edit; no surrounding write proving intent
  was found. Do not call it a speed optimization.

These are analyzed byte behaviors; original intent and full reachability are
`observed`/unresolved. None should be repaired in the preserved image.

## C08: Tail jumps and unusual machine entry in BASIC data

`$3EBD/$3EC6/$40B2/$4140/$4840` finish with JMP to a shared worker; its RTS
returns to the original caller. This uses ordinary JSR/RTS stack semantics and
avoids an extra JSR/RTS pair for wrappers. No special stack manipulation was found.

BASIC 8205 CALLs decimal 8835, CPU `$2283`. That byte is `$60`, the low byte of
line number 6240 (`$1860`) in the BASIC line header at `$2281`. It executes RTS
immediately. This is established by the original byte and direct BASIC caller,
not by treating all BASIC bytes as code. It gives a zero-allocation no-op target
but depends on absolute layout and this exact line number. Whether it was a
deliberate trick or a lucky remnant is unknown. See
[CPU6502-0002](../../findings/CPU6502-0002-rts-in-basic-line-header.md).

## C09: Alignment penalty in a 256-byte charset restore

Saving `$B8F0,X` at `$4EEC` reads across a page for X=`$10–$FF`: 240 extra read
cycles. The loop branch stays on one code page. Its 256-byte save costs 3,828
cycles through the final JMP, before the charset clear.

The restore reads aligned `$5900,X`, but its branch at `$4F04` returns to `$4EFD`:
the PC after the branch is `$4F06`, so each of its 255 taken branches crosses a
code page. Restore-loop work after the ROM call costs 3,846 cycles including
LDX and RTS. The routine total is that plus 6 for the ROM JSR plus unknown ROM
execution/interrupt costs. These counts illustrate why data alignment alone does
not settle loop timing. Relocating the branch could save 255 cycles per restore,
but demands a modified executable and verification of absolute references.

## Categories investigated without positive evidence

No established game-owned IRQ/RTI code, undocumented opcodes, explicit stack
trampoline, DMA, generic decompression, bit-shifted sprite cache or intentionally
unrolled high-volume memory copy was found. Room unpacking, victory composition
and some collision probes are manually repeated fixed work; that does not show
why the author chose duplication or prove a benchmark advantage. Aligned tables
are explicit; purposeful code alignment is not established, and the charset
restore actually crosses a code page. Busy waits are cycle-dependent, not
demonstrated video synchronization.

## Benchmark proposals

Measure only after producing a controlled executable and verified ROM setup:
generic multiplication versus stride-specific arithmetic; inline patches versus
separate opaque/OR renderers; aligned versus crossing sprite rows; shifted
charset-restore loop; descriptor layouts with equal atlas capacity. Record
interrupt settings, code/data addresses, bytes, input dimensions, output checks
and emulator/hardware conditions. No technique is promoted to a guideline here.
