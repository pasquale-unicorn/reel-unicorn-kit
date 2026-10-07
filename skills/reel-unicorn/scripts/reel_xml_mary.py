#!/usr/bin/env python3
"""Sequenza Premiere 9:16 EDITABILE in STILE MARY (ricavato dai suoi progetti, vedi analisi_mary/REPORT-*.md).

Grammatica Mary:
- ritmo: clip 1-5 s (mediana ~2,4), pause tagliate, nessun taglio > 3,5 s senza uno stacco di scala
- hook anticipato: la frase più forte all'inizio, poi il reel riparte in ordine cronologico (la frase si ripete al suo posto)
- inquadratura "split": V2 formatore a scala alta (piano americano, bordo basso del sorgente a ~1690 px), V1 stessa sorgente
  a scala maggiore che riempie la fascia bassa con la platea. Nessun keyframe: punch-in STATICI alternati al taglio
- una sola transizione video dopo l'hook (da aggiungere via MCP: Whip), tutti gli altri tagli secchi
- testo: solo sottotitoli nativi a frase (4-7 parole, ~1,5 s), Montserrat Bold, nessun titolo/callout
- audio: voce +8 dB, musica a -26 dB fissa, riser che culmina sul taglio dell'hook, whoosh sul taglio
- colore: Lumetri fisso (Temp -11, Tinta +8, Contrasto +29, Luci +68) -> NON passa in XML, Mary lo applica col suo preset

Uso: python3 reel_xml_mary.py scheda.json [cartella_output]
"""
import json, os, re, sys, uuid, wave
import reel_xml2 as R

FPS, SW, SH, SRC_W, SRC_H = R.FPS, R.SW, R.SH, R.SRC_W, R.SRC_H
fr, url, esc, RATE = R.fr, R.url, R.esc, R.RATE
FONT_SUB = "Montserrat-Bold"
BAND = 230            # fascia bassa con la platea (px)
PUNCH = [1.0, 1.3]    # alternanza: base 177,78 / punch-in ~231 (Mary luglio-settembre: 213-276)
PUNCH_CLIMAX = 1.42   # una sola volta, sulla battuta finale (Mary: 274-363)


def db(x): return 10 ** (x / 20)

def level_filter(gain_lin, kf=None):
    """Volume clip (xmeml 'Audio Levels', lineare). kf = [(frame, lin), ...] opzionale."""
    k = "".join(f"<keyframe><when>{f}</when><value>{v:.4f}</value></keyframe>" for f, v in (kf or []))
    return (f'<filter><effect><name>Audio Levels</name><effectid>audiolevels</effectid><effectcategory>audiolevels</effectcategory>'
            f'<effecttype>audiolevels</effecttype><mediatype>audio</mediatype><parameter><parameterid>level</parameterid><name>Level</name>'
            f'<valuemin>0</valuemin><valuemax>3.98109</valuemax><value>{gain_lin:.4f}</value>{k}</parameter></effect></filter>')

def motion_static(scale, h, v):
    return (f'<filter><effect><name>Basic Motion</name><effectid>basic</effectid><effectcategory>motion</effectcategory><effecttype>motion</effecttype><mediatype>video</mediatype>'
            f'<parameter><parameterid>scale</parameterid><name>Scale</name><valuemin>0</valuemin><valuemax>1000</valuemax><value>{scale:.2f}</value></parameter>'
            f'<parameter><parameterid>center</parameterid><name>Center</name><value><horiz>{h:.4f}</horiz><vert>{v:.4f}</vert></value></parameter>'
            f'<parameter><parameterid>centerOffset</parameterid><name>Anchor Point</name><value><horiz>0</horiz><vert>0</vert></value></parameter></effect></filter>')


def main_layer(cx, cy, top, punch):
    """Formatore. Base: la riga sorgente `top` (sopra la testa) finisce a y=0 e il bordo basso del sorgente a SH-BAND.
    Punch-in: scala x punch tenendo FERMO il viso (cy), così la testa non esce."""
    s0 = (SH - BAND) / (SRC_H - top) * 100
    y_face = (cy - top) * s0 / 100                     # dove sta il viso nel frame (base)
    s = s0 * punch
    cy_clip = y_face - (cy - SRC_H / 2) * s / 100
    w_px = SRC_W * s / 100
    ox = max(-(w_px - SW) / 2, min((w_px - SW) / 2, (SRC_W / 2 - cx) * s / 100))
    return s, ox / SRC_W, (cy_clip - SH / 2) / SRC_H

def single_layer(fx, fy, punch, face_y_frac=0.30):
    """Mary (2 reel su 3): un solo livello, base 177,78 (altezza piena), punch-in statici.
    Il viso (fx, fy sorgente) va a x=centro, y=face_y_frac dell'altezza; clamp per non scoprire i bordi."""
    s = R.BASE * punch
    w_px, h_px = SRC_W * s / 100, SRC_H * s / 100
    ox = max(-(w_px - SW) / 2, min((w_px - SW) / 2, (SRC_W / 2 - fx) * s / 100))
    cy = SH * face_y_frac - (fy - SRC_H / 2) * s / 100
    cy = max(SH - h_px / 2, min(h_px / 2, cy))
    return s, ox / SRC_W, (cy - SH / 2) / SRC_H

def band_layer(cx_aud, cy_aud, scale=265.0):
    """Platea: stessa sorgente scalata, con il punto (cx_aud, cy_aud) al centro della fascia bassa."""
    s = scale
    cy_clip = (SH - BAND / 2) - (cy_aud - SRC_H / 2) * s / 100
    ox = (SRC_W / 2 - cx_aud) * s / 100
    w_px, h_px = SRC_W * s / 100, SRC_H * s / 100
    ox = max(-(w_px - SW) / 2, min((w_px - SW) / 2, ox))
    cy_clip = max(SH - h_px / 2, min(h_px / 2, cy_clip))
    return s, ox / SRC_W, (cy_clip - SH / 2) / SRC_H


def split_long(segs, winwords, maxlen, gap_soft):
    """Mary non tiene clip lunghe: spezza ogni segmento > maxlen su una pausa morbida o una punteggiatura,
    senza togliere nulla (stacco di scala = jump cut)."""
    words = sorted(w for _, ws in winwords for w in ws)
    out = []
    for sg in segs:
        cur = dict(sg)
        while cur["out"] - cur["in"] > maxlen:
            cands = [w for w in words if cur["in"] + 1.2 <= w[1] <= cur["in"] + maxlen]
            best = None
            for a, b in zip(cands, cands[1:]):
                score = (b[0] - a[1]) + (0.3 if re.search(r"[.?!,;:]$", a[2]) else 0)
                if best is None or score > best[0]: best = (score, a[1], b[0])
            if best is None: break
            cut_end, cut_next = best[1] + 0.04, best[2] - 0.02
            out.append(dict(cur, out=cut_end)); cur = dict(cur, **{"in": cut_next})
        out.append(cur)
    return out


def build(spec, out_dir):
    src, src_dur = spec["source"], int(round(spec["source_duration_s"] * FPS))
    winwords = R.load_words(spec)
    segs = R.fine_segments(spec, winwords)
    segs = split_long(segs, winwords, spec.get("max_clip", 3.5), 0.25)
    # hook anticipato: la frase forte in testa (poi resta anche al suo posto)
    hk = spec.get("hook_src")
    if hk:
        w = next(w for w in spec["windows"] if w["src_in"] <= hk[0] <= w["src_out"])
        segs = [{"in": hk[0], "out": hk[1], "cx": w["cx"], "cy": w["cy"], "label": "HOOK " + w.get("label", ""), "hook": True}] + segs
    for i, s in enumerate(segs): s["punch"] = PUNCH[i % 2]
    if len(segs) > 2: segs[-1]["punch"] = PUNCH_CLIMAX
    # viso per clip (= Auto Reframe statico di Mary)
    if spec.get("autoface"):
        import face_center
        for sg in segs:
            (fx, fy), n = face_center.center(spec["source"], sg["in"], sg["out"], (sg["cx"], sg["cy"]))
            sg["fx"], sg["fy"], sg["face_n"] = fx, fy, n
    tmap = R.TimeMap(segs)
    hook_end = fr(hk[1] - hk[0]) if hk else 0

    v_main, v_band, a1, a2, pos = [], [], [], [], 0
    SINGLE = spec.get("layout", "single") == "single"
    voice_gain = db(spec.get("voice_db", 8))
    for i, sg in enumerate(segs, 1):
        fi, fo = fr(sg["in"]), fr(sg["out"]); d = fo - fi
        top = sg.get("top", spec.get("head_top", 230))
        if spec.get("layout", "single") == "single":
            sm, hm, vm = single_layer(sg.get("fx", sg["cx"]), sg.get("fy", sg["cy"]), sg["punch"])
        else:
            sm, hm, vm = main_layer(sg["cx"], sg["cy"], top, sg["punch"])
        sb, hb, vb = band_layer(spec.get("aud_cx", 960), spec.get("aud_cy", 980), spec.get("band_scale", 265))
        common = (f'<name>{esc(sg["label"])}</name><enabled>TRUE</enabled><duration>{src_dur}</duration>{RATE}'
                  f'<start>{pos}</start><end>{pos + d}</end><in>{fi}</in><out>{fo}</out>')
        v_band.append(f'<clipitem id="cb{i}-v">{common}{R.src_file(src, src_dur, i == 1 and not SINGLE)}<sourcetrack><mediatype>video</mediatype><trackindex>1</trackindex></sourcetrack>{motion_static(sb, hb, vb)}</clipitem>')
        v_main.append(f'<clipitem id="cl{i}-v">{common}{R.src_file(src, src_dur, i == 1 and SINGLE)}<sourcetrack><mediatype>video</mediatype><trackindex>1</trackindex></sourcetrack>{motion_static(sm, hm, vm)}{R.links(i)}</clipitem>')
        for k, lst in ((1, a1), (2, a2)):
            lst.append(f'<clipitem id="cl{i}-a{k}" premiereChannelType="mono">{common}{R.src_file(src, src_dur, False)}'
                       f'<sourcetrack><mediatype>audio</mediatype><trackindex>{k}</trackindex></sourcetrack>{level_filter(voice_gain)}{R.links(i)}</clipitem>')
        pos += d

    # sottotitoli a frase (4-7 parole), saltando l'hook anticipato se la frase è già chiara? no: Mary li mette anche lì
    subs = ""
    spec2 = dict(spec); spec2["sub_words"] = spec.get("sub_words", 6)
    cues = R.subtitle_cues(winwords, tmap, spec2)
    if hk:   # cue dentro l'hook anticipato (tempo reel 0..hook_end) ricavate dalle parole della finestra hook
        hcues = [(a - hk[0], b - hk[0], t) for a, b, t in R.subtitle_cues(winwords, R.TimeMap([{"in": hk[0], "out": hk[1]}]), spec2)
                 if hk[0] <= a < hk[1]]
    k = 0
    def wrap2(t, maxc=22):
        """Mary: 1-2 righe con a capo manuale. Spezza al centro se supera maxc caratteri."""
        if len(t) <= maxc: return t
        ws = t.split(); best, bd = None, 1e9
        for i in range(1, len(ws)):
            a, b = " ".join(ws[:i]), " ".join(ws[i:]); d = abs(len(a) - len(b))
            if max(len(a), len(b)) <= maxc + 4 and d < bd: best, bd = a + "\r" + b, d
        return best or t
    def add_sub(fa, fb, t):
        nonlocal subs, k
        return R.graphic(f"sub{k}", t, fa, max(fb, fa + 3), R.text_data(wrap2(t, spec.get("sub_maxc", 22)), spec.get("sub_size", 62), FONT_SUB, stroke_w=7),
                         spec.get("sub_y", 0.80), [(0, 100)])
    if hk:
        pass
    for a, b, t in sorted(cues, key=lambda c: tmap.reel(c[0])):   # Premiere vuole le clip in ordine di tempo
        subs += add_sub(fr(tmap.reel(a)), fr(tmap.reel(b)), t); k += 1

    # audio extra: musica fissa, riser che culmina sul taglio dell'hook, whoosh sul taglio
    def afile(fid, path, d):
        return (f'<file id="{fid}"><name>{esc(os.path.basename(path))}</name><pathurl>{url(path)}</pathurl>{RATE}<duration>{d}</duration>'
                f'<media><audio><samplecharacteristics><depth>16</depth><samplerate>48000</samplerate></samplecharacteristics><channelcount>2</channelcount></audio></media></file>')
    def wdur(p):
        with wave.open(p) as w: return int(round(w.getnframes() / w.getframerate() * FPS))
    music = ""
    if spec.get("music"):
        p = spec["music"]; d = min(wdur(p), pos)
        music = (f'<clipitem id="mus" premiereChannelType="stereo"><name>MUSICA</name><enabled>TRUE</enabled><duration>{wdur(p)}</duration>{RATE}'
                 f'<start>{hook_end}</start><end>{hook_end + d}</end><in>0</in><out>{d}</out>{afile("f-mus", p, wdur(p))}'
                 f'<sourcetrack><mediatype>audio</mediatype><trackindex>1</trackindex></sourcetrack>'
                 f'{level_filter(db(spec.get("music_db", -26)), [(0, 0.0), (6, db(spec.get("music_db", -26))), (d - 24, db(spec.get("music_db", -26))), (d, 0.0)])}</clipitem>')
    sfx = ""
    if spec.get("riser") and hk:
        p = spec["riser"]; d = wdur(p); a = max(0, hook_end - d)
        g = db(spec.get("riser_db", -20))
        sfx += (f'<clipitem id="riser" premiereChannelType="stereo"><name>RISER</name><enabled>TRUE</enabled><duration>{d}</duration>{RATE}'
                f'<start>{a}</start><end>{a + d}</end><in>0</in><out>{d}</out>{afile("f-riser", p, d)}'
                f'<sourcetrack><mediatype>audio</mediatype><trackindex>1</trackindex></sourcetrack>{level_filter(g, [(0, 0.0), (d, g)])}</clipitem>')
    if spec.get("whoosh") and hk:
        p = spec["whoosh"]; d = wdur(p); a = max(0, hook_end - 2)
        sfx += (f'<clipitem id="whoosh" premiereChannelType="stereo"><name>WHOOSH</name><enabled>TRUE</enabled><duration>{d}</duration>{RATE}'
                f'<start>{a}</start><end>{a + d}</end><in>0</in><out>{d}</out>{afile("f-whoosh", p, d)}'
                f'<sourcetrack><mediatype>audio</mediatype><trackindex>1</trackindex></sourcetrack>{level_filter(db(spec.get("whoosh_db", -14)))}</clipitem>')

    trk = lambda c: f"<track>{c}<enabled>TRUE</enabled><locked>FALSE</locked></track>"
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xmeml>
<xmeml version="4">
<sequence id="seq-1">
<uuid>{uuid.uuid4()}</uuid>
<duration>{pos}</duration>{RATE}
<name>{esc(spec["name"])}</name>
<media>
<video>
<format><samplecharacteristics>{RATE}<width>{SW}</width><height>{SH}</height><anamorphic>FALSE</anamorphic><pixelaspectratio>square</pixelaspectratio><fielddominance>none</fielddominance></samplecharacteristics></format>
{"" if SINGLE else trk("".join(v_band))}
{trk("".join(v_main))}
{trk(subs)}
</video>
<audio>
<numOutputChannels>2</numOutputChannels>
<format><samplecharacteristics><depth>16</depth><samplerate>48000</samplerate></samplecharacteristics></format>
<track currentExplodedTrackIndex="0" premiereTrackType="Stereo">{"".join(a1)}<enabled>TRUE</enabled><locked>FALSE</locked></track>
<track currentExplodedTrackIndex="1" premiereTrackType="Stereo">{"".join(a2)}<enabled>TRUE</enabled><locked>FALSE</locked></track>
<track premiereTrackType="Stereo">{music}<enabled>TRUE</enabled><locked>FALSE</locked></track>
<track premiereTrackType="Stereo">{sfx}<enabled>TRUE</enabled><locked>FALSE</locked></track>
</audio>
</media>
</sequence>
</xmeml>
'''
    out = os.path.join(out_dir, f'{spec["name"]}.xml')
    open(out, "w", encoding="utf-8").write(xml)
    lens = sorted(s["out"] - s["in"] for s in segs)
    print(out, f"{pos / FPS:.1f}s, {len(segs)} clip, mediana {lens[len(lens) // 2]:.2f}s, min {lens[0]:.2f} max {lens[-1]:.2f}, {len(cues)} sottotitoli")
    for s in segs: print(f"   {s['in']:8.2f} -> {s['out']:8.2f}  ({s['out']-s['in']:.2f}s) punch {s['punch']} viso {s.get('fx',0):.0f},{s.get('fy',0):.0f} ({s.get('face_n','-')}) {s['label']}")
    return out


if __name__ == "__main__":
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    build(spec, sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.abspath(sys.argv[1])))
