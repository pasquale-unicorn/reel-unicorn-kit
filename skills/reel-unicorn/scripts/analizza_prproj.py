#!/usr/bin/env python3
"""Legge un progetto Premiere (.prproj, gzip o XML) e misura COME è montato ogni reel 9:16:
ritmo dei tagli, scale/punch-in, keyframe, sottotitoli/testi, effetti, transizioni, audio.
Serve al ciclo di apprendimento: Mary finisce un reel -> questo script -> confronto con references/stile-mary.md.

Uso: python3 analizza_prproj.py progetto.prproj [--json out.json]
Stampa un riepilogo leggibile per ogni sequenza verticale (o tutte con --tutte).
"""
import gzip, json, re, statistics as st, sys, base64
import xml.etree.ElementTree as ET

TICKS = 254016000000


def load(path):
    raw = open(path, "rb").read()
    if raw[:2] == b"\x1f\x8b": raw = gzip.decompress(raw)
    return ET.fromstring(raw)


class Proj:
    def __init__(self, root):
        self.root, self.by = root, {}
        for el in root.iter():
            k = el.get("ObjectID") or el.get("ObjectUID")
            if k: self.by[k] = el

    def ref(self, el):
        if el is None: return None
        k = el.get("ObjectRef") or el.get("ObjectURef")
        return self.by.get(k) if k else None

    def child_ref(self, el, path):
        return self.ref(el.find(path)) if el is not None else None


def num(el, tag, default=0):
    t = el.findtext(tag) if el is not None else None
    try: return int(t)
    except (TypeError, ValueError): return default


def component_info(P, cti):
    """MatchName + parametri interessanti (scala, posizione, keyframe, testo) dei componenti di un track item
    (i componenti stanno in ClipTrackItem/ComponentOwner/Components, non sulla Clip)."""
    out = []
    chain = P.child_ref(cti, "ClipTrackItem/ComponentOwner/Components") if cti is not None else None
    comps = chain.find("ComponentChain/Components") if chain is not None else None
    if comps is None: return out
    for c in comps.findall("Component"):
        comp = P.ref(c)
        if comp is None: continue
        mn = comp.findtext(".//MatchName") or comp.tag
        info = {"match": mn, "params": {}}
        params = comp.find(".//Params")
        if params is not None:
            for p in params.findall("Param"):
                pp = P.ref(p)
                if pp is None: continue
                name = pp.findtext(".//Name") or ""
                tv = pp.findtext(".//IsTimeVarying") == "true"
                kfs = [k.text for k in pp.iter("StartKeyframe") if k.text] if tv else []
                cur = pp.findtext(".//CurrentValue")
                if name in ("Scale", "Scala", "Position", "Posizione", "Reframe Scale", "Scala reframe", "Level", "Livello", "Gain", "Guadagno"):
                    info["params"][name] = {"cur": cur, "kf": len(kfs), "kf_vals": [k.split(",")[1] if "," in k else k for k in kfs[:8]]}
                if mn == "AE.ADBE Text":
                    for blob in pp.iter():
                        txt = (blob.text or "").strip()
                        if len(txt) > 40 and re.fullmatch(r"[A-Za-z0-9+/=\s]+", txt):
                            try:
                                d = base64.b64decode(txt)[8:].decode("utf-16-le", errors="ignore")
                                m = re.search(r'"mText"\s*:\s*"((?:[^"\\]|\\.)*)"', d); f = re.search(r'"mFontName".*?\[\[0,\s*"([^"]+)"', d)
                                if m: info["text"] = json.loads('"' + m.group(1) + '"'); info["font"] = f.group(1) if f else None
                            except Exception: pass
        out.append(info)
    return out


def track_items(P, track):
    ct = track.find("ClipTrack") if track is not None else None
    if ct is None:
        for child in track or []:
            if child.find("ClipTrack") is not None: ct = child.find("ClipTrack"); break
    items = ct.find("ClipItems/TrackItems") if ct is not None else None
    trans = ct.find("TransitionItems/TrackItems") if ct is not None else None
    return ([P.ref(i) for i in items.findall("TrackItem")] if items is not None else [],
            [P.ref(i) for i in trans.findall("TrackItem")] if trans is not None else [])


def clip_of(P, cti):
    """-> (TrackItem con Start/End, SubClip con Name, Clip interna con InPoint/OutPoint)."""
    base = cti.find("ClipTrackItem") if cti is not None else None
    ti = base.find("TrackItem") if base is not None else (cti.find("TrackItem") if cti is not None else None)
    sub = P.child_ref(base if base is not None else cti, "SubClip")
    clipobj = P.child_ref(sub, "Clip") if sub is not None else None
    clip = clipobj.find("Clip") if clipobj is not None and clipobj.find("Clip") is not None else clipobj
    return ti, sub, clip


def analyze_sequence(P, seq):
    res = {"name": seq.findtext("Name"), "video": [], "audio": [], "transitions": 0, "transition_names": []}
    for tg in seq.iter("TrackGroup"):
        sec = tg.find("Second"); grp = P.ref(sec) if sec is not None else None
        if grp is None: continue
        kind = "video" if "Video" in grp.tag else "audio" if "Audio" in grp.tag else None
        if kind is None: continue
        if kind == "video":
            fr = grp.find(".//FrameRect")
            if fr is not None and fr.text:
                v = [int(x) for x in re.findall(r"-?\d+", fr.text)][-2:]
                res["size"] = v
        tracks = grp.find("TrackGroup/Tracks")
        if tracks is None: continue
        for ti_idx, tr in enumerate(tracks.findall("Track")):
            track = P.ref(tr)
            items, trans = track_items(P, track)
            res["transitions"] += len([t for t in trans if t is not None])
            for t in trans:
                if t is None: continue
                comp = t.find(".//MatchName")
                if comp is not None: res["transition_names"].append(comp.text)
            for cti in items:
                if cti is None: continue
                ti, sub, clip = clip_of(P, cti)
                s, e = num(ti, "Start") / TICKS, num(ti, "End") / TICKS
                if e <= s: continue
                ip, op = num(clip, "InPoint") / TICKS, num(clip, "OutPoint") / TICKS
                name = (sub.findtext("Name") if sub is not None else None) or cti.tag
                row = {"track": ti_idx + 1, "start": round(s, 3), "end": round(e, 3), "dur": round(e - s, 3),
                       "src_in": round(ip, 3), "src_out": round(op, 3), "name": name,
                       "auto_reframe": (ti.findtext(".//BE.Intrinsics.AutoReframe.V2") == "true") if ti is not None else False,
                       "components": component_info(P, cti)}
                res[kind].append(row)
    return res


def summarize(r):
    v = [c for c in r["video"] if not any(x["match"] in ("AE.ADBE Text", "AE.ADBE Capsule") or x.get("text") for x in c["components"])
         and "Graphic" not in c["name"] and not c["name"].lower().endswith((".png", ".jpg", ".mov"))]
    texts = [x for c in r["video"] for x in c["components"] if x.get("text") and "misterhorse" not in x["text"].lower() and "Mister Horse" not in x["text"]]
    # traccia principale = quella con più clip "da montaggio" (< 10 s): esclude fondi, platea, letti lunghi
    main_track = max(set(c["track"] for c in v), key=lambda t: (sum(1 for c in v if c["track"] == t and c["dur"] < 10),
                                                                 -max(c["dur"] for c in v if c["track"] == t))) if v else None
    mv = sorted([c for c in v if c["track"] == main_track], key=lambda c: c["start"])
    # tieni solo il blocco montato contiguo che parte dall'inizio (Mary lascia spezzoni di lavoro oltre la fine)
    keep, end = [], 0.0
    for c in mv:
        if c["start"] > end + 3 and keep: break
        if c["dur"] > 20 and keep: break
        keep.append(c); end = max(end, c["end"])
    mv = keep or mv
    durs = [c["dur"] for c in mv]
    total = max([c["end"] for c in mv] or [0])
    jumps = [mv[i + 1]["src_in"] - mv[i]["src_out"] for i in range(len(mv) - 1)]
    scales = [x["params"].get("Scale", x["params"].get("Scala", {})).get("cur") for c in mv for x in c["components"] if x["match"] == "AE.ADBE Motion"]
    kf = sum(p.get("kf", 0) for c in mv for x in c["components"] for p in x["params"].values() if isinstance(p, dict) and x["match"] == "AE.ADBE Motion")
    reframe = sum(1 for c in mv if c.get("auto_reframe"))
    effects = {}
    for c in r["video"]:
        for x in c["components"]: effects[x["match"]] = effects.get(x["match"], 0) + 1
    words = [len(t["text"].split()) for t in texts]
    out = {
        "sequenza": r["name"], "dimensioni": r.get("size"), "durata_s": round(total, 2),
        "clip_traccia_principale": len(mv), "tagli_al_minuto": round(len(mv) / total * 60, 1) if total else None,
        "clip_mediana_s": round(st.median(durs), 2) if durs else None, "clip_min_s": round(min(durs), 2) if durs else None,
        "clip_max_s": round(max(durs), 2) if durs else None,
        "salti_sorgente_<1s": sum(1 for j in jumps if 0 <= j < 1), "salti_sorgente_grandi": sum(1 for j in jumps if j >= 1 or j < 0),
        "clip_ripetute": len(mv) - len({(round(c["src_in"], 1), round(c["src_out"], 1)) for c in mv}),
        "scale_motion": sorted({s for s in scales if s}), "keyframe_motion": kf, "clip_auto_reframe": reframe,
        "testi_grafici": len(texts), "nota_sottotitoli": "i sottotitoli nativi (caption track) sono binari: contali in Premiere", "parole_per_testo_mediana": st.median(words) if words else None,
        "font": sorted({t.get("font") for t in texts if t.get("font")}), "esempi_testo": [t["text"] for t in texts[:6]],
        "transizioni": r["transitions"], "nomi_transizioni": sorted(set(r["transition_names"]))[:10],
        "effetti_video": effects, "clip_audio": len(r["audio"]),
        "audio_nomi": sorted({c["name"] for c in r["audio"]})[:12],
    }
    return out


def main():
    path = sys.argv[1]; tutte = "--tutte" in sys.argv
    P = Proj(load(path)); outs = []
    for seq in P.root.iter("Sequence"):
        if seq.findtext("Name") is None or seq.find(".//TrackGroup") is None: continue
        r = analyze_sequence(P, seq)
        if not r["video"]: continue
        s = summarize(r)
        vertical = s["dimensioni"] and s["dimensioni"][1] > s["dimensioni"][0]
        if not tutte and s["dimensioni"] and not vertical: continue
        outs.append(s)
    for s in outs:
        print(f"\n=== {s['sequenza']}  {s['dimensioni']}  {s['durata_s']} s")
        for k, v in s.items():
            if k not in ("sequenza", "dimensioni", "durata_s"): print(f"  {k}: {v}")
    if "--json" in sys.argv:
        json.dump(outs, open(sys.argv[sys.argv.index("--json") + 1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
