"""Standalone validation for native assets and non-destructive editor workspaces."""
import base64

SCHEMA = 'a2-artwork-v1'


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


def validate_native_project(project):
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


def validate_source(source, index=0):
    if not isinstance(source, dict):
        raise ValueError('Invalid source')
    if source.get('type') == 'edit':
        if not integer(source.get('base'), 0, index-1):
            raise ValueError('Invalid edit reference')
        before = validate_asset(source.get('before'))
        after = validate_asset(source.get('after'))
        for field in ('kind', 'mode', 'width', 'height', 'encoding'):
            if before.get(field) != after.get(field):
                raise ValueError('Inconsistent edit format')
    elif source.get('type') == 'native':
        validate_asset(source.get('asset'))
    elif source.get('type') == 'rgba':
        if type(source.get('mixed', False)) is not bool:
            raise ValueError('Invalid source presentation')
        w, h = source.get('width'), source.get('height')
        if not integer(w, 1, 4194304) or not integer(h, 1, 4194304) or w*h > 4194304:
            raise ValueError('Invalid source dimensions')
        if len(base64.b64decode(source.get('rgba', ''), validate=True)) != w*h*4:
            raise ValueError('Incomplete RGBA source')
        original = source.get('file')
        if original:
            if not isinstance(original.get('name'), str) or not isinstance(original.get('mime'), str):
                raise ValueError('Invalid original file metadata')
            if len(base64.b64decode(original.get('data', ''), validate=True)) > 16*1024*1024:
                raise ValueError('Original file exceeds 16 MiB')
    else:
        raise ValueError('Unknown source encoding')


def validate_project(project):
    if isinstance(project, dict) and project.get('schema') == SCHEMA:
        return validate_native_project(project)
    if not isinstance(project, dict) or project.get('schema') != 'a2-workspace-v2':
        raise ValueError('Expected a2-workspace-v2 or a2-artwork-v1')
    docs = project.get('documents')
    if not isinstance(docs, list) or len(docs) > 512:
        raise ValueError('Invalid workspace documents')
    ids = set()

    def variants(items):
        if not isinstance(items, dict):
            raise ValueError('Invalid variants')
        for mode, asset in items.items():
            validate_asset(asset)
            if mode != asset['mode']:
                raise ValueError('Variant mode mismatch')

    for d in docs:
        if not isinstance(d, dict) or not isinstance(d.get('id'), str) or d['id'] in ids:
            raise ValueError('Invalid or duplicate document ID')
        ids.add(d['id'])
        if not isinstance(d.get('name'), str) or type(d.get('frozen')) is not bool:
            raise ValueError('Invalid document metadata')
        if 'linkedModes' in d and type(d['linkedModes']) is not bool:
            raise ValueError('Invalid linked modes flag')
        sources = d.get('sources')
        if not isinstance(sources, list) or not sources or not integer(d.get('reference'), 0, len(sources)-1):
            raise ValueError('Invalid reference source')
        for index, source in enumerate(sources):
            validate_source(source, index)
        validate_asset(d.get('asset'))
        variants(d.get('variants'))
        if not isinstance(d.get('archives'), list):
            raise ValueError('Invalid archives')
        for archive in d['archives']:
            if 'linkedModes' in archive and type(archive['linkedModes']) is not bool:
                raise ValueError('Invalid archive linked modes flag')
            if not integer(archive.get('reference'), 0, len(sources)-1):
                raise ValueError('Invalid archived reference')
            variants(archive.get('variants'))
            if archive.get('active') not in archive['variants']:
                raise ValueError('Missing archived view')
    return project

