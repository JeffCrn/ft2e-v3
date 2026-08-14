#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compositeur de planche — archétype `coupe-traversee`.

Protocole : docs/superpowers/specs/2026-08-12-planches-references-protocole.md

Il lit un `planche.json` (l'extraction, produite par la session de génération) et
écrit les deux dessins qui en découlent :

    planche.svg    1200 x 800 — la planche de fiche, lue à 1152 px (échelle 0,96)
    vignette.svg    300 x 200 — la vignette de carte, lue à 274-296 px (0,91-0,99)

Usage :

    python scripts/planches/coupe-traversee.py public/images/projets/<slug>

La géométrie est CALCULÉE : aucune coordonnée n'est tapée à la main, et le bloc
`controles` du JSON est recalculé à chaque exécution.

Le motif de l'archétype — le mécanisme d'une coupe de principe : **une enveloppe
continue referme le bâtiment, tout ce qui la traverse est traité, la toiture
produit.** La démonstration est portée par la géométrie — une ligne isolante qui
ne s'interrompt qu'aux traversées marquées (baies, air neuf et rejet), un plancher
dont le pont thermique est enveloppé, des champs posés AU-DESSUS de la couverture
qui exportent vers la droite — jamais par une colonne de chiffres que la page
porte déjà. La coupe est un gabarit à deux pans symétriques : aucune proportion
réelle de l'ouvrage n'est reprise (règle 4).

Troisième module du chantier après `sankey-energie.py` et `zonage-ssi.py`.
Le tronc commun vit dans `_tronc.py` depuis le 2026-08-13.

Le module compose TROIS mécanismes de l'archétype, choisis par le bloc que
porte l'extraction :

- `coupe` — l'enveloppe traversée (ancien siège communautaire de Marennes) :
  une ligne isolante continue, des traversées traitées, une toiture qui
  produit ;
- `equilibre` — l'air extrait, l'air compensé (restaurant scolaire de
  Villedoux) : trois locaux sous une même ligne de toiture, l'air extrait
  fléché vers le haut en trait plein, l'air de compensation en trait
  interrompu là où le relevé ne l'a pas constaté — partout l'air monte,
  nulle part il ne redescend ;
- `enjambement` — l'enveloppe d'une parcelle enjambée (étude notariale
  Joffre) : trois niveaux empilés dont le premier plancher passe au-dessus
  d'un passage voiture — la ligne isolante ferme des faces qu'un bâtiment
  ordinaire n'a pas : le dessous du plancher au-dessus du vide, la fosse
  d'ascenseur sous le sol, chaque about de dalle marqué d'un rupteur.
"""

import math
import re as _re

from _tronc import (NN, W, H, MARGE, UTILE, VW, VH, V_MARGE, AW, AH, A_MARGE,
                    mesurer, echapper, texte, rect, rect_bord, ligne,
                    polyligne, fleche, cercle, entete_style, racine_appui,
                    controles_appui, executer)


# ── Rythme vertical de la planche ────────────────────────────────────────────
Y_SURTITRE = 76
Y_TITRE = 112
Y_SOUSTITRE = 138
Y_FILET_TITRE = 160
Y_ENTETE = 190
Y_TAGS = 240
Y_PHRASE = 688
Y_CARTOUCHE = 714
H_CARTOUCHE = 30

# ── La coupe : un gabarit de principe, jamais une géométrie d'ouvrage ────────
MUR_G, MUR_D = 300, 700       # nus extérieurs des murs
EP_MUR = 5                    # épaisseur de la structure de mur
Y_SOL = 640                   # ligne de sol
Y_EAVES = 430                 # sablière — sommet des murs
Y_APEX = 320                  # faîtage
X_APEX = (MUR_G + MUR_D) / 2  # 500 — deux pans symétriques
Y_DALLE = 530                 # plancher intermédiaire (dalle de 10)
EP_DALLE = 10

PENTE = (Y_EAVES - Y_APEX) / (X_APEX - MUR_G)          # 0,55
V = math.sqrt(1 + PENTE * PENTE)                       # 1,1414 — offset vertical

ITE_X0G, ITE_X1G = 286, 298   # bande d'isolant, mur gauche
ITE_X0D, ITE_X1D = 702, 714   # bande d'isolant, mur droit
D_C280, D_C220 = 8, 17        # distances perpendiculaires des deux couches
D_PV = 30                     # surimposition : les modules au-dessus des couches

FEN_ETAGE = (455, 505)        # baie représentative, étage
FEN_RDC = (555, 605)          # baie représentative, RDC

BOX_DF = (430, 385, 140, 35)  # centrale double flux, en combles
DUCT_NEUF, DUCT_REJET = 510, 555
Y_DUCT_HAUT = 302

PV_G = (320, 455)             # champ gauche, en abscisse le long du pan
PV_D = (600, 690)             # champ droit

BOX_OND = (770, 245, 180, 70) # les deux onduleurs
Y_EXPORT = 280                # la ligne de revente
X_EXPORT_FIN = 1126

CALL_X = MARGE                # colonne d'appels, à gauche
CALL_L = 200                  # sa largeur


def pan_y(x):
    """Ordonnée du pan (structure) à l'abscisse x — prolongée au-delà des murs."""
    if x <= X_APEX:
        return Y_APEX + (X_APEX - x) * PENTE
    return Y_APEX + (x - X_APEX) * PENTE


def pan_offset(x, d):
    """Point de la parallèle au pan, à la distance perpendiculaire d (vers le haut)."""
    return (x, pan_y(x) - d * V)


def bande_pan(A, x0, x1, d, cle, epaisseur):
    """Une bande parallèle aux pans, en deux segments joints au faîtage."""
    if x0 < X_APEX < x1:
        A(polyligne([pan_offset(x0, d), pan_offset(X_APEX, d),
                     pan_offset(x1, d)], cle, epaisseur))
    else:
        A(polyligne([pan_offset(x0, d), pan_offset(x1, d)], cle, epaisseur))


def champ_pv(A, x0, x1, d):
    """Un champ de modules : segments épais AU-DESSUS des couches (surimposition),
    coupés de deux joints, et trois attaches vers la couverture."""
    n_seg, joint = 3, 6
    total = x1 - x0
    seg = (total - (n_seg - 1) * joint) / n_seg
    x = x0
    for _ in range(n_seg):
        A(polyligne([pan_offset(x, d), pan_offset(x + seg, d)], "encre", 6))
        x += seg + joint
    for t in (0.18, 0.5, 0.82):
        xa = x0 + t * total
        A(polyligne([pan_offset(xa, d - 3), pan_offset(xa, D_C220 + 3)],
                    "encre", 1))


def appel(A, x, base, libelle, details, largeur, cible, controler, nom):
    """Un appel de la colonne de gauche : libellé Archivo 15/400, détails mono 10,
    ligne d'attache filet-1 vers l'organe désigné."""
    controler(f"appel {nom} — libellé", libelle, 15, "sans-400", largeur)
    A(texte(x, base, libelle, "sans", 15, 400, "encre", wdth=100))
    for k, l in enumerate(details):
        controler(f"appel {nom} — détail {k + 1}", l, 10, "mono",
                  largeur, 10 * 0.14)
        A(texte(x, base + 18 + k * 14, l, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))
    depart = (x + mesurer(libelle, 15, "sans-400") + 8, base - 4)
    A(polyligne([depart, cible], "filet-1", 1))
    return depart


def composer(donnees):
    c = donnees["coupe"]
    elems = {e["cle"]: e for e in c["elements"]}
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
    controler("en-tête schéma", c["entete"], 10, "mono", 700, 10 * 0.14)
    A(texte(MARGE, Y_ENTETE, c["entete"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    A(texte(MARGE, Y_TAGS, c["registres"]["gauche"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    A(texte(W - MARGE, Y_TAGS, c["registres"]["droite"], "mono", 10, 500,
            "pivot", ancre="end", tracking=10 * 0.14))

    # ── Le sol ───────────────────────────────────────────────────────────────
    A(ligne(240, Y_SOL, 780, Y_SOL, "filet-1", 2))
    for k in range(6):
        x = 262 + k * 90
        A(ligne(x, Y_SOL + 2, x - 9, Y_SOL + 10, "filet-2", 1))

    # ── La structure : murs, dalle, plancher de combles, pans ────────────────
    def mur(x, fenetres):
        """Le mur en segments, interrompu aux baies."""
        y = Y_EAVES
        for (f0, f1) in sorted(fenetres):
            A(rect(x, y, EP_MUR, f0 - y, "encre"))
            y = f1
        A(rect(x, y, EP_MUR, Y_SOL - y, "encre"))

    mur(MUR_G, [FEN_ETAGE, FEN_RDC])
    mur(MUR_D - EP_MUR, [])
    A(rect(MUR_G + EP_MUR, Y_DALLE, MUR_D - MUR_G - 2 * EP_MUR, EP_DALLE,
           "encre"))
    A(ligne(MUR_G + EP_MUR, Y_EAVES, MUR_D - EP_MUR, Y_EAVES, "filet-2", 1))
    A(polyligne([(MUR_G, Y_EAVES), (X_APEX, Y_APEX), (MUR_D, Y_EAVES)],
                "encre", 3))

    # ── L'enveloppe : bandes d'isolant continues, murs et deux couches ───────
    # Le haut des bandes de mur remonte SOUS les deux couches de pan : le
    # raccord de la sablière est le point où la continuité doit se voir.
    y_raccord = 412
    A(rect(ITE_X0G, y_raccord, ITE_X1G - ITE_X0G, Y_SOL - y_raccord, "clair"))
    A(rect(ITE_X0D, y_raccord, ITE_X1D - ITE_X0D, Y_SOL - y_raccord, "clair"))
    bande_pan(A, ITE_X0G, ITE_X1D, D_C280, "clair", 6)
    bande_pan(A, ITE_X0G, ITE_X1D, D_C220, "clair", 6)

    # Les baies interrompent la bande du mur : réserve papier + double vitrage.
    for (f0, f1) in (FEN_ETAGE, FEN_RDC):
        A(rect(ITE_X0G - 1, f0, ITE_X1G - ITE_X0G + 2 + EP_MUR + 16, f1 - f0,
               "papier"))
        A(ligne(MUR_G + 0.5, f0, MUR_G + 0.5, f1, "encre", 1.5))
        A(ligne(MUR_G + EP_MUR - 0.5, f0, MUR_G + EP_MUR - 0.5, f1,
                "encre", 1.5))
        for k in range(4):
            yb = f0 + 8 + k * 8
            A(ligne(ITE_X0G + 2, yb, ITE_X1G - 2, yb, "encre", 1))

    # ── Les champs photovoltaïques, en surimposition ─────────────────────────
    champ_pv(A, *PV_G, D_PV)
    champ_pv(A, *PV_D, D_PV)

    # ── La centrale double flux et ses deux traversées ───────────────────────
    bx, by, bw, bh = BOX_DF
    A(rect_bord(bx, by, bw, bh, "papier", "filet-1"))
    lib_df = c["equipement_combles"]
    controler("libellé double flux", lib_df, 15, "sans-600", bw - 24)
    A(texte(bx + bw / 2, by + bh / 2 + 5, lib_df, "sans", 15, 600,
            "encre", wdth=112, ancre="middle"))
    for xd, sens in ((DUCT_NEUF, "bas"), (DUCT_REJET, "haut")):
        A(ligne(xd, Y_DUCT_HAUT, xd, by, "encre", 1.5))
        if sens == "bas":
            A(fleche(xd, by - 2, "encre", "bas", 8))
        else:
            A(fleche(xd, Y_DUCT_HAUT, "encre", "haut", 8))
    lab_air = c["traversee_air"]
    x_air = (DUCT_NEUF + DUCT_REJET) / 2
    l_air = controler("air neuf · rejet", lab_air, 10, "mono", 200, 10 * 0.14)
    A(texte(x_air, Y_DUCT_HAUT - 10, lab_air, "mono", 10, 500, "pivot",
            ancre="middle", tracking=10 * 0.14))

    # Soufflage et reprise : la distribution intérieure, sous la centrale.
    A(ligne(470, by + bh, 470, 458, "encre", 1))
    A(fleche(470, 460, "encre", "bas", 7))
    A(ligne(530, 460, 530, by + bh + 2, "encre", 1))
    A(fleche(530, by + bh + 2, "encre", "haut", 7))
    A(texte(500, 478, c["interieur_air"], "mono", 10, 500, "pivot",
            ancre="middle", tracking=10 * 0.14))

    # ── Les niveaux, nommés ──────────────────────────────────────────────────
    A(texte(320, 484, c["niveaux"][1], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    A(texte(320, 592, c["niveaux"][0], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    A(texte(585, 424, c["niveaux"][2], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

    # ── La chaîne de production : champs → onduleurs → réseau ────────────────
    ox, oy, ow, oh = BOX_OND
    p_g = pan_offset(PV_G[1], D_PV)
    p_d = pan_offset(PV_D[0], D_PV)
    A(polyligne([p_g, (p_g[0], 265), (ox, 265)], "encre", 1))
    A(polyligne([p_d, (p_d[0], Y_EXPORT), (ox, Y_EXPORT)], "encre", 1))
    A(rect_bord(ox, oy, ow, oh, "papier", "filet-1"))
    ond = elems["onduleurs"]
    controler("libellé onduleurs", ond["libelle"], 15, "sans-600", ow - 32)
    A(texte(ox + 16, oy + 27, ond["libelle"], "sans", 15, 600, "encre",
            wdth=112))
    for k, l in enumerate(ond["detail"]):
        controler(f"onduleurs détail {k + 1}", l, 10, "mono", ow - 32,
                  10 * 0.14)
        A(texte(ox + 16, oy + 45 + k * 14, l, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))
    A(ligne(ox + ow, Y_EXPORT, X_EXPORT_FIN, Y_EXPORT, "encre", 2))
    A(fleche(X_EXPORT_FIN + 8, Y_EXPORT, "encre", "droite"))
    res = elems["reseau"]
    x_res = (ox + ow + X_EXPORT_FIN + 8) / 2
    for l, yr in ((res["detail"][0], Y_EXPORT - 12),
                  (res["detail"][1], Y_EXPORT + 20)):
        controler("réseau", l, 10, "mono", X_EXPORT_FIN + 8 - (ox + ow),
                  10 * 0.14)
        A(texte(x_res, yr, l, "mono", 10, 500, "pivot", ancre="middle",
                tracking=10 * 0.14))

    # L'appel du champ photovoltaïque — posé dans le bas de la colonne de
    # production, pour que la colonne se distribue au lieu de laisser un vide.
    mod = elems["modules"]
    Y_APPEL_PV = 470
    controler("appel modules — libellé", mod["libelle"], 15, "sans-400",
              W - MARGE - ox)
    A(texte(ox, Y_APPEL_PV, mod["libelle"], "sans", 15, 400, "encre", wdth=100))
    controler("appel modules — détail", mod["detail"][0], 10, "mono",
              W - MARGE - ox, 10 * 0.14)
    A(texte(ox, Y_APPEL_PV + 18, mod["detail"][0], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    cible_pv = pan_offset(PV_D[1] - 4, D_PV + 4)
    A(polyligne([(ox - 8, Y_APPEL_PV - 4), cible_pv], "filet-1", 1))

    # ── La colonne d'appels, à gauche ────────────────────────────────────────
    appels = [
        ("toiture", 296, pan_offset(370, D_C220 - 3)),
        ("double-flux", 380, (bx, by + bh / 2)),
        ("baies", 464, (ITE_X0G + 1, FEN_ETAGE[0] + 23)),
        ("plancher", 548, (MUR_G + 2, Y_DALLE + EP_DALLE / 2)),
        ("murs", 618, ((ITE_X0G + ITE_X1G) / 2, 612)),
    ]
    for cle, base, cible in appels:
        e = elems[cle]
        appel(A, CALL_X, base, e["libelle"], e["detail"], CALL_L, cible,
              controler, cle)

    # ── Phrase de principe, pleine largeur ───────────────────────────────────
    l_phrase = mesurer(donnees["phrase_principe"], 17, "sans-400")
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
        "demonstration": "la ligne d'enveloppe (bandes claires) est continue du "
                         "sol au faîtage et ne s'interrompt qu'aux traversées "
                         "marquées : 2 baies vitrées, 2 conduits d'air fléchés "
                         "en sens opposés — les champs de modules sont posés "
                         "AU-DESSUS des couches (surimposition) et la chaîne "
                         "sort du cadre à droite : la géométrie porte la thèse "
                         "« l'enveloppe d'abord, la production ensuite »",
        "topologie": f"appels (x {CALL_X}–{CALL_X + CALL_L}) → coupe "
                     f"(x {ITE_X0G}–{ITE_X1D}, sol {Y_SOL}, faîtage {Y_APEX}) "
                     f"→ production (onduleurs x {BOX_OND[0]}–"
                     f"{BOX_OND[0] + BOX_OND[2]}, export y {Y_EXPORT} "
                     f"jusqu'à x {X_EXPORT_FIN + 8})",
        "pans": f"pente {PENTE:.2f} — couches à {D_C280} et {D_C220} px des "
                f"pans, modules à {D_PV} px (surimposition lisible)",
        "bas_du_dessin": f"sol à {Y_SOL} (hachures jusqu'à {Y_SOL + 10}), "
                         f"dernier appel à 636, phrase de principe à "
                         f"{Y_PHRASE}, cartouche {Y_CARTOUCHE}–"
                         f"{Y_CARTOUCHE + H_CARTOUCHE}, marge basse "
                         f"{H - (Y_CARTOUCHE + H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur * H_CARTOUCHE} px², soit "
                            f"{largeur * H_CARTOUCHE / (W * H) * 100:.2f} % "
                            f"de la planche",
        "phrase_principe": f"126 signes — {l_phrase:.0f} px mesurés pour "
                           f"{UTILE} disponibles : la citation exacte tient "
                           f"sur sa ligne (la mesure prévaut sur la règle des "
                           f"120 signes ; arbitrage consigné dans "
                           f"a_valider_ft2e)",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l'échelle "
                         f"0,96 (1152 / {W})",
        "depassements": depassements if depassements
                        else "aucun — toutes les lignes mesurées sous leur colonne",
    }
    return "\n".join(out) + "\n", controles


def composer_vignette(donnees):
    """La vignette : le motif de l'archétype, sans son appareil.

    Ce qu'elle garde : la coupe fermée par sa bande continue, les champs en
    surimposition et la flèche d'export, avec les deux nœuds chiffrés
    (enveloppe R ≥ 4,15, production 33,48 kWc). Ce qu'elle laisse : les baies,
    la centrale, les conduits, la dalle annotée, les appels — six organes
    annotés dans 300 px ne se liraient pas."""
    elems = {e["cle"]: e for e in donnees["coupe"]["elements"]}
    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false" '
      f'style="width:100%;height:auto;display:block">')
    entete_style(A)
    A(rect(0, 0, VW, VH, "papier"))
    A(texte(V_MARGE, 22, donnees["vignette_surtitre"], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    # La coupe miniature — mêmes proportions de principe, repère propre.
    mg, md = 40, 160
    y_sol, y_eaves, y_apex = 172, 120, 88
    x_apex = (mg + md) / 2
    pente = (y_eaves - y_apex) / (x_apex - mg)
    v = math.sqrt(1 + pente * pente)

    def vpan_y(x):
        return y_apex + abs(x - x_apex) * pente

    def vpan_off(x, d):
        return (x, vpan_y(x) - d * v)

    A(ligne(24, y_sol, 190, y_sol, "filet-1", 1.5))
    A(rect(mg, y_eaves, 3, y_sol - y_eaves, "encre"))
    A(rect(md - 3, y_eaves, 3, y_sol - y_eaves, "encre"))
    A(rect(mg + 3, 144, md - mg - 6, 4, "encre"))
    A(polyligne([(mg, y_eaves), (x_apex, y_apex), (md, y_eaves)], "encre", 2))
    # La bande d'enveloppe continue : murs et pans.
    A(rect(32, 117, 5, y_sol - 117, "clair"))
    A(rect(163, 117, 5, y_sol - 117, "clair"))
    A(polyligne([vpan_off(32, 6), vpan_off(x_apex, 6), vpan_off(168, 6)],
                "clair", 4))
    # Les champs, en surimposition, et l'export.
    for (x0, x1) in ((48, 92), (108, 152)):
        milieu = (x0 + x1) / 2
        A(polyligne([vpan_off(x0, 14), vpan_off(milieu - 3, 14)], "encre", 4))
        A(polyligne([vpan_off(milieu + 3, 14), vpan_off(x1, 14)], "encre", 4))
    dep = vpan_off(108, 14)
    A(polyligne([dep, (dep[0], 56), (248, 56)], "encre", 1.2))
    A(fleche(254, 56, "encre", "droite", 7))

    # Les deux nœuds chiffrés.
    A(texte(190, 76, elems["modules"]["libelle"].split(" en ")[0] + " PV",
            "sans", 12, 600, "encre", wdth=112))
    A(texte(190, 90, f'{elems["modules"]["valeur"]}{NN}{elems["modules"]["unite"]}',
            "mono", 10, 500, "pivot", tabulaire=True))
    A(texte(190, 126, elems["murs"]["libelle"].split(" par ")[0], "sans", 12,
            600, "encre", wdth=112))
    A(texte(190, 140, f'R ≥ 4,15', "mono", 10, 500, "pivot", tabulaire=True))
    A(polyligne([(186, 122), (170, 130)], "filet-1", 1))

    A("</svg>")
    controles = {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": f"carte de projet mesurée de 274 à 296 px — "
                            f"échelle {274/VW:.2f} à {296/VW:.2f}",
        "corps_minimal": f"9 px dans le repère — rendu à {9*274/VW:.1f} px au pire cas",
        "motif": "la coupe fermée par sa bande continue, les champs en "
                 "surimposition et la flèche d'export — baies, centrale, "
                 "conduits et appels sont laissés à la planche",
        "bas_du_dessin": f"sol à 172 px, marge basse {VH - 172} px",
    }
    return "\n".join(out) + "\n", controles


# ═══ Mécanisme `equilibre` — l'air extrait, l'air compensé (Villedoux) ═══════
#
# Trois locaux sous une même ligne de toiture ; chaque conduit la traverse par
# un percement qui interrompt la ligne. La grammaire des traits est légendée en
# tête de dessin : trait plein = l'air qui passe, trait interrompu = l'air qui
# devrait passer. La largeur d'un conduit est PROPORTIONNELLE à son débit — la
# géométrie seule montre que le plus gros débit du bâtiment n'est plus compensé.

E_Y_LEGENDE = 220             # la légende des traits, sous l'en-tête
E_Y_TOIT = 348                # la ligne de toiture
E_MACH0, E_MACH1 = 262, 336   # la bande des machines, au-dessus
E_ROOM0, E_ROOM1 = 392, 588   # la bande des locaux, au-dessous
E_Y_ABSENCE = 376             # les mentions d'absence, dans la traversée
E_Y_PIED = 624                # la ligne de pied (les caissons qui tournaient)
E_COLS = ((56, 392), (424, 752), (784, 1144))   # salles · laverie · cuisson
E_K = 48 / 7500               # px par m³/h — 7 500 m³/h font 48 px de conduit


def _debit(valeur):
    """« 7 500 » → 7500 — la largeur du conduit se calcule, jamais ne se tape."""
    return int(_re.sub(r"\D", "", valeur))


def rect_interrompu(A, x, y0, y1, w, epaisseur=1.5, motif="6 6"):
    """Un conduit prescrit mais sans débit constaté : contour interrompu,
    aucun remplissage, aucune flèche."""
    from _tronc import JETON
    A(f'  <rect x="{x - w / 2:.2f}" y="{y0:.2f}" width="{w:.2f}" '
      f'height="{y1 - y0:.2f}" fill="none" class="s-encre" '
      f'stroke="{JETON["encre"]}" stroke-width="{epaisseur}" '
      f'stroke-dasharray="{motif}"/>')


def conduit_plein(A, x, y0, y1, w):
    """Un conduit où l'air passe : bande claire à contour encré — le flux est
    toujours doublé de flèches encrées et d'une cote."""
    from _tronc import JETON
    A(f'  <rect x="{x - w / 2:.2f}" y="{y0:.2f}" width="{w:.2f}" '
      f'height="{y1 - y0:.2f}" class="c-clair s-encre" '
      f'fill="{JETON["clair"]}" stroke="{JETON["encre"]}" stroke-width="1"/>')


def composer_equilibre(donnees):
    q = donnees["equilibre"]
    elems = {e["cle"]: e for e in q["elements"]}
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

    # ── En-tête, légende des traits, registre ────────────────────────────────
    controler("en-tête schéma", q["entete"], 10, "mono", UTILE, 10 * 0.14)
    A(texte(MARGE, Y_ENTETE, q["entete"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    controler("légende des traits", q["legende_traits"], 10, "mono",
              680, 10 * 0.14)
    A(texte(MARGE, E_Y_LEGENDE, q["legende_traits"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    controler("registre droite", q["registre_droite"], 10, "mono",
              380, 10 * 0.14)
    A(texte(W - MARGE, E_Y_LEGENDE, q["registre_droite"], "mono", 10, 500,
            "pivot", ancre="end", tracking=10 * 0.14))

    sal = elems["salles"]
    lav = elems["laverie"]
    hot = elems["cuisson-hotte"]
    cmp_ = elems["cuisson-compensation"]

    # Les largeurs de conduit, proportionnelles aux débits de la fiche.
    # Une double flux de 2 340 m³/h souffle ET reprend ce débit : chacun de
    # ses deux conduits se cote au débit plein, jamais à sa moitié.
    w_sal = _debit(sal["valeur"]) * E_K
    w_lav = _debit(lav["valeur"]) * E_K
    w_hot = _debit(hot["valeur"]) * E_K
    w_cmp = _debit(cmp_["valeur"]) * E_K

    (SX0, SX1), (LX0, LX1), (CX0, CX1) = E_COLS
    CX_SOUF, CX_REPR = 170, 290                  # les deux conduits de la CTA
    CX_LAV = 660                                 # l'extraction de la laverie
    CX_CMP, CX_HOT = 880, 1040                   # compensation · hotte du piano

    # ── La ligne de toiture, interrompue à chaque percement ──────────────────
    traversees = sorted((cx, w) for cx, w in
                        ((CX_SOUF, w_sal), (CX_REPR, w_sal), (CX_LAV, w_lav),
                         (CX_CMP, w_cmp), (CX_HOT, w_hot)))
    x = MARGE
    for cx, w in traversees:
        A(ligne(x, E_Y_TOIT, cx - w / 2 - 4, E_Y_TOIT, "encre", 2))
        x = cx + w / 2 + 4
    A(ligne(x, E_Y_TOIT, W - MARGE, E_Y_TOIT, "encre", 2))
    A(texte(MARGE, E_Y_TOIT - 8, q["toiture"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

    # ── Les trois locaux — blocs topologiques d'égale hauteur ────────────────
    for (x0, x1), e in zip(E_COLS, (sal, lav, hot)):
        A(rect(x0, E_ROOM0, x1 - x0, E_ROOM1 - E_ROOM0, "calcaire"))
        lib = e.get("libelle_dessin", e["libelle"])
        controler(f"libellé {e['cle']}", lib, 15, "sans-600", x1 - x0 - 32)
        A(texte(x0 + 16, E_ROOM0 + 28, lib, "sans", 15, 600,
                "encre", wdth=112))
        for k, l in enumerate(e.get("detail", [])):
            controler(f"détail {e['cle']} {k + 1}", l, 10, "mono",
                      x1 - x0 - 32, 10 * 0.14)
            A(texte(x0 + 16, E_ROOM0 + 50 + k * 14, l, "mono", 10, 500,
                    "pivot", tracking=10 * 0.14))
    # Les notes de constat, en pied de chaque local.
    for (x0, x1), e in zip(E_COLS, (sal, lav, hot)):
        notes = e.get("notes", [])
        for k, l in enumerate(notes):
            y = E_ROOM1 - 16 - (len(notes) - 1 - k) * 16
            controler(f"note {e['cle']} {k + 1}", l, 10, "mono",
                      x1 - x0 - 32, 10 * 0.14)
            A(texte(x0 + 16, y, l, "mono", 10, 500, "pivot",
                    tracking=10 * 0.14))

    # ── Salles : la CTA double flux, deux conduits prescrits, aucun débit ────
    BX0, BY0, BW, BH = 110, E_MACH0, 240, E_MACH1 - E_MACH0
    A(rect_bord(BX0, BY0, BW, BH, "papier", "filet-1"))
    controler("libellé CTA", sal["machine"], 15, "sans-600", BW - 32)
    A(texte(BX0 + 16, BY0 + 26, sal["machine"], "sans", 15, 600, "encre",
            wdth=112))
    for k, l in enumerate(sal["machine_detail"]):
        controler(f"détail CTA {k + 1}", l, 10, "mono", BW - 32, 10 * 0.14)
        A(texte(BX0 + 16, BY0 + 44 + k * 14, l, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))
    # Le voyant : un point clair, toujours doublé de sa mention.
    A(cercle(BX0 + 14, BY0 - 13.5, 4.5, "clair", "encre", 1))
    controler("mention voyant", sal["voyant"], 10, "mono", 340, 10 * 0.14)
    A(texte(BX0 + 26, BY0 - 10, sal["voyant"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    for cx in (CX_SOUF, CX_REPR):
        rect_interrompu(A, cx, E_MACH1, E_ROOM0, w_sal)
    # Le constat, posé ENTRE les deux conduits morts — deux lignes courtes,
    # pour qu'aucun trait interrompu ne traverse le texte.
    x_constat = (CX_SOUF + CX_REPR) / 2
    dispo_constat = CX_REPR - CX_SOUF - w_sal - 10
    for k, l in enumerate(sal["constat"]):
        controler(f"constat CTA {k + 1}", l, 10, "mono", dispo_constat,
                  10 * 0.14)
        A(texte(x_constat, 368 + k * 16, l, "mono", 10, 500, "pivot",
                ancre="middle", tracking=10 * 0.14))

    # ── Laverie : une extraction qui tire, aucun apport en face ──────────────
    conduit_plein(A, CX_LAV, 300, E_ROOM0, w_lav)
    A(fleche(CX_LAV, 296, "encre", "haut", 10))
    A(fleche(CX_LAV, 362, "encre", "haut", 10))
    controler("sortie laverie", lav["sortie"], 10, "mono", 300, 10 * 0.14)
    A(texte(CX_LAV, 278, lav["sortie"], "mono", 10, 500, "pivot",
            ancre="middle", tracking=10 * 0.14))
    for k, l in enumerate(lav["cotes"]):
        controler(f"cote laverie {k + 1}", l, 10, "mono", 216, 10 * 0.14)
        A(texte(CX_LAV - w_lav / 2 - 12, 316 + k * 14, l, "mono", 10, 500,
                "pivot", ancre="end", tracking=10 * 0.14))
    controler("absence laverie", lav["absence"], 10, "mono", 260, 10 * 0.14)
    A(texte((LX0 + CX_LAV - w_lav / 2) / 2, E_Y_ABSENCE, lav["absence"],
            "mono", 10, 500, "pivot", ancre="middle", tracking=10 * 0.14))

    # ── Cuisson : le plus gros débit, sa compensation coupée ─────────────────
    conduit_plein(A, CX_HOT, 300, E_ROOM0, w_hot)
    A(fleche(CX_HOT, 296, "encre", "haut", 14))
    A(fleche(CX_HOT, 362, "encre", "haut", 14))
    controler("cote hotte piano", hot["cote"], 10, "mono", 300, 10 * 0.14)
    A(texte(CX_HOT, 278, hot["cote"], "mono", 10, 500, "pivot",
            ancre="middle", tracking=10 * 0.14))
    # La batterie de compensation : le symbole CVC (rectangle barré), signalée
    # en surchauffe, et le conduit interrompu qui s'arrête avant le local.
    BAX0, BAX1 = CX_CMP - 35, CX_CMP + 35
    A(rect_bord(BAX0, E_MACH0 + 6, BAX1 - BAX0, E_MACH1 - E_MACH0 - 6,
                "papier", "filet-1"))
    A(ligne(BAX0, E_MACH1, BAX1, E_MACH0 + 6, "encre", 1.5))
    controler("mention batterie", cmp_["batterie"], 10, "mono",
              420, 10 * 0.14)
    A(texte(CX_CMP, E_MACH0 - 10, cmp_["batterie"], "mono", 10, 500, "pivot",
            ancre="middle", tracking=10 * 0.14))
    controler("cote compensation", cmp_["cote"], 10, "mono", 190, 10 * 0.14)
    A(texte(BAX0 - 8, 306, cmp_["cote"], "mono", 10, 500, "pivot",
            ancre="end", tracking=10 * 0.14))
    rect_interrompu(A, CX_CMP, E_MACH1, 360, w_cmp)
    # La coupure : deux traits de rupture en travers du conduit, doublés du mot.
    for dy in (0, 8):
        A(ligne(CX_CMP - w_cmp / 2 - 3, 374 + dy, CX_CMP + w_cmp / 2 + 3,
                366 + dy, "encre", 1.5))
    controler("mot de la coupure", cmp_["coupure"], 10, "mono",
              150, 10 * 0.14)
    A(texte(CX_CMP - w_cmp / 2 - 12, E_Y_ABSENCE, cmp_["coupure"], "mono",
            10, 500, "pivot", ancre="end", tracking=10 * 0.14))

    # ── La ligne de pied : ce qui tournait ───────────────────────────────────
    controler("ligne de pied", q["mention_pied"], 10, "mono", UTILE, 10 * 0.14)
    A(texte(MARGE, E_Y_PIED, q["mention_pied"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

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
        "demonstration": "cinq conduits traversent la ligne de toiture (chacun "
                         "par son percement) : deux pleins fléchés vers le "
                         "haut, trois interrompus sans flèche — et AUCUN "
                         "conduit plein ne descend : la géométrie seule montre "
                         "que l'air sort sans être compensé ; les largeurs "
                         f"sont proportionnelles aux débits ({E_K * 1000:.1f} "
                         "px pour 1 000 m³/h), le conduit le plus large du "
                         "dessin étant celui dont la compensation est coupée",
        "topologie": f"machines (y {E_MACH0}–{E_MACH1}) → toiture "
                     f"(y {E_Y_TOIT}) → locaux (y {E_ROOM0}–{E_ROOM1}) ; "
                     f"salles x {SX0}–{SX1} (conduits à {CX_SOUF} et "
                     f"{CX_REPR}), laverie x {LX0}–{LX1} (extraction à "
                     f"{CX_LAV}), cuisson x {CX0}–{CX1} (compensation à "
                     f"{CX_CMP}, hotte à {CX_HOT}) — l'ordre est celui du "
                     "récit de la visite",
        "conduits": f"soufflage/reprise CTA {w_sal:.1f} px chacun — une "
                    f"double flux souffle ET reprend son débit nominal "
                    f"(2 340 m³/h), laverie {w_lav:.1f} px (1 800), "
                    f"compensation {w_cmp:.1f} px (6 000), hotte du piano "
                    f"{w_hot:.1f} px (7 500) — largeur = débit x {E_K:.5f}",
        "bas_du_dessin": f"locaux jusqu'à {E_ROOM1}, ligne de pied à "
                         f"{E_Y_PIED}, phrase de principe à {Y_PHRASE}, "
                         f"cartouche {Y_CARTOUCHE}–{Y_CARTOUCHE + H_CARTOUCHE}, "
                         f"marge basse {H - (Y_CARTOUCHE + H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur * H_CARTOUCHE} px², soit "
                            f"{largeur * H_CARTOUCHE / (W * H) * 100:.2f} % "
                            f"de la planche",
        "chiffre_unique": "aucun chiffre de relevé — la démonstration n'est "
                          "pas chiffrée (révision 4) ; les quatre débits "
                          "restent au mono 10 pivot, en cote de leur conduit",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l'échelle "
                         f"0,96 (1152 / {W})",
        "phrase_principe": f"{len(donnees['phrase_principe'])} signes — "
                           f"{l_phrase:.0f} px mesurés pour {UTILE} disponibles",
        "depassements": depassements if depassements
                        else "aucun — toutes les lignes mesurées sous leur colonne",
    }
    return "\n".join(out) + "\n", controles


def composer_vignette_equilibre(donnees):
    """La vignette : le motif de l'archétype, sans son appareil.

    Ce qu'elle garde : la ligne de toiture percée, les trois locaux, les cinq
    conduits — deux pleins qui montent, trois interrompus — et le nœud chiffré
    de la hotte du piano (7 500 m³/h). Ce qu'elle laisse : la CTA, la
    batterie, le voyant, les cotes, les mentions d'absence et la ligne de
    pied — dix annotations dans 300 px ne se liraient pas."""
    q = donnees["equilibre"]
    elems = {e["cle"]: e for e in q["elements"]}
    hot = elems["cuisson-hotte"]
    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false" '
      f'style="width:100%;height:auto;display:block">')
    entete_style(A)
    A(rect(0, 0, VW, VH, "papier"))
    A(texte(V_MARGE, 22, donnees["vignette_surtitre"], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    # Le motif miniature — mêmes proportions de principe, repère propre.
    y_toit, y_room0, y_room1 = 96, 110, 160
    k = 13 / 7500                                # 7 500 m³/h font 13 px
    cols = ((20, 100), (114, 184), (198, 284))
    cx_souf, cx_repr, cx_lav, cx_cmp, cx_hot = 44, 72, 158, 218, 254
    w_sal, w_lav = 2340 * k, 1800 * k
    w_cmp, w_hot = 6000 * k, 7500 * k

    # La ligne de toiture, percée à chaque conduit.
    x = 20
    for cx, w in sorted((c, w) for c, w in
                        ((cx_souf, w_sal), (cx_repr, w_sal), (cx_lav, w_lav),
                         (cx_cmp, w_cmp), (cx_hot, w_hot))):
        A(ligne(x, y_toit, cx - w / 2 - 3, y_toit, "encre", 1.5))
        x = cx + w / 2 + 3
    A(ligne(x, y_toit, 284, y_toit, "encre", 1.5))

    # Les trois locaux.
    for (x0, x1) in cols:
        A(rect(x0, y_room0, x1 - x0, y_room1 - y_room0, "calcaire"))

    # Salles : la machine et ses deux conduits interrompus, sans flèche.
    A(rect_bord(30, 52, 60, 20, "papier", "filet-1"))
    for cx in (cx_souf, cx_repr):
        A(f'  <rect x="{cx - w_sal / 2:.2f}" y="72" width="{w_sal:.2f}" '
          f'height="{y_room0 - 72}" fill="none" class="s-encre" '
          f'stroke="#00393A" stroke-width="1" stroke-dasharray="4 4"/>')

    # Laverie : la seule extraction qui tire — rien en face.
    A(f'  <rect x="{cx_lav - w_lav / 2:.2f}" y="62" width="{w_lav:.2f}" '
      f'height="{y_room0 - 62}" class="c-clair s-encre" fill="#99CCCD" '
      f'stroke="#00393A" stroke-width="1"/>')
    A(fleche(cx_lav, 58, "encre", "haut", 7))

    # Cuisson : la plus large monte, la compensation s'interrompt.
    A(f'  <rect x="{cx_hot - w_hot / 2:.2f}" y="54" width="{w_hot:.2f}" '
      f'height="{y_room0 - 54}" class="c-clair s-encre" fill="#99CCCD" '
      f'stroke="#00393A" stroke-width="1"/>')
    A(fleche(cx_hot, 50, "encre", "haut", 8))
    A(rect_bord(cx_cmp - 10, 44, 20, 16, "papier", "filet-1"))
    A(ligne(cx_cmp - 10, 60, cx_cmp + 10, 44, "encre", 1))
    A(f'  <rect x="{cx_cmp - w_cmp / 2:.2f}" y="60" width="{w_cmp:.2f}" '
      f'height="24" fill="none" class="s-encre" stroke="#00393A" '
      f'stroke-width="1" stroke-dasharray="4 4"/>')
    for dy in (0, 5):
        A(ligne(cx_cmp - w_cmp / 2 - 2, 90 + dy, cx_cmp + w_cmp / 2 + 2,
                86 + dy, "encre", 1))

    # Le nœud chiffré.
    A(texte(V_MARGE, 182, "Hotte du piano", "sans", 12, 600, "encre",
            wdth=112))
    l_hot = mesurer("Hotte du piano", 12, "sans-600")
    A(texte(V_MARGE + l_hot + 8, 182, f'{hot["valeur"]}{NN}{hot["unite"]}',
            "mono", 10, 500, "pivot", tabulaire=True))

    A("</svg>")
    controles = {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": f"carte de projet mesurée de 274 à 296 px — "
                            f"échelle {274/VW:.2f} à {296/VW:.2f}",
        "corps_minimal": f"9 px dans le repère — rendu à {9*274/VW:.1f} px au pire cas",
        "motif": "la ligne de toiture percée, trois locaux, cinq conduits — "
                 "deux pleins qui montent, trois interrompus — et le nœud "
                 "chiffré de la hotte ; CTA, batterie, cotes et mentions "
                 "sont laissés à la planche",
        "bas_du_dessin": "nœud de la hotte à y 182, marge basse 18 px",
    }
    return "\n".join(out) + "\n", controles


def composer_appui(donnees):
    """L'appui du hero (mécanisme `coupe`) : le motif à l'échelle 1.

    Ce qu'il garde : la coupe fermée par sa bande continue, les champs en
    surimposition, la flèche d'export, et trois nœuds — modules, isolation,
    revente. Ce qu'il laisse : les baies, la centrale, les conduits, la dalle
    annotée et la colonne d'appels — ils vivent sur la planche."""
    elems = {e["cle"]: e for e in donnees["coupe"]["elements"]}
    out = []
    A = out.append
    racine_appui(A, donnees)

    # La coupe — mêmes proportions de principe que la vignette, repère propre.
    mg, md = 74, 296
    y_sol, y_eaves, y_apex = 318, 222, 163
    x_apex = (mg + md) / 2
    pente = (y_eaves - y_apex) / (x_apex - mg)
    v = math.sqrt(1 + pente * pente)

    def apan_y(x):
        return y_apex + abs(x - x_apex) * pente

    def apan_off(x, d):
        return (x, apan_y(x) - d * v)

    A(ligne(46, y_sol, 330, y_sol, "filet-1", 2))
    for k in range(5):
        x = 70 + k * 56
        A(ligne(x, y_sol + 2, x - 8, y_sol + 9, "filet-2", 1))
    A(rect(mg, y_eaves, 4, y_sol - y_eaves, "encre"))
    A(rect(md - 4, y_eaves, 4, y_sol - y_eaves, "encre"))
    A(rect(mg + 4, 266, md - mg - 8, 5, "encre"))
    A(polyligne([(mg, y_eaves), (x_apex, y_apex), (md, y_eaves)], "encre", 2.5))
    # La bande d'enveloppe continue : murs et pans.
    A(rect(60, 216, 8, y_sol - 216, "clair"))
    A(rect(302, 216, 8, y_sol - 216, "clair"))
    A(polyligne([apan_off(60, 10), apan_off(x_apex, 10), apan_off(310, 10)],
                "clair", 7))
    # Les champs, en surimposition, et l'export.
    for (x0, x1) in ((88, 168), (202, 282)):
        milieu = (x0 + x1) / 2
        A(polyligne([apan_off(x0, 24), apan_off(milieu - 4, 24)], "encre", 7))
        A(polyligne([apan_off(milieu + 4, 24), apan_off(x1, 24)], "encre", 7))
    dep = apan_off(202, 24)
    A(polyligne([dep, (dep[0], 96), (452, 96)], "encre", 1.5))
    A(fleche(460, 96, "encre", "droite", 8))

    # Les trois nœuds chiffrés, à droite.
    mod = elems["modules"]
    res = elems["reseau"]
    mur = elems["murs"]
    A(texte(340, 122, mod["libelle"].split(" en ")[0] + " PV", "sans", 14, 600,
            "encre", wdth=112))
    A(texte(340, 139, f'{mod["valeur"]}{NN}{mod["unite"]}', "mono", 11, 500,
            "pivot", tabulaire=True))
    A(texte(340, 76, res["libelle"], "sans", 14, 600, "encre", wdth=112))
    A(polyligne([(452, 82), (440, 92)], "filet-1", 1))
    A(texte(340, 246, mur["libelle"].split(" par ")[0], "sans", 14, 600,
            "encre", wdth=112))
    A(texte(340, 263, f'R{NN}{mur["valeur"]}', "mono", 11, 500, "pivot",
            tabulaire=True))
    A(polyligne([(336, 252), (312, 262)], "filet-1", 1))

    A("</svg>")
    return "\n".join(out) + "\n", controles_appui(
        motif="la coupe fermée par sa bande continue, les champs en "
              "surimposition, la flèche d'export et trois nœuds (modules, "
              "isolation, revente) à l'échelle 1 — baies, centrale, conduits "
              "et appels laissés à la planche",
        bas=f"sol à 318 px (hachures à 327), marge basse {AH - 327} px")


def composer_appui_equilibre(donnees):
    """L'appui du hero (mécanisme `equilibre`) : le motif à l'échelle 1.

    Ce qu'il garde : la ligne de toiture percée, les trois locaux nommés, les
    cinq conduits aux largeurs proportionnelles — deux pleins qui montent,
    trois interrompus — et les cotes des deux extractions. Ce qu'il laisse :
    la CTA détaillée, le voyant, les mentions d'absence, la ligne de pied."""
    q = donnees["equilibre"]
    elems = {e["cle"]: e for e in q["elements"]}
    sal, lav = elems["salles"], elems["laverie"]
    hot, cmp_ = elems["cuisson-hotte"], elems["cuisson-compensation"]
    out = []
    A = out.append
    racine_appui(A, donnees)

    y_toit, y_room0, y_room1 = 178, 202, 300
    k = 24.0 / 7500
    cols = ((A_MARGE, 176), (200, 330), (354, AW - A_MARGE))
    cx_souf, cx_repr, cx_lav, cx_cmp, cx_hot = 68, 124, 290, 400, 470
    w_sal, w_lav = _debit(sal["valeur"]) * k, _debit(lav["valeur"]) * k
    w_cmp, w_hot = _debit(cmp_["valeur"]) * k, _debit(hot["valeur"]) * k

    # La ligne de toiture, percée à chaque conduit.
    x = A_MARGE
    for cx, w in sorted((c, w) for c, w in
                        ((cx_souf, w_sal), (cx_repr, w_sal), (cx_lav, w_lav),
                         (cx_cmp, w_cmp), (cx_hot, w_hot))):
        A(ligne(x, y_toit, cx - w / 2 - 4, y_toit, "encre", 2))
        x = cx + w / 2 + 4
    A(ligne(x, y_toit, AW - A_MARGE, y_toit, "encre", 2))
    # Le libellé de la toiture, dans la seule plage sans conduit (entre la
    # laverie et la batterie) — à la marge il était percé par les conduits
    # de la CTA, mesuré au premier rendu à 552.
    A(texte(340, y_toit - 8, q["toiture"], "mono", 10, 500, "pivot",
            ancre="middle", tracking=10 * 0.14))

    # Les trois locaux, nommés.
    for (x0, x1), e in zip(cols, (sal, lav, hot)):
        A(rect(x0, y_room0, x1 - x0, y_room1 - y_room0, "calcaire"))
        A(texte(x0 + 12, y_room0 + 24, e.get("libelle_dessin", e["libelle"]),
                "sans", 13, 600, "encre", wdth=112))

    # Salles : la CTA et ses deux conduits interrompus — aucun débit constaté.
    A(rect_bord(44, 96, 104, 32, "papier", "filet-1"))
    A(texte(56, 116, sal["machine"], "sans", 13, 600, "encre", wdth=112))
    for cx in (cx_souf, cx_repr):
        A(f'  <rect x="{cx - w_sal / 2:.2f}" y="128" width="{w_sal:.2f}" '
          f'height="{y_room0 - 128}" fill="none" class="s-encre" '
          f'stroke="#00393A" stroke-width="1.2" stroke-dasharray="5 5"/>')
    # Le constat, posé DANS le bloc des salles sous son libellé — entre les
    # conduits il était percé par leurs traits interrompus (rendu à 552).
    for k, l in enumerate(sal["constat"]):
        A(texte(36, y_room0 + 44 + k * 14, l, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))

    # Laverie : une extraction qui tire, rien en face.
    A(f'  <rect x="{cx_lav - w_lav / 2:.2f}" y="112" width="{w_lav:.2f}" '
      f'height="{y_room0 - 112}" class="c-clair s-encre" fill="#99CCCD" '
      f'stroke="#00393A" stroke-width="1"/>')
    A(fleche(cx_lav, 108, "encre", "haut", 9))
    A(texte(cx_lav, 96, f'{lav["valeur"]}{NN}{lav["unite"]}', "mono", 10, 500,
            "pivot", ancre="middle", tracking=10 * 0.14))

    # Cuisson : la plus large monte, la compensation s'interrompt.
    A(f'  <rect x="{cx_hot - w_hot / 2:.2f}" y="100" width="{w_hot:.2f}" '
      f'height="{y_room0 - 100}" class="c-clair s-encre" fill="#99CCCD" '
      f'stroke="#00393A" stroke-width="1"/>')
    A(fleche(cx_hot, 96, "encre", "haut", 10))
    A(texte(cx_hot, 84, f'{hot["valeur"]}{NN}{hot["unite"]}', "mono", 10, 500,
            "pivot", ancre="middle", tracking=10 * 0.14))
    A(rect_bord(cx_cmp - 18, 92, 36, 26, "papier", "filet-1"))
    A(ligne(cx_cmp - 18, 118, cx_cmp + 18, 92, "encre", 1.2))
    A(f'  <rect x="{cx_cmp - w_cmp / 2:.2f}" y="118" width="{w_cmp:.2f}" '
      f'height="36" fill="none" class="s-encre" stroke="#00393A" '
      f'stroke-width="1.2" stroke-dasharray="5 5"/>')
    for dy in (0, 7):
        A(ligne(cx_cmp - w_cmp / 2 - 3, 164 + dy, cx_cmp + w_cmp / 2 + 3,
                158 + dy, "encre", 1.2))
    # Le mot de la coupure, centré sous ses traits — à gauche du conduit il
    # traversait l'extraction de la laverie.
    A(texte(cx_cmp, 190, cmp_["coupure"], "mono", 10, 500, "pivot",
            ancre="middle", tracking=10 * 0.14))

    A("</svg>")
    return "\n".join(out) + "\n", controles_appui(
        motif="la ligne de toiture percée, trois locaux nommés, cinq conduits "
              "proportionnels (24 px pour 7 500 m³/h) — deux pleins cotés qui "
              "montent, trois interrompus dont la compensation supposée "
              "coupée — CTA, voyant, mentions d'absence et ligne de pied "
              "laissés à la planche",
        bas=f"locaux jusqu'à 300 px, marge basse {AH - 300} px")


# ═══ Mécanisme `enjambement` — l'enveloppe d'une parcelle enjambée (Joffre) ══
#
# Trois niveaux empilés sur une parcelle étroite que le bâtiment enjambe : le
# plancher du premier étage passe au-dessus d'un passage voiture et se traite
# comme un plancher sur l'extérieur. La démonstration est portée par la
# géométrie : une ligne isolante (bandes claires) qui ferme TOUTES les faces —
# elle passe SOUS le plancher au-dessus du vide, descend SOUS le sol autour de
# la fosse d'ascenseur, et chaque about de dalle qui l'interrompt est ponté
# d'un rupteur. L'extérieur est fléché sur trois faces, dessous compris ; la
# coupe est un gabarit de principe, aucune proportion d'ouvrage n'est reprise
# (règle 4). Les épaisseurs d'isolant de la fiche gouvernent l'épaisseur des
# bandes (N_K_ISOL) — la face dont la fiche ne fixe pas l'épaisseur est au
# trait minimal, jamais à une épaisseur inventée.

N_MUR_G = 430                 # nu extérieur du mur gauche
N_MUR_M = 674                 # mur droit du RDC — le passage s'ouvre à 680
N_MUR_D = 804                 # nu droit : le mur du R+1, au-dessus du passage
N_EP = 6                      # épaisseur de la structure
N_Y_SOL = 640
N_Y_R1 = 530                  # dessus de la dalle du R+1 (celle qui enjambe)
N_Y_R2 = 420                  # dessus de la dalle du R+2 et de la terrasse
N_Y_PLAF = 316                # plafond du dernier étage
N_Y_TOIT = 265                # toit des combles
N_EP_DALLE = 10

N_K_ISOL = 7.0 / 180          # px par mm d'isolant — 180 mm font 7 px
N_EP_MIN = 5.0                # trait minimal : épaisseur non fixée par la fiche

N_ASC_X0, N_ASC_X1 = 600, 640   # cage d'ascenseur, dans le RDC
N_FOSSE_Y = 660                 # fond de la fosse, sous le sol — la bande
                                # basse s'arrête à 670, la phrase de principe
                                # commence à 675 (688 − ascendante de 13)

N_CALL_L = 250                # colonne d'appels de gauche (x MARGE)
N_CALL_XD = 852               # colonne d'appels de droite


def _rupteur(A, x, y, w):
    """Un about de dalle ponté : réserve papier à filet porteur dans la dalle —
    la dalle ne touche pas la paroi, et c'est ce que le signe montre."""
    A(rect_bord(x, y, w, N_EP_DALLE, "papier", "filet-1"))


def composer_enjambement(donnees):
    q = donnees["enjambement"]
    elems = {e["cle"]: e for e in q["elements"]}
    out = []
    A = out.append
    depassements = []

    def controler(nom, texte_mesure, corps, profil, dispo, tracking=0.0):
        largeur = mesurer(texte_mesure, corps, profil, tracking)
        if largeur > dispo:
            depassements.append(f"{nom} : {largeur:.0f} px pour {dispo:.0f} px")
        return largeur

    # Les épaisseurs de bande, dérivées des épaisseurs d'isolant de la fiche.
    w_mur = 180 * N_K_ISOL      # 7,0
    w_pu = 140 * N_K_ISOL       # 5,4
    w_ldv = 480 * N_K_ISOL      # 18,7
    w_ter = 200 * N_K_ISOL      # 7,8

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
    controler("en-tête schéma", q["entete"], 10, "mono", UTILE, 10 * 0.14)
    A(texte(MARGE, Y_ENTETE, q["entete"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    A(texte(MARGE, Y_TAGS, q["registres"]["gauche"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    A(texte(W - MARGE, Y_TAGS, q["registres"]["droite"], "mono", 10, 500,
            "pivot", ancre="end", tracking=10 * 0.14))

    # ── Le sol — interrompu par la fosse d'ascenseur ─────────────────────────
    A(ligne(356, N_Y_SOL, 591, N_Y_SOL, "filet-1", 2))
    A(ligne(649, N_Y_SOL, 880, N_Y_SOL, "filet-1", 2))
    for x in (380, 470, 560, 700, 790, 866):
        A(ligne(x, N_Y_SOL + 2, x - 9, N_Y_SOL + 10, "filet-2", 1))

    # ── La structure : murs, dalles à abouts pontés, toit ────────────────────
    A(rect(N_MUR_G, N_Y_TOIT, N_EP, N_Y_SOL - N_Y_TOIT, "encre"))          # mur gauche
    A(rect(N_MUR_M, N_Y_TOIT, N_EP, N_Y_R2 - N_Y_TOIT, "encre"))           # mur droit du R+2
    A(rect(N_MUR_M, N_Y_R1 + N_EP_DALLE, N_EP,
           N_Y_SOL - N_Y_R1 - N_EP_DALLE, "encre"))                        # mur droit du RDC
    A(rect(N_MUR_D, 398, N_EP, N_Y_R1 - 398, "encre"))                     # mur droit du R+1 + garde-corps
    A(rect(N_MUR_G, N_Y_TOIT - 4, N_MUR_M + N_EP - N_MUR_G, 4, "encre"))   # toit des combles

    # La dalle du R+2, prolongée en terrasse — trois segments, deux rupteurs.
    A(rect(448, N_Y_R2, 663 - 448, N_EP_DALLE, "encre"))
    A(rect(679, N_Y_R2, N_MUR_D - 679, N_EP_DALLE, "encre"))
    # La dalle du R+1 — celle qui enjambe le passage.
    A(rect(448, N_Y_R1, 794 - 448, N_EP_DALLE, "encre"))
    # Le plafond du dernier étage.
    A(rect(436, N_Y_PLAF, N_MUR_M - 436, 4, "encre"))

    # ── Les rupteurs : quatre abouts de dalle pontés ─────────────────────────
    _rupteur(A, 433, N_Y_R2, 15)
    _rupteur(A, 433, N_Y_R1, 15)
    _rupteur(A, 663, N_Y_R2, 16)
    _rupteur(A, 794, N_Y_R1, 10)

    # ── L'enveloppe : la ligne isolante qui ferme chaque face ────────────────
    # Le plafond du dernier étage porte les deux couches superposées :
    # polyuréthane dessous, laine de verre dessus (position à valider).
    y_pu = N_Y_PLAF - w_pu
    y_ldv = y_pu - 2.5 - w_ldv
    A(rect(436, y_pu, N_MUR_M - 436, w_pu, "clair"))
    A(rect(436, y_ldv, N_MUR_M - 436, w_ldv, "clair"))
    # Murs par l'intérieur — la bande s'interrompt aux dalles, le rupteur ponte.
    for (y0, y1) in ((y_pu, N_Y_R2), (N_Y_R2 + N_EP_DALLE, N_Y_R1),
                     (N_Y_R1 + N_EP_DALLE, N_Y_SOL)):
        A(rect(N_MUR_G + N_EP + 1, y0, w_mur, y1 - y0, "clair"))
    A(rect(N_MUR_M - 1 - w_mur, y_pu, w_mur, N_Y_R2 - y_pu, "clair"))      # mur droit du R+2
    A(rect(679, N_Y_R2 - w_ter, N_MUR_D - 679, w_ter, "clair"))            # toiture-terrasse
    A(rect(N_MUR_D - 1 - w_mur, N_Y_R2 + N_EP_DALLE, w_mur,
           N_Y_R1 - N_Y_R2 - N_EP_DALLE, "clair"))                         # mur du R+1 sur le passage
    A(rect(679, N_Y_R1 + N_EP_DALLE, N_MUR_D - 679, N_EP_MIN, "clair"))    # SOUS le plancher enjambant
    A(rect(N_MUR_M - 1 - w_mur, N_Y_R1 + N_EP_DALLE + N_EP_MIN, w_mur,
           N_Y_SOL - N_Y_R1 - N_EP_DALLE - N_EP_MIN, "clair"))             # mur du RDC sur le passage

    # ── La cage d'ascenseur et sa fosse, sous le sol ─────────────────────────
    A(ligne(N_ASC_X0, 320, N_ASC_X0, N_Y_SOL, "filet-2", 1))
    A(ligne(N_ASC_X1, 320, N_ASC_X1, N_Y_SOL, "filet-2", 1))
    A(polyligne([(N_ASC_X0, N_Y_SOL), (N_ASC_X0, N_FOSSE_Y - 2),
                 (N_ASC_X1, N_FOSSE_Y - 2), (N_ASC_X1, N_Y_SOL)], "encre", 2))
    A(rect(N_ASC_X0 - 7, N_Y_SOL, N_EP_MIN, N_FOSSE_Y - N_Y_SOL + 5, "clair"))
    A(rect(N_ASC_X1 + 2, N_Y_SOL, N_EP_MIN, N_FOSSE_Y - N_Y_SOL + 5, "clair"))
    A(rect(N_ASC_X0 - 7, N_FOSSE_Y + 5, N_ASC_X1 - N_ASC_X0 + 14,
           N_EP_MIN, "clair"))

    # ── Les niveaux, nommés ──────────────────────────────────────────────────
    A(texte(452, 570, q["niveaux"][0], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    A(texte(452, 460, q["niveaux"][1], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    A(texte(452, 350, q["niveaux"][2], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    A(texte(452, 283, q["combles_libelle"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

    # ── L'extérieur, fléché sur trois faces — dessous compris ────────────────
    lab_ext = q["exterieur_libelle"]
    A(texte(555, 214, lab_ext, "mono", 10, 500, "pivot", ancre="middle",
            tracking=10 * 0.14))
    A(ligne(555, 222, 555, 246, "encre", 1))
    A(fleche(555, 255, "encre", "bas", 8))
    A(texte(386, 484, lab_ext, "mono", 10, 500, "pivot", ancre="end",
            tracking=10 * 0.14))
    A(ligne(394, 480, 416, 480, "encre", 1))
    A(fleche(424, 480, "encre", "droite", 8))
    # Dans le vide du passage : l'extérieur pointe le dessous du plancher.
    A(texte(742, 594, lab_ext, "mono", 10, 500, "pivot", ancre="middle",
            tracking=10 * 0.14))
    A(ligne(742, 578, 742, 558, "encre", 1))
    A(fleche(742, 551, "encre", "haut", 8))
    # Le passage voiture : la flèche traverse le vide et SORT du dessin par
    # l'ouverture réelle du passage, sous le mur du R+1 — le côté droit est
    # ouvert sur la rue, et c'est ce que la flèche montre.
    A(ligne(690, 610, 1050, 610, "encre", 1.5))
    A(fleche(1058, 610, "encre", "droite", 9))
    controler("passage voiture", q["passage_libelle"], 10, "mono",
              240, 10 * 0.14)
    A(texte(880, 628, q["passage_libelle"], "mono", 10, 500, "pivot",
            ancre="middle", tracking=10 * 0.14))

    # ── La colonne d'appels de gauche ────────────────────────────────────────
    appels_g = [
        ("combles", 296, (500, y_ldv + w_ldv / 2)),
        ("dernier-etage", 368, (490, y_pu + w_pu / 2)),
        ("murs", 440, (N_MUR_G + N_EP + 1 + w_mur / 2, 470)),
        ("rupteurs", 512, (440, N_Y_R1 + 5)),
        ("ascenseur", 584, (N_ASC_X0 - 5, 648)),
    ]
    for cle, base, cible in appels_g:
        e = elems[cle]
        appel(A, MARGE, base, e["libelle"], e["detail"], N_CALL_L, cible,
              controler, cle)

    # ── La colonne d'appels de droite — attache à gauche du libellé ──────────
    appels_d = [
        ("toiture-terrasse", 348, (770, N_Y_R2 - w_ter / 2)),
        ("plancher-passage", 436, (752, N_Y_R1 + N_EP_DALLE + N_EP_MIN / 2)),
    ]
    for cle, base, cible in appels_d:
        e = elems[cle]
        controler(f"appel {cle} — libellé", e["libelle"], 15, "sans-400",
                  W - MARGE - N_CALL_XD)
        A(texte(N_CALL_XD, base, e["libelle"], "sans", 15, 400, "encre",
                wdth=100))
        for k, l in enumerate(e["detail"]):
            controler(f"appel {cle} — détail {k + 1}", l, 10, "mono",
                      W - MARGE - N_CALL_XD, 10 * 0.14)
            A(texte(N_CALL_XD, base + 18 + k * 14, l, "mono", 10, 500,
                    "pivot", tracking=10 * 0.14))
        A(polyligne([(N_CALL_XD - 8, base - 4), cible], "filet-1", 1))

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
        "demonstration": "la ligne isolante (bandes claires) ferme chaque face "
                         "de l'empilement, y compris trois faces qu'un bâtiment "
                         "ordinaire n'a pas : SOUS la dalle du R+1 au-dessus du "
                         "vide du passage (l'extérieur y est fléché vers le "
                         "haut), autour de la fosse d'ascenseur SOUS le sol, et "
                         "à chaque about de dalle, ponté d'un rupteur — texte "
                         "masqué, la bande continue et le vide traversé par la "
                         "flèche suffisent à lire l'enjambement",
        "topologie": f"appels gauche (x {MARGE}–{MARGE + N_CALL_L}) → coupe "
                     f"(x {N_MUR_G}–{N_MUR_D + N_EP}, sol {N_Y_SOL}, toit "
                     f"{N_Y_TOIT - 4}, passage x 680–{N_MUR_D} sous la dalle "
                     f"{N_Y_R1}) → appels droite (x {N_CALL_XD}–{W - MARGE}) ; "
                     f"fosse y {N_Y_SOL}–{N_FOSSE_Y + 10}",
        "bandes": f"épaisseur = épaisseur d'isolant x {N_K_ISOL:.4f} px/mm : "
                  f"murs {w_mur:.1f} px (180 mm), polyuréthane {w_pu:.1f} px "
                  f"(140 mm), laine de verre {w_ldv:.1f} px (480 mm), "
                  f"toiture-terrasse {w_ter:.1f} px (200 mm) — le plancher sur "
                  f"le passage et la fosse, dont la fiche ne fixe pas "
                  f"l'épaisseur, sont au trait minimal de {N_EP_MIN:.0f} px",
        "bas_du_dessin": f"sol à {N_Y_SOL}, fosse jusqu'à {N_FOSSE_Y + 10}, "
                         f"dernier appel à 602, phrase de principe à "
                         f"{Y_PHRASE}, cartouche {Y_CARTOUCHE}–"
                         f"{Y_CARTOUCHE + H_CARTOUCHE}, marge basse "
                         f"{H - (Y_CARTOUCHE + H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur * H_CARTOUCHE} px², soit "
                            f"{largeur * H_CARTOUCHE / (W * H) * 100:.2f} % "
                            f"de la planche",
        "chiffre_unique": "aucun chiffre de relevé — les résultats RE2020 "
                          "restent à la page (révision 4) ; les épaisseurs "
                          "d'isolant sont des cotes mono 10 pivot dans les "
                          "appels",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l'échelle "
                         f"0,96 (1152 / {W})",
        "phrase_principe": f"{len(donnees['phrase_principe'])} signes — "
                           f"{l_phrase:.0f} px mesurés pour {UTILE} disponibles",
        "depassements": depassements if depassements
                        else "aucun — toutes les lignes mesurées sous leur colonne",
    }
    return "\n".join(out) + "\n", controles


def composer_vignette_enjambement(donnees):
    """La vignette : le motif de l'archétype, sans son appareil.

    Deux traits seulement, pour que le motif se lise à 274 px : la SILHOUETTE
    encrée du bâtiment — avec l'encoche du passage sous le flanc droit — et la
    LIGNE ISOLANTE claire qui la double à l'intérieur, continue de face en
    face, dessous du plancher et fosse compris ; une flèche traverse l'encoche
    et en sort. Ce qu'elle laisse : les dalles, les rupteurs, les niveaux
    nommés, les flèches d'extérieur, les appels — sept organes annotés dans
    300 px ne se liraient pas."""
    elems = {e["cle"]: e for e in donnees["enjambement"]["elements"]}
    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false" '
      f'style="width:100%;height:auto;display:block">')
    entete_style(A)
    A(rect(0, 0, VW, VH, "papier"))
    A(texte(V_MARGE, 22, donnees["vignette_surtitre"], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    # Le sol, interrompu par la fosse.
    y_sol = 168
    A(ligne(26, y_sol, 88, y_sol, "filet-1", 1.5))
    A(ligne(124, y_sol, 258, y_sol, "filet-1", 1.5))

    # La silhouette : l'encoche du passage est le profil même de l'enjambement.
    A(polyligne([(44, y_sol), (44, 52), (160, 52), (160, 94), (228, 94),
                 (228, 140), (164, 140), (164, y_sol)], "encre", 2.5))
    # La ligne isolante, continue à l'intérieur de la silhouette.
    A(polyligne([(49, y_sol), (49, 58), (154, 58), (154, 97), (222, 97),
                 (222, 134), (166, 134), (166, y_sol)], "clair", 4))
    # La fosse d'ascenseur, sous le sol — la ligne descend plus bas que le sol.
    A(polyligne([(96, y_sol), (96, 182), (114, 182), (114, y_sol)],
                "encre", 1.5))
    A(polyligne([(92, y_sol), (92, 187), (118, 187), (118, y_sol)],
                "clair", 3))
    # La flèche qui traverse l'encoche et en sort.
    A(ligne(172, 156, 240, 156, "encre", 1.2))
    A(fleche(247, 156, "encre", "droite", 6))

    # Les deux nœuds chiffrés.
    A(texte(240, 64, "Combles", "sans", 12, 600, "encre", wdth=112))
    A(texte(240, 78, f'{elems["combles"]["valeur"]}{NN}{elems["combles"]["unite"]}',
            "mono", 10, 500, "pivot", tabulaire=True))
    A(polyligne([(237, 60), (157, 59)], "filet-1", 1))
    A(texte(240, 110, elems["murs"]["libelle"].split(",")[0], "sans", 12, 600,
            "encre", wdth=112))
    A(texte(240, 124, f'{elems["murs"]["valeur"]}{NN}{elems["murs"]["unite"]}',
            "mono", 10, 500, "pivot", tabulaire=True))
    A(polyligne([(237, 106), (224, 112)], "filet-1", 1))

    A("</svg>")
    controles = {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": f"carte de projet mesurée de 274 à 296 px — "
                            f"échelle {274/VW:.2f} à {296/VW:.2f}",
        "corps_minimal": f"9 px dans le repère — rendu à {9*274/VW:.1f} px au pire cas",
        "motif": "deux traits : la silhouette encrée à encoche de passage, la "
                 "ligne isolante claire qui la double — dessous du plancher et "
                 "fosse compris — une flèche qui sort par l'encoche, deux "
                 "nœuds chiffrés ; dalles, rupteurs, niveaux et appels sont "
                 "laissés à la planche",
        "bas_du_dessin": "fosse jusqu'à 189 px, marge basse 11 px",
    }
    return "\n".join(out) + "\n", controles


def composer_appui_enjambement(donnees):
    """L'appui du hero : le motif à l'échelle 1.

    Ce qu'il garde : l'empilement aux niveaux nommés, le passage voiture
    fléché sous la dalle, la ligne isolante complète — dessous, terrasse et
    fosse compris, rupteurs aux abouts — et trois nœuds chiffrés (combles,
    toiture-terrasse, murs). Ce qu'il laisse : les flèches d'extérieur, les
    détails d'appel, la phrase et le cartouche."""
    q = donnees["enjambement"]
    elems = {e["cle"]: e for e in q["elements"]}
    out = []
    A = out.append
    racine_appui(A, donnees)

    ag, am, ad = 60, 246, 352          # murs gauche, médian, droit
    y_sol, y_r1, y_r2 = 322, 240, 158
    y_plaf, y_pu, y_ldv = 116, 111, 96
    fx0, fx1, fy = 196, 228, 340       # la fosse

    # Le sol, interrompu par la fosse.
    A(ligne(40, y_sol, fx0 - 8, y_sol, "filet-1", 2))
    A(ligne(fx1 + 8, y_sol, 500, y_sol, "filet-1", 2))
    for x in (64, 130, 262, 330, 388):
        A(ligne(x, y_sol + 2, x - 7, y_sol + 8, "filet-2", 1))

    # La structure.
    A(rect(ag, 76, 4, y_sol - 76, "encre"))
    A(rect(am, 76, 4, y_r2 - 76, "encre"))
    A(rect(am, y_r1 + 7, 4, y_sol - y_r1 - 7, "encre"))
    A(rect(ad, 144, 4, y_r1 - 144, "encre"))
    A(rect(ag, 73, am + 4 - ag, 3, "encre"))
    A(rect(ag + 4, y_plaf, am - ag - 4, 3, "encre"))
    # Dalles à abouts pontés.
    A(rect(76, y_r2, 240 - 76 + 4, 7, "encre"))
    A(rect(254, y_r2, ad - 254, 7, "encre"))
    A(rect(76, y_r1, 338 - 76, 7, "encre"))
    for (x, y, w) in ((64, y_r2, 12), (64, y_r1, 12), (240, y_r2, 14),
                      (338, y_r1, 14)):
        A(rect_bord(x, y, w, 7, "papier", "filet-1"))

    # La ligne isolante.
    A(rect(64, y_ldv, am - 64, 14, "clair"))
    A(rect(64, y_pu, am - 64, 4, "clair"))
    for (y0, y1) in ((115, y_r2), (y_r2 + 7, y_r1), (y_r1 + 7, y_sol)):
        A(rect(65, y0, 4, y1 - y0, "clair"))
    A(rect(241, 115, 4, y_r2 - 115, "clair"))
    A(rect(254, y_r2 - 6, ad - 254, 6, "clair"))               # toiture-terrasse
    A(rect(347, y_r2 + 7, 4, y_r1 - y_r2 - 7, "clair"))
    A(rect(254, y_r1 + 7, ad - 254, 4, "clair"))               # SOUS le plancher
    A(rect(241, y_r1 + 11, 4, y_sol - y_r1 - 11, "clair"))
    # La cage et sa fosse.
    A(ligne(fx0, y_plaf + 3, fx0, y_sol, "filet-2", 1))
    A(ligne(fx1, y_plaf + 3, fx1, y_sol, "filet-2", 1))
    A(polyligne([(fx0, y_sol), (fx0, fy - 2), (fx1, fy - 2), (fx1, y_sol)],
                "encre", 1.5))
    A(rect(fx0 - 6, y_sol, 4, fy - y_sol + 4, "clair"))
    A(rect(fx1 + 2, y_sol, 4, fy - y_sol + 4, "clair"))
    A(rect(fx0 - 6, fy + 4, fx1 - fx0 + 12, 4, "clair"))

    # Les niveaux, en tête de bande.
    for lib, y in ((q["niveaux"][0], 300), (q["niveaux"][1], 214),
                   (q["niveaux"][2], 150)):
        A(texte(74, y, lib.split(" · ")[0], "mono", 10, 500, "pivot",
                tracking=10 * 0.14))
    A(texte(74, 90, q["combles_libelle"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

    # Le passage voiture : la flèche traverse le vide et sort par l'ouverture
    # réelle du passage, sous le mur du R+1 — le libellé la suit, dehors.
    A(ligne(262, 296, 470, 296, "encre", 1.2))
    A(fleche(478, 296, "encre", "droite", 8))
    A(texte(368, 314, q["passage_libelle"], "mono", 10, 500, "pivot",
            ancre="middle", tracking=10 * 0.14))

    # Les trois nœuds chiffrés, à droite.
    com, ter, mur = elems["combles"], elems["toiture-terrasse"], elems["murs"]
    A(texte(380, 100, com["libelle"], "sans", 14, 600, "encre", wdth=112))
    A(texte(380, 117, f'{com["valeur"]}{NN}{com["unite"]}', "mono", 11, 500,
            "pivot", tabulaire=True))
    A(polyligne([(376, 96), (250, 103)], "filet-1", 1))
    A(texte(380, 160, ter["libelle"], "sans", 14, 600, "encre", wdth=112))
    A(texte(380, 177, f'{ter["valeur"]}{NN}{ter["unite"]}', "mono", 11, 500,
            "pivot", tabulaire=True))
    A(polyligne([(376, 156), (354, 155)], "filet-1", 1))
    A(texte(380, 215, mur["libelle"].split(",")[0], "sans", 14, 600, "encre",
            wdth=112))
    A(texte(380, 232, f'{mur["valeur"]}{NN}{mur["unite"]}', "mono", 11, 500,
            "pivot", tabulaire=True))
    A(polyligne([(376, 211), (353, 214)], "filet-1", 1))

    A("</svg>")
    return "\n".join(out) + "\n", controles_appui(
        motif="l'empilement aux niveaux nommés, le passage voiture fléché "
              "sous la dalle isolée, la ligne isolante complète — dessous, "
              "terrasse et fosse compris, quatre abouts pontés — et trois "
              "nœuds chiffrés à l'échelle 1 ; flèches d'extérieur, appels, "
              "phrase et cartouche laissés à la planche",
        bas=f"fosse jusqu'à 344 px, marge basse {AH - 344} px")


# ═══ Dispatch — le bloc de l'extraction choisit le mécanisme ═════════════════

def _composer(donnees):
    if "equilibre" in donnees:
        return composer_equilibre(donnees)
    if "enjambement" in donnees:
        return composer_enjambement(donnees)
    return composer(donnees)


def _composer_vignette(donnees):
    if "equilibre" in donnees:
        return composer_vignette_equilibre(donnees)
    if "enjambement" in donnees:
        return composer_vignette_enjambement(donnees)
    return composer_vignette(donnees)


def _composer_appui(donnees):
    if "equilibre" in donnees:
        return composer_appui_equilibre(donnees)
    if "enjambement" in donnees:
        return composer_appui_enjambement(donnees)
    return composer_appui(donnees)


if __name__ == "__main__":
    executer(_composer, _composer_vignette, _composer_appui)
