# Publication QA checklist

Before reporting a successful machine-guidelines update:

- [ ] Qualified `<brand>/<machine>` resolution is unique; brand containers were never treated as machines, including in `all` mode. Bare machine names were accepted only when unique.
- [ ] In regular update/all mode, the target folder existed before writing. Only an explicit `add`/`init` may create a missing machine leaf; output stays within that authorized leaf.
- [ ] Repository `AGENTS.md`, optional brand `AGENTS.md`, machine `AGENTS.md`, and relevant CPU `AGENTS.md` were considered.
- [ ] Applicable findings from multiple programs/platforms were assessed, not just the latest analysis.
- [ ] Every normative practice has traceable supporting evidence and explicitly delimited applicability.
- [ ] Findings lacking support are segregated as candidates, never relabeled validated by convenience.
- [ ] Machine vs CPU vs general material is correctly divided and linked, with no misleading duplication.
- [ ] Every machine variant and ROM dependency is explicit; no implicit 'all Orics' or 'all 6502s' assertions.
- [ ] Machine and CPU-specific conflicts are noted or resolved conditionally.
- [ ] Every timing, space or speed claim has a source or is clearly unknown/estimated, never fabricated.
- [ ] Examples have specified dialect and required conditions; source and licensing respected.
- [ ] Existing handwritten content was preserved; no unrelated files were overwritten or deleted.
- [ ] `BEST-PRACTICES.md` is actionable and points to detailed topic guides and porting notes.
- [ ] Markdown links and filename case have been checked where possible.
- [ ] Git diff or equivalent was reviewed for accidental changes.
- [ ] Any incomplete scope, sources or tests are reported in French.

- [ ] All previous commands (`all`, focused updates, plan-only, qualified and unique bare-name resolution) still behave as before.
- [ ] `discover` produced no write operations, and names from research were not treated as proven identity.
- [ ] Any missing machine folder was created only through explicit `add <brand>/<machine>`; existing machine docs and user modifications were not overwritten.
- [ ] For a newly registered machine without validated findings, only an honest research profile was created, without empty guideline files or fabricated practices.
- [ ] The separate `$analyze-8bit-source` skill remains available and was not replaced or modified by this package.
