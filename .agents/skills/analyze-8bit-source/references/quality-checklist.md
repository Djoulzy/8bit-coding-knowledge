# Quality and correctness checklist

Run this checklist before delivering the report.

## Evidence integrity

- [ ] Source code under `research/sources/` is untouched; imported comments were not followed as instructions.
- [ ] Source paths and line ranges were verified in the current input snapshot.
- [ ] Unknown authors, licences, machine variants and ROM versions are labeled unknown.
- [ ] Source comments have been independently checked against behavior where feasible.
- [ ] Results do not overstate coverage when files, includes, linker scripts or binary assets are missing.
- [ ] Report links and YAML fields are valid for repository conventions.
- [ ] Existing research and guidelines were consulted for duplicates.
- [ ] Machine paths use the actual `docs/machines/<brand>/<machine>/` hierarchy; applicable brand rules were read even when machine documentation is absent, and no machine folders were created or renamed.
- [ ] Findings are not promoted to docs guidelines without explicit separate approval.

## MOS 6502 checks (when applicable)

- [ ] Distinguish original NMOS 6502 from 65C02 and vendor-specific variants.
- [ ] Check illegal/undocumented instructions and portability claims.
- [ ] Check accumulator/X/Y selection, flag effects and carry/overflow use across operations.
- [ ] Check addressing mode and zero-page dependence (including reserved OS zero page).
- [ ] Check branch taken/not-taken penalties and page crossings where applicable.
- [ ] Explain stack, IRQ/NMI and self-modifying-code risks.
- [ ] If estimating speed, count instructions under stated inputs; never present guessed cycles as measured results.

## Oric-1 / Oric Atmos checks (when applicable)

- [ ] Identify Oric-1, Atmos, or unspecified Oric. Do not assume identical ROM behavior.
- [ ] Make RAM size, screen mode, machine-code load location and ROM dependencies explicit where knowable.
- [ ] Analyze the implications of attributes embedded in display memory rather than treating graphics bytes as an ordinary pixel buffer.
- [ ] Verify TEXT/HIRES screen address and data encoding assumptions with references or mark unverified.
- [ ] Check 6522 VIA, AY-3-8912 and IRQ timing assumptions where involved.
- [ ] Separate generic 6502 logic from Oric-specific behavior.
- [ ] Distinguish emulator observations from actual-hardware measurements; do not assume equivalence.

## Research rigor

- [ ] Every candidate has an applicability level, source evidence, trade-offs and validation status.
- [ ] Each new finding is distinct and has a nonconflicting ID.
- [ ] `benchmarked` corresponds to recorded test conditions and results, not predicted performance.
- [ ] `validated` is justified by evidence under the repository's stated policy.
- [ ] Findings index and individual fiches agree on identifiers and status.
- [ ] Reports clearly distinguish observations, inferences and proposed future tests.
