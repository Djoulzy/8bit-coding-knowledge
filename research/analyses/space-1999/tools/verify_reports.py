#!/usr/bin/env python3
"""Check report metadata, local links and pinned source line ranges."""
import ast
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[2]
FICHES = ['GEN-0003-clipped-scene-recomposition.md',
          'GEN-0004-stack-driven-pair-grammar.md',
          'ORIC-0003-parity-compressed-pixel-tables.md']


def main():
    manifest = json.loads((HERE / 'upstream-manifest.json').read_text())
    sources = {record['path']: record for record in manifest['files']}
    reports = sorted(HERE.glob('*.md'))
    assert {p.name for p in reports} == {'overview.md', 'architecture.md',
        'routines.md', 'cpu-techniques.md', 'hardware-techniques.md', 'findings.md'}
    fiches = [ROOT / 'research/findings' / name for name in FICHES]
    references, local_links = 0, 0
    for path in reports + fiches:
        text = path.read_text()
        assert text.startswith('---\n')
        metadata = dict(line.split(': ', 1) for line in text.split('---', 2)[1].strip().splitlines())
        assert metadata['id'] and metadata['cpu'] and metadata['machines']
        for key in ('cpu', 'machines', 'source_analyses', 'tags'):
            if key in metadata:
                assert isinstance(json.loads(metadata[key]), list)
        if path in fiches:
            assert metadata['status'] == 'analyzed'
        else:
            assert metadata['analysis_status'] == 'complete'
        for label, url in re.findall(r'\[([^\]]+)\]\(([^)]+)\)', text):
            if url.startswith('http'):
                parsed = urlsplit(url)
                if '#L' in url and 'Oric-Software/blob/' in url:
                    assert '/blob/' + manifest['revision'] + '/' in parsed.path
                    relative = 'games/' + unquote(parsed.path.split('/games/', 1)[1])
                    start, end = map(int, re.fullmatch(r'L(\d+)-L(\d+)', parsed.fragment).groups())
                    assert 1 <= start <= end <= sources[relative]['lines'], (path, url)
                    references += 1
            else:
                target = path.parent / unquote(url.split('#', 1)[0])
                assert target.exists(), (path, url)
                local_links += 1
    for path in (HERE / 'tools').glob('*.py'):
        ast.parse(path.read_text())
    # IDs in these new files must not collide with existing documentation.
    ids = {}
    for directory in ('docs', 'research'):
        for path in (ROOT / directory).rglob('*.md'):
            match = re.search(r'^id: (.+)$', path.read_text(), re.MULTILINE)
            if match:
                value = match[1].strip().strip('"').strip("'")
                ids.setdefault(value, []).append(path)
    for path in reports + fiches:
        value = re.search(r'^id: "([^"]+)"$', path.read_text(), re.MULTILINE)[1]
        assert ids[value] == [path], (value, ids[value])
    print(json.dumps(dict(documents=len(reports + fiches),
        pinned_source_spans_checked=references, local_links_checked=local_links,
        new_ids_unique=True, python_syntax_valid=True)))


if __name__ == '__main__':
    main()
