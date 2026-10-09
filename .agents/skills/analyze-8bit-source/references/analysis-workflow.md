# Source analysis workflow and output contract

## Stage 0 — Inspect existing work

- Identify the requested input, and list files by role (code, include, assets, build definitions, machine code, documentation).
- Search for existing reports under `research/analyses/` and findings under `research/findings/` before writing.
- Determine whether an existing analysis should be extended. Preserve user annotations and reviewed material; do not overwrite with an empty template.
- Record a reproducibility snapshot: repo-relative input, git commit hash if available, whether relevant files contain uncommitted changes, source language and assembler dialect when identifiable.
- Identify the target hardware; do not infer an Oric Atmos target from every Oric label or assume 65C02 instructions on an NMOS 6502.

## Stage 1 — Routine and architecture map

Build a routine inventory that includes, as available:

| Routine/symbol | Source path:lines | Called by / calls | Purpose | External state or hardware | Confidence |
|---|---|---|---|---|---|

Trace the entry point, initialization, principal loop, IRQ/NMI handlers, input, rendering, audio, storage and memory management. Explain limitations from conditional compilation, overlays, external libraries or missing includes.

Classify evidence as `confirmed by source`, `likely inference`, or `unknown`. Avoid inferring author intent solely from style.

## Stage 2 — Technical analysis

Identify candidates such as:

- General: data compression, lookup tables, fixed-point math, buffer lifetime reuse, state machines.
- CPU: zero-page allocations, indexed/indirect addressing, instruction/flag reuse, branch tricks, alignment, page crossings, code generation or self-modification, interrupts.
- Machine: screen addressing, attribute encoding, ULA behavior, ROM calls, VIA or PSG accesses, keyboard and storage interfaces.

For each candidate capture: unique provisional label, precise source span, how it works, evidence, assumptions, why it might be useful, ROM/RAM/CPU variant prerequisites, alternatives, measurable hypotheses, uncertainty and applicability level (`common`, `cpu`, `machine`). Note correctness risks and whether an optimization could be slower or larger in some cases.

## Stage 3 — Repository cross-check

- Look for the same algorithm under alternate names and in nearby CPU/machine directories.
- Reuse and cross-link an existing finding ID if it describes the same technique; do not generate duplicate IDs.
- If assigning a new ID, inspect all existing IDs in the namespace (e.g. `GEN-####`, `CPU6502-####`, `ORIC-####`) and choose the next unused number. Do not rely solely on filename order.
- Keep status at `observed` or `analyzed` absent actual reproducible tests and supporting evidence.

## Stage 4 — Output files

Default directory: `research/analyses/<program-slug>/`. Use a deterministic slug based on the requested program directory name. Do not create duplicate directories for the same source by silently changing capitalization or hyphenation.

In `full` mode, produce these files (can cross-reference rather than repeating long text):

1. `overview.md`: identity, scope, inputs, assumptions, source provenance/revision, coverage, headline results, risks.
2. `architecture.md`: modules, entry points, control flow, memory organization and dependencies.
3. `routines.md`: indexed routine map with source references and confidence.
4. `cpu-techniques.md`: CPU-relevant candidates, compatibility, timing notes and alternatives.
5. `hardware-techniques.md`: machine-relevant candidates, video/audio/ROM/IRQ and hardware dependencies.
6. `findings.md`: finding index; candidate IDs, source spans, classification, evidence level, status, duplicate/cross-links, suggested validation.

Honor `templates/analysis.md` section conventions: use or adapt its fields in the generated reports. If the repository already has a different naming policy, follow its `AGENTS.md` rather than forcibly renaming files.

In `focus=<topic>` mode, create/update `overview.md`, `routines.md` (or the necessary routine subset), `findings.md`, and relevant topical report(s). Note intentionally unexamined modules. Do not create irrelevant empty reports just to meet the full-mode list.

In `report-only` mode, do not create new `research/findings/*.md` files. Still list candidate techniques in the analysis's `findings.md`.

For a genuinely novel finding requiring a dedicated fiche, start from `templates/technique.md`, populate required YAML metadata, and write one file under `research/findings/` following established repository naming. Reference the source analysis and source path:lines. Never describe a proposed benchmark as already executed.

## Stage 5 — Incremental re-analysis

If outputs exist, compare the current source snapshot to the prior analysis (if revision metadata is available), preserve reviewed conclusions and cite changes. Update records only when justified. For disappeared routines, mark findings stale pending review rather than deleting references automatically. Never replace the source files or validated guidelines.

## Stage 6 — Final response in French

Briefly describe the analyzed path, hardware and source dialect, main routine map, reusable findings (CPU vs machine), unproven hypotheses, exact documents written, open issues and the single best next investigation. If an expected output was skipped, explain why.
