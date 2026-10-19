"""Native static cartography, compiled from the pinned Oric room records.

The supplied Amstrad picture is a presentation reference only. Doors and contents
come from Oric B2; this is a schematic, not a claim about physical dimensions.
"""
from model.world import Room
from tools.common import digest, write_json
from tools.resources import row_offset
from tools.text_font import glyph

MAP_SECTOR = 240
# Target monochrome artwork, seven native HGR pixels wide.
# The pin is byte-aligned at runtime and never covers numbers or contents.
PIN = [0x1C, 0x3E, 0x63, 0x6B, 0x63, 0x3E, 0x1C, 0x08, 0x08]
ICONS = {
 'chest': '0011100/0111110/1111111/1001001/1111111/1000001/1111111',
 'fireplace': '1111111/1000001/1011101/1010101/1010101/1010101/1110111',
 'stairs': '0000011/0000010/0001110/0001000/0111000/0100000/1100000',
 'furniture': '1111111/1111111/0100010/0100010/0100010/0100010/0000000',
 'scroll': '0111110/1100011/0101001/0101001/0100001/1100011/0111110',
 'gold': '0011100/0001000/0011100/0111110/1101011/1000001/0111110',
 'iron_key': '0110000/1001000/1001000/0111111/0000101/0000111/0000000',
 'gold_key': '0110000/1001000/1001000/0111111/0001010/0001110/0000000',
 'vial': '0011100/0001000/0001000/0011100/0111110/0101010/0011100',
 'ring': '0011100/0100010/1000001/1000001/1000001/0100010/0011100',
 'lead_eagle': '1000001/1100011/1111111/0011100/0001000/0011100/0011100',
 'book': '1110111/1001001/1011101/1011101/1011101/1001001/1110111',
 'diamond': '0011100/0101010/1000001/0100010/0010100/0001000/0001000',
 'golden_eagle': '1001001/1101011/1111111/0011100/0001000/0010100/0100010',
}
ITEMS = [None,'scroll','gold','iron_key','gold_key','vial','ring','lead_eagle']


def describe(world):
    rooms = [Room.decode(world, n) for n in range(64)]
    cells=[]
    # Ground-floor links embed without conflicting coordinates in this grid.
    # Catacomb ordinary doors form the perimeter cycle 1..8; room 0 is an inset.
    caves={8:(0,0),1:(1,0),2:(2,0),7:(0,1),0:(1,1),3:(2,1),6:(0,2),5:(1,2),4:(2,2)}
    for r in rooms:
        n=r.number
        if 9<=n<58:page,x,y=0,6-(n-9)%7,(n-9)//7
        elif n<9:page,x,y=1,*caves[n]
        else:page,x,y=1,(n-58)%3+4,(n-58)//3
        px=14+35*x;py=19+20*y if page==0 else 25+28*y
        item={1:'book',62:'diamond',63:'golden_eagle'}.get(n,ITEMS[r.treasure])
        furnishing={1:'fireplace',7:'chest'}.get(r.furnishing,'furniture' if r.furnishing else None)
        if r.fields[3]>1 and not furnishing:furnishing='stairs'
        cells.append({'room':n,'page':page,'x':px,'y':py,
                      'item':item,'furnishing':furnishing,'treasure':r.treasure,
                      'dark':r.light!=3,'trap':bool(r.features[0]),
                      'gate':bool(r.features[1]),
                      'secret':bool(r.fields[3]&1 and (r.furnishing==1 or n==63)),
                      'stairs':r.fields[3]>1})
    edges=[]
    for r in rooms:
        for facing,field in [(1,2),(2,1),(3,0)]:
            door=r.fields[field]
            secret=facing==3 and cells[r.number]['secret']
            if not door and not secret:continue
            target,arrival=r.transition(facing)
            exterior=r.number==12 and facing==3
            edges.append({'from':r.number,'to':None if exterior else target,
                          'facing':facing,'arrival':arrival,'type':'secret' if secret else ['wall','door','grille','arch'][door],
                          'lock':r.fields[9-facing], 'exterior':exterior})
    return cells,edges


def export_maps(world, dest, mode):
    """Both game editions package the same 280x192 one-bit MAIN HGR pages."""
    cells,edges=describe(world)
    images=[bytearray(280*192) for _ in range(3)]
    def pixel(p,x,y,value=1):
        if not (0<=x<280 and 0<=y<192):raise ValueError((p,x,y))
        images[p][y*280+x]=bool(value)
    def rect(p,x,y,w,h,value=1,fill=False):
        for j in range(h):
            for i in range(w):
                if fill or i in (0,w-1) or j in (0,h-1):pixel(p,x+i,y+j,value)
    def pattern(p,x,y,rows):
        for j,row in enumerate(rows.split('/')):
            for i,b in enumerate(row):
                if b=='1':pixel(p,x+i,y+j)
    def text(p,x,y,s):
        for k,ch in enumerate(s):
            for j,bits in enumerate(glyph(ch)):
                for i in range(5):
                    if bits&(16>>i):pixel(p,x+6*k+i,y+j)
    def icon(p,x,y,name):
        if name:pattern(p,x,y,ICONS[name])
    text(0,14,1,'Rez-de-chaussee')
    text(1,14,3,'Catacombes');text(1,154,3,'Etage')
    text(2,14,1,'Legende du plan')
    entry=cells[12]
    text(0,entry['x']-7,10,'Exterieur')
    for c in cells:
        n,p,x,y=c['room'],c['page'],c['x'],c['y']
        rect(p,x,y,36,21)
        text(p,x+3,y+3,'%02d'%n)
        icon(p,x+3,y+12,c['furnishing'])
        icon(p,x+16,y+12,c['item'])
        if c['dark']:pattern(p,x+30,y+3,'101/010/101')
        if c['trap']:pattern(p,x+32,y+12,'11/11')
        if c['gate']:pattern(p,x+32,y+17,'11/11')
        if c['secret']:pattern(p,x+1,y+11,'11/11/11')
        if c['stairs'] and c['furnishing']!='stairs':pattern(p,x+26,y+13,'001/011/110')
    pairs={}
    for edge in edges:
        if edge['to'] is None or edge['type']=='secret':continue
        a,b=cells[edge['from']],cells[edge['to']]
        if a['page']!=b['page']:continue
        dx,dy=b['x']-a['x'],b['y']-a['y']
        if abs(dx)+abs(dy)!=(35 if dx else (20 if a['page']==0 else 28)):continue
        if a['room']>=58 or b['room']>=58:continue
        pairs.setdefault(tuple(sorted((a['room'],b['room']))),[]).append(edge)
    for pair,links in pairs.items():
        a,b=(cells[n] for n in pair);p=a['page'];horizontal=a['y']==b['y']
        kinds={e['type'] for e in links}
        kind='grille' if 'grille' in kinds else 'door' if 'door' in kinds else 'arch'
        if horizontal:
            x,y=max(a['x'],b['x']),a['y']+10
            rect(p,x-2,y-3,5,7,0,True)
            if kind=='door':rect(p,x-1,y-3,3,7,1,True)
            if kind=='grille':pattern(p,x-2,y-3,'10101/11111/10101/10101/10101/11111/10101')
            if any(e['lock'] for e in links):rect(p,x+4,y+3,2,2,1,True)
        else:
            x,y=a['x']+17,min(a['y'],b['y'])+20
            gap=1 if p==0 else 9
            rect(p,x-3,y,7,gap,0,True)
            if p==1:rect(p,x-3,y,7,gap)
            if kind=='door':rect(p,x-3,y+gap//2,7,2,1,True)
            if kind=='grille':pattern(p,x-3,y+gap//2,'1010101/1111111')
            if any(e['lock'] for e in links):rect(p,x+5,y+gap//2,2,2,1,True)
    rect(0,entry['x']+14,entry['y'],7,1,0,True)
    text(1,14,116,'Liaisons hors plan')
    for i,s in enumerate(['09-58 15-59 57-60 51-61','33-62 57-06 13-00','Secrets 00-63 11-51 38-49']):text(1,14,127+11*i,s)
    for n in range(58,64):
        c=cells[n];targets=[e['to'] for e in edges if e['from']==n]
        text(1,c['x']+2,c['y']+21,'>%02d'%targets[0] if targets else '---')
    labels=[('chest','Coffre'),('fireplace','Cheminee'),('stairs','Escalier'),
            ('furniture','Meuble'),('scroll','Parchemin'),('gold','Or'),
            ('iron_key','Clef fer'),('gold_key','Clef or'),('vial','Fiole'),
            ('ring','Bague'),('lead_eagle','Plomb'),('book','Livre'),
            ('diamond','Diamant'),('golden_eagle','Aigle or')]
    for i,(name,label) in enumerate(labels):
        x=14+133*(i//7);y=17+11*(i%7)
        icon(2,x,y,name);text(2,x+12,y,label)
    for i,s in enumerate(['Epingle: vous   Noir: hachures',
                          'Porte pleine / grille a barres',
                          'Point: verrou  Vide: arche',
                          'Droite: trappe en haut, grille en bas',
                          'Trait gauche: passage secret',
                          'Objets et portes: etat initial']):text(2,14,99+10*i,s)
    # All three pages retain room/pit status, even when showing another floor.
    for p in range(3):
        text(p,7,164,'Position: salle');text(p,182,164,'Oubliette:')
        text(p,14,176,'Espace: suite  1-3: page  Echap: menu')
        text(p,14,185,'Ctrl+D: reprendre  Oubliette: X=oui')
    data=bytearray();hashes=[]
    for p,image in enumerate(images):
        main=bytearray(8192)
        for y in range(192):
            for x in range(280):
                if image[y*280+x]:main[row_offset(y)+x//7]|=1<<(x%7)
        raster=bytes(main);data+=raster;hashes.append(digest(raster))
        (dest/('map-%d.bin'%p)).write_bytes(raster)
    (dest/'maps.bin').write_bytes(data)
    report={'source':'Oric B2 $5600-$57FF; Room.decode; transition 4701-4710; door locks 10900-10990',
            'image_reference':'user supplied Amstrad plan: presentation inspiration only; no image pixels or Amstrad room data imported',
            'layout':'ground 9..57 reversed columns; catacomb 1..8 perimeter cycle with isolated room 0 inset; upper 58..63 separate cards',
            'video':'HGR one-bit MAIN, full-screen 280x192 in both game editions; bit 7 clear',
            'static':True,'position':'dynamic 7x9 white map pin beside room number; gameplay paused',
            'marker':{'width':7,'height':9,'rows_lsb_first':PIN,'x_offset':21,'y_offset':2},
            'footer':{'y':164,'room_byte_columns':[14,15],'pit_byte_column':35,'pit_codes':'X=yes, -=no'},
            'door_policy':'only source links between adjacent cells; a lock dot means at least one side is locked; types/locks can differ by side',
            'limitations':['schematic orientation and distances; not a geographic survey',
                          'quest item overrides ordinary treasure in 1/62/63',
                          'cross-floor and secret links are text references; no transient enemy prediction',
                          'icons remain initial state after pickups, opening and lighting',
                          'composite color monitors can show HGR artifact fringes; no IIe software color-kill switch'],
            'pages':3,'bytes':len(data),'disk_sector':MAP_SECTOR,'sha256':digest(data),'page_sha256':hashes,
            'cells':cells,'directed_links':edges,'drawn_door_pairs':[list(p) for p in sorted(pairs)]}
    write_json(dest/'maps.json',report)
    lines=[]
    for name,values in [('row',[c['y']+2 for c in cells]),
                        ('column',[(c['x']+21)//7 for c in cells])]:
        lines.append('map_room_%s: .byte '%name+','.join(map(str,values)))
    # Small overlays are resident so cached map pages need no AUX or disk reads.
    lines+=['.segment "CODE"','map_pin: .byte '+','.join('$%02X'%v for v in PIN),
            'map_glyphs:']
    masks=[]
    for ch in '0123456789-X':
        masks.extend(sum(1<<x for x in range(5) if row&(16>>x)) for row in glyph(ch))
    lines+=['    .byte '+','.join('$%02X'%v for v in masks[i:i+14]) for i in range(0,len(masks),14)]
    lines+=['.segment "RODATA"']
    return lines,report
