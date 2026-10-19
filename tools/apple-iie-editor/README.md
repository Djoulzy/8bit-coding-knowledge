---
record_type: development-tool
machines: [apple-iie]
status: analyzed
review_date: "2026-10-19"
---

# Apple IIe graphics atelier

A **generic, standalone** Apple IIe graphics editor with a French interface.
Create screens, import PNG/JPEG images or native memory dumps, edit pixels,
compare graphics modes and export hardware-ready data. No game, historical
source, ROM, assembler, package installation or network service is required.
Python 3.9+ and a modern browser are sufficient.

The complete `apple-iie-editor/` directory can be copied outside this repository.
Optional project libraries are adapters; none is loaded by default.

## Start

From the repository root:

```sh
python3 tools/apple-iie-editor/server.py
```

Open **http://127.0.0.1:8770/**. From a standalone copy, run `python3 server.py`.
`Launch.command` provides a macOS launcher. `--port 8771` selects another port;
Ctrl-C stops the server. Use HTTP rather than opening `index.html` directly.
The server binds only to loopback and serves an explicit file list. The default
standalone editor saves through the browser. An explicitly selected writable
project adapter can also save to its own fixed project resource file.

## Change modes without losing information

**Mode graphique changes the rendering of the current document.** All modes
represent one drawing. There is no manual reference-promotion step and no
independently edited per-mode version to restore when changing modes.

- The original source remains intact, including full imported RGBA/file bytes,
  native banks, unused bits, screen holes and native sprite masks.
- Retouches are stored as local changes against the view that was edited.
  Other modes update only cells sampling the changed pixels. Existing native
  bytes outside those regions are preserved, including fine lines, color phases,
  screen holes and reserved bits. Returning to a mode does not re-encode its
  entire image from a lower-fidelity intermediate view.
- Merely browsing modes does not accumulate quantization. A mode opened for the
  first time is derived from the original reference plus the shared edit history.
- Previous document revisions remain available through **Restaurer cette version**.
  Undo/redo also covers edits, mode changes and revision restoration.

For example, draw fine colored strokes in HGR, change to DHGR and draw elsewhere:
returning to HGR retains the original strokes and adds the converted retouch.
Similarly, editing one LOWRES cell does not reduce fine detail across the rest
of the image. The edited cell covers a larger area in higher-resolution modes;
that area changes intentionally. In HGR, chromatic retouches can also affect
neighbors sharing a byte's phase, as required by the hardware. A target mode's
palette and resolution still limit how a new stroke appears, while its full
native edit is retained for other views and the saved project.

The `sources` list can contain immutable `edit` revisions, each with a backward
`base` reference and exact native `before`/`after` images. Derived views apply
these edits locally; they do not flatten the original. Invalid forward, cyclic
or format-changing edit references are rejected. Older native/RGBA workspaces
remain readable. If an older editor already flattened a drawing, use a preceding
archived version to recover the earlier detail; opening the file does not silently
replace the current drawing with a guessed reconstruction.

Saving the workspace and exporting native resources also synchronize pending
retouches. Conversion caches in `variants` are views of one revision, not separate
drawings. Workspaces created by the earlier independent-mode editor are migrated:
the visible drawing drives subsequent conversions, and the previous independent
views remain in a legacy archive. The optional `linkedModes` flag distinguishes
these semantics within the existing `a2-workspace-v2` format.

This is non-destructive *project editing*, not lossless encoding into every
hardware format. A standalone LOWRES/HGR/DHGR binary contains only that mode's
limited representation. Keep the workspace JSON to preserve the original and
other variants. A native sprite converted to another mode becomes a derived
screen fitted to the display. Switching back without edits restores the original
sprite's size, opacity and ABI exactly. Editing that derived screen makes it the
shared drawing; restore the preceding version to recover the native sprite.
Generic arbitrary-size sprite formats are not inferred from screen dumps.

## Save, resume and export

In standalone mode, **Enregistrer le projet** downloads `apple-iie-workspace.json`, schema
`a2-workspace-v2`. It includes all documents, sources, variants, active views and
archives. **Ouvrir un projet** accepts this format and migrates the earlier
`a2-artwork-v1` files. Documents are added instead of silently replacing open
work. Source bytes already discarded by an older image import cannot be recovered
retroactively; reimport that original image to preserve it under the new model.

Each document tab has a **×** button. Unmodified documents close immediately;
modified ones offer **Enregistrer et fermer**, **Fermer sans enregistrer** and
**Annuler**. Saving preserves that document's sources, variants and archives in
its own workspace JSON. Supported browsers use a file picker: cancellation or
write failure leaves the document open. Other browsers initiate a download;
retain the downloaded file. Closing the last tab creates a fresh blank screen.
Closed documents are removed from local recovery; previously downloaded files
are unaffected. Native/PNG exports do not mark a workspace as saved.

The editor also attempts browser-local recovery after edits. Storage quotas can
prevent recovery saves; keep downloaded projects as the durable copy. Recovery
is scoped to the browser origin: `localhost` and `127.0.0.1` have separate storage.
Projects are limited to 64 MiB on import/export, image/binary imports to 16 MiB,
and decoded image sources to 4,194,304 pixels. Oversized inputs are rejected
rather than silently reduced. Original sources and archives are never pruned to
meet a storage limit. Undo history is separate and retains 60 operations.

- **Exporter la source originale** recovers the original file/native page, or
  the original sprite in a native-asset JSON. For a newly drawn document, the
  original is its initial blank screen; later drawing is retained in its views.
- **Enregistrer ce document** saves just the selected document as a complete
  workspace, including its sources and archives.
- **Exporter le binaire natif / MAIN / AUX** writes only the active native screen.
- **Exporter l'aperçu PNG** exports the current preview, including checkerboard
  for native sprites; this preview is not a preservation format.
- **Formats et conservation → Exporter les ressources natives JSON** writes the
  visited modes of the current drawing as `a2-artwork-v1`, for integration with
  an external loader or optional adapter. It deliberately does not replace the
  full workspace save. Conflicting edits of the same asset key are rejected.

Validate a saved project without starting a server:

```sh
python3 tools/apple-iie-editor/server.py --check /absolute/path/to/project.json
```

## Drawing and importing

On desktop-sized windows, the central workspace fits the viewport height. The
compact heading, drawing tools and palette remain above the canvas; the canvas
uses the remaining space and scrolls independently at larger zoom levels.
**Contraintes du mode et conservation** expands the explanations when needed.
The fit zoom updates when this panel opens or closes. Side panels have their own
scrolling; smaller windows retain a flowing layout so controls remain reachable.

Use pencil, eraser, contiguous fill, line, rectangle outline or eyedropper.
Zoom and grid expose logical editing cells, while the preview shows the result.
The library lists the workspace's own documents by default; **Renommer** changes
its document name. **Nouvel écran** explicitly creates a new blank document.

For optional native sprite records, opacity/status and row color are separate.
Select a palette color, choose **Outil couleur de ligne**, then click a row.
Tiles can have a shared accent color and additive-composition black policy.
The checkerboard represents transparency. Erasing restores transparency;
opaque black is an explicit status. HGR sprite pixels and opacity are separate.
These compact records are an interchange extension, not a universal Apple format.

Keyboard: **B** pencil, **E** erase, **F** fill, **L** line, **R** rectangle,
**I** eyedropper, **Cmd/Ctrl-Z** undo, **Cmd/Ctrl-Shift-Z** redo,
**Cmd/Ctrl-S** save the project (directly to the local project when its adapter
supports that, otherwise through the browser).

Binary import uses the selected mode and explicit DHGR bank order. It requires
headerless files of the exact sizes below. DOS headers, disk images, RLE and
other machine formats are not guessed. Image conversion fits the source's
aspect ratio into the target display, adds black margins, averages samples when
reducing resolution and quantizes to the mode palette without dithering.
Transparency is composited onto black for native screens; the full original
alpha channel remains in the source. HGR color quantization is sequential:
later cells can change earlier neighbors through shared byte phase.

Imports create new documents by default. **Remplacer l'écran actif** replaces
its active screen while archiving the previous document revision; the operation is
undoable and preserves the original source. It is unavailable for native sprites.

## Native formats

| Mode | Display | Constraint | Raw bytes |
| --- | --- | --- | --- |
| HGR Mono | 280 × 192 HGR dots | Seven bits per byte, monochrome | 8,192 |
| HGR couleur | HGR color profile | 140 two-dot brush cells or 280 dots; six nominal colors, shared phase | 8,192 |
| DHGR couleur | 140 color cells / 560 serial dots × 192 | Four samples per cell; AUX/MAIN crossings | 16,384 |
| DHGR Mono | 560 × 192 monochrome dots | One bit per dot; seven AUX bits then seven MAIN bits | 16,384 |
| LOWRES | 40 × 48 cells | 16 colors; top pixel in low nibble | 1,024 |

**DHGR Mono** (`dhgr-mono` in JSON) has a black/white palette, point editing,
560-column native/PNG rendering and the same complete MAIN/AUX import/export
layout as DHGR color. Mixed mode displays 560 × 160 points. Bit 7 and screen holes
are preserved. Changing to this mode converts the current drawing to black/white;
**Moniteur → Monochrome** instead inspects the raw bits of an existing color view
without changing the document mode. DHGR Mono is a screen format; the optional
native sprite ABI remains limited to the modes supported by its adapter.

The selector offers five modes: **HGR Mono**, **HGR couleur**, **DHGR couleur**,
**DHGR Mono** and **LOWRES**. HGR couleur replaces the redundant “Color · HGR
artefacts” and “HGR · mémoire native” choices. Cell/dot editing, phase inspection
and memory inspection remain tools within the mode. The identifiers `color` and
`hgr` are still accepted in existing projects, sources, archives and native
exports; both display as HGR couleur. Opening these files preserves their native
bytes and identifiers without performing a conversion. New HGR color documents
use `color` for compatibility with existing adapters.

HGR Mono and HGR couleur use the same HGR hardware memory layout with different
editing/rendering policies. HGR/DHGR mixed mode displays 160 graphics rows;
LOWRES mixed mode displays 40. Text is reserved rather than rendered or edited.
Unshown bytes are retained in native variants. The page selector only changes
inspected addresses; each document variant represents one page.

DHGR color and DHGR Mono files may use MAIN+AUX or AUX+MAIN concatenation, explicitly selected.
Serial video order is always seven AUX bits, seven MAIN bits, repeated; bit 7
is not a displayed DHGR dot. A four-sample color cell can cross banks. Cell
writes preserve neighboring bits. HGR phase belongs to an entire seven-dot byte;
its button toggles bit 7 of the pointed byte, or a native sprite's common phase.

The HGR row offset is `(y & 7)*$0400 + ((y >> 3) & 7)*$0080 +
(y >> 6)*$0028 + byte_column`. LOWRES uses text-row addressing and two graphics
rows per byte. No raw import/export normalizes reserved bytes or screen holes.

Color previews are digital approximations: neighbor-aware HGR, sample-aware
DHGR, raw monochrome, and a coarse DHGR palette diagnostic that hides subcell
detail. No calibrated NTSC/PAL filtering, half-dot displacement, RGB-card
emulation, MMU execution or hardware timing is claimed. Native bank data and
packing are represented exactly, separately from preview colors.

## Optional adapters

For the existing L'Aigle d'Or library:

```sh
python3 tools/apple-iie-editor/server.py --adapter laigle-dor
```

The left selector then offers its 301 resources, including the complete mono
game's atlas and title. There is no automatic title
load and no game dependency in the default editor. See the separate
[adapter/reintegration guide](../../ports/laigle-dor/apple-iie/docs/graphics-editor.md).

With this adapter, the main button becomes **Enregistrer dans L’Aigle d’Or**.
It replaces `ports/laigle-dor/apple-iie/resources/artwork.json`, which normal
`make games` builds read automatically. The file contains native compiler assets
and the complete workspace, including original sources, retouches and archives.
Saving only the selected document merges it with previously saved resources;
closed documents' graphics are retained. **Reprendre le projet local** reopens
the saved workspace. Library resources also load their saved native retouches.
Reopening a JSON replaces a clean open copy of the same resource; unsaved open
retouches remain separate tabs. Conflicting native copies must be resolved before
overwriting compiler resources.

**Exporter une copie JSON** retains the browser download/file-picker workflow.
Generic documents are retained in the attached workspace but are not inserted
into game resource slots. The adapter rejects unknown game keys and changed
dimensions/encodings. Native resource saves are atomic, limited to 32 MiB and
accepted only as same-origin JSON requests; the browser cannot supply a file path.
After updating an already running server, restart it and reload the editor to
activate its new saving controls. Previously downloaded workspaces can be opened
and saved into the project without repainting them.

A custom trusted Python adapter can be supplied with `--adapter /path/library.py`.
Its contract is a `TITLE` string and an `assets()` function returning a dictionary
of unique asset keys to native `a2-artwork-v1` asset objects. The server imports
only the explicitly selected module and calls its library on demand. Adapters
are executable local code, not untrusted data files. Game-specific extraction
and compilation hooks belong in the adapter/project, not in the generic editor.
An optional `KEY_PREFIX` enables unknown-key checks for that adapter's namespace
when validating native-resource JSON with `--adapter ... --check ...`.
Writable adapters additionally expose `project_info()`, `load_project()` and
`save_project(workspace)`. The adapter owns its fixed storage location, validation,
atomic replacement and any compiler integration. `project_info()` supplies a
display name, informational file path and existence flag. The save callback
returns a user-facing `message`. The generic server exposes these callbacks
through `GET/POST /api/project`; it provides no arbitrary filesystem writer and
does not execute a build. Adapters without these hooks remain read-only libraries.

## Validation and organization

`core.js` implements native codecs, `workspace.js` manages sources/variants and
conversion, `app.js` connects the UI, `project_format.py` validates portable
projects, and `server.py` provides the independent local service.
`ports/laigle-dor/apple-iie/tools/editor_adapter.py` owns game extraction.

```sh
python3 -m unittest discover -s tools/apple-iie-editor/tests -v
```

With a server running, visit **http://127.0.0.1:8770/tests.html**. Generic tests
cover native addressing/banking/phase, binary round trips, reversible mode
switching, non-cumulative quantization, shared retouches after save/reload and native export, legacy migration, source RGBA
and file-byte retention, reference archives, native sprite restoration and
schema migration. Game/vector checks are explicitly skipped without that adapter.
Python tests also copy the server outside the repository to check portability,
validate workspaces and exercise the optional resource compiler integration.

The 2 game-specific groups require the optional adapter in the browser. A separate browser
session verified that painting and then changing to LOWRES keeps one document
and displays the converted image. Browser checks also exercised tab closure,
cancellation of the save picker, save-and-close (including validation of the
written source and edited pixel), discard-and-close and closing an inactive tab.
This does not constitute physical CRT or
new edited-game-disk validation.

Shared-mode, DHGR Mono and local-edit update, 2026-10-14: 26 generic JavaScript
groups passed in Node (2 optional adapter groups skipped), and 12 Python tests passed. Checks
include all 560 monochrome columns, AUX/MAIN boundaries, reserved bits, raw bank
round trips, propagation into already visited modes, save/export synchronization,
legacy archive restoration, full-resolution source retention, HGR → edited DHGR →
HGR round trips, local erasure, chromatic phase, mixed-mode hidden rows and
cache-independent replay of shared edit revisions.

Hardware reference: Apple's [Apple IIe Technical Note #3](https://mirrors.apple2.org.za/ftp.apple.asimov.net/documentation/hardware/misc/Apple%20IIe%20Technical%20Notes.pdf).
Preview algorithms retain the existing port converter behavior; the local
[MIT notice](THIRD-PARTY-NOTICES.txt) credits Apple2js's DHGR classification.
No historical game artwork or ROM is bundled with this standalone editor.

Direct project saving, 2026-10-19: 21 Python tests and 29 browser JavaScript
groups passed with the optional adapter enabled. The downloaded mono retouches
were saved/reopened, both disks rebuilt through automatic project selection,
and the edited sprite checked against an independent compositor on the executed
6502. See the [scoped verification record](../../ports/laigle-dor/apple-iie/docs/graphics-editor.md#direct-save-verification-2026-10-19).
