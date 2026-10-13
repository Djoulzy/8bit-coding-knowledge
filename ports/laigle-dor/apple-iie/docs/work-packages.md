# Port delivery boundaries

Contract: [portage.md §6.2](../../../../research/analyses/laigle-dor/portage.md#62-ordered-work-packages-and-completion-gates).
The first interactive milestone is implemented. Full original-game gates remain
pending where the source configuration or source runtime evidence is absent.

Update, 2026-10-13: the user supplied Oric-1 BASIC 1.0 and Apple IIe enhanced
system ROM images. Their identities are pinned in
[rom-profile.json](../resources/rom-profile.json). The separate native-world
build uses the actual 64-byte Oric `$D000–$D03F` table. Original Oric execution,
final font capture, PRNG/timer traces and physical hardware certification remain
pending. Earlier W06 results below retain their original provisional inputs.

W07 now has an executed generic-room constructor and semantic grids for all
64 records. It uses four shared wall programs, parameterized openings and a
shared atlas; it contains no per-room bitmap archive. Source-derived rule/action
code is in development and has selected executed tests. This does **not** close
the complete M02–M24 gate. W08 presentation and audio, W09 performance and W10
full replay remain unfinished. See [native construction](world-construction.md).

The [presentation/pit follow-up](presentation-and-pits.md) adds the dedicated
oubliette scene and recovery/rope regression, full-screen TEXT panels, visible
merchant funds, and the original B1 title with lightning. Enhanced firmware
cold boot and title/merchant/room-12 presentation were observed in Virtual II.
These checks do not certify every action path or complete W08.

The [movement/scenery follow-up](movement-and-scenery.md) halves native walking
increments and narrows foot/proximity checks while retaining world coordinates.
It synchronizes pickup reach and door/arrival planes, restores original flame
frames on both buffers, and provides explicit native grille/lock and secret-cue
art. Twenty native checks and the unchanged 44-check graphics regression
passed. These target adaptations are distinct from source runtime equivalence.

The [room-transition follow-up](room-transitions.md) retains the visible room
during construction, initializes each frame pair only while hidden, and builds
a clean source-inspired darkness panel. It replaces the temporary TEXT screen
used to conceal simultaneous frame initialization. Early neighbor prediction
is not part of this synchronous preparation protocol.

| Package | Delivered | Gate / remaining work |
| --- | --- | --- |
| W00 | Pinned TAP/payload identity; target/dependency profile; executed Apple BOOT0/loader and HGR captures; optional Oric-ROM input with checksum | **Partially blocked:** no authoritative Oric ROM/model, `$D000–$D03F` capture, source screenshots or input/timer/RNG trace. Zero variation is provisional. Apple physical configuration/cold boot not certified |
| W01 | Source-to-port map below, retained W06 grammar/ID census, new Apple callable ABI, linker ownership and source line/address links | Complete for retained W06 paths; original complete inventory remains in research. Full transitive gameplay/stream reachability and remnant interpretation need later work |
| W02 | Deterministic initial-world export, title, captured font, six text groups including M2, raw pointer tables, 23 selected live atlas IDs, 16 actor phases, room-12 operations/grid/HGR, manifest with offsets and hashes | W06 resources checked. Full-game live-resource/stream census and ROM-adjusted fonts unverified; raw unused pointer-table words are not valid streams |
| W03 | Independent world/movement oracle; tagged rational RNG input; ordinary pickup, economy, lock/wear, completed potion, pit, quest/reset/victory predicates; executed predicate tests | **Partial:** no original runtime equivalence, Oric float/PRNG/timer emulator or complete BASIC action graph; staged/chest/enemy/climb/history mechanics pending. Differences are explicit in compatibility ledger |
| W04 | Local checksum-pinned ca65/ld65/py65 chain; actual assembler version log; native map; slot-6 Disk II contract, main-bank takeover/scratch/stack ABI | Execution in functional CPU harness passed. Full Apple emulator and hardware boot/drive/IRQ/NMI confirmation pending |
| W05 | Source-backed room-12 geometry/decor and original actor layers; neutral source image; cleared-header crop to 160-row HGR; native silhouette masks with Oric attribute cells transparent | CPU output matches pixel oracle on both frame pages; 460 sprite cases cover phases and upper/lower/right clipping. Oric runtime scene comparison blocked by W00 |
| W06 | Native boot images, animated actor, directional keyboard/aliases, no-key walk continuation, stop/crouch, collisions, bounded portal event, silent RAM event log; reproducible build/test/headless/local launch | **Milestone delivered under functional target model.** Full emulator/physical boot and faithful source timing remain unverified. W07 will consume room-transition requests |

## Symbolic source-to-port map

Original full inventory: [routines.md](../../../../research/analyses/laigle-dor/routines.md).
No original routine is linked verbatim into the Apple binary; fixed-address
workers have been rewritten or replaced with generated resources.

| Original source / consumers | New module and interface | Retained contract / excluded behavior |
| --- | --- | --- |
| `$4DDD–$4DFD`, B2 1/40/4010/4200 | `game_reset`, `model/world.py`, `model/rules.py` | Initial snapshot is `$5600–$57FF`, not captured live `$5000`; W06 starts x19/y140/facing0/empty hand |
| `$3F14–$3FF1`, B2 100/607 | `Room.decode`, `tools/resources.py` | 64 packed slots; geometry/features/light and three stored links; no four-neighbor assumption |
| B2 100/300/390/600–699, 720–725, 780/782 | `mono_room12` / `room12-operations.json` | Checked room-12 branches; vector rasterization, paper/color conversion and M=0 remain stated adaptations |
| `$3E18–$3E51`, `$3EBD`, `$3EF8` | Asset exporter and `draw_sprite` | Distinguish ROM cursor byte anchor from actor-byte anchor; seven-pixel packing replaces source six-pixel pixels |
| `$4500–$45A9`, `$4200`, B2 6/7/4910/5020 | `motion` / generated frame records / `game_tick` | Pre-increment cursor skips prefix; restore/delta/draw/yield grammar for IDs 0–11; delay/chain not silently implemented |
| `$45AA–$45FB`, `$4400`, B2 7 | Generated empty-hand equipment layers | IDs 0–3, crouch adds source dy10; no other equipment/action grammar claimed |
| `$3E52/$3E78`, saved F3/F4/F5 metadata | `draw_scene` / `draw_sprite` | Per-page dirty repair from `$A000`, ordered native pixel/mask layers and hidden-page rendering replace original saved buffers/patches |
| `$4B75–$4CDC`, B2 4800/4810/4900 | `collision_probe` / `model/movement.py` | Bounded 3×40 semantic grid, source perspective rows, left/right/far door statuses; no source hardware read from out-of-grid probes |
| B2 5030/5050/10000–10510, key table `$4300` | `keyboard_poll`, `game_tick`, `Actor.tick` | Turn-before-walk, directional key stops active walk, space stands, A crouches, no-key continues; unsupported bindings ignored |
| B2 97/5100/10000 | `log_event`, audio catalog | Captured native SOUND/PLAY parameters for walk/stop; no AY/speaker driver or source timing claim |
| B2 4702/4920, room 12 right link | `EVENT_EXIT` | Stop at portal and publish request; actual transition to room 11 deferred to W07 |

## Acceptance mapping

- A01: existing historical identity verification rerun; project resource equality
  tests passed. W00 ROM identity and Oric execution remain missing.
- A03/A04: W06 control trace and 360 bounded collision cases passed against the
  independent proposed controller. Source mid-phase input order differs explicitly.
- A05: room-12 stored-link decode tested; executing room changes is outside W06.
- A06: blocked by missing reference ROM; default zero table is labeled in manifest.
- A07/A08/A13–A16/A23: selected isolated source expressions are covered by host
  tests, not completed historical action sequences or target gameplay.
- A19: 23 live sprites × ten phase/edge setups × two pages = 460 CPU
  comparisons; startup/control frames compared. Full-game overlap/IDs pending.
- Display follow-up: 60 alternating-page frames preserve the visible image/text
  while drawing, repair both histories correctly and flip at fresh vertical blank
  in the functional NTSC clock model. Native text pages and attribute independence
  are tested; no physical refresh-rate/tear-free claim yet.
- A20: selected bounded phases extracted; complete chained/delay/action grammar
  intentionally not claimed.
- A21: zero speaker accesses and event ring verified; no acoustic/pace benchmark.
- A22: actual BOOT0 payload reconstruction, main-bank initialization flags,
  application ownership and event/tick wrap passed under the functional model.
  No reset-vector, drive error or real-hardware claim.
- A24: deterministic output hashes, invalid resources/oversize images and unknown
  key policy covered. Full W10 fresh hardware replay remains future work.

## Next inputs and operations

1. Supply/pin an Oric ROM/model and capture room 12, character states, cursor
   anchors, `$D000–$D03F`, ROM-adjusted fonts and input/RNG/timer trace.
2. Boot `.do` or `.nib` in an identified full Apple IIe emulator, then physical
   hardware; record CPU/ROM/RAM/video/controller hashes and setup.
3. Resolve the documented raster, paper, input-phase and pace differences before
   W07 extends the current pure state/resource/Apple interface boundaries.
4. Consume `EVENT_EXIT`, build all rooms from persistent world state, then bring
   equipment/traps/enemies/actions into both the oracle and the target together.
