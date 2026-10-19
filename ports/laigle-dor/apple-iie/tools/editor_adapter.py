"""Optional graphics-editor library. Importing this module verifies no assets until requested."""
from pathlib import Path
from functools import lru_cache
import copy
import json
import os
import tempfile
from threading import RLock
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
TITLE = "L’Aigle d’Or · bibliothèque optionnelle"
KEY_PREFIX = 'laigle/'
from tools.common import Source, B1_SHA, B2_SHA
from tools.resources import sprite, frames, room12_scene, hgr_image
from tools.game_resources import native_artwork
from tools.title_resources import title_pages, mono_title_page
from tools.hgr_color import target_sprite
from tools import dhgr
from tools.artwork import validate_project, PROJECT_FILE

PROJECT_NAME = "L’Aigle d’Or"
SAVE_LOCK = RLock()


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
        rows = s.get('tile_rows')
        a.update(width=s['width_bytes'] * 6 if 'width_bytes' in s else s['cell_width'],
                 pixels=s['pixels'] if 'pixels' in s else [[int(v == 2) for v in row] for row in rows],
                 masks=s['masks'] if 'masks' in s else [[int(bool(v)) for v in row] for row in rows],
                 phase=s.get('color_phase', 0))
    return a


def screen_asset(key, mode, name, main, aux=None, mixed=False):
    a = dict(key=key, name=name, kind='screen', mode=mode, main=list(main), mixed=mixed,
             source={'payloads': [B1_SHA, B2_SHA], 'policy': 'Current port converter; target adaptation'})
    if aux is not None:
        a['aux'] = list(aux)
    return a


@lru_cache(maxsize=1)
def base_assets():
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
    native_mono, _, _, _ = native_artwork(source, 'mono')
    for s in native_mono:
        a = sprite_asset(s, 'laigle/game/mono/atlas/' + str(s['id']), 'mono',
                         'Atlas %03d · jeu mono' % s['id'])
        result[a['key']] = a
    for flash in (False, True):
        key = 'laigle/game/mono/title' + ('-flash' if flash else '')
        result[key] = screen_asset(key, 'mono', 'Château · mono · ' + ('éclair' if flash else 'titre'), mono_title_page(flash))
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


def stored():
    if not PROJECT_FILE.exists():
        return {'schema': 'a2-artwork-v1', 'assets': []}
    if PROJECT_FILE.stat().st_size > 32 * 1024 * 1024:
        raise ValueError('Projet local supérieur à 32 Mio')
    return validate_project(json.loads(PROJECT_FILE.read_text()))


def assets():
    result = dict(base_assets())
    for asset in stored()['assets']:
        if asset['key'] in result:
            check_contract(asset, result[asset['key']])
            result[asset['key']] = asset
    return result


def check_contract(asset, original):
    for field in ('kind', 'mode', 'width', 'height', 'encoding', 'mixed'):
        if asset.get(field) != original.get(field):
            raise ValueError('Format incompatible (%s) : %s' % (field, asset['key']))


def project_info():
    return {'name': PROJECT_NAME, 'file': 'ports/laigle-dor/apple-iie/resources/artwork.json',
            'exists': PROJECT_FILE.exists()}


def load_project():
    data = stored()
    return data.get('workspace', {'schema': 'a2-artwork-v1', 'assets': data['assets']})


def save_project(workspace):
    """Merge open native resources, then atomically replace the compiler input."""
    from project_format import validate_project as validate_workspace
    validate_workspace(workspace)
    known = base_assets()
    incoming = {}
    for doc in workspace['documents']:
        for asset in [*doc['variants'].values(), doc['asset']]:
            key = asset['key']
            if key not in known:
                if key.startswith(KEY_PREFIX):
                    raise ValueError('Ressource inconnue : ' + key)
                continue  # Generic views are preserved in the full workspace.
            check_contract(asset, known[key])
            if key in incoming and incoming[key] != asset:
                raise ValueError('Deux documents modifient la même ressource : ' + key)
            incoming[key] = copy.deepcopy(asset)
    if not incoming:
        raise ValueError('Aucune ressource native du jeu à enregistrer. Revenez au mode original du sprite.')
    # Older mono prototype sprites have the same source-dot/mask contract as
    # the full game. Keep their original key and propagate them to the mono game.
    mirrored = []
    for key, asset in list(incoming.items()):
        prefix = 'laigle/prototype/mono/sprite/'
        if key.startswith(prefix):
            target = 'laigle/game/mono/atlas/' + key[len(prefix):]
            if target in incoming and any(asset.get(field) != incoming[target].get(field)
                                          for field in ('pixels', 'masks', 'phase')):
                raise ValueError('Les copies prototype et jeu mono diffèrent : ' + target +
                                 '. Fermez la copie que vous ne souhaitez pas enregistrer.')
            if target in known and target not in incoming:
                converted = dict(copy.deepcopy(asset), key=target, name=known[target]['name'])
                check_contract(converted, known[target])
                incoming[target] = converted
                mirrored.append(target)
    with SAVE_LOCK:
        previous = stored()
        merged = {a['key']: a for a in previous['assets']}
        merged.update(incoming)
        old_docs = previous.get('workspace', {}).get('documents', [])
        incoming_keys = {d['asset']['key'] for d in workspace['documents']}
        incoming_ids = {d['id'] for d in workspace['documents']}
        docs = [d for d in old_docs if d['asset']['key'] not in incoming_keys and d['id'] not in incoming_ids]
        full_workspace = dict(workspace, documents=docs + workspace['documents'])
        validate_workspace(full_workspace)
        payload = validate_project({'schema': 'a2-artwork-v1', 'assets': list(merged.values()),
                                    'workspace': full_workspace})
        raw = (json.dumps(payload, ensure_ascii=False) + '\n').encode('utf-8')
        if len(raw) > 32 * 1024 * 1024:
            raise ValueError('Projet local supérieur à 32 Mio. Exportez les documents indépendants séparément.')
        PROJECT_FILE.parent.mkdir(parents=True, exist_ok=True)
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(dir=PROJECT_FILE.parent, prefix='.artwork-', suffix='.tmp', delete=False) as out:
                temporary = Path(out.name)
                out.write(raw)
                out.flush()
                os.fsync(out.fileno())
            os.replace(temporary, PROJECT_FILE)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
    return dict(project_info(), saved=len(incoming), mirrored=mirrored,
                message='Graphismes enregistrés dans le projet. La prochaine recompilation les utilisera.')
