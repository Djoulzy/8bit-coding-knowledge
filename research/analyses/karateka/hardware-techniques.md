---
id: "ANALYSIS-APPLE2-KARATEKA-HARDWARE"
program: "Karateka"
cpu: ["6502"]
machines: ["apple-iie"]
analysis_status: complete
source_revision: "d02edc77fa0a02d3f679af22456ca1c762c305dc"
analysis_date: "2026-10-11"
---

# Apple II graphics, input, audio and disk techniques

The folder says Apple IIe; the author identifies the original game as Apple II.
Exact machine/ROM/disk edition is unknown. [Overview](overview.md) records
provenance; [architecture](architecture.md) defines memory phases and disk offsets.
Source references below are byte locations in the supplied disk, not historical
symbol names. CPU flag/patch mechanisms are explained in [CPU techniques](cpu-techniques.md).

## H01: page-relative HGR addressing

**Evidence:** tables `$0800–$097F`, `DSK=$00A000–$00A17F`;
renderer pointer formation `$1984–$1998`, `DSK=$009184–$009198`.
**Level/status:** machine; analyzed.

The code has two 192-byte arrays, low at `$0800`, high at `$08C0`. Their combined
values exactly match the page-relative row formula:

~~~text
row_offset(y) = (y mod 8) × $0400
              + ((y div 8) mod 8) × $0080
              + (y div 64) × $0028
address = page_base + row_offset(y) + byte_column
~~~

All y=0..191 entries are checked; legal byte columns 0..39 do not carry out
of the row low byte. The renderer therefore adds column to low and draw-page
selector to high independently. This reasoning depends on the checked table
and legal dimensions, not an arbitrary split-address arithmetic shortcut.

The use of seven pixel bits and separate bit-7 display metadata follows the
[Apple II reference documentation](https://www.applelogic.org/files/AIIREF.pdf).
The local code sets bit 7 in drawn bytes and works on pixel fields; its exact
artifact-color result on different monitors/board revisions was not rendered.
Out-of-range vertical positions can index beyond row arrays: no full vertical
clip or arbitrary-row safety was established.

## H02: shifted and mirrored packed rows

**Evidence:** source-header setup `$1A61` (`DSK=$009261`), normal loop
`$1927–$1A33` (`DSK=$009127–$009233`), shifter `$1A84–$1AEA`
(`DSK=$009284–$0092EA`), mirror `$1AF4–$1C5A`
(`DSK=$0092F4–$00945A`), table `$0980–$09FF`
(`DSK=$00A180–$00A1FF`). **Level/status:** machine; analyzed locally;
new [APPLE2-0003](../../findings/APPLE2-0003-runtime-sprite-shift-and-reflection.md).

Sprite records start with height and byte width, followed by row-major bytes.
Normal drawing shifts each seven-pixel field by phase `$10`, joins the current
low fragment with the previous overflow and preserves boundary bits. Source
stride remains the original row width even when horizontal clipping reduces
visible bytes. Mode `$0F` chooses copy, OR or AND through CPU patch sites.

The reflected path changes nonzero phase p to `7−p`; phase zero instead
decrements the byte anchor. It reads source bytes in ascending order but
writes decreasing destination offsets. Every table lookup forces bit 7 first,
so `LDA $0900,X` actually addresses `$0980–$09FF`; its apparent 256-byte
base overlaps the row-high array in the unused lower half. The 128 used entries
are `reverse7(pixel_bits) OR $80`. This is a verified compact table layout,
not a pair of nibble tables or full eight-bit reversal.

Leading/trailing masks at `$1A34/$1A3B` retain pixels outside the affected
phase. The mirrored worker saves/restores `$05/$10`, wrappers restore source
pointer `$03/$04`, and worker returns restore saved X/Y. Scratch/flags are not
generally preserved. The height/width and phase bounds are caller requirements;
horizontal clipping is present, but full zero-size/edge/mode correctness remains
to be tested with a reference image.

## H03: mask and image layer composition

**Evidence:** actor drawing `$6811–$693C`, first byte `DSK=$004011`;
normal mask/image sequence `$687B–$688D`, `DSK=$00407B–$00408D`;
mirror counterpart `$6904–$6919`, `DSK=$004104–$004119`.
**Level/status:** common composition with machine encoding; analyzed locally.

Per-frame pointer and offset arrays choose several actor layers. Selected paths
draw an AND mask (`$0F=$FF`) then an OR image (`$0F=$00`); other draws select
positive opaque mode. This gives `screen = (screen AND mask) OR image` for
the corresponding pixels if coordinates, shifted masks and layer order match.
It does not by itself implement alpha blending or arbitrary HGR color correctness.

This resembles Lode Runner's [APPLE2-0001](../../findings/APPLE2-0001-paired-hires-background-masks.md)
composition, but its baseline-save/erase contract is not established here.
Karateka repairs scene regions from patterns/layers and keeps page history;
do not transplant the Lode Runner paired-background invariant into this renderer.

## H04: alternating pages and retained repair geometry

**Evidence:** `$7609–$7627`, `DSK=$004E09–$004E27`; history
`$A316–$A344`, `DSK=$001B16–$001B44`; repair `$678F–$680E`,
first byte `DSK=$005F8F`, crossing the `$67FF/$6800` disk mapping boundary.
**Level/status:** common redraw organization plus machine page switches;
analyzed local flow; related [GEN-0003](../../findings/GEN-0003-clipped-scene-recomposition.md).

The completed draw page is displayed via `$C054/$C055`, then the next draw uses
the other selector. Older positions/phases are retained in paired globals;
actor repair reads the older coordinates, clears spans and restores patterned
background through `$0A00/$0A03` and high scene helpers. This supplies concrete
evidence of repair across alternating pages, but all scene/layer dependencies
and dirty bounds have not been proven. This is direct repair in full video pages,
not Space: 1999's small offscreen occlusion scratch rectangle.

The conditional wait at `$779A` (`DSK=$004F9A`) and `$07D7`
(`DSK=$009FD7`) polls `$C019` while bit 7 is set, only when ROM `$FBB3 == $06`.
The [Apple IIe manual, printed p. 157](https://www.applelogic.org/files/AIIETECHREF3.pdf)
documents changing display state in the low interval. The loop can return
immediately if already low; it does not wait for a new edge, prove every frame
fits that interval, or establish an IRQ. Full fetch of this PDF timed out;
the publisher-manual searchable excerpt supplied the polarity reference.

## H05: page transfers for intro and scene transition

**Evidence:** `$0786–$0798`, `$07B9–$07D6`, `DSK=$009F86`, `$009FB9`;
`$774B–$778D`, `DSK=$004F4B–$004F8D`. **Level/status:** machine;
analyzed loops; visual effect inferred.

Intro copies 190 × 40 = 7,600 visible bytes: other-page rows 2..191 into
draw-page rows 0..189. It leaves the bottom two rows for other drawing. The
following flip updates `$E4` as the next source page; this is software row
copying across buffers, not hardware scrolling.

The column transfer copies 192 × 40 = 7,680 visible bytes from draw page to
other page. Y selects a column, X enumerates rows; after each column it checks
pause input and tail-calls monitor delay `$FCA8`. No page switch occurs inside
this worker. A progressive scene wipe is the likely visual purpose, but neither
the timing nor displayed transition was observed. Copying visible bytes excludes
the 512 allocation holes; HGR clear `$190F` instead writes the full 8,192-byte page.

`$0ABF` clears bit 6 of byte column 39 over the interleaved draw-page rows.
This is a specific edge cleanup convention, not evidence that bit 6 is generally
metadata; it is one of the seven displayed pixel bits.

## H06: keyboard/buttons and speaker in the foreground

**Evidence:** `$B7EA–$B822`, first byte `DSK=$008FEA`;
`$7697–$7720`, `DSK=$004E97`; `$0D00–$0DA5`, `DSK=$00A500–$00A5A5`;
`$0DC0–$0DF9`, `DSK=$00A5C0–$00A5F9`; service `$7628–$7696`,
`DSK=$004E28–$004E96`. **Level/status:** machine; analyzed local effects.

Keyboard polling reads `$C000` and clears the strobe through `$C010`.
Title button polling retains `$C061/$C062` values and detects state changes.
Some control keys toggle global sound/input flags. Complete paddle and key
action mapping remains outside the detailed review. Hardware address meanings
are cross-checked against the [Apple Red Book I/O equates](https://downloads.reactivemicro.com/Apple%20II%20Items/Documentation/Manuals/Apple%20II%20Reference%20Manual%20-%20The%20Red%20Book/2023-04-27%20-%20Apple%20II%20Redbook.pdf).

Speaker accesses to `$C030` occur in synchronous busy loops. `$0D00` reads a
stream: initial bytes patch immediate timing values, `$FE` selects NOP/NOP,
`$FD` selects LDY immediate plus a following operand at `$0D79/$0D7A`, and
`$FF` ends. Ordinary records feed duration/counter fields. This shares the
equal-width patch principle with C02, though the flags/register/timing contract
differs. `$0DC0` processes eight bits per input byte and toggles only when the
current sign bit differs from retained sign state `$9B`; delay uses `$BA`.
Its pointer-low initialization/reuse needs a wider caller audit.

No custom music interrupt was established. Sound consumes foreground CPU time
and may affect update latency; exact sample rate, pitch, duty cycle and interruption
behavior remain unmeasured. Do not import Oric VIA/PSG or timer claims here.

## H07: disk boot versus later raw-read paths

**Evidence:** initial `$B715`, `DSK=$000115`; runtime `$020C–$025D`,
`DSK=$009A0C–$009A5D`; `$0300–$03ED`, `DSK=$009B00–$009BED`.
**Level/status:** machine; initial core mapping analyzed, later protocol observed.

Initial loading uses DOS-style RWTS without a valid DOS catalog. Later code
copies `$C600` firmware to `$4600`, patches it and transfers into the copy.
Other helpers poll disk controller registers, check a nonstandard marker sequence,
decode bytes into `$4000` and call that loaded code. A 256-byte exchange with
`$4F00` temporarily moves ZP state. These are strong candidates for scene-loading
or protection research, but the complete data protocol and selected disk
provenance are unresolved. A sector `.dsk` is not a capture of original physical
track timing/protection. No protection bypass or original-edition equivalence
is claimed.

## Verification and next work

Local checks are in [verification.json](verification.json). All named hardware
dependencies are either connected to primary Apple documentation or explicitly
unresolved. No hardware benchmarks or portability certificates were produced.
Trace page selection and one actor mask/image pair before expanding to complete
clipping, scene overlays, sound timing or other Apple II variants.

