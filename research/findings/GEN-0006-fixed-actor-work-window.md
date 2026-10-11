---
id: "GEN-0006"
title: "Load actor records into a fixed work window for shared routines"
category: "memory"
cpu: ["6502"]
machines: ["apple-iie"]
status: analyzed
source_analyses: ["../analyses/karateka/overview.md"]
tags: ["actor-state", "zero-page", "record-copy", "cooperative-update"]
---

# Load actor records into a fixed work window

## Summary

Copy a selected actor's persistent record into fixed workspace addresses, run
shared routines against those fields, then commit the result. Karateka uses
two 16-byte records and a 16-byte zero-page work window. The organization is
general; direct zero-page access is a CPU-specific benefit of this implementation.

## Problem and context

- **Problem:** reuse animation/decision/drawing routines for two actors without
  passing a record-base index through every field access.
- **Use cases:** a small set of actors updated cooperatively, with substantial
  processing between record transfers and a stable compact field layout.
- **Preconditions:** disjoint source/work records, explicit load/process/commit
  lifetime, exclusive work-window ownership and sufficient scratch memory.
- **Applicability:** common organization; inspected instance uses documented
  NMOS 6502 instructions on the supplied Apple II/IIe-targeted disk. Exact CPU,
  ROM and disk edition, and other processor/machine implementations are untested.

## Provenance

| Field | Value |
| --- | --- |
| Original program | Karateka; supplied 1984/Broderbund-marked image |
| Author / publisher | Jordan Mechner / Broderbund; individual routine authorship unknown |
| Archive / license | Download provenance and license grant unknown |
| Original file | [Karateka (1984)(Broderbund).dsk](<../sources/Apple IIe/Karateka/Karateka (1984)(Broderbund).dsk>) |
| Repository baseline | `d02edc77fa0a02d3f679af22456ca1c762c305dc` |
| Disk SHA-256 | `4399db1c5469299f6a519abd890456ba1bbba70596d72096f1db4a84e5669370` |
| Routine / byte location | Runtime `$7071–$70A5`, `DSK=$004871–$0048A5`; caller `$B584–$B591`, `DSK=$008D84–$008D91` |
| Source lines / symbols | Unavailable: binary-only input; analyst descriptions and phase-specific CPU addresses |
| First analysis | [Karateka overview](../analyses/karateka/overview.md) |

The [author's account](https://www.jordanmechner.com/en/games-movies/karateka/)
supports author, Apple II origin and publisher identity; it does not authenticate
this particular image. [Selected listing](../analyses/karateka/extracted/selected-disassembly.txt)
maps observed instructions back to the pinned disk.

## Original implementation

Original assembler dialect and labels are unknown. Instruction behavior is
summarized instead of presenting reconstructed names as historical source:

| Public interface / worker | Copy direction | Tail |
| --- | --- | --- |
| `$7009 → $707D` | `$70–$7F → $20–$2F` | Classify actor at `$60`, update `$32/$33` |
| `$7006 → $7071` | `$20–$2F → $70–$7F` | RTS |
| `$700F → $7099` | `$60–$6F → $20–$2F` | Classify actor at `$70`, update `$32/$33` |
| `$700C → $708D` | `$20–$2F → $60–$6F` | RTS |

Each copy initializes X to zero, uses LDA zp,X / STA zp,X, increments X,
compares it with `$10` and repeats until all 16 bytes are copied.

## Technical explanation

The ordinary second-actor update calls load `$7009`, decision `$6B00`, sequence
update `$6400` and commit `$7006`. The first-actor worker `$B69A` loads `$700F`,
selects/updates a sequence and eventually jumps to commit `$700C`. Drawing also
loads the records into the same work addresses. This is one cooperative workspace,
not an interrupt scheduler or a full CPU context save.

The sequence updater directly accesses frame fields `$20/$21`, position `$22`,
cursors `$25/$26`, steps `$27/$28` and facing `$2C`. Keeping these addresses
fixed makes actor selection independent of most individual field instructions.
Other global context is derived by load tails; the 16-byte record is not the
entire actor/world state.

An analyst-written abstract model is:

~~~text
work[0..15] = actor[selected][0..15]
derive_other_actor_context()
update_sequence_and_action(work, globals)
actor[selected][0..15] = work[0..15]
~~~

Changes before commit are unpublished. Nested selection or rendering that
loads another actor midway can overwrite the work record. The caller must
also decide whether a read-only draw should commit modified scratch fields;
the observed interfaces do not automatically enforce that policy.

## CPU-specific considerations

- **Registers/flags:** copy uses/clobbers A and X; INX/CPX establish termination.
  It is not a register/processor-status preservation facility.
- **Addressing:** zp,X transfers, direct zp accesses in consumers. Record
  ranges do not wrap around `$FF`; fixed work addresses simplify X/Y allocation.
- **Compatibility:** only documented NMOS instructions in this loop. No
  65C02-only optimization or tested cross-CPU binary portability is claimed.
- **Branches/interrupts:** all copy-loop branches stay within page `$70`.
  Reentry or an interrupt using the same window requires an explicit protocol.
- **Alignment:** these specific records are in ZP. On another CPU or larger
  program, a fixed RAM buffer can preserve the organization with different costs.

## Machine-specific considerations

No video device is required by the pattern. This instance owns addresses normally
usable as Apple firmware workspace; it does not establish safe coexistence with
arbitrary ROM calls, extensions or an operating system. Check ZP/stack ownership
for the actual environment. Actor coordinates and frame IDs connect to the
machine renderer, but record copying itself is separate from HGR encoding.

## Performance and resource costs

| Metric | Original instance | Alternative / method |
| --- | --- | --- |
| Persistent record RAM | 2 × 16 = 32 ZP bytes | Retained records still needed for indexed access |
| Work window | 16 additional ZP bytes | Indexed/indirect fields may avoid this copy buffer |
| Copy core | 241 calculated cycles | 2 + 16 × 12 + 15 × 3 + 2; no IRQ, same-page branch |
| Commit with RTS / caller JSR | 247 / 253 calculated cycles | Load tails add classification/distance; exclude them from this fixed number |
| Commit worker code | 12 bytes each | Inclusive `$7071–$707C` and `$708D–$7098`; interfaces/tails excluded |
| Consumer field access | Direct zp load/store 3 cycles | zp,X 4; indirect alternatives depend on indexing/pages |
| ROM / total engine cost | Not determined; no ROM call in copy core | Whole update/draw and other global context excluded |

These are instruction-table calculations using the
[MOS summary](https://ftpmirror.your.org/pub/misc/bitsavers/components/mosTechnology/6502_Instruction_Set_Summary.pdf),
not measurements. Load+commit incurs at least 482 copy-core cycles plus calls,
returns and load-tail work. A one-cycle-per-field-access saving alone needs many
accesses to repay that cost; register/setup simplification can matter too.

## Advantages

- Shared routines see a stable compact field layout.
- Actor-base bookkeeping is concentrated in load/commit helpers.
- Direct addresses leave index registers available for frames, streams and tables.

## Limitations and risks

- Extra ZP storage and copy traffic can outweigh cheaper field access.
- A forgotten commit loses changes; a second load destroys unpublished work.
- Shared globals and derived context remain outside the record.
- Nested updates, IRQ users and ROM scratch ownership must be defined explicitly.

## Alternatives

Index records directly, use an indirect record pointer, split fields into
parallel arrays, or specialize the hottest actor routines. Compare complete
caller cost and register pressure, not just the copy loop or one field access.

## Validation record

- **Current status:** analyzed, provisional.
- **Source evidence:** four exact 16-byte loops, load tails, update callers and
  fixed-address animation consumers.
- **Theoretical checks:** byte bounds/disjoint records and conditional cycle sum.
- **Reproducer:** `python3 research/analyses/karateka/tools/verify_analysis.py`;
  [results](../analyses/karateka/verification.json).
- **Benchmark / hardware:** none. Static loop assertions are not a measured benchmark.
- **Outstanding:** trace commits, all modified fields/global tails, nested/IRQ
  ownership and complete copied-window versus indexed-record workloads.

## Recommendation for new projects

Consider a fixed work window when complex shared routines use many fields and
index registers are scarce. Prefer direct indexed records for short/simple
updates or concurrent actors. Define the copy/commit contract, own the workspace
and compare real workloads before adopting it as an optimization.

## References and related techniques

- [Architecture](../analyses/karateka/architecture.md),
  [CPU analysis C01](../analyses/karateka/cpu-techniques.md#c01-fixed-actor-fields-through-a-copied-work-record).
- [GEN-0001](GEN-0001-resumable-animation-streams.md), retained sequence state,
  a consumer pattern rather than a record-selection mechanism.
- [CPU6502-0005](CPU6502-0005-zero-page-code-operands-as-state.md), distinct use
  of zero-page instruction bytes as state, not this copied data window.

