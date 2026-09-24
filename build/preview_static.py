"""Local QA: strip animations from SVGs and screenshot them at a given width.
Usage: python build/preview_static.py OUT.png WIDTH file1.svg [file2.svg ...]
"""
import re
import subprocess
import sys
from pathlib import Path

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
out, width, files = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
tmp = Path(__file__).parent / "_static"
tmp.mkdir(exist_ok=True)
imgs = []
for f in files:
    s = Path(f).read_text(encoding="utf-8")
    s = re.sub(r"<animate(Transform|Motion)?[^>]*/>", "", s)
    s = s.replace('<g opacity="0">', "<g>").replace('opacity="0" d=', "d=")
    name = Path(f).name
    (tmp / name).write_text(s, encoding="utf-8")
    imgs.append(f'<img src="{name}" style="width:{width}px;display:block;margin:0 0 12px">')
(tmp / "index.html").write_text(
    f'<html><body style="margin:0;padding:16px;background:#0d1117">{"".join(imgs)}</body></html>', encoding="utf-8"
)
height = 4000
subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={width + 32},{height}",
                f"--screenshot={Path(out).resolve()}", (tmp / "index.html").resolve().as_uri()],
               capture_output=True)
print(out)
