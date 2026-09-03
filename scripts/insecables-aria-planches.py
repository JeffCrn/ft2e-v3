#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pose la typographie d'espacement française sur les `aria_label` des planches.

    python scripts/insecables-aria-planches.py             # contrôle seul, ne modifie rien
    python scripts/insecables-aria-planches.py --appliquer

PORTÉE — un seul champ, et ce n'est pas une timidité
====================================================
Le corpus dessiné porte trois populations de texte, et une seule est corrigeable
aujourd'hui :

1. `aria_label` — CE QUE CE SCRIPT TRAITE. Jamais dessiné : `_tronc.entete_appui`
   et les six compositeurs ne l'écrivent qu'en attribut `aria-label=` sur la
   racine SVG, et `PlancheReference.astro` le pose en `aria-label` sur le
   conteneur de la vignette (qui est `aria-hidden` à la source). Aucun appel à
   `_tronc.mesurer` ne le touche : **aucune géométrie n'en dépend.**

2. le texte DESSINÉ (`titre`, `surtitre`, libellés, cotes…) — HORS PORTÉE. Les
   compositeurs mesurent ces chaînes pour poser la géométrie, et U+202F n'a pas
   la chasse d'une espace ordinaire (`_tronc.mesurer` distingue FINE, INSEC et
   l'avance courante). Chaque insécable ajoutée DÉPLACE le dessin, ce qui
   demande une recette au rendu aux trois tailles. Chantier à part.

3. les champs éditoriaux (`archetype_motif`, `a_valider_ft2e`,
   `exclusions_appliquees`, `controles*`) — HORS PORTÉE. Ils ne sortent jamais
   du dépôt : les corriger ne change rien pour personne, et `controles*` est
   réécrit par `_tronc.executer` à chaque régénération.

C'est aussi pourquoi ce script n'a PAS de passe sur `scripts/planches/*.py`, à
la différence de `apostrophes-planches.py` : un compositeur ne fabrique jamais
d'`aria_label`, il ne fait que le relire. Rien ne peut le réintroduire fautif.

DEUX GESTES, PAS UN — et c'est le second qui manquait au relevé précédent
=========================================================================
Le script AJOUTE les insécables manquantes, et il NORMALISE celles qui sont
posées au mauvais caractère. Le second geste est nécessaire parce que le motif
canonique de `injection-typographique.py` cherche `[ ]`, une espace ORDINAIRE
littérale : une U+202F déjà posée devant un « : » lui est invisible, et passe
donc tout contrôle sans être conforme. Relevé au 2026-09-03 sur les 47
dossiers — 18 fines devant une ponctuation double, contre 5 insécables justes.

La règle départage, et c'est celle du dépôt (`.claude/rules/french-editorial.md`) :

    U+00A0  avant  :  ;  !  ?   et autour des guillemets « »
    U+202F  entre un nombre et son unité, et en séparateur de milliers

⚠ Les unités ne sont PAS retapées ici : elles sont importées de
`scripts/injection-typographique.py`, qui reste la source de vérité du lexique.
Seule la classe d'espaces est élargie, pour normaliser autant qu'ajouter. Une
liste d'unités recopiée divergerait au premier ajout — c'est le défaut qu'a
connu le lexique de `releve-numeral.py`, trois fois de suite.

⚠ AUCUNE INSÉCABLE N'EST ÉCRITE EN LITTÉRAL DANS CE FICHIER. Les outils
d'écriture normalisent U+00A0 et U+202F de façon NON DÉTERMINISTE : elles sont
construites par `chr()`, et le contrôle final est une assertion CALCULÉE
(relecture du fichier écrit, comparaison à la chaîne attendue), jamais un
nombre tapé à la main.
"""

import importlib.util
import io
import json
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
PROJETS = RACINE / "public" / "images" / "projets"

NBSP = chr(160)     # U+00A0 — espace insécable
NNBSP = chr(8239)   # U+202F — espace fine insécable


def moteur_canonique():
    """Charge `injection-typographique.py` SANS déclencher sa boucle de tête.

    Le module traite `sys.argv[1:]` au chargement : importé tel quel depuis un
    script lancé avec `--appliquer`, il tenterait d'ouvrir « --appliquer »
    comme un fichier. On neutralise l'argv le temps de l'exécution.
    """
    sauve = sys.argv
    sys.argv = [sys.argv[0]]
    try:
        spec = importlib.util.spec_from_file_location(
            "injection_typographique", RACINE / "scripts" / "injection-typographique.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        sys.argv = sauve


INJ = moteur_canonique()

# La classe d'espaces est ÉLARGIE aux trois formes : une fine mal placée doit
# être vue pour être corrigée. C'est la seule différence avec les motifs du
# moteur canonique, dont le lexique d'unités est réutilisé tel quel.
ESP = " " + NBSP + NNBSP
RE_PONCT = re.compile("[" + ESP + "]([;:!?])")
RE_GUILLEMET_OUVRANT = re.compile("«[" + ESP + "]")
RE_GUILLEMET_FERMANT = re.compile("[" + ESP + "]»")
RE_MILLE = re.compile(r"(\d)[" + ESP + r"](\d{3})(?!\d)")
RE_UNITE = re.compile(r"(\d)[" + ESP + r"](" + "|".join(INJ.UNITES) + r")(?![A-Za-zÀ-ÿ0-9])")


def typographier(texte):
    """Les seules règles d'ESPACEMENT. Ni courbure d'apostrophe (déjà passée le
    2026-08-16), ni protections Markdown (backticks, clés YAML) : un `aria_label`
    n'est ni du Markdown ni du YAML."""
    texte = RE_PONCT.sub(NBSP + r"\1", texte)
    texte = RE_GUILLEMET_OUVRANT.sub("«" + NBSP, texte)
    texte = RE_GUILLEMET_FERMANT.sub(NBSP + "»", texte)
    for _ in range(3):          # « 1 200 000 » : deux passes utiles, la 3e est un filet
        texte = RE_MILLE.sub(r"\1" + NNBSP + r"\2", texte)
    texte = RE_UNITE.sub(r"\1" + NNBSP + r"\2", texte)
    return texte


def ventiler(avant, apres):
    """Ce que la correction a fait, par nature — un total qui ne se décompose
    pas n'est pas une mesure."""
    v = {"ajoutees": 0, "normalisees": 0}
    for a, b in zip(avant, apres):
        if a == b:
            continue
        v["ajoutees" if a == " " else "normalisees"] += 1
    return v


def main(appliquer):
    dossiers = sorted(d for d in PROJETS.iterdir() if (d / "planche.json").is_file())
    total = {"ajoutees": 0, "normalisees": 0}
    touches, sans_champ = [], []

    for dossier in dossiers:
        chemin = dossier / "planche.json"
        donnees = json.loads(chemin.read_text(encoding="utf-8"))
        avant = donnees.get("aria_label")
        if not isinstance(avant, str):
            sans_champ.append(dossier.name)
            continue

        apres = typographier(avant)
        if apres == avant:
            continue

        v = ventiler(avant, apres)
        total["ajoutees"] += v["ajoutees"]
        total["normalisees"] += v["normalisees"]
        touches.append((dossier.name, v))

        if not appliquer:
            continue

        donnees["aria_label"] = apres
        # Format identique à `_tronc.executer` : la régénération qui suit
        # réécrira le fichier, un format divergent ferait un diff parasite.
        io.open(chemin, "w", encoding="utf-8", newline="\n").write(
            json.dumps(donnees, ensure_ascii=False, indent=2) + "\n")

        # ASSERTION CALCULÉE — on relit le fichier écrit et on le compare à la
        # chaîne attendue, caractère par caractère. Un compte tapé à la main ne
        # prouverait rien : c'est la relecture qui atteste que `json.dumps` a
        # bien écrit les insécables en littéral (`ensure_ascii=False`) et que
        # rien ne les a normalisées en chemin.
        relu = json.loads(chemin.read_text(encoding="utf-8"))["aria_label"]
        if relu != apres:
            raise SystemExit(
                f"ÉCHEC D'ÉCRITURE sur {dossier.name} : la relecture diffère de "
                f"la chaîne attendue.\n  attendu {apres!r}\n  relu    {relu!r}")

    print(f"{len(dossiers)} dossiers · {len(touches)} porteurs d'un écart")
    print(f"  insécables AJOUTÉES    (espace ordinaire → insécable) : {total['ajoutees']:4d}")
    print(f"  insécables NORMALISÉES (mauvais caractère → le bon)   : {total['normalisees']:4d}")
    print("  " + "-" * 56)
    print(f"  TOTAL {sum(total.values())}")
    if sans_champ:
        print(f"\n/!\\ {len(sans_champ)} dossier(s) SANS `aria_label` : {', '.join(sans_champ)}")

    if appliquer:
        # Contrôle global : plus aucun écart ne doit subsister sur le disque.
        restant = sum(
            sum(1 for a, b in zip(t, typographier(t)) if a != b)
            for t in (json.loads((d / "planche.json").read_text(encoding="utf-8"))
                      .get("aria_label", "") for d in dossiers))
        print(f"\nCONTRÔLE APRÈS ÉCRITURE : {restant} écart(s) restant(s)")
        if restant:
            raise SystemExit("le corpus n'est pas convergent — voir ci-dessus")
        print("appliqué. /!\\ RÉGÉNÉRER les planches : l'`aria-label` des SVG en dépend.")
    else:
        for nom, v in sorted(touches, key=lambda x: -sum(x[1].values()))[:12]:
            print(f"    {sum(v.values()):3d}  {nom}")
        print("\n(contrôle seul — rien n'a été écrit ; --appliquer pour corriger)")

    return 0


if __name__ == "__main__":
    sys.exit(main("--appliquer" in sys.argv[1:]))
