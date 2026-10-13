"""Shared DHGR atlas policy, with explicit source/target art separation."""
import json
from tools.common import ROOT

ART = json.loads((ROOT / 'resources/world-art.json').read_text())
GRILLES = {int(sid): p for sid, p in ART['grilles'].items()}
SECRET = ART['secret_marker']


def tile(s, color):
    grille = GRILLES.get(s['id'])
    rows = []
    for row, mask in zip(s['pixels'], s['masks']):
        output = []
        for x in range(0, len(row), 2):
            pair = row[x:x+2]
            cut = (not grille and any(pair) and not all(pair) and x > 0
                   and x+2 < len(row) and row[x-1] and row[x+2])
            output.append(2 if any(pair) and not cut else 1 if any(mask[x:x+2]) else 0)
        rows.append(output)
    if grille:
        # A pair of source one-dot outlines can merge into a solid native cell.
        # Keep the perspective/silhouette, substitute separated one-cell bars.
        rows = [[1 if v else 0 for v in row] for row in rows]
        for x,top,bottom in grille['bars']:
            for y in range(top,bottom+1):
                if rows[y][x]: rows[y][x]=2
        for x,y,end_x,end_y in grille['rails']:
            for col in range(x,end_x+1):
                row=y+(end_y-y)*(col-x)//(end_x-x)
                for j in (row,row+1):
                    if rows[j][col]:rows[j][col]=2
        for j, row in enumerate(ART['lock_rows'], grille['lock_row']):
            for k, v in enumerate(row, grille['lock_cell']):
                if v != '.': rows[j][k] = 3 if v == 'a' else 1
    # Original two-frame wall flames: yellow tips, orange base. Hand flames
    # use the same source-derived atlas policy and palette.
    flame = s['id'] in (36, 37, 72, 73)
    if flame:
        for row in rows[-6:]:
            row[:] = [3 if c == 2 else c for c in row]
    return dict(s, cell_width=s['width_bytes']*3, colors=[15 if grille else color]*s['height'],
                tile_rows=rows, accent=13 if grille else 9 if flame else 0,
                force_black=bool(grille))


def marker():
    rows = [[2 if v == 'g' else 1 for v in row] for row in SECRET['rows']]
    return {'id': SECRET['id'], 'cell_width': len(rows[0]), 'height': len(rows),
            'colors': [5]*len(rows), 'tile_rows': rows}
