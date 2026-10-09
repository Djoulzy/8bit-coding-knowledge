# MOS 6502 Programming Knowledge

## Scope

This directory documents the original NMOS MOS 6502
CPU architecture and programming techniques.

Machine-specific behavior belongs in docs/machines/.

## CPU Architecture

When analyzing 6502 assembly, consider:

- Accumulator and X/Y register usage.
- Status flags and flag dependencies.
- Zero-page addressing.
- Indexed and indirect addressing.
- Stack organization.
- Interrupt handling.
- Branching and page boundaries.
- Binary and decimal arithmetic.
- Instruction timing.
- Memory access patterns.

## Optimization Analysis

Pay particular attention to:

### Instruction Selection

- Instruction byte size.
- Execution cycle count.
- Addressing mode overhead.
- Page-crossing penalties.
- Branch timing.
- Register preservation costs.

### Zero Page

- Efficient zero-page allocation.
- Zero-page pointers.
- Indirect indexed addressing.
- Reuse of temporary variables.
- Conflicts with operating system usage.

### Algorithms

- Fast memory copying.
- Memory initialization.
- Arithmetic using shifts and additions.
- Fixed-point calculations.
- Lookup tables.
- Optimized iteration.
- Bit manipulation.
- Data compression and decompression.

### Advanced Techniques

Investigate when present:

- Self-modifying code.
- Unrolled loops.
- Jump tables.
- Carry flag reuse.
- Stack-based techniques.
- Page-aligned data and code.
- Undocumented NMOS 6502 opcodes.

Treat undocumented instructions as non-portable.

## Cycle Counting

When analyzing performance:

1. Calculate instruction cycles accurately.
2. Account for taken branches.
3. Account for page crossing.
4. Consider interrupt interference.
5. Include memory and alignment assumptions.
6. Distinguish theoretical timing from measurements.

Do not report a single fixed cycle count when
execution time depends on runtime conditions.

## Compatibility

Distinguish between:

- NMOS 6502
- 6502 variants
- 65C02
- Other compatible or extended processors

Do not assume that instructions from later
processors are available on the original 6502.

## Documentation

Each technique should explain:

- The original implementation.
- Why it works on the 6502.
- CPU cycles and code size when known.
- Alternative implementations.
- Portability limitations.
- Situations where the technique is beneficial.

## Priority

Favor correctness and reproducible performance
analysis over speculative optimization claims.