/* Uživatelské rozhraní – běží čistě v prohlížeči, bez serveru a bez internetu. */
(function () {
  'use strict';
  const D = window.RData, C = window.RCalc, R = window.RDraw;
  const $ = s => document.querySelector(s);
  const KEY = 'rozvadec.board.v1';
  let B = load() || D.templateRD();
  let calc = null, sel = null, tab = 'board';

  // ---------- ukládání ----------
  function load() { try { const s = localStorage.getItem(KEY); return s ? JSON.parse(s) : null; } catch (e) { return null; } }
  function persist() { try { localStorage.setItem(KEY, JSON.stringify(B)); } catch (e) { /* např. režim soukromí */ } }
  function download(name, data, type) {
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([data], { type: type || 'application/octet-stream' }));
    a.download = name; document.body.appendChild(a); a.click();
    setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 500);
  }
  const fname = ext => (B.meta.bmk || B.meta.name || 'rozvadec').replace(/[^\w\-=.]+/g, '_').replace(/^=/, '') + ext;
  const esc = s => String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  const fx = (v, n) => (v == null || !isFinite(v)) ? '—' : (+v).toFixed(n == null ? 1 : n).replace('.', ',');

  // ---------- záložka 1: parametry rozváděče ----------
  const META_FIELDS = [
    ['Identifikace'],
    ['name', 'Název rozváděče'], ['bmk', 'Označení (např. =RD1, =UV2)'], ['project', 'Zakázka / projekt'], ['location', 'Umístění'],
    ['manufacturer', 'Výrobce rozváděče (kdo jej sestavil)', '', 'Dle EN 61439 je „výrobcem“ ten, kdo rozváděč kompletuje – tj. často elektrikář/firma.'],
    ['type', 'Typové označení'], ['serial', 'Výrobní číslo'], ['date', 'Datum výroby', 'date'], ['author', 'Zpracoval'],
    ['lang', 'Jazyk štítků a popisků', [['cz', 'Čeština'], ['de', 'Deutsch'], ['en', 'English']]],
    ['Napájení'],
    ['network', 'Soustava', D.NETWORKS.map(n => [n, n])],
    ['U0', 'U0 fáze–zem [V]', 'number'], ['Un', 'Un sdružené [V]', 'number'], ['fn', 'Kmitočet [Hz]', 'number'],
    ['Ze', 'Impedance smyčky na přívodu Ze [Ω]', 'number', 'Změřit na svorkách přívodu nebo údaj od distributora. U TT zadejte RA.'],
    ['Ik3', 'Zkratový proud na přípojnici Ik3 [kA]', 'number', 'Pro kontrolu vypínací schopnosti Icn.'],
    ['dUfeed', 'Úbytek napětí na přívodu [%]', 'number', 'Úbytek od elektroměru k rozváděči – přičítá se ke každému vývodu.'],
    ['Skříň a štítek (EN 61439)'],
    ['standard', 'Norma rozváděče', [['61439-3', 'EN 61439-3 – DBO (obsluha laiky, byty/RD)'], ['61439-2', 'EN 61439-2 – PSC (výkonové, obsluha znalými)']]],
    ['rows', 'Počet řad', 'number'], ['modules', 'Modulů v řadě (1 M = 17,5 mm)', 'number'],
    ['Pde', 'Ztrátový výkon skříně Pde [W]', 'number', 'Z katalogu výrobce skříně – max. ztrátový výkon pro ověření oteplení.'],
    ['IP', 'Krytí IP'], ['IK', 'Mechanická odolnost IK'], ['Ui', 'Izolační napětí Ui [V]', 'number'], ['Uimp', 'Uimp [kV]', 'number'],
    ['Icc', 'Icc / Icw na štítek [kA]', 'number', 'U DBO podmíněný zkratový proud (Icc) – musí být ≥ Ik3 na místě instalace.'],
    ['weight', 'Hmotnost [kg] (volitelně)'],
    ['ce', 'Značka CE na štítku', [['', 'ne'], ['1', 'ano']]]
  ];
  function renderBoard() {
    const el = $('#boardForm'); let h = '';
    for (const fdef of META_FIELDS) {
      if (fdef.length === 1) { h += '<h3>' + fdef[0] + '</h3>'; continue; }
      const [k, lab, type, hint] = fdef, v = B.meta[k] == null ? '' : B.meta[k];
      let inp;
      if (Array.isArray(type)) inp = '<select data-m="' + k + '">' + type.map(o => '<option value="' + o[0] + '"' + (String(v) === String(o[0]) ? ' selected' : '') + '>' + esc(o[1]) + '</option>').join('') + '</select>';
      else inp = '<input data-m="' + k + '" type="' + (type === 'number' ? 'number' : type === 'date' ? 'date' : 'text') + '"' + (type === 'number' ? ' step="any"' : '') + ' value="' + esc(v) + '">';
      h += '<label class="f">' + esc(lab) + inp + (hint ? '<small>' + esc(hint) + '</small>' : '') + '</label>';
    }
    el.innerHTML = h;
  }
  $('#boardForm').addEventListener('change', e => {
    const k = e.target.dataset.m; if (!k) return;
    const v = e.target.type === 'number' ? C.num(e.target.value) : e.target.value;
    B.meta[k] = v; update();
  });

  // ---------- záložka 2: přístroje ----------
  const ADD = [['main', 'Hlavní vypínač'], ['rcd', 'Chránič (RCD)'], ['mcb', 'Jistič 1f'], ['mcb3', 'Jistič 3f'], ['rcbo', 'RCBO'], ['fuse', 'Pojistky'], ['spd', 'SPD'], ['contactor', 'Stykač'], ['relay', 'Relé'], ['meter', 'Elektroměr'], ['psu', 'Zdroj'], ['terminal', 'Svorky'], ['spacer', 'Rezerva']];
  $('#addbar').innerHTML = '<b>Přidat:</b> ' + ADD.map(a => '<button data-add="' + a[0] + '">+ ' + a[1] + '</button>').join('') +
    '<span class="sep"></span><button data-act="balance" title="Rozdělí 1f vývody na L1/L2/L3 podle soudobého výkonu">⚖ Vyvážit fáze</button>' +
    '<button data-act="renum" title="Přečísluje -Q, -F, -K… podle pořadí v řadách">№ Přečíslovat BMK</button>' +
    '<button data-act="autoS" title="U všech vývodů navrhne nejmenší vyhovující průřez">⌀ Navrhnout průřezy</button>';
  $('#addbar').addEventListener('click', e => {
    const t = e.target.dataset.add; if (!t) return;
    const lastRow = B.devices.length ? B.devices[B.devices.length - 1].row : 1;
    const rcds = B.devices.filter(d => d.type === 'rcd');
    let d;
    if (t === 'mcb3') d = D.dev('mcb', { poles: 3, char: 'C', circuit: D.newCircuit({ kind: 'motor', phase: 'L123', P: 5.5, cos: 0.85, cable: 'CYKY-J 5x2,5' }) });
    else d = D.dev(t, {});
    d.row = lastRow;
    if (t === 'rcd') d.In = 40;
    if (t === 'main') d.In = 40;
    if ((t === 'mcb') && rcds.length) d.parent = rcds[rcds.length - 1].id;
    if (sel) { const i = B.devices.findIndex(x => x.id === sel); const s = B.devices[i]; d.row = s.row; if (s.type === 'rcd' && t === 'mcb') d.parent = s.id; else if (s.parent && t === 'mcb') d.parent = s.parent; B.devices.splice(i + 1, 0, d); }
    else B.devices.push(d);
    autoBmk(d); sel = d.id; update();
  });
  function autoBmk(d) {
    const L = D.DEVICE_TYPES[d.type].bmk; if (!L) return;
    let n = 1; const used = new Set(B.devices.map(x => x.bmk));
    while (used.has('-' + L + n)) n++;
    d.bmk = '-' + L + n;
  }

  const opt = (arr, v) => arr.map(o => { const [val, lab] = Array.isArray(o) ? o : [o, o]; return '<option value="' + esc(val) + '"' + (String(val) === String(v) ? ' selected' : '') + '>' + esc(lab) + '</option>'; }).join('');
  function renderDevices() {
    const rcds = B.devices.filter(d => d.type === 'rcd');
    const rows = Array.from({ length: Math.max(1, C.num(B.meta.rows, 1)) }, (_, i) => i + 1);
    let h = '<thead><tr><th class="grp" colspan="11">Přístroj</th><th class="grp" colspan="13">Vývod / kabel</th><th class="grp" colspan="2"></th></tr><tr>' +
      ['', 'Řada', 'BMK', 'Typ', 'Pól', 'In [A]', 'Char.', 'Icn [kA]', 'IΔn [mA]', 'RCD typ', 'Za chráničem',
        'Název okruhu / popisek', 'Druh zátěže', 'P [kW]', 'cos φ', 'ks', 'Fáze', 'Kabel', 'S [mm²]', 'S PE', 'Délka [m]', 'Uložení', 'Svazek', 't [°C]', 'Stav', ''].map(x => '<th>' + x + '</th>').join('') + '</tr></thead><tbody>';
    B.devices.forEach((d, i) => {
      const t = D.DEVICE_TYPES[d.type], c = d.circuit, r = calc && calc.circuits[d.id];
      const has = k => {
        if (k === 'char') return ['mcb', 'rcbo'].includes(d.type);
        if (k === 'Icn') return ['mcb', 'rcbo', 'main'].includes(d.type);
        if (k === 'IdN') return t.rcd;
        if (k === 'In') return !['spacer', 'terminal', 'relay', 'psu', 'meter'].includes(d.type);
        return true;
      };
      const cell = (k, html) => has(k) ? '<td>' + html + '</td>' : '<td class="na">–</td>';
      let st = '';
      if (r) {
        const lvl = r.msgs.some(m => m.lvl === 'err') ? 'err' : r.msgs.some(m => m.lvl === 'warn') ? 'warn' : 'ok';
        st = '<span class="st ' + lvl + '" title="' + esc(r.msgs.map(m => m.m).join('\n') || 'Vyhovuje') + '">' + (lvl === 'ok' ? '✔' : lvl === 'warn' ? '!' : '✖') + '</span>';
      }
      h += '<tr data-id="' + d.id + '" class="' + (d.id === sel ? 'sel ' : '') + (d.type === 'rcd' ? 'rcdrow' : '') + '">' +
        '<td><button data-mv="-1" title="Nahoru">↑</button><button data-mv="1" title="Dolů">↓</button></td>' +
        '<td><select data-k="row">' + opt(rows, d.row) + '</select></td>' +
        '<td><input class="n" data-k="bmk" value="' + esc(d.bmk) + '"></td>' +
        '<td>' + esc(t.name) + '</td>' +
        '<td><select data-k="poles">' + opt(t.poles, d.poles) + '</select></td>' +
        cell('In', '<select data-k="In">' + opt([2, 4, 6, 10, 13, 16, 20, 25, 32, 40, 50, 63, 80, 100, 125, 160], d.In) + '</select>') +
        cell('char', '<select data-k="char">' + opt(['B', 'C', 'D', 'K', 'Z'], d.char) + '</select>') +
        cell('Icn', '<select data-k="Icn">' + opt([3, 4.5, 6, 10, 15, 25], d.Icn) + '</select>') +
        cell('IdN', '<select data-k="IdN">' + opt([10, 30, 100, 300, 500], d.IdN) + '</select>') +
        cell('IdN', '<select data-k="rcdType">' + opt(['AC', 'A', 'F', 'B', 'A-EV'], d.rcdType) + '</select>') +
        (c ? '<td><select data-k="parent">' + opt([['', '—']].concat(rcds.map(x => [x.id, x.bmk + ' ' + x.IdN + 'mA'])), d.parent) + '</select></td>' : '<td class="na">–</td>');
      if (c) {
        h += '<td><input class="l" data-c="name" value="' + esc(c.name) + '"></td>' +
          '<td><select data-c="kind">' + opt(Object.entries(D.LOAD_KINDS).map(([k, v]) => [k, v.cz]), c.kind) + '</select></td>' +
          '<td><input class="n" type="number" step="any" data-c="P" value="' + esc(c.P) + '"></td>' +
          '<td><input class="n" type="number" step="0.01" data-c="cos" value="' + esc(c.cos) + '"></td>' +
          '<td><input class="n" type="number" step="0.05" data-c="ks" placeholder="' + (D.LOAD_KINDS[c.kind] || D.LOAD_KINDS.other).ks + '" value="' + esc(c.ks == null ? '' : c.ks) + '" title="Koeficient soudobosti – prázdné = výchozí podle druhu zátěže"></td>' +
          '<td>' + (C.phasesOf(d) === 3 ? 'L1L2L3' : '<select data-c="phase">' + opt(['L1', 'L2', 'L3'], c.phase) + '</select>') + '</td>' +
          '<td><input class="m" data-c="cable" value="' + esc(c.cable) + '"></td>' +
          '<td><select data-c="S">' + opt(D.SECTIONS, c.S) + '</select></td>' +
          '<td><select data-c="Spe">' + opt(D.SECTIONS, c.Spe) + '</select></td>' +
          '<td><input class="n" type="number" step="any" data-c="len" value="' + esc(c.len) + '"></td>' +
          '<td><select data-c="method" title="' + esc(D.METHODS[c.method]) + '">' + opt(Object.keys(D.METHODS).map(k => [k, D.METHODS[k]]), c.method) + '</select></td>' +
          '<td><input class="n" type="number" min="1" data-c="group" value="' + esc(c.group) + '" title="Počet obvodů ve svazku"></td>' +
          '<td><input class="n" type="number" data-c="temp" value="' + esc(c.temp) + '"></td>';
      } else {
        h += '<td><input class="l" data-k="label" value="' + esc(d.label) + '"></td>' + '<td class="na" colspan="12">–</td>';
      }
      h += '<td>' + st + '</td><td><button data-dup title="Duplikovat">⧉</button><button data-del title="Smazat">✕</button></td></tr>';
    });
    $('#devTable').innerHTML = h + '</tbody>';
  }
  $('#devTable').addEventListener('change', e => {
    const tr = e.target.closest('tr'); if (!tr) return;
    const d = B.devices.find(x => x.id === tr.dataset.id); if (!d) return;
    const k = e.target.dataset.k, ck = e.target.dataset.c;
    const numeric = ['row', 'poles', 'In', 'Icn', 'IdN'];
    if (k) d[k] = numeric.includes(k) ? C.num(e.target.value) : e.target.value;
    if (ck) {
      const nk = ['P', 'cos', 'S', 'Spe', 'len', 'group', 'temp'];
      let v = e.target.value;
      if (ck === 'ks') v = v === '' ? null : C.num(v); else if (nk.includes(ck)) v = C.num(v);
      d.circuit[ck] = v;
      if (ck === 'kind') { const kk = D.LOAD_KINDS[v]; if (kk) d.circuit.cos = kk.cos; }
      if (ck === 'S') { d.circuit.Spe = v <= 16 ? v : Math.max(16, v / 2); syncCableName(d); }
    }
    if (k === 'poles' && d.circuit) { d.circuit.phase = d.poles >= 3 ? 'L123' : (d.circuit.phase === 'L123' ? 'L1' : d.circuit.phase); syncCableName(d); }
    update();
  });
  function syncCableName(d) {
    const c = d.circuit; const m = /^(\S+)\s+(\d)x([\d,\.]+)/.exec(c.cable || '');
    const cores = C.phasesOf(d) === 3 ? 5 : 3;
    const s = String(c.S).replace('.', ',');
    c.cable = (m ? m[1] : 'CYKY-J') + ' ' + cores + 'x' + s;
  }
  $('#devTable').addEventListener('click', e => {
    const tr = e.target.closest('tr'); if (!tr || !tr.dataset.id) return;
    const i = B.devices.findIndex(x => x.id === tr.dataset.id);
    if (e.target.dataset.mv) {
      const j = i + (+e.target.dataset.mv);
      if (j >= 0 && j < B.devices.length) { const [x] = B.devices.splice(i, 1); B.devices.splice(j, 0, x); }
      sel = tr.dataset.id; update(); return;
    }
    if (e.target.hasAttribute('data-del')) {
      const id = B.devices[i].id;
      B.devices.splice(i, 1); B.devices.forEach(x => { if (x.parent === id) x.parent = ''; });
      sel = null; update(); return;
    }
    if (e.target.hasAttribute('data-dup')) {
      const x = JSON.parse(JSON.stringify(B.devices[i])); x.id = 'd' + Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
      autoBmk(x); B.devices.splice(i + 1, 0, x); sel = x.id; update(); return;
    }
    if (sel !== tr.dataset.id) { sel = tr.dataset.id; document.querySelectorAll('#devTable tr').forEach(r => r.classList.toggle('sel', r.dataset.id === sel)); renderMini(); }
  });
  function clickSvg(e) {
    const r = e.target.closest('[data-id]'); if (!r) return;
    sel = r.dataset.id; switchTab('devices'); update();
    const row = document.querySelector('#devTable tr[data-id="' + sel + '"]'); if (row) row.scrollIntoView({ block: 'center' });
  }
  $('#miniFront').addEventListener('click', clickSvg);
  $('#frontOut').addEventListener('click', clickSvg);
  function renderMini() { $('#miniFront').innerHTML = R.toSVG(R.front(B, { selected: sel })); }

  // ---------- záložka 3: výpočty ----------
  function renderCalc() {
    const c = calc, m = B.meta;
    const allMsgs = c.msgs.slice();
    B.devices.filter(d => d.circuit).forEach(d => c.circuits[d.id].msgs.forEach(x => allMsgs.push({ lvl: x.lvl, m: (d.bmk || '') + ' ' + (d.circuit.name || '') + ': ' + x.m })));
    let h = '<div class="cards">' + [
      ['Instalovaný výkon', fx(c.Pinst, 1) + ' kW'], ['Soudobý výkon', fx(c.Psim, 1) + ' kW'],
      ['Soudobý proud L1 / L2 / L3', fx(c.phases.L1, 1) + ' / ' + fx(c.phases.L2, 1) + ' / ' + fx(c.phases.L3, 1) + ' A'],
      ['Nesymetrie fází', fx(c.unbalance, 0) + ' %'], ['InA (hlavní vypínač)', (c.InA || '—') + ' A'],
      ['RDF dle EN ' + m.standard, fx(c.RDF, 1) + ' (' + c.nCircuits + ' vývodů)'],
      ['Ztrátový výkon Pv / Pde', fx(c.Pv, 1) + ' / ' + (m.Pde || '—') + ' W'], ['Rezerva místa', c.reserve + ' M']
    ].map(x => '<div class="card"><div class="k">' + x[0] + '</div><div class="v">' + x[1] + '</div></div>').join('') + '</div>';
    h += '<ul class="msgs">' + (allMsgs.length ? allMsgs.map(x => '<li class="' + x.lvl + '">' + (x.lvl === 'err' ? '✖ ' : '! ') + esc(x.m) + '</li>').join('') : '<li class="ok">✔ Všechny kontroly vyhovují.</li>') + '</ul>';
    h += '<table class="res"><thead><tr><th>BMK</th><th>Okruh</th><th>Fáze</th><th>P [kW]</th><th>ks</th><th>Ib [A]</th><th>In [A]</th><th>Iz [A]<br><small>(tab × kT × kG)</small></th><th>Ib≤In≤Iz</th>' +
      '<th>ΔU [%]</th><th>ΔU celk. [%]</th><th>Zs [Ω]</th><th>Zs max [Ω]</th><th>Ik1 min [A]</th><th>Ia [A]</th><th>t odp. [s]</th><th>RCD</th><th>Pv [W]</th></tr></thead><tbody>';
    for (const d of B.devices.filter(d => d.circuit)) {
      const r = c.circuits[d.id], pv = c.pvList.find(p => p.id === d.id);
      const k3 = r.Ib <= r.In && r.Iz != null && r.In <= r.Iz;
      h += '<tr><td class="t"><b>' + esc(d.bmk) + '</b></td><td class="t">' + esc(d.circuit.name) + '</td><td>' + esc(r.phase) + '</td><td>' + fx(d.circuit.P, 2) + '</td><td>' + fx(r.ks, 2) + '</td>' +
        '<td>' + fx(r.Ib) + '</td><td>' + esc(r.In) + '</td><td title="' + fx(r.IzBase) + ' × ' + fx(r.kT, 2) + ' × ' + fx(r.kG, 2) + '">' + fx(r.Iz) + '</td>' +
        '<td class="' + (k3 ? 'good' : 'bad') + '">' + (k3 ? '✔' : '✖') + '</td>' +
        '<td>' + fx(r.dU, 2) + '</td><td class="' + (r.dUtot > r.dULim ? 'bad' : 'good') + '">' + fx(r.dUtot, 2) + ' ≤ ' + r.dULim + '</td>' +
        '<td>' + fx(r.Zs, 2) + '</td><td>' + fx(r.ZsMax, 2) + '</td><td class="' + (r.discOk === false ? 'bad' : 'good') + '">' + fx(r.Ik1, 0) + '</td>' +
        '<td title="' + esc(r.iaHow) + '">' + fx(r.Ia, 0) + '</td><td>' + r.tReq + '</td><td class="t">' + esc(r.rcd || '—') + '</td><td>' + fx(pv && pv.p, 2) + '</td></tr>';
    }
    h += '</tbody></table>';
    h += '<p class="hint" style="margin-top:10px">Předpoklady: Cu vodiče, izolace PVC 70 °C, ρ = 0,0225 Ω·mm²/m (70 °C), x = 0,08 mΩ/m, c<sub>min</sub> = 0,95. ' +
      'Zatížitelnost dle IEC 60364-5-52 tab. B.52.2/B.52.4/B.52.10 (ČSN 33 2000-5-52, DIN VDE 0298-4 se může v některých hodnotách lišit). ' +
      'Doba odpojení TN 230 V: koncové obvody ≤ 32 A 0,4 s, ostatní 5 s (ČSN 33 2000-4-41, VDE 0100-410). Ztrátové výkony přístrojů jsou typické – pro ověření oteplení dle EN 61439 použijte katalog výrobce. ' +
      'Výpočet nenahrazuje měření při výchozí revizi (ČSN 33 2000-6 / DIN VDE 0100-600).</p>';
    $('#calcOut').innerHTML = h;
  }

  // ---------- výkresy ----------
  const SHEETS = {
    front: () => R.front(B, {}), singleLine: () => R.singleLine(B, calc), multiLine: () => R.multiLine(B, calc),
    labelStrips: () => R.labelStrips(B), nameplate: () => R.nameplate(B, calc), circuitList: () => R.circuitList(B, calc)
  };
  const SHEET_NAMES = { front: 'pohled', singleLine: 'jednopolove', multiLine: 'vicepolove', labelStrips: 'popisky', nameplate: 'stitek', circuitList: 'seznam_okruhu' };
  document.querySelectorAll('.dl').forEach(el => {
    const k = el.dataset.sheet;
    el.innerHTML = '<button data-svg="' + k + '">⬇ SVG</button><button data-dxf="' + k + '">⬇ DXF (CAD)</button><button data-png="' + k + '">⬇ PNG</button><button data-pr="' + k + '">🖶 Tisk tohoto listu</button>';
  });
  document.addEventListener('click', e => {
    const t = e.target.dataset;
    if (t.svg) download(fname('_' + SHEET_NAMES[t.svg] + '.svg'), R.toSVG(SHEETS[t.svg](), { mm: true }), 'image/svg+xml');
    if (t.dxf) download(fname('_' + SHEET_NAMES[t.dxf] + '.dxf'), R.toDXF(SHEETS[t.dxf]()), 'application/dxf');
    if (t.png) toPNG(t.png);
    if (t.pr) printSheet(t.pr);
  });
  function toPNG(k) {
    const sh = SHEETS[k](), scale = 8; // 8 px/mm ≈ 200 dpi
    const img = new Image();
    img.onload = () => {
      const cv = document.createElement('canvas'); cv.width = sh.w * scale; cv.height = sh.h * scale;
      const g = cv.getContext('2d'); g.fillStyle = '#fff'; g.fillRect(0, 0, cv.width, cv.height); g.drawImage(img, 0, 0, cv.width, cv.height);
      cv.toBlob(b => download(fname('_' + SHEET_NAMES[k] + '.png'), b, 'image/png'));
    };
    img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(R.toSVG(sh, { mm: true }));
  }
  function printSheet(k) {
    const sh = SHEETS[k](), oneToOne = ['labelStrips', 'nameplate', 'circuitList'].includes(k);
    const w = window.open('', '_blank');
    if (!w) { alert('Prohlížeč zablokoval nové okno – povolte vyskakovací okna.'); return; }
    const land = sh.w > sh.h;
    w.document.write('<!doctype html><html><head><meta charset="utf-8"><title>' + esc(B.meta.name) + '</title><style>@page{size:' + (oneToOne ? 'A4 portrait' : (sh.w > 300 ? 'A3' : 'A4') + (land ? ' landscape' : ' portrait')) + ';margin:6mm}body{margin:0}svg{' + (oneToOne ? '' : 'width:100%;height:auto;max-height:100vh') + '}</style></head><body>' +
      R.toSVG(sh, { mm: oneToOne }) + '<script>window.onload=function(){window.print()}<\/script></body></html>');
    w.document.close();
  }

  // ---------- záložka 8: protokol ----------
  const CHECKS = [
    ['11.2', 'Stupeň ochrany krytem (IP)'], ['11.3', 'Vzdušné vzdálenosti a povrchové cesty'], ['11.4', 'Ochrana před úrazem el. proudem, spojitost ochranných obvodů'],
    ['11.5', 'Vestavěné přístroje – typy, nastavení, označení dle dokumentace'], ['11.6', 'Vnitřní el. obvody a spoje – utahovací momenty'],
    ['11.7', 'Svorky pro vnější vodiče'], ['11.8', 'Mechanická funkce ovládacích prvků'], ['11.9', 'Dielektrické vlastnosti (zkouška / měření Riso)'],
    ['11.10', 'Zapojení, provozní funkce'], ['6.1', 'Typový štítek a označení dle 6.1, dokumentace dle 6.2']
  ];
  function renderProto() {
    B.proto = B.proto || { checks: {}, Riso: '', who: '', date: '' };
    const P = B.proto;
    let h = '<div class="proto"><h2>Protokol o kusovém ověření rozváděče (ČSN EN 61439-1 čl. 11)</h2>' +
      '<p>' + esc(B.meta.name) + ' ' + esc(B.meta.bmk) + ' · ' + esc(B.meta.network) + ' ' + esc(B.meta.U0) + '/' + esc(B.meta.Un) + ' V · InA ' + esc(calc.InA || '—') + ' A · ' + esc(B.meta.manufacturer) + '</p>' +
      '<div class="chk">' + CHECKS.map(c => '<span>' + c[0] + ' – ' + esc(c[1]) + '</span><select data-pc="' + c[0] + '">' + opt([['', '—'], ['ok', 'vyhovuje'], ['nok', 'nevyhovuje'], ['na', 'neaplikuje se']], P.checks[c[0]] || '') + '</select>').join('') + '</div>' +
      '<table class="res"><thead><tr><th>BMK</th><th>Okruh</th><th>Zs max výpočet [Ω]</th><th>Zs naměřeno [Ω]</th><th>Riso [MΩ]</th><th>RCD t [ms]</th><th>RCD IΔ [mA]</th><th>Vyhodnocení</th></tr></thead><tbody>';
    for (const d of B.devices.filter(d => d.circuit)) {
      const r = calc.circuits[d.id], me = d.circuit.meas || {};
      const zs = C.num(me.Zs, NaN);
      let ev = '';
      if (isFinite(zs)) ev = zs <= (r.ZsMax || Infinity) ? '✔' : '✖ Zs';
      if (me.Riso !== undefined && me.Riso !== '' && C.num(me.Riso) < 1) ev += ' ✖ Riso';
      if (me.t !== undefined && me.t !== '' && C.num(me.t) > 300) ev += ' ✖ t';
      h += '<tr data-id="' + d.id + '"><td class="t">' + esc(d.bmk) + '</td><td class="t">' + esc(d.circuit.name) + '</td><td>' + fx(r.ZsMax, 2) + '</td>' +
        ['Zs', 'Riso', 't', 'I'].map(k => '<td><input data-me="' + k + '" value="' + esc(me[k] == null ? '' : me[k]) + '"></td>').join('') + '<td>' + ev + '</td></tr>';
    }
    h += '</tbody></table><div class="grid" style="margin-top:12px"><label class="f">Izolační odpor celého rozváděče [MΩ]<input data-pm="Riso" value="' + esc(P.Riso) + '"></label>' +
      '<label class="f">Ověřil (jméno, osvědčení)<input data-pm="who" value="' + esc(P.who) + '"></label><label class="f">Datum<input type="date" data-pm="date" value="' + esc(P.date) + '"></label></div>' +
      '<p class="hint">Mezní hodnoty: Riso ≥ 1 MΩ (500 V DC), RCD 30 mA vybavení ≤ 300 ms při IΔn. Naměřená Zs se porovnává s vypočtenou Zs max (bez korekce na teplotu – při měření za studena doporučeno ≤ 2/3 Zs max).</p>' +
      '<button data-act="printProto" class="primary">🖶 Tisk protokolu</button></div>';
    $('#protoOut').innerHTML = h;
  }
  $('#protoOut').addEventListener('change', e => {
    const P = B.proto;
    if (e.target.dataset.pc) P.checks[e.target.dataset.pc] = e.target.value;
    if (e.target.dataset.pm) P[e.target.dataset.pm] = e.target.value;
    if (e.target.dataset.me) { const d = B.devices.find(x => x.id === e.target.closest('tr').dataset.id); d.circuit.meas = d.circuit.meas || {}; d.circuit.meas[e.target.dataset.me] = e.target.value; }
    update();
  });

  // ---------- CSV ----------
  const CSV_COLS = ['row', 'bmk', 'type', 'poles', 'In', 'char', 'Icn', 'IdN', 'rcdType', 'parentBmk', 'label', 'name', 'kind', 'P', 'cos', 'ks', 'phase', 'cable', 'S', 'Spe', 'len', 'method', 'group', 'temp'];
  function toCSV() {
    const lines = [CSV_COLS.join(';')];
    for (const d of B.devices) {
      const c = d.circuit || {}, p = B.devices.find(x => x.id === d.parent);
      const v = { row: d.row, bmk: d.bmk, type: d.type, poles: d.poles, In: d.In, char: d.char, Icn: d.Icn, IdN: d.IdN, rcdType: d.rcdType, parentBmk: p ? p.bmk : '', label: d.label,
        name: c.name, kind: c.kind, P: c.P, cos: c.cos, ks: c.ks, phase: c.phase, cable: c.cable, S: c.S, Spe: c.Spe, len: c.len, method: c.method, group: c.group, temp: c.temp };
      lines.push(CSV_COLS.map(k => { let s = v[k] == null ? '' : String(v[k]); if (typeof v[k] === 'number') s = s.replace('.', ','); return /[;"\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; }).join(';'));
    }
    return '﻿' + lines.join('\r\n');
  }
  function parseCSV(txt) {
    txt = txt.replace(/^﻿/, '');
    const rows = []; let cur = [''], q = false;
    for (let i = 0; i < txt.length; i++) {
      const ch = txt[i];
      if (q) { if (ch === '"') { if (txt[i + 1] === '"') { cur[cur.length - 1] += '"'; i++; } else q = false; } else cur[cur.length - 1] += ch; }
      else if (ch === '"') q = true;
      else if (ch === ';' || ch === '\t') cur.push('');
      else if (ch === '\n') { rows.push(cur); cur = ['']; }
      else if (ch !== '\r') cur[cur.length - 1] += ch;
    }
    if (cur.length > 1 || cur[0]) rows.push(cur);
    const head = rows.shift().map(s => s.trim());
    const devs = [], byBmk = {};
    for (const r of rows) {
      const o = {}; head.forEach((h, i) => o[h] = (r[i] || '').trim());
      if (!o.type || !D.DEVICE_TYPES[o.type]) continue;
      const n = s => C.num(s);
      const d = D.dev(o.type, { row: n(o.row) || 1, bmk: o.bmk, poles: n(o.poles) || D.DEVICE_TYPES[o.type].poles[0], In: n(o.In) || 16, char: o.char || 'B', Icn: n(o.Icn) || 6, IdN: n(o.IdN) || 30, rcdType: o.rcdType || 'A', label: o.label || '' });
      if (d.circuit) Object.assign(d.circuit, { name: o.name, kind: o.kind || 'other', P: n(o.P), cos: n(o.cos) || 1, ks: o.ks === '' ? null : n(o.ks), phase: o.phase || 'L1', cable: o.cable, S: n(o.S) || 2.5, Spe: n(o.Spe) || n(o.S) || 2.5, len: n(o.len), method: o.method || 'C', group: n(o.group) || 1, temp: n(o.temp) || 30 });
      d._pb = o.parentBmk; devs.push(d); if (d.bmk) byBmk[d.bmk] = d;
    }
    devs.forEach(d => { if (d._pb && byBmk[d._pb]) d.parent = byBmk[d._pb].id; delete d._pb; });
    return devs;
  }

  // ---------- akce ----------
  const fileIn = $('#fileIn'); let fileMode = 'json';
  fileIn.addEventListener('change', () => {
    const f = fileIn.files[0]; if (!f) return;
    const rd = new FileReader();
    rd.onload = () => {
      try {
        if (fileMode === 'csv' || /\.(csv|txt)$/i.test(f.name)) {
          const devs = parseCSV(rd.result);
          if (!devs.length) throw new Error('V CSV nejsou žádné řádky s platným sloupcem „type“.');
          B.devices = devs; flash('Načteno ' + devs.length + ' přístrojů z CSV');
        } else {
          const nb = JSON.parse(rd.result); if (!nb.meta || !Array.isArray(nb.devices)) throw new Error('Soubor není projekt rozváděče.');
          B = nb; B.meta = Object.assign(D.newBoard().meta, B.meta); flash('Otevřeno: ' + f.name);
        }
        sel = null; renderBoard(); update();
      } catch (err) { alert('Chyba načtení: ' + err.message); }
      fileIn.value = '';
    };
    rd.readAsText(f, 'utf-8');
  });
  document.querySelector('.bar').addEventListener('click', e => act(e.target.dataset.act));
  $('#addbar').addEventListener('click', e => act(e.target.dataset.act));
  $('#protoOut').addEventListener('click', e => act(e.target.dataset.act));
  function act(a) {
    if (!a) return;
    if (a === 'new') { if (confirm('Založit nový prázdný rozváděč? Neuložené změny se ztratí.')) { B = D.templateEmpty(); sel = null; renderBoard(); update(); } }
    if (a === 'tpl') { if (confirm('Načíst vzorový rozváděč rodinného domu? Aktuální projekt se přepíše.')) { B = D.templateRD(); sel = null; renderBoard(); update(); } }
    if (a === 'open') { fileMode = 'json'; fileIn.accept = '.json'; fileIn.click(); }
    if (a === 'csvin') { fileMode = 'csv'; fileIn.accept = '.csv,.txt'; fileIn.click(); }
    if (a === 'save') download(fname('.json'), JSON.stringify(B, null, 1), 'application/json');
    if (a === 'csv') download(fname('_okruhy.csv'), toCSV(), 'text/csv;charset=utf-8');
    if (a === 'print' || a === 'printProto') {
      if (a === 'printProto') switchTab('proto');
      document.querySelectorAll('.tab').forEach(t => t.classList.toggle('printing', t.id === 'tab-' + tab));
      window.print();
    }
    if (a === 'balance') { C.balance(B); flash('Fáze přerozděleny'); update(); }
    if (a === 'renum') { C.renumber(B); flash('BMK přečíslována'); update(); }
    if (a === 'autoS') {
      let n = 0;
      for (const d of B.devices.filter(d => d.circuit)) { const s = C.suggestS(B, d); if (s && s !== d.circuit.S) { d.circuit.S = s; d.circuit.Spe = s <= 16 ? s : Math.max(16, s / 2); syncCableName(d); n++; } }
      flash(n ? 'Upraveno průřezů: ' + n : 'Průřezy vyhovují'); update();
    }
  }
  function flash(s) { const el = $('#status'); el.textContent = s; clearTimeout(flash.t); flash.t = setTimeout(() => { el.textContent = ''; }, 3500); }

  // ---------- záložky ----------
  $('#tabs').addEventListener('click', e => { const t = e.target.dataset.tab; if (t) { switchTab(t); renderTab(); } });
  function switchTab(t) {
    tab = t;
    document.querySelectorAll('#tabs button').forEach(b => b.classList.toggle('on', b.dataset.tab === t));
    document.querySelectorAll('.tab').forEach(s => s.classList.toggle('on', s.id === 'tab-' + t));
  }
  function renderTab() {
    if (tab === 'devices') { renderDevices(); renderMini(); }
    if (tab === 'calc') renderCalc();
    if (tab === 'front') $('#frontOut').innerHTML = R.toSVG(R.front(B, {}));
    if (tab === 'sl') $('#slOut').innerHTML = R.toSVG(R.singleLine(B, calc));
    if (tab === 'ml') $('#mlOut').innerHTML = R.toSVG(R.multiLine(B, calc));
    if (tab === 'labels') {
      $('#labOut').innerHTML = R.toSVG(R.labelStrips(B), { mm: true });
      $('#plateOut').innerHTML = R.toSVG(R.nameplate(B, calc), { mm: true });
      $('#listOut').innerHTML = R.toSVG(R.circuitList(B, calc), { mm: true });
    }
    if (tab === 'proto') renderProto();
  }
  function update() {
    calc = C.board(B);
    persist();
    const nErr = calc.msgs.filter(m => m.lvl === 'err').length + Object.values(calc.circuits).filter(c => !c.ok).length;
    document.querySelector('[data-tab="calc"]').textContent = '3 · Výpočty ' + (nErr ? '✖ ' + nErr : '✔');
    renderTab();
  }

  $('#helpOut').innerHTML = `
<h2>Jak s programem pracovat</h2>
<ol>
<li><b>Rozváděč</b> – vyplňte soustavu, Ze (změřená impedance smyčky na přívodu), Ik3, velikost skříně (řady × moduly) a Pde z katalogu skříně. Údaje pro typový štítek.</li>
<li><b>Přístroje a vývody</b> – přidávejte přístroje tlačítky „+“. Nový přístroj se vloží za vybraný řádek. Jistič přiřaďte ke chrániči ve sloupci <i>Za chráničem</i>. Řada určuje, na které DIN liště přístroj sedí; pořadí v tabulce = pořadí zleva doprava. Kliknutím na přístroj v náhledu jej vyberete.</li>
<li><b>Výpočty</b> – Ib, Iz s přepočtem na teplotu a seskupení, Ib ≤ In ≤ Iz, I2 ≤ 1,45·Iz, úbytek napětí, Zs a Ik1 min, doba odpojení, požadavek RCD 30 mA, vypínací schopnost, zatížení chráničů, soudobost, RDF, ztrátový výkon vs. Pde, symetrie fází.</li>
<li><b>Pohled, Jednopólové, Vícepólové</b> – výkresy se generují automaticky. Export do <b>DXF</b> (AutoCAD, DraftSight, EPLAN import), SVG, PNG, nebo tisk.</li>
<li><b>Štítky</b> – popisové pruhy 1:1 nad přístroje, typový štítek dle EN 61439-1 čl. 6.1, výstražný štítek a seznam okruhů (na dvířka) – CZ / DE / EN.</li>
<li><b>Protokol</b> – kusové ověření dle EN 61439-1 čl. 11 s naměřenými hodnotami.</li>
</ol>
<h3>Překreslení stávajícího rozváděče</h3>
<p>Nejrychlejší je <b>Export CSV</b> → doplnit v Excelu (oddělovač středník, desetinná čárka) → <b>Import CSV</b>. Sloupec <code>type</code>: ${Object.keys(D.DEVICE_TYPES).map(k => '<code>' + k + '</code>').join(', ')}. Druh zátěže <code>kind</code>: ${Object.keys(D.LOAD_KINDS).map(k => '<code>' + k + '</code>').join(', ')}. Fáze <code>L1/L2/L3/L123</code>. <code>parentBmk</code> = označení chrániče, pod kterým vývod je.</p>
<h3>Ukládání</h3>
<p>Projekt se průběžně ukládá v prohlížeči (na tomto počítači). Pro archivaci a přenos použijte <b>Uložit (.json)</b> – soubor lze kdykoli znovu otevřít.</p>
<h3>Normy a předpisy</h3>
<table class="res"><thead><tr><th>Oblast</th><th>EU / CZ</th><th>DE</th></tr></thead><tbody>
<tr><td class="t">Rozváděče, štítek, oteplení, RDF</td><td class="t">ČSN EN IEC 61439-1, -2, -3</td><td class="t">DIN EN IEC 61439 (VDE 0660-600)</td></tr>
<tr><td class="t">Samočinné odpojení, RCD</td><td class="t">ČSN 33 2000-4-41 ed. 3</td><td class="t">DIN VDE 0100-410</td></tr>
<tr><td class="t">Ochrana proti nadproudům</td><td class="t">ČSN 33 2000-4-43</td><td class="t">DIN VDE 0100-430</td></tr>
<tr><td class="t">Zatížitelnost, úbytek napětí</td><td class="t">ČSN 33 2000-5-52 ed. 2</td><td class="t">DIN VDE 0100-520, VDE 0298-4, DIN 18015-1</td></tr>
<tr><td class="t">Přepětí (SPD)</td><td class="t">ČSN 33 2000-4-443, -5-534</td><td class="t">DIN VDE 0100-443, -534</td></tr>
<tr><td class="t">Revize / výchozí ověření</td><td class="t">ČSN 33 2000-6, ČSN 33 1500</td><td class="t">DIN VDE 0100-600, DGUV V3</td></tr>
<tr><td class="t">Značení vodičů, BMK</td><td class="t">ČSN EN 60445, ČSN EN IEC 81346</td><td class="t">DIN EN 60445, DIN EN IEC 81346</td></tr>
<tr><td class="t">Připojení k síti (DE)</td><td class="t">PNE 33 3302 (připojení ČEZ/EG.D/PRE)</td><td class="t">VDE-AR-N 4100, TAB des Netzbetreibers</td></tr>
</tbody></table>
<p class="hint">Upozornění: program je pomůcka pro návrh. Tabulkové hodnoty jsou převzaty z IEC 60364-5-52 a typických katalogových údajů; před realizací ověřte vůči platnému vydání norem, podmínkám distributora a katalogům výrobců přístrojů. Odpovědnost za návrh a revizi nese oprávněná osoba.</p>`;

  renderBoard(); update();
})();
