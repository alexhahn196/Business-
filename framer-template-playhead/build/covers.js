// Viewport captures for marketplace covers → previews/raw/, then composes covers from build/covers.html → previews/
const path = require('path'); const fs = require('fs');
const { chromium } = require(process.env.PW_MODULE || 'playwright');
(async () => {
  const root = path.resolve(__dirname, '..'); const raw = path.join(root, 'previews', 'raw'); fs.mkdirSync(raw, { recursive: true });
  const browser = await chromium.launch(process.env.PW_EXEC ? { executablePath: process.env.PW_EXEC } : {});
  const prep = async (page) => { await page.evaluate(() => Promise.all([document.fonts.load('700 20px "Bricolage Grotesque"'), document.fonts.load('400 16px "Inter"'), document.fonts.load('500 12px "JetBrains Mono"')]).then(() => document.fonts.ready)); await page.addStyleTag({ content: '.appear{opacity:1!important;transform:none!important;transition:none!important} .marquee-track{animation:none!important}' }); await page.waitForTimeout(250); };
  const desk = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
  const d = await desk.newPage();
  const shots = [
    ['index', 0, 'home-hero'], ['index', '#showreel', 'home-showreel'], ['index', '.reels', 'home-reels'], ['index', '.pricing', 'home-pricing'],
    ['work', 0, 'work'], ['project', 0, 'project'], ['services', '.pricing', 'services'], ['about', 0, 'about'], ['contact', 0, 'contact'], ['404', 0, '404'],
  ];
  for (const [p, target, name] of shots) {
    await d.goto('file://' + path.join(root, 'site', p + '.html'), { waitUntil: 'networkidle' }); await prep(d);
    if (target) { await d.evaluate((sel) => { const el = document.querySelector(sel); const y = el.getBoundingClientRect().top + window.scrollY - (sel === '.pricing' ? 230 : 120); document.documentElement.style.scrollBehavior = 'auto'; window.scrollTo({ top: y, behavior: 'instant' }); }, target); await d.waitForTimeout(500); }
    await d.screenshot({ path: path.join(raw, name + '.png'), type: 'png' });
  }
  await desk.close();
  const mob = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
  const m = await mob.newPage();
  for (const [p, target, name] of [['index', 0, 'm-home'], ['index', '.reels', 'm-reels'], ['work', 0, 'm-work'], ['project', 0, 'm-project'], ['services', '.pricing', 'm-services'], ['contact', 0, 'm-contact']]) {
    await m.goto('file://' + path.join(root, 'site', p + '.html'), { waitUntil: 'networkidle' }); await prep(m);
    if (target) { await m.evaluate((sel) => { const el = document.querySelector(sel); document.documentElement.style.scrollBehavior = 'auto'; window.scrollTo({ top: el.getBoundingClientRect().top + window.scrollY - 80, behavior: 'instant' }); }, target); await m.waitForTimeout(500); }
    await m.screenshot({ path: path.join(raw, name + '.png'), type: 'png' });
  }
  await mob.close();
  // compose covers
  const cov = await browser.newContext({ viewport: { width: 1700, height: 1300 }, deviceScaleFactor: 1 });
  const c = await cov.newPage();
  await c.goto('file://' + path.join(__dirname, 'covers.html'), { waitUntil: 'networkidle' });
  await c.evaluate(() => document.fonts.ready); await c.waitForTimeout(400);
  const ids = await c.$$eval('.cover', els => els.map(e => e.id));
  for (const id of ids) { const el = await c.$('#' + id); await el.screenshot({ path: path.join(root, 'previews', id + '.jpg'), type: 'jpeg', quality: 90 }); console.log('cover', id); }
  await cov.close(); await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
