# Charte v2 « Ingénierie de l'invisible » — monochrome 197° (application au site)

**Date** : 2026-08-06
**Source** : « FT2E Charte » v1.0, août 2026 — bundle `branding-v2/Ingénierie de l'invisible_v2.html` (design doc `FT2E Charte.dc.html`, claude.ai/design). Le document se déclare « document de référence · remplace toute version antérieure ».
**Remplace** : le système cuivre/marine du 2026-08-04 (`2026-08-04-ft2e-v2-ingenierie-invisible-design.md`, conservé pour l'historique).

## 1. Ce que la charte v2 change

La v2 conserve la philosophie (« un document d'ingénierie : cartouches, filets, annotations mono, chiffres tabulaires, duotone ») mais reconstruit la fondation :

| Axe | Système 2026-08-04 (cuivre) | Charte v2 (monochrome 197°) |
|---|---|---|
| Palette | encre `#08131f` + marine + **cuivre accent** | teinte unique 197° : `profond #001718`, `encre #00393a`, `pivot #336667`, `clair #99cccd`, `voile #e1f4f4` + neutres `papier #f7f9fa`, `calcaire #edf0f2` — **aucun accent** |
| Origine | palette composée | **2 valeurs fournies par FT2E** (`#336667`, `#99CCCD`, même teinte à 0,6° près) + 3 calculées (L 18,6 / 31,2 / 95,3) ; neutres non teintés |
| Polarité | nav/heros/footer/CTA sombres | **le papier gouverne** — réserve profonde ≤ 1/5, une apparition par écran, réservée aux relevés mesurés |
| Hiérarchie | la couleur signale (cuivre) | **valeur + épaisseur de trait (4/2/1 px) + largeur de caractère (wdth 125/118/112/100/72)** |
| Interaction | hover cuivre, lift 2 px | survol = filet épaissi d'un cran + intitulé à l'encre ; **aucun changement de teinte, aucun déplacement** ; focus 2 px pivot |
| Motion | reveals, compteurs, parallax | **un seul tracé animé, 900 ms, une fois par chargement** |
| Références | grille de cartes | **nomenclature** (rang du filet 4/2/1 = livré/en cours/archive) |
| Logo | pictogramme + wordmark texte | **monogramme complet** (cadre + flux débordant + lettres + baseline), 3 versions + forme réduite |

### Les cinq règles de couleur (planche 02)

1. Deux valeurs par composition, trois au maximum.
2. Jamais deux valeurs voisines en contact — sauter un palier (encre/pivot 1,97:1 interdit ; profond/pivot 2,85:1 interdit hors monogramme).
3. Aucune valeur intermédiaire, aucun dégradé, aucune opacité de teinte.
4. Réserve profonde comptée : 1/5 de surface max, une apparition par page.
5. Une alerte est un signe (filet doublé + mention), pas une couleur.

### Contrastes de référence (planche 02)

`encre/papier` 12,08 · `profond/papier` 17,51 · `pivot/papier` 6,14 · `pivot/calcaire` 5,67 · `voile/encre` 11,21 · `clair/profond` 10,45 · `clair/encre` 7,21. Tout est AA en petit corps sur son fond d'emploi.

### Rangs typographiques (planche 03)

Vedette 125/700 (une par page) · Titre 118/600 · Sous-titre 118/700 · Intitulé 112/600 · Courant 100/400 lh 1,6 · Annexe 72/600 · Étiquette mono 500, 11/10 px, 0,14 em. Tout nombre mesuré en mono tabulaire ; les vedettes chiffrées de blocs stats sont en Archivo 118/600 tabulaire (planche 08).

### Monogramme (planche 04)

Cadre ouvert sur ses flancs (angles vifs) traversé par un flux qui déborde de 6,5 unités (bouts ronds) — la distinction tient à la forme, pas à la valeur. 11 modules × 3, trait 7 unités. Versions : principal (flux profond, cadre+mot pivot), inversé (clair/voile sur réserve), valeur unique. Tailles minimales : 180 px écran, 42 mm impression ; sous 180 px le mot tombe (cadre seul, trait 9). Zone de protection : une hauteur de capitale. Baseline « BUREAU D'ÉTUDES TECHNIQUES » toujours en Plex Mono.

### Grille, filets, images, cartouche (planches 05–07)

- 12 colonnes, gouttière 24 px, marge 40 px, module 8 px. Zéro rayon, zéro ombre.
- Trois rangs de trait à valeur constante : ouvrage 4 px, section 2 px, indication 1 px.
- Images : duotone point noir `#001718` / point blanc `#E1F4F4`, gamma neutre ; 4 équerres 1 px / 18 px dans les angles ; 2 annotations max (verticale d'appui à 1/8) ; rapports 3:2 et 16:9 seulement.
- Cartouche (élément signature) : barre de rang 4 px + en-tête (domaine mono + intitulé vedette) + cases de données mono. Trois formats (plein / compact / vignette), même ordre : intitulé, référence, date. Calé à gauche, jamais d'ombre.

### Le site (planche 08)

- Écran 1 accueil : nav claire (monogramme + liens mono, actif souligné 2 px), hero clair 2 colonnes — l'image recule dans sa colonne, elle ne porte pas le titre ; vedette + barre 4 px + stats Archivo.
- Écran 2 index : nomenclature complète sans pagination — « un bureau d'études consulte une nomenclature, il ne parcourt pas un catalogue ».
- Écran 3 fiche : cartouche plein + mission (label mono à filet 2 px) + image 3:2 équerres 16 px + **bloc de relevés sur profond** (l'unique réserve de l'écran).
- Mouvement : un seul tracé (filet de flux reliant les sections), 900 ms, 1×/chargement. Survol : filet épaissi + intitulé à l'encre. Densité : la recherche filtre les lignes.

### Les huit interdits (planche 09)

1. Aucune couleur hors 197° + neutres. 2. Aucune valeur intermédiaire/dégradé/opacité de teinte. 3. Jamais deux valeurs voisines en contact. 4. Aucun rayon/ombre/**bouton plein sans nécessité**. 5. Aucun nombre mesuré en Archivo, aucune étiquette hors mono. 6. Aucune image en couleurs natives ni gris neutre. 7. Aucun icône illustratif/pictogramme/emoji. 8. Réserve ≤ 1/5, jamais le voile sur le calcaire.

### Ce que la charte ne tranche pas (décisions FT2E en attente)

1. **L'alerte** (filet doublé + mention — à valider sur cas réel). 2. **Le duotone sur lot réel** (passe de 30 vues à faire). 3. **La numérotation des affaires** (champ dédié à créer — en attendant, le site dérive `FT2E—{annee}`). 4. **La bascule des supports imprimés** (épuisement du stock).

## 2. Implémentation dans le site (2026-08-06)

- `src/styles/global.css` : @theme réécrit (7 tokens + `line`/`line-strong` en alpha d'encre 0,18/0,3 ; ~30 aliases legacy repointés), recettes retunées (`type-display` 125/700/0,96, `type-h2` → 118, nouveaux `type-intitule` et `type-annexe`, corps 400), boutons filaires à épaississement (`box-shadow inset`), duotone réel par sandwich `lighten`/`darken` isolé, focus/selection encre-pivot.
- `src/styles/motion.css` : réduit au tracé de flux + reduced-motion (~1 Ko). Script motion de `BaseLayout.astro` supprimé (hero reveal, scroll reveal, parallax) ; compteur de `Chiffre.astro` supprimé (valeur posée).
- `TraceFlux.astro` : suivi de scroll remplacé par un dessin unique 900 ms au `astro:page-load` (géométrie mesurée + nœuds conservés, recalage ResizeObserver silencieux).
- `Logo.astro` : monogramme complet de la charte (versions `principal`/`inverse`/`valeur-unique`, forme `cadre`, baseline optionnelle). `public/favicon.svg` : tuile profonde + cadre inversé, zéro rayon.
- Chrome : Header clair (monogramme, actif souligné 2 px encre), Footer calcaire à filet 2 px, skip-link encre.
- Heros : `HeroPage`/`Hero` clairs — vedette `text-profond`, barre de rang 4 px, sous-titre pivot ; hero accueil 2 colonnes avec média duotone annoté + cartouche compact du projet en avant.
- `/references` : nomenclature (en-tête 2 px, rang 4/2/1 px + wdth 118/100/72 par `statut` — nouveau champ Zod à défaut `livré`), filtres secteur en chips `aria-pressed`, compteur « N lignes sur T », pas d'animation de filtre.
- Fiche projet : cartouche (`FicheTechnique.astro` à barre de rang), mission à filet 2 px, image 3:2 équerres 16 px, **bloc relevés `bg-profond`** (si `performance`) — seule réserve de l'écran.
- `CarteProjet.astro` : format vignette (équerres 14 px + pied cartouche 4 px). `CoinsCuivre.astro` : équerres voile 1 px dans les angles (nom de fichier conservé, sémantique « équerres »).
- Toutes les pages recolorées (papier/calcaire, encre/pivot, plus aucune section sombre décorative — bandes « méthode » et « recrutement » passées au clair) ; hover lift supprimés ; `font-light` → 400.
- Règles mises à jour : `.claude/rules/tailwind-design-tokens.md` (réécrite), `.claude/rules/accessibility-rgaa.md` (table de contrastes), `.claude/skills/ft2e-design-system/SKILL.md`, `CLAUDE.md`.

**Hors périmètre v2 (à traiter)** : `SchemaTechnique.astro` (composant en réserve, non migré, non rendu), refonte éventuelle des images OG, passe duotone sur les photos réelles en phase de production.
