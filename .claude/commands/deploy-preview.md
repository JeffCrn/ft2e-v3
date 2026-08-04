---
description: Prépare et déclenche un déploiement de preview (recette OVH)
---

# Deploy preview — recette OVH

Procédure de déploiement d'une **preview de recette** sur l'URL technique OVH (de type `ft2e-recette.ovh.net`). Voir `docs/09-deploiement-ovh.md` pour le détail complet.

## Pré-requis

1. La branche courante n'est **pas** `main`.
2. Tous les checks `/pre-commit-check` sont au vert.
3. Le tag de version (si applicable) est défini.

## Étapes

```bash
# 1. Build local
npm run build

# 2. Vérifier la taille du bundle
du -sh dist/
ls -la dist/_astro/ | head -20

# 3. Vérifier les redirections (.htaccess)
cat dist/.htaccess 2>/dev/null || echo "Pas de .htaccess (à générer en phase de migration)"

# 4. Déclencher le déploiement via le workflow Git
git push origin <branche-courante>
```

## Vérifications post-déploiement

- Charger l'URL de recette dans un navigateur privé.
- Vérifier le certificat SSL (Let's Encrypt actif).
- Lancer Lighthouse mobile sur la home : `npx lighthouse <url-recette>`.
- Vérifier qu'aucun lien interne ne renvoie en 404.

## Rappel

- **Aucune donnée de production** sur la recette (formulaire de contact pointe vers une boîte de test si possible).
- Le déploiement vers `ft2e.fr` ne se fait **qu'après validation finale** par l'équipe associée de FT2E (voir `docs/12-cadrage-jalons.md`).
