#!/usr/bin/env python3
"""Sequenza Premiere (xmeml) 9:16 EDITABILE, versione 2 "ritmo + takeover".

Tutti i tempi della scheda sono in SECONDI SORGENTE: il generatore taglia i silenzi (dalle parole whisper) e
converte da solo in tempo reel. Così overlay, effetti e takeover restano agganciati alle parole di Angelo.

V1  tagli fini dalla sorgente (silenzi rimossi), zoom alternato, keyframe Scala+Centro per i takeover (Angelo nella finestra PIP)
V2  motion graphics (MOV con trasparenza) + stinger sui tagli
V3  sottotitoli nativi (generati dalle parole whisper, max 3 parole, numeri in fucsia)
A1/A2 audio sorgente, A3 effetti sonori

Uso: python3 reel_xml2.py scheda.json [cartella_output]
"""
import json, os, re, sys, unicodedata, urllib.parse, uuid, wave
from base64 import b64encode
KIT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))  # cartella reel-unicorn-kit

FPS, SW, SH = 24, 1080, 1920
SRC_W, SRC_H = 1920, 1080
BASE = SH / SRC_H * 100
WHITE, BLACK, FUCSIA = 16777215.0, 0.0, 16056575.0
FONT_SUB = "Montserrat-Black"
# finestra PIP (deve coincidere con build_scenes2.py)
PIP_L, PIP_T, PIP_W, PIP_H = 41, 120, 998, 562
PIP_SCALE = 95.0                                    # Angelo grande nella finestra (il MOV copre il resto)
PIP_CY = PIP_T + PIP_H / 2                          # centro verticale finestra (401 px)
# UNITÀ CENTRO (calibrato 2026-10-06, 2 test): horiz/vert = frazione di LARGHEZZA/ALTEZZA NATIVE della clip (video 1920x1080, testi 1080x1920).
T_IN = 7                                            # frame di apertura/chiusura takeover

def fr(s): return int(round(s * FPS))
def url(p): return "file://localhost" + urllib.parse.quote(p)
def ascii_(t): return unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
def esc(t): return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
RATE = f"<rate><timebase>{FPS}</timebase><ntsc>FALSE</ntsc></rate>"


# ---------- parole e tagli ----------
def load_words(spec):
    """Parole whisper in tempo sorgente assoluto, per ogni finestra grezza."""
    out = []
    for w in spec["windows"]:
        j = json.load(open(w["whisper"], encoding="utf-8"))
        raw = [(w["src_in"] + x["start"], w["src_in"] + x["end"], x["word"].strip())
               for s in j["segments"] for x in s.get("words", [])]
        words = []
        for a, b, t in raw:   # whisper spezza "l 'affitto", "50 %", "12 .000", "-2007": riattacca al precedente
            if words and (t[:1] in "'%.,-" and not t.startswith("...")):
                pa, pb, pt = words[-1]; words[-1] = (pa, b, pt + t)
            else: words.append((a, b, t))
        fix = spec.get("glossary", {})
        words = [(a, b, fix.get(re.sub(r"[^\w']", "", t.lower()), None) and re.sub(re.escape(re.sub(r"[^\w']", "", t)), fix[re.sub(r"[^\w']", "", t.lower())], t) or t) for a, b, t in words]
        out.append((w, words))
    return out

def fine_segments(spec, winwords):
    """Spezza ogni finestra dove c'è una pausa > gap, con un po' di aria prima/dopo."""
    gap, pad = spec.get("gap", 0.45), spec.get("pad", 0.08)
    segs = []
    for w, words in winwords:
        if not words: continue
        runs, cur = [], [words[0]]
        for a, b in zip(words, words[1:]):
            if b[0] - a[1] > gap: runs.append(cur); cur = []
            cur.append(b)
        runs.append(cur)
        for k, r in enumerate(runs):
            s = w["src_in"] if k == 0 else max(w["src_in"], r[0][0] - pad)
            e = min(w["src_out"], r[-1][1] + pad)
            if e - s > 0.3: segs.append({"in": s, "out": e, "cx": w["cx"], "cy": w["cy"], "label": w.get("label", "")})
    # zoom alternato a ogni taglio (pattern interrupt)
    for i, s in enumerate(segs): s["zoom"] = 1.0 if i % 2 == 0 else 1.12
    return segs

class TimeMap:
    """tempo sorgente <-> tempo reel sui segmenti fini."""
    def __init__(self, segs):
        self.segs, pos = [], 0.0
        for s in segs:
            self.segs.append((s["in"], s["out"], pos)); pos += s["out"] - s["in"]
        self.total = pos
    def reel(self, src):
        for a, b, p in self.segs:
            if a <= src <= b: return p + src - a
        nxt = [(a, p) for a, b, p in self.segs if a > src]
        return nxt[0][1] if nxt else self.total   # dentro un silenzio tagliato: aggancia al taglio successivo
    def inside(self, src): return any(a <= src <= b for a, b, p in self.segs)
    def src_of_reel(self, r):
        for a, b, p in self.segs:
            if p <= r <= p + (b - a): return a + r - p
        a, b, p = self.segs[-1]; return b + (r - (p + b - a))   # oltre la fine: prosegue nella sorgente


# ---------- testo nativo Premiere ----------
def text_data(text, size, font, fill=WHITE, stroke_w=0.0):
    pv = lambda v: {"mParamValues": [[0.0 if isinstance(v, float) else 0, v]]}
    st = {"mAdditionalStrokeColor": [], "mAdditionalStrokeVisible": [], "mAdditionalStrokeWidth": [],
          "mBaselineOption": pv(0.0), "mBaselineShift": pv(0.0), "mCapsOption": pv(0.0), "mFauxBold": pv(False),
          "mFauxItalic": pv(False), "mFillColor": pv(fill), "mFillOverStroke": pv(False), "mFillVisible": pv(True),
          "mFontName": pv(font), "mFontSize": pv(float(size)), "mKerning": pv(0.0), "mStrokeColor": pv(BLACK),
          "mStrokeVisible": pv(stroke_w > 0), "mStrokeWidth": pv(float(stroke_w)), "mText": text, "mTracking": pv(0.0),
          "mTsumi": pv(0.0), "mUnderline": None}
    tp = {"mAlignment": 2.0, "mBackFillColor": 0.0, "mBackFillOpacity": 0.0, "mBackFillSize": 0.0, "mBackFillVisible": False,
          "mDefaultRun": [], "mHeight": 0.0, "mHindiDigits": False, "mIndic": False, "mIsMask": False, "mIsMaskInverted": False,
          "mIsVerticalText": False, "mLeading": 0.0, "mLigatures": False, "mLineCapType": 0.0, "mLineJoinType": 1.0,
          "mMiterLimit": 4.0, "mNumStrokes": 1.0, "mRTL": False, "mShadowAngle": 135.0, "mShadowBlur": 30.0, "mShadowColor": 0.0,
          "mShadowOffset": 6.0, "mShadowOpacity": 60.0, "mShadowSize": 0.0, "mShadowVisible": True, "mStyleSheet": st,
          "mTabWidth": 400.0, "mVerticalAlignment": 0.0, "mWidth": 0.0}
    s = json.dumps({"mShadowFontMapHash": None, "mTextParam": tp, "mUseLegacyTextBox": False, "mVersion": 1.0}, ensure_ascii=False)
    return b64encode(b"\x0f\x0f\x00\x00\x00\x00\x00\x00" + s.encode("utf-16-le")).decode()

def pop_motion(dur, y, keys):
    dy = y - 0.5   # clip grafica 1080x1920: unità = altezza clip
    kf = "".join(f"<keyframe><when>{min(f, dur)}</when><value>{v}</value></keyframe>" for f, v in keys)
    return (f'<filter><effect><name>Basic Motion</name><effectid>basic</effectid><effectcategory>motion</effectcategory>'
            f'<effecttype>motion</effecttype><mediatype>video</mediatype>'
            f'<parameter><parameterid>scale</parameterid><name>Scale</name><valuemin>0</valuemin><valuemax>1000</valuemax><value>100</value>{kf}</parameter>'
            f'<parameter><parameterid>center</parameterid><name>Center</name><value><horiz>0</horiz><vert>{dy:.4f}</vert></value></parameter>'
            f'<parameter><parameterid>centerOffset</parameterid><name>Anchor Point</name><value><horiz>0</horiz><vert>0</vert></value></parameter>'
            f'</effect></filter>')

def graphic(cid, label, a, b, data, y, keys):
    lab = esc(ascii_(label)[:40])
    return (f'<clipitem id="{cid}"><masterclipid>m-{cid}</masterclipid><name>{lab}</name><enabled>TRUE</enabled>{RATE}'
            f'<start>{a}</start><end>{b}</end><in>0</in><out>{b - a}</out><alphatype>none</alphatype>'
            f'<pixelaspectratio>square</pixelaspectratio><anamorphic>FALSE</anamorphic>'
            f'<file id="f-{cid}"><name>Graphic</name><mediaSource>GraphicAndType</mediaSource><media><video><samplecharacteristics>'
            f'<width>{SW}</width><height>{SH}</height><anamorphic>FALSE</anamorphic><pixelaspectratio>square</pixelaspectratio>'
            f'<fielddominance>none</fielddominance></samplecharacteristics></video></media></file>'
            f'<filter><effect><name>{lab}</name><effectid>GraphicAndType</effectid><effectcategory>graphic</effectcategory>'
            f'<effecttype>filter</effecttype><pproBypass>false</pproBypass>'
            f'<parameter authoringApp="PremierePro"><parameterid>1</parameterid><name>Source Text</name><value>{data}</value></parameter>'
            f'<parameter authoringApp="PremierePro"><parameterid>3</parameterid><name>Position</name><IsTimeVarying>false</IsTimeVarying>'
            f'<value>0,0.5:0.5,0,0,0,0,0,0,0,0,0,0,0,0</value></parameter></effect></filter>'
            f'{pop_motion(b - a, y, keys)}</clipitem>')


# ---------- sorgente + takeover ----------
def src_file(src, dur, full):
    if not full: return '<file id="file-src"/>'
    return (f'<file id="file-src"><name>{esc(os.path.basename(src))}</name><pathurl>{url(src)}</pathurl>{RATE}<duration>{dur}</duration>'
            f'<media><video><samplecharacteristics>{RATE}<width>{SRC_W}</width><height>{SRC_H}</height></samplecharacteristics></video>'
            f'<audio><samplecharacteristics><depth>16</depth><samplerate>48000</samplerate></samplecharacteristics><channelcount>2</channelcount></audio></media></file>')

def links(i):
    return "".join(f'<link><linkclipref>cl{i}-{k}</linkclipref><mediatype>{mt}</mediatype><trackindex>{ti}</trackindex><clipindex>{i}</clipindex>{g}</link>'
                   for k, mt, ti, g in (("v", "video", 1, ""), ("a1", "audio", 1, "<groupindex>1</groupindex>"), ("a2", "audio", 2, "<groupindex>1</groupindex>")))

def framing(cx, cy, z):
    s = BASE * z; w, h = SRC_W * s / 100, SRC_H * s / 100
    dx = max(-(w - SW) / 2, min((w - SW) / 2, (SRC_W / 2 - cx) * s / 100))
    dy = max(-(h - SH) / 2, min((h - SH) / 2, (SRC_H / 2 - cy) * s / 100))
    return s, dx / SRC_W, dy / SRC_H

def pip_target(cx, cy):
    """scala e centro per mettere Angelo (cx,cy sorgente) al centro della finestra PIP, coprendola tutta."""
    s = PIP_SCALE / 100; hw, hh = SRC_W * s / 2, SRC_H * s / 2
    ox = max(-(hw - PIP_W / 2) - (PIP_L + PIP_W / 2 - SW / 2), min(hw - PIP_W / 2 - (PIP_L + PIP_W / 2 - SW / 2), (SRC_W / 2 - cx) * s)) + (PIP_L + PIP_W / 2 - SW / 2)
    cyc = PIP_CY + (SRC_H / 2 - cy) * s                     # centro clip desiderato
    cyc = max(PIP_T + PIP_H - hh, min(PIP_T + hh, cyc))     # la clip deve coprire la finestra
    return PIP_SCALE, ox / SRC_W, (cyc - SH / 2) / SRC_H

def motion_kf(fi, fo, base, takeovers, push, pip):
    """Keyframe Scala e Centro (in frame sorgente). base=(scala,h,v). takeovers: [(src_start, src_end)] in frame sorgente.
    Dentro un takeover la clip va alla finestra PIP in T_IN frame e torna in T_IN frame."""
    s0, h0, v0 = base; s1 = s0 + BASE * push       # zoom lento (push) fuori dai takeover
    def val(f):
        for a, b in takeovers:
            if a <= f <= b:
                t = 1.0
                if f < a + T_IN: t = (f - a) / T_IN
                elif f > b - T_IN: t = (b - f) / T_IN
                base_s = s0 + (s1 - s0) * (f - fi) / max(1, fo - fi)
                ps, ph, pv = pip
                return base_s + (ps - base_s) * t, h0 + (ph - h0) * t, v0 + (pv - v0) * t
        base_s = s0 + (s1 - s0) * (f - fi) / max(1, fo - fi)
        return base_s, h0, v0
    pts = {fi, fo}
    for a, b in takeovers:
        for f in (a, a + T_IN, b - T_IN, b):
            if fi <= f <= fo: pts.add(f)
    pts = sorted(pts)
    ks = "".join(f"<keyframe><when>{f}</when><value>{val(f)[0]:.2f}</value></keyframe>" for f in pts)
    kc = "".join(f"<keyframe><when>{f}</when><value><horiz>{val(f)[1]:.4f}</horiz><vert>{val(f)[2]:.4f}</vert></value></keyframe>" for f in pts)
    return (f'<filter><effect><name>Basic Motion</name><effectid>basic</effectid><effectcategory>motion</effectcategory><effecttype>motion</effecttype><mediatype>video</mediatype>'
            f'<parameter><parameterid>scale</parameterid><name>Scale</name><valuemin>0</valuemin><valuemax>1000</valuemax><value>{s0:.2f}</value>{ks}</parameter>'
            f'<parameter><parameterid>center</parameterid><name>Center</name><value><horiz>{h0:.4f}</horiz><vert>{v0:.4f}</vert></value>{kc}</parameter>'
            f'<parameter><parameterid>centerOffset</parameterid><name>Anchor Point</name><value><horiz>0</horiz><vert>0</vert></value></parameter>'
            f'</effect></filter>')


# ---------- sottotitoli dalle parole ----------
FUNC = {"il","lo","la","i","gli","le","l","un","uno","una","di","a","da","in","con","su","per","tra","fra","e","o","che","del","della","al","alla","nel","nella","ma","se","non","è","ti","mi","si","ci","alle","agli","dei","delle","degli","nei","sui"}
def is_key(t): return bool(re.search(r"\d", t))
def subtitle_cues(winwords, tmap, spec):
    cues, cur = [], []
    maxw, gap = spec.get("sub_words", 3), 0.45
    def flush():
        if cur:
            t = " ".join(w[2] for w in cur).upper()
            t = re.sub(r"\s+([,.;:!?])", r"\1", t); t = re.sub(r"[,.;:]+$", "", t)
            t = t.replace(" '", "'").replace("' ", "'")
            for k_, v_ in spec.get("text_fix", {}).items(): t = t.replace(k_, v_)
            cues.append((cur[0][0], cur[-1][1], t)); cur.clear()
    for w, words in winwords:
        for k, wd in enumerate(words):
            if not tmap.inside(wd[0]): flush(); continue
            if cur and (wd[0] - cur[-1][1] > gap or len(cur) >= maxw or re.search(r"[.?!,;:]$", cur[-1][2])):
                carry = []   # non chiudere un cartello su articolo/preposizione: passa al successivo
                while len(cur) > 1 and cur[-1][2].lower().strip(",.") in FUNC and wd[0] - cur[-1][1] <= gap:
                    carry.insert(0, cur.pop())
                flush(); cur.extend(carry)
            cur.append(wd)
        flush()
    return cues


# ---------- build ----------
def build(spec, out_dir):
    src, src_dur = spec["source"], int(round(spec["source_duration_s"] * FPS))
    winwords = load_words(spec)
    segs = fine_segments(spec, winwords); tmap = TimeMap(segs)
    push = spec.get("zoom_push", 0.05)
    for t in spec.get("takeovers", []):
        t["src_end"] = tmap.src_of_reel(tmap.reel(t["src_start"]) + t["dur"])
    take_f = [(fr(t["src_start"]), fr(t["src_end"])) for t in spec.get("takeovers", [])]
    take_reel = ([(tmap.reel(t["src_start"]), tmap.reel(t["src_start"]) + t["dur"]) for t in spec.get("takeovers", [])]
                 + [(tmap.reel(o["src"]), tmap.reel(o["src"]) + o["dur"]) for o in spec.get("overlays", [])])

    v, a1, a2, pos = [], [], [], 0
    for i, sg in enumerate(segs, 1):
        fi, fo = fr(sg["in"]), fr(sg["out"]); d = fo - fi
        base = framing(sg["cx"], sg["cy"], sg["zoom"])
        common = (f'<name>{esc(sg["label"])}</name><enabled>TRUE</enabled><duration>{src_dur}</duration>{RATE}'
                  f'<start>{pos}</start><end>{pos + d}</end><in>{fi}</in><out>{fo}</out>')
        v.append(f'<clipitem id="cl{i}-v">{common}{src_file(src, src_dur, i == 1)}<sourcetrack><mediatype>video</mediatype><trackindex>1</trackindex></sourcetrack>'
                 f'{motion_kf(fi, fo, base, take_f, push, pip_target(sg["cx"], sg["cy"]))}{links(i)}</clipitem>')
        for k, lst in ((1, a1), (2, a2)):
            lst.append(f'<clipitem id="cl{i}-a{k}" premiereChannelType="mono">{common}{src_file(src, src_dur, False)}'
                       f'<sourcetrack><mediatype>audio</mediatype><trackindex>{k}</trackindex></sourcetrack>{links(i)}</clipitem>')
        pos += d

    def mov_clip(fid, path, a, d):
        return (f'<clipitem id="{fid}"><name>MG {esc(os.path.basename(path))}</name><enabled>TRUE</enabled><duration>{d}</duration>{RATE}'
                f'<start>{a}</start><end>{a + d}</end><in>0</in><out>{d}</out><alphatype>straight</alphatype>'
                f'<file id="f-{fid}"><name>{esc(os.path.basename(path))}</name><pathurl>{url(path)}</pathurl>{RATE}<duration>{d}</duration>'
                f'<media><video><samplecharacteristics>{RATE}<width>{SW}</width><height>{SH}</height></samplecharacteristics></video></media></file>'
                f'<sourcetrack><mediatype>video</mediatype><trackindex>1</trackindex></sourcetrack></clipitem>')
    # overlay: ogni takeover ha il suo MOV; gli overlay "card" hanno un src; gli stinger vanno sui tagli scelti
    ovs, j = [], 0
    for t in spec.get("takeovers", []):
        a = fr(tmap.reel(t["src_start"])); d = fr(t["dur"])
        ovs.append((a, mov_clip(f"ov{j}", t["file"], a, d))); j += 1
    for o in spec.get("overlays", []):
        a = fr(tmap.reel(o["src"])); d = fr(o["dur"])
        ovs.append((a, mov_clip(f"ov{j}", o["file"], a, d))); j += 1
    stingers, extra_sfx = "", []
    wipe = spec.get("stinger")
    if wipe:
        dw = fr(wipe["dur"])
        for k in spec.get("stinger_on_cuts", []):          # k = indice del taglio (fine del segmento k)
            if 0 < k < len(segs):
                a = fr(tmap.segs[k][2]) - dw // 2
                stingers += mov_clip(f"st{k}", wipe["file"], max(0, a), dw); extra_sfx.append((max(0, a), "swish"))
    ovs.sort(key=lambda x: x[0]); ovs = "".join(c for _, c in ovs)

    subs = ""
    for k, (a, b, t) in enumerate(subtitle_cues(winwords, tmap, spec)):
        fa, fb = fr(tmap.reel(a)), fr(tmap.reel(b)); fb = max(fb, fa + 3)
        if any(x <= tmap.reel(a) < y for x, y in take_reel): continue
        subs += graphic(f"sub{k}", t, fa, fb, text_data(t, 78, FONT_SUB, fill=FUCSIA if is_key(t) else WHITE, stroke_w=12),
                        spec.get("sub_y", 0.72), [(0, 88), (2, 104), (4, 100)])

    sfx, seen = "", set()
    items = [(fr(tmap.reel(t)), name) for t, name in spec.get("sfx", [])] + extra_sfx
    for j, (a, name) in enumerate(sorted(items)):
        path = os.path.join(spec["sfx_dir"], name + ".wav")
        with wave.open(path) as w: d = max(1, int(round(w.getnframes() / w.getframerate() * FPS)))
        if name in seen: f = f'<file id="sfx-{name}"/>'
        else:
            seen.add(name)
            f = (f'<file id="sfx-{name}"><name>{name}.wav</name><pathurl>{url(path)}</pathurl>{RATE}<duration>{d}</duration>'
                 f'<media><audio><samplecharacteristics><depth>16</depth><samplerate>48000</samplerate></samplecharacteristics><channelcount>2</channelcount></audio></media></file>')
        sfx += (f'<clipitem id="sx{j}" premiereChannelType="mono"><name>SFX {name}</name><enabled>TRUE</enabled><duration>{d}</duration>{RATE}'
                f'<start>{a}</start><end>{a + d}</end><in>0</in><out>{d}</out>{f}<sourcetrack><mediatype>audio</mediatype><trackindex>1</trackindex></sourcetrack></clipitem>')

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
{trk("".join(v))}
{trk(ovs)}
{trk(stingers)}
{trk(subs)}
</video>
<audio>
<numOutputChannels>2</numOutputChannels>
<format><samplecharacteristics><depth>16</depth><samplerate>48000</samplerate></samplecharacteristics></format>
<track currentExplodedTrackIndex="0" premiereTrackType="Stereo">{"".join(a1)}<enabled>TRUE</enabled><locked>FALSE</locked></track>
<track currentExplodedTrackIndex="1" premiereTrackType="Stereo">{"".join(a2)}<enabled>TRUE</enabled><locked>FALSE</locked></track>
<track premiereTrackType="Mono">{sfx}<enabled>TRUE</enabled><locked>FALSE</locked></track>
</audio>
</media>
</sequence>
</xmeml>
'''
    out = os.path.join(out_dir, f'{spec["name"]}.xml')
    open(out, "w", encoding="utf-8").write(xml)
    print(out, f"{pos / FPS:.1f}s, {len(segs)} tagli")
    for s in segs: print(f"   {s['in']:8.2f} -> {s['out']:8.2f}  ({s['out']-s['in']:.2f}s) zoom {s['zoom']}")
    return out, tmap


if __name__ == "__main__":
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    build(spec, sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.abspath(sys.argv[1])))
