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

### Contraste — charte v2 « ingénierie de l'invisible » (monochrome 197°)

Texte normal / fond : ratio **≥ 4.5:1**. Texte large (≥ 18 pt ou 14 pt gras) : ratio **≥ 3:1**. Éléments d'interface : ratio **≥ 3:1**.

Depuis 2026-08-06, la fondation chromatique est la charte v2 monochrome (« FT2E Charte », bundle `branding-v2/`) : une teinte unique 197°, cinq valeurs teintées (`profond #001718`, `encre #00393a`, `pivot #336667`, `clair #99cccd`, `voile #e1f4f4`) et deux neutres (`papier #f7f9fa`, `calcaire #edf0f2`). **Aucun accent : chaque valeur du système est lisible en petit corps sur son fond d'emploi.**

Combinaisons validées (ratios mesurés de la charte) :

| Avant-plan | Fond | Ratio | Emploi |
|---|---|---|---|
| `encre` `#00393a` | `papier` `#f7f9fa` | 12.08:1 | texte courant et titres — paire de référence |
| `profond` `#001718` | `papier` `#f7f9fa` | 17.51:1 | vedette, cartouche de tête |
| `pivot` `#336667` | `papier` `#f7f9fa` | 6.14:1 | données, dates, corps secondaire |
| `pivot` `#336667` | `calcaire` `#edf0f2` | 5.67:1 | mêmes emplois sur surface secondaire |
| `voile` `#e1f4f4` | `encre` `#00393a` | 11.21:1 | chiffres et titres dans un bloc de relevés |
| `clair` `#99cccd` | `profond` `#001718` | 10.45:1 | texte et filets sur réserve profonde |
| `clair` `#99cccd` | `encre` `#00393a` | 7.21:1 | étiquettes sur aplat encre |
| `encre` `#00393a` | `pivot` `#336667` | 1.97:1 | ⛔ deux valeurs voisines en contact — interdit |
| `profond` `#001718` | `pivot` `#336667` | 2.85:1 | ⛔ interdit hors monogramme |

**Règles spécifiques à la charte v2** :
- Jamais deux valeurs voisines de la rampe en contact : toujours sauter un palier.
- `clair` et `voile` ne se posent **que sur fonds sombres** (`encre`, `profond`) ; sur clair, le texte est `encre` ou `pivot`.
- Le focus ring est `2px solid pivot` (6,1:1 sur papier, ≥ 3:1 UI). L'interaction est signalée par l'épaisseur de filet et la bascule de valeur — jamais par une teinte.
- L'affordance des liens repose sur le **soulignement** (liens éditoriaux, encre → hover pivot) ou la **casse mono uppercase** (navigation) — jamais sur la couleur seule (critère 3.2).
- Distinction titre ↔ lien : titres uppercase condensés jamais soulignés ; liens éditoriaux soulignés.
- Une alerte est **un signe, pas une couleur** : filet doublé + mention explicite (le système n'a pas de rouge).
- Tous les anciens tokens (cuivre, marine, slate, mist, bleus) sont des aliases repointés — à ne plus utiliser.

### Navigation clavier

- **Tous les éléments interactifs** atteignables au `Tab` dans un ordre logique.
- **`:focus-visible`** : `outline: 2px solid #336667` (pivot), offset 2px.
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
- Inputs sur fond `calcaire` avec bordure `line` : le focus ring pivot (2 px) assure la visibilité.
- Captcha non visuel à éviter ; préférer un *honeypot* transparent.

### Mouvement

- Aucune animation > 5 s en boucle sans contrôle utilisateur.
- Respecter `prefers-reduced-motion: reduce` pour toute transition ou animation.
- Un seul élément animé sur le site (tracé de flux, 900 ms, une fois par chargement) — décoratif, `aria-hidden`.

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
