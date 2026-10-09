---
id: "ANALYSIS-ORIC-SPACE1999-HARDWARE"
program: "Space: 1999"
cpu: ["6502"]
machines: ["oric-atmos"]
analysis_status: complete
source_revision: "upstream c81612082482d1f497638ada14ad4640c5e4f1ec; local disk SHA-256 9d85e1d75d9f1e548f4d1e3bc3750085e7c8c125bb6cd110fb604ba86ba3e851"
analysis_date: "2026-10-09"
---

# Space: 1999 hardware techniques

## 1–3. Scope and references

Targeted Atmos/Microdisc source analysis. The local README L60–L66 and publisher require Atmos; do not transfer ROM-entry assumptions to Oric-1. Hardware claims are checked against the [Atmos manual](https://library.defence-force.org/books/content/manual_atmos.pdf), graphics chapter and memory-map appendix, and Oricutron's [ULA](https://github.com/pete-gordon/oricutron/blob/master/ula.c) and [Microdisc model](https://github.com/pete-gordon/oricutron/blob/master/disk.c). Emulator source corroborates implementation expectations; it is not a real-hardware measurement or controller schematic.

## 4–5. Video and memory findings

### Parity-compressed screen addressing

In screen mode `pixel_address` calculates `$A000 + 40*y + floor(x/6)` and mask `$20 >> (x mod 6)`. It stores only even-row offsets (100 little-endian words) and even-X quotient/mask pairs (120 pairs), then reconstructs odd coordinates. [upstream `game source/NOISE/groutines.s:L97–L175`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/NOISE/groutines.s#L97-L175); [upstream `game source/NOISE/noise-tail.s:L13–L37`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/NOISE/noise-tail.s#L13-L37). The table footprint is 440 bytes, half the 880 bytes of an all-row/all-X implementation with the same word/pair layout. This is a size comparison, not a measured speedup.

The six-pixel rule is Oric-specific; the shift/flag/index operations are ordinary 6502. [ORIC-0003](../../findings/ORIC-0003-parity-compressed-pixel-tables.md) records bounds, arithmetic and model results. Negative X handling belongs to the scratch-relative path and is not covered by the 48000-coordinate screen model.

### Small dirty rectangles and layered occlusion

NOISE reserves a six-byte-stride 240-byte scratch image at `$0200` and a matching occlusion region at `$0400`. Their capacity supports a maximum nominal 6×40 byte rectangle. Movement expands a sprite rectangle to cover vacated and newly occupied pixels; WHITE redraws intersecting scene content rather than preserving an old background snapshot. [upstream `game source/NOISE/noise-start.s:L14–L25`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/NOISE/noise-start.s#L14-L25), [upstream `game source/NOISE/noise-start.s:L96–L114`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/NOISE/noise-start.s#L96-L114), [upstream `game source/NOISE/spritemov.s:L71–L208`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/NOISE/spritemov.s#L71-L208). See [GEN-0003](../../findings/GEN-0003-clipped-scene-recomposition.md).

Occlusion generation explicitly considers selected neighboring and upper blocks, layers and other sprites. It relies on LAYER_HEIGHT=8 and four layers; the source calls this correction a kludge. [upstream `game source/NOISE/occlusions.s:L78–L181`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/NOISE/occlusions.s#L78-L181). Treat the chosen geometry as a constraint, not a universal solution to isometric ordering.

The sprite path combines image masks, shift spill, screen bytes and a foreground mask; mirrored six-bit values use a 64-byte lookup. [upstream `game source/NOISE/groutines.s:L449–L587`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/NOISE/groutines.s#L449-L587); [upstream `game source/NOISE/noise-tail.s:L76–L79`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/NOISE/noise-tail.s#L76-L79). One source comment says “remove bit 7” beside `AND #$BF`: **$BF clears bit 6**, not bit 7. This is an example of why the instructions take precedence over comments.

### Embedded attributes are part of rendering

WHITE clears graphics with `$40`, hides the room using black ink, then reveals it through ink attributes, sometimes alternating ink by row. [upstream `game source/WHITE/white.s:L571–L651`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/WHITE/white.s#L571-L651), [upstream `game source/WHITE/white.s:L663–L755`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/WHITE/white.s#L663-L755). This coordinates a direct room redraw with visibility but does not establish vertical-blank synchronization or guarantee tear-free updates.

ULA interpretation depends on control bits as well as pixel bits; copying or ORing arbitrary bytes can create attributes. Keep attribute columns and the frame outside the normal sprite clip. Neither the small scratch buffer nor “double_buff” means a second full 8000-byte framebuffer.

## 5. Disk, IRQ, audio and input

### Overlay takeover and fixed sector layout

`_switch_ovl` toggles control bit 1 in the maintained `diskcntrl` shadow at `$0314`, masking interrupts during the write. `_init_disk` writes `$FFFE/$FFFF`. [upstream `game source/disk.s:L25–L46`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/disk.s#L25-L46). This requires writable overlay memory and the assumed Microdisc control mapping.

The game loads 54 sectors from sector 104: 38 pages for map reservation and 16 for sound/padding, covering `$C000–$F5FF`. Exact 9722-byte map matching independently confirms the data at the expected disk position. Filesystem startup and gameplay sector access are separate: the DSK begins with Sedoric metadata, even though the running game uses direct sectors.

DRQ polling uses `$0318` and data `$0313`; controller registers occupy `$0310–$0313`. Completion escapes polling via an IRQ as described in [CPU6502-0006](../../findings/CPU6502-0006-irq-frame-discard-and-rts.md). [upstream `game source/disk.s:L170–L245`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/disk.s#L170-L245). After eight failed read/write attempts, the driver returns with nonzero status. Selected callers do not establish robust recovery for missing disk, incomplete loads or failed backup writes; seek/restore loops also lack an overall timeout.

### IRQ cadence inherited from the system

The gameplay IRQ initializer redirects the vector without configuring the timer period. [upstream `game source/sp1999.s:L4695–L4759`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/sp1999.s#L4695-L4759). Source comments describe 100 Hz IRQ and 25 Hz key polling; the observed code only proves “keyboard on every fourth decrement,” with TimerCounter also maintained by the foreground. Exact cadence depends on prior timer setup and foreground timing; no 100 Hz measurement was made.

### AY write shadow and shared keyboard wiring

`SendAY` compares desired `RegisterBank` against `ReferenceBank` and submits only changed values through VIA port A and PCR strobes. [upstream `game source/sound.s:L297–L317`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/sound.s#L297-L317). This reduces bus writes when registers are unchanged, at the cost of comparison/shadow storage. Equality is not sufficient for all side-effectful PSG writes: review envelope-shape retrigger behavior and all paths that force/update the shadow before adopting this as a generic PSG rule.

The IRQ calls ProcMusic (which reaches SendAY) before ProcEffect, so effect state changes can be submitted on the following service. [upstream `game source/sp1999.s:L4731–L4734`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/sp1999.s#L4731-L4734). This is the source order, not a measured audible delay.

Keyboard scanning selects AY register `$0E`, writes column masks, chooses a VIA row while retaining upper port bits, then waits four NOPs and reads bit 3. [upstream `game source/sp1999.s:L4761–L4815`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/sp1999.s#L4761-L4815). The author says real Orics need the settling delay even where Euphoric does not. Four documented NOPs give eight CPU cycles of inserted delay; total electrical settling time and adequacy were not measured. Preserve strobe transitions and shared audio/input state before trying to remove this delay.

## 6–8. Verification and related work

Local CRCs and data matching are recorded in [verification.json](verification.json); no peripheral execution occurred. GEN-0002 confirms semantic geometry separate from screen pixels. ORIC-0001's background-page technique is a comparison, not this renderer's implementation. ORIC-0002's charset-bank animation does not apply to the HIRES sprite pipeline. All new fiches remain under research.

## 9–10. Next tests

Trace rectangle capacity and attribute preservation across six sub-byte X phases, both mirror states, room edges, all movement directions and stacked objects. Trace disk-completion IRQ origin and game handler reinstatement during failures. Check timer initialization and keyboard/audio operation on an Atmos plus Microdisc-compatible device. Exact ROM `$EB7E` reboot compatibility remains a dependency, not a portable API claim.
