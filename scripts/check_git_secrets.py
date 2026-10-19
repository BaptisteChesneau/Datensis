"""Bloque les fichiers sensibles deja suivis par Git."""

import subprocess
import sys

result = subprocess.run(["git", "ls-files", "-z"], capture_output=True, check=True)
paths = [p.decode("utf-8", errors="replace") for p in result.stdout.split(b"\0") if p]
blocked = [
    p
    for p in paths
    if p.endswith((".db", ".sqlite", ".sqlite3"))
    or p.split("/")[-1] in {".env", ".env.production", ".env.local"}
]
if blocked:
    print("Fichiers sensibles suivis par Git :", *blocked, sep="\n - ")
    sys.exit(1)
print("Aucune base SQLite ni fichier .env sensible suivi par Git.")
