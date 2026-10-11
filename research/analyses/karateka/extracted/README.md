# Derived evidence for the supplied Karateka disk

Input: `research/sources/Apple IIe/Karateka/Karateka (1984)(Broderbund).dsk`,
SHA-256 `4399db1c5469299f6a519abd890456ba1bbba70596d72096f1db4a84e5669370`.
Historical bytes remain in their original source file. These files are
reproducible analytical rearrangements of the provided binary, not recovered
assembler source, a runnable build or an authenticated original media edition.

## Files and phases

| Artifact | Interpretation |
| --- | --- |
| `boot-sector.bin` | 256 input bytes modeled at `$0800` during firmware boot |
| `boot-dos.bin` | First ten image slots, 2,560 bytes modeled at `$B600` before startup |
| `core-initial.bin` | 40,960 bytes at `$0800–$A7FF`; tracks `$01–$0A` reordered by observed descending loader |
| `resident-low.bin` | Initial `$2000–$27FF`, relocated to `$0000–$07FF` |
| `resident-high.bin` | Initial `$2800–$3FFF`, relocated to `$A800–$BFFF` |
| `manifest.json` | Input checksum, all 160 core-sector mappings, copies, file hashes and assumptions |
| `selected-disassembly.txt` | Selected phase-labeled linear spans; each instruction includes CPU address, first-byte DSK offset and captured bytes |
| `tables.json` | Row arrays, seven-bit reflection table and phase boundary masks, with CPU/DSK locations |

`DSK` is a zero-based byte offset, **not a physical disk-sector address or source
line number**. For selected core sectors, the disk slot is `(track × 16 + sector)
× 256`; CPU page is `$A8 − 16 × track + sector`. Runtime copies inherit byte
origins from their initial source addresses. An instruction across a remapped
page boundary can have noncontiguous image offsets. The listing's DSK field
locates its first byte; the model's per-byte origins establish the remainder.

The row-high table ends at `$097F`. Reflection accesses use nominal base `$0900`
but force X bit 7, so only `$0980–$09FF` is the used reflection table.

## Reproduction

From the repository root:

~~~sh
python3 research/analyses/karateka/tools/inspect_disk.py --extract
python3 research/analyses/karateka/tools/verify_analysis.py
python3 research/analyses/karateka/tools/inspect_disk.py --initial --disassemble 2100 2169
python3 research/analyses/karateka/tools/inspect_disk.py --disassemble 1A84 1AEA
~~~

The inspector uses the repository's previously reviewed NMOS decoder in
`research/analyses/laigle-dor/tools/inspect_tape.py` by importing definitions;
its CLI is not invoked. Tools need only Python's standard library. They do not
run historical code, ROM routines, disk firmware or build scripts.

The runtime model represents known copies/clears and original-byte provenance,
not CPU execution. Initial core loading overwrites `$0800`, so the selected
boot listing uses a separate boot-only memory model. `$B715` has different
initial/runtime contents. Dynamic operand/opcode changes, actor writes, CPU
flags, stack, interrupts, later disk loads and video/audio output are unmodeled.
Captured binary operands are therefore not a live memory snapshot after all patches.

Linear listing spans can include embedded data or extend through an instruction
starting at the selected endpoint. Unknown NMOS opcodes decode as `.byte`; their
appearance in a listing is not proof of undocumented instructions in executed code.
The source contains no original labels or assembler dialect information.

Verification writes [verification.json](../verification.json) and checks static
bytes/models. Model tests are not an emulator trace, benchmark or whole-game
correctness proof. See [overview](../overview.md) and [open findings](../findings.md).

