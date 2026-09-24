// Render the cover logo (with the book's fonts) to assets/book-logo.png for the page frames.
const path = require("path");
let pw;
try { pw = require("playwright"); } catch { pw = require("/opt/node22/lib/node_modules/playwright"); }
(async () => {
  const b = await pw.chromium.launch();
  const p = await b.newPage({ deviceScaleFactor: 4 });
  await p.goto("file://" + path.join(__dirname, "index.html"));
  await p.evaluate(() => document.fonts.ready);
  await p.locator(".cover-logo svg").screenshot({ path: path.join(__dirname, "assets", "book-logo.png"), omitBackground: true });
  await b.close();
})();
