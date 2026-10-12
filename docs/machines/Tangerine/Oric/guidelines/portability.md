---
record_type: machine-topic-guide
topic: portability
machines: ["oric-1", "oric-atmos"]
cpu: ["6502"]
status: evidence-profile
review_date: "2026-10-11"
---

# Porting software to Oric-1 and Oric Atmos

Portability here means preserving behavior under an explicitly selected Oric
hardware, ROM and peripheral profile. A shared NMOS 6502 does not make memory,
display, firmware or I/O assumptions portable.

## Evidence profiles

| Program | Supported/observed profile | Evidence strength | Compatibility boundary |
| --- | --- | --- | --- |
| *L'Aigle d'Or* | 48 KiB; the analysis records an Oric-1 metadata label; tape; BASIC/ROM graphics, input, timers and sound; intended ROM-call adaptation | Static TAP/BASIC/machine-code analysis; functional models; draft dossier; original metadata file currently absent | Exact Oric-1/Atmos ROM binaries were not executed; the one-byte ROM patch is not a complete model adapter |
| *Space: 1999* | Atmos required; 48 KiB base RAM; Microdisc-compatible overlay RAM; private IRQ; HIRES; VIA/AY/keyboard/direct sectors | Complete source analysis at a pinned revision plus exact map/grammar disk matches | Full French executable identity, controller model, ROM `$EB7E` and all I/O failure paths remain unresolved |
| Vip4 / Quintessential | NMOS 6502 code; Oric display; Microdisc-compatible registers; writable upper RAM; direct AY/VIA and multiple IRQ regimes; current metadata labels Atmos | Static binary analysis and CRC/arithmetic/state models; draft dossier; current model label is metadata-only | Exact release, binary-to-model compatibility, ROM, inherited flags and runtime paths are unknown |

Sources: [L'Aigle d'Or overview](../../../../../research/analyses/laigle-dor/overview.md),
[Space: 1999 overview](../../../../../research/analyses/space-1999/overview.md),
[Vip4 overview](../../../../../research/analyses/vip4-demo/overview.md).

The current [Vip4 metadata](<../../../../../research/sources/Oric/Vip4 Demo/metadata.md>)
names Atmos and disk media; this differs from the stale conflicting metadata
described in its analysis. The image SHA-256 still matches that dossier.
The current label does not establish runtime compatibility. L'Aigle d'Or's
missing metadata is a provenance gap, not a reason to rewrite its historical
image or treat its intended ROM adaptation as validated.

## Cross-platform research boundary

Two Apple II dossiers were reviewed in this update without registering an Apple
machine or certifying an Apple-to-Oric port:

| Source | Transfer candidates examined | Boundary / required experiment |
| --- | --- | --- |
| [Lode Runner](../../../../../research/analyses/lode-runner/overview.md) | `GEN-0005` actor quotas, `CPU6502-0007` inline JSR parameters, semantic grids and persistent terrain comparison | Exact Apple CPU/ROM/edition and some loader paths remain unresolved; only general/CPU mechanisms are candidates, with new Oric scratch, stack and callback contracts |
| [Karateka](../../../../../research/analyses/karateka/overview.md) | `GEN-0006` actor work window; additional equal-width patches, retained animation cursors and page-repair evidence | Static local checks do not establish complete execution; Oric ownership, copy/commit, clipping and attribute behavior require separate tests |

The new candidate references are detailed in
[CPU and memory](cpu-and-memory.md#candidates-requiring-validation) and
[graphics](graphics.md#candidates-requiring-validation). Their status remains
`analyzed`; there is no Oric benchmark or hardware confirmation for these
transfers. Apple-specific `APPLE2-0001` through `APPLE2-0003` are not Oric
recommendations: seven-pixel HGR packing, page/bank controls, ROM calls, input,
speaker and disk interfaces need target-specific replacements, not base-address
substitution. The three existing validated general/CPU contracts keep their
original scope.

## Establish the target profile first

**Recommendation:** Before adapting code, record:

- exact model and ROM checksum/revision;
- NMOS 6502 or any replacement CPU, including timing/decimal/interrupt behavior;
- RAM size and which ROM/overlay windows are visible and writable;
- TEXT/HIRES mode, charset selection, bottom text rows and attribute layout;
- tape, Microdisc-compatible controller or another disk interface;
- whether BASIC, ROM, DOS, keyboard and sound services remain active;
- VIA timer/PCR/port ownership, AY shadow state and every IRQ/NMI source;
- assembler/linker dialect, load format, fixed addresses and self-modifying code;
- emulator version/configuration and real-hardware configuration.

This information is a prerequisite, not documentation to reconstruct after a
port works accidentally.

## CPU and calling contracts

- Restrict source instructions to the documented NMOS 6502 set unless the
  chosen replacement CPU is an explicit target. Recalculate instruction and
  bus behavior rather than assuming 65C02 equivalence.
- Document A/X/Y, status flags, decimal mode, stack depth, zero-page pointers
  and self-modified operands at every assembly boundary.
- Preserve the complete caller contract when replacing a tail `JMP`, ROM call,
  IRQ/RTI path or nonlocal stack escape. A routine's opcode semantics do not
  establish its surrounding firmware/device contract.
- Reallocate every historical zero-page address. *L'Aigle d'Or* coexists with
  interpreter services; *Space: 1999* and Vip4 take over regions more
  aggressively. None supplies a universal free-memory map.

Validated CPU mechanisms and candidate risks are detailed in
[cpu-and-memory.md](cpu-and-memory.md).

## Video and memory adaptation

- Convert coordinates to the selected Oric mode with explicit bounds. Ordinary
  HIRES pixel addressing is based on 40 bytes per row and six pixel bits per
  graphic byte, but in-band attributes are part of the same stream.
- Keep attribute/control cells out of generic pixel Boolean operations unless
  the transformation defines their exact encoding and propagation.
- Track TEXT, HIRES and charset overlaps by phase. Do not count visible memory,
  font memory and an overlay buffer as simultaneously free.
- Choose saved backgrounds, scene recomposition, charset animation or full
  redraw only after correctness and capacity tests. Their historical evidence
  is analyzed, not a validated performance ranking.

See [graphics.md](graphics.md).

## ROM and firmware adaptation

- Put every ROM entry point behind a model/revision-specific adapter. Record
  inputs, outputs, clobbers, workspace, display state and interrupt assumptions.
- A byte test such as the historical `$FFF9` check is evidence for one program,
  not a complete identification API.
- If retaining BASIC/ROM sound, keyboard or timer services, reserve their low
  memory and VIA/AY state. If replacing them, define startup, restoration and
  failure/reset behavior explicitly.
- Do not assume an Atmos-only reboot/ROM entry or upper-RAM mapping exists on
  Oric-1 merely because the CPU code is otherwise compatible.

## Storage, audio, input and interrupts

- Tape and direct-sector disk code have different firmware, timing, workspace
  and error contracts. A Microdisc register map does not establish Jasmin,
  Pravetz or other interface compatibility.
- Validate overlay selection and writable vectors before installing an IRQ.
  Record every VIA and controller source that can enter it.
- AY-3-8912 access and keyboard scanning share VIA/PSG wiring. Preserve port
  directions, PCR transitions, row/column state and required settling time when
  changing the audio or input path.
- Do not derive an IRQ/audio frequency solely from a Timer 1 latch constant.
  Counter state, ACR mode, reload timing, interrupt latency and hardware revision
  are part of the measurement.
- Changed-register AY shadows can reduce writes, but side-effectful operations
  such as envelope retriggering need their own correctness rules.
- Prefer normal RTI plus explicit completion/error state unless a nonlocal IRQ
  return has a fully audited stack and recovery contract.

Evidence and open risks are in the
[Space: 1999 hardware report](../../../../../research/analyses/space-1999/hardware-techniques.md)
and [Vip4 hardware report](../../../../../research/analyses/vip4-demo/hardware-techniques.md).

## Minimum porting test matrix

1. **Startup:** cold and warm start on every supported ROM/model; verify D, I,
   stack pointer, overlay state and all vectors before the first subsystem call.
2. **Memory:** assert every loaded/cleared/copied range, alias and phase change;
   fill guard bytes around low-memory, screen, charset and overlay allocations.
3. **Graphics:** render reference scenes at edges, across attributes and through
   all animation/overlap orders; compare bytes and captured output.
4. **Input/audio:** exercise all keys during silence, music and effects; log
   VIA/AY writes and IRQ latency without assuming emulator timing is hardware.
5. **Storage:** test success, retry exhaustion, missing/write-protected media,
   sector boundaries and recovery after partial operations.
6. **Interrupts:** inject every enabled source at each critical call/patch/vector
   transition; measure stack high-water use and verify foreground state.
7. **Performance:** only after output equivalence, record code/table/RAM size and
   elapsed cycles with page alignments, branch outcomes and interrupt conditions.
8. **Hardware:** repeat timing- and bus-sensitive cases on real hardware; retain
   emulator results as a separate evidence class.

## Known unresolved risks

- Exact Oric-1/Atmos ROM-call equivalence in *L'Aigle d'Or*.
- Full linked-binary correspondence and all error paths for *Space: 1999*.
- Exact Vip4 release/model, inherited carry/decimal state, IRQ-vector transitions
  and upper-memory/charset bank contents.
- Attribute-safe overlap/clipping for both save-under and dirty recomposition.
- Comparative timing for all Oric-specific rendering candidates.
- Real-hardware validation for every machine-specific candidate in this guide.

Until these are resolved, keep the affected code behind configuration checks or
explicit experimental build options rather than presenting it as general Oric
support.
