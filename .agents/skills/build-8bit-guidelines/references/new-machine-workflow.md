# Incremental machine registration and discovery

This workflow extends the existing publisher. It does not replace `$analyze-8bit-source`, which remains the way to add new research.

## Discover new machines: read-only

1. Enumerate registered `docs/machines/<brand>/<machine>/` leaves using the registration criteria in `SKILL.md`; list empty leaves separately. Preserve existing directory names and do not treat brand-level instructions as a machine profile.
2. Inspect available structured metadata, `research/analyses/`, `research/findings/`, source program READMEs and other existing docs for explicit make/model and CPU/ROM clues. Existing folder names under `research/` alone are insufficient proof.
3. Report a table of candidate brand/model, CPU (known/unknown), evidence path, identity confidence, and whether already registered.
4. Where variant identity cannot be distinguished (e.g., machine family versus specific model), do not choose arbitrarily. Suggest a qualified name only after checking the repository naming conventions.
5. Do not create or update files in `discover`.

## Add a new machine: explicit registration

Command shape: `$build-8bit-guidelines add <brand>/<machine> [plan-only]`.
Quote targets containing spaces, for example `add "Apple/Apple IIe"`.

1. Require both nonempty path components supplied explicitly by the user; reject paths containing traversal, empty segments, absolute paths or unsafe symlinks. Do not infer a brand name from source analysis.
2. Check for an existing machine with that full path and nearby variant/model names. If an exact directory exists, reuse it; merge existing documentation, or add the requested profile to an empty leaf. Never rename, delete or regenerate it. For potentially accidental duplicates, document the alternatives before writing.
3. Read root `AGENTS.md`, brand-level and machine-level `AGENTS.md` files if present, templates and applicable CPU rules if CPU identification is backed by evidence.
4. Seek evidence for machine identification, CPU variant, memory map, video/ULA, ROM, storage, audio, I/O and source programs. Mark missing facts `Unknown — verification needed`. Keep differences among closely related model variants explicit.
5. In `plan-only`, list the directory to create, profile sections and potential guideline topics; do not write anything.
6. In normal `add`, create `docs/machines/<brand>/<machine>/` (and brand parent if missing). Populate or merge a concise `README.md` with identity, scope, known sources, status and gaps. Do not overwrite existing user content. Do not generate a generic `AGENTS.md` unless the user explicitly asks for machine-specific agent rules.
7. If evidence supports actual validated programming rules, use the original publisher workflow to build `BEST-PRACTICES.md` and focused topic guides. Otherwise stop after `README.md` and list concrete next steps to collect code/measurements.
8. After registration, the target participates in `$build-8bit-guidelines all`, and future `$build-8bit-guidelines <brand>/<machine>` calls incrementally fold in new program analyses.

## Example minimal registration profile

```markdown
# <Machine name> — Research profile

**Brand / family:** <as supplied or verified>

**Machine variant:** <verified identity, or verification needed>

**CPU:** <variant supported by sources, or Unknown — verification needed>

## Confirmed hardware and software facts

- <fact + source; omit items not verified>

## Applicable general/CPU references

- <relative links to existing docs, where actually applicable>

## Research evidence

- <links to analyses/findings/source metadata if present>

## Open verification tasks

- Confirm model and ROM variants.
- Confirm target-specific hardware constraints.
- Benchmark or validate proposed reusable optimizations.
```

Do not create empty performance claims or pretend that the profile is already a best-practices guide.

## Incremental update safeguards

- Keep history: never delete or replace older validated rules when new results disagree. Identify the conflict and mark which conditions are unresolved.
- Preserve user-authored files and relative links; include only necessary changes in git diff.
- Never auto-create brand containers or machine leaves in `all`, focus-only, or ordinary update mode; substantive guideline pages may be added within an existing registered leaf. `discover` creates no files or directories.
- Source import or routine analysis remains the job of the independent analysis skill.
