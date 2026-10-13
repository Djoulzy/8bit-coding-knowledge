# Toolchain, boot contract and memory ownership

## Available and selected tools

Initial inventory: Python 3.9.6, Make, Apple Clang, Git, curl and Homebrew were
available. No ca65/ld65/cc65, xa, acme, 64tass, py65 or native Oric/Apple emulator
was installed. No browser automation surface was available for a browser UI test.

The selected assembler/linker are built from the authors' cc65 **V2.19** source
tag. Build/test dependency URLs and archive/ROM hashes are in
[dependencies.json](../tools/dependencies.json). No historical source/build
script, unknown native game binary or system installation is executed. The
reviewed `src/Makefile` compiles and links `ca65` and `ld65`; the bootstrap does
not invoke its install, library or sample targets. The source's version output
is `V2.18 - V2.19`, as recorded by the actual tool invocation.

[ca65's official documentation](https://cc65.github.io/doc/ca65.html) describes
the assembly dialect. This project uses `.setcpu "6502"`, named labels,
`.segment`, `.include`, `.incbin`, `.byte`, `.align`, `.export` and `.res`.
It has no ca65 C runtime, Applesoft controller or 65C02 instruction dependency.
[ld65](https://cc65.github.io/doc/ld65.html) uses explicit configurations:
[game.cfg](../src/game.cfg) and [boot.cfg](../src/boot.cfg).

## Deterministic build

`tools/build.py` verifies the two extracted source hashes, regenerates selected
assets, invokes ca65/ld65 and creates the boot sector after calculating the
application's exclusive loaded end page. Its outputs include binary/listing/
symbols/link map, per-asset evidence, input-source hashes and tool versions.
No wall-clock timestamp enters the game or disk bytes.

`make build VIDEO=color` / `tools/build.py --video color` selects the separate
`build/color/` output directory and defines ca65 `HGR_COLOR=1`; the default
`mono` defines `HGR_COLOR=0` and retains `build/`. `tools/check.py` and
`tools/run.py` accept the same flag. `LAIGLE_VIDEO=mono|color` is the Python
tools' default selector; the Makefile passes its explicit `VIDEO` value.
Both variants use the same loader and game code. See the
[color experiment](color-experiment.md) for its executed checks and limitations.

`VIDEO=dhgr` / `--video dhgr` selects `build/dhgr/`, ca65 `DHGR=1` and
[dhgr.cfg](../src/dhgr.cfg). The linker places the two auxiliary read workers
at run address `$0040`, with their load bytes in the application image. Startup
copies them there after the boot firmware has finished. The NMOS entry and
Disk II boot contract are unchanged. DHGR has a separate
[128-KiB allocation and display contract](dhgr.md); the main-only allocation
table below applies to the HGR variants.

`tools/disk.py` writes track/physical-sector payloads using a DOS-order mapping.
The `.do` file contains 35 tracks × 16 sectors × 256 bytes. The `.nib` file
encodes identical physical sector payloads with standard address fields,
6-and-2 data and checksums, padded to 6,656 bytes per track. These are two
representations of the same boot disk, not two filesystems. The mapping and
algorithm were checked against the authors' [apple2js format implementation](https://github.com/whscullin/apple2js/blob/ee0aed25f73c69d0245e86a2a5fccb3324c3056c/js/formats/format_utils.ts).
Actual BOOT0 sector decoding is exercised in CPU tests; the tests do not replace
sector reads with a high-level file-load trap.

## Loader ABI

This loader requires a Disk II **16-sector** controller in **slot 6**, drive 1,
track-0 initial seek and ordinary main-RAM loading. It is not a generic slot,
13-sector, SmartPort, DOS RWTS or ProDOS interface. A cold/warm system reset and
firmware workspace coexistence are outside the current tested entry contract.

1. Enter the controller BOOT0 at `$C600`. Its ROM generates the GCR decode table,
   seeks track 0 and reads physical sector 0 into `$0800`.
2. The sector's first byte is 1; BOOT0 transfers to `$0801`.
3. Our boot sector sets `$26/$27` to `$6000`, `$3D` to sector 1 and `$41` to
   track 0. It calls the private ROM reader by `JMP $C65C`, X=`$60`, C clear.
4. BOOT0 increments destination page and sector, reads until the exclusive sector
   count in `$0800`, then jumps back to `$0801`. This is **not** a JSR/RTS ABI.
5. Until all application pages are loaded, the sector moves the head two adjacent
   half steps, increments track, resets sector and re-enters the ROM reader.
6. It stops the motor with `$C0E8` and jumps to application entry `$6000`.

The tested ROM is exactly 256 bytes, SHA-256
`de1e3e035878bab43d0af8fe38f5839c527e9548647036598ee6fe7ec74d2a7d`,
from the pinned [apple2js BOOT0 array](https://github.com/whscullin/apple2js/blob/ee0aed25f73c69d0245e86a2a5fccb3324c3056c/js/roms/cards/disk2.ts).
Its firmware calls `$FF58` and `$FCA8` execute in the local Apple IIe ROM;
they are not emulated as instant-return hooks. The source array and decoded
ROM hashes are checked. ROM files stay in ignored `local/roms/`.
Real drive settle/retry/error timing is unverified; unreadable media can remain
in BOOT0's scan loop. The harness imposes an instruction timeout for diagnosis.

## Application ABI and allocation

Entry executes SEI/CLD, selects main memory/zero page/stack, sets SP=`$FF`, resets
state, initializes HGR and expands terrain. No further monitor, disk, OS or Oric
ROM calls occur. All helper calls may clobber A/X/Y/status and the private scratch
range; D must be zero. Nested callbacks/reentry and NMI sources are unsupported.

| Main-memory address | Owner / lifetime |
| --- | --- |
| `$0000–$007F` | BOOT0/firmware scratch during boot; application does not use it |
| `$0080–$00AA` | Application scratch, defined in `src/memory.inc` |
| `$0100–$01FF` | Application stack after entry; BOOT0/ROM stack during loading |
| `$0200–$03FF` | BOOT0 GCR decode/data workspace during loading; not application buffers |
| `$0400–$07FF` | Native text page 1; HUD rows 20–23 |
| `$0800–$0BFF` | Boot sector at startup, then native text page 2; HUD rows 20–23 |
| `$0C00–$0C1C` | Actor/controller/event metadata plus video/page dirty bounds |
| `$0D00–$0DFF` | 64-record silent event/diagnostic ring |
| `$0E00–$1FFF` | Unallocated by this prototype |
| `$2000–$3FFF` | Main-RAM HGR frame page 1, alternately displayed/drawn |
| `$4000–$5FFF` | Main-RAM HGR frame page 2, alternately displayed/drawn |
| `$6000` through generated loaded end | Application code, tables, generated resources and final sector padding |
| Loaded end through `$9FFF` | Unallocated by this prototype |
| `$A000–$BFFF` | Immutable terrain baseline for dirty repairs |
| `$C000–$C0FF` | Apple/Disk II I/O, never ordinary application RAM |
| `$C600–$C6FF` | Required controller firmware during boot |
| `$D000–$FFFF` | System ROM during boot; no language-card RAM allocation |

The native application is about 14 KiB in this milestone; the **current** exact
size and segment limits are generated in `build/game.map` and
`build/build-manifest.json`. All generated load pages must end at or below
`$A000`, where the terrain baseline starts. A full game's fit is not established.
HGR allocations are 8 KiB each; mixed mode shows 40×160 graphics bytes plus
four 40-column text lines. Both text pages belong to the application after loading.

The renderer consumes a frame with three ordered layers, canonical seven-bit
sprite pixel/mask rows, seven 256-byte shift tables and generated row
addresses. Runtime tests compare all seven phases against independent pixel
placement and protect right/bottom edges. Source legal actor anchors have a
20-pixel left margin; entirely invalid byte-x anchors are a no-op, not arbitrary
negative-coordinate clipping. Bit 7 stays zero; this requires a monochrome
output policy rather than a claim of white artifact color on composite displays.

Main-bank controls `$C000/$C002/$C004/$C008`, 40-column/default charset controls
`$C00C/$C00E`, HGR/page/mixed/text controls `$C050/$C053/$C054/$C055/$C057`, and keyboard
strobe `$C010` follow Apple's [IIe Reference Manual](https://www.applelogic.org/files/AIIEREF.pdf),
Chapters 2 and 4, and its [monitor-ROM listing addendum](https://mirrors.apple2.org.za/ftp.apple.asimov.net/documentation/hardware/machines/Reference%20Manual%20Addendum%20Monitor%20ROM%20Listings%20IIe.pdf).
`$C000` read is keyboard data while write selects 80STORE off. The program reads
the keyboard before reading `$C010`; it does not use the any-key-down flag as
the game walking-state flag. [Display contracts](display.md) cover `$C019`
polarity, paired text/graphics pages and per-page dirty history.

## Harness boundaries

`tools/machine.py` uses py65's documented NMOS instruction implementation and
authors' pinned Apple IIe/Disk II ROM bytes. It begins at `$C600`, not the reset
vector, with main-bank assumptions and a simplified keyboard/video/drive bus.
Each disk latch read returns the next encoded nibble; analog flux, rotation and
bus timing are omitted. Page pixels and selected native text rows are decoded
from actual RAM writes. A simplified NTSC RDVBLBAR cycle model exercises page
presentation waits; it does not implement the complete video scanner.

This proves execution of the selected binary paths and the sector loader under
that model. It does not prove cold boot, video synchronization, IRQ/NMI handling,
auxiliary banking, monitor/OS coexistence, drive timing or physical compatibility.
The generated screenshots are target RAM captures, not original Oric captures.
No benchmarked/validated optimization claim is made.
