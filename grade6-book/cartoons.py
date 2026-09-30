# -*- coding: utf-8 -*-
"""Colourful cartoon scenes for the «تمهيد» of every lesson (hand-built SVG, fixed cheerful palette)."""
import re

SKIN = ["#F4CBA3", "#E0A878", "#B7784E"]
HAIR = ["#3B2A20", "#1E1E1E", "#7A4A22"]


def _t(x, y, s, size=13, fill="#1d2433", weight=700, anchor="middle"):
    d = ' direction="rtl"' if re.search("[؀-ۿ]", s) else ""
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"'
            f' font-family="Readex Pro, sans-serif"{d}>{s}</text>')


def kid(x, y, shirt="#E4572E", skin=0, hair=0, girl=False, arm="wave", s=1.0, pants="#2E4A7A"):
    """A cheerful child standing with feet at (x, y). Height ≈ 110·s."""
    sk, hr = SKIN[skin], HAIR[hair]
    g = [f'<g transform="translate({x} {y}) scale({s})">']
    g.append(f'<rect x="-13" y="-40" width="10" height="38" rx="4" fill="{pants}"/><rect x="3" y="-40" width="10" height="38" rx="4" fill="{pants}"/>')
    g.append('<ellipse cx="-8" cy="-2" rx="9" ry="4" fill="#333"/><ellipse cx="8" cy="-2" rx="9" ry="4" fill="#333"/>')
    if girl:
        g.append(f'<path d="M-22 -36 L22 -36 L16 -76 L-16 -76 Z" fill="{shirt}"/>')
    else:
        g.append(f'<rect x="-18" y="-78" width="36" height="42" rx="10" fill="{shirt}"/>')
    # arms
    arms = {"wave": (f'<path d="M-16 -70 Q-30 -60 -28 -44" stroke="{shirt}" stroke-width="9" fill="none" stroke-linecap="round"/>'
                     f'<path d="M16 -70 Q32 -84 30 -100" stroke="{shirt}" stroke-width="9" fill="none" stroke-linecap="round"/>'
                     f'<circle cx="-28" cy="-42" r="5" fill="{sk}"/><circle cx="30" cy="-103" r="5.5" fill="{sk}"/>'),
            "point": (f'<path d="M-16 -70 Q-30 -60 -28 -44" stroke="{shirt}" stroke-width="9" fill="none" stroke-linecap="round"/>'
                      f'<path d="M16 -70 L40 -74" stroke="{shirt}" stroke-width="9" fill="none" stroke-linecap="round"/>'
                      f'<circle cx="-28" cy="-42" r="5" fill="{sk}"/><circle cx="45" cy="-75" r="5.5" fill="{sk}"/>'),
            "hold": (f'<path d="M-16 -70 Q-24 -54 -8 -50" stroke="{shirt}" stroke-width="9" fill="none" stroke-linecap="round"/>'
                     f'<path d="M16 -70 Q24 -54 8 -50" stroke="{shirt}" stroke-width="9" fill="none" stroke-linecap="round"/>'
                     f'<circle cx="-5" cy="-50" r="5" fill="{sk}"/><circle cx="5" cy="-50" r="5" fill="{sk}"/>'),
            "think": (f'<path d="M-16 -70 Q-30 -60 -28 -44" stroke="{shirt}" stroke-width="9" fill="none" stroke-linecap="round"/>'
                      f'<path d="M16 -70 Q30 -66 16 -88" stroke="{shirt}" stroke-width="9" fill="none" stroke-linecap="round"/>'
                      f'<circle cx="-28" cy="-42" r="5" fill="{sk}"/><circle cx="13" cy="-92" r="5.5" fill="{sk}"/>')}
    g.append(arms[arm])
    # head
    g.append(f'<rect x="-5" y="-86" width="10" height="10" fill="{sk}"/><circle cx="0" cy="-100" r="19" fill="{sk}"/>')
    if girl:
        g.append(f'<path d="M-21 -98 Q-22 -124 0 -123 Q22 -124 21 -98 Q20 -110 8 -113 Q-6 -104 -21 -98 Z" fill="{hr}"/>'
                 f'<path d="M-20 -100 Q-28 -80 -22 -66 M20 -100 Q28 -80 22 -66" stroke="{hr}" stroke-width="7" fill="none" stroke-linecap="round"/>'
                 f'<circle cx="16" cy="-116" r="5" fill="#FF6FA8"/>')
    else:
        g.append(f'<path d="M-20 -102 Q-18 -124 2 -122 Q20 -121 20 -104 Q12 -114 0 -112 Q-10 -110 -20 -102 Z" fill="{hr}"/>')
    g.append('<circle cx="-7" cy="-100" r="2.6" fill="#222"/><circle cx="7" cy="-100" r="2.6" fill="#222"/>'
             '<circle cx="-6" cy="-101" r=".9" fill="#fff"/><circle cx="8" cy="-101" r=".9" fill="#fff"/>'
             '<path d="M-7 -92 Q0 -86 7 -92" stroke="#7A2E1E" stroke-width="2.2" fill="none" stroke-linecap="round"/>'
             '<circle cx="-12" cy="-93" r="3" fill="#FF8A8A" opacity=".45"/><circle cx="12" cy="-93" r="3" fill="#FF8A8A" opacity=".45"/>')
    g.append("</g>")
    return "".join(g)


def bubble(x, y, w, h, text, size=14, tail="left"):
    tx = x + (18 if tail == "left" else w - 18)
    return (f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#fff" stroke="#1d2433" stroke-width="1.8"/>'
            f'<path d="M{tx - 7} {y + h - 1} L{tx - 12} {y + h + 12} L{tx + 5} {y + h - 1}" fill="#fff" stroke="#1d2433" stroke-width="1.8" stroke-linejoin="round"/>'
            f'<rect x="{tx - 8}" y="{y + h - 3}" width="14" height="4" fill="#fff"/>'
            + _t(x + w / 2, y + h / 2 + size * .36, text, size) + "</g>")


def sun(x, y, r=16):
    rays = "".join(f'<path d="M{x} {y - r - 4} v-8" transform="rotate({a} {x} {y})" stroke="#F7B32B" stroke-width="3" stroke-linecap="round"/>' for a in range(0, 360, 45))
    return rays + f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFD23F"/>'


def cloud(x, y, s=1):
    return f'<g transform="translate({x} {y}) scale({s})" fill="#fff"><circle cx="0" cy="0" r="12"/><circle cx="14" cy="-6" r="15"/><circle cx="30" cy="0" r="12"/><rect x="0" y="0" width="30" height="12"/></g>'


def ground(color="#9BD37A"):
    return f'<path d="M0 158 Q80 150 160 156 T320 154 V180 H0 Z" fill="{color}"/>'


def board(x, y, w, h, lines, bg="#2F5D50", fg="#fff", size=15):
    out = [f'<rect x="{x - 4}" y="{y - 4}" width="{w + 8}" height="{h + 8}" rx="8" fill="#A0522D"/><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{bg}"/>']
    step = h / (len(lines) + 1)
    for i, s in enumerate(lines):
        out.append(_t(x + w / 2, y + step * (i + 1) + size * .35, s, size, fg))
    return "".join(out)


def pencil(x, y, color, ang=0):
    return (f'<g transform="translate({x} {y}) rotate({ang})"><rect x="-3" y="-26" width="6" height="22" fill="{color}"/>'
            f'<path d="M-3 -4 L3 -4 L0 3 Z" fill="#F4CBA3"/><path d="M-1 1 L1 1 L0 3 Z" fill="#333"/><rect x="-3" y="-29" width="6" height="4" fill="#FF8FB1"/></g>')


def box(x, y, w, h, color, label="", size=12):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{color}" stroke="#1d2433" stroke-width="1.4"/>'
            + (_t(x + w / 2, y + h / 2 + size * .35, label, size, "#fff") if label else ""))


def thermometer(x, y, level, label):
    return (f'<rect x="{x - 9}" y="{y}" width="18" height="96" rx="9" fill="#fff" stroke="#1d2433" stroke-width="1.6"/>'
            f'<circle cx="{x}" cy="{y + 104}" r="13" fill="#E4572E" stroke="#1d2433" stroke-width="1.6"/>'
            f'<rect x="{x - 4}" y="{y + 96 - level}" width="8" height="{level + 6}" fill="#E4572E"/>'
            + "".join(f'<path d="M{x + 9} {y + 10 + i * 14} h6" stroke="#1d2433" stroke-width="1.2"/>' for i in range(6))
            + _t(x + 34, y + 100 - level, label, 14, "#2B5FB3"))


def clock(x, y, r, h_ang, label):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="#1d2433" stroke-width="2.4"/>'
            f'<circle cx="{x - r * .7}" cy="{y - r * .85}" r="{r * .28}" fill="#FFD23F" stroke="#1d2433" stroke-width="1.4"/>'
            f'<circle cx="{x + r * .7}" cy="{y - r * .85}" r="{r * .28}" fill="#FFD23F" stroke="#1d2433" stroke-width="1.4"/>'
            + "".join(f'<path d="M{x} {y - r + 3} v5" transform="rotate({a} {x} {y})" stroke="#1d2433" stroke-width="1.6"/>' for a in range(0, 360, 30))
            + f'<path d="M{x} {y} v{-r * .55}" transform="rotate({h_ang} {x} {y})" stroke="#1d2433" stroke-width="3" stroke-linecap="round"/>'
            f'<path d="M{x} {y} v{-r * .8}" stroke="#E4572E" stroke-width="2" stroke-linecap="round"/>'
            + _t(x, y + r + 16, label, 12))


def pizza(x, y, r, n, k):
    import math
    out = [f'<circle cx="{x}" cy="{y}" r="{r + 4}" fill="#E9B44C"/>']
    for j in range(n):
        a1, a2 = -90 + j * 360 / n, -90 + (j + 1) * 360 / n
        p1 = (x + r * math.cos(math.radians(a1)), y + r * math.sin(math.radians(a1)))
        p2 = (x + r * math.cos(math.radians(a2)), y + r * math.sin(math.radians(a2)))
        fill = "#F6E7C8" if j < k else "#FFB347"
        out.append(f'<path d="M{x} {y} L{p1[0]:.1f} {p1[1]:.1f} A{r} {r} 0 0 1 {p2[0]:.1f} {p2[1]:.1f} Z" fill="{fill}" stroke="#C9962A" stroke-width="1.5"/>')
        if j >= k:
            cx = x + r * .6 * math.cos(math.radians((a1 + a2) / 2)); cy = y + r * .6 * math.sin(math.radians((a1 + a2) / 2))
            out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3.2" fill="#D1342F"/>')
    return "".join(out)


def tree(x, y, s=1):
    return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-6" y="-50" width="12" height="50" fill="#8B5A2B"/>'
            f'<circle cx="0" cy="-66" r="26" fill="#3FA34D"/><circle cx="-18" cy="-54" r="16" fill="#4DB85A"/><circle cx="18" cy="-54" r="16" fill="#4DB85A"/>'
            f'<circle cx="-8" cy="-72" r="3" fill="#E4572E"/><circle cx="10" cy="-60" r="3" fill="#E4572E"/></g>')


def sky(night=False):
    return f'<rect x="0" y="0" width="320" height="180" rx="14" fill="{"#CDEBFF" if not night else "#DCE7F5"}"/>'


def svg(body):
    return f'<svg class="cartoon" viewBox="0 0 320 180" role="img" aria-hidden="true" direction="ltr">{body}</svg>'


# ---- one scene per lesson ------------------------------------------------------------
def scene(lid):
    S = {
        "naturals": lambda: sky() + cloud(40, 30) + sun(290, 30) + ground() +
            board(100, 36, 150, 70, ["سكّان لبنان", "5 800 000"], "#FFFFFF", "#1d2433", 16) + kid(60, 162, "#2B9ED8", arm="point"),
        "order": lambda: sky() + ground("#F2D7A7") + "".join(box(120 + i * 38, 118, 32, 38, c, "12") for i, c in enumerate(["#E4572E", "#2B9ED8", "#3FA34D", "#F7B32B"]))
            + "".join(pencil(284 + i * 6, 156, c, 8 * i - 20) for i, c in enumerate(["#E4572E", "#2B9ED8", "#3FA34D", "#9B5DE5", "#F7B32B", "#FF6FA8", "#00B8A9"]))
            + kid(60, 162, "#9B5DE5", arm="think") + bubble(96, 18, 150, 40, "4 × 12 + 7 = ?"),
        "primes": lambda: sky() + ground("#F2D7A7") + "".join(f'<path d="M{150 + i * 32} 128 h24 l-3 30 h-18 Z" fill="{c}" stroke="#1d2433" stroke-width="1.3"/>' for i, c in enumerate(["#FFD23F", "#9BD37A", "#8EC5FF", "#FFB3C7", "#D6B4FF"]))
            + "".join(pencil(160 + i * 32, 130, "#E4572E") + pencil(168 + i * 32, 130, "#2B9ED8") for i in range(3))
            + kid(70, 162, "#FF6FA8", girl=True, skin=1, arm="hold") + bubble(110, 20, 130, 40, "12 ÷ 5 = ?", 16),
        "powers": lambda: sky() + ground() + "".join(box(170 + (i % 3) * 36, 118 - (i // 3) * 30, 32, 28, ["#E4572E", "#2B9ED8", "#3FA34D"][i % 3], "10") for i in range(9))
            + kid(70, 162, "#3FA34D", skin=2, arm="wave") + bubble(96, 16, 120, 40, "10 × 10 × 10", 14),
        "lcm-gcd": lambda: sky() + ground("#F2D7A7") + clock(170, 90, 30, 120, "كل 4 ساعات") + clock(260, 90, 30, 180, "كل 6 ساعات")
            + kid(60, 162, "#F7B32B", arm="think") + _t(215, 36, "متى ترنّان معًا؟", 15, "#9B5DE5"),
        "irreducible": lambda: sky() + ground("#F2D7A7") + pizza(150, 96, 36, 8, 2) + pizza(250, 96, 36, 4, 1)
            + _t(150, 152, "6/8", 16, "#E4572E") + _t(250, 152, "3/4", 16, "#E4572E") + kid(50, 170, "#2B9ED8", arm="point", s=.9),
        "dec-fractions": lambda: sky() + ground("#F2D7A7") + f'<path d="M150 150 h40 l-6 -44 h-28 Z" fill="#8EC5FF" stroke="#1d2433" stroke-width="1.5"/><rect x="156" y="120" width="28" height="30" fill="#FFD23F"/>'
            + f'<path d="M220 150 h56 l-4 -60 q-24 -10 -48 0 Z" fill="#F6E7C8" stroke="#1d2433" stroke-width="1.5"/>' + _t(248, 124, "طحين", 12)
            + _t(170, 94, "1.5", 15, "#E4572E") + _t(248, 80, "1.75", 15, "#E4572E")
            + kid(70, 162, "#fff", arm="wave", pants="#555") + '<path d="M52 44 h36 v-10 q-18 -18 -36 0 Z" fill="#fff" stroke="#1d2433" stroke-width="1.4"/>',
        "dec-expand": lambda: sky() + ground() + f'<path d="M150 150 q30 -60 90 -60 q-10 20 -80 66 Z" fill="#FFE135" stroke="#C9A100" stroke-width="2"/>'
            + board(200, 110, 90, 36, ["1.67 $"], "#fff", "#E4572E", 16) + kid(60, 162, "#E4572E", arm="point", skin=1) + bubble(84, 18, 120, 36, "1.67 ≈ ?", 15),
        "frac-mul": lambda: sky() + ground("#F2D7A7") + '<rect x="150" y="136" width="130" height="10" rx="4" fill="#A0522D"/>'
            + '<path d="M170 136 v-30 h90 v30 Z" fill="#F6C1D1" stroke="#1d2433" stroke-width="1.5"/><path d="M170 106 h90" stroke="#fff" stroke-width="6"/>'
            + '<path d="M215 106 v30" stroke="#1d2433" stroke-width="1.5" stroke-dasharray="4 3"/>' + kid(70, 162, "#00B8A9", arm="hold") + bubble(96, 16, 140, 40, "3/4 × 1/2 = ?", 15),
        "rationals": lambda: '<rect x="0" y="0" width="320" height="180" rx="14" fill="#E4F1FF"/>'
            + '<path d="M150 158 L220 50 L290 158 Z" fill="#8FA7C8"/><path d="M200 82 L220 50 L240 82 Q220 90 200 82 Z" fill="#fff"/>'
            + thermometer(110, 30, 20, "−5°") + '<rect x="0" y="158" width="320" height="22" fill="#F0F6FF"/>'
            + kid(50, 170, "#2B9ED8", arm="wave", s=.9) + '<path d="M36 64 h28 v-10 q-14 -10 -28 0 Z" fill="#E4572E"/>',
        "compare": lambda: sky() + ground("#E8F0F8") + board(130, 36, 70, 44, ["باريس", "−6°"], "#2B5FB3", "#fff", 13)
            + board(230, 36, 70, 44, ["لندن", "−9°"], "#2B5FB3", "#fff", 13) + '<path d="M165 84 v70 M265 84 v70" stroke="#8B5A2B" stroke-width="6"/>'
            + kid(60, 162, "#E4572E", arm="think", skin=1) + '<path d="M44 70 h32 v10 h-32 Z" fill="#3FA34D"/>',
        "add-sub": lambda: sky() + ground() + thermometer(170, 30, 70, "+3°") + '<path d="M215 120 Q260 100 250 60" stroke="#3FA34D" stroke-width="4" fill="none" marker-end=""/>'
            + '<path d="M244 64 l6 -8 l4 10" stroke="#3FA34D" stroke-width="4" fill="none"/>' + _t(270, 120, "−5°", 14, "#2B5FB3") + _t(275, 60, "+8", 16, "#3FA34D")
            + kid(70, 162, "#F7B32B", arm="point", girl=True),
        "lines-circles": lambda: sky() + ground() + '<ellipse cx="200" cy="146" rx="90" ry="22" fill="none" stroke="#E4572E" stroke-width="2.4" stroke-dasharray="7 5"/>'
            + '<path d="M200 146 v-18" stroke="#8B5A2B" stroke-width="5"/><path d="M200 132 Q235 150 262 124" stroke="#1d2433" stroke-width="1.6" fill="none"/>'
            + '<g transform="translate(270 128)"><ellipse cx="0" cy="0" rx="18" ry="11" fill="#fff" stroke="#1d2433" stroke-width="1.4"/><circle cx="16" cy="-8" r="7" fill="#fff" stroke="#1d2433" stroke-width="1.4"/>'
            '<path d="M-10 8 v10 M8 8 v10" stroke="#1d2433" stroke-width="2.4"/><path d="M14 -14 l-4 -6 M20 -14 l2 -7" stroke="#8B5A2B" stroke-width="2"/></g>'
            + tree(120, 150, .7) + kid(50, 170, "#9B5DE5", arm="point", s=.85, skin=2) + _t(236, 118, "3 m", 13, "#E4572E"),
        "angles": lambda: sky() + ground() + '<path d="M190 158 V60" stroke="#8B5A2B" stroke-width="10" stroke-linecap="round"/>'
            + '<path d="M190 110 L140 70 M190 96 L250 60" stroke="#8B5A2B" stroke-width="6" stroke-linecap="round"/>'
            + '<circle cx="140" cy="66" r="14" fill="#4DB85A"/><circle cx="252" cy="56" r="16" fill="#4DB85A"/><circle cx="190" cy="54" r="18" fill="#3FA34D"/>'
            + '<path d="M168 92 A26 26 0 0 1 190 84" stroke="#E4572E" stroke-width="3" fill="none"/>'
            + kid(70, 162, "#2B9ED8", arm="hold", girl=True, skin=1) + '<rect x="55" y="100" width="30" height="20" rx="4" fill="#333"/><circle cx="70" cy="110" r="6" fill="#8EC5FF"/>',
        "triangles": lambda: sky() + ground("#F2D7A7") + '<path d="M140 150 L220 150 L170 80 Z" fill="#FFD23F" stroke="#1d2433" stroke-width="1.8"/>'
            + '<path d="M240 150 h60" stroke="#1d2433" stroke-width="2"/><path d="M270 150 l-22 -8 a24 24 0 0 1 2 -12 Z" fill="#E4572E"/><path d="M270 150 l-20 -20 a28 28 0 0 1 26 -6 Z" fill="#2B9ED8"/><path d="M270 150 l6 -26 a26 26 0 0 1 22 26 Z" fill="#3FA34D"/>'
            + _t(270, 172, "180°", 14, "#9B5DE5") + kid(70, 162, "#FF6FA8", arm="point"),
        "areas": lambda: sky() + ground("#F2D7A7") + "".join(f'<rect x="{150 + c * 24}" y="{64 + r * 22}" width="24" height="22" fill="{["#F6E7C8", "#E9D4AE"][(r + c) % 2]}" stroke="#C9A97A"/>' for r in range(4) for c in range(6))
            + _t(222, 58, "6 m", 13, "#E4572E") + _t(304, 112, "4 m", 13, "#E4572E") + kid(70, 162, "#3FA34D", arm="point", skin=2),
        "ratio": lambda: sky() + ground("#F2D7A7") + '<path d="M170 110 h100 q-6 44 -50 44 q-44 0 -50 -44 Z" fill="#8EC5FF" stroke="#1d2433" stroke-width="1.6"/>'
            + "".join(f'<path d="M{160 + i * 22} 70 h16 l-2 22 h-12 Z" fill="#F6E7C8" stroke="#1d2433" stroke-width="1.2"/>' for i in range(3))
            + "".join(f'<path d="M{236 + i * 22} 70 h16 l-2 22 h-12 Z" fill="#fff" stroke="#1d2433" stroke-width="1.2"/>' for i in range(2))
            + _t(192, 62, "3 طحين", 12) + _t(258, 62, "2 حليب", 12) + kid(70, 162, "#fff", arm="wave", girl=True, pants="#555"),
        "literal": lambda: sky() + ground() + kid(170, 162, "#2B9ED8", arm="point", s=1.05) + kid(250, 162, "#F7B32B", arm="wave", s=.75, skin=1)
            + bubble(40, 20, 120, 40, "3x + 11", 16, "right") + _t(250, 170, "x", 14, "#E4572E"),
        "percent": lambda: sky() + ground("#F2D7A7") + '<rect x="150" y="70" width="110" height="70" rx="8" fill="#fff" stroke="#1d2433" stroke-width="1.6"/><path d="M150 72 L205 108 L260 72" stroke="#1d2433" stroke-width="1.6" fill="none"/>'
            + _t(205, 130, "140 $", 16, "#3FA34D") + '<circle cx="272" cy="64" r="24" fill="#E4572E"/>' + _t(272, 70, "+20%", 13, "#fff") + kid(70, 162, "#9B5DE5", arm="wave", skin=1),
        "proportional": lambda: sky() + ground("#F2D7A7") + '<rect x="140" y="110" width="160" height="46" fill="#A0522D"/><path d="M130 110 h180 l-14 -26 h-152 Z" fill="#E4572E"/>'
            + "".join(f'<circle cx="{160 + i * 18}" cy="{102 - (i % 2) * 8}" r="9" fill="#D1342F"/>' for i in range(7))
            + board(170, 20, 100, 44, ["1 kg", "25 000"], "#fff", "#1d2433", 13) + kid(70, 162, "#00B8A9", arm="point"),
        "stats": lambda: '<rect x="0" y="0" width="320" height="180" rx="14" fill="#FFF3DC"/>'
            + "".join(f'<rect x="{150 + i * 30}" y="{150 - v * 11}" width="22" height="{v * 11}" rx="3" fill="{c}"/>' for i, (v, c) in enumerate(zip([5, 8, 6, 9, 4], ["#E4572E", "#2B9ED8", "#3FA34D", "#F7B32B", "#9B5DE5"])))
            + '<path d="M144 150 h156" stroke="#1d2433" stroke-width="2"/>' + '<rect x="0" y="158" width="320" height="22" fill="#E9D4AE"/>'
            + kid(70, 162, "#2B9ED8", arm="point", girl=True, skin=2) + _t(225, 28, "الكتب المستعارة", 14, "#1d2433"),
    }
    f = S.get(lid)
    return svg(f()) if f else ""
