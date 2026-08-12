# Chantier des planches de références — programme et suivi

> **Objet.** Substituer, sur les 23 fiches de références, un dessin FT2E aux visuels
> actuels. **Ouvert le 2026-08-12. 1 planche publiée sur 23.**
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

## État — 1 / 23

| № | Fiche | Secteur | Archétype | État |
|---|---|---|---|---|
| 01 | `ecole-des-douanes-rue-du-jura-la-rochelle` | Monotechnique | `sankey-energie` | ✅ **publiée** |
| — | `abbaye-sablonceaux-ssi` | Patrimoine | | à faire |
| — | `ancien-siege-communautaire-marennes` | Tertiaire / ERP | | à faire |
| — | `atelier-dufour-yachts-perigny` | Industriel et commercial | | à faire |
| — | `ateliers-pilotes-capsulae` | Industriel et commercial | | à faire |
| — | `centre-formation-ormeau-du-pied-saintes` | Tertiaire / ERP | | à faire |
| — | `creche-oranger-perigny` | Tertiaire / ERP | | à faire |
| — | `cuisine-groupe-scolaire-villedoux` | Tertiaire / ERP | | à faire |
| — | `ehpad-coulonges-sur-autize-ssi` | Coordination SSI | | à faire |
| — | `etude-notariale-boulevard-joffre` | Tertiaire / ERP | | à faire |
| — | `exe-residence-horizon-mediatim` | Études d'exécution / BIM | | à faire |
| — | `fougerou-sainte-marie-de-re` | Logements | | à faire |
| — | `habitat-inclusif-salignac-sur-charente` | Logements | | à faire |
| — | `hotel-yachtman-quai-valin-la-rochelle` | Tertiaire / ERP | | à faire |
| — | `logements-maubec-chagnolet` | Logements | | à faire |
| — | `logements-nerea-aytre` | Logements | | à faire |
| — | `logements-pas-des-boeufs-bois-plage` | Logements | | à faire |
| — | `maison-relais-saint-jean-d-angely` | Logements | | à faire |
| — | `maisons-tourtet-saint-georges-de-didonne` | Logements | | à faire |
| — | `passerelle-ecluse-carreau-d-or-marans` | Monotechnique | | à faire |
| — | `place-des-chenes-verts-saint-rogatien` | Industriel et commercial | | à faire |
| — | `residence-intergenerationnelle-saint-agnant` | Logements | | à faire |
| — | `siege-rese-aigrefeuille` | Tertiaire / ERP | | à faire |

**Registre des archétypes employés** — à tenir à jour, il conditionne la variété de la série :

| Archétype | Employé | Module |
|---|---|---|
| `sankey-energie` | 1 (École des douanes) | ✅ `scripts/planches/sankey-energie.py` |
| `boucle-fluide` | 0 | à écrire |
| `coupe-traversee` | 0 | à écrire |
| `tableau-electrique` | 0 | à écrire |
| `zonage-ssi` | 0 | à écrire |
| `chronologie-affaire` | 0 | à écrire |
| `planche-chiffree` | 0 | à écrire — c'est le repli, il servira |

⚠️ **L'archétype se choisit sur la thèse de la fiche, jamais sur son secteur ni sur sa liste
de missions.** Neuf fiches sur vingt-deux portent la même quadruple mission
(Thermique · CVC · CFO · CFA) : s'y fier produirait neuf planches identiques. Ce qui les
sépare est ce que chacune démontre.

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
6. **Basculer la fiche** : remplacer `image_principale` / `image_principale_alt` par
   `planche:` dans le frontmatter.
7. **Contrôler** : `npm run typecheck`, `npm run build`, `npm run preview` + capture de la
   fiche, de la carte de secteur et du téléphone.
8. **Consigner** ici : numéro, archétype, arbitrages ouverts.

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
- **Le repli de lecture sous 1024 px** n'a de bloc composé que pour `sankey-energie`. Chaque
  nouvel archétype doit ajouter le sien dans `PlancheReference.astro`, faute de quoi la
  fiche perd son dessin sur téléphone sans rien mettre à la place.
- **Les six autres modules de composition** sont à écrire. Ce que `sankey-energie.py`
  contient de commun — jetons, mesure des chasses, échappement des insécables, double
  écriture des couleurs — a vocation à remonter dans un module partagé **le jour où le
  deuxième existera**, pas avant : factoriser sur un seul cas revient à généraliser un
  accident.
