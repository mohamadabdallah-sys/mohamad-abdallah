# -*- coding: utf-8 -*-
"""Step 1: apply the editorial work to the extracted text.

src/original.txt  : the manuscript as extracted from the .docx, one paragraph per line
src/structure.txt : DEL <line numbers / ranges>  -> remove duplicated or stray paragraphs
                    HEAD <line> <title>           -> insert a missing topic title before a line
src/fixes.txt     : old|||new  -> language corrections, one per line ("⏎" = paragraph break)

Writes build/edited.txt (one paragraph per line) and reports any correction that did not apply.
"""
import os, re, sys, unicodedata

NFC = lambda s: unicodedata.normalize("NFC", s)

HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda *a: os.path.join(HERE, *a)


def load_structure():
    dels, heads = set(), {}
    for line in open(P("src", "structure.txt"), encoding="utf8"):
        parts = line.split()
        if not parts:
            continue
        if parts[0] == "DEL":
            for tok in parts[1:]:
                if "-" in tok:
                    a, b = map(int, tok.split("-"))
                    dels.update(range(a, b + 1))
                else:
                    dels.add(int(tok))
        elif parts[0] == "HEAD":
            heads[int(parts[1])] = " ".join(parts[2:])
    return dels, heads


def load_fixes():
    fixes = []
    for n, line in enumerate(open(P("src", "fixes.txt"), encoding="utf8"), 1):
        line = line.rstrip("\n")
        if not line.strip():
            continue
        old, new = line.split("|||")
        fixes.append((n, NFC(old), NFC(new)))
    return fixes


def main():
    lines = NFC(open(P("src", "original.txt"), encoding="utf8").read()).replace("\u00a0", " ").split("\n")
    dels, heads = load_structure()
    fixes = load_fixes()
    used = {n: 0 for n, _, _ in fixes}
    out = []
    for i, text in enumerate(lines, 1):
        if i in heads:
            out.append("**%s**" % heads[i])
        if i in dels:
            continue
        for n, old, new in fixes:
            if old in text:
                used[n] += text.count(old)
                text = text.replace(old, new)
        for part in text.split("⏎"):
            part = part.strip()
            if part:
                out.append(part)
    bad = [(n, old) for n, old, _ in fixes if used[n] == 0]
    for n, old in bad:
        print("fix not applied (line %d): %s" % (n, old[:80]), file=sys.stderr)
    os.makedirs(P("build"), exist_ok=True)
    open(P("build", "edited.txt"), "w", encoding="utf8").write("\n".join(out) + "\n")
    print("paragraphs:", len(out), "fixes:", len(fixes), "unapplied:", len(bad))


if __name__ == "__main__":
    main()
