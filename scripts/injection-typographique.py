# Injection typographique française — sessions du chantier références FT2E.
# `Write` normalise U+00A0 / U+202F : on les réinjecte ici, après coup.
# Conventions relevées dans le corpus (S13-S15) :
#   U+00A0 avant : ; ! ?  et autour des guillemets « »
#   U+202F entre nombre et unité, et comme séparateur de milliers (et avant €)
#   U+2019 pour l'apostrophe
import re, sys

NBSP, NNBSP, APO = ' ', ' ', '’'

# Unités, les plus longues d'abord (l'alternance regex est ordonnée).
UNITES = [
    'kWhep/m²/an', 'kWh/m²/an', 'm³/\\(h·m²\\)', 'W/\\(m²·K\\)', 'kg/m³', 'm³/h',
    'kWhep', 'kWh', 'kVA', 'kWc', 'Wc', 'kW', 'mbar', 'lumens', 'litres', 'lux', 'ans',
    'm²', 'm³', 'mm', 'cm', 'km', '°C', 'Pa', 'kg', 'lm', 'VA', 'dB', 'm', 'W', 'V', '%', '€',
]
RE_UNITE = re.compile(r'(\d)[ ](' + '|'.join(UNITES) + r')(?![A-Za-zÀ-ÿ0-9])')
RE_MILLE = re.compile(r'(\d)[ ](\d{3})(?!\d)')
RE_PONCT = re.compile(r'[ ]([;:!?])')


# Champs dont la valeur alimente une énumération Zod : elle doit correspondre au
# caractère près, apostrophe DROITE comprise (« Études d'exécution / BIM »).
# La ligne entière est mise à l'abri, valeur incluse — protéger la seule clé ne
# suffit pas, et courber l'apostrophe casse le build (piège relevé en session
# hors-programme du 2026-08-09, sur `secteurs/etudes-execution-bim.md`).
CLES_ENUM = ('secteur', 'typologie', 'mission_ft2e')


def protege(texte, chemin=''):
    """Sort les segments intouchables : code inline, valeurs d'énumération, clés YAML."""
    jetons = []

    def mettre(m):
        jetons.append(m.group(0))
        return '\x00%d\x00' % (len(jetons) - 1)

    # (a) code inline entre backticks — jamais de typographie à l'intérieur
    texte = re.sub(r'`[^`\n]*`', mettre, texte)
    # (b) lignes entières dont la valeur est une énumération Zod. Le `titre` d'une
    #     fiche secteur en fait partie : c'est lui que le champ `secteur` des
    #     fiches projet doit égaler.
    cles = CLES_ENUM + (('titre',) if '/secteurs/' in chemin.replace('\\', '/') else ())
    texte = re.sub(r'(?m)^(?:' + '|'.join(cles) + r'):.*$', mettre, texte)
    # (c) clés YAML du frontmatter : « titre: », « surface_m2: »… en début de ligne.
    #     La regex accepte les chiffres (piège relevé en session 15).
    texte = re.sub(r'(?m)^([A-Za-z_][A-Za-z_0-9]*:)', mettre, texte)
    return texte, jetons


def restitue(texte, jetons):
    return re.sub(r'\x00(\d+)\x00', lambda m: jetons[int(m.group(1))], texte)


def typographie(texte, chemin=''):
    texte, jetons = protege(texte, chemin)
    texte = texte.replace("'", APO)
    texte = RE_PONCT.sub(NBSP + r'\1', texte)
    texte = texte.replace('« ', '«' + NBSP).replace(' »', NBSP + '»')
    for _ in range(3):                      # 1 200 000 : deux passes utiles, la 3e est un filet
        texte = RE_MILLE.sub(r'\1' + NNBSP + r'\2', texte)
    texte = RE_UNITE.sub(r'\1' + NNBSP + r'\2', texte)
    return restitue(texte, jetons)


for chemin in sys.argv[1:]:
    with open(chemin, encoding='utf8') as f:
        avant = f.read()
    apres = typographie(avant, chemin)
    with open(chemin, 'w', encoding='utf8', newline='\n') as f:
        f.write(apres)
    print('%-72s  nbsp %3d  fine %3d  apostrophes %3d  droites restantes %d' % (
        chemin.split('/')[-1], apres.count(NBSP), apres.count(NNBSP),
        apres.count(APO), apres.count("'")))
