---
id: PORT-LAIGLE-DOR-NATIVE-ROOMS
program: "L'Aigle d'Or"
cpu: ["6502"]
machines: ["apple-iie", "oric-1"]
analysis_status: draft
source_revision: "sha256:7f01e1a3d05825aab887952cd5711bea69d6525730aba5c1e25c814334fe77d7"
analysis_date: "2026-10-13"
---

# Generic room construction on Apple IIe

## Scope and historical evidence

The native world build uses **no per-room bitmap or pre-rendered variant**.
The earlier approved room-12 graphics prototype still has one cached terrain
image. It remains a separate build for visual comparison.

Original author: Louis-Marie Rocques; Loriciels, 1984. Historical inputs and
their licence status are described in the [analysis](../../../../research/analyses/laigle-dor/overview.md).
References below mean original B2 BASIC line numbers in the
[extracted listing](../../../../research/analyses/laigle-dor/extracted/aigledor.2.basic.txt),
not invented assembler symbols. No historical input is edited or linked as
executable Oric code.

The constructor is a translation of B2 100–1110. Its four wall templates come
from 200/300, 390/400/410 and 500–530; openings from 600/620/630 and the
geometry-selected far-door branches. Decorations and semantic collision marks
come from 600–699 and 700–1110. The packed-world decoder is `$3F14–$3FF1`.

## Resources and target environment

| Resource | Allocation / source | Role |
| --- | --- | --- |
| Mutable room records | MAIN `$1000–$11FF`; initial B2 `$5600–$57FF` | 64 eight-byte records across two 256-byte pages; geometry, flags, contents and three stored links |
| Current semantic grid | MAIN `$1200–$1277` | 120 cells; rebuilt alongside the visible room |
| Variation table | 64 resident bytes; supplied Oric ROM `$D000–$D03F` | Furnishing and trap placement; hash-pinned input rather than the prototype's provisional zeros |
| Shared walls | Four small main-bank command programs | Source-coordinate vectors and repeated atlas stamps; independent of room number |
| Shared sprites | AUX `$6000` onward, bounded below `$A000` | Static scenery, actor, equipment and enemy atlas; no room images |
| Terrain baseline | MAIN and AUX `$A000–$BFFF` | One current-room terrain pair, constructed at runtime |
| Frame buffers | MAIN and AUX `$2000–$3FFF`, `$4000–$5FFF` | Two alternating DHGR frame pairs; four mixed text rows |
| Bank-read code | MAIN zero page `$0040–$0051` | Safe instruction fetch while briefly enabling auxiliary data reads |

The target needs 128 KiB with an extended 80-column bank and DHGR support. The
application uses documented NMOS 6502 instructions. The supplied enhanced
Apple firmware requires an appropriate enhanced/65C02 configuration for its
own cold start; functional tests enter Disk II BOOT0 directly and do not test
the system ROM reset sequence. See [rom-profile.json](../resources/rom-profile.json).
ROM identification links point to the matching
[Oric MAME definition](https://github.com/mamedev/mame/blob/master/src/mame/tangerine/oric.cpp)
and [Apple firmware definition](https://github.com/mamedev/mess-svn/blob/master/src/mess/drivers/apple2.c).

## Construction order and interfaces

`world_load_scene` in [room-builder.s](../src/apple/room-builder.s) decodes the
current persistent record, clears the grid/baselines, then calls:

1. The selected shared wall/column program.
2. `scene_upper`, `scene_left`, `scene_right` for the upper and two side openings.
3. The geometry-3 left-border redraw prescribed by B2 150.
4. Furnishings, wall torches, floor/gate hazards, treasures and quest objects.
5. Invalidates both frame histories; the display copies the completed baseline
   into each pair only when that pair is hidden.

Openings are selected by the first three two-bit fields. State mutations such
as an opened chest, taken treasure or fallen gate alter the world record; the
same constructor then reads those flags on the next reconstruction. A change
of room needs no disk access. The disk loader preloads the shared atlas once.
The displayed room stays visible during construction. The first complete hidden
pair is presented at vertical blank; the former visible pair initializes on the
next iteration. See [room-transitions.md](room-transitions.md). The constructor
also publishes the semantic grid used by movement and pickup.
This confirms the existing [semantic-grid separation](../../../../docs/common/semantic-collision-grid.md)
within this target implementation; it is not a new technique fiche.

`scene_program_run` interprets only two bounded, generated command types:
vector endpoints and static atlas placement. It does not interpret a program
per room. `scene_line` uses signed 16-bit Bresenham error, with source-space
coordinates independent of Apple row addresses. `scene_stamp` retains the
source byte anchor `(CURSET_x div 6 + 1)*6`; glyphs use their direct pixel anchor.
Both paths use the common cross-bank DHGR cell compositor.

[game_resources.py](../tools/game_resources.py) exports compact records and
the shared atlas. `game-resources.json` records source addresses, dimensions
and hashes. Complete opaque/transparent actor cells use a lossless two-bit
status encoding where possible; fine actor pairs retain the approved four-bit
format. No duplicate painting is introduced for each room.

## Reproduction and evidence boundaries

From `ports/laigle-dor/apple-iie/`:

```sh
make game
make test-game
```

The image is `build/game/laigle-dor.do` (DOS-order direct sectors, no DOS
filesystem) or the nibble equivalent. Use slot 6, drive 1, a 16-sector Disk II
controller and an Apple IIe with the required auxiliary bank. Names accept six
characters; Return opens the exterior menu, `1` enters the castle and `3`
opens the merchant. This remains a W07 development build, not the finished game.

The actual firmware sector decoder, startup atlas preload and native
constructor are exercised by `tools/check_game.py`. Tests compare all room
grids and both frame pairs against a source-expression oracle. Rendering is
compared with an independent **layer-level target oracle**, which consumes
source-backed operations rather than generated geometry programs.

The [executed record](world-verification.json) pins the tested program, disk,
atlas and firmware. **Twenty checks passed**, including all 64 original room
records, both frame pairs, 256 room/direction transition combinations, 138
approved-actor render cases, selected inventory/economy/reward paths and the
four original clue texts, pit recovery, title sequence, finer movement/proximity,
21 ground-item approach/pickup cases, scenery/flame checks, hidden-only frame
initialization and darkness recovery. The application is 17,912 bytes and the
shared atlas 15,134 bytes; the title raster is an
additional 16,384 disk bytes. These are build sizes, not performance measurements.

The target quantizes individual atlas layers before composition. The approved
prototype quantizes the completed source-space raster. Material-boundary
differences and the new deliberate grille/lock artwork are expected;
`room-verification.json` records their combined cell counts (7,590 total, at most
610 in a room; room 12 remains 15). This is a comparison with the unretouched
completed source raster, not a failed target-layer oracle.
Neither oracle reproduces the Oric ROM line rasterizer, final ROM-adjusted
glyphs, timing or PRNG. Room 12 and the presentation changes have now been
observed in Virtual II; all-room visual acceptance and physical measurements
remain pending. See [presentation-and-pits.md](presentation-and-pits.md) and
[movement-and-scenery.md](movement-and-scenery.md). The original
approved graphics build remains unchanged.

## Remaining work

The rules/actions module is under active development. Complete source-timing
equivalence, every staged action/enemy path, original introduction/ending
presentation and a full gameplay replay are not certified by room construction
tests. Audio remains a silent event log. Signed hundredths and a deterministic
target LFSR are provisional policies; they do not emulate Oric BASIC floats or
ROM RND. Separate performance measurements are needed before recommending
this renderer as an optimization.
