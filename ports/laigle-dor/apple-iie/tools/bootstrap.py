"""Install pinned build/test tools locally; never install into system directories."""
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import tarfile
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def fetch(url, sha):
    cache = ROOT / 'local' / 'downloads' / sha
    if not cache.exists():
        cache.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(url, timeout=60) as response:
            cache.write_bytes(response.read())
    data = cache.read_bytes()
    if hashlib.sha256(data).hexdigest() != sha:
        raise ValueError('Checksum mismatch: ' + url)
    return data


def unpack(data, destination):
    destination.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(data), mode='r:gz') as archive:
        # Reject traversal and links before extraction, including Python 3.9.
        for member in archive.getmembers():
            target = (destination / member.name).resolve()
            if destination.resolve() not in target.parents or member.issym() or member.islnk():
                raise ValueError('Unsafe archive member: ' + member.name)
        archive.extractall(destination)


def main():
    lock = json.loads((ROOT / 'tools/dependencies.json').read_text())
    for name in ['cc65', 'py65']:
        dep = lock[name]
        target = ROOT / 'local' / dep['directory']
        if not target.exists():
            unpack(fetch(dep['url'], dep['sha256']), ROOT / 'local')
    # Reviewed V2.19 src/Makefile: compile/link these two tools only; no install.
    subprocess.run(['make', '-C', str(ROOT / 'local/cc65-2.19/src'), '-j4',
                    'ca65', 'ld65', 'BUILD_ID=V2.19'], check=True)
    romdir = ROOT / 'local/roms'
    romdir.mkdir(exist_ok=True)
    for name in ['disk2', 'apple2e']:
        dep = lock[name]
        data = fetch(dep['url'], dep['sha256']).decode()
        array = data.split('new Uint8Array([')[1].split('])')[0]
        rom = bytes(int(x, 16) for x in re.findall(r'0x([0-9a-fA-F]{2})', array))
        if hashlib.sha256(rom).hexdigest() != dep['rom_sha256']:
            raise ValueError('Decoded ROM mismatch: ' + name)
        (romdir / (name + '.rom')).write_bytes(rom)
    print('Tools and test ROMs are ready in local/. No system installation.')


if __name__ == '__main__':
    main()
