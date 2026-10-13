"""Independent operation-level DHGR oracle for the native room builder.

It consumes source-backed Constructor operations, never generated geometry
bytecode. Target adaptation quantizes each atlas layer before composition.
This differs at some material boundaries from quantizing the completed Oric
raster; compare both policies and record that distinction.
"""
from tools import dhgr
from tools.video_layout import source_y
from tools.world_scene import COLORS
from tools.scenery import ART, GRILLES, SECRET


def scene_pages(constructor, operations):
    main,aux=bytearray(8192),bytearray(8192)
    def put(x,y,color):
        ty=source_y(y)
        if ty is not None and source_y(y+1)!=ty and 0<=x<240:
            dhgr.put_cell(main,aux,10+x//2,ty,color)
    for op in operations:
        if op[0]=='line':
            x,y,ex,ey=op[1:5]
            dx,dy=abs(ex-x),-abs(ey-y);sx=1 if x<ex else -1;sy=1 if y<ey else -1;err=dx+dy
            while True:
                put(x,y,15)
                if (x,y)==(ex,ey):break
                twice=2*err
                if twice>=dy:err+=dy;x+=sx
                if twice<=dx:err+=dx;y+=sy
        elif op[0]=='sprite':
            sid,left,top,add=op[1:5];s=constructor.atlas(sid)
            grille=GRILLES.get(sid)
            for j,(row,mask) in enumerate(zip(s['pixels'],s['masks'])):
                for k in range(0,len(row),2):
                    pair=row[k:k+2]
                    cut=not grille and any(pair) and not all(pair) and k>0 and k+2<len(row) and row[k-1] and row[k+2]
                    if grille:
                        if any(mask[k:k+2]):put(left+k,top+j,0)
                    elif any(pair) and not cut:put(left+k,top+j,COLORS[sid])
                    elif any(mask[k:k+2]) and (not add or grille):put(left+k,top+j,0)
            if grille:
                def occupied(x,y):
                    return any(s['masks'][y][2*x:2*x+2])
                for x,first,last in grille['bars']:
                    for j in range(first,last+1):
                        if occupied(x,j):put(left+2*x,top+j,15)
                for x,y,ex,ey in grille['rails']:
                    for col in range(x,ex+1):
                        j=y+(ey-y)*(col-x)//(ex-x)
                        for row in (j,j+1):
                            if occupied(col,row):put(left+2*col,top+row,15)
                for j,row in enumerate(ART['lock_rows'],grille['lock_row']):
                    for k,v in enumerate(row,grille['lock_cell']):
                        if v!='.':put(left+2*k,top+j,13 if v=='a' else 0)
        elif op[0]=='secret_marker':
            _,x,y,_=op
            left=(x//6+1)*6
            for j,row in enumerate(SECRET['rows']):
                for k,v in enumerate(row):put(left+2*k,y+j,5 if v=='g' else 0)
        elif op[0]=='captured_glyph':
            code,x,y=op[1:4]
            for j,bits in enumerate(constructor.font[code*8:code*8+8]):
                for k in range(3):
                    if bits & (48 >> (2*k)):put(x+2*k,y+j,13)
        else:raise ValueError('Unsupported reference operation')
    return bytes(main),bytes(aux)
