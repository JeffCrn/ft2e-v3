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
> **Ouvert le 2026-08-16.** État : **3 sessions sur 4 exécutées** (S1, S2, S3), **1 décision sur 2 tranchée** (D1).

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
2. **40 px de vide mort sous `sm` dans le hero de l'accueil** : le média est
   `hidden sm:block`, mais sa cellule de grille et le `gap-10` du conteneur restent.
   Sans effet sur le CLS ni sur le débordement.

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
| S2 — planches : typo + régénération | ☑ **faite** le 2026-08-16 | `+1` | ✅ **complète** — **0** apostrophe droite dans les 23 extractions, les 69 `<text>` et les 69 `aria-label` (1 694 courbées) ; régénération **23 / 23** octet à octet ; rendu inchangé hors apostrophes et cartouches (9 bandes de pixels sur 5 200) ; build vert. **Trouvé au passage : une collision `XB0` entre deux mécanismes de `tableau-electrique.py`, qui recomposait faux la planche de la crèche** |
| S3 — trois défauts de rendu | ☑ **faite** le 2026-08-16 | `806e803` | ✅ **complète** — CLS **0** sur `/`, `/contact/`, `/references/` et `/equipe/` (seuil 0,05) ; `/contact/` a11y **97 → 100** ; débordement nul sur 45 mesures (15 routes × 3 largeurs) et à 320 / 360 / 390 / 430 px ; accueil perf **100** |
| S4 — hygiène et garde-fous | ☐ à faire | — | — |
| D1 — arbitrage A2 × Lighthouse | ☑ **tranché** le 2026-08-16 — issue 2 (inscrire l’exception, viser 96) | `4416c20` · `806e803` | ✅ **appliqué** à `.claude/rules/accessibility-rgaa.md` en S3 |
| D2 — trois questions à FT2E | ☐ à poser | — | — |

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
