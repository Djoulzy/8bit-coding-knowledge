---
id: "ANALYSIS-ORIC-SPACE1999-OVERVIEW"
program: "Space: 1999 (French disk; supplementary published source)"
cpu: ["6502"]
machines: ["oric-atmos"]
analysis_status: complete
source_revision: "local repository aa45faba50a848ff725c40f61ccd438fa4e25b79; upstream c81612082482d1f497638ada14ad4640c5e4f1ec; input hashes in verification.json"
analysis_date: "2026-10-09"
---

# Source-code analysis: Space: 1999

## 1. Objective and scope

Analyze `research/sources/Oric/Space 1999` in full report mode. The supplied directory contains a French DSK image, metadata and a README, **no assembly source**. This report therefore separates local binary facts, the README's historical claims, and supplementary published source at a pinned revision. “Complete” describes the required report set, not exhaustive reverse engineering or successful execution.

Deep inspection covers NOISE screen addressing, clipping, sprite compositing and occlusion; WHITE room loading and movement coordination; game startup and loop; grammar decompression; disk transfer and IRQ handover; keyboard and audio register submission. Inventory-level coverage includes collision branches and general game logic. Intro artwork/effects, all puzzles, every audio opcode, Sedoric filesystem allocation and a complete executable-to-source comparison remain outside deep coverage.

## 2. Source provenance

| Field | Evidence |
| --- | --- |
| Supplied version/date | README identifies version 1.00, February 2008, L1–L7 |
| Authors | Chema: principal code; Twilighte: graphics, music, effects and keyboard; Dbug: intro and development, README L99–L101 |
| Additional credits | Sam Hocevar: scene conversion; Maximus: French translation; Waskol: testing/tools; Fabrice Frances: sector access, README L103–L113 |
| Original publication date | Not established for this disk. The publisher page displays September 26, 2004; this differs from the supplied README's version date |
| Source archive | Published game source in the [Oric Software archive](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source), commit `c81612082482d1f497638ada14ad4640c5e4f1ec` |
| License | No explicit game-code license identified in the inspected text. Free game availability is not a code reuse license; no full source mirror or binary payload is redistributed here |
| Local revision | Repository HEAD `aa45faba50a848ff725c40f61ccd438fa4e25b79`; input files ignored by `.gitignore`, so their hashes are the reproducible identity |
| Dialect | OSDK/XA assembly: `.zero`, `.text`, `.bss`, `.dsb`, `.byt`, scoped `.(….)`, exported `+` labels, preprocessor includes/defines; Windows batch build orchestration |
| Supplemental intro | OSDK C and assembly, configured separately at `$0600`; this archive does not support calling the entire release “100% assembly” without qualification |

The [publisher page](https://defenceforce.itch.io/space-1999) identifies Chema Enguita, Jonathan Bristow and Mickaël Pointier, requires Atmos, and links the source archive. Local README attribution is preserved; ownership of individual uncredited routines is not invented. The readme's “100% asm” statement at L23–L31 describes the game, while the published intro contains C.

| Supplied input | Bytes | SHA-256 |
| --- | ---: | --- |
| `space1999-fr.dsk` | 192256 | `9d85e1d75d9f1e548f4d1e3bc3750085e7c8c125bb6cd110fb604ba86ba3e851` |
| `space1999-readme.txt` | 5801 | `e8b406282e743a5a1c52920682b843fc3d1a844f1885ab227dbe938ecd0856bb` |
| `metadata.md` | 106 | `1b6b677cd43ad66cbe859b3568c6a58c75146ff59be275bc52648b3f3319ee14` |

[upstream-manifest.json](upstream-manifest.json) records 83 selectively downloaded text files, original byte hashes, Git blob identities, line counts and exact URLs. Files were read in a scratch directory; historical executables and build scripts were not run.

## 3. Target environment

NMOS MOS 6502; Oric Atmos with 48 KiB base RAM and accessible upper overlay RAM through a Microdisc-compatible interface. HIRES rendering uses `$A000` and a 40-byte scanline. VIA, AY-3-8912, keyboard matrix and WD17xx-compatible disk access are relevant. The game replaces the IRQ vector in overlay RAM. Exact ROM bytes and model of physical disk controller are unknown. No emulator or real hardware was run; Oric-1 compatibility is explicitly unsupported by local metadata and the publisher.

## 4. Program architecture

Two-stage startup: Sedoric launches the intro; the intro changes startup behavior and reboots; later warm resets launch the game (README L52–L62). The game takes over overlay RAM, loads map/audio sectors and installs a private IRQ. WHITE coordinates movement and room state; NOISE renders the isometric scene. See [architecture](architecture.md) and the [routine inventory](routines.md).

## 5. Analysis findings

Three distinct provisional fiches: clipped scene recomposition, stack-driven binary-pair text expansion, and parity-compressed Oric pixel tables. CPU findings also include writable instruction operands, optional JSR hooks, narrow shift/add arithmetic, IRQ-context disposal and separate interrupt scratch state. These are source analyses, not best-practice certification. See [findings](findings.md).

## 6. Performance and verification

`tools/inspect_inputs.py` verifies the local MFM geometry and CRCs. All 510 sectors have valid identifier and data CRCs; payload total is 130560 bytes. Every logical sector has a recorded original DSK offset. Logical offsets are analysis coordinates, **not CPU addresses**.

Exact comparisons with the published source:

- The 9722-byte `world/world.s` map equals the local disk at logical offset `$6800` (zero-based sector 104), with 114 distinct room IDs.
- The 256-byte grammar equals bytes at logical offset `$1D3C3`; all 128 tokens form an acyclic grammar.
- The disk IRQ instruction signature occurs at logical offset `$1A0E2`. Masked operands establish a matching sequence, not a unique linked module or execution trace.

An arithmetic model using the source's actual tables verifies 48000 legal screen coordinates. Grammar modeling finds longest token expansion of eight output bytes and at most four pending tokens, excluding sentinel, return addresses and nested calls. These are static checks; no cycle benchmark or measured frame rate exists. Full executable identity is **unproven**, despite exact shared data.

Reproduce without executing historical code:

```sh
python3 research/analyses/space-1999/tools/fetch_references.py /tmp/space1999-reference-review
python3 research/analyses/space-1999/tools/inspect_inputs.py --upstream /tmp/space1999-reference-review --output /tmp/space1999-verification.json
python3 research/analyses/space-1999/tools/verify_reports.py
```

The destination must be new; network access is required for the first command. Without `--upstream`, the collector verifies only local input and sector evidence. [verification.json](verification.json) is the recorded complete run.

## 7. Comparison with the knowledge base

Existing CPU6502-0006 describes the IRQ-frame/RTS mechanism; this program supplies an enabled transfer-path example. GEN-0002's semantic collision separation is corroborated with a richer layered scene. Equal-width executable patches relate to CPU6502-0001. These IDs are cross-linked, without duplicating fiches or changing their existing validation status.

## 8. Documentation produced

Six reports in this directory, three new provisional fiches under `research/findings/`, three analysis tools and two JSON manifests. The tools inspect inputs, fetch pinned references and verify report references. Imported files and `docs/` guidelines remain untouched.

## 9. Open questions and next tests

First establish the French executable's exact linked map from Sedoric file allocation and source reproduction. Then trace room transitions, all movement directions and dirty-region bounds in an Atmos/Microdisc emulator. Investigate map-clearing bounds, early collision-callback returns, IRQ/main timer races, save-block length and I/O failure handling. The user manual mentioned in the README is absent locally.

## 10. Summary

The strongest evidence is exact disk/map/grammar correspondence plus pinned source spans. The most reusable ideas trade a small working set and compact data for more complex recomputation and control flow. No findings were promoted to guidelines.

## References

- [Local README](../../sources/Oric/Space%201999/space1999-readme.txt), L23–L31, L52–L66, L99–L143.
- Build/module order: [upstream `game source/osdk_config.bat:L8–L24`](https://github.com/Oric-Software-Development-Kit/Oric-Software/blob/c81612082482d1f497638ada14ad4640c5e4f1ec/games/Space%201999/Sources/game%20source/osdk_config.bat#L8-L24).
- [CPU report](cpu-techniques.md), [hardware report](hardware-techniques.md), [finding index](findings.md).
