# Native renderer optimization

This implementation reduces the cost identified by the
[input-responsiveness diagnosis](input-responsiveness.md). Historical inputs,
approved artwork, collision geometry, two display pages, mixed text and keyboard
command meanings are retained. The target remains documented NMOS 6502.

## Byte-oriented sprites

[`native_sprites.py`](../tools/native_sprites.py) compiles opacity and color into
seven-bit mask/pixel fragments. Identical scanlines share one immutable AUX
record. The 16-byte sprite header retains the existing dimensions and seven
horizontal extents; format byte 10 is 2, byte 13 is the unshifted row width in
bytes. The following stream has one little-endian AUX row pointer per source
scanline. Each row contains interleaved mask, pixel pairs, with color restricted
to the opacity mask.

All mono actors use this representation. DHGR uses it for actor IDs 40–61 and
both wall/hand flame pairs (36/37, 72/73); the remaining equipment, action and
enemy sprites retain the compact cell decoder to fit the available AUX memory.
All other scenery retains its existing shared atlas. No per-room bitmap or
pre-rendered room variant is introduced.

[`draw_native_sprite`](../src/apple/native-sprites.s) prepares a 128-byte
seven-bit rotation table for the horizontal phase. Advancing by `1 << phase`
with end-around carry modulo 127 generates all rotations, including the distinct
all-one value. Masks split the rotated byte into its current-byte contribution
and carry into the next byte. Source rows are copied from AUX into a small MAIN
buffer before composition, using a worker in unbanked zero page. This removes
per-cell decoding and repeated bank switches for individual resource bytes.

The blitter preserves the existing dynamic row-composition order and the static
flames' last-source-row sampling. It handles top/bottom clipping and the right
viewport edge. Fast flames are used by the existing non-additive wall/hand
rendering paths; unrelated additive scenery keeps the general renderer.

[`repair_rectangle`](../src/apple/dhgr.s) now copies contiguous MAIN and AUX
spans separately. In DHGR, odd serial-byte indices are MAIN, even indices AUX:
MAIN bounds use floor(left/2), floor(right/2), while AUX bounds use the ceiling.
The AUX copy loop executes entirely in MAIN zero page with ALTZP off, then
restores MAIN reads and writes. Empty spans are skipped.

## Per-page actor reuse

[`actor_cache`](../src/apple/actor-cache.s) retains four keys per page: x, y,
facing and frame. Reuse is deliberately restricted to a stationary,
empty-handed actor in the central region, with no staged action, enemy, hazard
or pit. The horizontal guard excludes overlap with wall flames. Darkness, dirty
terrain, invalid background history and changes in those keys force normal
composition. The preserved page keeps its dirty bounds for the next actual
movement. Flame and HUD updates continue normally.

This improves polling while the player is deciding what to do. It does not make
all frames cost the same: movement, equipment, enemies, room construction and
returning from a modal page still require composition. There is no new input
queue; staged-action command handling retains its existing semantics.

## Strength and torch lifetime

[`service-clock.s`](../src/apple/service-clock.s) samples IIe RDVBLBAR at bounded
points in sprite drawing, background repair, HUD formatting and presentation.
Ordinary strength drain and held-torch wear advance every **18 observed video
refreshes**, approximately 300 ms at 60 Hz, close to the earlier warm-room loop.
Menus/help clear accumulated time, and room construction resets the clock.
Collision, trap and command processing remain immediate.

This is an explicit target cadence, not reconstructed Oric timing. Walking,
staged animation, enemy/hazard logic and flame phase still advance with the
controller/render loop and can run faster as drawing becomes cheaper. A fully
fixed-rate simulation remains future work. On a different video refresh rate,
the 18-refresh interval has a different duration; an accelerator does not change
the count of physical refreshes. The counter bounds pending time to prevent an
unbounded catch-up after a long unsampled operation.

## Memory ownership

| Region | Purpose |
| --- | --- |
| MAIN `$0040` through the exported AUX-worker size, below `$0080` | AUX read, row transfer and span-copy workers; reinstalled after each BOOT0 read |
| MAIN `$0200–$027F` | Rotation table rebuilt for each native sprite |
| MAIN `$0280–$02FF` | Row scratch; maximum 128 bytes, checked by the compiler |
| MAIN `$0300–$03D5` | BOOT0 decode workspace and GCR table; the new scratch does not overwrite them |
| MAIN `$1340–$1347` | Per-page actor-cache keys |
| MAIN `$1348–$1349` | Wear-clock refresh count and previous VBL state |
| AUX `$0400–$0BFF` | Both text pages, **excluded from resource allocation** |
| AUX `$0C00–$13FF` | 2,048 bytes of shared DHGR native rows; disk sectors 336–343 |
| AUX `$1400–$1FFF` | Text scripts (2,768 bytes used) |
| AUX `$6000…` | Main shared atlas: 15,690 bytes DHGR, 22,828 bytes mono |

MAIN and AUX low memory have different owners. The native row transfer writes
MAIN scratch while reading AUX; the retained row atlas is never used as a
destination. The full builds still require 128 KiB. The final end screens use
the existing AUX text-script engine to release padded MAIN strings. Unused raw
clue copies and unused atlas pointer slots are removed from the resident image;
displayed clue content is unchanged.

## Validation and remaining work

Rebuild and run from the port directory:

```sh
make games
python3 tools/check_game.py --video dhgr
python3 tools/check_game.py --video mono
python3 tools/profile_input.py --video dhgr
python3 tools/profile_input.py --video mono
```

New tests compare all 60 actors at all seven horizontal phases against the
independent source/status interpreters. Existing edge clipping, flame, room,
equipment and page-write checks remain. Cache tests compare reused pages with
forced recomposition and verify that text drawing cannot corrupt the AUX row
pool. A timed integration test compares actual refresh crossings in the
functional model with strength loss, torch wear and the remaining clock count;
help must pause both resources.

Results and hashes are recorded in the full-game test reports and the linked
input profiles. Execution uses py65 and the functional Apple bus, including real
Disk II BOOT0 instructions; this is not a new Virtual II or physical-machine
timing measurement. Future work can address pre-shifted/composed actor data,
HUD caching and input buffering, with explicit memory and action policies.

The final binaries passed **45 full-suite DHGR tests and 46 mono tests**, plus
three supplemental tests per edition for end screens, cache/darkness and the
wear clock. Those supplemental runs include assertions added after the full
suites were collected. Together the runs cover 64 room constructors per edition
and 420 actor/phase compositions per edition. The matching thirteen profiling
scenarios were also executed against both archived and final builds. See the
[consolidated evidence and hashes](renderer-verification.json),
[DHGR suite](../build/game/game-test-results.json),
[mono suite](../build/game-mono/game-test-results.json),
[DHGR supplemental checks](../build/game/render-focused-test-results.json) and
[mono supplemental checks](../build/game-mono/render-focused-test-results.json).
