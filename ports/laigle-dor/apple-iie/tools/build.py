"""Build locally with ca65/ld65, then create self-booting DOS-order and NIB disks."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.common import ROOT, REPO, digest, write_json, build_dir, video_mode, select_video
from tools.resources import export
from tools.disk import make_disk, nibble_tracks


def main(oric_rom=None):
    build = build_dir()
    build.mkdir(parents=True, exist_ok=True)
    resources = export(oric_rom)
    commands = {}
    versions = {}
    for tool in ['ca65', 'ld65']:
        path = os.environ.get(tool.upper())
        if not path:
            local = ROOT / 'local/cc65-2.19/bin' / tool
            path = str(local) if local.exists() else shutil.which(tool)
        if not path:
            raise SystemExit('Missing %s. Run make bootstrap or set %s.' % (tool, tool.upper()))
        commands[tool] = path
        result = subprocess.run([path, '--version'], capture_output=True, text=True, check=True)
        versions[tool] = (result.stdout + result.stderr).strip()

    def run(tool, *args):
        subprocess.run([commands[tool], *map(str, args)], cwd=ROOT, check=True)
    run('ca65', '--cpu', '6502', '-D', 'HGR_COLOR=%d' % (video_mode() == 'color'),
        '-D', 'DHGR=%d' % (video_mode() == 'dhgr'), '-g', '-I', ROOT / 'src', '-I', resources,
        '--bin-include-dir', resources, '-l', build / 'game.lst',
        '-o', build / 'game.o', ROOT / 'src/main.s')
    run('ld65', '-C', ROOT / ('src/dhgr.cfg' if video_mode() == 'dhgr' else 'src/game.cfg'), '-m', build / 'game.map',
        '-Ln', build / 'game.lbl', '-o', build / 'game.bin', build / 'game.o')
    program = (build / 'game.bin').read_bytes()
    end_page = 0x60 + (len(program) + 255) // 256
    if end_page > 0xA0:
        raise ValueError('Application overlaps the $A000 terrain baseline')
    run('ca65', '--cpu', '6502', '-D', 'APP_END_PAGE=%d' % end_page,
        '-l', build / 'boot.lst', '-o', build / 'boot.o', ROOT / 'src/apple/boot.s')
    run('ld65', '-C', ROOT / 'src/boot.cfg', '-o', build / 'boot.bin', build / 'boot.o')
    disk = make_disk((build / 'boot.bin').read_bytes(), program)
    (build / 'laigle-dor.do').write_bytes(disk)
    (build / 'laigle-dor.nib').write_bytes(b''.join(nibble_tracks(disk)))
    versioned = {}
    for folder in ['src', 'model', 'tools', 'resources']:
        for path in sorted((ROOT / folder).rglob('*')):
            if path.is_file() and '__pycache__' not in path.parts:
                versioned[str(path.relative_to(ROOT))] = digest(path.read_bytes())
    write_json(build / 'build-manifest.json', {
        'tools': versions, 'program_address': '$6000', 'entry': '$6000',
        'program_bytes': len(program), 'loaded_end_exclusive': '$%04X' % (end_page * 256),
        'video': 'mixed ' + ('DHGR, main+aux' if video_mode() == 'dhgr' else 'HGR') + ', alternating $2000/$4000 frames; baseline $A000',
        'video_profile': video_mode(),
        'disk_format': 'DOS-order, 35 tracks x 16 sectors x 256; custom loader; no filesystem',
        'disk_sha256': digest(disk), 'program_sha256': digest(program),
        'source_files': versioned, 'oric_rom': 'missing/provisional' if not oric_rom else 'supplied',
        'verification': 'assembled and packaged; execution recorded separately by tests'})
    print('Built %d application bytes, entry $6000, loaded end $%04X.' % (len(program), end_page * 256))
    print('%s/laigle-dor.do and laigle-dor.nib (%s)' % (build.relative_to(ROOT), video_mode()))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--oric-rom')
    main(select_video(parser).oric_rom)
