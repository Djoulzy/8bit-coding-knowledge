# Input responsiveness: diagnosis and optimization

## Optimized full-game builds

The [renderer changes](renderer-optimization.md) are implemented in both full
editions. The comparison below executes the same thirteen-scenario input script
against the archived original binaries and the rebuilt binaries. Times are
cycle-derived estimates at exactly 1 MHz, not Virtual II measurements.

| Scenario | DHGR before → after | Mono before → after |
| --- | ---: | ---: |
| Warm stationary loop in room 12, first sample | 289.516 → 85.134 ms | 306.546 → 51.108 ms |
| Turn command arriving just after an idle poll, to next affected flip | 595.931 → 340.435 ms | 647.024 → 204.201 ms |
| Turn right, already pending at poll, to flip | 272.391 → 221.215 ms | 289.424 → 136.094 ms |
| Stop arriving just after a walking poll, to flip | 544.840 → 459.640 ms | 595.928 → 272.340 ms |

The idle loop is about **3.4× faster in DHGR and 6.0× in mono**. The sampled
late idle command reaches the display about **43% / 68% sooner**. Moving frames
benefit less from the cache, especially in DHGR. These are individual matched
scenarios, not universal worst-case latency guarantees.

Current [DHGR](../build/game/input-profile.json) and
[mono](../build/game-mono/input-profile.json) reports include program/disk
hashes, routine cycle counts and state transitions. The matched baseline reports
are [DHGR](../build/latency-baseline/dhgr/input-profile.json) and
[mono](../build/latency-baseline/mono/input-profile.json). To rerun an archived
build, pass `--directory build/latency-baseline/dhgr` or `.../mono` to the same
profiler. All these directories contain their own disk and linker labels.

Strength drain and torch wear now use 18 observed refreshes per service rather
than one decrement per rendered frame. Walking, staged actions, enemy/hazard
logic and flame animation remain controller-loop based and can run faster.
See the renderer document for memory allocations, cache exclusions, clock
scope and validation commands.

## Original diagnosis and reproduction

The original diagnostic pass profiled both editions without changing target
instructions. Its twelve-scenario evidence is preserved separately below.
The profiler remains read-only with respect to game binaries and disk images.

From the port directory, with both full builds already available:

```sh
python3 tools/profile_input.py --video dhgr
python3 tools/profile_input.py --video mono
```

The profiler executes the supplied Disk II BOOT0 and the native program under
py65, enters room 12 normally, then warms both terrain buffers. It records
instruction cycles, keyboard consumption and page flips. The initial twelve
scenarios are archived with program and disk SHA-256 hashes:

- [Original DHGR report](../build/latency-baseline/dhgr/input-profile-original.json)
- [Original HGR mono report](../build/latency-baseline/mono/input-profile-original.json)
- [Profiler](../tools/profile_input.py)

Counts include executed branch/page-crossing costs as modeled by py65. VBL uses
the existing simplified NTSC phase model. Milliseconds below are **estimates at
exactly 1 MHz**, obtained by dividing cycles by 1,000. They are not measurements
of Virtual II, a physical Apple IIe, host keyboard delay or monitor scanout.
Disk/room-construction latency is outside these steady-room scenarios.

## Original results

| Executed scenario | DHGR cycles | HGR mono cycles | Meaning |
| --- | ---: | ---: | --- |
| Room 12 idle loop, first warm sample | 289,516 | 306,546 | About 290 / 307 ms between keyboard polls |
| Turn right: key pending at loop entry to page flip | 272,396 | 289,424 | About 272 / 289 ms before the new image is submitted |
| Start walking right: key pending at loop entry to page flip | 289,416 | 306,458 | About 289 / 306 ms |
| Stop: key arrives just after polling, to consumption | 272,480 | 306,537 | The first loop cannot see this key |
| Same stop: key arrival to following page flip | 544,837 | 595,935 | About 545 / 596 ms before the stopped pose is submitted |
| Inventory idle loop | 68,115 | 51,082 | Menus are faster but still rebuilt each loop |

Four consecutive stationary room-12 loops measure 289,502–289,518 cycles in
DHGR and 306,534–306,546 in mono. These are sampled results, not universal
latency bounds: pose, equipment, enemies, room changes and input phase matter.

In the first stationary sample, `draw_scene` consumes 280,528 cycles in DHGR
and 300,264 in mono, approximately 97% and 98% of the full loop. The native
game-rule update consumes 367 cycles in that sample. For the turn command,
keyboard polling consumes 92 cycles and `game_tick` consumes 387 cycles in
both editions. Command decoding is therefore a minor part of this delay.

Inside the stationary render, actor `draw_sprite` calls total 169,560 / 206,489
cycles; wall torches consume another 57,233 / 70,481 cycles. The renderer also
restores old actor backgrounds and rewrites the HUD. Reported routine times
are **inclusive**: equipment drawing includes some actor sprite calls, and
`draw_scene` includes all of these operations. Do not add nested totals.

The profiler verifies the intended turn/walk/stop/crouch/menu outcomes and
checks that no graphics or mixed-text writes affect the visible page. This is
a targeted diagnostic execution, not a rerun of the complete regression suite.

## Causes identified before optimization

1. [`main_loop`](../src/full-main.s) calls `keyboard_poll` once, then
   `game_tick`, `full_clock`, any required room construction, `draw_scene`, and
   `present_frame`. The next keyboard poll occurs only after all of that work.
2. [`keyboard_poll`](../src/apple/input.s) consumes `$C000`/`$C010` directly.
   The application has no input queue or polling during drawing. The functional
   profiler injects one late key; it does not simulate typematic overwrites or
   establish which events Virtual II may retain when several keys arrive.
3. [`draw_scene` / `draw_sprite`](../src/apple/dhgr.s) rebuild the hidden frame's
   actor even when stationary, decoding resource data through AUX reads and a
   general masked-cell renderer. Mono uses one source dot per output bit;
   DHGR uses paired source-dot cells. Consequently mono is not automatically
   faster despite its simpler video writes. Both currently pay the cost of a
   general sprite decoder rather than a prepacked byte blitter.
4. [`full_draw_torches`](../src/apple/torches.s) restores and draws the flame
   sprites each loop. The full HUD is also formatted and written each time.
5. Double buffering hides construction and avoids visible writes. It does not
   execute the CPU's drawing and keyboard code concurrently. The VBL wait is
   a small part of the sampled delay, not its main source.

There are also **control semantics distinct from rendering latency**:

- [`game_tick`](../src/game/core.s) turns on the first direction command and
  starts walking when already facing that direction. While walking, a direction
  command first stops the actor. Held-key repeats can therefore alternate walking
  and stopping; key release does not stop automatic walking.
- [`full_dispatch`](../src/game/full-core.s) advances an active staged action
  before ordinary movement/item commands. Some keys received during a jump,
  drink or climb are consumed without being deferred. Modal help/test/checkpoint
  routing precedes this path in [`full_ui_key`](../src/game/ui.s).

## Original optimization plan and remaining work

The original plan was to prioritize the renderer, then input scheduling. The
first two items are now implemented within the conservative scope described
above; the fourth is implemented for periodic strength drain and torch wear.
Input queuing and fully independent simulation scheduling remain future work:

1. Replace per-cell actor composition with byte-oriented masked blits and
   precomputed horizontal phases where the resource/memory budget permits.
   Use a dedicated mono path and keep DHGR MAIN/AUX packing correct.
2. Cache composition state **per display page**. Skip unchanged actor/HUD work
   only when that hidden page already contains the required result. Track
   overlap with flames, equipment and enemies; never let a cached sprite erase
   a newer foreground element or survive a terrain change.
3. Poll into a small pending-input buffer during bounded rendering work, then
   dispatch at defined game-state boundaries. This can retain commands but does
   not by itself remove the cost of composing the visible response. Define
   repeat, overflow, modal-close and staged-action policies explicitly.
4. Separate elapsed gameplay time from rendering iterations. Currently energy,
   wear, walking and effects advance per loop; speeding up the renderer alone
   also speeds those systems up. Establish a measured target cadence before
   changing their scheduling.

Any renderer replacement should retain pixel equivalence tests in both banks,
hidden-page write checks, overlap/room-transition tests, and checkpoint/menu
regressions. Recheck input-to-display latency in Virtual II at standard speed;
the functional CPU counts do not establish physical video timing.
