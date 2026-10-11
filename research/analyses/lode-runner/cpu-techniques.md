---
id: "ANALYSIS-APPLE2-LODE-RUNNER-CPU-TECHNIQUES"
program: "Lode Runner (local cracked disk)"
cpu: ["6502"]
machines: ["apple-ii-family", "apple-iie-variant-unknown"]
analysis_status: draft
source_revision: "d02edc77fa0a02d3f679af22456ca1c762c305dc"
analysis_date: "2026-10-10"
---

# Lode Runner: MOS 6502 techniques

## Scope and evidence

The [snapshot](overview.md) is analyzed using documented NMOS instructions.
Original assembler syntax is unknown. Runtime addresses map to disk bytes.
Data decoded as instructions does not establish illegal/65C02 opcode use.

## C01 — Carry selects packed nibbles (analyzed, CPU/common)

[level.asm.txt:L35–L53](extracted/level.asm.txt), CPU $627E–$629E, first instruction at DSK $013B85. LSR of a cell counter puts parity in C; LDY/LDA preserve C,
so BCS selects AND $0F or four LSRs. Byte index advances only after the high
nibble. Counter wrap at 256 is harmless for parity; 448 cells consume 224 bytes.
This differs from CPU6502-0003's high-first destructive two-bit carry stream.

The inverse uses four ASLs and ORA: [level.asm.txt:L73–L108](extracted/level.asm.txt), CPU $62C7–$630D, first instruction at DSK $013BCE. Its BPL requires the
first cell to have bit 7 clear. Packed storage saves 224 bytes per level;
two byte-per-cell runtime grids spend 896 bytes for simpler queries.

## C02 — Split tables and absolute-load operand patches (analyzed, CPU)

[renderer.asm.txt:L418–L480](extracted/renderer.asm.txt), CPU $8438–$84C0, first instruction at DSK $015E3F. Pixel phase $00–$06 selects high byte $A2–$A8 through
$84C1 and patches four indexed table loads. Two row tokens then index split
low/high pointer tables. Four absolute LDA operands are patched for dictionary
pairs and their adjacent bytes. The decoder merges two pairs into three scratch
bytes, advances X by 3 and the token pointer by $68 twice, for eleven rows.

Low-byte +1 does not carry into the high byte. All 896 checked pairs begin at
even addresses and avoid offset $FF, satisfying this data-layout contract.
It is not a general 16-bit pointer update.

[APPLE2-0002](../../findings/APPLE2-0002-seven-phase-sprite-tables.md) covers the
data mechanism. CPU6502-0001 patches an operation; CPU6502-0005 uses ZP code
operands as IRQ state. These related records are not duplicates.

Absolute LDA is 3 bytes/4 cycles; LDA (zp),Y is 2 bytes/5 cycles plus read page
crossing. Include setup/patch costs and register contracts. RAM code and exclusive
scratch and D = 0 are required; IRQ/NMI re-entry can observe partial operands.
These are local [MOS table](https://ftpmirror.your.org/pub/misc/bitsavers/components/mosTechnology/6502_Instruction_Set_Summary.pdf) costs, not measured sprite timings.

## C03 — Inline streams rewrite the return address (analyzed, CPU6502-0007)

[input-audio.asm.txt:L225–L242](extracted/input-audio.asm.txt), CPU $86E0–$86FF, first instruction at DSK $016FE7; [input-audio.asm.txt:L353–L378](extracted/input-audio.asm.txt), CPU $87E1–$8810, first instruction at DSK $0161E8.
Both pop a JSR return address into $10/$11, advance into adjacent parameter
data, then push the terminator address high first/low second. RTS resumes
after that terminator. One prints text; the other collects audio pairs.

JSR stacks its last-byte address. The initial branch skips it; treating that
address as the first parameter is wrong. Helpers must not reuse $10/$11.
Nested consumers need explicit pointer preservation. See the
[fiche](../../findings/CPU6502-0007-inline-stream-return-address.md).

## C04 — Synthetic RTS command dispatch (analyzed candidate, CPU)

[input-audio.asm.txt:L12–L28](extracted/input-audio.asm.txt), CPU $6A2B–$6A48, first instruction at DSK $014332 scans key values, doubles an index, pushes table high/low,
and executes RTS. Table $6B67–$6B80 holds target−1: $6A55 selects $6A56.
The editor repeats it: [editor.asm.txt:L34–L51](extracted/editor.asm.txt), CPU $7C29–$7C4C, first instruction at DSK $015530, first pair $7C5F → $7C60.

It avoids a private indirect-jump pointer but uses two stack bytes.
After index computation, two absolute indexed loads, two PHAs and RTS cost
20 cycles plus read crossings; search/index work and handler return are excluded.
Correct target−1 encoding and push order are required. Candidate retained here.

## C05 — Quota bits and persistent actor cursor (analyzed, common/CPU)

[startup.asm.txt:L90–L103](extracted/startup.asm.txt), CPU $60C5–$60E2, first instruction at DSK $0139CC; [scheduler.asm.txt:L1–L18](extracted/scheduler.asm.txt), CPU $6C82–$6CA6, first instruction at DSK $014589; [scheduler.asm.txt:L19–L25](extracted/scheduler.asm.txt), CPU $6CDB–$6CE9, first instruction at DSK $0145E2.
A lookup selects three quota bytes; a phase counter cycles through them.
LSR yields C; a set bit schedules the next guard. $19 wraps through 1..$8D.
These are update quotas, not bits selecting particular guard identities.
$00/$01/$03/$07 request zero through three consecutive updates.
Death may abort a quota. See [GEN-0005](../../findings/GEN-0005-bit-quota-round-robin.md).
Difficulty-index bounds and full AI route selection remain open.

## C06 — BCD score and comparison-established carry (analyzed, CPU)

[renderer.asm.txt:L91–L104](extracted/renderer.asm.txt), CPU $7A92–$7AA9, first instruction at DSK $015399 adds packed-BCD A/Y into four score bytes with SED/ADC,
propagates carry and ends with CLD. This supports direct digit display.
IRQ code must tolerate D = 1; prior caller D is not restored. NMOS decimal
ADC N/Z cannot be treated as ordinary binary-result flags.

[renderer.asm.txt:L141–L155](extracted/renderer.asm.txt), CPU $7AF8–$7B14, first instruction at DSK $0153FF converts an 8-bit binary value with repeated subtraction.
CMP establishes C = 1 on the SBC path, avoiding a separate SEC. D = 0 is
required. Score overflow and whole-session arithmetic were not traced.

## C07 — Full pages and overlap direction (analyzed, existing principles)

[renderer.asm.txt:L59–L75](extracted/renderer.asm.txt), CPU $7A51–$7A6F, first instruction at DSK $015358 clears a complete HGR allocation through Y wrap/high-byte
counting. [level.asm.txt:L275–L293](extracted/level.asm.txt), CPU $6469–$648A, first instruction at DSK $013D70 copies page 2 to page 1 for a preview path.
Both traverse complete pages, with contracts differing from CPU6502-0004.

The cracked loader moves overlapping data upward by copying backward:
[loader.asm.txt:L67–L91](extracted/loader.asm.txt), CPU $5F5D–$5F8D, first instruction at DSK $013864. Its bytewise pointers/comparisons are expensive and include
questionable endpoints; captured code is not presumed optimal or original.

## Performance and proposed optimizations

| Hypothesis | Concrete trade-off | Required verification |
| --- | --- | --- |
| Direct phase outputs instead of pointer tables + dictionary | 1,792 pointer bytes + 1,024 dictionary bytes = 2,816; direct 7 × 128 × 2 = 1,792, saving 1,024 data bytes in checked domain; decoder changes too | Exact bit-7 output, used tokens/IDs, full cycles/code size |
| Page loops plus explicit edges for the cracked loader | Fewer pointer/limit operations; overlap/edge handling remains necessary | Intended endpoints, unknown extra bytes and I/O writes first |
| Explicit pointers instead of code operands | Reentrancy/relocation improve; indirect read costs and Y contract increase | Complete setup/inner loop and interruption requirements |
| Bounded audio queue replacing LIFO events | Extra head/tail/bounds state; changes order/timing | Intended reversed playback and maximum depth |

All are proposed experiments. No measured speedups, full routine timing or
guideline promotion is claimed.
