# 8-Bit Programming Knowledge Base

## Mission

Build a comprehensive, technically accurate knowledge base
of programming techniques for 8-bit computers.

The knowledge base has three levels:

1. General 8-bit programming techniques.
2. CPU-specific programming and optimization techniques.
3. Machine-specific hardware and programming techniques.

The primary goal is to extract knowledge from historical
source code and use it to establish reliable guidelines
for new software development.

## Repository Structure

- docs/common/       : Platform-independent techniques
- docs/cpu/          : CPU architecture and optimization
- docs/machines/     : Machine-specific documentation
- research/sources/  : Original historical source code
- research/analyses/ : Detailed source code analyses
- research/findings/ : Discovered techniques
- templates/         : Documentation templates
- benchmarks/        : Performance tests

Machine documentation uses `docs/machines/<brand>/<machine>/`, for example
`docs/machines/Tangerine/Oric/` and `docs/machines/Apple/Apple IIe/`.
`<brand>` and `<machine>` are placeholders for actual directory names;
manufacturers are direct children of `docs/machines/`, with no intermediate
`brand/` directory. Preserve existing spelling, capitalization and spaces.
Brand-level `AGENTS.md` files provide shared instructions; machine profiles
and development guides belong in the machine leaf.

## Working Principles

### Accuracy

- Never invent CPU instructions or hardware capabilities.
- Never invent instruction timings or performance results.
- Verify hardware-specific claims against reliable references.
- Clearly identify assumptions and uncertain conclusions.
- Distinguish documented behavior from observed behavior.
- Do not treat historical code as inherently optimal.

### Source Code Analysis

When analyzing historical source code:

1. Identify the target CPU and machine.
2. Identify the assembler or compiler dialect.
3. Understand the program architecture.
4. Identify significant algorithms and routines.
5. Examine CPU-specific optimizations.
6. Examine hardware-specific optimizations.
7. Identify memory management techniques.
8. Identify reusable programming patterns.
9. Document limitations and trade-offs.
10. Record precise source references.

Do not limit analysis to explicitly commented code.
Look for implicit optimizations and unusual instruction
sequences that deserve investigation.

### Evidence

Every discovered technique must include:

- Original program and author, when known.
- Source file and routine or line location.
- Technical explanation.
- CPU and machine applicability.
- Advantages and disadvantages.
- Validation status.

Never fabricate source references.

### Validation Status

Use these classifications:

- observed: Found in historical source code.
- analyzed: Behavior understood and technically explained.
- benchmarked: Performance measured in a reproducible test.
- validated: Recommendation supported by sufficient evidence.

A benchmark alone does not automatically make a technique
a validated best practice.

### Knowledge Organization

Before creating documentation:

1. Search for related existing knowledge.
2. Avoid duplicate technique descriptions.
3. Place generic techniques in docs/common/.
4. Place CPU-specific techniques in docs/cpu/.
5. Place hardware-specific techniques in docs/machines/.
6. Use cross-references between documentation levels.

A machine-specific document should reference applicable
CPU techniques instead of duplicating them.

### Documentation Format

- Use Markdown.
- Write technical documentation in English.
- Use YAML frontmatter for technique metadata.
- Include assembly examples where appropriate.
- Use explicit hexadecimal notation.
- Document assembler syntax when relevant.
- Favor clear technical explanations over generic advice.

### Historical Sources

- Preserve imported historical source code unchanged.
- Store analysis and annotations separately.
- Respect original licenses and attribution.
- Do not copy large source sections into documentation
  unless permitted.
- Never execute untrusted build scripts without inspection.

### Promotion to Guidelines

New discoveries must first be documented under research/.

Do not automatically promote discoveries into
validated coding guidelines.

Promotion requires:

1. Technical understanding.
2. Evidence supporting the recommendation.
3. Defined applicability and limitations.
4. Comparison with existing techniques when relevant.

### Specialized Instructions

When working on a CPU, read its corresponding
docs/cpu/<cpu>/AGENTS.md if present.

When working on a machine, resolve its existing brand/machine path and read
`docs/machines/<brand>/AGENTS.md` and
`docs/machines/<brand>/<machine>/AGENTS.md` if present, as well as the
applicable CPU instructions. Brand instructions also apply when analyzing
a machine whose leaf has no documentation yet. Do not create or rename
directories merely to match an example path.

These instructions complement the repository rules.

### Reporting

After each analysis, provide:

- An overview of the examined code.
- Newly discovered techniques.
- Existing techniques confirmed.
- Potential optimizations.
- Unresolved technical questions.
- Documentation created or updated.
- Recommended next investigations.
