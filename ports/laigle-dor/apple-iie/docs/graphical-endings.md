# Graphical victory and memorial screens

Both full-game editions now display the historical victory and death artwork
in full-screen graphics: **280×192 HGR monochrome** or **140×192 DHGR color**.
Partial departure without all three quest objects retains the exterior TEXT
outcome. Original source files, extracted payloads and editor artwork are
preserved.

## Historical evidence and target presentation

Victory follows B2 **3000, 3080–3092**: return to the exterior with the book,
diamond and golden eagle acquired. The target's inverted `objectives` mask
must be zero when leaving room 12. Acquiring the last object elsewhere does
not immediately show the ending.

The six records in `$4E2A–$4E90` select these sprites and byte-column/y pairs
from `$5B00–$5B0B`:

| Atlas ID | Byte column | Source y |
| --- | --- | --- |
| 31 | 8 | 150 |
| 29 | 15 | 157 |
| 30 | 27 | 153 |
| 40 | 19 | 50 |
| 46 | 19 | 81 |
| 64 | 18 | 64 |

The original `$3E52` blitter writes columns `width..1`, so the first displayed
byte is one column after the supplied address. The converter checks the
instruction pattern of all six source records, preserves composition order,
and reads the original motto at `$5B11`: `Richesse  Sagesse  Puissance`.
The victory sentence comes from B2 **3090**.

Death follows B2 **9000–9050**. Sprite **112** is the tomb, and **113** is the
figure above it. The original x values at `$5BBE–$5BC2` are **102, 60, 144, 18,
186**. The memorial adds one tomb per attempt, with the corresponding
six-character name underneath. Five successive attempts are retained in
MAIN `$1380–$139D`; the next attempt starts a new visible memorial cycle.
The existing session-name storage and wrapping rules are reused.

The converter copies the source sprites, including their embedded INK
attributes. The death scene retains the upper blue paper band and the lower
white-ink area in the color edition. Source foreground dots are retained in
monochrome. No replacement ending illustration was drawn.

Display adaptations are explicit:

- Source picture rows 0–175 are sampled into target rows 0–159, keeping every
  complete sprite inside the picture area. The 240-pixel source width is
  centered with a 20-dot HGR margin or ten DHGR color cells.
- The motto or memorial names use native-height captured glyphs at y=164.
  Outcome/replay text occupies y=176 and y=184. All 192 rows are graphics;
  Apple TEXT is disabled for these two screens.
- The color edition maps source colors to the existing Apple palette and
  combines pairs of source dots into complete DHGR color cells, as on the
  title. This sacrifices fine color detail. Captured standard HIRES glyphs
  come from B2 `$9800–$9BFF`; their complete original ROM-driven CHAR execution
  has not been compared.
- **O or Return** starts another attempt, retaining the port's restart
  convenience. The original victory ends in the terminal loop at **3092**.
  **H / ?** still opens help and restores the graphical ending afterward.
- Audio remains an event log; no ending music has been added.

## Rendering and memory ownership

[ending_resources.py](../tools/ending_resources.py) generates six scenes:
one victory and five memorial variants. Each scanline is encoded as bounded
count/color pairs. No compressed run crosses a scanline. Names remain dynamic
and are drawn from the live session history.

Each disk slot contains the small renderer, captured font, five name x
positions and one scene's RLE data. Slot size is **8,192 bytes**:

| Scene | First physical sector | Track / sector |
| --- | --- | --- |
| Victory | 352 | 22 / 0 |
| Death 1 | 384 | 24 / 0 |
| Death 2 | 416 | 26 / 0 |
| Death 3 | 448 | 28 / 0 |
| Death 4 | 480 | 30 / 0 |
| Death 5 | 512 | 32 / 0 |

The archive ends before physical sector 544; the checkpoint module occupies
544–559. Both fit within the existing 560-sector
disk. It follows the three maps and AUX scanline archive without overlapping
them. The build checks both disk bounds and each overlay's 8 KiB limit.

[ending.s](../src/apple/ending.s) is a 60-byte resident loader. Its `ENDCODE`
segment follows RODATA. The DHGR worker-template end is `$9FFC`, below the
`$A000` baseline boundary; the linker guards this tight allocation. The build
assembles [ending-overlay.s](../src/apple/ending-overlay.s) separately with
[ending.cfg](../src/ending.cfg), using the linked resident addresses of
`row_lo`, `row_hi` and `draw_cell`.

On first use of each hidden frame page, the loader replaces disposable MAIN
`$A000–$BFFF` with the selected overlay and calls `$A000`. The overlay clears
and composes that hidden frame; DHGR writes AUX graphics through the existing
bank-safe renderer. Resident instructions, WORLD, AUX text and sprite archives
remain intact. The ordinary vertical-blank flip presents the completed frame.
Once both pages are cached, idle frames perform no disk reads or graphics
writes. Reset invalidates both tags and reconstructs the normal room baseline
before gameplay resumes. The overlay has returned to resident code before
that baseline is overwritten.

## Build, test and inspect

From the port directory:

```sh
make games
python3 tools/check_game.py --video mono --suite endings
python3 tools/check_game.py --video dhgr --suite endings
```

The build produces `ending-engine.bin`, `endings.bin`,
`resources/ending-manifest.json` and the scene rasters beside the usual disk
images. The manifest pins source sprite addresses/hashes, layout, RLE sizes,
overlay sizes and disk slots.

[ending_cases.py](../tests/ending_cases.py) compares the host composition
byte-for-byte with the **executed original 6502 blitters** (`$4E2A`, `$3EBD`,
`$3EC6`), without executing untrusted historical build scripts. Native tests
check all eight objective masks at the exit, both frame buffers, exact final
pixels, five names including lowercase, the sixth-attempt wrap, help, restart,
cache reuse and resident/AUX ownership. The focused selection also checks the
falling-grille death, partial departure, title and graphical map.

For a manual victory check, grant the three quest objects through Ctrl+D / 1,
return to room 12, then leave the castle. For death, Q reduces strength to zero;
the next ordinary wear update triggers the memorial. Restart with O or Return.

Executed results and image hashes are recorded in
[ending-verification.json](ending-verification.json). Functional CPU tests use
the real Disk II BOOT0 reader and supplied Apple firmware, without a system-ROM
cold start. They do not establish Virtual II, real-drive timing or physical
Apple display behavior. Earlier verification files retain their earlier
program hashes and are not evidence for these rebuilt disks.
