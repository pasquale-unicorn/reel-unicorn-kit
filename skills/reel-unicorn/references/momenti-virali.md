# Fase 1 — trovare i momenti (metodo validato)

Validato alla cieca sull'evento del 18/09/2026: ritrovati tutti i reel scelti a mano + nuovi candidati buoni.

## Procedura
1. `python3 scripts/compatta_trascrizione.py TRASCRIZIONE.md 20 > compatta.txt` e **leggere TUTTO**, a pezzi. Mai a campione.
2. Metodo **clip-factory** (skill installata): cercare ARCHI completi, non frasi isolate: affermazione che sorprende, storia con svolta,
   disaccordo forte, un punto di una lista, picco emotivo CON il suo setup (controllare i 30 s prima).
3. Etichettare ogni candidato con un archetipo Unicorn:
   **Operazione chiusa · Mito sfatato · Numero che fa male · Confessione · Manifesto ribelle** (quest'ultimo col contagocce).
   Formato domanda-risposta formatore/studente: la domanda o l'errore dello studente è spesso il gancio.
4. Punteggio 0-100 (rubrica claude-shorts): gancio 30 · sta in piedi da solo 25 · emozione 20 · densità di valore 15 · risultato finale 10.
   Sotto 60 si scarta. Il punteggio ordina, non decide: decide Mary.
5. Per il gancio usare le skill `viral-hooks` e `viral-short-form` (archetipi, "togli le prime due frasi, il gancio è la terza").
6. **Honesty gate**: scartare sarcasmo, ipotesi, battute presentate come affermazioni serie, frasi che fuori contesto tradiscono Angelo.
7. **Linea rossa Unicorn** (skill `unicorn-brand-voice`): MAI cifre di guadagno in testi scritti (hook, caption, grafiche).
   Nel parlato vanno bene. Parolacce: ok nel parlato (o censura stile Mary), mai nei testi.
8. Regole di forma: 30-60 s, Angelo/formatore in camera (non slide, non video proiettati, non altri relatori se non richiesti), max ~6 blocchi.
9. Momenti vicini (< 2 min) non nella stessa settimana: segnalarli o farne "parte 2".

## Output: `CANDIDATI.md` nella cartella di lavoro
Tabella ordinata (n, titolo, in–out, durata, archetipo, punteggio, perché in una riga), poi per ogni candidato:
blocchi con timecode e verbatim, frase-gancio da anticipare (hook_src), hook scritto (≤ 8 parole, niente cifre di guadagno),
caption, rischi (linea rossa / contesto). In fondo: scartati all'honesty gate.

**STOP: Mary approva i candidati sul MESSAGGIO prima di qualsiasi montaggio.** Obiettivo: 15-20 candidati per 2-3 ore di live.
