# -*- coding: utf-8 -*-
"""Geometric ornaments (eight-pointed stars, rules) as SVG strings, shared by the book and the covers."""
import math, base64

GOLD = "#b48a35"
GOLD_LIGHT = "#e2c27a"
GREEN = "#0d5a42"
DEEP = "#0a3b2e"


def star(cx, cy, R, r, n=8, rot=0.0):
    pts = []
    for i in range(2 * n):
        a = rot + math.pi * i / n - math.pi / 2
        rad = R if i % 2 == 0 else r
        pts.append("%.2f,%.2f" % (cx + rad * math.cos(a), cy + rad * math.sin(a)))
    return " ".join(pts)


def khatam(cx, cy, R, stroke, fill="none", sw=1.0, inner=True):
    """eight-pointed star made of two squares, with an inner octagon ring"""
    s = R * 0.7071
    out = ['<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="%s" stroke="%s" stroke-width="%.2f"/>'
           % (cx - s, cy - s, 2 * s, 2 * s, fill, stroke, sw),
           '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="%s" stroke="%s" stroke-width="%.2f" transform="rotate(45 %.2f %.2f)"/>'
           % (cx - s, cy - s, 2 * s, 2 * s, fill, stroke, sw, cx, cy)]
    if inner:
        out.append('<polygon points="%s" fill="none" stroke="%s" stroke-width="%.2f"/>' % (star(cx, cy, R * 0.62, R * 0.5, 8, math.pi / 8), stroke, sw * 0.7))
        out.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="none" stroke="%s" stroke-width="%.2f"/>' % (cx, cy, R * 0.3, stroke, sw * 0.7))
    return "".join(out)


def svg(w, h, body):
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %g %g" width="%g" height="%g">%s</svg>' % (w, h, w, h, body)


def data_uri(s):
    return "data:image/svg+xml;base64," + base64.b64encode(s.encode("utf8")).decode()


def divider(w=360, h=30, color=GOLD):
    cy = h / 2
    b = []
    for side in (-1, 1):
        x0 = w / 2 + side * 22
        x1 = w / 2 + side * (w / 2 - 6)
        b.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="1.1"/>' % (x0, cy - 2.2, x1, cy - 2.2, color))
        b.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="0.5"/>' % (x0, cy + 2.2, x1 + side * -30, cy + 2.2, color))
        for k, xx in enumerate((w / 2 + side * 46, w / 2 + side * 70)):
            d = 3.4 - k
            b.append('<polygon points="%g,%g %g,%g %g,%g %g,%g" fill="%s"/>' % (xx - d, cy, xx, cy - d, xx + d, cy, xx, cy + d, color))
        b.append('<circle cx="%g" cy="%g" r="1.6" fill="%s"/>' % (x1, cy - 2.2, color))
    b.append(khatam(w / 2, cy, 12, color, "#fff", 1.1))
    return svg(w, h, "".join(b))


def headpiece(w=420, h=64):
    """band above a topic title: double rule with a big star in the middle (the topic number sits on it)"""
    cy = h / 2
    b = []
    for side in (-1, 1):
        x0, x1 = w / 2 + side * 34, w / 2 + side * (w / 2 - 4)
        for dy, sw in ((-5, 1.2), (5, 1.2)):
            b.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="%g"/>' % (x0, cy + dy, x1, cy + dy, GOLD, sw))
        b.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="0.6" stroke-dasharray="1.5 3"/>' % (x0 + side * 8, cy, x1, cy, GOLD))
        for xx in (w / 2 + side * (w / 2 - 14),):
            b.append(khatam(xx, cy, 9, GOLD, "#fff", 0.9, inner=False))
        b.append('<circle cx="%g" cy="%g" r="2" fill="%s"/>' % (w / 2 + side * 60, cy, GOLD))
        b.append('<circle cx="%g" cy="%g" r="1.4" fill="%s"/>' % (w / 2 + side * 72, cy, GOLD))
    b.append(khatam(w / 2, cy, 30, GOLD, GREEN, 1.6, inner=False))
    b.append('<polygon points="%s" fill="none" stroke="%s" stroke-width="0.8"/>' % (star(w / 2, cy, 24, 19, 8, math.pi / 8), GOLD_LIGHT))
    return svg(w, h, "".join(b))


def pattern_tile(s=60, color=GOLD, op=0.2):
    """repeating tile of eight-pointed stars joined by small squares"""
    b = [khatam(s / 2, s / 2, s * 0.36, color, "none", 0.8)]
    for cx, cy in ((0, 0), (s, 0), (0, s), (s, s)):
        b.append('<rect x="%g" y="%g" width="%g" height="%g" fill="none" stroke="%s" stroke-width="0.8" transform="rotate(45 %g %g)"/>'
                 % (cx - s * 0.11, cy - s * 0.11, s * 0.22, s * 0.22, color, cx, cy))
    for cx, cy in ((s / 2, 0), (s / 2, s), (0, s / 2), (s, s / 2)):
        b.append('<circle cx="%g" cy="%g" r="%g" fill="none" stroke="%s" stroke-width="0.6"/>' % (cx, cy, s * 0.06, color))
    return '<g opacity="%g">%s</g>' % (op, "".join(b))


def corner(size=70, color=GOLD, fx=False, fy=False):
    """corner ornament for frames (top-left; fx / fy mirror it)"""
    b = ['<path d="M%g,4 L4,4 L4,%g" fill="none" stroke="%s" stroke-width="1.6"/>' % (size, size, color),
         '<path d="M%g,10 L10,10 L10,%g" fill="none" stroke="%s" stroke-width="0.7"/>' % (size - 12, size - 12, color),
         khatam(22, 22, 11, color, "none", 1.0, inner=False),
         '<circle cx="22" cy="22" r="3" fill="%s"/>' % color]
    t = "translate(%g %g) scale(%d %d)" % (size if fx else 0, size if fy else 0, -1 if fx else 1, -1 if fy else 1)
    return svg(size, size, '<g transform="%s">%s</g>' % (t, "".join(b)))
