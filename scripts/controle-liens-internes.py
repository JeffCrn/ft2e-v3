# Contrôle des liens internes du Markdown — et du maillage minimal des fiches.
#
# À lancer sur `dist/`, jamais sur les sources seules :
#   npm run build && python scripts/controle-liens-internes.py
#
# Pourquoi ce contrôle existe. Astro en `output: 'static'` ne valide PAS les
# liens internes écrits dans le corps d'un Markdown : un `[texte](/references/x)`
# qui ne mène nulle part traverse le build en vert et se découvre en 404, à la
# main, ou jamais. Le 2026-08-09, six liens de `src/content/` pointaient depuis
# quatre mois vers des fiches supprimées le 2026-08-08 — personne ne l'avait vu.
# La passe de maillage de fin de chantier crée plus de cent liens : sans
# instrument, elle pourrirait de la même façon à la première fiche dépubliée.
#
# La source de vérité des cibles est `dist/`, pas la liste des fichiers de
# `src/content/` : c'est ce qui est RENDU qui répond en 200. Une collection dont
# la page de détail n'est pas engendrée (un secteur sans référence publiée, par
# exemple) n'est pas une cible valide, même si son `.md` existe.
import glob
import io
import os
import re
import sys

# Liens Markdown vers une route absolue du site. Les liens externes (http…),
# les ancres nues (#…) et les mailto: ne relèvent pas de ce contrôle.
RE_LIEN = re.compile(r'\[([^\]]*)\]\((/[^)\s]*)\)')

# Le maillage attendu par `.claude/rules/seo-geo.md` : cinq liens internes
# contextuels au minimum par page de contenu.
MINIMUM_PAR_FICHE = 5


def routes_publiees():
    """Les routes réellement engendrées, relevées sur les index.html de dist."""
    routes = set()
    for chemin in glob.glob('dist/**/index.html', recursive=True):
        route = os.path.dirname(chemin)[len('dist'):].replace(os.sep, '/')
        routes.add(route or '/')
    return routes


def liens_du_markdown():
    """Tous les liens absolus du contenu, fichier par fichier."""
    trouves = {}
    for chemin in sorted(glob.glob('src/content/**/*.md', recursive=True)):
        texte = io.open(chemin, encoding='utf8').read()
        # Le frontmatter n'est pas de la prose : il ne porte pas de maillage.
        corps = texte.split('\n---\n', 1)[-1]
        trouves[chemin.replace(os.sep, '/')] = RE_LIEN.findall(corps)
    return trouves


def main():
    routes = routes_publiees()
    if not routes:
        print('ECHEC : dist/ est vide — lancer `npm run build` d\'abord.')
        return 1

    liens = liens_du_markdown()
    morts, total = [], 0
    for chemin, refs in liens.items():
        for libelle, cible in refs:
            total += 1
            # Une ancre ou une chaîne de requête ne change pas la page visée.
            page = cible.split('#')[0].split('?')[0].rstrip('/') or '/'
            if page not in routes:
                morts.append((chemin, libelle, cible))

    fiches = {c: r for c, r in liens.items() if '/projets/' in c}
    sous_maillees = sorted(
        (c, len(r)) for c, r in fiches.items() if len(r) < MINIMUM_PAR_FICHE)

    print('%d routes publiées · %d liens internes dans %d fichiers de contenu.'
          % (len(routes), total, len(liens)))
    print('Liens morts : %d.' % len(morts))
    for chemin, libelle, cible in morts:
        print('  %-58s [%s](%s)' % (chemin, libelle, cible))

    print('Maillage des fiches : %d/%d atteignent %d liens.'
          % (len(fiches) - len(sous_maillees), len(fiches), MINIMUM_PAR_FICHE))
    for chemin, n in sous_maillees:
        print('  %-58s %d lien(s)' % (chemin, n))

    return 1 if (morts or sous_maillees) else 0


if __name__ == '__main__':
    sys.exit(main())
