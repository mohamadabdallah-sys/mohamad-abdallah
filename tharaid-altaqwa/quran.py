# -*- coding: utf-8 -*-
"""Find every Qur'an quotation of the book in the Mushaf (Uthmani text, src/quran-uthmani.json).

The author's quotations are written in ordinary spelling, often without diacritics, sometimes
shortened with "..." or with small slips. We compare consonant skeletons (no vowels, no long
vowels, no hamza seats), so that e.g. «الصلاة» matches «ٱلصَّلَوٰةَ». A quotation is replaced by the
exact Uthmani words it covers and gets its sura / verse reference.
"""
import json, os, re, difflib
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))

DROP = set("اأإآٱءؤئوىيـ")
KEEP = set("بتثجحخدذرزسشصضطظعغفقكلمنهة")


def skel(s):
    out = []
    for c in s:
        if c in KEEP:
            out.append("ه" if c == "ة" else c)
    return re.sub("ل+", "ل", "".join(out))


def skel_text(s):
    return "".join(skel(w) for w in s.split())


class Quran:
    def __init__(self):
        data = json.load(open(os.path.join(HERE, "src", "quran-uthmani.json"), encoding="utf8"))
        self.names = {}
        self.words = []          # (sura, ayah, word)
        chars, owner = [], []
        for sura in data:
            self.names[sura["id"]] = sura["name"]
            for v in sura["verses"]:
                for w in v["text"].split():
                    wi = len(self.words)
                    self.words.append((sura["id"], v["id"], w))
                    for c in skel(w):
                        chars.append(c)
                        owner.append(wi)
        self.S = "".join(chars)
        self.owner = owner
        self.grams = defaultdict(list)       # 4-gram -> positions (for fuzzy search)
        for i in range(len(self.S) - 3):
            self.grams[self.S[i:i + 4]].append(i)

    # ------------------------------------------------------------------ search
    def find(self, frag, hint_sura=None, after=None):
        """-> (first_word, last_word, exact) or None
        hint_sura: sura named by the author; after: word index the quotation continues from"""
        F = skel_text(frag)
        if len(F) < 3:
            return None
        hits = [m.start() for m in re.finditer("(?=%s)" % re.escape(F), self.S)]
        if hits:
            pick = hits[0]
            if after is not None:
                near = [h for h in hits if 0 <= self.owner[h] - after < 120]
                if near:
                    hits = near
            if hint_sura:
                for h in hits:
                    if self.words[self.owner[h]][0] == hint_sura:
                        pick = h
                        break
                else:
                    pick = hits[0]
            else:
                pick = hits[0]
            if len(hits) > 1 and len(F) < 8 and not hint_sura and after is None:
                return None              # too short to know which verse
            return self.owner[pick], self.owner[pick + len(F) - 1], True
        # fuzzy: vote for regions sharing 4-grams, then align
        votes = defaultdict(int)
        for i in range(len(F) - 3):
            for p in self.grams.get(F[i:i + 4], ())[:400]:
                votes[(p - i) // 40] += 1
        best = None
        for region, _ in sorted(votes.items(), key=lambda kv: -kv[1])[:12]:
            lo = max(0, region * 40 - 40)
            hi = min(len(self.S), region * 40 + len(F) + 80)
            W = self.S[lo:hi]
            sm = difflib.SequenceMatcher(None, F, W, autojunk=False)
            blocks = [b for b in sm.get_matching_blocks() if b.size]
            if not blocks:
                continue
            matched = sum(b.size for b in blocks)
            ratio = matched / len(F)
            start = lo + blocks[0].b
            end = lo + blocks[-1].b + blocks[-1].size - 1
            span = end - start + 1
            score = ratio - abs(span - len(F)) / (2 * len(F))
            if best is None or score > best[0]:
                best = (score, start, end, ratio)
        if best and best[3] >= 0.82 and best[0] >= 0.72:
            return self.owner[best[1]], self.owner[best[2]], False
        return None

    def text(self, w1, w2):
        return " ".join(self.words[i][2] for i in range(w1, w2 + 1))

    def ref(self, w1, w2):
        s1, a1, _ = self.words[w1]
        s2, a2, _ = self.words[w2]
        return s1, a1, s2, a2
