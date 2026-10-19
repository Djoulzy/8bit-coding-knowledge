---
id: PORT-LAIGLE-DOR-MOVEMENT-SCENERY
program: "L'Aigle d'Or"
cpu: ["6502"]
machines: ["apple-iie", "oric-1"]
analysis_status: draft
analysis_date: "2026-10-19"
---

# Finer movement and readable scenery

This changes the native `make game` build. The approved room-12 prototype has
its own source collision oracle and retains its original movement profile.
The historical TAP, extracted blocks and ROMs are read-only inputs.

## Movement and interaction contract

[proximity.s](../src/game/proximity.s) is a **target adaptation**, rather than a
translation of every original collision decision. It separates proposed feet,
semantic obstacles and door proximity from rendering.

| Parameter | Previous native build | Current native build |
| --- | --- | --- |
| Horizontal walk increment | 2 source bytes = 12 source dots | 1 source byte = 6 source dots = 3 native color cells |
| Vertical walk increment | 10 source rows | 5 source rows (4 or 5 target rows after mapping) |
| Ordinary obstacle probe | Directional run of 3–5 semantic cells | Proposed foot-center cell, column `proposed_x + 2` |
| Side portal foot planes | Left `x=7`, right `x=31` | Left `x=2`, right `x=34`, `y>=175` |
| Far portal foot planes, geometry 0/1/2/3 | `y=160/140/140/180` | `y=145/125/125/155`, aligned at `x=17..20` |
| Fixture interaction window | Exact `x=27,y=160` | Quest: `x=27..30,y=155..165`; chest: `x=26..32,y=155..175` with its own pickup shortcut |

`actor_x` still uses source byte units and `actor_y` uses source scanlines.
World links, resource anchors and packed room records keep their original
units. Walking uses the proposal returned by the collision worker. Up/down
steps clamp to the floor limits when an action leaves a non-multiple-of-five
height, preventing a skipped threshold. A portal is reported at its foot plane;
approaching that plane is still a movement in the current room. Arrival positions
use the corresponding new planes.

The far-door window also accepts `x=17`: its stable foot base at source dots
114..125 lies inside the arch drawn by atlas 5 (source anchor 102, clear bottom
span 109..136). Previously the window began at 18, rejecting this visibly
aligned approach. The existing right-side tolerance and arrival `x=19` remain.
This is an Apple target movement adjustment; packed links and lock rules are
independent of the horizontal acceptance window.

The semantic grid remains the source-backed 3-by-40 map. Proposed heights
`<=150`, `151..170`, `>=171` map to its rows representing depths 140, 160, 180.
This closes the former "all other heights use the bottom row" gap. Walls retain
their semantic marks; a small geometry/depth corridor also prevents the narrower
probe from slipping around the isolated source wall marks. Side lanes open at
depth 175 to approach the door artwork.

Chairs, tables and chests additionally use a geometric foot test. The stable
foot base spans `[(move_x+2)*6, (move_x+4)*6)`, twelve source dots. Each
furnishing has a barrier from the room's rear floor plane to
the exclusive front edge of their artwork:

| Furnishing | Source-dot horizontal bounds | Exclusive front y | Blocked actor x |
| --- | --- | --- | --- |
| High-backed chair, field 4 / atlas 23, geometries 0/3 | `[168,186)` | 161 | 25..28 |
| High-backed chair, field 4 / atlas 23, geometries 1/2 | `[168,186)` | 138 | 25..28 |
| Wide table, field 5 / atlas 25, geometry 0 | `[168,210)` | 166 | 25..32 |
| Wide table, field 5 / atlas 25, geometries 1/2/3 | `[162,204)` | 143 | 24..31 |
| Chest, field 7 / atlas 26/27, all geometries | `[180,210)` | 166 | 27..32 |

This deliberately closes the route behind the furniture. Scenery is baked
into the baseline and the character is drawn afterward; allowing that route
would paint the character over the tabletop. Front and side approaches remain
available wherever the perspective floor corridor permits them. This is a
target collision adaptation shared by HGR/DHGR, not depth-sorted rendering or
an Oric instruction-level translation.

The first correction covered the high-backed chair, mistakenly named "table"
in this port's labels and documentation. The wide table is the different,
42-dot-wide atlas entry 25 in rooms 15, 17, 21, 56 and 61. Its former six `153`
grid cells left a rear gap at `y=145..150` in geometry 0, and insufficient side
clearance in geometry 1. The barrier covers those approaches as well as the
top surface. Scene labels now distinguish chair, table and pedestal.

The constructor still writes its original furnishing grid. Collision replaces
only chair field 4's `151`, table field 5's `153` and chest field 7's `154` tests
with their geometric barriers. Other obstacle values and other furnishings'
`151`/`153`/`154` cells keep their ordinary semantic behavior. Pits have none of
these barriers. This is a stable
foot rectangle, not a silhouette derived from animation frames or editor edits.

`P` samples the adjacent proposed foot cell using the **same** depth mapping.
A character stopped just before an object can crouch (`A`) and collect it (`P`).
The right-facing ground-item pose is now `x=5`, instead of `x=4`; left-facing
approach and downward approach are also tested. Chest and quest windows include
their source anchors but tolerate the closer positions made reachable by the
reduced clearance. Quest-pedestal facing, standing, empty-hand and objective
conditions remain in [full-core.s](../src/game/full-core.s). Chest access has a
separate approach window as described below.

These are semantic foot collisions, not per-pixel body collisions. A sprite may
overlap an object above its feet. The grid still has three depth bands; this is
not a new continuous-depth physics engine. Jump and climbing trajectories,
vertical interaction and enemy motion retain their existing source-based steps.
The target controller's drain/fuel cadence is unchanged: smaller walking steps
also reduce distance traveled per service tick. Original timing equivalence and
full-game balance remain part of W08/W09 playtesting.

Historical comparison: B2 `$4C73–$4CB2` dispatches collision probes;
`$4CB6–$4CDC` builds the grid pointer only at exact depths 140 and 160.
BASIC 4200/4300/4400 establishes source arrival coordinates; 10703 gives the
original pickup offsets; 10702/10785 and 10910 give fixture anchors. Refer to the
[original analysis](../../../../research/analyses/laigle-dor/routines.md) and
[extracted BASIC listing](../../../../research/analyses/laigle-dor/extracted/aigledor.2.basic.txt).

## Chest collision, opening and contents

The former three `154` cells were tested only in the middle depth band. They
left the top/rear of the chest walkable, while `O` required the shared narrow
`y=155..165` fixture window. A player standing just in front at `y=170` could
therefore receive Impossible instead of opening the chest. Both failures were
reproduced in executed regressions with the preceding binary.

The chest body uses the same barrier in both states: closed atlas 26 begins at
source `(180,136)` with a 30-row image; open atlas 27 begins at `(180,126)` with
40 rows. Both bottom edges are exclusive `y=166`. The stable horizontal body
envelope is `[180,210)`; the open lid's opaque pixels also fit within it.
The first normal walking height in front is `y=170`; the left stop is `x=26`.
Blocking the region behind this body also avoids drawing the actor over the
chest when walking at the rear wall. No scenery bitmap or grid data is changed.

[full_chest_reach](../src/game/proximity.s) accepts `x=26..32,y=155..175`, which
includes the left and front stopping positions as well as the original anchor.
`O` retains the original crowbar/empty-hand conditions (B2 10910..10965) and
sets the persistent open bits before rebuilding the hidden terrain. Keys do
not satisfy the chest opening rule. The six initial chest rooms are
4, 13, 26, 52, 58 and 60. Their supplied ROM variation values are all above 100,
so empty-hand opening is refused. The general `M<=100` exception is
retained for other states/firmware variations.

An open chest's `P` handler uses that same adjacent window before the ordinary
floor/quest pickup guards. It can now collect from the front, facing Up, as
well as the left, facing Right. This facing tolerance is an explicit target
adaptation of B2 10700/10702; the chest reward shortcut still skips ordinary
held-item/crouch requirements as in 10775. Furnishing 7, open state, proximity
and remaining treasure are required, and rewards clear the treasure once.
Floor pickups and quest-pedestal guards retain their separate behavior.

Room **26 is empty in the initial Oric records** (`TR=0`); opening it must
visibly raise the lid without creating gold, points or an item. The other five
initial chests contain gold or a vial. The focused tests cover opening through
the native `5`/`O` keyboard path in room 26, collision before/after opening in
all six rooms, the left/front approaches, refused keys/empty hands and one-shot
contents collection. Functional previews are `room26-chest-closed.png` and
`room26-chest-open.png` in each edition's build directory.

The adjacent `P` action now distinguishes `Ferme`, `Vide`, and the collected
content: `Fiole` in rooms 4/13/60 or `Or trouve` in 52/58. A second collection
displays `Vide` without another reward. `O` on an already open chest displays
`Deja fait` without further crowbar wear. See the
[outcome rules and native checks](presentation-and-pits.md#impossible-action-feedback).

## Room 18 / 25 navigation and the separate grille

The original records are directional. In B2 `$5600..$57FF`, room 18's far
opening is type 3, lock 0, destination 25 with arrival 2. In room 25, the **right
arch** returns to room 18 with arrival 0. Walking through these open arches
needs no key or Open command. Pressing Open on an arch is not the ordinary
transition trigger (B2 10900 only dispatches door types 1/2 to 4600).

Room 25's **far grille** is a different link: type 2, lock 2, destination 26
with arrival 2. B2 4600..4630 permits the iron key only for lock 1. This grille
therefore requires a selected crowbar (`5`, held-item code 6), facing Up at
the far threshold, then `O`. Each attempt consumes crowbar durability and may
fail; successful opening immediately executes the destination transition.
The original test is `RND(1)*ST < .3`, with `ST=2` here. The port uses its
documented native integer/random adaptation rather than Oric ROM RNG replay.
Gold-key use is reserved for the separately guarded secret-fireplace action.

See the read-only [B2 listing](../../../../research/analyses/laigle-dor/extracted/aigledor.2.basic.txt),
lines 4600..4710 and 10900, and [world.py](../model/world.py) for the record/link
decoding. Native keyboard regressions cover room 18's visible-center approach,
the return via room 25/right, both refused keys at room 25/far, and a reproducible
sequence of crowbar attempts reaching room 26.

## Flame animation and independent restoration

[torches.s](../src/apple/torches.s) restores two **small independent rectangles**
from the immutable room baseline on the hidden frame pair before drawing the
wall flames. They do not widen the actor's dirty rectangle across the entire
screen. The actor is then drawn over the flames; held flames join the actor's
normal dirty bounds. Both MAIN and AUX banks are restored. Room construction
and title/menus retain their existing ownership of the two frame pairs.

Original B2 `$40C8–$411F` selects atlas 36/37, changes the high phase bit in
`$0497`, tests its low lamp bits, and draws at `$69/$6A = 4/64` or `35/64`.
`$40B2` decrements the byte-column before drawing. For held torches it selects
72/73 and uses the eight position pairs at `$4120–$412F`, translated through
`$3EF8`. The port exports these four original atlas entries; their exact source
addresses/hashes appear in `build/game/resources/game-resources.json`.

The carried-flame x offsets are `0,3,0,3` for the four standing directions,
repeated for crouching. The native renderer already applies the shared
`(actor_x+dx+1)*6` source-dot anchor. An additional decrement in the offset
table incorrectly placed the flame six dots left of the torch head. Crouching
adds ten source rows to both equipment and flame; walking keeps the standing
equipment anchors. These anchors do not change the wall-flame positions.

The native phase holds for two controller ticks. Each alternating page therefore
receives **both** flame frames, avoiding a phase pinned to buffer parity. This
is a target cadence, not an Oric timing measurement. Rendering consumes no game
PRNG state and emits no synthesized sound. Yellow tips and orange bases are
Apple art choices. Unlit fixtures stay unlit; room-local lit flags allow a
single burning fixture. Initially fully lit rooms display both flames.

## Grilles, padlocks and secret marker

[world-art.json](../resources/world-art.json) records the native art edits.
[scenery.py](../tools/scenery.py) applies them to the shared atlas, without a
painting or special bitmap for each room.

The source grille entries 9/11/13 (B2 230/330, 120 and 140) use fine one-dot
outlines. Pair quantization merged some outlines into adjacent color cells.
Native grilles now have separated white bars, diagonal/horizontal rails, opaque
black gaps and a yellow padlock with a black keyhole. Bar extents and rail slopes
follow their source-facing silhouette; the precise cell artwork and enlarged
lock are new target art. Ordinary doors remain gray. The compact static-tile
format uses its formerly unused status 3 for a per-tile accent; header bytes
11/12 specify that accent and whether black holes must clear underlying scenery.
Approved actor tile encodings and masks are unchanged.

B2 397 draws fireplace atlas 20. B2 398 tests field `$0485` for 1/3 and performs
`CURSET 107,108,1`; 10907 uses the same secret flag for the gold-key action.
The port makes that distinction explicit with one shared small black round mark
on the **right pillar**, placed only for those secret flags. This enlarged gray/
black patch is target artwork (atlas ID 200), not an exact reconstruction of the
ROM's CURSET dot or a newly discovered original sprite. Source rooms
0, 11, 38, 49, 51 and 63 carry the marker. Ordinary fireplaces 9, 20 and 46 do not.

## Opening and traversing secret fireplaces

The former port set `passage` only at the exact source keyhole pose. It omitted
both B2 **10980**'s visible opening and **10405**'s crouched-Up transition, so
even a successful key action did not produce a usable passage.

[game/passage.s](../src/game/passage.s) keeps the gold-key and secret-flag guards
from B2 **10907** (`held_item=8`, facing 3, decoded field `$0485` equal to 1 or 3).
The target opening window is **x=14–20, y=125–145**, in source-byte/source-row
coordinates. It includes the original x=15, y=140 pose and the closer positions
reachable with the finer walking steps. Ordinary fireplaces, wrong keys,
incorrect facing and distant requests are refused. Reopening an already open
passage displays `Deja fait`, without closing it or consuming the key.

Opening requests a hidden-buffer terrain rebuild. [apple/passage.s](../src/apple/passage.s)
draws a shared opening at source x=114–130, y=98–120: a white top edge and black
interior. Its bounds come from B2 **10980**; filling intervening rows and showing
the final opening immediately are explicit target adaptations of the original
alternating-line animation. There is no new per-room bitmap. Both page buffers
receive the updated baseline while hidden, retaining the actor and HUD.

To enter, move to the center (**x=18–20, y=125–145**), crouch with **A**, face
the fireplace, then press **Up**. The controller honors B2 **10405** before
ordinary crouched direction handling. Standing, a closed fireplace, or being
off-center cannot trigger this transition. The source's north link supplies the
destination; the existing alternate arrival sets x=19, y=140, facing down and
crouched. The key is retained. The passage flag clears on arrival and does not
modify persistent packed room records.

| Fireplace links in the pinned Oric data | Behavior |
| --- | --- |
| 0 ↔ 63 | Catacombs / dungeon summit |
| 11 ↔ 51 | Ground-floor secret connection |
| 38 ↔ 49 | Ground-floor secret connection |

Native tests approach all six fireplaces through keyboard movement, select the
gold key, open, compare the complete baseline with an independently patched
raster, pause/resume, reject repeat opening/standing entry, then crouch and
traverse all six source links. They verify the alternate arrival and normal
destination terrain, unconsumed key, unchanged world records and no writes to
visible frame/text pages. Guard tests include the exact original pose and the
three ordinary fireplaces. See the [executed interaction record](interaction-verification.json).

## Reproduction and verification

The focused carried-flame, table and map-marker regression can be run for both
current editions, including the configured editor artwork:

```sh
make games
python3 tools/check_game.py --video dhgr --suite geometry
python3 tools/check_game.py --video mono --suite geometry
```

This fourteen-test selection covers 48 carried-torch compositions per edition
(four directions, three pose groups, two flame phases, both buffers), the five
chair rooms and two synthetic geometry variants, walking around the five actual
tables at the rear wall and along the front, ordinary depth-band obstacles,
door approach, the 18/25 round trip and 25/26 grille, the six chests and their
contents/approaches, quest reach, and the smiley for all 64 map positions.
Native flame/equipment comparisons
consume the configured sprite overrides; historical inputs remain unchanged.
Reports are written to
[DHGR geometry results](../build/game/geometry-test-results.json) and
[HGR geometry results](../build/game-mono/geometry-test-results.json), with
program/disk hashes and execution scope. The checks execute assembled NMOS
6502 instructions in the functional Apple bus model, including Disk II BOOT0.
They do not establish Virtual II CRT output or physical hardware behavior.
The new rear-route regression reproduced the defect with the preceding binary
in all five actual table rooms. The room-18 center regression also rejected
`x=17` in the preceding binary before the acceptance window was corrected.
The complete pre-existing suites were not rerun for this update; the focused
reports record the current execution results and hashes.
The chest regressions reproduced the inaccessible front action window and
walkable top in the preceding binary. Current results are recorded in the
focused reports above.
On 2026-10-19 all fourteen selected tests passed in each edition, including
keyboard opening in room 26 and the six-chest collision/reward scenarios.
`table-rear-blocked.png` and `table-front-approach.png` in each build directory
are functional-model previews of the new stopping positions in room 17.

The broader pre-existing checks remain available:

```sh
make game
make test-game
make test VIDEO=dhgr
```

Reload `build/game/laigle-dor.do` in Virtual II slot 6, drive 1, then **Boot**.
Eject/reinsert an older mount to avoid cached sectors. Use the existing enhanced
ROM, 64 KiB MAIN plus 64 KiB auxiliary memory, and the Color monitor setting.

The integration suite in [world_port.py](../tests/world_port.py) exercises actual
NMOS instructions for steps in all directions, intermediate-depth collisions,
door approach/arrival, 21 floor-treasure approach/pickup combinations, nearby
chest/quest actions, pit entry/recovery, both flame phases on both pages, repeated
frame restoration, unchanged terrain/PRNG and marker/padlock cells. The existing
64-room grid/layer oracle and 138 approved actor-render cases still apply.
The layer oracle derives scenery from source operations and native art policy,
rather than reading assembled tile bytes.

The current executed results and emulator scope are pinned in
[world-verification.json](world-verification.json). Functional previews use an
illustrative palette. They are distinct from Virtual II screen exports, Oric
runtime replay and physical hardware measurements. Whole-game traversal, original
timing and audio remain outside this change's verification scope.
