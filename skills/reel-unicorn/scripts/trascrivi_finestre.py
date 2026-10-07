#!/usr/bin/env python3
"""Trascrizione PRECISA (parola per parola) delle sole finestre scelte di un reel, con whisper.
Legge la scheda JSON (campi source, windows[src_in, src_out]) e scrive seg/<n>.json accanto alla scheda,
aggiornando windows[i].whisper. La trascrizione dell'evento serve a trovare i momenti; questa a tagliare sulle parole.
Uso: python3 trascrivi_finestre.py scheda.json [--model small]"""
import json, os, subprocess, sys, shutil

spec_path = sys.argv[1]; model = sys.argv[sys.argv.index("--model") + 1] if "--model" in sys.argv else "small"
spec = json.load(open(spec_path, encoding="utf-8"))
base = os.path.dirname(os.path.abspath(spec_path)); segdir = os.path.join(base, "seg"); os.makedirs(segdir, exist_ok=True)
whisper = shutil.which("whisper") or os.path.expanduser("~/.reel-unicorn/venv/bin/whisper")
wavs = []
for i, w in enumerate(spec["windows"], 1):
    wav = os.path.join(segdir, f"{spec.get('slug', 'reel')}_w{i}.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(w["src_in"]), "-to", str(w["src_out"]), "-i", spec["source"],
                    "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
    wavs.append(wav); w["whisper"] = wav[:-4] + ".json"
subprocess.run([whisper, *wavs, "--model", model, "--language", "it", "--word_timestamps", "True",
                "--output_format", "json", "--output_dir", segdir, "--verbose", "False"], check=True)
json.dump(spec, open(spec_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok:", [w["whisper"] for w in spec["windows"]])
