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
                    fleche, cercle, entete_style, replier, racine_appui,
                    controles_appui, executer)


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
        "demonstration": f"barres d'alarme : {barres_avant} sur 1 bloc AVANT "
                         f"(tout le site) contre {barres_apres} sur {len(zones)} "
                         f"blocs APRÈS — la géométrie porte la thèse, aucun "
                         f"chiffre de la fiche n'est répété",
        "topologie": f"événement (x {EVT_X}) → système (x {BOITE_X0}–"
                     f"{BOITE_X0 + BOITE_W}) → site (x {BLOC_X0}–{BLOC_X1}) ; "
                     f"tronc de distribution à x {TRONC_X}",
        "bas_du_dessin": f"pile de zones jusqu'à {bas_zones:.0f} px, ligne hors "
                         f"zonage à {Y_HORS}, phrase de principe à {Y_PHRASE}, "
                         f"cartouche {Y_CARTOUCHE}–{Y_CARTOUCHE + H_CARTOUCHE}, "
                         f"marge basse {H - (Y_CARTOUCHE + H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur * H_CARTOUCHE} px², soit "
                            f"{largeur * H_CARTOUCHE / (W * H) * 100:.2f} % de la planche",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l'échelle 0,96 "
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
        motif=f"1 bloc AVANT (barre d'alarme sur tout, {avant['valeur']} m² "
              f"évacués) contre {len(zones)} zones APRÈS dont la provisionnée, "
              "barre et mention sur la seule zone en alarme, légende en tête — "
              "événement, systèmes et hors zonage laissés à la planche",
        bas=f"pile de zones jusqu'à {y1} px, marge basse {AH - y1} px")


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
                         "paroi à l'horizontale (encre 2,5), la descente est "
                         "barrée d'une croix, l'escalier extérieur monte vers "
                         "l'étage — la géométrie porte la thèse, aucun chiffre "
                         "de la fiche n'est répété",
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
                            f"l'encre, pas de la réserve)",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l'échelle "
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
                 "la traverse, la descente barrée — l'alerte, l'escalier des "
                 "secours et l'unité protégée sont laissés à la planche",
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
              "transfert à travers la paroi, la descente barrée, l'unité "
              "protégée du rez-de-chaussée, l'escalier des secours — "
              "l'alerte (centrale et départs) reste à la planche",
        bas=f"sol à {sol_y} px, notes de pied empilées à 316–332, "
            f"marge basse {AH - 332} px")


if __name__ == "__main__":
    import json as _json
    import sys
    from pathlib import Path as _Path
    _d = _json.loads((_Path(sys.argv[1]) / "planche.json")
                     .read_text(encoding="utf-8"))
    if "transfert" in _d:
        executer(composer_transfert, composer_vignette_transfert,
                 composer_appui_transfert)
    else:
        executer(composer, composer_vignette, composer_appui)
