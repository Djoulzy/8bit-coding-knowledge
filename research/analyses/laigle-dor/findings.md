---
id: ANALYSIS-ORIC-0001-FINDINGS
program: "L'Aigle d'Or"
cpu: ["6502"]
machines: ["oric-1", "oric-atmos"]
analysis_status: draft
source_revision: "sha256:7f01e1a3d05825aab887952cd5711bea69d6525730aba5c1e25c814334fe77d7"
analysis_date: "2026-10-09"
---

# Findings, knowledge integration and validation plan

## Interpretation of novelty and status

This document records the initial analysis. For current knowledge-base status,
see [integration-review.md](integration-review.md): GEN-0002's general principle
and C04/C06's bounded CPU algorithms now have validated canonical guidelines.
The historical Oric collision implementation and other research records retain
their analyzed status.

The repository initially contained instructions and templates, but no technique
records or validated guidelines in `docs/common/`, `docs/cpu/6502/` or the actual
Oric directory. There were no earlier analyses or findings to compare against.
Thus **no existing repository technique is confirmed**, and no existing
guideline can yet be improved by an edit. Conventional patterns can be recognized
without inventing repository references or claiming worldwide novelty.

The five standalone records below are selected for useful detail, unusual
implementation or a significant analysis lesson. Simpler familiar patterns stay
inside this dossier to avoid proliferating duplicate CPU/hardware records. All
were `analyzed` at the initial review: their mechanisms are explained from exact bytes. Intended
optimizations, complete reachability, firmware compatibility and visual behavior
remain uncertain where stated. None was `benchmarked` or `validated` at that stage.

## Selected new research records

| ID / classification | Exact source entry | Knowledge extracted / reuse judgment |
| --- | --- | --- |
| [GEN-0001](../../findings/GEN-0001-resumable-animation-streams.md), General 8-bit | B2 `$4500`, `$45AA`; BASIC 6, 5017, 5020 | Resumable draw/restore/move/event streams with two cursors. Reusable architecture after adding bounds and a per-call work budget |
| [CPU6502-0001](../../findings/CPU6502-0001-two-byte-render-patches.md), MOS 6502 | BASIC 3/4; B2 patch `$3E56` | Equal-length NOP/ORA substitutions share a byte loop. Useful where code is writable and exclusive; compare dedicated workers before reuse |
| [ORIC-0001](../../findings/ORIC-0001-background-pages-with-position-metadata.md), Oric-specific implementation | B2 `$4140`, `$3ECF`, `$4574`, `$4840` | Saved-background page contains pixel bytes and its restoration coordinates. Reusable for bounded layers; screen attributes and ownership constrain it |
| [GEN-0002](../../findings/GEN-0002-semantic-collision-grid.md), General 8-bit | BASIC 5, 600–940; B2 `$4B82`, `$4CB6` | Separate 120-byte semantic grid. Reusable principle; original three-row perspective mapping and result anomalies are game-specific |
| [CPU6502-0002](../../findings/CPU6502-0002-rts-in-basic-line-header.md), MOS 6502 | BASIC 8205; B2 `$2283` | Existing line-number byte doubles as RTS. Important exact-byte analysis lesson; fragile, no recommendation to reproduce it |

Routine names in these records are analytical, not recovered symbols. Source
addresses resolve to original TAP offsets by [the overview mapping](overview.md#precise-reference-convention).
The original download origin and assembler dialect remain unknown.

## Other significant techniques retained in the dossier

Each entry below links to its mechanism, possible motivation, costs, constraints
and alternatives. These are new **local observations** of established patterns,
not additional unique finding IDs.

| Finding / classification | Source / detailed explanation | Status and reuse |
| --- | --- | --- |
| BASIC controller with machine workers — General 8-bit | BASIC 4000–5990; [architecture](architecture.md#execution-graph) | `analyzed`; separates complex rules from byte-intensive work; CALL/POKE overhead and shared ABI limit speed/reentrancy |
| Fixed memory and phase-dependent ownership — General 8-bit | BASIC HIMEM/VARTAB, [memory ledger](architecture.md#runtime-ownership-and-allocations) | `analyzed`; useful lifetime planning, but exact RAM addresses and heap size are not portable |
| Two four-byte records per room — General 8-bit | B2 `$5000/$5100`, `$3F14`; [packed rooms](architecture.md#packed-room-data) | `analyzed`; 64 rooms fit 512 bytes; fixed field widths limit content and make mutation masks important |
| Replay from a preserved room snapshot — General 8-bit | `$5600–$57FF` → `$5000–$51FF`, `$4DDD` | `analyzed`; fast simple reset at 512-byte backup cost; suitable for small mutable worlds |
| Zero-page pointer arguments — MOS 6502 | `$3E3B–$3E77`; [C01](cpu-techniques.md#c01-zero-page-parameter-blocks-and-register-roles) | `analyzed`; compact indirect indexing, destructive arguments; firmware ownership must be checked |
| Four aligned descriptor field pages — MOS 6502 | `$9400–$97FF`, `$3E3B`; [C03](cpu-techniques.md#c03-page-aligned-field-arrays) | `analyzed`; direct byte indexing without read crossing; 1,024-byte table cost and unused entries |
| Carry-stream field extraction — MOS 6502 | `$3F0B`, `$3F14`; [C04](cpu-techniques.md#c04-carry-stream-unpacking) | `analyzed`; preserves record index X; destructive source and call overhead need comparison with masking |
| Shift/add byte multiplication — MOS 6502 | `$3E00`; [C05](cpu-techniques.md#c05-general-multiplication-used-for-a-constant-stride) | `analyzed`; reusable unsigned multiplication with D clear; generic implementation may be costly for constant 40 |
| Bounded carry reuse / A:Y arithmetic — MOS 6502 | `$3E21–$3E3A`; [C05](cpu-techniques.md#c05-general-multiplication-used-for-a-constant-stride) | `analyzed`; high-byte ADC provably leaves C clear for low-byte ADC after TYA; cannot be generalized to unrestricted bases |
| Countdown byte loops and full-page wrap — MOS 6502 | `$3E52`, `$4DDD`; [C06](cpu-techniques.md#c06-countdown-indexing-and-row-layout) | `analyzed`; simple traversal but zero can mean 256, and order is not overlap-safe |
| Tail-jump wrappers — MOS 6502 | `$3EBD`, `$3EC6`, `$4140`; [C08](cpu-techniques.md#c08-tail-jumps-and-unusual-machine-entry-in-basic-data) | `analyzed`; reuse worker RTS, avoid nested JSR/RTS; require compatible argument/clobber contracts |
| Sign-flag range shortcuts — MOS 6502 | `$45E1`, collision/enemy checks; [C07](cpu-techniques.md#c07-branch-flags-signed-ranges-and-suspicious-sequences) | `analyzed` byte behavior; operand bounds must justify each translation; N is not a universal comparison predicate |
| Charset loop crossing a code page — MOS 6502 | `$4F04` → `$4EFD`; [C09](cpu-techniques.md#c09-alignment-penalty-in-a-256-byte-charset-restore) | `analyzed`; explains 255 taken-branch penalties; possible improvement, not evidence of intentional alignment |
| Six-pixel byte-oriented sprites — Oric-specific | BASIC 90, `$3E21`; [H01](hardware-techniques.md#h01-byte-column-coordinates-and-six-pixel-alignment) | `analyzed`; avoids arbitrary pixel shifting; horizontal granularity and bounds constrain reuse |
| Per-row serial attribute column — Oric-specific | `$4000/$402D`; [H02](hardware-techniques.md#h02-attributes-emitted-beside-sprite-rows) | `analyzed`; compact colors with effects to the right; `$0A` stop is not proved general clipping |
| Selective charset preservation / mode overlays — Oric-specific | `$4EEA/$4EF8`; [H04](hardware-techniques.md#h04-texthires-overlays-and-charset-lifetimes) | `analyzed` byte transfers; font meanings/ROM effects uncertain; reuse requires mode/lifetime validation |
| Timer latch changes without application IRQ — Oric-specific | BASIC 3000/4000/9030; [H05](hardware-techniques.md#h05-via-latch-changes-with-the-rom-interrupt-service-retained) | `analyzed` writes, pacing intent inferred; current phase/ACR/ROM service untested |
| Firmware-controlled sound — Oric-specific | BASIC SOUND/MUSIC/PLAY paths; [H06](hardware-techniques.md#h06-ay-3-8912-effects-through-basic-firmware) | `analyzed`; less driver code but timing/interpreter overhead; no custom AY optimization found |
| ROM keyboard plus line-number table — General 8-bit dispatch / Oric input | BASIC 5050, `$4300`; [H07](hardware-techniques.md#h07-rom-input-and-two-level-key-dispatch) | `analyzed`; configurable bindings, not a machine jump table or proven constant-time BASIC dispatch |
| Conditional ROM-entry patch — Oric-specific | BASIC 42, `$4EF8`; [H08](hardware-techniques.md#h08-rom-version-adaptation-and-implicit-abi) | `analyzed` patch; intended compatibility requires both exact ROM images |
| Local hazard with two saved bytes — General 8-bit strategy / Oric pixels | `$4CDD`; [H09](hardware-techniques.md#h09-local-movement-instead-of-whole-screen-scrolling) | `analyzed`; very small save-under specialization; `$FF` appearance depends on ink/paper/inverse video |
| Backslash-terminated messages — General 8-bit | BASIC 9100–9130 | `analyzed`; no stored length required, sentinel costs scanning and cannot appear literally; CHAR is ROM-specific |

## Important limitations and apparent anomalies

- `$3EF5` jumps to an operand byte; `$4B50` has a constant comparison that makes
  one path impossible. Neither has an established live caller.
- `$4B92` stores A=`$A0` after loading X=`$02`; a nonzero collision contract may
  tolerate it, but a precise enum contract would not. Do not silently correct
  the documented behavior.
- The attribute blitter can stop partway through a row and record only fully
  completed rows. This and zero recorded height are visual/capacity test cases.
- `$5900` has sprite-buffer and charset-buffer roles. Their separation is a
  hypothesis supported by phase structure, not a traced ownership proof.
- The loader's two anomalous linked tail records, residual foreign BASIC text
  and orphan machine fragments are preserved. Their presence is not evidence
  of intentional optimizations or additional game functionality.
- No established undocumented instructions, custom IRQ audio/graphics engine,
  stack trick, arbitrary sprite shifting, full-screen scrolling or generic image
  decompressor was found. Apparent code in tables is not positive evidence.

## Potential future guideline topics

No validated document was edited. If further evidence supports promotion, create
general guidelines for bounded animation streams, semantic collision maps and
explicit ownership of saved layers; CPU guidelines for zero-page contracts,
conditional cycle accounting and writable-code patch invariants; and Oric
guidelines for serial attributes, ROM-version adapters and mode-dependent RAM.
Cross-reference the CPU mechanisms from Oric documents rather than repeating
them. Treat the RTS alias as a cautionary case, not a coding guideline.

## Reproducible checks already completed

`tools/inspect_tape.py` parses both tape blocks, verifies BASIC links, extracts
exact payloads and produces opt-in analytical listings. `tools/verify_analysis.py`
checks the image hash, extraction equality, key opcode sequences and buffer
capacity, and models all 65,536 unsigned multiplications, 8,000 visible byte
addresses and 512 carry-unpacking cases. Results are recorded in
[verification.json](verification.json).

These checks run analytical Python code, not the historical program. They do
not model ROM side effects, the ULA scan, interrupts, decimal arithmetic or
complete program execution. The cycle figures are instruction-table calculations,
not benchmark measurements. This distinction prevents promotion by arithmetic
model alone.

## Benchmark and investigation opportunities

| Priority | Question / comparison | Required method and outputs |
| --- | --- | --- |
| 1 | Does this image run on both intended models? | Identify/hash ROM 1.0/1.1 images; run both stages, record `$FFF9`, font reset call, display/input/sound and success/death/replay paths |
| 1 | Are saved layers and borrowed scratch safe? | Trace every slot/cursor/zero-page owner across drawing, ROM calls, IRQs and darkness; capture overlap/attribute frames |
| 1 | Which anomalies are live? | Breakpoints at `$2283`, `$3EF1`, `$4B50`, `$4B92`, `$4069`, `$415C`; record callers, inputs, effects and stream path |
| 2 | Multiply-by-40 alternatives | Compare original, shift/add and scanline tables with identical x/y outputs, D clear, all visible coordinates, actual code/data locations and RAM costs |
| 2 | Inline patches versus dedicated blitters | Compare identical rectangles/output bytes for opaque and OR modes; include setup and pointer crossing, exclude or separately record IRQ costs |
| 2 | Charset code alignment | Relocate restore branch in a separate experimental executable; theoretical saving is 255 cycles per 256-byte loop; verify addresses and glyph result before measuring |
| 3 | Dense versus split descriptors | Equal image capacity and lookup contract; record bytes, cycles, scratch use and indexing work |
| 3 | Animation latency / collision coverage | Traverse reachable commands and all 64 rooms/directions; record worst call latency, bounds and dynamic-map consistency |

Keep benchmarks in separate trusted harnesses under `benchmarks/` only when
actually implemented. Record emulator/version, machine/ROM hashes, interrupt
settings, inputs, code/data addresses, cycle boundaries, expected/actual output
and real-hardware differences. Do not alter the original cassette to test an
optimization; derive a clearly identified experimental image instead.

## Deliverables and preservation

The six requested English documents are [overview](overview.md),
[architecture](architecture.md), [routines](routines.md),
[CPU techniques](cpu-techniques.md), [hardware techniques](hardware-techniques.md)
and this findings synthesis. Five standalone records are linked above.

At the user's additional request, [extracted/](extracted/README.md) stores both
byte-exact payloads, standalone tape blocks, analytical BASIC listings and a
hash/offset manifest.
The original TAP and metadata remain unchanged. The tools and verification
result make narrow parts of the analysis reproducible. No build script or
historical executable was run and no validated guideline was promoted.
