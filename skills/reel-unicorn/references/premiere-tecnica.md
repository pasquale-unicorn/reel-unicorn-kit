# Premiere: come Claude ci lavora (verificato su Premiere 26.5 macOS)

## Ponte Claude ↔ Premiere (ogni sessione)
1. Proxy: `pgrep -f "node proxy.js"`. Se spento: `bash ~/.reel-unicorn/avvia-ponte.sh` (il kit lo installa anche all'avvio del Mac).
2. Premiere aperto con un progetto. Pannello **Finestra > UXP Plugins > Premiere MCP Agent > Connect**
   (se il pannello non c'è: UXP Developer Tools > Load del plugin `vendor/adb-mcp/uxp/pr/manifest.json`).
3. In Claude: leggere la risorsa MCP `config://get_instructions` del server `premiere`, poi `get_project_info`.
   Se risponde "Could not connect": il pannello non è su Connect. Se "Cannot read properties of null (reading 'name')": plugin
   non aggiornato, ricaricarlo da UXP Developer Tools (il kit ne contiene una versione corretta).
4. Le risposte dei tool sono enormi (tutto il progetto): leggerle con un piccolo script Python sul file salvato, cercando solo la sequenza che serve.

## Regole d'oro
- `save_project` PRIMA di ogni `import_media`. **Un XML per chiamata** (tre insieme = crash).
- Nome sequenza = nome nell'XML. Reimportare con lo stesso nome = duplicato: usare v2, v3...
- `export_frame` scrive in `percorso.png.png` se il nome finisce in .png: dare il percorso e cercare il file reale.
- Dopo l'import: `set_active_sequence` + 3-4 `export_frame` e GUARDARLI (testa tagliata? sottotitoli visibili? bande nere?).
- Il MCP NON sa: cancellare/rinominare item, keyframe, testi, Lumetri, Essential Sound, velocità. Tutto questo va nell'XML o lo fa Mary.

## XML xmeml: cosa passa (calibrato)
- Sequenza 1080x1920 dall'XML. Clip sorgente 1920x1080 con filtro Basic Motion: Scala e Centro (anche con keyframe).
- **Unità del Centro**: frazione delle dimensioni NATIVE della clip. Video 1920x1080: px_x = horiz×1920, px_y = vert×1080.
  Grafica/testo 1080x1920: px_y = vert×1920. Positivo = verso destra/basso. Scala 177,78 = altezza piena del 9:16.
- **Testi nativi** (Grafica essenziale, modificabili): effetto `GraphicAndType`, parametro Source Text = 8 byte + JSON UTF-16LE in base64
  (`text_data()` in reel_xml2.py). Font per nome PostScript: serve il font STATICO installato (Montserrat-Bold/Black/ExtraBold) e
  Premiere va **riavviato** dopo aver installato un font, altrimenti usa un serif di ripiego.
- Le clip di una traccia devono essere in ordine di tempo, altrimenti Premiere ne perde qualcuna.
- Volume clip: filtro "Audio Levels" lineare (1 = 0 dB).
- MOV ProRes 4444 con trasparenza (motion graphics HyperFrames) si importano come clip normali su una traccia sopra.
- NON passano: Lumetri, Essential Sound, Auto Reframe, transizioni Mister Horse, Remix musica, sottotitoli come caption track.
  Le dissolvenze audio di 4 frame si possono aggiungere a mano: seleziona tutte le clip audio voce > Cmd+Shift+D (con durata
  predefinita impostata a 4 frame in Preferenze > Timeline).

## Sottotitoli e whisper
- Whisper spezza "l 'affitto", "50 %", "12 .000": il generatore li riattacca. Errori di trascrizione → `glossary` (parola) e
  `text_fix` (frase) nella scheda. Ogni correzione nuova va anche in `impara/glossario.json` così non si ripete.
