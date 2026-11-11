// Generates share (Open Graph) images: node scripts/make_og.js items.json outdir
// Needs Playwright + Chromium and the Noto CJK fonts. Images are committed; the build only links them.
const {chromium} = require('playwright');
const fs = require('fs');
const [,, itemsPath, outDir] = process.argv;
const items = JSON.parse(fs.readFileSync(itemsPath, 'utf8'));
const esc = s => s.replace(/&/g,'&amp;').replace(/</g,'&lt;');
const html = it => `<!doctype html><html><head><meta charset="utf-8"><style>
*{margin:0;box-sizing:border-box}
body{width:1200px;height:630px;background:#1f2f5a;color:#f4f1ea;font-family:"Noto Sans CJK JP",sans-serif;position:relative;overflow:hidden}
.grain{position:absolute;inset:0;background:repeating-linear-gradient(90deg,rgba(255,255,255,.035) 0 1px,transparent 1px 64px),repeating-linear-gradient(0deg,rgba(255,255,255,.035) 0 1px,transparent 1px 64px)}
.bar{position:absolute;left:0;top:0;bottom:0;width:18px;background:#b9770e}
.k{position:absolute;right:56px;top:40px;bottom:120px;width:520px;display:flex;align-items:center;justify-content:center;
   font-family:"Noto Serif CJK JP",serif;font-weight:900;color:rgba(244,241,234,.95);line-height:1.05;text-align:center;writing-mode:horizontal-tb}
.txt{position:absolute;left:76px;top:70px;width:560px}
.en{font-family:"Noto Sans CJK JP",sans-serif;font-weight:700;font-size:54px;line-height:1.12;letter-spacing:-.5px}
.ja{margin-top:22px;font-size:32px;font-weight:500;color:#cfe3df}
.tag{margin-top:26px;font-size:24px;color:#c8c3b5}
.foot{position:absolute;left:76px;right:56px;bottom:44px;display:flex;align-items:center;gap:18px;font-size:26px;color:#f4f1ea}
.logo{width:56px;height:56px;border-radius:12px;background:#f4f1ea;color:#1f2f5a;display:flex;align-items:center;justify-content:center;font-family:"Noto Serif CJK JP",serif;font-weight:900;font-size:36px}
.url{margin-left:auto;color:#9fcbc4;font-size:24px}
</style></head><body><div class="grain"></div><div class="bar"></div>
<div class="txt"><div class="en">${esc(it.en)}</div><div class="ja">${esc(it.ja)}</div><div class="tag">${esc(it.tag)}</div></div>
<div class="k" id="k" style="${/[ァ-ヿ]/.test(it.k) ? "white-space:nowrap" : ""}">${esc(it.k)}</div>
<div class="foot"><div class="logo">武</div><div>Okinawa Martial Arts · 沖縄 武道・格闘技</div><div class="url">okinawamartialarts.com</div></div>
</body></html>`;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({viewport: {width: 1200, height: 630}});
  for (const it of items) {
    await p.setContent(html(it));
    // fit the big glyph block: largest size that fits 520x(630-160) in at most 2 lines
    await p.evaluate(() => {
      const k = document.getElementById('k'); let s = 300;
      k.style.fontSize = s + 'px';
      while (s > 60 && (k.scrollWidth > k.clientWidth || k.scrollHeight > k.clientHeight)) { s -= 6; k.style.fontSize = s + 'px'; }
    });
    // shrink English title if it runs too tall
    await p.evaluate(() => { const e = document.querySelector('.en'); let s = 54; while (s > 34 && e.getBoundingClientRect().height > 250) { s -= 2; e.style.fontSize = s + 'px'; } });
    await p.screenshot({path: `${outDir}/${it.key}.jpg`, type: "jpeg", quality: 86});
  }
  await b.close();
})();
