---
description: Vérifications obligatoires avant commit
---

# Pre-commit check

Lance les vérifications suivantes **dans l'ordre**, et **stoppe immédiatement** si l'une échoue.

```bash
npm run typecheck   # `npm run lint` en est un alias strict — inutile de lancer les deux
npm run build
npx markdownlint-cli2 "src/content/**/*.md" "docs/**/*.md"
```

Puis, **obligatoirement si le diff touche un composant, une page, `src/styles/`, `tailwind` ou `.gitignore`** :

```bash
npm run preview     # puis capture de la page modifiée
```

Un build vert ne prouve que la compilation. Tailwind n'émet aucune erreur pour une classe qu'il n'a pas vue : seule la page rendue le montre. Contrôler **la page touchée**, pas l'accueil. Si le `.gitignore` a changé, vérifier en plus que `git check-ignore -v src/pages/<dossier>/index.astro` ne renvoie rien. Détail : `.claude/rules/astro-conventions.md` § Tailwind v4 et § Vérification du rendu.

## Si tout passe

- Affiche un récapitulatif des fichiers modifiés (`git status -s`).
- Propose un message de commit conforme à `.claude/rules/git-commit.md`.
- N'exécute **pas** le commit toi-même : laisse la main à l'utilisateur.

## Si quelque chose échoue

- Rapporte précisément la commande qui a échoué et son message d'erreur.
- Propose la correction si elle est triviale ; sinon **stoppe** et demande des instructions.

## Rappel

- Pas de commit anglais.
- La branche de travail du dépôt est **`master`** (il n'y a pas de `main`). Le workflow du projet commite et pousse sur `master` — mais **ne pousse jamais sans que l'utilisateur l'ait demandé**, le push déclenche la mise en production Vercel.
- Vérifier que les images ajoutées sont optimisées (AVIF/WebP, ≤ 200 KB chacune au-dessus du fold).
