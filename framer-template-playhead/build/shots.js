// Full-page screenshots of every built page at three Framer breakpoints → previews/qa/
const path = require('path'); const fs = require('fs');
const { chromium } = require(process.env.PW_MODULE || 'playwright');
(async () => {
  const root = path.resolve(__dirname, '..'); const out = path.join(root, 'previews', 'qa'); fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch(process.env.PW_EXEC ? { executablePath: process.env.PW_EXEC } : {});
  const pages = (process.env.PAGES || 'index,work,project,services,about,contact,404,legal,start-here,lite').split(',');
  const widths = (process.env.WIDTHS || '1440,1000,390').split(',').map(Number);
  for (const w of widths) {
    const ctx = await browser.newContext({ viewport: { width: w, height: 900 }, deviceScaleFactor: w < 500 ? 2 : 1 });
    const page = await ctx.newPage();
    for (const p of pages) {
      await page.goto('file://' + path.join(root, 'site', p + '.html'), { waitUntil: 'networkidle' });
      await page.evaluate(() => Promise.all([document.fonts.load('700 20px "Bricolage Grotesque"'), document.fonts.load('400 16px "Inter"'), document.fonts.load('500 12px "JetBrains Mono"')]).then(() => document.fonts.ready));
      await page.addStyleTag({ content: '.appear{opacity:1!important;transform:none!important;transition:none!important} .marquee-track{animation:none!important}' });
      await page.waitForTimeout(300);
      await page.screenshot({ path: path.join(out, `${p}-${w}.jpg`), fullPage: true, type: 'jpeg', quality: 70 });
      console.log('shot', p, w);
    }
    await ctx.close();
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
