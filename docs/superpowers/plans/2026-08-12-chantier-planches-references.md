# Chantier des planches de références — programme et suivi

> **Objet.** Substituer, sur les 23 fiches de références, un dessin FT2E aux visuels
> actuels. **Ouvert le 2026-08-12. 2 planches publiées sur 23.**
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

## État — 2 / 23

| № | Fiche | Secteur | Archétype | État |
|---|---|---|---|---|
| 01 | `ecole-des-douanes-rue-du-jura-la-rochelle` | Monotechnique | `sankey-energie` | ✅ **publiée** |
| 02 | `abbaye-sablonceaux-ssi` | Patrimoine | `zonage-ssi` | ✅ **publiée** |
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
| `zonage-ssi` | 1 (Abbaye de Sablonceaux) | ✅ `scripts/planches/zonage-ssi.py` |
| `boucle-fluide` | 0 | à écrire |
| `coupe-traversee` | 0 | à écrire |
| `tableau-electrique` | 0 | à écrire |
| `chronologie-affaire` | 0 | à écrire |
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

AVANT TOUTE AUTRE CHOSE, cloner le dépôt et lire le protocole (révision 4). Il fait
autorité sur tout ce qui suit, y compris sur ce message :

    git clone --depth 1 https://github.com/JeffCrn/ft2e-v3
    docs/superpowers/specs/2026-08-12-planches-references-protocole.md

LA PLANCHE EST UN DESSIN. Elle schématise la solution apportée par FT2E — un mécanisme
dont la géométrie porte la démonstration. Elle ne répète AUCUNE donnée que la fiche
porte déjà : pas de colonne de relevé, pas de classements, pas de listes.

Fiche à traiter :  <slug>
    src/content/projets/<slug>.md   — frontmatter ET corps, jamais un résumé

Archétypes déjà employés, à ne pas répéter sans raison explicite :
    sankey-energie — ecole-des-douanes-rue-du-jura-la-rochelle
    zonage-ssi — abbaye-sablonceaux-ssi

Exemple achevé, à consulter comme référence de niveau attendu :
    public/images/projets/abbaye-sablonceaux-ssi/planche.json
    scripts/planches/zonage-ssi.py
    (la planche 01, École des douanes, garde une colonne de relevé antérieure à la
    révision 4 — ne pas l'imiter sur ce point)

CE QUE TU REMETS — un dossier <slug>/ contenant les quatre fichiers du protocole,
puis le prompt de lancement de la session suivante (une fiche = une session).

  · Si l'archétype retenu a déjà son compositeur dans scripts/planches/, tu ne produis
    QUE planche.json, puis tu lances :
        python scripts/planches/<archetype>.py <dossier>
    qui écrit planche.svg et vignette.svg. N'écris pas de SVG à la main dans ce cas.

  · Sinon, tu écris aussi les deux SVG selon les gabarits du protocole (1200 × 800 et
    300 × 200), et tu me dis explicitement qu'un compositeur reste à écrire.

  · Le PNG 2400 × 1600 dans les deux cas.

  · Le prompt de la session suivante : ce gabarit, avec la première fiche « à faire »
    du programme du suivi et la ligne des archétypes actualisée depuis le registre.

TROIS CHOSES QUE JE REFUSERAI :
  · un tableau de synthèse habillé — masque mentalement le texte du dessin : si la
    géométrie seule ne démontre plus rien, ce n'est pas une planche. La première
    version de la planche 02 a été refusée pour ce motif exact ;
  · une planche que tu n'as pas regardée À SA TAILLE DE LECTURE — 1152 px pour la
    planche, une carte de 296 px pour la vignette. Le rendu en pleine page ne prouve
    rien : les sept défauts de la première planche y étaient tous invisibles ;
  · une extraction dont `a_valider_ft2e` est vide. Un dessin tranche toujours ce qu'un
    texte laisse ouvert ; une liste vide signifie que tu ne l'as pas vu, pas qu'il n'y
    avait rien à trancher.

Réponds par les fichiers, puis en prose brève : l'archétype retenu et son motif, les
arbitrages laissés à FT2E, ce que tu as dû exclure, et ce que le contrôle à la taille de
lecture t'a fait corriger. Termine par le prompt de la session suivante. Ne me raconte
pas ta méthode.
```

**Ce que la session ne fait pas** : elle ne touche ni au frontmatter de la fiche, ni au
site. La bascule `image_principale` → `planche` et le contrôle de rendu se font ici, dans
une session de dépôt, une fois les quatre fichiers reçus.

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
9. **Produire le prompt de lancement de la session suivante** depuis le gabarit
   ci-dessus — première fiche « à faire » du programme, registre des archétypes
   actualisé. **Une fiche = une session** : une session qui rend ses fichiers sans le
   prompt suivant laisse le chantier sans relève.

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
- **À répercuter** : le protocole (révision 4 à écrire — le gabarit prescrit encore la
  partition 7/5 avec colonne de relevé) et la **planche 01** (sa colonne de relevé
  répète la fiche de l'École des douanes — réalignement à trancher avec FT2E).

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
- **Le repli de lecture sous 1024 px** a ses blocs pour `sankey-energie` et `zonage-ssi`.
  Chaque nouvel archétype doit ajouter le sien dans `PlancheReference.astro`, faute de quoi
  la fiche perd son dessin sur téléphone sans rien mettre à la place.
- **Les cinq autres modules de composition** sont à écrire. Le deuxième module existe
  depuis la planche 02 : la **factorisation du tronc commun** de `sankey-energie.py` et
  `zonage-ssi.py` — jetons, mesure des chasses, insécables, double écriture des couleurs,
  repli de libellé — est désormais légitime, à faire avant d'écrire le troisième.
- **Le `grep -c` de Git Bash sous Windows ne sait pas chercher U+202F** (`grep -c $' '`
  rend 0 sur un fichier qui en porte 9) : le contrôle des insécables du protocole se rejoue
  en Python (`collections.Counter`) sur cette machine, pas en grep.
