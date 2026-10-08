# -*- coding: utf-8 -*-
"""build/book.html (the #src part) -> build/word.json : the chapters as blocks of inline runs, for make_word.js"""
import json, os, re
from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))


def runs(node):
    """inline children -> [{t: text, k: 'n'|'b'|'q'|'a', fn: note}]"""
    out = []

    def walk(n, kind):
        for c in n.children:
            if c.name is None:
                t = str(c)
                if t:
                    out.append({"t": t, "k": kind})
            elif c.name == "span" and "fn" in (c.get("class") or []):
                out.append({"fn": c.get("data-note", "")})
            elif c.name == "span" and "ayah" in (c.get("class") or []):
                out.append({"t": c.get_text(), "k": "a"})
            elif c.name == "span" and "q" in (c.get("class") or []):
                walk(c, "q")
            elif c.name == "b":
                walk(c, "b")
            else:
                walk(c, kind)
    walk(node, "n")
    # normalise whitespace
    for r in out:
        if "t" in r:
            r["t"] = re.sub(r"\s+", " ", r["t"])
    return out


def main():
    html = open(os.path.join(HERE, "build", "book.html"), encoding="utf8").read()
    soup = BeautifulSoup(html, "html.parser")
    src = soup.find(id="src")
    chapters = []
    for sec in src.find_all("section", recursive=False):
        cls = sec.get("class") or []
        if "title-page" in cls or "basmala-page" in cls:
            continue
        ch = {"title": sec.get("data-title"), "kind": "dedication" if "dedication" in cls else ("biblio" if "biblio" in cls else ("intro" if "intro" in cls else "topic")), "blocks": []}
        for el in sec.children:
            if el.name is None or (el.get("class") and "opener" in el.get("class")):
                continue
            c = el.get("class") or []
            if el.name == "h3":
                ch["blocks"].append({"type": "h3", "runs": runs(el)})
            elif el.name == "div" and "li" in c:
                ch["blocks"].append({"type": "li", "runs": runs(el)})
            elif el.name == "p":
                t = "ded" if "ded" in c else "bib" if "bib" in c else "end" if "hamd-end" in c else "verse" if "verse-block" in c else "quote" if "quote-block" in c else "p"
                ch["blocks"].append({"type": t, "runs": runs(el)})
        chapters.append(ch)
    json.dump(chapters, open(os.path.join(HERE, "build", "word.json"), "w", encoding="utf8"), ensure_ascii=False)
    print("chapters:", len(chapters), "blocks:", sum(len(c["blocks"]) for c in chapters),
          "notes:", sum(1 for c in chapters for b in c["blocks"] for r in b["runs"] if "fn" in r))


if __name__ == "__main__":
    main()
