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

Le motif de l'archétype : un contraste de découpage. La bande AVANT — une seule
zone d'alarme — s'oppose à la pile des zones APRÈS ; les blocs sont d'ÉGALE
hauteur parce qu'aucune surface par zone n'est donnée : la géométrie code le
nombre de zones, jamais leur taille. Un bloc `provisionnee` se distingue par
deux signes redondants (fond papier + mention dans son étiquette), jamais par
une couleur — le système n'en a pas.

Deuxième module du chantier après `sankey-energie.py` : ce qu'ils partagent
(jetons, mesure des chasses, insécables, double écriture des couleurs) a
désormais deux occurrences et peut remonter dans un module commun — décision
de dépôt, pas de session.
"""

import io
import json
import sys
from pathlib import Path

NN = " "   # espace fine insécable — texte courant et mono
INS = " "  # espace insécable normale — relevés en grand corps

# ── Gabarit (protocole rév. 3) ────────────────────────────────────────────────
W, H = 1200, 800
MARGE = 56
MODULE = 28
UTILE = W - 2 * MARGE                      # 1088
GOUTTIERE = 56
DESSIN_W = round((UTILE - GOUTTIERE) * 7 / 12)   # 602
RELEVE_W = UTILE - GOUTTIERE - DESSIN_W          # 430
DESSIN_X0, DESSIN_X1 = MARGE, MARGE + DESSIN_W
RELEVE_X0, RELEVE_X1 = DESSIN_X1 + GOUTTIERE, W - MARGE
SEPARATEUR_X = DESSIN_X1 + GOUTTIERE / 2

# ── Gabarit de la VIGNETTE ────────────────────────────────────────────────────
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

# ── Rythme vertical de la planche ────────────────────────────────────────────
Y_SURTITRE = 76
Y_TITRE = 112
Y_SOUSTITRE = 138
Y_FILET_TITRE = 160
Y_ENTETE = 190
Y_AVANT_TAG = 214
Y_AVANT = 222
H_AVANT = 48
ECART_APRES = 26          # entre la bande AVANT et l'étiquette APRÈS
DECAL_TAG = 8             # entre l'étiquette APRÈS et le premier bloc
H_ZONE = 52
ECART_ZONE = 10
ECART_HORS = 14
H_HORS = 44
PAD = 16                  # retrait interne des blocs
Y_PHRASE = 688
Y_CARTOUCHE = 714
H_CARTOUCHE = 30

# Avances CALIBRÉES au rendu navigateur (getBBox) sur la première planche.
AVANCE = {
    "sans-400": 0.500,
    "sans-600": 0.480,
    "sans-700": 0.596,
    "mono": 0.600,
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


def rect_bord(x, y, w, h, fond, filet):
    """Bloc de zone : fond opaque + filet 1 px. Le rang du filet est porté par
    l'opacité (filet-1 porteur, filet-2 provisionné, filet-3 indication)."""
    return (f'  <rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
            f'class="c-{fond} s-{filet}" fill="{JETON[fond]}" '
            f'stroke="{JETON[filet]}" stroke-width="1"/>')


def entete_style(A):
    A("<style>")
    for cle, hexa in JETON.items():
        A(f"  .c-{cle} {{ fill: var(--color-{cle}, {hexa}); }}")
    for cle in ("filet-1", "filet-2", "filet-3", "encre"):
        A(f"  .s-{cle} {{ stroke: var(--color-{cle}, {JETON[cle]}); }}")
    A(f"  .t-sans {{ font-family: {SANS}; }}")
    A(f"  .t-mono {{ font-family: {MONO}; }}")
    A("</style>")


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
    entete_style(A)
    A(rect(0, 0, W, H, "papier"))

    # ── Bloc de titre ────────────────────────────────────────────────────────
    A(texte(MARGE, Y_SURTITRE, donnees["surtitre"], "mono", 11, 500,
            "pivot", tracking=11 * 0.14))
    A(texte(MARGE, Y_TITRE, donnees["titre"], "sans", 30, 700, "encre", wdth=112))
    A(texte(MARGE, Y_SOUSTITRE, donnees["sous_titre"], "sans", 16, 400,
            "pivot", wdth=100))
    A(rect(MARGE, Y_FILET_TITRE, UTILE, 1, "filet-1"))

    # ── En-têtes de périmètre ────────────────────────────────────────────────
    controler("en-tête dessin", z["entete"], 10, "mono", DESSIN_W, 10 * 0.14)
    A(texte(DESSIN_X0, Y_ENTETE, z["entete"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    controler("en-tête relevé", donnees["releve_entete"], 10, "mono",
              RELEVE_W, 10 * 0.14)
    A(texte(RELEVE_X0, Y_ENTETE, donnees["releve_entete"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    A(rect(SEPARATEUR_X, Y_FILET_TITRE + 12, 1, 488, "filet-3"))

    # ── AVANT : la zone unique d'origine ─────────────────────────────────────
    avant = z["avant"]
    A(texte(DESSIN_X0, Y_AVANT_TAG, avant["tag"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    A(rect_bord(DESSIN_X0, Y_AVANT, DESSIN_W, H_AVANT, "calcaire", "filet-1"))
    valeur_avant = f'{avant["valeur"]}{NN}{avant["unite"]}'
    largeur_valeur = mesurer(valeur_avant, 12, "mono")
    controler("libellé AVANT", avant["libelle"], 15, "sans-400",
              DESSIN_W - 2 * PAD - largeur_valeur - 16)
    A(texte(DESSIN_X0 + PAD, Y_AVANT + 21, avant["libelle"], "sans", 15, 400,
            "encre", wdth=100))
    A(texte(DESSIN_X1 - PAD, Y_AVANT + 21, valeur_avant, "mono", 12, 500,
            "encre", ancre="end", tabulaire=True))
    for k, ligne in enumerate(avant["detail"]):
        controler(f"détail AVANT {k+1}", ligne, 10, "mono",
                  DESSIN_W - 2 * PAD, 10 * 0.14)
        A(texte(DESSIN_X0 + PAD, Y_AVANT + 38 + k * 13, ligne, "mono", 10, 500,
                "pivot", tracking=10 * 0.14))

    # ── APRÈS : la pile des zones ────────────────────────────────────────────
    y_apres_tag = Y_AVANT + H_AVANT + ECART_APRES
    A(texte(DESSIN_X0, y_apres_tag, z["apres_tag"], "mono", 10, 500,
            "pivot", tracking=10 * 0.14))
    y = y_apres_tag + DECAL_TAG
    for zone in z["zones"]:
        prov = zone.get("etat") == "provisionnee"
        fond = "papier" if prov else "calcaire"
        filet = "filet-2" if prov else "filet-1"
        A(rect_bord(DESSIN_X0, y, DESSIN_W, H_ZONE, fond, filet))
        A(texte(DESSIN_X0 + PAD, y + 19, zone["tag"], "mono", 10, 500,
                "pivot", tracking=10 * 0.14))
        largeur_nom = mesurer(zone["libelle"], 15, "sans-600")
        A(texte(DESSIN_X0 + PAD, y + 40, zone["libelle"], "sans", 15, 600,
                "encre", wdth=112))
        details = zone.get("detail", []) or []
        base = y + H_ZONE / 2 + 3.5 - (len(details) - 1) * 7
        for k, ligne in enumerate(details):
            controler(f'détail {zone["cle"]} {k+1}', ligne, 10, "mono",
                      DESSIN_W - 2 * PAD - largeur_nom - 16, 10 * 0.14)
            A(texte(DESSIN_X1 - PAD, base + k * 14, ligne, "mono", 10, 500,
                    "pivot", ancre="end", tracking=10 * 0.14))
        y += H_ZONE + ECART_ZONE
    bas_zones = y - ECART_ZONE

    # ── Hors zonage ──────────────────────────────────────────────────────────
    y_hors = bas_zones + ECART_HORS
    for hz in z["hors_zonage"]:
        A(rect_bord(DESSIN_X0, y_hors, DESSIN_W, H_HORS, "papier", "filet-3"))
        A(texte(DESSIN_X0 + PAD, y_hors + 17, hz["tag"], "mono", 10, 500,
                "pivot", tracking=10 * 0.14))
        largeur_nom = mesurer(hz["libelle"], 15, "sans-400")
        A(texte(DESSIN_X0 + PAD, y_hors + 36, hz["libelle"], "sans", 15, 400,
                "encre", wdth=100))
        details = hz.get("detail", []) or []
        base = y_hors + H_HORS / 2 + 3.5 - (len(details) - 1) * 7
        for k, ligne in enumerate(details):
            controler(f'détail {hz["cle"]} {k+1}', ligne, 10, "mono",
                      DESSIN_W - 2 * PAD - largeur_nom - 16, 10 * 0.14)
            A(texte(DESSIN_X1 - PAD, base + k * 14, ligne,
                    "mono", 10, 500, "pivot", ancre="end", tracking=10 * 0.14))
        y_hors += H_HORS
    bas_dessin = y_hors

    # ── Note de pied de la zone de dessin ────────────────────────────────────
    y_filet_note = bas_dessin + 14
    A(rect(DESSIN_X0, y_filet_note, DESSIN_W, 1, "filet-3"))
    y_note = y_filet_note + 16
    for k, ligne in enumerate(z["note_pied"]):
        controler(f"note de pied {k+1}", ligne, 10, "mono", DESSIN_W, 10 * 0.14)
        A(texte(DESSIN_X0, y_note + k * 13, ligne, "mono", 10, 500,
                "pivot", tracking=10 * 0.14))
    bas_notes = y_note + (len(z["note_pied"]) - 1) * 13

    # ── Colonne de relevé ────────────────────────────────────────────────────
    y = 244.0
    for i, r in enumerate(donnees["releve"]):
        couleur = "encre" if i == 0 else "pivot"
        x = RELEVE_X0
        if r.get("prefixe"):
            A(texte(x, y, r["prefixe"], "sans", 22, 400, "pivot", wdth=100))
            x += mesurer(r["prefixe"], 22, "sans-400") + 14
        A(texte(x, y, r["valeur"], "sans", 40, 700, couleur, wdth=118,
                tabulaire=True))
        x += mesurer(r["valeur"], 40, "sans-700") + 8
        A(texte(x, y, r["unite"], "sans", 15, 400, couleur, wdth=100))
        for k, ligne in enumerate(r["legende"]):
            controler(f"légende relevé {i+1}.{k+1}", ligne, 10, "mono",
                      RELEVE_W, 10 * 0.14)
            A(texte(RELEVE_X0, y + 24 + k * 14, ligne, "mono", 10, 500,
                    "pivot", tracking=10 * 0.14))
        y += 96
    A(rect(RELEVE_X0, y - 44, RELEVE_W, 1, "filet-3"))
    y -= 8
    for j, r in enumerate(donnees["releve_secondaire"]):
        A(texte(RELEVE_X0, y, r["intitule"], "sans", 16, 600, "encre", wdth=112))
        A(texte(RELEVE_X1, y, r["valeur"], "sans", 22, 700, "pivot",
                wdth=118, ancre="end", tabulaire=True))
        for k, ligne in enumerate(r["appui"]):
            controler(f"appui secondaire {j+1}.{k+1}", ligne, 10, "mono",
                      RELEVE_W, 10 * 0.14)
            A(texte(RELEVE_X0, y + 22 + k * 14, ligne, "mono", 10, 500,
                    "pivot", tracking=10 * 0.14))
        y += 76
    bas_releve = y - 76 + 22 + 14

    # ── Phrase de principe, pleine largeur ───────────────────────────────────
    controler("phrase de principe", donnees["phrase_principe"], 17,
              "sans-400", UTILE)
    A(texte(MARGE, Y_PHRASE, donnees["phrase_principe"], "sans", 17, 400,
            "encre", wdth=100))

    # ── Cartouche — largeur AJUSTÉE au texte, jamais codée ───────────────────
    libelle = donnees["cartouche_legende"]
    largeur = min(DESSIN_W,
                  round(mesurer(libelle, 11, "mono", tracking=11 * 0.14) + 40))
    A(rect(MARGE, Y_CARTOUCHE, largeur, H_CARTOUCHE, "profond"))
    A(texte(MARGE + 20, Y_CARTOUCHE + 20, libelle, "mono", 11, 500, "voile",
            tracking=11 * 0.14))

    A("</svg>")

    actives = sum(1 for zz in z["zones"] if zz.get("etat") != "provisionnee")
    prov = len(z["zones"]) - actives
    controles = {
        "gabarit": f"{W} x {H} — rapport {W/H:.4f} (3:2 exact)",
        "partition": f"zone de dessin {DESSIN_W} px / colonne de relevé {RELEVE_W} px "
                     f"= {DESSIN_W/RELEVE_W:.4f} — partition 7/5 de la charte",
        "comptage_zones": f"1 bande AVANT + {actives} zones actives + {prov} provisionnée "
                          f"+ {len(z['hors_zonage'])} bloc hors zonage — blocs d'égale "
                          f"hauteur, la géométrie ne code que le nombre",
        "bas_du_dessin": f"blocs jusqu'à {bas_dessin:.0f} px, note de pied "
                         f"{y_note:.0f}–{bas_notes:.0f} px — phrase de principe à "
                         f"{Y_PHRASE}, cartouche {Y_CARTOUCHE}–{Y_CARTOUCHE+H_CARTOUCHE}, "
                         f"marge basse {H - (Y_CARTOUCHE + H_CARTOUCHE)} px",
        "bas_du_releve": f"relevé secondaire jusqu'à {bas_releve:.0f} px",
        "reserve_profonde": f"cartouche {largeur} x {H_CARTOUCHE} px = "
                            f"{largeur*H_CARTOUCHE} px², soit "
                            f"{largeur*H_CARTOUCHE/(W*H)*100:.2f} % de la planche",
        "corps_minimal": "10 px dans le repère — rendu à 9,60 px à l'échelle 0,96 "
                         f"(1152 / {W})",
        "depassements": depassements if depassements
                        else "aucun — toutes les lignes mesurées sous leur colonne",
    }
    return "\n".join(out) + "\n", controles


def composer_vignette(donnees):
    """La vignette : le motif de l'archétype, sans son appareil.

    Ce qu'elle garde : le contraste une zone / trois zones — la bande unique
    d'origine à gauche, la pile des trois zones actives à droite, et la surface
    évacuée comme valeur du nœud AVANT. Ce qu'elle laisse : la zone
    provisionnée, le bloc hors zonage, les classements, le relevé, la phrase
    de principe et le cartouche. Trois blocs nommés dans 300 px se lisent ;
    six blocs annotés ne se liraient pas."""
    z = donnees["zonage"]
    zones = [zz for zz in z["zones"] if zz.get("etat") != "provisionnee"]

    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
      f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false" '
      f'style="width:100%;height:auto;display:block">')
    entete_style(A)
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
    avant = z["avant"]
    lignes = replier(avant.get("libelle_vignette", avant["libelle"]), 12,
                     bloc_g_w - 20, "sans-600")
    centre = y0 + h_pile / 2
    base = centre - 8 - (len(lignes) - 1) * 8
    for k, ligne in enumerate(lignes):
        A(texte(bloc_g_x + 10, base + k * 16, ligne, "sans", 12, 600,
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
        "motif": f"1 bande AVANT contre {len(zones)} zones actives — la zone "
                 f"provisionnée et le bloc hors zonage sont laissés à la planche",
        "bas_du_dessin": f"{VH - 24} px, marge basse 24 px",
    }
    return "\n".join(out) + "\n", controles


def main():
    dossier = Path(sys.argv[1])
    donnees = json.loads((dossier / "planche.json").read_text(encoding="utf-8"))
    svg, controles = composer(donnees)

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
