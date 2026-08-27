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

Deux mécanismes à ce jour, dispatchés sur le bloc de l'extraction.

`precedence` — premier emploi, résidence Horizon (2026-08-14) : **le dessin
précède le gros œuvre.** Deux registres au-dessus d'un même axe des temps. En
haut, la pile des niveaux du bâtiment : chaque niveau reçoit sa diffusion de
réservations (une marque encrée) puis se fige (une bande calcaire court de la
marque au bout de l'axe — rien ne s'y perce plus). Les marques montent la pile
d'avance sur le gros œuvre : c'est l'escalier, et c'est lui qui porte la thèse.
En bas, la bande des plans d'exécution, reprise en versions successives. La
géométrie code l'ordre et la précédence, jamais la forme de l'ouvrage : les
niveaux sont des bandes topologiques d'égale hauteur.

`divergence` — second emploi, maisons Tourtet (2026-08-15) : **l'enveloppe fixe
la limite, les systèmes font la marge.** Un axe des temps, une ordonnée d'écart
au seuil du label, et deux tracés en marches d'escalier posés dessus.
L'un ne bouge pas d'un calcul à l'autre et frôle le seuil du label ; l'autre
décroche marche après marche et s'en éloigne. Deux cotes verticales relèvent
l'écart de chacun au seuil : elles sont dans le rapport exact que la fiche
énonce, et c'est ce rapport qui porte la démonstration — le texte masqué, il
reste une ligne collée à un seuil et une ligne qui s'en va. L'ordonnée est
CALCULÉE depuis les valeurs et leur maximum réglementaire ; aucun pourcentage
n'est tapé.
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
                         f"niveau figé de sa marque au bout de l’axe, bande des "
                         f"plans {ech(p['debut']):.0f} → {ech(p['fin']):.0f} sous "
                         f"la pile — la géométrie porte la précédence, aucun "
                         f"chiffre de la fiche n’est répété",
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
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l’échelle "
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
        "motif": f"l’escalier seul : {n_rows} niveaux, marques montantes de "
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
    A(texte(x_deb + 12, y_bande + 20, "Plans d’exécution", "sans", 13, 600,
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


# ═════════════════════════════════════════════════════════════════════════════
# Mécanisme `divergence` — deux grandeurs contre un seuil, sur un axe des temps
# ═════════════════════════════════════════════════════════════════════════════
#
# La géométrie ne code pas le temps seul : elle code un ÉCART. L'ordonnée est
# l'écart AU SEUIL DU LABEL, en points de pourcentage, dérivé de
# (maximum − valeur) / maximum moins l'écart du seuil — jamais tapé. Les deux
# tracés partagent donc une ordonnée alors qu'ils n'ont pas la même unité :
# c'est exactement la lecture que la fiche fait quand elle les compare tous deux
# au seuil du label, et c'est le seul repère où sa phrase se dessine.
# L'arbitrage est consigné dans `a_valider_ft2e`, comme il se doit.
#
# L'origine est le SEUIL, non l'exigence : une ordonnée partant de l'exigence
# donnait au vide réglementaire (les vingt points qu'aucun des deux tracés
# n'occupe) 44 % de la hauteur du cadre, et écrasait la cote de 1,58 point à
# onze pixels — illisible au contrôle à 1152. Ce n'est pas un axe tronqué : le
# seuil est nommé, coté, et la zone qui le surplombe est dessinée en bande.

# ── Rythme vertical ─────────────────────────────────────────────────────────
D_Y_ENTETE = 184
D_Y_BANDE = 202               # bande « au-dessus du seuil » — le côté interdit
D_H_BANDE = 28                # un module : une marge de limite, pas une zone
D_Y_ZERO = 230                # le seuil du label — l'origine de l'ordonnée
D_Y_MAX = 528                 # le bas du cadre, à `echelle.max` points d'écart
D_Y_ARRET = 542               # bande de l'arrêt d'opération
D_H_ARRET = 16
D_Y_DATES = 572               # dates des calculs, juste au-dessus de l'axe
D_Y_AXE = 578
D_Y_ANNEES = 598
D_Y_MENTION = 630

# ── Partition horizontale ───────────────────────────────────────────────────
D_X0 = 240                    # début de l'axe des temps ; à sa gauche, les pistes
D_X1 = W - MARGE              # 1144
D_COTE = (D_X1 - 28, D_X1 - 10)   # abscisses des deux cotes verticales
D_COTE_TICK = 5
D_MARQUE = 7                  # la marque d'un calcul — carrée, rayon 0
D_LABEL_X = D_X1 - 40         # les libellés de cote se rangent avant les cotes


def _annees_bornes(axe):
    """Les 1ᵉʳ janvier strictement intérieurs à l'axe — les bornes de l'échelle
    des millésimes. Calculées, jamais énumérées."""
    debut, fin = _d(axe["debut"]), _d(axe["fin"])
    bornes, an = [], debut.year + 1
    while date(an, 1, 1) < fin:
        if date(an, 1, 1) > debut:
            bornes.append(date(an, 1, 1))
        an += 1
    return bornes


def _ecart(piste, valeur, seuil=0.0):
    """L'écart au seuil, en points de pourcentage. C'est l'ordonnée — calculée
    depuis la valeur et son maximum réglementaire, jamais tapée."""
    return (piste["maximum"] - valeur) / piste["maximum"] * 100.0 - seuil


def _marches(pts):
    """Le tracé en marches : la valeur tenue jusqu'au calcul suivant, puis la
    contremarche. C'est la lecture honnête d'une grandeur qui n'existe qu'aux
    dates où elle a été calculée."""
    trace = [pts[0]]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        trace.append((x1, y0))
        trace.append((x1, y1))
    return trace


def _cadre(dv, y_zero, y_max):
    """L'ordonnée : y(écart) et y(seuil), depuis l'échelle de l'extraction."""
    haut, bas = dv["echelle"]["min"], dv["echelle"]["max"]
    k = (y_max - y_zero) / (bas - haut)
    return (lambda e: y_zero + (e - haut) * k), k


def composer_divergence(donnees):
    dv = donnees["divergence"]
    axe = dv["axe"]
    seuil = dv["seuil"]["ecart"]
    ech = _echelle(axe, D_X0, D_X1)
    y_de, k = _cadre(dv, D_Y_ZERO, D_Y_MAX)
    y_seuil = D_Y_ZERO
    pistes = sorted(dv["pistes"], key=lambda p: p["ordre"])
    out = []
    A = out.append
    depassements = []

    def controler(nom, chaine, corps, profil, dispo, tracking=0.0):
        largeur = mesurer(chaine, corps, profil, tracking)
        if largeur > dispo:
            depassements.append(f"{nom} : {largeur:.0f} px pour {dispo:.0f} px")
        return largeur

    def mono(x, y, chaine, couleur="pivot", corps=10, ancre=None):
        return texte(x, y, chaine, "mono", corps, 500, couleur,
                     ancre=ancre, tracking=corps * 0.14)

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

    # ── En-tête du registre, et la légende de la marque ──────────────────────
    l_leg = mesurer(dv["legende_calcul"], 10, "mono", 1.4)
    A(rect(D_X1 - l_leg - 15, D_Y_ENTETE - 7.5, D_MARQUE, D_MARQUE, "encre"))
    A(mono(D_X1, D_Y_ENTETE, dv["legende_calcul"], ancre="end"))
    controler("en-tête", dv["entete"], 10, "mono",
              D_X1 - l_leg - 15 - 24 - MARGE, 1.4)
    A(mono(MARGE, D_Y_ENTETE, dv["entete"]))

    # ── Le cadre : la bande du côté interdit, puis la ligne de seuil ─────────
    # La bande ne représente pas une zone bornée mais un demi-plan : au-dessus
    # du seuil, le projet reste réglementaire et cesse d'être labellisable.
    # C'est la marge d'une ligne de limite — 28 px, un module —, pas une surface
    # à l'échelle ; elle donne au seuil son sens de plancher.
    A(rect(D_X0, D_Y_BANDE, D_X1 - D_X0, D_H_BANDE, "calcaire"))
    controler("libellé de bande", dv["bande_sans_label"], 10, "mono", 420, 1.4)
    A(mono(D_X0 + 12, D_Y_BANDE + 18, dv["bande_sans_label"]))
    # Le libellé s'arrête AVANT les cotes : aligné sur D_X1, sa queue surplombait
    # à dix pixels près l'étrier de la petite cote (vu au contrôle à 1152 px).
    controler("libellé de seuil", dv["seuil"]["libelle"], 10, "mono", 420, 1.4)
    A(mono(D_LABEL_X, D_Y_BANDE + 18, dv["seuil"]["libelle"], ancre="end"))

    # Les verticales des calculs, sous tout le reste : elles relient chaque
    # marque à sa date, et rien d'autre ne quadrille le cadre.
    dates = [p["date"] for p in pistes[0]["points"]]
    for d in dates:
        A(ligne(ech(d), y_seuil, ech(d), D_Y_AXE, "filet-3", 1.0))

    A(ligne(D_X0, y_seuil, D_X1, y_seuil, "encre", 1.5))

    # ── La bande de l'arrêt d'opération, sous le cadre ───────────────────────
    ar = dv["arret"]
    xa0, xa1 = ech(ar["debut"]), ech(ar["fin"])
    A(rect_bord(xa0, D_Y_ARRET, xa1 - xa0, D_H_ARRET, "calcaire", "filet-1"))
    controler("libellé d’arrêt", ar["libelle"], 10, "mono",
              xa1 - xa0 - 24, 1.4)
    A(mono((xa0 + xa1) / 2, D_Y_ARRET + 11, ar["libelle"], ancre="middle"))

    # ── Les libellés de piste, à gauche du cadre ─────────────────────────────
    # Chaque tracé dit ce qu'il mesure : c'est ce qui interdit de lire la
    # géométrie à l'envers, et ce qui double le signe graphique d'un texte.
    traces = {}
    for p in pistes:
        pts = [(ech(q["date"]), y_de(_ecart(p, q["valeur"], seuil)))
               for q in p["points"]]
        traces[p["cle"]] = pts
        y_ancre = pts[0][1]
        lignes = p["libelle_lignes"]
        y_lib = y_ancre - (len(lignes) - 1) * 17 / 2 + 5
        for i, l in enumerate(lignes):
            controler(f'libellé {p["cle"]} l{i}', l, 15, "sans-600",
                      D_X0 - MARGE - 12)
            A(texte(MARGE, y_lib + i * 17, l, "sans", 15, 600, "encre", wdth=112))
        controler(f'détail {p["cle"]}', p["detail"], 10, "mono",
                  D_X0 - MARGE - 12, 1.4)
        A(mono(MARGE, y_lib + len(lignes) * 17 + 2, p["detail"]))

    # ── Les deux tracés, en marches, puis leurs marques ──────────────────────
    for p in pistes:
        A(polyligne(_marches(traces[p["cle"]]), "encre", 1.5))
    for p in pistes:
        for x, y in traces[p["cle"]]:
            A(rect(x - D_MARQUE / 2, y - D_MARQUE / 2, D_MARQUE, D_MARQUE,
                   "encre"))

    # ── Les notes, accrochées à ce qu'elles expliquent ───────────────────────
    bbio, cep = pistes[0], pistes[1]
    x_dep = traces[bbio["cle"]][0][0] + 12
    y_bbio = traces[bbio["cle"]][0][1]
    for i, note in enumerate(bbio["notes"]):
        controler(f"note bbio {i}", note, 10, "mono", D_LABEL_X - x_dep, 1.4)
        A(mono(x_dep, y_bbio + 16 + i * 16, note))

    x_cep0, y_cep0 = traces[cep["cle"]][0]
    controler("note cep départ", cep["note_depart"], 10, "mono",
              D_X1 - (x_cep0 + 12), 1.4)
    A(mono(x_cep0 + 12, y_cep0 - 10, cep["note_depart"]))

    x_fin, y_fin = traces[cep["cle"]][-1]
    y_marche = traces[cep["cle"]][-2][1]
    controler("note cep marche", cep["note_marche"], 10, "mono",
              (x_fin - 10) - (x_cep0 + 12), 1.4)
    A(mono(x_fin - 10, y_marche + 18, cep["note_marche"], ancre="end"))
    A(mono(x_fin - 10, y_fin + 18, cep["note_arrivee"], ancre="end"))

    # ── Les deux cotes — le cœur de la démonstration ─────────────────────────
    # Elles se mesurent du seuil au tracé, à l'arrivée. Leur rapport est celui
    # que la fiche énonce ; il est RECALCULÉ ici et reporté aux contrôles.
    cotes_mesurees = []
    for i, c in enumerate(dv["cotes"]):
        p = next(q for q in pistes if q["cle"] == c["piste"])
        x_c = D_COTE[i]
        y_t = traces[p["cle"]][-1][1]
        e = _ecart(p, p["points"][-1]["valeur"], seuil)
        cotes_mesurees.append((c["piste"], e, abs(y_t - y_seuil)))
        A(ligne(traces[p["cle"]][-1][0], y_t, x_c + D_COTE_TICK, y_t,
                "filet-3", 1.0))
        A(ligne(x_c, y_seuil, x_c, y_t, "encre", 1.0))
        A(ligne(x_c - D_COTE_TICK, y_seuil, x_c + D_COTE_TICK, y_seuil,
                "encre", 1.0))
        A(ligne(x_c - D_COTE_TICK, y_t, x_c + D_COTE_TICK, y_t, "encre", 1.0))
        y_lab = y_t + 16 if i == 0 else (y_seuil + y_t) / 2 + 4
        controler(f'cote {c["piste"]}', c["libelle"], 10, "mono", 320, 1.4)
        A(mono(D_LABEL_X, y_lab, c["libelle"], ancre="end"))

    # ── L'axe des temps et ses millésimes ────────────────────────────────────
    for p in pistes[:1]:
        for q in p["points"]:
            A(mono(ech(q["date"]), D_Y_DATES, q["date_libelle"], ancre="middle"))
    A(ligne(D_X0, D_Y_AXE, D_X1, D_Y_AXE, "encre", 1.5))
    bornes = [D_X0] + [ech(b.isoformat()) for b in _annees_bornes(axe)] + [D_X1]
    for b in bornes:
        A(ligne(b, D_Y_AXE, b, D_Y_AXE + 6, "encre", 1.0))
    for (a, b), an in zip(zip(bornes, bornes[1:]), axe["annees"]):
        A(mono((a + b) / 2, D_Y_ANNEES, an, ancre="middle"))

    controler("mention de bas", dv["mention_bas"], 10, "mono", UTILE, 1.4)
    A(mono(MARGE, D_Y_MENTION, dv["mention_bas"]))

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

    plate = len({round(y, 3) for _, y in traces[bbio["cle"]]}) == 1
    ecarts = [y for _, y in traces[cep["cle"]]]
    descend = all(b > a for a, b in zip(ecarts, ecarts[1:]))
    rapport = cotes_mesurees[1][2] / cotes_mesurees[0][2]
    controles = {
        "gabarit": f"{W} x {H} — rapport {W/H:.4f} (3:2 exact)",
        "demonstration":
            f"deux tracés de {len(dates)} calculs sur un même écart au seuil : "
            f"{bbio['cle']} {'PLAT' if plate else '⚠ NON PLAT'} à "
            f"{_ecart(bbio, bbio['points'][0]['valeur'], seuil):.2f} point sous "
            f"le seuil, {cep['cle']} "
            f"{'DESCENDANT' if descend else '⚠ NON MONOTONE'} de "
            f"{_ecart(cep, cep['points'][0]['valeur'], seuil):.2f} à "
            f"{_ecart(cep, cep['points'][-1]['valeur'], seuil):.2f} points ; "
            f"dernière marche {abs(ecarts[-1] - ecarts[-2]):.1f} px contre "
            f"{abs(ecarts[1] - ecarts[0]):.1f} et {abs(ecarts[2] - ecarts[1]):.1f} "
            f"pour les deux premières — la géométrie porte la thèse, aucun "
            f"chiffre de la fiche n’est répété hors des nœuds du mécanisme",
        "cotes":
            f"cote {cotes_mesurees[0][0]} = {cotes_mesurees[0][1]:.3f} points "
            f"({cotes_mesurees[0][2]:.2f} px, citée {dv['cotes'][0]['valeur_citee']}) ; "
            f"cote {cotes_mesurees[1][0]} = {cotes_mesurees[1][1]:.3f} points "
            f"({cotes_mesurees[1][2]:.2f} px, citée {dv['cotes'][1]['valeur_citee']}) ; "
            f"rapport dessiné {rapport:.2f} contre "
            f"{dv['cotes'][1]['valeur_citee'] / dv['cotes'][0]['valeur_citee']:.2f} cité",
        "ordonnee": f"origine = le seuil du label (RT2012 moins "
                    f"{dv['seuil']['ecart']:.0f} points), à y {y_seuil} ; écart 0 à "
                    f"{dv['echelle']['max']:.0f} points sur {D_Y_MAX - D_Y_ZERO} px, "
                    f"soit {k:.3f} px par point — toute ordonnée dérivée de "
                    f"(maximum − valeur) / maximum, jamais tapée ; bande du côté "
                    f"interdit {D_Y_BANDE}–{D_Y_BANDE + D_H_BANDE} (un module, "
                    f"marge de limite et non surface à l’échelle)",
        "topologie": f"pistes (x {MARGE}–{D_X0 - 12}) → axe des temps "
                     f"(x {D_X0}–{D_X1}), {axe['debut']} → {axe['fin']} ; "
                     f"calculs à x " + ", ".join(f"{ech(d):.0f}" for d in dates)
                     + f" ; cotes à x {D_COTE[0]} et {D_COTE[1]}",
        "bas_du_dessin": f"cadre jusqu’à {D_Y_MAX}, bande d’arrêt {D_Y_ARRET}–"
                         f"{D_Y_ARRET + D_H_ARRET}, axe à {D_Y_AXE}, millésimes "
                         f"à {D_Y_ANNEES}, mention à {D_Y_MENTION}, phrase à "
                         f"{Y_PHRASE}, cartouche {Y_CARTOUCHE}–"
                         f"{Y_CARTOUCHE + H_CARTOUCHE}, marge basse "
                         f"{H - (Y_CARTOUCHE + H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur * H_CARTOUCHE} px², soit "
                            f"{largeur * H_CARTOUCHE / (W * H) * 100:.2f} % de "
                            f"la planche (la bande « sans label » est en calcaire, "
                            f"surface secondaire, elle ne compte pas comme réserve)",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l’échelle "
                         f"0,96 (1152 / {W})",
        "depassements": depassements if depassements
                        else "aucun — toutes les lignes mesurées sous leur colonne",
    }
    return "\n".join(out) + "\n", controles


def composer_vignette_divergence(donnees):
    """La vignette : le cadre et les deux tracés, rien d'autre. Les cotes y
    tomberaient à 4 px pour la petite — invisibles ; l'axe des temps, les dates
    et les notes sont laissés à la planche. Ce qui reste est ce qui se lit à
    296 px : une ligne plate contre le seuil, une ligne qui décroche."""
    dv = donnees["divergence"]
    axe = dv["axe"]
    seuil = dv["seuil"]["ecart"]
    x0, x1 = V_MARGE, VW - V_MARGE - 4
    ech = _echelle(axe, x0, x1)
    y_seuil, y_max = 52, 158
    y_de, _ = _cadre(dv, y_seuil, y_max)
    y_bande, h_bande = 32, 20
    pistes = sorted(dv["pistes"], key=lambda p: p["ordre"])
    bas = 176

    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false" '
      f'style="width:100%;height:auto;display:block">')
    entete_style(A, ("filet-1", "filet-2", "filet-3", "encre"))
    A(rect(0, 0, VW, VH, "papier"))
    A(texte(V_MARGE, 22, donnees["vignette_surtitre"], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    # La bande porte son nom même ici : un aplat calcaire muet ne serait qu'une
    # couleur, et la couleur seule ne porte jamais (RGAA, protocole règle 2).
    A(rect(x0, y_bande, x1 - x0, h_bande, "calcaire"))
    A(texte(x1, y_bande + 14, dv["seuil"]["libelle_court"], "mono", 9, 500,
            "pivot", ancre="end", tracking=9 * 0.14))
    A(ligne(x0, y_seuil, x1, y_seuil, "encre", 1.5))

    traces = {}
    for p in pistes:
        pts = [(ech(q["date"]), y_de(_ecart(p, q["valeur"], seuil)))
               for q in p["points"]]
        traces[p["cle"]] = pts
        A(polyligne(_marches(pts), "encre", 1.2))
    for p in pistes:
        for x, y in traces[p["cle"]]:
            A(rect(x - 2, y - 2, 4, 4, "encre"))

    # Deux étiquettes de piste et deux valeurs : le plancher de ce qui reste
    # lisible dans 300 px, et le strict nécessaire pour que la géométrie ne
    # se lise pas à l'envers.
    bbio, cep = pistes[0], pistes[1]
    xb, yb = traces[bbio["cle"]][0]
    A(texte(xb + 8, yb + 15, bbio["libelle_court"], "sans", 12, 600,
            "encre", wdth=112))
    lb = mesurer(bbio["libelle_court"], 12, "sans-600") * 1.3
    A(texte(xb + 8 + lb + 10, yb + 15, bbio["points"][0]["affichee"], "mono",
            10, 500, "pivot", tracking=1.4))
    xc, yc = traces[cep["cle"]][0]
    A(texte(xc + 8, yc - 8, cep["libelle_court"], "sans", 12, 600,
            "encre", wdth=112))
    lc = mesurer(cep["libelle_court"], 12, "sans-600") * 1.3
    A(texte(xc + 8 + lc + 10, yc - 8, cep["points"][0]["affichee"], "mono",
            10, 500, "pivot", tracking=1.4))
    xf, yf = traces[cep["cle"]][-1]
    A(texte(xf, yf + 15, cep["points"][-1]["affichee"], "mono", 10, 500,
            "pivot", ancre="middle", tracking=1.4))

    A(ligne(x0, bas, x1, bas, "filet-1", 1.0))
    A("</svg>")

    ecart_bbio = abs(traces[bbio["cle"]][0][1] - y_seuil)
    ecart_cep = abs(traces[cep["cle"]][-1][1] - y_seuil)
    controles = {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": f"carte de projet mesurée de 274 à 296 px — "
                            f"échelle {274/VW:.2f} à {296/VW:.2f}",
        "corps_minimal": f"9 px dans le repère — rendu à {9*274/VW:.1f} px au pire cas",
        "motif": f"le cadre et les deux tracés seuls : ligne plate à "
                 f"{ecart_bbio:.1f} px sous le seuil contre {ecart_cep:.1f} px à "
                 f"l’arrivée de la seconde, deux étiquettes et trois valeurs — "
                 f"cotes, axe des temps, dates et notes laissés à la planche",
        "bas_du_dessin": f"{bas} px, marge basse {VH - bas} px",
    }
    return "\n".join(out) + "\n", controles


def composer_appui_divergence(donnees):
    """L'appui du hero : le motif entier à l'échelle 1 — le cadre, la bande sans
    label, les deux tracés, les deux cotes et l'axe des millésimes. Trois nœuds
    chiffrés et deux libellés de piste sur deux lignes ; sans phrase de principe
    ni cartouche, le hero portant déjà sa légende de carte."""
    dv = donnees["divergence"]
    axe = dv["axe"]
    x_lbl, x0, x1 = A_MARGE, 150, AW - A_MARGE - 32
    ech = _echelle(axe, x0, x1)
    seuil = dv["seuil"]["ecart"]
    y_seuil, y_max = 96, 276
    y_de, _ = _cadre(dv, y_seuil, y_max)
    y_bande, h_bande = 72, 24
    pistes = sorted(dv["pistes"], key=lambda p: p["ordre"])
    cotes_x = (x1 + 12, x1 + 28)
    y_arret, h_arret = 284, 14
    y_axe, y_annees = 304, 322

    out = []
    A = out.append
    racine_appui(A, donnees, strokes=("filet-1", "filet-2", "filet-3", "encre"))

    def mono(x, y, chaine, corps=10, ancre=None):
        return texte(x, y, chaine, "mono", corps, 500, "pivot",
                     ancre=ancre, tracking=corps * 0.14)

    A(rect(x0, y_bande, x1 - x0, h_bande, "calcaire"))
    # Le libellé de bande est laissé à la planche : dans les 346 px utiles de
    # l'appui, il percute celui du seuil (vu au contrôle à 552 px).
    A(mono(x1, y_bande + 16, dv["seuil"]["libelle"], ancre="end"))
    for q in pistes[0]["points"]:
        A(ligne(ech(q["date"]), y_seuil, ech(q["date"]), y_axe, "filet-3", 1.0))
    A(ligne(x0, y_seuil, x1, y_seuil, "encre", 1.5))

    ar = dv["arret"]
    xa0, xa1 = ech(ar["debut"]), ech(ar["fin"])
    A(rect_bord(xa0, y_arret, xa1 - xa0, h_arret, "calcaire", "filet-1"))
    A(mono((xa0 + xa1) / 2, y_arret + 10, ar["libelle_court"], ancre="middle"))

    traces = {}
    for p in pistes:
        pts = [(ech(q["date"]), y_de(_ecart(p, q["valeur"], seuil)))
               for q in p["points"]]
        traces[p["cle"]] = pts
        lignes = p["libelle_lignes"]
        y_lib = pts[0][1] - (len(lignes) - 1) * 15 / 2 + 4
        for i, l in enumerate(lignes):
            A(texte(x_lbl, y_lib + i * 15, l, "sans", 13, 600, "encre", wdth=112))
        A(mono(x_lbl, y_lib + len(lignes) * 15 + 1, p["detail"]))
    for p in pistes:
        A(polyligne(_marches(traces[p["cle"]]), "encre", 1.5))
    for p in pistes:
        for x, y in traces[p["cle"]]:
            A(rect(x - 3, y - 3, 6, 6, "encre"))

    bbio, cep = pistes[0], pistes[1]
    xb, yb = traces[bbio["cle"]][0]
    A(mono(xb + 9, yb + 14, bbio["points"][0]["affichee"]))
    xc, yc = traces[cep["cle"]][0]
    A(mono(xc + 9, yc - 9, cep["points"][0]["affichee"]))
    xf, yf = traces[cep["cle"]][-1]
    A(mono(xf - 9, yf + 15, cep["points"][-1]["affichee"], ancre="end"))

    for i, c in enumerate(dv["cotes"]):
        p = next(q for q in pistes if q["cle"] == c["piste"])
        x_c = cotes_x[i]
        y_t = traces[p["cle"]][-1][1]
        A(ligne(traces[p["cle"]][-1][0], y_t, x_c + 4, y_t, "filet-3", 1.0))
        A(ligne(x_c, y_seuil, x_c, y_t, "encre", 1.0))
        A(ligne(x_c - 4, y_seuil, x_c + 4, y_seuil, "encre", 1.0))
        A(ligne(x_c - 4, y_t, x_c + 4, y_t, "encre", 1.0))
        y_lab = y_t + 14 if i == 0 else (y_seuil + y_t) / 2 + 4
        A(mono(x1, y_lab, c["libelle_court"], ancre="end"))

    A(ligne(x0, y_axe, x1, y_axe, "encre", 1.5))
    bornes = [x0] + [ech(b.isoformat()) for b in _annees_bornes(axe)] + [x1]
    for b in bornes:
        A(ligne(b, y_axe, b, y_axe + 5, "encre", 1.0))
    for (a, b), an in zip(zip(bornes, bornes[1:]), axe["annees"]):
        A(mono((a + b) / 2, y_annees, an, ancre="middle"))

    A("</svg>")
    return "\n".join(out) + "\n", controles_appui(
        motif=f"le motif entier : le cadre, la bande sans label, les deux "
              f"tracés de {len(pistes[0]['points'])} calculs en marches, les "
              f"deux cotes au seuil ({abs(traces['bbio'][-1][1] - y_seuil):.1f} px "
              f"contre {abs(traces['cep'][-1][1] - y_seuil):.1f} px), la bande "
              f"d’arrêt et l’axe des millésimes — trois nœuds chiffrés ; dates "
              f"des calculs, notes, phrase et cartouche laissés à la planche",
        bas=f"bande d’arrêt {y_arret}–{y_arret + h_arret}, axe à {y_axe}, "
            f"millésimes à {y_annees}, marge basse {AH - y_annees} px")


def _composer(donnees):
    if "divergence" in donnees:
        return composer_divergence(donnees)
    return composer(donnees)


def _composer_vignette(donnees):
    if "divergence" in donnees:
        return composer_vignette_divergence(donnees)
    return composer_vignette(donnees)


def _composer_appui(donnees):
    if "divergence" in donnees:
        return composer_appui_divergence(donnees)
    return composer_appui(donnees)


if __name__ == "__main__":
    executer(_composer, _composer_vignette, _composer_appui)
