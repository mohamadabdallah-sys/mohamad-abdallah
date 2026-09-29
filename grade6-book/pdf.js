// Print a built page to PDF with Chromium (Playwright).
// usage: node pdf.js <page.html> <out.pdf> [cover|body]
//   cover: only the cover, full bleed.  body: everything else, with page margins for the frame.
const path = require("path");
let pw;
try { pw = require("playwright"); } catch { pw = require("/opt/node22/lib/node_modules/playwright"); }

const MODE_CSS = {
  cover: "@page { size: A4; margin: 0 } .sheet:not(.cover) { display: none !important }",
  body: `@page { size: A4; margin: 17mm 15mm 21mm }
         .cover { display: none !important }
         .sheet { padding: 0 !important; -webkit-box-decoration-break: slice !important; box-decoration-break: slice !important }`,
};

(async () => {
  const [src = "index.html", out = "book.pdf", mode = "body"] = process.argv.slice(2);
  const browser = await pw.chromium.launch();
  const page = await browser.newPage();
  await page.goto("file://" + path.resolve(__dirname, src), { waitUntil: "load" });
  await page.addStyleTag({ content: MODE_CSS[mode] });
  await page.evaluate(() => document.fonts.ready);
  await page.emulateMedia({ media: "print", colorScheme: "light" });
  await page.pdf({ path: path.resolve(__dirname, out), format: "A4", printBackground: true, preferCSSPageSize: true });
  await browser.close();
  console.log("PDF ->", out, `(${mode})`);
})();
