# FT2E v2 — Site internet

> Site institutionnel de FT2E, société d'ingénierie pluridisciplinaire créée en 2008 et basée à La Rochelle. **v2 = fork de `ft2e-site`** : contenus, collections et CMS identiques, design system remplacé par « l'ingénierie de l'invisible » (blueprint technique : Archivo condensé uppercase + IBM Plex Mono, encre/marine/cuivre, cartouches, filets 1 px). Build Astro statique, à déployer sur Vercel (`ft2e-v2.vercel.app`), destinée à migrer vers `ft2e.fr`.

## Quoi, exactement

Une **build Astro statique** fonctionnelle, déployée sur Vercel, qui :

1. Implémente intégralement le sitemap (Accueil, Société, Équipe, Expertises, Références, Fiche projet, Actualités, Article, Contact, pages légales).
2. Présente des fiches projets structurées (encore largement en `[DÉMO]` en attendant la phase de production).
3. Donne à voir le design system complet (palette encre/marine/cuivre, typo Archivo + IBM Plex Mono, composants blueprint).
4. Démontre les filtres de la page Références, le gabarit de fiche projet, le composant `HeroPage` unifié, la signature éditoriale, le JSON-LD, les performances.
5. Anime le tout via un système de motion design vanilla (hero reveal, scroll reveal, compteurs, View Transitions Astro), easing unique `cubic-bezier(0.16, 1, 0.3, 1)`.

Ce qui n'est pas encore en place :

- Pas de Decap CMS configuré (juste les Content Collections Astro + Zod, prêtes à recevoir Decap).
- Pas de formulaire Contact branché (UI uniquement, sans backend).
- Pas encore migré sur `ft2e.fr` (déploiement Vercel sur `ft2e-site.vercel.app`).
- **Indexation moteurs bloquée par triple sécurité** (robots.txt `Disallow: /`, meta `noindex` global, header HTTP `X-Robots-Tag`) tant que le site est en démo client. Procédure de revert exacte : `docs/19-migration-production.md`.
- Photos équipe (collective + 7 portraits individuels) et 8 visuels de fiches projet sont des **images de démonstration générées par IA** marquées `DÉMO` ; reportage photographique professionnel prévu en phase de production.

## Référentiel : le PDF de proposition stratégique + informations FT2E

La spécification initiale (positionnement, sitemap, modèle de contenu, filtres, gabarit fiche projet) **provient du PDF de proposition** (mai 2026). Les informations sur l'équipe et la société ont été précisées par FT2E le 2026-05-28 (voir `docs/00-vision-produit.md` et la mémoire `project-team-info`). Le design system v2 provient du bundle Claude Design « Ingénierie de l'invisible » (`FT2E Démo V2.dc.html`, 2026-08-04) ; en cas de conflit sur le design, **`docs/superpowers/specs/2026-08-04-ft2e-v2-ingenierie-invisible-design.md` et `.claude/rules/tailwind-design-tokens.md` font foi** (`docs/02-design-system.md` décrit l'ancien système Apple-style de la v1 et n'est conservé que pour l'historique).

## Stack — versions en production

| Couche | Choix | Version |
|---|---|---|
| Framework | Astro (génération statique) | 6.x |
| Styling | Tailwind CSS | 4.x |
| Langage | TypeScript strict | 5.x |
| Polices | `@fontsource-variable/archivo` (axe wdth) + `@fontsource/ibm-plex-mono` | dernière |
| Runtime build | Node.js | 20+ |
| Hébergement | **Vercel** (déploiement continu via GitHub) | n/a |
| View Transitions | `astro:transitions/ClientRouter` | natif |

## Design system — « Ingénierie de l'invisible » (blueprint technique)

Le site ressemble à un document d'ingénierie : cartouches, filets 1 px, annotations mono, chiffres tabulaires, coins cuivre, médias duotone. Source de vérité : `.claude/rules/tailwind-design-tokens.md` et `docs/superpowers/specs/2026-08-04-ft2e-v2-ingenierie-invisible-design.md`.

### Palette

| Token | Hex | Usage |
|---|---|---|
| `encre` (= `marine-deep`) | `#08131f` | nav, hero, footer, CTA final |
| `marine` | `#16324f` | **titres** sur fond clair, texte fort |
| `marine-surface` / `-2` | `#0e2233` / `#123049` | surfaces sur fond encre |
| `cool-white` | `#edf0f2` | fond clair principal, texte sur encre |
| `paper` | `#f7f9fa` | surface claire secondaire, hover, encarts |
| `slate` | `#4a6076` | corps de texte et labels sur fond clair |
| `mist` | `#8fa2b4` | labels et texte secondaire **sur encre uniquement** |
| `copper` | `#c46a38` | filets, bordures, coins, texte sur encre |
| `bright-copper` | `#e08a50` | hover liens et annotations sur encre |
| `copper-text` | `#a04e20` | petit texte cuivre sur fond clair (contraste ≥ 5:1) |
| `line` / `line-strong` | `rgba(74,96,118,.35)` / `#4a6076` | filets standard / cartouches |

Plus de bleu d'action : le cuivre porte l'identité **et** l'interaction (hover, focus ring). Les tokens bleus et Apple de la v1 sont des aliases repointés, à ne plus utiliser.

### Typographie

- **Archivo Variable** (axe `wdth` via `font-stretch` 112–125 %) : titres condensés-larges **uppercase**, corps 300.
- **IBM Plex Mono** (400/500) : labels 11 px `tracking .14em` uppercase, données 13 px tabulaires, nav, boutons.
- Classes recettes globales : `type-display`, `type-h2`, `mono-label`, `mono-data`, `filet-top`, `btn-blueprint*`, `chip-blueprint`, `duotone-media`, `duotone-photo`.
- Chargement fontsource, `font-display: swap`, pas de CDN Google.

### Navigation

- Barre fixe **opaque** encre, 56 px mobile / 74 px desktop, filet bas `mist/25`.
- Liens mono uppercase `mist` → hover `bright-copper` ; page courante `cool-white` + filet cuivre.
- Plus de glass/blur ni de nav transparente (le script navGlass a été supprimé).

### Composant HeroPage

- `src/components/blocs/HeroPage.astro` — building block unique pour le hero de toutes les pages internes.
- Hero encre aligné à gauche + breadcrumb mono intégré (theme dark) + eyebrow cuivre + h1 `type-display` + sous-titre `mist` + slot `metadata`.
- Prop `size: 'default' | 'compact'` (compact = pages légales).
- Toutes les pages internes l'utilisent obligatoirement.

### Boutons, cartes & médias

- Boutons : **rectangles mono uppercase** (`btn-blueprint-dark` plein encre sur clair, `btn-blueprint-solid` plein clair sur encre, `btn-blueprint` filaire). Jamais de pill.
- Cartes : **bordure 1 px** (`border-line`), hover `border-copper`, fond `paper` — pas d'ombre, pas de rayon.
- Cartouches : grilles bordées `gap-px bg-line` (chiffres clés, fiche technique).
- Médias : `duotone-media` (placeholder hachuré) / `duotone-photo` (photo duotone) + composant `CoinsCuivre` (équerres 16 px).

### Layout

- Conteneur principal : `max-w-[1200px]` ; prose éditoriale `max-w-[840px]`.
- Fond global `cool-white`, sections encre pour hero/CTA (avec `border-t border-copper`).

### Ombre & rayons

- **Aucune ombre** (`--shadow-soft: none`). **Aucun rayon** (2 px max sur les inputs).

### Motion design

- Système vanilla JS/CSS (~14 KB gzip total, zéro dépendance externe).
- Hero reveal mot par mot (40 ms stagger), scroll reveal IntersectionObserver (12 px), compteur pulse, parallax CTA, chevron animé, filtre Références animé. Easing unique `--ease-blueprint` (le tilt 3D et la nav glass de la v1 ont été supprimés).
- Dispositifs blueprint (2026-08-05) : tracé de flux cuivre suivant le scroll (`TraceFlux.astro`), filet cuivre animé (`filet-trace`), hover lift 2 px sur les cartes. `SchemaTechnique.astro` retiré du hero (chantier en attente d'une solution plus impactante). Détail : `.claude/rules/tailwind-design-tokens.md` § « Dispositifs de couleur structurante ».
- View Transitions Astro pour cross-fade entre pages.
- Toutes les animations respectent `prefers-reduced-motion`.
- Implémenté dans `src/styles/motion.css` + script inline dans `src/layouts/BaseLayout.astro`.

## Règles non négociables

1. **Toute donnée métier de démo** (titre projet, MOA, surface, performance, chiffre) doit être **plausible** mais clairement signalée par le tag `[DÉMO]` dans le contenu Markdown ET par un badge visuel sur la page.
2. **L'équipe de sept personnes** (Mathieu, Géraldine, Sandrine, Vincent, Tanguy, Emma, Carole) est désignée uniformément par prénom dans toute la narration. Aucun membre n'est distingué individuellement — le bureau est porté collectivement. Les rôles (co-gérants associés, associés, collaborateurs) ne s'affichent que dans la grille structurée de la page Équipe, avec un traitement visuel identique pour tous les profils.
3. **Design system « Ingénierie de l'invisible »** — voir `.claude/rules/tailwind-design-tokens.md` et la spec `docs/superpowers/specs/2026-08-04-ft2e-v2-ingenierie-invisible-design.md`.
4. **Audit RGAA AA** dès le premier composant.
5. **Performance** : Lighthouse mobile ≥ 90 sur la home, 100/100/100 sur A11y / BP / SEO.
6. **Aucun lorem ipsum.** Tout texte est en français, conforme à la voix FT2E, et marqué `[DÉMO]` si non vérifié.
7. **Tout contenu = un `.md` dans `src/content/`.** Aucune donnée en dur.
8. **Toute nouvelle page interne** utilise le composant `HeroPage` pour son hero — garantit la cohérence visuelle (hero encre, breadcrumb mono, eyebrow cuivre).
9. **Tout `<script>` de composant Astro** qui appelle `addEventListener` doit s'initialiser via `document.addEventListener('astro:page-load', initX)` avec guard `dataset.bound`. Sinon le composant devient inerte après la première navigation View Transitions. Règle détaillée : `.claude/rules/astro-conventions.md` § « Scripts client & View Transitions ».
10. **Indexation moteurs bloquée** tant que le site est en démo Vercel (`ft2e-v2.vercel.app`). Trois fichiers verrouillent le SEO : `public/robots.txt`, `vercel.json`, valeur par défaut de `noindex` dans `BaseLayout.astro`. **Ne PAS débloquer sans validation FT2E**. Procédure de revert détaillée : `docs/19-migration-production.md`.

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
| Design tokens stricts | `.claude/rules/tailwind-design-tokens.md` (v2) — `docs/02-design-system.md` = historique v1 |
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
| Faits vérifiés issus de la plaquette 2024 (références réelles, chiffres, qualifications) | `docs/20-source-plaquette-2024.md` |

## Commandes disponibles

- `/nouvelle-fiche-projet`, `/nouvelle-page`, `/nouveau-composant`, `/audit-page`, `/pre-commit-check`, `/deploy-preview`

## Voix du projet

> **« Sobre, technique, chaleureuse. »** Trois adjectifs que FT2E partage avec EuporIA Factory. Aucun superlatif, aucun jargon marketing, aucune promesse chiffrée non vérifiable. Précision métier (RT2012, RE2020, BIM, SSI, CFO/CFA) et chaleur d'équipe pluridisciplinaire.
