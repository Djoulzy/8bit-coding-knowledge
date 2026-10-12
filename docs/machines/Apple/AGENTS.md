# Apple II Programming Knowledge

## Scope

Document programming techniques for:

- Apple II
- Apple II Plus
- Apple IIe, distinguishing enhancement status
- Apple IIc

Identify the actual CPU variant for each target.
For NMOS 6502 code, apply the general CPU guidelines from:

[docs/cpu/6502/AGENTS.md](../../cpu/6502/AGENTS.md)

Treat 65C02 and other processor variants separately.
Do not transfer claims to Apple III, Macintosh, clones or
Apple IIgs native-mode code without separate evidence.

Apply the repository [AGENTS.md](../../../AGENTS.md) and more specific
machine instructions when present. These brand-level rules apply to
Apple source analyses and `docs/machines/Apple/<machine>/`, including
`docs/machines/Apple/Apple IIe/`. Preserve existing directory names.
This file is not a machine registration or a hardware profile.

## Machine Identification

For every analyzed program, identify when possible:

- Target model, enhancement status and motherboard revision.
- CPU variant and instruction set used.
- Main RAM, auxiliary RAM, language card and other expansions.
- ROM version and BASIC environment.
- Video mode, video standard and output device.
- Storage system, controller firmware, slot and drive configuration.
- Operating system, boot environment and required expansion cards.
- Accelerator or emulator settings affecting timing.
- Source edition, including cracks, conversions and modifications.

Do not assume full compatibility between Apple II models.
A folder name or a ROM-byte test alone does not establish
the complete machine configuration.

## Hardware Architecture

Investigate interactions with:

- CPU and model-specific instruction compatibility.
- Video hardware and display soft switches.
- Main/auxiliary memory selection and language-card mapping.
- Speaker and sound expansion cards when present.
- Keyboard, buttons, paddles and joystick interfaces.
- Disk controller, slot firmware and custom boot loaders.
- System ROM and operating-system services.

For input code, document strobe handling, polling loops,
measurement ranges, firmware dependencies and side effects.

For disk images, verify format and sector ordering rather than
trusting filename extensions. Distinguish filesystem files from
direct-sector data, and host offsets from loaded CPU addresses.
Examine controller polling, retries and protection-related code.

## Memory Management

Analyze:

- Zero-page and stack usage.
- Firmware and operating-system workspace ownership.
- Main and auxiliary RAM selection.
- Language-card memory, ROM overlays and slot firmware.
- Text and graphics page layouts.
- Memory used by storage software and loaded modules.
- Writable code, patch sites, relocation and aliasing.

For each accessed soft switch, verify its hexadecimal address,
supported models, read/write side effects and required state.
Check interactions among `80STORE`, `RAMRD`, `RAMWRT`, `ALTZP`,
`PAGE2` and video controls where applicable.

Memory availability depends on switch state, video mode,
firmware and machine configuration. Document initialization
and restoration across mode changes and ROM/OS calls.
Do not assume that unused-looking addresses are safe for application use.

## Graphics

Pay particular attention to:

- TEXT, lores, HGR and double-resolution modes where supported.
- Non-linear screen addressing and scanline generation.
- Pixel packing, bit order and non-pixel bits.
- HGR byte alignment, pixel phase and composite-color behavior.
- Monochrome, composite and emulator output differences.
- Mixed modes, active display pages and memory banking.
- Software sprites, masking, shifts, clipping and edge spill.
- Saved backgrounds, dirty-region redraw and overlap ordering.
- Page flipping, offscreen drawing and scrolling.
- Rendering synchronization and model-specific status signals.

Do not infer double-HGR or auxiliary-memory use from the model alone.
Distinguish saved-baseline pages from alternating frame buffers.
Verify banking controls and compare bytes with rendered output;
bitwise correctness alone does not prove correct colors or restoration.

## Audio

Investigate:

- Speaker access and transition timing.
- Software sound synthesis and sound effects.
- Expansion-card audio when present.
- Interrupt interactions and CPU usage.
- Sound loops that also regulate gameplay speed.

State instruction-count assumptions, CPU speed and interrupt
effects before estimating frequency. Report audible quality
and measured timing only with test evidence.

## System ROM

Identify monitor, BASIC, slot-ROM, DOS/RWTS and ProDOS
interfaces used by programs.

Document:

- Entry addresses and supported firmware/OS revisions.
- Calling conventions, inputs, outputs and error behavior.
- Register, flag and stack effects.
- Workspace, bank selection and interrupt-state side effects.
- Preconditions and ROM-version dependencies.

Distinguish documented interfaces from private binary entries.
Never assume a ROM routine, slot number or scratch address
is compatible between machine versions without verification.

## Interrupts and Timing

Analyze:

- IRQ/NMI sources, handlers and ownership.
- Timing-sensitive loops and accelerator effects.
- Interaction with firmware and peripheral routines.
- Rendering, audio and input synchronization.

Boot-time `SEI` does not prove uninterrupted runtime execution.
Busy waits do not establish video synchronization.
Distinguish verified hardware timing from approximate software timing.

## Optimization

Look for techniques that exploit Apple-specific hardware behavior.

Apply CPU rules to flags, decimal mode, branches, page crossings
and stack manipulation. For self-modifying code, verify writable
locations, initialization, relocation and concurrent-execution exclusion.
Trace exact caller/stack contracts for inline streams and return-address changes.

Record new discoveries under `research/` first.
When sufficiently supported for promotion, place general techniques
in `docs/common/`, CPU techniques in `docs/cpu/<cpu>/`, and Apple
hardware techniques in the resolved `docs/machines/Apple/<machine>/`.
Cross-reference these levels instead of duplicating them.

## Validation

Prefer model-specific Apple technical references, schematics,
firmware listings and reproducible emulator tests.

State explicitly whether behavior was:

- Verified against documentation.
- Observed in an emulator.
- Measured on real hardware.
- Inferred from source code or a functional model.

Do not assume emulator behavior is identical to real hardware.
Use the root validation statuses and scope recommendations to the
verified model, ROM, memory, video and peripheral configuration.
Preserve historical inputs unchanged; store extractions and annotations
under `research/analyses/`. Do not attribute a patch to the original
author without provenance evidence. Report unresolved questions and
required tests; keep unsupported recommendations as candidates.
