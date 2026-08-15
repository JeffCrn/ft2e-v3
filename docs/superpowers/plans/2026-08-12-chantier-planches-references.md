# Chantier des planches de références — programme et suivi

> **Objet.** Substituer, sur les 23 fiches de références, un dessin FT2E aux visuels
> actuels. **Ouvert le 2026-08-12, CLOS le 2026-08-15 — 23 planches publiées sur 23.**
> Le programme est épuisé ; ce document devient le bilan du chantier et le registre
> de ce qu'il laisse ouvert (§ Bilan de clôture, § Points ouverts).
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

## État — 23 / 23 · programme épuisé

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
| 21 | `place-des-chenes-verts-saint-rogatien` | Industriel et commercial | `tableau-electrique` (mécanisme `essaimage`) | ✅ **publiée** (versée le 2026-08-15) |
| 22 | `residence-intergenerationnelle-saint-agnant` | Logements | `sankey-energie` (mécanisme `bascule`) | ✅ **publiée** (versée le 2026-08-15) |
| 23 | `siege-rese-aigrefeuille` | Tertiaire / ERP | `boucle-fluide` (mécanisme `commande`) | ✅ **publiée** (versée le 2026-08-15) |

**Registre des archétypes employés** — à tenir à jour, il conditionne la variété de la série :

| Archétype | Employé | Module |
|---|---|---|
| `sankey-energie` | 4 — quatre mécanismes : le flux à largeur proportionnelle (École des douanes), `plafonds` (la proportion sans flux — trois pistes à échelle commune, le plafond carbone qui tombe au tiers à la frontière réglementaire et commande le générateur, logements Maubec à Chagnolet), `dedoublement` (la partition contractuelle — un permis contigu qui fourche en deux marchés à 3 px par logement, une bande calcaire unique qui traverse les deux flux, le BET fluides commun ; les arrivées en segments comptent les bâtiments, logements Néréa à Aytré) et `bascule` (la grandeur qui change de signe — une opération partagée en deux zones de calcul à largeur proportionnelle à leur surface, une production qui n'entre que dans la seconde, un dixième du bâtiment ; trois lignes pleine largeur, plafond, zéro et bilan, mais deux HAUTEURS confinées à la colonne de cette zone : la bande autorisée de 73,9 px contre une colonne de 182,1 px, subdivisée par des traits au pas du plafond pour que la profondeur se COMPTE — deux bandes et demie sous le zéro, résidence intergénérationnelle de Saint-Agnant) | ✅ `scripts/planches/sankey-energie.py` (dispatch sur le bloc de l'extraction) |
| `zonage-ssi` | 3 — trois mécanismes : `zonage` (un même déclenchement, l'alarme avant/après — Abbaye de Sablonceaux), `transfert` (la mise à l'abri au même niveau, la descente barrée — EHPAD de Coulonges-sur-l'Autize) et `partage` (le découpage réglementaire d'une enveloppe montée d'un seul tenant — la limite sans mur qui commande l'étanchéité, les machines et l'incendie, habitat inclusif de Salignac-sur-Charente) | ✅ `scripts/planches/zonage-ssi.py` (dispatch sur le bloc de l'extraction) |
| `boucle-fluide` | **7 — sept mécanismes** : `boucle` (récupération, Atelier Dufour), `utilites` (réseau de livraison, Ateliers Capsulae), `substitution` (production réversible, centre de formation de Saintes), `declinaison` (le parti répété — une maison dessinée une fois, 54 cellules identiques en `<defs>`/`<use>`, Le Fougerou), `appariement` (la partition des services — trois bandes de service, deux colonnes de machines, et dans chaque colonne UNE boîte qui enjambe une frontière de bande, jamais la même : l'eau chaude porte la ventilation chez les T2, le chauffage porte l'eau chaude chez les T3 ; contour d'encre dominant la frontière filet-1, logements du Pas des Bœufs au Bois-Plage) et `individualisation` (le collectif produit, chaque logement compte — deux flux collectifs entrent dans une colonne qui dessert une pile de 21 modules identiques en trois groupes typologiques ; UN module tiré au détail par deux filets d'agrandissement montre deux arrivées, trois départs, trois compteurs, maison relais de Saint-Jean-d'Angély) et `commande` (les six premiers disent OÙ va le fluide, celui-ci dit QUI décide qu'il parte — trois circuits d'air indépendants dans une même enveloppe, dont le point de décision REMONTE vers l'occupant : posé sur la machine pour une extraction permanente, dans le réseau pour une régulation à pression constante, dans le local pour une sonde de CO2. Trois lignes de commande de 0, 250 et 532 px, et une seconde grandeur dans la même colonne (x 850–1116) : la bande de chaleur qui part, pleine à 22 px sur deux circuits, effondrée à 2,2 px sur celui qui la rend — siège du Fief Girard à Aigrefeuille-d'Aunis) | ✅ `scripts/planches/boucle-fluide.py` (dispatch sur le bloc de l'extraction) |
| `coupe-traversee` | 4 — quatre mécanismes : `coupe` (l'enveloppe traversée, Marennes), `equilibre` (l'air extrait, l'air compensé — restaurant scolaire de Villedoux), `enjambement` (l'enveloppe qui ferme les faces qu'un bâtiment ordinaire n'a pas — dessous du plancher sur le passage, fosse d'ascenseur, abouts pontés — étude notariale Joffre) et `portee` (deux périmètres inégaux sur une même coupe de niveaux — la mission bornée au coin bas-gauche, l'enceinte de la zone d'alarme qui enclot tout, hôtel Le Yachtman) | ✅ `scripts/planches/coupe-traversee.py` (dispatch sur le bloc de l'extraction) |
| `tableau-electrique` | 3 — trois mécanismes : `autoconsommation` (la toiture est la seconde arrivée du tableau, crèche de l'Oranger) et `franchissement` (le sujet n'est plus la distribution mais ce que les départs TRAVERSENT — une arrivée, une barre, cinq départs, et trois frontières : la tension, où deux départs d'éclairage changent de poids de trait en sortant des blocs 48 V ; le joint mobile, où deux cotes se rejoignent en sens contraire, 10 m de câble d'un côté contre 6,80 m de course de l'autre, à la même échelle ; la limite du réseau public, où une descente barrée d'une croix vers un mât jamais construit répond à un mât dédié plus court, alimenté depuis la barre par le plus long des départs — passerelle du Carreau d'Or à Marans) et `essaimage` (le tableau qui n'existe pas — le motif est renversé : au lieu d'une arrivée qui se ramifie, cinq comptages descendent séparément du réseau public dans cinq cellules qu'aucune liaison ne relie, et le seul ouvrage commun est la maçonnerie qui les contient. La démonstration se COMPTE — cinq franchissements de la ligne du réseau, zéro des quatre refends — et se rompt à deux endroits distincts : un tronc triple en cellule 3, deux postes de plus en cellule 1 ; les libellés de poste sont nommés une fois, en gouttière, place des Chênes Verts à Saint-Rogatien) | ✅ `scripts/planches/tableau-electrique.py` (dispatch sur le bloc de l'extraction) |
| `chronologie-affaire` | 2 — deux mécanismes : `precedence` (le dessin précède le gros œuvre : l'escalier des réservations gravit les niveaux d'avance sur l'exécution, résidence Horizon) et `divergence` (l'écart qui se creuse — une ordonnée d'écart au seuil du label, deux tracés en marches sur le même axe des temps : le besoin bioclimatique plat et collé au seuil, la consommation qui décroche marche après marche ; deux cotes verticales dans le rapport exact que la fiche énonce, 1,58 point contre 23,01, maisons Tourtet à Saint-Georges-de-Didonne) | ✅ `scripts/planches/chronologie-affaire.py` (dispatch sur le bloc de l'extraction) |
| `planche-chiffree` | **0 — jamais employé, et le chantier s'achève sans lui** | non écrit. La règle 5 le réservait aux fiches sans trois organes identifiables ; aucune des vingt-trois n'était dans ce cas. Et la **révision 4 l'a rendu presque inutilisable** : elle interdit de remonter à la planche les chiffres que la fiche porte déjà, or un repli typographique ne dessine rien d'autre. Son maintien au protocole est une décision à prendre, pas un reste (§ Points ouverts) |

⚠️ **L'archétype se choisit sur la thèse de la fiche, jamais sur son secteur ni sur sa liste
de missions.** Neuf fiches sur vingt-deux portent la même quadruple mission
(Thermique · CVC · CFO · CFA) : s'y fier produirait neuf planches identiques. Ce qui les
sépare est ce que chacune démontre.

---

## Bilan de clôture — 2026-08-15

*Cette section remplace le « prompt de lancement d'une session neuve », qui n'a plus de
fiche à porter. Le gabarit du prompt reste consultable dans l'historique du dépôt
(`git log -p` sur ce fichier, révisions antérieures au 2026-08-15) : il resservira si une
vingt-quatrième fiche entre au catalogue.*

**Ce qui est fait.** Les vingt-trois fiches de `src/content/projets/` portent un champ
`planche` et cinq fichiers dans `public/images/projets/<slug>/`. Aucune ne porte plus
`image_principale`. Les vingt et un visuels litigieux — neuf perspectives d'architecte ou
vues de drone sans crédit, douze extraits reproduisant un fond de plan — ne sont plus
référencés nulle part dans `src/`.

**Ce que le chantier a produit, en pièces**

| | |
|---|---|
| Planches publiées | 23 — 115 fichiers (`planche.json`, `planche.svg`, `vignette.svg`, `appui.svg`, `planche.png`) |
| Compositeurs | 6 modules sur 7 archétypes, ~10 000 lignes, tronc commun `_tronc.py` |
| Mécanismes distincts | **23 — un par fiche, aucun réemployé** |
| Révisions du protocole | 5 (rév. 4 : « la planche est un dessin » ; rév. 5 : l'appui du hero) |

**Ce que le chantier a établi, et qui vaut au-delà de lui.** Chaque leçon est née d'un
défaut invisible en pleine page et trouvé à la taille de lecture — c'est le fil, et il
n'a pas varié en vingt-trois planches.

| Planche | Ce qu'elle a établi |
|---|---|
| 01 | un gabarit se choisit à la largeur où il sera lu (1500 → 1200 × 800) |
| 02 | **la planche schématise la solution, elle ne récapitule pas la fiche** — le principe qui gouverne tout le reste |
| 19 | sur une planche qui porte une grandeur, l'origine de l'échelle est un choix de composition |
| 20 | une étiquette posée sur un trait porte son propre fond, et l'ordre de tracé en fait partie |
| 21 | une avance calibrée l'est pour une police, pas pour un dessin — le mono ne connaît pas la fine |
| 22 | deux hauteurs ne se comparent que dans la même colonne |
| 23 | **une proportion qu'un format ne peut pas dessiner ne s'y arrondit pas : elle s'y tait** |

**Ce que le registre des archétypes dit de la série.** `boucle-fluide` 7, `sankey-energie`
et `coupe-traversee` 4, `tableau-electrique` et `zonage-ssi` 3, `chronologie-affaire` 2,
`planche-chiffree` 0. La répartition est inégale et ce n'est pas un défaut : **l'archétype
est une famille géométrique, le mécanisme est la planche.** Neuf fiches sur vingt-trois
portent la même quadruple mission ; s'être fié à l'archétype aurait produit neuf dessins
identiques, s'être fié au mécanisme en a produit vingt-trois distincts. Le septième
`boucle-fluide` ne répète aucun des six autres — il est le seul à dessiner l'ordre de
marche plutôt que le trajet.

**Ce que le chantier laisse ouvert** — le détail est au § Points ouverts ci-dessous. Au
premier rang : **la régénération des vingt planches antérieures à la 21**, qui élargira
leur cartouche de 5 à 12 px et demande un contrôle du rendu à 1152 px de chacune. Tant
qu'elle n'est pas faite, l'invariant « régénération octet à octet » du chantier ne tient
plus, et c'est le seul contrôle qui protégeait les planches publiées d'une dérive
silencieuse du tronc.

---

## Le nettoyage de clôture — 2026-08-15

Le chantier laissait derrière lui du code que rien n'appelait plus. Relevé par mesure, pas
par impression, et retiré dans le même mouvement que la clôture.

| Retiré | Volume | Motif |
|---|---|---|
| Les 25 visuels d'origine des fiches (`01.jpg`, `01-recadre.jpg`) | 6,1 Mo | plus référencés nulle part depuis la 23ᵉ planche — ce sont les perspectives d'architecte et les extraits de plan qui ont motivé le chantier |
| `image_principale` / `image_principale_alt` | schéma Zod, Decap, 4 branches de rendu | zéro fiche les portait ; `planche` devient **obligatoire** |
| Le `superRefine` « planche OU visuel » | 14 lignes | une règle qui n'a plus d'alternative à départager ment sur ce qu'elle contrôle |
| Neuf composants sans aucun import | 406 lignes | `AcronymeFT2E`, `BandeauPartenaires`, `CartesExpertises`, `ChiffresCles`, `EquipePreview`, `ReferencesRecentes`, `SchemaTechnique`, `SecteursPhares`, `Capsule` |
| `demo_reason`, `contact_email` | schéma Zod + Decap | renseignés dans zéro fichier de contenu, lus nulle part |
| `@fontsource-variable/inter` | une dépendance | la charte v3 ne charge qu'Archivo et IBM Plex Mono |
| Deux SVG de logo orphelins | 2 Ko | aucun appel dans `src/` |

**Ce qui a été gardé alors qu'il paraissait mort**, et pourquoi :

- **`.bg-profond :focus-visible` et `.polarite-profonde :focus-visible`** (`global.css`) :
  aucun composant n'emploie ces deux classes aujourd'hui. Ce ne sont pas des règles mortes,
  ce sont les **garde-fous de l'amendement A4** — le pivot est invisible sur réserve
  profonde (2,85), et ces sélecteurs garantissent l'anneau clair au premier bloc sombre
  qui apparaîtra. Une règle défensive ne se mesure pas à son taux d'emploi.
- **`associe`, `formation`, `icone`** : renseignés dans 7, 6 et 4 fichiers de contenu,
  affichés nulle part. Ce n'est pas un champ mort, c'est **du contenu sans affichage** —
  la page Équipe pourrait montrer la formation. Décision reportée aux optimisations.
- **`fs.existsSync`** : le motif ne sert plus les fiches projet, mais toujours les
  photographies d'équipe, qui manquent jusqu'au reportage. La règle
  `.claude/rules/astro-conventions.md` a été **réécrite** en conséquence : elle décrivait
  un code qui n'existait plus, ce qui est pire qu'une règle absente.

⚠️ **La suppression des 25 visuels ne les efface pas du dépôt public.** Ils restent dans
l'historique git, donc dans tout clone. Le site publié ne les sert plus — c'était l'objet
du chantier — mais si l'exposition au droit d'auteur doit être effacée du dépôt lui-même,
il faut une réécriture d'historique, qui invalide tous les SHA. Point ouvert, décision FT2E.

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
9. **Produire le prompt de lancement de la session suivante** — *sans objet depuis le
   2026-08-15, le programme étant épuisé.* Le gabarit vit dans l'historique du dépôt et
   resservira si une fiche entre au catalogue. La règle qu'il portait, elle, demeure :
   **une fiche = une session**, et une session qui rend ses fichiers sans consigner son
   mécanisme au registre laisse la série sans mémoire.

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

## Ce que la vingt-et-unième planche a appris — 2026-08-15 : la chasse fixe ne connaît pas la fine

La planche de la place des Chênes Verts est la première dont le cartouche a **débordé de
sa réserve** : le dernier chiffre du millésime tombait hors du rectangle profond. La cause
n'est pas dans le compositeur, elle est dans l'instrument de mesure.

`_tronc.mesurer` comptait les deux insécables aux largeurs relevées **dans Archivo** —
U+202F à 0,098 em, U+00A0 à 0,196 — y compris sur les chaînes destinées au mono. Or *une
police à chasse fixe ne connaît pas la fine* : dans IBM Plex Mono, l'espace fine avance de
0,600 em comme tout autre glyphe. Sur un cartouche de trente signes portant une surface,
l'écart vaut **5,5 px**, absorbés jusqu'ici par les 20 px de marge — sauf quand la légende
est courte, ce qui est le cas dès que la ville est brève et la surface à trois chiffres.

Correction : `mesurer` traite le profil `mono` à part, toutes avances égales. Deux
conséquences, la seconde plus importante que la première :

- les cartouches s'élargissent de 5 à 12 px — **les vingt et une légendes du chantier sont
  concernées**, mesurées ;
- surtout, **tout `controler()` portant sur une ligne mono était permissif** de ce même
  écart. Un dépassement pouvait passer sans être signalé sur n'importe quelle planche.

**La leçon : une avance calibrée l'est pour une police, pas pour un dessin.** Le fil du
chantier — mesurer plutôt qu'estimer — ne protège de rien si l'instrument mesure la
mauvaise police.

⚠️ **Les vingt planches publiées avant celle-ci n'ont pas été régénérées.** Leur
régénération n'est donc plus octet à octet : elle élargira leur cartouche. La passe est à
faire d'un bloc, avec un contrôle du rendu à 1152 px de chacune — c'est un point ouvert
ci-dessous, pas un oubli.

## Ce que la vingt-deuxième planche a appris — 2026-08-15 : deux hauteurs ne se comparent que dans la même colonne

La planche de Saint-Agnant est la première dont la thèse est un **rapport entre deux
hauteurs** : ce que le plafond réglementaire laisse consommer à une zone (90 unités) contre
la profondeur que son bilan atteint de l'autre côté du zéro (221,8). Sa première version
dessinait la bande autorisée **en pleine largeur** — les deux lignes de l'axe la portent, il
semblait naturel de la remplir sur toute la planche — et la colonne du bilan sur les 125 px
de la zone concernée. Au rendu à 1152 px, deux défauts d'un seul tenant :

- **une bande pleine largeur et une colonne étroite ne se rapportent pas l'une à l'autre**.
  L'œil compare des surfaces, pas des hauteurs : 1 088 × 74 contre 125 × 182 se lisent comme
  deux objets sans commune mesure, et le rapport 2,46 — qui *est* la démonstration —
  disparaissait ;
- la bande pleine largeur, remplie de ses deux légendes, se lisait comme **un pavé de
  texte** : exactement le tableau de synthèse habillé que la révision 4 proscrit.

Correction : **les trois LIGNES restent en pleine largeur — plafond, zéro, bilan, ce sont les
repères de l'axe — mais les deux HAUTEURS se confinent à la colonne de la zone.** Deux
rectangles empilés dans les mêmes 125 px, l'un au-dessus du zéro, l'autre au-dessous : le
rapport se lit d'un coup d'œil et se vérifie à la règle. Les légendes, chassées de la bande,
sont allées se poser contre elle, à sa hauteur — ce qui a du même coup rempli le quart
inférieur gauche, resté vide dans la première version.

Corollaire, ajouté au même passage : **une profondeur qui vaut « deux fois et demie » se
compte mieux qu'elle ne s'estime.** La colonne est subdivisée par des traits au pas du
plafond — deux traits, donc deux bandes autorisées pleines et une troisième entamée. Aucun
chiffre n'est fabriqué : le pas de la graduation est le plafond, qui est déjà sur la planche,
et le signe est doublé de sa mention (« la colonne en descend deux et demie sous le zéro »).

**La leçon : sur une planche qui compare deux grandeurs, ce qui doit coïncider n'est pas la
graduation mais la LARGEUR des objets gradués.** Une échelle commune ne suffit pas si les
deux hauteurs ne partagent pas la même colonne — et le défaut ne se voit qu'à la taille de
lecture, où l'on cesse de savoir ce qu'on a dessiné pour ne plus voir que ce qui est là.

## Ce que la vingt-troisième planche a appris — 2026-08-15 : une proportion qu'un format ne peut pas dessiner

La planche du siège du Fief Girard porte deux grandeurs. La première — la longueur des
trois lignes de commande — se transpose partout. La seconde ne se transpose nulle part :
c'est la **part de chaleur qui part** après la machine, un dixième de ce que l'air a
emporté du local, dessinée sur la planche par une bande de 2,2 px contre 22.

Trois enseignements, tous relevés à la taille de lecture.

- **Un filet de 2,2 px posé à 7 px sous un conduit de 1,5 px ne se lit pas comme une
  bande effondrée : il se lit comme un SECOND CONDUIT.** Aucune couleur, aucune épaisseur
  ne l'en distingue — seule la *place* le peut. L'écart est passé à 14 px et les bords
  hauts des trois bandes sont alignés : les circuits 1 et 2 enseignent alors la
  convention (une ligne, puis une bande à cette distance), et le filet du troisième se
  lit à la place qu'occupe la bande ailleurs. **Une convention graphique s'enseigne dans
  le cas plein avant de servir dans le cas vide.**
- **À 274 px et à 552 px, cette proportion vaut 0,73 et 1,6 px : elle n'est pas petite,
  elle est fausse.** Un sous-pixel n'est pas une proportion, c'est un arrondi — et un
  arrondi signé par un bureau d'études est une donnée technique inexacte (règle 1). La
  vignette et l'appui ne la dessinent donc **pas du tout** : ils gardent la chaleur
  emportée du local et celle qui revient, deux bandes franches, et taisent la troisième.
  Le champ `proportion_non_dessinee` de leurs contrôles dit ce qui a été tu et pourquoi.
  **Un format ne rogne pas une proportion, il y renonce** — c'est la règle de la vignette
  jamais recadrée, appliquée à une grandeur au lieu d'un cadrage.
- **Le rendu de contrôle a signalé un débordement de cartouche qui n'existait pas.**
  cairosvg arrondit à l'entier l'avance du mono aux petites échelles : à 0,96, les 291,5 px
  mesurés se rendaient en ~312 et le millésime semblait tomber hors de sa réserve —
  exactement le défaut de la planche 21, mais en trompe-l'œil. Le `getBBox()` du navigateur
  a donné 290,7 px et 22,3 px de marge. **Après la planche 21 qui a appris qu'un instrument
  peut mesurer la mauvaise police, la 23 apprend qu'il peut aussi mesurer sous les mauvaises
  conditions** : le juge des chasses est le navigateur, à la largeur de lecture, et rien
  d'autre.

**La leçon commune aux trois : ce que le dessin ne peut pas porter honnêtement, il ne le
porte pas — et il le consigne.** Un chantier qui a passé vingt-deux planches à mesurer
plutôt qu'estimer finit sur le cas où la mesure commande de ne rien tracer.

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
- **Le repli de lecture sous 880 px** est acquis par la **forme** de l'extraction
  depuis le 2026-08-13 : tout bloc d'archétype à tableau `elements` ordonné est rendu
  par le bloc générique de `PlancheReference.astro` (`coupe-traversee` et
  `boucle-fluide` l'utilisent) ; `sankey-energie` et `zonage-ssi`, antérieurs à cette
  forme, gardent leur rendeur propre. Une extraction sans aucune forme de repli fait
  **échouer le build** — la fiche ne peut plus perdre son dessin sur téléphone en
  silence.

  ⚠ **Le seuil et le rôle du repli ont changé le 2026-08-15** : il ne remplace plus le
  dessin, il le suit. La fiche sert `planche.svg` au-dessus de 880 px, `appui.svg` de 480
  à 879, `vignette.svg` en dessous — et sous 880 le repli vient **sous** le dessin, allégé
  de son surtitre et de son titre. Détail et mesures :
  `docs/superpowers/specs/2026-08-16-responsive-planches-fiches.md`.

  À noter au passage, relevé en ouvrant ce chantier : **`extraction.releve` est vide sur
  les 23 planches** — le bloc `releve` du repli (`releve_entete`, chiffres à 30 px,
  `releve-retrait`) n'est rendu nulle part depuis la décision FT2E du 2026-08-13. Il est
  conservé en l'état, parce que le garde-fou de build l'accepte encore comme forme de
  repli valide : le retirer sans retirer la branche du garde-fou laisserait passer une
  extraction qui ne rendrait rien.
- **`planche-chiffree` n'a jamais servi et son module n'est pas écrit** — décision à
  prendre plutôt qu'un reste à faire. La révision 4 interdit de remonter à la planche les
  chiffres que la fiche porte déjà ; un repli typographique ne dessine rien d'autre. Soit
  le protocole le retire de sa liste fermée, soit il redéfinit ce qu'il devrait montrer.
  Le **tronc commun** vit dans
  `scripts/planches/_tronc.py` depuis le 2026-08-13 : jetons, gabarits, avances
  calibrées, insécables, primitives à double écriture des couleurs, routine
  d'exécution. L'extraction a été contrôlée par **régénération octet à octet** des
  quatre planches publiées. Un nouveau module importe le tronc et n'écrit que la
  géométrie de son archétype.
- **La régénération des vingt planches antérieures n'est plus neutre** (2026-08-15) :
  la correction de `_tronc.mesurer` sur le profil mono élargit les cartouches de 5 à
  12 px — **21 légendes sur 21** sont concernées, écart mesuré fiche par fiche. Les vingt
  planches publiées avant la 21 n'ont pas été régénérées ; la passe est à faire d'un bloc,
  chaque planche recontrôlée à 1152 px, et l'invariant « régénération octet à octet » se
  rétablit à ce moment-là et pas avant.
- **La vignette de `/references` est servie à 54 px** (mesuré au navigateur sur les
  vingt-trois lignes de la nomenclature : colonne de tête de 56 px, échelle 0,18, mono de
  9 px rendu à 1,6). Le dessin y est une texture, pas un schéma — il est `aria-hidden` à
  la source, donc rien n'est perdu pour l'accessibilité, mais c'est la même arithmétique
  qui a condamné l'ancienne miniature au § « Pourquoi ce chantier ». Trois issues :
  élargir la colonne, retirer la vignette de la nomenclature, ou l'assumer comme repère
  de couleur. **Décision FT2E** — elle n'est pas propre à une planche, elle porte sur les
  vingt-trois.
- **`planche-chiffree` : voir ci-dessus.** Le seul archétype du protocole que le chantier
  n'a pas exercé, donc le seul dont rien ne garantit qu'il fonctionne.
- **Le `grep -c` de Git Bash sous Windows ne sait pas chercher U+202F** (`grep -c $' '`
  rend 0 sur un fichier qui en porte 9) : le contrôle des insécables du protocole se rejoue
  en Python (`collections.Counter`) sur cette machine, pas en grep.
- **cairosvg arrondit l'avance du mono aux petites échelles** (relevé en S27) : un rendu de
  contrôle à 1152 gonfle une ligne mono de ~7 % et fait croire à un débordement de cartouche
  qui n'existe pas dans la page. Toute mesure de chasse se tranche au `getBBox()` du
  navigateur, à la largeur de lecture — jamais sur le PNG.
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
