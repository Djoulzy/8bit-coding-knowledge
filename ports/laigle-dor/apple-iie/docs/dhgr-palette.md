---
record_type: port-display-experiment
program: "L'Aigle d'Or"
machines: ["apple-iie"]
cpu: ["6502"]
status: analyzed
review_date: "2026-10-13"
---

# Material colors without flattening the actor

This records **palette-v1**, SHA-256 `924d15905bf08aef5709ff30d9c7d68b0ecc6d2b034ae67c863680d260b7ba43`.
The subsequent [actor refinement](dhgr-actor.md) trades hair/leg detail for
more uniform colors and adds brown boots; face and tunic retain this revision's
fine conversion. Palette-v1 counts and capture below describe the earlier build.

This revision follows the user's art direction after the
[detail recovery](dhgr-detail-review.md). Colors belong to the Apple port;
they are not recovered Oric ink values. Historical sources remain unchanged.

| Material | Palette index (lores order) | Low-first serial nibble |
| --- | --- | --- |
| Wall edges and column atlas 3/4 | White `$0F` | `$0F` |
| Doors and arches, atlas 5/7/8 | Gray `$05` | `$05` |
| Torches, atlas 14/15 | Brown `$08` | `$04` |
| Actor hair | Yellow `$0D` | `$0E` |
| Face and hands | Pink `$0B` | `$0D` |
| Tunic and sleeves | Green `$0C` | `$06` |
| Trousers, atlas 46–61 | Dark blue `$02` | `$01` |

[dhgr-palette.json](../resources/dhgr-palette.json) contains the material map and
anatomical row bands. Upper-body atlas 40–42 uses hair above row 5, skin below
that and tunic from row 12/13. Back-facing atlas 43 has hair through row 8,
neck rows 9–11 and tunic thereafter. Separate arm layers 64/65/67 begin with
green sleeves and switch to pink hands. Walking and crouching reuse these
source atlas layers at their original offsets; colors follow the layer,
not its screen y position. These bands are **provisional visual interpretation**
of the decoded atlas, not facts documented by the original author.

## Actor detail

The exporter keeps the four-bit source pair-status format and two-sample
opacity for each original dot. Full foreground pairs use the material pattern,
including former white edge statuses. Mixed foreground/black pairs intersect
the doubled foreground mask with that pattern. Black source marks remain
opaque black; transparent margins still preserve the background. If a fine
mark falls entirely on zero bits of its hue, retain its original bright detail
pattern. For example, the second half of a dark-blue `$01` cell has no set bit;
without that fallback an isolated mark would vanish.

This retains foreground side, holes and opacity for all **1,252 mixed pairs**
in the 23 actor images. It does not retain the exact old monochrome bitstream:
color patterns deliberately modulate luminance. A fine mark has only two serial
samples and cannot express every hue independently. Bright fallback marks and
composite edges can still produce blue/orange fringes. No coarse occupancy
union or fake preview overlay is used for the character.

## Static materials

Fine isolated white strokes in the previous terrain produced prominent colored
edges. Static room resources now use complete four-sample, phase-aligned color
cells. White edges therefore have a white body, doors a gray body and torches
a brown body. A mixed pair bracketed horizontally by the same material becomes
a black cut: this retains small enclosed dark marks that the first `any(pair)`
converter erased. Outside contours expand to a cell; enclosed cuts also widen.
This is a declared target-art compromise at 140 color columns, with less precise
static geometry than the previous doubled-dot terrain. It leaves actor masks,
game coordinates, collision data, double buffering and mixed text unchanged.

Ordinary NTSC color decoding still fringes some white/black transitions.
Complete color cells do not guarantee fringe-free composite boundaries. The
project preview remains a digital approximation; the native emulator capture
is the visual evidence used here. See [DHGR hardware references](dhgr.md).

## Build and evidence

```sh
make test VIDEO=dhgr
python3 tools/run.py --video dhgr --serve --port 8767
```

Mount `build/dhgr/laigle-dor.do` in Virtual II slot 6, drive 1, with the existing
DHGR/128-KiB profile and **color** display. Eject and reinsert after rebuilding:
a mounted image may be cached. The native application is 15,076 bytes, entry
`$6000`, padded through exclusive `$9B00` below the `$A000` terrain baseline.

Palette-v1 evidence is retained in the [local archived snapshot](../build/dhgr/revisions/palette-v1/verification-snapshot.json):
41 DHGR tests cover native boot/loader, 460 layer/phase/edge cases, 480 palette
writes, 120 partial writes, 360 collisions and 60 alternating hidden frames.
Three added resource tests check materials/anatomical bands, small dark marks
and stable static color cells. The functional CPU tests exercise assembled
code; anatomical interpretation is a visual/static assertion.

Virtual II 13.3 ran the rebuilt disk in the separate NMOS/128-KiB test session.
The color display was inspected during walking, standing and crouching.
[Exported native screenshot, x19/y180](../build/dhgr/virtualii-palette-y180.png).
No physical Apple IIe, calibrated CRT, frame-rate benchmark or Oric reference
execution was performed. The missing Oric ROM variation fixture remains declared.

`python3 tools/review_detail.py` now compares five actual binaries at x19/y180/frame 0:
monochrome HGR, archived flat DHGR, archived detail DHGR, archived palette DHGR,
and current actor DHGR. It requires the local `build/dhgr/revisions/flat-v1/`,
`detail-v1/` and `palette-v1/` archives;
it is optional for a fresh build. Captures and the actor mixed-pair audit are
written under `build/dhgr/detail-review/`.
