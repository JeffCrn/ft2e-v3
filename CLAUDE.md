# FT2E — Site internet

> Site institutionnel de FT2E, société d'ingénierie pluridisciplinaire créée en 2008 et basée à La Rochelle. Build Astro statique, déployée sur Vercel (`ft2e-site.vercel.app`), destinée à migrer vers `ft2e.fr`. Esthétique Apple-style, navigation glass, motion design vanilla.

## Quoi, exactement

Une **build Astro statique** fonctionnelle, déployée sur Vercel, qui :

1. Implémente intégralement le sitemap (Accueil, Société, Équipe, Expertises, Références, Fiche projet, Actualités, Article, Contact, pages légales).
2. Présente des fiches projets structurées (encore largement en `[DÉMO]` en attendant la phase de production).
3. Donne à voir le design system complet (palette Apple-style, typo Inter, composants).
4. Démontre les filtres de la page Références, le gabarit de fiche projet, le composant `HeroPage` unifié, la signature éditoriale, le JSON-LD, les performances.
5. Anime le tout via un système de motion design vanilla (hero reveal, scroll reveal, card tilt 3D, nav glass dynamique, View Transitions Astro).

Ce qui n'est pas encore en place :

- Pas de Decap CMS configuré (juste les Content Collections Astro + Zod, prêtes à recevoir Decap).
- Pas de formulaire Contact branché (UI uniquement, sans backend).
- Pas encore migré sur `ft2e.fr` (déploiement Vercel sur `ft2e-site.vercel.app`).
- **Indexation moteurs bloquée par triple sécurité** (robots.txt `Disallow: /`, meta `noindex` global, header HTTP `X-Robots-Tag`) tant que le site est en démo client. Procédure de revert exacte : `docs/19-migration-production.md`.
- Photos équipe (collective + 7 portraits individuels) et 8 visuels de fiches projet sont des **images de démonstration générées par IA** marquées `DÉMO` ; reportage photographique professionnel prévu en phase de production.

## Référentiel : le PDF de proposition stratégique + informations FT2E

La spécification initiale (positionnement, sitemap, modèle de contenu, filtres, gabarit fiche projet) **provient du PDF de proposition** (mai 2026). Les informations sur l'équipe et la société ont été précisées par FT2E le 2026-05-28 (voir `docs/00-vision-produit.md` et la mémoire `project-team-info`). Le design system a été refondu vers une esthétique Apple-style ; en cas de conflit sur le design, **`docs/02-design-system.md` et `.claude/rules/tailwind-design-tokens.md` font foi**.

## Stack — versions en production

| Couche | Choix | Version |
|---|---|---|
| Framework | Astro (génération statique) | 6.x |
| Styling | Tailwind CSS | 4.x |
| Langage | TypeScript strict | 5.x |
| Polices | `@fontsource-variable/inter` | dernière |
| Runtime build | Node.js | 20+ |
| Hébergement | **Vercel** (déploiement continu via GitHub) | n/a |
| View Transitions | `astro:transitions/ClientRouter` | natif |

## Design system — esthétique Apple-style

Le design system adopte les codes visuels Apple. Source de vérité : `docs/02-design-system.md` et `.claude/rules/tailwind-design-tokens.md`.

### Palette

| Token | Hex | Usage |
|---|---|---|
| `marine-deep` | `#0f2436` | hero, CTA final, nav solidifiée — fond le plus immersif |
| `marine` | `#16324f` | sections sombres, **titres** (`h1`–`h6`) sur fond clair, nav |
| `marine-surface` | `#1d3a57` | cartes sur fond sombre |
| `marine-surface-2` | `#223f5e` | variation de surface sombre |
| `cool-white` | `#edf1f5` | fonds de section alternés, cartes, footer |
| `near-black` | `#1d1d1f` | **body** (texte courant) sur fond clair — inchangé |
| `slate` | `#45535f` | texte secondaire, légendes, baseline sur fond clair |
| `mist` | `#9fb0bf` | texte secondaire, baseline sur fond marine |
| `apple-blue` | `#0071e3` | CTA principal, accent d'action |
| `link-blue` | `#0066cc` | liens texte sur fond clair |
| `bright-blue` | `#2997ff` | liens sur fond sombre (sur `marine-deep` uniquement, voir a11y) |
| `copper` | `#c46a38` | accent d'identité (logo, eyebrow, filet) — fond clair |
| `bright-copper` | `#d98a55` | accent d'identité (logo, eyebrow) — fond sombre |
| `pure-black` | `#000000` | **legacy** — n'est plus utilisé pour les surfaces (remplacé par `marine-deep`) |

### Typographie

- **Police unique : Inter Variable** (substitute libre de SF Pro). Pas de Manrope.
- Chargement via `@fontsource-variable/inter`. `font-display: swap` obligatoire.
- Headings : `font-semibold` (600), `line-height: 1.07`, `letter-spacing: -0.02em`.
- Texte courant : `font-normal` (400), `line-height: 1.47`.

### Navigation

- Glass nav fixe, hauteur 48 px.
- Sur hero sombre (`data-hero-dark`) : transparente au chargement, puis se solidifie au scroll (`bg-marine-deep/80` + `backdrop-blur(20px)` + `saturate(180%)`).
- Sur les autres pages : opaque dès le chargement.

### Composant HeroPage

- `src/components/blocs/HeroPage.astro` — building block unique pour le hero de toutes les pages internes.
- Hero marine profond + breadcrumb intégré (theme dark) + eyebrow + h1 + sous-titre + slot `metadata`.
- Prop `size: 'default' | 'compact'` (compact = pages légales).
- Toutes les pages internes l'utilisent obligatoirement.

### Boutons & cartes

- Boutons : **pill shape** (`border-radius: 980px`).
- Cartes : **pas de bordures**, fond plein ou transparent.

### Layout

- Conteneur principal : `max-w-[980px]`.
- Sections alternées marine / blanc / blanc froid.

### Ombre

- Une seule ombre autorisée : `3px 5px 30px rgba(0, 0, 0, 0.22)`.

### Motion design

- Système vanilla JS/CSS (~14 KB gzip total, zéro dépendance externe).
- Hero reveal mot par mot (40 ms stagger), scroll reveal IntersectionObserver, card tilt 3D, nav glass dynamique, compteur pulse, parallax CTA, chevron animé, filtre Références animé.
- View Transitions Astro pour cross-fade entre pages.
- Toutes les animations respectent `prefers-reduced-motion`.
- Implémenté dans `src/styles/motion.css` + script inline dans `src/layouts/BaseLayout.astro`.

## Règles non négociables

1. **Toute donnée métier de démo** (titre projet, MOA, surface, performance, chiffre) doit être **plausible** mais clairement signalée par le tag `[DÉMO]` dans le contenu Markdown ET par un badge visuel sur la page.
2. **L'équipe de sept personnes** (Mathieu, Géraldine, Sandrine, Vincent, Tanguy, Emma, Carole) est désignée uniformément par prénom dans toute la narration. Aucun membre n'est distingué individuellement — le bureau est porté collectivement. Les rôles (co-gérants associés, associés, collaborateurs) ne s'affichent que dans la grille structurée de la page Équipe, avec un traitement visuel identique pour tous les profils.
3. **Design system Apple-style** — voir `docs/02-design-system.md` et `.claude/rules/tailwind-design-tokens.md`.
4. **Audit RGAA AA** dès le premier composant.
5. **Performance** : Lighthouse mobile ≥ 90 sur la home, 100/100/100 sur A11y / BP / SEO.
6. **Aucun lorem ipsum.** Tout texte est en français, conforme à la voix FT2E, et marqué `[DÉMO]` si non vérifié.
7. **Tout contenu = un `.md` dans `src/content/`.** Aucune donnée en dur.
8. **Toute nouvelle page interne** utilise le composant `HeroPage` pour son hero — garantit la cohérence visuelle et la nav glass correcte.
9. **Tout `<script>` de composant Astro** qui appelle `addEventListener` doit s'initialiser via `document.addEventListener('astro:page-load', initX)` avec guard `dataset.bound`. Sinon le composant devient inerte après la première navigation View Transitions. Règle détaillée : `.claude/rules/astro-conventions.md` § « Scripts client & View Transitions ».
10. **Indexation moteurs bloquée** tant que le site est sur `ft2e-site.vercel.app` (démo). Trois fichiers verrouillent le SEO : `public/robots.txt`, `vercel.json`, valeur par défaut de `noindex` dans `BaseLayout.astro`. **Ne PAS débloquer sans validation FT2E**. Procédure de revert détaillée : `docs/19-migration-production.md`.

## Workflow

- Lire `docs/04-specifications-pages.md` pour chaque page à construire.
- Lire `docs/18-contenus-demonstration.md` pour savoir quels contenus de démo utiliser.
- Avant commit : `npm run build` (échec = blocage).
- Après commit + push : `npx vercel deploy --prod --yes` pour déployer.

## Où trouver quoi

| Besoin | Fichier |
|---|---|
| Vision produit | `docs/00-vision-produit.md` |
| Audit du site précédent | `docs/15-audit-site-actuel.md` |
| Périmètre du livrable | `docs/17-perimetre-livrable.md` |
| Écosystème clients FT2E | `docs/16-ecosysteme-clients.md` |
| Contenus de démonstration | `docs/18-contenus-demonstration.md` |
| Architecture technique | `docs/01-architecture-technique.md` |
| Design tokens stricts | `docs/02-design-system.md` |
| Modèle de contenu | `docs/03-modele-contenu.md` |
| Spécifications page-par-page | `docs/04-specifications-pages.md` |
| Bibliothèque de composants | `docs/05-bibliotheque-composants.md` |
| SEO/GEO | `docs/06-strategie-seo-geo.md` |
| Conformité RGAA/RGPD | `docs/07-conformite-rgaa-rgpd.md` |
| Configuration Decap CMS | `docs/08-configuration-decap.md` |
| Déploiement | `docs/09-deploiement-ovh.md` (à actualiser pour Vercel) |
| Performance budget | `docs/10-budget-performance.md` |
| Voix éditoriale | `docs/11-voix-editoriale.md` |
| Calendrier 6 phases | `docs/12-cadrage-jalons.md` |
| Glossaire BET | `docs/13-glossaire-bet.md` |
| **Migration vers `ft2e.fr` (revert SEO inclus)** | **`docs/19-migration-production.md`** |

## Commandes disponibles

- `/nouvelle-fiche-projet`, `/nouvelle-page`, `/nouveau-composant`, `/audit-page`, `/pre-commit-check`, `/deploy-preview`

## Voix du projet

> **« Sobre, technique, chaleureuse. »** Trois adjectifs que FT2E partage avec EuporIA Factory. Aucun superlatif, aucun jargon marketing, aucune promesse chiffrée non vérifiable. Précision métier (RT2012, RE2020, BIM, SSI, CFO/CFA) et chaleur d'équipe pluridisciplinaire.
