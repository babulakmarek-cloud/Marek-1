// Spuštění: node test/calc.test.js
const assert = require('assert');
const D = require('../js/data.js');
globalThis.RData = D;
const C = require('../js/calc.js');
let n = 0; const t = (name, f) => { f(); n++; console.log('ok', name); };

t('Iz 2,5 mm² metoda C 2 vodiče = 27 A', () => assert.strictEqual(C.izBase(2.5, 'C', 2), 27));
t('kT 40 °C = 0,87, svazek 3 = 0,70', () => { assert.strictEqual(C.kTemp(40), 0.87); assert.strictEqual(C.kGroup(3), 0.7); });
t('Ib 1f 2,3 kW cos 1 = 10 A', () => assert.ok(Math.abs(C.ib({ P: 2.3, cos: 1 }, 1, { U0: 230 }) - 10) < 1e-9));
t('Ib 3f 11 kW cos 1 ≈ 15,9 A', () => assert.ok(Math.abs(C.ib({ P: 11, cos: 1 }, 3, { Un: 400 }) - 15.877) < 0.01));
t('ΔU 1f 10 A 20 m 2,5 mm² cos1 = 3,6 V', () => { const r = C.dU({ len: 20, S: 2.5, cos: 1 }, 1, 10, { U0: 230 }); assert.ok(Math.abs(r.V - 3.6) < 1e-6); });
t('Zs = Ze + 2ρL/S', () => assert.ok(Math.abs(C.loopZ({ len: 20, S: 2.5, Spe: 2.5 }, { Ze: 0.3 }) - (0.3 + 0.36)) < 1e-9));
t('Šablona RD: výpočet bez výjimky, sporák 3f', () => {
  const b = D.templateRD(); const r = C.board(b);
  const spor = b.devices.find(d => d.circuit && d.circuit.kind === 'spor');
  assert.strictEqual(r.circuits[spor.id].ph, 3);
  assert.ok(r.Pinst > 20 && r.RDF === 0.5);
});
t('B16 na 1,5 mm² metoda A1 (14,5 A) = chyba In > Iz', () => {
  const b = D.templateEmpty(); const d = D.dev('mcb', { In: 16, char: 'B', circuit: D.newCircuit({ S: 1.5, Spe: 1.5, kind: 'other', method: 'A1' }) }); b.devices.push(d);
  assert.ok(C.circuit(b, d).msgs.some(m => /Iz/.test(m.m)));
});
t('Zásuvky bez RCD = chyba', () => {
  const b = D.templateEmpty(); const d = D.dev('mcb', { circuit: D.newCircuit({ kind: 'zas' }) }); b.devices.push(d);
  assert.ok(!C.circuit(b, d).ok);
});
t('Dlouhý vývod C32 100 m 2,5 mm² neodpojí', () => {
  const b = D.templateEmpty(); const d = D.dev('mcb', { In: 32, char: 'C', circuit: D.newCircuit({ kind: 'motor', len: 100, S: 2.5, Spe: 2.5 }) }); b.devices.push(d);
  assert.ok(C.circuit(b, d).msgs.some(m => /doba odpojení/.test(m.m)));
});
t('Návrh průřezu B16, metoda A1 → 2,5 mm²', () => {
  const b = D.templateEmpty(); const d = D.dev('mcb', { In: 16, circuit: D.newCircuit({ kind: 'other', S: 1.5, len: 15, P: 2, method: 'A1' }) }); b.devices.push(d);
  assert.strictEqual(C.suggestS(b, d), 2.5);
});
t('Vyvážení fází', () => { const b = D.templateRD(); C.balance(b); const r = C.board(b); assert.ok(r.unbalance < 30, 'unb ' + r.unbalance); });
t('RDF 61439-2 pro 5 obvodů = 0,8', () => assert.strictEqual(C.rdfFor('61439-2', 5), 0.8));
console.log(n + ' testů OK');
