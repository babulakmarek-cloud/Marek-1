/* Kreslení: pohled na rozváděč, jednopólové a vícepólové schéma, popisky, typový štítek.
 * Vše se kreslí do seznamu primitiv v mm → render do SVG (tisk 1:1) nebo DXF (CAD).
 */
(function (root) {
  'use strict';
  const D = root.RData, C = root.RCalc;
  const M = 17.5; // šířka modulu [mm]

  // ---------- primitiva ----------
  function Sheet(w, h) { this.w = w; this.h = h; this.p = []; }
  Sheet.prototype.line = function (x1, y1, x2, y2, o) { this.p.push(Object.assign({ t: 'line', x1, y1, x2, y2 }, o)); return this; };
  Sheet.prototype.rect = function (x, y, w, h, o) { this.p.push(Object.assign({ t: 'rect', x, y, w, h }, o)); return this; };
  Sheet.prototype.circle = function (cx, cy, r, o) { this.p.push(Object.assign({ t: 'circle', cx, cy, r }, o)); return this; };
  Sheet.prototype.text = function (x, y, s, o) { this.p.push(Object.assign({ t: 'text', x, y, s: String(s == null ? '' : s), size: 2.5 }, o)); return this; };
  Sheet.prototype.poly = function (pts, o) { this.p.push(Object.assign({ t: 'poly', pts }, o)); return this; };

  const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const f = n => +(+n).toFixed(2);

  function toSVG(sh, opt) {
    opt = opt || {};
    const out = [];
    out.push('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + f(sh.w) + ' ' + f(sh.h) + '"' +
      (opt.mm ? ' width="' + f(sh.w) + 'mm" height="' + f(sh.h) + 'mm"' : '') +
      ' font-family="Arial, Helvetica, sans-serif" class="sheet">');
    out.push('<rect x="0" y="0" width="' + f(sh.w) + '" height="' + f(sh.h) + '" fill="#fff"/>');
    for (const e of sh.p) {
      const st = ' stroke="' + (e.stroke || '#000') + '" stroke-width="' + (e.sw || 0.25) + '"' + (e.dash ? ' stroke-dasharray="' + e.dash + '"' : '');
      const data = e.id ? ' data-id="' + e.id + '"' : '';
      if (e.t === 'line') out.push('<line x1="' + f(e.x1) + '" y1="' + f(e.y1) + '" x2="' + f(e.x2) + '" y2="' + f(e.y2) + '"' + st + '/>');
      else if (e.t === 'rect') out.push('<rect' + data + ' x="' + f(e.x) + '" y="' + f(e.y) + '" width="' + f(e.w) + '" height="' + f(e.h) + '"' + (e.rx ? ' rx="' + e.rx + '"' : '') + ' fill="' + (e.fill || 'none') + '"' + (e.stroke === 'none' ? '' : st) + (e.cls ? ' class="' + e.cls + '"' : '') + '/>');
      else if (e.t === 'circle') out.push('<circle cx="' + f(e.cx) + '" cy="' + f(e.cy) + '" r="' + f(e.r) + '" fill="' + (e.fill || 'none') + '"' + (e.stroke === 'none' ? '' : st) + '/>');
      else if (e.t === 'poly') out.push('<polygon points="' + e.pts.map(p => f(p[0]) + ',' + f(p[1])).join(' ') + '" fill="' + (e.fill || 'none') + '"' + (e.stroke === 'none' ? '' : st) + '/>');
      else if (e.t === 'text') {
        const anchor = e.anchor || 'start';
        const tr = e.rot ? ' transform="rotate(' + e.rot + ' ' + f(e.x) + ' ' + f(e.y) + ')"' : '';
        out.push('<text x="' + f(e.x) + '" y="' + f(e.y) + '" font-size="' + e.size + '" text-anchor="' + anchor + '"' +
          (e.weight ? ' font-weight="' + e.weight + '"' : '') + ' fill="' + (e.fill || '#000') + '"' + tr + '>' + esc(e.s) + '</text>');
      }
    }
    out.push('</svg>');
    return out.join('');
  }

  // DXF R12 (ASCII) – kompatibilní s AutoCAD, DraftSight, LibreCAD, EPLAN import
  function toDXF(sh) {
    const o = [];
    const P = (c, v) => { o.push(String(c)); o.push(String(v)); };
    const Y = y => f(sh.h - y);
    const layer = e => e.layer || (e.t === 'text' ? 'TEXT' : 'GEOM');
    P(0, 'SECTION'); P(2, 'HEADER'); P(9, '$INSUNITS'); P(70, 4); P(0, 'ENDSEC');
    P(0, 'SECTION'); P(2, 'ENTITIES');
    const line = (x1, y1, x2, y2, e) => { P(0, 'LINE'); P(8, layer(e)); P(10, f(x1)); P(20, Y(y1)); P(30, 0); P(11, f(x2)); P(21, Y(y2)); P(31, 0); };
    for (const e of sh.p) {
      if (e.t === 'line') line(e.x1, e.y1, e.x2, e.y2, e);
      else if (e.t === 'rect') { if (e.stroke === 'none') continue; line(e.x, e.y, e.x + e.w, e.y, e); line(e.x + e.w, e.y, e.x + e.w, e.y + e.h, e); line(e.x + e.w, e.y + e.h, e.x, e.y + e.h, e); line(e.x, e.y + e.h, e.x, e.y, e); }
      else if (e.t === 'poly') { for (let i = 0; i < e.pts.length; i++) { const a = e.pts[i], b = e.pts[(i + 1) % e.pts.length]; line(a[0], a[1], b[0], b[1], e); } }
      else if (e.t === 'circle') { P(0, 'CIRCLE'); P(8, layer(e)); P(10, f(e.cx)); P(20, Y(e.cy)); P(30, 0); P(40, f(e.r)); }
      else if (e.t === 'text' && e.s) {
        const h = e.size * 0.72; // výška verzálek
        P(0, 'TEXT'); P(8, 'TEXT'); P(10, f(e.x)); P(20, Y(e.y)); P(30, 0); P(40, f(h)); P(1, e.s.replace(/[\r\n]/g, ' '));
        if (e.rot) P(50, f(-e.rot));
        const al = { middle: 1, end: 2 }[e.anchor];
        if (al) { P(72, al); P(11, f(e.x)); P(21, Y(e.y)); P(31, 0); }
      }
    }
    P(0, 'ENDSEC'); P(0, 'EOF');
    return o.join('\r\n');
  }

  // ---------- pomocné ----------
  const tr = (meta, k) => (D.L[meta.lang] || D.L.cz)[k];
  function cname(d, lang) {
    if (d.circuit && d.circuit.name) return d.circuit.name;
    if (d.label) return d.label;
    const t = D.DEVICE_TYPES[d.type];
    return lang === 'de' ? t.de : lang === 'en' ? t.en : t.name;
  }
  function rating(d) {
    if (d.type === 'mcb') return d.char + d.In;
    if (d.type === 'rcbo') return d.char + d.In + ' ' + d.IdN + 'mA';
    if (d.type === 'rcd') return d.In + 'A ' + d.IdN + 'mA';
    if (d.type === 'fuse') return d.In + 'A gG';
    if (d.type === 'main' || d.type === 'contactor') return d.In + 'A';
    if (d.type === 'spd') return 'T1+T2';
    return '';
  }
  function wrap(s, maxChars, maxLines) {
    const words = String(s).split(/\s+/); const lines = []; let cur = '';
    for (const w of words) {
      if ((cur + ' ' + w).trim().length <= maxChars) cur = (cur + ' ' + w).trim();
      else { if (cur) lines.push(cur); cur = w.length > maxChars ? w.slice(0, maxChars) : w; }
    }
    if (cur) lines.push(cur);
    return lines.slice(0, maxLines);
  }
  function titleBlock(sh, b, title, sheetNo) {
    const m = b.meta, w = 180, h = 22, x = sh.w - w - 5, y = sh.h - h - 5;
    sh.rect(5, 5, sh.w - 10, sh.h - 10, { sw: 0.5 });
    sh.rect(x, y, w, h, { sw: 0.5 });
    sh.line(x, y + 8, x + w, y + 8); sh.line(x + 110, y, x + 110, y + h); sh.line(x + 110, y + 15, x + w, y + 15);
    sh.text(x + 2, y + 6, title, { size: 4, weight: 'bold' });
    sh.text(x + 2, y + 13, (m.project || '') + (m.location ? ' – ' + m.location : ''), { size: 2.8 });
    sh.text(x + 2, y + 19, m.name + '  ' + (m.bmk || ''), { size: 3.2, weight: 'bold' });
    sh.text(x + 112, y + 6, 'Datum: ' + (m.date || ''), { size: 2.5 });
    sh.text(x + 112, y + 13, 'Zprac.: ' + (m.author || ''), { size: 2.5 });
    sh.text(x + 112, y + 20, 'List ' + sheetNo + '   ' + m.network + ' ' + m.U0 + '/' + m.Un + ' V ' + m.fn + ' Hz', { size: 2.5 });
  }

  // ---------- pohled na rozváděč ----------
  function front(b, opt) {
    opt = opt || {};
    const m = b.meta, rows = Math.max(1, +m.rows), mods = Math.max(1, +m.modules);
    const pad = 30, rowH = 125, labH = 14;
    const W = mods * M + 2 * pad, H = rows * rowH + 2 * pad;
    const sh = new Sheet(W + 20, H + 30);
    const ox = 10, oy = 10;
    // skříň
    sh.rect(ox, oy, W, H, { fill: '#e9ecef', sw: 0.8, rx: 4 });
    sh.rect(ox + 8, oy + 8, W - 16, H - 16, { fill: '#f8f9fa', sw: 0.3, rx: 2 });
    sh.text(ox + W / 2, oy + 6, m.name + ' ' + (m.bmk || '') + '  –  ' + rows + ' × ' + mods + ' M  (' + f(mods * M) + ' mm)', { size: 3.5, anchor: 'middle', weight: 'bold' });
    for (let r = 1; r <= rows; r++) {
      const y0 = oy + pad + (r - 1) * rowH;
      const railY = y0 + labH + 45;
      // popisový pruh
      sh.rect(ox + pad, y0, mods * M, labH, { fill: '#fffbe6', sw: 0.2 });
      // DIN lišta
      sh.rect(ox + pad - 8, railY - 3.75, mods * M + 16, 7.5, { fill: '#adb5bd', sw: 0.2 });
      sh.text(ox + pad - 12, railY + 1.2, r, { size: 3.5, anchor: 'end', weight: 'bold' });
      // kryt s výřezem
      sh.rect(ox + pad, railY - 22.5, mods * M, 45, { fill: '#343a40', stroke: 'none' });
      let x = ox + pad;
      for (const d of b.devices.filter(d => +d.row === r)) {
        const w = C.width(d) * M;
        drawDevice(sh, d, x, railY, w, opt);
        // popisek
        const lines = wrap(cname(d, m.lang), Math.max(4, Math.floor(w / 1.45)), 3);
        sh.text(x + w / 2, y0 + 3.3, d.bmk || '', { size: 2.4, anchor: 'middle', weight: 'bold' });
        lines.forEach((ln, i) => sh.text(x + w / 2, y0 + 6.6 + i * 2.6, ln, { size: 2.0, anchor: 'middle' }));
        sh.line(x, y0, x, y0 + labH, { sw: 0.15 });
        x += w;
      }
      sh.line(x, y0, x, y0 + labH, { sw: 0.15 });
      if (x > ox + pad + mods * M + 0.1) sh.text(ox + pad + mods * M, railY + 30, '⚠ přeplněno', { size: 3, fill: '#c00', anchor: 'end' });
    }
    return sh;
  }

  function drawDevice(sh, d, x, cy, w, opt) {
    const sel = opt.selected === d.id;
    const top = cy - 45, h = 90;
    const t = d.type;
    const body = { spacer: '#495057', meter: '#f1f3f5', terminal: '#ced4da' }[t] || '#f8f9fa';
    if (t === 'spacer') { sh.rect(x + 0.3, cy - 22, w - 0.6, 44, { fill: '#495057', sw: 0.2, id: d.id, cls: 'dev' }); return; }
    sh.rect(x + 0.3, top, w - 0.6, h, { fill: body, sw: sel ? 0.9 : 0.25, stroke: sel ? '#0d6efd' : '#000', rx: 1, id: d.id, cls: 'dev' });
    // svorky nahoře/dole
    const poles = d.poles || 1, pw = w / Math.max(1, poles);
    for (let i = 0; i < poles && t !== 'terminal'; i++) {
      sh.circle(x + pw * (i + 0.5), top + 4, 1.6, { fill: '#adb5bd', sw: 0.15 });
      sh.circle(x + pw * (i + 0.5), top + h - 4, 1.6, { fill: '#adb5bd', sw: 0.15 });
    }
    sh.text(x + w / 2, top + 13, rating(d), { size: w < 20 ? 2.6 : 3.2, anchor: 'middle', weight: 'bold' });
    if (t === 'mcb' || t === 'rcbo' || t === 'main' || t === 'rcd' || t === 'fuse') {
      const lw = Math.min(6, w * 0.4);
      const col = t === 'main' ? '#c92a2a' : t === 'fuse' ? '#495057' : '#212529';
      // páčka (spojená přes všechny póly)
      sh.rect(x + w / 2 - Math.max(lw, w * 0.35) / 2, cy - 9, Math.max(lw, w * 0.35), 14, { fill: col, sw: 0.2, rx: 1 });
      sh.text(x + w / 2, cy - 11, 'I', { size: 2.2, anchor: 'middle', fill: '#555' });
      sh.text(x + w / 2, cy + 9, 'O', { size: 2.2, anchor: 'middle', fill: '#555' });
      if (d.type === 'rcd' || d.type === 'rcbo') {
        sh.rect(x + w - 6, cy + 13, 4, 4, { fill: '#ffd43b', sw: 0.2 });
        sh.text(x + w - 4, cy + 16.2, 'T', { size: 2.4, anchor: 'middle', weight: 'bold' });
        sh.text(x + 2, cy + 16.5, 'typ ' + d.rcdType, { size: 2 });
      }
    } else if (t === 'spd') {
      for (let i = 0; i < poles; i++) sh.rect(x + pw * i + pw * 0.2, cy - 6, pw * 0.6, 8, { fill: '#51cf66', sw: 0.2 });
    } else if (t === 'meter') {
      sh.rect(x + 3, cy - 10, w - 6, 9, { fill: '#c3fae8', sw: 0.2 });
      sh.text(x + w / 2, cy - 3.5, '000123,4', { size: 2.4, anchor: 'middle' });
      sh.text(x + w / 2, cy + 6, 'kWh', { size: 2.4, anchor: 'middle' });
    } else if (t === 'terminal') {
      const n = Math.round(w / 5);
      const cols = ['#1c7ed6', '#1c7ed6', '#2f9e44', '#2f9e44', '#868e96'];
      for (let i = 0; i < n; i++) sh.rect(x + 0.5 + i * (w - 1) / n, top + 10, (w - 1) / n - 0.4, h - 20, { fill: cols[i % cols.length], sw: 0.1 });
    } else {
      sh.rect(x + 2, cy - 6, w - 4, 12, { fill: '#dee2e6', sw: 0.2 });
      sh.text(x + w / 2, cy + 1, D.DEVICE_TYPES[t].bmk === 'Q' ? 'A1 A2' : t === 'psu' ? '~/=' : '◼', { size: 2.2, anchor: 'middle' });
    }
    sh.text(x + w / 2, top + h - 9, d.bmk || '', { size: 2.6, anchor: 'middle', weight: 'bold' });
  }

  // ---------- struktura pro schémata ----------
  function groups(b) {
    const devs = b.devices.filter(d => !['spacer', 'terminal', 'main'].includes(d.type));
    const used = new Set();
    const g = [];
    for (const d of devs) {
      if (used.has(d.id)) continue;
      if (d.type === 'rcd') {
        const ch = devs.filter(x => x.parent === d.id);
        ch.forEach(x => used.add(x.id));
        used.add(d.id);
        g.push({ head: d, items: ch.length ? ch : [] , cols: Math.max(1, ch.length) });
      } else if (!d.parent || !devs.find(x => x.id === d.parent)) {
        used.add(d.id); g.push({ head: null, items: [d], cols: 1 });
      }
    }
    return g;
  }
  function phaseList(d) {
    const c = d.circuit;
    const ph = C.phasesOf(d);
    if (d.type === 'spd' || d.type === 'meter') return d.poles >= 3 ? ['L1', 'L2', 'L3', 'N'] : ['L1', 'N'];
    if (d.type === 'rcd') return d.poles >= 4 ? ['L1', 'L2', 'L3', 'N'] : [d._ph || 'L1', 'N'];
    if (!c) return [d._ph || 'L1'];
    if (ph === 3) return d.poles >= 4 ? ['L1', 'L2', 'L3', 'N'] : ['L1', 'L2', 'L3'];
    return d.poles >= 2 ? [c.phase, 'N'] : [c.phase];
  }

  // ---------- jednopólové schéma ----------
  function singleLine(b, calc) {
    const m = b.meta, G = groups(b);
    const colW = 26, x0 = 60;
    const nCols = G.reduce((a, g) => a + g.cols, 0);
    const W = Math.max(420, x0 + nCols * colW + 30), H = 297;
    const sh = new Sheet(W, H);
    titleBlock(sh, b, 'Jednopólové schéma / Übersichtsschaltplan', 1);
    const main = b.devices.find(d => d.type === 'main');
    const busY = 70;
    // přívod
    const ix = 35;
    sh.line(ix, 15, ix, 30, { sw: 0.5 });
    sh.text(ix + 3, 18, 'Přívod / Einspeisung', { size: 2.5 });
    sh.text(ix + 3, 22, m.network + ' ' + m.U0 + '/' + m.Un + ' V ' + m.fn + ' Hz', { size: 2.5 });
    sh.text(ix + 3, 26, 'Ik3 = ' + m.Ik3 + ' kA, Ze = ' + m.Ze + ' Ω', { size: 2.5 });
    if (main) { symDisconnector(sh, ix, 30, main); sh.text(ix + 6, 40, main.bmk + '  ' + main.In + ' A  ' + main.poles + 'p', { size: 2.6, weight: 'bold' }); }
    else sh.line(ix, 30, ix, 48, { sw: 0.5 });
    sh.line(ix, 48, ix, busY, { sw: 0.5 });
    poleMark(sh, ix, 55, main ? main.poles : 4);
    sh.line(ix, busY, x0 + nCols * colW, busY, { sw: 1.2 });
    sh.text(ix - 2, busY - 2, 'L1,L2,L3,N,PE', { size: 2.3, anchor: 'end' });
    // tabulka dole
    const tY = 175, rowsT = ['Označení', 'Přístroj', 'Fáze', 'P [kW]', 'Ib [A]', 'Kabel', 'Délka [m]', 'ΔU [%]', 'Okruh'];
    rowsT.forEach((r, i) => { sh.text(8, tY + 4 + i * 8, r, { size: 2.5, weight: 'bold' }); sh.line(7, tY + i * 8, x0 + nCols * colW, tY + i * 8, { sw: 0.15 }); });
    sh.line(7, tY + rowsT.length * 8, x0 + nCols * colW, tY + rowsT.length * 8, { sw: 0.15 });
    let col = 0;
    for (const g of G) {
      const gx = x0 + col * colW;
      if (g.head) {
        const cx = gx + (g.cols * colW) / 2 - colW / 2 + colW / 2;
        const hx = gx + colW / 2;
        sh.circle(hx, busY, 0.9, { fill: '#000' });
        sh.line(hx, busY, hx, busY + 8, { sw: 0.4 });
        symRCD(sh, hx, busY + 8, g.head);
        sh.text(hx + 6, busY + 14, g.head.bmk, { size: 2.6, weight: 'bold' });
        sh.text(hx + 6, busY + 18, g.head.In + 'A/' + g.head.IdN + 'mA ' + g.head.rcdType, { size: 2.3 });
        sh.line(hx, busY + 26, hx, busY + 34, { sw: 0.4 });
        sh.line(hx, busY + 34, gx + (g.cols - 0.5) * colW, busY + 34, { sw: 0.8 });
        void cx;
        g.items.forEach((d, i) => { const x = gx + (i + 0.5) * colW; outgoing(sh, d, x, busY + 34, calc, tY); });
        if (!g.items.length) sh.text(hx, busY + 40, '(bez vývodů)', { size: 2.2, anchor: 'middle' });
      } else {
        const d = g.items[0], x = gx + colW / 2;
        sh.circle(x, busY, 0.9, { fill: '#000' });
        outgoing(sh, d, x, busY, calc, tY, true);
      }
      col += g.cols;
    }
    return sh;
  }

  function poleMark(sh, x, y, n) {
    if (!n || n < 2) return;
    for (let i = 0; i < Math.min(n, 4); i++) sh.line(x - 2, y + 2 + i * 1.5, x + 2, y - 1 + i * 1.5, { sw: 0.3 });
    sh.text(x + 3, y + 3, n, { size: 2.2 });
  }
  function symBreaker(sh, x, y, len, kind) {
    // vertikální jistič: spodní pevný kontakt, šikmý nůž, × na horním kontaktu
    sh.line(x, y, x, y + 4, { sw: 0.4 });
    if (kind === 'fuse') { sh.rect(x - 1.8, y + 4, 3.6, 10, { sw: 0.35 }); sh.line(x, y + 4, x, y + 14, { sw: 0.3 }); sh.line(x, y + 14, x, y + len, { sw: 0.4 }); return; }
    sh.line(x - 1.5, y + 2.5, x + 1.5, y + 5.5, { sw: 0.35 }); sh.line(x + 1.5, y + 2.5, x - 1.5, y + 5.5, { sw: 0.35 });
    sh.line(x, y + 12, x - 4, y + 5, { sw: 0.4 });
    sh.line(x, y + 12, x, y + len, { sw: 0.4 });
    if (kind === 'contactor') { sh.circle(x, y + 4.8, 0.9); }
  }
  function symDisconnector(sh, x, y, d) {
    sh.line(x, y, x, y + 4, { sw: 0.5 });
    sh.line(x - 1.8, y + 4, x + 1.8, y + 4, { sw: 0.5 });
    sh.line(x, y + 12, x - 4.5, y + 4.5, { sw: 0.5 });
    sh.line(x, y + 12, x, y + 18, { sw: 0.5 });
    void d;
  }
  function symRCD(sh, x, y, d) {
    sh.line(x, y, x, y + 2, { sw: 0.4 });
    sh.line(x, y + 9, x - 4, y + 2, { sw: 0.4 });
    sh.line(x, y + 9, x, y + 18, { sw: 0.4 });
    // součtový transformátor
    sh.rect(x - 3, y + 13, 6, 3, { sw: 0.35, rx: 1.5 });
    sh.line(x - 3, y + 14.5, x - 6, y + 14.5, { sw: 0.25, dash: '0.8 0.6' });
    sh.line(x - 6, y + 14.5, x - 6, y + 6, { sw: 0.25, dash: '0.8 0.6' });
    sh.line(x - 6, y + 6, x - 2, y + 6, { sw: 0.25, dash: '0.8 0.6' });
    void d;
  }
  function outgoing(sh, d, x, y, calc, tY, fromBus) {
    sh.line(x, y, x, y + (fromBus ? 42 : 8), { sw: 0.4 });
    const sy = y + (fromBus ? 42 : 8);
    const r = calc && calc.circuits[d.id];
    const kind = d.type === 'fuse' ? 'fuse' : d.type === 'contactor' ? 'contactor' : 'mcb';
    if (d.type === 'spd') {
      sh.rect(x - 3, sy, 6, 10, { sw: 0.35 }); sh.line(x - 2, sy + 8, x + 2, sy + 2, { sw: 0.3 });
      sh.line(x, sy + 10, x, sy + 16, { sw: 0.4 }); sh.line(x - 3, sy + 16, x + 3, sy + 16, { sw: 0.4 }); sh.line(x - 2, sy + 17, x + 2, sy + 17, { sw: 0.4 }); sh.line(x - 1, sy + 18, x + 1, sy + 18, { sw: 0.4 });
    } else if (!d.circuit) {
      sh.rect(x - 4, sy, 8, 10, { sw: 0.35 }); sh.text(x, sy + 6.5, D.DEVICE_TYPES[d.type].bmk, { size: 2.6, anchor: 'middle' });
      sh.line(x, sy + 10, x, tY - 5, { sw: 0.4 });
    } else {
      symBreaker(sh, x, sy, 16, kind);
      if (d.type === 'rcbo') { sh.rect(x - 3, sy + 12, 6, 3, { sw: 0.35, rx: 1.5 }); }
      poleMark(sh, x, sy + 22, d.poles);
      sh.line(x, sy + 16, x, tY - 8, { sw: 0.4 });
      // šipka vývodu
      sh.poly([[x - 1.5, tY - 8], [x + 1.5, tY - 8], [x, tY - 5]], { fill: '#000', stroke: 'none' });
    }
    sh.text(x + (d.type === 'spd' ? 4 : 2.5), sy + 9, d.bmk || '', { size: 2.4, weight: 'bold' });
    const c = d.circuit || {};
    const vals = [d.bmk || '', rating(d), r ? r.phase : '', c.P != null && d.circuit ? c.P : '', r ? r.Ib.toFixed(1) : '',
      d.circuit ? c.cable : '', d.circuit ? c.len : '', r ? r.dUtot.toFixed(2) : '', cname(d, 'cz')];
    vals.forEach((v, i) => {
      const fill = (i === 7 && r && r.dUtot > r.dULim) ? '#c00' : '#000';
      if (i === 8) wrap(v, 12, 2).forEach((ln, k) => sh.text(x, tY + 3.6 + i * 8 + k * 2.8, ln, { size: 2.0, anchor: 'middle' }));
      else sh.text(x, tY + 5 + i * 8, v, { size: i === 5 ? 1.9 : 2.3, anchor: 'middle', fill });
    });
    if (r && !r.ok) sh.text(x, y + 6 + (fromBus ? 30 : 0), '⚠', { size: 4, anchor: 'middle', fill: '#c00' });
  }

  // ---------- vícepólové schéma ----------
  function multiLine(b, calc) {
    const m = b.meta, G = groups(b);
    const colW = 30, x0 = 70;
    const nCols = G.reduce((a, g) => a + g.cols, 0);
    const W = Math.max(420, x0 + nCols * colW + 30), H = 297;
    const sh = new Sheet(W, H);
    titleBlock(sh, b, 'Vícepólové schéma / Stromlaufplan', 2);
    const RY = { L1: 45, L2: 51, L3: 57, N: 63, PE: 69 };
    const RC = { L1: '#7b3f00', L2: '#000', L3: '#868e96', N: '#1c7ed6', PE: '#2f9e44' };
    const xEnd = x0 + nCols * colW;
    const main = b.devices.find(d => d.type === 'main');
    // přívod + hlavní vypínač
    const mph = ['L1', 'L2', 'L3', 'N'];
    const mx = 22;
    mph.forEach((p, i) => {
      const x = mx + i * 5;
      sh.text(x, 14, p, { size: 2.2, anchor: 'middle', fill: RC[p] });
      sh.line(x, 16, x, 22, { stroke: RC[p], sw: 0.35 });
      const switched = main && (main.poles >= 4 || (p !== 'N' && main.poles >= 3) || (main.poles === 2 && (p === 'L1' || p === 'N')) || (main.poles === 1 && p === 'L1'));
      if (switched) { sh.line(x - 1.2, 22, x + 1.2, 22, { sw: 0.35 }); sh.line(x, 30, x - 3, 23, { sw: 0.35, stroke: RC[p] }); }
      else sh.line(x, 22, x, 30, { stroke: RC[p], sw: 0.35 });
      sh.line(x, 30, x, RY[p], { stroke: RC[p], sw: 0.35 });
      sh.circle(x, RY[p], 0.7, { fill: RC[p], stroke: 'none' });
    });
    sh.text(mx - 4, 14, 'PE', { size: 2.2, anchor: 'middle', fill: RC.PE });
    sh.line(mx - 4, 16, mx - 4, RY.PE, { stroke: RC.PE, sw: 0.35 }); sh.circle(mx - 4, RY.PE, 0.7, { fill: RC.PE, stroke: 'none' });
    if (main) { sh.line(mx - 1.5, 26.5, mx + 15, 26.5, { dash: '1 0.8', sw: 0.2 }); sh.text(mx + 18, 27, main.bmk + ' ' + main.In + 'A', { size: 2.6, weight: 'bold' }); }
    for (const p in RY) { sh.line(mx - 6, RY[p], xEnd, RY[p], { stroke: RC[p], sw: 0.6 }); sh.text(xEnd + 2, RY[p] + 0.9, p, { size: 2.4, fill: RC[p] }); }

    const outY = 222;
    let col = 0;
    for (const g of G) {
      const gx = x0 + col * colW;
      if (g.head) {
        const r = g.head;
        r._ph = (g.items[0] && g.items[0].circuit && g.items[0].circuit.phase !== 'L123' && g.items[0].circuit.phase) || 'L1';
        const ph = phaseList(r);
        const hx = gx + 4;
        const subY = {};
        ph.forEach((p, i) => {
          const x = hx + i * 5;
          sh.circle(x, RY[p], 0.7, { fill: RC[p], stroke: 'none' });
          sh.line(x, RY[p], x, 80, { stroke: RC[p], sw: 0.35 });
          sh.line(x, 88, x - 3, 81, { sw: 0.35, stroke: RC[p] });
          sh.line(x, 88, x, 100 + i * 5, { stroke: RC[p], sw: 0.35 });
          subY[p] = 100 + i * 5;
          sh.line(x, subY[p], gx + (g.cols - 0.2) * colW, subY[p], { stroke: RC[p], sw: 0.45 });
        });
        sh.rect(hx - 2.5, 90, (ph.length - 1) * 5 + 5, 4, { sw: 0.3, rx: 2 });
        sh.line(hx - 2, 84.5, hx + (ph.length - 1) * 5 + 2, 84.5, { dash: '1 0.8', sw: 0.2 });
        sh.text(hx + ph.length * 5 + 1, 85, r.bmk, { size: 2.6, weight: 'bold' });
        sh.text(hx + ph.length * 5 + 1, 89, r.In + 'A ' + r.IdN + 'mA ' + r.rcdType, { size: 2.1 });
        g.items.forEach((d, i) => mlOutgoing(sh, d, gx + i * colW + 6, subY, RY, RC, outY, calc, 125));
      } else {
        mlOutgoing(sh, g.items[0], gx + 6, RY, RY, RC, outY, calc, 80);
      }
      col += g.cols;
    }
    return sh;
  }

  function mlOutgoing(sh, d, x0, srcY, RY, RC, outY, calc, devY) {
    const ph = phaseList(d);
    const switched = d.type === 'mcb' || d.type === 'rcbo' || d.type === 'fuse' || d.type === 'contactor';
    const nOnly = d.circuit && !ph.includes('N');
    let xi = 0;
    const xs = {};
    ph.forEach((p) => {
      const x = x0 + xi * 4; xi++; xs[p] = x;
      const y0 = srcY[p] != null ? srcY[p] : RY[p];
      sh.circle(x, y0, 0.7, { fill: RC[p], stroke: 'none' });
      sh.line(x, y0, x, devY, { stroke: RC[p], sw: 0.35 });
      if (d.type === 'spd') { sh.rect(x - 1.3, devY, 2.6, 7, { sw: 0.3 }); sh.line(x, devY + 7, x, devY + 12, { sw: 0.3 }); return; }
      if (switched) {
        if (d.type === 'fuse') sh.rect(x - 1.2, devY, 2.4, 8, { sw: 0.3 });
        else { sh.line(x - 1, devY + 1, x + 1, devY + 3, { sw: 0.25 }); sh.line(x + 1, devY + 1, x - 1, devY + 3, { sw: 0.25 }); sh.line(x, devY + 9, x - 2.7, devY + 3, { sw: 0.35, stroke: RC[p] }); }
        sh.line(x, devY + 9, x, outY, { stroke: RC[p], sw: 0.35 });
      } else {
        sh.rect(x - 1.3, devY, 2.6, 8, { sw: 0.3 }); sh.line(x, devY + 8, x, outY, { stroke: RC[p], sw: 0.35 });
      }
      sh.circle(x, outY, 0.8, { fill: '#fff', sw: 0.3 });
      sh.text(x, outY + 4, p, { size: 1.8, anchor: 'middle', fill: RC[p] });
    });
    if (d.type === 'spd') {
      const xm = x0 + (ph.length - 1) * 2;
      sh.line(x0, devY + 12, x0 + (ph.length - 1) * 4, devY + 12, { sw: 0.3 });
      sh.line(xm, devY + 12, xm, RY.PE, { stroke: RC.PE, sw: 0.35 });
      sh.text(x0 + ph.length * 4, devY + 6, d.bmk, { size: 2.4, weight: 'bold' });
      return;
    }
    if (switched && ph.length > 1) sh.line(x0 - 1.5, devY + 5.5, x0 + (ph.length - 1) * 4 + 0.5, devY + 5.5, { dash: '1 0.8', sw: 0.2 });
    // N nespínaný a PE
    const xn = x0 + xi * 4;
    if (d.circuit && nOnly && C.phasesOf(d) === 1) {
      const nY = srcY.N != null ? srcY.N : RY.N;
      sh.circle(xn, nY, 0.7, { fill: RC.N, stroke: 'none' }); sh.line(xn, nY, xn, outY, { stroke: RC.N, sw: 0.35 });
      sh.circle(xn, outY, 0.8, { fill: '#fff', sw: 0.3 }); sh.text(xn, outY + 4, 'N', { size: 1.8, anchor: 'middle', fill: RC.N }); xi++;
    }
    if (d.circuit) {
      const xp = x0 + xi * 4;
      sh.circle(xp, RY.PE, 0.7, { fill: RC.PE, stroke: 'none' }); sh.line(xp, RY.PE, xp, outY, { stroke: RC.PE, sw: 0.3, dash: '2 0.8' });
      sh.circle(xp, outY, 0.8, { fill: '#fff', sw: 0.3 }); sh.text(xp, outY + 4, 'PE', { size: 1.8, anchor: 'middle', fill: RC.PE });
    }
    sh.text(x0 - 2, devY + 18, d.bmk || '', { size: 2.5, weight: 'bold', rot: -90, anchor: 'end' });
    sh.text(x0 + 1, devY + 18, rating(d), { size: 2.1, rot: -90, anchor: 'end' });
    if (d.circuit) {
      sh.text(x0 + 4, outY - 3, d.circuit.cable + '  ' + d.circuit.len + ' m', { size: 1.9, rot: -90 });
      wrap(cname(d, 'cz'), 18, 2).forEach((ln, i) => sh.text(x0 + 8 + i * 2.6, outY + 9, ln, { size: 2.0, rot: -90, anchor: 'end' }));
    } else sh.text(x0 + 8, outY + 9, cname(d, 'cz'), { size: 2.0, rot: -90, anchor: 'end' });
  }

  // ---------- popisky 1:1 ----------
  function labelStrips(b) {
    const m = b.meta, rows = +m.rows, mods = +m.modules;
    const h = 14, gap = 8;
    const sh = new Sheet(mods * M + 20, rows * (h + gap) + 14);
    sh.text(10, 6, 'Popisové pruhy 1:1 – ' + m.name + ' (tisknout 100 %, bez přizpůsobení stránce)', { size: 2.8 });
    for (let r = 1; r <= rows; r++) {
      const y0 = 10 + (r - 1) * (h + gap);
      sh.text(8, y0 + h / 2 + 1, r, { size: 3, anchor: 'end' });
      sh.rect(10, y0, mods * M, h, { sw: 0.2 });
      let x = 10;
      for (const d of b.devices.filter(d => +d.row === r)) {
        const w = C.width(d) * M;
        const lines = wrap(cname(d, m.lang), Math.max(4, Math.floor(w / 1.45)), 3);
        sh.text(x + w / 2, y0 + 3.4, (d.bmk || '') + (rating(d) && d.type !== 'spacer' ? ' ' + rating(d) : ''), { size: 2.2, anchor: 'middle', weight: 'bold' });
        lines.forEach((ln, i) => sh.text(x + w / 2, y0 + 6.8 + i * 2.6, ln, { size: 2.0, anchor: 'middle' }));
        x += w; sh.line(x, y0, x, y0 + h, { sw: 0.15 });
      }
    }
    return sh;
  }

  function warnTriangle(sh, x, y, s) {
    sh.poly([[x, y + s], [x + s / 2, y], [x + s, y + s]], { fill: '#ffd43b', sw: s / 25 });
    const k = s / 20;
    sh.poly([[x + s * 0.53, y + 5 * k], [x + s * 0.38, y + 12 * k], [x + s * 0.5, y + 12 * k], [x + s * 0.44, y + 18 * k], [x + s * 0.62, y + 10 * k], [x + s * 0.5, y + 10 * k]], { fill: '#000', stroke: 'none' });
  }

  function nameplate(b, calc) {
    const m = b.meta, T = k => tr(m, k);
    const W = 105, H = 74;
    const sh = new Sheet(W + 10, H + 10 + 40);
    const x = 5, y = 5;
    sh.rect(x, y, W, H, { sw: 0.4, rx: 2 });
    sh.rect(x, y, W, 9, { fill: '#212529', stroke: 'none' });
    sh.text(x + W / 2, y + 6.3, T('plate'), { size: 3.6, anchor: 'middle', fill: '#fff', weight: 'bold' });
    const rows = [
      [T('manufacturer'), m.manufacturer],
      [T('type'), (m.type || m.name) + ' ' + (m.bmk || '')],
      [T('serial') + ' / ' + T('date'), (m.serial || '—') + ' / ' + (m.date || '')],
      [T('standard'), 'EN IEC 61439-1, -' + (m.standard === '61439-2' ? '2' : '3') + (m.standard === '61439-3' ? ' (DBO)' : ' (PSC)')],
      [T('Un') + ' / ' + T('fn'), '3/N/PE AC ' + m.Un + '/' + m.U0 + ' V ' + m.fn + ' Hz'],
      [T('Ui') + ' / Uimp', m.Ui + ' V / ' + m.Uimp + ' kV'],
      [T('InA'), (calc.InA || '—') + ' A'],
      [m.standard === '61439-3' ? T('Icc') : T('Icw'), m.Icc + ' kA'],
      [T('RDF'), String(calc.RDF).replace('.', ',')],
      [T('network') + ' / ' + T('IP') + ' / ' + T('IK'), m.network + ' / ' + m.IP + ' / ' + m.IK],
    ];
    if (m.weight) rows.push([T('weight'), m.weight + ' kg']);
    rows.forEach((r, i) => {
      const yy = y + 14 + i * 5.6;
      sh.text(x + 3, yy, r[0], { size: 2.3 });
      sh.text(x + W - 3, yy, r[1] || '', { size: 2.6, anchor: 'end', weight: 'bold' });
      sh.line(x + 2, yy + 1.4, x + W - 2, yy + 1.4, { sw: 0.1, stroke: '#adb5bd' });
    });
    if (m.ce) { sh.text(x + W - 4, y + H - 2.5, 'CE', { size: 6, anchor: 'end', weight: 'bold' }); }
    sh.text(x + 3, y + H - 3, m.standard === '61439-3' ? T('ordinary') : T('skilled'), { size: 2.1 });
    // výstražný štítek
    const wy = y + H + 6;
    sh.rect(x, wy, W, 30, { sw: 0.4, rx: 2 });
    warnTriangle(sh, x + 4, wy + 4, 22);
    sh.text(x + 32, wy + 12, T('warn'), { size: 3.4, weight: 'bold' });
    sh.text(x + 32, wy + 18, T('warn2'), { size: 2.8 });
    sh.text(x + 32, wy + 25, T('board') + ' ' + (m.bmk || '') + '  ' + m.U0 + '/' + m.Un + ' V', { size: 2.8 });
    return sh;
  }

  function circuitList(b, calc) {
    const m = b.meta, lang = m.lang;
    const H = { cz: ['Označ.', 'Okruh', 'Jištění', 'Chránič', 'Fáze', 'Kabel', 'Délka'], de: ['BMK', 'Stromkreis', 'Absicherung', 'FI', 'Phase', 'Kabel', 'Länge'], en: ['Ref.', 'Circuit', 'Protection', 'RCD', 'Phase', 'Cable', 'Length'] }[lang] || [];
    const title = { cz: 'Seznam okruhů', de: 'Stromkreisliste', en: 'Circuit schedule' }[lang];
    const outs = b.devices.filter(d => d.circuit);
    const X = [5, 22, 75, 100, 125, 140, 180], rowH = 6;
    const sh = new Sheet(200, 26 + outs.length * rowH + 10);
    sh.text(5, 8, title + ' – ' + m.name + ' ' + (m.bmk || ''), { size: 4, weight: 'bold' });
    sh.text(5, 13, m.network + ' ' + m.U0 + '/' + m.Un + ' V, InA = ' + (calc.InA || '—') + ' A, ' + (m.date || ''), { size: 2.6 });
    const y0 = 20;
    sh.rect(4, y0 - 4.5, 192, rowH, { fill: '#e9ecef', sw: 0.2 });
    H.forEach((h, i) => sh.text(X[i], y0, h, { size: 2.6, weight: 'bold' }));
    outs.forEach((d, k) => {
      const r = calc.circuits[d.id], yy = y0 + (k + 1) * rowH;
      const vals = [d.bmk, d.circuit.name, rating(d), r.rcd || '—', r.phase, d.circuit.cable, d.circuit.len + ' m'];
      vals.forEach((v, i) => sh.text(X[i], yy, i === 1 ? wrap(v, 30, 1)[0] || '' : v, { size: 2.5 }));
      sh.line(4, yy + 1.6, 196, yy + 1.6, { sw: 0.1, stroke: '#adb5bd' });
    });
    return sh;
  }

  root.RDraw = { Sheet, toSVG, toDXF, front, singleLine, multiLine, labelStrips, nameplate, circuitList, rating, cname, M };
})(typeof window !== 'undefined' ? window : globalThis);
