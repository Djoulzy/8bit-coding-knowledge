# Derived Vip4 disk evidence

These are local analytical derivatives of the original ignored disk image,
not historical source files and not a redistribution license. Original
authors' symbols and assembler/compiler syntax are unknown. All files are
regenerated without executing imported code:

```sh
python3 research/analyses/vip4-demo/tools/inspect_disk.py --extract
python3 research/analyses/vip4-demo/tools/verify_analysis.py
```

`manifest.json` records the original checksum, geometry, CRC results and exact
original DSK payload offsets for each recovered module sector. `resident.bin`
is sectors 5–12 on side 0, track 0, mapped to `$F800`. `boot-sector.bin` is the
full sector 2; `boot-relocated.bin` is its classified relocation body, mapped
to `$A7D0`. `module-NN.bin` names an analytical descriptor index, not a recovered
filesystem filename or historical effect name. It includes final sector padding;
the original logical file length is unknown.

`descriptor-0c-prefix.bin` contains only the five pages reachable in this image
under the loader's track increment. Its next requested sector, side 0 track 42
sector 1, is absent. The remaining requested pages are not extracted by assuming
that the next image side is a valid continuation.

`*.asm.txt` are selected linear analytical listings. They do not prove every
instruction is reached. `sample-zp.asm.txt` shows the relocated IRQ instructions
and the two initialization-patched pointer bytes. `final-zp.asm.txt` relocates
the 48-byte ending IRQ body; its setup copies 56 bytes. The DSK columns refer
to the original template byte location, even for modified runtime operands.
These views must not be mistaken for exact assembled copies of the original
disk bytes. Code not included in a selected listing can be inspected with:

```sh
python3 research/analyses/vip4-demo/tools/inspect_disk.py --module 0B --disassemble 883B 88A1
python3 research/analyses/vip4-demo/tools/inspect_disk.py --disassemble FA9F FAF6
```

CLI addresses and module indices are hexadecimal. Do not disassemble a full
asset region and infer undocumented instructions or routine boundaries from
the output. No source build scripts, disk executable, emulator or hardware
were run during this analysis.
