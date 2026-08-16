#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Courbe l'apostrophe (U+0027 -> U+2019) sur le corpus DESSINE des planches.

    python scripts/apostrophes-planches.py            # controle seul, ne modifie rien
    python scripts/apostrophes-planches.py --appliquer

Pourquoi un second outil a cote de `scripts/injection-typographique.py` : celui-la
est taille pour le Markdown de `src/content/` et applique la typographie ENTIERE
(insecables avant la ponctuation double, autour des guillemets, entre nombre et
unite). Passe tel quel sur les extractions, il change 1 186 signes de plus que
les apostrophes -- et comme les compositeurs mesurent leurs chaines pour poser la
geometrie (`_tronc.mesurer`), chaque insecable ajoutee DEPLACE le dessin. La
session du 2026-08-16 ne courbe donc que l'apostrophe ; les insecables des
extractions restent un chantier a part, qui devra se recetter au rendu.

DEUX CORPUS, DEUX PORTEES :

1. `public/images/projets/*/planche.json` -- l'extraction, texte brut. C'est la
   SOURCE : le site y lit le titre court, le cartouche et l'`aria_label` que les
   lecteurs d'ecran prononcent, et les compositeurs y lisent tout le texte
   dessine. Corriger les SVG serait corriger la sortie ; ils se regenerent.

2. `scripts/planches/*.py` -- le CONTENU des litterales de chaine seulement,
   jamais les delimiteurs. Un compositeur porte deux sortes de prose francaise
   qui atteint la sortie : quelques libelles dessines (« Plans d'execution »)
   et tout le bloc `controles`, que `_tronc.executer` reecrit dans le JSON a
   chaque regeneration. Sans cette passe, la regeneration reintroduirait des
   apostrophes droites dans les extractions qu'on vient de corriger.
   Les docstrings sont laissees : elles documentent la source, elles ne sont
   pas du « contenu destine a l'utilisateur final ».

GARDE-FOU -- une apostrophe n'est courbee que si elle est FRANCAISE : une lettre
a gauche, et a droite une lettre ou un guillemet ouvrant. Tout le reste est
REFUSE et signale, jamais converti en silence. C'est ce qui protege la syntaxe
qui emploie la meme touche : `font-variation-settings="'wdth' 112"` et
`font-family='...'` dans `_tronc.texte`, et les cles de dictionnaire logees dans
une f-string (`f"{d['cle']}"`, ou l'apostrophe touche `[` ou `]`).
"""

import ast
import io
import sys
import tokenize
from pathlib import Path

APO = "’"
RACINE = Path(__file__).resolve().parents[1]


def francaise(gauche, droite):
    """Une elision francaise : lettre a gauche, lettre ou guillemet ouvrant a
    droite (« qu'« air/eau » implique » est dans le corpus)."""
    return gauche.isalpha() and (droite.isalpha() or droite in "«“")


def courber(texte, origine, refus):
    sortie = []
    for i, c in enumerate(texte):
        if c != "'":
            sortie.append(c)
            continue
        gauche = texte[i - 1] if i else ""
        droite = texte[i + 1] if i + 1 < len(texte) else ""
        if francaise(gauche, droite):
            sortie.append(APO)
        else:
            sortie.append(c)
            refus.append((origine, texte[max(0, i - 45):i + 45].replace("\n", " ")))
    return "".join(sortie)


def positions_docstrings(source):
    """Lignes/colonnes des docstrings -- laissees intactes."""
    vues = set()
    for node in ast.walk(ast.parse(source)):
        for champ in ("body", "orelse", "finalbody"):
            corps = getattr(node, champ, None)
            if not isinstance(corps, list):
                continue
            for st in corps:
                if isinstance(st, ast.Expr) and isinstance(st.value, ast.Constant) \
                        and isinstance(st.value.value, str):
                    vues.add((st.value.lineno, st.value.col_offset))
    return vues


def courber_python(source, chemin, refus):
    """Ne touche qu'au CONTENU des jetons STRING, delimiteurs exclus."""
    docs = positions_docstrings(source)
    lignes = source.splitlines(keepends=True)
    remplacements = []
    jetons = tokenize.generate_tokens(io.StringIO(source).readline)
    for jeton in jetons:
        if jeton.type != tokenize.STRING or "'" not in jeton.string:
            continue
        if jeton.start in docs:
            continue
        prefixe = jeton.string[:len(jeton.string) - len(jeton.string.lstrip("rbfuRBFU"))]
        reste = jeton.string[len(prefixe):]
        for delim in ('"""', "'''", '"', "'"):
            if reste.startswith(delim):
                break
        corps = reste[len(delim):-len(delim)]
        neuf = courber(corps, f"{chemin}:{jeton.start[0]}", refus)
        if neuf != corps:
            remplacements.append((jeton.start, jeton.end, prefixe + delim + neuf + delim))

    for (l0, c0), (l1, c1), neuf in reversed(remplacements):
        if l0 != l1:                       # chaine multiligne : on recompose
            avant = lignes[l0 - 1][:c0]
            apres = lignes[l1 - 1][c1:]
            lignes[l0 - 1:l1] = [avant + neuf + apres]
        else:
            ligne = lignes[l0 - 1]
            lignes[l0 - 1] = ligne[:c0] + neuf + ligne[c1:]
    return "".join(lignes)


def main():
    appliquer = "--appliquer" in sys.argv[1:]
    refus = []
    bilan = []

    for chemin in sorted((RACINE / "public" / "images" / "projets").glob("*/planche.json")):
        avant = chemin.read_text(encoding="utf-8")
        apres = courber(avant, str(chemin.relative_to(RACINE)), refus)
        n = avant.count("'") - apres.count("'")
        if n and appliquer:
            io.open(chemin, "w", encoding="utf-8", newline="\n").write(apres)
        bilan.append((chemin.parent.name + "/planche.json", n, apres.count("'")))

    for chemin in sorted((RACINE / "scripts" / "planches").glob("*.py")):
        avant = chemin.read_text(encoding="utf-8")
        apres = courber_python(avant, str(chemin.relative_to(RACINE)), refus)
        n = avant.count("'") - apres.count("'")
        if n and appliquer:
            io.open(chemin, "w", encoding="utf-8", newline="\n").write(apres)
        if n:
            bilan.append((chemin.name, n, -1))

    for nom, n, reste in bilan:
        if n:
            print("%-52s courbees %4d%s" % (nom, n, "" if reste < 0 else "  restantes %d" % reste))
    print("\n%s : %d apostrophes courbees sur %d pieces"
          % ("APPLIQUE" if appliquer else "CONTROLE (rien ecrit)",
             sum(n for _, n, _ in bilan), sum(1 for _, n, _ in bilan if n)))

    if refus:
        print("\n%d apostrophes REFUSEES -- non francaises, laissees telles quelles :" % len(refus))
        for origine, ctx in refus:
            print("   %-40s %s" % (origine, ctx))


if __name__ == "__main__":
    main()
