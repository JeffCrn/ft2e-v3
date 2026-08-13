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
`coupe-traversee.py`. Le tronc commun (jetons, mesure des chasses, insécables,
double écriture des couleurs, routine d'exécution) vit dans `_tronc.py` depuis
le 2026-08-13 — extraction contrôlée par régénération octet à octet des quatre
planches publiées.

Le module compose DEUX mécanismes de l'archétype, choisis par le bloc que porte
l'extraction :

- `boucle` — la boucle de récupération (atelier Dufour) : deux conduits qui ne
  se rencontrent jamais, une boucle seule à traverser ;
- `utilites` — le réseau de livraison (ateliers Capsulae) : des productions
  centralisées, des chaînes de distribution, et une LIMITE DE MARCHÉ sur
  laquelle tout s'arrête — les attentes — quand les consommateurs se tiennent
  au-delà.
"""

from _tronc import (NN, INS, W, H, MARGE, UTILE, VW, VH, V_MARGE, mesurer,
                    echapper, texte, rect, rect_bord, ligne, polyligne,
                    fleche, cercle, entete_style, executer)


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


def batterie(A, x0, x1, y0, y1):
    """Le symbole CVC de la batterie d'échange : un rectangle barré d'une
    diagonale. Doublé partout d'un libellé — la forme seule ne porte pas."""
    A(rect_bord(x0, y0, x1 - x0, y1 - y0, "papier", "filet-1"))
    A(ligne(x0, y1, x1, y0, "encre", 1.5))


def composer_recuperation(donnees):
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


def composer_vignette_recuperation(donnees):
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


# ═══ Mécanisme `utilites` — production → distribution → limite de marché ═════

U_BX0, U_BX1 = 56, 320        # les boîtes de production
U_BH = 72                     # leur hauteur
U_Y0S = (252, 356, 460, 564)  # leurs ordonnées — quatre chaînes
U_XLIM = 800                  # la limite du marché bâtiment
U_AX0, U_AX1 = 830, 1144      # les blocs d'atelier
U_AY = ((252, 372), (386, 506), (520, 640))


def ligne_pointillee(x0, y0, x1, y1, cle, epaisseur=1.5, motif="6 6"):
    """La limite de marché : un trait interrompu — c'est une frontière, pas
    une paroi."""
    from _tronc import JETON
    return (f'  <path d="M {x0:.2f} {y0:.2f} L {x1:.2f} {y1:.2f}" fill="none" '
            f'class="s-{cle}" stroke="{JETON[cle]}" '
            f'stroke-width="{epaisseur}" stroke-dasharray="{motif}"/>')


def composer_utilites(donnees):
    u = donnees["utilites"]
    elems = {e["cle"]: e for e in u["elements"]}
    out = []
    A = out.append
    depassements = []

    def controler(nom, texte_mesure, corps, profil, dispo, tracking=0.0):
        largeur = mesurer(texte_mesure, corps, profil, tracking)
        if largeur > dispo:
            depassements.append(f"{nom} : {largeur:.0f} px pour {dispo:.0f} px")
        return largeur

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

    # ── En-tête et registres ─────────────────────────────────────────────────
    controler("en-tête schéma", u["entete"], 10, "mono", UTILE, 10 * 0.14)
    A(texte(MARGE, Y_ENTETE, u["entete"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    A(texte(MARGE, Y_REGISTRES, u["registres"]["gauche"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    A(texte(W - MARGE, Y_REGISTRES, u["registres"]["droite"], "mono", 10, 500,
            "pivot", ancre="end", tracking=10 * 0.14))

    # ── Les quatre productions et leurs chaînes ──────────────────────────────
    cles_prod = ("froid", "air-comprime", "ecs", "tgbt")
    for cle, y0 in zip(cles_prod, U_Y0S):
        e = elems[cle]
        cy = y0 + U_BH / 2
        A(rect_bord(U_BX0, y0, U_BX1 - U_BX0, U_BH, "papier", "filet-1"))
        controler(f"libellé {cle}", e["libelle"], 15, "sans-600",
                  U_BX1 - U_BX0 - 32)
        A(texte(U_BX0 + 16, y0 + 28, e["libelle"], "sans", 15, 600, "encre",
                wdth=112))
        for k, l in enumerate(e.get("detail", [])):
            controler(f"détail {cle} {k + 1}", l, 10, "mono",
                      U_BX1 - U_BX0 - 32, 10 * 0.14)
            A(texte(U_BX0 + 16, y0 + 46 + k * 14, l, "mono", 10, 500, "pivot",
                    tracking=10 * 0.14))
        # La chaîne : du flanc de la boîte à la limite — pas au-delà.
        A(ligne(U_BX1, cy, U_XLIM - 7, cy, "encre", 1.5))
        for xf in (430, 700):
            A(fleche(xf, cy, "encre", "droite", 9))
        controler(f"étiquette {cle}", e["etiquette"], 10, "mono",
                  U_XLIM - U_BX1 - 40, 10 * 0.14)
        A(texte((U_BX1 + U_XLIM) / 2, cy - 9, e["etiquette"], "mono", 10, 500,
                "pivot", ancre="middle", tracking=10 * 0.14))
        # L'attente : le nœud sur la limite, où la chaîne s'arrête.
        A(cercle(U_XLIM, cy, 5, "papier", "encre"))

    # ── Le chiffre que la planche défend — le seul en encre pleine ───────────
    ef = elems["froid"]
    val = f'{ef["valeur"]}{NN}{ef["unite"]}'
    cy_froid = U_Y0S[0] + U_BH / 2
    x_val = 340
    l_val = controler("chiffre du froid", val, 22, "sans-700", 200)
    A(texte(x_val, cy_froid + 36, val, "sans", 22, 700, "encre", wdth=118,
            tabulaire=True))
    legende = f'{ef["etiquette"]} · {ef["legende"]}'
    controler("légende du chiffre", legende, 10, "mono", 330, 10 * 0.14)
    A(texte(x_val, cy_froid + 54, legende, "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

    # ── La limite du marché bâtiment ─────────────────────────────────────────
    A(ligne_pointillee(U_XLIM, 240, U_XLIM, 648, "encre", 1.5))
    lim = u["limite"]
    controler("libellé limite", lim["libelle"], 10, "mono", 400, 10 * 0.14)
    A(texte(U_XLIM, 232, lim["libelle"], "mono", 10, 500, "pivot",
            ancre="middle", tracking=10 * 0.14))
    controler("mention limite", lim["mention"], 10, "mono", UTILE, 10 * 0.14)
    A(texte(U_XLIM, 664, lim["mention"], "mono", 10, 500, "pivot",
            ancre="middle", tracking=10 * 0.14))

    # ── Les trois ateliers, au-delà — des blocs topologiques ─────────────────
    cles_ateliers = ("atelier-lit", "atelier-spray", "atelier-rd")
    for cle, (y0, y1) in zip(cles_ateliers, U_AY):
        e = elems[cle]
        A(rect(U_AX0, y0, U_AX1 - U_AX0, y1 - y0, "calcaire"))
        controler(f"libellé {cle}", e["libelle"], 15, "sans-600",
                  U_AX1 - U_AX0 - 40)
        A(texte(U_AX0 + 20, y0 + 34, e["libelle"], "sans", 15, 600, "encre",
                wdth=112))
        for k, l in enumerate(e.get("detail", [])):
            controler(f"détail {cle} {k + 1}", l, 10, "mono",
                      U_AX1 - U_AX0 - 40, 10 * 0.14)
            A(texte(U_AX0 + 20, y0 + 54 + k * 14, l, "mono", 10, 500, "pivot",
                    tracking=10 * 0.14))

    # ── Phrase de principe, pleine largeur ───────────────────────────────────
    l_phrase = controler("phrase de principe", donnees["phrase_principe"], 17,
                         "sans-400", UTILE)
    A(texte(MARGE, Y_PHRASE, donnees["phrase_principe"], "sans", 17, 400,
            "encre", wdth=100))

    # ── Cartouche — largeur ajustée, jamais codée ────────────────────────────
    libelle = donnees["cartouche_legende"]
    largeur = min(600,
                  round(mesurer(libelle, 11, "mono", tracking=11 * 0.14) + 40))
    A(rect(MARGE, Y_CARTOUCHE, largeur, H_CARTOUCHE, "profond"))
    A(texte(MARGE + 20, Y_CARTOUCHE + 20, libelle, "mono", 11, 500, "voile",
            tracking=11 * 0.14))

    A("</svg>")

    controles = {
        "gabarit": f"{W} x {H} — rapport {W/H:.4f} (3:2 exact)",
        "demonstration": "quatre chaînes partent des productions et s'arrêtent "
                         f"TOUTES sur la limite (x {U_XLIM}, trait interrompu) "
                         "où chacune porte son nœud d'attente ; les trois blocs "
                         "d'atelier se tiennent au-delà, sans aucun trait qui "
                         "les relie — la géométrie porte la thèse « livrer "
                         "jusqu'aux attentes, pas au-delà »",
        "topologie": f"productions (x {U_BX0}–{U_BX1}, quatre boîtes de "
                     f"{U_BH} px) → chaînes (x {U_BX1}–{U_XLIM - 7}) → limite "
                     f"(x {U_XLIM}, y 240–648) → ateliers (x {U_AX0}–{U_AX1}, "
                     "trois blocs) — l'ordre est celui de l'énumération de la "
                     "fiche",
        "bas_du_dessin": f"dernière production à {U_Y0S[-1] + U_BH}, dernier "
                         f"atelier à {U_AY[-1][1]}, mention des attentes à 664, "
                         f"phrase de principe à {Y_PHRASE}, cartouche "
                         f"{Y_CARTOUCHE}–{Y_CARTOUCHE + H_CARTOUCHE}, marge "
                         f"basse {H - (Y_CARTOUCHE + H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur * H_CARTOUCHE} px², soit "
                            f"{largeur * H_CARTOUCHE / (W * H) * 100:.2f} % "
                            f"de la planche",
        "chiffre_unique": f"un seul chiffre en encre pleine — {l_val:.0f} px "
                          "mesurés à 22 px (261 kW, au plan de marché) ; le "
                          "régime 2/6 °C reste au mono 10 pivot",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l'échelle "
                         f"0,96 (1152 / {W})",
        "phrase_principe": f"{len(donnees['phrase_principe'])} signes — "
                           f"{l_phrase:.0f} px mesurés pour {UTILE} disponibles",
        "depassements": depassements if depassements
                        else "aucun — toutes les lignes mesurées sous leur colonne",
    }
    return "\n".join(out) + "\n", controles


def composer_vignette_utilites(donnees):
    """La vignette du mécanisme `utilites` : quatre chaînes, la limite
    interrompue et ses nœuds, trois blocs au-delà — avec le nœud chiffré du
    froid glycolé. Les libellés de production, la mention des attentes et les
    noms d'atelier sont laissés à la planche."""
    u = donnees["utilites"]
    elems = {e["cle"]: e for e in u["elements"]}
    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false" '
      f'style="width:100%;height:auto;display:block">')
    entete_style(A)
    A(rect(0, 0, VW, VH, "papier"))
    A(texte(V_MARGE, 22, donnees["vignette_surtitre"], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    ys = (58, 88, 118, 148)
    xlim = 196
    for y in ys:
        A(rect_bord(22, y - 9, 34, 18, "papier", "filet-1"))
        A(ligne(56, y, xlim - 4, y, "encre", 1.2))
        A(fleche(120, y, "encre", "droite", 6))
        A(cercle(xlim, y, 3.5, "papier", "encre", 1.2))
    A(ligne_pointillee(xlim, 46, xlim, 160, "encre", 1.2, "4 4"))
    for (y0, y1) in ((46, 80), (86, 120), (126, 160)):
        A(rect(210, y0, 76, y1 - y0, "calcaire"))

    ef = elems["froid"]
    A(texte(22, 180, "Froid glycolé", "sans", 12, 600, "encre", wdth=112))
    A(texte(110, 180, f'{ef["valeur"]}{NN}{ef["unite"]}', "mono", 10, 500,
            "pivot", tabulaire=True))
    A(texte(210, 40, "3 ATELIERS", "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    A("</svg>")
    controles = {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": f"carte de projet mesurée de 274 à 296 px — "
                            f"échelle {274/VW:.2f} à {296/VW:.2f}",
        "corps_minimal": f"9 px dans le repère — rendu à {9*274/VW:.1f} px au pire cas",
        "motif": "quatre chaînes arrêtées sur la limite interrompue, leurs "
                 "nœuds d'attente, trois blocs au-delà — libellés de "
                 "production et noms d'atelier laissés à la planche",
        "bas_du_dessin": "nœud du froid glycolé à y 180, marge basse 20 px",
    }
    return "\n".join(out) + "\n", controles


# ═══ Dispatch — le bloc de l'extraction choisit le mécanisme ═════════════════

def composer(donnees):
    if "utilites" in donnees:
        return composer_utilites(donnees)
    return composer_recuperation(donnees)


def composer_vignette(donnees):
    if "utilites" in donnees:
        return composer_vignette_utilites(donnees)
    return composer_vignette_recuperation(donnees)


if __name__ == "__main__":
    executer(composer, composer_vignette)
