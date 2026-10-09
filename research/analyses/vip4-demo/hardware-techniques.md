---
id: ANALYSIS-ORIC-0002-HARDWARE
program: "Vip4 Demo / Quintessential"
cpu: ["6502"]
machines: ["oric-unspecified", "microdisc"]
analysis_status: draft
source_revision: "sha256:555e811187069b29bfc6cf657be7f19f8c49aa8d25fbbeeb8ab4718ad2577558"
analysis_date: "2026-10-09"
---

# Hardware techniques

## References and evidence boundaries

Locations use the [overview convention](overview.md#references-and-precise-location-convention)
and [routine index](routines.md). The official
[Atmos manual](https://library.defence-force.org/books/content/manual_atmos.pdf),
printed pp. 84–85 and appendix 5, supplies the video map and embedded-attribute
context. It does not prove this executable's model compatibility.
The emulator authors' [disk implementation](https://raw.githubusercontent.com/pete-gordon/oricutron/master/disk.c),
functions `microdisc_read`/`microdisc_write`, and
[ULA implementation](https://raw.githubusercontent.com/pete-gordon/oricutron/master/ula.c),
functions `ula_decode_attr`/`ula_renderscreen`, provide explicit software hardware
models, **not observations of this demo running**. The
[WDC W65C22 datasheet](https://www.westerndesigncenter.com/wdc/documentation/w65c22.pdf),
tables 2-6 to 2-8, distinguishes Timer 1 counter/latch accesses. It is a later
CMOS part reference; actual NMOS 6522 edge timing remains to be verified.

## 5. Machine-specific findings

### H01: Custom sector loader and overlay RAM

Boot:$A7F8–$A83B and R:$FA13–$FA7E program registers `$0310–$0313`, select
hardware control at `$0314`, poll bit 7 of `$0318` and read bytes from `$0313`.
The emulator's model identifies these as WD controller registers, control and
active-low DRQ. This establishes a Microdisc-style dependency; Jasmin/Pravetz
interfaces cannot be assumed to share it. `$85/$84` select upper RAM on this
control model, with side bit `$10` ORed for side 1. Code, data and IRQ vectors
occupy this RAM instead of relying on BASIC services during the traced core.

Each read is 256 bytes. A short delay follows command `$80`, then a polling
loop transfers every byte; no throughput or rotation timing is measured. Track
seek uses command `$1F` if the requested track differs from `$0311`.
The status mask is `$1C`. The resident loop advances pages even without a
source-visible retry/status check. CPU-side I is set throughout the load path;
see [C02/C06](cpu-techniques.md) for dormant IRQ and retry limitations.

The arrays are compile-time sector descriptors, not a demonstrated general
filesystem. The [Oricutron container reader](https://raw.githubusercontent.com/pete-gordon/oricutron/master/disk.c)
confirms header fields and 6,400-byte track records. All sector CRCs were checked
locally; that proves image integrity, not successful mechanical disk reading.

### H02: Display bytes, whole-screen clears and reduced raster work

HIRES uses 40 bytes per row and 200 rows, with six pixels per pixel byte and
serial attributes embedded in the stream. `$40` is a pixel marker with zero
low pixel bits; arbitrary low-valued bytes are not interchangeable pixels.
These facts constrain every blitter and mask composition.

R:$FB1F's partially unrolled clear covers exactly `$A000–$BF3F`, using a
192-byte overlap to handle the tail. It does not clear the following text/status
area. M0B:$8A7C uses a different tail base `$BEE0`, reaching `$BFDF`; the two
clearers should not be merged by assuming they have identical visible effects.
R:$FB08 clears text to zero rather than ASCII space and stops before `$BFE0`
music state. Meaning depends on the charset/mode in effect at that moment.

M0B:$883B–$88A1 copies 29 bytes for each of 66 rows, with destination stride
120. M0B:$89D9–$8A18 copies 18 bytes for each of 43 rows with the same stride.
Writing every third scanline is explicit in the addresses; the inference that
neighboring lines supply a color/motion treatment requires rendered-frame
verification. The dancer copy is an overwrite, not a demonstrated masked
sprite blit. Background generation/refresh can restore overwritten pixels;
no per-dancer saved-background algorithm is established here.

### H03: VIA timer/music ABI and direct PSG control

R:$F9C6–$FA12 writes DDRA/DDRB, IER=`$7F` then `$C0`, ACR=`$40`, and T1 latch
bytes `$10/$27`. It installs vector `$0245` and builds
`PHA; LDA $0304; PLA` at `$0245–$0249`. M00:$C000 installs JMP `$C035` at
`$024A–$024C`, completing the trampoline. The counter read acknowledges T1
before dispatch. The player saves A/X/Y, updates three voices and effects,
writes AY registers 10 down to 0 from `$CCC5,X`, restores registers and RTIs.
Music timing and format details beyond this interface remain partial.

Writes to `$0306/$0307` update the latches; `$0307` is **not** the T1 counter
high start register (`$0305`). Consequently the observed `$2710` latch does not
by itself establish when the first IRQ occurs. Later steady timing depends on
free-run mode, the existing counter state and exact VIA revision. This also
applies to the sample routines' changed latches. Do not report exact 100 Hz or
sample rate based solely on the hexadecimal constants.

PSG transactions use VIA port A without handshake at `$030F` and PCR sequences
`$FF,$DD` (register select), then `$FD,$DD` (data write). Port and control-line
ownership must be exclusive; keyboard and ROM services share this circuitry.
R:$F98D silences registers 0–10 and installs vector `$8AFC`. The resident
contains an RTI byte at `$FC8A`, but the two immediate values install the address
in reversed byte order. `$8AFC` changes meaning with overlays; in M0B it is a
STA instruction, not RTI. **The installed target is `$8AFC`, not `$FC8A`.**
The helper issues no SEI, and several preceding effect paths enable IRQs.
Both the transient vector between the two stores and its final target need
tracing before this can be treated as a safe interrupt-disable function.

### H04: Packed nibbles and two IRQ playback designs

M02:$9D0D–$9DD5 and the identical player structure in M04 select fast T1 latch
`$007D`, relocate code to zero, set X=`$DD`, Y=`$FF`, then enable IRQs while the
foreground only polls the high byte of the executable sample pointer.
The low-nibble handler at `$00` writes AY volume register 8 and caches the byte
in immediate operand `$2F`. It swaps the vector low byte to `$25`. The second
handler writes the high nibble to register 9, changes the vector low byte back
to zero and increments the pointer. Samples read `$1000–$9BFF` before the high
pointer reaches `$9C`. Each byte supplies two channel-volume updates on alternate
IRQs. This does **not** alone establish stereo intent, a linear PCM transfer
function, or consecutive mono samples; AY volume codes are not linear amplitudes.

The ending's relocated IRQ `$10–$3F` uses a single selected volume register and
a self-modified phase operand. It sends low then high nibbles on consecutive
IRQs, advances the pointer and wraps `$8000` to `$67BF`. Setup copies the IRQ
template after the resident patches its source pointer at `$60A3/$60A4`.
It keeps X/Y intact and restores A from an immediate operand instead of PHA/PLA.
PCR is left in a write state rather than strobed for every sample; actual
chip-level behavior and audio quality require hardware checking.

The ending initializes T1 counter high zero, then low/latch `$C8`, and ACR=`$50`.
SR is written `$55`, T2 counter is cleared, and PCR is configured. Shared timer,
shift-register and control-line interactions make nominal latch-derived rates
inadequate evidence of actual playback frequency. No audible output was tested.

### H05: Masked charset animation with stable text

**Analyzed byte composition; ORIC-0002.** M13:$60DE–$6112 fills 28 text rows
with `$08`, populates a line of character codes `$20–$3F` and selects alternate
characters using `$09` at `$BDB3`. M13:$6127–$6196 shifts masks, injects text/font
data and controls slower updates. M13:$6197–$61C7 combines banked data and masks
into selected glyph bytes at `$B910–$B9EF`, `$B900–$B90F` and `$B9F0–$B9FF`.
Thus movement can be produced by changing glyphs rather than moving the text
codes every iteration. The first pass writes 224 bytes, the second 32 bytes,
for 256 glyph-byte stores per call.

The bank pointer high byte starts `$C0`, advances once per call, and wraps zero
back to `$C0`. Its low byte `$02` is inherited, not initialized in this entry.
With `$02=0` this selects 64 aligned 256-byte banks; otherwise indirect reads
may cross pages and mix banks. `$C000–$FFFF` overlaps music, `$D000` assets and
resident loader bytes. The examined code does not establish that it is a
dedicated 64-frame atlas, or that ROM is re-enabled for the read. Treat the
masking algorithm as explained, and the historical bank's visual intention as
unresolved. See [ORIC-0002](../../findings/ORIC-0002-masked-charset-bank-animation.md).

## 6–9. Verification, comparisons and next tests

No hardware technique was benchmarked or promoted. The existing background-page
finding [ORIC-0001](../../findings/ORIC-0001-background-pages-with-position-metadata.md)
uses per-object restoration and differs from overwriting selected glyphs.
General operand patching is recorded once under the CPU findings.

Trace: actual disk-side requests; `$0314` bank switches; I flag around `$F98D`;
T1 counter versus latches and SR state; executable zero-page ownership; AY
register/volume writes; `$02` at ending entry; rendered serial attributes and
all glyph destinations. Repeat relevant checks on hardware before inferring
timing, audio fidelity, screen synchronization or model compatibility.
