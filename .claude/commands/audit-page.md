---
description: Audit complet d'une page (perf, SEO, a11y, éditorial)
argument-hint: <route, ex: / ou /references/maison-pierre-loti>
---

# Audit complet — $ARGUMENTS

Audite la page **$ARGUMENTS** sur quatre axes, en parallèle si possible.

## Étapes

1. **Démarre le serveur dev** si nécessaire : `npm run dev` en arrière-plan.
2. **Délègue en parallèle** :
   - `seo-reviewer` → audit SEO/GEO de la route.
   - `a11y-auditor` → audit RGAA AA de la route.
   - `editorial-reviewer` → lecture du contenu visible de la route.
3. **Mesure performance** :
   ```bash
   npx lighthouse http://localhost:4321$ARGUMENTS \
     --only-categories=performance,accessibility,best-practices,seo \
     --emulated-form-factor=mobile \
     --output=json --output-path=./audits/<date>-<route>.json
   ```
4. **Compile** un rapport unique :
   - Scores Lighthouse (cibles : Perf ≥ 90 mobile, A11y 100, BP 100, SEO 100).
   - Top 3 problèmes par axe.
   - Plan d'action priorisé.

## Sortie

- Un fichier `audits/YYYY-MM-DD-<route-slug>.md` synthétisant tous les constats.
- Un rapport conversationnel synthétique à l'utilisateur.

## Critères de blocage

- Toute régression sur les scores cibles = action immédiate avant tout autre travail.
