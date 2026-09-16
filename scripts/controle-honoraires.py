# Contrôle « aucun honoraire publié », sur les TROIS corpus servis.
#
# ⚠ Ne pas faire ce contrôle en `grep -P` : sur cette machine il refuse la
# locale (« -P supports only unibyte and UTF-8 locales ») et rend 0 — un zéro
# qui ressemble à un succès. Mesuré le 2026-09-16 : la sonde témoin, qui devait
# trouver un montant de travaux, rendait 0 elle aussi. C'est ainsi qu'on signe
# une conformité qu'on n'a pas mesurée.
import io, os, re, sys, glob

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MONTANT = re.compile(r'\d[\d\u00a0\u202f\u2009 ]*[,.]?\d*\s*(?:€|&#8364;|&euro;)')
TAUX = re.compile(r'taux[^.;]{0,40}?\d+[,.]?\d*\s*%', re.I)
MOTS = re.compile(r'honorair|rémunér|facturé', re.I)

def lire(p):
    return io.open(p, encoding='utf-8', errors='replace').read()

echecs = []

# --- 1. la prose -----------------------------------------------------------
n = 0
for f in glob.glob(os.path.join(R, 'src', 'content', 'projets', '*.md')):
    t = lire(f)
    if MOTS.search(t) or TAUX.search(t):
        echecs.append(('prose', os.path.basename(f), (MOTS.search(t) or TAUX.search(t)).group(0)))
    n += 1
print('1. PROSE          %d fiches — %d en faute' % (n, sum(1 for e in echecs if e[0] == 'prose')))

# --- 2. les JSON servis ----------------------------------------------------
# Le mot « honoraires » de la formule d'exclusion est LÉGITIME ; le chiffre non.
for corpus, motif in (('public', os.path.join(R, 'public', 'images', 'projets', '*', 'planche.json')),
                      ('dist', os.path.join(R, 'dist', 'images', 'projets', '*', 'planche.json'))):
    fichiers = glob.glob(motif)
    fautifs = [f for f in fichiers if MONTANT.search(lire(f)) or TAUX.search(lire(f))]
    for f in fautifs:
        echecs.append((corpus, os.path.basename(os.path.dirname(f)),
                       (MONTANT.search(lire(f)) or TAUX.search(lire(f))).group(0)))
    print('2. JSON %-9s %d fichiers — %d en faute' % (corpus, len(fichiers), len(fautifs)))
    assert fichiers, 'aucun planche.json trouvé dans %s — le contrôle ne mesure rien' % corpus

# --- 3. le HTML servi ------------------------------------------------------
pages = glob.glob(os.path.join(R, 'dist', 'references', '**', '*.html'), recursive=True)
assert len(pages) >= 47, 'pages de références trouvées : %d' % len(pages)
fautives = [p for p in pages if MOTS.search(lire(p)) or TAUX.search(lire(p))]
for p in fautives:
    echecs.append(('html', os.path.relpath(p, R), (MOTS.search(lire(p)) or TAUX.search(lire(p))).group(0)))
print('3. HTML servi     %d pages — %d en faute' % (len(pages), len(fautives)))

# --- SONDE TÉMOIN : un montant de TRAVAUX doit rester trouvable -------------
# Sans elle, les trois zéros ci-dessus pourraient venir d'un motif qui ne mord
# pas plutôt que d'un corpus propre.
temoin = [p for p in pages if MONTANT.search(lire(p))]
assert temoin, ('SONDE TÉMOIN EN ÉCHEC : aucun montant trouvé nulle part dans dist/references/. '
                'Le motif ne mord pas — les zéros ci-dessus ne valent rien.')
print('\nSonde témoin      %d pages portent encore un montant de TRAVAUX (attendu, c’est '
      'le chiffre du maître d’ouvrage)' % len(temoin))

if echecs:
    print('\n⛔ %d FAUTE(S) :' % len(echecs))
    for c, f, v in echecs:
        print('   %-8s %-44s %r' % (c, f, v))
    sys.exit(1)
print('\n✅ aucun honoraire, aucun taux de mission dans les trois corpus servis')
