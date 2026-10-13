---
id: PORT-LAIGLE-DOR-HIDDEN-ROOM-TRANSITIONS
program: "L'Aigle d'Or"
cpu: ["6502"]
machines: ["apple-iie"]
analysis_status: draft
analysis_date: "2026-10-13"
---

# Room preparation without a stale TEXT screen

The native world build retains the previous graphics frame while constructing
the next room. It no longer switches to TEXT to conceal writes to both frame
pairs. The packed world and shared atlas remain unchanged; no room bitmap
archive or third frame pair is introduced.

## Ownership and presentation

1. `world_load_scene` constructs MAIN/AUX `$A000–$BFFF`, rebuilds the semantic
   grid and leaves the displayed frame and video mode untouched.
2. It invalidates both frame histories and sets `terrain_pending` to `%11`.
3. `draw_scene` selects the hidden pair. `full_prepare_page` copies the new
   baseline into **only that pair**, then clears its pending bit. Actor, flames,
   other effects and the paired HUD are composed before presentation.
4. The existing fresh-vertical-blank `present_frame` selects the complete frame.
5. On the next iteration the previously visible pair is hidden; it receives
   its full baseline copy before normal drawing. Subsequent iterations use
   ordinary dirty-rectangle restoration.

The two pending bits live in MAIN `$133D`. Copies use the existing bank-safe
`init_page` worker; resident code, zero page and stack remain MAIN. Each pair
contains 8 KiB MAIN and 8 KiB AUX. Only 16 KiB of baseline copying precedes the
first flip, instead of copying 32 KiB under a temporary TEXT screen. Total
initialization of both pairs is still 32 KiB. This is a byte-work statement,
not a frame-rate or hardware loading-time benchmark.

The constructor remains synchronous CPU work. Preparation starts **after the
destination is selected**, with the old frame still displayed. This uses the
double buffer to prepare the next screen; it does not predict a neighbor before
the player chooses a door. An anticipatory cache would additionally need room
selection, mutable-state invalidation and cancellation rules. The current
pipeline also handles a taken object, opened chest, fallen gate and pit scene
as a new terrain generation.

Implementation: [room-builder.s](../src/apple/room-builder.s),
[dhgr.s](../src/apple/dhgr.s),
[full-memory.inc](../src/game/full-memory.inc).
The historical room constructor is B2 100–1110 and the pit constructor is
7030–7046; the staging protocol is new Apple code. See the
[source analysis](../../../../research/analyses/laigle-dor/routines.md).

## Intentional darkness and menus

A second stale-screen path was the source-inspired darkness branch: it selected
TEXT without constructing a fresh panel. `full_is_dark` now supplies one common
predicate to preparation, drawing and mode selection. An unlit room without a
held torch shows a freshly composed **40-column TEXT page** with current HUD
values and **IL FAIT NOIR ICI !**. It retains the source's darkness concept
(B2 6000–6003), with new Apple keyboard help. Exterior and merchant panels keep
their normal TEXT presentation.

During darkness, both terrain bits remain pending. Equipping a torch or another
source-defined visibility exception prepares each hidden graphics pair before
returning to mixed DHGR. A stale partial graphics page cannot become visible.

Implementation: [full-display.s](../src/apple/full-display.s) and
[full-text.s](../src/apple/full-text.s).

## Verification and reproduction

```sh
make game
make test-game
make test VIDEO=dhgr
```

Reload `build/game/laigle-dor.do` in Virtual II, then cold **Boot**. In a lit
room, the last frame remains visible during construction, followed by the new
room and HUD. A genuine dark room shows the dedicated message, rather than a
previous merchant panel.

[world_port.py](../tests/world_port.py) checks that all 64 baseline/grid outputs
still match the source-backed target oracle, that construction preserves the
active frame, and that both pairs initialize only while hidden. It also checks
room 12→11 presentation after a merchant visit, no transitional `$C051` access,
matching completed frame pairs, no visible graphics/text writes, and darkness
TEXT→torch/DHGR recovery. Pit and flame regressions remain in the same suite.
Executed revisions and emulator observations are pinned separately in
[world-verification.json](world-verification.json).
