# Protocole — planche de schéma de principe pour une fiche référence FT2E

*Révision 3 (2026-08-12). Le corps de ce document se colle tel quel en début de session
neuve : rien d'autre n'y est supposé connu. Il est versionné ici parce qu'il pilote la
production de vingt-deux planches restantes, et qu'un protocole qui vit hors du dépôt ne
survit pas à un nettoyage de répertoire de travail.*

**Où sont les pièces**

| | |
|---|---|
| Ce protocole | `docs/superpowers/specs/2026-08-12-planches-references-protocole.md` |
| Compositeurs | `scripts/planches/<archetype>.py` — un module par archétype |
| Suivi du chantier | `docs/superpowers/plans/2026-08-12-chantier-planches-references.md` |
| Planches publiées | `public/images/projets/<slug>/planche.{json,svg,png}` + `vignette.svg` |
| Rendu | `src/components/blocs/PlancheReference.astro` |

---

## Répartition du travail — ce qui a changé en révision 3

La révision 2 demandait à la session de génération d'écrire elle-même le SVG. À
l'exécution de la première planche, cette division s'est révélée fausse : **l'extraction
est un travail de lecture, la composition un travail de calcul**, et les mêler faisait
retomber sept défauts de géométrie sur un raisonnement par ailleurs juste.

- **La session de génération produit `planche.json`.** C'est le travail irréductible :
  lire la fiche entière, choisir l'archétype, extraire des valeurs littérales, consigner
  chaque arbitrage dans `a_valider_ft2e`. C'est la pièce que FT2E relit, et c'est aussi
  la source du repli de lecture que le site sert sous 1024 px.
- **Le dépôt compose les dessins**, par `scripts/planches/<archetype>.py` : géométrie
  calculée, jamais tapée, et bloc `controles` recalculé à chaque exécution.
- **Si l'archétype n'a pas encore son module**, la session écrit aussi le SVG en suivant
  le gabarit ci-dessous ; sa géométrie est ensuite portée dans un module, et la planche
  régénérée pour vérifier qu'elle est reproductible.

> **Ce qui change depuis la révision 1** — la révision 1 composait une planche imprimée de
> 1500 × 1000 sans avoir mesuré la page qui devait l'accueillir : à la largeur réelle du
> site, son mono de 11 px se rendait à 8,4 px, et à 4,3 px dans la colonne d'origine.
> La révision 2 recale le gabarit sur **1200 × 800**, qui est la largeur du conteneur du
> site — les corps de la planche deviennent alors les corps de la charte. Elle corrige
> aussi le nom de la famille de police (faux depuis l'origine), tranche la question
> hexadécimal / `var()` qui était laissée ouverte, impose le nommage des fichiers, et
> ajoute deux livrables que le site réclame : un cadrage de vignette et un JSON
> suffisant pour recomposer la planche en texte sur téléphone.
> **Les règles dures 1 à 4 sont inchangées : elles sont le cœur du dispositif.**
>
> **Révision 2.1** — quatre corrections relevées à la composition de la première
> planche (École des douanes), toutes trouvées au temps 4 et aucune au temps 3 :
> la casse des unités, le choix d'insécable selon le corps, la pleine largeur de
> la phrase de principe, et ce qui peut entrer dans un cadrage de vignette.

---

## Contexte

FT2E est un bureau d'études techniques de La Rochelle (CVC, électricité CFO/CFA, SSI,
thermique, BIM). Son site de références est illustré par des extraits de plans et des
perspectives issus des dossiers d'affaires. L'audit distingue deux familles, toutes deux
fautives :

- **neuf perspectives et vues aériennes** dues à des architectes tiers ou à un opérateur
  de drone non identifié, publiées sans qu'aucun crédit ait jamais été obtenu ;
- **douze extraits de nos propres plans** : le trait est FT2E, mais le fond de plan est la
  géométrie de l'ouvrage, donc l'œuvre de l'architecte, reproduite à l'identique.

La substitution retenue : **ne plus montrer l'ouvrage, montrer le raisonnement.**
Chaque fiche reçoit une planche dessinée à partir de sa propre matière technique —
topologie, traversée, flux, chiffres — sans aucune géométrie d'autrui.

Ta tâche : produire cette planche pour la fiche que je vais te désigner.

---

## Ce que tu produis

Un dossier nommé d'après le slug de la fiche, contenant **exactement quatre fichiers** :

```
<slug>/
├── planche.json     l'extraction — la pièce que FT2E relit, et la source du repli de lecture
├── planche.svg      la planche de fiche, viewBox 0 0 1200 800
├── vignette.svg     la vignette de carte, viewBox 0 0 300 200
└── planche.png      rendu de contrôle et source de l'og:image, 2400 × 1600
```

Pas d'autre nom, pas de préfixe `ref_NNN`, pas de nom d'ouvrage dans les noms de fichiers :
ils sont copiés tels quels dans `public/images/projets/<slug>/` et tout renommage est une
occasion d'erreur. Le composant les charge par convention de nom — un fichier manquant
fait échouer le build, ce qui est le comportement voulu.

### La vignette est une COMPOSITION, jamais un recadrage

C'est la correction la plus coûteuse de la première planche, et elle mérite d'être
comprise plutôt que suivie.

La vignette a d'abord été un rectangle 3:2 découpé dans la planche, écrit par
l'extraction. Il a fallu **trois cadrages successifs** pour qu'elle ne coupe ni un mot, ni
le filet séparateur des colonnes, ni la colonne des valeurs — et le troisième restait un
compromis. La raison est arithmétique et aucun cadrage ne pouvait y échapper : *un dessin
composé pour 1200 px et donné à lire à 290 tombe à l'échelle 0,24, quel que soit l'endroit
où on le découpe.*

`vignette.svg` est donc composée dans son propre repère de **300 × 200**, soit l'échelle
0,91 à 0,99 des cartes de projet mesurées (274 à 296 px). Elle garde de la planche ce qui
porte la thèse — la géométrie et les nœuds chiffrés — et laisse le reste :

| Ce que la vignette garde | Ce qu'elle laisse |
|---|---|
| le motif de l'archétype, entier | le titre d'ouvrage — la carte l'affiche juste dessous |
| les nœuds ou totaux, avec leur valeur | le relevé et le relevé secondaire |
| un surtitre mono de 9 px, trois mots au plus | la phrase de principe, le cartouche, les libellés de poste |

Six libellés dans 300 px de large ne se lisent pas. Les taire est une décision ; les
rogner en était une aussi, mais subie.

---

## Entrée

Le markdown complet de la fiche : frontmatter et corps.

Le dépôt est public : `https://github.com/JeffCrn/ft2e-v3`, branche `master`.
Tu peux le cloner (`git clone --depth 1`) et lire `src/content/projets/<slug>.md`.
Le site déployé bloque les robots — n'essaie pas de le récupérer.

Si je ne t'ai donné ni slug ni fiche, demande-la. Ne devine pas.

---

## Méthode

### Temps 1 — Lire la fiche entière

Frontmatter **et** corps. Le corps porte la thèse ; le frontmatter porte les chiffres.
Ne travaille jamais depuis un résumé ou depuis la page rendue.

### Temps 2 — Extraire

Choisis **un** archétype dans cette liste fermée, sur la **thèse de la fiche** — jamais
sur son secteur déclaré ni sur sa liste de missions :

| Clé | Emploi |
|---|---|
| `boucle-fluide` | Production → distribution → terminaux |
| `coupe-traversee` | Empilement de niveaux, traversées, réservations |
| `tableau-electrique` | Arrivée → TGBT → départs |
| `sankey-energie` | Flux énergétiques à largeur proportionnelle |
| `zonage-ssi` | Catégorie, zones de détection et de mise en sécurité |
| `chronologie-affaire` | Jalons contractuels et diffusions |
| `planche-chiffree` | Repli typographique |

Justifie le choix en une à trois phrases. Si je t'indique les archétypes déjà employés
sur d'autres fiches, tiens-en compte : vingt-trois planches du même archétype ne
constituent pas une série, elles constituent une redite.

Produis ensuite l'objet :

```json
{
  "fiche": "<slug>",
  "archetype": "<clé>",
  "archetype_motif": "<pourquoi celui-là>",
  "titre": "<ouvrage — deux à quatre mots>",
  "sous_titre": "<la thèse, une ligne littérale, 90 signes max>",
  "cartouche_legende": "Ville · 000 m² · 0000",
  "<bloc propre à l'archétype>": { },
  "releve": [ { "valeur": "", "unite": "", "legende": "" } ],
  "releve_secondaire": [ { "intitule": "", "valeur": "", "appui": "" } ],
  "phrase_principe": "<une phrase de la fiche, 120 signes max>",
  "vignette_surtitre": "<TROIS MOTS AU PLUS, CASSE D'AFFICHAGE>",
  "a_valider_ft2e": [ ],
  "exclusions_appliquees": [ ],
  "controles": { }
}
```

`releve` : trois entrées maximum. `releve_secondaire` : deux maximum.

### Temps 3 — Composer, rendre, regarder

Écris le SVG. Rends-le en PNG. **Ouvre le PNG et regarde-le.** Corrige les
chevauchements, les appels de cote mal placés, les zones vides. Itère jusqu'à ce que
la planche tienne. Ne me remets jamais une planche que tu n'as pas vue.

Environnement : `pip install cairosvg --break-system-packages`. Les polices ne sont pas
installées — récupère-les depuis le dépôt Google Fonts vers `~/.fonts`, puis `fc-cache -f` :
`ofl/archivo/Archivo[wdth,wght].ttf` et `ofl/ibmplexmono/IBMPlexMono-Regular.ttf`.

**Rends le PNG depuis une copie du SVG dont tu as retiré le bloc `<style>`.** cairosvg ne
résout pas `var()` : sur le fichier de livraison il rendrait tout en noir, et tu croirais
avoir cassé la palette. C'est le bloc `<style>` qui sert au navigateur, les attributs
hexadécimaux qui servent au rendu de contrôle — les deux disent la même chose.

Le rendu creuse les espaces fines insécables : c'est un artefact du moteur, pas du fichier.

### Temps 4 — Regarder à la taille réelle

Le PNG en pleine page ne prouve rien : **la planche sera lue à 1152 px de large.**
Rends une seconde image à **1152 × 768** et regarde-la. Toute étiquette que tu ne lis pas
à cette taille est à reprendre — pas à agrandir en dernière minute, mais à supprimer ou à
déplacer. Une planche dont on doit zoomer pour lire le propos a manqué son objet.

---

## Règles dures

**1 — Rien qui ne soit littéral.** Toute valeur portée à la planche doit être citable
dans la fiche. Un débit, une puissance, un régime de température, une profondeur qui
n'y figure pas ne peut pas apparaître. *Un chiffre juste posé sur le mauvais organe est
une donnée technique fausse signée par un bureau d'études : c'est la faute la plus grave
que ce dispositif puisse commettre.*

**2 — Ce que le dessin exige et que la source ne fixe pas va dans `a_valider_ft2e`.**
Un dessin tranche ce qu'un texte laisse ouvert : une position, un nombre, une
correspondance, un ordre. Chaque fois que tu tranches, inscris-le — en disant ce que la
source affirme exactement, et ce que le dessin a dû supposer. **Cette liste est le cœur
du dispositif.** Une extraction qui la rend vide est suspecte, pas exemplaire : reprends.

**3 — Exclusions permanentes.** Ne portent jamais au dessin :
- le **numéro d'affaire** (champ `reference`, graphie `NN-NNN`) — il encode le volume
  annuel d'affaires du bureau ;
- tout **montant** : marché, lot, honoraires ;
- les **noms de tiers** : maîtrise d'ouvrage, architecte, BET, installateur, entreprises ;
- toute **donnée d'exploitation** propre au client.

Ces éléments peuvent rester au texte de la fiche. Ils ne passent pas au dessin.

**4 — Aucune géométrie d'autrui.** Le schéma représente un principe : topologie,
succession, traversée, flux, proportion. Jamais un plan, jamais une façade, jamais une
distribution de pièces, jamais une implantation réelle. *La forme architecturale
appartient à l'architecte ; le principe technique appartient à FT2E.* C'est la raison
d'être de toute l'opération — si tu la perds, la planche ne sert à rien.

**5 — Repli plutôt qu'approximation.** Si la fiche ne porte pas trois organes, étapes ou
niveaux identifiables, bascule en `planche-chiffree` et ne remplis que `releve`. Une
planche typographique honnête vaut mieux qu'un schéma vraisemblable.

**6 — Mesurer, pas affirmer.** Contrastes, coordonnées, comptages : chiffre-les dans
`controles`. Si tu dis d'une valeur qu'elle est conforme, montre le calcul.

**7 — Le JSON doit suffire à recomposer la planche sans le dessin.** *(nouveau)*
À 358 px de large — un téléphone — aucun schéma ne se lit : le site y remplace le dessin
par une lecture textuelle bâtie sur le seul JSON. Chaque élément dessiné doit donc porter,
dans son bloc d'archétype, au minimum un `libelle`, une `valeur`, une `unite`, et un
`detail` facultatif — dans **l'ordre de lecture voulu**. Un élément qui n'existe que
comme géométrie est invisible à la moitié des visiteurs.

---

## Charte graphique FT2E — axe monochrome 197°

### Jetons

| Rôle | Variable CSS | Valeur | Emploi |
|---|---|---|---|
| `profond` | `--color-profond` | `#001718` | Réserve. Un cinquième de planche au maximum. |
| `encre` | `--color-encre` | `#00393A` | Texte, titres, filets porteurs. |
| `pivot` | `--color-pivot` | `#336667` | Données, étiquettes mono, cotes secondaires. |
| `clair` | `--color-clair` | `#99CCCD` | Aplats et filets seulement. **Jamais surface de lecture.** |
| `voile` | `--color-voile` | `#E1F4F4` | N'existe que sur réserve. |
| `papier` | `--color-papier` | `#F7F9FA` | Fond par défaut. |
| `calcaire` | `--color-calcaire` | `#EDF0F2` | Surface secondaire. N'existe que sur papier. |
| filet rang 1 | `--color-filet-1` | `#00393A38` | Porteur — encre 22 %. |
| filet rang 2 | `--color-filet-2` | `#00393A29` | Plan — encre 16 %. |
| filet rang 3 | `--color-filet-3` | `#00393A1F` | Séparation — encre 12 %. |

### Polices — **le nom exact compte**

| Rôle | `font-family` à écrire |
|---|---|
| Texte, titres, chiffres de relevé | `"Archivo Variable", Archivo, "Helvetica Neue", Arial, sans-serif` |
| Étiquettes, cotes, mono | `"IBM Plex Mono", ui-monospace, monospace` |

⚠️ **La famille du site est `Archivo Variable`, pas `Archivo`.** Le paquet
`@fontsource-variable/archivo` n'enregistre aucune famille nommée « Archivo ». Un SVG qui
écrit `font-family="Archivo"` se rend correctement dans ton environnement — où tu as
installé le TTF sous ce nom — et **retombe sur la police système une fois posé dans la
page**. C'est un défaut invisible au contrôle : écris la pile complète ci-dessus, dans cet
ordre, sur chaque nœud de texte.

L'axe de chasse s'écrit `font-variation-settings="'wdth' 112, 'wght' 700"`. Le mono n'a pas
d'axe : graisse 500, interlettrage 0,14 em (soit `letter-spacing` = 0,14 × corps, en
unités du repère), capitales.

### Interdits

- Aucune couleur hors de l'axe 197°. **Aucun gris neutre** : il est hors axe, donc hors système.
- Aucun angle arrondi, aucun dégradé, aucune ombre — le relief vient de la page, pas du fichier.
- Le mono ne sert jamais de texte courant ; Archivo ne sert jamais de cote.
- Jamais voile sur calcaire ni calcaire sur voile — iso-claires à 1,01.
- Jamais `pivot` sur `profond` : 2,85, sous le seuil de 3,0, interdit en texte **et** en filet porteur.
- Une seule réserve profonde par planche. C'est le cartouche de légende.
- **Aucun cadre autour de la planche** : la bordure 1 px et l'ombre sont posées par le site
  (`.plan-pose`). Un cadre dessiné dans le fichier en ferait deux.
- **Pas d'équerres** : la charte les veut en voile, invisible sur fond papier (1,01).
  Le dispositif appartient à la photographie duotone, pas à la planche dessinée.
- Rapport **3:2 exclusivement**. Aucun autre, et notamment aucun carré.

### Casse — l'extraction la porte, le dessin ne la change pas

**Les chaînes destinées au mono s'écrivent dans le JSON DANS LEUR CASSE
D'AFFICHAGE**, capitales comprises. Le générateur ne doit appliquer aucune
transformation de casse.

Motif : une capitalisation automatique écrit « 1 657 M² », « 10,6 KW »,
« W/(M²·K) », « À 16 H ». **Une unité ne se capitalise pas** — le symbole du
kilowatt est `kW`, celui du mètre carré `m²`, et les majuscules y sont fausses,
pas seulement laides. Aucune règle de capitalisation automatique ne connaît la
liste des unités ; celle qui essaierait se tromperait sur la suivante.

Écrire donc : `"UNE SALLE DE COURS DU REZ-DE-CHAUSSÉE · 63 m² · MATIN DE JUILLET"`,
et non la version en bas de casse à capitaliser au rendu.

### Convention numérale

**Deux insécables, et le corps décide laquelle.** Mesuré au rendu dans Archivo
Variable : U+202F vaut **0,098 em**, U+00A0 **0,196 em** — soit 3,93 px contre
7,85 px à 40 px de corps.

| Emploi | Espace | Motif |
|---|---|---|
| Texte courant, mono, détails, légendes | **U+202F** (fine) | c'est la graphie française, et à 10–15 px elle se voit |
| **Chiffres de relevé, corps ≥ 22 px** | **U+00A0** (normale) | sous la fine, « 152 947 » se lit « 152947 » : un groupement de milliers doit se voir d'un coup d'œil, et 3,93 px ne suffit pas à 40 px |

Devant l'unité : `864 m²`, `185 L`, `−4 °C` — fine, sauf au relevé, où
l'unité suit son chiffre : `48 291 W`. Lettres sous dix, chiffres à partir de dix pour les quantités dont le nom
s'écrit en un seul mot (« quatre chambres », « treize logements ») ; chiffres pour les
noms composés (« 21 logements », « 46 chambres ») ; **les unités et les mesures toujours
en chiffres**, quelle que soit la valeur.

---

## Gabarit de composition — **1200 × 800**

Ce n'est pas un format d'impression : **c'est la largeur du conteneur du site.** La planche
s'affiche à 1152 px, soit une échelle de 0,96 — donc les corps que tu écris ici sont, à 4 %
près, les corps que le visiteur lit. C'est la raison d'être de ce gabarit, et la raison
pour laquelle il ne se change pas.

### Structure

- `viewBox="0 0 1200 800"`. **Ni attribut `width` ni attribut `height`** — ils empêcheraient
  la planche de se dimensionner dans la page. `preserveAspectRatio="xMidYMid meet"`.
- Marges de **56** (deux modules). Pas de grille : **28**.
- Largeur utile : 1200 − 112 = **1088**.
- Partition : gouttière de **56**, puis 7/5 sur le reste → **zone de dessin 602**,
  **colonne de relevé 430** (602 / 430 = 1,4000 exactement). Sépare-les d'un filet rang 3.

### Corps — ce sont ceux de la charte, écris-les tels quels

| Élément | Police | Corps | Chasse / graisse | Couleur |
|---|---|---|---|---|
| Surtitre | mono | 11 | 500, 0,14 em, capitales | `pivot` |
| Titre d'ouvrage | Archivo | **30** | wdth 112, wght 700 | `encre` |
| Sous-titre (la thèse) | Archivo | 16 | wdth 100, wght 400 | `pivot` |
| Libellé d'organe ou de poste | Archivo | 15 | wdth 100, wght 400 | `encre` |
| Détail d'appui | mono | 10 | 500, 0,14 em, capitales | `pivot` |
| Chiffre de relevé | Archivo | **40** | wdth 118, wght 700, tabulaire | `encre` (un seul), `pivot` (les autres) |
| Unité du relevé | Archivo | 15 | wdth 100, wght 400 | `encre` ou `pivot`, comme son chiffre |
| Légende de relevé | mono | 10 | 500, 0,14 em, capitales | `pivot` |
| Relevé secondaire | Archivo | 22 | wdth 118, wght 700 | `pivot` |
| Phrase de principe | Archivo | 17 | wdth 100, wght 400 | `encre` |
| Cartouche | mono | 11 | 500, 0,14 em, capitales | `voile` sur `profond` |

**Rien sous 10.** Un texte à 9 dans ce repère se rend à 8,6 px : il n'est pas petit, il est
absent. S'il ne tient pas, il ne va pas sur la planche — il va dans `a_valider_ft2e` ou
dans le JSON.

**Un seul chiffre en encre pleine par relevé** — celui que la fiche défend. Les autres au
`pivot`. C'est la règle du relevé clair de la charte, et elle vaut ici.

### Blocs

- **Bloc de titre** en haut à gauche : surtitre, titre, sous-titre, puis un filet rang 1
  pleine largeur.
- **Zone de dessin** à gauche, sous un en-tête mono qui nomme son périmètre.
  **Colonne de relevé** à droite, sous un en-tête mono qui nomme le sien. Quand les deux
  périmètres diffèrent — un local d'un côté, le bâtiment de l'autre — ces deux en-têtes
  sont ce qui empêche la planche de mentir.
- **Relevé** : jusqu'à trois chiffres, puis un filet rang 3, puis le relevé secondaire.
- **Phrase de principe** en bas de planche, **sur toute la largeur utile** (1088)
  et non dans la seule zone de dessin. Mesure : une phrase de 107 signes en
  Archivo 17 fait 817 px — elle tient sur une ligne à 1088, il lui en faut deux à
  602, et ces deux lignes ne rentrent plus entre la note de pied et le cartouche.
- **Cartouche de légende** en bas à gauche : rectangle `profond`, hauteur **30**, largeur
  ajustée au texte plus 20 de part et d'autre, plafonnée à la largeur de la zone de dessin.
  **Ne code pas une largeur en dur** : elle change à chaque fiche.
  Il porte **`Ville · Surface · Millésime`** — pas le nom de l'ouvrage, que le titre porte
  déjà à 30 px trente centimètres plus haut.

---

## Intégration au site — ce que le fichier doit permettre

### Le SVG sera **inliné**, pas appelé en `<img>`

Un SVG appelé en `src` est un document isolé : il ne reçoit ni les polices ni les variables
de la page. Le site injecte donc le fichier dans le HTML. Conséquences fermes :

- **Pas de `<foreignObject>`, pas de `<image>`, pas de police embarquée, pas de script.**
- **Pas de `<title>` ni de `<desc>`** — ils créeraient une double annonce avec l'`aria-label`.
- Racine : `role="img"` + `aria-label` décrivant **le principe technique**, jamais l'ouvrage.
- **Aucun `id` générique** (`a`, `g1`, `defs`) : un identifiant dupliqué entre deux planches
  d'une même page casse les références. Préfixe tout identifiant par le slug.
- Fichier **sous 40 Ko**.

### Les couleurs s'écrivent deux fois

Attribut de présentation en hexadécimal **et** classe reprise dans un `<style>` interne en
`var()`. En CSS un sélecteur de classe l'emporte toujours sur un attribut de présentation :
le navigateur prend les jetons du site, cairosvg prend l'hexadécimal.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800"
     preserveAspectRatio="xMidYMid meet" role="img" aria-label="…">
  <style>
    .c-encre  { fill: var(--color-encre,  #00393A); }
    .c-pivot  { fill: var(--color-pivot,  #336667); }
    .c-clair  { fill: var(--color-clair,  #99CCCD); }
    .c-voile  { fill: var(--color-voile,  #E1F4F4); }
    .c-profond{ fill: var(--color-profond,#001718); }
    .c-papier { fill: var(--color-papier, #F7F9FA); }
    .s-filet1 { stroke: var(--color-filet-1, #00393A38); }
    .t-sans   { font-family: "Archivo Variable", Archivo, "Helvetica Neue", Arial, sans-serif; }
    .t-mono   { font-family: "IBM Plex Mono", ui-monospace, monospace; }
  </style>
  <rect x="0" y="0" width="1200" height="800" class="c-papier" fill="#F7F9FA"/>
  <text x="56" y="82" class="t-mono c-pivot" fill="#336667"
        font-family="IBM Plex Mono, ui-monospace, monospace"
        font-size="11" font-weight="500" letter-spacing="1.54">SURTITRE</text>
</svg>
```

### Le gabarit de la vignette — 300 × 200

- `viewBox="0 0 300 200"`, marges de 14, `aria-hidden="true"` posé **à la source** : une
  vignette est décorative, elle est toujours doublée du titre de la fiche.
- Surtitre mono **9 px**, en pivot, sur une ligne — 40 signes au plus.
- Le motif occupe la bande médiane ; les étiquettes de nœud sont en Archivo 600 **12 px**,
  leur valeur en mono **10 px** au pivot.
- **Rien sous 9 px**, et rien qui touche un bord.

Le compositeur de l'archétype l'écrit en même temps que la planche : les deux dessins
partagent la même extraction, donc ils ne peuvent pas diverger.

### Le PNG

**2400 × 1600**, fond papier opaque. Il sert de rendu de contrôle, de repli d'impression, et
de source de l'`og:image` de la fiche — que le site produit en **letterbox sur papier**,
jamais en rognage : les vingt-trois fiches partagent aujourd'hui la même image de partage.

---

## Trois pièges déjà rencontrés

**Le duotone du site ne récupérera pas ta planche.** Le sandwich CSS `.duotone-photo`
(`grayscale` + `mix-blend-mode: lighten/darken`) ne mappe correctement que le noir et le
blanc purs : `encre` y ressort à (45, 45, 45), `pivot` à (91, 91, 91) — gris neutres,
hors axe. Compose donc directement dans les jetons, en polarité claire sur `papier`.
Le site **exempte** les planches du duotone et des équerres : ces deux traitements
appartiennent à la photographie.

**Le mono à 11 px n'est lisible que si le gabarit fait 1200.** À 1500 il se rend à 8,4 px
dans la page. C'est le défaut qui a motivé cette révision : une planche peut être
parfaitement composée et parfaitement illisible, et le PNG de contrôle ne le montre pas —
il faut la regarder à 1152 px (temps 4).

**Les espaces fines insécables se perdent en cours de route.** Plusieurs outils
d'écriture normalisent U+202F en espace ordinaire sans le signaler. Après avoir écrit le
SVG, vérifie qu'il en contient encore : `grep -c $' ' planche.svg`. Un compte à zéro
sur une planche qui porte des milliers signifie que le fichier a été normalisé, pas que tu
as oublié de les mettre.

---

## Contrôle avant remise

**Fidélité**
- [ ] Chaque valeur du dessin est citable dans la fiche.
- [ ] `a_valider_ft2e` n'est pas vide.
- [ ] Ni numéro d'affaire, ni montant, ni nom de tiers sur la planche.
- [ ] Aucune géométrie d'ouvrage reproduite.

**Charte**
- [ ] `viewBox="0 0 1200 800"`, sans `width` ni `height`. Aucun angle arrondi.
- [ ] Aucune couleur hors axe, aucun gris neutre, aucune ombre, aucun cadre.
- [ ] Une seule réserve profonde : le cartouche. Sa largeur est calculée, pas codée.
- [ ] Un seul chiffre de relevé en encre pleine ; les autres au pivot.
- [ ] Mono pour les cotes, Archivo pour le texte courant. Pas l'inverse.
- [ ] Aucun corps sous 10.
- [ ] U+202F vérifié par `grep` après écriture ; U+00A0 dans les relevés en grand corps.
- [ ] Aucune unité capitalisée : `m²`, `kW`, `h`, `W/(m²·K)` — le générateur ne transforme pas la casse.
- [ ] Le titre porte l'ouvrage, le cartouche porte ville · surface · millésime. Pas de doublon.

**Intégration**
- [ ] `font-family` écrit avec la pile complète commençant par **`"Archivo Variable"`**.
- [ ] Chaque couleur écrite deux fois : classe `var()` dans `<style>` **et** attribut hexadécimal.
- [ ] `role="img"` + `aria-label` sur la racine, décrivant le principe et non l'ouvrage.
- [ ] Aucun `<title>`, `<desc>`, `<image>`, `<foreignObject>`, `<script>`. Identifiants préfixés par le slug.
- [ ] SVG sous 40 Ko.
- [ ] `vignette_surtitre` rempli, trois mots au plus, dans sa casse d'affichage.
- [ ] `vignette.svg` composée à 300 × 200, `aria-hidden` à la source, rien sous 9 px, rien qui touche un bord.
- [ ] Le bloc d'archétype du JSON porte libellé, valeur, unité et ordre pour chaque élément dessiné.
- [ ] Quatre fichiers — `planche.json`, `planche.svg`, `vignette.svg`, `planche.png` — dans un dossier `<slug>/`.

**Rendu**
- [ ] Le PNG 2400 × 1600 a été rendu **et regardé**.
- [ ] Le rendu à **1152 × 768** a été regardé, et toute étiquette illisible à cette taille a été traitée.
- [ ] La vignette a été regardée **dans une carte de 296 px et de 274 px**, pas isolée.

---

## Format de ta réponse

Les trois fichiers. Puis, en prose brève : l'archétype retenu et son motif, la liste des
arbitrages laissés à FT2E, ce que tu as dû exclure, et ce que le rendu à 1152 px t'a fait
corriger.

Ne me raconte pas ta méthode. Montre le résultat et ce qui reste ouvert.
