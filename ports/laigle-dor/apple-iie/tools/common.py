import hashlib
from pathlib import Path
import json
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
ANALYSIS = REPO / 'research/analyses/laigle-dor'
TAP_SHA = '7f01e1a3d05825aab887952cd5711bea69d6525730aba5c1e25c814334fe77d7'
B1_SHA = 'e0c58b933133459eb7d38476cab0fb4f49b5964afd0db8982915b36a42be3340'
B2_SHA = '0753ce4ed6c8904118fbd9e40ef459fa46140a770e00902213794ef2c33c28ac'


def video_mode():
    mode = os.environ.get('LAIGLE_VIDEO', 'mono')
    if mode not in ('mono', 'color', 'dhgr'):
        raise ValueError('LAIGLE_VIDEO must be mono, color or dhgr')
    return mode


def build_dir(mode=None):
    mode = mode or video_mode()
    if mode not in ('mono', 'color', 'dhgr'):
        raise ValueError('Unknown video profile: ' + mode)
    if os.environ.get('LAIGLE_STAGE') == 'game':
        if mode == 'color': raise ValueError('Full game profiles are mono or dhgr')
        return ROOT / ('build/game-mono' if mode == 'mono' else 'build/game')
    return ROOT / ('build/' + mode if mode != 'mono' else 'build')


def select_video(parser):
    parser.add_argument('--video', choices=['mono', 'color', 'dhgr'], default=video_mode())
    args = parser.parse_args()
    os.environ['LAIGLE_VIDEO'] = args.video
    return args


def digest(data):
    return hashlib.sha256(data).hexdigest()


class Source:
    def __init__(self):
        original = REPO / "research/sources/Oric/L'Aigle d'Or/Aigle D'or, Le (1984)(Loriciels).tap"
        if original.exists() and digest(original.read_bytes()) != TAP_SHA:
            raise ValueError('Original TAP checksum mismatch')
        self.blocks = {}
        for i, expected in [(1, B1_SHA), (2, B2_SHA)]:
            data = (ANALYSIS / ('extracted/aigledor.%d.bin' % i)).read_bytes()
            if digest(data) != expected:
                raise ValueError('Historical payload checksum mismatch')
            self.blocks[i] = data

    def read(self, address, length, block=2):
        offset = address - 0x0501
        data = self.blocks[block]
        if offset < 0 or length < 0 or offset + length > len(data):
            raise ValueError('Source range outside payload')
        return data[offset:offset + length]

    def byte(self, address):
        return self.read(address, 1)[0]

    def word(self, address):
        return int.from_bytes(self.read(address, 2), 'little')


def load_py65():
    sys.path.insert(0, str(ROOT / 'local/py65-1.2.0'))
    try:
        from py65.devices.mpu6502 import MPU
    except ImportError as exc:
        raise SystemExit('Run python3 tools/bootstrap.py first (py65 missing).') from exc
    return MPU


def labels(directory=None):
    result = {}
    for line in ((directory or build_dir()) / 'game.lbl').read_text().splitlines():
        parts = line.split()
        if len(parts) == 3:
            result[parts[2].lstrip('.')] = int(parts[1], 16)
    return result


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')
