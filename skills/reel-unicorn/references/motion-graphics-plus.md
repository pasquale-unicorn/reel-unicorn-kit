# Opzione PLUS: motion graphics (solo su richiesta, 1-2 per reel)

Non è lo stile di Mary: usarle solo se lo chiede, sui numeri o sui concetti più forti.
- Scene HTML animate (HyperFrames, skill `/hyperframes`) renderizzate in MOV ProRes 4444 con trasparenza:
  `npx hyperframes render <cartella> -c scenes2/<scena>.html --format mov -f 24 -o renders2/<scena>.mov`.
- Esempio completo e funzionante: `mg/build_scenes2.py` (takeover: sfondo scuro, Angelo in finestra in alto, grafica sotto;
  contatore, TG, indicatore, busta "pagato", stinger). Font in `mg/fonts/` (il kit li copia lì).
- In Premiere: il generatore `reel_xml2.py` (campi `takeovers`, `overlays`, `stinger`, `sfx`) mette le scene su una traccia sopra
  e anima Angelo dentro la finestra con keyframe. Effetti sonori sintetici in `assets/sfx/` (`make_sfx.py` per rigenerarli).
- Controllo: `mg/preview.py` fa la griglia dei fotogrammi; guardarla sempre prima di importare.

## Come si fa davvero (lavoro su misura, 20-40 min per reel)
1. Copiare `mg/` del kit in `W/reel-<slug>/mg/` (con `fonts/`): `build_scenes2.py` contiene le scene di ESEMPIO del Reel morosità,
   vanno riscritte per il contenuto del nuovo reel (stessa struttura: funzione `page()`, una voce in `S` per scena).
2. `PY build_scenes2.py` → `scenes2/*.html`; render di ogni scena con il comando sopra (cartella = `W/reel-<slug>/mg`).
3. Generatore: `reel_xml2.py` (non `reel_xml_mary.py`) con scheda che ha anche `takeovers`/`overlays`/`stinger`. I due generatori NON
   si combinano: per un reel "Mary + 1 grafica" generare con `reel_xml_mary.py` e chiedere a Mary di trascinare il MOV su V2.
