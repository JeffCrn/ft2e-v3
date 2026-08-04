---
description: Crée un nouveau composant Astro réutilisable
argument-hint: <NomComposant> [catégorie: primitives|blocs|layout]
---

# Nouveau composant — $ARGUMENTS

Délègue à l'agent `component-builder` la création d'un composant Astro réutilisable.

## Avant délégation

1. Vérifie que le composant n'existe pas déjà : `glob src/components/**/*.astro`.
2. Vérifie sa présence (ou non) dans `docs/05-bibliotheque-composants.md`.
3. Si l'utilisateur n'a pas précisé la catégorie, propose une catégorie (`primitives` / `blocs` / `layout`) et demande confirmation.

## Critères d'acceptation

- Composant typé strictement (interface TypeScript).
- Aucune dépendance externe non justifiée.
- Tokens Tailwind uniquement (aucune couleur hard-codée).
- Exemple d'usage en commentaire de tête.
- Entrée ajoutée à `docs/05-bibliotheque-composants.md`.
- `npm run typecheck && npm run build` passent.
