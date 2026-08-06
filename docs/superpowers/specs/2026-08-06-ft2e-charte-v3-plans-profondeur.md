# Charte v3 « Ingénierie de l'invisible » — plans et profondeur

**Référence** : « FT2E Charte graphique » document 10 · révision 2 (août 2026), bundle `branding-v3/` — remplace la révision 1 (charte v2 monochrome, `branding-v2/`). Ce document est la spec d'application de la révision 2 au site `ft2e-v3`.

## Ce qui ne change pas

- La rampe 197° : `profond #001718`, `encre #00393a`, `pivot #336667` (vert FT2E), `clair #99cccd`, `voile #e1f4f4`, `papier #f7f9fa`, `calcaire #edf0f2`. Aucun accent, aucune valeur hors rampe (chroma ≤ 0,055).
- Archivo Variable (wdth 62–125) + IBM Plex Mono. Fontsource, `font-display: swap`.
- Le duotone 197° des images (point noir profond, point blanc voile), les équerres, les annotations mono.
- Le filet de flux (`TraceFlux.astro`), 900 ms, une fois par chargement.
- Polarité claire par défaut ; réserve profonde comptée : une par écran, 1/5 de la surface max.
- Rayon 0 (une seule exception nouvelle : la puce de section, cercle de 7 px).
- Focus `2px solid pivot` décalé 2 px ; `prefers-reduced-motion` partout.

## Les quatre décisions de la révision 2

1. **Une seule teinte** (inchangé).
2. **Aucune couleur d'accent** (inchangé) : chaque valeur du système se lit.
3. **L'état par défaut est clair** (inchangé, précisé) : une réserve profonde par écran, une page encrée sur quarante.
4. **La profondeur remplace l'ornement** (NOUVEAU) : le relief vient des plans — une planche posée, une planche qui déborde, une ligne encrée. Trois rangs d'ombre, aucun autre effet.

## Ruptures v2 → v3 — table de traduction

| Sujet | v2 (révision 1) | v3 (révision 2) |
|---|---|---|
| Ombres | aucune, jamais | **3 rangs d'ombre à l'encre translucide** (voir § Plans) |
| Rang d'un filet | épaisseur 4/2/1 px, encre pleine | **1 px, opacité d'encre 22 % / 16 % / 12 %** |
| Bouton principal | filaire 2 px encre | **aplat encre**, filet clair 3 px à gauche, hover → profond 260 ms |
| Fond de page | papier nu | **papier tramé 28 px** (7 % d'encre), planche max 1440 px posée sur calcaire, ombre de page `0 0 90px` 18 % |
| h1 de page interne | vedette 125/700 capitales | **« Titre d'écran »** : wdth 100, 600, **casse normale, jamais capitales**, interligne 1,02 (`.type-ecran`) |
| Titre de section | `type-h2` 118/600 | **118/700**, précédé de la **puce profonde 7 px** ; mot porteur encre + **complément en clair précédé d'une barre oblique** |
| Corps | Archivo 400 (« plus de font-light ») | **Archivo 300** (trois graisses : 300/600/700) |
| Clair sur papier | interdit partout | **admis en filet, aplat et second mot des titres de section** (jamais en texte porteur : rapport 1,62) |
| Mouvement | un seul tracé (flux) | **4 mouvements** : flux 900 ms + **révélation de plan 760 ms / 22 px** (une fois, à l'entrée dans la vue) + survol cellule 300 ms + survol bouton 260 ms |
| Courbe | `cubic-bezier(0.16,1,0.3,1)` | **`cubic-bezier(0.2,0.7,0.2,1)`** |
| Module | 8 px | **28 px** (pas de trame) ; marge de page 60 px (44 px < 1200, 24 px à 390) ; 76 px entre sections ; gouttière 24 px |
| Rapports d'image | 3:2 et 16:9 | **21:8 (bandeau), 16:10 (appui de titre), 3:2 (fiche, index)** — aucun autre |
| Relevé chiffré | bg profond + voile | deux formes : **relevé clair** (un seul chiffre plein encre, les autres encre 13 %) et **ligne encrée** (rang 3) |
| Survol | filet épaissi d'un cran | **bascule de fond** (calcaire→papier, encre→profond) — aucun déplacement, le filet ne bouge pas |
| Mono | 400/500 | 400/**500/600** |

## Plans et profondeur (§ 09) — classes `global.css`

| Rang | Classe | Recette | Emploi |
|---|---|---|---|
| Planche de page | (BaseLayout) | papier max-w-1440 + `.trame-fond` + `shadow-[var(--shadow-page)]` sur body calcaire | la feuille du site |
| 1 — plan posé | `.plan-pose` | papier, bordure 1 px `filet-2` **obligatoire**, ombre `0 24 60` 12 % | planche principale d'un écran, carte de contenu |
| 2 — plan qui déborde | `.plan-deborde` | idem, ombre `0 32 70` 16 % ; chevauche le plan précédent de 40 px, se retire de 92 px sur un flanc | **une fois par écran au plus** |
| 3 — ligne encrée | `.plan-encre` | profond, **filet 3 px clair à gauche**, ombre `0 30 64` 30 %, pas de bordure | la réserve profonde de l'écran (relevés) |

L'ombre est toujours de l'encre translucide, jamais du noir. Aucun flou > 70 px (90 px réservé à la planche de page), aucun décalage horizontal, aucune ombre intérieure, aucune ombre sur un texte. La trame n'est jamais visible sous un plan (les plans ont un fond opaque).

**Révélation de plan** : poser `data-plan` sur les blocs `plan-pose` / `plan-deborde` / `plan-encre` significatifs (pas sur les cellules ni les cartes individuelles). `BaseLayout` observe et révèle une fois (760 ms, 22 px, courbe unique). Sans JS, tout est visible.

## Échelle de titrage (§ 06)

| Rang | Classe | Corps site | Chasse | Graisse | Casse |
|---|---|---|---|---|---|
| Vedette | `.type-display` | clamp(3rem, 7.5vw, 6.5rem), lh 0,92 | 125 | 700 | capitales — **accueil uniquement, une par page** |
| Titre d'écran | `.type-ecran` | clamp(2.25rem, 5vw, 3.875rem), lh 1,02 | 100 | 600 | **normale** — h1 des pages internes (`HeroPage`) |
| Section | `.type-section` (= `.type-h2`) | 22–26 px | 118 | 700 | capitales + puce + « /complément » clair |
| Intitulé | `.type-intitule` | 17–20 px | 112 | 600 | capitales |
| Corps | (défaut body) | 15–17 px, lh 1,6, 52–68 signes | 100 | **300** | — |
| Étiquette | `.mono-label` | 11/10 px, 0,14 em | mono | 500 | capitales |
| Relevé | `.releve-chiffre` | clamp(3.5rem, 7vw, 5.75rem), lh 1, ls −0,04 em | 118 | 700 | tabulaire |

## Titre de section — le motif

```astro
<div class="flex items-center gap-3">
  <span class="puce-section" aria-hidden="true"></span>
  <span class="mono-label text-pivot">01 — expertises</span>
</div>
<h2 class="type-section text-[26px] mt-4">
  <span class="text-encre">Six</span>
  <span class="text-clair">/expertises</span>
</h2>
```

Le mot porteur (encre) doit suffire au sens : le complément clair (1,62:1 sur papier) est **toujours redondant ou accessoire** — c'est la dérogation décorative documentée dans `accessibility-rgaa.md`.

## Composants (§ 10)

- **Bouton principal** `.btn-principal` (alias `.btn-blueprint-dark`) : aplat encre, texte papier mono 11/500, filet clair 3 px à gauche, padding 15/20, hover → profond 260 ms, flèche `→` admise. Le filet ne bouge pas.
- **Bouton filaire** `.btn-filaire` (alias `.btn-blueprint`) : 1 px à 28 % d'encre, texte pivot, hover → encre.
- **Étiquette de mission** `.etiquette-mission` : mono 10 px, 0,12 em, filet 1 px 28 %, **jamais d'aplat, six max par bloc**.
- **Chip de filtre** `.chip-blueprint` : actif = aplat encre/texte papier (`aria-pressed`).
- **Cellule de liste** `.cellule-liste` : calcaire, bordure 1 px `filet-1`, min-h 112 px, **numéro mono en tête, intitulé (112/600) en pied aligné à droite**, hover → papier 300 ms.
- **Cartouche** (`FicheTechnique`) : plan posé (bordure 1 px, ombre rang 1), en-tête calcaire, filets internes 1 px par rangs d'opacité, données mono. La barre de rang 4 px n'existe plus.
- **Relevé clair** (`ChiffresCles`) : colonnes séparées par filets 1 px `filet-2`, bord haut `filet-1` ; par colonne : commentaire (Archivo 300, 14 px, pivot, le commentaire **précède** le chiffre) → étiquette mono « — libellé » → chiffre `.releve-chiffre`. **Un seul chiffre en encre pleine par relevé** (celui que la page défend), les autres en `.releve-retrait` (encre 13 %).
- **Relevé encré** (fiche projet) : `.plan-encre`, chiffres `.releve-chiffre text-voile`, étiquettes `mono-label text-clair`. Jamais de vert FT2E en texte sur profond (3,67:1) — toléré en filet/aplat seulement.
- **Équerres** (`CoinsCuivre`) : 4 équerres 1 px au voile, **18 px de côté**, dans les angles. Repère de tirage, pas un encadrement.
- **Nomenclature** (`/references`) : liste tabulaire ; rang par **opacité du filet gauche 1 px** (livré 22 %, en cours 16 %, archive 12 %) et **graisse de l'intitulé** (700/600/300). Plus de 4/2/1 px.
- **Navigation** : barre claire fixe ; liens mono uppercase pivot → hover encre ; page courante = encre + filet bas 1 px encre plein.
- **Monogramme** (`Logo.astro`) : inchangé dans son dessin ; hauteur minimale 28 px à l'écran ; sous 180 px de place : forme `cadre`.

## Interdits (§ 15)

1. Aucune teinte hors axe 197°, y compris héritée (cuivre…).
2. Aucun dégradé coloré, aucune ombre teintée hors encre, aucune lueur.
3. Jamais de vert FT2E en **texte** sur réserve profonde (3,67:1).
4. Jamais de voile sur calcaire ni calcaire sur voile (iso-clairs).
5. Deux réserves profondes par écran, ou deux vedettes par page.
6. Aucun angle arrondi hors puce de section. Aucun cadre autour d'une image.
7. Le monogramme ne se déforme pas, ne reçoit ni ombre ni contour.
8. Le mono jamais en texte courant ; l'Archivo jamais en cote ni référence d'affaire.
9. Aucune photo en couleurs d'origine ; cadrages 21:8, 16:10, 3:2 seulement.
