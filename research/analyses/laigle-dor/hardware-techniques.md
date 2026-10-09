---
id: ANALYSIS-ORIC-0001-HARDWARE
program: "L'Aigle d'Or"
cpu: ["6502"]
machines: ["oric-1", "oric-atmos"]
analysis_status: draft
source_revision: "sha256:7f01e1a3d05825aab887952cd5711bea69d6525730aba5c1e25c814334fe77d7"
analysis_date: "2026-10-09"
---

# Oric hardware techniques

## Evidence and reference model

Loaded addresses refer to B2 unless B1 is stated. Convert them to exact tape
offsets using [the overview](overview.md#precise-reference-convention). All
implementation explanations are `analyzed`; author intent and untraced runtime
conditions are identified separately. Compatibility is intended for Oric-1 and
Atmos, but neither firmware image was supplied or executed.

The primary [Atmos manual](https://library.defence-force.org/books/content/manual_atmos.pdf),
chapters 7–8 and appendices 5, 9–10, supplies the memory, graphics and firmware
model. The [Oric service manual](https://www.cpcwiki.eu/imgs/7/70/Oric_-_Service_manual.pdf)
supplies the hardware context. The authors' [Oricutron ULA implementation](https://github.com/pete-gordon/oricutron/blob/master/ula.c)
corroborates display decoding; it is implementation evidence, not a hardware
measurement. OCR errors in scanned manuals are not adopted as instruction or
address facts.

## H01: Byte-column coordinates and six-pixel alignment

**Category:** Oric-specific technique. **Source:** B1 BASIC 1010–1020 and
generated `$0400`; B2 BASIC 90 and `$3E21–$3E3A`, `$3E52–$3E77`.

HIRES uses 40 bytes per scanline and 200 scanlines, giving 8,000 bytes at
`$A000–$BF3F`. The six low bits describe a six-pixel group; bit 6 distinguishes
ordinary graphic data from the low-valued serial attributes used here, and bit
7 provides inverse video. The game translates the ROM pixel cursor x to
`INT(x/6+1)` and keeps y in scanlines. Machine arithmetic computes
`$A000 + 40*y + byte_column` and renderer wrappers adjust the pointer convention.

The likely benefit is moving an entire six-pixel group with one byte transfer,
avoiding bit shifts and adjacent-byte assembly. Motion records therefore encode
byte-column deltas. This gives coarse horizontal placement; no arbitrary
one-pixel sprite shifter was established. The address helper has no screen
clipping: byte arithmetic outside valid coordinates can write other memory.
Port the byte-oriented idea to similarly packed displays; replace the stride,
pixel encoding and boundary rules for another machine. CPU arithmetic costs and
alternatives are in [C05](cpu-techniques.md#c05-general-multiplication-used-for-a-constant-stride).

## H02: Attributes emitted beside sprite rows

**Category:** Oric-specific technique. **Source:** `$4000–$402A`,
`$402D–$4076`, wrappers `$4082/$408E/$4840`, BASIC 6510 and 9030.

After copying each row, `$4000` writes `$6C` at destination offset 1. The
attribute wrappers decrement the byte-column first, reserving this left cell
while retaining the ordinary sprite descriptor width. The copied first byte is
then replaced by an attribute: this is a layout convention, not an extra
out-of-band color plane. BASIC also uses `FILL` to establish long attribute
runs. Attribute values affect following bytes on that scanline until superseded.

`$402D` first saves each old screen byte. If the saved byte equals `$0A`, it
stops and `$4069` records `original_height - remaining_height` in the background
descriptor. `$0A` is a text-attribute value, not an arbitrary pixel mask. Its
use as a local stopping marker is verified; the intended geometry/occlusion
meaning is inferred. A stop in mid-row can leave a partly modified row excluded
from the recorded complete-row height; a zero recorded height also interacts
badly with countdown blitters. Trace the actual marked backgrounds before
calling this a general clipping algorithm.

Embedding attributes is compact and directly fits the ULA, but sprites can
change colors to their right and cannot have independent per-pixel palettes.
The OR compositor at `$3E56` combines entire bytes: applying it to attributes
can change control values, not merely add pixels. It is reusable only with
explicitly compatible pixel/attribute regions. The CPU patch mechanism is
documented once in [CPU6502-0001](../../findings/CPU6502-0001-two-byte-render-patches.md).

## H03: Save-under sprites with position-bearing buffers

**Category:** Oric-specific implementation of a general 8-bit technique.
**Source:** `$3E78–$3EAE`, `$3ECF`, `$4140–$415B`, `$4574–$458C`;
attribute variant `$4840–$4858`.

Moving images save old video bytes into tightly packed background buffers,
then draw their new bytes. Restoration uses the same descriptor loader and
blitter as ordinary images. Each active page stores its old byte-column and
scanline at offsets `$FE/$FF`; erasure therefore needs no separate global
coordinate pair for each layer. Six loaded save-slot descriptors occupy pages
`$5200–$5500,$5800,$5900`; their pixel areas fit below those metadata bytes.

This reduces redraw work for small actors on a largely static room and preserves
attributes along with pixels. It costs six 256-byte allocations and requires a
consistent layer restoration order. Drawing another object into a saved area
can be undone by a later restore. `$5900` has a second charset-related owner
during darkness transitions, so lifetime separation is essential. Static buffer
capacity is verified; arbitrary overlapping animation correctness is not.
See [ORIC-0001](../../findings/ORIC-0001-background-pages-with-position-metadata.md)
for the original layout, exact references and reuse conditions.

## H04: TEXT/HIRES overlays and charset lifetimes

**Category:** Oric-specific technique. **Source:** B2 BASIC 1, 3005,
6000–6100; `$4E00–$4E28`, `$4EEA–$4F06`; image `$9800–$9FFF`.

The game switches between HIRES room views and TEXT interfaces. TEXT screen
memory `$BB80–$BFDF` overlaps the HIRES bitmap, and its charset area starts at
`$B400/$B800`. HIRES character definitions are below the bitmap at `$9800/$9C00`;
the three bottom text rows occupy `$BF68–$BFDF`. These regions must be modeled
by display phase, not counted as independent spare RAM.

In darkness BASIC switches to TEXT, prints a message, waits, then CALLs `$4EEA`.
That routine preserves exactly 256 bytes `$B8F0–$B9EF` in `$5900–$59FF`, then
clears `$B400–$BB7F`. Later `$4EF8` calls firmware and restores the saved bytes.
The sequence suggests preserving custom character definitions while hiding the
display. The save/clear/restore byte ranges are established; the exact glyph
contents and both ROM call effects require runtime inspection. This is not a
full 1,024-byte or full dual-set charset backup.

The likely advantage is a cheap mode-dependent visual effect while retaining
selected custom glyphs. Costs include destruction of overlapping video data,
dependence on font relocation by ROM and reuse of sprite-buffer RAM. New Oric
projects can reuse lifetime planning and selective font preservation, but should
define the exact set of characters needed and track every region's owner.
Loop alignment costs are in [C09](cpu-techniques.md#c09-alignment-penalty-in-a-256-byte-charset-restore).

## H05: VIA latch changes with the ROM interrupt service retained

**Category:** Oric-specific use of the 6522. **Source:** B2 BASIC 3000,
4000, 9030; timer reads in enemy code `$49E9–$49EE` and `$4ACE–$4B3D`.

`DOKE #306,#2710` and `DOKE #306,#FFFF` write the low/high **Timer 1 latch**
registers at `$0306/$0307`. They do not write the counter-high register at
`$0305`. In free-running mode the latch supplies a future reload; latch writes
alone do not establish an immediate new timer interval. The distinction follows
the original [MOS 6522 documentation](https://www.bitsavers.org/components/mosTechnology/_dataBooks/1982_MOS_Technology_Data_Catalog.pdf),
Timer 1 register operations and free-running mode.

No game-owned interrupt vector, IRQ handler or `RTI` path was established.
Keyboard polling and ROM software timers remain dependencies. Enemy decisions
sample a ROM timer byte at `$0276`, producing timer-dependent variation rather
than a demonstrated random generator or video phase lock. The probable reason
for different latches is changing the pace/service rate between interfaces and
gameplay; exact IRQ frequency depends on the existing ACR, counter phase and
firmware handler. No frequency or frame rate is claimed from these writes.

Changing this timer can affect all ROM services sharing it, including input
latency and delays. It is not portable to other 6522-based machines at these
addresses. Reuse requires reading the firmware's timer setup and defining how
keyboard, sound and game timing continue to work together. The sequential DOKE
stores and any interrupt between them also deserve tracing.

## H06: AY-3-8912 effects through BASIC firmware

**Category:** Oric-specific firmware interface; no custom AY optimization found.
**Source:** B1 BASIC 8–18, 1100–1200, 1400–1450; B2 BASIC 97,
4110–4150, 6215–6320, 6500–6520, 7015, 8100–8215, 12035–12130.

Music and effects use `MUSIC`, `SOUND`, `PLAY` and built-in effect tokens. BASIC
loops vary frequencies or control parameters; commands explicitly stop effects
in several exits. No application routine that selects and writes AY registers
through VIA ports was identified. The ROM interface reduces game-side code and
retains the keyboard integration of the standard hardware, whose AY port and
VIA connections are shared with keyboard circuitry (service manual).

Costs include interpreter and ROM overhead, firmware state/clobber dependencies
and sound timing tied to game/control paths. No separate IRQ music sequencer or
precise note timing was established. High-level control of low-level audio is a
reusable architecture; these command conventions require Oric ROM support.
Direct AY programming would be an alternative for a new engine, with explicit
responsibility for preserving keyboard use. No comparative benchmark exists.

## H07: ROM input and two-level key dispatch

**Category:** General 8-bit table dispatch plus Oric-specific input service.
**Source:** B1 GET lines 1580/1690; B2 BASIC 5030–5050, 7100;
`$4300–$43FF`.

`KEY$` obtains the key through firmware. BASIC 5050 multiplies its ASCII value
by two and DEEKs a little-endian **BASIC line number**, then GOTO dispatches it.
This is not a 6502 jump-address table. Unassigned entries contain `$5555`, which
maps to the actual BASIC fallback line 21845 at `$3BF4`, returning to 5100.
The table has 128 words; values outside its intended ASCII domain need checking.

This separates bindings from action code and avoids a long sequence of key
comparisons. BASIC still searches/executes a target line, and the table alone
does not guarantee constant total dispatch time. Input repeat behavior, IRQ
latency and ROM key translation require execution. Preserve the data-driven
dispatch idea for reuse; choose the target representation appropriate to the
new language/runtime. Hardware matrix scanning was not implemented here.

## H08: ROM-version adaptation and implicit ABI

**Category:** Oric-specific technique. **Source:** B2 BASIC 42 and
`$4EF8–$4F06`; graphics cursor import `$3E18–$3E20`, BASIC 90.

The game tests `PEEK(#FFF9)=1` and patches byte `$4EF9` to `$D0`, changing a
JSR from `$F89B` to `$F8D0`. This is a one-byte ROM-entry adaptation; it does
not prove a complete model detector or compatibility with every ROM variant.
The surrounding save/restore makes a charset-reset role plausible, but the
entry's registers, side effects and exact operation are not asserted without
the corresponding ROM images.

The renderer also borrows firmware graphics cursor address `$10/$11`, pixel
coordinates `$0219/$021A` and the BASIC workspace containing its scratch area.
This saves duplicate state but couples the engine to ROM calling sequences.
Zero-page ownership and destructive register contracts are covered in
[C01](cpu-techniques.md#c01-zero-page-parameter-blocks-and-register-roles).
For reuse, define a verified firmware adapter and keep model-specific entries
in it; validate cursor and font behavior for each supported ROM checksum.

## H09: Local movement instead of whole-screen scrolling

**Category:** Oric-specific graphic implementation, general 8-bit strategy.
**Source:** room reconstruction BASIC 100–1999, save-under renderers,
two-byte moving hazard `$4CDD–$4D50`.

The world changes by rebuilding rooms and animating bounded objects. No
full-screen scrolling routine or full second 8,000-byte framebuffer was found.
The hazard restores two old video bytes, saves two new ones and writes `$FF`
into them. `$FF` has bit 6 set and bit 7 set: it is inverse graphic data, not
a serial color attribute. Its visible result depends on current ink/paper.

Avoiding whole-screen copies is a plausible fit for RAM pressure and a BASIC
controller. It trades scrolling continuity for small redraw regions and room
transitions. The small hazard's reuse is limited to simple moving byte patterns;
it shares the same overlap/ownership risks as larger save-under sprites.
Neither absence of scrolling nor byte-only motion proves historical optimality.

## Required hardware investigations

1. Trace both exact ROM revisions through mode/font transitions, while watching
   `$5900` and all active save slots for overlapping lifetimes.
2. Inspect VIA ACR/IER, live Timer 1 phase and ROM timer service before assigning
   periods to latch values; record keyboard repeat and sound behavior.
3. Capture render bytes and scanlines around attribute sprites, `$0A` stopping
   markers and OR composition. Include clipping and overlapping layers.
4. Trace whether animation opcode `$15` reaches the three nested `$FF` counters
   at `$415C`; its blocking delay is not a vertical-blank wait.
5. Measure on a controlled emulator and then real hardware. Keep firmware,
   interrupt conditions and display mode in every result.

No existing machine guideline was changed, and no finding is `benchmarked` or
`validated` on the present static evidence.
