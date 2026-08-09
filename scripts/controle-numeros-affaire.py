# Contrôle ADR-003 — le numéro d'affaire ne doit apparaître nulle part dans le
# HTML lisible. Il ne survit que dans `identifier` du JSON-LD, et c'est voulu.
#
# À lancer sur `dist/`, jamais sur les sources : c'est le rendu qui fuit.
#   npm run build && python scripts/controle-numeros-affaire.py
#
# Deux pièges que ce contrôle évite :
#  - un motif `\d{2}-\d{3}` nu produit des faux positifs (les récits SSI citent
#    les normes NF S 61-931, 61-932, 61-970). On ne cherche donc que les
#    numéros RÉELLEMENT relevés dans les frontmatters ;
#  - retirer le numéro du JSON-LD serait une régression, pas un succès : le
#    contrôle vérifie AUSSI qu'il y est encore.
import glob
import io
import os
import re
import sys

RE_LD = re.compile(r'<script type="application/ld\+json">.*?</script>', re.S)


def numeros_reels():
    trouves = {}
    for chemin in sorted(glob.glob('src/content/projets/*.md')):
        texte = io.open(chemin, encoding='utf8').read()
        m = re.search(r'(?m)^reference:\s*"([^"]+)"', texte)
        if m:
            trouves[m.group(1)] = os.path.basename(chemin)[:-3]
    return trouves


def main():
    numeros = numeros_reels()
    if not numeros:
        print('ECHEC : aucun numéro d\'affaire relevé dans les frontmatters.')
        return 1
    pages = sorted(glob.glob('dist/**/*.html', recursive=True))
    if not pages:
        print('ECHEC : dist/ est vide — lancer `npm run build` d\'abord.')
        return 1

    fuites, porteuses = [], set()
    for page in pages:
        html = io.open(page, encoding='utf8').read()
        for bloc in RE_LD.findall(html):
            for numero in numeros:
                if numero in bloc:
                    porteuses.add(numero)
        lisible = RE_LD.sub('', html)
        for numero, slug in numeros.items():
            if numero in lisible:
                i = lisible.find(numero)
                fuites.append((page, numero, slug, lisible[max(0, i - 70):i + 40]))

    print('%d numéros d\'affaire réels, %d pages HTML analysées.' % (len(numeros), len(pages)))
    print('JSON-LD : %d numéros sur %d présents en `identifier`.' % (len(porteuses), len(numeros)))
    manquants = sorted(set(numeros) - porteuses)
    if manquants:
        print('  ECHEC — disparus du JSON-LD : %s' % ', '.join(manquants))
    print('HTML lisible : %d fuite(s).' % len(fuites))
    for page, numero, slug, extrait in fuites:
        print('  %-60s %s (%s)' % (page, numero, slug))
        print('      …%s…' % extrait.replace('\n', ' '))

    return 1 if (fuites or manquants) else 0


if __name__ == '__main__':
    sys.exit(main())
