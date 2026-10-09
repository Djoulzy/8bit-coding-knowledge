---
id: ""                   # e.g. ANALYSIS-ORIC-0001
program: ""
cpu: []                  # e.g. ["6502"]
machines: []             # e.g. ["oric-atmos"]
analysis_status: draft   # draft | reviewed | complete
source_revision: ""
analysis_date: ""       # ISO 8601 date, YYYY-MM-DD
---

# Source-code analysis: Program name

## 1. Objective and scope

Explain the research goal, included files, excluded areas, and whether the
analysis covers the entire program or only selected routines.

## 2. Source provenance

| Field | Value |
| --- | --- |
| Program and version | Unknown |
| Author / publisher | Unknown |
| Original publication / date | Unknown |
| Repository / archive URL | Unknown |
| License / distribution terms | Unknown |
| Local source path | `research/sources/...` |
| Git revision / file checksums | Unknown |
| Assembly dialect and toolchain | Unknown |

Never edit imported historical source files as part of the analysis.

## 3. Target environment

- **Processor / exact variant:**
- **Machine / exact model:**
- **RAM and ROM configuration:**
- **ROM version and operating environment:**
- **Display mode and memory map assumptions:**
- **Audio / input / storage devices:**
- **Emulator or real hardware used for verification:**
- **Uncertainties:**

Do not infer Oric-1 / Atmos compatibility without supporting evidence.

## 4. Program architecture

Summarize startup, main loop, interrupts, state management, memory layout,
module dependencies, and external ROM / hardware calls.

### Memory allocations

| Address / range | Owner | Purpose | Evidence |
| --- | --- | --- | --- |
| Unknown | Unknown | Unknown | File, lines or reference |

### Routine inventory

| Routine / label | File and lines | Purpose | Inputs / outputs | Calls / hardware effects |
| --- | --- | --- | --- | --- |
| | | | | |

## 5. Analysis findings

Analyze algorithmic patterns, register and flag handling, zero-page usage,
page-crossing effects, code size, CPU cycles, self-modifying code, graphics,
sound, interrupts, memory management, and machine-specific techniques.
Do not assume every category is present.

### Finding F001: Short descriptive name

- **Location:** File / label / exact line range
- **Observed code behavior:**
- **Technical explanation:**
- **CPU-specific considerations:**
- **Machine-specific considerations:**
- **Benefits and trade-offs:**
- **Evidence:**
- **Confidence and unknowns:**
- **Existing technique ID or proposed new ID:**
- **Status:** observed

Repeat this subsection for each distinct finding.

## 6. Performance and verification

| Routine / scenario | Method | Environment | Cycles / bytes / result | Confidence |
| --- | --- | --- | --- | --- |
| Not yet measured | | | | |

Distinguish instruction-table calculations, emulator traces, and real-hardware
measurements. Include reproducer commands or benchmark files when available.

## 7. Comparison with the knowledge base

| Finding | Existing guideline / technique | New insight | Proposed action |
| --- | --- | --- | --- |
| F001 | None identified | | Draft finding only |

Search existing documentation before proposing a new technique.
Do not modify validated guidelines automatically.

## 8. Proposed documentation changes

List exact target paths and whether to add a finding, revise an existing
technique, or propose promotion. Keep proposed changes separate from approved
changes.

## 9. Open questions and next tests

- [ ] Confirm hardware or ROM assumptions.
- [ ] Resolve assembler syntax or undocumented behavior.
- [ ] Benchmark promising technique against a baseline.
- [ ] Verify portability across stated CPU and machine variants.

## 10. Summary

- **Most reusable techniques:**
- **Potentially misleading historical practices:**
- **Evidence still missing:**
- **Files created or changed:**
- **Recommended next investigation:**

## References

Link to original files, manuals, other analyses, and related technique IDs.
