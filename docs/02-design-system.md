# 02 · Design System

> **Minimalisme cinematique.** Le site s'efface devant le projet. Chaque section est une scene ; chaque transition de fond, un changement de lumiere. Fondation Apple (minimalisme, rythme noir/blanc, Inter partout, accent bleu d'action) desormais **derivee du logo** : bleu marine encre et blanc froid remplacent le noir pur et le gris clair des surfaces et des titres.

---

## 1. Philosophie visuelle

Le design system FT2E adopte l'esthetique Apple — minimalisme cinematique, sections sombres/claires alternees, produit (= projet FT2E) comme heros, interface qui s'efface devant le contenu — dont la fondation chromatique a evolue (2026-07-03) pour decouler du logo « flux dans le cadre » : marine encre a la place du noir pur, blanc froid a la place du gris clair.

Principes directeurs :

- **Le contenu est le hero.** Pas de decoration superflue, pas de bordure gratuite, pas d'ombre par defaut. Le projet parle pour lui-meme.
- **Rythme cinematique.** Le site se lit comme une succession de scenes (marine profond, blanc froid, blanc, marine...). Chaque changement de fond marque une nouvelle unite narrative.
- **Trois registres, un accent d'action isole.** La **structure** (surfaces sombres et titres) vit desormais sur l'echelle marine (`marine-deep` / `marine` / `marine-surface`), a la place du noir/near-black. L'**identite** reste portee par le cuivre (`copper` / `bright-copper`) — logo, chiffre « 2 » du wordmark, eyebrow, filet — sans jamais signaler une action. L'**action** reste l'unique privilege du bleu Apple (`apple-blue` / `link-blue` / `bright-blue`) : CTA, liens, focus. Le gris-bleu de baseline (`slate` / `mist`) porte le texte secondaire.
- **Inter comme substitute libre de SF Pro.** Police unique, chargee en local, qui reproduit la neutralite elegante de la typographie Apple.
- **Densite maitrisee.** Padding vertical genereux, conteneur etroit (980 px), texte centre pour les titres de section.

---

## 2. Palette

> Evolution du 2026-07-03 : la fondation chromatique decoule desormais du logo « flux dans le cadre » (`logo/logo-1-flux-cadre.svg` et sa variante fond sombre). Le marine remplace le noir pur pour les surfaces sombres et les titres ; le blanc froid remplace le gris clair. Voir la spec `docs/superpowers/specs/2026-07-03-evolution-palette-logo-design.md`.

### Echelle marine — structure (surfaces sombres, titres)

| Nom | Hex | Token CSS | Usage | Remplace |
|---|---|---|---|---|
| Marine Deep | `#0f2436` | `--color-marine-deep` | hero, CTA final, nav solidifiee — fond le plus immersif | `pure-black` (surfaces immersives) |
| Marine | `#16324f` | `--color-marine` | sections sombres, **titres** (`h1`–`h6`) sur fond clair, nav | `pure-black` (sections) + `near-black` (titres) |
| Marine Surface | `#1d3a57` | `--color-marine-surface` | cartes sur fond sombre | `dark-surface-1` |
| Marine Surface 2 | `#223f5e` | `--color-marine-surface-2` | variation de surface sombre | `dark-surface-2` |

### Blanc froid & encre body

| Nom | Hex | Token CSS | Usage | Remplace |
|---|---|---|---|---|
| Cool White | `#edf1f5` | `--color-cool-white` | fond clair alterne, cartes, footer | `light-gray #f5f5f7` |
| Near Black | `#1d1d1f` | `--color-near-black` | **body** (texte courant) sur fond clair — inchange | — |

Le **body** (paragraphes, listes, texte courant) reste en `near-black` pour le confort de lecture ; seuls les **titres** passent en `marine`.

### Gris-bleu de baseline — texte secondaire

| Nom | Hex | Token CSS | Usage |
|---|---|---|---|
| Slate | `#45535f` | `--color-slate` | texte secondaire, legendes, baseline sur fond clair |
| Mist | `#9fb0bf` | `--color-mist` | texte secondaire, baseline sur fond marine |

### Accent d'action — bleu (inchange)

| Nom | Hex | Token CSS | Usage |
|---|---|---|---|
| Apple Blue | `#0071e3` | `--color-apple-blue` | accent d'action, CTA, focus ring |
| Link Blue | `#0066cc` | `--color-link-blue` | liens texte sur fond clair |
| Bright Blue | `#2997ff` | `--color-bright-blue` | liens texte sur fond sombre — reserve a `marine-deep` (voir §11 et la regle a11y) |

### Accent d'identite — cuivre (inchange)

Le cuivre porte la chaleur de la marque FT2E (le troisieme adjectif de la voix : « chaleureuse »). Le cuivre est l'accent d'**identite** ; le bleu reste l'accent d'**action** ; le marine porte desormais la **structure**. Le cuivre n'habille jamais un element cliquable pour signaler une action — il sert la marque : logo, chiffre « 2 » du wordmark, eyebrow, filet.

| Nom | Hex | Token CSS | Usage |
|---|---|---|---|
| Copper | `#c46a38` | `--color-copper` | accent d'identite sur fond clair |
| Bright Copper | `#d98a55` | `--color-bright-copper` | accent d'identite sur fond sombre |

### Surfaces de boutons

| Nom | Hex | Token CSS | Usage |
|---|---|---|---|
| Button Active | `#ededf2` | `--color-button-active` | etat active/pressed des boutons secondaires |
| Button Light | `#fafafc` | `--color-button-light` | fond bouton secondaire au repos |

### Texte semantique

| Nom | Valeur | Token CSS | Usage |
|---|---|---|---|
| Text Primary | `#1d1d1f` | `--color-text-primary` | texte principal, titres sur fond clair |
| Text Secondary | `rgba(0,0,0,0.8)` | `--color-text-secondary` | sous-titres, texte d'accompagnement |
| Text Tertiary | `rgba(0,0,0,0.48)` | `--color-text-tertiary` | legendes, metadonnees, texte desactive |

### Etats

| Nom | Hex | Token CSS | Usage |
|---|---|---|---|
| Success | `#30d158` | `--color-success` | confirmation formulaire, validation |
| Error | `#ff3b30` | `--color-error` | erreur de validation, champ invalide |

### Pure Black — legacy

| Nom | Hex | Token CSS | Usage |
|---|---|---|---|
| Pure Black | `#000000` | `--color-pure-black` | **legacy** — conserve comme alias, n'est plus utilise pour les surfaces (« plus de noir pur ») |

### Strategie de repointage (churn minimal)

Deux mouvements distincts, selon que le **role** d'un token est preserve ou change :

- **Repointage** (role preserve, valeur seule change) : `light-gray` → `#edf1f5` (meme role : fond clair alterne — toutes les classes `bg-light-gray` deviennent blanc froid automatiquement) ; `dark-surface-1` / `dark-surface-2` → `#1d3a57` / `#223f5e` (meme role : cartes sur fond sombre) ; alias legacy `bleu-nuit` → `marine-deep #0f2436`.
- **Migration** (role change, references a mettre a jour dans les composants) : `bg-pure-black` → `bg-marine-deep` (surfaces immersives) ; `text-near-black` **sur un titre** → `text-marine` (le body et le texte courant conservent `near-black`).

### Aliases legacy

Pour assurer la compatibilite avec les references existantes dans le code et la documentation, les anciens tokens sont mappes vers la nouvelle palette dans le CSS :

| Ancien token | Nouvelle valeur | Justification |
|---|---|---|
| `bleu-nuit` | `#0f2436` (Marine Deep) | Les sections d'autorite passent au marine profond (plus de noir pur) |
| `sarcelle` | `#0071e3` (Apple Blue) | L'accent principal reste le bleu Apple |
| `cuivre` | `#0071e3` (Apple Blue) | Alias legacy inchange (aucun composant ne l'utilise). Le cuivre de marque vit desormais dans les tokens dedies `copper` / `bright-copper`, voir « Accent d'identite » ci-dessus |
| `creme-pierre` | `#edf1f5` (Cool White) | Le fond de respiration passe au blanc froid du logo |
| `anthracite` | `#1d1d1f` (Near Black) | Le texte courant reste en near-black |

Ces aliases permettent de ne pas casser les composants existants tout en migrant progressivement vers les nouveaux tokens.

---

## 3. Configuration CSS (Tailwind v4)

### Source de verite

La source de verite du design system est le fichier `src/styles/global.css`, via le bloc `@theme`. **Il n'y a pas de fichier `tailwind.config.ts`.** Tailwind v4 utilise le CSS natif pour la configuration.

### Structure du bloc @theme

```css
/* src/styles/global.css */
@import "tailwindcss";
@import "@fontsource-variable/inter";

@theme {
  /* --- Echelle marine (structure) --- */
  --color-marine-deep: #0f2436;      /* hero, CTA final, nav solidifiee */
  --color-marine: #16324f;           /* sections sombres, titres sur clair, nav */
  --color-marine-surface: #1d3a57;   /* cartes sur fond sombre */
  --color-marine-surface-2: #223f5e; /* variation surface sombre */

  /* --- Blanc froid, encre body, baseline --- */
  --color-cool-white: #edf1f5;       /* fond clair alterne, cartes, footer */
  --color-near-black: #1d1d1f;       /* body sur fond clair (inchange) */
  --color-slate: #45535f;            /* texte secondaire / baseline sur clair */
  --color-mist: #9fb0bf;             /* texte secondaire / baseline sur marine */

  /* --- Accent d'identite — cuivre (inchange) --- */
  --color-copper: #c46a38;
  --color-bright-copper: #d98a55;

  /* --- Accent d'action — bleu (inchange) --- */
  --color-apple-blue: #0071e3;
  --color-link-blue: #0066cc;
  --color-bright-blue: #2997ff;

  /* --- Tokens repointes (meme role, nouvelle valeur) --- */
  --color-light-gray: #edf1f5;       /* repointe → blanc froid */
  --color-dark-surface-1: #1d3a57;   /* repointe → marine-surface */
  --color-dark-surface-2: #223f5e;   /* repointe → marine-surface-2 */
  --color-pure-black: #000000;       /* legacy — ne plus utiliser pour les surfaces */
  --color-button-active: #ededf2;
  --color-button-light: #fafafc;

  /* --- Texte semantique --- */
  --color-text-primary: #1d1d1f;
  --color-text-secondary: rgba(0, 0, 0, 0.8);
  --color-text-tertiary: rgba(0, 0, 0, 0.48);

  /* --- Aliases legacy --- */
  --color-bleu-nuit: #0f2436;        /* repointe → marine-deep */
  --color-sarcelle: #0071e3;
  --color-cuivre: #0071e3;
  --color-creme-pierre: #edf1f5;     /* repointe → blanc froid */
  --color-anthracite: #1d1d1f;
  --color-success: #30d158;
  --color-error: #ff3b30;

  /* --- Typographie --- */
  --font-heading: "Inter Variable", "Helvetica Neue", Helvetica, Arial, system-ui, sans-serif;
  --font-body: "Inter Variable", "Helvetica Neue", Helvetica, Arial, system-ui, sans-serif;

  /* --- Ombres --- */
  --shadow-soft: 3px 5px 30px rgba(0, 0, 0, 0.22);
}
```

### Regles d'usage

- **Aucune valeur de couleur hard-codee** dans les fichiers `.astro` ou `.ts`. Tout passe par les tokens definis dans `@theme`.
- Les classes Tailwind generees correspondent directement aux tokens : `bg-marine-deep`, `text-marine`, `bg-cool-white`, `text-apple-blue`, etc.
- Les classes issues des tokens repointes (`bg-light-gray`, `bg-dark-surface-1`, `bg-dark-surface-2`) restent valides et rendent desormais les nouvelles valeurs marine/blanc froid automatiquement.
- Les aliases legacy generent les classes `bg-bleu-nuit`, `text-sarcelle`, etc., pour la retrocompatibilite.

---

## 4. Typographie

### Police

**Police unique : Inter Variable**, substitute libre de SF Pro. Chargee en local via `@fontsource-variable/inter`. Pas de Google Fonts CDN (RGPD).

- **Titres (heading)** : Inter Variable, Helvetica Neue, Helvetica, Arial, system-ui, sans-serif
- **Corps (body)** : identique
- `font-display: swap` obligatoire.
- **Pas de Manrope.** Pas de JetBrains Mono (sauf bloc code eventuel en `monospace`).

### Echelle typographique

Style Apple : titres amples avec tracking serre, corps lisible avec tracking leger.

| Token | Taille | Line-height | Weight | Letter-spacing | Usage |
|---|---|---|---|---|---|
| Display Hero | `clamp(2.5rem, 5vw, 3.5rem)` | 1.07 | `font-semibold` (600) | `-0.015em` | `<h1>` de la page d'accueil, hero principal |
| Section Heading | `clamp(1.75rem, 3vw, 2.5rem)` | 1.10 | `font-semibold` (600) | `-0.01em` | `<h2>` de section |
| Heading 3 | `1.125rem` (`text-lg`) | 1.25 | `font-semibold` (600) | normal | `<h3>`, titres de carte |
| Body | `1rem` | 1.5 | `font-normal` (400) | `-0.01em` (`tracking-tight`) | texte courant |
| Small | `0.875rem` (`text-sm`) | 1.43 | `font-normal` (400) | normal | metadonnees, legendes |
| Caption | `0.75rem` (`text-xs`) | 1.33 | `font-normal` (400) | `0.08em` (`tracking-widest`), uppercase | labels, capsules, categories |

### Regles d'usage

- Un seul Display Hero par page.
- Pas de saut de niveau (`h3` sans `h2` parent).
- Texte long limite a `max-width: 68ch` pour la lisibilite.
- Pas de texte en justifie.

---

## 5. Grille & Layout

### Conteneur principal

```
max-w-[980px] mx-auto px-4 md:px-6
```

Le conteneur de 980 px est la largeur signature Apple. Il s'applique a tout le contenu textuel et aux grilles de cartes.

### Hero

Pleine largeur (`w-full`) avec contenu centre a l'interieur du conteneur 980 px. Le hero occupe toute la hauteur du viewport ou une hauteur significative.

### Navigation glass

Position fixed, contenu centre dans un conteneur `max-w-[980px]`. Hauteur 48 px. Voir section 9 pour les details.

### Footer

Fond `light-gray`, contenu organise en 4 colonnes sur un rythme de 12 px. Conteneur 980 px centre.

### Breakpoints

Breakpoints Tailwind par defaut conserves :

| Nom | min-width | Usage |
|---|---|---|
| (default) | 0 | mobile |
| `sm` | 640 px | petit tablet |
| `md` | 768 px | tablet |
| `lg` | 1024 px | desktop |
| `xl` | 1280 px | grand desktop |

---

## 6. Espacements

Echelle autorisee : **1, 2, 3, 4, 6, 8, 12, 16, 24, 32** (multiples Tailwind). Valeurs intermediaires (`5, 7, 9, 10...`) : refuser sans justification.

### Conventions de section

| Contexte | Espacement |
|---|---|
| Section standard | `py-20` |
| Section CTA / mise en avant | `py-24` |
| Gap entre cartes | `gap-4` (pas `gap-6`) |
| Espacement interne carte | `p-6` a `p-8` |
| Marge entre titre de section et contenu | `mb-12` a `mb-16` |

---

## 7. Rayons

Apple utilise deux familles de rayons, pas de valeurs intermediaires.

| Token | Valeur | Usage |
|---|---|---|
| `rounded-lg` | 8 px | cartes, conteneurs, modales, panneaux |
| `rounded-[980px]` | pill (quasi-infini) | CTA pill, capsules, badges, filtres, boutons d'action |
| `rounded-full` (50 %) | cercle | controles media circulaires, avatars |

**Ne pas utiliser** `rounded-sm` (2 px) ni `rounded` (4 px). Le design Apple utilise soit 8 px pour les conteneurs, soit la forme pill pour les elements interactifs.

---

## 8. Ombres

Une seule ombre autorisee :

```
shadow-soft = 3px 5px 30px rgba(0, 0, 0, 0.22)
```

### Regles d'usage

- **Pas d'ombre par defaut** sur les elements. Les cartes, boutons et conteneurs n'ont pas d'ombre au repos.
- `shadow-soft` est reserve au **hover des cartes** uniquement. C'est un signal d'interactivite.
- La profondeur visuelle se cree par **contraste de fond** et non par ombre :
  - Carte blanc froid (`bg-light-gray` → `#edf1f5`) sur fond blanc = profondeur implicite.
  - Carte marine (`bg-dark-surface-1` → `#1d3a57`) sur fond marine sombre = profondeur implicite.
- Pas de `shadow-md`, `shadow-lg`, `shadow-xl` Tailwind.

---

## 9. Navigation glass

La barre de navigation reprend le paradigme Apple : transparente, flottante, discrete.

### Specifications techniques

| Propriete | Valeur |
|---|---|
| Position | `fixed`, `z-50` |
| Hauteur | `h-12` (48 px) |
| Fond | `bg-marine-deep/80` (marine profond à 80 %) |
| Effet | `backdrop-filter: saturate(180%) blur(20px)` |
| Largeur contenu | `max-w-[980px]` centre |
| Panneau mobile | `bg-marine-deep/95` |

### Typographie de la nav

| Element | Style |
|---|---|
| Logo (texte "FT2E") | `font-heading font-semibold text-sm text-white` (14 px) |
| Liens de navigation | `text-xs text-white/80` (12 px), hover `text-white` |

### Compensation du fixed

Un `<div>` spacer de `h-12` est insere immediatement apres le `<header>` pour compenser la hauteur de la nav fixe et eviter que le contenu ne passe sous la barre.

---

## 10. Composants signature

### CTA pill (bouton d'action principal)

```
bg-apple-blue text-white rounded-[980px] px-4 py-2 font-semibold text-sm
hover:bg-apple-blue/90 transition-colors
```

Le bouton pill est la signature visuelle du site. Il est toujours bleu Apple, toujours arrondi en pill.

### Lien "En savoir plus"

```
text-apple-blue hover:underline inline-flex items-center gap-1
```

Suivi d'un chevron `>` en texte. Le lien Apple classique : bleu, discret, avec un chevron directionnel.

### Cartes fond clair (sur fond blanc)

```
bg-light-gray rounded-lg p-6
hover:shadow-soft transition-shadow
```

Pas de bordure. La profondeur vient du contraste entre le blanc froid (`#edf1f5`, via le token repointe `light-gray`) et le fond blanc.

### Cartes fond sombre (sur fond marine)

```
bg-dark-surface-1 rounded-lg p-6
```

Pas de bordure, pas d'ombre. Le contraste subtil entre `#1d3a57` (marine-surface, via le token repointe `dark-surface-1`) et `#0f2436`/`#16324f` (fond marine) suffit.

### Capsules (badges, filtres, categories)

```
bg-apple-blue/10 text-apple-blue rounded-[980px] px-3 py-1 text-xs font-medium
```

Fond bleu tres clair, texte bleu, forme pill. Utilisees pour les filtres de la page References et les categories de projet.

---

## 11. Rythme cinematique

Le rythme cinematique est le principe organisateur du site. Chaque section est une "scene" avec sa propre couleur de fond.

### Alternance des fonds

```
Hero          → bg-marine-deep  (#0f2436) — texte blanc froid / eyebrow cuivre clair
Chiffres      → bg-cool-white   (#edf1f5)
Services      → bg-white
Secteurs      → bg-marine        (#16324f) — texte blanc froid / eyebrow cuivre clair
References    → bg-white
Equipe        → bg-cool-white
Partenaires   → bg-white
CTA final     → bg-marine-deep  (#0f2436)
```

Le rythme alterne Apple survit : le noir devient marine profond, le gris clair devient blanc froid. Chaque changement de couleur de fond marque une nouvelle unite de contenu. Le visiteur "progresse" dans le site comme dans une presentation Apple.

### Regles

- **Titres de section centres.** Le texte d'introduction d'une section est centre (`text-center`), pas aligne a gauche.
- **Padding vertical genereux.** Minimum `py-20` entre les sections. `py-24` pour les sections de mise en avant.
- **Pas de bordure horizontale** entre les sections. Le changement de fond suffit.
- **Texte blanc sur fond marine sombre**, `near-black` sur fond clair (body), `marine` pour les titres sur fond clair. Pas de melange.
- **Les liens texte sur fond sombre vivent sur `marine-deep`** (hero, CTA final) — voir la regle `bright-blue` ci-dessous. La section Secteurs (`marine` moyen) n'expose pas de lien texte en petits caracteres ; l'interactivite y passe par un CTA plein.
- **Les images projets sont pleine largeur** ou cadrees dans le conteneur 980 px avec `rounded-lg`.

### Contrastes texte/fond valides

Ratios calcules contre le fond d'usage. Cible Lighthouse Accessibilite : **100/100**.

| Texte | Fond | Ratio | Statut |
|---|---|---|---|
| `marine #16324f` | blanc | 13.1:1 | titres |
| `marine #16324f` | `cool-white #edf1f5` | 11.5:1 | titres |
| `cool-white #edf1f5` | `marine #16324f` | 11.5:1 | OK |
| `cool-white #edf1f5` | `marine-deep #0f2436` | 13.9:1 | OK |
| blanc | `marine-deep #0f2436` | 15.8:1 | body sombre |
| blanc | `marine-surface #1d3a57` | 11.7:1 | cartes |
| `near-black #1d1d1f` | blanc | 16.5:1 | body |
| `slate #45535f` | blanc | 7.9:1 | OK |
| `slate #45535f` | `cool-white` | 7.0:1 | OK |
| `mist #9fb0bf` | `marine #16324f` | 5.9:1 | OK |
| `bright-copper #d98a55` | `marine-deep #0f2436` | 5.8:1 | eyebrow, « 2 » |
| `bright-copper #d98a55` | `marine #16324f` | 4.8:1 | eyebrow (petit texte) |
| `copper #c46a38` | blanc | 3.8:1 | gros glyphe de marque uniquement |
| `apple-blue #0071e3` | blanc | 4.6:1 | OK |
| `link-blue #0066cc` | blanc | 5.3:1 | liens clairs |
| `bright-blue #2997ff` | `marine-deep #0f2436` | 5.25:1 | liens sombres |
| `bright-blue #2997ff` | `marine #16324f` | 4.34:1 | texte large / UI uniquement |

**Regle `bright-blue` sur fond sombre.** `bright-blue` passe AA sur `marine-deep` (5,25:1) mais tombe a 4,34:1 sur le `marine` moyen. Les liens texte sur fond sombre vivent donc sur `marine-deep` ; sur une section `marine` moyen, l'interactivite passe par un CTA plein (`apple-blue`, texte blanc) ou un lien en gros caracteres (≥ 18 pt / 14 pt gras, seuil 3:1). Aucune autre combinaison non listee ci-dessus n'est autorisee sans validation prealable du ratio de contraste.

---

## 12. Mode sombre

**Non applicable.** Le site utilise nativement des sections sombres (fond marine) et des sections claires (fond blanc, fond blanc froid) en alternance. C'est le rythme cinematique Apple, pas un mode sombre classique.

- **Pas de classe `dark:`** dans le code.
- **Pas de `prefers-color-scheme`** a gerer.
- Le choix des couleurs de texte et de lien depend du fond de la section dans laquelle on se trouve (voir tableau des contrastes ci-dessus).

---

## 13. Logo FT2E

Le logo est un rendu typographique du wordmark « FT2E », affiche a gauche de la nav glass, accompagne du pictogramme « flux dans le cadre » (cadre bati ouvert, traverse par un flux cuivre). Le chiffre « 2 » est en cuivre (`bright-copper` sur fond sombre / `copper` sur fond clair) : c'est le point focal et la signature de marque. Au survol, « FT » et « E » passent au cuivre pendant que le « 2 » passe au blanc (inversion).

```
Texte « FT2E » — font-heading font-semibold text-lg text-white (ou text-marine en contexte clair)
« 2 » : text-bright-copper (fond sombre) / text-copper (fond clair), inversion de couleur au survol
```

**Integration complete du logo SVG (« flux dans le cadre »)** — deux declinaisons dans `logo/`, dont l'encre a fixe la fondation marine du design system (voir §2 et la spec `docs/superpowers/specs/2026-07-03-evolution-palette-logo-design.md`) :

- `logo-1-flux-cadre.svg` — encre marine `#16324f` + flux cuivre `#c46a38`, sur fond clair
- `logo-1-flux-cadre-fond-sombre.svg` — encre `#edf1f5` (blanc froid) + flux cuivre `#d98a55`, sur fond sombre

L'encre marine du SVG n'est plus reconciliee avec `near-black` : elle est devenue le token `marine`, utilise pour les titres sur fond clair et les surfaces sombres (`marine-deep` / `marine`). `Logo.astro` expose une prop `theme: 'dark' | 'light'` pour le lockup clair (cadre `marine`, flux `copper`), utilisable en contexte clair (footer, page claire).
