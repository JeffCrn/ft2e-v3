---
name: ft2e-design-system
description: Source de vérité du design system « Ingénierie de l'invisible » FT2E v2 — tokens de couleur (encre/marine/cuivre), typographie Archivo + IBM Plex Mono, cartouches, filets, duotone, boutons blueprint. À consulter à chaque création de composant ou de page pour garantir la cohérence visuelle. Déclenche-toi sur toute mention de couleur, typo, espacement, hero, CTA, bouton, lien, cartouche, duotone.
---

# Skill : FT2E Design System — « Ingénierie de l'invisible »

## Philosophie

Le site ressemble à un **document d'ingénierie** : cartouches bordées, filets 1 px, annotations mono uppercase, chiffres tabulaires, coins cuivre sur les médias, images duotone. La technique invisible dans le bâtiment devient visible dans le design. Référence : bundle Claude Design `FT2E Démo V2.dc.html` (2026-08-04) et spec `docs/superpowers/specs/2026-08-04-ft2e-v2-ingenierie-invisible-design.md`.

## Tokens — source de vérité : `src/styles/global.css` (@theme)

### Couleurs

| Token | Hex | Usage |
|---|---|---|
| `encre` / `marine-deep` | `#08131f` | nav, hero, footer, CTA final |
| `marine` | `#16324f` | titres sur clair, texte fort, données de cartouche |
| `cool-white` | `#edf0f2` | fond clair principal, texte sur encre |
| `paper` | `#f7f9fa` | surface claire secondaire, hover, encarts |
| `slate` | `#4a6076` | corps de texte et labels sur fond clair |
| `mist` | `#8fa2b4` | labels et texte secondaire sur encre UNIQUEMENT (2,3:1 sur clair) |
| `copper` | `#c46a38` | filets, bordures, équerres ; texte sur encre (4,9:1) |
| `bright-copper` | `#e08a50` | hover liens / annotations sur encre (7,1:1) |
| `copper-text` | `#a04e20` | petit texte cuivre sur fond clair (≥ 5:1) |
| `line` / `line-strong` | `rgba(74,96,118,.35)` / `#4a6076` | filet standard / contour de cartouche |

**Pas de bleu.** Le cuivre porte identité + interaction (hover, focus `2px solid copper`). Aliases legacy (`apple-blue`, `link-blue`, `bright-blue`, `near-black`, `light-gray`, `dark-surface-*`) repointés — ne plus les utiliser.

### Typographie

- **Archivo Variable** — titres condensés-larges uppercase via `font-stretch` (112 % sections, 118 % wordmark, 125 % display), corps `font-light` (300) 15–17 px, `line-height` 1.55–1.6.
- **IBM Plex Mono** 400/500 — labels 11 px `tracking .14em` uppercase, données 13 px `tabular-nums`, nav, boutons, breadcrumbs.

### Classes recettes (global.css, @layer components)

`type-display` (hero), `type-h2` (sections/cartes), `mono-label`, `mono-data`, `filet-top` (filet cuivre au-dessus des h2 éditoriaux), `btn-blueprint` (filaire), `btn-blueprint-solid` (plein clair sur encre), `btn-blueprint-dark` (plein encre sur clair), `chip-blueprint` (filtres), `duotone-media` (placeholder hachuré), `duotone-photo` (photo duotone). Composant `CoinsCuivre.astro` pour les équerres.

## Grammaire des blocs

- **Section claire** : `bg-cool-white`, titre `type-h2 text-marine text-[22px]` en baseline avec un `mono-label text-slate`.
- **Section encre** : `bg-encre border-t border-copper text-cool-white` (CTA final, bandeaux).
- **Cartouche** : `border border-line-strong` + grille `gap-px bg-line`, cellules `bg-cool-white p-5`, label mono + valeur mono marine.
- **Carte** : `border border-line bg-paper hover:border-copper`, média duotone 3:2 avec référence `FT2E—{année}` en bas à gauche, titre `type-h2 text-base`, méta `mono-data`.
- **Liste secteurs** : lignes `border-b border-line` avec n° cuivre tabulaire, hover `border-b-copper bg-paper`.
- **Média** : parent `relative` + `duotone-media`/`duotone-photo` + `CoinsCuivre` + annotation `mono-label text-cool-white` en bas à gauche.
- **Prose éditoriale** : `max-w-[840px]`, h2 `filet-top`, corps `text-slate font-light text-[17px]`, listes à `border-l border-copper`, liens soulignés marine hover `copper-text`.

## Interdits

- Rayons (`rounded-lg`, pill `rounded-[980px]`) — seuls les inputs ont `rounded-[2px]`.
- Ombres (`shadow-*`).
- Bleu d'action, glass/blur, tilt 3D.
- Texte `copper` standard ou `mist` sur fond clair (contraste insuffisant → `copper-text` / `slate`).
- Couleur forcée sur `h1`–`h6` en CSS global (Tailwind v4 : utilitaires d'abord).

## Motion

Easing unique `--ease-blueprint: cubic-bezier(0.16, 1, 0.3, 1)` (alias `--ease-apple` conservé). Hero reveal mot à mot, scroll reveal 12 px, compteurs, transitions de bordure 400 ms. `prefers-reduced-motion` respecté partout.
