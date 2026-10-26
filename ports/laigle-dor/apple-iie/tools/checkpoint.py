"""Twelve-byte v2 checkpoints: 80 payload bits and CRC-16/CCITT-FALSE.

Inventory, economy, integer strength and sixteen pickup flags survive. The
newly typed name stays local; wear, traps, doors and the held item restart.
This is reversible packed data, not a hash or a complete machine savestate.
"""
import argparse
import binascii
import json

VERSION = 2
SECTOR = 544
CAPACITY = 4096
FIELDS = [('vials',3),('torches',3),('ropes',3),('crowbars',3),
          ('possessions',4),('objectives',3),('scrolls',3),('room',6),
          ('gold',16),('points',12),('strength_tag',8),('pickups',16)]
DEFAULTS = dict(vials=0,torches=0,ropes=0,crowbars=0,possessions=0,
                objectives=7,scrolls=0,gold=500,points=0,force=100,pickups=0)
# Bit i represents removal of the ordinary treasure initially in this room.
# Kept explicit as part of the versioned protocol, checked against B2 at build.
PICKUP_ROOMS = (1,4,13,18,28,30,35,38,52,53,57,58,59,60,61,62)


def pickup_rooms(world):
    rooms=tuple(r for r in range(64) if world[256+4*r]&0x38)
    if rooms != PICKUP_ROOMS:
        raise ValueError('Initial treasure rooms changed; checkpoint protocol needs review')
    return rooms


def encode(state):
    unknown=set(state)-set(DEFAULTS)-{'room'}
    if unknown:raise ValueError('Unknown checkpoint fields: '+', '.join(sorted(unknown)))
    values={**DEFAULTS,**state}
    force=values.pop('force')
    if type(force) is not int or not 0<=force<=100:
        raise ValueError('Out-of-range field: force (0-100)')
    # 100 needs seven bits: the remaining high bit identifies this format.
    values['strength_tag']=0x80|force
    bits=0
    for name,width in FIELDS:
        value=values.get(name)
        if type(value) is not int or not 0<=value<(1<<width):
            raise ValueError('Out-of-range field: '+name)
        bits=(bits<<width)|value
    payload=bits.to_bytes(10,'big')
    packet=payload+binascii.crc_hqx(payload,0xFFFF).to_bytes(2,'big')
    text=packet.hex().upper()
    return '-'.join(text[i:i+6] for i in range(0,24,6))


def decode(code):
    text=''.join(ch for ch in code if ch not in '- \t\r\n')
    if len(text)==18:
        raise ValueError('Legacy 18-character checkpoint is incompatible with v2')
    if len(text)!=24 or any(ch not in '0123456789abcdefABCDEF' for ch in text):
        raise ValueError('Expected 24 hexadecimal characters')
    packet=bytes.fromhex(text);payload=packet[:10]
    if binascii.crc_hqx(payload,0xFFFF)!=int.from_bytes(packet[10:],'big'):
        raise ValueError('Checkpoint checksum mismatch')
    bits=int.from_bytes(payload,'big');state={}
    for name,width in reversed(FIELDS):
        state[name]=bits&((1<<width)-1);bits>>=width
    tag=state.pop('strength_tag')
    if tag&0x80==0 or tag&0x7F>100:
        raise ValueError('Unsupported checkpoint format or invalid strength')
    state['force']=tag&0x7F
    return state


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('decode');p.add_argument('code')
    p=sub.add_parser('encode');p.add_argument('--room',type=int,required=True)
    for name,default in DEFAULTS.items():
        p.add_argument('--'+name,type=int,default=default)
    args=vars(parser.parse_args());command=args.pop('command')
    try:
        print(json.dumps(decode(args['code']),indent=2) if command=='decode' else encode(args))
    except ValueError as error:parser.exit(2,str(error)+'\n')
