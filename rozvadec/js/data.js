/* Katalog přístrojů, tabulky norem a šablony.
 * Hodnoty tabulek: IEC/ČSN EN 60364-5-52 (ČSN 33 2000-5-52), příloha B – Cu, PVC 70 °C, okolí 30 °C.
 * Ztrátové výkony přístrojů jsou TYPICKÉ hodnoty – pro oteplení dle EN 61439 použijte údaje výrobce.
 */
(function (root) {
  'use strict';

  // Proudová zatížitelnost Iz [A], Cu/PVC, 30 °C. Index = průřez.
  const SECTIONS = [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120];
  const IZ = {
    // 2 zatížené vodiče (1f)
    2: {
      A1: [14.5, 19.5, 26, 34, 46, 61, 80, 99, 119, 151, 182, 210],
      A2: [14, 18.5, 25, 32, 43, 57, 75, 92, 110, 139, 167, 192],
      B1: [17.5, 24, 32, 41, 57, 76, 101, 125, 151, 192, 232, 269],
      B2: [16.5, 23, 30, 38, 52, 69, 90, 111, 133, 168, 201, 232],
      C: [19.5, 27, 36, 46, 63, 85, 112, 138, 168, 213, 258, 299],
      E: [22, 30, 40, 51, 70, 94, 119, 148, 180, 232, 282, 328]
    },
    // 3 zatížené vodiče (3f)
    3: {
      A1: [13.5, 18, 24, 31, 42, 56, 73, 89, 108, 136, 164, 188],
      A2: [13, 17.5, 23, 29, 39, 52, 68, 83, 99, 125, 150, 172],
      B1: [15.5, 21, 28, 36, 50, 68, 89, 110, 134, 171, 207, 239],
      B2: [15, 20, 27, 34, 46, 62, 80, 99, 118, 149, 179, 206],
      C: [17.5, 24, 32, 41, 57, 76, 96, 119, 144, 184, 223, 259],
      E: [18.5, 25, 34, 43, 60, 80, 101, 126, 153, 196, 238, 276]
    }
  };
  const METHODS = {
    A1: 'A1 – vodiče v trubce v tepelně izolační stěně',
    A2: 'A2 – kabel v trubce v tepelně izolační stěně',
    B1: 'B1 – vodiče v trubce na/ve zdi',
    B2: 'B2 – kabel v trubce na/ve zdi',
    C: 'C – kabel přímo na/ve zdi (pod omítkou)',
    E: 'E – kabel ve volném vzduchu / na žlabu'
  };
  // Přepočet na teplotu okolí (PVC)
  const K_TEMP = { 10: 1.22, 15: 1.17, 20: 1.12, 25: 1.06, 30: 1.0, 35: 0.94, 40: 0.87, 45: 0.79, 50: 0.71, 55: 0.61 };
  // Seskupení – svazek (řada 1 tab. B.52.17)
  const K_GROUP = { 1: 1.0, 2: 0.8, 3: 0.7, 4: 0.65, 5: 0.6, 6: 0.57, 7: 0.54, 8: 0.52, 9: 0.5, 12: 0.45, 16: 0.41, 20: 0.38 };

  // Rated diversity factor (RDF) dle EN 61439-3 tab. 101 a EN 61439-2 tab. 101 (počet hlavních obvodů)
  const RDF = {
    '61439-3': [[1, 1.0], [3, 0.8], [5, 0.7], [9, 0.6], [Infinity, 0.5]],
    '61439-2': [[1, 1.0], [3, 0.9], [5, 0.8], [9, 0.7], [Infinity, 0.6]]
  };

  // Pojistky gG – orientační proud Ia pro odpojení 5 s a 0,4 s [A] (z charakteristik IEC 60269, ORIENTAČNÍ)
  const FUSE_GG = {
    2: [9.2, 16], 4: [19, 32], 6: [28, 47], 10: [46, 82], 16: [65, 107], 20: [85, 145],
    25: [110, 180], 32: [150, 265], 40: [190, 310], 50: [250, 460], 63: [320, 550],
    80: [425, 735], 100: [580, 1050], 125: [715, 1300], 160: [950, 1800]
  };

  /* Katalog typů přístrojů.
   * w = šířka v modulech (1 TE / 1 M = 17,5 mm), pv = typický ztrátový výkon na pól při In [W]
   */
  const DEVICE_TYPES = {
    main: { name: 'Hlavní vypínač', de: 'Hauptschalter', en: 'Main switch', poles: [3, 4, 2, 1], w: p => p, pv: 1.0, bmk: 'Q' },
    mcb: { name: 'Jistič', de: 'LS-Schalter', en: 'MCB', poles: [1, 2, 3, 4], w: p => p, pv: 2.2, bmk: 'F', circuit: true },
    rcbo: { name: 'Proudový chránič s jističem', de: 'FI/LS-Schalter', en: 'RCBO', poles: [2, 4], w: p => p, pv: 3.0, bmk: 'F', circuit: true, rcd: true },
    rcd: { name: 'Proudový chránič', de: 'FI-Schutzschalter', en: 'RCD', poles: [4, 2], w: p => p, pv: 1.5, bmk: 'F', rcd: true, group: true },
    fuse: { name: 'Pojistkový odpínač', de: 'Sicherungslasttrennschalter', en: 'Fuse switch', poles: [1, 3], w: p => p * 1.5, pv: 3.0, bmk: 'F', circuit: true },
    spd: { name: 'Přepěťová ochrana', de: 'Überspannungsschutz', en: 'SPD', poles: [4, 2], w: p => p, pv: 0.2, bmk: 'F' },
    contactor: { name: 'Stykač', de: 'Schütz', en: 'Contactor', poles: [2, 4], w: p => (p > 2 ? 2 : 1), pv: 2.0, bmk: 'Q', circuit: true },
    relay: { name: 'Impulzní relé / spínač', de: 'Stromstoßschalter', en: 'Impulse relay', poles: [1], w: () => 1, pv: 1.0, bmk: 'K' },
    meter: { name: 'Elektroměr', de: 'Zähler', en: 'Energy meter', poles: [4, 2], w: p => (p > 2 ? 4 : 1), pv: 2.0, bmk: 'P' },
    terminal: { name: 'Svorky', de: 'Klemmen', en: 'Terminals', poles: [5], w: () => 3, pv: 0.3, bmk: 'X' },
    psu: { name: 'Zdroj / transformátor', de: 'Netzteil / Trafo', en: 'Power supply', poles: [1], w: () => 2, pv: 3.0, bmk: 'T' },
    spacer: { name: 'Záslepka / rezerva', de: 'Reserve', en: 'Spare', poles: [1], w: () => 1, pv: 0, bmk: '' }
  };

  const LOAD_KINDS = {
    zas: { cz: 'Zásuvky', de: 'Steckdosen', en: 'Sockets', ks: 0.3, cos: 0.95, rcdReq: true },
    sv: { cz: 'Světla', de: 'Beleuchtung', en: 'Lighting', ks: 0.8, cos: 0.95, rcdReq: false },
    spor: { cz: 'Sporák', de: 'Herd', en: 'Cooker', ks: 0.5, cos: 1.0, rcdReq: false },
    motor: { cz: 'Motor', de: 'Motor', en: 'Motor', ks: 0.8, cos: 0.85, rcdReq: false },
    tc: { cz: 'Tepelné čerpadlo', de: 'Wärmepumpe', en: 'Heat pump', ks: 1.0, cos: 0.9, rcdReq: false },
    ev: { cz: 'Wallbox', de: 'Wallbox', en: 'EV charger', ks: 1.0, cos: 1.0, rcdReq: true },
    pv: { cz: 'Fotovoltaika', de: 'PV-Anlage', en: 'PV system', ks: 1.0, cos: 1.0, rcdReq: false },
    other: { cz: 'Ostatní', de: 'Sonstiges', en: 'Other', ks: 0.7, cos: 0.95, rcdReq: false }
  };

  const NETWORKS = ['TN-C-S', 'TN-S', 'TN-C', 'TT'];

  // Texty pro štítky ve třech jazycích
  const L = {
    cz: {
      manufacturer: 'Výrobce rozváděče', type: 'Typ / označení', serial: 'Výrobní číslo', date: 'Datum výroby',
      standard: 'Norma', Un: 'Jmenovité napětí Un', Ui: 'Izolační napětí Ui', Uimp: 'Impulzní výdržné napětí Uimp',
      InA: 'Jmenovitý proud rozváděče InA', fn: 'Kmitočet fn', Icc: 'Podmíněný zkratový proud Icc', Icw: 'Krátkodobý výdržný proud Icw',
      RDF: 'Činitel soudobosti RDF', IP: 'Krytí', IK: 'Mechanická odolnost', network: 'Soustava', weight: 'Hmotnost',
      plate: 'TYPOVÝ ŠTÍTEK ROZVÁDĚČE', warn: 'Pozor! Elektrické zařízení', warn2: 'Nepovolaným vstup zakázán',
      board: 'Rozváděč', indoor: 'pro vnitřní použití', ordinary: 'obsluha laiky (DBO)', skilled: 'obsluha osobami znalými (PSC)'
    },
    de: {
      manufacturer: 'Hersteller der Schaltgerätekombination', type: 'Typ / Kennzeichnung', serial: 'Seriennummer', date: 'Herstelldatum',
      standard: 'Norm', Un: 'Bemessungsspannung Un', Ui: 'Bemessungsisolationsspannung Ui', Uimp: 'Bemessungsstoßspannung Uimp',
      InA: 'Bemessungsstrom InA', fn: 'Bemessungsfrequenz fn', Icc: 'Bedingter Kurzschlussstrom Icc', Icw: 'Kurzzeitstromfestigkeit Icw',
      RDF: 'Bemessungsbelastungsfaktor RDF', IP: 'Schutzart', IK: 'Stoßfestigkeit', network: 'Netzform', weight: 'Gewicht',
      plate: 'TYPENSCHILD', warn: 'Warnung vor elektrischer Spannung', warn2: 'Zutritt für Unbefugte verboten',
      board: 'Verteiler', indoor: 'für Innenraum', ordinary: 'Bedienung durch Laien (DBO)', skilled: 'Bedienung durch Fachkräfte (PSC)'
    },
    en: {
      manufacturer: 'Assembly manufacturer', type: 'Type designation', serial: 'Serial number', date: 'Date of manufacture',
      standard: 'Standard', Un: 'Rated voltage Un', Ui: 'Rated insulation voltage Ui', Uimp: 'Rated impulse withstand voltage Uimp',
      InA: 'Rated current of assembly InA', fn: 'Rated frequency fn', Icc: 'Rated conditional short-circuit current Icc', Icw: 'Rated short-time withstand current Icw',
      RDF: 'Rated diversity factor RDF', IP: 'Degree of protection', IK: 'Impact protection', network: 'Earthing system', weight: 'Weight',
      plate: 'RATING PLATE', warn: 'Danger – electricity', warn2: 'No unauthorised access',
      board: 'Distribution board', indoor: 'indoor use', ordinary: 'operation by ordinary persons (DBO)', skilled: 'operation by skilled persons (PSC)'
    }
  };

  let _id = 1;
  const nid = () => 'd' + (Date.now().toString(36)) + (_id++);

  function dev(type, o) {
    const t = DEVICE_TYPES[type];
    const d = Object.assign({
      id: nid(), type, poles: t.poles[0], In: 16, char: 'B', Icn: 6, IdN: 30, rcdType: 'A',
      bmk: '', row: 1, parent: '', label: '',
      circuit: null
    }, o || {});
    if (t.circuit && !d.circuit) d.circuit = newCircuit();
    if (d.circuit) d.circuit = Object.assign(newCircuit(), d.circuit);
    return d;
  }
  function newCircuit(o) {
    return Object.assign({
      name: '', kind: 'zas', P: 2.0, cos: 0.95, ks: null, phase: 'L1',
      cable: 'CYKY-J 3x2,5', S: 2.5, Spe: 2.5, len: 20, method: 'C', group: 1, temp: 30
    }, o || {});
  }

  function newBoard() {
    return {
      meta: {
        name: 'Rozváděč RD1', bmk: '=RD1', location: '', project: '', manufacturer: '', type: '', serial: '',
        date: new Date().toISOString().slice(0, 10), standard: '61439-3', network: 'TN-C-S',
        Un: 400, U0: 230, fn: 50, Ui: 440, Uimp: 4, IP: 'IP40', IK: 'IK07', Icc: 6, weight: '',
        Ze: 0.3, Ik3: 6, rows: 3, modules: 12, Pde: 30, dUfeed: 0.5, lang: 'cz', author: ''
      },
      devices: []
    };
  }

  // Šablona: byt / RD – 3 řady po 12 M
  function templateRD() {
    const b = newBoard();
    b.meta.name = 'Rozváděč RD – rodinný dům';
    const q = dev('main', { bmk: '-Q1', poles: 3, In: 40, row: 1, label: 'Hlavní vypínač' });
    const spd = dev('spd', { bmk: '-F1', poles: 4, In: 25, row: 1, label: 'SPD T1+T2' });
    const r1 = dev('rcd', { bmk: '-F2', poles: 4, In: 40, IdN: 30, row: 2, label: 'Chránič A' });
    const r2 = dev('rcd', { bmk: '-F3', poles: 4, In: 40, IdN: 30, row: 3, label: 'Chránič B' });
    const c = (bmk, row, parent, In, char, circuit, poles) => dev('mcb', { bmk, row, parent: parent.id, In, char, poles: poles || 1, circuit: newCircuit(circuit) });
    b.devices = [
      q, spd,
      dev('mcb', { bmk: '-F4', row: 1, poles: 3, In: 16, char: 'B', circuit: newCircuit({ name: 'Sporák', kind: 'spor', P: 9, cos: 1, phase: 'L123', cable: 'CYKY-J 5x2,5', S: 2.5, Spe: 2.5, len: 12 }) }),
      dev('spacer', { row: 1 }), dev('spacer', { row: 1 }),
      r1,
      c('-F5', 2, r1, 10, 'B', { name: 'Světla přízemí', kind: 'sv', P: 0.6, phase: 'L1', cable: 'CYKY-J 3x1,5', S: 1.5, Spe: 1.5, len: 25 }),
      c('-F6', 2, r1, 16, 'B', { name: 'Zásuvky obývák', kind: 'zas', P: 2.5, phase: 'L2', len: 22 }),
      c('-F7', 2, r1, 16, 'B', { name: 'Zásuvky kuchyň', kind: 'zas', P: 3.0, phase: 'L3', len: 15 }),
      c('-F8', 2, r1, 16, 'B', { name: 'Myčka', kind: 'other', P: 2.2, phase: 'L1', len: 14 }),
      c('-F9', 2, r1, 16, 'B', { name: 'Pračka', kind: 'other', P: 2.3, phase: 'L2', len: 18 }),
      dev('spacer', { row: 2 }), dev('spacer', { row: 2 }), dev('spacer', { row: 2 }),
      r2,
      c('-F10', 3, r2, 10, 'B', { name: 'Světla patro', kind: 'sv', P: 0.5, phase: 'L3', cable: 'CYKY-J 3x1,5', S: 1.5, Spe: 1.5, len: 30 }),
      c('-F11', 3, r2, 16, 'B', { name: 'Zásuvky ložnice', kind: 'zas', P: 2.0, phase: 'L1', len: 28 }),
      c('-F12', 3, r2, 16, 'B', { name: 'Zásuvky koupelna', kind: 'zas', P: 2.0, phase: 'L2', len: 26 }),
      c('-F13', 3, r2, 16, 'B', { name: 'Venkovní zásuvky', kind: 'zas', P: 2.0, phase: 'L3', len: 35 }),
      dev('terminal', { bmk: '-X1', row: 3, label: 'N/PE' })
    ];
    return b;
  }

  function templateEmpty() {
    const b = newBoard();
    b.devices = [dev('main', { bmk: '-Q1', poles: 3, In: 40, row: 1, label: 'Hlavní vypínač' })];
    return b;
  }

  const api = { SECTIONS, IZ, METHODS, K_TEMP, K_GROUP, RDF, FUSE_GG, DEVICE_TYPES, LOAD_KINDS, NETWORKS, L, dev, newCircuit, newBoard, templateRD, templateEmpty };
  root.RData = api;
  if (typeof module !== 'undefined') module.exports = api;
})(typeof window !== 'undefined' ? window : globalThis);
