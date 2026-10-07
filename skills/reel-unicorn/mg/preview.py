#!/usr/bin/env python3
"""Anteprima: estrae fotogrammi dalle scene MOV (con trasparenza) e li compone su sfondo verde. uso: preview.py out.png scena:sec ..."""
import sys, subprocess, os, tempfile
from PIL import Image
out, items = sys.argv[1], sys.argv[2:]
here = os.path.dirname(os.path.abspath(__file__)); tmp = tempfile.mkdtemp(); ims = []
rend = os.environ.get("RENDERS", "renders"); crop = os.environ.get("CROP", "crop=1080:1100:0:500")
for k, it in enumerate(items):
    s, t = it.split(":"); p = os.path.join(tmp, f"{k}.png")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", t, "-i", os.path.join(here, rend, s + ".mov"), "-frames:v", "1",
                    "-vf", crop + ",scale=300:-1", p], check=True)
    ims.append(Image.open(p).convert("RGBA"))
c = Image.new("RGBA", (len(ims) * 310, ims[0].height), (70, 110, 70, 255))
for k, im in enumerate(ims): c.alpha_composite(im, (k * 310, 0))
c.convert("RGB").save(out); print(out)
