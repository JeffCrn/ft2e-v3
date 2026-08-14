#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compositeur de planche — archétype `chronologie-affaire`.

Protocole : docs/superpowers/specs/2026-08-12-planches-references-protocole.md

Il lit un `planche.json` (l'extraction, produite par la session de génération) et
écrit les trois dessins qui en découlent :

    planche.svg    1200 x 800 — la planche de fiche, lue à 1152 px (échelle 0,96)
    vignette.svg    300 x 200 — la vignette de carte, lue à 274-296 px (0,91-0,99)
    appui.svg       552 x 368 — l'appui du hero de l'accueil, lu à ~552 px (1,0)

Usage :

    python scripts/planches/chronologie-affaire.py public/images/projets/<slug>

La géométrie est CALCULÉE : aucune coordonnée n'est tapée à la main — les
positions sur l'axe des temps sont dérivées des dates de l'extraction — et le
bloc `controles` du JSON est recalculé à chaque exécution.

Le motif de l'archétype — premier emploi, résidence Horizon (2026-08-14) : **le
dessin précède le gros œuvre.** Deux registres au-dessus d'un même axe des
temps. En haut, la pile des niveaux du bâtiment : chaque niveau reçoit sa
diffusion de réservations (une marque encrée) puis se fige (une bande calcaire
court de la marque au bout de l'axe — rien ne s'y perce plus). Les marques
montent la pile d'avance sur le gros œuvre : c'est l'escalier, et c'est lui qui
porte la thèse. En bas, la bande des plans d'exécution, reprise en versions
successives. La géométrie code l'ordre et la précédence, jamais la forme de
l'ouvrage : les niveaux sont des bandes topologiques d'égale hauteur.
"""

from datetime import date

from _tronc import (W, H, MARGE, UTILE, VW, VH, V_MARGE, AW, AH, A_MARGE,
                    mesurer, echapper, texte, rect, rect_bord, ligne,
                    polyligne, entete_style, racine_appui, controles_appui,
                    executer)


# ── Rythme vertical de la planche ────────────────────────────────────────────
Y_SURTITRE = 76
Y_TITRE = 112
Y_SOUSTITRE = 138
Y_FILET_TITRE = 160
Y_ENTETE_A = 190
Y_ROWS = 214
H_ROW = 36
ECART_ROW = 6
Y_ENTETE_B = 490
Y_VERSIONS = 504
Y_BANDE = 512
H_BANDE = 44
Y_DERNIERE = 582
Y_AXE = 600
Y_MOIS = 620
Y_PHRASE = 688
Y_CARTOUCHE = 714
H_CARTOUCHE = 30

# ── Partition horizontale : libellés de niveau → zone des temps ──────────────
X0 = 176                      # début de l'axe des temps
X1 = W - MARGE                # 1144
COTE_MARQUE = 7               # la marque de diffusion — carrée, rayon 0
PAD = 14


def _d(s):
    return date.fromisoformat(s)


def _echelle(axe, x0, x1):
    """x(date) sur l'axe des temps — la position est dérivée, jamais tapée."""
    debut, fin = _d(axe["debut"]), _d(axe["fin"])
    total = (fin - debut).days
    return lambda s: x0 + (_d(s) - debut).days / total * (x1 - x0)


def _premiers_mois(axe):
    """Les premiers du mois strictement intérieurs à l'axe (bornes exclues)."""
    debut, fin = _d(axe["debut"]), _d(axe["fin"])
    ms, (y, m) = [], (debut.year, debut.month)
    while True:
        m += 1
        if m > 12:
            m, y = 1, y + 1
        p = date(y, m, 1)
        if p >= fin:
            return ms
        ms.append(p)


def _marque(A, x, cy, cote=COTE_MARQUE):
    A(rect(x - cote / 2, cy - cote / 2, cote, cote, "encre"))


def _escalier_pts(marques):
    """L'escalier : des marches orthogonales de marque en marque, de bas en
    haut — la contremarche monte à l'aplomb de la diffusion précédente, le
    giron rejoint la suivante."""
    pts = [marques[0]]
    for (x0, y0), (x1, y1) in zip(marques, marques[1:]):
        pts.append((x0, y1))
        pts.append((x1, y1))
    return pts


def composer(donnees):
    ch = donnees["chronologie"]
    axe = ch["axe"]
    ech = _echelle(axe, X0, X1)
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
    entete_style(A, ("filet-1", "filet-2", "filet-3", "encre"))
    A(rect(0, 0, W, H, "papier"))

    # ── Bloc de titre ────────────────────────────────────────────────────────
    A(texte(MARGE, Y_SURTITRE, donnees["surtitre"], "mono", 11, 500,
            "pivot", tracking=11 * 0.14))
    A(texte(MARGE, Y_TITRE, donnees["titre"], "sans", 30, 700, "encre", wdth=112))
    A(texte(MARGE, Y_SOUSTITRE, donnees["sous_titre"], "sans", 16, 400,
            "pivot", wdth=100))
    A(rect(MARGE, Y_FILET_TITRE, UTILE, 1, "filet-1"))

    # ── En-tête du registre des réservations + double légende ────────────────
    # Deux signes, deux textes : la marque carrée (une diffusion) et l'aplat
    # calcaire (le niveau figé) — la couleur seule ne porte jamais (RGAA).
    l_fige = mesurer(ch["legende_fige"], 10, "mono", 10 * 0.14)
    x_sw2 = X1 - l_fige - 22
    A(rect_bord(x_sw2, Y_ENTETE_A - 8, 14, 8, "calcaire", "filet-1"))
    A(texte(X1, Y_ENTETE_A, ch["legende_fige"], "mono", 10, 500, "pivot",
            ancre="end", tracking=10 * 0.14))
    x_fin_diff = x_sw2 - 24
    l_diff = mesurer(ch["legende_diffusion"], 10, "mono", 10 * 0.14)
    A(rect(x_fin_diff - l_diff - 15, Y_ENTETE_A - 7.5, COTE_MARQUE,
           COTE_MARQUE, "encre"))
    A(texte(x_fin_diff, Y_ENTETE_A, ch["legende_diffusion"], "mono", 10, 500,
            "pivot", ancre="end", tracking=10 * 0.14))
    controler("en-tête réservations", ch["entete_reservations"], 10, "mono",
              x_fin_diff - l_diff - 15 - 24 - MARGE, 10 * 0.14)
    A(texte(MARGE, Y_ENTETE_A, ch["entete_reservations"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))

    # ── La grille des mois — sous les bandes, jamais au travers ──────────────
    mois_x = [ech(p.isoformat()) for p in _premiers_mois(axe)]
    for mx in mois_x:
        A(ligne(mx, Y_ROWS, mx, Y_AXE, "filet-3", 1.0))

    # ── La pile des niveaux : marque de diffusion, puis niveau figé ──────────
    niveaux = sorted(ch["niveaux"], key=lambda n: n["ordre"])
    n_rows = len(niveaux)
    bas_pile = Y_ROWS + n_rows * H_ROW + (n_rows - 1) * ECART_ROW
    marques = []
    for n in niveaux:
        i = n_rows - n["ordre"]                       # le RDC en bas de pile
        y = Y_ROWS + i * (H_ROW + ECART_ROW)
        cy = y + H_ROW / 2
        x_m = ech(n["date"])
        controler(f'libellé {n["cle"]}', n["libelle"], 15, "sans-600",
                  X0 - MARGE - 10)
        A(texte(MARGE, cy + 5, n["libelle"], "sans", 15, 600, "encre", wdth=112))
        A(ligne(X0, cy, x_m, cy, "filet-3", 1.0))
        A(rect_bord(x_m, y, X1 - x_m, H_ROW, "calcaire", "filet-2"))
        if n.get("mention"):
            if n.get("ancre") == "fin":
                controler(f'mention {n["cle"]}', n["mention"], 10, "mono",
                          X1 - 12 - (x_m + PAD), 10 * 0.14)
                A(texte(X1 - 12, cy + 3.5, n["mention"], "mono", 10, 500,
                        "pivot", ancre="end", tracking=10 * 0.14))
            else:
                controler(f'mention {n["cle"]}', n["mention"], 10, "mono",
                          X1 - 12 - (x_m + PAD), 10 * 0.14)
                A(texte(x_m + PAD, cy + 3.5, n["mention"], "mono", 10, 500,
                        "pivot", tracking=10 * 0.14))
        marques.append((x_m, cy))
    for x_m, cy in marques:
        _marque(A, x_m, cy)
    # L'escalier — il se trace après les bandes : c'est lui qu'on doit voir.
    A(polyligne(_escalier_pts(marques), "encre", 1.5))

    # ── Le registre des plans : une bande, trois versions ────────────────────
    controler("en-tête plans", ch["entete_plans"], 10, "mono",
              ech(ch["plans"]["versions"][0]["date"]) - 16 - MARGE, 10 * 0.14)
    A(texte(MARGE, Y_ENTETE_B, ch["entete_plans"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    p = ch["plans"]
    x_deb, x_fin = ech(p["debut"]), ech(p["fin"])
    A(rect_bord(x_deb, Y_BANDE, x_fin - x_deb, H_BANDE, "calcaire", "filet-1"))
    controler("libellé plans", p["libelle"], 15, "sans-600",
              x_fin - x_deb - 2 * PAD)
    A(texte(x_deb + PAD, Y_BANDE + 19, p["libelle"], "sans", 15, 600,
            "encre", wdth=112))
    controler("détail plans", p["detail"], 10, "mono",
              x_fin - x_deb - 2 * PAD, 10 * 0.14)
    A(texte(x_deb + PAD, Y_BANDE + 36, p["detail"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    for k, v in enumerate(p["versions"]):
        xv = ech(v["date"])
        # Deux étriers qui pincent la bande, jamais une ligne au travers :
        # elle couperait le libellé des plans (vu au contrôle à 1152 px).
        A(ligne(xv, Y_VERSIONS + 4, xv, Y_BANDE + 8, "encre", 1.5))
        A(ligne(xv, Y_BANDE + H_BANDE - 8, xv, Y_BANDE + H_BANDE + 6,
                "encre", 1.5))
        if k == len(p["versions"]) - 1:
            controler("version finale", v["libelle"], 10, "mono",
                      X1 - (mois_x[-1] + 10), 10 * 0.14)
            A(texte(X1, Y_VERSIONS, v["libelle"], "mono", 10, 500, "pivot",
                    ancre="end", tracking=10 * 0.14))
        else:
            A(texte(xv, Y_VERSIONS, v["libelle"], "mono", 10, 500, "pivot",
                    ancre="middle", tracking=10 * 0.14))

    # ── La dernière diffusion, puis l'axe des temps ──────────────────────────
    derniere = axe.get("derniere")
    if derniere:
        xd = ech(derniere["date"])
        A(ligne(xd, Y_DERNIERE + 6, xd, Y_AXE, "encre", 1.5))
        A(texte(X1, Y_DERNIERE, derniere["libelle"], "mono", 10, 500, "pivot",
                ancre="end", tracking=10 * 0.14))
    A(ligne(X0, Y_AXE, X1, Y_AXE, "encre", 1.5))
    bornes = [X0] + mois_x + [X1]
    for b in bornes:
        A(ligne(b, Y_AXE, b, Y_AXE + 6, "encre", 1.0))
    for (a, b), libelle in zip(zip(bornes, bornes[1:]), axe["mois"]):
        A(texte((a + b) / 2, Y_MOIS, libelle, "mono", 10, 500, "pivot",
                ancre="middle", tracking=10 * 0.14))

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

    montees = all(x1 > x0 and y1 < y0 for (x0, y0), (x1, y1)
                  in zip(marques, marques[1:]))
    controles = {
        "gabarit": f"{W} x {H} — rapport {W/H:.4f} (3:2 exact)",
        "demonstration": f"escalier de {len(marques)} marques "
                         f"{'strictement montantes' if montees else '⚠ NON MONOTONES'} "
                         f"(x {marques[0][0]:.0f} → {marques[-1][0]:.0f}), chaque "
                         f"niveau figé de sa marque au bout de l'axe, bande des "
                         f"plans {ech(p['debut']):.0f} → {ech(p['fin']):.0f} sous "
                         f"la pile — la géométrie porte la précédence, aucun "
                         f"chiffre de la fiche n'est répété",
        "topologie": f"libellés (x {MARGE}) → axe des temps (x {X0}–{X1}) ; "
                     f"pile de {n_rows} niveaux {Y_ROWS}–{bas_pile}, bande des "
                     f"plans {Y_BANDE}–{Y_BANDE + H_BANDE}, axe à y {Y_AXE}",
        "bas_du_dessin": f"axe à {Y_AXE}, mois à {Y_MOIS}, phrase de principe "
                         f"à {Y_PHRASE}, cartouche {Y_CARTOUCHE}–"
                         f"{Y_CARTOUCHE + H_CARTOUCHE}, marge basse "
                         f"{H - (Y_CARTOUCHE + H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur * H_CARTOUCHE} px², soit "
                            f"{largeur * H_CARTOUCHE / (W * H) * 100:.2f} % de "
                            f"la planche",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l'échelle "
                         f"0,96 (1152 / {W})",
        "depassements": depassements if depassements
                        else "aucun — toutes les lignes mesurées sous leur colonne",
    }
    return "\n".join(out) + "\n", controles


def composer_vignette(donnees):
    """La vignette : l'escalier seul — la pile des niveaux, les marques qui la
    gravissent, les bandes figées. Le registre des plans, les mentions et les
    mois sont laissés à la planche : deux étiquettes dans 300 px se lisent."""
    ch = donnees["chronologie"]
    axe = ch["axe"]
    x0, x1 = V_MARGE, VW - V_MARGE
    ech = _echelle(axe, x0, x1)
    niveaux = sorted(ch["niveaux"], key=lambda n: n["ordre"])
    n_rows = len(niveaux)
    y0, h_row, ecart = 40, 19, 3
    bas = y0 + n_rows * h_row + (n_rows - 1) * ecart   # 169

    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false" '
      f'style="width:100%;height:auto;display:block">')
    entete_style(A, ("filet-1", "filet-2", "filet-3", "encre"))
    A(rect(0, 0, VW, VH, "papier"))
    A(texte(V_MARGE, 22, donnees["vignette_surtitre"], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    for p in _premiers_mois(axe):
        mx = ech(p.isoformat())
        A(ligne(mx, y0, mx, bas + 3, "filet-3", 1.0))

    marques = []
    for n in niveaux:
        i = n_rows - n["ordre"]
        y = y0 + i * (h_row + ecart)
        cy = y + h_row / 2
        x_m = ech(n["date"])
        A(ligne(x0, cy, x_m, cy, "filet-3", 1.0))
        A(rect_bord(x_m, y, x1 - x_m, h_row, "calcaire", "filet-2"))
        marques.append((x_m, cy))
    for x_m, cy in marques:
        A(rect(x_m - 2.5, cy - 2.5, 5, 5, "encre"))
    A(polyligne(_escalier_pts(marques), "encre", 1.2))

    # Deux étiquettes : le pied et la tête de l'escalier.
    bas_n, haut_n = niveaux[0], niveaux[-1]
    x_b, cy_b = marques[0]
    A(texte(x_b + 8, cy_b + 4, bas_n["libelle"], "sans", 12, 600,
            "encre", wdth=112))
    # L'avance 0,48 est calibrée en casse mixte : un libellé tout en capitales
    # (« RDC ») rend plus large — majoration mesurée au contrôle à 296 px.
    l_b = mesurer(bas_n["libelle"], 12, "sans-600") * 1.3
    A(texte(x_b + 8 + l_b + 12, cy_b + 4, "16 JANV", "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    x_h, cy_h = marques[-1]
    A(texte(x_h + 8, cy_h + 4, haut_n["libelle"], "sans", 12, 600,
            "encre", wdth=112))

    A(ligne(x0, bas + 3, x1, bas + 3, "filet-1", 1.0))

    A("</svg>")
    controles = {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": f"carte de projet mesurée de 274 à 296 px — "
                            f"échelle {274/VW:.2f} à {296/VW:.2f}",
        "corps_minimal": f"9 px dans le repère — rendu à {9*274/VW:.1f} px au pire cas",
        "motif": f"l'escalier seul : {n_rows} niveaux, marques montantes de "
                 f"x {marques[0][0]:.0f} à {marques[-1][0]:.0f}, deux étiquettes "
                 f"(pied et tête) — plans, mentions et mois laissés à la planche",
        "bas_du_dessin": f"{bas + 3:.0f} px, marge basse {VH - bas - 3:.0f} px",
    }
    return "\n".join(out) + "\n", controles


def composer_appui(donnees):
    """L'appui du hero : le motif entier à l'échelle 1 — la pile, l'escalier,
    la bande des plans et l'axe des mois. Densité intermédiaire : trois nœuds
    datés (16 JANV, DÉBUT MARS, la version finale), la double légende — sans
    phrase de principe ni cartouche, le hero porte déjà sa légende de carte."""
    ch = donnees["chronologie"]
    axe = ch["axe"]
    x_lbl, x0, x1 = A_MARGE, 84, AW - A_MARGE
    ech = _echelle(axe, x0, x1)
    niveaux = sorted(ch["niveaux"], key=lambda n: n["ordre"])
    n_rows = len(niveaux)
    y0, h_row, ecart = 68, 24, 4
    bas_pile = y0 + n_rows * h_row + (n_rows - 1) * ecart   # 232
    y_bande, h_bande = 252, 32
    y_versions = 304
    y_axe = 318
    y_mois = 334

    out = []
    A = out.append
    racine_appui(A, donnees, strokes=("filet-1", "filet-2", "filet-3", "encre"))

    # La double légende, en tête à droite — le signe toujours doublé du texte.
    # Formes courtes : les légendes de la planche percutaient le surtitre
    # dans les 504 px utiles de l'appui (vu au contrôle à 552 px).
    leg_fige = ch.get("legende_fige_court", ch["legende_fige"])
    leg_diff = ch.get("legende_diffusion_court", ch["legende_diffusion"])
    l_fige = mesurer(leg_fige, 10, "mono", 10 * 0.14)
    x_sw2 = x1 - l_fige - 20
    A(rect_bord(x_sw2, 27, 14, 8, "calcaire", "filet-1"))
    A(texte(x1, 34, leg_fige, "mono", 10, 500, "pivot",
            ancre="end", tracking=10 * 0.14))
    x_fin_diff = x_sw2 - 20
    l_diff = mesurer(leg_diff, 10, "mono", 10 * 0.14)
    A(rect(x_fin_diff - l_diff - 13, 27.5, 6, 6, "encre"))
    A(texte(x_fin_diff, 34, leg_diff, "mono", 10, 500, "pivot",
            ancre="end", tracking=10 * 0.14))

    for p in _premiers_mois(axe):
        mx = ech(p.isoformat())
        A(ligne(mx, y0, mx, y_axe, "filet-3", 1.0))

    marques = []
    for n in niveaux:
        i = n_rows - n["ordre"]
        y = y0 + i * (h_row + ecart)
        cy = y + h_row / 2
        x_m = ech(n["date"])
        A(texte(x_lbl, cy + 4, n["libelle"], "sans", 13, 600, "encre", wdth=112))
        A(ligne(x0, cy, x_m, cy, "filet-3", 1.0))
        A(rect_bord(x_m, y, x1 - x_m, h_row, "calcaire", "filet-2"))
        if n["ordre"] == 1:
            A(texte(x_m + 10, cy + 3.5, "16 JANV", "mono", 10, 500, "pivot",
                    tracking=10 * 0.14))
        if n["ordre"] == n_rows:
            A(texte(x_m + 10, cy + 3.5, "DÉBUT MARS", "mono", 10, 500, "pivot",
                    tracking=10 * 0.14))
        marques.append((x_m, cy))
    for x_m, cy in marques:
        A(rect(x_m - 3, cy - 3, 6, 6, "encre"))
    A(polyligne(_escalier_pts(marques), "encre", 1.5))

    p = ch["plans"]
    x_deb, x_fin = ech(p["debut"]), ech(p["fin"])
    A(rect_bord(x_deb, y_bande, x_fin - x_deb, h_bande, "calcaire", "filet-1"))
    A(texte(x_deb + 12, y_bande + 20, "Plans d'exécution", "sans", 13, 600,
            "encre", wdth=112))
    for k, v in enumerate(p["versions"]):
        xv = ech(v["date"])
        A(ligne(xv, y_bande - 6, xv, y_bande + h_bande + 6, "encre", 1.5))
        if k == len(p["versions"]) - 1:
            A(texte(x1, y_versions, "V3 · 20 AVR", "mono", 10, 500, "pivot",
                    ancre="end", tracking=10 * 0.14))
        else:
            A(texte(xv, y_versions, v["libelle"].split(" · ")[0], "mono", 10,
                    500, "pivot", ancre="middle", tracking=10 * 0.14))

    A(ligne(x0, y_axe, x1, y_axe, "encre", 1.5))
    bornes = [x0] + [ech(pm.isoformat()) for pm in _premiers_mois(axe)] + [x1]
    for b in bornes:
        A(ligne(b, y_axe, b, y_axe + 5, "encre", 1.0))
    for (a, b), libelle in zip(zip(bornes, bornes[1:]), axe["mois"]):
        A(texte((a + b) / 2, y_mois, libelle, "mono", 10, 500, "pivot",
                ancre="middle", tracking=10 * 0.14))

    A("</svg>")
    return "\n".join(out) + "\n", controles_appui(
        motif=f"le motif entier : pile de {n_rows} niveaux, escalier de "
              f"marques montantes, bandes figées, bande des plans à trois "
              f"versions, axe des mois — trois nœuds datés (16 JANV, DÉBUT "
              f"MARS, V3 · 20 AVR), double légende en tête ; phrase et "
              f"cartouche laissés à la planche",
        bas=f"axe à {y_axe} px, mois à {y_mois} px, marge basse {AH - y_mois} px")


if __name__ == "__main__":
    executer(composer, composer_vignette, composer_appui)
