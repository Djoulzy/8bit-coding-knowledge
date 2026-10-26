---
id: PORT-LAIGLE-DOR-CHECKPOINTS
program: "L'Aigle d'Or"
cpu: ["6502"]
machines: ["apple-iie"]
status: implemented
validation_status: analyzed
review_date: "2026-10-20"
---

# Twelve-byte progress checkpoints

This Apple port feature works between the DHGR color and HGR monochrome
editions. A checkpoint carries **10 payload bytes and 2 CRC bytes**, displayed
as **24 hexadecimal characters**, in four groups of six. It is reversible
packed data, not an MD5 hash or a complete machine savestate. Historical inputs
and validated knowledge-base guidelines are unchanged.

## Player flow

Press **C** during castle gameplay and note the code. For an untouched room-12
state with no provisions, 500 gold, zero points and 100% strength:

```text
0000E0-C01F40-00E400-00550B
```

Space, Return or Escape closes the panel. Opening/closing keys are consumed;
controller time, movement, actions and wear pause. **H / ?** opens help and
returns to the same code.

To resume, boot either edition, enter a name normally, then choose **4. Reprendre
avec un code** outside the castle. Type the code and press Return. Letters are
case-insensitive; spaces and hyphens are ignored. Backspace corrects the last
accepted character. Escape cancels without changing the game. Help preserves
partial input. An invalid character or a 25th digit must be edited before
acceptance. CRC, format and range checks finish before any game state changes.

**The former 18-character version-1 codes are incompatible.** Native input and
the host helper identify their length explicitly; they do not reinterpret them.

## Preserved state and limits

| Data                      | Bits      | Meaning                                                               |
|---------------------------|-----------|-----------------------------------------------------------------------|
| Four provisions           | 12        | Vials, torches, ropes, crowbars: 3 bits each, 0–7                     |
| Equipment                 | 4         | Iron key 1, gold key 2, ring 4, lead eagle 8                          |
| Quest objects             | 3         | Missing book 1, diamond 2, golden eagle 4; inverted possession flags  |
| Scrolls                   | 3         | Three independently acquired scroll flags                             |
| Room                      | 6         | 0–63                                                                  |
| Gold                      | 16        | Unsigned 0–65535                                                      |
| Points                    | 12        | 0–4095; ordinary finite rewards total at most 2630                    |
| Strength and format tag   | 8         | High bit set for v2; low seven bits hold 0–100 percent                |
| Ordinary pickups removed  | 16        | One bit for each initially populated treasure record                  |
| CRC                       | 16        | Entry-error detection over the preceding 80 payload bits              |
| **Total**                 | **96**    | **12 bytes**                                                          |

The three scroll flags need three bits, rather than the initially proposed two.
Thus inventory, room, economy and strength occupy exactly eight bytes. The
pickup mask and CRC bring the packet to twelve.

Strength is saved as `floor(energy / 100)`, then restored as `percent * 100`
hundredths. For example, 5099 becomes 50%, restored as 5000. Capturing does not
change the active strength. The high bit of this field identifies the format
without adding an extra byte. Negative strength or values above 10000
hundredths cannot be encoded.

The game still supports its ordinary byte-sized provision stocks. If **any
stock exceeds seven**, checkpoint generation displays an error and emits no
code; it neither reduces the stock nor silently truncates it. Scores above
4095 are similarly rejected. The test menu still grants nine consumables, so
that debug inventory must be reduced before generating a representable code.

The name is not encoded: the newly entered name is retained. The selected
item is also omitted: resume starts **empty-handed**, standing and facing down
on a free near-floor cell (`y=180`). An oubliette checkpoint returns to its
originating room's ordinary scene. Darkness follows the normal lighting rules;
select a torch again if necessary.

The following restart as in a new adventure: wear, poison, RNG, drain, doors,
locks, chests, traps, room lighting history, enemies, exact coordinates, current
action, pit state and temporary fireplace passages. Owned torch/crowbar lives
use the normal fresh-item helpers. This remains a partial checkpoint; it does
not claim to preserve wear or trap state.

## Pickup mask and repeat-reward prevention

Bit `i`, least-significant bit first, means the ordinary treasure originally
in `PICKUP_ROOMS[i]` has been removed:

```text
bit:   0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15
room:  1  4 13 18 28 30 35 38 52 53 57 58 59 60 61 62
```

The build verifies this table against all 64 original B2 records at `$5600`.
It covers three scrolls, four money bags, two keys, five vials, the ring and the
lead eagle. Quest objects have their own three flags. Capture tests treasure
bits `$38` of each mutable `WORLD + $0100 + 4*room` record. A zero treasure field
sets the mask bit, independently of current inventory quantities.

After fresh-game reset, apply clears **only** those treasure bits with `$C7`
for each set mask bit. Furniture, initial room geometry and hazards keep their
original values. Removed pickups consequently cannot reappear and award gold
or points again, even after a consumable has been used up or a key worn out.
Uncollected treasure remains available. Door/chest/trap state is deliberately
separate and restarts.

## Binary protocol, version 2

Payload bits run **MSB first**, across byte boundaries. Multibyte integers and
the CRC are serialized **big endian**; native game counters remain little endian.

| First bit | Width | Field |
| --- | ---: | --- |
| 0 | 3 | Vials |
| 3 | 3 | Torches |
| 6 | 3 | Ropes |
| 9 | 3 | Crowbars |
| 12 | 4 | Equipment flags |
| 16 | 3 | Missing quest flags |
| 19 | 3 | Scroll flags |
| 22 | 6 | Room |
| 28 | 16 | Gold |
| 44 | 12 | Points |
| 56 | 8 | `$80 OR strength_percent` |
| 64 | 16 | Removed-pickup mask |
| 80 | 16 | CRC, high byte first |

There is no padding. The native byte-wise packer splits gold, points and the
pickup mask into high/low chunks so no individual codec field exceeds eight
bits. Its field widths are `3,3,3,3,4,3,3,6,8,8,4,8,8,8,8`.

CRC-16/CCITT-FALSE uses polynomial `$1021`, initial `$FFFF`, no reflection and
zero final XOR. It covers exactly payload bytes 0–9. The host reference uses
Python `binascii.crc_hqx(payload, 0xFFFF)`. CRC detects accidental entry errors;
it is not authentication or protection against edited game states.

The fixed vector above has payload `00 00 E0 C0 1F 40 00 E4 00 00` and CRC
`55 0B`. The embedded tag must be set and the decoded percentage must be at most
100, even if the CRC is valid.

## Native memory and disk integration

The resident [adapter](../src/game/checkpoint.s) intercepts C / exterior option
4 and loads a **bounded 4 KiB slot** at physical sectors **544–559**, track 34.
The module executes at MAIN `$A000–$AFFF` while its 40-column TEXT panel is
visible. It uses the existing pinned slot-6 BOOT0 reader; the disk must remain
inserted. It performs no disk writes.

[checkpoint-overlay.s](../src/apple/checkpoint-overlay.s) contains five fixed
jump vectors, the [capture/codec/apply logic](../src/game/checkpoint-codec.s)
and the [TEXT editor](../src/apple/checkpoint.s). The build resolves resident
helper addresses separately for each edition using `game.lbl`, then links with
[checkpoint.cfg](../src/checkpoint.cfg). The 16-room protocol table is generated
from the checked original records. Scratch occupies MAIN `$0F30–$0F77`, after
the disk/render workspaces. The former PASSCODE/PASSTAIL/PASSUI startup
relocations are removed.

The module replaces part of the disposable room baseline, never the resident
program, AUX atlas or the displayed game buffer. Dirty rectangles are disabled
before loading so help cannot repair graphics using module bytes. Closing the
save panel tail-jumps through resident code, which recreates the baseline while
TEXT is still visible, preserving a falling grille's latched side. Applying a
valid code resets/restores state, then **tail-jumps** to resident safe placement:
that routine may overwrite `$A000`, so no overlay return address may remain on
the stack. Ordinary hidden-page preparation then draws the next game frame
before the flip; the other buffer follows on the next frame.

Graphical endings use the same disposable baseline at different times, with
separate disk slots 352–543. No ending or map resource is removed to fit the
checkpoint module. Disk allocation and linker limits are checked at build.

## Reproduction and execution evidence

From the port directory:

```sh
make games
python3 tools/check_game.py --video dhgr --suite checkpoint
python3 tools/check_game.py --video mono --suite checkpoint
python3 tools/check_game.py --video dhgr --suite endings
python3 tools/check_game.py --video mono --suite endings
python3 tools/checkpoint.py encode --room 12
python3 tools/checkpoint.py decode 0000E0-C01F40-00E400-00550B
```

Host encode options mirror the preserved fields: `--vials`, `--torches`,
`--ropes`, `--crowbars`, `--possessions`, `--objectives`, `--scrolls`, `--gold`,
`--points`, `--force` and `--pickups`. `--pickups` accepts the integer bit mask;
there is no held-item or player-name field.

Ten checkpoint integration tests passed per edition (20 executions), including
64 native codec vectors and all 96 individual packet-bit corruptions. Eight
ending regression tests also passed per edition (16 executions). Rebuilding
both games a second time produced identical application, checkpoint-module,
`.do` and `.nib` bytes.

See [checkpoint-verification.json](checkpoint-verification.json) for the actual
executed suites, hashes and scope. Tests execute the assembled NMOS code in
py65, including real BOOT0 sector reads, codec boundary vectors, corrupted
packets, UI editing, pause/help/cancel, baseline restoration and cold
cross-edition resume. The PNGs are functional CPU previews. Virtual II,
system-ROM cold-start and physical-hardware validation remain separate; no
such new validation is claimed here. Older reports retain their revision hashes.
