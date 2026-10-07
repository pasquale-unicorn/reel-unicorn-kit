---
name: reel-unicorn
description: Use when someone wants reels, shorts or vertical clips cut from a long Unicorn live/event/university video (2-3 hours) with its transcript, when Mary asks for "bozze di reel", "trova i momenti", "fammi i reel della live", when a reel draft must be delivered as an editable Adobe Premiere sequence, or when Mary hands back a finished Premiere project so the editing style can be learned.
---

# Reel Unicorn

Assistente di montaggio di Mary (videomaker Unicorn). Da una live lunga + trascrizione produce bozze di reel 9:16
**già tagliate e montate in Premiere nel suo stile**, modificabili; Mary rifinisce ed esporta. Obiettivo: da 1 a 10+ reel al giorno.

**Principio:** Claude fa la base, Mary decide. Due cancelli obbligatori: Mary approva i MOMENTI prima del montaggio,
e guarda la BOZZA in Premiere prima che diventi definitiva. Consegna sempre editabile (XML in Premiere), mai video "cotti".

Prima di scrivere qualsiasi testo (hook, caption): skill `unicorn-brand-voice`. Linea rossa: mai cifre di guadagno nei testi scritti.

## Percorsi (usarli sempre così)
- `PY` = `~/.reel-unicorn/venv/bin/python` (ha whisper, opencv, numpy). Mai `python3` di sistema.
- `S` = `~/.claude/skills/reel-unicorn/scripts`
- `W` = **cartella di lavoro** = `<cartella della live>/REEL-LAVORO/`. Tutto ciò che Claude produce va lì (CANDIDATI.md, compatta.txt,
  una sottocartella `reel-<slug>/` per reel con `scheda.json`, XML, seg/). Mai dentro il kit.

## Flusso

| Fase | Cosa | Riferimento |
|---|---|---|
| 0. Setup | Ponte Premiere attivo, progetto aperto, plugin su Connect | `references/premiere-tecnica.md` |
| 0b. Sorgente | `ffprobe` del video: durata, fps, risoluzione (il generatore si adatta da solo) e chiedere a Mary su quale progetto Premiere lavorare | |
| 1. Momenti | `PY S/compatta_trascrizione.py LIVE.md 20 > W/compatta.txt`, letta TUTTA → `W/CANDIDATI.md` (15-20) | `references/momenti-virali.md` |
| — | **STOP: Mary sceglie i momenti** | |
| 2. Scheda | Per ogni momento scelto: `W/reel-<slug>/scheda.json` da `templates/scheda-esempio.json` | sotto |
| 3. Parole | `PY S/trascrivi_finestre.py W/reel-<slug>/scheda.json` (whisper sulle sole finestre) | |
| 4. Bozza | `PY S/reel_xml_mary.py W/reel-<slug>/scheda.json` → XML in `W/reel-<slug>/` | `references/stile-mary.md` |
| 5. Premiere | save_project → import_media (UN xml) → set_active_sequence → export_frame a 4 istanti e guardarli | `references/premiere-tecnica.md` |
| — | **STOP: Mary guarda la bozza** | |
| 6. Impara | Mary salva il reel finito in `impara/progetti/` → analisi → diario e glossario | `references/impara.md` |

**Richieste urgenti** ("8 per stasera"): i due STOP restano, ma brevi. Proporre: lista candidati in 10-15 minuti, Mary sceglie,
poi bozze in sequenza consegnando ognuna appena pronta (non tutte alla fine). Motion graphics mai sotto scadenza.

**Testi scritti** (hook ≤ 8 parole, caption): stanno in `CANDIDATI.md` e in `W/reel-<slug>/caption.md` per la pubblicazione.
Nello stile di Mary NON vanno a schermo: a schermo ci sono solo i sottotitoli.

## Scheda del reel (campi che contano)
- `source`: percorso assoluto del video della live (durata, fps e risoluzione li legge lo script). `windows`: blocchi in secondi
  sorgente, uno per pezzo di discorso (anche separati di minuti), presi dai timecode di CANDIDATI.md con 1 s di margine.
  `cx`,`cy` (facoltativi): pixel sorgente dove sta il formatore, usati solo se il rilevamento del viso fallisce.
  Per `layout: split` servono anche `aud_cx`, `aud_cy` (punto della platea) e `band_scale` (265).
- `hook_src`: [inizio, fine] in secondi sorgente della frase da anticipare in testa (3-5 s). Viene ripetuta al suo posto senza sottotitoli.
- `layout`: `single` (formatore che si muove, default) o `split` (camera fissa + platea sotto). `autoface: true` aggancia il viso clip per clip.
- `music`, `whoosh`, `riser`: file dalla libreria di Mary (Artlist, WAV o MP3). Se mancano, chiederli: niente musica inventata.
  I percorsi della libreria, una volta noti, stanno in `impara/diario.md`.
- `glossary` / `text_fix`: correzioni SOLO di questo reel. Il glossario del kit (`impara/glossario.json`) si applica da solo.
- `name`: nome della sequenza in Premiere, con versione (`REEL farmacista v1`). Ogni reimport = nuova versione.

## Consegna a Mary (messaggio dopo ogni bozza)
Una riga per reel: nome sequenza, durata, numero di clip, gancio usato. Poi cosa resta a lei, sempre lo stesso elenco:
Lumetri (regolato sulla sala), preset voce "Dialogo", dissolvenze audio 4 frame (seleziona clip voce > Cmd+Shift+D), la transizione
Mister Horse sul taglio dopo l'hook (una sola, sempre), controllo sottotitoli, export. Se un frame di controllo mostra un problema (testa tagliata, sottotitolo sbagliato): correggere
la scheda e reimportare come nuova versione PRIMA di consegnare.

## Errori comuni
| Errore | Correzione |
|---|---|
| Leggere la trascrizione a campione | Compattarla e leggerla tutta: i momenti migliori stanno spesso a metà |
| Montare prima che Mary approvi i momenti | Fermarsi a `CANDIDATI.md` |
| Importare più XML insieme | Uno per chiamata, `save_project` prima |
| Sottotitoli con font serif | Font statici Montserrat installati + Premiere riavviato |
| Viso fuori quadro su un punch-in | Ridurre il punch-in di quella clip o correggere `cx/cy`, nuova versione |
| Cifre di guadagno in hook o caption | Toglierle: linea rossa |
| Cambiare `stile-mary.md` dopo un solo reel | Solo dopo 3 conferme o richiesta esplicita di Mary (`references/impara.md`) |
| Aggiungere takeover/motion graphics di default | Solo su richiesta: `references/motion-graphics-plus.md` |
