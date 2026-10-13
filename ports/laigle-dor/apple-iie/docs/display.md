# Mixed HGR, native sprites and alternating frame pages

This implementation follows the requested Apple display adaptation: ordinary
monochrome HGR with four text lines below, two displayed/drawn frame pages, and
no emulation of Oric ink/paper attribute effects.

The monochrome profile remains the default. An optional
[native HGR color experiment](color-experiment.md) uses the same page/viewport
contract, but converts artwork into two-dot cells and lets sprite writes select
HGR bit 7. The monochrome bit-7/mask statements below describe `VIDEO=mono`.

The [DHGR variant](dhgr.md) has its own banked renderer, fine-dot masks and
16-color material patterns (see [palette adaptation](dhgr-palette.md)). It uses
two main+aux frame pairs, a main+aux baseline and four
80-column text rows. Its mapping and memory contract are separate from the
main-only HGR contract below.

## Video and RAM contract

With 80STORE, RAMRD, RAMWRT, ALTZP and 80COL off, the program uses main RAM.
`$C057` selects HGR, `$C053` enables mixed mode and `$C050` enables graphics.
The visible layout is **280×160 graphics pixels plus four 40-column text rows**.
See Apple's [IIe Reference Manual](https://www.applelogic.org/files/AIIEREF.pdf),
Chapter 2, display pages/mixed graphics.

| Selected page | HGR frame allocation | Corresponding bottom text row starts |
| --- | --- | --- |
| `$C054`: page 1 | `$2000–$3FFF` | `$0650`, `$06D0`, `$0750`, `$07D0` |
| `$C055`: page 2 | `$4000–$5FFF` | `$0A50`, `$0AD0`, `$0B50`, `$0BD0` |

PAGE2 selects both displays under this mapping; a fixed page-1 HUD would
disappear or show stale text every other frame. The state moved to `$0C00`
and events to `$0D00` to avoid the second text page. The custom `$0800` boot
sector is reclaimed only after it jumps into the complete application.

## Frame construction

Startup expands terrain at `$A000–$BFFF`, initializes both frame pages and
clears both text pages while full text is selected. It prepares the first
hidden frame before enabling mixed graphics. All later iterations:

1. Select the page opposite `display_page_hi`.
2. Restore **that page's own** previous actor rectangle from the immutable
   `$A000` baseline, using non-linear scanline addresses.
3. Reset its dirty bounds; draw the current three actor layers using pixel/mask
   planes and accumulate their clipped byte-x/pixel-y union.
4. Write the four HUD lines into the matching hidden text page.
5. Wait for a fresh vertical blank and switch PAGE2. Leave the visible page
   unchanged until the next iteration draws into it as the hidden page.

Per-page history matters: the hidden page contains an actor from two presentations
earlier. Restoring only the most recently displayed position would leave trails.
R restarts game state while retaining video histories until their pages are
repaired; it does not discard the rectangles that still own old pixels.

Full 8 KiB page copies occur during initialization only. A normal frame repairs
the actor's old bounded rectangle rather than rewriting the entire terrain.
The third baseline costs another 8 KiB, so the application/linker is capped at
`$A000` and no auxiliary RAM is required. Room changes must initialize both
pages and invalidate/rebuild their histories; dynamic terrain, multiple actors
and overlapping dirty regions need a broader compositor in W07.

## VBL presentation

On the **Apple IIe**, bit 7 of `$C019` is RDVBLBAR: high during active display,
low during vertical blank. The code waits until active display, then waits for
the next low transition, and performs the page switch before returning. This
avoids accepting an already-expiring blank period.

Polarity is supported by Sather's primary [Understanding the Apple IIe](https://www.dmcmillan.co.uk/blog/apple-iie-without-a-keyboard/Understanding_the_Apple_IIe.pdf),
Chapter 8 / the VBL' polling example, and cross-checked against the authors'
[AppleWin NTSC_GetVblBar implementation](https://github.com/AppleWin/AppleWin/blob/master/source/NTSC.cpp).
This is IIe behavior; do not transfer the polarity to the IIgs.

The harness models 262×65 CPU-cycle frame phases and 192 active lines, including
text. It verifies the waiting/switch sequence; it is not a full IOU/scanner,
PAL configuration, bus-phase or real display timing measurement. The target
assembly polls the signal and does not hard-code those NTSC constants. No fixed
FPS, original Oric pace or physical smoothness measurement is claimed.

## Viewport and attribute removal

Room 12's B2 line 690 clears source rows 0–34. Crop only that known empty band,
then map source 35–199 to target 0–159 with
`floor((source_y-35)*160/165)`. Coincident destination rows retain the last
source row. Logical collision/movement coordinates remain unchanged. This
keeps the floor and feet and limits vertical compression of the actual artwork;
other rooms, intros and future jumps need their own clipping review.

Bitmap shape uses Oric bits `$20` through `$01`, including data such as `$22`.
Ink/paper values are discarded. Their cells have **zero opacity** rather than
six opaque black pixels. Each graphical row gets a native silhouette mask:
pixels between its first and last foreground pixels are opaque where the
source cell contains graphic data; outside pixels and all attribute cells are
transparent. Interior black details occlude terrain, while margins preserve it.

Pixels and masks are packed as interleaved seven-bit rows. The renderer shifts
both through the same seven-phase tables, composes `(old & ~mask) | (pixels &
mask)`, clips before touching a neighboring row, and keeps HGR bit 7 zero.
Changing only source ink values must not change either target shape or mask;
that invariant is tested on a private copy of the historical payload.

## Text and verification scope

The native HUD writes normal Apple text codes into rows 20–23 of the hidden
page. It includes initialized forces/points/gold, empty hand, room/coordinates,
current actor status and controls. Coordinates/status update; full-game resource
depletion and inventory remain outside this milestone.

Actual Apple hardware uses its character ROM. The functional preview reads the
same text RAM but uses a small project-owned development font to show it in
PNG/browser images; glyph fidelity is not certified. The host view follows the
selected graphics/text page rather than always reading `$2000`.

Executed tests compare both page histories with a full redraw pixel oracle,
check native text addressing, enforce no visible-frame/HUD writes during
construction, test both pages' sprite phases/edges, and check VBL presentation.
This remains project validation under a stated functional model, not a promoted
knowledge-base renderer guideline or a hardware benchmark.
