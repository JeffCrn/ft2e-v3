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

Depuis 2026-08-08, la fondation chromatique est la charte v3 « plans et profondeur » **révision 2.1** (« FT2E Charte graphique » document 10, bundle `branding-v3-bis/`) : une teinte unique 197°, cinq valeurs teintées (`profond #001718`, `encre #00393a`, `pivot #336667`, `clair #99cccd`, `voile #e1f4f4`) et deux neutres (`papier #f7f9fa`, `calcaire #edf0f2`). **Aucun accent : chaque valeur du système est lisible en petit corps sur son fond d'emploi** — le fond d'emploi du `clair` en texte est la réserve profonde, jamais le papier.

Combinaisons validées (ratios mesurés de la charte) :

**Valeurs recalculées par la révision 2.1** (08.2026) — sur une rampe monochrome l'œil surestime les écarts, toutes les paires ont été remesurées. Les chiffres ci-dessous remplacent ceux de la révision 2.

| Avant-plan | Fond | Ratio | Emploi |
|---|---|---|---|
| `encre` `#00393a` | `papier` `#f7f9fa` | 12,08:1 | texte courant et titres — paire de référence (le bouton principal, papier sur encre, partage ce rapport) |
| `profond` `#001718` | `papier` `#f7f9fa` | 17,51:1 | vedette d'accueil, puce de section (aplat) |
| `encre` `#00393a` | `calcaire` `#edf0f2` | 11,14:1 | texte sur surface secondaire : bloc de rappel, en-tête de tableau, champ de formulaire |
| `pivot` `#336667` | `papier` `#f7f9fa` | 6,14:1 | données, dates, chapô, chiffres de relevé en retrait, anneau de focus clair |
| `pivot` `#336667` | `calcaire` `#edf0f2` | 5,67:1 | mêmes emplois sur surface secondaire (cellules de liste) |
| `papier` `#f7f9fa` | `profond` `#001718` | 17,51:1 | réserve pleine : panneau, couverture |
| `voile` `#e1f4f4` | `profond` `#001718` | 16,24:1 | chiffres et titres sur la ligne encrée (`.plan-encre`), légende en cartouche de réserve |
| `clair` `#99cccd` | `profond` `#001718` | 10,45:1 | corps, étiquettes mono et **anneau de focus** sur réserve profonde |
| `pivot` `#336667` | `profond` `#001718` | **2,85:1** | ⛔ **interdit en texte ET en filet porteur** (amendement A3 — la révision 2 annonçait 3,67, la mesure donne 2,85, sous le seuil de 3,0). Toléré en aplat décoratif seulement |
| `clair` `#99cccd` | `papier` `#f7f9fa` | 1,67:1 | ⛔ **jamais porteur de sens** — filet, aplat et complément décoratif de titre, **obligatoirement `aria-hidden`** (A2) |
| `voile` `#e1f4f4` | `calcaire` `#edf0f2` | 1,01:1 | ⛔ **interdit sans exception** — les deux valeurs sont iso-claires |

**La règle des 4,5** : un rapport inférieur à 4,5 disqualifie l'emploi en texte **quelle que soit la taille**. Le système n'use pas de la tolérance à 3,0 des grands corps — c'est plus strict que le RGAA, et c'est voulu.
**La règle des 3,0** : un filet ou un indicateur de focus qui porte une information doit atteindre 3,0. C'est ce qui exclut le pivot sur réserve profonde.

**Dérogation documentée — complément clair des titres de section (amendement A2)** : le motif `<span class="text-encre">Mot</span><span class="text-clair" aria-hidden="true">/complément</span>` est admis parce que le mot porteur en encre **suffit au sens**. La révision 2.1 rend le marquage **`aria-hidden="true"` obligatoire** : le complément (1,67:1) est purement décoratif et ne doit porter aucune information qui ne soit redonnée ailleurs. Un complément clair sans `aria-hidden` est un bug. Toute autre utilisation du `clair` en texte sur fond clair est un bug.

**Règles spécifiques à la charte v3** :
- La hiérarchie passe par la **valeur**, la **graisse** (Archivo **300/400/600/700** — le corps est en 400 depuis l'amendement A7, la 300 est réservée au chapô) et les **plans** (trois rangs d'ombre) — plus jamais par l'épaisseur de filet : tous les filets font 1 px, leur rang est porté par l'opacité d'encre (22 % / 16 % / 12 %), toujours doublée d'un autre signe, jamais seule porteuse d'information. Sur l'index des références, le statut est ainsi dit **trois** fois — le mot au pied de la carte, la graisse de l'intitulé (700/600/300), l'opacité du filet gauche — et c'est le **mot** qui porte : mesuré au rendu, 22 % contre 16 % d'encre sur un filet de 1 px ne se départagent pas à l'œil d'une carte à l'autre (amendement A9).
- Les **ombres** (`--shadow-plan-1/2/3`, `--shadow-page`) sont de l'encre translucide posée sous des plans à fond opaque : elles n'ont **aucune incidence de contraste** — jamais d'ombre sur un texte. La trame de fond (28 px, 7 % d'encre) est trop ténue pour affecter les ratios mesurés sur papier.
- `clair` et `voile` en **texte** ne se posent que sur la réserve profonde ; sur clair, le texte est `encre` ou `pivot`. Jamais de voile sur calcaire ni calcaire sur voile (iso-clairs).
- **Focus par polarité (amendement A4)** : `2px solid pivot` décalé 2 px sur fond clair (6,14) ; `2px solid clair` sur réserve profonde (10,45) — le pivot y est invisible (2,85). Implémenté dans `global.css` par `.plan-encre :focus-visible`, `.bg-profond :focus-visible`, `.polarite-profonde :focus-visible`. L'anneau ne prend jamais de rayon et **ne remplace pas** l'état de survol ; `outline: none` sans substitut est un défaut bloquant. Le survol reste une **bascule de fond** — jamais une teinte nouvelle, jamais un déplacement.
- **Liens en paragraphe (amendement A6)** : `encre` + soulignement **1 px à 3 px sous la ligne de base**, porté à **2 px au survol**. **Aucun changement de couleur** — la recette est `.lien-texte`. La navigation garde son affordance de casse mono capitale. Jamais la couleur seule (critère 3.2).
- **États de formulaire (amendement A5)** — le système n'a ni rouge ni vert, un état se dit par trois signes redondants :

| État | Filet du champ | Marque | Message |
|---|---|---|---|
| Repos | 1 px · encre 16 % | — | — |
| Actif | 1 px · encre 22 % | — | libellé en pivot |
| Erreur | **2 px · encre 100 %** | **▲** à gauche | sous le champ, mono 11 px en encre, préfixé « Erreur — », `role="alert"` posé **à l'apparition seulement** |
| Succès | 1 px · encre 22 % | aucune | **bandeau séparé** en calcaire à filet clair 3 px, hors du champ (`role="status"`) |
| Désactivé | 1 px · encre 12 % | — | texte pivot, fond calcaire, curseur interdit |

  L'erreur se signale par l'**épaisseur**, une **marque** et un **mot** ; le succès par un **déplacement**. Recettes : `.champ`, `.message-erreur`, `.bandeau-succes`.
- **Cible tactile** : 44 × 44 px au minimum pour tout élément actionnable, y compris lorsque son tracé visible est plus petit (recette `.cible-44`, marge transparente).
- Distinction titre ↔ lien : titres jamais soulignés ; liens éditoriaux soulignés.
- Une alerte est **un signe, pas une couleur** : filet doublé + mention explicite (le système n'a pas de rouge) — inchangé depuis la révision 1.
- **Hygiène du dépôt (§ 17)** : aucun alias hérité n'est conservé. Les jetons `cuivre`, `marine`, `slate`, `mist`, `line`/`line-strong` ont été **supprimés** de `global.css` — un jeton nommé d'après une identité antérieure se supprime, il ne se redirige pas. Aucune valeur hexadécimale ne s'écrit en dur dans un composant.

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
