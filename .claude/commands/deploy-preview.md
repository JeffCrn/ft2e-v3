---
description: Prépare et déclenche un déploiement Vercel
---

# Deploy — Vercel

Le projet est hébergé sur **Vercel** (`ft2e-v3.vercel.app`), en déploiement continu depuis la branche **`master`** du dépôt GitHub `JeffCrn/ft2e-v3`. La migration vers `ft2e.fr` n'est pas faite : voir `docs/19-migration-production.md`.

> `docs/09-deploiement-ovh.md` décrit l'hébergement OVH **envisagé au cadrage puis abandonné** — document d'historique, à ne pas suivre. Aucun `.htaccess`, aucune URL de recette OVH.

## Pré-requis

1. Les contrôles de `/pre-commit-check` sont au vert, **contrôle du rendu inclus**.
2. Les modifications sont commitées selon `.claude/rules/git-commit.md`.

## Déploiement

Un `git push origin master` suffit : Vercel construit et promeut en production automatiquement. C'est la voie normale.

```bash
git push origin master
```

Déploiement manuel (utile seulement si la chaîne GitHub est indisponible) — nécessite le CLI, absent par défaut de l'environnement :

```bash
npm i -g vercel      # si besoin
npx vercel deploy --prod --yes
```

## Vérifications post-déploiement

- Relever le hash du CSS servi et confirmer qu'il a changé si le style a été touché :
  `curl -s https://ft2e-v3.vercel.app/ | grep -o 'href="/_astro/[^"]*\.css"'`
- **Charger la page réellement modifiée** et la regarder (capture Playwright ou navigateur) — pas seulement l'accueil. Un déploiement `READY` ne garantit que la compilation.
- Lighthouse mobile sur la home : `npx lighthouse https://ft2e-v3.vercel.app --only-categories=performance,accessibility,best-practices,seo`.
- Vérifier qu'aucun lien interne ne renvoie en 404.

## Rappel

- L'indexation reste bloquée (robots.txt, meta `noindex`, header `X-Robots-Tag`) tant que FT2E n'a pas validé la mise en production — `docs/19-migration-production.md`.
- La mise en ligne sur `ft2e.fr` ne se fait **qu'après validation finale** par l'équipe associée de FT2E (`docs/12-cadrage-jalons.md`).
