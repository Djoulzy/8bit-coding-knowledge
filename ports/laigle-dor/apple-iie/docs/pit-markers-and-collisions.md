---
id: PORT-LAIGLE-DOR-PIT-MARKERS-COLLISIONS
program: "L'Aigle d'Or"
cpu: ["6502"]
machines: ["apple-iie", "oric-1"]
analysis_status: analyzed
analysis_date: "2026-10-20"
---

# Alternate symbols and the oubliette floor

This fixes both Apple editions. Historical inputs and editor artwork remain
unchanged. Original author: Louis-Marie Rocques, Loriciels 1984. Source references
are BASIC line numbers in the pinned
[B2 listing](../../../../research/analyses/laigle-dor/extracted/aigledor.2.basic.txt).
This is port evidence, not a promoted knowledge-base guideline.

## Why the right-wall mark became a parenthesis

B2 **660** places `CHAR41,1,1` at source `(220,110)` in room 36. The second
argument selects the alternate character set. The port exported codes 33–41
from the standard HIRES bank at `$9800`; standard code 41 is literally `)`.
The [Oric Atmos manual](https://www.defence-force.org/computing/oric/library/lib_manual_oric/files/manual_atmos.pdf),
printed pages **86–87**, documents `CHAR`'s charset argument and the HIRES
standard/alternate bases `$9800`/`$9C00`. A glyph is eight rows; its address is
the chosen base plus eight times its character code, with six useful bits per row.

[game_resources.py](../tools/game_resources.py), `native_artwork`, now reads
the alternate bank. `game-resources.json` records each code, atlas ID, original
CPU address and eight captured bytes. Code 41 is read from **`$9D48`**:
`00 00 11 0A 04 0A 12 01`, which gives the crossed mark rather than punctuation.
The glyph remains shared atlas ID 169, with its source anchor preserved.
[world_scene.py](../tools/world_scene.py), `Constructor`, selects the same bank
for the independent operation-level mono/DHGR reference renderers. The title's
ordinary lettering still uses its own standard font.

This corrects a source-selection error, rather than inventing a new warning
icon. Captured B2 bytes and documented bank selection are verified; the original
Oric runtime's font contents after every graphics transition were not replayed.

## Trap hints and the ring

B2 **790–799** sets the floor's semantic trap cells, draws atlas 16 when the
trap is already open, otherwise selects alternate code `33+R` where
`R=INT((M AND 63)*5/63)`. The same bank error affected these hints. The compiler
now supplies their original custom rows rather than punctuation.

The port retains the ring rules and explicit source anchors, with a target
fallback for the implicit variants:

* B2 **794** suppresses unopened-trap hints when the ring is owned
  (`possessions & $04`). The hidden test menu's complete equipment includes it.
* The ring does **not** hide an already opened hatch.
* **795–798** explicitly position variants 1–4 relative to the trap anchor.
  For variants 0 and 5, B2 supplies no explicit `CURSET`. The earlier port kept
  its preceding cursor at `(214,80)`, so the marker overlapped the right wall
  torch rather than appearing on the floor. Correcting the font bank alone
  did not solve this placement bug, reported again for room **55**.
  Both variants now use the target floor anchor **`(N+18,176)`**, centered
  horizontally over the opened hatch. The initial world uses variant 0 in
  rooms **5, 53, 55, 61 and 62**. Room 55 has M=72, semantic cells 15–17,
  N=78 and therefore a marker at **`(96,176)`**. Variant 5 is covered by a
  controlled M=63 fixture, as no initial trap room uses it.
  This fallback is an explicit Apple layout adaptation. The exact original
  Oric cursor after the preceding machine-code blit remains unverified.
* No warning appears merely because a room is dark: a torch must first make
  the room visible. Existing ordinary hints remain small and intentionally
  subtle; no larger replacement marker is added.

All twelve initial trap rooms are covered by native raster checks: **0, 5, 7,
23, 28, 32, 40, 41, 53, 55, 61, 62**. Codes 39 and 40, used by B2 **1110/652**,
also benefit from the corrected shared bank.

## Dedicated foot collisions in the pit

B2 **7030–7040** draws the pit outline through source points
`(72,199)`, `(81,179)`, `(104,159)`, `(134,159)`, `(157,179)`, `(166,199)`.
The preceding Apple movement adapter treated it as an ordinary geometry-3
room, applying its wider corridor and unrelated coarse grid bands. This allowed
walking onto the side panels while blocking parts of the actual pit floor.

[proximity.s](../src/game/proximity.s), `full_pit_collision`, now selects a
separate envelope before ordinary room bounds, furnishings or portal checks.
It keeps the existing walking increments: one source byte horizontally and
five source rows vertically. Stable feet occupy source dots
`[(actor_x+2)*6, (actor_x+4)*6)`; the animated head/arms are not a wall probe.
Allowed foot depth is **160–195**, using the conservative back edge of each
five-row band to stay inside the drawn polygon:

| Source foot y | Minimum actor x | Maximum actor x, inclusive |
|---|---:|---:|
| 160–164 | 16 | 18 |
| 165–169 | 15 | 19 |
| 170–174 | 14 | 20 |
| 175–179 | 13 | 21 |
| 180–184 | 12 | 22 |
| 185–189 | 12 | 22 |
| 190–194 | 11 | 23 |
| 195 | 11 | 23 |

The pit's historical semantic grid is retained for provenance/other consumers;
walking no longer interprets its coarse wall bands as modern foot collisions.
The pit never returns a numbered-room portal or a second fall. Room number,
opened-trap state, recovery with A/Space and rope ascent retain their existing
rules. After G the original saved room/x and y=180 are restored.

Horizontal jump initiation also checks the landing eight source bytes away,
at the original foot depth, through the same envelope. An invalid landing
reports `Impossible` without starting the action or discarding the held item.
Valid jumps keep their trajectory and item restoration. Airborne sprite y is
visual height, not floor depth. Vertical jumps and rope ascent keep their staged
motion. These foot limits and jump guards are target adaptations, not claims
of original Oric collision equivalence.

The worker uses existing `move_x`, `move_y` and `blocked` scratch. Its compact
tables occupy CODE, collision workers occupy LOWCODE, and the existing quest
reach helper moves to CODE to fit the established allocations. Two redundant
stores before pickup's complete proposal calculation are removed; pickup
behavior is unchanged and covered by focused regression cases. No new memory
bank, framebuffer, CPU instruction extension or room bitmap is required.

## Reproduction and evidence

From the port directory:

```sh
make games
python3 tools/check_game.py --video mono --suite pits
python3 tools/check_game.py --video dhgr --suite pits
```

[pit_geometry_cases.py](../tests/pit_geometry_cases.py) pins the alternate glyph
bytes independently of the compiler constant and exercises the native raster
worker on both frame pages. It checks all twelve trap rooms, source anchors,
the R=0/5 fallback, ring masking, and opened-hatch visibility. A new complete
constructor/rendering regression checks floor pixels in rooms 55, 5, 53, 61
and 62 on both displayed buffers, with and without the ring. The preceding
isolated glyph test accepted the wrong wall cursor, so it could not detect
room 55's missing floor marker. This regression was observed failing on the
previous executable before the placement fix.
An independent rational-coordinate
polygon oracle checks **7,360** movement probes per edition (40 x coordinates,
46 y coordinates, four directions), including both depth limits and side walls.
Keyboard/CPU scenarios cover pit routes, valid/invalid jump landings, recovery,
rope return, help, ordinary room movement/portals, the room-36 falling grille,
and pickups after the redundant-store removal.

The focused selection contains **14 tests per edition**. Execution reports are
`build/game/pit-test-results.json` and `build/game-mono/pit-test-results.json`;
the [verification snapshot](pit-markers-verification.json) pins their program
and disk hashes. Generated previews in both directories are
`room36-marker.png`, `room23-trap-hint.png`, and `pit-floor-walking.png`.
`room55-trap-hint.png` and `room55-trap-ring.png` show the reported room with
the floor mark present and intentionally hidden, respectively.

Execution uses py65's functional NMOS 6502 and the port's Apple bus, including
real Disk II BOOT0. Assembly/link assertions statically check memory bounds.
Virtual II, system-ROM cold-start, physical Apple hardware, and the original
Oric runtime were not executed for this revision. These checks are neither a
complete adventure replay nor a performance benchmark. Older verification
records keep their original hashes and do not certify these new binaries.
