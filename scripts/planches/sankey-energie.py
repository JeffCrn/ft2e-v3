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
                    ligne, replier, racine_appui, controles_appui, executer)


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
                          f"jusqu'à {W - MARGE} px — schéma pleine largeur, colonne "
                          f"de relevé supprimée (révision 4)",
        "bouclage_bandes": " + ".join(str(s["valeur"]) for s in sources)
                           + f" = {total}{NN}{sk['unite']} ; "
                           f"hauteur totale {sum(p['h'] for p in poses):.2f} px "
                           f"(échelle {echelle:.6f} px/{sk['unite']})",
        "part_enveloppe_dans_la_hauteur":
            f"{sources[-1]['valeur']} / {total} = "
            f"{sources[-1]['valeur']/total*100:.3f} %",
        "bas_du_dessin": f"bandes jusqu'à {bas_bandes:.2f} px, libellés jusqu'à "
                         f"{bas_libelles:.2f} px — note de pied à {y_note:.2f}, "
                         f"phrase de principe à 688, cartouche 714–744, "
                         f"marge basse {H - (Y_CARTOUCHE + H_CARTOUCHE)} px",
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur*H_CARTOUCHE} px², soit "
                            f"{largeur*H_CARTOUCHE/(W*H)*100:.2f} % de la planche",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l'échelle 0,96 "
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
              "l'échelle 1 ; libellés portés par les bandes assez hautes "
              "(plus l'enveloppe) — valeurs par poste, détails et note de "
              "pied laissés à la planche",
        bas=f"bandes jusqu'à {poses[-1]['y1']:.0f} px, marge basse "
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
        "demonstration": "trois pistes à la même origine et à l'échelle commune "
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
        "bas_du_dessin": f"rangs A/B/C jusqu'à {bas_a:.0f}, {bas_b:.0f} et "
                         f"{bas_c:.0f} px, seuil prolongé jusqu'à "
                         f"{y_c + 6 + P_H + 14:.0f}, phrase de principe à 688, "
                         f"cartouche 714–744, marge basse {H - 744} px",
        "reserve_profonde": f"cartouche {largeur} x 30 px = {largeur * 30} px², "
                            f"soit {largeur * 30 / (W * H) * 100:.2f} % de la planche",
        "chiffre_unique": "aucun chiffre de relevé — les six valeurs des pistes "
                          "sont des cotes mono 10 et 12 (révision 4)",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l'échelle "
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
        "bas_du_dessin": "piste C jusqu'à 158 px, marge basse "
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
        motif="les trois pistes à l'échelle 1, la frontière à double trait et "
              "sa mention, le seuil prolongé, les couples résultat / plafond "
              "et la légende des deux signes — cellules, compositions et "
              "détails de générateur laissés à la planche",
        bas="légende jusqu'à 296 px, marge basse 72 px")


def _composer(donnees):
    if "plafonds" in donnees:
        return composer_plafonds(donnees)
    return composer(donnees, donnees["fiche"])


def _composer_vignette(donnees):
    if "plafonds" in donnees:
        return composer_vignette_plafonds(donnees)
    return composer_vignette(donnees)


def _composer_appui(donnees):
    if "plafonds" in donnees:
        return composer_appui_plafonds(donnees)
    return composer_appui(donnees)


if __name__ == "__main__":
    executer(_composer, _composer_vignette, _composer_appui)
