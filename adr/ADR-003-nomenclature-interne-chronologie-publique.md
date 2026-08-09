# ADR-003 — Nomenclature interne, chronologie publique

- **Statut** : accepté
- **Date** : 2026-08-09
- **Décideurs** : FT2E, EuporIA Factory
- **Remplace** : rien. **Complète** : `.claude/rules/content-collections.md` § « Fiches projet — référence et millésimes ».

## Contexte

Les fiches de référence affichaient jusqu'ici deux données issues du système de gestion interne de FT2E :

- le **numéro d'affaire** (`reference`, graphie `NN-NNN`), relevé sur les pièces du bureau ;
- le **millésime d'ouverture de l'affaire** (`annee`), que ce numéro encode.

Elles apparaissaient en six endroits du site : l'eyebrow de la fiche, le cartouche `FicheTechnique`, deux colonnes de la nomenclature `/references`, le pied des vignettes `CarteProjet` (donc au pied de **chaque** fiche projet, via `ProjetsSimilaires`) et le bloc « en avant » de l'accueil.

Retour client du 2026-08-09 : ces deux données ne veulent rien dire pour un lecteur extérieur, et elles en disent trop pour un lecteur averti.

1. **Le numéro d'affaire est une clé de gestion**, pas une information publique. Affiché, il expose le rang de l'affaire dans l'année — donc, par recoupement de plusieurs fiches, une indication sur le volume d'activité du bureau. Ce n'est pas une donnée que FT2E souhaite publier.
2. **Le millésime d'ouverture est trompeur.** « Affaire 2022 » sur un ouvrage réceptionné en 2024 laisse croire à une référence plus ancienne qu'elle ne l'est ; sur une affaire toujours en cours, il laisse croire à un chantier qui s'éternise. Ce que le public veut savoir d'une référence, c'est **quand elle a été livrée**, ou **où elle en est**.

La difficulté : ces deux champs sont par ailleurs **structurants**. `annee` est la clé de tri primaire de la nomenclature, `reference` son critère de départage ; le schéma vérifie au build que les deux concordent. Les retirer de la donnée casserait le tri, la validation et la traçabilité.

## Décision

**Séparer la nomenclature interne de la chronologie publique.** Les champs restent ; leur rendu disparaît.

### Ce qui est retiré de l'affichage

| Emplacement | Avant | Après |
|---|---|---|
| Eyebrow de fiche — `references/[...slug].astro` | `fiche d'affaire — tertiaire / erp — 22-033` | `fiche d'affaire — tertiaire / erp` |
| Sous-titre de fiche (`jalons`) | `affaire 2022 · livraison 2024` | `livraison 2024`, ou le statut |
| Cartouche `FicheTechnique` | lignes `référence`, `année`, `livraison` | une seule ligne : `livraison` ou `statut` |
| Nomenclature `/references` | colonnes `référence` et `année` | colonnes supprimées (4 colonnes au lieu de 6) |
| Ligne mono mobile de la nomenclature | `secteur · statut · 22-033` | `secteur · statut` |
| Pied de vignette `CarteProjet` | `22-033 · La Rochelle` | `La Rochelle · livraison 2024` |
| Bloc « en avant » de l'accueil | `22-033 · La Rochelle` | `La Rochelle · livraison 2024` |

### Ce qui survit, et où

- **Le tri.** `parAffaireDecroissante` (`src/lib/projets.ts`) continue d'ordonner sur `annee` puis `reference`. C'est le bon critère : l'ordre d'ouverture des affaires est chronologiquement fiable, là où la livraison manque sur les affaires en cours. Le tri est un **usage interne de la donnée**, pas un affichage — l'ADR ne le touche pas.
- **Le JSON-LD.** `identifier: <reference>` et `dateCreated: <annee>` restent dans le `CreativeWork` de chaque fiche, ainsi que `temporalCoverage: <annee>/<annee_livraison>`. C'est **le seul endroit du HTML livré** où le numéro d'affaire subsiste, et c'est délibéré : ces propriétés servent l'indexation sémantique et la citation par les moteurs génératifs, pas la lecture humaine. Un lecteur ne les voit pas ; un agent qui recoupe des sources en a besoin pour désambiguïser deux ouvrages homonymes.
- **La validation.** Le `superRefine` de `src/content.config.ts` est **inchangé** : numéro d'affaire obligatoire dès que `demo: false`, concordance `reference` ↔ `annee` refusée au build en cas de contradiction, `annee_livraison` interdite tant que le statut est « en cours ». Ces contrôles portent sur la **justesse du dossier**, indépendamment de ce qui s'affiche.

### La règle de chronologie publique — une seule implémentation

`src/lib/projets.ts` expose deux fonctions, et elles sont le **seul** endroit du dépôt où la règle est écrite :

```ts
chronologie(projet)        // → { label: 'livraison', valeur: '2024' }  |  { label: 'statut', valeur: 'en cours' }
libelleChronologie(projet) // → 'livraison 2024'  |  'en cours'
```

La décision — réception prononcée ou non — se prend dans `chronologie` et nulle part ailleurs. `libelleChronologie` n'est qu'un aplatissement pour les contextes en ligne courante. Quatre consommateurs : `FicheTechnique`, le sous-titre de la fiche, `CarteProjet`, l'accueil. La nomenclature `/references` n'en est **pas** un — voir « Chronologie en nomenclature — ajournée » plus bas. **Toute réécriture du test `annee_livraison ? … : …` ailleurs dans le code est une régression de cet ADR**, pas une optimisation.

`libelleReference()` — qui rendait `reference ?? '—'` — est supprimée : elle n'avait plus d'appelant, et un tiret dans une colonne est une case vide qui s'ignore.

## Pourquoi les champs restent au schéma

Trois raisons, dans l'ordre de force :

1. **On ne supprime pas une donnée pour résoudre un problème de mise en page.** Le numéro d'affaire est ce qui relie une fiche du site au dossier papier de FT2E. Le jour où une fiche est contestée, corrigée ou reprise, c'est par lui qu'on retrouve la pièce d'origine. Le retirer du frontmatter rendrait les 19 fiches non traçables pour économiser six lignes de gabarit.
2. **Le contrôle de cohérence a besoin des deux champs.** `annee` sans `reference` ne se vérifie plus ; `reference` sans `annee` ne se trie plus. Le `superRefine` transforme une convention documentaire en invariant de build : une fiche dont le millésime contredit le numéro ne se publie pas. Cette garantie vaut indépendamment de l'affichage — elle a d'ailleurs déjà rattrapé une erreur de saisie le 2026-08-08.
3. **L'affichage est réversible, la donnée perdue ne l'est pas.** Si FT2E change d'avis — un secteur où le numéro d'affaire rassure, un usage export, une fiche PDF — le rendu se rebranche en une ligne. Une donnée effacée de 19 fichiers se re-saisit à la main sur 19 dossiers.

Corollaire pour l'édition : `reference` et `annee` **restent des champs Decap obligatoires et visibles** dans l'admin. FT2E continue de les saisir. Ils ne quittent que la page publique. Le `hint` de chaque champ dit désormais ce qu'il sert (traçabilité, tri, validation), et non plus ce qu'il affiche.

## Conséquences

### Positives

- La chronologie lue par le public est celle qui l'intéresse : livraison prononcée, ou état d'avancement. Aucune fiche n'affiche plus de date qui vieillit artificiellement une référence.
- **Aucune case vide** : les 14 fiches sur 19 qui n'ont pas encore de réception affichent leur statut, là où une ligne « livraison » vide ou un libellé orphelin traînait auparavant.
- La règle est centralisée. Un changement de formulation (« réceptionné en 2024 » plutôt que « livraison 2024 ») se fait en un point.
- Le numéro d'affaire disparaît du HTML lisible, y compris des vignettes de bas de fiche — la fuite la moins visible et la plus systématique, puisqu'elle se produisait sur **chaque** page de référence.

### Négatives, et ce qu'on en fait

- **La nomenclature `/references` ne porte plus aucune date.** Elle garde le statut (`livré` / `en cours` / `archive`), qui reste la colonne de rang. Un visiteur qui cherche les réalisations récentes doit ouvrir une fiche. Le correctif évident — remplacer la colonne `statut` par `libelleChronologie` — a été **implémenté, mesuré et ajourné** : voir la section dédiée ci-dessous.
- **Le champ `statut` n'était pas éditable dans Decap.** Il ne l'était déjà pas avant cet ADR, mais il devient ici la donnée chronologique publique de 14 fiches sur 19 — et il reste la colonne de rang de la nomenclature. **Corrigé** : widget `select` (`livré` / `en cours` / `archive`, défaut `livré`) ajouté à la collection `projets` de `public/admin/config.yml`, placé **avant** `annee_livraison` pour que son avertissement arrive dans l'ordre où l'éditeur saisit. Le hint dit le piège : passer à « livré » avant de renseigner l'année de livraison, sinon le build échoue sans message dans Decap.
- Le tri reste fondé sur une donnée que le visiteur ne voit plus. L'ordre de la nomenclature n'est donc plus explicable par la lecture seule de la page. C'est acceptable : l'ordre reste « du plus récent au plus ancien », ce que le lecteur postule de toute façon.

## Chronologie en nomenclature — ajournée

La conséquence négative ci-dessus appelait un correctif évident : donner à `/references` une colonne alimentée par `libelleChronologie`, en remplacement de la colonne `statut`. Elle affiche « livraison 2026 » sur les fiches réceptionnées et retombe sur le statut pour les autres. **Elle a été implémentée, mesurée sur le build, et retirée.** La colonne `statut` est rétablie, `rangs.statut` avec elle.

### Ce que la mesure a donné

Colonne telle qu'elle s'affichait, en regard de la clé de tri, sur les 19 fiches au 2026-08-09 :

| Rang | Fiche | Colonne affichée | Année d'ouverture (tri) |
|---|---|---|---|
| 1 | Études d'exécution fluides — Horizon | en cours | 2025 |
| 2 | Réhabilitation local commercial, Saintes | en cours | 2025 |
| 3 | Hôtel Le Yachtman | **livraison 2026** | 2024 |
| 4 | Étude notariale boulevard Joffre | en cours | 2024 |
| 5 | Siège de la RESE, Aigrefeuille | en cours | 2024 |
| 6 | Habitat inclusif, Salignac-sur-Charente | en cours | 2023 |
| 7 | Place des Chênes Verts, Saint-Rogatien | en cours | 2023 |
| 8 | Crèche de l'Oranger, Périgny | **livré** (sans année) | 2023 |
| 9 | Ancien siège communautaire, Marennes | **livraison 2026** | 2023 |
| 10 | Pas des Bœufs, Le Bois-Plage | en cours | 2022 |
| 11 | Abbaye de Sablonceaux | **livraison 2026** | 2022 |
| 12 | Résidence intergénérationnelle, Saint-Agnant | en cours | 2022 |
| 13 | Ateliers Capsulae | en cours | 2022 |
| 14 | Maubec, Chagnolet | en cours | 2022 |
| 15 | Maison relais, Saint-Jean-d'Angély | en cours | 2021 |
| 16 | EHPAD Aliénor d'Aquitaine | **livraison 2026** | 2021 |
| 17 | Néréa, Aytré | en cours | 2020 |
| 18 | « Le Fougerou », Sainte-Marie-de-Ré | **livraison 2026** | 2020 |
| 19 | Dix maisons, Saint-Georges-de-Didonne | en cours | 2019 |

### Pourquoi c'est rejeté

1. **La colonne est mono-valuée.** Les cinq fiches à réception prononcée portent **toutes le même millésime, 2026** — les seules réceptions actées sur pièce à ce jour sont récentes. Sur 19 lignes, la colonne ne montre donc qu'**une seule date**. Elle ne peut ordonner quoi que ce soit.
2. **Elle contredit visuellement l'ordre des lignes.** Les cinq « livraison 2026 » tombent aux rangs 3, 9, 11, 16 et 18, dispersées sur toute la hauteur, entre des « en cours ». La clé de tri descend proprement 2025 → 2019, mais elle est invisible : le lecteur voit une colonne qui n'explique pas l'ordre dans lequel on lui présente les affaires. Une colonne datée qui paraît mélangée est **pire** qu'une colonne de statut assumée.
3. **Un contrôle automatique de décroissance ne l'aurait pas détecté.** Compter les « ruptures de décroissance » sur cette colonne renvoie zéro — non parce que l'ordre est bon, mais parce qu'une colonne dont toutes les valeurs datées sont identiques ne peut ni croître ni décroître. Le chiffre rassurait à tort ; c'est la lecture du tableau, pas la métrique, qui a tranché.

La colonne `statut` ne prétend, elle, rien ordonner : elle qualifie chaque ligne indépendamment, et le rang de nomenclature reste porté par l'opacité du filet gauche **et** la graisse de l'intitulé, comme l'exige la charte.

### Cas particulier relevé — `creche-oranger-perigny`

Cette fiche porte `statut: livré` **sans `annee_livraison`**. Le schéma l'autorise (`annee_livraison` est optionnelle, et n'est interdite que sur un statut « en cours »), mais la combinaison est éditorialement incomplète : la fiche annonce une affaire livrée sans dire quand. En nomenclature elle affichait une cellule « livré » nue, sans millésime, au milieu de cellules datées — la plus faible du tableau. Deux issues, à trancher avec FT2E :

- **soit** la réception est prononcée et datable sur pièce → renseigner `annee_livraison`, et la fiche rejoint le lot des affaires datées ;
- **soit** elle ne l'est pas → le statut doit repasser à « en cours ».

Aucune des deux ne se décide depuis le dépôt : il faut la pièce. À vérifier lors de la passe rédactionnelle.

### Condition de réexamen

Rouvrir la question quand **`annee_livraison` est renseignée sur une majorité des fiches publiées** (soit 10 sur 19 aujourd'hui, seuil à réévaluer si le corpus grandit) **et** que ces millésimes s'étalent sur au moins trois années distinctes. Les deux conditions comptent : la première donne à la colonne de quoi remplir ses cellules, la seconde de quoi ordonner. Tant que l'une manque, la colonne `statut` reste le meilleur choix, et `libelleChronologie` continue de servir la fiche, les vignettes et l'accueil — où elle qualifie **une** affaire à la fois, usage pour lequel elle n'a aucun de ces défauts.

## Suivi

- Revoir la colonne de nomenclature (statut vs chronologie) après retour d'usage FT2E.
- Ajouter le champ `statut` à Decap avant la prise en main éditoriale par FT2E.
- Vérifier à chaque nouvelle surface d'affichage d'une fiche (export PDF, flux, page secteur) qu'elle consomme `libelleChronologie` et non les champs bruts.
