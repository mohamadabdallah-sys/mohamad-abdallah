// A small pagination engine for the book (runs in Chromium before printing).
//
// #src holds the book as a flat list of blocks (sections of <p>, <h3>, .li, …). Footnotes are
// <span class="fn" data-note="…"> inside the text. We pour the blocks into fixed-size pages,
// put the notes of each page at its bottom (numbered from ١ on every page), split paragraphs
// between pages at word boundaries, start every topic on a new page and finish with the table
// of contents. window.__done = true when finished.
(function () {
  const AR = s => String(s).replace(/[0-9]/g, d => "٠١٢٣٤٥٦٧٨٩"[d]);
  const MIN_WORDS = 5;          // never leave fewer words than this on either side of a split

  let book, pages = [], cur = null, curTopic = "", chapterStarts = [];

  function newPage(opts = {}) {
    const page = document.createElement("div");
    page.className = "page" + (opts.cls ? " " + opts.cls : "");
    page.innerHTML =
      '<div class="head"></div><div class="body"><div class="text"></div>' +
      '<div class="notes"></div></div><div class="foot"></div>';
    book.appendChild(page);
    const p = {
      el: page, text: page.querySelector(".text"), notes: page.querySelector(".notes"),
      body: page.querySelector(".body"), n: 0, topic: curTopic, opener: !!opts.opener,
      plain: !!opts.plain,
    };
    pages.push(p);
    cur = p;
    return p;
  }

  function fits(p) {
    const h = p.text.offsetHeight + (p.notes.childElementCount ? p.notes.offsetHeight : 0);
    return h <= p.body.clientHeight;
  }

  // ---- atoms: a block's inline content as a list of words with their wrapping tags
  function atomize(el) {
    const atoms = [];
    function walk(node, stack) {
      for (const ch of node.childNodes) {
        if (ch.nodeType === 3) {
          const parts = ch.nodeValue.split(/(\s+)/);
          for (const part of parts) {
            if (!part) continue;
            if (/^\s+$/.test(part)) {
              if (atoms.length) atoms[atoms.length - 1].space = true;
              else atoms.push({ text: "", stack, space: true });
            } else atoms.push({ text: part, stack, space: false });
          }
        } else if (ch.nodeType === 1) {
          if (ch.classList.contains("fn")) {
            atoms.push({ fn: ch.getAttribute("data-note"), stack, space: false });
          } else {
            walk(ch, stack.concat([[ch.tagName.toLowerCase(), ch.getAttribute("class") || ""]]));
          }
        }
      }
    }
    walk(el, []);
    return atoms;
  }

  const esc = s => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

  // rebuild html for atoms[a:b]; footnotes get the numbers given in nums (atom index -> number)
  function build(atoms, a, b, nums) {
    let html = "", open = [];
    const same = (x, y) => x[0] === y[0] && x[1] === y[1];
    for (let i = a; i < b; i++) {
      const at = atoms[i], st = at.stack;
      let k = 0;
      while (k < open.length && k < st.length && same(open[k], st[k])) k++;
      while (open.length > k) html += "</" + open.pop()[0] + ">";
      for (; k < st.length; k++) {
        html += "<" + st[k][0] + (st[k][1] ? ' class="' + st[k][1] + '"' : "") + ">";
        open.push(st[k]);
      }
      if (at.fn !== undefined) html += '<sup class="fnr">' + AR(nums.get(i)) + "</sup>";
      else html += esc(at.text);
      if (at.space && i < b - 1) html += " ";
    }
    while (open.length) html += "</" + open.pop()[0] + ">";
    return html;
  }

  function addNote(p, num, text) {
    const d = document.createElement("div");
    d.className = "fnote";
    d.innerHTML = '<span class="fnn">' + AR(num) + ":</span> " + text;
    p.notes.appendChild(d);
    return d;
  }

  // place atoms[a:b] of block `tpl` on page p as a (possibly partial) block; returns the element
  function place(p, tpl, atoms, a, b, cont, split) {
    const el = tpl.cloneNode(false);
    if (cont) el.classList.add("cont");
    if (split) el.classList.add("split");
    const nums = new Map(), notes = [];
    let n = p.n;
    for (let i = a; i < b; i++) if (atoms[i].fn !== undefined) { nums.set(i, ++n); notes.push(addNote(p, n, atoms[i].fn)); }
    el.innerHTML = build(atoms, a, b, nums);
    p.text.appendChild(el);
    return { el, notes, n };
  }

  // how much of the width the last line of el fills (text is right-aligned before justification)
  function lastLineFill(el) {
    // a zero-width marker at the very end of the text sits where the last line ends (on its left, RTL)
    const m = document.createElement("span");
    m.textContent = "\u200b";
    el.appendChild(m);
    const x = m.getBoundingClientRect().left;
    m.remove();
    const box = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    const padR = parseFloat(cs.paddingRight) || 0, padL = parseFloat(cs.paddingLeft) || 0;
    const indent = el.classList.contains("cont") ? 0 : 0;
    return (box.right - padR - x) / (box.width - padR - padL - indent);
  }

  function unplace(p, r) {
    r.el.remove();
    r.notes.forEach(x => x.remove());
  }

  function flowBlock(tpl, keepWithNext) {
    const atoms = atomize(tpl);
    let a = 0, cont = false;
    while (a < atoms.length) {
      // whole rest fits?
      let r = place(cur, tpl, atoms, a, atoms.length, cont, false);
      if (fits(cur)) { cur.n = r.n; return r.el; }
      unplace(cur, r);
      // break points: after atoms that end with a space
      const breaks = [];
      for (let i = a + MIN_WORDS; i <= atoms.length - MIN_WORDS; i++) if (atoms[i - 1].space) breaks.push(i);
      let lo = 0, hi = breaks.length - 1, best = -1;
      while (lo <= hi) {
        const mid = (lo + hi) >> 1;
        r = place(cur, tpl, atoms, a, breaks[mid], cont, true);
        const ok = fits(cur);
        unplace(cur, r);
        if (ok) { best = mid; lo = mid + 1; } else hi = mid - 1;
      }
      if (best < 0) {
        if (cur.text.childElementCount === 0) {        // cannot fit even on an empty page: force
          r = place(cur, tpl, atoms, a, atoms.length, cont, false);
          cur.n = r.n;
          return r.el;
        }
        newPage();
        continue;
      }
      r = place(cur, tpl, atoms, a, breaks[best], cont, false);
      if (lastLineFill(r.el) > 0.72) r.el.classList.add("split");
      cur.n = r.n;
      a = breaks[best];
      cont = true;
      newPage();
    }
  }

  function flowWhole(el) {           // headings, openers: never split
    const c = el.cloneNode(true);
    cur.text.appendChild(c);
    if (fits(cur) || cur.text.childElementCount === 1) return c;
    c.remove();
    newPage();
    cur.text.appendChild(c);
    return c;
  }

  function flowSection(sec) {
    const title = sec.getAttribute("data-title");
    curTopic = title;
    const p = newPage({ opener: true });
    p.topic = title;
    chapterStarts.push({ id: sec.id, title, page: pages.length, kind: sec.className });
    const kids = Array.from(sec.children);
    for (let i = 0; i < kids.length; i++) {
      const el = kids[i];
      if (el.classList.contains("opener")) { flowWhole(el); continue; }
      if (el.tagName === "H3") {
        // keep a heading with at least the start of the next block
        const h = flowWhole(el);
        const next = kids[i + 1];
        if (next) {
          const probe = next.cloneNode(true);
          probe.style.maxHeight = "3.6em"; probe.style.overflow = "hidden";
          cur.text.appendChild(probe);
          const ok = fits(cur);
          probe.remove();
          if (!ok && cur.text.childElementCount > 1) { h.remove(); newPage(); cur.text.appendChild(h); }
        }
        continue;
      }
      flowBlock(el);
    }
  }

  function fixedPage(sec) {
    const p = newPage({ plain: true, cls: "fixed" });
    p.body.innerHTML = "";
    p.body.appendChild(sec.cloneNode(true));
  }

  let tocPage = 0;
  function toc() {
    curTopic = "الفهرس";
    const p = newPage({ opener: true });
    tocPage = pages.length;
    p.topic = "الفهرس";
    const op = document.createElement("div");
    op.className = "opener";
    op.innerHTML = '<h2 class="ch-title">الفهرس</h2><div class="orn"></div>';
    flowWhole(op);
    let k = 0;
    for (const c of chapterStarts) {
      const row = document.createElement("div");
      const topic = c.kind === "chapter";
      row.className = "toc-row" + (topic ? "" : " front");
      row.innerHTML = '<span class="tn">' + (topic ? AR(++k) + "." : "۞") + '</span><span class="tt">' + c.title +
        '</span><span class="fill"></span><span class="tp">' + AR(c.page) + "</span>";
      flowWhole(row);
    }
  }

  function decorate() {
    pages.forEach((p, i) => {
      const num = i + 1;
      if (!p.plain) p.el.querySelector(".foot").innerHTML = '<span class="pn">' + AR(num) + "</span>";
      if (!p.plain && !p.opener && p.topic) p.el.querySelector(".head").innerHTML = '<span>' + p.topic + "</span>";
      if (!p.notes.childElementCount) p.notes.remove();
    });
  }

  async function run() {
    // load every font face now: faces are otherwise fetched lazily, after the text was measured
    await Promise.all(Array.from(document.fonts).map(f => f.load().catch(() => null)));
    await document.fonts.ready;
    book = document.getElementById("book");
    const src = document.getElementById("src");
    for (const sec of Array.from(src.children)) {
      if (sec.classList.contains("title-page") || sec.classList.contains("basmala-page")) fixedPage(sec);
      else flowSection(sec);
    }
    toc();
    decorate();
    src.remove();
    window.__pages = pages.length;
    window.__overflow = pages.map((p, i) => (!p.plain && !fits(p)) ? i + 1 : 0).filter(Boolean);
    window.__chapters = chapterStarts.concat([{ title: "الفهرس", page: tocPage }]);
    window.__done = true;
  }

  window.addEventListener("load", () => { run().catch(e => { console.error(e.stack || e); window.__done = "error"; }); });
})();
