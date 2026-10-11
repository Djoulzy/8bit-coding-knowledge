# Evidence-to-guidelines synthesis workflow

This reference is operational guidance for Codex working **inside the user's local repository**. It must inspect the actual repository, not assume the example paths have files. Resolve `docs/machines/<brand>/<machine>/` before selecting documents or writing. Only explicit `add <brand>/<machine>` permits registering a missing leaf; `discover` is read-only.

## A. Read and normalize findings

Search `research/analyses/` and `research/findings/` plus relevant `docs/`, including legacy analysis formats. Use frontmatter when available, but confirm its claims from the body and linked source. Preserve original IDs such as `CPU6502-0001`, `ORIC-0001`, and `GEN-0001`; never mint a new technique ID merely to republish an existing finding.

Record privately for each candidate:

| Field | What to check |
| --- | --- |
| Claim | Exact technique and use case, not a broad slogan |
| Scope | General 8-bit / CPU family / machine variant |
| Source | Analysis path, originating code file and line or symbol |
| Status | observed / analyzed / benchmarked / validated |
| Support | Theoretical proof, hardware manual, reproducible benchmark, tests |
| Trade-offs | Code bytes, RAM, cycles, complexity, compatibility |
| Conflicts | Competing recommendations and context differences |
| Destination | Link-only / best practice / provisional candidate / excluded |

An analysis that mentions `oric` in text is not automatically Oric-compatible. Establish the target and the CPU variant explicitly. Source program authorship, dates, licenses, and ROM addresses must never be invented.

## B. Promotion thresholds

- **observed**: Historical implementation exists; no universal recommendation follows. Store as candidate only if it teaches a useful hypothesis.
- **analyzed**: The mechanism is technically understood, but benefit and suitability may remain conditional. Document as candidate with test prerequisites, unless separate validated evidence exists.
- **benchmarked**: A measured comparison exists; verify workload, alignments, hardware/emulator, program versions, and reproducibility. Benchmark alone does not prove portability or justify unqualified advice.
- **validated**: Support is adequate for a **particular CPU/machine configuration and objective**. May become normative only within its proven conditions; cite evidence and trade-offs. Reassess stale 'validated' tags if the linked proof is absent.

Hardware facts verified in authoritative hardware docs may become **constraints** ('screen attribute bytes must be handled') even when they are not a benchmarked optimization. Keep them distinct from claims that an algorithm performs better.

When multiple sources disagree, avoid majority voting: compare preconditions and evidence, express the conditional result, or defer. Clearly report missing experiments rather than fabricate validations.

## C. Cross-platform transfer rules

1. A technique is placed in `docs/common/` only if platform-independent; in `docs/cpu/<cpu>/` if dictated by CPU semantics. A machine guide should link to those and add its hardware/OS constraints.
2. Never assume `6502` equals `65C02` or that all NMOS variants behave identically. Verify instructions, flags, opcode availability, timing, decimal mode and interrupt effects as applicable.
3. For an Oric target, check Oric-1 versus Atmos ROM APIs, memory layout, video attributes, I/O and peripheral state before proposing a port. Do not assume a home computer's zero-page layout equals another's.
4. Portability between 6502 machines is not guaranteed even when assembly instructions themselves are portable. Label CPU-portable versus machine-dependent code paths.
5. Treat code copied from a program as illustrative only when license and assembler dialect are known; otherwise write original pseudocode or a short independent example with attribution to evidence.

## D. Merge strategy

- Discover existing brand folders and machine leaves separately. In `add` mode only, register the explicitly named leaf without overwriting similar variants. Identify existing documentation in the **resolved** `docs/machines/<brand>/<machine>/` only; update in place, preserving technical material and manual edits. Keep filenames if they already serve the required topic.
- `BEST-PRACTICES.md`: rapid development entrypoint — scope, prerequisites, high-impact validated practices, topic navigation, quick portability checklist, research status.
- `guidelines/<topic>.md`: details and examples, conditions, alternatives, evidence links, and candidates only in a segregated section when useful.
- Avoid duplicate paragraphs in `BEST-PRACTICES.md`, CPU guidelines and machine topic guides. Reference stable anchors and technique IDs.
- When source evidence is thin, a concise, honest guide is better than multiple generic placeholders.
- For an `all` run, iterate over each verified two-level `docs/machines/<brand>/<machine>/` leaf, not `docs/machines/<brand>/`; treat each machine's evidence independently. In final report summarize updated / skipped / insufficient evidence for each.

## E. Traceability

Make repository-relative links that open the target in Markdown viewers. Recalculate paths based on the extra brand-level directory; do not reuse link depth from an older one-level machines layout. Link to `research/findings/`, `research/analyses/`, and preferably file+symbol/line in `research/sources/` where discoverable. Use stable links to technique files even if their absolute line numbers may change. If the precise source location is missing, identify the limitation.

Example evidence row (illustrative; never copy as real proof):

| Claim | Technique | Sources | Status | Scope |
| --- | --- | --- | --- | --- |
| Consider an indexed memory copy for a constrained buffer | `CPU6502-XXXX` | `research/analyses/example/` | analyzed | investigate, not a validated universal speedup |

## F. Final report and follow-up tests

Say what changed and why, list concrete files, enumerate deferred candidates and test conditions, and describe any conflicts or variant-specific restrictions. Do not claim real hardware testing without evidence.

## G. Incremental expansion

- New research for a registered machine should be merged through a subsequent targeted or `all` run; do not start over from scratch or remove earlier citations.
- Discovery of new platforms in research is only a **suggestion**. `discover` does not write, and `all` does not auto-register.
- Explicit `add <brand>/<machine>` creates a machine research profile even if validated findings have not yet been established; do not infer unknown technical specifications. See [new-machine-workflow.md](new-machine-workflow.md) for registration details.
