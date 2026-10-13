# Verification record — W06 prototype

Executed on 2026-10-13 with Python 3.9.6, cc65 source tag V2.19 and py65 1.2.0.
The machine-readable snapshot is [verification.json](verification.json).
The default profile uses the explicitly provisional 64-zero-byte Oric variation
table. No Oric reference game, full Apple emulator or physical machine was run.

This record describes the original monochrome milestone. The subsequent
[color experiment](color-experiment.md) records the optional color binary and
the 27-test regression run for each profile; its generated evidence is separate.

The later [DHGR experiment](dhgr.md) records the banked implementation and
additional memory/pixel tests separately. Earlier HGR results do not validate
auxiliary-memory mapping or DHGR output.

## Executed target checks

`make test` / `python3 tools/check.py`: **23 tests passed**. These include nine
executed-CPU test groups, six resource/model groups and eight isolated rule
groups. The CPU executes a native, assembled NMOS program; it does not run a
Python rewrite in place of the Apple game. Independent models supply expected
states and pixels, rather than preloading the expected HGR into the CPU.

| Check | Actual result / evidence boundary |
| --- | --- |
| Boot from `$C600` | Stock Disk II BOOT0, actual GCR decoding, project boot sector and all payload tracks executed; loaded bytes equal the assembled application |
| Loader payload | 14,322 application bytes, load `$6000`, page-padded exclusive end `$9800`; no overlap with `$A000` terrain baseline |
| First scene | HGR RAM equals independent room/actor pixel reference; decoded PNG visually inspected |
| Control trace | Turns, two walking phases, empty-key continuation, floor stop, right portal request, crouch/stand and unsupported `>` behavior agree with the **proposed W06** controller |
| Collision | 360 x/y/direction combinations compared against independent bounded map oracle; invalid x rejected |
| Sprite rendering | 23 original atlas IDs × ten phase/edge cases × two pages = 460 comparisons; upper/lower/right clipping, neighbors and page holes preserved |
| Alternating pages | 60 frame constructions leave visible graphics/text unchanged until presentation; dirty history matches full-redraw oracle on both pages; at most 495 distinct graphics addresses written in a tested frame |
| VBL | Each tested presentation occurs inside the functional VBL model; starting in an existing blank still waits for a fresh edge |
| Native text | Four normal-code rows follow selected HGR/text page; coordinates/status change; initial resource counters remain fixed at W06 defaults |
| Attribute removal | Private-copy ink changes leave pixels/masks identical; attribute cells are transparent, with native row-span silhouette opacity |
| State/ownership | Runtime writes restricted to private ZP, stack, relocated state/event ring, hidden HGR and its four text rows; application and `$A000` baseline unchanged |
| Keyboard | Strobe consumed once per polled character, Apple right `$15`, lowercase normalization, aliases and reset tested |
| Events | Native walk/stop cue catalog plus separate diagnostics; ring cap/wrap/overwrite and 16-bit tick carry tested; **zero speaker accesses** |
| Stack | Minimum SP `$F9` observed in the executed test paths; this is path coverage, not a full-game stack proof |
| Local HTTP view | GET page/frame and POST A/R verified against executed CPU pose changes; browser layout/keyboard-event delivery not exercised because no browser surface was available |

The headless `tools/run.py` trace starts at x19/y140, walks to y180, stops at
the floor, turns right, reaches x31/y180 and emits the right-portal request.
It then crouches and stands. Native other-room transitions remain deferred.

```sh
make bootstrap
make test
python3 tools/run.py
python3 tools/run.py --serve
```

Generated evidence: `build/test-results.json`, `cpu-verification.json`,
`execution.json`, `room12-boot.png`, `room12-after.png`, `test-screen.png`.
The aggregate test runner reports failures and returns nonzero; generated
execution reports must be matched to the current program hash before reuse.

## Static checks and host models

These are different evidence from executing the target CPU:

- Historical `verify_analysis.py` and `verify_integration.py` passed. Original
  TAP hash remains `7f01e1a3d05825aab887952cd5711bea69d6525730aba5c1e25c814334fe77d7`.
- Exported historical spans equal pinned B1/B2 bytes; CPU/TAP offsets, stable
  IDs and checksums are recorded. M2 ends at `$5C69` with its `$5C` sentinel.
- Room 12 decodes geometry 1, light 3, furnishing 2, no initial treasure;
  its three stored links and current-room special case are model checked.
- Full HGR address generation has 7,680 distinct bytes within an 8 KiB page;
  mixed mode displays 6,400 of them. Cropping the known cleared source header
  and mapping the remaining 165 rows covers all 160 graphics rows. Both native
  text-row address sets are independently checked.
- Selected stream decoding preserves skipped prefix, separate draw records,
  `$14/$16` event identity and both walking-phase deltas; complete grammar and
  source runtime scheduling are not certified.
- Isolated rational rule tests cover energy `<0`, merchant funds/wear, ordinary
  lock predicates, seven ordinary rewards/single pickup, poison consumption,
  pit formulas, objective prerequisites/victory and per-game reset. This does
  not emulate the original floating-point package or its random sequence.
- `.setcpu "6502"` / ca65 selected the documented instruction set. The harness
  also rejects unsupported opcodes on every executed instruction fetch.
- Python syntax and Markdown links were checked; `git diff --check` passed.

## Reproducibility

The project tools were removed from `local/` and reconstructed from the pinned
cached archives. The documented bootstrap completed, then build and tests ran.
A second resource regeneration/assembly produced identical game, `.do`, `.nib`,
room HGR and generated include bytes. This exercises clean tool reconstruction
and deterministic outputs on this host; first-run network delivery and a second
host remain separate checks. See `build/reproducibility.json`.

| Output | SHA-256 |
| --- | --- |
| `game.bin` | `699107ea7a2bc798634fef3f8fa60bf4b5bb8950e42eddabf4f1fe23e0b34720` |
| `laigle-dor.do` | `39f1c42a14a3f4e7ba908985eb9f6aaa2981f2f0eded872eedb71ff6dd00eee3` |
| `laigle-dor.nib` | `15b4cfd81cc11b5084828e8136d178e806c80b55abf68310ce833a65df56562d` |
| `resources/room12.hgr` | `541559a3ead66c5eeecfd4e56c4ea7ea8b0a3a4b3e155b28a811bddfaefd77de` |

Hashes above apply to the default fixture build at this record's date, not a
later build with a supplied Oric ROM or modified code. Pin the new manifest
when comparing another build.

## Remaining validation

The executed loader test begins in Disk II firmware, **not the Apple ROM reset
vector**. Device accesses are functional approximations: no analog disk timing,
floating bus, full video/IRQ scanner, auxiliary RAM mapping or NMI handling.
The new simplified NTSC cycle-phase clock exercises RDVBLBAR presentation waits.
CPU
instruction totals are test diagnostics, not a real-time or performance result.

Before extending compatibility claims, run the generated media in a full,
identified Apple IIe emulator and on hardware, capture boot/controls, and verify
drive seek timing, display mode/bank state, monochrome output and input latency.
Pin the Oric ROM and compare original room imagery, cursor anchors, two-phase
input order, collision queries and RNG/timer/effect calls. See
[work-package gates](work-packages.md) and [compatibility ledger](compatibility.md).
No project implementation has been promoted to a benchmarked or validated KB
technique.
