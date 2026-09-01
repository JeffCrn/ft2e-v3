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

- `terminaux` — l'équipement par local (mairie des Portes-en-Ré) : six
  cellules portant chacune leur équipement propre, l'air pour seul réseau
  — trois flèches entrantes, quatre lignes menant chacune à son groupe
  d'extraction dimensionnés par zone — et AUCUN nœud central : la
  décentralisation est la démonstration.

- `regime` — ce que l'aval interdit à l'amont (audit de chauffage de sept
  sites médico-sociaux) : une chaudière déposée, la pompe à chaleur qui la
  remplace, et les DEUX régimes d'eau qu'elle sait fournir en deux longues
  horizontales ; à droite trois familles d'émetteurs posées chacune à la
  hauteur de ce qu'elles exigent — le trait qui monte vers l'aérotherme
  S'ARRÊTE, celui du radiateur traverse une boîte intercalée (l'isolation),
  celui du plancher chauffant atteint sans rien franchir.

- `comptage` — le compteur sur le retour (plan de comptage d'énergie d'un site
  industriel, Rochefort) : une chaufferie, un départ unique, quatre retours
  dont trois passent par un cercle et un se termine en éventail sans cercle,
  un cercle seul sur le tronc de retour — le bâtiment trop ramifié se compte
  par soustraction ; en regard, le bilan du site en carrés pleins (existants)
  et cercles vides (à installer).
"""

from _tronc import (NN, INS, W, H, MARGE, UTILE, VW, VH, V_MARGE, AW, AH,
                    A_MARGE, mesurer, replier, echapper, texte, rect,
                    rect_bord, ligne, polyligne, fleche, cercle, entete_style,
                    racine_appui, controles_appui, executer)


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
                         f"(x {XP1} et {XP2}) ; le chemin d’air de l’atelier "
                         "reste dans son bloc — la géométrie porte la thèse "
                         "« l’échange sans le contact »",
        "topologie": f"dehors (x < {X_DUCT0}) → conduits (x {X_DUCT0}–{X_AT0}) "
                     f"→ atelier (x {X_AT0}–{X_AT1}) ; extrait y {YT0}–{YT1} "
                     f"vers la gauche, neuf y {YB0}–{YB1} vers la droite ; "
                     f"batteries alignées x {BX0}–{BX1}, gaz x {GX0}–{GX1}, "
                     f"pac x {PX0}–{PX1} — l’ordre du flux est celui du "
                     "descriptif d’origine",
        "bas_du_dessin": f"libellés d’organes à {Y_LIB}, dernier détail à "
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
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l’échelle "
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
    A(texte(150, 100, bg["libelle"].replace("d’eau glycolée", "glycolée"),
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
                 "vase et étiquettes d’air sont laissés à la planche",
        "bas_du_dessin": "nœud de l’air neuf à y 180, marge basse 20 px",
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
        "demonstration": "quatre chaînes partent des productions et s’arrêtent "
                         f"TOUTES sur la limite (x {U_XLIM}, trait interrompu) "
                         "où chacune porte son nœud d’attente ; les trois blocs "
                         "d’atelier se tiennent au-delà, sans aucun trait qui "
                         "les relie — la géométrie porte la thèse « livrer "
                         "jusqu’aux attentes, pas au-delà »",
        "topologie": f"productions (x {U_BX0}–{U_BX1}, quatre boîtes de "
                     f"{U_BH} px) → chaînes (x {U_BX1}–{U_XLIM - 7}) → limite "
                     f"(x {U_XLIM}, y 240–648) → ateliers (x {U_AX0}–{U_AX1}, "
                     "trois blocs) — l’ordre est celui de l’énumération de la "
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
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l’échelle "
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
                 "nœuds d’attente, trois blocs au-delà — libellés de "
                 "production et noms d’atelier laissés à la planche",
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
                         f"convergent sur l’UNIQUE cercle du point de "
                         f"substitution (x {S_NX}, y {S_NY}) d’où partent les "
                         f"deux conduites du réseau d’émission ; en bas, les "
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
        "bas_du_dessin": f"liaisons jusqu’à {Y_LIAISONS[-1]}, blocs écartés "
                         f"jusqu’à {S_PAC_Y1}, phrase de principe à {Y_PHRASE}, "
                         f"cartouche {Y_CARTOUCHE}–{Y_CARTOUCHE + H_CARTOUCHE}, "
                         f"marge basse {H - (Y_CARTOUCHE + H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur * H_CARTOUCHE} px², soit "
                            f"{largeur * H_CARTOUCHE / (W * H) * 100:.2f} % "
                            f"de la planche",
        "chiffre_unique": "aucun chiffre de relevé — la démonstration n’est "
                          "pas chiffrée (révision 4) ; 40 kW reste au mono 10 "
                          "pivot dans la boîte de la chaudière",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l’échelle "
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
                 "le parti écarté, les tags et l’étiquette du réseau sont "
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
              "le bloc atelier et la cote de l’air neuf — gaz, pompe à "
              "chaleur, circulateur et vase laissés à la planche",
        bas=f"conduit bas jusqu’à 302 px, marge basse {AH - 312} px")


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
              "interrompue (nommée) et ses nœuds d’attente, trois ateliers "
              "nommés au-delà, nœud chiffré du froid (261 kW) — étiquettes de "
              "chaîne et mention des attentes laissées à la planche",
        bas=f"ateliers jusqu’à 314 px, marge basse {AH - 314} px")


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
              "écarté et l’étiquette du réseau laissés à la planche",
        bas=f"bâtiment jusqu’à 264 px, marge basse {AH - 264} px")


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
                         "ballon, deux départs, VMC, deux échanges d’air avec "
                         f"le dehors) contre {D_COLS * D_LIGNES} cellules "
                         "STRICTEMENT identiques portant le même glyphe "
                         "(production → deux départs) ; l’accolade de cote "
                         "les prend toutes — la géométrie porte la thèse "
                         "« un parti, décliné », aucun chiffre de la fiche "
                         "n’est répété en colonne",
        "topologie": f"dehors (x < {D_MX0}) → maison-type (x {D_MX0}–{D_MX1} : "
                     f"PAC x {D_PX0}–{D_PX1} avec ballon intégré, radiateurs "
                     f"x {D_EX0}–{D_EX1}, ECS, VMC y {D_VY0}–{D_VY0 + D_VH}) "
                     f"→ flèche → grille {D_COLS} × {D_LIGNES} "
                     f"(x {D_GX0}–{gx1}, y {D_GY0}–{gy1}, cellule {D_GC}, "
                     f"gouttière {D_GG}) — matrice topologique, ni îlots ni "
                     "implantation",
        "bas_du_dessin": f"maison jusqu’à {D_MY1}, grille jusqu’à {gy1}, "
                         f"accolade à {yb}, mention des calculs jusqu’à "
                         f"{yb + 21 + 16}, phrase de principe à {Y_PHRASE}, "
                         f"cartouche {Y_CARTOUCHE}–{Y_CARTOUCHE + H_CARTOUCHE}, "
                         f"marge basse {H - (Y_CARTOUCHE + H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur * H_CARTOUCHE} px², soit "
                            f"{largeur * H_CARTOUCHE / (W * H) * 100:.2f} % "
                            f"de la planche",
        "chiffre_unique": "aucun chiffre de relevé — la démonstration n’est "
                          "pas chiffrée (révision 4) ; COP 4,65, 50/45 °C, "
                          "190 L et la mention des 27 calculs restent au "
                          "mono 10 pivot",
        "grille": f"{D_COLS * D_LIGNES} cellules — le compte est celui de la "
                  "fiche (54 maisons), vérifié par construction "
                  f"{D_COLS} × {D_LIGNES}",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l’échelle "
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
    A(texte(x_mi, ay1 + 42, f"DE 14 À 36{NN}% SOUS L’EXIGENCE", "mono", 10,
            500, "pivot", ancre="middle", tracking=10 * 0.14))

    A("</svg>")
    return "\n".join(out) + "\n", controles_appui(
        motif="la maison-type nommée (PAC double service, ballon intégré, "
              "départs chauffage 50/45 °C et ECS 190 L, COP 4,65), la flèche, "
              "la matrice complète des 54 cellules, la mention des 27 calculs "
              "— VMC, échanges d’air et radiateurs dessinés laissés à la "
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
                         "texte masqué, l’asymétrie des enjambements porte "
                         "seule la thèse",
        "topologie": f"machines T2 (x {AP_GX0}–{AP_GX1}) → liens → axe des "
                     f"services (x {AP_CX}) ← liens ← machines T3 "
                     f"(x {AP_DX0}–{AP_DX1}) ; bandes chauffage y "
                     f"{AP_BANDES[0][0]}–{AP_BANDES[0][1]}, eau chaude y "
                     f"{AP_BANDES[1][0]}–{AP_BANDES[1][1]}, ventilation y "
                     f"{AP_BANDES[2][0]}–{AP_BANDES[2][1]} ; frontières "
                     f"y {AP_SEP[0]} et {AP_SEP[1]} — l’ordre des équipements "
                     "est celui de la fiche, typologie par typologie",
        "bas_du_dessin": f"boîtes basses jusqu’à {AP_BANDES[2][1]}, phrase de "
                         f"principe à {Y_PHRASE}, cartouche {Y_CARTOUCHE}–"
                         f"{Y_CARTOUCHE + H_CARTOUCHE}, marge basse "
                         f"{H - (Y_CARTOUCHE + H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur * H_CARTOUCHE} px², soit "
                            f"{largeur * H_CARTOUCHE / (W * H) * 100:.2f} % "
                            f"de la planche",
        "chiffre_unique": "aucun chiffre de relevé — la démonstration n’est "
                          "pas chiffrée (révision 4) ; 4,40 kW, COP 4,63 et "
                          "4,95, 100 L et 190 L, 50/45 °C restent au mono 10 "
                          "pivot dans les boîtes et sur les liens",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l’échelle "
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
        "demonstration": "deux flux collectifs (la paire de chaleur, l’eau "
                         f"froide) entrent dans la colonne x {I_XCOL} qui "
                         f"dessert une pile de 21 modules identiques "
                         f"(x {I_MX0}–{I_MX1}, trois groupes 7/8/6) ; UN module "
                         "est tiré au détail par deux filets d’agrandissement : "
                         "deux arrivées y entrent, TROIS départs en sortent, "
                         "chacun barré d’un compteur — texte masqué, la "
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
                     f"x {I_XCPT} — l’ordre des typologies est celui de "
                     "l’énumération de la fiche",
        "bas_du_dessin": f"pile des modules jusqu’à {etendues[-1][1]}, bloc du "
                         f"détail jusqu’à {I_BY1}, phrase de principe à "
                         f"{Y_PHRASE}, cartouche {Y_CARTOUCHE}–"
                         f"{Y_CARTOUCHE + H_CARTOUCHE}, marge basse "
                         f"{H - (Y_CARTOUCHE + H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur * H_CARTOUCHE} px², soit "
                            f"{largeur * H_CARTOUCHE / (W * H) * 100:.2f} % "
                            f"de la planche",
        "chiffre_unique": "aucun chiffre de relevé — la démonstration n’est "
                          "pas chiffrée (révision 4) ; le seul nombre du "
                          "dessin est le décompte 21 (7 T1 · 8 T1 BIS · 6 T2), "
                          "au mono 10 pivot le long de la pile",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l’échelle "
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
        "bas_du_dessin": f"pile jusqu’à {etendues[-1][1]:.0f}, nœuds chiffrés "
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
        bas=f"pile jusqu’à {etendues[-1][1]:.0f}, mention basse à 340, marge "
            f"basse {AH - 340} px")


# ── Mécanisme `commande` — où le débit se décide ─────────────────────────────
#
# Les six mécanismes précédents disent OÙ va le fluide. Celui-ci dit QUI décide
# qu'il parte : trois circuits d'air indépendants traversent une même enveloppe,
# et leur point de commande se déplace — posé sur la machine pour une extraction
# permanente, dans le réseau pour une régulation à pression constante, dans le
# local pour une sonde de CO2. La géométrie porte donc DEUX grandeurs, toutes
# deux mesurables à la règle :
#
#   · la LONGUEUR de la ligne de commande — la distance de la machine au point
#     où le débit se décide. Elle croît d'un circuit à l'autre, et c'est la
#     démonstration principale ;
#   · l'ÉPAISSEUR de la bande de chaleur APRÈS la machine — pleine quand l'air
#     part avec toute sa chaleur, réduite au dixième quand un échangeur la rend.
#     Les trois épaisseurs se lisent dans LA MÊME COLONNE (x 850–1116), sans
#     quoi elles ne se compareraient pas : leçon de la planche 22.
C_XL0, C_XL1 = 56, 280        # le local
C_XM0, C_XM1 = 620, 850       # la machine
C_XE0, C_XE1 = 900, 916       # l'enveloppe traversée
C_XOUT, C_XFIN = 1116, 1124   # fin des bandes de chaleur, fin des conduits
C_XRISER = 700                # la remontée de la commande dans la machine
C_Y_ZONES = 224               # la ligne des quatre zones nommées
C_Y0 = 244                    # haut du premier bloc
C_H_BLOC = 48                 # hauteur d'un bloc simple flux
C_ECART_FLUX = 58             # écart des deux conduits du double flux
C_GAP_CMD = 26                # du bas des blocs à la ligne de commande
C_GAP_ETIQ = 18               # de la ligne de commande à son étiquette
C_GAP_BANDE = 22              # d'un circuit au suivant
C_H_CHALEUR = 22.0            # la chaleur emportée par l'air extrait — 100 %
# La bande de chaleur se pose sous son conduit, ALIGNÉE PAR SON BORD HAUT — c'est
# cet alignement qui rend les trois épaisseurs comparables. L'écart valait 7 px à
# la première composition : au rendu à 1152, le filet de 2,2 px du troisième
# circuit se lisait alors comme un SECOND CONDUIT et non comme une bande
# effondrée. À 14 px, les circuits 1 et 2 enseignent la convention (une ligne,
# puis une bande) et le filet du troisième se lit à la place de la bande.
C_DECALAGE = 14
C_INTERLIGNE = 20             # dans les blocs
C_R_CAPTEUR = 7.0
C_PROBE_X = {"machine": C_XRISER, "reseau": 450, "local": 168}


def _bandes_commande(elements, y0=C_Y0, h=C_H_BLOC, ecart=C_ECART_FLUX,
                     gap_cmd=C_GAP_CMD, gap_etiq=C_GAP_ETIQ,
                     gap_bande=C_GAP_BANDE):
    """Le rythme vertical des circuits — calculé, jamais tapé. Un circuit à
    double flux occupe deux conduits, donc un bloc plus haut."""
    bandes, y = [], y0
    for e in elements:
        ya = y + h / 2
        ya2 = ya + ecart if e["double_flux"] else None
        by1 = (ya2 if ya2 else ya) + h / 2
        cmd = by1 + gap_cmd
        etiq = cmd + gap_etiq
        bandes.append({"by0": y, "by1": by1, "ya": ya, "ya2": ya2,
                       "cmd": cmd, "etiq": etiq})
        y = etiq + gap_bande
    return bandes


def _pile_lignes(A, controler, nom, x, by0, hauteur_bloc, lignes, largeur):
    """Un bloc de libellés centré verticalement. Chaque ligne porte sa police :
    ('sans', texte) en Archivo 15/600, ('mono', texte) en mono 10 au pivot,
    ('cote', texte) en mono 11 à l'encre — la cote est une mesure, jamais du
    texte courant."""
    total = len(lignes) * C_INTERLIGNE
    y = by0 + (hauteur_bloc - total) / 2 + 14
    for k, (police, contenu) in enumerate(lignes):
        if police == "sans":
            controler(f"{nom} {k + 1}", contenu, 15, "sans-600", largeur)
            A(texte(x, y, contenu, "sans", 15, 600, "encre", wdth=112))
        elif police == "cote":
            controler(f"{nom} {k + 1}", contenu, 11, "mono", largeur, 11 * 0.14)
            A(texte(x, y, contenu, "mono", 11, 500, "encre", tracking=11 * 0.14))
        else:
            controler(f"{nom} {k + 1}", contenu, 10, "mono", largeur, 10 * 0.14)
            A(texte(x, y, contenu, "mono", 10, 500, "pivot", tracking=10 * 0.14))
        y += C_INTERLIGNE


def _etiquette_mono(A, x, y, contenu, corps, tracking, largeur, ancre=None):
    """Un libellé mono posé SUR un trait : il porte son propre fond de papier,
    à la mesure du texte, et interrompt la ligne qu'il annote. Sans lui, les
    limites de zone rayaient les trois étiquettes de commande — le défaut relevé
    à la planche 20, retrouvé ici au rendu à 1152 et invisible en pleine page.
    Le fond est émis AVANT le texte : appelé après, il l'effacerait."""
    x0 = x - largeur if ancre == "end" else x
    A(rect(x0 - 5, y - corps + 1, largeur + 10, corps + 5, "papier"))
    A(texte(x, y, contenu, "mono", corps, 500, "pivot", ancre=ancre,
            tracking=tracking))


def _cote_debit(e):
    """« 1 020 m³/h » — la fine insécable devant l'unité, et dans le
    groupement de milliers que le JSON écrit en espace ordinaire (le site le
    convertit de son côté ; le dessin le convertit ici)."""
    if not e.get("valeur"):
        return None
    return f"{e['valeur'].replace(' ', NN)}{NN}{e['unite']}"


def composer_commande(donnees):
    c = donnees["commande"]
    elements = sorted(c["elements"], key=lambda e: e["ordre"])
    ch = c["chaleur"]
    part = ch["rendement_dessine"] / 100.0
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

    # ── En-tête du schéma ────────────────────────────────────────────────────
    controler("en-tête schéma", c["entete"], 10, "mono", UTILE, 10 * 0.14)
    A(texte(MARGE, Y_ENTETE, c["entete"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

    bandes = _bandes_commande(elements)
    y_haut, y_bas = C_Y0 - 10, bandes[-1]["etiq"] + 6

    # ── Les quatre zones nommées, et les deux limites qui les séparent ───────
    # Sans elles, la longueur d'une ligne de commande ne dirait rien : c'est la
    # zone où le point tombe qui la rend lisible.
    for x, z in zip((C_XL0, C_XL1 + 16, C_XM0, C_XE0), c["zones"]):
        controler(f"zone {z['cle']}", z["libelle"], 10, "mono", 220, 10 * 0.14)
        A(texte(x, C_Y_ZONES, z["libelle"], "mono", 10, 500, "pivot",
                tracking=10 * 0.14))
    for x in (C_XL1, C_XM0):
        A(ligne(x, y_haut, x, y_bas, "filet-3", 1))

    # ── L'enveloppe — une paroi unique, traversée par les trois circuits ─────
    A(rect_bord(C_XE0, y_haut, C_XE1 - C_XE0, bandes[-1]["by1"] + 14 - y_haut,
                "calcaire", "filet-1"))

    # ── Les trois circuits ───────────────────────────────────────────────────
    for e, b in zip(elements, bandes):
        by0, by1, ya, ya2 = b["by0"], b["by1"], b["ya"], b["ya2"]
        h_bloc = by1 - by0

        # Le local, puis la machine — deux blocs topologiques d'égale hauteur.
        A(rect_bord(C_XL0, by0, C_XL1 - C_XL0, h_bloc, "papier", "filet-1"))
        lignes_loc = [("sans", l) for l in e["local_lignes"]]
        if e.get("local_detail"):
            lignes_loc.append(("mono", e["local_detail"]))
        _pile_lignes(A, controler, f"local {e['cle']}", C_XL0 + 16, by0,
                     h_bloc, lignes_loc, C_XL1 - C_XL0 - 32)

        A(rect_bord(C_XM0, by0, C_XM1 - C_XM0, h_bloc, "papier", "filet-1"))
        lignes_mac = [("sans", l) for l in e["machine_lignes"]]
        cote = _cote_debit(e)
        lignes_mac.append(("cote", cote) if cote
                          else ("mono", e["valeur_mention"]))
        largeur_mac = (C_XM1 - 76 if e["double_flux"] else C_XM1) - C_XM0 - 32
        _pile_lignes(A, controler, f"machine {e['cle']}", C_XM0 + 16, by0,
                     h_bloc, lignes_mac, largeur_mac)

        # L'air extrait : du local à la machine, puis dehors.
        A(ligne(C_XL1, ya, C_XM0, ya, "encre", 1.5))
        for x in (430, 545):
            A(fleche(x, ya, "encre", "droite", 9))
        A(rect(C_XL1, ya + C_DECALAGE, C_XM0 - C_XL1, C_H_CHALEUR, "encre"))
        A(ligne(C_XM1, ya, C_XFIN, ya, "encre", 1.5))
        A(fleche(C_XFIN + 8, ya, "encre", "droite", 9))

        # Ce qui part APRÈS la machine — l'épaisseur est la démonstration.
        h_sortie = C_H_CHALEUR * (1 - part) if e["double_flux"] else C_H_CHALEUR
        A(rect(C_XM1, ya + C_DECALAGE, C_XOUT - C_XM1, h_sortie, "encre"))
        legende = ch["legende_fuite"] if e["double_flux"] else ch["legende_perte"]
        controler(f"légende sortie {e['cle']}", legende, 10, "mono",
                  W - MARGE - (C_XE1 + 8), 10 * 0.14)
        A(texte(C_XE1 + 8, ya - 8, legende, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))

        if e["double_flux"]:
            # L'échangeur à contre-courant : deux diagonales croisées, dans la
            # machine, à cheval sur les deux conduits.
            xe0, xe1 = C_XM1 - 56, C_XM1 - 12
            A(rect_bord(xe0, ya - 14, xe1 - xe0, ya2 - ya + 28, "papier",
                        "filet-1"))
            A(ligne(xe0, ya - 14, xe1, ya2 + 14, "encre", 1.5))
            A(ligne(xe0, ya2 + 14, xe1, ya - 14, "encre", 1.5))

            # L'air neuf : du dehors à la machine, puis au local — et la
            # chaleur rendue, 90 % de celle que l'air avait emportée.
            A(ligne(C_XFIN, ya2, C_XM1, ya2, "encre", 1.5))
            A(fleche(C_XM1 + 8, ya2, "encre", "gauche", 9))
            A(ligne(C_XM0, ya2, C_XL1, ya2, "encre", 1.5))
            for x in (400, 515):
                A(fleche(x, ya2, "encre", "gauche", 9))
            A(rect(C_XL1, ya2 + C_DECALAGE, C_XM0 - C_XL1,
                   C_H_CHALEUR * part, "encre"))
            controler("légende retour", ch["legende_retour"], 10, "mono",
                      C_XM0 - (C_XL1 + 8), 10 * 0.14)
            A(texte(C_XL1 + 8, ya2 - 8, ch["legende_retour"], "mono", 10, 500,
                    "pivot", tracking=10 * 0.14))
        elif e["ordre"] == 1:
            controler("légende source", ch["legende_source"], 10, "mono",
                      C_XM0 - (C_XL1 + 8), 10 * 0.14)
            A(texte(C_XL1 + 8, ya - 8, ch["legende_source"], "mono", 10, 500,
                    "pivot", tracking=10 * 0.14))

        # La commande — la ligne dont la LONGUEUR est la thèse.
        xp = C_PROBE_X[e["commande_zone"]]
        if xp != C_XRISER:
            A(ligne(xp, b["cmd"], C_XRISER, b["cmd"], "encre", 2))
        A(ligne(C_XRISER, b["cmd"], C_XRISER, by1 + 9, "encre", 2))
        A(fleche(C_XRISER, by1, "encre", "haut", 9))
        A(cercle(xp, b["cmd"], C_R_CAPTEUR, "papier", "encre", 1.5))
        a_la_machine = e["commande_zone"] == "machine"
        dispo = (xp - C_R_CAPTEUR - MARGE) if a_la_machine else (W - MARGE - xp)
        l_etiq = controler(f"commande {e['cle']}", e["commande_etiquette"], 10,
                           "mono", dispo, 10 * 0.14)
        _etiquette_mono(A, xp - C_R_CAPTEUR - (6 if a_la_machine else 0),
                        b["etiq"], e["commande_etiquette"], 10, 10 * 0.14,
                        l_etiq, ancre="end" if a_la_machine else None)

    # ── La mention de séparation ─────────────────────────────────────────────
    y_mention = bandes[-1]["etiq"] + 30
    mention = " — ".join(c["mention_separation"])
    controler("mention", mention, 10, "mono", UTILE, 10 * 0.14)
    A(texte(MARGE, y_mention, mention, "mono", 10, 500, "pivot",
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

    longueurs = [C_XRISER - C_PROBE_X[e["commande_zone"]] for e in elements]
    aplats = sum((C_XM0 - C_XL1) * C_H_CHALEUR for _ in elements)
    aplats += sum((C_XOUT - C_XM1) * (C_H_CHALEUR * (1 - part)
                                      if e["double_flux"] else C_H_CHALEUR)
                  for e in elements)
    aplats += (C_XM0 - C_XL1) * C_H_CHALEUR * part

    controles = {
        "gabarit": f"{W} x {H} — rapport {W/H:.4f} (3:2 exact)",
        "demonstration": "deux grandeurs mesurables à la règle, aucune "
                         "répétition de la fiche — (1) la LONGUEUR des trois "
                         "lignes de commande, distance de la machine au point "
                         "où le débit se décide : "
                         f"{'/'.join(str(l) for l in longueurs)} px, croissante "
                         "d’un circuit à l’autre ; (2) l’ÉPAISSEUR de la bande "
                         "de chaleur APRÈS la machine, dans la même colonne "
                         f"(x {C_XM1}–{C_XOUT}) pour les trois : "
                         f"{C_H_CHALEUR:.0f}/{C_H_CHALEUR:.0f}/"
                         f"{C_H_CHALEUR * (1 - part):.1f} px — texte masqué, "
                         "trois lignes qui s’allongent et un filet qui remplace "
                         "une bande portent seuls la thèse",
        "topologie": f"local (x {C_XL0}–{C_XL1}) → réseau → machine "
                     f"(x {C_XM0}–{C_XM1}) → enveloppe (x {C_XE0}–{C_XE1}) → "
                     f"dehors ; points de commande x "
                     f"{'/'.join(str(C_PROBE_X[e['commande_zone']]) for e in elements)}"
                     f", remontée commune à x {C_XRISER} ; l’ordre des circuits "
                     "est celui de l’énumération de la fiche",
        "proportion_chaleur": f"rendement dessiné au plancher de la fiche "
                              f"({ch['rendement_dessine']} %) : la bande qui "
                              f"revient vaut {C_H_CHALEUR * part:.1f} px, celle "
                              f"qui part {C_H_CHALEUR * (1 - part):.1f} px, "
                              f"pour {C_H_CHALEUR:.0f} px emportés du local",
        "bas_du_dessin": f"dernier circuit jusqu’à {bandes[-1]['etiq']:.0f}, "
                         f"mention à {y_mention:.0f}, phrase de principe à "
                         f"{Y_PHRASE}, cartouche {Y_CARTOUCHE}–"
                         f"{Y_CARTOUCHE + H_CARTOUCHE}, marge basse "
                         f"{H - (Y_CARTOUCHE + H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur * H_CARTOUCHE} px², soit "
                            f"{largeur * H_CARTOUCHE / (W * H) * 100:.2f} % "
                            f"de la planche",
        "aplats_encre": f"bandes de chaleur {aplats:.0f} px², soit "
                        f"{aplats / (W * H) * 100:.2f} % de la planche — "
                        "aplats d’encre sur papier (12,08), doublés d’une "
                        "mention mono chacun",
        "chiffre_unique": "aucun chiffre de relevé — la démonstration n’est pas "
                          "chiffrée (révision 4) ; les deux seuls nombres du "
                          "dessin sont les débits portés par leur machine "
                          f"({'/'.join(e['valeur'] for e in elements if e.get('valeur'))}"
                          " m³/h), et le troisième circuit porte à leur place la "
                          "mention de son absence",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l’échelle "
                         f"0,96 (1152 / {W})",
        "phrase_principe": f"{len(donnees['phrase_principe'])} signes — "
                           f"{l_phrase:.0f} px mesurés pour {UTILE} disponibles",
        "depassements": depassements if depassements
                        else "aucun — toutes les lignes mesurées sous leur colonne",
    }
    return "\n".join(out) + "\n", controles


def composer_vignette_commande(donnees):
    """La vignette : le motif entier réduit à ce qui démontre — trois circuits,
    trois lignes de commande de longueur croissante, et les trois épaisseurs de
    chaleur dans la même colonne. Ce qu'elle laisse : les libellés de local et
    de machine, les zones nommées, les étiquettes de commande. Six libellés
    dans 300 px ne se lisent pas ; leur absence est une décision."""
    c = donnees["commande"]
    elements = sorted(c["elements"], key=lambda e: e["ordre"])
    part = c["chaleur"]["rendement_dessine"] / 100.0
    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false" '
      f'style="width:100%;height:auto;display:block">')
    entete_style(A)
    A(rect(0, 0, VW, VH, "papier"))
    A(texte(V_MARGE, 22, donnees["vignette_surtitre"], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    xl0, xl1, xm0, xm1 = 14, 56, 152, 208
    xe0, xoutf = 228, 282
    xriser = 180
    h_ch, dec = 8.0, 5.0
    probes = {"machine": xriser, "reseau": 104, "local": 30}
    bandes = _bandes_commande(elements, y0=32, h=20, ecart=22, gap_cmd=13,
                              gap_etiq=0, gap_bande=10)

    A(rect_bord(xe0, 28, 6, bandes[-1]["by1"] + 5 - 28, "calcaire", "filet-1"))
    for e, b in zip(elements, bandes):
        by0, by1, ya, ya2 = b["by0"], b["by1"], b["ya"], b["ya2"]
        A(rect_bord(xl0, by0, xl1 - xl0, by1 - by0, "papier", "filet-1"))
        A(rect_bord(xm0, by0, xm1 - xm0, by1 - by0, "papier", "filet-1"))
        A(ligne(xl1, ya, xm0, ya, "encre", 1.2))
        A(fleche(96, ya, "encre", "droite", 6))
        A(rect(xl1, ya + dec, xm0 - xl1, h_ch, "encre"))
        A(ligne(xm1, ya, xoutf + 4, ya, "encre", 1.2))
        A(fleche(xoutf + 10, ya, "encre", "droite", 6))
        if not e["double_flux"]:
            A(rect(xm1, ya + dec, xoutf - xm1, h_ch, "encre"))
        if e["double_flux"]:
            A(ligne(xoutf + 4, ya2, xm1, ya2, "encre", 1.2))
            A(fleche(xm1 + 6, ya2, "encre", "gauche", 6))
            A(ligne(xm0, ya2, xl1, ya2, "encre", 1.2))
            A(fleche(xl1 + 6, ya2, "encre", "gauche", 6))
            A(rect(xl1, ya2 + dec, xm0 - xl1, h_ch * part, "encre"))
        cote = _cote_debit(e)
        if cote:
            A(texte(xl1 + 4, ya - 5, cote, "mono", 9, 500, "encre",
                    tracking=9 * 0.14))
        xp = probes[e["commande_zone"]]
        if xp != xriser:
            A(ligne(xp, b["cmd"], xriser, b["cmd"], "encre", 1.6))
        A(ligne(xriser, b["cmd"], xriser, by1 + 4, "encre", 1.6))
        A(fleche(xriser, by1, "encre", "haut", 5))
        A(cercle(xp, b["cmd"], 4, "papier", "encre", 1.2))

    A("</svg>")
    controles = {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": f"carte de projet mesurée de 274 à 296 px — "
                            f"échelle {274/VW:.2f} à {296/VW:.2f}",
        "corps_minimal": f"9 px dans le repère — rendu à {9*274/VW:.1f} px au pire cas",
        "motif": "trois circuits, trois lignes de commande de longueur "
                 f"{'/'.join(str(xriser - probes[e['commande_zone']]) for e in elements)}"
                 f" px, la chaleur emportée du local ({h_ch:.0f} px) et celle "
                 f"qui revient au troisième ({h_ch * part:.1f} px) ; les deux "
                 "débits restent, tout libellé part",
        "proportion_non_dessinee": "la part qui PART après la machine "
                 f"({100 - c['chaleur']['rendement_dessine']} % de {h_ch:.0f} px "
                 f"= {h_ch*(1-part):.1f} px, soit {h_ch*(1-part)*274/VW:.2f} px "
                 "rendus dans une carte de 274) n’est pas dessinée : un "
                 "sous-pixel n’est pas une proportion, c’est un arrondi. La "
                 "planche la porte, la vignette la tait — comme elle tait ses "
                 "libellés",
        "bas_du_dessin": f"dernière ligne de commande à {bandes[-1]['cmd']:.0f}, "
                         f"marge basse {VH - bandes[-1]['cmd'] - 4:.0f} px",
    }
    return "\n".join(out) + "\n", controles


def composer_appui_commande(donnees):
    """L'appui du hero : le motif entier à l'échelle 1 — les trois circuits
    nommés par leur local, les deux débits, l'enveloppe traversée et les trois
    lignes de commande avec la zone où chacune naît. Ce qu'il laisse : les
    machines nommées, les légendes de chaleur, la mention et la phrase."""
    c = donnees["commande"]
    elements = sorted(c["elements"], key=lambda e: e["ordre"])
    part = c["chaleur"]["rendement_dessine"] / 100.0
    out = []
    A = out.append
    racine_appui(A, donnees)

    xl0, xl1, xm0, xm1 = A_MARGE, 152, 300, 388
    xe0, xoutf, xfin = 420, 500, 508
    xriser = 344
    h_ch, dec = 16.0, 9.0
    probes = {"machine": xriser, "reseau": 220, "local": 60}
    zones = {"machine": "À LA MACHINE", "reseau": "DANS LE RÉSEAU",
             "local": "DANS LE LOCAL"}
    bandes = _bandes_commande(elements, y0=50, h=38, ecart=36, gap_cmd=18,
                              gap_etiq=18, gap_bande=14)

    A(rect_bord(xe0, 44, 10, bandes[-1]["by1"] + 8 - 44, "calcaire", "filet-1"))
    for e, b in zip(elements, bandes):
        by0, by1, ya, ya2 = b["by0"], b["by1"], b["ya"], b["ya2"]
        A(rect_bord(xl0, by0, xl1 - xl0, by1 - by0, "papier", "filet-1"))
        lib = e["local_lignes"][0] if len(e["local_lignes"]) == 1 else \
            " ".join(e["local_lignes"])
        for k, l in enumerate(replier(lib, 13, xl1 - xl0 - 20, "sans-600")):
            A(texte(xl0 + 10, by0 + 20 + k * 16, l, "sans", 13, 600, "encre",
                    wdth=112))
        A(rect_bord(xm0, by0, xm1 - xm0, by1 - by0, "papier", "filet-1"))
        A(ligne(xl1, ya, xm0, ya, "encre", 1.4))
        A(fleche(240, ya, "encre", "droite", 7))
        A(rect(xl1, ya + dec, xm0 - xl1, h_ch, "encre"))
        A(ligne(xm1, ya, xfin, ya, "encre", 1.4))
        A(fleche(xfin + 8, ya, "encre", "droite", 7))
        if not e["double_flux"]:
            A(rect(xm1, ya + dec, xoutf - xm1, h_ch, "encre"))
        cote = _cote_debit(e)
        if cote:
            A(texte(xl1 + 6, ya - 6, cote, "mono", 10, 500, "encre",
                    tracking=10 * 0.14))
        if e["double_flux"]:
            xg0, xg1 = xm1 - 30, xm1 - 8
            A(rect_bord(xg0, ya - 8, xg1 - xg0, ya2 - ya + 16, "papier",
                        "filet-1"))
            A(ligne(xg0, ya - 8, xg1, ya2 + 8, "encre", 1.4))
            A(ligne(xg0, ya2 + 8, xg1, ya - 8, "encre", 1.4))
            A(ligne(xfin, ya2, xm1, ya2, "encre", 1.4))
            A(fleche(xm1 + 7, ya2, "encre", "gauche", 7))
            A(ligne(xm0, ya2, xl1, ya2, "encre", 1.4))
            A(fleche(xl1 + 7, ya2, "encre", "gauche", 7))
            A(rect(xl1, ya2 + dec, xm0 - xl1, h_ch * part, "encre"))
        xp = probes[e["commande_zone"]]
        if xp != xriser:
            A(ligne(xp, b["cmd"], xriser, b["cmd"], "encre", 1.8))
        A(ligne(xriser, b["cmd"], xriser, by1 + 7, "encre", 1.8))
        A(fleche(xriser, by1, "encre", "haut", 7))
        A(cercle(xp, b["cmd"], 5.5, "papier", "encre", 1.4))
        tag = zones[e["commande_zone"]]
        if e["commande_zone"] == "machine":
            A(texte(xp - 11.5, b["etiq"], tag, "mono", 10, 500, "pivot",
                    ancre="end", tracking=10 * 0.14))
        else:
            A(texte(xp - 5.5, b["etiq"], tag, "mono", 10, 500, "pivot",
                    tracking=10 * 0.14))

    A("</svg>")
    return "\n".join(out) + "\n", controles_appui(
        motif="trois circuits nommés par leur local, les deux débits portés, "
              "l’enveloppe traversée, et les trois lignes de commande avec la "
              "zone où chacune naît ; la chaleur emportée du local et celle qui "
              "revient au troisième — machines nommées, légendes, mention et "
              "phrase laissées à la planche",
        proportion_non_dessinee="la part qui PART après la machine vaudrait "
              f"{h_ch * (1 - part):.1f} px à l’échelle 1 : indiscernable du "
              "conduit de 1,4 px qui la surmonte. Même arbitrage qu’à la "
              "vignette — seule la planche, à 1152, la dessine",
        bas=f"dernière étiquette de commande à {bandes[-1]['etiq']:.0f}, marge "
            f"basse {AH - bandes[-1]['etiq'] - 4:.0f} px",
        longueurs_de_commande="/".join(
            str(xriser - probes[e["commande_zone"]]) for e in elements) + " px")


# ─────────────────────────────────────────────────────────────────────────────
# Mécanisme `terminaux` — des équipements par local, aucune production centrale
# Huitième emploi, mairie des Portes-en-Ré (2026-08-27, reprise sur arbitrage
# FT2E : la planche schématise la solution technique, pas le déroulé de
# l'affaire). Six cellules de locaux portent chacune leur équipement propre
# (une marque encrée + son intitulé) ; le seul réseau est l'air — trois
# flèches entrantes par les menuiseries, quatre lignes qui convergent vers
# trois groupes d'extraction dimensionnés par zone et le caisson régulé du
# local serveur. Texte masqué : six boîtes à marque propre, des flèches
# entrantes, quatre lignes vers quatre petites boîtes, AUCUN nœud central —
# la décentralisation est la démonstration. Les cellules sont des bandes
# topologiques d'égale taille : aucune implantation réelle (règle 4).
# Constantes préfixées TX_ — deux affectations d'un même nom au niveau du
# module se marchent dessus, et c'est le premier dessin qui se recompose faux.
# ─────────────────────────────────────────────────────────────────────────────

TX_ARR0 = 66                    # la menuiserie (tick) et le départ des flèches
TX_LX0, TX_LX1 = 148, 620       # les cellules de locaux
TX_GX0, TX_GX1 = 920, 1144      # les groupes d'extraction
TX_Y0 = 248                     # haut de la première cellule
TX_H_CEL = 56
TX_ECART = 12
TX_H_GRP = 48


def composer_terminaux(donnees):
    tx = donnees["terminaux"]
    locaux = sorted(tx["locaux"], key=lambda l: l["ordre"])
    groupes = {g["cle"]: g for g in tx["groupes"]}
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

    # ── En-tête + double légende courte (le signe toujours doublé d'un mot) ──
    leg_eq = tx["legende_equipement_court"]
    leg_air = tx["legende_air_court"]
    l_air = mesurer(leg_air, 10, "mono", 10 * 0.14)
    x_fl = W - MARGE - l_air - 30
    A(ligne(x_fl, Y_ENTETE - 3.5, x_fl + 16, Y_ENTETE - 3.5, "encre", 1.5))
    A(fleche(x_fl + 22, Y_ENTETE - 3.5, "encre", direction="droite", taille=7))
    A(texte(W - MARGE, Y_ENTETE, leg_air, "mono", 10, 500, "pivot",
            ancre="end", tracking=10 * 0.14))
    l_eq = mesurer(leg_eq, 10, "mono", 10 * 0.14)
    x_chip = x_fl - 24 - l_eq - 15
    A(rect(x_chip, Y_ENTETE - 7.5, 7, 7, "encre"))
    A(texte(x_fl - 24, Y_ENTETE, leg_eq, "mono", 10, 500, "pivot",
            ancre="end", tracking=10 * 0.14))
    controler("en-tête schéma", tx["entete"], 10, "mono",
              x_chip - 24 - MARGE, 10 * 0.14)
    A(texte(MARGE, Y_ENTETE, tx["entete"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))

    # ── Les deux registres ───────────────────────────────────────────────────
    A(texte(MARGE, Y_REGISTRES, tx["registres"]["gauche"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    A(texte(W - MARGE, Y_REGISTRES, tx["registres"]["droite"], "mono", 10, 500,
            "pivot", ancre="end", tracking=10 * 0.14))

    # ── Les six cellules, leurs équipements, leurs flux ──────────────────────
    cys = {}
    for i, lo in enumerate(locaux):
        y = TX_Y0 + i * (TX_H_CEL + TX_ECART)
        cy = y + TX_H_CEL / 2
        cys[lo["cle"]] = cy
        A(rect_bord(TX_LX0, y, TX_LX1 - TX_LX0, TX_H_CEL, "papier", "filet-1"))
        controler(f'libellé {lo["cle"]}', lo["libelle"], 15, "sans-600",
                  TX_LX1 - TX_LX0 - 32)
        A(texte(TX_LX0 + 16, y + 23, lo["libelle"], "sans", 15, 600,
                "encre", wdth=112))
        if lo["equipement"]:
            A(rect(TX_LX0 + 16, y + 37, 7, 7, "encre"))
            controler(f'équipement {lo["cle"]}', lo["equipement"], 10, "mono",
                      TX_LX1 - TX_LX0 - 46, 10 * 0.14)
            A(texte(TX_LX0 + 30, y + 44, lo["equipement"], "mono", 10, 500,
                    "pivot", tracking=10 * 0.14))
        if lo["entree_air"]:
            A(ligne(TX_ARR0, cy - 8, TX_ARR0, cy + 8, "encre", 1.5))
            A(ligne(TX_ARR0, cy, TX_LX0 - 10, cy, "encre", 1.5))
            A(fleche(TX_LX0 - 3, cy, "encre", direction="droite", taille=8))

    # ── Les groupes d'extraction, alignés sur leur local ─────────────────────
    ordre_groupes = [lo["extraction"] for lo in locaux if lo["extraction"]]
    for cle in ordre_groupes:
        g = groupes[cle]
        cy = cys[cle]
        y = cy - TX_H_GRP / 2
        A(ligne(TX_LX1, cy, TX_GX0 - 10, cy, "encre", 1.5))
        A(fleche(TX_GX0 - 3, cy, "encre", direction="droite", taille=8))
        A(rect_bord(TX_GX0, y, TX_GX1 - TX_GX0, TX_H_GRP, "papier", "filet-1"))
        controler(f'groupe {cle}', g["libelle"], 13, "sans-600",
                  TX_GX1 - TX_GX0 - 24)
        A(texte(TX_GX0 + 12, y + 20, g["libelle"], "sans", 13, 600,
                "encre", wdth=112))
        # Forme courte dans la boîte — la forme longue vit au JSON et à l’aria.
        det = g.get("detail_court", g["detail"])
        valeur = g["affichee"] + (" · " + det if det else "")
        controler(f'valeur {cle}', valeur, 10, "mono",
                  TX_GX1 - TX_GX0 - 24, 10 * 0.14)
        A(texte(TX_GX0 + 12, y + 38, valeur, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))

    # ── Phrase de principe, pleine largeur ───────────────────────────────────
    controler("phrase de principe", donnees["phrase_principe"], 17,
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

    n_eq = sum(1 for lo in locaux if lo["equipement"])
    n_arr = sum(1 for lo in locaux if lo["entree_air"])
    bas_cellules = TX_Y0 + len(locaux) * TX_H_CEL + (len(locaux) - 1) * TX_ECART
    controles = {
        "gabarit": f"{W} x {H} — rapport {W/H:.4f} (3:2 exact)",
        "demonstration": f"{len(locaux)} cellules dont {n_eq} à équipement "
                         f"propre (marque encrée), {n_arr} flèches d’air "
                         f"entrantes, {len(ordre_groupes)} lignes horizontales "
                         f"menant chacune à sa boîte "
                         f"d’extraction alignées chacune sur son local — aucun "
                         f"nœud central sur la planche : la décentralisation "
                         f"est portée par la géométrie seule",
        "topologie": f"menuiseries x {TX_ARR0}, cellules x {TX_LX0}–{TX_LX1}, "
                     f"groupes x {TX_GX0}–{TX_GX1} ; cellules y {TX_Y0}–"
                     f"{bas_cellules}",
        "bas_du_dessin": f"cellules jusqu’à y {bas_cellules}, phrase à "
                         f"{Y_PHRASE}, cartouche {Y_CARTOUCHE}–"
                         f"{Y_CARTOUCHE + H_CARTOUCHE}, marge basse "
                         f"{H - (Y_CARTOUCHE + H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur * H_CARTOUCHE} px², soit "
                            f"{largeur * H_CARTOUCHE / (W * H) * 100:.2f} % de "
                            f"la planche",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l’échelle "
                         f"0,96 (1152 / {W})",
        "depassements": depassements if depassements
                        else "aucun — toutes les lignes mesurées sous leur colonne",
    }
    return "\n".join(out) + "\n", controles


def composer_vignette_terminaux(donnees):
    """La vignette : le motif seul — six cellules à marque propre, trois
    flèches entrantes, quatre lignes vers quatre boîtes chiffrées. Libellés
    et légendes laissés à la planche ; quatre valeurs se lisent."""
    tx = donnees["terminaux"]
    locaux = sorted(tx["locaux"], key=lambda l: l["ordre"])
    groupes = {g["cle"]: g for g in tx["groupes"]}
    x_arr, lx0, lx1 = 8, 24, 140
    gx0, gx1 = 204, 286
    y0, h_cel, ecart = 44, 16, 6
    h_grp = 18

    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false" '
      f'style="width:100%;height:auto;display:block">')
    entete_style(A)
    A(rect(0, 0, VW, VH, "papier"))
    A(texte(V_MARGE, 22, donnees["vignette_surtitre"], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    cys = {}
    for i, lo in enumerate(locaux):
        y = y0 + i * (h_cel + ecart)
        cy = y + h_cel / 2
        cys[lo["cle"]] = cy
        A(rect_bord(lx0, y, lx1 - lx0, h_cel, "papier", "filet-1"))
        if lo["equipement"]:
            A(rect(lx0 + 6, cy - 2.5, 5, 5, "encre"))
        if lo["entree_air"]:
            A(ligne(x_arr, cy, lx0 - 7, cy, "encre", 1.2))
            A(fleche(lx0 - 2, cy, "encre", direction="droite", taille=5))

    for cle in [lo["extraction"] for lo in locaux if lo["extraction"]]:
        g = groupes[cle]
        cy = cys[cle]
        y = cy - h_grp / 2
        A(ligne(lx1, cy, gx0 - 7, cy, "encre", 1.2))
        A(fleche(gx0 - 2, cy, "encre", direction="droite", taille=5))
        A(rect_bord(gx0, y, gx1 - gx0, h_grp, "papier", "filet-1"))
        A(texte(gx0 + 8, cy + 3.5, g["affichee"], "mono", 10, 500, "pivot",
                tracking=10 * 0.14))

    A("</svg>")
    bas = y0 + len(locaux) * h_cel + (len(locaux) - 1) * ecart
    controles = {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": f"carte de projet mesurée de 274 à 296 px — "
                            f"échelle {274/VW:.2f} à {296/VW:.2f}",
        "corps_minimal": f"9 px dans le repère — rendu à {9*274/VW:.1f} px au pire cas",
        "motif": f"le motif seul : {len(locaux)} cellules à marque propre, "
                 f"trois flèches entrantes, quatre lignes vers quatre boîtes "
                 f"chiffrées (les débits) — libellés et légendes laissés à la "
                 f"planche",
        "bas_du_dessin": f"{bas:.0f} px, marge basse {VH - bas:.0f} px",
    }
    return "\n".join(out) + "\n", controles


def composer_appui_terminaux(donnees):
    """L'appui du hero : le motif entier à l'échelle 1 — les six cellules
    nommées en court, leurs équipements en court, les flux et les quatre
    boîtes chiffrées. Sans phrase de principe ni cartouche."""
    tx = donnees["terminaux"]
    locaux = sorted(tx["locaux"], key=lambda l: l["ordre"])
    groupes = {g["cle"]: g for g in tx["groupes"]}
    x_arr, lx0, lx1 = 8, 24, 300
    gx0, gx1 = 392, AW - A_MARGE
    y0, h_cel, ecart = 64, 34, 8
    h_grp = 34

    out = []
    A = out.append
    racine_appui(A, donnees)

    leg_eq = tx["legende_equipement_court"]
    l_eq = mesurer(leg_eq, 10, "mono", 10 * 0.14)
    A(rect(gx1 - l_eq - 15, 27.5, 6, 6, "encre"))
    A(texte(gx1, 34, leg_eq, "mono", 10, 500, "pivot",
            ancre="end", tracking=10 * 0.14))

    cys = {}
    for i, lo in enumerate(locaux):
        y = y0 + i * (h_cel + ecart)
        cy = y + h_cel / 2
        cys[lo["cle"]] = cy
        A(rect_bord(lx0, y, lx1 - lx0, h_cel, "papier", "filet-1"))
        A(texte(lx0 + 10, y + 15, lo["libelle_court"], "sans", 13, 600,
                "encre", wdth=112))
        if lo["equipement_court"]:
            A(rect(lx0 + 10, y + 23, 5, 5, "encre"))
            A(texte(lx0 + 21, y + 29, lo["equipement_court"], "mono", 10, 500,
                    "pivot", tracking=10 * 0.14))
        if lo["entree_air"]:
            A(ligne(x_arr, cy, lx0 - 8, cy, "encre", 1.5))
            A(fleche(lx0 - 2, cy, "encre", direction="droite", taille=6))

    for cle in [lo["extraction"] for lo in locaux if lo["extraction"]]:
        g = groupes[cle]
        cy = cys[cle]
        y = cy - h_grp / 2
        A(ligne(lx1, cy, gx0 - 8, cy, "encre", 1.5))
        A(fleche(gx0 - 2, cy, "encre", direction="droite", taille=6))
        A(rect_bord(gx0, y, gx1 - gx0, h_grp, "papier", "filet-1"))
        valeur = g["affichee"] + (" · SONDE" if g["detail"] else "")
        A(texte(gx0 + 10, cy + 3.5, valeur, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))

    A("</svg>")
    bas = y0 + len(locaux) * h_cel + (len(locaux) - 1) * ecart
    return "\n".join(out) + "\n", controles_appui(
        motif=f"le motif entier : {len(locaux)} cellules nommées avec leur "
              f"équipement en court, trois flèches entrantes, quatre lignes "
              f"vers quatre boîtes chiffrées — la légende courte de "
              f"l’équipement en tête ; phrase et cartouche laissés à la planche",
        bas=f"cellules jusqu’à y {bas} px, marge basse {AH - bas} px")


# ─────────────────────────────────────────────────────────────────────────────
# Mécanisme `comptage` — où se pose le compteur, et quel bâtiment se compte
# par soustraction. Neuvième emploi, plan de comptage de l'énergie de
# chauffage d'un site industriel de Rochefort (2026-08-31, session N09).
# L'archétype est lu au RETOUR : la chaufferie envoie un départ unique vers
# quatre bâtiments, et chaque retour revient au collecteur à travers un
# compteur — sauf celui du bâtiment trop ramifié, qui n'en reçoit aucun et
# se déduit du compteur général posé sur le retour commun. Texte masqué : une
# boîte de production, deux collecteurs verticaux, quatre allers, quatre
# retours dont trois portent un cercle (un en porte trois) et un qui se
# termine en éventail sans cercle, un cercle seul sur le tronc de retour —
# la soustraction est portée par la géométrie. En regard, le bilan du site :
# quatre rangs de marques, carré plein pour l'existant, cercle vide pour ce
# qui reste à poser. Les cellules sont des bandes topologiques d'égale
# taille : aucune implantation réelle (règle 4). Constantes préfixées CP_ —
# deux affectations d'un même nom au niveau du module se marchent dessus.
# ─────────────────────────────────────────────────────────────────────────────

CP_CX0, CP_CX1 = 56, 190        # la chaufferie
CP_XA, CP_XR = 250, 282         # les deux collecteurs verticaux : aller, retour
CP_BX0, CP_BX1 = 500, 700       # les cellules de bâtiment
CP_H_BAT = 44
CP_Y0 = 322                     # ordonnée du premier rang
CP_PAS = 72                     # pas des rangs
CP_DEC = 8                      # demi-écart aller / retour dans un rang
CP_XC = 420                     # le compteur d'un bâtiment à un compteur
CP_PAS_C = 54                   # pas entre les compteurs d'un même bâtiment
CP_R = 9                        # rayon du compteur
CP_XSEP = 730                   # filet séparant les deux registres
CP_RX0, CP_RX1 = 760, 1144      # le registre du site
CP_PAS_MARQUE = 20              # pas des marques du bilan
CP_Y_TOTAUX = 606               # la ligne des totaux


def _cp_compteur(A, x, y, r):
    """Le compteur d'énergie : un cercle vide sur le retour — même signe que
    « à installer » au bilan, puisque tous ceux de la chaufferie le sont."""
    A(cercle(x, y, r, "papier", "encre", 1.5))


def _cp_eventail(A, x0, x1, y, n, pas):
    """Les ramifications du bâtiment sans compteur : n lignes divergentes qui
    naissent du retour et entrent dans la cellule à des hauteurs différentes."""
    for k in range(n):
        yk = y - pas * (n - 1) / 2 + pas * k
        A(ligne(x0, y, x1, yk, "encre", 1.2))


def composer_comptage(donnees):
    cp = donnees["comptage"]
    bats = sorted(cp["batiments"], key=lambda b: b["ordre"])
    bilan = sorted(cp["bilan"], key=lambda b: b["ordre"])
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

    # ── En-tête + double légende (le signe toujours doublé d'un mot) ────────
    leg_ex, leg_ai = cp["legende_existant"], cp["legende_a_installer"]
    l_ai = mesurer(leg_ai, 10, "mono", 10 * 0.14)
    x_ai = W - MARGE - l_ai
    A(cercle(x_ai - 13, Y_ENTETE - 3.5, 4.5, "papier", "encre", 1.5))
    A(texte(W - MARGE, Y_ENTETE, leg_ai, "mono", 10, 500, "pivot",
            ancre="end", tracking=10 * 0.14))
    x_ex1 = x_ai - 13 - 4.5 - 26
    l_ex = mesurer(leg_ex, 10, "mono", 10 * 0.14)
    A(rect(x_ex1 - l_ex - 15, Y_ENTETE - 7.5, 7, 7, "encre"))
    A(texte(x_ex1, Y_ENTETE, leg_ex, "mono", 10, 500, "pivot",
            ancre="end", tracking=10 * 0.14))
    controler("en-tête schéma", cp["entete"], 10, "mono",
              x_ex1 - l_ex - 15 - 24 - MARGE, 10 * 0.14)
    A(texte(MARGE, Y_ENTETE, cp["entete"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))

    # ── Les deux registres ───────────────────────────────────────────────────
    controler("registre gauche", cp["registres"]["gauche"], 10, "mono",
              CP_XSEP - 24 - MARGE, 10 * 0.14)
    A(texte(MARGE, Y_REGISTRES, cp["registres"]["gauche"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    controler("registre droit", cp["registres"]["droite"], 10, "mono",
              CP_RX1 - CP_RX0, 10 * 0.14)
    A(texte(W - MARGE, Y_REGISTRES, cp["registres"]["droite"], "mono", 10, 500,
            "pivot", ancre="end", tracking=10 * 0.14))
    A(ligne(CP_XSEP, Y_REGISTRES + 20, CP_XSEP, CP_Y_TOTAUX + 10, "filet-2", 1))

    # ── La chaufferie et ses deux collecteurs ────────────────────────────────
    cys = [CP_Y0 + i * CP_PAS for i in range(len(bats))]
    ya_tr = cys[0] - CP_DEC                # le tronc aller, au premier rang
    yr_tr = cys[-1] + CP_DEC               # le tronc retour, au dernier rang
    cy0, cy1 = ya_tr - 22, yr_tr + 20
    A(rect_bord(CP_CX0, cy0, CP_CX1 - CP_CX0, cy1 - cy0, "calcaire", "filet-1"))
    ch = cp["chaufferie"]
    controler("chaufferie", ch["libelle"], 15, "sans-600", CP_CX1 - CP_CX0 - 32)
    A(texte(CP_CX0 + 16, cy0 + 30, ch["libelle"], "sans", 15, 600, "encre", wdth=112))
    for k, d in enumerate(ch["details"]):
        controler(f"chaufferie détail {k}", d, 10, "mono", CP_CX1 - CP_CX0 - 32, 10 * 0.14)
        A(texte(CP_CX0 + 16, cy0 + 50 + 16 * k, d, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))
    # tronc aller → collecteur aller
    A(ligne(CP_CX1, ya_tr, CP_XA, ya_tr, "encre", 1.5))
    A(ligne(CP_XA, ya_tr, CP_XA, cys[-1] - CP_DEC, "encre", 1.5))
    A(texte(CP_CX1 + 6, ya_tr - 6, cp["legende_aller"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    # collecteur retour → tronc retour → chaufferie, à travers le compteur général
    A(ligne(CP_XR, cys[0] + CP_DEC, CP_XR, yr_tr, "encre", 1.5))
    A(ligne(CP_XR, yr_tr, CP_CX1 + 8, yr_tr, "encre", 1.5))
    A(fleche(CP_CX1 + 1, yr_tr, "encre", direction="gauche", taille=8))
    x_tot = (CP_CX1 + CP_XR) / 2
    _cp_compteur(A, x_tot, yr_tr, CP_R)
    A(texte(CP_CX1 + 6, yr_tr - 14, cp["legende_retour"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    tot = cp["total"]
    l_tot = controler("total", tot["affichee"], 10, "mono", 200, 10 * 0.14)
    A(texte(x_tot, yr_tr + 24, tot["affichee"], "mono", 10, 500, "encre",
            ancre="middle", tracking=10 * 0.14))

    # ── Les quatre rangs : aller, cellule, retour et ses compteurs ───────────
    n_compteurs = 0
    n_fans = 0
    for b, cy in zip(bats, cys):
        ya, yr = cy - CP_DEC, cy + CP_DEC
        # l'aller franchit le collecteur retour sans s'y raccorder : un saut
        if cy > cys[0]:
            A(ligne(CP_XA, ya, CP_XR - 5, ya, "encre", 1.5))
            A(ligne(CP_XR + 5, ya, CP_BX0 - 8, ya, "encre", 1.5))
        else:
            A(ligne(CP_XA, ya, CP_BX0 - 8, ya, "encre", 1.5))
        A(fleche(CP_BX0 - 1, ya, "encre", direction="droite", taille=8))
        A(rect_bord(CP_BX0, cy - CP_H_BAT / 2, CP_BX1 - CP_BX0, CP_H_BAT,
                    "papier", "filet-1"))
        controler(f'libellé {b["cle"]}', b["libelle"], 15, "sans-600",
                  CP_BX1 - CP_BX0 - 32)
        A(texte(CP_BX0 + 16, cy - 2, b["libelle"], "sans", 15, 600, "encre", wdth=112))
        controler(f'détail {b["cle"]}', b["detail"], 10, "mono",
                  CP_BX1 - CP_BX0 - 32, 10 * 0.14)
        A(texte(CP_BX0 + 16, cy + 15, b["detail"], "mono", 10, 500, "pivot",
                tracking=10 * 0.14))
        # le retour, du bâtiment au collecteur
        A(ligne(CP_BX0, yr, CP_XR + 8, yr, "encre", 1.5))
        A(fleche(CP_XR + 1, yr, "encre", direction="gauche", taille=8))
        n = len(b["compteurs"])
        for k, c in enumerate(b["compteurs"]):
            x = CP_XC + (k - (n - 1) / 2) * CP_PAS_C
            _cp_compteur(A, x, yr, CP_R)
            controler(f'compteur {c["cle"]}', c["affichee"], 10, "mono",
                      CP_PAS_C - 6, 10 * 0.14)
            A(texte(x, yr + 24, c["affichee"], "mono", 10, 500, "pivot",
                    ancre="middle", tracking=10 * 0.14))
            n_compteurs += 1
        if b.get("soustraction"):
            _cp_eventail(A, CP_BX0 - 72, CP_BX0, yr, b["ramifications"], 6)
            n_fans += 1
            # la formule sous l'éventail, calée à droite — la ligne du total,
            # centrée sous son cercle, garde sa propre place à gauche
            controler("formule de soustraction", b["formule"], 10, "mono",
                      CP_BX0 - 8 - (x_tot + 60), 10 * 0.14)
            A(texte(CP_BX0 - 8, yr + 24, b["formule"], "mono", 10, 500, "encre",
                    ancre="end", tracking=10 * 0.14))

    # ── Le bilan du site : quatre rangs de marques ───────────────────────────
    n_ex = n_ai = 0
    for r, cy in zip(bilan, cys):
        controler(f'bilan {r["cle"]}', r["libelle"], 13, "sans-600", CP_RX1 - CP_RX0)
        A(texte(CP_RX0, cy - 10, r["libelle"], "sans", 13, 600, "encre", wdth=112))
        x = CP_RX0 + 4
        for _ in range(r["existants"]):
            A(rect(x - 4, cy + 2, 8, 8, "encre"))
            x += CP_PAS_MARQUE
            n_ex += 1
        for _ in range(r["a_installer"]):
            A(cercle(x, cy + 6, 4.5, "papier", "encre", 1.5))
            x += CP_PAS_MARQUE
            n_ai += 1
        controler(f'bilan détail {r["cle"]}', r["detail"], 10, "mono",
                  CP_RX1 - CP_RX0, 10 * 0.14)
        A(texte(CP_RX0, cy + 26, r["detail"], "mono", 10, 500, "pivot",
                tracking=10 * 0.14))
    A(rect(CP_RX0, CP_Y_TOTAUX - 18, CP_RX1 - CP_RX0, 1, "filet-2"))
    controler("totaux", cp["totaux"]["affichee"], 10, "mono",
              CP_RX1 - CP_RX0, 10 * 0.14)
    A(texte(CP_RX0, CP_Y_TOTAUX, cp["totaux"]["affichee"], "mono", 10, 500,
            "encre", tracking=10 * 0.14))

    # ── Phrase de principe, pleine largeur ───────────────────────────────────
    controler("phrase de principe", donnees["phrase_principe"], 17,
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

    assert n_ex == cp["totaux"]["existants"] and n_ai == cp["totaux"]["a_installer"], \
        "le bilan dessiné ne somme pas comme les totaux de l’extraction"
    bas_gauche = yr_tr + 24
    controles = {
        "gabarit": f"{W} x {H} — rapport {W/H:.4f} (3:2 exact)",
        "demonstration": f"chaufferie O : un tronc aller, un collecteur, {len(bats)} "
                         f"cellules, {len(bats)} retours dont {len(bats) - n_fans} "
                         f"portent {n_compteurs} cercles et {n_fans} se termine en "
                         f"éventail sans cercle, un cercle seul sur le tronc de "
                         f"retour — la soustraction est portée par la géométrie ; "
                         f"bilan du site : {n_ex} carrés pleins et {n_ai} cercles "
                         f"vides sur {len(bilan)} rangs, la somme vaut celle de "
                         f"l’extraction",
        "topologie": f"chaufferie x {CP_CX0}–{CP_CX1} y {cy0}–{cy1}, collecteurs "
                     f"x {CP_XA} (aller) et {CP_XR} (retour), compteurs autour de "
                     f"x {CP_XC} au pas {CP_PAS_C}, cellules x {CP_BX0}–{CP_BX1} ; "
                     f"rangs y {cys[0]}–{cys[-1]} au pas {CP_PAS} ; bilan "
                     f"x {CP_RX0}–{CP_RX1}, totaux y {CP_Y_TOTAUX}",
        "bas_du_dessin": f"formule et total à y {bas_gauche}, totaux du bilan à "
                         f"{CP_Y_TOTAUX}, phrase à {Y_PHRASE}, cartouche "
                         f"{Y_CARTOUCHE}–{Y_CARTOUCHE + H_CARTOUCHE}, marge basse "
                         f"{H - (Y_CARTOUCHE + H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur * H_CARTOUCHE} px², soit "
                            f"{largeur * H_CARTOUCHE / (W * H) * 100:.2f} % de "
                            f"la planche",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l’échelle "
                         f"0,96 (1152 / {W})",
        "depassements": depassements if depassements
                        else "aucun — toutes les lignes mesurées sous leur colonne",
    }
    return "\n".join(out) + "\n", controles


def composer_vignette_comptage(donnees):
    """La vignette : le motif de la chaufferie seul — la boîte, les deux
    collecteurs, quatre allers, quatre retours, les cercles et l'éventail, le
    cercle du tronc. Les diamètres se lisent en mono 9 ; le bilan reste à la
    planche."""
    cp = donnees["comptage"]
    bats = sorted(cp["batiments"], key=lambda b: b["ordre"])
    cx0, cx1 = V_MARGE, 58
    xa, xr = 76, 90
    bx0, bx1 = 212, VW - V_MARGE
    h_bat, y0, pas, dec, r = 20, 66, 30, 4, 3.5
    xc, pas_c = 152, 36

    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false" '
      f'style="width:100%;height:auto;display:block">')
    entete_style(A)
    A(rect(0, 0, VW, VH, "papier"))
    A(texte(V_MARGE, 22, donnees["vignette_surtitre"], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    cys = [y0 + i * pas for i in range(len(bats))]
    ya_tr, yr_tr = cys[0] - dec, cys[-1] + dec
    cy0, cy1 = ya_tr - 12, yr_tr + 12
    A(rect_bord(cx0, cy0, cx1 - cx0, cy1 - cy0, "calcaire", "filet-1"))
    A(ligne(cx1, ya_tr, xa, ya_tr, "encre", 1.2))
    A(ligne(xa, ya_tr, xa, cys[-1] - dec, "encre", 1.2))
    A(ligne(xr, cys[0] + dec, xr, yr_tr, "encre", 1.2))
    A(ligne(xr, yr_tr, cx1 + 5, yr_tr, "encre", 1.2))
    A(fleche(cx1 + 1, yr_tr, "encre", direction="gauche", taille=5))
    x_tot = (cx1 + xr) / 2
    _cp_compteur(A, x_tot, yr_tr, r)
    A(texte(cx1 + 4, yr_tr + 14, cp["total"]["affichee_courte"], "mono", 9, 500,
            "pivot", tracking=9 * 0.14))

    for b, cy in zip(bats, cys):
        ya, yr = cy - dec, cy + dec
        if cy > cys[0]:
            A(ligne(xa, ya, xr - 3, ya, "encre", 1.2))
            A(ligne(xr + 3, ya, bx0 - 5, ya, "encre", 1.2))
        else:
            A(ligne(xa, ya, bx0 - 5, ya, "encre", 1.2))
        A(fleche(bx0 - 1, ya, "encre", direction="droite", taille=5))
        A(rect_bord(bx0, cy - h_bat / 2, bx1 - bx0, h_bat, "papier", "filet-1"))
        A(texte(bx0 + 8, cy + 4, b["libelle_court"], "sans", 12, 600, "encre", wdth=112))
        A(ligne(bx0, yr, xr + 5, yr, "encre", 1.2))
        A(fleche(xr + 1, yr, "encre", direction="gauche", taille=5))
        n = len(b["compteurs"])
        for k, c in enumerate(b["compteurs"]):
            x = xc + (k - (n - 1) / 2) * pas_c
            _cp_compteur(A, x, yr, r)
            # Trois étiquettes de 38 px ne tiennent pas dans les 122 px entre
            # le collecteur et la cellule : seul le compteur unique porte son
            # diamètre, les trois de l'autre rang restent des cercles (leurs
            # valeurs vivent à la planche et au JSON).
            if n == 1:
                A(texte(x, yr + 13, c["affichee"], "mono", 9, 500, "pivot",
                        ancre="middle", tracking=9 * 0.14))
        if b.get("soustraction"):
            _cp_eventail(A, bx0 - 36, bx0, yr, 3, 6)
            # sous la cellule, calée à son bord droit — hors de la ligne du
            # diamètre du tronc
            A(texte(bx1, cy + h_bat / 2 + 12, b["formule_courte"], "mono", 9, 500,
                    "encre", ancre="end", tracking=9 * 0.14))

    A("</svg>")
    bas = max(cy1, yr_tr + 14, cys[-1] + h_bat / 2 + 12)
    controles = {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": f"carte de projet mesurée de 274 à 296 px — "
                            f"échelle {274/VW:.2f} à {296/VW:.2f}",
        "corps_minimal": f"9 px dans le repère — rendu à {9*274/VW:.1f} px au pire cas",
        "motif": f"le motif seul : la chaufferie, deux collecteurs, {len(bats)} "
                 f"allers et retours, les cercles des compteurs avec leur diamètre, "
                 f"l’éventail du bâtiment sans compteur et sa formule courte, le "
                 f"cercle du tronc — bilan, légendes et phrase laissés à la planche",
        "bas_du_dessin": f"{bas:.0f} px, marge basse {VH - bas:.0f} px",
    }
    return "\n".join(out) + "\n", controles


def composer_appui_comptage(donnees):
    """L'appui du hero : le motif de la chaufferie à l'échelle 1 — cellules
    nommées, détails en court, compteurs et diamètres, formule de soustraction,
    la légende du compteur à installer. Sans bilan, phrase ni cartouche."""
    cp = donnees["comptage"]
    bats = sorted(cp["batiments"], key=lambda b: b["ordre"])
    # La boîte fait 98 px : « Chaufferie O » en 13/600 mesure 75 px aux avances
    # calibrées et ~90 au rendu (les sans-600 sous-mesurent d'environ 20 %,
    # relevé N08) — 30 px de marge, pas 12.
    cx0, cx1 = A_MARGE, 122
    xa, xr = 154, 176
    bx0, bx1 = 392, AW - A_MARGE
    h_bat, y0, pas, dec, r = 36, 96, 64, 7, 6
    xc, pas_c = 284, 52

    out = []
    A = out.append
    racine_appui(A, donnees)

    leg_ai = cp["legende_a_installer"]
    l_ai = mesurer(leg_ai, 10, "mono", 10 * 0.14)
    A(cercle(bx1 - l_ai - 12, 30.5, 4, "papier", "encre", 1.5))
    A(texte(bx1, 34, leg_ai, "mono", 10, 500, "pivot", ancre="end",
            tracking=10 * 0.14))

    cys = [y0 + i * pas for i in range(len(bats))]
    ya_tr, yr_tr = cys[0] - dec, cys[-1] + dec
    cy0, cy1 = ya_tr - 20, yr_tr + 20
    A(rect_bord(cx0, cy0, cx1 - cx0, cy1 - cy0, "calcaire", "filet-1"))
    ch = cp["chaufferie"]
    A(texte(cx0 + 12, cy0 + 26, ch["libelle_court"], "sans", 13, 600, "encre", wdth=112))
    for k, d in enumerate(ch["details"]):
        A(texte(cx0 + 12, cy0 + 44 + 15 * k, d, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))
    A(ligne(cx1, ya_tr, xa, ya_tr, "encre", 1.5))
    A(ligne(xa, ya_tr, xa, cys[-1] - dec, "encre", 1.5))
    A(texte(cx1 + 6, ya_tr - 6, cp["legende_aller"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    A(ligne(xr, cys[0] + dec, xr, yr_tr, "encre", 1.5))
    A(ligne(xr, yr_tr, cx1 + 7, yr_tr, "encre", 1.5))
    A(fleche(cx1 + 1, yr_tr, "encre", direction="gauche", taille=6))
    x_tot = (cx1 + xr) / 2
    _cp_compteur(A, x_tot, yr_tr, r)
    A(texte(cx1 + 6, yr_tr + 14, cp["legende_retour"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    A(texte(x_tot, cy1 + 16, cp["total"]["affichee"], "mono", 10, 500, "encre",
            ancre="middle", tracking=10 * 0.14))

    for b, cy in zip(bats, cys):
        ya, yr = cy - dec, cy + dec
        if cy > cys[0]:
            A(ligne(xa, ya, xr - 4, ya, "encre", 1.5))
            A(ligne(xr + 4, ya, bx0 - 7, ya, "encre", 1.5))
        else:
            A(ligne(xa, ya, bx0 - 7, ya, "encre", 1.5))
        A(fleche(bx0 - 1, ya, "encre", direction="droite", taille=6))
        A(rect_bord(bx0, cy - h_bat / 2, bx1 - bx0, h_bat, "papier", "filet-1"))
        A(texte(bx0 + 10, cy - 3, b["libelle_court"], "sans", 13, 600, "encre", wdth=112))
        A(texte(bx0 + 10, cy + 13, b["detail"], "mono", 10, 500, "pivot",
                tracking=10 * 0.14))
        A(ligne(bx0, yr, xr + 7, yr, "encre", 1.5))
        A(fleche(xr + 1, yr, "encre", direction="gauche", taille=6))
        n = len(b["compteurs"])
        for k, c in enumerate(b["compteurs"]):
            x = xc + (k - (n - 1) / 2) * pas_c
            _cp_compteur(A, x, yr, r)
            A(texte(x, yr + 20, c["affichee"], "mono", 10, 500, "pivot",
                    ancre="middle", tracking=10 * 0.14))
        if b.get("soustraction"):
            _cp_eventail(A, bx0 - 50, bx0, yr, b["ramifications"], 6)
            A(texte(xr + 12, yr + 20, b["formule_courte"], "mono", 10, 500, "encre",
                    tracking=10 * 0.14))

    A("</svg>")
    bas = cy1 + 16
    return "\n".join(out) + "\n", controles_appui(
        motif=f"le motif entier à l’échelle 1 : la chaufferie nommée, deux "
              f"collecteurs, {len(bats)} cellules nommées avec leur détail en "
              f"court, les cercles des compteurs et leurs diamètres, l’éventail "
              f"et la formule courte du bâtiment compté par soustraction, le "
              f"cercle du tronc avec son diamètre ; la légende du compteur à "
              f"installer en tête — bilan, phrase et cartouche laissés à la planche",
        bas=f"total sous la chaufferie à y {bas} px, marge basse {AH - bas} px")


# ─────────────────────────────────────────────────────────────────────────────
# Mécanisme `cascade` — la puissance s'ajuste au juste besoin. Dixième emploi,
# chaufferie bois granulés du foyer de Saint-Martin-de-Ré (2026-08-31, N10).
# L'archétype dans son sens premier, production → distribution → terminaux,
# mais la thèse est la MODULATION : quatre chaudières identiques s'enclenchent
# en cascade (la quatrième est le secours), un ballon tampon découple la
# production, et trois départs comptés partent en réseau enterré vers trois
# sous-stations. Texte masqué : une réserve qui nourrit quatre cellules
# identiques, leurs sorties rassemblées sur un collecteur vers une cellule
# unique, puis trois branches en pointillé (l'enterré) traversant chacune un
# cercle (le compteur) vers trois cellules — la modulation est portée par la
# répétition du module, le comptage par le cercle sur chaque branche. Bandes
# topologiques d'égale taille : aucune implantation réelle (règle 4).
# Constantes préfixées CA_ — deux affectations d'un même nom au niveau du
# module se marchent dessus (piège tableau-electrique, 2026-08-16).
# ─────────────────────────────────────────────────────────────────────────────

CA_SX0, CA_SX1 = 56, 214        # la pièce de réserve
CA_CHX0, CA_CHX1 = 278, 434     # les quatre chaudières
CA_COLX = 466                   # le collecteur des départs
CA_BX0, CA_BX1 = 506, 648       # le ballon tampon
CA_DISX = 690                   # la ligne verticale de distribution
CA_CPX = 738                    # le compteur de chaque départ
CA_SSX0, CA_SSX1 = 806, 1050    # les sous-stations
CA_CHY0 = 300                   # ordonnée de la première chaudière
CA_CH_H, CA_CH_E = 54, 14       # cellule de chaudière, écart
CA_SS_H, CA_SS_E = 68, 42       # cellule de sous-station, écart
CA_R = 9                        # rayon du compteur


def composer_cascade(donnees):
    ca = donnees["cascade"]
    chaudieres = sorted(ca["chaudieres"], key=lambda c: c["ordre"])
    circuits = sorted(ca["circuits"], key=lambda c: c["ordre"])
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

    # ── En-tête + double légende (le signe toujours doublé d'un mot) ─────────
    leg_cp = ca["legende_compteur"]
    l_cp = mesurer(leg_cp, 10, "mono", 10 * 0.14)
    A(cercle(W - MARGE - l_cp - 16, Y_ENTETE - 3.5, 5, "papier", "encre", 1.5))
    A(texte(W - MARGE, Y_ENTETE, leg_cp, "mono", 10, 500, "pivot",
            ancre="end", tracking=10 * 0.14))
    leg_re = ca["legende_reseau"]
    x_txt_re = W - MARGE - l_cp - 40
    l_re = mesurer(leg_re, 10, "mono", 10 * 0.14)
    A(ligne_pointillee(x_txt_re - l_re - 26, Y_ENTETE - 3.5,
                       x_txt_re - l_re - 8, Y_ENTETE - 3.5, "encre", 1.5))
    A(texte(x_txt_re, Y_ENTETE, leg_re, "mono", 10, 500, "pivot",
            ancre="end", tracking=10 * 0.14))
    controler("en-tête schéma", ca["entete"], 10, "mono",
              x_txt_re - l_re - 50 - MARGE, 10 * 0.14)
    A(texte(MARGE, Y_ENTETE, ca["entete"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))

    # ── Les deux registres ───────────────────────────────────────────────────
    A(texte(MARGE, Y_REGISTRES, ca["registres"]["gauche"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    A(texte(W - MARGE, Y_REGISTRES, ca["registres"]["droite"], "mono", 10, 500,
            "pivot", ancre="end", tracking=10 * 0.14))

    bas_ch = CA_CHY0 + 4 * CA_CH_H + 3 * CA_CH_E
    cy_mid = (CA_CHY0 + bas_ch) / 2

    # ── La pièce de réserve, qui nourrit les quatre chaudières ───────────────
    re_ = ca["reserve"]
    A(rect_bord(CA_SX0, CA_CHY0, CA_SX1 - CA_SX0, bas_ch - CA_CHY0,
                "calcaire", "filet-1"))
    controler("libellé réserve", re_["libelle"], 15, "sans-600",
              CA_SX1 - CA_SX0 - 24)
    A(texte(CA_SX0 + 12, CA_CHY0 + 26, re_["libelle"], "sans", 15, 600,
            "encre", wdth=112))
    for k, d in enumerate(re_["details"]):
        controler(f"détail réserve {k}", d, 10, "mono",
                  CA_SX1 - CA_SX0 - 24, 10 * 0.14)
        A(texte(CA_SX0 + 12, CA_CHY0 + 48 + 16 * k, d, "mono", 10, 500,
                "pivot", tracking=10 * 0.14))

    # ── Les quatre chaudières identiques, alimentées et collectées ───────────
    cys = []
    for i, ch in enumerate(chaudieres):
        y = CA_CHY0 + i * (CA_CH_H + CA_CH_E)
        cy = y + CA_CH_H / 2
        cys.append(cy)
        A(ligne(CA_SX1, cy, CA_CHX0 - 9, cy, "encre", 1.5))
        A(fleche(CA_CHX0 - 2, cy, "encre", direction="droite", taille=7))
        A(rect_bord(CA_CHX0, y, CA_CHX1 - CA_CHX0, CA_CH_H, "papier", "filet-1"))
        controler(f'libellé {ch["cle"]}', ch["libelle"], 13, "sans-600",
                  CA_CHX1 - CA_CHX0 - 24)
        A(texte(CA_CHX0 + 12, y + 21, ch["libelle"], "sans", 13, 600,
                "encre", wdth=112))
        A(texte(CA_CHX0 + 12, y + 39, ch["affichee"], "mono", 10, 500,
                "pivot", tracking=10 * 0.14))
        A(ligne(CA_CHX1, cy, CA_COLX, cy, "encre", 1.5))
    A(ligne(CA_COLX, cys[0], CA_COLX, cys[-1], "encre", 1.5))
    A(ligne(CA_COLX, cy_mid, CA_BX0 - 9, cy_mid, "encre", 1.5))
    A(fleche(CA_BX0 - 2, cy_mid, "encre", direction="droite", taille=7))

    # ── Le total de la cascade et sa règle de conduite ───────────────────────
    controler("total cascade", ca["total"]["affichee"], 10, "mono",
              CA_BX0 - 24 - CA_CHX0, 10 * 0.14)
    A(texte(CA_CHX0, bas_ch + 26, ca["total"]["affichee"], "mono", 10, 500,
            "encre", tracking=10 * 0.14))
    controler("légende cascade", ca["legende_cascade"], 10, "mono",
              CA_DISX - 40 - CA_SX0, 10 * 0.14)
    A(texte(CA_SX0, bas_ch + 50, ca["legende_cascade"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))

    # ── Le ballon tampon, qui découple ───────────────────────────────────────
    ba = ca["ballon"]
    b_y0, b_h = cy_mid - 60, 120
    A(rect_bord(CA_BX0, b_y0, CA_BX1 - CA_BX0, b_h, "papier", "filet-1"))
    controler("libellé ballon", ba["libelle"], 15, "sans-600",
              CA_BX1 - CA_BX0 - 24)
    A(texte(CA_BX0 + 12, b_y0 + 30, ba["libelle"], "sans", 15, 600,
            "encre", wdth=112))
    A(texte(CA_BX0 + 12, b_y0 + 52, ba["affichee"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    A(texte(CA_BX0 + 12, b_y0 + 68, ba["detail"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))

    # ── Trois départs comptés, en réseau enterré, vers trois sous-stations ───
    cys_ss = [cy_mid - (CA_SS_H + CA_SS_E), cy_mid, cy_mid + (CA_SS_H + CA_SS_E)]
    A(ligne(CA_BX1, cy_mid, CA_DISX, cy_mid, "encre", 1.5))
    A(ligne(CA_DISX, cys_ss[0], CA_DISX, cys_ss[-1], "encre", 1.5))
    for ci, cy in zip(circuits, cys_ss):
        A(ligne_pointillee(CA_DISX, cy, CA_SSX0 - 9, cy, "encre", 1.5))
        A(fleche(CA_SSX0 - 2, cy, "encre", direction="droite", taille=7))
        A(cercle(CA_CPX, cy, CA_R, "papier", "encre", 1.5))
        y = cy - CA_SS_H / 2
        A(rect_bord(CA_SSX0, y, CA_SSX1 - CA_SSX0, CA_SS_H, "papier", "filet-1"))
        controler(f'libellé {ci["cle"]}', ci["libelle"], 15, "sans-600",
                  CA_SSX1 - CA_SSX0 - 24)
        A(texte(CA_SSX0 + 12, y + 24, ci["libelle"], "sans", 15, 600,
                "encre", wdth=112))
        controler(f'détail {ci["cle"]}', ci["detail"], 10, "mono",
                  CA_SSX1 - CA_SSX0 - 24, 10 * 0.14)
        A(texte(CA_SSX0 + 12, y + 42, ci["detail"], "mono", 10, 500,
                "pivot", tracking=10 * 0.14))
        if ci.get("detail2"):
            controler(f'détail 2 {ci["cle"]}', ci["detail2"], 10, "mono",
                      CA_SSX1 - CA_SSX0 - 24, 10 * 0.14)
            A(texte(CA_SSX0 + 12, y + 58, ci["detail2"], "mono", 10, 500,
                    "pivot", tracking=10 * 0.14))

    # ── Phrase de principe, pleine largeur ───────────────────────────────────
    controler("phrase de principe", donnees["phrase_principe"], 17,
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
        "demonstration": f"une réserve nourrit {len(chaudieres)} cellules "
                         f"identiques (la modulation est portée par la "
                         f"répétition du module), leurs sorties collectées "
                         f"vers une cellule unique de découplage, puis "
                         f"{len(circuits)} branches en pointillé — l’enterré — "
                         f"traversant chacune un cercle — le compteur — vers "
                         f"{len(circuits)} sous-stations : aucun texte "
                         f"nécessaire pour lire cascade, découplage et "
                         f"comptage",
        "topologie": f"réserve x {CA_SX0}–{CA_SX1}, chaudières x {CA_CHX0}–"
                     f"{CA_CHX1} y {CA_CHY0}–{bas_ch}, collecteur x {CA_COLX}, "
                     f"ballon x {CA_BX0}–{CA_BX1}, distribution x {CA_DISX}, "
                     f"compteurs x {CA_CPX}, sous-stations x {CA_SSX0}–"
                     f"{CA_SSX1} y {cys_ss[0] - CA_SS_H / 2:.0f}–"
                     f"{cys_ss[-1] + CA_SS_H / 2:.0f}",
        "bas_du_dessin": f"légende de cascade à y {bas_ch + 50}, sous-stations "
                         f"jusqu’à y {cys_ss[-1] + CA_SS_H / 2:.0f}, phrase à "
                         f"{Y_PHRASE}, cartouche {Y_CARTOUCHE}–"
                         f"{Y_CARTOUCHE + H_CARTOUCHE}",
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur * H_CARTOUCHE} px², soit "
                            f"{largeur * H_CARTOUCHE / (W * H) * 100:.2f} % de "
                            f"la planche",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l’échelle "
                         f"0,96 (1152 / {W})",
        "depassements": depassements if depassements
                        else "aucun — toutes les lignes mesurées sous leur colonne",
    }
    return "\n".join(out) + "\n", controles


def composer_vignette_cascade(donnees):
    """La vignette : le motif seul — quatre cellules identiques collectées vers
    le ballon, trois branches pointillées à cercle vers trois cellules. Deux
    valeurs se lisent : la cascade totale et le ballon."""
    ca = donnees["cascade"]
    chaudieres = sorted(ca["chaudieres"], key=lambda c: c["ordre"])
    circuits = sorted(ca["circuits"], key=lambda c: c["ordre"])
    chx0, chx1, colx = 14, 64, 74
    bx0, bx1 = 92, 146
    disx, cpx = 162, 182
    ssx0, ssx1 = 204, 286
    y0, h_ch, e_ch = 58, 15, 5
    h_ss = 15

    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false" '
      f'style="width:100%;height:auto;display:block">')
    entete_style(A)
    A(rect(0, 0, VW, VH, "papier"))
    A(texte(V_MARGE, 22, donnees["vignette_surtitre"], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    bas_ch = y0 + 4 * h_ch + 3 * e_ch
    cy_mid = (y0 + bas_ch) / 2
    cys = []
    for i in range(4):
        y = y0 + i * (h_ch + e_ch)
        cy = y + h_ch / 2
        cys.append(cy)
        A(rect_bord(chx0, y, chx1 - chx0, h_ch, "papier", "filet-1"))
        A(ligne(chx1, cy, colx, cy, "encre", 1.2))
    A(ligne(colx, cys[0], colx, cys[-1], "encre", 1.2))
    A(ligne(colx, cy_mid, bx0 - 6, cy_mid, "encre", 1.2))
    A(fleche(bx0 - 1, cy_mid, "encre", direction="droite", taille=5))
    A(rect_bord(bx0, cy_mid - 22, bx1 - bx0, 44, "papier", "filet-1"))
    A(texte((bx0 + bx1) / 2, cy_mid + 3.5, ca["ballon"]["affichee"], "mono",
            10, 500, "pivot", ancre="middle", tracking=10 * 0.14))
    cys_ss = [cy_mid - 30, cy_mid, cy_mid + 30]
    A(ligne(bx1, cy_mid, disx, cy_mid, "encre", 1.2))
    A(ligne(disx, cys_ss[0], disx, cys_ss[-1], "encre", 1.2))
    for cy in cys_ss:
        A(ligne_pointillee(disx, cy, ssx0 - 6, cy, "encre", 1.2, motif="4 4"))
        A(fleche(ssx0 - 1, cy, "encre", direction="droite", taille=5))
        A(cercle(cpx, cy, 4.5, "papier", "encre", 1.2))
        A(rect_bord(ssx0, cy - h_ss / 2, ssx1 - ssx0, h_ss, "papier", "filet-1"))
    A(texte(chx0, bas_ch + 18, ca["total"]["affichee"], "mono", 10, 500,
            "encre", tracking=10 * 0.14))

    A("</svg>")
    controles = {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": f"carte de projet mesurée de 274 à 296 px — "
                            f"échelle {274/VW:.2f} à {296/VW:.2f}",
        "corps_minimal": f"9 px dans le repère — rendu à {9*274/VW:.1f} px au pire cas",
        "motif": "le motif seul : quatre cellules identiques collectées vers "
                 "le ballon, trois branches pointillées à cercle vers trois "
                 "cellules — deux valeurs lisibles, la cascade et le ballon ; "
                 "la réserve, les libellés et les légendes laissés à la planche",
        "bas_du_dessin": f"total de cascade à y {bas_ch + 18} px, marge basse "
                         f"{VH - (bas_ch + 18)} px",
    }
    return "\n".join(out) + "\n", controles


def composer_appui_cascade(donnees):
    """L'appui : le motif entier à l'échelle 1 — la réserve, les quatre
    chaudières nommées et chiffrées, le ballon, les trois branches comptées
    vers les sous-stations nommées en court. Sans phrase ni cartouche."""
    ca = donnees["cascade"]
    chaudieres = sorted(ca["chaudieres"], key=lambda c: c["ordre"])
    circuits = sorted(ca["circuits"], key=lambda c: c["ordre"])
    sx0, sx1 = 24, 104
    chx0, chx1, colx = 122, 234, 252
    bx0, bx1 = 274, 348
    disx, cpx = 366, 388
    ssx0, ssx1 = 410, 528
    y0, h_ch, e_ch = 76, 34, 8
    h_ss = 36

    out = []
    A = out.append
    racine_appui(A, donnees)

    leg_cp = ca["legende_compteur"]
    l_cp = mesurer(leg_cp, 10, "mono", 10 * 0.14)
    A(cercle(AW - A_MARGE - l_cp - 14, 30.5, 4.5, "papier", "encre", 1.2))
    A(texte(AW - A_MARGE, 34, leg_cp, "mono", 10, 500, "pivot",
            ancre="end", tracking=10 * 0.14))

    bas_ch = y0 + 4 * h_ch + 3 * e_ch
    cy_mid = (y0 + bas_ch) / 2
    re_ = ca["reserve"]
    A(rect_bord(sx0, y0, sx1 - sx0, bas_ch - y0, "calcaire", "filet-1"))
    A(texte(sx0 + 10, y0 + 20, re_["libelle_court"], "sans", 13, 600,
            "encre", wdth=112))
    A(texte(sx0 + 10, y0 + 36, re_["detail_court"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))

    cys = []
    for i, ch in enumerate(chaudieres):
        y = y0 + i * (h_ch + e_ch)
        cy = y + h_ch / 2
        cys.append(cy)
        A(ligne(sx1, cy, chx0 - 8, cy, "encre", 1.5))
        A(fleche(chx0 - 2, cy, "encre", direction="droite", taille=6))
        A(rect_bord(chx0, y, chx1 - chx0, h_ch, "papier", "filet-1"))
        A(texte(chx0 + 10, y + 15, ch["libelle"], "sans", 13, 600,
                "encre", wdth=112))
        A(texte(chx0 + 10, y + 28, ch["affichee"], "mono", 10, 500,
                "pivot", tracking=10 * 0.14))
        A(ligne(chx1, cy, colx, cy, "encre", 1.5))
    A(ligne(colx, cys[0], colx, cys[-1], "encre", 1.5))
    A(ligne(colx, cy_mid, bx0 - 8, cy_mid, "encre", 1.5))
    A(fleche(bx0 - 2, cy_mid, "encre", direction="droite", taille=6))

    ba = ca["ballon"]
    A(rect_bord(bx0, cy_mid - 37, bx1 - bx0, 74, "papier", "filet-1"))
    A(texte(bx0 + 10, cy_mid - 12, ba["libelle_court"], "sans", 13, 600,
            "encre", wdth=112))
    A(texte(bx0 + 10, cy_mid + 6, ba["affichee"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))

    cys_ss = [cy_mid - 58, cy_mid, cy_mid + 58]
    A(ligne(bx1, cy_mid, disx, cy_mid, "encre", 1.5))
    A(ligne(disx, cys_ss[0], disx, cys_ss[-1], "encre", 1.5))
    for ci, cy in zip(circuits, cys_ss):
        A(ligne_pointillee(disx, cy, ssx0 - 8, cy, "encre", 1.5, motif="5 5"))
        A(fleche(ssx0 - 2, cy, "encre", direction="droite", taille=6))
        A(cercle(cpx, cy, 6, "papier", "encre", 1.5))
        A(rect_bord(ssx0, cy - h_ss / 2, ssx1 - ssx0, h_ss, "papier", "filet-1"))
        A(texte(ssx0 + 10, cy - 2, ci["libelle_court"], "sans", 13, 600,
                "encre", wdth=112))
        A(texte(ssx0 + 10, cy + 12, ci["detail_court"], "mono", 10, 500,
                "pivot", tracking=10 * 0.14))
    A(texte(chx0, bas_ch + 22, ca["total"]["affichee"], "mono", 10, 500,
            "encre", tracking=10 * 0.14))

    A("</svg>")
    return "\n".join(out) + "\n", controles_appui(
        motif="le motif entier à l’échelle 1 : la réserve nommée, les quatre "
              "chaudières nommées et chiffrées, le collecteur, le ballon "
              "chiffré, les trois branches pointillées à cercle vers les "
              "sous-stations nommées en court, la légende du compteur en "
              "tête — total de cascade sous la pile ; phrase et cartouche "
              "laissés à la planche",
        bas=f"total de cascade à y {bas_ch + 22} px, marge basse "
            f"{AH - (bas_ch + 22)} px")


# ── `regime` — ce que l'aval interdit à l'amont ──────────────────────────────
# Le onzième mécanisme de l'archétype, et le premier à poser une CONDITION
# D'ADMISSION plutôt qu'un trajet. Une chaudière déposée, la pompe à chaleur qui
# la remplace, et les DEUX régimes d'eau qu'elle sait fournir tracés en deux
# longues horizontales. À droite, trois familles d'émetteurs posées chacune à la
# hauteur de ce qu'elles exigent : l'aérotherme au-dessus des deux lignes — le
# trait qui monte vers lui s'ARRÊTE —, le radiateur sur la ligne haute
# température mais derrière une boîte intercalée — l'isolation —, le plancher
# chauffant sous la ligne basse, franchement atteint.
#
# La géométrie porte seule la démonstration : trois traits, un qui s'arrête, un
# qui passe sous condition, un qui atteint. Masquer tout le texte laisse lire le
# mécanisme.
RG_PX0, RG_PX1 = 56, 260        # la colonne de production
RG_CHY0, RG_CH_H = 252, 58      # la chaudière déposée — contour interrompu
RG_PACY0, RG_PAC_H = 336, 292   # le bloc de la pompe à chaleur
RG_EX0, RG_EX1 = 812, 1144      # les trois émetteurs
RG_EM_H = 74                    # hauteur d'une boîte d'émetteur
RG_Y_HT = 424                   # la ligne haute température
RG_Y_STD = 556                  # la ligne du régime standard
RG_CY_AERO = 276                # au-dessus des deux lignes
RG_CY_RAD = RG_Y_HT             # SUR la ligne haute température
RG_CY_PLAN = 596                # sous la ligne du régime standard
RG_CDX0, RG_CDX1 = 600, 768     # la boîte de condition posée sur le trajet
RG_CD_H = 46
RG_MONTX = 560                  # le trait qui monte vers l'aérotherme
RG_ARRET_X = 740                # et qui s'arrête avant de l'atteindre
RG_DESCX = 772                  # le trait qui descend vers le plancher
RG_ETIQ_X = 280                 # les étiquettes de palier, posées sur la ligne
RG_Y_LEGENDE = 628              # la légende d'arrêt, en zone franche — au
                                # pied du dessin, jamais sous un détail de palier

RG_CY = {"aerotherme": RG_CY_AERO, "radiateur": RG_CY_RAD, "plancher": RG_CY_PLAN}


def _rg_barre_arret(x, y, demi=12):
    """Le signe d'arrêt : une barre EN TRAVERS du trait qui n'aboutit pas.
    Le trait courant vers l'émetteur est horizontal — la barre est donc
    verticale, et se lit comme une butée, jamais comme une extrémité."""
    return ligne(x, y - demi, x, y + demi, "encre", 2.0)


def composer_regime(donnees):
    rg = donnees["regime"]
    paliers = {p["cle"]: p for p in sorted(rg["paliers"], key=lambda p: p["ordre"])}
    emetteurs = sorted(rg["emetteurs"], key=lambda e: e["ordre"])
    out = []
    A = out.append
    trop = []

    def controler(nom, contenu, corps, profil, dispo, tracking=0.0):
        largeur = mesurer(contenu, corps, profil, tracking)
        if largeur > dispo:
            trop.append(f"{nom} : {largeur:.1f} px pour {dispo:.1f} px")
        return dispo - largeur

    marges = []

    def poser(nom, contenu, corps, profil, dispo, tracking=0.0):
        marges.append((nom, controler(nom, contenu, corps, profil, dispo, tracking)))

    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
      f'preserveAspectRatio="xMidYMid meet" role="img" '
      f'style="width:100%;height:auto;display:block" '
      f'aria-label="{echapper(donnees["aria_label"])}">')
    entete_style(A)
    A(rect(0, 0, W, H, "papier"))

    # ── Bloc de titre ────────────────────────────────────────────────────────
    A(texte(MARGE, Y_SURTITRE, donnees["surtitre"], "mono", 11, 500,
            "pivot", tracking=11 * 0.14))
    poser("surtitre", donnees["surtitre"], 11, "mono", UTILE, 11 * 0.14)
    A(texte(MARGE, Y_TITRE, donnees["titre"], "sans", 30, 700, "encre", wdth=112))
    poser("titre", donnees["titre"], 30, "sans-700", UTILE)
    A(texte(MARGE, Y_SOUSTITRE, donnees["sous_titre"], "sans", 16, 400,
            "pivot", wdth=100))
    poser("sous-titre", donnees["sous_titre"], 16, "sans-400", UTILE)
    A(rect(MARGE, Y_FILET_TITRE, UTILE, 1, "filet-1"))

    # ── En-tête et registres ─────────────────────────────────────────────────
    A(texte(MARGE, Y_ENTETE, rg["entete"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    poser("en-tête", rg["entete"], 10, "mono", UTILE, 10 * 0.14)
    A(texte(MARGE, Y_REGISTRES, rg["registres"]["gauche"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    A(texte(W - MARGE, Y_REGISTRES, rg["registres"]["droite"], "mono", 10, 500,
            "pivot", ancre="end", tracking=10 * 0.14))
    poser("registres", rg["registres"]["gauche"] + rg["registres"]["droite"],
          10, "mono", UTILE - 60, 10 * 0.14)

    dispo_prod = RG_PX1 - RG_PX0 - 24

    # ── La chaudière déposée : contour interrompu, elle n'est plus là ────────
    de = rg["depose"]
    A(rect_pointille(RG_PX0, RG_CHY0, RG_PX1 - RG_PX0, RG_CH_H, "filet-1"))
    A(texte(RG_PX0 + 12, RG_CHY0 + 25, de["libelle"], "sans", 15, 600,
            "encre", wdth=112))
    poser("libellé chaudière", de["libelle"], 15, "sans-600", dispo_prod)
    A(texte(RG_PX0 + 12, RG_CHY0 + 44, de["detail"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    poser("détail chaudière", de["detail"], 10, "mono", dispo_prod, 10 * 0.14)

    # la substitution : une seule flèche, vers le bas
    cx_prod = (RG_PX0 + RG_PX1) / 2
    A(ligne(cx_prod, RG_CHY0 + RG_CH_H, cx_prod, RG_PACY0 - 9, "encre", 1.5))
    A(fleche(cx_prod, RG_PACY0 - 2, "encre", direction="bas", taille=7))

    # ── La pompe à chaleur : elle embrasse les deux lignes de régime ─────────
    pr = rg["production"]
    A(rect_bord(RG_PX0, RG_PACY0, RG_PX1 - RG_PX0, RG_PAC_H, "calcaire", "filet-1"))
    A(texte(RG_PX0 + 12, RG_PACY0 + 30, pr["libelle"], "sans", 17, 600,
            "encre", wdth=112))
    poser("libellé production", pr["libelle"], 17, "sans-600", dispo_prod)
    A(texte(RG_PX0 + 12, RG_PACY0 + 50, pr["detail"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    poser("détail production", pr["detail"], 10, "mono", dispo_prod, 10 * 0.14)

    # ── Les deux lignes de régime, et leur étiquette posée dessus ───────────
    A(ligne(RG_PX1, RG_Y_HT, RG_EX0, RG_Y_HT, "encre", 1.5))
    A(ligne(RG_PX1, RG_Y_STD, RG_DESCX, RG_Y_STD, "encre", 1.5))
    for cle, y, borne in (("ht", RG_Y_HT, RG_CDX0), ("std", RG_Y_STD, RG_DESCX)):
        p = paliers[cle]
        A(texte(RG_ETIQ_X, y - 10, p["affichee"], "mono", 10, 500, "encre",
                tracking=10 * 0.14))
        poser(f'palier {cle}', p["affichee"], 10, "mono",
              borne - RG_ETIQ_X - 16, 10 * 0.14)
        A(texte(RG_ETIQ_X, y + 20, p["detail"], "mono", 10, 500, "pivot",
                tracking=10 * 0.14))
        poser(f'détail palier {cle}', p["detail"], 10, "mono",
              borne - RG_ETIQ_X - 16, 10 * 0.14)

    # ── La condition posée SUR le trajet de la ligne haute température ──────
    cd = rg["condition"]
    A(rect_bord(RG_CDX0, RG_Y_HT - RG_CD_H / 2, RG_CDX1 - RG_CDX0, RG_CD_H,
                "papier", "filet-1"))
    A(texte(RG_CDX0 + 12, RG_Y_HT - 5, cd["libelle"], "sans", 15, 600,
            "encre", wdth=112))
    poser("libellé condition", cd["libelle"], 15, "sans-600",
          RG_CDX1 - RG_CDX0 - 24)
    A(texte(RG_CDX0 + 12, RG_Y_HT + 13, cd["detail"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    poser("détail condition", cd["detail"], 10, "mono",
          RG_CDX1 - RG_CDX0 - 24, 10 * 0.14)

    # ── Le trait qui monte vers l'aérotherme, et qui s'arrête ───────────────
    A(polyligne([(RG_MONTX, RG_Y_HT), (RG_MONTX, RG_CY_AERO),
                 (RG_ARRET_X, RG_CY_AERO)], "encre", 1.5))
    A(_rg_barre_arret(RG_ARRET_X, RG_CY_AERO))
    # la légende se pose en zone franche, sous la ligne basse : partout
    # ailleurs le trait montant la traverserait — deux traits qui se croisent
    # doivent différer par autre chose que leur position
    A(texte(RG_ETIQ_X, RG_Y_LEGENDE, rg["legende_arret"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    poser("légende d’arrêt", rg["legende_arret"], 10, "mono",
          RG_DESCX - RG_ETIQ_X - 16, 10 * 0.14)

    # ── Le trait qui descend vers le plancher chauffant ─────────────────────
    A(polyligne([(RG_DESCX, RG_Y_STD), (RG_DESCX, RG_CY_PLAN),
                 (RG_EX0 - 9, RG_CY_PLAN)], "encre", 1.5))
    A(fleche(RG_EX0 - 2, RG_CY_PLAN, "encre", direction="droite", taille=7))
    A(fleche(RG_EX0 - 2, RG_CY_RAD, "encre", direction="droite", taille=7))

    # ── Les trois émetteurs, chacun à la hauteur de ce qu'il exige ──────────
    dispo_em = RG_EX1 - RG_EX0 - 24
    for e in emetteurs:
        cy = RG_CY[e["cle"]]
        y = cy - RG_EM_H / 2
        A(rect_bord(RG_EX0, y, RG_EX1 - RG_EX0, RG_EM_H, "papier", "filet-1"))
        A(texte(RG_EX0 + 12, y + 26, e["libelle"], "sans", 17, 600,
                "encre", wdth=112))
        poser(f'libellé {e["cle"]}', e["libelle"], 17, "sans-600", dispo_em)
        A(texte(RG_EX0 + 12, y + 46, e["detail"], "mono", 10, 500, "pivot",
                tracking=10 * 0.14))
        poser(f'détail {e["cle"]}', e["detail"], 10, "mono", dispo_em, 10 * 0.14)
        A(texte(RG_EX0 + 12, y + 63, e["exigence"], "mono", 10, 500, "pivot",
                tracking=10 * 0.14))
        poser(f'exigence {e["cle"]}', e["exigence"], 10, "mono", dispo_em,
              10 * 0.14)
        # l'issue, sous la boîte : le mot porte, le trait double
        issue = f'{e["issue"]} — {e["issue_detail"]}'
        A(texte(RG_EX0, y + RG_EM_H + 18, issue, "mono", 10, 500, "encre",
                tracking=10 * 0.14))
        poser(f'issue {e["cle"]}', issue, 10, "mono", RG_EX1 - RG_EX0,
              10 * 0.14)

    # ── Phrase de principe, pleine largeur ──────────────────────────────────
    A(texte(MARGE, Y_PHRASE, donnees["phrase_principe"], "sans", 17, 400,
            "encre", wdth=100))
    poser("phrase de principe", donnees["phrase_principe"], 17, "sans-400", UTILE)

    # ── Cartouche — largeur AJUSTÉE au texte, jamais codée ──────────────────
    libelle = donnees["cartouche_legende"]
    largeur = min(600,
                  round(mesurer(libelle, 11, "mono", tracking=11 * 0.14) + 40))
    A(rect(MARGE, Y_CARTOUCHE, largeur, H_CARTOUCHE, "profond"))
    A(texte(MARGE + 20, Y_CARTOUCHE + 20, libelle, "mono", 11, 500, "voile",
            tracking=11 * 0.14))

    A("</svg>")

    assert not trop, "dépassements de colonne : " + " | ".join(trop)
    pire = min(marges, key=lambda m: m[1])
    bas_plan = RG_CY_PLAN + RG_EM_H / 2 + 18

    controles = {
        "gabarit": f"{W} x {H} — rapport {W/H:.4f} (3:2 exact)",
        "demonstration": f"une production unique, {len(paliers)} lignes de "
                         f"régime, {len(emetteurs)} émetteurs posés chacun à la "
                         f"hauteur de ce qu’il exige — et TROIS TRAITS qui "
                         f"suffisent à lire le mécanisme sans un mot : celui "
                         f"qui monte vers l’aérotherme s’arrête sur une barre "
                         f"{RG_EX0 - RG_ARRET_X} px avant lui, celui qui va au "
                         f"radiateur traverse d’abord une boîte intercalée, "
                         f"celui qui descend au plancher l’atteint sans rien "
                         f"franchir",
        "topologie": f"production x {RG_PX0}–{RG_PX1} (chaudière y {RG_CHY0}–"
                     f"{RG_CHY0 + RG_CH_H} en trait interrompu, pompe à chaleur "
                     f"y {RG_PACY0}–{RG_PACY0 + RG_PAC_H}), ligne haute "
                     f"température y {RG_Y_HT}, ligne standard y {RG_Y_STD}, "
                     f"condition x {RG_CDX0}–{RG_CDX1}, montée x {RG_MONTX} "
                     f"arrêt x {RG_ARRET_X}, émetteurs x {RG_EX0}–{RG_EX1} "
                     f"y {RG_CY_AERO - RG_EM_H / 2:.0f}, "
                     f"{RG_CY_RAD - RG_EM_H / 2:.0f}, "
                     f"{RG_CY_PLAN - RG_EM_H / 2:.0f}",
        "hierarchie_des_hauteurs": f"aérotherme {RG_CY_AERO} < ligne 65 °C "
                                   f"{RG_Y_HT} = radiateur {RG_CY_RAD} < ligne "
                                   f"35 °C {RG_Y_STD} < plancher {RG_CY_PLAN} — "
                                   f"l’ordre vertical EST l’ordre des exigences",
        "bas_du_dessin": f"issue du plancher à y {bas_plan:.0f}, phrase à "
                         f"{Y_PHRASE}, cartouche {Y_CARTOUCHE}–"
                         f"{Y_CARTOUCHE + H_CARTOUCHE}",
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur * H_CARTOUCHE} px², soit "
                            f"{largeur * H_CARTOUCHE / (W * H) * 100:.2f} % de "
                            f"la planche",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l’échelle "
                         f"0,96 (1152 / {W})",
        "depassements": f"{len(marges)} chaînes mesurées, 0 dépassement, marge "
                        f"la plus faible {pire[1]:.1f} px sur « {pire[0]} »",
    }
    return "\n".join(out) + "\n", controles


def composer_vignette_regime(donnees):
    """La vignette : le motif seul — la pompe à chaleur, les deux lignes
    chiffrées, les trois boîtes à leur hauteur, le trait qui s'arrête et la
    boîte intercalée. Deux valeurs se lisent : les deux régimes."""
    rg = donnees["regime"]
    paliers = {p["cle"]: p for p in rg["paliers"]}
    emetteurs = sorted(rg["emetteurs"], key=lambda e: e["ordre"])
    px0, px1 = 14, 62
    ex0, ex1 = 214, 286
    y_ht, y_std = 110, 148
    cy = {"aerotherme": 56, "radiateur": y_ht, "plancher": 172}
    h_em, h_pac = 22, 96
    cdx0, cdx1 = 146, 192
    montx, arret_x = 118, 190
    descx = 202

    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false" '
      f'style="width:100%;height:auto;display:block">')
    entete_style(A)
    A(rect(0, 0, VW, VH, "papier"))
    A(texte(V_MARGE, 22, donnees["vignette_surtitre"], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    y_pac = (y_ht + y_std) / 2 - h_pac / 2
    A(rect_pointille(px0, y_pac - 34, px1 - px0, 24, "filet-1", 1.2, "4 4"))
    A(ligne((px0 + px1) / 2, y_pac - 10, (px0 + px1) / 2, y_pac - 5, "encre", 1.2))
    A(fleche((px0 + px1) / 2, y_pac - 1, "encre", direction="bas", taille=5))
    A(rect_bord(px0, y_pac, px1 - px0, h_pac, "calcaire", "filet-1"))

    A(ligne(px1, y_ht, ex0, y_ht, "encre", 1.2))
    A(ligne(px1, y_std, descx, y_std, "encre", 1.2))
    A(texte(px1 + 8, y_ht - 6, paliers["ht"]["affichee_courte"], "mono", 9, 500,
            "encre", tracking=9 * 0.14))
    A(texte(px1 + 8, y_std - 6, paliers["std"]["affichee_courte"], "mono", 9, 500,
            "encre", tracking=9 * 0.14))

    A(rect_bord(cdx0, y_ht - 11, cdx1 - cdx0, 22, "papier", "filet-1"))
    A(polyligne([(montx, y_ht), (montx, cy["aerotherme"]),
                 (arret_x, cy["aerotherme"])], "encre", 1.2))
    A(ligne(arret_x, cy["aerotherme"] - 8, arret_x, cy["aerotherme"] + 8,
            "encre", 2.0))
    A(polyligne([(descx, y_std), (descx, cy["plancher"]),
                 (ex0 - 6, cy["plancher"])], "encre", 1.2))
    A(fleche(ex0 - 1, cy["plancher"], "encre", direction="droite", taille=5))
    A(fleche(ex0 - 1, cy["radiateur"], "encre", direction="droite", taille=5))

    for e in emetteurs:
        A(rect_bord(ex0, cy[e["cle"]] - h_em / 2, ex1 - ex0, h_em,
                    "papier", "filet-1"))

    A("</svg>")
    controles = {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": f"carte de projet mesurée de 274 à 296 px — "
                            f"échelle {274/VW:.2f} à {296/VW:.2f}",
        "corps_minimal": f"9 px dans le repère — rendu à {9*274/VW:.1f} px au "
                         f"pire cas",
        "motif": "le motif seul : la production, les deux lignes chiffrées, la "
                 "boîte intercalée, le trait qui s’arrête sur sa barre, et les "
                 "trois émetteurs muets à leur hauteur — deux valeurs lisibles, "
                 "les deux régimes ; libellés, exigences et issues laissés à la "
                 "planche",
        "bas_du_dessin": f"boîte basse à y {cy['plancher'] + h_em / 2:.0f} px, "
                         f"marge basse {VH - (cy['plancher'] + h_em / 2):.0f} px",
    }
    return "\n".join(out) + "\n", controles


def composer_appui_regime(donnees):
    """L'appui : le motif entier à l'échelle 1 — la production nommée, les deux
    régimes chiffrés, les trois émetteurs nommés en court avec leur issue.
    Sans phrase ni cartouche."""
    rg = donnees["regime"]
    paliers = {p["cle"]: p for p in rg["paliers"]}
    emetteurs = sorted(rg["emetteurs"], key=lambda e: e["ordre"])
    px0, px1 = 24, 128
    ex0, ex1 = 366, 528
    y_ht, y_std = 190, 262
    cy = {"aerotherme": 122, "radiateur": y_ht, "plancher": 304}
    h_em, h_pac = 40, 150
    cdx0, cdx1 = 250, 338
    montx, arret_x = 190, 330
    descx = 344

    out = []
    A = out.append
    racine_appui(A, donnees)

    y_pac = (y_ht + y_std) / 2 - h_pac / 2
    de, pr = rg["depose"], rg["production"]
    A(rect_pointille(px0, y_pac - 46, px1 - px0, 34, "filet-1", 1.5, "5 5"))
    A(texte(px0 + 10, y_pac - 25, de["libelle_court"], "sans", 13, 600,
            "encre", wdth=112))
    A(ligne((px0 + px1) / 2, y_pac - 12, (px0 + px1) / 2, y_pac - 8, "encre", 1.5))
    A(fleche((px0 + px1) / 2, y_pac - 2, "encre", direction="bas", taille=6))
    A(rect_bord(px0, y_pac, px1 - px0, h_pac, "calcaire", "filet-1"))
    A(texte(px0 + 10, y_pac + 22, pr["libelle_court"], "sans", 13, 600,
            "encre", wdth=112))

    A(ligne(px1, y_ht, ex0, y_ht, "encre", 1.5))
    A(ligne(px1, y_std, descx, y_std, "encre", 1.5))
    A(texte(px1 + 10, y_ht - 8, paliers["ht"]["affichee_courte"], "mono", 10,
            500, "encre", tracking=10 * 0.14))
    A(texte(px1 + 10, y_std - 8, paliers["std"]["affichee_courte"], "mono", 10,
            500, "encre", tracking=10 * 0.14))

    cd = rg["condition"]
    A(rect_bord(cdx0, y_ht - 17, cdx1 - cdx0, 34, "papier", "filet-1"))
    A(texte(cdx0 + 10, y_ht + 4, cd["libelle"], "sans", 13, 600, "encre",
            wdth=112))

    A(polyligne([(montx, y_ht), (montx, cy["aerotherme"]),
                 (arret_x, cy["aerotherme"])], "encre", 1.5))
    A(ligne(arret_x, cy["aerotherme"] - 11, arret_x, cy["aerotherme"] + 11,
            "encre", 2.0))
    A(polyligne([(descx, y_std), (descx, cy["plancher"]),
                 (ex0 - 8, cy["plancher"])], "encre", 1.5))
    A(fleche(ex0 - 2, cy["plancher"], "encre", direction="droite", taille=6))
    A(fleche(ex0 - 2, cy["radiateur"], "encre", direction="droite", taille=6))

    for e in emetteurs:
        y = cy[e["cle"]] - h_em / 2
        A(rect_bord(ex0, y, ex1 - ex0, h_em, "papier", "filet-1"))
        A(texte(ex0 + 10, y + 17, e["libelle_court"], "sans", 13, 600,
                "encre", wdth=112))
        A(texte(ex0 + 10, y + 32, e["issue"].upper(), "mono", 10, 500,
                "pivot", tracking=10 * 0.14))

    A("</svg>")
    return "\n".join(out) + "\n", controles_appui(
        motif="le motif entier à l’échelle 1 : la chaudière déposée en trait "
              "interrompu, la pompe à chaleur, les deux régimes chiffrés, la "
              "boîte de condition nommée, le trait qui s’arrête sur sa barre, "
              "et les trois émetteurs nommés en court avec leur issue ; "
              "détails, exigences, phrase et cartouche laissés à la planche",
        bas=f"boîte basse à y {cy['plancher'] + h_em / 2:.0f} px, marge basse "
            f"{AH - (cy['plancher'] + h_em / 2):.0f} px")


# ═══ Dispatch — le bloc de l'extraction choisit le mécanisme ═════════════════

def composer(donnees):
    if "regime" in donnees:
        return composer_regime(donnees)
    if "cascade" in donnees:
        return composer_cascade(donnees)
    if "comptage" in donnees:
        return composer_comptage(donnees)
    if "terminaux" in donnees:
        return composer_terminaux(donnees)
    if "commande" in donnees:
        return composer_commande(donnees)
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
    if "regime" in donnees:
        return composer_vignette_regime(donnees)
    if "cascade" in donnees:
        return composer_vignette_cascade(donnees)
    if "comptage" in donnees:
        return composer_vignette_comptage(donnees)
    if "terminaux" in donnees:
        return composer_vignette_terminaux(donnees)
    if "commande" in donnees:
        return composer_vignette_commande(donnees)
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
    if "regime" in donnees:
        return composer_appui_regime(donnees)
    if "cascade" in donnees:
        return composer_appui_cascade(donnees)
    if "comptage" in donnees:
        return composer_appui_comptage(donnees)
    if "terminaux" in donnees:
        return composer_appui_terminaux(donnees)
    if "commande" in donnees:
        return composer_appui_commande(donnees)
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
