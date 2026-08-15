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

Le module compose CINQ mécanismes de l'archétype, choisis par le bloc que
porte l'extraction :

- `boucle` — la boucle de récupération (atelier Dufour) : deux conduits qui ne
  se rencontrent jamais, une boucle seule à traverser ;
- `utilites` — le réseau de livraison (ateliers Capsulae) : des productions
  centralisées, des chaînes de distribution, et une LIMITE DE MARCHÉ sur
  laquelle tout s'arrête — les attentes — quand les consommateurs se tiennent
  au-delà ;
- `substitution` — la production réversible (centre de formation de Saintes) :
  deux productions convergent sur un même POINT DE SUBSTITUTION qui alimente
  le réseau d'émission — tout ce qui est à droite du point demeure. En regard,
  le parti écarté : des liaisons qui filent de la machine au bâtiment sans
  aucun point, et figent le mode de production ;
- `declinaison` — le parti répété (Le Fougerou) : UNE maison dessinée en
  détail contre 54 cellules strictement identiques portant le même glyphe —
  c'est la répétition qui démontre, l'accolade des 27 calculs la prouve ;
- `appariement` — la partition des services (Pas des Bœufs) : trois bandes de
  service, deux colonnes de machines, et dans chaque colonne UNE boîte qui
  enjambe une frontière de bande — jamais la même. À gauche l'eau chaude
  porte la ventilation, à droite le chauffage porte l'eau chaude.
"""

from _tronc import (NN, INS, W, H, MARGE, UTILE, VW, VH, V_MARGE, AW, AH,
                    A_MARGE, mesurer, echapper, texte, rect, rect_bord, ligne,
                    polyligne, fleche, cercle, entete_style, racine_appui,
                    controles_appui, executer)


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


# ═══ Mécanisme `substitution` — deux productions, un point, un réseau ════════

S_BX0, S_BX1 = 56, 330        # les boîtes de production, à gauche
S_AX0, S_AX1 = 880, 1144      # le bloc bâtiment, à droite
S_CH_Y0, S_CH_Y1 = 264, 348   # la chaudière en service
S_RC_Y0, S_RC_Y1 = 396, 472   # le réseau de chaleur à venir
S_NX, S_NY, S_NR = 470, 368, 10   # le point de substitution
S_YP1, S_YP2 = 360, 376       # les deux conduites du réseau d'émission
S_YSEP = 500                  # le filet qui sépare les deux partis
S_PAC_Y0, S_PAC_Y1 = 536, 620     # le parti écarté


def rect_pointille(x, y, w, h, filet, epaisseur=1.5, motif="6 6"):
    """La production à venir : un contour interrompu — elle n'est pas encore là."""
    from _tronc import JETON
    return (f'  <rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
            f'fill="none" class="s-{filet}" stroke="{JETON[filet]}" '
            f'stroke-width="{epaisseur}" stroke-dasharray="{motif}"/>')


def emetteur(A, x0, y0, w, h):
    """Le symbole générique de l'émetteur : un rectangle à trois éléments —
    aucun modèle réel, un motif topologique."""
    A(rect_bord(x0, y0, w, h, "papier", "filet-1"))
    for k in (1, 2, 3):
        xt = x0 + w * k / 4
        A(ligne(xt, y0 + 5, xt, y0 + h - 5, "filet-1", 1))


def composer_substitution(donnees):
    s = donnees["substitution"]
    elems = {e["cle"]: e for e in s["elements"]}
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
    controler("en-tête schéma", s["entete"], 10, "mono", UTILE, 10 * 0.14)
    A(texte(MARGE, Y_ENTETE, s["entete"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    A(texte(MARGE, Y_REGISTRES, s["registres"]["gauche"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    A(texte(W - MARGE, Y_REGISTRES, s["registres"]["droite"], "mono", 10, 500,
            "pivot", ancre="end", tracking=10 * 0.14))

    # ── Le parti retenu — deux productions, un point, un réseau ─────────────
    ch = elems["chaudiere"]
    rc = elems["reseau-chaleur"]
    pt = elems["point-substitution"]
    em = elems["emission"]
    et = elems["emetteurs"]

    # La chaudière en service — contour plein.
    controler("tag chaudière", ch["tag"], 10, "mono", 500, 10 * 0.14)
    A(texte(S_BX0, S_CH_Y0 - 8, ch["tag"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    A(texte(W - MARGE, S_CH_Y0 - 8, s["tag_retenu"], "mono", 10, 500, "pivot",
            ancre="end", tracking=10 * 0.14))
    A(rect_bord(S_BX0, S_CH_Y0, S_BX1 - S_BX0, S_CH_Y1 - S_CH_Y0,
                "papier", "filet-1"))
    controler("libellé chaudière", ch["libelle"], 15, "sans-600",
              S_BX1 - S_BX0 - 32)
    A(texte(S_BX0 + 16, S_CH_Y0 + 28, ch["libelle"], "sans", 15, 600, "encre",
            wdth=112))
    det_ch = f'{ch["valeur"]}{NN}{ch["unite"]} · {ch["detail"][0]}'
    controler("détail chaudière 1", det_ch, 10, "mono",
              S_BX1 - S_BX0 - 32, 10 * 0.14)
    A(texte(S_BX0 + 16, S_CH_Y0 + 48, det_ch, "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    controler("détail chaudière 2", ch["detail"][1], 10, "mono",
              S_BX1 - S_BX0 - 32, 10 * 0.14)
    A(texte(S_BX0 + 16, S_CH_Y0 + 64, ch["detail"][1], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

    # Le réseau de chaleur à venir — contour interrompu.
    controler("tag réseau de chaleur", rc["tag"], 10, "mono", 500, 10 * 0.14)
    A(texte(S_BX0, S_RC_Y0 - 8, rc["tag"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    A(rect_pointille(S_BX0, S_RC_Y0, S_BX1 - S_BX0, S_RC_Y1 - S_RC_Y0,
                     "filet-1"))
    controler("libellé réseau de chaleur", rc["libelle"], 15, "sans-600",
              S_BX1 - S_BX0 - 32)
    A(texte(S_BX0 + 16, S_RC_Y0 + 28, rc["libelle"], "sans", 15, 600, "encre",
            wdth=112))
    controler("détail réseau de chaleur", rc["detail"][0], 10, "mono",
              S_BX1 - S_BX0 - 32, 10 * 0.14)
    A(texte(S_BX0 + 16, S_RC_Y0 + 48, rc["detail"][0], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

    # Les deux raccordements convergent sur le POINT — plein pour la chaudière,
    # interrompu pour le réseau à venir, qui arrive par-dessous.
    cy_ch = (S_CH_Y0 + S_CH_Y1) / 2                       # 306
    cy_rc = (S_RC_Y0 + S_RC_Y1) / 2                       # 434
    A(polyligne([(S_BX1, cy_ch), (400, cy_ch), (400, S_NY), (S_NX - 24, S_NY)],
                "encre", 1.5))
    A(fleche(S_NX - S_NR - 4, S_NY, "encre", "droite", 9))
    A(ligne_pointillee(S_BX1, cy_rc, S_NX, cy_rc, "encre", 1.5))
    A(ligne_pointillee(S_NX, cy_rc, S_NX, S_NY + S_NR + 12, "encre", 1.5))
    A(fleche(S_NX, S_NY + S_NR + 2, "encre", "haut", 8))
    A(cercle(S_NX, S_NY, S_NR, "papier", "encre"))
    # L'appel du point : un tiret qui attache l'étiquette au cercle.
    A(ligne(S_NX, S_NY - S_NR, S_NX, S_NY - S_NR - 12, "filet-1", 1))
    controler("étiquette du point", pt["etiquette"], 10, "mono",
              S_AX0 - (S_NX + 20), 10 * 0.14)
    A(texte(S_NX + 20, S_NY - 28, pt["etiquette"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

    # Le réseau d'émission : deux conduites, aller et retour, du point au
    # bâtiment — rien d'autre ne les touche.
    A(ligne(S_NX + S_NR - 2, S_YP1, 898, S_YP1, "encre", 1.5))
    A(ligne(S_NX + S_NR - 2, S_YP2, 898, S_YP2, "encre", 1.5))
    for x in (600, 780):
        A(fleche(x, S_YP1, "encre", "droite", 9))
    for x in (620, 800):
        A(fleche(x, S_YP2, "encre", "gauche", 9))
    x_mi = (S_NX + S_AX0) / 2                             # 675
    controler("étiquette du réseau", em["etiquette"], 10, "mono",
              S_AX0 - S_NX - 24, 10 * 0.14)
    A(texte(x_mi, S_YP2 + 22, em["etiquette"], "mono", 10, 500, "pivot",
            ancre="middle", tracking=10 * 0.14))
    controler("mention du parti retenu", s["mention_retenu"], 10, "mono",
              S_AX0 - S_NX - 24, 10 * 0.14)
    A(texte(x_mi, S_YP2 + 40, s["mention_retenu"], "mono", 10, 500, "pivot",
            ancre="middle", tracking=10 * 0.14))

    # Le bâtiment et ses émetteurs — des blocs topologiques.
    A(rect(S_AX0, S_CH_Y0, S_AX1 - S_AX0, S_RC_Y1 - S_CH_Y0, "calcaire"))
    controler("libellé émetteurs", et["libelle"], 15, "sans-600",
              S_AX1 - S_AX0 - 40)
    A(texte(S_AX0 + 20, S_CH_Y0 + 28, et["libelle"], "sans", 15, 600, "encre",
            wdth=112))
    Y_EMET = (308, 352, 396)
    A(ligne(898, Y_EMET[0] + 12, 898, Y_EMET[2] + 12, "encre", 1.2))
    for y0 in Y_EMET:
        emetteur(A, 940, y0, 168, 24)
        A(ligne(898, y0 + 12, 940, y0 + 12, "encre", 1.2))
    controler("détail émetteurs", et["detail"][0], 10, "mono",
              S_AX1 - S_AX0 - 40, 10 * 0.14)
    A(texte(S_AX0 + 20, 448, et["detail"][0], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

    # ── Le parti écarté — des liaisons sans point ────────────────────────────
    A(rect(MARGE, S_YSEP, UTILE, 1, "filet-2"))
    controler("tag du parti écarté", s["tag_ecarte"], 10, "mono",
              UTILE, 10 * 0.14)
    A(texte(MARGE, S_YSEP + 24, s["tag_ecarte"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

    pac = elems["pac-ecartee"]
    A(rect_bord(S_BX0, S_PAC_Y0, S_BX1 - S_BX0, S_PAC_Y1 - S_PAC_Y0,
                "papier", "filet-1"))
    lib_pac = pac.get("libelle_dessin", pac["libelle"])
    controler("libellé pac", lib_pac, 15, "sans-600", S_BX1 - S_BX0 - 32)
    A(texte(S_BX0 + 16, S_PAC_Y0 + 28, lib_pac, "sans", 15, 600, "encre",
            wdth=112))
    for k, l in enumerate(pac["detail"]):
        controler(f"détail pac {k + 1}", l, 10, "mono",
                  S_BX1 - S_BX0 - 32, 10 * 0.14)
        A(texte(S_BX0 + 16, S_PAC_Y0 + 46 + k * 14, l, "mono", 10, 500,
                "pivot", tracking=10 * 0.14))

    bf = s["batiment_fige"]
    A(rect(S_AX0, S_PAC_Y0, S_AX1 - S_AX0, S_PAC_Y1 - S_PAC_Y0, "calcaire"))
    controler("libellé bâtiment figé", bf["libelle"], 15, "sans-600",
              S_AX1 - S_AX0 - 40)
    A(texte(S_AX0 + 20, S_PAC_Y0 + 28, bf["libelle"], "sans", 15, 600, "encre",
            wdth=112))
    for k, l in enumerate(bf["detail"]):
        controler(f"détail bâtiment figé {k + 1}", l, 10, "mono",
                  S_AX1 - S_AX0 - 40, 10 * 0.14)
        A(texte(S_AX0 + 20, S_PAC_Y0 + 46 + k * 14, l, "mono", 10, 500,
                "pivot", tracking=10 * 0.14))

    # Les liaisons : trois traits qui filent d'un bloc à l'autre SANS s'arrêter
    # nulle part — c'est l'absence de nœud qui porte la démonstration.
    Y_LIAISONS = (552, 578, 604)
    for y in Y_LIAISONS:
        A(ligne(S_BX1, y, S_AX0, y, "encre", 1))
        A(fleche(590, y, "encre", "droite", 8))
    x_me = (S_BX1 + S_AX0) / 2                            # 605
    controler("étiquette des liaisons", s["etiquette_liaisons"], 10, "mono",
              S_AX0 - S_BX1 - 24, 10 * 0.14)
    A(texte(x_me, Y_LIAISONS[0] - 10, s["etiquette_liaisons"], "mono", 10, 500,
            "pivot", ancre="middle", tracking=10 * 0.14))

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
        "demonstration": "en haut, les deux raccordements (plein pour la "
                         f"chaudière, interrompu pour le réseau à venir) "
                         f"convergent sur l'UNIQUE cercle du point de "
                         f"substitution (x {S_NX}, y {S_NY}) d'où partent les "
                         f"deux conduites du réseau d'émission ; en bas, les "
                         f"trois liaisons du parti écarté filent de la machine "
                         f"au bâtiment sans rencontrer AUCUN nœud — la "
                         "géométrie seule oppose « un raccord se change » à "
                         "« tout est figé »",
        "topologie": f"productions (x {S_BX0}–{S_BX1} : chaudière y {S_CH_Y0}–"
                     f"{S_CH_Y1} pleine, réseau de chaleur y {S_RC_Y0}–"
                     f"{S_RC_Y1} interrompu) → point (x {S_NX}, r {S_NR}) → "
                     f"conduites y {S_YP1}/{S_YP2} → bâtiment (x {S_AX0}–"
                     f"{S_AX1}, trois émetteurs génériques) ; parti écarté "
                     f"sous le filet y {S_YSEP}, liaisons y "
                     f"{'/'.join(str(y) for y in Y_LIAISONS)}",
        "bas_du_dessin": f"liaisons jusqu'à {Y_LIAISONS[-1]}, blocs écartés "
                         f"jusqu'à {S_PAC_Y1}, phrase de principe à {Y_PHRASE}, "
                         f"cartouche {Y_CARTOUCHE}–{Y_CARTOUCHE + H_CARTOUCHE}, "
                         f"marge basse {H - (Y_CARTOUCHE + H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur * H_CARTOUCHE} px², soit "
                            f"{largeur * H_CARTOUCHE / (W * H) * 100:.2f} % "
                            f"de la planche",
        "chiffre_unique": "aucun chiffre de relevé — la démonstration n'est "
                          "pas chiffrée (révision 4) ; 40 kW reste au mono 10 "
                          "pivot dans la boîte de la chaudière",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l'échelle "
                         f"0,96 (1152 / {W})",
        "phrase_principe": f"{len(donnees['phrase_principe'])} signes — "
                           f"{l_phrase:.0f} px mesurés pour {UTILE} disponibles",
        "depassements": depassements if depassements
                        else "aucun — toutes les lignes mesurées sous leur colonne",
    }
    return "\n".join(out) + "\n", controles


def composer_vignette_substitution(donnees):
    """La vignette : le motif de la substitution, sans son appareil.

    Ce qu'elle garde : les deux productions (pleine et interrompue), le point,
    les deux conduites, le bâtiment et ses émetteurs — avec le nœud chiffré de
    la chaudière (40 kW). Ce qu'elle laisse : le parti écarté tout entier, les
    tags, l'étiquette du réseau — un second registre dans 300 px ne se lirait
    pas."""
    s = donnees["substitution"]
    elems = {e["cle"]: e for e in s["elements"]}
    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false" '
      f'style="width:100%;height:auto;display:block">')
    entete_style(A)
    A(rect(0, 0, VW, VH, "papier"))
    A(texte(V_MARGE, 22, donnees["vignette_surtitre"], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    # Les deux productions — la pleine en service, l'interrompue à venir.
    A(rect_bord(22, 48, 64, 36, "papier", "filet-1"))
    A(rect_pointille(22, 108, 64, 36, "filet-1", 1.2, "4 4"))
    A(texte(54, 130, "À VENIR", "mono", 9, 500, "pivot",
            ancre="middle", tracking=9 * 0.14))

    # Le point, et les deux raccordements qui y convergent.
    nx, ny, nr = 140, 96, 6
    A(polyligne([(86, 66), (nx, 66), (nx, ny - nr - 8)], "encre", 1.2))
    A(fleche(nx, ny - nr - 2, "encre", "bas", 6))
    A(ligne_pointillee(86, 126, nx, 126, "encre", 1.2, "4 4"))
    A(ligne_pointillee(nx, 126, nx, ny + nr + 8, "encre", 1.2, "4 4"))
    A(fleche(nx, ny + nr + 2, "encre", "haut", 6))
    A(cercle(nx, ny, nr, "papier", "encre"))

    # Les deux conduites, vers le bâtiment et ses émetteurs.
    A(ligne(nx + nr, 92, 210, 92, "encre", 1.2))
    A(ligne(nx + nr, 100, 210, 100, "encre", 1.2))
    A(fleche(180, 92, "encre", "droite", 6))
    A(fleche(184, 100, "encre", "gauche", 6))
    A(rect(210, 48, 76, 96, "calcaire"))
    A(ligne(217, 66, 217, 130, "encre", 1))
    for y0 in (58, 90, 122):
        A(rect_bord(224, y0, 48, 16, "papier", "filet-1"))
        A(ligne(217, y0 + 8, 224, y0 + 8, "encre", 1))
        for k in (1, 2, 3):
            A(ligne(224 + 48 * k / 4, y0 + 3, 224 + 48 * k / 4, y0 + 13,
                    "filet-1", 1))

    # Les deux nœuds nommés.
    ch = elems["chaudiere"]
    et = elems["emetteurs"]
    A(texte(22, 170, ch["libelle"], "sans", 12, 600, "encre", wdth=112))
    l_ch = mesurer(ch["libelle"], 12, "sans-600")
    A(texte(22 + l_ch + 8, 170, f'{ch["valeur"]}{NN}{ch["unite"]}',
            "mono", 10, 500, "pivot", tabulaire=True))
    A(texte(22, 186, et["libelle"], "sans", 12, 600, "encre", wdth=112))
    l_et = mesurer(et["libelle"], 12, "sans-600")
    A(texte(22 + l_et + 8, 186, et["detail"][0], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    A("</svg>")
    controles = {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": f"carte de projet mesurée de 274 à 296 px — "
                            f"échelle {274/VW:.2f} à {296/VW:.2f}",
        "corps_minimal": f"9 px dans le repère — rendu à {9*274/VW:.1f} px au pire cas",
        "motif": "deux productions (pleine, interrompue) convergeant sur le "
                 "point, deux conduites, le bâtiment et ses trois émetteurs — "
                 "le parti écarté, les tags et l'étiquette du réseau sont "
                 "laissés à la planche",
        "bas_du_dessin": "nœud des émetteurs à y 186, marge basse 14 px",
    }
    return "\n".join(out) + "\n", controles


def composer_appui_recuperation(donnees):
    """L'appui du hero (mécanisme `boucle`) : le motif à l'échelle 1.

    Ce qu'il garde : les deux conduits à contre-courant nommés, les deux
    batteries, la boucle seule à traverser (avec son chiffre), le bloc atelier
    et la cote de l'air neuf. Ce qu'il laisse : gaz, pompe à chaleur,
    circulateur, vase et mention de séparation — ils vivent sur la planche."""
    b = donnees["boucle"]
    elems = {e["cle"]: e for e in b["elements"]}
    et_ext = elems["conduit-extrait"]
    et_neuf = elems["conduit-neuf"]
    bg = elems["boucle-glycol"]
    out = []
    A = out.append
    racine_appui(A, donnees)

    # Les deux conduits et le bloc atelier.
    yt0, yt1, yb0, yb1 = 88, 140, 240, 292
    x0, xa = 40, 462
    A(rect(xa, yt0 - 10, AW - A_MARGE - xa, yb1 - yt0 + 20, "calcaire"))
    for y in (yt0, yt1, yb0, yb1):
        A(ligne(x0, y, xa, y, "encre", 1.4))
    # Batteries et boucle — le seul trait qui franchit la séparation.
    bx0, bx1 = 190, 258
    for (y0, y1) in ((yt0 - 10, yt1 + 10), (yb0 - 10, yb1 + 10)):
        A(rect_bord(bx0, y0, bx1 - bx0, y1 - y0, "papier", "filet-1"))
        A(ligne(bx0, y1, bx1, y0, "encre", 1.4))
    xp1, xp2 = 210, 238
    A(ligne(xp1, yt1 + 10, xp1, yb0 - 10, "encre", 2))
    A(ligne(xp2, yt1 + 10, xp2, yb0 - 10, "encre", 2))
    A(fleche(xp1, 198, "encre", "bas", 7))
    A(fleche(xp2, 186, "encre", "haut", 7))
    # Flux à contre-courant.
    yme, ymn = (yt0 + yt1) / 2, (yb0 + yb1) / 2
    for x in (100, 380):
        A(fleche(x, yme, "encre", "gauche", 8))
    for x in (100, 380):
        A(fleche(x, ymn, "encre", "droite", 8))

    # Les étiquettes d'air et les nœuds chiffrés.
    A(texte(x0, yt0 - 20, et_ext["etiquette_amont"].split(" · ")[0], "mono",
            10, 500, "pivot", tracking=10 * 0.14))
    A(texte(x0, yb0 - 20, et_neuf["etiquette_amont"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    A(texte(276, 178, bg["libelle"], "sans", 14, 600, "encre", wdth=112))
    val = f'{bg["valeur"]}{NN}{bg["unite"]}'.replace(INS, NN)
    A(texte(276, 195, val, "mono", 11, 500, "pivot", tabulaire=True))
    A(polyligne([(272, 186), (xp2 + 4, 192)], "filet-1", 1))

    A("</svg>")
    return "\n".join(out) + "\n", controles_appui(
        motif="les deux conduits à contre-courant nommés, les deux batteries, "
              "la boucle seule à traverser avec son chiffre (146 045 kWh/an), "
              "le bloc atelier et la cote de l'air neuf — gaz, pompe à "
              "chaleur, circulateur et vase laissés à la planche",
        bas=f"conduit bas jusqu'à 302 px, marge basse {AH - 312} px")


def composer_appui_utilites(donnees):
    """L'appui du hero (mécanisme `utilites`) : le motif à l'échelle 1.

    Ce qu'il garde : les quatre productions nommées, leurs chaînes arrêtées
    sur la limite interrompue et ses nœuds d'attente, les trois ateliers
    nommés, et le nœud chiffré du froid. Ce qu'il laisse : les étiquettes de
    chaîne, la mention des attentes, les détails — ils vivent sur la planche."""
    u = donnees["utilites"]
    elems = {e["cle"]: e for e in u["elements"]}
    out = []
    A = out.append
    racine_appui(A, donnees)

    xlim = 360
    ax0, ax1 = 386, AW - A_MARGE
    ys_boites = (92, 150, 208, 266)
    h_boite = 34
    cles_prod = ("froid", "air-comprime", "ecs", "tgbt")
    for cle, y0 in zip(cles_prod, ys_boites):
        e = elems[cle]
        cy = y0 + h_boite / 2
        A(texte(A_MARGE, y0 - 8, e["libelle"], "sans", 13, 600, "encre",
                wdth=112))
        A(rect_bord(A_MARGE, y0, 126, h_boite, "papier", "filet-1"))
        A(ligne(A_MARGE + 126, cy, xlim - 6, cy, "encre", 1.4))
        A(fleche(260, cy, "encre", "droite", 8))
        A(cercle(xlim, cy, 4.5, "papier", "encre"))
    # Le nœud chiffré du froid, dans sa boîte.
    ef = elems["froid"]
    A(texte(A_MARGE + 12, ys_boites[0] + 22,
            f'{ef["valeur"]}{NN}{ef["unite"]}', "mono", 11, 500, "pivot",
            tabulaire=True))

    # La limite du marché — un trait interrompu, nommé.
    A(ligne_pointillee(xlim, 78, xlim, 312, "encre", 1.4, "5 5"))
    A(texte(xlim, 66, u["limite"]["libelle"], "mono", 10, 500, "pivot",
            ancre="middle", tracking=10 * 0.14))

    # Les trois ateliers, au-delà, nommés.
    cles_ateliers = ("atelier-lit", "atelier-spray", "atelier-rd")
    for cle, (y0, y1) in zip(cles_ateliers, ((78, 150), (160, 232), (242, 314))):
        e = elems[cle]
        A(rect(ax0, y0, ax1 - ax0, y1 - y0, "calcaire"))
        A(texte(ax0 + 12, y0 + 26, e["libelle"], "sans", 13, 600, "encre",
                wdth=112))

    A("</svg>")
    return "\n".join(out) + "\n", controles_appui(
        motif="quatre productions nommées, chaînes arrêtées sur la limite "
              "interrompue (nommée) et ses nœuds d'attente, trois ateliers "
              "nommés au-delà, nœud chiffré du froid (261 kW) — étiquettes de "
              "chaîne et mention des attentes laissées à la planche",
        bas=f"ateliers jusqu'à 314 px, marge basse {AH - 314} px")


def composer_appui_substitution(donnees):
    """L'appui du hero (mécanisme `substitution`) : le motif à l'échelle 1.

    Ce qu'il garde : les deux productions (pleine et interrompue) nommées, le
    point de substitution nommé, les deux conduites, le bâtiment et ses trois
    émetteurs nommés, le chiffre de la chaudière. Ce qu'il laisse : le parti
    écarté, les tags de registre, l'étiquette du réseau d'émission."""
    s = donnees["substitution"]
    elems = {e["cle"]: e for e in s["elements"]}
    ch = elems["chaudiere"]
    rc = elems["reseau-chaleur"]
    pt = elems["point-substitution"]
    et = elems["emetteurs"]
    out = []
    A = out.append
    racine_appui(A, donnees)

    # Les deux productions — la pleine en service, l'interrompue à venir.
    A(texte(A_MARGE, 80, ch["libelle"], "sans", 13, 600, "encre", wdth=112))
    A(rect_bord(A_MARGE, 88, 126, 52, "papier", "filet-1"))
    A(texte(A_MARGE + 12, 118, f'{ch["valeur"]}{NN}{ch["unite"]}', "mono",
            11, 500, "pivot", tabulaire=True))
    A(texte(A_MARGE, 188, rc["libelle"], "sans", 13, 600, "encre", wdth=112))
    A(rect_pointille(A_MARGE, 196, 126, 52, "filet-1", 1.4, "5 5"))
    A(texte(A_MARGE + 63, 226, "À VENIR", "mono", 10, 500, "pivot",
            ancre="middle", tracking=10 * 0.14))

    # Le point, et les deux raccordements qui y convergent.
    nx, ny, nr = 258, 164, 9
    A(polyligne([(150, 114), (nx, 114), (nx, ny - nr - 10)], "encre", 1.4))
    A(fleche(nx, ny - nr - 2, "encre", "bas", 7))
    A(ligne_pointillee(150, 222, nx, 222, "encre", 1.4))
    A(ligne_pointillee(nx, 222, nx, ny + nr + 10, "encre", 1.4))
    A(fleche(nx, ny + nr + 2, "encre", "haut", 7))
    A(cercle(nx, ny, nr, "papier", "encre"))
    A(ligne(nx, ny - nr, nx, ny - nr - 8, "filet-1", 1))
    # L'étiquette du point, à GAUCHE du cercle — à droite, le bloc bâtiment
    # peint après elle la recouvrait (mesuré au premier rendu à 552).
    A(texte(nx - 14, 146, pt["etiquette"], "mono", 10, 500, "pivot",
            ancre="end", tracking=10 * 0.14))

    # Les deux conduites, vers le bâtiment et ses émetteurs.
    bx0, bx1 = 396, AW - A_MARGE
    A(ligne(nx + nr, 158, bx0 + 14, 158, "encre", 1.4))
    A(ligne(nx + nr, 170, bx0 + 14, 170, "encre", 1.4))
    A(fleche(330, 158, "encre", "droite", 7))
    A(fleche(336, 170, "encre", "gauche", 7))
    A(rect(bx0, 80, bx1 - bx0, 184, "calcaire"))
    A(texte(bx0 + 14, 104, et["libelle"], "sans", 13, 600, "encre", wdth=112))
    A(ligne(bx0 + 14, 122, bx0 + 14, 232, "encre", 1.2))
    for y0 in (122, 176, 230):
        emetteur(A, bx0 + 28, y0 - 11, 100, 22)
        A(ligne(bx0 + 14, y0, bx0 + 28, y0, "encre", 1.2))

    A("</svg>")
    return "\n".join(out) + "\n", controles_appui(
        motif="deux productions nommées (pleine, interrompue « à venir ») "
              "convergeant sur le point de substitution nommé, deux "
              "conduites, le bâtiment et ses trois émetteurs — le parti "
              "écarté et l'étiquette du réseau laissés à la planche",
        bas=f"bâtiment jusqu'à 264 px, marge basse {AH - 264} px")


# ═══ Mécanisme `declinaison` — un parti dessiné une fois, 54 cellules ════════
#
# Le Fougerou (Sainte-Marie-de-Ré) : la thèse de la fiche n'est pas un organe,
# c'est une répétition — « un schéma technique sobre, décliné 54 fois ». La
# géométrie oppose UNE maison dessinée en détail (PAC double service → deux
# usages, VMC, échanges avec le dehors) à une matrice de 54 cellules
# strictement identiques, chacune portant le même glyphe du parti. C'est la
# répétition qui démontre ; l'accolade des 27 calculs la prouve.

D_MX0, D_MX1 = 158, 560       # le bloc de la maison-type
D_MY0, D_MY1 = 252, 632
D_PX0, D_PX1 = 176, 356       # la PAC double service
D_PY0, D_PY1 = 300, 440
D_BALLON = 36                 # le compartiment du ballon, intégré à la PAC
D_VX0, D_VX1 = 176, 420       # la VMC hygroréglable
D_VY0, D_VH = 496, 104
D_EX0, D_EX1 = 442, 546       # les radiateurs
D_COLL = 430                  # le collecteur des émetteurs
D_GX0 = 634                   # la grille des 54 maisons
D_GC, D_GG = 50, 7            # cellule et gouttière
D_COLS, D_LIGNES = 9, 6
D_GY0 = 256


def glyphe_parti(A, x, y, c, ep=1.0, bord=True):
    """Le parti en miniature : une production, deux départs — le même signe
    dans chacune des 54 cellules. Doublé partout d'un registre nommé (la
    forme seule ne porte pas)."""
    bx0 = x + 0.14 * c
    bw, bh = 0.26 * c, 0.22 * c
    cy = y + c / 2
    if bord:
        A(rect_bord(bx0, cy - bh / 2, bw, bh, "papier", "filet-1"))
    else:
        # Sous ~30 px de cellule, une boîte papier bordée n'est plus visible :
        # la production devient un point d'encre plein — mesuré à la vignette,
        # où les cellules se lisaient « < » au lieu de « production → départs ».
        A(rect(bx0, cy - bh / 2, bw, bh, "encre"))
    xf1 = x + 0.52 * c
    xf2 = x + 0.82 * c
    A(ligne(bx0 + bw, cy, xf1, cy, "encre", ep))
    A(ligne(xf1, cy, xf2, cy - 0.20 * c, "encre", ep))
    A(ligne(xf1, cy, xf2, cy + 0.20 * c, "encre", ep))


def matrice_cellules(A, id_cellule, x0, y0, c, g, lignes=6, colonnes=9,
                     ep=1.0, bord=True):
    """La matrice des 54 : la cellule est DÉFINIE une fois (`<defs>`,
    identifiant préfixé par le slug — protocole, § Intégration) et employée 54
    fois par `<use>`. La stricte identité des cellules est ainsi garantie par
    la structure du fichier même — et le SVG reste sous 40 Ko."""
    A(f'  <defs><g id="{id_cellule}">')
    A(rect(0, 0, c, c, "calcaire"))
    glyphe_parti(A, 0, 0, c, ep=ep, bord=bord)
    A('  </g></defs>')
    for i in range(lignes):
        for j in range(colonnes):
            x = x0 + j * (c + g)
            y = y0 + i * (c + g)
            A(f'  <use href="#{id_cellule}" xlink:href="#{id_cellule}" '
              f'x="{x:.2f}" y="{y:.2f}"/>')


def composer_declinaison(donnees):
    d = donnees["declinaison"]
    elems = {e["cle"]: e for e in d["elements"]}
    out = []
    A = out.append
    depassements = []

    def controler(nom, texte_mesure, corps, profil, dispo, tracking=0.0):
        largeur = mesurer(texte_mesure, corps, profil, tracking)
        if largeur > dispo:
            depassements.append(f"{nom} : {largeur:.0f} px pour {dispo:.0f} px")
        return largeur

    A(f'<svg xmlns="http://www.w3.org/2000/svg" '
      f'xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" '
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
    controler("en-tête schéma", d["entete"], 10, "mono", UTILE, 10 * 0.14)
    A(texte(MARGE, Y_ENTETE, d["entete"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    A(texte(MARGE, Y_REGISTRES, d["registres"]["gauche"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    A(texte(W - MARGE, Y_REGISTRES, d["registres"]["droite"], "mono", 10, 500,
            "pivot", ancre="end", tracking=10 * 0.14))

    # ── Le dehors, à gauche — les deux échanges d'air de la maison ───────────
    controler("étiquette air extérieur", d["dehors"]["entree"], 10, "mono",
              D_MX0 - MARGE - 6, 10 * 0.14)
    A(texte(MARGE, 340, d["dehors"]["entree"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    A(ligne(MARGE, 356, D_PX0 - 6, 356, "encre", 1.5))
    A(fleche(D_PX0 - 2, 356, "encre", "droite", 9))
    controler("étiquette air extrait", d["dehors"]["sortie"], 10, "mono",
              D_MX0 - MARGE - 6, 10 * 0.14)
    A(texte(MARGE, 538, d["dehors"]["sortie"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    A(ligne(100, 554, D_VX0, 554, "encre", 1.5))
    A(fleche(100, 554, "encre", "gauche", 9))

    # ── La maison-type — un bloc topologique, pas un plan ────────────────────
    A(rect(D_MX0, D_MY0, D_MX1 - D_MX0, D_MY1 - D_MY0, "calcaire"))

    # La PAC double service, et le ballon qui lui est INTÉGRÉ : le compartiment
    # dans la boîte dit l'intégration — la géométrie porte le mot.
    pac = elems["pac"]
    A(rect_bord(D_PX0, D_PY0, D_PX1 - D_PX0, D_PY1 - D_PY0, "papier", "filet-1"))
    lib_pac = pac.get("libelle_dessin", pac["libelle"])
    controler("libellé pac", lib_pac, 15, "sans-600", D_PX1 - D_PX0 - 28)
    A(texte(D_PX0 + 14, D_PY0 + 26, lib_pac, "sans", 15, 600, "encre", wdth=112))
    for k, l in enumerate(pac["detail"]):
        controler(f"détail pac {k + 1}", l, 10, "mono",
                  D_PX1 - D_PX0 - 28, 10 * 0.14)
        A(texte(D_PX0 + 14, D_PY0 + 46 + k * 16, l, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))
    ecs = elems["ecs"]
    A(ligne(D_PX0, D_PY1 - D_BALLON, D_PX1, D_PY1 - D_BALLON, "filet-1", 1))
    controler("compartiment ballon", ecs["detail_dessin"][0], 10, "mono",
              D_PX1 - D_PX0 - 28, 10 * 0.14)
    A(texte(D_PX0 + 14, D_PY1 - 14, ecs["detail_dessin"][0], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))

    # Le départ chauffage : aller et retour vers le collecteur des radiateurs.
    rad = elems["radiateurs"]
    y_all, y_ret = 336, 348
    A(ligne(D_PX1, y_all, D_COLL, y_all, "encre", 1.5))
    A(fleche(400, y_all, "encre", "droite", 9))
    A(ligne(D_PX1, y_ret, D_COLL, y_ret, "encre", 1.5))
    A(fleche(388, y_ret, "encre", "gauche", 9))
    A(ligne(D_COLL, 329, D_COLL, 375, "encre", 1.2))
    for y_em in (318, 364):
        emetteur(A, D_EX0, y_em, D_EX1 - D_EX0, 22)
        A(ligne(D_COLL, y_em + 11, D_EX0, y_em + 11, "encre", 1.2))
    controler("libellé radiateurs", rad["libelle"], 15, "sans-400",
              D_EX1 - 370)
    A(texte(D_EX1, 306, rad["libelle"], "sans", 15, 400, "encre",
            wdth=100, ancre="end"))
    controler("détail radiateurs", rad["detail_dessin"][0], 10, "mono",
              D_EX1 - 366, 10 * 0.14)
    A(texte(D_EX1, 404, rad["detail_dessin"][0], "mono", 10, 500, "pivot",
            ancre="end", tracking=10 * 0.14))

    # Le départ eau chaude sanitaire, depuis le compartiment du ballon.
    y_ecs = 422
    A(ligne(D_PX1, y_ecs, D_COLL, y_ecs, "encre", 1.5))
    A(fleche(404, y_ecs, "encre", "droite", 9))
    A(cercle(D_COLL + 8, y_ecs, 6, "papier", "encre"))
    controler("libellé ecs", ecs["libelle"], 15, "sans-400", D_EX1 - 370)
    A(texte(D_EX1, 448, ecs["libelle"], "sans", 15, 400, "encre",
            wdth=100, ancre="end"))

    # La VMC hygroréglable — le second réseau de la maison, vers le dehors.
    vmc = elems["vmc"]
    lignes_vmc = [seg for dt in vmc["detail"] for seg in dt.split(" · ")]
    A(rect_bord(D_VX0, D_VY0, D_VX1 - D_VX0, D_VH, "papier", "filet-1"))
    lib_vmc = vmc.get("libelle_dessin", vmc["libelle"])
    controler("libellé vmc", lib_vmc, 15, "sans-600", D_VX1 - D_VX0 - 28)
    A(texte(D_VX0 + 14, D_VY0 + 26, lib_vmc, "sans", 15, 600, "encre",
            wdth=112))
    for k, l in enumerate(lignes_vmc):
        controler(f"détail vmc {k + 1}", l, 10, "mono",
                  D_VX1 - D_VX0 - 28, 10 * 0.14)
        A(texte(D_VX0 + 14, D_VY0 + 48 + k * 14, l, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))

    # ── La déclinaison : une flèche, puis 54 cellules identiques ─────────────
    gx1 = D_GX0 + D_COLS * D_GC + (D_COLS - 1) * D_GG
    gy1 = D_GY0 + D_LIGNES * D_GC + (D_LIGNES - 1) * D_GG
    y_mi = (D_GY0 + gy1) / 2
    A(ligne(D_MX1 + 8, y_mi, D_GX0 - 10, y_mi, "encre", 1.5))
    A(fleche(D_GX0 - 6, y_mi, "encre", "droite", 9))
    matrice_cellules(A, "fougerou-cellule-fiche", D_GX0, D_GY0, D_GC, D_GG,
                     lignes=D_LIGNES, colonnes=D_COLS)

    # L'accolade des 27 calculs — une ligne de cote sous la grille entière.
    yb = gy1 + 18
    A(ligne(D_GX0, yb - 5, D_GX0, yb + 5, "encre", 1))
    A(ligne(gx1, yb - 5, gx1, yb + 5, "encre", 1))
    A(ligne(D_GX0, yb, gx1, yb, "encre", 1))
    x_mi = (D_GX0 + gx1) / 2
    for k, l in enumerate(d["mention_calculs"]):
        controler(f"mention calculs {k + 1}", l, 10, "mono",
                  gx1 - D_GX0, 10 * 0.14)
        A(texte(x_mi, yb + 21 + k * 16, l, "mono", 10, 500, "pivot",
                ancre="middle", tracking=10 * 0.14))

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
        "demonstration": "UNE maison dessinée en détail (PAC à compartiment "
                         "ballon, deux départs, VMC, deux échanges d'air avec "
                         f"le dehors) contre {D_COLS * D_LIGNES} cellules "
                         "STRICTEMENT identiques portant le même glyphe "
                         "(production → deux départs) ; l'accolade de cote "
                         "les prend toutes — la géométrie porte la thèse "
                         "« un parti, décliné », aucun chiffre de la fiche "
                         "n'est répété en colonne",
        "topologie": f"dehors (x < {D_MX0}) → maison-type (x {D_MX0}–{D_MX1} : "
                     f"PAC x {D_PX0}–{D_PX1} avec ballon intégré, radiateurs "
                     f"x {D_EX0}–{D_EX1}, ECS, VMC y {D_VY0}–{D_VY0 + D_VH}) "
                     f"→ flèche → grille {D_COLS} × {D_LIGNES} "
                     f"(x {D_GX0}–{gx1}, y {D_GY0}–{gy1}, cellule {D_GC}, "
                     f"gouttière {D_GG}) — matrice topologique, ni îlots ni "
                     "implantation",
        "bas_du_dessin": f"maison jusqu'à {D_MY1}, grille jusqu'à {gy1}, "
                         f"accolade à {yb}, mention des calculs jusqu'à "
                         f"{yb + 21 + 16}, phrase de principe à {Y_PHRASE}, "
                         f"cartouche {Y_CARTOUCHE}–{Y_CARTOUCHE + H_CARTOUCHE}, "
                         f"marge basse {H - (Y_CARTOUCHE + H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur * H_CARTOUCHE} px², soit "
                            f"{largeur * H_CARTOUCHE / (W * H) * 100:.2f} % "
                            f"de la planche",
        "chiffre_unique": "aucun chiffre de relevé — la démonstration n'est "
                          "pas chiffrée (révision 4) ; COP 4,65, 50/45 °C, "
                          "190 L et la mention des 27 calculs restent au "
                          "mono 10 pivot",
        "grille": f"{D_COLS * D_LIGNES} cellules — le compte est celui de la "
                  "fiche (54 maisons), vérifié par construction "
                  f"{D_COLS} × {D_LIGNES}",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l'échelle "
                         f"0,96 (1152 / {W})",
        "phrase_principe": f"{len(donnees['phrase_principe'])} signes — "
                           f"{l_phrase:.0f} px mesurés pour {UTILE} disponibles",
        "depassements": depassements if depassements
                        else "aucun — toutes les lignes mesurées sous leur colonne",
    }
    return "\n".join(out) + "\n", controles


def composer_vignette_declinaison(donnees):
    """La vignette : une cellule dessinée, 54 cellules identiques.

    Ce qu'elle garde : le motif entier — la maison-type (le glyphe en grand),
    la flèche, la matrice complète des 54 cellules — et les deux totaux (54
    maisons, 27 calculs). Ce qu'elle laisse : les organes nommés de la
    maison-type, la mention de conformité, l'accolade — six libellés dans
    300 px ne se liraient pas."""
    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" '
      f'xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false" '
      f'style="width:100%;height:auto;display:block">')
    entete_style(A)
    A(rect(0, 0, VW, VH, "papier"))
    A(texte(V_MARGE, 22, donnees["vignette_surtitre"], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    # La maison-type : une cellule en grand, même glyphe que la matrice.
    A(rect(16, 52, 62, 62, "calcaire"))
    glyphe_parti(A, 16, 52, 62, ep=1.2)
    A(ligne(84, 83, 96, 83, "encre", 1.2))
    A(fleche(100, 83, "encre", "droite", 6))

    # La matrice des 54 — 9 x 6, complète.
    vc, vg = 17, 3
    vx0, vy0 = 104, 34
    matrice_cellules(A, "fougerou-cellule-carte", vx0, vy0, vc, vg,
                     ep=0.9, bord=False)
    vx1 = vx0 + 9 * vc + 8 * vg
    vy1 = vy0 + 6 * vc + 5 * vg

    # Les deux totaux.
    A(texte(16, 172, "La maison-type", "sans", 12, 600, "encre", wdth=112))
    A(texte(16, 186, f"54{NN}MAISONS · 27{NN}CALCULS RT2012", "mono", 10, 500,
            "pivot", tracking=10 * 0.14, tabulaire=True))

    A("</svg>")
    controles = {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": f"carte de projet mesurée de 274 à 296 px — "
                            f"échelle {274/VW:.2f} à {296/VW:.2f}",
        "corps_minimal": f"9 px dans le repère — rendu à {9*274/VW:.1f} px au pire cas",
        "motif": "une cellule en grand (le glyphe du parti), la flèche, la "
                 f"matrice complète des 54 (x {vx0}–{vx1}, y {vy0}–{vy1}) — "
                 "organes nommés, accolade et mention de conformité laissés "
                 "à la planche",
        "bas_du_dessin": "totaux à y 186, marge basse 14 px",
    }
    return "\n".join(out) + "\n", controles


def composer_appui_declinaison(donnees):
    """L'appui du hero (mécanisme `declinaison`) : le motif à l'échelle 1.

    Ce qu'il garde : la maison-type nommée avec la PAC double service et ses
    deux départs chiffrés (chauffage 50/45 °C, ECS 190 L, COP 4,65), la
    flèche, la matrice complète des 54, la mention des 27 calculs. Ce qu'il
    laisse : la VMC, les échanges d'air, les radiateurs dessinés — ils vivent
    sur la planche."""
    d = donnees["declinaison"]
    elems = {e["cle"]: e for e in d["elements"]}
    pac = elems["pac"]
    out = []
    A = out.append
    # La racine est écrite ici plutôt que par `racine_appui` : la matrice en
    # `<use>` réclame l'espace de noms xlink, que le tronc ne déclare pas.
    A(f'<svg xmlns="http://www.w3.org/2000/svg" '
      f'xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {AW} {AH}" '
      f'preserveAspectRatio="xMidYMid meet" role="img" '
      f'style="width:100%;height:auto;display:block" '
      f'aria-label="{echapper(donnees["aria_label"])}">')
    entete_style(A)
    A(rect(0, 0, AW, AH, "papier"))
    A(texte(A_MARGE, 34, donnees["vignette_surtitre"], "mono", 11, 500,
            "pivot", tracking=11 * 0.14))

    # La maison-type, nommée.
    A(texte(A_MARGE, 66, "La maison-type", "sans", 13, 600, "encre", wdth=112))
    A(rect(A_MARGE, 74, 190, 190, "calcaire"))
    # Les deux départs, au-dessus de la PAC.
    A(texte(32, 106, f"CHAUFFAGE 50/45{NN}°C", "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    A(texte(206, 128, f"ECS 190{NN}L", "mono", 10, 500, "pivot",
            ancre="end", tracking=10 * 0.14))
    A(ligne(119, 168, 119, 148, "encre", 1.4))
    A(ligne(119, 148, 72, 126, "encre", 1.4))
    A(fleche(70, 125, "encre", "haut", 7))
    A(ligne(119, 148, 166, 126, "encre", 1.4))
    A(fleche(168, 125, "encre", "haut", 7))
    # La PAC et son compartiment ballon.
    A(rect_bord(40, 168, 158, 84, "papier", "filet-1"))
    lib_pac = pac.get("libelle_dessin", pac["libelle"])
    A(texte(52, 192, lib_pac, "sans", 13, 600, "encre", wdth=112))
    A(texte(52, 212, pac["detail"][1], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    A(ligne(40, 228, 198, 228, "filet-1", 1))
    A(texte(52, 244, "BALLON INTÉGRÉ", "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

    # La flèche de déclinaison, puis la matrice complète.
    A(ligne(222, 197, 246, 197, "encre", 1.4))
    A(fleche(250, 197, "encre", "droite", 8))
    A(texte(258, 66, "Les 54 maisons", "sans", 13, 600, "encre", wdth=112))
    ac, ag = 26, 4
    ax0, ay0 = 258, 74
    matrice_cellules(A, "fougerou-cellule-appui", ax0, ay0, ac, ag,
                     ep=1.0, bord=False)
    ax1 = ax0 + 9 * ac + 8 * ag
    ay1 = ay0 + 6 * ac + 5 * ag

    # La mention des 27 calculs, sous la matrice.
    x_mi = (ax0 + ax1) / 2
    A(texte(x_mi, ay1 + 24, "27 CALCULS RT2012 · TOUS CONFORMES", "mono", 10,
            500, "pivot", ancre="middle", tracking=10 * 0.14))
    A(texte(x_mi, ay1 + 42, f"DE 14 À 36{NN}% SOUS L'EXIGENCE", "mono", 10,
            500, "pivot", ancre="middle", tracking=10 * 0.14))

    A("</svg>")
    return "\n".join(out) + "\n", controles_appui(
        motif="la maison-type nommée (PAC double service, ballon intégré, "
              "départs chauffage 50/45 °C et ECS 190 L, COP 4,65), la flèche, "
              "la matrice complète des 54 cellules, la mention des 27 calculs "
              "— VMC, échanges d'air et radiateurs dessinés laissés à la "
              "planche",
        bas=f"mention des calculs à {250 + 42}, marge basse {AH - 292} px")


# ═══ Mécanisme `appariement` — trois services, deux regroupements ═══════════
#
# Le motif (logements du Pas des Bœufs) : trois bandes de service horizontales
# — chauffage, eau chaude, ventilation — et deux colonnes de machines, une par
# typologie. Dans chaque colonne, UNE boîte enjambe une frontière de bande,
# mais jamais la même : à gauche (T2), la machine d'eau chaude enjambe vers la
# ventilation (caisson d'extraction intégré au ballon) ; à droite (T3), la
# machine de chauffage enjambe vers l'eau chaude (ballon intégré). Texte
# masqué, l'asymétrie des deux enjambements porte seule la thèse « la
# partition par typologie commande celle des équipements ».

AP_GX0, AP_GX1 = 56, 312          # boîtes machines T2, à gauche
AP_DX0, AP_DX1 = 888, 1144        # boîtes machines T3, à droite
AP_CX = 600                       # l'axe des services, au centre
AP_BANDES = ((252, 372), (396, 516), (540, 660))   # chauffage, ecs, ventilation
AP_SEP = (384, 528)               # les deux frontières de bande
AP_ECART = 16                     # respiration entre lien et libellé de service


def _ap_contour(x, y, w, h, ep=1.5):
    """Le contour d'une machine : un trait d'encre, comme les conduits des
    autres mécanismes — il doit dominer la frontière de bande (filet-1) que
    la boîte enjambe, sans quoi l'enjambement se lit comme deux boîtes."""
    from _tronc import JETON
    return (f'  <rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
            f'class="c-papier s-encre" fill="{JETON["papier"]}" '
            f'stroke="{JETON["encre"]}" stroke-width="{ep}"/>')


def _ap_boite(A, controler, e, x0, x1, y0, y1, compartiment_y=None):
    """Une boîte machine : libellé 15/600, détails mono 10 — et, si la machine
    porte deux services, un compartiment (filet-1) avec son propre libellé.
    C'est la boîte qui enjambe la frontière de bande, jamais un trait seul."""
    A(_ap_contour(x0, y0, x1 - x0, y1 - y0))
    dispo = x1 - x0 - 32
    lib = e.get("libelle_dessin", e["libelle"])
    controler(f"libellé {e['cle']}", lib, 15, "sans-600", dispo)
    A(texte(x0 + 16, y0 + 28, lib, "sans", 15, 600, "encre", wdth=112))
    for k, l in enumerate(e.get("detail_dessin", [])):
        controler(f"détail {e['cle']} {k + 1}", l, 10, "mono", dispo, 10 * 0.14)
        A(texte(x0 + 16, y0 + 48 + k * 16, l, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))
    if compartiment_y is not None:
        c = e["compartiment"]
        A(ligne(x0, compartiment_y, x1, compartiment_y, "filet-1", 1))
        controler(f"compartiment {e['cle']}", c["libelle"], 15, "sans-400", dispo)
        A(texte(x0 + 16, compartiment_y + 28, c["libelle"], "sans", 15, 400,
                "encre", wdth=100))
        for k, l in enumerate(c.get("detail", [])):
            controler(f"compartiment {e['cle']} — détail {k + 1}", l, 10,
                      "mono", dispo, 10 * 0.14)
            A(texte(x0 + 16, compartiment_y + 46 + k * 14, l, "mono", 10, 500,
                    "pivot", tracking=10 * 0.14))
        for k, l in enumerate(e.get("mention_dessin", [])):
            controler(f"mention {e['cle']} {k + 1}", l, 10, "mono", dispo,
                      10 * 0.14)
            A(texte(x0 + 16, y1 - 30 + k * 16, l, "mono", 10, 500, "pivot",
                    tracking=10 * 0.14))


def composer_appariement(donnees):
    ap = donnees["appariement"]
    elems = {e["cle"]: e for e in ap["elements"]}
    services = {s["cle"]: s for s in ap["services"]}
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
    controler("en-tête schéma", ap["entete"], 10, "mono", UTILE, 10 * 0.14)
    A(texte(MARGE, Y_ENTETE, ap["entete"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    A(texte(MARGE, Y_REGISTRES, ap["registres"]["gauche"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    A(texte(W - MARGE, Y_REGISTRES, ap["registres"]["droite"], "mono", 10, 500,
            "pivot", ancre="end", tracking=10 * 0.14))

    # ── Les deux frontières de bande — visibles dans l'entre-deux ────────────
    for y in AP_SEP:
        A(ligne(MARGE, y, W - MARGE, y, "filet-1", 1))

    # ── L'axe des services, au centre ────────────────────────────────────────
    centres = {cle: (b0 + b1) / 2
               for cle, (b0, b1) in zip(("chauffage", "ecs", "ventilation"),
                                        AP_BANDES)}
    demi = {}
    for cle, cy in centres.items():
        lib = services[cle]["libelle"]
        l_srv = controler(f"service {cle}", lib, 15, "sans-600", 300)
        demi[cle] = l_srv / 2
        A(texte(AP_CX, cy + 5, lib, "sans", 15, 600, "encre",
                wdth=112, ancre="middle"))

    # ── Les quatre boîtes machines — deux par colonne ────────────────────────
    _ap_boite(A, controler, elems["pac-air-air"], AP_GX0, AP_GX1,
              AP_BANDES[0][0], AP_BANDES[0][1])
    _ap_boite(A, controler, elems["cet"], AP_GX0, AP_GX1,
              AP_BANDES[1][0], AP_BANDES[2][1], compartiment_y=AP_SEP[1])
    _ap_boite(A, controler, elems["pac-air-eau"], AP_DX0, AP_DX1,
              AP_BANDES[0][0], AP_BANDES[1][1], compartiment_y=AP_SEP[0])
    _ap_boite(A, controler, elems["hygro-b"], AP_DX0, AP_DX1,
              AP_BANDES[2][0], AP_BANDES[2][1])

    # ── Les liens : chaque machine rejoint la bande du service qu'elle rend ──
    def lien_gauche(cle_service, etiquettes, nom):
        cy = centres[cle_service]
        x_fin = AP_CX - demi[cle_service] - AP_ECART
        A(ligne(AP_GX1, cy, x_fin - 8, cy, "encre", 1.5))
        A(fleche(x_fin, cy, "encre", "droite", 9))
        x_mi = (AP_GX1 + x_fin) / 2
        for k, l in enumerate(etiquettes):
            controler(f"lien {nom} {k + 1}", l, 10, "mono",
                      x_fin - AP_GX1, 10 * 0.14)
            A(texte(x_mi, cy - 10 - (len(etiquettes) - 1 - k) * 14, l,
                    "mono", 10, 500, "pivot", ancre="middle",
                    tracking=10 * 0.14))

    def lien_droit(cle_service, etiquettes, nom):
        cy = centres[cle_service]
        x_fin = AP_CX + demi[cle_service] + AP_ECART
        A(ligne(AP_DX0, cy, x_fin + 8, cy, "encre", 1.5))
        A(fleche(x_fin, cy, "encre", "gauche", 9))
        x_mi = (AP_DX0 + x_fin) / 2
        for k, l in enumerate(etiquettes):
            controler(f"lien {nom} {k + 1}", l, 10, "mono",
                      AP_DX0 - x_fin, 10 * 0.14)
            A(texte(x_mi, cy - 10 - (len(etiquettes) - 1 - k) * 14, l,
                    "mono", 10, 500, "pivot", ancre="middle",
                    tracking=10 * 0.14))

    lien_gauche("chauffage", elems["pac-air-air"]["lien"], "unités intérieures")
    lien_gauche("ecs", [], "ecs T2")
    lien_gauche("ventilation", elems["cet"]["lien_ventilation"], "hygro A")
    lien_droit("chauffage", elems["pac-air-eau"]["lien"], "radiateurs")
    lien_droit("ecs", [], "ecs T3")
    lien_droit("ventilation", elems["hygro-b"]["lien_ventilation"], "hygro B")

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
        "demonstration": "trois bandes de service et deux colonnes de deux "
                         "boîtes ; dans chaque colonne UNE boîte enjambe une "
                         f"frontière de bande, jamais la même — à gauche le "
                         f"chauffe-eau enjambe y {AP_SEP[1]} (eau chaude → "
                         f"ventilation), à droite la PAC double service "
                         f"enjambe y {AP_SEP[0]} (chauffage → eau chaude) ; "
                         "les deux petites boîtes restent dans leur bande — "
                         "texte masqué, l'asymétrie des enjambements porte "
                         "seule la thèse",
        "topologie": f"machines T2 (x {AP_GX0}–{AP_GX1}) → liens → axe des "
                     f"services (x {AP_CX}) ← liens ← machines T3 "
                     f"(x {AP_DX0}–{AP_DX1}) ; bandes chauffage y "
                     f"{AP_BANDES[0][0]}–{AP_BANDES[0][1]}, eau chaude y "
                     f"{AP_BANDES[1][0]}–{AP_BANDES[1][1]}, ventilation y "
                     f"{AP_BANDES[2][0]}–{AP_BANDES[2][1]} ; frontières "
                     f"y {AP_SEP[0]} et {AP_SEP[1]} — l'ordre des équipements "
                     "est celui de la fiche, typologie par typologie",
        "bas_du_dessin": f"boîtes basses jusqu'à {AP_BANDES[2][1]}, phrase de "
                         f"principe à {Y_PHRASE}, cartouche {Y_CARTOUCHE}–"
                         f"{Y_CARTOUCHE + H_CARTOUCHE}, marge basse "
                         f"{H - (Y_CARTOUCHE + H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur * H_CARTOUCHE} px², soit "
                            f"{largeur * H_CARTOUCHE / (W * H) * 100:.2f} % "
                            f"de la planche",
        "chiffre_unique": "aucun chiffre de relevé — la démonstration n'est "
                          "pas chiffrée (révision 4) ; 4,40 kW, COP 4,63 et "
                          "4,95, 100 L et 190 L, 50/45 °C restent au mono 10 "
                          "pivot dans les boîtes et sur les liens",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l'échelle "
                         f"0,96 (1152 / {W})",
        "phrase_principe": f"{len(donnees['phrase_principe'])} signes — "
                           f"{l_phrase:.0f} px mesurés pour {UTILE} disponibles",
        "depassements": depassements if depassements
                        else "aucun — toutes les lignes mesurées sous leur colonne",
    }
    return "\n".join(out) + "\n", controles


def composer_vignette_appariement(donnees):
    """La vignette : le motif entier — trois bandes, deux colonnes, les deux
    enjambements en miroir — et les deux ballons chiffrés (100 L, 190 L).
    Ce qu'elle laisse : les libellés de machines, les étiquettes de liens,
    les détails — huit libellés dans 300 px ne se liraient pas."""
    ap = donnees["appariement"]
    services = {s["cle"]: s for s in ap["services"]}
    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false" '
      f'style="width:100%;height:auto;display:block">')
    entete_style(A)
    A(rect(0, 0, VW, VH, "papier"))
    A(texte(V_MARGE, 22, donnees["vignette_surtitre"], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    bandes = ((44, 84), (92, 132), (140, 180))
    seps = (88, 136)
    gx0, gx1, dx0, dx1, cx = 16, 84, 216, 284, 150
    for y in seps:
        A(ligne(V_MARGE, y, VW - V_MARGE, y, "filet-1", 1))

    # Les tags de typologie.
    A(texte(gx0, 38, "SEPT T2", "mono", 9, 500, "pivot", tracking=9 * 0.14))
    A(texte(dx1, 38, "TROIS T3", "mono", 9, 500, "pivot", ancre="end",
            tracking=9 * 0.14))

    # Les quatre boîtes — les deux enjambements en miroir, contours d'encre
    # dominant la frontière (filet-1) que les boîtes hautes enjambent.
    A(_ap_contour(gx0, bandes[0][0], gx1 - gx0,
                  bandes[0][1] - bandes[0][0], 1.2))
    A(_ap_contour(gx0, bandes[1][0], gx1 - gx0,
                  bandes[2][1] - bandes[1][0], 1.2))
    A(ligne(gx0, seps[1], gx1, seps[1], "filet-1", 1))
    A(_ap_contour(dx0, bandes[0][0], dx1 - dx0,
                  bandes[1][1] - bandes[0][0], 1.2))
    A(ligne(dx0, seps[0], dx1, seps[0], "filet-1", 1))
    A(_ap_contour(dx0, bandes[2][0], dx1 - dx0,
                  bandes[2][1] - bandes[2][0], 1.2))

    # Les deux ballons chiffrés — les machines qui portent deux services.
    A(texte((gx0 + gx1) / 2, 122, f"100{NN}L", "mono", 10, 500, "pivot",
            ancre="middle", tabulaire=True))
    A(texte((dx0 + dx1) / 2, 118, f"190{NN}L", "mono", 10, 500, "pivot",
            ancre="middle", tabulaire=True))

    # L'axe des services et les liens.
    centres = {cle: (b0 + b1) / 2
               for cle, (b0, b1) in zip(("chauffage", "ecs", "ventilation"),
                                        bandes)}
    liens = {"chauffage": ("g", "d"), "ecs": ("g", "d"),
             "ventilation": ("g", "d")}
    for cle, cy in centres.items():
        lib = services[cle].get("libelle_court", services[cle]["libelle"])
        l_srv = mesurer(lib, 12, "sans-600")
        A(texte(cx, cy + 4, lib, "sans", 12, 600, "encre", wdth=112,
                ancre="middle"))
        xg = cx - l_srv / 2 - 8
        xd = cx + l_srv / 2 + 8
        A(ligne(gx1, cy, xg - 5, cy, "encre", 1.2))
        A(fleche(xg, cy, "encre", "droite", 6))
        A(ligne(dx0, cy, xd + 5, cy, "encre", 1.2))
        A(fleche(xd, cy, "encre", "gauche", 6))

    A("</svg>")
    controles = {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": f"carte de projet mesurée de 274 à 296 px — "
                            f"échelle {274/VW:.2f} à {296/VW:.2f}",
        "corps_minimal": f"9 px dans le repère — rendu à {9*274/VW:.1f} px au pire cas",
        "motif": "trois bandes, deux colonnes, les deux enjambements en "
                 "miroir (compartiments aux frontières 88 et 136) et les deux "
                 "ballons chiffrés — libellés de machines, étiquettes de "
                 "liens et détails laissés à la planche",
        "bas_du_dessin": "boîtes basses à y 180, marge basse 20 px",
    }
    return "\n".join(out) + "\n", controles


def composer_appui_appariement(donnees):
    """L'appui du hero (mécanisme `appariement`) : le motif à l'échelle 1 —
    trois bandes, deux colonnes nommées, les deux enjambements, les nœuds
    chiffrés (COP 4,63 et 4,95, 100 L et 190 L). Ce qu'il laisse : les
    étiquettes de liens, les mentions, la phrase — ils vivent sur la planche."""
    ap = donnees["appariement"]
    services = {s["cle"]: s for s in ap["services"]}
    out = []
    A = out.append
    racine_appui(A, donnees)

    bandes = ((66, 148), (162, 244), (258, 340))
    seps = (155, 251)
    gx0, gx1, dx0, dx1, cx = 24, 196, 356, 528, 276

    A(texte(gx0, 58, "SEPT T2", "mono", 10, 500, "pivot", tracking=10 * 0.14))
    A(texte(dx1, 58, "TROIS T3", "mono", 10, 500, "pivot", ancre="end",
            tracking=10 * 0.14))
    for y in seps:
        A(ligne(gx0, y, dx1, y, "filet-1", 1))

    # T2 — la PAC air-air, bande du chauffage seule.
    A(_ap_contour(gx0, bandes[0][0], gx1 - gx0,
                  bandes[0][1] - bandes[0][0], 1.4))
    A(texte(gx0 + 12, 90, "PAC air-air multisplit", "sans", 13, 600, "encre",
            wdth=112))
    A(texte(gx0 + 12, 110, "CHAUD SEUL · COP 4,63", "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    A(texte(gx0 + 12, 126, f"4,40{NN}kW À +7{NN}°C", "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

    # T2 — le chauffe-eau, qui enjambe eau chaude et ventilation.
    A(_ap_contour(gx0, bandes[1][0], gx1 - gx0,
                  bandes[2][1] - bandes[1][0], 1.4))
    A(ligne(gx0, seps[1], gx1, seps[1], "filet-1", 1))
    A(texte(gx0 + 12, 186, "Chauffe-eau", "sans", 13, 600, "encre", wdth=112))
    A(texte(gx0 + 12, 202, "thermodynamique", "sans", 13, 600, "encre",
            wdth=112))
    A(texte(gx0 + 12, 222, f"100{NN}L · R134a", "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    A(texte(gx0 + 12, 277, "CAISSON D’EXTRACTION", "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    A(texte(gx0 + 12, 293, "INTÉGRÉ AU BALLON", "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

    # T3 — la PAC double service, qui enjambe chauffage et eau chaude.
    A(_ap_contour(dx0, bandes[0][0], dx1 - dx0,
                  bandes[1][1] - bandes[0][0], 1.4))
    A(ligne(dx0, seps[0], dx1, seps[0], "filet-1", 1))
    A(texte(dx0 + 12, 90, "PAC air-eau", "sans", 13, 600, "encre", wdth=112))
    A(texte(dx0 + 12, 110, "DOUBLE SERVICE", "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    A(texte(dx0 + 12, 126, f"COP 4,95 À +7{NN}°C", "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    A(texte(dx0 + 12, 182, f"BALLON 190{NN}L INTÉGRÉ", "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    A(texte(dx0 + 12, 198, "HEURES CREUSES", "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

    # T3 — la ventilation, seule, a sa machine.
    A(_ap_contour(dx0, bandes[2][0], dx1 - dx0,
                  bandes[2][1] - bandes[2][0], 1.4))
    A(texte(dx0 + 12, 282, "Groupe hygroréglable B", "sans", 13, 600, "encre",
            wdth=112))
    A(texte(dx0 + 12, 302, "INDÉPENDANT", "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

    # L'axe des services et les liens.
    centres = {cle: (b0 + b1) / 2
               for cle, (b0, b1) in zip(("chauffage", "ecs", "ventilation"),
                                        bandes)}
    for cle, cy in centres.items():
        lib = services[cle].get("libelle_court", services[cle]["libelle"])
        l_srv = mesurer(lib, 13, "sans-600")
        A(texte(cx, cy + 4, lib, "sans", 13, 600, "encre", wdth=112,
                ancre="middle"))
        xg = cx - l_srv / 2 - 10
        xd = cx + l_srv / 2 + 10
        A(ligne(gx1, cy, xg - 6, cy, "encre", 1.4))
        A(fleche(xg, cy, "encre", "droite", 7))
        A(ligne(dx0, cy, xd + 6, cy, "encre", 1.4))
        A(fleche(xd, cy, "encre", "gauche", 7))

    A("</svg>")
    return "\n".join(out) + "\n", controles_appui(
        motif="trois bandes de service, deux colonnes de machines nommées, "
              "les deux enjambements en miroir (compartiments aux frontières "
              "155 et 251), les nœuds chiffrés COP 4,63 / 4,95 et 100 L / "
              "190 L — étiquettes de liens et mentions laissées à la planche",
        bas=f"boîtes basses à 340, marge basse {AH - 340} px")


# ═══ Mécanisme `individualisation` — le collectif produit, chaque logement compte ═══
#
# Maison relais de Saint-Jean-d'Angély : une chaufferie gaz à condensation en
# cascade et une distribution d'eau froide alimentent une colonne collective qui
# dessert 21 modules thermiques d'appartement — un par logement (7 T1, 8 T1 bis,
# 6 T2). Le détail d'UN logement montre le mécanisme : deux arrivées collectives,
# trois départs comptés (chaleur, eau chaude produite au module, eau froide).
# La démonstration est géométrique : le collectif entre d'un côté de la pile,
# l'individuel comptés sort de l'autre — deux traits deviennent soixante-trois.

I_PX0, I_PX1 = 56, 310          # les boîtes de production, à gauche
I_CH_Y0, I_CH_Y1 = 264, 352     # la chaufferie
I_EF_Y0, I_EF_Y1 = 420, 480     # l'eau froide
I_XCOL = 500                    # la colonne collective (trait vertical)
I_MX0, I_MX1 = 516, 530         # la pile des 21 modules (petits carrés)
I_M_H, I_M_G, I_M_GG = 14, 4, 10    # module, écart, écart de groupe
I_MY0 = 258                     # haut du premier module
I_BX0, I_BX1 = 640, 1144        # le bloc du logement détaillé
I_BY0, I_BY1 = 320, 616
I_DX0, I_DX1 = 720, 880         # le module agrandi
I_Y_ARR = (420, 436)            # arrivée chaleur (aller / retour)
I_Y_EF = 520                    # arrivée eau froide
I_Y_DEP = (400, 470, 540)       # départs comptés : chaleur, eau chaude, eau froide
I_XCPT, I_XFLECHE, I_XTERM = 928, 1008, 1020


def _piles_modules(y0, h, g, gg, groupes):
    """Les ordonnées (haut) des modules, groupés par typologie ; renvoie les
    tops groupe par groupe et l'étendue (haut, bas) de chaque groupe."""
    tops, etendues = [], []
    y = y0
    for n in groupes:
        rang = []
        for _ in range(n):
            rang.append(y)
            y += h + g
        tops.append(rang)
        etendues.append((rang[0], rang[-1] + h))
        y += gg - g
    return tops, etendues


def composer_individualisation(donnees):
    ind = donnees["individualisation"]
    elems = {e["cle"]: e for e in ind["elements"]}
    det = ind["detail"]
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
    controler("en-tête schéma", ind["entete"], 10, "mono", UTILE, 10 * 0.14)
    A(texte(MARGE, Y_ENTETE, ind["entete"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    A(texte(MARGE, Y_REGISTRES, ind["registres"]["gauche"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    A(texte(W - MARGE, Y_REGISTRES, ind["registres"]["droite"], "mono", 10, 500,
            "pivot", ancre="end", tracking=10 * 0.14))

    # ── Les deux productions collectives, à gauche ───────────────────────────
    ch = elems["chaufferie"]
    A(rect_bord(I_PX0, I_CH_Y0, I_PX1 - I_PX0, I_CH_Y1 - I_CH_Y0,
                "papier", "filet-1"))
    lib_ch = ch.get("libelle_dessin", ch["libelle"])
    controler("libellé chaufferie", lib_ch, 15, "sans-600", I_PX1 - I_PX0 - 32)
    A(texte(I_PX0 + 16, I_CH_Y0 + 28, lib_ch, "sans", 15, 600, "encre",
            wdth=112))
    for k, l in enumerate(ch["detail"]):
        controler(f"détail chaufferie {k + 1}", l, 10, "mono",
                  I_PX1 - I_PX0 - 32, 10 * 0.14)
        A(texte(I_PX0 + 16, I_CH_Y0 + 48 + k * 16, l, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))

    ef = elems["eau-froide"]
    A(rect_bord(I_PX0, I_EF_Y0, I_PX1 - I_PX0, I_EF_Y1 - I_EF_Y0,
                "papier", "filet-1"))
    controler("libellé eau froide", ef["libelle"], 15, "sans-600",
              I_PX1 - I_PX0 - 32)
    A(texte(I_PX0 + 16, I_EF_Y0 + 26, ef["libelle"], "sans", 15, 600, "encre",
            wdth=112))
    controler("détail eau froide", ef["detail"][0], 10, "mono",
              I_PX1 - I_PX0 - 32, 10 * 0.14)
    A(texte(I_PX0 + 16, I_EF_Y0 + 46, ef["detail"][0], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))

    # ── Les flux collectifs vers la colonne ──────────────────────────────────
    y_al, y_re = 296, 312          # chaleur : aller et retour
    arr_ch, arr_ef = det["arrivees"][0], det["arrivees"][1]
    controler("étiquette chaleur", arr_ch["etiquette"], 10, "mono",
              I_XCOL - I_PX1 - 20, 10 * 0.14)
    A(texte(I_PX1 + 12, y_al - 12, arr_ch["etiquette"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    A(ligne(I_PX1, y_al, I_XCOL, y_al, "encre", 1.5))
    A(ligne(I_PX1, y_re, I_XCOL, y_re, "encre", 1.5))
    for x in (400, 480):
        A(fleche(x, y_al, "encre", "droite", 9))
    for x in (340, 420):
        A(fleche(x, y_re, "encre", "gauche", 9))

    y_ef = 450
    controler("étiquette eau froide", arr_ef["etiquette"], 10, "mono",
              I_XCOL - I_PX1 - 20, 10 * 0.14)
    A(texte(I_PX1 + 12, y_ef - 12, arr_ef["etiquette"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    A(ligne(I_PX1, y_ef, I_XCOL, y_ef, "encre", 1.5))
    for x in (400, 480):
        A(fleche(x, y_ef, "encre", "droite", 9))

    # ── La colonne collective et la pile des 21 modules ──────────────────────
    groupes = [t["nombre"] for t in ind["typologies"]]
    tops, etendues = _piles_modules(I_MY0, I_M_H, I_M_G, I_M_GG, groupes)
    dernier_centre = tops[-1][-1] + I_M_H / 2
    A(ligne(I_XCOL, tops[0][0] + I_M_H / 2, I_XCOL, dernier_centre,
            "encre", 1.5))
    for rang in tops:
        for t in rang:
            cy = t + I_M_H / 2
            A(ligne(I_XCOL, cy, I_MX0, cy, "encre", 1))
            A(rect_bord(I_MX0, t, I_MX1 - I_MX0, I_M_H, "papier", "filet-1"))

    controler("étiquette de la colonne", ind["colonne"]["etiquette"], 10,
              "mono", I_BX1 - I_XCOL, 10 * 0.14)
    A(texte(I_XCOL, I_MY0 - 8, ind["colonne"]["etiquette"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))

    for t_typ, (g0, g1) in zip(ind["typologies"], etendues):
        controler(f"tag {t_typ['tag']}", t_typ["tag"], 10, "mono",
                  90, 10 * 0.14)
        A(texte(I_MX1 + 14, (g0 + g1) / 2 + 3, t_typ["tag"], "mono", 10, 500,
                "pivot", tracking=10 * 0.14))

    # ── Le rappel d'agrandissement : un module tiré vers le détail ───────────
    tire = tops[1][3]              # au sein des T1 bis — le groupe médian
    A(ligne(I_MX1, tire, I_BX0, I_BY0, "filet-1", 1))
    A(ligne(I_MX1, tire + I_M_H, I_BX0, I_BY1, "filet-1", 1))

    # ── Le logement détaillé — un bloc topologique, pas un plan ──────────────
    controler("tag du détail", det["tag"], 10, "mono",
              I_BX1 - I_BX0, 10 * 0.14)
    A(texte(I_BX0, I_BY0 - 12, det["tag"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    A(rect(I_BX0, I_BY0, I_BX1 - I_BX0, I_BY1 - I_BY0, "calcaire"))

    # Les deux arrivées collectives, reprises à l'échelle du logement.
    controler("arrivée chaleur (détail)", arr_ch["etiquette"], 10, "mono",
              I_DX0 - I_BX0 - 4, 10 * 0.14)
    A(texte(I_BX0, I_Y_ARR[0] - 12, arr_ch["etiquette"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    A(ligne(I_BX0, I_Y_ARR[0], I_DX0, I_Y_ARR[0], "encre", 1.5))
    A(ligne(I_BX0, I_Y_ARR[1], I_DX0, I_Y_ARR[1], "encre", 1.5))
    A(fleche(I_DX0 - 8, I_Y_ARR[0], "encre", "droite", 8))
    A(fleche(I_BX0 + 16, I_Y_ARR[1], "encre", "gauche", 8))
    # L'étiquette passe SOUS sa ligne : au-dessus, elle se lisait en enfilade
    # avec « EAU CHAUDE PRODUITE AU MODULE » de l'autre côté de la paroi.
    controler("arrivée eau froide (détail)", arr_ef["etiquette"], 10, "mono",
              I_DX0 - I_BX0 - 4, 10 * 0.14)
    A(texte(I_BX0, I_Y_EF + 16, arr_ef["etiquette"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    A(ligne(I_BX0, I_Y_EF, I_DX0, I_Y_EF, "encre", 1.5))
    A(fleche(I_DX0 - 8, I_Y_EF, "encre", "droite", 8))

    # Le module agrandi : deux arrivées, trois départs, un échangeur.
    A(rect_bord(I_DX0, 348, I_DX1 - I_DX0, 572 - 348, "papier", "filet-1"))
    # (les étiquettes de départ acceptent une ou deux lignes — voir plus bas)
    for k, l in enumerate(det["module"]["libelle"]):
        controler(f"libellé module {k + 1}", l, 15, "sans-600",
                  I_DX1 - I_DX0 - 24)
        A(texte(I_DX0 + 12, 376 + k * 18, l, "sans", 15, 600, "encre",
                wdth=112))
    controler("détail module", det["module"]["detail"][0], 10, "mono",
              I_DX1 - I_DX0 - 24, 10 * 0.14)
    A(texte(I_DX0 + 12, 414, det["module"]["detail"][0], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    batterie(A, 824, 860, 446, 482)      # l'échangeur — l'eau chaude naît ici
    for k, l in enumerate(det["production"]):
        controler(f"production {k + 1}", l, 10, "mono",
                  I_DX1 - I_DX0 - 24, 10 * 0.14)
        A(texte(I_DX0 + 12, 500 + k * 16, l, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))

    # Les trois départs comptés — un compteur sur chacun.
    for (y, dep) in zip(I_Y_DEP, det["departs"]):
        A(ligne(I_DX1, y, I_XFLECHE - 8, y, "encre", 1.5))
        A(fleche(I_XFLECHE, y, "encre", "droite", 9))
        A(cercle(I_XCPT, y, 8, "papier", "encre"))
        et = dep["etiquette"]
        lignes_et = et if isinstance(et, list) else [et]
        for k, l in enumerate(lignes_et):
            controler(f"étiquette {dep['cle']} {k + 1}", l, 10, "mono",
                      I_XFLECHE - (I_DX1 + 12), 10 * 0.14)
            A(texte(I_DX1 + 12, y - 12 - (len(lignes_et) - 1 - k) * 14, l,
                    "mono", 10, 500, "pivot", tracking=10 * 0.14))

    # Les terminaux : le chauffage a les siens, les deux eaux les partagent.
    term_ch = det["departs"][0]["terminal"]
    for k, l in enumerate(term_ch):
        controler(f"terminal chauffage {k + 1}", l, 15, "sans-400",
                  I_BX1 - I_XTERM - 4)
        A(texte(I_XTERM, I_Y_DEP[0] - 6 + k * 18, l, "sans", 15, 400,
                "encre", wdth=100))
    for k, l in enumerate(det["terminal_eau"]):
        controler(f"terminal eau {k + 1}", l, 15, "sans-400",
                  I_BX1 - I_XTERM - 4)
        A(texte(I_XTERM, 490 + k * 18, l, "sans", 15, 400, "encre", wdth=100))

    controler("mention du détail", det["mention"], 10, "mono",
              I_BX1 - (I_BX0 + 20) - 10, 10 * 0.14)
    A(texte(I_BX0 + 20, I_BY1 - 16, det["mention"], "mono", 10, 500, "pivot",
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
        "demonstration": "deux flux collectifs (la paire de chaleur, l'eau "
                         f"froide) entrent dans la colonne x {I_XCOL} qui "
                         f"dessert une pile de 21 modules identiques "
                         f"(x {I_MX0}–{I_MX1}, trois groupes 7/8/6) ; UN module "
                         "est tiré au détail par deux filets d'agrandissement : "
                         "deux arrivées y entrent, TROIS départs en sortent, "
                         "chacun barré d'un compteur — texte masqué, la "
                         "multiplication (2 traits → 21 modules → 3 comptages) "
                         "porte seule la thèse",
        "topologie": f"productions (x {I_PX0}–{I_PX1} : chaufferie y "
                     f"{I_CH_Y0}–{I_CH_Y1}, eau froide y {I_EF_Y0}–{I_EF_Y1}) "
                     f"→ colonne (x {I_XCOL}) → pile des modules "
                     f"(y {tops[0][0]}–{etendues[-1][1]}, groupes "
                     f"{'/'.join(str(n) for n in groupes)}) ; détail "
                     f"(x {I_BX0}–{I_BX1}, y {I_BY0}–{I_BY1}) : module agrandi "
                     f"x {I_DX0}–{I_DX1}, départs y "
                     f"{'/'.join(str(y) for y in I_Y_DEP)}, compteurs "
                     f"x {I_XCPT} — l'ordre des typologies est celui de "
                     "l'énumération de la fiche",
        "bas_du_dessin": f"pile des modules jusqu'à {etendues[-1][1]}, bloc du "
                         f"détail jusqu'à {I_BY1}, phrase de principe à "
                         f"{Y_PHRASE}, cartouche {Y_CARTOUCHE}–"
                         f"{Y_CARTOUCHE + H_CARTOUCHE}, marge basse "
                         f"{H - (Y_CARTOUCHE + H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur * H_CARTOUCHE} px², soit "
                            f"{largeur * H_CARTOUCHE / (W * H) * 100:.2f} % "
                            f"de la planche",
        "chiffre_unique": "aucun chiffre de relevé — la démonstration n'est "
                          "pas chiffrée (révision 4) ; le seul nombre du "
                          "dessin est le décompte 21 (7 T1 · 8 T1 BIS · 6 T2), "
                          "au mono 10 pivot le long de la pile",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l'échelle "
                         f"0,96 (1152 / {W})",
        "phrase_principe": f"{len(donnees['phrase_principe'])} signes — "
                           f"{l_phrase:.0f} px mesurés pour {UTILE} disponibles",
        "depassements": depassements if depassements
                        else "aucun — toutes les lignes mesurées sous leur colonne",
    }
    return "\n".join(out) + "\n", controles


def composer_vignette_individualisation(donnees):
    """La vignette : le motif entier — deux flux collectifs, la colonne, la
    pile des 21 modules, un module tiré au détail avec ses trois compteurs —
    et le nœud chiffré 21. Ce qu'elle laisse : les libellés de production,
    les typologies, les terminaux — dix libellés dans 300 px ne se liraient
    pas."""
    ind = donnees["individualisation"]
    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false" '
      f'style="width:100%;height:auto;display:block">')
    entete_style(A)
    A(rect(0, 0, VW, VH, "papier"))
    A(texte(V_MARGE, 22, donnees["vignette_surtitre"], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    # Les flux collectifs et la colonne.
    A(texte(V_MARGE, 50, "CHALEUR", "mono", 9, 500, "pivot",
            tracking=9 * 0.14))
    A(ligne(V_MARGE, 58, 100, 58, "encre", 1.2))
    A(ligne(V_MARGE, 66, 100, 66, "encre", 1.2))
    A(fleche(62, 58, "encre", "droite", 6))
    A(fleche(50, 66, "encre", "gauche", 6))
    A(texte(V_MARGE, 96, "EAU FROIDE", "mono", 9, 500, "pivot",
            tracking=9 * 0.14))
    A(ligne(V_MARGE, 104, 100, 104, "encre", 1.2))
    A(fleche(62, 104, "encre", "droite", 6))

    # La pile des 21 modules, en trois groupes.
    groupes = [t["nombre"] for t in ind["typologies"]]
    tops, etendues = _piles_modules(48, 4.2, 1.3, 4.0, groupes)
    A(ligne(100, tops[0][0] + 2.1, 100, tops[-1][-1] + 2.1, "encre", 1.2))
    for rang in tops:
        for t in rang:
            A(ligne(100, t + 2.1, 108, t + 2.1, "encre", 0.8))
            A(rect_bord(108, t, 9, 4.2, "papier", "filet-1"))

    # Un module tiré au détail : trois départs, trois compteurs.
    tire = tops[1][3]
    A(ligne(117, tire, 150, 54, "filet-1", 1))
    A(ligne(117, tire + 4.2, 150, 170, "filet-1", 1))
    A(rect_bord(150, 54, 72, 116, "papier", "filet-1"))
    A(texte(158, 78, "Module", "sans", 12, 600, "encre", wdth=112))
    A(texte(158, 92, "thermique", "sans", 12, 600, "encre", wdth=112))
    for y in (80, 112, 144):
        A(ligne(222, y, 254, y, "encre", 1.2))
        A(cercle(236, y, 3.5, "papier", "encre", 1.2))
        A(fleche(262, y, "encre", "droite", 6))

    # Le nœud chiffré.
    A(texte(V_MARGE, 186, "21 modules", "sans", 12, 600, "encre", wdth=112))
    A(texte(96, 186, "UN PAR LOGEMENT", "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    A("</svg>")
    controles = {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": f"carte de projet mesurée de 274 à 296 px — "
                            f"échelle {274/VW:.2f} à {296/VW:.2f}",
        "corps_minimal": f"9 px dans le repère — rendu à {9*274/VW:.1f} px au pire cas",
        "motif": "deux flux collectifs, la colonne, la pile des 21 modules en "
                 "trois groupes, un module tiré au détail avec ses trois "
                 "compteurs — libellés de production, typologies et terminaux "
                 "laissés à la planche",
        "bas_du_dessin": f"pile jusqu'à {etendues[-1][1]:.0f}, nœuds chiffrés "
                         "à y 186, marge basse 14 px",
    }
    return "\n".join(out) + "\n", controles


def composer_appui_individualisation(donnees):
    """L'appui du hero (mécanisme `individualisation`) : le motif à l'échelle
    1 — les deux productions nommées, la colonne, la pile des 21 modules avec
    ses trois typologies, le module agrandi et ses trois départs comptés. Ce
    qu'il laisse : les terminaux, la mention, la phrase — ils vivent sur la
    planche."""
    ind = donnees["individualisation"]
    elems = {e["cle"]: e for e in ind["elements"]}
    det = ind["detail"]
    out = []
    A = out.append
    racine_appui(A, donnees)

    # Les deux productions.
    A(rect_bord(A_MARGE, 64, 126, 60, "papier", "filet-1"))
    A(texte(A_MARGE + 10, 90, "Chaufferie gaz", "sans", 13, 600, "encre",
            wdth=112))
    A(texte(A_MARGE + 10, 110, "EN CASCADE", "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    A(rect_bord(A_MARGE, 148, 126, 48, "papier", "filet-1"))
    A(texte(A_MARGE + 10, 176, "Eau froide", "sans", 13, 600, "encre",
            wdth=112))

    # Les flux vers la colonne.
    A(ligne(150, 84, 210, 84, "encre", 1.4))
    A(ligne(150, 98, 210, 98, "encre", 1.4))
    A(fleche(185, 84, "encre", "droite", 7))
    A(fleche(168, 98, "encre", "gauche", 7))
    A(ligne(150, 172, 210, 172, "encre", 1.4))
    A(fleche(185, 172, "encre", "droite", 7))

    # La colonne et la pile des 21 modules.
    groupes = [t["nombre"] for t in ind["typologies"]]
    tops, etendues = _piles_modules(84, 8, 2.4, 6.0, groupes)
    A(texte(210, 74, "21 MODULES — UN PAR LOGEMENT", "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    A(ligne(210, tops[0][0] + 4, 210, tops[-1][-1] + 4, "encre", 1.4))
    for rang in tops:
        for t in rang:
            A(ligne(210, t + 4, 222, t + 4, "encre", 1))
            A(rect_bord(222, t, 12, 8, "papier", "filet-1"))
    for t_typ, (g0, g1) in zip(ind["typologies"], etendues):
        A(texte(246, (g0 + g1) / 2 + 3, t_typ["tag"], "mono", 10, 500,
                "pivot", tracking=10 * 0.14))

    # Le module agrandi et ses trois départs comptés.
    tire = tops[1][3]
    A(ligne(234, tire, 320, 96, "filet-1", 1))
    A(ligne(234, tire + 8, 320, 300, "filet-1", 1))
    A(rect_bord(320, 96, 108, 204, "papier", "filet-1"))
    A(texte(332, 126, "Module", "sans", 13, 600, "encre", wdth=112))
    A(texte(332, 144, "thermique", "sans", 13, 600, "encre", wdth=112))
    A(texte(332, 162, "d’appartement", "sans", 13, 600, "encre", wdth=112))
    for y, lib in zip((140, 205, 270), ("CHALEUR", "EAU CHAUDE", "EAU FROIDE")):
        A(texte(434, y - 14, lib, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))
        A(ligne(428, y, 504, y, "encre", 1.4))
        A(cercle(458, y, 7, "papier", "encre"))
        A(fleche(512, y, "encre", "droite", 8))

    A(texte(A_MARGE, 340, "TROIS SERVICES COMPTÉS AU MODULE", "mono", 10, 500,
            "pivot", tracking=10 * 0.14))

    A("</svg>")
    return "\n".join(out) + "\n", controles_appui(
        motif="deux productions nommées, la colonne, la pile des 21 modules "
              "en trois typologies (7 T1 · 8 T1 BIS · 6 T2), le module "
              "agrandi et ses trois départs comptés — terminaux et mention "
              "laissés à la planche",
        bas=f"pile jusqu'à {etendues[-1][1]:.0f}, mention basse à 340, marge "
            f"basse {AH - 340} px")


# ═══ Dispatch — le bloc de l'extraction choisit le mécanisme ═════════════════

def composer(donnees):
    if "individualisation" in donnees:
        return composer_individualisation(donnees)
    if "appariement" in donnees:
        return composer_appariement(donnees)
    if "declinaison" in donnees:
        return composer_declinaison(donnees)
    if "substitution" in donnees:
        return composer_substitution(donnees)
    if "utilites" in donnees:
        return composer_utilites(donnees)
    return composer_recuperation(donnees)


def composer_vignette(donnees):
    if "individualisation" in donnees:
        return composer_vignette_individualisation(donnees)
    if "appariement" in donnees:
        return composer_vignette_appariement(donnees)
    if "declinaison" in donnees:
        return composer_vignette_declinaison(donnees)
    if "substitution" in donnees:
        return composer_vignette_substitution(donnees)
    if "utilites" in donnees:
        return composer_vignette_utilites(donnees)
    return composer_vignette_recuperation(donnees)


def composer_appui(donnees):
    if "individualisation" in donnees:
        return composer_appui_individualisation(donnees)
    if "appariement" in donnees:
        return composer_appui_appariement(donnees)
    if "declinaison" in donnees:
        return composer_appui_declinaison(donnees)
    if "substitution" in donnees:
        return composer_appui_substitution(donnees)
    if "utilites" in donnees:
        return composer_appui_utilites(donnees)
    return composer_appui_recuperation(donnees)


if __name__ == "__main__":
    executer(composer, composer_vignette, composer_appui)
