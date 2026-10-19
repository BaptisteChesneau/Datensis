"""Bloque les fichiers sensibles deja suivis par Git."""

import shutil
import subprocess  # noqa: S603
import sys
from pathlib import PurePath

git_executable = shutil.which("git")

if git_executable is None:
    print("Erreur : executable Git introuvable.")
    sys.exit(1)

# Appel controle : executable Git localise et arguments fixes.
result = subprocess.run(  # noqa: S603
    [git_executable, "ls-files", "-z"],
    capture_output=True,
    check=True,
)

paths = [p.decode("utf-8", errors="replace") for p in result.stdout.split(b"\0") if p]

blocked = []

for path in paths:
    filename = PurePath(path).name.lower()

    if filename.endswith((".db", ".sqlite", ".sqlite3")) or filename in {
        ".env",
        ".env.production",
        ".env.local",
    }:
        blocked.append(path)

if blocked:
    print("Fichiers sensibles suivis par Git :", *blocked, sep="\n - ")
    sys.exit(1)

print("Aucune base SQLite ni fichier .env sensible suivi par Git.")
