---
record_type: port-project
program: "L'Aigle d'Or"
cpu: ["6502"]
machines: ["apple-iie"]
status: prototype
review_date: "2026-10-13"
---

# L'Aigle d'Or — Apple IIe first playable milestone

The [local graphics editor](../../../tools/apple-iie-editor/README.md) opens the
native screens and sprite atlas, preserves masks and bank packing, and exports
artwork projects that can be applied with `LAIGLE_ARTWORK=/absolute/project.json`.
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
Press Enter or Space, then type a name,
Return, then `1` to enter or `3` to visit the merchant. This development build
also contains initial transitions, items, actions, hazards and menus; the full
W07/W08 acceptance gates remain pending. Read
[world-construction.md](docs/world-construction.md) for resource ownership,
source references, executed checks and known rendering differences.

Exterior and modal panels use full-screen TEXT; the merchant header updates
gold after every purchase. Gameplay returns to mixed DHGR. In an oubliette,
press **A**, then **Space** to stand; **G** climbs with a rope and an empty hand.
The room number remains the originating room, but the dedicated pit scene is
displayed. See [presentation-and-pits.md](docs/presentation-and-pits.md).
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
**IL FAIT NOIR ICI !** panel. See [room-transitions.md](docs/room-transitions.md).

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

All outputs can be regenerated. Build/check tools are repository-authored;
historical build scripts are not executed. `make clean` removes only `build/`.

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
