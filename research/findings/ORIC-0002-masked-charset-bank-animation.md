---
id: ORIC-0002
title: "Mask-composed charset animation over fixed text codes"
category: graphics
cpu: ["6502"]
machines: ["oric-unspecified"]
status: analyzed
source_analyses: ["../analyses/vip4-demo/overview.md"]
tags: [charset, animation, masking, lookup-tables]
---

# Mask-composed charset animation over fixed text codes

## Summary

**Classification: Oric-specific implementation of a general glyph animation
strategy.** Vip4's ending installs fixed alternate-character codes, updates
masks and composes 256 glyph bytes from a changing bank. The pixel changes
occur in character data rather than moving every displayed text code each
iteration. Historical bank initialization and intended imagery remain unresolved.

## Problem and context

- **Problem:** animate a text-mode display with a bounded glyph-update cost.
- **Use cases:** repeated character tiles, patterned text and font effects.
- **Preconditions:** writable active charset; explicit glyph/code ownership;
  initialized bank pointer, masks and serial attributes.
- **Target:** unspecified Oric model, documented NMOS 6502 instructions.
  Whole-image Oric-1/Atmos compatibility has not been tested.

## Provenance

| Field | Value |
| --- | --- |
| Original program | Local Vip4 Demo / likely Quintessential; exact release match unknown |
| Author / archive / license | Defence Force program attribution; routine author, download origin and license unknown |
| Source | `research/sources/Oric/Vip4 Demo/vip4.dsk` |
| Revision | `a04d227fbbc9252d9dda01641581f4f0dc49a8e3`; ignored image, not a historical source commit |
| SHA-256 | `555e811187069b29bfc6cf657be7f19f8c49aa8d25fbbeeb8ab4718ad2577558` |
| Text setup | M13 CPU `$60DE–$6112`, DSK start `$06FF79` |
| Mask updates | M13 CPU `$6127–$6196`, DSK start `$070028` |
| Compositor | M13 CPU `$6197–$61C7`, DSK start `$070098` |
| Exact mapping | [ending listing](../analyses/vip4-demo/extracted/module-13-selected.asm.txt), [manifest](../analyses/vip4-demo/extracted/manifest.json) |
| First analysis | [H05](../analyses/vip4-demo/hardware-techniques.md#h05-masked-charset-animation-with-stable-text) |

These are binary template locations, not fabricated historical source lines.

## Original implementation

Assembler syntax and original labels are unknown. Setup writes codes `$20–$3F`
at `$BDB4–$BDD3` with the alternate-charset attribute `$09` at `$BDB3`. The
compositor uses indirect bank reads through `$02/$03`, AND masks, and indexed
stores into glyph RAM. No large historical excerpt is reproduced.

## Technical explanation

The first loop has Y=`$20–$FF`: `bank[Y] AND mask[$B2F0+Y]` goes to `$B8F0+Y`,
covering `$B910–$B9EF` (224 bytes). The second loop visits Y=`$0F...$00`:

- `bank[Y] AND [$B300+Y] AND [$608B+Y]` goes to `$B900+Y`.
- `bank[Y] AND [$B3F0+Y] AND [$6083+Y]` goes to `$B9F0+Y`.

Those two 16-byte regions complete the 256-byte charset slice `$B900–$B9FF`,
corresponding to 32 glyphs of eight bytes. Every occurrence of these character
codes shares the same changing glyphs; that is both the benefit and a constraint.
The mask update worker shifts and injects data at a slower cadence.

Bank high starts `$C0`, increments per composition, and wraps zero to `$C0`.
With low byte `$02=0`, this visits 64 aligned 256-byte pages. **The ending entry
does not initialize `$02`.** With another value the source pages mix through
indexed crossing. The upper region also contains prior music/assets/resident
code; a dedicated animation-frame atlas is not established. This record explains
the composition, not the author's unproven data intention.

## CPU-specific considerations

- **Registers/flags:** Y is the byte index; AND supplies N/Z; loop control uses
  INY/BNE or DEY/BPL; the bank high INC controls wrap. The separate IRQ preserves
  A and leaves X/Y alone but occupies nearby zero page.
- **Addressing:** `(zp),Y` reads plus absolute,Y mask reads and stores.
- **Compatibility:** documented NMOS instructions; no later-CPU dependency.
- **Page/interrupt costs:** bank low affects read-cross penalties; mask bases
  are deliberately offset, so not every read is page-aligned. IRQs add elapsed
  time. No frame-sync guarantee is demonstrated.
- **Alignment:** recommend explicit bank alignment; actual inherited low unknown.

## Machine-specific considerations

Oric TEXT character definitions are shared by every on-screen instance of a
code. Serial attributes such as `$09` select the relevant charset; glyph bytes
are six-bit patterns, whereas text cells also encode attributes and inversion.
This is not a free-form HIRES sprite buffer. Writable upper RAM and ROM mapping
affect the original bank reads; exact ending bank contents must be traced.
The [Atmos manual](https://library.defence-force.org/books/content/manual_atmos.pdf)
and [ULA model](https://raw.githubusercontent.com/pete-gordon/oricutron/master/ula.c)
support the hardware interpretation, not whole-demo compatibility.

## Performance and resource costs

| Metric | Original | Alternative | Evidence / method |
| --- | --- | --- | --- |
| Glyph writes per call | 224 + 16 + 16 = 256 | Whole text/pixel redraw depends on region | Exact loop enumeration |
| Glyph slice | 256 bytes at `$B900–$B9FF` | Private nonshared tiles need more definitions or screen updates | Destination union |
| Source bank span | 64 high-byte values; ideal aligned span 16 KiB | Fewer frames or generated glyphs trade storage for computation | High-byte sequence; low-byte initialization unresolved |
| Scratch pointer | `$02/$03`, shared lifetime must be established | Private initialized pointer is safer | Source addressing |
| Cycles / ROM cost | Not measured; conditional read crossings and IRQ interference | Not measured | No benchmark or full renderer timing claim |

## Advantages

- Fixed character placements can display changing glyph pixels.
- Repeated codes reuse the same composed pattern across the screen.
- Masks permit text and effects to share a bounded glyph-update slice.

## Limitations and risks

- All instances of a glyph change together; arbitrary independent sprites are
  outside this mechanism's contract.
- Serial-attribute and charset selection errors change interpretation.
- Historical bank content and low-pointer initialization remain unknown.
- Updating the visible charset during display can tear; synchronization unproved.

## Alternatives

Update text codes from a precomputed tile bank; copy full glyph definitions
without masks; compose a HIRES buffer; or alternate private glyph sets after
verified display synchronization. Compare total bank/mask RAM and visible output.

## Validation record

- **Status:** analyzed byte composition; historical image semantics partial.
- **Evidence:** fixed text-code setup, mask worker, exact glyph-store loops.
- **Theory:** destination coverage and aligned bank-index model in
  [verify_analysis.py](../analyses/vip4-demo/tools/verify_analysis.py).
- **Emulator/benchmark/hardware:** none; no frame was rendered.
- **Open:** initial `$02`, carry at text setup, actual ROM/overlay bank contents,
  mask/font layout and visual synchronization.

## Recommendation for new projects

Use shared glyph animation for repeated tiles or text effects with explicit
charset ownership. Initialize both bank pointer bytes, retain correct serial
attributes and check update timing. Avoid assuming independent per-cell graphics
or copying the original memory layout without resolving its inherited state.

## References and related techniques

- [CPU6502-0005](CPU6502-0005-zero-page-code-operands-as-state.md): the ending's
  IRQ state is a separate CPU mechanism.
- [ORIC-0001](ORIC-0001-background-pages-with-position-metadata.md): saved sprite
  backgrounds differ from shared glyph composition.
- [Vip4 architecture](../analyses/vip4-demo/architecture.md).
