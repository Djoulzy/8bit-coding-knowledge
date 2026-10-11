---
id: "ANALYSIS-APPLE2-KARATEKA-ARCH"
program: "Karateka"
cpu: ["6502"]
machines: ["apple-iie"]
analysis_status: complete
source_revision: "d02edc77fa0a02d3f679af22456ca1c762c305dc"
analysis_date: "2026-10-11"
---

# Architecture and memory phases

## Scope and evidence conventions

Identity, checksum, original-path attribution and environment uncertainties are
in [overview](overview.md). `DSK=$xxxxxx` denotes the zero-based byte offset in
that image. Addresses denote CPU memory in the named phase. There are no
original symbols or source line numbers. The [selected listing](extracted/selected-disassembly.txt)
records CPU address, first-byte disk origin, captured bytes and decoded operation.
An instruction crossing a remapped page boundary can have noncontiguous disk
origins; use [manifest](extracted/manifest.json) or the tool's provenance model
for each byte. Linear listing spans may include interleaved data and do not
by themselves establish reachability.

## Entry and loading

1. **Boot sector at `$0800`:** byte zero is `$01`; code begins at `$0801`
   (`DSK=$000001`). A sector translation table at `$084D` (`DSK=$00004D`)
   and disk-ROM entry derived from slot state support initial DOS-style loading.
   The load at `$0866` has immediate `$00`, so `$0868` falls through and
   `$086D` jumps to `$B715`. Firmware execution and physical disk encoding are
   assumptions, not emulated steps.
2. **Initial loader at `$B715`:** `DSK=$000115–$000149`. Read track `$01`,
   sector `$0F` into page `$A7`; decrease buffer page and sector, increment
   track after sector `$00`; stop when the page becomes `$07`. The result is
   160 sector reads, tracks `$01–$0A`, destination pages `$A7–$08`.
3. **Slot mapping:** for these core reads, image offset is
   `256 × (16 × track + sector)`; destination page is
   `$A8 − 16 × track + sector`. The first read uses `DSK=$001F00 → $A700`;
   the last uses `DSK=$00A000 → $0800`. Track-order reversal produces a
   coherent code/table map. This is an inference about the supplied image,
   independent of a missing DOS catalog.
4. **Relocation at `$2100`:** `DSK=$009900–$009969`. Copy 24 pages from
   `$2800` to `$A800`, clear page 2, select full HGR/page 2, copy eight pages
   from `$2000` to `$0000`, jump to `$0153`. The relocated tail at `$0153`
   (`DSK=$009953–$009969`) clears page 1 and jumps to `$B77C`.
5. **Resident title/game:** `$B77C` (`DSK=$008F7C`) uses graphics, text and
   input helpers. The non-input-aborted title path reaches `$B895 → $B400`.
   Input can instead transfer into the low disk/scene machinery.

The initial loader's `$B7B5` (`DSK=$0001B5`) masks IRQ while calling `$BD00`
and returns carry for success/failure; the `$B715` loop does not visibly test
that return carry. Successful reads are a reconstruction precondition.
Addresses `$B715` and `$B7B5` later contain different resident game code.

## Memory allocations

| Phase / range | Role | Evidence and limits |
| --- | --- | --- |
| Boot `$0800–$08FF` | Firmware-loaded sector | `DSK=$000000–$0000FF`; subsequently overwritten by core tables |
| Initial `$B600–$BFFF` | DOS-style code and read service | Image slots of track 0; ROM/load interpretation not executed |
| Initial `$0800–$A7FF` | 40 KiB core before relocation | Track/sector records in manifest |
| Initial `$2000–$27FF` | Low resident block stored in future page 1 | Copy at `$213A`; later moved to `$0000–$07FF` |
| Initial `$2800–$3FFF` | High resident block stored in future page 1 | Copy at `$2102`; later moved to `$A800–$BFFF` |
| Runtime `$0000–$00FF` | Renderer arguments, actor records, counters and global state | Numerous fixed ZP accesses; not a complete symbol table |
| Runtime `$0100–$01FF` | Hardware stack plus temporary relocated clear code | `$0153–$0169`; stack headroom/lifetime not measured |
| Runtime `$0200–$03FF` | Disk/scene transition and low helper code | `$0200` jump table, `$0300` slot-ROM copying, `$0393` ZP exchange |
| Runtime `$0400–$06FF` | Data accessed by the low text renderer | Inferred glyph/data region; later text/disk path can overwrite it |
| Runtime `$0700–$07FF` | Text and intro copy/page helpers, with embedded data | `$0700` and `$0780` interfaces; complete text encoding not audited |
| Runtime `$0800–$08BF` | 192 HGR row low bytes | `DSK=$00A000–$00A0BF`; all entries checked |
| Runtime `$08C0–$097F` | 192 HGR row high bytes, page-relative | `DSK=$00A0C0–$00A17F`; all entries checked |
| Runtime `$0980–$09FF` | 128 seven-bit reflection values with bit 7 set | `DSK=$00A180–$00A1FF`; accessed as `$0900,X` with `X ≥ $80` |
| Runtime `$0A00–$1FFF` | Graphics, health, audio, sequence/scene helpers and data | Mixed code/data; renderer `$1900–$1C79` deeply examined |
| Runtime `$2000–$3FFF`, `$4000–$5FFF` | HGR pages 1 and 2 | Cleared with `$80`, addressed via row tables and `$07` |
| Runtime `$6000–$62FF` | Parallel frame/layer lookup data | Actor drawing `$6811` reads pointer and offset arrays |
| Runtime around `$6300–$63FF` | Animation tokens and signed movement deltas | Reads at `$6300`, `$6360`, `$63BE`; exact stream extents not all classified |
| Runtime `$6400–$77FF` | Sequence update, actor drawing/decisions, record handling, page/input services | Selected call map and listing |
| Runtime `$7800–$A7FF` | Scene/controller helpers and packed assets | Partial map only; `$A300` is scene bookkeeping, not the actor blitter |
| Runtime `$A800–$BFFF` | Relocated controller, scenery, title, tables and alternate actor drawing | `$B400`, `$B77C`, `$BC00`; not all bytes code |

These are initial resident allocations. The `$0300` path and later disk-loaded
code may reuse `$0400–$07FF`, `$4000` and other areas; their full overlay lifetimes
are unknown. Do not reserve all ranges simultaneously in a new program based
on this map.

## Actor and frame control

`$60–$6F` holds the first actor and `$70–$7F` the second. Load helpers copy one
record into `$20–$2F`; shared routines access fields at fixed ZP addresses;
commit helpers copy the result back. Load tails also classify the other actor
and derive distance/scene state into `$32/$33`.

The ordinary update path at `$B584` calls `$7009 → $6B00 → $6400 → $7006`
for the second actor. `$B69A` loads the first via `$700F`, selects/updates its
sequence, and ends with `$700C`. The same work window is loaded again for
drawing at `$B654`, `$B675` and `$B683`. Record switching is cooperative;
there is no evidence that it is interrupt-driven context switching.

Animation retains separate cursors/steps in `$25/$27` and `$26/$28`; positive
tokens choose frame IDs in `$20/$21`, negative tokens select sequence controls.
`$22` is a coarse horizontal coordinate, `$2C` supplies facing sign, and
per-frame arrays add layer offsets and pixel phase. These meanings are demonstrated
in local consumers; the remaining fields have not all been named.

## Rendering and page history

`$B4E7` includes actor decisions, health/collision consumers, background repairs
and layered draws. `$678C/$6780` clear bounded spans using retained actor
coordinates, then scene helpers rebuild parts of the background. `$6783`
draws actor layers, using AND masks followed by OR images where selected.
`$7600` flips via `$7609` and processes foreground audio events.

`$07` identifies the draw page's high byte, `$20` or `$40`. A flip shows the
completed draw page and changes `$07` to the other page for subsequent work.
`$A316` shifts position/phase history through pairs of globals such as
`$E2 → $E3` followed by `$62 → $E2`, and `$AD → $AE` followed by `$50 → $AD`.
Clearing reads the older values. This supports page-aware repair across two
alternating buffers; a complete proof for every camera/scene transition is pending.

The intro helper `$0780` copies source rows `2..191` to destination rows `0..189`
across the two pages. `$7606/$774B` instead copies **from the current draw page
to the other page**, one column at a time, using 192 row lookups and a ROM delay
between columns. It performs no page switch internally. These are distinct
operations, not two names for a whole-frame memcpy.

## Input, audio, storage and interrupts

`$B7EA/$B7F5` poll buttons and keyboard; `$7603/$7697` handles control keys.
The decision module `$6B00` consults both actors, distance and scene variables.
Complete keyboard-to-action and paddle calibration contracts remain unresolved.

`$0C40` dispatches effects with `$C030` accesses and monitor delays.
`$0D00` parses a command stream and synthesizes transitions with paired counters;
`$0DC0` shifts packed bits and toggles the speaker when the next sign bit differs
from retained state. Gameplay audio service `$7628` calls these in the foreground.
There is no measured sound rate or established music IRQ in these paths.

`$020C` calls `$0300`, checks bytes near `$BFFF` and transfers through `$BFFA`.
`$0300` copies slot-6 ROM, patches the copy and executes it; a raw-read helper
at `$0348` contains nonstandard prologue checks and a transfer to loaded code
at `$4000`. `$0393` exchanges all 256 ZP bytes with `$4F00–$4FFF`. `$03DC`
also accesses `$C081/$C082`; its banking purpose/reachability is not fully
verified. These observations do not authenticate the original protection or
prove a minimum language-card configuration.

## References and next investigations

[Routine inventory](routines.md), [CPU analysis](cpu-techniques.md),
[hardware analysis](hardware-techniques.md), [manifest](extracted/manifest.json)
and [verification](verification.json). Trace startup and one normal update
before expanding into later disk overlays or treating this as a complete memory map.

