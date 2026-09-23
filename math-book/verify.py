# -*- coding: utf-8 -*-
"""Check every exercise / exam answer in content.py with sympy."""
import random
import sympy as sp
from content import LESSONS, EXAMS

x, y = sp.symbols("x y")
NS = {"x": x, "y": y, "sqrt": sp.sqrt}


def check(chk):
    kind = chk[0]
    if kind == "eq":
        a, b = (sp.sympify(s, locals=NS) for s in chk[1:])
        if sp.simplify(sp.radsimp(a - b)) == 0:
            return True
        # numeric fallback at random points
        return all(abs(complex((a - b).subs({x: v, y: w}).evalf())) < 1e-9
                   for v, w in [(random.uniform(-5, 5), random.uniform(-5, 5)) for _ in range(6)])
    if kind == "sys":
        eqs, (xv, yv) = chk[1], chk[2]
        exprs = [sp.sympify(e, locals=NS) for e in eqs]
        sol = sp.solve(exprs, [x, y], dict=True)
        return (len(sol) == 1 and abs(float(sol[0][x]) - xv) < 1e-9
                and abs(float(sol[0][y]) - yv) < 1e-9)
    if kind == "pt":
        eqs, (xv, yv) = chk[1], chk[2]
        return all(sp.simplify(sp.sympify(e, locals=NS).subs({x: xv, y: yv})) == 0 for e in eqs)
    raise ValueError(kind)


def run():
    bad, n = [], 0
    for L in LESSONS:
        for lvl in ("easy", "medium", "hard", "challenge"):
            for i, ex in enumerate(L.get(lvl, [])):
                chks = ex["chk"] if isinstance(ex["chk"], list) else [ex["chk"]]
                for c in chks:
                    n += 1
                    if not check(c):
                        bad.append((L["id"], lvl, i + 1, c))
        sk = L.get("skills")
        if sk:
            n += 1
            if not check(sk["model"]["chk"]):
                bad.append((L["id"], "skills-model", sk["model"]["chk"]))
            for i, ex in enumerate(sk["practice"]):
                for c in (ex["chk"] if isinstance(ex["chk"], list) else [ex["chk"]]):
                    n += 1
                    if not check(c):
                        bad.append((L["id"], "skills", i + 1, c))
        for qi, (_, items) in enumerate(L.get("quiz", [])):
            for it in items:
                n += 1
                if not check(it["chk"]):
                    bad.append((L["id"], "quiz", qi + 1, it["chk"]))
        for i, q in enumerate(L.get("mcq", [])):
            n += 1
            if q["expr"]:
                ok = [check(("eq", q["expr"], o)) for o in q["syms"]]
                good = ok[q["ans"]] and sum(ok) == 1
            else:
                good = all(check(c) for c in q["chk"])
            if not good:
                bad.append((L["id"], "mcq", i + 1))
        for i, t in enumerate(L.get("tf", [])):
            n += 1
            if check(t["chk"]) != t["truth"]:
                bad.append((L["id"], "tf", i + 1, t["chk"]))
    for X in EXAMS:
        for qi, q in enumerate(X["qs"]):
            for it in q[2]:
                n += 1
                if not check(it[2]):
                    bad.append((X["id"], qi + 1, it[0], it[2]))
    return n, bad


if __name__ == "__main__":
    n, bad = run()
    print(f"checked {n} answers, {len(bad)} wrong")
    for b in bad:
        print("  WRONG:", b)
    raise SystemExit(1 if bad else 0)
