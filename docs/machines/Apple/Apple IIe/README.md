---
record_type: machine-profile
id: apple-iie
name: "Apple IIe"
manufacturer: Apple
cpu: ["6502"]
cpu_scope: "Documented NMOS 6502 code; physical CPU and enhanced/65C02 configuration unverified"
registration_status: registered
doc_status: draft
review_date: "2026-10-12"
---

# Apple IIe — Research and development profile

## Identity and scope

This directory registers the explicitly requested `Apple/Apple IIe` target.
It participates in subsequent `$build-8bit-guidelines all` runs. Registration
does not certify either historical program's compatibility with every IIe.

The current corpus establishes Apple II family interfaces and documented NMOS
6502 instructions. Exact motherboard, enhancement status, physical CPU, ROM,
auxiliary-memory configuration and video standard are **Unknown — verification
needed**. The source-directory name alone is not evidence of these properties.
Treat 65C02 and other replacement processors as separate configurations.

Apply the [Apple instructions](../AGENTS.md), applicable
[6502 instructions](../../../cpu/6502/AGENTS.md), and root repository rules.

## Evidence-backed observations

These describe inspected program paths, not a complete hardware specification
or a demonstrated minimum machine configuration.

| Area | Current evidence | Limitation |
| --- | --- | --- |
| CPU | Both dossiers identify documented NMOS 6502 instructions | Physical CPU and enhanced-IIe behavior were not tested |
| Memory | Reconstructed code/data use main-RAM addresses through `$BFFF` | Whole-game minimum RAM, auxiliary RAM and language-card requirements are not established |
| Video | Ordinary HGR paths use `$2000–$3FFF` and `$4000–$5FFF` | Actual IIe bank state and displayed artifact colors remain untraced; no double-HGR renderer was established |
| Firmware/input/audio | Monitor or DOS-style services, keyboard, buttons/paddles and foreground speaker access occur | Exact firmware, slot configuration, calibrated input and sound timing remain unverified |
| Storage | Two sector images with different reconstructed loading arrangements | Neither filename nor sector geometry authenticates an original release or physical protection scheme |

The corresponding source locations and assumptions are in
[Lode Runner's target environment](../../../../research/analyses/lode-runner/overview.md#3-target-environment)
and [Karateka's target environment](../../../../research/analyses/karateka/overview.md#3-target-environment).

## Historical inputs and analyses

| Program / attribution recorded in analysis | Historical input | Dossier / edition limit |
| --- | --- | --- |
| Lode Runner — Doug Smith / Brøderbund | [Supplied disk](<../../../../research/sources/Apple IIe/Lode Runner/Lode Runner (1983)(broderbund)[cr].dsk>) | [Overview](../../../../research/analyses/lode-runner/overview.md); local cracked edition, original-release equivalence unknown |
| Karateka — Jordan Mechner / Broderbund | [Supplied disk](<../../../../research/sources/Apple IIe/Karateka/Karateka (1984)(Broderbund).dsk>) | [Overview](../../../../research/analyses/karateka/overview.md); exact disk/loader edition unknown |

The dossiers contain input SHA-256 values, precise disk offsets, phase-specific
CPU addresses and derived listings. Original symbols and assembler dialects
are unavailable. No historical code was executed in those investigations;
static byte checks and translated models are not execution benchmarks.
No source redistribution license has been established.

## Applicable guidance

- [Development best practices](BEST-PRACTICES.md): scoped entrypoint and candidate index.
- [CPU and memory](guidelines/cpu-and-memory.md): existing validated CPU contracts and Apple allocation constraints.
- [Graphics](guidelines/graphics.md): validated logical collision separation and unvalidated renderer comparisons.
- [Portability](guidelines/portability.md): configuration boundaries and test matrix.

The three reused validated records are
[GEN-0002](../../../common/semantic-collision-grid.md),
[CPU6502-0003](../../../cpu/6502/carry-stream-field-extraction.md), and
[CPU6502-0004](../../../cpu/6502/descending-page-copy.md). Their original
applicability limits remain unchanged. Apple-specific discoveries remain
`analyzed`; no IIe renderer, audio or disk implementation is promoted here.

## Open verification tasks

- [ ] Record an exact target CPU, motherboard/ROM checksum, memory expansions,
  video output/standard, disk interface and emulator/hardware configuration.
- [ ] Trace boot and one gameplay exchange from each pinned disk, including
  relocation, bank/page state, zero-page/stack ownership and ROM calls.
- [ ] Resolve Lode Runner's first-level I/O vector and captured out-of-domain
  data; resolve Karateka's later disk/overlay path before claiming full support.
- [ ] Compare renderer output across phases, reflection, edges and overlaps;
  test bit-7/color behavior separately from pixel arithmetic.
- [ ] Benchmark equivalent complete workloads only after output and ownership
  checks pass; retain real-hardware results separately from emulation.

The next useful investigation is a bounded startup/gameplay trace on a named
IIe configuration, not a further automatic promotion of static findings.
