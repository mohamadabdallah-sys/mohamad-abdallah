# -*- coding: utf-8 -*-
"""Front and back cover (build/cover.html, two 170×240 mm pages): a conceptual illustrated cover —
a traveller with his provision crossing dunes at dusk towards a great pale disc, hazy warm light,
a heavy display title at the top and the author at the foot."""
import os, re, math, random

HERE = os.path.dirname(os.path.abspath(__file__))

BACK_TEXT = [
    "أنا حلم النّيام، وخديعة الأيّام؛ من استغنى فيّ فتن، ومن افتقر إليّ حزن. "
    "فاحذرني، فإنّ بقاءك فيّ كفيء السّحاب ووميض السّراب. "
    "لو كنت وفيّةً لمّا خلّفت مقعد حبيب ربّ العالمين، ولو كنت نافعةً لمّا نصبت الشّراك للغافلين. "
    "طويت القرون في جوفي، وأذقت الجبابرة كأساً من خوفي؛ لا رضيعي سلم، ولا معمّري غنم.",
    "فيا من ملّكه الأمل وطول المهلة: بادر العمل قبل خفوت القبس؛ "
    "فما الأيّام إلّا مراحل تطوى إلى القبور، وما الفوز إلّا لمن خاف العبور، "
    "يوم ينكشف المستور ويحصّل ما في الصّدور.",
]
TITLE_HTML = ("ثرائد", "التّقوى")
AUTHOR = "محمّد عبدالله"

VW, VH = 680, 960            # 4 units per mm


def plain(s):
    """the cover uses the book's vocalisation: shadda and tanween only"""
    return re.sub("[\u064E-\u0650\u0652\u0670\u0640]", "", s)


def ridge(y0, amp, seed, n=9, bottom=VH + 10, shift=0.0):
    """a wind-swept dune line as a closed path (smooth cubic curve through random crests)"""
    rnd = random.Random(seed)
    xs = [-20 + i * (VW + 40) / n for i in range(n + 1)]
    ys = [y0 + amp * math.sin(i * 1.3 + shift) * 0.6 + rnd.uniform(-amp, amp) * 0.5 for i in range(n + 1)]
    d = "M %.1f %.1f " % (xs[0], ys[0])
    for i in range(1, n + 1):
        cx = (xs[i - 1] + xs[i]) / 2
        d += "C %.1f %.1f %.1f %.1f %.1f %.1f " % (cx, ys[i - 1], cx, ys[i], xs[i], ys[i])
    return d + "L %.1f %.1f L %.1f %.1f Z" % (xs[-1], bottom, xs[0], bottom), (xs, ys)


def traveller(x, y, s=1.0, col="#1a1218"):
    """a small cloaked figure with a staff and a bundle on the back, seen from the side (facing left)"""
    g = '<g transform="translate(%.1f %.1f) scale(%.2f)" fill="%s">' % (x, y, s, col)
    g += '<path d="M0 0 C-3 -10 -4 -22 -2 -34 C-1 -40 3 -44 7 -43 C11 -42 12 -37 11 -33 C14 -24 14 -10 15 0 Z"/>'      # cloak
    g += '<circle cx="5" cy="-50" r="6.3"/>'                                                                          # head
    g += '<path d="M-1 -41 C-9 -42 -14 -35 -12 -27 C-8 -26 -4 -29 0 -33 Z"/>'                                       # bundle
    g += '<rect x="-18" y="-60" width="2.4" height="62" rx="1.2" transform="rotate(7 -17 -30)"/>'                    # staff
    g += '<path d="M2 0 L-4 0 L-7 4 L6 4 Z"/>'
    return g + "</g>"


def catmull(pts, n=200):
    """a smooth curve through the given points (Catmull-Rom), as n samples"""
    P = [pts[0]] + pts + [pts[-1]]
    out = []
    segs = len(pts) - 1
    for k in range(segs):
        p0, p1, p2, p3 = P[k], P[k + 1], P[k + 2], P[k + 3]
        for t in [i / (n // segs) for i in range(n // segs)]:
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[a]) + (-p0[a] + p2[a]) * t + (2 * p0[a] - 5 * p1[a] + 4 * p2[a] - p3[a]) * t2
                                    + (-p0[a] + 3 * p1[a] - 3 * p2[a] + p3[a]) * t3) for a in (0, 1)))
    out.append(pts[-1])
    return out


def crumb(cx, cy, r, rnd, fill):
    """one irregular piece of bread"""
    n = rnd.choice((5, 6, 7))
    a0 = rnd.uniform(0, 6.28)
    pts = []
    for i in range(n):
        a = a0 + i * 2 * math.pi / n + rnd.uniform(-0.25, 0.25)
        rr = r * rnd.uniform(0.62, 1.12)
        pts.append("%.1f,%.1f" % (cx + rr * math.cos(a), cy + rr * math.sin(a) * 0.82))
    return '<polygon points="%s" fill="%s"/>' % (" ".join(pts), fill)


def star4(x, y, r, fill, op=1.0):
    k = r * 0.22
    d = "M %.1f %.1f L %.1f %.1f L %.1f %.1f L %.1f %.1f L %.1f %.1f L %.1f %.1f L %.1f %.1f L %.1f %.1f Z" % (
        x, y - r, x + k, y - k, x + r, y, x + k, y + k, x, y + r, x - k, y + k, x - r, y, x - k, y - k)
    return '<path d="%s" fill="%s" opacity="%.2f"/>' % (d, fill, op)


def bread(x, y, r, rnd, base="#d9a35f", light="#f3d49a", dark="#a8702f"):
    """a flat piece of bread: shadow, body, lit facet"""
    n = rnd.choice((5, 6, 7))
    a0 = rnd.uniform(0, 6.28)
    P = []
    for i in range(n):
        a = a0 + i * 2 * math.pi / n + rnd.uniform(-0.28, 0.28)
        rr = r * rnd.uniform(0.6, 1.1)
        P.append((rr * math.cos(a), rr * math.sin(a) * 0.85))
    f = lambda pts, dx=0, dy=0, k=1.0: " ".join("%.1f,%.1f" % (x + dx + p[0] * k, y + dy + p[1] * k) for p in pts)
    return ('<polygon points="%s" fill="#06292e" opacity="0.28"/>' % f(P, r * 0.18, r * 0.28) +
            '<polygon points="%s" fill="%s"/>' % (f(P), base) +
            '<polygon points="%s" fill="%s"/>' % (f(P[: max(3, n // 2 + 1)] + [(0, 0)], -r * 0.05, -r * 0.08, 0.95), light) +
            '<polygon points="%s" fill="%s" opacity="0.55"/>' % (f(P[n // 2:] + [P[0], (0, 0)], 0, 0, 0.98), dark))


BEIGE, SAND, TURQ, DEEP, INK = "#eadfc8", "#d9c8a5", "#19a7a1", "#0c5d63", "#062f35"


def blob(x, y, r, rnd, fill, rot=None):
    """a small rounded crumb"""
    n = 7
    a0 = rnd.uniform(0, 6.28) if rot is None else rot
    P = []
    for k in range(n):
        a = a0 + k * 2 * math.pi / n
        rr = r * rnd.uniform(0.78, 1.08)
        P.append((x + rr * math.cos(a), y + rr * math.sin(a) * 0.86))
    d = "M %.1f %.1f " % ((P[0][0] + P[-1][0]) / 2, (P[0][1] + P[-1][1]) / 2)
    for k in range(n):
        q, nx = P[k], P[(k + 1) % n]
        d += "Q %.1f %.1f %.1f %.1f " % (q[0], q[1], (q[0] + nx[0]) / 2, (q[1] + nx[1]) / 2)
    return '<path d="%sZ" fill="%s"/>' % (d, fill)


def spiral(cx, cy, n, spread, rnd, inner, R, big, back=False):
    """crumbs along the golden-angle spiral: bread inside the bowl, stars once they leave it"""
    out = []
    ga = math.pi * (3 - math.sqrt(5))
    for i in range(1, n):
        r = spread * math.sqrt(i)
        a = i * ga
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        if r < R - 12:
            t = r / R
            size = big * (0.25 + 0.75 * t ** 0.9)
            col = "#fff1c9" if t < 0.18 else ("#f6cd7d" if t < 0.55 else "#e0a14e")
            out.append('<g opacity="0.25"><path d="M0 0" /></g>' if False else blob(x + 1.4, y + 2.2, size, rnd, "#06292e"))
            out.append(blob(x, y, size, rnd, col))
        else:
            t = min(1.0, (r - R) / 380)
            sz = (1 - t) ** 1.3 * 9.5 + 1.6
            if (y < 835 or back) and rnd.random() < 0.30 * (1 - 0.6 * t) + 0.04:
                out.append(star4(x, y, sz, inner if rnd.random() < 0.7 else "#c9853f", 0.95 - 0.55 * t))
    return "".join(out)


def flat(u, back=False):
    rnd = random.Random(5)
    dark = not back
    b = ["""<defs>
  <radialGradient id="bg{u}" cx="0.5" cy="0.42" r="0.9"><stop offset="0" stop-color="{c0}"/><stop offset="1" stop-color="{c1}"/></radialGradient>
  <radialGradient id="bowl{u}" cx="0.5" cy="0.45" r="0.62"><stop offset="0" stop-color="#2fcbc2"/><stop offset="0.75" stop-color="#17a8a2"/><stop offset="1" stop-color="#0e8a8f"/></radialGradient>
  <filter id="grain{u}" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.75" numOctaves="3" seed="9"/>
    <feColorMatrix type="matrix" values="0 0 0 0 {gn}  0 0 0 0 {gn}  0 0 0 0 {gn}  0 0 0 0.55 -0.12"/>
  </filter>
</defs>""".format(u=u, c0="#0f7377" if dark else "#f3ead7", c1="#06393f" if dark else "#d9ccb0", gn="0.9" if dark else "0.2"),
         '<rect width="%d" height="%d" fill="url(#bg%s)"/>' % (VW, VH, u)]
    if dark:
        cx, cy, R = 340, 628, 196
    else:
        cx, cy, R = 650, 985, 215
    b.append('<circle cx="%d" cy="%d" r="%d" fill="#03242a" opacity="0.35"/>' % (cx + 9, cy + 13, R + 14))
    b.append('<circle cx="%d" cy="%d" r="%d" fill="%s"/>' % (cx, cy, R + 14, "#eadfc8" if dark else "#0c5d63"))
    b.append('<circle cx="%d" cy="%d" r="%d" fill="url(#bowl%s)"/>' % (cx, cy, R, u))
    b.append('<circle cx="%d" cy="%d" r="%.1f" fill="none" stroke="#e9fffb" stroke-width="1" opacity="0.4"/>' % (cx, cy, R - 9))
    star_col = "#f1e6cc" if dark else DEEP
    b.append(spiral(cx, cy, 1700 if dark else 1200, 8.0 if dark else 8.2, rnd, star_col, R, 8.6, back))
    if dark:
        for _ in range(30):
            x, y = rnd.uniform(40, 640), rnd.uniform(30, 330)
            b.append(star4(x, y, rnd.uniform(2.5, 6), "#f1e6cc", 0.55))
    b.append('<rect width="%d" height="%d" filter="url(#grain%s)" opacity="0.5" style="mix-blend-mode:%s"/>' % (VW, VH, u, "screen" if dark else "multiply"))
    return '<svg class="art" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg">%s</svg>' % (VW, VH, "".join(b))


def shrouded_man():
    """a man wrapped in his shroud (kafan), tied at head, knees and feet; his face is split down the middle:
    the left half laughs (the world's illusion), the right half is grim and sunken (the truth)"""
    g = []
    # ground shadow
    g.append('<ellipse cx="340" cy="896" rx="150" ry="17" fill="#021c20" opacity="0.55"/>')
    # body
    body = "M 276 438 C 232 470 218 530 226 610 L 244 846 C 246 884 434 884 436 846 L 454 610 C 462 530 448 470 404 438 Z"
    g.append('<path d="%s" fill="url(#cloth)"/>' % body)
    # shade on the right half of the cloth (the grim side)
    g.append('<path d="%s" fill="#06292e" opacity="0.30" clip-path="url(#rightHalf)"/>' % body)
    # folds
    for d, op in (("M 300 462 C 280 560 294 700 282 850", .55), ("M 336 470 C 330 580 338 720 334 868", .45),
                  ("M 380 464 C 396 570 384 704 396 850", .55), ("M 262 520 C 252 600 262 720 256 840", .35),
                  ("M 416 520 C 428 610 416 720 424 840", .35), ("M 318 590 C 306 640 314 700 304 760", .25),
                  ("M 356 600 C 366 650 358 704 368 766", .25)):
        g.append('<path d="%s" fill="none" stroke="#a89a74" stroke-width="3" stroke-linecap="round" opacity="%.2f"/>' % (d, op))
    # the hands crossed under the cloth (a soft bulge on the chest)
    g.append('<path d="M 298 560 Q 340 538 384 560 Q 340 586 298 560 Z" fill="#c9bc98" opacity="0.5"/>')
    # ties: knees and feet
    for y, w in ((720, 9), (836, 9)):
        g.append('<path d="M %d %d Q 340 %d %d %d" fill="none" stroke="#b39d6a" stroke-width="%d" stroke-linecap="round"/>' % (240 if y < 800 else 244, y, y + 24, 440 if y < 800 else 436, y, w))
    # gathered cloth below the feet, tied
    g.append('<path d="M 300 846 L 268 902 Q 300 888 340 904 Q 380 888 412 902 L 380 846 Z" fill="url(#cloth)"/>')
    g.append('<path d="M 340 850 L 340 904" stroke="#a89a74" stroke-width="2.5" opacity="0.6"/>')
    # neck tie
    pass
    # the hood and the knot above the head
    g.append('<g transform="translate(340 366) scale(1.2) translate(-340 -366)">')
    g.append('<path d="M 306 282 Q 340 226 374 282 Q 340 270 306 282 Z" fill="url(#cloth)"/>')
    g.append('<path d="M 310 284 Q 340 300 370 284" fill="none" stroke="#b39d6a" stroke-width="9" stroke-linecap="round"/>')
    g.append('<ellipse cx="340" cy="362" rx="82" ry="98" fill="url(#cloth)"/>')
    g.append('<ellipse cx="340" cy="362" rx="82" ry="98" fill="#06292e" opacity="0.30" clip-path="url(#rightHalf)"/>')
    # the face opening
    g.append('<ellipse cx="340" cy="366" rx="58" ry="72" fill="#4a3a28" opacity="0.55"/>')
    face = []
    face.append('<g clip-path="url(#leftHalf)">')
    face.append('<ellipse cx="340" cy="366" rx="54" ry="68" fill="url(#skinL)"/>')
    face.append('<ellipse cx="304" cy="388" rx="15" ry="11" fill="#f0897b" opacity="0.55"/>')                       # flushed cheek
    face.append('<path d="M 291 338 Q 311 320 335 330" fill="none" stroke="#3b2418" stroke-width="5" stroke-linecap="round"/>')   # raised brow
    face.append('<path d="M 297 356 Q 313 340 331 356" fill="none" stroke="#2a1810" stroke-width="5" stroke-linecap="round"/>')   # laughing eye
    face.append('<path d="M 292 360 l-6 -4 M 293 366 l-7 0" stroke="#7a4a30" stroke-width="2" stroke-linecap="round"/>')
    face.append('<path d="M 339 356 Q 334 380 326 388" fill="none" stroke="#a8683e" stroke-width="3" stroke-linecap="round"/>')   # nose
    face.append('<path d="M 340 400 Q 318 398 298 388 Q 306 432 340 436 Z" fill="#5a1420"/>')                       # open laughing mouth
    face.append('<path d="M 340 400 Q 318 398 298 388 Q 312 408 340 410 Z" fill="#fffaf0"/>')                       # teeth
    face.append('<path d="M 340 424 Q 322 426 310 418 Q 322 432 340 432 Z" fill="#d9605f"/>')                       # tongue
    face.append('<path d="M 296 384 Q 290 396 298 408" fill="none" stroke="#a8683e" stroke-width="2.6" stroke-linecap="round"/>')  # laugh line
    face.append('</g>')
    face.append('<g clip-path="url(#rightHalf)">')
    face.append('<ellipse cx="340" cy="366" rx="54" ry="68" fill="url(#skinR)"/>')
    face.append('<ellipse cx="373" cy="392" rx="15" ry="26" fill="#1a2420" opacity="0.38"/>')                       # hollow cheek
    face.append('<path d="M 346 326 Q 368 322 390 342" fill="none" stroke="#1d2622" stroke-width="6" stroke-linecap="round"/>')    # heavy brow
    face.append('<ellipse cx="368" cy="352" rx="17" ry="12" fill="#1c2523"/>')                                       # sunken eye
    face.append('<circle cx="368" cy="353" r="4.2" fill="#c9d1c3"/>')
    face.append('<path d="M 350 366 Q 368 380 388 364" fill="none" stroke="#2c3733" stroke-width="3.4" stroke-linecap="round"/>')   # bags
    face.append('<path d="M 340 356 Q 346 380 356 388" fill="none" stroke="#3b4638" stroke-width="3" stroke-linecap="round"/>')    # nose
    face.append('<path d="M 340 414 Q 362 408 384 430" fill="none" stroke="#1a1f1c" stroke-width="5.5" stroke-linecap="round"/>')  # downturned mouth
    face.append('<path d="M 340 420 Q 356 418 372 432" fill="none" stroke="#5d6b5a" stroke-width="2" opacity="0.7"/>')
    face.append('<path d="M 356 302 l8 11 -6 9 9 8 M 380 322 l-6 10" fill="none" stroke="#2d3731" stroke-width="2" stroke-linecap="round" opacity="0.8"/>')  # cracks
    face.append('<path d="M 384 384 Q 392 398 386 410" fill="none" stroke="#2d3731" stroke-width="2.4" stroke-linecap="round"/>')
    face.append('</g>')
    g.append("".join(face))
    g.append('<ellipse cx="340" cy="366" rx="54" ry="68" fill="none" stroke="#2a1c10" stroke-width="2" opacity="0.7"/>')
    g.append('<line x1="340" y1="298" x2="340" y2="434" stroke="#241a12" stroke-width="1.2" opacity="0.35"/>')
    g.append('</g>')
    g.append('<path d="M 262 478 Q 340 512 418 478" fill="none" stroke="#b39d6a" stroke-width="11" stroke-linecap="round"/>')
    g.append('<circle cx="340" cy="500" r="10" fill="#b39d6a"/>')
    return "".join(g)


def duality_front(u):
    rnd = random.Random(3)
    b = ["""<defs>
  <linearGradient id="bgL{u}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#35c3ba"/><stop offset="1" stop-color="#1b9a97"/></linearGradient>
  <linearGradient id="bgR{u}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a4a51"/><stop offset="1" stop-color="#021c20"/></linearGradient>
  <linearGradient id="cloth" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fbf6e8"/><stop offset="1" stop-color="#e2d6b8"/></linearGradient>
  <radialGradient id="skinL" cx="0.35" cy="0.4" r="0.8"><stop offset="0" stop-color="#ffd9b0"/><stop offset="1" stop-color="#eaa877"/></radialGradient>
  <radialGradient id="skinR" cx="0.7" cy="0.4" r="0.85"><stop offset="0" stop-color="#a3ad98"/><stop offset="1" stop-color="#5d6a5d"/></radialGradient>
  <linearGradient id="fade{u}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffffff"/><stop offset="0.38" stop-color="#ffffff"/><stop offset="0.62" stop-color="#000000"/><stop offset="1" stop-color="#000000"/></linearGradient>
  <mask id="mL{u}"><rect width="680" height="960" fill="url(#fade{u})"/></mask>
  <clipPath id="leftHalf"><rect x="0" y="0" width="340" height="960"/></clipPath>
  <clipPath id="rightHalf"><rect x="340" y="0" width="340" height="960"/></clipPath>
  <radialGradient id="halo{u}" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#fff3d2" stop-opacity="0.55"/><stop offset="1" stop-color="#fff3d2" stop-opacity="0"/></radialGradient>
  <filter id="grain{u}" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.75" numOctaves="3" seed="9"/>
    <feColorMatrix type="matrix" values="0 0 0 0 0.9  0 0 0 0 0.9  0 0 0 0 0.9  0 0 0 0.5 -0.1"/>
  </filter>
</defs>""".format(u=u)]
    b.append('<rect width="680" height="960" fill="url(#bgR%s)"/>' % u)
    b.append('<rect width="680" height="960" fill="url(#bgL%s)" mask="url(#mL%s)"/>' % (u, u))
    b.append('<circle cx="340" cy="560" r="330" fill="url(#halo%s)"/>' % u)
    # stars on the dark side, soft sparkles on the light side
    for _ in range(46):
        x, y = rnd.uniform(380, 660), rnd.uniform(240, 900)
        b.append(star4(x, y, rnd.uniform(2, 5.5), "#f1e6cc", rnd.uniform(0.25, 0.7)))
    for _ in range(26):
        x, y = rnd.uniform(20, 300), rnd.uniform(240, 900)
        b.append(star4(x, y, rnd.uniform(2, 6), "#fff3d2", rnd.uniform(0.3, 0.75)))
    b.append('<g transform="translate(57.8 86) scale(0.83)">%s</g>' % shrouded_man())
    b.append('<rect width="680" height="960" filter="url(#grain%s)" opacity="0.5" style="mix-blend-mode:soft-light"/>' % u)
    return '<svg class="art" viewBox="0 0 680 960" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg">%s</svg>' % "".join(b)


def emblem_back(u):
    """the back: warm paper with a small two-faced circle, light and dark halves"""
    b = ["""<defs>
  <radialGradient id="bg{u}" cx="0.5" cy="0.4" r="0.9"><stop offset="0" stop-color="#f3ead7"/><stop offset="1" stop-color="#d9ccb0"/></radialGradient>
  <filter id="grain{u}" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.75" numOctaves="3" seed="9"/>
    <feColorMatrix type="matrix" values="0 0 0 0 0.2  0 0 0 0 0.2  0 0 0 0 0.12  0 0 0 0.5 -0.12"/>
  </filter>
</defs>""".format(u=u),
         '<rect width="680" height="960" fill="url(#bg%s)"/>' % u]
    cx, cy, r = 340, 770, 54
    b.append('<path d="M %d %d A %d %d 0 0 0 %d %d Z" fill="#2fb9b0"/>' % (cx, cy - r, r, r, cx, cy + r))
    b.append('<path d="M %d %d A %d %d 0 0 1 %d %d Z" fill="#063239"/>' % (cx, cy - r, r, r, cx, cy + r))
    b.append('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="#063239" stroke-width="2"/>' % (cx, cy, r))
    b.append('<path d="M %d %d Q %d %d %d %d" fill="none" stroke="#f6eedc" stroke-width="3.2" stroke-linecap="round"/>' % (cx - 26, cy + 14, cx - 14, cy + 34, cx, cy + 22))
    b.append('<path d="M %d %d Q %d %d %d %d" fill="none" stroke="#f6eedc" stroke-width="3.2" stroke-linecap="round"/>' % (cx, cy + 22, cx + 14, cy + 12, cx + 26, cy + 30))
    b.append('<rect width="680" height="960" filter="url(#grain%s)" opacity="0.5" style="mix-blend-mode:multiply"/>' % u)
    return '<svg class="art" viewBox="0 0 680 960" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg">%s</svg>' % "".join(b)


def main():
    paras = "".join("<p>%s</p>" % plain(t) for t in BACK_TEXT)
    html = """<!doctype html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>الغلاف</title>
<style>
@font-face {{ font-family: "Noto Kufi"; font-weight: 800; src: url(../fonts/noto-kufi-arabic-arabic-800-normal.woff2) format("woff2"); }}
@font-face {{ font-family: "Cairo"; font-weight: 300; src: url(../fonts/cairo-arabic-300-normal.woff2) format("woff2"); }}
@font-face {{ font-family: "Cairo"; font-weight: 400; src: url(../fonts/cairo-arabic-400-normal.woff2) format("woff2"); }}
@font-face {{ font-family: "Cairo"; font-weight: 700; src: url(../fonts/cairo-arabic-700-normal.woff2) format("woff2"); }}
@page {{ size: 170mm 240mm; margin: 0; }}
html, body {{ margin: 0; padding: 0; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.page {{ position: relative; width: 170mm; height: 240mm; overflow: hidden; break-after: page; background: #0b5a60; }}
.art {{ position: absolute; inset: 0; width: 100%; height: 100%; }}

.title {{
  position: absolute; left: 0; right: 0; top: 8mm; text-align: center;
  font-family: "Noto Kufi", sans-serif; font-weight: 800; line-height: 1.0; color: #f6eedc;
  text-shadow: 0 0.5mm 0 #053238, 0 1.1mm 2.4mm rgba(0,0,0,.35);
}}
.title .t1 {{ display: block; font-size: 42pt; color: #f2c97e; }}
.title .t2 {{ display: block; font-size: 84pt; margin-top: 9mm; letter-spacing: -0.5pt; }}
.author {{
  position: absolute; left: 50%; width: 112mm; margin-left: -56mm; bottom: 11mm; text-align: center;
  background: #f6eedc; color: #07383e; border-radius: 40mm; padding: 2.4mm 0 3mm;
  font-family: "Cairo", sans-serif; box-shadow: 0 1mm 3mm rgba(0,0,0,.35);
}}
.author small {{ display: block; font-weight: 700; font-size: 10.5pt; color: #b87a35; line-height: 1.2; }}
.author b {{ display: block; font-weight: 700; font-size: 27pt; line-height: 1.25; font-feature-settings: "rlig" 0, "liga" 0, "calt" 0; }}

.text {{
  position: absolute; left: 22mm; right: 22mm; top: 36mm; height: 124mm;
  display: flex; flex-direction: column; justify-content: center;
}}
.text::before {{ content: ""; display: block; width: 16mm; border-top: 2pt solid #0c8f93; margin-bottom: 7mm; }}
.text p {{
  margin: 0 0 3.4mm; text-align: justify;
  font-family: "Cairo", sans-serif; font-weight: 400; font-size: 11.6pt; line-height: 2.0; color: #07383e;
}}
.text p:last-child {{ margin: 0; font-weight: 700; color: #0c6a70; }}
.sign {{ position: absolute; left: 0; right: 0; top: 214mm; text-align: center; color: #07383e; font-family: "Cairo", sans-serif; }}
.sign .ba {{ font-weight: 700; font-size: 17pt; color: #b87a35; font-feature-settings: "rlig" 0, "liga" 0, "calt" 0; }}
</style></head><body>
<div class="page">{front}
  <div class="title"><span class="t1">{t1}</span><span class="t2">{t2}</span></div>
  <div class="author"><small>تأليف</small><b>{author}</b></div>
</div>
<div class="page">{back}<div class="text">{paras}</div>
  <div class="sign"><span class="ba">{author}</span></div>
</div>
</body></html>""".format(front=duality_front("a"), back=emblem_back("b"), paras=paras, t1=TITLE_HTML[0], t2=TITLE_HTML[1], author=AUTHOR)
    open(os.path.join(HERE, "build", "cover.html"), "w", encoding="utf8").write(html)


if __name__ == "__main__":
    main()
