---
record_type: port-project
program: "L'Aigle d'Or"
cpu: ["6502"]
machines: ["apple-iie"]
status: prototype
review_date: "2026-10-19"
---

# L'Aigle d'Or — Apple IIe port

The full-game development port now has **two separate boot disks**:

| Version | Disk image | Presentation |
| --- | --- | --- |
| [HGR monochrome](build/game-mono/laigle-dor-hgr-mono.do) | `build/game-mono/laigle-dor-hgr-mono.do` | Original Oric sprite/scenery dots; HGR 280 × 160 with a centered 240-dot scene and four 40-column text rows |
| [DHGR color](build/game/laigle-dor-dhgr-color.do) | `build/game/laigle-dor-dhgr-color.do` | Approved 16-color adaptation, fine source-dot details and four 80-column text rows |

Both versions share the same game rules, 64-room constructor, controls,
collisions, double buffering, title/intro, merchant and H/? help. Both currently
require **128 KiB with auxiliary RAM**. HGR uses auxiliary RAM for resources;
its displayed graphics and text pages are in MAIN. In Virtual II select a
**Mono** monitor for HGR, and **Color** for DHGR. Use the same supplied-ROM / Disk
II slot-6 setup described below. Choose the disk before booting.

```sh
make games                 # build both full-game disks
make test-game-mono        # execute the HGR full-game checks
make run-game-mono         # functional HGR preview, port 8769
```

`make game`, `make test-game` and `make run-game` select the full DHGR build.
`make game-mono` builds the full monochrome version. `make build VIDEO=mono`
continues to build the older W06 room-12 reference prototype.
See [HGR implementation and verification](docs/hgr-mono.md).

Both full-game editions now use native masked-byte sprites, faster background
copies and conservative per-page reuse of an idle actor. Strength drain and
torch wear use video refreshes so faster rendering does not accelerate them.
See the [renderer changes](docs/renderer-optimization.md) and
[input latency measurements](docs/input-responsiveness.md) for scope,
remaining limits and reproducible checks.
For a future project, the
[porting optimization workbook](../../../research/analyses/laigle-dor/portage-optimizations.md)
explains the reusable mechanisms, bank/page ownership contracts, trade-offs
and tests to retain when adapting them.

The [local graphics editor](../../../tools/apple-iie-editor/README.md) opens the
native screens and sprite atlas, preserves masks and bank packing, and saves
retouches directly into `resources/artwork.json`. Normal `make games` builds
consume that saved input automatically. `LAIGLE_ARTWORK=/absolute/project.json`
can select an external override instead; an empty value selects standard artwork.
Run `python3 tools/apple-iie-editor/server.py --adapter laigle-dor` from the repository root.
Use the editor’s native-resource JSON export for the compiler; keep the full
workspace JSON for reversible editing. See [adapter instructions](docs/graphics-editor.md).

The W06 prototype boots a custom Disk II image, displays converted room 12,
animates the original character images, and implements turning, walking,
stop/stand, crouching and logical collisions. Movement continues without a new
key. It uses mixed HGR (160 graphics rows and four native text rows), alternates
both frame/text pages at vertical blank, and restores each page's previous actor
rectangle. Oric ink/paper cells are transparent; native silhouette masks preserve
the surrounding scene. Audio cues are logged in RAM. The right exit produces an event and retains
room 12; other rooms, items, enemies, menus and actual audio are future work.

There is now a separate **W07 native-world development build**. It reconstructs
all 64 room records with four generic wall templates, then upper/left/right
openings and parameterized decorations. It stores a shared atlas and compact
world data, with **no per-room bitmap or pre-rendered room variants**. The
approved DHGR room-12 prototype remains independently buildable.

```sh
make game
make test-game
```

Use `build/game/laigle-dor.do` or `.nib` in slot 6, drive 1. Configure DHGR and
128 KiB with the extended 80-column bank. The supplied enhanced Apple ROM needs
a compatible enhanced CPU configuration for firmware cold boot. The original
castle/title page now appears first, with lightning and a delayed title reveal.
Press Enter or Space to read the original text introduction, press a key,
then type a name,
Return, then `1` to enter or `3` to visit the merchant. This development build
also contains initial transitions, items, actions, hazards and menus; the full
W07/W08 acceptance gates remain pending. Read
[world-construction.md](docs/world-construction.md) for resource ownership,
source references, executed checks and known rendering differences.

Exterior and modal panels use full-screen TEXT. Death and victory instead use
the original artwork in full-screen HGR/DHGR graphics, with five-attempt named
tombs, the three-objective victory composition and O/Return to restart. See
[graphical endings and verification](docs/graphical-endings.md).
The exterior greets the player
by name; the merchant has a spaced price list, live funds and purchase feedback.
**H** or **?** opens the command/item help page and pauses the game, even during
an action or inside another menu. Any key returns to the previous screen without
executing that key. During name entry use **?**, since H remains a name character.
Gameplay returns to mixed DHGR. In an oubliette,
press **A**, then **Space** to stand; **G** climbs with a rope and an empty hand.
The room number remains the originating room, but the dedicated pit scene is
displayed. See [presentation-and-pits.md](docs/presentation-and-pits.md).
Pit walking follows its own perspective floor, with jumps rejected when the
landing would cross a wall. The original alternate-font wall/trap hints are
restored in both editions; owning the ring still hides unopened-trap hints.
See [pit markers and collision checks](docs/pit-markers-and-collisions.md).
`make run-game` starts the full-build functional preview on port 8768.

The native build now walks in half-sized steps, tests obstacles at the proposed
feet and requires approaching the visible doorway before changing rooms. Ground
objects can be approached, then collected with **A**, **P**. Wall and held
torches use the original two-frame flame assets. Grilles have white separated
bars and yellow padlocks; secret fireplaces have a small black mark on their
right pillar. See [movement-and-scenery.md](docs/movement-and-scenery.md) for
the collision/interaction contract, original evidence and target artwork.

Room changes now keep the previous graphics frame visible while preparing the
next room in the hidden buffer, then flip only after its actor/effects/HUD are
complete. They no longer expose an old TEXT menu. Actual darkness has a clean
**Il fait noir ici !** message centered above the same four bottom HUD rows
(40 columns in mono, 80 in DHGR). See [room-transitions.md](docs/room-transitions.md).

Falling-grille traps now descend visibly before their outcome. Walking onto
the trigger is lethal even with a torch; a horizontal jump (**S**) across it
allows survival. Help pauses the fall. See
[grille traps and darkness](docs/grille-traps-and-darkness.md) for original
source references, native sequencing and focused execution checks.

The four gameplay text rows now contain the original room description on rows
1–2, **Force / Points** on row 3 and **Pieces d'or / Main** on row 4. The hand
shows its item name; an empty hand leaves the field blank. Coordinates, room
numbers and keyboard reminders are removed from this panel. See the
[HUD source mapping](docs/presentation-and-pits.md#compact-gameplay-hud).

Press **I** to open a spacious, two-column inventory: provisions with quantities,
equipment with **oui/non** possession indicators, quest objects and collected
scroll count. The held item appears above the lists. **Space**, **Return** or
**Escape** closes it; **H / ?** opens help and returns to the inventory.
Keys **0–5** select the held item during gameplay.

Press **C** during castle gameplay to display a **12-byte checkpoint code**
such as `0000E0-C01F40-00E400-00550B`. Note its 24 hexadecimal characters. To
resume later, boot either edition, type your name, then choose **4. Reprendre
avec un code** outside the castle. Enter the code and press **Return**;
Backspace corrects it and Escape cancels. H/? preserves the code or partial input.

The code retains room, inventory, gold, points, integer strength and sixteen
pickup flags, so collected treasure cannot award its rewards again. Resume
starts safely on the near floor with empty hands and the newly typed name.
Wear, doors and traps restart. Each provision stock must fit 0–7; larger stocks
produce an explicit error without changing the game. Old 18-character codes
are incompatible. See the [format, limits and verification](docs/checkpoints.md).

Menus, descriptions, clues, HUD labels, feedback and map captions use mixed
case for readability. Native Apple TEXT uses the IIe's built-in lowercase;
names preserve the typed case, while gameplay commands accept either case.
See [inventory and text presentation](docs/presentation-and-pits.md#inventory-and-lowercase-text)
for implementation and reproducible focused checks.

Action outcomes appear **in inverse video**, right-aligned on the first text
row: `Impossible` for an invalid action, `Vide`/`Ferme` for empty/closed chests,
`Echec` for a failed crowbar attempt, `Casse` for an exhausted crowbar,
`Verrouille` for an unsuitable tool/lock, and `Deja fait` for an already open
chest or secret passage. Successful pickup names the reward (`Fiole`,
`Or trouve`, etc.). Descriptions and statistics remain visible. Messages stay
until the next gameplay key; help pauses them. See
[action feedback and focused checks](docs/presentation-and-pits.md#impossible-action-feedback).

To use a secret fireplace, select the **gold key (3)**, face the fireplace and
press **O** nearby. Once the opening is visible, move to its center, crouch with
**A**, then press **Up** while facing it. See [secret-passage controls and evidence](docs/movement-and-scenery.md#opening-and-traversing-secret-fireplaces).

For testing in either full-game edition, press **Ctrl+D** during gameplay
to open the hidden test menu. **1** grants all inventory objects, including
quest objects, and nine of each consumable. **2**, a decimal room number
**0–63**, then **Return** teleports directly to that room. Backspace edits the
number; **Escape** or **Ctrl+D** resumes play. The menu pauses gameplay and
shows the current room number. Enter the castle normally before opening it.
**3** opens a graphical map with numbered rooms, source-backed doorways,
fireplaces, treasure pictograms and a white smiley beside the current
room number. Dark rooms are black; lit rooms are white with inverse labels
and icons. Doors and grilles share one symbol; locks and other furniture
are omitted, including the floor-bones decoration in rooms 6, 13, 28 and 38
(previously misidentified as stairs on the map).
Secret fireplaces have a solid right pillar; the map's legend
shows this symbol. The footer displays the room number and controls only.
**Space/Return**
cycles ground floor, catacombs/upper rooms and legend; **1/2/3** selects a page.
**Escape** returns to the test menu; **Ctrl+D** resumes gameplay. Contents show
the initial Oric data; cross-floor and secret links have numeric references.
Both editions show the same **full-screen HGR monochrome map at 280 × 192**,
with native-pixel lettering, finer pictograms and graphic status/control lines.
Closing it restores the edition's normal mixed HGR or DHGR gameplay mode.
The map is a schematic inspired by the supplied plan. See
[map controls, display limits and focused tests](docs/test-menu.md#graphical-room-map).

This is a local development port of the analyzed Loriciels 1984 edition credited
to Louis-Marie Rocques. Historical inputs remain unchanged. Original reuse and
redistribution rights are unresolved; generated historical assets, ROMs and
disk images remain local ignored outputs. No new license is assigned to them.

## Build and test

Run from this directory. Python 3.9+, Make and a C compiler are sufficient.
No Python package installation or system-wide assembler installation is needed.

An optional **native HGR color experiment** is also available. It retains mixed
mode, alternating pages, controls and collision rules; color choices are a new
Apple adaptation. The default remains monochrome. Build/test outputs coexist:

```sh
make test VIDEO=color
python3 tools/run.py --video color --serve --port 8766
```

Open `http://127.0.0.1:8766`. Color disks are
`build/color/laigle-dor.do` and `build/color/laigle-dor.nib`; select standard
**HGR composite color / NTSC artifact color** in a full emulator. No RGB
expansion card or double-HGR is required. To compare the two native binaries:

```sh
make build
python3 tools/compare_video.py
```

See [color experiment and verification](docs/color-experiment.md) for palette,
two-dot artwork conversion, byte-wide phase limits and preview scope. Running
`make test`/`make run` without `VIDEO=color` selects the monochrome build.

The **DHGR variant** uses a 16-color palette with **140 independent color columns**,
retains fine source-dot patterns in its 560-dot serial stream, and uses
four native **80-column** text rows and double buffering across main/auxiliary
RAM. It requires a DHGR-capable IIe with a configured 64 KiB extended 80-column
card (128 KiB total). To build, test and open its executed preview:

```sh
make test VIDEO=dhgr
python3 tools/run.py --video dhgr --serve --port 8767
```

Open `http://127.0.0.1:8767`. Boot disks and reports are in `build/dhgr/`;
select ordinary DHGR color and 128 KiB in a complete emulator. See
[DHGR implementation and checks](docs/dhgr.md) and its
[target profile](resources/dhgr-profile.json). The scaled preview is not a
claim of 560 independent color pixels. The default build remains monochrome.

The DHGR palette uses white wall edges, gray doors and brown torches; the actor
has yellow hair, pink skin, a green tunic, blue trousers and brown boots. Hair
and legs use stable native color cells; face/tunic/hands keep their fine masks,
with a separately retouched left-facing portrait.
See [actor refinement](docs/dhgr-actor.md). Static material contours use phase-aligned color cells
with dark cuts for enclosed source marks. See [palette adaptation](docs/dhgr-palette.md).
The local monitor selector provides sample-aware color,
raw-dot monochrome and coarse-palette diagnostics. The last view deliberately
hides subcell detail. See [detail review and Virtual II evidence](docs/dhgr-detail-review.md).

```sh
cd ports/laigle-dor/apple-iie
make bootstrap
make build
make test
python3 tools/run.py
```

`bootstrap` downloads checksum-pinned cc65 V2.19 and py65 1.2.0 from their
authors, builds only `ca65`/`ld65`, and obtains private test ROMs. Everything
goes into `local/`. Network access is needed on the first bootstrap. Source
Makefiles were inspected; there is no `make install`. The V2.19 tag reports
`ca65 V2.18 - V2.19` / `ld65 V2.18 - V2.19`; the build manifest records the
actual output rather than assuming an internal version string.

An existing assembler can be used instead:

```sh
CA65=/path/to/ca65 LD65=/path/to/ld65 python3 tools/build.py
```

py65 and the local test ROMs are still required for the execution tests. The
known-good pinned chain is the default. See [dependencies](tools/dependencies.json)
and [toolchain contracts](docs/toolchain.md).

## Launch and controls

For an immediately usable local view of the **executed binary**:

```sh
make run
```

Open `http://127.0.0.1:8765`. This is a functional CPU test harness with a local
web display, not a complete Apple IIe emulator. Each display request advances a
target iteration. Its wall-clock rate is unrelated to a physical 1 MHz system.
Ctrl-C stops the server. An occupied port can be changed with
`python3 tools/run.py --serve --port 8766`. In restricted agent environments,
opening a local listening socket may require the environment's network permission.

| Key | Prototype action |
| --- | --- |
| Left / Right / Down / Up | Turn; repeat the same direction to walk |
| J / K / N / U | Alternative left / right / down / up |
| Space | Stop and stand |
| A | Crouch |
| R | Reset this prototype to room 12 |
| Return / Escape | Additional stop aliases |

While walking, a direction key first stops the character. Release does not stop
walking. Keyboard repeats can therefore alternate stop/walk; use discrete key
presses for the source-style controls. Lowercase letters are normalized. Other
gameplay bindings are ignored at this milestone and do not implement their full
game actions. See [compatibility decisions](docs/compatibility.md).

For a full Apple IIe emulator or a physical disk-image device, mount
`build/laigle-dor.do` as a **DOS-order 140 KiB image**, or use
`build/laigle-dor.nib` as a raw 35×6,656-byte nibble image. Configure a Disk II
16-sector controller in slot 6, drive 1, main RAM, standard CPU speed and a
monochrome HGR display. Boot drive 1. From an appropriate monitor environment,
`C600G` enters that controller's boot firmware. The disk has no DOS catalog or
ProDOS filesystem; attempting to BLOAD a named file is not its launch method.

The existing tests execute the actual Disk II firmware and custom loader from
`$C600`; physical cold boot, real drive settling, full emulator integration and
hardware have **not** been tested. Composite color output is outside this
monochrome target profile. The application does not return to DOS or the monitor.

## Outputs and source separation

| Location | Role |
| --- | --- |
| [src/game/core.s](src/game/core.s) | Display-independent W06 controller and bounded semantic collision |
| [model/](model/) | Independent host movement/world models and selected full-game rule expressions |
| [src/apple/](src/apple/) | Loader, HGR renderer, keyboard and silent event sink |
| [tools/resources.py](tools/resources.py) | Source-hashed extraction, scene translation, sprite/viewport conversion |
| [resources/](resources/) | Target profile and sound-event catalog; generated historical data are excluded |
| `build/resources/manifest.json` | Per-resource offsets, hashes, source IDs, room fields and provisional ROM status |
| `build/game.bin`, `game.map`, `game.lbl`, `game.lst` | Native binary, allocation, symbols and ca65 listing |
| `build/laigle-dor.do`, `laigle-dor.nib` | Generated boot media |
| `build/test-results.json`, `cpu-verification.json` | Aggregate tests and executed CPU coverage |
| `build/execution.json`, `room12-boot.png`, `room12-after.png` | Scripted execution trace and decoded HGR captures |

The table above describes the earlier W06 outputs. The two maintained full-game
editions live in `build/game/` and `build/game-mono/`; see the
[build directory guide](docs/build-outputs.md). Their build outputs can be regenerated
with `make games`. Build/check tools are repository-authored; historical build
scripts are not executed.

For routine housekeeping, use `make tidy`. It removes legacy prototype binaries,
exported prototype resources, object/listing files and temporary Virtual II disk
copies while retaining both full games, their test resources, reports/captures
and the `latency-baseline/` comparison archive. Preview its selection with
`python3 tools/tidy_build.py --dry-run`. `make clean` removes the entire `build/`
directory, including those retained outputs and archives.

## Fidelity and outstanding inputs

The original Oric reference ROM is still missing. B2 line 607 reads the 64-byte
variation table at `$D000–$D03F`, including `$D00C` for room 12. The default
zero fixture selects a provisional decoration position. It does not establish
Atmos or Oric-1 room equivalence. Supply a local **16 KiB ROM mapped at `$C000`**:

```sh
python3 tools/build.py --oric-rom /path/to/reference-oric.rom
python3 tools/check.py
```

Do not follow this command with `make build`/`make test`, which rebuild the
explicit default zero fixture; use `tools/check.py` directly for that selected
build. Its manifest records the ROM hash. The project does not redistribute
this ROM or infer the original intended revision from its filename.

W00 lacks an Oric runtime trace, font-state capture and reference screenshots.
W03 currently covers independent predicates and the W06 controller, not every
original action or ROM floating-point/RNG sequence. The renderer uses a declared
monochrome/viewport policy and source-backed geometry, not an Oric runtime image.
[Work-package status](docs/work-packages.md) states the completion boundary of
every W00–W06 gate.

## Evidence and next iteration

The [porting workbook](../../../research/analyses/laigle-dor/portage.md),
[routine analysis](../../../research/analyses/laigle-dor/routines.md) and
[verification report](docs/verification.md) are the review entry points. This
project uses [GEN-0002](../../../docs/common/semantic-collision-grid.md) to keep
collision semantics independent of HGR and observes the
[Apple IIe guides](<../../../docs/machines/Apple/Apple IIe/BEST-PRACTICES.md>).
It does not promote renderer or pacing choices to validated guidelines.

See [display implementation](docs/display.md) for page ownership, dirty repair,
sprite masks, viewport mapping and the mixed-mode text contract. The HUD shows
initial forces/points/gold/held-item values; coordinates and actor status update.
Full-game energy/economy updates remain outside W06. The native program uses the
Apple text ROM; the functional preview draws the same text RAM with a small
development font, so its letter shapes do not certify the machine's charset.

Next: pin and run the Oric reference; compare room 12 and action ordering;
boot these images in a full, identified Apple IIe emulator; then implement W07
room transitions with the same source-hashed resources and trace comparisons.
