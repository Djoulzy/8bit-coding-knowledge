---
id: "ANALYSIS-APPLE2-LODE-RUNNER-ARCHITECTURE"
program: "Lode Runner (local cracked disk)"
cpu: ["6502"]
machines: ["apple-ii-family", "apple-iie-variant-unknown"]
analysis_status: draft
source_revision: "d02edc77fa0a02d3f679af22456ca1c762c305dc"
analysis_date: "2026-10-10"
---

# Lode Runner architecture and memory ownership

## Objective, provenance and evidence conventions

Same snapshot/environment as the [overview](overview.md). Runtime listings under
research/analyses/lode-runner/extracted/ map CPU addresses to original image bytes.
Addresses and DSK offsets replace unavailable source lines. Linear decoding may
include inline data and is not a reachability proof.

## Entry and relocation phases

BASIC startup and binary entry: [hello.basic.txt](extracted/hello.basic.txt) and
[loader.asm.txt:L1–L1](extracted/loader.asm.txt), CPU $07FD–$07FF, first instruction at DSK $010104. The front end copies a 22-byte cracker credit to text RAM,
polls $C000, and jumps to $5F00: [loader.asm.txt:L2–L17](extracted/loader.asm.txt), CPU $5A00–$5A22, first instruction at DSK $013307.
The local cracker is not the original game's routine author.

Under binary arithmetic (D = 0) and uninterrupted pointer ownership, the
loader performs these copies in order, with Y = $00:

| Source, inclusive | Destination, inclusive | Direction | Qualification |
| --- | --- | --- | --- |
| $8F04–$9701 | $0004–$0801 | Ascending | Last two source bytes are outside the DOS payload |
| $3A00–$5F01 | $9B00–$C001 | Ascending | $C000/$C001 are I/O accesses, not RAM |
| $0900–$3A00 | $0F00–$4000 | Descending | Overlapping upward move; backward order protects unread bytes |

[loader.asm.txt:L18–L101](extracted/loader.asm.txt), CPU $5F00–$5FA1, first instruction at DSK $013807. Endpoints follow comparisons **after** pointer updates.
The loader does not establish D = 0 itself. Unknown bytes stay unknown in
the model. Captured zero page and stack bytes
are overwritten; interrupt coexistence and return to DOS are not demonstrated.

## Main loop and state machine

$6000 probes analog input, reads metadata, draws the title and enables HGR.
Its patched absolute LDA at $6030 reads a stream: negative bytes draw pixels,
positive bytes select a column, zero ends a scanline. It walks 192 scanlines:
[startup.asm.txt:L1–L37](extracted/startup.asm.txt), CPU $6000–$6055, first instruction at DSK $013907. The operand starts at $0EFF and increments before fetching,
so the relocated stream begins at $0F00. This is not the level decoder.

Session initialization clears state/score and sets five lives:
[startup.asm.txt:L38–L71](extracted/startup.asm.txt), CPU $6056–$609E, first instruction at DSK $01395D. After level initialization, the foreground cycle calls
player, audio, holes, audio and guards: [startup.asm.txt:L87–L127](extracted/startup.asm.txt), CPU $60BF–$6119, first instruction at DSK $0139C6.
Death/completion routes to level restart, life decrement, scores or demo:
[startup.asm.txt:L128–L217](extracted/startup.asm.txt), CPU $611A–$6213, first instruction at DSK $013A21. $A7 selects modes; the whole transition matrix is untraced.

~~~mermaid
flowchart TD
    A[HELLO / DOS BRUN] --> B[Cracked loader / RAM copies]
    B --> C[Title and metadata]
    C --> D[Level decode]
    D --> E[Player update]
    E --> F[Sound and delay]
    F --> G[Hole timers]
    G --> H[Sound and delay]
    H --> I[Guard quota / next actor]
    I --> E
    E --> J[Death or completion]
    J --> D
    C --> K[Board editor]
    K --> D
~~~

This is a static subsystem map, not an executed trace.

## Memory allocations

| Address / range | Role | Evidence |
| --- | --- | --- |
| $0000–$0005 | Player coarse x/y, subcell offsets, frame/facing | movement and level listings |
| $0006/$0007, $0008/$0009 | Occupancy/terrain row pointers | $6269–$6278; $884B–$885C |
| $000C/$000D, $000E/$000F | Foreground/background HGR pointers, reused in other phases | $7A31/$7A3E; level readers |
| $0010/$0011 | Shared inline text/audio pointer | $86E0/$87E1 |
| $0012–$0018 | Selected guard working record | $75CE–$75F3 |
| $0054 | Audio event depth | $87D5/$87E1/$8811 |
| $0060–$0062, $0063/$0064 | Three quota phases, shifted quota, phase index | $60CB–$60E2; $6C82 |
| $008E–$0091 | Four packed-BCD score bytes | $7A92 |
| $008D/$0093/$0096/$0098/$0099 | Guards, gold, level index, lives, sound enable | setup/callers; complete contracts still open |
| $00DF–$00FF | 33-byte sprite workspace | $8438; 11 × 3-byte rows |
| $0800–$09BF | 448-cell live occupancy grid | row tables and level writes |
| $0A00–$0BBF | 448-cell terrain/item grid | high row byte +$02 |
| $0C00/$0C30 | Hidden-ladder coordinate lists; $0C00 also completion scratch | $63D6–$63E5; $8631 |
| $0C60–$0C9D | Guard fields in parallel arrays, indices 1–5 | $63FC–$641B; $75CE |
| $0CA0/$0CC0/$0CE0 | Hole column/row/countdown arrays | $6C39; $75F4 |
| $0D00–$0DFF | Sector buffer; first 224 bytes encode cells | $630E and decoder |
| $0E00/$0E80 | Parallel audio arrays, one-based indices | $87D5/$87E1; bounds open |
| $0F00 onward | Relocated title/assets; no single complete extent asserted | loader and $6000 |
| $1A85/$1B45 | 192 low/high HGR row entries | $7A31; tables.hex.txt |
| $1C05 onward | Grid/coordinate tables | tables.hex.txt |
| $1F00–$1FFF | Metadata/high-score buffer, signature/flag at end | $6359–$63A4 |
| $2000–$3FFF | Display HGR page in mapped gameplay | $6047; paired renderer |
| $4000–$5FFF | Terrain baseline; also some UI work | $63B3; $8336/$83A7 |
| $6000–$8D52 | Game/editor/render code with interleaved data | selected listings, not an all-code extent |
| $9B00–$BFFF | Relocated resources and DOS/RWTS portions | loader; $B7B5 |
| $A200–$A8FF | Seven split pointer-table pages | $8438; verification |
| $A900–$ACFF | 512 shared two-byte pixel pairs | verification |
| $AD00 onward | Sprite row-token slices, stride $68 | $8438; used-ID census still needed |

## Level representation and ownership

Zero-based level index $96 selects track = $03 + (index >> 4),
sector = index & $0F, buffer $0D00. Demo mode copies a resident page selected
by $9E + $A6: [level.asm.txt:L109–L146](extracted/level.asm.txt), CPU $630E–$6358, first instruction at DSK $013C15. The disk path's $0023 call remains unresolved.

The decoder takes low nibble then high nibble, advancing the byte index after
the high half. It fills 16 × 28 cells in both grids and maps $0A–$0F to blank:
[level.asm.txt:L35–L61](extracted/level.asm.txt), CPU $627E–$62AE, first instruction at DSK $013B85. That is 224 packed bytes; the remaining 32 sector bytes are
outside this decoder.

Preprocessing creates up to five guards and one retained player, counts gold,
records up to 45 hidden-ladder coordinates and removes actors from terrain.
It renders page 2 then removes actors in play mode: [level.asm.txt:L187–L317](extracted/level.asm.txt), CPU $63B3–$64BC, first instruction at DSK $013CBA.
Additional players/excess guards are removed; this is observed behavior,
not a recommended content-validation policy.

Local comparisons plus the publisher manual, printed pp. 5–6, identify:
$00 blank, $01 diggable brick, $02 solid brick, $03 ladder, $04 bar,
$05 trap door, $06 hidden ladder, $07 gold, $08 guard, $09 player.
$05 initially draws as brick. Every later transformation has not been traced.

## Graphics ownership

$7A3E pairs page addresses through high-byte XOR $60. $8336 restores old pixels
from page 2; $83A7 compares pixels against that baseline before OR drawing.
This demonstrates persistent scene-with-actors and terrain representations,
not gameplay frame flipping. Terrain changes must synchronize the baseline.

## Dependencies, interrupts and unresolved paths

$6359 → $63A5 → JMP ($0036), initially $8E50 → $B7B5 → $BD00.
The DOS wrapper saves P, disables IRQ, restores P and returns carry:
[disk.asm.txt:L46–L55](extracted/disk.asm.txt), CPU $B7B5–$B7C1, first instruction at DSK $0120BC.

$630E instead calls $0023, initially JMP $1700: [disk.asm.txt:L1–L1](extracted/disk.asm.txt), CPU $0023–$0025, first instruction at DSK $01692A.
The destination is graphics-like data after modeled copies. No intervening
patch/overlay was established. Disk reads, formatting and writes remain provisional.

No custom IRQ/NMI game handler was established. Foreground waits are demonstrated;
this does not prove that the entire disk never uses interrupts. ROM $FC58 is
used by the cracked front end. The $0600 disk reader's live use is unknown.
