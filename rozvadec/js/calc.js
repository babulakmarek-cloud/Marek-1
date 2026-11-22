/* Výpočty rozváděče: Ib, Iz, ΔU, Zs/Ik1, doba odpojení, zkrat, soudobost, oteplení, symetrie fází.
 * Normy (CZ = ČSN, DE = DIN VDE, EU = EN/HD):
 *  - ČSN 33 2000-4-41 / DIN VDE 0100-410 (HD 60364-4-41) – samočinné odpojení, doplňková ochrana RCD
 *  - ČSN 33 2000-4-43 / DIN VDE 0100-430 – Ib ≤ In ≤ Iz, I2 ≤ 1,45·Iz
 *  - ČSN 33 2000-5-52 / DIN VDE 0100-520 – zatížitelnost, úbytek napětí
 *  - ČSN EN 61439-1/-2/-3 / DIN EN 61439 (VDE 0660-600) – RDF, oteplení, štítek
 */
(function (root) {
  'use strict';
  const D = root.RData || (typeof require !== 'undefined' ? require('./data.js') : null);

  const RHO = 0.0225;      // Ω·mm²/m, Cu při 70 °C (1,25 × ρ20)
  const X_PER_M = 0.08e-3; // Ω/m, reaktance kabelu
  const CMIN = 0.95;       // napěťový činitel pro Ik min
  const SQ3 = Math.sqrt(3);

  const num = (v, d) => { const n = parseFloat(String(v).replace(',', '.')); return isFinite(n) ? n : (d === undefined ? 0 : d); };

  function phasesOf(dv) {
    if (!dv.circuit) return 1;
    return (dv.poles >= 3 || dv.circuit.phase === 'L123') ? 3 : 1;
  }

  function nearestKey(table, v) {
    const keys = Object.keys(table).map(Number).sort((a, b) => a - b);
    let best = keys[0];
    for (const k of keys) { if (k <= v) best = k; }
    return best;
  }
  function kTemp(t) {
    // lineární interpolace
    const keys = Object.keys(D.K_TEMP).map(Number).sort((a, b) => a - b);
    t = num(t, 30);
    if (t <= keys[0]) return D.K_TEMP[keys[0]];
    for (let i = 1; i < keys.length; i++) {
      if (t <= keys[i]) {
        const a = keys[i - 1], b = keys[i];
        return D.K_TEMP[a] + (D.K_TEMP[b] - D.K_TEMP[a]) * (t - a) / (b - a);
      }
    }
    return D.K_TEMP[keys[keys.length - 1]];
  }
  function kGroup(n) {
    n = Math.max(1, Math.round(num(n, 1)));
    // pro n mezi tabulkovými hodnotami bereme nejbližší vyšší počet (konzervativně)
    const keys = Object.keys(D.K_GROUP).map(Number).sort((a, b) => a - b);
    for (const k of keys) if (n <= k) return D.K_GROUP[k];
    return D.K_GROUP[keys[keys.length - 1]];
  }

  function izBase(S, method, loaded) {
    const i = D.SECTIONS.indexOf(num(S));
    if (i < 0) return null;
    const t = D.IZ[loaded >= 3 ? 3 : 2][method] || D.IZ[loaded >= 3 ? 3 : 2].C;
    return t[i];
  }

  function iz(c, ph) {
    const base = izBase(c.S, c.method, ph === 3 ? 3 : 2);
    if (base == null) return null;
    return base * kTemp(c.temp) * kGroup(c.group);
  }

  function ib(c, ph, meta) {
    const P = num(c.P) * 1000, cos = num(c.cos, 1) || 1;
    return ph === 3 ? P / (SQ3 * num(meta.Un, 400) * cos) : P / (num(meta.U0, 230) * cos);
  }

  function dU(c, ph, I, meta) {
    const L = num(c.len), S = num(c.S, 1.5) || 1.5, cos = num(c.cos, 1) || 1;
    const sin = Math.sqrt(Math.max(0, 1 - cos * cos));
    const R = RHO * L / S, X = X_PER_M * L;
    if (ph === 3) { const v = SQ3 * I * (R * cos + X * sin); return { V: v, pct: 100 * v / num(meta.Un, 400) }; }
    const v = 2 * I * (R * cos + X * sin);
    return { V: v, pct: 100 * v / num(meta.U0, 230) };
  }

  function loopZ(c, meta) {
    const L = num(c.len), S = num(c.S, 1.5) || 1.5, Spe = num(c.Spe, S) || S;
    return num(meta.Ze, 0.3) + RHO * L / S + RHO * L / Spe;
  }

  // vypínací proud Ia a požadovaná doba odpojení
  function tripCurrent(dv, meta) {
    const In = num(dv.In);
    const tReq = (In <= 32) ? 0.4 : 5; // koncové obvody ≤ 32 A: 0,4 s (TN, 230 V); rozvodné: 5 s
    if (dv.type === 'fuse') {
      const k = nearestKey(D.FUSE_GG, In);
      const row = D.FUSE_GG[k];
      return { Ia: tReq === 0.4 ? row[1] : row[0], tReq, how: 'gG ' + k + ' A (orientačně)' };
    }
    if (dv.type === 'contactor') return { Ia: null, tReq, how: 'stykač – ochranu zajišťuje předřazený přístroj' };
    const f = { B: 5, C: 10, D: 20, K: 14, Z: 3 }[dv.char] || 5;
    return { Ia: f * In, tReq, how: dv.char + ' → ' + f + '×In' };
  }

  function findParent(board, dv) { return board.devices.find(x => x.id === dv.parent) || null; }

  /** Výpočet jednoho vývodu */
  function circuit(board, dv) {
    const meta = board.meta, c = dv.circuit, res = { id: dv.id, msgs: [], ok: true };
    if (!c) return null;
    const warn = (m) => res.msgs.push({ lvl: 'warn', m });
    const err = (m) => { res.msgs.push({ lvl: 'err', m }); res.ok = false; };
    const ph = phasesOf(dv);
    const kind = D.LOAD_KINDS[c.kind] || D.LOAD_KINDS.other;
    res.ph = ph;
    res.ks = c.ks == null || c.ks === '' ? kind.ks : num(c.ks, kind.ks);
    res.Ib = ib(c, ph, meta);
    res.In = num(dv.In);
    res.IzBase = izBase(c.S, c.method, ph === 3 ? 3 : 2);
    res.kT = kTemp(c.temp); res.kG = kGroup(c.group);
    res.Iz = iz(c, ph);

    // 1) Ib ≤ In ≤ Iz
    if (res.Iz == null) err('Neznámý průřez ' + c.S + ' mm² (tabulka: ' + D.SECTIONS.join(', ') + ')');
    if (res.Ib > res.In) err('Ib ' + res.Ib.toFixed(1) + ' A > In ' + res.In + ' A – přístroj je poddimenzovaný');
    if (res.Iz != null) {
      // I2: jistič 1,45·In; gG ≥16 A 1,6·In (pod 16 A 1,9·In)
      const k2 = dv.type === 'fuse' ? (res.In >= 16 ? 1.6 : 1.9) : 1.45;
      res.I2 = k2 * res.In;
      if (res.In > res.Iz) err('In ' + res.In + ' A > Iz ' + res.Iz.toFixed(1) + ' A – kabel není chráněn proti přetížení');
      else if (res.I2 > 1.45 * res.Iz + 1e-9) err('I2 ' + res.I2.toFixed(1) + ' A > 1,45·Iz ' + (1.45 * res.Iz).toFixed(1) + ' A');
    }

    // 2) úbytek napětí
    const du = dU(c, ph, res.Ib, meta);
    res.dU = du.pct; res.dUV = du.V;
    res.dUtot = du.pct + num(meta.dUfeed, 0);
    const lim = c.kind === 'sv' ? 3 : 5;
    res.dULim = lim;
    if (res.dUtot > lim) warn('Celkový úbytek ' + res.dUtot.toFixed(2) + ' % > ' + lim + ' % (ČSN 33 2000-5-52 příl. G; DE: DIN 18015-1 / TAB 3 % za elektroměrem)');

    // 3) samočinné odpojení – Zs, Ik1
    res.Zs = loopZ(c, meta);
    res.Ik1 = CMIN * num(meta.U0, 230) / res.Zs;
    const tr = tripCurrent(dv, meta);
    res.Ia = tr.Ia; res.tReq = tr.tReq; res.iaHow = tr.how;
    const rcd = dv.type === 'rcbo' ? dv : (findParent(board, dv) && D.DEVICE_TYPES[findParent(board, dv).type].rcd ? findParent(board, dv) : null);
    res.rcd = rcd ? (rcd.IdN + ' mA typ ' + rcd.rcdType + (rcd === dv ? '' : ' (' + (rcd.bmk || 'RCD') + ')')) : '';
    res.ZsMax = res.Ia ? CMIN * num(meta.U0, 230) / res.Ia : null;
    if (meta.network === 'TT') {
      if (!rcd) err('Soustava TT: vývod musí být chráněn proudovým chráničem');
      else if (num(meta.Ze) * num(rcd.IdN) / 1000 > 50) err('TT: RA·IΔn = ' + (num(meta.Ze) * rcd.IdN / 1000).toFixed(1) + ' V > 50 V');
      res.discOk = !!rcd;
    } else if (res.Ia) {
      res.discOk = res.Ik1 >= res.Ia;
      if (!res.discOk) {
        if (rcd) warn('Ik1 ' + res.Ik1.toFixed(0) + ' A < Ia ' + res.Ia.toFixed(0) + ' A – odpojení zajištěno jen chráničem ' + res.rcd);
        else err('Ik1 ' + res.Ik1.toFixed(0) + ' A < Ia ' + res.Ia.toFixed(0) + ' A – nesplněna doba odpojení ' + res.tReq + ' s (Zs ' + res.Zs.toFixed(2) + ' Ω > ' + res.ZsMax.toFixed(2) + ' Ω)');
      }
    }

    // 4) doplňková ochrana RCD ≤ 30 mA
    if (kind.rcdReq && (!rcd || num(rcd.IdN) > 30)) err('Chybí doplňková ochrana RCD ≤ 30 mA (zásuvky ≤ 32 A, ČSN 33 2000-4-41 čl. 411.3.3 / VDE 0100-410)');
    if (!rcd && c.kind === 'sv') warn('DE: v bytech RCD 30 mA i pro světelné obvody (DIN VDE 0100-410:2018-10)');
    if (c.kind === 'ev' && rcd && rcd.rcdType === 'A') warn('Wallbox: RCD typ A jen s detekcí DC 6 mA ve wallboxu, jinak typ B');

    // 5) vypínací schopnost
    if (dv.type !== 'contactor' && dv.type !== 'fuse' && num(dv.Icn) < num(meta.Ik3)) warn('Icn ' + dv.Icn + ' kA < Ik3 ' + meta.Ik3 + ' kA na přípojnici – nutné jištění předřazením (back-up) dle výrobce');

    // 6) selektivita s předřazeným
    const main = board.devices.find(x => x.type === 'main');
    const up = (findParent(board, dv) && findParent(board, dv).type !== 'rcd') ? findParent(board, dv) : null;
    if (up && num(up.In) <= res.In) warn('In ' + res.In + ' A ≥ předřazený ' + up.In + ' A – neselektivní');
    if (main && num(main.In) < res.In) warn('In ' + res.In + ' A > hlavní vypínač ' + main.In + ' A');
    res.phase = ph === 3 ? 'L1L2L3' : c.phase;
    return res;
  }

  function rdfFor(std, n) {
    const t = D.RDF[std] || D.RDF['61439-3'];
    for (const [max, f] of t) if (n <= max) return f;
    return t[t.length - 1][1];
  }

  /** Výpočet celého rozváděče */
  function board(b) {
    const meta = b.meta;
    const circuits = {}, out = { circuits, msgs: [], phases: { L1: 0, L2: 0, L3: 0 }, phasesP: { L1: 0, L2: 0, L3: 0 } };
    const outs = b.devices.filter(d => d.circuit);
    for (const d of outs) circuits[d.id] = circuit(b, d);
    out.nCircuits = outs.length;
    out.RDF = rdfFor(meta.standard, outs.length);

    let Pinst = 0, Psim = 0;
    for (const d of outs) {
      const r = circuits[d.id], c = d.circuit, P = num(c.P);
      Pinst += P; Psim += P * r.ks;
      const Iks = r.Ib * r.ks;
      if (r.ph === 3) { for (const p of ['L1', 'L2', 'L3']) { out.phases[p] += Iks; out.phasesP[p] += P * r.ks / 3; } }
      else { const p = ['L1', 'L2', 'L3'].includes(c.phase) ? c.phase : 'L1'; out.phases[p] += Iks; out.phasesP[p] += P * r.ks; }
    }
    out.Pinst = Pinst; out.Psim = Psim;
    const Iv = Object.values(out.phases);
    out.Imax = Math.max(...Iv); out.Imin = Math.min(...Iv);
    out.unbalance = out.Imax > 0 ? 100 * (out.Imax - out.Imin) / out.Imax : 0;
    if (out.unbalance > 30 && out.Imax > 5) out.msgs.push({ lvl: 'warn', m: 'Nesymetrie fází ' + out.unbalance.toFixed(0) + ' % – zvažte přerozdělení (tlačítko „Vyvážit fáze“)' });

    const main = b.devices.find(d => d.type === 'main');
    out.InA = main ? num(main.In) : null;
    if (main && out.Imax > num(main.In)) out.msgs.push({ lvl: 'err', m: 'Soudobý proud ' + out.Imax.toFixed(1) + ' A > hlavní vypínač ' + main.In + ' A' });
    if (!main) out.msgs.push({ lvl: 'warn', m: 'Rozváděč nemá hlavní vypínač' });

    // zatížení chráničů
    out.rcdLoad = {};
    for (const r of b.devices.filter(d => d.type === 'rcd')) {
      const ch = { L1: 0, L2: 0, L3: 0 };
      for (const d of outs.filter(x => x.parent === r.id)) {
        const rr = circuits[d.id], I = rr.Ib * rr.ks;
        if (rr.ph === 3) { ch.L1 += I; ch.L2 += I; ch.L3 += I; } else ch[d.circuit.phase] = (ch[d.circuit.phase] || 0) + I;
      }
      const m = Math.max(ch.L1, ch.L2, ch.L3);
      out.rcdLoad[r.id] = m;
      if (m > num(r.In)) out.msgs.push({ lvl: 'err', m: (r.bmk || 'RCD') + ': soudobý proud ' + m.toFixed(1) + ' A > In ' + r.In + ' A' });
      if (r.poles === 2 && outs.some(x => x.parent === r.id && phasesOf(x) === 3)) out.msgs.push({ lvl: 'err', m: (r.bmk || 'RCD') + ': 2pólový chránič nemůže chránit 3f vývod' });
      const n = outs.filter(x => x.parent === r.id).length;
      if (n > 6) out.msgs.push({ lvl: 'warn', m: (r.bmk || 'RCD') + ': ' + n + ' vývodů za jedním chráničem – riziko nežádoucího vybavení (doporučeno ≤ 4–6)' });
    }

    // ztrátový výkon (EN 61439-1 čl. 10.10.4 / IEC TR 60890)
    let Pv = 0;
    const pvList = [];
    for (const d of b.devices) {
      const t = D.DEVICE_TYPES[d.type];
      let load = 1;
      if (d.circuit) load = Math.min(1.2, circuits[d.id].Ib * circuits[d.id].ks / Math.max(1, num(d.In)));
      else if (d.type === 'rcd') load = Math.min(1.2, (out.rcdLoad[d.id] || 0) / Math.max(1, num(d.In)));
      else if (d.type === 'main') load = Math.min(1.2, out.Imax / Math.max(1, num(d.In)));
      else if (d.type === 'spacer') load = 0;
      const p = t.pv * (d.poles || 1) * load * load;
      Pv += p; pvList.push({ id: d.id, p });
    }
    out.Pv = Pv; out.pvList = pvList;
    if (num(meta.Pde) > 0 && Pv > num(meta.Pde)) out.msgs.push({ lvl: 'err', m: 'Ztrátový výkon ' + Pv.toFixed(1) + ' W > Pde skříně ' + meta.Pde + ' W (ověření oteplení EN 61439-3 čl. 10.10.4.2)' });

    // šířka řad
    out.rowWidth = {};
    for (const d of b.devices) out.rowWidth[d.row] = (out.rowWidth[d.row] || 0) + width(d);
    for (const [r, w] of Object.entries(out.rowWidth)) {
      if (w > num(meta.modules)) out.msgs.push({ lvl: 'err', m: 'Řada ' + r + ': ' + w + ' M > ' + meta.modules + ' M' });
      if (num(r) > num(meta.rows)) out.msgs.push({ lvl: 'err', m: 'Řada ' + r + ' neexistuje (skříň má ' + meta.rows + ' řady)' });
    }
    const used = b.devices.filter(d => d.type !== 'spacer').reduce((a, d) => a + width(d), 0);
    out.reserve = num(meta.rows) * num(meta.modules) - used;
    if (out.reserve < 0.2 * num(meta.rows) * num(meta.modules)) out.msgs.push({ lvl: 'warn', m: 'Rezerva místa ' + out.reserve + ' M (< 20 %) – doporučeno ponechat rezervu' });

    // duplicita BMK
    const seen = {};
    for (const d of b.devices) if (d.bmk) { if (seen[d.bmk]) out.msgs.push({ lvl: 'warn', m: 'Duplicitní označení ' + d.bmk }); seen[d.bmk] = 1; }

    out.ok = !out.msgs.some(m => m.lvl === 'err') && Object.values(circuits).every(c => c.ok);
    return out;
  }

  function width(d) { const t = D.DEVICE_TYPES[d.type]; return t ? t.w(d.poles || 1) : 1; }

  /** Navrhne nejmenší průřez splňující Iz, ΔU a odpojení */
  function suggestS(b, dv) {
    const orig = Object.assign({}, dv.circuit);
    let found = null;
    for (const S of D.SECTIONS) {
      dv.circuit.S = S; dv.circuit.Spe = S <= 16 ? S : Math.max(16, S / 2);
      const r = circuit(b, dv);
      const hardFail = r.msgs.some(m => m.lvl === 'err' && /Iz|I2|odpojení|průřez/.test(m.m));
      if (!hardFail && r.dUtot <= r.dULim) { found = S; break; }
    }
    Object.assign(dv.circuit, orig);
    return found;
  }

  /** Vyvážení 1f vývodů mezi fáze (greedy podle výkonu) */
  function balance(b) {
    const load = { L1: 0, L2: 0, L3: 0 };
    const outs = b.devices.filter(d => d.circuit);
    for (const d of outs) if (phasesOf(d) === 3) for (const p in load) load[p] += num(d.circuit.P) / 3;
    const single = outs.filter(d => phasesOf(d) === 1).sort((a, c) => num(c.circuit.P) * ks(c) - num(a.circuit.P) * ks(a));
    for (const d of single) {
      const p = Object.keys(load).sort((a, c) => load[a] - load[c])[0];
      d.circuit.phase = p; load[p] += num(d.circuit.P) * ks(d);
    }
    return load;
  }
  function ks(d) { const k = D.LOAD_KINDS[d.circuit.kind] || D.LOAD_KINDS.other; return d.circuit.ks == null || d.circuit.ks === '' ? k.ks : num(d.circuit.ks); }

  /** Automatické číslování BMK podle pořadí v řadách */
  function renumber(b) {
    const cnt = {};
    const order = [...b.devices].sort((a, c) => a.row - c.row || b.devices.indexOf(a) - b.devices.indexOf(c));
    for (const d of order) {
      const L = D.DEVICE_TYPES[d.type].bmk;
      if (!L) { d.bmk = ''; continue; }
      cnt[L] = (cnt[L] || 0) + 1; d.bmk = '-' + L + cnt[L];
    }
  }

  const api = { RHO, num, phasesOf, iz, izBase, ib, dU, loopZ, kTemp, kGroup, tripCurrent, circuit, board, rdfFor, width, suggestS, balance, renumber };
  root.RCalc = api;
  if (typeof module !== 'undefined') module.exports = api;
})(typeof window !== 'undefined' ? window : globalThis);
