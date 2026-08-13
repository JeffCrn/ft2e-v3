#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compositeur de planche — archétype `tableau-electrique`.

Protocole : docs/superpowers/specs/2026-08-12-planches-references-protocole.md

Il lit un `planche.json` (l'extraction, produite par la session de génération) et
écrit les deux dessins qui en découlent :

    planche.svg    1200 x 800 — la planche de fiche, lue à 1152 px (échelle 0,96)
    vignette.svg    300 x 200 — la vignette de carte, lue à 274-296 px (0,91-0,99)

Usage :

    python scripts/planches/tableau-electrique.py public/images/projets/<slug>

La géométrie est CALCULÉE : aucune coordonnée n'est tapée à la main, et le bloc
`controles` du JSON est recalculé à chaque exécution.

Le motif de l'archétype — arrivée → tableau → départs, et le mécanisme composé
ici (`autoconsommation`) le renverse : **la toiture est la seconde arrivée du
tableau.** La production descend du bandeau de modules — comptés un à un, 48
rectangles pour 48 modules — vers la barre de distribution ; l'échange avec le
réseau se lit par deux flèches opposées (surplus revendu, appoint soutiré) ; et
le départ que la planche suit s'élargit en traversant la pompe à chaleur — trois
bandes aux largeurs 1 / 3,6 / 4,6, proportionnelles au COP — avant de se
répandre dans la longue dalle du plancher. La démonstration est portée par la
géométrie : une source en haut, un aller-retour à gauche, un épaississement au
centre, une nappe en bas. Toiture et plancher sont des bandes topologiques :
aucune implantation réelle n'est reprise (règle 4).

Cinquième module du chantier après `sankey-energie.py`, `zonage-ssi.py`,
`coupe-traversee.py` et `boucle-fluide.py`. Le tronc commun (jetons, mesure des
chasses, insécables, double écriture des couleurs, routine d'exécution) vit dans
`_tronc.py`.
"""

from _tronc import (NN, INS, W, H, MARGE, UTILE, VW, VH, V_MARGE, mesurer,
                    replier, echapper, texte, rect, rect_bord, ligne,
                    polyligne, fleche, entete_style, executer)


# ── Rythme vertical de la planche ────────────────────────────────────────────
Y_SURTITRE = 76
Y_TITRE = 112
Y_SOUSTITRE = 138
Y_FILET_TITRE = 160
Y_ENTETE = 190
Y_PHRASE = 688
Y_CARTOUCHE = 714
H_CARTOUCHE = 30

# ── Le registre de toiture : 48 modules comptés un à un ──────────────────────
N_MODULES = 48
T_X0, T_X1 = 380, 1144        # le bandeau de modules
T_Y0, T_Y1 = 240, 268         # un module de haut (28 px)
Y_TOIT = 272                  # le plan de toiture, sous les modules

# ── La barre de distribution et l'échange avec le réseau ─────────────────────
X_COND = 762                  # la descente d'autoconsommation
Y_BUS = 376                   # la barre
XB0, XB1 = 420, 1050
R_X0, R_X1 = 56, 230          # le bloc réseau public
R_Y0, R_Y1 = 348, 416
Y_SURPLUS, Y_APPOINT = 366, 392   # les deux sens de l'échange

# ── Le départ suivi : la pompe à chaleur et ses trois bandes ─────────────────
UCOP = 4.0                    # 1 kWh électrique = 4 px de large
P_X0, P_X1 = 480, 700         # la boîte de la pompe à chaleur
P_Y0, P_Y1 = 448, 524
X_ELEC = 560                  # la descente électrique (largeur 1 x UCOP)
Y_AIR0 = 476                  # la bande d'air (largeur part_air x UCOP)
X_CHAL = 587.2                # l'axe de la bande de chaleur (rapport x UCOP)

# ── L'autre départ, groupé ───────────────────────────────────────────────────
D_X0, D_X1 = 800, 1144
D_Y0, D_Y1 = 448, 524
X_DEP = 920                   # sa descente depuis la barre

# ── Le registre du sol : la dalle et sa serpentine ───────────────────────────
S_X0, S_X1 = 420, 1144
S_Y0, S_Y1 = 580, 620
X_TEXTE_SOL = 56              # la colonne de texte du sol, à gauche de la dalle


def composer(donnees):
    t = donnees["tableau"]
    elems = {e["cle"]: e for e in t["elements"]}
    cop = t["cop"]
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

    # ── En-tête du schéma ────────────────────────────────────────────────────
    controler("en-tête schéma", t["entete"], 10, "mono", UTILE, 10 * 0.14)
    A(texte(MARGE, Y_ENTETE, t["entete"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))

    # ── EN TOITURE — le bandeau des 48 modules, comptés un à un ──────────────
    A(texte(MARGE, 226, t["tag_toiture"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    pas = (T_X1 - T_X0) / N_MODULES
    for k in range(N_MODULES):
        A(rect(T_X0 + k * pas, T_Y0, pas - 4, T_Y1 - T_Y0, "clair"))
    A(ligne(T_X0, Y_TOIT, T_X1, Y_TOIT, "encre", 1.5))

    to = elems["toiture"]
    controler("libellé toiture", to["libelle"], 15, "sans-400", 300)
    A(texte(MARGE, 252, to["libelle"], "sans", 15, 400, "encre", wdth=100))
    # Le chiffre que la planche défend — le seul en encre pleine.
    val = f'{to["valeur"]}{INS}{to["unite"]}'
    l_val = controler("chiffre de la toiture", val, 22, "sans-700", 300)
    A(texte(MARGE, 280, val, "sans", 22, 700, "encre", wdth=118,
            tabulaire=True))
    for k, l in enumerate(to["detail"]):
        controler(f"détail toiture {k + 1}", l, 10, "mono", 310, 10 * 0.14)
        A(texte(MARGE, 300 + k * 14, l, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))

    # ── La descente d'autoconsommation, du bandeau à la barre ────────────────
    A(ligne(X_COND, Y_TOIT, X_COND, Y_BUS - 6, "encre", 2))
    A(fleche(X_COND, Y_BUS - 2, "encre", "bas", 9))
    controler("liaison autoconsommation", t["liaison_autoconsommation"],
              10, "mono", 300, 10 * 0.14)
    A(texte(X_COND + 12, 330, t["liaison_autoconsommation"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))

    # ── La barre de distribution ─────────────────────────────────────────────
    A(ligne(XB0, Y_BUS, XB1, Y_BUS, "encre", 3))
    di = elems["distribution"]
    controler("libellé distribution", di["libelle"], 15, "sans-400", 300)
    A(texte(XB0, Y_BUS - 16, di["libelle"], "sans", 15, 400, "encre", wdth=100))

    # ── L'échange avec le réseau : deux flèches opposées ─────────────────────
    re_ = elems["reseau"]
    A(rect_bord(R_X0, R_Y0, R_X1 - R_X0, R_Y1 - R_Y0, "papier", "filet-1"))
    controler("libellé réseau", re_["libelle"], 15, "sans-400",
              R_X1 - R_X0 - 32)
    A(texte(R_X0 + 16, R_Y0 + 40, re_["libelle"], "sans", 15, 400, "encre",
            wdth=100))
    x_mi = (R_X1 + XB0) / 2
    A(ligne(R_X1 + 10, Y_SURPLUS, XB0, Y_SURPLUS, "encre", 1.5))
    A(fleche(R_X1 + 10, Y_SURPLUS, "encre", "gauche", 9))
    controler("étiquette surplus", t["echange"]["vers_reseau"], 10, "mono",
              XB0 - R_X1 - 16, 10 * 0.14)
    A(texte(x_mi, Y_SURPLUS - 10, t["echange"]["vers_reseau"], "mono", 10, 500,
            "pivot", ancre="middle", tracking=10 * 0.14))
    A(ligne(R_X1, Y_APPOINT, XB0 - 10, Y_APPOINT, "encre", 1.5))
    A(fleche(XB0 - 10, Y_APPOINT, "encre", "droite", 9))
    controler("étiquette appoint", t["echange"]["du_reseau"], 10, "mono",
              XB0 - R_X1 - 16, 10 * 0.14)
    A(texte(x_mi, Y_APPOINT + 18, t["echange"]["du_reseau"], "mono", 10, 500,
            "pivot", ancre="middle", tracking=10 * 0.14))

    # ── Le départ suivi : la pompe à chaleur, et le COP en largeurs ──────────
    # La descente électrique — large d'UNE unité.
    A(rect(X_ELEC - UCOP / 2, Y_BUS + 1.5, UCOP, P_Y0 - Y_BUS - 1.5, "encre"))
    controler("étiquette électricité", cop["entree"], 10, "mono",
              X_ELEC - 14 - XB0, 10 * 0.14)
    A(texte(X_ELEC - 14, 416, cop["entree"], "mono", 10, 500, "pivot",
            ancre="end", tracking=10 * 0.14))

    pa = elems["pac"]
    A(rect_bord(P_X0, P_Y0, P_X1 - P_X0, P_Y1 - P_Y0, "papier", "filet-1"))
    controler("libellé pac", pa["libelle"], 15, "sans-400", P_X1 - P_X0 - 32)
    A(texte(P_X0 + 16, P_Y0 + 30, pa["libelle"], "sans", 15, 400, "encre",
            wdth=100))
    det_pa = f'{pa["valeur"]}{NN}{pa["unite"]} · COP{NN}4,60'
    controler("détail pac", det_pa, 10, "mono", P_X1 - P_X0 - 32, 10 * 0.14)
    A(texte(P_X0 + 16, P_Y0 + 50, det_pa, "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

    # La bande d'air — large de part_air unités, prise dehors, à gauche.
    h_air = cop["part_air"] * UCOP
    A(rect(MARGE, Y_AIR0, P_X0 - MARGE - 10, h_air, "clair"))
    A(fleche(P_X0 - 2, Y_AIR0 + h_air / 2, "encre", "droite", 10))
    controler("étiquette air", cop["air"], 10, "mono", P_X0 - MARGE - 20,
              10 * 0.14)
    A(texte(MARGE, Y_AIR0 - 10, cop["air"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

    # La bande de chaleur — large du rapport entier, vers la dalle.
    l_chal = cop["rapport"] * UCOP
    A(rect(X_CHAL - l_chal / 2, P_Y1, l_chal, S_Y0 - P_Y1 - 8, "clair"))
    A(fleche(X_CHAL, S_Y0 - 4, "encre", "bas", 11))
    controler("étiquette chaleur", cop["sortie"], 10, "mono",
              D_X0 - (X_CHAL + 22), 10 * 0.14)
    A(texte(X_CHAL + 22, 556, cop["sortie"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

    # ── L'autre départ, groupé — un bloc topologique ─────────────────────────
    A(ligne(X_DEP, Y_BUS + 1.5, X_DEP, D_Y0 - 6, "encre", 1.5))
    A(fleche(X_DEP, D_Y0 - 2, "encre", "bas", 8))
    de = elems["departs"]
    A(rect(D_X0, D_Y0, D_X1 - D_X0, D_Y1 - D_Y0, "calcaire"))
    controler("libellé départs", de["libelle"], 15, "sans-400",
              D_X1 - D_X0 - 40)
    A(texte(D_X0 + 20, D_Y0 + 30, de["libelle"], "sans", 15, 400, "encre",
            wdth=100))
    for k, l in enumerate(de["detail"]):
        controler(f"détail départs {k + 1}", l, 10, "mono",
                  D_X1 - D_X0 - 40, 10 * 0.14)
        A(texte(D_X0 + 20, D_Y0 + 50 + k * 14, l, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))

    # ── AU SOL — la dalle, sa serpentine, sa colonne de texte ────────────────
    A(texte(X_TEXTE_SOL, 560, t["tag_sol"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    pl = elems["plancher"]
    lignes_pl = replier(pl["libelle"], 15, S_X0 - X_TEXTE_SOL - 20, "sans-400")
    for k, l in enumerate(lignes_pl):
        A(texte(X_TEXTE_SOL, 584 + k * 20, l, "sans", 15, 400, "encre",
                wdth=100))
    y_det = 584 + len(lignes_pl) * 20 + 4
    regime = f'RÉGIME{NN}{pl["valeur"]}{NN}{pl["unite"]}'
    for k, l in enumerate([regime] + pl["detail"]):
        controler(f"détail plancher {k + 1}", l, 10, "mono",
                  S_X0 - X_TEXTE_SOL - 10, 10 * 0.14)
        A(texte(X_TEXTE_SOL, y_det + k * 14, l, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))

    A(rect(S_X0, S_Y0, S_X1 - S_X0, S_Y1 - S_Y0, "calcaire"))
    # La serpentine : le circuit du plancher, topologique — amplitude constante.
    y_h, y_b = S_Y0 + 8, S_Y1 - 8
    pas_s = 44
    xs = S_X0 + 16
    pts = [(xs, y_b)]
    monte = True
    while xs + pas_s <= S_X1 - 16:
        pts.append((xs, y_h if monte else y_b))
        xs += pas_s
        pts.append((xs, y_h if monte else y_b))
        monte = not monte
    pts.append((xs, y_h if monte else y_b))
    A(polyligne(pts, "encre", 1.2))

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
        "demonstration": f"la production descend du bandeau ({N_MODULES} "
                         f"rectangles dessinés = {N_MODULES} modules de la "
                         f"fiche) vers la barre de distribution ; l'échange "
                         f"réseau se lit par deux flèches opposées (y "
                         f"{Y_SURPLUS} et {Y_APPOINT}) ; le départ suivi "
                         f"s'élargit en traversant la pompe à chaleur — trois "
                         f"bandes de {UCOP:.0f}, {cop['part_air'] * UCOP:.1f} "
                         f"et {cop['rapport'] * UCOP:.1f} px, soit 1 / "
                         f"{cop['part_air']} / {cop['rapport']}, "
                         f"proportionnelles au COP — avant de se répandre dans "
                         f"la dalle ; la géométrie porte la thèse « de la "
                         f"toiture au sol »",
        "topologie": f"toiture (y {T_Y0}–{Y_TOIT}, x {T_X0}–{T_X1}) → descente "
                     f"(x {X_COND}) → barre (y {Y_BUS}, x {XB0}–{XB1}) ; "
                     f"réseau x {R_X0}–{R_X1} à gauche ; pompe à chaleur x "
                     f"{P_X0}–{P_X1} et départs groupés x {D_X0}–{D_X1} "
                     f"dessous ; dalle y {S_Y0}–{S_Y1}, x {S_X0}–{S_X1}",
        "bas_du_dessin": f"dalle jusqu'à {S_Y1}, dernier détail du sol à "
                         f"{y_det + (len(pl['detail'])) * 14}, phrase de "
                         f"principe à {Y_PHRASE}, cartouche {Y_CARTOUCHE}–"
                         f"{Y_CARTOUCHE + H_CARTOUCHE}, marge basse "
                         f"{H - (Y_CARTOUCHE + H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur * H_CARTOUCHE} px², soit "
                            f"{largeur * H_CARTOUCHE / (W * H) * 100:.2f} % "
                            f"de la planche",
        "chiffre_unique": f"un seul chiffre en encre pleine — {l_val:.0f} px "
                          f"mesurés à 22 px (17,5 kWc, la production que la "
                          f"planche défend) ; 7,5 kW, COP 4,60 et le régime "
                          f"30/35 °C restent au mono 10 pivot",
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

    Ce qu'elle garde : le bandeau des 48 modules, la descente, la barre,
    l'échange réseau à deux flèches, les trois bandes du COP et la dalle — avec
    les deux nœuds chiffrés (17,5 kWc en toiture, COP 4,60 à la machine). Ce
    qu'elle laisse : les libellés d'organes, les étiquettes d'échange, le bloc
    des autres départs annoté — six libellés dans 300 px ne se lisent pas."""
    t = donnees["tableau"]
    elems = {e["cle"]: e for e in t["elements"]}
    cop = t["cop"]
    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false" '
      f'style="width:100%;height:auto;display:block">')
    entete_style(A)
    A(rect(0, 0, VW, VH, "papier"))
    A(texte(V_MARGE, 22, donnees["vignette_surtitre"], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    # Le bandeau des 48 modules — le compte est le même que sur la planche.
    vt0, vt1 = 88, 286
    pas = (vt1 - vt0) / N_MODULES
    for k in range(N_MODULES):
        A(rect(vt0 + k * pas, 34, pas - 1.2, 12, "clair"))
    A(ligne(vt0, 48, vt1, 48, "encre", 1.2))

    # Les deux nœuds chiffrés.
    to = elems["toiture"]
    A(texte(V_MARGE, 42, to["libelle"].replace("Production en toiture",
                                               "Toiture"),
            "sans", 12, 600, "encre", wdth=112))
    A(texte(V_MARGE, 56, f'{to["valeur"]}{NN}{to["unite"]}', "mono", 10, 500,
            "pivot", tabulaire=True))

    # Descente, barre, échange réseau.
    A(ligne(190, 48, 190, 88, "encre", 1.5))
    A(fleche(190, 92, "encre", "bas", 6))
    A(ligne(88, 93, 266, 93, "encre", 2))
    A(rect_bord(14, 82, 46, 22, "papier", "filet-1"))
    A(ligne(66, 88, 88, 88, "encre", 1.2))
    A(fleche(66, 88, "encre", "gauche", 6))
    A(ligne(60, 98, 82, 98, "encre", 1.2))
    A(fleche(84, 98, "encre", "droite", 6))

    # Le départ suivi : les trois bandes du COP, à l'échelle de la planche.
    u = 2.0
    A(rect(130 - u / 2, 94, u, 24, "encre"))
    A(rect_bord(106, 118, 64, 30, "papier", "filet-1"))
    h_air = cop["part_air"] * u
    A(rect(V_MARGE, 128, 106 - V_MARGE - 6, h_air, "clair"))
    A(fleche(104, 128 + h_air / 2, "encre", "droite", 7))
    l_chal = cop["rapport"] * u
    A(rect(138 - l_chal / 2, 148, l_chal, 10, "clair"))
    A(fleche(138, 160, "encre", "bas", 7))
    A(texte(V_MARGE, 152, f'COP{NN}4,60', "mono", 10, 500, "pivot",
            tabulaire=True))

    # L'autre départ, muet — un bloc calcaire.
    A(ligne(230, 94, 230, 118, "encre", 1.2))
    A(rect(200, 118, 86, 30, "calcaire"))

    # La dalle et sa serpentine.
    A(rect(88, 162, 198, 16, "calcaire"))
    y_h, y_b = 166, 174
    xs, pas_s = 96, 18
    pts = [(xs, y_b)]
    monte = True
    while xs + pas_s <= 278:
        pts.append((xs, y_h if monte else y_b))
        xs += pas_s
        pts.append((xs, y_h if monte else y_b))
        monte = not monte
    pts.append((xs, y_h if monte else y_b))
    A(polyligne(pts, "encre", 1))

    A("</svg>")
    controles = {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": f"carte de projet mesurée de 274 à 296 px — "
                            f"échelle {274/VW:.2f} à {296/VW:.2f}",
        "corps_minimal": f"9 px dans le repère — rendu à {9*274/VW:.1f} px au pire cas",
        "motif": f"le bandeau des {N_MODULES} modules, la descente, la barre, "
                 "l'échange réseau à deux flèches, les trois bandes du COP "
                 "(2 / 7,2 / 9,2 px) et la dalle — libellés d'organes, "
                 "étiquettes d'échange et bloc des autres départs laissés à "
                 "la planche",
        "bas_du_dessin": "dalle jusqu'à y 178, marge basse 22 px",
    }
    return "\n".join(out) + "\n", controles


if __name__ == "__main__":
    executer(composer, composer_vignette)
