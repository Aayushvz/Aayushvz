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

def burst(cx, cy, r_out, r_in, n=14):
    pts = []
    for i in range(n * 2):
        a = math.pi * i / n - math.pi / 2
        # uneven spikes read as hand-drawn comic
        r = r_out * (1 if i % 4 == 0 else 0.9) if i % 2 == 0 else r_in
        pts.append(f"{cx + r * math.cos(a) * 1.55:.1f},{cy + r * math.sin(a):.1f}")
    return " ".join(pts)


def techstack():
    W, H = 1400, 760
    T = 2.2  # seconds per tech
    N = len(TECH)
    total = T * N
    cx, cy = 820, 520
    sx, sy = 330, 520  # spider at rest
    eps = 0.001

    halftone = (
        '<pattern id="dots" width="14" height="14" patternUnits="userSpaceOnUse">'
        f'<circle cx="7" cy="7" r="2.6" fill="{BLUE}"/></pattern>'
        '<radialGradient id="fade" cx="50%" cy="50%" r="50%">'
        '<stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
        '<mask id="m"><rect width="1400" height="330" fill="url(#fade)"/></mask>'
    )

    title = (
        f'<rect width="1400" height="330" fill="url(#dots)" mask="url(#m)"/>'
        f'<text class="c" x="708" y="238" text-anchor="middle" font-size="168" fill="{BLUE}" '
        f'stroke="{INK}" stroke-width="10" stroke-linejoin="round" paint-order="stroke">MY TECH-STACK</text>'
        f'<text class="c" x="700" y="228" text-anchor="middle" font-size="168" fill="{RED}" '
        f'stroke="{INK}" stroke-width="10" stroke-linejoin="round" paint-order="stroke">MY TECH-STACK</text>'
        f'<text class="c" x="700" y="228" text-anchor="middle" font-size="168" fill="none" '
        'stroke="#fff" stroke-opacity=".35" stroke-width="2">MY TECH-STACK</text>'
    )

    spline = 'calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"'
    # thread from top + spider bobbing, synced to each tech cycle
    spider = (
        f'<g><line x1="{sx}" y1="300" x2="{sx}" y2="{sy - 10}" stroke="{WEB}" stroke-width="2.5"/>'
        f'<g transform="translate({sx - 48} {sy - 40}) scale(3)">{spider_shape(RED, 2)}</g>'
        f'<animateTransform attributeName="transform" type="translate" values="0 -14;0 10;0 -14" '
        f'dur="{T}s" {spline} repeatCount="indefinite"/></g>'
    )

    # web line shot from spider to the burst at the start of each cycle
    shot_len = cx - 300 - sx
    shot = (
        f'<line x1="{sx + 40}" y1="{sy}" x2="{cx - 260}" y2="{cy}" stroke="#fff" stroke-width="3" '
        f'stroke-linecap="round" stroke-dasharray="{shot_len} {shot_len}">'
        f'<animate attributeName="stroke-dashoffset" values="{shot_len};0;0;{-shot_len};{-shot_len}" '
        f'keyTimes="0;.12;.2;.32;1" dur="{T}s" repeatCount="indefinite"/></line>'
        f'<text class="c" x="{sx + 70}" y="{sy - 70}" font-size="46" fill="#fff" stroke="{INK}" '
        f'stroke-width="6" paint-order="stroke" transform="rotate(-8 {sx + 70} {sy - 70})">THWIP!'
        f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;.05;.25;.35;1" dur="{T}s" repeatCount="indefinite"/></text>'
    )

    pop = (
        f'<animateTransform attributeName="transform" type="scale" values=".55;1.08;1;1;.9" '
        f'keyTimes="0;.14;.22;.9;1" dur="{T}s" repeatCount="indefinite" additive="sum"/>'
    )
    burst_g = (
        f'<g transform="translate({cx} {cy})"><g>'
        f'<polygon points="{burst(8, 10, 205, 165)}" fill="{BLUE}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
        f'<polygon points="{burst(0, 0, 205, 165)}" fill="#FFF7E6" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
        f"{pop}"
    )
    names = []
    for i, name in enumerate(TECH):
        s, e = i / N, (i + 1) / N
        size = 88 if len(name) <= 9 else 70
        if i == 0:
            vals, kt = "1;1;0;0", f"0;{e - eps:.4f};{e:.4f};1"
        elif i == N - 1:
            vals, kt = "0;0;1;1", f"0;{s - eps:.4f};{s:.4f};1"
        else:
            vals, kt = "0;0;1;1;0;0", f"0;{s - eps:.4f};{s:.4f};{e - eps:.4f};{e:.4f};1"
        names.append(
            f'<text class="c" x="0" y="{size * 0.35:.0f}" text-anchor="middle" font-size="{size}" '
            f'fill="{RED}" stroke="{INK}" stroke-width="5" stroke-linejoin="round" paint-order="stroke" opacity="{1 if i == 0 else 0}">'
            f'{name}<animate attributeName="opacity" values="{vals}" keyTimes="{kt}" dur="{total}s" '
            f'calcMode="discrete" repeatCount="indefinite"/></text>'
        )
    burst_g += "".join(names) + "</g></g>"

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}"><defs>{FONT_CSS}{halftone}</defs>'
        f"{title}{spider}{shot}{burst_g}</svg>"
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


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
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
