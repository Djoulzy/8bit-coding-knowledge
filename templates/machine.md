---
id: ""                   # e.g. oric-1, oric-atmos
name: ""
manufacturer: ""
introduced: ""           # Year or documented date
cpu: []                  # e.g. ["6502"]
variants: []             # e.g. ["Oric-1", "Oric Atmos"]
doc_status: draft         # draft | reviewed | validated
---

# Machine name

## Overview

Briefly describe the computer, supported variants, and scope of this page.
Keep CPU-wide concepts in `docs/cpu/`; this page describes hardware-specific
constraints and programming practices.

## Variants and compatibility

| Model / revision | CPU | RAM | ROM | Notable differences | Evidence |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

Do not assume identical ROM entry points or extension hardware across models.

## Core hardware

| Component | Model / details | Programming consequences | Reference |
| --- | --- | --- | --- |
| CPU | | | |
| Video | | | |
| Sound | | | |
| I/O | | | |
| Storage | | | |

## Memory map

| Start | End | Size | Purpose | Availability / caveats | Reference |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

Record hexadecimal notation consistently (for example `$A000`).
Distinguish physical addresses, ROM overlays, reserved system locations,
and memory that varies with video mode or peripherals.

### Zero-page and stack considerations

Specify reserved areas, safe application areas, interrupt use, and ROM
requirements. Mark uncertain allocations explicitly.

## Video system

### Modes and layouts

| Mode | Resolution / characters | Memory layout | Encoding / attributes | Constraints |
| --- | --- | --- | --- | --- |
| | | | | |

### Rendering implications

Describe pixel packing, attributes, screen organization, character memory,
scrolling, sprite implementation, timing, and display synchronization.
For the Oric, explain in-band video attributes and their impact on drawing.

## Audio system

Describe sound-chip access, register programming, timing and CPU trade-offs.

## Input / output and peripheral interfaces

Describe keyboard, timers, VIA/PIA interfaces (as applicable), cassette,
disk hardware, and required initialization.

## Interrupts and timing

- IRQ/NMI sources and vectors:
- Timer behavior:
- ROM interactions:
- Display / audio synchronization:
- Known timing uncertainties:

## System ROM and firmware interfaces

| Entry / address | Function | Calling convention | Clobbered state | Variant compatibility | Source |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

Document preconditions, side effects, and ROM-version dependencies.

## Toolchains, emulators and test environment

- **Assemblers / dialects:**
- **Build tools:**
- **Emulators and debugging capabilities:**
- **Hardware test procedure:**
- **Known emulator versus hardware differences:**

## Machine-specific optimization patterns

Link to entries in `docs/machines/<machine>/techniques/` and cross-reference
CPU techniques in `docs/cpu/<cpu>/techniques/` instead of duplicating them.

| Technique ID | Applicability | Main benefit | Caveat |
| --- | --- | --- | --- |
| | | | |

## Guidelines for new projects

Document recommendations only when evidence supports them. For each guideline,
include assumptions, affected machine variants, and links to supporting
techniques or tests.

## Open questions and validation backlog

- [ ] Verify memory map using authoritative machine documentation.
- [ ] Verify ROM version differences.
- [ ] Test hardware-dependent behavior in emulator and, if possible, on device.

## References

List primary technical manuals, schematics, trusted documentation, source
programs and reproducible tests. Include dates or revisions where possible.
