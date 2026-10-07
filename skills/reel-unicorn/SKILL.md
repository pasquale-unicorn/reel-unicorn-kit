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

## Flusso

| Fase | Cosa | Riferimento |
|---|---|---|
| 0. Setup | Ponte Premiere attivo, progetto aperto, plugin su Connect | `references/premiere-tecnica.md` |
| 1. Momenti | Trascrizione compattata letta TUTTA → `CANDIDATI.md` (15-20) | `references/momenti-virali.md` |
| — | **STOP: Mary sceglie i momenti** | |
| 2. Scheda | Per ogni momento scelto: cartella `reel-<slug>/scheda.json` da `templates/scheda-esempio.json` | sotto |
| 3. Parole | `python3 scripts/trascrivi_finestre.py reel-<slug>/scheda.json` (whisper sulle sole finestre) | |
| 4. Bozza | `python3 scripts/reel_xml_mary.py reel-<slug>/scheda.json` → XML | `references/stile-mary.md` |
| 5. Premiere | save_project → import_media (UN xml) → set_active_sequence → export_frame ×4 e guardarli | `references/premiere-tecnica.md` |
| — | **STOP: Mary guarda la bozza** | |
| 6. Impara | Mary salva il reel finito in `impara/progetti/` → analisi → diario e glossario | `references/impara.md` |

Python: usare `~/.reel-unicorn/venv/bin/python` (ha whisper, opencv, numpy). Gli script stanno in `scripts/` di questa skill.

## Scheda del reel (campi che contano)
- `source`: percorso assoluto del video della live. `windows`: blocchi in secondi sorgente, uno per ogni pezzo di discorso (anche
  separati di minuti). `cx`,`cy`: punto della sorgente dove sta il formatore (fallback se il viso non si trova).
- `hook_src`: [inizio, fine] in secondi sorgente della frase da anticipare in testa (3-5 s). Viene ripetuta al suo posto senza sottotitoli.
- `layout`: `single` (formatore che si muove, default) o `split` (camera fissa + platea sotto). `autoface: true` aggancia il viso clip per clip.
- `music`, `whoosh`, `riser`: file dalla libreria di Mary (Artlist). Se mancano, chiederli: niente musica inventata.
- `glossary` / `text_fix`: correzioni ai sottotitoli. Partire da `impara/glossario.json` del kit.
- `name`: nome della sequenza in Premiere, con versione (`REEL farmacista v1`). Ogni reimport = nuova versione.

## Consegna a Mary (messaggio dopo ogni bozza)
Una riga per reel: nome sequenza, durata, numero di clip, gancio usato. Poi cosa resta a lei, sempre lo stesso elenco:
Lumetri (preset sala), preset voce "Dialogo", dissolvenze audio 4 frame (seleziona clip voce > Cmd+Shift+D), transizione dopo l'hook
se la vuole, controllo sottotitoli, export. Se un frame di controllo mostra un problema (testa tagliata, sottotitolo sbagliato): correggere
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
