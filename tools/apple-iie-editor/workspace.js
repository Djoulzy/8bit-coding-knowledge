// Non-destructive document model, independent of any game's resource format.
import * as C from './core.js';

export const SCHEMA = 'a2-workspace-v2';
export const MODES = ['mono', 'color', 'dhgr', 'dhgr-mono', 'lowres'];
const MODE_IDS = [...MODES, 'hgr']; // Legacy native/project identifier remains valid.
export const editorMode = mode => mode === 'hgr' ? 'color' : mode;
export const modeLabel = mode => ({mono: 'HGR Mono', color: 'HGR couleur',
  dhgr: 'DHGR couleur', 'dhgr-mono': 'DHGR Mono', lowres: 'LOWRES'}[editorMode(mode)] || mode);

export function encodeBytes(bytes) {
  let result = '';
  for (let i = 0; i < bytes.length; i += 8192) {
    result += String.fromCharCode(...bytes.subarray(i, i + 8192));
  }
  return btoa(result);
}

export function decodeBytes(text) {
  return Uint8Array.from(atob(text), c => c.charCodeAt(0));
}

export function createDocument(asset, rasterSource = null) {
  C.validateAsset(asset);
  return {
    id: C.blank(asset.mode).key,
    name: asset.name || 'Sans titre',
    asset: C.clone(asset),
    sources: [rasterSource || {type: 'native', asset: C.clone(asset)}],
    reference: 0,
    frozen: !!rasterSource,
    linkedModes: true,
    variants: {[asset.mode]: C.clone(asset)},
    archives: [],
  };
}

export function rasterSource(width, height, rgba, file = null) {
  if (!Number.isInteger(width) || !Number.isInteger(height) || width < 1 || height < 1 ||
      width * height > 4_194_304 || rgba.length !== width * height * 4) {
    throw Error('Image source limitée à 4 millions de pixels ; aucune réduction silencieuse.');
  }
  return {type: 'rgba', width, height, rgba: encodeBytes(rgba), file};
}

// Immutable sources are shared by undo snapshots; mutable variants are copied.
export function snapshot(d) {
  return {id: d.id, name: d.name, asset: C.clone(d.asset), sources: [...d.sources],
    reference: d.reference, frozen: d.frozen, linkedModes: d.linkedModes,
    variants: C.clone(d.variants), archives: [...d.archives]};
}

// Native views are conversion caches of ONE revision, never independent drawings.
// Metadata is not a drawing change (renaming must not quantize an imported image).
function drawing(a) {
  const {key, name, source, ...pixels} = a;
  return JSON.stringify(pixels);
}

function derived(d, mode, previous) {
  const a = convert(d.sources[d.reference], mode, d.sources);
  return viewMetadata(d, a, mode, previous);
}

function viewMetadata(d, a, mode, previous) {
  if (previous && previous.kind === a.kind) {
    a.key = previous.key;
    if (previous.source) a.source = C.clone(previous.source);
  } else if (previous) {
    // Stable generic key when a native sprite becomes a derived screen.
    a.key = 'custom/' + mode + '/converted-' + previous.key.slice(-100);
  }
  a.name = d.name;
  return a;
}

function archiveCurrent(d) {
  d.archives.push({reference: d.reference, variants: C.clone(d.variants),
    active: d.asset.mode, linkedModes: true});
}

export function synchronize(d) {
  const baseline = d.variants[d.asset.mode] || derived(d, d.asset.mode);
  if (drawing(d.asset) === drawing(baseline)) return false;
  // Retain the full reference and record only a change to one of its views.
  d.variants[d.asset.mode] = C.clone(baseline);
  archiveCurrent(d);
  const previous = d.variants;
  const edit = {type: 'edit', base: d.reference,
    before: C.clone(baseline), after: C.clone(d.asset)};
  d.sources.push(edit);
  d.reference = d.sources.length - 1;
  d.frozen = true;
  d.variants = {};
  for (const mode of Object.keys(previous)) {
    d.variants[mode] = viewMetadata(d, applyEdit(previous[mode], edit, mode), mode, previous[mode]);
  }
  d.variants[d.asset.mode] = C.clone(d.asset);
  return true;
}

export function switchMode(d, mode) {
  mode = editorMode(mode);
  if (!MODES.includes(mode)) throw Error('Mode graphique inconnu');
  if (mode === editorMode(d.asset.mode)) return;
  synchronize(d);
  if (mode === 'color') {
    // Reuse the original identifier and native bytes, including old HGR keys.
    const source = d.sources[d.reference];
    if (source.type === 'native' && editorMode(source.asset.mode) === 'color') mode = source.asset.mode;
    else if (!d.variants.color && d.variants.hgr) mode = 'hgr';
  }
  d.asset = d.variants[mode] ? C.clone(d.variants[mode]) : derived(d, mode);
  d.asset.name = d.name;
  d.variants[mode] = C.clone(d.asset);
}

export function replaceSource(d, asset, source = null) {
  synchronize(d);
  archiveCurrent(d);
  d.sources.push(source || {type: 'native', asset: C.clone(asset)});
  d.reference = d.sources.length - 1;
  d.asset = C.clone(asset);
  d.variants = {[asset.mode]: C.clone(asset)};
  d.frozen = true;
}

export function restoreArchive(d, index) {
  const archive = d.archives[index];
  if (!archive) throw Error('Version archivée introuvable');
  synchronize(d);
  archiveCurrent(d);
  d.reference = archive.reference;
  d.variants = C.clone(archive.variants);
  d.asset = C.clone(d.variants[archive.active]);
  d.asset.name = d.name;
  d.frozen = true;
  if (!archive.linkedModes) linkLegacyViews(d);
}

// Preserve all old independent drawings in an archive; use the visible drawing
// for subsequent conversions. Unedited imports retain their full RGBA reference.
function linkLegacyViews(d) {
  const previous = {...d.variants, [d.asset.mode]: C.clone(d.asset)};
  d.archives.push({reference: d.reference, variants: C.clone(previous), active: d.asset.mode});
  // Make each old independent drawing recoverable from the version selector.
  for (const [mode, a] of Object.entries(previous)) {
    if (mode !== d.asset.mode) d.archives.push({reference: d.reference,
      variants: {[mode]: C.clone(a)}, active: mode});
  }
  d.linkedModes = true;
  d.variants = {[d.asset.mode]: derived(d, d.asset.mode, d.asset)};
  synchronize(d);
  for (const mode of Object.keys(previous)) d.variants[mode] = derived(d, mode, previous[mode]);
  d.variants[d.asset.mode] = C.clone(d.asset);
}

export function sourceRaster(source) {
  if (source.type === 'rgba') {
    return {width: source.width, height: source.height, data: decodeBytes(source.rgba),
      displayRatio: source.width / source.height};
  }
  const a = source.asset, sprite = a.kind === 'sprite';
  const width = sprite ? a.width * (a.mode === 'dhgr' ? 4 : 1) :
    a.mode === 'lowres' ? 40 : C.dhgr(a) ? 560 : 280;
  const height = sprite ? a.height : C.dimensions(a)[1];
  const data = new Uint8Array(width * height * 4);
  for (let y = 0; y < height; y++) {
    const native = sprite ? C.spritePages(a, y, 1) : null;
    const row = C.scanline(native ? native.page : a, sprite ? 0 : y, 'color');
    for (let x = 0; x < width; x++) {
      const p = (y * width + x) * 4;
      data.set(row[x], p);
      data[p + 3] = native ? native.alpha[0][x] * 255 : 255;
    }
  }
  const displayRatio = sprite ? width * (a.mode === 'dhgr' ? 1 : 2) / (height * 2) :
    560 / (384 * (a.mixed ? 5 / 6 : 1));
  return {width, height, data, displayRatio};
}

export function nearest(rgb, colors) {
  let best = colors[0], error = Infinity;
  for (const color of colors) {
    const distance = C.RGB[color].reduce((sum, value, k) => sum + (value - rgb[k]) ** 2, 0);
    if (distance < error) {best = color; error = distance;}
  }
  return best;
}

// Composite native differences instead of re-encoding an entire existing view.
// A color's shared phase can still affect neighbors within a hardware byte.
function applyEdit(view, edit, mode) {
  const {before, after} = edit;
  if (after.kind === 'sprite' && mode === after.mode) return C.clone(after);
  let result = C.clone(view);
  if (result.kind !== 'screen') {
    // Screen retouches cannot be encoded back into the optional sprite ABI.
    result = quantize(sourceRaster({type: 'native', asset: view}), mode, !!after.mixed);
  }
  // Mixed mode is a presentation flag, not an instruction to erase hidden rows.
  const full = a => a.kind === 'screen' ? {...a, mixed: false} : a;
  if (editorMode(before.mode) === editorMode(mode) && before.kind === 'screen') {
    // The edited native mode keeps exact bit changes, including reserved bytes.
    for (const bank of C.dhgr(result) ? ['main', 'aux'] : ['main']) {
      for (let i = 0; i < result[bank].length; i++) {
        const mask = before[bank][i] ^ after[bank][i];
        result[bank][i] = (result[bank][i] & ~mask) | (after[bank][i] & mask);
      }
    }
  } else {
    const oldRaster = sourceRaster({type: 'native', asset: full(before)});
    const newRaster = sourceRaster({type: 'native', asset: full(after)});
    const {width, height} = newRaster, stride = width + 1;
    // Summed-area mask: conversion affects only cells sampling changed pixels.
    const changed = new Uint32Array(stride * (height + 1));
    for (let y = 0; y < height; y++) {
      let row = 0;
      for (let x = 0; x < width; x++) {
        const p = (y * width + x) * 4;
        if ([0, 1, 2, 3].some(k => oldRaster.data[p+k] !== newRaster.data[p+k])) row++;
        changed[(y+1)*stride+x+1] = changed[y*stride+x+1] + row;
      }
    }
    const newView = convert({type: 'native', asset: full(after)}, mode);
    const [w, h] = C.dimensions({...result, mixed: false}, C.monochrome(result) ? 'dot' : 'cell');
    const usedW = Math.min(w, w * newRaster.displayRatio / (560/384));
    const usedH = Math.min(h, h * (560/384) / newRaster.displayRatio);
    const left = (w-usedW)/2, top = (h-usedH)/2;
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      if (x+.5 < left || x+.5 >= left+usedW || y+.5 < top || y+.5 >= top+usedH) continue;
      const x0 = Math.max(0, Math.floor((x-left)*width/usedW));
      const x1 = Math.min(width, Math.max(x0+1, Math.ceil((x+1-left)*width/usedW)));
      const y0 = Math.max(0, Math.floor((y-top)*height/usedH));
      const y1 = Math.min(height, Math.max(y0+1, Math.ceil((y+1-top)*height/usedH)));
      if (!(changed[y1*stride+x1]-changed[y0*stride+x1]-changed[y1*stride+x0]+changed[y0*stride+x0])) continue;
      if (C.monochrome(result)) C.writeDot(result,x,y,C.readDot(newView,x,y));
      else if (!C.hgr(result)) C.writeCell(result,x,y,C.readCell(newView,x,y));
      else {
        const bits = [C.readDot(newView,x*2,y),C.readDot(newView,x*2+1,y)];
        for (let b = 0; b < 2; b++) {
          C.writeDot(result,x*2+b,y,bits[b]);
          // Black/white cells need no phase change. Chromatic cells share the
          // phase of their byte with neighbors, as required by native HGR.
          if (bits[0] !== bits[1]) {
            const p = C.location(result,x*2+b,y,'dot');
            result.main[p.offset] = (result.main[p.offset]&127) | (newView.main[p.offset]&128);
          }
        }
      }
    }
  }
  result.mixed = !!after.mixed;
  return result;
}

export function convert(source, mode, sources = []) {
  if (source.type === 'edit') {
    // Backward-only references are validated on load. Iterate to avoid stack
    // limits for long editing sessions; never flatten away the original data.
    const edits = [], seen = new Set();
    while (source.type === 'edit') {
      if (seen.has(source) || !sources[source.base]) throw Error('Référence de retouche invalide');
      seen.add(source);edits.push(source);source = sources[source.base];
    }
    let view = convert(source, mode, sources);
    for (let i = edits.length - 1; i >= 0; i--) view = applyEdit(view, edits[i], mode);
    return view;
  }
  if (source.type === 'native' && source.asset.mode === mode) return C.clone(source.asset);
  if (source.type === 'native' && source.asset.kind === 'screen' &&
      editorMode(source.asset.mode) === 'color' && editorMode(mode) === 'color') {
    return {...C.clone(source.asset), mode}; // Alias change must not requantize HGR memory.
  }
  return quantize(sourceRaster(source), mode, source.type === 'native' ? !!source.asset.mixed : !!source.mixed);
}

function quantize(raster, mode, mixed) {
  const a = C.blank(mode);
  a.mixed = mixed;
  const [w, h] = C.dimensions(a, C.monochrome(a) ? 'dot' : 'cell');
  const displayRatio = 560 / (384 * (a.mixed ? 5 / 6 : 1));
  const usedW = Math.min(w, w * raster.displayRatio / displayRatio);
  const usedH = Math.min(h, h * displayRatio / raster.displayRatio);
  const left = (w - usedW) / 2, top = (h - usedH) / 2;
  const colors = C.monochrome(a) ? [0, 15] : C.hgr(a) ? C.HGR_COLORS : C.RGB.map((_, i) => i);
  for (let y = 0; y < h; y++) {
    for (let x = 0; x < w; x++) {
      if (x + .5 < left || x + .5 >= left + usedW || y + .5 < top || y + .5 >= top + usedH) continue;
      // Area average when reducing resolution, nearest sample when enlarging.
      const x0 = Math.max(0, Math.floor((x - left) * raster.width / usedW));
      const x1 = Math.min(raster.width, Math.max(x0 + 1, Math.ceil((x + 1 - left) * raster.width / usedW)));
      const y0 = Math.max(0, Math.floor((y - top) * raster.height / usedH));
      const y1 = Math.min(raster.height, Math.max(y0 + 1, Math.ceil((y + 1 - top) * raster.height / usedH)));
      const rgb = [0, 0, 0];
      let count = 0;
      for (let sy = y0; sy < y1; sy++) for (let sx = x0; sx < x1; sx++) {
        const p = (sy * raster.width + sx) * 4, alpha = raster.data[p + 3] / 255;
        for (let k = 0; k < 3; k++) rgb[k] += raster.data[p + k] * alpha;
        count++;
      }
      const color = nearest(rgb.map(v => v / Math.max(1, count)), colors);
      if (C.monochrome(a)) C.writeDot(a, x, y, color !== 0);
      else C.writeCell(a, x, y, color);
    }
  }
  return a;
}

function validateSource(source, index) {
  if (source?.type === 'edit') {
    if (!Number.isInteger(source.base) || source.base < 0 || source.base >= index) throw Error('Référence de retouche invalide');
    C.validateAsset(source.before);C.validateAsset(source.after);
    for (const field of ['kind', 'mode', 'width', 'height', 'encoding']) {
      if (source.before[field] !== source.after[field]) throw Error('Format de retouche incohérent');
    }
    return;
  }
  if (source?.type === 'native') {C.validateAsset(source.asset); return;}
  if (source?.type !== 'rgba') throw Error('Source de référence invalide');
  if (source.mixed !== undefined && typeof source.mixed !== 'boolean') throw Error('Présentation source invalide');
  const bytes = decodeBytes(source.rgba);
  rasterSource(source.width, source.height, bytes);
  if (source.file && (typeof source.file.name !== 'string' || typeof source.file.mime !== 'string' ||
      typeof source.file.data !== 'string' || decodeBytes(source.file.data).length > 16 * 1024 * 1024)) {
    throw Error('Fichier source invalide');
  }
}

export function validateDocument(d) {
  if (!d || typeof d.id !== 'string' || typeof d.name !== 'string' || typeof d.frozen !== 'boolean' ||
      !Array.isArray(d.sources) || !d.sources.length || !Array.isArray(d.archives) ||
      !Number.isInteger(d.reference) || d.reference < 0 || d.reference >= d.sources.length) {
    throw Error('Document multiformat invalide');
  }
  if (d.linkedModes !== undefined && typeof d.linkedModes !== 'boolean') throw Error('Liaison des modes invalide');
  C.validateAsset(d.asset);
  d.sources.forEach(validateSource);
  const checkVariants = variants => {
    if (!variants || Array.isArray(variants) || typeof variants !== 'object') throw Error('Variantes invalides');
    for (const [mode, a] of Object.entries(variants)) {
      if (!MODE_IDS.includes(mode) || mode !== a.mode) throw Error('Mode de variante incohérent');
      C.validateAsset(a);
    }
  };
  checkVariants(d.variants);
  for (const archive of d.archives) {
    if (archive.linkedModes !== undefined && typeof archive.linkedModes !== 'boolean') throw Error('Archive invalide');
    if (!Number.isInteger(archive.reference) || archive.reference < 0 || archive.reference >= d.sources.length) throw Error('Archive invalide');
    checkVariants(archive.variants);
    if (!Object.hasOwn(archive.variants, archive.active)) throw Error('Vue archivée manquante');
  }
  return d;
}

export function serialize(documents) {
  // Saving/exporting must also include edits made since the last mode switch.
  // Work on snapshots so saving does not alter undo history or the live document.
  return {schema: SCHEMA, name: 'Atelier Apple IIe', documents: documents.map(d => {
    const copy = snapshot(d);
    synchronize(copy);
    return copy;
  })};
}

export function load(project) {
  if (project?.schema === C.SCHEMA) {
    C.validateProject(project);
    // Adapter saves are compiler-native resources with the complete workspace
    // attached. Reopening that same file must retain sources and edit history.
    if (project.workspace !== undefined) {
      if (project.workspace?.schema !== SCHEMA) throw Error('Projet multiformat associé invalide');
      return load(project.workspace);
    }
    return project.assets.map(a => createDocument(a));
  }
  if (project?.schema !== SCHEMA || !Array.isArray(project.documents) || project.documents.length > 512) {
    throw Error('Projet a2-workspace-v2 ou a2-artwork-v1 attendu');
  }
  const ids = new Set();
  return project.documents.map(d => {
    validateDocument(d);
    if (ids.has(d.id)) throw Error('Identifiant de document dupliqué');
    ids.add(d.id);
    if (!d.linkedModes) linkLegacyViews(d);
    return d;
  });
}

// A separate export keeps native game ABI keys out of the generic workspace.
export function exportNativeAssets(documents) {
  const assets = new Map();
  for (const d of serialize(documents).documents) {
    const variants = {...d.variants, [d.asset.mode]: d.asset};
    for (const a of Object.values(variants)) {
      if (assets.has(a.key) && JSON.stringify(assets.get(a.key)) !== JSON.stringify(a)) {
        throw Error('Deux documents modifient la même ressource : ' + a.key);
      }
      assets.set(a.key, C.clone(a));
    }
  }
  return C.validateProject({schema: C.SCHEMA, assets: [...assets.values()]});
}
