# Installation - incremental 8-bit Codex workflows v3

This package contains two full, validated Codex skills for `.agents/skills/`:

1. `build-8bit-guidelines` v3: preserves all previous publishing/update modes and adds `discover` plus explicit `add <brand>/<machine>` registration.
2. `analyze-8bit-source` compatibility update: preserves full historical analysis workflow, while resolving scoped machine instructions in `docs/machines/<brand>/<machine>/` instead of the previous one-level folder.

Extract at the Git repository root, retaining the hidden `.agents` folder. It updates the two skill folders only. Research and documentation in the repository remain untouched. If you've made custom changes inside either existing skill, review the Git diff or use the builder-only installer instead.

Commands:

- `$analyze-8bit-source research/sources/<program>` to analyze a new program.
- `$build-8bit-guidelines discover` to list not-yet-registered machines suggested by research (read-only).
- `$build-8bit-guidelines add <brand>/<machine>` to register one new machine intentionally.
- `$build-8bit-guidelines add <brand>/<machine> plan-only` for a read-only preview.
- `$build-8bit-guidelines <brand>/<machine>` to update the machine's guides incrementally.
- `$build-8bit-guidelines <brand>/<machine> focus=graphics` for a focused update.
- `$build-8bit-guidelines <brand>/<machine> plan-only` for a read-only update preview.
- `$build-8bit-guidelines all` to update all currently registered machine folders, without automatically creating new ones.

Adding a new machine with no validated findings creates only a research profile, not invented or blank best-practice documents. Run `add` once, then analyze new programs and rerun the normal update command as evidence accumulates.
