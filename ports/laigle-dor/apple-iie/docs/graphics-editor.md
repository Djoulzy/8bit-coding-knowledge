# Optional L'Aigle d'Or editor adapter

The generic editor works without this adapter. From the repository root:

```sh
python3 tools/apple-iie-editor/server.py --adapter laigle-dor
```

Select the optional library in the left sidebar. Its assets are loaded on demand.
Save the full `a2-workspace-v2` project to retain sources and all modes. For the
compiler, use **Formats et conservation → Exporter les ressources natives JSON**.
This downloads `apple-iie-artwork.json` in the existing `a2-artwork-v1` format.
Without intervening edits, returning to the original mode restores its exact
native sprite/screen contract. Retouches automatically update the shared drawing
used by all modes. Editing a derived screen cannot recreate a native sprite ABI;
restore its previous document version before editing/exporting the native sprite.

## Reintegration

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
does not download these dependencies or rebuild disks. Rebuilding without
`LAIGLE_ARTWORK` regenerates the standard artwork.

| Project key | Compiler consumer |
| --- | --- |
| `laigle/game/dhgr/atlas/<id>` | Full-game shared atlas, actors, objects, scenery and HUD glyphs |
| `laigle/game/dhgr/title` | Full-game title MAIN+AUX banks |
| `laigle/game/dhgr/title-flash` | Explicit flash-state override |
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

