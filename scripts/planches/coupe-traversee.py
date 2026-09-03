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
- `colonne` — le conduit collectif 3CEp (résidence Aurora) : une chaudière
  étanche par logement, et, en gaine technique, un conduit concentrique
  unique traversant les niveaux — fumées par le cœur, air de combustion par
  la couronne, clapet à chaque piquage, té de purge en pied — confronté à la
  ventouse individuelle et aux trois gabarits de débit du label.
- `sortie` — l'extraction quitte le logement (cité Louise Magnan) : deux
  maisons de principe confrontées, AVANT et APRÈS — à gauche le relevé du
  diagnostic (extracteur en coffre, gaines souples toutes branchées sur le
  seul piquage cuisine, rejet en façade, entrées d'air obturées), à droite
  le dossier de consultation (caisson sur dallettes en toiture-terrasse,
  traversée carottée, fourreautée et bavettée, un piquage rigide par bouche,
  sifflet de rejet) ; puis quatre gabarits de largeur proportionnelle aux
  débits de caisson des quatre typologies, comptés jusqu'à soixante.
- `frontiere` — deux régimes de desserte sous un même toit (bâtiment
  d'assemblage de Saint-Agnant) : un mur plein sépare le hall d'assemblage du
  plateau de bureaux, et quatre familles de services le rencontrent — l'air
  traité a sa machine de chaque côté, le 220 V descend d'un maillage de
  plafond à gauche et monte de la plinthe à droite, l'air comprimé et le
  triphasé de charge n'ont pas de côté droit du tout. La colonne de droite
  s'interrompt à mi-hauteur : c'est la démonstration.
"""

import math
import re as _re

from _tronc import (NN, W, H, MARGE, UTILE, VW, VH, V_MARGE, AW, AH, A_MARGE,
                    mesurer, replier, echapper, texte, rect, rect_bord, ligne,
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
        "demonstration": "la ligne d’enveloppe (bandes claires) est continue du "
                         "sol au faîtage et ne s’interrompt qu’aux traversées "
                         "marquées : 2 baies vitrées, 2 conduits d’air fléchés "
                         "en sens opposés — les champs de modules sont posés "
                         "AU-DESSUS des couches (surimposition) et la chaîne "
                         "sort du cadre à droite : la géométrie porte la thèse "
                         "« l’enveloppe d’abord, la production ensuite »",
        "topologie": f"appels (x {CALL_X}–{CALL_X + CALL_L}) → coupe "
                     f"(x {ITE_X0G}–{ITE_X1D}, sol {Y_SOL}, faîtage {Y_APEX}) "
                     f"→ production (onduleurs x {BOX_OND[0]}–"
                     f"{BOX_OND[0] + BOX_OND[2]}, export y {Y_EXPORT} "
                     f"jusqu’à x {X_EXPORT_FIN + 8})",
        "pans": f"pente {PENTE:.2f} — couches à {D_C280} et {D_C220} px des "
                f"pans, modules à {D_PV} px (surimposition lisible)",
        "bas_du_dessin": f"sol à {Y_SOL} (hachures jusqu’à {Y_SOL + 10}), "
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
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l’échelle "
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
                 "surimposition et la flèche d’export — baies, centrale, "
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
                         "que l’air sort sans être compensé ; les largeurs "
                         f"sont proportionnelles aux débits ({E_K * 1000:.1f} "
                         "px pour 1 000 m³/h), le conduit le plus large du "
                         "dessin étant celui dont la compensation est coupée",
        "topologie": f"machines (y {E_MACH0}–{E_MACH1}) → toiture "
                     f"(y {E_Y_TOIT}) → locaux (y {E_ROOM0}–{E_ROOM1}) ; "
                     f"salles x {SX0}–{SX1} (conduits à {CX_SOUF} et "
                     f"{CX_REPR}), laverie x {LX0}–{LX1} (extraction à "
                     f"{CX_LAV}), cuisson x {CX0}–{CX1} (compensation à "
                     f"{CX_CMP}, hotte à {CX_HOT}) — l’ordre est celui du "
                     "récit de la visite",
        "conduits": f"soufflage/reprise CTA {w_sal:.1f} px chacun — une "
                    f"double flux souffle ET reprend son débit nominal "
                    f"(2 340 m³/h), laverie {w_lav:.1f} px (1 800), "
                    f"compensation {w_cmp:.1f} px (6 000), hotte du piano "
                    f"{w_hot:.1f} px (7 500) — largeur = débit x {E_K:.5f}",
        "bas_du_dessin": f"locaux jusqu’à {E_ROOM1}, ligne de pied à "
                         f"{E_Y_PIED}, phrase de principe à {Y_PHRASE}, "
                         f"cartouche {Y_CARTOUCHE}–{Y_CARTOUCHE + H_CARTOUCHE}, "
                         f"marge basse {H - (Y_CARTOUCHE + H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur * H_CARTOUCHE} px², soit "
                            f"{largeur * H_CARTOUCHE / (W * H) * 100:.2f} % "
                            f"de la planche",
        "chiffre_unique": "aucun chiffre de relevé — la démonstration n’est "
                          "pas chiffrée (révision 4) ; les quatre débits "
                          "restent au mono 10 pivot, en cote de leur conduit",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l’échelle "
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
              "surimposition, la flèche d’export et trois nœuds (modules, "
              "isolation, revente) à l’échelle 1 — baies, centrale, conduits "
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
              "coupée — CTA, voyant, mentions d’absence et ligne de pied "
              "laissés à la planche",
        bas=f"locaux jusqu’à 300 px, marge basse {AH - 300} px")


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
                         "de l’empilement, y compris trois faces qu’un bâtiment "
                         "ordinaire n’a pas : SOUS la dalle du R+1 au-dessus du "
                         "vide du passage (l’extérieur y est fléché vers le "
                         "haut), autour de la fosse d’ascenseur SOUS le sol, et "
                         "à chaque about de dalle, ponté d’un rupteur — texte "
                         "masqué, la bande continue et le vide traversé par la "
                         "flèche suffisent à lire l’enjambement",
        "topologie": f"appels gauche (x {MARGE}–{MARGE + N_CALL_L}) → coupe "
                     f"(x {N_MUR_G}–{N_MUR_D + N_EP}, sol {N_Y_SOL}, toit "
                     f"{N_Y_TOIT - 4}, passage x 680–{N_MUR_D} sous la dalle "
                     f"{N_Y_R1}) → appels droite (x {N_CALL_XD}–{W - MARGE}) ; "
                     f"fosse y {N_Y_SOL}–{N_FOSSE_Y + 10}",
        "bandes": f"épaisseur = épaisseur d’isolant x {N_K_ISOL:.4f} px/mm : "
                  f"murs {w_mur:.1f} px (180 mm), polyuréthane {w_pu:.1f} px "
                  f"(140 mm), laine de verre {w_ldv:.1f} px (480 mm), "
                  f"toiture-terrasse {w_ter:.1f} px (200 mm) — le plancher sur "
                  f"le passage et la fosse, dont la fiche ne fixe pas "
                  f"l’épaisseur, sont au trait minimal de {N_EP_MIN:.0f} px",
        "bas_du_dessin": f"sol à {N_Y_SOL}, fosse jusqu’à {N_FOSSE_Y + 10}, "
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
                          "d’isolant sont des cotes mono 10 pivot dans les "
                          "appels",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l’échelle "
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
                 "fosse compris — une flèche qui sort par l’encoche, deux "
                 "nœuds chiffrés ; dalles, rupteurs, niveaux et appels sont "
                 "laissés à la planche",
        "bas_du_dessin": "fosse jusqu’à 189 px, marge basse 11 px",
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
        motif="l’empilement aux niveaux nommés, le passage voiture fléché "
              "sous la dalle isolée, la ligne isolante complète — dessous, "
              "terrasse et fosse compris, quatre abouts pontés — et trois "
              "nœuds chiffrés à l’échelle 1 ; flèches d’extérieur, appels, "
              "phrase et cartouche laissés à la planche",
        bas=f"fosse jusqu’à 344 px, marge basse {AH - 344} px")


# ═══ Mécanisme `portee` — la mission bornée, le système entier (Yachtman) ════
#
# Deux bâtiments accolés en piles topologiques — trois étages sur sous-sol
# côté quai, cinq côté rue Saint-Nicolas — sur une même grille de niveaux.
# La démonstration est portée par la géométrie : deux bandes de travaux
# (calcaire, largeurs proportionnelles aux 140 et 90 m² de la fiche, cernées
# d'un périmètre encré en L) tiennent dans le coin bas-gauche de la coupe,
# quand l'enceinte de la zone d'alarme (bande claire continue) enclot les
# deux piles entières — sous-sol et combles compris — et que la détection
# (points clairs cerclés d'encre) occupe chaque niveau. Aucune proportion
# d'ouvrage : hauteurs de niveau égales, largeurs de pile égales (règle 4) ;
# seules les deux emprises de travaux sont proportionnelles ENTRE ELLES.

P_H_NIV = 50                  # hauteur d'un niveau — jamais une cote réelle
P_Y_GRADE = 610               # la ligne de sol (le quai)
P_Y_FOND = 660                # fond du sous-sol
P_QX0, P_QX1 = 380, 590       # pile côté quai
P_SX0, P_SX1 = 590, 800       # pile côté rue Saint-Nicolas
P_Y_TOIT_Q = 410              # toit du quai — dessus du R+3
P_Y_TOIT_S = 310              # dessus du R+5 — plancher des combles
P_Y_COMBLES = 292             # dessus des combles Saint-Nicolas
P_K_M2 = 1.3                  # px par m² d'emprise de travaux
P_ENV = 8                     # retrait de l'enceinte de zone d'alarme
P_X_RISER = 610               # colonne montante de la détection adressable
P_X_DOT_Q, P_X_DOT_S = 470, 700
P_X_ARROW = 420               # la salle qui redescend
P_CALL_L = 250                # colonne d'appels de gauche
P_CALL_XD = 830               # colonne d'appels de droite
P_Y_LEGENDE = 262             # la légende des signes


def _boitier(A, x, y, c, ep=1.5, interne=False):
    """Un boîtier SSI : carré papier à contour encré. La centrale est le grand
    (22, trait 1,5) ; le répétiteur le petit (12, trait 1) barré d'une ligne —
    la taille seule ne porte jamais la distinction, la légende la double."""
    from _tronc import JETON
    A(f'  <rect x="{x:.2f}" y="{y:.2f}" width="{c:.2f}" height="{c:.2f}" '
      f'class="c-papier s-encre" fill="{JETON["papier"]}" '
      f'stroke="{JETON["encre"]}" stroke-width="{ep}"/>')
    if interne:
        A(ligne(x + 2.5, y + c / 2, x + c - 2.5, y + c / 2, "encre", 1))


def _pointille(A, x0, y0, x1, y1, ep=1.2, motif="6 6"):
    """La mitoyenneté : les deux bâtiments sont accolés et NON isolés l'un de
    l'autre — le trait interrompu dit la limite qui ne sépare pas."""
    from _tronc import JETON
    A(f'  <path d="M {x0:.2f} {y0:.2f} L {x1:.2f} {y1:.2f}" fill="none" '
      f'class="s-encre" stroke="{JETON["encre"]}" stroke-width="{ep}" '
      f'stroke-dasharray="{motif}"/>')


def composer_portee(donnees):
    q = donnees["portee"]
    elems = {e["cle"]: e for e in q["elements"]}
    out = []
    A = out.append
    depassements = []

    def controler(nom, texte_mesure, corps, profil, dispo, tracking=0.0):
        largeur = mesurer(texte_mesure, corps, profil, tracking)
        if largeur > dispo:
            depassements.append(f"{nom} : {largeur:.0f} px pour {dispo:.0f} px")
        return largeur

    w_rdc = 140 * P_K_M2      # 182 — l'emprise du rez-de-chaussée
    w_r1 = 90 * P_K_M2        # 117 — l'emprise de l'étage
    bx = P_QX0 + 3            # les bandes s'appuient sur la façade du quai

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

    # ── En-tête, registres, légende des signes ───────────────────────────────
    controler("en-tête schéma", q["entete"], 10, "mono", UTILE, 10 * 0.14)
    A(texte(MARGE, Y_ENTETE, q["entete"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    controler("registre gauche", q["registres"]["gauche"], 10, "mono",
              520, 10 * 0.14)
    A(texte(MARGE, Y_TAGS, q["registres"]["gauche"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    controler("registre droite", q["registres"]["droite"], 10, "mono",
              520, 10 * 0.14)
    A(texte(W - MARGE, Y_TAGS, q["registres"]["droite"], "mono", 10, 500,
            "pivot", ancre="end", tracking=10 * 0.14))
    # La légende : un signe n'est jamais porté par sa seule forme.
    x_leg = MARGE + 4
    A(cercle(x_leg, P_Y_LEGENDE - 3.5, 3.5, "clair", "encre", 1))
    x_leg += 12
    for k, lib in enumerate(q["legende"]):
        controler(f"légende {k + 1}", lib, 10, "mono", 300, 10 * 0.14)
        A(texte(x_leg, P_Y_LEGENDE, lib, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))
        x_leg += mesurer(lib, 10, "mono", 10 * 0.14) + 24
        if k == 0:
            _boitier(A, x_leg, P_Y_LEGENDE - 10, 11, 1.5)
            x_leg += 19
        elif k == 1:
            _boitier(A, x_leg, P_Y_LEGENDE - 9, 9, 1, interne=True)
            x_leg += 17

    # ── Les bandes de travaux — posées sous les traits de structure ──────────
    A(rect(bx, 512, w_r1, 48, "calcaire"))
    A(rect(bx, 560, w_rdc, 48, "calcaire"))

    # ── Les planchers, la trame des niveaux ──────────────────────────────────
    for y in (460, 510, 560, P_Y_GRADE):
        A(ligne(P_QX0 + 2, y, P_QX1 - 2, y, "filet-2", 1))
    for y in (P_Y_TOIT_S, 360, 410, 460, 510, 560, P_Y_GRADE):
        A(ligne(P_SX0 + 2, y, P_SX1 - 2, y, "filet-2", 1))

    # ── Les contours des deux piles ──────────────────────────────────────────
    A(polyligne([(P_QX0, P_Y_FOND), (P_QX0, P_Y_TOIT_Q), (P_QX1, P_Y_TOIT_Q)],
                "encre", 2))
    A(polyligne([(P_SX0, P_Y_TOIT_Q), (P_SX0, P_Y_COMBLES),
                 (P_SX1, P_Y_COMBLES), (P_SX1, P_Y_FOND)], "encre", 2))
    A(ligne(P_QX0, P_Y_FOND, P_SX1, P_Y_FOND, "encre", 2))
    _pointille(A, P_SX0, P_Y_TOIT_Q, P_SX0, P_Y_FOND)

    # La ligne de sol — à gauche seulement : à droite, l'enceinte de zone
    # d'alarme (x 808) puis la colonne d'appels (x 830) ne lui laissent
    # aucune place, et le talon atterrissait sous le texte de l'appel.
    A(ligne(324, P_Y_GRADE, 364, P_Y_GRADE, "filet-1", 2))
    for x in (336, 354):
        A(ligne(x, P_Y_GRADE + 2, x - 8, P_Y_GRADE + 9, "filet-2", 1))

    # ── Le périmètre de la mission — le L encré sur les deux bandes ──────────
    A(polyligne([(bx, 512), (bx + w_r1, 512), (bx + w_r1, 560),
                 (bx + w_rdc, 560), (bx + w_rdc, 608), (bx, 608), (bx, 512)],
                "encre", 2))
    controler("périmètre mission", q["perimetre_mission"], 10, "mono",
              200, 10 * 0.14)
    A(texte(bx, 505, q["perimetre_mission"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

    # La salle qui redescend : l'étage devient de l'hébergement.
    A(ligne(P_X_ARROW, 528, P_X_ARROW, 583, "encre", 1.5))
    A(fleche(P_X_ARROW, 591, "encre", "bas", 9))

    # ── L'enceinte de la zone d'alarme — elle enclot TOUT ────────────────────
    env = [(P_QX0 - P_ENV, P_Y_FOND + P_ENV), (P_QX0 - P_ENV, P_Y_TOIT_Q - P_ENV),
           (P_SX0 - P_ENV, P_Y_TOIT_Q - P_ENV), (P_SX0 - P_ENV, P_Y_COMBLES - P_ENV),
           (P_SX1 + P_ENV, P_Y_COMBLES - P_ENV), (P_SX1 + P_ENV, P_Y_FOND + P_ENV)]
    A(polyligne(env + [env[0]], "clair", 4))

    # ── La détection : la colonne montante et un point par niveau ────────────
    _boitier(A, 566, 580, 22, 1.5)                       # la centrale, au RDC
    A(ligne(588, 591, P_X_RISER, 591, "encre", 1))  # traverse la mitoyenneté
    A(ligne(P_X_RISER, 301, P_X_RISER, 635, "encre", 1.5))
    for y in (635, 585, 535, 485, 435):
        A(cercle(P_X_DOT_Q, y, 3.5, "clair", "encre", 1))
    for y in (635, 585, 535, 485, 435, 385, 335, 301):
        A(cercle(P_X_DOT_S, y, 3.5, "clair", "encre", 1))
    _boitier(A, 505, 578, 12, 1, interne=True)           # répétiteur du bar
    _boitier(A, 734, 372, 12, 1, interne=True)           # répétiteur du R+4

    # L'escalier neuf de la seconde dérogation, du R+3 au R+4.
    pas = [(640, 434)]
    for k in range(4):
        x0, y0 = pas[-1]
        pas += [(x0 + 8, y0), (x0 + 8, y0 - 12)]
    A(polyligne(pas, "encre", 1.5))
    controler("mention escalier", q["mention_escalier"], 10, "mono",
              120, 10 * 0.14)
    A(texte(656, 380, q["mention_escalier"], "mono", 10, 500, "pivot",
            ancre="middle", tracking=10 * 0.14))

    # ── Les niveaux et les deux bâtiments, nommés ────────────────────────────
    niv = q["niveaux"]
    for lib, y in zip(niv[:5], (638, 588, 538, 488, 438)):
        A(texte(362, y, lib, "mono", 10, 500, "pivot", ancre="end",
                tracking=10 * 0.14))
    for lib, y in zip(niv[5:], (388, 338, 304)):
        A(texte(574, y, lib, "mono", 10, 500, "pivot", ancre="end",
                tracking=10 * 0.14))
    A(texte((P_QX0 + P_QX1) / 2, 394, q["tag_quai"], "mono", 10, 500,
            "pivot", ancre="middle", tracking=10 * 0.14))
    A(texte((P_SX0 + P_SX1) / 2, 278, q["tag_saint_nicolas"], "mono", 10, 500,
            "pivot", ancre="middle", tracking=10 * 0.14))

    # ── La colonne d'appels de gauche — la mission ───────────────────────────
    appels_g = [
        ("redescend", 440, (P_X_ARROW, 530)),
        ("chambres", 520, (bx, 522)),
        ("services", 596, (bx, 604)),
    ]
    for cle, base, cible in appels_g:
        e = elems[cle]
        appel(A, MARGE, base, e["libelle"], e["detail"], P_CALL_L, cible,
              controler, cle)

    # ── La colonne d'appels de droite — le système ───────────────────────────
    appels_d = [
        ("systeme", 320, (P_X_RISER + 2, 314)),
        ("derogations", 412, (676, 392)),
        ("detection", 500, (P_X_DOT_S + 4.5, 487)),
        ("zone", 588, (P_SX1 + P_ENV + 2, 560)),
    ]
    for cle, base, cible in appels_d:
        e = elems[cle]
        controler(f"appel {cle} — libellé", e["libelle"], 15, "sans-400",
                  W - MARGE - P_CALL_XD)
        A(texte(P_CALL_XD, base, e["libelle"], "sans", 15, 400, "encre",
                wdth=100))
        for k, l in enumerate(e["detail"]):
            controler(f"appel {cle} — détail {k + 1}", l, 10, "mono",
                      W - MARGE - P_CALL_XD, 10 * 0.14)
            A(texte(P_CALL_XD, base + 18 + k * 14, l, "mono", 10, 500,
                    "pivot", tracking=10 * 0.14))
        A(polyligne([(P_CALL_XD - 8, base - 4), cible], "filet-1", 1))

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
        "demonstration": "deux bandes de travaux calcaire cernées d’un L encré "
                         f"({w_rdc:.0f} et {w_r1:.0f} px, proportionnelles aux "
                         "140 et 90 m² de la fiche) tiennent dans le coin "
                         "bas-gauche de la coupe ; l’enceinte claire de la "
                         "zone d’alarme enclot les deux piles entières "
                         f"(x {P_QX0 - P_ENV}–{P_SX1 + P_ENV}, "
                         f"y {P_Y_COMBLES - P_ENV}–{P_Y_FOND + P_ENV}) et "
                         "13 points de détection occupent chaque niveau, "
                         "sous-sol et combles compris — texte masqué, la "
                         "disproportion des deux périmètres porte la thèse",
        "topologie": f"appels mission (x {MARGE}–{MARGE + P_CALL_L}) → piles "
                     f"(quai x {P_QX0}–{P_QX1} sur 5 niveaux, Saint-Nicolas "
                     f"x {P_SX0}–{P_SX1} sur 7 + combles, mitoyenneté "
                     f"pointillée à {P_SX0}) → appels système "
                     f"(x {P_CALL_XD}–{W - MARGE}) ; colonne montante à "
                     f"{P_X_RISER}, centrale 566–588 au RDC",
        "emprises": f"largeur = surface x {P_K_M2} px/m² : RDC 140 m² → "
                    f"{w_rdc:.0f} px, R+1 90 m² → {w_r1:.0f} px — aucune "
                    "autre proportion d’ouvrage n’est reprise",
        "bas_du_dessin": f"fond du sous-sol à {P_Y_FOND}, enceinte jusqu’à "
                         f"{P_Y_FOND + P_ENV + 2}, dernier appel à 634, "
                         f"phrase de principe à {Y_PHRASE}, cartouche "
                         f"{Y_CARTOUCHE}–{Y_CARTOUCHE + H_CARTOUCHE}, marge "
                         f"basse {H - (Y_CARTOUCHE + H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur * H_CARTOUCHE} px², soit "
                            f"{largeur * H_CARTOUCHE / (W * H) * 100:.2f} % "
                            f"de la planche",
        "chiffre_unique": "aucun chiffre de relevé — la démonstration n’est "
                          "pas chiffrée (révision 4) ; les surfaces restent "
                          "au mono 10 pivot, dans les appels",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l’échelle "
                         f"0,96 (1152 / {W})",
        "phrase_principe": f"{len(donnees['phrase_principe'])} signes — "
                           f"{l_phrase:.0f} px mesurés pour {UTILE} disponibles",
        "depassements": depassements if depassements
                        else "aucun — toutes les lignes mesurées sous leur colonne",
    }
    return "\n".join(out) + "\n", controles


def composer_vignette_portee(donnees):
    """La vignette : le motif de l'archétype, sans son appareil.

    Ce qu'elle garde : les deux piles inégales, les deux bandes de travaux
    cernées de leur L, l'enceinte claire qui enclot tout, la colonne montante
    et ses points de détection, et les deux nœuds chiffrés (230 m² contre
    sept niveaux). Ce qu'elle laisse : la centrale, les répétiteurs,
    l'escalier, les niveaux nommés, la légende — huit signes annotés dans
    300 px ne se liraient pas."""
    q = donnees["portee"]
    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false" '
      f'style="width:100%;height:auto;display:block">')
    entete_style(A)
    A(rect(0, 0, VW, VH, "papier"))
    A(texte(V_MARGE, 22, donnees["vignette_surtitre"], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    # Les deux piles — même grille de niveaux, repère propre.
    qx0, qx1, sx1 = 36, 104, 172
    y_fond, y_toit_q, y_toit_s, y_combles = 172, 102, 74, 66
    A(rect(38, 130.5, 23, 13.5, "calcaire"))
    A(rect(38, 144.5, 36, 13, "calcaire"))
    for y in (116, 130, 144, 158):
        A(ligne(qx0 + 1, y, qx1 - 1, y, "filet-2", 0.8))
    for y in (74, 88, 102, 116, 130, 144, 158):
        A(ligne(qx0 + 69, y, sx1 - 1, y, "filet-2", 0.8))
    A(polyligne([(qx0, y_fond), (qx0, y_toit_q), (qx1, y_toit_q)], "encre", 1.5))
    A(polyligne([(qx1, y_toit_q), (qx1, y_combles), (sx1, y_combles),
                 (sx1, y_fond)], "encre", 1.5))
    A(ligne(qx0, y_fond, sx1, y_fond, "encre", 1.5))
    _pointille(A, qx1, y_toit_q, qx1, y_fond, 0.8, "3 3")

    # Le L de la mission.
    A(polyligne([(38, 130.5), (61, 130.5), (61, 144.5), (74, 144.5),
                 (74, 157.5), (38, 157.5), (38, 130.5)], "encre", 1.2))

    # L'enceinte de la zone d'alarme.
    env = [(31, 177), (31, 97), (99, 97), (99, 61), (177, 61), (177, 177)]
    A(polyligne(env + [env[0]], "clair", 3))

    # La colonne montante et les points de détection.
    A(ligne(108, 70, 108, 165, "encre", 1))
    for y in (165, 151, 137, 123, 109):
        A(cercle(70, y, 2, "clair", "encre", 0.8))
    for y in (165, 151, 137, 123, 109, 95, 81, 70):
        A(cercle(138, y, 2, "clair", "encre", 0.8))

    # Les deux nœuds chiffrés.
    A(texte(192, 62, "Coordination SSI", "sans", 12, 600, "encre", wdth=112))
    A(texte(192, 76, "SEPT NIVEAUX", "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    A(polyligne([(189, 58), (179, 62)], "filet-1", 1))
    A(texte(192, 130, "Lots techniques", "sans", 12, 600, "encre", wdth=112))
    A(texte(192, 144, f"230{NN}m²", "mono", 10, 500, "pivot", tabulaire=True))
    A(polyligne([(189, 126), (76, 146)], "filet-1", 1))

    A("</svg>")
    controles = {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": f"carte de projet mesurée de 274 à 296 px — "
                            f"échelle {274/VW:.2f} à {296/VW:.2f}",
        "corps_minimal": f"9 px dans le repère — rendu à {9*274/VW:.1f} px au pire cas",
        "motif": "deux piles inégales, le L de la mission au coin bas-gauche, "
                 "l’enceinte claire qui enclot tout, la colonne montante et "
                 "13 points de détection, deux nœuds chiffrés — centrale, "
                 "répétiteurs, escalier et niveaux nommés sont laissés à la "
                 "planche",
        "bas_du_dessin": "enceinte jusqu’à 178,5 px, marge basse 21,5 px",
    }
    return "\n".join(out) + "\n", controles


def composer_appui_portee(donnees):
    """L'appui du hero : le motif à l'échelle 1.

    Ce qu'il garde : les deux piles, les bandes de travaux et leur L, la
    flèche de la salle qui redescend, la centrale, la colonne montante et ses
    points, l'enceinte de la zone d'alarme, et trois nœuds chiffrés
    (lots techniques, coordination SSI, établissement). Ce qu'il laisse :
    les répétiteurs, l'escalier, la légende, les niveaux nommés."""
    q = donnees["portee"]
    elems = {e["cle"]: e for e in q["elements"]}
    out = []
    A = out.append
    racine_appui(A, donnees)

    qx0, qx1, sx1 = 96, 236, 376
    y_fond, y_toit_q, y_combles = 332, 182, 108
    w_rdc, w_r1 = 77, 50

    A(rect(100, 244, w_r1, 28, "calcaire"))
    A(rect(100, 274, w_rdc, 26, "calcaire"))
    for y in (212, 242, 272, 302):
        A(ligne(qx0 + 1, y, qx1 - 1, y, "filet-2", 1))
    for y in (122, 152, 182, 212, 242, 272, 302):
        A(ligne(qx0 + 141, y, sx1 - 1, y, "filet-2", 1))
    A(polyligne([(qx0, y_fond), (qx0, y_toit_q), (qx1, y_toit_q)], "encre", 2))
    A(polyligne([(qx1, y_toit_q), (qx1, y_combles), (sx1, y_combles),
                 (sx1, y_fond)], "encre", 2))
    A(ligne(qx0, y_fond, sx1, y_fond, "encre", 2))
    _pointille(A, qx1, y_toit_q, qx1, y_fond, 1, "5 5")

    # Le L de la mission, et la salle qui redescend.
    A(polyligne([(100, 244), (150, 244), (150, 274), (177, 274), (177, 300),
                 (100, 300), (100, 244)], "encre", 1.5))
    A(ligne(118, 252, 118, 288, "encre", 1.2))
    A(fleche(118, 295, "encre", "bas", 8))

    # L'enceinte de la zone d'alarme.
    env = [(90, 338), (90, 176), (230, 176), (230, 102), (382, 102),
           (382, 338)]
    A(polyligne(env + [env[0]], "clair", 4))

    # La centrale, la colonne montante, les points de détection.
    _boitier(A, 206, 278, 18, 1.5)
    A(ligne(224, 287, 242, 287, "encre", 1))
    A(ligne(242, 115, 242, 317, "encre", 1.2))
    for y in (317, 287, 257, 227, 197):
        A(cercle(190, y, 3, "clair", "encre", 1))
    for y in (317, 287, 257, 227, 197, 167, 137, 115):
        A(cercle(306, y, 3, "clair", "encre", 1))

    # Les trois nœuds chiffrés, à droite.
    A(texte(400, 140, "Coordination SSI", "sans", 14, 600, "encre", wdth=112))
    A(texte(400, 157, "SEPT NIVEAUX", "mono", 11, 500, "pivot",
            tracking=11 * 0.14))
    A(polyligne([(397, 136), (386, 132)], "filet-1", 1))
    A(texte(400, 220, "Lots techniques", "sans", 14, 600, "encre", wdth=112))
    A(texte(400, 237, f"230{NN}m²", "mono", 11, 500, "pivot", tabulaire=True))
    A(polyligne([(397, 216), (179, 274)], "filet-1", 1))
    A(texte(400, 300, "L’établissement", "sans", 14, 600, "encre", wdth=112))
    A(texte(400, 317, f'{elems["etablissement"]["valeur"]} CHAMBRES', "mono",
            11, 500, "pivot", tracking=11 * 0.14))
    A(polyligne([(397, 296), (384, 298)], "filet-1", 1))

    A("</svg>")
    return "\n".join(out) + "\n", controles_appui(
        motif="les deux piles inégales, le L de la mission et sa flèche, "
              "l’enceinte claire de la zone d’alarme, la centrale, la "
              "colonne montante et 13 points de détection, trois nœuds "
              "chiffrés à l’échelle 1 — répétiteurs, escalier, légende et "
              "niveaux nommés laissés à la planche",
        bas=f"enceinte jusqu’à 340 px, marge basse {AH - 340} px")


# ── Mécanisme `restitution` — l'air pris hors marché, rendu au marché ────────
#
# La thèse : l'aspiration des machines est un ouvrage du procédé, hors des
# marchés du bureau ; elle prend à l'atelier son air, et le rendre EST au
# marché. La coupe suit l'air — il entre en haut par la gaine perforée,
# descend, est capté au ras des postes, franchit la limite des marchés et
# quitte le dessin — tandis que la chaleur de confort descend du même plafond
# SANS CONDUIT et ne quitte rien. Les trois départs de la chaufferie sont
# tracés à l'échelle de leurs diamètres nominaux : le plus gros ne chauffe
# personne.
#
# ⚠ Toutes les mesures de ce bloc sont ABSOLUES et propres au format planche.
# La vignette et l'appui ont les leurs (préfixes RSV_ et RSA_) : les trois
# formats partagent l'implantation des primitives, jamais les coordonnées.

RS_Y_LEGENDE = 216            # légende des traits, et en-tête du hors-marché
RS_Y_LIMITE_LIB = 240         # la mention qui nomme le trait de limite

RS_HALLE0, RS_HALLE1 = 240, 880       # emprise de la halle (gabarit de principe)
RS_Y_PLAFOND = 252
RS_Y_SOL = 640

RS_X_LIMITE = 940             # le trait de limite des marchés
RS_Y_LIM0, RS_Y_LIM1 = 244, 660

RS_CH0, RS_CH1 = 56, 212      # la chaufferie, hors halle, à gauche
RS_CH_Y0, RS_CH_Y1 = 330, 470
RS_N_CHAUD = 4                # module de quatre chaudières (CCTP § 4.1.2)

RS_K_DN = 0.16                # px par unité de diamètre nominal — DN 80 → 12,8 px
RS_Y_D80, RS_Y_D50, RS_Y_D33 = 356, 400, 444  # sorties de la chaufferie
RS_X_MONTEE = 220             # colonne de la montée du DN 80
RS_X_DESCENTE = 236           # colonne du DN 50 vers son collecteur
RS_X_D33 = 228                # le DN 33 descend DANS LE COULOIR, hors des
                              # colonnes de texte — il traversait « 4 × 145 kW »

RS_CTA = (250, 262, 150, 54)  # centrale de compensation : x, y, largeur, hauteur
RS_X_TXT_CTA = 416            # ses libellés, à droite du caisson

RS_Y_GAINE = 336              # gaine circulaire perforée
RS_H_GAINE = 14
RS_X_GAINE1 = 860
RS_AIR_X = (465, 635, 820)    # les descentes d'air, DANS LES INTERVALLES
                              # entre les panneaux : les deux vecteurs se
                              # partagent le plafond sans se confondre
RS_AIR_Y0, RS_AIR_Y1 = 356, 384

RS_Y_COLL50 = 408             # collecteur des panneaux rayonnants
RS_X_COLL50 = 840
RS_PAN_X = (320, 490, 660)    # trois panneaux rayonnants
RS_PAN_W, RS_PAN_H = 120, 10
RS_Y_PAN = 416
RS_RAY_Y0, RS_RAY_Y1 = 432, 456        # le rayonnement : des flèches, aucun conduit

RS_Y_DET_PAN = 480            # détails des panneaux, deux lignes
RS_Y_MENTIONS = 508           # captation (gauche) · destin de l'air (droite)

RS_Y_COLL_ASP = 518           # collecteur de l'air capté
RS_H_COLL_ASP = 12
RS_POSTE_X = (320, 490, 660)
RS_POSTE_W = 120
RS_Y_POSTE0, RS_Y_POSTE1 = 566, 626
RS_Y_CAPT0, RS_Y_CAPT1 = 536, 562      # la captation, entre poste et collecteur

RS_Y_LIB_POSTES = 660         # sous le sol

RS_ASP = (960, 462, 184, 118) # le bloc hors marché : x, y, largeur, hauteur
RS_Y_ASP_MENTION = 602

RS_Y_D33_BAS = 570            # le départ des services, qui quitte le dessin
RS_X_D33_FIN = 70


def _rs_epaisseur(dn):
    """Épaisseur d'un départ, à l'échelle de son diamètre nominal."""
    return dn * RS_K_DN


def _rs_perfore(A, x0, x1, y, h):
    """La gaine perforée : un conduit plein, ponctué de ses perforations.

    ⚠ Ordre des arguments : x0, x1, PUIS y. Un appel positionnel les a
    intervertis une fois — la gaine se traçait alors à y 860, hors du repère
    de 800, et rien ne le signalait : l’assertion de dépassement mesure des
    LARGEURS, jamais une occupation. Seul le PNG l’a montré.
    """
    A(rect(x0, y, x1 - x0, h, "clair"))
    A(ligne(x0, y, x1, y, "encre", 1.5))
    A(ligne(x0, y + h, x1, y + h, "encre", 1.5))
    n = int((x1 - x0) // 24)
    for i in range(1, n):
        cx = x0 + i * 24
        A(ligne(cx, y + h - 3, cx, y + h, "encre", 1))


def _rs_rayon(A, cx, y0, y1):
    """Le rayonnement : trois traits divergents, sans conduit ni gaine."""
    for dx in (-9, 0, 9):
        A(ligne(cx, y0, cx + dx * 1.6, y1, "encre", 1))
        A(fleche(cx + dx * 1.6, y1 + 4, "encre", "bas", 6))


def _rs_replier_mono(chaine, corps, dispo, tracking_em=0.14):
    """Replie une ligne mono EN MESURANT SON INTERLETTRAGE.

    ⚠ `replier` du tronc mesure sans tracking : sur du mono à 0,14 em, il
    laisse passer près d’un quart de largeur en trop, et l’assertion de
    dépassement rompt ensuite. Un facteur correctif approché ne suffit pas non
    plus — il a laissé passer une ligne à 243 px pour 226 disponibles, à un
    demi-pixel près du seuil. On replie donc en mesurant chaque essai avec son
    tracking réel. Le tronc n’est pas touché : l’invariant octet des planches
    publiées en dépend.
    """
    tr = corps * tracking_em
    if mesurer(chaine, corps, "mono", tr) <= dispo:
        return [chaine]
    lignes, courante = [], ""
    for mot in chaine.split(" "):
        essai = f"{courante} {mot}".strip()
        if courante and mesurer(essai, corps, "mono", tr) > dispo:
            lignes.append(courante)
            courante = mot
        else:
            courante = essai
    if courante:
        lignes.append(courante)
    return lignes


def _rs_captation(A, x0, x1, y0, y1):
    """La captation : une hotte tronconique au ras du poste."""
    A(polyligne([(x0, y1), (x0 + 26, y0), (x1 - 26, y0), (x1, y1)],
                "encre", 1.5))


def composer_restitution(donnees):
    q = donnees["restitution"]
    dep = {e["cle"]: e for e in q["departs"]}
    prod, hors, postes = q["production"], q["hors_marche"], q["postes"]
    out = []
    A = out.append
    depassements = []

    def controler(nom, chaine, corps, profil, dispo, tracking=0.0):
        largeur = mesurer(chaine, corps, profil, tracking)
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

    # ── En-têtes : le périmètre du dessin, et celui qui lui échappe ──────────
    controler("en-tête schéma", q["entete"], 10, "mono", UTILE, 10 * 0.14)
    A(texte(MARGE, Y_ENTETE, q["entete"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

    # ⚠ La borne de la légende n'est PAS une abscisse de colonne : c'est le
    # bord gauche MESURÉ de l'en-tête droit, qui est ancré à la marge droite
    # (piège N23 — une borne se calcule, elle ne se lit pas sur une constante).
    l_entete_d = mesurer(q["entete_droite"], 10, "mono", 10 * 0.14)
    x_entete_d = W - MARGE - l_entete_d
    controler("légende des traits", q["legende_traits"], 10, "mono",
              x_entete_d - MARGE - 24, 10 * 0.14)
    A(texte(MARGE, RS_Y_LEGENDE, q["legende_traits"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    A(texte(W - MARGE, RS_Y_LEGENDE, q["entete_droite"], "mono", 10, 500,
            "pivot", ancre="end", tracking=10 * 0.14))
    controler("mention de limite", q["limite"], 10, "mono",
              RS_X_LIMITE - 10 - MARGE, 10 * 0.14)
    A(texte(RS_X_LIMITE - 10, RS_Y_LIMITE_LIB, q["limite"], "mono", 10, 500,
            "pivot", ancre="end", tracking=10 * 0.14))

    e80 = _rs_epaisseur(dep["compensation"]["dn"])
    e50 = _rs_epaisseur(dep["rayonnant"]["dn"])
    e33 = _rs_epaisseur(dep["services"]["dn"])

    # ── La halle : un gabarit de principe, percé par ce qui entre et sort ────
    cx, cy, cw, ch = RS_CTA
    # plafond
    A(ligne(RS_HALLE0, RS_Y_PLAFOND, RS_HALLE1, RS_Y_PLAFOND, "encre", 2))
    # sol
    A(ligne(RS_HALLE0, RS_Y_SOL, RS_X_LIMITE, RS_Y_SOL, "encre", 2))
    # mur gauche, interrompu aux deux traversées d'eau
    for a, b in ((RS_Y_PLAFOND, cy + ch / 2 - e80 / 2 - 3),
                 (cy + ch / 2 + e80 / 2 + 3, RS_Y_COLL50 - e50 / 2 - 3),
                 (RS_Y_COLL50 + e50 / 2 + 3, RS_Y_SOL)):
        if b > a:
            A(ligne(RS_HALLE0, a, RS_HALLE0, b, "encre", 2))
    # mur droit, interrompu au collecteur de l'air capté
    for a, b in ((RS_Y_PLAFOND, RS_Y_COLL_ASP - 3),
                 (RS_Y_COLL_ASP + RS_H_COLL_ASP + 3, RS_Y_SOL)):
        A(ligne(RS_HALLE1, a, RS_HALLE1, b, "encre", 2))
    A(texte(RS_HALLE0 + 12, RS_Y_PLAFOND - 8, q["halle"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))

    # ── La chaufferie, hors de la halle ─────────────────────────────────────
    lib_ch = replier(prod["libelle"], 15, RS_CH1 - RS_CH0, "sans-600")
    for k, l in enumerate(lib_ch):
        controler(f"libellé chaufferie {k + 1}", l, 15, "sans-600",
                  RS_CH1 - RS_CH0)
        A(texte(RS_CH0, RS_CH_Y0 - 14 - (len(lib_ch) - 1 - k) * 18, l,
                "sans", 15, 600, "encre", wdth=112))
    A(rect_bord(RS_CH0, RS_CH_Y0, RS_CH1 - RS_CH0, RS_CH_Y1 - RS_CH_Y0,
                "papier", "filet-1"))
    # les quatre chaudières, en cascade : la répétition du module EST le signe
    h_mod = (RS_CH_Y1 - RS_CH_Y0 - 20) / RS_N_CHAUD
    for i in range(RS_N_CHAUD):
        A(rect(RS_CH0 + 14, RS_CH_Y0 + 10 + i * h_mod + 3,
               56, h_mod - 8, "calcaire"))
        A(rect_bord(RS_CH0 + 14, RS_CH_Y0 + 10 + i * h_mod + 3,
                    56, h_mod - 8, "calcaire", "filet-1"))
    # la bouteille de découplage : la colonne verticale que tous les départs voient
    A(rect(RS_CH0 + 92, RS_CH_Y0 + 13, 12, RS_CH_Y1 - RS_CH_Y0 - 26, "clair"))
    A(rect_bord(RS_CH0 + 92, RS_CH_Y0 + 13, 12, RS_CH_Y1 - RS_CH_Y0 - 26,
                "clair", "encre"))
    for i in range(RS_N_CHAUD):
        yy = RS_CH_Y0 + 10 + i * h_mod + h_mod / 2 - 1
        A(ligne(RS_CH0 + 70, yy, RS_CH0 + 92, yy, "encre", 1.5))
    valeur_ch = f'{prod["valeur"]}{NN}{prod["unite"]}'
    controler("valeur chaufferie", valeur_ch, 10, "mono", 180, 10 * 0.14)
    A(texte(RS_CH0, RS_CH_Y1 + 20, valeur_ch, "mono", 10, 500, "pivot",
            tracking=10 * 0.14, tabulaire=True))
    dispo_ch = RS_X_D33 - RS_CH0 - 12
    lignes_ch = []
    for l in prod["detail"]:
        lignes_ch += _rs_replier_mono(l, 10, dispo_ch)
    for k, l in enumerate(lignes_ch):
        controler(f"détail chaufferie {k + 1}", l, 10, "mono", dispo_ch,
                  10 * 0.14)
        A(texte(RS_CH0, RS_CH_Y1 + 36 + k * 14, l, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))

    # ── Les trois départs, tracés à l'échelle de leur diamètre nominal ───────
    # DN 80 — vers la centrale de compensation
    y_cta = cy + ch / 2
    A(polyligne([(RS_CH1, RS_Y_D80), (RS_X_MONTEE, RS_Y_D80),
                 (RS_X_MONTEE, y_cta), (cx, y_cta)], "encre", e80))
    # DN 50 — vers le collecteur des panneaux
    A(polyligne([(RS_CH1, RS_Y_D50), (RS_X_DESCENTE, RS_Y_D50),
                 (RS_X_DESCENTE, RS_Y_COLL50), (RS_X_COLL50, RS_Y_COLL50)],
                "encre", e50))
    # DN 33 — le plus fin, qui quitte le dessin par la gauche
    A(polyligne([(RS_CH1, RS_Y_D33), (RS_X_D33, RS_Y_D33),
                 (RS_X_D33, RS_Y_D33_BAS),
                 (RS_X_D33_FIN + 8, RS_Y_D33_BAS)], "encre", e33))
    A(fleche(RS_X_D33_FIN, RS_Y_D33_BAS, "encre", "gauche", 9))
    svc = dep["services"]
    lib_svc = replier(svc["libelle"], 15, 168, "sans-600")
    for k, l in enumerate(lib_svc):
        controler(f"libellé services {k + 1}", l, 15, "sans-600", 168)
        A(texte(RS_X_D33_FIN, RS_Y_D33_BAS + 24 + k * 18, l, "sans", 15, 600,
                "encre", wdth=112))
    y_svc = RS_Y_D33_BAS + 24 + len(lib_svc) * 18
    dispo_svc = RS_POSTE_X[0] - RS_X_D33_FIN - 24
    lignes_svc = []
    for l in [f'{svc["diametre"]} · {svc["valeur"]}{NN}{svc["unite"]}',
              svc["destin"]] + svc["detail"]:
        lignes_svc += _rs_replier_mono(l, 10, dispo_svc)
    for k, l in enumerate(lignes_svc):
        controler(f"détail services {k + 1}", l, 10, "mono", dispo_svc,
                  10 * 0.14)
        A(texte(RS_X_D33_FIN, y_svc + k * 14, l, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))

    # ── La compensation : la centrale, sa gaine, l'air qui descend ──────────
    cpn = dep["compensation"]
    A(rect_bord(cx, cy, cw, ch, "papier", "filet-1"))
    # la batterie : des ailettes, dans la veine
    for i in range(6):
        A(ligne(cx + 24 + i * 9, cy + 12, cx + 24 + i * 9, cy + ch - 12,
                "encre", 1.5))
    lib_cta = replier(cpn["libelle"], 15, W - MARGE - RS_X_TXT_CTA, "sans-600")
    for k, l in enumerate(lib_cta):
        controler(f"libellé centrale {k + 1}", l, 15, "sans-600",
                  W - MARGE - RS_X_TXT_CTA)
        A(texte(RS_X_TXT_CTA, cy + 12 + k * 18, l, "sans", 15, 600, "encre",
                wdth=112))
    y_cta_det = cy + 12 + len(lib_cta) * 18
    for k, l in enumerate([cpn["diametre"]] + cpn["detail"]):
        controler(f"détail centrale {k + 1}", l, 10, "mono",
                  W - MARGE - RS_X_TXT_CTA, 10 * 0.14)
        A(texte(RS_X_TXT_CTA, y_cta_det + k * 14, l, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))
    # la gaine perforée, et l'air qui en descend
    A(ligne(cx + cw / 2, cy + ch, cx + cw / 2, RS_Y_GAINE, "encre", 8))
    _rs_perfore(A, cx + cw / 2 - 8, RS_X_GAINE1, RS_Y_GAINE, RS_H_GAINE)
    cote_air = f'{cpn["valeur"]}{NN}{cpn["unite"]}'
    controler("cote de la gaine", cote_air, 10, "mono", 200, 10 * 0.14)
    A(texte(RS_X_GAINE1, RS_Y_GAINE - 8, cote_air, "mono", 10, 500, "pivot",
            ancre="end", tracking=10 * 0.14, tabulaire=True))
    for x in RS_AIR_X:
        A(ligne(x, RS_AIR_Y0, x, RS_AIR_Y1, "encre", 1.5))
        A(fleche(x, RS_AIR_Y1 + 4, "encre", "bas", 9))

    # ── Le rayonnement : les panneaux, et des flèches sans conduit ───────────
    ray = dep["rayonnant"]
    controler("libellé panneaux", ray["libelle"], 15, "sans-600",
              RS_X_COLL50 - RS_PAN_X[0] - 120)
    A(texte(RS_PAN_X[0], RS_Y_COLL50 - 12, ray["libelle"], "sans", 15, 600,
            "encre", wdth=112))
    cote_ray = f'{ray["diametre"]} · {ray["valeur"]}{NN}{ray["unite"]}'
    controler("cote des panneaux", cote_ray, 10, "mono", 200, 10 * 0.14)
    A(texte(RS_X_COLL50, RS_Y_COLL50 - 12, cote_ray, "mono", 10, 500, "pivot",
            ancre="end", tracking=10 * 0.14, tabulaire=True))
    for x in RS_PAN_X:
        A(ligne(x + RS_PAN_W / 2, RS_Y_COLL50, x + RS_PAN_W / 2, RS_Y_PAN,
                "encre", 2))
        A(rect(x, RS_Y_PAN, RS_PAN_W, RS_PAN_H, "clair"))
        A(rect_bord(x, RS_Y_PAN, RS_PAN_W, RS_PAN_H, "clair", "encre"))
        for c in (x + 26, x + RS_PAN_W / 2, x + RS_PAN_W - 26):
            _rs_rayon(A, c, RS_RAY_Y0, RS_RAY_Y1)
    l_lib_ray = mesurer(ray["libelle"], 15, "sans-600")
    l_cote_ray = mesurer(cote_ray, 10, "mono", 10 * 0.14)
    x_haut = RS_PAN_X[0] + l_lib_ray + 20
    controler("détail panneaux 2 (en ligne)", ray["detail"][1], 10, "mono",
              (RS_X_COLL50 - l_cote_ray - 20) - x_haut, 10 * 0.14)
    A(texte(x_haut, RS_Y_COLL50 - 12, ray["detail"][1], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    controler("détail panneaux 1", ray["detail"][0], 10, "mono", 420,
              10 * 0.14)
    A(texte(RS_PAN_X[0], RS_Y_DET_PAN, ray["detail"][0], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    controler("destin du rayonnement", ray["destin"], 10, "mono", 300,
              10 * 0.14)
    A(texte(RS_X_GAINE1, RS_Y_DET_PAN, ray["destin"], "mono", 10, 500,
            "pivot", ancre="end", tracking=10 * 0.14))

    # ── Les postes, leurs captations, et l'air qui s'en va ───────────────────
    # ⚠ Les deux mentions de cette ligne se partagent la largeur : la borne de
    # la gauche est le bord gauche MESURÉ de la droite, jamais une constante.
    l_destin = mesurer(cpn["destin"], 10, "mono", 10 * 0.14)
    x_destin = RS_X_GAINE1 - l_destin
    controler("mention de captation", postes["captation"], 10, "mono",
              x_destin - RS_POSTE_X[0] - 24, 10 * 0.14)
    A(texte(RS_POSTE_X[0], RS_Y_MENTIONS, postes["captation"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    A(texte(RS_X_GAINE1, RS_Y_MENTIONS, cpn["destin"], "mono", 10, 500,
            "pivot", ancre="end", tracking=10 * 0.14))

    A(rect(RS_POSTE_X[0], RS_Y_COLL_ASP, RS_X_LIMITE - RS_POSTE_X[0],
           RS_H_COLL_ASP, "clair"))
    A(rect_bord(RS_POSTE_X[0], RS_Y_COLL_ASP, RS_X_LIMITE - RS_POSTE_X[0],
                RS_H_COLL_ASP, "clair", "encre"))
    for x in RS_POSTE_X:
        A(rect_bord(x, RS_Y_POSTE0, RS_POSTE_W, RS_Y_POSTE1 - RS_Y_POSTE0,
                    "calcaire", "filet-1"))
        _rs_captation(A, x + 16, x + RS_POSTE_W - 16, RS_Y_CAPT0, RS_Y_CAPT1)
        A(ligne(x + RS_POSTE_W / 2, RS_Y_COLL_ASP + RS_H_COLL_ASP,
                x + RS_POSTE_W / 2, RS_Y_CAPT0, "encre", 5))
        A(fleche(x + RS_POSTE_W / 2, RS_Y_COLL_ASP + RS_H_COLL_ASP - 2,
                 "encre", "haut", 9))
    controler("libellé postes", postes["libelle"], 15, "sans-600", 560)
    A(texte(RS_POSTE_X[0], RS_Y_LIB_POSTES, postes["libelle"], "sans", 15, 600,
            "encre", wdth=112))

    # ── La limite des marchés, et ce qui est au-delà ─────────────────────────
    A(ligne(RS_X_LIMITE, RS_Y_LIM0, RS_X_LIMITE, RS_Y_LIM1, "encre", 2))
    ax, ay, aw, ah = RS_ASP
    A(fleche(ax - 2, RS_Y_COLL_ASP + RS_H_COLL_ASP / 2, "encre", "droite", 10))
    A(rect_bord(ax, ay, aw, ah, "papier", "filet-1"))
    lib_asp = replier(hors["libelle"], 15, aw - 24, "sans-600")
    for k, l in enumerate(lib_asp):
        controler(f"libellé aspiration {k + 1}", l, 15, "sans-600", aw - 24)
        A(texte(ax + 12, ay + 24 + k * 18, l, "sans", 15, 600, "encre",
                wdth=112))
    y_asp = ay + 24 + len(lib_asp) * 18 + 4
    for k, l in enumerate([f'{hors["valeur"]}{NN}{hors["unite"]}']
                          + hors["detail"]):
        controler(f"détail aspiration {k + 1}", l, 10, "mono", aw - 24,
                  10 * 0.14)
        A(texte(ax + 12, y_asp + k * 14, l, "mono", 10, 500, "pivot",
                tracking=10 * 0.14, tabulaire=(k == 0)))
    for k, l in enumerate(_rs_replier_mono(hors["mention"], 10, W - MARGE - ax)):
        controler(f"mention aspiration {k + 1}", l, 10, "mono",
                  W - MARGE - ax, 10 * 0.14)
        A(texte(ax, RS_Y_ASP_MENTION + k * 14, l, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))

    # ── Phrase de principe, pleine largeur utile ─────────────────────────────
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
        "demonstration": "l’air fait une traversée complète et ne revient pas : "
                         f"il entre par la gaine perforée (y {RS_Y_GAINE}), "
                         f"descend en {len(RS_AIR_X)} filets, est capté au ras "
                         f"des {len(RS_POSTE_X)} postes (y {RS_Y_CAPT0}), "
                         f"remonte au collecteur (y {RS_Y_COLL_ASP}) et "
                         f"franchit la limite (x {RS_X_LIMITE}) ; le "
                         "rayonnement, lui, descend des panneaux SANS AUCUN "
                         "conduit et ne quitte pas le volume — texte masqué, "
                         "un seul des deux vecteurs sort du cadre",
        "echelle_des_departs": f"épaisseur = DN x {RS_K_DN} : "
                               f"DN 80 → {e80:.1f} px, DN 50 → {e50:.1f} px, "
                               f"DN 33 → {e33:.1f} px — rapport "
                               f"{e80/e33:.2f} entre le plus gros et le plus "
                               "fin ; les diamètres nominaux sont fermes (DPGF), "
                               "les débits d’eau du CCTP ne le sont pas et ne "
                               "sont pas dessinés",
        "topologie": f"chaufferie x {RS_CH0}–{RS_CH1} (hors halle) → trois "
                     f"départs → halle x {RS_HALLE0}–{RS_HALLE1} "
                     f"(plafond {RS_Y_PLAFOND}, sol {RS_Y_SOL}) → limite des "
                     f"marchés x {RS_X_LIMITE} → aspiration x {RS_ASP[0]}–"
                     f"{RS_ASP[0] + RS_ASP[2]}",
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur * H_CARTOUCHE} px², soit "
                            f"{largeur * H_CARTOUCHE / (W * H) * 100:.2f} % "
                            f"de la planche",
        "chiffre_unique": "aucun chiffre de relevé — la démonstration n’est pas "
                          "chiffrée (révision 4) ; les quatre valeurs restent "
                          "au mono 10 pivot, en cote de leur organe",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l’échelle "
                         f"0,96 (1152 / {W})",
        "bas_du_dessin": f"sol à {RS_Y_SOL}, libellé des postes à "
                         f"{RS_Y_LIB_POSTES}, phrase de principe à {Y_PHRASE}, "
                         f"cartouche {Y_CARTOUCHE}–{Y_CARTOUCHE + H_CARTOUCHE}, "
                         f"marge basse {H - (Y_CARTOUCHE + H_CARTOUCHE)} px",
        "phrase_principe": f"{len(donnees['phrase_principe'])} signes — "
                           f"{l_phrase:.0f} px mesurés pour {UTILE} disponibles",
        "bornes_calculees": "deux bornes sont MESURÉES et non lues sur une "
                            f"constante : la légende des traits s’arrête à "
                            f"{x_entete_d - MARGE - 24:.0f} px (bord gauche de "
                            f"l’en-tête droit, ancré à la marge), la mention de "
                            f"captation à {x_destin - RS_POSTE_X[0] - 24:.0f} px "
                            "(bord gauche du destin de l’air)",
        "depassements": depassements if depassements
                        else "aucun — toutes les lignes mesurées sous leur borne",
    }
    return "\n".join(out) + "\n", controles


# ── Vignette du mécanisme `restitution` — repère propre, mesures propres ─────
RSV_HALLE0, RSV_HALLE1 = 34, 232
RSV_Y_PLAF, RSV_Y_SOL = 62, 168
RSV_X_LIMITE = 250
RSV_Y_GAINE, RSV_H_GAINE = 82, 7
RSV_AIR_X = (52, 113, 175)    # dans les intervalles, jamais sur un panneau
RSV_Y_PAN = 112
RSV_PAN_X = (60, 122, 184)
RSV_PAN_W = 44
RSV_Y_COLL = 138
RSV_POSTE_Y = 150
RSV_CH = (16, 76, 14, 62)     # la chaufferie, réduite à son module répété


def composer_vignette_restitution(donnees):
    """La vignette : le motif, sans son appareil.

    Ce qu'elle garde : la halle, la gaine perforée et l'air qui descend, les
    trois panneaux et leur rayonnement sans conduit, le collecteur qui franchit
    la limite, et le nœud chiffré de la compensation. Ce qu'elle laisse : la
    chaufferie détaillée, les trois cotes de diamètre, les postes, les libellés
    d'organe et toutes les mentions — douze annotations dans 300 px ne se
    liraient pas.
    """
    q = donnees["restitution"]
    dep = {e["cle"]: e for e in q["departs"]}
    cpn = dep["compensation"]
    out = []
    A = out.append
    depassements = []

    def controler(nom, chaine, corps, profil, dispo, tracking=0.0):
        largeur = mesurer(chaine, corps, profil, tracking)
        if largeur > dispo:
            depassements.append(f"{nom} : {largeur:.0f} px pour {dispo:.0f} px")
        return largeur

    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false" '
      f'style="width:100%;height:auto;display:block">')
    entete_style(A)
    A(rect(0, 0, VW, VH, "papier"))
    controler("surtitre de vignette", donnees["vignette_surtitre"], 9, "mono",
              VW - 2 * V_MARGE, 9 * 0.14)
    A(texte(V_MARGE, 22, donnees["vignette_surtitre"], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    # la halle
    A(ligne(RSV_HALLE0, RSV_Y_PLAF, RSV_HALLE1, RSV_Y_PLAF, "encre", 1.5))
    A(ligne(RSV_HALLE0, RSV_Y_SOL, RSV_X_LIMITE, RSV_Y_SOL, "encre", 1.5))
    A(ligne(RSV_HALLE0, RSV_Y_PLAF, RSV_HALLE0, RSV_Y_SOL, "encre", 1.5))
    for a, b in ((RSV_Y_PLAF, RSV_Y_COLL - 2), (RSV_Y_COLL + 7, RSV_Y_SOL)):
        A(ligne(RSV_HALLE1, a, RSV_HALLE1, b, "encre", 1.5))

    # la chaufferie : quatre modules empilés, le signe de la cascade
    chx, chy, chw, chh = RSV_CH
    for i in range(4):
        A(rect_bord(chx, chy + i * (chh / 4) + 1, chw, chh / 4 - 2,
                    "calcaire", "filet-1"))
    A(polyligne([(chx + chw, chy + 8), (28, chy + 8), (28, RSV_Y_GAINE + 3),
                 (44, RSV_Y_GAINE + 3)], "encre", 4))
    A(polyligne([(chx + chw, chy + chh - 8), (30, chy + chh - 8),
                 (30, RSV_Y_PAN - 8), (RSV_PAN_X[0], RSV_Y_PAN - 8)],
                "encre", 2.5))

    # la gaine perforée, et l'air qui descend
    A(rect(44, RSV_Y_GAINE, RSV_HALLE1 - 56, RSV_H_GAINE, "clair"))
    A(rect_bord(44, RSV_Y_GAINE, RSV_HALLE1 - 56, RSV_H_GAINE, "clair", "encre"))
    for x in RSV_AIR_X:
        A(ligne(x, RSV_Y_GAINE + RSV_H_GAINE, x, RSV_Y_GAINE + 20, "encre", 1))
        A(fleche(x, RSV_Y_GAINE + 24, "encre", "bas", 6))

    # les panneaux : le rayonnement descend, sans conduit
    for x in RSV_PAN_X:
        A(ligne(x + RSV_PAN_W / 2, RSV_Y_PAN - 8, x + RSV_PAN_W / 2, RSV_Y_PAN,
                "encre", 1.5))
        A(rect(x, RSV_Y_PAN, RSV_PAN_W, 5, "clair"))
        A(rect_bord(x, RSV_Y_PAN, RSV_PAN_W, 5, "clair", "encre"))
        for c in (x + 10, x + RSV_PAN_W / 2, x + RSV_PAN_W - 10):
            for dx in (-4, 0, 4):
                A(ligne(c, RSV_Y_PAN + 5, c + dx, RSV_Y_PAN + 17, "encre", 0.8))

    # le collecteur de l'air capté, qui franchit la limite
    A(rect(60, RSV_Y_COLL, RSV_X_LIMITE - 60, 5, "clair"))
    A(rect_bord(60, RSV_Y_COLL, RSV_X_LIMITE - 60, 5, "clair", "encre"))
    for x in RSV_PAN_X:
        A(ligne(x + RSV_PAN_W / 2, RSV_POSTE_Y, x + RSV_PAN_W / 2,
                RSV_Y_COLL + 5, "encre", 2))
        A(rect_bord(x + 8, RSV_POSTE_Y, RSV_PAN_W - 16, 14, "calcaire",
                    "filet-1"))
    A(fleche(RSV_X_LIMITE + 12, RSV_Y_COLL + 2.5, "encre", "droite", 8))

    # la limite des marchés
    A(ligne(RSV_X_LIMITE, 56, RSV_X_LIMITE, RSV_Y_SOL + 6, "encre", 1.5))

    # le nœud chiffré : la compensation
    controler("nœud de vignette", cpn["libelle_vignette"], 12, "sans-600",
              VW - 2 * V_MARGE
              - mesurer(f'{cpn["valeur"]}{NN}{cpn["unite"]}', 10, "mono") - 16)
    A(texte(V_MARGE, 184, cpn["libelle_vignette"], "sans", 12, 600, "encre",
            wdth=112))
    A(texte(VW - V_MARGE, 184, f'{cpn["valeur"]}{NN}{cpn["unite"]}',
            "mono", 10, 500, "pivot", ancre="end", tabulaire=True))

    A("</svg>")
    controles = {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": f"carte de projet mesurée de 274 à 296 px — "
                            f"échelle {274/VW:.2f} à {296/VW:.2f}",
        "corps_minimal": f"9 px dans le repère — rendu à {9*274/VW:.1f} px au pire cas",
        "motif": "la halle, la gaine perforée et ses trois descentes d’air, "
                 "les trois panneaux dont le rayonnement descend sans conduit, "
                 "le collecteur qui franchit la limite, et le nœud chiffré de "
                 "la compensation ; chaufferie détaillée, cotes de diamètre, "
                 "libellés d’organe et mentions sont laissés à la planche",
        "elements_absents": "les trois cotes de diamètre nominal, les libellés "
                            "de la chaufferie, du bloc d’aspiration et des "
                            "postes, la mention de captation et le destin des "
                            "deux vecteurs — mesure de format, pas exception",
        "bas_du_dessin": "nœud chiffré à y 184, marge basse 16 px",
        "depassements": depassements if depassements
                        else "aucun — surtitre et nœud mesurés sous leur borne",
    }
    return "\n".join(out) + "\n", controles


# ── Appui du mécanisme `restitution` — 552 x 368, échelle 1,0 ────────────────
RSA_HALLE0, RSA_HALLE1 = 96, 424
RSA_Y_PLAF, RSA_Y_SOL = 96, 300
RSA_X_LIMITE = 452
RSA_Y_GAINE, RSA_H_GAINE = 128, 9
RSA_AIR_X = (126, 226, 326)   # dans les intervalles, jamais sur un panneau
RSA_Y_COLL50 = 178
RSA_PAN_X = (140, 240, 340)
RSA_PAN_W = 72
RSA_Y_PAN = 186
RSA_Y_COLL = 248
RSA_POSTE_Y = 266
RSA_CH = (32, 148, 40, 96)


def composer_appui_restitution(donnees):
    """L'appui : le motif entier, deux nœuds chiffrés, le surtitre court.

    Densité intermédiaire (protocole rév. 5) : la traversée complète et la
    limite des marchés, avec la compensation et l’aspiration chiffrées. Sont
    ABSENTS de ce format : les trois cotes de diamètre, les détails d’organe,
    les mentions de destin et le libellé des postes.
    """
    q = donnees["restitution"]
    dep = {e["cle"]: e for e in q["departs"]}
    cpn, hors = dep["compensation"], q["hors_marche"]
    out = []
    A = out.append
    depassements = []

    def controler(nom, chaine, corps, profil, dispo, tracking=0.0):
        largeur = mesurer(chaine, corps, profil, tracking)
        if largeur > dispo:
            depassements.append(f"{nom} : {largeur:.0f} px pour {dispo:.0f} px")
        return largeur

    controler("surtitre d’appui", donnees["vignette_surtitre"], 11, "mono",
              AW - 2 * A_MARGE, 11 * 0.14)
    racine_appui(A, donnees)

    # la halle
    A(ligne(RSA_HALLE0, RSA_Y_PLAF, RSA_HALLE1, RSA_Y_PLAF, "encre", 2))
    A(ligne(RSA_HALLE0, RSA_Y_SOL, RSA_X_LIMITE, RSA_Y_SOL, "encre", 2))
    A(ligne(RSA_HALLE0, RSA_Y_PLAF, RSA_HALLE0, RSA_Y_SOL, "encre", 2))
    for a, b in ((RSA_Y_PLAF, RSA_Y_COLL - 3), (RSA_Y_COLL + 9, RSA_Y_SOL)):
        A(ligne(RSA_HALLE1, a, RSA_HALLE1, b, "encre", 2))

    # la chaufferie et ses deux départs de calibres inégaux
    chx, chy, chw, chh = RSA_CH
    for i in range(4):
        A(rect_bord(chx, chy + i * (chh / 4) + 1.5, chw, chh / 4 - 3,
                    "calcaire", "filet-1"))
    A(polyligne([(chx + chw, chy + 12), (84, chy + 12), (84, RSA_Y_GAINE + 4),
                 (112, RSA_Y_GAINE + 4)], "encre", 8))
    A(polyligne([(chx + chw, chy + chh - 12), (88, chy + chh - 12),
                 (88, RSA_Y_COLL50), (RSA_PAN_X[-1] + RSA_PAN_W, RSA_Y_COLL50)],
                "encre", 5))

    # la gaine perforée et l'air qui descend
    A(rect(112, RSA_Y_GAINE, RSA_HALLE1 - 136, RSA_H_GAINE, "clair"))
    A(rect_bord(112, RSA_Y_GAINE, RSA_HALLE1 - 136, RSA_H_GAINE, "clair",
                "encre"))
    for x in RSA_AIR_X:
        A(ligne(x, RSA_Y_GAINE + RSA_H_GAINE, x, RSA_Y_GAINE + 26, "encre", 1.5))
        A(fleche(x, RSA_Y_GAINE + 31, "encre", "bas", 8))

    # les panneaux : le rayonnement, sans conduit
    for x in RSA_PAN_X:
        A(ligne(x + RSA_PAN_W / 2, RSA_Y_COLL50, x + RSA_PAN_W / 2, RSA_Y_PAN,
                "encre", 2))
        A(rect(x, RSA_Y_PAN, RSA_PAN_W, 7, "clair"))
        A(rect_bord(x, RSA_Y_PAN, RSA_PAN_W, 7, "clair", "encre"))
        for c in (x + 16, x + RSA_PAN_W / 2, x + RSA_PAN_W - 16):
            for dx in (-6, 0, 6):
                A(ligne(c, RSA_Y_PAN + 7, c + dx, RSA_Y_PAN + 24, "encre", 1))

    # le collecteur, les postes, la traversée de la limite
    A(rect(140, RSA_Y_COLL, RSA_X_LIMITE - 140, 9, "clair"))
    A(rect_bord(140, RSA_Y_COLL, RSA_X_LIMITE - 140, 9, "clair", "encre"))
    for x in RSA_PAN_X:
        A(ligne(x + RSA_PAN_W / 2, RSA_POSTE_Y, x + RSA_PAN_W / 2,
                RSA_Y_COLL + 9, "encre", 3))
        A(rect_bord(x + 12, RSA_POSTE_Y, RSA_PAN_W - 24, 22, "calcaire",
                    "filet-1"))
    A(ligne(RSA_X_LIMITE, 84, RSA_X_LIMITE, RSA_Y_SOL + 10, "encre", 2))
    A(fleche(RSA_X_LIMITE + 20, RSA_Y_COLL + 4.5, "encre", "droite", 9))

    # deux nœuds chiffrés : ce qui est rendu, ce qui prend
    # ⚠ Chaque nœud est borné par son VOISIN, jamais par la marge : à gauche
    # la valeur ancrée à AW/2+40, à droite celle ancrée à la marge droite.
    controler("nœud gauche d’appui", cpn["libelle_vignette"], 12, "sans-600",
              (AW / 2 + 40) - A_MARGE
              - mesurer(f'{cpn["valeur"]}{NN}{cpn["unite"]}', 10, "mono") - 16)
    controler("nœud droit d’appui", hors["libelle_vignette"], 12, "sans-600",
              (AW - A_MARGE) - (AW / 2 + 76)
              - mesurer(f'{hors["valeur"]}{NN}{hors["unite"]}', 10, "mono") - 16)
    A(texte(A_MARGE, 336, cpn["libelle_vignette"], "sans", 12, 600, "encre",
            wdth=112))
    A(texte(AW / 2 + 40, 336, f'{cpn["valeur"]}{NN}{cpn["unite"]}',
            "mono", 10, 500, "pivot", ancre="end", tabulaire=True))
    A(texte(AW / 2 + 76, 336, hors["libelle_vignette"], "sans", 12, 600,
            "encre", wdth=112))
    A(texte(AW - A_MARGE, 336, f'{hors["valeur"]}{NN}{hors["unite"]}',
            "mono", 10, 500, "pivot", ancre="end", tabulaire=True))

    A("</svg>")
    controles = controles_appui(
        "la halle, la gaine perforée et ses trois descentes d’air, les trois "
        "panneaux dont le rayonnement descend sans conduit, le collecteur qui "
        "franchit la limite des marchés, et deux nœuds chiffrés — ce que la "
        "compensation rend, ce que l’aspiration prend",
        "nœuds chiffrés à y 336, marge basse 32 px",
        elements_absents="les trois cotes de diamètre nominal, les détails "
                         "d’organe, les mentions de destin et le libellé des "
                         "postes — mesure de format, pas exception",
        echelle_des_departs="les deux départs dessinés gardent leur rapport "
                            "d’épaisseur (8 px pour le DN 80, 5 px pour le "
                            "DN 50) ; le DN 33, qui quitte le dessin, est "
                            "absent de ce format",
        depassements=depassements if depassements
                     else "aucun — surtitre et deux nœuds mesurés sous leur borne",
    )
    return "\n".join(out) + "\n", controles


# ═══ Dispatch — le bloc de l'extraction choisit le mécanisme ═════════════════

# ── Mécanisme `colonne` — le conduit collectif 3CEp (résidence Aurora) ───────
# Une production décentralisée (une chaudière étanche par logement) dont
# l'évacuation se partage : en gaine technique, les chaudières de quatre
# niveaux se piquent sur un conduit concentrique unique — fumées par le cœur,
# air de combustion par la couronne — éprouvé au test de fumée ; en façade,
# la ventouse individuelle. Deux registres confrontés, comme l'équilibre de
# Villedoux ; la géométrie porte la thèse : un seul conduit, quatre piquages.
# Toutes les constantes sont préfixées C_ (piège des affectations doublées,
# relevé le 2026-08-16 sur tableau-electrique.py).

C_Y_REGISTRES = 240           # en-têtes des deux registres
C_Y_TOIT = 300                # ligne de toiture du registre gauche
C_Y_SOL = 620                 # ligne de sol
C_PLANCHERS = (380, 460, 540) # les trois dalles intermédiaires
C_BANDES = (300, 380, 460, 540, 620)
C_X0, C_X1 = 80, 620          # emprise du registre gauche
C_BX0, C_BX1 = 140, 300       # les chaudières
C_CX = 340                    # axe du conduit collectif
C_AN = 16                     # demi-largeur de l'annulaire (couronne)
C_CO = 7                      # demi-largeur du cœur (fumées)
C_GX0, C_GX1 = 310, 370       # parois de la gaine technique
C_Y_TERMINAL = 262            # sommet du conduit (débouché)
C_Y_BASE = 596                # pied du conduit (té de purge)
C_X_APPELS = 400              # colonne des appels du registre gauche
C_LARG_APPELS = 236           # 636 − 400

C_VX0 = 704                   # emprise du registre droit
C_VMUR = 1010                 # nu de la façade
C_VBY0, C_VBY1 = 340, 384     # la chaudière de la ventouse
C_VDY = 362                   # axe du conduit concentrique horizontal
C_Y_TAILLES = 470             # en-tête du bloc des trois tailles
C_Y_BOITES = 488              # les trois gabarits
C_H_BOITES = 48
C_K_TAILLE = 8                # 1 L/min = 8 px de largeur de gabarit

C_Y_PIED = 655                # mention de pied


def composer_colonne(donnees):
    q = donnees["colonne"]
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

    # ── En-tête (il nomme la pièce d'où viennent les valeurs) et registres ───
    controler("en-tête schéma", q["entete"], 10, "mono", UTILE, 10 * 0.14)
    A(texte(MARGE, Y_ENTETE, q["entete"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    controler("registre gauche", q["registres"]["gauche"], 10, "mono",
              584, 10 * 0.14)
    A(texte(MARGE, C_Y_REGISTRES, q["registres"]["gauche"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    controler("registre droite", q["registres"]["droite"], 10, "mono",
              W - MARGE - C_VX0, 10 * 0.14)
    A(texte(W - MARGE, C_Y_REGISTRES, q["registres"]["droite"], "mono", 10,
            500, "pivot", ancre="end", tracking=10 * 0.14))

    # ── Registre gauche — la coupe : toiture, sol, dalles, gaine ─────────────
    # La ligne de toiture, percée au seul passage du conduit.
    A(ligne(C_X0, C_Y_TOIT, C_CX - C_AN - 4, C_Y_TOIT, "encre", 2))
    A(ligne(C_CX + C_AN + 4, C_Y_TOIT, C_X1, C_Y_TOIT, "encre", 2))
    # Le sol, et ses hachures.
    A(ligne(C_X0, C_Y_SOL, C_X1, C_Y_SOL, "filet-1", 2))
    for k in range(9):
        x = C_X0 + 30 + k * 60
        A(ligne(x, C_Y_SOL + 2, x - 9, C_Y_SOL + 10, "filet-2", 1))
    # Les dalles intermédiaires, interrompues par la gaine.
    for y in C_PLANCHERS:
        A(ligne(C_X0, y, C_GX0, y, "filet-2", 1.5))
        A(ligne(C_GX1, y, C_X1, y, "filet-2", 1.5))
    # Les parois de la gaine technique.
    for x in (C_GX0, C_GX1):
        A(ligne(x, C_Y_TOIT, x, C_Y_SOL, "filet-2", 1))

    # ── Les niveaux, et une chaudière par niveau ─────────────────────────────
    chaud = elems["chaudiere"]
    for k, niveau in enumerate(q["niveaux"]):
        haut = C_BANDES[k]
        controler(f"niveau {niveau}", niveau, 10, "mono", 44, 10 * 0.14)
        A(texte(C_X0 + 8, haut + 22, niveau, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))
        y0 = haut + 18
        A(rect_bord(C_BX0, y0, C_BX1 - C_BX0, 44, "papier", "filet-1"))
        y_racc = y0 + 22
        # Le raccord concentrique, et son clapet au piquage.
        A(ligne(C_BX1, y_racc - 4, C_CX - C_AN, y_racc - 4, "encre", 1.5))
        A(ligne(C_BX1, y_racc + 4, C_CX - C_AN, y_racc + 4, "encre", 1.5))
        A(cercle(C_CX - C_AN - 8, y_racc + 10, 3.5, "papier", "encre", 1.2))
    # La première chaudière porte le libellé du motif répété.
    y0 = C_BANDES[0] + 18
    controler("libellé chaudière", chaud["libelle"], 15, "sans-600",
              C_BX1 - C_BX0 - 24)
    A(texte(C_BX0 + 12, y0 + 19, chaud["libelle"], "sans", 15, 600, "encre",
            wdth=112))
    controler("détail chaudière", chaud["detail"][0], 10, "mono",
              C_BX1 - C_BX0 - 24, 10 * 0.14)
    A(texte(C_BX0 + 12, y0 + 36, chaud["detail"][0], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

    # ── Le conduit collectif : couronne, cœur, terminal, té de purge ─────────
    for x in (C_CX - C_AN, C_CX + C_AN):
        A(ligne(x, C_Y_TERMINAL, x, C_Y_BASE, "encre", 1.5))
    A(f'  <rect x="{C_CX - C_CO:.2f}" y="{C_Y_TERMINAL + 6:.2f}" '
      f'width="{2 * C_CO:.2f}" height="{C_Y_BASE - C_Y_TERMINAL - 6:.2f}" '
      f'class="c-clair s-encre" fill="#99CCCD" stroke="#00393A" '
      f'stroke-width="1"/>')
    # Le chapeau du débouché, au-dessus de la toiture.
    A(ligne(C_CX - C_AN - 4, C_Y_TERMINAL - 4, C_CX + C_AN + 4,
            C_Y_TERMINAL - 4, "encre", 2))
    deb = elems["debouche"]
    controler("libellé débouché", deb["libelle"].upper(), 10, "mono",
              C_X1 - (C_CX + C_AN + 16), 10 * 0.14)
    A(texte(C_CX + C_AN + 16, C_Y_TERMINAL + 2, deb["libelle"].upper(),
            "mono", 10, 500, "pivot", tracking=10 * 0.14))
    # Les fumées montent par le cœur…
    for y in (336, 476):
        A(fleche(C_CX, y, "encre", "haut", 8))
    # …l'air de combustion descend par la couronne.
    for x, y in ((C_CX - C_AN + 4.5, 318), (C_CX + C_AN - 4.5, 356)):
        A(fleche(x, y, "encre", "bas", 6))
    # Le té de purge, en pied, vers la colonne EU.
    A(ligne(C_CX, C_Y_BASE, C_CX, C_Y_SOL - 10, "encre", 1.5))
    A(ligne(C_CX, C_Y_SOL - 10, C_CX + 42, C_Y_SOL - 10, "encre", 1.5))
    A(fleche(C_CX + 50, C_Y_SOL - 10, "encre", "droite", 8))

    # ── Les appels du registre gauche ────────────────────────────────────────
    cond = elems["conduit"]
    A(ligne(C_CX + C_AN + 2, 332, C_X_APPELS - 8, 332, "filet-1", 1))
    controler("appel fumées", cond["detail"][0], 10, "mono",
              C_LARG_APPELS, 10 * 0.14)
    A(texte(C_X_APPELS, 335, cond["detail"][0], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    A(ligne(C_CX + C_AN + 2, 372, C_X_APPELS - 8, 372, "filet-1", 1))
    for k, l in enumerate(("AIR DE COMBUSTION", "PAR LA COURONNE")):
        controler(f"appel air {k + 1}", l, 10, "mono", C_LARG_APPELS, 10 * 0.14)
        A(texte(C_X_APPELS, 375 + k * 14, l, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))
    clap = elems["clapet"]
    A(ligne(C_CX + C_AN + 2, 500, C_X_APPELS - 8, 500, "filet-1", 1))
    for k, l in enumerate((clap["libelle"].upper(), clap["detail"][0])):
        controler(f"appel clapet {k + 1}", l, 10, "mono", C_LARG_APPELS,
                  10 * 0.14)
        A(texte(C_X_APPELS, 503 + k * 14, l, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))
    purge = elems["purge"]
    lib_purge = f'TÉ DE PURGE · {purge["detail"][0]}'
    controler("appel purge", lib_purge, 10, "mono",
              C_X1 - (C_CX + 58) + 240, 10 * 0.14)
    A(texte(C_CX + 58, C_Y_SOL - 6, lib_purge, "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

    # ── Registre droit — la ventouse individuelle ────────────────────────────
    vent = elems["ventouse"]
    # La façade, en deux segments de part et d'autre du conduit.
    A(rect(C_VMUR, 300, 6, C_VDY - 14 - 300, "encre"))
    A(rect(C_VMUR, C_VDY + 14, 6, 430 - (C_VDY + 14), "encre"))
    controler("mention extérieur", q.get("exterieur", "EXTÉRIEUR"), 10,
              "mono", 100, 10 * 0.14)
    A(texte(C_VMUR + 22, 316, q.get("exterieur", "EXTÉRIEUR"), "mono", 10,
            500, "pivot", tracking=10 * 0.14))
    # La chaudière, même gabarit qu'à gauche.
    A(rect_bord(790, C_VBY0, 160, C_VBY1 - C_VBY0, "papier", "filet-1"))
    controler("libellé chaudière ventouse", chaud["libelle"], 15, "sans-600",
              136)
    A(texte(802, C_VBY0 + 19, chaud["libelle"], "sans", 15, 600, "encre",
            wdth=112))
    A(texte(802, C_VBY0 + 36, chaud["detail"][0], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    # Le conduit concentrique horizontal, à travers la façade.
    A(ligne(950, C_VDY - 10, C_VMUR + 30, C_VDY - 10, "encre", 1.5))
    A(ligne(950, C_VDY + 10, C_VMUR + 30, C_VDY + 10, "encre", 1.5))
    A(f'  <rect x="950.00" y="{C_VDY - 4:.2f}" width="{C_VMUR + 42 - 950:.2f}" '
      f'height="8.00" class="c-clair s-encre" fill="#99CCCD" '
      f'stroke="#00393A" stroke-width="1"/>')
    A(ligne(C_VMUR + 42, C_VDY - 16, C_VMUR + 42, C_VDY + 16, "encre", 2))
    A(fleche(C_VMUR + 60, C_VDY, "encre", "droite", 8))
    controler("appel ventouse", vent["detail"][0], 10, "mono", 380, 10 * 0.14)
    A(texte(790, 412, vent["detail"][0], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

    # ── Les trois tailles : des gabarits proportionnels aux débits ───────────
    tailles = elems["tailles"]
    debits = [int(v.strip()) for v in tailles["valeur"].split("/")]
    controler("en-tête tailles", tailles["libelle"].upper(), 10, "mono",
              W - MARGE - C_VX0, 10 * 0.14)
    A(texte(C_VX0, C_Y_TAILLES, tailles["libelle"].upper(), "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    x = C_VX0
    boites = []
    for d in debits:
        w_b = d * C_K_TAILLE
        A(rect_bord(x, C_Y_BOITES, w_b, C_H_BOITES, "papier", "filet-1"))
        lib = f'{d}{NN}{tailles["unite"]}'
        controler(f"gabarit {d}", lib, 10, "mono", w_b - 8, 10 * 0.14)
        A(texte(x + w_b / 2, C_Y_BOITES + C_H_BOITES / 2 + 4, lib, "mono",
                10, 500, "pivot", ancre="middle", tracking=10 * 0.14))
        boites.append((x, w_b))
        x += w_b + ((W - MARGE - C_VX0) - sum(dd * C_K_TAILLE
                                              for dd in debits)) / 2
    for k, l in enumerate(tailles["detail"]):
        controler(f"détail tailles {k + 1}", l, 10, "mono",
                  W - MARGE - C_VX0, 10 * 0.14)
        A(texte(C_VX0, C_Y_BOITES + C_H_BOITES + 24 + k * 16, l, "mono", 10,
                500, "pivot", tracking=10 * 0.14))

    # ── Mention de pied, phrase de principe, cartouche ───────────────────────
    controler("mention de pied", q["mention_pied"], 10, "mono", UTILE,
              10 * 0.14)
    A(texte(MARGE, C_Y_PIED, q["mention_pied"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    l_phrase = controler("phrase de principe", donnees["phrase_principe"], 17,
                         "sans-400", UTILE)
    A(texte(MARGE, Y_PHRASE, donnees["phrase_principe"], "sans", 17, 400,
            "encre", wdth=100))
    libelle = donnees["cartouche_legende"]
    largeur = min(600,
                  round(mesurer(libelle, 11, "mono", tracking=11 * 0.14) + 40))
    A(rect(MARGE, Y_CARTOUCHE, largeur, H_CARTOUCHE, "profond"))
    A(texte(MARGE + 20, Y_CARTOUCHE + 20, libelle, "mono", 11, 500, "voile",
            tracking=11 * 0.14))

    A("</svg>")

    controles = {
        "gabarit": f"{W} x {H} — rapport {W/H:.4f} (3:2 exact)",
        "demonstration": "un seul conduit vertical traverse quatre niveaux et "
                         "la toiture ; quatre chaudières identiques s’y "
                         "piquent, chacune par son clapet ; les fumées "
                         "montent par le cœur (flèches hautes), l’air "
                         "descend par la couronne (flèches basses), le té de "
                         "purge sort en pied — face à lui, la ventouse "
                         "individuelle traverse la façade en un seul "
                         "terminal ; en bas à droite, trois gabarits de "
                         "largeur proportionnelle aux débits "
                         f"({C_K_TAILLE} px par L/min)",
        "topologie": f"registre gauche x {C_X0}–{C_X1} (chaudières "
                     f"{C_BX0}–{C_BX1}, conduit à x {C_CX}, couronne "
                     f"±{C_AN}, cœur ±{C_CO}, gaine {C_GX0}–{C_GX1}, "
                     f"toiture y {C_Y_TOIT}, sol y {C_Y_SOL}) ; registre "
                     f"droit x {C_VX0}–{W - MARGE} (façade à x {C_VMUR}, "
                     f"conduit horizontal à y {C_VDY}, gabarits y "
                     f"{C_Y_BOITES}–{C_Y_BOITES + C_H_BOITES})",
        "gabarits_debits": " · ".join(f"{d} L/min = {d * C_K_TAILLE} px"
                                      for d in debits),
        "bas_du_dessin": f"sol à {C_Y_SOL} (hachures à {C_Y_SOL + 10}), "
                         f"mention de pied à {C_Y_PIED}, phrase à {Y_PHRASE}, "
                         f"cartouche {Y_CARTOUCHE}–{Y_CARTOUCHE + H_CARTOUCHE}, "
                         f"marge basse {H - (Y_CARTOUCHE + H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur * H_CARTOUCHE} px², soit "
                            f"{largeur * H_CARTOUCHE / (W * H) * 100:.2f} % "
                            f"de la planche",
        "chiffre_unique": "aucun chiffre de relevé — la démonstration n’est "
                          "pas chiffrée (révision 4) ; les débits restent au "
                          "mono 10 pivot, dans leur gabarit",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l’échelle "
                         f"0,96 (1152 / {W})",
        "phrase_principe": f"{len(donnees['phrase_principe'])} signes — "
                           f"{l_phrase:.0f} px mesurés pour {UTILE} disponibles",
        "depassements": depassements if depassements
                        else "aucun — toutes les lignes mesurées sous leur colonne",
    }
    return "\n".join(out) + "\n", controles


def composer_vignette_colonne(donnees):
    """La vignette : la colonne seule — le conduit, trois piquages, le motif.

    Ce qu'elle garde : le conduit concentrique qui traverse les niveaux et la
    toiture, trois chaudières piquées, les flèches du cœur, le té de purge.
    Ce qu'elle laisse : la ventouse, les gabarits de débit, les appels — dix
    annotations dans 300 px ne se liraient pas."""
    q = donnees["colonne"]
    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false" '
      f'style="width:100%;height:auto;display:block">')
    entete_style(A)
    A(rect(0, 0, VW, VH, "papier"))
    A(texte(V_MARGE, 22, donnees["vignette_surtitre"], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    y_toit, y_sol = 56, 168
    planchers = (94, 131)
    cx, an, co = 170, 11, 5
    bx0, bx1 = 84, 148
    gx0, gx1 = 152, 190

    # Toiture percée, sol, dalles, gaine.
    A(ligne(30, y_toit, cx - an - 3, y_toit, "encre", 1.5))
    A(ligne(cx + an + 3, y_toit, 270, y_toit, "encre", 1.5))
    A(ligne(30, y_sol, 270, y_sol, "filet-1", 1.5))
    for y in planchers:
        A(ligne(30, y, gx0, y, "filet-2", 1))
        A(ligne(gx1, y, 270, y, "filet-2", 1))
    for x in (gx0, gx1):
        A(ligne(x, y_toit, x, y_sol, "filet-2", 0.8))

    # Le conduit : couronne, cœur, chapeau, purge.
    for x in (cx - an, cx + an):
        A(ligne(x, 44, x, 160, "encre", 1))
    A(f'  <rect x="{cx - co:.2f}" y="48.00" width="{2 * co:.2f}" '
      f'height="108.00" class="c-clair s-encre" fill="#99CCCD" '
      f'stroke="#00393A" stroke-width="0.8"/>')
    A(ligne(cx - an - 3, 41, cx + an + 3, 41, "encre", 1.5))
    A(fleche(cx, 66, "encre", "haut", 6))
    A(fleche(cx, 112, "encre", "haut", 6))
    A(ligne(cx, 160, cx, y_sol - 5, "encre", 1))
    A(ligne(cx, y_sol - 5, cx + 22, y_sol - 5, "encre", 1))
    A(fleche(cx + 27, y_sol - 5, "encre", "droite", 5))

    # Trois chaudières piquées, chacune par son raccord double.
    for haut, bas in ((y_toit, planchers[0]), (planchers[0], planchers[1]),
                      (planchers[1], y_sol)):
        y0 = haut + 9
        A(rect_bord(bx0, y0, bx1 - bx0, 18, "papier", "filet-1"))
        y_racc = y0 + 9
        A(ligne(bx1, y_racc - 2, cx - an, y_racc - 2, "encre", 0.8))
        A(ligne(bx1, y_racc + 2, cx - an, y_racc + 2, "encre", 0.8))

    # Le nœud : le motif répété a un nom.
    A(texte(V_MARGE, 188, "Une chaudière par logement", "sans", 12, 600,
            "encre", wdth=112))

    A("</svg>")
    controles = {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": f"carte de projet mesurée de 274 à 296 px — "
                            f"échelle {274/VW:.2f} à {296/VW:.2f}",
        "corps_minimal": f"9 px dans le repère — rendu à {9*274/VW:.1f} px au pire cas",
        "motif": "le conduit collectif seul : couronne, cœur fléché vers le "
                 "haut, trois chaudières piquées, té de purge — ventouse, "
                 "gabarits de débit et appels laissés à la planche",
        "bas_du_dessin": "nœud à y 188, marge basse 12 px",
    }
    return "\n".join(out) + "\n", controles


def composer_appui_colonne(donnees):
    """L'appui du hero : la colonne à l'échelle 1, trois appels, un nœud.

    Ce qu'il garde : le conduit traversant trois niveaux, les chaudières
    piquées, les flèches des deux flux, le té de purge, et le nœud des trois
    débits. Ce qu'il laisse : la ventouse et la mention de pied."""
    q = donnees["colonne"]
    elems = {e["cle"]: e for e in q["elements"]}
    tailles = elems["tailles"]
    out = []
    A = out.append
    racine_appui(A, donnees)

    y_toit, y_sol = 96, 316
    planchers = (170, 243)
    cx, an, co = 268, 13, 6
    bx0, bx1 = 96, 226
    gx0, gx1 = 232, 304

    A(ligne(48, y_toit, cx - an - 4, y_toit, "encre", 2))
    A(ligne(cx + an + 4, y_toit, 330, y_toit, "encre", 2))
    A(ligne(48, y_sol, 330, y_sol, "filet-1", 1.5))
    for k in range(5):
        x = 66 + k * 60
        A(ligne(x, y_sol + 2, x - 7, y_sol + 8, "filet-2", 1))
    for y in planchers:
        A(ligne(48, y, gx0, y, "filet-2", 1))
        A(ligne(gx1, y, 330, y, "filet-2", 1))
    for x in (gx0, gx1):
        A(ligne(x, y_toit, x, y_sol, "filet-2", 1))

    for x in (cx - an, cx + an):
        A(ligne(x, 74, x, 296, "encre", 1.2))
    A(f'  <rect x="{cx - co:.2f}" y="79.00" width="{2 * co:.2f}" '
      f'height="212.00" class="c-clair s-encre" fill="#99CCCD" '
      f'stroke="#00393A" stroke-width="1"/>')
    A(ligne(cx - an - 4, 70, cx + an + 4, 70, "encre", 2))
    for y in (108, 208):
        A(fleche(cx, y, "encre", "haut", 7))
    A(fleche(cx + an - 4, 152, "encre", "bas", 5))
    A(ligne(cx, 296, cx, y_sol - 8, "encre", 1.2))
    A(ligne(cx, y_sol - 8, cx + 30, y_sol - 8, "encre", 1.2))
    A(fleche(cx + 36, y_sol - 8, "encre", "droite", 6))

    chaud = elems["chaudiere"]
    for haut, bas in ((y_toit, planchers[0]), (planchers[0], planchers[1]),
                      (planchers[1], y_sol)):
        y0 = haut + 20
        A(rect_bord(bx0, y0, bx1 - bx0, 34, "papier", "filet-1"))
        y_racc = y0 + 17
        A(ligne(bx1, y_racc - 3, cx - an, y_racc - 3, "encre", 1))
        A(ligne(bx1, y_racc + 3, cx - an, y_racc + 3, "encre", 1))
        A(cercle(cx - an - 6, y_racc + 8, 2.5, "papier", "encre", 1))
    A(texte(bx0 + 8, y_toit + 41, chaud["libelle"], "sans", 13, 600,
            "encre", wdth=112))

    # Les appels, à droite.
    x_ap = 350
    A(ligne(cx + an + 2, 104, x_ap - 8, 104, "filet-1", 1))
    A(texte(x_ap, 107, "FUMÉES PAR LE CŒUR", "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    A(ligne(cx + an + 2, 132, x_ap - 8, 132, "filet-1", 1))
    A(texte(x_ap, 135, "AIR PAR LA COURONNE", "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    A(ligne(cx + an + 2, 196, x_ap - 8, 196, "filet-1", 1))
    A(texte(x_ap, 191, "CLAPET ANTI-RETOUR", "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    A(texte(x_ap, 205, "À CHAQUE PIQUAGE", "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    A(texte(cx + 44, y_sol - 4, "CONDENSATS VERS EU", "mono", 10, 500,
            "pivot", tracking=10 * 0.14))

    # Le nœud chiffré : les trois débits du label.
    A(texte(x_ap, 258, tailles["libelle"], "sans", 14, 600, "encre",
            wdth=112))
    A(texte(x_ap, 276, f'{tailles["valeur"]}{NN}{tailles["unite"]}', "mono",
            11, 500, "pivot", tabulaire=True))

    A("</svg>")
    return "\n".join(out) + "\n", controles_appui(
        motif="la colonne à l’échelle 1 : conduit concentrique traversant "
              "trois niveaux, chaudières piquées à clapet, flèches des deux "
              "flux, té de purge, et le nœud des trois débits — la ventouse "
              "et la mention de pied restent à la planche",
        bas=f"sol à 316 px (hachures à 324), condensats à 312, marge basse "
            f"{AH - 324} px")


# ── Mécanisme `sortie` — l'extraction quitte le logement (cité Louise Magnan) ─
# Deux maisons de principe confrontées : AVANT, le relevé du diagnostic — un
# extracteur en coffre à l'étage, des gaines souples (trait interrompu) qui
# convergent toutes en UN nœud sur le tronc de la cuisine, un rejet en façade,
# des entrées d'air barrées ; APRÈS, le dossier de consultation — le caisson sur
# dallettes et résilient AU-DESSUS de la ligne de toiture, un tronc rigide (bande
# claire à contour encré) qui traverse la dalle et la toiture par un fourreau
# bavetté, trois branches distinctes à trois hauteurs — un piquage par bouche —,
# un sifflet qui rejette au-dessus du toit, des entrées d'air fléchées vers
# l'intérieur. En bas, quatre gabarits de largeur proportionnelle aux débits de
# caisson des quatre typologies, comptés jusqu'à soixante.
# La maison est un gabarit à deux niveaux et toiture-terrasse : aucune proportion
# ni distribution réelle (règle 4). Constantes préfixées S_ (piège des
# affectations doublées, relevé le 2026-08-16 sur tableau-electrique.py).

S_Y_REG = 224                 # en-têtes des deux registres
S_Y_TOIT = 300                # ligne de toiture-terrasse
S_Y_DALLE = 400               # plancher intermédiaire
S_Y_SOL = 500                 # ligne de sol
S_Y_PIED = 526                # ligne de pied de chaque registre
S_H_ACRO = 16                 # l'acrotère : les murs dépassent la toiture
S_X0G, S_X1G = 96, 476        # murs de la maison AVANT
S_X0D, S_X1D = 724, 1104      # murs de la maison APRÈS
S_REG_G0, S_REG_G1 = MARGE, 560      # emprise du registre gauche
S_REG_D0, S_REG_D1 = 684, W - MARGE  # emprise du registre droit
S_R_BOUCHE = 5                # rayon d'une bouche d'extraction

# AVANT
S_A_TRONC = 232               # abscisse du tronc cuisine (le seul piquage)
S_A_Y_NOEUD = 336             # ordonnée du nœud unique
S_A_SDB = (166, 322)          # les trois bouches
S_A_WC = (166, 424)
S_A_CUIS = (232, 424)
S_A_COFFRE = (340, 316, 100, 40)   # x, y, largeur, hauteur du coffre
S_A_CAISSON = (352, 322, 76, 28)   # l'extracteur, dedans
S_A_X_LABELS = 116            # colonne des libellés intérieurs
S_A_X_FIN = 466               # ancre droite des libellés du coffre

# APRÈS
S_P_TRONC = 796               # abscisse du tronc rigide
S_P_W_TRONC = 12
S_P_CAISSON = (760, 256, 72, 28)
S_P_SDB = (900, 372)          # trois bouches, trois hauteurs
S_P_WC = (900, 420)
S_P_CUIS = (990, 448)
S_P_X_LABELS = 842            # colonne des appels
S_P_X_INT = 738               # libellés intérieurs du RDC

# Gabarits des typologies
S_Y_TYPO_ENTETE = 552
S_Y_GAB = 566
S_H_GAB = 44
S_K_GAB = 1.6                 # 1 m³/h = 1,6 px de largeur de gabarit
S_Y_MENTION = 640


def _souple(A, points, epaisseur=1.5, motif="5 4"):
    """Une gaine souple : trait interrompu, encre — le contraire du conduit
    plein à bande claire qui dit le réseau rigide."""
    from _tronc import JETON
    d = "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in points)
    A(f'  <path d="{d}" fill="none" class="s-encre" stroke="{JETON["encre"]}" '
      f'stroke-width="{epaisseur}" stroke-dasharray="{motif}"/>')


def _maison(A, x0, x1, niveaux, gap_tronc=None):
    """Le gabarit de maison : deux murs qui dépassent la toiture-terrasse
    (acrotère), la ligne de toiture, la dalle, le sol hachuré, les niveaux."""
    for x in (x0, x1):
        A(rect(x - 2, S_Y_TOIT - S_H_ACRO, 4, S_Y_SOL - S_Y_TOIT + S_H_ACRO,
               "encre"))
    A(ligne(x0, S_Y_TOIT, x1, S_Y_TOIT, "encre", 2))
    if gap_tronc is None:
        A(ligne(x0, S_Y_DALLE, x1, S_Y_DALLE, "filet-2", 1.5))
    else:
        A(ligne(x0, S_Y_DALLE, gap_tronc - 10, S_Y_DALLE, "filet-2", 1.5))
        A(ligne(gap_tronc + 10, S_Y_DALLE, x1, S_Y_DALLE, "filet-2", 1.5))
    A(ligne(x0, S_Y_SOL, x1, S_Y_SOL, "filet-1", 2))
    for k in range(9):
        x = x0 + 20 + k * 42
        A(ligne(x, S_Y_SOL + 2, x - 9, S_Y_SOL + 10, "filet-2", 1))
    for niveau, y in zip(niveaux, (S_Y_TOIT, S_Y_DALLE)):
        A(texte(x0 + 10, y + 18, niveau, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))


def _bouche(A, x, y, r=S_R_BOUCHE):
    A(cercle(x, y, r, "papier", "encre", 1.2))


def composer_sortie(donnees):
    q = donnees["sortie"]
    av = {e["cle"]: e for e in q["avant"]["elements"]}
    ap = {e["cle"]: e for e in q["apres"]["elements"]}
    typo = q["typologies"]
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

    # ── En-tête (il nomme les pièces d'où viennent les valeurs) et registres ─
    controler("en-tête schéma", q["entete"], 10, "mono", UTILE, 10 * 0.14)
    A(texte(MARGE, Y_ENTETE, q["entete"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    controler("registre gauche", q["registres"]["gauche"], 10, "mono",
              S_REG_G1 - S_REG_G0, 10 * 0.14)
    A(texte(S_REG_G0, S_Y_REG, q["registres"]["gauche"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    controler("registre droite", q["registres"]["droite"], 10, "mono",
              S_REG_D1 - S_REG_D0, 10 * 0.14)
    A(texte(S_REG_D1, S_Y_REG, q["registres"]["droite"], "mono", 10, 500,
            "pivot", ancre="end", tracking=10 * 0.14))

    # ── Registre gauche — AVANT : l'extracteur en coffre, un seul piquage ────
    _maison(A, S_X0G, S_X1G, q["niveaux"])
    cx, cy, cw, ch = S_A_COFFRE
    rect_interrompu(A, cx + cw / 2, cy, cy + ch, cw, 1.2, "6 5")
    kx, ky, kw, kh = S_A_CAISSON
    A(rect_bord(kx, ky, kw, kh, "papier", "filet-1"))
    A(cercle(kx + kw / 2, ky + kh / 2, 6, "papier", "encre", 1.2))
    # Les trois bouches et leurs gaines souples, toutes vers le seul nœud.
    for x, y in (S_A_SDB, S_A_WC, S_A_CUIS):
        _bouche(A, x, y)
    _souple(A, [(S_A_WC[0] + S_R_BOUCHE, S_A_WC[1]),
                (S_A_CUIS[0], S_A_CUIS[1])])
    _souple(A, [(S_A_CUIS[0], S_A_CUIS[1] - S_R_BOUCHE),
                (S_A_TRONC, S_A_Y_NOEUD), (cx, S_A_Y_NOEUD)])
    _souple(A, [(S_A_SDB[0] + S_R_BOUCHE, S_A_SDB[1]),
                (S_A_TRONC, S_A_Y_NOEUD)])
    A(cercle(S_A_TRONC, S_A_Y_NOEUD, 4, "clair", "encre", 1.2))
    # Le rejet en façade : la gaine souple traverse le mur, une flèche sort.
    _souple(A, [(kx + kw, S_A_Y_NOEUD), (S_X1G - 2, S_A_Y_NOEUD)])
    A(ligne(S_X1G + 2, S_A_Y_NOEUD, S_X1G + 22, S_A_Y_NOEUD, "encre", 1.5))
    A(fleche(S_X1G + 30, S_A_Y_NOEUD, "encre", "droite", 8))
    # Les entrées d'air obturées : un cadre barré dans le mur, à chaque niveau.
    for y in (346, 446):
        A(rect_bord(S_X0G - 8, y, 16, 10, "papier", "encre"))
        A(ligne(S_X0G - 7, y + 1, S_X0G + 7, y + 9, "encre", 1))
        A(ligne(S_X0G - 7, y + 9, S_X0G + 7, y + 1, "encre", 1))
    # Les libellés.
    piq = av["piquage"]
    for k, l in enumerate(piq["detail"]):
        controler(f"nœud {k + 1}", l, 10, "mono", cx - (S_A_TRONC + 12), 10 * 0.14)
        A(texte(S_A_TRONC + 12, 318 + k * 12, l, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))
    ext = av["extracteur"]
    for k, l in enumerate(ext["detail"]):
        controler(f"extracteur {k + 1}", l, 10, "mono",
                  S_A_X_FIN - (S_A_TRONC + 12), 10 * 0.14)
        A(texte(S_A_X_FIN, 372 + k * 14, l, "mono", 10, 500, "pivot",
                ancre="end", tracking=10 * 0.14))
    cui = av["cuisine"]
    for k, l in enumerate(cui["detail"]):
        controler(f"cuisine {k + 1}", l, 10, "mono", S_X1G - 10 - S_A_X_LABELS,
                  10 * 0.14)
        A(texte(S_A_X_LABELS, 470 + k * 16, l, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))
    rej = av["rejet"]
    for k, l in enumerate(rej["detail"]):
        controler(f"rejet {k + 1}", l, 10, "mono", S_REG_G1 - (S_X1G + 6),
                  10 * 0.14)
        A(texte(S_X1G + 6, 318 + k * 14, l, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))
    controler("pied avant", q["avant"]["pied"], 10, "mono",
              S_REG_G1 - S_REG_G0, 10 * 0.14)
    A(texte(S_REG_G0, S_Y_PIED, q["avant"]["pied"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

    # ── Registre droit — APRÈS : le caisson sur le toit, un piquage par bouche
    _maison(A, S_X0D, S_X1D, q["niveaux"], gap_tronc=S_P_TRONC)
    px, py, pw, ph = S_P_CAISSON
    # Le résilient, les deux dallettes, le caisson — au-dessus de la toiture.
    A(rect(px, S_Y_TOIT - 8, pw, 8, "clair"))
    A(rect(px + 6, py + ph, 14, 8, "encre"))
    A(rect(px + pw - 20, py + ph, 14, 8, "encre"))
    A(rect_bord(px, py, pw, ph, "papier", "filet-1"))
    A(cercle(S_P_TRONC, py + ph / 2, 6, "papier", "encre", 1.2))
    # Le tronc rigide, de la bouche la plus basse au caisson, à travers tout.
    conduit_plein(A, S_P_TRONC, py + ph, S_P_CUIS[1], S_P_W_TRONC)
    for y in (350, 432):
        A(fleche(S_P_TRONC, y, "encre", "haut", 7))
    # La traversée de la toiture : fourreau et bavette.
    for x in (S_P_TRONC - 10, S_P_TRONC + 10):
        A(ligne(x, S_Y_TOIT - 14, x, S_Y_TOIT + 6, "encre", 1))
    A(ligne(S_P_TRONC - 10, S_Y_TOIT - 6, S_P_TRONC - 18, S_Y_TOIT, "encre", 1))
    A(ligne(S_P_TRONC + 10, S_Y_TOIT - 6, S_P_TRONC + 18, S_Y_TOIT, "encre", 1))
    # Le sifflet de rejet, au-dessus du toit, vers l'extérieur.
    A(polyligne([(px, py + 14), (px - 16, py + 14), (px - 16, py - 12),
                 (px - 28, py - 12)], "encre", 1.5))
    A(fleche(px - 36, py - 12, "encre", "gauche", 7))
    # Trois bouches, trois branches rigides à trois hauteurs.
    for x, y in (S_P_SDB, S_P_WC, S_P_CUIS):
        _bouche(A, x, y)
        A(ligne(x - S_R_BOUCHE, y, S_P_TRONC + S_P_W_TRONC / 2, y, "encre", 1.5))
        A(ligne(S_P_TRONC + 26, y - 4, S_P_TRONC + 26, y + 4, "encre", 1))
    bou = ap["bouches"]
    for (x, y), l in zip((S_P_SDB, S_P_WC, S_P_CUIS), bou["detail"]):
        A(texte(x + 10, y + 4, l, "mono", 10, 500, "pivot", tracking=10 * 0.14))
    # Les entrées d'air : un cadre dans le mur, une flèche vers l'intérieur.
    for y in (346, 446):
        A(rect_bord(S_X0D - 8, y, 16, 10, "papier", "encre"))
        A(fleche(S_X0D + 24, y + 5, "encre", "droite", 7))
    # Les appels.
    cai = ap["caisson"]
    for k, l in enumerate(cai["detail"]):
        controler(f"caisson {k + 1}", l, 10, "mono", S_X1D - 10 - S_P_X_LABELS,
                  10 * 0.14)
        A(texte(S_P_X_LABELS, 266 + k * 14, l, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))
    A(ligne(S_P_TRONC + 12, S_Y_TOIT + 2, S_P_X_LABELS - 6, 322, "filet-1", 1))
    tra = ap["traversee"]
    for k, l in enumerate(tra["detail"]):
        controler(f"traversée {k + 1}", l, 10, "mono",
                  S_X1D - 10 - S_P_X_LABELS, 10 * 0.14)
        A(texte(S_P_X_LABELS, 326 + k * 14, l, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))
    res = ap["reseau"]
    for k, l in enumerate(res["detail"]):
        controler(f"réseau {k + 1}", l, 10, "mono", S_X1D - 10 - S_P_X_INT,
                  10 * 0.14)
        A(texte(S_P_X_INT, 474 + k * 14, l, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))
    sif = ap["sifflet"]
    # Le libellé du sifflet s'ancre à droite devant la flèche, dans la
    # gouttière entre les deux registres : de S_REG_G1 à px − 44.
    controler("sifflet", sif["detail"][0], 10, "mono", (px - 44) - S_REG_G1,
              10 * 0.14)
    A(texte(px - 44, py - 16, sif["detail"][0], "mono", 10, 500, "pivot",
            ancre="end", tracking=10 * 0.14))
    controler("pied après", q["apres"]["pied"], 10, "mono",
              S_REG_D1 - S_REG_D0, 10 * 0.14)
    A(texte(S_REG_D0, S_Y_PIED, q["apres"]["pied"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

    # ── Les quatre typologies : des gabarits proportionnels aux débits ───────
    controler("en-tête typologies", typo["entete"], 10, "mono", UTILE,
              10 * 0.14)
    A(texte(MARGE, S_Y_TYPO_ENTETE, typo["entete"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    gabarits = typo["gabarits"]
    largeurs = [g["debit"] * S_K_GAB for g in gabarits]
    ecart = (UTILE - sum(largeurs)) / (len(gabarits) - 1)
    x = MARGE
    for g, w_g in zip(gabarits, largeurs):
        A(rect_bord(x, S_Y_GAB, w_g, S_H_GAB, "papier", "filet-1"))
        controler(f"gabarit {g['cle']} libellé", g["libelle"], 15, "sans-600",
                  w_g - 24)
        A(texte(x + 12, S_Y_GAB + 19, g["libelle"], "sans", 15, 600, "encre",
                wdth=112))
        deb = f'{g["debit"]}{NN}{typo["unite"]}'
        controler(f"gabarit {g['cle']} débit", deb, 10, "mono", w_g - 24,
                  10 * 0.14)
        A(texte(x + 12, S_Y_GAB + 36, deb, "mono", 10, 500, "pivot",
                tracking=10 * 0.14, tabulaire=True))
        x += w_g + ecart
    total = sum(g["maisons"] for g in gabarits)

    # ── Mention de pied, phrase de principe, cartouche ───────────────────────
    controler("mention de pied", q["mention_pied"], 10, "mono", UTILE,
              10 * 0.14)
    A(texte(MARGE, S_Y_MENTION, q["mention_pied"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    l_phrase = controler("phrase de principe", donnees["phrase_principe"], 17,
                         "sans-400", UTILE)
    A(texte(MARGE, Y_PHRASE, donnees["phrase_principe"], "sans", 17, 400,
            "encre", wdth=100))
    libelle = donnees["cartouche_legende"]
    largeur = min(600,
                  round(mesurer(libelle, 11, "mono", tracking=11 * 0.14) + 40))
    A(rect(MARGE, Y_CARTOUCHE, largeur, H_CARTOUCHE, "profond"))
    A(texte(MARGE + 20, Y_CARTOUCHE + 20, libelle, "mono", 11, 500, "voile",
            tracking=11 * 0.14))

    A("</svg>")

    controles = {
        "gabarit": f"{W} x {H} — rapport {W/H:.4f} (3:2 exact)",
        "demonstration": "deux maisons de principe identiques (murs, acrotère, "
                         "toiture-terrasse, dalle, sol) ; à gauche l’extracteur "
                         "est DANS la maison, en coffre interrompu, et trois "
                         "gaines souples convergent en un seul nœud avant un "
                         "rejet en façade, les entrées d’air sont barrées ; à "
                         "droite le caisson est AU-DESSUS de la toiture, un "
                         "tronc plein la traverse par un fourreau bavetté, "
                         "trois branches distinctes s’y piquent à trois "
                         "hauteurs, le sifflet rejette au-dessus du toit, les "
                         "entrées d’air sont fléchées vers l’intérieur ; en "
                         "bas quatre gabarits de largeur proportionnelle aux "
                         f"débits ({S_K_GAB} px par m³/h) — texte masqué, la "
                         "sortie du caisson et la multiplication des piquages "
                         "se lisent",
        "topologie": f"maison AVANT x {S_X0G}–{S_X1G} (tronc à x {S_A_TRONC}, "
                     f"nœud y {S_A_Y_NOEUD}, coffre {cx}–{cx + cw}, rejet vers "
                     f"x {S_X1G + 30}) ; maison APRÈS x {S_X0D}–{S_X1D} (tronc "
                     f"à x {S_P_TRONC}, caisson {px}–{px + pw} à y {py}–{py + ph}"
                     f" au-dessus de la toiture y {S_Y_TOIT}, bouches à y "
                     f"{S_P_SDB[1]} / {S_P_WC[1]} / {S_P_CUIS[1]}) ; toiture y "
                     f"{S_Y_TOIT}, dalle y {S_Y_DALLE}, sol y {S_Y_SOL}",
        "gabarits_debits": " · ".join(
            f'{g["libelle"]} = {g["debit"]} m³/h = {w:.0f} px'
            for g, w in zip(gabarits, largeurs)) + f" — écart {ecart:.2f} px",
        "conservation": " + ".join(str(g["maisons"]) for g in gabarits)
                        + f" = {total} maisons",
        "bas_du_dessin": f"sol à {S_Y_SOL} (hachures à {S_Y_SOL + 10}), pieds "
                         f"de registre à {S_Y_PIED}, gabarits {S_Y_GAB}–"
                         f"{S_Y_GAB + S_H_GAB}, mention à {S_Y_MENTION}, phrase "
                         f"à {Y_PHRASE}, cartouche {Y_CARTOUCHE}–"
                         f"{Y_CARTOUCHE + H_CARTOUCHE}, marge basse "
                         f"{H - (Y_CARTOUCHE + H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur * H_CARTOUCHE} px², soit "
                            f"{largeur * H_CARTOUCHE / (W * H) * 100:.2f} % "
                            f"de la planche",
        "chiffre_unique": "aucun chiffre de relevé — la démonstration n’est "
                          "pas chiffrée (révision 4) ; le débit mesuré du "
                          "diagnostic et les débits de caisson restent au "
                          "mono 10 pivot",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l’échelle "
                         f"0,96 (1152 / {W})",
        "phrase_principe": f"{len(donnees['phrase_principe'])} signes — "
                           f"{l_phrase:.0f} px mesurés pour {UTILE} disponibles",
        "depassements": depassements if depassements
                        else "aucun — toutes les lignes mesurées sous leur colonne",
    }
    return "\n".join(out) + "\n", controles


def composer_vignette_sortie(donnees):
    """La vignette : la maison APRÈS seule — le caisson sur le toit, le tronc
    qui traverse, trois branches, le sifflet, les entrées d'air.

    Ce qu'elle garde : le motif entier de la sortie. Ce qu'elle laisse : le
    registre AVANT, les appels, les gabarits de débit — dix annotations dans
    300 px ne se liraient pas."""
    q = donnees["sortie"]
    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false" '
      f'style="width:100%;height:auto;display:block">')
    entete_style(A)
    A(rect(0, 0, VW, VH, "papier"))
    A(texte(V_MARGE, 22, donnees["vignette_surtitre"], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    x0, x1 = 70, 230
    y_toit, y_dalle, y_sol = 66, 112, 160
    tx = 120                    # le tronc
    for x in (x0, x1):
        A(rect(x - 1.5, y_toit - 8, 3, y_sol - y_toit + 8, "encre"))
    A(ligne(x0, y_toit, x1, y_toit, "encre", 1.5))
    A(ligne(x0, y_dalle, tx - 6, y_dalle, "filet-2", 1))
    A(ligne(tx + 6, y_dalle, x1, y_dalle, "filet-2", 1))
    A(ligne(x0, y_sol, x1, y_sol, "filet-1", 1.5))
    for k in range(5):
        x = x0 + 14 + k * 34
        A(ligne(x, y_sol + 2, x - 6, y_sol + 7, "filet-2", 0.8))
    # Caisson sur ses dallettes, au-dessus du toit ; tronc qui traverse.
    A(rect_bord(100, 46, 40, 14, "papier", "filet-1"))
    A(rect(104, 60, 8, 6, "encre"))
    A(rect(128, 60, 8, 6, "encre"))
    conduit_plein(A, tx, 60, 146, 6)
    A(fleche(tx, 92, "encre", "haut", 5))
    A(fleche(tx, 136, "encre", "haut", 5))
    for x in (tx - 5, tx + 5):
        A(ligne(x, y_toit - 7, x, y_toit + 3, "encre", 0.8))
    # Sifflet vers l'extérieur.
    A(polyligne([(100, 53), (92, 53), (92, 42), (84, 42)], "encre", 1))
    A(fleche(80, 42, "encre", "gauche", 5))
    # Trois bouches, trois branches.
    for x, y in ((176, 96), (176, 128), (206, 146)):
        A(cercle(x, y, 3, "papier", "encre", 1))
        A(ligne(x - 3, y, tx + 3, y, "encre", 1))
    # Entrées d'air fléchées vers l'intérieur.
    for y in (90, 140):
        A(rect_bord(x0 - 5, y - 3, 10, 6, "papier", "encre"))
        A(fleche(x0 + 16, y, "encre", "droite", 4))

    # Le nœud : le motif répété a un nom.
    A(texte(V_MARGE, 188, q["vignette_noeud"], "sans", 12, 600, "encre",
            wdth=112))

    A("</svg>")
    controles = {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": f"carte de projet mesurée de 274 à 296 px — "
                            f"échelle {274/VW:.2f} à {296/VW:.2f}",
        "corps_minimal": f"9 px dans le repère — rendu à {9*274/VW:.1f} px au pire cas",
        "motif": "la maison APRÈS seule : caisson sur dallettes au-dessus de la "
                 "toiture, tronc fléché qui traverse dalle et toiture, trois "
                 "branches, sifflet, entrées d’air — registre AVANT, appels et "
                 "gabarits de débit laissés à la planche",
        "bas_du_dessin": "nœud à y 188, marge basse 12 px",
    }
    return "\n".join(out) + "\n", controles


def composer_appui_sortie(donnees):
    """L'appui du hero : la maison APRÈS à l'échelle 1, trois appels, et le
    nœud chiffré des quatre débits de caisson."""
    q = donnees["sortie"]
    typo = q["typologies"]
    out = []
    A = out.append
    racine_appui(A, donnees)

    x0, x1 = 48, 288
    y_toit, y_dalle, y_sol = 96, 196, 296
    tx = 176
    for x in (x0, x1):
        A(rect(x - 2, y_toit - 12, 4, y_sol - y_toit + 12, "encre"))
    A(ligne(x0, y_toit, x1, y_toit, "encre", 2))
    A(ligne(x0, y_dalle, tx - 9, y_dalle, "filet-2", 1))
    A(ligne(tx + 9, y_dalle, x1, y_dalle, "filet-2", 1))
    A(ligne(x0, y_sol, x1, y_sol, "filet-1", 1.5))
    for k in range(6):
        x = x0 + 18 + k * 42
        A(ligne(x, y_sol + 2, x - 7, y_sol + 8, "filet-2", 1))
    for niveau, y in zip(q["niveaux"], (y_toit, y_dalle)):
        A(texte(x0 + 8, y + 16, niveau, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))
    # Résilient, dallettes, caisson ; tronc ; fourreau ; sifflet.
    A(rect(148, y_toit - 6, 56, 6, "clair"))
    A(rect(154, 84, 10, 6, "encre"))
    A(rect(188, 84, 10, 6, "encre"))
    A(rect_bord(148, 62, 56, 22, "papier", "filet-1"))
    A(cercle(tx, 73, 5, "papier", "encre", 1))
    conduit_plein(A, tx, 84, 246, 9)
    for y in (150, 236):
        A(fleche(tx, y, "encre", "haut", 6))
    for x in (tx - 8, tx + 8):
        A(ligne(x, y_toit - 10, x, y_toit + 5, "encre", 1))
    A(polyligne([(148, 73), (136, 73), (136, 54), (126, 54)], "encre", 1.2))
    A(fleche(120, 54, "encre", "gauche", 6))
    # Trois bouches, trois branches, nommées.
    bou = {e["cle"]: e for e in q["apres"]["elements"]}["bouches"]
    for (x, y), l in zip(((222, 150), (222, 222), (222, 246)), bou["detail"]):
        A(cercle(x, y, 4, "papier", "encre", 1))
        A(ligne(x - 4, y, tx + 4.5, y, "encre", 1.2))
        A(texte(x + 8, y + 4, l, "mono", 10, 500, "pivot", tracking=10 * 0.14))
    for y in (150, 240):
        A(rect_bord(x0 - 6, y - 4, 12, 8, "papier", "encre"))
        A(fleche(x0 + 18, y, "encre", "droite", 5))

    # Les appels, à droite.
    x_ap = 300
    appels = q["appui_appels"]
    A(ligne(204, 73, x_ap - 8, 108, "filet-1", 1))
    A(texte(x_ap, 112, appels[0], "mono", 10, 500, "pivot", tracking=10 * 0.14))
    A(ligne(tx + 8, y_toit + 2, x_ap - 8, 154, "filet-1", 1))
    A(texte(x_ap, 158, appels[1], "mono", 10, 500, "pivot", tracking=10 * 0.14))
    A(ligne(tx + 4.5, 186, x_ap - 8, 200, "filet-1", 1))
    A(texte(x_ap, 204, appels[2], "mono", 10, 500, "pivot", tracking=10 * 0.14))

    # Le nœud chiffré : les quatre débits de caisson, et le compte.
    A(texte(x_ap, 258, typo["appui_libelle"], "sans", 14, 600, "encre",
            wdth=112))
    A(texte(x_ap, 276, f'{typo["appui_valeur"]}{NN}{typo["unite"]}', "mono",
            11, 500, "pivot", tabulaire=True))
    compte = " + ".join(str(g["maisons"]) for g in typo["gabarits"]) + " MAISONS"
    A(texte(x_ap, 292, compte, "mono", 10, 500, "pivot", tracking=10 * 0.14,
            tabulaire=True))

    A("</svg>")
    return "\n".join(out) + "\n", controles_appui(
        motif="la maison APRÈS à l’échelle 1 : caisson sur dallettes au-dessus "
              "de la toiture, tronc fléché qui traverse, trois branches nommées, "
              "sifflet, entrées d’air, trois appels et le nœud des quatre débits "
              "de caisson — le registre AVANT et les gabarits restent à la "
              "planche",
        bas=f"sol à {y_sol} px (hachures à {y_sol + 8}), compte à 292, marge "
            f"basse {AH - (y_sol + 8)} px")


# ── Mécanisme `frontiere` — deux régimes de desserte sous un même toit ───────
#
# Bâtiment d'assemblage d'avions de Saint-Agnant (session N13). Le programme de
# l'utilisateur décrit la desserte zone par zone, et il en sort deux régimes qui
# ne se ressemblent pas de part et d'autre du mur qui sépare le hall du plateau
# de bureaux : à gauche les services DESCENDENT d'un maillage de plafond au pas
# de 10 m et s'arrêtent à 2,50 m ; à droite ils MONTENT de la plinthe. Et deux
# des quatre familles n'ont pas de côté droit du tout — le programme y écrit
# « N/A ».
#
# La géométrie porte seule les deux démonstrations : l'inversion du sens des
# piquages d'un côté à l'autre (rang 2), et les deux cellules barrées du bas
# (rangs 3 et 4), qui laissent la colonne de droite s'interrompre à mi-hauteur.
# Le rang 4 ajoute une troisième inversion, interne au hall : le triphasé de
# charge est le seul service qui n'arrive pas du plafond mais du SOL, en deux
# blocs pleins posés en bordure — la puissance lourde ne pleut pas.
#
# ⚠ Toutes les constantes de ce mécanisme portent le préfixe `FR_` : deux
# mécanismes d'un même module qui affectent le même nom se marchent dessus, la
# seconde affectation gagne, et c'est le PREMIER dessin qui se recompose faux
# (piège relevé le 2026-08-16 sur `tableau-electrique.py`).
FR_Y_REGISTRES = 216
FR_X_LIB = MARGE                     # colonne des libellés de service
FR_X_LIB_FIN = 300
FR_XH0, FR_XH1 = 320, 716            # colonne du hall
FR_X_MUR = 730                       # la frontière
FR_EP_MUR = 4
FR_XB0, FR_XB1 = 744, 1144           # colonne des bureaux
FR_MUR_Y0, FR_MUR_Y1 = 224, 636
FR_Y_MUR_LIB = 658

FR_T = (230, 332, 434, 536)          # ordonnée haute des quatre rangs
FR_D_PLAFOND = 14                    # ligne de plafond, depuis le haut du rang
FR_D_PIED = 46                       # pied des descentes
FR_D_SOL = 62                        # ligne de sol
FR_D_MONO1 = 80
FR_D_MONO2 = 94
FR_D_LIB = 30                        # libellé de service
FR_D_LIB_MONO = 50

FR_N_DESCENTES = 6                   # le maillage, régulier — pas une implantation
FR_N_MONTEES = 5
FR_TICK = 5                          # demi-largeur du sabot d'une descente
FR_BLOC_L, FR_BLOC_H = 128, 40       # machine de traitement d'air
FR_CHARGE_L, FR_CHARGE_H = 64, 26    # bloc de puissance de charge
FR_CROIX = 16                        # demi-bras de la croix « sans objet »


def _fr_croix(A, cx, cy, bras=FR_CROIX, epaisseur=1.8):
    """La marque d'absence : deux traits croisés, toujours doublés d'un mot."""
    A(ligne(cx - bras, cy - bras, cx + bras, cy + bras, "encre", epaisseur))
    A(ligne(cx - bras, cy + bras, cx + bras, cy - bras, "encre", epaisseur))


def _fr_pointille(A, x0, x1, y, cle="filet-1", epaisseur=1.0, pas=9, plein=5):
    """Un niveau conventionnel — un trait interrompu, jamais une cote d'ouvrage."""
    x = x0
    while x < x1:
        A(ligne(x, y, min(x + plein, x1), y, cle, epaisseur))
        x += pas


def _fr_descentes(A, x0, x1, y_haut, y_pied, n=FR_N_DESCENTES, tick=FR_TICK,
                  sabot="tick"):
    """Un maillage de plafond : n descentes régulières, sabot en pied.

    Deux sabots, parce que deux rangs emploient le même maillage et qu'un motif
    répété à l'identique ne démontre rien : `tick` pour le piquage électrique,
    `vanne` — un cercle — pour l'attente d'air comprimé, qui se raccorde.
    Rend leurs abscisses pour le bloc `controles`."""
    pas = (x1 - x0) / n
    xs = [x0 + pas * (k + 0.5) for k in range(n)]
    for x in xs:
        A(ligne(x, y_haut, x, y_pied, "encre", 1.4))
        if sabot == "vanne":
            A(cercle(x, y_pied, tick * 0.9, "papier", "encre", 1.3))
        else:
            A(ligne(x - tick, y_pied, x + tick, y_pied, "encre", 1.8))
    return xs, pas


def _fr_montees(A, x0, x1, y_bas, y_tete, n=FR_N_MONTEES, tick=FR_TICK):
    """L'inverse : n piquages qui montent du sol, sabot en tête."""
    pas = (x1 - x0) / n
    xs = [x0 + pas * (k + 0.5) for k in range(n)]
    for x in xs:
        A(ligne(x, y_bas, x, y_tete, "encre", 1.4))
        A(ligne(x - tick, y_tete, x + tick, y_tete, "encre", 1.8))
    return xs, pas


def _fr_gaine(A, x0, x1, y0, y1, xs_souffle):
    """Une gaine de soufflage : deux filets parallèles et des flèches vers le bas."""
    A(ligne(x0, y0, x1, y0, "encre", 1.4))
    A(ligne(x0, y1, x1, y1, "encre", 1.4))
    for x in xs_souffle:
        A(ligne(x, y1, x, y1 + 8, "encre", 1.2))
        A(fleche(x, y1 + 16, "encre", "bas", 8))


def composer_frontiere(donnees):
    q = donnees["frontiere"]
    rangs = q["rangs"]
    out = []
    A = out.append
    depassements = []

    def controler(nom, chaine, corps, profil, dispo, tracking=0.0):
        largeur = mesurer(chaine, corps, profil, tracking)
        if largeur > dispo:
            depassements.append(f"{nom} : {largeur:.0f} px pour {dispo:.0f} px")
        return largeur

    def mono(x, y, chaine, dispo, nom, ancre=None, couleur="pivot", corps=10):
        controler(nom, chaine, corps, "mono", dispo, corps * 0.14)
        A(texte(x, y, chaine, "mono", corps, 500, couleur, ancre=ancre,
                tracking=corps * 0.14))

    # ── Racine ───────────────────────────────────────────────────────────────
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
      f'preserveAspectRatio="xMidYMid meet" role="img" '
      f'style="width:100%;height:auto;display:block" '
      f'aria-label="{echapper(donnees["aria_label"])}">')
    entete_style(A)
    A(rect(0, 0, W, H, "papier"))

    # ── Bloc de titre ────────────────────────────────────────────────────────
    A(texte(MARGE, Y_SURTITRE, donnees["surtitre"], "mono", 11, 500, "pivot",
            tracking=11 * 0.14))
    A(texte(MARGE, Y_TITRE, donnees["titre"], "sans", 30, 700, "encre", wdth=112))
    A(texte(MARGE, Y_SOUSTITRE, donnees["sous_titre"], "sans", 16, 400, "pivot",
            wdth=100))
    A(rect(MARGE, Y_FILET_TITRE, UTILE, 1, "filet-1"))

    # ── En-tête du schéma, puis les trois registres qu'il découpe ────────────
    mono(MARGE, Y_ENTETE, q["entete"], UTILE, "en-tête schéma")
    mono(FR_X_LIB, FR_Y_REGISTRES, q["registres"]["service"],
         FR_X_LIB_FIN - FR_X_LIB, "registre service")
    mono(FR_XH0, FR_Y_REGISTRES, q["registres"]["hall"], FR_XH1 - FR_XH0,
         "registre hall")
    mono(FR_XB0, FR_Y_REGISTRES, q["registres"]["bureaux"], FR_XB1 - FR_XB0,
         "registre bureaux")

    # ── Les quatre rangs ─────────────────────────────────────────────────────
    releves = []
    for T, rang in zip(FR_T, rangs):
        y_plaf = T + FR_D_PLAFOND
        y_pied = T + FR_D_PIED
        y_sol = T + FR_D_SOL

        # Le service, dans la colonne de gauche.
        controler(f'{rang["cle"]} libellé', rang["libelle"], 15, "sans-400",
                  FR_X_LIB_FIN - FR_X_LIB)
        A(texte(FR_X_LIB, T + FR_D_LIB, rang["libelle"], "sans", 15, 400,
                "encre", wdth=100))
        mono(FR_X_LIB, T + FR_D_LIB_MONO, rang["libelle_detail"],
             FR_X_LIB_FIN - FR_X_LIB, f'{rang["cle"]} détail de libellé')

        # ── Côté hall ───────────────────────────────────────────────────────
        h = rang["hall"]
        if h["motif"] == "gaine":
            A(rect_bord(FR_XH0, T + 16, FR_BLOC_L, FR_BLOC_H, "calcaire",
                        "filet-1"))
            controler(f'{rang["cle"]} machine hall', h["machine"], 13,
                      "sans-600", FR_BLOC_L - 16)
            A(texte(FR_XH0 + FR_BLOC_L / 2, T + 41, h["machine"], "sans", 13,
                    600, "encre", wdth=112, ancre="middle"))
            xs = [FR_XH0 + FR_BLOC_L + 72 + 68 * k for k in range(3)]
            _fr_gaine(A, FR_XH0 + FR_BLOC_L, FR_XH1, T + 26, T + 40, xs)
            releves.append(f'{rang["cle"]} hall : gaine {FR_XH0 + FR_BLOC_L}'
                           f'–{FR_XH1}, {len(xs)} soufflages')
        elif h["motif"] == "descentes":
            A(ligne(FR_XH0, y_plaf, FR_XH1, y_plaf, "encre", 1.8))
            sabot = h.get("sabot", "tick")
            xs, pas = _fr_descentes(A, FR_XH0, FR_XH1, y_plaf, y_pied,
                                    sabot=sabot)
            if h.get("niveau"):
                _fr_pointille(A, FR_XH0, FR_XH1, y_pied + 8, "filet-1", 1.0)
            A(ligne(FR_XH0, y_sol, FR_XH1, y_sol, "filet-1", 1.2))
            releves.append(f'{rang["cle"]} hall : {len(xs)} descentes au pas '
                           f'de {pas:.1f} px, sabot « {sabot} », plafond y '
                           f'{y_plaf}, pied y {y_pied}'
                           + (f', niveau interrompu y {y_pied + 8}'
                              if h.get("niveau") else '')
                           + f', sol y {y_sol}')
        elif h["motif"] == "bordure":
            A(ligne(FR_XH0, y_sol, FR_XH1, y_sol, "encre", 1.8))
            xs = [FR_XH0 + 20, FR_XH1 - 20 - FR_CHARGE_L]
            # Les deux légendes s'ancrent SUR le bord extérieur de leur bloc,
            # jamais au centre : centrées, elles débordaient de la colonne du
            # hall des deux côtés (relevé au rendu à 1152 px).
            ancres = ("start", "end")
            for x, bloc, ancrage in zip(xs, h["blocs"], ancres):
                A(rect(x, y_sol - FR_CHARGE_H, FR_CHARGE_L, FR_CHARGE_H,
                       "encre"))
                controler(f'{rang["cle"]} {bloc["cle"]} valeur', bloc["valeur"],
                          10, "mono", FR_CHARGE_L - 8, 10 * 0.14)
                A(texte(x + FR_CHARGE_L / 2, y_sol - 9, bloc["valeur"], "mono",
                        10, 500, "voile", ancre="middle", tracking=10 * 0.14,
                        tabulaire=True))
                mono(x if ancrage == "start" else x + FR_CHARGE_L,
                     T + FR_D_MONO1, bloc["libelle"], FR_XH1 - FR_XH0,
                     f'{rang["cle"]} {bloc["cle"]} libellé', ancre=ancrage)
            releves.append(f'{rang["cle"]} hall : deux blocs de charge '
                           f'{FR_CHARGE_L} x {FR_CHARGE_H} px posés sur le sol '
                           f'y {y_sol}, en bordure (x {xs[0]:.0f} et '
                           f'{xs[1]:.0f})')

        for k, l in enumerate(h["detail"]):
            mono(FR_XH0, T + (FR_D_MONO1 if h["motif"] != "bordure"
                              else FR_D_MONO2) + k * 14, l, FR_XH1 - FR_XH0,
                 f'{rang["cle"]} hall détail {k + 1}')

        # ── Côté bureaux ────────────────────────────────────────────────────
        b = rang["bureaux"]
        if b["motif"] == "gaine":
            A(rect_bord(FR_XB0, T + 16, FR_BLOC_L, FR_BLOC_H, "calcaire",
                        "filet-1"))
            controler(f'{rang["cle"]} machine bureaux', b["machine"], 13,
                      "sans-600", FR_BLOC_L - 16)
            A(texte(FR_XB0 + FR_BLOC_L / 2, T + 41, b["machine"], "sans", 13,
                    600, "encre", wdth=112, ancre="middle"))
            xs = [FR_XB0 + FR_BLOC_L + 72 + 68 * k for k in range(3)]
            _fr_gaine(A, FR_XB0 + FR_BLOC_L, FR_XB1, T + 26, T + 40, xs)
        elif b["motif"] == "montees":
            A(ligne(FR_XB0, y_sol, FR_XB1, y_sol, "encre", 1.8))
            xs, pas = _fr_montees(A, FR_XB0, FR_XB1, y_sol, T + 34)
            releves.append(f'{rang["cle"]} bureaux : {len(xs)} montées au pas '
                           f'de {pas:.1f} px depuis le sol y {y_sol} — sens '
                           f'inverse du hall')
        elif b["motif"] == "absence":
            _fr_croix(A, (FR_XB0 + FR_XB1) / 2, T + 40)
            releves.append(f'{rang["cle"]} bureaux : croix — le programme y '
                           f'écrit « sans objet »')

        for k, l in enumerate(b["detail"]):
            if b["motif"] == "absence":
                mono((FR_XB0 + FR_XB1) / 2, T + FR_D_MONO1 + k * 14, l,
                     FR_XB1 - FR_XB0, f'{rang["cle"]} bureaux détail {k + 1}',
                     ancre="middle")
            else:
                mono(FR_XB0, T + FR_D_MONO1 + k * 14, l, FR_XB1 - FR_XB0,
                     f'{rang["cle"]} bureaux détail {k + 1}')

    # ── La frontière, posée par-dessus tout le reste ─────────────────────────
    A(rect(FR_X_MUR, FR_MUR_Y0, FR_EP_MUR, FR_MUR_Y1 - FR_MUR_Y0, "encre"))
    mono(FR_X_MUR + FR_EP_MUR / 2, FR_Y_MUR_LIB, q["mur"], UTILE,
         "libellé du mur", ancre="middle", couleur="encre")

    # ── Phrase de principe et cartouche ──────────────────────────────────────
    l_phrase = controler("phrase de principe", donnees["phrase_principe"], 17,
                         "sans-400", UTILE)
    A(texte(MARGE, Y_PHRASE, donnees["phrase_principe"], "sans", 17, 400,
            "encre", wdth=100))
    libelle = donnees["cartouche_legende"]
    largeur = min(600,
                  round(mesurer(libelle, 11, "mono", tracking=11 * 0.14) + 40))
    A(rect(MARGE, Y_CARTOUCHE, largeur, H_CARTOUCHE, "profond"))
    A(texte(MARGE + 20, Y_CARTOUCHE + 20, libelle, "mono", 11, 500, "voile",
            tracking=11 * 0.14))

    A("</svg>")

    absences = sum(1 for r in rangs if r["bureaux"]["motif"] == "absence")
    controles = {
        "gabarit": f"{W} x {H} — rapport {W/H:.4f} (3:2 exact)",
        "demonstration": "trois registres — le service, le hall, les bureaux — "
                         "séparés par un mur plein posé à x "
                         f"{FR_X_MUR} ; quatre rangs de desserte ; au rang du "
                         "220 V les piquages DESCENDENT du plafond à gauche et "
                         "MONTENT du sol à droite, sens strictement inversés ; "
                         f"les {absences} derniers rangs n’ont pas de côté "
                         "droit et portent une croix doublée du mot ; au "
                         "dernier rang la puissance de charge est le seul "
                         "service qui arrive du SOL dans le hall, en deux blocs "
                         "pleins posés en bordure — texte masqué, l’inversion "
                         "et l’interruption de la colonne de droite se lisent",
        "topologie": " ; ".join(releves),
        "registres": f'service x {FR_X_LIB}–{FR_X_LIB_FIN} · hall x {FR_XH0}–'
                     f'{FR_XH1} · mur x {FR_X_MUR}–{FR_X_MUR + FR_EP_MUR} '
                     f'(y {FR_MUR_Y0}–{FR_MUR_Y1}) · bureaux x {FR_XB0}–'
                     f'{FR_XB1}',
        "rangs": " ; ".join(f'{r["cle"]} y {t}–{t + FR_D_MONO2}'
                            for t, r in zip(FR_T, rangs)),
        "chiffre_unique": "aucun chiffre de relevé — la démonstration n’est pas "
                          "chiffrée (révision 4) ; les valeurs de desserte "
                          "restent au mono 10 pivot, sauf les deux points de "
                          "charge, en voile sur leur bloc d’encre",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l’échelle "
                         f"0,96 (1152 / {W})",
        "bas_du_dessin": f"dernier rang jusqu’à y {FR_T[-1] + FR_D_MONO2}, mur "
                         f"jusqu’à y {FR_MUR_Y1}, son libellé à y "
                         f"{FR_Y_MUR_LIB}, phrase à y {Y_PHRASE}, cartouche "
                         f"{Y_CARTOUCHE}–{Y_CARTOUCHE + H_CARTOUCHE}, marge "
                         f"basse {H - (Y_CARTOUCHE + H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur * H_CARTOUCHE} px², soit "
                            f"{largeur * H_CARTOUCHE / (W * H) * 100:.2f} % "
                            f"de la planche",
        "phrase_principe": f"{len(donnees['phrase_principe'])} signes — "
                           f"{l_phrase:.0f} px mesurés pour {UTILE} disponibles",
        "depassements": depassements if depassements
                        else "aucun — toutes les lignes mesurées sous leur colonne",
    }
    return "\n".join(out) + "\n", controles


# ── La vignette : deux rangs seulement — l'inversion, puis l'absence ─────────
FR_V_X_MUR = 168
FR_V_XG0, FR_V_XG1 = V_MARGE, 160
FR_V_XD0, FR_V_XD1 = 176, VW - V_MARGE
FR_V_Y_REG = 44
FR_V_A_PLAF, FR_V_A_PIED, FR_V_A_SOL = 58, 80, 92
FR_V_Y_MONO_A = 108
FR_V_B_SOL = 148
FR_V_CHARGE_L, FR_V_CHARGE_H = 52, 18
FR_V_Y_PIED = 180


def composer_vignette_frontiere(donnees):
    """Ce qu'elle garde : le mur, l'inversion des piquages, les deux blocs de
    charge et la croix. Ce qu'elle laisse : les quatre rangs nommés, les
    machines de traitement d'air, les détails de desserte — six libellés dans
    300 px ne se lisent pas."""
    q = donnees["frontiere"]
    v = q["vignette"]
    out = []
    A = out.append

    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" '
      f'focusable="false" style="width:100%;height:auto;display:block">')
    entete_style(A)
    A(rect(0, 0, VW, VH, "papier"))

    A(texte(V_MARGE, 26, donnees["vignette_surtitre"], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))
    A(texte(V_MARGE, FR_V_Y_REG, v["hall"], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))
    A(texte(FR_V_XD0, FR_V_Y_REG, v["bureaux"], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    # Rang A — l'inversion.
    A(ligne(FR_V_XG0, FR_V_A_PLAF, FR_V_XG1, FR_V_A_PLAF, "encre", 1.6))
    xs_d, pas_d = _fr_descentes(A, FR_V_XG0, FR_V_XG1, FR_V_A_PLAF,
                                FR_V_A_PIED, n=4, tick=4)
    A(ligne(FR_V_XG0, FR_V_A_SOL, FR_V_XG1, FR_V_A_SOL, "filet-1", 1.1))
    A(ligne(FR_V_XD0, FR_V_A_SOL, FR_V_XD1, FR_V_A_SOL, "encre", 1.6))
    xs_m, pas_m = _fr_montees(A, FR_V_XD0, FR_V_XD1, FR_V_A_SOL,
                              FR_V_A_PIED - 8, n=3, tick=4)
    A(texte(V_MARGE, FR_V_Y_MONO_A, v["rang_a"]["hall"], "mono", 9, 500,
            "pivot", tracking=9 * 0.14))
    A(texte(FR_V_XD0, FR_V_Y_MONO_A, v["rang_a"]["bureaux"], "mono", 9, 500,
            "pivot", tracking=9 * 0.14))

    # Rang B — l'absence, et la puissance qui vient du sol.
    A(ligne(FR_V_XG0, FR_V_B_SOL, FR_V_XG1, FR_V_B_SOL, "encre", 1.6))
    for x in (FR_V_XG0 + 4, FR_V_XG1 - 4 - FR_V_CHARGE_L):
        A(rect(x, FR_V_B_SOL - FR_V_CHARGE_H, FR_V_CHARGE_L, FR_V_CHARGE_H,
               "encre"))
        A(texte(x + FR_V_CHARGE_L / 2, FR_V_B_SOL - 5, v["rang_b"]["valeur"],
                "mono", 9, 500, "voile", ancre="middle", tracking=9 * 0.14,
                tabulaire=True))
    _fr_croix(A, (FR_V_XD0 + FR_V_XD1) / 2, FR_V_B_SOL - 12, bras=13,
              epaisseur=1.6)

    A(texte(V_MARGE, FR_V_Y_PIED, v["pied"], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    A(rect(FR_V_X_MUR, 50, 3.5, 120, "encre"))
    A("</svg>")

    l_pied = mesurer(v["pied"], 9, "mono", 9 * 0.14)
    controles = {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": "vignette servie à 274-296 px dans une carte — "
                            f"échelle {274/VW:.2f} à {296/VW:.2f}, jamais "
                            "au-dessus de 1,00",
        "corps_minimal": "9 px dans le repère — rendu à 8,2 px à l’échelle "
                         "0,91, à 8,9 px à 0,99",
        "motif": f"mur à x {FR_V_X_MUR} ; rang A — {len(xs_d)} descentes au pas "
                 f"de {pas_d:.1f} px à gauche contre {len(xs_m)} montées au pas "
                 f"de {pas_m:.1f} px à droite, sens inversés ; rang B — deux "
                 f"blocs de charge posés sur le sol à gauche, croix à droite",
        "pied": f'« {v["pied"]} » — {l_pied:.0f} px pour '
                f'{FR_V_XD1 - V_MARGE} disponibles',
        "marges": f"aucun trait sous x {V_MARGE} ni au-delà de x "
                  f"{FR_V_XD1} ; ligne de pied à y {FR_V_Y_PIED} pour "
                  f"{VH - V_MARGE} de bas de cadre",
    }
    return "\n".join(out) + "\n", controles


# ── L'appui : les quatre rangs, un mono par côté, sans phrase ni cartouche ───
FR_A_X_MUR = 286
FR_A_XG0, FR_A_XG1 = A_MARGE, 278
FR_A_XD0, FR_A_XD1 = 296, AW - A_MARGE
FR_A_Y_REG = 62
FR_A_T = (76, 138, 200, 262)
FR_A_CHARGE_L, FR_A_CHARGE_H = 56, 20
FR_A_BLOC_L, FR_A_BLOC_H = 76, 28


def composer_appui_frontiere(donnees):
    q = donnees["frontiere"]
    a = q["appui"]
    out = []
    A = out.append
    racine_appui(A, donnees)

    A(texte(FR_A_XG0, FR_A_Y_REG, a["hall"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    A(texte(FR_A_XD0, FR_A_Y_REG, a["bureaux"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

    for T, rang in zip(FR_A_T, a["rangs"]):
        y_plaf, y_pied, y_sol = T + 10, T + 30, T + 40
        if rang["motif"] == "gaine":
            A(rect_bord(FR_A_XG0, T + 6, FR_A_BLOC_L, FR_A_BLOC_H, "calcaire",
                        "filet-1"))
            A(texte(FR_A_XG0 + FR_A_BLOC_L / 2, T + 25, rang["machine_hall"],
                    "sans", 12, 600, "encre", wdth=112, ancre="middle"))
            _fr_gaine(A, FR_A_XG0 + FR_A_BLOC_L, FR_A_XG1, T + 12, T + 24,
                      [FR_A_XG0 + FR_A_BLOC_L + 60])
            A(rect_bord(FR_A_XD0, T + 6, FR_A_BLOC_L, FR_A_BLOC_H, "calcaire",
                        "filet-1"))
            A(texte(FR_A_XD0 + FR_A_BLOC_L / 2, T + 25, rang["machine_bureaux"],
                    "sans", 12, 600, "encre", wdth=112, ancre="middle"))
            _fr_gaine(A, FR_A_XD0 + FR_A_BLOC_L, FR_A_XD1, T + 12, T + 24,
                      [FR_A_XD0 + FR_A_BLOC_L + 60])
        elif rang["motif"] == "inversion":
            A(ligne(FR_A_XG0, y_plaf, FR_A_XG1, y_plaf, "encre", 1.6))
            _fr_descentes(A, FR_A_XG0, FR_A_XG1, y_plaf, y_pied, n=4, tick=4)
            A(ligne(FR_A_XG0, y_sol, FR_A_XG1, y_sol, "filet-1", 1.1))
            A(ligne(FR_A_XD0, y_sol, FR_A_XD1, y_sol, "encre", 1.6))
            _fr_montees(A, FR_A_XD0, FR_A_XD1, y_sol, T + 20, n=3, tick=4)
        elif rang["motif"] == "descentes_absence":
            A(ligne(FR_A_XG0, y_plaf, FR_A_XG1, y_plaf, "encre", 1.6))
            _fr_descentes(A, FR_A_XG0, FR_A_XG1, y_plaf, y_pied, n=4, tick=4,
                          sabot="vanne")
            _fr_pointille(A, FR_A_XG0, FR_A_XG1, y_pied + 6, "filet-1", 1.0,
                          pas=8, plein=4)
            A(ligne(FR_A_XG0, y_sol, FR_A_XG1, y_sol, "filet-1", 1.1))
            _fr_croix(A, (FR_A_XD0 + FR_A_XD1) / 2, T + 24, bras=12,
                      epaisseur=1.6)
        elif rang["motif"] == "bordure_absence":
            A(ligne(FR_A_XG0, y_sol, FR_A_XG1, y_sol, "encre", 1.6))
            for x in (FR_A_XG0 + 6, FR_A_XG1 - 6 - FR_A_CHARGE_L):
                A(rect(x, y_sol - FR_A_CHARGE_H, FR_A_CHARGE_L,
                       FR_A_CHARGE_H, "encre"))
                A(texte(x + FR_A_CHARGE_L / 2, y_sol - 6, rang["valeur"],
                        "mono", 10, 500, "voile", ancre="middle",
                        tracking=10 * 0.14, tabulaire=True))
            _fr_croix(A, (FR_A_XD0 + FR_A_XD1) / 2, T + 24, bras=12,
                      epaisseur=1.6)

        A(texte(FR_A_XG0, T + 54, rang["hall"], "mono", 10, 500, "pivot",
                tracking=10 * 0.14))
        A(texte(FR_A_XD0, T + 54, rang["bureaux"], "mono", 10, 500, "pivot",
                tracking=10 * 0.14))

    A(rect(FR_A_X_MUR, 70, 3, 250, "encre"))
    A("</svg>")

    largeurs = [(r["cle"], mesurer(r["hall"], 10, "mono", 10 * 0.14),
                 mesurer(r["bureaux"], 10, "mono", 10 * 0.14))
                for r in a["rangs"]]
    trop = [f"{c} : {lg:.0f} / {ld:.0f} px" for c, lg, ld in largeurs
            if lg > FR_A_XG1 - FR_A_XG0 or ld > FR_A_XD1 - FR_A_XD0]
    controles = controles_appui(
        f"quatre rangs à y {FR_A_T}, mur plein à x {FR_A_X_MUR} ; l’inversion "
        f"des piquages au rang 2 et les deux croix des rangs 3 et 4 portent "
        f"seules la démonstration",
        f"dernier mono à y {FR_A_T[-1] + 54}, mur jusqu’à y 320, marge basse "
        f"{AH - 320} px",
        colonnes=f"hall x {FR_A_XG0}–{FR_A_XG1} ({FR_A_XG1 - FR_A_XG0} px) · "
                 f"bureaux x {FR_A_XD0}–{FR_A_XD1} ({FR_A_XD1 - FR_A_XD0} px)",
        depassements=trop if trop else "aucun — les huit monos tiennent dans "
                                       "leur colonne",
    )
    return "\n".join(out) + "\n", controles

# ── `amorce` : l'épine construite entière, les postes à moitié pleins ───────
# Le mécanisme de la N19 (groupe scolaire de La Flotte-en-Ré). Une seule
# primitive, appelée par les TROIS formats et par les TROIS rangs : une épine
# pleine — jeu de barres, platelage, tronc enterré — et n postes dont les
# `poses` premiers sont pleins, les suivants interrompus. Le pas et les centres
# sont DÉRIVÉS de n, jamais choisis format par format ni rang par rang : c'est
# ce qui interdit aux trois dessins de diverger.
AM_X_LIB, AM_X_LIB_FIN = MARGE, 236
AM_X0, AM_X1 = 256, W - MARGE
AM_T = (232, 376, 520)
AM_SRC_L, AM_SRC_H = 156, 44
AM_ECART_SRC = 40
AM_D_EPINE = 34
AM_D_PIED_POSTE = 76
AM_D_ETIQ, AM_D_ETIQ2, AM_D_PIED = 96, 110, 128
AM_D_SEP = 144
AM_MACHINE_L, AM_MACHINE_H = 56, 30
AM_DECK_Y0, AM_DECK_Y1 = 22, 76
AM_CARRE = 15
AM_REGARD = 14
AM_BLOC_L, AM_BLOC_H = 104, 20
AM_SABOT = 9


def _am_centres(x0, x1, n):
    """Les n centres de poste — DÉRIVÉS du seul nombre de postes.

    Unique source de la géométrie horizontale du mécanisme : la planche,
    l'appui et la vignette l'appellent, et les trois rangs aussi. Rien
    d'autre ne place un poste."""
    pas = (x1 - x0) / n
    return [x0 + pas * (k + 0.5) for k in range(n)], pas


def _am_tirets(A, points, cle="encre", epaisseur=1.4, ech=1.0):
    """Le trait de la réserve — un seul motif d'interruption pour tout le
    dessin, de sorte que « interrompu » veuille dire la même chose partout."""
    from _tronc import JETON
    d = "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in points)
    A(f'  <path d="{d}" fill="none" class="s-{cle}" stroke="{JETON[cle]}" '
      f'stroke-width="{epaisseur}" stroke-dasharray="{_am_dash(ech)}"/>')


def _am_dash(ech):
    """Le motif d interruption s echelonne AVEC le dessin.

    A l echelle 0,62 de l appui, un carre de reserve fait 9 px de cote : le
    motif de la planche n y rendait qu un seul tiret par arete, et le carre se
    lisait comme un angle casse. Une seule valeur par FORMAT — jamais par
    glyphe : « interrompu » doit vouloir dire la meme chose partout dans un
    meme dessin."""
    a, b = 7.0 * ech, 5.0 * ech
    return f"{a:.1f} {b:.1f}"


def _am_boite_tirets(A, x, y, w, h, cle="encre", epaisseur=1.3, ech=1.0):
    from _tronc import JETON
    A(f'  <rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
      f'fill="none" class="s-{cle}" stroke="{JETON[cle]}" '
      f'stroke-width="{epaisseur}" stroke-dasharray="{_am_dash(ech)}"/>')


def _am_postes(A, x0, x1, y_epine, rang, ech=1.0):
    """Les n postes d'un rang, pleins jusqu'à `poses`, interrompus ensuite.

    Trois glyphes terminaux — `departs`, `alveoles`, `branches` — mais UNE
    implantation : mêmes centres, même seuil, même motif d'interruption.
    Rend les centres, le pas et l'abscisse de la frontière posé/réservé."""
    n, poses, motif = rang["n"], rang["poses"], rang["motif"]
    centres, pas = _am_centres(x0, x1, n)
    y_pied = y_epine + AM_D_PIED_POSTE * ech - AM_D_EPINE * ech

    if motif == "alveoles":
        # Le platelage est entier : un seul cadre plein, refendu en n travées.
        h = (AM_DECK_Y1 - AM_DECK_Y0) * ech
        y0 = y_epine - 12 * ech
        A(rect_bord(x0, y0, x1 - x0, h, "papier", "filet-1"))
        for k in range(1, n):
            A(ligne(x0 + pas * k, y0, x0 + pas * k, y0 + h, "filet-2", 1.0))
        for k, x in enumerate(centres):
            if k < poses:
                mw, mh = AM_MACHINE_L * ech, AM_MACHINE_H * ech
                A(rect_bord(x - mw / 2, y0 + (h - mh) / 2, mw, mh,
                            "calcaire", "filet-1"))
                A(cercle(x, y0 + h / 2, 7 * ech, "papier", "encre", 1.3))
            else:
                mw, mh = AM_MACHINE_L * ech, AM_MACHINE_H * ech
                _am_boite_tirets(A, x - mw / 2, y0 + (h - mh) / 2, mw, mh, ech=ech)
        return centres, pas, x0 + pas * poses

    for k, x in enumerate(centres):
        if motif == "departs":
            if k < poses:
                A(ligne(x, y_epine, x, y_pied, "encre", 1.6))
                A(ligne(x - AM_SABOT * ech, y_pied, x + AM_SABOT * ech, y_pied,
                        "encre", 2.0))
            else:
                _am_tirets(A, [(x, y_epine), (x, y_pied - AM_CARRE * ech)],
                           ech=ech)
                c = AM_CARRE * ech
                _am_boite_tirets(A, x - c / 2, y_pied - c, c, c, ech=ech)
        else:  # branches
            if k < poses:
                A(ligne(x, y_epine, x, y_pied - AM_BLOC_H * ech, "encre", 1.9))
                bw, bh = AM_BLOC_L * ech, AM_BLOC_H * ech
                A(rect_bord(x - bw / 2, y_pied - bh, bw, bh, "calcaire",
                            "filet-1"))
            else:
                # Le regard est PLEIN — il est construit ; seul ce qui le
                # dépasse est interrompu. C'est l'arbitrage qui porte la thèse :
                # une réserve n'est pas un vide, c'est un ouvrage qui attend.
                r = AM_REGARD * ech
                y_reg = y_epine + (y_pied - y_epine) * 0.42
                A(ligne(x, y_epine, x, y_reg, "encre", 1.6))
                A(rect_bord(x - r / 2, y_reg, r, r, "papier", "encre"))
                _am_tirets(A, [(x, y_reg + r), (x, y_pied + 10 * ech)], ech=ech)
    return centres, pas, x0 + pas * poses


def composer_amorce(donnees):
    q = donnees["amorce"]
    rangs = q["rangs"]
    out = []
    A = out.append
    trop = []

    def controler(nom, chaine, corps, profil, dispo, tracking=0.0):
        l = mesurer(chaine, corps, profil, tracking)
        if l > dispo:
            trop.append(f"{nom} : {l:.0f} px pour {dispo:.0f}")
        return l

    def mono(x, y, chaine, dispo, nom, ancre=None, couleur="pivot", corps=10,
             tab=False):
        controler(nom, chaine, corps, "mono", dispo, corps * 0.14)
        A(texte(x, y, chaine, "mono", corps, 500, couleur, ancre=ancre,
                tracking=corps * 0.14, tabulaire=tab))

    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
      f'preserveAspectRatio="xMidYMid meet" role="img" '
      f'style="width:100%;height:auto;display:block" '
      f'aria-label="{echapper(donnees["aria_label"])}">')
    entete_style(A)
    A(rect(0, 0, W, H, "papier"))

    A(texte(MARGE, Y_SURTITRE, donnees["surtitre"], "mono", 11, 500, "pivot",
            tracking=11 * 0.14))
    controler("surtitre", donnees["surtitre"], 11, "mono", UTILE, 11 * 0.14)
    A(texte(MARGE, Y_TITRE, donnees["titre"], "sans", 30, 700, "encre",
            wdth=112))
    controler("titre", donnees["titre"], 30, "sans-700", UTILE)
    A(texte(MARGE, Y_SOUSTITRE, donnees["sous_titre"], "sans", 16, 400,
            "pivot", wdth=100))
    controler("sous-titre", donnees["sous_titre"], 16, "sans-400", UTILE)
    A(rect(MARGE, Y_FILET_TITRE, UTILE, 1, "filet-1"))
    mono(MARGE, Y_ENTETE, q["entete"], UTILE, "en-tête schéma")

    releves = []
    for T, rang in zip(AM_T, rangs):
        # Colonne de gauche : le rang et sa raison.
        controler(f'{rang["cle"]} libellé', rang["libelle"], 15, "sans-400",
                  AM_X_LIB_FIN - AM_X_LIB)
        A(texte(AM_X_LIB, T + 30, rang["libelle"], "sans", 15, 400, "encre",
                wdth=100))
        mono(AM_X_LIB, T + 50, rang["libelle_detail"],
             AM_X_LIB_FIN - AM_X_LIB, f'{rang["cle"]} raison')

        # Le bloc qui nomme l'épine, puis l'épine elle-même — toujours pleine.
        y_ep = T + AM_D_EPINE
        A(rect_bord(AM_X0, T + 12, AM_SRC_L, AM_SRC_H, "calcaire", "filet-1"))
        controler(f'{rang["cle"]} source', rang["source"]["titre"], 10, "mono",
                  AM_SRC_L - 16, 10 * 0.14)
        A(texte(AM_X0 + AM_SRC_L / 2, T + 30, rang["source"]["titre"], "mono",
                10, 500, "pivot", ancre="middle", tracking=10 * 0.14))
        controler(f'{rang["cle"]} valeur', rang["source"]["valeur"], 13,
                  "sans-600", AM_SRC_L - 16)
        A(texte(AM_X0 + AM_SRC_L / 2, T + 48, rang["source"]["valeur"], "sans",
                13, 600, "encre", wdth=112, ancre="middle"))

        x_deb = AM_X0 + AM_SRC_L + AM_ECART_SRC
        ep = 2.6 if rang["motif"] == "branches" else 1.8
        A(ligne(AM_X0 + AM_SRC_L, y_ep, x_deb, y_ep, "encre", ep))
        if rang["motif"] != "alveoles":
            A(ligne(x_deb, y_ep, AM_X1, y_ep, "encre", ep))

        centres, pas, x_front = _am_postes(A, x_deb, AM_X1, y_ep, rang)

        # Le fourreau : un trait fin interrompu qui double le tronc sur toute
        # sa longueur — la réserve qui n'a pas de poste à elle.
        if rang.get("fourreau"):
            # Le fourreau passe AU-DESSUS du tronc, avec son libelle a son
            # extremite droite. Deux essais sous le tronc ont echoue au PNG :
            # ancre a droite il traversait la derniere branche, ancre a gauche
            # il butait sur la boite de la premiere. La bande situee au-dessus
            # du tronc est la seule ou rien ne descend — les branches vont
            # toutes vers le bas. La largeur disponible se mesure contre le
            # BORD des boites, jamais contre le centre des branches : c est
            # l erreur qui avait laisse passer le second essai.
            _am_tirets(A, [(AM_X0 + AM_SRC_L, y_ep - 10), (AM_X1, y_ep - 10)],
                       "filet-1", 1.2)
            mono(AM_X1, y_ep - 17, rang["fourreau"],
                 AM_X1 - (AM_X0 + AM_SRC_L), f'{rang["cle"]} fourreau',
                 ancre="end")

        largeur_poste = pas - 10
        for k, x in enumerate(centres):
            mono(x, T + AM_D_ETIQ, rang["etiquettes"][k], largeur_poste,
                 f'{rang["cle"]} étiquette {k + 1}', ancre="middle",
                 couleur="encre" if k < rang["poses"] else "pivot")
            if rang.get("terminaux"):
                mono(x, T + AM_D_ETIQ2, rang["terminaux"][k], largeur_poste,
                     f'{rang["cle"]} terminal {k + 1}', ancre="middle")

        mono(AM_X0, T + AM_D_PIED, rang["pied"], AM_X1 - AM_X0,
             f'{rang["cle"]} pied')
        if T != AM_T[-1]:
            A(rect(AM_X_LIB, T + AM_D_SEP, UTILE, 1, "filet-3"))

        releves.append(
            f'{rang["cle"]} — {rang["n"]} postes au pas de {pas:.1f} px sur '
            f'x {x_deb:.0f}–{AM_X1}, {rang["poses"]} pleins puis '
            f'{rang["n"] - rang["poses"]} interrompus, frontière x '
            f'{x_front:.0f} ({rang["poses"] / rang["n"] * 100:.0f} % du rang)')

    l_phrase = controler("phrase de principe", donnees["phrase_principe"], 17,
                         "sans-400", UTILE)
    A(texte(MARGE, Y_PHRASE, donnees["phrase_principe"], "sans", 17, 400,
            "encre", wdth=100))
    libelle = donnees["cartouche_legende"]
    largeur = min(600,
                  round(mesurer(libelle, 11, "mono", tracking=11 * 0.14) + 40))
    A(rect(MARGE, Y_CARTOUCHE, largeur, H_CARTOUCHE, "profond"))
    A(texte(MARGE + 20, Y_CARTOUCHE + 20, libelle, "mono", 11, 500, "voile",
            tracking=11 * 0.14))
    A("</svg>")

    assert not trop, "dépassements sur la planche : " + " ; ".join(trop)

    ratios = " · ".join(f'{r["poses"]}/{r["n"]}' for r in rangs)
    controles = {
        "gabarit": f"{W} x {H} — rapport {W/H:.4f} (3:2 exact)",
        "demonstration": "trois rangs, une seule primitive — une épine pleine "
                         "construite à sa taille définitive, et n postes dont "
                         "les premiers sont pleins et les suivants "
                         f"interrompus ; la partition se répète : {ratios}. "
                         "Au troisième rang le regard de vannes est PLEIN (il "
                         "est construit) et seul le tracé qui le dépasse est "
                         "interrompu, et s’arrête dans le vide — c’est "
                         "l’amorce. Texte masqué, la moitié droite de chaque "
                         "rang se lit comme non encore posée",
        "primitive_partagee": "_am_centres(x0, x1, n) — pas = (x1 - x0) / n, "
                              "centre k = x0 + pas (k + 0,5) ; appelée par les "
                              "trois rangs ET par les trois formats, aucune "
                              "abscisse de poste n’est écrite à la main",
        "topologie": " ; ".join(releves),
        "chiffre_unique": "aucun chiffre de relevé — la démonstration n’est pas "
                          "chiffrée (révision 4) ; les seules valeurs sont les "
                          "trois libellés d’épine, en Archivo 13",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l’échelle "
                         f"0,96 (1152 / {W})",
        "bas_du_dessin": f"dernier pied à y {AM_T[-1] + AM_D_PIED}, phrase à y "
                         f"{Y_PHRASE}, cartouche {Y_CARTOUCHE}–"
                         f"{Y_CARTOUCHE + H_CARTOUCHE}, marge basse "
                         f"{H - (Y_CARTOUCHE + H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur * H_CARTOUCHE / (W * H) * 100:.2f} % "
                            "de la planche",
        "phrase_principe": f"{len(donnees['phrase_principe'])} signes — "
                           f"{l_phrase:.0f} px pour {UTILE} disponibles",
        "depassements": "aucun — les "
                        f"{sum(2 + r['n'] * (2 if r.get('terminaux') else 1) for r in rangs) + 6} "
                        "chaînes mesurées tiennent sous leur colonne "
                        "(assertion de composition)",
    }
    return "\n".join(out) + "\n", controles


# ── La vignette : deux rangs — les alvéoles, puis les branches ──────────────
AM_V_X0, AM_V_X1 = V_MARGE, VW - V_MARGE
AM_V_YA, AM_V_YB = 58, 128
AM_V_DECK_H = 26
AM_V_BLOC_L, AM_V_BLOC_H = 46, 13
AM_V_REGARD = 9


def composer_vignette_amorce(donnees):
    """Ce qu'elle garde : les quatre alvéoles à moitié pleines et les trois
    branches dont une seule arrive. Ce qu'elle laisse : le rang électrique, les
    libellés de rang, les pieds — treize monos dans 300 px ne se lisent pas."""
    q = donnees["amorce"]
    v = q["vignette"]
    rangs = {r["cle"]: r for r in q["rangs"]}
    out = []
    A = out.append
    trop = []

    def mono(x, y, chaine, dispo, nom, ancre=None, couleur="pivot", corps=9):
        l = mesurer(chaine, corps, "mono", corps * 0.14)
        if l > dispo:
            trop.append(f"{nom} : {l:.0f} px pour {dispo:.0f}")
        A(texte(x, y, chaine, "mono", corps, 500, couleur, ancre=ancre,
                tracking=corps * 0.14))

    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" '
      f'focusable="false" style="width:100%;height:auto;display:block">')
    entete_style(A)
    A(rect(0, 0, VW, VH, "papier"))
    mono(V_MARGE, 26, donnees["vignette_surtitre"], AM_V_X1 - AM_V_X0,
         "surtitre")

    # Rang des alvéoles.
    p = rangs["plateforme"]
    mono(V_MARGE, 44, v["haut"], AM_V_X1 - AM_V_X0, "haut")
    centres_a, pas_a = _am_centres(AM_V_X0, AM_V_X1, p["n"])
    A(rect_bord(AM_V_X0, AM_V_YA, AM_V_X1 - AM_V_X0, AM_V_DECK_H, "papier",
                "filet-1"))
    for k in range(1, p["n"]):
        A(ligne(AM_V_X0 + pas_a * k, AM_V_YA, AM_V_X0 + pas_a * k,
                AM_V_YA + AM_V_DECK_H, "filet-2", 1.0))
    mw, mh = pas_a - 22, AM_V_DECK_H - 10
    for k, x in enumerate(centres_a):
        if k < p["poses"]:
            A(rect_bord(x - mw / 2, AM_V_YA + 5, mw, mh, "calcaire", "filet-1"))
            A(cercle(x, AM_V_YA + AM_V_DECK_H / 2, 4.5, "papier", "encre", 1.2))
        else:
            _am_boite_tirets(A, x - mw / 2, AM_V_YA + 5, mw, mh)

    # Rang des branches.
    r = rangs["reseau"]
    mono(V_MARGE, 114, v["bas"], AM_V_X1 - AM_V_X0, "bas")
    centres_b, pas_b = _am_centres(AM_V_X0, AM_V_X1, r["n"])
    A(ligne(AM_V_X0, AM_V_YB, AM_V_X1, AM_V_YB, "encre", 2.2))
    for k, x in enumerate(centres_b):
        if k < r["poses"]:
            A(ligne(x, AM_V_YB, x, AM_V_YB + 16, "encre", 1.5))
            A(rect_bord(x - AM_V_BLOC_L / 2, AM_V_YB + 16, AM_V_BLOC_L,
                        AM_V_BLOC_H, "calcaire", "filet-1"))
        else:
            y_reg = AM_V_YB + 12
            A(ligne(x, AM_V_YB, x, y_reg, "encre", 1.5))
            A(rect_bord(x - AM_V_REGARD / 2, y_reg, AM_V_REGARD, AM_V_REGARD,
                        "papier", "encre"))
            _am_tirets(A, [(x, y_reg + AM_V_REGARD), (x, AM_V_YB + 38)], "encre",
                       1.2)

    mono(V_MARGE, 180, v["pied"], AM_V_X1 - AM_V_X0, "pied")
    A("</svg>")

    assert not trop, "dépassements sur la vignette : " + " ; ".join(trop)
    return "\n".join(out) + "\n", {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": "vignette servie à 274-296 px dans une carte — "
                            f"échelle {274/VW:.2f} à {296/VW:.2f}, jamais "
                            "au-dessus de 1,00",
        "corps_minimal": "9 px dans le repère — rendu à 8,2 px à l’échelle "
                         "0,91, à 8,9 px à 0,99",
        "motif": f'{p["n"]} alvéoles au pas de {pas_a:.1f} px dont '
                 f'{p["poses"]} pleines ; {r["n"]} branches au pas de '
                 f'{pas_b:.1f} px dont {r["poses"]} arrive à un bloc, les '
                 f'{r["n"] - r["poses"]} autres s’arrêtent après leur regard',
        "primitive_partagee": "_am_centres — les mêmes centres que la planche "
                              "et l’appui, au facteur de largeur près",
        "marges": f"aucun trait sous x {V_MARGE} ni au-delà de x {AM_V_X1} ; "
                  f"pied à y 180 pour {VH - V_MARGE} de bas de cadre",
        "depassements": "aucun — assertion de composition",
    }


# ── L'appui : les trois rangs, sans phrase ni cartouche ────────────────────
AM_A_X_LIB = A_MARGE
AM_A_X0, AM_A_X1 = 150, AW - A_MARGE
AM_A_T = (80, 172, 264)
AM_A_ECH = 0.62


def composer_appui_amorce(donnees):
    q = donnees["amorce"]
    a = q["appui"]
    rangs = {r["cle"]: r for r in q["rangs"]}
    out = []
    A = out.append
    trop = []
    racine_appui(A, donnees)

    for T, meta in zip(AM_A_T, a["rangs"]):
        rang = rangs[meta["cle"]]
        l = mesurer(meta["libelle"], 10, "mono", 10 * 0.14)
        if l > AM_A_X0 - AM_A_X_LIB - 8:
            trop.append(f'{meta["cle"]} libellé : {l:.0f} px')
        A(texte(AM_A_X_LIB, T + 26, meta["libelle"], "mono", 10, 500, "pivot",
                tracking=10 * 0.14))
        y_ep = T + 22
        ep = 2.2 if rang["motif"] == "branches" else 1.6
        if rang["motif"] != "alveoles":
            A(ligne(AM_A_X0, y_ep, AM_A_X1, y_ep, "encre", ep))
        centres, pas, x_front = _am_postes(A, AM_A_X0, AM_A_X1, y_ep, rang,
                                           ech=AM_A_ECH)

    A("</svg>")
    assert not trop, "dépassements sur l’appui : " + " ; ".join(trop)

    ratios = " · ".join(f'{rangs[m["cle"]]["poses"]}/{rangs[m["cle"]]["n"]}'
                        for m in a["rangs"])
    return "\n".join(out) + "\n", controles_appui(
        f"trois rangs à y {AM_A_T} — même primitive qu’à la planche, à "
        f"l’échelle {AM_A_ECH} ; la partition {ratios} se répète et porte "
        "seule la démonstration",
        f"dernier rang jusqu’à y {AM_A_T[-1] + 70}, marge basse "
        f"{AH - (AM_A_T[-1] + 70)} px",
        colonnes=f"libellés x {AM_A_X_LIB}–{AM_A_X0 - 8} · dessin x "
                 f"{AM_A_X0}–{AM_A_X1} ({AM_A_X1 - AM_A_X0} px)",
        depassements="aucun — assertion de composition",
    )



# ── `exposition` : le plan de toiture comme frontière ──────────────────────
# Le mécanisme de la N20 (Maison des Métiers, La Rochelle). Un seul critère
# trie les organes d'une production de toiture sur un site littoral : doivent-
# ils être dehors ? Deux régimes en découlent, et UNE implantation les dessine
# tous les deux — `_ex_organe` reçoit la géométrie de son format dans `g`, et
# rien d'autre ne place une boîte, un capot, un plot ni une flèche.
#
# Deux grandeurs y sont soigneusement distinguées, et c'est la leçon de la N19 :
#   · les MESURES du dessin (l, h, y…) sont ABSOLUES, propres à chaque format —
#     une boîte de vignette n'est pas une boîte de planche réduite ;
#   · l'ÉCHELLE `ech` ne commande que les MOTIFS et les petits accessoires
#     (interruption, pointe de flèche, plot, brèche du plan), de sorte que
#     « interrompu » veuille dire la même chose dans les trois dessins.
# Les abscisses viennent de `_am_centres`, déjà partagée : deux mécanismes qui
# rangent n objets sur une largeur n'ont aucune raison de le faire deux fois.
EX_X0, EX_X1 = MARGE, W - MARGE
EX_Y_BANDE_H = 226
EX_Y_LIB_LIAISON_H, EX_Y_LIAISON_H = 244, 252
EX_Y_TOIT = 440
EX_Y_LIB_TOIT = 432
EX_Y_BANDE_B = 474
EX_Y_LIB_LIAISON_B, EX_Y_LIAISON_B = 628, 634
EX_Y_PIED = 660
EX_Y_ENCEINTE0, EX_Y_ENCEINTE1 = 462, 648
EX_EP_TOIT = 6                # écart des deux traits de la terrasse
EX_BRECHE = 30                # brèche du plan au droit d'une traversée
EX_PLOT = 8

# La géométrie d'un format : les seules mesures que `_ex_organe` consulte.
EX_G = dict(l=150, h=44, y_haut=286, y_bas=492, d_capot=18, h_capot=9,
            ech=1.0)


def _ex_toiture(A, x0, x1, y, breches, ech=1.0, epaisseur=1.8):
    """Le plan de toiture — deux traits parallèles, interrompus au droit de
    chaque traversée. La brèche EST la traversée : c'est la convention de
    coupe, et elle vaut pour les trois formats."""
    b = EX_BRECHE * ech
    bords = [x0]
    for cx in sorted(breches):
        bords += [cx - b / 2, cx + b / 2]
    bords.append(x1)
    for dy in (0, EX_EP_TOIT * ech):
        for k in range(0, len(bords), 2):
            xa, xb = bords[k], bords[k + 1]
            if xb - xa > 1:
                A(ligne(xa, y + dy, xb, y + dy, "encre", epaisseur))


def _ex_organe(A, cx, org, g):
    """Un organe et son régime, à l'abscisse cx.

    `dehors` — la boîte reste au-dessus du plan et reçoit ses protections
    (capot posé sur elle, grillage anti-volatiles, plots de surélévation).
    `descend` — une boîte interrompue marque la position abandonnée, une
    flèche traverse le plan, la boîte pleine est en dessous.

    Rend l'ordonnée du bas de la boîte pleine — la base des libellés — et,
    pour un organe qui descend, l'abscisse de sa traversée."""
    ech, L, Hb = g["ech"], g["l"], g["h"]
    x = cx - L / 2
    descend = org["regime"] == "descend"
    y_boite = g["y_bas"] if descend else g["y_haut"]

    if descend:
        _am_boite_tirets(A, x, g["y_haut"], L, Hb, ech=ech)
        y0 = g["y_haut"] + Hb + 6 * ech
        y1 = y_boite - 6 * ech
        A(ligne(cx, y0, cx, y1 - 9 * ech, "encre", 2.0 * max(ech, 0.7)))
        A(fleche(cx, y1, "encre", "bas", 9 * ech))
    else:
        for p in org.get("protections", ()):
            if p == "capot":
                # Un CADRE fermé autour de la machine — « capotage intégral ».
                # Premier essai : une barre posée au-dessus. Vue au PNG, elle
                # se lisait comme une seconde boîte plate et pâle, et non
                # comme une protection ; le grillage de la colonne voisine,
                # lui, se lisait d'emblée. Deux protections doivent différer
                # par autre chose que leur position.
                d = 7 * ech
                A(polyligne([(x - d, g["y_haut"] - d),
                             (x + L + d, g["y_haut"] - d),
                             (x + L + d, g["y_haut"] + Hb + d),
                             (x - d, g["y_haut"] + Hb + d),
                             (x - d, g["y_haut"] - d)], "encre", 1.8 * max(ech, 0.7)))
            elif p == "grille":
                yg = g["y_haut"] - g["d_capot"]
                A(ligne(x, yg, x + L, yg, "encre", 1.4))
                for k in range(7):
                    xt = x + L * (k + 0.5) / 7
                    A(ligne(xt, yg, xt, g["y_haut"], "encre", 1.0))
            elif p == "plots":
                yp = g["y_haut"] + Hb
                c = EX_PLOT * ech
                for s in (-1, 1):
                    A(rect_bord(cx + s * L / 4 - c / 2, yp, c, c, "calcaire",
                                "filet-1"))
                A(ligne(x, yp + c, x + L, yp + c, "encre", 1.6))

    A(rect_bord(x, y_boite, L, Hb, "calcaire", "filet-1"))
    return y_boite + Hb, (cx if descend else None)


def composer_exposition(donnees):
    q = donnees["exposition"]
    organes = q["organes"]
    out = []
    A = out.append
    trop = []

    def controler(nom, chaine, corps, profil, dispo, tracking=0.0):
        l = mesurer(chaine, corps, profil, tracking)
        if l > dispo:
            trop.append(f"{nom} : {l:.0f} px pour {dispo:.0f}")
        return l

    def mono(x, y, chaine, dispo, nom, ancre=None, couleur="pivot", corps=10):
        controler(nom, chaine, corps, "mono", dispo, corps * 0.14)
        A(texte(x, y, chaine, "mono", corps, 500, couleur, ancre=ancre,
                tracking=corps * 0.14))

    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
      f'preserveAspectRatio="xMidYMid meet" role="img" '
      f'style="width:100%;height:auto;display:block" '
      f'aria-label="{echapper(donnees["aria_label"])}">')
    entete_style(A)
    A(rect(0, 0, W, H, "papier"))

    A(texte(MARGE, Y_SURTITRE, donnees["surtitre"], "mono", 11, 500, "pivot",
            tracking=11 * 0.14))
    controler("surtitre", donnees["surtitre"], 11, "mono", UTILE, 11 * 0.14)
    A(texte(MARGE, Y_TITRE, donnees["titre"], "sans", 30, 700, "encre",
            wdth=112))
    controler("titre", donnees["titre"], 30, "sans-700", UTILE)
    A(texte(MARGE, Y_SOUSTITRE, donnees["sous_titre"], "sans", 16, 400,
            "pivot", wdth=100))
    controler("sous-titre", donnees["sous_titre"], 16, "sans-400", UTILE)
    A(rect(MARGE, Y_FILET_TITRE, UTILE, 1, "filet-1"))
    mono(MARGE, Y_ENTETE, q["entete"], UTILE, "en-tête schéma")

    centres, pas = _am_centres(EX_X0, EX_X1, len(organes))

    # La bande haute et la liaison supprimée — au-dessus des protections, la
    # seule bande où rien ne descend.
    mono(EX_X0, EX_Y_BANDE_H, q["bande_haute"], UTILE, "bande haute",
         couleur="encre")
    mono(EX_X1, EX_Y_LIB_LIAISON_H, q["liaison_supprimee"], UTILE,
         "liaison supprimée", ancre="end")
    _am_tirets(A, [(EX_X0, EX_Y_LIAISON_H), (EX_X1, EX_Y_LIAISON_H)],
               "encre", 1.4)

    # L'enceinte du niveau abrité, tracée AVANT les organes pour qu'ils la
    # recouvrent. Elle ne porte pas de sens propre : elle donne un corps à la
    # bande basse, dont la moitié gauche reste vide par construction — rien
    # ne descend au droit des deux machines qui restent dehors.
    A(rect_bord(EX_X0, EX_Y_ENCEINTE0, UTILE, EX_Y_ENCEINTE1 - EX_Y_ENCEINTE0,
                "papier", "filet-3"))

    traversees = []
    dispo_lib = pas - 16
    for cx, org in zip(centres, organes):
        base, tr = _ex_organe(A, cx, org, EX_G)
        if tr is not None:
            traversees.append(tr)
        controler(f'{org["cle"]} nom', org["nom"], 13, "sans-600", dispo_lib)
        A(texte(cx, base + 36, org["nom"], "sans", 13, 600, "encre",
                wdth=112, ancre="middle"))
        mono(cx, base + 54, org["regime_libelle"], dispo_lib,
             f'{org["cle"]} régime', ancre="middle", couleur="encre")
        mono(cx, base + 70, org["detail"], dispo_lib, f'{org["cle"]} détail',
             ancre="middle")

    _ex_toiture(A, EX_X0, EX_X1, EX_Y_TOIT, traversees)
    mono(EX_X0, EX_Y_LIB_TOIT, q["plan_toiture"], UTILE, "plan de toiture",
         couleur="encre")

    # La largeur de la bande basse se mesure contre le BORD de la première
    # boîte qui descend, jamais contre son centre (leçon de la N19).
    bord = min(traversees) - EX_G["l"] / 2 - 16 - EX_X0
    mono(EX_X0, EX_Y_BANDE_B, q["bande_basse"], bord, "bande basse",
         couleur="encre")

    mono(EX_X1, EX_Y_LIB_LIAISON_B, q["liaison_interieure"], UTILE,
         "liaison intérieure", ancre="end")
    A(ligne(EX_X0, EX_Y_LIAISON_B, EX_X1, EX_Y_LIAISON_B, "encre", 1.8))
    mono(EX_X0, EX_Y_PIED, q["pied"], UTILE, "pied")

    l_phrase = controler("phrase de principe", donnees["phrase_principe"], 17,
                         "sans-400", UTILE)
    A(texte(MARGE, Y_PHRASE, donnees["phrase_principe"], "sans", 17, 400,
            "encre", wdth=100))
    libelle = donnees["cartouche_legende"]
    largeur = min(600,
                  round(mesurer(libelle, 11, "mono", tracking=11 * 0.14) + 40))
    A(rect(MARGE, Y_CARTOUCHE, largeur, H_CARTOUCHE, "profond"))
    A(texte(MARGE + 20, Y_CARTOUCHE + 20, libelle, "mono", 11, 500, "voile",
            tracking=11 * 0.14))
    A("</svg>")

    assert not trop, "dépassements sur la planche : " + " ; ".join(trop)

    dehors = [o["cle"] for o in organes if o["regime"] == "dehors"]
    descend = [o["cle"] for o in organes if o["regime"] == "descend"]
    controles = {
        "gabarit": f"{W} x {H} — rapport {W/H:.4f} (3:2 exact)",
        "demonstration": "une coupe à un seul plan — le plan de toiture, à y "
                         f"{EX_Y_TOIT}. {len(organes)} organes rangés au même "
                         f"pas de part et d’autre : {len(dehors)} restent "
                         "au-dessus et reçoivent leurs protections "
                         f'({" · ".join(dehors)}), {len(descend)} descendent — '
                         "boîte interrompue à la position abandonnée, flèche à "
                         "travers le plan, boîte pleine en dessous "
                         f'({" · ".join(descend)}). Au-dessus, la liaison de '
                         "quartier à quartier est interrompue ; en dessous, la "
                         "liaison intérieure est pleine. Texte masqué, le "
                         "dessin se lit encore : deux boîtes protégées en haut, "
                         "deux boîtes en bas, deux flèches qui percent le plan",
        "primitive_partagee": "_ex_organe(A, cx, org, g) — une seule "
                              "implantation pour les trois formats et les deux "
                              "régimes ; `g` porte les MESURES du format "
                              "(absolues) et `ech` les seuls MOTIFS "
                              "(interruption, pointe, plot, brèche), de sorte "
                              "qu’aucun dessin ne soit la réduction d’un "
                              "autre et que « interrompu » veuille dire la "
                              "même chose partout. Abscisses par _am_centres "
                              "et interruptions par _am_dash(ech), déjà "
                              "partagées avec le mécanisme `amorce`",
        "topologie": f'{len(organes)} organes au pas de {pas:.1f} px sur x '
                     f'{EX_X0}–{EX_X1}, centres '
                     f'{", ".join(f"{c:.0f}" for c in centres)} ; plan de '
                     f'toiture à y {EX_Y_TOIT} et {EX_Y_TOIT + EX_EP_TOIT}, '
                     f'{len(traversees)} brèches de {EX_BRECHE} px à x '
                     f'{", ".join(f"{t:.0f}" for t in traversees)} ; bande '
                     f'basse bornée à {bord:.0f} px, mesurée contre le bord de '
                     "la première boîte descendue",
        "chiffre_unique": "aucun chiffre de relevé — la démonstration n’est "
                          "pas chiffrée (révision 4) ; les seules valeurs "
                          "écrites sont les régimes et le niveau d’accueil",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l’échelle "
                         f"0,96 (1152 / {W})",
        "bas_du_dessin": f"pied à y {EX_Y_PIED}, phrase à y {Y_PHRASE}, "
                         f"cartouche {Y_CARTOUCHE}–{Y_CARTOUCHE + H_CARTOUCHE}, "
                         f"marge basse {H - (Y_CARTOUCHE + H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur * H_CARTOUCHE / (W * H) * 100:.2f} % "
                            "de la planche",
        "phrase_principe": f"{len(donnees['phrase_principe'])} signes — "
                           f"{l_phrase:.0f} px pour {UTILE} disponibles",
        "depassements": f"aucun — les {8 + len(organes) * 3} chaînes mesurées "
                        "tiennent sous leur colonne (assertion de composition)",
    }
    return "\n".join(out) + "\n", controles


# ── La vignette : les quatre organes, le plan, la liaison intérieure ───────
EX_V_X0, EX_V_X1 = V_MARGE, VW - V_MARGE
EX_V_G = dict(l=44, h=20, y_haut=64, y_bas=140, d_capot=9, h_capot=5,
              ech=0.6)
EX_V_Y_TOIT = 116
EX_V_Y_LIAISON = 170
# Les deux libellés de bande. Le haut est descendu à 46 et les boîtes à 64 :
# à 56, le capot de la première colonne montait à 47 et passait sous le
# libellé — collision invisible au contrôle de largeur, qui ne mesure jamais
# une occupation.
EX_V_Y_HAUT, EX_V_Y_BAS, EX_V_Y_PIED = 46, 134, 184


def composer_vignette_exposition(donnees):
    """Ce qu'elle garde : les quatre organes, leurs deux régimes, le plan percé
    et la liaison intérieure. Ce qu'elle laisse : les noms d'organe, les
    détails, et la liaison supprimée du haut — à 300 px son trait interrompu
    passerait à 12 px des boîtes fantômes et les deux interruptions se
    confondraient."""
    q = donnees["exposition"]
    v = q["vignette"]
    out = []
    A = out.append
    trop = []

    def mono(x, y, chaine, dispo, nom, ancre=None, couleur="pivot", corps=9):
        l = mesurer(chaine, corps, "mono", corps * 0.14)
        if l > dispo:
            trop.append(f"{nom} : {l:.0f} px pour {dispo:.0f}")
        A(texte(x, y, chaine, "mono", corps, 500, couleur, ancre=ancre,
                tracking=corps * 0.14))

    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" '
      f'focusable="false" style="width:100%;height:auto;display:block">')
    entete_style(A)
    A(rect(0, 0, VW, VH, "papier"))
    mono(V_MARGE, 26, donnees["vignette_surtitre"], EX_V_X1 - EX_V_X0,
         "surtitre")

    centres, pas = _am_centres(EX_V_X0, EX_V_X1, len(q["organes"]))
    mono(V_MARGE, EX_V_Y_HAUT, v["haut"], EX_V_X1 - EX_V_X0, "haut",
         couleur="encre")
    traversees = []
    for cx, org in zip(centres, q["organes"]):
        _, tr = _ex_organe(A, cx, org, EX_V_G)
        if tr is not None:
            traversees.append(tr)
    _ex_toiture(A, EX_V_X0, EX_V_X1, EX_V_Y_TOIT, traversees,
                ech=EX_V_G["ech"], epaisseur=1.4)
    bord = min(traversees) - EX_V_G["l"] / 2 - 8 - EX_V_X0
    mono(V_MARGE, EX_V_Y_BAS, v["bas"], bord, "bas", couleur="encre")
    A(ligne(EX_V_X0, EX_V_Y_LIAISON, EX_V_X1, EX_V_Y_LIAISON, "encre", 1.5))
    mono(V_MARGE, EX_V_Y_PIED, v["pied"], EX_V_X1 - EX_V_X0, "pied")
    A("</svg>")

    assert not trop, "dépassements sur la vignette : " + " ; ".join(trop)
    return "\n".join(out) + "\n", {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": "vignette servie à 274-296 px dans une carte — "
                            f"échelle {274/VW:.2f} à {296/VW:.2f}, jamais "
                            "au-dessus de 1,00",
        "corps_minimal": "9 px dans le repère — rendu à 8,2 px à l’échelle "
                         "0,91, à 8,9 px à 0,99",
        "motif": f'{len(q["organes"])} organes au pas de {pas:.1f} px, '
                 f'{len(traversees)} qui percent le plan ; boîtes de '
                 f'{EX_V_G["l"]} x {EX_V_G["h"]} px — une composition propre, '
                 "pas une réduction de la planche — et motif d’interruption à "
                 f'l’échelle {{EX_V_G["ech"]}}',
        "primitive_partagee": "_ex_organe et _ex_toiture — les mêmes que la "
                              "planche et l’appui ; centres par _am_centres",
        "marges": f"aucun trait sous x {V_MARGE} ni au-delà de x {EX_V_X1} ; "
                  f"pied à y {EX_V_Y_PIED} pour {VH - V_MARGE} de bas de cadre",
        "depassements": "aucun — assertion de composition",
    }


# ── L'appui : les quatre organes et leurs libellés courts ──────────────────
EX_A_X0, EX_A_X1 = A_MARGE, AW - A_MARGE
EX_A_G = dict(l=92, h=30, y_haut=92, y_bas=210, d_capot=13, h_capot=7,
              ech=0.7)
EX_A_Y_TOIT = 162
EX_A_Y_LIAISON = 300


def composer_appui_exposition(donnees):
    q = donnees["exposition"]
    a = q["appui"]
    out = []
    A = out.append
    trop = []
    racine_appui(A, donnees)

    def mono(x, y, chaine, dispo, nom, ancre=None, couleur="pivot", corps=10):
        l = mesurer(chaine, corps, "mono", corps * 0.14)
        if l > dispo:
            trop.append(f"{nom} : {l:.0f} px pour {dispo:.0f}")
        A(texte(x, y, chaine, "mono", corps, 500, couleur, ancre=ancre,
                tracking=corps * 0.14))

    centres, pas = _am_centres(EX_A_X0, EX_A_X1, len(q["organes"]))
    mono(A_MARGE, 66, a["haut"], EX_A_X1 - EX_A_X0, "haut", couleur="encre")
    traversees = []
    for cx, org, lib in zip(centres, q["organes"], a["libelles"]):
        base, tr = _ex_organe(A, cx, org, EX_A_G)
        if tr is not None:
            traversees.append(tr)
        mono(cx, base + 26, lib, pas - 10, f'{org["cle"]} libellé',
             ancre="middle", couleur="encre")
    _ex_toiture(A, EX_A_X0, EX_A_X1, EX_A_Y_TOIT, traversees,
                ech=EX_A_G["ech"], epaisseur=1.6)
    bord = min(traversees) - EX_A_G["l"] / 2 - 10 - EX_A_X0
    mono(A_MARGE, 188, a["bas"], bord, "bas", couleur="encre")
    A(ligne(EX_A_X0, EX_A_Y_LIAISON, EX_A_X1, EX_A_Y_LIAISON, "encre", 1.6))
    mono(A_MARGE, 330, a["pied"], EX_A_X1 - EX_A_X0, "pied")
    A("</svg>")

    assert not trop, "dépassements sur l’appui : " + " ; ".join(trop)
    return "\n".join(out) + "\n", controles_appui(
        f'{len(q["organes"])} organes au pas de {pas:.1f} px — boîtes de '
        f'{EX_A_G["l"]} x {EX_A_G["h"]} px, motif à l’échelle '
        f'{EX_A_G["ech"]} ; la partition '
        f'{sum(1 for o in q["organes"] if o["regime"] == "dehors")} dehors / '
        f'{len(traversees)} descendus se répète et porte seule la démonstration',
        f"liaison intérieure à y {EX_A_Y_LIAISON}, pied à y 330, marge basse "
        f"{AH - 330} px",
        colonnes=f"dessin x {EX_A_X0}–{EX_A_X1} ({EX_A_X1 - EX_A_X0} px)",
        depassements="aucun — assertion de composition",
    )



# ── `retrait` : le périmètre du calcul recule à l'intérieur ─────────────────
# Le mécanisme de la N21 (bâtiment SSLIA, aéroport de La Rochelle). Une seule
# enveloppe construite, partagée par un mur ; le périmètre du calcul RT2012
# n'enferme que la partie droite, parce que la remise des véhicules est tenue
# sous 12 °C et sort du calcul. Le trait épais quitte donc la façade sur un
# seul côté et descend le long d'un mur INTÉRIEUR : c'est la démonstration, et
# elle tient sans un mot.
#
# Les deux grandeurs restent distinguées (leçon de la N20) :
#   · les MESURES du dessin (abscisses, ordonnées) sont ABSOLUES et propres à
#     chaque format — une coupe de vignette n'est pas une coupe de planche
#     réduite ;
#   · l'ÉCHELLE `ech` ne commande que les MOTIFS et les petits accessoires
#     (épaisseurs de trait, largeur du bloc-porte, longueur des amorces), de
#     sorte que « épais » veuille dire la même chose dans les trois dessins.
RE_G = dict(x0=276, x_mur=560, x1=1144,
            y_toit=250, y_plancher=396, y_sol=528,
            porte=(456, 500), ech=1.0)

RE_V_G = dict(x0=14, x_mur=118, x1=286,
              y_toit=62, y_plancher=112, y_sol=152,
              porte=None, ech=0.55)

RE_A_G = dict(x0=24, x_mur=210, x1=528,
              y_toit=76, y_plancher=176, y_sol=252,
              porte=None, ech=0.70)

RE_PX_PAR_KW = 40.0        # échelle des deux barres de puissance absorbée
RE_Y_REG2 = 552            # en-tête du second registre
RE_Y_BOITE, RE_H_BOITE = 570, 28
RE_Y_LIB_KW, RE_Y_LIB_ROLE = 618, 634


def _re_coupe(A, g):
    """L'enveloppe construite, son mur de partage, le plancher intermédiaire,
    le périmètre calculé et la porte — une seule implantation pour les trois
    formats.

    Ordre de tracé : l'aplat calcaire du volume calculé d'abord, le filet fin
    de l'enveloppe ensuite (il doit se voir par-dessus l'aplat), puis le trait
    épais du périmètre, qui recouvre le filet sur les trois côtés où les deux
    coïncident — le quatrième est la démonstration.

    Rend les ordonnées utiles aux appels de cote."""
    ech = g["ech"]
    x0, xm, x1 = g["x0"], g["x_mur"], g["x1"]
    yt, yp, ys = g["y_toit"], g["y_plancher"], g["y_sol"]
    ep_env = 1.6 * max(ech, 0.7)
    ep_per = 3.4 * max(ech, 0.62)
    ep_pla = 1.6 * max(ech, 0.7)

    A(rect(xm, yt, x1 - xm, ys - yt, "calcaire"))

    for a, b in (((x0, yt), (x1, yt)), ((x1, yt), (x1, ys)),
                 ((x1, ys), (x0, ys)), ((x0, ys), (x0, yt))):
        A(ligne(a[0], a[1], b[0], b[1], "filet-1", ep_env))

    A(ligne(xm, yp, x1, yp, "encre", ep_pla))

    if g["porte"] is not None:
        py0, py1 = g["porte"]
        lp = 14 * ech
        A(rect(xm - lp / 2, py0, lp, py1 - py0, "clair"))

    A(polyligne([(xm, yt), (x1, yt), (x1, ys), (xm, ys), (xm, yt)],
                "encre", ep_per))

    return dict(x_mur=xm, y_plancher=yp)


def _re_barre(A, cx, poste, y, h, px_par_kw):
    """Une barre de puissance absorbée, largeur proportionnelle, et sa flèche
    de desserte vers le volume qui la reçoit."""
    w = poste["valeur"] * px_par_kw
    A(rect_bord(cx - w / 2, y, w, h, "clair", "filet-1"))
    return w


def composer_retrait(donnees):
    q = donnees["retrait"]
    hc = q["hors_calcul"]
    g = RE_G
    out = []
    A = out.append
    trop = []

    def controler(nom, chaine, corps, profil, dispo, tracking=0.0):
        l = mesurer(chaine, corps, profil, tracking)
        if l > dispo:
            trop.append(f"{nom} : {l:.0f} px pour {dispo:.0f}")
        return l

    def mono(x, y, chaine, dispo, nom, ancre=None, couleur="pivot", corps=10):
        controler(nom, chaine, corps, "mono", dispo, corps * 0.14)
        A(texte(x, y, chaine, "mono", corps, 500, couleur, ancre=ancre,
                tracking=corps * 0.14))

    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
      f'preserveAspectRatio="xMidYMid meet" role="img" '
      f'style="width:100%;height:auto;display:block" '
      f'aria-label="{echapper(donnees["aria_label"])}">')
    entete_style(A)
    A(rect(0, 0, W, H, "papier"))

    A(texte(MARGE, Y_SURTITRE, donnees["surtitre"], "mono", 11, 500, "pivot",
            tracking=11 * 0.14))
    controler("surtitre", donnees["surtitre"], 11, "mono", UTILE, 11 * 0.14)
    A(texte(MARGE, Y_TITRE, donnees["titre"], "sans", 30, 700, "encre",
            wdth=112))
    controler("titre", donnees["titre"], 30, "sans-700", UTILE)
    A(texte(MARGE, Y_SOUSTITRE, donnees["sous_titre"], "sans", 16, 400,
            "pivot", wdth=100))
    controler("sous-titre", donnees["sous_titre"], 16, "sans-400", UTILE)
    A(rect(MARGE, Y_FILET_TITRE, UTILE, 1, "filet-1"))
    mono(MARGE, Y_ENTETE, q["entete"], UTILE, "en-tête schéma")

    x0, xm, x1 = g["x0"], g["x_mur"], g["x1"]
    yt, yp, ys = g["y_toit"], g["y_plancher"], g["y_sol"]

    # Les deux légendes de ligne, chacune AU-DESSUS du segment qu'elle nomme :
    # à gauche l'enveloppe seule, à droite l'enveloppe et le périmètre confondus.
    mono(x0, yt - 12, q["legende_enveloppe"], xm - x0 - 12, "légende enveloppe")
    mono(xm, yt - 12, q["legende_perimetre"], x1 - xm, "légende périmètre",
         couleur="encre")

    ancres = _re_coupe(A, g)

    # Le volume hors calcul — libellé, statut, consigne, puis la mention qui
    # occupe le milieu du volume : ce qu'il est au sens du calcul, c'est-à-dire
    # rien.
    x_g, dispo_g = x0 + 20, xm - x0 - 40
    mono(x_g, 276, hc["libelle"], dispo_g, "remise libellé", couleur="encre")
    mono(x_g, 294, hc["statut"], dispo_g, "remise statut", couleur="encre")
    mono(x_g, 312, hc["detail"], dispo_g, "remise consigne")
    mono(x_g, 410, hc["mention"], dispo_g, "remise mention")

    # Les deux niveaux calculés — alignés à droite, chacun dans son volume.
    x_d, dispo_d = x1 - 20, x1 - xm - 40
    for niveau, y in zip(q["niveaux"], (276, 424)):
        mono(x_d, y, niveau["libelle"], dispo_d, f'{niveau["cle"]} libellé',
             ancre="end", couleur="encre")
        mono(x_d, y + 18, niveau["detail"], dispo_d, f'{niveau["cle"]} détail',
             ancre="end")

    # Les trois requalifications, contre la limite. Chacune porte une amorce
    # qui la rattache au point du dessin qu'elle qualifie — le mur, la
    # naissance du plancher, la porte.
    x_c, dispo_c = xm + 22, x1 - (xm + 22)
    y_conseq = {"mur": 326, "plancher": 366, "porte": 468}
    for c in q["consequences"]:
        y = y_conseq[c["cle"]]
        mono(x_c, y, c["libelle"], dispo_c, f'{c["cle"]} libellé',
             couleur="encre")
        mono(x_c, y + 16, c["detail"], dispo_c, f'{c["cle"]} détail')
        if c["cle"] == "mur":
            A(ligne(xm + 4, y - 4, x_c - 6, y - 4, "encre", 1.4))
        elif c["cle"] == "plancher":
            A(polyligne([(x_c - 6, y - 4), (xm + 12, y - 4), (xm + 12, yp)],
                        "encre", 1.4))
        else:
            A(ligne(xm + 8, y - 4, x_c - 6, y - 4, "encre", 1.4))

    # Second registre : la puissance absorbée en chauffage, à largeur
    # proportionnelle. Une barre par volume, sous le volume qu'elle dessert.
    m = q["machines"]
    mono(x0, RE_Y_REG2, m["entete"], UTILE, "en-tête machines", couleur="encre")
    A(ligne(xm, RE_Y_REG2 + 8, xm, RE_Y_LIB_ROLE + 8, "filet-2", 1.4))
    centres = {"gauche": (x0 + xm) / 2, "droite": (xm + x1) / 2}
    largeurs = {}
    for poste in m["postes"]:
        cx = centres[poste["bord"]]
        w = _re_barre(A, cx, poste, RE_Y_BOITE, RE_H_BOITE, RE_PX_PAR_KW)
        largeurs[poste["cle"]] = w
        borne = (xm - x0 - 24) if poste["bord"] == "gauche" else (x1 - xm - 24)
        mono(cx, RE_Y_LIB_KW, poste["libelle"], borne,
             f'{poste["cle"]} puissance', ancre="middle", couleur="encre")
        mono(cx, RE_Y_LIB_ROLE, poste["role"], borne, f'{poste["cle"]} rôle',
             ancre="middle")

    l_phrase = controler("phrase de principe", donnees["phrase_principe"], 17,
                         "sans-400", UTILE)
    A(texte(MARGE, Y_PHRASE, donnees["phrase_principe"], "sans", 17, 400,
            "encre", wdth=100))
    libelle = donnees["cartouche_legende"]
    largeur = min(600,
                  round(mesurer(libelle, 11, "mono", tracking=11 * 0.14) + 40))
    A(rect(MARGE, Y_CARTOUCHE, largeur, H_CARTOUCHE, "profond"))
    A(texte(MARGE + 20, Y_CARTOUCHE + 20, libelle, "mono", 11, 500, "voile",
            tracking=11 * 0.14))
    A("</svg>")

    assert not trop, "dépassements sur la planche : " + " ; ".join(trop)

    rap = largeurs["tertiaire"] / largeurs["remise"]
    controles = {
        "gabarit": f"{W} x {H} — rapport {W/H:.4f} (3:2 exact)",
        "demonstration": "une enveloppe construite d’un seul tenant, x "
                         f"{x0}–{x1}, partagée par un mur à x {xm} ; à droite "
                         f"deux niveaux séparés par un plancher à y {yp}, à "
                         "gauche un seul volume. Le trait épais du périmètre "
                         "calculé ne ferme que la partie droite : il épouse "
                         "l’enveloppe sur trois côtés et la quitte sur le "
                         "quatrième, où il descend le long d’un mur "
                         "INTÉRIEUR. Texte masqué, le dessin se lit encore : "
                         "un rectangle fin, un rectangle épais plus petit "
                         "dedans, et l’écart entre les deux est exactement le "
                         "volume qui sort du calcul",
        "primitive_partagee": "_re_coupe(A, g) — une seule implantation pour "
                              "les trois formats ; `g` porte les MESURES du "
                              "format (absolues) et `ech` les seuls MOTIFS "
                              "(épaisseurs, largeur du bloc-porte), de sorte "
                              "qu’aucun dessin ne soit la réduction d’un autre "
                              "et que « épais » veuille dire la même chose "
                              "partout",
        "topologie": f"enveloppe {x1 - x0} x {ys - yt} px, mur de partage à x "
                     f"{xm} ({(xm - x0) / (x1 - x0) * 100:.0f} % à gauche) ; "
                     f"plancher intermédiaire y {yp} sur x {xm}–{x1} ; porte "
                     f"y {g['porte'][0]}–{g['porte'][1]} à cheval sur le mur ; "
                     "trois amorces rattachent les requalifications au mur, à "
                     "la naissance du plancher et à la porte",
        "proportionnalite": f"barres de puissance absorbée à "
                            f"{RE_PX_PAR_KW:.0f} px par kW : "
                            f"{largeurs['remise']:.0f} px pour 1,5 kW contre "
                            f"{largeurs['tertiaire']:.0f} px pour 6,7 kW, "
                            f"rapport {rap:.2f} — égal au rapport des "
                            f"puissances ({6.7/1.5:.2f})",
        "chiffre_unique": "aucun chiffre de relevé — la démonstration n’est "
                          "pas chiffrée (révision 4) ; les seules valeurs "
                          "écrites sont les deux perméabilités, les trois "
                          "coefficients de la limite et les deux puissances "
                          "absorbées",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l’échelle "
                         f"0,96 (1152 / {W})",
        "bas_du_dessin": f"barres {RE_Y_BOITE}–{RE_Y_BOITE + RE_H_BOITE}, "
                         f"rôles à y {RE_Y_LIB_ROLE}, phrase à y {Y_PHRASE}, "
                         f"cartouche {Y_CARTOUCHE}–{Y_CARTOUCHE + H_CARTOUCHE}, "
                         f"marge basse {H - (Y_CARTOUCHE + H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur * H_CARTOUCHE / (W * H) * 100:.2f} % "
                            "de la planche",
        "phrase_principe": f"{len(donnees['phrase_principe'])} signes — "
                           f"{l_phrase:.0f} px pour {UTILE} disponibles",
        "depassements": "aucun — 22 chaînes mesurées sous leur colonne "
                        "(assertion de composition)",
    }
    return "\n".join(out) + "\n", controles


def composer_vignette_retrait(donnees):
    """Ce qu'elle garde : l'enveloppe, le mur, le plancher, le périmètre épais
    et la porte — la géométrie entière, qui porte seule la thèse. Ce qu'elle
    laisse : les trois requalifications, les deux perméabilités et le registre
    des puissances ; à 300 px, six lignes de mono se confondraient."""
    q = donnees["retrait"]
    v = q["vignette"]
    g = RE_V_G
    out = []
    A = out.append
    trop = []

    def mono(x, y, chaine, dispo, nom, ancre=None, couleur="pivot", corps=9):
        l = mesurer(chaine, corps, "mono", corps * 0.14)
        if l > dispo:
            trop.append(f"{nom} : {l:.0f} px pour {dispo:.0f}")
        A(texte(x, y, chaine, "mono", corps, 500, couleur, ancre=ancre,
                tracking=corps * 0.14))

    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" '
      f'focusable="false" style="width:100%;height:auto;display:block">')
    entete_style(A)
    A(rect(0, 0, VW, VH, "papier"))
    mono(V_MARGE, 26, donnees["vignette_surtitre"], g["x1"] - g["x0"],
         "surtitre")

    _re_coupe(A, g)

    x0, xm, x1 = g["x0"], g["x_mur"], g["x1"]
    mono(x0 + 8, 80, v["hors"], xm - x0 - 16, "hors", couleur="encre")
    mono(x0 + 8, 94, v["consigne"], xm - x0 - 16, "consigne")
    mono(x1 - 8, 80, v["haut"], x1 - xm - 16, "haut", ancre="end",
         couleur="encre")
    mono(x1 - 8, 132, v["bas"], x1 - xm - 16, "bas", ancre="end",
         couleur="encre")
    mono(V_MARGE, 178, v["pied"], x1 - x0, "pied")
    A("</svg>")

    assert not trop, "dépassements sur la vignette : " + " ; ".join(trop)
    return "\n".join(out) + "\n", {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": "vignette servie à 274-296 px dans une carte — "
                            f"échelle {274/VW:.2f} à {296/VW:.2f}, jamais "
                            "au-dessus de 1,00",
        "corps_minimal": "9 px dans le repère — rendu à 8,2 px à l’échelle "
                         "0,91, à 8,9 px à 0,99",
        "motif": f"enveloppe {x1 - x0} x {g['y_sol'] - g['y_toit']} px, mur à "
                 f"x {xm}, plancher à y {g['y_plancher']} — une composition "
                 "propre, pas une réduction de la planche : les mesures sont "
                 f"absolues et seul le motif suit l’échelle {g['ech']}",
        "primitive_partagee": "_re_coupe — la même que la planche et l’appui",
        "marges": f"aucun trait sous x {V_MARGE} ni au-delà de x {x1} ; pied à "
                  f"y 178 pour {VH - V_MARGE} de bas de cadre",
        "depassements": "aucun — assertion de composition",
    }


def composer_appui_retrait(donnees):
    q = donnees["retrait"]
    a = q["appui"]
    g = RE_A_G
    out = []
    A = out.append
    trop = []
    racine_appui(A, donnees)

    def mono(x, y, chaine, dispo, nom, ancre=None, couleur="pivot", corps=10):
        l = mesurer(chaine, corps, "mono", corps * 0.14)
        if l > dispo:
            trop.append(f"{nom} : {l:.0f} px pour {dispo:.0f}")
        A(texte(x, y, chaine, "mono", corps, 500, couleur, ancre=ancre,
                tracking=corps * 0.14))

    x0, xm, x1 = g["x0"], g["x_mur"], g["x1"]
    mono(x0, g["y_toit"] - 10, a["legende_enveloppe"], xm - x0 - 10,
         "légende enveloppe")
    mono(xm, g["y_toit"] - 10, a["legende_perimetre"], x1 - xm,
         "légende périmètre", couleur="encre")

    _re_coupe(A, g)

    mono(x0 + 10, 104, a["hors"], xm - x0 - 20, "hors", couleur="encre")
    mono(x0 + 10, 122, a["statut"], xm - x0 - 20, "statut", couleur="encre")
    mono(x0 + 10, 140, a["consigne"], xm - x0 - 20, "consigne")
    mono(x1 - 10, 104, a["haut"], x1 - xm - 20, "haut", ancre="end",
         couleur="encre")
    mono(x1 - 10, 208, a["bas"], x1 - xm - 20, "bas", ancre="end",
         couleur="encre")
    mono(x0, 300, a["consequence"], x1 - x0, "conséquence", couleur="encre")
    mono(x0, 330, a["pied"], x1 - x0, "pied")
    A("</svg>")

    assert not trop, "dépassements sur l’appui : " + " ; ".join(trop)
    return "\n".join(out) + "\n", controles_appui(
        f"enveloppe {x1 - x0} x {g['y_sol'] - g['y_toit']} px, mur de partage "
        f"à x {xm}, plancher à y {g['y_plancher']} — même primitive qu’à la "
        f"planche, motifs à l’échelle {g['ech']} ; le trait épais ne ferme que "
        "la partie droite et porte seul la démonstration",
        f"conséquence à y 300, pied à y 330, marge basse {AH - 330} px",
        colonnes=f"dessin x {x0}–{x1} ({x1 - x0} px), volume hors calcul "
                 f"{xm - x0} px, volume calculé {x1 - xm} px",
        depassements="aucun — assertion de composition",
    )


def _composer(donnees):
    if "restitution" in donnees:
        return composer_restitution(donnees)
    if "retrait" in donnees:
        return composer_retrait(donnees)
    if "exposition" in donnees:
        return composer_exposition(donnees)
    if "amorce" in donnees:
        return composer_amorce(donnees)
    if "frontiere" in donnees:
        return composer_frontiere(donnees)
    if "sortie" in donnees:
        return composer_sortie(donnees)
    if "colonne" in donnees:
        return composer_colonne(donnees)
    if "equilibre" in donnees:
        return composer_equilibre(donnees)
    if "enjambement" in donnees:
        return composer_enjambement(donnees)
    if "portee" in donnees:
        return composer_portee(donnees)
    return composer(donnees)


def _composer_vignette(donnees):
    if "restitution" in donnees:
        return composer_vignette_restitution(donnees)
    if "retrait" in donnees:
        return composer_vignette_retrait(donnees)
    if "exposition" in donnees:
        return composer_vignette_exposition(donnees)
    if "amorce" in donnees:
        return composer_vignette_amorce(donnees)
    if "frontiere" in donnees:
        return composer_vignette_frontiere(donnees)
    if "sortie" in donnees:
        return composer_vignette_sortie(donnees)
    if "colonne" in donnees:
        return composer_vignette_colonne(donnees)
    if "equilibre" in donnees:
        return composer_vignette_equilibre(donnees)
    if "enjambement" in donnees:
        return composer_vignette_enjambement(donnees)
    if "portee" in donnees:
        return composer_vignette_portee(donnees)
    return composer_vignette(donnees)


def _composer_appui(donnees):
    if "restitution" in donnees:
        return composer_appui_restitution(donnees)
    if "retrait" in donnees:
        return composer_appui_retrait(donnees)
    if "exposition" in donnees:
        return composer_appui_exposition(donnees)
    if "amorce" in donnees:
        return composer_appui_amorce(donnees)
    if "frontiere" in donnees:
        return composer_appui_frontiere(donnees)
    if "sortie" in donnees:
        return composer_appui_sortie(donnees)
    if "colonne" in donnees:
        return composer_appui_colonne(donnees)
    if "equilibre" in donnees:
        return composer_appui_equilibre(donnees)
    if "enjambement" in donnees:
        return composer_appui_enjambement(donnees)
    if "portee" in donnees:
        return composer_appui_portee(donnees)
    return composer_appui(donnees)


if __name__ == "__main__":
    executer(_composer, _composer_vignette, _composer_appui)
