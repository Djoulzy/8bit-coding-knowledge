import * as C from './core.js';
import {runWorkspaceTests} from './workspace-tests.js';
const results=[];
function assert(v,m){if(!v)throw Error(m);}
function equal(a,b,m){assert(JSON.stringify(a)===JSON.stringify(b),m);}
async function test(name,fn){try{const skip=await fn();results.push((skip?'SKIP ':'PASS ')+name+(skip?' · '+skip:''));}catch(e){results.push('FAIL '+name+': '+e.message);}document.getElementById('result').textContent=results.join('\n');}
await test('All 192 HGR rows, boundary offsets and screen holes',()=>{
  equal([0,1,7,8,63,64,127,128,191].map(C.rowOffset),[0,1024,7168,128,8064,40,8104,80,8144],'Apple row offsets');
  const used=new Set();for(let y=0;y<192;y++)for(let x=0;x<40;x++)used.add(C.rowOffset(y)+x);
  assert(used.size===7680&&Math.max(...used)===8183,'screen bytes versus holes');
});
await test('DHGR: every cell/color, cross-bank writes, high bits and holes preserved',()=>{
  const a=C.blank('dhgr');a.main.fill(128);a.aux.fill(128);
  for(let y=0;y<192;y++)for(let x=0;x<140;x++)C.writeCell(a,x,y,(x+y)%16);
  for(let y=0;y<192;y++)for(let x=0;x<140;x++)assert(C.readCell(a,x,y)===(x+y)%16,'palette at '+x+','+y);
  assert([...a.main,...a.aux].every(v=>v&128),'bit 7 preserved');
  assert(a.main[0x1fff]===128&&a.aux[0x1fff]===128,'holes');
  const b=C.blank('dhgr');C.writeCell(b,1,0,15);assert(b.aux[0]===112&&b.main[0]===1,'cell crosses AUX/MAIN');
  C.writeCell(b,0,0,3);assert(C.readCell(b,1,0)===15,'neighbor untouched');
});
await test('DHGR Mono: 560 dots, both banks, monochrome rendering and preserved reserved bits',()=>{
  const a=C.blank('dhgr-mono');a.main.fill(128);a.aux.fill(128);
  C.validateAsset(a);equal(C.dimensions(a),[560,192],'full monochrome dimensions');
  equal([6,7,13,14,559].map(x=>C.location(a,x,191)),[
    {bank:'aux',offset:8144,bit:6},{bank:'main',offset:8144,bit:0},
    {bank:'main',offset:8144,bit:6},{bank:'aux',offset:8145,bit:0},
    {bank:'main',offset:8183,bit:6}], 'independent AUX/MAIN boundary vectors');
  for(let y=0;y<192;y++)for(let x=0;x<560;x++)C.writeDot(a,x,y,(x+y)&1);
  for(let y=0;y<192;y++)for(let x=0;x<560;x++)assert(C.readDot(a,x,y)===((x+y)&1),'every monochrome point');
  for(const monitor of ['color','mono','palette']){
    const row=C.scanline(a,0,monitor);assert(row.length===560,'no horizontal halving');
    for(let x=0;x<560;x++)equal(row[x],C.RGB[x&1?15:0],'black/white without color artifacts');
  }
  assert([...a.main,...a.aux].every(v=>v&128),'high bits preserved');
  assert(a.main[8191]===128&&a.aux[8191]===128,'holes preserved');
  a.mixed=true;equal(C.dimensions(a),[560,160],'mixed monochrome dimensions');
  C.writeCell(a,7,0,0);assert(C.readCell(a,7,0)===0&&C.readDot(a,9,0)===1,'one dot per cell');
  let rejected=false;try{C.validateAsset({...a,aux:[]});}catch{rejected=true;}assert(rejected,'AUX required');
  rejected=false;try{C.importBinary(new Uint8Array(8192),'dhgr-mono');}catch{rejected=true;}assert(rejected,'both banks required on import');
});
await test('HGR artifact parity, neighbor white, byte-wide phase and boundary cells',()=>{
  const a=C.blank('color');C.writeCell(a,3,0,6);assert(a.main[0]===192&&a.main[1]===128,'blue split cell sets both byte phases');
  equal(C.scanline(a,0)[6],C.RGB[6],'even phase=1 is blue');
  C.writeCell(a,0,0,3);equal(C.scanline(a,0)[6],C.RGB[3],'shared byte phase changes neighbor');
  C.writeDot(a,7,0,1);equal(C.scanline(a,0)[6],C.RGB[15],'adjacent dots white across bytes');
  const phase=a.main[0]&128;C.writeDot(a,0,0,0);assert((a.main[0]&128)===phase,'dot edit preserves phase');
});
await test('LOWRES nibble order, interleaved rows and mixed-mode text preservation',()=>{
  const a=C.blank('lowres');a.main.fill(0xa0);C.writeCell(a,0,0,3);assert(a.main[0]===0xa3,'top nibble low');C.writeCell(a,0,1,12);assert(a.main[0]===0xc3,'bottom nibble high');
  a.mixed=true;equal(C.dimensions(a),[40,40],'mixed geometry');
  for(let y=0;y<40;y++)for(let x=0;x<40;x++)C.writeCell(a,x,y,(x+y)%16);
  for(let r=20;r<24;r++)for(let x=0;x<40;x++)assert(a.main[C.textOffset(r)+x]===0xa0,'text preserved');
});
await test('Raw import/export exactly preserves all bytes and both DHGR orders',()=>{
  for(const mode of ['mono','color','hgr','dhgr','dhgr-mono','lowres']){const count=C.dhgr({mode})?16384:mode==='lowres'?1024:8192;const raw=Uint8Array.from({length:count},(_,i)=>(i*41+(i>>8))&255);for(const order of ['main-aux','aux-main']){const a=C.importBinary(raw,mode,order);equal(Array.from(C.binary(a,'both',order)),Array.from(raw),mode+' byte round trip');}}
  let rejected=false;try{C.importBinary(new Uint8Array(8192),'dhgr');}catch{rejected=true;}assert(rejected,'incomplete DHGR rejected');
});
await test('Sprite masks, fine detail fallback, tile accent and JSON losslessness',()=>{
  const a={key:'test',kind:'sprite',mode:'dhgr',encoding:'actor',width:4,height:1,statuses:[[0,3,12,15]],colors:[2],accent:0};C.validateAsset(a);
  const {page,alpha}=C.spritePages(a);equal(alpha[0],[0,0,0,0,1,1,0,0,0,0,1,1,1,1,1,1],'half masks');assert(C.readCell(page,2,0)===C.SERIAL[12],'unfavorable hue retains fine mark');
  const t={...a,encoding:'tile',statuses:[[0,1,2,3]],accent:13};const p=C.spritePages(t).page;assert(C.readCell(p,3,0)===13,'accent');
  const project={schema:C.SCHEMA,assets:[a,t].map((a,i)=>({...a,key:'test/'+i}))};equal(C.validateProject(JSON.parse(JSON.stringify(project))),project,'project round trip');
});
await test('All 187 real game assets validate, render and round-trip',async()=>{
  const catalog=await (await fetch('/api/catalog')).json();if(!catalog.some(a=>a.key.startsWith('laigle/')))return 'L’Aigle d’Or adapter not enabled';assert(catalog.length===187,'catalog count');
  for(const item of catalog){const a=await (await fetch('/api/asset/'+item.key)).json();C.validateAsset(a);if(a.kind==='screen'){const copy=C.importBinary(C.binary(a),a.mode);equal(copy.main,a.main,'main bank '+a.key);if(a.mode==='dhgr')equal(copy.aux,a.aux,'aux bank '+a.key);}else {const p=C.spritePages(a);assert(p.alpha.length===a.height,'sprite '+a.key);for(let y=0;y<a.height;y++)assert(C.scanline(p.page,y).length===(a.mode==='dhgr'?560:280),'render '+a.key);}}
});
await test('Invalid projects and unsupported masks rejected',()=>{
  const a=C.blank('dhgr');for(const p of [{schema:'unknown',assets:[]},{schema:C.SCHEMA,assets:[a,a]},{schema:C.SCHEMA,assets:[{...a,main:[0]}]}]){let fail=false;try{C.validateProject(p);}catch{fail=true;}assert(fail,'bad project accepted');}
});
await test('Preview RGB matches 56 independent Python port-converter vectors',async()=>{
  const catalog=await (await fetch('/api/catalog')).json();if(!catalog.some(a=>a.key.startsWith('laigle/')))return 'L’Aigle d’Or adapter not enabled';
  const vectors=await (await fetch('/preview-vectors.json')).json(),cache=new Map();
  for(const v of vectors.checks){if(!cache.has(v.key))cache.set(v.key,await (await fetch('/api/asset/'+v.key)).json());const bytes=new Uint8Array(C.scanline(cache.get(v.key),v.y,v.monitor).flat());const hash=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes)),n=>n.toString(16).padStart(2,'0')).join('');assert(hash===v.sha256,v.key+' row '+v.y+' '+v.monitor);}
});
await runWorkspaceTests(test,assert,equal);
document.title=results.some(s=>s.startsWith('FAIL'))?'FAIL · Apple IIe tests':'PASS · Apple IIe tests';
document.getElementById('result').textContent+='\n\n'+results.filter(s=>s.startsWith('PASS')).length+' passed; '+results.filter(s=>s.startsWith('SKIP')).length+' optional groups skipped; '+results.filter(s=>s.startsWith('FAIL')).length+' failed';
