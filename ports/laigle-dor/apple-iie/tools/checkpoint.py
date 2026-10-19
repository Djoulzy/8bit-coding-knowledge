"""Versioned short checkpoints: room/inventory only; typed names stay local.

Bits are emitted MSB first, then grouped into seven payload octets. A two-octet
CRC-16/CCITT-FALSE (big endian) detects entry errors. This is reversible data,
not a hash. It intentionally does not preserve the mutable world or economy.
"""
import argparse
import binascii
import json

VERSION = 1
FIELDS = [('version',3),('room',6),('held_slot',3),('vials',8),('torches',8),
          ('ropes',8),('crowbars',8),('possessions',4),('scrolls',3),
          ('objectives',3),('padding',2)]
ITEMS = [0,1,9,8,10,6]


def validate(state):
    if state['version'] != VERSION or state['padding'] != 0:
        raise ValueError('Unsupported checkpoint version or padding')
    slot=state['held_slot']
    if slot>=len(ITEMS):raise ValueError('Invalid held-item slot')
    owned=[True,state['torches']>0,bool(state['possessions']&1),
           bool(state['possessions']&2),state['vials']>0,state['crowbars']>0]
    if not owned[slot]:raise ValueError('Held item is absent from inventory')


def encode(state):
    values={'version':VERSION,'padding':0,'held_slot':ITEMS.index(state.get('held_item',0)),
            'vials':0,'torches':0,'ropes':0,'crowbars':0,'possessions':0,
            'scrolls':0,'objectives':7,**state}
    validate(values)
    bits=0
    for name,width in FIELDS:
        value=values[name]
        if not isinstance(value,int) or not 0<=value<(1<<width):
            raise ValueError('Out-of-range field: '+name)
        bits=(bits<<width)|value
    payload=bits.to_bytes(7,'big')
    packet=payload+binascii.crc_hqx(payload,0xFFFF).to_bytes(2,'big')
    text=packet.hex().upper()
    return '-'.join(text[i:i+6] for i in range(0,18,6))


def decode(code):
    text=''.join(ch for ch in code if ch not in '- \t\r\n')
    if len(text)!=18 or any(ch not in '0123456789abcdefABCDEF' for ch in text):
        raise ValueError('Expected 18 hexadecimal characters')
    packet=bytes.fromhex(text);payload=packet[:7]
    if binascii.crc_hqx(payload,0xFFFF)!=int.from_bytes(packet[7:],'big'):
        raise ValueError('Checkpoint checksum mismatch')
    bits=int.from_bytes(payload,'big');state={}
    for name,width in reversed(FIELDS):
        state[name]=bits&((1<<width)-1);bits>>=width
    validate(state)
    state['held_item']=ITEMS[state.pop('held_slot')]
    del state['version'];del state['padding']
    return state


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('decode');p.add_argument('code')
    p=sub.add_parser('encode');p.add_argument('--room',type=int,required=True)
    for name,default in [('held_item',0),('vials',0),('torches',0),('ropes',0),
                         ('crowbars',0),('possessions',0),('scrolls',0),('objectives',7)]:
        p.add_argument('--'+name.replace('_','-'),type=int,default=default)
    args=vars(parser.parse_args());command=args.pop('command')
    try:
        print(json.dumps(decode(args['code']),indent=2) if command=='decode' else encode(args))
    except ValueError as error:parser.exit(2,str(error)+'\n')
