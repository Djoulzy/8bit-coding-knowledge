"""Convert the original B1 title, including its attribute-controlled lightning.

Only the INK/PAPER attribute subset actually present in the pinned bitmap is
accepted. No hand-drawn castle or replacement title artwork is introduced.
"""
from tools.common import Source,digest,write_json
from tools import dhgr
from tools.artwork import override_screen

ORIC_COLORS=[0,1,12,13,2,3,6,15]
MONO_SCENERY_SOURCE_ROWS=100  # castle/hills/sky; horses and title lie below


def title_image(flash=False, monochrome=False):
    source=Source();raw=bytearray(source.read(0x1801,8000,1))
    def column(x,y,height,value):
        for row in range(y,y+height):raw[row*40+x//6]=value
    # B1 1140/1150/1160: blue paper, yellow flash versus blue hidden bolt.
    column(0,0,100,20);column(66,0,100,3 if flash else 4)
    column(144,0,10,64)
    column(6,102,25,7)
    # B1 1300/1305/1308: reveal crest/title and author band.
    column(18,131,57,64);column(78,131,55,5)
    column(36,142,2,3);column(54,142,2,2);column(6,190,9,5)
    image=[[0]*240 for _ in range(224)]
    for y in range(200):
        ink,paper=7,0
        for bx,value in enumerate(raw[40*y:40*y+40]):
            if value & 0x60:
                if monochrome:
                    bits=(value&63) ^ (63 if value&128 else 0)
                    for k in range(6):image[y][bx*6+k]=int(ink!=paper and bool(bits&(32>>k)))
                else:
                    for k in range(6):image[y][bx*6+k]=ORIC_COLORS[ink if value&(32>>k) else paper]
            else:
                if value<8:ink=value
                elif 16<=value<24:paper=value-16
                else:raise ValueError('Unsupported title ULA attribute $%02X'%value)
                image[y][bx*6:bx*6+6]=[0 if monochrome else ORIC_COLORS[paper]]*6
    # The author and copyright are runtime text, not stored title pixels.
    # Retain the supplied captured 6x8 font and the original credited wording.
    font=source.read(0x9800,2048)
    def text(message,x,y,color):
        for i,ch in enumerate(message):
            for j,bits in enumerate(font[ord(ch)*8:ord(ch)*8+8]):
                for k in range(6):
                    if bits&(32>>k):image[y+j][x+i*6+k]=1 if monochrome else color
    image[190:200]=[[0]*240 for _ in range(10)]
    text('par ROCQUES Louis-Marie',54,190,3)
    text('Copyright LORICIELS 84',54,208,15)
    text('ENTREE OU ESPACE POUR JOUER',42,216,15)
    if monochrome:
        # Negative scenery only: white sky, black castle/hills, dark lightning.
        # Both phases use the same inversion, so the hidden bolt stays hidden.
        for row in image[:MONO_SCENERY_SOURCE_ROWS]:
            row[:]=[1-bit for bit in row]
    return image


def title_pages(flash=False):
    main,aux=bytearray(8192),bytearray(8192)
    for sy,row in enumerate(title_image(flash)):
        if sy<190:y=sy*160//190
        elif sy<200:y=162+sy-190
        elif sy<208:continue
        elif sy<216:y=174+sy-208
        else:y=184+sy-216
        for x in range(0,240,2):
            a,b=row[x:x+2]
            # Whole palette cells avoid composite rainbow text and castle
            # fringes. Lightning foreground wins over the blue sky.
            color=next((c for c in (a,b) if c not in (0,2)),a or b)
            code=dhgr.pattern(color)
            dhgr.put_pattern(main,aux,10+x//2,y,code)
    return bytes(main),bytes(aux)


def mono_title_page(flash=False):
    from tools.resources import row_offset
    page=bytearray(8192)
    for sy,row in enumerate(title_image(flash,monochrome=True)):
        if sy<190:y=sy*160//190
        elif sy<200:y=162+sy-190
        elif sy<208:continue
        elif sy<216:y=174+sy-208
        else:y=184+sy-216
        address=row_offset(y);page[address:address+40]=bytes(40)
        for x,bit in enumerate(row):
            if bit:page[address+(x+20)//7] |= 1 << ((x+20)%7)
    return bytes(page)


def export_title(dest, mode='dhgr'):
    if mode=='mono':
        off,on=mono_title_page(False),mono_title_page(True)
        edited=override_screen('laigle/game/mono/title', 'mono', off)[0]
        on=bytes(b if a != b else e for a,b,e in zip(off,on,edited))
        off=edited
        on=override_screen('laigle/game/mono/title-flash', 'mono', on)[0]
        (dest/'title.hgr').write_bytes(off)
        patch=bytearray()
        for offset,(a,b) in enumerate(zip(off,on)):
            if a!=b:patch.extend([offset&255,offset>>8,b,a])
        patch.extend([255,255]);(dest/'title-flash.bin').write_bytes(patch)
        report={'source_block':'B1','cpu_range':'$1801-$3740',
                'source_sha256':digest(Source().read(0x1801,8000,1)),
                'raster_bytes':len(off),'raster_sha256':digest(off),'patch_bytes':len(patch),
                'conversion':'Oric foreground dots at x+20; 190->160 title rows; original captured-font credits and native-height keyboard prompt',
                'palette':'monochrome; source rows 0..99 inverted: white sky, black castle/hills and dark lightning; equal ink/paper hides lightning',
                'timing':'target frame counter; original WAIT/audio timing not reproduced'}
        write_json(dest/'title-manifest.json',report)
        return report
    off=title_pages(False);on=title_pages(True)
    edited=override_screen('laigle/game/dhgr/title', 'dhgr', *off)
    # Preserve edits in both animation states except at the original lightning
    # delta. An explicit flash-state edit takes precedence there too.
    on=tuple(bytes(b if a != b else e for a,b,e in zip(off[bank],on[bank],edited[bank])) for bank in range(2))
    off=edited
    on=override_screen('laigle/game/dhgr/title-flash', 'dhgr', *on)
    data=off[0]+off[1];(dest/'title.dhgr').write_bytes(data)
    patch=bytearray()
    for bank in range(2):
        for offset,(a,b) in enumerate(zip(off[bank],on[bank])):
            if a!=b:patch.extend([offset&255,(offset>>8)|(bank<<7),b,a])
    patch.extend([255,255])
    (dest/'title-flash.bin').write_bytes(patch)
    report={'source_block':'B1','cpu_range':'$1801-$3740',
        'source_sha256':digest(Source().read(0x1801,8000,1)),
        'script_lines':[1010,1020,1140,1150,1160,1300,1305,1308,1309,1310],
        'raster_sha256':digest(data),'raster_bytes':len(data),'patch_bytes':len(patch),
        'conversion':'source graphic 0..189 -> rows 0..159; native-height credits at 162/174/184; complete palette cells for uniform color; x margin 10 cells',
        'text_font':'B2 captured $9800; Oric final ROM CHAR output not runtime verified',
        'timing':'target vertical-blank frame counter; not original WAIT/audio timing',
        'palette':'Oric blue -> Apple dark blue; yellow lightning; magenta title; red/green crest',
        'prompt':'new Apple keyboard instruction, not historical pixels'}
    write_json(dest/'title-manifest.json',report)
    return report
