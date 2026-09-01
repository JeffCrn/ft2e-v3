#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rendus de controle d'un dossier de planche.

    python scripts/planches/rendre_png.py public/images/projets/<slug>

Ecrit, dans le dossier :
    planche.png    2400 x 1600 — la piece livree (og:image, impression)
et, dans le scratchpad passe en 2e argument (ou le dossier a defaut) :
    controle-1152.png   la planche a sa taille de lecture reelle
    controle-vignette-274.png / -296.png   la vignette dans sa carte
    controle-appui-552.png                 l'appui a la largeur du hero

⚠ cairosvg ne resout pas var() : la copie de controle perd le bloc <style>
ET l'attribut style de la racine. L'attribut n'est PAS toujours suivi d'une
espace (racine de vignette `...block">`) — un remplacement a espace finale le
manque et la vignette rend BLANCHE, sans erreur. Retrait par REGEX.

⚠ cairosvg ne fusionne pas les hexadecimaux a 8 chiffres (les filets) : on les
aplatit sur papier avant rendu.
"""
import io
import re
import sys
from pathlib import Path

import cairosvg

FILETS = {
    "#00393A38": "#C1CFD0",   # filet-1, encre 22 % sur papier
    "#00393A29": "#CFDADB",   # filet-2, encre 16 %
    "#00393A1F": "#D9E2E3",   # filet-3, encre 12 %
}


def preparer(svg):
    svg = re.sub(r"<style>.*?</style>", "", svg, flags=re.S)
    svg = re.sub(r'\sstyle="[^"]*"', "", svg, count=1)
    for a, b in FILETS.items():
        svg = svg.replace(a, b).replace(a.lower(), b)
    return svg


def rendre(chemin_svg, sortie, largeur):
    svg = preparer(io.open(chemin_svg, encoding="utf-8").read())
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=str(sortie),
                     output_width=largeur, background_color="#F7F9FA")
    print(f"{sortie.name:32s} {largeur} px")


if __name__ == "__main__":
    d = Path(sys.argv[1])
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else d
    out.mkdir(parents=True, exist_ok=True)
    rendre(d / "planche.svg", d / "planche.png", 2400)
    rendre(d / "planche.svg", out / "controle-1152.png", 1152)
    rendre(d / "vignette.svg", out / "controle-vignette-274.png", 274)
    rendre(d / "vignette.svg", out / "controle-vignette-296.png", 296)
    rendre(d / "appui.svg", out / "controle-appui-552.png", 552)
