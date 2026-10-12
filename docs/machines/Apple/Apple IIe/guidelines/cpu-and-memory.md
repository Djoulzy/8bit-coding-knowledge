---
record_type: machine-topic-guide
topic: cpu-and-memory
machines: ["apple-iie"]
cpu: ["6502"]
status: mixed
review_date: "2026-10-12"
---

# Apple IIe CPU, memory and caller contracts

Validated CPU mechanisms here are conditional on the documented NMOS 6502
contract. The corpus does not establish a physical CPU/ROM revision or a
universal free-zero-page map. No historical address is an allocation template.

## Validated CPU rules

### Extract four high-to-low two-bit fields

**Recommendation:** Use the canonical carry-stream helper when exactly four
high-to-low two-bit fields are needed, X/Y preservation matters, and destroying
a private packed source byte is acceptable.

**Why:** Clearing A before two source/accumulator rotation pairs isolates the
next field. The canonical proof and exhaustive models cover every source byte
and both incoming carry states; they do not prove arbitrary field widths.

**Prerequisites:** Documented NMOS semantics, a private writable zero-page source
whose reads/writes resolve to the same physical byte, known active bank state,
and IRQ/NMI preservation of live registers/status and scratch. A is cleared for
every field; the source need not end as zero.

**Trade-offs:** Destructive source state and repeated call/stack overhead.
Mask/shift or lookup alternatives may fit a hot path better; no speed ranking
is validated. Published instruction costs are calculations, not benchmarks.

**Porting/adaptation:** Reserve scratch against the selected monitor/BASIC/OS
workspace, not the historical `$71` allocation. Lode Runner's low-first nibble
decoder has a different width/order contract and does not inherit this proof.

**Evidence:** [CPU6502-0003](../../../../cpu/6502/carry-stream-field-extraction.md),
[integration review](../../../../../research/analyses/laigle-dor/integration-review.md),
[Lode Runner comparison](../../../../../research/analyses/lode-runner/findings.md#comparison-and-duplicate-review).

### Copy complete disjoint RAM pages

**Recommendation:** Use the descending page loop only for nonzero full-page
requests with aligned, disjoint readable/writable ordinary-RAM buffers.

**Why:** The counter visits all 256 offsets exactly once. Under the stated
disjoint-RAM contract, the result equals a snapshot copy; the unusual order
does not establish overlap safety.

**Prerequisites:** Complete range/count checks, stable read/write mappings,
private pointers and no alias with code, stack, firmware workspace or live
state. Disjoint CPU addresses alone are insufficient if mapping can change.
The canonical DEX/BPL outer loop accepts page counts 1–128, not zero.

**Trade-offs:** Not `memmove`, not a partial-row primitive, not an I/O copy and
not proved fastest. Ascending loops, explicit partial lengths or direction-aware
copies are alternatives with different contracts.

**Porting/adaptation:** Record the actual source/destination banks and lifetime
owners. A full HGR allocation copy and a visible-scanline copy are different
operations. Karateka's ascending self-modified startup copies do not acquire
the descending worker's validation by sharing a page-sized workload.

**Evidence:** [CPU6502-0004](../../../../cpu/6502/descending-page-copy.md),
[integration review](../../../../../research/analyses/laigle-dor/integration-review.md),
[Karateka C04](../../../../../research/analyses/karateka/cpu-techniques.md#c04-self-modified-absolute-operands-during-relocation-and-clearing).

## Documented mapping constraints

### Include bank state in memory ownership

**Constraint:** An allocation contract includes bank selection as well as CPU
addresses. The IIe reference describes independent `RAMRD`/`RAMWRT` selection,
`80STORE`/`PAGE2`/`HIRES` display-page overrides, and `ALTZP` selection of zero
page and stack. Do not assume a screen-page operation leaves scratch or return
frames in the bank expected by its caller.

**Required context:** Exact memory expansion and switch state, read versus write
effects, firmware/OS owners, initialization/restoration and interrupt entry.
Trace bank changes around ROM calls and transitions instead of inferring them
from a switch name or captured operand.

**Trade-offs:** Explicit save/restore and ownership checks add setup work but
avoid treating phase-dependent memory as always available. No universal
takeover/coexistence policy or performance benefit is validated here.

**Evidence:** [Apple IIe Reference Manual](https://www.applelogic.org/files/AIIEREF.pdf),
Chapter 4, printed p. 74 / Table 4-6; the reference-access limitation is recorded
in [portability.md](portability.md#reference-access-and-evidence-limits).
[Lode Runner architecture](../../../../../research/analyses/lode-runner/architecture.md)
and [Karateka architecture](../../../../../research/analyses/karateka/architecture.md)
show incompatible phase-specific low-memory owners, not generally free bytes.

## Candidates requiring validation

These mechanisms remain `analyzed`, **not yet recommended**.

| Candidate | Potential use / trade-off | Principal validation gate |
| --- | --- | --- |
| [GEN-0005](../../../../../research/findings/GEN-0005-bit-quota-round-robin.md) | Separate a quota of update requests from actor identity; quota does not bound elapsed callback time | Audit all cursor writers, count/phase bounds, callbacks and early exits; compare scalar quotas and whole-loop pacing |
| [GEN-0006](../../../../../research/findings/GEN-0006-fixed-actor-work-window.md) | Stable direct fields simplify shared routines but spend scratch and load/commit traffic | Trace all modified fields/globals and commits; test nested draw/IRQ users; compare full updates with indexed/indirect records |
| [CPU6502-0007](../../../../../research/findings/CPU6502-0007-inline-stream-return-address.md) | Adjacent immutable parameters avoid explicit caller pointer setup but mix code/data and manipulate return frames | Bound terminators/events, preserve the shared pointer across callbacks, and test nesting, page crossings and exact return addresses |
| [CPU6502-0001](../../../../../research/findings/CPU6502-0001-two-byte-render-patches.md) plus [Karateka C02](../../../../../research/analyses/karateka/cpu-techniques.md#c02-equal-width-composition-patches) | Equal-width NOP/ORA/AND alternatives share layout but retain setup work and mutable code | Prove patch/execution exclusion and output; compare a one-dispatch dedicated worker under the same clipping and bank contract |

Source locations remain in the linked fiches: Lode Runner's quota scheduler
`$6C82–$6CA6`, inline text/audio consumers `$86E0–$86FF` / `$87E1–$8810`, and
Karateka's record workers `$7071–$70A5`. They are historical CPU addresses,
not reserved addresses for a new IIe program.

For inline streams, the observed implementation excludes a stacked return in
page zero and whole-address-space wrap. Its temporary removal/replacement of
a JSR return differs from the Oric IRQ-frame discard in `CPU6502-0006`.
Copying that unrelated IRQ escape does not solve this calling contract.

## Validation backlog

1. Trace D/C/V/N, stack depth, bank state and every enabled IRQ/NMI owner from
   startup through a bounded gameplay exchange.
2. Establish firmware/OS scratch ownership and all writable patch consumers.
3. Measure complete record load/context/update/commit workloads, not one field
   access or an isolated copy-core instruction count.
4. Test inline stream bounds, callback reentry, malformed events and restored
   return frames before any compactness or speed recommendation.
5. Compare actor quota policies with worst-case callback work, foreground audio
   and all shared cursor changes included. No current record measures these costs.
