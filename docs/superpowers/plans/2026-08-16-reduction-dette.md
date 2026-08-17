# Programmation de la réduction de dette — FT2E v3

> **Objet.** Ordonnancer en sessions de travail les constats du **relevé de dette du
> 2026-08-15** (commit `d3bd8d9`). Le relevé mesure ; ce document exécute.
>
> **Source unique :** l’artefact « Relevé de dette FT2E v3 »
> — <https://claude.ai/code/artifact/15dabf99-84c0-4b7c-a2cd-4bfd88d5b3ef>
> Toute mesure citée ici en vient. **Aucun chiffre de ce document n’a été redérivé** :
> s’ils divergent du dépôt, c’est le dépôt qui a bougé depuis `d3bd8d9`, et il faut
> remesurer avant d’agir.
>
> **Ouvert le 2026-08-16.** État : **4 sessions sur 4 exécutées** (S1, S2, S3, S4),
> **1 décision sur 2 tranchée** (D1) — **D2 reste pendante chez FT2E**. Une session
> de suites, **S5**, a soldé le dernier point laissé ouvert et constaté au
> 2026-08-16 qu’aucune des trois réponses n’était arrivée.

---

## D’où vient cette programmation

Le relevé de dette a trois registres — treize dettes déclarées **vérifiées comme
soldées**, onze points ouverts **que le dépôt déclarait déjà**, et dix constats
**que rien ne déclarait**. Sa section 06 propose un ordre en neuf rangs. Cette
programmation regroupe ces neuf rangs en **quatre sessions de travail et deux
décisions**, selon deux critères :

1. **Ce qui réécrit les mêmes fichiers va dans la même session.** Le relevé le
   demande explicitement pour les rangs 2 et 3 : « les séparer double le contrôle
   de rendu à 1 152 px ». Le même argument regroupe les rangs 6, 7 et 8.
2. **Ce qui n’est pas du travail n’est pas une session.** Les rangs 5 et 9 sont
   des arbitrages : ils se posent, ils ne s’exécutent pas. Les traiter comme des
   sessions les ferait attendre leur tour alors qu’ils doivent circuler dès
   maintenant — le premier conditionne les critères de recette du reste.

### Le tableau de marche

| Session | Rangs du relevé | Nature | Bloquant du projet ? |
|---|---|---|---|
| **S1** — Le pipeline d’images | 1 | technique, structurel | ✅ oui — LCP 15,68 s, perf 74 |
| **S2** — Les planches : typographie et régénération | 2 + 3 | éditorial + technique | non, mais c’est le livrable le plus visible |
| **S3** — Les trois défauts de rendu | 4 | technique, localisé | ✅ oui — CLS 0,098 pour un plafond de 0,05 |
| **S4** — Hygiène documentaire et garde-fous | 6 + 7 + 8 | hygiène, sans risque | non |
| **D1** — Arbitrage A2 × Lighthouse 100 | 5 | décision | ✅ conditionne les recettes a11y |
| **D2** — Trois questions à FT2E | 9 | décision client | non |

**D1 circule dès l’ouverture de S1**, pas à son rang : la recette d’accessibilité
de S3 est indécidable tant qu’il n’est pas tranché (voir § S3).

---

## S1 — Le pipeline d’images

> **Rang 1 du relevé.** Le seul constat qui rend une page inutilisable sur mobile,
> et le seul qui doive être en place **avant** le reportage photographique.

### Le constat, tel que mesuré

```
/equipe/   perf=74   LCP=15,68 s   poids=4 766 Kio
collectif.jpg 846 Ko · geraldine.jpg 617 Ko · emma.jpg 563 Ko
```

Huit JPEG bruts de 460 à 866 Ko, servis par un `<img>` depuis `public/`, sans
`astro:assets` : ni AVIF, ni WebP, ni `srcset`. Le critère de blocage du projet est
un **LCP mobile sous 1,8 s** et une **performance d’au moins 90**
(`.claude/rules/astro-conventions.md` § Performances).

**Le reportage photographique ne réglera rien.** Ce qui manque n’est pas la qualité
des images, c’est le pipeline : de vraies photographies pèseront autant. C’est la
raison pour laquelle cette session passe en premier — livrer le reportage sur le
pipeline actuel rejouerait le défaut à l’identique, avec des fichiers qu’on ne
pourra plus regénérer soi-même.

### Ce que la session doit réellement faire

⚠ **Ce n’est pas « enrober les `<img>` dans `<Image>` ».** Vérifié au dépôt le
2026-08-16 :

| Constat | Conséquence |
|---|---|
| Les huit JPEG sont dans `public/images/equipe/` | `astro:assets` ne les verra jamais — `public/` est **recopié tel quel**, il n’est pas un pipeline |
| `src/assets/` **n’existe pas** | il est à créer |
| Le champ Zod `photo` est une `z.string()` — un chemin depuis `public/` | le chemin doit être **résolu** vers un module, pas passé à `src` |
| `equipe.astro` rend un `<img src={membre.photo}>` | à remplacer par `<Image src={module} …>` |
| `fs.existsSync` garde `hasPhoto` et `collectifExiste` | à reporter sur le glob (voir ci-dessous) |

**La forme retenue** — déplacer les fichiers dans `src/assets/equipe/`, puis résoudre
le chemin du frontmatter par un `import.meta.glob` avec `eager: true`. Le champ Zod
ne bouge pas : le contenu continue de nommer un chemin, c’est le rendu qui apprend à
le résoudre.

**Le garde-fou `fs.existsSync` se reporte sans se dupliquer** : l’absence d’entrée
dans le glob *est* l’absence de fichier. Le même mécanisme fait alors les deux
métiers — résoudre l’image et détecter qu’elle manque — là où le code actuel en
emploie deux (`fs.existsSync` pour tester, une chaîne pour servir). C’est une
simplification, pas une charge supplémentaire ; le motif documenté dans
`.claude/rules/astro-conventions.md` § « Images optionnelles & fs.existsSync »
devra être mis à jour dans le même commit.

⚠ **La photographie collective est rendue à deux endroits** — `src/pages/equipe.astro`
(`collectifExiste`) **et** `src/pages/index.astro` (même constante). Les deux migrent
ensemble ou l’accueil casse.
> ⚠ **Faux — il y en a TROIS.** Relevé à l’exécution le 2026-08-16 :
> `src/pages/societe.astro` porte un troisième rendu (bandeau 21:8), avec la même
> constante. Les trois sont migrés ; le chemin est désormais porté une seule fois
> par `CHEMIN_COLLECTIF` (`src/lib/photos.ts`).

⚠ **`duotone-photo` est un filtre CSS posé sur l’élément.** `<Image>` émet bien un
`<img>`, la classe se pose dessus sans changement. Le vérifier au rendu quand même :
la charte interdit toute couleur native (règle du duotone 197°).

### Critères de recette — mesurés, pas déclarés

| Critère | Seuil | Instrument |
|---|---|---|
| LCP mobile sur `/equipe/` | **< 1,8 s** | Lighthouse mobile |
| Performance sur `/equipe/` | **≥ 90** | Lighthouse mobile |
| Performance sur `/` | **≥ 90**, sans régression | Lighthouse mobile |
| Formats émis | AVIF **et** WebP présents dans `dist/` | `ls dist/_astro/*.avif` |
| `srcset` présent sur les huit portraits | 8 occurrences | `grep -c srcset dist/equipe/index.html` |
| Repli « Photo à venir » toujours fonctionnel | rendu correct en retirant un fichier | build + capture |
| Duotone conservé | aucune couleur native à l’écran | capture |

```bash
npm run build && npm run preview          # puis, sur un autre terminal :
npx lighthouse http://localhost:4321/equipe/ --preset=perf --form-factor=mobile --quiet
```

### ✅ Exécutée le 2026-08-16 — ce qui a été mesuré

Toutes les mesures ci-dessous sont **Lighthouse mobile sur `npm run preview`**
(localhost, throttling simulé), avant et après, sur la même machine et dans la même
session. Trois runs de contrôle après migration : perf 98 / 98 / 98, LCP 2,2 s à
chaque fois — la mesure est stable, pas un tirage heureux.

| Page | Avant | Après |
|---|---|---|
| `/equipe/` — poids | **4 766 Kio** | **243 Kio** (**−94,9 %**) |
| `/equipe/` — performance | 93 | **98** |
| `/equipe/` — LCP | 3,0 s | **2,2 s** |
| `/` — performance | 96 | **96** (aucune régression) |
| `/societe/` — performance | non mesuré avant | 98 |

⚠ Ces chiffres sont ceux de `npm run preview`. **Ceux qui font foi sont ceux du
déploiement**, plus bas : `/equipe/` perf **100**, LCP **1,2 s**. Voir la règle de
méthode ci-dessous — le serveur de prévisualisation ne compresse rien.

- **AVIF et WebP** : 26 fichiers de chaque dans `dist/_astro/`. Sur `/equipe/`,
  8 `<picture>`, 24 `srcset`, 8 × `type="image/avif"` et 8 × `type="image/webp"`.
- **Ressource la plus lourde de `/equipe/`** : ce n'est plus une image mais la
  police Archivo variable ( 90 104 octets ). La plus grosse image fait 27 Ko.
  ⚠ Constat de taille, **pas** de goulot : un woff2 est déjà compressé, et le
  déploiement le sert à l'octet près comme le fait le serveur local — voir la
  correction plus bas.
- **Repli** : `tanguy.jpg` retiré → build vert, 7 `<picture>` au lieu de 8, la
  cellule bascule sur la hachure `duotone-media`, zéro occurrence de `tanguy` dans
  le HTML émis.
- **Duotone** : contrôlé en *computed style*, pas à l'œil —
  `filter: grayscale(1) contrast(1.05)`, `mix-blend-mode: lighten`, fond
  `rgb(0,23,24)`, `::after` `rgb(225,244,244)` en `darken`. Aucune couleur native.
- **390 px** : `/equipe/` sans débordement horizontal, collectif servi à 293 px
  (variante 420 w), portraits à 170 px.

#### ✅ Le critère « LCP mobile < 1,8 s » EST tenu — mesuré sur le déploiement

| Instrument | perf | FCP | LCP | poids |
|---|---|---|---|---|
| `npm run preview` (localhost) | 98 | 1,8 s | 2,2 s | 243 Kio |
| **`ft2e-v3.vercel.app` (déployé)** | **100** | **1,0 s** | **1,2 s** ✅ | 240 Kio |

⚠ **Correction d'une conclusion publiée quelques minutes plus tôt**, y compris dans
le message du commit `71cc72f` : ce message annonce le critère non tenu et
« non atteignable », en désignant la police de 88 Ko comme plancher. **C'est faux,
et le commit ne sera pas réécrit** — réécrire l'historique invalide tous les SHA
cités dans les plans et les règles (voir § D2). La correction vit ici.

**Ce qui était mesuré n'était pas le site, c'était le serveur de prévisualisation.**
`astro preview` sert **tout sans compression** — aucun en-tête `Content-Encoding` ;
Vercel sert le HTML et le CSS en **brotli**. Le CSS fait 48 Kio bruts, et sous le
throttling simulé slow-4G de Lighthouse ces 48 Kio non compressés sur le chemin
bloquant sont exactement ce qui portait le FCP à 1,8 s.

La police que le diagnostic accusait est un **faux coupable** : un woff2 est déjà
compressé en interne, il est servi à **90 104 octets sur les deux serveurs** — et le
LCP passe pourtant de 2,2 à 1,2 s. Ce n'était pas elle.

Après correction, `lcp-discovery-insight` passe à 1/1 (`requestDiscoverable`,
`eagerlyLoaded`, `priorityHinted` tous vrais) : côté image il n'y a plus rien à
gagner, et il n'y a plus rien à chercher ailleurs non plus.

> ### 📏 Règle de méthode, à appliquer aux sessions suivantes
>
> **`npm run preview` n'est pas un instrument de mesure de performance sur ce
> projet.** Il reste l'instrument du *rendu* (règle 11 du `CLAUDE.md`, inchangée),
> mais tout jugement de LCP, de FCP ou de score de performance pris dessus est
> biaisé d'environ **0,8 s vers le haut** — et le biais porte précisément sur la
> chaîne bloquante, c'est-à-dire là où l'on cherche à conclure.
>
> Une performance se mesure **sur `https://ft2e-v3.vercel.app`**, après avoir
> vérifié que le déploiement porte bien le commit en cours. C'est ce que faisait le
> relevé de dette, et c'est pourquoi ses chiffres ne se rejouaient pas en local.
>
> Le contrôle de fraîcheur du déploiement doit porter sur un **marqueur du build**,
> jamais sur un délai : ici, le passage de 0 à 8 occurrences de `type="image/avif"`
> dans le HTML servi de `/equipe/`. Un `sleep` suivi d'une mesure peut mesurer
> l'ancienne build sans que rien ne le signale.

#### ⚠ Deux écarts entre le plan et le dépôt, relevés à l'exécution

1. **La photographie collective est rendue à TROIS endroits, pas deux** : le plan
   citait `index.astro` et `equipe.astro` ; `societe.astro` porte un troisième rendu
   (bandeau 21:8) avec la même constante. Les trois sont migrés, et le chemin est
   désormais porté une seule fois par `CHEMIN_COLLECTIF` — c'est par la recopie que
   la troisième occurrence pouvait être manquée.
2. **Le repli « [Photo à venir] » n'existait dans aucune page** — seulement dans
   l'exemple de `.claude/rules/astro-conventions.md`. Les trois emplacements
   rendaient une hachure `duotone-media` nue. Le comportement est **conservé tel
   quel** et la règle a été réécrite pour décrire le code : le site est en
   démonstration client, et une hachure se lit comme un placeholder dessiné là où un
   libellé se lirait comme un site inachevé. À rouvrir si FT2E en décide autrement.

#### ✅ Le relevé mesurait le déploiement — et sur cet instrument, avant/après se compare

Le relevé donnait `/equipe/` à **perf 74, LCP 15,68 s, poids 4 766 Kio**. Ce chiffre
ne se rejouait pas sur `npm run preview` (93 / 3,0 s / 4 766 Kio) et cet écart a
d'abord été mis au compte de l'instrument. **La vraie raison est que le relevé
mesurait le déploiement**, ce que la mesure post-déploiement confirme : sur
`ft2e-v3.vercel.app`, la même page passe de **74 à 100** et de **15,68 à 1,2 s**.

Le poids, lui, tombait au kilo-octet près sur les deux instruments — c'est ce qui a
permis de vérifier qu'il s'agissait bien de la même page avant d'agir.

| `/equipe/` sur le déploiement | Relevé du 2026-08-15 | Après S1 |
|---|---|---|
| Performance | 74 | **100** |
| LCP | 15,68 s | **1,2 s** |
| Poids | 4 766 Kio | **240 Kio** |

---

## S2 — Les planches : typographie et régénération

> **Rangs 2 et 3, fusionnés à la demande du relevé** : « les deux réécrivent les
> mêmes fichiers, et les séparer double le contrôle de rendu à 1 152 px ».

### Les deux constats

**L’apostrophe droite, sur tout le corpus dessiné.** La règle éditoriale impose
U+2019 sur « tout contenu textuel destiné à l’utilisateur final ». Les planches — le
livrable le plus récent et le plus visible — ne l’ont jamais reçue :

```
205 occurrences dans le texte dessiné des SVG
1 325 occurrences dans les extractions planche.json, aria_label compris
```

Les `aria_label` sont **lus tels quels par les lecteurs d’écran**. L’outil existe
déjà — `scripts/injection-typographique.py` définit `APO = '’'` — il n’a simplement
jamais été passé sur `public/images/projets/`. Le relevé nomme exactement la cause :
*la discipline appliquée à `src/content/` n’a pas suivi le contenu quand il a changé
de répertoire.*

**L’invariant de régénération est rompu.** Quatorze planches datent des 13 et 14 août,
alors que la correction de `_tronc.mesurer` n’est arrivée que le 15 avec la planche 21
(`1b23d48`). « Régénération octet à octet » — le seul contrôle qui protège les planches
publiées d’une dérive du tronc commun — ne tient plus tant que la passe n’est pas faite.

### ⚠ L’ordre des deux opérations n’est pas indifférent

**Corriger la typographie d’abord, régénérer ensuite.** Dans l’autre sens, la
régénération réécrit les SVG depuis les compositeurs et **écrase les apostrophes
corrigées** — on aurait fait le travail deux fois, et le second passage effacerait le
premier sans que rien ne le signale.

Corollaire : la correction porte sur **la source**, pas sur le rendu.

1. `planche.json` de chaque dossier — c’est la pièce que FT2E relit, et la source du
   titre court, du cartouche et de l’`aria_label` ;
2. les compositeurs `scripts/planches/<archetype>.py` et le tronc `_tronc.py`, s’ils
   portent des chaînes littérales à apostrophe ;
3. **puis** régénération des 23 dossiers, qui propage la correction aux trois SVG.

Corriger les SVG directement serait une correction de sortie : elle disparaîtrait à la
première régénération. C’est le même principe que la règle des deux titres — on corrige
l’original, jamais la copie.

### Critères de recette

| Critère | Seuil | Instrument |
|---|---|---|
| Apostrophes droites dans les 23 `planche.json` | **0** | `grep -c "'" public/images/projets/*/planche.json` |
| Apostrophes droites dans les 69 SVG | **0** | balayage des `<text>` |
| Régénération octet à octet | **23 / 23** | rejouer les compositeurs, comparer les sommes |
| Rendu de la planche à 1 152 px | inchangé hors apostrophes | capture, échantillon de 3 dossiers |
| Rendu de la vignette à 300 px | inchangé | capture, même échantillon |
| Build | vert | `npm run build` |

⚠ **Contrôler à la taille de lecture, jamais en pleine page** (règle 13 du `CLAUDE.md`) :
1 152 px pour la planche, 552 pour l’appui, 300 pour la vignette.

### ✅ Exécutée le 2026-08-16 — recette tenue sur les six critères

| Critère | Seuil | Mesuré |
|---|---|---|
| Apostrophes droites dans les 23 `planche.json` | 0 | **0** (1 330 courbées) |
| Apostrophes droites dans les `<text>` des 69 SVG | 0 | **0** (178 courbées) |
| Apostrophes droites dans les `aria-label` des 69 SVG | — | **0** (186 courbées) — *le critère qui portait l’enjeu d’accessibilité ne figurait pas au tableau* |
| Régénération octet à octet | 23 / 23 | **23 / 23** — second passage intégralement stable |
| Rendu de la planche à 1 152 px, de l’appui à 552, de la vignette à 300 | inchangé hors apostrophes | **9 bandes d’écart sur 5 200 lignes de pixels** : 3 bandes de 30 px = les cartouches élargis (voulu), 6 bandes de 3 à 13 px = les glyphes d’apostrophe |
| Build | vert | **vert**, `astro check` 0 erreur 0 avertissement |

Restent 3 596 apostrophes droites dans les SVG : ce sont les
`font-variation-settings="'wdth' …"` et `font-family='…'`. **De la syntaxe, pas du
texte** — les courber casserait le rendu des polices.

#### Les trois chiffres du constat ne se reproduisent pas — et le dépôt n’a pas bougé

| Grandeur | Annoncé par le relevé | Mesuré | Écart |
|---|---|---|---|
| Apostrophes dans le texte dessiné des SVG | 205 | **178** | −27 |
| Apostrophes dans les extractions | 1 325 | **1 330** | +5 |
| Planches à régénérer | 14 | **20** | +6 |

Le préambule de cette programmation prévoit le cas : « s’ils divergent du dépôt, c’est
le dépôt qui a bougé depuis `d3bd8d9` ». **Vérifié : il n’a pas bougé.** Remesuré à
`d3bd8d9` même, le corpus donne 178 / 186 / 1 330 — les chiffres d’aujourd’hui. Les
deux premiers écarts viennent donc de la méthode du relevé, qu’on ne peut pas
reconstituer : ni le décompte par occurrences ni le décompte par lignes ne donnent 205.

**Le troisième écart, lui, s’explique — et il est instructif.** Les 14 planches
« des 13 et 14 août » sont exactes *au jour de commit* : 8 le 13, 6 le 14. Mais six
des neuf planches versées le 15 ont été composées **avant** que la correction de
`_tronc.mesurer` n’arrive dans la journée (`1b23d48`, planche 21). **La date de commit
n’est pas un indicateur de l’invariant** : seules les planches 21, 22 et 23 se
rejouaient à l’identique. Le seul test valable est de rejouer.

#### ⚠ Ce que la régénération a trouvé — une collision de constantes, pas une somme de contrôle

C’est le vrai gain de la session, et il n’était pas au programme. `tableau-electrique.py`
affecte **`XB0, XB1` deux fois au niveau du module** : ligne 82 pour le mécanisme
`autoconsommation` (la crèche, `420, 1050`) et ligne 582 pour `franchissement`
(Marans, `56, 930`). Les deux affectations s’exécutent à l’import, **la seconde
gagne**, et c’est le **premier** dessin qui se recompose faux.

Rejouée, la planche de la crèche sortait avec sa barre de distribution partant de 56
au lieu de 420, deux flèches pointant à x 46 — hors de la marge de 56 — et un bloc de
contrôle qui annonçait des largeurs **négatives** (`étiquette surplus : 110 px pour
-190 px`). Huit lignes de SVG déplacées.

Rien ne le signalait : ni le build, ni `astro check`, ni le rendu de Marans, qui était
juste. La planche publiée l’était aussi — elle avait été composée quand la seconde
affectation n’existait pas encore. **Le défaut n’était visible nulle part ailleurs que
dans la régénération**, c’est-à-dire dans le contrôle même que le constat 2 déclarait
rompu. C’est la démonstration de ce à quoi sert l’invariant : il ne garde pas des
sommes de contrôle, il garde la capacité de refabriquer.

Correction : le second mécanisme nomme désormais ses repères `XBARRE0` / `XBARRE1`, à
l’image de `Y_BUS` / `Y_BARRE` que le fichier distinguait déjà. Un balayage des sept
compositeurs — toute constante affectée plus d’une fois au niveau du module — ne
trouve **aucune autre collision** : les autres fichiers préfixent leurs repères par
mécanisme.

#### La portée a été réduite à l’apostrophe, et c’est mesuré

Le constat renvoyait à `scripts/injection-typographique.py`, « qui n’a simplement
jamais été passé sur `public/images/projets/` ». Passé tel quel, il change **1 186
signes de plus** que les apostrophes — des insécables. Or les compositeurs **mesurent**
leurs chaînes pour poser la géométrie (`_tronc.mesurer`) : chaque insécable ajoutée
déplace le dessin, sur 23 planches à recetter au rendu. La recette de cette session dit
« inchangé hors apostrophes » : les deux ne tiennent pas ensemble.

**Les insécables des extractions restent donc ouvertes** et deviennent un chantier à
part entière — voir les points ouverts ci-dessous.

L’instrument est `scripts/apostrophes-planches.py`, rejouable, qui sert de contrôle
autant que de correcteur (`--appliquer` pour écrire, sans argument pour mesurer).
Son garde-fou fait le vrai travail : **une apostrophe n’est courbée que si elle est
française** — une lettre à gauche, une lettre ou un guillemet ouvrant à droite. Tout
le reste est refusé et nommé. C’est ce qui protège la syntaxe qui emploie la même
touche, et le piège n’est pas théorique : en Python 3.11 une f-string est **un seul
jeton**, si bien que `f"{d['cle']}"` porte ses apostrophes de syntaxe à l’intérieur du
littéral. **302 refus**, tous examinés, tous légitimes : clés de dictionnaire,
`'wdth'`, `font-family='…'`.

#### La preuve que l’ordre a été respecté

Le piège annoncé — régénérer avant de corriger efface la correction — se contrôle
autrement que par la parole. Les 23 dossiers ont été régénérés **une première fois
avant toute correction**, dans une copie hors dépôt. Le corpus final, comparé à cette
copie **apostrophes neutralisées**, donne **zéro écart** : la passe typographique n’a
déplacé aucun dessin, et la régénération n’a effacé aucune apostrophe.

#### Trois points ouverts, laissés en l’état et documentés

1. **`logements-pas-des-boeufs` : deux textes 4 px plus larges que leur colonne.**
   `détail pac-air-air 2 : 228 px pour 224 px`, et son jumeau `pac-air-eau 1`. Le
   défaut est **antérieur** — le SVG n’a pas bougé — mais l’ancienne mesure le
   cachait : elle comptait les insécables du mono aux avances d’Archivo. Le bloc
   `depassements` de l’extraction le dit maintenant. Non corrigé ici : le réparer
   demande de recomposer une planche, ce que la recette de cette session interdit.
2. **`core.autocrlf` vaut `true` et le dépôt n’a pas de `.gitattributes`.** Les 92
   pièces sont en LF dans cette copie de travail, et l’invariant y tient. **Il ne
   tiendrait pas dans un clone neuf** : git y écrirait des CRLF, les compositeurs
   réécriraient du LF, et la régénération afficherait 92 écarts qui n’en seraient pas.
   Le contrôle de l’invariant doit donc porter sur une copie écrite par Python, ou
   normaliser les fins de ligne avant de comparer.
3. **`scripts/planches/verser.py` contrôle deux choses qui n’existent plus** : une
   « forme de repli mobile » (retirée le 2026-08-15 avec le repli lui-même) et un
   champ `image_principale` (supprimé du schéma le même jour). Un garde-fou qui
   survit à son objet est un contrôle qui ment — même principe que l’amendement A9.
   Renvoyé à S4, dont c’est exactement le périmètre.

---

## S3 — Les trois défauts de rendu

> **Rang 4 du relevé.** Trois défauts localisés et déjà diagnostiqués ; deux touchent
> le même écran, et aucun ne demande d’arbitrage technique.

### Les trois constats, avec leur cause

**Le CLS de l’accueil est au double du seuil que le projet s’impose.** 0,098 mesuré
pour un plafond de **0,05** inscrit aux critères de blocage ; 0,057 sur l’index des
références. Le décalage vient d’**un seul bloc**, déjà identifié :

```
main#contenu-principal > section.py-16 > div.max-w-[1200px] > div.mt-8   — score 0,0984
```

**Le débordement de l’accueil à 390 px — la cause, cette fois.** Le symptôme était
connu (mémoire `debordement-horizontal-accueil`), la cause ne l’était pas. Deux
éléments débordent, pour la même raison :

```
/ à 390 px :  clientWidth=390  scrollWidth=405
h1.type-display  +31 px   (mot le plus long : 389 px dans une boîte de 358)
p.releve-chiffre +18 px   (« +1 686 » : 148 px dans une colonne de 130)
```

Les deux tiennent à la **borne basse d’un `clamp()`** — 3 rem pour la vedette,
2,5 rem pour le relevé — jamais validée à 390 px avec les chasses 118 et 125. Aucune
autre page ne déborde, à aucune des trois largeurs testées.

**Les cibles tactiles de la page Contact.** Les liens de téléphone et de courriel
passent sous 44 × 44 px ; la page plafonne à 97 d’accessibilité. La recette `.cible-44`
**existe déjà** dans `global.css` — elle n’est appliquée que dans `PlancheReference`.
Le relevé souligne l’ironie : *c’est précisément là où elle manque que la cible est la
plus utile — sur un téléphone, devant un numéro de téléphone.*

### ⚠ La recette d’accessibilité de cette session dépend de D1

La règle exige **100/100** en accessibilité sous peine de blocage. L’accueil plafonne
à **96** pour une raison qui n’est pas dans le périmètre de cette session (le
complément clair d’un titre de section, voir D1). Deux conséquences :

- **la recette a11y de l’accueil est suspendue à D1** — viser 100 avant l’arbitrage,
  c’est viser une cible que le relevé démontre inatteignable ;
- **la recette a11y de Contact, elle, ne dépend de rien** : 97 → 100 par la seule
  application de `.cible-44`.

### Critères de recette

| Critère | Seuil | Instrument |
|---|---|---|
| CLS sur `/` | **< 0,05** | Lighthouse mobile |
| CLS sur `/references/` | **< 0,05** | Lighthouse mobile |
| `scrollWidth` de `/` à 390 px | **= `clientWidth`** | mesure en iframe |
| Débordement des 14 autres routes | inchangé — aucun | balayage 15 routes × 3 largeurs |
| Accessibilité de `/contact/` | **100** | Lighthouse |
| Accessibilité de `/` | selon D1 | Lighthouse |

⚠ **Deux pièges de mesure propres à cette machine**, tous deux en mémoire :
Chrome refuse toute fenêtre sous 500 px — les mesures à 390 px passent par une
**iframe servie en même origine** ; et `browser_resize` de Playwright **persiste** d'un
appel à l'autre, ce qui fait passer une page saine pour cassée.

⚠ **Troisième piège, relevé le 2026-08-16 et absent de la mémoire : la barre de
défilement de l'iframe mange 15 px.** Une iframe de 390 px donne un document de
**375**, soit une mesure 15 px plus sévère qu'un vrai téléphone, où la barre est en
surimpression. Le probe doit s'élargir jusqu'à ce que `contentDocument.
documentElement.clientWidth` vaille exactement la largeur visée — sans quoi on
corrige un débordement qui n'existe pas, ou on en manque un de 15 px.

### ✅ Exécutée le 2026-08-16 — recette mesurée sur le déploiement

| Page | perf | FCP | LCP | CLS | a11y |
|---|---|---|---|---|---|
| `/` | 97 → **100** | 1,7 → **1,2 s** | 1,69 → **1,68 s** | **0,098 → 0** | 96 → 96 *(D1)* |
| `/contact/` | 100 → **100** | 1,5 → **1,1 s** | 1,5 → **1,5 s** | **0,031 → 0** | **97 → 100** |
| `/references/` | 98 → **99** | 1,8 → **1,1 s** | 1,8 → **1,7 s** | **0,057 → 0** | 100 → 100 |
| `/equipe/` | 100 | — | — | **0** | 100 |

Trois relevés de contrôle sur l'accueil : perf 100 / 100 / 100, LCP 1 673 / 1 683 / 1 688 ms,
CLS 0 à chaque fois. **Tous les seuils du projet sont tenus** — CLS < 0,05, LCP < 1,8 s,
performance ≥ 90 — et le FCP gagne 0,4 à 0,7 s sur toutes les pages, effet de bord du
préchargement.

#### ⚠ Le CLS n'était pas un défaut de mise en page

Le plan l'imputait à « un seul bloc, déjà identifié » en citant le sélecteur que
Lighthouse affiche. **C'est le bloc qui a bougé, pas celui qui l'a poussé** : un
décalage s'impute toujours à la victime. Le sous-tableau `layout-shifts` nomme la
cause — `cause: "Web font loaded"`, sur les trois fontes — et `unsized-images` est
vide. Un seul décalage sur la page, entièrement dû au FOUT.

La vedette est composée en `font-stretch: 125%`, un axe `wdth` que la police de repli
système ne possède pas : l'écart de chasse au moment du swap est donc maximal, le
titre change de nombre de lignes, et tout ce qui suit descend. C'est pourquoi
l'accueil était la pire page du site sur ce critère — la seule qui porte une vedette.

Correction : **préchargement des trois fontes du chemin critique**, résolues par
`?url` pour suivre les hachages de build. Contrôlé que le fichier préchargé est bien
celui du `@font-face` (hachage identique, une seule copie dans `dist/`) — précharger
une copie que personne n'utilise ne se signale nulle part. `crossorigin` est
obligatoire même en même origine.

#### ⚠ La recette `.cible-44` ne convenait pas — premier cas où elle ne compose pas

Le plan prévoyait de l'appliquer. Son `::after` est un **calque de 44 px centré** :
sur deux liens distants de 22 px, les calques se chevauchent sur la moitié de leur
hauteur, et toucher le haut de l'adresse déclencherait l'appel téléphonique. Ce sont
donc les **boîtes** qui font 44 px, ce qui garantit l'espacement en même temps que la
taille. À noter pour tout futur emploi : `.cible-44` vaut pour une cible **isolée**,
pas pour des cibles empilées.

#### ⚠ Deux constats hors périmètre, relevés au passage

1. **Le footer porte les mêmes liens à 17 px, espacés de 29** — sur les 46 pages.
   `axe` ne les signale pas (l'exception d'espacement de WCAG 2.2 joue à partir de
   24 px), donc le défaut n'apparaît dans aucun score ; mais la règle FT2E dit
   **44 × 44 pour tout élément actionnable**, sans exception d'espacement. C'est un
   écart règle/code, pas un écart outil.
2. **40 px de vide mort sous `sm` dans le hero de l’accueil** : le média est
   `hidden sm:block`, mais sa cellule de grille et le `gap-10` du conteneur restent.
   Sans effet sur le CLS ni sur le débordement.
   ✅ **Corrigé en S5** le 2026-08-16 (`c6f7c53`) — et le diagnostic ci-dessus était
   juste à un mot près : ce n’est pas le `gap-10` **et** la cellule, c’est le
   `gap-10` **parce que** la cellule. Voir la section S5.

---

## S4 — Hygiène documentaire et garde-fous

> **Rangs 6, 7 et 8 du relevé.** Aucune dépendance, aucun risque, aucun arbitrage.
> Regroupés parce que le coût de contrôle est le même pour un bloc que pour trois.

| № | Objet | Détail mesuré |
|---|---|---|
| 1 | **L’hôte, dans cinq documents** | `docs/09`, `docs/14`, `docs/19`, `docs/20-pistes` et les commentaires de `robots.txt` et `BaseLayout.astro` nomment `ft2e-site.vercel.app`. L’opérationnel est juste (`config.yml`, remote git → `ft2e-v3`). **Le risque est concentré sur `docs/19-migration-production.md` : c’est le runbook de mise en production, il nommera le mauvais hôte au moment précis où on l’exécutera, redirections 301 comprises.** |
| 2 | **Garde-fou `MILLESIME_LIVRAISON_ANNONCE`** | La constante vaut 2026 et sera **fausse sur quatorze affaires au 1ᵉʳ janvier 2027** — ni le build, ni le typecheck, ni le rendu ne le signaleront. Un test de build qui échoue au-delà de l’année en cours coûte trois lignes et supprime une échéance silencieuse. |
| 3 | **`legendeMedia`, code mort** | Calculé sur quatre lignes dans `references/[...slug].astro`, lu nulle part : c’est la légende de média d’avant les planches, manquée par le nettoyage de clôture. Signalé par le typecheck, avec l’interface `Props` de `PlancheReference` — deux hints sur 82, les deux seuls qui désignent du code réellement mort. |
| 4 | **Quatre valeurs hexadécimales en dur** | Trois dans `Logo.astro`, une dans `TraceFlux.astro`. Les valeurs *sont* celles de la rampe — c’est le chaînage au jeton qui manque, donc la garantie qu’elles suivront la prochaine révision de charte (§ 17, sans réserve). |
| 5 | **Champs image morts des actualités** | `image` et `image_alt` sont déclarés au Zod **et** à Decap pour `actualites`, lus par aucun rendu. Le fichier pointé n’existe pas, le répertoire est vide. **Conséquence de comptage : un des huit marqueurs `[DÉMO]` restants ne peut jamais s’afficher — le compte réel des marqueurs atteignables est de sept**, tous dans les secteurs. Corriger le champ *et* le compte annoncé dans `CLAUDE.md`. |
| 6 | **Fine des milliers du champ `performance`** | ⚠ **Le périmètre déclaré est faux.** Le plan annonçait « sur les 23 fiches » ; la mesure en trouve **quatre** : Dufour (5), Villedoux (4), École des douanes (4), Marans (1). La passe reste à faire, mais elle est bien plus courte qu’annoncé. |

⚠ Toute suppression de champ Zod se répercute dans `public/admin/config.yml` **au sein
du même commit** (règle du sous-agent `content-modeller`).


### ✅ Exécutée le 2026-08-16 — neuf commits, et deux constats que la mesure a déplacés

| № | État | Ce qui a été fait, et ce que la mesure a dit |
|---|---|---|
| 1 | ☑ | Six documents et deux commentaires corrigés (`docs/08`, `09`, `14`, `19`, `20-pistes`, `21`, `robots.txt`, `BaseLayout.astro`) — **six, pas cinq** : `docs/21` portait quatre occurrences que le relevé n’avait pas vues. **⚠ Voir le constat A ci-dessous : la vérification de l’hôte a trouvé bien plus qu’une faute de frappe.** |
| 2 | ☑ | Garde-fou posé dans `src/lib/projets.ts`, **échec dur** (arbitrage retenu contre l’avertissement). Recette par échec provoqué : constante ramenée à 2025 → `npm run build` sort en code 1 avec le message attendu ; remise à 2026 → code 0 |
| 3 | ☑ | `legendeMedia` retirée, et `surface_m2` avec elle (seul consommateur). **Mais le second hint n’était PAS du code mort** — voir le constat B |
| 4 | ☑ | Six valeurs (cinq distinctes) chaînées par **classes Tailwind littérales**, pas par `var()` en attribut — voir le constat C. Rendu identique au pixel près (même MD5 sur 1440 × 3000) |
| 5 | ☑ | `image` / `image_alt` retirés du Zod **et** de Decap dans le même commit, frontmatter nettoyé, compte des `[DÉMO]` corrigé à **sept** dans `CLAUDE.md` |
| 6 | ☒ | **Sans objet : le défaut n’existait pas.** Les quatorze groupes de milliers portaient déjà U+202F, et ils le portaient **au commit du relevé lui-même** (`d3bd8d9`), vérifié fiche par fiche. Les chiffres « Dufour (5), Villedoux (4), École des douanes (4), Marans (1) » comptaient les groupes du corpus, pas les écarts — un dénombrement de la **population** lu comme un dénombrement du **défaut**. L’écart réel était ailleurs : trois U+00A0 dans le récit de l’abbaye, corrigés. Le corpus porte 203 séparateurs, tous en fine |
| S2-a | ☑ | `verser.py` : les deux contrôles périmés retirés ; le versement devient une **insertion après `mission_ft2e:`**, ancre relevée sur 23 fiches / 23. Recette sur les deux chemins |
| S2-b | ☑ | `.gitattributes` posé (`* text=auto eol=lf`). **Défaut reproduit avant correction** : clone neuf → 92 pièces sur 92 en CRLF ; après → 92 sur 92 en LF, PNG intacts octet pour octet |
| S3-a | ☑ | Cibles du pied portées à 44 px — **douze, pas deux** (7 liens de plan du site, 2 coordonnées, 3 mentions légales). Par la **boîte**, jamais par `.cible-44`. Zéro sous 44, zéro chevauchement, aucun débordement à 390 / 768 / 1440 ; a11y `/contact/` à 100 |
| S3-b | ☑ | **Reporté en S5**, et corrigé le 2026-08-16 (`c6f7c53`) : les 40 px de vide mort sous `sm` dans le hero de l’accueil |

**Commits** : `7cf8918` · `4ed3e6b` · `e8e3b69` · `348de96` · `0d8b0e8` · `270f93d` · `6e74910` · `d7e5cfc` · `5c0cc69`.

#### Constat A — deux déploiements résiduels servent encore les photographies d’ouvrages

C’est le résultat le plus important de la session, et il ne figurait à aucun rang
du relevé. En vérifiant **lequel** des deux hôtes était le bon, la mesure a montré
que `ft2e-site.vercel.app` (la v1) **et** `ft2e-v2.vercel.app` répondent tous deux
`200` et servent encore leur site, avec les visuels que le chantier des planches
avait retirés de la v3 pour motif de droit d’auteur — huit distincts sur la seule
page `/references`, de 819 à 937 Ko, servis en `200`.

**Cela déplace la question 2 de D2.** Elle posait l’exposition résiduelle comme un
problème d’**historique git**, dont la levée coûterait une réécriture invalidant
tous les SHA cités dans les plans et les règles. L’exposition la plus directe n’est
pas archivée : elle est **servie en HTTP à qui connaît l’URL**, et se lève en
supprimant deux déploiements — coût nul. Les deux sont `noindex` et `Disallow: /`,
ce qui empêche le référencement mais pas l’accès, et ce verrou est justement pensé
pour être levé un jour. Consigné en **§ 6 bis de `docs/19-migration-production.md`**,
avec la procédure et le contrôle par `curl`.

#### Constat B — le hint `Props` désignait un contrat débranché, pas du code mort

Le relevé rangeait les deux hints ensemble, comme « les deux seuls qui désignent
du code réellement mort ». Ils disaient l’inverse l’un de l’autre.

Sonde, avec témoin : un `variante="VALEUR-INVALIDE"` chez `CarteProjet`, et un
appel de `PlancheReference` **sans son `src` requis**, passaient tous deux le
typecheck sans une erreur — là où le même essai sur `HeroPage` en lève une.
`Astro.props` y retombait sur `Record<string, any>` : les **deux** appelants du
composant n’étaient pas contrôlés du tout. Supprimer l’interface, comme le
prévoyait la programmation, aurait entériné l’absence de contrôle.

⚠ **La cause n’est pas caractérisée, et deux explications plausibles ont été
écartées par la mesure.** Une première rédaction de ce constat attribuait le défaut
au bloc de commentaire de 71 lignes intercalé entre les imports et l’interface. C’est
faux : `MarqueOpqibi` porte 3 771 signes de commentaire au même endroit et
`CarteProjet` a le motif exact — trois imports, puis 548 signes de commentaire, puis
l’interface — et les deux sont correctement typés, sondés un par un. Ni la nature
JSDoc (le passer en `/*` ne changeait rien), ni une balise `<img src>` citée dans le
commentaire (injectée dans `CarteProjet`, sans effet) ne rendent compte du défaut.

**Ce qui est établi, et qui suffit :** retirer le bloc réparait, remonter l’interface
au-dessus répare aussi, et c’est la seconde solution qui est en place. Le composant
était le SEUL atteint — `ts(6196)` n’a flambé que sur lui, et trois sondes
indépendantes (`HeroPage`, `MarqueOpqibi`, `CarteProjet`) confirment que les autres
sont branchés. La recette est écrite au-dessus de l’interface : une valeur invalide
dans le `variante=` de `CarteProjet` doit rendre une erreur `ts(2322)`.

**À retenir au-delà de ce fichier :** `ts(6196)` sur une interface `Props` ne dit
jamais « code mort » — il dit « contrat non consommé », ce qui est l’inverse d’un
surplus. Et une sonde de typage se fait en REMPLAÇANT un attribut, jamais en en
ajoutant un second : un attribut dupliqué ne lève aucune erreur, et la première
version de cette vérification a conclu à tort que `MarqueOpqibi` était atteint.

#### Constat C — pourquoi des classes et non `var(--color-…)`

Tailwind v4 **élague les variables de thème qu’aucune classe n’emploie** : mesuré,
le CSS produit ne porte aucune des couleurs par défaut de Tailwind, et exactement
les treize de la rampe. Un `var()` écrit dans un attribut SVG échappe au scan : le
monogramme aurait dépendu d’un autre composant employant `text-voile` ailleurs sur
la page, et aurait perdu ses couleurs le jour où celui-ci change — **sans un mot du
build** (même famille que la règle 11). Les huit classes ont été contrôlées
présentes dans le CSS produit, chacune résolvant bien sur son jeton.

`_tronc.py` reçoit une note : sa table `JETON` est le **miroir nécessaire** du bloc
`@theme` — une planche est lue hors du site (PNG, impression, `og:image`) et ne peut
pas résoudre `var()`. Une révision de charte s’y répercute donc aussi, et les 23
dossiers se régénèrent.

#### Ce que trois de ces points ont en commun

Les rangs 6, 3 et le constat A tiennent le même enseignement : **un relevé de dette
se vérifie avant d’être exécuté.** Le rang 6 comptait une population pour un
défaut ; le rang 3 rangeait un contrat débranché avec du code mort ; le rang 1
nommait une faute de frappe là où il y avait une exposition vivante. Aucun des
trois n’était un mensonge : chacun était une lecture plausible d’une mesure qui
n’avait pas été poussée d’un cran.

---

## D1 — Arbitrage : A2 contre le 100 de Lighthouse

> **Rang 5.** Décision, pas travail. **À poser dès l’ouverture de S1**, pour être
> tranchée avant la recette de S3.

### Le constat de gouvernance

La règle d’accessibilité exige **100/100 sous peine de blocage**. La dérogation **A2**
autorise un complément de titre à **1,54:1**, à condition qu’il porte `aria-hidden`.
Les deux sont respectées à la lettre — et l’accueil plafonne pourtant à **96** : `axe`
signale le contraste dès qu’il peut résoudre le fond, et `aria-hidden` ne l’en dispense
pas.

**Le plus gênant n’est pas l’échec, c’est le succès des autres pages.** Le seul
complément détecté est celui de la section 07, posé sur un **aplat calcaire**. Les six
autres compléments de la même page échappent à la détection parce que sur le papier
tramé, le `background-image` de la trame empêche `axe` de résoudre la couleur de fond,
et l’outil s’abstient. **Ils ne sont pas plus conformes — ils sont seulement moins
mesurables.** Le 100 des autres pages mesure la trame, pas le contraste.

### Les trois issues — aucune n’est technique

| Issue | Ce qu’elle coûte | Ce qu’elle admet |
|---|---|---|
| Retirer le complément des sections posées sur aplat | une passe de gabarit | que A2 ne vaut que sur fond tramé |
| Inscrire l’exception dans la règle et viser **96** sur l’accueil | une ligne de règle | que le critère de blocage n’était pas tenable tel qu’écrit |
| Porter le complément à une valeur qui passe le seuil | une passe de charte | **l’abrogation de A2** |

**Ne rien décider laisse en place un critère de blocage que personne ne peut
satisfaire — et c’est ainsi qu’un critère cesse d’être appliqué.**

### ✅ Tranché le 2026-08-16 — issue 2 : inscrire l’exception, viser 96

**Décision.** A2 est maintenue telle quelle. `.claude/rules/accessibility-rgaa.md`
reçoit l’exception : l’accueil est **reçue à 96** dès lors que la seule violation
`axe` est un `color-contrast` portant sur un complément de titre `aria-hidden`.
**Le critère 100/100 reste opposable à toute AUTRE violation** — c’est ce qui
empêche l’exception de devenir une porte ouverte.

Ce que la décision admet, et qu’il faut assumer par écrit : le critère de blocage
n’était pas tenable tel qu’il était rédigé. Ce que la décision refuse : faire
dépendre A2 du fond sur lequel le titre est posé (issue 1), ce qui aurait produit
une règle redécouverte à chaque nouveau gabarit ; et abroger A2 en assombrissant le
complément (issue 3), ce qui l’aurait fait cesser d’être un décor.

⚠ **À retenir pour la recette de S3** : viser 96 sur l’accueil, 100 ailleurs, et
**nommer la violation attendue** dans le compte rendu. Un 96 non expliqué est
indistinguable d’une régression.

⚠ Le constat du relevé reste vrai et n’est pas levé par la décision : **le 100 des
autres pages mesure la trame, pas le contraste.** Six compléments sur sept échappent
à `axe` parce que le `background-image` de la trame l’empêche de résoudre le fond.
Ils ne sont pas plus conformes — seulement moins mesurables.

---

## D2 — Trois questions à poser à FT2E

> **Rang 9.** Aucune n’est décidable depuis le dépôt.

| Question | Ce qu’elle demande | Pourquoi elle ne peut pas attendre indéfiniment |
|---|---|---|
| **Réception de la crèche de l’Oranger** | une pièce | ⚠ **Le défaut est devenu invisible.** La ligne `statut` a disparu du frontmatter, donc le défaut livré du schéma s’applique : la fiche annonce une affaire livrée **sans dire quand**, et plus rien dans le fichier ne signale l’anomalie. C’est la seule des 23 dans ce cas. |
| **Les 25 visuels dans l’historique git** | un arbitrage | Le site ne les sert plus ; le dépôt les porte encore. Effacer l’exposition du dépôt lui-même demande une **réécriture d’historique qui invalide tous les SHA** — y compris ceux cités dans les plans et les règles. |
| **`planche-chiffree`, jamais écrit** | un arbitrage | Seul archétype du protocole que le chantier n’a pas exercé, donc **le seul dont rien ne garantit qu’il fonctionne**. Le retirer de la liste fermée, ou redéfinir ce qu’il montre. |

---

## S5 — Les suites : le dernier point ouvert, et l’attente de FT2E

> **Session de suites, le 2026-08-16.** Le chantier de réduction de dette est clos ;
> cette session solde ce qu’il laissait derrière lui. Elle avait deux contenus
> possibles selon que les réponses de FT2E soient arrivées ou non.

### Ce que FT2E a répondu : rien, à ce jour

Les trois questions de D2 ont été posées le 2026-08-16 et **aucune n’a reçu de
réponse**. Les trois points qui en dépendent sont donc **laissés strictement en
l’état** — c’est la consigne, et elle est plus forte qu’une préférence :

| Point | État au 2026-08-16 | Ce qui a été fait |
|---|---|---|
| **Les deux déploiements résiduels** | `ft2e-site.vercel.app` et `ft2e-v2.vercel.app` répondent **toujours `200`** — remesuré en ouverture de session | **Rien supprimé.** Ce sont les déploiements de FT2E, la décision leur appartient, et la CLI Vercel répond « Not authorized » sur cette machine de toute façon |
| **Réception de la crèche de l’Oranger** | `annee_livraison` toujours vide, `statut` toujours absent du frontmatter | **Aucun millésime fabriqué.** Un millésime inventé serait indistinguable d’un millésime relevé — c’est précisément ce que la règle 10 interdit |
| **L’archétype `planche-chiffree`** | toujours dans la liste fermée du protocole, toujours jamais exercé | **Rien retiré.** Retirer un archétype est un arbitrage éditorial, pas une opération d’hygiène |

**Ne pas confondre « laissé en l’état » et « oublié ».** Les trois repartent
intégralement dans le prompt de la session suivante (annexe E).

### Point 4 — les 40 px de vide mort du hero : corrigé, mesuré

Le seul point de S3 resté ouvert. Le diagnostic de S3 nommait deux causes — « sa
cellule de grille **et** le `gap-10` du conteneur restent » — là où il n’y en a
qu’une, et la nuance décide de la correction : c’est le `gap-10` **parce que** la
cellule. Une cellule de grille de hauteur 0 est invisible, mais elle ouvre une
seconde rangée, et une seconde rangée se paie son `row-gap`.

**Mesuré avant correction, à 390 px :** `grid-template-rows: 247,375px 0px` pour un
`row-gap: 40px` — **40,00 px** de vide entre le bouton « Nos références » et la
section 01.

#### La correction, et pourquoi celle-là

Deux formes possibles, qui ne rangent pas la connaissance du point de rupture au
même endroit :

| Forme | Ce qu’elle fait | Ce qu’elle laisse |
|---|---|---|
| Neutraliser le `row-gap` sous `sm` | le conteneur compense | la rangée fantôme, **et le `sm` écrit à deux endroits** |
| **Retenue** — masquer l’enveloppe du slot | la cellule n’existe plus | le `sm` écrit **une seule fois** |

`Hero.astro` porte désormais le `hidden sm:block` sur l’**enveloppe** du slot, et
`index.astro` cesse de le porter sur les deux enfants qu’il y range. Le **motif** du
masquage — l’appui composé pour 552 px tomberait à l’échelle 0,62, mono de 10 rendu
à 6,2 px, sous le plancher de 6,5 — reste écrit chez l’appelant, qui compose le
média ; le **point de rupture**, lui, n’existe plus qu’à un endroit.

C’est la règle que ce dépôt réapprend à chaque session : deux exemplaires d’une même
donnée, et c’est la copie qui dérive. Ici la copie n’avait même pas dérivé — les deux
fichiers étaient justes **pris séparément**. Le défaut vivait dans l’écart entre eux,
ce qui explique qu’aucune relecture ne l’ait vu.

#### Recette

| Largeur | Avant | Après |
|---|---|---|
| 390 px | `grid-template-rows: 247,375px 0px` · vide mort **40,00 px** · hero 625,88 px | `247,375px` · vide mort **0,00 px** · hero **585,88 px** |
| 480 px | — | une seule rangée · vide mort **0,00 px** |
| 640 px | hero 1 052,31 px | hero **1 052,31 px** — inchangé au centième |
| 1 280 px | — | hero **1 006,72 px** · deux colonnes · vide mort **0,00 px** |

`scrollWidth` = `clientWidth` aux quatre largeurs : aucun débordement introduit.
Rendu contrôlé par capture à 390 px réels. `npm run typecheck` : 0 erreur,
0 avertissement. `npm run build` : 46 pages.

⚠ **Un quatrième piège de mesure, à ajouter aux trois de S3 : Chrome refuse les
fenêtres sous 500 px EN HEADLESS AUSSI.** Une capture directe en
`--window-size=390,900` ne rend pas une page de 390 px : elle compose la page à
~500 px puis **rogne l’image à 390**. Le résultat montre un texte coupé au bord
droit — c’est-à-dire un débordement parfaitement crédible, et parfaitement faux, sur
une page dont la sonde venait de mesurer `scrollWidth == clientWidth`. La sonde en
iframe calibrée reste le seul instrument valable, et elle n’a rien à restaurer.

### Point 5 — le millésime annoncé : rien à faire, et c’est la bonne réponse

`MILLESIME_LIVRAISON_ANNONCE` vaut **2026**, nous sommes en **2026**, et le garde-fou
posé en S4 échoue en dur au-delà. Vérifié sur pièce : le `throw` est bien en place
dans `src/lib/projets.ts`, il compare `new Date().getFullYear()` à la constante, et
son message ordonne les trois opérations dans le bon sens — relever les réceptions
auprès de FT2E, renseigner les `annee_livraison`, **puis** porter la constante.

**Il n’y a donc rien à exécuter, et surtout rien à anticiper.** Pousser la constante
maintenant reviendrait à désarmer le garde-fou quatre mois avant qu’il ne serve, pour
s’épargner un échec de build qui est exactement ce qu’on lui demande de produire.

### Relevé au passage, hors périmètre et non corrigé

**L’appui du hero est servi au-dessus de sa taille de conception entre `sm` et `lg`.**
Constaté en mesurant le point 4, sur des largeurs que la session n’avait pas de raison
de visiter autrement :

| Fenêtre | Appui rendu | Échelle (dessin composé à 552 px) |
|---|---|---|
| 640 px | 606 px | 1,10 |
| 700 px | 666 px | 1,21 |
| 768 px | 718 px | 1,30 |
| 900 px | 850 px | 1,54 |
| 1 000 px | **950 px** | **1,72** |
| ≥ 1 024 px | 460 à 550 px | ≤ 1,00 — la grille à 12 colonnes reprend la main |

**Ce n’est pas un défaut de lisibilité** — le mono de 10 px y gagne, il monte à 17.
C’est un **épaississement des filets de 1 px**, c’est-à-dire le défaut fondateur que
le chantier des planches a chassé partout ailleurs en plafonnant chaque dessin à sa
taille de conception : la vignette à 300 px dans `CarteProjet`, les trois bandes de
`PlancheReference`. Le hero de l’accueil est le seul endroit du site où un dessin est
encore étiré, et il l’était **avant** cette session — les hauteurs mesurées à 640 et
1 280 px sont identiques au centième avant et après correction.

Non corrigé ici : plafonner l’appui touche à la composition du hero, ce qui déborde
d’un point qualifié de « le moins coûteux du lot ». Reporté au prompt suivant.

---

## S6 — Le plafond du hero, et trois points ajournés

> **Session du 2026-08-16.** Ouverte pour exécuter ce que des réponses de FT2E
> auraient débloqué ; refermée sur le seul point qui ne dépendait de personne.

### Les trois points suspendus : ajournés, et non plus en attente

État revérifié au dépôt et par `curl` en ouverture de session, inchangé depuis S5 :

| Point | Mesure du 2026-08-16 |
|---|---|
| Les deux déploiements résiduels | `ft2e-site.vercel.app` et `ft2e-v2.vercel.app` répondent **toujours 200** sur `/references/`, au même titre que `ft2e-v3` |
| Réception de la crèche de l'Oranger | `annee_livraison` toujours absent, `statut` toujours absent : la fiche annonce une affaire livrée **sans dire quand**, et plus rien dans le fichier ne le signale |
| L'archétype `planche-chiffree` | toujours dans la liste fermée du protocole, toujours cité par sa règle de bascule, toujours jamais exercé |

**Ce qui change est le statut de l'attente, pas son contenu.** Arbitrage rendu en
ouverture de session : le projet n'a pas encore été présenté à FT2E, et les trois
points sont mis en suspens jusque-là.

La conséquence pratique est celle de S5 — rien supprimé, aucun millésime fabriqué,
aucun archétype retiré. La conséquence de méthode diffère : ils ne sont plus en
attente d'une réponse qui tarde, ils sont **ajournés à la présentation du projet**.
Ils repartent au prompt suivant sous cette forme, et non comme une relance.

⚠ **Correction du même jour, après lecture du compte rendu : les deux déploiements
antérieurs sortent du périmètre.** Arbitrage de l'utilisateur, mot pour mot : « Ces
projets antérieurs ne sont plus concernés par quoi que ce soit. On traite la V3 et
uniquement la v3. » Le point est donc **clos, et non ajourné** — il quitte le prompt
de la session suivante, et il ne reste que **deux** points en suspens : la réception
de la crèche et `planche-chiffree`.

Le § 6 bis de `docs/19-migration-production.md` est **conservé mais marqué hors
périmètre**. Il documente un fait vrai, qui redevient opérationnel le jour de la mise
en production — quand les redirections 301 et la levée du `noindex` se poseront — et
ce jour-là seulement. Le supprimer ferait perdre l'information ; le laisser sans son
arbitrage la ferait rouvrir à chaque session, ce que ce dépôt a déjà payé
plusieurs fois.

⚠ **Une seule des trois porte une échéance qui ne dépend pas de FT2E.** La réception
de la crèche est le premier des quatorze relevés qu'appelle
`MILLESIME_LIVRAISON_ANNONCE` : le garde-fou posé en S4 fera **échouer le build au
1ᵉʳ janvier 2027**, et la seule réponse admise est d'aller chercher les réceptions.
L'ajournement est sans coût jusqu'à cette date, et bloquant après.

### Point 4 — l'appui du hero plafonné à sa taille de conception

Le seul point exécutable de la session, et le dernier endroit du site où un dessin
était servi au-dessus de son repère.

#### Ce que la mesure a confirmé, avant et après

Sonde en iframe même origine, sur le `dist/` du commit en cours :

| Fenêtre | Appui avant | Échelle | Appui après | Échelle |
|---|---|---|---|---|
| 640 px | 606,00 px | 1,098 | **550,00 px** | **0,996** |
| 700 px | 666,00 px | 1,207 | 550,00 px | 0,996 |
| 768 px | 718,00 px | 1,301 | 550,00 px | 0,996 |
| 900 px | 850,00 px | 1,540 | 550,00 px | 0,996 |
| 1 000 px | **950,00 px** | **1,721** | 550,00 px | 0,996 |
| 1 024 px | 462,00 px | 0,837 | 462,00 px | 0,837 — inchangé |
| 1 280 px | 550,00 px | 0,996 | 550,00 px | 0,996 — inchangé |

La carte-lien qui légende le dessin suivait sa largeur **au pixel** (952 contre 952 à
1 000 px) : c'est la raison pour laquelle le plafond enveloppe les deux, et non le
seul plan posé.

#### Trois choix d'implantation, dont aucun ne va de soi

| Question | Retenu | Pourquoi |
|---|---|---|
| Sur quoi porte le plafond | le dessin **et** sa carte-lien | plafonner le plan seul laisserait une légende de 950 px sous un dessin de 552 |
| Où il s'écrit | `src/pages/index.astro`, chez qui compose le média | le nombre de colonnes est un réglage de page, la taille de conception une propriété du dessin — même partage que la vignette de `CarteProjet`, dont le plafond vit dans le composant du dessin |
| Comment | CSS de composant (`.appui-hero`), pas `max-w-[552px]` | une classe en valeur arbitraire, unique au dépôt, disparaîtrait sans un mot du build le jour où l'élagage de sources de Tailwind v4 cesserait de voir ce fichier (incident du 2026-08-08) |

**Aucune borne de largeur n'a été nécessaire** : sous `sm` le média entier est masqué
par `Hero.astro`, au-dessus de `lg` la colonne mesure 462 à 550 px et la règle est
sans effet. Elle ne mord qu'entre les deux, ce qui est exactement l'étendue du défaut.

#### Recette

- échelle **0,996 partout de 640 à 1 000 px**, contre 1,10 à 1,72 avant ;
- **rien déplacé ailleurs** : hero **585,88 px à 390 px** et **1 006,72 px à 1 280 px**,
  identiques **au centième** à la recette de S5 — la correction des 40 px de vide mort
  n'est pas touchée. À 640 px le hero passe de 1 052,31 à 1 014,97 px, soit 37,34 px de
  moins : c'est la hauteur que perd l'appui en cessant d'être étiré (368 × 550/552
  contre 368 × 606/552), pas un déplacement ;
- `scrollWidth == clientWidth` sur **neuf largeurs de 360 à 1 440 px** ;
- règle présente dans le HTML produit : `.appui-hero[data-astro-cid-…]{max-width:552px;margin-inline:auto}` ;
- rendu contrôlé par capture à **1 000 px** — la largeur où le défaut culminait — et à
  1 440 px, où rien ne devait bouger et où rien n'a bougé ;
- `npm run typecheck` : 0 erreur, 0 avertissement. `npm run build` : 46 pages.

#### La leçon, remontée dans les règles

L'argument qui avait épargné le hero jusqu'ici — « c'est un ornement de couverture,
pas une figure de fiche » — ne tient pas, et il valait d'être tranché explicitement
plutôt que laissé implicite : **la règle porte sur le filet, pas sur le rôle du
dessin.** La lisibilité *gagnait* à l'étirement, le mono de 10 px montant à 17 ; ce
qui se dégradait est l'épaisseur des filets de 1 px, or la charte fait porter le rang
d'un filet par son **opacité**, ce qui suppose que son épaisseur ne bouge pas. Un
dessin agrandi rend donc tous ses rangs faux à la fois — et c'est vrai d'un ornement
comme d'une figure. Consigné dans `.claude/rules/tailwind-design-tokens.md`
§ Composants signature, à la suite de la vignette et des trois bandes.

### Trouvé au passage : le déploiement a dix-huit commits de retard

`origin/master` est à `ba3cc3b`, relevé par `git ls-remote` et non par la référence
locale, qui pouvait être périmée. Le déploiement `ft2e-v3.vercel.app` est donc à cet
état : il porte S1, S2 et S3, et **ni S4, ni S5, ni S6**. Contrôlé par des marqueurs
du build plutôt que par une date — les huit `type="image/avif"` de `/equipe/` (S1)
**sont** servis, les cibles de 44 px du pied de page (S4) ne le sont **pas**, et la
règle `.appui-hero` de cette session non plus.

**La conséquence pour la session suivante est bloquante** : toute mesure faite « sur
le déploiement » — c'est-à-dire toute mesure de performance, puisque `npm run preview`
ne compresse rien — porterait sur un site vieux de trois sessions. Le push n'a pas été
fait ici : il est sortant, et personne ne l'a demandé. Il doit l'être avant toute
recette de performance, et le contrôle reste le même : un marqueur du build, jamais un
délai d'attente.

### Trois pièges de mesure, dont deux inédits

1. ⚠ **La sonde en iframe voit 15 px de moins que les media queries.** Les `min-width`
   de CSS comptent la barre de défilement, `clientWidth` non : à `clientWidth == 1023`
   la page est **déjà en `lg`**, parce que la viewport CSS vaut 1 038. Les seuils
   relevés par cette sonde sont donc décalés d'une largeur de barre — sans conséquence
   sur une échelle, mais décisif sur une borne. Ne pas conclure « la bascule a lieu à
   1 023 » sur ce seul chiffre.
2. ⚠ **`--user-data-dir` fait échouer `--dump-dom` en silence.** Chrome sort en **code
   0** et n'écrit **rien** — ni DOM, ni message d'erreur. Le même appel sans l'option
   rend le document complet. Cherché du côté de la page et du serveur avant d'être
   trouvé du côté de la ligne de commande.
3. **Des serveurs `astro preview` de sessions antérieures tournent encore** — seize
   ports occupés, plusieurs répondant `200`. Le risque n'est pas celui qu'on croit :
   `astro preview` sert le **disque**, donc tous servent le `dist/` courant, ce qui a
   été vérifié par un marqueur déposé dans `dist/` et relu sur trois ports. Le vrai
   risque est de mesurer **sans avoir rebuild** — un marqueur du build le dit, un
   numéro de port ne dit rien.

---

## S7 — La recette d'ensemble avant présentation

> **Session du 2026-08-16.** Le chantier de dette étant clos et son dernier point de
> rendu soldé, cette session n'exécute pas un programme : elle **mesure l'état du site
> avant qu'il soit montré**, et corrige ce que la mesure trouve. Périmètre défini avec
> l'utilisateur en ouverture, en quatre volets : recette d'ensemble, relecture
> éditoriale, script de démonstration, prise en main du CMS.

### Le constat le plus important : le CMS ne se connecte pas

C'est le seul défaut de cette session qui **empêche quelque chose**, et il ne vit pas
dans le dépôt.

| Mesuré le 2026-08-16 sur le déploiement | Résultat |
|---|---|
| `GET /admin/` | `200` — l'interface Decap s'affiche |
| `GET /admin/config.yml` | `200` — la configuration est servie et à jour |
| `GET /api/auth?provider=github` | **`500`** — « Configuration OAuth manquante : definir `OAUTH_GITHUB_CLIENT_ID` » |

Le bouton **Se connecter** tombe donc sur une erreur serveur. La section C du script de
démonstration — celle que le script lui-même appelle « le moment clé » — ne peut pas
avoir lieu.

**Rien n'est en cause dans le dépôt.** `api/auth.js` et `api/callback.js` sont justes,
`config.yml` pointe le bon dépôt depuis la correction du 2026-08-10. Il manque, hors du
dépôt : `OAUTH_GITHUB_CLIENT_ID` et `OAUTH_GITHUB_CLIENT_SECRET` sur le projet Vercel,
et la callback `https://ft2e-v3.vercel.app/api/callback` sur l'OAuth App GitHub.

⚠ **Ce qu'il faut retenir de méthode, plus que du fait lui-même.** L'avertissement
existait, mot pour mot, **en commentaire en tête de `config.yml` depuis le 2026-08-10** :
« Tant que ce n'est pas fait, la connexion au CMS échoue. » Il a traversé **six
sessions** sans être exécuté ni même relevé. **Un commentaire n'échoue jamais** — il
n'est lu que par qui ouvre déjà le fichier, et pour une autre raison. C'est pourquoi il
est désormais dans `CLAUDE.md`, dans `docs/22` § 0, dans le pré-vol du script de
démonstration, et surtout accompagné d'une **commande de contrôle** qui, elle, se rejoue :

```bash
curl -s -o /dev/null -w "%{http_code}\n" "https://ft2e-v3.vercel.app/api/auth?provider=github"
```

Aucune recette de code ne pouvait le trouver : `npm run build` est vert, `npm run
typecheck` est vert, `/admin/` répond `200`. Il fallait appeler la chaîne
d'authentification.

### La recette mesurée — Lighthouse sur le déploiement, neuf routes, mobile

Le déploiement portait bien le code en cours, contrôlé **avant** de mesurer, en deux
temps : `git ls-remote origin master` (et non la référence locale, qui peut être
périmée) puis le marqueur de build `.appui-hero[data-astro-cid-…]{max-width:552px}`
servi sur `/`.

| Route | Perf | A11y | BP | SEO | LCP | CLS | TBT |
|---|---|---|---|---|---|---|---|
| `/` | **100** | 96 | 100 | 69 | 1 681 ms | 0 | 0 |
| `/societe/` | **100** | 97 | 100 | 69 | 1 686 ms | 0 | 0 |
| `/equipe/` | **100** | **100** | 100 | 69 | 1 807 ms | 0 | 0 |
| `/expertises/` | **100** | **100** | 100 | 69 | 1 681 ms | 0 | 0 |
| `/references/` | **100** | **100** | 100 | 69 | 1 673 ms | 0 | 0 |
| fiche `abbaye-sablonceaux-ssi` | **100** | **100** | 100 | 69 | 1 663 ms | 0 | 0 |
| `/actualites/` | **100** | **100** | 100 | 69 | 1 669 ms | 0 | 0 |
| article de lancement | **100** | **100** | 100 | 69 | 1 527 ms | 0 | 0 |
| `/contact/` | **100** | **100** | 100 | 69 | 1 516 ms | 0 | 0 |

Trois lectures, dont deux qui ne vont pas de soi :

- **Le 69 en SEO n'est pas un défaut.** L'unique audit en échec est `is-crawlable`,
  « Page is blocked from indexing ». C'est le verrou à trois serrures, voulu, et il
  remontera mécaniquement à la levée du `noindex`. Vérifié audit par audit, pas déduit.
- **Le 97 de `/societe/` a fait bouger une règle**, voir ci-dessous.
- **`/equipe/` est AU seuil de LCP, pas sous le seuil.** Quatre tirs : 1 807, 1 815,
  1 658, 1 656 ms pour un budget de 1 800, et une fois 98 en performance. Ce n'est ni un
  échec ni une réussite franche, et une mesure unique n'aurait pas permis de le dire —
  le premier tir seul concluait « 7 ms au-dessus, donc bloqué ». C'est la seule page du
  site dont la performance ne soit pas confortable ; S1 y avait relevé 1,2 s, ce qui
  situe l'écart du côté des conditions de mesure plus que du code.

Contrôles déterministes, tous verts : **211 liens internes, 0 mort** ; **23 numéros
d'affaire, 0 fuite** en HTML lisible ; typecheck 0 erreur ; build 46 pages.

### L'exception D1 était rédigée par page, sa justification portait sur un motif

`/societe/` sort à **97**, et l'exception D1 ne nommait que l'accueil. À la lettre,
c'était donc un blocage. La violation est pourtant **exactement la même et la seule** :
`color-contrast` sur `<span class="text-clair" aria-hidden="true">`, à 1,54 sur calcaire.

D1 avait été rédigé « l'accueil plafonne à 96 » parce que l'accueil était **la seule
page alors mesurée**. Neuf routes plus tard, la formulation par page aurait fait lire un
cas prévu comme une régression. Elle est donc portée sur le **motif**.

Le corollaire, ajouté à la règle parce qu'il vaut pour tout gabarit à venir : **le
complément est signalé exactement là où il est posé sur un aplat plein.** Les deux
violations le sont sur `calcaire` `#edf0f2`, qu'`axe` sait résoudre ; partout ailleurs
le complément repose sur le papier tramé, dont le `background-image` empêche la
résolution, et l'outil s'abstient. Un futur gabarit qui pose un titre de section sur un
aplat fera **baisser son score sans qu'aucune règle du système ait été enfreinte**.

### La relecture éditoriale — ce que la portée des règles avait laissé passer

Le corpus de `src/content/` s'est révélé remarquablement propre : zéro point de
suspension en trois points, zéro tiret double, zéro guillemet droit, zéro `m2`, zéro
`RT 2012`, zéro exclamation, et les insécables autour des « » correctes partout. Le
relevé numéral est inchangé (95/1 · 40/8 · 1/22).

Les écarts étaient **hors de `src/content/`**, c'est-à-dire là où la portée des règles
ne les faisait pas chercher :

| Écart | Où | Servi au visiteur | Levé |
|---|---|---|---|
| Apostrophe droite de l'énumération « Études d'exécution » | énumérations Zod + Decap + 6 fiches | 26 occ., 6 pages, dont le chip de filtre de `/references` | oui |
| Apostrophe droite de la baseline du monogramme | `Logo.astro`, SVG `<text>` | **46 pages**, à côté d'un « Bureau d'études » déjà courbe | oui |
| La même dans l'`aria-label` du monogramme | `Logo.astro` | prononcée par les lecteurs d'écran | oui |
| Espace ordinaire avant `?` et `:` | 4 points de microcopie en composants, dont le CTA des 23 fiches | 27 occ., 25 pages | oui |
| Espace ordinaire avant `:` | un `image_alt` de secteur | 1 occ. | oui |
| Ponctuation du corpus **dessiné** | 12 occ. dans les planches SVG | oui | **non — délibérément** |

**Mesure du texte servi, hors SVG : apostrophe droite 72 → 0, espace ordinaire avant
ponctuation double 39 → 0.** La convention retenue est celle du corpus, relevée et non
décrétée : **U+00A0** avant la ponctuation double (540 occurrences contre une seule
espace ordinaire), **U+202F** entre nombre et unité (541).

Deux points d'arbitrage valent d'être consignés :

- **Les 12 écarts du corpus dessiné ne se corrigent pas ici.**
  `injection-typographique.py` **déplace le dessin** : les compositeurs mesurent leurs
  chaînes pour poser la géométrie, et U+202F n'a pas la chasse d'une espace ordinaire.
  `french-editorial.md` identifiait déjà ce chantier comme ouvert. Un défaut se corrige,
  une dette se programme ; les confondre la veille d'une présentation est la façon la
  plus sûre de casser quelque chose.
- **Les 65 autres apostrophes droites de `config.yml` sont hors périmètre par la règle
  elle-même** : ce sont des libellés d'aide de Decap, et `french-editorial.md` borne sa
  portée au « contenu destiné à l'utilisateur final ». Une aide de saisie s'adresse à
  l'éditeur.

**La charte ne s'opposait pas au redressement de la baseline**, contrairement à ce qu'un
`grep` laissait croire : ses deux pièces comptent **213 et 217 apostrophes droites pour
zéro courbe**. Une décision typographique se manifeste par un **contraste**, un filtre
d'export par une **uniformité** — 100 % / 0 % est la signature du second.

### Le script de démonstration portait quatre erreurs, dont deux cassantes

Il datait d'avant trois chantiers. Il faisait ouvrir **deux fois** « Maison Pierre
Loti », fiche **supprimée le 2026-08-08** ; il annonçait au client « cible : hébergement
souverain français (OVH) » alors que `docs/19` présente le choix comme **non tranché** ;
il décrivait le design comme « Apple-style », soit la charte v1 ; il parlait des
« fiches marquées `[DÉMO]` », dont il ne reste aucune. Et il ne disait **pas un mot des
planches**, qui sont le principal travail des trois derniers mois.

Refait intégralement, avec le blocage OAuth en tête du pré-vol et la conduite à tenir
s'il n'est pas levé le jour J — ouvrir `/admin/` pour buter sur une erreur coûte plus
que de ne pas l'ouvrir.

### La prise en main du CMS — `docs/22`, et ce qu'elle a vérifié au passage

`docs/08` décrit la **configuration** du CMS ; il manquait un mode d'emploi destiné aux
**rédacteurs**. Neuf sections, dont deux pièges qu'un rédacteur ne peut pas deviner : le
numéro d'affaire **se relève sur pièce et ne se fabrique pas**, et le visuel d'une fiche
**ne se téléverse pas** — créer une fiche dont la planche n'existe pas fait échouer la
publication du site entier.

Vérifié et conforme au passage : le champ `photo` de la collection Équipe **surcharge
bien** `media_folder` vers `/src/assets/equipe` (`config.yml` l. 355-356). Un
téléversement Decap atterrit donc là où `astro:assets` le résout, et non dans `public/`
où il ne s'afficherait pas.

### L'incident de la session : un remplacement qui a détruit du contenu, build vert

À consigner parce qu'il a failli passer.

Une passe de correction typographique a écrit ses références arrière `\1` `\2` `\3`
**comme caractères de contrôle** `U+0001` `U+0002` `U+0003` : le double antislash s'est
effondré en simple sur le trajet, et Python a lu `"\1"` comme `chr(1)`. Le texte capturé
n'a donc pas été réinséré, il a été **remplacé**. Trois libellés détruits :

- `index.astro:347` — « 07 — maîtres d'ouvrage » réduit à trois caractères invisibles ;
- `index.astro:351` — « /maîtres d'ouvrage et clients » idem ;
- `societe.astro:240` — « une méthode : elle atteste » idem.

**`npm run build` a produit 46 pages sans broncher.** Astro n'a rien à valider
là-dedans : du texte reste du texte, fût-il invisible. Seul `astro check` a protesté, et
pour une raison **indirecte** — il sérialise l'AST en JSON, qui interdit les caractères
de contrôle nus dans une chaîne. Le garde-fou qui a sauvé la mise n'était pas celui
prévu pour ça.

Trois enseignements, tous vérifiés dans la session :

1. **Une mesure d'absence de défaut ne distingue pas « corrigé » de « supprimé ».**
   L'instrument annonçait « 0 apostrophe droite, 0 ponctuation fautive » — exact,
   puisque le texte fautif n'existait plus **du tout**. Il faut contrôler la **présence
   du texte attendu**, et c'est ce que fait la passe de reprise.
2. **Ne pas faire traverser au canal d'écriture les caractères qu'il normalise — lui
   faire traverser leur recette.** `chr(0xA0)` est strictement plus sûr qu'un littéral
   *et* qu'un échappement : les deux premiers peuvent être réécrits en route, un appel
   de fonction non. L'échappement a échoué **deux fois** avant que ce soit clair.
3. **L'assertion d'auto-contrôle n'est pas une précaution de style.** La normalisation
   des insécables **n'est pas déterministe d'un appel à l'autre** : le même script
   littéral est passé une fois et a échoué la suivante. C'est l'assertion qui a empêché
   la seconde écriture ; le script qui n'en avait pas a détruit du contenu.

Un corollaire de mesure, du même ordre : un instrument dont les insécables ont été
normalisées signale comme **fautives les pages les mieux composées** — parce que
`.replace('&nbsp;', NBSP)` y injecte alors des espaces ordinaires. Deux relevés
intermédiaires de cette session l'ont fait (41 guillemets « fautifs », puis 28
ponctuations), tous deux sur des pages légales écrites au cordeau. **Un instrument qui
ne trouve ses fautes que là où le soin est maximal se dénonce lui-même.**

### Recette de la session

- typecheck **0 erreur, 0 avertissement** ; build **46 pages** ;
- **211 liens internes, 0 mort** ; **23 numéros d'affaire, 0 fuite** ;
- texte servi hors SVG : **0 apostrophe droite, 0 espace ordinaire avant ponctuation
  double** (contre 72 et 39 à l'ouverture) ;
- **présence** du texte attendu contrôlée sur les 10 corrections, et **zéro caractère de
  contrôle** sur les 13 fichiers modifiés ;
- rendu contrôlé par sonde en iframe même origine, serveur apparié à son `dist` par
  marqueur : baseline du monogramme **x 104,0 → 304,1 pour un `viewBox` de 330**, donc
  sans débordement, identique sur sept largeurs ; `scrollWidth == clientWidth` sur
  **neuf mesures de 320 à 1 440 px** ; CTA rendant leur insécable et se repliant
  normalement (285 × 73 à 390 px, 215 × 121 à 320 px) ;
- l'URL `/secteurs/etudes-execution-bim/` **inchangée** malgré le renommage de
  l'énumération, le slug d'un secteur venant du nom de fichier.

⚠ **Poussé le 2026-08-16 sur demande de l'utilisateur** : `8518d49..e6cc9f0`,
six commits. Arrivée du déploiement contrôlée **par marqueur du build et non par un
délai** — l'apostrophe courbe de la baseline, produite par le build et absente de la
version précédente — servie **en une vingtaine de secondes**.

Recette refaite **après** déploiement, sur le code en ligne :

- typographie du **site servi**, 12 routes : **0 apostrophe droite, 0 espace ordinaire
  avant ponctuation double**, baseline courbée sur **12 / 12** pages ;
- le renommage de l'énumération tient en production : `/secteurs/etudes-execution-bim/`,
  `/references/` et la fiche EXE répondent `200`, et le chip de filtre affiche
  « Études d'exécution / BIM **(1)** » — apostrophe courbe **et comptage non nul**, donc
  l'appariement par égalité de chaînes fonctionne toujours. Zéro graphie droite
  résiduelle ;
- Lighthouse, huit routes, mobile : **perf 100 sur six routes et 99 sur deux**, a11y
  **inchangée** (96 / 97 / 100 × 6 — exactement la répartition que prévoit l'amendement
  D1), BP 100, SEO 69, **CLS 0 partout**, TBT 0 sauf 60 ms sur `/equipe/`.

⚠ **Correction d'une lecture de cette même section : le LCP n'est pas un
problème de `/equipe/`.** Le premier relevé concluait « `/equipe/` est la seule page dont
la performance ne soit pas confortable ». Le second l'infirme : `/equipe/` y passe à
1 768 ms, sous le seuil, et c'est **l'accueil** qui tombe à 1 806. Les sept mesures
cumulées sur ces deux pages — 1 656, 1 658, 1 681, 1 768, 1 806, 1 807, 1 815 — se
répartissent de part et d'autre de 1 800 **sans qu'aucune page ne soit systématiquement
du mauvais côté**.

Le constat juste est donc : **le LCP mobile du site est au seuil, pas sous le seuil**,
sur ses deux pages les plus lourdes, et celle qui bascule change d'un tir à l'autre.
Attribuer le dépassement à `/equipe/` enverrait une session future optimiser la mauvaise
page. La fiche projet, elle, descend à **1 068 ms**.

Ce constat, puis l'alignement de l'annexe G sur lui, ont été consignés par deux commits
supplémentaires, poussés dans la foulée. **Aucun décompte n'est donné ici à dessein** :
un document qui cite le nombre de commits d'une session est invalidé par le commit qui
l'écrit, et dérive d'une passe à l'autre. La session part de `8518d49` ;
`git log --oneline 8518d49..master` en donne le contenu exact et reste juste.


---

## S8 — Un blocage qui ne se lève pas depuis le code

> **Session du 2026-08-17.** Elle ne touche pas une ligne de `src/`. Son périmètre a été
> arrêté avec l’utilisateur en ouverture, et il tient en deux décisions : le déblocage
> du CMS est **remis à plus tard**, et **rien d’autre n’est engagé** avant la
> présentation. Ce qui suit est un relevé et une consignation, pas un chantier.

### L’état mesuré à l’ouverture

Trois contrôles, tous rejoués **sur le déploiement** et non sur le disque.

| Contrôle | Instrument | Résultat |
|---|---|---|
| Le dépôt est-il poussé ? | `git ls-remote origin master` | `62fb9ff`, **identique** au HEAD local |
| Le déploiement porte-t-il ce code ? | marqueur de build dans le HTML servi | la baseline du monogramme **à l’apostrophe courbe**, et 46 occurrences d’U+2019 sur `/` |
| La chaîne d’authentification répond-elle ? | `GET /api/auth?provider=github` | **`500`** — « Configuration OAuth manquante » |

Le deuxième contrôle mérite d’être détaillé, parce que c’est celui qu’on est tenté de
sauter. `git ls-remote` prouve que GitHub porte la même chose que le disque ; il ne
prouve **pas** que Vercel a construit depuis. Le marqueur, lui, est un fait du **HTML
servi** : l’apostrophe courbe de la baseline n’existe dans aucun build antérieur au
2026-08-16. Les deux contrôles **ensemble** ferment la chaîne disque, dépôt,
déploiement ; pris séparément, chacun laisse un maillon dans l’ombre. En S6, c’est
exactement là que le site en ligne s’était arrêté **trois sessions en arrière** sans que
rien ne le signale.

### Le blocage a changé de nature, pas d’état

`/api/auth` rend toujours `500`, et c’est le même `500` qu’au 2026-08-16. Il ne faut
pourtant pas lire cette session comme une septième traversée du même défaut.

**Ce qui a changé est le régime du blocage.** Jusqu’au 2026-08-16 il vivait en
commentaire en tête de `config.yml` : personne ne le voyait, personne n’en répondait,
et il se reconduisait tout seul. Il est désormais **relevé à l’ouverture de session par
une commande**, inscrit dans `CLAUDE.md`, dans `docs/22` § 0 et dans le pré-vol du
script de démonstration — et l’utilisateur l’a **explicitement ajourné**. Un défaut
ajourné et un défaut non vu ont le même état et deux natures opposées : le premier a
un propriétaire, le second n’en a pas.

C’est la seule raison pour laquelle cette session ne le traite pas, et ce n’est pas une
tolérance : **les trois gestes sont hors du dépôt** — la callback sur l’OAuth App
GitHub, les deux variables sur le projet Vercel, le redéploiement — et aucun outil de
cette machine ne peut les poser (la CLI Vercel répond « Not authorized », et elle
n’est même pas installée). **Il n’existe aucune correction de code qui approche du
problème.**

⚠ **Ne pas ajouter un avertissement de plus.** Le fait est écrit à quatre endroits ;
il lui manque une exécution, pas une cinquième mention. La seule chose qui se rejoue est
la commande de contrôle.

### Le dépôt a bougé pendant la session, et pas de mon fait

Le contrôle d’ouverture donnait `62fb9ff` des deux côtés. Trois heures plus tard, au
moment de committer, `HEAD` valait `1ad72b5` : **six commits** `chore(deploy)`
s’étaient intercalés et avaient été **poussés** par un hook `Stop`, le travail d’une
session parallèle sur le même dépôt (un script de captures de portfolio,
`scripts/captures/portfolio.mjs`, plus `package.json` et `.gitignore`).

**Rien n’est en cause dans ce qu’ils ont écrit.** Le motif ajouté au `.gitignore` est
**correctement ancré** (`/livrables/captures-portfolio/`) et porte même le
commentaire qui rappelle le piège. Contrôle joué et non déduit : `git check-ignore`
ne rend rien sur les quatre répertoires de pages, les quatre paliers de `grid-cols` sont
bien émis dans le CSS produit, et le site servi est inchangé **à l’octet près** (82 383),
les commits ne touchant pas `src/`.

Deux conséquences de méthode, qui valent plus que l’incident :

- **« Rien n’est en attente de push » est une mesure périssable, pas un état.**
  Elle était juste à l’ouverture et fausse trois heures plus tard, sans que rien ne le
  signale. Un dépôt que se partagent plusieurs sessions, avec un hook qui commite et
  pousse tout seul, se revérifie **au moment de committer** — pas seulement à
  l’ouverture.
- **Un marqueur de build prouve « pas plus ancien que », jamais « exactement ce
  commit ».** L’apostrophe courbe de la baseline est servie aussi bien par `62fb9ff`
  que par `1ad72b5` : elle date le déploiement du 2026-08-16 au plus tôt, elle ne
  l’identifie pas. Pour trancher qu’un déploiement porte **le** commit en cours, il faut
  un marqueur introduit **par ce commit-là**. C’est une limite du procédé de S7, pas un
  défaut de son application.

### Ce que la session n’a pas fait, et pourquoi c’est écrit

Aucun des candidats connus n’a été ouvert — insécables du corpus dessiné,
régénération des vingt planches, marqueurs `[DÉMO]`, LCP au seuil — et les deux
points ajournés (réception de la crèche de l’Oranger, archétype `planche-chiffree`) sont
restés fermés.

Une session dont la sortie honnête est « rien à faire » doit tout de même laisser
une trace, faute de quoi la suivante remesure depuis zéro et croit découvrir. C’est
l’objet de cette section : **elle vaut par ce qu’elle dispense de refaire.**

**Relevé au passage, non traité** : `livrables/cv-ft2e/CV-FT2E.zip` est non suivi dans
un répertoire qui n’est pas ignoré. Sans incidence sur le site — `livrables/` ne sert
pas au build — mais c’est une pièce binaire qui attend une décision : suivre,
ignorer, ou retirer.

---

## Ce que cette programmation ne traite pas

Repris du relevé, et **volontairement laissé ouvert** :

- **L’indexation verrouillée** — triple sécurité cohérente (`robots.txt`, en-tête
  `X-Robots-Tag`, `noindex` par défaut). C’est la cause unique du score SEO de 69 sur
  l’accueil : **un verrou, pas un défaut.** Procédure de levée : `docs/19`.
- **Le formulaire de contact sans backend** — question de périmètre, pas de dette.
- **Decap non pris en main par FT2E** — le code est en place et cohérent ; ce qui
  manque est la prise en main.
- **Les photographies de démonstration** — 8 photos d’équipe et 7 visuels de secteurs
  marqués `[DÉMO]`, qui se lèvent au reportage. ⚠ **Le constat de performance de S1 ne
  se lèvera pas avec eux** : c’est le pipeline qui manque, pas la qualité des images.
- **`associe`, `formation`, `icone`** — renseignés dans 7, 6 et 4 fichiers, affichés
  nulle part, **gardés sciemment** : c’est du contenu sans affichage, pas un champ mort.

---

## Suivi

| Session | État | Commit | Recette |
|---|---|---|---|
| S1 — pipeline d’images | ☑ **faite** le 2026-08-16 | `71cc72f` · `4416c20` · `+1` | ✅ **complète, mesurée sur le déploiement** — `/equipe/` perf **100**, LCP **1,2 s** (seuil 1,8), poids **4 766 → 240 Kio** ; AVIF+WebP+srcset, repli et duotone contrôlés ; `/` sans régression (96) |
| S2 — planches : typo + régénération | ☑ **faite** le 2026-08-16 | `22033a2` · `+1` | ✅ **complète** — **0** apostrophe droite dans les 23 extractions, les 69 `<text>` et les 69 `aria-label` (1 694 courbées) ; régénération **23 / 23** octet à octet ; rendu inchangé hors apostrophes et cartouches (9 bandes de pixels sur 5 200) ; build vert. **Trouvé au passage : une collision `XB0` entre deux mécanismes de `tableau-electrique.py`, qui recomposait faux la planche de la crèche** |
| S3 — trois défauts de rendu | ☑ **faite** le 2026-08-16 | `806e803` | ✅ **complète** — CLS **0** sur `/`, `/contact/`, `/references/` et `/equipe/` (seuil 0,05) ; `/contact/` a11y **97 → 100** ; débordement nul sur 45 mesures (15 routes × 3 largeurs) et à 320 / 360 / 390 / 430 px ; accueil perf **100** |
| S4 — hygiène et garde-fous | ☑ **faite** le 2026-08-16 | `7cf8918` → `5c0cc69` (9) | ✅ **complète** — cinq des six points exécutés, le sixième **sans objet** (la fine des milliers était déjà posée au commit du relevé) ; plus les deux garde-fous de S2 et les cibles 44 px de S3. Garde-fou du millésime recetté **par échec provoqué** ; `.gitattributes` recetté **sur un clone neuf** (92 CRLF → 92 LF) ; rendu identique **au pixel** ; a11y `/contact/` 100. **Trouvé au passage : `ft2e-site` et `ft2e-v2` répondent encore et servent les photographies d'ouvrages** |
| D1 — arbitrage A2 × Lighthouse | ☑ **tranché** le 2026-08-16 — issue 2 (inscrire l’exception, viser 96) | `4416c20` · `806e803` | ✅ **appliqué** à `.claude/rules/accessibility-rgaa.md` en S3 |
| D2 — trois questions à FT2E | ◑ **posées** le 2026-08-16, **toujours sans réponse** au soir du 2026-08-16 (revérifié en S5) | `7cf8918` (§ 6 bis) | ⚠ **La question 2 a changé de nature** : l'exposition des visuels n'est pas seulement archivée dans l'historique git, elle est **servie en HTTP** par deux déploiements vivants — coût de levée nul, contre une réécriture d'historique. Voir le constat A de S4 |
| S5 — suites et dernier point ouvert | ☑ **faite** le 2026-08-16 | `c6f7c53` | ✅ **complète sur son périmètre réel** — les 40 px de vide mort du hero supprimés (`grid-template-rows` passe de `247,375px 0px` à `247,375px`, hero 625,88 → 585,88 px à 390 px, inchangé au centième à 640 et 1 280) ; garde-fou du millésime vérifié sur pièce, rien à faire ; **les trois points suspendus à FT2E laissés intacts, faute de réponse**. Trouvé au passage : l’appui du hero servi à l’échelle **1,72** entre `sm` et `lg` |
| S6 — plafond du hero et points ajournés | ☑ **faite** le 2026-08-16 | `b0213f5` · `+2` | ✅ **complète sur son périmètre réel** — appui du hero plafonné à sa taille de conception : échelle **1,72 → 0,996** à 1 000 px, 0,996 de 640 à 1 000, inchangée au-delà de `lg` ; hero identique **au centième** à 390 et 1 280 px, donc recette de S5 intacte ; zéro débordement sur neuf largeurs de 360 à 1 440 ; leçon remontée dans `.claude/rules/tailwind-design-tokens.md`. **Les trois points suspendus à FT2E sont ajournés à la présentation du projet**, à la demande de l'utilisateur — les deux déploiements antérieurs en ont ensuite été **sortis définitivement**, il n'en reste que deux |
| S7 — recette d'ensemble avant présentation | ☑ **faite** le 2026-08-16 | `653ce16` → `e6cc9f0` (6), **poussés** | ✅ **complète sur les quatre volets** — Lighthouse sur 9 routes du déploiement : **perf 100 partout**, CLS 0, TBT 0, a11y 100 sauf `/` 96 et `/societe/` 97 (même et unique violation, exception D1 **portée sur le motif**), SEO 69 = le seul audit `is-crawlable`, donc le verrou ; 211 liens 0 mort ; typographie du texte servi **72 → 0** apostrophes droites et **39 → 0** espaces fautives ; script de démonstration refait (il faisait ouvrir une fiche supprimée) ; `docs/22` prise en main FT2E créée. 🔴 **Trouvé, et bloquant pour la présentation : la connexion au CMS échoue** — `/api/auth` rend `500`, il manque deux variables d'environnement Vercel et la callback GitHub. ⚠ **Incident consigné** : une passe de correction a détruit trois libellés en écrivant ses références arrière comme caractères de contrôle, **build vert** |
| S8 — blocage hors dépôt et consignation | ☑ **faite** le 2026-08-17 | portée `docs` | ✅ **conforme à son périmètre, qui est un relevé** — dépôt et déploiement alignés, contrôlés **en deux temps** (`git ls-remote origin master` puis marqueur de build dans le HTML servi) ; `/api/auth` rend toujours **`500`**, blocage **ajourné par l’utilisateur**, aucun geste possible depuis le dépôt ; **aucun candidat ouvert**, les deux points ajournés laissés fermés. `src/` intact — **zéro ligne touchée**, donc aucune recette de rendu à jouer. ⚠ **Le dépôt a bougé pendant la session** — six commits `chore(deploy)` d’une session parallèle, poussés par un hook `Stop` ; contrôlés, **sans conséquence** (`.gitignore` ancré, grille émise, site inchangé à l’octet près) |

---

## Annexes — prompts de lancement

> **Règle de continuité du chantier.** Toute session se termine par le prompt de
> lancement de la suivante — `docs/superpowers/plans/2026-08-07-chantier-references-reelles.md`
> § 12 la donne comme « OBLIGATOIRE, clôture de session », et le protocole des
> planches la reprend en dernière consigne.
>
> ⚠ **Elle n’a été tenue ni à la clôture de S1 ni à celle de S3.** Omission relevée
> et réparée le 2026-08-16 : les annexes B et C ci-dessous ont été rédigées
> **après coup**, et non au fil des sessions comme le protocole l’exige. Le manque
> n’a pas eu de conséquence — les deux sessions ont été enchaînées dans la même
> conversation — mais c’est précisément ce qui l’a rendu invisible.
>
> Un prompt est écrit pour être **autoportant** : collé dans une session neuve,
> il ne suppose aucun contexte des sessions précédentes.

### Annexe A — session 1, le pipeline d’images (exécutée le 2026-08-16)

```text
Session 1 de la réduction de dette FT2E v3 — le pipeline d’images.

Contexte. Le relevé de dette du 2026-08-15 (commit d3bd8d9) a classé ce chantier
au rang 1 sur 9. La programmation complète est dans
docs/superpowers/plans/2026-08-16-reduction-dette.md — lis sa section « S1 » avant
toute chose, elle contient le diagnostic et les critères de recette.

Le constat mesuré. La page /equipe/ obtient perf=74 avec un LCP de 15,68 s et un
poids de 4 766 Kio. Huit JPEG bruts de 460 à 866 Ko sont servis par un <img> depuis
public/images/equipe/, sans astro:assets : ni AVIF, ni WebP, ni srcset. Les critères
de blocage du projet sont un LCP mobile sous 1,8 s et une performance d’au moins 90.

Ce n’est pas un travail d’enrobage. astro:assets ne traite que ce qu’il résout au
build depuis src/ ; public/ est recopié tel quel. Le travail est donc :

1. déplacer les huit fichiers de public/images/equipe/ vers src/assets/equipe/
   (src/assets n’existe pas encore, il est à créer) ;
2. résoudre le chemin porté par le frontmatter via import.meta.glob (eager: true) —
   le champ Zod `photo` ne change pas, c’est le rendu qui apprend à le résoudre ;
3. reporter le garde-fou fs.existsSync sur le glob : l’absence d’entrée EST l’absence
   de fichier, donc un seul mécanisme fait les deux métiers au lieu de deux ;
4. mettre à jour .claude/rules/astro-conventions.md § « Images optionnelles &
   fs.existsSync » dans le MÊME commit — la règle décrit le motif que tu remplaces.

Deux pièges vérifiés au dépôt :
- la photographie collective est rendue à DEUX endroits, src/pages/equipe.astro
  (collectifExiste) et src/pages/index.astro (même constante) — les deux migrent
  ensemble ou l’accueil casse ;
- duotone-photo est un filtre CSS posé sur l’élément ; <Image> émet bien un <img>,
  mais vérifie au rendu qu’aucune couleur native ne réapparaît (charte : duotone 197°
  obligatoire sur toute photographie).

Recette — mesurée, pas déclarée. Ne conclus pas sur un build vert (règle 11 du
CLAUDE.md) :
- LCP mobile sur /equipe/ < 1,8 s et performance >= 90 ;
- performance sur / >= 90, sans régression ;
- AVIF et WebP présents dans dist/, srcset sur les huit portraits ;
- le repli « [Photo à venir] » fonctionne toujours quand un fichier manque —
  teste-le en en retirant un ;
- capture de /equipe/ et de / après npm run preview.

Pièges de mesure propres à cette machine : Chrome refuse toute fenêtre sous 500 px,
les mesures à 390 px passent par une iframe servie en même origine par npm run
preview ; browser_resize de Playwright persiste d’un appel à l’autre et fait passer
une page saine pour cassée — restaure toujours la taille après mesure.

Commit selon .claude/rules/git-commit.md, portée `equipe` ou `layout`.

Question à poser en ouverture, sans attendre : l’arbitrage D1 (A2 contre le 100 de
Lighthouse) doit être tranché avant la recette de la session 3. Sa formulation est
en section D1 du plan. Pose-la, note la réponse dans le plan, et continue S1 sans
attendre qu’elle arrive.
```

---

### Annexe B — session 2, les planches : typographie et régénération

```text
Session 2 de la réduction de dette FT2E v3 — les planches : typographie puis
régénération.

Contexte. Le relevé de dette du 2026-08-15 (commit d3bd8d9) classe ces deux
constats aux rangs 2 et 3, fusionnés parce qu'ils réécrivent les mêmes fichiers —
les séparer doublerait le contrôle de rendu à 1 152 px. La programmation est dans
docs/superpowers/plans/2026-08-16-reduction-dette.md : lis sa section « S2 » avant
toute chose. Le protocole de production des planches est dans
docs/superpowers/specs/2026-08-12-planches-references-protocole.md, le bilan de
clôture du chantier dans docs/superpowers/plans/2026-08-12-chantier-planches-references.md.

Deux constats, tels que mesurés.

1. L'APOSTROPHE DROITE, SUR TOUT LE CORPUS DESSINÉ. La règle éditoriale impose
   U+2019 sur « tout contenu textuel destiné à l'utilisateur final ». Les planches —
   le livrable le plus récent et le plus visible — ne l'ont jamais reçue : 205
   occurrences dans le texte dessiné des SVG, 1 325 dans les extractions
   planche.json, aria_label compris. Les aria_label sont LUS TELS QUELS par les
   lecteurs d'écran : ce n'est pas une coquetterie typographique, c'est de
   l'accessibilité. L'outil existe déjà — scripts/injection-typographique.py définit
   APO = U+2019 — il n'a simplement jamais été passé sur public/images/projets/. Le
   relevé nomme la cause exactement : la discipline appliquée à src/content/ n'a pas
   suivi le contenu quand il a changé de répertoire.

2. L'INVARIANT DE RÉGÉNÉRATION EST ROMPU. Quatorze planches datent des 13 et 14
   août, alors que la correction de _tronc.mesurer n'est arrivée que le 15 avec la
   planche 21 (commit 1b23d48). « Régénération octet à octet » est le seul contrôle
   qui protège les planches publiées d'une dérive du tronc commun ; il ne tient plus
   tant que la passe n'est pas faite.

L'ORDRE DES DEUX OPÉRATIONS N'EST PAS INDIFFÉRENT — c'est le seul vrai piège de
cette session. Corriger la typographie D'ABORD, régénérer ENSUITE. Dans l'autre
sens, la régénération réécrit les SVG depuis les compositeurs et ÉCRASE les
apostrophes corrigées : on aurait fait le travail deux fois, et le second passage
effacerait le premier sans que rien ne le signale.

Corollaire : la correction porte sur la SOURCE, jamais sur le rendu.
  1. les planche.json de chaque dossier — la pièce que FT2E relit, et la source du
     titre court, du cartouche et de l'aria_label ;
  2. les compositeurs scripts/planches/<archetype>.py et le tronc _tronc.py, s'ils
     portent des chaînes littérales à apostrophe ;
  3. PUIS la régénération des 23 dossiers, qui propage la correction aux trois SVG.

Corriger les SVG directement serait une correction de sortie : elle disparaîtrait à
la première régénération. Même principe que la règle des deux titres — on corrige
l'original, jamais la copie.

Recette — mesurée, pas déclarée :
- 0 apostrophe droite dans les 23 planche.json ;
- 0 apostrophe droite dans les <text> des 69 SVG ;
- régénération octet à octet : 23 / 23, sommes de contrôle comparées ;
- rendu de la planche à 1 152 px et de la vignette à 300 px inchangé hors
  apostrophes, sur un échantillon de trois dossiers, par capture ;
- npm run build vert.

⚠ Contrôler À LA TAILLE DE LECTURE, jamais en pleine page (règle 13 du CLAUDE.md) :
1 152 px pour la planche, 552 pour l'appui, 300 pour la vignette. Une planche ne se
recadre pas, ne se duotone pas, ne s'illustre pas.

⚠ Insécables : l'outil d'écriture de fichiers normalise U+00A0 et U+202F. Si tu dois
en écrire dans un .md ou un .json, réinjecte-les par script après coup — voir la
mémoire insecables-normalisees-par-write.

Pièges de mesure propres à cette machine, tous vérifiés :
- la PERFORMANCE ne se mesure pas sur npm run preview, qui ne compresse rien : 0,8 s
  de biais sur la chaîne bloquante. Elle se mesure sur https://ft2e-v3.vercel.app,
  après avoir vérifié par un MARQUEUR DU BUILD — pas par un délai d'attente — que le
  déploiement porte bien le commit en cours. Règle consignée dans
  .claude/rules/astro-conventions.md § Performances ;
- Chrome refuse toute fenêtre sous 500 px : les largeurs de téléphone se mesurent par
  une iframe servie en même origine ;
- ⚠ la barre de défilement de l'iframe mange 15 px — une iframe de 390 donne un
  document de 375. Élargir jusqu'à ce que contentDocument.documentElement.clientWidth
  vaille exactement la largeur visée ;
- browser_resize de Playwright persiste d'un appel à l'autre et fait passer une page
  saine pour cassée. Préférer l'iframe, qui n'a rien à restaurer.

Commit selon .claude/rules/git-commit.md, portée `references` ou `design-system`.
Consigne la recette dans la section S2 du plan et mets à jour le tableau de suivi.

Termine par le prompt de lancement de la session suivante, en annexe du plan. ⚠ La
règle de continuité n'a été tenue ni en S1 ni en S3 — ne la manque pas une
troisième fois.
```

---

### Annexe C — session 4, hygiène documentaire et garde-fous

```text
Session 4 de la réduction de dette FT2E v3 — hygiène documentaire et garde-fous.

Contexte. Rangs 6, 7 et 8 du relevé de dette du 2026-08-15 (commit d3bd8d9),
regroupés parce que le coût de contrôle est le même pour un bloc que pour trois.
Aucune dépendance, aucun arbitrage technique, aucun risque. La programmation est
dans docs/superpowers/plans/2026-08-16-reduction-dette.md : lis sa section « S4 »
avant toute chose.

Six points, tous déjà mesurés. Le premier est le seul qui soit urgent.

1. L'HÔTE, DANS CINQ DOCUMENTS. docs/09, docs/14, docs/19, docs/20-pistes et les
   commentaires de public/robots.txt et src/layouts/BaseLayout.astro nomment
   ft2e-site.vercel.app. L'hôte réel est ft2e-v3.vercel.app — l'opérationnel, lui,
   est juste (config.yml, remote git). ⚠ Le risque est concentré sur
   docs/19-migration-production.md : c'est le RUNBOOK DE MISE EN PRODUCTION, il
   nommera le mauvais hôte au moment précis où on l'exécutera, redirections 301
   comprises.

2. GARDE-FOU MILLESIME_LIVRAISON_ANNONCE. La constante vaut 2026 et sera fausse sur
   quatorze affaires au 1er janvier 2027 — ni le build, ni le typecheck, ni le rendu
   ne le signaleront. Un test de build qui échoue au-delà de l'année en cours coûte
   trois lignes et supprime une échéance silencieuse.

3. legendeMedia, CODE MORT. Calculé sur quatre lignes dans
   src/pages/references/[...slug].astro, lu nulle part : c'est la légende de média
   d'avant les planches, manquée par le nettoyage de clôture. Signalé par le
   typecheck avec l'interface Props de PlancheReference — deux hints sur 82, les
   deux seuls qui désignent du code réellement mort.

4. QUATRE VALEURS HEXADÉCIMALES EN DUR. Trois dans Logo.astro, une dans
   TraceFlux.astro. Les valeurs SONT celles de la rampe — c'est le chaînage au jeton
   qui manque, donc la garantie qu'elles suivront la prochaine révision de charte
   (§ 17 de la charte, sans réserve).

5. CHAMPS IMAGE MORTS DES ACTUALITÉS. `image` et `image_alt` sont déclarés au Zod ET
   à Decap pour la collection actualites, lus par aucun rendu ; le fichier pointé
   n'existe pas, le répertoire est vide. Conséquence de comptage : un des huit
   marqueurs [DÉMO] restants ne peut jamais s'afficher — le compte réel des marqueurs
   ATTEIGNABLES est de sept, tous dans les secteurs. Corriger le champ ET le compte
   annoncé dans CLAUDE.md.

6. FINE DES MILLIERS DU CHAMP `performance`. ⚠ Le périmètre annoncé par le plan est
   faux : il dit « sur les 23 fiches », la mesure en trouve QUATRE — Dufour (5),
   Villedoux (4), École des douanes (4), Marans (1). La passe est bien plus courte
   qu'annoncé.

Deux constats ajoutés par la session 3, à arbitrer ici ou à laisser ouverts :
- le footer porte les liens tel: et mailto: à 17 px de haut, espacés de 29, sur les
  46 pages. axe ne les signale pas — l'exception d'espacement de WCAG 2.2 joue à
  partir de 24 px — mais la règle FT2E dit 44 × 44 pour tout élément actionnable,
  sans exception d'espacement. C'est un écart règle/code, pas un écart d'outil.
  ⚠ Ne PAS y appliquer la recette .cible-44 : son ::after est un calque de 44 px
  centré, qui se chevaucherait sur des cibles empilées — ce sont les BOÎTES qui
  doivent faire 44 px (voir la section S3 du plan) ;
- 40 px de vide mort sous sm dans le hero de l'accueil : le média est
  `hidden sm:block`, mais sa cellule de grille et le gap-10 du conteneur restent.

Deux constats ajoutés par la session 2, tous deux dans le périmètre « garde-fous » :
- scripts/planches/verser.py CONTRÔLE DEUX CHOSES QUI N'EXISTENT PLUS. Sa règle 2
  exige « une forme de repli mobile que le site sait rendre » — or le repli de
  lecture a été SUPPRIMÉ le 2026-08-15, et CLAUDE.md consigne que son garde-fou a
  été retiré avec lui ; celui de verser.py a survécu. Son étape 4 bascule
  `image_principale` en `planche:` — champ supprimé du schéma le même jour, donc la
  bascule échouerait sur toute fiche neuve. Un garde-fou qui survit à son objet est
  un contrôle qui ment sur ce qu'il contrôle : même principe que l'amendement A9.
- core.autocrlf VAUT true ET LE DÉPÔT N'A PAS DE .gitattributes. Les 92 pièces des
  planches (69 SVG + 23 JSON) sont en LF dans la copie de travail actuelle, et
  l'invariant de régénération y tient — 23 / 23 octet à octet. Dans un CLONE NEUF il
  ne tiendrait pas : git écrirait des CRLF, les compositeurs réécrivent du LF
  (`newline="\n"` dans _tronc.executer), et la régénération afficherait 92 écarts qui
  n'en seraient pas. À trancher : poser un .gitattributes (`*.svg text eol=lf`,
  `*.json text eol=lf`) ou inscrire dans le protocole que le contrôle de l'invariant
  normalise les fins de ligne avant de comparer. Ne PAS conclure « l'invariant est
  rompu » sur une machine fraîchement clonée sans avoir vérifié ce point d'abord.

⚠ Toute suppression de champ Zod se répercute dans public/admin/config.yml AU SEIN
DU MÊME COMMIT (règle du sous-agent content-modeller).

⚠ Un build vert ne prouve pas que la page s'affiche (règle 11) : après toute
modification de mise en page ou de global.css, contrôler le rendu de la page
touchée. La PERFORMANCE, elle, se mesure sur https://ft2e-v3.vercel.app et jamais
sur npm run preview, qui ne compresse rien — voir .claude/rules/astro-conventions.md
§ Performances.

Commit selon .claude/rules/git-commit.md ; les portées sont multiples, préfère
plusieurs commits nets à un fourre-tout. Consigne la recette dans la section S4 du
plan et mets à jour le tableau de suivi.

Question à poser en ouverture, sans attendre : D2, les trois questions à FT2E —
réception de la crèche de l'Oranger, sort des 25 visuels qui subsistent dans
l'historique git, archétype planche-chiffree jamais exercé. Leur formulation est en
section D2 du plan. Aucune n'est décidable depuis le dépôt, et la première masque un
défaut devenu invisible : la ligne statut a disparu du frontmatter, donc la fiche
annonce une affaire livrée sans dire quand, et plus rien dans le fichier ne signale
l'anomalie. C'est la seule des 23 dans ce cas.
```

### Annexe D — session 5, les suites de FT2E et les deux points ouverts (à coller telle quelle)

> Rédigée le 2026-08-16 **à la clôture de S4**, comme l'exige la règle de continuité
> de `CLAUDE.md`. Autoportante : elle ne suppose aucun contexte des sessions
> précédentes.

```
Session 5 du chantier FT2E v3 — suites des réponses FT2E et deux points ouverts.

Contexte. Le chantier de réduction de dette ouvert le 2026-08-16 est CLOS : ses
quatre sessions sont faites, sa décision D1 est tranchée, et ses trois questions
D2 ont été posées à FT2E le 2026-08-16. Le plan et ses recettes sont dans
docs/superpowers/plans/2026-08-16-reduction-dette.md — lis la section S4 et son
constat A avant toute chose. Cette session-ci n'a de contenu que si des réponses
sont arrivées ; sans elles, elle se limite aux deux points 4 et 5.

1. ⚠ LE PLUS URGENT, ET IL NE VIENT PAS DU RELEVÉ DE DETTE. Deux déploiements
   Vercel antérieurs répondent encore et servent les photographies d'ouvrages que
   le chantier des planches avait retirées de la v3 pour motif de droit d'auteur :
   ft2e-site.vercel.app (la v1) et ft2e-v2.vercel.app. Mesuré le 2026-08-16 : code
   200, huit visuels distincts sur la seule page /references, 819 à 937 Ko chacun,
   servis en 200. Les deux portent noindex et Disallow: / — ce qui empêche le
   référencement, pas l'accès, et c'est un verrou de démonstration pensé pour être
   levé un jour.
   Procédure, contrôle par curl et cases à cocher : docs/19-migration-production.md
   § 6 bis. NE RIEN SUPPRIMER SANS ARBITRAGE FT2E : ce sont leurs déploiements, et
   la décision est la leur. Vérifier d'abord si la réponse est arrivée.
   ⚠ La CLI Vercel répond « Not authorized » sur cette machine — la suppression se
   fait au tableau de bord, par FT2E ou avec elle.

2. RÉCEPTION DE LA CRÈCHE DE L'ORANGER, si la pièce est arrivée. La fiche
   src/content/projets/creche-oranger-perigny.md annonce une affaire livrée sans
   dire quand : annee_livraison est vide, la ligne statut a disparu du frontmatter,
   et plus rien dans le fichier ne signale l'anomalie. C'est la seule des 23 dans ce
   cas. Avec la date de réception : renseigner annee_livraison (le schéma l'exige
   dès que statut ne vaut plus « en cours », règle 10). Sans réponse : laisser en
   l'état et le redire dans le prompt suivant — ne pas fabriquer un millésime.

3. planche-chiffree, SI FT2E A TRANCHÉ. Seul archétype du protocole que les 23
   planches n'ont pas exercé, donc le seul dont rien ne garantit qu'il fonctionne.
   Soit le retirer de la liste fermée de
   docs/superpowers/specs/2026-08-12-planches-references-protocole.md, soit
   redéfinir ce qu'il montre. Le retirer suppose de vérifier qu'aucun compositeur
   ni verser.py n'y renvoie.

4. 40 PX DE VIDE MORT SOUS sm DANS LE HERO DE L'ACCUEIL. Le média est
   `hidden sm:block`, mais sa cellule de grille et le gap-10 du conteneur restent.
   Sans effet sur le CLS ni sur le débordement — c'est le seul point de la S3 laissé
   ouvert, et le moins coûteux du lot.

5. LE MILLÉSIME ANNONCÉ, SI ON APPROCHE DE 2027. MILLESIME_LIVRAISON_ANNONCE vaut
   2026 dans src/lib/projets.ts et porte l'affichage de quatorze affaires. Depuis le
   2026-08-16, le build ÉCHOUE en dur passé cette année-là — ce n'est plus une
   échéance silencieuse, mais il faut y répondre par des réceptions relevées auprès
   de FT2E, pas en poussant la constante.

Pièges vérifiés au dépôt, à ne pas redécouvrir :
- Un build vert ne prouve pas que la page s'affiche (règle 11). La PERFORMANCE ne se
  mesure JAMAIS sur npm run preview, qui ne compresse rien : 0,8 s de biais sur la
  chaîne bloquante. Elle se mesure sur https://ft2e-v3.vercel.app.
- Tailwind v4 élague les variables de thème qu'aucune classe n'emploie. Une couleur
  s'écrit en CLASSE littérale (stroke-encre), jamais en var(--color-…) dans un
  attribut SVG : le var() échappe au scan et la couleur tombe sans un mot du build.
- Dans un frontmatter .astro, une sonde de typage se fait en REMPLAÇANT un attribut,
  jamais en en ajoutant un second — un attribut dupliqué ne lève aucune erreur.
  Et ts(6196) sur une interface Props ne dit pas « code mort », il dit « contrat non
  consommé ». Recette écrite au-dessus de l'interface de PlancheReference.astro.
- Le dépôt porte un .gitattributes depuis le 2026-08-16 : ne pas le retirer. Sans
  lui, un clone neuf sort les 92 pièces des planches en CRLF et l'invariant de
  régénération se lit comme rompu alors qu'il tient.
- L'accueil est reçue à 96 en accessibilité, et c'est admis — à condition que la
  SEULE violation axe soit le color-contrast d'un complément de titre aria-hidden
  (arbitrage D1). Un 96 dû à autre chose est un blocage. Un 96 non expliqué dans le
  compte rendu est indistinguable d'une régression.
- L'outil Write normalise U+00A0 et U+202F : les insécables se réinjectent après coup
  par scripts/injection-typographique.py. ⚠ Ne PAS lancer ce script sur un document
  entier qui n'a jamais été normalisé — il réécrit alors des centaines de lignes sans
  rapport avec le travail en cours (mesuré sur le plan de dette : 173 lignes).

Recette de fin de session : npm run typecheck (0 erreur), npm run build (46 pages),
contrôle du RENDU de toute page touchée, et consignation dans le plan.

Portée de commit : plusieurs commits nets valent mieux qu'un fourre-tout — les
portées sont content, docs, fix, a11y selon les points.

Termine par le prompt de lancement de la session suivante, en annexe du plan et
reproduit intégralement dans ton message final. Cette règle est dans CLAUDE.md
parce qu'elle a été manquée deux fois.
```

---

### Annexe E — session 6, les trois réponses attendues et un dessin étiré (à coller telle quelle)

> Rédigée le 2026-08-16 **à la clôture de S5**, comme l’exige la règle de continuité
> de `CLAUDE.md`. Autoportante : elle ne suppose aucun contexte des sessions
> précédentes.

```
Session 6 du chantier FT2E v3 — trois réponses attendues de FT2E, et un dessin étiré.

Contexte. FT2E v3 est un site institutionnel Astro statique, déployé en démonstration
client sur https://ft2e-v3.vercel.app, indexation verrouillée par triple sécurité. Le
chantier de réduction de dette ouvert le 2026-08-16 est CLOS : ses quatre sessions
sont faites, sa décision D1 est tranchée, et sa session de suites S5 a soldé le
dernier point de rendu qui restait. Le plan et toutes ses recettes sont dans
docs/superpowers/plans/2026-08-16-reduction-dette.md — lis sa section S5 et le
constat A de S4 avant toute chose.

Les points 1, 2 et 3 attendent une réponse de FT2E, posée le 2026-08-16 et TOUJOURS
SANS RÉPONSE au soir du 2026-08-16 (revérifié en S5). Vérifie d'abord si elle est
arrivée. Sans elle, ces trois points ne s'exécutent pas — ne rien supprimer, ne rien
fabriquer, ne rien retirer — et la session se limite au point 4, qui ne dépend de
personne.

1. ⚠ LES DEUX DÉPLOIEMENTS RÉSIDUELS — le plus urgent, et il ne vient pas du relevé
   de dette. ft2e-site.vercel.app (la v1) et ft2e-v2.vercel.app répondent encore et
   servent les photographies d'ouvrages que le chantier des planches avait retirées
   de la v3 pour motif de droit d'auteur : code 200, huit visuels distincts sur la
   seule page /references, 819 à 937 Ko chacun. Revérifié le 2026-08-16 en ouverture
   de S5 : les deux répondent toujours 200. Les deux portent noindex et Disallow: /
   — ce qui empêche le référencement, pas l'accès, et c'est un verrou de démonstration
   pensé pour être levé un jour.
   Procédure, contrôle par curl et cases à cocher : docs/19-migration-production.md
   § 6 bis. NE RIEN SUPPRIMER SANS ARBITRAGE FT2E : ce sont leurs déploiements, et la
   décision est la leur.
   ⚠ La CLI Vercel répond « Not authorized » sur cette machine — la suppression se
   fait au tableau de bord, par FT2E ou avec elle.

2. RÉCEPTION DE LA CRÈCHE DE L'ORANGER, si la pièce est arrivée. La fiche
   src/content/projets/creche-oranger-perigny.md annonce une affaire livrée sans dire
   quand : annee_livraison est vide, la ligne statut a disparu du frontmatter, et plus
   rien dans le fichier ne signale l'anomalie. C'est la seule des 23 dans ce cas. Avec
   la date de réception : renseigner annee_livraison (le schéma l'exige dès que statut
   ne vaut plus « en cours », règle 10). Sans réponse : laisser en l'état et le redire
   dans le prompt suivant — ne pas fabriquer un millésime.

3. planche-chiffree, SI FT2E A TRANCHÉ. Seul archétype du protocole que les 23
   planches n'ont pas exercé, donc le seul dont rien ne garantit qu'il fonctionne.
   Soit le retirer de la liste fermée de
   docs/superpowers/specs/2026-08-12-planches-references-protocole.md, soit redéfinir
   ce qu'il montre. Le retirer suppose de vérifier qu'aucun compositeur ni verser.py
   n'y renvoie.

4. L'APPUI DU HERO EST SERVI ÉTIRÉ ENTRE sm ET lg — le seul point exécutable sans
   FT2E. Il ne vient pas non plus du relevé de dette : il a été mesuré en S5, en
   passant. L'appui de la fiche vedette (public/images/projets/<slug>/appui.svg,
   viewBox 0 0 552 368) est inliné dans le hero de src/pages/index.astro et occupe
   toute la largeur de sa colonne. Mesuré le 2026-08-16 par sonde en iframe :

     fenêtre      appui rendu    échelle
     640 px         606 px        1,10
     700 px         666 px        1,21
     768 px         718 px        1,30
     900 px         850 px        1,54
     1 000 px       950 px        1,72
     >= 1 024 px    460 a 550 px  <= 1,00   (la grille a 12 colonnes reprend la main)

   Ce n'est PAS un défaut de lisibilité — le mono de 10 px y gagne, il monte à 17.
   C'est un ÉPAISSISSEMENT DES FILETS DE 1 px, c'est-à-dire le défaut fondateur que le
   chantier des planches a chassé partout ailleurs en plafonnant chaque dessin à sa
   taille de conception : la vignette à 300 px dans CarteProjet, les trois bandes de
   PlancheReference. Le hero de l'accueil est le seul endroit du site où un dessin est
   encore étiré, et il l'était avant S5 — la correction des 40 px n'y est pour rien,
   les hauteurs à 640 et 1 280 px sont identiques au centième avant et après.
   Règles applicables : .claude/rules/tailwind-design-tokens.md § Composants signature
   (« aucune échelle au-dessus de 1,00 ») et CLAUDE.md § Les planches de références,
   principe 3. Le plafond vit dans le COMPOSANT DU DESSIN, jamais dans la grille
   appelante — leçon écrite pour CarteProjet le 2026-08-15, et elle vaut ici : le
   nombre de colonnes est un réglage de page, la taille de conception est une
   propriété du dessin.
   ⚠ Pose la question avant de corriger : le hero relève-t-il du même plafond ?
   L'appui y est un ornement de couverture, pas une figure de fiche, et la charte ne
   tranche pas explicitement ce cas. Si le plafond s'applique, la marge de papier qui
   reste autour d'un dessin plafonné est légitime — un plan a des marges.

5. LE MILLÉSIME ANNONCÉ, SI ON APPROCHE DE 2027. MILLESIME_LIVRAISON_ANNONCE vaut 2026
   dans src/lib/projets.ts et porte l'affichage de quatorze affaires. Depuis le
   2026-08-16 le build ÉCHOUE EN DUR passé cette année-là — ce n'est plus une échéance
   silencieuse. Il faut y répondre par des réceptions relevées auprès de FT2E, jamais
   en poussant la constante : la pousser désarmerait le garde-fou pour s'épargner
   exactement l'échec qu'on lui demande de produire.

Pièges vérifiés au dépôt, à ne pas redécouvrir :
- Un build vert ne prouve pas que la page s'affiche (règle 11). La PERFORMANCE ne se
  mesure JAMAIS sur npm run preview, qui ne compresse rien : 0,8 s de biais sur la
  chaîne bloquante. Elle se mesure sur https://ft2e-v3.vercel.app, après avoir vérifié
  par un MARQUEUR DU BUILD — jamais par un délai d'attente — que le déploiement porte
  bien le commit en cours.
- ⚠ Chrome refuse toute fenêtre sous 500 px, EN HEADLESS AUSSI. Une capture directe en
  --window-size=390,900 ne rend pas une page de 390 : elle la compose à ~500 px puis
  ROGNE l'image à 390. Le résultat montre un texte coupé au bord droit, c'est-à-dire
  un débordement parfaitement crédible et parfaitement faux — sur une page dont la
  sonde venait de mesurer scrollWidth == clientWidth. Les largeurs de téléphone se
  mesurent par une IFRAME servie en même origine, élargie jusqu'à ce que
  contentDocument.documentElement.clientWidth vaille exactement la largeur visée : la
  barre de défilement de l'iframe mange 15 px.
- ⚠ Et cette sonde ne se cale pas sur la seule largeur : le document about:blank
  INITIAL de l'iframe a exactement la largeur du cadre, donc une boucle qui compare
  clientWidth à la cible sort au premier tour et mesure le vide. Le symptôme ne
  ressemble pas à une erreur de synchronisation mais à un défaut de la page —
  conteneur introuvable, hauteurs nulles, sélecteurs qui ne mordent pas. Attendre
  onload, ou caler sur la présence d'un élément de la page (querySelector('h1')).
- browser_resize de Playwright persiste d'un appel à l'autre et fait passer une page
  saine pour cassée ; et son profil Chrome peut être VERROUILLÉ quand le navigateur du
  client est ouvert (« Browser is already in use »). Chrome headless lancé à la main
  avec son propre --user-data-dir n'a ni l'un ni l'autre problème.
- Tailwind v4 élague les variables de thème qu'aucune classe n'emploie. Une couleur
  s'écrit en CLASSE littérale (stroke-encre), jamais en var(--color-…) dans un
  attribut SVG : le var() échappe au scan et la couleur tombe sans un mot du build.
- Dans un frontmatter .astro, une sonde de typage se fait en REMPLAÇANT un attribut,
  jamais en en ajoutant un second — un attribut dupliqué ne lève aucune erreur. Et
  ts(6196) sur une interface Props ne dit pas « code mort », il dit « contrat non
  consommé ».
- Le dépôt porte un .gitattributes depuis le 2026-08-16 : ne pas le retirer. Sans lui,
  un clone neuf sort les 92 pièces des planches en CRLF et l'invariant de régénération
  se lit comme rompu alors qu'il tient.
- L'accueil est reçue à 96 en accessibilité, et c'est admis — à condition que la SEULE
  violation axe soit le color-contrast d'un complément de titre aria-hidden (arbitrage
  D1). Un 96 dû à autre chose est un blocage. Un 96 non expliqué dans le compte rendu
  est indistinguable d'une régression.
- ⚠ Les insécables sont normalisées EN ENTRÉE des outils d'édition : un U+00A0 ou
  U+202F tapé dans une chaîne à remplacer en ressort en espace ordinaire, et l'édition
  échoue sans rien dire d'utile — le plan de dette en porte 174 et 57. Pour éditer ces
  documents, passer par un petit script Python qui lit et écrit l'UTF-8 tel quel, avec
  un contrôle d'occurrences qui ÉCHOUE plutôt que de remplacer au hasard. ⚠ Ne PAS
  lancer scripts/injection-typographique.py sur un document entier qui n'a jamais été
  normalisé : il réécrit des centaines de lignes sans rapport avec le travail en cours
  (mesuré sur le plan de dette : 173 lignes).

Recette de fin de session : npm run typecheck (0 erreur), npm run build (46 pages),
contrôle du RENDU de toute page touchée à sa largeur de lecture, et consignation dans
le plan.

Portée de commit : plusieurs commits nets valent mieux qu'un fourre-tout — les portées
sont content, docs, fix, design-system selon les points.

Termine par le prompt de lancement de la session suivante, en annexe du plan et
reproduit intégralement dans ton message final. Cette règle est dans CLAUDE.md parce
qu'elle a été manquée deux fois.
```

### Annexe F — session 7, la finalisation avant présentation à FT2E (à coller telle quelle)

```
Session 7 du chantier FT2E v3 — deux points ajournes, et la finalisation avant
presentation.

Contexte. FT2E v3 est un site institutionnel Astro statique, deploye en demonstration
client sur https://ft2e-v3.vercel.app, indexation verrouillee par triple securite
(robots.txt Disallow, meta noindex, header X-Robots-Tag). Le chantier de reduction de
dette ouvert le 2026-08-16 est CLOS : ses quatre sessions sont faites, sa decision D1
est tranchee, et ses deux sessions de suites S5 et S6 ont solde les deux derniers
points de rendu. Le plan et toutes ses recettes sont dans
docs/superpowers/plans/2026-08-16-reduction-dette.md — lis sa section S6 avant toute
chose. Le site ne porte plus AUCUN dessin servi au-dessus de sa taille de conception.

0. LE PERIMETRE — la v3, et uniquement la v3. Deux deploiements anterieurs
   (ft2e-site.vercel.app, la v1, et ft2e-v2.vercel.app) repondent encore et servent
   des photographies d'ouvrages. Ils sont HORS PERIMETRE par decision de
   l'utilisateur du 2026-08-16 : « ces projets anterieurs ne sont plus concernes par
   quoi que ce soit ». Ne pas les mesurer, ne pas les proposer, ne pas les remettre
   dans un compte rendu. Le fait reste documente au § 6 bis de
   docs/19-migration-production.md, ou il sert le jour de la mise en production et ce
   jour-la seulement.

1. LES DEUX POINTS AJOURNES — ne PAS les rouvrir sans que l'utilisateur le demande.
   Ils sont mis en suspens jusqu'a la presentation du projet final, a la demande
   explicite de l'utilisateur le 2026-08-16 (« je veux finaliser sans me preoccuper
   de ces questions annexes »). Les redire en fin de session, ne rien executer
   dessus, ne rien fabriquer :
   a. Reception de la creche de l'Oranger — src/content/projets/creche-oranger-
      perigny.md annonce une affaire livree sans dire quand : annee_livraison vide,
      ligne statut absente, et plus rien dans le fichier ne signale l'anomalie. Seule
      des 23 dans ce cas. NE PAS FABRIQUER DE MILLESIME.
   b. planche-chiffree — seul archetype de la liste fermee du protocole que les 23
      planches n'ont pas exerce, donc le seul dont rien ne garantit qu'il fonctionne.
      Le retirer ou le redefinir est un arbitrage editorial.
   ⚠ Un seul de ces deux porte une echeance propre : la reception de la creche est
   le premier des quatorze releves qu'appelle MILLESIME_LIVRAISON_ANNONCE, et le
   garde-fou de S4 fera ECHOUER LE BUILD au 1er janvier 2027. Ne jamais y repondre en
   poussant la constante : cela desarmerait le garde-fou pour s'epargner exactement
   l'echec qu'on lui demande de produire. La reponse est d'aller relever les
   receptions aupres de FT2E.

2. CE QUE LA SESSION FAIT REELLEMENT — a definir avec l'utilisateur en ouverture.
   Le chantier de dette est clos et son dernier point de rendu est solde : il n'y a
   plus de travail programme en attente. Demande ce que « finaliser » recouvre pour
   lui avant de lancer quoi que ce soit. Les candidats connus, tous hors dette et
   aucun ouvert d'office :
   - la recette d'ensemble avant presentation : Lighthouse sur les pages
     principales du DEPLOIEMENT (jamais sur npm run preview), controle des liens
     internes par scripts/controle-liens-internes.py, relecture editoriale ;
   - le script de demonstration client (docs/21-script-demo-2-juillet.md) a
     actualiser pour la presentation reelle ;
   - la prise en main de Decap par FT2E (le code est en place et coherent ; ce qui
     manque est la prise en main) ;
   - les 7 marqueurs [DEMO] restants, tous des image_alt de src/content/secteurs/,
     qui se levent au reportage photographique et pas par une validation.

Pieges verifies au depot, a ne pas redecouvrir :
- ⚠ AVANT TOUTE MESURE DE PERFORMANCE, VERIFIER QUE LE DEPLOIEMENT PORTE LE CODE.
  Il le portait au 2026-08-16 au soir — cd0e635 pousse, arrivee controlee par marqueur
  et capture du deploiement identique a la locale au MD5 — mais il ne l'a pas toujours
  porte : les sessions S4, S5 et S6 avaient accumule 18 commits non pousses, et le site
  en ligne s'etait arrete TROIS SESSIONS en arriere sans que rien ne le signale. Les
  recettes de ces sessions restent valables (elles mesuraient le local et le disaient),
  mais le client, lui, voyait un site vieux de trois sessions. Le controle prend dix
  secondes et il est double : git ls-remote origin master — la reference LOCALE peut
  etre perimee — et un MARQUEUR DU BUILD dans le HTML servi. Le push reste sortant : le
  demander, ne pas le faire d'office.
- Un build vert ne prouve pas que la page s'affiche (regle 11). La PERFORMANCE ne se
  mesure JAMAIS sur npm run preview, qui ne compresse rien : 0,8 s de biais sur la
  chaine bloquante. Elle se mesure sur https://ft2e-v3.vercel.app, apres avoir
  verifie par un MARQUEUR DU BUILD — jamais par un delai d'attente — que le
  deploiement porte bien le commit en cours.
- ⚠ Des serveurs astro preview de sessions anterieures tournent encore : seize ports
  occupes au 2026-08-16, plusieurs repondant 200. Ce n'est pas grave en soi (astro
  preview sert le DISQUE, donc tous servent le dist/ courant, verifie par marqueur
  sur trois ports) — le vrai risque est de mesurer SANS AVOIR REBUILD.
- ⚠ Chrome refuse toute fenetre sous 500 px, EN HEADLESS AUSSI : une capture en
  --window-size=390,900 compose la page a ~500 px puis ROGNE l'image a 390, ce qui
  montre un debordement parfaitement credible et parfaitement faux. Les largeurs de
  telephone se mesurent par une IFRAME servie en meme origine, elargie jusqu'a ce que
  contentDocument.documentElement.clientWidth vaille la largeur visee.
- ⚠ Et cette sonde a deux biais connus : le document about:blank INITIAL de l'iframe a
  exactement la largeur du cadre, donc caler sur onload ET sur la presence d'un
  element de la page, sinon la boucle sort au premier tour et mesure le vide ; et les
  media queries CSS comptent la barre de defilement quand clientWidth ne la compte
  pas, soit 15 px d'ecart — a clientWidth 1023 la page est deja en lg. Sans
  consequence sur une echelle, decisif sur une borne.
- ⚠ --user-data-dir fait echouer --dump-dom de Chrome EN SILENCE : code de sortie 0 et
  aucune sortie du tout. Le meme appel sans l'option rend le document complet.
- browser_resize de Playwright persiste d'un appel a l'autre et fait passer une page
  saine pour cassee ; son profil peut etre VERROUILLE si le navigateur du client est
  ouvert. Chrome headless lance a la main n'a ni l'un ni l'autre probleme.
- Tailwind v4 elague les variables de theme qu'aucune classe n'emploie. Une couleur
  s'ecrit en CLASSE litterale (stroke-encre), jamais en var(--color-…) dans un
  attribut SVG. Et une mesure de mise en page (un plafond, une borne) s'ecrit en CSS
  de composant plutot qu'en classe arbitraire unique, pour la meme raison.
- Dans un frontmatter .astro, une sonde de typage se fait en REMPLACANT un attribut,
  jamais en en ajoutant un second — un attribut duplique ne leve aucune erreur. Et
  ts(6196) sur une interface Props ne dit pas « code mort », il dit « contrat non
  consomme ».
- Le depot porte un .gitattributes depuis le 2026-08-16 : ne pas le retirer. Sans lui,
  un clone neuf sort les 92 pieces des planches en CRLF et l'invariant de
  regeneration se lit comme rompu alors qu'il tient.
- L'accueil est recue a 96 en accessibilite, et c'est admis — a condition que la SEULE
  violation axe soit le color-contrast d'un complement de titre aria-hidden (arbitrage
  D1). Un 96 du a autre chose est un blocage ; un 96 non explique dans le compte rendu
  est indistinguable d'une regression.
- ⚠ Les insecables sont normalisees EN ENTREE des outils d'edition : un U+00A0 ou
  U+202F tape dans une chaine a remplacer en ressort en espace ordinaire, et l'edition
  echoue sans rien dire d'utile — le plan de dette en porte 219 et 75. Pour editer ces
  documents, passer par un petit script Python qui lit et ecrit l'UTF-8 tel quel, avec
  un controle d'occurrences qui ECHOUE plutot que de remplacer au hasard, et qui ecrit
  ses propres insecables en echappement \u00a0 / \u202f — un echappement, lui, survit
  a la normalisation. ⚠ Ne PAS lancer scripts/injection-typographique.py sur un
  document entier qui n'a jamais ete normalise : il reecrit des centaines de lignes
  sans rapport avec le travail en cours (mesure sur le plan de dette : 173 lignes).

- ⚠ Une ancre de remplacement se COPIE du fichier, elle ne se retape pas : le corpus
  melange apostrophes droites et typographiques, et une ancre retapee echoue en
  disant seulement « 0 occurrence », ce qui ne designe pas la cause. Cibler par
  PREFIXE DE LIGNE quand c'est possible, et faire echouer le script plutot que
  remplacer au hasard.

Recette de fin de session : npm run typecheck (0 erreur), npm run build (46 pages),
controle du RENDU de toute page touchee a sa largeur de lecture, et consignation dans
le plan.

Portee de commit : plusieurs commits nets valent mieux qu'un fourre-tout — les portees
sont content, docs, fix, design-system selon les points.

Termine par le prompt de lancement de la session suivante, en annexe du plan et
reproduit integralement dans ton message final. Cette regle est dans CLAUDE.md parce
qu'elle a ete manquee deux fois.
```
### Annexe G — session 8, le déblocage du CMS (à coller telle quelle)

````
Session 8 du chantier FT2E v3 — un blocage hors dépôt qui ne se lève pas depuis le
code, et deux points toujours ajournés.

Contexte. FT2E v3 est un site institutionnel Astro statique, déployé en démonstration
client sur https://ft2e-v3.vercel.app, indexation verrouillée par triple sécurité
(robots.txt Disallow, meta noindex, header X-Robots-Tag). Le chantier de réduction de
dette est CLOS depuis S6. La session 7 (2026-08-16) a fait la recette d'ensemble avant
présentation : Lighthouse sur neuf routes du déploiement, relecture éditoriale, script
de démonstration refait, et création du mode d'emploi CMS pour FT2E. Lis la section S7
de docs/superpowers/plans/2026-08-16-reduction-dette.md avant toute chose.

0. LE PÉRIMÈTRE — la v3, et uniquement la v3. Deux déploiements antérieurs
   (ft2e-site.vercel.app et ft2e-v2.vercel.app) répondent encore et servent des
   photographies d'ouvrages. Ils sont HORS PÉRIMÈTRE par décision de l'utilisateur du
   2026-08-16 : « ces projets antérieurs ne sont plus concernés par quoi que ce soit ».
   Ne pas les mesurer, ne pas les proposer, ne pas les remettre dans un compte rendu.
   Le fait reste documenté au § 6 bis de docs/19-migration-production.md, où il sert le
   jour de la mise en production et ce jour-là seulement.

1. LE POINT BLOQUANT, ET IL N'EST PAS DANS LE DÉPÔT — la connexion au CMS échoue.
   Mesuré sur le déploiement le 2026-08-16 : /admin/ répond 200 et l'interface Decap
   s'affiche, /admin/config.yml répond 200, mais /api/auth?provider=github rend
   HTTP 500 — « Configuration OAuth manquante : definir OAUTH_GITHUB_CLIENT_ID dans les
   variables d'environnement Vercel ». Le bouton « Se connecter » est donc mort.

   ⚠ NE RIEN CORRIGER DANS LE DÉPÔT : api/auth.js et api/callback.js sont justes, et
   config.yml pointe le bon dépôt depuis la correction du 2026-08-10. Ce qui manque vit
   dans deux consoles d'administration, et SEUL L'UTILISATEUR PEUT LE FAIRE (la CLI
   Vercel répond « Not authorized » sur cette machine, et elle n'est même pas installée).
   Les trois gestes, dans l'ordre, sont écrits avec leur commande de contrôle dans
   docs/22-prise-en-main-decap.md § 0 : callback GitHub sur
   https://ft2e-v3.vercel.app/api/callback, puis OAUTH_GITHUB_CLIENT_ID et
   OAUTH_GITHUB_CLIENT_SECRET sur le projet Vercel, puis redéploiement.

   OUVRIR LA SESSION EN LE DEMANDANT. Tant que ce n'est pas levé, la section C du script
   de démonstration — que le script appelle lui-même « le moment clé » — ne peut pas
   avoir lieu, et la prise en main par FT2E ne peut pas commencer. Contrôle en dix
   secondes, doit cesser de rendre 500 :
   curl -s -o /dev/null -w "%{http_code}\n" "https://ft2e-v3.vercel.app/api/auth?provider=github"

   ⚠ Cet avertissement existait EN COMMENTAIRE en tête de public/admin/config.yml depuis
   le 2026-08-10 et a traversé six sessions sans être exécuté. Un commentaire n'échoue
   jamais. Ne pas se contenter d'en ajouter un de plus.

2. LES COMMITS DE S7 SONT POUSSÉS ET DÉPLOYÉS, à partir de `8518d49`, le 2026-08-16 à la
   demande de l'utilisateur. (Pas de décompte ici : chaque commit qui documente le
   décompte l'invalide. `git log --oneline 8518d49..master` le donne, et reste juste.)
   Arrivée contrôlée par marqueur du build (l'apostrophe courbe de la baseline) en une
   vingtaine de secondes, puis recette
   refaite sur le code en ligne : typographie 0/0 sur 12 routes, baseline courbée 12/12,
   l'énumération renommée tient en production (chip « Études d'exécution / BIM (1) »,
   comptage non nul donc appariement intact), Lighthouse perf 100 sur six routes et 99
   sur deux, a11y 96/97/100 x 6 inchangée, CLS 0 partout.
   RIEN N'EST EN ATTENTE DE PUSH à l'ouverture de cette session. Le vérifier quand même,
   en dix secondes et EN DEUX TEMPS : git ls-remote origin master (la référence locale
   peut être périmée) ET un marqueur du build dans le HTML servi. En S6, le site en
   ligne s'était arrêté TROIS SESSIONS en arrière sans que rien ne le signale.

3. LES DEUX POINTS AJOURNÉS — ne PAS les rouvrir sans que l'utilisateur le demande. Ils
   sont en suspens jusqu'à la présentation du projet, à sa demande explicite du
   2026-08-16 (« je veux finaliser sans me préoccuper de ces questions annexes »). Les
   redire en fin de session, ne rien exécuter dessus, ne rien fabriquer :
   a. Réception de la crèche de l'Oranger — src/content/projets/creche-oranger-perigny.md
      annonce une affaire livrée sans dire quand : annee_livraison vide, ligne statut
      absente. Seule des 23 dans ce cas. NE PAS FABRIQUER DE MILLÉSIME.
   b. planche-chiffree — seul archétype de la liste fermée du protocole que les 23
      planches n'ont pas exercé, donc le seul dont rien ne garantit qu'il fonctionne.
      Le retirer ou le redéfinir est un arbitrage éditorial.
   ⚠ Un seul des deux porte une échéance propre : la réception de la crèche est le
   premier des quatorze relevés qu'appelle MILLESIME_LIVRAISON_ANNONCE, et le garde-fou
   de S4 fera ÉCHOUER LE BUILD au 1er janvier 2027. Ne jamais y répondre en poussant la
   constante : cela désarmerait le garde-fou pour s'épargner exactement l'échec qu'on lui
   demande de produire. La réponse est d'aller relever les réceptions auprès de FT2E.

4. CE QUE LA SESSION FAIT D'AUTRE — à définir avec l'utilisateur en ouverture. Rien
   n'est programmé. Les candidats connus, aucun ouvert d'office :
   - les insécables du CORPUS DESSINÉ : 12 écarts de ponctuation subsistent dans les
     planches SVG. ⚠ Ne PAS lancer scripts/injection-typographique.py dessus : il
     DÉPLACE LE DESSIN, les compositeurs mesurant leurs chaînes pour poser la géométrie
     et U+202F n'ayant pas la chasse d'une espace ordinaire. C'est un chantier avec
     régénération des 23 dossiers et contrôle du rendu, pas une passe de correction ;
   - la régénération des vingt planches antérieures à la 21 (point ouvert le plus ancien,
     docs/superpowers/plans/2026-08-12-chantier-planches-references.md) ;
   - les 7 marqueurs [DÉMO] restants, tous des image_alt de src/content/secteurs/, qui se
     lèvent au reportage photographique et pas par une validation ;
   - le LCP mobile, qui est AU seuil et non sous le seuil. Sept mesures sur les deux
     pages les plus lourdes : 1 656, 1 658, 1 681, 1 768, 1 806, 1 807 et 1 815 ms pour
     un budget de 1 800. Elles se répartissent de part et d'autre du seuil SANS qu'aucune
     page ne soit systématiquement du mauvais côté — c'est l'accueil qui bascule sur un
     tir, /equipe/ sur un autre. Ne PAS traiter cela comme un défaut de /equipe/ : ce
     serait optimiser la mauvaise page. La fiche projet, elle, descend à 1 068 ms.

Pièges vérifiés au dépôt, à ne pas redécouvrir :
- ⚠ UN BUILD VERT NE PROUVE MÊME PAS QUE LE TEXTE EXISTE. En S7, une passe de correction
  a écrit ses références arrière \1 \2 \3 comme caractères de contrôle U+0001-0003 et
  a DÉTRUIT trois libellés de l'accueil et de /societe/ ; npm run build a produit ses
  46 pages sans broncher. Seul astro check a protesté, et pour une raison indirecte (il
  sérialise l'AST en JSON, qui interdit les caractères de contrôle nus). Corollaire :
  après toute correction de texte, contrôler la PRÉSENCE du texte attendu — une mesure
  d'absence de défaut ne distingue pas « corrigé » de « supprimé ».
- ⚠ Les insécables sont normalisées EN ENTRÉE des outils d'édition, ET CE N'EST PAS
  DÉTERMINISTE : en S7 le même script littéral est passé une fois puis a échoué la
  suivante. Trois conséquences. (1) Tout script qui manipule des insécables doit porter
  une ASSERTION D'AUTO-CONTRÔLE en tête — c'est elle qui a empêché la seconde écriture
  destructrice. (2) Les caractères sensibles se CONSTRUISENT par chr(0xA0) / chr(0x2019),
  jamais en littéral et pas davantage en échappement \u00a0 : l'échappement a échoué
  deux fois avant que ce soit clair, un appel de fonction ne peut pas être réécrit en
  route. (3) Un instrument dont les insécables ont été normalisées signale comme
  fautives LES PAGES LES MIEUX COMPOSÉES, parce que .replace('&nbsp;', NBSP) y injecte
  des espaces ordinaires — deux relevés de S7 l'ont fait, sur des pages légales.
- ⚠ Une ancre de remplacement se COPIE du fichier, elle ne se retape pas : le corpus
  mélange apostrophes droites et typographiques, et une ancre retapée échoue en disant
  seulement « 0 occurrence ». Le plan de dette porte 219 U+00A0 et 75 U+202F : l'éditer
  passe obligatoirement par un script Python, avec contrôle du compte AVANT et APRÈS.
- ⚠ La PERFORMANCE ne se mesure JAMAIS sur npm run preview, qui ne compresse rien :
  0,8 s de biais sur la chaîne bloquante. Elle se mesure sur le déploiement, après avoir
  vérifié par un MARQUEUR DU BUILD — jamais par un délai d'attente — qu'il porte le
  commit en cours. Et une seule mesure ne conclut pas : le LCP des deux pages les plus
  lourdes passe de 1 656 à 1 815 ms d'un tir à l'autre, de part et d'autre du seuil, et
  ce n'est pas toujours la même qui bascule.
- ⚠ npx lighthouse est un processus Windows et n'accepte PAS les chemins Git-Bash
  /c/... en --output-path : il n'écrit rien, en silence, et le script conclut « aucun
  JSON ». Se placer dans le répertoire et passer un chemin relatif.
- ⚠ Chrome refuse toute fenêtre sous 500 px, EN HEADLESS AUSSI : une capture en
  --window-size=390,900 compose la page à ~500 px puis ROGNE l'image, ce qui montre un
  débordement crédible et faux. Les largeurs de téléphone se mesurent par une IFRAME
  servie en même origine. Deux biais de cette sonde : caler sur onload ET sur la
  présence d'un élément de la page (le about:blank initial a la largeur du cadre) ; et
  les media queries comptent la barre de défilement que clientWidth ne compte pas, soit
  15 px d'écart — sans conséquence sur une échelle, décisif sur une borne.
- ⚠ Une sonde en iframe dont le sentinelle de résultat apparaît LITTÉRALEMENT dans son
  propre <script> se fait extraire son code source au lieu de son résultat. Construire
  le sentinelle à l'exécution.
- ⚠ --user-data-dir fait échouer --dump-dom de Chrome EN SILENCE : code de sortie 0 et
  aucune sortie. Le même appel sans l'option rend le document complet.
- ⚠ Des serveurs astro preview de sessions antérieures tournent encore. Ce n'est pas
  grave en soi (astro preview sert le DISQUE, donc tous servent le dist/ courant) — le
  vrai risque est de mesurer SANS AVOIR REBUILD. Apparier le serveur à son dist par un
  marqueur déposé dans dist/ et relu par curl.
- L'accueil est reçue à 96 en accessibilité et /societe/ à 97, et c'est admis :
  l'exception D1 a été portée SUR LE MOTIF en S7, et non plus sur la seule page. La
  condition reste stricte — la SEULE violation doit être le color-contrast d'un
  complément de titre aria-hidden. Elle se déclenche exactement là où ce complément est
  posé sur un APLAT PLEIN, qu'axe sait résoudre ; ailleurs le papier tramé l'empêche de
  conclure et l'outil s'abstient. Un score non expliqué dans un compte rendu est
  indistinguable d'une régression.
- Le SEO plafonne à 69 sur toutes les pages, et l'unique audit en échec est
  is-crawlable. C'est le verrou d'indexation, pas un défaut. Ne pas le « corriger ».
- Tailwind v4 élague les variables de thème qu'aucune classe n'emploie. Une couleur
  s'écrit en CLASSE littérale (stroke-encre), jamais en var(--color-…) dans un attribut
  SVG. Et une mesure de mise en page (un plafond, une borne) s'écrit en CSS de composant
  plutôt qu'en classe arbitraire unique, pour la même raison.
- Dans un frontmatter .astro, une sonde de typage se fait en REMPLAÇANT un attribut,
  jamais en en ajoutant un second — un attribut dupliqué ne lève aucune erreur. Et
  ts(6196) sur une interface Props ne dit pas « code mort », il dit « contrat non
  consommé ».
- Le dépôt porte un .gitattributes depuis le 2026-08-16 : ne pas le retirer. Sans lui,
  un clone neuf sort les 92 pièces des planches en CRLF et l'invariant de régénération
  se lit comme rompu alors qu'il tient.
- L'énumération « Études d'exécution » s'écrit depuis S7 avec l'APOSTROPHE
  TYPOGRAPHIQUE, dans src/content.config.ts, public/admin/config.yml et six fiches.
  L'appariement fiche/secteur se fait en égalité de chaînes : une fiche rédigée hors
  Decap avec l'ancienne graphie fait échouer le build. C'est voulu.

Recette de fin de session : npm run typecheck (0 erreur), npm run build (46 pages),
python scripts/controle-liens-internes.py (0 lien mort), contrôle du RENDU de toute page
touchée à sa largeur de lecture, et consignation dans le plan.

Portée de commit : plusieurs commits nets valent mieux qu'un fourre-tout — les portées
sont content, docs, fix, design-system selon les points.

Termine par le prompt de lancement de la session suivante, en annexe du plan et
reproduit intégralement dans ton message final. Cette règle est dans CLAUDE.md parce
qu'elle a été manquée deux fois.
````

### Annexe H — session 9, le CMS toujours bloqué et rien de programmé (à coller telle quelle)

````
Session 9 du chantier FT2E v3 - un blocage hors depot qui n'a toujours pas ete leve, et
rien de programme par ailleurs.

Contexte. FT2E v3 est un site institutionnel Astro statique, deploye en demonstration
client sur https://ft2e-v3.vercel.app, indexation verrouillee par triple securite
(robots.txt Disallow, meta noindex, header X-Robots-Tag). Le chantier de reduction de
dette est CLOS depuis S6. La session 7 (2026-08-16) a fait la recette d'ensemble avant
presentation : Lighthouse sur neuf routes du deploiement, relecture editoriale, script
de demonstration refait, mode d'emploi CMS cree. La session 8 (2026-08-17) N'A RIEN
CONSTRUIT, et c'est son resultat : elle a mesure l'etat, constate que le seul point
bloquant est hors du depot, et tout le reste a ete ajourne par l'utilisateur. Lis les
sections S7 et S8 de docs/superpowers/plans/2026-08-16-reduction-dette.md avant toute
chose.

0. LE PERIMETRE - la v3, et uniquement la v3. Deux deploiements anterieurs
   (ft2e-site.vercel.app et ft2e-v2.vercel.app) repondent encore et servent des
   photographies d'ouvrages. Ils sont HORS PERIMETRE par decision de l'utilisateur du
   2026-08-16 : « ces projets anterieurs ne sont plus concernes par quoi que ce soit ».
   Ne pas les mesurer, ne pas les proposer, ne pas les remettre dans un compte rendu.
   Le fait reste documente au § 6 bis de docs/19-migration-production.md, ou il sert le
   jour de la mise en production et ce jour-la seulement.

1. LE POINT BLOQUANT, ET IL N'EST PAS DANS LE DEPOT - la connexion au CMS echoue.
   Remesure le 2026-08-17, inchangee depuis le 2026-08-16 : /admin/ repond 200 et
   l'interface Decap s'affiche, mais /api/auth?provider=github rend HTTP 500 -
   « Configuration OAuth manquante : definir OAUTH_GITHUB_CLIENT_ID dans les variables
   d'environnement Vercel ». Le bouton « Se connecter » est donc mort.

   OUVRIR LA SESSION EN LE DEMANDANT, et commencer par le controle - dix secondes, il
   doit cesser de rendre 500 :
   curl -s -o /dev/null -w "%{http_code}\n" "https://ft2e-v3.vercel.app/api/auth?provider=github"

   Si la reponse est encore 500, RIEN DANS LE DEPOT N'EST EN CAUSE et il n'y a rien a
   corriger la : api/auth.js et api/callback.js sont justes, config.yml pointe le bon
   depot depuis le 2026-08-10. Ce qui manque vit dans deux consoles d'administration et
   SEUL L'UTILISATEUR PEUT LE FAIRE (la CLI Vercel repond « Not authorized » sur cette
   machine, et elle n'est meme pas installee). Les trois gestes, dans l'ordre, avec leur
   commande de controle, sont dans docs/22-prise-en-main-decap.md § 0 : callback GitHub
   sur https://ft2e-v3.vercel.app/api/callback, puis OAUTH_GITHUB_CLIENT_ID et
   OAUTH_GITHUB_CLIENT_SECRET sur le projet Vercel, puis redeploiement.

   ATTENTION - l'utilisateur a AJOURNE ce point le 2026-08-17 en connaissance de cause.
   Ce n'est donc pas un oubli a rattraper de force : c'est une decision a lui rappeler
   une fois, en ouverture, puis a respecter. Tant qu'il n'est pas leve, la section C du
   script de demonstration - que le script appelle lui-meme « le moment cle » - ne peut
   pas avoir lieu, et la prise en main par FT2E ne peut pas commencer.

   ATTENTION - NE PAS AJOUTER UN AVERTISSEMENT DE PLUS. Le fait est deja ecrit dans
   CLAUDE.md, dans docs/22 § 0, dans le pre-vol du script de demonstration et en
   commentaire de public/admin/config.yml. Il a survecu six sessions SOUS FORME DE
   COMMENTAIRE : un commentaire n'echoue jamais. Ce qui manque est une execution hors
   depot, pas une cinquieme mention.

2. L'ETAT DU DEPOT A L'OUVERTURE - la session 8 n'a produit qu'une consignation de
   portee docs. MAIS CE DEPOT EST PARTAGE, et c'est le constat le plus utile de S8 :
   pendant la session, SIX COMMITS chore(deploy) s'y sont intercales et ont ete POUSSES
   par un hook Stop, sans aucun rapport avec son travail (un script de captures de
   portfolio, scripts/captures/portfolio.mjs, plus package.json et .gitignore). Ne
   jamais supposer que le depot est reste ou on l'a laisse.
   LE VERIFIER, en dix secondes et EN DEUX TEMPS, parce que ni l'un ni l'autre ne
   suffit seul :
   a. git ls-remote origin master - a comparer au HEAD local ; la reference locale
      (origin/master) peut etre perimee et mentir.
   b. un MARQUEUR DU BUILD dans le HTML servi - git ls-remote prouve que GitHub a le
      code, PAS que Vercel a construit depuis. Marqueur disponible, present sur les
      46 pages depuis le 2026-08-16 - la baseline du monogramme :
      curl -s https://ft2e-v3.vercel.app/ | grep -c "BUREAU D’ÉTUDES TECHNIQUES"
      L'apostrophe y est TYPOGRAPHIQUE : retapee droite, le grep rend 0 et fait
      conclure a tort que le deploiement est perime. La copier, ne pas la retaper.
   c. ET REVERIFIER AU MOMENT DE COMMITTER, pas seulement a l'ouverture. « Rien n'est
      en attente de push » est une mesure PERISSABLE sur un depot ou un hook commite
      tout seul : en S8 elle est devenue fausse en trois heures, en silence.
   En S6, le site en ligne s'etait arrete TROIS SESSIONS en arriere sans que rien ne le
   signale. Jamais par un delai d'attente : toujours par un marqueur.
   ATTENTION SUR LA PORTEE D'UN MARQUEUR : il prouve « pas plus ancien que », JAMAIS
   « exactement ce commit ». La baseline est servie par tout build posterieur au
   2026-08-16 et ne distingue pas deux commits de cette periode. Pour trancher qu'un
   deploiement porte LE commit en cours, il faut un marqueur introduit PAR CE COMMIT -
   sinon on ne mesure qu'un plancher de date.

3. LES DEUX POINTS AJOURNES - ne PAS les rouvrir sans que l'utilisateur le demande. Ils
   sont en suspens jusqu'a la presentation du projet, a sa demande explicite du
   2026-08-16, reconduite le 2026-08-17. Les redire en fin de session, ne rien executer
   dessus, ne rien fabriquer :
   a. Reception de la creche de l'Oranger - src/content/projets/creche-oranger-perigny.md
      annonce une affaire livree sans dire quand : annee_livraison vide, ligne statut
      absente. Seule des 23 dans ce cas. NE PAS FABRIQUER DE MILLESIME.
   b. planche-chiffree - seul archetype de la liste fermee du protocole que les 23
      planches n'ont pas exerce, donc le seul dont rien ne garantit qu'il fonctionne.
      Le retirer ou le redefinir est un arbitrage editorial.
   ATTENTION - un seul des deux porte une echeance propre : la reception de la creche
   est le premier des quatorze releves qu'appelle MILLESIME_LIVRAISON_ANNONCE, et le
   garde-fou de S4 fera ECHOUER LE BUILD au 1er janvier 2027. Ne jamais y repondre en
   poussant la constante : cela desarmerait le garde-fou pour s'epargner exactement
   l'echec qu'on lui demande de produire. La reponse est d'aller relever les receptions
   aupres de FT2E.

4. CE QUE LA SESSION FAIT D'AUTRE - a definir avec l'utilisateur en ouverture. Rien
   n'est programme, et la session 8 n'a rien laisse en cours. Les candidats connus,
   aucun ouvert d'office :
   - les insecables du CORPUS DESSINE : 12 ecarts de ponctuation subsistent dans les
     planches SVG. NE PAS lancer scripts/injection-typographique.py dessus : il DEPLACE
     LE DESSIN, les compositeurs mesurant leurs chaines pour poser la geometrie et
     U+202F n'ayant pas la chasse d'une espace ordinaire. C'est un chantier avec
     regeneration des 23 dossiers et controle du rendu, pas une passe de correction ;
   - la regeneration des vingt planches anterieures a la 21 (point ouvert le plus ancien,
     docs/superpowers/plans/2026-08-12-chantier-planches-references.md) ;
   - les 7 marqueurs [DEMO] restants, tous des image_alt de src/content/secteurs/, qui
     se levent au reportage photographique et pas par une validation ;
   - le LCP mobile, qui est AU seuil et non sous le seuil. Sept mesures sur les deux
     pages les plus lourdes : 1 656, 1 658, 1 681, 1 768, 1 806, 1 807 et 1 815 ms pour
     un budget de 1 800. Elles se repartissent de part et d'autre du seuil SANS qu'aucune
     page ne soit systematiquement du mauvais cote - c'est l'accueil qui bascule sur un
     tir, /equipe/ sur un autre. NE PAS traiter cela comme un defaut de /equipe/ : ce
     serait optimiser la mauvaise page. La fiche projet, elle, descend a 1 068 ms ;
   - livrables/cv-ft2e/CV-FT2E.zip est non suivi dans un repertoire qui n'est pas ignore
     (releve en S8, non traite). Sans incidence sur le build. Trois issues : suivre,
     ignorer, retirer - c'est une decision de l'utilisateur, pas un defaut a corriger.

Pieges verifies au depot, a ne pas redecouvrir :
- UN BUILD VERT NE PROUVE MEME PAS QUE LE TEXTE EXISTE. En S7, une passe de correction
  a ecrit ses references arriere \1 \2 \3 comme caracteres de controle U+0001-0003 et
  a DETRUIT trois libelles de l'accueil et de /societe/ ; npm run build a produit ses
  46 pages sans broncher. Seul astro check a proteste, et pour une raison indirecte (il
  serialise l'AST en JSON, qui interdit les caracteres de controle nus). Corollaire :
  apres toute correction de texte, controler la PRESENCE du texte attendu - une mesure
  d'absence de defaut ne distingue pas « corrige » de « supprime ».
- Les insecables sont normalisees EN ENTREE des outils d'edition, ET CE N'EST PAS
  DETERMINISTE : en S7 le meme script litteral est passe une fois puis a echoue la
  suivante. Trois consequences. (1) Tout script qui manipule des insecables doit porter
  une ASSERTION D'AUTO-CONTROLE en tete - c'est elle qui a empeche la seconde ecriture
  destructrice. (2) Les caracteres sensibles se CONSTRUISENT par chr(0xA0) / chr(0x2019),
  jamais en litteral et pas davantage en echappement \u00a0 : l'echappement a echoue
  deux fois avant que ce soit clair, un appel de fonction ne peut pas etre reecrit en
  route. (3) Un instrument dont les insecables ont ete normalisees signale comme
  fautives LES PAGES LES MIEUX COMPOSEES, parce que .replace('&nbsp;', NBSP) y injecte
  des espaces ordinaires - deux releves de S7 l'ont fait, sur des pages legales.
  La recette qui a marche en S8, et qui est rejouable : ecrire le contenu en clair avec
  des JETONS pour les seuls caracteres sensibles, les substituer en fin de course par
  chr(), et asserter que le SOURCE DU SCRIPT n'en contient aucun en litteral - s'il n'y
  en a pas, il n'y a rien qu'un outil ait pu normaliser en silence. Mesure faite en S8 :
  les lettres accentuees (e accent aigu, E accent aigu), les guillemets, les points de
  suspension et les fleches traversent l'ecriture intacts ; seules les insecables sont
  effacees. Ne pas tokeniser plus que necessaire, le texte en deviendrait illisible.
- Une ancre de remplacement se COPIE du fichier, elle ne se retape pas : le corpus
  melange apostrophes droites et typographiques, et une ancre retapee echoue en disant
  seulement « 0 occurrence ». Le plan de dette porte plus de 200 U+00A0 et 75 U+202F :
  l'editer passe obligatoirement par un script Python, avec comptage AVANT et APRES et
  une assertion que chaque ancre est presente EXACTEMENT UNE FOIS.
- La PERFORMANCE ne se mesure JAMAIS sur npm run preview, qui ne compresse rien :
  0,8 s de biais sur la chaine bloquante. Elle se mesure sur le deploiement, apres avoir
  verifie par un MARQUEUR DU BUILD - jamais par un delai d'attente - qu'il porte le
  commit en cours. Et une seule mesure ne conclut pas : le LCP des deux pages les plus
  lourdes passe de 1 656 a 1 815 ms d'un tir a l'autre, de part et d'autre du seuil, et
  ce n'est pas toujours la meme qui bascule.
- npx lighthouse est un processus Windows et n'accepte PAS les chemins Git-Bash
  /c/... en --output-path : il n'ecrit rien, en silence, et le script conclut « aucun
  JSON ». Se placer dans le repertoire et passer un chemin relatif. Meme famille, releve
  en S8 : /tmp n'existe pas depuis ce shell - ecrire dans le repertoire temporaire de la
  session, sous peine d'un FileNotFoundError au milieu d'une mesure.
- Chrome refuse toute fenetre sous 500 px, EN HEADLESS AUSSI : une capture en
  --window-size=390,900 compose la page a ~500 px puis ROGNE l'image, ce qui montre un
  debordement credible et faux. Les largeurs de telephone se mesurent par une IFRAME
  servie en meme origine. Deux biais de cette sonde : caler sur onload ET sur la
  presence d'un element de la page (le about:blank initial a la largeur du cadre) ; et
  les media queries comptent la barre de defilement que clientWidth ne compte pas, soit
  15 px d'ecart - sans consequence sur une echelle, decisif sur une borne.
- Une sonde en iframe dont le sentinelle de resultat apparait LITTERALEMENT dans son
  propre <script> se fait extraire son code source au lieu de son resultat. Construire
  le sentinelle a l'execution.
- --user-data-dir fait echouer --dump-dom de Chrome EN SILENCE : code de sortie 0 et
  aucune sortie. Le meme appel sans l'option rend le document complet.
- Des serveurs astro preview de sessions anterieures tournent encore. Ce n'est pas grave
  en soi (astro preview sert le DISQUE, donc tous servent le dist/ courant) - le vrai
  risque est de mesurer SANS AVOIR REBUILD. Apparier le serveur a son dist par un
  marqueur depose dans dist/ et relu par curl.
- L'accueil est recue a 96 en accessibilite et /societe/ a 97, et c'est admis :
  l'exception D1 a ete portee SUR LE MOTIF en S7, et non plus sur la seule page. La
  condition reste stricte - la SEULE violation doit etre le color-contrast d'un
  complement de titre aria-hidden. Elle se declenche exactement la ou ce complement est
  pose sur un APLAT PLEIN, qu'axe sait resoudre ; ailleurs le papier trame l'empeche de
  conclure et l'outil s'abstient. Un score non explique dans un compte rendu est
  indistinguable d'une regression.
- Le SEO plafonne a 69 sur toutes les pages, et l'unique audit en echec est
  is-crawlable. C'est le verrou d'indexation, pas un defaut. Ne pas le « corriger ».
- Tailwind v4 elague les variables de theme qu'aucune classe n'emploie. Une couleur
  s'ecrit en CLASSE litterale (stroke-encre), jamais en var(--color-...) dans un attribut
  SVG. Et une mesure de mise en page (un plafond, une borne) s'ecrit en CSS de composant
  plutot qu'en classe arbitraire unique, pour la meme raison.
- Dans un frontmatter .astro, une sonde de typage se fait en REMPLACANT un attribut,
  jamais en en ajoutant un second - un attribut duplique ne leve aucune erreur. Et
  ts(6196) sur une interface Props ne dit pas « code mort », il dit « contrat non
  consomme ».
- Le depot porte un .gitattributes depuis le 2026-08-16 : ne pas le retirer. Sans lui,
  un clone neuf sort les 92 pieces des planches en CRLF et l'invariant de regeneration
  se lit comme rompu alors qu'il tient.
- L'enumeration « Etudes d'execution » s'ecrit depuis S7 avec l'APOSTROPHE
  TYPOGRAPHIQUE, dans src/content.config.ts, public/admin/config.yml et six fiches.
  L'appariement fiche/secteur se fait en egalite de chaines : une fiche redigee hors
  Decap avec l'ancienne graphie fait echouer le build. C'est voulu.

Recette de fin de session : npm run typecheck (0 erreur), npm run build (46 pages),
python scripts/controle-liens-internes.py (0 lien mort), controle du RENDU de toute page
touchee a sa largeur de lecture, et consignation dans le plan. Si la session ne touche
pas src/, le dire explicitement plutot que de laisser croire a une recette non jouee.

Portee de commit : plusieurs commits nets valent mieux qu'un fourre-tout - les portees
sont content, docs, fix, design-system selon les points.

Termine par le prompt de lancement de la session suivante, en annexe du plan et
reproduit integralement dans ton message final. Cette regle est dans CLAUDE.md parce
qu'elle a ete manquee deux fois.
````
