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

import io
import json
import sys
from pathlib import Path

NN = " "   # espace fine insécable — texte courant et mono
INS = " "  # espace insécable normale — relevés en grand corps (cf. § Mesures)

# ── Gabarit (protocole rév. 4) ────────────────────────────────────────────────
# La révision 4 supprime la partition 7/5 et la colonne de relevé : la planche
# schématise la solution — le flux occupe la largeur utile entière, et les
# chiffres que la fiche porte déjà ne montent pas sur le dessin.
W, H = 1200, 800
MARGE = 56
MODULE = 28
UTILE = W - 2 * MARGE                      # 1088
DESSIN_X0 = MARGE

# ── Gabarit de la VIGNETTE (protocole rév. 2.2) ───────────────────────────────
# Une vignette n'est pas un recadrage de la planche : c'est une COMPOSITION
# PROPRE, calée sur la taille où elle est lue. Les cartes de projet font 274 à
# 296 px de large ; à 300 px de repère, l'échelle de rendu va de 0,91 à 0,99, et
# les corps écrits ici sont donc les corps lus. Recadrer la planche de 1200 dans
# la même case donnait 0,25 : un lavis, et un cadrage subi.
VW, VH = 300, 200
V_MARGE = 14

# ── Jetons ────────────────────────────────────────────────────────────────────
JETON = {
    "profond": "#001718",
    "encre": "#00393A",
    "pivot": "#336667",
    "clair": "#99CCCD",
    "voile": "#E1F4F4",
    "papier": "#F7F9FA",
    "calcaire": "#EDF0F2",
    "filet-1": "#00393A38",
    "filet-2": "#00393A29",
    "filet-3": "#00393A1F",
}

SANS = '"Archivo Variable", Archivo, "Helvetica Neue", Arial, sans-serif'
MONO = '"IBM Plex Mono", ui-monospace, monospace'

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


# Avances CALIBRÉES au rendu navigateur (getBBox), et non estimées : c'est la
# mesure qui a montré que l'estimation posait l'unité 22 px trop loin.
AVANCE = {
    "sans-400": 0.500,      # Archivo Variable wdth 100 / 400 — de 0,455 à 0,507 selon
                        # la chaîne mesurée ; 0,500 majore, donc le repli est prudent
    "sans-600": 0.480,      # wdth 112 / 600
    "sans-700": 0.596,      # wdth 118 / 700, chiffres tabulaires — mesuré 23,84 px à 40 px
    "mono": 0.600,          # IBM Plex Mono, chasse fixe
}
FINE = 0.098               # U+202F dans Archivo — mesuré 3,93 px à 40 px
INSEC = 0.196              # U+00A0 — mesuré 7,85 px à 40 px


def mesurer(t, corps, profil="sans-400", tracking=0.0):
    """Largeur d'une chaîne, aux avances calibrées ci-dessus."""
    a = AVANCE[profil]
    l = 0.0
    for c in t:
        if c == NN:
            l += FINE
        elif c == INS:
            l += INSEC
        else:
            l += a
    return l * corps + tracking * max(len(t) - 1, 0)


def replier(t, corps, largeur, profil="sans-400"):
    """Découpe un libellé sur la largeur disponible, au dernier espace qui tient."""
    if mesurer(t, corps, profil) <= largeur:
        return [t]
    mots, lignes, courante = t.split(" "), [], ""
    for m in mots:
        essai = f"{courante} {m}".strip()
        if courante and mesurer(essai, corps, profil) > largeur:
            lignes.append(courante)
            courante = m
        else:
            courante = essai
    if courante:
        lignes.append(courante)
    return lignes


def echapper(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def texte(x, y, contenu, police, corps, graisse, couleur,
          wdth=None, ancre=None, tracking=None, tabulaire=False):
    """Un nœud de texte. La couleur est écrite DEUX FOIS : classe `var()` pour le
    navigateur, attribut hexadécimal pour le moteur de rendu de contrôle."""
    fam = MONO if police == "mono" else SANS
    cls = f"t-{'mono' if police == 'mono' else 'sans'} c-{couleur}"
    a = [f'x="{x:.2f}"', f'y="{y:.2f}"', f'class="{cls}"',
         f'fill="{JETON[couleur]}"', f'font-family=\'{fam}\'',
         f'font-size="{corps}"', f'font-weight="{graisse}"']
    if wdth is not None:
        a.append(f"font-variation-settings=\"'wdth' {wdth}, 'wght' {graisse}\"")
    if tracking:
        a.append(f'letter-spacing="{tracking:.2f}"')
    if ancre:
        a.append(f'text-anchor="{ancre}"')
    if tabulaire:
        a.append('font-variant-numeric="tabular-nums"')
    return f'  <text {" ".join(a)}>{echapper(contenu)}</text>'


def rect(x, y, w, h, couleur):
    return (f'  <rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
            f'class="c-{couleur}" fill="{JETON[couleur]}"/>')


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


def main():
    dossier = Path(sys.argv[1])
    donnees = json.loads((dossier / "planche.json").read_text(encoding="utf-8"))
    svg, controles = composer(donnees, donnees["fiche"])

    io.open(dossier / "planche.svg", "w", encoding="utf-8", newline="\n").write(svg)

    vignette, controles_vignette = composer_vignette(donnees)
    io.open(dossier / "vignette.svg", "w", encoding="utf-8", newline="\n").write(vignette)

    donnees["controles"] = controles
    donnees["controles_vignette"] = controles_vignette
    io.open(dossier / "planche.json", "w", encoding="utf-8", newline="\n").write(
        json.dumps(donnees, ensure_ascii=False, indent=2) + "\n")

    print(f"planche.svg  — {len(svg.encode('utf-8'))} octets, "
          f"{svg.count('<text')} nœuds de texte")
    print(f"vignette.svg — {len(vignette.encode('utf-8'))} octets, "
          f"{vignette.count('<text')} nœuds de texte")
    for k, v in controles_vignette.items():
        print(f"  · vignette · {k} : {v}")
    for k, v in controles.items():
        print(f"  · {k} : {v}")


if __name__ == "__main__":
    main()
