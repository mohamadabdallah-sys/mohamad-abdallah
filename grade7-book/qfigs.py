# -*- coding: utf-8 -*-
"""Small geometry figures for questions. Drawn from the real measures (angles to scale).

A question gets a figure by carrying the marker [[fig:key]] in its (html) text, or `fig="key"` on a worked example.
build.page() swaps each marker for the SVG. Coordinates are math-style (y up); the SVG viewBox is fitted automatically.
"""
import math


def _u(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy) or 1
    return dx / n, dy / n


def _deg(p, d, t):
    return p[0] + t * math.cos(math.radians(d)), p[1] + t * math.sin(math.radians(d))


def tri(alpha, beta, base=6.0):
    """Triangle A(0,0) B(base,0) C with angle alpha at A and beta at B."""
    t = base * math.sin(math.radians(beta)) / math.sin(math.radians(alpha + beta))
    return (0.0, 0.0), (base, 0.0), _deg((0.0, 0.0), alpha, t)


class Fig:
    S = 30  # px per unit

    def __init__(self):
        self.el, self.pts, self.txt = [], [], []

    def P(self, p):
        return p[0] * self.S, -p[1] * self.S

    def _see(self, *ps):
        self.pts += [self.P(p) for p in ps]

    def poly(self, *ps, fill=True):
        self._see(*ps)
        d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in map(self.P, ps)) + " Z"
        self.el.insert(0, f'<path class="{"f1 " if fill else ""}qf-edge" d="{d}"/>')

    def seg(self, a, b, cls="qf-edge"):
        self._see(a, b)
        (x1, y1), (x2, y2) = self.P(a), self.P(b)
        self.el.append(f'<path class="{cls}" d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}"/>')

    def line(self, a, b, ext=1.2, cls="qf-line", name=None, at=1):
        u = _u(a, b)
        p, q = (a[0] - ext * u[0], a[1] - ext * u[1]), (b[0] + ext * u[0], b[1] + ext * u[1])
        self.seg(p, q, cls)
        if name:
            e = q if at else p
            self.text((e[0] + 0.1 * u[0] * (1 if at else -1), e[1] + 0.35), name, "qf-sm")

    def dot(self, p):
        self._see(p)
        x, y = self.P(p)
        self.el.append(f'<circle class="dot" cx="{x:.1f}" cy="{y:.1f}" r="3.2"/>')

    def text(self, p, s, cls="", anchor="middle"):
        x, y = self.P(p)
        self.pts.append((x, y - 12)); self.pts.append((x + 8 * len(s) / 2 + 4, y + 4)); self.pts.append((x - 8 * len(s) / 2 - 4, y + 4))
        fs = {"qf-sm": 12, "qf-acc": 13}.get(cls, 14)
        self.txt.append((f'<text x="{x:.1f}" y="{y + 5:.1f}" text-anchor="{anchor}" class="lt {cls}" style="font-size:', fs, f'px">{s}</text>'))

    def name(self, p, s, center, gap=0.45):
        u = _u(center, p)
        self.text((p[0] + gap * u[0], p[1] + gap * u[1] - 0.05), s)

    def angle(self, v, p1, p2, label=None, r=0.75, right=False, acc=True, n=1):
        u1, u2 = _u(v, p1), _u(v, p2)
        if right:
            s = 0.34
            a = (v[0] + s * u1[0], v[1] + s * u1[1]); c = (v[0] + s * u2[0], v[1] + s * u2[1])
            b = (a[0] + s * u2[0], a[1] + s * u2[1])
            (x1, y1), (x2, y2), (x3, y3) = self.P(a), self.P(b), self.P(c)
            self.el.append(f'<path class="qf-mark" d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f} L{x3:.1f} {y3:.1f}"/>')
        else:
            for k in range(n):
                rr = r + k * 0.14
                a = self.P((v[0] + rr * u1[0], v[1] + rr * u1[1])); b = self.P((v[0] + rr * u2[0], v[1] + rr * u2[1]))
                sa, sb = (u1[0], -u1[1]), (u2[0], -u2[1])
                sweep = 1 if sa[0] * sb[1] - sa[1] * sb[0] > 0 else 0
                self.el.append(f'<path class="qf-arc" d="M{a[0]:.1f} {a[1]:.1f} A{rr * self.S:.1f} {rr * self.S:.1f} 0 0 {sweep} {b[0]:.1f} {b[1]:.1f}"/>')
        if label:
            m = _u((0, 0), (u1[0] + u2[0], u1[1] + u2[1]))
            d = r + 0.55 + 0.05 * len(label)
            self.text((v[0] + d * m[0], v[1] + d * m[1] - 0.08), label, "qf-acc" if acc else "qf-sm")

    def ticks(self, a, b, n=1):
        u = _u(a, b); nx, ny = -u[1], u[0]
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        for k in range(n):
            o = (k - (n - 1) / 2) * 0.13
            cx, cy = mx + o * u[0], my + o * u[1]
            self.seg((cx - 0.17 * nx, cy - 0.17 * ny), (cx + 0.17 * nx, cy + 0.17 * ny), "qf-mark")

    def svg(self, w=None):
        xs = [p[0] for p in self.pts]; ys = [p[1] for p in self.pts]
        pad = 10
        x0, y0 = min(xs) - pad, min(ys) - pad
        vw, vh = max(xs) - min(xs) + 2 * pad, max(ys) - min(ys) + 2 * pad
        k = min(1.0, 150 / vh)   # display scale; labels keep their size
        txt = "".join(f"{a}{fs / k:.1f}{b}" for a, fs, b in self.txt)
        return (f'<svg class="il qf" viewBox="{x0:.0f} {y0:.0f} {vw:.0f} {vh:.0f}" style="height:{min(vh, 150):.0f}px;--k:{k:.2f}" direction="ltr" '
                f'role="img" aria-hidden="true">{"".join(self.el)}{txt}</svg>')


def _c(*ps):
    return sum(p[0] for p in ps) / len(ps), sum(p[1] for p in ps) / len(ps)


# ---------------------------------------------------------------- triangles
def triangle(alpha, beta, names="ABC", labels=("", "", ""), right=(), sides=(), ticks=(), base=5.5):
    """labels: angle labels at A, B, C (e.g. '40°' or '?'). sides: {(i,j): text}. ticks: [(i, j, n)]."""
    A, B, C = tri(alpha, beta, base)
    V = [A, B, C]
    f = Fig(); f.poly(A, B, C); g = _c(A, B, C)
    for i in range(3):
        o = [V[j] for j in range(3) if j != i]
        if i in right:
            f.angle(V[i], o[0], o[1], right=True)
        elif labels[i]:
            f.angle(V[i], o[0], o[1], labels[i], r=0.62)
    for (i, j, n) in ticks:
        f.ticks(V[i], V[j], n)
    for (i, j), s in dict(sides).items():
        m = ((V[i][0] + V[j][0]) / 2, (V[i][1] + V[j][1]) / 2); u = _u(g, m)
        f.text((m[0] + 0.45 * u[0], m[1] + 0.45 * u[1] - 0.1), s, "qf-sm")
    for i in range(3):
        f.name(V[i], names[i], g)
    return f.svg()


def iso(apex, lab_apex, lab_base="?", names="ABC", extra=None):
    """Isosceles triangle, apex names[0] on top, base names[1]names[2]."""
    b = (180 - apex) / 2
    B, C, A = tri(b, b, 5.5)
    f = Fig(); f.poly(A, B, C); g = _c(A, B, C)
    f.ticks(A, B); f.ticks(A, C)
    f.angle(A, B, C, lab_apex, r=0.55)
    f.angle(B, A, C, lab_base, r=0.6); f.angle(C, A, B, lab_base, r=0.6)
    if extra:
        extra(f, A, B, C)
    for p, s in zip((A, B, C), names):
        f.name(p, s, g)
    return f.svg()


def pair(kind):
    """Two congruent triangles ABC and DEF with the marks of one congruence case."""
    f = Fig()
    for off, nm in ((0, "ABC"), (6.6, "DEF")):
        A, B, C = tri(62, 48, 5.0)
        A, B, C = [(p[0] + off, p[1]) for p in (A, B, C)]
        f.poly(A, B, C); g = _c(A, B, C)
        if kind == "SAS":    # AB, angle B, BC
            f.ticks(A, B, 1); f.ticks(B, C, 2); f.angle(B, A, C, r=0.6)
        elif kind == "SSS":
            f.ticks(A, B, 1); f.ticks(B, C, 2); f.ticks(A, C, 3)
        elif kind == "ASA":  # angle A, AB, angle B
            f.angle(A, B, C, r=0.6); f.angle(B, A, C, r=0.6, n=2); f.ticks(A, B, 1)
        for p, s in zip((A, B, C), nm):
            f.name(p, s, g)
    return f.svg(290)


def midpoint_x():
    """[AB] and [CD] cut at their common midpoint M: triangles AMC and BMD."""
    M = (0, 0); A = _deg(M, 160, 3); B = _deg(M, -20, 3); C = _deg(M, 110, 2.2); D = _deg(M, -70, 2.2)
    f = Fig(); f.poly(A, M, C); f.poly(B, M, D)
    f.seg(A, B); f.seg(C, D); f.seg(A, C); f.seg(B, D)
    f.ticks(A, M, 1); f.ticks(M, B, 1); f.ticks(C, M, 2); f.ticks(M, D, 2)
    f.angle(M, A, C, r=0.5); f.angle(M, B, D, r=0.5)
    for p, s in ((A, "A"), (B, "B"), (C, "C"), (D, "D")):
        f.name(p, s, M)
    f.text((0.45, -0.05), "M")
    f.dot(M)
    return f.svg(230)


def iso_height(name="H", with_marks=True):
    B, C, A = tri(65, 65, 5.0)
    H = ((B[0] + C[0]) / 2, 0.0)
    f = Fig(); f.poly(A, B, C); f.seg(A, H, "qf-line2")
    f.ticks(A, B); f.ticks(A, C)
    if with_marks:
        f.angle(H, A, C, right=True)
    else:
        f.ticks(B, H, 2); f.ticks(H, C, 2)
    g = _c(A, B, C)
    for p, s in ((A, "A"), (B, "B"), (C, "C")):
        f.name(p, s, g)
    f.text((H[0], H[1] - 0.45), name); f.dot(H)
    return f.svg(200)


def altitude():
    """Triangle ABC with the height [AH], B = 50°."""
    B, C, A = tri(50, 70, 5.5)
    H = (A[0], 0.0)
    f = Fig(); f.poly(A, B, C); f.seg(A, H, "qf-line2")
    f.angle(H, A, C, right=True); f.angle(B, A, C, "50°", r=0.7); f.angle(A, B, H, "?", r=0.7)
    g = _c(A, B, C)
    for p, s in ((A, "A"), (B, "B"), (C, "C")):
        f.name(p, s, g)
    f.text((H[0], -0.45), "H"); f.dot(H)
    return f.svg(210)


def iso_bisector(apex, lab_apex, ask):
    """Isosceles ABC (apex A), [BM] bisects angle B; M on [AC]."""
    b = (180 - apex) / 2
    B, C, A = tri(b, b, 5.5)
    # M on AC with angle ABM = b/2
    t = 5.5 * math.sin(math.radians(b)) / math.sin(math.radians(b / 2 + b))
    M = _deg(B, b / 2, t)
    f = Fig(); f.poly(A, B, C); f.seg(B, M, "qf-line2")
    f.ticks(A, B); f.ticks(A, C)
    f.angle(A, B, C, lab_apex, r=0.5)
    f.angle(B, A, M, ask[0], r=1.0, acc=ask[0] == "?"); f.angle(B, M, C, ask[1], r=1.35, acc=ask[1] == "?")
    g = _c(A, B, C)
    for p, s in ((A, "A"), (B, "B"), (C, "C")):
        f.name(p, s, g)
    f.name(M, "M", g); f.dot(M)
    return f.svg(220)


def circum():
    A, B, C = tri(58, 50, 5.6)
    f = Fig(); f.poly(A, B, C)
    ab = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2); ac = ((A[0] + C[0]) / 2, (A[1] + C[1]) / 2)
    # circumcentre
    ax, ay = A; bx, by = B; cx, cy = C
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax ** 2 + ay ** 2) * (by - cy) + (bx ** 2 + by ** 2) * (cy - ay) + (cx ** 2 + cy ** 2) * (ay - by)) / d
    uy = ((ax ** 2 + ay ** 2) * (cx - bx) + (bx ** 2 + by ** 2) * (ax - cx) + (cx ** 2 + cy ** 2) * (bx - ax)) / d
    G = (ux, uy)
    for m, (p, q) in ((ab, (A, B)), (ac, (A, C))):
        u = _u(m, G)
        f.seg((m[0] - 0.9 * u[0], m[1] - 0.9 * u[1]), (G[0] + 1.2 * u[0], G[1] + 1.2 * u[1]), "qf-line2")
        f.angle(m, q, G, right=True)
    f.ticks(A, ab); f.ticks(ab, B); f.ticks(A, ac, 2); f.ticks(ac, C, 2)
    g = _c(A, B, C)
    for p, s in ((A, "A"), (B, "B"), (C, "C")):
        f.name(p, s, g)
    f.dot(G); f.text((G[0] + 0.35, G[1] + 0.3), "G")
    return f.svg(210)


# ---------------------------------------------------------------- lines & angles
def parallels(ang=50, show=("AGH",), q=()):
    """(AB) ∥ (CD) cut by (EF) at G and H. show/q: angles to mark with the value / with '?'."""
    th = math.radians(ang)
    G = (0.0, 2.2); H = (G[0] - 2.2 / math.tan(th), 0.0)
    u = _u(H, G)
    E = (G[0] + 1.3 * u[0], G[1] + 1.3 * u[1]); F = (H[0] - 1.3 * u[0], H[1] - 1.3 * u[1])
    A, B, C, D = (-3.6, 2.2), (2.8, 2.2), (-3.6 - 1.6, 0.0), (2.8 - 1.6, 0.0)
    f = Fig()
    f.seg(A, B, "qf-line"); f.seg(C, D, "qf-line"); f.seg(E, F, "qf-line2")
    pts = {"A": A, "B": B, "C": C, "D": D, "E": E, "F": F, "G": G, "H": H}
    for key in list(show) + list(q):
        a, v, b = key
        f.angle(pts[v], pts[a], pts[b], f"{ang}°" if key in show else "?", r=0.5,
                acc=key in q)
    for s, p, d in (("A", A, (-0.3, 0.1)), ("B", B, (0.3, 0.1)), ("C", C, (-0.3, 0.1)), ("D", D, (0.3, 0.1)),
                    ("E", E, (0.2, 0.3)), ("F", F, (-0.2, -0.35)), ("G", G, (-0.4, 0.35)), ("H", H, (0.45, -0.35))):
        f.text((p[0] + d[0], p[1] + d[1] - 0.05), s, "qf-sm" if s in "ABCDEF" else "")
    f.dot(G); f.dot(H)
    return f.svg(260)


def linear_pair(a=135):
    O = (0, 0)
    f = Fig(); f.seg((-3, 0), (3, 0), "qf-line"); f.seg(O, _deg(O, a, 2.4), "qf-line2")
    f.angle(O, (3, 0), _deg(O, a, 2), f"{a}°", r=0.55, acc=False)
    f.angle(O, _deg(O, a, 2), (-3, 0), "x", r=0.8)
    f.dot(O)
    return f.svg(220)


def vertical(a=65):
    O = (0, 0)
    f = Fig()
    f.seg(_deg(O, 180 + 20, 2.6), _deg(O, 20, 2.6), "qf-line"); f.seg(_deg(O, 180 + 20 + a, 2.6), _deg(O, 20 + a, 2.6), "qf-line2")
    f.angle(O, _deg(O, 20, 1), _deg(O, 20 + a, 1), f"{a}°", r=0.55, acc=False)
    f.angle(O, _deg(O, 200, 1), _deg(O, 200 + a, 1), "?", r=0.55)
    f.dot(O)
    return f.svg(200)


def trapezoid(D=120, C=126, bis=False):
    """ABCD with (AB) ∥ (DC), D and C at the bottom."""
    Dp, Cp = (0, 0), (6.0, 0)
    h = 2.2
    A = (Dp[0] - h / math.tan(math.radians(D)), h)
    B = (Cp[0] + h / math.tan(math.radians(C)), h)
    f = Fig(); f.poly(A, B, Cp, Dp)
    f.angle(Dp, Cp, A, f"{D}°", r=0.55, acc=False); f.angle(Cp, B, Dp, f"{C}°", r=0.55, acc=False)
    g = _c(A, B, Cp, Dp)
    if bis:
        # bisectors from D and C meet at I
        dI = D / 2
        t = 6.0 * math.sin(math.radians(C / 2)) / math.sin(math.radians(D / 2 + C / 2))
        I = _deg(Dp, dI, t)
        f.seg(Dp, I, "qf-line2"); f.seg(Cp, I, "qf-line2"); f.dot(I)
        f.angle(I, Dp, Cp, "?", r=0.4); f.text((I[0], I[1] + 0.4), "I")
    else:
        f.angle(A, Dp, B, "?", r=0.55); f.angle(B, A, Cp, "?", r=0.55)
    for p, s in ((A, "A"), (B, "B"), (Cp, "C"), (Dp, "D")):
        f.name(p, s, g)
    return f.svg(250)


def parallelogram(a=140):
    D, C = (0, 0), (5.0, 0)
    v = _deg((0, 0), 180 - a, 2.4)
    A, B = v, (v[0] + 5.0, v[1])
    f = Fig(); f.poly(A, B, C, D)
    f.ticks(A, B); f.ticks(D, C); f.ticks(A, D, 2); f.ticks(B, C, 2)
    f.angle(A, B, D, f"{a}°", r=0.5, acc=False); f.angle(D, A, C, "?", r=0.55)
    g = _c(A, B, C, D)
    for p, s in ((A, "A"), (B, "B"), (C, "C"), (D, "D")):
        f.name(p, s, g)
    return f.svg(230)


def tri_ray():
    """ABC with BAC=80, ACB=50 and a ray [BD) (D on [AC]) with DBC=25."""
    B, C, A = tri(50, 50, 5.5)
    t = 5.5 * math.sin(math.radians(50)) / math.sin(math.radians(25 + 50))
    D = _deg(B, 25, t)
    f = Fig(); f.poly(A, B, C); f.seg(B, D, "qf-line2")
    f.angle(A, B, C, "80°", r=0.5, acc=False); f.angle(C, A, B, "50°", r=0.6, acc=False)
    f.angle(B, D, C, "25°", r=1.4, acc=False); f.angle(B, A, D, "?", r=0.9)
    g = _c(A, B, C)
    for p, s in ((A, "A"), (B, "B"), (C, "C")):
        f.name(p, s, g)
    f.name(D, "D", g); f.dot(D)
    return f.svg(220)


def alt_parallel():
    """ABC with BAC = 80°, and [CX) such that ACX = 80°: (AB) ∥ (CX)."""
    A, B, C = tri(80, 45, 5.0)
    X = (C[0] + 3.0, C[1])
    f = Fig(); f.poly(A, B, C); f.seg(C, X, "qf-line2")
    f.angle(A, B, C, "80°", r=0.55, acc=False); f.angle(C, A, X, "80°", r=0.55)
    g = _c(A, B, C)
    for p, s in ((A, "A"), (B, "B"), (C, "C")):
        f.name(p, s, g)
    f.text((X[0] + 0.3, X[1] + 0.05), "X")
    return f.svg(230)


# ---------------------------------------------------------------- bisectors
def perp(lab_a, lab_b, P="M"):
    A, B = (-2.6, 0), (2.6, 0)
    I = (0, 0); M = (0, 2.4)
    f = Fig(); f.seg(A, B)
    f.seg((0, -1.0), (0, 3.2), "qf-line2"); f.text((0.35, 3.1), "(Δ)", "qf-sm")
    f.angle(I, B, M, right=True); f.ticks(A, I); f.ticks(I, B)
    f.seg(M, A, "qf-edge qf-dash"); f.seg(M, B, "qf-edge qf-dash")
    for p in (A, B, M, I):
        f.dot(p)
    f.text((A[0] - 0.3, A[1] - 0.05), "A"); f.text((B[0] + 0.3, B[1] - 0.05), "B"); f.text((M[0] - 0.4, M[1] + 0.2), P)
    f.text((-1.6, 1.55), lab_a, "qf-acc"); f.text((1.6, 1.55), lab_b, "qf-acc")
    return f.svg(210)


def angle_bis(lab_all, lab_half, names=("x", "O", "y", "z")):
    O = (0, 0); X = _deg(O, 0, 4); Y = _deg(O, 76, 3.2); Z = _deg(O, 38, 3.6)
    f = Fig(); f.seg(O, X, "qf-line"); f.seg(O, Y, "qf-line"); f.seg(O, Z, "qf-line2")
    f.angle(O, X, Z, lab_half[0], r=1.0, acc=lab_half[0] == "?"); f.angle(O, Z, Y, lab_half[1], r=1.0, n=1, acc=lab_half[1] == "?")
    if lab_all:
        f.angle(O, X, Y, lab_all, r=1.9, acc=lab_all == "?")
    f.dot(O)
    f.text((-0.3, -0.3), names[1]); f.text((X[0] + 0.3, X[1] - 0.05), names[0], "qf-sm")
    f.text((Y[0] + 0.1, Y[1] + 0.3), names[2], "qf-sm"); f.text((Z[0] + 0.3, Z[1] + 0.1), names[3], "qf-sm")
    return f.svg(200)


QFIGS = {
    # L11 triangles
    "t-50-70": lambda: triangle(50, 70, labels=("50°", "70°", "?")),
    "t-45-75": lambda: triangle(45, 75, labels=("45°", "75°", "?")),
    "t-efg": lambda: triangle(40, 70, names="FGE", labels=("40°", "70°", "?"), sides={(0, 1): "6"}),
    "t-iso-right": lambda: triangle(45, 45, labels=("?", "?", ""), right=(2,), ticks=((0, 2, 1), (1, 2, 1)), names="BCA",
                                    sides={(0, 2): "4", (1, 2): "4"}),
    "t-bc55": lambda: triangle(55, 55, names="BCA", labels=("55°", "55°", "?"), sides={(0, 1): "5"}),
    "t-right-b50": lambda: triangle(90, 50, names="ABC", labels=("", "50°", "?"), right=(0,)),
    "iso-40": lambda: iso(40, "40°"),
    "iso-100": lambda: iso(100, "100°"),
    "sas": lambda: pair("SAS"), "sss": lambda: pair("SSS"), "asa": lambda: pair("ASA"),
    "mid-x": midpoint_x,
    "iso-height": lambda: iso_height("H", True),
    "iso-mid": lambda: iso_height("M", False),
    # L12 angles
    "par-agh": lambda: parallels(50, show=("AGH",), q=("GHD", "GHC")),
    "par-ex": lambda: parallels(50, show=("AGH",), q=("EGB", "GHD", "CHG")),
    "par-agh-chf": lambda: parallels(55, show=(), q=("AGH", "CHF")),
    "lin-135": lambda: linear_pair(135),
    "vert-65": lambda: vertical(65),
    "trap": lambda: trapezoid(120, 126),
    "trap-bis": lambda: trapezoid(120, 126, bis=True),
    "para-140": lambda: parallelogram(140),
    "tri-ray": tri_ray,
    "alt-par": alt_parallel,
    # L13 bisectors
    "perp-7": lambda: perp("7 cm", "?"),
    "perp-9": lambda: perp("9", "?"),
    "perp-45": lambda: perp("4.5 cm", "?"),
    "perp-x": lambda: perp("2x+3", "11"),
    "perp-x2": lambda: perp("3x+1", "10"),
    "perp-c": lambda: perp("", "", "C"),
    "perp-5": lambda: perp("5", "?"),
    "bis-84": lambda: angle_bis("84°", ("?", "")),
    "bis-76": lambda: angle_bis("76°", ("?", "")),
    "bis-38": lambda: angle_bis("?", ("38°", ""), names=("A", "B", "C", "D")),
    "bis-70": lambda: angle_bis("70°", ("?", "?"), names=("A", "B", "C", "D")),
    "altitude": altitude,
    "iso-bis-100": lambda: iso_bisector(100, "100°", ("?", "")),
    "iso-bis-40": lambda: iso_bisector(40, "40°", ("", "?")),
    "circum": circum,
}


def render(key):
    return f'<span class="qfig">{QFIGS[key]()}</span>'
