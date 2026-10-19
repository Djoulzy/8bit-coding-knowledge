---
id: PORT-LAIGLE-DOR-TEST-MENU
program: "L'Aigle d'Or"
cpu: ["6502"]
machines: ["apple-iie"]
analysis_status: draft
analysis_date: "2026-10-18"
---

# Hidden development menu

This is a new Apple port testing aid shared by the HGR monochrome and DHGR color
full-game editions. It is not historical game behavior or a promoted technique.
The [historical analysis](../../../../research/analyses/laigle-dor/overview.md)
and original sources remain unchanged. W06 room-12 reference disks do not have
this menu.

## Controls

Enter the castle normally, then press **Ctrl+D** (ASCII `$04`). The shortcut
also works during darkness, a jump, a fall or oubliette recovery. It is not
listed in the ordinary H/? help page. Title, introduction, name entry, exterior,
merchant, help and other modal pages retain their normal controls; return to
gameplay to use the shortcut.

The menu uses 40-column full-screen TEXT and shows the current room number.
Controller ticks, movement, actions, strength loss, torch wear and enemy/hazard
services pause. Unknown keys are ignored, including the legacy R reset key.

| Key | Operation |
| --- | --- |
| `1` | Grant every inventory category; stay in the menu |
| `2` | Begin room-number entry |
| `3` | Show the room map on the page containing the current room |
| `0`–`9` | Enter one or two decimal room digits after `2` |
| Backspace / left arrow (`$08`) | Remove the last accepted room digit |
| Return | Validate and teleport; return to gameplay |
| Escape or Ctrl+D | Close the menu, cancelling any partial room request |

Room numbers are **0–63 inclusive**, matching the source's 64 packed records.
An empty number, 64–99 or a third digit produces an error without changing the
room. Backspace clears the error and edits the accepted digits. The closing or
confirming key is consumed, with game services suppressed on that iteration.

In the functional browser preview Ctrl+D sends `$04` to the native program;
Command/Option browser shortcuts are left alone. Virtual II must pass the
Control key combination to its Apple keyboard. Reload a rebuilt disk by
ejecting/reinserting the image and selecting Boot.

## Graphical room map

Both editions use **full-screen 280×192 MAIN HGR**, with one bit per pixel and
no horizontal pixel doubling. The map's labels, status and controls are drawn
in graphics; all 192 scanlines are available. **Space/Return** cycles through three
pages; **1/2/3** selects the ground floor, catacombs/upper rooms, or legend.
Escape returns to the hidden menu; Ctrl+D resumes gameplay. Unrecognized keys
are consumed. Game services stay paused, including on the closing iteration.

The supplied Amstrad map inspired the presentation (room outlines, doorway
symbols, furniture and treasure pictograms). Its geography and artwork were
not imported. Initial contents and directed links come from the pinned **Oric
B2 `$5600–$57FF`** records, decoded with the existing `Room` model. The 49
ground-floor rooms use `x=6-((n-9)%7), y=(n-9)//7`: every ordinary link between
ground-floor rooms joins adjacent cells in this layout. This is a schematic,
not a measurement of physical distances or compass orientation.

Catacomb rooms 1–8 form a perimeter cycle, with room 0 shown as an isolated
inset. Rooms 58–63 are separate upper-floor cards. Floor grouping follows B2
4150–4170. Cross-floor links and the nonlocal fireplace passages are printed
as room-number pairs. The castle exit is specifically room 12's far opening
(B2 4701–4710), not the unused destination bits in that record.

A **7×9 white map pin with a dark center** marks the current room beside its
number. The previous locator was only three rows high. The pin has its own
reserved area, separate from the number, two content pictograms and fixture
badges. The graphic footer always shows the room number, even when viewing
another floor or the legend. In a pit, the originating room remains marked;
`Oubliette: X` replaces the ordinary `Oubliette: -` status.

- Doorways: a gap for an arch, a filled door, or a barred grille. A nearby dot
  means at least one direction has a nonzero lock field. It does **not** imply
  that every lock takes a key. Door type and lock requirements can differ by
  side; the metadata preserves both directed records. When symbols differ,
  the grille takes priority over the solid door, then the open arch.
- First pictogram: fireplace, chest, generic furniture, or stairs when no
  furniture occupies that slot. Other furnishings are intentionally grouped.
- Second pictogram: scroll, gold, iron/gold key, vial, ring, lead eagle, book,
  diamond or golden eagle. The two keys and two eagles have distinct silhouettes
  so their legends also work in monochrome.
- Small badges: hatching for non-permanent lighting, two high right-edge dots
  for a trap, a low right-edge dot for a falling grille, and a left-side stroke
  for a fireplace secret. Two middle dots additionally mark stairs when a
  furnishing takes the first pictogram. Several badges can coexist.

The legend is page 3. Content remains **static initial state**: pickups,
opening doors/chests, lighting and grants do not edit these maps. Book, diamond
and golden eagle take icon priority over ordinary treasures in rooms 1/62/63.
Transient enemies, trap recovery destinations, secret accessibility and
one-way lock requirements are not expanded into a walkthrough.

[debug_map.py](../tools/debug_map.py) compiles the map with original target
pixel glyphs and pictograms. `resources/maps.json` contains all 64 coordinates,
contents, 137 directed records (including the exterior), and 58 drawn adjacent
door pairs. It records provenance and display limitations. The ground and
catacomb layouts are separate from the mutable game state. The historical
room constructor still uses its four shared geometry templates; these three
cartography pages do not introduce per-room scenery bitmaps.

### Display and storage

The compiler uses native 280×192 coordinates, 5×7 mixed-case letters and
7×7 content pictograms. Ground-floor room cells are 35×20 pixels, starting at
`(14,19)`; the catacomb/upper-floor cards have a 28-row pitch. Doorways, locks
and badges use individual HGR pixels. Static strings use the port's target
font; Apple TEXT and the character ROM are not used for the map.

The pin begins at room offset `(21,2)`, aligned to a seven-pixel HGR byte.
[map.s](../src/apple/map.s) overlays its nine masks only on the floor containing
the current room. The two room digits and the pit indicator use resident
seven-row glyph masks at scanlines 164–170. Both overlays use ordinary MAIN
stores, independently of the edition's gameplay `draw_cell` adapter. Reserved
blank bytes prevent overwriting static letters, room numbers or content icons.

Three identical native rasters occupy physical sectors **240–335** (24,576
bytes) on both disks. Each 8 KiB page is loaded through the existing Disk II
loader into the **hidden MAIN HGR page**, without modifying AUX frame data.
Each frame page has a map-page tag; once both contain the current page, idle
frames perform no graphics writes or disk reads. Switching pages can require
disk access. The application does not promise instant switching on a physical
drive.

At presentation, `full_visibility` selects 40 columns (`$C00C`), disables DHGR
through `$C05F`, and selects full graphics (`$C052`). The next ordinary frame
restores mixed mode, with `$C00D/$C05E` for the DHGR edition. `80STORE` remains
off so page selection addresses the two real HGR pages. The functional preview
now follows these actual video switches when choosing its raster decoder.

All map phase bits are zero and the resources contain only black/white dots.
An Apple IIe composite color monitor can still interpret fine HGR patterns as
artifact colors; pure black/white output depends on the monitor or emulator's
Mono setting. There is no automatic Virtual II monitor-setting change. Do not
use the IIGS `$C029` monochrome control on a IIe: Apple's
[IIGS Technical Note 29](https://apple2.gs/technotes/tn-iigs-029/)
describes that separate machine capability. The program's HGR/DHGR switches
follow the high-resolution chapter of
[Inside the Apple IIe](https://vintageapple.org/apple_ii/pdf/Inside_The_Apple_IIe_1985.pdf).

The terrain baseline, WORLD, collision grid, atlas and actor are retained.
Map entry clears old sprite restoration rectangles and marks both terrain
buffers pending. Map drawing bypasses ordinary terrain repair. On resuming,
the existing hidden-page preparation restores the game baseline, then its
actor/effects/HUD before flipping. This avoids rebuilding a room or resetting
an ongoing jump, fall, enemy, lamp timer or random state just to close the map.

## Inventory semantics

Granting fills vials, torches, ropes and crowbars to **nine each**, sets both
key/ring/lead-eagle possession bits (`$0F`), all three scroll bits (`$07`) and
clears the missing-objective bits (`$00`: book, diamond, golden eagle owned).
Repeated grants refill these amounts; they do not add an unbounded count.

Torch and crowbar lifetimes are initialized through the existing game helpers
(200–299 ticks and 20–39 uses respectively). This consumes the normal target
PRNG. Gold, score, strength, poison, drain and the selected hand are preserved.
All ordinary hand selections become available after closing the menu. Select
`1` during gameplay to hold a torch if a teleported room is dark.

Granting quest objects also satisfies the ordinary victory prerequisite when
leaving room 12. It can bypass one-time reward and puzzle paths, so use a fresh
game when testing progression. Owned quest objects disappear after rebuilding
the current scenery; packed room mutations and lamp history are retained.

## Teleportation and rendering

[debug.s](../src/game/debug.s) validates the number before indexing WORLD, then
cancels pit/passage, staged action, walking, gate-jump, enemy/contact and hazard
state. Cancelling a jump restores its saved hand item. Persistent room edits,
inventory, lamp history, player identity, score, gold, strength and PRNG state
are retained; teleportation itself grants no reward or invulnerability.

The existing parameterized constructor rebuilds the destination's baseline and
semantic grid; it does not load a room bitmap. Spawn uses the near floor band
(`y=180`), starts at `x=19`, and scans right through `x=32` for an empty semantic
foot cell (`GRID[x+2] == 0`). This avoids source rooms whose center contains a
trap or obstacle. All 64 original rooms have a free cell in this bounded range;
the defensive fallback is `x=19` if future room data fill the entire range.
Facing, pose and frame return to the neutral downward stance.

The destination keeps its ordinary lighting and persistent traps/locks.
An unlit room without a held torch therefore still uses the darkness panel.
While the menu is visible, terrain baselines are retained and the normal
hidden-page repair may remove old actors from the graphics buffers. On return, the
existing pending-page mechanism prepares the hidden graphics/text frame and
flips it when complete; the other frame is refreshed on the following tick.
Normal collision, traps, damage and enemies resume after that first frame.

Menu state occupies MAIN `$1362–$1366`; map cache/scratch uses `$1367–$136B`.
Modes `$0D/$0E/$0F` select the graphical pages; `$0C` is the hidden TEXT menu.
Map controls are intercepted before game dispatch and clock services. Static
menu scripts are preloaded in the shared AUX text archive. Map footer scripts
are no longer needed because their text is part of each HGR raster.

The text archive uses 2,768 bytes in AUX `$1400–$1ECF` (eleven padded sectors,
physical 224–234), including the later checkpoint screens, within the existing
3 KiB allocation. MAIN LOWCODE starts
at `$13C0`, after the state/name allocations, and remains bounded by `$1DFF`,
below the `$1E00` disk buffer. The linker installs its relocated bytes before
the baseline overwrites the load image. MAIN and AUX remain separate physical
banks; resident code/data and the bank worker remain below MAIN `$A000`.

## Reproduction and evidence

From the port directory:

```sh
make games
python3 tools/check_game.py --video dhgr --suite map
python3 tools/check_game.py --video mono --suite map
```

The shared [integration tests](../tests/world_port.py) execute the assembled
menu in both profiles, covering modal pause and close-key consumption, all
inventory categories and usable hands, unchanged economy, empty/out-of-range/
overlong room input, editing/cancellation, room 0 and 63, cancellation of pit/
jump/enemy/hazard state, preserved WORLD and PRNG, safe spawn, and initialization
of both hidden frame buffers. The independent constructor checks spawn-space
availability in all 64 original rooms. Existing all-room/grid/layer, movement,
quest, pit, title, help and merchant checks remain in the full suites.

Map tests compare the three loaded native rasters plus marker/status against expected
bytes on both frame buffers, exercise all 64 native locator placements, and
check controls, pit annotation, ignored keys, pause/resume, unchanged packed
records/baselines/atlas, static quest icons after a grant, cache reuse and
restoration of both game buffers. Source metadata checks also cover the
specific keys, treasures, secrets and adjacent-door topology.

Executed on 2026-10-18 for the full-screen HGR map: **five targeted tests per
edition passed**, including all 64 pin positions per edition, both buffers,
all three disk pages, MAIN-only map loads, exact video-switch state, the bottom
scanline, pit status, unchanged game data, cache reuse and HGR/DHGR restoration.
Inventory and modal help regressions also passed.

The [map verification record](map-verification.json) pins these binaries,
disk images and executed previews; `build/game*/map-test-results.json` contains
the results. Earlier full-suite, interaction and presentation records retain
their previous hashes and do not certify the new binaries. Run `make test-game`
and `make test-game-mono` for the complete suites when broader changes require
them. Execution here is in the py65 functional 6502/Apple bus with real Disk II
BOOT0, without a system-ROM cold-start. The revision has not been relaunched in
Virtual II or measured on physical hardware.
