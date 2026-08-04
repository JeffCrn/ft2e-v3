---
description: Crée une nouvelle page Astro à partir d'une spécification existante
argument-hint: <nom de la page tel que dans docs/04-specifications-pages.md>
---

# Nouvelle page — $ARGUMENTS

Tu vas implémenter la page **$ARGUMENTS** en suivant strictement sa spécification.

## Étapes

1. **Délègue** à l'agent `page-builder` (`.claude/agents/page-builder.md`).
2. **Vérifie** au préalable :
   - La spec existe dans `docs/04-specifications-pages.md`. Si elle manque, **demande** à l'utilisateur les éléments clés (sujet, hiérarchie, CTA, contenu).
   - La page n'existe pas déjà dans `src/pages/`.
3. **Après création**, lance :
   ```bash
   npm run typecheck
   npm run build
   ```
4. **Rapport** : ce qui a été fait, les `TODO:` restants (images, contenu CMS, micro-interactions).

## Critères d'acceptation

- La page passe le build.
- Métadonnées SEO complètes (`title`, `description`, `canonical`, `og_image`).
- JSON-LD approprié injecté.
- Un seul `<h1>`.
- Score Lighthouse ≥ 90 sur Performance, 100 sur Accessibilité, 100 sur SEO en local.
