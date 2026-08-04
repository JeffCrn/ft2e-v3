# 20 · Decap CMS — du mode démo à la production

> Note de cadrage rédigée le 2026-06-18. **Statut actuel : back-office Decap pleinement opérationnel sur l'URL live**, avec backend GitHub authentifié — l'édition affiche le vrai contenu et commit/redéploie. Solution **temporaire** : à refaire au passage en **hébergement souverain (OVH probable)**. Ce document liste l'état en place et les pistes de production.

## Ce qui est en place (live, fonctionnel)

- `public/admin/index.html` — charge Decap CMS **3.14.1** (version épinglée + intégrité SRI) depuis unpkg, page `noindex`, config chargée par chemin absolu (`<link rel="cms-config-url">`).
- `public/admin/config.yml` — `backend: name: github` (`repo: JeffCrn/ft2e-site`, `branch: master`, `base_url: https://ft2e-site.vercel.app`, `auth_endpoint: api/auth`). Après connexion GitHub, Decap lit/écrit le **vrai** contenu du dépôt.
- **Proxy OAuth** : fonctions serverless Vercel `api/auth.js` + `api/callback.js` (`client_secret` côté serveur ; `state` CSRF via CSPRNG+cookie ; origine postMessage figée ; anti-XSS). Variables d'env Vercel : `OAUTH_GITHUB_CLIENT_ID`, `OAUTH_GITHUB_CLIENT_SECRET`. OAuth App GitHub « FT2E CMS », callback `https://ft2e-site.vercel.app/api/callback`.
- **5 collections** alignées sur les schémas Zod (`src/content.config.ts`) : `projets`, `actualites`, `equipe`, `expertises`, `secteurs`.

### À montrer pendant la démo (2026-07-02) — sur l'URL live, sans machine locale

Décision FT2E (2026-06-18) : la démo se fait **directement sur `https://ft2e-site.vercel.app/admin/`**, sans poste de démo local. L'**authentification est repoussée** et sera montée au moment du passage en production (OVH ou autre) — l'utilisateur sollicitera EuporIA à ce moment-là.

Parcours démontrable sur l'URL live (vérifié le 2026-06-18) :
1. Ouvrir `https://ft2e-site.vercel.app/admin/` → bouton « Se connecter » (test-repo, aucune authentification).
2. Les **5 collections** s'affichent (Projets, Actualités, Équipe, Expertises, Secteurs).
3. Cliquer « ＋ Projet » → le **formulaire structuré complet** s'ouvre (titre, secteur, typologie, MOA, lieu, surface, année, performance, mission, image, badge démo, récit en markdown) **avec aperçu en direct**.

Message à FT2E : « Voici l'interface de gestion. Vous remplissez ce formulaire, l'aperçu se met à jour en direct. En production — une fois l'hébergement souverain choisi — ce formulaire enregistre et publie automatiquement (commit Git + mise en ligne). »

> ⚠️ Limites en `test-repo` (assumées pour la démo) : les collections démarrent **vides** (ce backend ne lit pas les fichiers du dépôt) et les modifications **ne sont pas sauvegardées**. C'est une **vitrine d'interface**, pas un backend opérationnel. Le contenu réel + la sauvegarde nécessitent l'authentification (voir ci-dessous), volontairement reportée.

### Option de test en local (non utilisée pour la démo, pour mémoire)

Pour éditer le **vrai contenu** en local sans authentification : ajouter `local_backend: true` au `config.yml`, lancer `npx decap-server` depuis la racine + `npm run dev`, puis ouvrir `http://localhost:4321/admin/index.html`. Vérifié le 2026-06-18 (les 8 projets et 7 membres se chargent et s'éditent réellement). Non activé dans le `config.yml` déployé, car la démo ne se fera pas en local.

## Ce qu'il restera à faire pour la production (à trancher)

### 1. Hébergement — décision préalable

FT2E s'oriente vers une **solution souveraine française (OVH)**. Le choix d'hébergeur conditionne le mécanisme d'authentification de Decap :

| Cible | Auth Decap recommandée | Remarque |
|---|---|---|
| **OVH (mutualisé / VPS)** | `git-gateway` auto-hébergé **ou** proxy OAuth GitHub déployé sur l'infra OVH | Souveraineté FR ; demande un petit service serveur pour l'OAuth |
| Vercel (si maintenu) | Fonctions `/api` (proxy OAuth GitHub) | Simple mais hébergement US |
| Netlify | Identity / git-gateway natif | Écarté (dépendance Netlify, cf. ADR-002) |

### 2. Backend Git réel

Remplacer le bloc `backend: test-repo` du `config.yml` par :

```yaml
backend:
  name: github          # ou gitlab / git-gateway selon l'hébergeur
  repo: <organisation>/ft2e-site
  branch: main
publish_mode: editorial_workflow   # brouillon → relecture → publication (via PR)
```

Le reste du `config.yml` (collections, champs) **ne bouge pas** : c'est la force du modèle Git-based — seul le bloc `backend` change.

### 3. Authentification

- **GitHub/GitLab OAuth** : créer une OAuth App dédiée, déployer un proxy OAuth (le `client_secret` reste côté serveur). Chaque rédacteur FT2E a besoin d'un compte Git.
- **`git-gateway` auto-hébergé** : pas de compte Git côté rédacteur, mais un service à maintenir.
- Décision à prendre avec FT2E selon leur tolérance (comptes GitHub vs service à héberger).

### 4. Médias & images

- Upload Decap → `public/images/` (dossier plat). Réorganisation manuelle vers `public/images/projets/<slug>/` en V1 (cf. ADR-002).
- Optimisation AVIF/WebP à automatiser ultérieurement (hook CI `sharp`).

## Cohérence Zod ↔ Decap — golden rule (toujours valable)

Toute modification d'un schéma dans `src/content.config.ts` se répercute dans `public/admin/config.yml` **au sein du même commit**. Exemple appliqué le 2026-06-18 : ajout du champ `role` à la collection `equipe`, synchronisé dans les deux fichiers.

## Référence

- ADR-002 (`adr/ADR-002-choix-decap-cms.md`) — pourquoi Decap.
- Doc 08 (`docs/08-configuration-decap.md`) — configuration de référence détaillée.
- Doc 19 (`docs/19-migration-production.md`) — séquence de mise en production du **site** (déblocage SEO inclus), à coordonner avec ce document.
