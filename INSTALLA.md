# Installazione del kit (istruzioni per Claude)

Esegui nell'ordine. Spiega a Mary ogni passo in una riga. Se un passo fallisce, fermati e spiega l'errore in parole semplici.

## Parte A — automatica (Claude)
1. Controlla di essere su macOS e che il kit sia in una posizione stabile (es. `~/Documents/reel-unicorn-kit`, NON in Download o sul
   Desktop se Mary lo pulisce spesso). Se è in Download, proponi di spostarlo prima di installare: i percorsi vengono registrati.
2. Lancia `bash install.sh` dalla cartella del kit (ci mette 5-15 minuti: scarica whisper e alcune librerie).
   - Se dice che manca Homebrew: chiedi a Mary di incollare nel terminale il comando che stampa (le chiede la password del Mac),
     oppure di scrivere nel prompt `! <comando>`. Poi rilancia `bash install.sh`.
3. Lancia `bash install.sh --verifica` e riporta a Mary l'esito: tutte le righe devono essere ✓.
4. Dì a Mary di **chiudere e riaprire Claude Code** (le skill e il server MCP si caricano all'avvio) e **riavviare Premiere** (font).

## Parte B — una volta, con Pasquale (plugin di Premiere)
Claude non può farla da solo: va fatta nell'interfaccia di Adobe. Guida Mary un click alla volta.
1. App **Creative Cloud** > Tutte le app > installa **UXP Developer Tools**.
2. In Premiere: **Impostazioni > Plugin > spunta "Abilita modalità sviluppatore"**, poi riavvia Premiere.
3. Apri **UXP Developer Tools** > **Add Plugin** > scegli `vendor/adb-mcp/uxp/pr/manifest.json` dentro il kit > sulla riga
   "Premiere MCP Agent" clicca **Load**.
4. In Premiere (con un progetto aperto): **Finestra > UXP Plugins > Premiere MCP Agent** > **Connect**.
5. Verifica: chiedi a Claude "controlla Premiere". Claude chiama `get_project_info`: se risponde con il nome del progetto, è fatto.

Ogni volta che Premiere si riapre: UXP Developer Tools > Load, poi Connect nel pannello (30 secondi). Il ponte (proxy) parte da solo.

## Parte C — prova finale (10 minuti)
1. Mary indica una live con trascrizione (.md o .srt).
2. Claude segue la skill `reel-unicorn` fino a `CANDIDATI.md` su una sola ora di live e ne monta UNO.
3. Mary lo guarda in Premiere. Se va, il kit è operativo.

## Libreria di Mary da chiedere alla prima sessione
- Cartella delle musiche Artlist e degli effetti (whoosh "Transition Complex 14", riser, boom): annota i percorsi in
  `impara/diario.md` così Claude li propone in ogni scheda.
- Il preset Lumetri e il preset voce "Dialogo" che usa: restano in Premiere, Claude li cita nella consegna.
