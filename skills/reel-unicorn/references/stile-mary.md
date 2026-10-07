# Stile Mary — preset di montaggio (versione 1, 2026-10-07)

Ricavato da 4 progetti Premiere di Mary (report completi in `impara/REPORT-*.md`). Questo file È il preset: il generatore
`reel_xml_mary.py` ne applica i numeri. Quando Mary corregge un reel, si aggiorna QUI (vedi `impara.md`), con data e motivo.

## Costanti (uguali in tutti i reel)
| Cosa | Valore |
|---|---|
| Formato | 1080x1920, 24 fps (25 nei recap) |
| Durata reel | 45-65 s |
| Ritmo | 20-24 tagli/min, clip mediana 2,0-2,4 s, min 0,3, max ~5 s |
| Pause | tolte: metà dei tagli salta < 1 s di sorgente (tightening). Soglia generatore `gap` 0,3 s |
| Ordine | quasi cronologico; salti grandi solo per cambio argomento |
| Hook | la frase più forte va in testa (3-5 s), poi il reel riparte e la stessa clip torna al suo posto **senza sottotitoli** |
| Transizioni video | tutti tagli secchi. UNA sola transizione (Mister Horse zoom+mirror+blur, 0,5 s) sul taglio dopo l'hook o sui cambi di blocco |
| Sottotitoli | nativi Premiere, Montserrat Bold, 4-5 parole, ~1,4 s, 1-2 righe con a capo a mano, trascrizione corretta a mano. Nessun titolo/callout/forma |
| Voce | Enhance Speech v2 + preset Essential Sound "Dialogo" (stesso compressore in tutti i progetti), gain +5/+8 dB |
| Audio sui tagli | dissolvenza Constant Power 4 frame su OGNI taglio della voce |
| Musica | Artlist, Remix alla durata, livello fisso (-20/-26 dB, da riverificare), nessun ducking, fade-out 2-3 s |
| SFX | 1 whoosh "Transition Complex 14" al 160% sul taglio dell'hook; riser solo a volte, culmina sul taglio |

## Variabili (dipendono dalla ripresa)
| Situazione | Scelta di Mary | Generatore |
|---|---|---|
| Formatore che cammina tra il pubblico | 1 livello, Auto Reframe o pan con keyframe, base 177,78 | `layout: single` + `autoface: true` (viso agganciato per clip) |
| Camera fissa, dialogo con studente in platea | "split": formatore sopra (226), platea sotto (265) | `layout: split` |
| Enfasi | punch-in statici al taglio 213-276 | alternanza 100% / 130% |
| Battuta finale | un solo punch-in forte 274-363 | ultima clip 142% |
| Colore | Lumetri che segue la luce della sala (non preset fisso) | NON passa in XML: Mary lo applica |

## Censura e momenti speciali (dal recap)
- Parolaccia da coprire: bleep -6 dB + glitch 5 frame + zoom rapido 4 frame (100→148%) sullo stesso frame.
- "Stop-drop" sulla frase chiave: riser che finisce sul taglio, ~1,7 s senza musica, boom 2 frame prima del rientro.
- Dopo il rientro della musica si taglia sul beat.

## Cosa Mary NON fa (non aggiungerlo di default)
Takeover a tutto schermo, stinger, SFX sintetici, sottotitoli parola per parola, titoli e callout, zoom animati lenti.
Le motion graphics (`motion-graphics-plus.md`) sono un'opzione su richiesta, 1-2 per reel al massimo.

## Storico modifiche
- v1 2026-10-07: prima versione da 4 progetti (Business Plan sett., Perché lo faccio lug., Tagli lug., Recap 1 lug.).
