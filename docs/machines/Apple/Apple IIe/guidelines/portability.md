---
record_type: machine-topic-guide
topic: portability
machines: ["apple-iie"]
cpu: ["6502"]
status: evidence-profile
review_date: "2026-10-12"
---

# Porting programs to an explicitly configured Apple IIe

This guide defines compatibility checks, not a claim that the supplied disks
work on every IIe. CPU-compatible instructions do not make ROM, bank, display,
input, speaker or disk assumptions portable.

## Evidence profiles

| Program | Inspected environment | Evidence strength | Compatibility boundary |
| --- | --- | --- | --- |
| [Lode Runner](../../../../../research/analyses/lode-runner/overview.md) | NMOS-compatible instruction paths; main-RAM working range; ordinary HGR foreground/terrain pages; Applesoft/DOS-style services and foreground audio/input | Static extraction, byte mappings and translated table/quota models; draft dossier | Local cracked edition; exact CPU/ROM/banking and first-level I/O execution unresolved; no emulator or hardware run |
| [Karateka](../../../../../research/analyses/karateka/overview.md) | NMOS-compatible instruction paths; two HGR pages; copied actor records; monitor/Disk II interfaces and foreground audio/input | Completed static report scope with relocation, record, row and shifter models | Exact disk/ROM/CPU revision, bank state, full clipping and later disk protocol unresolved; no emulator or hardware run |

The recorded main-RAM ranges are not proofs of whole-game minimum hardware.
Folder names and the observed Karateka `$FBB3 == $06` branch are not sufficient
configuration identification or enhanced-IIe compatibility tests.

## Establish the target profile first

Before selecting an implementation, record:

- motherboard/model revision, physical CPU and enhancement status;
- ROM checksum/revision, BASIC/OS environment and retained firmware services;
- main/auxiliary RAM, expansions, bank controls and phase-specific owners;
- ordinary HGR or another explicitly supported mode, page roles, video
  standard and monochrome/composite/other output;
- disk controller, firmware, slot, loading environment and exact media edition;
- input devices, calibration and foreground versus interrupt-driven audio;
- all IRQ/NMI sources, stack headroom and writable patch consumers;
- assembler/linker dialect, load format, relocation and code/data boundaries;
- emulator version/configuration and real hardware used for each test.

Unknown fields remain **Unknown — verification needed**. Do not fill them from
source timestamps, filenames or an assumed default configuration.

## CPU, memory and firmware boundaries

- Retain the documented NMOS scope of the two published CPU recommendations.
  Other processors need explicit instruction/bus/timing verification; an ISA
  match in a listing does not prove physical CPU identity.
- Define register/flag, D-state, scratch, stack, bank and interrupt contracts
  at every helper boundary. Reassign historical zero-page constants rather
  than importing a program's takeover map.
- Separate ordinary RAM copies from I/O, slot ROM, firmware workspace and
  bank-changing operations. Specify source/destination mapping and restoration.
- Identify exact monitor/BASIC/OS/slot-ROM interfaces, inputs/outputs, clobbers,
  workspace and revision limits. A private binary entry is not a stable API.
- Preserve patch/execution exclusion or compare a non-mutating worker design.
  Startup `SEI` alone is not a proof of runtime IRQ/NMI or reentry safety.

Details and candidate gates are in [CPU and memory](cpu-and-memory.md).

## Display and cross-machine adaptation

The validated semantic collision representation is independent of display
encoding; its historical cell dimensions and special values are not defaults.
The two CPU mechanisms are reusable only under their original contracts.

Hardware renderers are not interchangeable. Apple ordinary HGR row layout and
pixel/bit-7 conventions differ from Oric's six-pixel bytes and serial attributes;
saved backgrounds, clipped recomposition and page ownership need new target
tests. A second page serving as terrain cannot silently become a frame buffer.
See [graphics](graphics.md) and the comparison boundaries in
[Oric portability](../../../Tangerine/Oric/guidelines/portability.md#cross-platform-research-boundary).

No audio or input timing transfers with CPU instructions alone. Foreground
speaker loops, analog polling and actor updates can affect one another's pace;
measure the actual workload and configuration instead of assuming an IRQ rate.

## Disk images and edition provenance

The Lode Runner analysis identifies a DOS 3.3 filesystem in ProDOS image-sector
order. Karateka uses a loader-led reconstruction without a usable DOS catalog;
its logical-sector interpretation is an inference from coherent code/data.
Neither `.dsk` extension authenticates ordering, original release or protection.

Keep host offsets, sectors and phase-specific CPU addresses distinct. The
[Lode Runner extraction notes](../../../../../research/analyses/lode-runner/extracted/README.md)
and [Karateka extraction notes](../../../../../research/analyses/karateka/extracted/README.md)
document mappings. Neither sector image establishes original magnetic timing.
Loader anomalies and patches cannot be attributed to the original authors
without a trusted-edition comparison. No protection bypass is prescribed here.

## Minimum validation matrix

1. **Identity/boot:** pin image and ROM hashes; trace a bounded cold/warm boot and
   one gameplay exchange for every claimed CPU/memory configuration.
2. **Memory:** assert every load/copy/clear range and owner; trace bank changes,
   stack use, vectors, firmware calls and all code-patch transitions.
3. **Graphics:** compare reference images across phase, mirror, mode, edge,
   overlap, terrain changes and both page histories; test color separately.
4. **Input/audio:** exercise controls with silence/effects and changed CPU speed;
   record calibration, foreground latency and interrupt conditions.
5. **Storage:** trace first-level and later scene reads, failed/missing media,
   sector boundaries and recovery before certifying complete loading support.
6. **Candidates:** audit quota cursor writers, record-window commits, stream
   bounds/reentry and patch exclusion under the complete caller workload.
7. **Performance:** after output equivalence, compare total code/table/scratch
   size and elapsed cycles with branch/page/bank and interrupt conditions stated.
8. **Hardware:** repeat timing-, bus- and video-sensitive cases on identified
   hardware; keep emulator observations in a separate evidence class.

Current records do not complete this matrix. The first priority is the bounded
boot/gameplay trace; static model coverage is not a benchmark or compatibility
certificate. Findings remain `analyzed` until their proposed recommendation has
sufficient evidence under an explicit configuration.

## Reference access and evidence limits

The [Apple IIe Reference Manual](https://www.applelogic.org/files/AIIEREF.pdf),
Chapter 4, printed p. 74 / Table 4-6, supports the mapping constraints linked
from the CPU/memory guide. The
[Apple II Reference Manual](https://www.applelogic.org/files/AIIREF.pdf), printed
p. 19, supports ordinary HGR representation, not later-model banking.
These are primary Apple manuals hosted by an archive mirror.

On this review date, the IIe full-PDF fetch timed out; the indexed primary-manual
excerpt was available for the cited mapping passage. A full-page scan check
remains advisable before building a complete soft-switch address/API table.
No such unverified address table, firmware clobber list, IRQ frequency or
performance measurement is invented in these guides.
