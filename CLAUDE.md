# FT2E v3 — Site internet

> Site institutionnel de FT2E, société d'ingénierie pluridisciplinaire créée en 2008 et basée à La Rochelle. **v3 = fork de `ft2e-v2`** : contenus, collections et CMS identiques, design system : charte v3 « plans et profondeur » **révision 2.1** (08.2026, bundle `branding-v3-bis/`) — rampe monochrome 197° inchangée, relief par trois rangs d'ombre à l'encre translucide, filets 1 px hiérarchisés par l'opacité, trame 28 px, planche de page 1440 px posée sur calcaire, bouton principal en aplat encre. Build Astro statique, à déployer sur Vercel (`ft2e-v3.vercel.app`), destinée à migrer vers `ft2e.fr`.

## Quoi, exactement

Une **build Astro statique** fonctionnelle, déployée sur Vercel, qui :

1. Implémente intégralement le sitemap (Accueil, Société, Équipe, Expertises, Références, Fiche projet, Actualités, Article, Contact, pages légales).
2. Présente **vingt-trois fiches projets réelles**, sourcées pièce par pièce sur les dossiers d'affaires FT2E. **Plus aucune fiche de démonstration : les huit `demo: true` ont été supprimées le 2026-08-08 à la demande de FT2E.**
2 bis. **Illustre chaque fiche par une planche de schéma de principe** — un dessin FT2E composé à partir de sa propre matière technique, sans aucune géométrie d'ouvrage ni œuvre de tiers. **Chantier ouvert le 2026-08-12, CLOS le 2026-08-15 : 23 planches sur 23, vingt-trois mécanismes distincts.** Bilan de clôture et points ouverts (au premier rang : la régénération des vingt planches antérieures à la 21) : `docs/superpowers/plans/2026-08-12-chantier-planches-references.md`.
3. Donne à voir le design system complet (rampe monochrome 197°, plans et ombres à l'encre, trame 28 px, typo Archivo + IBM Plex Mono, cartouches, nomenclature, monogramme).
4. Démontre les filtres de la page Références, le gabarit de fiche projet, le composant `HeroPage` unifié, la signature éditoriale, le JSON-LD, les performances.
5. Anime le tout via quatre mouvements vanilla (filet de flux 900 ms, révélation de plan 760 ms / 22 px, survols 300/260 ms) + View Transitions Astro, courbe unique `cubic-bezier(0.2, 0.7, 0.2, 1)`.

Ce qui n'est pas encore en place :

- **Decap CMS est configuré** (`public/admin/config.yml`, cinq collections, backend GitHub via le proxy OAuth `api/auth.js` + `api/callback.js` sur Vercel) — il reste à le faire valider et prendre en main par FT2E. Toute modification d'un schéma Zod se répercute dans `config.yml` **au sein du même commit** (sous-agent `content-modeller`).
- Pas de formulaire Contact branché (UI uniquement, sans backend).
- Pas encore migré sur `ft2e.fr` (déploiement Vercel sur `ft2e-v3.vercel.app`).
- **Indexation moteurs bloquée par triple sécurité** (robots.txt `Disallow: /`, meta `noindex` global, header HTTP `X-Robots-Tag`) tant que le site est en démo client. Procédure de revert exacte : `docs/19-migration-production.md`.
- Photos équipe (collective + 7 portraits individuels) et visuels de secteurs sont des **images de démonstration générées par IA** marquées `DÉMO` ; reportage photographique professionnel prévu en phase de production. Les visuels des treize fiches réelles, eux, sont authentiques (perspectives d'architecte, vues de dossier, extraits de nos propres plans).
- **Marqueurs `[DÉMO]` restants : 8, tous des `image_alt`** (7 dans `src/content/secteurs/`, 1 dans l'unique actualité). Ils marquent des visuels de démonstration générés par IA et **se lèvent au reportage photographique**, pas par une validation FT2E. Les **10 marqueurs en prose ont été levés le 2026-08-09** : chaque exemple fictif a été remplacé par un exemple relevé sur une des 19 fiches réelles, avec lien interne vivant — au passage, les six liens `/references/…` de `src/content/` étaient **tous morts** depuis la suppression des fiches de démonstration.
- **Secteur `Monotechnique` sans référence publiée** depuis la suppression des démos : sa seule fiche était `chaufferie-pac-ecole-la-flotte` (`demo: true`). Le secteur reste présent sur `/secteurs` mais disparaît du filtre de `/references` tant qu'il est vide ; les sessions 20 à 22 du chantier doivent le peupler (Passerelle de Marans, cuisine de Villedoux, faisabilité Dufour).

## Référentiel : le PDF de proposition stratégique + informations FT2E

La spécification initiale (positionnement, sitemap, modèle de contenu, filtres, gabarit fiche projet) **provient du PDF de proposition** (mai 2026). Les informations sur l'équipe et la société ont été précisées par FT2E le 2026-05-28 (voir `docs/00-vision-produit.md` et la mémoire `project-team-info`). Le design system provient de la charte v3 « FT2E Charte graphique » document 10 · **révision 2.1** (`branding-v3-bis/`, 08.2026 — remplace la révision 2 `branding-v3/`, elle-même successeur de la révision 1 `branding-v2/`). La 2.1 garde la structure de la 2 et corrige **huit prescriptions** (registre des amendements A1–A8, § 16 de la charte, reporté dans `.claude/rules/tailwind-design-tokens.md`) ; en cas de conflit sur le design, **`.claude/rules/tailwind-design-tokens.md` (v3) et `docs/superpowers/specs/2026-08-06-ft2e-charte-v3-plans-profondeur.md` font foi** (`docs/superpowers/specs/2026-08-06-ft2e-charte-v2-monochrome-197.md` décrit la révision 1 monochrome, `docs/superpowers/specs/2026-08-04-ft2e-v2-ingenierie-invisible-design.md` le système cuivre intermédiaire, `docs/02-design-system.md` l'Apple-style v1 — conservés pour l'historique).

## Stack — versions en production

| Couche | Choix | Version |
|---|---|---|
| Framework | Astro (génération statique) | 6.x |
| Styling | Tailwind CSS | 4.x |
| Langage | TypeScript strict | 6.x |
| Polices | `@fontsource-variable/archivo` (axe wdth) + `@fontsource/ibm-plex-mono` | dernière |
| Runtime build | Node.js | 20+ |
| Hébergement | **Vercel** (déploiement continu via GitHub) | n/a |
| View Transitions | `astro:transitions/ClientRouter` | natif |

## Design system — charte v3 « Plans et profondeur » · révision 2.1 (rampe 197°)

Depuis 2026-08-08, le site applique la charte v3 **révision 2.1** (« FT2E Charte graphique » document 10, bundle `branding-v3-bis/`) : la rampe 197° et le duotone sont inchangés — **une teinte unique, aucune couleur d'accent, l'état par défaut est clair** — mais **la profondeur remplace l'ornement** : le relief vient des plans (une planche posée, une planche qui déborde, une ligne encrée), portés par trois rangs d'ombre à l'encre translucide. Le rang d'un filet passe désormais par son **opacité** (1 px à 22/16/12 %), plus par son épaisseur ; la hiérarchie typographique par la graisse (Archivo **300/400/600/700** — quatre graisses depuis l'amendement A7) et la chasse. Source de vérité : `.claude/rules/tailwind-design-tokens.md` et `docs/superpowers/specs/2026-08-06-ft2e-charte-v3-plans-profondeur.md`.

### Palette (rampe 197° inchangée)

| Token | Hex | Usage |
|---|---|---|
| `profond` | `#001718` | **réserve — 1/5 max, 1×/écran** : ligne encrée (relevés), duotone, puce de section ; texte vedette sur papier |
| `encre` | `#00393a` | toute la lecture : titres, corps, aplat du bouton principal — et l'encre translucide des filets et ombres |
| `pivot` | `#336667` | données, dates, chapô, chiffres de relevé en retrait, anneau de focus en polarité claire — **jamais en texte ni en filet porteur sur profond** (2,85:1) |
| `clair` | `#99cccd` | texte **sur fonds sombres** ; sur papier : filets, aplats et complément des titres de section (décor, jamais porteur) |
| `voile` | `#e1f4f4` | pôle clair du duotone ; texte/équerres **sur réserve profonde uniquement** |
| `papier` | `#f7f9fa` | la planche de page (max 1440 px) et les plans posés (neutre) |
| `calcaire` | `#edf0f2` | fond sous la planche, cellules au repos, en-têtes (neutre) — jamais sous le voile |
| `filet-1/2/3` | `#00393a38/29/1f` | trois rangs de filet 1 px — le rang est porté par l'opacité (22/16/12 %) |
| `filet-clair-1/2` | `#99cccd59/2e` | filets en polarité profonde (35/18 %) — le pivot y est interdit |
| `filet-chip` | `#00393a47` | étiquettes de mission, chips, bouton filaire (28 %) |

Règles : 2 valeurs par composition (3 max) · une seule réserve profonde par écran (`bg-profond` / `.plan-encre`) · aucune teinte hors rampe, aucun dégradé · ombre = encre translucide, jamais du noir · alerte = filet doublé + mention, pas une couleur. **Hygiène du dépôt (rév. 2.1 § 17) : tous les anciens tokens (cuivre, marine, slate, mist, bleus, `line`/`line-strong`) ont été SUPPRIMÉS de `global.css` — un jeton nommé d'après une identité antérieure ne se redirige pas.**

### Typographie — échelle v3

- **Archivo Variable** (`wdth` 62–125, graisses **300/400/600/700**) : Vedette `type-display` (125/700 capitales — **accueil uniquement**, une par page) ; **Titre d'écran** `type-ecran` (100/600, **casse normale, jamais capitales**, interligne 1,02 — h1 des pages internes) ; Section `type-section` (118/700 capitales, puce 7 px, mot porteur encre + complément clair « /… » **`aria-hidden`**) ; Intitulé `type-intitule` (112/600) ; **Corps 100/400 interligne 1,6** (amendement A7) ; **Chapô `type-chapo`** (100/**300**, 19–22 px, interligne 1,5, **en pivot**, trois lignes au plus — le seul emploi de la 300) ; Relevé `releve-chiffre` (118/700 tabulaire).
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
- **Nomenclature** (`/references`) : liste tabulaire, pas de grille de cartes — **titre COURT** (celui de la planche, lu par `titreCourt()`), le titre long du frontmatter restant au `<h1>` de la fiche et au référencement. La **vignette croît avec le palier** — masquée sous md, 160 px de md à lg, 220 px à xl — et la ligne passe de quatre colonnes à deux sous lg, le secteur et le statut se rangeant sous le titre — rang par **opacité du filet gauche 1 px** (livré 22 % / en cours 16 % / archive 12 %, champ `statut` des fiches) et **graisse de l'intitulé** (700/600/300), tout sur une page.
- **Relevés** : relevé clair (composé dans `src/pages/index.astro` — le commentaire précède le chiffre, **un seul chiffre plein encre par bloc**, les autres `releve-retrait` encre 13 %) et relevé encré (`.plan-encre`, chiffres `releve-chiffre` voile, étiquettes mono clair) — la seule réserve profonde de l'écran (fiche projet).
- **Médias** : duotone 197° (`#001718` → `#E1F4F4`) via `duotone-photo` (sandwich lighten/darken) / `duotone-media` (hachure) + `CoinsCuivre` (équerres **voile** 1 px, 18 px, en retrait de 5 px dans les angles) + annotations mono (2 max/image) ; rapports **21:8 / 16:10 / 3:2** seulement.
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

## Les planches de références — le dispositif visuel des fiches

Depuis le 2026-08-12, une fiche de référence n'est plus illustrée par une photographie mais
par une **planche de schéma de principe** : un dessin FT2E tiré de la matière technique de
la fiche — topologie, flux, chiffres — qui ne reproduit **aucune géométrie d'ouvrage**, ne
nomme **aucun tiers** et ne porte **aucune donnée commerciale**.

Deux motifs, l'un juridique et l'autre éditorial. Les visuels précédents exposaient le
bureau au droit d'auteur des architectes — neuf perspectives publiées sans qu'aucun crédit
ait jamais été obtenu, douze extraits reproduisant leur fond de plan. Et un extrait de plan
au 1/50 réduit à 581 px puis passé au duotone ne démontre rien : le code en portait l'aveu,
la miniature de `/references` était à la fois `hidden md:block` et `aria-hidden`.

**Cinq pièces par fiche**, dans `public/images/projets/<slug>/` :

| Fichier | Rôle |
|---|---|
| `planche.json` | l'extraction — la pièce que FT2E relit, **et** la source du repli de lecture sous 1024 px |
| `planche.svg` | la planche, `viewBox 0 0 1200 800`, lue à 1152 px (échelle 0,96) |
| `vignette.svg` | la vignette de carte, `viewBox 0 0 300 200`, lue à 274-296 px |
| `appui.svg` | l'appui du hero de l'accueil, `viewBox 0 0 552 368`, lu à ~552 px (fiche `en_avant`) |
| `planche.png` | 2400 × 1600 — contrôle, impression, et `og:image` de la fiche |

**Trois principes de rendu, chacun mesuré :**

1. **Le SVG est inliné, jamais appelé en `<img src>`** — un SVG en `src` est un document
   isolé qui ne reçoit ni les polices ni les jetons de la page.
2. **La planche occupe la largeur du conteneur, sans padding de plan** : elle porte ses
   propres marges de 56 et *est* le plan posé. Dans la colonne de 581 px de l'ancien visuel,
   son mono de 10 px tomberait à 3,9.
3. **Sous `lg`, le dessin cède la place à sa lecture**, composée depuis le `planche.json` —
   à 358 px l'échelle vaut 0,30, aucun schéma ne s'y lit.

**Ni duotone ni équerres** : les deux appartiennent à la photographie, et la planche est
déjà composée dans les jetons.

**La vignette est une composition, pas un recadrage.** Trois cadrages successifs de la
planche ont été essayés et rejetés : un dessin composé pour 1200 px et lu à 290 tombe à
l'échelle 0,24, quel que soit l'endroit où on le découpe.

| Besoin | Fichier |
|---|---|
| Protocole de production (à coller en session neuve) | `docs/superpowers/specs/2026-08-12-planches-references-protocole.md` |
| Compositeurs, un par archétype | `scripts/planches/<archetype>.py` (tronc commun : `scripts/planches/_tronc.py`) |
| Versement d'une planche sur sa fiche | `scripts/planches/verser.py <slug>` — contrôles puis bascule du frontmatter |
| Bilan de clôture du chantier et points ouverts | `docs/superpowers/plans/2026-08-12-chantier-planches-references.md` |
| Rendu | `src/components/blocs/PlancheReference.astro` |

## Règles non négociables

1. **Toute donnée métier de démo** (titre projet, MOA, surface, performance, chiffre) doit être **plausible** mais clairement signalée par le tag `[DÉMO]` dans le contenu Markdown ET par un badge visuel sur la page.
2. **L'équipe de sept personnes** (Mathieu, Géraldine, Sandrine, Vincent, Tanguy, Emma, Carole) est désignée uniformément par prénom dans toute la narration. Aucun membre n'est distingué individuellement — le bureau est porté collectivement. Les rôles (co-gérants associés, associés, collaborateurs) ne s'affichent que dans la grille structurée de la page Équipe, avec un traitement visuel identique pour tous les profils.
3. **Design system charte v3 « Plans et profondeur » — révision 2.1** (rampe 197°, trois rangs d'ombre, filets par opacité, **huit amendements A1–A8**) — voir `.claude/rules/tailwind-design-tokens.md` (§ Les huit amendements) et la spec `docs/superpowers/specs/2026-08-06-ft2e-charte-v3-plans-profondeur.md`. La charte prévaut sur tout support existant ; **en cas de contradiction interne à la charte, la mesure prévaut sur la règle**.
4. **Audit RGAA AA** dès le premier composant.
5. **Performance** : Lighthouse mobile ≥ 90 sur la home, 100/100/100 sur A11y / BP / SEO.
6. **Aucun lorem ipsum.** Tout texte est en français, conforme à la voix FT2E, et marqué `[DÉMO]` si non vérifié.
7. **Tout contenu = un `.md` dans `src/content/`.** Aucune donnée en dur.
8. **Toute nouvelle page interne** utilise le composant `HeroPage` pour son hero — garantit la cohérence visuelle (hero clair, breadcrumb mono, titre d'écran en casse normale).
9. **Tout `<script>` de composant Astro** qui appelle `addEventListener` doit s'initialiser via `document.addEventListener('astro:page-load', initX)` avec guard `dataset.bound`. Sinon le composant devient inerte après la première navigation View Transitions. Règle détaillée : `.claude/rules/astro-conventions.md` § « Scripts client & View Transitions ».
10. **Une fiche projet réelle porte son numéro d'affaire FT2E** (`reference`, graphie `NN-NNN`, relevé sur une pièce FT2E) ; `annee` est le millésime d'**ouverture** qu'encode ce numéro, `annee_livraison` la réception prononcée. **Ne jamais fabriquer un identifiant à partir d'un autre champ.** Détail : `.claude/rules/content-collections.md`.
11. **Un build vert ne prouve pas que la page s'affiche.** Après toute modification de mise en page, de `global.css` ou du `.gitignore`, contrôler le **rendu** de la page touchée (`npm run preview` + capture). Tailwind v4 lit le `.gitignore` : un motif non ancré supprime silencieusement les classes d'un répertoire source. Détail : `.claude/rules/astro-conventions.md`.
12. **Indexation moteurs bloquée** tant que le site est en démo Vercel (`ft2e-v3.vercel.app`). Trois fichiers verrouillent le SEO : `public/robots.txt`, `vercel.json`, valeur par défaut de `noindex` dans `BaseLayout.astro`. **Ne PAS débloquer sans validation FT2E**. Procédure de revert détaillée : `docs/19-migration-production.md`.
13. **Une planche ne se recadre pas, ne se duotone pas, ne s'illustre pas.** Elle se compose à la taille où elle est lue — 1200 px pour la planche, 300 px pour la vignette — et se contrôle **à cette taille**, jamais en pleine page. Toute valeur qu'elle porte est citable dans la fiche ; tout ce que le dessin a dû trancher va dans `a_valider_ft2e`. Protocole : `docs/superpowers/specs/2026-08-12-planches-references-protocole.md`.

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
| **Chantier des 23 fiches références réelles** (programme, protocole, suivi) | **`docs/superpowers/plans/2026-08-07-chantier-references-reelles.md`** |
| **Planches de références — protocole de production** | **`docs/superpowers/specs/2026-08-12-planches-references-protocole.md`** |
| **Planches de références — bilan de clôture et points ouverts** | **`docs/superpowers/plans/2026-08-12-chantier-planches-references.md`** |
| **Remasterisation de `/references` en grille de cartes** (spec + prompt de lancement, à ouvrir) | **`docs/superpowers/specs/2026-08-15-remasterisation-nomenclature-references.md`** |
| Version liminaire (historique de la première livraison) | `docs/14-version-liminaire.md` |
| Pistes de production CMS | `docs/20-pistes-production-cms.md` (⚠ numéro 20 partagé avec la source plaquette) |
| Script de la démonstration client du 2 juillet | `docs/21-script-demo-2-juillet.md` |

## Commandes disponibles

- `/nouvelle-fiche-projet`, `/nouvelle-page`, `/nouveau-composant`, `/audit-page`, `/pre-commit-check`, `/deploy-preview`

## Voix du projet

> **« Sobre, technique, chaleureuse. »** Trois adjectifs que FT2E partage avec EuporIA Factory. Aucun superlatif, aucun jargon marketing, aucune promesse chiffrée non vérifiable. Précision métier (RT2012, RE2020, BIM, SSI, CFO/CFA) et chaleur d'équipe pluridisciplinaire.
