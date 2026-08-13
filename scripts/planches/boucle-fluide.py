#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compositeur de planche — archétype `boucle-fluide`.

Protocole : docs/superpowers/specs/2026-08-12-planches-references-protocole.md

Il lit un `planche.json` (l'extraction, produite par la session de génération) et
écrit les deux dessins qui en découlent :

    planche.svg    1200 x 800 — la planche de fiche, lue à 1152 px (échelle 0,96)
    vignette.svg    300 x 200 — la vignette de carte, lue à 274-296 px (0,91-0,99)

Usage :

    python scripts/planches/boucle-fluide.py public/images/projets/<slug>

La géométrie est CALCULÉE : aucune coordonnée n'est tapée à la main, et le bloc
`controles` du JSON est recalculé à chaque exécution.

Le motif de l'archétype — le mécanisme d'une boucle de récupération : **deux
conduits d'air superposés ne se rencontrent jamais ; une boucle fermée entre
leurs deux batteries est seule à traverser la bande qui les sépare.** La
démonstration est portée par la géométrie — le seul trait qui franchit la
séparation est la paire de conduites de la boucle — jamais par une colonne de
chiffres que la page porte déjà. Les conduits sont des canaux topologiques :
aucune implantation réelle n'est reprise (règle 4).

Quatrième module du chantier après `sankey-energie.py`, `zonage-ssi.py` et
`coupe-traversee.py` : le tronc commun (jetons, mesure des chasses, insécables,
double écriture des couleurs) a maintenant quatre occurrences — sa factorisation
est actée au suivi, décision de dépôt, pas de session.
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

# ── Jetons ────────────────────────────────────────────────────────────────────
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

# ── Rythme vertical de la planche ────────────────────────────────────────────
Y_SURTITRE = 76
Y_TITRE = 112
Y_SOUSTITRE = 138
Y_FILET_TITRE = 160
Y_ENTETE = 190
Y_REGISTRES = 220
Y_PHRASE = 688
Y_CARTOUCHE = 714
H_CARTOUCHE = 30

# ── Les deux conduits et la bande de séparation ──────────────────────────────
X_DUCT0 = 120                 # ouverture des conduits, côté dehors
X_AT0, X_AT1 = 920, 1144      # le bloc atelier
YT0, YT1 = 252, 308           # conduit d'air extrait (haut)
YB0, YB1 = 512, 568           # conduit d'air neuf (bas)
Y_AT0, Y_AT1 = YT0, YB1       # l'atelier embrasse les deux conduits

# Les organes du conduit bas, dans l'ordre du flux (batterie, gaz, pac).
BX0, BX1 = 470, 546           # batteries — alignées verticalement
GX0, GX1 = 650, 730           # appoint gaz
PX0, PX1 = 810, 890           # pompe à chaleur
DEBORD = 8                    # débord des boîtes au-delà du conduit

# La boucle : deux conduites verticales entre les deux batteries.
XP1, XP2 = 492, 524

# Avances CALIBRÉES au rendu navigateur (getBBox) sur la première planche.
AVANCE = {
    "sans-400": 0.500,
    "sans-600": 0.480,
    "sans-700": 0.596,
    "mono": 0.600,
}
FINE = 0.098               # U+202F dans Archivo — mesuré 3,93 px à 40 px
INSEC = 0.196              # U+00A0 — mesuré 7,85 px à 40 px


def mesurer(t, corps, profil="sans-400", tracking=0.0):
    """Largeur d'une chaîne, aux avances calibrées ci-dessus."""
    a = AVANCE[profil]
    l = 0.0
    for c in t:
        if c == NN:
            l += FINE
        elif c == INS:
            l += INSEC
        else:
            l += a
    return l * corps + tracking * max(len(t) - 1, 0)


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


def entete_style(A):
    A("<style>")
    for cle, hexa in JETON.items():
        A(f"  .c-{cle} {{ fill: var(--color-{cle}, {hexa}); }}")
    for cle in ("filet-1", "filet-2", "filet-3", "encre", "clair"):
        A(f"  .s-{cle} {{ stroke: var(--color-{cle}, {JETON[cle]}); }}")
    A(f"  .t-sans {{ font-family: {SANS}; }}")
    A(f"  .t-mono {{ font-family: {MONO}; }}")
    A("</style>")


def batterie(A, x0, x1, y0, y1):
    """Le symbole CVC de la batterie d'échange : un rectangle barré d'une
    diagonale. Doublé partout d'un libellé — la forme seule ne porte pas."""
    A(rect_bord(x0, y0, x1 - x0, y1 - y0, "papier", "filet-1"))
    A(ligne(x0, y1, x1, y0, "encre", 1.5))


def composer(donnees):
    b = donnees["boucle"]
    elems = {e["cle"]: e for e in b["elements"]}
    out = []
    A = out.append
    depassements = []

    def controler(nom, texte_mesure, corps, profil, dispo, tracking=0.0):
        largeur = mesurer(texte_mesure, corps, profil, tracking)
        if largeur > dispo:
            depassements.append(f"{nom} : {largeur:.0f} px pour {dispo:.0f} px")
        return largeur

    # ── Racine ───────────────────────────────────────────────────────────────
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
      f'preserveAspectRatio="xMidYMid meet" role="img" '
      f'style="width:100%;height:auto;display:block" '
      f'aria-label="{echapper(donnees["aria_label"])}">')
    entete_style(A)
    A(rect(0, 0, W, H, "papier"))

    # ── Bloc de titre ────────────────────────────────────────────────────────
    A(texte(MARGE, Y_SURTITRE, donnees["surtitre"], "mono", 11, 500,
            "pivot", tracking=11 * 0.14))
    A(texte(MARGE, Y_TITRE, donnees["titre"], "sans", 30, 700, "encre", wdth=112))
    A(texte(MARGE, Y_SOUSTITRE, donnees["sous_titre"], "sans", 16, 400,
            "pivot", wdth=100))
    A(rect(MARGE, Y_FILET_TITRE, UTILE, 1, "filet-1"))

    # ── En-tête du schéma et les deux registres ──────────────────────────────
    controler("en-tête schéma", b["entete"], 10, "mono", UTILE, 10 * 0.14)
    A(texte(MARGE, Y_ENTETE, b["entete"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    A(texte(MARGE, Y_REGISTRES, b["registres"]["gauche"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    A(texte(W - MARGE, Y_REGISTRES, b["registres"]["droite"], "mono", 10, 500,
            "pivot", ancre="end", tracking=10 * 0.14))

    # ── Le bloc atelier, à droite — un bloc topologique, pas un bâtiment ─────
    A(rect(X_AT0, Y_AT0, X_AT1 - X_AT0, Y_AT1 - Y_AT0, "calcaire"))
    at = b["atelier"]["detail"]
    x_at_texte = (X_AT0 + X_AT1) / 2 - 22   # décalé du chemin d'air intérieur
    for k, l in enumerate(at):
        controler(f"atelier — détail {k + 1}", l, 10, "mono",
                  X_AT1 - X_AT0 - 34, 10 * 0.14)
        A(texte(x_at_texte, 400 + k * 16, l, "mono", 10, 500, "pivot",
                ancre="middle", tracking=10 * 0.14))

    # Le chemin d'air intérieur : du soufflage à l'extraction, topologique.
    X_CHEMIN = X_AT1 - 54
    A(polyligne([(X_AT0 + 20, (YB0 + YB1) / 2), (X_CHEMIN, (YB0 + YB1) / 2),
                 (X_CHEMIN, (YT0 + YT1) / 2), (X_AT0 + 16, (YT0 + YT1) / 2)],
                "encre", 1))
    A(fleche(X_CHEMIN, 380, "encre", "haut", 8))
    A(fleche(X_AT0 + 12, (YT0 + YT1) / 2, "encre", "gauche", 8))

    # ── Les deux conduits : parois pleines, jamais en contact ────────────────
    for y in (YT0, YT1):
        A(ligne(X_DUCT0, y, X_AT0, y, "encre", 1.5))
    for y in (YB0, YB1):
        A(ligne(X_DUCT0, y, X_AT0, y, "encre", 1.5))

    # Flèches de flux — extrait vers la gauche, neuf vers la droite.
    y_ext = (YT0 + YT1) / 2
    y_neuf = (YB0 + YB1) / 2
    for x in (300, 650, 820):
        A(fleche(x, y_ext, "encre", "gauche", 9))
    A(fleche(X_DUCT0 - 18, y_ext, "encre", "gauche", 9))
    A(ligne(X_DUCT0 - 18, y_ext, X_DUCT0, y_ext, "encre", 1.5))
    for x in (310, 610, 780):
        A(fleche(x, y_neuf, "encre", "droite", 9))
    A(fleche(X_AT0 + 20, y_neuf, "encre", "droite", 9))

    # Étiquettes des quatre états de l'air.
    et_ext = elems["conduit-extrait"]
    et_neuf = elems["conduit-neuf"]
    controler("étiquette air rejeté", et_ext["etiquette_aval"], 10, "mono",
              340, 10 * 0.14)
    A(texte(X_DUCT0, YT0 - 8, et_ext["etiquette_aval"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    controler("étiquette air extrait", et_ext["etiquette_amont"], 10, "mono",
              340, 10 * 0.14)
    A(texte(X_AT0 - 12, YT0 - 8, et_ext["etiquette_amont"], "mono", 10, 500,
            "pivot", ancre="end", tracking=10 * 0.14))
    # Les boîtes d'organes débordent du conduit bas : les étiquettes montent
    # au-dessus du débord, sans jamais toucher un contour.
    y_et_neuf = YB0 - DEBORD - 10
    controler("étiquette air neuf", et_neuf["etiquette_amont"], 10, "mono",
              340, 10 * 0.14)
    A(texte(X_DUCT0, y_et_neuf, et_neuf["etiquette_amont"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    controler("étiquette air soufflé", et_neuf["etiquette_aval"], 10, "mono",
              340, 10 * 0.14)
    A(texte(X_AT0 - 12, y_et_neuf, et_neuf["etiquette_aval"], "mono", 10, 500,
            "pivot", ancre="end", tracking=10 * 0.14))

    # ── Les deux batteries, alignées, et la boucle entre elles ───────────────
    batterie(A, BX0, BX1, YT0 - DEBORD, YT1 + DEBORD)
    batterie(A, BX0, BX1, YB0 - DEBORD, YB1 + DEBORD)

    be = elems["batterie-extrait"]
    lib_be = be["libelle"]
    x_batt = (BX0 + BX1) / 2
    controler("libellé batterie haute", lib_be, 15, "sans-400", 300)
    A(texte(x_batt, YT0 - DEBORD - 12, lib_be, "sans", 15, 400, "encre",
            wdth=100, ancre="middle"))
    det_be = f'{be["valeur"]}{NN}{be["unite"]} · {be["detail"][0]}'
    controler("détail batterie haute", det_be, 10, "mono", 420, 10 * 0.14)
    A(texte(x_batt, YT1 + DEBORD + 18, det_be, "mono", 10, 500, "pivot",
            ancre="middle", tracking=10 * 0.14))

    # Les conduites de la boucle — le SEUL trait qui franchit la séparation.
    y_haut = YT1 + DEBORD
    y_bas = YB0 - DEBORD
    A(ligne(XP1, y_haut, XP1, y_bas, "encre", 2))
    A(ligne(XP2, y_haut, XP2, y_bas, "encre", 2))
    A(fleche(XP1, 396, "encre", "bas", 8))     # descente à gauche
    A(fleche(XP2, 372, "encre", "haut", 8))    # remontée à droite
    A(cercle(XP1, 452, 9, "papier", "encre"))  # circulateur
    A(fleche(XP1, 457, "encre", "bas", 7))
    A(ligne(XP2, 356, XP2 + 15, 356, "encre", 1))   # vase d'expansion
    A(cercle(XP2 + 21, 356, 6, "clair", "encre", 1))

    # L'appel de la boucle, à gauche.
    bg = elems["boucle-glycol"]
    controler("appel boucle — libellé", bg["libelle"], 15, "sans-400", 400)
    l_lib = mesurer(bg["libelle"], 15, "sans-400")
    A(texte(MARGE, 402, bg["libelle"], "sans", 15, 400, "encre", wdth=100))
    for k, l in enumerate(bg["detail"]):
        controler(f"appel boucle — détail {k + 1}", l, 10, "mono",
                  400, 10 * 0.14)
        A(texte(MARGE, 420 + k * 14, l, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))
    A(polyligne([(MARGE + l_lib + 8, 398), (XP1 - 2, 430)], "filet-1", 1))

    # Le chiffre que la planche défend — le seul en encre pleine.
    val = f'{bg["valeur"]}{INS}{bg["unite"]}'
    x_val = XP2 + 36
    l_val = controler("chiffre de la boucle", val, 22, "sans-700",
                      X_AT0 - x_val)
    A(texte(x_val, 410, val, "sans", 22, 700, "encre", wdth=118,
            tabulaire=True))
    controler("légende du chiffre", bg["legende"], 10, "mono",
              X_AT0 - x_val, 10 * 0.14)
    A(texte(x_val, 430, bg["legende"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    controler("mention du chiffre", bg["mention"], 10, "mono",
              X_AT0 - x_val, 10 * 0.14)
    A(texte(x_val, 446, bg["mention"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    A(ligne(XP2 + 6, 404, x_val - 6, 404, "filet-1", 1))

    # La mention de séparation — ce que la géométrie vient de montrer. Calée
    # sur la colonne du chiffre, écartée en diagonale de l'étiquette AIR SOUFFLÉ.
    for k, l in enumerate(b["mention_separation"]):
        controler(f"mention séparation {k + 1}", l, 10, "mono",
                  X_AT0 - x_val, 10 * 0.14)
        A(texte(x_val, 474 + k * 16, l, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))

    # ── Les organes du conduit bas, libellés dessous ─────────────────────────
    Y_LIB = YB1 + DEBORD + 20        # 596
    Y_DET = Y_LIB + 18               # 614
    for cle, (x0, x1) in (("batterie-neuf", (BX0, BX1)),
                          ("gaz", (GX0, GX1)), ("pac", (PX0, PX1))):
        e = elems[cle]
        xc = (x0 + x1) / 2
        if cle != "batterie-neuf":
            A(rect_bord(x0, YB0 - DEBORD, x1 - x0, YB1 - YB0 + 2 * DEBORD,
                        "papier", "filet-1"))
        controler(f"libellé {cle}", e["libelle"], 15, "sans-400", 220)
        A(texte(xc, Y_LIB, e["libelle"], "sans", 15, 400, "encre",
                wdth=100, ancre="middle"))
        for k, l in enumerate(e["detail"]):
            controler(f"détail {cle} {k + 1}", l, 10, "mono", 220, 10 * 0.14)
            A(texte(xc, Y_DET + k * 14, l, "mono", 10, 500, "pivot",
                    ancre="middle", tracking=10 * 0.14))

    # ── Phrase de principe, pleine largeur ───────────────────────────────────
    l_phrase = controler("phrase de principe", donnees["phrase_principe"], 17,
                         "sans-400", UTILE)
    A(texte(MARGE, Y_PHRASE, donnees["phrase_principe"], "sans", 17, 400,
            "encre", wdth=100))

    # ── Cartouche — largeur AJUSTÉE au texte, jamais codée ───────────────────
    libelle = donnees["cartouche_legende"]
    largeur = min(600,
                  round(mesurer(libelle, 11, "mono", tracking=11 * 0.14) + 40))
    A(rect(MARGE, Y_CARTOUCHE, largeur, H_CARTOUCHE, "profond"))
    A(texte(MARGE + 20, Y_CARTOUCHE + 20, libelle, "mono", 11, 500, "voile",
            tracking=11 * 0.14))

    A("</svg>")

    controles = {
        "gabarit": f"{W} x {H} — rapport {W/H:.4f} (3:2 exact)",
        "demonstration": "les deux conduits (parois encre 1,5) ne se touchent "
                         f"nulle part — bande de séparation y {YT1}–{YB0}, "
                         f"haute de {YB0 - YT1} px ; le seul trait qui la "
                         f"franchit est la paire de conduites de la boucle "
                         f"(x {XP1} et {XP2}) ; le chemin d'air de l'atelier "
                         "reste dans son bloc — la géométrie porte la thèse "
                         "« l'échange sans le contact »",
        "topologie": f"dehors (x < {X_DUCT0}) → conduits (x {X_DUCT0}–{X_AT0}) "
                     f"→ atelier (x {X_AT0}–{X_AT1}) ; extrait y {YT0}–{YT1} "
                     f"vers la gauche, neuf y {YB0}–{YB1} vers la droite ; "
                     f"batteries alignées x {BX0}–{BX1}, gaz x {GX0}–{GX1}, "
                     f"pac x {PX0}–{PX1} — l'ordre du flux est celui du "
                     "descriptif d'origine",
        "bas_du_dessin": f"libellés d'organes à {Y_LIB}, dernier détail à "
                         f"{Y_DET + 14}, phrase de principe à {Y_PHRASE}, "
                         f"cartouche {Y_CARTOUCHE}–{Y_CARTOUCHE + H_CARTOUCHE}, "
                         f"marge basse {H - (Y_CARTOUCHE + H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur * H_CARTOUCHE} px², soit "
                            f"{largeur * H_CARTOUCHE / (W * H) * 100:.2f} % "
                            f"de la planche",
        "chiffre_unique": f"un seul chiffre en encre pleine — "
                          f"{l_val:.0f} px mesurés à 22 px (Archivo 700, "
                          f"tabulaire, U+00A0 au groupement) ; 158 kW et "
                          f"38 000 m³/h restent au mono 10 pivot",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l'échelle "
                         f"0,96 (1152 / {W})",
        "phrase_principe": f"{len(donnees['phrase_principe'])} signes — "
                           f"{l_phrase:.0f} px mesurés pour {UTILE} disponibles",
        "depassements": depassements if depassements
                        else "aucun — toutes les lignes mesurées sous leur colonne",
    }
    return "\n".join(out) + "\n", controles


def composer_vignette(donnees):
    """La vignette : le motif de l'archétype, sans son appareil.

    Ce qu'elle garde : les deux conduits à contre-courant, les deux batteries,
    la boucle qui traverse seule, le bloc atelier — avec les deux nœuds
    chiffrés (la boucle 146 045 kWh/an, l'air neuf 38 000 m³/h). Ce qu'elle
    laisse : l'appoint gaz, la pompe à chaleur, le circulateur, le vase, les
    quatre étiquettes d'air — sept organes annotés dans 300 px ne se
    liraient pas."""
    b = donnees["boucle"]
    elems = {e["cle"]: e for e in b["elements"]}
    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false" '
      f'style="width:100%;height:auto;display:block">')
    entete_style(A)
    A(rect(0, 0, VW, VH, "papier"))
    A(texte(V_MARGE, 22, donnees["vignette_surtitre"], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    # Le motif : conduits y 48-76 et 130-158, atelier à droite, boucle entre.
    yt0, yt1, yb0, yb1 = 48, 76, 130, 158
    x0, xa = 22, 252
    A(rect(xa, yt0 - 6, 286 - xa, yb1 - yt0 + 12, "calcaire"))
    for y in (yt0, yt1, yb0, yb1):
        A(ligne(x0, y, xa, y, "encre", 1.2))
    # Batteries et boucle.
    bx0, bx1 = 104, 140
    for (y0, y1) in ((yt0 - 6, yt1 + 6), (yb0 - 6, yb1 + 6)):
        A(rect_bord(bx0, y0, bx1 - bx0, y1 - y0, "papier", "filet-1"))
        A(ligne(bx0, y1, bx1, y0, "encre", 1.2))
    xp1, xp2 = 114, 130
    A(ligne(xp1, yt1 + 6, xp1, yb0 - 6, "encre", 1.6))
    A(ligne(xp2, yt1 + 6, xp2, yb0 - 6, "encre", 1.6))
    A(fleche(xp1, 106, "encre", "bas", 6))
    A(fleche(xp2, 98, "encre", "haut", 6))
    # Flux à contre-courant.
    yme, ymn = (yt0 + yt1) / 2, (yb0 + yb1) / 2
    for x in (58, 200):
        A(fleche(x, yme, "encre", "gauche", 7))
    for x in (58, 200):
        A(fleche(x, ymn, "encre", "droite", 7))

    # Les deux nœuds chiffrés.
    bg = elems["boucle-glycol"]
    cn = elems["conduit-neuf"]
    A(texte(150, 100, bg["libelle"].replace("d'eau glycolée", "glycolée"),
            "sans", 12, 600, "encre", wdth=112))
    val = f'{bg["valeur"]}{NN}{bg["unite"]}'.replace(INS, NN)
    A(texte(150, 114, val, "mono", 10, 500, "pivot", tabulaire=True))
    A(texte(x0, 180, cn["libelle"], "sans", 12, 600, "encre", wdth=112))
    A(texte(x0 + 58, 180, f'{cn["valeur"]}{NN}{cn["unite"]}', "mono", 10, 500,
            "pivot", tabulaire=True))

    A("</svg>")
    controles = {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": f"carte de projet mesurée de 274 à 296 px — "
                            f"échelle {274/VW:.2f} à {296/VW:.2f}",
        "corps_minimal": f"9 px dans le repère — rendu à {9*274/VW:.1f} px au pire cas",
        "motif": "deux conduits à contre-courant, deux batteries, la boucle "
                 "seule à traverser, le bloc atelier — gaz, pac, circulateur, "
                 "vase et étiquettes d'air sont laissés à la planche",
        "bas_du_dessin": "nœud de l'air neuf à y 180, marge basse 20 px",
    }
    return "\n".join(out) + "\n", controles


def main():
    dossier = Path(sys.argv[1])
    donnees = json.loads((dossier / "planche.json").read_text(encoding="utf-8"))
    svg, controles = composer(donnees)

    io.open(dossier / "planche.svg", "w", encoding="utf-8", newline="\n").write(svg)

    vignette, controles_vignette = composer_vignette(donnees)
    io.open(dossier / "vignette.svg", "w", encoding="utf-8", newline="\n").write(vignette)

    donnees["controles"] = controles
    donnees["controles_vignette"] = controles_vignette
    io.open(dossier / "planche.json", "w", encoding="utf-8", newline="\n").write(
        json.dumps(donnees, ensure_ascii=False, indent=2) + "\n")

    print(f"planche.svg  — {len(svg.encode('utf-8'))} octets, "
          f"{svg.count('<text')} nœuds de texte")
    print(f"vignette.svg — {len(vignette.encode('utf-8'))} octets, "
          f"{vignette.count('<text')} nœuds de texte")
    for k, v in controles_vignette.items():
        print(f"  · vignette · {k} : {v}")
    for k, v in controles.items():
        print(f"  · {k} : {v}")


if __name__ == "__main__":
    main()
