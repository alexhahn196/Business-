const path = require('path'); const fs = require('fs');
const { chromium } = require(process.env.PW_MODULE || 'playwright');
(async () => {
  const root = path.resolve(__dirname, '..'); const out = path.join(root, 'previews', 'qa'); fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch(process.env.PW_EXEC ? { executablePath: process.env.PW_EXEC } : {});
  const jobs = [
    ['index', 1440, 0, 900, 'crop-home-hero-1440'],
    ['index', 1000, 0, 1000, 'crop-home-hero-1000'],
    ['index', 390, 0, 1300, 'crop-home-hero-390'],
    ['work', 1440, 0, 1400, 'crop-work-1440'],
    ['work', 390, 0, 1400, 'crop-work-390'],
    ['services', 1440, 900, 1500, 'crop-services-1440'],
    ['contact', 1440, 0, 1200, 'crop-contact-1440'],
    ['contact', 390, 0, 1500, 'crop-contact-390'],
  ];
  for (const [p, w, y, h, name] of jobs) {
    const ctx = await browser.newContext({ viewport: { width: w, height: 900 }, deviceScaleFactor: w < 500 ? 2 : 1 });
    const page = await ctx.newPage();
    await page.goto('file://' + path.join(root, 'site', p + '.html'), { waitUntil: 'networkidle' });
    await page.evaluate(() => Promise.all([document.fonts.load('700 20px "Bricolage Grotesque"'), document.fonts.load('400 16px "Inter"'), document.fonts.load('500 12px "JetBrains Mono"')]).then(() => document.fonts.ready));
    await page.addStyleTag({ content: '.appear{opacity:1!important;transform:none!important;transition:none!important} .marquee-track{animation:none!important}' });
    await page.waitForTimeout(300);
    if (p === 'index' && w === 1440) {
      const ok = await page.evaluate(() => [document.fonts.check('700 20px "Bricolage Grotesque"'), document.fonts.check('400 16px "Inter"'), document.fonts.check('500 12px "JetBrains Mono"'), Array.from(document.fonts).filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight).slice(0, 12)]);
      console.log('fonts:', JSON.stringify(ok));
    }
    await page.screenshot({ path: path.join(out, name + '.jpg'), clip: { x: 0, y, width: w, height: h }, fullPage: true, type: 'jpeg', quality: 80 });
    console.log('crop', name);
    await ctx.close();
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
