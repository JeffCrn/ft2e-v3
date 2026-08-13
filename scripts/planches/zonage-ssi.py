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
    """Bloc à fond opaque + filet 1 px. Le rang du filet est porté par
    l'opacité (filet-1 porteur, filet-2 provisionné, filet-3 indication)."""
    return (f'  <rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
            f'class="c-{fond} s-{filet}" fill="{JETON[fond]}" '
            f'stroke="{JETON[filet]}" stroke-width="1"/>')


def ligne(x0, y0, x1, y1, cle, epaisseur=1.0):
    return (f'  <path d="M {x0:.2f} {y0:.2f} L {x1:.2f} {y1:.2f}" fill="none" '
            f'class="s-{cle}" stroke="{JETON[cle]}" '
            f'stroke-width="{epaisseur}"/>')


def fleche(x, y, cle):
    """Pointe de flèche vers la droite, l'apex en (x, y)."""
    return (f'  <path d="M {x:.2f} {y:.2f} L {x - 9:.2f} {y - 4.5:.2f} '
            f'L {x - 9:.2f} {y + 4.5:.2f} Z" class="c-{cle}" '
            f'fill="{JETON[cle]}"/>')


def entete_style(A):
    A("<style>")
    for cle, hexa in JETON.items():
        A(f"  .c-{cle} {{ fill: var(--color-{cle}, {hexa}); }}")
    for cle in ("filet-1", "filet-2", "filet-3", "encre"):
        A(f"  .s-{cle} {{ stroke: var(--color-{cle}, {JETON[cle]}); }}")
    A(f"  .t-sans {{ font-family: {SANS}; }}")
    A(f"  .t-mono {{ font-family: {MONO}; }}")
    A("</style>")


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
    entete_style(A)
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
