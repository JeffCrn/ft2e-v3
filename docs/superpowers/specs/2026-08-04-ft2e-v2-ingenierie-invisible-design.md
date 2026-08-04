# FT2E v2 — Design system « Ingénierie de l'invisible »

Date : 2026-08-04
Statut : validé par principe (demande utilisateur explicite : « seul change le style et le design du site »)
Référence : bundle Claude Design `C:\claude_code_dev_projects\ing-nierie-de-l-invisible\project\FT2E Démo V2.dc.html`

## Objet

Nouveau repo `ft2e-v2`, fork de `ft2e-site`, qui conserve **à l'identique** :

- tous les contenus (`src/content/**` — 8 projets, 6 expertises, 7 profils, 6 secteurs, actualités) ;
- les Content Collections + schémas Zod (`src/content.config.ts`) ;
- le CMS Decap (`public/admin/config.yml` + `index.html` + `api/` OAuth) ;
- le SEO (JSON-LD, canonicals, noindex démo, sitemap, robots) ;
- l'architecture Astro 6 statique + Tailwind 4 + View Transitions ;
- les patterns obligatoires (`astro:page-load` + guard `dataset`, `fs.existsSync` images).

Et remplace **uniquement** la couche design (esthétique Apple-style → blueprint technique).

## Direction esthétique — « le plan d'exécution »

Le site ressemble à un document d'ingénierie : cartouches, filets 1 px, annotations
mono, chiffres tabulaires. La technique invisible dans le bâtiment devient visible
dans le design.

### Palette

| Token | Hex | Usage |
|---|---|---|
| `encre` (`marine-deep`) | `#08131F` | fond nav, hero, footer, CTA final |
| `marine` | `#16324F` | titres sur clair, surfaces duotone |
| `cool-white` | `#EDF0F2` | fond clair principal, texte sur encre |
| `paper` | `#F7F9FA` | surface claire secondaire (hover, encarts) |
| `slate` | `#4A6076` | corps de texte sur clair, filets (à 35 %) |
| `mist` | `#8FA2B4` | labels mono, texte secondaire sur encre |
| `copper` | `#C46A38` | accent : numéros, filets forts, hover bordures, focus |
| `bright-copper` | `#E08A50` | hover liens sur encre, annotations sur duotone |

Pas de bleu d'action : le cuivre porte à la fois l'identité **et** l'interaction
(hover, focus ring `2px solid #C46A38`). Les anciens tokens (`apple-blue`,
`link-blue`, `bright-blue`, `near-black`…) sont conservés comme **aliases repointés**
vers la nouvelle palette pour limiter le churn.

### Typographie

- **Archivo Variable** (axes `wdth` 62–125, `wght` 300–700) — titres condensés
  larges **uppercase** (`wdth` 112–125, 600–700, `letter-spacing: -0.02em`,
  `line-height` 0.98–1.15) et corps en 300 (15–17 px, `line-height` 1.6).
- **IBM Plex Mono** (400/500) — labels (`11px`, `letter-spacing: .14em`, uppercase),
  données (`13px`, `font-variant-numeric: tabular-nums`), navigation, boutons.
- Chargement via `@fontsource-variable/archivo` (axe wdth) et
  `@fontsource/ibm-plex-mono`. `font-display: swap`. Pas de CDN Google (RGPD).

Classes recettes globales (dans `global.css`, `@layer components`) :
`type-display`, `type-h2`, `type-h3`, `mono-label`, `mono-data`, `btn-blueprint`,
`btn-blueprint-solid`, `chip-blueprint`, `duotone-media`, `corner-frame`.

### Vocabulaire graphique

- **Bordures 1 px partout** : `rgba(74,96,118,.35)` (filet standard), `#4A6076`
  (filet fort), `#C46A38` (filet accent — top des `h2` éditoriaux, top des
  sections encre).
- **Cartouches** : tableaux en grille bordée (chiffres clés, fiche technique
  projet) — l'anti-carte : pas d'ombre, pas de rayon, pas de fond dégradé.
- **Coins cuivre** (`corner-frame`) : équerres 16 px aux angles des médias.
- **Duotone hachuré** : placeholders et traitement image
  `repeating-linear-gradient(135deg, #08131F 0 1px, #2c4560 1px 8px)` + voile
  `linear-gradient(150deg, rgba(22,50,79,.6), rgba(237,240,242,.18))`.
- **Rayons : zéro** (2 px max sur les inputs). **Ombres : zéro.**
- Boutons rectangulaires mono uppercase : plein (`cool-white` sur encre, hover
  fond cuivre) ou filaire (bordure `mist/40`, hover bordure + texte cuivre).
- Hover systémique : `border-color → copper`, transition
  `400ms cubic-bezier(0.16, 1, 0.3, 1)`.

### Navigation

Barre encre opaque 74 px (60 px mobile), logo « flux dans le cadre » (SVG du
bundle), liens mono uppercase 11 px `mist` → hover `bright-copper`. Plus de
glass/blur ni de nav transparente — la nav reste fixe et opaque sur toutes les
pages (le script `navGlass` est neutralisé, l'attribut `data-hero-dark` reste
pour la sémantique).

### Accessibilité (RGAA AA maintenu)

Contrastes clés : `cool-white`/`encre` ≈ 14,9:1 ; `mist`/`encre` ≈ 7,4:1 ;
`marine`/`cool-white` ≈ 9,9:1 ; `slate`/`cool-white` ≈ 5,9:1 ;
`bright-copper`/`encre` ≈ 6,7:1 ; `copper` sur clair = 3,8:1 → réservé aux
**gros glyphes, numéros décoratifs et filets**, jamais au texte porteur seul
(les labels cuivre sur clair sont doublés d'un contexte ou passés en `copper`
uniquement à taille large / éléments UI ≥ 3:1). Focus visible cuivre partout.
`prefers-reduced-motion` conservé.

### Motion

Le système vanilla existant est conservé (hero reveal, scroll reveal, compteurs,
View Transitions). Adaptations : easing global `--ease-blueprint:
cubic-bezier(0.16, 1, 0.3, 1)`, suppression du tilt 3D et du glass dynamique
(étrangers au langage blueprint), reveals plus discrets (translation 12 px).

## Ce qui ne change pas (contrat)

Routes et URLs, frontmatters, schémas Zod, config Decap, JSON-LD, règles
éditoriales françaises, badge `[DÉMO]`, triple verrou noindex.

## Hors périmètre

Nouvelles pages, nouveaux contenus, migration ft2e.fr, reportage photo.
