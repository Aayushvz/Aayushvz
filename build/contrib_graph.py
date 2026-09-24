"""Draws the Spider-Man contribution graph from live GitHub data.

Run by .github/workflows/spider.yml every day. Locally:
    GITHUB_TOKEN=$(gh auth token) python build/contrib_graph.py Aayushvz dist
"""
import datetime as dt
import json
import math
import os
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_assets import BLUE, FONT_CSS, INK, RED, WEB, big_web, spider_shape  # noqa: E402

QUERY = """query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{
totalContributions weeks{contributionDays{date contributionCount contributionLevel weekday}}}}}}"""

LEVELS = {
    "NONE": "#16213D",
    "FIRST_QUARTILE": "#1F3FA8",
    "SECOND_QUARTILE": "#3D6BE0",
    "THIRD_QUARTILE": "#B72B37",
    "FOURTH_QUARTILE": RED,
}


def fetch(login, token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        cal = json.load(r)["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    return cal["totalContributions"], [w["contributionDays"] for w in cal["weeks"]]


def streaks(weeks):
    days = [d for w in weeks for d in w]
    longest = run = 0
    for d in days:
        run = run + 1 if d["contributionCount"] else 0
        longest = max(longest, run)
    # today may not have commits yet; the streak is still alive until tomorrow
    tail = days[:-1] if days and not days[-1]["contributionCount"] else days
    current = 0
    for d in reversed(tail):
        if not d["contributionCount"]:
            break
        current += 1
    best = max(days, key=lambda d: d["contributionCount"]) if days else {"contributionCount": 0}
    return longest, current, best["contributionCount"]


def render(total, weeks):
    W, H = 1400, 560
    cell, gap = 20, 4
    step = cell + gap
    gx, gy = (W - len(weeks) * step + gap) / 2, 176
    crawl, hold = 12.0, 3.0
    D = crawl + hold

    h = hold / D  # everything shows lit during the hold, then the spider re-spins it

    def t_at(col):
        return h + (col + 0.5) / len(weeks) * (1 - h - 0.02)

    # month labels
    labels, last, last_c = [], None, -9
    for c, w in enumerate(weeks):
        m = dt.date.fromisoformat(w[0]["date"]).strftime("%b").upper()
        if m != last and c < len(weeks) - 2 and c - last_c >= 3:
            last_c = c
            labels.append(f'<text class="c" x="{gx + c * step:.1f}" y="{gy - 14}" font-size="22" letter-spacing="1" fill="#8B949E">{m}</text>')
        last = m

    # cells, revealed column by column as the spider passes
    cols = []
    for c, w in enumerate(weeks):
        t = t_at(c)
        rects = "".join(
            f'<rect x="{gx + c * step:.1f}" y="{gy + d["weekday"] * step}" width="{cell}" height="{cell}" rx="4" '
            f'fill="{LEVELS[d["contributionLevel"]]}"/>'
            for d in w
        )
        cols.append(
            f'<g>{rects}<animate attributeName="opacity" values="1;1;.25;.25;1;1" '
            f'keyTimes="0;{h:.4f};{h + 0.005:.4f};{t:.4f};{t + 0.01:.4f};1" dur="{D}s" repeatCount="indefinite"/></g>'
        )

    # the spider's dragline: a wave through the grid that it spins as it goes
    x0, x1 = gx - 30, gx + len(weeks) * step + 10
    mid = gy + 3.5 * step - gap / 2
    pts = [(x0 + (x1 - x0) * i / 120, mid + 58 * math.sin(i / 120 * math.pi * 6)) for i in range(121)]
    path = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}" + "".join(f" L{x:.1f} {y:.1f}" for x, y in pts[1:])
    L = sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))
    c_end = 0.98
    trail = (
        f'<path d="{path}" stroke="#fff" stroke-width="2.5" fill="none" stroke-linecap="round" opacity=".85" '
        f'stroke-dasharray="{L:.0f} {L + 40:.0f}"><animate attributeName="stroke-dashoffset" values="{L + 20:.0f};{L + 20:.0f};0;0" '
        f'keyTimes="0;{h:.4f};{c_end:.4f};1" dur="{D}s" repeatCount="indefinite"/></path>'
    )
    spider = (
        f'<g opacity="0"><g transform="rotate(90) translate(-35 -40) scale(2.2)">{spider_shape(INK, 3.4)}</g>'
        f'<g transform="rotate(90) translate(-35 -40) scale(2.2)">{spider_shape(RED, 2)}</g>'
        f'<animateMotion dur="{D}s" repeatCount="indefinite" path="{path}" rotate="auto" '
        f'keyPoints="0;0;1;1" keyTimes="0;{h:.4f};{c_end:.4f};1" calcMode="linear"/>'
        f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{h - 0.01:.4f};{h:.4f};{c_end:.4f};1" '
        f'dur="{D}s" repeatCount="indefinite"/></g>'
    )

    longest, current, best = streaks(weeks)
    stats = [("TOTAL", f"{total:,} contributions"), ("LONGEST STREAK", f"{longest} days"),
             ("CURRENT STREAK", f"{current} days"), ("BEST DAY", f"{best} contributions")]
    sans = "font-family=\"'Segoe UI',Helvetica,Arial,sans-serif\""
    boxes = []
    bw, bgap = 300, 26
    bx0 = (W - 4 * bw - 3 * bgap) / 2
    for i, (label, value) in enumerate(stats):
        x, y = bx0 + i * (bw + bgap), 408
        rot = (-1.5, 1, -1, 1.5)[i]
        boxes.append(
            f'<g transform="rotate({rot} {x + bw / 2} {y + 50})">'
            f'<rect x="{x + 6}" y="{y + 6}" width="{bw}" height="100" fill="{BLUE}" stroke="{INK}" stroke-width="4"/>'
            f'<rect x="{x}" y="{y}" width="{bw}" height="100" fill="#FFE45C" stroke="{INK}" stroke-width="4"/>'
            f'<rect x="{x}" y="{y}" width="{bw}" height="38" fill="{RED}" stroke="{INK}" stroke-width="4"/>'
            f'<text class="c" x="{x + 14}" y="{y + 29}" font-size="26" letter-spacing="2" fill="#fff">{label}</text>'
            f'<text x="{x + 14}" y="{y + 80}" {sans} font-weight="800" font-size="27" fill="{INK}">{value}</text></g>'
        )

    legend = "".join(
        f'<rect x="{1180 + i * 26}" y="118" width="20" height="20" rx="4" fill="{c}"/>'
        for i, c in enumerate(LEVELS.values())
    )

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}"><defs>{FONT_CSS}'
        '<pattern id="gd" width="16" height="16" patternUnits="userSpaceOnUse">'
        f'<circle cx="8" cy="8" r="3" fill="{BLUE}"/></pattern>'
        '<linearGradient id="gf" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".45"/>'
        '<stop offset=".5" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        f'<mask id="gm"><rect width="{W}" height="{H}" fill="url(#gf)"/></mask>'
        f'<clipPath id="gp"><rect x="6" y="6" width="{W - 12}" height="{H - 12}" rx="22"/></clipPath></defs>'
        f'<rect x="6" y="6" width="{W - 12}" height="{H - 12}" rx="22" fill="#0E1526"/>'
        f'<g clip-path="url(#gp)"><rect width="{W}" height="{H}" fill="url(#gd)" mask="url(#gm)"/>'
        f'<g stroke="{WEB}" stroke-width="1.5" fill="none" opacity=".35">{big_web(W - 6, H - 6, 260, 180, 270, 4, 6)}</g></g>'
        f'<rect x="6" y="6" width="{W - 12}" height="{H - 12}" rx="22" fill="none" stroke="{RED}" stroke-width="6"/>'
        f'<text class="c" x="{gx + 6:.1f}" y="106" font-size="72" fill="{BLUE}" stroke="{INK}" stroke-width="8" '
        f'stroke-linejoin="round" paint-order="stroke">SPIDER-SENSE ACTIVITY</text>'
        f'<text class="c" x="{gx:.1f}" y="100" font-size="72" fill="{RED}" stroke="{INK}" stroke-width="8" '
        f'stroke-linejoin="round" paint-order="stroke">SPIDER-SENSE ACTIVITY</text>'
        f'<text class="c" x="1172" y="136" text-anchor="end" font-size="22" letter-spacing="1" fill="#8B949E">LESS</text>'
        f'{legend}<text class="c" x="1316" y="136" font-size="22" letter-spacing="1" fill="#8B949E">MORE</text>'
        f'{"".join(labels)}{"".join(cols)}{trail}{spider}{"".join(boxes)}</svg>'
    )


if __name__ == "__main__":
    login = sys.argv[1] if len(sys.argv) > 1 else "Aayushvz"
    out = Path(sys.argv[2] if len(sys.argv) > 2 else "dist")
    out.mkdir(parents=True, exist_ok=True)
    total, weeks = fetch(login, os.environ["GITHUB_TOKEN"])
    (out / "spider-contribution-graph.svg").write_text(render(total, weeks), encoding="utf-8")
    print(f"{total} contributions, {len(weeks)} weeks")
