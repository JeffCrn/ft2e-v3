---
name: ft2e-design-system
description: Source de vérité du design system Apple-style FT2E — tokens de couleur, typographie, espacement, rayons, ombres, navigation glass. À consulter à chaque création de composant ou de page pour garantir la cohérence visuelle. Déclenche-toi sur toute mention de couleur, typo, espacement, hero, CTA, bouton, lien.
---

# Skill : FT2E Design System (Apple-style)

## Philosophie

Esthétique Apple : minimalisme cinématique, fondation chromatique dérivée du logo « flux dans le cadre » (marine + blanc froid) avec accent bleu unique pour l'action, sections alternées pour un rythme visuel fort, Inter Variable comme police unique.

## Tokens — uniques sources de vérité

Source : `src/styles/global.css` (bloc `@theme`).

### Palette

| Token Tailwind | Hex | Usage |
| --- | --- | --- |
| `marine-deep` | `#0f2436` | hero, CTA final, nav solidifiée — fond le plus immersif |
| `marine` | `#16324f` | sections sombres, **titres** (`h1`–`h6`) sur fond clair, nav |
| `marine-surface` | `#1d3a57` | cartes sur fond sombre |
| `marine-surface-2` | `#223f5e` | variation de surface sombre |
| `cool-white` | `#edf1f5` | fonds de section, cartes, footer |
| `near-black` | `#1d1d1f` | **body** (texte courant) sur fond clair — inchangé |
| `slate` | `#45535f` | texte secondaire, légendes, baseline sur fond clair |
| `mist` | `#9fb0bf` | texte secondaire, baseline sur fond marine |
| `apple-blue` | `#0071e3` | accent d'action, CTA principal, focus ring |
| `link-blue` | `#0066cc` | liens texte sur fond clair |
| `bright-blue` | `#2997ff` | liens sur fond sombre — réservé à `marine-deep` |
| `copper` | `#c46a38` | accent d'identité (logo, eyebrow, filet) — fond clair |
| `bright-copper` | `#d98a55` | accent d'identité (logo, eyebrow) — fond sombre |
| `pure-black` | `#000000` | **legacy** — n'est plus utilisé pour les surfaces |
| `text-secondary` | `rgba(0,0,0,0.8)` | texte secondaire |
| `text-tertiary` | `rgba(0,0,0,0.48)` | légendes, captions |

**Trois registres, un accent d'action isolé.** Le marine (`marine-deep` / `marine` / `marine-surface`) porte la **structure** (surfaces sombres, titres). Apple Blue reste l'accent d'**action** (CTA, liens, focus). Cuivre (`copper` / `bright-copper`) = accent d'**identité** de marque (logo, chiffre « 2 », eyebrow, filet), jamais pour signaler une action. Règle titres/body : titres → `text-marine` ; body/texte courant → `text-near-black`.

### Repointage (churn minimal)

`light-gray` → `#edf1f5` ; `dark-surface-1` → `#1d3a57` ; `dark-surface-2` → `#223f5e`. Les classes historiques (`bg-light-gray`, `bg-dark-surface-1`, `bg-dark-surface-2`) restent valides et rendent les nouvelles valeurs automatiquement.

### Aliases legacy (rétrocompatibilité)

| Ancien token | Pointe vers |
| --- | --- |
| `bleu-nuit` | `#0f2436` (marine-deep) |
| `sarcelle` | `#0071e3` (apple-blue) |
| `cuivre` | `#0071e3` (apple-blue) — alias legacy ; cuivre de marque = `copper` / `bright-copper` |
| `creme-pierre` | `#edf1f5` (cool-white) |
| `anthracite` | `#1d1d1f` (near-black) |

### Combinaisons validées (contraste RGAA AA)

- `marine` sur blanc → 13.1:1 ✅ (titres)
- `marine` sur `cool-white` → 11.5:1 ✅ (titres)
- Blanc sur `marine-deep` → 15.8:1 ✅ (body sombre)
- Blanc sur `marine-surface` → 11.7:1 ✅ (cartes)
- `near-black` sur blanc → 16.5:1 ✅ (body)
- `slate` sur blanc → 7.9:1 ✅
- `mist` sur `marine` → 5.9:1 ✅
- `link-blue` sur blanc → 5.3:1 ✅
- `apple-blue` sur blanc → 4.6:1 ✅
- `bright-blue` sur `marine-deep` → 5.25:1 ✅ (liens sombres)
- `bright-blue` sur `marine` moyen → 4.34:1 ⚠️ texte large / UI uniquement, pas de lien texte
- `bright-copper` sur `marine-deep` → 5.8:1 ✅ (eyebrow, « 2 »)
- `copper` sur blanc → 3.8:1 ⚠️ gros glyphe de logo uniquement
- `text-tertiary` sur blanc → ~3.7:1 ⚠️ texte large uniquement

### Typographie

```css
/* src/styles/global.css → @theme */
--font-heading: "Inter Variable", "Helvetica Neue", "Helvetica", "Arial", system-ui, sans-serif;
--font-body: "Inter Variable", "Helvetica Neue", "Helvetica", "Arial", system-ui, sans-serif;
```

Échelle Apple-style :

| Rôle | Taille | Poids | Line-height | Letter-spacing |
| --- | --- | --- | --- | --- |
| Display Hero | clamp(2.5rem, 5vw, 3.5rem) | 600 | 1.07 | -0.015em |
| Section Heading | clamp(1.75rem, 3vw, 2.5rem) | 600 | 1.10 | -0.01em |
| Body | 1rem | 400 | 1.5 | tracking-tight |
| Small | 0.875rem | 400 | 1.43 | tracking-tight |
| Caption | 0.75rem | 400 | 1.33 | tracking-widest uppercase |

### Espacements autorisés

Tailwind par défaut, **multiples permis** : `1, 2, 3, 4, 6, 8, 12, 16, 24, 32`.
Sections : `py-20` standard, `py-24` pour CTA final. Gaps cartes : `gap-4`.

### Rayons

- `rounded-lg` (8 px) — cartes, conteneurs, inputs
- `rounded-[980px]` — CTA pill, capsules, badges, filtres (signature Apple)
- `rounded-full` (50%) — contrôles media circulaires

Pas de `rounded-sm` ni `rounded` (4 px).

### Ombres

`shadow-soft` unique : `3px 5px 30px rgba(0, 0, 0, 0.22)`. **Rare** — hover cartes uniquement.

### Conteneur

`max-w-[980px] mx-auto px-4 md:px-6` — pas `max-w-screen-xl`.

## Patterns récurrents

### CTA principal (pill Apple Blue)

```astro
<a href="…" class="inline-flex items-center gap-2 bg-apple-blue text-white px-4 py-2 rounded-[980px] text-sm hover:bg-[#0077ED] transition-colors">
  Parlons de votre projet
</a>
```

### Lien « En savoir plus »

```astro
<a href="…" class="text-link-blue text-sm hover:underline tracking-tight">
  En savoir plus ›
</a>
```

### Titre de section (sur fond clair)

```astro
<h2 class="text-marine font-semibold">Nos expertises</h2>
```

Le body et le texte courant restent en `text-near-black` ; seuls les titres passent en `text-marine`.

### Capsule (badge secteur/mission)

```astro
<span class="inline-flex items-center px-3 py-1 rounded-[980px] text-xs bg-apple-blue/10 text-apple-blue tracking-tight">
  Logement
</span>
```

### Carte (fond clair, sans bordure)

```astro
<div class="bg-light-gray rounded-lg p-6 transition-all hover:shadow-soft">
  …
</div>
```

### Navigation glass

```astro
<header class="fixed top-0 inset-x-0 z-50 h-12 bg-marine-deep/80 backdrop-blur-[20px] backdrop-saturate-[180%]">
  …
</header>
<div class="h-12" aria-hidden="true"></div>
```

Panneau mobile : `bg-marine-deep/95`.

### Rythme cinématique des sections

```
Hero         → bg-marine-deep (texte blanc froid / eyebrow cuivre clair)
Chiffres     → bg-cool-white
Services     → bg-white
Secteurs     → bg-marine (texte blanc froid / eyebrow cuivre clair)
Références   → bg-white
Équipe       → bg-cool-white
Partenaires  → bg-white
CTA final    → bg-marine-deep (texte blanc froid)
```
