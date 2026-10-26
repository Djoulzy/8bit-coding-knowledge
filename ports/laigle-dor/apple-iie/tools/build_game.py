"""Build the world/action port independently of the accepted graphics prototype."""
import os
import argparse
from pathlib import Path
import shutil
import subprocess
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from tools.common import ROOT, Source, build_dir, digest, write_json, labels
from tools.game_resources import export_game, ARCHIVE_START
from tools.disk import make_disk, offset, nibble_tracks
from tools.text_panels import TEXT_SECTOR
from tools.debug_map import MAP_SECTOR
from tools.native_sprites import EXTRA_SECTOR, EXTRA_CAPACITY
from tools.ending_resources import END_SECTOR
from tools import checkpoint


def main(mode='dhgr'):
    os.environ['LAIGLE_STAGE']='game'; os.environ['LAIGLE_VIDEO']=mode
    build=build_dir();build.mkdir(parents=True,exist_ok=True)
    resources, resource_report=export_game()
    commands={}
    for tool in ['ca65','ld65']:
        commands[tool]=os.environ.get(tool.upper()) or str(ROOT/'local/cc65-2.19/bin'/tool)
        if not Path(commands[tool]).exists(): commands[tool]=shutil.which(tool)
        if not commands[tool]: raise SystemExit('Run make bootstrap: missing '+tool)
    def run(tool,*args):subprocess.run([commands[tool],*map(str,args)],cwd=ROOT,check=True)
    run('ca65','--cpu','6502','-D','FULL_GAME=1','-D','DHGR=%d'%(mode=='dhgr'),
        '-D','HGR_MONO=%d'%(mode=='mono'),'-D','HGR_COLOR=0','-g',
        '-I',ROOT/'src','-I',resources,'--bin-include-dir',resources,
        '-l',build/'game.lst','-o',build/'game.o',ROOT/'src/full-main.s')
    run('ld65','-C',ROOT/('src/full-mono.cfg' if mode=='mono' else 'src/full.cfg'),'-m',build/'game.map','-Ln',build/'game.lbl',
        '-o',build/'game.bin',build/'game.o')
    # Endings replace MAIN's disposable room baseline. Their small renderer
    # and captured font travel with the selected picture, not resident RAM.
    symbols=labels(build)
    # Checkpoint UI temporarily replaces the baseline, sharing no executing
    # code with the room constructor. Final disk track is its bounded slot.
    (resources/'checkpoint-rooms.bin').write_bytes(bytes(checkpoint.pickup_rooms(Source().read(0x5600,512))))
    (resources/'checkpoint-symbols.inc').write_text(''.join(
        '%s = $%04X\n'%(name,symbols[name]) for name in [
            'full_text_address','full_hud_string','debug_teleport','game_reset',
            'reset_torch_life','reset_bar_life','name_count']))
    run('ca65','--cpu','6502','-D','FULL_GAME=1','-D','DHGR=%d'%(mode=='dhgr'),
        '-D','HGR_MONO=%d'%(mode=='mono'),'-I',ROOT/'src','-I',resources,
        '--bin-include-dir',resources,'-o',build/'checkpoint.o',ROOT/'src/apple/checkpoint-overlay.s')
    run('ld65','-C',ROOT/'src/checkpoint.cfg','-Ln',build/'checkpoint.lbl',
        '-o',build/'checkpoint.bin',build/'checkpoint.o')
    checkpoint_module=(build/'checkpoint.bin').read_bytes()
    if not 0<len(checkpoint_module)<=checkpoint.CAPACITY:
        raise ValueError('Checkpoint module exceeds final disk track')
    resource_report['checkpoint']={'version':checkpoint.VERSION,'packet_bytes':12,
        'payload_bytes':10,'hex_characters':24,'pickup_rooms':list(checkpoint.PICKUP_ROOMS),
        'module_address':'$A000','sector':checkpoint.SECTOR,
        'module_bytes':len(checkpoint_module),'module_sha256':digest(checkpoint_module)}
    (resources/'ending-symbols.inc').write_text(''.join(
        '%s = $%04X\n'%(name,symbols[name]) for name in ['row_lo','row_hi','draw_cell']))
    run('ca65','--cpu','6502','-D','HGR_MONO=%d'%(mode=='mono'),'-I',ROOT/'src','-I',resources,
        '--bin-include-dir',resources,'-o',build/'ending.o',ROOT/'src/apple/ending-overlay.s')
    run('ld65','-C',ROOT/'src/ending.cfg','-Ln',build/'ending.lbl',
        '-o',build/'ending-engine.bin',build/'ending.o')
    engine=(build/'ending-engine.bin').read_bytes()
    endings=bytearray()
    for scene in resource_report['endings']['scenes']:
        data=engine+(resources/(scene['name']+'.rle')).read_bytes()
        if len(data)>8192:raise ValueError('Ending overlay exceeds MAIN baseline')
        scene['overlay_bytes']=len(data);scene['overlay_sha256']=digest(data)
        endings.extend(data.ljust(8192,b'\0'))
    (build/'endings.bin').write_bytes(endings)
    resource_report['endings'].update(engine_bytes=len(engine),engine_sha256=digest(engine),
        overlay_address='$A000',archive_bytes=len(endings),archive_sha256=digest(endings))
    write_json(resources/'ending-manifest.json',resource_report['endings'])
    write_json(resources/'game-resources.json',resource_report)
    program=(build/'game.bin').read_bytes();end_page=0x60+(len(program)+255)//256
    if len(program)> (ARCHIVE_START-1)*256: raise ValueError('Application overlaps shared atlas sectors')
    run('ca65','--cpu','6502','-D','FULL_GAME=1','-D','APP_END_PAGE=%d'%end_page,
        '-l',build/'boot.lst','-o',build/'boot.o',ROOT/'src/apple/boot.s')
    run('ld65','-C',ROOT/'src/boot.cfg','-o',build/'boot.bin',build/'boot.o')
    disk=bytearray(make_disk((build/'boot.bin').read_bytes(),program))
    atlas=(build/'aux-assets.bin').read_bytes()
    if not 0 < len(atlas) <= (24576 if mode=='mono' else 16384): raise ValueError('Shared atlas exceeds auxiliary allocation')
    for i,start in enumerate(range(0,len(atlas),256),ARCHIVE_START):
        track,s=divmod(i,16);a=offset(track,s)
        disk[a:a+256]=atlas[start:start+256].ljust(256,b'\0')
    title=(resources/('title.hgr' if mode=='mono' else 'title.dhgr')).read_bytes()
    title_sector=192 if mode=='mono' else 160
    if len(title)!=(8192 if mode=='mono' else 16384):raise ValueError('Unexpected title raster size')
    if ARCHIVE_START+(len(atlas)+255)//256>title_sector:raise ValueError('Atlas sectors overlap title')
    for i,start in enumerate(range(0,len(title),256),title_sector):
        track,s=divmod(i,16);a=offset(track,s)
        disk[a:a+256]=title[start:start+256]
    text_assets=(build/'text-assets.bin').read_bytes()
    if not 0 < len(text_assets) <= 0xC00:raise ValueError('Low auxiliary text allocation exceeded')
    for i,start in enumerate(range(0,len(text_assets),256),TEXT_SECTOR):
        track,s=divmod(i,16);a=offset(track,s)
        disk[a:a+256]=text_assets[start:start+256].ljust(256,b'\0')
    maps=(resources/'maps.bin').read_bytes()
    if TEXT_SECTOR+(len(text_assets)+255)//256>MAP_SECTOR or MAP_SECTOR+len(maps)//256>560:
        raise ValueError('Map disk allocation overlap or overflow')
    for i,start in enumerate(range(0,len(maps),256),MAP_SECTOR):
        track,s=divmod(i,16);a=offset(track,s)
        disk[a:a+256]=maps[start:start+256]
    extra=(build/'extra-assets.bin').read_bytes()
    if len(extra)>EXTRA_CAPACITY or MAP_SECTOR+(len(maps)+255)//256>EXTRA_SECTOR:
        raise ValueError('Native row allocation overlap')
    for i,start in enumerate(range(0,len(extra),256),EXTRA_SECTOR):
        track,s=divmod(i,16);a=offset(track,s)
        disk[a:a+256]=extra[start:start+256].ljust(256,b'\0')
    if EXTRA_SECTOR+(len(extra)+255)//256>END_SECTOR or END_SECTOR+len(endings)//256>checkpoint.SECTOR:
        raise ValueError('Ending disk allocation overlap or overflow')
    for i,start in enumerate(range(0,len(endings),256),END_SECTOR):
        track,s=divmod(i,16);a=offset(track,s)
        disk[a:a+256]=endings[start:start+256]
    module_slot=checkpoint_module.ljust(checkpoint.CAPACITY,b'\0')
    if checkpoint.SECTOR+len(module_slot)//256>560:
        raise ValueError('Checkpoint disk allocation overflow')
    for i,start in enumerate(range(0,len(module_slot),256),checkpoint.SECTOR):
        track,s=divmod(i,16);a=offset(track,s)
        disk[a:a+256]=module_slot[start:start+256]
    (build/'laigle-dor.do').write_bytes(disk)
    (build/'laigle-dor.nib').write_bytes(b''.join(nibble_tracks(disk)))
    disk_name='laigle-dor-hgr-mono' if mode=='mono' else 'laigle-dor-dhgr-color'
    (build/(disk_name+'.do')).write_bytes(disk)
    (build/(disk_name+'.nib')).write_bytes((build/'laigle-dor.nib').read_bytes())
    versions={t:subprocess.check_output([commands[t],'--version'],stderr=subprocess.STDOUT,text=True).strip() for t in commands}
    write_json(build/'build-manifest.json',{'stage':'world-game','video_profile':mode,'tools':versions,
        'program_sha256':digest(program),'program_bytes':len(program),'entry':'$6000',
        'loaded_end_exclusive':'$%04X'%(end_page*256),'resources':resource_report,
        'atlas_bytes':len(atlas),'atlas_sha256':digest(atlas),
        'extra_sector':EXTRA_SECTOR,'extra_bytes':len(extra),'extra_sha256':digest(extra),
        'title_sector':title_sector,'title_bytes':len(title),'title_sha256':digest(title),
        'text_sector':TEXT_SECTOR,'text_bytes':len(text_assets),'text_sha256':digest(text_assets),
        'map_sector':MAP_SECTOR,'map_bytes':len(maps),'map_sha256':digest(maps),
        'ending_sector':END_SECTOR,'ending_bytes':len(endings),'ending_sha256':digest(endings),
        'checkpoint_sector':checkpoint.SECTOR,'checkpoint_bytes':len(checkpoint_module),
        'checkpoint_sha256':digest(checkpoint_module),
        'disks':{'laigle-dor.do':digest(disk)},
        'validation':'assembled/packaged; execution evidence recorded separately'})
    print('World port: %d application bytes; %d shared atlas bytes; one Disk II image'%(len(program),len(atlas)))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--video',choices=['dhgr','mono'],default='dhgr')
    main(parser.parse_args().video)
