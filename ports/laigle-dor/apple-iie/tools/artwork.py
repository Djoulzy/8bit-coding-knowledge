"""Versioned, opt-in target artwork overrides; historical sources stay read-only."""
import json
import os
from pathlib import Path
from tools.common import digest

SCHEMA = 'a2-artwork-v1'
PROJECT_FILE = Path(__file__).resolve().parents[1] / 'resources/artwork.json'


def integer(value, low, high):
    return type(value) is int and low <= value <= high


def vector(value, size, maximum):
    return isinstance(value, list) and len(value) == size and all(integer(v, 0, maximum) for v in value)


def validate_asset(a):
    if not isinstance(a, dict) or not isinstance(a.get('key'), str) or len(a['key']) > 160:
        raise ValueError('Invalid asset key')
    kind = a.get('kind')
    mode = a.get('mode')
    if mode not in ('mono', 'color', 'hgr', 'dhgr', 'dhgr-mono', 'lowres'):
        raise ValueError('Invalid graphics mode')
    if kind == 'screen':
        size = 1024 if mode == 'lowres' else 8192
        if not vector(a.get('main'), size, 255):
            raise ValueError('Incorrect main bank length or byte value')
        if mode in ('dhgr', 'dhgr-mono') and not vector(a.get('aux'), 8192, 255):
            raise ValueError('DHGR needs a complete auxiliary bank')
        if type(a.get('mixed', False)) is not bool:
            raise ValueError('Invalid mixed mode')
    elif kind == 'sprite':
        w, h = a.get('width'), a.get('height')
        if not integer(w, 1, 140) or not integer(h, 1, 200):
            raise ValueError('Invalid sprite dimensions')
        field = 'statuses' if mode == 'dhgr' else 'pixels'
        rows = a.get(field)
        maximum = 3 if a.get('encoding') == 'tile' else 15 if mode == 'dhgr' else 1
        if not isinstance(rows, list) or len(rows) != h or not all(vector(r, w, maximum) for r in rows):
            raise ValueError('Invalid sprite rows')
        if mode == 'dhgr':
            if a.get('encoding') not in ('tile', 'actor') or not vector(a.get('colors'), h, 15):
                raise ValueError('Invalid DHGR sprite encoding/colors')
            # These are the statuses emitted by the port. Others do not have a
            # meaningful foreground/opacity relationship in its sprite ABI.
            if a['encoding'] == 'actor' and any(v not in (0, 1, 3, 4, 5, 7, 10, 12, 13, 15) for r in rows for v in r):
                raise ValueError('Invalid actor opacity/foreground status')
            if not integer(a.get('accent', 0), 0, 15) or type(a.get('force_black', False)) is not bool:
                raise ValueError('Invalid tile accent or black policy')
        elif mode in ('mono', 'color'):
            if not isinstance(a.get('masks'), list) or len(a['masks']) != h or not all(vector(r, w, 1) for r in a['masks']):
                raise ValueError('Invalid sprite opacity mask')
            if a.get('phase', 0) not in (0, 128):
                raise ValueError('HGR phase must be 0 or 128')
            if any(p and not m for row, mask in zip(rows, a['masks']) for p, m in zip(row, mask)):
                raise ValueError('Foreground pixels must be opaque')
        else:
            raise ValueError('Native sprites support mono, color or DHGR')
    else:
        raise ValueError('Invalid asset kind')
    return a


def validate_project(project):
    if not isinstance(project, dict) or project.get('schema') != SCHEMA or not isinstance(project.get('assets'), list):
        raise ValueError('Expected a2-artwork-v1 project')
    if len(project['assets']) > 512:
        raise ValueError('Too many assets')
    keys = set()
    for a in project['assets']:
        validate_asset(a)
        if a['key'] in keys:
            raise ValueError('Duplicate asset key: ' + a['key'])
        keys.add(a['key'])
    return project


def configured():
    filename = os.environ.get('LAIGLE_ARTWORK', str(PROJECT_FILE) if PROJECT_FILE.exists() else '')
    if not filename:
        return None
    path = Path(filename).expanduser()
    if path.stat().st_size > 32 * 1024 * 1024:
        raise ValueError('Artwork project exceeds 32 MiB')
    raw = path.read_bytes()
    return validate_project(json.loads(raw)), {'file': str(path.resolve()), 'sha256': digest(raw)}


def replacement(key):
    config = configured()
    return next((a for a in config[0]['assets'] if a['key'] == key), None) if config else None


def override_screen(key, mode, main, aux=None):
    a = replacement(key)
    if a is None:
        return main, aux
    if a['kind'] != 'screen' or a['mode'] != mode:
        raise ValueError('Screen override format mismatch: ' + key)
    return bytes(a['main']), bytes(a['aux']) if mode == 'dhgr' else None


def override_sprites(sprites, prefix, mode):
    result = []
    config = configured()
    edits = {a['key']: a for a in config[0]['assets']} if config else {}
    for s in sprites:
        a = edits.get(prefix + str(s['id']))
        if a is None:
            result.append(s)
            continue
        width = s['cell_width'] if 'cell_width' in s else s['width_bytes'] * 6
        encoding = 'tile' if 'tile_rows' in s else 'actor'
        if (a['kind'], a['mode'], a['width'], a['height']) != ('sprite', mode, width, s['height']):
            raise ValueError('Sprite override dimensions/format mismatch: ' + a['key'])
        if mode == 'dhgr':
            if a['encoding'] != encoding:
                raise ValueError('Sprite override encoding mismatch: ' + a['key'])
            s = dict(s, colors=a['colors'])
            s['tile_rows' if encoding == 'tile' else 'statuses'] = a['statuses']
            if encoding == 'tile':
                s.update(accent=a.get('accent', 0), force_black=a.get('force_black', False))
        else:
            s = dict(s, pixels=a['pixels'], masks=a['masks'], color_phase=a.get('phase', 0))
            if mode == 'mono':
                if 'tile_rows' in s:
                    s['tile_rows'] = [[2 if p else 1 if m else 0 for p, m in zip(row, mask)]
                                      for row, mask in zip(a['pixels'], a['masks'])]
                elif 'statuses' in s:
                    s['statuses'] = [[10 if p else 5 if m else 0 for p, m in zip(row, mask)]
                                     for row, mask in zip(a['pixels'], a['masks'])]
        result.append(s)
    return result


def audit(dest, supported):
    """Record which edits this build consumes, including other target variants."""
    config = configured()
    if config:
        project, report = config
        keys = [a['key'] for a in project['assets']]
        unknown = [k for k in keys if k.startswith('laigle/') and k not in supported]
        # Projects may hold several targets. Report other variants explicitly.
        report.update(applied=[k for k in keys if k in supported], unused=[k for k in keys if k not in supported])
        (dest / 'artwork-overrides.json').write_text(json.dumps(report, indent=2) + '\n')
        if unknown:
            print('Artwork not consumed by this build: ' + ', '.join(unknown))
    else:
        (dest / 'artwork-overrides.json').unlink(missing_ok=True)
