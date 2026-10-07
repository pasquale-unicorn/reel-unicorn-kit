#!/usr/bin/env python3
"""'Auto Reframe' statico: per ogni clip trova il viso (OpenCV Haar frontale+profilo) su 3 fotogrammi e restituisce
il centro medio (cx, cy) in pixel sorgente. Fallback: valore di default. Uso da reel_xml_mary (spec["autoface"]=true)."""
import subprocess, tempfile, os, cv2, numpy as np
CASC = cv2.data.haarcascades
FRONT = cv2.CascadeClassifier(CASC + "haarcascade_frontalface_default.xml")
PROF = cv2.CascadeClassifier(CASC + "haarcascade_profileface.xml")

def grab(src, t, path):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", src, "-frames:v", "1", "-vf", "scale=960:-1", path], check=True)
    return cv2.imread(path)

def faces(img):
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    out = list(FRONT.detectMultiScale(g, 1.1, 5, minSize=(40, 40)))
    out += list(PROF.detectMultiScale(g, 1.1, 5, minSize=(40, 40)))
    out += [(img.shape[1] - x - w, y, w, h) for x, y, w, h in PROF.detectMultiScale(cv2.flip(g, 1), 1.1, 5, minSize=(40, 40))]
    return out

def center(src, t_in, t_out, default, min_w=50):
    tmp = tempfile.mkdtemp(); pts = []
    for t in (t_in + 0.25, (t_in + t_out) / 2, max(t_in + 0.25, t_out - 0.25)):
        try: img = grab(src, t, os.path.join(tmp, "f.jpg"))
        except Exception: continue
        if img is None: continue
        fs = [f for f in faces(img) if f[2] >= min_w]
        if fs:
            x, y, w, h = max(fs, key=lambda f: f[2] * f[3])
            pts.append(((x + w / 2) * 2, (y + h / 2) * 2))     # scala 960 -> 1920
    if not pts: return default, 0
    arr = np.array(pts); return (float(np.median(arr[:, 0])), float(np.median(arr[:, 1]))), len(pts)

if __name__ == "__main__":
    import sys
    print(center(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), (960, 400)))
