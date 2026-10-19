---
id: PORT-LAIGLE-DOR-PRESENTATION-PITS
program: "L'Aigle d'Or"
cpu: ["6502"]
machines: ["apple-iie", "oric-1"]
analysis_status: draft
source_revision: "sha256:7f01e1a3d05825aab887952cd5711bea69d6525730aba5c1e25c814334fe77d7"
analysis_date: "2026-10-18"
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
The exterior, merchant, inventory, name entry, introduction and help use positioned text
scripts rather than four crowded menu rows. Other panels reuse the dynamic HUD
formatter, deinterleave the four rows into MAIN text, and select the hidden text
page at the existing fresh vertical blank.
`full_visibility` restores the selected mixed graphics profile for gameplay:
160 graphics rows and four bottom text rows, using DHGR/80 columns or
[HGR monochrome/40 columns](hgr-mono.md), with double buffering in both.

The merchant's funds line formats current 16-bit gold every frame. Buying a
torch changes visible 500 to 310; buying a rope changes it to 200. Prices and
the purchase transaction retain their source-backed behavior. B2 3005–3015's
exterior choices are spaced vertically, with a greeting built from the player's
name. B2 13000–13040's merchant offers have aligned prices and the eau de
Jouvence description. Success/insufficient-funds messages follow 13500–13510.

## Text introduction and modal help

[text_panels.py](../tools/text_panels.py) reads quoted literals directly from
the pinned BASIC records. The narrative follows **B1 1620–1687**: arrival at the
castle, the legend and the three values Fortune, Sagesse and Puissance. It
appears between the graphical title and name entry. Any key continues;
H or ? opens help while retaining the introduction as the return screen.
Whitespace is reflowed to 36 columns; the source's mixed ASCII case is retained.
The historical spelling `Wesphalie` is retained.

The help page takes its commands and object names from **B1 1515–1570**. Its
24-row Apple layout uses two columns for the six held-item choices. The Apple
commands **T** (light a torch) and **H / ?** (help) are added. These pages use
native 40-column TEXT and the Apple character ROM in an emulator or on hardware.
The host preview uses its documented development font, including punctuation.

Calling help during gameplay is a **new target interface**, not a claim that
the original B2 game provided that hotkey. [game/ui.s](../src/game/ui.s),
`full_ui_key`, intercepts help before controller ticks, pit recovery or staged
actions. `help_return_mode` retains the previous panel; closing keys are consumed,
including R and movement/action keys. The controller tick, actor/action/enemy
state, PRNG, strength and torch lifetime stay unchanged. `ui_skip_clock` also
suppresses the service pass on the closing iteration. H remains a literal
character in name entry; ? opens help there. The next ordinary gameplay
iteration resumes the saved action.

The renderer in [full-panels.inc](../src/apple/full-panels.inc) clears and writes
only the hidden MAIN text page, reading shared AUX scripts through the existing
zero-page bank worker. Each script is a sequence of row, column and a terminated
string, ending with `$FF`. Names, funds and purchase results are inserted at
runtime. It returns through the existing page flip and mode selection; DHGR
terrain and frame buffers are retained.

| Allocation | Role |
| --- | --- |
| AUX `$1400–$1FFF` | Bounded 3 KiB `TEXTASSETS` allocation; 2,768 used bytes including inventory, checkpoint, end screens and hidden test menus; the map has a graphic footer |
| MAIN `$13C0–$1DFF` | LOWCODE including map UI; a physically separate bank |
| MAIN `$0F2C` | Text-script column scratch |
| MAIN `$133E/$133F` | Help return mode / closing-tick service suppression |
| Disk physical sectors 224–233 | Ten padded sectors, preloaded after the shared atlas; no menu-time disk access |

The linker bounds the text segment, the builder checks its size and records its
hash, and startup reuses the existing Disk II loader to fill AUX `$1400`.
`text-panels.json` preserves source line numbers, packet offsets and formatted
rows. No Oric source or validated guideline is changed.

Native tests cover text preload, introduction progression, named exterior,
merchant purchases/denial, paused walking/jumping, darkness, pit recovery, ten
modal return modes, name input and absence of visible-page writes. The generated
`introduction.png`, `exterior.png`, `merchant.png` and `help.png` are functional
CPU previews. This revision has not been relaunched in Virtual II.

## Compact gameplay HUD

The native world build uses these four mixed-mode text rows:

```text
Vous etes dans une salle
au rez-de-chaussee.
Force:  99%    Points:     0
Pieces d'or:   500  Main:
```

The first two rows replace the source's top-of-HIRES description; the last two
retain only the statistics from B2 **5700–5710**. This is an Apple layout
adaptation requested after comparison with the original Oric screenshot.
There are no room numbers, actor coordinates or control reminders. Item names
replace numeric hand codes; an empty hand is blank, following source `BR$`.
Help and the README retain the controls. The inventory now uses the dedicated
layout below; other full-screen panels retain their existing spacing.

[game_resources.py](../tools/game_resources.py), `hud_strings`, exports the
original backslash-terminated B2 strings directly from these addresses, including
their original letter case; historical inputs remain unchanged.

| Role | B2 address | Selection, BASIC lines 4150–4170 |
| --- | --- | --- |
| Shared prefix | `$5A00` | `Vous etes ` |
| Sacred crypt | `$5A0B` | Room 1, before all other checks |
| Dungeon | `$5A22` | Rooms 62 or 33 |
| Dungeon summit | `$5A32` | Room 63 |
| Corridor / room / passage | `$5A47` / `$5A58` / `$5A67` | Geometry 0 / 1 / 3 |
| Catacombs / first floor / ground floor | `$5A78` / `$5A8D` / `$5A9F` | Room < 9 / > 57 / otherwise |
| Oubliette | `$5AB3` | `in_pit`, after room 1 and before dungeon overrides |

[full-description.inc](../src/apple/full-description.inc),
`full_room_description`, reproduces the source priority. Special descriptions
fit on the first row, leaving the second blank. Ordinary descriptions use the
geometry on row 1 and the room-number band on row 2. B2 has **no geometry-2
phrase**: the port retains the prefix alone for that case rather than inventing
one. In the pinned world, all four geometry-2 rooms (1, 33, 62, 63) have special
descriptions, so none display an incomplete generic description. The all-room
tests cover these overrides.

Hand labels follow B2 **11010, 11120, 11220, 11320, 11420, 11520**:
empty, `Torche`, `Clef en fer`, `Clef en or`, `Une fiole`, `Pied de biche`.
Force still uses the integer part of the port's signed hundredths, with
negative values displayed as zero. Points and gold retain the existing unsigned
16-bit state. Gameplay numbers are right-aligned without zero padding;
merchant formatting is unchanged.

The compact 40-character rows use the DHGR 80-column MAIN/AUX interleave,
with the right-hand 40 columns cleared. HGR writes these rows directly to
40-column MAIN text. Every row is
rebuilt on the hidden text page before the existing page flip. The two added
native CPU tests exercise all 64 room descriptions, pit/special-room priority,
both pages, all six hand labels, changing string lengths, numeric boundary
values and absence of visible-page text writes. `build/game/room12-hud.png`
is an executed functional-harness preview, not a new Virtual II capture or
physical-hardware verification.

## Impossible-action feedback

Both full-game editions display **Impossible in inverse video** at the right
edge of the first text row when a requested action is refused. The ten letters
occupy zero-based columns **70–79 in DHGR**, or **30–39 in HGR/full-screen TEXT**.
Ordinary descriptions keep both lines. In the 40-column layout, special-room
and oubliette descriptions retain `Vous etes` on row 1 and move the complete
remaining phrase onto row 2 while feedback is active. This prevents long
descriptions from overlapping the message; both statistics rows remain visible.

[full-core.s](../src/game/full-core.s), `full_denied`, already records the refusal
as `message_id=1` and event 7. This covers failed pickup, opening, reading,
drinking, climbing, invalid jumps and unavailable held-item selections.
`full_dispatch` now clears the previous message on the next ordinary gameplay
key, before processing it; idle frames (`raw_key=$FF`) preserve it. A successful
room transition or castle entry also clears it. Help and the test menu pause
the underlying feedback along with gameplay. Ordinary wall collisions still use
their separate blocked-movement event.

The explicit **T** request now calls `full_request_light` in
[ui.s](../src/game/ui.s), which converts a failed lighting attempt into a denial.
The automatic lighting probe during a vertical jump still calls `full_light`
directly: absence of a reachable fixture during that animation is harmless.
Successful lighting replaces the denial state. The merchant uses the same
wording with its reason: **Impossible: pas assez d'or !**; funds stay visible.

[full-display.s](../src/apple/full-display.s) writes the 40-column message after
clearing the hidden page. In DHGR graphics, [feedback.s](../src/apple/feedback.s)
writes it after the compact HUD's MAIN/AUX interleave, into the last five byte
columns of each bank. Video initialization now enables ALTCHAR at `$C00F`.
The message is encoded as `$09` for inverse uppercase I followed by ASCII
`mpossible` in the inverse-lowercase range `$60–$7F`; it avoids MouseText and
flashing codes. Both page buffers are rebuilt
from current state, preventing alternating text, stale inversions or leftover
letters. The functional preview also decodes these inverse codes using its
development font. This interface policy does not claim to reproduce the original
message duration.

Rebuild both disks and run the focused native CPU regressions:

```sh
make games
python3 tools/check_game.py --video dhgr --suite interactions
python3 tools/check_game.py --video mono --suite interactions
```

Each profile runs fourteen tests: keyboard refusals and persistence across both
pages, clearing on the next command, inverse character bytes and right-edge
placement, special-room/pit/darkness display, explicit and automatic lighting,
all description choices, numeric HUD boundaries, purchases, help pause, hidden
room transitions, startup code relocation, all 64 scene/grid constructions,
all stored direction links, and secret-fireplace opening/traversal guards.
These are py65 execution checks using Disk II BOOT0 in the functional Apple bus;
they do not establish Virtual II, system-ROM cold-start or physical-hardware
behavior. `action-impossible.png` in each build directory is a functional preview.

The [interaction verification record](interaction-verification.json) pins these
executions and their binaries. `--suite interactions` writes a separate
`interactions-test-results.json`; the earlier [feedback record](action-feedback-verification.json)
retains evidence for the previous second-line presentation. `--suite feedback`
still runs nine HUD/UI-focused tests. Neither focused selection reruns every
map or quest scenario; earlier full-suite records retain their program hashes.
`make test-game` and `make test-game-mono` still run the complete suites,
including these new tests.

## Inventory and lowercase text

The inventory is a target presentation change shared by HGR mono and DHGR.
It uses the AUX script renderer and 40-column full-screen TEXT with a blank
row between entries. Zero-based rows 1/3 show the title and held item;
rows 5–13 group provisions and equipment in two columns; rows 15–19 show
quest progress. Rows 22–23 explain return and help. Static labels are compiled
by [text_panels.py](../tools/text_panels.py); `full_inventory_panel` in
[full-panels.inc](../src/apple/full-panels.inc) inserts the live values.

| Display | State interpretation |
| --- | --- |
| Fioles, torches, cordes, pieds de biche | Four unsigned byte quantities, right-aligned in three columns, including 0 and 255 |
| Clef en fer, clef en or, bague, aigle (plomb) | `possessions` bits 0–3; `oui` when set, `non` otherwise |
| Livre, diamant, aigle d'or | `objectives` bits 0–2 have inverted polarity; `oui` when cleared |
| Parchemins | Population count of the three low `scrolls` bits, shown as 0/3 through 3/3 |
| En main | Shared HUD item name, or explicit `Vide` |

The panel is read-only. Space, Return and Escape resume gameplay; 0–5 remain
gameplay item-selection keys. H/? returns to this same inventory after help.
Inventory pauses energy, item wear and enemy services, as before; the general
controller tick still increments. Each page is cleared and rebuilt while hidden,
so changing from a long held-item name or a three-digit count cannot leave stale
letters. This reuses MAIN `$0F2C` as a loop index after the AUX script has finished;
it adds no state allocation and performs no disk access when opened.

The original intro, descriptions and clue exports now retain source letter case.
New interface labels use sentence case, with command letters identifiable in
help. Names preserve input case; keyboard commands are still normalized for
dispatch. The source graphics and title bitmap are untouched. Map captions use
a separate target 5×7 mixed-case raster font in the full-screen HGR map;
Apple TEXT uses the character ROM.
The portable ASCII wording omits French accents to avoid depending on a national
character-ROM variant.

Normal lowercase is written with bit 7 set (`$E0–$FF`). ALTCHAR also provides
inverse lowercase at `$60–$7F`, used only for `Impossible`. The first capital is
in `$00–$1F`, avoiding the `$40–$5F` alternate range that became MouseText on
enhanced machines. See Apple's [IIe Reference Manual, primary/alternate character
set tables](https://www.applelogic.org/files/AIIEREF.pdf) and
[Mouse Technical Note 6](https://mirrors.apple2.org.za/apple.cabi.net/FAQs.and.INFO/A2.TECH.NOTES.ETC/A2.CLASSIC.TNTS/mouse006.html).
No 65C02 instruction or system-ROM call is required. W06 video initialization
retains its previous character-set choice.

The host preview's 5×7 font now includes lowercase and uses the bus's ALTCHAR
state to render inverse cells. It remains a development font, not a reproduction
of the Apple video ROM or a Virtual II screenshot.

```sh
make games
python3 tools/check_game.py --video dhgr --suite presentation
python3 tools/check_game.py --video mono --suite presentation
```

This focused suite covers both inventory buffers, empty/full/partial possessions,
all objective-bit polarities, quantity boundaries, scroll counts, help/return,
mixed-case names, normal/inverse screen codes, descriptions for all room numbers,
HUD statistics, merchant purchases, clues, introduction and map/menu transitions.
See [presentation verification](presentation-verification.json) for the executed
results and matching artifact hashes. Earlier interaction/full-suite records
retain their original hashes and do not certify these new binaries.

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
the lower title/credits. Enter or Space advances to the introduction. Original WAIT,
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
scopes. The 2026-10-18 HUD revision was executed in the functional CPU harness;
Virtual II observations refer to the earlier program hashes recorded there.
The pit sequence was tested in the functional CPU harness; no complete
playthrough to room 23 in Virtual II is claimed. Audio, original ending
presentation and entire-game replay remain open.
