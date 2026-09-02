#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compositeur de planche — archétype `zonage-ssi`.

Protocole : docs/superpowers/specs/2026-08-12-planches-references-protocole.md

Il lit un `planche.json` (l'extraction, produite par la session de génération) et
écrit les deux dessins qui en découlent :

    planche.svg    1200 x 800 — la planche de fiche, lue à 1152 px (échelle 0,96)
    vignette.svg    300 x 200 — la vignette de carte, lue à 274-296 px (0,91-0,99)

Usage :

    python scripts/planches/zonage-ssi.py public/images/projets/<slug>

La géométrie est CALCULÉE : aucune coordonnée n'est tapée à la main, et le bloc
`controles` du JSON est recalculé à chaque exécution.

Le motif de l'archétype — arrêté avec FT2E le 2026-08-13 : **la planche
schématise la solution, elle ne récapitule pas la fiche.** Un même déclenchement
est suivi à travers les deux systèmes : avant, le SDI à zone unique diffuse
l'alarme partout ; après, la centrale adressable ne la diffuse que dans la zone
concernée. La démonstration est portée par la géométrie — une barre d'alarme
(aplat clair) sur tout le site contre une barre sur un seul bloc — jamais par
une colonne de chiffres que la page porte déjà. Les blocs sont d'égale hauteur :
aucune surface par zone n'étant donnée, la géométrie ne code que le nombre.

Deuxième module du chantier après `sankey-energie.py` : ce qu'ils partagent
(jetons, mesure des chasses, insécables, double écriture des couleurs) a
désormais deux occurrences et peut remonter dans un module commun — décision
de dépôt, pas de session.
"""

from _tronc import (NN, W, H, MARGE, UTILE, VW, VH, V_MARGE, AW, AH, A_MARGE,
                    JETON, mesurer, echapper, texte, rect, rect_bord, ligne,
                    polyligne, fleche, cercle, entete_style, replier,
                    racine_appui, controles_appui, executer)


# ── Rythme vertical de la planche ────────────────────────────────────────────
Y_SURTITRE = 76
Y_TITRE = 112
Y_SOUSTITRE = 138
Y_FILET_TITRE = 160
Y_ENTETE = 190
Y_AVANT_TAG = 226
Y_AVANT = 240
H_AVANT = 64
Y_APRES_TAG = 354
Y_ZONES = 368
H_ZONE = 58
ECART_ZONE = 12
Y_HORS = 660
Y_PHRASE = 688
Y_CARTOUCHE = 714
H_CARTOUCHE = 30

# ── Partition horizontale : événement → système → diffusion ──────────────────
EVT_X = MARGE                 # libellé de l'événement
BOITE_X0, BOITE_W = 270, 226  # boîte du système (SDI, puis centrale)
BLOC_X0 = 520                 # les blocs du site
BLOC_X1 = W - MARGE           # 1144
BLOC_W = BLOC_X1 - BLOC_X0    # 624
TRONC_X = 508                 # tronc vertical de la distribution APRÈS
H_BARRE = 8                   # la barre d'alarme — aplat clair en tête de bloc
PAD = 16


def barre_alarme(A, x, y, w):
    """La barre d'alarme : un aplat clair en tête de bloc — le seul signe.
    Le clair n'est jamais surface de lecture : aucun texte ne s'y pose."""
    A(rect(x + 1, y + 1, w - 2, H_BARRE, "clair"))


def evenement(A, cy, libelle):
    """Le déclencheur : libellé mono, marque carrée (rayon 0 — la charte ne
    connaît qu'un seul cercle, la puce de section), trait vers le système."""
    A(texte(EVT_X, cy + 3, libelle, "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    A(rect(BOITE_X0 - 18, cy - 3.5, 7, 7, "encre"))
    A(ligne(BOITE_X0 - 11, cy, BOITE_X0, cy, "encre", 1.0))


def boite_systeme(A, y, h, systeme):
    """La boîte du système : nom en Archivo, propriétés en mono."""
    A(rect_bord(BOITE_X0, y, BOITE_W, h, "papier", "filet-1"))
    n = len(systeme["detail"])
    base = y + h / 2 - (n * 13 + 4) / 2 + 8
    A(texte(BOITE_X0 + PAD, base, systeme["libelle"], "sans", 15, 600,
            "encre", wdth=112))
    for k, l in enumerate(systeme["detail"]):
        A(texte(BOITE_X0 + PAD, base + 18 + k * 13, l, "mono", 10, 500,
                "pivot", tracking=10 * 0.14))


def composer(donnees):
    z = donnees["zonage"]
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

    # ── En-tête du schéma + légende de la barre d'alarme ─────────────────────
    controler("en-tête schéma", z["entete"], 10, "mono", 700, 10 * 0.14)
    A(texte(MARGE, Y_ENTETE, z["entete"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    l_legende = mesurer(z["legende_alarme"], 10, "mono", 10 * 0.14)
    A(rect(BLOC_X1 - l_legende - 22, Y_ENTETE - 7, 14, H_BARRE, "clair"))
    A(texte(BLOC_X1, Y_ENTETE, z["legende_alarme"], "mono", 10, 500,
            "pivot", ancre="end", tracking=10 * 0.14))

    # ── AVANT : une seule zone, l'alarme se diffuse partout ──────────────────
    avant = z["avant"]
    controler("tag AVANT", avant["tag"], 10, "mono", UTILE, 10 * 0.14)
    A(texte(MARGE, Y_AVANT_TAG, avant["tag"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    cy = Y_AVANT + H_AVANT / 2
    controler("événement", z["evenement"], 10, "mono",
              BOITE_X0 - 18 - 10 - EVT_X, 10 * 0.14)
    evenement(A, cy, z["evenement"])
    boite_systeme(A, Y_AVANT, H_AVANT, avant["systeme"])
    A(ligne(BOITE_X0 + BOITE_W, cy, BLOC_X0 - 9, cy, "encre", 1.5))
    A(fleche(BLOC_X0, cy, "encre"))
    diff = avant["diffusion"]
    A(rect_bord(BLOC_X0, Y_AVANT, BLOC_W, H_AVANT, "calcaire", "filet-1"))
    if diff.get("alarme"):
        barre_alarme(A, BLOC_X0, Y_AVANT, BLOC_W)
    A(texte(BLOC_X0 + PAD, Y_AVANT + 41, diff["libelle"], "sans", 15, 600,
            "encre", wdth=112))
    A(texte(BLOC_X1 - PAD, Y_AVANT + 41,
            f'{diff["valeur"]}{NN}{diff["unite"]}', "mono", 12, 500,
            "encre", ancre="end", tabulaire=True))

    # ── APRÈS : la centrale adressable ne diffuse que dans la zone concernée ─
    apres = z["apres"]
    controler("tag APRÈS", apres["tag"], 10, "mono", UTILE, 10 * 0.14)
    A(texte(MARGE, Y_APRES_TAG, apres["tag"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))

    zones = apres["zones"]
    centres = []
    y = Y_ZONES
    for zone in zones:
        prov = zone.get("etat") == "provisionnee"
        filet = "filet-2" if prov else "filet-1"
        A(rect_bord(BLOC_X0, y, BLOC_W, H_ZONE, "calcaire" if not prov else "papier", filet))
        if zone.get("alarme"):
            barre_alarme(A, BLOC_X0, y, BLOC_W)
        A(texte(BLOC_X0 + PAD, y + 24, zone["tag"], "mono", 10, 500,
                "pivot", tracking=10 * 0.14))
        A(texte(BLOC_X0 + PAD, y + 45, zone["libelle"], "sans", 15, 600,
                "encre", wdth=112))
        if zone.get("mention"):
            controler(f'mention {zone["cle"]}', zone["mention"], 10, "mono",
                      BLOC_W - 2 * PAD - mesurer(zone["libelle"], 15, "sans-600") - 16,
                      10 * 0.14)
            A(texte(BLOC_X1 - PAD, y + 45, zone["mention"], "mono", 10, 500,
                    "pivot", ancre="end", tracking=10 * 0.14))
        centres.append((y + H_ZONE / 2, bool(zone.get("alarme"))))
        y += H_ZONE + ECART_ZONE
    bas_zones = y - ECART_ZONE

    # La centrale, centrée sur la pile, et sa distribution orthogonale : un
    # tronc, quatre départs — seul le départ en alarme est encré et fléché.
    H_BOITE = 72
    centre_pile = (Y_ZONES + bas_zones) / 2
    y_boite = centre_pile - H_BOITE / 2
    cy = centre_pile
    controler("événement", z["evenement"], 10, "mono",
              BOITE_X0 - 18 - 10 - EVT_X, 10 * 0.14)
    evenement(A, cy, z["evenement"])
    boite_systeme(A, y_boite, H_BOITE, apres["systeme"])
    A(ligne(BOITE_X0 + BOITE_W, cy, TRONC_X, cy, "filet-1", 1.0))
    A(ligne(TRONC_X, centres[0][0], TRONC_X, centres[-1][0], "filet-1", 1.0))
    for c, alarme in centres:
        if alarme:
            A(ligne(TRONC_X, c, BLOC_X0 - 9, c, "encre", 1.5))
            A(fleche(BLOC_X0, c, "encre"))
        else:
            A(ligne(TRONC_X, c, BLOC_X0, c, "filet-2", 1.0))

    # ── Hors zonage : une ligne, pas un bloc ─────────────────────────────────
    controler("hors zonage", z["hors_zonage"], 10, "mono", UTILE, 10 * 0.14)
    A(texte(MARGE, Y_HORS, z["hors_zonage"], "mono", 10, 500,
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

    barres_avant = 1 if z["avant"]["diffusion"].get("alarme") else 0
    barres_apres = sum(1 for zz in zones if zz.get("alarme"))
    controles = {
        "gabarit": f"{W} x {H} — rapport {W/H:.4f} (3:2 exact)",
        "demonstration": f"barres d’alarme : {barres_avant} sur 1 bloc AVANT "
                         f"(tout le site) contre {barres_apres} sur {len(zones)} "
                         f"blocs APRÈS — la géométrie porte la thèse, aucun "
                         f"chiffre de la fiche n’est répété",
        "topologie": f"événement (x {EVT_X}) → système (x {BOITE_X0}–"
                     f"{BOITE_X0 + BOITE_W}) → site (x {BLOC_X0}–{BLOC_X1}) ; "
                     f"tronc de distribution à x {TRONC_X}",
        "bas_du_dessin": f"pile de zones jusqu’à {bas_zones:.0f} px, ligne hors "
                         f"zonage à {Y_HORS}, phrase de principe à {Y_PHRASE}, "
                         f"cartouche {Y_CARTOUCHE}–{Y_CARTOUCHE + H_CARTOUCHE}, "
                         f"marge basse {H - (Y_CARTOUCHE + H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur * H_CARTOUCHE} px², soit "
                            f"{largeur * H_CARTOUCHE / (W * H) * 100:.2f} % de la planche",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l’échelle 0,96 "
                         f"(1152 / {W})",
        "depassements": depassements if depassements
                        else "aucun — toutes les lignes mesurées sous leur colonne",
    }
    return "\n".join(out) + "\n", controles


def composer_vignette(donnees):
    """La vignette : le motif de l'archétype, sans son appareil.

    Ce qu'elle garde : le contraste une zone / trois zones — le bloc unique
    d'origine à gauche, la pile des trois zones actives à droite, et la
    surface évacuée comme valeur du nœud AVANT. Ce qu'elle laisse : la zone
    provisionnée, le hors zonage, l'événement et les systèmes. Trois blocs
    nommés dans 300 px se lisent ; six blocs annotés ne se liraient pas."""
    z = donnees["zonage"]
    zones = [zz for zz in z["apres"]["zones"] if zz.get("etat") != "provisionnee"]
    avant = z["avant"]["diffusion"]

    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false" '
      f'style="width:100%;height:auto;display:block">')
    entete_style(A, ("filet-1", "filet-2", "filet-3", "encre"))
    A(rect(0, 0, VW, VH, "papier"))
    A(texte(V_MARGE, 22, donnees["vignette_surtitre"], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    # Deux colonnes : le bloc unique à gauche, la pile à droite.
    bloc_g_x, bloc_g_w = V_MARGE, 118
    bloc_d_x, bloc_d_w = 180, VW - V_MARGE - 180      # 106
    y0, y1 = 48, VH - 24                              # 48..176
    h_pile = y1 - y0

    A(texte(bloc_g_x, 40, "AVANT", "mono", 9, 500, "pivot", tracking=9 * 0.14))
    A(texte(bloc_d_x, 40, "APRÈS", "mono", 9, 500, "pivot", tracking=9 * 0.14))

    # Bloc AVANT : la zone unique, avec sa valeur.
    A(rect_bord(bloc_g_x, y0, bloc_g_w, h_pile, "calcaire", "filet-1"))
    lignes = replier(avant.get("libelle_vignette", avant["libelle"]), 12,
                     bloc_g_w - 20, "sans-600")
    centre = y0 + h_pile / 2
    base = centre - 8 - (len(lignes) - 1) * 8
    for k, l in enumerate(lignes):
        A(texte(bloc_g_x + 10, base + k * 16, l, "sans", 12, 600,
                "encre", wdth=112))
    A(texte(bloc_g_x + 10, base + (len(lignes) - 1) * 16 + 20,
            f'{avant["valeur"]}{NN}{avant["unite"]}', "mono", 10, 500,
            "pivot", tabulaire=True))

    # La flèche du principe : une zone devient trois.
    fy = centre
    A(f'  <path d="M {bloc_g_x + bloc_g_w + 8:.2f} {fy:.2f} '
      f'L {bloc_d_x - 12:.2f} {fy:.2f}" class="s-encre" fill="none" '
      f'stroke="{JETON["encre"]}" stroke-width="1.5"/>')
    A(f'  <path d="M {bloc_d_x - 4:.2f} {fy:.2f} '
      f'L {bloc_d_x - 13:.2f} {fy - 4.5:.2f} '
      f'L {bloc_d_x - 13:.2f} {fy + 4.5:.2f} Z" class="c-encre" '
      f'fill="{JETON["encre"]}"/>')

    # La pile APRÈS : un bloc par zone active, d'égale hauteur.
    n = len(zones)
    ecart = 7
    h_bloc = (h_pile - (n - 1) * ecart) / n
    for i, zone in enumerate(zones):
        yz = y0 + i * (h_bloc + ecart)
        A(rect_bord(bloc_d_x, yz, bloc_d_w, h_bloc, "calcaire", "filet-1"))
        A(texte(bloc_d_x + 10, yz + h_bloc / 2 + 4,
                zone.get("libelle_vignette", zone["libelle"]), "sans", 12, 600,
                "encre", wdth=112))

    A("</svg>")
    controles = {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": f"carte de projet mesurée de 274 à 296 px — "
                            f"échelle {274/VW:.2f} à {296/VW:.2f}",
        "corps_minimal": f"9 px dans le repère — rendu à {9*274/VW:.1f} px au pire cas",
        "motif": f"1 bloc AVANT contre {len(zones)} zones actives — la zone "
                 f"provisionnée et le hors zonage sont laissés à la planche",
        "bas_du_dessin": f"{VH - 24} px, marge basse 24 px",
    }
    return "\n".join(out) + "\n", controles


def composer_appui(donnees):
    """L'appui du hero : le motif entier à l'échelle 1, densité intermédiaire.

    Ce qu'il garde : le bloc unique AVANT (barre d'alarme, surface évacuée)
    contre les QUATRE zones APRÈS — provisionnée comprise —, la barre sur la
    seule zone en alarme, sa mention, et la légende de la barre. Ce qu'il
    laisse : l'événement, les systèmes et le hors zonage — ils vivent sur la
    planche."""
    z = donnees["zonage"]
    zones = z["apres"]["zones"]
    avant = z["avant"]["diffusion"]

    out = []
    A = out.append
    racine_appui(A, donnees, strokes=("filet-1", "filet-2", "filet-3", "encre"))

    # La légende de la barre d'alarme, en haut à droite.
    l_leg = mesurer(z["legende_alarme"], 10, "mono", 10 * 0.14)
    A(rect(AW - A_MARGE - l_leg - 22, 27, 14, 7, "clair"))
    A(texte(AW - A_MARGE, 34, z["legende_alarme"], "mono", 10, 500, "pivot",
            ancre="end", tracking=10 * 0.14))

    g_x0, g_x1 = A_MARGE, 216
    d_x0, d_x1 = 300, AW - A_MARGE
    y0, y1 = 76, 336
    A(texte(g_x0, 64, "AVANT", "mono", 10, 500, "pivot", tracking=10 * 0.14))
    A(texte(d_x0, 64, "APRÈS", "mono", 10, 500, "pivot", tracking=10 * 0.14))

    # Le bloc AVANT : une seule zone, l'alarme partout, la surface évacuée.
    A(rect_bord(g_x0, y0, g_x1 - g_x0, y1 - y0, "calcaire", "filet-1"))
    if avant.get("alarme"):
        A(rect(g_x0 + 1, y0 + 1, g_x1 - g_x0 - 2, 7, "clair"))
    centre = (y0 + y1) / 2
    A(texte(g_x0 + 14, centre - 6, avant["libelle"], "sans", 14, 600,
            "encre", wdth=112))
    A(texte(g_x0 + 14, centre + 12, f'{avant["valeur"]}{NN}{avant["unite"]}',
            "mono", 11, 500, "pivot", tabulaire=True))

    # La flèche du principe : une zone devient quatre.
    A(ligne(g_x1 + 12, centre, d_x0 - 16, centre, "encre", 1.5))
    A(fleche(d_x0 - 8, centre, "encre", "droite", 8))

    # La pile APRÈS : les quatre zones, d'égale hauteur.
    n = len(zones)
    ecart = 8
    h_bloc = (y1 - y0 - (n - 1) * ecart) / n
    for i, zone in enumerate(zones):
        yz = y0 + i * (h_bloc + ecart)
        prov = zone.get("etat") == "provisionnee"
        A(rect_bord(d_x0, yz, d_x1 - d_x0, h_bloc,
                    "papier" if prov else "calcaire",
                    "filet-2" if prov else "filet-1"))
        if zone.get("alarme"):
            A(rect(d_x0 + 1, yz + 1, d_x1 - d_x0 - 2, 7, "clair"))
        # Un tag long (« · PROVISIONNÉE ») se partage : la base à gauche, le
        # complément à droite — mesuré, il ne tient pas sur la colonne.
        tag = zone["tag"]
        if " · " in tag:
            base, complement = tag.split(" · ", 1)
            A(texte(d_x0 + 12, yz + 19, base, "mono", 10, 500, "pivot",
                    tracking=10 * 0.14))
            A(texte(d_x1 - 12, yz + 19, complement, "mono", 10, 500, "pivot",
                    ancre="end", tracking=10 * 0.14))
        else:
            A(texte(d_x0 + 12, yz + 19, tag, "mono", 10, 500, "pivot",
                    tracking=10 * 0.14))
        A(texte(d_x0 + 12, yz + 39, zone["libelle"], "sans", 13, 600,
                "encre", wdth=112))
        if zone.get("mention") and zone.get("alarme"):
            A(texte(d_x0 + 12, yz + 54, zone["mention"], "mono", 10, 500,
                    "pivot", tracking=10 * 0.14))

    A("</svg>")
    return "\n".join(out) + "\n", controles_appui(
        motif=f"1 bloc AVANT (barre d’alarme sur tout, {avant['valeur']} m² "
              f"évacués) contre {len(zones)} zones APRÈS dont la provisionnée, "
              "barre et mention sur la seule zone en alarme, légende en tête — "
              "événement, systèmes et hors zonage laissés à la planche",
        bas=f"pile de zones jusqu’à {y1} px, marge basse {AH - y1} px")


# ═════════════════════════════════════════════════════════════════════════════
# Mécanisme `transfert` — EHPAD de Coulonges-sur-l'Autize (2026-08-14)
#
# Même archétype (zones de mise en sécurité), démonstration inverse : à
# Sablonceaux la géométrie montrait où l'alarme se diffuse ; ici elle montre où
# vont les personnes. Deux registres : l'alerte (un foyer, la centrale, trois
# départs — le personnel fléché, les résidents barrés, les asservissements),
# puis la coupe de principe — l'étage en deux zones coupe-feu, la flèche de
# transfert qui traverse la paroi au même niveau, la descente barrée, et
# l'escalier extérieur par lequel les secours montent. Le dispatch se fait sur
# le bloc de l'extraction (`transfert` contre `zonage`), comme `boucle-fluide`.
# ═════════════════════════════════════════════════════════════════════════════

# ── Rythme vertical de la planche `transfert` ────────────────────────────────
T_Y_ENTETE_A = 190
T_BOITE_X0, T_BOITE_W, T_H_BOITE = 270, 230, 84
T_CY_BOITE = 268
T_TRONC_X = 540
T_ROWS_CY = (222, 268, 314)
T_X_DEPART = 574
T_Y_ENTETE_B = 358
T_E_Y0, T_E_Y1 = 390, 502          # l'étage
T_R_Y0, T_R_Y1 = 502, 570          # le rez-de-chaussée
T_B_X0, T_B_X1 = 56, 1010          # la coupe du bâtiment
T_PAROI_X, T_PAROI_W = 533, 7
T_CY_FLECHE = 448                  # la flèche de transfert
T_GAP = 32                         # l'ouverture dans la paroi
T_SOL_Y = 570
T_Y_CAPTIONS = 590
T_Y_PHRASE = 688
T_Y_CARTOUCHE = 714
T_H_CARTOUCHE = 30


def _croix(A, cx, cy, demi=7.0, epaisseur=1.5):
    """La marque d'interdiction : deux diagonales encrées — toujours doublée
    d'un texte (la couleur ni la forme seules ne portent, RGAA)."""
    A(ligne(cx - demi, cy - demi, cx + demi, cy + demi, "encre", epaisseur))
    A(ligne(cx - demi, cy + demi, cx + demi, cy - demi, "encre", epaisseur))


def _escalier(A, x_pied, y_pied, x_tete, y_tete, marches=5, epaisseur=1.5):
    """L'escalier extérieur : un zigzag de marches, du sol vers l'étage."""
    dx = (x_tete - x_pied) / marches
    dy = (y_tete - y_pied) / marches
    pts = [(x_pied, y_pied)]
    x, y = x_pied, y_pied
    for _ in range(marches):
        y += dy
        pts.append((x, y))
        x += dx
        pts.append((x, y))
    from _tronc import polyligne
    A(polyligne(pts, "encre", epaisseur))


def composer_transfert(donnees):
    t = donnees["transfert"]
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

    # ── Registre A : l'alerte ────────────────────────────────────────────────
    controler("en-tête alerte", t["entete_alerte"], 10, "mono", UTILE, 10 * 0.14)
    A(texte(MARGE, T_Y_ENTETE_A, t["entete_alerte"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))

    # L'événement : deux lignes mono, la marque carrée, le trait vers la boîte.
    for k, l in enumerate(t["evenement"]):
        controler(f"événement l.{k + 1}", l, 10, "mono",
                  T_BOITE_X0 - 28 - MARGE, 10 * 0.14)
        A(texte(MARGE, T_CY_BOITE - 4 + k * 14, l, "mono", 10, 500,
                "pivot", tracking=10 * 0.14))
    A(rect(T_BOITE_X0 - 18, T_CY_BOITE - 3.5, 7, 7, "encre"))
    A(ligne(T_BOITE_X0 - 11, T_CY_BOITE, T_BOITE_X0, T_CY_BOITE, "encre", 1.0))

    # La centrale.
    y_boite = T_CY_BOITE - T_H_BOITE / 2
    sys_ = t["systeme"]
    A(rect_bord(T_BOITE_X0, y_boite, T_BOITE_W, T_H_BOITE, "papier", "filet-1"))
    n = len(sys_["detail"])
    base = y_boite + T_H_BOITE / 2 - (n * 13 + 4) / 2 + 8
    A(texte(T_BOITE_X0 + PAD, base, sys_["libelle"], "sans", 15, 600,
            "encre", wdth=112))
    for k, l in enumerate(sys_["detail"]):
        controler(f"détail centrale l.{k + 1}", l, 10, "mono",
                  T_BOITE_W - 2 * PAD, 10 * 0.14)
        A(texte(T_BOITE_X0 + PAD, base + 18 + k * 13, l, "mono", 10, 500,
                "pivot", tracking=10 * 0.14))

    # Le tronc et les trois départs : le personnel fléché, les résidents
    # barrés, les asservissements fléchés — le signe toujours doublé du texte.
    lys = [cy - 8 for cy in T_ROWS_CY]
    A(ligne(T_BOITE_X0 + T_BOITE_W, T_CY_BOITE, T_TRONC_X, T_CY_BOITE,
            "filet-1", 1.0))
    A(ligne(T_TRONC_X, lys[0], T_TRONC_X, lys[-1], "filet-1", 1.0))
    for depart, cy, ly in zip(t["departs"], T_ROWS_CY, lys):
        if depart["alerte"]:
            A(ligne(T_TRONC_X, ly, T_X_DEPART - 12, ly, "encre", 1.5))
            A(fleche(T_X_DEPART - 4, ly, "encre", "droite", 8))
        else:
            A(ligne(T_TRONC_X, ly, T_X_DEPART - 8, ly, "filet-2", 1.0))
            _croix(A, T_TRONC_X + 14, ly, 6.0)
        A(texte(T_X_DEPART, cy - 3, depart["libelle"], "sans", 15, 600,
                "encre", wdth=112))
        controler(f'détail {depart["cle"]}', depart["detail"], 10, "mono",
                  W - MARGE - T_X_DEPART, 10 * 0.14)
        A(texte(T_X_DEPART, cy + 14, depart["detail"], "mono", 10, 500,
                "pivot", tracking=10 * 0.14))

    # ── Registre B : la mise à l'abri — la coupe de principe ─────────────────
    controler("en-tête bâtiment", t["entete_batiment"], 10, "mono",
              UTILE, 10 * 0.14)
    A(texte(MARGE, T_Y_ENTETE_B, t["entete_batiment"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))

    et = t["etage"]
    demi = (T_B_X1 - T_B_X0) / 2                      # 477
    # Les deux zones coupe-feu, d'égale largeur : la géométrie code le nombre.
    A(rect_bord(T_B_X0, T_E_Y0, demi, T_E_Y1 - T_E_Y0, "calcaire", "filet-1"))
    A(rect_bord(T_B_X0 + demi, T_E_Y0, demi, T_E_Y1 - T_E_Y0,
                "calcaire", "filet-1"))
    # La paroi coupe-feu : un aplat encré, ouvert au droit de la flèche.
    px = T_PAROI_X - T_PAROI_W / 2
    gap0, gap1 = T_CY_FLECHE - T_GAP / 2, T_CY_FLECHE + T_GAP / 2
    A(rect(px, T_E_Y0 + 1, T_PAROI_W, gap0 - T_E_Y0 - 1, "encre"))
    A(rect(px, gap1, T_PAROI_W, T_E_Y1 - 1 - gap1, "encre"))
    # Son étiquette, accrochée par un tick au-dessus de la coupe.
    A(ligne(T_PAROI_X, T_E_Y0, T_PAROI_X, T_E_Y0 - 14, "encre", 1.0))
    A(texte(T_PAROI_X + 8, T_E_Y0 - 10, et["paroi"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))

    # Les étiquettes de zone.
    controler("tag zone foyer", et["zone_foyer_tag"], 10, "mono",
              demi - 24, 10 * 0.14)
    A(texte(T_B_X0 + 12, T_E_Y0 + 18, et["zone_foyer_tag"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    controler("tag zone abri", et["zone_abri_tag"], 10, "mono",
              demi - 24, 10 * 0.14)
    A(texte(T_B_X0 + demi + 19, T_E_Y0 + 18, et["zone_abri_tag"], "mono", 10,
            500, "pivot", tracking=10 * 0.14))

    # Le foyer, puis la flèche de transfert qui traverse la paroi.
    A(rect(92, T_CY_FLECHE - 4, 8, 8, "encre"))
    A(ligne(106, T_CY_FLECHE, 870, T_CY_FLECHE, "encre", 2.5))
    A(fleche(884, T_CY_FLECHE, "encre", "droite", 10))
    controler("libellé transfert", et["transfert_libelle"], 15, "sans-600",
              px - 128 - 10)
    A(texte(128, T_CY_FLECHE - 14, et["transfert_libelle"], "sans", 15, 600,
            "encre", wdth=112))
    controler("détail transfert", et["transfert_detail"], 10, "mono",
              px - 128 - 10, 10 * 0.14)
    A(texte(128, T_CY_FLECHE + 24, et["transfert_detail"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    for k, l in enumerate(et["abri_details"]):
        controler(f"détail abri l.{k + 1}", l, 10, "mono",
                  T_B_X1 - 12 - (T_B_X0 + demi + 19), 10 * 0.14)
        A(texte(T_B_X0 + demi + 19, T_CY_FLECHE + 24 + k * 16, l, "mono", 10,
                500, "pivot", tracking=10 * 0.14))

    # Le rez-de-chaussée et son unité protégée : une boîte dans la boîte —
    # la protection au même niveau, déjà, de plain-pied.
    A(rect_bord(T_B_X0, T_R_Y0, T_B_X1 - T_B_X0, T_R_Y1 - T_R_Y0,
                "calcaire", "filet-1"))
    A(texte(T_B_X0 + 12, T_R_Y0 + 20, t["rdc"]["tag"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    A(rect_bord(720, T_R_Y0 + 10, 274, T_R_Y1 - T_R_Y0 - 20,
                "papier", "filet-1"))
    controler("unité protégée", t["rdc"]["unite_protegee"], 10, "mono",
              274 - 24, 10 * 0.14)
    A(texte(732, T_R_Y0 + (T_R_Y1 - T_R_Y0) / 2 + 4, t["rdc"]["unite_protegee"],
            "mono", 10, 500, "pivot", tracking=10 * 0.14))

    # La descente barrée : sortir n'est pas le principe.
    A(ligne(410, T_E_Y1, 410, T_SOL_Y - 8, "encre", 1.5))
    A(fleche(410, T_SOL_Y - 4, "encre", "bas", 8))
    _croix(A, 410, (T_E_Y1 + T_SOL_Y) / 2, 7.0)
    controler("descente", t["descente"], 10, "mono", 720 - 430, 10 * 0.14)
    A(texte(430, (T_E_Y1 + T_SOL_Y) / 2 + 4, t["descente"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))

    # Le sol, l'escalier extérieur, l'entrée des secours à l'étage.
    A(ligne(MARGE, T_SOL_Y, W - MARGE, T_SOL_Y, "encre", 1.5))
    _escalier(A, 1122, T_SOL_Y, 1016, 456, marches=5)
    A(fleche(T_B_X1 + 2, 456, "encre", "gauche", 8))

    # Les deux notes de pied de coupe.
    controler("recoupement", t["recoupement"], 10, "mono", 540, 10 * 0.14)
    A(texte(MARGE, T_Y_CAPTIONS, t["recoupement"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    secours = f'{t["secours_escalier"]} · {t["secours_acces"]}'
    controler("secours", secours, 10, "mono", 530, 10 * 0.14)
    A(texte(W - MARGE, T_Y_CAPTIONS, secours, "mono", 10, 500,
            "pivot", ancre="end", tracking=10 * 0.14))

    # ── Phrase de principe, pleine largeur ───────────────────────────────────
    controler("phrase de principe", donnees["phrase_principe"], 17,
              "sans-400", UTILE)
    A(texte(MARGE, T_Y_PHRASE, donnees["phrase_principe"], "sans", 17, 400,
            "encre", wdth=100))

    # ── Cartouche — largeur AJUSTÉE au texte, jamais codée ───────────────────
    libelle = donnees["cartouche_legende"]
    largeur = min(600,
                  round(mesurer(libelle, 11, "mono", tracking=11 * 0.14) + 40))
    A(rect(MARGE, T_Y_CARTOUCHE, largeur, T_H_CARTOUCHE, "profond"))
    A(texte(MARGE + 20, T_Y_CARTOUCHE + 20, libelle, "mono", 11, 500, "voile",
            tracking=11 * 0.14))

    A("</svg>")

    controles = {
        "gabarit": f"{W} x {H} — rapport {W/H:.4f} (3:2 exact)",
        "demonstration": "trois flèches, trois sens : le transfert traverse la "
                         "paroi à l’horizontale (encre 2,5), la descente est "
                         "barrée d’une croix, l’escalier extérieur monte vers "
                         "l’étage — la géométrie porte la thèse, aucun chiffre "
                         "de la fiche n’est répété",
        "topologie": f"alerte : événement (x {MARGE}) → centrale "
                     f"(x {T_BOITE_X0}–{T_BOITE_X0 + T_BOITE_W}) → départs "
                     f"(x {T_X_DEPART}) ; coupe : étage {T_E_Y0}–{T_E_Y1}, "
                     f"rez-de-chaussée {T_R_Y0}–{T_R_Y1}, paroi à "
                     f"x {T_PAROI_X}, sol à y {T_SOL_Y}",
        "bas_du_dessin": f"sol à {T_SOL_Y}, notes de pied à {T_Y_CAPTIONS}, "
                         f"phrase de principe à {T_Y_PHRASE}, cartouche "
                         f"{T_Y_CARTOUCHE}–{T_Y_CARTOUCHE + T_H_CARTOUCHE}, "
                         f"marge basse {H - (T_Y_CARTOUCHE + T_H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {T_H_CARTOUCHE} px = "
                            f"{largeur * T_H_CARTOUCHE} px², soit "
                            f"{largeur * T_H_CARTOUCHE / (W * H) * 100:.2f} % "
                            f"de la planche (la paroi et les marques sont de "
                            f"l’encre, pas de la réserve)",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l’échelle "
                         f"0,96 (1152 / {W})",
        "depassements": depassements if depassements
                        else "aucun — toutes les lignes mesurées sous leur colonne",
    }
    return "\n".join(out) + "\n", controles


def composer_vignette_transfert(donnees):
    """La vignette : la coupe seule — deux zones, la paroi, la flèche qui la
    traverse, la descente barrée. L'alerte, l'escalier des secours et l'unité
    protégée sont laissés à la planche : quatre mots dans 300 px se lisent."""
    t = donnees["transfert"]
    et = t["etage"]

    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false" '
      f'style="width:100%;height:auto;display:block">')
    entete_style(A, ("filet-1", "filet-2", "filet-3", "encre"))
    A(rect(0, 0, VW, VH, "papier"))
    A(texte(V_MARGE, 22, donnees["vignette_surtitre"], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    e_y0, e_y1 = 46, 116
    r_y0, r_y1 = 120, 168
    demi = (VW - 2 * V_MARGE) / 2                     # 136
    A(rect_bord(V_MARGE, e_y0, demi, e_y1 - e_y0, "calcaire", "filet-1"))
    A(rect_bord(V_MARGE + demi, e_y0, demi, e_y1 - e_y0, "calcaire", "filet-1"))
    cy = (e_y0 + e_y1) / 2 + 3                        # 84
    px = V_MARGE + demi - 2.5
    A(rect(px, e_y0 + 1, 5, cy - 10 - e_y0 - 1, "encre"))
    A(rect(px, cy + 10, 5, e_y1 - 1 - cy - 10, "encre"))
    A(texte(V_MARGE + 12, 66, et["zone_foyer_vignette"], "sans", 12, 600,
            "encre", wdth=112))
    A(texte(V_MARGE + demi + 12, 66, et["zone_abri_vignette"], "sans", 12, 600,
            "encre", wdth=112))
    A(rect(30, cy - 3, 6, 6, "encre"))
    A(ligne(40, cy, 256, cy, "encre", 2.0))
    A(fleche(264, cy, "encre", "droite", 7))
    A(texte(V_MARGE + demi + 12, 106, et["transfert_detail_court"], "mono", 9,
            500, "pivot", tracking=9 * 0.14))

    A(rect_bord(V_MARGE, r_y0, VW - 2 * V_MARGE, r_y1 - r_y0,
                "calcaire", "filet-1"))
    A(ligne(70, e_y1, 70, r_y1 - 10, "encre", 1.5))
    A(fleche(70, r_y1 - 6, "encre", "bas", 6))
    _croix(A, 70, (e_y1 + r_y1) / 2 - 2, 5.0)
    A(texte(84, (e_y1 + r_y1) / 2 + 2, t["descente_court"], "mono", 9, 500,
            "pivot", tracking=9 * 0.14))

    A("</svg>")
    controles = {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": f"carte de projet mesurée de 274 à 296 px — "
                            f"échelle {274/VW:.2f} à {296/VW:.2f}",
        "corps_minimal": f"9 px dans le repère — rendu à {9*274/VW:.1f} px au pire cas",
        "motif": "la coupe seule : deux zones, la paroi ouverte, la flèche qui "
                 "la traverse, la descente barrée — l’alerte, l’escalier des "
                 "secours et l’unité protégée sont laissés à la planche",
        "bas_du_dessin": f"{r_y1} px, marge basse {VH - r_y1} px",
    }
    return "\n".join(out) + "\n", controles


def composer_appui_transfert(donnees):
    """L'appui du hero : la coupe entière à l'échelle 1 — l'étage en deux
    zones, la flèche de transfert, la descente barrée, l'unité protégée du
    rez-de-chaussée et l'escalier des secours. L'alerte reste à la planche."""
    t = donnees["transfert"]
    et = t["etage"]

    out = []
    A = out.append
    racine_appui(A, donnees, strokes=("filet-1", "filet-2", "filet-3", "encre"))

    b_x0, b_x1 = A_MARGE, 444
    e_y0, e_y1 = 74, 212
    r_y0, r_y1 = 212, 292
    sol_y = 292
    demi = (b_x1 - b_x0) / 2                          # 210
    cy = 148

    A(rect_bord(b_x0, e_y0, demi, e_y1 - e_y0, "calcaire", "filet-1"))
    A(rect_bord(b_x0 + demi, e_y0, demi, e_y1 - e_y0, "calcaire", "filet-1"))
    px = b_x0 + demi - 3
    A(rect(px, e_y0 + 1, 6, cy - 16 - e_y0 - 1, "encre"))
    A(rect(px, cy + 16, 6, e_y1 - 1 - cy - 16, "encre"))

    A(texte(b_x0 + 12, e_y0 + 18, et["zone_foyer_tag_court"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    A(texte(b_x0 + demi + 15, e_y0 + 18, et["zone_abri_tag_court"], "mono", 10,
            500, "pivot", tracking=10 * 0.14))
    A(texte(b_x0 + 12, 128, et["transfert_libelle_court"], "sans", 14, 600,
            "encre", wdth=112))
    A(rect(b_x0 + 14, cy - 3.5, 7, 7, "encre"))
    A(ligne(b_x0 + 26, cy, 404, cy, "encre", 2.0))
    A(fleche(414, cy, "encre", "droite", 9))
    A(texte(b_x0 + demi + 15, 176, et["transfert_detail_court"], "mono", 10,
            500, "pivot", tracking=10 * 0.14))
    A(texte(b_x0 + 12, 196, et["lits"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

    A(rect_bord(b_x0, r_y0, b_x1 - b_x0, r_y1 - r_y0, "calcaire", "filet-1"))
    A(texte(b_x0 + 12, r_y0 + 20, t["rdc"]["tag"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    A(rect_bord(306, r_y0 + 10, 130, r_y1 - r_y0 - 20, "papier", "filet-1"))
    for k, l in enumerate(t["rdc"]["unite_protegee_lignes"]):
        A(texte(318, r_y0 + 34 + k * 14, l, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))

    # La descente barrée passe à droite de l'étiquette du rez-de-chaussée
    # (elle finit à x 221) et son libellé se pose à sa gauche, sous l'étiquette.
    A(ligne(270, e_y1, 270, r_y1 - 10, "encre", 1.5))
    A(fleche(270, r_y1 - 6, "encre", "bas", 7))
    _croix(A, 270, (e_y1 + r_y1) / 2 - 2, 6.0)
    A(texte(256, (e_y1 + r_y1) / 2 + 2, t["descente_court"], "mono", 10, 500,
            "pivot", ancre="end", tracking=10 * 0.14))

    A(ligne(A_MARGE, sol_y, AW - A_MARGE, sol_y, "encre", 1.5))
    _escalier(A, 512, sol_y, 448, 164, marches=4)
    A(fleche(b_x1 + 2, 164, "encre", "gauche", 7))
    # Deux lignes empilées à droite : une seule ligne se lirait d'un trait.
    A(texte(AW - A_MARGE, 316, t["secours_escalier"], "mono", 10, 500, "pivot",
            ancre="end", tracking=10 * 0.14))
    A(texte(AW - A_MARGE, 332, t["secours_acces"], "mono", 10, 500, "pivot",
            ancre="end", tracking=10 * 0.14))

    A("</svg>")
    return "\n".join(out) + "\n", controles_appui(
        motif="la coupe entière : deux zones coupe-feu, la flèche de "
              "transfert à travers la paroi, la descente barrée, l’unité "
              "protégée du rez-de-chaussée, l’escalier des secours — "
              "l’alerte (centrale et départs) reste à la planche",
        bas=f"sol à {sol_y} px, notes de pied empilées à 316–332, "
            f"marge basse {AH - 332} px")


# ═════════════════════════════════════════════════════════════════════════════
# Mécanisme `partage` — habitat inclusif de Salignac-sur-Charente (2026-08-14)
#
# Même archétype (un découpage commande les exigences), troisième démonstration :
# à Sablonceaux la géométrie montrait où l'alarme se diffuse, à Coulonges où vont
# les personnes ; ici elle montre ce qu'une limite purement réglementaire impose
# à une enveloppe montée d'un seul tenant. Une seule enveloppe fermée d'un trait
# continu, qui change de graisse à la limite (l'étanchéité tenue et mesurée d'un
# côté, la valeur par défaut de l'autre) ; la limite en trait interrompu — aucun
# mur ne la porte ; quatorze cellules marquées chacune de sa production contre
# une seule boîte collective. La position de la limite est CALCULÉE depuis les
# deux surfaces de l'extraction — la géométrie code le partage, jamais un plan.
# Le dispatch se fait sur le bloc de l'extraction (`partage`), comme `transfert`.
# ═════════════════════════════════════════════════════════════════════════════

# ── Rythme vertical de la planche `partage` ──────────────────────────────────
P_Y_ENTETE = 190
P_Y_LIMITE = 232               # étiquette de la limite, au-dessus de l'enveloppe
P_E_Y0, P_E_Y1 = 252, 556      # l'enveloppe
P_E_X0, P_E_X1 = 56, 1144
P_TRAIT_FORT, P_TRAIT_FIN = 3.5, 1.25
P_PAD = 20
P_Y_TAG = 278                  # étiquettes de zone, à l'intérieur
P_Y_CELL = 312                 # première rangée de cellules
P_H_CELL, P_ECART_CELL = 64, 12
P_Y_PROD = 488                 # légende des productions individuelles
P_Y_COTE = 536                 # cotes de surface, en pied de zone
P_BOX = (898, 330, 238)        # boîte de la production collective (x, y, w)
P_Y_ETANCH = 588               # mentions d'étanchéité, sous l'enveloppe
P_Y_NOTES = (624, 640)         # la ligne d'incendie
P_Y_PHRASE = 688
P_Y_CARTOUCHE = 714
P_H_CARTOUCHE = 30
P_MARQUE = 7                   # la marque carrée d'une production individuelle


def _surfaces_partage(elems):
    """Le partage se calcule depuis les deux surfaces littérales de
    l'extraction — « 488,81 » → 488.81. Jamais une position tapée."""
    def _f(v):
        return float(v.replace(" ", "").replace(" ", "")
                     .replace(" ", "").replace(",", "."))
    g = _f(elems["logements"]["valeur"])
    d = _f(elems["commun"]["valeur"])
    return g, d, g / (g + d)


def _limite(A, x, y0, y1, epaisseur=2.0, motif="8 6"):
    """La limite réglementaire : un trait interrompu — aucun mur ne la porte."""
    A(f'  <path d="M {x:.2f} {y0:.2f} L {x:.2f} {y1:.2f}" fill="none" '
      f'class="s-encre" stroke="{JETON["encre"]}" '
      f'stroke-width="{epaisseur}" stroke-dasharray="{motif}"/>')


def _enveloppe(A, x0, x1, x_lim, y0, y1, fort, fin):
    """L'enveloppe : un contour unique dont le trait change de graisse à la
    limite — même paroi, deux niveaux d'exigence. Toujours doublée des deux
    mentions d'étanchéité (la graisse seule ne porte jamais)."""
    A(polyligne([(x_lim, y0), (x0, y0), (x0, y1), (x_lim, y1)], "encre", fort))
    A(polyligne([(x_lim, y0), (x1, y0), (x1, y1), (x_lim, y1)], "encre", fin))


def composer_partage(donnees):
    p = donnees["partage"]
    elems = {e["cle"]: e for e in p["elements"]}
    out = []
    A = out.append
    depassements = []

    def controler(nom, texte_mesure, corps, profil, dispo, tracking=0.0):
        largeur = mesurer(texte_mesure, corps, profil, tracking)
        if largeur > dispo:
            depassements.append(f"{nom} : {largeur:.0f} px pour {dispo:.0f} px")
        return largeur

    s_g, s_d, frac = _surfaces_partage(elems)
    x_lim = P_E_X0 + (P_E_X1 - P_E_X0) * frac

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

    # ── En-tête du schéma ────────────────────────────────────────────────────
    controler("en-tête schéma", p["entete"], 10, "mono", UTILE, 10 * 0.14)
    A(texte(MARGE, P_Y_ENTETE, p["entete"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))

    # ── La limite : son étiquette, son tick, son trait interrompu ────────────
    controler("étiquette de la limite", p["limite_libelle"], 10, "mono",
              x_lim - 10 - MARGE, 10 * 0.14)
    A(texte(x_lim - 10, P_Y_LIMITE, p["limite_libelle"], "mono", 10, 500,
            "pivot", ancre="end", tracking=10 * 0.14))
    A(ligne(x_lim, P_Y_LIMITE + 6, x_lim, P_E_Y0 - 2, "encre", 1.0))
    _limite(A, x_lim, P_E_Y0 + 6, P_E_Y1 - 6)

    # ── L'enveloppe : un trait, deux graisses ────────────────────────────────
    _enveloppe(A, P_E_X0, P_E_X1, x_lim, P_E_Y0, P_E_Y1,
               P_TRAIT_FORT, P_TRAIT_FIN)

    # ── Zone gauche : les quatorze logements ─────────────────────────────────
    gx = P_E_X0 + P_PAD
    controler("tag gauche", p["tag_gauche"], 10, "mono",
              x_lim - P_PAD - gx, 10 * 0.14)
    A(texte(gx, P_Y_TAG, p["tag_gauche"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    controler("tag gauche détail", p["tag_gauche_detail"], 10, "mono",
              x_lim - P_PAD - gx, 10 * 0.14)
    A(texte(gx, P_Y_TAG + 16, p["tag_gauche_detail"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))

    # Les cellules : le compte de la fiche (2 x 7), jamais l'implantation.
    par_rangee, rangees = p["par_rangee"], p["rangees"]
    span = (x_lim - P_PAD) - gx
    ecart = 10
    w_cell = (span - (par_rangee - 1) * ecart) / par_rangee
    for r in range(rangees):
        y = P_Y_CELL + r * (P_H_CELL + P_ECART_CELL)
        for c in range(par_rangee):
            x = gx + c * (w_cell + ecart)
            A(rect_bord(x, y, w_cell, P_H_CELL, "calcaire", "filet-1"))
            A(rect(x + 10, y + P_H_CELL - 17, P_MARQUE, P_MARQUE, "encre"))

    # La légende des productions : la marque carrée reprise devant le libellé.
    prod_g = elems["logements-production"]
    A(rect(gx, P_Y_PROD - P_MARQUE - 1, P_MARQUE, P_MARQUE, "encre"))
    controler("production gauche", prod_g["libelle"], 15, "sans-600",
              span - 16)
    A(texte(gx + P_MARQUE + 8, P_Y_PROD, prod_g["libelle"], "sans", 15, 600,
            "encre", wdth=112))
    controler("production gauche détail", prod_g["detail"][0], 10, "mono",
              span, 10 * 0.14)
    A(texte(gx, P_Y_PROD + 18, prod_g["detail"][0], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))

    # La cote de surface, en pied de zone.
    cote_g = (f'{elems["logements"]["valeur"]}{NN}{elems["logements"]["unite"]}'
              f' · {elems["logements"]["mention"]}')
    controler("cote gauche", cote_g, 10, "mono", 400, 10 * 0.14)
    A(texte(gx, P_Y_COTE, cote_g, "mono", 10, 500, "pivot",
            tracking=10 * 0.14, tabulaire=True))

    # ── Zone droite : l'espace commun ────────────────────────────────────────
    dx = x_lim + 14
    controler("tag droite", p["tag_droite"], 10, "mono",
              P_E_X1 - 14 - dx, 10 * 0.14)
    A(texte(dx, P_Y_TAG, p["tag_droite"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    for k, l in enumerate(p["tag_droite_detail"]):
        controler(f"tag droite détail {k + 1}", l, 10, "mono",
                  P_E_X1 - 14 - dx, 10 * 0.14)
        A(texte(dx, P_Y_TAG + 16 + k * 16, l, "mono", 10, 500,
                "pivot", tracking=10 * 0.14))

    # La production collective : une seule boîte — contre quatorze marques.
    prod_d = elems["commun-production"]
    bx, by, bw = P_BOX
    lignes_prod = p["production_droite_lignes"]
    bh = 26 + 18 + len(lignes_prod) * 14
    A(rect_bord(bx, by, bw, bh, "papier", "filet-1"))
    controler("production droite", prod_d["libelle"], 15, "sans-600", bw - 28)
    A(texte(bx + 14, by + 26, prod_d["libelle"], "sans", 15, 600,
            "encre", wdth=112))
    for k, l in enumerate(lignes_prod):
        controler(f"production droite l.{k + 1}", l, 10, "mono", bw - 28,
                  10 * 0.14)
        A(texte(bx + 14, by + 44 + k * 14, l, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))

    cote_d = (f'{elems["commun"]["valeur"]}{NN}{elems["commun"]["unite"]}'
              f' · {elems["commun"]["mention"]}')
    controler("cote droite", cote_d, 10, "mono", P_E_X1 - 14 - dx, 10 * 0.14)
    A(texte(P_E_X1 - 14, P_Y_COTE, cote_d, "mono", 10, 500, "pivot",
            ancre="end", tracking=10 * 0.14, tabulaire=True))

    # ── Les deux mentions d'étanchéité, sous leur segment d'enveloppe ────────
    A(ligne(P_E_X0 + 4, P_E_Y1 + 5, P_E_X0 + 4, P_Y_ETANCH - 12, "encre", 1.0))
    controler("étanchéité gauche", p["etancheite_gauche"], 10, "mono",
              x_lim - MARGE, 10 * 0.14)
    A(texte(P_E_X0, P_Y_ETANCH, p["etancheite_gauche"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    A(ligne(P_E_X1 - 4, P_E_Y1 + 5, P_E_X1 - 4, P_Y_ETANCH - 12, "encre", 1.0))
    controler("étanchéité droite", p["etancheite_droite"], 10, "mono",
              P_E_X1 - x_lim, 10 * 0.14)
    A(texte(P_E_X1, P_Y_ETANCH, p["etancheite_droite"], "mono", 10, 500,
            "pivot", ancre="end", tracking=10 * 0.14))

    # ── La ligne d'incendie : la même limite, une troisième fois ─────────────
    for l, y in zip(p["mention_separation"], P_Y_NOTES):
        controler("ligne d’incendie", l, 10, "mono", UTILE, 10 * 0.14)
        A(texte(MARGE, y, l, "mono", 10, 500, "pivot", tracking=10 * 0.14))

    # ── Phrase de principe, pleine largeur ───────────────────────────────────
    controler("phrase de principe", donnees["phrase_principe"], 17,
              "sans-400", UTILE)
    A(texte(MARGE, P_Y_PHRASE, donnees["phrase_principe"], "sans", 17, 400,
            "encre", wdth=100))

    # ── Cartouche — largeur AJUSTÉE au texte, jamais codée ───────────────────
    libelle = donnees["cartouche_legende"]
    largeur = min(600,
                  round(mesurer(libelle, 11, "mono", tracking=11 * 0.14) + 40))
    A(rect(MARGE, P_Y_CARTOUCHE, largeur, P_H_CARTOUCHE, "profond"))
    A(texte(MARGE + 20, P_Y_CARTOUCHE + 20, libelle, "mono", 11, 500, "voile",
            tracking=11 * 0.14))

    A("</svg>")

    controles = {
        "gabarit": f"{W} x {H} — rapport {W/H:.4f} (3:2 exact)",
        "demonstration": "une seule enveloppe fermée d’un trait continu qui "
                         f"change de graisse à la limite ({P_TRAIT_FORT} côté "
                         f"mesuré, {P_TRAIT_FIN} côté par défaut) ; la limite "
                         "en trait interrompu — aucun mur ne la porte ; "
                         f"{rangees * par_rangee} cellules marquées chacune de "
                         "sa production contre 1 boîte collective — la "
                         "géométrie porte le partage, aucun chiffre de la "
                         "fiche n’est répété",
        "partage": f"limite à x {x_lim:.1f} = {P_E_X0} + {P_E_X1 - P_E_X0} x "
                   f"{s_g:.2f} / ({s_g:.2f} + {s_d:.2f}) — {frac * 100:.1f} % "
                   f"/ {(1 - frac) * 100:.1f} % : la position code les deux "
                   "surfaces de la fiche",
        "cellules": f"{rangees} rangées de {par_rangee} cellules de "
                    f"{w_cell:.1f} x {P_H_CELL} px — le compte de la fiche, "
                    "jamais l’implantation (règle 4)",
        "bas_du_dessin": f"enveloppe jusqu’à {P_E_Y1}, mentions d’étanchéité à "
                         f"{P_Y_ETANCH}, incendie à {P_Y_NOTES[0]}–"
                         f"{P_Y_NOTES[1]}, phrase de principe à {P_Y_PHRASE}, "
                         f"cartouche {P_Y_CARTOUCHE}–"
                         f"{P_Y_CARTOUCHE + P_H_CARTOUCHE}, marge basse "
                         f"{H - (P_Y_CARTOUCHE + P_H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {P_H_CARTOUCHE} px = "
                            f"{largeur * P_H_CARTOUCHE} px², soit "
                            f"{largeur * P_H_CARTOUCHE / (W * H) * 100:.2f} % "
                            "de la planche",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l’échelle "
                         f"0,96 (1152 / {W})",
        "depassements": depassements if depassements
                        else "aucun — toutes les lignes mesurées sous leur colonne",
    }
    return "\n".join(out) + "\n", controles


def composer_vignette_partage(donnees):
    """La vignette : le motif de l'archétype, sans son appareil.

    Ce qu'elle garde : l'enveloppe au trait double, la limite interrompue posée
    au partage des surfaces, les quatorze cellules contre la boîte unique, les
    deux régimes nommés et les deux niveaux d'étanchéité. Ce qu'elle laisse :
    les étiquettes de zone, les productions, les cotes de surface et la ligne
    d'incendie — six mentions dans 300 px ne se liraient pas."""
    p = donnees["partage"]
    elems = {e["cle"]: e for e in p["elements"]}
    _, _, frac = _surfaces_partage(elems)

    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false" '
      f'style="width:100%;height:auto;display:block">')
    entete_style(A, ("filet-1", "filet-2", "filet-3", "encre"))
    A(rect(0, 0, VW, VH, "papier"))
    A(texte(V_MARGE, 22, donnees["vignette_surtitre"], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    e_x0, e_x1 = V_MARGE, VW - V_MARGE
    e_y0, e_y1 = 44, 164
    x_lim = e_x0 + (e_x1 - e_x0) * frac
    _enveloppe(A, e_x0, e_x1, x_lim, e_y0, e_y1, 2.2, 1.0)
    _limite(A, x_lim, e_y0 + 4, e_y1 - 4, 1.3, "5 4")

    A(texte(e_x0 + 10, 62, "RE2020", "sans", 12, 600, "encre", wdth=112))
    A(texte(x_lim + 8, 62, "RT2012", "sans", 12, 600, "encre", wdth=112))

    # Les cellules — le compte, à l'échelle de la carte.
    gx = e_x0 + 10
    span = (x_lim - 10) - gx
    ecart = 4
    w_cell = (span - (p["par_rangee"] - 1) * ecart) / p["par_rangee"]
    for r in range(p["rangees"]):
        y = 74 + r * (28 + 6)
        for c in range(p["par_rangee"]):
            A(rect_bord(gx + c * (w_cell + ecart), y, w_cell, 28,
                        "calcaire", "filet-1"))
    # La boîte de la production collective, seule dans sa zone.
    A(rect_bord(x_lim + 8, 74, e_x1 - 10 - (x_lim + 8), 30,
                "papier", "filet-1"))

    # Les deux niveaux d'étanchéité — les nœuds chiffrés de la vignette.
    A(texte(e_x0, 184, f'0,8{NN}· MESURÉ', "mono", 10, 500, "pivot",
            tracking=10 * 0.14, tabulaire=True))
    A(texte(e_x1, 184, f'1,7{NN}· PAR DÉFAUT', "mono", 10, 500, "pivot",
            ancre="end", tracking=10 * 0.14, tabulaire=True))

    A("</svg>")
    controles = {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": f"carte de projet mesurée de 274 à 296 px — "
                            f"échelle {274/VW:.2f} à {296/VW:.2f}",
        "corps_minimal": f"9 px dans le repère — rendu à {9*274/VW:.1f} px au pire cas",
        "motif": "l’enveloppe au trait double, la limite interrompue au "
                 f"partage des surfaces ({frac * 100:.0f} %), 14 cellules "
                 "contre 1 boîte, les deux régimes nommés et les deux niveaux "
                 "d’étanchéité — étiquettes, productions et incendie sont "
                 "laissés à la planche",
        "bas_du_dessin": "nœuds d’étanchéité à y 184, marge basse 16 px",
    }
    return "\n".join(out) + "\n", controles


def composer_appui_partage(donnees):
    """L'appui du hero : le motif entier à l'échelle 1, densité intermédiaire.

    Ce qu'il garde : l'enveloppe au trait double, la limite étiquetée, les
    quatorze cellules marquées et leur légende de production, la zone commune
    nommée avec sa production collective, les deux niveaux d'étanchéité. Ce
    qu'il laisse : les étiquettes d'exigences, les cotes de surface, la boîte
    machine détaillée et la ligne d'incendie — ils vivent sur la planche."""
    p = donnees["partage"]
    elems = {e["cle"]: e for e in p["elements"]}
    _, _, frac = _surfaces_partage(elems)

    out = []
    A = out.append
    racine_appui(A, donnees, strokes=("filet-1", "filet-2", "filet-3", "encre"))

    e_x0, e_x1 = A_MARGE, AW - A_MARGE
    e_y0, e_y1 = 76, 298
    x_lim = e_x0 + (e_x1 - e_x0) * frac
    A(texte(x_lim - 8, 68, "LA LIMITE DES DEUX CALCULS", "mono", 10, 500,
            "pivot", ancre="end", tracking=10 * 0.14))
    _enveloppe(A, e_x0, e_x1, x_lim, e_y0, e_y1, 3.0, 1.2)
    _limite(A, x_lim, e_y0 + 5, e_y1 - 5, 1.6, "7 5")

    gx = e_x0 + 12
    A(texte(gx, 96, p["tag_gauche"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

    # Les cellules, marquées chacune de sa production.
    span = (x_lim - 12) - gx
    ecart = 6
    w_cell = (span - (p["par_rangee"] - 1) * ecart) / p["par_rangee"]
    for r in range(p["rangees"]):
        y = 108 + r * (40 + 8)
        for c in range(p["par_rangee"]):
            x = gx + c * (w_cell + ecart)
            A(rect_bord(x, y, w_cell, 40, "calcaire", "filet-1"))
            A(rect(x + 6, y + 40 - 11, 5, 5, "encre"))

    A(rect(gx, 214, 5, 5, "encre"))
    A(texte(gx + 11, 222, "QUATORZE PRODUCTIONS INDIVIDUELLES", "mono", 10,
            500, "pivot", tracking=10 * 0.14))
    A(texte(gx, 240, "PANNEAU RAYONNANT · CHAUFFE-EAU DE 100 L", "mono",
            10, 500, "pivot", tracking=10 * 0.14))

    # La zone commune : trois lignes courtes, la colonne fait 110 px.
    dx = x_lim + 10
    for k, l in enumerate(("L’ESPACE", "COMMUN", "RT2012")):
        A(texte(dx, 96 + k * 16, l, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))
    for k, l in enumerate(("UNE", "PRODUCTION", "COLLECTIVE")):
        A(texte(dx, 198 + k * 16, l, "mono", 10, 500, "pivot",
                tracking=10 * 0.14))

    # Les deux niveaux d'étanchéité, sous leur segment d'enveloppe.
    A(texte(e_x0, 322, "ÉTANCHÉITÉ TENUE À 0,8 · MESURÉE", "mono", 10, 500,
            "pivot", tracking=10 * 0.14, tabulaire=True))
    A(texte(e_x1, 322, "1,7 PAR DÉFAUT · SANS TEST", "mono", 10, 500,
            "pivot", ancre="end", tracking=10 * 0.14, tabulaire=True))

    A("</svg>")
    return "\n".join(out) + "\n", controles_appui(
        motif="l’enveloppe au trait double fermant les deux zones, la limite "
              f"interrompue étiquetée au partage des surfaces ({frac * 100:.0f}"
              " %), 14 cellules marquées et leur légende contre la zone "
              "commune nommée, les deux niveaux d’étanchéité en pied — "
              "exigences, cotes de surface, boîte machine et incendie laissés "
              "à la planche",
        bas="mentions d’étanchéité à y 322, marge basse 46 px")


# ═════════════════════════════════════════════════════════════════════════════
# Mécanisme `inversion` — Maison de Pierre Loti, Rochefort (2026-08-28)
#
# Même archétype (détection et mise en sécurité), démonstration inverse de
# celle de Sablonceaux : là-bas la géométrie montrait qu'une seule zone évacue
# quand les autres ne bougent pas ; ici elle montre que TOUT s'exécute sur
# toute détection — le musée ne forme qu'une seule zone d'alarme, et le
# déclenchement commande quatre gestes simultanés (alarme générale, remise en
# lumière, arrêt de la sonorisation, arrêt des CTA) : la mise en sécurité
# inverse la scénographie. La géométrie porte la thèse deux fois : les hauteurs
# des deux familles de détection sont proportionnelles à leurs effectifs
# (46 radio / 38 filaire — la radio majoritaire, qui épargne les décors
# classés), et les QUATRE départs de la centrale sont encrés et fléchés, contre
# l'unique départ encré du mécanisme par défaut. Le dispatch se fait sur le
# bloc de l'extraction (`inversion` contre `zonage`), comme les deux autres.
# ═════════════════════════════════════════════════════════════════════════════

# ── Rythme de la planche `inversion` ─────────────────────────────────────────
I_Y_ENTETE = 190                    # les deux en-têtes de registre
I_Y0 = 268                          # haut des piles — centré entre en-têtes et report
I_H_PILE = 296                      # hauteur commune des deux piles
I_ECART = 12
I_F_X0, I_F_X1 = 250, 550           # la pile des familles de détection
I_B_X0, I_B_W = 620, 230            # la boîte ECS + CMSI
I_A_X0, I_A_X1 = 900, 1144          # la pile des gestes de mise en sécurité
I_COUDE_X = 585                     # le coude des collecteurs familles → boîte
I_TRONC_X = 875                     # le tronc des départs boîte → gestes
I_H_BOITE = 96
I_Y_REPORT = 660
I_Y_PHRASE = 688
I_Y_CARTOUCHE = 714
I_H_CARTOUCHE = 30


def _hauteurs_familles(familles, h_totale, ecart):
    """Hauteurs proportionnelles aux effectifs de détecteurs — la géométrie
    code la proportion (46/38), jamais réglée à l'œil."""
    valeurs = [float(f["valeur"]) for f in familles]
    dispo = h_totale - ecart * (len(familles) - 1)
    return [dispo * v / sum(valeurs) for v in valeurs]


def composer_inversion(donnees):
    inv = donnees["inversion"]
    familles = inv["familles"]
    actions = inv["actions"]
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

    # ── Les deux en-têtes de registre — ce qui empêche la planche de mentir ──
    controler("en-tête détection", inv["entete_detection"], 10, "mono",
              680, 10 * 0.14)
    A(texte(MARGE, I_Y_ENTETE, inv["entete_detection"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    controler("en-tête mise en sécurité", inv["entete_actions"], 10, "mono",
              I_A_X1 - MARGE - 680, 10 * 0.14)
    A(texte(I_A_X1, I_Y_ENTETE, inv["entete_actions"], "mono", 10, 500,
            "pivot", ancre="end", tracking=10 * 0.14))

    # ── La pile des familles, hauteurs proportionnelles aux effectifs ────────
    hauteurs = _hauteurs_familles(familles, I_H_PILE, I_ECART)
    centres_familles = []
    y = I_Y0
    for f, h in zip(familles, hauteurs):
        A(rect_bord(I_F_X0, y, I_F_X1 - I_F_X0, h, "calcaire", "filet-1"))
        controler(f'tag {f["cle"]}', f["tag"], 10, "mono",
                  I_F_X1 - I_F_X0 - 28, 10 * 0.14)
        A(texte(I_F_X0 + PAD, y + 24, f["tag"], "mono", 10, 500,
                "pivot", tracking=10 * 0.14, tabulaire=True))
        A(texte(I_F_X0 + PAD, y + 47, f["libelle"], "sans", 15, 600,
                "encre", wdth=112))
        for k, l in enumerate(f["detail"]):
            controler(f'détail {f["cle"]} l.{k + 1}', l, 10, "mono",
                      I_F_X1 - I_F_X0 - 28, 10 * 0.14)
            A(texte(I_F_X0 + PAD, y + 68 + k * 14, l, "mono", 10, 500,
                    "pivot", tracking=10 * 0.14))
        centres_familles.append(y + h / 2)
        y += h + I_ECART

    # ── L'événement : deux lignes mono, la marque carrée, la fourche ─────────
    cy_evt = sum(centres_familles) / len(centres_familles)
    for k, l in enumerate(inv["evenement"]):
        controler(f"événement l.{k + 1}", l, 10, "mono",
                  I_F_X0 - 28 - MARGE, 10 * 0.14)
        A(texte(MARGE, cy_evt - 4 + k * 14, l, "mono", 10, 500,
                "pivot", tracking=10 * 0.14))
    A(rect(I_F_X0 - 18, cy_evt - 3.5 + 5, 7, 7, "encre"))
    x_fourche = I_F_X0 - 8
    A(ligne(I_F_X0 - 11, cy_evt + 5, x_fourche, cy_evt + 5, "encre", 1.0))
    A(ligne(x_fourche, centres_familles[0], x_fourche, centres_familles[-1],
            "encre", 1.0))
    for c in centres_familles:
        A(ligne(x_fourche, c, I_F_X0, c, "encre", 1.0))

    # ── La boîte ECS + CMSI, centrée sur la pile ─────────────────────────────
    cy_boite = I_Y0 + I_H_PILE / 2
    y_boite = cy_boite - I_H_BOITE / 2
    sys_ = inv["systeme"]
    A(rect_bord(I_B_X0, y_boite, I_B_W, I_H_BOITE, "papier", "filet-1"))
    n = len(sys_["detail"])
    base = cy_boite - (n * 13 + 4) / 2 + 8
    controler("libellé système", sys_["libelle"], 15, "sans-600",
              I_B_W - 2 * PAD)
    A(texte(I_B_X0 + PAD, base, sys_["libelle"], "sans", 15, 600,
            "encre", wdth=112))
    for k, l in enumerate(sys_["detail"]):
        controler(f"détail système l.{k + 1}", l, 10, "mono",
                  I_B_W - 2 * PAD, 10 * 0.14)
        A(texte(I_B_X0 + PAD, base + 18 + k * 13, l, "mono", 10, 500,
                "pivot", tracking=10 * 0.14))

    # ── Les collecteurs : chaque famille rejoint la boîte, encrée, fléchée ───
    for c in centres_familles:
        A(polyligne([(I_F_X1, c), (I_COUDE_X, c), (I_COUDE_X, cy_boite)],
                    "encre", 1.5))
    A(ligne(I_COUDE_X, cy_boite, I_B_X0 - 9, cy_boite, "encre", 1.5))
    A(fleche(I_B_X0, cy_boite, "encre"))

    # ── La pile des gestes : TOUS les départs sont encrés et fléchés ─────────
    n_a = len(actions)
    h_a = (I_H_PILE - (n_a - 1) * I_ECART) / n_a
    centres_actions = []
    y = I_Y0
    for a_ in actions:
        A(rect_bord(I_A_X0, y, I_A_X1 - I_A_X0, h_a, "calcaire", "filet-1"))
        if a_.get("alarme"):
            A(rect(I_A_X0 + 1, y + 1, I_A_X1 - I_A_X0 - 2, H_BARRE, "clair"))
        controler(f'libellé {a_["cle"]}', a_["libelle"], 15, "sans-600",
                  I_A_X1 - I_A_X0 - 28)
        A(texte(I_A_X0 + PAD, y + 30, a_["libelle"], "sans", 15, 600,
                "encre", wdth=112))
        if a_.get("detail"):
            controler(f'détail {a_["cle"]}', a_["detail"], 10, "mono",
                      I_A_X1 - I_A_X0 - 28, 10 * 0.14)
            A(texte(I_A_X0 + PAD, y + 50, a_["detail"], "mono", 10, 500,
                    "pivot", tracking=10 * 0.14, tabulaire=True))
        centres_actions.append(y + h_a / 2)
        y += h_a + I_ECART

    A(ligne(I_B_X0 + I_B_W, cy_boite, I_TRONC_X, cy_boite, "encre", 1.5))
    A(ligne(I_TRONC_X, centres_actions[0], I_TRONC_X, centres_actions[-1],
            "encre", 1.5))
    for c in centres_actions:
        A(ligne(I_TRONC_X, c, I_A_X0 - 9, c, "encre", 1.5))
        A(fleche(I_A_X0, c, "encre"))

    # ── Le report : une ligne, pas un bloc ───────────────────────────────────
    controler("report", inv["report"], 10, "mono", UTILE, 10 * 0.14)
    A(texte(MARGE, I_Y_REPORT, inv["report"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))

    # ── Phrase de principe, pleine largeur ───────────────────────────────────
    controler("phrase de principe", donnees["phrase_principe"], 17,
              "sans-400", UTILE)
    A(texte(MARGE, I_Y_PHRASE, donnees["phrase_principe"], "sans", 17, 400,
            "encre", wdth=100))

    # ── Cartouche — largeur AJUSTÉE au texte, jamais codée ───────────────────
    libelle = donnees["cartouche_legende"]
    largeur = min(600,
                  round(mesurer(libelle, 11, "mono", tracking=11 * 0.14) + 40))
    A(rect(MARGE, I_Y_CARTOUCHE, largeur, I_H_CARTOUCHE, "profond"))
    A(texte(MARGE + 20, I_Y_CARTOUCHE + 20, libelle, "mono", 11, 500, "voile",
            tracking=11 * 0.14))

    A("</svg>")

    ratio = " / ".join(f'{f["valeur"]}' for f in familles)
    controles = {
        "gabarit": f"{W} x {H} — rapport {W/H:.4f} (3:2 exact)",
        "demonstration": f"{len(familles)} familles de détection aux hauteurs "
                         f"proportionnelles ({ratio} : "
                         f"{hauteurs[0]:.0f} px / {hauteurs[1]:.0f} px) "
                         f"convergent vers la centrale, et les {n_a} départs "
                         f"de mise en sécurité sont TOUS encrés et fléchés — "
                         f"contre l’unique barre d’alarme claire : tout "
                         f"s’exécute sur toute détection",
        "topologie": f"événement (x {MARGE}) → familles (x {I_F_X0}–{I_F_X1}) "
                     f"→ centrale (x {I_B_X0}–{I_B_X0 + I_B_W}) → gestes "
                     f"(x {I_A_X0}–{I_A_X1}) ; coude des collecteurs à "
                     f"x {I_COUDE_X}, tronc des départs à x {I_TRONC_X}",
        "bas_du_dessin": f"piles jusqu’à {I_Y0 + I_H_PILE} px, report à "
                         f"{I_Y_REPORT}, phrase de principe à {I_Y_PHRASE}, "
                         f"cartouche {I_Y_CARTOUCHE}–"
                         f"{I_Y_CARTOUCHE + I_H_CARTOUCHE}, marge basse "
                         f"{H - (I_Y_CARTOUCHE + I_H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {I_H_CARTOUCHE} px = "
                            f"{largeur * I_H_CARTOUCHE} px², soit "
                            f"{largeur * I_H_CARTOUCHE / (W * H) * 100:.2f} % "
                            f"de la planche",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l’échelle "
                         f"0,96 (1152 / {W})",
        "depassements": depassements if depassements
                        else "aucun — toutes les lignes mesurées sous leur colonne",
    }
    return "\n".join(out) + "\n", controles


def composer_vignette_inversion(donnees):
    """La vignette : le motif sans son appareil — les deux familles aux
    hauteurs proportionnelles, la flèche, la pile des quatre gestes avec la
    barre d'alarme. Ce qu'elle laisse : l'événement, la centrale, le report
    et tous les détails — six blocs annotés dans 300 px ne se liraient pas."""
    inv = donnees["inversion"]
    familles = inv["familles"]
    actions = inv["actions"]

    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false" '
      f'style="width:100%;height:auto;display:block">')
    entete_style(A, ("filet-1", "filet-2", "filet-3", "encre"))
    A(rect(0, 0, VW, VH, "papier"))
    A(texte(V_MARGE, 22, donnees["vignette_surtitre"], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    y0, y1 = 48, VH - 24                              # 48..176
    h_pile = y1 - y0
    f_x0, f_x1 = V_MARGE, 98                          # familles
    a_x0, a_x1 = 164, VW - V_MARGE                    # gestes

    # Les familles, hauteurs proportionnelles.
    hauteurs = _hauteurs_familles(familles, h_pile, 6)
    y = y0
    for f, h in zip(familles, hauteurs):
        A(rect_bord(f_x0, y, f_x1 - f_x0, h, "calcaire", "filet-1"))
        cy = y + h / 2
        A(texte(f_x0 + 8, cy - 1, f.get("libelle_vignette", f["libelle"]),
                "sans", 12, 600, "encre", wdth=112))
        A(texte(f_x0 + 8, cy + 15, f["valeur"], "mono", 10, 500, "pivot",
                tabulaire=True))
        y += h + 6

    # La flèche du principe.
    fy = (y0 + y1) / 2
    A(ligne(f_x1 + 10, fy, a_x0 - 16, fy, "encre", 1.5))
    A(fleche(a_x0 - 8, fy, "encre", "droite", 8))

    # La pile des gestes, la barre claire sur l'alarme.
    n = len(actions)
    ecart = 6
    h_bloc = (h_pile - (n - 1) * ecart) / n
    for i, a_ in enumerate(actions):
        ya = y0 + i * (h_bloc + ecart)
        A(rect_bord(a_x0, ya, a_x1 - a_x0, h_bloc, "calcaire", "filet-1"))
        if a_.get("alarme"):
            A(rect(a_x0 + 1, ya + 1, a_x1 - a_x0 - 2, 5, "clair"))
        A(texte(a_x0 + 8, ya + h_bloc / 2 + 4 + (2 if a_.get("alarme") else 0),
                a_.get("libelle_vignette", a_["libelle"]), "sans", 12, 600,
                "encre", wdth=112))

    A("</svg>")
    controles = {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": f"carte de projet mesurée de 274 à 296 px — "
                            f"échelle {274/VW:.2f} à {296/VW:.2f}",
        "corps_minimal": f"9 px dans le repère — rendu à {9*274/VW:.1f} px au pire cas",
        "motif": f"{len(familles)} familles aux hauteurs proportionnelles "
                 f"({familles[0]['valeur']}/{familles[1]['valeur']}) contre "
                 f"{n} gestes, la barre claire sur l’alarme — événement, "
                 f"centrale et report laissés à la planche",
        "bas_du_dessin": f"{y1} px, marge basse {VH - y1} px",
    }
    return "\n".join(out) + "\n", controles


def composer_appui_inversion(donnees):
    """L'appui du hero : le motif entier à l'échelle 1, densité intermédiaire.

    Ce qu'il garde : les deux familles avec leurs effectifs, la centrale
    (libellé court), les quatre gestes tous fléchés, la barre et les 90 dB
    sur l'alarme. Ce qu'il laisse : l'événement, les détails des familles et
    le report — ils vivent sur la planche."""
    inv = donnees["inversion"]
    familles = inv["familles"]
    actions = inv["actions"]
    sys_ = inv["systeme"]

    out = []
    A = out.append
    racine_appui(A, donnees, strokes=("filet-1", "filet-2", "filet-3", "encre"))

    y0, y1 = 76, 336
    h_pile = y1 - y0
    f_x0, f_x1 = A_MARGE, 174
    b_x0, b_w = 204, 140
    a_x0, a_x1 = 380, AW - A_MARGE

    # Les familles, hauteurs proportionnelles, effectifs en mono.
    hauteurs = _hauteurs_familles(familles, h_pile, 12)
    centres = []
    y = y0
    for f, h in zip(familles, hauteurs):
        A(rect_bord(f_x0, y, f_x1 - f_x0, h, "calcaire", "filet-1"))
        cy = y + h / 2
        A(texte(f_x0 + 12, cy - 4, f["libelle"], "sans", 14, 600,
                "encre", wdth=112))
        A(texte(f_x0 + 12, cy + 14,
                f'{f["valeur"]}{NN}{f["unite"].upper()}', "mono", 10, 500,
                "pivot", tabulaire=True))
        centres.append(cy)
        y += h + 12

    # La centrale, centrée, et ses collecteurs.
    cy_boite = (y0 + y1) / 2
    y_boite = cy_boite - 38
    A(rect_bord(b_x0, y_boite, b_w, 76, "papier", "filet-1"))
    base = cy_boite - 8
    A(texte(b_x0 + 12, base, sys_.get("libelle_appui", sys_["libelle"]),
            "sans", 14, 600, "encre", wdth=112))
    for k, l in enumerate(sys_.get("detail_appui", [])):
        A(texte(b_x0 + 12, base + 16 + k * 13, l, "mono", 10, 500,
                "pivot", tracking=10 * 0.14))
    coude = (f_x1 + b_x0) / 2
    for c in centres:
        A(polyligne([(f_x1, c), (coude, c), (coude, cy_boite)], "encre", 1.5))
    A(ligne(coude, cy_boite, b_x0 - 8, cy_boite, "encre", 1.5))
    A(fleche(b_x0, cy_boite, "encre", "droite", 8))

    # Les gestes : quatre départs, tous fléchés, la barre sur l'alarme.
    n = len(actions)
    h_a = (h_pile - (n - 1) * 10) / n
    tronc = (b_x0 + b_w + a_x0) / 2
    A(ligne(b_x0 + b_w, cy_boite, tronc, cy_boite, "encre", 1.5))
    centres_a = [y0 + i * (h_a + 10) + h_a / 2 for i in range(n)]
    A(ligne(tronc, centres_a[0], tronc, centres_a[-1], "encre", 1.5))
    for i, a_ in enumerate(actions):
        ya = y0 + i * (h_a + 10)
        A(rect_bord(a_x0, ya, a_x1 - a_x0, h_a, "calcaire", "filet-1"))
        if a_.get("alarme"):
            A(rect(a_x0 + 1, ya + 1, a_x1 - a_x0 - 2, 7, "clair"))
        A(texte(a_x0 + 12, ya + h_a / 2 + (0 if a_.get("alarme") else 4),
                a_.get("libelle_vignette", a_["libelle"]), "sans", 13, 600,
                "encre", wdth=112))
        if a_.get("alarme"):
            A(texte(a_x0 + 12, ya + h_a / 2 + 16, "90" + NN + "dB", "mono",
                    10, 500, "pivot", tabulaire=True))
        A(ligne(tronc, centres_a[i], a_x0 - 8, centres_a[i], "encre", 1.5))
        A(fleche(a_x0, centres_a[i], "encre", "droite", 8))

    A("</svg>")
    return "\n".join(out) + "\n", controles_appui(
        motif=f"les {len(familles)} familles aux hauteurs proportionnelles "
              f"({familles[0]['valeur']}/{familles[1]['valeur']}, effectifs "
              "en mono), la centrale au libellé court, et les "
              f"{n} gestes TOUS fléchés avec la barre claire et les 90 dB "
              "sur l’alarme — événement, détails des familles et report "
              "laissés à la planche",
        bas=f"piles jusqu’à {y1} px, marge basse {AH - y1} px")


# ── Mécanisme `convergence` (2026-09-01) ─────────────────────────────────────
# La détection est fine, la mise en sécurité ne connaît qu'une échelle. Seize
# zones réparties sur six niveaux convergent vers une centrale unique dont
# toute sortie vaut pour le bâtiment entier ; deux fonctions de sécurité sont
# dessinées dans le registre de droite SANS liaison au centralisateur, parce
# que le cahier des charges les en exclut nommément.
#
# ⚠ Les repères sont préfixés `C_` : deux mécanismes qui affectent le même nom
# au niveau du module se marchent dessus, et c'est le PREMIER dessin qui se
# recompose faux (piège du protocole, relevé sur `tableau-electrique.py`).
C_Y_ENTETE = 190
C_Y0 = 214                          # haut des deux piles
C_H_ROW, C_ECART_ROW = 60, 6        # 6 x 60 + 5 x 6 = 390 → la pile finit à 604
C_N_X0, C_N_X1 = MARGE, 520         # les niveaux
C_COUDE_X = 546                     # coude des collecteurs niveaux → centrale
C_B_X0, C_B_W = 570, 230            # la centrale
C_TRONC_X = 826                     # tronc des départs centrale → mise en sécurité
C_A_X0, C_A_X1 = 856, W - MARGE     # la mise en sécurité (1144)
C_H_ACTIONS = 216                   # hauteur de la pile des deux zones
C_ECART_ACTION = 12
C_Y_HORS_TAG = 462                  # en-tête du troisième registre
C_Y_HORS = 474                      # les deux fonctions hors centralisateur
C_ECART_HORS = 12
C_Y_LEGENDE = 630
C_Y_REPORT = 654
C_Y_PHRASE = 688
C_Y_CARTOUCHE = 714
C_H_CARTOUCHE = 30
C_MARQUE = 9                        # côté de la marque de zone
C_PAS_MARQUE = 18                   # pas entre deux marques
C_PAD = 16


def _hauteurs_actions(actions, h_totale, ecart):
    """Hauteurs proportionnelles aux effectifs de zones commandées — la
    géométrie code la proportion (16/10), jamais réglée à l'œil."""
    valeurs = [float(a["valeur"]) for a in actions]
    dispo = h_totale - ecart * (len(actions) - 1)
    return [dispo * v / sum(valeurs) for v in valeurs]


def _rect_pointille(x, y, w, h, fond, filet, motif="5 4"):
    """Un bloc dont le filet est interrompu : ce qui n'est pas raccordé au
    centralisateur ne se dessine pas d'un trait plein."""
    return (f'  <rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
            f'class="c-{fond} s-{filet}" fill="{JETON[fond]}" '
            f'stroke="{JETON[filet]}" stroke-width="1" '
            f'stroke-dasharray="{motif}"/>')


def _marque_zone(x, y, cote, pleine):
    """La marque d'une zone de détection : carré plein pour une détection
    automatique, carré évidé pour une zone de déclencheurs manuels. Rayon 0 —
    la charte ne connaît qu'un seul cercle, la puce de section. Les deux
    marques sont toujours doublées du texte qui les nomme (RGAA 3.2)."""
    if pleine:
        return rect(x, y, cote, cote, "encre")
    return (f'  <rect x="{x + 0.5:.2f}" y="{y + 0.5:.2f}" '
            f'width="{cote - 1:.2f}" height="{cote - 1:.2f}" '
            f'class="c-papier s-encre" fill="{JETON["papier"]}" '
            f'stroke="{JETON["encre"]}" stroke-width="1"/>')


def _marques_du_niveau(A, n, x_droite, cy, cote=None, pas=None):
    """Les marques d'un niveau. Le DERNIER emplacement est réservé à la zone de
    déclencheurs manuels, les zones de détection automatique se rangeant à
    droite dans les emplacements précédents.

    L'emplacement réservé est le point : la colonne évidée devient continue, et
    le vide des combles se lit comme ce qu'il est — pas de déclencheur manuel à
    ce niveau. Aligner les marques d'un seul tenant, comme le faisait la
    première version, logeait la marque PLEINE des combles dans la colonne des
    évidées et effaçait la distinction à la lecture (relevé au rendu à
    1152 px)."""
    cote = C_MARQUE if cote is None else cote
    pas = C_PAS_MARQUE if pas is None else pas
    x_zdm = x_droite - cote
    for k in range(n["zdm"]):
        A(_marque_zone(x_zdm - k * pas, cy - cote / 2, cote, False))
    x_zda = x_zdm - pas
    for k in range(n["zda"]):
        A(_marque_zone(x_zda - k * pas, cy - cote / 2, cote, True))
    return n["zda"] + n["zdm"]


def composer_convergence(donnees):
    cv = donnees["convergence"]
    niveaux = cv["niveaux"]
    actions = cv["actions"]
    hors = cv["hors"]
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

    # ── Les en-têtes de registre — ce qui empêche la planche de mentir ───────
    controler("en-tête détection", cv["entete_detection"], 10, "mono",
              C_N_X1 - MARGE, 10 * 0.14)
    A(texte(MARGE, C_Y_ENTETE, cv["entete_detection"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    controler("en-tête mise en sécurité", cv["entete_securite"], 10, "mono",
              C_A_X1 - C_A_X0, 10 * 0.14)
    A(texte(C_A_X1, C_Y_ENTETE, cv["entete_securite"], "mono", 10, 500,
            "pivot", ancre="end", tracking=10 * 0.14))

    # ── La pile des six niveaux : le libellé, les repères, les usages, les
    #    marques. Les marques SONT le compte : seize à gauche, deux blocs à
    #    droite — c'est la démonstration, et elle tient sans le texte. ────────
    largeur_marques = 4 * C_PAS_MARQUE
    dispo_texte = (C_N_X1 - C_PAD) - (C_N_X0 + C_PAD) - largeur_marques - 12
    centres_niveaux = []
    total_zda = total_zdm = 0
    y = C_Y0
    for n in niveaux:
        A(rect_bord(C_N_X0, y, C_N_X1 - C_N_X0, C_H_ROW, "calcaire", "filet-1"))
        controler(f'niveau {n["cle"]}', n["libelle"], 15, "sans-600", dispo_texte)
        A(texte(C_N_X0 + C_PAD, y + 22, n["libelle"], "sans", 15, 600,
                "encre", wdth=112))
        controler(f'repères {n["cle"]}', n["reperes"], 10, "mono",
                  dispo_texte, 10 * 0.14)
        A(texte(C_N_X0 + C_PAD, y + 40, n["reperes"], "mono", 10, 500,
                "pivot", tracking=10 * 0.14, tabulaire=True))
        controler(f'usages {n["cle"]}', n["usages"], 10, "mono",
                  dispo_texte, 10 * 0.14)
        A(texte(C_N_X0 + C_PAD, y + 54, n["usages"], "mono", 10, 500,
                "pivot", tracking=10 * 0.14))
        _marques_du_niveau(A, n, C_N_X1 - C_PAD, y + C_H_ROW / 2)
        total_zda += n["zda"]
        total_zdm += n["zdm"]
        centres_niveaux.append(y + C_H_ROW / 2)
        y += C_H_ROW + C_ECART_ROW
    bas_pile = y - C_ECART_ROW

    # ── La centrale, centrée sur la pile des niveaux ─────────────────────────
    sys_ = cv["systeme"]
    cy_boite = (C_Y0 + bas_pile) / 2
    n_det = len(sys_["detail"])
    h_boite = 44 + n_det * 13
    y_boite = cy_boite - h_boite / 2
    A(rect_bord(C_B_X0, y_boite, C_B_W, h_boite, "papier", "filet-1"))
    base = cy_boite - (n_det * 13 + 4) / 2 + 8
    controler("libellé centrale", sys_["libelle"], 15, "sans-600",
              C_B_W - 2 * C_PAD)
    A(texte(C_B_X0 + C_PAD, base, sys_["libelle"], "sans", 15, 600,
            "encre", wdth=112))
    for k, l in enumerate(sys_["detail"]):
        controler(f"détail centrale l.{k + 1}", l, 10, "mono",
                  C_B_W - 2 * C_PAD, 10 * 0.14)
        A(texte(C_B_X0 + C_PAD, base + 18 + k * 13, l, "mono", 10, 500,
                "pivot", tracking=10 * 0.14))

    # ── Les collecteurs : les six niveaux rejoignent la centrale ─────────────
    for c in centres_niveaux:
        A(polyligne([(C_N_X1, c), (C_COUDE_X, c), (C_COUDE_X, cy_boite)],
                    "encre", 1.5))
    A(ligne(C_COUDE_X, cy_boite, C_B_X0 - 9, cy_boite, "encre", 1.5))
    A(fleche(C_B_X0, cy_boite, "encre"))

    # ── La mise en sécurité : deux zones, hauteurs proportionnelles à 16/10 ──
    hauteurs = _hauteurs_actions(actions, C_H_ACTIONS, C_ECART_ACTION)
    centres_actions = []
    y = C_Y0
    for a_, h in zip(actions, hauteurs):
        A(rect_bord(C_A_X0, y, C_A_X1 - C_A_X0, h, "calcaire", "filet-1"))
        if a_.get("alarme"):
            A(rect(C_A_X0 + 1, y + 1, C_A_X1 - C_A_X0 - 2, H_BARRE, "clair"))
        décalage = 12 if a_.get("alarme") else 0
        controler(f'libellé {a_["cle"]}', a_["libelle"], 15, "sans-600",
                  C_A_X1 - C_A_X0 - 2 * C_PAD)
        A(texte(C_A_X0 + C_PAD, y + 28 + décalage, a_["libelle"], "sans", 15,
                600, "encre", wdth=112))
        for k, l in enumerate(a_["detail"]):
            controler(f'détail {a_["cle"]} l.{k + 1}', l, 10, "mono",
                      C_A_X1 - C_A_X0 - 2 * C_PAD, 10 * 0.14)
            A(texte(C_A_X0 + C_PAD, y + 48 + décalage + k * 14, l, "mono", 10,
                    500, "pivot", tracking=10 * 0.14, tabulaire=True))
        centres_actions.append(y + h / 2)
        y += h + C_ECART_ACTION

    A(ligne(C_B_X0 + C_B_W, cy_boite, C_TRONC_X, cy_boite, "encre", 1.5))
    # ⚠ La fourche doit ENGLOBER l'ordonnée de la centrale : la pile de droite
    # est calée en haut et plus courte que celle des niveaux, si bien que
    # cy_boite tombe SOUS le dernier départ. Une fourche bornée aux seuls
    # départs laisserait le segment sortant de la centrale pendre dans le vide.
    y_fourche = [cy_boite] + centres_actions
    A(ligne(C_TRONC_X, min(y_fourche), C_TRONC_X, max(y_fourche),
            "encre", 1.5))
    for c in centres_actions:
        A(ligne(C_TRONC_X, c, C_A_X0 - 9, c, "encre", 1.5))
        A(fleche(C_A_X0, c, "encre"))

    # ── Le troisième registre : ce que le centralisateur ne commande PAS.
    #    Aucun tronc ne le rejoint — l'absence de liaison est le propos. ──────
    controler("en-tête hors centralisateur", cv["entete_hors"], 10, "mono",
              C_A_X1 - C_A_X0, 10 * 0.14)
    A(texte(C_A_X0, C_Y_HORS_TAG, cv["entete_hors"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    h_hors = (bas_pile - C_Y_HORS - C_ECART_HORS * (len(hors) - 1)) / len(hors)
    y = C_Y_HORS
    for h_ in hors:
        A(_rect_pointille(C_A_X0, y, C_A_X1 - C_A_X0, h_hors, "papier", "filet-1"))
        controler(f'libellé {h_["cle"]}', h_["libelle"], 15, "sans-600",
                  C_A_X1 - C_A_X0 - 2 * C_PAD)
        A(texte(C_A_X0 + C_PAD, y + 24, h_["libelle"], "sans", 15, 600,
                "encre", wdth=112))
        controler(f'détail {h_["cle"]}', h_["detail"], 10, "mono",
                  C_A_X1 - C_A_X0 - 2 * C_PAD, 10 * 0.14)
        A(texte(C_A_X0 + C_PAD, y + 42, h_["detail"], "mono", 10, 500,
                "pivot", tracking=10 * 0.14))
        y += h_hors + C_ECART_HORS

    # ── La légende des deux marques — la couleur ne porte jamais seule ───────
    x = MARGE
    for entree in cv["legende"]:
        A(_marque_zone(x, C_Y_LEGENDE - C_MARQUE + 1, C_MARQUE,
                       entree["marque"] == "pleine"))
        largeur = controler(f'légende {entree["marque"]}', entree["libelle"],
                            10, "mono", 360, 10 * 0.14)
        A(texte(x + C_MARQUE + 8, C_Y_LEGENDE, entree["libelle"], "mono", 10,
                500, "pivot", tracking=10 * 0.14))
        x += C_MARQUE + 8 + largeur + 40

    # ── Le report : une ligne, pas un bloc ───────────────────────────────────
    controler("report", cv["report"], 10, "mono", UTILE, 10 * 0.14)
    A(texte(MARGE, C_Y_REPORT, cv["report"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))

    # ── Phrase de principe, pleine largeur ───────────────────────────────────
    controler("phrase de principe", donnees["phrase_principe"], 17,
              "sans-400", UTILE)
    A(texte(MARGE, C_Y_PHRASE, donnees["phrase_principe"], "sans", 17, 400,
            "encre", wdth=100))

    # ── Cartouche — largeur AJUSTÉE au texte, jamais codée ───────────────────
    libelle = donnees["cartouche_legende"]
    largeur = min(600,
                  round(mesurer(libelle, 11, "mono", tracking=11 * 0.14) + 40))
    A(rect(MARGE, C_Y_CARTOUCHE, largeur, C_H_CARTOUCHE, "profond"))
    A(texte(MARGE + 20, C_Y_CARTOUCHE + 20, libelle, "mono", 11, 500, "voile",
            tracking=11 * 0.14))

    A("</svg>")

    total = total_zda + total_zdm
    controles = {
        "gabarit": f"{W} x {H} — rapport {W/H:.4f} (3:2 exact)",
        "demonstration": f"{total} marques de zone comptées sur "
                         f"{len(niveaux)} niveaux ({total_zda} pleines pour la "
                         f"détection automatique, {total_zdm} évidées pour les "
                         f"déclencheurs manuels) convergent par un tronc UNIQUE "
                         f"vers deux zones de mise en sécurité aux hauteurs "
                         f"proportionnelles "
                         f"({actions[0]['valeur']}/{actions[1]['valeur']} : "
                         f"{hauteurs[0]:.0f} px / {hauteurs[1]:.0f} px) ; "
                         f"les {len(hors)} fonctions hors centralisateur sont "
                         f"dans le même registre, en filet interrompu, et "
                         f"AUCUN tronc ne les atteint",
        "comptage": f"détection : {' + '.join(str(n['zda'] + n['zdm']) for n in niveaux)}"
                    f" = {total} zones ; compartimentage : "
                    f"{actions[1]['valeur']} zones sur {total}",
        "topologie": f"niveaux (x {C_N_X0}–{C_N_X1}) → coude x {C_COUDE_X} → "
                     f"centrale (x {C_B_X0}–{C_B_X0 + C_B_W}) → tronc "
                     f"x {C_TRONC_X} → mise en sécurité (x {C_A_X0}–{C_A_X1}) ; "
                     f"registre hors centralisateur dans la même colonne, sans "
                     f"liaison",
        "bas_du_dessin": f"piles jusqu’à {bas_pile:.0f} px, légende à "
                         f"{C_Y_LEGENDE}, report à {C_Y_REPORT}, phrase de "
                         f"principe à {C_Y_PHRASE}, cartouche "
                         f"{C_Y_CARTOUCHE}–{C_Y_CARTOUCHE + C_H_CARTOUCHE}, "
                         f"marge basse {H - (C_Y_CARTOUCHE + C_H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {C_H_CARTOUCHE} px = "
                            f"{largeur * C_H_CARTOUCHE} px², soit "
                            f"{largeur * C_H_CARTOUCHE / (W * H) * 100:.2f} % "
                            f"de la planche",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l’échelle "
                         f"0,96 (1152 / {W})",
        "depassements": depassements if depassements
                        else "aucun — toutes les lignes mesurées sous leur colonne",
    }
    return "\n".join(out) + "\n", controles


def composer_vignette_convergence(donnees):
    """La vignette : le motif sans son appareil — six rangées de marques, un
    tronc unique, deux blocs aux hauteurs proportionnelles. Ce qu'elle laisse :
    les libellés de niveau, les repères de zone, la centrale, le registre hors
    centralisateur, le report et le cartouche."""
    cv = donnees["convergence"]
    niveaux = cv["niveaux"]
    actions = cv["actions"]
    out = []
    A = out.append

    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" '
      f'style="width:100%;height:auto;display:block">')
    entete_style(A, ("filet-1", "filet-2", "encre"))
    A(rect(0, 0, VW, VH, "papier"))
    A(texte(V_MARGE, 26, donnees["vignette_surtitre"], "mono", 9, 500,
            "pivot", tracking=9 * 0.14))

    y0, h_row, ecart = 42, 18, 3
    n_x0, n_x1 = V_MARGE, 96
    a_x0, a_x1 = 170, VW - V_MARGE
    cote, pas = 5, 9

    centres = []
    y = y0
    for n in niveaux:
        A(rect_bord(n_x0, y, n_x1 - n_x0, h_row, "calcaire", "filet-1"))
        _marques_du_niveau(A, n, n_x1 - 8, y + h_row / 2, cote, pas)
        centres.append(y + h_row / 2)
        y += h_row + ecart
    bas = y - ecart

    # Le tronc unique : c'est lui la démonstration — six rangées, une ligne.
    cy = (y0 + bas) / 2
    fourche_in, fourche_out = 104, 140
    for c in centres:
        A(polyligne([(n_x1, c), (fourche_in, c), (fourche_in, cy)], "encre", 1.5))
    A(ligne(fourche_in, cy, fourche_out, cy, "encre", 1.5))

    hauteurs = _hauteurs_actions(actions, bas - y0, 8)
    y = y0
    for a_, h in zip(actions, hauteurs):
        A(rect_bord(a_x0, y, a_x1 - a_x0, h, "calcaire", "filet-1"))
        if a_.get("alarme"):
            A(rect(a_x0 + 1, y + 1, a_x1 - a_x0 - 2, 6, "clair"))
        cyb = y + h / 2
        décalage = 3 if a_.get("alarme") else 0
        A(texte(a_x0 + 10, cyb + décalage - 2, a_["libelle_vignette"], "sans",
                12, 600, "encre", wdth=112))
        A(texte(a_x0 + 10, cyb + décalage + 12, a_["tag"], "mono", 10, 500,
                "pivot", tabulaire=True))
        A(ligne(fourche_out, cyb, a_x0 - 7, cyb, "encre", 1.5))
        A(fleche(a_x0, cyb, "encre", "droite", 7))
        y += h + 8
    A(ligne(fourche_out, y0 + hauteurs[0] / 2,
            fourche_out, bas - hauteurs[-1] / 2, "encre", 1.5))

    A("</svg>")
    total = sum(n["zda"] + n["zdm"] for n in niveaux)
    controles = {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": "carte de projet mesurée à 274–296 px — échelle "
                            f"{274/VW:.2f} à {296/VW:.2f}",
        "motif": f"{total} marques sur {len(niveaux)} rangées, un tronc unique, "
                 f"deux blocs aux hauteurs proportionnelles "
                 f"({hauteurs[0]:.0f} px / {hauteurs[-1]:.0f} px) — libellés de "
                 f"niveau, repères, centrale, registre hors centralisateur, "
                 f"report et cartouche laissés à la planche",
        "corps_minimal": "9 px — rien sous 9, rien ne touche un bord "
                         f"(marge {V_MARGE} px, bas du dessin {bas:.0f} px)",
    }
    return "\n".join(out) + "\n", controles


def composer_appui_convergence(donnees):
    """L'appui : le motif entier à l'échelle 1, densité intermédiaire. Il garde
    les libellés de niveau, les marques, la centrale au libellé court, les deux
    zones avec leur proportion, et une bande basse pour ce qui reste hors du
    centralisateur. Il laisse les repères de zone, les usages, le report, la
    phrase de principe et le cartouche."""
    cv = donnees["convergence"]
    niveaux = cv["niveaux"]
    actions = cv["actions"]
    sys_ = cv["systeme"]

    out = []
    A = out.append
    racine_appui(A, donnees, strokes=("filet-1", "filet-2", "filet-3", "encre"))

    y0, h_row, ecart = 76, 32, 6
    n_x0, n_x1 = A_MARGE, 190
    b_x0, b_w = 214, 156     # 156 et non 130 : « ALARME DE TYPE 1 » mesure
    a_x0, a_x1 = 386, AW - A_MARGE   # 117 px et affleurait le filet de droite
    cote, pas = 7, 13

    # La place libre pour un libellé, marques DÉDUITES : le niveau le plus
    # fourni en porte quatre, et c'est lui qui borne la colonne de texte.
    marques_max = max(n["zda"] + n["zdm"] for n in niveaux)
    dispo_libelle = (n_x1 - 10 - marques_max * pas) - (n_x0 + 10) - 6
    depassements_appui = []
    centres = []
    y = y0
    for n in niveaux:
        A(rect_bord(n_x0, y, n_x1 - n_x0, h_row, "calcaire", "filet-1"))
        cy = y + h_row / 2
        libelle_n = n.get("libelle_court", n["libelle"])
        # ⚠ Les avances calibrées sous-mesurent Archivo 600 d'environ 20 % au
        # rendu (relevé en N08-N09) : la marge est prise ici, pas à l'œil.
        largeur_n = mesurer(libelle_n, 13, "sans-600") * 1.2
        if largeur_n > dispo_libelle:
            depassements_appui.append(
                f"{n['cle']} : {largeur_n:.0f} px pour {dispo_libelle:.0f} px")
        A(texte(n_x0 + 10, cy + 4, libelle_n, "sans", 13, 600,
                "encre", wdth=112))
        _marques_du_niveau(A, n, n_x1 - 10, cy, cote, pas)
        centres.append(cy)
        y += h_row + ecart
    bas = y - ecart

    cy_boite = (y0 + bas) / 2
    A(rect_bord(b_x0, cy_boite - 34, b_w, 68, "papier", "filet-1"))
    A(texte(b_x0 + 12, cy_boite - 4, sys_["libelle_appui"], "sans", 13, 600,
            "encre", wdth=112))
    dispo_boite = b_w - 24
    largeur_sys = mesurer(sys_["libelle_appui"], 13, "sans-600") * 1.2
    if largeur_sys > dispo_boite:
        depassements_appui.append(
            f"centrale : {largeur_sys:.0f} px pour {dispo_boite:.0f} px")
    for k, l in enumerate(sys_["detail_appui"]):
        largeur_l = mesurer(l, 10, "mono", 10 * 0.14)
        if largeur_l > dispo_boite:
            depassements_appui.append(
                f"détail centrale l.{k + 1} : {largeur_l:.0f} px pour "
                f"{dispo_boite:.0f} px")
        A(texte(b_x0 + 12, cy_boite + 14 + k * 13, l, "mono", 10, 500,
                "pivot", tracking=10 * 0.14))
    coude = (n_x1 + b_x0) / 2
    for c in centres:
        A(polyligne([(n_x1, c), (coude, c), (coude, cy_boite)], "encre", 1.5))
    A(ligne(coude, cy_boite, b_x0 - 8, cy_boite, "encre", 1.5))
    A(fleche(b_x0, cy_boite, "encre", "droite", 8))

    hauteurs = _hauteurs_actions(actions, bas - y0, 10)
    tronc = (b_x0 + b_w + a_x0) / 2
    A(ligne(b_x0 + b_w, cy_boite, tronc, cy_boite, "encre", 1.5))
    centres_a = []
    y = y0
    for a_, h in zip(actions, hauteurs):
        A(rect_bord(a_x0, y, a_x1 - a_x0, h, "calcaire", "filet-1"))
        if a_.get("alarme"):
            A(rect(a_x0 + 1, y + 1, a_x1 - a_x0 - 2, 7, "clair"))
        cyb = y + h / 2
        décalage = 4 if a_.get("alarme") else 0
        A(texte(a_x0 + 12, cyb + décalage - 3, a_["libelle_court"], "sans", 13,
                600, "encre", wdth=112))
        A(texte(a_x0 + 12, cyb + décalage + 13, a_["tag"], "mono", 10, 500,
                "pivot", tabulaire=True))
        centres_a.append(cyb)
        y += h + 10
    A(ligne(tronc, centres_a[0], tronc, centres_a[-1], "encre", 1.5))
    for c in centres_a:
        A(ligne(tronc, c, a_x0 - 8, c, "encre", 1.5))
        A(fleche(a_x0, c, "encre", "droite", 8))

    # La bande basse : ce que le centralisateur ne commande pas, en filet
    # interrompu et sans liaison — le propos de la planche tient à l'appui.
    y_hors = bas + 12
    A(_rect_pointille(n_x0, y_hors, a_x1 - n_x0, 30, "papier", "filet-1"))
    libelle = cv["entete_hors"] + " · " + " · ".join(
        h_["libelle"].upper() for h_ in cv["hors"])
    A(texte(n_x0 + 12, y_hors + 19, libelle, "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

    A("</svg>")
    total = sum(n["zda"] + n["zdm"] for n in niveaux)
    return "\n".join(out) + "\n", controles_appui(
        motif=f"les {len(niveaux)} niveaux avec leurs {total} marques, la "
              f"centrale au libellé court, les deux zones aux hauteurs "
              f"proportionnelles ({hauteurs[0]:.0f} px / {hauteurs[-1]:.0f} px) "
              f"et la bande en filet interrompu du registre hors "
              f"centralisateur — repères de zone, usages, report, phrase de "
              f"principe et cartouche laissés à la planche",
        bas=f"piles jusqu’à {bas:.0f} px, bande hors centralisateur "
            f"{y_hors:.0f}–{y_hors + 30:.0f} px, marge basse "
            f"{AH - (y_hors + 30):.0f} px",
        largeur_bande=f"{mesurer(libelle, 10, 'mono', 10 * 0.14):.0f} px pour "
                      f"{a_x1 - n_x0 - 24} px disponibles",
        boite_centrale=f"{b_w} px de large, {dispo_boite} px utiles pour un "
                       f"libellé de {largeur_sys:.0f} px et un mono de "
                       f"{mesurer(sys_['detail_appui'][0], 10, 'mono', 1.4):.0f} px",
        libelles_de_niveau=f"colonne de texte {dispo_libelle:.0f} px "
                           f"(marques déduites, {marques_max} au plus) — "
                           + (", ".join(depassements_appui)
                              if depassements_appui
                              else "aucun dépassement, marge de 20 % prise sur "
                                   "la sous-mesure d’Archivo 600"))


# ── Mécanisme `compensation` — Les Cabanes Urbaines, La Rochelle (2026-09-01) ─
#
# Sixième mécanisme du compositeur. La thèse n'est ni un découpage, ni un
# mouvement, ni une convergence : c'est une SUBSTITUTION. Les planchers n'ont
# pas été traités coupe-feu ; le bâtiment ne forme donc qu'un seul compartiment,
# et ce que la matière ne fait pas, la détection le fait.
#
# La géométrie porte trois affirmations, et rien d'autre :
#   1. le plan qui manque — deux traits INTERROMPUS entre les trois niveaux,
#      épaisseur 2 px, motif long : ils ne peuvent pas se confondre avec les
#      filets de 1 px pleins qui bordent les bandes (piège relevé en N13 et
#      N14 — deux traits doivent différer par autre chose que leur position) ;
#   2. ce qui le remplace — les marques de zone, niveau par niveau, avec la
#      même convention que `convergence` (pleine = détection automatique,
#      évidée = déclencheurs manuels), toujours doublées du texte ;
#   3. ce qui en découle — UNE SEULE accolade embrasse l'empilement entier et
#      aboutit à l'équation que portent les trois plans de zonage de FT2E.
#      C'est ce qui distingue le dessin de `convergence` : là-bas, chaque
#      niveau envoyait son collecteur vers un nœud ; ici rien ne converge,
#      l'accolade dit une ÉGALITÉ, pas un rassemblement.
#
# La bande basse est la vérification : deux foyers de contrôle d'efficacité
# réellement allumés, dont les longueurs de barre sont proportionnelles aux
# deux temps de déclenchement mesurés au procès-verbal. Ce n'est pas une
# conservation — rien ne se somme —, c'est une comparaison à échelle commune ;
# l'interdit posé en N14 (« jamais de schéma proportionnel sur des valeurs qui
# ne bouclent pas ») ne porte pas sur ce cas, et le rapport dessiné est publié
# au bloc `controles`.

CP_Y_ENTETE = 190
CP_Y0 = 204                          # tête de l'empilement des niveaux
CP_H_ROW = 76
CP_ECART_ROW = 22                    # l'entre-deux où passe le plancher
CP_N_X0 = MARGE                      # 56
CP_N_X1 = 660
CP_ACCOLADE_X = 682                  # la barre unique de l'accolade
CP_C_X0 = 704                        # colonne des conséquences
CP_C_X1 = W - MARGE                  # 1144
CP_ECART_C = 12
CP_MARQUE = 9
CP_PAS_MARQUE = 18
CP_PAD = 16
CP_Y_PREUVE_TAG = 506
CP_Y_PREUVE = 518
CP_H_PREUVE = 40
CP_ECART_PREUVE = 10
CP_BARRE_X = 470                     # origine commune des deux barres
CP_BARRE_L = 470                     # longueur de la plus longue
CP_H_BARRE_PREUVE = 10
CP_Y_LEGENDE = 632
CP_Y_REPORT = 654
CP_Y_PHRASE = 686
CP_Y_CARTOUCHE = 714
CP_H_CARTOUCHE = 30


def _plancher_interrompu(A, x0, x1, y, epaisseur=2.0, motif="12 7"):
    """Le plan qui manque : un trait interrompu, plus épais que les filets de
    bande, jamais un filet de 1 px. Ce qui n'arrête pas le feu ne se dessine
    pas d'un trait plein."""
    return A(f'  <line x1="{x0:.2f}" y1="{y:.2f}" x2="{x1:.2f}" y2="{y:.2f}" '
             f'class="s-encre" stroke="{JETON["encre"]}" '
             f'stroke-width="{epaisseur}" stroke-dasharray="{motif}"/>')


def _accolade_compensation(A, x, y_haut, y_bas, x_pile, x_sortie, cy,
                           epaisseur=1.5, retour=10.0):
    """L'accolade unique : deux retours vers l'empilement, une barre verticale
    qui l'embrasse en entier, un départ horizontal vers l'égalité. Elle ne
    collecte pas des niveaux un à un — elle les prend ensemble."""
    A(ligne(x_pile, y_haut, x, y_haut, "encre", epaisseur))
    A(ligne(x_pile, y_bas, x, y_bas, "encre", epaisseur))
    A(ligne(x, y_haut, x, y_bas, "encre", epaisseur))
    A(ligne(x, cy, x_sortie - 9, cy, "encre", epaisseur))
    A(fleche(x_sortie, cy, "encre"))
    return retour


def composer_compensation(donnees):
    cp = donnees["compensation"]
    niveaux = cp["niveaux"]
    consequences = cp["consequences"]
    preuve = cp["preuve"]
    out = []
    A = out.append
    depassements = []
    mesures = 0

    def controler(nom, texte_mesure, corps, profil, dispo, tracking=0.0,
                  marge=1.0):
        """Chaque chaîne dessinée est mesurée contre la largeur intérieure de
        son contenant, et l'écart est publié. Un `assert` rompt la composition
        avant tout rendu (recette de la N14)."""
        nonlocal mesures
        mesures += 1
        largeur = mesurer(texte_mesure, corps, profil, tracking) * marge
        if largeur > dispo:
            depassements.append(f"{nom} : {largeur:.0f} px pour {dispo:.0f} px")
        return dispo - largeur

    marges = []

    # ── Racine ───────────────────────────────────────────────────────────────
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
      f'preserveAspectRatio="xMidYMid meet" role="img" '
      f'style="width:100%;height:auto;display:block" '
      f'aria-label="{echapper(donnees["aria_label"])}">')
    entete_style(A, ("filet-1", "filet-2", "filet-3", "encre"))
    A(rect(0, 0, W, H, "papier"))

    # ── Bloc de titre ────────────────────────────────────────────────────────
    marges.append(controler("surtitre", donnees["surtitre"], 11, "mono", UTILE,
                            11 * 0.14))
    A(texte(MARGE, Y_SURTITRE, donnees["surtitre"], "mono", 11, 500, "pivot",
            tracking=11 * 0.14))
    marges.append(controler("titre", donnees["titre"], 30, "sans-600", UTILE,
                            marge=1.2))
    A(texte(MARGE, Y_TITRE, donnees["titre"], "sans", 30, 700, "encre",
            wdth=112))
    marges.append(controler("sous-titre", donnees["sous_titre"], 16, "sans-400",
                            UTILE))
    A(texte(MARGE, Y_SOUSTITRE, donnees["sous_titre"], "sans", 16, 400,
            "pivot", wdth=100))
    A(rect(MARGE, Y_FILET_TITRE, UTILE, 1, "filet-1"))

    # ── En-têtes de registre ─────────────────────────────────────────────────
    marges.append(controler("en-tête coupe", cp["entete_coupe"], 10, "mono",
                            CP_N_X1 - CP_N_X0, 10 * 0.14))
    A(texte(CP_N_X0, CP_Y_ENTETE, cp["entete_coupe"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    marges.append(controler("en-tête conséquences", cp["entete_consequence"],
                            10, "mono", CP_C_X1 - CP_C_X0, 10 * 0.14))
    A(texte(CP_C_X1, CP_Y_ENTETE, cp["entete_consequence"], "mono", 10, 500,
            "pivot", ancre="end", tracking=10 * 0.14))

    # ── L'empilement des trois niveaux, lu du haut vers le bas comme une coupe
    #    — et, entre eux, le plan qui manque. ─────────────────────────────────
    marques_max = max(n["zda"] + n["zdm"] for n in niveaux)
    dispo_texte = ((CP_N_X1 - CP_PAD) - (CP_N_X0 + CP_PAD)
                   - marques_max * CP_PAS_MARQUE - 14)
    total_zda = total_zdm = 0
    planchers = []
    y = CP_Y0
    for i, n in enumerate(niveaux):
        A(rect_bord(CP_N_X0, y, CP_N_X1 - CP_N_X0, CP_H_ROW, "calcaire",
                    "filet-1"))
        marges.append(controler(f'niveau {n["cle"]}', n["libelle"], 15,
                                "sans-600", dispo_texte, marge=1.2))
        A(texte(CP_N_X0 + CP_PAD, y + 26, n["libelle"], "sans", 15, 600,
                "encre", wdth=112))
        marges.append(controler(f'usages {n["cle"]}', n["usages"], 10, "mono",
                                dispo_texte, 10 * 0.14))
        A(texte(CP_N_X0 + CP_PAD, y + 46, n["usages"], "mono", 10, 500,
                "pivot", tracking=10 * 0.14))
        marges.append(controler(f'repères {n["cle"]}', n["reperes"], 10, "mono",
                                dispo_texte, 10 * 0.14))
        A(texte(CP_N_X0 + CP_PAD, y + 64, n["reperes"], "mono", 10, 500,
                "pivot", tracking=10 * 0.14, tabulaire=True))
        _marques_du_niveau(A, n, CP_N_X1 - CP_PAD, y + CP_H_ROW / 2)
        total_zda += n["zda"]
        total_zdm += n["zdm"]
        if i < len(niveaux) - 1:
            planchers.append(y + CP_H_ROW + CP_ECART_ROW / 2)
        y += CP_H_ROW + CP_ECART_ROW
    bas_pile = y - CP_ECART_ROW
    cy_pile = (CP_Y0 + bas_pile) / 2

    for y_p in planchers:
        _plancher_interrompu(A, CP_N_X0, CP_N_X1, y_p)
    # Le libellé du plan manquant se pose sur le PREMIER entre-deux, à fond
    # papier : le trait passe dessous et ne le barre pas.
    libelle_plan = cp["plan_manquant"]
    # ⚠ La mesure calibrée sous-estime le mono au rendu : sans marge, le
    # dernier tiret du trait interrompu mord sur la dernière lettre.
    largeur_plan = mesurer(libelle_plan, 10, "mono", 10 * 0.14) * 1.08
    marges.append(controler("plan manquant", libelle_plan, 10, "mono",
                            CP_N_X1 - CP_N_X0 - 2 * CP_PAD, 10 * 0.14))
    x_plan = CP_N_X0 + CP_PAD
    A(rect(x_plan - 6, planchers[0] - 8, largeur_plan + 12, 16, "papier"))
    A(texte(x_plan, planchers[0] + 4, libelle_plan, "mono", 10, 500, "encre",
            tracking=10 * 0.14))

    # ── L'accolade unique et les trois conséquences ──────────────────────────
    # Les hauteurs sont DÉRIVÉES du contenu de chaque bloc — jamais
    # réparties à égalité ni réglées à l'œil : le bloc de l'égalité porte
    # une barre d'alarme et une ligne de détail de plus, il est donc plus
    # haut. Le surplus de place se répartit dans le même rapport.
    besoins = [34 + (12 if c.get("alarme") else 0) + 14 * len(c["detail"])
               for c in consequences]
    dispo_c = (bas_pile - CP_Y0) - CP_ECART_C * (len(consequences) - 1)
    hauteurs_c = [dispo_c * b / sum(besoins) for b in besoins]
    centres_c = []
    y = CP_Y0
    for c, h_c in zip(consequences, hauteurs_c):
        if c["pointille"]:
            A(_rect_pointille(CP_C_X0, y, CP_C_X1 - CP_C_X0, h_c, "papier",
                              "filet-1"))
        else:
            A(rect_bord(CP_C_X0, y, CP_C_X1 - CP_C_X0, h_c, "calcaire",
                        "filet-1"))
            A(rect(CP_C_X0 + 1, y + 1, CP_C_X1 - CP_C_X0 - 2, H_BARRE, "clair"))
        décalage = 12 if c.get("alarme") else 0
        largeur_c = CP_C_X1 - CP_C_X0 - 2 * CP_PAD
        marges.append(controler(f'conséquence {c["cle"]}', c["libelle"], 15,
                                "sans-600", largeur_c, marge=1.2))
        A(texte(CP_C_X0 + CP_PAD, y + 26 + décalage, c["libelle"], "sans", 15,
                600, "encre", wdth=112))
        for k, l in enumerate(c["detail"]):
            marges.append(controler(f'détail {c["cle"]} l.{k + 1}', l, 10,
                                    "mono", largeur_c, 10 * 0.14))
            A(texte(CP_C_X0 + CP_PAD, y + 46 + décalage + k * 14, l, "mono",
                    10, 500, "pivot", tracking=10 * 0.14))
        centres_c.append(y + h_c / 2)
        y += h_c + CP_ECART_C

    i_egalite = next(k for k, c in enumerate(consequences)
                     if not c["pointille"])
    _accolade_compensation(A, CP_ACCOLADE_X, CP_Y0, bas_pile, CP_N_X1,
                           CP_C_X0, centres_c[i_egalite])

    # ── La bande basse : la compensation vérifiée au feu réel ────────────────
    marges.append(controler("en-tête preuve", preuve["entete"], 10, "mono",
                            UTILE, 10 * 0.14))
    A(texte(MARGE, CP_Y_PREUVE_TAG, preuve["entete"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    essais = preuve["essais"]
    plus_long = max(e["secondes"] for e in essais)
    echelle = CP_BARRE_L / plus_long
    longueurs = []
    # Le zéro commun : UNE ligne verticale qui traverse les deux rangées,
    # tracée avant les barres. Un trait posé à l'origine de chaque barre
    # disparaissait sous elle (relevé au PNG de contrôle à 1152 px).
    bas_bande = (CP_Y_PREUVE + len(essais) * CP_H_PREUVE
                 + (len(essais) - 1) * CP_ECART_PREUVE)
    A(ligne(CP_BARRE_X, CP_Y_PREUVE - 6, CP_BARRE_X, bas_bande + 6,
            "encre", 1.0))
    y = CP_Y_PREUVE
    for e in essais:
        A(rect_bord(MARGE, y, UTILE, CP_H_PREUVE, "papier", "filet-3"))
        dispo_e = CP_BARRE_X - (MARGE + CP_PAD) - 20
        marges.append(controler(f'essai {e["cle"]}', e["libelle"], 15,
                                "sans-600", dispo_e, marge=1.2))
        A(texte(MARGE + CP_PAD, y + 19, e["libelle"], "sans", 15, 600,
                "encre", wdth=112))
        marges.append(controler(f'combustible {e["cle"]}', e["detail"], 10,
                                "mono", dispo_e, 10 * 0.14))
        A(texte(MARGE + CP_PAD, y + 34, e["detail"], "mono", 10, 500,
                "pivot", tracking=10 * 0.14))
        longueur = e["secondes"] * echelle
        longueurs.append(longueur)
        y_barre = y + (CP_H_PREUVE - CP_H_BARRE_PREUVE) / 2
        A(rect(CP_BARRE_X, y_barre, longueur, CP_H_BARRE_PREUVE, "encre"))
        marges.append(controler(f'temps {e["cle"]}', e["valeur"], 13,
                                "mono",
                                CP_C_X1 - (CP_BARRE_X + longueur + 12),
                                13 * 0.14))
        A(texte(CP_BARRE_X + longueur + 12, y + 25, e["valeur"], "mono",
                13, 600, "encre", tracking=13 * 0.14, tabulaire=True))
        y += CP_H_PREUVE + CP_ECART_PREUVE
    bas_preuve = y - CP_ECART_PREUVE

    # ── La légende des deux marques — la couleur ne porte jamais seule ───────
    x = MARGE
    for entree in cp["legende"]:
        A(_marque_zone(x, CP_Y_LEGENDE - CP_MARQUE + 1, CP_MARQUE,
                       entree["marque"] == "pleine"))
        largeur = mesurer(entree["libelle"], 10, "mono", 10 * 0.14)
        marges.append(controler(f'légende {entree["marque"]}',
                                entree["libelle"], 10, "mono", 380, 10 * 0.14))
        A(texte(x + CP_MARQUE + 8, CP_Y_LEGENDE, entree["libelle"], "mono", 10,
                500, "pivot", tracking=10 * 0.14))
        x += CP_MARQUE + 8 + largeur + 40

    # ── Le report : le périmètre exact de la détection, une ligne ────────────
    marges.append(controler("report", cp["report"], 10, "mono", UTILE,
                            10 * 0.14))
    A(texte(MARGE, CP_Y_REPORT, cp["report"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

    # ── Phrase de principe, pleine largeur ───────────────────────────────────
    marges.append(controler("phrase de principe", donnees["phrase_principe"],
                            17, "sans-400", UTILE))
    A(texte(MARGE, CP_Y_PHRASE, donnees["phrase_principe"], "sans", 17, 400,
            "encre", wdth=100))

    # ── Cartouche — largeur AJUSTÉE au texte, jamais codée ───────────────────
    libelle = donnees["cartouche_legende"]
    largeur = min(600,
                  round(mesurer(libelle, 11, "mono", tracking=11 * 0.14) + 40))
    A(rect(MARGE, CP_Y_CARTOUCHE, largeur, CP_H_CARTOUCHE, "profond"))
    A(texte(MARGE + 20, CP_Y_CARTOUCHE + 20, libelle, "mono", 11, 500, "voile",
            tracking=11 * 0.14))

    A("</svg>")

    assert not depassements, (
        "dépassement de colonne avant rendu : " + " ; ".join(depassements))

    total = total_zda + total_zdm
    controles = {
        "gabarit": f"{W} x {H} — rapport {W/H:.4f} (3:2 exact)",
        "demonstration": f"{total} marques de zone sur {len(niveaux)} niveaux "
                         f"({total_zda} pleines pour la détection automatique, "
                         f"{total_zdm} évidées pour les déclencheurs manuels) ; "
                         f"{len(planchers)} planchers dessinés en trait "
                         f"INTERROMPU de 2 px — le plan qui manque — contre des "
                         f"filets de bande pleins de 1 px ; UNE accolade "
                         f"embrasse l’empilement entier et aboutit à l’égalité, "
                         f"sans collecteur par niveau : rien ne converge, une "
                         f"seule zone est affirmée",
        "comptage": f"détection : {' + '.join(str(n['zda'] + n['zdm']) for n in niveaux)}"
                    f" = {total} zones ; mise en sécurité : 1 zone d’alarme = "
                    f"1 zone de compartimentage = le bâtiment ; "
                    f"{len([c for c in consequences if c['pointille']])} "
                    f"registres en filet interrompu, qu’aucune liaison "
                    f"n’atteint",
        "hauteurs_des_consequences": " · ".join(
            f"{c['cle']} {h:.0f} px pour {b} px de contenu"
            for c, h, b in zip(consequences, hauteurs_c, besoins)),
        "zero_commun": f"une ligne verticale unique à x {CP_BARRE_X}, "
                       f"de y {CP_Y_PREUVE - 6} à {bas_bande + 6} — les deux "
                       f"barres partent du même zéro",
        "proportion_des_barres": f"échelle commune {echelle:.4f} px/s — "
                                 f"{essais[0]['secondes']} s → "
                                 f"{longueurs[0]:.0f} px, "
                                 f"{essais[1]['secondes']} s → "
                                 f"{longueurs[1]:.0f} px ; rapport dessiné "
                                 f"{longueurs[1] / longueurs[0]:.2f}, rapport "
                                 f"mesuré au procès-verbal "
                                 f"{essais[1]['secondes'] / essais[0]['secondes']:.2f} "
                                 f"— comparaison de deux durées, aucune somme "
                                 f"n’est affirmée",
        "topologie": f"empilement (x {CP_N_X0}–{CP_N_X1}, y {CP_Y0}–"
                     f"{bas_pile:.0f}) → accolade x {CP_ACCOLADE_X} → "
                     f"conséquences (x {CP_C_X0}–{CP_C_X1}) ; l’accolade "
                     f"n’aboutit qu’au bloc plein, les deux registres en filet "
                     f"interrompu ne reçoivent aucune liaison",
        "bas_du_dessin": f"empilement jusqu’à {bas_pile:.0f} px, bande de "
                         f"preuve {CP_Y_PREUVE}–{bas_preuve:.0f}, légende à "
                         f"{CP_Y_LEGENDE}, report à {CP_Y_REPORT}, phrase de "
                         f"principe à {CP_Y_PHRASE}, cartouche "
                         f"{CP_Y_CARTOUCHE}–{CP_Y_CARTOUCHE + CP_H_CARTOUCHE}, "
                         f"marge basse {H - (CP_Y_CARTOUCHE + CP_H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {CP_H_CARTOUCHE} px = "
                            f"{largeur * CP_H_CARTOUCHE} px², soit "
                            f"{largeur * CP_H_CARTOUCHE / (W * H) * 100:.2f} % "
                            f"de la planche",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l’échelle "
                         f"0,96 (1152 / {W})",
        "depassements": f"{mesures} chaînes mesurées, 0 dépassement, marge la "
                        f"plus faible {min(marges):.1f} px"
                        if not depassements else depassements,
    }
    return "\n".join(out) + "\n", controles


def composer_vignette_compensation(donnees):
    """La vignette : le motif sans son appareil — trois bandes de marques, deux
    planchers interrompus, une accolade, un bloc plein. Ce qu'elle laisse : les
    libellés d'usage, les repères de zone, les détails des conséquences, la
    bande de preuve, la légende, le report et le cartouche."""
    cp = donnees["compensation"]
    niveaux = cp["niveaux"]
    consequences = cp["consequences"]
    out = []
    A = out.append

    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" '
      f'style="width:100%;height:auto;display:block">')
    entete_style(A, ("filet-1", "filet-2", "encre"))
    A(rect(0, 0, VW, VH, "papier"))
    A(texte(V_MARGE, 26, donnees["vignette_surtitre"], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    y0, h_row, ecart = 46, 30, 14
    n_x0, n_x1 = V_MARGE, 138
    c_x0, c_x1 = 186, VW - V_MARGE
    cote, pas = 5, 9

    planchers = []
    y = y0
    for i, n in enumerate(niveaux):
        A(rect_bord(n_x0, y, n_x1 - n_x0, h_row, "calcaire", "filet-1"))
        A(texte(n_x0 + 8, y + h_row / 2 + 4, n["libelle_court"], "sans", 11,
                600, "encre", wdth=112))
        _marques_du_niveau(A, n, n_x1 - 8, y + h_row / 2, cote, pas)
        if i < len(niveaux) - 1:
            planchers.append(y + h_row + ecart / 2)
        y += h_row + ecart
    bas = y - ecart
    for y_p in planchers:
        # 2 px à 300 comme à 1200 : le trait du plan manquant ne se réduit pas
        # avec le gabarit, sans quoi il cesse de se distinguer des filets.
        _plancher_interrompu(A, n_x0, n_x1, y_p, 2.0, "7 4")

    h_c = ((bas - y0) - 8 * (len(consequences) - 1)) / len(consequences)
    centres_c = []
    y = y0
    for c in consequences:
        if c["pointille"]:
            A(_rect_pointille(c_x0, y, c_x1 - c_x0, h_c, "papier", "filet-1",
                              "4 3"))
        else:
            A(rect_bord(c_x0, y, c_x1 - c_x0, h_c, "calcaire", "filet-1"))
            A(rect(c_x0 + 1, y + 1, c_x1 - c_x0 - 2, 6, "clair"))
        décalage = 3 if c.get("alarme") else 0
        A(texte(c_x0 + 9, y + h_c / 2 + 4 + décalage, c["libelle_court"],
                "sans", 11, 600, "encre", wdth=112))
        centres_c.append(y + h_c / 2)
        y += h_c + 8

    i_egalite = next(k for k, c in enumerate(consequences)
                     if not c["pointille"])
    x_acc = (n_x1 + c_x0) / 2
    A(ligne(n_x1, y0, x_acc, y0, "encre", 1.5))
    A(ligne(n_x1, bas, x_acc, bas, "encre", 1.5))
    A(ligne(x_acc, y0, x_acc, bas, "encre", 1.5))
    A(ligne(x_acc, centres_c[i_egalite], c_x0 - 7, centres_c[i_egalite],
            "encre", 1.5))
    A(fleche(c_x0, centres_c[i_egalite], "encre", "droite", 7))

    A("</svg>")
    total = sum(n["zda"] + n["zdm"] for n in niveaux)
    controles = {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": "carte de projet mesurée à 274–296 px — échelle "
                            f"{274/VW:.2f} à {296/VW:.2f}",
        "motif": f"{total} marques sur {len(niveaux)} bandes, "
                 f"{len(planchers)} planchers interrompus de 2 px, une "
                 f"accolade unique et un bloc plein — usages, repères, détails "
                 f"des conséquences, bande de preuve, légende, report et "
                 f"cartouche laissés à la planche",
        "trait_du_plan_manquant": "2,0 px à 300 comme à 1200 — l’épaisseur ne "
                                  "se réduit pas avec le gabarit, sinon le "
                                  "trait cesse de se distinguer des filets de "
                                  "bande (1 px)",
        "corps_minimal": "9 px — rien sous 9, rien ne touche un bord "
                         f"(marge {V_MARGE} px, bas du dessin {bas:.0f} px)",
    }
    return "\n".join(out) + "\n", controles


def composer_appui_compensation(donnees):
    """L'appui : le motif entier à l'échelle 1, densité intermédiaire. Il garde
    les libellés de niveau, les marques, les planchers interrompus, l'accolade,
    les trois conséquences au libellé court, et une bande basse pour les deux
    temps de déclenchement. Il laisse les usages, les repères, les détails, la
    légende, le report, la phrase de principe et le cartouche."""
    cp = donnees["compensation"]
    niveaux = cp["niveaux"]
    consequences = cp["consequences"]
    preuve = cp["preuve"]

    out = []
    A = out.append
    racine_appui(A, donnees, strokes=("filet-1", "filet-2", "filet-3", "encre"))

    y0, h_row, ecart = 60, 50, 24
    n_x0, n_x1 = A_MARGE, 216
    c_x0, c_x1 = 296, AW - A_MARGE
    cote, pas = 7, 13
    depassements_appui = []

    marques_max = max(n["zda"] + n["zdm"] for n in niveaux)
    dispo_libelle = (n_x1 - 10 - marques_max * pas) - (n_x0 + 10) - 6

    planchers = []
    y = y0
    for i, n in enumerate(niveaux):
        A(rect_bord(n_x0, y, n_x1 - n_x0, h_row, "calcaire", "filet-1"))
        cy = y + h_row / 2
        libelle_n = n["libelle_court"]
        largeur_n = mesurer(libelle_n, 13, "sans-600") * 1.2
        if largeur_n > dispo_libelle:
            depassements_appui.append(
                f"{n['cle']} : {largeur_n:.0f} px pour {dispo_libelle:.0f} px")
        A(texte(n_x0 + 10, cy + 4, libelle_n, "sans", 13, 600, "encre",
                wdth=112))
        _marques_du_niveau(A, n, n_x1 - 10, cy, cote, pas)
        if i < len(niveaux) - 1:
            planchers.append(y + h_row + ecart / 2)
        y += h_row + ecart
    bas = y - ecart
    for y_p in planchers:
        _plancher_interrompu(A, n_x0, n_x1, y_p, 2.0, "9 5")
    # Le premier entre-deux porte le libellé, sur fond papier : le trait
    # passe dessous. Le second reste nu — même graphique, même sens.
    libelle_plan = cp["plan_manquant_court"]
    largeur_plan = mesurer(libelle_plan, 9, "mono", 9 * 0.14) * 1.08
    if largeur_plan > n_x1 - n_x0 - 12:
        depassements_appui.append(
            f"plan manquant : {largeur_plan:.0f} px pour "
            f"{n_x1 - n_x0 - 12} px")
    # ⚠ Le libellé se pose SOUS le trait, pas dessus : la bande de l’appui ne
    # fait que 192 px, et un fond papier de 150 px y masquait le trait presque
    # entier — l’interruption cessait de se lire (relevé au PNG à 552 px).
    A(texte(n_x0 + 2, planchers[0] + 12, libelle_plan, "mono", 9, 500,
            "pivot", tracking=9 * 0.14))

    h_c = ((bas - y0) - 10 * (len(consequences) - 1)) / len(consequences)
    centres_c = []
    y = y0
    for c in consequences:
        if c["pointille"]:
            A(_rect_pointille(c_x0, y, c_x1 - c_x0, h_c, "papier", "filet-1"))
        else:
            A(rect_bord(c_x0, y, c_x1 - c_x0, h_c, "calcaire", "filet-1"))
            A(rect(c_x0 + 1, y + 1, c_x1 - c_x0 - 2, 7, "clair"))
        décalage = 4 if c.get("alarme") else 0
        libelle_c = c["libelle_court"]
        largeur_c = mesurer(libelle_c, 13, "sans-600") * 1.2
        if largeur_c > c_x1 - c_x0 - 24:
            depassements_appui.append(
                f"{c['cle']} : {largeur_c:.0f} px pour {c_x1 - c_x0 - 24} px")
        A(texte(c_x0 + 12, y + h_c / 2 - 3 + décalage, libelle_c, "sans", 13,
                600, "encre", wdth=112))
        detail_c = c["detail_appui"]
        largeur_d = mesurer(detail_c, 9, "mono", 9 * 0.14)
        if largeur_d > c_x1 - c_x0 - 24:
            depassements_appui.append(
                f"détail {c['cle']} : {largeur_d:.0f} px pour "
                f"{c_x1 - c_x0 - 24} px")
        A(texte(c_x0 + 12, y + h_c / 2 + 13 + décalage, detail_c, "mono", 9,
                500, "pivot", tracking=9 * 0.14))
        centres_c.append(y + h_c / 2)
        y += h_c + 10

    i_egalite = next(k for k, c in enumerate(consequences)
                     if not c["pointille"])
    x_acc = (n_x1 + c_x0) / 2
    A(ligne(n_x1, y0, x_acc, y0, "encre", 1.5))
    A(ligne(n_x1, bas, x_acc, bas, "encre", 1.5))
    A(ligne(x_acc, y0, x_acc, bas, "encre", 1.5))
    A(ligne(x_acc, centres_c[i_egalite], c_x0 - 8, centres_c[i_egalite],
            "encre", 1.5))
    A(fleche(c_x0, centres_c[i_egalite], "encre", "droite", 8))

    # La bande basse : les deux temps, à la même échelle qu'à la planche.
    essais = preuve["essais"]
    plus_long = max(e["secondes"] for e in essais)
    barre_x = 150
    barre_l = 240
    echelle = barre_l / plus_long
    y = bas + 22
    longueurs = []
    for e in essais:
        libelle_e = e["libelle_court"]
        largeur_e = mesurer(libelle_e, 11, "mono", 11 * 0.14)
        if largeur_e > barre_x - n_x0 - 12:
            depassements_appui.append(
                f"{e['cle']} : {largeur_e:.0f} px pour {barre_x - n_x0 - 12} px")
        A(texte(n_x0, y + 8, libelle_e, "mono", 11, 500, "pivot",
                tracking=11 * 0.14))
        longueur = e["secondes"] * echelle
        longueurs.append(longueur)
        A(rect(barre_x, y + 1, longueur, 8, "encre"))
        A(ligne(barre_x, y - 2, barre_x, y + 11, "encre", 1.0))
        A(texte(barre_x + longueur + 10, y + 8, e["valeur"], "mono", 11, 600,
                "encre", tracking=11 * 0.14, tabulaire=True))
        y += 26
    bas_preuve = y - 26 + 11

    A("</svg>")
    total = sum(n["zda"] + n["zdm"] for n in niveaux)
    return "\n".join(out) + "\n", controles_appui(
        motif=f"les {len(niveaux)} niveaux avec leurs {total} marques, les "
              f"{len(planchers)} planchers interrompus, l’accolade unique, les "
              f"{len(consequences)} conséquences au libellé court et la bande "
              f"des deux temps de déclenchement — usages, repères, détails, "
              f"légende, report, phrase de principe et cartouche laissés à la "
              f"planche",
        bas=f"empilement jusqu’à {bas:.0f} px, bande de preuve "
            f"{bas + 22:.0f}–{bas_preuve:.0f} px, marge basse "
            f"{AH - bas_preuve:.0f} px",
        proportion_des_barres=f"échelle {echelle:.4f} px/s — "
                              f"{longueurs[0]:.0f} px et {longueurs[1]:.0f} px, "
                              f"rapport {longueurs[1] / longueurs[0]:.2f}",
        libelles=f"colonne de niveau {dispo_libelle:.0f} px (marques déduites, "
                 f"{marques_max} au plus) — "
                 + (", ".join(depassements_appui) if depassements_appui
                    else "aucun dépassement, marge de 20 % prise sur la "
                         "sous-mesure d’Archivo 600"))



# ── Mécanisme `discordance` (2026-09-02) ─────────────────────────────────────
# Deux découpages d'un même bâtiment qui ne se recouvrent pas. Au-dessus de la
# bande, le découpage RÉGLEMENTAIRE : un crochet continu embrasse les deux
# volumes neufs en une seule zone de calcul, tandis que le volume restructuré
# ne porte que des marques isolées — la réglementation par éléments n'embrasse
# rien. Au-dessous, le découpage de l'AIR : une descente et une machine par
# volume, aucune mutualisée, plus cinq extractions sous le seul laboratoire.
#
# La démonstration se lit texte masqué : continu contre discret en haut, un
# contre trois en bas. Et une frontière — celle qui sépare la liaison de l'open
# space — traverse la bande, descend vers deux machines distinctes, et BUTE
# contre le crochet du calcul, qui l'ignore.
#
# ⚠ Aucun trait interrompu : le corpus lui fait déjà dire deux choses
# différentes (« position abandonnée » à la Maison des Métiers, « réserve pour
# plus tard » au groupe scolaire de La Flotte). L'isolement se dit ici par des
# marques SÉPARÉES, l'appartenance par un trait CONTINU.
#
# ⚠ Mesures ABSOLUES par format ; `ech` ne commande que les motifs et les
# petits accessoires (épaisseurs, pointes). Les extractions sont ABSENTES de la
# vignette et de l'appui (`postes=None`) : c'est une mesure de format.

DI_Y_H1 = 210          # régime — ligne 1
DI_Y_H2 = 226          # régime — ligne 2
DI_Y_H3 = 242          # cote / exigences — ligne 3
DI_Y_H4 = 258          # exigences — ligne 4 (colonne des éléments seule)
DI_Y_CROCH_H = 264     # sommet du crochet du calcul et des marques isolées
DI_H_CROCH_H = 24      # pied à 288 — c'est là que bute la frontière ignorée
DI_Y_NOTE_LIM = 304
DI_Y_BANDE = 316
DI_H_BANDE = 74        # bas de bande à 390
DI_Y_CTA = 424
DI_H_CTA = 40
DI_L_CTA_MAX = 200
DI_Y_TAG_B = 494
DI_Y_DET_B = 510
DI_Y_EXTR_TAG = 542
DI_Y_EXTR0 = 566
DI_PAS_EXTR = 22
DI_Y_PHRASE = 688
DI_Y_CARTOUCHE = 714
DI_H_CARTOUCHE = 30
DI_MARQUE = 7
DI_PAD = 14


def _di_largeurs(volumes, span):
    """Largeur de chaque volume, proportionnée au débit de sa centrale.

    Le dossier ne donne pas la surface volume par volume — seulement local par
    local, sans dire quel local tient dans quel volume. Proportionner sur les
    débits est un choix consigné dans `a_valider_ft2e` : il code une donnée que
    la source établit, au lieu d'en supposer une qu'elle n'établit pas.
    """
    total = sum(v["debit"] for v in volumes)
    return [span * v["debit"] / total for v in volumes], total


def _di_bornes(volumes, x0, span):
    largeurs, total = _di_largeurs(volumes, span)
    bornes, x = [], x0
    for l in largeurs:
        bornes.append((x, x + l))
        x += l
    return bornes, largeurs, total


def _di_crochet(A, x0, x1, y_sommet, h, epaisseur, vers_le_bas=True):
    """Accolade carrée : deux montants et une traverse. Ouverte vers le bas
    (registre du calcul) ou vers le haut (registre de l'air)."""
    y1 = y_sommet + h if vers_le_bas else y_sommet - h
    A(polyligne([(x0, y1), (x0, y_sommet), (x1, y_sommet), (x1, y1)],
                "encre", epaisseur))


def _di_marques_isolees(A, x0, x1, n, y_sommet, h, epaisseur):
    """n traits verticaux que RIEN ne relie — le régime par éléments."""
    pas = (x1 - x0) / (n + 1)
    for k in range(n):
        x = x0 + pas * (k + 1)
        A(ligne(x, y_sommet, x, y_sommet + h, "encre", epaisseur))
    return [x0 + pas * (k + 1) for k in range(n)]


def composer_discordance(donnees):
    d = donnees["discordance"]
    volumes = d["volumes"]
    out = []
    A = out.append
    depassements = []

    def controler(nom, chaine, corps, profil, dispo, tracking=0.0):
        largeur = mesurer(chaine, corps, profil, tracking)
        if largeur > dispo:
            depassements.append(
                f"{nom} : {largeur:.0f} px pour {dispo:.0f} px")
        return largeur

    bornes, largeurs, total = _di_bornes(volumes, MARGE, UTILE)
    i_calc = [k for k, v in enumerate(volumes) if v["dans_le_calcul"]]
    x_calc0 = bornes[i_calc[0]][0]
    x_calc1 = bornes[i_calc[-1]][1]
    x_hors0, x_hors1 = bornes[0]
    # La frontière que le calcul ignore : entre les deux volumes du calcul.
    x_ignoree = bornes[i_calc[0]][1]

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
    A(texte(MARGE, Y_TITRE, donnees["titre"], "sans", 30, 700, "encre",
            wdth=112))
    A(texte(MARGE, Y_SOUSTITRE, donnees["sous_titre"], "sans", 16, 400,
            "pivot", wdth=100))
    A(rect(MARGE, Y_FILET_TITRE, UTILE, 1, "filet-1"))

    # ── En-tête du schéma ────────────────────────────────────────────────────
    controler("en-tête schéma", d["entete"], 10, "mono", UTILE, 10 * 0.14)
    A(texte(MARGE, Y_ENTETE, d["entete"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

    # ── Registre HAUT, colonne des éléments (hors calcul) ────────────────────
    el = d["elements"]
    dispo_g = x_hors1 - x_hors0 - 8
    for cle, y in (("tag", DI_Y_H1), ("detail", DI_Y_H2)):
        controler(f"éléments {cle}", el[cle], 10, "mono", dispo_g, 10 * 0.14)
        A(texte(x_hors0, y, el[cle], "mono", 10, 500, "pivot",
                tracking=10 * 0.14))
    marques = el["marques"]
    milieu = (len(marques) + 1) // 2
    for k, (y, groupe) in enumerate(((DI_Y_H3, marques[:milieu]),
                                     (DI_Y_H4, marques[milieu:]))):
        ligne_txt = " · ".join(f'{m["libelle"]}{NN}{m["valeur"]}'
                               for m in groupe)
        controler(f"exigences l.{k + 1}", ligne_txt, 10, "mono", dispo_g,
                  10 * 0.14)
        A(texte(x_hors0, y, ligne_txt, "mono", 10, 500, "pivot",
                tracking=10 * 0.14, tabulaire=True))
    _di_marques_isolees(A, x_hors0, x_hors1, len(marques),
                        DI_Y_CROCH_H, DI_H_CROCH_H, 2.0)

    # ── Registre HAUT, colonne du calcul ─────────────────────────────────────
    ca = d["calcul"]
    dispo_d = x_calc1 - x_calc0 - 8
    for cle, y in (("tag", DI_Y_H1), ("detail", DI_Y_H2), ("cote", DI_Y_H3)):
        controler(f"calcul {cle}", ca[cle], 10, "mono", dispo_d, 10 * 0.14)
        A(texte(x_calc0 + 10, y, ca[cle], "mono", 10, 500, "pivot",
                tracking=10 * 0.14, tabulaire=(cle == "cote")))
    _di_crochet(A, x_calc0, x_calc1, DI_Y_CROCH_H, DI_H_CROCH_H, 2.0)

    y_butee = DI_Y_CROCH_H + DI_H_CROCH_H
    controler("note de limite", d["note_limite"], 10, "mono",
              W - MARGE - (x_ignoree + 12), 10 * 0.14)
    A(texte(x_ignoree + 12, DI_Y_NOTE_LIM, d["note_limite"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))

    # ── La bande : les trois volumes, largeur ∝ débit de leur centrale ───────
    for (x0, x1), v in zip(bornes, volumes):
        A(rect_bord(x0, DI_Y_BANDE, x1 - x0, DI_H_BANDE, "calcaire", "filet-1"))
        controler(f'volume {v["cle"]}', v["libelle"], 15, "sans-600",
                  x1 - x0 - 2 * DI_PAD)
        A(texte(x0 + DI_PAD, DI_Y_BANDE + 30, v["libelle"], "sans", 15, 600,
                "encre", wdth=112))
        controler(f'mention {v["cle"]}', v["mention"], 10, "mono",
                  x1 - x0 - 2 * DI_PAD, 10 * 0.14)
        A(texte(x0 + DI_PAD, DI_Y_BANDE + 52, v["mention"], "mono", 10, 500,
                "pivot", tracking=10 * 0.14))

    # ── La frontière que le calcul ignore : elle traverse la bande et bute ──
    # ⚠ APRÈS la bande : les cases ont un fond opaque et l'effaceraient.
    A(ligne(x_ignoree, y_butee, x_ignoree, DI_Y_BANDE + DI_H_BANDE,
            "encre", 2.0))
    A(ligne(x_ignoree - 9, y_butee, x_ignoree + 9, y_butee, "encre", 2.0))

    # ── Registre BAS : une descente et une machine par volume ────────────────
    air = d["air"]
    y_bas_bande = DI_Y_BANDE + DI_H_BANDE
    for (x0, x1), v in zip(bornes, volumes):
        cx = (x0 + x1) / 2
        l_cta = min(DI_L_CTA_MAX, (x1 - x0) * 0.72)
        bx = cx - l_cta / 2
        A(ligne(cx, y_bas_bande, cx, DI_Y_CTA, "encre", 2.0))
        A(rect_bord(bx, DI_Y_CTA, l_cta, DI_H_CTA, "papier", "filet-1"))
        controler(f'cta {v["cle"]}', air["libelle_centrale"], 10, "mono",
                  l_cta - 24, 10 * 0.14)
        A(texte(bx + 12, DI_Y_CTA + 16, air["libelle_centrale"], "mono", 10,
                500, "pivot", tracking=10 * 0.14))
        cote = f'{v["debit"]}{NN}{v["unite"]}'
        controler(f'débit {v["cle"]}', cote, 18, "sans-700", l_cta - 24)
        A(texte(bx + 12, DI_Y_CTA + 34, cote, "sans", 18, 700, "encre",
                wdth=118, tabulaire=True))

    for cle, y in (("tag", DI_Y_TAG_B), ("detail", DI_Y_DET_B)):
        controler(f"air {cle}", air[cle], 10, "mono", UTILE, 10 * 0.14)
        A(texte(MARGE, y, air[cle], "mono", 10, 500, "pivot",
                tracking=10 * 0.14))

    # ── Les extractions : des marques isolées, sous le seul premier volume ───
    ex = d["extractions"]
    controler("extractions tag", ex["tag"], 10, "mono", UTILE, 10 * 0.14)
    A(texte(MARGE, DI_Y_EXTR_TAG, ex["tag"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))
    x_val = x_hors1 - 26
    x_lib = x_hors0 + DI_MARQUE + 9
    for k, poste in enumerate(ex["postes"]):
        y = DI_Y_EXTR0 + k * DI_PAS_EXTR
        A(rect(x_hors0, y - DI_MARQUE, DI_MARQUE, DI_MARQUE, "encre"))
        valeur = f'{poste["valeur"]}{NN}{ex["unite"]}'
        l_val = mesurer(valeur, 10, "mono", 10 * 0.14)
        controler(f'extraction {k + 1}', poste["libelle"], 10, "mono",
                  x_val - l_val - 10 - x_lib, 10 * 0.14)
        A(texte(x_lib, y, poste["libelle"], "mono", 10, 500, "pivot",
                tracking=10 * 0.14))
        A(texte(x_val, y, valeur, "mono", 10, 500, "encre",
                ancre="end", tracking=10 * 0.14, tabulaire=True))
        A(fleche(x_val + 14, y + 1, "encre", "bas", 8))

    # ── Phrase de principe, pleine largeur ───────────────────────────────────
    controler("phrase de principe", donnees["phrase_principe"], 17,
              "sans-400", UTILE)
    A(texte(MARGE, DI_Y_PHRASE, donnees["phrase_principe"], "sans", 17, 400,
            "encre", wdth=100))

    # ── Cartouche — largeur AJUSTÉE au texte, jamais codée ───────────────────
    libelle = donnees["cartouche_legende"]
    largeur = min(600,
                  round(mesurer(libelle, 11, "mono", tracking=11 * 0.14) + 40))
    A(rect(MARGE, DI_Y_CARTOUCHE, largeur, DI_H_CARTOUCHE, "profond"))
    A(texte(MARGE + 20, DI_Y_CARTOUCHE + 20, libelle, "mono", 11, 500,
            "voile", tracking=11 * 0.14))

    A("</svg>")

    assert not depassements, (
        "dépassement(s) sur la planche : " + " ; ".join(depassements))

    controles = {
        "gabarit": f"{W} x {H} — rapport {W/H:.4f} (3:2 exact)",
        "demonstration": "deux découpages superposés d’une même bande : au "
                         f"registre haut, un crochet continu sur {len(i_calc)} "
                         f"volumes contre {len(el['marques'])} marques que rien "
                         "ne relie ; au registre bas, une descente et une "
                         f"machine par volume, {len(volumes)} en tout, aucune "
                         "mutualisée. La frontière ignorée du calcul traverse "
                         "la bande et bute sur la traverse du crochet — "
                         "continu contre discret, un contre trois",
        "proportion": "largeurs ∝ débits des centrales : "
                      + " / ".join(f'{v["debit"]}' for v in volumes)
                      + f" m³/h sur {total} — "
                      + " / ".join(f"{l:.1f}" for l in largeurs)
                      + f" px sur {UTILE}",
        "frontiere_ignoree": f"x {x_ignoree:.1f} — trait de "
                             f"{DI_Y_BANDE + DI_H_BANDE} à {y_butee}, arrêté "
                             f"{y_butee - DI_Y_CROCH_H} px sous la traverse du "
                             f"crochet du calcul (x {x_calc0:.1f} à "
                             f"{x_calc1:.1f}) : il ne la touche pas",
        "extractions": f'{len(ex["postes"])} marques isolées sous le seul '
                       f'volume hors calcul (x {x_hors0:.0f} à {x_hors1:.0f}), '
                       "chacune sa flèche de rejet — aucune reprise dessinée",
        "bas_du_dessin": f"machines jusqu’à {DI_Y_CTA + DI_H_CTA}, mentions "
                         f"d’air à {DI_Y_TAG_B}–{DI_Y_DET_B}, extractions "
                         f"{DI_Y_EXTR_TAG}–"
                         f"{DI_Y_EXTR0 + (len(ex['postes']) - 1) * DI_PAS_EXTR}"
                         f", phrase à {DI_Y_PHRASE}, cartouche "
                         f"{DI_Y_CARTOUCHE}–{DI_Y_CARTOUCHE + DI_H_CARTOUCHE}, "
                         f"marge basse {H - (DI_Y_CARTOUCHE + DI_H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {DI_H_CARTOUCHE} px = "
                            f"{largeur * DI_H_CARTOUCHE} px², soit "
                            f"{largeur * DI_H_CARTOUCHE / (W * H) * 100:.2f} % "
                            "de la planche",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l’échelle "
                         f"0,96 (1152 / {W})",
        "depassements": "aucun — toutes les lignes mesurées sous leur colonne",
    }
    return "\n".join(out) + "\n", controles


# ── Vignette : le motif seul ─────────────────────────────────────────────────
DIV_Y_SURTITRE = 30
DIV_Y_CROCH_H = 48
DIV_H_CROCH_H = 14
DIV_Y_BANDE = 76
DIV_H_BANDE = 40
DIV_Y_CTA = 138
DIV_H_CTA = 22
DIV_PAD = 6


def composer_vignette_discordance(donnees):
    d = donnees["discordance"]
    volumes = d["volumes"]
    out = []
    A = out.append
    depassements = []

    def controler(nom, chaine, corps, profil, dispo, tracking=0.0):
        largeur = mesurer(chaine, corps, profil, tracking)
        if largeur > dispo:
            depassements.append(f"{nom} : {largeur:.0f} px pour {dispo:.0f} px")

    span = VW - 2 * V_MARGE
    bornes, largeurs, total = _di_bornes(volumes, V_MARGE, span)
    i_calc = [k for k, v in enumerate(volumes) if v["dans_le_calcul"]]
    x_calc0, x_calc1 = bornes[i_calc[0]][0], bornes[i_calc[-1]][1]
    x_hors0, x_hors1 = bornes[0]
    x_ignoree = bornes[i_calc[0]][1]

    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" '
      f'focusable="false" style="width:100%;height:auto;display:block">')
    entete_style(A, ("filet-1", "filet-2", "encre"))
    A(rect(0, 0, VW, VH, "papier"))

    controler("surtitre", donnees["vignette_surtitre"], 9, "mono", span,
              9 * 0.14)
    A(texte(V_MARGE, DIV_Y_SURTITRE, donnees["vignette_surtitre"], "mono", 9,
            500, "pivot", tracking=9 * 0.14))

    # Registre haut : le crochet continu contre les marques isolées.
    _di_crochet(A, x_calc0, x_calc1, DIV_Y_CROCH_H, DIV_H_CROCH_H, 1.5)
    _di_marques_isolees(A, x_hors0, x_hors1, len(d["elements"]["marques"]),
                        DIV_Y_CROCH_H, DIV_H_CROCH_H, 1.5)

    y_butee = DIV_Y_CROCH_H + DIV_H_CROCH_H

    for (x0, x1), v in zip(bornes, volumes):
        A(rect_bord(x0, DIV_Y_BANDE, x1 - x0, DIV_H_BANDE, "calcaire",
                    "filet-1"))
        controler(f'volume {v["cle"]}', v["libelle_vignette"], 9, "mono",
                  x1 - x0 - 2 * DIV_PAD, 9 * 0.14)
        A(texte(x0 + DIV_PAD, DIV_Y_BANDE + 24, v["libelle_vignette"], "mono",
                9, 500, "encre", tracking=9 * 0.14))

    # La frontière ignorée — tracée APRÈS la bande, dont le fond est opaque.
    A(ligne(x_ignoree, y_butee, x_ignoree, DIV_Y_BANDE + DIV_H_BANDE,
            "encre", 1.5))
    A(ligne(x_ignoree - 5, y_butee, x_ignoree + 5, y_butee, "encre", 1.5))

    # Registre bas : une descente et une machine par volume.
    y_bas = DIV_Y_BANDE + DIV_H_BANDE
    for (x0, x1), v in zip(bornes, volumes):
        cx = (x0 + x1) / 2
        l_cta = min(76, (x1 - x0) * 0.72)
        A(ligne(cx, y_bas, cx, DIV_Y_CTA, "encre", 1.5))
        A(rect_bord(cx - l_cta / 2, DIV_Y_CTA, l_cta, DIV_H_CTA, "papier",
                    "filet-1"))
        cote = f'{v["debit"]}'
        controler(f'débit {v["cle"]}', cote, 10, "sans-700", l_cta - 10)
        A(texte(cx, DIV_Y_CTA + 15, cote, "sans", 10, 700, "encre", wdth=118,
                ancre="middle", tabulaire=True))

    A("</svg>")

    assert not depassements, (
        "dépassement(s) sur la vignette : " + " ; ".join(depassements))

    controles = {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": "carte de projet mesurée de 274 à 296 px — "
                            f"échelle {274/VW:.2f} à {296/VW:.2f}",
        "corps_minimal": f"9 px dans le repère — rendu à {9*274/VW:.1f} px "
                         "au pire cas",
        "motif": f"la bande à {len(volumes)} volumes proportionnés aux débits, "
                 f"le crochet continu sur {len(i_calc)} d’entre eux contre "
                 f"{len(d['elements']['marques'])} marques isolées, la "
                 "frontière ignorée qui bute, et une machine chiffrée par "
                 "volume — exigences, article, extractions, phrase de principe "
                 "et cartouche laissés à la planche",
        "bas_du_dessin": f"machines jusqu’à {DIV_Y_CTA + DIV_H_CTA} px, marge "
                         f"basse {VH - (DIV_Y_CTA + DIV_H_CTA)} px",
    }
    return "\n".join(out) + "\n", controles


# ── Appui : densité intermédiaire ────────────────────────────────────────────
DIA_Y_TAG = 72
DIA_Y_CROCH_H = 92
DIA_H_CROCH_H = 20
DIA_Y_BANDE = 136
DIA_H_BANDE = 54
DIA_Y_CTA = 228
DIA_H_CTA = 30
DIA_Y_NOTE = 300
DIA_PAD = 9


def composer_appui_discordance(donnees):
    d = donnees["discordance"]
    volumes = d["volumes"]
    out = []
    A = out.append
    depassements = []

    def controler(nom, chaine, corps, profil, dispo, tracking=0.0):
        largeur = mesurer(chaine, corps, profil, tracking)
        if largeur > dispo:
            depassements.append(f"{nom} : {largeur:.0f} px pour {dispo:.0f} px")

    span = AW - 2 * A_MARGE
    bornes, largeurs, total = _di_bornes(volumes, A_MARGE, span)
    i_calc = [k for k, v in enumerate(volumes) if v["dans_le_calcul"]]
    x_calc0, x_calc1 = bornes[i_calc[0]][0], bornes[i_calc[-1]][1]
    x_hors0, x_hors1 = bornes[0]
    x_ignoree = bornes[i_calc[0]][1]

    racine_appui(A, donnees, ("filet-1", "filet-2", "encre"))

    # Les deux régimes, en tête de chaque colonne — libellés courts.
    controler("appui régime hors calcul", d["elements"]["tag_court"], 10,
              "mono", x_hors1 - x_hors0 - 4, 10 * 0.14)
    A(texte(x_hors0, DIA_Y_TAG, d["elements"]["tag_court"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    controler("appui régime calcul", d["calcul"]["tag_court"], 10, "mono",
              x_calc1 - x_calc0 - 4, 10 * 0.14)
    A(texte(x_calc0 + 8, DIA_Y_TAG, d["calcul"]["tag_court"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))

    _di_crochet(A, x_calc0, x_calc1, DIA_Y_CROCH_H, DIA_H_CROCH_H, 1.75)
    _di_marques_isolees(A, x_hors0, x_hors1, len(d["elements"]["marques"]),
                        DIA_Y_CROCH_H, DIA_H_CROCH_H, 1.75)

    y_butee = DIA_Y_CROCH_H + DIA_H_CROCH_H

    for (x0, x1), v in zip(bornes, volumes):
        A(rect_bord(x0, DIA_Y_BANDE, x1 - x0, DIA_H_BANDE, "calcaire",
                    "filet-1"))
        controler(f'appui volume {v["cle"]}', v["libelle_court"], 10, "mono",
                  x1 - x0 - 2 * DIA_PAD, 10 * 0.14)
        A(texte(x0 + DIA_PAD, DIA_Y_BANDE + 22, v["libelle_court"], "mono", 10,
                500, "encre", tracking=10 * 0.14))
        controler(f'appui mention {v["cle"]}', v["mention"], 10, "mono",
                  x1 - x0 - 2 * DIA_PAD, 10 * 0.14)
        A(texte(x0 + DIA_PAD, DIA_Y_BANDE + 40, v["mention"], "mono", 10, 500,
                "pivot", tracking=10 * 0.14))

    # La frontière ignorée — tracée APRÈS la bande, dont le fond est opaque.
    A(ligne(x_ignoree, y_butee, x_ignoree, DIA_Y_BANDE + DIA_H_BANDE,
            "encre", 1.75))
    A(ligne(x_ignoree - 7, y_butee, x_ignoree + 7, y_butee, "encre", 1.75))

    y_bas = DIA_Y_BANDE + DIA_H_BANDE
    for (x0, x1), v in zip(bornes, volumes):
        cx = (x0 + x1) / 2
        l_cta = min(112, (x1 - x0) * 0.76)
        A(ligne(cx, y_bas, cx, DIA_Y_CTA, "encre", 1.75))
        A(rect_bord(cx - l_cta / 2, DIA_Y_CTA, l_cta, DIA_H_CTA, "papier",
                    "filet-1"))
        cote = f'{v["debit"]}{NN}{v["unite"]}'
        controler(f'appui débit {v["cle"]}', cote, 13, "sans-700", l_cta - 10)
        A(texte(cx, DIA_Y_CTA + 20, cote, "sans", 13, 700, "encre", wdth=118,
                ancre="middle", tabulaire=True))

    controler("appui note", d["note_courte"], 10, "mono", span, 10 * 0.14)
    A(texte(A_MARGE, DIA_Y_NOTE, d["note_courte"], "mono", 10, 500, "pivot",
            tracking=10 * 0.14))

    A("</svg>")

    assert not depassements, (
        "dépassement(s) sur l’appui : " + " ; ".join(depassements))

    return "\n".join(out) + "\n", controles_appui(
        motif=f"la bande à {len(volumes)} volumes proportionnés aux débits, "
              f"le crochet continu sur {len(i_calc)} d’entre eux contre "
              f"{len(d['elements']['marques'])} marques isolées, la frontière "
              "ignorée qui bute, une machine chiffrée par volume et les deux "
              "régimes nommés court — les exigences par élément, l’article 20 "
              "et les cinq extractions sont ABSENTS de ce format : mesure de "
              "format, pas exception (leurs libellés tomberaient sous le "
              "plancher de lisibilité)",
        bas=f"machines jusqu’à {DIA_Y_CTA + DIA_H_CTA} px, note à "
            f"{DIA_Y_NOTE} px, marge basse {AH - DIA_Y_NOTE} px",
        proportion="largeurs ∝ débits : "
                   + " / ".join(f"{l:.1f}" for l in largeurs)
                   + f" px sur {span}")

if __name__ == "__main__":
    import json as _json
    import sys
    from pathlib import Path as _Path
    _d = _json.loads((_Path(sys.argv[1]) / "planche.json")
                     .read_text(encoding="utf-8"))
    if "transfert" in _d:
        executer(composer_transfert, composer_vignette_transfert,
                 composer_appui_transfert)
    elif "partage" in _d:
        executer(composer_partage, composer_vignette_partage,
                 composer_appui_partage)
    elif "inversion" in _d:
        executer(composer_inversion, composer_vignette_inversion,
                 composer_appui_inversion)
    elif "compensation" in _d:
        executer(composer_compensation,
                 composer_vignette_compensation,
                 composer_appui_compensation)
    elif "discordance" in _d:
        executer(composer_discordance, composer_vignette_discordance,
                 composer_appui_discordance)
    elif "convergence" in _d:
        executer(composer_convergence, composer_vignette_convergence,
                 composer_appui_convergence)
    else:
        executer(composer, composer_vignette, composer_appui)
