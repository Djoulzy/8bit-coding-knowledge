---
id: "ANALYSIS-ORIC-SPACE1999-CPU"
program: "Space: 1999"
cpu: ["6502"]
machines: ["oric-atmos"]
analysis_status: complete
source_revision: "upstream c81612082482d1f497638ada14ad4640c5e4f1ec; local disk SHA-256 9d85e1d75d9f1e548f4d1e3bc3750085e7c8c125bb6cd110fb604ba86ba3e851"
analysis_date: "2026-10-09"
---

# Space: 1999 CPU techniques

## 1–3. Scope and compatibility

Static NMOS 6502 analysis of the pinned source in [overview](overview.md). All discussed instructions are documented NMOS instructions. No undocumented-opcode optimization was established. This does not certify every byte in the local disk as code or establish 65C02 timing equivalence.

## 4–5. Findings

### Executable operands specialize repeated work

The game keeps executable code in writable RAM. `_set_doublebuff` patches the sprite stride immediates from 40 to six; clipping limits and mirror flags are similarly installed as immediates before a draw. [upstream `game source/NOISE/clipping.s:L359–L377`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/NOISE/clipping.s#L359-L377); [upstream `game source/NOISE/groutines.s:L433–L458`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/NOISE/groutines.s#L433-L458); [upstream `game source/NOISE/groutines.s:L590–L607`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/NOISE/groutines.s#L590-L607).

This removes repeated parameter fetching inside the hot scan loops, but is not reentrant: two callers cannot safely draw with independently prepared values. Patches and affected code must remain writable and coherent. The IRQ uses separate `irq_*` scratch variables; that does not by itself prove it never reaches a patched foreground helper.

Optional hooks use three bytes with equal layout: NOP/NOP/NOP becomes JSR absolute. The installer writes the destination before opcode `$20`; removal writes `$EA` three times. [upstream `game source/WHITE/white.s:L411–L462`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/WHITE/white.s#L411-L462). This is related to [CPU6502-0001](../../findings/CPU6502-0001-two-byte-render-patches.md), with different instruction width and call semantics. No duplicate fiche is created.

The removal routine correctly starts its writes at Y=0. Hook updates are multiple stores, so a consumer must not execute a slot while it is partly installed or removed; this foreground room-hook design does not establish a general interrupt-safe patch protocol.

### Small-domain arithmetic avoids general multiplication

Active FASTMULT forms 6× and 12× by ASL and ADC. `ij2xy` projects legal tile coordinates as X = 108 + 12(i−j), Y = 32 + 6(i+j), with a sign-dependent X path. [upstream `game source/NOISE/auxiliar.s:L195–L271`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/NOISE/auxiliar.s#L195-L271). For a 10×10 grid, i,j in 0…9 give X in 0…216 and Y in 32…140; the formula is not safe for arbitrary byte inputs. Fine-coordinate offset and height adjustments occur elsewhere.

Record indexes use 4× via two shifts, 6× via 2×+4×, and grid indexes 10× via 2×+8×. [upstream `game source/NOISE/isofuncs.s:L26–L42`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/NOISE/isofuncs.s#L26-L42); [upstream `game source/WHITE/white.s:L185–L247`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/WHITE/white.s#L185-L247). This trades domain restrictions and carry discipline for compact code. The square-table `mul8` is excluded by FASTMULT, so it is an alternative in the archive rather than an active finding.

### The hardware stack is an explicit token work list

`decomp` pushes a zero sentinel and input byte. High-bit tokens index a 256-byte pair grammar; pushing second then first ensures output order. Low nonzero bytes go to `put_code`. [upstream `game source/sp1999.s:L4235–L4264`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/sp1999.s#L4235-L4264). See [GEN-0004](../../findings/GEN-0004-stack-driven-pair-grammar.md). This shares the page-`$01` stack with JSR and IRQ frames; it does not make recursive calls for grammar expansion.

### Disk IRQ completion returns out of a polling function

The caller JSRs `readwrite_data`; that routine enables interrupts and polls indefinitely. The completion handler removes three hardware IRQ bytes and RTSes using the still-pending JSR return. [upstream `game source/disk.s:L170–L245`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/disk.s#L170-L245). This is the existing [CPU6502-0006](../../findings/CPU6502-0006-irq-frame-discard-and-rts.md) mechanism, now visible in an enabled source path.

PLP later restores the caller's saved flags. The handler itself does not restore the IRQ flags or original PC. Validity depends on stack topology and completion interrupt origin; VIA IRQ handling follows a separate RTI path. Save/load must reinstall the gameplay vector. Presence in source and a matching disk signature are not proof that all device races are handled.

### Decimal and flag contracts

The gameplay IRQ executes CLD before arithmetic and returns with RTI, restoring interrupted status. Foreground ADC/SBC routines expect binary mode; this analysis did not establish a universal startup CLD invariant across every launch path. [upstream `game source/sp1999.s:L4718–L4759`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/sp1999.s#L4718-L4759).

In sprite drawing, `BVC sps_rotate` is commented as unconditional. [upstream `game source/NOISE/groutines.s:L460–L505`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/NOISE/groutines.s#L460-L505). BVC only branches when V=0, and intervening loads/stores do not establish V. Check all preceding arithmetic/helper paths before accepting that comment. Carry propagation in compact pixel tables and coordinate additions likewise requires its actual producers to be traced, not guessed.

## 6. Performance evidence

[MOS instruction summary](https://ftpmirror.your.org/pub/misc/bitsavers/components/mosTechnology/6502_Instruction_Set_Summary.pdf) supports the following theoretical observations:

- Three NOPs occupy three bytes and take six cycles; JSR absolute occupies three bytes and takes six cycles before executing its callee. A returning callee adds its own work and a six-cycle RTS.
- Indirect-indexed reads can gain a page-crossing cycle. Indexed stores have their own fixed timing; branch cost depends on outcome and page crossing.
- No routine-level cycle sum, emulator measurement or CPU budget is claimed. Table addressing alignment and IRQ work can change total cost.

The coordinate and grammar checks in [verification.json](verification.json) are mathematical/data checks, not instruction emulation.

## 7–8. Knowledge-base comparison

CPU6502-0001 confirms equal-width executable rewriting as a related pattern; CPU6502-0006 confirms the exact IRQ escape mechanism. [Carry-stream extraction](../../../docs/cpu/6502/carry-stream-field-extraction.md) and [descending page copy](../../../docs/cpu/6502/descending-page-copy.md) were consulted; neither needs a duplicate fiche for these narrower loops. No CPU guideline was edited.

## 9–10. Risks and proposed improvements

1. Audit library callback contracts: `_wh_bkgcol` saves `tmp` with PHA, but a callback return X=0 branches past its restoring PLA into RTS. [upstream `game source/WHITE/white.s:L325–L383`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/WHITE/white.s#L325-L383). The selected game's callback explicitly returns X=1 through its normal common epilogue, [upstream `game source/sp1999.s:L3199–L3251`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/sp1999.s#L3199-L3251), so this is a latent reusable-engine early-return defect, not an established gameplay failure.
2. `_white_clear_room_map` initializes X=100 and writes through X=0 inclusive: 101 writes per 100-byte array. Adjacent map starts are cleared redundantly, and the final write reaches `_ink_colour`. [upstream `game source/WHITE/white.s:L29–L50`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/WHITE/white.s#L29-L50); [upstream `game source/WHITE/white.s:L791–L804`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/WHITE/white.s#L791-L804). Use a bounds-aware reproduction to assess the effect; historical files remain unchanged.
3. TimerCounter is changed by IRQ DEC and a foreground read/add/store. An IRQ between foreground load and store can lose a decrement; a long foreground pause can also defeat its signed-byte tick scheme. [upstream `game source/sp1999.s:L1005–L1028`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/sp1999.s#L1005-L1028). Compare a protected update or monotonic tick accumulator, including IRQ latency cost.
4. Compare memory parameters with executable patches under realistic redraw sizes before assuming self-modification wins.
