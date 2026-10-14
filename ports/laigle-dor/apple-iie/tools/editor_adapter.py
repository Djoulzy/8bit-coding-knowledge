"""Optional graphics-editor library. Importing this module verifies no assets until requested."""
from pathlib import Path
from functools import lru_cache
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
TITLE = "L’Aigle d’Or · bibliothèque optionnelle"
KEY_PREFIX = 'laigle/'
from tools.common import Source, B1_SHA, B2_SHA
from tools.resources import sprite, frames, room12_scene, hgr_image
from tools.game_resources import native_artwork
from tools.title_resources import title_pages
from tools.hgr_color import target_sprite
from tools import dhgr
from tools.artwork import validate_project


def sprite_asset(s, key, mode, label):
    a = dict(key=key, name=label, kind='sprite', mode=mode, height=s['height'],
             source={'program': "L'Aigle d'Or (Loriciels, 1984)", 'author': 'Louis-Marie Rocques',
                     'atlas_id': s['id'], 'payload_sha256': B2_SHA,
                     'cpu_start': s.get('source_start'), 'asset_sha256': s.get('sha256')})
    if mode == 'dhgr':
        a.update(width=s['cell_width'], encoding='tile' if 'tile_rows' in s else 'actor',
                 statuses=s.get('tile_rows', s.get('statuses')), colors=s['colors'],
                 accent=s.get('accent', 0), force_black=s.get('force_black', False))
    else:
        a.update(width=s['width_bytes'] * 6, pixels=s['pixels'], masks=s['masks'], phase=s.get('color_phase', 0))
    return a


def screen_asset(key, mode, name, main, aux=None, mixed=False):
    a = dict(key=key, name=name, kind='screen', mode=mode, main=list(main), mixed=mixed,
             source={'payloads': [B1_SHA, B2_SHA], 'policy': 'Current port converter; target adaptation'})
    if aux is not None:
        a['aux'] = list(aux)
    return a


@lru_cache(maxsize=1)
def assets():
    source = Source()
    result = {}
    native, _, _, _ = native_artwork(source)
    for s in native:
        a = sprite_asset(s, 'laigle/game/dhgr/atlas/' + str(s['id']), 'dhgr',
                         'Atlas %03d · %s' % (s['id'], 'Décor' if 'tile_rows' in s else 'Personnage / objet'))
        result[a['key']] = a
    for flash in (False, True):
        key = 'laigle/game/dhgr/title' + ('-flash' if flash else '')
        result[key] = screen_asset(key, 'dhgr', 'Château · ' + ('éclair' if flash else 'titre'), *title_pages(flash))
    used = sorted({r[0] for f in frames(source) for r in f['layers']})
    for mode in ('mono', 'color', 'dhgr'):
        prefix = 'laigle/prototype/' + mode + '/'
        image, _, _ = room12_scene(source, 0, mode)
        main, aux = dhgr.image_pages(image) if mode == 'dhgr' else (hgr_image(image, mode), None)
        a = screen_asset(prefix + 'room12', mode, 'Salle 12 · prototype · ' + mode, main, aux, True)
        a['source']['variation'] = 'Provisional zero fixture, not a supplied Oric ROM'
        result[a['key']] = a
        for sid in used:
            s = sprite(source, sid)
            s = dhgr.target_sprite(s) if mode == 'dhgr' else target_sprite(s, mode)
            a = sprite_asset(s, prefix + 'sprite/' + str(sid), mode, 'Sprite %03d · prototype %s' % (sid, mode))
            result[a['key']] = a
    return result
