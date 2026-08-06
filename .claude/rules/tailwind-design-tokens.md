# Tailwind & Design Tokens — charte v3 « Ingénierie de l'invisible » (plans et profondeur)

**Scope** : tout fichier utilisant Tailwind (`.astro`, `.tsx`, `.html`).

**Référence** : « FT2E Charte graphique » document 10 · révision 2 (août 2026), bundle `branding-v3/` — remplace la révision 1 (charte v2 monochrome, `branding-v2/`). Spec d'application : `docs/superpowers/specs/2026-08-06-ft2e-charte-v3-plans-profondeur.md`.

## Principe directeur

**Une teinte unique (197°), cinq valeurs teintées, deux neutres, aucune couleur d'accent — et la profondeur remplace l'ornement.** Le relief vient des plans : une planche posée, une planche qui déborde, une ligne encrée — trois rangs d'ombre à l'encre translucide, aucun autre effet. Le rang d'un filet est porté par son **opacité d'encre** (22 / 16 / 12 %), plus jamais par son épaisseur ; la hiérarchie typographique passe par la **graisse** (Archivo 300 / 600 / 700) et la **chasse** (wdth 62–125).

**Aucune valeur hard-codée** hors de `src/styles/global.css` (bloc `@theme` + `@layer components`). Pas de `tailwind.config.ts`.

## Couleurs — la rampe 197° (inchangée depuis la révision 1)

| Token | Hex | Nom charte | Usage exclusif |
|---|---|---|---|
| `profond` | `#001718` | Profond | **réserve — 1/5 max, une apparition par écran** : ligne encrée (relevés), duotone des images, couverture, puce de section ; texte vedette sur papier (17,5:1) |
| `encre` | `#00393a` | Encre | toute la lecture : titres, corps, aplat du bouton principal, chip actif — et l'encre translucide des filets et des ombres |
| `pivot` | `#336667` | Vert FT2E (valeur client) | données, dates, mentions, corps secondaire sur clair (6,1:1), focus ring — **jamais en texte sur profond** (3,67:1, toléré en filet/aplat seulement) |
| `clair` | `#99cccd` | Clair (valeur client) | texte sur fond profond/encre (10,4:1 / 7,2:1) ; **sur papier : filets, aplats et complément des titres de section uniquement** (1,62:1 — décor, jamais porteur de sens) |
| `voile` | `#e1f4f4` | Voile | pôle clair du duotone ; titres, chiffres et équerres **sur réserve profonde uniquement** — jamais sur papier ni calcaire |
| `papier` | `#f7f9fa` | Papier (neutre) | la planche de page (max 1440 px) et les plans posés ; fond des cellules au survol |
| `calcaire` | `#edf0f2` | Calcaire (neutre) | le fond sous la planche de page ; cellules de liste au repos, blocs de rappel, en-têtes de tableau — **jamais le voile sur le calcaire** (iso-clairs) |

### Filets — trois rangs portés par l'opacité (1 px)

| Token | Valeur | Emploi |
|---|---|---|
| `filet-1` | `rgba(0,57,58,.22)` | rang 1 : porteur, contour appuyé, bordure de cellule, statut livré |
| `filet-2` | `rgba(0,57,58,.16)` | rang 2 : bordure de plan, séparateur de colonnes, statut en cours |
| `filet-3` | `rgba(0,57,58,.12)` | rang 3 : indication, note, statut archive |
| `filet-chip` | `rgba(0,57,58,.28)` | étiquette de mission, chip de filtre, bouton filaire |

**L'épaisseur ne porte plus le rang : tous les filets font 1 px.** Trois exceptions dessinées, à valeur pleine : le filet clair 3 px du bouton principal et de la ligne encrée, et le filet bas 1 px encre plein de la page courante en navigation. `line`/`line-strong` sont des aliases repointés (16 / 22 %) — valides au build, interdits dans le nouveau code.

### Les cinq règles

1. **Une seule teinte** : aucune valeur hors rampe 197° (chroma ≤ 0,055), y compris héritée — le cuivre n'existe plus, tous les anciens tokens (`copper`, `marine`, `slate`, `mist`, `apple-blue`…) sont des aliases repointés, interdits dans le nouveau code.
2. **Aucune couleur d'accent** : chaque valeur du système se lit ; deux valeurs par composition, trois au maximum.
3. **L'état par défaut est clair** : une seule réserve profonde par écran (`bg-profond` / `.plan-encre`), 1/5 de la surface max — une page encrée sur quarante.
4. **La profondeur remplace l'ornement** : trois rangs d'ombre à l'encre translucide (`--shadow-plan-1/2/3`) plus l'ombre de page (`--shadow-page`) — aucun autre effet, aucun dégradé coloré, aucune lueur, aucune ombre teintée hors encre.
5. **Une alerte est un signe, pas une couleur** : filet doublé + mention explicite (`--color-success`/`--color-error` repointés sur l'encre).

Garde-fous de contraste : jamais de vert FT2E en texte sur profond ; jamais de voile sur calcaire ni de calcaire sur voile ; le clair sur papier n'est jamais porteur de sens.

## Échelle de titrage — sept rangs

| Rang | Classe | Corps | wdth | Graisse | Casse — emploi |
|---|---|---|---|---|---|
| Vedette | `.type-display` | clamp(3rem, 7.5vw, 6.5rem), lh 0,92 | 125 | 700 | capitales — **accueil uniquement, une par page** |
| Titre d'écran | `.type-ecran` | clamp(2.25rem, 5vw, 3.875rem), lh 1,02 | 100 | 600 | **casse normale, jamais capitales** — h1 des pages internes (`HeroPage`) |
| Section | `.type-section` (= `.type-h2`) | 22–26 px | 118 | 700 | capitales — puce 7 px + mot porteur encre + « /complément » clair |
| Intitulé | `.type-intitule` | 17–20 px | 112 | 600 | capitales — carte, cellule, ligne de tableau |
| Corps | (défaut body) | 15–17 px, lh 1,6, 52–68 signes | 100 | **300** | paragraphes — trois graisses Archivo seulement : 300/600/700 |
| Étiquette | `.mono-label` | 11/10 px, 0,14 em | mono | 500 | capitales — jamais plus grand, jamais en texte courant |
| Relevé | `.releve-chiffre` | clamp(3.5rem, 7vw, 5.75rem), lh 1, ls −0,04 em | 118 | 700 | chiffres tabulaires |

- **IBM Plex Mono** (400/**500/600**) : tout ce qui est mesuré, référencé ou daté — `.mono-data` 13 px tabulaire pour les données. Le mono jamais en texte courant ; l'Archivo jamais en cote ni référence d'affaire.
- `.type-annexe` (72/600) est un legacy v2 conservé pour l'existant : la v3 hiérarchise par la graisse et l'opacité, plus par la chasse réduite.

## Plans et profondeur — trois rangs d'ombre

| Rang | Classe | Recette | Emploi |
|---|---|---|---|
| Planche de page | (`BaseLayout`) | papier `max-w-[1440px]` + `.trame-fond` + `shadow-[var(--shadow-page)]` (`0 0 90px` encre 18 %) sur body calcaire | la feuille du site |
| 1 — plan posé | `.plan-pose` | papier, **bordure 1 px `filet-2` obligatoire**, ombre `0 24px 60px` encre 12 % | planche principale d'un écran, carte de contenu |
| 2 — plan qui déborde | `.plan-deborde` | idem, ombre `0 32px 70px` encre 16 % ; chevauche le plan précédent de 40 px, se retire de 92 px sur un flanc | **une fois par écran au plus** |
| 3 — ligne encrée | `.plan-encre` | profond, **filet 3 px clair à gauche**, ombre `0 30px 64px` encre 30 %, pas de bordure | la réserve profonde de l'écran (relevés) |

L'ombre est toujours de l'encre translucide, **jamais du noir**. Aucun flou > 70 px (90 px réservé à la planche de page), aucun décalage horizontal, aucune ombre intérieure, aucune ombre sur un texte. La trame n'est jamais visible sous un plan (les plans ont un fond opaque).

**Révélation de plan** : poser `data-plan` sur les blocs `plan-pose` / `plan-deborde` / `plan-encre` significatifs (pas sur les cellules ni les cartes individuelles). `BaseLayout` observe et révèle une fois (760 ms, 22 px, courbe unique). Sans JS, tout est visible d'emblée.

## Trame et marges

- **Trame de fond** `.trame-fond` : pas de 28 px à 7 % d'encre — elle porte le fond de page, jamais visible sous un plan.
- **Module 28 px** (le pas de la trame) ; marge de page **60 px** (44 px sous 1200 px, 24 px à 390 px) ; **76 px entre sections** ; gouttière **24 px**.
- Planche de page `max-w-[1440px]` sur calcaire ; conteneur de contenu `max-w-[1200px]` ; prose éditoriale `max-w-[840px]`.
- **Rayon 0 partout** — seule exception : la puce de section (cercle 7 px, `.puce-section`).
- Rapports d'image : **21:8** (bandeau), **16:10** (appui de titre), **3:2** (fiche, index) — aucun autre.

## Composants signature

- **Bouton principal** `.btn-principal` (alias `.btn-blueprint-dark`) : **aplat encre**, texte papier mono 11/500, **filet clair 3 px à gauche**, padding 15/20, hover → profond 260 ms, flèche `→` admise. **Le filet ne bouge pas.**
- **Bouton filaire** `.btn-filaire` (alias `.btn-blueprint`) : 1 px à 28 % d'encre, texte pivot, hover → encre. Sur réserve profonde : `.btn-blueprint-solid` (filaire clair — le vert FT2E est interdit en texte sur profond).
- **Étiquette de mission** `.etiquette-mission` : mono 10 px, 0,12 em, filet 1 px 28 %, **jamais d'aplat, six max par bloc**. **Chip de filtre** `.chip-blueprint` : même dessin ; actif = aplat encre / texte papier (`aria-pressed`).
- **Cellule de liste** `.cellule-liste` : calcaire, bordure 1 px `filet-1`, min-h 112 px, **numéro mono en tête, intitulé (112/600) en pied aligné à droite**, hover → papier 300 ms.
- **Titre de section** : puce profonde 7 px + numéro `mono-label` pivot, puis `type-section` — mot porteur encre + complément clair précédé d'une barre oblique. Le mot porteur doit suffire au sens (le complément clair est toujours redondant ou accessoire — dérogation décorative documentée dans `accessibility-rgaa.md`).
- **Cartouche** (`FicheTechnique.astro`) : plan posé (bordure 1 px, ombre rang 1), en-tête calcaire, filets internes 1 px par rangs d'opacité, données mono. **La barre de rang 4 px n'existe plus.** Calé à gauche, jamais centré.
- **Nomenclature** (`/references`) : liste tabulaire, pas une grille de cartes. Rang par **opacité du filet gauche 1 px** (livré 22 % · en cours 16 % · archive 12 %) et **graisse de l'intitulé** (700/600/300). Plus de 4/2/1 px. Tout sur une page, la recherche filtre les lignes.
- **Relevé clair** (`ChiffresCles`) : colonnes séparées par filets 1 px `filet-2`, bord haut `filet-1` ; par colonne : commentaire (Archivo 300, 14 px, pivot — **le commentaire précède le chiffre**) → étiquette mono « — libellé » → chiffre `.releve-chiffre`. **Un seul chiffre en encre pleine par relevé** (celui que la page défend), les autres en `.releve-retrait` (encre 13 %).
- **Relevé encré** (fiche projet) : `.plan-encre`, chiffres `.releve-chiffre text-voile`, étiquettes `mono-label text-clair` — la réserve profonde de l'écran.
- **Monogramme** (`Logo.astro`) : dessin inchangé (cadre ouvert + flux débordant) ; **hauteur minimale 28 px** à l'écran ; sous 180 px de place : `forme="cadre"`. Ne se déforme pas, ne reçoit ni ombre ni contour ; le débord ne se recadre jamais.
- **Équerres** (`CoinsCuivre.astro`) : 4 équerres 1 px au voile, **18 px de côté**, dans les angles du média. Repère de tirage, pas un encadrement — jamais de cadre autour d'une image.
- **Images** : tout passe au duotone 197° (point noir `#001718`, point blanc `#E1F4F4`, gamma neutre) via `duotone-photo` / `duotone-media` (hachure placeholder). Jamais de couleurs natives, max 2 annotations mono par image.

## Interactions & motion

- **Quatre mouvements, une seule courbe** `--ease-blueprint` = `cubic-bezier(0.2, 0.7, 0.2, 1)` — remplace `cubic-bezier(0.16, 1, 0.3, 1)` :
  1. filet de flux (`TraceFlux.astro`), 900 ms, une fois par chargement — le seul tracé animé ;
  2. révélation de plan (`[data-plan]`), 760 ms, 22 px, une fois à l'entrée dans la vue ;
  3. survol de cellule, 300 ms, calcaire → papier ;
  4. survol de bouton, 260 ms, encre → profond.
- **Survol = bascule de fond** — aucun déplacement, aucun filet qui s'épaissit (**plus de `box-shadow` inset**), aucune ombre qui apparaît. Le filet ne bouge pas.
- **Focus** : cadre `2px solid pivot`, décalé 2 px.
- Aucun compteur qui s'incrémente, aucun parallax, aucun hover lift ; `prefers-reduced-motion` partout (tout est posé d'emblée).

## Patterns

```astro
<!-- ✅ Titre de section : puce + numéro mono, mot porteur encre + complément clair -->
<div class="flex items-center gap-3">
  <span class="puce-section" aria-hidden="true"></span>
  <span class="mono-label text-pivot">01 — expertises</span>
</div>
<h2 class="type-section text-[26px] mt-4">
  <span class="text-encre">Six</span>
  <span class="text-clair">/expertises</span>
</h2>

<!-- ✅ Plan posé, révélé une fois à l'entrée dans la vue -->
<section class="plan-pose p-7" data-plan>…</section>

<!-- ✅ Relevé clair : le commentaire précède le chiffre, un seul plein -->
<div class="border-t border-filet-1 grid md:grid-cols-3">
  <div class="px-6 py-5 border-l border-filet-2 first:border-l-0">
    <p class="text-[14px] text-pivot">Un bureau né en 2008, toujours à La Rochelle.</p>
    <p class="mono-label text-pivot mt-3">— années d'exercice</p>
    <p class="releve-chiffre text-encre mt-2">17</p>       <!-- le chiffre que la page défend -->
  </div>
  <div class="px-6 py-5 border-l border-filet-2">
    …
    <p class="releve-chiffre releve-retrait mt-2">7</p>    <!-- les autres, en retrait (encre 13 %) -->
  </div>
</div>

<!-- ✅ Ligne encrée — la réserve profonde de l'écran -->
<div class="plan-encre px-6 py-7">
  <p class="mono-label text-clair">performances mesurées</p>
  <p class="releve-chiffre text-voile mt-2">0,18</p>
</div>

<!-- ❌ Interdits -->
<div class="shadow-lg">…</div>                        <!-- ombre hors des trois rangs (+ planche de page) -->
<div class="rounded-lg">…</div>                       <!-- rayon 0 partout, sauf .puce-section -->
<div class="border-l-4 border-encre">…</div>          <!-- le rang ne passe plus par l'épaisseur -->
<p class="text-clair">Texte porteur sur papier</p>    <!-- clair jamais porteur sur fond clair (1,62:1) -->
<div class="bg-profond"><p class="text-pivot">…</p></div> <!-- vert FT2E interdit en texte sur profond -->
<section class="bg-profond">…</section> <!-- ×2 sur un même écran : une seule réserve profonde -->
<div style="transition: all 300ms cubic-bezier(0.16, 1, 0.3, 1)">…</div> <!-- ancienne courbe v2 -->
<a class="hover:shadow-[inset_0_0_0_1px_#00393a] hover:-translate-y-1">…</a> <!-- ni inset ni déplacement au survol -->
```

## Mode sombre

**Non applicable.** Le clair gouverne ; la réserve profonde est une exception comptée. Ne pas implémenter `dark:`.
