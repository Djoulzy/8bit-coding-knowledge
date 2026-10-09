#!/usr/bin/env python3
"""Fetch pinned reference text into a separate scratch directory; execute nothing."""
import argparse
import concurrent.futures
import hashlib
import json
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    manifest = json.loads((HERE / 'upstream-manifest.json').read_text())
    def fetch(record):
        data = urllib.request.urlopen(record['url'], timeout=60).read()
        assert len(data) == record['bytes']
        assert hashlib.sha256(data).hexdigest() == record['sha256']
        blob = b'blob ' + str(len(data)).encode() + b'\0' + data
        assert hashlib.sha1(blob).hexdigest() == record['sha1']
        relative = record['path'].split('/Sources/', 1)[1]
        target = args.destination / relative
        assert not target.exists(), f'Refusing to overwrite {target}'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(fetch, manifest['files']))
    print(f"Verified {len(manifest['files'])} reference files")


if __name__ == '__main__':
    main()

