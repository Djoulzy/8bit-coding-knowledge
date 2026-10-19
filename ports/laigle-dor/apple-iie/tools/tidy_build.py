"""Remove regenerable legacy outputs and scratch while keeping both full games."""
import argparse
from pathlib import Path
import shutil


BUILD = Path(__file__).resolve().parents[1] / 'build'
LEGACY_ASSET_DIRS = (
    'resources', 'color/resources', 'dhgr/resources',
    'dhgr/actor-review', 'dhgr/detail-review',
)
LEGACY_OUTPUT_DIRS = (
    '.', 'color', 'dhgr',
    'dhgr/revisions/flat-v1', 'dhgr/revisions/detail-v1',
    'dhgr/revisions/palette-v1',
)
LEGACY_SUFFIXES = {'.bin', '.o', '.lst', '.lbl', '.map', '.do', '.nib'}


def has_symlink_parent(path, build):
    parent = build
    for part in path.relative_to(build).parts[:-1]:
        parent /= part
        if parent.is_symlink():
            return True
    return False


def candidates(build):
    """Select only known outputs; keep unknown files, reports and native captures."""
    if build.is_symlink():
        raise ValueError('Refusing to tidy a symlinked build directory')
    result = set()
    for relative in LEGACY_ASSET_DIRS:
        path = build / relative
        if not has_symlink_parent(path, build) and (path.exists() or path.is_symlink()):
            result.add(path)
    for relative in LEGACY_OUTPUT_DIRS:
        directory = build / relative
        if not has_symlink_parent(directory, build) and directory.is_dir() and not directory.is_symlink():
            result.update(path for path in directory.iterdir()
                          if path.is_file() and path.suffix in LEGACY_SUFFIXES)
    for name in ('game', 'game-mono'):
        directory = build / name
        if directory.is_dir() and not directory.is_symlink():
            result.update(path for path in directory.iterdir()
                          if path.is_file() and (path.suffix in {'.o', '.lst'} or
                             path.name.startswith('virtualii-') and
                             path.suffix in {'.do', '.nib'} or
                             path.name == 'title-flat-review.png'))
    # Do not walk symlinked directories, or enter archives such as latency-baseline.
    for directory in (build, build/'color', build/'dhgr',
                      build/'game', build/'game-mono'):
        if directory.is_dir() and not directory.is_symlink():
            path = directory / '.DS_Store'
            if path.exists() or path.is_symlink():
                result.add(path)
    return sorted(result)


def content_size(path):
    if path.is_symlink():
        return path.lstat().st_size
    if path.is_dir():
        return sum(p.stat().st_size for p in path.rglob('*')
                   if p.is_file() and not p.is_symlink())
    return path.stat().st_size


def tidy(build, dry_run=False):
    selected = candidates(build)
    total = sum(content_size(path) for path in selected)
    for path in selected:
        print(('Would remove: ' if dry_run else 'Removing: ') + str(path.relative_to(build)))
        if not dry_run:
            if path.is_symlink() or not path.is_dir():
                path.unlink()
            else:
                shutil.rmtree(path)
    print('%s %d outputs (%s bytes). Full games and latency baselines retained.' %
          ('Selected' if dry_run else 'Removed', len(selected), format(total, ',')))
    return len(selected), total


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true', help='List outputs without removing them')
    args = parser.parse_args()
    if BUILD.is_symlink():
        raise SystemExit('Refusing to tidy a symlinked build directory')
    tidy(BUILD, args.dry_run)


if __name__ == '__main__':
    main()
