# -*- coding: utf-8 -*-
"""Helpers shared by the grade-7 content files. Every answer carries a machine check (see verify.py)."""


def E(q, a, chk=None, text=False, hint=None, ahtml=False, kind=None):
    """Exercise. q/a are TeX unless text=True (q and a are HTML)."""
    return dict(q=q, a=a, chk=chk, text=text, hint=hint, ahtml=ahtml or text, kind=kind)


def V(kind, q, a, chk):
    """Varied-type exercise (HTML question + answer) with a type label."""
    return dict(q=q, a=a, chk=chk, text=True, hint=None, ahtml=True, kind=kind)


def eq(expr, ans):          # identical for every x, y (or equal numbers)
    return ("eq", expr, ans)


def approx(expr, val, tol=0.006):   # rounded numeric answers
    return ("approx", expr, val, tol)


def sysc(eqs, sol):
    return ("sys", eqs, sol)


def pt(eqs, p):
    return ("pt", eqs, p)


def truth(expr):            # a Python/sympy boolean that must be True, e.g. "sqrt(2) < 3/2"
    return ("true", expr)


def TF(s, truth_, fix=None, chk=None):
    return dict(s=s, truth=truth_, fix=fix, chk=chk)


def MC(q, opts, ans, expr=None, syms=None, chk=None):
    return dict(q=q, opts=opts, ans=ans, expr=expr, syms=syms, chk=chk)


def ACT(kind, title, fmt, body, lines=0, scale=False):
    return dict(kind=kind, title=title, fmt=fmt, body=body, lines=lines, scale=scale)


def ACTV(title, aids, steps, goal):
    return dict(title=title, aids=aids, steps=steps, goal=goal)


def INTRO(hook, recall, idea):
    return dict(hook=hook, recall=recall, idea=idea)


def T(q, a, chk):
    return dict(q=q, a=a, chk=chk)


def QI(q, steps, chk):
    return dict(q=q, steps=steps, chk=chk)


def SK(q, understand, plan, solve, check, chk):
    return dict(q=q, steps=[understand, plan, solve, check], chk=chk)
