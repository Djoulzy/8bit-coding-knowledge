---
id: PORT-LAIGLE-DOR-PRESENTATION-PITS
program: "L'Aigle d'Or"
cpu: ["6502"]
machines: ["apple-iie", "oric-1"]
analysis_status: draft
source_revision: "sha256:7f01e1a3d05825aab887952cd5711bea69d6525730aba5c1e25c814334fe77d7"
analysis_date: "2026-10-13"
---

# Oubliettes, text panels and original title

Original references mean BASIC line numbers in the pinned
[B1 listing](../../../../research/analyses/laigle-dor/extracted/aigledor.1.basic.txt)
and [B2 listing](../../../../research/analyses/laigle-dor/extracted/aigledor.2.basic.txt).
Original author: Louis-Marie Rocques, Loriciels 1984. Historical inputs remain
unchanged. This is port evidence, not a new validated guideline.

## Dedicated oubliette scene

B2 7000 sets the originating room's persistent floor bit. B2 7020 saves
`AP=NP`, `AX=XH+4`, sets `OU=1` and substitutes geometry 3. **NP remains the
originating room number**. Lines 7030–7046 construct a dedicated pit outline,
patterned panels and a different collision grid. B2 6910 draws its perspective
floor; 7048 may add atlas 28 depending on the ROM variation byte. The previous
port mutated the floor bit then reconstructed the ordinary room.

[room-builder.s](../src/apple/room-builder.s), `world_load_scene`/`scene_pit`,
now honor this override. Transient room fields are cleared and the pit stays
visible without a torch. It uses shared vectors and atlas pieces, with no
per-pit bitmap. The semantic map blocks 11–13 and 29–31, plus 41–71, following
line 5's pre-increment and 7046's absolute range.

Source `$2A` patterned side fill becomes a stable Apple gray material. Floor
lines use a repeating four-on/four-off target pattern; its phase relative to
Oric ROM DRAW is not runtime verified. Source endpoints are retained.

B2 7100 intentionally waits for **A**. Then **Space** stands, and **G** climbs
when a rope is available and the hand is empty (7200–7310). The lying equipment
stream is no longer forced after recovery or during climbing. Rope atlas 90
follows the ascent and its pixels are restored per frame page. One rope is
consumed. Return restores the saved room/x at y=180, retaining the opened trap.
Fall damage/drain still use the provisional target LFSR and hundredths; drain
now multiplies by five before rounding, fixing an erroneous zero increase.

## Full-screen text and live funds

[full-text.s](../src/apple/full-text.s) draws name entry, exterior, merchant,
inventory, clues and ending panels in **40-column full-screen Apple TEXT**.
It reuses the dynamic HUD formatter, deinterleaves the four rows into MAIN
text, and selects the hidden text page at the existing fresh vertical blank.
`full_visibility` restores 80-column mixed DHGR for gameplay: 160 graphics
rows and four bottom text rows, with the original paired frame buffers.

The panel header formats current 16-bit gold every frame. Buying a torch
changes visible 500 to 310; buying a rope changes it to 200. Prices and the
purchase transaction retain their source-backed behavior.

## Original title and lightning

[title_resources.py](../tools/title_resources.py) reads the exact B1
`$1801–$3740` 8,000-byte castle/crest/title bitmap. B1 1140/1150/1160's ink/paper
changes expose yellow lightning or hide it in blue. B1 1300/1305 reveal the
crest and magenta title. Author/copyright wording comes from 100/1309/1310;
the captured B2 6×8 font supplies converted letters. No replacement artwork
is generated.

Only the ink/paper attribute subset present in this pinned image is accepted.
Conversion uses complete DHGR palette cells for uniform colors, losing some
thin-stroke detail. CRT fringes can still occur at edges. Source graphic rows
0–189 fit into 0–159; full-height credits and a new keyboard prompt are placed
at 162/174/184. These are explicit Apple layout/font adaptations.

The title uses **192-row full-screen DHGR**, two frame pairs and a retained
baseline pair. Disk sectors 160–223 contain its 16 KiB main/aux raster. The
castle stays visible while shared sprites preload. Off/on byte patches animate
lightning on the hidden pair; after 72 target iterations each page reveals
the lower title/credits. Enter or Space advances to name entry. Original WAIT,
thunder and music timing are not reproduced; audio remains silent.

## Reproduction and verification

```sh
make test-game
make run-game
```

The preview uses port 8768. In Virtual II, mount `build/game/laigle-dor.do` or
`.nib` in slot 6, drive 1, and cold boot with 128 KiB / extended 80-column RAM.
The supplied enhanced ROM requires an enhanced/65C02 firmware configuration;
application instructions remain NMOS. Use a byte-identical disk copy for a
separate VM if the original image is already mounted elsewhere.

| Scenario | Executed evidence |
| --- | --- |
| Room 23 fall, pit grid/display, A/Space recovery, missing-rope denial, climb and persistent return | Native keyboard/6502 in functional Apple bus; `room23-pit.png` |
| 64 ordinary rooms, both frame pairs, 256 room/direction combinations, approved actor pixels | Native-world regression suite |
| Off/on title bytes, reveal on both pages, transition to TEXT | Native execution against bitmap conversion; `title-lightning.png`, `title-complete.png` |
| Enhanced firmware cold boot, final title, TEXT panels, gold 500 → 310 → 200, return to mixed DHGR | Virtual II 13.3, separate 65C02 1 MHz / 128 KiB VM, supplied ROM, Color monitor |
| Original Oric runtime and physical Apple behavior | Not tested |

[world-verification.json](world-verification.json) pins current artifacts and
scopes. The pit sequence was tested in the functional CPU harness; no complete
playthrough to room 23 in Virtual II is claimed. Full introduction/story,
audio, original ending presentation and entire-game replay remain open.
