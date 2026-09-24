"""Portrait versions of the wide banners, served to phones via <picture media>.
Run: python build/mobile.py  (writes assets/m/*.svg)
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_assets import (  # noqa: E402
    ASSETS, BLUE, CONTACTS, DESIGN, FONT_CSS, INK, POWERS, PROFILE, PROJECTS, RED, TECH, WEB,
    big_web, burst, footer_swing, suit_divider, web_divider, icon_mask, icon_web, skyline, spider_shape, tagline, write, wrap,
)

SANS = "font-family=\"'Segoe UI',Helvetica,Arial,sans-serif\""
SPLINE = 'calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"'
ONCE = 'fill="freeze" calcMode="spline" keySplines=".2 .9 .3 1"'


def panel(W, H, uid, web_corner="br"):
    """Navy comic panel with halftone, a corner web and a red border."""
    corner = big_web(W - 6, H - 6, min(W, H) * 0.4, 180, 270, 4, 6) if web_corner == "br" else big_web(6, 6, min(W, H) * 0.45, 0, 90, 4, 6)
    defs = (
        f'<pattern id="{uid}d" width="16" height="16" patternUnits="userSpaceOnUse"><circle cx="8" cy="8" r="3" fill="{BLUE}"/></pattern>'
        f'<linearGradient id="{uid}f" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".45"/>'
        '<stop offset=".5" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        f'<mask id="{uid}m"><rect width="{W}" height="{H}" fill="url(#{uid}f)"/></mask>'
        f'<clipPath id="{uid}c"><rect x="6" y="6" width="{W - 12}" height="{H - 12}" rx="22"/></clipPath>'
    )
    back = (
        f'<rect x="6" y="6" width="{W - 12}" height="{H - 12}" rx="22" fill="#0E1526"/>'
        f'<g clip-path="url(#{uid}c)"><rect width="{W}" height="{H}" fill="url(#{uid}d)" mask="url(#{uid}m)"/>'
        f'<g stroke="{WEB}" stroke-width="1.5" fill="none" opacity=".4">{corner}</g></g>'
    )
    border = f'<rect x="6" y="6" width="{W - 12}" height="{H - 12}" rx="22" fill="none" stroke="{RED}" stroke-width="6"/>'
    return defs, back, border


def comic_title(text, x, y, size, anchor="middle", sw=None):
    sw = sw or max(6, size // 14)
    return "".join(
        f'<text class="c" x="{x + d}" y="{y + d}" text-anchor="{anchor}" font-size="{size}" fill="{c}" stroke="{INK}" '
        f'stroke-width="{sw}" stroke-linejoin="round" paint-order="stroke">{text}</text>'
        for d, c in ((max(4, size // 22), BLUE), (0, RED))
    )


def caption_box(x, y, w, label, body, rot=0, body_size=30):
    h = 108
    return (
        f'<g transform="rotate({rot} {x + w / 2} {y + h / 2})">'
        f'<rect x="{x + 7}" y="{y + 7}" width="{w}" height="{h}" fill="{BLUE}" stroke="{INK}" stroke-width="5"/>'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#FFE45C" stroke="{INK}" stroke-width="5"/>'
        f'<rect x="{x}" y="{y}" width="{w}" height="44" fill="{RED}" stroke="{INK}" stroke-width="5"/>'
        f'<text class="c" x="{x + 18}" y="{y + 34}" font-size="32" letter-spacing="2" fill="#fff">{label}</text>'
        f'<text x="{x + 18}" y="{y + 90}" {SANS} font-weight="700" font-size="{body_size}" fill="{INK}">{body}</text></g>'
    )


def svg(W, H, defs, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}"><defs>{FONT_CSS}{defs}</defs>{body}</svg>'


# ---------- header ----------

def header_m():
    W, H = 600, 950
    defs, back, border = panel(W, H, "h", "tl")
    sx = 548
    spider = (
        f'<g><line x1="{sx}" y1="6" x2="{sx}" y2="150" stroke="#C9D1D9" stroke-width="2.5"/>'
        f'<g transform="translate({sx - 40} 134) scale(2.5)">{spider_shape(RED, 2)}</g>'
        f'<animateTransform attributeName="transform" type="translate" values="0 -200;0 0" dur="1s" {ONCE}/>'
        f'<animateTransform attributeName="transform" type="translate" values="0 0;0 12;0 0" begin="1s" dur="2.6s" '
        f'{SPLINE} repeatCount="indefinite" additive="sum"/></g>'
    )
    title = (
        f'<g>{comic_title("AAYUSH", 250, 250, 170)}{comic_title("RAJ", 250, 400, 170)}'
        f'<animateTransform attributeName="transform" type="translate" values="-40 0;0 0" dur=".6s" {ONCE}/></g>'
        + "".join(
            f'<text class="c" x="300" y="{470 + i * 46}" text-anchor="middle" font-size="42" letter-spacing="2" fill="#fff" '
            f'stroke="{INK}" stroke-width="6" paint-order="stroke">{ln}</text>'
            for i, ln in enumerate(["YOUR FRIENDLY NEIGHBOURHOOD", "PIXEL-SLINGER"])
        )
    )
    caps = [("WHO?", "Designer who codes", -1.5), ("BASE", "VIT Vellore, final year", 1), ("SPIDER-SENSE", "Something is 1px off.", -1)]
    boxes = "".join(caption_box(50, 560 + i * 122, 500, l, b, r, 28) for i, (l, b, r) in enumerate(caps))
    return svg(W, H, defs, back + spider + title + boxes + border)


# ---------- hero profile ----------

def hero_profile_m():
    W, H = 600, 1060
    defs, back, border = panel(W, H, "r")
    mask = icon_mask()
    inner = mask[mask.index(">") + 1:-len("</svg>")]
    at = inner.index('<path d="M5.5')
    head = inner[:at].replace('id="h"', 'id="rmh"').replace("url(#h)", "url(#rmh)")
    eyes = inner[at:]
    cx, cy, ps = 300, 250, 7
    portrait = (
        f'<pattern id="rdp" width="12" height="12" patternUnits="userSpaceOnUse"><rect width="12" height="12" fill="#1B274A"/>'
        f'<circle cx="6" cy="6" r="2.4" fill="{BLUE}"/></pattern>'
        f'<circle cx="{cx}" cy="{cy}" r="{17.5 * ps}" fill="url(#rdp)" stroke="{INK}" stroke-width="6"/>'
        f'<g transform="translate({cx - 16 * ps} {cy - 16.5 * ps}) scale({ps})">{head}'
        f'<g transform="translate(16 14)"><g><g transform="translate(-16 -14)">{eyes}</g>'
        '<animateTransform attributeName="transform" type="scale" values="1 1;1 1;1 .08;1 1" keyTimes="0;.92;.96;1" '
        'dur="4.5s" repeatCount="indefinite"/></g></g></g>'
    )
    top = comic_title("HERO PROFILE", 300, 96, 76)
    alias = (
        f'<g transform="rotate(-3 300 420)"><rect x="96" y="398" width="408" height="52" fill="{BLUE}" stroke="{INK}" stroke-width="4"/>'
        f'<rect x="90" y="392" width="408" height="52" fill="#FFE45C" stroke="{INK}" stroke-width="4"/>'
        f'<text class="c" x="294" y="429" text-anchor="middle" font-size="31" letter-spacing="2" fill="{INK}">ALIAS: THE PIXEL-SLINGER</text></g>'
    )
    rows = []
    y = 506
    for label, value in PROFILE:
        lines = wrap(value, 34)
        rows.append(f'<text class="c" x="50" y="{y}" font-size="30" letter-spacing="2" fill="{RED}">{label}</text>')
        for j, ln in enumerate(lines):
            rows.append(f'<text x="50" y="{y + 38 + j * 34}" {SANS} font-weight="700" font-size="27" fill="#F0F3F6">{ln}</text>')
        y += 38 + 34 * len(lines) + 14
        rows.append(f'<line x1="50" y1="{y - 24}" x2="550" y2="{y - 24}" stroke="#8B949E" stroke-opacity=".35" stroke-width="2" stroke-dasharray="4 8"/>')
        y += 12
    rows.append(f'<text class="c" x="50" y="{y + 6}" font-size="30" letter-spacing="2" fill="{RED}">POWERS</text>')
    chips = []
    for i, p in enumerate(POWERS):
        w = len(p) * 16 + 40
        cy2 = y + 30 + i * 62
        chips.append(
            f'<g transform="rotate({(-2, 1.5, -1)[i]} {50 + w / 2} {cy2 + 25})">'
            f'<rect x="56" y="{cy2 + 6}" width="{w}" height="50" rx="6" fill="{INK}"/>'
            f'<rect x="50" y="{cy2}" width="{w}" height="50" rx="6" fill="{(RED, BLUE, RED)[i]}" stroke="{INK}" stroke-width="4"/>'
            f'<text class="c" x="{50 + w / 2}" y="{cy2 + 36}" text-anchor="middle" font-size="30" letter-spacing="1" fill="#fff">{p}</text></g>'
        )
    H = y + 30 + 3 * 62 + 30
    defs, back, border = panel(W, H, "r")
    return svg(W, H, defs, back + top + portrait + alias + "".join(rows) + "".join(chips) + border)


# ---------- tech stack: tags hang in a web column, spider climbs down ----------

def techstack_m():
    W = 600
    per_tag = 1.6
    n = len(TECH)
    total = per_tag * n
    order = [t for t in TECH]
    rows = math.ceil(n / 2)
    top, step = 250, 96
    H = top + rows * step + 90
    defs, back, border = panel(W, H, "t")
    moon = (
        '<radialGradient id="tglow"><stop offset="0" stop-color="#F3EBD3" stop-opacity=".35"/>'
        '<stop offset="1" stop-color="#F3EBD3" stop-opacity="0"/></radialGradient>'
    )
    bldg, windows = skyline(H - 6, rng_seed=3, h_range=(120, 340))
    scene = (
        f'<g clip-path="url(#tc)"><circle cx="505" cy="175" r="90" fill="url(#tglow)"/><circle cx="505" cy="175" r="44" fill="#F3EBD3"/>'
        f'<g fill="#16213D">{bldg}</g><g fill="#FFE45C">{windows}</g></g>'
    )
    title = comic_title("MY TECH-STACK", 272, 110, 84) + (
        f'<g transform="rotate(-3 250 160)"><rect x="80" y="136" width="330" height="44" fill="#FFE45C" stroke="{INK}" stroke-width="4"/>'
        f'<text class="c" x="245" y="168" text-anchor="middle" font-size="28" letter-spacing="2" fill="{INK}">CAUGHT IN MY WEB</text></g>'
    )
    # zigzag web: vertical silk in the middle, tags alternate left/right
    silk = f'<line x1="300" y1="200" x2="300" y2="{top + rows * step}" stroke="#C9D1D9" stroke-width="2.5" opacity=".6"/>'
    pts, tags = [], []
    for i, name in enumerate(order):
        row, side = divmod(i, 2)
        x = 160 if side == 0 else 440
        y = top + row * step + (0 if side == 0 else 40)
        pts.append((300, y))
        silk += f'<line x1="300" y1="{y}" x2="{x}" y2="{y}" stroke="#C9D1D9" stroke-width="2" opacity=".45"/>'
        base = RED if name in DESIGN else BLUE
        w = len(name) * 16 + 40
        s, e = i / n, (i + 0.7) / n
        k = f"0;{s:.4f};{s + 0.01:.4f};{e:.4f};{e + 0.01:.4f};1"
        rot = ((i * 37) % 7) - 3
        tags.append(
            f'<g transform="translate({x} {y}) rotate({rot})">'
            f'<rect x="{-w / 2 + 6}" y="-19" width="{w}" height="50" rx="6" fill="{INK}"/>'
            f'<rect x="{-w / 2}" y="-25" width="{w}" height="50" rx="6" fill="{base}" stroke="{INK}" stroke-width="4">'
            f'<animate attributeName="fill" values="{base};{base};#FFE45C;#FFE45C;{base};{base}" keyTimes="{k}" dur="{total}s" repeatCount="indefinite"/></rect>'
            f'<text class="c" x="0" y="11" text-anchor="middle" font-size="32" letter-spacing="1" fill="#fff">{name}'
            f'<animate attributeName="fill" values="#fff;#fff;{INK};{INK};#fff;#fff" keyTimes="{k}" dur="{total}s" repeatCount="indefinite"/></text></g>'
        )
    ys = [p[1] for p in pts]
    kp = []
    kt = []
    span = ys[-1] - ys[0]
    for i, y in enumerate(ys):
        kp += [(y - ys[0]) / span] * 2
        kt += [i / n, (i + 0.7) / n]
    kp.append(0)
    kt.append(1)
    path = f"M300 {ys[0]} L300 {ys[-1]}"
    spider = (
        f'<g><g transform="translate(-30 -30) scale(1.9)">{spider_shape(INK, 3.4)}</g>'
        f'<g transform="translate(-30 -30) scale(1.9)">{spider_shape(RED, 2)}</g>'
        f'<animateMotion dur="{total}s" repeatCount="indefinite" path="{path}" '
        f'keyPoints="{";".join(f"{v:.4f}" for v in kp)}" keyTimes="{";".join(f"{v:.4f}" for v in kt)}" calcMode="linear"/></g>'
    )
    legend = (
        f'<g transform="translate(40 {H - 50})"><rect width="24" height="24" rx="4" fill="{RED}" stroke="{INK}" stroke-width="3"/>'
        f'<text class="c" x="34" y="21" font-size="26" fill="#fff" stroke="{INK}" stroke-width="4" paint-order="stroke">DESIGN</text>'
        f'<rect x="140" width="24" height="24" rx="4" fill="{BLUE}" stroke="{INK}" stroke-width="3"/>'
        f'<text class="c" x="174" y="21" font-size="26" fill="#fff" stroke="{INK}" stroke-width="4" paint-order="stroke">CODE</text></g>'
    )
    return svg(W, H, defs + moon, back + scene + title + silk + "".join(tags) + spider + legend + border)


# ---------- project covers: title-first, readable at half a phone width ----------

def project_m(idx, key, line1, line2, genre, shout, desc, tags):
    W, H = 500, 560
    lines = wrap(f"{line1} {line2}", 11)
    size = 92 if max(len(l) for l in lines) <= 8 else 76
    title = "".join(comic_title(l, 250, 190 + i * (size + 4), size) for i, l in enumerate(lines))
    return svg(
        W, H,
        f'<clipPath id="pc"><rect x="5" y="5" width="{W - 10}" height="{H - 10}" rx="20"/></clipPath>'
        f'<pattern id="pd" width="14" height="14" patternUnits="userSpaceOnUse"><circle cx="7" cy="7" r="2.6" fill="{BLUE}"/></pattern>',
        f'<rect x="5" y="5" width="{W - 10}" height="{H - 10}" rx="20" fill="#0E1526"/>'
        f'<g clip-path="url(#pc)"><rect width="{W}" height="{H}" fill="url(#pd)" opacity=".45"/>'
        f'<rect width="{W}" height="86" fill="{RED}"/><rect y="86" width="{W}" height="6" fill="{INK}"/>'
        f'<text class="c" x="{W / 2}" y="62" text-anchor="middle" font-size="52" letter-spacing="2" fill="#fff">ISSUE #{idx + 1:02d}</text></g>'
        f'<rect x="5" y="5" width="{W - 10}" height="{H - 10}" rx="20" fill="none" stroke="{RED}" stroke-width="6"/>'
        f"{title}"
        f'<g transform="rotate(-3 250 {H - 110})"><rect x="46" y="{H - 146}" width="408" height="64" fill="{BLUE}" stroke="{INK}" stroke-width="5"/>'
        f'<rect x="40" y="{H - 152}" width="408" height="64" fill="#FFE45C" stroke="{INK}" stroke-width="5"/>'
        f'<text class="c" x="244" y="{H - 106}" text-anchor="middle" font-size="44" letter-spacing="2" fill="{INK}">{genre}</text></g>'
        f'<text class="c" x="{W / 2}" y="{H - 34}" text-anchor="middle" font-size="36" letter-spacing="2" fill="#fff">TAP TO OPEN'
        f'<animate attributeName="fill" values="#fff;{RED};#fff" dur="2.4s" repeatCount="indefinite"/></text>',
    )


# ---------- contact tiles: big icon, short label ----------

def contact_m(key, label, color, glyph):
    W, H = 240, 240
    fg = INK if color == "#FFE45C" else "#fff"
    c, cy = 120, 100
    if glyph == "web":
        w = icon_web(fg)
        icon = f'<g transform="translate({c - 56} {cy - 56}) scale(3.5)">{w[w.index(">") + 1:-6]}</g>'
    elif glyph == "cam":
        icon = (f'<rect x="{c - 46}" y="{cy - 46}" width="92" height="92" rx="26" fill="none" stroke="{fg}" stroke-width="9"/>'
                f'<circle cx="{c}" cy="{cy}" r="22" fill="none" stroke="{fg}" stroke-width="9"/><circle cx="{c + 27}" cy="{cy - 27}" r="6" fill="{fg}"/>')
    elif glyph == "mail":
        icon = (f'<rect x="{c - 52}" y="{cy - 36}" width="104" height="72" rx="8" fill="none" stroke="{fg}" stroke-width="9"/>'
                f'<path d="M{c - 46} {cy - 30} L{c} {cy + 6} L{c + 46} {cy - 30}" fill="none" stroke="{fg}" stroke-width="9" stroke-linejoin="round"/>')
    else:
        icon = (f'<text x="{c}" y="{cy + 34}" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-weight="900" '
                f'font-size="96" fill="{fg}">{glyph}</text>')
    short = {"PORTFOLIO": "SITE", "INSTAGRAM": "INSTA"}.get(label, label)
    return svg(
        W, H, "",
        f'<rect x="14" y="14" width="{W - 22}" height="{H - 22}" rx="18" fill="{INK}"/>'
        f'<rect x="5" y="5" width="{W - 22}" height="{H - 22}" rx="18" fill="{color}" stroke="{INK}" stroke-width="6"/>'
        f"{icon}"
        f'<text class="c" x="{(W - 17) / 2 + 3}" y="{H - 38}" text-anchor="middle" font-size="46" letter-spacing="2" fill="{fg}">{short}</text>',
    )


# ---------- spider-signal ----------

def signal_m():
    W, H = 600, 700
    defs, back, border = panel(W, H, "s")
    ox, oy = 110, 330
    sx, sy, sr = 330, 150, 92
    d = math.dist((ox, oy), (sx, sy))
    ang = math.atan2(sy - oy, sx - ox)
    half = math.atan2(sr, d)
    far = d + sr
    p1 = (ox + far * math.cos(ang - half), oy + far * math.sin(ang - half))
    p2 = (ox + far * math.cos(ang + half), oy + far * math.sin(ang + half))
    bldg, windows = skyline(H - 6, rng_seed=11, h_range=(40, 110))
    sway = f'values="-5 {ox} {oy};5 {ox} {oy};-5 {ox} {oy}" dur="6s" {SPLINE} repeatCount="indefinite"'
    extra = (
        f'<linearGradient id="sb" gradientUnits="userSpaceOnUse" x1="{ox}" y1="{oy}" x2="{sx}" y2="{sy}">'
        '<stop offset="0" stop-color="#FFE9A8" stop-opacity=".75"/><stop offset="1" stop-color="#FFE9A8" stop-opacity=".12"/></linearGradient>'
    )
    scene = (
        f'<g clip-path="url(#sc)"><g><polygon points="{ox},{oy} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="url(#sb)"/>'
        f'<circle cx="{sx}" cy="{sy}" r="{sr}" fill="#FFE9A8" opacity=".95"/>'
        f'<g transform="translate({sx - 62} {sy - 62}) scale(3.9)">{spider_shape(INK, 2.2)}</g>'
        f'<animateTransform attributeName="transform" type="rotate" {sway}/></g>'
        f'<rect x="{ox - 50}" y="{oy + 12}" width="100" height="{H - oy}" fill="#1B274A"/>'
        f'<rect x="{ox - 20}" y="{oy - 6}" width="40" height="20" rx="4" fill="#2A3558" stroke="{INK}" stroke-width="3"/>'
        f'<g fill="#16213D">{bldg}</g><g fill="#FFE45C">{windows}</g></g>'
    )
    copy = (
        comic_title("NEED A HERO?", 300, 440, 92)
        + f'<text class="c" x="300" y="498" text-anchor="middle" font-size="40" letter-spacing="2" fill="#fff" stroke="{INK}" '
        f'stroke-width="6" paint-order="stroke">OR A DESIGNER WHO CODES</text>'
        f'<g transform="rotate(-2 300 555)"><rect x="70" y="528" width="460" height="54" fill="#FFE45C" stroke="{INK}" stroke-width="4"/>'
        f'<text class="c" x="300" y="567" text-anchor="middle" font-size="32" letter-spacing="2" fill="{INK}">'
        "SEND THE SIGNAL. I'LL SWING BY.</text></g>"
    )
    return svg(W, H, defs + extra, back + scene + copy + border)


# ---------- portfolio CTA ----------

def cta_m():
    W, H = 560, 300
    return svg(
        W, H, "",
        f'<rect x="29" y="79" width="510" height="190" rx="14" fill="{BLUE}" stroke="{INK}" stroke-width="6"/>'
        f'<rect x="20" y="70" width="510" height="190" rx="14" fill="#FFE45C" stroke="{INK}" stroke-width="6"/>'
        f'<path d="M34 70 H516 A14 14 0 0 1 530 84 V132 H20 V84 A14 14 0 0 1 34 70Z" fill="{RED}" stroke="{INK}" stroke-width="6"/>'
        f'<text class="c" x="275" y="116" text-anchor="middle" font-size="40" letter-spacing="2" fill="#fff" stroke="{INK}" '
        f'stroke-width="5" paint-order="stroke">SWING BY THE PORTFOLIO</text>'
        f'<text x="60" y="210" {SANS} font-weight="800" font-size="40" fill="{INK}">aayushvisuals.com</text>'
        f'<g><g transform="translate(470 196)"><polygon points="{burst(0, 0, 40, 30, 10)}" transform="scale(.62 1)" fill="#fff" '
        f'stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
        f'<path d="M-15 0 H13 M1 -12 L14 0 L1 12" stroke="{RED}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>'
        f'<animateTransform attributeName="transform" type="translate" values="0 0;7 0;0 0" dur="1.2s" {SPLINE} repeatCount="indefinite"/></g>'
        f'<g><line x1="440" y1="0" x2="440" y2="72" stroke="#8B949E" stroke-width="2"/>'
        f'<g transform="translate(418 36) scale(1.4)">{spider_shape(INK, 3.2)}</g><g transform="translate(418 36) scale(1.4)">{spider_shape(RED, 1.9)}</g>'
        f'<animateTransform attributeName="transform" type="translate" values="0 -22;0 -4;0 -22" dur="2.6s" {SPLINE} repeatCount="indefinite"/></g>',
    )


if __name__ == "__main__":
    out = ASSETS / "m"
    (out / "projects").mkdir(parents=True, exist_ok=True)
    (out / "contact").mkdir(exist_ok=True)
    write("m/header.svg", header_m())
    write("m/tagline.svg", tagline(mobile=True))
    write("m/hero-profile.svg", hero_profile_m())
    write("m/portfolio-cta.svg", cta_m())
    write("m/techstack-web.svg", techstack_m())
    for i, p in enumerate(PROJECTS):
        write(f"m/projects/{p[0]}.svg", project_m(i, *p))
    write("m/spider-signal.svg", signal_m())
    write("m/footer-swing.svg", footer_swing(mobile=True))
    write("m/web-divider.svg", web_divider(600))
    write("m/suit-divider.svg", suit_divider(600))
    for c in CONTACTS:
        write(f"m/contact/{c[0]}.svg", contact_m(*c))
