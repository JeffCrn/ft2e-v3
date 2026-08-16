#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tronc commun des compositeurs de planches.

Protocole : docs/superpowers/specs/2026-08-12-planches-references-protocole.md

Ce module porte tout ce que les compositeurs d'archétype partageaient par
copie : jetons, gabarits, avances calibrées, insécables, primitives SVG à
double écriture des couleurs, et la routine d'exécution. Il a été extrait le
2026-08-13, après que le même bloc a été recopié quatre fois — la porte de
contrôle de l'extraction a été la régénération des quatre planches publiées,
comparées octet à octet à leur version d'avant.

Un compositeur l'importe ainsi (le répertoire du script est sur `sys.path`) :

    from _tronc import (JETON, MARGE, UTILE, ..., texte, rect, executer)

et ne garde chez lui que la géométrie de son archétype.
"""

import io
import json
import sys
from pathlib import Path

NN = " "   # espace fine insécable — texte courant et mono
INS = " "  # espace insécable normale — relevés en grand corps

# ── Gabarit (protocole rév. 4) ────────────────────────────────────────────────
W, H = 1200, 800
MARGE = 56
MODULE = 28
UTILE = W - 2 * MARGE                      # 1088

# ── Gabarit de la VIGNETTE ────────────────────────────────────────────────────
VW, VH = 300, 200
V_MARGE = 14

# ── Gabarit de l'APPUI (hero de l'accueil) ───────────────────────────────────
# La colonne média du hero (lg:col-span-6 d'une grille de 1200) lit le dessin à
# ~552 px : le repère fait 552 x 368 (3:2 exact) pour que l'échelle de rendu
# vaille 1,0 — les corps écrits ici sont les corps lus, comme pour la planche.
# Ni la planche (0,48 : mono à 4,8 px) ni la vignette agrandie (1,84 : traits
# épaissis) ne se transposent — l'appui est une TROISIÈME composition, tirée de
# la même extraction, de densité intermédiaire : le motif entier, deux ou trois
# nœuds chiffrés, un surtitre. Sans phrase de principe ni cartouche : le hero
# porte déjà sa légende de carte sous le dessin.
AW, AH = 552, 368
A_MARGE = 24

# ── Jetons ────────────────────────────────────────────────────────────────────
# ⚠ Cette table est le MIROIR du bloc `@theme` de `src/styles/global.css`, et
# elle est nécessaire : une planche est lue hors du site (PNG de contrôle,
# impression, `og:image`), donc elle ne peut pas résoudre `var(--color-…)`.
# Conséquence : une révision de charte se répercute ICI AUSSI, et les 23 dossiers
# se régénèrent — sans quoi le site et ses dessins divergeraient en silence.
JETON = {
    "profond": "#001718",
    "encre": "#00393A",
    "pivot": "#336667",
    "clair": "#99CCCD",
    "voile": "#E1F4F4",
    "papier": "#F7F9FA",
    "calcaire": "#EDF0F2",
    "filet-1": "#00393A38",
    "filet-2": "#00393A29",
    "filet-3": "#00393A1F",
}

SANS = '"Archivo Variable", Archivo, "Helvetica Neue", Arial, sans-serif'
MONO = '"IBM Plex Mono", ui-monospace, monospace'

# Avances CALIBRÉES au rendu navigateur (getBBox) sur la première planche.
AVANCE = {
    "sans-400": 0.500,   # Archivo Variable wdth 100 / 400 — 0,500 majore, repli prudent
    "sans-600": 0.480,   # wdth 112 / 600
    "sans-700": 0.596,   # wdth 118 / 700, chiffres tabulaires — mesuré 23,84 px à 40 px
    "mono": 0.600,       # IBM Plex Mono, chasse fixe
}
FINE = 0.098               # U+202F dans Archivo — mesuré 3,93 px à 40 px
INSEC = 0.196              # U+00A0 — mesuré 7,85 px à 40 px


def mesurer(t, corps, profil="sans-400", tracking=0.0):
    """Largeur d'une chaîne, aux avances calibrées ci-dessus.

    En MONO, toutes les avances sont égales — les deux insécables comprises :
    une police à chasse fixe ne connaît pas la fine. Les compter aux largeurs
    d'Archivo (0,098 et 0,196 em) sous-mesure toute chaîne mono qui porte un
    groupement de chiffres ou une unité : 5,5 px de moins sur un cartouche de
    30 signes, ce qui rogne d'autant sa réserve profonde et rend permissif tout
    contrôle de dépassement portant sur une ligne mono. Relevé au rendu de la
    planche 21, où le dernier chiffre du millésime tombait hors du cartouche.
    """
    a = AVANCE[profil]
    if profil == "mono":
        return a * corps * len(t) + tracking * max(len(t) - 1, 0)
    l = 0.0
    for c in t:
        if c == NN:
            l += FINE
        elif c == INS:
            l += INSEC
        else:
            l += a
    return l * corps + tracking * max(len(t) - 1, 0)


def replier(t, corps, largeur, profil="sans-400"):
    """Découpe un libellé sur la largeur disponible, au dernier espace qui tient."""
    if mesurer(t, corps, profil) <= largeur:
        return [t]
    mots, lignes, courante = t.split(" ", ), [], ""
    for m in mots:
        essai = f"{courante} {m}".strip()
        if courante and mesurer(essai, corps, profil) > largeur:
            lignes.append(courante)
            courante = m
        else:
            courante = essai
    if courante:
        lignes.append(courante)
    return lignes


def echapper(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def texte(x, y, contenu, police, corps, graisse, couleur,
          wdth=None, ancre=None, tracking=None, tabulaire=False):
    """Un nœud de texte. La couleur est écrite DEUX FOIS : classe `var()` pour le
    navigateur, attribut hexadécimal pour le moteur de rendu de contrôle."""
    fam = MONO if police == "mono" else SANS
    cls = f"t-{'mono' if police == 'mono' else 'sans'} c-{couleur}"
    a = [f'x="{x:.2f}"', f'y="{y:.2f}"', f'class="{cls}"',
         f'fill="{JETON[couleur]}"', f'font-family=\'{fam}\'',
         f'font-size="{corps}"', f'font-weight="{graisse}"']
    if wdth is not None:
        a.append(f"font-variation-settings=\"'wdth' {wdth}, 'wght' {graisse}\"")
    if tracking:
        a.append(f'letter-spacing="{tracking:.2f}"')
    if ancre:
        a.append(f'text-anchor="{ancre}"')
    if tabulaire:
        a.append('font-variant-numeric="tabular-nums"')
    return f'  <text {" ".join(a)}>{echapper(contenu)}</text>'


def rect(x, y, w, h, couleur):
    return (f'  <rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
            f'class="c-{couleur}" fill="{JETON[couleur]}"/>')


def rect_bord(x, y, w, h, fond, filet):
    """Bloc à fond opaque + filet 1 px. Le rang du filet est porté par
    l'opacité (filet-1 porteur, filet-2 plan, filet-3 indication)."""
    return (f'  <rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
            f'class="c-{fond} s-{filet}" fill="{JETON[fond]}" '
            f'stroke="{JETON[filet]}" stroke-width="1"/>')


def ligne(x0, y0, x1, y1, cle, epaisseur=1.0):
    return (f'  <path d="M {x0:.2f} {y0:.2f} L {x1:.2f} {y1:.2f}" fill="none" '
            f'class="s-{cle}" stroke="{JETON[cle]}" '
            f'stroke-width="{epaisseur}"/>')


def polyligne(points, cle, epaisseur=1.0):
    d = "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in points)
    return (f'  <path d="{d}" fill="none" class="s-{cle}" '
            f'stroke="{JETON[cle]}" stroke-width="{epaisseur}"/>')


def fleche(x, y, cle, direction="droite", taille=9.0):
    """Pointe de flèche, l'apex en (x, y)."""
    t, d = taille, taille / 2
    if direction == "droite":
        pts = [(x, y), (x - t, y - d), (x - t, y + d)]
    elif direction == "gauche":
        pts = [(x, y), (x + t, y - d), (x + t, y + d)]
    elif direction == "haut":
        pts = [(x, y), (x - d, y + t), (x + d, y + t)]
    else:  # bas
        pts = [(x, y), (x - d, y - t), (x + d, y - t)]
    d_attr = "M " + " L ".join(f"{px:.2f} {py:.2f}" for px, py in pts) + " Z"
    return f'  <path d="{d_attr}" class="c-{cle}" fill="{JETON[cle]}"/>'


def cercle(cx, cy, r, fond, filet, epaisseur=1.5):
    return (f'  <circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" '
            f'class="c-{fond} s-{filet}" fill="{JETON[fond]}" '
            f'stroke="{JETON[filet]}" stroke-width="{epaisseur}"/>')


def entete_style(A, strokes=("filet-1", "filet-2", "filet-3", "encre", "clair")):
    """Le bloc `<style>` : chaque couleur en `var()` doublée de l'hexadécimal.
    `strokes` liste les classes de trait que la planche emploie réellement."""
    A("<style>")
    for cle, hexa in JETON.items():
        A(f"  .c-{cle} {{ fill: var(--color-{cle}, {hexa}); }}")
    for cle in strokes:
        A(f"  .s-{cle} {{ stroke: var(--color-{cle}, {JETON[cle]}); }}")
    A(f"  .t-sans {{ font-family: {SANS}; }}")
    A(f"  .t-mono {{ font-family: {MONO}; }}")
    A("</style>")


def racine_appui(A, donnees, strokes=("filet-1", "filet-2", "filet-3",
                                      "encre", "clair")):
    """L'ouverture commune d'un appui : racine `role="img"` (le hero l'affiche
    seul, sa légende de carte ne décrit pas le principe), fond papier, et le
    surtitre court de l'extraction (`vignette_surtitre` — le surtitre complet
    de la planche ne tient pas toujours dans 504 px)."""
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {AW} {AH}" '
      f'preserveAspectRatio="xMidYMid meet" role="img" '
      f'style="width:100%;height:auto;display:block" '
      f'aria-label="{echapper(donnees["aria_label"])}">')
    entete_style(A, strokes)
    A(rect(0, 0, AW, AH, "papier"))
    A(texte(A_MARGE, 34, donnees["vignette_surtitre"], "mono", 11, 500,
            "pivot", tracking=11 * 0.14))


def controles_appui(motif, bas, **extra):
    """Le bloc de contrôle commun des appuis — gabarit, échelle, corps minimal."""
    base = {
        "gabarit": f"{AW} x {AH} — rapport {AW/AH:.4f} (3:2 exact)",
        "echelle_de_rendu": "colonne média du hero mesurée à ~552 px — "
                            f"échelle {552/AW:.2f} : les corps écrits sont les corps lus",
        "corps_minimal": "10 px dans le repère — rendu à 10 px (échelle 1,0)",
        "motif": motif,
        "bas_du_dessin": bas,
    }
    base.update(extra)
    return base


def executer(composer, composer_vignette, composer_appui=None):
    """Routine d'exécution commune : lit `planche.json` dans le dossier passé
    en argument, écrit les deux (ou trois) SVG, recalcule le bloc `controles`."""
    dossier = Path(sys.argv[1])
    donnees = json.loads((dossier / "planche.json").read_text(encoding="utf-8"))
    svg, controles = composer(donnees)

    io.open(dossier / "planche.svg", "w", encoding="utf-8", newline="\n").write(svg)

    vignette, controles_vignette = composer_vignette(donnees)
    io.open(dossier / "vignette.svg", "w", encoding="utf-8", newline="\n").write(vignette)

    donnees["controles"] = controles
    donnees["controles_vignette"] = controles_vignette

    if composer_appui is not None:
        appui, controles_appui = composer_appui(donnees)
        io.open(dossier / "appui.svg", "w", encoding="utf-8", newline="\n").write(appui)
        donnees["controles_appui"] = controles_appui

    io.open(dossier / "planche.json", "w", encoding="utf-8", newline="\n").write(
        json.dumps(donnees, ensure_ascii=False, indent=2) + "\n")

    print(f"planche.svg  — {len(svg.encode('utf-8'))} octets, "
          f"{svg.count('<text')} nœuds de texte")
    print(f"vignette.svg — {len(vignette.encode('utf-8'))} octets, "
          f"{vignette.count('<text')} nœuds de texte")
    if composer_appui is not None:
        print(f"appui.svg    — {len(appui.encode('utf-8'))} octets, "
              f"{appui.count('<text')} nœuds de texte")
        for k, v in controles_appui.items():
            print(f"  · appui · {k} : {v}")
    for k, v in controles_vignette.items():
        print(f"  · vignette · {k} : {v}")
    for k, v in controles.items():
        print(f"  · {k} : {v}")
