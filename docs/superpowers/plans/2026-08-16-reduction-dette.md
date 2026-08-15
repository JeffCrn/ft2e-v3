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
> **Ouvert le 2026-08-16.** État : 0 session sur 4 exécutée.

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

⚠ **Deux pièges de mesure propres à cette machine**, tous deux en mémoire :
Chrome refuse toute fenêtre sous 500 px — les mesures à 390 px passent par une
**iframe servie en même origine** par `npm run preview` ; et `browser_resize` de
Playwright **persiste** d’un appel à l’autre, ce qui fait passer une page saine pour
cassée. Toujours restaurer la taille après mesure.

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
| S1 — pipeline d’images | ☐ à faire | — | — |
| S2 — planches : typo + régénération | ☐ à faire | — | — |
| S3 — trois défauts de rendu | ☐ à faire | — | — |
| S4 — hygiène et garde-fous | ☐ à faire | — | — |
| D1 — arbitrage A2 × Lighthouse | ☐ à poser | — | — |
| D2 — trois questions à FT2E | ☐ à poser | — | — |

---

## Annexe — prompt de lancement de la session 1

> À coller tel quel dans une session neuve. Il est écrit pour être autoportant :
> il ne suppose aucun contexte de la session d’audit.

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
