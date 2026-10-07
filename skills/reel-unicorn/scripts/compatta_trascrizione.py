#!/usr/bin/env python3
"""Compatta una trascrizione lunga in blocchi da N secondi con timecode, per leggerla TUTTA senza saltare.
Formati: .md con righe *MM:SS* / *H:MM:SS* seguite dal testo, oppure .srt.
Uso: python3 compatta_trascrizione.py trascrizione.(md|srt) [secondi_blocco=20] > compatta.txt"""
import re, sys

def tosec(t):
    p = [float(x) for x in t.replace(",", ".").split(":")]
    while len(p) < 3: p.insert(0, 0.0)
    return p[0] * 3600 + p[1] * 60 + p[2]

TC = r"\[?\*?\(?(\d{1,2}:\d{2}(?::\d{2})?(?:[.,]\d+)?)\)?\*?\]?"
def parse_md(txt):
    """Righe '*MM:SS*' seguite dal testo, oppure '[00:01:02] testo' / '00:01:02 testo' sulla stessa riga."""
    out, cur = [], None
    for line in txt.splitlines():
        l = line.strip()
        m = re.match(r"^" + TC + r"\s*$", l)
        if m: cur = tosec(m.group(1)); continue
        m = re.match(r"^" + TC + r"\s*[-–:]?\s*(.+)$", l)
        if m and ":" in m.group(1): out.append((tosec(m.group(1)), m.group(2))); cur = tosec(m.group(1)); continue
        if cur is not None and l: out.append((cur, l))
    return out

def parse_srt(txt):
    out = []
    for blk in re.split(r"\n\s*\n", txt.strip()):
        ln = blk.strip().splitlines()
        tl = next((l for l in ln if "-->" in l), None)
        if not tl: continue
        i = ln.index(tl)
        out.append((tosec(tl.split("-->")[0].strip()), " ".join(ln[i + 1:]).strip()))
    return out

def hms(s): s = int(s); return f"{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}"

if __name__ == "__main__":
    path = sys.argv[1]; blk = float(sys.argv[2]) if len(sys.argv) > 2 else 20
    txt = open(path, encoding="utf-8", errors="ignore").read()
    rows = parse_srt(txt) if path.lower().endswith((".srt", ".vtt")) or "-->" in txt[:2000] else parse_md(txt)
    if not rows:
        sys.exit("ERRORE: nessun timecode riconosciuto. Formati: .srt/.vtt, righe '*MM:SS*', '[HH:MM:SS] testo'. Mostra a Claude le prime righe del file.")
    buckets = {}
    for t, w in rows: buckets.setdefault(int(t // blk), []).append(w)
    for k in sorted(buckets): print(f"[{hms(k * blk)}] {' '.join(buckets[k])}")
