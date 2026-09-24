"""Spider-Man version of the aayushvz logo (slash + dot) as a profile picture.
Run: python build/avatar.py  (writes assets/avatar.svg and assets/avatar.png)
"""
import math
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_assets import ASSETS, BLUE, INK, RED, RED_DK, WEB, spider_shape  # noqa: E402

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
W = 1000
# logo geometry measured from the 2000px source logo, centred and scaled to stay inside a circular crop
s = 0.54
ox, oy = 500 - 953 * s, 520 - 935 * s


def P(x, y):
    return f"{ox + x * s:.1f} {oy + y * s:.1f}"


slash = f"M{P(1262, 447)} L{P(735, 1422)} L{P(318, 1422)} L{P(790, 552)} Q{P(845, 447)} {P(965, 447)} Z"
cx, cy, r = ox + 1345 * s, oy + 1178 * s, 243 * s


def build():
    spokes = [i * math.pi / 8 for i in range(16)]
    web = [f'<path d="M500 500 L{500 + 800 * math.cos(a):.1f} {500 + 800 * math.sin(a):.1f}"/>' for a in spokes]
    for rr in range(70, 760, 85):
        pts = [(500 + rr * math.cos(a), 500 + rr * math.sin(a)) for a in spokes]
        pts.append(pts[0])
        d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
        for p0, p1 in zip(pts, pts[1:]):
            mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
            d += f" Q{500 + (mx - 500) * .9:.1f} {500 + (my - 500) * .9:.1f} {p1[0]:.1f} {p1[1]:.1f}"
        web.append(f'<path d="{d}"/>')

    # suit seams inside the slash
    sx, sy = ox + 700 * s, oy + 1000 * s
    seams = [f'<path d="M{sx:.1f} {sy:.1f} L{sx + 700 * math.cos(a):.1f} {sy + 700 * math.sin(a):.1f}"/>'
             for a in [i * math.pi / 6 for i in range(12)]]
    seams += [f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="{rr * s / 0.5:.0f}"/>' for rr in (70, 150, 240, 340)]

    # the dot becomes a chest emblem hanging on a thread
    emblem = f'<g transform="translate({cx - r * 0.62:.1f} {cy - r * 0.64:.1f}) scale({r * 1.24 / 32:.3f})">{spider_shape(INK, 2.6)}</g>'
    sh = 22
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {W}" width="{W}" height="{W}">
<defs>
<pattern id="d" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="11" cy="11" r="4" fill="{BLUE}"/></pattern>
<radialGradient id="g" cx="50%" cy="50%" r="60%"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff" stop-opacity=".55"/></radialGradient>
<mask id="m"><rect width="{W}" height="{W}" fill="url(#g)"/></mask>
<radialGradient id="glow" cx="50%" cy="52%" r="45%"><stop offset="0" stop-color="{RED}" stop-opacity=".28"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></radialGradient>
<clipPath id="sl"><path d="{slash}"/></clipPath>
</defs>
<rect width="{W}" height="{W}" fill="#0E1526"/>
<rect width="{W}" height="{W}" fill="url(#d)" mask="url(#m)"/>
<rect width="{W}" height="{W}" fill="url(#glow)"/>
<g stroke="{WEB}" stroke-width="3" fill="none" opacity=".32">{"".join(web)}</g>
<line x1="{cx:.1f}" y1="0" x2="{cx:.1f}" y2="{cy - r:.1f}" stroke="#E6EDF3" stroke-width="7"/>
<path d="{slash}" fill="{BLUE}" stroke="{INK}" stroke-width="20" stroke-linejoin="round" transform="translate({sh} {sh})"/>
<circle cx="{cx + sh:.1f}" cy="{cy + sh:.1f}" r="{r:.1f}" fill="{BLUE}" stroke="{INK}" stroke-width="20"/>
<path d="{slash}" fill="{RED}"/>
<g clip-path="url(#sl)" stroke="{RED_DK}" stroke-width="5" fill="none" opacity=".9">{"".join(seams)}</g>
<path d="{slash}" fill="none" stroke="{INK}" stroke-width="20" stroke-linejoin="round"/>
<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{RED}" stroke="{INK}" stroke-width="20"/>
{emblem}
</svg>'''


if __name__ == "__main__":
    svg_path = ASSETS / "avatar.svg"
    svg_path.write_text(build(), encoding="utf-8")
    page = Path(__file__).parent / "_static" / "avatar.html"
    page.parent.mkdir(exist_ok=True)
    page.write_text(f'<html><body style="margin:0"><img src="{svg_path.as_uri()}" width="{W}" height="{W}" style="display:block"></body></html>')
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={W},{W}",
                    f"--screenshot={(ASSETS / 'avatar.png').resolve()}", page.resolve().as_uri()], capture_output=True)
    print("assets/avatar.svg, assets/avatar.png")
