# FT2E v2 — Site internet

> Site institutionnel de FT2E, société d'ingénierie pluridisciplinaire créée en 2008 et basée à La Rochelle. **v2 = fork de `ft2e-site`** : contenus, collections et CMS identiques, design system : charte v2 « l'ingénierie de l'invisible » monochrome 197° (Archivo à largeur variable + IBM Plex Mono, papier/encre/pivot sans accent, cartouches à barre de rang, filets 4/2/1 px, nomenclature). Build Astro statique, à déployer sur Vercel (`ft2e-v2.vercel.app`), destinée à migrer vers `ft2e.fr`.

## Quoi, exactement

Une **build Astro statique** fonctionnelle, déployée sur Vercel, qui :

1. Implémente intégralement le sitemap (Accueil, Société, Équipe, Expertises, Références, Fiche projet, Actualités, Article, Contact, pages légales).
2. Présente des fiches projets structurées (encore largement en `[DÉMO]` en attendant la phase de production).
3. Donne à voir le design system complet (rampe monochrome 197° papier/encre/pivot, typo Archivo + IBM Plex Mono, cartouches, nomenclature, monogramme).
4. Démontre les filtres de la page Références, le gabarit de fiche projet, le composant `HeroPage` unifié, la signature éditoriale, le JSON-LD, les performances.
5. Anime le tout via un système de motion design vanilla (hero reveal, scroll reveal, compteurs, View Transitions Astro), easing unique `cubic-bezier(0.16, 1, 0.3, 1)`.

Ce qui n'est pas encore en place :

- Pas de Decap CMS configuré (juste les Content Collections Astro + Zod, prêtes à recevoir Decap).
- Pas de formulaire Contact branché (UI uniquement, sans backend).
- Pas encore migré sur `ft2e.fr` (déploiement Vercel sur `ft2e-site.vercel.app`).
- **Indexation moteurs bloquée par triple sécurité** (robots.txt `Disallow: /`, meta `noindex` global, header HTTP `X-Robots-Tag`) tant que le site est en démo client. Procédure de revert exacte : `docs/19-migration-production.md`.
- Photos équipe (collective + 7 portraits individuels) et 8 visuels de fiches projet sont des **images de démonstration générées par IA** marquées `DÉMO` ; reportage photographique professionnel prévu en phase de production.

## Référentiel : le PDF de proposition stratégique + informations FT2E

La spécification initiale (positionnement, sitemap, modèle de contenu, filtres, gabarit fiche projet) **provient du PDF de proposition** (mai 2026). Les informations sur l'équipe et la société ont été précisées par FT2E le 2026-05-28 (voir `docs/00-vision-produit.md` et la mémoire `project-team-info`). Le design system provient de la charte v2 « FT2E Charte » v1.0 (`branding-v2/`, août 2026 — « document de référence · remplace toute version antérieure ») ; en cas de conflit sur le design, **`.claude/rules/tailwind-design-tokens.md` et `docs/superpowers/specs/2026-08-06-ft2e-charte-v2-monochrome-197.md` font foi** (`docs/superpowers/specs/2026-08-04-ft2e-v2-ingenierie-invisible-design.md` décrit le système cuivre intermédiaire, `docs/02-design-system.md` l'Apple-style v1 — conservés pour l'historique).

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

## Design system — charte v2 « Ingénierie de l'invisible » (monochrome 197°)

Depuis 2026-08-06, le site applique la charte v2 (« FT2E Charte » v1.0, bundle `branding-v2/`) : **une teinte unique (197°), cinq valeurs teintées, deux neutres, aucune couleur d'accent** — le cuivre n'existe plus. La hiérarchie passe par la valeur, l'épaisseur de trait (4/2/1 px) et la largeur de caractère (Archivo wdth 125→72). Source de vérité : `.claude/rules/tailwind-design-tokens.md` et `docs/superpowers/specs/2026-08-06-ft2e-charte-v2-monochrome-197.md`.

### Palette (rampe 197°)

| Token | Hex | Usage |
|---|---|---|
| `profond` | `#001718` | **réserve — 1/5 max, 1×/écran** : relevés, duotone, couverture ; texte vedette sur papier |
| `encre` | `#00393a` | toute la lecture : titres, filets porteurs, cadres, barres de rang |
| `pivot` | `#336667` | données, dates, corps de texte sur clair, filets 2ᵉ rang, focus ring (valeur client) |
| `clair` | `#99cccd` | étiquettes/texte **sur fonds sombres uniquement** (valeur client) |
| `voile` | `#e1f4f4` | pôle clair du duotone ; texte/équerres **sur réserve profonde uniquement** |
| `papier` | `#f7f9fa` | **fond par défaut de toute page** (neutre) |
| `calcaire` | `#edf0f2` | surface secondaire, hover de surface (neutre) — jamais sous le voile |
| `line` / `line-strong` | `rgba(0,57,58,.18)` / `.3` | filet d'indication / contour de cartouche |

Règles : 2 valeurs par composition (3 max) · jamais deux valeurs voisines en contact · aucun dégradé ni opacité de teinte · alerte = filet doublé + mention, pas une couleur. Tous les anciens tokens (cuivre, marine, slate, mist, bleus) sont des aliases repointés, interdits dans le nouveau code.

### Typographie — rangs documentés

- **Archivo Variable** (`wdth` 62–125) : Vedette `type-display` (125/700, une par page), Titre `type-h2` (118/600), Intitulé `type-intitule` (112/600), Courant (100/400 — plus de `font-light`), Annexe `type-annexe` (72/600).
- **IBM Plex Mono** (400/500) : `mono-label` 11 px 0,14 em uppercase, `mono-data` 13 px tabulaire — tout ce qui est mesuré, référencé ou daté.
- Chargement fontsource, `font-display: swap`, pas de CDN Google.

### Navigation

- Barre fixe **claire** (`papier`), 56 px mobile / 74 px desktop, filet bas `line`.
- Monogramme complet à gauche (cadre seul sur mobile) ; liens mono uppercase `pivot` → hover `encre` ; page courante `encre` + filet 2 px encre.

### Composant HeroPage

- `src/components/blocs/HeroPage.astro` — building block unique pour le hero de toutes les pages internes.
- Hero **clair** aligné à gauche : breadcrumb mono + eyebrow `mono-label pivot` + h1 `type-display text-profond` + **barre de rang 4 px encre** + sous-titre `pivot` + slot `metadata`.
- Prop `size: 'default' | 'compact'` (compact = pages légales).
- Toutes les pages internes l'utilisent obligatoirement.

### Éléments signature

- **Monogramme** (`Logo.astro`) : cadre ouvert + flux débordant + lettres FT2E + baseline mono. Versions `principal`/`inverse`/`valeur-unique`, forme `cadre` sous 180 px. Le débord ne se recadre jamais.
- **Cartouche** : barre de rang 4 px encre + cases de données mono (`FicheTechnique.astro`, pied des vignettes `CarteProjet.astro`). Jamais centré, jamais d'ombre.
- **Nomenclature** (`/references`) : liste tabulaire, pas de grille de cartes — rang du filet gauche 4/2/1 px = livré/en cours/archive (champ `statut` des fiches), largeur Archivo 118/100/72 assortie, tout sur une page.
- **Relevés** : `bg-profond` + chiffres Archivo 118/600 `voile` — la seule réserve profonde de l'écran (fiche projet).
- **Médias** : duotone 197° (`#001718` → `#E1F4F4`) via `duotone-photo` (sandwich lighten/darken) / `duotone-media` (hachure) + `CoinsCuivre` (équerres **voile** 1 px, 18/16/14 px, dans les angles) + annotations mono (2 max/image).
- Boutons **filaires** mono uppercase (`btn-blueprint-dark` 2 px encre = principal, `btn-blueprint` 1 px, `btn-blueprint-solid` clair sur sombre) — aucun bouton plein sans nécessité, le survol épaissit le filet d'un cran.

### Layout

- Conteneur principal : `max-w-[1200px]` ; prose éditoriale `max-w-[840px]` ; module 8 px ; rapports d'image 3:2 et 16:9 seulement.
- **Le papier gouverne** : fond global `papier`, bandes secondaires `calcaire border-t-2 border-encre`, CTA final `calcaire border-t-4 border-encre`. Plus de sections sombres décoratives.
- **Aucune ombre**, **aucun rayon** (2 px max inputs).

### Motion design

- **Un seul tracé animé sur tout le site** : le filet de flux (`TraceFlux.astro`), 900 ms, une fois par chargement, nœuds posés sur les frontières de sections. Aucun compteur qui s'incrémente, aucune apparition au défilement, aucun parallax, aucun hover lift.
- États interactifs : survol = filet épaissi d'un cran + intitulé à l'encre (200 ms) ; focus = 2 px pivot décalé 2 px.
- View Transitions Astro pour cross-fade entre pages ; `prefers-reduced-motion` respecté partout.
- Implémenté dans `src/styles/motion.css` (réduit à ~1 KB) + script du composant `TraceFlux.astro` (plus de script motion dans `BaseLayout.astro`).

## Règles non négociables

1. **Toute donnée métier de démo** (titre projet, MOA, surface, performance, chiffre) doit être **plausible** mais clairement signalée par le tag `[DÉMO]` dans le contenu Markdown ET par un badge visuel sur la page.
2. **L'équipe de sept personnes** (Mathieu, Géraldine, Sandrine, Vincent, Tanguy, Emma, Carole) est désignée uniformément par prénom dans toute la narration. Aucun membre n'est distingué individuellement — le bureau est porté collectivement. Les rôles (co-gérants associés, associés, collaborateurs) ne s'affichent que dans la grille structurée de la page Équipe, avec un traitement visuel identique pour tous les profils.
3. **Design system charte v2 « Ingénierie de l'invisible » (monochrome 197°)** — voir `.claude/rules/tailwind-design-tokens.md` et la spec `docs/superpowers/specs/2026-08-06-ft2e-charte-v2-monochrome-197.md`.
4. **Audit RGAA AA** dès le premier composant.
5. **Performance** : Lighthouse mobile ≥ 90 sur la home, 100/100/100 sur A11y / BP / SEO.
6. **Aucun lorem ipsum.** Tout texte est en français, conforme à la voix FT2E, et marqué `[DÉMO]` si non vérifié.
7. **Tout contenu = un `.md` dans `src/content/`.** Aucune donnée en dur.
8. **Toute nouvelle page interne** utilise le composant `HeroPage` pour son hero — garantit la cohérence visuelle (hero clair, breadcrumb mono, vedette au profond, barre de rang 4 px).
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
