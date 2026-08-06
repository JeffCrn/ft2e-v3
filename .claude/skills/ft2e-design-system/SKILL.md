---
name: ft2e-design-system
description: Source de vérité du design system FT2E v2 — charte « Ingénierie de l'invisible » v2 monochrome 197° (papier/encre/pivot, aucun accent), typographie Archivo (wdth 125/118/112/100/72) + IBM Plex Mono, cartouches à barre de rang, filets 4/2/1 px, duotone, nomenclature, monogramme. À consulter à chaque création de composant ou de page pour garantir la cohérence visuelle. Déclenche-toi sur toute mention de couleur, typo, espacement, hero, CTA, bouton, lien, cartouche, duotone, nomenclature, monogramme.
---

# Skill : FT2E Design System — charte v2 « Ingénierie de l'invisible » (monochrome 197°)

## Philosophie

Un bureau d'études ne signale pas : il cote, il hiérarchise, il archive. **Une teinte unique (197°), cinq valeurs teintées, deux neutres, aucune couleur d'accent.** La hiérarchie passe par les trois moyens du dessin technique : la valeur, l'épaisseur de trait (4/2/1 px) et la largeur de caractère (Archivo wdth). Référence : « FT2E Charte » v1.0 (août 2026, bundle `branding-v2/`) et `docs/superpowers/specs/2026-08-06-ft2e-charte-v2-monochrome-197.md` — remplace le système cuivre/marine antérieur.

## Tokens — source de vérité : `src/styles/global.css` (@theme)

| Token | Hex | Usage |
|---|---|---|
| `profond` | `#001718` | réserve — 1/5 max, UNE apparition/écran (relevés, duotone, couverture) ; texte vedette sur papier |
| `encre` | `#00393a` | toute la lecture : titres, filets porteurs, cadres, barres de rang |
| `pivot` | `#336667` | données, dates, corps de texte sur clair (6,1:1), filets 2ᵉ rang, focus |
| `clair` | `#99cccd` | étiquettes/texte sur fond profond ou encre UNIQUEMENT |
| `voile` | `#e1f4f4` | pôle clair du duotone ; texte/équerres sur réserve profonde UNIQUEMENT |
| `papier` | `#f7f9fa` | **fond par défaut de toute page** |
| `calcaire` | `#edf0f2` | surface secondaire, hover de surface — jamais sous le voile (iso-clairs) |
| `line` / `line-strong` | `rgba(0,57,58,.18)` / `.3` | filet d'indication / contour de cartouche |

**Le cuivre n'existe plus** (aliases repointés). Règles : 2 valeurs par composition (3 max) ; jamais deux valeurs voisines en contact (sauter un palier) ; aucun dégradé ni opacité de teinte ; alerte = filet doublé + mention, pas une couleur.

## Typographie — rangs

`type-display` = Vedette (125/700, une par page, `text-profond`) · `type-h2` = Titre (118/600) · `type-intitule` = Intitulé (112/600, cartes et nomenclature) · corps Courant (100/400, 15–17 px, lh 1,6 — plus de `font-light`) · `type-annexe` (72/600) · `mono-label` (11 px/500/0,14 em) · `mono-data` (13 px tabulaire). Tout nombre mesuré en mono ; vedettes chiffrées de stats en Archivo 118/600 tabulaire.

## Grammaire des blocs

- **Section claire** : `bg-papier`, titre `type-h2 text-encre text-[22px]` en baseline avec `mono-label text-pivot`.
- **Bande secondaire** : `bg-calcaire border-t-2 border-encre` (partenaires, méthode) ; CTA final : `bg-calcaire border-t-4 border-encre`.
- **Hero** : clair, vedette `type-display text-profond` + **barre de rang 4 px encre** (110 px) + sous-titre pivot. Accueil : 2 colonnes, média duotone annoté + cartouche compact à droite — l'image ne porte pas le titre.
- **Cartouche** : `grid-cols-[4px_1fr]` barre encre + `border border-line-strong`, cases mono ; ordre constant intitulé → référence → date. Jamais centré, jamais d'ombre.
- **Nomenclature** (`/references`) : liste tabulaire, en-tête `border-b-2 border-encre`, rang du filet gauche 4/2/1 px = livré/en cours/archive (champ `statut`), largeur Archivo 118/100/72 assortie. Pas de pagination.
- **Relevés** : `bg-profond` + label `mono-label text-clair` + chiffres Archivo 118/600 `text-voile` — la seule réserve profonde de l'écran.
- **Média** : duotone 197° (`duotone-photo` : sandwich lighten/darken #001718→#E1F4F4 ; `duotone-media` : hachure placeholder) + `CoinsCuivre` (équerres voile 1 px, 18/16/14 px, DANS les angles) + annotation mono voile (2 max, verticale d'appui à 1/8).
- **Monogramme** (`Logo.astro`) : `version` principal/inverse/valeur-unique, `forme` complet/cadre (sous 180 px le mot tombe). Le débord du flux ne se recadre jamais.
- **Prose** : `max-w-[840px]`, h2 `filet-top` (2 px encre), corps pivot, listes `border-l border-line-strong`, liens soulignés encre hover pivot.

## Interdits

- Aplat sombre décoratif (`bg-encre`/`bg-profond` hors relevés) — le papier gouverne.
- Rayons (2 px max inputs), ombres, dégradés, boutons pleins sans nécessité.
- Couleur hors rampe 197° + 2 neutres ; `voile`/`clair` sur fond clair ; encre sur pivot (1,97:1).
- Compteurs animés, apparitions au défilement, parallax, hover lift (aucun déplacement).
- Icônes illustratifs, pictogrammes décoratifs, emojis.
- Images en couleurs natives ou gris neutre ; cadre d'image fermé ; 3ᵉ rapport d'image (3:2 et 16:9 seulement).

## Motion

**Un seul tracé animé sur tout le site** : `TraceFlux.astro`, 900 ms, une fois par chargement. États : survol = filet épaissi d'un cran (`box-shadow inset`) + intitulé à l'encre, 200 ms ; focus = 2 px pivot décalé 2 px. Easing unique `--ease-blueprint`. `prefers-reduced-motion` partout.
