# Maintained Apple IIe build outputs

| Directory | Contents |
| --- | --- |
| `game/` | Current DHGR color game: `laigle-dor-dhgr-color.do` / `.nib`, executable, symbols, map, assets, test reports and captures |
| `game-mono/` | Current HGR monochrome game: `laigle-dor-hgr-mono.do` / `.nib`, executable, symbols, map, assets, test reports and captures |
| `latency-baseline/` | Archived pre-optimization binary, labels, disk and profiles for each edition; required by the matched latency comparisons |
| `color/`, `dhgr/` and root-level reports/captures | Retained evidence from earlier prototype experiments; their obsolete executables, disks and exported assets have been removed |

The generic `laigle-dor.do` / `.nib` in each full-game directory contains the
same bytes as its named edition. Keep these aliases: preview, tests and profiling
use the generic disk name. `.do` and `.nib` are two encodings of the boot disk.
The full-game `resources/`, atlas/text/native-row binaries and `game.lbl` remain
available for the existing execution and verification tools.

From the [project directory](../README.md):

```sh
make games                                  # rebuild both current editions
make tidy                                   # remove obsolete/scratch outputs
python3 tools/tidy_build.py --dry-run         # inspect the selection
```

`tidy` removes ca65 object/listing files; `make games` regenerates them. It
preserves linker maps, source code, ROMs in `local/`, original/extracted Oric
inputs, full-game assets and recorded evidence. Historical review commands that
need a removed prototype binary require restoring its recorded revision from
Git; a rebuild of the current source does not recover a historical baseline.

The separate `make clean` target removes **all** build outputs and archives.
See the [input measurements](input-responsiveness.md) and
[renderer verification](renderer-verification.json) for evidence scope.
