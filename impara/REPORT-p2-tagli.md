# Analisi stile Mary — progetto "1 LUGLIO 2026", sequenza "tagli"

Analisi read-only di `p2.xml` (Premiere 26, creato 1/7/2026, ultimo salvataggio 26.3.0). Fonte: `UNIVERSITY 1 LUGLIO 2026 01.mp4` (1920x1080, 24 fps, 3h18m, H.264 5,7 Mbps, AAC 48 kHz). Audio esterni: `antonio-esv2-50p-bg-10p-music-3p.wav` (48,25 s, 48 kHz/16 bit) e `Angelika Conrad - Sunbeam.wav` (162,9 s, 44,1 kHz/24 bit). Frame in `frames_p2/` (`src_*.jpg` sorgente, `comp_*.jpg` crop ricostruiti, `montage_src.jpg`, `montage_comp.jpg`).

**Verdetto**: non è un reel chiuso né una selezione grezza. È un montaggio 9:16 quasi finito (sottotitoli corretti a mano, musica Remix, voce già processata) salvato in uno stato "spezzato": due blocchi con un buco di 22,25 s in mezzo. Il contenuto reale è 47,1 s.

## 1. Sequenza

| Parametro | Valore |
|---|---|
| Risoluzione | 1080x1920 (9:16), PAR 1:1, 24 fps (10584000000 ticks/frame) |
| Audio | 48 kHz stereo, Rec.709 display-referred |
| Tracce | V1 (21 clip), V2 (2 livelli di regolazione vuoti), A1 camera (mutata), A2 voce processata, A3 musica, 1 traccia Captions it-IT |
| Timeline | 0–69,375 s; **blocco B** 0–31,875 s, **vuoto** 31,875–54,125 s, **blocco A** 54,125–69,375 s |
| In/Out sequenza | 0–31,875 s (solo blocco B) |
| Marker | 1 marker commento a 8,167 s |
| Export registrato | `export/ESTRATTO_PERCHè LO FACCIO.mp4`, Match Source - Adaptive High Bitrate (H.264/AAC), range 0–60,1 s a livello progetto; a livello sequenza CustomOut 46,75 s |
| Lumetri / transizioni video / testi grafici | **nessuno** (0 occorrenze di Lumetri nel file) |

Prova dell'ordine originale: la wav della voce copre il blocco A con i secondi 0–15,25 e il blocco B con 15,25–46,75; i due livelli di regolazione su V2 e i caption hanno in-point sintetici 3600,0 (A) e 3615,25 (B). Quindi la sequenza era A→B continua (46,75 s), esportata così per il processing voce; poi Mary ha spostato B in testa (la domanda-hook "siamo veramente sicuri…?") e parcheggiato A a 54 s, senza chiudere il buco. In/Out su B suggerisce che stesse valutando B da solo (31,9 s).

## 2. Timeline video (V1, unica traccia con immagine)

| # | Timeline | Dur | Sorgente in–out | Salto | Scala | Pan kf | Testo (caption) |
|---|---|---|---|---|---|---|---|
| 1 | 0,000–1,625 | 1,63 | 1380,13–1381,75 | — | **248,8** | 2 | HOOK "E la domanda che uno si fa è" |
| 2 | 1,625–5,250 | 3,63 | 1383,71–1387,33 | +1,96 | 177,8 | 0 | "ma siamo veramente sicuri… quello che sostanzialmente" |
| 3 | 5,250–6,500 | 1,25 | 1388,83–1390,08 | +1,50 | **244,8** | 2 | "abbiamo inseguito per anni," |
| 4 | 6,500–7,708 | 1,21 | 1391,00–1392,21 | +0,92 | 177,8 | 2 | "sia effettivamente" |
| 5 | 7,708–8,958 | 1,25 | 1394,29–1395,54 | +2,08 | 177,8 | 2 | "Quello che noi tutti vogliamo?" |
| 6 | 8,958–11,125 | 2,17 | 1442,88–1445,04 | +47,3 | 177,8 | 0 | "mi raccomando… non fare questo," |
| 7 | 11,125–12,292 | 1,17 | 1445,38–1446,54 | +0,33 | **273,8** | 2 | "attenzione se fai quello ti fai male" |
| 8 | 12,292–13,083 | 0,79 | 1433,83–1434,63 | **−12,7** | 177,8 | 0 | "i nostri genitori" |
| 9 | 13,083–14,167 | 1,08 | 1439,25–1440,33 | +4,63 | 177,8 | (fuori clip) | "ci hanno trasmesso che l'errore" |
| 10 | 14,167–14,750 | 0,58 | 1451,04–1451,63 | +10,7 | **271,8** | 0 | "è una cosa sbagliata." |
| 11 | 14,750–16,042 | 1,29 | 1452,46–1453,75 | +0,83 | **212,8** | 2 | idem |
| 12 | 16,042–20,500 | 4,46 | 1455,04–1459,50 | +1,29 | 177,8 | 6 | "Ma in realtà, ragazzi, l'errore è una tappa…" |
| 13 | 20,500–22,250 | 1,75 | 1460,17–1461,92 | +0,67 | **249,8** | 6 (condivisi con 12) | "per raggiungere i nostri obiettivi." |
| 14 | 22,250–25,292 | 3,04 | 1463,67–1466,71 | +1,75 | 177,8 | 3 | "dagli errori / Dobbiamo comprendere / e capire" |
| 15 | 25,292–27,458 | 2,17 | 1467,79–1469,96 | +1,08 | 177,8 | 0 | "di avere il coraggio di andare avanti." |
| 16 | 27,458–31,875 | 4,42 | 1469,96–1474,38 | **0,00** (split solo video) | 177,8 | 3 | "l'errore non deve generare paura, ma coraggio." |
| 17 | 54,125–57,417 | 3,29 | 1344,96–1348,25 | (blocco A) | 177,8 | 0 | "Noi oggi lavoriamo… 40 ore a settimana?" |
| 18 | 57,417–60,375 | 2,96 | 1358,83–1361,79 | +10,6 | **237,8** | 2 | "per uno stipendio medio di 1400/1.500€" |
| 19 | 60,375–64,917 | 4,54 | 1362,79–1367,33 | +1,00 | 177,8 | 2 | "Il valore medio orario… vale 6/7€ l'ora." |
| 20 | 64,917–66,958 | 2,04 | 1368,75–1370,79 | +1,42 | **223,8** | 0 | "È il tempo che noi togliamo" |
| 21 | 66,958–69,375 | 2,42 | 1371,63–1374,04 | +0,83 | 177,8 | 0 | "ai nostri figli, alle nostre passioni, ai nostri hobby." |

**Statistiche**: 21 clip, 19 tagli interni (+1 confine di blocco) su 47,1 s di contenuto → **24,2 tagli/min** (25,5 contando il confine). Durata media **2,24 s**, mediana 2,04, min 0,58, max 4,54. Distribuzione: 2 clip <1 s, 8 tra 1–2, 8 tra 2–4, 3 ≥4. Salti sorgente: 1 contiguo (15→16, ricomposizione senza taglio audio), 5 sotto 1 s, 8 tra 1 e 2,1 s, 5 grandi (4,6 / 10,6 / 10,7 / 47,3 / −12,7 s). Il "tightening" qui salta 1–2 s per taglio (pause più lunghe del formatore), non 0,1–1 s. Finestra sorgente 1344,96–1474,38 = 129,4 s per 47,1 s → **rapporto 2,75:1**. **Nessuna clip ripetuta** (zero sovrapposizioni in sorgente). Ordine: blocco A cronologico; blocco B cronologico con uno scambio (clip 6–7 anticipate rispetto a 8–9). **Hook anticipato sì, ma per blocco intero** (la domanda spostata in testa), non per singola clip ripetuta come nel Business Plan. Ultimi 0,375 s del blocco B (31,5–31,875) senza voce: A1 e A2 finiscono a 31,5.

## 3. Movimento / zoom (Motion)

Un solo livello video. **Scala base 177,78%** = altezza sorgente 1080 portata a 1920: il frame 9:16 è una fetta verticale di 607x1080 px della sorgente, nessuna barra. Niente livello platea sotto: la "split" con le teste del pubblico nella fascia bassa viene gratis dall'inquadratura larga (platea = terzo inferiore).

| Livello | Scala | Clip | Fetta sorgente (w×h px) | Uso |
|---|---|---|---|---|
| base | 177,78 | 13 su 21 | 607×1080 (piena altezza) | piano americano/mezzo busto, platea sotto |
| punch-in leggero | 212,8 / 223,8 / 237,8 | 11, 20, 18 | 508–454 × 902–808 | enfasi su numeri ("40 ore", "1400€") |
| punch-in medio | 244,8 / 248,8 / 249,8 | 3, 1 (hook), 13 | ~440×775 | hook e frasi chiave |
| punch-in forte | 271,8 / 273,8 | 10, 7 | ~395×705 | volto+microfono ("ti fai male", "cosa sbagliata") |

Tutti i valori di scala finiscono in ",78": Mary parte da 177,78 e trascina, non digita numeri tondi. **Scala mai animata** (IsTimeVarying assente su Scala). **Posizione animata in 13 clip su 21**: 17 segmenti di pan orizzontale effettivi, durata tipica 0,5–0,8 s (fino a 2,25 s nelle clip lunghe), ampiezza 0,2–0,44 normalizzata = 90–265 px sorgente, con handle di interpolazione non lineari (ease). Non sono zoom: sono **ri-inquadrature che seguono il formatore che cammina** sul palco, fatte a mano clip per clip. Nessun pan verticale (Y fisso 0,5, salvo 0,44 e 0,40 su clip 18 e 20). Ritaglio 0, rotazione 0, anti-flicker 0.

V2: due `Livello di regolazione` senza alcun effetto, coestensivi ai due blocchi — residuo di un Lumetri rimosso o mai applicato. Nessuna transizione video, nessun Mister Horse, nessuna forma.

## 4. Testi

Solo sottotitoli nativi (traccia Captions, trascrizione corretta a mano: virgolette tipografiche "mi raccomando…", "1400/1.500€", "6/7€ l'ora", "boh,").

| Parametro | Valore |
|---|---|
| Font | **Montserrat-Bold** (blob stile traccia), dimensione 48 (float nel blob) |
| Cartelli | 30, tutti con testo (nessun vuoto) |
| Parole per cartello | media **4,5**, mediana 4,5, min 2, max 8; max 41 caratteri |
| Durata on-screen | media **1,57 s**, mediana 1,54 (0,58–3,00 s) |
| Righe | 20 a una riga, 10 a due righe con a capo manuale (`\r`) |
| Allineamento | i confini dei cartelli coincidono quasi sempre con i tagli video; un buco di 0,167 s a 29,9 s |

Nessun titolo, callout o cartello grafico; i 3 `AE.ADBE Text` del file sono gli stili progetto dei caption.

## 5. Colore

**Nessun Lumetri, nessuna correzione**: la sorgente va in uscita com'è (0 occorrenze nel file). I livelli di regolazione su V2 sono vuoti.

## 6. Audio

| Traccia | Contenuto | Posizione | Livelli / effetti |
|---|---|---|---|
| A1 | audio camera delle 20 clip (linkate al video) | 0–31,5 e 54,1–69,4 | **traccia MUTATA** (`Muto=true`); tag Essential Sound "dialog" sui clip ma nessun componente effetto reale; gain 0 |
| A2 | `antonio-esv2-50p-bg-10p-music-3p.wav` = voce dell'intero montaggio già processata fuori Premiere | 0–31,5 ← wav 15,25–46,75; 54,125–69,375 ← wav 0–15,25 | sopra, in Premiere, preset Essential Sound Dialogo: **Dynamics** (gain 0,85, soglia 0,548, ratio 0,695, release 0,718) + **Riduzione rumore 5,6%**; gain clip 0 dB; fade Constant Power 0,5 s in coda (31,0–31,5) |
| A3 | `Angelika Conrad - Sunbeam.wav` via Essential Sound **Remix** (target ≈63 s, 7 segmenti in sequenza nidificata da 68,1 s), tag "music" | 0–15,96 (remix 15,08–31,04), 15,96–31,5 (remix 33,75–49,29), 54,29–69,375 (remix 0–15,08) | gain **−22 dB** sui pezzi 1 e 3; pezzo 2 gain −15 dB + Livello 0,255 + volume canali −15 dB (più basso, è la coda); fade-in CP 0,5 s a 0, CP 0,167 s a 15,9, **fade-out CP 3,25 s** (28,25–31,5) |

Lettura del nome wav: "esv2" = Enhance Speech v2 (Adobe Podcast) al 50%, "bg-10p" = fondo ambiente al 10%, "music-3p" = musica residua al 3%: la voce di Antonio esportata dalla sequenza A→B (46,75 s), ripulita sul web e reimportata al posto dell'audio camera, poi ri-compressa in Premiere con lo stesso preset Dialogo del reel Business Plan.

Transizioni: **17 Constant Power da 0,167 s (4 frame)** centrate sui tagli di A1 (mancano solo sul taglio 20,5 e sullo split 27,46), più head 0,167 s a 54,125 e coda a 31,33. Nessun ducking, nessun keyframe di volume, nessun riser/whoosh/SFX: la musica parte a 0 insieme alla voce.

## 7. Fotogrammi

`montage_src.jpg`: una sola camera fissa da fondo sala, campo largo; formatore in giacca con microfono giallo che **cammina da sinistra a destra** del palco (x 650–1300 su 1920), schermo di proiezione dietro, teste della platea nel terzo inferiore. `montage_comp.jpg` ricostruisce i crop: a 177,8 il formatore è a mezzo busto con le teste del pubblico che occupano il 30–35% basso del frame (look "split" naturale); a 238–250 testa e spalle; a 272–274 volto e microfono riempiono il frame. I pan con keyframe compensano la camminata: senza, il soggetto uscirebbe dalla fetta di 607 px.

## 8. Sintesi — regole di stile come parametri

**Ritmo**
- Contenuto 47 s (blocchi di 31,9 + 15,3 s); 24 tagli/min; clip mediana 2,0 s, min 0,6, max 4,5.
- Tightening di 1–2 s per taglio; 5 salti grandi per cambio di frase; 1 inversione cronologica.
- Rapporto sorgente/reel 2,75:1 da una finestra di 2 min 10 s.
- Hook = la domanda retorica spostata in testa come blocco intero; nessuna clip ripetuta.

**Inquadratura / zoom**
- Un solo livello: base 177,78 (piena altezza sorgente, fetta 607x1080), soggetto a mezzo busto, platea nel terzo basso.
- Punch-in statici al taglio su 8 clip/21: 213–250 per enfasi, 272–274 sulla battuta forte (mai oltre 274).
- Pan orizzontali con keyframe (0,5–0,8 s, 90–265 px sorgente) in 13 clip per seguire chi cammina; scala mai animata.
- Nessuna transizione video.

**Testo**
- Solo caption native Montserrat-Bold 48; 4–5 parole/cartello (max 8 / 41 caratteri), 1,5 s medi, a capo a mano, trascrizione corretta (numeri e virgolette).

**Suono**
- Voce: export → Enhance Speech v2 (50/10/3) → reimport su A2, camera mutata; sopra Dialogo: compressore (soglia 0,55, ratio 0,69, release 0,72) + denoise 5,6%; gain 0.
- CP 4 frame su ogni taglio voce.
- Musica Remix Essential Sound a −22 dB, fade-in 0,5 s, fade-out 3,25 s, nessun ducking.

**Colore**: nessuno.

### UGUALE al reel Business Plan
- 1080x1920 a 24 fps, una sola camera fissa larga, crop deciso clip per clip.
- Scala fissa cambiata al taglio, punch-in statici, nessuno zoom animato.
- Caption native Montserrat-Bold ~48, 4–5 parole, ~1,5 s, a capo manuale, niente titoli/callout/forme.
- Constant Power da 4 frame su ogni taglio voce; stesso preset Essential Sound Dialogo (compressore 0,55/0,69/0,72 + restauro ~5–7%); musica fissa senza ducking e senza keyframe; Remix Essential Sound.
- Clip corte (mediana ~2 s), ordine quasi cronologico con uno scambio.

### DIVERSO dal reel Business Plan
- **Posizione animata con keyframe** (13 clip) per seguire il formatore che cammina: nel Business Plan non c'era alcun keyframe reale.
- **Un solo livello video**: niente V1 platea a 265% sotto V2; la base è 177,78 e non 226; punch-in massimo 274 e non 353–458.
- **Voce processata fuori Premiere** (Enhance Speech v2) e audio camera mutato; gain 0 invece di +8 dB.
- **Nessun Lumetri** (Business Plan: Temp −11, Tinta +8, Contrasto +29, Luci +68).
- **Niente riser, whoosh né transizione Mister Horse**; musica a −22 dB che parte a 0 (Business Plan: −26 dB dopo il hook, con riser al 30% e whoosh).
- **Nessuna clip ripetuta**: il hook è ottenuto riordinando i blocchi; fade-out musica lungo (3,25 s) in chiusura.
- Tightening più largo (1–2 s per taglio) e ritmo più alto (24 vs 20 tagli/min); rapporto sorgente 2,75:1 vs 4,2:1.
- Stato del progetto: sequenza spezzata in due blocchi con 22 s di vuoto, non ancora ricomposta/esportata in questa forma.
