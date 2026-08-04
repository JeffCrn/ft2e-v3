# Évolution de la palette (logo marine + cuivre) — Plan d'implémentation

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Faire évoluer la fondation chromatique du site FT2E du modèle Apple (noir/blanc/bleu) vers la palette bi-mode du logo « flux dans le cadre » : échelle marine en structure, blanc froid en lumière, gris-bleu en encre secondaire — cuivre (identité) et bleu (action) conservés et isolés.

**Architecture:** Un unique `@theme` dans `src/styles/global.css` porte tous les tokens. On **repointe** les tokens dont le rôle est préservé (`light-gray`, `dark-surface-*`, alias `bleu-nuit`) pour basculer automatiquement fonds clairs, cartes et inputs. On **migre** ensuite chirurgicalement les classes dont le rôle change (`bg-pure-black` → marine, titres `text-near-black` → `text-marine`, sous-titres `white/70` → `text-mist`). Enfin, doc et mémoire (sources de vérité) sont mises à jour.

**Tech Stack:** Astro 6 (static), Tailwind CSS 4 (`@theme` dans `global.css`, pas de `tailwind.config.ts`), TypeScript strict.

## Global Constraints

- **Source de vérité des couleurs** : `src/styles/global.css` bloc `@theme` uniquement. Aucune valeur chromatique hors tokens (sauf ombres existantes).
- **RGAA AA / Lighthouse Accessibilité 100/100** : aucune régression de contraste vs. le tableau du spec §6.
- **Règle non négociable** : le cuivre (`copper`/`bright-copper`) ne signale JAMAIS une action ; le bleu (`apple-blue`/`link-blue`/`bright-blue`) est l'unique accent d'action.
- **Règle liens sur sombre** : un lien texte petit sur fond sombre vit sur `marine-deep` (5,25:1). Sur `marine` moyen, l'interactivité passe par un CTA plein ou un lien ≥ 18 pt.
- **Body reste `near-black`** (`#1d1d1f`) ; seuls les titres passent en `marine`.
- **Conteneur, rayons, ombres, espacements, typo (Inter) : inchangés.** Pas de mode `dark:`.
- **Scripts client** : tout `addEventListener` passe par `astro:page-load` + guard `dataset` (règle projet). Aucun script modifié ici.
- **Vérification par tâche** (pas de tests unitaires de couleur dans ce projet) : `npm run build` passe + grep de contrôle + revue visuelle. Cible finale : `npm run lint` et `npm run typecheck` passent aussi.
- **Commits** : format conventionnel français (`type(portée): sujet impératif`), ≤ 72 car., et finir par `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`. Branche de travail : `feat/palette-marine-logo`.
- **Spec de référence** : `docs/superpowers/specs/2026-07-03-evolution-palette-logo-design.md`.

---

## File Structure

| Fichier | Responsabilité | Tâche |
|---|---|---|
| `src/styles/global.css` | `@theme` : nouveaux tokens + repointage | 1 |
| `src/components/blocs/Hero.astro` | Hero accueil : bg + titre + sous-titre | 2, 3, 5 |
| `src/components/blocs/HeroPage.astro` | Hero pages internes : bg + sous-titre | 2, 5 |
| `src/components/blocs/CtaFinal.astro` | CTA final : bg + sous-titre | 2, 5 |
| `src/components/blocs/SecteursPhares.astro` | Section secteurs sombre : bg + texte | 2, 5 |
| `src/pages/equipe.astro` | Bande CTA sombre + sous-titre + titres | 2, 3, 5 |
| `src/components/layout/Header.astro` | Nav glass : rgba marine | 2 |
| Composants blocs (titres) | `text-near-black` → `text-marine` sur titres | 3 |
| Pages long-form (titres prose) | `[&>h2/h3]:text-near-black` → marine | 4 |
| `src/components/layout/Logo.astro` | Prop `theme`, encre blanc froid | 6 (opt.) |
| `src/components/layout/Footer.astro` | Bloc de marque (lockup clair + tagline slate) | 6 (opt.) |
| Docs / règles / skill / mémoire | Palette = source de vérité | 7 |

---

## Task 1: Tokens `@theme` — fondation marine

**Files:**
- Modify: `src/styles/global.css:6-35` (palette + aliases dans `@theme` ; le bloc Typography/`--font-*` et `--shadow-soft` lignes 37-43 reste **intact**)

**Interfaces:**
- Produces (nouveaux tokens Tailwind, consommés par toutes les tâches suivantes) :
  `bg-marine-deep` `#0F2436`, `bg-marine` / `text-marine` `#16324F`,
  `bg-marine-surface` `#1D3A57`, `bg-marine-surface-2` `#223F5E`,
  `text-mist` `#9FB0BF`, `text-slate` `#45535F`.
- Produces (repointages, rôle inchangé) : `light-gray` → `#EDF1F5`,
  `dark-surface-1` → `#1D3A57`, `dark-surface-2` → `#223F5E`, `bleu-nuit` → `#0F2436`.

- [ ] **Step 1: Ajouter les nouveaux tokens et repointer dans `@theme`**

Dans `src/styles/global.css`, remplacer le bloc palette + aliases (lignes 6-35, du commentaire `/* Apple palette */` jusqu'à `--color-error` inclus) par le bloc ci-dessous. **Ne pas toucher** aux lignes suivantes (`/* Typography */`, `--font-*`, `--shadow-soft`) ni au bloc `:root { --c-* }` plus bas :

```css
  /* Palette FT2E — évolution logo « flux dans le cadre » */
  /* Structure — échelle marine (remplace le noir) */
  --color-marine-deep: #0f2436;      /* hero, CTA final, nav solidifiée */
  --color-marine: #16324f;           /* sections sombres, titres sur clair, nav */
  --color-marine-surface: #1d3a57;   /* cartes sur fond sombre */
  --color-marine-surface-2: #223f5e; /* variation surface sombre */

  /* Lumière & encre */
  --color-cool-white: #edf1f5;       /* fond clair alterné, cartes, footer */
  --color-near-black: #1d1d1f;       /* body sur fond clair (inchangé) */
  --color-slate: #45535f;            /* texte secondaire / baseline sur clair */
  --color-mist: #9fb0bf;             /* texte secondaire / baseline sur marine */

  /* Identité — cuivre (inchangé, déjà exact) */
  --color-copper: #c46a38;
  --color-bright-copper: #d98a55;

  /* Action — bleu, isolé (inchangé) */
  --color-apple-blue: #0071e3;
  --color-link-blue: #0066cc;
  --color-bright-blue: #2997ff;

  /* Surfaces & boutons */
  --color-light-gray: #edf1f5;       /* repointé → blanc froid */
  --color-dark-surface-1: #1d3a57;   /* repointé → marine-surface */
  --color-dark-surface-2: #223f5e;   /* repointé → marine-surface-2 */
  --color-pure-black: #000000;       /* legacy — ne plus utiliser pour surfaces */
  --color-button-active: #ededf2;
  --color-button-light: #fafafc;

  /* Semantic aliases */
  --color-text-primary: #1d1d1f;
  --color-text-secondary: rgba(0, 0, 0, 0.8);
  --color-text-tertiary: rgba(0, 0, 0, 0.48);

  /* Legacy mappings for gradual migration */
  --color-bleu-nuit: #0f2436;        /* repointé → marine-deep */
  --color-sarcelle: #0071e3;
  --color-cuivre: #0071e3;
  --color-creme-pierre: #edf1f5;     /* repointé → blanc froid */
  --color-anthracite: #1d1d1f;
  --color-gris-bord: rgba(0, 0, 0, 0.08);
  --color-gris-doux: rgba(0, 0, 0, 0.48);
  --color-success: #30d158;
  --color-error: #ff3b30;
```

- [ ] **Step 2: Vérifier que le build passe**

Run: `npm run build`
Expected: build OK, aucune erreur. (Les fonds clairs et cartes passent déjà en blanc froid / marine automatiquement via repointage.)

- [ ] **Step 3: Vérifier que les nouveaux tokens sont bien émis**

Run: `npm run build && grep -rl "marine" dist/_astro/*.css`
Expected: au moins un fichier CSS listé (les classes `marine` référencées le seront après les tâches suivantes ; à ce stade, vérifier surtout l'absence d'erreur de parse `@theme`).

- [ ] **Step 4: Commit**

```bash
git add src/styles/global.css
git commit -m "feat(design-system): ajoute l'échelle marine et repointe les fonds clairs

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 2: Surfaces immersives → marine + nav glass

**Files:**
- Modify: `src/components/blocs/Hero.astro:31`
- Modify: `src/components/blocs/HeroPage.astro:36`
- Modify: `src/components/blocs/CtaFinal.astro:15`
- Modify: `src/components/blocs/SecteursPhares.astro:15`
- Modify: `src/pages/equipe.astro:106`
- Modify: `src/components/layout/Header.astro:8,48`

**Interfaces:**
- Consumes : `bg-marine-deep`, `bg-marine` (Task 1).
- Produces : toutes les surfaces immersives sont en marine ; la nav glass est teintée marine.

- [ ] **Step 1: Hero accueil → marine-deep**

`src/components/blocs/Hero.astro` ligne 31, remplacer :
```astro
    isAccueil ? 'bg-pure-black text-white py-24 md:py-32 lg:py-40' : 'bg-light-gray py-16 md:py-20',
```
par :
```astro
    isAccueil ? 'bg-marine-deep text-white py-24 md:py-32 lg:py-40' : 'bg-light-gray py-16 md:py-20',
```

- [ ] **Step 2: HeroPage → marine-deep**

`src/components/blocs/HeroPage.astro` ligne 36, remplacer `'bg-pure-black'` par `'bg-marine-deep'` :
```astro
<section class:list={['bg-marine-deep', paddingClasses[size]]} data-hero-dark>
```

- [ ] **Step 3: CTA final → marine-deep**

`src/components/blocs/CtaFinal.astro` ligne 15, remplacer :
```astro
<section class="bg-pure-black py-24">
```
par :
```astro
<section class="bg-marine-deep py-24">
```

- [ ] **Step 4: Secteurs → marine (moyen, per rythme §4)**

`src/components/blocs/SecteursPhares.astro` ligne 15, remplacer :
```astro
<section class="py-20 bg-pure-black">
```
par :
```astro
<section class="py-20 bg-marine">
```

- [ ] **Step 5: Bande CTA équipe → marine-deep**

`src/pages/equipe.astro` ligne 106, remplacer :
```astro
  <section class="bg-pure-black py-20">
```
par :
```astro
  <section class="bg-marine-deep py-20">
```

- [ ] **Step 6: Nav glass → rgba marine**

`src/components/layout/Header.astro` ligne 8, remplacer `bg-[rgba(0,0,0,0.8)]` par `bg-[rgba(15,36,54,0.8)]` :
```astro
<header class="fixed top-0 inset-x-0 z-50 h-12 bg-[rgba(15,36,54,0.8)] backdrop-blur-[20px] backdrop-saturate-[180%]" data-nav-glass>
```
Ligne 48, remplacer `bg-[rgba(0,0,0,0.95)]` par `bg-[rgba(15,36,54,0.95)]` :
```astro
  <div class="hidden md:hidden bg-[rgba(15,36,54,0.95)] backdrop-blur-[20px]" data-menu-panel>
```

- [ ] **Step 7: Vérifier le build + absence de `bg-pure-black` résiduel**

Run: `npm run build && grep -rn "bg-pure-black" src/`
Expected: build OK ; le grep ne retourne **aucune** occurrence.

- [ ] **Step 8: Commit**

```bash
git add src/components/blocs/Hero.astro src/components/blocs/HeroPage.astro src/components/blocs/CtaFinal.astro src/components/blocs/SecteursPhares.astro src/pages/equipe.astro src/components/layout/Header.astro
git commit -m "feat(design-system): bascule les surfaces immersives et la nav en marine

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 3: Titres en marine — composants blocs (display & cartes)

**Files:**
- Modify: `src/components/blocs/CartesExpertises.astro:10`
- Modify: `src/components/blocs/ReferencesRecentes.astro:14`
- Modify: `src/components/blocs/EquipePreview.astro:26`
- Modify: `src/components/blocs/ProjetsSimilaires.astro:31`
- Modify: `src/components/primitives/Chiffre.astro:16`
- Modify: `src/components/blocs/CarteExpertise.astro:17`
- Modify: `src/components/blocs/CarteActualite.astro:37`
- Modify: `src/components/blocs/CarteProjet.astro:45`
- Modify: `src/components/blocs/FAQ.astro:18`
- Modify: `src/components/blocs/FicheTechnique.astro:25`
- Modify: `src/components/blocs/Hero.astro:39`

**Interfaces:**
- Consumes : `text-marine` (Task 1).
- Règle : on ne change QUE la couleur des titres (`h1`–`h3`, gros chiffres, titres de carte). On NE touche PAS aux valeurs `dd`, labels, badges (`FicheTechnique.astro:38`, `Capsule.astro`).

- [ ] **Step 1: Appliquer `text-near-black` → `text-marine` sur ces titres**

Sur chaque ligne ci-dessous, remplacer la sous-chaîne `text-near-black` par `text-marine` (le reste de la classe inchangé) :

| Fichier | Ligne | Élément |
|---|---|---|
| `CartesExpertises.astro` | 10 | `<h2>` section |
| `ReferencesRecentes.astro` | 14 | `<h2>` section |
| `EquipePreview.astro` | 26 | `<h2>` section |
| `ProjetsSimilaires.astro` | 31 | `<h2>` section |
| `Chiffre.astro` | 16 | gros chiffre (display) |
| `CarteExpertise.astro` | 17 | `<h3>` carte (garde `group-hover:text-apple-blue`) |
| `CarteActualite.astro` | 37 | `<h3>` carte |
| `CarteProjet.astro` | 45 | `<h3>` carte |
| `FAQ.astro` | 18 | `<summary>` (titre question) |
| `FicheTechnique.astro` | 25 | `<h2>` « Fiche technique » |
| `Hero.astro` | 39 | `<h1>` variante non-accueil (fond clair) |

Exemple (CarteExpertise.astro:17) — avant :
```astro
  <h3 class="font-heading font-semibold text-near-black text-lg tracking-tight group-hover:text-apple-blue transition-colors">
```
après :
```astro
  <h3 class="font-heading font-semibold text-marine text-lg tracking-tight group-hover:text-apple-blue transition-colors">
```

- [ ] **Step 2: Vérifier qu'aucun titre-body n'a été touché par erreur**

Run: `grep -n "text-near-black" src/components/blocs/FicheTechnique.astro`
Expected: la ligne 38 (`<dd ... text-near-black ...>`) est **toujours présente** (valeur de fiche = body, on la garde).

- [ ] **Step 3: Vérifier le build**

Run: `npm run build`
Expected: build OK.

- [ ] **Step 4: Commit**

```bash
git add src/components/blocs/CartesExpertises.astro src/components/blocs/ReferencesRecentes.astro src/components/blocs/EquipePreview.astro src/components/blocs/ProjetsSimilaires.astro src/components/primitives/Chiffre.astro src/components/blocs/CarteExpertise.astro src/components/blocs/CarteActualite.astro src/components/blocs/CarteProjet.astro src/components/blocs/FAQ.astro src/components/blocs/FicheTechnique.astro src/components/blocs/Hero.astro
git commit -m "feat(design-system): titres des blocs en marine

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 4: Titres en marine — pages (prose long-form & headings explicites)

**Files:**
- Modify: `src/pages/societe.astro:26,50,64,76`
- Modify: `src/pages/equipe.astro:69,91`
- Modify: `src/pages/actualites/[...slug].astro:73,76`
- Modify: `src/pages/references/[...slug].astro:75,78`
- Modify: `src/pages/expertises/[...slug].astro:72,75,94,124,149`
- Modify: `src/pages/accessibilite.astro:23`
- Modify: `src/pages/mentions-legales.astro:23`
- Modify: `src/pages/politique-confidentialite.astro:23`
- Modify: `src/pages/404.astro:13,14`
- Modify: `src/components/blocs/FormulaireContact.astro:9,15,118,136`
- Modify: `src/components/seo/Breadcrumbs.astro:34`

**Interfaces:**
- Consumes : `text-marine` (Task 1).
- Règle critique : dans les blocs prose, migrer UNIQUEMENT les variantes titre `[&>h2]:text-near-black` et `[&>h3]:text-near-black`. **NE PAS** toucher `[&_strong]:text-near-black` (gras dans le body → reste near-black). Les labels de formulaire (`FormulaireContact.astro:28,42,56,68`) restent near-black.

- [ ] **Step 1: Migrer les variantes titre prose**

Dans chaque fichier, remplacer les occurrences `[&>h2]:text-near-black` → `[&>h2]:text-marine` et `[&>h3]:text-near-black` → `[&>h3]:text-marine`. Laisser intact tout `[&_strong]:text-near-black`.

Fichiers concernés (variantes prose `[&>h2]`/`[&>h3]`) : `societe.astro:26,76`, `actualites/[...slug].astro:73,76`, `references/[...slug].astro:75,78`, `expertises/[...slug].astro:72,75`, `accessibilite.astro:23`, `mentions-legales.astro:23`, `politique-confidentialite.astro:23`.

Exemple (actualites/[...slug].astro) — avant :
```astro
               [&>h2]:font-heading [&>h2]:font-semibold [&>h2]:text-near-black [&>h2]:tracking-tight
```
après :
```astro
               [&>h2]:font-heading [&>h2]:font-semibold [&>h2]:text-marine [&>h2]:tracking-tight
```

- [ ] **Step 2: Migrer les titres explicites `<h1>/<h2>/<h3>` des pages**

Remplacer `text-near-black` → `text-marine` sur ces lignes de titres explicites :

| Fichier | Lignes |
|---|---|
| `societe.astro` | 50 (`<h2>`), 64 (`<h3>`) |
| `equipe.astro` | 69 (`<h2>`), 91 (`<h3>`) |
| `expertises/[...slug].astro` | 94, 124, 149 (`<h2>` de section) |
| `404.astro` | 13 (`<p>` display 404), 14 (`<h1>`) |
| `FormulaireContact.astro` | 9 (`<h2>`), 15 (`<legend>`), 118 (`<h3>`), 136 (`<h3>`) |

- [ ] **Step 3: Breadcrumb « current » → marine (fil d'Ariane sur clair)**

`src/components/seo/Breadcrumbs.astro` ligne 34, remplacer :
```astro
    current: 'text-near-black font-medium',
```
par :
```astro
    current: 'text-marine font-medium',
```

- [ ] **Step 4: Vérifier que les `[&_strong]` et labels sont intacts**

Run: `grep -rn "\[&_strong\]:text-near-black" src/pages/`
Expected: les occurrences `[&_strong]:text-near-black` sont **toujours présentes** (societe, actualites, references, expertises, accessibilite, mentions-legales, politique-confidentialite).

Run: `grep -n "text-near-black" src/components/blocs/FormulaireContact.astro`
Expected: les lignes 28, 42, 56, 68 (labels `<label>`) sont **toujours** en `text-near-black`.

- [ ] **Step 5: Vérifier le build**

Run: `npm run build`
Expected: build OK.

- [ ] **Step 6: Commit**

```bash
git add src/pages/ src/components/blocs/FormulaireContact.astro src/components/seo/Breadcrumbs.astro
git commit -m "feat(design-system): titres des pages en marine, body inchangé

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 5: Sous-titres sur fond sombre → `mist`

**Files:**
- Modify: `src/components/blocs/HeroPage.astro:58`
- Modify: `src/components/blocs/CtaFinal.astro:20`
- Modify: `src/components/blocs/SecteursPhares.astro:41`
- Modify: `src/pages/equipe.astro:111`
- Modify: `src/components/blocs/Hero.astro:66`

**Interfaces:**
- Consumes : `text-mist` (Task 1).
- Règle : `mist` #9FB0BF passe AA sur `marine` (5,9:1) et `marine-deep` (7,1:1). On migre les sous-titres principaux `white/70` (+ le sous-titre accueil `white/80`). On **laisse** les `white/50` et `white/60` peu visibles (dates, breadcrumb) tels quels.

- [ ] **Step 1: Migrer les sous-titres `white/70` → `text-mist`**

| Fichier | Ligne | Avant → Après |
|---|---|---|
| `HeroPage.astro` | 58 | `text-white/70` → `text-mist` |
| `CtaFinal.astro` | 20 | `text-white/70` → `text-mist` |
| `SecteursPhares.astro` | 41 | `text-white/70` → `text-mist` |
| `equipe.astro` | 111 | `text-white/70` → `text-mist` |

Exemple (CtaFinal.astro:20) — avant :
```astro
    <p class="mt-4 text-white/70 text-lg tracking-tight max-w-xl mx-auto" data-reveal>
```
après :
```astro
    <p class="mt-4 text-mist text-lg tracking-tight max-w-xl mx-auto" data-reveal>
```

- [ ] **Step 2: Sous-titre hero accueil `white/80` → `mist`**

`src/components/blocs/Hero.astro` ligne 66, remplacer :
```astro
          isAccueil ? 'text-white/80' : 'text-text-secondary',
```
par :
```astro
          isAccueil ? 'text-mist' : 'text-text-secondary',
```

- [ ] **Step 3: Vérifier le build**

Run: `npm run build`
Expected: build OK.

- [ ] **Step 4: Commit**

```bash
git add src/components/blocs/HeroPage.astro src/components/blocs/CtaFinal.astro src/components/blocs/SecteursPhares.astro src/pages/equipe.astro src/components/blocs/Hero.astro
git commit -m "feat(design-system): sous-titres sur fond sombre en gris-bleu mist

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 6: (Recommandé, optionnel) Logo bi-thème + bloc de marque au footer

> Cette tâche donne un vrai consommateur au lockup clair et au token `slate`, et complète réellement « l'intégration du logo » (aujourd'hui présent seulement dans la nav). Peut être sautée sans casser les tâches précédentes.

**Files:**
- Modify: `src/components/layout/Logo.astro` (entier)
- Modify: `src/components/layout/Footer.astro:8-14` (ajout bloc de marque)

**Interfaces:**
- Produces : `Logo` accepte `theme?: 'dark' | 'light'` (défaut `'dark'`) et `class?: string`.
  - `dark` → cadre `stroke-cool-white`, flux `stroke-bright-copper` (usage nav, inchangé visuellement sauf encre blanc froid).
  - `light` → cadre `stroke-marine`, flux `stroke-copper` (usage footer, contexte clair).
- Consumes : `cool-white`, `marine`, `copper`, `bright-copper`, `slate` (Task 1).

- [ ] **Step 1: Paramétrer `Logo.astro` avec la prop `theme`**

Remplacer l'intégralité de `src/components/layout/Logo.astro` par :

```astro
---
// Pictogramme « flux dans le cadre » — mark de marque FT2E.
// Cadre bâti (encre) traversé par un flux continu (cuivre) : l'ingénierie
// rend le bâtiment perméable à l'énergie.
//
// Décoratif : le lien parent porte déjà aria-label + le wordmark texte « FT2E ».
// theme='dark'  → nav / fond sombre : cadre blanc froid, flux cuivre clair.
// theme='light' → footer / fond clair : cadre marine, flux cuivre.
interface Props {
  class?: string;
  theme?: 'dark' | 'light';
}

const { class: className, theme = 'dark' } = Astro.props;

const frame = theme === 'dark' ? 'stroke-cool-white' : 'stroke-marine';
const flux = theme === 'dark' ? 'stroke-bright-copper' : 'stroke-copper';
const frameHover = theme === 'dark' ? 'group-hover:stroke-bright-copper' : 'group-hover:stroke-copper';
const fluxHover = theme === 'dark' ? 'group-hover:stroke-cool-white' : 'group-hover:stroke-marine';
---

<svg
  viewBox="0 0 90 90"
  class:list={['block h-[26px] w-auto shrink-0', className]}
  aria-hidden="true"
  focusable="false"
>
  <g transform="translate(5,5)" fill="none" stroke-width="7">
    <!-- Cadre structurel, ouvert à gauche et à droite au passage du flux -->
    <path
      class:list={[frame, frameHover, 'motion-safe:transition-colors motion-safe:duration-500 motion-safe:ease-[var(--ease-apple)]']}
      stroke-linejoin="miter"
      d="M3.5,42 V3.5 H76.5 V42 M76.5,66 V76.5 H3.5 V66"
    />
    <!-- Flux continu : entre, dessert, ressort -->
    <path
      class:list={[flux, fluxHover, 'motion-safe:transition-colors motion-safe:duration-500 motion-safe:ease-[var(--ease-apple)]']}
      stroke-linecap="round"
      stroke-linejoin="round"
      d="M-3,54 H26 V26 H54 V54 H83"
    />
  </g>
</svg>
```

- [ ] **Step 2: Ajouter le bloc de marque clair au footer**

`src/components/layout/Footer.astro` : ajouter l'import du Logo en tête du frontmatter (après la ligne 3) :
```astro
import Logo from './Logo.astro';
```
Puis remplacer le bloc `<div class="py-4 border-b border-gris-bord">…</div>` (lignes 10-14) par :
```astro
    <div class="py-6 border-b border-gris-bord flex flex-col sm:flex-row sm:items-center gap-4">
      <div class="flex items-center gap-2 text-marine font-heading font-semibold text-lg leading-none tracking-tight shrink-0">
        <Logo theme="light" />
        <span aria-hidden="true">FT<span class="text-copper">2</span>E</span>
        <span class="ml-3 text-[0.7rem] font-normal uppercase tracking-[0.16em] text-slate">Bureau d'études techniques</span>
      </div>
      <p class="text-xs text-text-secondary leading-relaxed max-w-2xl">
        Bureau d’études techniques pluridisciplinaire à La Rochelle. Fluides, thermique, électricité, SSI, BIM. Au service des architectes et maîtres d’ouvrage depuis 2008.
      </p>
    </div>
```

- [ ] **Step 3: Vérifier le build et le rendu du lockup**

Run: `npm run build`
Expected: build OK. Le footer affiche le pictogramme marine + « FT2E » (2 cuivre) + tagline ardoise sur fond blanc froid.

- [ ] **Step 4: Vérifier les contrastes du lockup clair**

Contrôle manuel (spec §6) : `marine` sur `cool-white` = 11,5:1 ✅ ; `slate` sur `cool-white` = 7,0:1 ✅ ; `copper` = gros glyphe de marque uniquement (le « 2 » est un glyphe de wordmark, pas un lien) ✅.

- [ ] **Step 5: Commit**

```bash
git add src/components/layout/Logo.astro src/components/layout/Footer.astro
git commit -m "feat(layout): logo bi-thème et bloc de marque clair au footer

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 7: Documentation, règles, skill & mémoire

**Files:**
- Modify: `CLAUDE.md` (tableau palette § « Palette »)
- Modify: `docs/02-design-system.md`
- Modify: `.claude/rules/tailwind-design-tokens.md`
- Modify: `.claude/rules/accessibility-rgaa.md`
- Modify: `.claude/skills/ft2e-design-system/SKILL.md`
- Modify: `C:\Users\rougi\.claude\projects\c--claude-code-dev-projects-ft2e-site\memory\project-design-apple.md` + `MEMORY.md`

**Interfaces:**
- Consumes : la palette figée (spec §3) et le tableau de contraste (spec §6).
- Règle : la doc est source de vérité ; elle doit refléter exactement les tokens du `@theme`.

- [ ] **Step 1: `CLAUDE.md` — mettre à jour le tableau « Palette »**

Remplacer les lignes `pure-black`, `light-gray`, `near-black`, `dark-surface-*` du tableau palette par les entrées marine (`marine-deep`, `marine`, `marine-surface`), `cool-white`, `slate`, `mist`, et ajuster la description : `near-black` = body, `marine` = titres. Marquer `pure-black` comme legacy. Mettre à jour la ligne de la section « Navigation » : glass `rgba(15,36,54,0.8)` au lieu de `rgba(0,0,0,0.8)`.

- [ ] **Step 2: `docs/02-design-system.md` + `.claude/rules/tailwind-design-tokens.md`**

Reporter le système de tokens du spec §3 (tableau complet, stratégie de repointage, rôles). Mettre à jour les patterns d'exemple (fonds `bg-marine-deep`/`bg-marine`, titres `text-marine`).

- [ ] **Step 3: `.claude/rules/accessibility-rgaa.md` — tableau des combinaisons validées**

Remplacer le tableau de contraste par celui du spec §6 (16 combinaisons marine/cool-white/slate/mist + règle `bright-blue` sur `marine-deep`).

- [ ] **Step 4: `.claude/skills/ft2e-design-system/SKILL.md`**

Mettre à jour la table palette et le « rythme cinématique des sections » (spec §4 : marine-deep / cool-white / white / marine).

- [ ] **Step 5: Mémoire `project-design-apple`**

Mettre à jour `project-design-apple.md` : noter l'évolution « Apple → palette logo marine + cuivre », lister les tokens fondateurs, lier `[[reference-branding-test]]`. Mettre à jour la ligne correspondante dans `MEMORY.md`.

- [ ] **Step 6: Commit**

```bash
git add CLAUDE.md docs/02-design-system.md .claude/rules/tailwind-design-tokens.md .claude/rules/accessibility-rgaa.md .claude/skills/ft2e-design-system/SKILL.md
git commit -m "docs(design-system): documente la palette marine dans la source de vérité

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 8: Vérification finale (build, lint, typecheck, anti-hardcode, Lighthouse)

**Files:** aucun a priori (tâche de contrôle ; corriger inline si un grep remonte quelque chose).

- [ ] **Step 1: Grep anti-hardcode**

Run: `grep -rn "bg-pure-black\|#000000\|#1d1d1f\|#f5f5f7\|rgba(0, ?0, ?0, ?0\.8)\|rgba(0,0,0,0\.95)" src/ --include=*.astro`
Expected: aucune couleur de fond/texte codée en dur hors tokens. (Les `rgba(0,0,0,0.22)` d'ombre et `rgba(0,0,0,0.08)` de bordure legacy sont tolérés — ils ne sont pas des couleurs de fond/texte.) Corriger toute occurrence résiduelle.

- [ ] **Step 2: Build + lint + typecheck**

Run: `npm run build && npm run lint && npm run typecheck`
Expected: les trois passent sans erreur.

- [ ] **Step 3: Lighthouse Accessibilité (accueil + une page interne)**

Run: `npm run build && npm run preview` puis dans un autre terminal :
`npx lighthouse http://localhost:4321 --only-categories=accessibility --quiet --chrome-flags="--headless"`
Puis une page interne (ex. `/references`).
Expected: score Accessibilité **100/100** sur les deux. Toute régression < 100 = blocage à corriger avant de continuer.

- [ ] **Step 4: Revue visuelle rapide**

Vérifier à l'œil (`npm run preview`) : hero marine profond, nav qui se solidifie en marine au scroll sur l'accueil, sections claires en blanc froid, titres marine, cartes marine sur sections sombres, sous-titres gris-bleu, CTA bleu inchangé, logo lisible.

- [ ] **Step 5: Commit (si correctifs) + fin**

```bash
git add -A
git commit -m "fix(design-system): nettoie les dernières valeurs hors tokens

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Self-review (couverture du spec)

- Spec §2 (approche marine + sous-décisions) → Tasks 1, 2, 3 (titres marine / body near-black).
- Spec §3 (tokens) → Task 1.
- Spec §4 (rythme cinématique) → Task 2 (bg marine-deep/marine) — Chiffres/Équipe/Partenaires restent cool-white/white via repointage.
- Spec §5 (composants/fichiers) → Tasks 2-6.
- Spec §6 (a11y) → Task 8 Step 3 + contrôles inline.
- Spec §7 (doc/mémoire) → Task 7.
- Spec §9 (critères d'acceptation) → Task 8.
- `slate` / lockup clair du Logo → Task 6 (leur seul consommateur ; optionnel).
