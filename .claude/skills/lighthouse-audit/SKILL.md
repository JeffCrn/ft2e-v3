---
name: lighthouse-audit
description: Lance un audit Lighthouse complet (Performance, Accessibility, Best Practices, SEO) sur une route donnée, et produit un rapport structuré exploitable. À déclencher pour « audite la perf », « lance Lighthouse », « vérifie les Core Web Vitals ».
---

# Skill : Audit Lighthouse

## Quand lancer

- Avant tout commit qui touche au layout, aux assets ou à un composant rendu au-dessus du fold.
- À chaque jalon de livraison (cf. `docs/12-cadrage-jalons.md`).
- Sur la branche `main` après chaque déploiement de recette.

## Commande standard

```bash
mkdir -p audits

DATE=$(date +%Y-%m-%d)
ROUTE="${1:-/}"
SLUG=$(echo "$ROUTE" | sed 's|^/||' | sed 's|/|-|g')
[ -z "$SLUG" ] && SLUG="home"

npx lighthouse "http://localhost:4321${ROUTE}" \
  --only-categories=performance,accessibility,best-practices,seo \
  --emulated-form-factor=mobile \
  --throttling-method=simulate \
  --output=json,html \
  --output-path="./audits/${DATE}-${SLUG}" \
  --quiet \
  --chrome-flags="--headless --no-sandbox"
```

## Cibles de score

| Catégorie | Mobile | Desktop |
|---|---|---|
| Performance | ≥ 90 | ≥ 95 |
| Accessibility | **100** | **100** |
| Best Practices | **100** | **100** |
| SEO | **100** | **100** |

## Core Web Vitals — cibles strictes

| Métrique | Cible |
|---|---|
| LCP | < 1.8 s |
| INP | < 200 ms |
| CLS | < 0.05 |
| TBT | < 200 ms |
| FCP | < 1.5 s |
| Speed Index | < 2.5 s |

## Que faire des résultats

1. **Si tous les seuils sont tenus** : commit le rapport dans `audits/` et continue.
2. **Si une régression apparaît** :
   - Identifie la cause via la section « Opportunities » et « Diagnostics » du rapport HTML.
   - Causes fréquentes :
     - Images non optimisées (convertir en AVIF, dimensions exactes).
     - JS non-utilisé (vérifier les `client:*` Astro).
     - Police custom bloquante (vérifier `font-display: swap`).
     - CSS critique non inliné.
   - Corrige, relance.
3. **Si la régression vient d'une dépendance** : isoler dans une ADR et discuter avant d'élargir.

## Rapport synthétique attendu

À chaque audit, produis un résumé en 5 lignes max :

```
Route        : <route>
Date         : <YYYY-MM-DD>
Perf mobile  : <score> (LCP <s>, CLS <v>, TBT <ms>)
A11y         : <score>
Top fix      : <l'opportunité avec le plus gros gain estimé>
```
