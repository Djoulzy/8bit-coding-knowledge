---
record_type: port-display-experiment
program: "L'Aigle d'Or"
machines: ["apple-iie"]
cpu: ["6502"]
status: analyzed
review_date: "2026-10-13"
---

# Uniform actor colors and brown boots

After accepting the [material palette](dhgr-palette.md), the user preferred
less detail and more uniform hair/leg colors. The face and green tunic were
accepted. A subsequent request singled out the **left-facing face** for
retouching; front, right and back faces keep their previous conversion.

All changes are Apple target art, configured in
[dhgr-palette.json](../resources/dhgr-palette.json), not historical-source edits.
Room-12 main and auxiliary terrain bytes are identical to accepted palette-v1.
Game rules, collisions, keyboard, silent events, mixed text and double buffering
retain their contracts. No new 6502 instructions or video switches are needed.

## Hair, legs and boots

Hair in upper atlas 40–43 now uses complete, phase-aligned yellow `$0D` cells.
Original whole black pairs remain dark; mixed-pair checker texture is smoothed
into yellow. This avoids the previous green/bright flecks inside the hair.

Lower atlas 46–61 uses complete dark-blue `$02` cells for trousers and brown
`$08` cells for boots. Standing/walking atlas 46–57 changes material at row 16,
following the visible cuff/knee region. Crouching atlas 58–61 changes at row 11,
following its compressed/folded geometry. These boundaries are provisional
artistic interpretations of decoded source shapes. Materials follow the atlas
layer, so walking/crouching offsets do not turn shoes blue accidentally.

For legs, a mixed pair enclosed horizontally by foreground becomes an opaque
black cut; an outside contour becomes a full material cell. Whole opaque black
pairs remain black. In front-standing atlas 46, this preserves a black column
between the legs instead of merging both into a blue rectangle. Four-sample
opacity deliberately rounds the outline to native color columns. Edges/cuts may
move or widen by one original source dot. Boots use the same brown palette
entry as the accepted torches, without their former orange detail fallback.

The existing compact row format is sufficient: statuses `$00`, `$05`, `$0F`
encode transparent, opaque black and complete material cells. Selected hair/leg
rows no longer use partial color masks. The application remains 15,076 bytes,
entry `$6000`, page-padded exclusive end `$9B00`.

## Left-facing portrait

Atlas 42's skin rows 5–12 use complete pink `$0B` cells. Its source-derived
silhouette remains, with checker marks smoothed. Two declared native edits add
an opaque black eye at row 7/cell 5 and a mouth notch at row 10/cell 4. Cell
indices are local four-sample columns in the 12-cell-wide sprite, not screen
coordinates or Oric byte addresses. These edits are new artwork decisions.

This removes the unsightly phase-dependent marks in that profile while giving
it a readable eye/mouth. All left-facing walking/crouching poses reuse atlas 42;
its repeated equipment-layer draw remains idempotent. Other skin, tunic and
hand rows retain their original fine masks and material bytes. In particular,
the front face remains unchanged as requested.

## Reproduction and evidence

```sh
make test VIDEO=dhgr
python3 tools/review_actor.py
python3 tools/run.py --video dhgr --serve --port 8767
```

`review_actor.py` executes the native compositor and page presentation for all
16 linked frame IDs at x19/y180. These are **renderer fixtures**, not a gameplay
recording. It produces actual-bank-byte digital PNG previews and HTML under
`build/dhgr/actor-review/`; the digital preview is not a calibrated CRT.

For comparison with the accepted palette-v1 build saved locally before editing:

```sh
python3 tools/review_actor.py --baseline build/dhgr/revisions/palette-v1
```

This additionally compares native resource row bytes for all unchanged fine
face/tunic/hand regions and asserts identical main/aux terrain. The optional
archive is not necessary for a fresh current build. Historical source hashes
remain verified by the exporter and test suite.

[dhgr-verification.json](dhgr-verification.json) pins current build/test evidence:
44 DHGR tests and 41 monochrome regression tests; 460 layer/phase/edge cases,
480 palette writes, 120 partial writes, 360 collisions and 60 hidden frames.
Artist-selected bands/marks are static assertions; compositor, bank access,
dirty restoration and presentation are executed NMOS checks. The actor review
captures 32 fixtures when using the baseline. Gameplay comparison separately
executes identical keyboard input in the native mono/DHGR programs.

The rebuilt disk was also inspected in the separate Virtual II 13.3 color
session with its retained NMOS/128-KiB profile. Native captures:
[front](../build/dhgr/virtualii-actor-front-y180.png) and
[retouched left profile](../build/dhgr/virtualii-actor-left-y180.png).
Some NTSC boundary fringes remain; this revision favors stable body colors
over fine hair/leg texture. No physical hardware, calibrated CRT, FPS benchmark
or original Oric reference execution is claimed.
