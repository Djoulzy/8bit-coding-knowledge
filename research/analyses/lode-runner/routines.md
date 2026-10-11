---
id: "ANALYSIS-APPLE2-LODE-RUNNER-ROUTINES"
program: "Lode Runner (local cracked disk)"
cpu: ["6502"]
machines: ["apple-ii-family", "apple-iie-variant-unknown"]
analysis_status: draft
source_revision: "d02edc77fa0a02d3f679af22456ca1c762c305dc"
analysis_date: "2026-10-10"
---

# Lode Runner routine inventory

## Scope and naming

All names are analytical; the input has no original symbols or assembly source.
See [overview](overview.md) for attribution, edition, CPU/ROM uncertainty and hash.
Each citation gives generated listing lines, a CPU span and the first instruction's
original image offset. Every instruction also carries its own DSK mapping.
The listings model loader copies; they are not an executed control-flow trace.

**Confirmed by source** means demonstrated by examined bytes and local control
flow. It does not certify whole-program correctness. **Likely inference** marks
a subsystem interpretation with incomplete callers/state. **Unknown** marks
unresolved reachability, interfaces or behavior.

## Entry, session and storage

| Entry / analytical name | Evidence | Called by / calls | Purpose / external state | Confidence |
| --- | --- | --- | --- | --- |
| BASIC line 10 | [HELLO decoding](extracted/hello.basic.txt) | DOS → BRUN LODE RUNNER | Text title; binary startup | Confirmed by source |
| $07FD binary entry | [loader.asm.txt:L1–L1](extracted/loader.asm.txt), CPU $07FD–$07FF, DSK $010104 | DOS load → $5A00 | Cracked front end | Confirmed by source |
| $5A00 cracker front end | [loader.asm.txt:L2–L17](extracted/loader.asm.txt), CPU $5A00–$5A22, DSK $013307 | $07FD → ROM $FC58, $5F00 | Credit to $05B0; keyboard $C000 | Confirmed by source; publisher equivalence unknown |
| $5F00 relocation | [loader.asm.txt:L18–L101](extracted/loader.asm.txt), CPU $5F00–$5FA1, DSK $013807 | front end → $6000 | Three copies; captured ZP/stack; outside-payload bytes/I/O edges | Confirmed by source, intended endpoints unknown |
| $6000 game/title startup | [startup.asm.txt:L1–L37](extracted/startup.asm.txt), CPU $6000–$6055, DSK $013907 | loader → $87A2, $6359, $7A51, $7A31, $618E | Input detection, metadata, patched title stream, HGR switches | Confirmed by source |
| $6056 new session | [startup.asm.txt:L38–L71](extracted/startup.asm.txt), CPU $6056–$609E, DSK $01395D | title/editor → $6238 through continuation | Four score bytes zero; five lives; demo pointer $A8/$A9 | Confirmed by source |
| $60BF foreground cycle | [startup.asm.txt:L87–L127](extracted/startup.asm.txt), CPU $60BF–$6119, DSK $0139C6 | level continuation → $64BD, $8811, $75F4, $6C82 | Player, audio/delay, hidden ladder, holes, guards; lives/state | Confirmed by source |
| $611A completion | [startup.asm.txt:L128–L143](extracted/startup.asm.txt), CPU $611A–$613E, DSK $013A21 | cycle completion → $7A92, $622A, $609F | Level counters, life increase, score/audio | Confirmed by source; session limits not exhausted |
| $613F death branch | [startup.asm.txt:L144–L146](extracted/startup.asm.txt), CPU $613F–$6146, DSK $013A46 | cycle death | Decrement $98; branch outside selected span | Confirmed fragment; full route incomplete |
| $618E title/input routing | [startup.asm.txt:L157–L217](extracted/startup.asm.txt), CPU $618E–$6213, DSK $013A95 | title → $869F, $6359, $786B, $6056, $7B84 | Keyboard/buttons; mode $A7, editor entry | Confirmed fragment; complete mode matrix unknown |
| $6238 initialize/decode board | [level.asm.txt:L1–L72](extracted/level.asm.txt), CPU $6238–$62C4, DSK $013B3F | session/editor → $630E, $63B3 | 448 low-first nibbles into two grids; clears timers/guards | Confirmed by source |
| $62C7 encode board | [level.asm.txt:L73–L108](extracted/level.asm.txt), CPU $62C7–$630D, DSK $013BCE | editor paths → $630E | Inverse nibble packing; command $02 write | Confirmed transform; disk success unproved |
| $630E board I/O selector | [level.asm.txt:L109–L146](extracted/level.asm.txt), CPU $630E–$6358, DSK $013C15 | decoder/encoder → $0023 or resident copy | Track/sector from $96; $0D00 buffer; $A7 demo choice | Confirmed selector; disk entry unresolved |
| $6359 metadata read/check | [level.asm.txt:L147–L180](extracted/level.asm.txt), CPU $6359–$63A4, DSK $013C60 | startup → $63A5 | Track $0C/sector $0F; $1F00; signature/flag | Confirmed local interface; I/O unexecuted |
| $63A5 inherited I/O vector | [level.asm.txt:L181–L181](extracted/level.asm.txt), CPU $63A5–$63A7, DSK $013CAC | metadata → JMP ($0036) | Reconstructed target $8E50 → $B7B5 | Confirmed reconstructed bytes |
| $0023 legacy vector | [disk.asm.txt:L1–L1](extracted/disk.asm.txt), CPU $0023–$0025, DSK $01692A | level I/O → $1700 | Destination is currently asset bytes, no patch established | Unknown live behavior |
| $0609 disk-byte reader | [disk.asm.txt:L5–L44](extracted/disk.asm.txt), CPU $0609–$065C, DSK $016010 | callers not established → $0657 | Poll $C08C,X; pair decoding into ($3C),Y | Confirmed fragment; live use unknown |
| $B7B5 DOS wrapper | [disk.asm.txt:L46–L55](extracted/disk.asm.txt), CPU $B7B5–$B7C1, DSK $0120BC | $8E50 → $BD00 | PHP/SEI/PLP; carry result | Confirmed interface; underlying RWTS not exhausted |

## World state and gameplay

| Entry / analytical name | Evidence | Called by / calls | Purpose / external state | Confidence |
| --- | --- | --- | --- | --- |
| $63B3 board preprocessing | [level.asm.txt:L187–L317](extracted/level.asm.txt), CPU $63B3–$64BC, DSK $013CBA | $6238 → $82B0, $82AA | Gold, player/guards, hidden ladders; terrain page then preview/play handoff | Confirmed by source |
| $64BD player-update entry | [movement.asm.txt:L1–L122](extracted/movement.asm.txt), CPU $64BD–$65C4, DSK $013DC4 | cycle → $6A12, $6B85, $8336 and other movement branches | Grids, gravity/ladder/bar tests, previous image | Confirmed fragment; all movement transitions untraced |
| $6B85 player coordinates | [movement.asm.txt:L123–L133](extracted/movement.asm.txt), CPU $6B85–$6B9C, DSK $01448C | movement paths → $888F, $887C | Coarse location plus subcell offsets; sprite selection; $888F outside selected listing | Confirmed fragment |
| $6C02 draw/check player | [movement.asm.txt:L187–L194](extracted/movement.asm.txt), CPU $6C02–$6C12, DSK $014509 | movement continuation → $6B85, $83A7 | Pixel overlap $52 plus other state may clear $9A | Confirmed by source; complete death conditions incomplete |
| $6C39 commit digging | [movement.asm.txt:L213–L246](extracted/movement.asm.txt), CPU $6C39–$6C81, DSK $014540 | digging continuation → $82AA, $82B0 | Clears occupancy and page images, retains terrain-grid brick; allocates timer $B4 | Confirmed fragment |
| $6C82 guard quota scheduler | [scheduler.asm.txt:L1–L18](extracted/scheduler.asm.txt), CPU $6C82–$6CA6, DSK $014589 | cycle → $6CDB | Three quota phases $60–$62, persistent cursor $19, guard count $8D | Confirmed by source |
| $6CDB select/update next guard | [scheduler.asm.txt:L19–L80](extracted/scheduler.asm.txt), CPU $6CDB–$6D60, DSK $0145E2 | scheduler → $75CE; $6E65/$75A8/$6DB7 and branches | Cursor wrap, working record, preliminary terrain tests | Confirmed prefix; complete AI unknown |
| $75CE load guard working record | [scheduler.asm.txt:L81–L96](extracted/scheduler.asm.txt), CPU $75CE–$75F3, DSK $014ED5 | $6CDB, holes | Seven fields from parallel arrays into $12–$18 | Confirmed by source |
| $75F4 hole countdown service | [scheduler.asm.txt:L97–L223](extracted/scheduler.asm.txt), CPU $75F4–$7715, DSK $014EFB | cycle → $7716, tile/sprite helpers, score | Timer scan, closure frames at $14/$0A, terrain/actor effects | Confirmed fragment; $7716 not reviewed |
| $8631 release hidden ladders | [input-audio.asm.txt:L151–L198](extracted/input-audio.asm.txt), CPU $8631–$869E, DSK $016F38 | cycle when gold count zero → tile/render helpers | Pending coordinates, both grids and terrain baseline | Confirmed fragment |
| $884B logical-row pointers | [input-audio.asm.txt:L410–L417](extracted/input-audio.asm.txt), CPU $884B–$885C, DSK $016252 | movement/world paths | Y row → $06/$07 occupancy and $08/$09 terrain | Confirmed by source |

Hole initialization and service scan indices $00–$1E; the reviewed allocator
tests X against $1E before selecting, so it uses $00–$1D. Do not infer 31
allocatable holes from the countdown scan alone.

## Renderer, text and arithmetic

| Entry / analytical name | Evidence | Called by / calls | Purpose / external state | Confidence |
| --- | --- | --- | --- | --- |
| $79AD HUD initialization | [renderer.asm.txt:L1–L38](extracted/renderer.asm.txt), CPU $79AD–$7A07, DSK $0152B4 | session → clears, $86E0 | Both pages, borders and inline labels | Confirmed fragment |
| $7A31 one-page row pointer | [renderer.asm.txt:L44–L49](extracted/renderer.asm.txt), CPU $7A31–$7A3D, DSK $015338 | title/tile renderer | Y scanline, page selector $1F → $0C/$0D | Confirmed by source |
| $7A3E paired row pointers | [renderer.asm.txt:L50–L58](extracted/renderer.asm.txt), CPU $7A3E–$7A50, DSK $015345 | restore/draw | Display $0C/$0D and baseline $0E/$0F | Confirmed by source |
| $7A51 / $7A57 HGR clears | [renderer.asm.txt:L59–L75](extracted/renderer.asm.txt), CPU $7A51–$7A6F, DSK $015358 | title/session/editor | Fill selected 8 KiB region with $80 | Confirmed by source |
| $7A70 lives / $7A8C level | [renderer.asm.txt:L76–L90](extracted/renderer.asm.txt), CPU $7A70–$7A91, DSK $015377 | session/status callers | Numeric HUD; $98, $A6; calls $7AF8 | Confirmed fragments |
| $7A92 BCD score addition | [renderer.asm.txt:L91–L104](extracted/renderer.asm.txt), CPU $7A92–$7AA9, DSK $015399 | awards/completion | A/Y increment to four bytes $8E–$91; SED then CLD | Confirmed by source |
| $7AF8 binary digit conversion | [renderer.asm.txt:L141–L155](extracted/renderer.asm.txt), CPU $7AF8–$7B14, DSK $0153FF | HUD/level prompt | Repeated subtraction into $89–$8B; D=0 contract | Confirmed by source |
| $7B64 print character | [renderer.asm.txt:L201–L216](extracted/renderer.asm.txt), CPU $7B64–$7B83, DSK $01546B | $86E0 | Character offset and tile draw; cursor $85/$86, page $87 | Confirmed local implementation |
| $82AA / $82B0 tile draw | [renderer.asm.txt:L217–L281](extracted/renderer.asm.txt), CPU $82AA–$8327, DSK $015CB1 | level/editor/terrain → $885D, $8868, $8438, $7A31 | Select page 1/2, edge masks, 11 rows, two/three bytes | Confirmed by source |
| $8336 restore previous sprite | [renderer.asm.txt:L282–L341](extracted/renderer.asm.txt), CPU $8336–$83A6, DSK $015D3D | player/guard/terrain paths → $8872, $8438, $7A3E | Mask foreground then OR baseline | Confirmed by source |
| $83A7 draw and accumulate overlap | [renderer.asm.txt:L342–L417](extracted/renderer.asm.txt), CPU $83A7–$8437, DSK $015DAE | player/guard paths → same helpers | $52 accumulates masked foreground XOR baseline; OR draw | Confirmed by source |
| $8438 expand sprite tokens | [renderer.asm.txt:L418–L480](extracted/renderer.asm.txt), CPU $8438–$84C0, DSK $015E3F | tile/sprite renderers | Phase-selected shared pairs; patched absolute operands; $DF–$FF | Confirmed in bounded token domain |
| $86E0 inline text consumer | [input-audio.asm.txt:L225–L242](extracted/input-audio.asm.txt), CPU $86E0–$86FF, DSK $016FE7 | title/HUD/editor → $7B64 | Pop/replace JSR return; zero-terminated bytes; $10/$11 | Confirmed by source |
| $885D cell-to-sprite coordinates | [input-audio.asm.txt:L418–L424](extracted/input-audio.asm.txt), CPU $885D–$8867, DSK $016264 | world/player/tile | X cell column,Y row → half-pixel x,scanline y | Confirmed by source |
| $8868 / $8872 alignment lookup | [input-audio.asm.txt:L425–L436](extracted/input-audio.asm.txt), CPU $8868–$887B, DSK $01626F | tiles/sprites | Byte offset in A, phase in X; two coordinate domains | Confirmed by source |

## Input, audio and editor

| Entry / analytical name | Evidence | Called by / calls | Purpose / external state | Confidence |
| --- | --- | --- | --- | --- |
| $6A12 player input/control | [input-audio.asm.txt:L1–L35](extracted/input-audio.asm.txt), CPU $6A12–$6A55, DSK $014319 | player → demo $69B8 or key dispatch | $C000/$C010; control table; synthetic RTS | Confirmed fragment; demo commands incomplete |
| $6A9E / $6AAD axis inversion | [input-audio.asm.txt:L70–L79](extracted/input-audio.asm.txt), CPU $6A9E–$6AB9, DSK $0143A5 | control handlers | Swap direction thresholds $6B81/$6B82 and $6B83/$6B84 | Confirmed by source |
| $869F / $86A8 keyboard wait | [input-audio.asm.txt:L199–L206](extracted/input-audio.asm.txt), CPU $869F–$86B0, DSK $016FA6 | menus/control/editor | Keyboard strobe/read; wait for high-bit key | Confirmed by source |
| $86B1 / $86B5 delays | [input-audio.asm.txt:L207–L214](extracted/input-audio.asm.txt), CPU $86B1–$86BD, DSK $016FB8 | audio/title/waits | X/Y counter loops; input-dependent duration | Confirmed by source; elapsed time unmeasured |
| $86CE beep | [input-audio.asm.txt:L215–L224](extracted/input-audio.asm.txt), CPU $86CE–$86DF, DSK $016FD5 | bad command paths | Sound flag $99 and speaker reads | Confirmed by source |
| $8700 blinking-cell wait | [input-audio.asm.txt:L243–L272](extracted/input-audio.asm.txt), CPU $8700–$8744, DSK $016107 | editor → $82AA, $876D | Saves tile byte in code operand; animation/key/button polling | Confirmed local implementation |
| $8746 analog sample | [input-audio.asm.txt:L273–L291](extracted/input-audio.asm.txt), CPU $8746–$876C, DSK $01614D | $876D and control paths | Trigger $C070; counters $65/$66; bounded sign test | Confirmed by source |
| $876D neutral/action check | [input-audio.asm.txt:L292–L320](extracted/input-audio.asm.txt), CPU $876D–$87A1, DSK $016174 | waits/menu → $8746 | Axis range and $C061/$C062; carry return; sentinel $CB delay | Confirmed by source |
| $87A2 analog startup probe | [input-audio.asm.txt:L321–L332](extracted/input-audio.asm.txt), CPU $87A2–$87B9, DSK $0161A9 | $6000 | Timer polling; inherited Y; timeout stores $CB in $95 | Confirmed by source |
| $87BA foreground tone/delay | [input-audio.asm.txt:L333–L346](extracted/input-audio.asm.txt), CPU $87BA–$87D4, DSK $0161C1 | $8811 | A period,X duration; Y inherited; $99 speaker enable | Confirmed loop; calibrated timing unknown |
| $87D5 append audio event | [input-audio.asm.txt:L347–L352](extracted/input-audio.asm.txt), CPU $87D5–$87E0, DSK $0161DC | movement/awards | Increment $54, store A/X in parallel arrays | Confirmed by source; capacity not enforced |
| $87E1 inline audio consumer | [input-audio.asm.txt:L353–L378](extracted/input-audio.asm.txt), CPU $87E1–$8810, DSK $0161E8 | callers with adjacent data | Pop/replace return; duration/pitch pairs terminated by zero duration | Confirmed by source |
| $8811 sound/pace service | [input-audio.asm.txt:L379–L409](extracted/input-audio.asm.txt), CPU $8811–$884A, DSK $016218 | foreground/session/title → $87BA, delays | LIFO event playback and timing/speed state | Confirmed by source; complete sequences untraced |
| $7B84 editor entry | [editor.asm.txt:L1–L29](extracted/editor.asm.txt), CPU $7B84–$7BC1, DSK $01548B | title/editor → clear, text | Mode $A7=5; saves I/O vector; resets lives/score | Confirmed prefix; full editor initialization incomplete |
| $7C29 editor key dispatch | [editor.asm.txt:L34–L51](extracted/editor.asm.txt), CPU $7C29–$7C4C, DSK $015530 | editor loop → $823D, selected target | P/C/E/M/I/S key table, target−1 RTS | Confirmed dispatch; handler bodies partly unknown |
| $7C60 play selected level | [editor.asm.txt:L52–L52](extracted/editor.asm.txt), CPU $7C60–$7C62, DSK $015567; [editor.asm.txt:L53–L65](extracted/editor.asm.txt), CPU $7C71–$7C8D, DSK $015578 | P command → $817B, $6056 | Inline prompt; mode $A7=3; selected level | Confirmed fragment |
| $8106 disk-error display | [editor.asm.txt:L66–L72](extracted/editor.asm.txt), CPU $8106–$8115, DSK $015A0D; [editor.asm.txt:L73–L73](extracted/editor.asm.txt), CPU $8148–$814A, DSK $015A4F | editor I/O paths not exhausted | Page 2 error text then $80D8 | Likely inference from message/call fragment |
| $814B cell flash selection | [editor.asm.txt:L74–L83](extracted/editor.asm.txt), CPU $814B–$8161, DSK $015A52 | editor paths → $8700 | Reads current logical cell; keyboard strobe | Confirmed by source |
| $817B numeric level prompt | [editor.asm.txt:L84–L100](extracted/editor.asm.txt), CPU $817B–$819F, DSK $015A82 | editor Play and other paths → $7AF8/$7B15 | Decimal prompt digits; further input outside selected span | Confirmed fragment |

## Unmapped or incompletely reviewed code

The selected listings cover representative routines, not every byte. In
particular, $69B8 demo commands, most of guard routing $6D61–$75CD, $7716
continuation, high-score ordering/display, full editor move/edit/init/save
handlers and $BD00 RWTS internals are not exhausted. Linear disassembly of inline
streams is deliberately avoided at known strings.

The key-table targets are $7C60, $7C8E, $7CBC, $7CD8, $7D5D and $7E75.
Only the first handler is examined here. No disk formatting or writes were run.
IRQ/NMI ownership and RAM changes during DOS/ROM calls remain unknown.
