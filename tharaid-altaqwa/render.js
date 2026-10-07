// Paginate an HTML page with Paged.js in Chromium and print it to PDF.
// usage: node render.js <in.html> <out.pdf> [--paged]
const path = require("path");
let pw;
try { pw = require("playwright"); } catch { pw = require("/opt/node22/lib/node_modules/playwright"); }

(async () => {
  const [src, out, mode] = process.argv.slice(2);
  const browser = await pw.chromium.launch();
  const page = await browser.newPage();
  page.on("console", m => { if (m.type() === "error") console.error("console:", m.text()); });
  page.on("pageerror", e => console.error("pageerror:", e.message));
  await page.goto("file://" + path.resolve(src), { waitUntil: "load" });
  if (mode === "--paged") {
    await page.waitForFunction(() => window.__done === true || window.__done === "error", null, { timeout: 900000, polling: 1000 });
    const n = await page.evaluate(() => window.__pages || window.__done);
    console.log("pages:", n);
    const ov = await page.evaluate(() => window.__overflow || []);
    if (ov.length) console.log("WARNING overflowing pages:", ov.join(", "));
    const ch = await page.evaluate(() => JSON.stringify(window.__chapters || []));
    require("fs").writeFileSync(path.resolve(path.dirname(out), "chapters.json"), ch);
    const audit = await page.evaluate(() => JSON.stringify(window.__audit || []));
    require("fs").writeFileSync(path.resolve(path.dirname(out), "audit.json"), audit);
  } else {
    await page.evaluate(() => document.fonts.ready);
  }
  await page.pdf({ path: path.resolve(out), preferCSSPageSize: true, printBackground: true });
  await browser.close();
})();
