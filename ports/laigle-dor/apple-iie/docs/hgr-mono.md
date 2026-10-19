---
id: PORT-LAIGLE-DOR-HGR-MONO
program: "L'Aigle d'Or"
cpu: ["6502"]
machines: ["apple-iie", "oric-1"]
analysis_status: draft
source_revision: "sha256:7f01e1a3d05825aab887952cd5711bea69d6525730aba5c1e25c814334fe77d7"
analysis_date: "2026-10-18"
---

# Full-game HGR monochrome edition

## Scope and source graphics

This is a second rendering profile of the native-world development port. It
shares game rules, movement/collisions, all 64 rooms, items, actions, enemies,
text pages and modal help with the DHGR build. Neither edition claims a complete
validated replay of the historical game. Audio remains a silent event log.

The source is Louis-Marie Rocques / Loriciels' 1984 edition, documented in the
[original analysis](../../../../research/analyses/laigle-dor/overview.md).
Historical inputs are unchanged. The exporter reads B2's original atlas using
the width/height/pointer tables at `$9400/$9500/$9600/$9700`. All actor and scenery
foreground dots are retained horizontally, including original grilles, locks,
flames and the original left-facing portrait. The DHGR clothing bands, portrait
retouch and redesigned color grilles are exclusive to the color profile.

Serial Oric ink/paper cells remain transparent; they do not introduce attribute
blocks or color clash. Graphic data retain their original inverse-bit handling.
The established row-span masks provide opaque sprite interiors and transparent
surroundings. Static additive stamps keep their source semantics. The secret
fireplace cue follows B2 **398**, the single source point at x=107, y=108;
the enlarged DHGR right-pillar marker is not used in HGR.

The scene retains the existing viewport: source rows 35–199 map to 160 graphics
rows, with the last source row winning when rows coincide. Source x=0–239 maps
to HGR x=20–259. Sprites clip to that source window before an 8-bit x coordinate
can wrap. This preserves one horizontal HGR dot per Oric dot, within a native
280-dot scanline. The four bottom TEXT rows remain 40 columns.

## Shared engine and separate renderer configuration

`HGR_MONO=1`, `DHGR=0`, `FULL_GAME=1` selects the new profile. The renderer in
[dhgr.s](../src/apple/dhgr.s) shares frame scheduling, sprite decoding and layer
composition, with a one-bit HGR writer selected at assembly time. Each packed
two-bit atlas status denotes transparent, opaque black or foreground. The
HGR writer sets/clears one MAIN bit and leaves byte bit 7 zero.

Graphics run in ordinary HGR, `80COL` off and double HGR disabled. Frame pages
`$2000/$4000` and their text pages alternate at the existing fresh vertical blank.
Only the hidden page is repaired, initialized and drawn. Room changes retain the
previous completed frame while rebuilding the MAIN baseline, then present a
complete destination frame. No bitmap is stored per room.

[mono.py](../tools/mono.py) converts original sprite masks/dots and provides an
operation-level reference that reads historical atlas data, independently of
generated atlas bytes and geometry programs. The builder uses the same four
geometry templates and upper/left/right openings as DHGR.

## Allocation and disk layout

| Resource | HGR monochrome allocation |
| --- | --- |
| Two displayed/drawn frames | MAIN `$2000–$3FFF` and `$4000–$5FFF` |
| Current terrain baseline | MAIN `$A000–$BFFF` only |
| Shared atlas | AUX `$6000–$B9ED`, 23,022 bytes; bounded below `$C000` |
| Shared full-text scripts | AUX `$1400–$1AD6`, 1,751 bytes, including the hidden test menu/map footer |
| Graphical test map | Three HGR pages, 24,576 bytes at disk sectors 240–335; hidden MAIN page loading and a live marker, with four text rows below |
| Bank-read workers | MAIN zero page starting at `$0040`, below `$0080`; MAIN zero page and stack remain selected |
| Extra resident code | MAIN `$0E30–$0EFF` allocation for secret-passage handlers, installed before title/baseline construction |
| Atlas disk sectors | Physical 96–185, padded to 90 sectors |
| Monochrome title | Physical 192–223, 8,192 bytes |
| Text scripts | Physical 224–230, twelve padded sectors |

The atlas occupies AUX addresses which serve as the DHGR baseline in the color
edition. **HGR room construction, page preparation and title restoration never
write that AUX range.** The all-room test checks the atlas remains unchanged.
The HGR linker configuration [full-mono.cfg](../src/full-mono.cfg) gives the
atlas a 24 KiB allocation. Its larger disk range ends before the relocated
monochrome title; the builder checks the boundary.

The title uses B1 `$1801–$3740` foreground dots, a MAIN-only full-height HGR page,
and the existing 190-to-160 title viewport plus captured-font credits. Ink/paper
equality hides lightning in its off phase. Original castle/title shapes are
retained as monochrome foreground; the original color relationships are omitted.
The monochrome title inverts only source rows 0..99 (native rows 0..83,
x=20..259): a white sky surrounds the black castle and hills, and lightning
appears dark against the sky. Horses, crest, title lettering and credits keep
their existing polarity. Both lightning phases and the corresponding saved
editor documents use this treatment. The DHGR title retains its color palette.
The title, narrative and name-entry sequence stays common to both editions.

## Build and launch

From `ports/laigle-dor/apple-iie/`:

```sh
make games
make test-game-mono
make run-game-mono
```

The functional preview is at `http://127.0.0.1:8769`. The separate DHGR preview
uses `make run-game` on port 8768. An alternative profile selector is
`make game GAME_VIDEO=mono`; the older `VIDEO` variable selects W06 prototypes.

Boot either named disk in Virtual II, Disk II slot 6 drive 1:

- `build/game-mono/laigle-dor-hgr-mono.do` or `.nib`: select **Mono** display.
- `build/game/laigle-dor-dhgr-color.do` or `.nib`: select **Color** display.

Both currently require 128 KiB. The supplied enhanced Apple ROM needs the
existing compatible enhanced/65C02 firmware configuration for cold boot;
application instructions remain documented NMOS 6502. Eject/reinsert a rebuilt
image and Boot to avoid retained emulator disk sectors.

## Verification scope

The monochrome suite inherits game/UI scenarios from
[world_port.py](../tests/world_port.py) and replaces color-specific checks in
[mono_world.py](../tests/mono_world.py). It covers:

- All 64 source-backed scene/grid constructions and both MAIN frame pages.
- 138 original actor-sprite placements, including clipping.
- Source wall/hand flames on both pages and partial lighting states.
- Original grilles and source secret cue, title lightning/reveal and TEXT return.
- Movement, 256 room/direction links, pickup, purchases, clues, pit/rope recovery,
  help/pause and text HUD behavior inherited from the shared game suite.
- HGR/40-column switch state, no AUX graphics writes, unchanged AUX atlas,
  zero phase bits and absence of visible-page writes.

`build/game-mono/game-test-results.json` and the
[verification record](hgr-mono-verification.json) identify the earlier full-suite artifacts.
The checks execute real NMOS instructions and Disk II BOOT0 in the functional
bus model. They do not execute the original Oric runtime, the Apple system-ROM
reset path, physical hardware, or certify real video/drive timing. New HGR PNGs
are functional previews, not Virtual II captures. Both full-game editions now
include the shared [hidden test menu](test-menu.md). The subsequent
[action-feedback revision](presentation-and-pits.md#impossible-action-feedback)
and secret-fireplace repair are pinned in the [interaction record](interaction-verification.json),
with focused native execution checks in both profiles. The earlier full-suite
records retain their original program hashes. `room-verification.json` is
regenerated by the interaction suite's all-room constructor check.
