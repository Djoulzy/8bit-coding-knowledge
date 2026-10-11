---
id: "GEN-0005"
title: "Schedule actor work quotas with a persistent round-robin cursor"
category: "scheduling"
cpu: ["6502"]
machines: ["apple-ii-family"]
status: analyzed
source_analyses: ["../analyses/lode-runner/overview.md"]
tags: ["quotas", "round-robin", "bounded-work", "foreground-loop"]
---

# Schedule actor work quotas with a persistent round-robin cursor


## Summary

Select a work quota for the current loop phase, then apply that many updates to
successive actors using a persistent cursor. Lode Runner represents each quota
as a leading-one bit pattern and separates the amount of work from actor identity.

## Problem and context

- **Problem:** spread actor work over foreground iterations while changing update rate.
- **Use cases:** small fixed actor sets with speed/difficulty controls.
- **Preconditions:** bounded count, initialized cursor/phase, callback preservation of scheduler state and a defined early-stop condition.
- **Applicability:** common algorithm; the observed shift/carry implementation is documented NMOS 6502 code on Apple II family hardware. Exact CPU/machine revision is unknown.

## Provenance

| Field | Value |
| --- | --- |
| Original program | Lode Runner; supplied 1983-marked cracked Apple II disk |
| Author / publisher | Doug Smith / Brøderbund, corroborated by the publisher manual linked in overview; individual routine authorship and publisher-original equivalence unknown |
| Source / archive | research/sources/Apple IIe/Lode Runner/Lode Runner (1983)(broderbund)[cr].dsk; download/archive provenance unknown |
| License / usage | No license supplied; no redistribution grant established |
| Source revision | Repository baseline d02edc77fa0a02d3f679af22456ca1c762c305dc; historical image is gitignored |
| Image SHA-256 | cbc048a55c2835f1b3b54696660e8902c84c25dac44a6dc94b13a7e8f81379ec |
| File / routine / addresses | [startup.asm.txt:L90–L103](../analyses/lode-runner/extracted/startup.asm.txt), CPU $60C5–$60E2, first instruction DSK $0139CC; [scheduler.asm.txt:L1–L18](../analyses/lode-runner/extracted/scheduler.asm.txt), CPU $6C82–$6CA6, first instruction DSK $014589; [scheduler.asm.txt:L19–L25](../analyses/lode-runner/extracted/scheduler.asm.txt), CPU $6CDB–$6CE9, first instruction DSK $0145E2 |
| First analysis | [Lode Runner overview](../analyses/lode-runner/overview.md) |

The input has no assembly source or original labels. Generated listing lines,
CPU addresses and original image offsets replace unavailable source-line
references. The [extraction conventions](../analyses/lode-runner/extracted/README.md)
explain relocation, byte provenance and unresolved runtime dependencies.


## Original implementation

Original assembler dialect is unknown. Analytical pseudocode, not copied source:

~~~text
if actorCount == 0: return
phase = (phase + 1) mod 3
remaining = quota[phase]
do:
    request = remaining & 1
    remaining >>= 1
    if request:
        cursor += 1
        if cursor > actorCount: cursor = 1
        updateActor(cursor)
        if playerAlive == 0: return
while remaining != 0
~~~

The three quota bytes are copied into $60–$62. $64 holds the phase, $63 the
shifted quota, $19 the cursor and $8D the actor count. Level setup initializes
$19 to zero: [level.asm.txt:L1–L8](../analyses/lode-runner/extracted/level.asm.txt), CPU $6238–$6245, first instruction DSK $013B3F. The update prefix then loads the selected actor
from parallel arrays through $75CE.

## Technical explanation

The local table at $6CA7–$6CC1 has nine three-byte rows:

~~~text
00 00 00    00 01 01    01 01 01
01 03 01    01 03 03    03 03 03
03 03 07    03 07 07    07 07 07
~~~

Values $00/$01/$03/$07 encode zero/one/two/three requests. They are quotas:
bit position does not identify a particular guard. The cursor persists across
calls, wraps in 1..count, and can wrap inside one quota if count is small.

Without early exit or other cursor writes, successive events visit consecutive
actors. Over enough events this distributes selections evenly; it is not a
guarantee of equal elapsed CPU time, equal gameplay speed or global fairness.
Hole-service code also writes $19, so the complete game need not behave as an
isolated round-robin scheduler. AI costs may differ per actor.

## CPU-specific considerations

LSR $63 sends the low bit to carry. BCC decides whether to call the updater;
the remainder is subsequently tested through A/Z. INC/CPX/BCS wrap the cursor.
The updater and any interrupt must preserve/reestablish the remaining quota
and phase. Registers A/X/Y and flags are scratch across scheduler calls.

Only documented NMOS instructions appear in this fragment. Porting the
algorithm does not require a 6502 or any undocumented opcode. Branch outcomes,
callback costs and possible crossings prevent a constant whole-call timing.
No IRQ-driven scheduling or fixed frame period was established.

## Machine-specific considerations

The quota algorithm has no inherent video or audio dependency. In this game,
audio waits, player work and hole handling share the foreground loop. Their
timing and other writes to the cursor influence observed guard pace.

## Performance and resource costs

| Metric | Original | Alternative | Evidence |
| --- | --- | --- | --- |
| Policy table | 27 bytes, nine three-phase rows | Scalar counts or accumulator policy | Actual table bytes |
| Scheduler storage | 6 bytes: three quotas, remainder, phase, cursor; count/stop state shared | Counts can eliminate bit scanning | Mapped ZP references |
| Maximum requests in checked table | 3 per call before early stop | Policy-dependent | Bit-count model |
| CPU cycles / elapsed time | Not measured; updater-dependent | Not measured | No emulator/hardware run |

The nine rows express average requested work from zero to three updates per
iteration over three phases, assuming no early exit. This is a work count,
not a frame rate.

## Advantages

- Work amount and actor identity have separate, inspectable state.
- Fixed small quotas bound requests for this table.
- Cursor wrap permits changing actor count without rebuilding an identity mask.

## Limitations and risks

Invalid policy indices, clobbered quota state or unbounded callbacks defeat the
work bound. Early exit and unrelated cursor changes affect distribution.
A count of zero is explicitly handled. Quotas larger than the actor set can
update an actor more than once per call.

## Alternatives

A simple decrementing count preserves the same cursor policy without bit
scanning. A fractional accumulator supports finer average rates. Updating all
actors each frame is simpler when capacity and timing allow it. Benchmark actual
callback costs before choosing any representation.

## Validation record

- **Current status:** analyzed; provisional.
- **Evidence:** linked scheduler, setup and actor-selection bytes; policy table.
- **Static check:** every actual quota over counts 1..5 and initial cursor 0..count gives popcount requests and in-range consecutive selections under the isolated model.
- **Reproducer:** [verify_analysis.py](../analyses/lode-runner/tools/verify_analysis.py), results in [verification.json](../analyses/lode-runner/verification.json).
- **Benchmark / real hardware:** none; the historical program was not executed.
- **Open:** full AI preservation contracts, all cursor writers, difficulty index bounds, early exits and measured pace.

## Recommendation for new projects

Consider separating a small work budget from actor selection when foreground
capacity is tight. Specify whether repeated updates and early exits are allowed.
Use scalar counts if they make the policy clearer; measure callback work and
audit shared cursor ownership before relying on fairness.

## References and related techniques

- [CPU analysis](../analyses/lode-runner/cpu-techniques.md#c05--quota-bits-and-persistent-actor-cursor-analyzed-commoncpu).
- [Routine inventory](../analyses/lode-runner/routines.md).
- [Table dump](../analyses/lode-runner/extracted/tables.hex.txt), $6CA7–$6CC1.
