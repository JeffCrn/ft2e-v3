#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compositeur de planche — archétype `sankey-energie`.

Protocole : docs/superpowers/specs/2026-08-12-planches-references-protocole.md

Il lit un `planche.json` (l'extraction, produite par la session de génération) et
écrit les deux dessins qui en découlent :

    planche.svg    1200 x 800 — la planche de fiche, lue à 1152 px (échelle 0,96)
    vignette.svg    300 x 200 — la vignette de carte, lue à 274-296 px (0,91-0,99)

Usage :

    python scripts/planches/sankey-energie.py public/images/projets/<slug>

La géométrie est CALCULÉE : aucune coordonnée n'est tapée à la main, et le bloc
`controles` du JSON est recalculé à chaque exécution — c'est ce qui rend le relevé
rejouable et ce qui a permis de trouver, à la première planche, sept défauts que
le seul rendu en pleine page ne montrait pas.

Les six autres archétypes du protocole recevront chacun leur module dans ce même
répertoire. Ce qu'ils partagent — jetons, mesure des chasses, échappement des
insécables, double écriture des couleurs — a vocation à remonter dans un module
commun le jour où le deuxième existera ; le factoriser maintenant reviendrait à
généraliser sur un seul cas.
"""

from _tronc import (NN, W, H, MARGE, UTILE, VW, VH, V_MARGE, AW, AH, A_MARGE,
                    JETON, SANS, MONO, mesurer, echapper, texte, rect, rect_bord,
                    ligne, replier, racine_appui, controles_appui, executer,
                    entete_style, fleche)


# La révision 4 supprime la partition 7/5 et la colonne de relevé : la planche
# schématise la solution — le flux occupe la largeur utile entière, et les
# chiffres que la fiche porte déjà ne montent pas sur le dessin.
DESSIN_X0 = MARGE

# Une vignette n'est pas un recadrage de la planche : c'est une COMPOSITION
# PROPRE, calée sur la taille où elle est lue. Les cartes de projet font 274 à
# 296 px de large ; à 300 px de repère, l'échelle de rendu va de 0,91 à 0,99, et
# les corps écrits ici sont donc les corps lus. Recadrer la planche de 1200 dans
# la même case donnait 0,25 : un lavis, et un cadrage subi.


# ── Colonnes de la zone de schéma — pleine largeur depuis la révision 4 ──────
LIB_X = DESSIN_X0                 # libellés + détails
VAL_X = DESSIN_X0 + 280           # valeurs mono, alignées à droite
BANDE_X0 = DESSIN_X0 + 310        # départ des bandes (366)
BANDE_X1 = DESSIN_X0 + 850        # arrivée des bandes (906) — le flux porte la planche
NOEUD_W = 9
NOEUD_LIB_X = BANDE_X1 + NOEUD_W + 10   # 925 — étiquettes de nœud jusqu'à 1144

# ── Rythme vertical ───────────────────────────────────────────────────────────
Y_SURTITRE = 76
Y_TITRE = 112
Y_SOUSTITRE = 138
Y_FILET_TITRE = 160
Y_ENTETE = 190
Y_BANDES = 206
HAUTEUR_BANDES = 232.0            # hauteur totale d'encre des bandes —
                                  # calée pour que la note de pied laisse
                                  # 30 px à la phrase de principe
ECART = 24.0                      # écart entre deux postes de même origine
ECART_ORIGINE = 40.0              # écart entre deux origines — il porte du sens
Y_CARTOUCHE = 714
H_CARTOUCHE = 30


# mesure qui a montré que l'estimation posait l'unité 22 px trop loin.


def bande(y0g, y1g, y0d, y1d, couleur):
    """Ruban de Sankey : deux cubiques symétriques, point d'inflexion à mi-course."""
    xm = (BANDE_X0 + BANDE_X1) / 2
    d = (f"M {BANDE_X0:.2f} {y0g:.2f} "
         f"C {xm:.2f} {y0g:.2f}, {xm:.2f} {y0d:.2f}, {BANDE_X1:.2f} {y0d:.2f} "
         f"L {BANDE_X1:.2f} {y1d:.2f} "
         f"C {xm:.2f} {y1d:.2f}, {xm:.2f} {y1g:.2f}, {BANDE_X0:.2f} {y1g:.2f} Z")
    return (f'  <path d="{d}" class="c-{couleur} s-filet1" fill="{JETON[couleur]}" '
            f'stroke="{JETON["filet-1"]}" stroke-width="1"/>')


def composer(donnees, slug):
    sk = donnees["sankey"]
    sources = sk["sources"]
    total = sum(s["valeur"] for s in sources)
    echelle = HAUTEUR_BANDES / total

    # ── Hauteurs et positions verticales, source par source ──────────────────
    y = float(Y_BANDES)
    poses = []
    for i, s in enumerate(sources):
        if i > 0:
            precedente = sources[i - 1]["origine"]
            y += ECART_ORIGINE if s["origine"] != precedente else ECART
        h = s["valeur"] * echelle
        poses.append({"src": s, "y0": y, "y1": y + h, "h": h})
        y += h
    bas_bandes = y

    # ── Nœuds : les bandes d'une même origine s'y touchent, sans écart ───────
    noeuds = {}
    for n in sk["noeuds"]:
        membres = [p for p in poses if p["src"]["origine"] == n["cle"]]
        hauteur = sum(p["h"] for p in membres)
        centre = (membres[0]["y0"] + membres[-1]["y1"]) / 2
        noeuds[n["cle"]] = {"n": n, "y0": centre - hauteur / 2, "h": hauteur}

    out = []
    A = out.append

    # ── Racine ───────────────────────────────────────────────────────────────
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
      f'preserveAspectRatio="xMidYMid meet" role="img" '
      f'style="width:100%;height:auto;display:block" '
      f'aria-label="{echapper(donnees["aria_label"])}">')
    A("<style>")
    for cle, hexa in JETON.items():
        A(f"  .c-{cle} {{ fill: var(--color-{cle}, {hexa}); }}")
    A(f'  .s-filet1 {{ stroke: var(--color-filet-1, {JETON["filet-1"]}); }}')
    A(f"  .t-sans {{ font-family: {SANS}; }}")
    A(f"  .t-mono {{ font-family: {MONO}; }}")
    A("</style>")

    A(rect(0, 0, W, H, "papier"))

    # ── Bloc de titre ────────────────────────────────────────────────────────
    A(texte(MARGE, Y_SURTITRE, donnees["surtitre"], "mono", 11, 500,
            "pivot", tracking=11 * 0.14))
    A(texte(MARGE, Y_TITRE, donnees["titre"], "sans", 30, 700, "encre", wdth=112))
    A(texte(MARGE, Y_SOUSTITRE, donnees["sous_titre"], "sans", 16, 400,
            "pivot", wdth=100))
    A(rect(MARGE, Y_FILET_TITRE, UTILE, 1, "filet-1"))

    # ── En-tête de périmètre — il empêche la planche de mentir ───────────────
    # (Depuis la révision 4, la planche ne porte qu'un périmètre : celui du
    # schéma. Le relevé du bâtiment et son en-tête ont quitté le dessin.)
    A(texte(DESSIN_X0, Y_ENTETE, sk["entete"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))

    # ── Bandes ───────────────────────────────────────────────────────────────
    curseur = {c: n["y0"] for c, n in noeuds.items()}
    for p in poses:
        cle = p["src"]["origine"]
        yd0 = curseur[cle]
        yd1 = yd0 + p["h"]
        curseur[cle] = yd1
        A(bande(p["y0"], p["y1"], yd0, yd1,
                "pivot" if cle == "enveloppe" else "clair"))

    # ── Libellés de poste ────────────────────────────────────────────────────
    # La largeur disponible pour le libellé se DÉDUIT de celle de sa valeur : la
    # mesure a montré « Vidéoprojecteur, baie de brassage » à 3,2 px de son
    # « 200 W ». Un libellé qui dépasse se replie sur deux lignes.
    bas_libelles = 0.0
    for p in poses:
        src = p["src"]
        yl = p["y0"] + 12
        valeur = f'{src["valeur_affichee"]}{NN}{sk["unite"]}'
        dispo = VAL_X - mesurer(valeur, 12, "mono") - LIB_X - 16
        lignes = replier(src["libelle"], 15, dispo)
        for k, ligne in enumerate(lignes):
            A(texte(LIB_X, yl + k * 17, ligne, "sans", 15, 400, "encre", wdth=100))
        A(texte(VAL_X, yl, valeur, "mono", 12, 500, "encre",
                ancre="end", tabulaire=True))
        y_detail = yl + len(lignes) * 17
        for k, ligne in enumerate(src.get("detail", []) or []):
            A(texte(LIB_X, y_detail + k * 13, ligne, "mono", 10, 500,
                    "pivot", tracking=10 * 0.14))
        bas = y_detail + max(len(src.get("detail", []) or []) - 1, 0) * 13 + 5
        bas_libelles = max(bas_libelles, bas)

    # ── Nœuds ────────────────────────────────────────────────────────────────
    for cle, nd in noeuds.items():
        A(rect(BANDE_X1, nd["y0"], NOEUD_W, nd["h"], "encre"))
        yl = nd["y0"] + nd["h"] / 2
        A(texte(NOEUD_LIB_X, yl - 2, nd["n"]["libelle"], "sans", 15, 600,
                "encre", wdth=112))
        A(texte(NOEUD_LIB_X, yl + 16, f'{nd["n"]["valeur_affichee"]}{NN}{sk["unite"]}',
                "mono", 12, 500, "pivot", tabulaire=True))

    # ── Note de pied de la zone de schéma ────────────────────────────────────
    y_note = max(bas_bandes, bas_libelles) + 36
    A(rect(DESSIN_X0, y_note - 18, UTILE, 1, "filet-3"))
    A(texte(DESSIN_X0, y_note, sk["note_pied"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))

    # La colonne de relevé de la révision 3 a été SUPPRIMÉE (révision 4) : les
    # chiffres du bâtiment vivent dans la fiche, pas sur la planche. Si une
    # planche future relève de l'exception chiffrée du Temps 2, ce module sera
    # révisé à ce moment-là — pas de code mort en attendant.

    # ── Phrase de principe, pleine largeur ───────────────────────────────────
    A(texte(MARGE, 688, donnees["phrase_principe"], "sans", 17, 400,
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
        "gabarit_schema": f"flux de {BANDE_X0} à {BANDE_X1} px, nœuds étiquetés "
                          f"jusqu’à {W - MARGE} px — schéma pleine largeur, colonne "
                          f"de relevé supprimée (révision 4)",
        "bouclage_bandes": " + ".join(str(s["valeur"]) for s in sources)
                           + f" = {total}{NN}{sk['unite']} ; "
                           f"hauteur totale {sum(p['h'] for p in poses):.2f} px "
                           f"(échelle {echelle:.6f} px/{sk['unite']})",
        "part_enveloppe_dans_la_hauteur":
            f"{sources[-1]['valeur']} / {total} = "
            f"{sources[-1]['valeur']/total*100:.3f} %",
        "bas_du_dessin": f"bandes jusqu’à {bas_bandes:.2f} px, libellés jusqu’à "
                         f"{bas_libelles:.2f} px — note de pied à {y_note:.2f}, "
                         f"phrase de principe à 688, cartouche 714–744, "
                         f"marge basse {H - (Y_CARTOUCHE + H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur*H_CARTOUCHE} px², soit "
                            f"{largeur*H_CARTOUCHE/(W*H)*100:.2f} % de la planche",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l’échelle 0,96 "
                         f"(1152 / {W})",
    }
    return "\n".join(out) + "\n", controles


def composer_vignette(donnees):
    """La vignette : le motif de l'archétype, sans son appareil.

    Ce qu'elle garde de la planche : la géométrie des flux et les deux nœuds
    avec leur valeur — c'est-à-dire la thèse, un rapport.
    Ce qu'elle laisse : le titre (la carte le porte en dessous), le relevé, la
    phrase de principe, le cartouche, et tous les libellés de poste. Six
    libellés dans 300 px de large ne se lisent pas ; les taire est une décision,
    les rogner en était une aussi, mais subie."""
    sk = donnees["sankey"]
    sources = sk["sources"]
    total = sum(s["valeur"] for s in sources)

    x0, x1 = V_MARGE, 170
    noeud_w, lib_x = 6, 182
    hauteur, ecart, ecart_origine = 96.0, 5.0, 14.0
    echelle = hauteur / total

    y = 38.0
    poses = []
    for i, src in enumerate(sources):
        if i > 0:
            y += ecart_origine if src["origine"] != sources[i - 1]["origine"] else ecart
        h = src["valeur"] * echelle
        poses.append({"src": src, "y0": y, "y1": y + h, "h": h})
        y += h

    noeuds = {}
    for n in sk["noeuds"]:
        membres = [p for p in poses if p["src"]["origine"] == n["cle"]]
        ht = sum(p["h"] for p in membres)
        centre = (membres[0]["y0"] + membres[-1]["y1"]) / 2
        noeuds[n["cle"]] = {"n": n, "y0": centre - ht / 2, "h": ht, "centre": centre}

    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false" '
      f'style="width:100%;height:auto;display:block">')
    A("<style>")
    for cle, hexa in JETON.items():
        A(f"  .c-{cle} {{ fill: var(--color-{cle}, {hexa}); }}")
    A(f'  .s-filet1 {{ stroke: var(--color-filet-1, {JETON["filet-1"]}); }}')
    A(f"  .t-sans {{ font-family: {SANS}; }}")
    A(f"  .t-mono {{ font-family: {MONO}; }}")
    A("</style>")
    A(rect(0, 0, VW, VH, "papier"))
    A(texte(V_MARGE, 22, donnees["vignette_surtitre"], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    xm = (x0 + x1) / 2
    curseur = {c: n["y0"] for c, n in noeuds.items()}
    for p in poses:
        cle = p["src"]["origine"]
        d0 = curseur[cle]
        d1 = d0 + p["h"]
        curseur[cle] = d1
        couleur = "pivot" if cle == "enveloppe" else "clair"
        d = (f'M {x0:.2f} {p["y0"]:.2f} C {xm:.2f} {p["y0"]:.2f}, {xm:.2f} {d0:.2f}, '
             f'{x1:.2f} {d0:.2f} L {x1:.2f} {d1:.2f} '
             f'C {xm:.2f} {d1:.2f}, {xm:.2f} {p["y1"]:.2f}, {x0:.2f} {p["y1"]:.2f} Z')
        A(f'  <path d="{d}" class="c-{couleur} s-filet1" fill="{JETON[couleur]}" '
          f'stroke="{JETON["filet-1"]}" stroke-width="1"/>')

    for nd in noeuds.values():
        A(rect(x1, nd["y0"], noeud_w, nd["h"], "encre"))
        A(texte(lib_x, nd["centre"] - 3, nd["n"]["libelle"], "sans", 12, 600,
                "encre", wdth=112))
        A(texte(lib_x, nd["centre"] + 11,
                f'{nd["n"]["valeur_affichee"]}{NN}{sk["unite"]}',
                "mono", 10, 500, "pivot", tabulaire=True))

    A("</svg>")
    controles = {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": f"carte de projet mesurée de 274 à 296 px — "
                            f"échelle {274/VW:.2f} à {296/VW:.2f}",
        "corps_minimal": f"9 px dans le repère — rendu à {9*274/VW:.1f} px au pire cas",
        "bas_du_dessin": f"{poses[-1]['y1']:.2f} px, marge basse "
                         f"{VH - poses[-1]['y1']:.2f} px",
    }
    return "\n".join(out) + "\n", controles


def composer_appui(donnees):
    """L'appui du hero : le motif entier à l'échelle 1, densité intermédiaire.

    Ce qu'il garde : les six bandes aux hauteurs proportionnelles, les deux
    nœuds avec leur valeur, et les libellés des postes dont la bande est assez
    haute pour les porter (plus l'enveloppe, que son écart d'origine isole).
    Ce qu'il laisse : les valeurs par poste, les détails, la note de pied —
    ils vivent sur la planche."""
    sk = donnees["sankey"]
    sources = sk["sources"]
    total = sum(s["valeur"] for s in sources)

    x0, x1 = 200, 396
    noeud_w, lib_node_x = 8, 412
    hauteur, ecart, ecart_origine = 210.0, 8.0, 24.0
    echelle = hauteur / total

    y = 62.0
    poses = []
    for i, src in enumerate(sources):
        if i > 0:
            y += ecart_origine if src["origine"] != sources[i - 1]["origine"] else ecart
        h = src["valeur"] * echelle
        poses.append({"src": src, "y0": y, "y1": y + h, "h": h})
        y += h

    noeuds = {}
    for n in sk["noeuds"]:
        membres = [p for p in poses if p["src"]["origine"] == n["cle"]]
        ht = sum(p["h"] for p in membres)
        centre = (membres[0]["y0"] + membres[-1]["y1"]) / 2
        noeuds[n["cle"]] = {"n": n, "y0": centre - ht / 2, "h": ht, "centre": centre}

    out = []
    A = out.append
    racine_appui(A, donnees, strokes=("filet-1",))

    xm = (x0 + x1) / 2
    curseur = {c: n["y0"] for c, n in noeuds.items()}
    for p in poses:
        cle = p["src"]["origine"]
        d0 = curseur[cle]
        d1 = d0 + p["h"]
        curseur[cle] = d1
        couleur = "pivot" if cle == "enveloppe" else "clair"
        d = (f'M {x0:.2f} {p["y0"]:.2f} C {xm:.2f} {p["y0"]:.2f}, {xm:.2f} {d0:.2f}, '
             f'{x1:.2f} {d0:.2f} L {x1:.2f} {d1:.2f} '
             f'C {xm:.2f} {d1:.2f}, {xm:.2f} {p["y1"]:.2f}, {x0:.2f} {p["y1"]:.2f} Z')
        A(f'  <path d="{d}" class="c-{couleur} s-filet1" fill="{JETON[couleur]}" '
          f'stroke="{JETON["filet-1"]}" stroke-width="1"/>')

    # Les libellés de poste — seulement là où la bande peut les porter.
    for p in poses:
        if p["h"] >= 14 or p["src"]["origine"] == "enveloppe":
            lib = p["src"]["libelle"]
            A(texte(x0 - 12, (p["y0"] + p["y1"]) / 2 + 4, lib, "sans", 13, 600,
                    "encre", wdth=112, ancre="end"))

    for nd in noeuds.values():
        A(rect(x1, nd["y0"], noeud_w, nd["h"], "encre"))
        A(texte(lib_node_x, nd["centre"] - 2, nd["n"]["libelle"], "sans", 14,
                600, "encre", wdth=112))
        A(texte(lib_node_x, nd["centre"] + 15,
                f'{nd["n"]["valeur_affichee"]}{NN}{sk["unite"]}',
                "mono", 11, 500, "pivot", tabulaire=True))

    A("</svg>")
    return "\n".join(out) + "\n", controles_appui(
        motif="les six bandes proportionnelles et les deux nœuds chiffrés à "
              "l’échelle 1 ; libellés portés par les bandes assez hautes "
              "(plus l’enveloppe) — valeurs par poste, détails et note de "
              "pied laissés à la planche",
        bas=f"bandes jusqu’à {poses[-1]['y1']:.0f} px, marge basse "
            f"{AH - poses[-1]['y1']:.0f} px")


# ═══════════════════════════════════════════════════════════════════════════════
# Mécanisme `plafonds` — la frontière réglementaire qui commande le générateur
# (logements Maubec, Chagnolet). Même famille que le Sankey : la proportion
# portée par la géométrie. Trois pistes à la même origine et à la même échelle —
# 1 px par kg éq. CO₂/m², l'échelle EST la donnée —, le plafond qui s'effondre
# au passage de la frontière (un double trait, comme toute alerte de la charte :
# filet doublé + mention), le générateur qui répond. Texte masqué : deux pistes
# longues aux trois quarts pleines, une piste courte au remplissage mince, et le
# seuil des accolées prolongé, que les remplissages du gaz dépassent.
# ═══════════════════════════════════════════════════════════════════════════════

P_X0 = MARGE + 414         # 470 — départ des pistes
P_K = 1.0                  # px par kg éq. CO₂/m²
P_H = 30                   # hauteur de piste
P_LIB_DISPO = P_X0 - 16 - MARGE   # 398 — largeur de la colonne bâtiment


def _batiments(donnees):
    return [e for e in donnees["plafonds"]["elements"] if e.get("type") == "batiment"]


def _frontiere(donnees):
    return next(e for e in donnees["plafonds"]["elements"]
                if e.get("type") == "frontiere")


def composer_plafonds(donnees):
    p = donnees["plafonds"]
    bats = _batiments(donnees)
    depassements = []

    def controler(nom, contenu, corps, profil, dispo, tracking=0.0):
        l = mesurer(contenu, corps, profil, tracking)
        if l > dispo:
            depassements.append(f"{nom} : {l:.0f} px pour {dispo:.0f} disponibles")
        return l

    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
      f'preserveAspectRatio="xMidYMid meet" role="img" '
      f'style="width:100%;height:auto;display:block" '
      f'aria-label="{echapper(donnees["aria_label"])}">')
    A("<style>")
    for cle, hexa in JETON.items():
        A(f"  .c-{cle} {{ fill: var(--color-{cle}, {hexa}); }}")
    A(f'  .s-filet1 {{ stroke: var(--color-filet-1, {JETON["filet-1"]}); }}')
    A(f'  .s-encre {{ stroke: var(--color-encre, {JETON["encre"]}); }}')
    A(f"  .t-sans {{ font-family: {SANS}; }}")
    A(f"  .t-mono {{ font-family: {MONO}; }}")
    A("</style>")
    A(rect(0, 0, W, H, "papier"))

    # ── Bloc de titre ────────────────────────────────────────────────────────
    A(texte(MARGE, 76, donnees["surtitre"], "mono", 11, 500, "pivot",
            tracking=11 * 0.14))
    A(texte(MARGE, 112, donnees["titre"], "sans", 30, 700, "encre", wdth=112))
    A(texte(MARGE, 138, donnees["sous_titre"], "sans", 16, 400, "pivot", wdth=100))
    A(rect(MARGE, 160, UTILE, 1, "filet-1"))

    # ── En-tête de périmètre + légende des signes ────────────────────────────
    controler("entête", p["entete"], 10, "mono", UTILE, 1.4)
    A(texte(MARGE, 190, p["entete"], "mono", 10, 500, "pivot", tracking=1.4))

    lx = float(MARGE)
    A(rect_bord(lx, 206, 18, 10, "clair", "filet-1"))
    lx += 26
    A(texte(lx, 215, p["legende_resultat"], "mono", 10, 500, "pivot", tracking=1.4))
    lx += mesurer(p["legende_resultat"], 10, "mono", 1.4) + 30
    A(rect_bord(lx, 206, 18, 10, "papier", "filet-1"))
    lx += 26
    A(texte(lx, 215, p["legende_plafond"], "mono", 10, 500, "pivot", tracking=1.4))
    lx += mesurer(p["legende_plafond"], 10, "mono", 1.4) + 30
    A(rect_bord(lx, 205, 12, 12, "calcaire", "filet-1"))
    lx += 20
    A(texte(lx, 215, p["legende_logement"], "mono", 10, 500, "pivot", tracking=1.4))

    # ── Un rang par bâtiment ─────────────────────────────────────────────────
    def rang(e, y0):
        nom_l = mesurer(e["nom"], 15, "sans-600")
        A(texte(MARGE, y0 + 14, e["nom"], "sans", 15, 600, "encre", wdth=112))
        cx = MARGE + nom_l + 18
        for i in range(e["cellules"]):
            A(rect_bord(cx + i * 22, y0 + 1, 16, 16, "calcaire", "filet-1"))
        controler(f'composition {e["cle"]}', e["composition"], 10, "mono",
                  P_LIB_DISPO, 1.4)
        A(texte(MARGE, y0 + 36, e["composition"], "mono", 10, 500, "pivot",
                tracking=1.4))
        yg = y0 + 60
        for g in e["generateurs"]:
            controler(f'générateur {e["cle"]}', g["libelle"], 15, "sans-400",
                      P_LIB_DISPO)
            A(texte(MARGE, yg, g["libelle"], "sans", 15, 400, "encre", wdth=100))
            controler(f'détail {e["cle"]}', g["detail"], 10, "mono",
                      P_LIB_DISPO, 1.4)
            A(texte(MARGE, yg + 18, g["detail"], "mono", 10, 500, "pivot",
                    tracking=1.4))
            yg += 44
        py = y0 + 6
        A(rect_bord(P_X0, py, e["plafond"] * P_K, P_H, "papier", "filet-1"))
        A(rect_bord(P_X0, py, e["resultat"] * P_K, P_H, "clair", "filet-1"))
        A(texte(P_X0 + e["plafond"] * P_K - 8, py - 6,
                f'PLAFOND{NN}{e["plafond_affiche"]}', "mono", 10, 500, "pivot",
                tracking=1.4, ancre="end"))
        A(texte(P_X0 + e["resultat"] * P_K + 10, py + P_H / 2 + 4,
                e["resultat_affiche"], "mono", 12, 500, "encre", tabulaire=True))
        return max(yg - 44 + 22, py + P_H)

    A(texte(MARGE, 246, p["regime_collectif"], "mono", 10, 500, "pivot",
            tracking=1.4))
    y_a, y_b, y_c = 262.0, 370.0, 524.0
    bas_a = rang(bats[0], y_a)
    bas_b = rang(bats[1], y_b)

    # ── La frontière : filet doublé + mention, comme toute alerte du système ──
    fr = _frontiere(donnees)
    A(texte(MARGE, 478, p["frontiere_mention"], "mono", 10, 500, "encre",
            tracking=1.4))
    A(ligne(MARGE, 488, W - MARGE, 488, "encre"))
    A(ligne(MARGE, 492, W - MARGE, 492, "encre"))
    A(texte(MARGE, 512, p["regime_accole"], "mono", 10, 500, "pivot",
            tracking=1.4))
    A(texte(W - MARGE, 512, fr["detail"][1], "mono", 10, 500, "pivot",
            tracking=1.4, ancre="end"))

    bas_c = rang(bats[2], y_c)

    # ── Le seuil des accolées, prolongé sur les trois pistes ─────────────────
    guide_x = P_X0 + bats[2]["plafond"] * P_K
    A(ligne(guide_x, 252, guide_x, y_c + 6 + P_H + 14, "encre"))
    controler("mention du guide", p["guide_mention"], 10, "mono",
              W - MARGE - guide_x - 8, 1.4)
    A(texte(guide_x + 8, 246, p["guide_mention"], "mono", 10, 500, "pivot",
            tracking=1.4))

    # ── Phrase de principe, pleine largeur ───────────────────────────────────
    l_phrase = controler("phrase de principe", donnees["phrase_principe"], 17,
                         "sans-400", UTILE)
    A(texte(MARGE, 688, donnees["phrase_principe"], "sans", 17, 400, "encre",
            wdth=100))

    # ── Cartouche — largeur ajustée au texte, jamais codée ───────────────────
    libelle = donnees["cartouche_legende"]
    largeur = min(600, round(mesurer(libelle, 11, "mono", 11 * 0.14) + 40))
    A(rect(MARGE, 714, largeur, 30, "profond"))
    A(texte(MARGE + 20, 734, libelle, "mono", 11, 500, "voile",
            tracking=11 * 0.14))

    A("</svg>")

    controles = {
        "gabarit": f"{W} x {H} — rapport {W/H:.4f} (3:2 exact)",
        "demonstration": "trois pistes à la même origine et à l’échelle commune "
                         f"de {P_K:.0f} px par kg éq. CO₂/m² : plafonds de "
                         f"{bats[0]['plafond']:.0f}, {bats[1]['plafond']:.0f} et "
                         f"{bats[2]['plafond']:.0f} px, remplissages de "
                         f"{bats[0]['resultat']:.0f}, {bats[1]['resultat']:.0f} et "
                         f"{bats[2]['resultat']:.0f} px — texte masqué, la chute "
                         "du plafond au double trait et le seuil prolongé que les "
                         "remplissages du gaz dépassent portent la thèse",
        "topologie": f"colonne bâtiment (x {MARGE}–{MARGE + P_LIB_DISPO}) → "
                     f"pistes (x {P_X0}–{P_X0 + bats[1]['plafond'] * P_K:.0f}) ; "
                     f"frontière à double trait y 488–492, seuil prolongé à "
                     f"x {guide_x:.1f}",
        "cellules": f"{bats[0]['cellules']} + {bats[1]['cellules']} + "
                    f"{bats[2]['cellules']} = "
                    f"{sum(b['cellules'] for b in bats)} logements — la géométrie "
                    "code le nombre, jamais la surface",
        "bas_du_dessin": f"rangs A/B/C jusqu’à {bas_a:.0f}, {bas_b:.0f} et "
                         f"{bas_c:.0f} px, seuil prolongé jusqu’à "
                         f"{y_c + 6 + P_H + 14:.0f}, phrase de principe à 688, "
                         f"cartouche 714–744, marge basse {H - 744} px",
        "reserve_profonde": f"cartouche {largeur} x 30 px = {largeur * 30} px², "
                            f"soit {largeur * 30 / (W * H) * 100:.2f} % de la planche",
        "chiffre_unique": "aucun chiffre de relevé — les six valeurs des pistes "
                          "sont des cotes mono 10 et 12 (révision 4)",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l’échelle "
                         f"0,96 (1152 / {W})",
        "phrase_principe": f"{len(donnees['phrase_principe'])} signes — "
                           f"{l_phrase:.0f} px mesurés pour {UTILE} disponibles",
        "depassements": " ; ".join(depassements) if depassements
                        else "aucun — toutes les lignes mesurées sous leur colonne",
    }
    return "\n".join(out) + "\n", controles


def composer_vignette_plafonds(donnees):
    """La vignette : les trois pistes et la frontière, sans l'appareil.

    Ce qu'elle garde : la géométrie des pistes à échelle commune, le double
    trait de la frontière, le seuil prolongé, et les couples résultat / plafond.
    Ce qu'elle laisse : les cellules de logements, les compositions, les détails
    de générateur, la légende des signes — six libellés dans 300 px ne se
    lisent pas."""
    bats = _batiments(donnees)
    k = (VW - 2 * V_MARGE) / max(b["plafond"] for b in bats)
    x0 = float(V_MARGE)

    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false" '
      f'style="width:100%;height:auto;display:block">')
    A("<style>")
    for cle, hexa in JETON.items():
        A(f"  .c-{cle} {{ fill: var(--color-{cle}, {hexa}); }}")
    A(f'  .s-filet1 {{ stroke: var(--color-filet-1, {JETON["filet-1"]}); }}')
    A(f'  .s-encre {{ stroke: var(--color-encre, {JETON["encre"]}); }}')
    A(f"  .t-sans {{ font-family: {SANS}; }}")
    A(f"  .t-mono {{ font-family: {MONO}; }}")
    A("</style>")
    A(rect(0, 0, VW, VH, "papier"))
    A(texte(V_MARGE, 22, donnees["vignette_surtitre"], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    def v_rang(e, y_lbl):
        A(texte(x0, y_lbl, f'{e["nom"]} — {e["generateur_court"]}', "sans", 12,
                600, "encre", wdth=112))
        A(texte(VW - V_MARGE, y_lbl, e["valeur"], "mono", 10, 500, "pivot",
                ancre="end", tabulaire=True))
        A(rect_bord(x0, y_lbl + 6, e["plafond"] * k, 12, "papier", "filet-1"))
        A(rect_bord(x0, y_lbl + 6, e["resultat"] * k, 12, "clair", "filet-1"))

    v_rang(bats[0], 44)
    v_rang(bats[1], 78)
    A(ligne(x0, 104, VW - V_MARGE, 104, "encre"))
    A(ligne(x0, 107, VW - V_MARGE, 107, "encre"))
    A(texte(x0, 121, "LA FRONTIÈRE RE2020", "mono", 9, 500, "pivot",
            tracking=9 * 0.14))
    v_rang(bats[2], 140)

    # Le seuil des accolées, en marques de coupe sur les seules pistes (et sur
    # la frontière) : un trait continu traverserait les libellés pleine largeur.
    guide_x = x0 + bats[2]["plafond"] * k
    for y0g, y1g in ((47, 65), (81, 99), (101, 110), (143, 161)):
        A(ligne(guide_x, y0g, guide_x, y1g, "encre"))

    A("</svg>")
    controles = {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": "carte de projet mesurée de 274 à 296 px — "
                            f"échelle {274/VW:.2f} à {296/VW:.2f}",
        "corps_minimal": f"9 px dans le repère — rendu à {9*274/VW:.1f} px au pire cas",
        "motif": "trois pistes à échelle commune, le double trait de la "
                 "frontière, le seuil prolongé et les couples résultat / "
                 "plafond — cellules, compositions et légende laissées à la planche",
        "bas_du_dessin": "piste C jusqu’à 158 px, marge basse "
                         f"{VH - 158} px",
    }
    return "\n".join(out) + "\n", controles


def composer_appui_plafonds(donnees):
    """L'appui du hero : le motif entier à l'échelle 1, densité intermédiaire.

    Ce qu'il garde : les trois pistes, la frontière à double trait et sa
    mention, le seuil prolongé, les couples résultat / plafond et la légende
    des deux signes. Ce qu'il laisse : les cellules, les compositions et les
    détails de générateur — ils vivent sur la planche."""
    p = donnees["plafonds"]
    bats = _batiments(donnees)
    fr = _frontiere(donnees)
    k = (AW - 2 * A_MARGE) / max(b["plafond"] for b in bats)
    x0 = float(A_MARGE)

    out = []
    A = out.append
    racine_appui(A, donnees, strokes=("filet-1", "encre"))

    def a_rang(e, y_lbl):
        A(texte(x0, y_lbl, f'{e["nom"]} — {e["generateur_court"]}', "sans", 14,
                600, "encre", wdth=112))
        A(texte(AW - A_MARGE, y_lbl, e["valeur"], "mono", 11, 500, "pivot",
                ancre="end", tabulaire=True))
        A(rect_bord(x0, y_lbl + 8, e["plafond"] * k, 18, "papier", "filet-1"))
        A(rect_bord(x0, y_lbl + 8, e["resultat"] * k, 18, "clair", "filet-1"))

    a_rang(bats[0], 78)
    a_rang(bats[1], 132)
    A(ligne(x0, 172, AW - A_MARGE, 172, "encre"))
    A(ligne(x0, 176, AW - A_MARGE, 176, "encre"))
    A(texte(x0, 196, f'{fr["detail"][1]}', "mono", 10, 500, "encre",
            tracking=1.4))
    a_rang(bats[2], 220)

    # Marques de coupe plutôt que trait continu : voir la vignette.
    guide_x = x0 + bats[2]["plafond"] * k
    for y0g, y1g in ((82, 108), (136, 162), (166, 182), (224, 250)):
        A(ligne(guide_x, y0g, guide_x, y1g, "encre"))

    lx = x0
    A(rect_bord(lx, 288, 16, 9, "clair", "filet-1"))
    lx += 23
    A(texte(lx, 296, p["legende_resultat"], "mono", 10, 500, "pivot",
            tracking=1.4))
    lx += mesurer(p["legende_resultat"], 10, "mono", 1.4) + 26
    A(rect_bord(lx, 288, 16, 9, "papier", "filet-1"))
    lx += 23
    A(texte(lx, 296, "PLAFOND MODULÉ", "mono", 10, 500, "pivot",
            tracking=1.4))
    A(texte(AW - A_MARGE, 296, f'IC ÉNERGIE · {p["unite"]}', "mono", 10, 500,
            "pivot", tracking=1.4, ancre="end"))

    A("</svg>")
    return "\n".join(out) + "\n", controles_appui(
        motif="les trois pistes à l’échelle 1, la frontière à double trait et "
              "sa mention, le seuil prolongé, les couples résultat / plafond "
              "et la légende des deux signes — cellules, compositions et "
              "détails de générateur laissés à la planche",
        bas="légende jusqu’à 296 px, marge basse 72 px")


# ═══════════════════════════════════════════════════════════════════════════════
# Mécanisme `dedoublement` — une opération, deux marchés, un seul BET fluides
# (logements Néréa, Aytré). Même famille que le Sankey : la proportion portée
# par la géométrie. Un permis unique (une barre d'origine contiguë) se partage
# en deux marchés (trois rubans à 3 px par logement : 42, puis 30 + 18), qui
# arrivent sur deux barres segmentées — cinq bâtiments comptés. Une bande
# calcaire UNIQUE traverse les deux flux : le BET fluides commun aux deux
# maîtres d'ouvrage. Texte masqué : une pile qui fourche en deux rubans
# inégaux, une colonne qui les traverse tous les deux, deux arrivées en 2 + 3.
# ═══════════════════════════════════════════════════════════════════════════════

DD_LIB_W = 330             # largeur de la colonne de libellés
DD_BAR_X = 398             # barre du permis (9 px)
DD_X0 = DD_BAR_X + 9       # départ des rubans
DD_X1 = 860                # barres d'arrivée (9 px)
DD_LETTRE_X = 877          # lettres de bâtiment
DD_NLIB_X = 895            # étiquettes d'arrivée — jusqu'à 1144
DD_PXL = 3.0               # px par logement — l'échelle EST la donnée
DD_Y0 = 262.0              # haut de la barre d'origine
DD_ECART = 30.0            # divergence des groupes à l'arrivée
DD_BANDE = (560.0, 710.0)  # la bande du BET, x0-x1
DD_BANDE_DEBORD = 26.0     # débord de la bande au-delà des arrivées


def _ruban(x0, x1, y0g, y1g, y0d, y1d):
    """Ruban de flux : mêmes cubiques symétriques que le Sankey de flux."""
    xm = (x0 + x1) / 2
    d = (f"M {x0:.2f} {y0g:.2f} "
         f"C {xm:.2f} {y0g:.2f}, {xm:.2f} {y0d:.2f}, {x1:.2f} {y0d:.2f} "
         f"L {x1:.2f} {y1d:.2f} "
         f"C {xm:.2f} {y1d:.2f}, {xm:.2f} {y1g:.2f}, {x0:.2f} {y1g:.2f} Z")
    return (f'  <path d="{d}" class="c-clair s-filet1" fill="{JETON["clair"]}" '
            f'stroke="{JETON["filet-1"]}" stroke-width="1"/>')


def _dd_geometrie(donnees, pxl, y0, ecart):
    """Origines contiguës (le permis est UN), arrivées divergentes par marché."""
    dd = donnees["dedoublement"]
    y = float(y0)
    poses = []
    for f in dd["flux"]:
        h = f["logements"] * pxl
        poses.append({"f": f, "o0": y, "o1": y + h, "h": h})
        y += h
    groupes = []
    for a in dd["arrivees"]:
        membres = [p for p in poses if p["f"]["marche"] == a["cle"]]
        g0 = membres[0]["o0"] + (-ecart if not groupes else ecart)
        yg = g0
        for p in membres:
            p["a0"], p["a1"] = yg, yg + p["h"]
            yg += p["h"]
        groupes.append({"a": a, "y0": g0, "h": yg - g0, "centre": (g0 + yg) / 2})
    return dd, poses, groupes, y  # y = bas de la barre d'origine


def _dd_segments(A, x, y0, h, batiments, lettre_x, lettre_corps=10, gap=3.0):
    """La barre d'arrivée, découpée en bâtiments COMPTÉS (jamais dimensionnés)."""
    n = len(batiments)
    seg = (h - gap * (n - 1)) / n
    for i, b in enumerate(batiments):
        ys = y0 + i * (seg + gap)
        A(rect(x, ys, 9, seg, "encre"))
        A(texte(lettre_x, ys + seg / 2 + lettre_corps * 0.36, b, "mono",
                lettre_corps, 500, "pivot"))


def composer_dedoublement(donnees):
    dd, poses, groupes, bas_barre = _dd_geometrie(donnees, DD_PXL, DD_Y0, DD_ECART)
    bx0, bx1 = DD_BANDE
    bcx = (bx0 + bx1) / 2
    haut_arrivees = min(g["y0"] for g in groupes)
    bas_arrivees = max(g["y0"] + g["h"] for g in groupes)
    bande_y0 = haut_arrivees - DD_BANDE_DEBORD
    bande_y1 = bas_arrivees + DD_BANDE_DEBORD
    depassements = []

    def controler(nom, contenu, corps, profil, dispo, tracking=0.0):
        l = mesurer(contenu, corps, profil, tracking)
        if l > dispo:
            depassements.append(f"{nom} : {l:.0f} px pour {dispo:.0f} disponibles")
        return l

    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
      f'preserveAspectRatio="xMidYMid meet" role="img" '
      f'style="width:100%;height:auto;display:block" '
      f'aria-label="{echapper(donnees["aria_label"])}">')
    entete_style(A, strokes=("filet-1", "filet-2", "encre"))
    A(rect(0, 0, W, H, "papier"))

    # ── Bloc de titre ────────────────────────────────────────────────────────
    A(texte(MARGE, 76, donnees["surtitre"], "mono", 11, 500, "pivot",
            tracking=11 * 0.14))
    A(texte(MARGE, 112, donnees["titre"], "sans", 30, 700, "encre", wdth=112))
    A(texte(MARGE, 138, donnees["sous_titre"], "sans", 16, 400, "pivot", wdth=100))
    A(rect(MARGE, 160, UTILE, 1, "filet-1"))

    # ── En-tête de périmètre ─────────────────────────────────────────────────
    controler("entête", dd["entete"], 10, "mono", UTILE, 1.4)
    A(texte(MARGE, 190, dd["entete"], "mono", 10, 500, "pivot", tracking=1.4))

    # ── La bande du BET — dessinée SOUS les rubans : elle les traverse ───────
    A(rect_bord(bx0, bande_y0, bx1 - bx0, bande_y1 - bande_y0,
                "calcaire", "filet-2"))

    # ── Les rubans — un permis contigu qui fourche en deux marchés ───────────
    for p in poses:
        A(_ruban(DD_X0, DD_X1, p["o0"], p["o1"], p["a0"], p["a1"]))

    # Les arêtes de la bande, REDESSINÉES par-dessus les rubans : la colonne
    # doit se lire en train de traverser les flux, pas seulement en déborder.
    A(ligne(bx0, bande_y0, bx0, bande_y1, "filet-1"))
    A(ligne(bx1, bande_y0, bx1, bande_y1, "filet-1"))

    # ── La barre du permis — l'origine est UNE ───────────────────────────────
    A(rect(DD_BAR_X, DD_Y0, 9, bas_barre - DD_Y0, "encre"))
    for i, ligne_permis in enumerate(dd["permis"]["lignes"]):
        controler("permis", ligne_permis, 10, "mono", 300, 1.4)
        A(texte(DD_BAR_X + 4.5, 556 + i * 14, ligne_permis, "mono", 10, 500,
                "encre" if i == 0 else "pivot", ancre="middle", tracking=1.4))

    # ── Libellés de flux, à gauche — jamais posés sur le clair ───────────────
    for p in poses:
        f = p["f"]
        lignes = replier(f["libelle"], 15, DD_LIB_W)
        for l in lignes:
            controler(f'libellé {f["cle"]}', l, 15, "sans-400", DD_LIB_W)
        total_h = len(lignes) * 17 + 13
        yl = (p["o0"] + p["o1"]) / 2 - total_h / 2 + 12
        for k, l in enumerate(lignes):
            A(texte(MARGE, yl + k * 17, l, "sans", 15, 400, "encre", wdth=100))
        controler(f'marché {f["cle"]}', f["marche_mention"], 10, "mono",
                  DD_LIB_W, 1.4)
        A(texte(MARGE, yl + len(lignes) * 17 + 13 - 4, f["marche_mention"],
                "mono", 10, 500, "pivot", tracking=1.4))

    # ── Arrivées : barres segmentées (bâtiments comptés) + étiquettes ────────
    nlib_dispo = W - MARGE - DD_NLIB_X
    for g in groupes:
        a = g["a"]
        _dd_segments(A, DD_X1, g["y0"], g["h"], a["batiments"], DD_LETTRE_X)
        c = g["centre"]
        controler(f'nom {a["cle"]}', a["nom"], 15, "sans-600", nlib_dispo)
        A(texte(DD_NLIB_X, c - 22, a["nom"], "sans", 15, 600, "encre", wdth=112))
        controler(f'valeur {a["cle"]}', a["valeur_mention"], 10, "mono",
                  nlib_dispo, 1.4)
        A(texte(DD_NLIB_X, c - 4, a["valeur_mention"], "mono", 10, 500, "encre",
                tracking=1.4))
        for k, lc in enumerate(a["certification"]):
            controler(f'certification {a["cle"]}', lc, 10, "mono", nlib_dispo, 1.4)
            A(texte(DD_NLIB_X, c + 14 + k * 14, lc, "mono", 10, 500, "pivot",
                    tracking=1.4))

    # ── La bande, nommée sous elle — le signe est toujours doublé d'un texte ─
    A(ligne(bcx, bande_y1, bcx, bande_y1 + 10, "encre"))
    l_bande = controler("bande", dd["bande_bet"]["libelle"], 10, "mono", 700, 1.4)
    A(texte(bcx, bande_y1 + 24, dd["bande_bet"]["libelle"], "mono", 10, 500,
            "encre", ancre="middle", tracking=1.4))
    l_csq = controler("conséquence", dd["bande_bet"]["consequence"], 10, "mono",
                      UTILE, 1.4)
    A(texte(bcx, bande_y1 + 40, dd["bande_bet"]["consequence"], "mono", 10, 500,
            "pivot", ancre="middle", tracking=1.4))

    # ── Phrase de principe, pleine largeur ───────────────────────────────────
    l_phrase = controler("phrase de principe", donnees["phrase_principe"], 17,
                         "sans-400", UTILE)
    A(texte(MARGE, 688, donnees["phrase_principe"], "sans", 17, 400, "encre",
            wdth=100))

    # ── Cartouche — largeur ajustée au texte, jamais codée ───────────────────
    libelle = donnees["cartouche_legende"]
    largeur = min(600, round(mesurer(libelle, 11, "mono", 11 * 0.14) + 40))
    A(rect(MARGE, 714, largeur, 30, "profond"))
    A(texte(MARGE + 20, 734, libelle, "mono", 11, 500, "voile",
            tracking=11 * 0.14))

    A("</svg>")

    total = sum(p["f"]["logements"] for p in poses)
    controles = {
        "gabarit": f"{W} x {H} — rapport {W/H:.4f} (3:2 exact)",
        "demonstration": f"une barre d’origine contiguë de {bas_barre - DD_Y0:.0f} px "
                         f"(90 logements à {DD_PXL:.0f} px) qui fourche en deux "
                         f"groupes divergents de ±{DD_ECART:.0f} px, traversés par "
                         f"une bande calcaire unique (x {bx0:.0f}–{bx1:.0f}) — "
                         "texte masqué, la fourche inégale, la colonne qui "
                         "traverse les deux flux et les arrivées en 2 + 3 "
                         "segments portent la thèse",
        "bouclage_rubans": " + ".join(str(p["f"]["logements"]) for p in poses)
                           + f" = {total} logements ; hauteurs "
                           + " + ".join(f'{p["h"]:.0f}' for p in poses)
                           + f" = {sum(p['h'] for p in poses):.0f} px",
        "topologie": f"libellés (x {MARGE}–{MARGE + DD_LIB_W}) → permis "
                     f"(x {DD_BAR_X}) → rubans (x {DD_X0}–{DD_X1}) → arrivées "
                     f"segmentées + étiquettes (x {DD_NLIB_X}–{W - MARGE}) ; "
                     f"bande du BET x {bx0:.0f}–{bx1:.0f}, y {bande_y0:.0f}–"
                     f"{bande_y1:.0f}",
        "segments": " + ".join(str(len(g["a"]["batiments"])) for g in groupes)
                    + " = 5 bâtiments — la géométrie code le nombre, jamais "
                      "la contenance",
        "bas_du_dessin": f"arrivées jusqu’à {bas_arrivees:.0f} px, bande nommée à "
                         f"{bande_y1 + 24:.0f} et {bande_y1 + 40:.0f}, phrase de "
                         f"principe à 688, cartouche 714–744, marge basse "
                         f"{H - 744} px",
        "reserve_profonde": f"cartouche {largeur} x 30 px = {largeur * 30} px², "
                            f"soit {largeur * 30 / (W * H) * 100:.2f} % de la planche",
        "chiffre_unique": "aucun chiffre de relevé — les comptes des flux sont "
                          "des libellés Archivo 15 et des cotes mono 10 "
                          "(révision 4)",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l’échelle "
                         f"0,96 (1152 / {W})",
        "phrase_principe": f"{len(donnees['phrase_principe'])} signes — "
                           f"{l_phrase:.0f} px mesurés pour {UTILE} disponibles",
        "etiquette_bande": f"{l_bande:.0f} px centrés sur x {bcx:.0f} — de "
                           f"{bcx - l_bande/2:.0f} à {bcx + l_bande/2:.0f}, "
                           f"conséquence {l_csq:.0f} px",
        "depassements": " ; ".join(depassements) if depassements
                        else "aucun — toutes les lignes mesurées sous leur colonne",
    }
    return "\n".join(out) + "\n", controles


def composer_vignette_dedoublement(donnees):
    """La vignette : la fourche, la bande et les deux totaux, sans l'appareil.

    Ce qu'elle garde : la barre d'origine, les trois rubans proportionnels, la
    bande unique nommée, les deux arrivées avec leur total. Ce qu'elle laisse :
    les libellés de flux, les certifications, les lettres de bâtiment, le
    permis — six libellés dans 300 px ne se lisent pas."""
    pxl, y0, ecart = 0.9, 48.0, 10.0
    dd, poses, groupes, bas_barre = _dd_geometrie(donnees, pxl, y0, ecart)
    x_bar, x0, x1, x_lib = 20.0, 26.0, 218.0, 230.0
    bx0, bx1 = 103.0, 141.0
    haut = min(g["y0"] for g in groupes)
    bas = max(g["y0"] + g["h"] for g in groupes)
    vb_y0, vb_y1 = haut - 10, bas + 10

    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false" '
      f'style="width:100%;height:auto;display:block">')
    entete_style(A, strokes=("filet-1", "filet-2", "encre"))
    A(rect(0, 0, VW, VH, "papier"))
    A(texte(V_MARGE, 22, donnees["vignette_surtitre"], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    A(rect_bord(bx0, vb_y0, bx1 - bx0, vb_y1 - vb_y0, "calcaire", "filet-2"))
    for p in poses:
        A(_ruban(x0, x1, p["o0"], p["o1"], p["a0"], p["a1"]))
    A(ligne(bx0, vb_y0, bx0, vb_y1, "filet-1"))
    A(ligne(bx1, vb_y0, bx1, vb_y1, "filet-1"))
    A(rect(x_bar, y0, 6, bas_barre - y0, "encre"))
    for g in groupes:
        A(rect(x1, g["y0"], 6, g["h"], "encre"))
        c = g["centre"]
        A(texte(x_lib, c - 3, g["a"]["nom_court"], "sans", 12, 600, "encre",
                wdth=112))
        A(texte(x_lib, c + 11, g["a"]["total_affiche"], "mono", 10, 500, "pivot",
                tabulaire=True))
    A(texte((bx0 + bx1) / 2, 168, dd["bande_bet"]["libelle_court"], "mono", 9,
            500, "encre", ancre="middle", tracking=9 * 0.14))

    A("</svg>")
    controles = {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": "carte de projet mesurée de 274 à 296 px — "
                            f"échelle {274/VW:.2f} à {296/VW:.2f}",
        "corps_minimal": f"9 px dans le repère — rendu à {9*274/VW:.1f} px au pire cas",
        "motif": "la barre d’origine, les trois rubans proportionnels, la bande "
                 "unique nommée et les deux arrivées avec leur total — libellés "
                 "de flux, certifications et permis laissés à la planche",
        "bas_du_dessin": f"bande nommée à 168 px, marge basse {VH - 168} px",
    }
    return "\n".join(out) + "\n", controles


def composer_appui_dedoublement(donnees):
    """L'appui du hero : le motif entier à l'échelle 1, densité intermédiaire.

    Ce qu'il garde : la fourche complète avec ses trois comptes (42, 30, 18),
    la bande unique nommée, les cinq bâtiments en segments lettrés, le permis
    et la ligne de résumé. Ce qu'il laisse : les libellés de flux et les
    certifications — ils vivent sur la planche."""
    pxl, y0, ecart = 1.6, 100.0, 12.0
    dd, poses, groupes, bas_barre = _dd_geometrie(donnees, pxl, y0, ecart)
    x_bar, x0, x1 = 64.0, 72.0, 420.0
    bx0, bx1 = 220.0, 300.0
    bcx = (bx0 + bx1) / 2
    haut = min(g["y0"] for g in groupes)
    bas = max(g["y0"] + g["h"] for g in groupes)
    ab_y0, ab_y1 = haut - 20, bas + 20

    out = []
    A = out.append
    racine_appui(A, donnees, strokes=("filet-1", "filet-2", "encre"))

    A(rect_bord(bx0, ab_y0, bx1 - bx0, ab_y1 - ab_y0, "calcaire", "filet-2"))
    for p in poses:
        A(_ruban(x0, x1, p["o0"], p["o1"], p["a0"], p["a1"]))
    A(ligne(bx0, ab_y0, bx0, ab_y1, "filet-1"))
    A(ligne(bx1, ab_y0, bx1, ab_y1, "filet-1"))
    A(rect(x_bar, y0, 8, bas_barre - y0, "encre"))
    for p in poses:
        A(texte(56, (p["o0"] + p["o1"]) / 2 + 4, str(p["f"]["logements"]),
                "mono", 11, 500, "pivot", ancre="end", tabulaire=True))
    for g in groupes:
        _dd_segments(A, x1, g["y0"], g["h"], g["a"]["batiments"], 434,
                     lettre_corps=10)
    for i, ligne_permis in enumerate(dd["permis"]["lignes"]):
        A(texte(A_MARGE, 258 + i * 14, ligne_permis, "mono", 10, 500,
                "encre" if i == 0 else "pivot", tracking=1.4))
    A(texte(bcx, 292, dd["bande_bet"]["libelle_court"], "mono", 10, 500,
            "encre", ancre="middle", tracking=1.4))
    A(texte(A_MARGE, 330, dd["appui_resume"], "mono", 10, 500, "pivot",
            tracking=1.4))

    A("</svg>")
    return "\n".join(out) + "\n", controles_appui(
        motif="la fourche complète à l’échelle 1 avec ses trois comptes, la "
              "bande unique nommée, les cinq bâtiments en segments lettrés, "
              "le permis et la ligne de résumé — libellés de flux et "
              "certifications laissés à la planche",
        bas="ligne de résumé à 330 px, marge basse 38 px")


# ═══════════════════════════════════════════════════════════════════════════════
# Mécanisme `bascule` — la grandeur qui change de signe (résidence
# intergénérationnelle, Saint-Agnant). Même famille que le Sankey : une
# proportion portée par la géométrie, sur une échelle qui EST la donnée. Mais
# aucun des trois mécanismes précédents ne connaît le passage sous zéro.
#
# Ce qui se passe : une production entre dans UNE zone de calcul — un dixième de
# la surface de l'opération, et la largeur des deux bandes le dit —, et le bilan
# d'énergie primaire de cette zone tombe de l'autre côté du zéro.
#
# Trois lignes pleine largeur ordonnent la planche : le plafond, le zéro, le
# bilan. Entre les deux premières, la BANDE AUTORISÉE en calcaire — tout ce que
# le plafond laisse consommer à la zone. Entre les deux dernières, la profondeur
# atteinte, où pend la seule colonne de la zone concernée. Les deux hauteurs
# sont à la même échelle : c'est leur rapport qui démontre, et il se mesure à la
# règle sur la planche.
#
# L'ORIGINE DE L'ÉCHELLE EST LE ZÉRO, PAS LE PLAFOND — leçon de la planche 19 :
# l'origine se choisit à la question que le dessin pose. Ici « de combien la
# production dépasse-t-elle le besoin ? ». Graduée depuis le plafond, la bande
# autorisée tomberait à 24 % de la hauteur du cadre.
#
# Texte masqué : un bloc en haut à gauche, une flèche qui traverse la planche et
# plonge dans le dixième droit d'une bande large, une mince bande claire, et une
# colonne qui pend deux fois et demie plus bas.
# ═══════════════════════════════════════════════════════════════════════════════

BC_SRC_Y0, BC_SRC_H = 208.0, 72.0     # le bloc de la source
BC_SRC_PAD = 14.0
BC_ROUTE_Y = 244.0                    # la route de la production
BC_TAG_Z1_Y = 300.0                   # tag de la zone 1, au-dessus de la bande
BC_BANDE_Y0, BC_BANDE_H = 310.0, 48.0 # la bande de l'opération, deux zones
BC_TAG_AXE_Y = 374.0                  # tag d'axe (g.) et tag de la zone 2 (d.)
BC_SEUIL_Y = 392.0                    # la ligne du plafond
BC_BILAN_Y = 648.0                    # la ligne du bilan
BC_PHRASE_Y = 688.0
BC_CARTOUCHE_Y, BC_CARTOUCHE_H = 714.0, 30.0


def _bc_elements(donnees, type_):
    return [e for e in donnees["bascule"]["elements"] if e.get("type") == type_]


def _bc_echelle(donnees, y_seuil, y_bilan):
    """L'échelle est DÉRIVÉE des deux niveaux de l'extraction, jamais choisie :
    px par kWhep/m²/an, origine au zéro."""
    seuil = _bc_elements(donnees, "seuil")[0]["niveau"]
    bilan = _bc_elements(donnees, "bilan")[0]["niveau"]
    k = (y_bilan - y_seuil) / (seuil - bilan)
    return seuil, bilan, k, y_seuil + seuil * k


def _bc_zones(donnees, x0, largeur):
    """Les deux zones, à largeur PROPORTIONNELLE À LEUR SURFACE. La géométrie
    code la surface en largeur ; la hauteur, elle, n'appartient qu'à l'axe."""
    zones = _bc_elements(donnees, "zone")
    total = sum(z["surface"] for z in zones)
    x = float(x0)
    poses = []
    for z in zones:
        w = largeur * z["surface"] / total
        poses.append({"z": z, "x0": x, "x1": x + w, "w": w, "part": z["surface"] / total})
        x += w
    return poses, total


def composer_bascule(donnees):
    bc = donnees["bascule"]
    seuil, bilan, k, y_zero = _bc_echelle(donnees, BC_SEUIL_Y, BC_BILAN_Y)
    poses, surface_totale = _bc_zones(donnees, MARGE, UTILE)
    pose_bilan = next(p for p in poses if p["z"]["cle"] == bc["zone_du_bilan"])
    x_route = (pose_bilan["x0"] + pose_bilan["x1"]) / 2
    src = _bc_elements(donnees, "source")[0]
    seuil_e = _bc_elements(donnees, "seuil")[0]
    bilan_e = _bc_elements(donnees, "bilan")[0]

    depassements = []

    def controler(nom, chaine, corps, profil, dispo, tracking=0.0):
        l = mesurer(chaine, corps, profil, tracking)
        if l > dispo:
            depassements.append(f"{nom} : {l:.0f} px pour {dispo:.0f} disponibles")
        return l

    def mono(x, y, chaine, dispo=None, nom=None, ancre=None, couleur="pivot",
             corps=10):
        if dispo is not None:
            controler(nom or chaine, chaine, corps, "mono", dispo, corps * 0.14)
        A(texte(x, y, chaine, "mono", corps, 500, couleur, ancre=ancre,
                tracking=corps * 0.14))

    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
      f'preserveAspectRatio="xMidYMid meet" role="img" '
      f'style="width:100%;height:auto;display:block" '
      f'aria-label="{echapper(donnees["aria_label"])}">')
    entete_style(A, strokes=("filet-1", "filet-3", "encre"))
    A(rect(0, 0, W, H, "papier"))

    # ── Bloc de titre ────────────────────────────────────────────────────────
    A(texte(MARGE, 76, donnees["surtitre"], "mono", 11, 500, "pivot",
            tracking=11 * 0.14))
    A(texte(MARGE, 112, donnees["titre"], "sans", 30, 700, "encre", wdth=112))
    A(texte(MARGE, 138, donnees["sous_titre"], "sans", 16, 400, "pivot", wdth=100))
    A(rect(MARGE, 160, UTILE, 1, "filet-1"))

    # ── En-tête de périmètre — il empêche la planche de mentir ───────────────
    mono(MARGE, 190, bc["entete"], UTILE, "entête")

    # ── La source : le lot détaché, un seul bloc — sa topologie interne n'est
    #    pas à la fiche, et un bloc sans détail vaut mieux qu'un détail inventé.
    src_w = max(mesurer(src["libelle"], 15, "sans-400"),
                max(mesurer(d, 10, "mono", 1.4) for d in src["detail"])) + 2 * BC_SRC_PAD
    src_x1 = MARGE + src_w
    A(rect_bord(MARGE, BC_SRC_Y0, src_w, BC_SRC_H, "papier", "filet-1"))
    A(texte(MARGE + BC_SRC_PAD, BC_SRC_Y0 + 24, src["libelle"], "sans", 15, 400,
            "encre", wdth=100))
    for i, d in enumerate(src["detail"]):
        mono(MARGE + BC_SRC_PAD, BC_SRC_Y0 + 44 + i * 16, d)

    # ── La route de la production — elle n'entre que dans UNE zone ───────────
    A(ligne(src_x1, BC_ROUTE_Y, x_route, BC_ROUTE_Y, "encre", 1.5))
    A(ligne(x_route, BC_ROUTE_Y, x_route, BC_BANDE_Y0 - 10, "encre", 1.5))
    A(fleche(x_route, BC_BANDE_Y0, "encre", "bas", 10))
    # L'étiquette INTERROMPT la route qu'elle annote (procédé du dessin coté) :
    # posée à côté, elle serait partout au mauvais endroit ; posée dessus sans
    # fond, la ligne la raye. Elle vient donc APRÈS le trait.
    l_route = mesurer(bc["etiquette_route"], 10, "mono", 1.4)
    cx_route = (src_x1 + x_route) / 2
    A(rect(cx_route - l_route / 2 - 8, BC_ROUTE_Y - 12, l_route + 16, 18, "papier"))
    mono(cx_route, BC_ROUTE_Y, bc["etiquette_route"], x_route - src_x1 - 20,
         "étiquette de route", ancre="middle")

    # ── La bande de l'opération : deux zones à largeur proportionnelle ───────
    z1 = poses[0]
    mono(MARGE, BC_TAG_Z1_Y, z1["z"]["tag"], z1["w"], "tag zone 1")
    for p in poses:
        porte = p is pose_bilan
        A(rect_bord(p["x0"], BC_BANDE_Y0, p["w"], BC_BANDE_H,
                    "clair" if porte else "papier", "filet-1"))
    for i, d in enumerate(z1["z"]["detail"]):
        mono(z1["x0"] + BC_SRC_PAD, BC_BANDE_Y0 + 18 + i * 18, d,
             z1["w"] - 2 * BC_SRC_PAD, f"détail zone 1 {i}")
    mono(W - MARGE, BC_TAG_AXE_Y, pose_bilan["z"]["tag"], 420, "tag zone 2",
         ancre="end")
    mono(MARGE, BC_TAG_AXE_Y, bc["tag_axe"], 420, "tag d’axe")

    # ── Les filets de projection : la colonne de la zone descend sur l'axe ───
    for x in (pose_bilan["x0"], pose_bilan["x1"]):
        A(ligne(x, BC_BANDE_Y0 + BC_BANDE_H, x, BC_SEUIL_Y, "filet-1", 1))

    # ── Les trois lignes de l'axe, en PLEINE LARGEUR — plafond, zéro, bilan.
    #    Les deux HAUTEURS, elles, sont confinées à la colonne de la zone : une
    #    bande pleine largeur et une colonne étroite ne se comparent pas à l'œil,
    #    et c'est leur rapport qui démontre. Défaut relevé au rendu à 1152 px.
    x_lib = pose_bilan["x0"] - 16          # les légendes butent contre la colonne
    h_bande = y_zero - BC_SEUIL_Y
    A(ligne(MARGE, BC_SEUIL_Y, W - MARGE, BC_SEUIL_Y, "encre", 1))

    # La bande autorisée : du plafond au zéro, dans la colonne de la zone.
    # Bordée : calcaire sur papier vaut 1,05 — une bande non bordée n'existe pas.
    A(rect_bord(pose_bilan["x0"], BC_SEUIL_Y, pose_bilan["w"], h_bande,
                "calcaire", "filet-1"))
    # Les deux légendes de la bande se lisent CONTRE elle, à sa hauteur : posées
    # à gauche sous le tag d'axe, elles se chevauchaient à dix pixels près.
    for i, l in enumerate(bc["legende_bande"]):
        mono(x_lib, BC_SEUIL_Y + 26 + i * 20, l, x_lib - MARGE,
             f"légende de bande {i}", ancre="end")

    # ── Le zéro : le datum de la planche ─────────────────────────────────────
    A(ligne(MARGE, y_zero, W - MARGE, y_zero, "encre", 1.5))
    mono(MARGE, y_zero + 20, bc["mention_zero"], UTILE, "mention du zéro")

    # ── La colonne du bilan : elle pend du zéro à la ligne du bilan ──────────
    A(rect_bord(pose_bilan["x0"], y_zero, pose_bilan["w"], BC_BILAN_Y - y_zero,
                "clair", "filet-1"))
    # Traits au pas du plafond : la profondeur atteinte se COMPTE en bandes
    # autorisées, elle ne se suppose pas. Le signe est doublé de sa mention.
    n_pas = int((BC_BILAN_Y - y_zero) / h_bande)
    for i in range(1, n_pas + 1):
        A(ligne(pose_bilan["x0"], y_zero + i * h_bande,
                pose_bilan["x1"], y_zero + i * h_bande, "filet-1", 1))
    mono(MARGE, y_zero + h_bande + 20, bc["mention_pas"], x_lib - MARGE,
         "mention du pas")
    A(ligne(MARGE, BC_BILAN_Y, W - MARGE, BC_BILAN_Y, "encre", 1))

    # ── Le chiffre du bilan, contre sa colonne — le seul de la planche ───────
    mono(x_lib, BC_BILAN_Y - 128, bc["legende_bilan"], x_lib - MARGE,
         "légende du bilan", ancre="end")
    l_chiffre = mesurer(bilan_e["valeur"], 40, "sans-700")
    l_unite = mesurer(bilan_e["unite"], 15, "sans-400")
    x_chiffre = x_lib - l_chiffre - 10 - l_unite
    A(texte(x_chiffre, BC_BILAN_Y - 48, bilan_e["valeur"], "sans", 40, 700,
            "encre", wdth=118, tabulaire=True))
    A(texte(x_chiffre + l_chiffre + 10, BC_BILAN_Y - 48, bilan_e["unite"],
            "sans", 15, 400, "encre", wdth=100))

    # ── Phrase de principe, pleine largeur ───────────────────────────────────
    l_phrase = controler("phrase de principe", donnees["phrase_principe"], 17,
                         "sans-400", UTILE)
    A(texte(MARGE, BC_PHRASE_Y, donnees["phrase_principe"], "sans", 17, 400,
            "encre", wdth=100))

    # ── Cartouche — largeur ajustée au texte, jamais codée ───────────────────
    libelle = donnees["cartouche_legende"]
    largeur = min(600, round(mesurer(libelle, 11, "mono", 11 * 0.14) + 40))
    A(rect(MARGE, BC_CARTOUCHE_Y, largeur, BC_CARTOUCHE_H, "profond"))
    A(texte(MARGE + 20, BC_CARTOUCHE_Y + 20, libelle, "mono", 11, 500, "voile",
            tracking=11 * 0.14))

    A("</svg>")

    h_bande = y_zero - BC_SEUIL_Y
    h_colonne = BC_BILAN_Y - y_zero
    controles = {
        "gabarit": f"{W} x {H} — rapport {W/H:.4f} (3:2 exact)",
        "demonstration": f"bande autorisée {h_bande:.1f} px ({seuil:.0f} unités) "
                         f"contre colonne du bilan {h_colonne:.1f} px "
                         f"({-bilan:.1f} unités) — rapport {h_colonne/h_bande:.2f}, "
                         f"soit celui des deux valeurs ({-bilan/seuil:.2f}). Texte "
                         "masqué : une flèche qui plonge dans le dixième droit "
                         "d’une bande large, une mince bande claire, une colonne "
                         "qui pend deux fois et demie plus bas",
        "echelle": f"{k:.5f} px par {bc['unite']} — origine AU ZÉRO "
                   f"(y {y_zero:.2f}), plafond +{seuil:.0f} à y {BC_SEUIL_Y:.0f}, "
                   f"bilan {bilan:.1f} à y {BC_BILAN_Y:.0f} ; graduée depuis le "
                   f"plafond, la bande autorisée tomberait à "
                   f"{seuil/(seuil-bilan)*100:.0f} % de la hauteur (leçon de la "
                   "planche 19)",
        "proportion_des_zones": " + ".join(
            f'{p["z"]["cle"]} {p["z"]["surface"]:.2f} m² = {p["w"]:.1f} px '
            f'({p["part"]*100:.1f} %)' for p in poses)
            + f" = {surface_totale:.2f} m² sur {UTILE} px",
        "topologie": f"source (x {MARGE}–{src_x1:.0f}) → route (y {BC_ROUTE_Y:.0f}) "
                     f"→ descente à x {x_route:.1f} → zone 2 "
                     f"(x {pose_bilan['x0']:.1f}–{pose_bilan['x1']:.1f}) → axe ; "
                     f"trois lignes pleine largeur à y {BC_SEUIL_Y:.0f}, "
                     f"{y_zero:.2f} et {BC_BILAN_Y:.0f}",
        "bas_du_dessin": f"ligne du bilan à {BC_BILAN_Y:.0f} px, phrase de principe "
                         f"à {BC_PHRASE_Y:.0f}, cartouche {BC_CARTOUCHE_Y:.0f}–"
                         f"{BC_CARTOUCHE_Y + BC_CARTOUCHE_H:.0f}, marge basse "
                         f"{H - (BC_CARTOUCHE_Y + BC_CARTOUCHE_H):.0f} px",
        "reserve_profonde": f"cartouche {largeur} x {BC_CARTOUCHE_H:.0f} px = "
                            f"{largeur * BC_CARTOUCHE_H:.0f} px², soit "
                            f"{largeur * BC_CARTOUCHE_H / (W * H) * 100:.2f} % "
                            "de la planche",
        "chiffre_unique": f"un seul chiffre de relevé — {bilan_e['valeur']} en "
                          "encre pleine (Archivo 40) ; le plafond "
                          f"{seuil_e['valeur']} est une cote mono 10",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l’échelle 0,96 "
                         f"(1152 / {W})",
        "phrase_principe": f"{len(donnees['phrase_principe'])} signes — "
                           f"{l_phrase:.0f} px mesurés pour {UTILE} disponibles",
        "depassements": " ; ".join(depassements) if depassements
                        else "aucun — toutes les lignes mesurées sous leur colonne",
    }
    return "\n".join(out) + "\n", controles


def composer_vignette_bascule(donnees):
    """La vignette : les trois lignes, la bande autorisée et la colonne.

    Ce qu'elle garde : la partition des deux zones en largeur, la mince bande
    autorisée, le zéro et la colonne qui pend — c'est-à-dire le rapport, qui
    est la thèse. Ce qu'elle laisse : la source et sa route, les détails de
    zone, la mention du zéro, la phrase et le cartouche. Six libellés dans
    300 px ne se lisent pas ; les taire est une décision."""
    bc = donnees["bascule"]
    y_seuil, y_bilan = 78.0, 176.0
    seuil, bilan, k, y_zero = _bc_echelle(donnees, y_seuil, y_bilan)
    largeur = VW - 2 * V_MARGE
    poses, _ = _bc_zones(donnees, V_MARGE, largeur)
    pose_bilan = next(p for p in poses if p["z"]["cle"] == bc["zone_du_bilan"])
    bilan_e = _bc_elements(donnees, "bilan")[0]
    seuil_e = _bc_elements(donnees, "seuil")[0]

    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false" '
      f'style="width:100%;height:auto;display:block">')
    entete_style(A, strokes=("filet-1", "filet-3", "encre"))
    A(rect(0, 0, VW, VH, "papier"))
    A(texte(V_MARGE, 22, donnees["vignette_surtitre"], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    for p in poses:
        A(rect_bord(p["x0"], 42, p["w"], 18,
                    "clair" if p is pose_bilan else "papier", "filet-1"))

    A(texte(V_MARGE, 74, f'PLAFOND {seuil_e["valeur"]}', "mono", 9, 500, "pivot",
            tracking=9 * 0.14))
    # Les deux hauteurs se comparent dans la MÊME colonne — pleine largeur
    # contre colonne étroite, l'œil ne les rapporte pas l'une à l'autre.
    A(rect_bord(pose_bilan["x0"], y_seuil, pose_bilan["w"], y_zero - y_seuil,
                "calcaire", "filet-1"))
    A(ligne(V_MARGE, y_seuil, VW - V_MARGE, y_seuil, "encre", 1))
    A(ligne(V_MARGE, y_zero, VW - V_MARGE, y_zero, "encre", 1.5))
    A(texte(V_MARGE, y_zero - 4, "ZÉRO", "mono", 9, 500, "pivot",
            tracking=9 * 0.14))
    A(rect_bord(pose_bilan["x0"], y_zero, pose_bilan["w"], y_bilan - y_zero,
                "clair", "filet-1"))
    A(ligne(V_MARGE, y_bilan, VW - V_MARGE, y_bilan, "encre", 1))
    A(texte(V_MARGE, y_bilan - 22, "Bilan de la zone", "sans", 12, 600, "encre",
            wdth=112))
    A(texte(V_MARGE, y_bilan - 6, f'{bilan_e["valeur"]}{NN}{bilan_e["unite"]}',
            "mono", 10, 500, "pivot", tabulaire=True))

    A("</svg>")
    controles = {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": "carte de projet mesurée de 274 à 296 px — "
                            f"échelle {274/VW:.2f} à {296/VW:.2f}",
        "corps_minimal": f"9 px dans le repère — rendu à {9*274/VW:.1f} px au pire cas",
        "motif": f"bande autorisée {y_zero - y_seuil:.1f} px contre colonne "
                 f"{y_bilan - y_zero:.1f} px — rapport "
                 f"{(y_bilan - y_zero)/(y_zero - y_seuil):.2f} ; partition des "
                 f"zones {poses[0]['w']:.0f} + {pose_bilan['w']:.0f} px — source, "
                 "route, détails de zone et mention du zéro laissés à la planche",
        "bas_du_dessin": f"ligne du bilan à {y_bilan:.0f} px, marge basse "
                         f"{VH - y_bilan:.0f} px",
    }
    return "\n".join(out) + "\n", controles


def composer_appui_bascule(donnees):
    """L'appui du hero : le motif entier à l'échelle 1, densité intermédiaire.

    Ce qu'il garde : la route de la production, la partition des deux zones, les
    trois lignes, la bande autorisée nommée, la mention du zéro et le chiffre du
    bilan. Ce qu'il laisse : le bloc de la source et ses détails, les détails de
    zone — ils vivent sur la planche."""
    bc = donnees["bascule"]
    y_seuil, y_bilan = 160.0, 330.0
    seuil, bilan, k, y_zero = _bc_echelle(donnees, y_seuil, y_bilan)
    largeur = AW - 2 * A_MARGE
    poses, _ = _bc_zones(donnees, A_MARGE, largeur)
    pose_bilan = next(p for p in poses if p["z"]["cle"] == bc["zone_du_bilan"])
    bilan_e = _bc_elements(donnees, "bilan")[0]
    x_route = (pose_bilan["x0"] + pose_bilan["x1"]) / 2

    out = []
    A = out.append
    racine_appui(A, donnees, strokes=("filet-1", "filet-3", "encre"))

    A(texte(A_MARGE, 62, bc["appui_source"], "mono", 10, 500, "pivot",
            tracking=1.4))
    x_depart = A_MARGE + mesurer(bc["appui_source"], 10, "mono", 1.4) + 14
    A(ligne(x_depart, 76, x_route, 76, "encre", 1.5))
    A(ligne(x_route, 76, x_route, 86, "encre", 1.5))
    A(fleche(x_route, 96, "encre", "bas", 9))

    for p in poses:
        A(rect_bord(p["x0"], 96, p["w"], 28,
                    "clair" if p is pose_bilan else "papier", "filet-1"))
    A(texte(poses[0]["x0"] + 10, 114, bc["appui_zone1"], "mono", 10, 500,
            "pivot", tracking=1.4))
    A(texte(AW - A_MARGE, 140, bc["appui_zone2"], "mono", 10, 500, "pivot",
            ancre="end", tracking=1.4))

    # Les deux légendes de la bande se lisent CONTRE elle, à sa hauteur : posée
    # au-dessus de la ligne du plafond, la première se collait au tag de zone 2.
    x_lib = pose_bilan["x0"] - 12
    A(rect_bord(pose_bilan["x0"], y_seuil, pose_bilan["w"], y_zero - y_seuil,
                "calcaire", "filet-1"))
    A(ligne(A_MARGE, y_seuil, AW - A_MARGE, y_seuil, "encre", 1))
    A(texte(x_lib, y_seuil + 20, bc["legende_bande"][0], "mono", 10, 500,
            "pivot", ancre="end", tracking=1.4))
    A(texte(x_lib, y_seuil + 38, bc["appui_bande"], "mono", 10, 500, "pivot",
            ancre="end", tracking=1.4))
    A(ligne(A_MARGE, y_zero, AW - A_MARGE, y_zero, "encre", 1.5))
    A(texte(A_MARGE, y_zero + 20, bc["appui_zero"], "mono", 10, 500, "pivot",
            tracking=1.4))

    for x in (pose_bilan["x0"], pose_bilan["x1"]):
        A(ligne(x, 124, x, y_seuil, "filet-1", 1))
    A(rect_bord(pose_bilan["x0"], y_zero, pose_bilan["w"], y_bilan - y_zero,
                "clair", "filet-1"))
    # Traits au pas du plafond — la profondeur se compte, ici comme sur la planche.
    h_bande = y_zero - y_seuil
    for i in range(1, int((y_bilan - y_zero) / h_bande) + 1):
        A(ligne(pose_bilan["x0"], y_zero + i * h_bande,
                pose_bilan["x1"], y_zero + i * h_bande, "filet-1", 1))
    A(ligne(A_MARGE, y_bilan, AW - A_MARGE, y_bilan, "encre", 1))

    A(texte(A_MARGE, y_bilan - 44, bc["appui_bilan"], "mono", 10, 500, "pivot",
            tracking=1.4))
    l_chiffre = mesurer(bilan_e["valeur"], 30, "sans-700")
    A(texte(A_MARGE, y_bilan - 10, bilan_e["valeur"], "sans", 30, 700, "encre",
            wdth=118, tabulaire=True))
    A(texte(A_MARGE + l_chiffre + 8, y_bilan - 10, bilan_e["unite"], "sans", 14,
            400, "encre", wdth=100))

    A("</svg>")
    return "\n".join(out) + "\n", controles_appui(
        motif=f"la route de la production, les deux zones à largeur "
              f"proportionnelle ({poses[0]['w']:.0f} + {pose_bilan['w']:.0f} px), "
              f"les trois lignes, la bande autorisée {y_zero - y_seuil:.1f} px "
              f"contre la colonne {y_bilan - y_zero:.1f} px (rapport "
              f"{(y_bilan - y_zero)/(y_zero - y_seuil):.2f}) et le chiffre du "
              "bilan — bloc de la source et détails de zone laissés à la planche",
        bas=f"ligne du bilan à {y_bilan:.0f} px, marge basse {AH - y_bilan:.0f} px",
        echelle_derivee=f"{k:.5f} px par {bc['unite']}, origine au zéro "
                        f"(y {y_zero:.2f})")


# ═══════════════════════════════════════════════════════════════════════════════
# Mécanisme `partage` — une production qui se partage sur le réseau public
# (pôle commercial de Fors). Même famille que le Sankey : la proportion portée
# par la géométrie. Deux origines à gauche (la toiture, le réseau), deux
# destinations à droite (la revente du surplus, les bâtiments communaux) ; la
# bande de la toiture se SÉPARE en deux rubans, et la part partagée CONVERGE
# avec le soutirage vers le même nœud. La conservation des flux tient
# l'équilibre : production + soutirage = consommation + surplus, donc les deux
# colonnes finissent à la même ordonnée — c'est le contrôle du mécanisme.
# L'ordre des destinations (revente en haut) évite tout croisement de rubans.
# Texte masqué : une petite barre dont la couleur part pour moitié vers un
# petit nœud isolé et pour moitié dans le haut d'un grand flux pâle — une
# production modeste, plus qu'à moitié partagée, des besoins bien plus grands.
# ═══════════════════════════════════════════════════════════════════════════════

PART_BARRE_W = 9
PART_X_BARRE_G = 366                        # barre des origines
PART_X_BARRE_D = 906                        # barre des destinations
PART_X0 = PART_X_BARRE_G + PART_BARRE_W     # 375 — départ des rubans
PART_LIB_D_X = PART_X_BARRE_D + PART_BARRE_W + 10   # 925 — étiquettes de droite
PART_Y0 = 232.0
PART_HAUTEUR = 320.0                        # encre totale d'une colonne
PART_ECART = 40.0                           # écart entre origines ET entre destinations


def _part_valeurs(pg):
    v = {f["cle"]: float(f["valeur"]) for f in pg["flux"]}
    total = v["surplus"] + v["partage"] + v["soutirage"]
    return v, total


def _part_geometrie(pg, y0, hauteur, ecart):
    """Les ordonnées des tranches, à l'échelle commune des deux colonnes.
    Gauche : toiture (surplus puis partagé), écart, réseau.
    Droite : revente, écart, communaux (partagé puis soutirage) — sans croisement."""
    v, total = _part_valeurs(pg)
    e = hauteur / total
    g = {"echelle": e, "total": total}
    y = y0
    g["surplus_g"] = (y, y + v["surplus"] * e); y = g["surplus_g"][1]
    g["partage_g"] = (y, y + v["partage"] * e); y = g["partage_g"][1]
    g["toiture"] = (y0, y)
    y += ecart
    g["reseau"] = (y, y + v["soutirage"] * e)
    y = y0
    g["revente"] = (y, y + v["surplus"] * e); y = g["revente"][1]
    y += ecart
    g["partage_d"] = (y, y + v["partage"] * e); y = g["partage_d"][1]
    g["soutirage_d"] = (y, y + v["soutirage"] * e)
    g["communaux"] = (g["partage_d"][0], g["soutirage_d"][1])
    g["bas"] = max(g["reseau"][1], g["communaux"][1])
    return g


def _part_ruban(x0, x1, y0g, y1g, y0d, y1d, couleur):
    xm = (x0 + x1) / 2
    d = (f"M {x0:.2f} {y0g:.2f} "
         f"C {xm:.2f} {y0g:.2f}, {xm:.2f} {y0d:.2f}, {x1:.2f} {y0d:.2f} "
         f"L {x1:.2f} {y1d:.2f} "
         f"C {xm:.2f} {y1d:.2f}, {xm:.2f} {y1g:.2f}, {x0:.2f} {y1g:.2f} Z")
    return (f'  <path d="{d}" class="c-{couleur} s-filet1" fill="{JETON[couleur]}" '
            f'stroke="{JETON["filet-1"]}" stroke-width="1"/>')


PART_COULEUR = {"surplus": "clair", "partage": "clair", "soutirage": "calcaire"}
PART_TRANCHES = {"surplus": ("surplus_g", "revente"),
                 "partage": ("partage_g", "partage_d"),
                 "soutirage": ("reseau", "soutirage_d")}


def composer_partage(donnees):
    pg = donnees["partage"]
    v, total = _part_valeurs(pg)
    g = _part_geometrie(pg, PART_Y0, PART_HAUTEUR, PART_ECART)

    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
      f'preserveAspectRatio="xMidYMid meet" role="img" '
      f'style="width:100%;height:auto;display:block" '
      f'aria-label="{echapper(donnees["aria_label"])}">')
    A("<style>")
    for cle, hexa in JETON.items():
        A(f"  .c-{cle} {{ fill: var(--color-{cle}, {hexa}); }}")
    A(f'  .s-filet1 {{ stroke: var(--color-filet-1, {JETON["filet-1"]}); }}')
    A(f"  .t-sans {{ font-family: {SANS}; }}")
    A(f"  .t-mono {{ font-family: {MONO}; }}")
    A("</style>")
    A(rect(0, 0, W, H, "papier"))

    # ── Bloc de titre ────────────────────────────────────────────────────────
    A(texte(MARGE, Y_SURTITRE, donnees["surtitre"], "mono", 11, 500,
            "pivot", tracking=11 * 0.14))
    A(texte(MARGE, Y_TITRE, donnees["titre"], "sans", 30, 700, "encre", wdth=112))
    A(texte(MARGE, Y_SOUSTITRE, donnees["sous_titre"], "sans", 16, 400,
            "pivot", wdth=100))
    A(rect(MARGE, Y_FILET_TITRE, UTILE, 1, "filet-1"))

    # ── En-tête de registre — il empêche la planche de mentir ────────────────
    A(texte(DESSIN_X0, Y_ENTETE, pg["entete"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))

    # ── Rubans, puis barres par-dessus ───────────────────────────────────────
    for f in pg["flux"]:
        cg, cd = PART_TRANCHES[f["cle"]]
        A(_part_ruban(PART_X0, PART_X_BARRE_D, g[cg][0], g[cg][1],
                      g[cd][0], g[cd][1], PART_COULEUR[f["cle"]]))
    A(rect(PART_X_BARRE_G, g["toiture"][0], PART_BARRE_W,
           g["toiture"][1] - g["toiture"][0], "encre"))
    A(rect(PART_X_BARRE_G, g["reseau"][0], PART_BARRE_W,
           g["reseau"][1] - g["reseau"][0], "encre"))
    A(rect(PART_X_BARRE_D, g["revente"][0], PART_BARRE_W,
           g["revente"][1] - g["revente"][0], "encre"))
    A(rect(PART_X_BARRE_D, g["communaux"][0], PART_BARRE_W,
           g["communaux"][1] - g["communaux"][0], "encre"))

    # ── Cotes des rubans — sur la bande, en encre (le pivot n'atteint pas
    #    4,5:1 sur le clair) ─────────────────────────────────────────────────
    xm = (PART_X0 + PART_X_BARRE_D) / 2
    depassements = []
    for f in pg["flux"]:
        cg, cd = PART_TRANCHES[f["cle"]]
        ym = ((g[cg][0] + g[cg][1]) / 2 + (g[cd][0] + g[cd][1]) / 2) / 2
        A(texte(xm, ym + 3.5, f["libelle_bande"], "mono", 10, 500, "encre",
                ancre="middle", tracking=10 * 0.14))
        largeur = mesurer(f["libelle_bande"], 10, "mono", tracking=10 * 0.14)
        depassements.append((f["cle"], largeur))

    # ── Étiquettes des origines, à gauche — bloc centré sur la tranche ──────
    for o in pg["origines"]:
        y0o, y1o = g[o["cle"]]
        centre = (y0o + y1o) / 2
        nd = len(o.get("detail", []) or [])
        y_lib = centre - (17 + nd * 13) / 2 + 12
        valeur = f'{o["valeur_affichee"]}{NN}{o["unite"]}'
        A(texte(DESSIN_X0, y_lib, o["libelle"], "sans", 15, 400, "encre", wdth=100))
        A(texte(VAL_X, y_lib, valeur, "mono", 12, 500, "encre",
                ancre="end", tabulaire=True))
        for k, d_ligne in enumerate(o.get("detail", []) or []):
            A(texte(DESSIN_X0, y_lib + 17 + k * 13, d_ligne, "mono", 10, 500,
                    "pivot", tracking=10 * 0.14))

    # ── Étiquettes des destinations, à droite ────────────────────────────────
    for de in pg["destinations"]:
        y0d, y1d = g[de["cle"]]
        centre = (y0d + y1d) / 2
        A(texte(PART_LIB_D_X, centre - 2, de["libelle"], "sans", 15, 600,
                "encre", wdth=112))
        A(texte(PART_LIB_D_X, centre + 16,
                f'{de["valeur_affichee"]}{NN}{de["unite"]}',
                "mono", 12, 500, "pivot", tabulaire=True))
        for k, d_ligne in enumerate(de.get("detail", []) or []):
            A(texte(PART_LIB_D_X, centre + 32 + k * 13, d_ligne, "mono", 10, 500,
                    "pivot", tracking=10 * 0.14))

    # ── Note de pied — la boucle que les rubans traversent ───────────────────
    y_note = g["bas"] + 30
    A(rect(DESSIN_X0, y_note - 18, UTILE, 1, "filet-3"))
    A(texte(DESSIN_X0, y_note, pg["note_pied"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))

    # ── Phrase de principe, cartouche ────────────────────────────────────────
    A(texte(MARGE, 688, donnees["phrase_principe"], "sans", 17, 400,
            "encre", wdth=100))
    libelle = donnees["cartouche_legende"]
    largeur = min(600,
                  round(mesurer(libelle, 11, "mono", tracking=11 * 0.14) + 40))
    A(rect(MARGE, Y_CARTOUCHE, largeur, H_CARTOUCHE, "profond"))
    A(texte(MARGE + 20, Y_CARTOUCHE + 20, libelle, "mono", 11, 500, "voile",
            tracking=11 * 0.14))
    A("</svg>")

    gauche = v["surplus"] + v["partage"] + v["soutirage"]
    droite = (g["revente"][1] - g["revente"][0]) + (g["communaux"][1] - g["communaux"][0])
    controles = {
        "gabarit": f"{W} x {H} — rapport {W/H:.4f} (3:2 exact)",
        "conservation": f'{pg["flux"][0]["valeur"]} + {pg["flux"][1]["valeur"]} '
                        f'(toiture) + {pg["flux"][2]["valeur"]} (réseau) '
                        f'= {int(gauche)}{NN}{pg["unite"]} de part et d’autre — '
                        f'colonnes closes à {g["reseau"][1]:.2f} et '
                        f'{g["communaux"][1]:.2f} px (écart '
                        f'{abs(g["reseau"][1] - g["communaux"][1]):.4f})',
        "echelle": f'{g["echelle"]:.6f} px par {pg["unite"]} — encre totale '
                   f'{PART_HAUTEUR:.0f} px par colonne, écart d’origine {PART_ECART:.0f} px',
        "demonstration": f'partagé {v["partage"]:.0f} contre surplus {v["surplus"]:.0f} '
                         f'({v["partage"]/(v["partage"]+v["surplus"])*100:.1f} % de la '
                         f'production) ; part de la toiture dans le nœud communal '
                         f'{v["partage"]/(v["partage"]+v["soutirage"])*100:.1f} %. '
                         f'Texte masqué : une petite barre se sépare en deux, '
                         f'sa moitié colorée coiffe un grand flux pâle',
        "topologie": f'origines x {PART_X_BARRE_G}, rubans {PART_X0} → '
                     f'{PART_X_BARRE_D}, destinations étiquetées jusqu’à '
                     f'{W - MARGE} px — revente en haut à droite : aucun croisement',
        "cotes_des_rubans": " ; ".join(f"{c} {l:.0f} px sur "
                                       f"{PART_X_BARRE_D - PART_X0:.0f} disponibles"
                                       for c, l in depassements),
        "bas_du_dessin": f'rubans jusqu’à {g["bas"]:.2f} px, note de pied à '
                         f'{y_note:.2f}, phrase de principe à 688, cartouche '
                         f'714–744, marge basse {H - (Y_CARTOUCHE + H_CARTOUCHE)} px',
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur*H_CARTOUCHE} px², soit "
                            f"{largeur*H_CARTOUCHE/(W*H)*100:.2f} % de la planche",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l’échelle 0,96 "
                         f"(1152 / {W})",
    }
    return "\n".join(out) + "\n", controles


def composer_vignette_partage(donnees):
    """La vignette : le partage entier — deux origines, la séparation, la
    convergence — et les deux nœuds de droite chiffrés. Libellés d'origine,
    détails et note laissés à la planche."""
    pg = donnees["partage"]
    x_bar_g, x_bar_d, bar_w = 18.0, 170.0, 5.0
    x0 = x_bar_g + bar_w
    lib_x = 182.0
    g = _part_geometrie(pg, 40.0, 100.0, 10.0)
    courts = pg["libelles_courts"]

    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false" '
      f'style="width:100%;height:auto;display:block">')
    A("<style>")
    for cle, hexa in JETON.items():
        A(f"  .c-{cle} {{ fill: var(--color-{cle}, {hexa}); }}")
    A(f'  .s-filet1 {{ stroke: var(--color-filet-1, {JETON["filet-1"]}); }}')
    A(f"  .t-sans {{ font-family: {SANS}; }}")
    A(f"  .t-mono {{ font-family: {MONO}; }}")
    A("</style>")
    A(rect(0, 0, VW, VH, "papier"))
    A(texte(V_MARGE, 22, donnees["vignette_surtitre"], "mono", 9, 500, "pivot",
            tracking=9 * 0.14))

    for f in pg["flux"]:
        cg, cd = PART_TRANCHES[f["cle"]]
        A(_part_ruban(x0, x_bar_d, g[cg][0], g[cg][1],
                      g[cd][0], g[cd][1], PART_COULEUR[f["cle"]]))
    A(rect(x_bar_g, g["toiture"][0], bar_w,
           g["toiture"][1] - g["toiture"][0], "encre"))
    A(rect(x_bar_g, g["reseau"][0], bar_w,
           g["reseau"][1] - g["reseau"][0], "encre"))
    A(rect(x_bar_d, g["revente"][0], bar_w + 1,
           g["revente"][1] - g["revente"][0], "encre"))
    A(rect(x_bar_d, g["communaux"][0], bar_w + 1,
           g["communaux"][1] - g["communaux"][0], "encre"))

    for cle in ("revente", "communaux"):
        de = next(d for d in pg["destinations"] if d["cle"] == cle)
        centre = (g[cle][0] + g[cle][1]) / 2
        A(texte(lib_x, centre - 3, courts[cle], "sans", 12, 600, "encre", wdth=112))
        A(texte(lib_x, centre + 11, f'{de["valeur_affichee"]}{NN}{de["unite"]}',
                "mono", 10, 500, "pivot", tabulaire=True))

    A("</svg>")
    controles = {
        "gabarit": f"{VW} x {VH} — rapport {VW/VH:.4f} (3:2 exact)",
        "echelle_de_rendu": f"carte de projet mesurée de 274 à 296 px — "
                            f"échelle {274/VW:.2f} à {296/VW:.2f}",
        "corps_minimal": f"9 px dans le repère — rendu à {9*274/VW:.1f} px au pire cas",
        "motif": "les deux origines, la séparation et la convergence à "
                 "l’échelle commune ; les deux nœuds de droite chiffrés — "
                 "libellés d’origine, cotes de ruban et note laissés à la planche",
        "bas_du_dessin": f'{g["bas"]:.2f} px, marge basse {VH - g["bas"]:.2f} px',
    }
    return "\n".join(out) + "\n", controles


def composer_appui_partage(donnees):
    """L'appui : le motif entier à l'échelle 1 — les quatre barres, les trois
    rubans, les origines et destinations chiffrées, une cote dans le ruban
    partagé. Détails et note laissés à la planche."""
    pg = donnees["partage"]
    v, total = _part_valeurs(pg)
    x_lib_g, x_bar_g, x_bar_d, bar_w = 180.0, 188.0, 392.0, 8.0
    x0 = x_bar_g + bar_w
    lib_x = 408.0
    g = _part_geometrie(pg, 66.0, 200.0, 24.0)
    courts = pg["libelles_courts"]

    out = []
    A = out.append
    racine_appui(A, donnees, strokes=("filet-1",))

    for f in pg["flux"]:
        cg, cd = PART_TRANCHES[f["cle"]]
        A(_part_ruban(x0, x_bar_d, g[cg][0], g[cg][1],
                      g[cd][0], g[cd][1], PART_COULEUR[f["cle"]]))
    A(rect(x_bar_g, g["toiture"][0], bar_w,
           g["toiture"][1] - g["toiture"][0], "encre"))
    A(rect(x_bar_g, g["reseau"][0], bar_w,
           g["reseau"][1] - g["reseau"][0], "encre"))
    A(rect(x_bar_d, g["revente"][0], bar_w,
           g["revente"][1] - g["revente"][0], "encre"))
    A(rect(x_bar_d, g["communaux"][0], bar_w,
           g["communaux"][1] - g["communaux"][0], "encre"))

    for o in pg["origines"]:
        centre = (g[o["cle"]][0] + g[o["cle"]][1]) / 2
        A(texte(x_lib_g, centre - 2, courts[o["cle"]], "sans", 13, 600,
                "encre", wdth=112, ancre="end"))
        A(texte(x_lib_g, centre + 14, f'{o["valeur_affichee"]}{NN}{o["unite"]}',
                "mono", 11, 500, "pivot", ancre="end", tabulaire=True))
    for de in pg["destinations"]:
        centre = (g[de["cle"]][0] + g[de["cle"]][1]) / 2
        A(texte(lib_x, centre - 2, courts[de["cle"]], "sans", 13, 600,
                "encre", wdth=112))
        A(texte(lib_x, centre + 14, f'{de["valeur_affichee"]}{NN}{de["unite"]}',
                "mono", 11, 500, "pivot", tabulaire=True))

    # Une seule cote de ruban : la part partagée, la thèse de l'appui.
    xm = (x0 + x_bar_d) / 2
    ym = ((g["partage_g"][0] + g["partage_g"][1]) / 2
          + (g["partage_d"][0] + g["partage_d"][1]) / 2) / 2
    pct = v["partage"] / (v["partage"] + v["surplus"]) * 100
    A(texte(xm, ym + 3.5, f'{pct:.0f}{NN}%{NN}PARTAGÉS', "mono", 10, 500,
            "encre", ancre="middle", tracking=10 * 0.14))

    A("</svg>")
    return "\n".join(out) + "\n", controles_appui(
        motif="les quatre barres, les trois rubans et les quatre valeurs à "
              "l’échelle 1, une cote dans le ruban partagé — détails, cotes "
              "des autres rubans et note laissés à la planche",
        bas=f'rubans jusqu’à {g["bas"]:.0f} px, marge basse '
            f'{AH - g["bas"]:.0f} px',
        echelle_derivee=f'{g["echelle"]:.6f} px par {pg["unite"]}, colonnes '
                        f'closes à {g["reseau"][1]:.2f} et {g["communaux"][1]:.2f} px')


def _composer(donnees):
    if "bascule" in donnees:
        return composer_bascule(donnees)
    if "dedoublement" in donnees:
        return composer_dedoublement(donnees)
    if "partage" in donnees:
        return composer_partage(donnees)
    if "plafonds" in donnees:
        return composer_plafonds(donnees)
    return composer(donnees, donnees["fiche"])


def _composer_vignette(donnees):
    if "bascule" in donnees:
        return composer_vignette_bascule(donnees)
    if "dedoublement" in donnees:
        return composer_vignette_dedoublement(donnees)
    if "partage" in donnees:
        return composer_vignette_partage(donnees)
    if "plafonds" in donnees:
        return composer_vignette_plafonds(donnees)
    return composer_vignette(donnees)


def _composer_appui(donnees):
    if "bascule" in donnees:
        return composer_appui_bascule(donnees)
    if "dedoublement" in donnees:
        return composer_appui_dedoublement(donnees)
    if "partage" in donnees:
        return composer_appui_partage(donnees)
    if "plafonds" in donnees:
        return composer_appui_plafonds(donnees)
    return composer_appui(donnees)


if __name__ == "__main__":
    executer(_composer, _composer_vignette, _composer_appui)
