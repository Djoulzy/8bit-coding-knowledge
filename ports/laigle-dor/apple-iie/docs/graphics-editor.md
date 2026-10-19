# Optional L'Aigle d'Or editor adapter

The generic editor works without this adapter. From the repository root:

```sh
python3 tools/apple-iie-editor/server.py --adapter laigle-dor
```

Select the optional library in the left sidebar. Its assets are loaded on demand.
Use **Enregistrer dans L’Aigle d’Or** (or Cmd/Ctrl-S) to save into the project.
The server atomically replaces [resources/artwork.json](../resources/artwork.json).
This permanent input contains compiler-native `a2-artwork-v1` assets plus the full
workspace in its `workspace` member, retaining sources, variants and edit history.
Both full-game builds consume it automatically. Files under `build/` are generated
outputs and are not the durable editing target.

**Reprendre le projet local** reopens the saved workspace; the library also
returns the saved native graphics. A save merges selected/open resources with
previously saved ones, so closing another document does not discard its graphics.
Unknown game keys, conflicting copies and incompatible sprite contracts fail
before replacement. On a write failure, the existing file and unsaved UI state
are retained. Original Oric source/extraction files remain unchanged.

For a portable backup, use **Exporter une copie JSON**, which downloads the full
`a2-workspace-v2` project. Existing downloads can be imported with **Ouvrir un
fichier JSON**, then saved directly into the project. The separate **Formats et
conservation → Exporter les ressources natives JSON** command still provides
`apple-iie-artwork.json` for explicit external compiler overrides.
Without intervening edits, returning to the original mode restores its exact
native sprite/screen contract. Retouches automatically update the shared drawing
used by all modes. Editing a derived screen cannot recreate a native sprite ABI;
restore its previous document version before editing/exporting the native sprite.

## Recompile saved project graphics

After saving in the editor:

```sh
cd ports/laigle-dor/apple-iie
make games
```

`make game` rebuilds DHGR; `make game-mono` rebuilds HGR mono. The editor does not
invoke the assembler automatically. Restart an older editor server and reload
its page once to enable the new controls. Use full-game **Atlas … · jeu mono**
resources for monochrome edits. For existing workspaces, prototype mono sprite
edits are also copied to the matching full-game mono atlas keys at save time;
their pixels/masks have the same contract. Differing open prototype/full-game
copies of one sprite are rejected instead of silently choosing one.

The [standard build prerequisites](../README.md) still apply. `LAIGLE_ARTWORK`
overrides the saved project with another native JSON file; setting it explicitly
to an empty string uses the standard artwork for a comparison build:

```sh
LAIGLE_ARTWORK= make games
```

This does not delete or modify saved retouches. Rebuilding without that variable
uses `resources/artwork.json` again.

## Explicit external overrides

Save the downloaded JSON somewhere durable, for example
`tools/apple-iie-editor/projects/my-art.json` (this directory is ignored).
Validate it first, from the repository root:

```sh
python3 tools/apple-iie-editor/server.py --adapter laigle-dor --check tools/apple-iie-editor/projects/my-art.json
```

Then build with an **absolute path** so the port's working directory is irrelevant:

```sh
cd ports/laigle-dor/apple-iie
LAIGLE_ARTWORK=/absolute/path/to/my-art.json make game
# Prototype alternatives:
LAIGLE_ARTWORK=/absolute/path/to/my-art.json make build VIDEO=mono
LAIGLE_ARTWORK=/absolute/path/to/my-art.json make build VIDEO=color
LAIGLE_ARTWORK=/absolute/path/to/my-art.json make build VIDEO=dhgr
```

The existing assembler, ROM and build prerequisites still apply; see the
[port README](../README.md). The editor itself
does not download these dependencies or rebuild disks. An external override
temporarily replaces the automatic saved-project input for that build.

| Project key | Compiler consumer |
| --- | --- |
| `laigle/game/dhgr/atlas/<id>` | Full-game shared atlas, actors, objects, scenery and HUD glyphs |
| `laigle/game/dhgr/title` | Full-game title MAIN+AUX banks |
| `laigle/game/dhgr/title-flash` | Explicit flash-state override |
| `laigle/game/mono/atlas/<id>` | Full HGR mono shared atlas, actor pixels/masks and scenery |
| `laigle/game/mono/title` / `title-flash` | Full HGR mono title and explicit flash state |
| `laigle/prototype/<mono\|color\|dhgr>/sprite/<id>` | Matching prototype native sprite |
| `laigle/prototype/<mono\|color\|dhgr>/room12` | Matching prototype terrain banks, before RLE compression |
| `custom/...` | Independent document; export only, no automatic game insertion |

The current full game constructs its rooms from shared tiles and vectors.
Editing its atlas changes those tiles wherever used; editing the prototype's
room-12 bitmap does **not** replace a full-game room. Native sprite dimensions,
IDs and encoding are fixed to preserve the existing runtime ABI. Fine actor
retouches can increase packed asset size; normal assembler and disk/allocation
checks remain authoritative. The editor does not estimate free runtime memory.

Title edits carry over into the flash frame outside the original lightning
delta. An explicit `title-flash` document overrides that frame independently;
if both states are in the project, edit both as desired. The compiler recomputes
the flash patch from the two final pages, including the restore bytes.

The compiler writes `build/.../resources/artwork-overrides.json` with the
project SHA-256 and lists of consumed and unused keys. Multi-target projects
are supported: other variants and independent documents are reported as unused.
Use `--check` to catch misspelled game keys before building. Historical sources
and the default palette files are never changed by an artwork override.

LOWRES and independent screens can be created and exported for other Apple
software, but **the current game has no LOWRES renderer**. New sprite IDs,
animation timelines, room geometry, collision editing, arbitrary image-to-atlas
conversion and new game resource slots are outside this editor's first version.

## Direct-save verification, 2026-10-19

- **Executed service/model tests:** 21 Python tests passed, including same-origin
  HTTP save/reload, automatic compiler selection, partial-save merging, source
  retention, invalid/conflicting assets and failed atomic replacement.
- **Executed browser codec/workspace tests:** 29 JavaScript groups passed with
  the adapter enabled (301 assets); the compiler-resource wrapper reopens its
  complete workspace and latest retouches.
- **Executed browser workflow:** the existing downloaded workspace was imported,
  saved through the local-project button and reopened. Saved sprite pixels and
  masks exactly match the download; original sources and archives are retained.
- **Executed compilation:** `make games` built both editions without an artwork
  environment override. The saved mono sprites 47/48 are listed as applied in
  `build/game-mono/resources/artwork-overrides.json`. The DHGR binary/disk remain
  byte-identical for these mono-only edits.
- **Executed functional CPU checks:** both rebuilt disks passed Disk II BOOT0,
  title, introduction, name/exterior and room-12 entry. The edited mono sprite 48
  matched an independent dot/mask compositor at all seven horizontal phases on
  both graphics pages (14 comparisons), with visible differences from the
  original sprite. These are py65/functional-bus checks; the complete game suite,
  Virtual II and physical hardware were not rerun for this artwork change.

Reproduce the automated editor checks from the repository root:

```sh
python3 -m unittest discover -s tools/apple-iie-editor/tests -v
```

With the adapter running, open `http://127.0.0.1:8770/tests.html` for the
JavaScript groups. The supplied workspace lives inside the permanent artwork
file; use **Reprendre le projet local** to inspect or continue it.
