# Analisi stile Mary — "REEL_ BUSINESS PLAN_UNIVERSITY 11 SETTEMBRE 2026 01_Sub_01"

Analisi read-only del `pr.xml` (Premiere 2026). Fonte: `UNIVERSITY 11 SETTEMBRE 2026 01.mp4` (1920x1080, 24 fps, 3h14m). Export registrato: `REEL_B&B - APPARTAMENTO COMPETITOR.mp4`, range 0–65 s, preset "Match Source - Adaptive High Bitrate" (H.264, AAC 48 kHz stereo). Frame estratti e compositi in `frames/` (`montage_src.jpg`, `montage_comp.jpg`).

## 1. Sequenza

| Parametro | Valore |
|---|---|
| Risoluzione | 1080x1920 (9:16), PAR 1:1 |
| Frame rate | 24 fps (10584000000 ticks/frame) |
| Audio | 48 kHz, stereo, Rec.709 display-referred |
| Durata reel | 64,917 s (export OutPoint 65,0 s) |
| Tracce | V1–V6 (V3 vuota), A1–A4, 1 traccia Captions (it-IT) |
| Residui | 2 clip "parcheggiate" e mutate a 91,7 s e 182,2 s, fuori export |
| Marker | 1 marker commento a 33,9 s |

## 2. Timeline video

V1 e V2 contengono LE STESSE 23 clip (stessi tagli, stessi in/out), con Motion diverso: V2 è l'inquadratura principale sul formatore, V1 è una seconda inquadratura della stessa sorgente, visibile solo nella fascia bassa del frame (vedi §3). Le due tracce sono un unico montaggio duplicato.

| # | Timeline | Durata | Sorgente in–out | Chi parla (dai sottotitoli) |
|---|---|---|---|---|
| 1 | 0,000–5,583 | 5,58 | 3512,50–3518,08 | HOOK studente: "Io ho fatto dei prezzi in base alla stagionalità…" |
| 2 | 5,583–8,000 | 2,42 | 3420,88–3423,29 | studente: "attorno a me c'erano solo B&B" |
| 3 | 8,000–13,000 | 5,00 | 3423,71–3428,71 | studente: "…un intero appartamento" |
| 4 | 13,000–13,833 | 0,83 | 3482,88–3483,71 | formatore: "Quanti ospiti?" |
| 5 | 13,833–14,292 | 0,46 | 3484,13–3484,58 | studente: "Quattro." |
| 6 | 14,292–17,250 | 2,96 | 3486,17–3489,13 | formatore: "due camere o 2+2 sul divano?" |
| 7 | 17,250–20,125 | 2,88 | 3489,42–3492,29 | studente |
| 8 | 20,125–21,917 | 1,79 | 3493,17–3494,96 | formatore (reframe) |
| 9 | 21,917–22,250 | 0,33 | 3495,04–3495,38 | reazione (senza testo) |
| 10 | 22,250–23,292 | 1,04 | 3495,83–3496,88 | studente "No, solo b&b" (punch-in 290%) |
| 11 | 23,292–27,292 | 4,00 | 3501,71–3505,71 | formatore + studente "circa 80€" |
| 12 | 27,292–32,958 | 5,67 | 3512,50–3518,17 | RIPETIZIONE del hook, senza sottotitoli |
| 13 | 32,958–37,917 | 4,96 | 3608,96–3613,92 | studente (fuori ordine cronologico) |
| 14 | 37,917–42,833 | 4,92 | 3574,67–3579,58 | formatore |
| 15 | 42,833–44,333 | 1,50 | 3580,13–3581,63 | |
| 16 | 44,333–46,042 | 1,71 | 3581,96–3583,67 | |
| 17 | 46,042–47,750 | 1,71 | 3591,83–3593,54 | |
| 18 | 47,750–48,833 | 1,08 | 3594,67–3595,75 | |
| 19 | 48,833–50,250 | 1,42 | 3596,29–3597,71 | |
| 20 | 50,250–55,250 | 5,00 | 3632,67–3637,67 | formatore (punch-in 276%) |
| 21 | 55,250–58,875 | 3,63 | 3638,46–3642,08 | formatore, primissimo piano 458% su V5 |
| 22 | 58,875–63,500 | 4,63 | 3688,92–3693,54 | formatore (276%) |
| 23 | 63,500–64,917 | 1,42 | 3694,25–3695,67 | chiusura "per il target era lo stesso" (353%) |

**Statistiche**: 23 clip, 22 tagli → **20,3 tagli/min**. Durata media 2,82 s, mediana 2,42 s, min 0,33 s, max 5,67 s. Distribuzione: 3 clip <1 s, 8 tra 1–2 s, 4 tra 2–4 s, 8 ≥4 s. Jump cut ravvicinati frequenti: 11 tagli su 22 saltano meno di 1 s di sorgente → sono tagli di pause/intercalari ("tightening"), non cambi di scena. Salti grandi (34–97 s) = cambio di argomento. Usa 274,8 s di live (3420–3695) per 64,9 s di reel: rapporto 4,2:1. **Una clip ripetuta**: il hook (3512,5) viene usato in apertura e poi rimesso al suo posto cronologico a 27,3 s (teaser + payoff). L'ordine è quasi cronologico con uno scambio (clip 13 anticipata rispetto alla 14). L'alternanza formatore/studente non è fatta con inquadrature diverse: la camera è una sola, fissa, larga; il "chi parla" è deciso dall'audio, l'immagine resta quasi sempre sul formatore.

## 3. Movimento / zoom (Motion)

Nessun keyframe reale nel file: tutti i parametri Motion sono statici per clip (gli `IsTimeVarying=true` hanno `Keyframes` vuoto). **Niente punch-in animati, niente pan, niente zoom lenti**: la grammatica è "scala fissa per clip, cambiata al taglio".

| Livello | Scala | Posizione (norm.) | Cosa inquadra |
|---|---|---|---|
| V1 (tutte le 23 clip) | 265 | (-0,560 ; 0,757) | sorgente x 1188–1596, y 0–716: la platea (zona in cui siede lo studente). Visibile solo nella fascia bassa (circa 230 px, y 1690–1920) dove V2 non copre |
| V2 base (17 clip) | 226 | (1,528 ; 0,245) o (1,528 ; 0,218) | formatore in piedi, piano americano, sorgente x 230–708 |
| V2 reframe | 226 | (1,780 ; 0,262) | clip 8–9: il formatore si è spostato a sinistra |
| V2 punch-in | 290 | (1,873 ; 0,295) | clip 10 (1,0 s) |
| V2 punch-in | 276 | (2,103 ; 0,221) | clip 20 e 22 |
| V2 punch-in | 353 | (2,093 ; 0,221) | clip 23, chiusura |
| V5 punch-in | 458 | (3,051 ; 0,365) | clip 21: primissimo piano volto (sorgente x 241–476, y 387–806) |

Regola dedotta: base 226%, punch-in a 276–290% su frasi chiave, 353–458% sulla frase di chiusura o sulla battuta più forte; il crop viene ri-centrato a mano su ogni clip per seguire il soggetto che cammina. Il formatore è sempre nel terzo alto/centrale del frame, la platea nella fascia bassa: lo stile caption si chiama infatti "TEXT SPLIT" (testo al confine fra le due inquadrature).

Geometry2 / Mirror / Alpha Adjust / Motion Blur / AEMask2 NON sono scelte di Mary: stanno tutti nelle due coppie di livelli "Figura" su V5/V6 a 5,458–5,958 s e sono i livelli di regolazione di una **transizione Mister Horse (Premiere Composer)**: zoom verticale (Altezza scala 200→50), specchiatura (Mirror angolo 0/180, centro 0,75/0,25) e sfocatura direzionale 90° con maschere. I testi AE.ADBE Text lì dentro sono "Mister Horse Adjustment" / "If the transition isn't working, visit misterhorse.com" in Arial, invisibili. È l'unica transizione del reel, sul passaggio hook → corpo. Tutti gli altri 21 tagli sono stacchi secchi.

**Anomalia da verificare con Mary**: su V4 c'è un matte colore "NERO" (nero, scala 100, posizione centrale, opacità default) per tutta la durata, sopra V1 e V2. Così com'è salvato coprirebbe tutto il video; non c'è maschera né opacità ridotta e Premiere non serializza lo stato "output traccia" (occhio). Quasi certamente V4 era spenta in uscita, oppure è un residuo. Non va copiato.

## 4. Testi

Non ci sono titoli, callout o cartelli: **l'unico testo visibile sono i sottotitoli nativi Premiere** (traccia Captions, trascrizione automatica poi corretta a mano: "B&B", "80€", "2+2 SUL DIVANO").

| Parametro | Valore |
|---|---|
| Font | Montserrat-Bold (stile traccia "TEXT SPLIT"; lo stile progetto padre usa Montserrat-ExtraBold) |
| Dimensione | 48 (dal template; stima, il blob è binario) |
| Colori | non decodificabili dal blob con certezza; nessun riempimento sfondo attivo |
| Cartelli | 41 item, 36 con testo, 5 vuoti (la ripetizione del hook a 27,3–33 s e la reazione a 21,9 s restano senza testo) |
| Parole per cartello | media 5,6, mediana 5,5, max 10; max 49 caratteri |
| Durata on-screen | media 1,64 s, mediana 1,58 s (0,33–3,96 s) |
| Righe | 1–2 righe, a capo manuale (`\r`) su 2–4 parole |

Sono sottotitoli a frase/sintagma, **non parola per parola**, e non c'è nessuna Forma (AE.ADBE Shape) visibile: le 4 Shape sono dentro i preset Mister Horse.

## 5. Colore (Lumetri, solo su V2 e sulla clip V5)

Un unico preset applicato identico a tutte le clip: **Temperatura -11, Tinta +8, Contrasto +29, Luci +68**. Tutto il resto a default: esposizione 0, ombre/bianchi/neri 0, saturazione 100, nessuna LUT, nessuna curva, nessuna vignetta, nessun HSL. V1 (la fascia platea) non ha Lumetri.

## 6. Audio

| Traccia | Contenuto | Start–End | Livelli |
|---|---|---|---|
| A1 | dialogo camera (23 clip) | 0–64,9 | Gain clip **+8 dB**; Essential Sound "Dialogo": Clarity → Dynamics (compressore soglia 0,55, ratio 0,69, release 0,72), Restoration leggera (rumore/rombo ≈5–7%) |
| A2 | whoosh `Transition Complex 14.wav` | 5,500–5,875 | velocità 160%, livello clip -20 dB, volume canali -15 dB, tag "sfx" |
| A3 | riser `Cymbal Risers - Reverse Cymbal.wav` | 0,000–5,875 | **velocità 30%** (1,76 s stirati a 5,9 s), gain -26 dB, fade-in Constant Power 0,75 s |
| A4 | musica `Rhythm Scott - Battle Cry.wav` | 5,667–64,917 | **Remix** Essential Sound (2 segmenti: 0–30 s e 32,9–62,2 s, giunta a 35,67 s), gain **-26 dB**, nessun keyframe |

Transizioni audio: **23 Constant Power da 0,167 s (4 frame)** centrate su ogni taglio del dialogo + 1 da 0,75 s sul riser. Nessun ducking (né keyframe né preset ducking): la musica sta fissa a -26 dB sotto la voce a +8 dB. Il riser parte a 0 e culmina esattamente sul taglio a 5,583; il whoosh copre il taglio (5,50–5,88) e la musica entra 2 frame dopo (5,667). Il riser anticipa un taglio, non un cartello.

## 7. Fotogrammi

`frames/src_*.jpg`: la sorgente è un'unica camera fissa, campo largo da fondo sala: formatore in piedi a sinistra/centro (x≈250–500 su 1920), schermo proiezione dietro, platea a destra (x≈1150–1920). `frames/comp_*.jpg` ricostruiscono il crop di Mary: V2 taglia il formatore dalla testa alle cosce con aria sopra la testa quasi nulla, lo riallinea clip per clip; V1 porta la fila di platea (lo studente) nella fascia bassa. Lo studente non ha mai un'inquadratura dedicata: nel punch-in 458% (clip 21) si vede solo il volto del formatore.

## 8. Sintesi — cosa copiare nella skill reel-unicorn

**Ritmo**
- Durata 60–65 s; 20–22 tagli/min; clip 1–5 s con mediana 2,4 s; mai più di 5,7 s.
- Apertura con HOOK di 5,5 s preso dal cuore del dialogo (la frase "sbagliata" dello studente), poi la stessa clip ri-usata al suo posto cronologico.
- Tagli di pulizia: saltare 0,1–1 s di sorgente fra una frase e l'altra (metà dei tagli sono così).
- Micro-clip da 0,3–0,8 s per domanda/risposta secca ("Quanti ospiti?" / "Quattro.").
- Rapporto sorgente/reel ≈ 4:1 da una finestra di 4–5 minuti di live.

**Inquadratura / zoom** (sorgente 1920x1080 in sequenza 1080x1920)
- Livello principale: scala 226, soggetto nel terzo alto, ri-centrato per clip (nessuna animazione).
- Punch-in statici al taglio: 276–290 per enfasi, 353–458 per la battuta finale (1 volta a reel).
- Secondo livello sotto: stessa sorgente a scala 265 che riempie la fascia bassa con la platea (look "split").
- Una sola transizione a tutto il reel: dopo il hook, zoom+mirror+blur direzionale di 0,5 s (0,125 s prima del taglio, 0,375 dopo).

**Testo**
- Solo sottotitoli nativi, Montserrat Bold ~48, 4–7 parole per cartello (max 10 / 49 caratteri), 1,5 s medi, a capo a mano.
- Nessun titolo, nessun callout, nessuna forma.

**Suono**
- Voce: gain +8 dB + Essential Sound Dialogo (compressore + restauro leggero).
- Constant Power 4 frame su ogni taglio voce.
- Riser rallentato al 30% a -26 dB con fade-in 0,75 s che chiude sul taglio del hook; whoosh -20 dB sul taglio; musica Remix -26 dB che parte subito dopo il hook e resta fissa (nessun ducking).

**Colore**
- Un preset Lumetri unico: Temp -11, Tinta +8, Contrasto +29, Luci +68. Niente LUT/vignetta.

**Cosa NON fa Mary (vs. nostra v6)**
- Nessun takeover a tutto schermo, nessun cartello/titolo, nessuna forma grafica.
- Nessuno stinger o SFX sintetico: 1 riser + 1 whoosh di libreria in tutto il reel, usati una sola volta, bassissimi.
- Nessun zoom animato o keyframe: solo scale fisse cambiate al taglio.
- Nessun ducking automatico, nessuna curva di volume.
- Nessuna inquadratura dedicata allo studente: una camera fissa, il dialogo è gestito dall'audio e dai sottotitoli.
- Usa i sottotitoli nativi Premiere (modificabili), non testo bruciato né parola per parola.
