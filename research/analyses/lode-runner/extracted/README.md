# Extraction and evidence conventions

The only historical input is
research/sources/Apple IIe/Lode Runner/Lode Runner (1983)(broderbund)[cr].dsk.
SHA-256: cbc048a55c2835f1b3b54696660e8902c84c25dac44a6dc94b13a7e8f81379ec.
Repository baseline: d02edc77fa0a02d3f679af22456ca1c762c305dc. The source directory is gitignored.
Author/publisher, cracked-edition limits and unknown license are recorded in
[overview](../overview.md). Extracted bytes and analytical listings are evidence
for local research; no permission to redistribute the game is established.

## Reproduce

Run from the repository root with Python 3 and its standard library:

~~~sh
python3 research/analyses/lode-runner/tools/inspect_disk.py --extract
python3 research/analyses/lode-runner/tools/verify_analysis.py
~~~

Both tools read the historical image; they write only this analysis's derived
artifacts. They verify the pinned input hash and do not execute imported machine
code, DOS or a build script. The documented NMOS decoder is imported from the
reviewed local [inspect_tape.py](../../laigle-dor/tools/inspect_tape.py);
its main function is not run. No external Python packages are needed.

For additional selected decoding:

~~~sh
python3 research/analyses/lode-runner/tools/inspect_disk.py --runtime --disassemble 8438 84c0
~~~

Without --runtime, addresses refer to the initial DOS load. --runtime applies
the observed loader copies. Neither mode establishes code reachability.

## Disk/file mapping

The image has 35 tracks, 16 sectors per track and 256 bytes per sector.
DOS logical sector to image slot:

~~~text
sector: 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F
slot:   00 0E 0D 0C 0B 0A 09 08 07 06 05 04 03 02 01 0F
~~~

Original byte offset is (16 × track + slot) × 256 + byteWithinSector.
The successful mapping yields coherent catalog and T/S chains, lengths and
allocation counts; identity image slots fail the same checks.
Image filename extensions alone do not establish sector order; see the
[CiderPress author's manual](https://github.com/fadden/CiderPress2/blob/main/docs/Manual-cp2.md).
This parser supports this non-sparse DOS snapshot, not every disk format.

[manifest.json](manifest.json) stores every live file's catalog location, T/S list,
file sector index, image offset, header length and payload hash. For a payload
byte, add the header length, divide by 256 to select the mapped file sector,
then add the remainder to that sector's original image offset.

lode-runner.bin contains the declared DOS payload, without the four-byte binary
header. It is the **initial** load at $07FD–$96FF, not a complete runtime memory
snapshot. hello.bin omits its two-byte Applesoft length header.
Their exact hashes are in the manifest.

## Loader model and limitations

[loader.asm.txt](loader.asm.txt) preserves initial-load addresses. All other
listings apply three copies under D = 0 and uninterrupted loader-pointer
ownership, with each byte retaining its original disk offset:

1. $8F04–$9701 → $0004–$0801, ascending.
2. $3A00–$5F01 → $9B00–$C001, ascending; $C000/$C001 are I/O writes.
3. $3A00–$0900 → $4000–$0F00, descending.

$9700/$9701 are outside the payload. The model's separate provenance array marks
these and all other uncaptured memory unknown, even though its bytearray storage
uses zero placeholders. It rejects listings containing unknown instruction bytes.
It does not predict I/O effects, ROM/DOS state changes, interrupts, the inherited
stack pointer or any intervening patch. The loader's own pointer-variable writes
are not modeled as CPU execution. The model is for selected byte provenance,
not boot correctness.

Every instruction line is CPU-address, DSK=original-offset, bytes, instruction.
The DSK field maps the first instruction byte. An instruction can cross
nonconsecutive disk sectors, so following bytes must use the provenance map;
do not assume a contiguous image span from one field. Line numbers are generated
evidence locations, not original source lines. Original assembler syntax, names
and labels are unknown. $ notation is an analytical formatting convention.

Linear decoding can interpret data as documented instructions. Start/end spans
are deliberately selected; a valid opcode does not prove executable code.
tables.hex.txt has analogous mappings for reconstructed data.

## Artifact roles

| Artifact | Purpose |
| --- | --- |
| manifest.json | Live DOS files, exact sector ownership and byte/hash provenance |
| hello.basic.txt | Analytical decoding of the starter's single BASIC line |
| loader.asm.txt | Binary entry, crack front end and relocation |
| startup.asm.txt | Title, session and main cycle fragments |
| level.asm.txt | Nibble codec, metadata and board preprocessing |
| renderer.asm.txt | HGR helpers, compositing, sprite expansion and HUD |
| movement.asm.txt / scheduler.asm.txt | Player prefix, guard scheduling, guard record, holes |
| input-audio.asm.txt | Keyboard, analog input, text/audio streams, timing |
| editor.asm.txt / disk.asm.txt | Selected editor entries and disk interfaces |
| tables.hex.txt | HGR/grid/coordinate/quota/mask/pointer/pair/token data |
| level-audit.json | 150 candidate board sectors selected by observed formula |
| ../verification.json | Static checks and explicit unresolved anomalies |

The level audit assumes the reconstructed disk-selection formula and selected
sector permutation. It neither demonstrates successful level I/O nor certifies
every original board. Candidate level 136 is anomalous; no repair is inferred.

The verifier checks byte reconstruction, listing references, 192 row addresses,
896 full-byte phase outputs, coordinate tables, quota/cursor bounds under stated
conditions, token-domain exceptions and board-marker statistics. It is a static
property suite, not emulation or a performance benchmark.
