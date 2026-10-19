---
id: PORT-LAIGLE-DOR-CHECKPOINTS
program: "L'Aigle d'Or"
cpu: ["6502"]
machines: ["apple-iie"]
status: implemented
validation_status: analyzed
review_date: "2026-10-18"
---

# Compact room and inventory checkpoint codes

This is a new Apple port feature, shared by the DHGR color and HGR monochrome
editions. It implements the requested short checkpoint: room and inventory,
with the player's name entered normally at the next start. Historical sources
and validated knowledge-base guidelines are unchanged.

## Player flow

During castle gameplay, press **C** to display a code such as
`260000-000000-1CEDA0`. Note the eighteen hexadecimal characters. Space,
Return or Escape closes the panel; its opening and closing keys are consumed.
Movement, actions, services, strength, timers and the controller tick pause.
H/? opens help and returns to the same code.

To resume, boot either edition, pass the title/introduction, enter a name,
then select **4. Reprendre avec un code** outside the castle. Type the code and
press Return. Hex letters are case-insensitive; spaces and hyphens are ignored.
Backspace deletes the last accepted digit. Escape cancels and returns to the
exterior with the existing game unchanged. H/? also preserves partial input.
A malformed character or an extra nineteenth digit requires editing before
validation; input is never silently truncated into an accepted code.

The code panel shows errors for incomplete input, a bad checksum, unsupported
versions, nonzero padding or inconsistent selected-hand data. Validation occurs
entirely in scratch memory before a successful code is applied.

## Checkpoint scope

A successful code starts fresh game state, restores the room and inventory,
and keeps the **newly typed name**. It preserves:

- All four stock quantities: vials, torches, ropes and crowbars, including 255.
- Iron/gold keys, ring and lead-eagle possession flags.
- The three scroll flags and the book/diamond/golden-eagle objective flags.
- The selected held item. A jump's temporarily hidden item uses `saved_item`.

The actor starts standing, facing down, on a free semantic foot cell of the
saved room's near floor (`y=180`). It uses the same bounded spawn scan as the
existing teleportation adapter. An oubliette code returns to its originating
room's ordinary scene. An unlit room still follows the normal torch/darkness
rules.

The compact protocol restarts the following as for a new adventure:

- Gold **500**, score **0**, full strength **10000** hundredths and initial drain.
- Packed world records, room lighting history, doors, chests, traps and pickups.
- Current pose, action, enemies, hazards, pit and temporary fireplace opening.
- Poison, random-generator state and item wear; owned torch/crowbar lifetimes
  are initialized using their existing fresh-item helpers.

Consequently, initial room objects can be present again after a checkpoint
resume. The UI explicitly states that gold, strength and room changes are not
saved. The name, economy, world mutations, exact coordinates and timers occupy
**no bits** in this selected short format. Codes are compatible between the two
video editions as long as this protocol version and game rules are retained.

## Binary protocol, version 1

There are **nine octets**: seven payload octets and a two-octet CRC. The payload
is a stream emitted **most-significant bit first**, across octet boundaries.
Bit 0 in the following table means the first transmitted bit, the high bit of
payload octet 0.

| First bit | Width | Field | Range / interpretation |
| --- | --- | --- | --- |
| 0 | 3 | Format version | `1` |
| 3 | 6 | Room | 0–63 |
| 9 | 3 | Held-item slot | 0–5; table below |
| 12 | 8 | Vials | 0–255 |
| 20 | 8 | Torches | 0–255 |
| 28 | 8 | Ropes | 0–255 |
| 36 | 8 | Crowbars | 0–255 |
| 44 | 4 | Possessions | Iron key 1, gold key 2, ring 4, lead eagle 8 |
| 48 | 3 | Scrolls | Three acquired-scroll bits |
| 51 | 3 | Objectives | Inverted source convention: set means missing; book 1, diamond 2, golden eagle 4 |
| 54 | 2 | Padding | Must be zero |
| 56 | 16 | CRC | High octet, then low octet |

The 54 meaningful payload bits plus two zero bits form seven octets. Quantities
retain full bytes because normal play can exceed the test menu's nine items.
The room and flags use only the bits required by their actual ranges.

| Slot | Held item | Native `held_item` value |
| --- | --- | --- |
| 0 | Empty hand | 0 |
| 1 | Torch | 1 |
| 2 | Iron key | 9 |
| 3 | Gold key | 8 |
| 4 | Vial | 10 |
| 5 | Crowbar | 6 |

Slots 6 and 7 are invalid. A nonempty hand requires positive corresponding
stock or an owned key. The decoder checks these semantics after the checksum.

Equivalently, payload octets can be described directly:

```text
byte 0: version[2:0] | room[5:1]
byte 1: room[0] | held_slot[2:0] | vials[7:4]
byte 2: vials[3:0] | torches[7:4]
byte 3: torches[3:0] | ropes[7:4]
byte 4: ropes[3:0] | crowbars[7:4]
byte 5: crowbars[3:0] | possessions[3:0]
byte 6: scrolls[2:0] | objectives[2:0] | 00
byte 7: CRC high
byte 8: CRC low
```

The CRC is CRC-16/CCITT-FALSE: polynomial `$1021`, initial value `$FFFF`,
unreflected input/output and zero final XOR. It covers exactly payload bytes
0–6. The host oracle uses Python's
[`binascii.crc_hqx(payload, 0xFFFF)`](https://docs.python.org/3/library/binascii.html#binascii.crc_hqx).
The CRC detects entry errors; the encoded payload remains reversible.

All nine octets are displayed as uppercase hexadecimal, in three groups of
six characters. The fixed empty-inventory room-12 vector is:

```text
payload: 26 00 00 00 00 00 1C
CRC:     ED A0
code:    260000-000000-1CEDA0
```

## Code and memory integration

[game/checkpoint.s](../src/game/checkpoint.s) contains capture, bit packing,
unpacking, CRC, semantic validation and fresh-game application.
[apple/checkpoint.s](../src/apple/checkpoint.s) handles editing and hidden-page
TEXT rendering. The ordinary AUX panel scripts provide static wording and
spacing. Native generation, checking and display require no disk access or
ROM service call.

The name is copied to temporary MAIN scratch only while applying a valid code,
then restored after `game_reset`. This preserves what the player typed without
putting their name in the packet. The normal reset restores the initial WORLD;
then inventory is committed and the shared safe-room-placement routine rebuilds
the destination. The next ordinary hidden frame is completed before display.

Three previously unused MAIN ranges hold relocated checkpoint code. All are
installed at entry before title/baseline writes reuse the packed load image.

| Allocation | Role and current used range |
| --- | --- |
| MAIN `$0C30–$0CFF` | `PASSCODE`: CRC/bit codec, used through `$0CF8`; after STATE and before the event log |
| MAIN `$0F30–$0F73` | Packet, decoded fields, hex input, temporary name and codec state; after disk/render scratch |
| MAIN `$0F80–$0FFF` | `PASSTAIL`: capture/close and ownership tables, used through `$0FFB`; before WORLD |
| MAIN `$1F10–$1FFF` | `PASSUI`: input/display and hex conversion, used through `$1FF8`; after the `$1E00` disk buffer and before HGR |
| AUX `$1400–$1ECF` | Shared 2,768-byte text archive, including checkpoint and end-screen panels |

The linker bounds these allocations and startup copies each bounded segment.
The full-game build also omits the unreachable W06 HUD formatter and its
prototype-only strings; W06 keeps its existing conditional branch. This makes
room for the resident interface while keeping the terrain baseline at `$A000`.
The feature adds modes 16/17 and intercepts their keys before gameplay/debug
controls. The renderer routes these modes to TEXT, separately from map modes
13–15. No historical data or source file is edited.

## Reproduction and executed evidence

From the port directory:

```sh
make games
python3 tools/check_game.py --video dhgr --suite checkpoint
python3 tools/check_game.py --video mono --suite checkpoint
python3 tools/checkpoint.py encode --room 12
python3 tools/checkpoint.py decode 260000-000000-1CEDA0
```

Optional host parameters include `--held-item`, `--vials`, `--torches`,
`--ropes`, `--crowbars`, `--possessions`, `--scrolls` and `--objectives`.
Held-item arguments use the native values in the table, and the host helper
checks ranges and ownership before producing a code.

Seven native tests passed per edition. They check startup relocation, 64 native
encode/decode vectors spanning all rooms and quantity/flag boundaries, every
single-bit corruption of a nine-octet packet, CRC-valid invalid versions/padding/
held items, paused generation, editing/overflow/cancellation, help returns, map
and merchant regressions, and cold cross-edition resume with a different name.
Both cold-resume tests execute the supplied Disk II BOOT0 and type the code
through the native keyboard path. They verify fresh excluded state, restored
inventory, safe spawn and absence of visible-page writes.

See [checkpoint-verification.json](checkpoint-verification.json) and each
build's `checkpoint-test-results.json` for hashes and executed scope. The
rendered `checkpoint-*.png` files are functional CPU previews. No new Virtual II,
system-ROM cold-start or physical-hardware test is claimed. Older full-suite,
map and presentation records retain the hashes of their own revisions.
