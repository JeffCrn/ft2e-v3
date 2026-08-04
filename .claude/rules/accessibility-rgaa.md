# Accessibilité RGAA AA

**Scope** : tout le site. Pas de dérogation.

## Référentiel

- **RGAA 4.1** (Référentiel Général d'Amélioration de l'Accessibilité), niveau **AA**.
- Équivalent international : **WCAG 2.1 AA**.

## Règles non négociables

### Sémantique HTML

- **Un seul `<h1>` par page**, qui décrit son sujet principal.
- Hiérarchie des `<h2>`/`<h3>` **sans saut de niveau** (pas de `<h3>` sans `<h2>` parent).
- `<main>`, `<header>`, `<footer>`, `<nav>`, `<article>`, `<aside>` utilisés à bon escient. Pas de `<div>` quand un élément sémantique existe.
- `<button>` pour une action, `<a>` pour une navigation. **Jamais l'inverse.**
- Liens externes : `target="_blank"` accompagné de `rel="noopener noreferrer"` et d'un texte indiquant l'ouverture nouvelle (ou icône avec `aria-label`).

### Contraste — palette marine + cuivre

Texte normal / fond : ratio **≥ 4.5:1**. Texte large (≥ 18 pt ou 14 pt gras) : ratio **≥ 3:1**. Éléments d'interface : ratio **≥ 3:1**.

Depuis le 2026-07-03, la fondation chromatique du design system est passée du noir pur au bleu marine du logo (`marine-deep` / `marine`) et du gris clair au blanc froid (`cool-white`). Voir `docs/superpowers/specs/2026-07-03-evolution-palette-logo-design.md` § 6 pour le détail des calculs.

Combinaisons validées du design system :

| Texte | Fond | Ratio | Statut |
|---|---|---|---|
| `marine` `#16324f` | Blanc `#FFFFFF` | 13.1:1 | OK — titres |
| `marine` `#16324f` | `cool-white` `#edf1f5` | 11.5:1 | OK — titres |
| `cool-white` `#edf1f5` | `marine` `#16324f` | 11.5:1 | OK |
| `cool-white` `#edf1f5` | `marine-deep` `#0f2436` | 13.9:1 | OK |
| Blanc `#FFFFFF` | `marine-deep` `#0f2436` | 15.8:1 | OK — body sombre |
| Blanc `#FFFFFF` | `marine-surface` `#1d3a57` | 11.7:1 | OK — cartes |
| `near-black` `#1d1d1f` | Blanc `#FFFFFF` | 16.5:1 | OK — body |
| `slate` `#45535f` | Blanc `#FFFFFF` | 7.9:1 | OK |
| `slate` `#45535f` | `cool-white` `#edf1f5` | 7.0:1 | OK |
| `mist` `#9fb0bf` | `marine` `#16324f` | 5.9:1 | OK |
| `bright-copper` `#d98a55` | `marine-deep` `#0f2436` | 5.8:1 | OK — accent d'identité (eyebrow, « 2 ») |
| `bright-copper` `#d98a55` | `marine` `#16324f` | 4.8:1 | OK — eyebrow (petit texte) |
| `copper` `#c46a38` | Blanc `#FFFFFF` | 3.8:1 | Gros glyphe de marque uniquement (logo) — jamais texte/lien |
| `apple-blue` `#0071e3` | Blanc `#FFFFFF` | 4.6:1 | OK |
| `link-blue` `#0066cc` | Blanc `#FFFFFF` | 5.3:1 | OK — liens clairs |
| `bright-blue` `#2997ff` | `marine-deep` `#0f2436` | 5.25:1 | OK — liens sombres |
| `bright-blue` `#2997ff` | `marine` `#16324f` | 4.34:1 | ⚠️ Texte large / UI uniquement |

**Règle `bright-blue` sur fond sombre (point tranché)** : `bright-blue` passe AA sur `marine-deep` (5,25:1) mais tombe à 4,34:1 sur le `marine` moyen. Les **liens texte sur fond sombre vivent sur `marine-deep`** (hero, CTA final). Sur une section `marine` moyen (ex. Secteurs), l'interactivité passe par un **CTA plein** (remplissage `apple-blue`, texte blanc) ou un lien en gros caractères (≥ 18 pt / 14 pt gras, seuil 3:1) — jamais un lien texte en petits caractères.

**Règles spécifiques au design Apple-style** :
- `slate` (texte secondaire sur fond clair) et `mist` (texte secondaire sur fond marine) remplacent respectivement `text-tertiary` et `white/70` pour le texte secondaire informatif ; `text-tertiary` (`rgba(0,0,0,0.48)`) reste réservé aux légendes, captions et texte non essentiel.
- Distinction titre marine ↔ lien bleu : les titres passent en `marine`, proche des bleus d'action. La distinction repose sur le **poids** (titres 600, larges, jamais soulignés) et l'**affordance de lien** (soulignement au hover, flux de texte). Aucun titre ne prend une couleur de lien ; aucun lien ne prend `marine`.
- L'accent d'action Apple Blue `#0071e3` garantit que les éléments interactifs sont identifiables.
- L'accent d'identité cuivre (`copper` / `bright-copper`) est réservé à la marque (logo, chiffre « 2 », eyebrow, filet) et ne signale jamais une action. `bright-copper` sur `marine-deep` (5,8:1) et sur `marine` (4,8:1) est sûr ; `copper` sur blanc (3,8:1) est réservé aux gros glyphes du logo — jamais du texte courant ni un lien. Un logotype reste par ailleurs exempté du critère 1.4.3.
- `pure-black` `#000000` est **legacy** : conservé comme alias, il n'est plus utilisé pour les surfaces du site.

### Navigation clavier

- **Tous les éléments interactifs** atteignables au `Tab` dans un ordre logique.
- **`:focus-visible`** : `outline: 2px solid #0071e3` (Apple Blue), offset 2px.
- **Lien d'évitement** (« Aller au contenu principal ») premier focus de chaque page.
- Pas de *focus trap* sauf modale légitime (et avec sortie `Esc`).
- La navigation glass (`position: fixed`, 48px) ne doit pas masquer le contenu focusé — le spacer `h-12` compense.

### Images

- `alt=""` pour images décoratives, sinon **alt descriptif**.
- Pas d'image porteuse de texte essentiel.
- SVG décoratif : `aria-hidden="true"` + `focusable="false"`.

### Formulaires (page Contact)

- Chaque `<input>` a un `<label>` associé (jamais en `placeholder` seul).
- Erreurs annoncées via `aria-describedby` + `role="alert"`.
- Champs requis marqués visuellement **et** via `aria-required="true"`.
- Inputs sur fond `light-gray` sans bordure : le focus ring Apple Blue assure la visibilité.
- Captcha non visuel à éviter ; préférer un *honeypot* transparent.

### Mouvement

- Aucune animation > 5 s en boucle sans contrôle utilisateur.
- Respecter `prefers-reduced-motion: reduce` pour toute transition ou animation.
- `backdrop-blur` de la navigation glass est purement décoratif.

### Lecteur d'écran

- Tester avec **NVDA** (Windows) et **VoiceOver** (macOS/iOS) au moins une fois par page avant livraison.

## Tests à exécuter

```bash
npx lighthouse https://localhost:4321 --only-categories=accessibility --quiet
npx axe http://localhost:4321
```

Cible Lighthouse Accessibility : **100/100**. Toute régression < 100 = blocage.

## Page de mention

Le site inclut une **page « Accessibilité »** (`/accessibilite`) déclarant le niveau de conformité, les éventuelles dérogations, et la date du dernier audit.
