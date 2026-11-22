// Spuštění: node test/ui.test.js [složka_pro_screenshoty]
const { chromium } = require('playwright');
const path = require('path'); const fs = require('fs');
const out = process.argv[2];
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1600, height: 1000 }, acceptDownloads: true });
  const errs = [];
  p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  p.on('dialog', d => d.accept());
  await p.goto('file://' + path.resolve(__dirname, process.env.PAGE || '../index.html'));
  const shot = async n => { if (out) await p.screenshot({ path: path.join(out, n + '.png') }); };
  await shot('ui_board');
  for (const t of ['devices', 'calc', 'front', 'sl', 'ml', 'labels', 'proto', 'help']) {
    await p.click('[data-tab="' + t + '"]'); await p.waitForTimeout(150); await shot('ui_' + t);
  }
  // přidání jističe a změna fáze
  await p.click('[data-tab="devices"]');
  const n0 = await p.locator('#devTable tbody tr').count();
  await p.click('[data-add="mcb"]');
  const n1 = await p.locator('#devTable tbody tr').count();
  if (n1 !== n0 + 1) throw new Error('přidání nefunguje');
  await p.locator('#devTable tr.sel [data-c="P"]').fill('3.5'); await p.locator('#devTable tr.sel [data-c="P"]').dispatchEvent('change');
  await p.click('[data-act="balance"]'); await p.click('[data-act="renum"]'); await p.click('[data-act="autoS"]');
  // export DXF + CSV + JSON
  for (const sel of ['[data-act="save"]', '[data-act="csv"]']) {
    const [dl] = await Promise.all([p.waitForEvent('download'), p.click(sel)]);
    const f = await dl.path(); console.log('download', dl.suggestedFilename(), fs.statSync(f).size, 'B');
    if (sel.includes('csv')) {
      // re-import CSV
      await p.setInputFiles('#fileIn', f); await p.waitForTimeout(200);
    }
  }
  await p.click('[data-tab="ml"]');
  const [dx] = await Promise.all([p.waitForEvent('download'), p.click('[data-dxf="multiLine"]')]);
  const dtxt = fs.readFileSync(await dx.path(), 'utf8'); if (!/EOF\s*$/.test(dtxt)) throw new Error('DXF neúplné');
  console.log('DXF', dx.suggestedFilename(), dtxt.length, 'B');
  await p.click('[data-tab="calc"]');
  console.log('tab výpočty:', await p.textContent('[data-tab="calc"]'));
  // persistence po reloadu
  await p.reload(); await p.click('[data-tab="devices"]');
  console.log('po reloadu řádků:', await p.locator('#devTable tbody tr').count(), '(očekáváno', n1 + ')');
  await b.close();
  if (errs.length) { console.error('CHYBY:', errs); process.exit(1); }
  console.log('UI test OK');
})();
