---
id: PORT-LAIGLE-DOR-GRILLE-DARKNESS
program: "L'Aigle d'Or"
cpu: ["6502"]
machines: ["apple-iie", "oric-1"]
analysis_status: draft
analysis_date: "2026-10-19"
---

# Visible falling grilles and consistent darkness presentation

Original references below are BASIC line numbers in the pinned
[B2 listing](../../../../research/analyses/laigle-dor/extracted/aigledor.2.basic.txt).
Original author: Louis-Marie Rocques, Loriciels 1984. Native timing and display
choices are Apple port adaptations; the original Oric runtime was not executed.

## Why room 36 kills a walking player

The original packed record has geometry 0, light 0, the falling-grille feature,
an unset persistent gate bit, and field 3 below 2. The supplied Oric ROM gives
room 36 variation **207**, so B2 **962** selects the right trap (`HR=2`). B2
**5015–5018** triggers at `XH=27` and distinguishes ordinary walking from the
horizontal jump (`AC=5`, which sets `HT`). B2 **6300** persists the closed gate;
**6310** draws it through **902** before testing `HT=0` and entering the death
routine. There is no y-coordinate or torch exemption in that trigger predicate.
The other initial trap rooms are 4 (left), 7 (right) and 8 (left).

The preceding Apple build reproduced the walking death with positive strength,
but changed to the ending panel in the same controller iteration that set the
gate bit. The renderer therefore never displayed a falling gate. A torch only
makes the room visible; it does not protect against this trap.

## Staged trap resolution

[game/gate.s](../src/game/gate.s) uses `action_kind=5` and the existing
`action_phase` byte. `full_gate_start` sets the persistent gate bit, stops the
player, and begins phase 1 without rebuilding the terrain. Phases **1–9** remain
in gameplay; **8 and 9** show the complete gate on the alternating buffers.
Phase 10 requests the final terrain rebuild, clears the active trap state,
and resolves the result: death for ordinary walking, survival after crossing
the trigger during a horizontal jump. The first segments start above the
35-source-row visible scene boundary and become visible as the gate extends.
This is a controller-frame cadence, not a measurement of original fall timing.

During the fall ordinary commands are consumed and `full_clock` pauses wear,
enemies and moving hazards. Help retains the phase and consumes its closing key.
The existing test/checkpoint panels follow their ordinary staged-action pause
policy. The fall remains graphical even without a held torch, making its cause
visible. Starting the fall records action event 9; a fatal outcome records end
event 10 after the visible sequence.

[apple/gate.s](../src/apple/gate.s) draws the original shared atlas 17/18 through
`scene_gate_bars` in [room-builder.s](../src/apple/room-builder.s). The two
interleaved columns grow down from the ceiling; the final number, spacing and
anchors are the existing closed-gate construction. They are drawn **after the
actor**, so the falling foreground gate can obscure the player. MAIN and AUX
immutable baselines retain the preceding room during the sequence. Each hidden
frame restores the complete affected view before composing the next stage;
`action_kind` excludes actor-cache reuse. Final construction bakes the closed
gate into the baseline and retains its original semantic grid marks. No new
per-room bitmap or replacement sprite is introduced.

## Jump crossing with the smaller walking step

Walking now permits even as well as odd source-byte x coordinates, while the
jump still advances two source bytes per phase. Testing only equality with the
odd trap coordinates 11/27 missed even-position crossings. The preceding port
also lost the trigger when a jump crossed the plane before its final position.

`full_gate_crossing` latches the crossing when the new jump position is either
on the plane or one byte beyond it in the jump direction. `full_clock` waits
until the jump finishes, then resolves that latch independently of the final x.
Jump initialization and completed gate resolution clear the latch. Trajectory,
held-item restoration and the historical lethal-walk rule remain separate from
this target collision adaptation. **S** is the horizontal-jump command.

## Darkness keeps the gameplay HUD

[full-text.s](../src/apple/full-text.s), `full_dark_text_draw`, clears the hidden
TEXT page and renders the ordinary HUD directly at rows **20–23**:

| Zero-based rows | Content |
|---|---|
| 0–19, except 11 | Blank |
| 11 | Centered `Il fait noir ici !` |
| 20–21 | Original room description |
| 22 | Force and points |
| 23 | Gold and held item |

HGR mono uses 40 columns; DHGR uses 80, preserving the lit edition's HUD layout.
Full-screen darkness is still TEXT, with mixed graphics disabled. The ordinary
40-column exterior, merchant and modal pages keep their own layouts. There is
no duplicated title/funds heading or extra keyboard-hint row in darkness.

`full_text_clear` clears MAIN and, in DHGR, AUX text RAM on the hidden page.
This prevents old merchant or 80-column characters from remaining in the empty
area. The darkness message uses the same native lowercase text encoding as
the HUD. DHGR interleaves the centered message into MAIN/AUX characters and
retains outcome feedback at columns 70–79; mono retains columns 30–39.
Special-room description wrapping is needed only in the 40-column edition.
Selecting a torch restores the existing mixed graphics and pending terrain
preparation without exposing an old panel.

## Resident space and reproducible checks

The extra state machine and display workers reuse existing state bytes. To
fit them below the immutable `$A000` baseline, `game_resources.py` stores the
compact fallback clue rows as NUL-terminated strings, rather than forty-byte
padded rows. `full_hud_clue_row` supplies the missing spaces, advances by the
consumed string length, and handles empty or exactly forty-character rows.
The actual AUX-script clue panels retain their text and layout. Linker bounds
continue to protect resident resources, bank workers and relocated code.

From the port directory:

```sh
make games
python3 tools/check_game.py --video mono --suite hazards
python3 tools/check_game.py --video dhgr --suite hazards
```

The selection includes twenty tests per edition: the new native trap and
darkness scenarios, the existing darkness/help cases, and all fourteen feedback
regressions. [room_hazards_cases.py](../tests/room_hazards_cases.py) executes the
reported room-36 torch/walk sequence, nine visible phases, help pause, delayed
death, unchanged baselines, both frame pages, and eight controlled jump approach
positions across the two trap sides. It also checks the bottom HUD and centered
message after an old merchant panel, repeated flips, help and torch selection.
The feedback cases exercise the compact clue fallback after its storage change;
a focused row test checks empty/exactly forty-character input, source page carry
and the guard byte immediately after the destination row.

Reports are `build/game/hazard-test-results.json` and
`build/game-mono/hazard-test-results.json`. Previews in each directory include
`room36-dark-hud.png` and `room36-grille-stage-1.png`, `-4.png`, `-8.png`.
Execution uses py65 with the functional Apple bus and real Disk II BOOT0;
Virtual II, system-ROM cold-start and physical Apple hardware are not tested.
These focused checks are not a complete adventure replay or a performance
benchmark.

On 2026-10-19 all twenty tests passed in each edition. The
[execution snapshot](grille-darkness-verification.json) pins the reports,
program/disk hashes, memory bounds and previews. Existing atlas, title, text
and extra asset hashes match the preceding committed build in both profiles;
the editor artwork file and historical inputs are unchanged.
