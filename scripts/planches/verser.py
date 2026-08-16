#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Versement d'une planche sur le site — la bascule en une commande.

    python scripts/planches/verser.py <slug>

Ce que fait le script, dans l'ordre, en s'arrêtant à la première faute :

1. vérifie que le dossier `public/images/projets/<slug>/` porte les CINQ
   fichiers du protocole (`planche.json`, `planche.svg`, `vignette.svg`,
   `appui.svg`, `planche.png`) — ils ne se séparent pas ;
2. vérifie l'extraction : archétype nommé et `a_valider_ft2e` non vide (une liste
   vide signifie que la session n'a pas vu ce qu'elle tranchait, pas qu'il n'y
   avait rien à trancher) ;
3. vérifie le SVG : sous 40 Ko, `role="img"` + `aria-label`, ni `width` ni
   `height` sur la racine ;
4. écrit `planche:` dans le frontmatter de `src/content/projets/<slug>.md`
   (no-op si déjà fait), juste après le champ `mission_ft2e`.

⚠ Deux contrôles ont été RETIRÉS le 2026-08-16, parce qu'ils avaient survécu à
leur objet — un garde-fou qui contrôle ce qui n'existe plus ment sur ce qu'il
contrôle (même principe que l'amendement A9) :

- l'exigence d'« une forme de repli mobile que le site sait rendre ». Le repli
  de lecture textuel a été supprimé le 2026-08-15 : une figure de fiche, c'est
  le dessin, son cartouche et l'agrandissement, rien d'autre. Les quatre
  rendeurs d'archétype du composant sont partis avec lui, et CLAUDE.md consigne
  que le garde-fou de build l'a suivi. Celui-ci, lui, était resté ;
- la bascule `image_principale` → `planche:`. Le champ a été supprimé du schéma
  le même 2026-08-15. Sur une fiche neuve — donc dépourvue d'`image_principale`
  — la substitution ne trouvait rien et le script REFUSAIT le versement, en
  reprochant à la fiche l'absence d'un champ que le schéma lui interdit de
  porter. Le versement est désormais une insertion, pas un remplacement.

Il ne touche ni au build ni au dépôt : après lui, `npm run build` puis le
contrôle du rendu (règle 11 — un build vert ne prouve pas que la page
s'affiche), et le commit de fin de session emporte le tout.
"""

import io
import json
import re
import sys
from pathlib import Path


def faute(message):
    print(f"REFUS — {message}")
    sys.exit(1)


def main():
    if len(sys.argv) != 2:
        faute("usage : python scripts/planches/verser.py <slug>")
    slug = sys.argv[1].strip("/").split("/")[-1]
    racine = Path(__file__).resolve().parents[2]
    dossier = racine / "public" / "images" / "projets" / slug
    fiche = racine / "src" / "content" / "projets" / f"{slug}.md"

    # 1 — les cinq fichiers, ensemble (l'appui du hero depuis le 2026-08-14)
    if not dossier.is_dir():
        faute(f"pas de dossier {dossier}")
    if not fiche.is_file():
        faute(f"pas de fiche {fiche}")
    manquants = [f for f in ("planche.json", "planche.svg", "vignette.svg",
                             "appui.svg", "planche.png")
                 if not (dossier / f).is_file()]
    if manquants:
        faute(f"fichiers manquants dans {dossier.name}/ : {', '.join(manquants)}")

    # 2 — l'extraction
    extraction = json.loads((dossier / "planche.json").read_text(encoding="utf-8"))
    if not extraction.get("archetype"):
        faute("l’extraction ne nomme pas son archétype")
    if not extraction.get("a_valider_ft2e"):
        faute("a_valider_ft2e est vide — un dessin tranche toujours ce qu’un texte "
              "laisse ouvert (protocole, règle 2)")

    # 3 — le SVG
    svg = (dossier / "planche.svg").read_text(encoding="utf-8")
    if len(svg.encode("utf-8")) > 40 * 1024:
        faute("planche.svg dépasse 40 Ko")
    racine_svg = svg[:svg.index(">") + 1]
    if 'role="img"' not in racine_svg or "aria-label=" not in racine_svg:
        faute("la racine du SVG ne porte pas role=\"img\" + aria-label")
    if re.search(r'<svg[^>]*\s(width|height)=', racine_svg):
        faute("la racine du SVG porte width/height — elle ne doit pas "
              "(protocole, § Structure)")

    # 4 — la bascule
    contenu = fiche.read_text(encoding="utf-8")
    ligne_planche = f'planche: "/images/projets/{slug}/planche.svg"'
    if "planche:" in contenu.split("---", 2)[1]:
        print(f"déjà versé — le frontmatter de {slug}.md porte déjà `planche:`")
        return
    # Insertion après `mission_ft2e:`, parce que c’est là que le champ se trouve
    # sur les 23 fiches versées — relevé, pas supposé : 23 sur 23. Le champ est
    # partout une liste inline, donc une seule ligne. Ce fut un remplacement
    # d’`image_principale` tant que ce champ existait ; il a été supprimé du
    # schéma le 2026-08-15, et une fiche neuve n’en porte plus.
    nouveau = re.sub(r"^(mission_ft2e: .*\n)",
                     lambda m: m.group(1) + ligne_planche + "\n",
                     contenu, count=1, flags=re.M)
    if nouveau == contenu:
        faute(f"{slug}.md n’a pas de champ `mission_ft2e:` après lequel insérer la "
              "planche — insertion à faire à la main")
    io.open(fiche, "w", encoding="utf-8", newline="\n").write(nouveau)

    print(f"versé — {slug}.md pointe sur la planche ({extraction['archetype']})")
    print("reste à faire : npm run build, contrôle du rendu (fiche, carte de "
          "secteur, largeur téléphone), puis commit de fin de session")


if __name__ == "__main__":
    main()
