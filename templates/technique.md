---
id: ""                    # e.g. CPU6502-0001, ORIC-0001, GEN-0001
title: ""
category: ""              # e.g. graphics, memory, arithmetic, timing
cpu: []                   # e.g. ["6502"]
machines: []              # e.g. ["oric-1", "oric-atmos"]
status: observed          # observed | analyzed | benchmarked | validated
source_analyses: []       # Relative links to research/analyses/
tags: []
---

# Technique name

## Summary

Explain the technique in two or three sentences, including its purpose.

## Problem and context

- **Problem being solved:**
- **Typical use cases:**
- **Assumptions / preconditions:**
- **CPU variants and target machines:**

## Provenance

| Field | Value |
| --- | --- |
| Original program | Unknown |
| Author / publisher | Unknown |
| Source URL / archive | Unknown |
| License / usage conditions | Unknown |
| Source revision / checksum | Unknown |
| File and routine | Unknown |
| Line range / symbols / address | Unknown |
| First analysis | Link to `research/analyses/...` |

Use exact relative file paths and line numbers when available. Do not invent attribution.

## Original implementation

State the assembler dialect, address conventions, and any required symbols.

```asm
; Insert a short, appropriately attributed source excerpt here.
; If copying is not permitted, summarize instead and link to the source.
```

## Technical explanation

Describe the algorithm, data flow, register/flag effects, and why it works.
Explain any non-obvious dependencies on initialization or surrounding code.

## CPU-specific considerations

- **Registers and flags:**
- **Addressing modes:**
- **Instruction compatibility (6502 / 65C02 / other):**
- **Page boundaries, branch timing, and interrupts:**
- **Code and data alignment:**

Write "Not applicable" when a field does not apply.

## Machine-specific considerations

Specify hardware dependencies such as reserved zero-page addresses, ROM calls,
video encoding, memory mapping, VIA timers, or other peripherals.
For Oric techniques, distinguish Oric-1 and Atmos behavior where relevant.

## Performance and resource costs

| Metric | Original | Alternative | Evidence / method |
| --- | --- | --- | --- |
| CPU cycles (including conditions) | Not measured | Not measured | |
| Code size (bytes) | Unknown | Unknown | |
| RAM / zero-page usage (bytes) | Unknown | Unknown | |
| ROM usage (bytes) | Unknown | Unknown | |

Never invent measurements. Explain any conditional timing, page crossing,
interrupt interference, input-size assumptions, or emulator limitations.

## Advantages

- Describe practical benefits and the circumstances in which they apply.

## Limitations and risks

- Describe portability, maintainability, memory, correctness, and hardware risks.

## Alternatives

Compare with conventional or simpler implementations where possible.

## Validation record

- **Current status:** observed
- **Source-based evidence:**
- **Theoretical analysis:**
- **Benchmark setup / commands / environment:**
- **Expected result versus actual result:**
- **Real-hardware confirmation (if any):**
- **Outstanding questions:**

Status definitions:
- `observed`: found in historical code, not necessarily understood or recommended.
- `analyzed`: behavior and constraints explained from evidence.
- `benchmarked`: reproducible performance measurement recorded.
- `validated`: recommendation justified for explicitly stated conditions.

## Recommendation for new projects

State **when to use**, **when not to use**, and what must be checked first.
Avoid unconditional "best practice" claims.

## References and related techniques

- Relative links to source analyses, CPU documentation, machine documentation,
  related technique IDs, authoritative manuals, and reproducible tests.
