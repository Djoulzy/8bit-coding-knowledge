---
record_type: port-display-review
program: "L'Aigle d'Or"
machines: ["apple-iie"]
cpu: ["6502"]
status: analyzed
review_date: "2026-10-13"
---

# DHGR: preserve fine patterns before adding color

This records the **detail-v1** revision, SHA-256 `87f1b65923b05789e380cf95dfc13935831d4205817eb6a1c567195939896fdd`.
The subsequent [material palette revision](dhgr-palette.md) replaces its interior-only
tinting. Counts, size and Virtual II capture below refer to detail-v1.

The supplied HGR/DHGR captures, aligned at x19/y180, exposed a real conversion
loss: face marks, arm separation and architectural texture disappeared in the
first DHGR build. The user identified Virtual II with its color monitor setting.
The cause was in the exporter, independently of monitor differences: pairs
`01`, `10` and `11` all became one opaque foreground color cell. Mask opacity
was merged in the same way. Changing row color then painted large flat areas.

For example, source atlas 40 has 43 `01` pairs and 25 `10` pairs. Across the 23
retained actor images, the previous policy merged **1,252 mixed pairs**, out of
2,753 pairs containing foreground. These are atlas counts, not a count of marks
in one displayed frame. The old frame/page tests proved the implementation
matched that lossy policy; they did not prove visual fidelity.

## Resolution and display interpretation

Apple's [IIe Technical Note #3](https://mirrors.apple2.org.za/ftp.apple.asimov.net/documentation/hardware/misc/Apple%20IIe%20Technical%20Notes.pdf)
distinguishes serial-dot resolution from independently selected color columns.
DHGR carries 560 serial samples across each row, while a stable independent
palette cell uses four samples. A 140-column palette limit does not require
flattening all drawing into 140 geometric columns. High-contrast detail can
use finer patterns, with its appearance dependent on monitor decoding. This
does not provide 280 or 560 arbitrary independent 16-color pixels.

Similarly, monochrome HGR data viewed in color still contains fine dot patterns,
which generate luminance detail and color artifacts. Comparing only the nominal
number of color columns did not justify the loss shown in the captures.

The primary [Virtual II help](https://www.virtualii.com/VirtualIIHelp/virtual_II_help.html)
documents NTSC-oriented DHGR rendering and the distinction between color and
monochrome monitors. No RGB-card mixed-mode extension is assumed here.

## Current conversion

Keep each source dot and its opacity separately. Two DHGR serial samples
represent one source dot. In left-to-right sample order:

| Source foreground pair | Detail pattern |
| --- | --- |
| `00` | `0,0,0,0` |
| `10` | `1,1,0,0` |
| `01` | `0,0,1,1` |
| `11` at a detail boundary | `1,1,1,1` |
| `11` in a solid interior | Selected palette pattern |

Separate two-sample opacity masks preserve the transparent sibling of an edge
pixel. A source full-white pair becomes tinted only when surrounding horizontal
and vertical foreground supports an interior; otherwise its white pattern is
retained. Terrain follows the same detail/interior policy. The existing room-12
vertical mapping and original layer order remain in use.

[dhgr.py](../tools/dhgr.py) packs two four-bit pair-status records per byte,
plus one foreground pattern per row. [dhgr.s](../src/apple/dhgr.s) shifts both
arbitrary four-bit patterns and masks into the two memory banks. Neighboring
pixels remain intact, including pairs split across bytes/banks. All 1,252 mixed
source pairs retain their separate patterns; 454 solid pairs in the retained
images are selected for tinting. This is a conservative starting policy, not a
finished artwork redesign or a calibrated color recommendation.

The native application is 15,154 bytes, padded through exclusive `$9C00`;
it still fits below the two-bank `$A000` terrain baseline. The unchanged
double-buffer, keyboard, rules and collision contracts are in [dhgr.md](dhgr.md).

## Preview and comparison

The earlier local preview enlarged each palette cell to four uniform samples,
which also hid subcell luminance. The revised preview offers:

- **Color:** sample-aware digital approximation with neighboring patterns and
  short white runs, cross-checked against the authors' standard decoder in
  [Apple2js canvas.ts](https://github.com/whscullin/apple2js/blob/ee0aed25f73c69d0245e86a2a5fccb3324c3056c/js/canvas.ts#L718).
  The adapted preview logic/palette retain the authors' [MIT notice](apple2js-license.txt);
  that license does not apply to the historical game assets.
- **Monochrome:** the actual 560 serial bits, without a palette reconstruction.
- **Palette:** coarse four-sample cells, explicitly a diagnostic view.

This preview is not the Virtual II renderer or an analog CRT simulation. Fine
patterns can still create colored fringes; preserving the bit geometry does
not guarantee exact CRT luminance or a particular hue.

Run from the project directory:

```sh
make test VIDEO=dhgr
python3 tools/run.py --video dhgr --serve --port 8767
python3 tools/run.py --video dhgr --monitor mono
python3 tools/review_detail.py
```

The last command now executes the monochrome HGR binary, archived flat/detail DHGR
binaries and current palette DHGR binary with identical input, ending at x19/y180/frame 0.
It writes color/monochrome captures, HTML and source-detail counts under
`build/dhgr/detail-review/`. The archived baseline must exist under
`build/dhgr/revisions/flat-v1/` and `build/dhgr/revisions/detail-v1/`; both were
saved locally before rebuilding. They are comparison dependencies, not required for a fresh current build.

## Executed evidence

- **38 current DHGR tests pass:** 360 collision cases, 460 sprite/page/edge
  cases, 480 full palette writes, 120 partial-opacity writes and 60 hidden
  frame constructions. The new tests distinguish `01` from `10` and verify
  transparency per original dot, instead of accepting merged occupancy.
- **35 monochrome regression tests pass.** The original HGR binary hash is
  unchanged. A separate 26-frame comparison gives identical game states/events
  between the current native HGR and DHGR programs.
- **Virtual II 13.3:** a separate `Apple //e Untitled 2` test session used a
  MOS/Synertec 6502 at standard 1 MHz, 64-KiB main plus 64-KiB RamWorks RAM,
  the project's pinned Apple IIe ROM, and a slot-6/drive-1 `.do` image. Cold
  restart executed the game. The video inspector showed HGR, double resolution,
  mixed text and page 2. The main color display showed the restored details at
  x19/y180. N movement/floor, A crouch and space/stand were visually checked.
  [The exported screenshot](../build/dhgr/virtualii-detail-y180.png) is actual
  Virtual II output, not the project's preview. The original user session was
  preserved; the new test session remains separate.

Machine-readable current evidence is [dhgr-verification.json](dhgr-verification.json).
The local archived report records the former flat build separately. No physical
Apple IIe, display calibration, FPS benchmark or original Oric runtime was
performed. Remaining work is artistic: refine interior colors and control
fringes while retaining the recovered detail. The 80-column HUD's narrower font
is a separate display choice; this revision does not change its native text mode.
