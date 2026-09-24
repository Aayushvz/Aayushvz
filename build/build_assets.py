"""Generates every SVG in ../assets. Run: python build/build_assets.py"""
import base64
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
FONT = base64.b64encode((Path(__file__).parent / "Bangers-sub.woff2").read_bytes()).decode()

RED = "#E23636"
RED_DK = "#9E1B1B"
BLUE = "#2B59D8"
BLUE_LT = "#5B8DEF"
INK = "#0B0E14"
WEB = "#8B949E"

FONT_CSS = (
    "<style>@font-face{font-family:'Sling';"
    f"src:url(data:font/woff2;base64,{FONT}) format('woff2');}}"
    ".c{font-family:'Sling','Impact','Arial Black',sans-serif;}</style>"
)

TECH = [
    "Figma", "Framer", "Photoshop", "Illustrator", "After Effects", "Premiere Pro",
    "Next.js", "React", "TypeScript", "JavaScript", "GSAP", "Tailwind CSS",
    "Three.js", "Python", "Streamlit", "Gemini API", "Git", "Vercel",
]


def write(name, svg):
    (ASSETS / name).write_text(svg, encoding="utf-8")
    print(f"{name}: {len(svg.encode()) // 1024} KB")


# ---------- small section icons (32x32) ----------

def spider_shape(color, legs_w=1.9):
    legs_left = [
        [(13, 12), (7, 7), (5, 2)],
        [(12.5, 15), (5.5, 12), (1.5, 10)],
        [(12.5, 18.5), (5.5, 19.5), (1.5, 23.5)],
        [(13.5, 21.5), (7.5, 25.5), (5.5, 30.5)],
    ]
    paths = []
    for leg in legs_left:
        for mirror in (False, True):
            pts = [((32 - x) if mirror else x, y) for x, y in leg]
            d = "M" + " L".join(f"{x} {y}" for x, y in pts)
            paths.append(f'<path d="{d}"/>')
    return (
        f'<g stroke="{color}" stroke-width="{legs_w}" fill="none" stroke-linecap="round" '
        f'stroke-linejoin="round">{"".join(paths)}</g>'
        f'<ellipse cx="16" cy="19.5" rx="4.6" ry="6.2" fill="{color}"/>'
        f'<circle cx="16" cy="11" r="3.1" fill="{color}"/>'
    )


def icon_spider(color):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">{spider_shape(color)}</svg>'


def icon_mask():
    # a generic masked head: red dome, web seams, two big white lenses
    seams = "".join(
        f'<path d="M16 17 L{16 + 13 * math.cos(a):.1f} {17 + 15 * math.sin(a):.1f}"/>'
        for a in [i * math.pi / 4 for i in range(8)]
    )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
        '<defs><clipPath id="h"><path d="M16 2 C25 2 29 9 29 16 C29 25 23 31 16 31 C9 31 3 25 3 16 C3 9 7 2 16 2Z"/></clipPath></defs>'
        f'<path d="M16 2 C25 2 29 9 29 16 C29 25 23 31 16 31 C9 31 3 25 3 16 C3 9 7 2 16 2Z" fill="{RED}"/>'
        f'<g clip-path="url(#h)" stroke="{RED_DK}" stroke-width="0.8" fill="none">{seams}'
        '<ellipse cx="16" cy="17" rx="6" ry="6.5"/><ellipse cx="16" cy="17" rx="11" ry="12"/></g>'
        f'<path d="M5.5 13.5 Q9 8.5 14 14.5 Q10.5 19.5 5.5 13.5Z" fill="#fff" stroke="{INK}" stroke-width="1.4" stroke-linejoin="round"/>'
        f'<path d="M26.5 13.5 Q23 8.5 18 14.5 Q21.5 19.5 26.5 13.5Z" fill="#fff" stroke="{INK}" stroke-width="1.4" stroke-linejoin="round"/>'
        "</svg>"
    )


def icon_web(color):
    cx = cy = 16
    spokes = [i * math.pi / 4 + math.pi / 8 for i in range(8)]
    out = [f'<path d="M{cx} {cy} L{cx + 15 * math.cos(a):.2f} {cy + 15 * math.sin(a):.2f}"/>' for a in spokes]
    for r in (4.5, 9, 13.5):
        pts = [(cx + r * math.cos(a), cy + r * math.sin(a)) for a in spokes]
        d = f"M{pts[0][0]:.2f} {pts[0][1]:.2f}"
        for i in range(1, 9):
            p0 = pts[(i - 1) % 8]
            p1 = pts[i % 8]
            mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
            # sag each strand toward the centre
            qx, qy = cx + (mx - cx) * 0.8, cy + (my - cy) * 0.8
            d += f" Q{qx:.2f} {qy:.2f} {p1[0]:.2f} {p1[1]:.2f}"
        out.append(f'<path d="{d}"/>')
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
        f'<g stroke="{color}" stroke-width="1.3" fill="none" stroke-linecap="round">{"".join(out)}</g></svg>'
    )


def icon_hanging(color):
    # a spider hanging off a thread, gently bobbing
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 40">'
        f'<g><line x1="16" y1="0" x2="16" y2="12" stroke="{WEB}" stroke-width="1.2"/>'
        f'<g transform="translate(0 8)">{spider_shape(color)}</g>'
        '<animateTransform attributeName="transform" type="translate" values="0 -2;0 2;0 -2" dur="2.4s" '
        'calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1" repeatCount="indefinite"/></g></svg>'
    )


# ---------- dividers ----------

def corner_web(x, flip):
    s = -1 if flip else 1
    spokes = [0, 22, 45, 68, 90]
    lines = []
    for a in spokes:
        r = math.radians(a)
        lines.append(f'<path d="M{x} 0 L{x + s * 34 * math.cos(r):.1f} {34 * math.sin(r):.1f}"/>')
    for rad in (10, 20, 30):
        pts = [(x + s * rad * math.cos(math.radians(a)), rad * math.sin(math.radians(a))) for a in spokes]
        d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}" + "".join(f" L{px:.1f} {py:.1f}" for px, py in pts[1:])
        lines.append(f'<path d="{d}"/>')
    return "".join(lines)


def web_divider():
    strand = "M40 6 Q700 34 1360 6"
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1400 44">'
        f'<g stroke="{WEB}" stroke-width="1.4" fill="none" opacity=".55">'
        f'{corner_web(0, False)}{corner_web(1400, True)}<path d="{strand}"/></g>'
        # dew drops sitting on the strand
        + "".join(
            f'<circle cx="{x}" cy="{6 + 14 * (1 - ((x - 700) / 660) ** 2):.1f}" r="2.4" fill="{BLUE_LT}" opacity=".7"/>'
            for x in (190, 420, 980, 1210)
        )
        + f'<g><g transform="translate(-16 -8) scale(.62)">{spider_shape(RED, 2.4)}</g>'
        f'<animateMotion dur="14s" repeatCount="indefinite" path="{strand}" rotate="auto" '
        'keyPoints="0;1;1;0;0" keyTimes="0;.45;.5;.95;1" calcMode="linear"/></g>'
        "</svg>"
    )


def suit_divider():
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1400 16">'
        f'<rect x="2" y="2" width="1396" height="5" rx="2.5" fill="{RED}"/>'
        f'<rect x="2" y="9" width="1396" height="5" rx="2.5" fill="{BLUE}"/>'
        "</svg>"
    )


# ---------- tech stack ----------
# Tools are caught in a giant web over a night skyline; the spider crawls
# from tag to tag and each tag lights up while the spider sits on it.

DESIGN = ["Figma", "Framer", "Photoshop", "Illustrator", "After Effects", "Premiere Pro"]


def skyline(y_base, rng_seed=7, h_range=(90, 250)):
    import random
    rnd = random.Random(rng_seed)
    out, windows = [], []
    x = 6
    while x < 1394:
        w = rnd.randint(60, 130)
        h = rnd.randint(*h_range)
        top = y_base - h
        out.append(f'<rect x="{x}" y="{top}" width="{w}" height="{h + 10}"/>')
        if rnd.random() < 0.3:  # rooftop water tank / antenna
            out.append(f'<rect x="{x + w // 2 - 2}" y="{top - 30}" width="4" height="30"/>')
        for wy in range(top + 14, y_base - 10, 22):
            for wx in range(x + 10, x + w - 14, 20):
                if rnd.random() < 0.18:
                    lit = rnd.random() < 0.35
                    anim = ""
                    if lit:
                        d = rnd.uniform(3, 7)
                        anim = (f'<animate attributeName="opacity" values=".9;.15;.9" dur="{d:.1f}s" '
                                f'begin="{rnd.uniform(0, 4):.1f}s" repeatCount="indefinite"/>')
                    windows.append(f'<rect x="{wx}" y="{wy}" width="8" height="10" opacity=".9">{anim}</rect>')
        x += w + rnd.randint(2, 10)
    return "".join(out), "".join(windows)


def tag(x, y, name, design, i, n, total, rot):
    w = len(name) * 17 + 44
    h = 50
    base = RED if design else BLUE
    s, e = i / n, (i + 0.7) / n
    k = f"0;{s:.4f};{s + 0.01:.4f};{e:.4f};{e + 0.01:.4f};1"
    return (
        f'<g transform="translate({x:.1f} {y:.1f}) rotate({rot})"><g>'
        f'<rect x="{-w / 2 + 6:.1f}" y="{-h / 2 + 6}" width="{w}" height="{h}" rx="6" fill="{INK}"/>'
        f'<rect x="{-w / 2:.1f}" y="{-h / 2}" width="{w}" height="{h}" rx="6" fill="{base}" stroke="{INK}" stroke-width="4">'
        f'<animate attributeName="fill" values="{base};{base};#FFE45C;#FFE45C;{base};{base}" keyTimes="{k}" '
        f'dur="{total}s" repeatCount="indefinite"/></rect>'
        f'<text class="c" x="0" y="12" text-anchor="middle" font-size="34" letter-spacing="1" fill="#fff">{name}'
        f'<animate attributeName="fill" values="#fff;#fff;{INK};{INK};#fff;#fff" keyTimes="{k}" '
        f'dur="{total}s" repeatCount="indefinite"/></text>'
        f'<animateTransform attributeName="transform" type="scale" values="1;1;1.15;1.08;1;1" keyTimes="{k}" '
        f'dur="{total}s" repeatCount="indefinite"/></g></g>'
    )


def techstack():
    W, H = 1400, 860
    cx, cy = 700, 520
    SX = 1.75  # web is stretched horizontally
    per_tag = 1.6
    n = len(TECH)
    total = per_tag * n

    defs = (
        f"{FONT_CSS}"
        '<pattern id="td" width="16" height="16" patternUnits="userSpaceOnUse">'
        f'<circle cx="8" cy="8" r="3" fill="{BLUE}"/></pattern>'
        '<linearGradient id="tf" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#fff" stop-opacity=".45"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        '<mask id="tm"><rect width="1400" height="860" fill="url(#tf)"/></mask>'
        '<radialGradient id="glow"><stop offset="0" stop-color="#F3EBD3" stop-opacity=".35"/>'
        '<stop offset="1" stop-color="#F3EBD3" stop-opacity="0"/></radialGradient>'
        f'<clipPath id="tp"><rect x="6" y="6" width="{W - 12}" height="{H - 12}" rx="22"/></clipPath>'
    )

    bldg, windows = skyline(H - 6)
    scene = (
        f'<rect x="6" y="6" width="{W - 12}" height="{H - 12}" rx="22" fill="#0E1526"/>'
        f'<g clip-path="url(#tp)"><rect width="{W}" height="{H}" fill="url(#td)" mask="url(#tm)"/>'
        f'<circle cx="1210" cy="200" r="150" fill="url(#glow)"/>'
        f'<circle cx="1210" cy="200" r="70" fill="#F3EBD3"/>'
        f'<circle cx="1186" cy="182" r="11" fill="#E2D8BC"/><circle cx="1232" cy="222" r="7" fill="#E2D8BC"/>'
        f'<g fill="#16213D">{bldg}</g><g fill="#FFE45C">{windows}</g>'
    )

    # the web: long spokes to the panel edges, sagging rings
    spokes = [math.radians(a) for a in range(0, 360, 30)]
    web = [f'<path d="M{cx} {cy} L{cx + 1200 * math.cos(a):.1f} {cy + 1200 * math.sin(a) / SX:.1f}"/>' for a in spokes]
    for r in (60, 130, 200, 265, 330):
        pts = [(cx + r * SX * math.cos(a), cy + r * math.sin(a)) for a in spokes]
        pts.append(pts[0])
        d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
        for p0, p1 in zip(pts, pts[1:]):
            mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
            d += f" Q{cx + (mx - cx) * 0.88:.1f} {cy + (my - cy) * 0.88:.1f} {p1[0]:.1f} {p1[1]:.1f}"
        web.append(f'<path d="{d}"/>')
    scene += f'<g stroke="#C9D1D9" stroke-width="2" fill="none" opacity=".35">{"".join(web)}</g></g>'
    scene += f'<rect x="6" y="6" width="{W - 12}" height="{H - 12}" rx="22" fill="none" stroke="{RED}" stroke-width="6"/>'

    title = (
        f'<text class="c" x="706" y="128" text-anchor="middle" font-size="120" fill="{BLUE}" stroke="{INK}" '
        f'stroke-width="10" stroke-linejoin="round" paint-order="stroke">MY TECH-STACK</text>'
        f'<text class="c" x="700" y="122" text-anchor="middle" font-size="120" fill="{RED}" stroke="{INK}" '
        f'stroke-width="10" stroke-linejoin="round" paint-order="stroke">MY TECH-STACK</text>'
        f'<g transform="rotate(-3 700 170)"><rect x="520" y="148" width="360" height="42" fill="#FFE45C" stroke="{INK}" stroke-width="4"/>'
        f'<text class="c" x="700" y="178" text-anchor="middle" font-size="28" letter-spacing="2" fill="{INK}">'
        "CAUGHT IN MY WEB</text></g>"
    )

    # design tools form the core ring, code wraps around it
    code = [t for t in TECH if t not in DESIGN]
    placed = [(a, 150, name) for a, name in zip(range(-60, 300, 60), DESIGN)]
    placed += [(a, 310, name) for a, name in zip(range(-75, 285, 30), code)]
    placed.sort(key=lambda t: t[0] % 360)
    points = []
    tags = []
    for i, (a, r, name) in enumerate(placed):
        ra = math.radians(a)
        x, y = cx + r * SX * math.cos(ra), cy + r * math.sin(ra) * 0.95
        points.append((x, y - 50))  # spider perches on the top edge
        rot = ((i * 37) % 9) - 4
        tags.append(tag(x, y, name, name in DESIGN, i, n, total, rot))

    # spider route: tag to tag, pausing on each
    pts = points + [points[0]]
    seg = [math.dist(p0, p1) for p0, p1 in zip(pts, pts[1:])]
    L = sum(seg)
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}" + "".join(f" L{x:.1f} {y:.1f}" for x, y in pts[1:])
    kp, kt, acc = [], [], 0.0
    for i in range(n):
        kp += [acc / L, acc / L]
        kt += [i / n, (i + 0.7) / n]
        acc += seg[i]
    kp.append(1)
    kt.append(1)
    kp_s = ";".join(f"{v:.4f}" for v in kp)
    kt_s = ";".join(f"{v:.4f}" for v in kt)
    route = f'<path d="{d}" stroke="#fff" stroke-width="2.5" stroke-dasharray="3 9" stroke-linecap="round" fill="none" opacity=".5"/>'
    spider = (
        f'<g><g transform="rotate(90) translate(-35 -40) scale(2.2)">{spider_shape(INK, 3.4)}</g>'
        f'<g transform="rotate(90) translate(-35 -40) scale(2.2)">{spider_shape(RED, 2)}</g>'
        f'<animateMotion dur="{total}s" repeatCount="indefinite" path="{d}" rotate="auto" '
        f'keyPoints="{kp_s}" keyTimes="{kt_s}" calcMode="linear"/></g>'
    )

    legend = (
        f'<g transform="translate(40 800)"><rect width="26" height="26" rx="4" fill="{RED}" stroke="{INK}" stroke-width="3"/>'
        f'<text class="c" x="36" y="22" font-size="28" fill="#fff" stroke="{INK}" stroke-width="4" paint-order="stroke">DESIGN</text>'
        f'<rect x="140" width="26" height="26" rx="4" fill="{BLUE}" stroke="{INK}" stroke-width="3"/>'
        f'<text class="c" x="176" y="22" font-size="28" fill="#fff" stroke="{INK}" stroke-width="4" paint-order="stroke">CODE</text></g>'
    )

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}"><defs>{defs}</defs>'
        f'{scene}{title}{route}{"".join(tags)}{spider}{legend}</svg>'
    )


# ---------- footer ----------

def footer_swing():
    W, H = 1400, 230
    ax = 700
    spline = 'calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"'
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}"><defs>{FONT_CSS}</defs>'
        # faint arc showing the swing path
        f'<path d="M{ax - 150} 100 Q{ax} 240 {ax + 150} 100" stroke="{WEB}" stroke-width="2" '
        'stroke-dasharray="2 12" stroke-linecap="round" fill="none" opacity=".6"/>'
        f'<g><line x1="{ax}" y1="0" x2="{ax}" y2="150" stroke="{WEB}" stroke-width="2.5"/>'
        f'<g transform="translate({ax - 40} 140) scale(2.5)">{spider_shape(RED, 2)}</g>'
        f'<animateTransform attributeName="transform" type="rotate" values="-42 {ax} 0;42 {ax} 0;-42 {ax} 0" '
        f'dur="3.2s" {spline} repeatCount="indefinite"/></g>'
        f'<text class="c" x="{ax - 330}" y="130" text-anchor="middle" font-size="40" fill="{BLUE_LT}" '
        f'stroke="{INK}" stroke-width="5" paint-order="stroke" transform="rotate(-6 {ax - 330} 130)">THWIP!'
        '<animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;.38;.5;.62;1" dur="3.2s" repeatCount="indefinite"/></text>'
        f'<text class="c" x="{ax + 330}" y="130" text-anchor="middle" font-size="40" fill="{RED}" '
        f'stroke="{INK}" stroke-width="5" paint-order="stroke" transform="rotate(6 {ax + 330} 130)">THWIP!'
        '<animate attributeName="opacity" values="1;0;0;1" keyTimes="0;.12;.88;1" dur="3.2s" repeatCount="indefinite"/></text>'
        "</svg>"
    )


# ---------- header banner ----------

def big_web(cx, cy, r, a0, a1, rings=5, spokes=7):
    angles = [math.radians(a0 + (a1 - a0) * i / (spokes - 1)) for i in range(spokes)]
    out = [f'<path d="M{cx} {cy} L{cx + r * math.cos(a):.1f} {cy + r * math.sin(a):.1f}"/>' for a in angles]
    for k in range(1, rings + 1):
        rr = r * k / rings
        pts = [(cx + rr * math.cos(a), cy + rr * math.sin(a)) for a in angles]
        d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
        for p0, p1 in zip(pts, pts[1:]):
            mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
            d += f" Q{cx + (mx - cx) * 0.86:.1f} {cy + (my - cy) * 0.86:.1f} {p1[0]:.1f} {p1[1]:.1f}"
        out.append(f'<path d="{d}"/>')
    return "".join(out)


def header():
    W, H = 1400, 640
    spline = 'calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"'
    once = 'fill="freeze" calcMode="spline" keySplines=".2 .9 .3 1"'

    defs = (
        f"{FONT_CSS}"
        '<pattern id="hd" width="16" height="16" patternUnits="userSpaceOnUse">'
        f'<circle cx="8" cy="8" r="3" fill="{BLUE}"/></pattern>'
        '<linearGradient id="hf" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#fff" stop-opacity=".5"/><stop offset=".55" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        '<mask id="hm"><rect width="1400" height="640" fill="url(#hf)"/></mask>'
        '<clipPath id="panel"><rect x="6" y="6" width="1388" height="628" rx="22"/></clipPath>'
    )

    bg = (
        f'<rect x="6" y="6" width="1388" height="628" rx="22" fill="#0E1526"/>'
        f'<g clip-path="url(#panel)"><rect width="1400" height="640" fill="url(#hd)" mask="url(#hm)"/>'
        f'<g stroke="{WEB}" stroke-width="1.6" fill="none" opacity=".45">{big_web(6, 6, 300, 0, 90)}'
        f'{big_web(1394, 634, 230, 180, 270, 4, 6)}</g></g>'
        f'<rect x="6" y="6" width="1388" height="628" rx="22" fill="none" stroke="{RED}" stroke-width="6"/>'
    )

    # spider dropping in on a thread, then bobbing
    sx = 1190
    spider = (
        f'<g><line x1="{sx}" y1="6" x2="{sx}" y2="236" stroke="#C9D1D9" stroke-width="2.5"/>'
        f'<g transform="translate({sx - 56} 216) scale(3.5)">{spider_shape(RED, 2)}</g>'
        f'<animateTransform attributeName="transform" type="translate" values="0 -300;0 0" dur="1.1s" {once}/>'
        f'<animateTransform attributeName="transform" type="translate" values="0 0;0 16;0 0" begin="1.1s" '
        f'dur="2.6s" {spline} repeatCount="indefinite" additive="sum"/></g>'
    )

    def title_layer(dx, dy, fill, stroke=f'stroke="{INK}" stroke-width="12" paint-order="stroke"'):
        return (
            f'<text class="c" x="{600 + dx}" y="{250 + dy}" text-anchor="middle" font-size="210" fill="{fill}" '
            f'stroke-linejoin="round" {stroke}>AAYUSH RAJ</text>'
        )

    title = (
        '<g opacity="0">'
        + title_layer(10, 10, BLUE)
        + title_layer(0, 0, RED)
        + '<animate attributeName="opacity" values="0;1" dur=".35s" begin=".2s" fill="freeze"/>'
        '<animateTransform attributeName="transform" type="translate" values="-60 0;0 0" dur=".6s" begin=".2s" '
        f'{once}/></g>'
        f'<text class="c" x="600" y="318" text-anchor="middle" font-size="46" letter-spacing="3" fill="#fff" '
        f'stroke="{INK}" stroke-width="6" paint-order="stroke" opacity="0">YOUR FRIENDLY NEIGHBOURHOOD PIXEL-SLINGER'
        '<animate attributeName="opacity" values="0;1" dur=".4s" begin=".8s" fill="freeze"/></text>'
    )

    # comic narration captions
    caps = [
        ("WHO?", "Designer who codes", 90, -2),
        ("BASE", "VIT Vellore, final year", 520, 1.5),
        ("SPIDER-SENSE", "Something is 1px off.", 950, -1.5),
    ]
    boxes = []
    for i, (label, body, x, rot) in enumerate(caps):
        w, h, y = 380, 150, 400
        begin = 1.2 + i * 0.3
        boxes.append(
            f'<g transform="rotate({rot} {x + w / 2} {y + h / 2})"><g opacity="0">'
            f'<rect x="{x + 8}" y="{y + 8}" width="{w}" height="{h}" fill="{BLUE}" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#FFE45C" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="46" fill="{RED}" stroke="{INK}" stroke-width="5"/>'
            f'<text class="c" x="{x + 18}" y="{y + 36}" font-size="34" letter-spacing="2" fill="#fff">{label}</text>'
            f'<text x="{x + 18}" y="{y + 108}" font-family="\'Segoe UI\',Helvetica,Arial,sans-serif" font-weight="700" '
            f'font-size="27" fill="{INK}">{body}</text>'
            f'<animate attributeName="opacity" values="0;1" dur=".2s" begin="{begin}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" values="0 40;0 0" dur=".45s" '
            f'begin="{begin}s" {once}/></g></g>'
        )

    # spider-sense: jagged ticks flickering around the last caption
    ticks = []
    ccx, ccy = 950 + 190, 475
    for k, a in enumerate(range(-160, 200, 40)):
        if -20 < a < 20 or 160 < abs(a) < 200:
            continue
        r = math.radians(a)
        r0x, r0y = 220, 110
        x0, y0 = ccx + r0x * math.cos(r), ccy + r0y * math.sin(r)
        x1, y1 = ccx + (r0x + 34) * math.cos(r), ccy + (r0y + 34) * math.sin(r)
        mx, my = (x0 + x1) / 2 + 7 * math.sin(r), (y0 + y1) / 2 - 7 * math.cos(r)
        ticks.append(
            f'<path opacity="0" d="M{x0:.1f} {y0:.1f} L{mx:.1f} {my:.1f} L{x1:.1f} {y1:.1f}">'
            f'<animate attributeName="opacity" values="0;1;0;0" keyTimes="0;.15;.4;1" dur="1.6s" '
            f'begin="{2.2 + k * 0.08:.2f}s" repeatCount="indefinite"/></path>'
        )
    sense = f'<g stroke="{RED}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" fill="none" opacity=".9">{"".join(ticks)}</g>'

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}"><defs>{defs}</defs>'
        f'{bg}{spider}{title}{sense}{"".join(boxes)}</svg>'
    )


# ---------- project cards: each one a comic book cover ----------

PROJECTS = [
    ("cat", "CAT OPERATOR", "ASSISTANT", "HACKATHON", "3D!",
     "Smart co-pilot for Cat excavator operators: 3D machine view, shift replay, safety and training.",
     ["JavaScript", "Python"]),
    ("invoice", "INVOICE", "GENERATOR", "WEB TOOL", "PDF!",
     "Fill a form, pick a template, get a real PDF. No account, and no client data leaves the browser.",
     ["Next.js", "Tailwind"]),
    ("contract", "CONTRACT", "GENERATOR", "WEB TOOL", "FREE!",
     "Freelance contracts in minutes on aayushvisuals.com. Fill in a form, print a ready contract.",
     ["Next.js", "TypeScript"]),
    ("visuals", "AAYUSH", "VISUALS", "PORTFOLIO", "SCROLL!",
     "Cinematic single-scroll portfolio where every section is a pinned, scroll-driven moment.",
     ["Next.js", "Framer Motion"]),
    ("coursebot", "COURSE FINDER", "BOT", "AI", "AI!",
     "Gemini-powered chatbot that finds courses by interest, domain, skill level and duration.",
     ["Python", "Streamlit", "Gemini"]),
    ("fuzion", "FUZION", "IDENTITY", "BRANDING", "BRAND!",
     "Full visual identity system on Behance, and my most appreciated piece there.",
     ["Branding", "Identity"]),
]


def burst(cx, cy, r_out, r_in, n=14):
    pts = []
    for i in range(n * 2):
        a = math.pi * i / n - math.pi / 2
        # uneven spikes read as hand-drawn comic
        r = r_out * (1 if i % 4 == 0 else 0.9) if i % 2 == 0 else r_in
        pts.append(f"{cx + r * math.cos(a) * 1.55:.1f},{cy + r * math.sin(a):.1f}")
    return " ".join(pts)


def wrap(text, width):
    lines, cur = [], ""
    for word in text.split():
        if len(cur) + len(word) + 1 > width and cur:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    return lines + [cur]


def project_card(idx, key, line1, line2, genre, shout, desc, tags):
    W, H = 700, 470
    sans = "font-family=\"'Segoe UI',Helvetica,Arial,sans-serif\""
    once = 'fill="freeze" calcMode="spline" keySplines=".2 .9 .3 1"'
    delay = 0.15 * idx

    def title(text, y, size):
        return (
            f'<text class="c" x="{40 + 7}" y="{y + 7}" font-size="{size}" fill="{BLUE}" stroke="{INK}" '
            f'stroke-width="9" stroke-linejoin="round" paint-order="stroke">{text}</text>'
            f'<text class="c" x="40" y="{y}" font-size="{size}" fill="{RED}" stroke="{INK}" '
            f'stroke-width="9" stroke-linejoin="round" paint-order="stroke">{text}</text>'
        )

    size = 78 if max(len(line1), len(line2)) <= 11 else 66
    body = "".join(
        f'<text x="58" y="{300 + i * 32}" {sans} font-weight="700" font-size="23" fill="{INK}">{ln}</text>'
        for i, ln in enumerate(wrap(desc, 46))
    )
    tag_x = 40
    chips = []
    for t in tags:
        w = len(t) * 12 + 30
        chips.append(
            f'<rect x="{tag_x}" y="{H - 62}" width="{w}" height="34" rx="17" fill="none" stroke="#C9D1D9" stroke-width="2"/>'
            f'<text x="{tag_x + w / 2}" y="{H - 39}" text-anchor="middle" {sans} font-weight="600" font-size="17" fill="#C9D1D9">{t}</text>'
        )
        tag_x += w + 10

    bx, by = 585, 150
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}"><defs>{FONT_CSS}'
        '<pattern id="pd" width="14" height="14" patternUnits="userSpaceOnUse">'
        f'<circle cx="7" cy="7" r="2.6" fill="{BLUE}"/></pattern>'
        '<linearGradient id="pf" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".5"/>'
        '<stop offset=".6" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        f'<mask id="pm"><rect width="{W}" height="{H}" fill="url(#pf)"/></mask>'
        f'<clipPath id="pc"><rect x="5" y="5" width="{W - 10}" height="{H - 10}" rx="18"/></clipPath></defs>'
        f'<rect x="5" y="5" width="{W - 10}" height="{H - 10}" rx="18" fill="#0E1526"/>'
        f'<g clip-path="url(#pc)"><rect width="{W}" height="{H}" fill="url(#pd)" mask="url(#pm)"/>'
        f'<g stroke="{WEB}" stroke-width="1.5" fill="none" opacity=".4">{big_web(W - 5, H - 5, 200, 180, 270, 4, 5)}</g>'
        # masthead strip
        f'<rect x="0" y="0" width="{W}" height="62" fill="{RED}"/>'
        f'<rect x="0" y="62" width="{W}" height="5" fill="{INK}"/>'
        f'<text class="c" x="30" y="45" font-size="34" letter-spacing="2" fill="#fff">ISSUE #{idx + 1:02d}</text>'
        f'<text class="c" x="{W - 30}" y="45" text-anchor="end" font-size="34" letter-spacing="2" fill="#FFE45C" '
        f'stroke="{INK}" stroke-width="4" paint-order="stroke">{genre}</text></g>'
        f'<rect x="5" y="5" width="{W - 10}" height="{H - 10}" rx="18" fill="none" stroke="{RED}" stroke-width="5"/>'
        # title
        f'<g opacity="0">{title(line1, 150, size)}{title(line2, 150 + size, size)}'
        f'<animate attributeName="opacity" values="0;1" dur=".3s" begin="{delay:.2f}s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" values="-40 0;0 0" dur=".5s" begin="{delay:.2f}s" {once}/></g>'
        # shout burst, pulsing
        f'<g transform="translate({bx} {by})"><g>'
        f'<polygon points="{burst(5, 6, 62, 46, 11)}" fill="{BLUE}" stroke="{INK}" stroke-width="5" stroke-linejoin="round" transform="scale(.62 1)"/>'
        f'<polygon points="{burst(0, 0, 62, 46, 11)}" fill="#FFE45C" stroke="{INK}" stroke-width="5" stroke-linejoin="round" transform="scale(.62 1)"/>'
        f'<text class="c" x="0" y="11" text-anchor="middle" font-size="{34 if len(shout) <= 4 else 26}" fill="{RED}" '
        f'stroke="{INK}" stroke-width="4" paint-order="stroke" transform="rotate(-8)">{shout}</text>'
        f'<animateTransform attributeName="transform" type="scale" values="1;1.1;1" dur="1.6s" begin="{delay:.2f}s" '
        'calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1" repeatCount="indefinite"/></g></g>'
        # narration caption
        f'<g transform="rotate(-1 350 320)"><rect x="46" y="{258 + 6}" width="608" height="{38 + 32 * len(wrap(desc, 46))}" fill="{BLUE}" stroke="{INK}" stroke-width="4"/>'
        f'<rect x="40" y="258" width="608" height="{38 + 32 * len(wrap(desc, 46))}" fill="#FFE45C" stroke="{INK}" stroke-width="4"/>'
        f"{body}</g>"
        f'{"".join(chips)}'
        f'<text class="c" x="{W - 34}" y="{H - 36}" text-anchor="end" font-size="30" letter-spacing="2" fill="#fff">OPEN ISSUE'
        f'<animate attributeName="fill" values="#fff;{RED};#fff" dur="2.4s" repeatCount="indefinite"/></text>'
        "</svg>"
    )


# ---------- find me: spider-signal banner + comic buttons ----------

def spider_signal():
    W, H = 1400, 380
    ox, oy = 250, H - 150  # spotlight on a rooftop
    sx, sy, sr = 430, 130, 88  # where the signal lands in the sky
    bldg, windows = skyline(H - 6, rng_seed=11, h_range=(40, 115))
    beam_half = math.atan2(sr, math.dist((ox, oy), (sx, sy)))
    ang = math.atan2(sy - oy, sx - ox)
    far = math.dist((ox, oy), (sx, sy)) + sr
    p1 = (ox + far * math.cos(ang - beam_half), oy + far * math.sin(ang - beam_half))
    p2 = (ox + far * math.cos(ang + beam_half), oy + far * math.sin(ang + beam_half))
    sway = f'values="-4 {ox} {oy};4 {ox} {oy};-4 {ox} {oy}" dur="6s" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1" repeatCount="indefinite"'
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}"><defs>{FONT_CSS}'
        '<linearGradient id="beam" gradientUnits="userSpaceOnUse" '
        f'x1="{ox}" y1="{oy}" x2="{sx}" y2="{sy}"><stop offset="0" stop-color="#FFE9A8" stop-opacity=".75"/>'
        '<stop offset="1" stop-color="#FFE9A8" stop-opacity=".12"/></linearGradient>'
        '<radialGradient id="halo"><stop offset=".6" stop-color="#FFE9A8" stop-opacity=".95"/>'
        '<stop offset="1" stop-color="#FFE9A8" stop-opacity=".5"/></radialGradient>'
        '<pattern id="sd" width="16" height="16" patternUnits="userSpaceOnUse">'
        f'<circle cx="8" cy="8" r="3" fill="{BLUE}"/></pattern>'
        '<linearGradient id="sf" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".45"/>'
        '<stop offset=".6" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        f'<mask id="sm"><rect width="{W}" height="{H}" fill="url(#sf)"/></mask>'
        f'<clipPath id="sc"><rect x="6" y="6" width="{W - 12}" height="{H - 12}" rx="22"/></clipPath></defs>'
        f'<rect x="6" y="6" width="{W - 12}" height="{H - 12}" rx="22" fill="#0E1526"/>'
        f'<g clip-path="url(#sc)"><rect width="{W}" height="{H}" fill="url(#sd)" mask="url(#sm)"/>'
        # sweeping spotlight with the spider emblem on the clouds
        f'<g><polygon points="{ox},{oy} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="url(#beam)"/>'
        f'<circle cx="{sx}" cy="{sy}" r="{sr}" fill="url(#halo)"/>'
        f'<g transform="translate({sx - 60} {sy - 60}) scale(3.75)">{spider_shape(INK, 2.2)}</g>'
        f'<animateTransform attributeName="transform" type="rotate" {sway}/></g>'
        f'<g fill="#16213D">{bldg}</g><g fill="#FFE45C">{windows}</g>'
        f'<rect x="{ox - 60}" y="{oy + 14}" width="120" height="{H - oy}" fill="#1B274A"/>'
        f'<rect x="{ox - 22}" y="{oy - 6}" width="44" height="22" rx="4" fill="#2A3558" stroke="{INK}" stroke-width="3"/></g>'
        f'<rect x="6" y="6" width="{W - 12}" height="{H - 12}" rx="22" fill="none" stroke="{RED}" stroke-width="6"/>'
        # copy
        f'<text class="c" x="{960 + 7}" y="{150 + 7}" text-anchor="middle" font-size="118" fill="{BLUE}" stroke="{INK}" '
        f'stroke-width="10" stroke-linejoin="round" paint-order="stroke">NEED A HERO?</text>'
        f'<text class="c" x="960" y="150" text-anchor="middle" font-size="118" fill="{RED}" stroke="{INK}" '
        f'stroke-width="10" stroke-linejoin="round" paint-order="stroke">NEED A HERO?</text>'
        f'<text class="c" x="960" y="208" text-anchor="middle" font-size="42" letter-spacing="2" fill="#fff" '
        f'stroke="{INK}" stroke-width="6" paint-order="stroke">OR A DESIGNER WHO CODES</text>'
        f'<g transform="rotate(-2 960 262)"><rect x="745" y="236" width="430" height="50" fill="#FFE45C" stroke="{INK}" stroke-width="4"/>'
        f'<text class="c" x="960" y="272" text-anchor="middle" font-size="31" letter-spacing="2" fill="{INK}">'
        "SEND THE SIGNAL. I'LL SWING BY.</text></g>"
        "</svg>"
    )


CONTACTS = [
    ("portfolio", "PORTFOLIO", RED, "web"),
    ("behance", "BEHANCE", BLUE, "Bē"),
    ("linkedin", "LINKEDIN", BLUE, "in"),
    ("instagram", "INSTAGRAM", RED, "cam"),
    ("email", "EMAIL", "#FFE45C", "mail"),
]


def contact_button(key, label, color, glyph):
    W, H = 300, 100
    ink_text = color == "#FFE45C"
    fg = INK if ink_text else "#fff"
    ix, iy = 50, 47
    if glyph == "web":
        icon = f'<g transform="translate({ix - 20} {iy - 20}) scale(1.25)">{icon_web(fg)[icon_web(fg).index(">") + 1:-6]}</g>'
    elif glyph == "cam":
        icon = (f'<rect x="{ix - 17}" y="{iy - 17}" width="34" height="34" rx="10" fill="none" stroke="{fg}" stroke-width="3.5"/>'
                f'<circle cx="{ix}" cy="{iy}" r="8" fill="none" stroke="{fg}" stroke-width="3.5"/>'
                f'<circle cx="{ix + 10}" cy="{iy - 10}" r="2.2" fill="{fg}"/>')
    elif glyph == "mail":
        icon = (f'<rect x="{ix - 19}" y="{iy - 13}" width="38" height="27" rx="3" fill="none" stroke="{fg}" stroke-width="3.5"/>'
                f'<path d="M{ix - 17} {iy - 11} L{ix} {iy + 2} L{ix + 17} {iy - 11}" fill="none" stroke="{fg}" stroke-width="3.5" stroke-linejoin="round"/>')
    else:
        icon = (f'<text x="{ix}" y="{iy + 12}" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" '
                f'font-weight="900" font-size="34" fill="{fg}">{glyph}</text>')
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}"><defs>{FONT_CSS}</defs>'
        f'<rect x="12" y="12" width="{W - 18}" height="{H - 18}" rx="10" fill="{INK}"/>'
        f'<g><rect x="4" y="4" width="{W - 18}" height="{H - 18}" rx="10" fill="{color}" stroke="{INK}" stroke-width="5"/>'
        f'<line x1="92" y1="16" x2="92" y2="{H - 26}" stroke="{fg}" stroke-opacity=".35" stroke-width="2"/>'
        f"{icon}"
        f'<text class="c" x="{(92 + W - 14) / 2 + 4}" y="{iy + 13}" text-anchor="middle" font-size="38" letter-spacing="2" '
        f'fill="{fg}">{label}</text></g>'
        "</svg>"
    )


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    write("spider-signal.svg", spider_signal())
    (ASSETS / "contact").mkdir(exist_ok=True)
    for c in CONTACTS:
        write(f"contact/{c[0]}.svg", contact_button(*c))
    (ASSETS / "projects").mkdir(exist_ok=True)
    for i, p in enumerate(PROJECTS):
        write(f"projects/{p[0]}.svg", project_card(i, *p))
    write("header.svg", header())
    write("spider-red.svg", icon_spider(RED))
    write("spider-blue.svg", icon_spider(BLUE_LT))
    write("mask.svg", icon_mask())
    write("web.svg", icon_web(WEB))
    write("spider-hanging.svg", icon_hanging(RED))
    write("web-divider.svg", web_divider())
    write("suit-divider.svg", suit_divider())
    write("techstack-web.svg", techstack())
    write("footer-swing.svg", footer_swing())
