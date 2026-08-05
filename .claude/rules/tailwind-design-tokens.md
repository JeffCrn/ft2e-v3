# Tailwind & Design Tokens — « Ingénierie de l'invisible »

**Scope** : tout fichier utilisant Tailwind (`.astro`, `.tsx`, `.html`).

## Principe directeur

**Aucune valeur de couleur, espacement, typographie ou rayon hard-codée** en dehors de `src/styles/global.css` (bloc `@theme` + `@layer components`). Tout passe par les *tokens* et les *classes recettes*. La source de verite est `src/styles/global.css`, **pas** un `tailwind.config.ts`.

Le langage visuel est celui d'un **document d'ingenierie** : cartouches, filets 1 px, annotations mono, chiffres tabulaires, coins cuivre, medias duotone. Zero rayon (2 px max sur les inputs), zero ombre.

## Couleurs

| Token | Hex | Usage exclusif |
|---|---|---|
| `encre` (= `marine-deep`) | `#08131f` | fond nav, hero, footer, CTA final |
| `marine` | `#16324f` | titres sur clair, texte fort, encre secondaire |
| `marine-surface` / `-2` | `#0e2233` / `#123049` | surfaces sur fond encre |
| `cool-white` | `#edf0f2` | fond clair principal, texte sur encre |
| `paper` | `#f7f9fa` | surface claire secondaire, hover, encarts |
| `slate` | `#4a6076` | corps de texte sur clair |
| `mist` | `#8fa2b4` | labels mono, texte secondaire sur encre |
| `copper` | `#c46a38` | filets, bordures, numeros decoratifs, texte sur **encre** (4,9:1) |
| `bright-copper` | `#e08a50` | hover liens et annotations sur **encre** (7,1:1) |
| `copper-text` | `#a04e20` | petit texte cuivre sur fond **clair** (≥ 5:1) |
| `line` | `rgba(74,96,118,.35)` | filet standard (bordures, separateurs) |
| `line-strong` | `#4a6076` | filet fort (contour de cartouche) |

**Plus de bleu d'action.** Le cuivre porte l'identite **et** l'interaction : hover (`border-copper`, `text-bright-copper` sur encre, `text-copper-text` sur clair), focus ring `2px solid copper`. Les anciens tokens (`apple-blue`, `link-blue`, `bright-blue`, `near-black`, `light-gray`, `dark-surface-*`, `pure-black`…) sont des **aliases repointes** vers cette palette — valides mais a eviter dans le nouveau code.

**Regle cuivre / contraste** : `copper` sur fond clair = 3,4:1 → uniquement filets, bordures, gros glyphes. Tout **texte** cuivre sur fond clair utilise `copper-text`. Sur encre, `copper` et `bright-copper` sont surs.

## Typographie

- **Archivo Variable** (axes `wdth` 62–125 via `font-stretch`, `wght` 100–900) : titres condenses-larges **uppercase** et corps en 300.
- **IBM Plex Mono** (400/500) : labels, donnees, navigation, boutons, breadcrumbs.
- Chargement `@fontsource-variable/archivo/wdth.css` + `@fontsource/ibm-plex-mono`. `font-display: swap`. Pas de CDN Google (RGPD).

### Classes recettes (`@layer components` — les utilitaires les surchargent)

| Classe | Effet |
|---|---|
| `type-display` | Archivo stretch 125 %, 700, uppercase, ls −0.02em, lh 0.98 — heros |
| `type-h2` | stretch 112 %, 600, uppercase, lh 1.1 — titres de section/carte |
| `mono-label` | mono 11 px, 500, ls .14em, uppercase — labels techniques |
| `mono-data` | mono 13 px, tabular-nums — donnees |
| `filet-top` | filet cuivre 1 px au-dessus (titres editoriaux) |
| `btn-blueprint` | bouton filaire mono uppercase |
| `btn-blueprint-solid` | bouton plein clair (sur encre), hover fond cuivre |
| `btn-blueprint-dark` | bouton plein encre (sur clair), hover fond cuivre |
| `chip-blueprint` | chip filtre 1 px, mono uppercase |
| `duotone-media` | placeholder hachure encre + voile marine |
| `duotone-photo` | photo passee en duotone (grayscale + voile multiply) |
| `filet-trace` | variante animee de `filet-top` : le filet cuivre se dessine (scaleX) au reveal |

### Dispositifs de couleur structurante (2026-08-05)

La palette reste fermee a 8 valeurs (« aucune extension », planche systeme), mais trois usages prevus par la planche sont actives :

- **Trace de flux** (`TraceFlux.astro`, primitives) : polyligne cuivre verticale + nœuds carres 7 px, dessinee au defilement — la pointe du trait suit le bas du viewport, sans inertie (arbitrage 2026-08-05). Usage : colonne de marge de l'accueil. Decoratif, `aria-hidden`, ecrans ≥ 1360 px.
- **Schema technique annote** (`SchemaTechnique.astro`, blocs) : media duotone + polylignes cuivre + annotations mono `bright-copper` sequencees. **Retire du hero le 2026-08-05** (implantation jugee trop standardisee) — composant conserve en reserve, chantier de reprise en attente d'une solution plus impactante.
- **Cartouche sombre marine** : `bg-marine border-t border-copper` en bande intermediaire (ex. bandeau partenaires). Contrastes valides : `cool-white`/marine 11,4:1 ; `mist`/marine 4,6:1 (AA texte normal) ; accents en `bright-copper` uniquement.
- **Gros glyphes cuivre** : valeurs de cartouche en mono 32 px `text-copper` sur clair (texte large, 3,4:1 ≥ 3:1). Jamais en dessous de 24 px. Le cartouche garde son encadrement gris `border-line-strong` — pas de filet cuivre ni de nœuds sur ses lignes (arbitrage 2026-08-05).
- **Hover lift** : cartes autoportees `hover:border-copper` + `motion-safe:hover:-translate-y-[2px]` (etat « survol » de la planche). Pas de lift sur les cellules de grilles `gap-px`.

Les `h1`–`h6` recoivent par defaut (layer base) : Archivo stretch 112 %, 600, uppercase, ls −0.02em — **jamais de couleur en CSS global** (regle Tailwind v4 : les utilitaires doivent gagner).

## Vocabulaire graphique

- **Bordures 1 px partout** : `border-line` (standard), `border-line-strong` (cartouches), `border-copper` (accent, hover, top des sections encre).
- **Cartouches** : grilles bordees `border border-line-strong` + `gap-px bg-line` avec cellules `bg-cool-white` — l'anti-carte.
- **Coins cuivre** : composant `CoinsCuivre.astro` (equerres 16 px) sur les medias, parent `relative`.
- **Hover systemique** : `border-color → copper`, transition `400ms var(--ease-blueprint)` (`cubic-bezier(0.16, 1, 0.3, 1)`).
- **Rayons** : `rounded-none` par defaut ; `rounded-[2px]` uniquement inputs. Jamais `rounded-lg`, jamais pill `rounded-[980px]`.
- **Ombres** : aucune (`--shadow-soft` repointe sur `none`).

## Conteneur & espacements

- Conteneur principal : `max-w-[1200px] mx-auto px-4 md:px-6`.
- Prose editoriale : `max-w-[840px]`.
- Echelle Tailwind par defaut, multiples `1 2 3 4 6 8 12 16 24 32` (+ demi-crans `2.5/3.5` pour les cartouches denses).

## Patterns

```astro
<!-- ✅ Section encre avec filet cuivre -->
<section class="bg-encre border-t border-copper text-cool-white">…</section>

<!-- ✅ Titre de section + label mono en baseline -->
<div class="flex items-baseline gap-x-5">
  <h2 class="type-h2 text-marine text-[22px]">Six expertises</h2>
  <span class="mono-label font-normal text-mist">de l'audit au DOE numérique</span>
</div>

<!-- ✅ Carte blueprint (bordure, pas d'ombre) -->
<a class="block border border-line bg-paper hover:border-copper transition-colors duration-[400ms] ease-[var(--ease-blueprint)]">…</a>

<!-- ✅ Media duotone avec coins cuivre -->
<div class="relative">
  <div class="aspect-[3/2] duotone-media">…</div>
  <CoinsCuivre />
</div>

<!-- ❌ Ancien langage Apple -->
<a class="bg-apple-blue rounded-[980px]">…</a>
<div class="rounded-lg shadow-soft">…</div>
<a class="text-copper">lien sur fond clair</a> <!-- contraste 3,4:1 : utiliser copper-text -->
```

## Mode sombre

**Non applicable.** Le rythme visuel vient de l'alternance encre / blanc froid. Ne pas implementer `dark:`.
