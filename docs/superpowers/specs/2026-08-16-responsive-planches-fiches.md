# Rendre le dessin présent à toutes les tailles d'écran — fiches de référence

*Rédigé le 2026-08-15, à l'issue de la remasterisation de `/references` en grille de cartes.
Le § « Prompt de lancement » se colle tel quel en session neuve : rien d'autre n'y est
supposé connu. Toutes les mesures ci-dessous ont été relevées au navigateur sur
`/references/logements-nerea-aytre/`, jamais estimées.*

---

## Le défaut

Sur une fiche de référence, **le dessin disparaît dès que l'écran se réduit** et cède la
place à un bloc de texte et de chiffres. Mesuré :

| Fenêtre | Largeur de la figure | Ce qui s'affiche | Hauteur du bloc |
|---|---|---|---|
| 1440 | 1152 px | le dessin (échelle 0,96) | — |
| 1024 | 961 px | le dessin (échelle 0,80) | — |
| 800 | 737 px | **du texte seul** | 566 px |
| 390 | 343 px | **du texte seul** | 881 px |

La bascule est brutale et unique : `hidden lg:block` sur le dessin, `lg:hidden` sur le
repli. À 1023 px la fiche est un schéma ; à 1024 px elle est un tableau de valeurs.

Ce n'est pas une négligence, c'est un arbitrage devenu faux. `PlancheReference.astro`
l'expose en tête de fichier : *« Sous `lg`, le dessin cède la place à sa lecture. À 358 px
l'échelle vaut 0,30 : aucun schéma ne s'y lit. »* Le raisonnement était juste **tant qu'il
n'y avait qu'un seul dessin à montrer**. Il ne l'est plus.

**Le coût, lui, est réel et se lit à l'œil** : sur téléphone, la fiche perd sa hiérarchie.
Le lecteur reçoit 881 px de libellés et de nombres alignés là où la page devait poser une
image, et plus rien ne distingue l'illustration du contenu. C'est le point de départ de ce
chantier.

---

## Ce qui rend la correction possible, et qui n'était pas su

**Les trois fichiers ne sont pas trois tailles du même dessin : ce sont trois compositions
distinctes, à charge de texte décroissante.** Contrôlé fichier par fichier sur
`logements-nerea-aytre` :

| Fichier | viewBox | Éléments `<text>` | Poids | Ce qu'il porte |
|---|---|---|---|---|
| `planche.svg` | 1200 × 800 | **30** | 10,8 ko | surtitre long, titre, chapô, les trois marchés détaillés, tous les libellés |
| `appui.svg` | 552 × 368 | **13** | 6,1 ko | surtitre court, les trois chiffres (42 / 30 / 18), la légende ramassée |
| `vignette.svg` | 300 × 200 | **6** | 3,7 ko | le motif seul, chiffres regroupés (A et B 42 · C, D, E 48) |

Chacune a été composée pour être lue à sa propre taille. **La réduction est éditoriale,
pas géométrique** — c'est exactement ce que le protocole des planches impose (« une
planche se compose à la taille où elle est lue »), et c'est ce qui rend légitime de servir
l'une ou l'autre selon la place disponible. Sans cette propriété, le chantier serait une
mise à l'échelle, donc interdite.

**Les 23 dossiers de `public/images/projets/` portent leurs 5 pièces.** Aucun n'est
incomplet : la matière existe pour toutes les fiches, il n'y a rien à produire.

---

## L'arithmétique — ce que chaque format donne à chaque largeur

Conteneur = `min(fenêtre, 1200) − 48` au-dessus de 768 px (`px-6`), `− 32` en dessous
(`px-4`). Échelle = largeur servie ÷ largeur de conception.

| Fenêtre | Conteneur | `planche` (1200) | `appui` (552) | `vignette` (300) |
|---|---|---|---|---|
| 1440 | 1152 | **0,96** | 2,09 | 3,84 |
| 1280 | 1152 | **0,96** | 2,09 | 3,84 |
| 1024 | 961 | **0,80** | 1,74 | 3,20 |
| 900 | 837 | 0,70 | 1,52 | 2,79 |
| 800 | 737 | 0,61 | 1,34 | 2,46 |
| 640 | 608 | 0,51 | **1,10** | 2,03 |
| 560 | 528 | 0,44 | **0,96** | 1,76 |
| 390 | 358 | 0,30 | 0,65 | **1,19** |

Deux enseignements, tous deux à prendre au sérieux :

1. **Aucun découpage en trois bandes ne place les trois dessins à leur taille**, parce que
   les bandes de largeur sont plus larges que la plage d'échelle acceptable. Entre 660 et
   1023 px, ni la planche (0,55 à 0,80) ni l'appui (1,20 à 1,74) n'est à sa cote.
2. **La sur-échelle est le vrai danger, pas la sous-échelle.** Le protocole des planches
   l'a documenté sur l'appui du hero : « la vignette grossie à 1,84 épaissit tous les
   filets de 1 px ». Une échelle supérieure à 1 dégrade le trait ; une échelle inférieure
   réduit le corps du mono, dont le plancher de lisibilité est **6,5 px** (le mono du
   dessin fait 9 à 10 px selon le format).

### L'hypothèse de tête — à mesurer, pas à croire

**Plafonner chaque dessin à sa taille de conception et le centrer**, plutôt que l'étirer :

```
≥ 1024 px  → planche,  largeur du conteneur (0,80 → 0,96)
640–1023   → appui,    max-width 552 px, centré  (jamais > 1,00)
< 640      → vignette, max-width 300 px, centré  (jamais > 1,00)
```

Aucun dessin n'est alors servi au-dessus de sa cote, et la marge blanche qui reste autour
est légitime : un plan a des marges. **Ce n'est pas une conclusion, c'est le point de
départ de la mesure** — trois choses restent à vérifier au rendu, et elles peuvent
renverser le découpage :

- **la planche descend-elle plus bas que `lg` sans casser ?** À 800 px elle vaut 0,61, son
  mono de 10 px se rend à 6,1 — sous le plancher, mais de peu. À vérifier à l'œil, sur
  plusieurs archétypes, avant d'écarter l'option la plus simple (une seule bascule) ;
- **l'appui porte-t-il ses propres marges ?** La planche en a (56 px dans son repère), ce
  qui lui permet d'ÊTRE le plan posé sans padding. Si l'appui et la vignette n'en ont pas,
  ils toucheront le filet du plan et il faudra leur en donner ;
- **les bornes 640 et 1024 sont-elles les bonnes ?** Elles sont posées ici sur l'échelle
  seule. Le rendu peut commander de les déplacer — auquel cas on documente pourquoi.

---

## Ce qui doit survivre

### 1. Le SVG reste INLINÉ

Un SVG appelé en `<img src>` est un document isolé : il ne reçoit ni les polices de la
page ni les variables CSS des jetons. Les trois formats se lisent au build par
`fs.readFileSync` et s'injectent par `set:html`. **Ne pas « optimiser » en passant à
`<img>` ou à `<picture>`** — la règle est ancienne, mesurée, et sa violation ne se voit
qu'après coup (le dessin se rend en Times, hors palette).

### 2. Le poids de page devient un critère, parce que trois SVG au lieu d'un

Inliner les trois formats fait passer une fiche de 10,8 ko à **20,6 ko de SVG brut**, et
le HTML les transporte tous les trois même si deux sont en `display:none`. C'est
mesurable et ça doit l'être : budget de performance à `docs/10-budget-performance.md`,
LCP mobile < 1,8 s, CLS < 0,05.

Si le surcoût gzippé s'avère notable, deux voies — à n'explorer **qu'après mesure** :
n'inliner que deux formats sur trois, ou composer un seul SVG dont des groupes
s'affichent par media query interne. Ne pas préempter.

### 3. L'agrandissement

`PlancheReference` porte une boîte d'agrandissement (`data-planche-agrandir`,
`data-planche-zone`), aujourd'hui `hidden lg:inline-flex` — donc **absente précisément là
où elle servirait le plus**. Si le dessin revient sur téléphone, la question se pose :
la vignette + l'agrandissement au doigt sont peut-être la vraie réponse aux petits écrans,
plus que le choix du format. À traiter dans le même chantier.

Ses scripts s'initialisent sur `astro:page-load` avec garde `dataset` : **ne pas perdre
ce motif** dans la réécriture, sous peine d'un composant inerte après la première
navigation View Transitions (`.claude/rules/astro-conventions.md`).

### 4. `planche.json` reste la source unique

Le repli de lecture en est bâti, et c'est ce qui interdit qu'il diverge du dessin. Le
titre court des cartes en vient aussi, par `titreCourt()`. Rien ne se recopie au
frontmatter.

### 5. La légende et le cartouche

`extraction.cartouche_legende` est rendu en deux variantes (`lg:hidden` et
`hidden lg:block`). Elles suivent la même bascule que le dessin et devront suivre le
nouveau découpage.

---

## La question à poser avant de coder

**Le repli de lecture disparaît-il, ou devient-il un complément ?**

Ce n'est pas une question d'implémentation, et elle ne se tranche pas seul.

La vignette publie **6 textes** là où la planche en publie **30**. Servir la vignette sur
téléphone rend donc le dessin visible *et* retire de la page les valeurs que le repli
portait — « 146 845 kWh/an », « 38 000 m³/h », les jalons, les libellés de zone. Sur une
fiche technique, ce sont ces valeurs qui font la démonstration.

Trois réponses possibles, à soumettre avec un avis motivé :

- **le dessin remplace le repli** — la fiche est plus lisible, mais elle publie moins sur
  téléphone que sur bureau, ce qui est un choix éditorial assumé, pas un détail ;
- **le dessin précède le repli, qui reste dessous, réduit** — l'information est conservée,
  la hiérarchie est rétablie (une image, puis sa lecture), au prix de la hauteur de page ;
- **le dessin précède un repli replié** (résumé + dépliage à la demande) — compromis, mais
  il introduit une interaction que la charte v3 ne connaît pas : à ne proposer que si les
  deux premières échouent.

**Ne pas commencer le code avant que ce point soit tranché.**

---

## Pièges déjà payés, à ne pas repayer

1. **Tailwind v4 lit le `.gitignore`** et élague les répertoires qui y correspondent, sans
   que le build échoue. Vérifier toute classe en valeur arbitraire dans `dist/_astro/*.css`,
   sélecteur par sélecteur — et Tailwind **échappe** les deux-points : chercher
   `.lg\:hidden`, jamais `lg:hidden`. Incident du 2026-08-08, quatre déploiements.
2. **Un bloc `data-plan` est à opacité 0 tant qu'il n'est pas entré dans la vue.** Une
   capture pleine hauteur montre un cadre vide et fait croire à une casse. Faire défiler,
   attendre ~800 ms, puis capturer. La figure de la planche EST un `data-plan`.
3. **Chrome sous Windows refuse une fenêtre sous 500 px** : le contrôle à 390 px se fait
   par une iframe de 390 dans une fenêtre de 500.
4. **Playwright pilote le Chrome du client et `browser_resize` persiste** : toujours
   restaurer la fenêtre à 1440 en fin de session, sans quoi la page suivante paraîtra
   cassée.
5. **`trailingSlash: 'always'`** : toute requête curl sur le serveur de prévisualisation
   doit porter la barre oblique finale, sinon 404 — y compris les liens internes que la
   page préfétche (leurs 404 en console sont un artefact du preview, pas un bug).
6. **Mesurer le texte au `Range`, jamais au `scrollWidth`** : sur un bloc qui ne déborde
   pas, `scrollWidth` vaut la boîte et ne dit rien du texte.
7. **Un build vert ne prouve pas que la page s'affiche.** Contrôler le rendu, page par
   page, à chaque palier.

---

## Critères de réception — mesurés, pas affirmés

À vérifier sur au moins **trois fiches d'archétypes différents** (par exemple
`logements-nerea-aytre` — sankey, `ehpad-coulonges-sur-autize-ssi` — zonage, et une fiche
à liste `elements`), aux paliers **1440, 1280, 1024, 900, 800, 640, 560 et 390** :

- [ ] **à aucun palier la fiche n'est privée de dessin** — c'est l'objet du chantier ;
- [ ] aucun dessin servi **au-dessus de sa taille de conception** (échelle ≤ 1,00), et
      aucun dont le mono tombe **sous 6,5 px** ;
- [ ] aucun débordement horizontal à 390 px ;
- [ ] la bascule d'un format à l'autre ne produit **ni saut de hauteur ni recouvrement** ;
- [ ] l'agrandissement fonctionne à tous les paliers où il est proposé, **après un
      aller-retour de navigation View Transitions** ;
- [ ] le poids de page d'une fiche est **relevé avant et après** (HTML brut et gzippé), et
      le budget de `docs/10-budget-performance.md` est tenu ;
- [ ] `npm run typecheck` et `npm run build` verts, **et** les classes de bascule présentes
      dans `dist/_astro/*.css` ;
- [ ] Lighthouse accessibilité **100** sur une fiche — le dessin est `aria-hidden`, ce qui
      rend d'autant plus critique ce que devient le repli côté lecteur d'écran ;
- [ ] `CLAUDE.md` et `.claude/rules/` **mis à jour dans le même commit** : le § « Les
      planches de références » de `CLAUDE.md` et l'en-tête de `PlancheReference.astro`
      affirment tous deux que « sous `lg`, le dessin cède la place à sa lecture ». Cette
      phrase ne peut pas survivre au chantier qui la contredit.

---

## Ce qu'on ne touche pas

- **Les cinq pièces de chaque planche et les compositeurs** (`scripts/planches/`) : aucune
  régénération, aucun recadrage, aucun redimensionnement de fichier. Le chantier choisit
  parmi ce qui existe, il ne produit pas.
- **La vignette sur `/references`** : elle vient d'être calée à 274 px, sa taille de
  conception exacte (amendement A9). Ne pas y toucher.
- **L'appui sur le hero de l'accueil** (`src/pages/index.astro`, fiche `en_avant`) : il y
  est servi à ~552 px, à sa cote.
- **`planche.json`** comme source unique des titres, valeurs et alternatives textuelles.
- **Le `<h1>`, la balise `<title>`, la description et le JSON-LD** des fiches.

---

## Prompt de lancement d'une session neuve

À coller tel quel.

```text
Tu traites la dimension responsive des visuels des fiches de référence du
site FT2E. Aujourd'hui le dessin disparaît sous 1024 px et cède la place à
un bloc de texte et de chiffres — 881 px de libellés alignés à 390 px. La
hiérarchie de la page s'effondre : plus rien ne distingue l'illustration du
contenu. L'objectif est que le DESSIN reste présent à toutes les tailles.

AVANT TOUTE AUTRE CHOSE, cloner le dépôt et lire la spécification. Elle fait
autorité sur tout ce qui suit, y compris sur ce message :

    git clone --depth 1 https://github.com/JeffCrn/ft2e-v3
    docs/superpowers/specs/2026-08-16-responsive-planches-fiches.md

CE QUI REND LA CORRECTION POSSIBLE, et qui n'était pas su : les trois
fichiers de chaque dossier de public/images/projets/ ne sont PAS trois
tailles du même dessin, ce sont TROIS COMPOSITIONS DISTINCTES à charge de
texte décroissante — planche.svg porte 30 éléments de texte, appui.svg en
porte 13, vignette.svg en porte 6. Chacune est composée pour être lue à sa
propre taille. C'est ce qui rend légitime de servir l'une ou l'autre selon la
place : ce n'est pas une mise à l'échelle, que le protocole des planches
interdit. Les 23 dossiers portent bien leurs 5 pièces, il n'y a rien à
produire.

    planche.svg   viewBox 1200 × 800   lue à 1152   (grand écran)
    appui.svg     viewBox  552 × 368   lue à ~552   (écran intermédiaire)
    vignette.svg  viewBox  300 × 200   lue à 274    (petit écran)

COMMENCE PAR LA QUESTION ÉDITORIALE, PAS PAR LE CODE. La vignette publie 6
textes là où la planche en publie 30 : ramener le dessin sur téléphone retire
de la page les valeurs que le bloc de texte portait. Le bloc disparaît-il, ou
reste-t-il SOUS le dessin ? Pose-la-moi avant d'écrire une ligne, avec ton
avis motivé. La spec détaille les trois réponses possibles.

L'HYPOTHÈSE DE TÊTE est de PLAFONNER chaque dessin à sa taille de conception
et de le centrer, plutôt que de l'étirer — aucun format servi au-dessus de
1,00, la marge blanche autour étant légitime sur un plan. Ce n'est PAS une
conclusion : la spec porte le tableau d'échelles complet et les trois points
à vérifier au rendu, qui peuvent renverser le découpage.

CE QUI DOIT SURVIVRE — la spec le détaille, ne le redécouvre pas :
  · le SVG reste INLINÉ, jamais en <img src> : en src il perd les polices et
    les jetons de la page, et ça ne se voit qu'après coup ;
  · les scripts s'initialisent sur `astro:page-load` avec garde `dataset`,
    sinon le composant est inerte après la première navigation ;
  · planche.json reste la source unique — rien ne se recopie au frontmatter ;
  · le poids de page devient un critère : trois SVG inlinés au lieu d'un font
    passer une fiche de 10,8 à 20,6 ko de SVG brut. À MESURER, avant/après.

TRAITE AUSSI L'AGRANDISSEMENT : la boîte de zoom est aujourd'hui
`hidden lg:inline-flex`, donc absente précisément là où elle servirait le
plus. Vignette + agrandissement au doigt est peut-être la vraie réponse aux
petits écrans.

CE QUE JE REFUSERAI :
  · un palier, un seul, où la fiche n'a pas de dessin ;
  · un dessin servi au-dessus de sa taille de conception — la sur-échelle
    épaissit les filets de 1 px, c'est le défaut fondateur du dispositif ;
  · une régénération ou un recadrage de fichier : on choisit parmi ce qui
    existe, on ne produit pas ;
  · une conclusion tirée d'un build vert. Contrôle le RENDU sur TROIS fiches
    d'archétypes différents, à 1440, 1280, 1024, 900, 800, 640, 560 et
    390 px, et donne-moi les mesures — format servi, échelle, corps du mono,
    hauteur de bloc, débordement horizontal, poids de page.

Termine par la mise à jour de `CLAUDE.md` et de l'en-tête de
`PlancheReference.astro` dans le même commit : tous deux affirment que « sous
lg, le dessin cède la place à sa lecture ». Cette phrase ne peut pas survivre
au chantier qui la contredit.
```
