# Ciclo di miglioramento (il kit impara da Mary)

Il preset vive in `references/stile-mary.md` e nel glossario `impara/glossario.json`. Si aggiorna SOLO con prove, mai a sensazione.

## Dopo ogni reel finito da Mary (2 minuti)
1. Mary salva il progetto Premiere finito (o una sua copia) in `impara/progetti/AAAA-MM-GG-nome.prproj`.
2. Claude lancia `python3 scripts/analizza_prproj.py impara/progetti/<file> --json impara/progetti/<file>.json`.
3. Claude confronta i numeri con la bozza che aveva consegnato (stessa sequenza, versione Claude) e scrive in `impara/diario.md`:
   data, reel, cosa Mary ha cambiato (tagli spostati/aggiunti, clip tolte, scale, sottotitoli corretti, musica), e UNA ipotesi di regola.
4. Le correzioni ai sottotitoli fatte da Mary → `impara/glossario.json` (subito, valgono dal reel successivo).

## Quando una regola entra nel preset
- La stessa correzione compare in **3 reel diversi** → si propone a Mary di metterla in `stile-mary.md` (con data e motivo nello storico).
- Mary dice "fallo sempre così" → entra subito.
- Mai cambiare `stile-mary.md` per un caso singolo.

## Ogni settimana (o quando lo chiede Pasquale)
- Riepilogo da `diario.md`: regole proposte, regole entrate, cosa Mary corregge ancora più spesso.
- Se il kit è in un repository git: commit di `impara/` e `references/` così Pasquale riceve i miglioramenti (e viceversa).
- Quando ci sono le statistiche dei reel pubblicati (salvataggi, condivisioni, % visualizzazione): annotarle in `diario.md` accanto
  all'archetipo; dopo 30 reel si guardano gli archetipi che rendono di più.
