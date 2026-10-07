# -*- coding: utf-8 -*-
"""Build everything: edited text -> typeset pages -> one PDF (front cover, book, back cover) with bookmarks.

    python3 make_pdf.py
needs: python3 + pymupdf, node + playwright (Chromium)
"""
import json, os, subprocess
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda *a: os.path.join(HERE, *a)
OUT = "ثرائد-التقوى.pdf"


def run(*cmd):
    subprocess.run(cmd, check=True, cwd=HERE)


def main():
    run("python3", "prep.py")
    run("python3", "build.py")
    run("python3", "cover.py")
    run("node", "render.js", "build/book.html", "build/body.pdf", "--paged")
    run("node", "render.js", "build/cover.html", "build/cover.pdf")

    cover = pymupdf.open(P("build", "cover.pdf"))
    body = pymupdf.open(P("build", "body.pdf"))
    doc = pymupdf.open()
    doc.insert_pdf(cover, from_page=0, to_page=0)
    doc.insert_pdf(body)
    doc.insert_pdf(cover, from_page=1, to_page=1)

    chapters = json.load(open(P("build", "chapters.json"), encoding="utf8"))
    toc = [[1, "الغلاف", 1]]
    toc += [[1, c["title"], c["page"] + 1] for c in chapters]
    toc.append([1, "الغلاف الخلفي", len(doc)])
    doc.set_toc(toc)
    doc.set_metadata({"title": "ثرائد التقوى", "author": "محمد عبدالله", "subject": "ثرائد التقوى — محمد عبدالله",
                      "creator": "", "producer": ""})
    doc.save(P(OUT), garbage=4, deflate=True)
    print(OUT, len(doc), "pages")

    # interior only (for the printing house) — the covers go separately
    body.save(P("للطباعة-المتن.pdf"), garbage=4, deflate=True)
    cover.save(P("للطباعة-الغلاف.pdf"), garbage=4, deflate=True)

    # cover images (for online stores / social media)
    for i, name in ((0, "غلاف-أمامي.png"), (1, "غلاف-خلفي.png")):
        cover[i].get_pixmap(dpi=200).save(P(name))


if __name__ == "__main__":
    main()
