// Hardware memory codecs. Digital previews match the port, not a calibrated CRT.
// DHGR preview classification derives from the port's dhgr.py (Apple2js MIT;
// see THIRD-PARTY-NOTICES.txt).
export const SCHEMA = 'a2-artwork-v1';
export const RGB = [[0,0,0],[227,30,96],[96,78,189],[255,68,253],[0,163,96],[156,156,156],[20,207,253],[208,195,255],[96,114,3],[255,106,60],[156,156,156],[255,160,208],[20,245,60],[208,221,141],[114,255,208],[255,255,255]];
export const NAMES = ['Noir','Rouge','Bleu foncé','Violet','Vert foncé','Gris 1','Bleu','Lavande','Brun','Orange','Gris 2','Rose','Vert','Jaune','Turquoise','Blanc'];
export const SERIAL = [0,2,4,6,8,5,12,14,1,3,10,7,9,11,13,15];
export const PATTERN = RGB.map((_, i) => SERIAL.indexOf(i));
export const HGR_COLORS = [0,3,12,15,9,6];
export const STATUS = [0,1,3,4,5,7,10,12,13,15];
export const clone = a => JSON.parse(JSON.stringify(a));
export const hex = (v, n=2) => '$' + v.toString(16).toUpperCase().padStart(n,'0');
export const rowOffset = y => (y & 7)*1024 + ((y >> 3)&7)*128 + (y >> 6)*40;
export const textOffset = y => (y & 7)*128 + (y >> 3)*40;
export const dhgr = a => ['dhgr','dhgr-mono'].includes(a.mode);
export const monochrome = a => ['mono','dhgr-mono'].includes(a.mode);
export const hgr = a => ['mono','color','hgr'].includes(a.mode);
export function dimensions(a, unit='cell') {
  if (a.kind === 'sprite') return [a.width, a.height];
  return [a.mode === 'lowres' ? 40 : dhgr(a) ? (unit === 'dot' || monochrome(a) ? 560 : 140) : (unit === 'cell' && a.mode !== 'mono' ? 140 : 280), a.mode === 'lowres' ? (a.mixed ? 40 : 48) : (a.mixed ? 160 : 192)];
}
export function blank(mode) {
  const a = {key:'custom/' + Date.now() + '-' + Math.random().toString(36).slice(2,7),name:'Sans titre · '+mode,kind:'screen',mode,mixed:false,main:Array(mode==='lowres'?1024:8192).fill(0)};
  if (dhgr(a)) a.aux=Array(8192).fill(0);
  return a;
}
export function location(a,x,y,unit='cell') {
  if(a.mode==='lowres') return {bank:'main',offset:textOffset(y>>1)+x,bit:(y&1)*4};
  if(dhgr(a)) {
    const sample=x*(unit==='dot'||monochrome(a)?1:4), serial=Math.floor(sample/7);
    return {bank:serial&1?'main':'aux',offset:rowOffset(y)+Math.floor(serial/2),bit:sample%7};
  }
  const dot=x*(unit==='cell'&&a.mode!=='mono'?2:1);
  return {bank:'main',offset:rowOffset(y)+Math.floor(dot/7),bit:dot%7};
}
export function readDot(a,x,y) {
  const p=location(a,x,y,'dot');return (a[p.bank][p.offset]>>p.bit)&1;
}
export function writeDot(a,x,y,value) {
  const p=location(a,x,y,'dot'), mask=1<<p.bit;
  a[p.bank][p.offset]=(a[p.bank][p.offset]&~mask)|(value?mask:0);
}
export function readCell(a,x,y) {
  if(a.mode==='dhgr-mono')return readDot(a,x,y)?15:0;
  if(a.kind==='sprite') return a.mode==='dhgr'?a.statuses[y][x]:a.masks[y][x]?a.pixels[y][x]?2:1:0;
  if(a.mode==='lowres') {const p=location(a,x,y);return (a.main[p.offset]>>p.bit)&15;}
  if(a.mode==='dhgr') {let code=0;for(let b=0;b<4;b++)code|=readDot(a,x*4+b,y)<<b;return SERIAL[code];}
  const p=location(a,x*2,y,'dot'),bits=readDot(a,x*2,y)|(readDot(a,x*2+1,y)<<1);
  return bits===0?0:bits===3?15:bits===1?(a.main[p.offset]&128?6:3):(a.main[p.offset]&128?9:12);
}
export function writeCell(a,x,y,color) {
  if(a.mode==='dhgr-mono'){if(![0,15].includes(color))throw Error('DHGR Mono : noir ou blanc attendu');writeDot(a,x,y,color!==0);return;}
  if(a.mode==='lowres') {const p=location(a,x,y), mask=15<<p.bit;a.main[p.offset]=(a.main[p.offset]&~mask)|(color<<p.bit);return;}
  if(a.mode==='dhgr') {for(let b=0;b<4;b++)writeDot(a,x*4+b,y,(PATTERN[color]>>b)&1);return;}
  const bits={0:0,3:1,12:2,15:3,9:2,6:1}[color];
  if(bits===undefined)throw Error('Couleur incompatible avec HGR');
  for(let b=0;b<2;b++) {
    const dot=x*2+b,p=location(a,dot,y,'dot');writeDot(a,dot,y,(bits>>b)&1);
    if(color!==0&&color!==15)a.main[p.offset]=(a.main[p.offset]&127)|([9,6].includes(color)?128:0);
  }
}
export function statusMask(v) {return v===10?15:((v&1?3:0)|(v&4?12:0));}
export function statusPattern(v, fg) {
  if(v===10||v===15)return fg;
  const detail=(v&2?3:0)|(v&8?12:0);return (detail&fg)||detail;
}
export function spritePages(a, firstRow=0, rowCount=a.height) {
  const page=blank(a.mode),alpha=[];
  for(let y=0;y<rowCount;y++) {
    const sourceY=firstRow+y;
    alpha[y]=[];
    for(let x=0;x<a.width;x++) {
      if(a.mode==='dhgr') {
        const v=a.statuses[sourceY][x],tile=a.encoding==='tile';
        const mask=tile?(v?15:0):statusMask(v);
        const code=tile?(v===1?0:PATTERN[v===3?a.accent:a.colors[sourceY]]):statusPattern(v,PATTERN[a.colors[sourceY]]);
        for(let b=0;b<4;b++){if(y<192)writeDot(page,x*4+b,y,(code>>b)&1);alpha[y][x*4+b]=(mask>>b)&1;}
      } else {
        if(y<192){writeDot(page,x,y,a.pixels[sourceY][x]);page.main[rowOffset(y)+Math.floor(x/7)]|=a.phase;}
        alpha[y][x]=a.masks[sourceY][x];
      }
    }
  }
  return {page,alpha};
}
export function scanline(a,y,monitor='color') {
  if(a.mode==='lowres')return Array.from({length:40},(_,x)=>RGB[readCell(a,x,y)]);
  const width=dhgr(a)?560:280,dots=Array.from({length:width},(_,x)=>readDot(a,x,y));
  if(monitor==='mono'||monochrome(a))return dots.map(v=>RGB[v?15:0]);
  if(a.mode==='dhgr') {
    const codes=Array.from({length:140},(_,x)=>PATTERN[readCell(a,x,y)]);
    return dots.map((_,x)=>{
      const cell=x>>2,bit=x&3,code=codes[cell],before=codes[cell-1]||0,after=codes[cell+1]||0;
      const window=(before|(code<<4)|(after<<8))>>bit,color=RGB[SERIAL[code]];
      if(monitor==='palette')return color;
      if(code!==before&&code!==after&&[0x1c,0x70,0x38].some(m=>(window&m)===m))return RGB[15];
      if((window&0x38)||code===before||code===after)return color;
      if(window&0x28)return color.map(v=>v>>1);
      return RGB[0];
    });
  }
  return dots.map((lit,x)=>{
    const before=dots[x-1]||0,after=dots[x+1]||0,phase=a.main[rowOffset(y)+Math.floor(x/7)]&128;
    const color=phase?(x&1?9:6):(x&1?12:3);
    if(lit)return RGB[before||after?15:color];
    if(before&&after)return RGB[phase?(x&1?6:9):(x&1?3:12)].map(v=>v>>1);
    return RGB[0];
  });
}
export function validateAsset(a) {
  const vec=(v,n,max)=>Array.isArray(v)&&v.length===n&&v.every(x=>Number.isInteger(x)&&x>=0&&x<=max);
  if(!a||typeof a.key!=='string'||a.key.length>160||!['mono','color','hgr','dhgr','dhgr-mono','lowres'].includes(a.mode))throw Error('Ressource invalide');
  if(a.name!==undefined&&typeof a.name!=='string')throw Error('Nom invalide');
  if(a.kind==='screen') {
    if(!vec(a.main,a.mode==='lowres'?1024:8192,255)||(dhgr(a)&&!vec(a.aux,8192,255)))throw Error('Taille de banque incorrecte');
    if(a.mixed!==undefined&&typeof a.mixed!=='boolean')throw Error('Mode mixte invalide');
  }else if(a.kind==='sprite') {
    if(!Number.isInteger(a.width)||a.width<1||a.width>140||!Number.isInteger(a.height)||a.height<1||a.height>200)throw Error('Dimensions invalides');
    const rows=a.mode==='dhgr'?a.statuses:a.pixels;
    if(!Array.isArray(rows)||rows.length!==a.height||!rows.every(r=>vec(r,a.width,a.mode==='dhgr'?(a.encoding==='tile'?3:15):1)))throw Error('Pixels invalides');
    if(a.mode==='dhgr') {
      if(!['tile','actor'].includes(a.encoding)||!vec(a.colors,a.height,15)||!Number.isInteger(a.accent??0)||(a.accent??0)<0||(a.accent??0)>15||typeof(a.force_black??false)!=='boolean')throw Error('Palette invalide');
      if(a.encoding==='actor'&&rows.some(r=>r.some(v=>!STATUS.includes(v))))throw Error('Statut de masque invalide');
    }else if(['mono','color'].includes(a.mode)) {
      if(!Array.isArray(a.masks)||a.masks.length!==a.height||!a.masks.every(r=>vec(r,a.width,1))||![0,128].includes(a.phase??0)||rows.some((r,y)=>r.some((p,x)=>p&&!a.masks[y][x])))throw Error('Masque/phase invalide');
    }else throw Error('Mode de sprite non pris en charge');
  }else throw Error('Type de ressource inconnu');
  return a;
}
export function validateProject(p) {
  if(!p||p.schema!==SCHEMA||!Array.isArray(p.assets)||p.assets.length>512)throw Error('Projet a2-artwork-v1 attendu');
  const keys=new Set();p.assets.forEach(a=>{validateAsset(a);if(keys.has(a.key))throw Error('Clé de ressource dupliquée');keys.add(a.key);});return p;
}
export function binary(a,bank='both',order='main-aux') {
  if(a.kind!=='screen')throw Error('Utilisez le projet JSON pour préserver le format et les masques du sprite');
  if(!dhgr(a)||bank==='main')return new Uint8Array(a.main);
  if(bank==='aux')return new Uint8Array(a.aux);
  return new Uint8Array(order==='main-aux'?[...a.main,...a.aux]:[...a.aux,...a.main]);
}
export function importBinary(bytes,mode,order='main-aux') {
  const a=blank(mode),size=mode==='lowres'?1024:dhgr(a)?16384:8192;
  if(bytes.length!==size)throw Error(`Fichier brut attendu : ${size} octets (sans en-tête). DHGR : deux banques complètes.`);
  if(dhgr(a)) {a.main=Array.from(bytes.slice(order==='main-aux'?0:8192,order==='main-aux'?8192:16384));a.aux=Array.from(bytes.slice(order==='main-aux'?8192:0,order==='main-aux'?16384:8192));}
  else a.main=Array.from(bytes);
  return a;
}
