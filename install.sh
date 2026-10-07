#!/bin/bash
# Installer del kit Reel Unicorn (macOS). Rilanciabile: salta quello che c'è già.
#   bash install.sh            installa / aggiorna tutto
#   bash install.sh --verifica controlla soltanto e stampa cosa manca
set -u
KIT="$(cd "$(dirname "$0")" && pwd)"
HOME_RU="$HOME/.reel-unicorn"
VENV="$HOME_RU/venv"
ONLY_CHECK=0; [ "${1:-}" = "--verifica" ] && ONLY_CHECK=1
ok()   { printf "  \033[32m✓\033[0m %s\n" "$1"; }
ko()   { printf "  \033[31m✗\033[0m %s\n" "$1"; MISSING=$((MISSING+1)); }
step() { printf "\n\033[1m%s\033[0m\n" "$1"; }
MISSING=0
mkdir -p "$HOME_RU"; echo "$KIT" > "$HOME_RU/kit-path"

step "1/9 Strumenti di base (Homebrew, ffmpeg, node, python, git-lfs)"
if ! command -v brew >/dev/null 2>&1; then
  ko "Homebrew manca. Va installato una volta a mano (chiede la password del Mac):"
  echo '     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
  echo "     poi rilancia: bash install.sh"; exit 1
fi
ok "Homebrew"
# comando:formula brew. Se il comando c'è già (anche installato senza brew) va bene così.
for pair in ffmpeg:ffmpeg node:node git:git git-lfs:git-lfs; do
  c=${pair%%:*}; f=${pair##*:}
  if command -v "$c" >/dev/null 2>&1; then ok "$c"
  elif [ $ONLY_CHECK = 1 ]; then ko "$c"
  else brew install "$f" >/dev/null && ok "$c installato" || ko "$c non installato"; fi
done
git lfs install >/dev/null 2>&1
# Python >= 3.10 (whisper). Preferisce python3.12 di brew, altrimenti quello di sistema se abbastanza recente.
PY=""
for cand in "$(brew --prefix 2>/dev/null)/bin/python3.12" /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 "$(command -v python3)"; do
  [ -x "$cand" ] && "$cand" -c "import sys; sys.exit(0 if (3,10) <= sys.version_info[:2] < (3,14) else 1)" 2>/dev/null && { PY="$cand"; break; }
done
if [ -n "$PY" ]; then ok "python ($PY)"
elif [ $ONLY_CHECK = 1 ]; then ko "python 3.10-3.13"
else brew install python@3.12 >/dev/null && PY="$(brew --prefix python@3.12)/bin/python3.12" && ok "python 3.12 installato" || ko "python"; fi

step "2/9 Ambiente Python (whisper, opencv, numpy, pillow, ponte MCP)"
if [ -x "$VENV/bin/python" ] && "$VENV/bin/python" -c "import whisper, cv2, numpy, PIL, mcp, socketio" 2>/dev/null; then ok "venv pronto ($VENV)"
elif [ $ONLY_CHECK = 1 ]; then ko "venv Python"
else
  "$PY" -m venv "$VENV" && "$VENV/bin/pip" install -q --upgrade pip \
  && "$VENV/bin/pip" install -q openai-whisper opencv-python numpy pillow "mcp<2" python-socketio requests websocket-client fonttools \
  && ok "venv creato" || ko "installazione pacchetti Python fallita"
fi
[ $ONLY_CHECK = 0 ] && "$VENV/bin/python" -c "import whisper; whisper.load_model('small')" >/dev/null 2>&1 && ok "modello whisper 'small' scaricato"

step "3/9 Font Montserrat (statici, servono a Premiere e alle grafiche)"
mkdir -p "$KIT/skills/reel-unicorn/mg/fonts"
for f in "$KIT"/assets/fonts/*.ttf; do
  b=$(basename "$f")
  [ -f "$HOME/Library/Fonts/$b" ] && ok "$b" || { [ $ONLY_CHECK = 1 ] && ko "$b" || { cp "$f" "$HOME/Library/Fonts/" && ok "$b installato"; }; }
  cp "$f" "$KIT/skills/reel-unicorn/mg/fonts/" 2>/dev/null
done

step "4/9 Ponte Claude <-> Premiere (proxy)"
PROXY="$KIT/vendor/adb-mcp/adb-proxy-socket"
if [ -d "$PROXY/node_modules" ]; then ok "dipendenze proxy"; elif [ $ONLY_CHECK = 1 ]; then ko "dipendenze proxy"
else (cd "$PROXY" && npm install --silent --no-audit --no-fund >/dev/null) && ok "dipendenze proxy installate" || ko "npm install proxy"; fi
cat > "$HOME_RU/avvia-ponte.sh" <<EOS
#!/bin/bash
pgrep -f "node proxy.js" >/dev/null || (cd "$PROXY" && nohup node proxy.js > "$HOME_RU/ponte.log" 2>&1 &)
EOS
chmod +x "$HOME_RU/avvia-ponte.sh"
PLIST="$HOME/Library/LaunchAgents/com.unicorn.reel-ponte.plist"
if [ $ONLY_CHECK = 0 ]; then
  mkdir -p "$HOME/Library/LaunchAgents"
  cat > "$PLIST" <<EOS
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>Label</key><string>com.unicorn.reel-ponte</string>
<key>ProgramArguments</key><array><string>$(command -v node)</string><string>$PROXY/proxy.js</string></array>
<key>WorkingDirectory</key><string>$PROXY</string>
<key>RunAtLoad</key><true/><key>KeepAlive</key><true/>
<key>StandardOutPath</key><string>$HOME_RU/ponte.log</string><key>StandardErrorPath</key><string>$HOME_RU/ponte.log</string>
</dict></plist>
EOS
  launchctl unload "$PLIST" >/dev/null 2>&1; launchctl load "$PLIST" >/dev/null 2>&1
fi
sleep 1; pgrep -f "proxy.js" >/dev/null && ok "proxy attivo (parte da solo all'avvio del Mac)" || ko "proxy non attivo (bash $HOME_RU/avvia-ponte.sh)"

step "5/9 Server MCP 'premiere' in Claude Code"
if ! command -v claude >/dev/null 2>&1; then ko "comando 'claude' non trovato"
else
  WANT="$KIT/vendor/adb-mcp/mcp/run-pr-mcp.py"
  if claude mcp get premiere 2>/dev/null | grep -q "$WANT"; then ok "MCP premiere registrato"
  elif [ $ONLY_CHECK = 1 ]; then ko "MCP premiere"
  else
    claude mcp remove premiere -s user >/dev/null 2>&1
    claude mcp add premiere -s user -- "$VENV/bin/python" "$WANT" >/dev/null && ok "MCP premiere registrato" || ko "registrazione MCP"
  fi
fi

step "6/9 Skill del kit (reel-unicorn, clip-factory, unicorn-brand-voice)"
mkdir -p "$HOME/.claude/skills"
for s in reel-unicorn clip-factory unicorn-brand-voice; do
  T="$HOME/.claude/skills/$s"
  if [ -L "$T" ] && [ "$(readlink "$T")" = "$KIT/skills/$s" ]; then ok "$s"
  elif [ $ONLY_CHECK = 1 ]; then ko "$s"
  else
    [ -e "$T" ] && mv "$T" "$T.backup-$(date +%Y%m%d%H%M%S)"
    ln -s "$KIT/skills/$s" "$T" && ok "$s collegata"
  fi
done

step "7/9 Skill esterne (modelli virali Vyral, Remotion)"
if [ -d "$HOME/.claude/skills/viral-hooks" ]; then ok "viral-* (Vyral)"; elif [ $ONLY_CHECK = 1 ]; then ko "viral-* (Vyral)"
else npx -y skills add vyralcontent/content-skills -g -a claude-code -y >/dev/null 2>&1 && ok "viral-* installate" || ko "skill Vyral"; fi
if [ -d "$HOME/.claude/skills/remotion-best-practices" ]; then ok "remotion-*"; elif [ $ONLY_CHECK = 1 ]; then ko "remotion-*"
else npx -y skills add remotion-dev/skills -g -a claude-code -y >/dev/null 2>&1 && ok "remotion-* installate" || ko "skill Remotion"; fi

step "8/9 HyperFrames (motion graphics opzionali)"
if claude plugin list 2>/dev/null | grep -q "hyperframes@hyperframes"; then ok "plugin HyperFrames"
elif [ $ONLY_CHECK = 1 ]; then ko "plugin HyperFrames"
else
  GIT_LFS_SKIP_SMUDGE=1 claude plugin marketplace add heygen-com/hyperframes >/dev/null 2>&1
  claude plugin install hyperframes@hyperframes --scope user >/dev/null 2>&1 && ok "plugin HyperFrames" || ko "plugin HyperFrames"
  npx -y hyperframes browser ensure >/dev/null 2>&1 && ok "browser di render HyperFrames"
fi

step "9/9 Glossario e cartelle di apprendimento"
[ -f "$KIT/impara/glossario.json" ] && ok "glossario" || ko "impara/glossario.json"
mkdir -p "$KIT/impara/progetti"; ok "impara/progetti"

echo
if [ $MISSING = 0 ]; then
  printf "\033[32mTutto pronto.\033[0m Ultimo passo (una volta, con Pasquale): plugin UXP in Premiere, vedi INSTALLA.md parte B.\n"
  echo "Poi chiudi e riapri Claude Code e Premiere."
else
  printf "\033[31m%s cose da sistemare\033[0m (vedi le righe con ✗).\n" "$MISSING"
fi
