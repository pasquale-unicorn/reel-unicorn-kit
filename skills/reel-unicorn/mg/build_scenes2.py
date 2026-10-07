#!/usr/bin/env python3
"""Scene motion graphics v2 "takeover": sfondo scuro a tutto schermo, Angelo rimpicciolito in una finestra 16:9 in alto
(la finestra è un buco trasparente nel MOV: il video sotto viene scalato da Premiere con keyframe generati da reel_xml2.py),
contenuto grafico grande sotto. Più stinger di transizione e card lower-third.
Output: scenes2/*.html -> render MOV ProRes 4444 con alpha."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "scenes2"); os.makedirs(OUT, exist_ok=True)

# finestra PIP (deve coincidere con PIP in reel_xml2.py)
PIP_L, PIP_T, PIP_W, PIP_H, PIP_R = 41, 120, 998, 562, 36
T_IN = 7 / 24  # durata apertura/chiusura takeover (frame 24fps)

HEAD = """<!doctype html><html lang="it"><head><meta charset="UTF-8"/>
<meta name="viewport" content="width=1080, height=1920"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>
@font-face{font-family:MB;src:url(../fonts/Montserrat-Black.ttf)}
@font-face{font-family:MX;src:url(../fonts/Montserrat-ExtraBold.ttf)}
html,body{margin:0;background:transparent}
#root{position:relative;width:100%;height:100%;overflow:hidden;font-family:MB,sans-serif;color:#fff}
.clip{position:absolute;inset:0}
.hole{position:absolute;left:0;top:0;width:1080px;height:1920px;border-radius:0;box-shadow:0 0 0 4000px #0b0510}
.frame{position:absolute;left:@Lpx;top:@Tpx;width:@Wpx;height:@Hpx;border-radius:@Rpx;border:6px solid #ff00f5;box-sizing:border-box;opacity:0}
.area{position:absolute;left:0;right:0;top:760px;height:1060px}
.f{color:#ff00f5}.g{color:#19c37d}.r{color:#e5162b}.k{color:#0b0510}
.center{display:flex;align-items:center;justify-content:center}
.col{flex-direction:column}
.lbl{font-family:MX,sans-serif;letter-spacing:2px}
.big{font-size:150px;line-height:.95;text-align:center}
.stamp{position:absolute;white-space:nowrap;padding:14px 34px;border:12px solid currentColor;border-radius:22px;font-size:84px;letter-spacing:3px;transform-origin:50% 50%}
.card{position:absolute;left:60px;right:60px;top:1130px;height:520px;background:#0b0510;border-radius:40px;box-shadow:0 30px 80px rgba(0,0,0,.5);overflow:hidden;border:4px solid rgba(255,0,245,.5)}
.grain{position:absolute;inset:0;pointer-events:none;opacity:.07;background-image:repeating-linear-gradient(0deg,#fff 0 1px,transparent 1px 3px)}
</style></head><body>
""".replace("@L",str(PIP_L)).replace("@T",str(PIP_T)).replace("@W",str(PIP_W)).replace("@H",str(PIP_H)).replace("@R",str(PIP_R))

def page(cid, dur, body, js):
    return (HEAD + f'<div id="root" data-composition-id="{cid}" data-start="0" data-width="1080" data-height="1920" data-duration="{dur}">'
            f'<div class="clip" data-start="0" data-duration="{dur}">{body}</div></div>'
            f'<script>const tl=gsap.timeline({{paused:true}});{js}window.__timelines["{cid}"]=tl;</script></body></html>')

# apertura/chiusura takeover: il buco passa da tutto schermo alla finestra PIP (lineare, in sync con i keyframe di Premiere)
TAKE = """<div id="hole" class="hole"></div><div id="frm" class="frame"></div><div class="grain"></div>"""
def take_js(dur):
    return (f"tl.fromTo('#hole',{{left:0,top:0,width:1080,height:1920,borderRadius:0}},{{left:{PIP_L},top:{PIP_T},width:{PIP_W},height:{PIP_H},borderRadius:{PIP_R},duration:{T_IN:.4f},ease:'none'}},0);"
            f"tl.fromTo('#frm',{{opacity:0}},{{opacity:1,duration:.12}},{T_IN:.4f});"
            f"tl.to('#frm',{{opacity:0,duration:.08}},{dur - T_IN - .08:.4f});"
            f"tl.to('#hole',{{left:0,top:0,width:1080,height:1920,borderRadius:0,duration:{T_IN:.4f},ease:'none'}},{dur - T_IN:.4f});")

S = {}

# 1 HOOK takeover (3.0s): slam del titolo + busta timbrata
S["t1_hook"] = (3.0, TAKE + """
<div class="area">
  <div id="l1" class="big" style="position:absolute;left:0;right:0;top:20px;font-size:118px;white-space:nowrap">GLI INQUILINI</div>
  <div id="l2" class="big f" style="position:absolute;left:0;right:0;top:150px;font-size:118px;white-space:nowrap">NON PAGANO?</div>
  <div id="env" style="position:absolute;left:120px;right:120px;top:400px;height:430px;background:#fff;border-radius:30px;box-shadow:0 30px 80px rgba(0,0,0,.6)">
    <div style="position:absolute;left:0;right:0;top:0;height:0;border-left:420px solid transparent;border-right:420px solid transparent;border-top:180px solid #f1e3f3"></div>
    <div class="k" style="position:absolute;left:0;right:0;top:215px;text-align:center;font-size:96px">AFFITTO</div>
    <div class="lbl" style="position:absolute;left:0;right:0;top:335px;text-align:center;font-size:38px;color:#777">SCADENZA: IERI</div>
  </div>
  <div id="st" class="stamp center r" style="left:150px;right:150px;top:530px;background:rgba(255,255,255,.9)">NON PAGATO</div>
</div>""", take_js(3.0) + """
tl.fromTo('#l1',{y:120,opacity:0,scale:1.4},{y:0,opacity:1,scale:1,duration:.22,ease:'power4.out'},0.3);
tl.fromTo('#l2',{y:120,opacity:0,scale:1.4},{y:0,opacity:1,scale:1,duration:.22,ease:'power4.out'},0.48);
tl.fromTo('#env',{y:700,rotation:8,opacity:0},{y:0,rotation:-3,opacity:1,duration:.4,ease:'back.out(1.6)'},1.0);
tl.fromTo('#st',{scale:3.2,rotation:-30,opacity:0},{scale:1,rotation:-12,opacity:1,duration:.2,ease:'power4.in'},1.6);
tl.to('.area',{x:-14,duration:.04,yoyo:true,repeat:5},1.8);
tl.to('.area',{opacity:0,y:-80,duration:.2,ease:'power3.in'},2.5);
""")

# 2 CONTATORE takeover (3.2s): 12.000 contratti -> 3 morosità
S["t2_counter"] = (3.2, TAKE + """
<div class="area">
  <div id="p1" class="center col" style="position:absolute;inset:0">
    <div id="num" style="font-size:250px;line-height:1;font-variant-numeric:tabular-nums">0</div>
    <div class="lbl" style="font-size:54px;color:#bbb;margin-top:10px">CONTRATTI D'AFFITTO</div>
    <div style="width:820px;height:26px;background:#2a1530;border-radius:13px;margin-top:60px;overflow:hidden"><div id="bar" style="height:100%;width:100%;background:#ff00f5;transform-origin:0 50%"></div></div>
  </div>
  <div id="p2" class="center col" style="position:absolute;inset:0;background:#0b0510">
    <div class="lbl" style="font-size:50px;color:#bbb">MOROSITÀ IN 14 ANNI</div>
    <div id="three" class="f" style="font-size:520px;line-height:1">3</div>
    <div id="pct" class="lbl" style="font-size:54px;background:#ff00f5;color:#0b0510;padding:10px 34px;border-radius:16px">LO 0,025%</div>
  </div>
</div>""", take_js(3.2) + """
const o={v:0};tl.to(o,{v:12000,duration:1.0,ease:'power2.out',onUpdate:()=>{document.getElementById('num').textContent=Math.round(o.v).toLocaleString('it-IT')}},0.35);
tl.fromTo('#bar',{scaleX:0},{scaleX:1,duration:1.0,ease:'power2.out'},0.35);
tl.fromTo('#num',{scale:.6},{scale:1,duration:1.0,ease:'power2.out'},0.35);
tl.fromTo('#p2',{clipPath:'circle(0% at 50% 50%)'},{clipPath:'circle(80% at 50% 50%)',duration:.28,ease:'power3.out'},1.7);
tl.fromTo('#three',{scale:2.5,opacity:0},{scale:1,opacity:1,duration:.3,ease:'back.out(2.5)'},1.75);
tl.to('.area',{x:12,duration:.04,yoyo:true,repeat:5},1.95);
tl.fromTo('#pct',{y:40,opacity:0},{y:0,opacity:1,duration:.25,ease:'power3.out'},2.25);
tl.to('.area',{opacity:0,duration:.2},2.75);
""")

# 3 TELEGIORNALE takeover (3.6s)
S["t3_tg"] = (3.6, TAKE + """
<div class="area">
  <div id="tv" style="position:absolute;inset:40px 50px;background:radial-gradient(circle at 50% 30%,#2b3d5c,#0c1220);border-radius:36px;overflow:hidden;border:10px solid #222">
    <div style="position:absolute;left:36px;top:30px;background:#e5162b;padding:6px 22px;border-radius:8px;font-size:48px">TG</div>
    <div class="lbl" style="position:absolute;right:40px;top:40px;font-size:36px;color:#ffcc00">● LIVE</div>
    <div id="ban" style="position:absolute;left:0;right:0;top:170px;background:#e5162b;padding:16px 36px;font-size:54px">ULTIM'ORA</div>
    <div id="big" style="position:absolute;left:0;right:0;top:300px;text-align:center;font-size:230px;line-height:1">50%</div>
    <div id="sub" class="lbl" style="position:absolute;left:0;right:0;top:560px;text-align:center;font-size:60px">DI INQUILINI MOROSI</div>
    <div id="tick" class="lbl" style="position:absolute;left:0;bottom:0;white-space:nowrap;background:#ffcc00;color:#111;font-size:36px;padding:10px 0;width:3200px">&nbsp; INQUILINI CHE NON PAGANO · ALLARME AFFITTI · PROPRIETARI IN CRISI · INQUILINI CHE NON PAGANO · ALLARME AFFITTI ·</div>
    <div id="noise" style="position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(255,255,255,.14) 0 2px,transparent 2px 5px)"></div>
  </div>
  <div id="st" class="stamp center f" style="left:150px;right:150px;top:380px;background:rgba(11,5,16,.92);font-size:110px">SICURO?</div>
</div>""", take_js(3.6) + """
tl.fromTo('#tv',{scaleY:.02,scaleX:1.1},{scaleY:1,scaleX:1,duration:.22,ease:'power4.out'},0.3);
tl.fromTo('#noise',{opacity:1},{opacity:0,duration:.4},0.35);
tl.fromTo('#ban',{xPercent:-100},{xPercent:0,duration:.3,ease:'power3.out'},0.6);
tl.fromTo('#tick',{x:0},{x:-1600,duration:3.6,ease:'none'},0);
tl.fromTo('#big',{scale:0,opacity:0},{scale:1,opacity:1,duration:.3,ease:'back.out(2.5)'},1.0);
tl.fromTo('#sub',{opacity:0,y:30},{opacity:1,y:0,duration:.25},1.25);
tl.fromTo('#st',{scale:3,rotation:20,opacity:0},{scale:1,rotation:8,opacity:1,duration:.2,ease:'power4.in'},2.5);
tl.to('#tv',{filter:'grayscale(1) brightness(.5)',duration:.2},2.5);
tl.to('.area',{scaleY:.02,opacity:0,duration:.2,ease:'power3.in'},3.15);
""")

# 4 AGENZIA SOTTO CASA — card (3.0s)
S["c4_agenzia"] = (3.0, """
<div id="card" class="card">
  <div id="casa" style="position:absolute;left:70px;top:70px;font-size:170px;line-height:1">🏠</div>
  <div class="lbl" style="position:absolute;left:60px;top:265px;font-size:34px;width:210px;text-align:center;color:#bbb">CASA TUA</div>
  <svg style="position:absolute;left:270px;top:130px" width="400" height="80"><path id="path" d="M10 40 L390 40" stroke="#ff00f5" stroke-width="12" stroke-linecap="round" stroke-dasharray="1 28" fill="none"/></svg>
  <div id="pin" class="lbl f" style="position:absolute;left:340px;top:50px;font-size:46px">📍 10 METRI</div>
  <div id="ag" style="position:absolute;right:70px;top:60px;font-size:180px;line-height:1">🏢</div>
  <div id="agl" class="lbl" style="position:absolute;right:50px;top:265px;background:#ff00f5;color:#0b0510;padding:6px 18px;border-radius:10px;font-size:34px">AGENZIA</div>
  <div id="q" class="center" style="position:absolute;left:0;right:0;bottom:40px;height:90px;font-size:50px;white-space:nowrap">SCELTA PER COMODITÀ<span id="face" style="display:inline-block;font-size:72px;margin-left:18px">🤦</span></div>
</div>""", """
tl.fromTo('#card',{y:500,opacity:0},{y:0,opacity:1,duration:.3,ease:'back.out(1.6)'},0);
tl.fromTo('#casa',{scale:0},{scale:1,duration:.3,ease:'back.out(2.5)'},0.15);
tl.fromTo('#ag',{scale:0},{scale:1,duration:.3,ease:'back.out(2.5)'},0.4);
tl.fromTo('#agl',{scale:0},{scale:1,duration:.25,ease:'back.out(2.5)'},0.55);
tl.fromTo('#path',{strokeDashoffset:300},{strokeDashoffset:0,duration:.6,ease:'none'},0.6);
tl.fromTo('#pin',{y:-30,opacity:0},{y:0,opacity:1,duration:.3,ease:'bounce.out'},0.9);
tl.fromTo('#q',{opacity:0,y:30},{opacity:1,y:0,duration:.25},1.4);
tl.fromTo('#face',{scale:0,rotation:-40},{scale:1,rotation:0,duration:.35,ease:'back.out(3)'},1.9);
tl.to('#card',{y:500,opacity:0,duration:.25,ease:'power3.in'},2.75);
""")

# 5 BADGE — card (3.2s)
S["c5_badge"] = (3.2, """
<div class="card" style="background:transparent;border:none;box-shadow:none">
  <div id="b1" class="center col" style="position:absolute;left:0;top:0;width:290px;height:400px;background:#0b0510;border-radius:30px;border:4px solid rgba(255,0,245,.5)"><div style="font-size:140px;line-height:1">💼</div><div class="lbl" style="font-size:32px;margin-top:20px">FINANZIERE</div></div>
  <div id="b2" class="center col" style="position:absolute;left:335px;top:0;width:290px;height:400px;background:#0b0510;border-radius:30px;border:4px solid rgba(255,0,245,.5)"><div style="font-size:140px;line-height:1">🚓</div><div class="lbl" style="font-size:32px;margin-top:20px">CARABINIERE</div></div>
  <div id="b3" class="center col" style="position:absolute;left:670px;top:0;width:290px;height:400px;background:#0b0510;border-radius:30px;border:4px solid rgba(255,0,245,.5)"><div style="font-size:140px;line-height:1">👮</div><div class="lbl" style="font-size:32px;margin-top:20px">POLIZIOTTO</div></div>
  <svg id="x" style="position:absolute;left:180px;top:-20px" width="600" height="440"><path id="x1" d="M40 40 L560 400" stroke="#e5162b" stroke-width="44" stroke-linecap="round" fill="none"/><path id="x2" d="M560 40 L40 400" stroke="#e5162b" stroke-width="44" stroke-linecap="round" fill="none"/></svg>
  <div id="no" class="center" style="position:absolute;left:0;right:0;top:420px;height:100px;background:#e5162b;border-radius:24px;font-size:60px">NON È UNA GARANZIA</div>
</div>""", """
[['#b1',0.05],['#b2',0.55],['#b3',1.1]].forEach(([s,t])=>tl.fromTo(s,{y:300,opacity:0,rotation:-8},{y:0,opacity:1,rotation:0,duration:.28,ease:'back.out(2)'},t));
tl.fromTo('#x1',{strokeDasharray:700,strokeDashoffset:700},{strokeDashoffset:0,duration:.14,ease:'power2.in'},2.0);
tl.fromTo('#x2',{strokeDasharray:700,strokeDashoffset:700},{strokeDashoffset:0,duration:.14,ease:'power2.in'},2.12);
tl.to(['#b1','#b2','#b3'],{filter:'grayscale(1)',opacity:.55,duration:.2},2.1);
tl.fromTo('#no',{scaleX:0},{scaleX:1,duration:.25,ease:'power3.out'},2.25);
tl.to('.card',{opacity:0,y:200,duration:.25,ease:'power3.in'},2.95);
""")

# 6 STRUMENTI takeover (3.6s): indicatore + checklist
S["t6_gauge"] = (3.6, TAKE + """
<div class="area">
  <div class="lbl" style="position:absolute;left:0;right:0;top:30px;text-align:center;font-size:44px;color:#bbb">CAPACITÀ DI TRATTENERE IL DENARO</div>
  <svg style="position:absolute;left:150px;top:110px" width="780" height="470" viewBox="0 0 420 260">
    <defs><linearGradient id="gr" x1="0" x2="1"><stop offset="0" stop-color="#e5162b"/><stop offset=".5" stop-color="#ffcc00"/><stop offset="1" stop-color="#19c37d"/></linearGradient></defs>
    <path d="M30 230 A180 180 0 0 1 390 230" stroke="#2a1530" stroke-width="40" fill="none" stroke-linecap="round"/>
    <path id="arc" d="M30 230 A180 180 0 0 1 390 230" stroke="url(#gr)" stroke-width="40" fill="none" stroke-linecap="round"/>
    <g id="needle" style="transform-origin:210px 230px"><line x1="210" y1="230" x2="210" y2="70" stroke="#fff" stroke-width="14" stroke-linecap="round"/><circle cx="210" cy="230" r="22" fill="#ff00f5"/></g>
  </svg>
  <div id="ok" class="g center" style="position:absolute;left:0;right:0;top:560px;font-size:96px">AFFIDABILE ✓</div>
  <div class="lbl" style="position:absolute;left:0;right:0;top:720px;font-size:52px;line-height:1.8;text-align:center">
    <span id="c1" style="display:inline-block;margin:0 20px"><span class="g">✓</span> REDDITO</span><span id="c2" style="display:inline-block;margin:0 20px"><span class="g">✓</span> SPESE</span><span id="c3" style="display:inline-block;margin:0 20px"><span class="g">✓</span> RISPARMIO</span>
  </div>
</div>""", take_js(3.6) + """
tl.fromTo('#arc',{strokeDasharray:600,strokeDashoffset:600},{strokeDashoffset:0,duration:.6,ease:'power2.out'},0.35);
tl.fromTo('#needle',{rotation:-85},{rotation:-60,duration:.3,ease:'power2.out'},0.4);
tl.to('#needle',{rotation:62,duration:1.1,ease:'elastic.out(1,.45)'},0.9);
tl.fromTo('#ok',{scale:0,opacity:0},{scale:1,opacity:1,duration:.3,ease:'back.out(3)'},2.0);
[['#c1',2.35],['#c2',2.6],['#c3',2.85]].forEach(([s,t])=>tl.fromTo(s,{y:40,opacity:0},{y:0,opacity:1,duration:.22,ease:'back.out(2)'},t));
tl.to('.area',{opacity:0,duration:.2},3.15);
""")

# 7 CHIUSURA takeover (3.0s): PAGATO + CTA
S["t7_pagato"] = (3.0, TAKE + """
<div class="area">
  <div id="env" style="position:absolute;left:120px;right:120px;top:60px;height:430px;background:#fff;border-radius:30px;box-shadow:0 30px 80px rgba(0,0,0,.6)">
    <div style="position:absolute;left:0;right:0;top:0;height:0;border-left:420px solid transparent;border-right:420px solid transparent;border-top:180px solid #f1e3f3"></div>
    <div class="k" style="position:absolute;left:0;right:0;top:215px;text-align:center;font-size:96px">AFFITTO</div>
    <div class="lbl" style="position:absolute;left:0;right:0;top:335px;text-align:center;font-size:38px;color:#777">PUNTUALE, OGNI MESE</div>
  </div>
  <div id="st" class="stamp center g" style="left:150px;right:150px;top:190px;background:rgba(255,255,255,.92)">PAGATO ✓</div>
  <div class="coin" style="position:absolute;left:480px;top:200px;font-size:110px;line-height:1">💰</div>
  <div class="coin" style="position:absolute;left:480px;top:200px;font-size:90px;line-height:1">🪙</div>
  <div class="coin" style="position:absolute;left:480px;top:200px;font-size:90px;line-height:1">🪙</div>
  <div id="cta" class="lbl center" style="position:absolute;left:140px;right:140px;top:620px;height:120px;background:#ff00f5;color:#0b0510;border-radius:60px;font-size:50px">SALVA QUESTO REEL 🔖</div>
  <div id="cta2" class="lbl" style="position:absolute;left:0;right:0;top:780px;text-align:center;font-size:40px;color:#bbb">E MANDALO A CHI HA PAURA DI AFFITTARE</div>
</div>""", take_js(3.0) + """
tl.fromTo('#env',{y:600,rotation:6,opacity:0},{y:0,rotation:-2,opacity:1,duration:.4,ease:'back.out(1.6)'},0.3);
tl.fromTo('#st',{scale:3.2,rotation:30,opacity:0},{scale:1,rotation:-10,opacity:1,duration:.2,ease:'power4.in'},0.95);
gsap.utils.toArray('.coin').forEach((c,i)=>tl.fromTo(c,{x:0,y:0,opacity:0,scale:.4},{x:(i-1)*330,y:-330-i*40,opacity:1,scale:1,duration:.6,ease:'power2.out'},1.1+i*.05));
tl.fromTo('#cta',{scale:0},{scale:1,duration:.3,ease:'back.out(2.5)'},1.6);
tl.fromTo('#cta2',{opacity:0,y:20},{opacity:1,y:0,duration:.25},1.9);
tl.to('.area',{opacity:0,duration:.2},2.55);
""")

# STINGER: wipe diagonale a 3 barre (0.4s), copre lo stacco
S["x_wipe"] = (0.4, """
<div id="w1" style="position:absolute;left:-60%;top:-20%;width:220%;height:140%;background:#ff00f5;transform:rotate(-18deg)"></div>
<div id="w2" style="position:absolute;left:-60%;top:-20%;width:220%;height:140%;background:#fff;transform:rotate(-18deg)"></div>
<div id="w3" style="position:absolute;left:-60%;top:-20%;width:220%;height:140%;background:#0b0510;transform:rotate(-18deg)"></div>
""", """
[['#w1',0],['#w2',0.04],['#w3',0.08]].forEach(([s,t])=>{tl.fromTo(s,{xPercent:-110},{xPercent:0,duration:.14,ease:'power3.in'},t);tl.to(s,{xPercent:110,duration:.16,ease:'power3.out'},t+.16);});
""")

for name, (dur, body, js) in S.items():
    open(os.path.join(OUT, f"{name}.html"), "w", encoding="utf-8").write(page(name, dur, body, js))
print(" ".join(S))
