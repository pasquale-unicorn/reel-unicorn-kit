#!/usr/bin/env python3
"""Effetti sonori sintetizzati (niente diritti): whoosh, pop, tick-counter, ding, buzz, stamp, kaching, static, sting, click."""
import numpy as np, wave, os, sys
SR = 48000
OUT = sys.argv[1] if len(sys.argv) > 1 else "sfx"
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(7)
t_ = lambda d: np.arange(int(SR * d)) / SR
def env(n, a=0.005, r=0.2):
    e = np.ones(n); na = max(1, int(a * SR)); e[:na] = np.linspace(0, 1, na)
    nr = min(n, int(r * SR)); e[-nr:] *= np.exp(-np.linspace(0, 6, nr)); return e
def lp(x, k):  # passa basso semplice
    y = np.zeros_like(x); acc = 0.0
    for i, v in enumerate(x): acc += k * (v - acc); y[i] = acc
    return y
def save(name, x, gain=0.5):
    x = x / (np.max(np.abs(x)) + 1e-9) * gain
    st = np.stack([x, x], 1); data = (st * 32767).astype(np.int16)
    with wave.open(os.path.join(OUT, name + ".wav"), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(data.tobytes())
def whoosh(d=0.45):
    n = int(SR * d); x = rng.standard_normal(n); k = np.linspace(0.02, 0.35, n) ** 1.5
    y = np.zeros(n); acc = 0.0
    for i in range(n): acc += k[i] * (x[i] - acc); y[i] = acc
    return y * np.sin(np.linspace(0, np.pi, n)) ** 2
def pop():
    t = t_(0.12); f = 900 * np.exp(-t * 30) + 300
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), 0.002, 0.1)
def click():
    t = t_(0.03); return np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 200)
def counter(d=0.9, n=16):
    out = np.zeros(int(SR * d)); c = click()
    for i in range(n):
        p = int(i / n * (len(out) - len(c))); out[p:p + len(c)] += c * (0.6 + 0.4 * i / n)
    return out
def ding():
    t = t_(1.2); x = sum(a * np.sin(2 * np.pi * f * t) for f, a in ((1320, 1), (2640, .5), (3960, .25), (1980, .3)))
    return x * np.exp(-t * 4) * env(len(t), 0.002, 0.3)
def buzz():
    t = t_(0.45); x = np.sign(np.sin(2 * np.pi * 110 * t)) + 0.5 * np.sign(np.sin(2 * np.pi * 116 * t))
    return lp(x, 0.25) * env(len(t), 0.005, 0.08)
def stamp():
    t = t_(0.35); low = np.sin(2 * np.pi * (70 + 60 * np.exp(-t * 25)) * t) * np.exp(-t * 12)
    nz = rng.standard_normal(len(t)) * np.exp(-t * 40) * 0.6
    return low + lp(nz, 0.3)
def kaching():
    a = stamp()[: int(SR * .08)] * 0.4; d = ding(); out = np.zeros(int(SR * 1.3))
    out[:len(a)] += a; out[int(SR * .07):int(SR * .07) + len(d)] += d[: len(out) - int(SR * .07)]
    t = t_(0.9); bell2 = np.sin(2 * np.pi * 2093 * t) * np.exp(-t * 5)
    out[int(SR * .16):int(SR * .16) + len(t)] += 0.7 * bell2[: len(out) - int(SR * .16)]
    return out
def static():
    t = t_(0.35); return lp(rng.standard_normal(len(t)), 0.6) * env(len(t), 0.003, 0.1)
def sting():
    out = np.zeros(int(SR * .7))
    for k, f in enumerate((880, 1175)):
        t = t_(0.28); s = np.sin(2 * np.pi * f * t) * env(len(t), 0.004, 0.2); p = int(k * .25 * SR); out[p:p + len(t)] += s
    return out

def riser(d=1.2):
    t = t_(d); f = 120 * (2 ** (t / d * 3)); x = np.sin(2 * np.pi * np.cumsum(f) / SR)
    nz = lp(rng.standard_normal(len(t)), 0.15) * np.linspace(0, 1, len(t)) ** 2
    return (x * 0.5 + nz) * np.linspace(0.05, 1, len(t)) ** 1.5
def impact():
    t = t_(1.0); sub = np.sin(2 * np.pi * (45 + 80 * np.exp(-t * 18)) * t) * np.exp(-t * 4)
    nz = lp(rng.standard_normal(len(t)), 0.5) * np.exp(-t * 30)
    return sub + nz * 0.8
def swish(d=0.25):
    n = int(SR * d); x = rng.standard_normal(n); y = lp(x, 0.5) - lp(x, 0.1)
    return y * np.sin(np.linspace(0, np.pi, n)) ** 1.5
def typewriter(n=8, gap=0.07):
    out = np.zeros(int(SR * (n * gap + 0.1)))
    for i in range(n):
        t = t_(0.04); c = (np.sin(2 * np.pi * 1800 * t) + 0.5 * rng.standard_normal(len(t))) * np.exp(-t * 120)
        p = int(i * gap * SR); out[p:p + len(c)] += c
    return out

for name, fn, g in (("riser", riser, .4), ("impact", impact, .7), ("swish", swish, .4), ("typewriter", typewriter, .3),
                    ("whoosh", whoosh, .45), ("pop", pop, .5), ("click", click, .35), ("counter", counter, .35),
                    ("ding", ding, .45), ("buzz", buzz, .4), ("stamp", stamp, .6), ("kaching", kaching, .5),
                    ("static", static, .25), ("sting", sting, .35)):
    save(name, fn(), g)
print("ok", sorted(os.listdir(OUT)))
