---
record_type: port-display-experiment
program: "L'Aigle d'Or"
machines: ["apple-iie"]
cpu: ["6502"]
status: analyzed
review_date: "2026-10-13"
---

# DHGR room-12 prototype

This variant combines **140 independent color columns** with fine source-dot
patterns in the **560-dot DHGR stream**, over 160 graphics rows. It boots the native NMOS program, draws source-backed room 12 and
adapted actor frames, accepts the existing keyboard controls and alternates two
complete main+auxiliary frame pairs. Four native 80-column text rows remain
below graphics. Game logic, collision data and event logging are shared with
the monochrome version. Historical sources remain unchanged.

The [porting analysis](../../../../research/analyses/laigle-dor/portage.md) and
[architecture](../../../../research/analyses/laigle-dor/architecture.md) remain
the source evidence. The reference Oric ROM and actual Oric runtime capture
are still missing. The default room decoration uses the declared zero fixture.
Colors are new artistic choices, with no inference of historical ink fidelity.

The first revision flattened source-dot pairs and lost interior details. The
preceding [detail revision](dhgr-detail-review.md) restored individual dots and
masks. The current [material palette](dhgr-palette.md) colors actor detail and
adapts static contours to stable color cells. The next [actor refinement](dhgr-actor.md)
also uses stable cells for hair, trousers and brown boots, and retouches the
left-facing face. Other face/tunic/hand regions retain fine masks. The palette's 140-column limit must not
be treated as a requirement to discard fine luminance patterns.

## Reproduction

From `ports/laigle-dor/apple-iie/`, using the existing local pinned tools:

```sh
make bootstrap
make test VIDEO=dhgr
python3 tools/run.py --video dhgr
python3 tools/run.py --video dhgr --serve --port 8767
```

Open `http://127.0.0.1:8767`. Ctrl-C stops the server. A full emulator should
use a **DHGR-capable Rev-B-compatible IIe**, a configured 64 KiB extended
80-column card, standard CPU speed, ordinary DHGR color output and the existing
slot-6/drive-1 Disk II controller. Mount `build/dhgr/laigle-dor.do` in DOS order
or `build/dhgr/laigle-dor.nib`; boot using the [existing loader](toolchain.md).
No DOS/ProDOS filesystem, RGB-card extension or 65C02 instruction is required.
Automatic motherboard/card detection is outside the prototype contract.

`build/dhgr/` holds binaries, disk images, manifests, test/CPU reports, screenshots
and execution traces. Other video variants keep their own directories. To
compare gameplay against the actual monochrome binary:

```sh
make build
python3 tools/compare_video.py --video dhgr
```

For a supplied 16 KiB Oric ROM mapped at `$C000`, use
`tools/build.py --video dhgr --oric-rom /path/to/rom`, then
`tools/check.py --video dhgr` directly; `make test` rebuilds the default fixture.

## Hardware interpretation

Apple's [IIe Technical Note #3](https://mirrors.apple2.org.za/ftp.apple.asimov.net/documentation/hardware/misc/Apple%20IIe%20Technical%20Notes.pdf)
documents the resolution, installation requirements, switches, bank access and
two-page operation. This variant sets HIRES, 80COL, AN3-off and MIXED, leaves
80STORE off, and switches PAGE2 only when presenting a completed hidden frame.
Its color geometry is 140 independently selected four-bit cells per row.
Fine contrast edges can use individual serial dots, with output dependent on
monitor decoding. This does not provide 560 independently colored pixels. Mixed text uses
80 columns. Main/auxiliary seven-bit bytes alternate, auxiliary first; bit 7
does not encode an eighth displayed DHGR dot.

Color patterns are checked against the authors' standard DHGR packing and
palette mapping in [Apple2js canvas.ts](https://github.com/whscullin/apple2js/blob/ee0aed25f73c69d0245e86a2a5fccb3324c3056c/js/canvas.ts#L660).
Four bytes, two from each bank, carry seven color cells. The implementation
keeps a distinct lores-order palette index and raw serial four-bit pattern,
including conventional gray-pattern names. A cell can cross a byte and bank
boundary; every write uses masks to preserve the neighboring cells.

The target profile is [dhgr-profile.json](../resources/dhgr-profile.json).
Physical composite filtering, PAL-specific behavior and RGB expansion modes are
not calibrated. The default preview uses a sample-aware digital signal
approximation, including neighboring patterns and short white runs. The palette
diagnostic repeats each cell across four samples and hides fine detail;
monochrome displays actual serial bits. All use a **560×384 PNG**, with two
output scanlines per native row. It preserves
screen aspect while accommodating the narrow 80-column development text font.
Hardware uses the Apple character ROM instead.

## Memory and bank ownership

| Address | Main bank | Auxiliary bank |
| --- | --- | --- |
| `$0040–$0051` | Two installed read-worker routines | Unused; ALTZP stays off |
| `$0080–$00B6` | Private pointers and scratch | Unused |
| `$0100–$01FF` | Stack | Unused |
| `$0400–$07FF` | Text page 1, odd display characters | Text page 1, even display characters |
| `$0800–$0BFF` | Loader initially, then text page 2 | Text page 2 |
| `$0C00–$0C1C` | Controller/video state | Unused |
| `$0D00–$0DFF` | Silent event ring | Unused |
| `$0E00–$0E27` | HUD conversion buffer | Unused |
| `$2000–$3FFF` | Frame 1 main half | Frame 1 auxiliary half |
| `$4000–$5FFF` | Frame 2 main half | Frame 2 auxiliary half |
| `$6000` through loaded end | Application and resources | Unused; application is **not mirrored** |
| `$A000–$BFFF` | Immutable terrain main half | Immutable terrain auxiliary half |

Each displayed frame owns 16 KiB; two frames plus baseline consume 48 KiB
across the two banks. The current application is **15,076 bytes**, entry
`$6000`, with page-padded exclusive end `$9B00`, below the baseline. This is a
single-room memory fit; it does not establish the full game's fit.

[dhgr.s](../src/apple/dhgr.s) expands separate RLE terrain halves and initializes
both frame pairs while full text is selected. Code/resource reads ordinarily
stay in main RAM. RAMWRT is enabled only during controlled auxiliary stores or
initial buffer loops; main zero page and stack remain selected. RAMRD reads
execute through installed main-zero-page workers, which select auxiliary reads,
load through a pointer and restore main reads before returning. This avoids
banking out instructions at `$6000`; no ROM AUXMOVE call is used.

Per-page dirty rectangles use **serial byte columns 0–79**, not physical bank
columns 0–39. Repair restores both halves from that page's own old bounds.
All actor layers and HUD text are constructed in the hidden pair; presentation
waits for the same fresh IIe RDVBLBAR blank edge as the HGR renderer. Restart
retains both histories until repair. Dynamic terrain, multiple actors and room
changes still require the broader W07 compositor.

## Resource conversion and sprite representation

[dhgr.py](../tools/dhgr.py) retains the two source dots inside each four-sample
group separately for fine actor materials: each source dot owns two serial mask samples.
Mixed pairs retain their black gap or foreground side. The material pattern is
intersected with fine foreground masks; a zero intersection keeps the original
bright mark instead of erasing it. Full foreground pairs receive the row color.
Fully transparent Oric attribute cells remain transparent. The 20-dot HGR margin becomes ten
color cells; actor anchors are `10 + (source_x + 1) * 3`. Gameplay coordinates
are unchanged. Vertical cropping/resampling follows the established room-12
mapping. Terrain uses last-source-row precedence; successive sprite rows that
map to the same target row compose through their masks.

Sprites store two four-bit pair statuses per byte, retaining each source dot's
opacity and foreground flag. Both the legacy edge marker and full-interior
status now select the row material. A 16-byte
header provides width, height, row stride and seven dirty byte extents. This
format keeps assets compact without precomputing seven expanded color planes.
The renderer clips source y before it can wrap and updates each occupied cell
through at most two masked serial-byte fragments. It preserves neighboring
colors even when the cell straddles auxiliary/main bytes.

The requested palette gives wall edges/columns white, doors/arches gray and
torches brown. The actor has yellow hair, pink face/hands, green tunic/sleeves
and dark-blue trousers. [dhgr-palette.json](../resources/dhgr-palette.json)
separates art direction from code; its anatomical row bands are provisional.
Static materials use complete phase-aligned cells, with enclosed mixed-pair
dark marks enlarged into black cuts rather than filled. This deliberately
adapts static geometry to 140 color columns. Actor face/tunic/hand masks remain
fine-grained. Hair uses solid native color cells; trousers and boots use native
cells with dark cuts. Standing/walking boots start at lower-layer row 16;
crouching boots start at row 11. The left-facing skin additionally uses full
pink cells with explicit eye/mouth marks. See [actor art policy](dhgr-actor.md).
NTSC color fringes remain at some boundaries, even around white cells.

## Verification and remaining work

The [verification snapshot](dhgr-verification.json) records executed results,
program hashes, MMU/pixel checks, comparison and reproducibility evidence.
Detailed reports are generated under `build/dhgr/`. Checks execute stock Disk II
BOOT0, the custom loader and the assembled NMOS application in py65 with the
project's functional main/auxiliary mapping and simplified VBL/drive model.

Executed on 2026-10-13:

| Check | Result |
| --- | --- |
| DHGR suite | **44 tests passed** |
| HGR regression | 41 tests passed for mono; its native binary retains its earlier hash |
| Loaded application | Stock BOOT0 plus custom loader; all loaded bytes match the 15,076-byte application |
| Logical collisions | 360 source-coordinate/direction combinations compared with bounded independent model |
| Sprite composition | 460 cases across 23 source IDs, seven shift phases, viewport/edge clipping and two complete frame pairs |
| Native color writes | 480 cases: 16 colors × 15 x positions × two pages; masks preserve both banks, neighbors and page holes |
| Partial-cell writes | 120 cases: separate first/second-dot opacity, black/white patterns, bank boundaries and both pages |
| Detail conversion | Face/tunic/hands retain per-dot opacity; hair/legs deliberately use whole color cells; tests check palette, anatomical bands, leg gap and stable-cell masks |
| Alternating frames | 60 frames; both bank halves and text remain unchanged until flip; dirty repair matches full-redraw oracle |
| Graphics write scope | Maximum 765 distinct `(bank,address)` graphics writes in a tested frame; no full-page runtime copies |
| Main/aux safety | ROM/application bytes and both baselines unchanged; scoped bank controls restored; no auxiliary game-state writes |
| RAMRD instruction fetches | `$0043`, `$0045`, `$004C`, `$004E` only; workers run in main zero page, without mirrored code |
| Stack/events | Minimum SP `$F5` in covered paths; zero speaker accesses; existing ring/tick checks pass |
| Gameplay comparison | 26 frames with identical native monochrome/DHGR states and events |
| HTTP preview | HTML/three monitor GETs and A/R commands verified; native frames produce RGB PNGs |
| Rebuild | Six binary/media/resource hashes identical after full regeneration |
| Virtual II 13.3 | Dedicated NMOS/128-KiB session, selected project ROM, mounted `.do`, cold boot, color scene, movement/floor and crouch/stand smoke checks; real screenshot exported |

Counts and write sets are test diagnostics, not physical performance results.
Aggregate tests return nonzero on failure; each report pins its application hash.

Pixel/byte comparisons, bank restoration and zero visible-page writes are
model results. They do not certify physical disk timing, original Oric scheduling
or physical frame rate. The separate Virtual II 13.3 smoke check and exported
capture for the actor revision are documented in [actor refinement](dhgr-actor.md).
The previous capture is retained in the [detail review](dhgr-detail-review.md). Next,
refine pose-specific color boundaries and compare physical composite output. No renderer choice is promoted
to a validated or benchmarked knowledge-base guideline.
