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

Le second mécanisme (`franchissement`, passerelle du Carreau d'Or) garde le même
motif — une arrivée, une barre, des départs — et lui donne pour sujet ce que les
départs doivent TRAVERSER pour atteindre ce qu'ils desservent : la tension (deux
départs passent en 48 V dans les mains courantes), le joint mobile (6,80 m de
tablier coulissent, franchis par un enrouleur dont le câble est coté plus long
que la course) et la limite du réseau public (un raccordement refusé, un mât
rapatrié sur le coffret). Trois longueurs et deux hauteurs sont portées à une
échelle unique dérivée du tablier ; tout le reste est topologique.

Cinquième module du chantier après `sankey-energie.py`, `zonage-ssi.py`,
`coupe-traversee.py` et `boucle-fluide.py`. Le tronc commun (jetons, mesure des
chasses, insécables, double écriture des couleurs, routine d'exécution) vit dans
`_tronc.py`.
"""

from _tronc import (NN, INS, JETON, W, H, MARGE, UTILE, VW, VH, V_MARGE, AW, AH,
                    A_MARGE, mesurer, replier, echapper, texte, rect,
                    rect_bord, ligne, polyligne, fleche, cercle, entete_style,
                    racine_appui, controles_appui, executer)


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


def composer_appui(donnees):
    """L'appui du hero : le motif entier à l'échelle 1, trois nœuds chiffrés.

    Ce qu'il garde : le bandeau des 48 modules, la descente, la barre,
    l'échange réseau (deux flèches, légendées sous le bloc), les trois bandes
    du COP et la dalle — avec 17,5 kWc, COP 4,60 et le régime 30/35 °C. Ce
    qu'il laisse : les détails de pose des modules, le contenu des autres
    départs, la phrase de principe et le cartouche (le hero porte sa légende
    de carte sous le dessin)."""
    t = donnees["tableau"]
    elems = {e["cle"]: e for e in t["elements"]}
    cop = t["cop"]
    out = []
    A = out.append
    racine_appui(A, donnees)

    # ── Le bandeau des 48 modules et son nœud chiffré ────────────────────────
    at0, at1 = 150, AW - A_MARGE
    pas = (at1 - at0) / N_MODULES
    for k in range(N_MODULES):
        A(rect(at0 + k * pas, 52, pas - 1.8, 20, "clair"))
    A(ligne(at0, 74, at1, 74, "encre", 1.2))
    to = elems["toiture"]
    A(texte(A_MARGE, 62, "Toiture", "sans", 14, 600, "encre", wdth=112))
    A(texte(A_MARGE, 79, f'{to["valeur"]}{NN}{to["unite"]}', "mono", 11, 500,
            "pivot", tabulaire=True))

    # ── La descente d'autoconsommation et la barre ───────────────────────────
    x_cond = (at0 + at1) / 2
    A(ligne(x_cond, 74, x_cond, 144, "encre", 2))
    A(fleche(x_cond, 148, "encre", "bas", 8))
    A(texte(x_cond + 12, 116, t["liaison_autoconsommation"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    xb0, xb1 = 190, 510
    A(ligne(xb0, 150, xb1, 150, "encre", 2.5))
    A(texte(356, 172, elems["distribution"]["libelle"], "sans", 14, 600,
            "encre", wdth=112))

    # ── L'échange réseau : deux flèches, légendées sous le bloc ──────────────
    A(rect_bord(A_MARGE, 126, 100, 40, "papier", "filet-1"))
    A(texte(A_MARGE + 10, 142, "Réseau", "sans", 14, 600, "encre", wdth=112))
    A(texte(A_MARGE + 10, 158, "public", "sans", 14, 600, "encre", wdth=112))
    A(ligne(A_MARGE + 108, 136, xb0, 136, "encre", 1.2))
    A(fleche(A_MARGE + 106, 136, "encre", "gauche", 7))
    A(ligne(A_MARGE + 100, 158, xb0 - 6, 158, "encre", 1.2))
    A(fleche(xb0 - 4, 158, "encre", "droite", 7))
    A(fleche(34, 179, "encre", "gauche", 6))
    A(texte(46, 183, t["echange"]["vers_reseau"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    A(fleche(40, 195, "encre", "droite", 6))
    A(texte(46, 199, t["echange"]["du_reseau"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

    # ── Le départ suivi : les trois bandes du COP, à l'échelle 1 ─────────────
    u = UCOP                          # 1 kWh = 4 px, comme sur la planche
    x_elec = 300
    A(rect(x_elec - u / 2, 151.5, u, 188 - 151.5, "encre"))
    A(texte(x_elec - 12, 180, cop["entree"], "mono", 10, 500, "pivot",
            ancre="end", tracking=10 * 0.14))
    px0, px1, py0, py1 = 240, 400, 188, 248
    A(rect_bord(px0, py0, px1 - px0, py1 - py0, "papier", "filet-1"))
    pa = elems["pac"]
    A(texte(px0 + 14, py0 + 20, "Pompe à chaleur", "sans", 14, 600, "encre",
            wdth=112))
    A(texte(px0 + 14, py0 + 38, f'AIR/EAU · {pa["valeur"]}{NN}{pa["unite"]}',
            "mono", 10, 500, "pivot", tracking=10 * 0.14))
    A(texte(px0 + 14, py0 + 53, "COP 4,60", "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    h_air = cop["part_air"] * u
    A(rect(A_MARGE, 210, px0 - A_MARGE - 8, h_air, "clair"))
    A(fleche(px0 - 2, 210 + h_air / 2, "encre", "droite", 9))
    # Le libellé court — la version longue de l'extraction touchait « COP 4,60 »
    # dans la boîte voisine, mesuré au premier rendu à 552.
    A(texte(A_MARGE, 242, "CHALEUR PRISE À L’AIR", "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    l_chal = cop["rapport"] * u
    x_chal = 321
    A(rect(x_chal - l_chal / 2, py1, l_chal, 296 - py1, "clair"))
    A(fleche(x_chal, 298, "encre", "bas", 10))
    A(texte(x_chal + 20, 276, cop["sortie"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

    # ── L'autre départ, muet — un bloc calcaire légendé dessous ──────────────
    A(ligne(470, 151.5, 470, 184, "encre", 1.2))
    A(fleche(470, 188, "encre", "bas", 7))
    A(rect(424, 188, AW - A_MARGE - 424, 60, "calcaire"))
    A(texte(424, 262, "AUTRES DÉPARTS", "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

    # ── La dalle, sa serpentine, son nœud chiffré ────────────────────────────
    s_x0, s_x1, s_y0, s_y1 = 190, AW - A_MARGE, 302, 334
    A(rect(s_x0, s_y0, s_x1 - s_x0, s_y1 - s_y0, "calcaire"))
    y_h, y_b = s_y0 + 8, s_y1 - 8
    xs, pas_s = s_x0 + 12, 26
    pts = [(xs, y_b)]
    monte = True
    while xs + pas_s <= s_x1 - 12:
        pts.append((xs, y_h if monte else y_b))
        xs += pas_s
        pts.append((xs, y_h if monte else y_b))
        monte = not monte
    pts.append((xs, y_h if monte else y_b))
    A(polyligne(pts, "encre", 1))
    pl = elems["plancher"]
    A(texte(A_MARGE, 314, "Plancher chauffant", "sans", 14, 600, "encre",
            wdth=112))
    A(texte(A_MARGE, 331, f'RÉGIME{NN}{pl["valeur"]}{NN}{pl["unite"]}',
            "mono", 10, 500, "pivot", tracking=10 * 0.14))

    A("</svg>")
    return "\n".join(out) + "\n", controles_appui(
        motif=f"le motif entier à l'échelle 1 : bandeau des {N_MODULES} "
              "modules, descente, barre, échange réseau à deux flèches "
              "légendées, trois bandes du COP (4 / 14,4 / 18,4 px) et dalle — "
              "trois nœuds chiffrés (17,5 kWc, COP 4,60, régime 30/35 °C) ; "
              "détails de pose, contenu des départs, phrase et cartouche "
              "laissés à la planche",
        bas=f"dalle jusqu'à 334, régime à 331 — marge basse {AH - 334} px")


# ═════════════════════════════════════════════════════════════════════════════
#  MÉCANISME `franchissement` — une arrivée, cinq départs, trois frontières
# ═════════════════════════════════════════════════════════════════════════════
#
# Le motif de l'archétype est inchangé (arrivée → barre → départs) ; son SUJET
# change : ce que la planche suit n'est pas la distribution, c'est ce que les
# départs doivent traverser. Trois frontières, chacune dessinée par un dispositif
# différent et chacune doublée d'un texte (règle du signe jamais seul) :
#
#   1. la TENSION — deux départs d'éclairage traversent la boîte des blocs
#      d'alimentation et changent de poids de trait (1,5 px → 3 px) ;
#   2. le JOINT MOBILE — un pointillé vertical coupe le tablier ; le départ de
#      l'éclairage mobile passe dessous, par un enrouleur, et remonte de l'autre
#      côté. Deux cotes se rejoignent au joint et s'étendent en sens contraire :
#      10 m de câble contre 6,80 m de course, à la MÊME échelle ;
#   3. la LIMITE DU RÉSEAU PUBLIC — la descente vers le mât public existant est
#      barrée d'une croix, et un long départ venu de la barre alimente à la place
#      un mât dédié, plus court.
#
# Une seule échelle, dérivée du tablier (ECH = largeur dessinée / 25,40 m), porte
# les trois longueurs et les deux hauteurs de mât. Les linéaires de bandeau, eux,
# ne sont PAS tracés à l'échelle (43 m de ruban sur une partie fixe plus courte) :
# ce sont des cumuls, et le dessin le dit en toutes lettres.

# ── Registre haut : l'amont, le coffret, le réseau public ────────────────────
F_TAG_HAUT = 210
AM_X0, AM_X1, AM_Y0, AM_Y1 = 56, 268, 224, 302      # branchement existant
CF_X0, CF_X1, CF_Y0, CF_Y1 = 320, 600, 216, 306     # le coffret du banc
RS_X0, RS_X1, RS_Y0, RS_Y1 = 940, 1144, 216, 284    # le réseau public

# ── La barre et ses cinq départs ─────────────────────────────────────────────
Y_BARRE = 348
XB0, XB1 = 56, 930
X_DESCENTE = 460                                     # coffret → barre
TB_X0, TB_X1, TB_Y0, TB_Y1 = 76, 194, 372, 416       # les blocs 48 V
BL_Y0, BL_Y1 = 372, 430                              # les deux départs à bloc
PR_X0, PR_X1 = 340, 560                              # coffret de prises
MO_X0, MO_X1 = 600, 820                              # armoire de motorisation
X_D1, X_D2 = 100, 170                                # éclairages fixe / mobile
X_D4, X_D3, X_D5 = 450, 710, 930                     # prises / motorisation / mât

# ── Registre bas : le tablier, la seule chose tracée à l'échelle ─────────────
# Il occupe presque toute la largeur utile : c'est LUI le sujet de la fiche —
# un ouvrage qui s'ouvre —, pas la nomenclature des départs.
X_PONT0, X_PONT1 = 200, 900
Y_PONT0, Y_PONT1 = 502, 550
Y_COTE_LONG = 474                                    # la cote de 25,40 m
Y_LED = 494                                          # le bandeau à leds
Y_CABLE = 568                                        # la route du câble mobile
Y_COTE_COURSE = 592
Y_COTE_CABLE = 614
Y_MAT_ROUTE = 642                                    # le long départ vers le mât
Y_NOTE = 664
JEU_JOINT = 12                                       # le jeu où passe le câble

# ── Le quai et ses deux mâts ─────────────────────────────────────────────────
QU_X0, QU_X1 = 950, 1144
X_MAT_REFUSE, X_MAT_RETENU = 1010, 1100
X_RISER_MAT = 1060                                   # la remontée du long départ


def _pointille(x0, y0, x1, y1, cle, epaisseur=1.2, motif="4 5"):
    """Un trait discontinu — la frontière que le dessin ne franchit pas seul."""
    return (f'  <path d="M {x0:.2f} {y0:.2f} L {x1:.2f} {y1:.2f}" fill="none" '
            f'class="s-{cle}" stroke="{JETON[cle]}" '
            f'stroke-width="{epaisseur}" stroke-dasharray="{motif}"/>')


def _croix(x, y, taille, cle="encre", epaisseur=2.0):
    """La croix qui barre une route abandonnée — doublée d'une mention."""
    t = taille / 2
    return (f'  <path d="M {x-t:.2f} {y-t:.2f} L {x+t:.2f} {y+t:.2f} '
            f'M {x+t:.2f} {y-t:.2f} L {x-t:.2f} {y+t:.2f}" fill="none" '
            f'class="s-{cle}" stroke="{JETON[cle]}" stroke-width="{epaisseur}"/>')


def _cote(A, x0, x1, y, libelle, corps=10, patte=5, ecart=8):
    """Une ligne de cote : le trait, ses deux pattes, son libellé centré dessus.
    C'est ce trait — et lui seul — qui engage l'échelle du dessin."""
    A(ligne(x0, y, x1, y, "encre", 1))
    A(ligne(x0, y - patte, x0, y + patte, "encre", 1))
    A(ligne(x1, y - patte, x1, y + patte, "encre", 1))
    A(fleche(x0 + 0.5, y, "encre", "gauche", 7))
    A(fleche(x1 - 0.5, y, "encre", "droite", 7))
    A(texte((x0 + x1) / 2, y - ecart, libelle, "mono", corps, 500, "pivot",
            ancre="middle", tracking=corps * 0.14))


def _etiquette(A, x, y, chaine, corps=10, ancre=None, marge=6):
    """Une étiquette mono posée SUR un trait : un fond papier à sa mesure, puis
    le texte. C'est le procédé du dessin coté — le libellé interrompt la ligne
    qu'il annote au lieu de se laisser rayer par elle. Sans lui, les tags de
    frontière étaient traversés par les descentes qu'ils nomment."""
    l = mesurer(chaine, corps, "mono", corps * 0.14)
    x0 = x if ancre is None else (x - l if ancre == "end" else x - l / 2)
    A(rect(x0 - marge, y - corps - 2, l + 2 * marge, corps + 8, "papier"))
    A(texte(x, y, chaine, "mono", corps, 500, "pivot", ancre=ancre,
            tracking=corps * 0.14))
    return l


def _bobine(A, cx, cy, r):
    """L'enrouleur : un tambour et son câble enroulé — trois quarts de tour
    concentriques, tracés, jamais un pictogramme importé."""
    A(cercle(cx, cy, r, "papier", "encre", 1.5))
    A(cercle(cx, cy, r * 0.42, "papier", "encre", 1.2))


def composer_franchissement(donnees):
    f = donnees["franchissement"]
    tab = f["tablier"]
    mats = f["mats"]
    out = []
    A = out.append
    depassements = []

    def controler(nom, chaine, corps, profil, dispo, tracking=0.0):
        largeur = mesurer(chaine, corps, profil, tracking)
        if largeur > dispo:
            depassements.append(f"{nom} : {largeur:.0f} px pour {dispo:.0f} px")
        return largeur

    def mono(x, y, chaine, dispo=None, nom=None, ancre=None, corps=10):
        if dispo is not None:
            controler(nom or chaine, chaine, corps, "mono", dispo, corps * 0.14)
        A(texte(x, y, chaine, "mono", corps, 500, "pivot", ancre=ancre,
                tracking=corps * 0.14))

    # ── L'échelle : dérivée du tablier, jamais choisie ───────────────────────
    long_m = float(tab["longueur"].replace(",", "."))
    mob_m = float(tab["mobile"].replace(",", "."))
    ech = (X_PONT1 - X_PONT0) / long_m
    x_joint = X_PONT1 - mob_m * ech
    x_enrouleur = x_joint - 10.0 * ech          # 10 m de câble, même échelle
    h_refuse = float(mats["abandonne"]["hauteur"].replace(",", ".")) * ech
    h_retenu = float(mats["retenu"]["hauteur"].replace(",", ".")) * ech

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
    A(texte(MARGE, Y_SOUSTITRE, donnees["sous_titre"], "sans", 16, 400,
            "pivot", wdth=100))
    A(rect(MARGE, Y_FILET_TITRE, UTILE, 1, "filet-1"))
    mono(MARGE, Y_ENTETE, f["entete"], UTILE, "en-tête du schéma")

    # ── AMONT — le branchement conservé ──────────────────────────────────────
    mono(MARGE, F_TAG_HAUT, f["tag_amont"], 600, "tag amont")
    am = f["amont"]
    A(rect_bord(AM_X0, AM_Y0, AM_X1 - AM_X0, AM_Y1 - AM_Y0, "papier", "filet-1"))
    controler("libellé amont", am["libelle"], 15, "sans-400", AM_X1 - AM_X0 - 32)
    A(texte(AM_X0 + 16, AM_Y0 + 30, am["libelle"], "sans", 15, 400, "encre",
            wdth=100))
    for k, l in enumerate(am["detail"]):
        mono(AM_X0 + 16, AM_Y0 + 52 + k * 16, l, AM_X1 - AM_X0 - 32,
             f"détail amont {k + 1}")
    A(ligne(AM_X1, (AM_Y0 + AM_Y1) / 2, CF_X0 - 10, (AM_Y0 + AM_Y1) / 2,
            "encre", 1.5))
    A(fleche(CF_X0 - 2, (AM_Y0 + AM_Y1) / 2, "encre", "droite", 9))

    # ── LE COFFRET — la source unique de tout l'ouvrage ──────────────────────
    co = f["coffret"]
    A(rect_bord(CF_X0, CF_Y0, CF_X1 - CF_X0, CF_Y1 - CF_Y0, "calcaire", "filet-1"))
    controler("libellé coffret", co["libelle"], 15, "sans-400", CF_X1 - CF_X0 - 32)
    A(texte(CF_X0 + 16, CF_Y0 + 36, co["libelle"], "sans", 15, 400, "encre",
            wdth=100))
    for k, l in enumerate(co["detail"]):
        mono(CF_X0 + 16, CF_Y0 + 60 + k * 16, l, CF_X1 - CF_X0 - 32,
             f"détail coffret {k + 1}")

    # ── LE RÉSEAU PUBLIC — le hors-périmètre, en haut à droite ───────────────
    re_ = f["reseau"]
    A(rect_bord(RS_X0, RS_Y0, RS_X1 - RS_X0, RS_Y1 - RS_Y0, "papier", "filet-1"))
    controler("libellé réseau", re_["libelle"], 15, "sans-400", RS_X1 - RS_X0 - 32)
    A(texte(RS_X0 + 16, RS_Y0 + 34, re_["libelle"], "sans", 15, 400, "encre",
            wdth=100))
    for k, l in enumerate(re_["detail"]):
        mono(RS_X0 + 16, RS_Y0 + 56 + k * 16, l, RS_X1 - RS_X0 - 32,
             f"détail réseau {k + 1}")

    # ── LA BARRE ET SES CINQ DÉPARTS ─────────────────────────────────────────
    A(ligne(X_DESCENTE, CF_Y1, X_DESCENTE, Y_BARRE - 6, "encre", 2))
    A(fleche(X_DESCENTE, Y_BARRE - 2, "encre", "bas", 9))
    mono(XB0, Y_BARRE - 14, f["tag_barre"], X_DESCENTE - XB0 - 20, "tag de la barre")
    A(ligne(XB0, Y_BARRE, XB1, Y_BARRE, "encre", 3))

    # FRONTIÈRE 1 — la tension. Les deux départs d'éclairage traversent la
    # boîte des blocs d'alimentation et changent de POIDS DE TRAIT en sortant.
    fr = {b["cle"]: b for b in f["frontieres"]}
    for x in (X_D1, X_D2):
        A(ligne(x, Y_BARRE + 1.5, x, TB_Y0, "encre", 1.5))     # 400/230 V
    A(rect_bord(TB_X0, TB_Y0, TB_X1 - TB_X0, TB_Y1 - TB_Y0, "calcaire", "filet-1"))
    # Le trait de conversion : au-dessus le 400/230 V, au-dessous le 48 V.
    A(ligne(TB_X0, (TB_Y0 + TB_Y1) / 2, TB_X1, (TB_Y0 + TB_Y1) / 2, "filet-1", 1))
    mono(TB_X1 + 10, TB_Y0 + 14, fr["tension"]["amont"], PR_X0 - TB_X1 - 20,
         "étiquette amont tension")
    mono(TB_X1 + 10, TB_Y0 + 38, fr["tension"]["aval"], PR_X0 - TB_X1 - 20,
         "étiquette aval tension")

    # Départ 1 — l'éclairage de la partie fixe : il rejoint le bandeau.
    A(ligne(X_D1, TB_Y1, X_D1, Y_LED, "encre", 3))
    A(ligne(X_D1, Y_LED, X_PONT0 - 12, Y_LED, "encre", 3))
    A(fleche(X_PONT0 - 2, Y_LED, "encre", "droite", 10))

    # Départ 2 — l'éclairage de la partie mobile : il passe SOUS le tablier.
    A(ligne(X_D2, TB_Y1, X_D2, Y_CABLE, "encre", 3))
    A(ligne(X_D2, Y_CABLE, x_enrouleur - 24, Y_CABLE, "encre", 3))
    A(fleche(x_enrouleur - 14, Y_CABLE, "encre", "droite", 10))

    # Le tag se pose SOUS la boîte, SUR les deux descentes qu'il qualifie : son
    # fond papier les interrompt — d'où l'ordre, après elles et non avant.
    controler("tag frontière 1", fr["tension"]["tag"], 10, "mono",
              PR_X0 - MARGE - 28, 1.4)
    _etiquette(A, MARGE, TB_Y1 + 18, fr["tension"]["tag"])

    # Départs 3 et 4 — deux blocs terminaux, sans appareil.
    for (x0, x1, xd, cle) in ((PR_X0, PR_X1, X_D4, "prises"),
                              (MO_X0, MO_X1, X_D3, "motorisation")):
        el = next(e for e in f["elements"] if e["cle"] == cle)
        A(ligne(xd, Y_BARRE + 1.5, xd, BL_Y0 - 6, "encre", 1.5))
        A(fleche(xd, BL_Y0 - 2, "encre", "bas", 8))
        A(rect(x0, BL_Y0, x1 - x0, BL_Y1 - BL_Y0, "calcaire"))
        controler(f"libellé {cle}", el["libelle"], 15, "sans-400", x1 - x0 - 24)
        A(texte(x0 + 12, BL_Y0 + 24, el["libelle"], "sans", 15, 400, "encre",
                wdth=100))
        for k, l in enumerate(el["detail"][:2]):
            mono(x0 + 12, BL_Y0 + 42 + k * 14, l, x1 - x0 - 24,
                 f"détail {cle} {k + 1}")

    # ── LE TABLIER — la bande cotée, et le joint qui la coupe ────────────────
    controler("tag de l'ouvrage", f["tag_ouvrage"], 10, "mono",
              X_PONT1 - X_PONT0, 1.4)
    _etiquette(A, X_PONT0, Y_COTE_LONG - 18, f["tag_ouvrage"])
    x_mobile = x_joint + JEU_JOINT              # le jeu où le câble remonte
    x_riser = x_joint + JEU_JOINT / 2
    A(rect_bord(X_PONT0, Y_PONT0, x_joint - X_PONT0, Y_PONT1 - Y_PONT0,
                "calcaire", "filet-1"))
    A(rect_bord(x_mobile, Y_PONT0, X_PONT1 - x_mobile,
                Y_PONT1 - Y_PONT0, "papier", "filet-1"))
    mono(X_PONT0 + 12, (Y_PONT0 + Y_PONT1) / 2 + 4, tab["tag_fixe"],
         x_joint - X_PONT0 - 24, "tag partie fixe")
    mono(x_mobile + 10, (Y_PONT0 + Y_PONT1) / 2 + 4, tab["tag_mobile"],
         X_PONT1 - x_mobile - 20, "tag partie mobile")
    _cote(A, X_PONT0, X_PONT1, Y_COTE_LONG, tab["cote_longueur"])

    # FRONTIÈRE 2 — le joint mobile.
    A(_pointille(x_joint, BL_Y1 + 8, x_joint, Y_MAT_ROUTE - 12, "encre", 1.4))
    controler("tag frontière 2", fr["joint"]["tag"], 10, "mono", 400, 1.4)
    _etiquette(A, x_joint, Y_MAT_ROUTE + 2, fr["joint"]["tag"], ancre="middle")

    # Le bandeau à leds : deux segments, coupés par le joint.
    ba = f["bandeaux"]
    A(ligne(X_PONT0, Y_LED, x_joint, Y_LED, "encre", 3))
    A(ligne(x_riser, Y_LED, X_PONT1, Y_LED, "encre", 3))
    mono(X_PONT0 + 6, Y_LED - 8, ba["fixe"], x_joint - X_PONT0 - 12,
         "étiquette bandeau fixe")
    mono(X_PONT1, Y_LED - 8, ba["mobile"], X_PONT1 - x_mobile - 8,
         "étiquette bandeau mobile", ancre="end")
    mono(MARGE, Y_NOTE, ba["note"], UTILE, "note des linéaires")

    # L'enrouleur, et les DEUX COTES qui se rejoignent au joint : le câble d'un
    # côté, la course de l'autre — à la même échelle, c'est la démonstration.
    _bobine(A, x_enrouleur, Y_CABLE, 13)
    A(ligne(x_enrouleur + 13, Y_CABLE, x_riser, Y_CABLE, "encre", 3))
    A(ligne(x_riser, Y_CABLE, x_riser, Y_LED + 8, "encre", 3))
    A(fleche(x_riser, Y_LED + 1, "encre", "haut", 10))
    _cote(A, x_joint, X_PONT1, Y_COTE_COURSE, tab["cote_mobile"])
    _cote(A, x_enrouleur, x_joint, Y_COTE_CABLE, tab["cote_cable"])

    # ── FRONTIÈRE 3 — la limite du réseau public, et les deux mâts ───────────
    mono(X_MAT_REFUSE - 16, RS_Y1 + 40, fr["reseau"]["tag"],
         X_MAT_REFUSE - CF_X1 - 40, "tag frontière 3", ancre="end")
    A(ligne(QU_X0, Y_PONT1, QU_X1, Y_PONT1, "encre", 1.5))
    mono((X_MAT_REFUSE + X_MAT_RETENU) / 2, F_TAG_HAUT + 178, f["tag_quai"],
         QU_X1 - QU_X0, "tag du quai", ancre="middle")

    # Le mât public existant : jamais construit, donc jamais plein — le trait
    # discontinu le dit, la croix barre son alimentation, la mention la nomme.
    ab = mats["abandonne"]
    y_haut_refuse = Y_PONT1 - h_refuse
    A(_pointille(X_MAT_REFUSE, RS_Y1, X_MAT_REFUSE, y_haut_refuse - 18,
                 "encre", 1.6, "5 5"))
    A(_croix(X_MAT_REFUSE, (RS_Y1 + y_haut_refuse) / 2, 20))
    A(_pointille(X_MAT_REFUSE, y_haut_refuse, X_MAT_REFUSE, Y_PONT1,
                 "encre", 2.4, "6 5"))
    A(rect(X_MAT_REFUSE - 6, y_haut_refuse - 8, 12, 8, "filet-1"))
    mono(X_MAT_REFUSE, Y_PONT1 + 20, ab["cote"], 66, "cote mât refusé",
         ancre="middle")
    mono(X_MAT_REFUSE, Y_PONT1 + 34, ab["mention"], 66, "mention mât refusé",
         ancre="middle")

    # Le mât dédié : alimenté depuis le banc, par le plus long des départs.
    rt = mats["retenu"]
    y_haut_retenu = Y_PONT1 - h_retenu
    A(ligne(X_D5, Y_BARRE + 1.5, X_D5, Y_MAT_ROUTE, "encre", 1.5))
    A(ligne(X_D5, Y_MAT_ROUTE, X_RISER_MAT, Y_MAT_ROUTE, "encre", 1.5))
    A(ligne(X_RISER_MAT, Y_MAT_ROUTE, X_RISER_MAT, Y_PONT1 + 8, "encre", 1.5))
    A(fleche(X_RISER_MAT, Y_PONT1 + 2, "encre", "haut", 9))
    A(ligne(X_RISER_MAT, Y_PONT1, X_MAT_RETENU, Y_PONT1, "encre", 1.5))
    A(ligne(X_MAT_RETENU, Y_PONT1, X_MAT_RETENU, y_haut_retenu, "encre", 3.5))
    A(rect(X_MAT_RETENU - 6, y_haut_retenu - 8, 12, 8, "encre"))
    mono(X_MAT_RETENU, Y_PONT1 + 20, rt["cote"], 66, "cote mât retenu",
         ancre="middle")
    mono(X_MAT_RETENU, Y_PONT1 + 34, rt["mention"], 66, "mention mât retenu",
         ancre="middle")

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
        "echelle": f"{ech:.4f} px/m, dérivée du tablier ({X_PONT1 - X_PONT0} px "
                   f"pour {tab['longueur']} m) — elle porte les trois longueurs "
                   f"et les deux hauteurs, rien d'autre",
        "demonstration": f"une arrivée, une barre, cinq départs, et trois "
                         f"frontières franchies : la TENSION (deux départs "
                         f"traversent la boîte des blocs et passent de 1,5 à "
                         f"3 px de trait), le JOINT MOBILE (pointillé à x "
                         f"{x_joint:.1f} ; deux cotes s'y rejoignent en sens "
                         f"contraire — câble {10 * ech:.1f} px contre course "
                         f"{mob_m * ech:.1f} px, soit 10 m contre "
                         f"{tab['mobile']} m à la même échelle), le RÉSEAU "
                         f"PUBLIC (descente barrée d'une croix vers un mât de "
                         f"{h_refuse:.1f} px, contre un mât de "
                         f"{h_retenu:.1f} px alimenté depuis la barre par le "
                         f"plus long départ)",
        "topologie": f"amont x {AM_X0}–{AM_X1} → coffret x {CF_X0}–{CF_X1} → "
                     f"descente x {X_DESCENTE} → barre y {Y_BARRE}, x {XB0}–"
                     f"{XB1} ; départs x {X_D1}, {X_D2}, {X_D4}, {X_D3}, "
                     f"{X_D5} ; tablier y {Y_PONT0}–{Y_PONT1}, x {X_PONT0}–"
                     f"{X_PONT1}, joint à {x_joint:.1f} ; enrouleur à "
                     f"{x_enrouleur:.1f} ; quai x {QU_X0}–{QU_X1}",
        "cotes_a_l_echelle": f"25,40 m = {X_PONT1 - X_PONT0} px · "
                             f"{tab['mobile']} m = {mob_m * ech:.1f} px · "
                             f"10 m de câble = {10 * ech:.1f} px · "
                             f"{mats['abandonne']['hauteur']} m = "
                             f"{h_refuse:.1f} px · "
                             f"{mats['retenu']['hauteur']} m = "
                             f"{h_retenu:.1f} px — rapport câble/course "
                             f"{10 / mob_m:.3f}, conforme à 10 ÷ {tab['mobile']}",
        "linéaires_non_cotés": "les 43 m et 28 m de bandeau sont des CUMULS, "
                               "portés en étiquette et jamais tracés à "
                               "l'échelle ; la note du dessin le dit",
        "bas_du_dessin": f"cote de câble à {Y_COTE_CABLE}, départ du mât à "
                         f"{Y_MAT_ROUTE}, note à {Y_NOTE}, phrase de principe à "
                         f"{Y_PHRASE}, cartouche {Y_CARTOUCHE}–"
                         f"{Y_CARTOUCHE + H_CARTOUCHE}, marge basse "
                         f"{H - (Y_CARTOUCHE + H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur * H_CARTOUCHE} px², soit "
                            f"{largeur * H_CARTOUCHE / (W * H) * 100:.2f} % "
                            f"de la planche",
        "releve": "aucun — la démonstration est géométrique, les chiffres de la "
                  "fiche restent à la fiche (révision 4)",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l'échelle "
                         f"0,96 (1152 / {W})",
        "phrase_principe": f"{len(donnees['phrase_principe'])} signes — "
                           f"{l_phrase:.0f} px mesurés pour {UTILE} disponibles",
        "depassements": depassements if depassements
                        else "aucun — toutes les lignes mesurées sous leur colonne",
    }
    return "\n".join(out) + "\n", controles


def composer_vignette_franchissement(donnees):
    """La vignette : la thèse seule, et rien de l'appareil.

    Premier essai gardé la nomenclature entière — coffret, boîte 48 V, blocs de
    prises et de motorisation : dans la carte de 274 px, quatre rectangles
    calcaire muets occupaient 40 % du dessin. Ce qui reste ici est ce qui
    démontre : la barre et son éventail, le tablier coupé par son joint, et les
    DEUX COTES qui s'y rejoignent en sens contraire — le câble plus long que la
    course. Plus les deux mâts, dont l'un barré. Le reste est à la planche."""
    f = donnees["franchissement"]
    tab = f["tablier"]
    mats = f["mats"]
    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false" '
      f'style="width:100%;height:auto;display:block">')
    entete_style(A)
    A(rect(0, 0, VW, VH, "papier"))
    A(texte(V_MARGE, 22, donnees["vignette_surtitre"], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    long_m = float(tab["longueur"].replace(",", "."))
    mob_m = float(tab["mobile"].replace(",", "."))
    px0, px1 = 80, 244
    ech = (px1 - px0) / long_m
    xj = px1 - mob_m * ech
    xe = xj - 10.0 * ech
    y_pont0, y_pont1 = 118, 140
    y_led, y_cable = 108, 154

    # La source et la barre : cinq départs, dont deux qui changent de tension.
    A(rect(46, 44, 18, 10, "encre"))
    A(ligne(55, 54, 55, 62, "encre", 1.5))
    A(ligne(30, 66, 252, 66, "encre", 2.4))
    for x in (40, 62, 120, 175, 250):
        A(ligne(x, 67, x, 78, "encre", 1))
    # La conversion : un filet en travers des deux départs d'éclairage.
    A(ligne(32, 86, 74, 86, "filet-1", 1.2))
    A(texte(V_MARGE, 100, f'48{NN}V', "mono", 10, 500, "pivot", tracking=1.4))
    A(ligne(40, 86, 40, y_led, "encre", 2.4))
    A(ligne(40, y_led, px0, y_led, "encre", 2.4))
    A(ligne(62, 86, 62, y_cable, "encre", 2.4))
    A(ligne(62, y_cable, xe - 7, y_cable, "encre", 2.4))

    # Le tablier, coupé par son joint.
    A(rect_bord(px0, y_pont0, xj - px0, y_pont1 - y_pont0,
                "calcaire", "filet-1"))
    A(rect_bord(xj + 5, y_pont0, px1 - xj - 5, y_pont1 - y_pont0,
                "papier", "filet-1"))
    A(ligne(px0, y_led, xj, y_led, "encre", 2.4))
    A(ligne(xj + 3, y_led, px1, y_led, "encre", 2.4))
    A(_pointille(xj, 96, xj, 184, "encre", 1.1, "3 4"))

    # L'enrouleur et les deux cotes — la démonstration, en petit.
    A(cercle(xe, y_cable, 5.5, "papier", "encre", 1.2))
    A(ligne(xe + 5.5, y_cable, xj + 3, y_cable, "encre", 2.4))
    A(ligne(xj + 3, y_cable, xj + 3, y_led, "encre", 2.4))
    for (a, b, y, lib, ancre, xt) in (
            (xj, px1, 168, f'{tab["mobile"]}{NN}m', "end", px1),
            (xe, xj, 186, f'10{NN}m', "middle", (xe + xj) / 2)):
        A(ligne(a, y, b, y, "encre", 1))
        A(ligne(a, y - 4, a, y + 4, "encre", 1))
        A(ligne(b, y - 4, b, y + 4, "encre", 1))
        A(texte(xt, y - 5, lib, "mono", 9, 500, "pivot", ancre=ancre,
                tracking=1.26))

    # Les deux mâts : l'un jamais construit et son alimentation barrée, l'autre
    # alimenté depuis la barre par le plus long des départs.
    h_ref = float(mats["abandonne"]["hauteur"].replace(",", ".")) * ech
    h_ret = float(mats["retenu"]["hauteur"].replace(",", ".")) * ech
    A(ligne(254, y_pont1, 286, y_pont1, "encre", 1.2))
    A(_pointille(262, y_pont1, 262, y_pont1 - h_ref, "encre", 2, "5 4"))
    A(_pointille(262, 44, 262, y_pont1 - h_ref - 6, "encre", 1.2, "4 4"))
    A(_croix(262, 62, 12, "encre", 1.8))
    # Le long départ longe le bord droit plutôt que de traverser le dessin :
    # tracé à travers, il fermait un rectangle qui se lisait comme une boîte.
    A(ligne(250, 78, 250, 178, "encre", 1.2))
    A(ligne(250, 178, 282, 178, "encre", 1.2))
    A(ligne(282, 178, 282, y_pont1, "encre", 1.2))
    A(ligne(282, y_pont1, 282, y_pont1 - h_ret, "encre", 2.8))

    A("</svg>")
    controles = {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": f"carte de projet mesurée de 274 à 296 px — "
                            f"échelle {274/VW:.2f} à {296/VW:.2f}",
        "corps_minimal": f"9 px dans le repère — rendu à {9*274/VW:.1f} px au pire cas",
        "motif": f"la barre et son éventail de cinq départs, le tablier coupé "
                 f"au joint (x {xj:.1f}), l'enrouleur et les deux cotes qui s'y "
                 f"rejoignent en sens contraire ({10 * ech:.1f} px de câble "
                 f"contre {mob_m * ech:.1f} px de course), les deux mâts dont "
                 f"un barré — un seul nœud chiffré au texte, 48 V. Coffret, "
                 f"amont, réseau public et blocs de départ laissés à la "
                 f"planche : quatre rectangles muets mangeaient 40 % du dessin "
                 f"dans la carte de 274 px",
        "bas_du_dessin": "cote de câble à 186, route du mât à 184 — marge basse "
                         "14 px, aucun trait ne touche un bord",
    }
    return "\n".join(out) + "\n", controles


def composer_appui_franchissement(donnees):
    """L'appui du hero : le motif entier à l'échelle 1, trois nœuds chiffrés.

    Ce qu'il garde : le coffret, la barre, les cinq départs, la boîte 48 V
    légendée, le tablier coté, le joint, l'enrouleur et ses deux cotes, les deux
    mâts cotés dont l'un barré. Ce qu'il laisse : l'amont, le réseau public, le
    contenu des blocs de départ, la note des linéaires, la phrase de principe et
    le cartouche (le hero porte sa légende de carte sous le dessin)."""
    f = donnees["franchissement"]
    tab = f["tablier"]
    mats = f["mats"]
    out = []
    A = out.append
    racine_appui(A, donnees)

    long_m = float(tab["longueur"].replace(",", "."))
    mob_m = float(tab["mobile"].replace(",", "."))
    px0, px1 = 150, 400
    ech = (px1 - px0) / long_m
    xj = px1 - mob_m * ech
    xe = xj - 10.0 * ech
    y_pont0, y_pont1 = 224, 256
    y_led = 214
    y_cable = 276
    x_ref, x_ret, x_riser = 440, 505, 470   # l'écart des mâts EST la largeur
    #                                          des étiquettes qu'ils portent

    # ── Le coffret et la barre ───────────────────────────────────────────────
    A(rect_bord(A_MARGE, 56, 124, 42, "calcaire", "filet-1"))
    A(texte(A_MARGE + 12, 78, "Coffret unique", "sans", 14, 600, "encre",
            wdth=112))
    A(texte(A_MARGE + 12, 92, "DANS LE BANC", "mono", 10, 500, "pivot",
            tracking=1.4))
    A(ligne(86, 98, 86, 112, "encre", 2))
    A(fleche(86, 116, "encre", "bas", 8))
    A(ligne(A_MARGE + 10, 120, 415, 120, "encre", 2.5))

    # ── Frontière 1 — la tension : un filet en travers des deux éclairages ───
    for x in (50, 84):
        A(ligne(x, 121.5, x, 138, "encre", 1.5))
    A(rect_bord(38, 138, 62, 26, "calcaire", "filet-1"))
    A(ligne(38, 151, 100, 151, "filet-1", 1))
    A(texte(108, 146, f'400/230{NN}V', "mono", 10, 500, "pivot", tracking=1.4))
    A(texte(108, 166, f'48{NN}V', "mono", 10, 500, "pivot", tracking=1.4))

    # Départ 1 — le bandeau de la partie fixe.
    A(ligne(50, 164, 50, y_led, "encre", 3))
    A(ligne(50, y_led, px0 - 10, y_led, "encre", 3))
    A(fleche(px0 - 2, y_led, "encre", "droite", 9))
    # Départ 2 — sous le tablier, jusqu'à l'enrouleur.
    A(ligne(84, 164, 84, y_cable, "encre", 3))
    A(ligne(84, y_cable, xe - 18, y_cable, "encre", 3))
    A(fleche(xe - 10, y_cable, "encre", "droite", 9))

    # ── Départs 3 et 4 — deux blocs muets, nommés dessous ────────────────────
    for x, l in ((225, "PRISES"), (330, "MOTORISATION")):
        A(ligne(x, 121.5, x, 146, "encre", 1.2))
        A(fleche(x, 150, "encre", "bas", 7))
        A(rect(x - 46, 150, 92, 22, "calcaire"))
        A(texte(x, 186, l, "mono", 10, 500, "pivot", ancre="middle",
                tracking=1.4))

    # ── Le tablier, le joint, le bandeau ─────────────────────────────────────
    A(rect_bord(px0, y_pont0, xj - px0, y_pont1 - y_pont0,
                "calcaire", "filet-1"))
    A(rect_bord(xj + 6, y_pont0, px1 - xj - 6, y_pont1 - y_pont0,
                "papier", "filet-1"))
    A(ligne(px0, y_led, xj, y_led, "encre", 3))
    A(ligne(xj + 3, y_led, px1, y_led, "encre", 3))
    A(_pointille(xj, 200, xj, 330, "encre", 1.3))
    A(texte(px0 + 10, y_pont1 - 11, tab["tag_fixe"], "mono", 10, 500, "pivot",
            tracking=1.4))

    # ── L'enrouleur et les deux cotes qui se rejoignent au joint ─────────────
    A(cercle(xe, y_cable, 9, "papier", "encre", 1.5))
    A(cercle(xe, y_cable, 3.8, "papier", "encre", 1.2))
    A(ligne(xe + 9, y_cable, xj + 3, y_cable, "encre", 3))
    A(ligne(xj + 3, y_cable, xj + 3, y_led + 8, "encre", 3))
    A(fleche(xj + 3, y_led + 1, "encre", "haut", 9))
    _cote(A, xj, px1, 300, f'{tab["mobile"]}{NN}m')
    _cote(A, xe, xj, 322, f'10{NN}m DE CÂBLE')

    # ── Les deux mâts ────────────────────────────────────────────────────────
    h_ref = float(mats["abandonne"]["hauteur"].replace(",", ".")) * ech
    h_ret = float(mats["retenu"]["hauteur"].replace(",", ".")) * ech
    A(ligne(425, y_pont1, AW - A_MARGE, y_pont1, "encre", 1.5))
    A(_pointille(x_ref, y_pont1, x_ref, y_pont1 - h_ref, "encre", 2, "6 5"))
    A(_pointille(x_ref, 126, x_ref, y_pont1 - h_ref - 12, "encre", 1.4, "5 5"))
    A(_croix(x_ref, 150, 16, "encre", 1.8))
    A(ligne(415, 121.5, 415, 310, "encre", 1.5))
    A(ligne(415, 310, x_riser, 310, "encre", 1.5))
    A(ligne(x_riser, 310, x_riser, y_pont1 + 8, "encre", 1.5))
    A(fleche(x_riser, y_pont1 + 2, "encre", "haut", 8))
    A(ligne(x_riser, y_pont1, x_ret, y_pont1, "encre", 1.5))
    A(ligne(x_ret, y_pont1, x_ret, y_pont1 - h_ret, "encre", 3.5))
    for x, m in ((x_ref, mats["abandonne"]), (x_ret, mats["retenu"])):
        A(texte(x, y_pont1 + 20, m["cote"], "mono", 10, 500, "pivot",
                ancre="middle", tracking=1.4))
        A(texte(x, y_pont1 + 34, m["mention"], "mono", 10, 500, "pivot",
                ancre="middle", tracking=1.4))

    A("</svg>")
    return "\n".join(out) + "\n", controles_appui(
        motif=f"le motif entier à l'échelle 1 : coffret, barre, cinq départs, "
              f"le filet de conversion et ses deux tensions, tablier coupé au "
              f"joint (x {xj:.1f}), enrouleur et les deux cotes qui s'y "
              f"rejoignent ({10 * ech:.1f} px de câble contre "
              f"{mob_m * ech:.1f} px de course), deux mâts cotés dont un barré "
              f"— trois nœuds chiffrés (48 V, 10 m, {tab['mobile']} m) ; amont, "
              f"réseau public, note des linéaires, phrase et cartouche laissés "
              f"à la planche",
        bas=f"cote de câble à 322, route du mât à 336 — marge basse {AH - 336} px",
        ecart_des_mats=f"mâts à x {x_ref} et {x_ret} : l'écart de "
                       f"{x_ret - x_ref} px est celui qu'imposent leurs deux "
                       f"étiquettes centrées (43 px chacune) ; la remontée du "
                       f"long départ passe à x {x_riser}, dans l'intervalle",
        echelle=f"{ech:.4f} px/m, dérivée du tablier — même construction que la "
                f"planche, à son échelle propre")


def _composer(donnees):
    if "franchissement" in donnees:
        return composer_franchissement(donnees)
    return composer(donnees)


def _composer_vignette(donnees):
    if "franchissement" in donnees:
        return composer_vignette_franchissement(donnees)
    return composer_vignette(donnees)


def _composer_appui(donnees):
    if "franchissement" in donnees:
        return composer_appui_franchissement(donnees)
    return composer_appui(donnees)


if __name__ == "__main__":
    executer(_composer, _composer_vignette, _composer_appui)
