# -*- coding: utf-8 -*-
"""Build the printable books: cover + framed, page-numbered body with a filled-in index and PDF bookmarks.

1. build.py writes index.html / answers.html (index page numbers from pages.json, if known)
2. pdf.js prints the cover and the body separately
3. the invisible @@markers@@ in the body tell us where every section starts -> pages.json
   (repeat until the numbers are stable, since filling the index could shift pages)
4. PyMuPDF draws the frame, logo and page number on every page and adds bookmarks
"""
import json, os, re, subprocess
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda *a: os.path.join(HERE, *a)
BOOK, ANSWERS = "كتاب-الرياضيات.pdf", "دليل-الإجابات-للمعلم.pdf"
GREEN, GOLD = (0.055, 0.353, 0.204), (0.914, 0.706, 0.298)
LESSON_COLOR = {"expand": "#0E7C7B", "factor": "#B7791F", "poly": "#7A3E8E", "roots": "#2B5FB3", "rational": "#2F7D46", "systems": "#C2452F"}


def rgb(h):
    return tuple(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))


def run(*cmd):
    subprocess.run(cmd, check=True, cwd=HERE, stdout=subprocess.DEVNULL)


def markers(pdf):
    """First page (0-based) on which each @@key@@ marker appears."""
    found = {}
    for i, page in enumerate(pymupdf.open(pdf)):
        for key in re.findall(r"@@([a-z0-9\-]+)@@", re.sub(r"\s+", "", page.get_text())):
            found.setdefault(key, i)
    return found


def frame(page, number, color, logo):
    W, H = page.rect.width, page.rect.height
    sh = page.new_shape()
    sh.draw_rect(pymupdf.Rect(16, 16, W - 16, H - 16), radius=0.025)
    sh.finish(color=GREEN, width=1.6)
    sh.draw_rect(pymupdf.Rect(21, 21, W - 21, H - 21), radius=0.02)
    sh.finish(color=color, width=0.7)
    for cx in (W * 0.3, W * 0.7):                       # small diamonds on the top and bottom edges
        for cy in (16, H - 16):
            sh.draw_polyline([(cx - 4, cy), (cx, cy - 4), (cx + 4, cy), (cx, cy + 4), (cx - 4, cy)])
            sh.finish(color=GREEN, fill=GOLD, width=0.6)
    sh.draw_circle((W / 2, 16), 13)                     # logo medallion on the top edge
    sh.finish(color=GREEN, fill=(1, 1, 1), width=1.2)
    sh.draw_circle((W / 2, H - 16), 12.5)               # page-number badge on the bottom edge
    sh.finish(color=(1, 1, 1), fill=color, width=1.6)
    sh.commit()
    page.insert_image(pymupdf.Rect(W / 2 - 10, 6, W / 2 + 10, 26), filename=logo)
    s = str(number)
    tw = pymupdf.get_text_length(s, fontname="hebo", fontsize=10)
    page.insert_text((W / 2 - tw / 2, H - 12.4), s, fontname="hebo", fontsize=10, color=(1, 1, 1))


def section_color(keys_by_page, n_pages):
    """Colour of each body page: the colour of the lesson it belongs to, else green."""
    starts = sorted((p, k) for k, p in keys_by_page.items() if k in LESSON_COLOR or k in ("cards", "exams", "summary", "howto", "index"))
    out, cur = [], GREEN
    for i in range(n_pages):
        for p, k in starts:
            if p == i:
                cur = rgb(LESSON_COLOR[k]) if k in LESSON_COLOR else GREEN
        out.append(cur)
    return out


def decorate(pdf_in, first_number, found, out, cover=None, toc_titles=None):
    body = pymupdf.open(pdf_in)
    colors = section_color(found, len(body))
    logo = P("assets", "mabarrat-logo.jpg")
    for i, page in enumerate(body):
        frame(page, first_number + i, colors[i], logo)
    doc = pymupdf.open()
    if cover:
        doc.insert_pdf(pymupdf.open(cover))
    doc.insert_pdf(body)
    if toc_titles:
        offset = 1 if cover else 0
        doc.set_toc([[lvl, t, found[k] + 1 + offset] for lvl, t, k in toc_titles if k in found])
    doc.save(P(out), garbage=3, deflate=True)
    return len(doc)


def main():
    import content
    prev = None
    for _ in range(4):
        run("python3", "build.py")
        run("node", "pdf.js", "index.html", "_body.pdf", "body")
        found = markers(P("_body.pdf"))
        pages = {k: v + 2 for k, v in found.items()}      # cover is page 1, body starts at 2
        if pages == prev:
            break
        json.dump(pages, open(P("pages.json"), "w"), ensure_ascii=False, indent=1, sort_keys=True)
        prev = pages
    run("node", "pdf.js", "index.html", "_cover.pdf", "cover")
    titles = [(1, "الفهرس", "index")]
    for L in content.LESSONS:
        titles.append((1, f'الدرس {L["num"]}: {L["title"]}', L["id"]))
        titles += [(2, p, f'{L["id"]}-{i + 1}') for i, p in enumerate(__import__("build").PARTS)]
    titles.append((1, "بطاقات المراجعة MCQ", "cards"))
    titles.append((1, "الامتحانات الرسميّة ونماذج التدريب", "exams"))
    titles += [(2, X["title"], X["id"]) for X in content.EXAMS]
    titles.append((1, "بطاقة المراجعة السريعة", "summary"))
    n = decorate(P("_body.pdf"), 2, found, BOOK, cover=P("_cover.pdf"), toc_titles=titles)
    print(f"{BOOK}: {n} pages")
    run("node", "pdf.js", "answers.html", "_answers.pdf", "body")
    n = decorate(P("_answers.pdf"), 1, {}, ANSWERS)
    print(f"{ANSWERS}: {n} pages")
    for f in ("_body.pdf", "_cover.pdf", "_answers.pdf"):
        os.remove(P(f))


if __name__ == "__main__":
    main()
