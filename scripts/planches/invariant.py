#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Invariant octet à octet des planches déjà publiées.

    python scripts/planches/invariant.py                 # les 6 compositeurs
    python scripts/planches/invariant.py zonage-ssi      # un seul

Rejoue chaque compositeur sur une COPIE HORS DÉPÔT des dossiers publiés et
compare les quatre pièces produites — `planche.svg`, `vignette.svg`,
`appui.svg`, `planche.json` — octet à octet. C'est le seul contrôle qui dise
si les planches en ligne se refabriquent : la date d'un commit n'en est pas un
indicateur (six planches versées le jour de la correction de `_tronc.mesurer`
avaient été composées avant elle).

Le protocole (révision 5, § « Quatre pièges déjà rencontrés ») le demande
AVANT toute greffe d'un mécanisme nouveau, APRÈS la greffe, et APRÈS la
dernière retouche. Il a été réécrit à chaque session depuis N01 ; il vit ici
pour cesser de l'être.

⚠ Un compte d'écarts sur une machine fraîchement clonée ne prouve rien avant
d'avoir vérifié les fins de ligne : `.gitattributes` porte `* text=auto eol=lf`
et c'est lui qui garantit la comparaison (voir `.claude/rules/astro-conventions.md`).
"""
import filecmp
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
PROJETS = RACINE / "public" / "images" / "projets"
PIECES = ("planche.svg", "vignette.svg", "appui.svg", "planche.json")


def dossiers_par_archetype():
    par = {}
    for chemin in sorted(PROJETS.glob("*/planche.json")):
        archetype = json.loads(chemin.read_text(encoding="utf-8"))["archetype"]
        par.setdefault(archetype, []).append(chemin.parent)
    return par


def main(filtre=None):
    par = dossiers_par_archetype()
    if filtre:
        par = {k: v for k, v in par.items() if k == filtre}
        if not par:
            print(f"aucune planche d’archétype « {filtre} »")
            return 1
    base = Path(tempfile.mkdtemp(prefix="invariant-planches-"))
    ok = ko = 0
    try:
        for archetype, dossiers in sorted(par.items()):
            compositeur = RACINE / "scripts" / "planches" / f"{archetype}.py"
            for dossier in dossiers:
                copie = base / archetype / dossier.name
                copie.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(dossier, copie)
                r = subprocess.run([sys.executable, str(compositeur), str(copie)],
                                   capture_output=True)
                if r.returncode:
                    ko += len(PIECES)
                    print(f"ÉCHEC {archetype} / {dossier.name}\n"
                          f"{r.stderr.decode('utf-8', 'replace')[-600:]}")
                    continue
                for piece in PIECES:
                    if filecmp.cmp(dossier / piece, copie / piece, shallow=False):
                        ok += 1
                    else:
                        ko += 1
                        print(f"ÉCART {archetype} / {dossier.name} / {piece}")
            print(f"  {archetype:20s} {len(dossiers)} planche(s)")
    finally:
        shutil.rmtree(base, ignore_errors=True)
    print(f"INVARIANT : {ok}/{ok + ko} pièces identiques octet à octet")
    return 0 if ko == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
