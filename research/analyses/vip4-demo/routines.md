---
id: ANALYSIS-ORIC-0002-ROUTINES
program: "Vip4 Demo / Quintessential"
cpu: ["6502"]
machines: ["oric-unspecified", "microdisc"]
analysis_status: draft
source_revision: "sha256:555e811187069b29bfc6cf657be7f19f8c49aa8d25fbbeeb8ab4718ad2577558"
analysis_date: "2026-10-09"
---

# Routine inventory

## 4. Source location and confidence

All rows refer to `research/sources/Oric/Vip4 Demo/vip4.dsk`. Names are
analytical, not recovered symbols. Each row provides the original DSK offset
of its first byte and a loaded CPU span (or logical sector-stream offset for
the stub). Use selected listings and `extracted/manifest.json` for each byte
across MFM sector gaps. `Confirmed by source` means bytes/calls were checked,
not runtime reachability. IRQ activation and dynamic targets require tracing.

| Routine / symbol | Source location | Called by / calls | Purpose | State / hardware | Confidence |
| --- | --- | --- | --- | --- | --- |
| Boot relocation stub | logical `$00117–$0013F`; DSK start `$000319` | Boot firmware; calls `$00`, jumps `$A7D0` | Recover location from retained JSR return bytes, copy relocation body | `$00/$01`, stack, firmware `$00AB` | confirmed by source; firmware ABI unknown |
| Boot entry | Boot CPU `$A7D0–$A7F7`; DSK start `$000342` | Relocation stub → `$A83C` → `$F800` | Set vector and eight-sector resident load | `$FFFE/$FFFF`, VIA IFR, controller | confirmed by source |
| Boot sector transfer | Boot CPU `$A7F8–$A83B`; DSK start `$00036A` | `$A83C`; calls `$A85C` | Seek/poll/read 256 bytes | `$0310–$0314/$0318`, patched `$A830` | confirmed by source |
| Boot read/count helper | Boot CPU `$A83C–$A85B`; DSK start `$0003AE` | Boot entry; calls `$A7F8` | Status check/attempt decrement; advance sector/destination | `$A877/$A879/$A87A`, inherited A initialization | confirmed by source; complete error recovery uncertain |
| Boot busy wait | Boot CPU `$A85C–$A868`; DSK start `$0003CE` | Boot transfer | Poll controller busy bit | Y, A/C, `$0310` | confirmed by source |
| Boot IRQ escape | Boot CPU `$A869–$A876`; DSK start `$0003DB` | Installed vector; live activation not established | Discard IRQ frame then RTS | Stack, P lost, controller | analyzed semantics; masked path |
| Resident orchestration | R CPU `$F800–$F989`; DSK start `$000734` | Boot JMP; calls helpers and overlays | Linear effects/assets sequence; ending loop | All descriptors, RAM lifetimes, VIA/PSG | confirmed by source |
| Silence helper | R CPU `$F98D–$F9BA`; DSK start `$000927` | Main at effect boundaries | Write AY registers; install vector `$8AFC` | A/X/Y, VIA, vector writes without SEI | confirmed by source; suspect vector byte order |
| Music timer trampoline setup | R CPU `$F9C6–$FA12`; DSK start `$000960` | Main after selected loads | Set latch/IER/ACR; build `$0245–$0249`; CLI | Timer 1, vectors, VIA direction/PCR | confirmed by source; initial counter phase unknown |
| Resident sector read | R CPU `$FA13–$FA7E`; DSK start `$000A13` | `$FA8E`; calls `$FAFB` | Sector/track/side update and polling transfer | Controller, patchable STA `$FA73` | confirmed by source |
| Resident IRQ escape | R CPU `$FA7F–$FA8D`; DSK start `$000A7F` | Vector set by `$FA9F`; I remains set | 3 PLA, control/status, RTS | Stack and nearest JSR frame | analyzed semantics; activation unknown |
| Resident page loop | R CPU `$FA8E–$FA9E`; DSK start `$000A8E` | `$FA9F` → `$FA13` | Read pages; advance operand high byte | `$FC8D/$FC8E`, `$FA75` | confirmed by source; no active retry branch |
| Descriptor load/patch | R CPU `$FA9F–$FAF6`; DSK start `$000A9F` | Main; calls `$FA8E` | Select descriptor X, patch target/destination, load | Arrays, SEI, upper RAM/control | confirmed by source |
| Overlay call wrapper | R CPU `$FAF7–$FAFA`; DSK start `$000AF7` | Main | Patched JSR then RTS | Loaded target from prior descriptor | confirmed by source |
| Controller busy wait | R CPU `$FAFB–$FB07`; DSK start `$000AFB` | Sector reader | Delay and poll status bit 0 | A/Y/C, `$0310` | confirmed by source |
| Text clear | R CPU `$FB08–$FB1E`; DSK start `$000B6E` | Main | 5-store unroll, union `$BB80–$BFDF` | X, text memory | analyzed coverage |
| HIRES clear | R CPU `$FB1F–$FB86`; DSK start `$000B85` | Main | 32-store unroll, union `$A000–$BF3F` | X, screen RAM | analyzed coverage |
| Charset copy / video setup | R CPU `$FB87–$FBE7`; DSK start `$000BED` | Main startup | Six-page copy; two fill phases and mode attribute | `$00/$01`, inherited C/D, charset/screen | confirmed by source; flag-dependent phase |
| Long software delay | R CPU `$FBE8–$FC00`; DSK start `$000C4E` | Main repeatedly | 256 by 256 loops; preserve A/X/Y | Stack; IRQs extend elapsed time | analyzed timing |
| Music init | M00 CPU `$C000–$C034`; DSK start `$002B64` | Explicit main JSR `$C000`; calls `$C206/$C0BD` | Set `$024A` JMP, voice state, CLI | ZP `$08/$09`, `$BFE6`, `$CCCC` | confirmed by source |
| Music IRQ | M00 CPU `$C035–$C0BC`; DSK start `$002B99` | Timer acknowledge trampoline; calls `$C0BD/$C1AF/$C121/$C206` | Voice/effect updates; AY writes; RTI | A/X/Y preserved; score/state partly decoded | confirmed by source; score semantics partial |
| Picture draw | M01 CPU `$1000–$1030`; DSK start `$003ECC` | Patched generic call target | 40 by 200 self-modifying row copies | X/Y, source/screen operands advanced | analyzed |
| Dormant picture delay | M01 CPU `$1031–$1049`; DSK start `$003EFD` | No caller in reviewed entry | Odd X decremented by two cannot reach zero | Stack; patch at `$1037` only after loop | analyzed nontermination; live reachability unknown |
| Sample init / foreground | M02 CPU `$9D0D–$9D86`; DSK start `$013D0E` | Entry JMP `$9D0D` at `$0FFD` | Configure AY/latches, relocate entire ZP, poll end | ZP overwritten, X/Y reserved, IER inherited | analyzed |
| Sample IRQ templates | M02 CPU `$9D87–$9DD5`; DSK start `$013D88` | Copied to `$00–$4E`; vector `$00` ↔ `$25` | Alternate nibbles/channels, pointer increment, RTI | AY8/9, T1 ACK, operand state | analyzed relocated semantics |
| Opposing-row effect | M05 CPU `$1000–$106B`; DSK start `$024202` | Patched generic call; calls `$11FC` | Two 40-byte copies with source strides ±80 | Patched addresses and row lookup arrays | confirmed by source; visual intent partial |
| Picture sequence / scroll | M06 CPU `$1000–$114B`; DSK start `$027402` | Generic call; calls `$117D/$119F/$114C/$1833` | Scripted transitions and repeated upward row copies | Screen addresses, patched workers | confirmed by source; script data partial |
| Parameterized blitter | M06 CPU `$114C–$117C`; DSK start `$0275B4` | Entry sequence | Descending row bytes with patched size/source/destination | Width/height fields in operands | analyzed |
| Picture sequence and blitter | M08 CPU `$1000–$1084`; DSK start `$02D968` | Generic call; calls `$109A/$1085` | Repeated image/script steps and row copy | Dynamic source and destination | confirmed by source; script data partial |
| Effect startup | M0B CPU `$0600–$0610`; DSK start `$034898` | Generic call; JMP `$0741` | Capture hardware SP; initialize software frame pointer | `$54/$55`, saved SP at `$0611` | confirmed by source |
| Software frame save/restore | M0B CPU `$0612–$069B`; DSK start `$0348AA` | Effect routines; paired helpers | Save local bytes and prior frame pointers, then restore | `$50–$55`, `$68–$6F` and frame RAM | analyzed selected frame mechanics; compiler unknown |
| Effect main prefix | M0B CPU `$0741–$0790`; DSK start `$034A3F` | Startup JMP; calls `$8AE4/$0AB9/$87FE/$06B9/$89D9` | Set graphics and enter effect/dancer work | Compiler workspace, screen, data tables | confirmed by source; full main partial |
| Texture base setup | M0B CPU `$87FE–$883A`; DSK start `$0407CC` | Effect main | Initialize split base tables | `$87F2–$87FD` writable data | confirmed by source |
| Sparse texture row worker | M0B CPU `$883B–$88A1`; DSK start `$04086F` | `$890E/$896E` and other effect paths | 66 rows ×29 bytes at stride 120; split phase increment | Patched `$8871/$8874`, texture tables | analyzed selected operations |
| Phase / two-pass texture setup | M0B CPU `$88B2–$8971`; DSK start `$0408E6` | Call chain not exhaustively mapped; invokes `$883B` | Circular shifts, split increments, lookup phases | `$88A2–$88B1`, `$87EC–$87F0` | analyzed operations; whole-effect reachability partial |
| Dancer copy | M0B CPU `$89D9–$8A18`; DSK start `$040A73` | Effect main prefix | 43 rows ×18 bytes, stride 120, overwrite | ZP `$56–$59`, atlas pointers, screen | analyzed copy; appearance unknown |
| Graphics setup | M0B CPU `$8AE4–$8AFF`; DSK start `$040BE4` | Effect main | Clear charset/screen/buffer, set `$1E` mode | Screen/charset RAM, state `$8A1A` | confirmed by source |
| Growing image reveal | M0D CPU `$1000–$1045`; DSK start `$04D732` | Generic call | Decrease source by 40; height changes; copy 41-byte rows | Executable operands, screen including `$BF40` | analyzed; overlap intention unknown |
| Ending entry | M13 CPU `$60CB–$60DD`; DSK start `$06FF66` | JMP at `$0FFD`; main calls `$0FFD` | IRQ setup; text setup; loop `$6127/$6197` | Carry and `$02` inherited | confirmed by source |
| Ending text setup | M13 CPU `$60DE–$6112`; DSK start `$06FF79` | Ending entry | Fill 28 text rows; install fixed codes and charset attribute | `$00/$01`, `$BDB3–$BDD3`, C/D | analyzed byte operations |
| Ending masks/text update | M13 CPU `$6127–$6196`; DSK start `$070028` | Endless main loop | Shift masks; slower character/font injection | `$B3xx/$B4xx`, `$6000–$6002` | confirmed by source; visual interpretation partial |
| Ending glyph compositor | M13 CPU `$6197–$61C7`; DSK start `$070098` | Endless main loop | 256 mask-composed glyph bytes, advance bank high | `$02/$03`, `$B900–$B9FF` | analyzed byte composition; bank origin unknown |
| Ending sample setup | M13 CPU `$61C8–$6238`; DSK start `$0700C9` | Ending entry | VIA setup, copy 56-byte IRQ, CLI | `$10–$47`, trampoline `$0244`, AY, timers/SR | analyzed setup; exact timing unknown |
| Ending IRQ template | M13 CPU `$609B–$60CA`; DSK start `$06FF36` | Copied to `$10–$3F` | Single-channel nibbles, state in operands, RTI | `$18/$19/$26/$3E`; A restored; X/Y untouched | analyzed relocated semantics |

## Coverage gaps

Module entries and payload sizes are indexed in [architecture.md](architecture.md).
Identical-looking blitter prefixes were byte-compared; asset contents differ.
No exhaustive CFG is claimed for compiler-style effects `$07/$0B/$0E/$10/$12`,
which have software frames, indirect jumps and mixed code/data. `$0C` is only
partly recoverable and uncalled by the main sequence. `$0A/$15` are asset loads,
not established executable entry points. Full score decoding and all external
calls remain incomplete. Imported source remains unchanged; this table is a
reproducible starting map for deeper analysis, not invented historical labels.
