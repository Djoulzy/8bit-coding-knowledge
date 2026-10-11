---
id: "ANALYSIS-APPLE2-KARATEKA-ROUTINES"
program: "Karateka"
cpu: ["6502"]
machines: ["apple-iie"]
analysis_status: complete
source_revision: "d02edc77fa0a02d3f679af22456ca1c762c305dc"
analysis_date: "2026-10-11"
---

# Routine inventory

All references are to [the supplied disk](<../../sources/Apple IIe/Karateka/Karateka (1984)(Broderbund).dsk>).
`DSK` offsets are exact first-byte locations, not invented source lines.
Original labels/dialect are unknown; names are analytical descriptions.
See [architecture](architecture.md#scope-and-evidence-conventions) for phase
rules and the [selected listing](extracted/selected-disassembly.txt) for bytes.
Confidence describes static understanding, not proof that a path runs in all editions.

## Boot and relocation

| Phase / entry | DSK evidence | Called by / calls | Purpose and effects | Confidence |
| --- | --- | --- | --- | --- |
| Boot `$0801–$084C`, `$085E–$0878` | `$000001`, `$00005E` | Disk firmware; monitor and indirect slot-ROM call; JMP `$B715` | Sector setup, stack initialization, selected custom loader branch | confirmed by bytes; ROM reads assumed |
| Initial `$B715–$B749` | `$000115–$000149` | Boot; calls `$B7B5`, JMP `$2100` | Descending page/sector core load; buffer pages `$A7..$08` | analyzed; read success not tested |
| Initial `$B7B5` | `$0001B5` | Initial loader; JSR `$BD00` | PHP/SEI, RWTS call, restore P, return C | analyzed locally; DOS internals not audited |
| Initial `$2100–$2169` | `$009900–$009969` | Initial loader | High/low relocation, page-2 clear, HGR soft switches; JMP `$0153` | analyzed; model copies checked |
| Runtime `$0153–$0169` | `$009953–$009969` | JMP from initial `$2150` | Clear page 1; operand high-byte patch `$0159`; JMP `$B77C` | analyzed; stack lifetime untested |

## Low services

| Runtime entry | DSK evidence | Caller / dependencies | Contract and effects | Confidence |
| --- | --- | --- | --- | --- |
| `$0200/$0209 → $020C/$0237` | `$009A00`, `$009A09` | Title input, scene paths; `$0300`, `$1900`, `$7609` | Scene/disk transfer, display preparation; uses `$D0/$D2`, `$BFFD–$BFFF` | confirmed operations; scenario semantics inferred |
| `$0300`, `$0348`, `$0393` | `$009B00`, `$009B48`, `$009B93` | Low scene path; copied `$C600` code, loaded `$4000` code | Copy/patch disk ROM; raw disk read; swap ZP with `$4F00` | observed; complete loader/protection protocol unknown |
| `$03C3/$03DC` | `$009BC3/$009BDC` | Call-site coverage incomplete | Page copy; `$C081/$C082` accesses with a `$D000` copy | observed; bank configuration/reachability unresolved |
| `$0700` | `$009F00` | Title `$B8C2/$B8CE`; sprite/text helpers | Consume text pointer `$E5/$E6`, vertical coordinate `$06`; draw HGR text | likely text renderer; full encoding not audited |
| `$0780 → $0786` | `$009F80/$009F86` | Intro `$B833`; `$07B9` | Copy 190 rows × 40 bytes across pages with a two-row upward source displacement | analyzed |
| `$0783 → $0799`; `$07D7` | `$009F83/$009F99`, `$009FD7` | Title/intro | Save old draw selector in `$E4`, toggle `$07`, optionally poll `$C019`, show completed page | analyzed |
| `$0A00/$0A03` | `$00A200/$00A203` | Repair `$679C`, low services | Rectangle fill/pattern with shared coordinates and bounds; full vertical clipping not established | analyzed locally |
| `$0A06 → $0ABF` | `$00A206/$00A2BF` | `$7609/$774B` | Clear bit 6 in last byte column of the draw page using interleaved row offsets | analyzed locally |
| `$0B00` | `$00A300` | Gameplay `$B5F0` | Clear health-display band using rectangle helper | analyzed locally |
| `$0B03/$0B06` | `$00A303/$00A306` | Gameplay | Draw health icons with normal/mirrored renderer; `$B6/$B7` counts | analyzed |
| `$0B09/$0B0C`, `$0B0F` | `$00A309/$00A30C`, `$00A30F` | Combat/update | Decrement health; clear alive flags on zero; timed capped regeneration | analyzed locally; real-time rate unknown |
| `$0C40` interfaces | `$00A440` | `$7628` audio events | Foreground effects, `$C030` and `$FCA8` | analyzed locally; pitches not measured |
| `$0D00–$0DA5` | `$00A500–$00A5A5` | Higher-level audio entry paths; keyboard service | Stream `$F7/$F8`, cursor `$F6`; timing values and `$FE/$FD/$FF` commands; paired speaker counters | analyzed local grammar; full streams unknown |
| `$0DC0–$0DF9` | `$00A5C0–$00A5F9` | `$7644` | Packed sign-bit stream from `$9C/$9D`; delay `$BA`; transition-based speaker toggles | analyzed locally; pointer initialization contract incomplete |

## Rendering and actor state

| Runtime interface / worker | DSK evidence | Calls and state | Purpose | Confidence |
| --- | --- | --- | --- | --- |
| `$1900 → $190F` | `$009100/$00910F` | Draw selector `$07`, pointer `$00/$01` | Clear one entire 8 KiB HGR allocation with `$80` | analyzed |
| `$1903/$1906 → $1A42/$1A4B` | `$009103/$009106`, `$009242/$00924B` | `$1A61`, `$1927`, `$1AEB` | Normal sprite draw; second interface adjusts byte anchor by width | analyzed locally |
| `$1909/$190C → $1C5B/$1C64` | `$009109/$00910C`, `$00945B/$009464` | `$1A61`, `$1AF4`, `$1AEB` | Mirrored sprite draw with two byte-anchor conventions | analyzed locally |
| `$1A61` | `$009261` | Source `$03/$04`, X/Y | Save source/X/Y, read height/width header, advance pointer by two | analyzed |
| `$1927–$1A33` | `$009127–$009233` | `$05/$06` position, `$07` page, `$0F` mode, `$10` phase | Horizontal clipping, row-table lookup, shift/join, patched composition, boundary preservation | analyzed; whole clipping/mode matrix untested |
| `$1A84–$1AEA` | `$009284–$0092EA` | A byte, `$10=0..6`; returns A and `$1A`, clobbers X | Seven-bit low/high fragment split, phase-specific accumulator paths | analyzed; exhaustive local model |
| `$1AF4–$1C5A` | `$0092F4–$00945A` | Same renderer arguments, reflection table `$0980` | Transform phase/anchor, reverse packed pixels and destination byte order, compose | analyzed locally; full edge equivalence untested |
| `$6400–$653F` | `$005C00–$005D3F` | Work record `$20–$2F`; `$6300/$6360/$63BE` tables | Advance horizontal/vertical cursors and frames; control-token dispatch | analyzed local dispatch; all sequences not traversed |
| `$6780/$678C → $6797/$678F` | `$005F80/$005F8C` | Retained `$E5/$E3`; `$0A00/$0A03` | Clear and pattern repair rectangles for previous actor positions | analyzed locally |
| `$6783 → $6811` | `$005F83/$004011` | Work frame IDs, facing `$2C`, position `$22`, phase `$50`; frame arrays `$6000–$62FF` | Layered actor rendering; normal/mirrored paths, AND mask and OR image calls | analyzed locally; branch to `$BC00` partially mapped |
| `$6B00` | `$004300` | Actor work record, other actor, distance `$33`, scene variables; `$6540` | Choose second actor's animation/action according to context | confirmed decisions; complete AI meaning unknown |
| `$7000/$7003 → $7021/$7048` | `$004800/$004803` | Fixed record fields | Initialize first/second actor | analyzed; not all fields initialized here |
| `$7006/$700C → $7071/$708D` | `$004806/$00480C` | `$20–$2F → $70–$7F` or `$60–$6F` | Commit 16-byte work record | analyzed; exact loop bytes checked |
| `$7009/$700F → $707D/$7099` | `$004809/$00480F` | Reverse copies; tail `$70A6` | Load work record; classify other actor and update distance `$32/$33` | analyzed; helpers have extra side effects |
| `$7012 → $70A6` | `$004812/$0048A6` | A state ID; table `$70C6`, scene/distance fields | State classification and contextual distance helper | analyzed locally |
| `$7366`, `$74C0` | `$004B66`, `$004CC0` | Calls at `$B5AD/$B5BD`, `$B680/$B688` | Combat-result consumers/producers | observed; exact attack/hit contracts unknown |

## High controller and page services

| Runtime entry | DSK evidence | Caller / calls | Purpose / state | Confidence |
| --- | --- | --- | --- | --- |
| `$7600 → $7628`; `$7609` | `$004E00/$004E28`, `$004E09` | Gameplay; `$0A06`, `$779A`, audio helpers | Flip completed page, update draw selector, dispatch sound flags | analyzed locally |
| `$7603 → $7697` | `$004E03/$004E97` | Title and audio polling | Keyboard/control-key service; strobe and control toggles | analyzed locally; entire key map incomplete |
| `$7606 → $774B` | `$004E06/$004F4B` | Gameplay setup | Copy draw page to other page, 40 columns × 192 rows, pause handling and ROM delay | analyzed; no measured visual transition |
| `$779A` | `$004F9A–$004FA6` | Page flip | If ROM `$FBB3 == $06`, poll `$C019` until bit 7 clears | analyzed |
| `$A300/$A306 → $A30C` | `$001B00/$001B06` | `$B5ED`; `$AD0F` | Decrement refresh counter `$5F`, conditionally redraw scenery | analyzed locally; not actor blitter |
| `$A309 → $A316` | `$001B09/$001B16` | End of frame `$B696` | Shift retained phase/position values; decrement `$54` | analyzed; page-history intent inferred |
| `$AD00` interfaces | `$008500` | Frame controller; `$1903` | Background layer draw/repair dispatch | observed interfaces; only selected workers analyzed |
| `$B0C0/$B0C3` | `$0088C0/$0088C3` | Frame controller | Conditional scenery/overlay repairs | analyzed locally; scene semantics incomplete |
| `$B400–$B4E6` | `$008C00–$008CE6` | Title `$B895` | Initialize globals, actors and health; two closely related update loops | analyzed |
| `$B4E7–$B699` | `$008CE7–$008E99` | Main loop | Decisions, sequences, combat consumers, regeneration, repairs, draws, history | analyzed call order; full scenario semantics incomplete |
| `$B69A–$B710` | `$008E9A–$008F10` | `$B581` | First actor work-record update/commit; action selector `$A000`, sequence `$6400` | analyzed locally |
| Runtime `$B711` | `$008F11` | `$B40C` | Byte recurrence from seed `$48`; arithmetic `$05 × seed + $0B` modulo 256 | analyzed; statistical quality not tested |
| Runtime `$B72E/$B73F` | `$008F2E/$008F3F` | Gameplay/health initialization | Set health/icon state from maxima `$B1/$B0` | analyzed locally |
| `$B763` | `$008F63` | Main loop | JMP `$B7F5` input poll | confirmed by bytes |
| `$B77C–$B7DB` | `$008F7C–$008FDB` | Relocated startup | Title, story, delays, intro drawing; JMP `$B895` | analyzed call sequence |
| `$B7DE/$B7EA/$B7F5` | `$008FDE/$008FEA/$008FF5` | Title/main/input delay helpers | Start/transition path; buttons `$C061/$C062`, keyboard `$C000/$C010` | analyzed locally |
| `$B823`, `$B833` | `$007023/$007033` | Title | Polling delay; intro row-copy and page-flip controller | analyzed locally |
| `$B898/$B8C2/$B8CE/$B8E6` | `$007098/$0070C2/$0070CE/$0070E6` | Title | Table-selected graphics, credit/story text, composed scene | analyzed locally |
| `$B960` | `$007160` | Text setup | Load pointer into `$E5/$E6` from `$BB9F/$BBB5` arrays | analyzed |
| `$BC00` | `$007400` | Facing branch `$6823` | Alternate actor drawing path | observed entry; only initial worker span examined |

## Coverage limits and next tests

No exhaustive reachable-code set, original symbol list, full IRQ/NMI map or
complete overlay inventory is claimed. Data bytes decoded linearly as `.byte`
or unusual instructions do not establish execution of undocumented opcodes.
Resolve later disk transfers and trace actual callers before extending the map.

