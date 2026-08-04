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

### Contraste — palette « ingénierie de l'invisible » (encre + cuivre)

Texte normal / fond : ratio **≥ 4.5:1**. Texte large (≥ 18 pt ou 14 pt gras) : ratio **≥ 3:1**. Éléments d'interface : ratio **≥ 3:1**.

Depuis 2026-08-04, la fondation chromatique est le système blueprint « ingénierie de l'invisible » : encre `#08131f`, marine `#16324f`, blanc froid `#edf0f2`, cuivre `#c46a38`. Voir `docs/superpowers/specs/2026-08-04-ft2e-v2-ingenierie-invisible-design.md`.

Combinaisons validées du design system :

| Texte | Fond | Ratio | Statut |
|---|---|---|---|
| `cool-white` `#edf0f2` | `encre` `#08131f` | 16.3:1 | OK — texte sur nav/hero/footer |
| `mist` `#8fa2b4` | `encre` `#08131f` | 7.1:1 | OK — labels et texte secondaire sur encre |
| `bright-copper` `#e08a50` | `encre` `#08131f` | 7.1:1 | OK — hover liens, annotations |
| `copper` `#c46a38` | `encre` `#08131f` | 4.9:1 | OK — eyebrows, labels cuivre sur encre |
| `marine` `#16324f` | `cool-white` `#edf0f2` | 11.4:1 | OK — titres, texte fort |
| `marine` `#16324f` | `paper` `#f7f9fa` | 12.4:1 | OK — données de cartouche |
| `slate` `#4a6076` | `cool-white` `#edf0f2` | 5.7:1 | OK — corps de texte |
| `slate` `#4a6076` | `paper` `#f7f9fa` | 6.2:1 | OK |
| `mist` `#8fa2b4` | `cool-white` `#edf0f2` | 2.3:1 | ⚠️ Jamais en texte porteur sur clair — labels `mist` uniquement sur encre ; sur clair, utiliser `slate` |
| `copper-text` `#a04e20` | `cool-white` `#edf0f2` | 5.1:1 | OK — petit texte cuivre sur clair |
| `copper-text` `#a04e20` | `paper` `#f7f9fa` | 5.5:1 | OK |
| `copper` `#c46a38` | `cool-white` `#edf0f2` | 3.4:1 | Filets, bordures, gros glyphes, UI (≥ 3:1) uniquement — **jamais du petit texte** |

**Règle cuivre (point tranché)** : le cuivre standard `#c46a38` est sûr sur encre (4,9:1) mais pas en petit texte sur fond clair (3,4:1). Sur fond clair, tout texte cuivre (numéros porteurs de sens, labels, notes `[démo]`, hover de lien) utilise **`copper-text` `#a04e20`** ; `copper` y reste réservé aux filets, bordures, équerres et gros glyphes du logo (un logotype est par ailleurs exempté du critère 1.4.3).

**Règles spécifiques au design blueprint** :
- `slate` porte le corps de texte sur fond clair ; `mist` porte les labels et le texte secondaire **sur encre uniquement**. Les labels `mono-label` sur fond clair porteurs d'information passent en `slate` ou `mist`→`slate`.
- Plus de bleu d'action : le cuivre signale l'interaction (hover de bordure, focus ring). L'affordance des liens repose sur le **soulignement** (liens éditoriaux) ou la **casse mono uppercase** (liens de navigation) — jamais sur la couleur seule (critère 3.2 distinction des liens).
- Distinction titre ↔ lien : les titres sont uppercase condensés `marine`, jamais soulignés ; les liens éditoriaux sont soulignés en `marine` avec hover `copper-text`.
- `pure-black` et les tokens bleus (`apple-blue`, `link-blue`, `bright-blue`) sont **legacy** : aliases repointés vers la palette cuivre/marine, à ne plus utiliser.

### Navigation clavier

- **Tous les éléments interactifs** atteignables au `Tab` dans un ordre logique.
- **`:focus-visible`** : `outline: 2px solid #c46a38` (cuivre), offset 2px.
- **Lien d'évitement** (« Aller au contenu principal ») premier focus de chaque page.
- Pas de *focus trap* sauf modale légitime (et avec sortie `Esc`).
- La navigation fixe encre (56 px mobile / 74 px desktop) ne doit pas masquer le contenu focusé — le spacer `h-14 md:h-[74px]` compense.

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
