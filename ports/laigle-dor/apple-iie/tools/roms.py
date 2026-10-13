"""Read-only verification of supplied firmware; never install or patch sources."""
import json
from tools.common import ROOT, REPO, digest


def supplied_rom(kind):
    profile = json.loads((ROOT / 'resources/rom-profile.json').read_text())[kind]
    path = REPO / profile['file']
    data = path.read_bytes()
    if len(data) != profile['bytes'] or digest(data) != profile['sha256']:
        raise ValueError('Firmware identity mismatch: ' + str(path))
    return data, dict(profile)


def room_variation():
    data, profile = supplied_rom('oric')
    return data[0x1000:0x1040], profile
