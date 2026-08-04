# Évolution de la palette : du modèle Apple à la palette du logo « flux dans le cadre »

> Spec de design — 2026-07-03. Fait suite à la livraison des deux fichiers logo
> (`logo/logo-1-flux-cadre.svg` et `logo/logo-1-flux-cadre-fond-sombre.svg`) et à la
> demande d'une **intégration complète** du logo, faisant évoluer la fondation
> chromatique du site.

## 1. Contexte & objectif

Une première intégration du logo a été faite partiellement (pictogramme dans la nav,
tokens `copper`/`bright-copper` ajoutés au `@theme`). Le cuivre est donc déjà exact.

Ce qui manque — et ce que « faire évoluer le modèle Apple vers le logo » implique — c'est
d'adopter la **fondation structurelle** portée par les SVG : un **bleu marine encre**
(`#16324F`) et un **blanc froid** (`#EDF1F5`) à la place du `pure-black #000000`, du
`near-black #1d1d1f` (pour les titres) et du `light-gray #f5f5f7`. Les SVG fournissent
aussi les gris-bleu de baseline (`#45535F` clair, `#9FB0BF` sombre) qui deviennent les
couleurs de texte secondaire.

**Objectif** : refondre la palette du design system pour qu'elle découle du logo, sans
casser la conformité RGAA AA (Lighthouse Accessibilité 100/100) ni la séparation
action/identité déjà en place.

### Source de vérité chromatique (extrait des SVG)

| Rôle dans le logo | Version claire | Version sombre |
|---|---|---|
| Encre (cadre + lettres F·T·E) | `#16324F` marine | `#EDF1F5` blanc froid |
| Accent (flux + « 2 ») | `#C46A38` cuivre | `#D98A55` cuivre clair |
| Baseline (tagline) | `#45535F` ardoise | `#9FB0BF` gris-bleu |

## 2. Décision retenue

**Approche « marine = fondation, bleu d'action conservé » (validée).** Trois registres de
structure/identité + un registre d'action isolé :

- **Structure** = échelle marine (remplace noir/near-black des surfaces et des titres).
- **Identité** = cuivre (`copper`/`bright-copper`) — inchangé, déjà exact.
- **Action** = bleu Apple (`apple-blue`/`link-blue`/`bright-blue`) — inchangé.
- **Encre secondaire** = gris-bleu de baseline (`slate`/`mist`).

Sous-décisions validées :

1. **Surfaces sombres** : échelle marine, plus de noir pur. `marine-deep #0F2436` pour le
   plus immersif (hero, CTA final, nav solidifiée) ; `marine #16324F` pour les sections
   sombres et la nav.
2. **Encre du texte** : titres (`h1`–`h6`) en `marine #16324F` ; **body reste `near-black
   #1d1d1f`** pour le confort de lecture.
3. **Liens sur fond sombre** : voir §6 (règle a11y `bright-blue`).
4. **Footer** : reste clair (`cool-white`), pas marine — churn minimal.
5. **Body sur sections sombres** : reste blanc pur (21:1). `cool-white` est réservé aux
   titres et au logo sur fond sombre.

La règle non-négociable du projet est préservée : **le cuivre ne signale jamais une
action** ; le bleu reste l'unique accent d'action.

## 3. Système de tokens cible

Source unique : `src/styles/global.css`, bloc `@theme`. Aucune valeur hors tokens.

### Nouveaux tokens

| Token | Hex | Rôle | Remplace |
|---|---|---|---|
| `marine-deep` | `#0F2436` | Hero, CTA final, nav solidifiée, fond le plus immersif | `pure-black` (surfaces immersives) |
| `marine` | `#16324F` | Sections sombres, **titres sur clair**, nav | `pure-black` (sections) + `near-black` (titres) |
| `marine-surface` | `#1D3A57` | Cartes sur fond sombre | `dark-surface-1` |
| `marine-surface-2` | `#223F5E` | Variation de surface sombre | `dark-surface-2` |
| `cool-white` | `#EDF1F5` | Fond clair alterné, cartes, footer | `light-gray #f5f5f7` |
| `slate` | `#45535F` | Texte secondaire, légendes, baseline sur clair | `text-tertiary` (informatif) |
| `mist` | `#9FB0BF` | Texte secondaire, baseline sur marine | `white/70` (secondaire sur sombre) |

### Tokens inchangés (conservés tels quels)

| Token | Hex | Rôle |
|---|---|---|
| `near-black` | `#1D1D1F` | **Body** sur fond clair |
| `copper` | `#C46A38` | Identité sur fond clair (logo, filet, « 2 ») |
| `bright-copper` | `#D98A55` | Identité sur fond sombre (eyebrow, « 2 », logo) |
| `apple-blue` | `#0071E3` | Remplissage CTA, anneau de focus |
| `link-blue` | `#0066CC` | Liens texte sur fond clair |
| `bright-blue` | `#2997FF` | Liens texte sur fond sombre (voir §6) |
| `success` / `error` | `#30D158` / `#FF3B30` | États sémantiques |

### Stratégie de repointage (churn minimal)

Là où le **rôle** d'un token est préservé, on repointe sa valeur plutôt que de migrer
toutes ses références :

- `light-gray` → **repointé** vers `#EDF1F5` (même rôle : fond clair alterné). Toutes les
  classes `bg-light-gray` deviennent blanc froid automatiquement.
- `dark-surface-1` / `dark-surface-2` → **repointés** vers `#1D3A57` / `#223F5E` (même
  rôle : cartes sur sombre). Les composants qui les utilisent s'alignent automatiquement.
- Alias legacy `bleu-nuit` → repointé vers `marine-deep #0F2436`.

Là où le **rôle change**, on migre les références (voir §5) :

- `bg-pure-black` → `bg-marine-deep` (surfaces immersives).
- `text-near-black` **sur un titre** → `text-marine`. `text-near-black` sur du body reste.

Le token `pure-black` (`#000000`) reste défini comme alias legacy mais n'est plus utilisé
pour les surfaces (« plus de noir pur »).

## 4. Rythme cinématique des sections (mis à jour)

Le rythme alterné Apple survit ; le noir devient marine profond, le gris clair devient
blanc froid.

```
Hero          → bg-marine-deep  (#0F2436) — texte blanc froid / eyebrow cuivre clair
Chiffres      → bg-cool-white   (#EDF1F5)
Services      → bg-white
Secteurs      → bg-marine        (#16324F) — texte blanc froid / eyebrow cuivre clair
Références    → bg-white
Équipe        → bg-cool-white
Partenaires   → bg-white
CTA final     → bg-marine-deep  (#0F2436)
```

## 5. Changements au niveau composant / fichier

Périmètre : ~35 fichiers `src/**` utilisent les patterns concernés. Détail exhaustif =
plan d'implémentation. Points structurants :

- **`src/styles/global.css`** (`@theme`) — cœur du changement : ajout des 7 nouveaux
  tokens, repointage de `light-gray`, `dark-surface-1/2`, `bleu-nuit`. Le `color` de base
  du `html` reste `near-black` (body).
- **`src/components/layout/Logo.astro`** — encre passe de `stroke-white` à
  `stroke-cool-white` ; ajout d'une prop `theme: 'dark' | 'light'` pour le lockup clair
  (cadre `marine`, flux `copper`) utilisable en contexte clair (footer, page claire).
  Le hover conserve l'inversion cadre ↔ flux.
- **`src/components/layout/Header.astro`** — nav glass : `bg-[rgba(0,0,0,0.8)]` →
  `bg-[rgba(15,36,54,0.8)]` ; panneau mobile `rgba(0,0,0,0.95)` → `rgba(15,36,54,0.95)` ;
  hover wordmark inchangé (déjà `bright-copper`).
- **`src/layouts/BaseLayout.astro`** — la logique `nav-transparent` (transparent sur hero
  sombre, se solidifie au scroll) est indépendante de la couleur ; rien à changer côté JS.
  Vérifier qu'aucune couleur `#000` n'est codée en dur dans le `<head>` (thème, meta).
- **Sections sombres** (`Hero`, `HeroPage`, `SecteursPhares`, `CtaFinal`, `Footer` si
  concerné) — `bg-pure-black` → `bg-marine-deep` ou `bg-marine` selon le rythme §4.
- **Titres sur fond clair** — `text-near-black` sur `h1`–`h3` → `text-marine`. Le body,
  les labels et le texte courant conservent `near-black` / `text-secondary`.
- **Cartes sur sombre** — récupèrent automatiquement les surfaces marine via le repointage
  de `dark-surface-*`.
- **Texte secondaire** — `white/70` sur sombre → `text-mist` ; `text-tertiary` informatif
  sur clair → `text-slate` (les légendes purement décoratives peuvent rester en
  `text-tertiary`).

## 6. Validation accessibilité (RGAA AA / WCAG 2.1)

Ratios calculés contre le fond d'usage. Cible Lighthouse Accessibilité : **100/100**.

| Texte | Fond | Ratio | Statut |
|---|---|---|---|
| `marine #16324F` | blanc | 13.1:1 | ✅ titres |
| `marine #16324F` | `cool-white #EDF1F5` | 11.5:1 | ✅ titres |
| `cool-white #EDF1F5` | `marine #16324F` | 11.5:1 | ✅ |
| `cool-white #EDF1F5` | `marine-deep #0F2436` | 13.9:1 | ✅ |
| blanc | `marine-deep #0F2436` | 15.8:1 | ✅ body sombre |
| blanc | `marine-surface #1D3A57` | 11.7:1 | ✅ cartes |
| `near-black #1D1D1F` | blanc | 16.5:1 | ✅ body |
| `slate #45535F` | blanc | 7.9:1 | ✅ |
| `slate #45535F` | `cool-white` | 7.0:1 | ✅ |
| `mist #9FB0BF` | `marine #16324F` | 5.9:1 | ✅ |
| `bright-copper #D98A55` | `marine-deep #0F2436` | 5.8:1 | ✅ eyebrow, « 2 » |
| `bright-copper #D98A55` | `marine #16324F` | 4.8:1 | ✅ eyebrow (petit texte) |
| `copper #C46A38` | blanc | 3.8:1 | ⚠️ gros glyphe de marque uniquement |
| `apple-blue #0071E3` | blanc | 4.6:1 | ✅ |
| `link-blue #0066CC` | blanc | 5.3:1 | ✅ liens clairs |
| `bright-blue #2997FF` | `marine-deep #0F2436` | 5.25:1 | ✅ liens sombres |
| `bright-blue #2997FF` | `marine #16324F` | 4.34:1 | ⚠️ texte large / UI uniquement |

### Règle `bright-blue` sur fond sombre (point tranché)

`bright-blue #2997FF` passe AA sur `marine-deep` (5,25:1) mais tombe à 4,34:1 sur le
`marine` moyen. **Règle** : les **liens texte sur fond sombre vivent sur `marine-deep`**.
Sur une section `marine` moyen, l'interactivité passe par un **CTA plein** (remplissage
`apple-blue`, texte blanc) ou un lien en gros caractères (≥ 18 pt / 14 pt gras, seuil
3:1). Cette contrainte guide le rythme §4 : le hero et le CTA final (qui portent des liens
texte) sont en `marine-deep` ; la section `Secteurs` en `marine` moyen n'expose pas de
lien texte en petits caractères.

### Distinction titre marine ↔ lien bleu

Les titres passent en `marine`, proche des bleus d'action. La distinction repose sur le
**poids** (titres 600, larges, jamais soulignés) et l'**affordance de lien** (soulignement
au hover, flux de texte). Aucun titre ne prend une couleur de lien ; aucun lien ne prend
`marine`.

## 7. Documentation & mémoire à mettre à jour (partie de l'intégration « complète »)

Le projet traite les tokens comme source de vérité ; la doc doit suivre, sinon elle ment.

- `CLAUDE.md` — tableau de palette (section « Design system »).
- `docs/02-design-system.md` — tokens détaillés.
- `.claude/rules/tailwind-design-tokens.md` — tokens autorisés + patterns.
- `.claude/rules/accessibility-rgaa.md` — tableau des combinaisons validées (§6).
- `.claude/skills/ft2e-design-system/SKILL.md` — palette + rythme des sections.
- Mémoire `project-design-apple.md` — noter l'évolution marine + cuivre.

## 8. Hors périmètre (non-goals)

- Pas de refonte typographique (Inter Variable reste la police unique).
- Pas de changement des rayons, ombres, espacements, du conteneur `max-w-[980px]`.
- Pas de mode sombre `dark:` (le site alterne déjà les fonds).
- Pas de nouveaux composants ni de nouvelles pages.
- Pas de déblocage SEO / indexation (verrou démo inchangé).
- Les visuels de démo (photos IA marquées `DÉMO`) ne sont pas retouchés.

## 9. Critères d'acceptation

1. `npm run build` passe (échec = blocage).
2. `npm run lint` + `npm run typecheck` passent.
3. Aucune valeur chromatique codée en dur hors `@theme` (grep de contrôle sur `#000`,
   `#1d1d1f`, `#f5f5f7`, `rgba(0,0,0` dans `src/**` hors tokens légitimes comme les ombres).
4. Lighthouse Accessibilité **100/100** sur l'accueil et une page interne ; aucune
   régression de contraste vs. le tableau §6.
5. Le pictogramme et le wordmark s'affichent correctement sur nav (sombre) **et** en
   contexte clair (lockup `theme="light"`).
6. La nav glass se solidifie en marine au scroll sur le hero sombre, comme avant en noir.
7. Doc et mémoire (§7) reflètent la nouvelle palette.
8. `prefers-reduced-motion` toujours respecté (aucune animation ajoutée).

## 10. Référence visuelle

Page-témoin de la palette (Artifact, privé) :
`scratchpad/palette-ft2e.html` — swatches, migration token-par-token, composants réels
repeints (nav, hero, sections claires, cartes marine, CTA), rythme des sections.
