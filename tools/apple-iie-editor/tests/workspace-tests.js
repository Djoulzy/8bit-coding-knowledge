import * as C from './core.js';
import * as W from './workspace.js';

export async function runWorkspaceTests(test, assert, equal) {
  function sample() {
    const a = C.blank('dhgr');
    a.name = 'Generic test pattern';
    for (let y=0; y<192; y++) for (let x=0; x<140; x++) C.writeCell(a,x,y,1+((x>>3)+(y>>3))%15);
    a.main[8191]=0xc7; a.aux[8191]=0x9b;
    return a;
  }

  await test('Mode changes convert the current document and restore every source byte', () => {
    const a=sample(), d=W.createDocument(a), id=d.id;
    for (const mode of ['lowres','mono','color','dhgr-mono','dhgr']) {
      W.switchMode(d,mode);
      assert(d.id===id && d.asset.mode===mode,'same document, requested mode');
      assert(d.asset.main.some(Boolean),'conversion contains the drawing');
    }
    equal(d.asset,a,'DHGR exact recovery, including holes and high bits');
    equal(d.sources[0].asset,a,'immutable original');
  });

  await test('No cumulative quantization: intermediate LOWRES never becomes the source', () => {
    const a=sample(), direct=W.createDocument(a), viaLow=W.createDocument(a);
    W.switchMode(direct,'color');
    W.switchMode(viaLow,'lowres'); W.switchMode(viaLow,'mono'); W.switchMode(viaLow,'color');
    equal(direct.asset.main,viaLow.asset.main,'same target generated from same source');
  });

  await test('HGR → edited DHGR → HGR preserves untouched strokes and native bytes', () => {
    const original=C.blank('color');original.name='Fine HGR strokes';
    for(let y=8;y<32;y++)for(let x=4;x<40;x++)C.writeCell(original,x,y,C.HGR_COLORS[2+(x%4)]);
    original.main[8191]=0xdb;
    const d=W.createDocument(original),id=d.id;
    W.switchMode(d,'dhgr');
    for(let y=100;y<104;y++)for(let x=100;x<110;x++)C.writeCell(d.asset,x,y,15);
    const edited=C.clone(d.asset);
    W.switchMode(d,'color');
    const touched=new Set();for(let y=100;y<104;y++)for(let x=0;x<40;x++)touched.add(C.rowOffset(y)+x);
    for(let i=0;i<8192;i++)if(!touched.has(i))assert(d.asset.main[i]===original.main[i],'untouched byte '+C.hex(i,4));
    assert(d.id===id && C.readCell(d.asset,104,101)===15,'DHGR retouch is visible in the same HGR document');
    const restored=W.load(JSON.parse(JSON.stringify(W.serialize([d]))))[0];
    equal(restored.asset.main,d.asset.main,'saved HGR preserves original strokes and new edit');
    W.switchMode(restored,'dhgr');equal(restored.asset,edited,'DHGR edit remains exact');
    W.switchMode(restored,'mono');
    const untouched=W.convert({type:'native',asset:original},'mono');
    for(let y=8;y<32;y++)for(let x=0;x<40;x++)assert(restored.asset.main[C.rowOffset(y)+x]===untouched.main[C.rowOffset(y)+x],'new mode derives untouched areas from original');
  });

  await test('Local erasure and later color edits propagate without flattening fine detail', () => {
    const a=C.blank('color');
    for(let y=10;y<16;y++)for(let x=0;x<20;x+=2)C.writeCell(a,x,y,3);
    for(let y=80;y<84;y++)for(let x=84;x<88;x++)C.writeCell(a,x,y,15);
    const d=W.createDocument(a);
    W.switchMode(d,'lowres');assert(C.readCell(d.asset,24,20)!==0,'erasable patch visible');
    C.writeCell(d.asset,24,20,0);W.switchMode(d,'dhgr');
    C.writeCell(d.asset,100,130,6);W.switchMode(d,'color');
    assert(C.readCell(d.asset,85,81)===0,'LOWRES eraser propagated');
    assert(C.readCell(d.asset,100,130)===6,'new blue retouch uses the correct HGR phase');
    for(let y=10;y<16;y++)for(let x=0;x<40;x++)assert(d.asset.main[C.rowOffset(y)+x]===a.main[C.rowOffset(y)+x],'fine purple strokes retained');
    const final=C.clone(d.asset),restored=W.load(JSON.parse(JSON.stringify(W.serialize([d]))))[0];
    W.switchMode(restored,'dhgr-mono');W.switchMode(restored,'color');
    equal(restored.asset,final,'erase and color edits stable after reload and further conversion');
    // Force replay, rather than relying on the saved HGR view cache.
    delete restored.variants.color;W.switchMode(restored,'dhgr');W.switchMode(restored,'color');
    equal(restored.asset.main,final.main,'shared revision replay reproduces exact HGR drawing');
  });

  await test('Mixed-mode display changes preserve hidden rows through other modes', () => {
    const a=C.blank('dhgr');C.writeCell(a,20,180,15);a.main[8191]=0xb7;
    const d=W.createDocument(a);d.asset.mixed=true;W.switchMode(d,'color');
    assert(d.asset.mixed,'mixed view propagated');
    d.asset.mixed=false;W.switchMode(d,'dhgr');
    assert(!d.asset.mixed&&C.readCell(d.asset,20,180)===15,'unshown row retained');
    equal(d.asset.main,a.main,'reserved bytes and MAIN unchanged');equal(d.asset.aux,a.aux,'AUX unchanged');
  });

  await test('Merged HGR choice preserves legacy identifiers, phase bits and screen holes', () => {
    const a=C.blank('hgr');a.main=a.main.map((_,i)=>(i*73+131)&255);
    const d=W.load({schema:C.SCHEMA,assets:[a]})[0],before=W.snapshot(d);
    W.switchMode(d,'color');equal(W.snapshot(d),before,'selecting the HGR alias is a no-op');
    W.switchMode(d,'lowres');W.switchMode(d,'color');
    equal(d.asset,a,'HGR native bytes and key restored without requantization');
    const restored=W.load(JSON.parse(JSON.stringify(W.serialize([d]))))[0];
    equal(restored.asset,a,'legacy HGR workspace still opens and saves exactly');
    const converted=W.convert({type:'native',asset:a},'color');
    equal(converted.main,a.main,'direct alias conversion preserves all 8192 bytes');
    assert(converted.mode==='color','explicit conversion has requested identifier');
    const color=W.createDocument(converted),colorBefore=W.snapshot(color);
    W.switchMode(color,'hgr');equal(W.snapshot(color),colorBefore,'reverse legacy alias is also a no-op');
    assert(!Object.hasOwn(color.variants,'hgr'),'no redundant variant created');
  });

  await test('Retouches propagate automatically to previously visited modes', () => {
    const original=C.blank('dhgr'),d=W.createDocument(original);
    W.switchMode(d,'mono'); W.switchMode(d,'lowres');
    // Deliberately replace the whole view to make stale cached images obvious.
    for(let y=0;y<48;y++)for(let x=0;x<40;x++)C.writeCell(d.asset,x,y,15);
    const edited=C.clone(d.asset);
    W.switchMode(d,'mono');
    equal(d.asset.main,W.convert({type:'native',asset:edited},'mono').main,'visited Mono uses new drawing');
    W.switchMode(d,'dhgr');
    const expected=W.convert({type:'native',asset:edited},'dhgr');
    equal(d.asset.main,expected.main,'visited DHGR MAIN uses new drawing');
    equal(d.asset.aux,expected.aux,'visited DHGR AUX uses new drawing');
    equal(d.sources[0].asset,original,'original bytes preserved');
    W.switchMode(d,'lowres');equal(d.asset,edited,'editing mode retains exact bytes');
  });

  await test('Saving and native exports synchronize edits without changing live history', () => {
    const original=sample(),d=W.createDocument(original);
    W.switchMode(d,'lowres'); C.writeCell(d.asset,0,0,9); C.writeCell(d.asset,39,47,6);
    const edited=C.clone(d.asset),before=W.snapshot(d),p=W.serialize([d]);
    equal(W.snapshot(d),before,'serialization has no side effects');
    const restored=W.load(JSON.parse(JSON.stringify(p)))[0];
    W.switchMode(restored,'dhgr');
    const converted=W.convert({type:'native',asset:edited},'dhgr'),expected=C.clone(original);
    // One LOWRES cell affects four DHGR rows and up to four color cells.
    for(const [left,top] of [[0,0],[136,188]])for(let y=top;y<top+4;y++)for(let x=left;x<left+4;x++)C.writeCell(expected,x,y,C.readCell(converted,x,y));
    equal(restored.asset.main,expected.main,'saved retouches shared without reducing untouched detail');
    equal(restored.asset.aux,expected.aux,'saved AUX matches');
    const native=W.exportNativeAssets([d]).assets.find(a=>a.mode==='dhgr');
    equal(native.main,expected.main,'native export cannot contain stale visited modes');
    equal(native.aux,expected.aux,'native AUX export refreshed');
  });

  await test('First conversion uses latest drawing while preserving pre-edit original', () => {
    const a=C.blank('dhgr'),d=W.createDocument(a);
    C.writeCell(d.asset,20,20,15);
    W.switchMode(d,'mono');
    assert(d.asset.main.some(Boolean),'edits are part of first reference');
    equal(d.sources[0].asset,a,'original still blank');
  });

  await test('Automatic revision archives restore detail before a lower-resolution edit', () => {
    const original=sample(),d=W.createDocument(original);
    W.switchMode(d,'lowres'); const before=W.snapshot(d);
    C.writeCell(d.asset,0,0,15); const low=C.clone(d.asset);
    W.switchMode(d,'dhgr');
    assert(d.archives.length===1,'edit archived automatically');
    W.restoreArchive(d,0);
    equal(d.asset,before.asset,'previous view restored, without later retouch');
    W.switchMode(d,'dhgr');equal(d.asset,original,'original fine detail and memory bytes restored');
    W.restoreArchive(d,1);W.switchMode(d,'lowres');
    equal(d.asset,low,'new revision also recoverable');
    W.validateDocument(d);
  });

  await test('Legacy independent modes are archived and linked to the visible drawing', () => {
    const original=sample(),d=W.createDocument(original);
    W.switchMode(d,'lowres'); C.writeCell(d.asset,0,0,15);
    delete d.linkedModes; const visible=C.clone(d.asset),oldVariants=C.clone(d.variants);
    const restored=W.load(JSON.parse(JSON.stringify({schema:W.SCHEMA,documents:[d]})))[0];
    assert(restored.linkedModes,'legacy workspace migrated');
    const archive=restored.archives[0];
    equal(archive.variants.dhgr,oldVariants.dhgr,'independent legacy DHGR preserved');
    equal(archive.variants.lowres,visible,'visible legacy retouches preserved');
    W.switchMode(restored,'dhgr');
    assert(C.readCell(restored.asset,0,0)===15,'legacy visible retouch propagates');
    for(let y=20;y<192;y++)for(let x=0;x<40;x++){const p=C.rowOffset(y)+x;assert(restored.asset.main[p]===original.main[p]&&restored.asset.aux[p]===original.aux[p],'legacy untouched detail retained');}
    W.restoreArchive(restored,1);equal(restored.asset,original,'other legacy drawing recoverable through version selector');
    W.restoreArchive(restored,0);W.switchMode(restored,'mono');
    assert(C.readDot(restored.asset,0,0)===1,'restoring legacy archive also links modes');
  });

  await test('Replacing an image preserves originals and uses the new shared source', () => {
    const original=sample(),d=W.createDocument(original),replacement=C.blank('lowres');
    C.writeCell(replacement,20,20,15);
    W.replaceSource(d,replacement);
    W.switchMode(d,'dhgr');
    equal(d.asset.main,W.convert({type:'native',asset:replacement},'dhgr').main,'replacement drives conversion');
    W.restoreArchive(d,0);equal(d.asset,original,'pre-import document retained');
    equal(d.sources[0].asset,original,'original source retained');
  });

  await test('Imported RGBA and original file bytes survive every conversion', () => {
    const rgba=Uint8Array.from({length:17*13*4},(_,i)=>(i*43)&255);
    const file={name:'original.png',mime:'image/png',data:W.encodeBytes(new Uint8Array([0,128,255,1]))};
    const source=W.rasterSource(17,13,rgba,file),d=W.createDocument(W.convert(source,'mono'),source);
    for(const mode of W.MODES)W.switchMode(d,mode);
    const restored=W.load(JSON.parse(JSON.stringify(W.serialize([d]))))[0];
    equal(Array.from(W.decodeBytes(restored.sources[0].rgba)),Array.from(rgba),'all source channels including alpha');
    equal(restored.sources[0].file,file,'exact original file');
  });

  await test('Adapter compiler files reopen their complete workspace and edits', () => {
    const a=C.blank('mono'),d=W.createDocument(a);
    C.writeDot(d.asset,20,30,1);
    const workspace=W.serialize([d]);
    const saved={...W.exportNativeAssets([d]),workspace};
    const restored=W.load(JSON.parse(JSON.stringify(saved)))[0];
    equal(W.serialize([restored]),workspace,'sources, variants and history retained');
    assert(C.readDot(restored.asset,20,30)===1,'latest retouch reopened');
    let rejected=false;
    try{W.load({...saved,workspace:{schema:C.SCHEMA,assets:[]}});}catch{rejected=true;}
    assert(rejected,'nested native wrapper rejected');
  });

  await test('Native sprite masks and ABI survive conversion to another mode', () => {
    const a={key:'adapter/sprite/1',name:'Sprite',kind:'sprite',mode:'dhgr',encoding:'actor',width:3,height:2,
      statuses:[[0,3,12],[15,5,10]],colors:[13,12],accent:0};
    const d=W.createDocument(a); W.switchMode(d,'lowres');
    assert(d.asset.kind==='screen','other mode is a derived native screen');
    W.switchMode(d,'dhgr');equal(d.asset,a,'native sprite restored exactly');
    equal(W.exportNativeAssets([d]).assets.find(a=>a.key==='adapter/sprite/1'),a,'adapter receives original ABI');
    W.switchMode(d,'lowres');C.writeCell(d.asset,0,0,15);
    const p=W.serialize([d]);
    equal(W.serialize([d]),p,'saving a converted sprite has stable keys');
    W.validateDocument(p.documents[0]);
    assert(p.documents[0].variants.dhgr.kind==='screen','retouched screen is shared across modes');
    assert(p.documents[0].variants.dhgr.key.startsWith('custom/'),'derived screen does not overwrite native sprite ABI');
  });

  await test('Renaming an imported image does not lower its reference resolution', () => {
    const source=W.rasterSource(19,11,new Uint8Array(19*11*4).fill(255));
    const d=W.createDocument(W.convert(source,'lowres'),source);
    d.name='Renamed';d.asset.name=d.name;
    W.switchMode(d,'dhgr');
    assert(d.sources.length===1 && d.reference===0,'rename keeps original RGBA reference');
    equal(d.asset.main,W.convert(source,'dhgr').main,'full original drives renamed conversion');
  });

  await test('DHGR Mono participates in shared conversion, edits and workspace round trips', () => {
    const a=C.blank('dhgr-mono');a.main[8191]=0xc7;a.aux[8191]=0x9b;
    for(let y=0;y<192;y++)for(let x=0;x<560;x++)C.writeDot(a,x,y,(x>>4)&1);
    const d=W.createDocument(a);
    for(const mode of W.MODES)W.switchMode(d,mode);
    W.switchMode(d,'dhgr-mono');equal(d.asset,a,'raw monochrome original recovered exactly');
    W.switchMode(d,'lowres');
    for(let y=0;y<48;y++)for(let x=0;x<40;x++)C.writeCell(d.asset,x,y,15);
    W.switchMode(d,'dhgr-mono');
    assert(C.readDot(d.asset,0,0)===1&&C.readDot(d.asset,559,191)===1,'LOWRES edit reaches all 560 columns');
    C.writeDot(d.asset,100,100,0);
    const restored=W.load(JSON.parse(JSON.stringify(W.serialize([d]))))[0];
    assert(restored.asset.mode==='dhgr-mono'&&C.readDot(restored.asset,100,100)===0,'monochrome edit saved');
    equal(restored.sources[0].asset,a,'all original MAIN/AUX bytes retained');
    const native=W.exportNativeAssets([restored]).assets.find(a=>a.mode==='dhgr-mono');
    assert(C.binary(native).length===16384,'native export retains both banks');
  });

  await test('Undo snapshots include conversion state without recursive undo stacks', () => {
    const d=W.createDocument(sample());d.undo=[];d.redo=[];
    const before=W.snapshot(d);d.undo.push(before);W.switchMode(d,'lowres');
    const after=W.snapshot(d);Object.assign(d,before);
    assert(d.asset.mode==='dhgr' && !Object.hasOwn(after,'undo'),'undo restored entire document');
    Object.assign(d,after);assert(d.asset.mode==='lowres','redo restored conversion');
  });

  await test('Legacy projects migrate; invalid workspace references are rejected', () => {
    const a=sample(),d=W.load({schema:C.SCHEMA,assets:[a]})[0];equal(d.asset,a,'v1 import');
    for(const bad of [{...d,reference:999},{...d,linkedModes:'yes'},{...d,variants:{mono:a}},{...d,sources:[{type:'rgba',width:2,height:2,rgba:'AAAA'}]}]) {
      let failed=false;try{W.validateDocument(bad);}catch{failed=true;}assert(failed,'invalid document accepted');
    }
    const edit={type:'edit',base:0,before:a,after:C.clone(a)};
    W.validateDocument({...d,sources:[...d.sources,edit],reference:1});
    for(const bad of [{...edit,base:1},{...edit,base:-1},{...edit,after:C.blank('mono')}]) {
      let failed=false;try{W.validateDocument({...d,sources:[...d.sources,bad],reference:1});}catch{failed=true;}
      assert(failed,'cyclic or incompatible edit accepted');
    }
  });
}
