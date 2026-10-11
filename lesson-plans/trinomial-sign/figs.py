"""SVG graphs of f(x) = ax² + bx + c, shared by the slides (make_ppt.js) and the cards (make_cards.py).

usage: python3 figs.py   -> figs/*.svg
"""
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
POS, NEG, INK, GRID = "#2F7D46", "#C2452F", "#172231", "#DCE2E9"

# key: (a, b, c, xmin, xmax, ymin, ymax)
FIGS = {
    "f1": (1, -1, -6, -4, 5, -7, 7),     # x² − x − 6, roots −2 and 3
    "g1": (1, -2, -3, -3, 5, -5, 6),     # Δ > 0
    "g2": (1, -2, 1, -3, 5, -5, 6),      # Δ = 0
    "g3": (1, -2, 3, -3, 5, -5, 6),      # Δ < 0
    "neg": (-1, 1, 6, -4, 5, -7, 7),     # −x² + x + 6 (a < 0)
    "title": (1, -1, -6, -4, 5, -7, 7),
}


def svg(a, b, c, x0, x1, y0, y1, w=640, h=480, labels=True, roots=True):
    pad = 34
    sx = (w - 2 * pad) / (x1 - x0)
    sy = (h - 2 * pad) / (y1 - y0)
    X = lambda x: pad + (x - x0) * sx
    Y = lambda y: h - pad - (y - y0) * sy
    f = lambda x: a * x * x + b * x + c
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="DejaVu Sans, Arial, sans-serif">',
           f'<rect width="{w}" height="{h}" fill="#FFFFFF"/>']
    for x in range(math.ceil(x0), math.floor(x1) + 1):
        out.append(f'<line x1="{X(x):.1f}" y1="{Y(y0):.1f}" x2="{X(x):.1f}" y2="{Y(y1):.1f}" stroke="{GRID}" stroke-width="1"/>')
    for y in range(math.ceil(y0), math.floor(y1) + 1):
        out.append(f'<line x1="{X(x0):.1f}" y1="{Y(y):.1f}" x2="{X(x1):.1f}" y2="{Y(y):.1f}" stroke="{GRID}" stroke-width="1"/>')
    # sampled curve, split by sign, with a light fill down to the axis
    n = 400
    pts = [(x0 + (x1 - x0) * i / n, f(x0 + (x1 - x0) * i / n)) for i in range(n + 1)]
    segs, cur = [], [pts[0]]
    for p, q in zip(pts, pts[1:]):
        if (p[1] > 0) != (q[1] > 0) and abs(q[1] - p[1]) > 1e-12:
            t = p[1] / (p[1] - q[1])
            z = (p[0] + t * (q[0] - p[0]), 0.0)
            cur.append(z); segs.append(cur); cur = [z]
        cur.append(q)
    segs.append(cur)
    clip = f'<clipPath id="cp"><rect x="{pad}" y="{pad}" width="{w - 2 * pad}" height="{h - 2 * pad}"/></clipPath>'
    out.append(clip)
    for s in segs:
        mid = s[len(s) // 2][1]
        col = POS if mid >= 0 else NEG
        if abs(mid) < 1e-9 and len(s) > 2:
            mid = max(s, key=lambda p: abs(p[1]))[1]; col = POS if mid >= 0 else NEG
        poly = " ".join(f"{X(x):.1f},{Y(max(min(y, y1 + 5), y0 - 5)):.1f}" for x, y in s)
        base = f"{X(s[-1][0]):.1f},{Y(0):.1f} {X(s[0][0]):.1f},{Y(0):.1f}"
        out.append(f'<polygon points="{poly} {base}" fill="{col}" fill-opacity="0.13" clip-path="url(#cp)"/>')
        out.append(f'<polyline points="{poly}" fill="none" stroke="{col}" stroke-width="5" stroke-linejoin="round" clip-path="url(#cp)"/>')
    # axes
    out.append(f'<line x1="{X(x0) - 8:.1f}" y1="{Y(0):.1f}" x2="{X(x1) + 14:.1f}" y2="{Y(0):.1f}" stroke="{INK}" stroke-width="2.4"/>')
    out.append(f'<polygon points="{X(x1) + 22:.1f},{Y(0):.1f} {X(x1) + 10:.1f},{Y(0) - 6:.1f} {X(x1) + 10:.1f},{Y(0) + 6:.1f}" fill="{INK}"/>')
    out.append(f'<line x1="{X(0):.1f}" y1="{Y(y0) + 8:.1f}" x2="{X(0):.1f}" y2="{Y(y1) - 14:.1f}" stroke="{INK}" stroke-width="2.4"/>')
    out.append(f'<polygon points="{X(0):.1f},{Y(y1) - 22:.1f} {X(0) - 6:.1f},{Y(y1) - 10:.1f} {X(0) + 6:.1f},{Y(y1) - 10:.1f}" fill="{INK}"/>')
    out.append(f'<text x="{X(x1) + 12:.1f}" y="{Y(0) + 24:.1f}" font-size="20" font-style="italic" fill="{INK}">x</text>')
    out.append(f'<text x="{X(0) + 10:.1f}" y="{Y(y1) - 6:.1f}" font-size="20" font-style="italic" fill="{INK}">y</text>')
    if labels:
        for x in range(math.ceil(x0), math.floor(x1) + 1):
            if x != 0:
                out.append(f'<text x="{X(x):.1f}" y="{Y(0) + 28:.1f}" font-size="15" text-anchor="middle" fill="#4F5C6E">{str(x).replace("-", "−")}</text>')
        step = 2 if y1 - y0 > 10 else 1
        for y in range(math.ceil(y0), math.floor(y1) + 1):
            if y != 0 and y % step == 0:
                out.append(f'<text x="{X(0) - 8:.1f}" y="{Y(y) + 5:.1f}" font-size="15" text-anchor="end" fill="#4F5C6E">{str(y).replace("-", "−")}</text>')
        out.append(f'<text x="{X(0) - 8:.1f}" y="{Y(0) + 20:.1f}" font-size="15" text-anchor="end" fill="#4F5C6E">0</text>')
    if roots:
        d = b * b - 4 * a * c
        rs = [] if d < 0 else sorted({(-b - math.sqrt(d)) / (2 * a), (-b + math.sqrt(d)) / (2 * a)})
        for r in rs:
            out.append(f'<circle cx="{X(r):.1f}" cy="{Y(0):.1f}" r="8" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/>')
    out.append("</svg>")
    return "\n".join(out)


def main():
    os.makedirs(os.path.join(HERE, "figs"), exist_ok=True)
    for k, (a, b, c, *box) in FIGS.items():
        kw = dict(labels=False, w=640, h=520) if k == "title" else {}
        open(os.path.join(HERE, "figs", k + ".svg"), "w").write(svg(a, b, c, *box, **kw))
    print("figs:", ", ".join(FIGS))


if __name__ == "__main__":
    main()
