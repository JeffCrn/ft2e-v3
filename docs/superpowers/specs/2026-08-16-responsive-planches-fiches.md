# Rendre le dessin présent à toutes les tailles d'écran — fiches de référence

*Rédigé le 2026-08-15, à l'issue de la remasterisation de `/references` en grille de cartes.
Le § « Prompt de lancement » se colle tel quel en session neuve : rien d'autre n'y est
supposé connu. Toutes les mesures ci-dessous ont été relevées au navigateur sur
`/references/logements-nerea-aytre/`, jamais estimées.*

> **✅ APPLIQUÉE le 2026-08-15.** Découpage retenu : `planche.svg` ≥ 880 px, `appui.svg` de
> 480 à 879, `vignette.svg` en dessous — chacun plafonné à sa taille de conception et centré,
> aucune échelle au-dessus de 1,00, mono minimal 6,79 px au point le plus défavorable.
>
> **La question éditoriale a été tranchée en deux temps, et la seconde réponse annule la
> première.** Le repli a d'abord été placé sous le dessin, réduit et plafonné ; à l'examen de
> la page rendue, FT2E l'a **supprimé** — voir le § « Le second arbitrage » ci-dessous. La
> figure est le dessin, son cartouche et l'agrandissement, rien d'autre.
>
> **L'agrandissement porte désormais le détail sur petit écran**, à deux états sous 940 px :
> ajusté à l'ouverture, puis 860 px pour lire, avec parcours au doigt.
>
> Quatre écarts par rapport aux hypothèses de ce document, tous imposés par le rendu et
> détaillés au § « Ce que la mesure a corrigé » : la borne haute est à 880 et non à `lg` ; la
> borne basse est à 480 et non à 640 ; le plafonnement du repli, que la spec n'avait pas
> prévu ; et enfin sa suppression, qui renverse la réponse que la spec appelait de ses vœux.

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

## Ce que la mesure a corrigé — bilan d'exécution du 2026-08-15

Trois hypothèses de ce document n'ont pas survécu au rendu. Elles sont consignées ici avec
ce qui les a renversées, pour qu'on ne les repose pas.

### 1. La borne haute n'est pas `lg` — elle est à 880

La spec proposait « ≥ 1024 px → planche ». Le plancher du mono la dément : le mono minimal
de la planche vaut **10 px sur les 23 dossiers**, il tient donc jusqu'à l'échelle 0,65, soit
un conteneur de 780 px, soit **845 px de fenêtre**. La planche descend donc presque 180 px
plus bas que `lg`. Contrôlée à l'œil à 880 px (échelle 0,679), elle reste parfaitement
lisible — étiquettes mono, ligne de jalons et géométrie du sankey compris.

880 plutôt que 845 : la marge, pour ne pas asseoir une borne sur la valeur exacte du
plancher.

### 2. La borne basse n'est pas 640 — elle est à 480

La spec proposait « 640–1023 → appui ». Mais l'appui tient jusqu'à un conteneur de 359 px,
soit **406 px de fenêtre** : le placer à 640 lui aurait retiré 160 px de bande utile. À
l'inverse, à 390 px l'appui tomberait à l'échelle 0,62, soit **6,2 px de mono — sous le
plancher**. La borne est donc posée à 480, c'est-à-dire **au-dessus de toutes les largeurs
de téléphone** (430 au plus, iPhone 15 Pro Max) : un téléphone reçoit la vignette, toujours.

### 3. Le repli devait être plafonné — la spec ne l'avait pas vu

Défaut trouvé au rendu à 879 px, invisible au calcul : un dessin plafonné à 552 et centré
dans un plan de 816 commence à **132 px** du bord, quand le repli commençait à **20**. Deux
blocs sans arête commune, que l'œil lit comme deux objets sans rapport.

Le même palier portait un second défaut, sans rapport apparent : le repli composait ses
lignes sur **776 px, soit ≈ 103 signes**, là où la charte prescrit 52 à 68.

Une seule règle corrige les deux — plafonner le repli à 552 px et le centrer comme le
dessin. Les colonnes se superposent alors à 4 px près (24 de marge interne au dessin, 20 de
padding au repli) et la ligne de lecture tombe à **512 px, soit 68 signes** : la borne haute
exacte de la charte. Que deux défauts indépendants se corrigent par la même mesure est ce
qui a fait retenir celle-ci plutôt qu'un réglage à l'œil.

### 4. Le second arbitrage — le repli est supprimé, pas déplacé

La première réponse à la question éditoriale (« le dessin précède le repli, qui reste
dessous, réduit ») a été appliquée, rendue, puis **renversée par FT2E à l'examen de la page**.
Elle avait raisonné sur la **figure seule** ; le défaut est ailleurs, dans l'**ordre de la
page**.

Sur téléphone une fiche se lit : titre → planche → cartouche technique → relevé → synthèse →
récit. Le repli s'intercalait entre l'illustration et le contenu réel :

| Fiche | hauteur du repli à 390 px | hauteur de la figure, avec → sans |
|---|---|---|
| `logements-nerea-aytre` | 791 px | 1 145 → **355** |
| `ehpad-coulonges-sur-autize-ssi` | 965 px | 1 333 → **368** |
| `passerelle-…-marans` | **1 181 px** | 1 535 → **355** |

Le visiteur traversait jusqu'à un écran et demi de valeurs synthétiques avant d'apprendre de
quoi la fiche parle. Et l'argument de fond se retourne : des valeurs qui arrivent **avant
tout contexte** ne démontrent rien — elles ne démontrent qu'une fois qu'on sait ce qu'on
regarde. Le détail reste accessible, mais par l'agrandissement, qui donne les 30 textes de la
planche entière et non les 13 ou 6 d'un format réduit.

**L'objection d'accessibilité est levée autrement, et mieux.** C'était le seul argument
solide pour garder le repli : `vignette.svg` est `aria-hidden` à la source, donc la servir
seule aurait laissé un lecteur d'écran devant rien. Son conteneur porte désormais
`role="img"` et l'`aria_label` de l'extraction — 822 signes, les mêmes que `planche.svg` et
`appui.svg` exposent nativement. Équivalent textuel intégral, zéro pixel visible, Lighthouse
accessibilité 100.

**Ce qui part avec le repli** : le garde-fou de build « toute extraction doit porter une forme
de repli », les quatre rendeurs d'archétype (`sankey`, `zonage`, liste `elements`, `releve`)
et les aides d'espaces insécables — 149 lignes. Le garde-fou protégeait d'un risque devenu
impossible (une fiche sans dessin ET sans lecture) : le maintenir aurait fait échouer le build
au nom d'un rendu qui n'a plus lieu. Même principe que l'amendement A9 — un contrôle se retire
avec ce qu'il contrôlait, sinon il ment sur son objet.

**Conséquence pour le protocole** : les blocs d'archétype du `planche.json` ne sont plus lus
par aucun rendu du site. Ils servent les compositeurs et la relecture FT2E ; un archétype
futur n'a plus rien à brancher côté composant.

### 5. L'agrandissement en portrait — deux états sous 940 px

Relevé par FT2E sur téléphone : à l'ouverture, une partie de la feuille est hors champ et le
réflexe est de basculer en paysage. La cause est géométrique et n'a pas de solution unique :
**une planche en 3:2 dans un écran en 1:2 ne peut pas être à la fois entière et lisible.**

Le `min-width: 860px` de la feuille est une cote de **lisibilité** — c'est la largeur en
dessous de laquelle le mono de 10 px de la planche passe sous le plancher de 6,5 (860 → 7,2).
La boîte était donc réglée pour lire, en acceptant le parcours : à 390 px, 42 % de la feuille
visible.

Réponse retenue — **deux états explicites**, plutôt qu'un compromis qui ne sert ni l'un ni
l'autre :

| État | Largeur de la feuille à 390 px | Échelle | Mono | Ce qu'on en fait |
|---|---|---|---|---|
| **Ajusté** (ouverture) | 334 × 223 px, entière | 0,278 | 2,78 | on saisit la structure d'un coup d'œil, sans basculer le téléphone |
| **Loupe** (« Lire au détail ») | 860 × 573 px | 0,717 | 7,17 | on lit, en parcourant du doigt, recadré au centre |

Le bouton vit dans la barre de la boîte, avec `aria-pressed`, et **n'apparaît que sous
940 px** — soit 860 + les 56 de marge de zone + la barre de défilement ≈ 931, arrondi à 940.
Au-delà les deux états donnent la même image et le bouton n'a plus d'objet. La boîte se rouvre
toujours ajustée : un état hérité de la consultation précédente rouvrirait sur un fragment,
soit exactement le défaut corrigé. Le pincer-pour-zoomer reste disponible par-dessus, la méta
viewport ne portant ni `maximum-scale` ni `user-scalable=no`.

⚠ **Piège payé à l'écriture** : les deux règles qui portent ces états doivent rester **après**
`.planche-plan` dans le `<style>`. Une `@media` n'ajoute aucune spécificité ; placées plus
haut — ce qui fut le cas au premier jet — elles sont écrasées par le `min-width: 860px` de la
règle de base, et la boîte s'ouvre agrandie. Ni le build, ni le typecheck, ni une capture ne
le signalent : seule la mesure de la largeur rendue l'a montré.

### Le relevé de réception

Mesuré sur `logements-nerea-aytre` (sankey), `ehpad-coulonges-sur-autize-ssi` (zonage) et
`passerelle-ecluse-carreau-d-or-marans` (liste `elements`). Les métriques de dessin sont
identiques sur les trois, les 23 planches partageant leurs trois viewBox.

| Fenêtre | Conteneur | Format servi | Largeur | Échelle | Mono | Débordement | Zoom |
|---|---|---|---|---|---|---|---|
| 1440 | 1152 | planche | 1150 | 0,958 | 9,58 | non | ✓ |
| 1280 | 1152 | planche | 1150 | 0,958 | 9,58 | non | ✓ |
| 1024 | 961 | planche | 959 | 0,799 | 7,99 | non | ✓ |
| 900 | 837 | planche | 835 | 0,696 | 6,96 | non | ✓ |
| 880 | 817 | planche | 815 | 0,679 | **6,79** | non | ✓ |
| 879 | 816 | appui | 552 | 1,000 | 10,0 | non | ✓ |
| 800 | 737 | appui | 552 | 1,000 | 10,0 | non | ✓ |
| 640 | 593 | appui | 552 | 1,000 | 10,0 | non | ✓ |
| 560 | 513 | appui | 511 | 0,926 | 9,26 | non | ✓ |
| 480 | 433 | appui | 431 | 0,781 | 7,81 | non | ✓ |
| 479 | 432 | vignette | 300 | 1,000 | 9,0 | non | ✓ |
| 390 | 343 | vignette | 300 | 1,000 | 9,0 | non | ✓ |

Poids de page en gzip, aux trois états du chantier :

| Fiche | avant chantier | avec repli | **état livré** | net |
|---|---|---|---|---|
| `logements-nerea-aytre` | 15 731 | 16 663 | **16 326** | +595 o |
| `ehpad-coulonges-sur-autize-ssi` | 14 453 | 15 229 | **14 791** | +338 o |
| `passerelle-…-marans` | 17 300 | 19 099 | **18 252** | +952 o |

**+21 % de brut ne coûte que +10 % de transporté** : les trois SVG d'un dossier partagent
mot pour mot leur bloc `<style>`, leurs noms de classes et la plupart de leurs libellés, et
la fenêtre de 32 ko de DEFLATE les retrouve. C'est ce qui rend l'inlining des trois formats
soutenable — et ce qui rend inutiles, pour l'instant, les deux replis que ce document
réservait au cas où (n'inliner que deux formats, ou composer un SVG à media queries
internes). **Ne pas les mettre en œuvre sans avoir refait la mesure.**

Le reste : `npm run typecheck` et `npm run build` verts (0 erreur), classes de bascule
présentes dans `dist/_astro/*.css` (`min-width:880px`), Lighthouse accessibilité **100** sur
`/references/logements-nerea-aytre/`, agrandissement fonctionnel à 390 px **après deux
navigations View Transitions** (le clone servi est bien la planche, viewBox 1200 × 800, à
860 px), `/references` inchangée (23 cartes, vignette à 274 px à 1440 — amendement A9 intact).

### Deux réserves, honnêtement

- **Le budget de poids HTML était déjà dépassé avant ce chantier.** `docs/10-budget-performance.md`
  fixe 15 ko gzip pour une page interne ; `logements-nerea-aytre` était à 15,7 et
  `passerelle` à 17,3 **avant** toute modification — le terme dominant est la planche inlinée
  elle-même, acquise au chantier des planches. Ce chantier ajoute 338 à 952 o. Le seuil est
  donc à réexaminer pour ce qu'il est : un budget écrit avant que les fiches ne portent un
  dessin vectoriel inliné.
- **La bascule à 880 px produit une variation de hauteur de la figure** — 617 px au-dessus,
  498 juste en dessous —, la planche à l'échelle 0,68 étant plus haute que l'appui à sa cote.
  L'écart est de 119 px, sans recouvrement ni débordement horizontal à aucun palier. Il était
  de 346 à 731 px tant que le repli paraissait à cette borne ; sa suppression l'a réduit d'un
  facteur trois à six, sans que ce fût le but.

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
