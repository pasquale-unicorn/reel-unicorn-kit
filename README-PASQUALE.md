# Kit Reel Unicorn — note per Pasquale

## Cosa contiene
| Cartella | Cosa |
|---|---|
| `install.sh` | installa tutto su un Mac nuovo (ffmpeg, python+whisper+opencv, font, ponte Premiere, MCP, skill, HyperFrames). `--verifica` controlla soltanto |
| `skills/reel-unicorn/` | la skill: flusso con 2 cancelli (momenti approvati, bozza vista), script, preset stile Mary, tecnica Premiere |
| `skills/clip-factory/`, `skills/unicorn-brand-voice/` | copie incluse (Vyral e Remotion si scaricano dall'installer) |
| `vendor/adb-mcp/` | ponte Claude↔Premiere di Mike Chambers (MIT) **con la nostra correzione** (non si blocca sulle clip di testo) e il launcher `run-pr-mcp.py` |
| `assets/` | font Montserrat statici (OFL), effetti sonori sintetici |
| `impara/` | report sullo stile di Mary, diario, glossario sottotitoli, cartella dove Mary salva i reel finiti |

## Cosa devi fare tu con Mary (una volta, ~20 minuti)
1. Repository privato: https://github.com/pasquale-unicorn/reel-unicorn-kit — invita Mary come collaboratrice (serve il suo username GitHub).
2. Lei apre Claude Code nella cartella e scrive "installa il kit". Il primo pezzo che può chiederle la password è Homebrew.
3. **Parte B di INSTALLA.md insieme**: UXP Developer Tools da Creative Cloud, modalità sviluppatore in Premiere, Load del plugin, Connect.
4. Prova finale su un'ora di live (Parte C).
5. Fatti dare: cartella musiche/effetti Artlist, il suo preset Lumetri e il preset voce. Annotali nel diario.

## Cose da decidere tu
- **Piano Claude di Mary**: una live di 3 ore + 10 reel consuma parecchio. Serve un piano Max o crediti, altrimenti si ferma a metà
  (oggi è successo anche a noi con gli agenti in parallelo).
- **Condivisione dei miglioramenti**: consiglio un repository git privato (GitHub) del kit. Mary fa crescere `impara/` (diario, glossario,
  preset), tu fai crescere gli script: con `git pull` ve li scambiate. Senza repo, ogni miglioramento resta su un solo Mac.
- **Diritti musica**: il kit non contiene musica Artlist (licenza di Mary); usa la sua libreria.

## Come migliora nel tempo
Regola in `skills/reel-unicorn/references/impara.md`: ogni reel finito → analisi automatica (`analizza_prproj.py`) → diario.
Una correzione che si ripete in 3 reel (o che Mary chiede esplicitamente) entra nel preset `stile-mary.md`. Le correzioni ai sottotitoli
entrano subito nel glossario. Fra qualche settimana, con le statistiche dei reel pubblicati, si possono pesare gli archetipi che rendono.

## Limiti noti (onesti)
- Lumetri, preset voce, dissolvenze audio 4 frame, Mister Horse: non passano via XML, restano a Mary (le dissolvenze sono 1 scorciatoia).
- Il plugin UXP va ricaricato a ogni riavvio di Premiere (30 secondi).
- Il viso agganciato è "statico per clip": se Angelo attraversa il palco dentro una clip lunga può uscire dal quadro → Mary sistema o
  attiva Auto Reframe su quella clip.
- Testato su: Premiere 26.5 macOS, evento 18/09/2026 (Reel 2 morosità, sequenza "v9 STILE MARY").
