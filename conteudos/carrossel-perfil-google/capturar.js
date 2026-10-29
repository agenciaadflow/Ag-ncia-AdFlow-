// Tira o print 1080x1350 de cada HTML recebido, salvando um PNG ao lado
const { chromium } = require('playwright');
(async () => {
  const nav = await chromium.launch();
  const pg = await nav.newPage({ viewport: { width: 1080, height: 1350 } });
  for (const f of process.argv.slice(2)) {
    await pg.goto('file://' + f, { waitUntil: 'networkidle' });
    await pg.evaluate(() => document.fonts.ready);
    await pg.screenshot({ path: f.replace(/\.html$/, '.png') });
  }
  await nav.close();
})();
