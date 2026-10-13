---
record_type: port-display-design
program: "L'Aigle d'Or"
machines: ["apple-iie"]
cpu: ["6502"]
status: analyzed
review_date: "2026-10-13"
---

# DHGR feasibility and selected display design

The requested combination of 16 independently selected colors and the existing
280-dot monochrome horizontal resolution is unavailable in standard Apple IIe
DHGR. Apple's [IIe Technical Note #3](https://mirrors.apple2.org.za/ftp.apple.asimov.net/documentation/hardware/misc/Apple%20IIe%20Technical%20Notes.pdf),
printed pages 2, 8–10 and 16–17, establishes these constraints:

| Display | Full graphics | Mixed graphics | Independent colors |
| --- | --- | --- | --- |
| Existing HGR monochrome | 280 × 192 dots | 280 × 160 dots | Black/white |
| DHGR monochrome | 560 × 192 dots | 560 × 160 dots | Black/white |
| Standard DHGR color | 140 × 192 color cells | 140 × 160 color cells | 16 |

Four serial bits form each color cell. A 560-dot presentation grid does not
provide 560 independently colored pixels. Scaling a 140-cell preview to 280 or
560 display samples cannot recover discarded artwork details. DHGR can improve
palette flexibility, but this alone does not meet the user's resolution request.

## Hardware and memory plan

The new profile would require a Rev-B-compatible IIe with a suitably configured
extended 80-column/64-KiB auxiliary card. It changes the earlier main-RAM-only
profile. Graphics initialization would enable HIRES, 80COL and AN3-off; mixed
mode necessarily displays **four 80-column text rows**. Both banks of the
bottom text page must be populated.

Keep 80STORE off for real PAGE2 display selection. A complete DHGR frame uses
8 KiB in main RAM and 8 KiB in auxiliary RAM at the same addresses. Alternating
frames therefore own `$2000–$3FFF` and `$4000–$5FFF` in both banks. A terrain
baseline at `$A000–$BFFF` in each bank would make total graphics ownership
48 KiB across the two banks. Neither auxiliary HGR half is a second displayed
frame by itself.

The existing main-RAM game state, keyboard, event ring and logic can remain
independent of display packing. Extend the renderer and harness to cover both
banks, per-page dirty history, hidden text/graphics construction, fresh VBL
flips and correct bank restoration. Avoid fetching main-RAM code while RAMRD
selects auxiliary RAM: bank-changing read workers need a safe execution area
or an explicit mirrored-code contract. 80STORE page-1 overrides do not provide
general access to the auxiliary page at `$4000`.

## Selected choice and evidence boundary

The user selected the **140×160, 16-color DHGR experiment with adapted
sprites**, retaining double buffering and four text rows. The implementation
and target profile are now documented in [dhgr.md](dhgr.md).

The design above was checked against primary references. The new banked
renderer and its functional CPU/MMU tests provide separate execution evidence;
the earlier [HGR experiment](color-experiment.md) does not validate DHGR.
A scaled palette preview remains a representation of 140 color columns.
Complete machine compatibility and physical-hardware validation remain outstanding.

The subsequent [detail review](dhgr-detail-review.md) corrects the initial
interpretation of that color limit: it does not require flattening all geometry
to full palette cells. Fine serial patterns are retained and the revised binary
has a separately recorded Virtual II 13.3 color smoke test. Physical validation
remains outstanding; the first build's evidence is preserved as a local archive.

The next [material palette revision](dhgr-palette.md) preserves fine actor masks
while adapting static material contours to phase-aligned cells. It documents
that geometry/color trade-off and the remaining NTSC edge fringes explicitly.
