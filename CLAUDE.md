# FT2E v3 — Site internet

> Site institutionnel de FT2E, société d'ingénierie pluridisciplinaire créée en 2008 et basée à La Rochelle. **v3 = fork de `ft2e-v2`** : contenus, collections et CMS identiques, design system : charte v3 « plans et profondeur » (révision 2, août 2026, bundle `branding-v3/`) — rampe monochrome 197° inchangée, relief par trois rangs d'ombre à l'encre translucide, filets 1 px hiérarchisés par l'opacité, trame 28 px, planche de page 1440 px posée sur calcaire, bouton principal en aplat encre. Build Astro statique, à déployer sur Vercel (`ft2e-v3.vercel.app`), destinée à migrer vers `ft2e.fr`.

## Quoi, exactement

Une **build Astro statique** fonctionnelle, déployée sur Vercel, qui :

1. Implémente intégralement le sitemap (Accueil, Société, Équipe, Expertises, Références, Fiche projet, Actualités, Article, Contact, pages légales).
2. Présente des fiches projets structurées (encore largement en `[DÉMO]` en attendant la phase de production).
3. Donne à voir le design system complet (rampe monochrome 197°, plans et ombres à l'encre, trame 28 px, typo Archivo + IBM Plex Mono, cartouches, nomenclature, monogramme).
4. Démontre les filtres de la page Références, le gabarit de fiche projet, le composant `HeroPage` unifié, la signature éditoriale, le JSON-LD, les performances.
5. Anime le tout via quatre mouvements vanilla (filet de flux 900 ms, révélation de plan 760 ms / 22 px, survols 300/260 ms) + View Transitions Astro, courbe unique `cubic-bezier(0.2, 0.7, 0.2, 1)`.

Ce qui n'est pas encore en place :

- Pas de Decap CMS configuré (juste les Content Collections Astro + Zod, prêtes à recevoir Decap).
- Pas de formulaire Contact branché (UI uniquement, sans backend).
- Pas encore migré sur `ft2e.fr` (déploiement Vercel sur `ft2e-v3.vercel.app`).
- **Indexation moteurs bloquée par triple sécurité** (robots.txt `Disallow: /`, meta `noindex` global, header HTTP `X-Robots-Tag`) tant que le site est en démo client. Procédure de revert exacte : `docs/19-migration-production.md`.
- Photos équipe (collective + 7 portraits individuels) et 8 visuels de fiches projet sont des **images de démonstration générées par IA** marquées `DÉMO` ; reportage photographique professionnel prévu en phase de production.

## Référentiel : le PDF de proposition stratégique + informations FT2E

La spécification initiale (positionnement, sitemap, modèle de contenu, filtres, gabarit fiche projet) **provient du PDF de proposition** (mai 2026). Les informations sur l'équipe et la société ont été précisées par FT2E le 2026-05-28 (voir `docs/00-vision-produit.md` et la mémoire `project-team-info`). Le design system provient de la charte v3 « FT2E Charte graphique » document 10 · révision 2 (`branding-v3/`, août 2026 — remplace la révision 1) ; en cas de conflit sur le design, **`.claude/rules/tailwind-design-tokens.md` (v3) et `docs/superpowers/specs/2026-08-06-ft2e-charte-v3-plans-profondeur.md` font foi** (`docs/superpowers/specs/2026-08-06-ft2e-charte-v2-monochrome-197.md` décrit la révision 1 monochrome, `docs/superpowers/specs/2026-08-04-ft2e-v2-ingenierie-invisible-design.md` le système cuivre intermédiaire, `docs/02-design-system.md` l'Apple-style v1 — conservés pour l'historique).

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

## Design system — charte v3 « Plans et profondeur » (rampe 197°)

Depuis 2026-08-06, le site applique la charte v3 (« FT2E Charte graphique » document 10 · révision 2, bundle `branding-v3/`) : la rampe 197° et le duotone sont inchangés — **une teinte unique, aucune couleur d'accent, l'état par défaut est clair** — mais **la profondeur remplace l'ornement** : le relief vient des plans (une planche posée, une planche qui déborde, une ligne encrée), portés par trois rangs d'ombre à l'encre translucide. Le rang d'un filet passe désormais par son **opacité** (1 px à 22/16/12 %), plus par son épaisseur ; la hiérarchie typographique par la graisse (Archivo 300/600/700) et la chasse. Source de vérité : `.claude/rules/tailwind-design-tokens.md` et `docs/superpowers/specs/2026-08-06-ft2e-charte-v3-plans-profondeur.md`.

### Palette (rampe 197° inchangée)

| Token | Hex | Usage |
|---|---|---|
| `profond` | `#001718` | **réserve — 1/5 max, 1×/écran** : ligne encrée (relevés), duotone, puce de section ; texte vedette sur papier |
| `encre` | `#00393a` | toute la lecture : titres, corps, aplat du bouton principal — et l'encre translucide des filets et ombres |
| `pivot` | `#336667` | données, dates, corps secondaire, focus ring (valeur client) — jamais en texte sur profond (3,67:1) |
| `clair` | `#99cccd` | texte **sur fonds sombres** ; sur papier : filets, aplats et complément des titres de section (décor, jamais porteur) |
| `voile` | `#e1f4f4` | pôle clair du duotone ; texte/équerres **sur réserve profonde uniquement** |
| `papier` | `#f7f9fa` | la planche de page (max 1440 px) et les plans posés (neutre) |
| `calcaire` | `#edf0f2` | fond sous la planche, cellules au repos, en-têtes (neutre) — jamais sous le voile |
| `filet-1/2/3` | `rgba(0,57,58,.22/.16/.12)` | trois rangs de filet 1 px — le rang est porté par l'opacité |
| `filet-chip` | `rgba(0,57,58,.28)` | étiquettes de mission, chips, bouton filaire |

Règles : 2 valeurs par composition (3 max) · une seule réserve profonde par écran (`bg-profond` / `.plan-encre`) · aucune teinte hors rampe, aucun dégradé · ombre = encre translucide, jamais du noir · alerte = filet doublé + mention, pas une couleur. Tous les anciens tokens (cuivre, marine, slate, mist, bleus, `line`/`line-strong`) sont des aliases repointés, interdits dans le nouveau code.

### Typographie — échelle v3

- **Archivo Variable** (`wdth` 62–125, graisses **300/600/700**) : Vedette `type-display` (125/700 capitales — **accueil uniquement**, une par page) ; **Titre d'écran** `type-ecran` (100/600, **casse normale, jamais capitales**, interligne 1,02 — h1 des pages internes) ; Section `type-section` (118/700 capitales, précédée de la puce 7 px, mot porteur encre + complément clair « /… ») ; Intitulé `type-intitule` (112/600) ; Corps 100/**300** interligne 1,6 ; Relevé `releve-chiffre` (118/700 tabulaire).
- **IBM Plex Mono** (400/**500/600**) : `mono-label` 11 px 0,14 em uppercase, `mono-data` 13 px tabulaire — tout ce qui est mesuré, référencé ou daté.
- Chargement fontsource, `font-display: swap`, pas de CDN Google.

### Plans et profondeur

- **Planche de page** (`BaseLayout.astro`) : papier `max-w-[1440px]` + trame 28 px à 7 % d'encre (`trame-fond`) + ombre de page `0 0 90px` encre 18 %, posée sur body calcaire.
- **Plan posé** `.plan-pose` (bordure 1 px `filet-2` obligatoire, ombre `0 24 60` 12 %) ; **plan qui déborde** `.plan-deborde` (`0 32 70` 16 %, chevauche de 40 px — une fois par écran max) ; **ligne encrée** `.plan-encre` (profond, filet clair 3 px à gauche, `0 30 64` 30 %) = la réserve profonde de l'écran.
- Aucune autre ombre, aucune ombre intérieure ni sur un texte ; la trame n'est jamais visible sous un plan.

### Navigation

- Barre fixe **claire** (`papier`), 56 px mobile / 74 px desktop, filet bas 1 px.
- Monogramme complet à gauche (cadre seul sur mobile, 28 px min) ; liens mono uppercase `pivot` → hover `encre` ; page courante `encre` + filet bas 1 px encre plein.

### Composant HeroPage

- `src/components/blocs/HeroPage.astro` — building block unique pour le hero de toutes les pages internes.
- Hero **clair** aligné à gauche : breadcrumb mono + eyebrow `mono-label pivot` + h1 `type-ecran` (**casse normale** — la vedette capitale est réservée à l'accueil) + sous-titre `pivot` + slot `metadata`. La barre de rang 4 px n'existe plus.
- Prop `size: 'default' | 'compact'` (compact = pages légales).
- Toutes les pages internes l'utilisent obligatoirement.

### Éléments signature

- **Monogramme** (`Logo.astro`) : cadre ouvert + flux débordant + lettres FT2E + baseline mono. Versions `principal`/`inverse`/`valeur-unique`, forme `cadre` sous 180 px, hauteur min 28 px. Le débord ne se recadre jamais ; ni ombre ni contour.
- **Cartouche** (`FicheTechnique.astro`, pied des vignettes `CarteProjet.astro`) : plan posé (bordure 1 px + ombre rang 1), en-tête calcaire, filets internes 1 px par rangs d'opacité, données mono — **plus de barre de rang 4 px**. Jamais centré.
- **Nomenclature** (`/references`) : liste tabulaire, pas de grille de cartes — rang par **opacité du filet gauche 1 px** (livré 22 % / en cours 16 % / archive 12 %, champ `statut` des fiches) et **graisse de l'intitulé** (700/600/300), tout sur une page.
- **Relevés** : relevé clair (`ChiffresCles` — le commentaire précède le chiffre, **un seul chiffre plein encre par bloc**, les autres `releve-retrait` encre 13 %) et relevé encré (`.plan-encre`, chiffres `releve-chiffre` voile, étiquettes mono clair) — la seule réserve profonde de l'écran (fiche projet).
- **Médias** : duotone 197° (`#001718` → `#E1F4F4`) via `duotone-photo` (sandwich lighten/darken) / `duotone-media` (hachure) + `CoinsCuivre` (équerres **voile** 1 px, 18 px, dans les angles) + annotations mono (2 max/image) ; rapports **21:8 / 16:10 / 3:2** seulement.
- **Boutons** : principal `.btn-principal` = **aplat encre**, filet clair 3 px à gauche, hover → profond 260 ms (le filet ne bouge pas) ; secondaire `.btn-filaire` 1 px 28 % ; `.btn-blueprint-solid` filaire clair sur profond. **Cellules de liste** `.cellule-liste` calcaire → papier au survol (300 ms). **Étiquettes** `.etiquette-mission` filaires, jamais d'aplat, six max par bloc.

### Layout

- Planche de page 1440 px sur calcaire ; conteneur principal `max-w-[1200px]` ; prose éditoriale `max-w-[840px]` ; **module 28 px** ; marge de page 60 px (44 px < 1200, 24 px à 390) ; 76 px entre sections ; gouttière 24 px.
- **Le papier gouverne**, tramé 28 px à 7 % ; les plans posés occultent la trame ; aucune section sombre décorative hors la ligne encrée.
- **Aucune ombre hors des trois rangs** (+ planche de page), **aucun rayon** (seule exception : puce de section, cercle 7 px).

### Motion design

- **Quatre mouvements, une seule courbe** `cubic-bezier(0.2, 0.7, 0.2, 1)` : filet de flux (`TraceFlux.astro`, 900 ms, une fois par chargement) ; révélation de plan (`[data-plan]`, 760 ms, 22 px, une fois à l'entrée dans la vue — observée par `BaseLayout`) ; survol de cellule (300 ms, calcaire → papier) ; survol de bouton (260 ms, encre → profond).
- Aucun compteur qui s'incrémente, aucun parallax, aucun hover lift, aucun filet qui s'épaissit ; survol = bascule de fond, **aucun déplacement** ; focus = 2 px pivot décalé 2 px.
- View Transitions Astro pour cross-fade entre pages ; `prefers-reduced-motion` respecté partout (tout posé d'emblée, fallback complet sans JS).
- Implémenté dans `src/styles/motion.css` + script `initPlans` de `BaseLayout.astro` + script du composant `TraceFlux.astro`.

## Règles non négociables

1. **Toute donnée métier de démo** (titre projet, MOA, surface, performance, chiffre) doit être **plausible** mais clairement signalée par le tag `[DÉMO]` dans le contenu Markdown ET par un badge visuel sur la page.
2. **L'équipe de sept personnes** (Mathieu, Géraldine, Sandrine, Vincent, Tanguy, Emma, Carole) est désignée uniformément par prénom dans toute la narration. Aucun membre n'est distingué individuellement — le bureau est porté collectivement. Les rôles (co-gérants associés, associés, collaborateurs) ne s'affichent que dans la grille structurée de la page Équipe, avec un traitement visuel identique pour tous les profils.
3. **Design system charte v3 « Plans et profondeur » (rampe 197°, trois rangs d'ombre, filets par opacité)** — voir `.claude/rules/tailwind-design-tokens.md` et la spec `docs/superpowers/specs/2026-08-06-ft2e-charte-v3-plans-profondeur.md`.
4. **Audit RGAA AA** dès le premier composant.
5. **Performance** : Lighthouse mobile ≥ 90 sur la home, 100/100/100 sur A11y / BP / SEO.
6. **Aucun lorem ipsum.** Tout texte est en français, conforme à la voix FT2E, et marqué `[DÉMO]` si non vérifié.
7. **Tout contenu = un `.md` dans `src/content/`.** Aucune donnée en dur.
8. **Toute nouvelle page interne** utilise le composant `HeroPage` pour son hero — garantit la cohérence visuelle (hero clair, breadcrumb mono, titre d'écran en casse normale).
9. **Tout `<script>` de composant Astro** qui appelle `addEventListener` doit s'initialiser via `document.addEventListener('astro:page-load', initX)` avec guard `dataset.bound`. Sinon le composant devient inerte après la première navigation View Transitions. Règle détaillée : `.claude/rules/astro-conventions.md` § « Scripts client & View Transitions ».
10. **Indexation moteurs bloquée** tant que le site est en démo Vercel (`ft2e-v3.vercel.app`). Trois fichiers verrouillent le SEO : `public/robots.txt`, `vercel.json`, valeur par défaut de `noindex` dans `BaseLayout.astro`. **Ne PAS débloquer sans validation FT2E**. Procédure de revert détaillée : `docs/19-migration-production.md`.

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
| Design tokens stricts | `.claude/rules/tailwind-design-tokens.md` (v3) — `docs/02-design-system.md` = historique v1 |
| **Spec charte v3 « plans et profondeur »** | **`docs/superpowers/specs/2026-08-06-ft2e-charte-v3-plans-profondeur.md`** |
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
