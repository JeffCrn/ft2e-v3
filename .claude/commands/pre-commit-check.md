---
description: Vérifications obligatoires avant commit
---

# Pre-commit check

Lance les vérifications suivantes **dans l'ordre**, et **stoppe immédiatement** si l'une échoue.

```bash
npm run lint
npm run typecheck
npm run build
npx markdownlint-cli2 "src/content/**/*.md" "docs/**/*.md"
```

## Si tout passe

- Affiche un récapitulatif des fichiers modifiés (`git status -s`).
- Propose un message de commit conforme à `.claude/rules/git-commit.md`.
- N'exécute **pas** le commit toi-même : laisse la main à l'utilisateur.

## Si quelque chose échoue

- Rapporte précisément la commande qui a échoué et son message d'erreur.
- Propose la correction si elle est triviale ; sinon **stoppe** et demande des instructions.

## Rappel

- Pas de commit anglais.
- Pas de push direct sur `main` sans validation explicite.
- Vérifier que les images ajoutées sont optimisées (AVIF/WebP, ≤ 200 KB chacune au-dessus du fold).
