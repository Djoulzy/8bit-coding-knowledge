---
id: PORT-LAIGLE-DOR-TEST-MENU
program: "L'Aigle d'Or"
cpu: ["6502"]
machines: ["apple-iie"]
analysis_status: draft
analysis_date: "2026-10-19"
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
symbols, fireplaces and treasure pictograms). Its geography and artwork were
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

A **7×9 white smiley with dark eyes and a smile** marks the current room beside
its number. Its complete black-backed badge replaces a reserved area so the
eyes and mouth remain visible in both black and white rooms. This area stays
separate from the number, content pictograms and fixture badges.
The graphic footer always shows the room number, even when viewing another
floor or the legend. The map ignores the player's pit state: its room marker,
footer and legend do not change when the player falls into an oubliette. The
originating room number remains the current room used for the map position.

- Room polarity: dark rooms have a black background and white numbers/icons;
  permanently lit rooms have a white background and black numbers/icons.
  Hatching is removed. Initial lighting still follows `Room.light == 3`.
- Doorways: doors and grilles share the same solid symbol. Arches use an open
  symbol. A small black symbol tile makes either opening legible beside both
  room polarities. Lock markers are omitted. The metadata preserves both
  directed source types and lock fields; gameplay rules remain unchanged.
- First pictogram: fireplace only. Chairs, tables, chests, wall pictures,
  floor obstacles and other furniture have no map pictogram. Treasure inside
  a chest still appears as an item. A secret fireplace uses a **solid right
  pillar**, drawn in black in a white room and white in a black room; ordinary
  fireplaces keep their hollow right pillar. The separate left-wall secret
  badge is removed. All six initial secret fireplaces (0, 11, 38, 49, 51, 63)
  use this symbol. Room 63 follows B2 **397**'s fireplace override even though
  its packed furnishing field is 6. These are target map pictograms, not new
  historical sprites or gameplay rules.
- Second pictogram: scroll, gold, iron/gold key, vial, ring, lead eagle, book,
  diamond or golden eagle. The two keys and two eagles have distinct silhouettes
  so their legends also work in monochrome.
- Hazard letters: a small **H** at the upper right denotes a falling grille
  (*herse*); a small **o** at the lower right denotes a floor trap (*trappe*).
  Both are 3×5 pixels in the room's contrasting ink, inside the wall and clear
  of doorways and the player marker. The two letters can coexist.
- The symbols previously mislabeled as stairs in rooms **6, 13, 28 and 38**
  are removed from both map editions and the legend. A scan of all 64 source
  records finds `$0485 > 1` only in these four rooms: values 2, 2, 2 and 3
  respectively. B2 **635, 880–884** draws sprite 28 and writes two three-cell
  obstacle runs with semantic value `$9C` (156); these are not room links.
  The port retains these obstacles in gameplay (`room-builder.s` `@pile`
  and `full_collision_probe`), and only their map representation is removed.
  Room 38 keeps its secret-fireplace and vial pictograms. Its secret low bit
  remains independent of the omitted obstacle bit. The map metadata records
  this audit under `omitted_floor_obstacles`.

The original graphic is **sprite 28**, selected by B2 **884** with
`POKE #68,28`. Its atlas descriptor points to `$7FB8`; the 144-byte pixel
payload occupies `$7FB9–$8048` (9 Oric bytes per row, 16 rows). Decoding it
with [resources.py](../tools/resources.py) `sprite(Source(),28)` shows bones
and a skull: the map's former staircase silhouette was an incorrect target
interpretation. This is a visual identification, not a recovered original
asset name. The [enlarged monochrome preview](../build/game/sprite-028-oric-preview.png)
ignores serial color attributes. The historical sprite and its gameplay
collision marks remain intact.

The legend is page 3, grouped into two aligned columns: **Plan** contains the
native smiley beside `Vous`, followed by the fireplace, secret fireplace,
shared door/grille symbol, arch, room swatches and hazards; **Objets**
contains all ten treasure pictograms. The secret-fireplace pictogram appears
beside `Passage secret`, directly below the ordinary fireplace.

`Trappe` and `Herse` each have a miniature room outline with the corresponding
letter drawn inside: **H** at the upper right for a falling grille, **o** at the
lower right for a floor trap. These illustrations replace the old anonymous
dots and their positional explanation. The player illustration uses the same
7×9 row masks as the actual map marker. All symbols are grouped with their
labels; only the initial-state reminder remains below the two columns.
The legend includes no lock, generic-furniture or chest key, and no oubliette
player-status explanation.
Content remains **static initial state**: pickups,
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
`(14,19)`; the catacomb/upper-floor cards have a 28-row pitch. Doorways
and badges use individual HGR pixels. Static strings use the port's target
font; Apple TEXT and the character ROM are not used for the map.

The smiley begins at room offset `(21,2)`, aligned to a seven-pixel HGR byte.
[map.s](../src/apple/map.s) writes its nine rows only on the floor containing
the current room. The two room digits use ten resident seven-row digit glyphs
at scanlines 164–170. Both overlays use ordinary MAIN
stores, independently of the edition's gameplay `draw_cell` adapter. The smiley
replaces all seven bits of each reserved byte instead of ORing a face onto a
white room. The footer retains blank reserved bytes for its live room digits.
Neither overlay overwrites static letters, room numbers or content icons.

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

The text archive uses 2,635 bytes in AUX `$1400–$1E4A` (11 padded sectors,
physical 224–234), including the later checkpoint screens and removal of the
old death/victory TEXT panels, within the existing
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
check controls, ignored keys, pause/resume, unchanged packed
records/baselines/atlas, static quest icons after a grant, cache reuse and
restoration of both game buffers. Source metadata checks also cover the
specific keys, treasures, secrets and adjacent-door topology.

The 2026-10-20 presentation revision adds two host-side map-policy regressions
in [map_artwork_cases.py](../tests/map_artwork_cases.py): swapping every wooden
door with a grille and changing every lock leaves all map pixels unchanged;
removing every non-fireplace furnishing also leaves the pixels unchanged, while
removing fireplaces changes the map. The furniture-policy check now also clears
the floor-obstacle bit in all 64 records while preserving secret-fireplace bits:
this must leave every map pixel unchanged. It checks the four source rooms and
the absence of `Escalier` in the legend. Treasure icons remain.
The native all-room test checks both room polarities in every reserved marker
area and verifies complete smiley masks at all 64 positions. The focused map
selection initially contained five native integration cases and two host cases
per edition, with functional previews of all three pages.

The subsequent footer/fireplace revision adds a native overlay case proving
that pit state 0/1 produces identical bytes on every map page and both buffers.
A host policy case checks all six secret-fireplace pillars, the room-63
override, ordinary hollow pillars, removal of the old left-wall badge, and a
controlled dark-room variant. The focused selection now contains **six native
integration cases and three host cases per edition**. The actual gameplay pit
state and scene remain intact when closing the map.

Executed on 2026-10-18 for the full-screen HGR map: **five targeted tests per
edition passed**, including all 64 pin positions per edition, both buffers,
all three disk pages, MAIN-only map loads, exact video-switch state, the bottom
scanline, pit status, unchanged game data, cache reuse and HGR/DHGR restoration.
Inventory and modal help regressions also passed.

Executed on 2026-10-20 for the simplified inverse-room map before the subsequent
footer/fireplace revision: all seven focused cases passed in each edition
(five native integration cases plus two host policy cases). The executed
ground-floor, catacomb/upper and legend previews
were visually inspected. All 64 smiley positions, both frame buffers, pause,
cache reuse and gameplay restoration passed. This revision was not launched
in Virtual II or on physical hardware.

The latest floor-obstacle removal passed **all nine focused cases per
edition** on 2026-10-20 (six native integration cases and three host policy
cases). All three executed map previews were visually inspected: rooms
6/13/28/38 no longer display staircase pictograms, the fireplace and vial in
room 38 remain, and the legend omits `Escalier`. A separate static byte
comparison confirms that the two floor-map pages differ from the preceding
revision only at the four removed icons; H/o markers, treasures and doorways
are unchanged. Both program binaries and the editor artwork are unchanged.
Native checks still confirm that both pit-state values yield identical map
pixels on all three pages and both frame buffers. These results use the
functional 6502 harness; Virtual II and physical hardware were not tested for
this revision.

The [map verification record](map-verification.json) pins that map revision's
binaries, disk images and executed previews; `build/game*/map-test-results.json`
contains its results. Later graphical-ending builds have a separate
[verification record](ending-verification.json), including map-navigation
regression checks. Earlier full-suite, interaction and presentation records retain
their previous hashes and do not certify the new binaries. Run `make test-game`
and `make test-game-mono` for the complete suites when broader changes require
them. Execution here is in the py65 functional 6502/Apple bus with real Disk II
BOOT0, without a system-ROM cold-start. The revision has not been relaunched in
Virtual II or measured on physical hardware.
