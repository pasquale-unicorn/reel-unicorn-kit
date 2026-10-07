# Analisi stile Mary: "RECAP_montaggio" (progetto "1 LUGLIO 2026", p3)

Analisi read-only di `p3.xml` (Premiere 2026), con lo stesso metodo dei report p1/p2: dizionario ObjectID/ObjectUID, Start mancante = 0, 254016000000 tick = 1 s. Export registrato: `/Volumes/2_unicorn/EVENTI/FORMAZIONE - 1 LUGLIO 26/export/RECAP - 1 Luglio 26.mp4`, range 0–37,56 s (MZ.OutPoint = fine del pezzo). Frame in `frames_p3/` (8 jpg + `montage_p3.jpg`).

**Cos'è.** Un **recap promozionale verticale 9:16 di 37,6 s** dell'evento di luglio, non un estratto di un unico discorso. Parte da un hook provocatorio dal palco ("Ma che c**zo c'è di nobile nel lavoro?", con bleep), poi passa al racconto della sede ("poche aziende fanno… venire in sede… Benvenuto allo Unicorn") coperto di b-roll, e chiude sul palco con "…e io ho risolto tutta sta roba qui. Grazie all'immobiliare." sopra un'esterna DJI della sede. Voce, musica e b-roll si alternano come in un trailer.

**Le altre sequenze.**
- **"montaggio" (2 copie identiche, 49,1 s)**: solo audio, 5 spezzoni di `Sam Lux - Celestial Rush` uniti da 4 Constant Power di 0,44 s. **Non le ha montate Mary**: sono le sequenze interne del **Remix** di Premiere. La RemixClip su A5 ha come sorgente `AudioSequenceSource → montaggio`. Una copia per ciascuno dei due pezzi di musica. I salti nella sorgente (14,22 s = 32 beat) e le dissolvenze di 0,44 s (= 1 beat) sono a griglia di battuta.
- **"Sequenza nidificata 01"**: 1,48 s di `DJI_…0017` (59,94 fps), usata a 15,00–16,24 sotto la MOGRT "Camera Viewfinder".
- **"Duration" non è una sequenza**: è il nome di un parametro (MOGRT/Capsule).
- Il wav voce `montaggio_audio-esv2-50p-bg-10p-music-m.wav` è il parlato di un premontaggio precedente, esportato e passato in Enhance Speech v2 (stessa naming di p2). I suoi in-point seguono i tagli del live, quindi Mary ha prima scelto le frasi, poi le ha pulite fuori da Premiere e poi le ha ri-tagliate qui.

## 1. Sequenza

| Parametro | Valore |
|---|---|
| Formato | **1080x1920 (9:16)**, PAR 1:1, **25 fps** (10160640000 tick/frame), audio 48 kHz stereo |
| Durata | **37,56 s** |
| Tracce video | V1 base (live + camera parlata), V2 b-roll/glitch/Mister Horse #1, V3 Mister Horse #1 (blur) + 2 livelli Lumetri + 1 b-roll, V4 livelli di regolazione Lumetri per inquadratura, V5 MOGRT viewfinder, V6–V8 Mister Horse #2 ("Anchor") |
| Tracce audio | A1 audio live (**escluso dal solo**), A2 SFX bleep/boom, A3 voce, A4 SFX whoosh/riser/ambiente, A5 musica Remix; A6–A7 vuote. A2–A5 in **Solo** |
| Sottotitoli | 1 traccia Captions it-IT, Montserrat-Bold: 27 cartelli nel pezzo (148 in totale, gli altri stanno sul materiale parcheggiato) |
| Parcheggio | dopo 44 s: 7 frasi live candidate (97–207 s), tutti i rush camera 6F6A3380–3408 messi in fila (1553–2384 s), 2 b-roll scartati |

Sorgenti: live `UNIVERSITY…01.mp4` 1920x1080 a 24 fps (scala 177,8 = riempie l'altezza). Camera 6F6A 3840x2160 a 25 o **50 fps** (scala 88,9 = riempie l'altezza; 177,8 = punch-in 2x). DJI 3840x2160 (0018/0021/0025 sono riprese gimbal in sala, 0405/0407 sono esterne della sede di aprile, 59,94 fps a 10 bit). Glitch `.mov` 1920x1080 a 30 fps.

## 2. Struttura (inquadrature visibili, livello più alto)

| # | Timeline | Dur. | Fonte | Contenuto / note |
|---|---|---|---|---|
| 1 | 0,00–2,00 | 2,00 | LIVE | HOOK "Ma che c**zo c'è di nobile nel lavoro?". Snap zoom 100→148% in 4 frame a 0,48 s + glitch + bleep |
| 2 | 2,00–5,24 | 3,24 | LIVE | "40 ore a settimana?" (da 1345 s, salto indietro di 980 s), snap zoom 100→152% a 3,80 |
| 3 | 5,24–6,48 | 1,24 | LIVE | panoramica Motion continua (pos 0,30→0,90) spalmata su 4 clip, scala 224 |
| 4 | 6,48–8,80 | 2,32 | DJI 0018 | pubblico (cutaway sopra la voce live) |
| 5–7 | 8,80–11,56 | 2,76 | LIVE | 3 clip, una con punch-in 319% |
| 8 | 11,56–12,88 | 1,32 | DJI 0405 | esterna della sede. **Mister Horse "Anchor" + swoosh** |
| 9 | 12,88–14,08 | 1,20 | CAM 3374 | parlato del coach in sede (audio camera) |
| 10 | 14,08–15,00 | 0,92 | DJI 0021 | sala |
| 11 | 15,00–16,24 | 1,24 | DJI 0017 (nest) | zoom 100→166% + MOGRT viewfinder "REC" |
| 12 | 16,24–18,16 | 1,92 | CAM 3397 | punch-in 177% |
| 13 | 18,16–19,24 | 1,08 | CAM 3382 | **slow motion 50%** (girato a 50p) |
| 14 | 19,24–20,60 | 1,36 | CAM 3383 | sala. Il riser chiude qui e la musica si ferma |
| 15 | 20,60–22,28 | 1,68 | CAM 3374 | "Benvenuto allo Unicorn": **1,68 s senza musica**, pan Motion |
| 16 | 22,28–24,48 | 2,20 | CAM 3375 | **DROP**: boom + rientro della musica, pan Motion 1,21→−0,23 |
| 17 | 24,48–27,28 | 2,80 | CAM 3398 | slow 50%, sopra la voce live |
| 18 | 27,28–29,88 | 2,60 | DJI 0025 | pubblico |
| 19–22 | 29,88–34,80 | 4,92 | LIVE | 4 clip, punch-in 237/262% sulle 2 corte |
| 23 | 34,80–37,56 | 2,76 | DJI 0407 | esterna con insegna UNICORN. **Speed ramp** con Time Remapping (9,8 s di sorgente in 0,3 s, circa 33x) a circa 36,1 s |

Il racconto ha tre blocchi: **hook live (0–11,6)** → **sede/intervista con b-roll (11,6–29,9)** → **chiusura live + esterna (29,9–37,6)**. La voce è continua dall'inizio alla fine. Il b-roll copre la voce live (L-cut) e non interrompe mai il parlato.

## 3. Statistiche tagli

| | Valore |
|---|---|
| Inquadrature / tagli | **23 / 22** |
| Tagli/min | **35,1** (p1: 20, Business Plan: circa 20) |
| Durata media / mediana | 1,63 s / **1,36 s** |
| Min / max | 0,44 s / 3,24 s |
| Mix | LIVE 10 shot / 14,2 s (38%), CAM 7 / 12,2 s (33%), DJI 6 / 11,2 s (30%) |
| Alternanza | mai più di 4 shot live di fila. Il b-roll arriva in blocchi da 1–5 shot |

**Ritmo musicale.** Musica a **135 BPM** (beat 0,444 s, battuta 1,78 s), stima con comb filter sugli onset di energia del wav (librosa non è installato). Tolleranza ±0,06 s (1,5 frame):
- **dopo il drop (22,28–37,5): 7 tagli su 8 sul beat** (a caso se ne aspettano 2,2). Lì il montaggio segue la musica.
- **prima (0–20,6): 6 su 13** (a caso 3,5; sulla griglia di 1/8 sono 10 su 13). Qui comanda la voce e i tagli cadono sulle frasi.
- Le durate post-drop sono vicine a multipli di beat: 4,95 / 6,3 / 5,85 / 4,05 / 3,06 beat.

## 4. Motion, zoom, velocità

- Base: live a 177,8 con la posizione X spostata a mano sul soggetto (0,11–0,34). Camera 4K a 88,9 (inquadratura piena) oppure 177,8 (crop 2x).
- **Punch-in statici** al taglio: 224, 237, 262, 319%.
- **Snap zoom animati** con Trasformazione (Scala uniforme): 100→148% e 100→152% in **0,16 s (4 frame)**, con spostamento laterale. Cadono sulla parolaccia e sulla domanda "40 ore a settimana?".
- **Pan con keyframe**: un movimento unico tagliato su 4 clip live (5,24–11,56), poi 3374 e 3375 (pan rapido 1,2→−0,2 in 2,3 s).
- Velocità: 3382 e 3398 al **50%** (materiale a 50p, quindi slow motion pulito). Nest DJI con zoom 100→166%. **Speed ramp** con Time Remapping sull'esterna finale. Whoosh al 160%.

## 5. Transizioni video

| Dove | Cosa | Durata |
|---|---|---|
| 1,88–2,40 (taglio 2,00) | **Mister Horse** zoom+mirror+blur direzionale (stesso preset di p1/Business Plan, con i testi "Mister Horse Adjustment" invisibili) | 0,52 s |
| 11,28–12,20 (taglio 11,56) | **Mister Horse "Anchor"**: Corner Pin + 3 Mirror + blur direzionale su V6–V8, live → esterna della sede | 0,92 s |
| 0,68–0,72 | Dissolvenza (Impact Dissolve) solo in uscita del glitch | 0,04 s |

Tutti gli altri tagli sono **stacchi secchi**. Le 2 transizioni stanno solo sui cambi di blocco (hook→corpo, palco→sede).

## 6. Overlay glitch e grafica

- `energetic-glitch…mov`: **0,52–0,72 s (5 frame)** su V2, scala 354%, opacità 100%, **metodo di fusione non Normale** (valori interni 15/19: va controllato in Premiere quale voce corrisponde). È sincronizzato al frame con il **bleep** e con lo snap zoom: serve a censurare la parolaccia del hook.
- MOGRT **"Camera Viewfinder"** (cornice REC) a 15,00–16,24 sul nest DJI.
- Nessun titolo, lower third o logo: tutti i 23 `AE.ADBE Text` stanno dentro i preset Mister Horse.

## 7. Testi

Solo **sottotitoli nativi** Montserrat-Bold, 27 cartelli in 36,8 s (circa 1,36 s l'uno), 2–6 parole, 1–2 righe con a capo manuale. Seguono i tagli e la parolaccia è scritta "c**zo". Ci sono sottotitoli anche sui pezzi in cui la voce è coperta dal b-roll.

## 8. Lumetri

Livello di regolazione su V4 **tagliato per ogni inquadratura**, con correzione diversa shot per shot. Tutti hanno "Intensità 50" (senza LUT, quindi nessun effetto).

| Shot | Correzione |
|---|---|
| live hook 0–9,5 | Luci +63, Ombre +20 (+ Bianchi +46 a 9,5–11,6) |
| 3374 | Contr +5, Luci +13, Ombre +17 |
| DJI sala | Sat 109–116, Contr +21, Luci +54/+102, Ombre fino a +66 |
| 3382 / 3383 | Temp −11 / **Temp +29, Contr +65** |
| live finale | Luci +64, Ombre +60, Bianchi +26 |
| DJI esterne (V3) | **Sat 129, Contr +95** (riprese di aprile, piatte) |

Rispetto a p1 (un solo livello Contr +43 / Luci −31 / Ombre +19) qui il colore viene pareggiato a mano su 3 camere diverse.

## 9. Audio

Nota sulle unità: il "Livello" del volume interno ha 0 dB = 0,1778 (dB = 20·log10(v) + 15). Il "Gain" della clip è lineare (1 = 0 dB). I valori "Livello 0,1 = −20 dB" dei report precedenti vanno corretti in **−5 dB**.

| Elemento | Dove | Livello |
|---|---|---|
| Voce (wav Enhance + audio camera 3374 + live in chiusura) | 0–37,56, A3 | gain 0. Essential Sound Dialogo con **compressore identico a p1/p2** (0,8475 / soglia 0,548 / ratio 0,695 / release 0,718) + riduzione rumore 6,8%. **15 Constant Power da 0,16 s (4 frame)** su ogni taglio (0,08 s sui due più stretti) |
| Coda voce | 36,28–37,56 | **Studio Reverb** sull'ultima clip + livello → −∞ a 36,40–36,46: la frase finisce in un riverbero sotto la musica |
| **Bleep** Censor | 0,52–0,72 | gain −6 dB. Copre la parolaccia, insieme a glitch e zoom |
| Whoosh `Transition Complex 14` | 1,92–2,32 (taglio 2,00) | velocità 160%, gain −9 dB, livello −5 dB. Accompagna Mister Horse #1 |
| `Swoosh Transition 28` | 11,28–12,04 (taglio 11,56) | livello −5 dB. Accompagna Mister Horse #2 |
| Reverse Whoosh Riser | 17,76–20,60 | gain −17 dB, fade-in CP 1,76 s. **Finisce dove si ferma la musica** |
| **BOOM Impact Sub Boom** | 22,20–26,24 | gain −15 dB. **Parte 2 frame prima del drop** (22,28) |
| Ambiente camera 3375 | 22,28–24,48 | livello circa −32 dB, coda CP 0,44 s |
| Musica Remix Celestial Rush | 0–20,60 e 22,28–37,48 | gain **−20 dB**. Fade-in CP 2,2 s, **pausa di 1,68 s** prima del drop, fade-out CP 2,96 s. Sul primo pezzo 4 keyframe di livello (da +15 a 0 dB, cioè da circa −5 a −20 dB effettivi) nei primi 10 s circa: posizione esatta incerta per via del Remix |

Non c'è ducking automatico. L'unico "ducking" è a mano: musica alta all'attacco che poi scende sotto la voce, e un keyframe −4,4→0 dB su un taglio della 3374.

## 10. Fotogrammi

`frames_p3/01…08` (crop 9:16 ricostruito da scala e posizione Motion): hook live con oratore col codino; pubblico DJI; coach 3374 alla lavagna; sala con laptop "BENVENUTI UNICORNI"; slow motion della platea; pubblico DJI; oratore al microfono giallo; esterna con insegna UNICORN.

## 11. Sintesi

### Regole di sound design e transizioni di Mary (parametri)

1. **Voce**: preset Essential Sound Dialogo fisso (compressore 0,8475/0,548/0,695/0,718) + riduzione rumore 5–7%. Voce pulita prima in Enhance Speech v2 (esv2-50p-bg-10p).
2. **Constant Power di 4 frame su ogni taglio voce**, centrato sul taglio (2 frame se il taglio è stretto).
3. **Whoosh + Mister Horse su ogni cambio di blocco** (dopo il hook, a 2,0 s; palco→sede). Whoosh 0,4–0,76 s centrato sul taglio, a circa −5…−14 dB. Il resto sono stacchi secchi.
4. **Censura = bleep −6 dB + glitch 5 frame + snap zoom 4 frame**, tutti sullo stesso frame.
5. **Struttura stop-drop**: riser (fade-in lungo) che finisce sul taglio → **musica in pausa 1–2 s** sulla frase chiave → **boom 2 frame prima** del rientro della musica.
6. **Musica in Remix** a −20…−26 dB, fade-in breve, **fade-out di 2–3 s** in coda, nessun ducking automatico.
7. **Finale**: ultima frase con reverb e taglio netto del livello, sopra un'esterna con speed ramp.
8. **Dopo il drop si taglia sul beat** (7 su 8). Prima del drop comanda la frase.

### Cosa è riusabile in un REEL 9:16 da live
- Formato, sottotitoli Montserrat-Bold 1–2 righe, catena voce, CP di 4 frame, hook provocatorio tolto dal suo punto cronologico.
- Censura bleep+glitch+zoom (è un mini-gancio visivo nei primi secondi).
- Snap zoom di 4 frame e punch-in 224–320% per dare ritmo al live in campo singolo.
- Una sola transizione Mister Horse + whoosh dopo il hook. Stop-drop se c'è una frase-slogan.
- Coda in reverb.

### Cosa è specifico del recap
- B-roll multicamera e DJI (63% delle inquadrature non live), slow motion a 50p, nest+viewfinder, esterne con speed ramp.
- 35 tagli/min (un reel parlato sta intorno a 20) e montaggio sul beat: servono b-roll e musica in primo piano.
- Lumetri shot per shot per pareggiare 3 camere. Seconda transizione "Anchor" per cambiare luogo.
- Montaggio della voce a mosaico da più momenti e più persone (salti fino a 980 s).
