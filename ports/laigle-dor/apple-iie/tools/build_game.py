"""Build the world/action port independently of the accepted graphics prototype."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from tools.common import ROOT, build_dir, digest, write_json
from tools.game_resources import export_game, ARCHIVE_START
from tools.disk import make_disk, offset, nibble_tracks


def main():
    os.environ['LAIGLE_STAGE']='game'; os.environ['LAIGLE_VIDEO']='dhgr'
    build=build_dir();build.mkdir(parents=True,exist_ok=True)
    resources, resource_report=export_game()
    commands={}
    for tool in ['ca65','ld65']:
        commands[tool]=os.environ.get(tool.upper()) or str(ROOT/'local/cc65-2.19/bin'/tool)
        if not Path(commands[tool]).exists(): commands[tool]=shutil.which(tool)
        if not commands[tool]: raise SystemExit('Run make bootstrap: missing '+tool)
    def run(tool,*args):subprocess.run([commands[tool],*map(str,args)],cwd=ROOT,check=True)
    run('ca65','--cpu','6502','-D','FULL_GAME=1','-D','DHGR=1','-D','HGR_COLOR=0','-g',
        '-I',ROOT/'src','-I',resources,'--bin-include-dir',resources,
        '-l',build/'game.lst','-o',build/'game.o',ROOT/'src/full-main.s')
    run('ld65','-C',ROOT/'src/full.cfg','-m',build/'game.map','-Ln',build/'game.lbl',
        '-o',build/'game.bin',build/'game.o')
    program=(build/'game.bin').read_bytes();end_page=0x60+(len(program)+255)//256
    if len(program)> (ARCHIVE_START-1)*256: raise ValueError('Application overlaps shared atlas sectors')
    run('ca65','--cpu','6502','-D','FULL_GAME=1','-D','APP_END_PAGE=%d'%end_page,
        '-l',build/'boot.lst','-o',build/'boot.o',ROOT/'src/apple/boot.s')
    run('ld65','-C',ROOT/'src/boot.cfg','-o',build/'boot.bin',build/'boot.o')
    disk=bytearray(make_disk((build/'boot.bin').read_bytes(),program))
    atlas=(build/'aux-assets.bin').read_bytes()
    if not 0 < len(atlas) <= 16384: raise ValueError('Shared atlas exceeds auxiliary allocation')
    for i,start in enumerate(range(0,len(atlas),256),ARCHIVE_START):
        track,s=divmod(i,16);a=offset(track,s)
        disk[a:a+256]=atlas[start:start+256].ljust(256,b'\0')
    title=(resources/'title.dhgr').read_bytes()
    if len(title)!=16384:raise ValueError('Title raster must contain both complete DHGR banks')
    for i,start in enumerate(range(0,len(title),256),160):
        track,s=divmod(i,16);a=offset(track,s)
        disk[a:a+256]=title[start:start+256]
    (build/'laigle-dor.do').write_bytes(disk)
    (build/'laigle-dor.nib').write_bytes(b''.join(nibble_tracks(disk)))
    versions={t:subprocess.check_output([commands[t],'--version'],stderr=subprocess.STDOUT,text=True).strip() for t in commands}
    write_json(build/'build-manifest.json',{'stage':'world-game','tools':versions,
        'program_sha256':digest(program),'program_bytes':len(program),'entry':'$6000',
        'loaded_end_exclusive':'$%04X'%(end_page*256),'resources':resource_report,
        'atlas_bytes':len(atlas),'atlas_sha256':digest(atlas),
        'title_sector':160,'title_bytes':len(title),'title_sha256':digest(title),
        'disks':{'laigle-dor.do':digest(disk)},
        'validation':'assembled/packaged; execution evidence recorded separately'})
    print('World port: %d application bytes; %d shared atlas bytes; one Disk II image'%(len(program),len(atlas)))


if __name__=='__main__':main()
