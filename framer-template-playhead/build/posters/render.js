// Renders each poster element in posters.html to a JPEG in site/assets/img (75% scale, q85 → small files).
// Usage: node build/posters/render.js   (env PW_MODULE / PW_EXEC optional)
const path = require('path');
const fs = require('fs');
const { chromium } = require(process.env.PW_MODULE || 'playwright');
(async () => {
  const root = path.resolve(__dirname, '..', '..');
  const out = path.join(root, 'site', 'assets', 'img');
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch(process.env.PW_EXEC ? { executablePath: process.env.PW_EXEC } : {});
  const page = await browser.newPage({ viewport: { width: 1700, height: 2100 }, deviceScaleFactor: 0.75 });
  await page.goto('file://' + path.join(__dirname, 'posters.html'), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(500);
  const ids = await page.$$eval('.p', els => els.map(e => e.id));
  for (const id of ids) {
    const el = await page.$('#' + id);
    await el.screenshot({ path: path.join(out, id + '.jpg'), type: 'jpeg', quality: 85 });
    console.log('rendered', id);
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
