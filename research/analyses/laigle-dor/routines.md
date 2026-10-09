---
id: ANALYSIS-ORIC-0001-ROUTINES
program: "L'Aigle d'Or"
cpu: ["6502"]
machines: ["oric-1", "oric-atmos"]
analysis_status: draft
source_revision: "sha256:7f01e1a3d05825aab887952cd5711bea69d6525730aba5c1e25c814334fe77d7"
analysis_date: "2026-10-09"
---

# Routine inventory

## Reading this inventory

Names are analytical descriptions, not original symbols. `B1/B2` and offsets
follow [the overview convention](overview.md#precise-reference-convention).
Every B2 machine address `a` maps to original TAP offset `a + $3566`.
The BASIC text contains an exact location for every line; line ranges below
identify related routines without reproducing the entire historical program.
Ranges encompass shared branches; they do not imply separate callable functions
at every address. No original assembler or calling convention documentation was
provided.

## BASIC: first stage

| Lines | Entry CPU / TAP offset | Purpose and relationships |
| --- | --- | --- |
| 0–18 | `$0501` / `$000018` | Set VARTAB `$0F69`, HIMEM `$17FF`, display flags, title attribution and opening sound |
| 20–52 | `$05D4` / `$0000EB` | Decode hexadecimal strings into machine copy helpers at `$0400/$0430` |
| 100, 658 | `$06E9` / `$000200` | Author string and small state initialization |
| 1000–1020 | `$0725` / `$00023C` | Set HIRES; initialize `$60–$65`; CALL generated copy helper to display title |
| 1100–1200 | `$0779` / `$000290` | Repeated color/attribute effects and sound; state-based repetition |
| 1300–1350 | `$0894` / `$0003AB` | Additional graphics, author lettering, tune calls, story/control flow, CLOAD main stage |
| 1400–1450 | `$0A3E` / `$000555` | ROM MUSIC/PLAY sequence parameterized by octave `O`; called three times |
| 1500–1580 | `$0AEE` / `$000605` | Explain controls and equipment; GET key and return to title |
| 1600–1690 | `$0CF8` / `$00080F` | TEXT story, GET key, proceed to controls |
| 32849, 33792 | `$0F67/$0F6F` | Anomalous tail records; preserved but not given application meanings |

The generated `$0400–$0426` helper copies `(src),Y` to `(dst),Y`; `$0430–$0456`
reverses those pointers' roles in the first six bytes and shares the same
algorithmic tail. Both consume width/height/pointers in `$60–$65` and clobber A
and Y. `$0400` is explicitly called by B1 line 1020; no executed call to `$0430`
was established. Their runtime bytes can be reproduced from B1 lines 20/25/30.

## BASIC: main game

| Lines | Entry CPU / TAP offset | Purpose and relationships |
| --- | --- | --- |
| 0–1 | `$0501` / `$003A67` | Autorun/reset; VARTAB `$3C00`; RUN 1; HIMEM `$3DFF`; reset packed room records |
| 3–4 | `$054E/$0561` / `$003AB4/$003AC7` | Patch `$3E56/$3E57` to two NOPs or `ORA ($62),Y` |
| 5 | `$0574` / `$003ADA` | Write three collision-map cells beginning at `X+1`, using semantic value `W` |
| 6 | `$058C` / `$003AF2` | Reset movement/equipment stream cursors |
| 7–8 | `$05A2` / `$003B08` | Marshal BASIC state into `$0498,$04A1–$04A6,$0478/$0479,$04AB` |
| 9 | `$05FD` / `$003B63` | Impossible-action message / return |
| 40–50 | `$0627` / `$003B8D` | Initialize quest/economy/fatigue, conditional ROM patch, player name and score/name buffer |
| 90–99 | `$0713` / `$003C79` | Graphics cursor to byte coordinates, passage message, conditional animation, generic effect, save/draw wrapper |
| 100–199 | `$07D0` / `$003D36` | Room display dispatcher; derive geometry class and draw side features; set renderer / torch update addresses |
| 200–230 | `$093C` / `$003EA2` | Geometry type 0, repeated wall pieces and front feature |
| 300–399 | `$0A12` / `$003F78` | Geometry type 1 and shared perspective frame / feature handling |
| 400–430 | `$0B4D` / `$0040B3` | Geometry type 2, column overlays, shared front feature |
| 500–530 | `$0BF7` / `$00415D` | Geometry type 3, alternate perspective outline |
| 600–699 | `$0CAA` / `$004210` | Construct semantic grid, furnishings, treasures, gates, special objects and header attributes |
| 700–799 | `$0F8F` / `$0044F5` | Furnishing handlers; screen placement from room fields; chest/light-feature overlays |
| 800–884 | `$127F` / `$0047E5` | Treasure variants and floor features; save slots `$F9/$FA`, attribute renderer for some objects |
| 900–992 | `$13CB` / `$004931` | Ladder/gate geometry and matching collision cells |
| 1000–1110 | `$155F` / `$004AC5` | Small optional room decorations; line 1000 is only REM |
| 2300–2420 | `$15A4` / `$004B0A` | Tool/torch expiration; reset animation and return to equipment action |
| 2500–2599 | `$1655` / `$004BBB` | Inventory and temporary TEXT output |
| 3000–3092 | `$17B9` / `$004D1F` | Exterior/menu, Timer 1 latch, entering/shop/exit, replay and victory |
| 4000–4010 | `$19CB` / `$004F31` | In-game timer-latch setting; decode and render room; place actor; enter loop |
| 4100–4500 | `$1A0E` / `$004F74` | Entry/neutral actor placements and contextual message selection |
| 4600–4710 | `$1C8D` / `$0051F3` | Lock/open checks and packed room transition; decode destination then reconstruct scene |
| 4800–4810 | `$1DCA` / `$005330` | CALL collision; return machine result bytes to BASIC variables |
| 4900–4930 | `$1DFB` / `$005361` | Marshal state, collision for walking, animation advancement, torch/equipment refresh |
| 5000–5050 | `$1E4F` / `$0053B5` | Main action loop, darkness, enemies/traps, KEY$ and table-based dispatch |
| 5100–5990 | `$2058` / `$0055BE` | Torch lifetime, fatigue, enemy processing, HUD and death check; return to 5000 |
| 6000–6100 | `$2152` / `$0056B8` | Darkness TEXT transition, clear/preserve charset, light restoration |
| 6200–6240 | `$2209` / `$00576F` | Special horizontal graphic hazard, damage and audio; line-number byte supplies `RTS` at `$2283` |
| 6300–6520 | `$2287` / `$0057ED` | Gate state changes, enemy spawn decisions, treasure feedback |
| 6900–7060 | `$245F` / `$0059C5` | Special pit geometry, clear logical grid, set actor/quest state |
| 7100–7450 | `$269E` / `$005C04` | Pit input constraint, rope/climb sequence, return to room |
| 8000–8220 | `$287E` / `$005DE4` | Enemy-type dispatch, animation frame toggle, damage/sound, machine movement |
| 9000–9050 | `$29A5` / `$005F0B` | Death display, recorded names/attempts, replay menu |
| 9100–9130 | `$2A91` / `$005FF7` | Render backslash-terminated text with CHAR, six-pixel advance and line wrapping |
| 10000–10510 | `$2B15` / `$00607B` | Stop, directional movement and crouch/pose state machines |
| 10600–10690 | `$2D85` / `$0062EB` | Jump precheck, jump animation, staged equipment restoration |
| 10700–10799 | `$2E5B` / `$0063C1` | Pick up map-marked objects, mutate room treasure bits, quest rewards |
| 10800–10840 | `$3336` / `$00689C` | Read acquired messages, using shared text renderer |
| 10900–10990 | `$33AC` / `$006912` | Open doors/chests/passages, mutate packed room state |
| 11000–11520 | `$354D` / `$006AB3` | Select empty hand, torch, keys, vial or crowbar |
| 12000–12360 | `$36BF` / `$006C25` | Light-feature interaction, drinking, suicide and another staged vertical action |
| 13000–13510 | `$3912` / `$006E78` | Shop/input/purchase checks, inventory updates and money subtraction |
| 21845 | `$3BF4` / `$00715A` | GOTO 5100 fallback, matching `$5555` default key-table words |

Main keyboard dispatch is BASIC 5050: `DEEK($4300 + 2*ASC(K$))` supplies a
BASIC **line number**, not a machine address. Default `$5555` means decimal
21845, a real line. The motion pointer table at `$4200` and equipment pointer
table at `$4400` instead contain machine memory addresses of interpreted data.

## 6502: arithmetic and graphics

| Entry / range | Purpose | Inputs → outputs / effects | Relationships |
| --- | --- | --- | --- |
| `$3E00–$3E17` | Unsigned byte multiply | `$70*$71` → `$73:$72`, A high, Y low; consumes `$71`, clobbers X/flags | Called by address arithmetic |
| `$3E18–$3E20` | Import ROM cursor | `$10/$11` → `$62/$63`; A clobbered | ROM-cursor drawing wrappers |
| `$3E21–$3E3A` | HIRES byte address | `$69=x,$6A=y` → `$62/$63=$A000+40*y+x` | `$3E00`; requires binary arithmetic |
| `$3E3B–$3E51` | Load descriptor | `$68` ID → source `$60/$61`, width `$64`, height `$65`; X/A clobbered | Four aligned field tables |
| `$3E52–$3E77` | Rectangular copy / OR composition | Pointer-before-first-byte convention; consumes rows and advances source/screen | Pair patch at `$3E56` |
| `$3E78–$3EAE` | Save-under and overwrite | Read screen to packed buffer, copy image to screen, advance three pointers | `$3ECF`; `$3E80` currently NOP pair |
| `$3EAF–$3EBC` | Truncated-height helper | Original height minus rows remaining → save descriptor | Not reached by current NOP pair; intent/reachability unresolved |
| `$3EBD–$3EC5` | Draw at ROM cursor | Import cursor, load descriptor, tail-jump to blitter | BASIC variable `D` |
| `$3EC6–$3ECE` | Draw at byte coordinates | Calculate address, load descriptor, tail-jump to blitter | Restore and static-image routines |
| `$3ECF–$3EF0` | Save background and draw | `$6B` save slot, `$68` image, `$69/$6A` position; copies dimensions into save slot | `$3E21,$3E3B,$3E78` |
| `$3EF1–$3EF7` | Restoration remnant candidate | Copies `$6B` to `$68` then jumps into `$3EC5` | Target overlaps operand byte; no live caller established |
| `$3EF8–$3F08` | Add actor-relative offset | `$0478/$0479` added modulo 256 to `$69/$6A` | Animation interpreter and equipment |
| `$4000–$402A` | Copy with attribute column | Draw rectangle, then write `$6C` at offset 1 of each row | `$4078/$4082` |
| `$402D–$4068` | Attribute drawing with save-under | Save prior bytes, draw image, add row attribute; stop on screen `$0A` | `$408E`; branches to `$4069` |
| `$4069–$4076` | Record shortened saved height | Save only completed-row count in slot descriptor | `$402D`; partial-row consequences need testing |
| `$4078–$4081` | Attribute draw at ROM cursor | Cursor and descriptor → `$4000` | BASIC chest/treasure effects |
| `$4082–$408D` | Attribute draw at byte coordinates | Decrement x before computing screen base; call `$4000` | Shared by saved-color paths |
| `$408E–$40B1` | Save and draw with attributes | Decrement x, resolve save buffer and sprite dimensions, call `$402D` | `$4840` |
| `$40B2–$40B6` | Decrement x and ordinary draw | x → x−1; tail-jump `$3EC6` | Torch/equipment handler |
| `$40C0–$40C7` | Conditional torch update | Check `$047C == 3`, return or fall through | BASIC `B` is `$40C8`, so bypasses this check |
| `$40C8–$411F` | Torch/equipment visual state | Toggle high phase bit in `$0497`, test light state; draw torch/equipment using offset table | `$40B2,$3EF8`; BASIC CALL B |
| `$4140–$415B` | Save position and draw | `$6B` page slot; store x/y at offsets `$FE/$FF`; decrement x; tail-jump `$3ECF` | Main command draw handler |
| `$415C–$416D` | Long software delay | Nested Y/A/X decrement loops, clobbers registers | Stream opcode `$15`; no timer/VBlank sync |
| `$4840–$4858` | Save position and attribute draw | Store x/y at end of save page, tail-jump `$408E` | BASIC treasure variants |

Blitters clobber A, Y and their zero-page arguments; wrappers also clobber X.
The animation interpreter stores cursor state before drawing because draw calls
consume Y. None of these interfaces is demonstrated to be reentrant.

## 6502: room, animation, enemies and collision

| Entry / range | Purpose and relationships |
| --- | --- |
| `$3F0B–$3F13` | Extract next two high bits of `$71` into A using carry, without changing X |
| `$3F14–$3FF1` | Clear 120 grid bytes and 25 decoded fields; unpack two four-byte room records using rotations |
| `$4500–$4570` | Select/resume motion stream; handle restore, delta, yield, delay, chain and drawing commands |
| `$4574–$458C` | Restore saved image at its retained end-of-page x/y coordinates; `$4576` accepts preselected `$68` |
| `$4590–$45A9` | Stream command `$00`: add signed deltas to actor byte coordinates and retain cursor |
| `$45AA–$45FB` | Equipment stream, independent cursor; `$14` returns to caller; draw with pose-dependent y offset |
| `$46BA–$46FF` | Partial duplicate interpreter fragment with no established entry; unresolved remnant |
| `$495C–$4963` | Restore enemy save slot `$F6`; calls `$4576` |
| `$4964–$4975` | Save/draw selected enemy sprite at `$04B2/$04B3` using `$F6` |
| `$4976–$4A08` | Enemy type update: movement, bounds/direction reversal, proximity, torch/timer checks, restore and frame selection |
| `$4A09–$4A47` | Alternate enemy/contact phase, another y offset, damage/termination conditions |
| `$4A50–$4ACA` | Pursuit/update path: choose direction toward actor, move by three columns, test contact and bounds |
| `$4ACE–$4B3D` | Continue pursuit if engaged, otherwise timer-derived constrained idle motion and frame selection |
| `$4B40–$4B4F` | Add unsigned X to 16-bit grid pointer `$78/$79`, propagating carry |
| `$4B50–$4B71` | Earlier grid-pointer helper; first compare follows A=`$04`, so `$8C` equality path is impossible; no live caller established |
| `$4B75–$4B81` | Door-state check that marks movement blocked for states below 3 |
| `$4B82–$4BA9` | Classify semantic cell: negative, `$A0`, `$01`; set collision and special-object flags; requires incoming N established from A by caller |
| `$4BAD–$4BDB` | Direction 0 probe across three cells on previous grid row, plus y-limit handling |
| `$4BE0–$4C04` | Direction 1 probe; special right-door location and span of grid cells |
| `$4C08–$4C36` | Direction 2 probe; special left-door location and backward cell span |
| `$4C3A–$4C6F` | Direction 3 probe; front-door comparison or next-row cells |
| `$4C73–$4CB2` | Collision entry: build pointer, clear result, select room-specific front-door height and direction probe |
| `$4CB6–$4CDC` | Grid pointer `$0400 + x + row_offset`, where y=`$8C` → `$50`, y=`$A0` → `$28`, otherwise `$00` |
| `$4CDD–$4D50` | Advancing two-byte HIRES hazard on row at `$B130`; restore old bytes, preserve new ones, actor hit/bounds checks |
| `$4D55–$4DC4` | Jump permission: reject two facings, collision test at current x and x±4, restore actor x |

## 6502: replay and display transitions

| Entry / range | Purpose and relationships |
| --- | --- |
| `$4DDD–$4DFD` | Copy `$5600–$57FF` to `$5000–$51FF`; called by startup/replay |
| `$4E00–$4E28` | Clear exactly `$B400–$BB7F` using an exclusive end pointer `$BB80`; called after charset save |
| `$4E2A–$4E90` | Victory composition: six descriptors and position pairs at `$5B00–$5B0B` |
| `$4E94–$4EE9` | Another static-image composition with 79 background and 120 ink attribute rows; no established BASIC caller |
| `$4EEA–$4EF7` | Copy 256 bytes from `$B8F0–$B9EF` to `$5900–$59FF`, then clear charset area |
| `$4EF8–$4F06` | ROM call `$F89B`, patched to `$F8D0` conditionally; restore those 256 bytes to `$B8F0–$B9EF` |
| `$2283` | Single `RTS` byte in BASIC line 6240's number; target of BASIC 8205's decimal CALL 8835 |

`$4EF8` is the only direct external JSR in the identified application machine
paths. BASIC invokes many firmware operations by tokens instead. Its input
register assumptions and complete ROM clobber set are unresolved; do not invent
a clean ABI. The intended operation appears related to charset reinitialization
before restoring custom characters, but both ROM revisions require verification.

No game-owned IRQ handler, `RTI` path, stack trampoline, `PHA/PLA` preservation
scheme or hardware interrupt-vector installation was identified in established
game code. Apparent instances in tables or padding are not instruction evidence.
