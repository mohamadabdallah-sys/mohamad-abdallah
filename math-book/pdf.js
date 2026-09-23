// Print a built page to an A4 PDF with Chromium (Playwright).  usage: node pdf.js [page.html] [out.pdf]
const path = require("path");
let pw;
try { pw = require("playwright"); } catch { pw = require("/opt/node22/lib/node_modules/playwright"); }

(async () => {
  const src = process.argv[2] || "index.html";
  const out = process.argv[3] || path.join(__dirname, "كتاب-الرياضيات.pdf");
  const browser = await pw.chromium.launch();
  const page = await browser.newPage();
  await page.goto("file://" + path.join(__dirname, src), { waitUntil: "load" });
  await page.evaluate(() => document.fonts.ready);
  await page.emulateMedia({ media: "print", colorScheme: "light" });
  await page.pdf({ path: out, format: "A4", printBackground: true, preferCSSPageSize: true });
  await browser.close();
  console.log("PDF ->", out);
})();
