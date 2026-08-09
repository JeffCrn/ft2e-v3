# Questions ouvertes au 2026-08-09 — sortie de la session « dette rédactionnelle »

Consolidé à l'issue de la session hors-programme précédant la S19. Deux
destinataires distincts, à ne pas mélanger dans un même envoi : ce que **FT2E**
seul peut trancher, et ce qui relève d'une **décision éditoriale interne**.

---

## A. À poser à FT2E

### A1 — Les cinq noms d'`ouvrage` composés

Cinq fiches portent un nom d'ouvrage **rédigé faute de nom propre au dossier**.
Il s'affiche en légende de média et sert d'intitulé court. FT2E confirme-t-elle
ces formulations, ou l'opération porte-t-elle en interne un nom que nous ignorons ?

| Fiche | `ouvrage` proposé |
|---|---|
| `centre-formation-ormeau-du-pied-saintes` | Centre de formation CCI |
| `etude-notariale-boulevard-joffre` | Étude notariale Joffre |
| `habitat-inclusif-salignac-sur-charente` | Habitat inclusif ADMR |
| `maison-relais-saint-jean-d-angely` | Maison relais Pasteur |
| `residence-intergenerationnelle-saint-agnant` | Résidence intergénérationnelle |

⚠️ Ne pas soumettre à FT2E une liste établie par test automatique : un simple
test d'inclusion dans le titre se trompe dans les deux sens. Il classe
« Ateliers Capsulae », « Crèche de l'Oranger », « Pas des Bœufs » et « Maisons
Tourtet » comme composés alors qu'ils dérivent d'un nom propre présent au
dossier ; et il classe « Résidence intergénérationnelle » comme propre alors
que c'est le plus descriptif des dix-neuf. La liste ci-dessus est relevée à la
main.

### A2 — La réception de la crèche de l'Oranger

`creche-oranger-perigny` porte `statut: livré` **sans `annee_livraison`**. Le
schéma l'autorise, mais la fiche annonce une affaire livrée sans dire quand.
Deux issues, aucune décidable depuis le dépôt — il faut la pièce :

- **soit** la réception est prononcée et datable → renseigner `annee_livraison` ;
- **soit** elle ne l'est pas → le statut repasse à `en cours`.

Relevé dans `adr/ADR-003` § « Cas particulier », resté ouvert.

### A3 — Le volume d'opérations, hors tertiaire

`expertises/cvc.md` avançait « plus de 150 opérations depuis 2008 », sans
source. Le chiffre a été remplacé par celui de la plaquette 2024, qui est
sourcé mais **ne couvre que le tertiaire** : « 98 opérations tertiaires pour
les seules années 2019 à 2024 ». Si FT2E dispose d'un décompte toutes
typologies confondues depuis 2008, il rendrait la phrase à la fois plus juste
et plus parlante.

---

## B. Décision éditoriale interne — ne concerne pas FT2E

### B1 — ⚠ Le seuil de la convention numérale

Le relevé de `.claude/rules/french-editorial.md` a été recompté et outillé
(`scripts/releve-numeral.py`). Il confirme qu'il n'y avait **qu'un**
écart sous dix, désormais corrigé — et il en découvre un autre, bien plus large :

| Bande | En lettres | En chiffres |
|---|---|---|
| de deux à neuf | 65 — conforme | 1 — citation du contrat Yachtman |
| **de dix à trente** | **27** | **13** |
| au-delà de trente | 0 | 12 — conforme |

La règle prescrit les chiffres **dès dix**. Entre dix et trente, le corpus fait
l'inverse deux fois sur trois (« treize logements », « seize lots », « trente
places »), et au-delà de trente il ne s'écrit jamais qu'en chiffres. Deux
issues :

- **monter le seuil** — les nombres qui s'écrivent en un mot restent en lettres
  jusqu'à trente, les composés passent en chiffres. C'est déjà l'usage
  dominant : la règle rejoint le corpus, rien à réécrire ;
- **tenir le seuil** — 27 occurrences à réécrire dans neuf récits.

Ne rien décider laisse en place une règle que le corpus désobéit dans sa
majorité — c'est ainsi qu'une règle cesse d'être lue.

**Ce qui rend l'arbitrage urgent** : trois fiches portent les deux graphies du
même nombre, dans le même fichier — `fougerou` (« 27 calculs » en `synthese`,
« vingt-sept » au récit), `exe-residence-horizon-mediatim` (« 15 diffusions » /
« quinze envois »), `hotel-yachtman-quai-valin-la-rochelle` (« 46 chambres » /
« quarante-six chambres »). La synthèse surmontant le récit sur la fiche, la
contradiction se lit **d'un seul écran**. Les corriger avant l'arbitrage, ce
serait les corriger deux fois.

⚠️ **Rejouer le relevé avant de trancher, pas avant de l'avoir relu.** La
première version du script arrêtait son lexique à « trente » et annonçait
« au-delà de trente, jamais de lettres » — un zéro qui n'était que la forme du
dictionnaire. Le lexique est désormais **engendré** (2 à 100, composés compris)
et la bande haute compte trois occurrences en lettres, pas zéro.

### B2 — La fine insécable devant un nom commun

Six occurrences séparent le nombre du nom par une **fine insécable** (U+202F) :
« 13 logements », « 21 logements » (×4), « 19 lots », dans
`logements-maubec-chagnolet`, `maison-relais-saint-jean-d-angely` et
`residence-intergenerationnelle-saint-agnant`. Sept occurrences comparables
(« 12 chambres », « 11 zones », « 13 lots »…) emploient l'espace ordinaire.
La fine est réservée au couple **nombre + unité** (`230 m²`, `7 °C`) ; devant un
nom commun, elle n'a pas lieu d'être. Uniformisation à faire, sans urgence.

### B3 — ⚠ Trois récits datent encore l'ouverture d'affaire en clair

ADR-003 retire le millésime d'ouverture de l'affichage parce qu'il **vieillit
artificiellement la référence** : « affaire 2022 » sur un ouvrage réceptionné en
2024. Or trois récits le réintroduisent en prose, ce que la session du
2026-08-09 n'a pas traité — son périmètre était le **numéro**, pas le millésime :

- `logements-maubec-chagnolet` — « l'écart entre l'ouverture de l'affaire en 2022
  et les opérations préalables à la réception de l'automne 2025 » ;
- `habitat-inclusif-salignac-sur-charente` — « l'affaire est ouverte en novembre 2023 » ;
- `centre-formation-ormeau-du-pied-saintes` — formulation analogue, en mars 2025.

À trancher **globalement**, pas fiche par fiche : soit la prose peut dire quand
le bureau a été saisi (ce qui est une information de mission, non un identifiant
de gestion), soit l'ADR vaut aussi pour le récit et les trois se réécrivent.

### B4 — Deux formulations qui se lisent comme une contradiction

`secteurs/coordination-ssi.md` annonce « plus de vingt ans de pratique » en
accroche (sourcé sur la formation de coordinateur SSI de 2003, antérieure au
bureau) et « sans interruption depuis la création du bureau en 2008 » trois
paragraphes plus bas. Les deux affirmations sont vraies ; posées à cette
distance, elles se lisent comme 18 ans contre plus de vingt. Une seule des deux
suffit.

### B5 — Deux détails relevés en relecture

- `abbaye-sablonceaux-ssi` : le chapô écrit « 58 255 € HT », le § solution
  « 58 255,70 € HT ». Troncature voulue, ou coquille ?
- `secteurs/tertiaire-erp` renvoie vers l'EHPAD de Coulonges, dont le champ
  `secteur` est « Coordination SSI » : le lecteur quitte la page Tertiaire / ERP
  pour une fiche classée ailleurs. Acceptable — un ouvrage relève de plusieurs
  angles — mais à confirmer comme un choix.

### B6 — Le masquage `hidden lg:inline-flex` de la légende de média

Inchangé, décision en attente, adossée à une mesure : 32 signes de budget pour
une ligne, 45 de longueur médiane après l'introduction du champ `ouvrage`.

---

## C. Sans question — pour mémoire

- **Les 8 marqueurs `[DÉMO]` restants** sont tous des `image_alt` (7 fiches
  secteur, 1 actualité). Ils marquent des visuels de démonstration générés par
  IA : ils se lèvent au **reportage photographique**, pas par une validation
  FT2E. Aucune question à poser.
  ⚠️ Deux nuances relevées au contrôle du HTML livré, à garder en tête sans en
  faire un chantier : (i) **deux seulement de ces huit alt atteignent une page**
  (`secteurs/logements`, `secteurs/tertiaire-erp`) — les six autres visuels
  n'existent pas encore dans `public/`, et le composant bascule sur son
  placeholder ; (ii) le marqueur ne vit que dans l'`alt`, donc **seul un
  lecteur d'écran l'entend**, quand la règle 1 de `CLAUDE.md` demande le tag
  Markdown *et* un badge visuel. À traiter avec le reportage photo, qui rendra
  la question sans objet.
- **Les 10 marqueurs en prose sont levés** : chacun a été remplacé par un
  exemple relevé sur une des dix-neuf fiches réelles. Aucun n'a été retiré
  « parce que ça semblait raisonnable ».
