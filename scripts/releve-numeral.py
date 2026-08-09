# Relevé de la convention numérale des récits de référence.
# Méthode : `.claude/rules/french-editorial.md` § Nombres et quantités.
#
# Ne sont comptés que les nombres qui qualifient DIRECTEMENT un nom
# dénombrable d'une liste close. Le périmètre est ce qui fait le chiffre :
# l'élargir à tout substantif happe des fragments de mesures et multiplie
# le total par trois. Toute reprise doit republier sa méthode avec ses
# chiffres, faute de quoi ils ne veulent rien dire.
#
# Usage :
#   python scripts/releve-numeral.py            # état du disque
#   python scripts/releve-numeral.py --head     # état du dernier commit
import glob
import io
import os
import re
import subprocess
import sys

NOMS = ['logement', 'chambre', 'lit', 'niveau', 'place', 'zone', 'lot',
        'bâtiment', 'étage', 'mission', 'semaine', 'réunion', 'réserve',
        'cotraitant', 'poste', 'maison', 'appartement']
NOMS = sorted(NOMS + [n + 's' for n in NOMS], key=len, reverse=True)
NOM = r'(?:' + '|'.join(NOMS) + r')\b'

# Le lexique est ENGENDRÉ, jamais tapé. Une liste écrite à la main s'arrête là
# où l'auteur a cessé d'imaginer des cas, et le compteur renvoie alors un zéro
# qui ressemble à une mesure : la première version de ce script s'arrêtait à
# « trente » et concluait « au-delà de trente, jamais de lettres » — alors qu'il
# y a « quarante-six chambres », « quarante-trois postes », « trente-deux
# réunions » au corpus. Le zéro était la forme du dictionnaire, pas celle du texte.
UNITES_MOT = ['', 'un', 'deux', 'trois', 'quatre', 'cinq', 'six', 'sept',
              'huit', 'neuf', 'dix', 'onze', 'douze', 'treize', 'quatorze',
              'quinze', 'seize']
DIZAINES_MOT = {20: 'vingt', 30: 'trente', 40: 'quarante', 50: 'cinquante',
                60: 'soixante', 80: 'quatre-vingt'}


def lexique():
    """Tous les cardinaux français de 2 à 100, composés et irréguliers compris."""
    mots = {UNITES_MOT[n]: n for n in range(2, 17)}
    for n in range(17, 20):
        mots['dix-' + UNITES_MOT[n - 10]] = n
    for base in (20, 30, 40, 50, 60, 80):
        racine = DIZAINES_MOT[base]
        mots[racine + ('s' if base == 80 else '')] = base
        mots['quatre-vingt-un' if base == 80 else racine + ' et un'] = base + 1
        for u in range(2, 10):
            mots['%s-%s' % (racine, UNITES_MOT[u])] = base + u
    # 70 et 90 se comptent sur soixante et quatre-vingt, augmentés de dix à
    # dix-neuf : soixante-dix = 60 + 10, quatre-vingt-dix-sept = 80 + 17.
    for racine, souche in (('soixante', 60), ('quatre-vingt', 80)):
        for reste in range(10, 20):
            mot = UNITES_MOT[reste] if reste < 17 else 'dix-' + UNITES_MOT[reste - 10]
            # « soixante et onze », mais « quatre-vingt-onze » : le `et` ne
            # s'emploie qu'avec soixante.
            liaison = ' et ' if (reste == 11 and souche == 60) else '-'
            mots[racine + liaison + mot] = souche + reste
    mots['cent'] = 100
    # `un` / `une` sont exclus : article aussi souvent que numéral.
    return {mot: valeur for mot, valeur in mots.items() if valeur >= 2}


MOTS = lexique()

# Espace ordinaire, insécable (U+00A0) ou fine insécable (U+202F).
ESPACE = r'[   ]'
RE_LETTRE = re.compile(
    r'\b(' + '|'.join(sorted(MOTS, key=len, reverse=True)) + r')' + ESPACE + NOM, re.I)
RE_CHIFFRE = re.compile(r'(?<![\w,])(\d+)' + ESPACE + r'(' + NOM + r')', re.I)

BANDES = [('de deux à neuf', 2, 9), ('de dix à trente', 10, 30),
          ('au-delà de trente', 31, 10 ** 9)]


def corps(texte):
    """Le récit seul : ce qui suit la fermeture du frontmatter."""
    return texte.split('\n---\n', 1)[-1]


def bande(valeur):
    for nom, bas, haut in BANDES:
        if bas <= valeur <= haut:
            return nom
    return None


def releve(lire, fichiers):
    compte = {(n, forme): [] for n, _, _ in BANDES for forme in ('lettres', 'chiffres')}
    for chemin in fichiers:
        texte = corps(lire(chemin))
        for motif, forme, valeur_de in (
                (RE_LETTRE, 'lettres', lambda m: MOTS[m.group(1).lower()]),
                (RE_CHIFFRE, 'chiffres', lambda m: int(m.group(1)))):
            for m in motif.finditer(texte):
                b = bande(valeur_de(m))
                if b:
                    compte[(b, forme)].append((os.path.basename(chemin), m.group(0)))
    return compte


def main():
    fichiers = sorted(glob.glob('src/content/projets/*.md'))
    if '--head' in sys.argv:
        def lire(chemin):
            ref = 'HEAD:' + chemin.replace(os.sep, '/')
            sortie = subprocess.run(['git', 'show', ref], capture_output=True)
            return sortie.stdout.decode('utf8')
        etat = 'dernier commit'
    else:
        def lire(chemin):
            return io.open(chemin, encoding='utf8').read()
        etat = 'disque'

    compte = releve(lire, fichiers)
    print('Relevé numéral — %d récits, état %s\n' % (len(fichiers), etat))
    print('%-20s %10s %10s' % ('bande', 'lettres', 'chiffres'))
    for nom, _, _ in BANDES:
        print('%-20s %10d %10d' % (nom, len(compte[(nom, 'lettres')]),
                                   len(compte[(nom, 'chiffres')])))

    # Les deux cases que la règle du tableau réprouve.
    for titre, cle in (('Sous dix, en chiffres', ('de deux à neuf', 'chiffres')),
                       ('De dix à trente, en lettres', ('de dix à trente', 'lettres'))):
        occurrences = compte[cle]
        print('\n%s — %d occurrence(s)' % (titre, len(occurrences)))
        for fichier, extrait in occurrences:
            print('    %-45s %s' % (fichier, extrait))


if __name__ == '__main__':
    main()
