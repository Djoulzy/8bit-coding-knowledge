# Oric Programming Knowledge

## Scope

Document programming techniques for:

- Oric-1
- Oric Atmos

The primary CPU is the NMOS 6502.

Always apply the general 6502 guidelines from:

[docs/cpu/6502/AGENTS.md](../../../cpu/6502/AGENTS.md)

Apply the repository [AGENTS.md](../../../../AGENTS.md) and optional
`docs/machines/Tangerine/AGENTS.md` as well. This machine's canonical
documentation directory is `docs/machines/Tangerine/Oric/`.

## Machine Identification

For every analyzed program, identify when possible:

- Target machine.
- RAM configuration.
- ROM version.
- Video mode.
- Storage system.
- Required hardware extensions.

Do not assume full compatibility between
Oric-1 and Oric Atmos.

## Hardware Architecture

Investigate interactions with:

- MOS 6502 CPU.
- Oric ULA video hardware.
- 6522 VIA.
- AY-3-8912 sound generator.
- Keyboard interface.
- Tape interface.
- Disk interfaces when present.
- System ROM.

## Memory Management

Analyze:

- Zero-page usage.
- System-reserved memory.
- Stack usage.
- Text-mode memory layout.
- HIRES-mode memory layout.
- Character generator memory.
- ROM and RAM boundaries.
- Memory used by storage extensions.
- Overlay RAM when available.

Memory availability depends on the video mode
and machine configuration.

Do not assume that unused-looking addresses
are safe for application use.

## Graphics

Pay particular attention to:

- TEXT mode.
- HIRES mode.
- Screen memory organization.
- Attribute-based color handling.
- Pixel encoding.
- Character sets.
- Software sprites.
- Scrolling techniques.
- Screen clearing and memory copying.
- Graphics compression.
- Rendering synchronization.

The Oric uses display attributes embedded
in video memory.

Always account for their consequences when
analyzing graphics algorithms.

## Audio

Investigate:

- AY-3-8912 register programming.
- Sound effects.
- Music playback routines.
- Interrupt-driven audio.
- Timing constraints.
- CPU usage.

## System ROM

Identify ROM routines used by programs.

Document:

- Entry addresses.
- Calling conventions.
- Register modifications.
- Side effects.
- ROM-version dependencies.

Never assume a ROM routine is compatible
between machine versions without verification.

## Interrupts and Timing

Analyze:

- IRQ handling.
- VIA timers.
- Timing-sensitive loops.
- Interaction with system routines.
- Rendering and audio synchronization.

Distinguish verified hardware timing
from approximate software timing.

## Optimization

Look for techniques that exploit
Oric-specific hardware behavior.

When a technique is purely CPU-related,
document it under docs/cpu/6502/.

When a technique relies on Oric hardware,
document it under `docs/machines/Tangerine/Oric/`.

Cross-reference both levels when necessary.

## Validation

Prefer hardware documentation and
reproducible emulator tests.

State explicitly whether behavior was:

- Verified against documentation.
- Observed in an emulator.
- Measured on real hardware.
- Inferred from source code.

Do not assume emulator behavior is
identical to real hardware.
