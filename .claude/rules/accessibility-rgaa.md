# Accessibilité RGAA AA

**Scope** : tout le site. Une seule dérogation documentée : le complément clair des titres de section (§ Contraste).

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

### Contraste — charte v3 « plans et profondeur » (monochrome 197°)

Texte normal / fond : ratio **≥ 4,5:1**. Texte large (≥ 18 pt ou 14 pt gras) : ratio **≥ 3:1**. Éléments d'interface : ratio **≥ 3:1**.

Depuis 2026-08-06, la fondation chromatique est la charte v3 « plans et profondeur » (« FT2E Charte graphique » document 10 · révision 2, bundle `branding-v3/`) : une teinte unique 197°, cinq valeurs teintées (`profond #001718`, `encre #00393a`, `pivot #336667`, `clair #99cccd`, `voile #e1f4f4`) et deux neutres (`papier #f7f9fa`, `calcaire #edf0f2`). **Aucun accent : chaque valeur du système est lisible en petit corps sur son fond d'emploi** — le fond d'emploi du `clair` en texte est la réserve profonde, jamais le papier.

Combinaisons validées (ratios mesurés de la charte) :

| Avant-plan | Fond | Ratio | Emploi |
|---|---|---|---|
| `encre` `#00393a` | `papier` `#f7f9fa` | 12,08:1 | texte courant et titres — paire de référence (le bouton principal, papier sur encre, partage ce rapport) |
| `profond` `#001718` | `papier` `#f7f9fa` | 17,51:1 | vedette d'accueil, puce de section (aplat) |
| `pivot` `#336667` | `papier` `#f7f9fa` | 6,14:1 | données, dates, corps secondaire, commentaires de relevé |
| `pivot` `#336667` | `calcaire` `#edf0f2` | 5,67:1 | mêmes emplois sur surface secondaire (cellules de liste) |
| `voile` `#e1f4f4` | `profond` `#001718` | 16,04:1 | chiffres et titres sur la ligne encrée (`.plan-encre`) |
| `clair` `#99cccd` | `profond` `#001718` | 10,55:1 | étiquettes mono sur réserve profonde |
| `pivot` `#336667` | `profond` `#001718` | 3,67:1 | ⛔ **interdit en texte** — toléré en filet ou aplat seulement |
| `clair` `#99cccd` | `papier` `#f7f9fa` | 1,62:1 | ⛔ **jamais porteur de sens** — admis uniquement en filet, aplat et complément décoratif des titres de section |

**Dérogation documentée — complément clair des titres de section** : le motif `<span class="text-encre">Mot</span><span class="text-clair">/complément</span>` est admis parce que le mot porteur en encre **suffit au sens** ; le complément clair (1,62:1) est toujours redondant ou accessoire, jamais une information exclusive. Toute autre utilisation du `clair` en texte sur fond clair est un bug.

**Règles spécifiques à la charte v3** :
- La hiérarchie passe par la **valeur**, la **graisse** (Archivo 300/600/700) et les **plans** (trois rangs d'ombre) — plus jamais par l'épaisseur de filet : tous les filets font 1 px, leur rang est porté par l'opacité d'encre (22 % / 16 % / 12 %), toujours doublée d'un autre signe (graisse de l'intitulé en nomenclature, champ `statut`), jamais seule porteuse d'information.
- Les **ombres** (`--shadow-plan-1/2/3`, `--shadow-page`) sont de l'encre translucide posée sous des plans à fond opaque : elles n'ont **aucune incidence de contraste** — jamais d'ombre sur un texte. La trame de fond (28 px, 7 % d'encre) est trop ténue pour affecter les ratios mesurés sur papier.
- `clair` et `voile` en **texte** ne se posent que sur la réserve profonde ; sur clair, le texte est `encre` ou `pivot`. Jamais de voile sur calcaire ni calcaire sur voile (iso-clairs).
- Le focus ring est `2px solid pivot` (6,1:1 sur papier, ≥ 3:1 UI). Le survol est une **bascule de fond** (calcaire → papier, encre → profond) — jamais une teinte nouvelle, jamais un déplacement.
- L'affordance des liens repose sur le **soulignement** (liens éditoriaux, encre → hover pivot) ou la **casse mono uppercase** (navigation) — jamais sur la couleur seule (critère 3.2).
- Distinction titre ↔ lien : titres jamais soulignés ; liens éditoriaux soulignés.
- Une alerte est **un signe, pas une couleur** : filet doublé + mention explicite (le système n'a pas de rouge) — inchangé depuis la révision 1.
- Tous les anciens tokens (cuivre, marine, slate, mist, bleus, `line`/`line-strong`) sont des aliases repointés — à ne plus utiliser.

### Navigation clavier

- **Tous les éléments interactifs** atteignables au `Tab` dans un ordre logique.
- **`:focus-visible`** : `outline: 2px solid #336667` (pivot), offset 2px.
- **Lien d'évitement** (« Aller au contenu principal ») premier focus de chaque page.
- Pas de *focus trap* sauf modale légitime (et avec sortie `Esc`).
- La navigation fixe claire (`papier`, 56 px mobile / 74 px desktop) ne doit pas masquer le contenu focusé — le spacer `h-14 md:h-[74px]` compense.

### Images

- `alt=""` pour images décoratives, sinon **alt descriptif**.
- Pas d'image porteuse de texte essentiel.
- SVG décoratif : `aria-hidden="true"` + `focusable="false"`.

### Formulaires (page Contact)

- Chaque `<input>` a un `<label>` associé (jamais en `placeholder` seul).
- Erreurs annoncées via `aria-describedby` + `role="alert"`.
- Champs requis marqués visuellement **et** via `aria-required="true"`.
- Inputs sur fond `calcaire` avec bordure 1 px (`filet-1`) : le focus ring pivot (2 px) assure la visibilité.
- Captcha non visuel à éviter ; préférer un *honeypot* transparent.

### Mouvement

- Aucune animation > 5 s en boucle sans contrôle utilisateur.
- **Quatre mouvements v3, une seule courbe** (`cubic-bezier(0.2, 0.7, 0.2, 1)`) :
  1. tracé de flux (`TraceFlux.astro`) — 900 ms, une fois par chargement, décoratif, `aria-hidden` ;
  2. révélation de plan (`[data-plan]`, initiée par `BaseLayout.astro`) — 760 ms / 22 px, une fois par élément, à l'entrée dans la vue ;
  3. survol de cellule — 300 ms, bascule calcaire → papier ;
  4. survol de bouton — 260 ms, bascule encre → profond.
- `prefers-reduced-motion: reduce` **supprime les quatre** : tout est posé d'emblée (`motion.css` + garde dans `initPlans`). Sans JavaScript, rien n'est masqué (classe `html.js-plans`).
- Rien d'autre ne bouge : ni compteur, ni parallax, ni déplacement au survol.

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
