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
    elif "convergence" in _d:
        executer(composer_convergence, composer_vignette_convergence,
                 composer_appui_convergence)
    else:
        executer(composer, composer_vignette, composer_appui)
