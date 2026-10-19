"""One Oric source dot per HGR dot; no DHGR recoloring or sprite retouching."""
from tools.resources import row_offset
from tools.video_layout import source_y


def actor(s):
    return dict(s, cell_width=s['width_bytes']*6, colors=[15]*s['height'],
                statuses=[[10 if bit else 5 if mask else 0 for bit,mask in zip(row,masks)]
                          for row,masks in zip(s['pixels'],s['masks'])])


def tile(s):
    return dict(s, cell_width=s['width_bytes']*6, colors=[15]*s['height'],
                tile_rows=[[2 if bit else 1 if mask else 0 for bit,mask in zip(row,masks)]
                           for row,masks in zip(s['pixels'],s['masks'])])


def put(page,x,y,bit):
    if 0 <= x < 240 and 0 <= y < 192:
        x += 20; address=row_offset(y)+x//7; mask=1 << (x%7)
        page[address]=(page[address] | mask) if bit else (page[address] & (127 ^ mask))


def scene_page(constructor, operations):
    """Operation-level oracle; no generated atlas or geometry programs read."""
    page=bytearray(8192)
    def point(x,y,bit):
        ty=source_y(y)
        if ty is not None and source_y(y+1)!=ty:put(page,x,ty,bit)
    for op in operations:
        if op[0]=='line':
            x,y,ex,ey=op[1:5]
            dx,dy=abs(ex-x),-abs(ey-y);sx=1 if x<ex else -1;sy=1 if y<ey else -1;err=dx+dy
            while True:
                point(x,y,1)
                if (x,y)==(ex,ey):break
                twice=2*err
                if twice>=dy:err+=dy;x+=sx
                if twice<=dx:err+=dx;y+=sy
        elif op[0]=='sprite':
            sid,left,top,add=op[1:5];s=constructor.atlas(sid)
            for j,(row,masks) in enumerate(zip(s['pixels'],s['masks'])):
                for k,(bit,mask) in enumerate(zip(row,masks)):
                    if bit or (mask and not add):point(left+k,top+j,bit)
        elif op[0]=='secret_marker':point(107,108,1) # B2 398 CURSET
        elif op[0]=='captured_glyph':
            code,x,y=op[1:4]
            for j,bits in enumerate(constructor.font[8*code:8*code+8]):
                for k in range(6):
                    if bits & (32 >> k):point(x+k,y+j,1)
        else:raise ValueError('Unknown monochrome room operation')
    return bytes(page)


def actor_layer(page,s,x,y,dx=0,dy=0):
    left=(((x+dx)&255)+1)*6;top=(y+dy)&255
    if ((x+dx)&255)>=40 or top>=200:return
    for j,(row,masks) in enumerate(zip(s['pixels'],s['masks'])):
        if top+j>=200:break
        ty=source_y(top+j)
        if ty is not None:
            for k,(bit,mask) in enumerate(zip(row,masks)):
                if mask:put(page,left+k,ty,bit)
