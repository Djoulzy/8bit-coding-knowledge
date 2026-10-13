---
record_type: port-display-experiment
program: "L'Aigle d'Or"
machines: ["apple-iie"]
cpu: ["6502"]
status: analyzed
review_date: "2026-10-13"
---

# Native HGR color experiment

This optional W06 variant encodes color in the **native Apple HGR bytes**, in
both the bootable application and its terrain/sprite resources. Its purpose is
to assess an Apple color adaptation of room 12. The new palette is a porting
choice, not a reconstruction of Oric ink colors. Historical inputs and game
rules are unchanged. The monochrome binary remains the default and has the
same SHA-256 as the preceding mixed-mode milestone.

The source geometry and animation records come from the
[original analysis](../../../../research/analyses/laigle-dor/architecture.md)
and [porting contract](../../../../research/analyses/laigle-dor/portage.md).
The missing Oric ROM variation table remains the explicitly provisional zero
fixture unless `--oric-rom` is supplied.

## Build, test and launch

From `ports/laigle-dor/apple-iie/`, after the existing `make bootstrap`:

```sh
make test VIDEO=color
python3 tools/run.py --video color
python3 tools/run.py --video color --serve --port 8766
```

Open `http://127.0.0.1:8766`; Ctrl-C stops the server. The native binary is
executed by the existing functional CPU harness. The browser receives PNGs
decoded from the displayed HGR/text RAM. Arrows/J/K/U/N, space, A and R retain
their existing actions. Audio events remain silent.

The optional commands accept `--video mono|color`. Make accepts `VIDEO=mono|color`;
the default is `mono`. For example, `make run VIDEO=color` uses port 8765;
the explicit 8766 command allows an existing monochrome server to keep running.

| Output | Monochrome | Color |
| --- | --- | --- |
| Native application | `build/game.bin` | `build/color/game.bin` |
| DOS-order disk | `build/laigle-dor.do` | `build/color/laigle-dor.do` |
| Nibble disk | `build/laigle-dor.nib` | `build/color/laigle-dor.nib` |
| Exports, manifests, CPU/test reports | `build/` | `build/color/` |
| Executed screenshots | `build/room12-boot.png`, `room12-after.png` | `build/color/room12-boot.png`, `room12-after.png` |

To compare actual game states/events from both native programs:

```sh
make build
python3 tools/compare_video.py
```

The color build must already exist. Comparison boots both programs from their
Disk II images, supplies the same 26-frame input sequence and writes
`build/color/comparison.json`. It compares game state and event logs; it does
not equate the two pictures or claim identical physical frame rates.

For a complete Apple IIe emulator, mount the color `.do` as DOS-order or its
`.nib` in slot 6, drive 1, with standard CPU speed and **ordinary HGR NTSC
artifact/composite color** enabled. Use the existing custom boot procedure in
[toolchain.md](toolchain.md). This experiment requires main RAM only, and no
RGB expansion card or double-HGR. A monochrome monitor will display the native
alternating dot patterns. PAL/video-card-specific output is not verified.

With a local source ROM, preserve the selected build when checking:

```sh
python3 tools/build.py --video color --oric-rom /path/to/reference-oric.rom
python3 tools/check.py --video color
```

## Color representation and palette

Ordinary HGR retains seven dot bits per byte. Isolated even-position dots use
violet with bit 7 clear or blue with bit 7 set; isolated odd-position dots use
green or orange. Adjacent set dots tend to produce white. Seven dots per byte
means the parity alternates from one byte to the next.
This interpretation follows Apple's
[IIe Reference Manual](https://www.applelogic.org/files/AIIEREF.pdf), Chapter 2,
and the authors' standard-HGR decoder in
[Apple2js canvas.ts, pinned revision](https://github.com/whscullin/apple2js/blob/ee0aed25f73c69d0245e86a2a5fccb3324c3056c/js/canvas.ts#L773).

The experiment converts foreground shape to even-aligned **two-dot cells**.
One occupied source dot is sufficient to mark a cell; the desired color selects
which dot is lit. This gives 140 color cells across the 280-dot HGR display,
with the existing 160 graphics rows and four native 40-column text rows below.
Cell expansion can merge fine details and widen a silhouette by one dot.

| Color | Bits at even/odd screen positions | Bit 7 | Repeated pair of HGR bytes |
| --- | --- | --- | --- |
| Black | `0,0` | Clear in a fresh page | `$00,$00` |
| Violet | `1,0` | Clear | `$55,$2A` |
| Green | `0,1` | Clear | `$2A,$55` |
| White | `1,1` | Inherited | `$7F,$7F` when clear |
| Orange | `0,1` | Set | `$AA,$D5` |
| Blue | `1,0` | Set | `$D5,$AA` |

Black/white cell writes preserve an existing byte's phase; the last chromatic
cell write selects it. Because bit 7 affects **all seven dots**, different
color families sharing a byte can change each other's appearance. Neighboring
set dots can also create white fringes. These are Apple HGR constraints, not
retained Oric serial attributes. This version does not solve all color boundaries.

The explicit palette in [hgr_color.py](../tools/hgr_color.py) assigns blue to
atlas 3/4 columns, green to atlas 5/21 features, violet to atlas 8, orange to
atlas 7/14/15, and white to the floor/perspective lines. Actor IDs 46–61 use
blue; its other retained layers use orange. These are provisional artistic
choices and can be reviewed independently of the original stream records.

## Sprite composition and page repair

The historical sprite decoder still ignores ink/paper values and gives their
cells zero opacity. Color conversion expands each pair's pixel/mask occupancy
while retaining transparency. Source cells are six dots wide and native actor
anchors are `20 + (source_x + 1) * 6`, so every anchor is even. Moving by the
existing six-dot coordinate units preserves global color parity even though
the seven-bit byte shift changes. Arbitrary odd-dot positioning would need a
different conversion/renderer contract.

The seven-phase pixel/mask shifter remains in use. The color assembly path:

1. Loads the selected layer's phase bit.
2. Shifts foreground dots and opacity into destination bytes.
3. Skips an entirely transparent destination byte, preserving its phase.
4. Composes its low seven bits with the native silhouette mask.
5. Sets the byte's phase when the mask actually touches it.

Sprites currently use the blue/orange family (bit 7 set). A partly covered byte
can temporarily recolor an uncovered green/violet terrain dot. Each hidden
page's dirty rectangle is repaired from the immutable baseline, including
bit 7, so the effect does not leave permanent terrain changes or stale colors.
Layer order remains the source-backed three-layer order.

There are still two HGR/text frame pairs at `$2000/$0400` and `$4000/$0800`,
an immutable `$A000–$BFFF` terrain baseline, and a fresh-blank PAGE2 flip.
The same private zero-page allocation suffices; reserved `$90` holds the color
phase. Logical collisions never inspect graphic bytes. See
[display.md](display.md) for the common mixed-mode and page ownership contracts.

## Executed evidence and boundaries

Executed on 2026-10-13 with the pinned cc65 V2.19 and py65 1.2.0 toolchain:

| Check | Result |
| --- | --- |
| Test suites | **27 passed for mono, 27 passed for color** |
| Native loader | Stock Disk II BOOT0 plus custom loader executed; full loaded application matches binary |
| Collision checks per variant | 360 cases |
| Sprite checks per variant | 460 phase/edge/page comparisons; color backgrounds include both bit-7 states |
| Alternating-page checks per variant | 60 frames; visible graphics/text unchanged before flip; full-page redraw oracle matches |
| Largest tested graphics write set | Mono 495 / color 440 distinct addresses per frame; diagnostic, not a speed benchmark |
| Color contracts | Six literal palette patterns, byte parity, cross-byte white adjacency, paired opacity and RGB PNG format |
| Native mono/color comparison | 26 frames with identical states/events; zero visible-page write violations |
| HTTP harness | HTML and executed frame GETs, R/A/R POSTs verified; screenshot decoded and boot capture visually inspected |
| Rebuild | Regenerated color resources, assembly and disks match all five recorded hashes |

The monochrome application is 14,322 bytes, padded through exclusive `$9800`;
the color application is 14,601 bytes, padded through exclusive `$9A00`.
Both remain below the `$A000` baseline. Exact evidence and hashes are in
[color-verification.json](color-verification.json), with generated detailed
reports under each build directory.

The preview uses a **digital artifact-color approximation**, including global
parity, byte phase, lit neighbors and dim chroma in alternating gaps. RGB values
are a development palette. It omits analog composite filtering and half-dot
phase displacement. The text font remains the development preview font; real
Apple text uses the machine's character ROM. Native graphics bytes are tested;
these PNGs do not establish calibrated monitor colors or physical timing.

No complete Apple emulator, physical Apple IIe, source Oric runtime or browser
keyboard/layout automation was executed. Next, boot the color disk in an
identified Apple IIe emulator, inspect sprite/terrain byte boundaries while
walking and crouching, and compare a composite monitor capture. Review the
palette and lost two-dot details before adopting this as the full port's default.
This project experiment does not promote a new knowledge-base guideline.
