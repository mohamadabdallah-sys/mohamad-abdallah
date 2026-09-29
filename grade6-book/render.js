// Pre-render all \( \) and \[ \] TeX with KaTeX and inline KaTeX CSS + fonts.
// usage: node render.js in.html out.html
const fs = require("fs");
const path = require("path");
const katexDir = path.dirname(require.resolve("katex/package.json"));
const katex = require("katex");

const [, , input, output] = process.argv;
let html = fs.readFileSync(input, "utf8");

let count = 0;
const render = (tex, displayMode) => {
  count++;
  return katex.renderToString(tex, { displayMode, throwOnError: true, strict: false, output: "html" });
};
html = html.replace(/\\\[([\s\S]+?)\\\]/g, (_, t) => `<span class="dm">${render(t, true)}</span>`);
html = html.replace(/\\\(([\s\S]+?)\\\)/g, (_, t) => render(t, false));

// KaTeX CSS with woff2 fonts only, embedded as data URIs
let css = fs.readFileSync(path.join(katexDir, "dist", "katex.min.css"), "utf8");
css = css.replace(/src:url\(fonts\/([^)]+?)\.woff2\) format\("woff2"\)[^;}]*/g, (_, name) => {
  const b64 = fs.readFileSync(path.join(katexDir, "dist", "fonts", name + ".woff2")).toString("base64");
  return `src:url(data:font/woff2;base64,${b64}) format("woff2")`;
});
html = html.replace("/*KATEX_CSS*/", () => css);

fs.writeFileSync(output, html);
console.log(`rendered ${count} formulas -> ${output} (${(html.length / 1024).toFixed(0)} KB)`);
