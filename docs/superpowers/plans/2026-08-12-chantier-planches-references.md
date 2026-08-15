# Chantier des planches de références — programme et suivi

> **Objet.** Substituer, sur les 23 fiches de références, un dessin FT2E aux visuels
> actuels. **Ouvert le 2026-08-12. 20 planches publiées sur 23.**
>
> **Protocole de production :** `docs/superpowers/specs/2026-08-12-planches-references-protocole.md`
> **Compositeurs :** `scripts/planches/<archetype>.py`

---

## Pourquoi ce chantier

Les visuels en place posent deux problèmes distincts, et le second n'est pas le moins grave.

**Le droit d'auteur.** Neuf fiches montrent une perspective d'architecte ou une vue
aérienne : UBIK, SMART Architecte, ASP, ABP, BTB, un opérateur de drone non identifié. Le
tableau du chantier des références les marque toutes « crédit à confirmer / à obtenir → E ».
**Aucun crédit n'a jamais été obtenu.** Douze autres fiches montrent un extrait de nos
propres plans : le trait est FT2E, mais le fond de plan est la géométrie de l'ouvrage,
donc l'œuvre de l'architecte, reproduite à l'identique.

**La démonstration.** Un extrait de plan au 1/50 réduit à 581 px est réduit d'un facteur 5,
puis passé au `grayscale(100%)` du duotone — qui efface les couleurs de réseaux,
c'est-à-dire la clé de lecture du plan. Le code en portait l'aveu : sur `/references`, la
miniature était `hidden md:block` **et** `aria-hidden="true"`. Elle ne portait rien.

**La substitution retenue : ne plus montrer l'ouvrage, montrer le raisonnement.** Une
planche est dessinée à partir de la matière technique de la fiche — topologie, flux,
chiffres — sans aucune géométrie d'autrui, sans nom de tiers, sans donnée commerciale.
Elle démontre au lieu d'illustrer : un diagramme de flux *prouve* une proportion, une
façade l'affirme.

---

## État — 20 / 23

| № | Fiche | Secteur | Archétype | État |
|---|---|---|---|---|
| 01 | `ecole-des-douanes-rue-du-jura-la-rochelle` | Monotechnique | `sankey-energie` | ✅ **publiée** |
| 02 | `abbaye-sablonceaux-ssi` | Patrimoine | `zonage-ssi` | ✅ **publiée** |
| 03 | `ancien-siege-communautaire-marennes` | Tertiaire / ERP | `coupe-traversee` | ✅ **publiée** (versée le 2026-08-13) |
| 04 | `atelier-dufour-yachts-perigny` | Industriel et commercial | `boucle-fluide` | ✅ **publiée** (versée le 2026-08-13) |
| 05 | `ateliers-pilotes-capsulae` | Industriel et commercial | `boucle-fluide` (mécanisme `utilites`) | ✅ **publiée** (versée le 2026-08-13) |
| 06 | `centre-formation-ormeau-du-pied-saintes` | Tertiaire / ERP | `boucle-fluide` (mécanisme `substitution`) | ✅ **publiée** (versée le 2026-08-13) |
| 07 | `creche-oranger-perigny` | Tertiaire / ERP | `tableau-electrique` (mécanisme `autoconsommation`) | ✅ **publiée** (versée le 2026-08-13) |
| 08 | `cuisine-groupe-scolaire-villedoux` | Tertiaire / ERP | `coupe-traversee` (mécanisme `equilibre`) | ✅ **publiée** (versée le 2026-08-13) |
| 09 | `ehpad-coulonges-sur-autize-ssi` | Coordination SSI | `zonage-ssi` (mécanisme `transfert`) | ✅ **publiée** (versée le 2026-08-14) |
| 10 | `etude-notariale-boulevard-joffre` | Tertiaire / ERP | `coupe-traversee` (mécanisme `enjambement`) | ✅ **publiée** (versée le 2026-08-14) |
| 11 | `exe-residence-horizon-mediatim` | Études d'exécution / BIM | `chronologie-affaire` (mécanisme `precedence`) | ✅ **publiée** (versée le 2026-08-14) |
| 12 | `fougerou-sainte-marie-de-re` | Logements | `boucle-fluide` (mécanisme `declinaison`) | ✅ **publiée** (versée le 2026-08-14) |
| 13 | `habitat-inclusif-salignac-sur-charente` | Logements | `zonage-ssi` (mécanisme `partage`) | ✅ **publiée** (versée le 2026-08-14) |
| 14 | `hotel-yachtman-quai-valin-la-rochelle` | Tertiaire / ERP | `coupe-traversee` (mécanisme `portee`) | ✅ **publiée** (versée le 2026-08-14) |
| 15 | `logements-maubec-chagnolet` | Logements | `sankey-energie` (mécanisme `plafonds`) | ✅ **publiée** (versée le 2026-08-15) |
| 16 | `logements-nerea-aytre` | Logements | `sankey-energie` (mécanisme `dedoublement`) | ✅ **publiée** (versée le 2026-08-15) |
| 17 | `logements-pas-des-boeufs-bois-plage` | Logements | `boucle-fluide` (mécanisme `appariement`) | ✅ **publiée** (versée le 2026-08-15) |
| 18 | `maison-relais-saint-jean-d-angely` | Logements | `boucle-fluide` (mécanisme `individualisation`) | ✅ **publiée** (versée le 2026-08-15) |
| 19 | `maisons-tourtet-saint-georges-de-didonne` | Logements | `chronologie-affaire` (mécanisme `divergence`) | ✅ **publiée** (versée le 2026-08-15) |
| 20 | `passerelle-ecluse-carreau-d-or-marans` | Monotechnique | `tableau-electrique` (mécanisme `franchissement`) | ✅ **publiée** (versée le 2026-08-15) |
| — | `place-des-chenes-verts-saint-rogatien` | Industriel et commercial | | à faire |
| — | `residence-intergenerationnelle-saint-agnant` | Logements | | à faire |
| — | `siege-rese-aigrefeuille` | Tertiaire / ERP | | à faire |

**Registre des archétypes employés** — à tenir à jour, il conditionne la variété de la série :

| Archétype | Employé | Module |
|---|---|---|
| `sankey-energie` | 3 — trois mécanismes : le flux à largeur proportionnelle (École des douanes), `plafonds` (la proportion sans flux — trois pistes à échelle commune, le plafond carbone qui tombe au tiers à la frontière réglementaire et commande le générateur, logements Maubec à Chagnolet) et `dedoublement` (la partition contractuelle — un permis contigu qui fourche en deux marchés à 3 px par logement, une bande calcaire unique qui traverse les deux flux, le BET fluides commun ; les arrivées en segments comptent les bâtiments, logements Néréa à Aytré) | ✅ `scripts/planches/sankey-energie.py` (dispatch sur le bloc de l'extraction) |
| `zonage-ssi` | 3 — trois mécanismes : `zonage` (un même déclenchement, l'alarme avant/après — Abbaye de Sablonceaux), `transfert` (la mise à l'abri au même niveau, la descente barrée — EHPAD de Coulonges-sur-l'Autize) et `partage` (le découpage réglementaire d'une enveloppe montée d'un seul tenant — la limite sans mur qui commande l'étanchéité, les machines et l'incendie, habitat inclusif de Salignac-sur-Charente) | ✅ `scripts/planches/zonage-ssi.py` (dispatch sur le bloc de l'extraction) |
| `boucle-fluide` | 6 — six mécanismes : `boucle` (récupération, Atelier Dufour), `utilites` (réseau de livraison, Ateliers Capsulae), `substitution` (production réversible, centre de formation de Saintes), `declinaison` (le parti répété — une maison dessinée une fois, 54 cellules identiques en `<defs>`/`<use>`, Le Fougerou), `appariement` (la partition des services — trois bandes de service, deux colonnes de machines, et dans chaque colonne UNE boîte qui enjambe une frontière de bande, jamais la même : l'eau chaude porte la ventilation chez les T2, le chauffage porte l'eau chaude chez les T3 ; contour d'encre dominant la frontière filet-1, logements du Pas des Bœufs au Bois-Plage) et `individualisation` (le collectif produit, chaque logement compte — deux flux collectifs entrent dans une colonne qui dessert une pile de 21 modules identiques en trois groupes typologiques ; UN module tiré au détail par deux filets d'agrandissement montre deux arrivées, trois départs, trois compteurs, maison relais de Saint-Jean-d'Angély) | ✅ `scripts/planches/boucle-fluide.py` (dispatch sur le bloc de l'extraction) |
| `coupe-traversee` | 4 — quatre mécanismes : `coupe` (l'enveloppe traversée, Marennes), `equilibre` (l'air extrait, l'air compensé — restaurant scolaire de Villedoux), `enjambement` (l'enveloppe qui ferme les faces qu'un bâtiment ordinaire n'a pas — dessous du plancher sur le passage, fosse d'ascenseur, abouts pontés — étude notariale Joffre) et `portee` (deux périmètres inégaux sur une même coupe de niveaux — la mission bornée au coin bas-gauche, l'enceinte de la zone d'alarme qui enclot tout, hôtel Le Yachtman) | ✅ `scripts/planches/coupe-traversee.py` (dispatch sur le bloc de l'extraction) |
| `tableau-electrique` | 2 — deux mécanismes : `autoconsommation` (la toiture est la seconde arrivée du tableau, crèche de l'Oranger) et `franchissement` (le sujet n'est plus la distribution mais ce que les départs TRAVERSENT — une arrivée, une barre, cinq départs, et trois frontières : la tension, où deux départs d'éclairage changent de poids de trait en sortant des blocs 48 V ; le joint mobile, où deux cotes se rejoignent en sens contraire, 10 m de câble d'un côté contre 6,80 m de course de l'autre, à la même échelle ; la limite du réseau public, où une descente barrée d'une croix vers un mât jamais construit répond à un mât dédié plus court, alimenté depuis la barre par le plus long des départs — passerelle du Carreau d'Or à Marans) | ✅ `scripts/planches/tableau-electrique.py` (dispatch sur le bloc de l'extraction) |
| `chronologie-affaire` | 2 — deux mécanismes : `precedence` (le dessin précède le gros œuvre : l'escalier des réservations gravit les niveaux d'avance sur l'exécution, résidence Horizon) et `divergence` (l'écart qui se creuse — une ordonnée d'écart au seuil du label, deux tracés en marches sur le même axe des temps : le besoin bioclimatique plat et collé au seuil, la consommation qui décroche marche après marche ; deux cotes verticales dans le rapport exact que la fiche énonce, 1,58 point contre 23,01, maisons Tourtet à Saint-Georges-de-Didonne) | ✅ `scripts/planches/chronologie-affaire.py` (dispatch sur le bloc de l'extraction) |
| `planche-chiffree` | 0 | à écrire — c'est le repli, il servira |

⚠️ **L'archétype se choisit sur la thèse de la fiche, jamais sur son secteur ni sur sa liste
de missions.** Neuf fiches sur vingt-deux portent la même quadruple mission
(Thermique · CVC · CFO · CFA) : s'y fier produirait neuf planches identiques. Ce qui les
sépare est ce que chacune démontre.

---

## Prompt de lancement d'une session neuve

À coller tel quel, en remplaçant `<slug>` et en actualisant la ligne des archétypes déjà
employés depuis le registre ci-dessus. Le protocole étant versionné dans un dépôt public,
le prompt n'a plus à le recopier — **et c'est ce qui garantit qu'une session travaille
toujours sur sa dernière révision**, ce qu'un prompt recopié ne peut pas promettre.

```text
Tu produis une planche de schéma de principe pour une fiche de références FT2E.

AVANT TOUTE AUTRE CHOSE, cloner le dépôt et lire le protocole (révision 5). Il fait
autorité sur tout ce qui suit, y compris sur ce message :

    git clone --depth 1 https://github.com/JeffCrn/ft2e-v3
    docs/superpowers/specs/2026-08-12-planches-references-protocole.md

LA PLANCHE EST UN DESSIN. Elle schématise la solution apportée par FT2E — un mécanisme
dont la géométrie porte la démonstration. Elle ne répète AUCUNE donnée que la fiche
porte déjà : pas de colonne de relevé, pas de classements, pas de listes.

Fiche à traiter :  <slug>
    src/content/projets/<slug>.md   — frontmatter ET corps, jamais un résumé

Archétypes déjà employés, à ne pas répéter sans raison explicite :
    <la ligne se régénère depuis le registre des archétypes ci-dessus, un
     mécanisme par fiche, à chaque session>

Exemple achevé, à consulter comme référence de niveau attendu :
    public/images/projets/abbaye-sablonceaux-ssi/planche.json
    scripts/planches/zonage-ssi.py

CE QUE TU REMETS — un dossier <slug>/ contenant les cinq fichiers du protocole,
puis le prompt de lancement de la session suivante (une fiche = une session).

  · Si l'archétype retenu a déjà son compositeur dans scripts/planches/, tu ne produis
    QUE planche.json, puis tu lances :
        python scripts/planches/<archetype>.py <dossier>
    qui écrit planche.svg, vignette.svg et appui.svg. N'écris pas de SVG à la main dans ce cas.

  · Sinon, tu écris aussi les trois SVG selon les gabarits du protocole (1200 × 800,
    300 × 200 et 552 × 368), et tu me dis explicitement qu'un compositeur reste à écrire.

  · Le PNG 2400 × 1600 dans les deux cas.

  · Le versement : python scripts/planches/verser.py <slug>, puis npm run build et
    contrôle du RENDU des pages touchées (fiche à 1152 px, largeur téléphone, carte
    de secteur — et le hero de l’accueil si la fiche est en_avant) — un build vert ne prouve pas que la page s'affiche.

  · Le prompt de la session suivante : ce gabarit, avec la première fiche « à faire »
    du programme du suivi et la ligne des archétypes actualisée depuis le registre.

TROIS CHOSES QUE JE REFUSERAI :
  · un tableau de synthèse habillé — masque mentalement le texte du dessin : si la
    géométrie seule ne démontre plus rien, ce n'est pas une planche. La première
    version de la planche 02 a été refusée pour ce motif exact ;
  · une planche que tu n'as pas regardée À SA TAILLE DE LECTURE — 1152 px pour la
    planche, une carte de 296 px pour la vignette, 552 px pour l’appui. Le rendu en pleine page ne prouve
    rien : les sept défauts de la première planche y étaient tous invisibles ;
  · une extraction dont `a_valider_ft2e` est vide. Un dessin tranche toujours ce qu'un
    texte laisse ouvert ; une liste vide signifie que tu ne l'as pas vu, pas qu'il n'y
    avait rien à trancher.

Réponds par les fichiers, puis en prose brève : l'archétype retenu et son motif, les
arbitrages laissés à FT2E, ce que tu as dû exclure, et ce que le contrôle à la taille de
lecture t'a fait corriger. Termine par le prompt de la session suivante. Ne me raconte
pas ta méthode.
```

**Le versement fait partie de la session depuis le 2026-08-13.** Une fois les quatre
fichiers en place, `python scripts/planches/verser.py <slug>` contrôle le dossier et
l'extraction (cinq fichiers, `a_valider_ft2e` non vide, forme de repli mobile, racine
SVG conforme) puis bascule le frontmatter — et le repli mobile est rendu **par la forme**
de l'extraction : tout bloc d'archétype qui expose un tableau `elements` ordonné
(règle 7 du protocole) est servi par `PlancheReference.astro` sans une ligne de code
nouvelle ; une extraction sans aucune forme de repli fait échouer le build. Il ne reste
à la session que `npm run build` et le contrôle du rendu (règle 11), le commit de fin de
session emportant le tout — le push déclenche le déploiement Vercel.

---

## Ce que fait une session

1. **Lire la fiche entière** — frontmatter et corps. Jamais un résumé, jamais la page rendue.
2. **Produire `planche.json`** selon le protocole : archétype et son motif, valeurs
   littérales, `a_valider_ft2e` non vide, `exclusions_appliquees`.
3. **Composer** — `python scripts/planches/<archetype>.py public/images/projets/<slug>`
   si le module existe ; sinon écrire le SVG et porter ensuite sa géométrie dans un module.
4. **Regarder à la taille réelle** : la planche à **1152 px**, la vignette **dans une carte
   de 296 px**. Pas isolées, pas en pleine page.
5. **Rendre le PNG** 2400 × 1600.
6. **Verser** : `python scripts/planches/verser.py <slug>` — contrôle les quatre
   fichiers et l'extraction, puis bascule le frontmatter (`image_principale` →
   `planche:`).
7. **Contrôler** : `npm run typecheck`, `npm run build`, `npm run preview` + capture de la
   fiche, de la carte de secteur et du téléphone.
8. **Consigner** ici : numéro, archétype, arbitrages ouverts.
9. **Produire le prompt de lancement de la session suivante** depuis le gabarit
   ci-dessus — première fiche « à faire » du programme, registre des archétypes
   actualisé. **Une fiche = une session** : une session qui rend ses fichiers sans le
   prompt suivant laisse le chantier sans relève.

---

## Ce que la vedette de l'accueil a ajouté — 2026-08-14 : l'appui

Le hero de l'accueil illustre la fiche `en_avant` la plus récente par son
`image_principale` ; le versement de la planche 07 (crèche de l'Oranger, seule fiche
`en_avant`) a supprimé ce champ et le hero est retombé sur sa hachure de repli. Ni la
planche (échelle 0,48 dans la colonne de ~552 px : mono rendu à 4,8 px) ni la vignette
agrandie (1,84 : filets de 1 px épaissis) ne se transposaient — même arithmétique que la
vignette-jamais-recadrée, appliquée dans l'autre sens.

Réponse, portée au protocole en **révision 5** : un **cinquième fichier `appui.svg`**
(552 × 368, échelle de rendu 1,0), troisième composition tirée de la même extraction —
motif entier, deux ou trois nœuds chiffrés, surtitre court, sans phrase ni cartouche.
Le tronc (`racine_appui`, `controles_appui`) et les **cinq compositeurs** le produisent
(huit appuis composés, contrôlés à 552 px, trois défauts de collision corrigés à cette
taille) ; `verser.py` exige les cinq fichiers ; `index.astro` inline l'appui en
`plan-pose`, sans duotone ni équerres. **Sous 640 px, le hero n'affiche plus aucun
média de vedette** (décision FT2E du 2026-08-14) : l'appui ne s'y lit pas (échelle
0,62) et la hachure de repli était un décor `aria-hidden` qui coûtait un écran de
défilement — et la carte-lien, seule sous le titre, se lisait comme un bloc
orphelin — la vedette s'efface donc entièrement du téléphone, où « Nos références »
la dessert ; une photographie, elle, resterait affichée avec sa carte. Les huit planches publiées ont été régénérées — planches et vignettes
contrôlées octet à octet inchangées.

---

## Ce que la première planche a appris

Sept défauts, tous trouvés **au rendu à la taille de lecture** et aucun au rendu en pleine
page. Ils sont consignés au protocole ; en voici la leçon commune.

| Défaut | Ce qu'il enseigne |
|---|---|
| Gabarit 1500 → **1200 × 800** | un gabarit se choisit à la largeur où il sera lu, pas dans l'absolu |
| `font-family="Archivo"` au lieu de `"Archivo Variable"` | le contrôle réussit et le résultat est faux : divergence silencieuse |
| `var()` non résolu par le moteur de rendu | d'où la double écriture des couleurs, classe + attribut |
| U+202F à **3,93 px** contre 7,85 pour U+00A0 | une règle typographique juste peut être illisible à une taille donnée |
| Unités capitalisées (`1 657 M²`, `10,6 KW`) | aucune capitalisation automatique ne connaît la liste des unités |
| `.mono-label` et `@layer base` recapitalisent | la même faute commise deux fois, par deux couches différentes |
| Vignette par recadrage — **3 essais, tous mauvais** | un dessin de 1200 lu à 290 tombe à 0,24 où qu'on le coupe |

## Ce que la dix-neuvième planche a appris — 2026-08-15 : l'origine d'une ordonnée

La planche des maisons Tourtet est la première à porter une **ordonnée** — un écart
réglementaire en points de pourcentage — et non un simple rang topologique. Sa première
version graduait cet axe **depuis l'exigence RT2012** (0 en haut, 45 points en bas), ce qui
était la lecture la plus littérale de la fiche. Au contrôle à 1152 px, deux défauts liés :

- les vingt points qui séparent l'exigence du seuil du label **ne sont occupés par aucun des
  deux tracés** — 44 % de la hauteur du cadre en aplat vide, la « zone vide » que le
  protocole proscrit ;
- écrasée dans les 56 % restants, la cote de **1,58 point** tombait à onze pixels : la moitié
  de la démonstration devenait invisible, alors que c'est précisément elle qui dit que
  l'enveloppe *frôle* le seuil.

Correction : **l'origine de l'ordonnée est le seuil, pas l'exigence.** L'axe n'est pas
tronqué pour autant — le seuil est nommé, coté, et le demi-plan qui le surplombe est dessiné
en bande d'un module, comme la marge d'une ligne de limite sur un dessin coté. La cote passe
à 18,8 px, la dernière marche de 33 à 58 px, et le rapport des deux cotes (14,58) reste celui
que la fiche énonce (14,56).

**La leçon : sur une planche qui porte une grandeur, l'origine de l'échelle est un choix de
composition, pas une donnée.** Elle se choisit à la question que le dessin pose — ici « de
combien dépasse-t-on le seuil ? », pas « où en est-on de l'exigence ? » — et elle se contrôle
à la taille de lecture, où seule apparaît la cote qu'elle écrase.

## Ce que la vingtième planche a appris — 2026-08-15 : l'étiquette qui interrompt sa ligne

La planche de la passerelle de Marans est la première dont le dessin est un **réseau de
routes** plutôt qu'une pile de registres : cinq départs quittent une barre et vont chercher
ce qu'ils desservent. Trois enseignements, tous relevés au rendu à 1152 px.

- **Une étiquette posée sur un trait doit porter son propre fond.** Les tags de frontière
  nomment des descentes ; posés à côté d'elles, ils étaient partout au mauvais endroit, et
  posés dessus, ils étaient rayés. La recette `_etiquette` — un rectangle papier à la mesure
  du texte, puis le texte — est le procédé du dessin coté : le libellé *interrompt* la ligne
  qu'il annote. **Et l'ordre de tracé en fait partie** : appelée avant les descentes, elle
  était repeinte par elles ; le défaut ne se voit qu'à la taille de lecture.
- **Une route qui repart d'où elle vient dessine un rectangle, et un rectangle se lit comme
  une boîte.** Le départ de l'éclairage mobile descend sous le tablier, franchit le joint et
  remonte : avec la barre au-dessus, le tracé fermait un cadre. Les pointes de flèche le
  rouvrent — un contour orienté n'est plus une enceinte. Sur la vignette, où elles ne se
  lisent plus, le long départ a été **rabattu contre le bord droit** au lieu de traverser.
- **Calcaire sur papier vaut 1,05 de contraste : une bande non bordée n'existe pas.** Le
  tablier — le sujet même de la fiche — était invisible dans la carte de 274 px. Les deux
  parties reçoivent désormais un filet ; c'est le **remplissage** qui distingue la fixe de
  la mobile, pas la seule présence de la bande.

Corollaire sur la vignette : sa première version gardait la nomenclature entière — coffret,
boîte 48 V, blocs de prises et de motorisation. Dans 274 px, **quatre rectangles calcaire
muets occupaient 40 % du dessin**. Ce qui reste est ce qui démontre : la barre et son
éventail, le tablier coupé, et les deux cotes qui se rejoignent au joint. Une vignette ne se
dégraisse pas par économie, elle se dégraisse parce qu'un libellé illisible est du bruit.

## Ce que la deuxième planche a arrêté — 2026-08-13

**La planche schématise la solution, elle ne récapitule pas la fiche.** La première
version de la planche 02 alignait des blocs étiquetés (classements ERP, détails de
détection) et une colonne de relevé chiffré : un tableau de synthèse habillé, pas un
schéma. FT2E l'a refusée en posant le principe : le composant installe une dimension
**visuelle et synthétique** de l'affaire — pas une photo, pas une pièce de dossier,
et pas davantage une répétition des données que la page porte déjà dix lignes plus bas.

Conséquences, appliquées à la planche 02 et opposables aux suivantes :

- **Le dessin suit un mécanisme.** Pour `zonage-ssi` : un même déclenchement traverse
  les deux systèmes — avant, le SDI à zone unique diffuse l'alarme partout ; après, la
  centrale adressable ne la diffuse que dans la zone concernée. La démonstration est
  portée par la géométrie (une barre d'alarme sur tout le site contre une barre sur un
  seul bloc), le signe étant toujours doublé d'une flèche encrée et d'une mention.
- **Le relevé chiffré ne monte plus sur la planche.** Le champ `releve` du JSON peut
  être vide ; `PlancheReference.astro` ne rend la section du repli mobile que s'il est
  peuplé. Les classements ERP, essais et durées restent au texte de la fiche.
- **Répercuté le 2026-08-13** : le protocole est porté en **révision 4** (principe en
  tête, gabarit pleine largeur, groupe « Dessin » au contrôle, prompt de session
  suivante obligatoire — une fiche = une session) et la **planche 01 est réalignée** :
  colonne de relevé retirée, Sankey étendu à la largeur utile (flux de 366 à 906 px),
  extraction amendée. Les deux planches publiées appliquent le principe.

---

**Le fil commun : mesurer plutôt qu'estimer.** L'estimation des chasses posait l'unité du
relevé 22 px trop loin ; le `getBBox()` du navigateur a donné 0,596 em pour le chiffre
d'Archivo 700, et le décalage a disparu. Toute cote de ce chantier se relève, elle ne se
suppose pas.

---

## Points ouverts

- **`01.jpg` de l'École des douanes** reste sur disque, plus référencé nulle part. À
  supprimer à la fin du chantier, avec les 21 autres — décision client.
- **Le champ `performance`** compose ses milliers en fine insécable sur les 23 fiches :
  « 152 947 W » se lit « 152947 W » dans le relevé encré, à 28 px. Même mesure que pour les
  planches, même correction — U+00A0 au-delà de 22 px. Passe mécanique, à faire d'un bloc.
- **Le repli de lecture sous 1024 px** est acquis par la **forme** de l'extraction
  depuis le 2026-08-13 : tout bloc d'archétype à tableau `elements` ordonné est rendu
  par le bloc générique de `PlancheReference.astro` (`coupe-traversee` et
  `boucle-fluide` l'utilisent) ; `sankey-energie` et `zonage-ssi`, antérieurs à cette
  forme, gardent leur rendeur propre. Une extraction sans aucune forme de repli fait
  **échouer le build** — la fiche ne peut plus perdre son dessin sur téléphone en
  silence.
- **Un module de composition reste à écrire** (`planche-chiffree`, le repli) —
  `chronologie-affaire` a été écrit en S25 et reçu son second mécanisme en S26. Le **tronc commun** vit dans
  `scripts/planches/_tronc.py` depuis le 2026-08-13 : jetons, gabarits, avances
  calibrées, insécables, primitives à double écriture des couleurs, routine
  d'exécution. L'extraction a été contrôlée par **régénération octet à octet** des
  quatre planches publiées. Un nouveau module importe le tronc et n'écrit que la
  géométrie de son archétype.
- **Le `grep -c` de Git Bash sous Windows ne sait pas chercher U+202F** (`grep -c $' '`
  rend 0 sur un fichier qui en porte 9) : le contrôle des insécables du protocole se rejoue
  en Python (`collections.Counter`) sur cette machine, pas en grep.
- **cairosvg 2.9 (machine de production) rend BLANC tout SVG dont la racine porte
  `style="width:100%;height:auto;display:block"`** — y compris les planches déjà
  publiées, ce qui fait croire à un fichier cassé. Le fichier de livraison garde
  l'attribut (le site en a besoin) ; la copie de contrôle le retire, comme elle
  retire le bloc `<style>` (reconstaté en S24 sur la planche du Fougerou et sur le
  témoin de Sablonceaux).
- **Chrome sous Windows refuse une fenêtre sous 500 px** : une capture headless à
  `--window-size=390` met la page en page à 500 px puis recadre l'image à 390 — toutes
  les lignes paraissent coupées au bord droit, et une page saine passe pour cassée
  (constaté en S23 sur trois pages témoins, `innerWidth = 500` mesuré). Le contrôle
  « largeur téléphone » se fait par une **iframe de 390 px** dans une fenêtre de 500,
  jamais par la taille de fenêtre.
