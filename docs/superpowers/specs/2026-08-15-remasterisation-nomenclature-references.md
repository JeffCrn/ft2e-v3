# Remasterisation de `/references` — de la nomenclature tabulaire à la grille de cartes

*Rédigé le 2026-08-15, à l'issue de l'agrandissement de la vignette de nomenclature, qui a
révélé que la ligne de tableau n'était pas le bon contenant. Le § « Prompt de lancement »
se colle tel quel en session neuve : rien d'autre n'y est supposé connu.*

---

## Pourquoi ce chantier

La page `/references` sert 23 fiches en **liste tabulaire** : une ligne par affaire, quatre
colonnes (vignette · titre · secteur · statut). Trois évolutions successives l'ont conduite
à une impasse mesurable.

1. **Les planches** (chantier clos le 2026-08-15) ont donné à chaque fiche une **vignette
   dessinée**, composée dans un repère de 300 × 200 pour être lue entre 274 et 296 px.
   Dans la colonne de tête de 56 px de la nomenclature, elle tombait à l'échelle 0,18 : son
   mono de 9 px se rendait à 1,6 px. Le dessin n'y était qu'une texture.
2. **Le titre court** (2026-08-15) a libéré de la largeur : le titre le plus long ne réclame
   plus que 381 px là où la colonne en offrait 703.
3. **L'agrandissement de la vignette** (2026-08-15) a converti cette largeur en dessin —
   220 px à xl — mais une vignette 3:2 convertit toute largeur gagnée en **hauteur** : la
   ligne passe à 176 px, la liste de 1 528 à 4 040 px, et le titre flotte seul dans une
   colonne de 539 px dont il n'occupe que 381 au pire cas. **Beaucoup de blanc vide, pour
   une vignette qui n'atteint toujours pas sa taille de conception.**

Le constat qui referme le raisonnement : **la grille de cartes fait mieux sur les deux axes
à la fois.**

| | Nomenclature agrandie (xl) | Grille 4 colonnes |
|---|---|---|
| Vignette servie | 220 px — échelle 0,73, mono à 6,6 px | **274 px — échelle 0,91, mono à 8,2 px** |
| Rapport à la taille de conception | sous-échelle | **taille de conception exacte** |
| Hauteur pour 23 fiches | 4 040 px | **1 958 px** |
| Cohérence avec le reste du site | format propre à cette page | **le même bloc que l'accueil, les secteurs, les expertises** |

Mesures relevées au navigateur le 2026-08-15, pas estimées.

---

## La décision préalable : c'est une dérogation à la charte, et elle doit être assumée

**La charte prescrit littéralement l'inverse de ce chantier.**
`.claude/rules/tailwind-design-tokens.md`, § Composants signature, révision 2.1 :

> **Nomenclature** (`/references`) : liste tabulaire, **pas une grille de cartes**. Rang par
> **opacité du filet gauche 1 px** (livré 22 % · en cours 16 % · archive 12 %) et **graisse
> de l'intitulé** (700/600/300). Plus de 4/2/1 px. Tout sur une page, la recherche filtre
> les lignes.

`CLAUDE.md` reprend la même phrase. **La première tâche de la session n'est donc pas du
code : c'est de trancher, avec FT2E, entre deux voies.**

- **Amender la charte** — la prescription date d'avant les planches, à une époque où la
  vignette était un extrait de plan illisible qu'il valait mieux réduire à une pastille.
  L'argument qui la fondait a disparu avec son objet.
- **Documenter une dérogation** — la charte reste, la page s'en écarte, et l'écart est
  consigné au même endroit que la dérogation du complément clair des titres de section
  (`.claude/rules/accessibility-rgaa.md`).

**Ne pas commencer le code avant que ce point soit tranché**, et ne pas le trancher seul :
c'est une décision de marque, pas d'implémentation.

---

## Ce que la mesure impose, et qui ne se discute pas

**Quatre colonnes à xl. Ni trois, ni cinq.** Le conteneur utile fait 1 152 px (`max-w-[1200px]`
moins `px-6`), la gouttière 16 px :

| Colonnes | Carte | Échelle de la vignette | Verdict |
|---|---|---|---|
| 2 | 568 px | 1,89 | filets de 1 px épaissis de 89 % |
| 3 | 373 px | 1,24 | filets épaissis de 24 % |
| **4** | **276 px** | **0,91** | **taille de conception (274–296)** |
| 5 | 218 px | 0,72 | mono retombé à 6,5 px |

La sur-échelle n'est pas un détail cosmétique : c'est le défaut que le protocole des
planches a documenté pour l'appui du hero — « la vignette grossie à 1,84 épaissit tous les
filets de 1 px ». Un dessin composé pour une taille ne se transpose ni au-dessus ni en
dessous ; c'est la règle fondatrice de tout le dispositif visuel du site.

Échelle responsive attendue, à confirmer au rendu :
`grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4` — c'est celle des grilles
existantes, à ceci près qu'elles s'arrêtent à `lg:grid-cols-4`. **Vérifier au navigateur ce
que `lg` (conteneur 976) donne à 4 colonnes : 232 px, soit l'échelle 0,77 — sous la taille
de conception.** D'où la proposition de 3 colonnes à `lg` (312 px, échelle 1,04) et 4 à
`xl`. À mesurer, pas à supposer.

---

## Ce qui doit survivre au changement de contenant

C'est la partie du travail qu'un simple « remplacer la liste par une grille » ferait perdre
en silence.

### 1. Le rang — deux signes, pas un

La nomenclature encode `statut` **deux fois**, et le doublon est ce qui la rend conforme :
un signe graphique porteur ne doit jamais reposer sur la seule couleur (RGAA 3.2, et règle
du protocole des planches).

```ts
const rangs = {
  livré:      { filet: 'border-l-filet-1', graisse: 'font-bold',     statut: 'livré' },
  'en cours': { filet: 'border-l-filet-2', graisse: 'font-semibold', statut: 'en cours' },
  archive:    { filet: 'border-l-filet-3', graisse: 'font-light',    statut: 'archive' },
} as const;
```

`CarteProjet.astro` **ne porte ni l'un ni l'autre** aujourd'hui. Trois questions à trancher
au rendu :

- le filet gauche d'opacité se transpose-t-il au bord d'une carte, ou faut-il un autre
  porteur (bord haut ? bord du pied calcaire) ?
- la graisse de l'intitulé (700/600/300) reste-t-elle lisible en carte, où le titre est en
  `type-intitule` capitales à 15 px ?
- **le statut en toutes lettres** doit-il monter dans le pied de carte ? Il y est déjà, par
  `libelleChronologie()` : « livraison 2026 » ou « en cours ». Vérifier que ça suffit —
  auquel cas le rang graphique devient une redondance de confort, pas le porteur unique.

### 2. Les filtres et le compteur

`initFiltres()` (dans le `<script>` de la page) opère sur trois crochets :
`[data-grille]` (le conteneur), `[data-secteur]` (sur chaque `<li>`), `[data-compteur]`.
Il masque par `style.display` et recompose « N lignes sur N ».

- La grille doit **garder ces trois crochets** — le script fonctionne tel quel sur des
  éléments de grille, à condition que `[data-secteur]` reste sur l'élément que la grille
  positionne (le `<li>`, pas le `<a>` intérieur).
- **Le libellé du compteur doit changer** : « lignes » n'a plus de sens. « 23 fiches sur 23 ».
- Le guard `dataset.filtresBound` et l'écoute `astro:page-load` sont **obligatoires**
  (`.claude/rules/astro-conventions.md` § Scripts client & View Transitions) : ne pas les
  perdre dans la réécriture.

### 3. Le titre court

`titreCourt()` (`src/lib/projets.ts`) lit le `titre` du `planche.json` — c'est déjà ce que
`CarteProjet` affiche. Rien à faire, sinon ne pas régresser vers `projet.data.titre`, qui
est la forme longue réservée au `<h1>` de la fiche et au référencement.

### 4. La sémantique et l'ordre

`<ul role="list">` + `<li>` + un `<a>` par fiche : la grille garde cette structure, seule la
mise en page change. L'ordre reste `parAffaireDecroissante`.

### 5. « Tout sur une page »

La charte l'exige et la grille le sert mieux (1 958 px contre 4 040). **Ne pas introduire de
pagination**, ni de « voir plus ».

---

## Ce qui disparaît

- Les quatre colonnes, l'en-tête `vue · affaire · secteur · statut`, et le `lg:truncate`.
- La bascule à deux colonnes du palier md, posée le 2026-08-15 pour sauver les titres :
  elle devient sans objet.
- La ligne de légende du bas, « rang : opacité du filet — livré 22 % · en cours 16 % ·
  archive 12 % », **si et seulement si** le rang graphique disparaît. S'il survit sous une
  autre forme, la légende doit dire la nouvelle.

---

## Pièges déjà payés, à ne pas repayer

1. **Tailwind v4 lit le `.gitignore`.** Toute classe en valeur arbitraire doit être
   vérifiée dans le CSS produit, sélecteur par sélecteur — et Tailwind **échappe** les
   crochets et les deux-points : chercher `.lg\:grid-cols-4` et non `lg:grid-cols-4`.
   Le build reste vert quand une classe manque. (`.claude/rules/astro-conventions.md`)
2. **Un bloc `data-plan` est invisible tant qu'il n'est pas entré dans la vue.** Une capture
   prise sans avoir fait défiler la page montre un cadre vide et fait croire à une casse.
   Faire défiler, attendre ~800 ms, puis capturer.
3. **Chrome sous Windows refuse une fenêtre sous 500 px** : le contrôle « largeur
   téléphone » se fait par une **iframe de 390 px** dans une fenêtre de 500, jamais par la
   taille de fenêtre.
4. **Mesurer le texte au `Range`, pas au `scrollWidth`** : sur un bloc qui ne déborde pas,
   `scrollWidth` vaut la boîte et ne dit rien du texte.
5. **`CarteProjet` est utilisé par cinq pages** (accueil, secteurs, expertises,
   `ProjetsSimilaires`, et bientôt `/references`). Toute modification y est globale : si le
   rang doit s'y ajouter, le faire par **prop optionnelle**, pas par changement de défaut —
   sinon un signal de statut apparaît sur des pages qui n'en veulent pas.

---

## Critères de réception — mesurés, pas affirmés

À vérifier au navigateur, à **1440, 1280, 1024, 800 et 390 px** :

- [ ] la vignette est servie entre **274 et 296 px** au palier le plus large ; à aucun
      palier elle ne dépasse 296 (sur-échelle) ni ne descend sous 218 (mono < 6,5 px) ;
- [ ] la hauteur totale de la grille pour 23 fiches est **inférieure à 2 200 px** à xl ;
- [ ] aucun titre tronqué à aucun palier ;
- [ ] aucun débordement horizontal à 390 px ;
- [ ] les filtres masquent et démasquent, et le compteur suit, **après une navigation
      View Transitions** (aller sur `/references`, partir, revenir, refiltrer) ;
- [ ] le statut de chaque fiche reste lisible **sans recourir à la couleur seule** ;
- [ ] `npm run typecheck` et `npm run build` verts, et les classes de grille en valeur
      arbitraire présentes dans `dist/_astro/*.css` ;
- [ ] `.claude/rules/tailwind-design-tokens.md` et `CLAUDE.md` **mis à jour dans le même
      commit** — la prescription « pas une grille de cartes » ne peut pas survivre au
      chantier qui la contredit.

---

## Ce qu'on ne touche pas

- Le `<h1>` de la fiche, la balise `<title>`, la description et le JSON-LD : ils portent le
  **titre long**, c'est la forme que le référencement indexe.
- Les cinq pièces d'une planche et le composant `PlancheReference` : la vignette est un
  fichier composé, elle ne se recadre ni ne se redimensionne à la main.
- Les autres grilles du site : elles marchent, et ce chantier vient s'aligner sur elles,
  pas l'inverse.

---

## Prompt de lancement d'une session neuve

À coller tel quel.

```text
Tu remasterises la page /references du site FT2E : la nomenclature tabulaire
devient une grille de cartes, au format déjà employé partout ailleurs sur le
site (accueil, secteurs, expertises, projets similaires).

AVANT TOUTE AUTRE CHOSE, cloner le dépôt et lire la spécification. Elle fait
autorité sur tout ce qui suit, y compris sur ce message :

    git clone --depth 1 https://github.com/JeffCrn/ft2e-v3
    docs/superpowers/specs/2026-08-15-remasterisation-nomenclature-references.md

CE QUI MOTIVE LE CHANTIER, en une phrase : la grille sert la vignette à sa
taille de conception (274 px, mono à 8,2) sur MOITIÉ MOINS de hauteur que la
nomenclature agrandie (1 958 px contre 4 040) — un gain sur les deux axes, pas
un compromis. Les chiffres sont relevés au navigateur, ils sont dans la spec.

COMMENCE PAR LA DÉCISION DE CHARTE, PAS PAR LE CODE. La charte prescrit
littéralement « Nomenclature (/references) : liste tabulaire, PAS une grille de
cartes ». Amender ou déroger est une décision de marque : pose-la-moi avant
d'écrire une ligne, avec ton avis motivé.

CE QUI DOIT SURVIVRE — la spec le détaille, ne le redécouvre pas :
  · le RANG (statut) est encodé DEUX fois, filet d'opacité + graisse : un signe
    graphique porteur ne repose jamais sur la couleur seule ;
  · les filtres par secteur et le compteur, avec leurs crochets data-* et leur
    initialisation sur `astro:page-load` (sans quoi ils meurent à la première
    navigation View Transitions) ;
  · le titre COURT (titreCourt(), lu dans le planche.json) — jamais le titre
    long du frontmatter, réservé au h1 et au référencement ;
  · « tout sur une page » : pas de pagination, pas de « voir plus ».

QUATRE COLONNES À XL, ni trois ni cinq : à trois la vignette est sur-échelle et
ses filets de 1 px s'épaississent de 24 %, à cinq son mono retombe à 6,5 px. La
spec porte le tableau complet. L'échelle des paliers intermédiaires est à
MESURER au rendu, pas à supposer.

CE QUE JE REFUSERAI :
  · une grille qui perd le statut, ou qui ne le porte que par une nuance ;
  · des filtres qui cessent de fonctionner après un aller-retour de navigation ;
  · une conclusion tirée d'un build vert : un build vert ne prouve pas que la
    page s'affiche. Contrôle le RENDU à 1440, 1280, 1024, 800 et 390 px, et
    donne-moi les mesures — vignette servie, hauteur totale, titres tronqués,
    débordement horizontal.

Termine par la mise à jour de `.claude/rules/tailwind-design-tokens.md` et de
`CLAUDE.md` dans le même commit : la prescription qui interdit la grille ne peut
pas survivre au chantier qui la contredit.
```
