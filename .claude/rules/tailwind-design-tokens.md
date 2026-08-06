# Tailwind & Design Tokens — charte v2 « Ingénierie de l'invisible » (monochrome 197°)

**Scope** : tout fichier utilisant Tailwind (`.astro`, `.tsx`, `.html`).

**Référence** : « FT2E Charte » v1.0 (août 2026), bundle `branding-v2/` — remplace toute version antérieure (système cuivre/marine du 2026-08-04 inclus). Spec d'application : `docs/superpowers/specs/2026-08-06-ft2e-charte-v2-monochrome-197.md`.

## Principe directeur

**Une teinte unique (197°), cinq valeurs teintées, deux neutres, aucune couleur d'accent.** Un plan n'a pas de couleur d'appel : la hiérarchie passe par les trois moyens du dessin technique — la **valeur**, l'**épaisseur de trait** (4 / 2 / 1 px) et la **largeur de caractère** (Archivo wdth 125 / 118 / 112 / 100 / 72). Tout survit à la photocopie, au fax et au noir et blanc.

**Aucune valeur hard-codée** hors de `src/styles/global.css` (bloc `@theme` + `@layer components`). Pas de `tailwind.config.ts`.

## Couleurs — la rampe 197°

| Token | Hex | Nom charte | Usage exclusif |
|---|---|---|---|
| `profond` | `#001718` | Profond | **réserve — 1/5 max, une apparition par écran** : relevés chiffrés, duotone des images, couverture ; texte vedette sur papier (17,5:1) |
| `encre` | `#00393a` | Encre | toute la lecture : titres, filets porteurs, cadres, barres de rang |
| `pivot` | `#336667` | Vert FT2E (valeur client) | données, dates, mentions, corps de texte courant sur clair (6,1:1), filets de second rang, focus ring |
| `clair` | `#99cccd` | Clair (valeur client) | étiquettes et texte **sur fond profond/encre uniquement** (10,4:1 / 7,2:1) |
| `voile` | `#e1f4f4` | Voile | pôle clair du duotone ; titres, chiffres et équerres **sur réserve profonde uniquement** — jamais sur papier ni calcaire |
| `papier` | `#f7f9fa` | Papier (neutre) | **support par défaut** : fond de toute page |
| `calcaire` | `#edf0f2` | Calcaire (neutre) | surface secondaire : blocs de rappel, en-têtes de tableau, hover de surface — **jamais le voile sur le calcaire** (iso-clairs) |
| `line` | `rgba(0,57,58,.18)` | — | filet d'indication, séparateurs de lignes |
| `line-strong` | `rgba(0,57,58,.3)` | — | contour de cartouche, cadres |

### Les cinq règles de couleur

1. **Deux valeurs par composition, trois au maximum.**
2. **Jamais deux valeurs voisines en contact** — sauter un palier (encre sur pivot = 1,97:1, interdit ; profond sur pivot = 2,85:1, interdit hors monogramme).
3. **Aucune valeur intermédiaire, aucun dégradé, aucune opacité de teinte** (les filets `line`/`line-strong` en alpha d'encre sont le seul emploi d'alpha, hérité du vocabulaire de trait).
4. **La réserve profonde est comptée** : 1/5 de la surface max, une seule apparition par écran, réservée aux relevés mesurés (site).
5. **Une alerte est un signe, pas une couleur** : filet doublé + mention explicite. `--color-success`/`--color-error` sont repointés sur l'encre.

**Le cuivre n'existe plus.** `copper`, `bright-copper`, `copper-text` et tous les anciens tokens (`marine`, `slate`, `mist`, `cool-white`, `apple-blue`…) sont des **aliases repointés** sur la rampe 197° — valides au build, interdits dans le nouveau code.

## Typographie — rangs documentés

- **Archivo Variable** (axe `wdth` 62–125) : trois crans de largeur documentés, jamais d'interpolation libre.
- **IBM Plex Mono** (400/500) : tout ce qui est mesuré, référencé ou daté. **Aucun nombre de donnée en Archivo, aucune étiquette hors mono** (les vedettes chiffrées de bloc stats sont l'exception : Archivo 118/600 tabulaire, planche 08).

| Rang | Classe | Corps | wdth | Graisse | Emploi |
|---|---|---|---|---|---|
| Vedette | `type-display` | clamp ≤ 60 px | 125 | 700 | ouverture de page — **une seule par page**, `text-profond` |
| Titre | `type-h2` (+ base `h1–h6`) | 20–40 px | 118 | 600 | titre de section, intitulé de fiche |
| Intitulé | `type-intitule` | 15–19 px | 112 | 600 | nom d'affaire en nomenclature, en-tête de bloc, cartes |
| Courant | (défaut body) | 15–17 px | 100 | 400 | paragraphes, interligne 1,6 — **plus de `font-light`** |
| Annexe | `type-annexe` | 14 px | 72 | 600 | mention accessoire, troisième rang |
| Étiquette | `mono-label` | 11/10 px | mono | 500 | capitales, 0,14 em — jamais plus grand |
| Donnée | `mono-data` | 13 px | mono | 400 | chiffres tabulaires |

Autres recettes : `filet-top` (filet de section 2 px encre au-dessus d'un titre éditorial), `btn-blueprint` (filaire 1 px), `btn-blueprint-dark` (filaire fort 2 px encre — bouton principal), `btn-blueprint-solid` (filaire clair sur fond sombre), `chip-blueprint` (filtre, actif via `aria-pressed`), `duotone-media` (placeholder hachuré), `duotone-photo` (duotone réel #001718 → #E1F4F4 par sandwich lighten/darken).

## Vocabulaire de trait — trois rangs

| Rang | Épaisseur | Emploi |
|---|---|---|
| Ouvrage | **4 px** | entrée principale, affaire livrée, filet de tête de cartouche, barre de rang, CTA final |
| Section | **2 px** | sous-ensemble, en-tête de nomenclature, `filet-top`, phase en cours, nav active |
| Indication | **1 px** | séparateur, note, archive, équerre d'image |

Le rang est porté par l'épaisseur **seule**, à valeur constante (encre). Un filet ne change jamais de valeur pour signaler un rang.

## Éléments signature

- **Cartouche** (`FicheTechnique.astro`, vignettes `CarteProjet.astro`) : bloc-titre du plan — **barre de rang 4 px encre à gauche**, cases de données mono, ordre constant intitulé → référence → date. Calé à gauche, jamais centré, jamais d'ombre.
- **Nomenclature** (`/references`) : une liste tabulaire, pas une grille de cartes. Rang du filet gauche : 4 px livré · 2 px en cours · 1 px archive (champ `statut`), largeur d'Archivo assortie (118/100/72). Tout sur une page, la recherche filtre les lignes.
- **Monogramme** (`Logo.astro`) : cadre ouvert (angles vifs) + flux débordant (bouts ronds). 3 versions : `principal` (flux profond, cadre pivot — sur papier), `inverse` (clair/voile — sur profond), `valeur-unique`. Sous 180 px : `forme="cadre"`. Le débord ne se recadre jamais.
- **Équerres** (`CoinsCuivre.astro`) : 4 équerres 1 px au voile, 18/16/14 px, DANS les angles du média. Jamais de cadre fermé.
- **Images** : tout passe au duotone 197° (point noir `#001718`, point blanc `#E1F4F4`, gamma neutre). Jamais de couleurs natives, jamais de gris neutre, max 2 annotations/image (mono, verticale d'appui à 1/8 du cadre).

## Interactions & motion

- **Un seul tracé animé sur tout le site** : le filet de flux (`TraceFlux.astro`), 900 ms, une fois par chargement. **Aucun compteur qui s'incrémente, aucune apparition au défilement, aucun parallax.**
- **Survol** : épaissit le filet d'un cran (`box-shadow inset`) et passe l'intitulé à l'encre — aucun changement de teinte, **aucun déplacement** (pas de hover lift), aucune ombre. Surfaces : `hover:bg-calcaire` (neutre) admis.
- **Focus** : cadre `2px solid pivot`, décalé 2 px.
- **Boutons** : filaires mono uppercase — **aucun bouton plein sans nécessité**. Rayons : `rounded-none` (2 px max inputs). Ombres : aucune.
- Easing unique `--ease-blueprint` (`cubic-bezier(0.16,1,0.3,1)`), transitions d'état 200 ms, `prefers-reduced-motion` partout.

## Grille

- 12 colonnes, gouttière 24 px, marge 40 px ; conteneur `max-w-[1200px]`, prose `max-w-[840px]`.
- **Module 8 px** : hauteurs et espacements multiples de 8.
- Deux rapports d'image : **3:2** (fiche, index, vignette) et 16:9. Jamais un troisième.

## Patterns

```astro
<!-- ✅ Section claire, titre en baseline avec étiquette -->
<section class="bg-papier py-16">
  <div class="flex items-baseline gap-x-5">
    <h2 class="type-h2 text-encre text-[22px]">Six expertises</h2>
    <span class="mono-label font-normal text-pivot">de l'audit au DOE numérique</span>
  </div>
</section>

<!-- ✅ Cartouche à barre de rang -->
<div class="grid grid-cols-[4px_1fr] border border-line-strong">
  <div class="bg-encre" aria-hidden="true"></div>
  <div class="px-4 py-3">…</div>
</div>

<!-- ✅ Bloc de relevés — la seule réserve profonde de l'écran -->
<div class="bg-profond px-5 py-6">
  <p class="mono-label text-clair">performances mesurées</p>
  <p class="font-heading font-semibold text-voile tabular-nums" style="font-stretch:118%">0,18</p>
</div>

<!-- ❌ Interdits -->
<section class="bg-encre">…</section>            <!-- aplat sombre décoratif : le papier gouverne -->
<a class="text-copper">…</a>                     <!-- le cuivre n'existe plus -->
<div class="rounded-lg shadow-soft">…</div>       <!-- ni rayon ni ombre -->
<div class="motion-safe:hover:-translate-y-1">…</div> <!-- aucun déplacement au survol -->
<span class="text-voile">…</span>                 <!-- voile sur fond clair : réserve profonde uniquement -->
```

## Mode sombre

**Non applicable.** Le clair gouverne ; la réserve profonde est une exception comptée. Ne pas implémenter `dark:`.
