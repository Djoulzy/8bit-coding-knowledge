# Output format for machine development documentation

Use existing conventions where present. The target is a machine leaf below a brand directory; in regular update/all mode it must already exist, while `add <brand>/<machine>` may register a new leaf. Never write best practices directly to `docs/machines/<brand>/`. The structure below is a **layout contract**, not a requirement to generate empty pages. Machine docs are for **building and porting programs**, not merely describing old code.

## `docs/machines/<brand>/<machine>/BEST-PRACTICES.md`

Suggested sections:

1. `# <Machine> — Development best practices`
2. `## Supported hardware and assumptions` — explicit CPU/ROM/model/memory/video scope.
3. `## Quick-start rules` — 5–12 short, actionable, **validated** recommendations only if supported.
4. `## Topic guides` — relative links to existing detailed Markdown guides.
5. `## Porting an existing program` — concise adaptation checklist and links to `guidelines/portability.md`.
6. `## Evidence and status` — how recommendations were verified and where source findings live.
7. `## Candidates requiring validation` — brief separate table if applicable.

For each quick-start item, include the link to the detailed rule, not just a bare imperative. Avoid repeating the detailed analysis.

## `docs/machines/<brand>/<machine>/guidelines/<topic>.md`

Follow this pattern for each substantive rule:

```markdown
### <Rule title>

**Recommendation:** <do X when condition Y; avoid it when Z>.

**Why:** <mechanism based on CPU/hardware evidence>.

**Prerequisites:** <specific CPU variant, ROM, video mode, memory ownership>.

**Trade-offs:** <size, cycles, RAM, setup time, maintainability; unknown if not measured>.

**Porting/adaptation:** <what changes on target machine; required compatibility checks>.

**Evidence:** [Technique ID](relative/path/to/finding.md),
[source analysis](relative/path/to/analysis.md),
[reference](relative/path/to/machine/manual.md).
```

Add a short assembly snippet only if it clarifies implementation; specify assembler dialect, assumptions and register/flag effects. Do not invent measured cycles, source snippets, addresses or ROM APIs. When there is no evidence for a numerical optimization, say it is not measured.

### Candidate section

Below confirmed rules, optionally add `## Candidates requiring validation` with explicit **not yet recommended** labeling, proposed test conditions, and links to source findings. Do not phrase candidates as must/should. If a candidate is highly risky (undocumented opcodes, self-modifying code, unverified I/O timing), make the risk prominent.

## Portability guide checklist

- CPU variant and instruction compatibility.
- Calling conventions, register clobbering and stack use.
- Zero-page / direct-page ownership, RAM/ROM boundaries and relocation.
- Screen resolution, memory layout, character/pixel encoding, color attributes.
- Sound chip access, timers, IRQ ownership, keyboard or input reading.
- ROM entry points, firmware differences and disk/tape interfaces.
- Timing and speed assumptions (emulation versus real hardware).
- Toolchain, assembler syntax, object file or binary loading conventions.
- Test matrix for target model variants and minimal regression smoke test.

## Files and cross-links

Use exact directories and relative Markdown links. Preserve existing top-level `hardware.md`, `memory-map.md`, `graphics.md`, `audio.md` as hardware references unless user has requested refactoring. If a filename under `guidelines/` already exists, update it rather than create near-duplicates.

## New-machine profile (add/init only)

When a target is explicitly newly registered, create or merge a short `README.md` with supported identity and variant, backed CPU/hardware facts, links to research, and outstanding verification tasks. Use the example in [new-machine-workflow.md](new-machine-workflow.md). Do not create `BEST-PRACTICES.md` or empty `guidelines/` pages until meaningful supported rules exist. Later updates populate these files without restructuring the machine directory.
