import * as C from './core.js';
import * as W from './workspace.js';
const $=id=>document.getElementById(id), canvas=$('canvas'),ctx=canvas.getContext('2d'),preview=$('preview');
const state={docs:[],index:0,catalog:[],tool:'pencil',color:15,unit:'cell',monitor:'color',status:15,last:null,stroke:null,dirty:false};
let localProject=null;
const current=()=>state.docs[state.index];
const asset=()=>current().asset;
const msg=(s,error=false)=>{$('message').textContent=s;$('message').classList.toggle('error',error);};
const guard=fn=>async(...args)=>{try{await fn(...args);}catch(e){msg(e.message,true);}};
function add(a, source=null) {
  C.validateAsset(a);
  const found=state.docs.findIndex(d=>d.asset.key===a.key);
  if(found>=0){state.index=found;refresh();return;}
  state.docs.push({...W.createDocument(a,source),undo:[],redo:[],edited:false});state.index=state.docs.length-1;state.status=a.mode==='dhgr'&&a.encoding==='actor'?15:2;state.last=null;refresh();
}
function updateSaveState(){state.dirty=state.docs.some(d=>d.edited);$('save-state').textContent=state.dirty?'Modifications non enregistrées':'Aucune modification en attente';}
function changed() {current().edited=true;updateSaveState();autosave();renderTabs();}
let saveTimer;
function persistRecovery(){clearTimeout(saveTimer);try{localStorage.setItem('a2-atelier-recovery',JSON.stringify({...project(),unsavedDocumentIds:state.docs.filter(d=>d.edited).map(d=>d.id)}));}catch{msg('Stockage navigateur plein. Enregistrez votre projet JSON pour conserver vos retouches.',true);}}
function autosave() {clearTimeout(saveTimer);saveTimer=setTimeout(persistRecovery,500);}
function project(){return W.serialize(state.docs);}
function checkpoint(){const d=current();d.undo.push(W.snapshot(d));if(d.undo.length>60)d.undo.shift();d.redo=[];}
function history(redo=false){const d=current(),from=redo?d.redo:d.undo,to=redo?d.undo:d.redo;if(!from.length)return;to.push(W.snapshot(d));Object.assign(d,from.pop());changed();refresh();}
function renderTabs(){
  const box=$('tabs');box.replaceChildren();
  state.docs.forEach((d,i)=>{
    const tab=document.createElement('div');tab.className='document-tab';tab.classList.toggle('active',i===state.index);
    const b=document.createElement('button');b.textContent=(d.edited?'• ':'')+(d.asset.name||d.asset.key);
    b.setAttribute('aria-pressed',String(i===state.index));b.onclick=()=>{state.index=i;state.last=null;refresh();};
    const close=document.createElement('button');close.className='close-tab';close.textContent='×';
    close.title='Fermer '+(d.name||'ce document');close.setAttribute('aria-label',close.title);
    close.onclick=()=>requestClose(d.id);tab.append(b,close);box.append(tab);
  });
  $('undo').disabled=!current().undo.length;$('redo').disabled=!current().redo.length;
}
let closingDocumentId=null,closeSaving=false;
function requestClose(id){
  const d=state.docs.find(d=>d.id===id);if(!d)return;
  if(!d.edited){closeDocument(id);return;}
  closingDocumentId=id;$('close-document-name').textContent='« '+d.name+' » contient des modifications non enregistrées.';
  $('close-document-error').textContent='';$('close-document-dialog').showModal();
}
function closeDocument(id){
  const index=state.docs.findIndex(d=>d.id===id);if(index<0)return;
  const activeId=current().id,mode=state.docs[index].asset.mode;
  state.docs.splice(index,1);state.last=null;state.stroke=null;
  if(!state.docs.length){add(C.blank(mode));}
  else {const active=state.docs.findIndex(d=>d.id===activeId);state.index=active<0?Math.min(index,state.docs.length-1):active;refresh();}
  updateSaveState();msg('Document fermé.');persistRecovery();
}
$('close-cancel').onclick=()=>$('close-document-dialog').close();
$('close-discard').onclick=()=>{closeDocument(closingDocumentId);$('close-document-dialog').close();};
$('close-save').onclick=async()=>{
  const d=state.docs.find(d=>d.id===closingDocumentId);if(!d)return;
  closeSaving=true;for(const id of ['close-save','close-discard','close-cancel'])$(id).disabled=true;
  try{await saveDocuments([d],filename(d.asset)+'-workspace.json',!!localProject);closeDocument(d.id);$('close-document-dialog').close();}
  catch(e){if(e.name!=='AbortError')$('close-document-error').textContent='Enregistrement impossible : '+e.message;}
  finally{closeSaving=false;for(const id of ['close-save','close-discard','close-cancel'])$(id).disabled=false;}
};
$('close-document-dialog').addEventListener('cancel',e=>{if(closeSaving)e.preventDefault();});
$('close-document-dialog').addEventListener('close',()=>{closingDocumentId=null;});
function catalog() {
  const query=$('search').value.toLowerCase(), own=$('library-filter').value==='workspace';
  const items=(own?state.docs.map(d=>({key:d.id,name:d.name,kind:d.asset.kind,mode:d.asset.mode})):state.catalog)
    .filter(a=>(a.name+' '+a.key).toLowerCase().includes(query));
  const box=$('catalog');box.replaceChildren();$('asset-count').textContent=items.length;
  for(const a of items){
    const b=document.createElement('button');b.className='asset-item';
    b.classList.toggle('active',own?a.key===current().id:a.key===asset().key);
    const strong=document.createElement('strong');strong.textContent=a.name;
    const small=document.createElement('small');small.textContent=W.modeLabel(a.mode)+' / '+(a.kind==='sprite'?'SPRITE':'ÉCRAN');
    b.append(strong,small);
    b.onclick=guard(async()=>{
      if(own){state.index=state.docs.findIndex(d=>d.id===a.key);state.last=null;refresh();return;}
      const response=await fetch('/api/asset/'+a.key),data=await response.json();
      if(!response.ok)throw Error(data.error);add(data);msg('Ressource chargée depuis la bibliothèque optionnelle.');
    });box.append(b);
  }
}

function palette(){const a=asset(),colors=(C.monochrome(a)||state.unit==='dot'&&a.kind==='screen'&&a.mode!=='lowres')?[0,15]:C.hgr(a)?C.HGR_COLORS:C.RGB.map((_,i)=>i);if(!colors.includes(state.color))state.color=15;const box=$('palette');box.replaceChildren();colors.forEach(i=>{const b=document.createElement('button');b.className='swatch';b.style.background=`rgb(${C.RGB[i]})`;b.title=C.NAMES[i]+' '+C.hex(i);b.setAttribute('aria-label',b.title);b.classList.toggle('active',state.color===i);b.onclick=()=>{state.color=i;palette();};box.append(b);});$('color-chip').style.background=`rgb(${C.RGB[state.color]})`;$('color-name').textContent=C.NAMES[state.color]+' '+C.hex(state.color);}
function unit(){return asset().kind==='sprite'?'cell':C.monochrome(asset())?'dot':asset().mode==='lowres'?'cell':state.unit;}
function refresh(){const a=asset(),sprite=a.kind==='sprite';$('asset-name').textContent=a.name||'Sans titre';$('asset-subtitle').textContent=sprite?`Atlas ${a.source?.atlas_id??'personnalisé'} · ${a.width} × ${a.height} · ${a.mode==='dhgr'?(a.encoding==='tile'?'décor à 2 bits':'masques fins à 4 bits'):'pixels et masque séparé'}`:'Document multiformat · source préservée · export mémoire Apple II';$('mode').value=W.editorMode(a.mode);$('replace-screen').disabled=sprite;if(sprite)$('replace-screen').checked=false;$('mixed').checked=!!a.mixed;$('mixed').disabled=sprite||!!a.source?.program;$('unit').value=unit();$('unit').disabled=sprite||a.mode==='lowres'||C.monochrome(a);$('sprite-controls').hidden=!sprite;$('phase-controls').hidden=!C.hgr(a);$('export-native').disabled=sprite;$('export-main').disabled=sprite;$('export-aux').disabled=sprite||!C.dhgr(a);$('bank-order').disabled=!C.dhgr(a);$('page').disabled=sprite;$('accent-label').hidden=!(sprite&&a.encoding==='tile');$('force-label').hidden=!(sprite&&a.encoding==='tile');$('force-black').checked=!!a.force_black;$('accent').value=a.accent||0;$('row-color').disabled=a.mode!=='dhgr';
  const statuses=sprite?(a.mode==='dhgr'?(a.encoding==='tile'?[0,1,2,3]:C.STATUS):[0,1,2]):[];
  if(sprite&&!statuses.includes(state.status))state.status=a.mode==='dhgr'&&a.encoding==='actor'?15:2;
  $('status').replaceChildren(...statuses.map(v=>{const o=document.createElement('option');o.value=v;o.textContent=a.mode!=='dhgr'||a.encoding==='tile'?['Transparent','Noir opaque','Couleur principale','Accent'][v]:({0:'Transparent',1:'Noir gauche / transparent droite',3:'Couleur gauche / transparent droite',4:'Transparent gauche / noir droite',5:'Noir opaque',7:'Couleur gauche / noir droite',10:'Couleur pleine · marqueur historique',12:'Transparent gauche / couleur droite',13:'Noir gauche / couleur droite',15:'Couleur pleine'}[v]);return o;}));$('status').value=state.status;
  $('constraint').textContent=sprite?(a.mode==='dhgr'?`Format natif : ${a.encoding==='tile'?'transparent, noir, couleur de ligne et accent commun.':'opacité de chaque demi-cellule et couleur par ligne.'} Le damier représente la transparence. La gomme rend la cellule transparente.`:'Sprite HGR : pixels, masque opaque et phase commune. La gomme restaure la transparence.'):a.mode==='dhgr-mono'?'DHGR Mono : 560 × 192 points (160 lignes en mode mixte), noir et blanc. 7 bits AUX puis 7 bits MAIN ; bit 7 conservé et non affiché.':a.mode==='dhgr'?'DHGR couleur : 140 cellules couleur / 560 points série. Chaque cellule utilise 4 bits, parfois répartis entre AUX et MAIN. Le bit 7 des octets est conservé mais ne représente pas un point.':a.mode==='lowres'?'LOWRES : 40 × 48 cellules, 16 couleurs. Deux lignes verticales partagent un octet : nibble bas en haut, nibble haut en bas. Le mode mixte conserve les 4 lignes texte.':a.mode==='mono'?'HGR Mono : 280 points. Les 7 bits bas forment les pixels ; le bit 7 de phase est préservé.':'HGR couleur : la couleur dépend de la parité des points et du bit 7, commun à 7 points. Peindre une couleur peut modifier la teinte des points voisins du même octet.';
  renderTabs();catalog();palette();render();referenceInfo();setTool(state.tool);inspect(state.last);
}
function bitmap(){const a=asset(),sprite=a.kind==='sprite';const [width,height]=sprite?[a.width*(a.mode==='dhgr'?4:1),a.height]:[a.mode==='lowres'?40:C.dhgr(a)?560:280,C.dimensions(a)[1]];const {page,alpha}=sprite?C.spritePages(a):{page:a,alpha:null};const out=document.createElement('canvas');out.width=width;out.height=height;const c=out.getContext('2d'),data=c.createImageData(width,height);for(let y=0;y<height;y++){const extra=sprite&&y>=192?C.spritePages(a,y,1):null;const row=C.scanline(extra?extra.page:page,extra?0:y,state.monitor);for(let x=0;x<width;x++){let rgb=row[x];if(alpha&&!(extra?extra.alpha[0][x]:alpha[y][x]))rgb=((Math.floor(x/(a.mode==='dhgr'?8:2))+Math.floor(y/2))&1)?[46,55,59]:[31,38,42];const p=(y*width+x)*4;data.data.set([...rgb,255],p);}}c.putImageData(data,0,0);return out;}
function render(){const a=asset(),bmp=bitmap(),sprite=a.kind==='sprite',logical=C.dimensions(a,unit());const baseW=sprite?bmp.width*(a.mode==='dhgr'?1:2):560,baseH=sprite?bmp.height*2:384*(a.mixed?5/6:1);const stage=$('stage'),fit=Math.min((stage.clientWidth-26)/baseW,(stage.clientHeight-26)/baseH);const zoom=$('zoom').value==='fit'?Math.min(sprite?6:2,fit):Number($('zoom').value);canvas.width=Math.max(1,Math.round(baseW*zoom));canvas.height=Math.max(1,Math.round(baseH*zoom));canvas.style.width=canvas.width+'px';canvas.style.height=canvas.height+'px';ctx.imageSmoothingEnabled=false;ctx.drawImage(bmp,0,0,canvas.width,canvas.height);if($('grid').checked&&canvas.width/logical[0]>=4){ctx.strokeStyle='#a3b9c04a';ctx.lineWidth=.5;ctx.beginPath();for(let x=0;x<=logical[0];x++){const px=x*canvas.width/logical[0];ctx.moveTo(px,0);ctx.lineTo(px,canvas.height);}for(let y=0;y<=logical[1];y++){const py=y*canvas.height/logical[1];ctx.moveTo(0,py);ctx.lineTo(canvas.width,py);}ctx.stroke();}preview.width=280;preview.height=Math.max(1,Math.round(280*baseH/baseW));const pc=preview.getContext('2d');pc.imageSmoothingEnabled=false;pc.drawImage(bmp,0,0,preview.width,preview.height);$('dimensions').textContent=`${logical[0]} × ${logical[1]} ${sprite?'cellules':unit()==='dot'?'points':'cellules'} · ${Math.round(zoom*100)} %`;}
function coords(e){const r=canvas.getBoundingClientRect(),[w,h]=C.dimensions(asset(),unit());return {x:Math.max(0,Math.min(w-1,Math.floor((e.clientX-r.left)*w/r.width))),y:Math.max(0,Math.min(h-1,Math.floor((e.clientY-r.top)*h/r.height)))};}
function inspect(p){const a=asset();if(!p){$('memory-info').textContent=a.kind==='sprite'?'Atlas compact : pas une page écran.\nExport via le projet JSON.':C.dhgr(a)?'MAIN : 8 192 octets\nAUX  : 8 192 octets\nSérie vidéo : AUX → MAIN':`MAIN : ${a.main.length.toLocaleString('fr-FR')} octets\nAdressage entrelacé Apple II`;$('cursor-info').textContent='Survolez le visuel pour inspecter sa mémoire.';return;}const {x,y}=p;const [w,h]=C.dimensions(a,unit());if(x>=w||y>=h){state.last=null;inspect(null);return;}if(a.kind==='sprite'){$('cursor-info').textContent=`x ${x} / y ${y} · valeur ${C.hex(C.readCell(a,x,y))}`;$('memory-info').textContent=a.mode==='dhgr'?`Statut : ${C.hex(a.statuses[y][x])}\nCouleur de ligne : ${C.hex(a.colors[y])}\nLargeur : ${a.width} cellules`:`Pixel : ${a.pixels[y][x]} · masque : ${a.masks[y][x]}\nPhase : ${C.hex(a.phase||0)}`;return;}const loc=C.location(a,x,y,unit()),base=a.mode==='lowres'?($('page').value==='1'?0x400:0x800):($('page').value==='1'?0x2000:0x4000),value=a[loc.bank][loc.offset];$('cursor-info').textContent=`x ${x} / y ${y} · ${loc.bank.toUpperCase()} ${C.hex(base+loc.offset,4)} · bit ${loc.bit}`;$('memory-info').textContent=`${loc.bank.toUpperCase()} ${C.hex(base+loc.offset,4)} = ${C.hex(value)}\nBits : ${value.toString(2).padStart(8,'0')}\nOffset : ${C.hex(loc.offset,4)}\n${a.mode==='dhgr-mono'?'Point : 1 bit, AUX/MAIN entrelacés':a.mode==='dhgr'?'Cellule : 4 bits, AUX/MAIN entrelacés':a.mode==='lowres'?'Nibble '+(y&1?'haut':'bas'):'Phase bit 7 : '+(value>>7)}`;}
function paint(x,y,erase=false){const a=asset();if(a.kind==='sprite'){if(state.tool==='row-color'&&a.mode==='dhgr'){a.colors[y]=state.color;return;}const v=erase?0:state.status;if(a.mode==='dhgr')a.statuses[y][x]=v;else{a.pixels[y][x]=v===2?1:0;a.masks[y][x]=v?1:0;}return;}if(unit()==='dot')C.writeDot(a,x,y,!erase&&state.color!==0);else C.writeCell(a,x,y,erase?0:state.color);}
function read(x,y){const a=asset();return a.kind==='sprite'?C.readCell(a,x,y):unit()==='dot'?C.readDot(a,x,y):C.readCell(a,x,y);}
function line(p,q,fn){let x=p.x,y=p.y,dx=Math.abs(q.x-x),dy=-Math.abs(q.y-y),sx=x<q.x?1:-1,sy=y<q.y?1:-1,err=dx+dy;for(;;){fn(x,y);if(x===q.x&&y===q.y)break;const e=2*err;if(e>=dy){err+=dy;x+=sx;}if(e<=dx){err+=dx;y+=sy;}}}
function fill(p){const [w,h]=C.dimensions(asset(),unit()),old=read(p.x,p.y),original=Array.from({length:h},(_,y)=>Array.from({length:w},(_,x)=>read(x,y))),stack=[p],seen=new Uint8Array(w*h);while(stack.length){const {x,y}=stack.pop();if(x<0||y<0||x>=w||y>=h||seen[y*w+x]||original[y][x]!==old)continue;seen[y*w+x]=1;paint(x,y);stack.push({x:x-1,y},{x:x+1,y},{x,y:y-1},{x,y:y+1});}}
function setTool(t){state.tool=t;document.querySelectorAll('[data-tool]').forEach(b=>b.classList.toggle('active',b.dataset.tool===t));$('row-color').classList.toggle('active',t==='row-color');}
canvas.addEventListener('pointerdown',guard(e=>{if(e.button!==0)return;const p=coords(e);state.last=p;if(state.tool==='pick'){const a=asset();if(a.kind==='sprite'){state.status=read(p.x,p.y);if(a.mode==='dhgr')state.color=a.colors[p.y];$('status').value=state.status;}else state.color=unit()==='dot'?(read(p.x,p.y)?15:0):read(p.x,p.y);palette();inspect(p);return;}checkpoint();state.stroke={start:p,previous:p,before:C.clone(asset())};canvas.setPointerCapture(e.pointerId);if(state.tool==='fill'){fill(p);}else paint(p.x,p.y,state.tool==='erase');render();inspect(p);}));
canvas.addEventListener('pointermove',guard(e=>{const p=coords(e);state.last=p;if(state.stroke){if(['line','rect'].includes(state.tool)){current().asset=C.clone(state.stroke.before);const start=state.stroke.start;if(state.tool==='line')line(start,p,(x,y)=>paint(x,y));else{line(start,{x:p.x,y:start.y},paint);line({x:p.x,y:start.y},p,paint);line(p,{x:start.x,y:p.y},paint);line({x:start.x,y:p.y},start,paint);}}else if(state.tool!=='fill')line(state.stroke.previous,p,(x,y)=>paint(x,y,state.tool==='erase'));state.stroke.previous=p;render();}inspect(p);}));
function endStroke(){if(state.stroke){state.stroke=null;changed();render();}}
canvas.addEventListener('pointerup',endStroke);canvas.addEventListener('pointercancel',()=>{if(state.stroke){current().asset=state.stroke.before;current().undo.pop();state.stroke=null;refresh();}});canvas.addEventListener('lostpointercapture',endStroke);
document.querySelectorAll('[data-tool]').forEach(b=>b.onclick=()=>setTool(b.dataset.tool));$('row-color').onclick=()=>setTool('row-color');$('status').onchange=()=>state.status=Number($('status').value);
$('undo').onclick=()=>history();$('redo').onclick=()=>history(true);$('search').oninput=catalog;$('library-filter').onchange=catalog;
$('zoom').onchange=render;$('grid').onchange=render;$('monitor').onchange=()=>{state.monitor=$('monitor').value;render();};$('unit').onchange=()=>{state.unit=$('unit').value;state.last=null;palette();render();inspect(null);};$('page').onchange=()=>inspect(state.last);
$('mixed').onchange=()=>{checkpoint();asset().mixed=$('mixed').checked;state.last=null;changed();refresh();};
$('mode').onchange=guard(()=>{const mode=$('mode').value;if(mode===W.editorMode(asset().mode))return;checkpoint();W.switchMode(current(),mode);state.last=null;setTool('pencil');changed();refresh();msg('Rendu '+W.modeLabel(mode)+' du document courant. Les dernières retouches sont reprises automatiquement ; la source originale et les versions précédentes restent conservées.');});$('new-screen').onclick=()=>{const a=C.blank($('mode').value);a.name='Sans titre · '+W.modeLabel(a.mode);add(a);state.last=null;};
$('phase').onclick=()=>{const a=asset();if(a.kind!=='sprite'&&!state.last){msg('Survolez d’abord un octet du dessin.');return;}checkpoint();if(a.kind==='sprite')a.phase=(a.phase||0)^128;else{const p=C.location(a,state.last.x,state.last.y,unit());a.main[p.offset]^=128;}changed();render();inspect(state.last);};
for(let i=0;i<16;i++){const o=document.createElement('option');o.value=i;o.textContent=C.hex(i)+' '+C.NAMES[i];$('accent').append(o);}
$('accent').onchange=()=>{checkpoint();asset().accent=Number($('accent').value);changed();render();};$('force-black').onchange=()=>{checkpoint();asset().force_black=$('force-black').checked;changed();};
function download(data,name,mime){const blob=new Blob([data],{type:mime}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),10000);}
const filename=(a=asset())=> (a.name||'apple-iie').normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9_-]+/gi,'-').slice(0,90);
async function saveDocuments(docs,name,local=false,markSaved=true){
  const snapshots=docs.map(d=>JSON.stringify(W.serialize([d]))),data=W.serialize(docs);
  W.load(data);const json=JSON.stringify(data)+'\n';
  if(new Blob([json]).size>64*1024*1024)throw Error('Projet supérieur à 64 Mio. Exportez les documents séparément.');
  let saved;
  if(local){
    const response=await fetch('/api/project',{method:'POST',headers:{'Content-Type':'application/json'},body:json});
    saved=await response.json();if(!response.ok)throw Error(saved.error||'Enregistrement impossible');
    localProject={...localProject,...saved};$('open-local-project').hidden=false;
  }else if(window.showSaveFilePicker){
    const handle=await window.showSaveFilePicker({suggestedName:name,types:[{description:'Projet Apple IIe',accept:{'application/json':['.json']}}]});
    const writable=await handle.createWritable();
    try{await writable.write(json);await writable.close();}catch(e){try{await writable.abort();}catch{}throw e;}
  }else download(json,name,'application/json');
  if(markSaved)docs.forEach((d,i)=>{if(JSON.stringify(W.serialize([d]))===snapshots[i])d.edited=false;});
  updateSaveState();renderTabs();persistRecovery();
  msg(local?saved.message+(saved.mirrored?.length?' Les sprites de prototype mono sont aussi appliqués au jeu monochrome.':''):
    window.showSaveFilePicker?'Projet enregistré, sources et variantes conservées.':'Téléchargement du projet lancé. Conservez le fichier JSON pour reprendre vos retouches.');
}
$('save-project').onclick=guard(async()=>{try{await saveDocuments([...state.docs],'apple-iie-workspace.json',!!localProject);}catch(e){if(e.name!=='AbortError')throw e;}});
$('save-document').onclick=guard(async()=>{try{await saveDocuments([current()],filename()+'-workspace.json',!!localProject);}catch(e){if(e.name!=='AbortError')throw e;}});
$('download-project').onclick=guard(async()=>{try{await saveDocuments([...state.docs],'apple-iie-workspace.json',false,false);}catch(e){if(e.name!=='AbortError')throw e;}});
function openDocuments(docs){
  if(!docs.length)throw Error('Ce projet ne contient aucun document');
  for(const d of docs){
    // Reopening a saved document replaces its clean open copy. Keep unsaved
    // retouches as separate tabs rather than overwriting them on import.
    const index=state.docs.findIndex(existing=>existing.asset.key===d.asset.key&&!existing.edited);
    if(state.docs.some((existing,i)=>existing.id===d.id&&i!==index))d.id=C.blank(d.asset.mode).key;
    const opened={...d,undo:[],redo:[],edited:false};
    if(index>=0){state.docs[index]=opened;state.index=index;}
    else {state.docs.push(opened);state.index=state.docs.length-1;}
  }
  state.last=null;refresh();updateSaveState();autosave();
}
$('open-local-project').onclick=guard(async()=>{
  const response=await fetch('/api/project'),data=await response.json();
  if(!response.ok)throw Error(data.error);openDocuments(W.load(data));
  msg('Projet local rouvert avec ses retouches, sources et variantes.');
});
$('open-project').onclick=()=>$('project-input').click();
$('project-input').onchange=guard(async e=>{
  const file=e.target.files[0];e.target.value='';if(!file)return;
  if(file.size>64*1024*1024)throw Error('Projet trop volumineux (maximum 64 Mio)');
  const docs=W.load(JSON.parse(await file.text()));
  openDocuments(docs);
  msg(docs.length+' documents ouverts, avec leurs sources et toutes leurs variantes.');
});

function exportNative(bank){const a=asset(),order=$('bank-order').value;download(C.binary(a,bank,order),filename()+(C.dhgr(a)?'-'+(bank==='both'?order:bank):'')+(a.mode==='lowres'?'.lores':C.dhgr(a)?'.dhgr':'.hgr'),'application/octet-stream');msg('Binaire brut exporté, sans en-tête. Les octets non affichés sont conservés.');}
$('export-native').onclick=guard(()=>exportNative('both'));$('export-main').onclick=guard(()=>exportNative('main'));$('export-aux').onclick=guard(()=>exportNative('aux'));$('export-png').onclick=()=>{const bmp=bitmap();bmp.toBlob(b=>download(b,filename()+'.png','image/png'));};
$('import-file').onclick=()=>$('file-input').click();
$('file-input').onchange=guard(async e=>{
  const file=e.target.files[0];e.target.value='';if(!file)return;
  if(file.size>16*1024*1024)throw Error('Fichier trop volumineux (maximum 16 Mio)');
  const mode=$('mode').value,replace=$('replace-screen').checked&&asset().kind==='screen';
  let a,source=null;
  if(file.type.startsWith('image/')){
    const image=await createImageBitmap(file);
    try {
      if(image.width*image.height>4194304)throw Error('Maximum 4 millions de pixels : redimensionnez une copie avant import.');
      const tmp=document.createElement('canvas');tmp.width=image.width;tmp.height=image.height;
      const c=tmp.getContext('2d');c.drawImage(image,0,0);
      source=W.rasterSource(image.width,image.height,c.getImageData(0,0,image.width,image.height).data,
        {name:file.name,mime:file.type,data:W.encodeBytes(new Uint8Array(await file.arrayBuffer()))});
      if(replace)source.mixed=!!asset().mixed;
      a=W.convert(source,mode);
    } finally {image.close();}
  }else a=C.importBinary(new Uint8Array(await file.arrayBuffer()),mode,$('bank-order').value);
  a.name=file.name;
  if(replace){
    checkpoint();const d=current();
    a.key=d.asset.key;a.source=d.asset.source;a.name=d.name;a.mixed=d.asset.mixed;
    W.replaceSource(d,a,source);refresh();
  }else add(a,source);
  changed();msg('Import terminé. La source originale est conservée dans le projet ; le mode ne modifie que sa représentation.');
});

function referenceInfo(){
  const d=current(),source=d.sources[d.reference];
  $('reference-info').textContent=(source.type==='rgba'?`Source image ${source.width} × ${source.height}`:
    source.type==='edit'?'Dessin partagé · retouches locales':`Source native ${W.modeLabel(source.asset.mode)}`)+
    ' · Les changements de mode préservent les zones non retouchées.';
  $('archive-reference').replaceChildren(...d.archives.map((a,i)=>{
    const o=document.createElement('option');o.value=i;o.textContent=`Version ${i+1} · ${W.modeLabel(a.active)}`;return o;
  }));
  $('archive-reference').hidden=!d.archives.length;$('restore-reference').disabled=!d.archives.length;
}
$('restore-reference').onclick=guard(()=>{checkpoint();W.restoreArchive(current(),Number($('archive-reference').value));changed();refresh();});
$('rename').onclick=()=>{const name=prompt('Nom du document',current().name);if(name?.trim()){checkpoint();current().name=name.trim();asset().name=current().name;changed();refresh();}};
$('export-assets').onclick=guard(()=>{download(JSON.stringify(W.exportNativeAssets(state.docs),null,2)+'\n','apple-iie-artwork.json','application/json');msg('Ressources natives exportées séparément. Conservez le projet multiformat pour retrouver les sources et les archives.');});
$('export-source').onclick=guard(()=>{
  const source=current().sources[0];
  if(source.type==='native'){
    if(source.asset.kind==='screen')download(C.binary(source.asset),'source-originale.'+(C.dhgr(source.asset)?'dhgr':source.asset.mode==='lowres'?'lores':'hgr'),'application/octet-stream');
    else download(JSON.stringify({schema:C.SCHEMA,assets:[source.asset]},null,2),'source-originale.json','application/json');
  }else if(source.file)download(W.decodeBytes(source.file.data),source.file.name,source.file.mime);
  else{
    const tmp=document.createElement('canvas');tmp.width=source.width;tmp.height=source.height;
    tmp.getContext('2d').putImageData(new ImageData(new Uint8ClampedArray(W.decodeBytes(source.rgba)),source.width,source.height),0,0);
    tmp.toBlob(b=>download(b,'source-originale.png','image/png'));
  }
});

document.addEventListener('keydown',e=>{if($('close-document-dialog').open||['INPUT','SELECT','TEXTAREA'].includes(e.target.tagName))return;const mod=e.metaKey||e.ctrlKey;if(mod&&e.key.toLowerCase()==='z'){e.preventDefault();history(e.shiftKey);return;}if(mod&&e.key.toLowerCase()==='s'){e.preventDefault();$('save-project').click();return;}if(mod)return;const tool={b:'pencil',e:'erase',f:'fill',l:'line',r:'rect',i:'pick'}[e.key.toLowerCase()];if(tool)setTool(tool);});
window.addEventListener('beforeunload',e=>{if(state.dirty){e.preventDefault();e.returnValue='';}});let resizeTimer;const resizeCanvas=()=>{clearTimeout(resizeTimer);resizeTimer=setTimeout(()=>{if(current())render();},80);};window.addEventListener('resize',resizeCanvas);new ResizeObserver(resizeCanvas).observe($('stage'));
async function start(){
  add(C.blank('dhgr'));
  try{
    const stored=localStorage.getItem('a2-atelier-recovery');
    if(stored){const recovery=JSON.parse(stored),docs=W.load(recovery);if(docs.length){
      state.docs=docs.map(d=>({...d,undo:[],redo:[],edited:!Array.isArray(recovery.unsavedDocumentIds)||recovery.unsavedDocumentIds.includes(d.id)}));state.index=0;updateSaveState();refresh();
      msg('Session récupérée, sources et variantes conservées.');
    }}
  }catch(e){msg('Récupération locale indisponible : '+e.message,true);}
  try{
    const response=await fetch('/api/config'),config=await response.json();
    if(!response.ok)throw Error(config.error);
    if(config.library){
      $('adapter-option').hidden=false;$('adapter-option').textContent=config.library;
      const r=await fetch('/api/catalog'),data=await r.json();if(!r.ok)throw Error(data.error);
      state.catalog=data;
    }
    if(config.project){
      localProject=config.project;
      $('save-project').textContent='Enregistrer dans '+localProject.name;
      $('save-project').title='Mettre à jour les ressources utilisées par la recompilation';
      $('download-project').hidden=false;$('open-local-project').hidden=!localProject.exists;
    }
    catalog();msg('Atelier prêt. Importez une image ou un binaire ; changer de mode conserve le même document et sa source.');
  }catch(e){msg('Bibliothèque optionnelle indisponible. Les documents, imports et conversions restent utilisables. '+e.message,true);}
}
start();
