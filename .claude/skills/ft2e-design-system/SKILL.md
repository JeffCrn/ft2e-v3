---
name: ft2e-design-system
description: Source de vérité du design system FT2E v3 — charte « Ingénierie de l'invisible » révision 2 « plans et profondeur » (monochrome 197°, aucun accent, relief par trois rangs d'ombre à l'encre translucide), typographie Archivo (graisses 300/600/700, wdth 62–125) + IBM Plex Mono, trame 28 px, filets 1 px par opacité, titre d'écran en casse normale, bouton plein encre, relevés à un seul chiffre plein, courbe unique cubic-bezier(0.2, 0.7, 0.2, 1), rapports 21:8/16:10/3:2. À consulter à chaque création de composant ou de page pour garantir la cohérence visuelle. Déclenche-toi sur toute mention de couleur, typo, espacement, hero, CTA, bouton, lien, cartouche, duotone, nomenclature, monogramme, plan, ombre, trame, cellule, relevé.
---

# Skill : FT2E Design System — charte v3 « plans et profondeur » (monochrome 197°)

## Sources de vérité

1. `.claude/rules/tailwind-design-tokens.md` — règle stricte des tokens (charte v3).
2. `docs/superpowers/specs/2026-08-06-ft2e-charte-v3-plans-profondeur.md` — spec d'application, avec la table de traduction v2 → v3.
3. `src/styles/global.css` (`@theme` + `@layer components`) — les recettes réelles.

Référence charte : « FT2E Charte graphique » document 10 · révision 2 (août 2026, bundle `branding-v3/`) — remplace la charte v2 monochrome (`branding-v2/`).

## Philosophie

Un bureau d'études ne signale pas : il cote, il hiérarchise, il archive. Les trois premières décisions ne changent pas — **une teinte unique (197°), aucune couleur d'accent, l'état par défaut est clair** (une réserve profonde par écran, 1/5 de la surface max). La quatrième est nouvelle : **la profondeur remplace l'ornement**. Le relief vient des plans — une planche posée, une planche qui déborde, une ligne encrée — portés par trois rangs d'ombre à l'encre translucide. La hiérarchie passe par la valeur, la **graisse** (300/600/700) et le **plan**, plus jamais par l'épaisseur de filet.

## Tokens — source de vérité : `src/styles/global.css` (@theme)

| Token | Hex | Usage |
|---|---|---|
| `profond` | `#001718` | réserve — 1/5 max, UNE apparition/écran (`.plan-encre`, duotone, couverture) ; vedette et puce de section sur papier |
| `encre` | `#00393a` | toute la lecture : titres, paragraphes, aplat du bouton principal, chiffre plein d'un relevé |
| `pivot` | `#336667` | données, dates, commentaires, corps secondaire (6,14:1 papier), focus ring — ⛔ jamais en texte sur profond (3,67:1) |
| `clair` | `#99cccd` | texte sur profond uniquement (10,55:1) ; sur clair : filet, aplat et complément « / » des titres de section seulement (1,62:1, jamais porteur de sens) |
| `voile` | `#e1f4f4` | pôle clair du duotone ; chiffres/titres sur `.plan-encre` (16,04:1) ; équerres d'image |
| `papier` | `#f7f9fa` | fond des plans et de la planche de page |
| `calcaire` | `#edf0f2` | fond du body (visible au-delà de 1440 px), cellules de liste, en-têtes de cartouche — jamais au contact du voile (iso-clairs) |
| `filet-1/2/3` | encre 22 % / 16 % / 12 % | **filets tous à 1 px** — le rang est porté par l'opacité (porteur / bordure de plan / indication) |
| `filet-chip` | encre 28 % | étiquette de mission, chip de filtre, bouton filaire |
| `shadow-plan-1/2/3` | encre 12 % / 16 % / 30 % | ombres des trois plans ; `--shadow-page` (0 0 90px, 18 %) pour la planche de page |

**Le cuivre n'existe plus** ; `line`/`line-strong` sont des aliases v2 repointés, interdits dans le nouveau code. L'ombre est toujours de l'encre translucide, jamais du noir : aucun flou > 70 px (90 px réservé à la planche de page), aucun décalage horizontal, aucune ombre intérieure ni sur un texte. Alerte = filet doublé + mention, pas une couleur.

## Nouveautés v3 (ruptures depuis la v2)

- **Plans et ombres, 3 rangs** : `.plan-pose` (papier, bordure 1 px `filet-2` obligatoire, ombre rang 1), `.plan-deborde` (ombre rang 2, chevauche de 40 px, se retire de 92 px — **1×/écran max**), `.plan-encre` (profond, filet clair 3 px à gauche, ombre rang 3 — la réserve de l'écran). Révélation via `data-plan` (BaseLayout) sur les blocs significatifs seulement.
- **Planche de page** : le site est une feuille papier `max-w-[1440px]` posée sur le calcaire du body, portée par `--shadow-page`, fond `.trame-fond` (pas de 28 px, 7 % d'encre, jamais visible sous un plan opaque).
- **Filets par opacité** : tous à 1 px ; rang = 22 % / 16 % / 12 % (+ 28 % pour chips). Plus de 4/2/1 px.
- **Titre d'écran** : h1 des pages internes en `.type-ecran` — wdth 100, 600, **casse normale, jamais capitales**, interligne 1,02. La vedette capitales (`.type-display`, 125/700) est réservée à l'accueil.
- **Titre de section** : `.type-section` 118/**700** capitales, précédé de la **puce profonde 7 px** (`.puce-section`, seule exception au rayon 0) + numéro mono ; mot porteur encre + complément `text-clair` précédé d'une barre oblique (dérogation : le mot en encre suffit au sens).
- **Corps Archivo 300** : trois graisses seulement (300/600/700) ; mono 400/500/600.
- **Bouton principal plein** : `.btn-principal` (alias `.btn-blueprint-dark`) — aplat encre, texte papier mono 11/500, **filet clair 3 px à gauche**, hover → profond 260 ms, flèche `→` admise ; le filet ne bouge pas. Secondaire : `.btn-filaire` (1 px à 28 %). Sur profond : `.btn-blueprint-solid` (filaire clair).
- **Relevé clair** : le commentaire (Archivo 300, 14 px, pivot) **précède** le chiffre ; **un seul chiffre plein encre par relevé** (celui que la page défend), les autres en `.releve-retrait` (encre 13 %) ; chiffres `.releve-chiffre` (118/700, ls −0,04 em, tabulaire). Relevé encré : `.plan-encre`, chiffres `text-voile`, étiquettes `mono-label text-clair`.
- **Courbe unique** : `cubic-bezier(0.2, 0.7, 0.2, 1)` (`--ease-blueprint`) — remplace `cubic-bezier(0.16, 1, 0.3, 1)`.
- **Module 28 px** (pas de trame) ; marge de page 60 px (44 px < 1200, 24 px à 390) ; 76 px entre sections ; gouttière 24 px ; conteneur planche 1440 px.
- **Rapports d'image** : **21:8** (bandeau), **16:10** (appui de titre), **3:2** (fiche, index) — le 16:9 n'existe plus.
- **Survol = bascule de fond** (calcaire → papier 300 ms, encre → profond 260 ms) — plus de `box-shadow inset`, plus de filet épaissi, aucun déplacement.

## Échelle de titrage (§ 06)

| Rang | Classe | Chasse | Graisse | Casse |
|---|---|---|---|---|
| Vedette | `.type-display` | 125 | 700 | capitales — accueil uniquement, une par page |
| Titre d'écran | `.type-ecran` | 100 | 600 | **normale** — h1 des pages internes (`HeroPage`) |
| Section | `.type-section` (= `.type-h2`) | 118 | 700 | capitales + puce + « /complément » clair |
| Intitulé | `.type-intitule` | 112 | 600 | capitales — cartes, cellules, nomenclature |
| Corps | (défaut body) | 100 | **300** | 15–17 px, lh 1,6, 52–68 signes |
| Étiquette | `.mono-label` | mono | 500 | 11/10 px, 0,14 em, capitales |
| Relevé | `.releve-chiffre` | 118 | 700 | tabulaire, ls −0,04 em |

Le mono jamais en texte courant ; l'Archivo jamais en cote ni référence d'affaire.

## Grammaire des composants (§ 10)

- **Cartouche** (`FicheTechnique`) : plan posé (bordure 1 px, ombre rang 1), en-tête calcaire, filets internes 1 px par rangs d'opacité, données mono. **La barre de rang 4 px n'existe plus.**
- **Cellule de liste** : `.cellule-liste` — calcaire, bordure `filet-1`, min-h 112 px, numéro mono en tête, intitulé (112/600) en pied aligné à droite, hover → papier 300 ms.
- **Étiquette de mission** : `.etiquette-mission` — mono 10 px, filet 1 px 28 %, jamais d'aplat, six max par bloc. **Chip de filtre** : `.chip-blueprint`, actif = aplat encre/texte papier (`aria-pressed`).
- **Nomenclature** (`/references`) : liste tabulaire ; rang par **opacité du filet gauche 1 px** (livré 22 %, en cours 16 %, archive 12 %) doublée de la **graisse de l'intitulé** (700/600/300).
- **Média** : duotone 197° (`duotone-photo` : sandwich lighten/darken profond → voile ; `duotone-media` : hachure placeholder) + équerres voile 1 px, **18 px de côté**, dans les angles (repère de tirage, pas un encadrement) + annotations mono (2 max/image). Aucun cadre autour d'une image.
- **Navigation** : barre **claire** fixe ; liens mono uppercase pivot → hover encre ; page courante = encre + filet bas 1 px encre plein.
- **Monogramme** (`Logo.astro`) : dessin inchangé ; hauteur minimale 28 px ; sous 180 px de place : `forme="cadre"`. Ne se déforme pas, ne reçoit ni ombre ni contour ; le débord du flux ne se recadre jamais.

## Interdits (§ 15)

- Teinte hors axe 197° (cuivre inclus) ; dégradé coloré ; ombre hors encre ; lueur.
- Vert FT2E (`pivot`) en **texte** sur profond ; `clair` porteur de sens sur fond clair ; voile/calcaire en contact.
- Deux réserves profondes par écran ; deux vedettes par page.
- Angle arrondi hors puce de section ; cadre fermé autour d'une image.
- Rang par épaisseur de filet (4/2 px) ; `box-shadow inset` au survol ; déplacement au survol ; compteur animé ; parallax.
- Photo en couleurs d'origine ; cadrage hors 21:8, 16:10, 3:2.

## Motion (§ 13)

**Quatre mouvements, une seule courbe** (`--ease-blueprint`) : tracé de flux 900 ms (1×/chargement, `TraceFlux.astro`) · révélation de plan 760 ms / 22 px (1×/élément `data-plan`, à l'entrée dans la vue, via `BaseLayout`) · survol de cellule 300 ms · survol de bouton 260 ms. Rien d'autre ne bouge. Focus : 2 px pivot décalé 2 px. `prefers-reduced-motion` supprime tout ; sans JS, rien n'est masqué (`html.js-plans`).
