---
id: PORT-LAIGLE-DOR-MOVEMENT-SCENERY
program: "L'Aigle d'Or"
cpu: ["6502"]
machines: ["apple-iie", "oric-1"]
analysis_status: draft
analysis_date: "2026-10-13"
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
| Far portal foot planes, geometry 0/1/2/3 | `y=160/140/140/180` | `y=145/125/125/155`, aligned at `x=18..20` |
| Chest/quest interaction window | Exact `x=27,y=160` | `x=27..30,y=155..165`; original facing/item/pose guards retained |

`actor_x` still uses source byte units and `actor_y` uses source scanlines.
World links, resource anchors and packed room records keep their original
units. Walking uses the proposal returned by the collision worker. Up/down
steps clamp to the floor limits when an action leaves a non-multiple-of-five
height, preventing a skipped threshold. A portal is reported at its foot plane;
approaching that plane is still a movement in the current room. Arrival positions
use the corresponding new planes.

The semantic grid remains the source-backed 3-by-40 map. Proposed heights
`<=150`, `151..170`, `>=171` map to its rows representing depths 140, 160, 180.
This closes the former "all other heights use the bottom row" gap. Walls retain
their semantic marks; a small geometry/depth corridor also prevents the narrower
probe from slipping around the isolated source wall marks. Side lanes open at
depth 175 to approach the door artwork.

`P` samples the adjacent proposed foot cell using the **same** depth mapping.
A character stopped just before an object can crouch (`A`) and collect it (`P`).
The right-facing ground-item pose is now `x=5`, instead of `x=4`; left-facing
approach and downward approach are also tested. Chest and quest windows include
their source anchors but tolerate the closer positions made reachable by the
reduced clearance. Original iron/gold-key, crowbar, objective and held-item
conditions remain in [full-core.s](../src/game/full-core.s).

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
passage is also refused, without closing it or consuming the key.

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
