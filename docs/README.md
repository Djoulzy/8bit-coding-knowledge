---
record_type: knowledge-index
review_date: "2026-10-09"
---

# Programming knowledge

Validated recommendations have an explicit scope. The status does not imply
measured performance or compatibility of an entire historical program.

| Level | Technique | Validated scope |
| --- | --- | --- |
| General 8-bit | [GEN-0002: semantic collision grids](common/semantic-collision-grid.md) | Bounded logical cell lookup independent of display pixels |
| MOS 6502 | [CPU6502-0003: carry-stream field extraction](cpu/6502/carry-stream-field-extraction.md) | Four high-to-low two-bit fields with stated source/register ownership |
| MOS 6502 | [CPU6502-0004: descending full-page copy](cpu/6502/descending-page-copy.md) | Aligned disjoint RAM, complete pages and explicit counter/alias constraints |

No Oric-specific guideline has yet passed the required ROM/display/ownership
verification. Pending work is documented in the
[L'Aigle d'Or integration review](../research/analyses/laigle-dor/integration-review.md).
The review also covers related research findings and benchmark proposals.

CPU policy is in [6502/AGENTS.md](cpu/6502/AGENTS.md); the existing Oric policy
is in [Oric/AGENTS.md](machines/Tangerine/Oric/AGENTS.md). Apple family policy
is in [Apple/AGENTS.md](machines/Apple/AGENTS.md).
