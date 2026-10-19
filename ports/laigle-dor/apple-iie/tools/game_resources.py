"""Compile a shared actor/static atlas and compact world records, no room bitmaps."""
from pathlib import Path
import textwrap
from tools.common import Source, write_json, digest, video_mode
from tools.resources import export, frames, sprite, motion
from tools.roms import room_variation
from tools.world_scene import COLORS, Constructor
from tools import dhgr
from model.world import Room
from tools.title_resources import export_title
from tools.scenery import tile, marker, SECRET
from tools.artwork import override_sprites, audit
from tools.text_panels import export_panels
from tools.debug_map import export_maps
from tools.native_sprites import compile_sprites, FAST_FLAMES

ARCHIVE_START = 96  # auxiliary atlas begins at physical track 6 / sector 0
RASTER_BYTES = 70 * 160 + 120


def hud_strings(source):
    """B2 4150-4170 descriptions; held-item names from B2 11010-11520."""
    addresses = [0x5A00, 23051, 23074, 23090, 23111, 23128,
                 23143, 23160, 23181, 23199, 23219]
    descriptions = []
    for address in addresses:
        raw = source.read(address, 40)
        if b'\\' not in raw:
            raise ValueError('Unterminated historical room description')
        descriptions.append(raw.split(b'\\', 1)[0].decode('ascii'))
    # Empty BR$ is intentional when no item is held (B2 11010).
    hands = ['', 'Torche', 'Clef en fer', 'Clef en or', 'Une fiole', 'Pied de biche']
    lines = []
    for prefix, strings in [('description', descriptions), ('hand', hands)]:
        for n, value in enumerate(strings):
            data = value.encode('ascii') + b'\0'
            lines += ['hud_%s_%d:' % (prefix, n),
                      '    .byte ' + ','.join('$%02X' % b for b in data)]
    for prefix, indices in [('description', range(len(descriptions))),
                            ('hand', [0, 1, 0, 0, 0, 0, 5, 0, 3, 2, 4])]:
        for part in ['lo', 'hi']:
            lines += ['hud_%s_%s: .byte ' % (prefix, part) +
                      ','.join(('<' if part == 'lo' else '>') + 'hud_%s_%d' % (prefix, n)
                               for n in indices)]
    return lines, {'description_addresses': ['$%04X' % a for a in addresses],
                   'descriptions': descriptions, 'hand_names': hands,
                   'source': 'B2 4150-4170, 5700-5710, 11010-11520',
                   'adaptation': 'source letter case retained; two description rows then two stats rows'}


def native_artwork(source, mode='dhgr'):
    """Shared native assets for the compiler and interactive editor; no disk writes."""
    fs = frames(source)
    for f in fs: f['layers'] = f['layers'][:2]
    fs.extend(motion(source,12,5)); fs.extend(motion(source,13,5))
    fs.append(motion(source,18)[0]); fs.append(motion(source,19)[0])
    equipment = []
    for i in range(26):
        pointer = source.word(0x4400 + 2*i); cursor = 1; layers = []
        for _ in range(32):
            cmd = source.byte(pointer+cursor); cursor += 1
            if cmd == 20: break
            if not 1 <= cmd < 20: raise ValueError('Unsupported equipment grammar')
            layers.append(list(source.read(pointer+cursor,3))); cursor += 3
        else: raise ValueError('Unbounded equipment stream')
        equipment.append(layers)
    used = sorted({r[0] for f in fs for r in f['layers']} |
                  {r[2] for rows in equipment for r in rows} | set(range(94,104)))
    native = []
    for sid in used:
        s = sprite(source,sid)
        if mode == 'mono':
            from tools.mono import actor
            native.append(actor(s))
            continue
        if sid not in dhgr.ART_PALETTE['lower_body_ids'] and str(sid) not in dhgr.ART_PALETTE['actor_bands']:
            if sid in (44,45,91,110):
                s['target_materials'] = ['hair' if y<5 else 'skin' if y<11 else 'tunic' for y in range(s['height'])]
            elif sid in (62,63,111):
                s['target_materials'] = ['trousers' if y<s['height']-8 else 'boots' for y in range(s['height'])]
            else:
                material = 'torch' if 68<=sid<=71 else 'skin' if 78<=sid<=83 else 'door'
                s['target_materials'] = [material]*s['height']
            s['target_policies'] = ['solid']*s['height']
        native.append(dhgr.target_sprite(s))
    # All rooms are built natively from a shared atlas and decoded records.
    # No per-room bitmap, pre-rendered variant or room archive is emitted.
    static_ids = sorted(set(COLORS) | {29,36,37,72,73,112,113})
    for sid in static_ids:
        if sid in used: continue
        s = sprite(source,sid)
        if mode == 'mono':
            from tools.mono import tile as mono_tile
            native.append(mono_tile(s))
        else:native.append(tile(s,COLORS.get(sid,13)))
        used.append(sid)
    if mode != 'mono':
        native.append(marker())
        used.append(SECRET['id'])
    native.sort(key=lambda s:s['id'])
    font=source.read(0x9800,2048)
    for code in range(33,42):
        sid=128+code
        width=6 if mode=='mono' else 3
        rows=[[2 if bits & ((32 >> x) if mode=='mono' else (48 >> (2*x))) else 0 for x in range(width)] for bits in font[8*code:8*code+8]]
        native.append({'id':sid,'cell_width':width,'height':8,'colors':[15 if mode=='mono' else 13]*8,'tile_rows':rows})
        used.append(sid)
    return native, fs, equipment, static_ids


def export_game():
    variation, rom = room_variation()
    source = Source(); world = source.read(0x5600,512)
    dest = export(Path(__file__).resolve().parents[4] / rom['file'])
    mode=video_mode()
    native, fs, equipment, static_ids = native_artwork(source,mode)
    native = override_sprites(native, 'laigle/game/'+mode+'/atlas/', mode)
    used = [s["id"] for s in native]
    # Generate the existing actor ABI, then append compact two-bit static tiles.
    actors=[s for s in native if 'tile_rows' not in s]
    fast_actors=[s for s in actors if mode=='mono' or s['id']<=61]
    cell_bits=1 if mode=='mono' else 4
    dhgr.generate_include(dest,actors,fs,compact_cells=True,graphics_rows=192,cell_bits=cell_bits,
                          skip_sprites={s['id'] for s in fast_actors})
    lines=(dest/'generated.inc').read_text().splitlines()
    lines[:4]=['room12_rle: .byte 0','room12_aux_rle: .byte 0','room12_grid = GRID']
    first=next((i for i,line in enumerate(lines) if any(line=='sprite_%d:'%s['id']
                for s in actors if s not in fast_actors)),len(lines))
    lines.insert(first,'.segment "ASSETS"')
    lines += ['.segment "ASSETS"']
    fast_lines, fast_report = compile_sprites(fast_actors + [s for s in native if s['id'] in FAST_FLAMES], mode)
    lines += fast_lines
    for s in native:
        if 'tile_rows' not in s or s['id'] in FAST_FLAMES: continue
        w=s['cell_width'];stride=1+(w+3)//4
        data=[w,s['height'],stride]+[(w*cell_bits+p+6)//7 for p in range(7)]+[1,dhgr.pattern(s.get('accent',0)),int(s.get('force_black',False))]+[0]*3
        for row,color in zip(s['tile_rows'],s['colors']):
            data.append(dhgr.pattern(color))
            data.extend(sum(v<<(2*k) for k,v in enumerate(row[x:x+4])) for x in range(0,w,4))
        lines.append('sprite_%d:'%s['id'])
        lines.extend('    .byte '+','.join('$%02X'%v for v in data[i:i+16]) for i in range(0,len(data),16))
    lookup={s['id']:i for i,s in enumerate(actors)}
    # Actor frame pointers keep their original actor-table indices. Static IDs
    # use an independent 256-slot pointer table instead of renumbering actors.
    lines+=['.segment "RODATA"','source_variation: .incbin "room-variation.bin"']
    lines+=['atlas_lo: .byte '+','.join('<sprite_%d'%i if i in used else '0' for i in range(max(used)+1)),
            'atlas_hi: .byte '+','.join('>sprite_%d'%i if i in used else '0' for i in range(max(used)+1))]
    lines+=['equipment_lo: .byte '+','.join('<equipment_%d'%n for n in range(26)),
            'equipment_hi: .byte '+','.join('>equipment_%d'%n for n in range(26))]
    for n,rows in enumerate(equipment):
        data=[len(rows)]+[v for dx,dy,sid in rows for v in (lookup[sid],dx,dy)]
        lines+=['equipment_%d:'%n,'    .byte '+','.join('$%02X'%v for v in data)]
    lines+=['enemy_sprite_indices: .byte '+','.join(str(lookup[n]) for n in range(94,104))]
    lines += ['full_clue_lo: .byte '+','.join('<full_clue_%d'%n for n in range(4)),
              'full_clue_hi: .byte '+','.join('>full_clue_%d'%n for n in range(4))]
    for n,name in enumerate(['scroll1.bin','scroll2.bin','scroll3.bin','book.bin']):
        text=(dest/name).read_bytes().rstrip(b'\\').decode('ascii')
        rows=textwrap.wrap(' '.join(text.split()),width=40)
        if len(rows)>3:raise ValueError('Clue exceeds compact reading panel')
        rows += ['']*(3-len(rows))
        data=''.join(row.ljust(40) for row in rows).encode('ascii')
        lines += ['full_clue_%d:'%n,'    .byte '+','.join('$%02X'%v for v in data)]
    # One shared fourth row, rather than four copies in resident memory.
    lines += ['full_clue_footer:',
              '    .byte "' + 'Une touche: indice suivant'.ljust(40) + '"']
    # Four shared geometry programs, not 64 per-room operation lists.
    # Bytecode: 1,x0,y0,x1,y1 = vector; 2,id,CURSET-x,y,additive = atlas stamp.
    templates=[]
    constructor=Constructor(source)
    for geometry in range(4):
        synthetic=bytearray(512);synthetic[8]=geometry<<6
        ops=constructor.scene(bytes(synthetic),2,bytes(64))[2]
        if geometry==3:
            repeat=next(i for i,op in enumerate(ops) if op[-1]=='B2 150')
            templates.append(('geometry_left_border',ops[repeat:]))
            ops=ops[:repeat]
        templates.append(('geometry_%d'%geometry,ops))
    for label,ops in templates:
        data=[]
        for op in ops:
            if op[0]=='line':data.extend([1,*op[1:5]])
            elif op[0]=='sprite':data.extend([2,op[1],op[5],op[3],int(op[4])])
            else:raise ValueError('Unexpected generic geometry command')
        lines += [label+':','    .byte '+','.join('$%02X'%v for v in data+[0])]
    lines += ['geometry_lo: .byte '+','.join('<geometry_%d'%g for g in range(4)),
              'geometry_hi: .byte '+','.join('>geometry_%d'%g for g in range(4))]
    hud_lines, hud_report = hud_strings(source)
    lines += hud_lines
    panel_lines, panel_report = export_panels(source, dest)
    lines += panel_lines
    map_lines, map_report = export_maps(world, dest, mode)
    lines += map_lines
    title_report=export_title(dest,mode)
    lines+=['title_flash_data: .incbin "title-flash.bin"']
    (dest/'generated.inc').write_text('\n'.join(lines)+'\n')
    for path in dest.glob('room-*.pal'):path.unlink()
    for path in dest.glob('room-*-operations.json'):path.unlink()
    for name in ['world-archive.bin','world-archive.json']:
        if (dest/name).exists():(dest/name).unlink()
    # export() also prepares the earlier W06 reference room. Keep those files
    # only in the prototype's own build directory, never in this native build.
    for path in dest.glob('room12*'):path.unlink()
    manifest=dest/'manifest.json'
    if manifest.exists():
        import json
        record=json.loads(manifest.read_text())
        record.pop('room12',None)
        record['exports']=[e for e in record['exports'] if not e['file'].startswith('room12')]
        record['note']='Common historical exports; see game-resources.json for linked native assets and source locations.'
        record['frames']=fs
        write_json(manifest,record)
    write_json(dest/'frames.json',fs)
    def provenance(sid):
        s=sprite(source,sid)
        data=source.read(s['source_start'],s['width_bytes']*s['height'])
        return {'id':sid,'cpu_start':'$%04X'%s['source_start'],
                'width_bytes':s['width_bytes'],'height':s['height'],'sha256':digest(data)}
    report={'rom':rom,'construction':'native generic geometry, upper/left/right openings, then parameterized atlas decorations',
            'room_bitmaps':0,'world_bytes':512,'variation_bytes':64,'actor_frames':len(fs),
            'actor_sprite_ids':[s['id'] for s in actors],'static_atlas_ids':static_ids,
            'native_blitter':fast_report,
            'source_atlas_records':[provenance(sid) for sid in sorted(set(static_ids)|{s['id'] for s in actors})],
            'geometry_templates':4,'equipment_streams':len(equipment),
            'title':title_report,
            'hud':hud_report,
            'text_panels':panel_report,
            'graphical_map':map_report,
            'target_scenery_art':('original Oric dots/masks, grilles and actors; B2 398 single-dot cue' if mode=='mono' else 'resources/world-art.json; white grilles, yellow locks, right-pillar secret cue, yellow/orange source flames'),
            'captured_font':'B2 $9800, provisional until original ROM/font execution is compared'}
    write_json(dest/'game-resources.json',report)
    audit(dest, {'laigle/game/'+mode+'/title', 'laigle/game/'+mode+'/title-flash'} |
          {'laigle/game/'+mode+'/atlas/' + str(s['id']) for s in native})
    return dest,report
