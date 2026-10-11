---
id: "ANALYSIS-APPLE2-KARATEKA-CPU"
program: "Karateka"
cpu: ["6502"]
machines: ["apple-iie"]
analysis_status: complete
source_revision: "d02edc77fa0a02d3f679af22456ca1c762c305dc"
analysis_date: "2026-10-11"
---

# MOS 6502 techniques and constraints

Scope/provenance are in [overview](overview.md). References below denote CPU
addresses and zero-based offsets in [the original disk](<../../sources/Apple IIe/Karateka/Karateka (1984)(Broderbund).dsk>),
with bytes in [selected disassembly](extracted/selected-disassembly.txt).
These are documented NMOS instructions in inspected code, not evidence of a
65C02 requirement. Linear data decoding is not an undocumented-opcode finding.

## C01: fixed actor fields through a copied work record

**Evidence:** `$7071–$70A5`, `DSK=$004871–$0048A5`; update caller
`$B584–$B591`, `DSK=$008D84–$008D91`; animation `$6400`, `DSK=$005C00`.
**Level/status:** common pattern with a 6502 implementation; analyzed;
new [GEN-0006](../../findings/GEN-0006-fixed-actor-work-window.md).

Four loops transfer exactly 16 bytes between `$20–$2F` and `$60–$6F` or
`$70–$7F`. The common updater uses direct ZP fields: frame `$20/$21`, position
`$22`, cursors `$25/$26`, steps `$27/$28`, facing sign `$2C`. It can process
either actor without carrying an actor-base index through every field access.
The record load also classifies the other actor and recomputes `$32/$33`;
these tails must be included in a full caller contract and performance comparison.

All three record blocks are in ZP: 32 persistent bytes plus 16 work bytes.
This saves neither the original records nor the copy traffic. On a 6502,
direct ZP loads/stores cost three cycles, ZP,X forms four; using a copied window
can save one cycle for each substituted access, but needs enough subsequent
work to repay copying and context setup. It also simplifies register allocation.

For a commit at `$7071` or `$708D`, the loop and exit are:

| Portion | Table-derived cycles |
| --- | --- |
| LDX immediate | 2 |
| 16 × (LDA zp,X + STA zp,X + INX + CPX immediate) | 16 × (4 + 4 + 2 + 2) = 192 |
| 15 taken same-page BNE, one not taken | 15 × 3 + 2 = 47 |
| Core total | 241 |
| Core + RTS; caller JSR + core + RTS | 247; 253 |

The branch source/target remain within page `$70`. ZP-indexed accesses here
do not wrap across `$FF`; both blocks are disjoint. These counts use the
[MOS instruction table](https://ftpmirror.your.org/pub/misc/bitsavers/components/mosTechnology/6502_Instruction_Set_Summary.pdf)
and assume no interrupt. They are calculations, not measured timings. Two
copy cores alone cost 482 cycles; whole load/update/commit includes additional
calls and tails. Do not quote 253 for a complete load helper.

Loads/stores preserve carry; INX/CPX/branches establish loop termination.
A/X/flags are scratch. An interrupt, nested actor update or renderer sharing
the same fields can corrupt work in progress; no save/restore protocol was
established for such reentry. Keep paired load/process/commit ownership explicit.

## C02: equal-width composition patches

**Evidence:** setup `$1965–$1981`, site `$19E6/$19E7`
(`DSK=$009165`, `$0091E6`); mirrored setup `$1B56–$1B72`, site
`$1BF2/$1BF3` (`DSK=$009356`, `$0093F2`). **Level/status:** CPU; analyzed;
additional instance of [CPU6502-0001](../../findings/CPU6502-0001-two-byte-render-patches.md).

Both sites select a transformation between prepared source A and the final
screen store. The actual mode variable is `$0F`:

| `$0F` | Patched bytes | Operation / isolated cost |
| --- | --- | --- |
| zero | `$11,$00` | ORA (`$00`),Y; 5 cycles + indexed-read page crossing |
| negative | `$31,$00` | AND (`$00`),Y; same conditional cost |
| positive | `$EA,$EA` | NOP; NOP; 4 cycles |

The second adjacent operation is the final STA, not a second unconditional
redundant store. In the captured mirrored bytes both decode as STA, but setup
replaces the first site's bytes before drawing. Mode selection once per draw
avoids a mode branch inside each byte iteration; NOP mode still costs work
that a dedicated opaque loop could omit.

ORA/AND change N/Z and leave C; NOP leaves flags. Subsequent store/index/compare
operations determine the loop decision. Writable RAM and exclusive execution
are required: operand and opcode stores are not atomic. An interrupt executing
a partly patched site could observe an invalid instruction/pointer. Branching
once to separate workers or once per row is an alternative; compare complete
code size, setup costs and clipping behavior before changing it.

## C03: specialized shifts with masked carry history

**Evidence:** `$1A84–$1AEA`, `DSK=$009284–$0092EA`;
join `$19D9–$19E4`, `DSK=$0091D9–$0091E4`.
**Level/status:** CPU mechanism within a machine-specific encoding; analyzed
local algebra; [APPLE2-0003](../../findings/APPLE2-0003-runtime-sprite-shift-and-reflection.md).

The routine dispatches phase `$10=0..6` using DEX/BEQ. Phase zero returns the
input A and zero fragment. Small phases use ASL/ROL; phases five and six use
four or three RORs followed by two ROLs and masks. DEX/BEQ do not reset C, so
incoming carry can enter those ROR paths. The masks discard its contribution
in the returned seven-pixel fields; they are not arbitrary cyclic eight-bit shifts.

For every input byte b and either input C, the checked contract is:

~~~text
(returned_A & $7F) = ((b & $7F) << phase) & $7F
$1A = ((b & $7F) << phase) >> 7
~~~

Returned bit 7 is not a uniform preserved metadata bit. The renderer subsequently
ORs `$80`. Low current pixels and the previous byte's overflow occupy disjoint
positions, so EOR at `$19DE` equals OR **under that invariant**. It is not a
general recommendation to replace OR with EOR. The outgoing flags/X are scratch.

[Static verification](verification.json) covers all 3,584 byte/phase/carry cases
and all 114,688 two-token/phase joins. The Python translation is pinned to the
shifter's source bytes and reviewed paths. No instruction-stream execution,
whole-renderer proof or speed comparison is implied. Invalid phases fall into
the last path rather than being range-checked.

## C04: self-modified absolute operands during relocation and clearing

**Evidence:** initial `$2100–$214F`, `DSK=$009900–$00994F`;
relocated `$0153–$0169`, `DSK=$009953–$009969`. **Level/status:** CPU;
analyzed local behavior; no new fiche.

X enumerates `$00..$FF`; after wrap, INC changes high operand bytes of absolute
indexed LDA/STA, advancing to the next page. Low bytes are zero. A page-aligned
LDA abs,X does not incur an indexed-read crossing for X in `$00..$FF`; STA abs,X
still has its normal fixed store cost. Clear loops reload `$80` each iteration.
This is ascending copying/clearing, not the exact descending loop in
[CPU6502-0004](../../../docs/cpu/6502/descending-page-copy.md).

The low copy includes hardware stack page `$0100` and moves code to `$0153`.
Startup reaches it by JMP and it does not call subroutines before the final JMP,
but later stack depth, IRQ pushes and overlap have not been measured. Reusing
that page is a lifetime constraint, not free 256-byte storage.

## C05: carry reuse with a bounded row table

**Evidence:** `$7761–$777D`, `DSK=$004F61–$004F7D`;
row tables `$0800/$08C0`, `DSK=$00A000/$00A0C0`. **Level/status:** CPU
and table-range invariant; analyzed locally; no duplicate fiche.

The column copy forms destination-page/source-page high bytes from the same
page-relative high byte. After CLC and ADC `$07`, it saves that result, restores
the table byte with PLA, and ADCs `$80` without a new CLC. All 192 table highs
are at most `$1F`, and page selectors are `$20/$40`; the first ADC cannot carry.
PHA/PLA/STA do not change C. Thus the second ADC sees C=0 under those checked
selectors. Changing table ranges or banking/selector representation breaks the proof.

## C06: retained token cursors and movement sign

**Evidence:** `$6400–$648A`, `DSK=$005C00–$005C8A`;
control handlers through `$653F`, `DSK=$005C8B–$005D3F`.
**Level/status:** common interpreter pattern; local dispatch analyzed;
related [GEN-0001](../../findings/GEN-0001-resumable-animation-streams.md).

Horizontal step `$27` advances cursor `$25`; `$6360,X` supplies a movement
delta, with adjusted/negated lookup on reverse stepping. Facing `$2C` can
negate the delta again before adding it to `$22`. Tokens from `$6300,X`
set frame `$20` or dispatch `$FF/$80..$83`. Vertical step `$28` advances `$26`;
`$63BE,X` sets frame `$21` or dispatches `$FF/$86/$84`. Some controls restart
the updater. It retains progress between calls, but no universal one-token-per-frame
or bounded restart count is proven. Byte indices wrap; invalid data has no
established bounds recovery. ADC/SBC deltas require binary arithmetic.

## Optimization hypotheses and validation priorities

| Concrete target | Proposed experiment | Trade-off / proof needed |
| --- | --- | --- |
| Duplicate LDA `$0F` at `$196A/$196C` and `$1B5B/$1B5D` | Remove one load in a rebuilt worker | 2 code bytes / 3 table-derived cycles per setup; same flags if no asynchronous `$0F` writer; relocate branches/operands correctly |
| Repeated phase dispatch in `$1A84` for every byte | Dispatch once per sprite/row or use compact output tables | More code/table RAM, separate phase paths; exact clipping/bit-7 contracts must match |
| NOP pair in opaque mode | Separate opaque worker | Removes four cycles per visited patch site; adds code and maintenance, setup/edge paths still matter |
| ZP actor window | Compare retained records with indexed or indirect field access | Copy cost versus many direct accesses; include classification tails and both actors |
| Page clearing loops | Hoist invariant LDA `$80` where flag flow allows | Writable-code rebuild, branch flags and setup lifetime need rechecking |

These are unimplemented hypotheses, not recommendations with measured gains.
First trace decimal state, stack high-water use, ZP ownership and patch ordering;
then compare complete workloads rather than isolated instruction costs.

