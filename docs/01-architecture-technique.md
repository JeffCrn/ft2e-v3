# 01 · Architecture technique

## Stack canonique

| Couche | Choix | Version cible |
|---|---|---|
| Framework | **Astro** (génération statique) | 5.x |
| Styling | **Tailwind CSS** | 4.x |
| Langage | **TypeScript** strict | 5.x |
| CMS | **Decap CMS** | 3.x |
| Hébergement | **OVHcloud Webhosting Pro** | n/a |
| CDN / cache | OVH natif | n/a |
| Analytics | **Plausible** (RGPD) | hébergé EU |
| Formulaire | **Formspree** ou **n8n** auto-hébergé | à arbitrer |
| Polices | `@fontsource-variable/inter` | dernière |
| Runtime build | Node.js | 20 LTS |
| Gestionnaire de paquets | npm (par défaut) ou pnpm | dernière |

## Pourquoi Astro

Voir `adr/ADR-001-choix-astro.md`. En résumé :
- HTML statique servi → score Lighthouse élevé par construction.
- *Islands* permettent une interactivité ciblée sans le coût d'un SPA complet.
- TypeScript natif, content collections natives avec validation Zod.
- Communauté large, écosystème stable.

## Pourquoi Tailwind CSS 4

- Engine entièrement réécrit, performance multipliée.
- Tokens centralisés dans `tailwind.config.ts` (notre source de vérité).
- Pas de génération de classes inutiles (PurgeCSS intégré).

## Pourquoi Decap CMS

Voir `adr/ADR-002-choix-decap-cms.md`. En résumé :
- Open source, basé Git, **aucune dépendance SaaS payante**.
- Contenu = fichiers Markdown versionnés dans le dépôt = sauvegarde par construction.
- Portabilité du modèle de contenu (frontmatter YAML lisible par tout autre CMS).

## Dépendances autorisées

### Cœur (jamais débattues)

- `astro`, `@astrojs/check`, `@astrojs/sitemap`, `@astrojs/rss`
- `tailwindcss`, `@tailwindcss/vite`
- `@fontsource-variable/inter`
- `typescript`
- `decap-cms-app` (chargé uniquement à `/admin`)

### Optionnelles (ADR requise avant ajout)

- `@astrojs/preact` — uniquement si une *island* interactive complexe le justifie (ex. : filtres de la page Références).
- `@astrojs/image` ou Sharp pour optimisation d'images personnalisée.
- Librairie d'animation : **non installée par défaut**. Si besoin de transitions, View Transitions API natif d'Astro.

### Bannies par défaut

- ❌ React global, Vue, Svelte (poids JS injustifié pour un site institutionnel).
- ❌ jQuery (anachronique).
- ❌ Google Fonts en CDN (RGPD, performances).
- ❌ Bibliothèque d'icônes lourde — préférer SVG inline ou `iconify` avec tree-shaking.
- ❌ Tracker tiers (GA, Hotjar, Meta Pixel…).

## Variables d'environnement

```
# .env.example — à dupliquer en .env (jamais commité)
PUBLIC_SITE_URL=https://ft2e.fr
PUBLIC_PLAUSIBLE_DOMAIN=ft2e.fr
FORMSPREE_ENDPOINT=                  # ou URL webhook n8n
DECAP_GIT_TOKEN=                     # token pour git-gateway si self-hosted
```

## Structure de dépôt cible

```
ft2e-site/
├── .claude/                  # config Claude Code
├── docs/                     # cadrage (ce dossier)
├── adr/                      # Architecture Decision Records
├── audits/                   # rapports Lighthouse datés
├── content-models/           # schémas et docs des modèles
├── content-templates/        # gabarits de contenu
├── prompts/                  # prompts réutilisables
├── public/
│   ├── admin/                # interface Decap CMS
│   │   ├── config.yml
│   │   └── index.html
│   ├── images/               # médias servis
│   │   ├── projets/<slug>/
│   │   ├── equipe/
│   │   └── og/
│   ├── favicon.svg
│   └── robots.txt
├── src/
│   ├── content/
│   │   ├── config.ts         # schémas Zod
│   │   ├── projets/
│   │   ├── actualites/
│   │   ├── equipe/
│   │   ├── services/
│   │   └── secteurs/
│   ├── layouts/
│   │   ├── BaseLayout.astro
│   │   └── PageLayout.astro
│   ├── pages/
│   │   ├── index.astro
│   │   ├── societe.astro
│   │   ├── equipe.astro
│   │   ├── services/{index, [slug]}.astro
│   │   ├── references/{index, [slug]}.astro
│   │   ├── actualites/{index, [slug]}.astro
│   │   ├── contact.astro
│   │   └── accessibilite.astro
│   ├── components/
│   │   ├── primitives/
│   │   ├── blocs/
│   │   ├── layout/
│   │   └── seo/
│   ├── lib/
│   │   ├── constants.ts
│   │   └── utils/
│   └── styles/
│       └── global.css
├── tailwind.config.ts
├── astro.config.mjs
├── tsconfig.json
└── package.json
```

## Workflow de développement

```bash
# Setup initial (à exécuter une fois)
npm install
cp .env.example .env

# Boucle de dev
npm run dev               # serveur de développement
npm run typecheck         # vérification types
npm run lint              # linter
npm run build             # build prod
npm run preview           # serveur du build prod local
```

## CI/CD (à mettre en place après scaffolding)

- **GitHub Actions** ou **GitLab CI** selon hébergement du dépôt.
- Pipeline minimal sur chaque PR : lint → typecheck → build → Lighthouse en mode headless.
- Déploiement automatique vers la recette OVH sur push de la branche `recette`.
- Déploiement vers `ft2e.fr` uniquement sur push de la branche `main`, **après validation manuelle**.

## Décisions différées (V2+)

- Mode sombre (`docs/02-design-system.md` § « Mode sombre »).
- Pages géolocalisées par commune (V2 SEO).
- Recherche interne sur le site (FlexSearch ou Pagefind).
- Espace presse / téléchargements (plaquettes, dossier de presse).
