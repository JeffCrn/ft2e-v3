# Chantier des 27 nouvelles fiches références — de 23 à 50 (ouvert le 2026-08-27)

Commande FT2E du 2026-08-27 : compléter le catalogue par **27 nouveaux dossiers
d'affaires**, en accomplissant pour chacun **exactement le même travail** que pour
les 23 premières fiches — dépouillement, fiche de collecte, fiche publiée, planche
de schéma de principe. Contrainte reconduite : **une session = un dossier**, close
par le prompt de la session suivante.

**Ce plan ne réécrit pas les protocoles fondateurs : il les branche.** Les deux
textes opératoires restent :

| Pièce | Rôle |
|---|---|
| `docs/superpowers/plans/2026-08-07-chantier-references-reelles.md` | la FICHE — § Contraintes globales, § Protocole de session (12 étapes), gabarit de prompt, corrections apprises (numéro d'affaire, synthèse, ouvrage, convention numérale) |
| `docs/superpowers/specs/2026-08-12-planches-references-protocole.md` | la PLANCHE — révision 5 : extraction `planche.json`, archétypes, règles dures 1-7, gabarits 1200 × 800 / 552 × 368 / 300 × 200, contrôles aux tailles réelles |
| `docs/superpowers/plans/2026-08-12-chantier-planches-references.md` | le déroulé de session planche (§ Ce que fait une session) et les pièges de rendu (cairosvg, U+202F, iframe 390) |
| `.claude/rules/content-collections.md` + `src/content.config.ts` | le schéma qui fait foi (taxonomie ACTUELLE) |
| `.claude/rules/french-editorial.md` | voix, typographie, convention numérale FINALE (un seul mot = lettres, composé = chiffres) |

## 1. État d'entrée — ce qui diffère de 2026-08

- **L'ancien fonds d'archives n'existe plus.** `C:\ft2e-arch\` et son ZIP ont été
  supprimés le 2026-08-16 ; `references/inventaire-archives-2026.csv` n'inventorie
  que l'ancien corpus. **Le chemin du nouveau fonds est fourni par l'utilisateur**,
  à l'ouverture du chantier ou dossier par dossier.
- **L'espace de travail continue** : `references/` (gitignoré, motif ancré) porte
  `ref_001` à `ref_023` — les nouveaux dossiers de travail se numérotent
  **`ref_024` à `ref_050`**, numérotation continue. Les sources croisées restent
  valables : `references/docs_references/` (11 docx sectoriels) et
  `docs/20-source-plaquette-2024.md`.
- **La taxonomie a bougé** (BREAKING `8250827` puis `3a24cdf`) : secteurs =
  `Logements | Tertiaire / ERP | Industriel | Patrimoine | Monotechnique — Audit |
  Coordination SSI | Études d'exécution / BIM` (tiret cadratin, Audit en bas de
  casse) ; la typologie **`Étude`** existe pour les missions sans travaux (audit,
  faisabilité) — plus aucun atterrissage forcé en `Réhabilitation`.
- **La planche est OBLIGATOIRE au schéma** : une fiche sans ses cinq pièces
  (`planche.json`, `planche.svg`, `appui.svg`, `vignette.svg`, `planche.png` dans
  `public/images/projets/<slug>/`) **ne build pas**. Conséquence structurante :
  là où les chantiers fondateurs étaient deux chantiers successifs, **une session
  produit la fiche ET sa planche, dans le même commit**.
- **Plus de visuel photographique de fiche** : les champs `image_principale` ont
  disparu, le dispositif visuel est la planche. Un cliché trouvé au dossier peut
  candidater au corpus SECTEURS (arbitrage FT2E, hors session).
- **Le repli de lecture n'existe plus** : les blocs d'archétype du `planche.json`
  servent les compositeurs et la relecture FT2E, plus aucun rendu. L'alternative
  textuelle passe par l'`aria_label` de l'extraction (règle dure 7 inchangée).
- **`verser.py <slug>`** garde toute sa valeur de CONTRÔLE des cinq pièces et de
  l'extraction ; sa bascule de frontmatter (`image_principale` → `planche:`) est
  sans objet sur une fiche neuve — écrire `planche:` directement, puis passer
  `verser.py` pour ses contrôles. S'il refuse une fiche déjà conforme, lire son
  message avant de conclure.
- **ADR-003 et chronologie éditoriale** : `reference` et `annee` ne s'affichent
  jamais ; le site annonce « livraison AAAA » via `MILLESIME_LIVRAISON_ANNONCE`
  (2026) sur les affaires non réceptionnées. ⚠ Cette constante sera fausse au
  1ᵉʳ janvier 2027 sans que rien ne le signale.
- **`commune()` échoue bruyamment** : le champ `lieu` DOIT porter le code postal
  entre parenthèses — « Aytré (17440) » au minimum.
- **Deux titres, deux emplois** : le `titre` long du frontmatter (h1, SEO) et le
  titre COURT du `planche.json` (cartes, index — lu par `titreCourt()`, échec
  bruyant s'il manque). Ne jamais recopier l'un dans l'autre.
- **Le maillage se fait à la rédaction** : chaque fiche neuve arrive avec ses
  **≥ 5 liens internes contextuels** (expertises, secteurs, fiches voisines) —
  `scripts/controle-liens-internes.py` doit rendre « N/N atteignent 5 liens ».
  La passe globale de 2026-08-10 ne se rejouera pas pour rattraper une fiche.
- **Le gabarit des métadonnées est repris** (`title` 50-60, `description`
  140-160 composés par `references/[...slug].astro`) : rien à faire par fiche,
  mais vérifier l'unicité sur le site (46 + n pages).
- **A13** : le voyage du visuel carte → fiche est automatique (`transition:name`
  posé par `CarteProjet` et le gabarit de fiche) — rien à faire par fiche.
- **Répartition des archétypes à l'ouverture** (23 planches) : boucle-fluide 7 ·
  coupe-traversée 4 · sankey-énergie 4 · zonage-ssi 3 · tableau-électrique 3 ·
  chronologie-affaire 2 · **planche-chiffrée 0, et son module n'existe pas** —
  si un dossier l'exige, décision à prendre (l'écrire, ou retirer l'archétype de
  la liste fermée) plutôt qu'un bricolage. Varier : se re-mesurer à chaque
  session (`grep archetype public/images/projets/*/planche.json`).
- **Arbitrage FT2E du 2026-08-27 (session N01, sur la premiere planche livree) : la
  planche schematise la SOLUTION APPORTEE, jamais le deroule de l'affaire.** La
  premiere planche des Portes-en-Re portait le phasage de l'operation (deux
  chantiers sur un axe des temps) : refusee — c'est un recit historique, pas une
  conception technique. Elle a ete refaite en `boucle-fluide`, mecanisme
  `terminaux` (six locaux a equipement propre, l'air pour seul reseau, aucun
  noeud central), et le mecanisme `relais` retire du compositeur chronologie.
  C'est la regle de la revision 4 du protocole (« le dessin montre un mecanisme »)
  relue strictement : un archetype `chronologie-affaire` n'est admissible que si
  sa these est d'INGENIERIE (precedence de reservations d'Horizon, divergence
  reglementaire de Tourtet), pas le calendrier d'une operation.
- **L'accueil bougera tout seul** : « Références récentes » sert les `en_avant`
  puis les affaires les plus récentes — une fiche 25-NNN ou 26-NNN nouvelle y
  entrera d'elle-même. `en_avant: false` par défaut, arbitrage FT2E sinon.

## 2. Le pipeline d'une session (fusion des deux protocoles)

1. **Ouverture** — lire ce plan (§ 1, § 2, § Suivi) et le prompt de session.
2. **Dépouillement** du dossier d'affaires (chemin fourni). Pièces prioritaires :
   synthèse RT/RE la plus récente, CCTP des lots FT2E, DPGF/estimation, pièces
   marché. PDF par l'outil Read (param `pages`).
   **2 bis. Relevé du numéro d'affaire `NN-NNN` sur une pièce FT2E** (« Affaire
   n° : … », devis, cartouche) — jamais sur le seul nom de dossier ; gare aux
   numéros des cotraitants. En déduire `annee`.
3. **Dossier de travail** `references/ref_NNN/` (suite de ref_023) : 3 à 8 pièces
   décisives copiées — la traçabilité de chaque affirmation.
4. **Croisement commercial** : docx sectoriels + plaquette. Conflit → la pièce du
   dossier fait foi, conflit noté.
5. **Fiche de collecte** `references/ref_NNN/fiche-collecte-<slug>.md` — A/A+
   préremplies, B/C/D/E en questions pour FT2E.
6. **Rédaction de la fiche** `src/content/projets/<slug>.md` : frontmatter complet
   (taxonomie actuelle, `lieu` avec code postal, `reference`/`annee` cohérents,
   `annee_livraison` seulement sur réception prononcée, `ouvrage` 2-40 signes,
   `mission_ft2e`) ; récit 4 sections ; `synthese` 480-780 signes écrite après le
   récit ; **synthèse et récit posés par script Python** (les outils d'édition
   normalisent les insécables — `scripts/injection-typographique.py` après coup) ;
   convention numérale finale ; ≥ 5 liens internes ; AUCUN numéro d'affaire ni
   millésime d'ouverture en prose.
7. **Planche** — protocole révision 5, intégralement : extraction `planche.json`
   (archétype choisi sur la THÈSE, motif justifié, `a_valider_ft2e` non vide) ; composition par
   `python scripts/planches/<archetype>.py public/images/projets/<slug>` ;
   contrôles AUX TAILLES RÉELLES (planche 1152, vignette dans une carte de
   274-296, appui à 552) ; PNG 2400 × 1600 ;
   `python scripts/apostrophes-planches.py` (mesure puis `--appliquer` si
   besoin) ; `python scripts/planches/verser.py <slug>` pour ses contrôles.
8. **Contrôles qualité** : `npm run typecheck` (0 erreur) ; `npm run build` vert
   (46 + n pages — Zod refuse calibre, taxonomie, contradiction
   référence ↔ année, planche manquante) ; relecture `editorial-reviewer` ;
   `python scripts/controle-liens-internes.py` (0 mort, N/N à 5 liens) ;
   `python scripts/controle-numeros-affaire.py` (0 fuite hors JSON-LD) ;
   `python scripts/releve-numeral.py` (aucun écart nouveau).
9. **Commit UNIQUE** fiche + planche + collecte hors dépôt :
   `content(references): ajoute la fiche réelle <nom court> et sa planche`.
   ⚠ `git ls-remote` avant (dépôt partagé) ; le hook Stop pousse ce qui traîne.
10. **Livraison** : push (c'est lui qui déploie), `curl` de la fiche AVEC barre
    oblique finale, marqueur du commit dans le HTML servi ; contrôle du rendu de
    la fiche aux trois bandes (≥ 880 / 480-879 / < 480 — sonde iframe pour les
    largeurs téléphone) et de sa carte dans `/references`.
11. **Suivi** : ligne du § Suivi ci-dessous (statut, archétype, arbitrages,
    questions B-E ouvertes).
12. **Prompt de la session suivante** — rédigé en annexe de CE plan (append) et
    reproduit intégralement au message final. Gabarit : celui du plan de
    2026-08-07, adapté (chemin d'archives du dossier suivant fourni par
    l'utilisateur, ou demandé en ouverture).

## 3. Questions d'ouverture (posées à la session N01, réponses à consigner ici)

- **Q1 — le chemin du nouveau fonds d'archives**, et sa structure (un répertoire
  par affaire ? un inventaire existe-t-il ?).
- **Q2 — la liste des 27 dossiers** et l'ordre souhaité (à défaut : même logique
  que 2026-08 — les mieux documentés d'abord, couverture des secteurs, dossiers
  minces en fin).
- **Q3 — la règle des dossiers minces** est-elle reconduite (matière insuffisante
  → collecte seule + substitution proposée) ?
- **Q4 — les questions transversales T1-T7** du chantier fondateur (autorisations
  MOA, montants publiables, graphies d'acteurs…) valent-elles pour les 27 ?

### Réponses consignées le 2026-08-27 (session N01)

- **Q1 — répondu.** Le fonds est livré **par tranches de millésime de livraison** :
  la première est `C:\claude_code_dev_projectst2e_new_archives5.zip`
  (1,7 Go, 1 298 fichiers, un répertoire par affaire sous `2025/`, pas
  d'inventaire). Cadrage utilisateur : **les 23 fiches en ligne couvrent les
  livraisons 2026 ; cette tranche couvre les livraisons 2025.** ⚠ Le disque de la
  machine est saturé (1,9 Go libres avant extraction) : l'extraction se fait
  **dossier par dossier, par session** — le ZIP reste la source, le répertoire
  extrait de la session précédente se supprime à l'ouverture de la suivante.
- **Q2 — partiellement répondu.** La tranche 2025 porte **10 dossiers** (liste
  ci-dessous) ; les tranches suivantes viendront d'autres millésimes (objectif 27).
  Ordre non imposé par FT2E → règle par défaut reconduite : les mieux documentés
  d'abord, couverture des secteurs, dossiers minces en fin. ⚠ **Collision relevée :
  `23-075` (« Extension crèche Périgny UDAF ») est déjà publié**
  (`creche-oranger-perigny.md`, ref_001) — ce dossier ne produit pas de fiche
  nouvelle ; il peut en revanche répondre à la question T7 (millésime de livraison
  de la crèche) et compléter la fiche existante. **9 dossiers publiables.**

  | Fichiers | Dossier de la tranche 2025 | Note |
  |---|---|---|
  | 273 | `22-011- Réhab Mairie Les Portes en Ré - BTB` | **N01 → ref_024** |
  | 255 | `21-062 - Pôle commercial FORS 79 - BTB` | |
  | 208 | `19-036 -150 logts Rompsay MEDIATIM` | « AURORA » — le cliché du hero de l'accueil vient de cette opération |
  | 191 | `25-004 - Musée Pierre Loti ROCHEFORT` | l'ancienne fiche DÉMO « maison-pierre-loti » (supprimée) portait ce sujet |
  | 103 | `19-096 - Eglise St Sauveur - GOUTAL` | |
  | 102 | `22-013- 16 Logts L'Houmeau OPH - BTB` | |
  | 73 | `23-075- Extension creche Périgny UDAF - ASP` | ⚠ déjà publié (ref_001) — hors programme de fiches neuves |
  | 58 | `23-009- 60 maisons Louise Magnan - IAA` | |
  | 25 | `23-099 - CPAM La Rochelle` | dossier mince ? |
  | 10 | `23-083- Airbus - Comptage énergie - EQUANS` | dossier mince ? candidat Monotechnique — Audit |
- **Q3 — non répondu, défaut reconduit** : matière insuffisante → collecte seule +
  substitution proposée. À confirmer par FT2E.
- **Q4 — non répondu, défaut reconduit** : T1-T7 valent pour les nouvelles fiches
  (T6 reste hors chantier — page Équipe). À confirmer par FT2E.

### Complément consigné le 2026-08-27 au soir (session N02) — le classeur FT2E

**FT2E a fourni son propre classeur de références** (« REFERENCES SITE FT2E.ods »,
déposé dans `docs/references/` pendant la session, **déplacé dans
`references/docs_references/`** — il liste tous les numéros d'affaire et le dépôt
est public). Il complète les réponses Q1/Q2 :

- **les tranches suivent le millésime de livraison** : « Finalisées en 2026 » (les
  23 fiches en ligne + Yachtman « T § C », Loti absent), **« Finalisées en 2025 »**
  (les 10 dossiers de `2025.zip`), puis 2024 (5 : 19110 CDAIR, 20031 UNDERTECH,
  21093 Central Hostel, 21095 Voltaero, 23036 Fountaine Pajot), 2023 (5), 2022 (4),
  2020 (2), 2019 (1) — le compte au-delà de la tranche 2025 fera l'objet des
  prochains ZIP ;
- **le classeur porte le SECTEUR de chaque affaire selon FT2E** (légende
  L/T/I/P/C/M/E) — il fait foi : la N02 a classé Fors `Tertiaire / ERP` (« 21062 ·
  Commerces de Fors · T ») là où le dépouillement penchait pour `Industriel`
  (Saint-Rogatien, pôle commercial lui aussi, y est pourtant « I ») ;
- ⚠ **23075 (crèche de Périgny) figure dans DEUX tranches** (« Finalisées en 2026 »
  et « Finalisées en 2025 » en « Extension crêche Périgny UDAF ») — à trancher avec
  FT2E (question T7, millésime de livraison de la crèche) ;
- ~~certaines affaires portent un domaine double (« T § C », « P § C ») que la
  taxonomie du site ne connaît pas~~ — **TRAITÉ le 2026-08-27 au soir** (demande
  utilisateur) : champ optionnel `secteur_secondaire` au schéma + Decap (commit
  `ce334b2`, sous-agent content-modeller), branché sur les filtres de /references,
  les pages de secteur, les projets similaires, l’eyebrow, le cartouche et le
  JSON-LD. **Les 25 fiches publiées sont alignées sur le classeur** (commit
  `09270a3`) : sept bascules (abbaye → Coordination SSI, Dufour et Villedoux →
  Monotechnique — Audit, École des douanes → Études d’exécution / BIM, maison
  relais → Tertiaire / ERP, passerelle de Marans → Patrimoine, Chênes Verts →
  Industriel) et le Yachtman « T § C » en double domaine. Répartition vérifiée
  au déploiement : 7/9/2/1/3/2/2 — les sept secteurs peuplés. Les fiches à venir
  prennent leur secteur (et l’éventuel secondaire) DANS LE CLASSEUR.

### Complément consigné le 2026-08-31 (session N10) — la tranche 2024 (Q1/Q2)

- **Q1 — le ZIP de la tranche « Finalisées en 2024 » est livré** :
  `C:\claude_code_dev_projects\ft2e_new_archives\2024.zip` (472,7 Mo,
  648 entrées, racine `2024/`, un répertoire par affaire, pas d'inventaire).
  Même discipline que la tranche 2025 : extraction dossier par dossier par
  `zipfile` (jamais un chemin tapé — noms en mojibake), le répertoire extrait
  de la session précédente se supprime à l'ouverture de la suivante, le ZIP
  reste la source.
- **Q2 — ordre non imposé par l'utilisateur** (« Continuer ») → règle par
  défaut reconduite : les mieux documentés d'abord, d'après le compte de
  fichiers lu par `zipfile.namelist()` — sans jamais conclure « mince » sur ce
  seul compte (quatre démentis en N08-N09) :

  | Fichiers | Dossier de la tranche 2024 | Classeur | Note |
  |---|---|---|---|
  | 199 | `19-110 -CDAIR  St Martin de Ré -ARCHITEM` | 19110 · T § C | **N10 → ref_033** |
  | 159 | `20-031- Projet tertiaire UNDERTECH Médiatim -SMART` | 20031 · T | |
  | 96 | `21-093- Rehab bat rue de l'ESCALE - SMART` | 21093 · T § C | Central Hostel |
  | 72 | `21-095- VOLTAREAO ST AGNANT - Cab SOURD` | 21095 · I | graphie VoltAero (coquille « Voltareo » déjà relevée sur la plaquette) |
  | 70 | `23-036- Extension bat 5-8 Fountaine Pajot - ASP` | 23036 · I | |

## Suivi (une ligne par session)

| N | Affaire | Slug | Fiche | Planche (archétype) | Collecte | Notes |
|---|---|---|---|---|---|---|
| N01 | 22-011 — Réhabilitation de la mairie et création de l'office de tourisme, Les Portes-en-Ré | `mairie-les-portes-en-re` | ✅ rédigée, build 47 pages | ✅ `boucle-fluide`, **mécanisme `terminaux` créé** (8ᵉ du compositeur — invariant octet des 7 planches existantes vérifié avant/après ; une 1ʳᵉ planche `chronologie/relais` a été refusée par FT2E — voir l'arbitrage au § 1 — et le mécanisme retiré) | ✅ ref_024 (8 pièces) | `annee_livraison: 2025` sur docx commercial « RÉALISATION : 2025 » + cadrage tranche — PV de réception absent (→ B1) ; questions B1-B4, C1-C2, E1-E2 ouvertes ; Eric Moinet vérificateur des CCTP (T6) ; secteur Tertiaire / ERP |
| N02 | 21-062 — Construction d'un pôle commercial et requalification des espaces urbains et paysagers, Fors | `pole-commercial-fors` | ✅ rédigée, build 48 pages | ✅ `sankey-energie`, **mécanisme `partage` créé** (5ᵉ du compositeur — invariant octet des 4 planches sankey existantes vérifié avant/après la greffe, 16/16 deux fois) — l'année d'énergie de l'étude d'autoconsommation collective (36 kWc), en-tête de registre nommant l'étude | ✅ ref_025 (8 pièces) | `annee_livraison: 2025` (cadrage tranche + classeur FT2E « Finalisées en 2025 ») ; secteur `Tertiaire / ERP` par le classeur (≠ dépouillement qui penchait `Industriel`) ; mission MOE photovoltaïque séparée (21-062PV, DCE 04/2025, travaux prévus sept.-oct. 2025 → B2) ; questions B1-B5, C1-C2, E1-E3 ouvertes ; auteurs relevés (T6) : Mathieu Braud, Vincent Jaoul, Sandrine Rameau, Tanguy Moinet, Eric Moinet |
| N03 | 19-036 — Résidence Aurora, 147 logements dans le quartier de Rompsay, La Rochelle | `residence-aurora-la-rochelle` | ✅ rédigée, build 49 pages | ✅ `coupe-traversee`, **mécanisme `colonne` créé** (5ᵉ du compositeur — invariant octet des 4 planches existantes vérifié avant/après la greffe puis après la passe apostrophes, 16/16 trois fois) — le conduit collectif 3CEp confronté à la ventouse individuelle, trois gabarits proportionnels aux débits Promotelec (12/14/16 L/min) | ✅ ref_026 (8 pièces) | `annee_livraison: 2025` (classeur « Finalisées en 2025 » + cadrage tranche ; CR MOE 132 du 16/07/2025 en « bonne fin de travaux », GPA — PV de réception absent → B1) ; secteur `Logements` par le classeur (« 19036 · 150 Logts Rompsay Mediatim - AURORA · L ») ; MOA SARL Opus, commanditaire Mediatim Promotion (contrat direct promoteur — même groupe que Horizon 25-097) ; compte de logements élucidé sur pièces : 150 (propo 2019) → 148 (études 2021) → 147 (marché déc. 2022) — la légende du hero « Aurora, 147 logements » était déjà juste, aucune retouche ; T1 en chauffe-eau électrique 100 L (§ 3.3), compteur gaz par logement (§ 5.1) ; mission de base sans DET ni AOR (suivi OTEEC) + AMO label Promotelec (−20 % A-B-D-E-F-G / −10 % C) + 2 reprises thermiques (gain 20 % 2021, Alkern/ECBL 2023) ≠ docx « mission complète » → B2 ; questions B1-B6, C1-C3, E1-E3 ouvertes ; /secteurs/logements n'affiche que les 4 affaires les plus récentes du secteur — 19-036 hors du top 4, comportement de gabarit |
| N04 | 25-004 — Maison de Pierre Loti, reprise des lots techniques et coordination SSI, Rochefort | `maison-pierre-loti-rochefort` | ✅ rédigée, build 50 pages | ✅ `zonage-ssi`, **mécanisme `inversion` créé** (4ᵉ du compositeur — invariant octet des 3 planches existantes rejoué avant la greffe, après la greffe et après la passe apostrophes : 12/12 trois fois ; la passe a courbé 8 apostrophes droites fuies dans les chaînes de contrôles du compositeur, piège N03 reconfirmé) — deux familles de détection aux hauteurs proportionnelles (46 radio / 38 filaire) convergent vers l’ECS-CMSI, quatre départs de mise en sécurité TOUS fléchés : la mise en sécurité inverse la scénographie | ✅ ref_027 (8 pièces) | **Premier double domaine de la tranche** : `Patrimoine` + `secteur_secondaire: Coordination SSI` par le classeur (« 25004 · Maison pierre Loti · P § C ») ; `annee_livraison: 2025` sur PV de réception SSI du 21/10/2025 (avis favorable, V. Jaoul) + classeur — le PV de réception des TRAVAUX manque → B1 ; mission de REPRISE : cessation d’activité du BET CIEL Ingénierie, lots à 80-90 %, FT2E sous-traitant de Sunmetron par acte spécial DC4 (marché MOE Ville de Rochefort n° 2019/030) — conception et visas restés à l’équipe d’origine ; les docx commerciaux disent « Livraison 2026 » et « type E », les pièces 2025 et « type Y, L et M, 5ᵉ catégorie » → B3/B4, la pièce fait foi ; SSI catégorie A / alarme type 1 sur ERP 5ᵉ catégorie, détection 46 radio / 38 filaire (as-built Chubb 01/09/2025), 15 zones, une seule ZA, sous-fonctions remise en lumière / arrêt sonorisation / arrêt CTA ; § Loti de `secteurs/patrimoine.md` RÉÉCRIT sur pièces (plancher chauffant et BIM non sourcés retirés, lien vers la fiche) ; questions B1-B6, C1-C2, E1-E4 ouvertes |
| N05 | 19-096 — Restauration du clocher, des cloches et du beffroi de l'église Saint-Sauveur, La Rochelle | `eglise-saint-sauveur-la-rochelle` | ✅ rédigée, build 51 pages | ✅ `tableau-electrique`, **mécanisme `montee` créé** (4ᵉ du compositeur — invariant octet des 3 planches existantes rejoué avant la greffe, après la greffe et après la passe apostrophes : 12/12 trois fois ; la passe a ENCORE courbé 6 apostrophes droites fuies dans les chaînes de contrôles du mécanisme neuf, piège N03/N04 reconfirmé) — deux flux contraires sur la même verticale : l'énergie monte du TGBT de la sacristie aux deux tableaux de la salle des cloches (TD-SMV 5 kVA, TD-MC 3 kVA, la commande des sonneries en pointillé), la foudre redescend du paratonnerre niveau I vers ses prises de terre, liaison équipotentielle refermée | ✅ ref_028 (8 pièces) | Marché de MOE Ville de La Rochelle n° 2019-312, groupement conjoint Agence Goutal (Michel Goutal, ACMH, mandataire) + CECIBAT (économiste MH) + FT2E (BET fluides) — mission complète DIAG 1-2 → AOR, part FT2E 9 500 € HT portée à 14 615,57 € par l'avenant 1 (coût prévisionnel APD 1 966 332,88 € HT contre 1 200 000 initial — le docx commercial publie encore 1,2 M → B2) ; FT2E écrit les lots 6 électricité CFO/CFA et 7 paratonnerre (CCTP/DPGF PRO octobre 2021, « Affaire n° : 19096 », auteur V. Jaoul, vérifié E. Moinet — T6) ; église inscrite ISMH, clocher du XVᵉ classé MH depuis le 13/04/1907 (CCTP MOE Ville) ; secteur `Patrimoine` par le classeur (« 19096 · Eglise St SAUVEUR · P »), pas de domaine double ; `annee_livraison: 2025` sur CR d'OPR n° 58 du 22/04/2025 (OPR du 8 au 22 avril « date de la réception », levée des réserves le 06/05/2025) + classeur — PV de réception des travaux absent → B1 ; chantier 09/2022 → 04/2025, suspendu 4 fois par la Ville (juillets et décembres 2023-2024) ; cloches bénies le 20/04/2025, levage et mise en service fin juin 2025 (nombre de cloches final → B3 : TD-MC dimensionné 5 volée + 5 tintement, le CCTP MOE partait de 2 cloches dont 1 à refondre) ; questions B1-B5, C, E ouvertes |
| N06 | 22-013 — Construction de 16 logements, ZAC ÉcoQuartier de L’Houmeau (secteur de Monsidun) | `logements-ecoquartier-l-houmeau` | ✅ rédigée, build 52 pages | ✅ `sankey-energie`, **mécanisme `affectation` créé** (6ᵉ du compositeur — invariant octet des 5 planches sankey existantes rejoué avant la greffe, après la greffe et après la passe apostrophes : 20/20 trois fois ; la passe a ENCORE courbé 6 apostrophes droites — 3 dans les chaînes du mécanisme neuf, 3 dans l’extraction —, piège N03-N05 reconfirmé) — seize logements sans chaufferie commune affectés à trois productions par typologie (13 chaudières gaz individuelles / 1 PAC double service au T4 / 2 T1 tout électriques à CET), second registre : les 8 modules PV de 375 Wc à micro-onduleur, autoconsommation individuelle des logements de l’étage | ✅ ref_029 (8 pièces) | Secteur `Logements` par le classeur (« 22013 · 16 Logements l’Houmeau- Monsidun · L ») ; `annee_livraison: 2025` sur CR de chantier n° 60 du 30/06/2025 (« RÉCEPTION LE 30/06 (hors VRD et espaces verts) ») + classeur — PV de réception absent → B1 ; MOE en groupement conjoint BTB (mandataire) + BAG + FT2E + Acoustex + BF ECO (économiste-OPC, CR préfixés « 543 » — numéro du cotraitant), mission base + EXE + OPC + diag performances énergétiques (FT2E 95 %), part FT2E 30 518,83 € HT (18,22 %) ; programme 2 T1 bis (PLAI) + 2 T2 + 11 T3 + 1 T4, charte ÉcoQuartier (biosourcés 18 kg/m² SP, solaire imposé) ; certification « BEE » (synthèse RE2020) contre « BEE+ » (docx) → B2 ; 8 modules/coffrets pour 7 logements à l’étage → B4 ; valeurs dessinées = DCE 07/2023, DOE absent → B5 ; « logements individuels » (docx) contre « collectifs » (calcul RE2020) → B6 ; questions B1-B6, C, E ouvertes ; T6 : Mathieu Braud et Vincent Jaoul aux CR, DPGF « MB », synthèse RE rédacteurs « KB »/« GM » à identifier |
| N07 | 23-009 — Reprise de la ventilation de soixante maisons individuelles, cité Louise Magnan, La Rochelle | `maisons-louise-magnan-la-rochelle` | ✅ rédigée, build 53 pages | ✅ `coupe-traversee`, **mécanisme `sortie` créé** (6ᵉ du compositeur — invariant octet des 5 planches existantes rejoué avant la greffe, après la greffe et après la passe apostrophes : 20/20 trois fois ; ⚠ pour la première fois depuis la N03 la passe n’a RIEN courbé — les chaînes de contrôles ont été écrites courbes ET mesurées avant de composer) — AVANT/APRÈS : l’extracteur en coffre et ses gaines souples convergeant sur le seul piquage cuisine, rejet en façade, entrées d’air barrées, contre le caisson sur dallettes et résilient AU-DESSUS de la toiture-terrasse, la traversée carottée-fourreautée-bavettée, un piquage rigide par bouche à trois hauteurs, le sifflet ; puis quatre gabarits de largeur proportionnelle aux débits de caisson (120/150/165/195 m³/h — 8 + 8 + 28 + 16 = 60) | ✅ ref_030 (8 pièces) | Secteur `Logements` par le classeur (« 23009 · 60 maisons Louise Magnan · L ») ; **première fiche en contrat direct avec un bailleur, sans architecte ni groupement** : trois contrats FT2E — diagnostic moisissures 3 100 € HT (13/01/2023, accepté 16/01), mission de base MOE ventilation « 23-009 A » 9 600 € HT (15/03/2023, bon pour accord 29/03), complément DET/AOR percements-coffres-peinture « 23-009 B » 2 250 € HT (accepté 27/09/2023) = 14 950 € HT ; MOA Immobilière Atlantic Aménagement (groupe 3F, Niort) ; 60 maisons de 1972 (8 T2, 8 T3, 28 T4, 16 T6) sur 8 îlots, plans d’origine « 60 logements PRI – ZUP II Périgny » (programme bailleur « GR 0085 », à ne pas prendre pour un numéro d’affaire) ; diagnostic sur 5 maisons visitées (thermographie 15 °C à la jonction toiture/mur, sondage de toiture gorgée d’eau, calcul de condensation 2/3-1/3, débits mesurés sous l’arrêté de 1982) hiérarchisant toiture > ventilation > menuiseries > sol ; trois emplacements de caisson chiffrés (actuel 156 800 / garage 201 992 / toiture-terrasse 198 296 €, marge 1,4), toiture retenue au DCE d’octobre 2023 (CCTP/DPGF « Affaire n° : 23-009 », auteur Mathieu Braud, vérifié Géraldine Michaud ; 19 CR de chantier de Géraldine Michaud — T6) ; lot unique ventilation : caissons EC 120/150/165/195 m³/h, réseau rigide galva calorifugé 25 mm, 80-160 Pa, carottage + fourreau + résine + bitume armé + bavette, 60 sifflets, 185 m² de coffres ; chantier 29/01/2025 → 48 logements terminés le 12/06/2025, `annee_livraison: 2025` sur CR n° 19 du 26/06/2025 (OPR fixées au 03/07/2025) + classeur — PV de réception absent → B1 ; docx commerciaux « 203 095 € » non recoupés → B2 ; DPGF « 24 bouches par typologie » (96 pour 60 maisons) contre 3 bouches par maison aux plans → B3 ; décomposition des débits 165/195 → B4 ; rapport daté 24/01/2023 citant le sondage de février → B5 ; 5 maisons visitées pour 8-10 commandées → B6 ; réfection des toitures (priorité 1 du diagnostic) hors dossier → B7 ; DOE absent → B8 ; typologie `Réhabilitation`, `mission_ft2e` [Audit & diagnostic, CVC] ; aucune surface au dossier → cartouche « LA ROCHELLE · SOIXANTE MAISONS · 2025 » ; relecture éditoriale : 6 corrections appliquées (dont « VMC » remplacé, titre de section « soixante caissons sur soixante toits » ramené à ce que la pièce établit) ; questions B1-B8, C, E ouvertes |
| N08 | 23-099 — Bornes de recharge pour sept véhicules de service, La Rochelle et Saintes | `bornes-irve-la-rochelle-saintes` | ✅ rédigée, build 54 pages | ✅ `tableau-electrique`, **mécanisme `mutualisation` créé** (5ᵉ du compositeur — invariant octet des 4 planches existantes rejoué avant la greffe, après la greffe et après la retouche : 16/16 trois fois ; la passe apostrophes n’a RIEN courbé, chaînes écrites courbes et mesurées avant de composer, comme en N07) — deux registres : LE BESOIN, deux jauges graduées sur la borne de 7 kW (24 px par kW) où la puissance utile calculée sur l’usage (5,7 et 4,3 kW) est un niveau sous le bord ; LA DISTRIBUTION, une bande d’alimentation de 22 kW (4 px par kW) partagée en trois branches de 7 kW à largeur proportionnelle dont une seule est équipée (borne → quatre points de charge, lecteur de badge), les deux autres en cadres pointillés doublés de deux lignes en toutes lettres | ✅ ref_031 (9 pièces) | **DOSSIER ANNONCÉ MINCE (25 fichiers) — annotation démentie, comme Villedoux et Dufour en 2026-08** : contrat de MOE signé, note de dimensionnement au CCTP, synoptique, DPGF, OS avec montant, 5 CR jusqu’aux OPR → fiche publiée (règle Q3 examinée, non appliquée). Secteur `Monotechnique — Audit` par le classeur (« 23099 · CPAM - IRVE · M »), pas de domaine double ; typologie `Neuf` (installation créée sur sites existants → B6). **Deuxième fiche en contrat direct sans architecte ni groupement** (après Louise Magnan) : proposition ind. A du 16/11/2023 (La Rochelle seul, 3 040 € HT) → ind. B du 27/06/2024 (La Rochelle + Saintes, 4 256 € HT) → **marché de MOE CPAM n° PA 2024 – MO01** signé le 12/07 (CPAM) et le 15/07/2024 (FT2E, V. Jaoul), mission de base APD → AOR. Nature de la mission établie sur pièces : MOE d’une infrastructure IRVE — 4 véhicules de service à La Rochelle, 3 à Saintes, une borne mutualisée 7 kW monophasée par site (CCTP § 1.2 : 500 km/semaine, 20 kWh/100 km, 14 h de charge par nuit → 400 et 300 kWh, 5,7 et 4,3 kW utiles), TD IRVE alimenté en 22 kW tétrapolaire (4 × 63 A diff 500 mA S au TGBT, IG 80 A, 2 × 40 A 30 mA HI, deux emplacements libres — une borne par phase au synoptique EL01 → 12 véhicules), sans modification du raccordement. Marché de travaux PA 2024-02 notifié le 16/10/2024, **48 970,25 € HT**, 2 mois ; chantier Saintes 12/11 → La Rochelle 28-30/11, coupure générale le samedi 14/12, bornes posées les 18 et 19/12, **OPR le 20/12/2024** (CR n° 05) ; `annee_livraison: 2025` sur le classeur seul — ⚠ les OPR sont de décembre 2024, PV absent → B1 (corriger en 2024 si la réception a été prononcée avant le 1ᵉʳ janvier). Le slug et le titre n’emploient pas « CPAM » : **le marché de MOE porte une clause de confidentialité (art. 24, cinq ans) → E1**, à faire valider avant levée du noindex. Aucune trace commerciale hors classeur (docx et plaquette muets). Écarts CCTP : 7 / 7,4 kW et 22 kW / 22 kVA → B4 ; docx absents ; DOE absent → B3. Auteurs (T6) : Eric Moinet (propositions), Vincent Jaoul (CCTP/DPGF, marché, 5 CR), Tanguy Moinet (dessin EL01). Aucune surface → cartouche « LA ROCHELLE ET SAINTES · SEPT POINTS DE CHARGE · 2025 ». Répartition après N08 : L10 T9 I2 P3 C4 **M3** E2. Questions B1-B8, C, E1-E3 ouvertes |
| N09 | 23-083 — Plan de comptage de l’énergie de chauffage du site Airbus de Rochefort | `plan-comptage-energie-airbus-rochefort` | ✅ rédigée, build 55 pages | ✅ `boucle-fluide`, **mécanisme `comptage` créé** (9ᵉ du compositeur — invariant octet des 8 planches existantes rejoué avant la greffe, après la greffe et après la retouche : 32/32 trois fois ; la passe apostrophes n’a RIEN courbé) — l’archétype lu au RETOUR : la chaufferie O, un départ unique, deux collecteurs, quatre bâtiments dont trois rendent leur retour à travers un cercle (D DN 125, B trois cercles DN 50/65/40, C DN 100) et un se termine en éventail sans cercle (A), un cercle seul sur le tronc de retour (TOTAL · DN 200) — la soustraction est portée par la géométrie ; second registre : le bilan du site, quatre rangs de marques (carré plein = existant, cercle vide = à installer, 7 + 18, somme vérifiée par assertion contre l’extraction). Retouches au rendu : formule de soustraction calée à droite (elle partageait la ligne du total), vignette limitée au diamètre des compteurs uniques (trois étiquettes de 38 px ne tiennent pas en 122), boîte de l’appui élargie (« Chaufferie O » en 13/600 affleurait — sous-mesure des sans-600, N08) | ✅ ref_032 (7 pièces) | **DOSSIER ANNONCÉ MINCE (10 fichiers) — annotation démentie, QUATRIÈME fois** (Villedoux, Dufour, IRVE, Airbus) : rapport de 22 p. (18 compteurs localisés sur photographie avec leur DN, règle de pose, soustraction, priorisation), plan de comptage CVC01 en trois indices, contrat signé, bon de commande → fiche publiée (Q3 examinée, non appliquée). Secteur `Études d’exécution / BIM` par le classeur (« 23083 · Plan de comptage d’énergie - AIRBUS · E ») — contre l’intuition Monotechnique, cohérent avec le précédent École des douanes (mission vendue à l’entreprise = E) ; pas de domaine double ; typologie `Étude`. **Chaîne contractuelle : sous-traitance d’un installateur** — proposition FT2E n° 23-083 du 21/09/2023 (E. Moinet) → bon de commande Axima Concept / Equans n° 22984760 du 06/11/2023, **8 100 € HT**, convention de sous-traitance, autoliquidation TVA ; « Maître d’ouvrage : EQUANS » au rapport et au plan, site Airbus, ZI de l’Arsenal. Mission : bilan des compteurs d’énergie thermique (chauffage) existants et à installer, visite, réunion avec le service chauffage d’Airbus, rapport + plan de synthèse sur plan de masse ; nacelle exclue, eau hors contrat (feuillet manuscrit « Thermique – eau » → B4). Matière : 4 chaufferies gaz (CH, O, Vauban, V), 18 départs secondaires, **7 compteurs existants + 18 à installer = 25**, du DN 40 au DN 200 ; règle du retour et des 5D (DN 50 → 250 mm) ; bâtiment A compté par soustraction (CO-Tot DN 200) ; CCH-CH4 seul sur l’aller → B5 ; Vauban « 7 » au § 1.2.4 contre 6 au tableau → B2 ; DN « ? » des panneaux rayonnants de Liedot 2 → B3 ; priorisation en 5 rangs « sans audit » (indice c, avril 2024). `annee_livraison: 2025` sur le classeur seul — ⚠ dernière pièce = rapport indice c d’avril 2024 → B1 (corriger en 2024 sans suite en 2025). **Airbus nommé dans le titre, le slug et le récit** : la plaquette 2024 le cite parmi les clients industriels ET le corpus secteurs versé par FT2E porte déjà « Comptage Airbus, Rochefort » (cliché 08 Industriel — la couverture du rapport) ; aucune clause de confidentialité jointe à la commande → E1 à confirmer avant levée du noindex ; ni Airbus ni Equans au dessin. Lien ajouté depuis `secteurs/etudes-execution-bim.md`. Aucune trace dans les docx. Auteurs (T6) : Mathieu Braud (rapport), Eric Moinet (proposition, vérification). Aucune surface → cartouche « ROCHEFORT · QUATRE CHAUFFERIES · 2025 ». Relecture éditoriale : 7 corrections appliquées, aucune bloquante (diamètre nominal développé à la première occurrence, h2 sans abréviation, sigle GTC, « confiée par l’installateur » plutôt que « vendue »). ⚠ Le hook Stop a commité et poussé l’état intermédiaire (`6741210`, « chore(deploy) ») pendant l’attente de la relecture — les corrections sont dans `cc5bf84` : deux commits au lieu d’un, ne pas attendre un agent de fond en fin de tour sans avoir commité. Répartition après N09 : L10 T9 I2 P3 C4 M3 **E3**. **Tranche 2025 ÉPUISÉE** (23-075 déjà publié) — les ZIP suivants sont à demander. Questions B1-B9, C, E1-E4 ouvertes |
| N10 | 19-110 — Extension et rénovation du foyer occupationnel et d'hébergement du CDAIR, Saint-Martin-de-Ré | `foyer-cdair-saint-martin-de-re` | ✅ rédigée, build 56 pages | ✅ `boucle-fluide`, **mécanisme `cascade` créé** (10ᵉ du compositeur — invariant octet des 9 planches existantes rejoué avant la greffe, après la greffe et après la retouche : 36/36 trois fois ; ⚠ 49 apostrophes droites laissées dans l'extraction, courbées par `--appliquer` puis recomposition — la discipline « écrire courbe dès l'écriture » n'a pas été tenue, à reprendre en N11) — la modulation portée par la répétition du module : une réserve nourrit quatre chaudières identiques de 64 kW (256 kW), collecteur vers un ballon tampon de 2 500 L, trois branches pointillées (l'enterré) traversant chacune un cercle (le compteur) vers trois sous-stations (FOH existant par échangeur, extension, MRS) ; retouches au rendu : vignette descendue de 10 px ; ⚠ piège cairosvg nouveau — l'attribut `style` de la racine n'est pas toujours suivi d'une espace (racine de vignette `…block">`), un remplacement à espace finale le manque et la vignette rend BLANCHE : retrait par regex dans `rendre_png.py` | ✅ ref_033 (8 pièces + 2 sondes) | **Premier dossier de la tranche 2024** (ZIP livré en ouverture — `2024.zip`, 472,7 Mo, 5 dossiers, ordre par défaut : les mieux documentés d'abord ; ⚠ l'extraction `zipfile` recrée la racine interne du ZIP : le dossier vit sous `2024/2024/…`). Secteur `Tertiaire / ERP` + `secteur_secondaire: Coordination SSI` par le classeur (« 19110 · Centre d'Accueil St Martin de Ré - CDAIR · T § C ») — troisième domaine double, répartition après N10 : L10 **T10** I2 P3 **C5** M3 E3. MOA CDAIR (établissement public autonome), **SEMDAS mandataire** ; MOE groupement ARCHITEM (mandataire, Jacques Ossola) + ATLANTEC (structure) + FT2E (fluides), mission de base avec EXE et OPC (marché SEMDAS 2020/007, OS n° 2 du 20/02/2020) ; FT2E : lots 11 (élec CFO-CFa-SSI), 12 (Pb-CVC-désenfumage), 13 (cabines salles d'eau préfabriquées), coordination SSI (« 19-110-CSSI », 4 phases reçues une à une), **étude de faisabilité chaufferie biomasse + solaire thermique** (marché SEMDAS 2020/071 du 07/05/2020, 4 500 € HT, appel à projets régional Chaleur renouvelable) qui a fait basculer le projet au bois « à l'échelle globale du CDAIR » (avenant 2 : coût d'objectif 2 076 401 € HT, honoraires définitifs 211 792,90 €, part FT2E 39 456 + 5 850 SSI + av. 3 1 200), EXE CVC pour l'installateur Hervé Thermique (contrat 19-110 ind A, commande 2607472 du 25/09/2021, 3 phases) et CCTP du marché d'exploitation CPI P1-P2 (2022). Gare aux numéros de tiers : opération SEMDAS « 2507 », marchés SEMDAS « 2020/007 » et « 2020/071 », ARCHITEM « 1821 » (préfixe des  90 CR), commande Hervé Thermique « 2607472 ». Programme : FOH 56 résidents, 37 chambres (19 doubles + 18 simples) → 56 simples sur 2 niveaux ; MRS 11 chambres ; accueil de jour ; 8 zones de travaux ; ERP type J 4ᵉ catégorie ; SSI cat. A type 1 adressable étendu : 1 ZA, 8 ZC, 9 ZF dont 3 surpressions d'escalier ; chaufferie bois cascade 4 × 64 kW = 256 kW, ballon 2 500 L, 3 départs comptés (ultrasons) + GTC ; RT2012 extension SRT 814,64 m² : Bbio 67,8/79,2 (−14,4 %), Cep 140,5/142 ; SHON 1 147 m² (docx) → B5. `annee_livraison: 2024` sur le classeur seul — ⚠ réception phase 1 engagée mai 2023 (CR 90-91), docx « RÉALISATION : 2023 », phase 2 (salles de bains, désenfumage hall, espace administratif — ARCHITEM + FT2E, 15 788 € HT) notifiée 2024, DGD MOE signé 03/2025 → B1. T6 : Vincent Jaoul (CCTP 11, CCF-SSI), **Yoann Goulevant (CCTP 12 et 13 — hors équipe des sept → E2)**, Eric Moinet (vérifications, CR, répartitions). CDAIR déjà publié par FT2E (2 clichés « Chaufferie bois CDAIR » au corpus secteurs) → E1 ; ⚠ l'alt du cliché monotechnique 06 dit « deux générateurs » là où le DCE prescrit quatre chaudières → B2 (DOE absent). Relecture éditoriale en lecture seule (⚠ ses outils d'édition normaliseraient les insécables — constats appliqués par script) : 9 constats, aucun bloquant, 6 appliqués (« dédoubler », doublon « île de Ré », « à l'échelle de tout le CDAIR », « la détection s'étend », reformulation du programme, fine de « 1,25 litre »), 2 écartés motivés (forme longue de SSI — l'usage du corpus est l'acronyme nu, 1 fiche sur 23, à arbitrer globalement ; titre imagé conservé), 1 renvoyé à B1 (2023/2024). Questions B1-B7, C, E1-E3 ouvertes |
| N11 | 20-031 — Undertech, parc de bureaux et d’ateliers à La Pallice, La Rochelle | `undertech-la-pallice-la-rochelle` | ✅ rédigée, build 57 pages | ✅ `tableau-electrique`, **mécanisme `regimes` créé** (5ᵉ du compositeur — invariant octet des 5 planches existantes rejoué AVANT la greffe (15/15), APRÈS la greffe et APRÈS les trois retouches (18/18 sur 6 planches) ; ⚠ **la passe apostrophes n’a RIEN courbé** — les chaînes ont été écrites courbes dès l’extraction ET mesurées avant composition, la dette de la N10 est soldée) — le motif source → départs → point de livraison **dédoublé** en deux registres à échelles communes : le champ des ateliers (364 kWc, bandeau de 372 px) contre celui des bureaux (72 kWc, 73,6 px) au même px/kWc, et à gauche seulement la barre du point de livraison est **plus courte que la somme des départs** (250 contre 315 kVA, 70,2 px de moins) parce que l’injection est plafonnée ; seule la flèche des ateliers **franchit** la ligne pointillée de limite de propriété. Trois retouches au rendu : bandeaux de champ passés de calcaire à **aplat clair** (vides, ils se lisaient comme des cadres et non comme des mesures), libellé et détail du champ **alignés sur la colonne des mesures** (à gauche du registre, le texte s’intercalait entre deux groupes de barres et la lecture zigzaguait), limite de propriété **descendue de 10 px** (elle collait au bloc de livraison) | ✅ ref_034 (8 pièces) | Secteur `Tertiaire / ERP` par le classeur (« 20031 · Projet tertiaire La Pallice UNDERTECH · T »), **domaine simple** — répartition après N11 : L10 **T11** I2 P3 C5 M3 E3 pour 34 fiches (37 pondéré). MOA **Mediatim Promotion** (société de projet MP Montcalm), architecte **SMART Architecture** — le même couple que la résidence Aurora (19-036) ; groupement ATLANTEC (structure) + SIT&A Conseil (VRD) + FT2E (fluides) + OTEEC (économiste, MOE d’exécution sans plans, OPC) + APAVE (contrôle et SPS) + ACOUSTEX. Contrat FT2E : **proposition d’honoraires indice D du 14/10/2021, signée le 21/10/2021** — six indices au dossier (nu, A, B, C, D, E) ; mission FAE + RT2012 Bbio + AVP + PRO/DCE + ACT + VISA sur cinq lots (CVC-rafraîchissement, plomberie, électricité, photovoltaïque, désenfumage), **33 100 € HT** ; base d’estimation 550/590 k€ le lot fluides et **810 k€ le photovoltaïque**. **La thèse : deux champs photovoltaïques dans le même DCE, deux régimes contractuels opposés** — ateliers 1 104 modules de 330 Wc (364 kWc) en **revente totale** par logette C4 et disjoncteur 400 A, injection plafonnée à 250 kVA pour 315 kVA d’onduleurs en cinq groupes (80-80-60-55-40) ; bureaux 240 modules de 300 Wc (72 kWc) en **autoconsommation** sur le TGBT des services généraux, trois onduleurs de 25 kVA. Second fait marquant, non dessiné : **l’ingénierie de l’attente** — bâtiments livrés bruts, 75 W/m² et une platine de comptage par plateau, trois colonnes de 200 A (123/90/96 kVA) plus 160 kVA de services généraux et IRVE = **469 kVA utiles**, 44 kVA réservés à la recharge, une seule borne équipée ; une PAC Daikin R32 unique pour les trois immeubles (COP 3,45, EER 3,06) avec un compteur d’énergie par bâtiment ; et le calcul réglementaire **arrêté au Bbio** (article 51 — Cep à la charge des acquéreurs), A 67,2/70 et B 59,1/70, le bâtiment C non calculé (→ B6). `annee_livraison: 2024` **bien étayé** : CR OPC n° 66 du 06/02/2024 en tête « RÉCEPTION DES TRAVAUX, ensemble des entreprises convoqué » pour le 13/02/2024, OPR des ateliers le 19/12/2023 (CR 61), levées de réserves et GPA ensuite (CR 68 à 76), classeur et docx concordants — PV absent → B1. ⚠ **Contradiction de millésime d’ouverture (B4)** : la proposition initiale porte « N° 20 031 » ET la date du **26 mai 2019** ; l’indice A est de juillet 2020 et le schéma impose `annee: 2020`. ⚠ **Trois comptes de locaux** — 18 (CCTP de décembre 2021), 22 (les 104 CR de 2022-2024), « 13 ateliers et 3 immeubles » (docx) → **B2, aucun compte publié en prose**. ⚠ **Le CCTP B10 se contredit en interne** (§ 2.2 « ateliers 1-2-3-4-5-6-7-11-12-13-14-15 » contre § 3.3 blocs B = 5-6-7-13-14-15 et C = 8-9-10-16-17, et une 3ᵉ colonne de DPGF non dimensionnée) → B3 ; le dessin suit le § 3.3, seul endroit qui dénombre. E1 : **UNDERTECH est déjà publié par FT2E** (plaquette 2024 « Undertech — bureaux, CFO/CFA + photovoltaïque » + docx sectoriel avec MOA, architecte et montant) — précédent Airbus/CDAIR appliqué, à confirmer avant levée du noindex ; aucune clause de confidentialité au contrat. T6 : **Eric Moinet** (les six propositions), **« GM »** rédacteur de la synthèse RT — mêmes initiales non identifiées qu’en N06. Aucun cliché exploitable (esquisse urbaine et fonds de plan = œuvres de tiers). Questions B1-B10, C1-C3, E1-E3 ouvertes. **Relecture éditoriale en lecture seule** (ses outils d’édition normaliseraient les insécables — constats appliqués par réécriture scriptée) : 31 constats, **6 bloquants dont 5 appliqués** — la synthèse disait « tous livrés bruts » quand le récit dit les parties communes livrées équipées ; « auxquelles s’ajoutent » portait sur des kVA (masculins) ; « coefficient de consommation » n’est pas le terme RT2012 (le Cep est une **consommation**, graphie d’Aurora) ; « les deux immeubles calculés » arrivait après « trois immeubles » sans que le passage soit dit ; et `performance` attribuait 59,1 au « plus grand bâtiment » quand le récit l’attribuait au « second ». **Le 6ᵉ bloquant n’a PAS été appliqué en l’état** : l’agent proposait d’expliquer le calcul sur deux bâtiments par leur mitoyenneté thermique — hypothèse qu’aucune pièce n’établit, et qu’il signalait lui-même comme invérifiée ; la fiche **dit le fait sans en inventer la cause** (B6). 20 constats de confort appliqués ; 2 écartés motivés (8 paragraphes contre les 3-6 du gabarit — chacun porte un sujet distinct, et l’agent conclut lui-même qu’« aucun paragraphe ne mérite d’être coupé pour lui-même » ; « à la découpe » gardé). ⚠ **Une correction d’accord induite a échappé à l’agent** : le COD devenant féminin, « laissés ouverts » devient « laissées ouvertes » — corriger un terme en entraîne d’autres, à relire soi-même après application |
| N12 | 21-093 — Central Hostel, une auberge de jeunesse dans un immeuble du XVIIᵉ, 16 rue de l’Escale, La Rochelle | `auberge-central-hostel-la-rochelle` | ✅ rédigée, build 58 pages | ✅ `zonage-ssi`, **mécanisme `convergence` créé** (5ᵉ du compositeur — invariant octet rejoué AVANT la greffe (16/16 sur les 4 planches zonage-ssi), APRÈS la greffe et APRÈS les quatre retouches ; la dernière passe a été élargie à **tout le corpus, 140/140 pièces sur 35 planches** et 6 compositeurs, l’instrument étant devenu générique. ⚠ **La passe apostrophes n’a RIEN courbé** sur le dossier de la planche — chaînes écrites courbes dès l’extraction, avec assertion `"'" not in sortie` dans le script d’extraction) — la détection est fine, la mise en sécurité ne connaît qu’une échelle : seize marques de zone comptées sur six niveaux (11 pleines pour les ZDA, 5 évidées pour les ZDM, la colonne évidée continue sauf aux combles) convergent par un tronc UNIQUE vers deux blocs aux hauteurs proportionnelles à 16 et 10 (126 px / 78 px), et deux fonctions de sécurité — exutoires d’escalier, clapets coupe-feu — sont dessinées dans le même registre en filet interrompu, **sans qu’aucun tronc ne les atteigne**. Quatre retouches au rendu : la colonne des marques évidées réservée en dernier emplacement (la marque PLEINE des combles s’y logeait et effaçait la distinction), le tronc des départs prolongé jusqu’à l’ordonnée de la centrale (la pile de droite est plus courte que celle des niveaux : le segment sortant de la boîte pendait 18 px sous la fourche), un `libelle_court` pour l’appui (« Rez-de-chaussée » chevauchait les marques) et la boîte de centrale de l’appui élargie de 130 à 156 px | ✅ ref_035 (9 pièces) | **Domaine DOUBLE au classeur** : « 21093 · Réhabilitation rue de l’Escale - Central Hostel · T § C » → `secteur: Tertiaire / ERP` + `secteur_secondaire: Coordination SSI` ; répartition portée à **L10 T12 I2 P3 C6 M3 E3** pour 35 fiches, 39 en pondéré. `annee_livraison: 2024` sur quatre étais concordants — deux docx commerciaux « RÉALISATION : 2024 », classeur « Finalisées en 2024 », CR de chantier n° 26 du 09/04/2024 (« Pour rappel la réception est prévu le 16 avril », planning S15 réception / S17 commission de sécurité / S18 ouverture) et factures d’AOR et de réception SSI du 27/06/2024 — mais **PV de réception absent** → B1. Deux missions contractées à part : maîtrise d’œuvre fluides et électricité (indice A du 20/10/2021, 23 500 € HT) et coordination SSI (21-093-CSSI du 22/11/2021, signée « lu et approuve » le 23/11/2021, 3 200 € HT) ; 26 700 € HT facturés en quatorze factures. Auteurs relevés (T6) : Mathieu Braud (CCTP lot 07), Vincent Jaoul (CCTP lot 08, cahier des charges SSI, coordinateur SSI), Tanguy Moinet (zonage), Eric Moinet (vérificateur, gérant). Questions B1-B7, C1-C2, E1-E4 ouvertes ; ⚠ la plaquette 2024 date l’affaire de 2022 (année des études) et réduit la mission au CFO/CFA → B6. **Deux instruments versés au dépôt avec la fiche** : `scripts/planches/invariant.py` (l’invariant octet, générique, que chaque session réécrivait) et `scripts/planches/rendre_png.py` (les rendus de contrôle, perdu en N11). ⚠ **Le hook Stop a committé et poussé le livrable en cours de session** (`ca747c8`, « chore(deploy) ») avant la passe éditoriale : celle-ci a suivi en `2159bdf`, sous l’intitulé content(references) qui dit ce qui s’est passé. L’historique poussé n’a pas été réécrit, le dépôt étant partagé — piège reporté au prompt N13 |
| N13 | 21-095 — Bâtiment d’assemblage d’avions VoltAero, aéroport de Rochefort – Saint-Agnant | `batiment-voltaero-saint-agnant` | ✅ rédigée, build 59 pages | ✅ `coupe-traversee`, **mécanisme `frontiere` créé** (6ᵉ du compositeur — invariant octet rejoué AVANT la greffe (140/140), APRÈS la greffe (24/24 sur coupe-traversee) et APRÈS les deux retouches de rendu (144/144)) : un mur plein, quatre familles de services, deux qui n’ont pas de côté droit — au rang du 220 V les piquages descendent du plafond à gauche et montent de la plinthe à droite | ✅ ref_036 (9 pièces + 2 sondes) | ⚠ **LE DOSSIER D’ARCHIVES EST AMPUTÉ** : son sous-répertoire `02-Production/05-Pro/` porte les CCTP, DPGF, estimations et dix plans de l’affaire **21-093** (auberge de jeunesse rue de l’Escale, publiée en N12) — 17 fichiers sur 72, soit 24 %. **Aucune pièce technique signée FT2E de 21-095 n’existe au dossier** : ni CCTP, ni DPGF, ni estimation, ni plan, ni synthèse thermique. La fiche est bâtie sur trois familles de sources, toutes nommées en collecte : le cahier des charges de l’utilisateur (version 4, 20/10/2021 — les régimes de desserte), 39 comptes rendus de chantier de SD Architectes (les machines, le poste de transformation, le photovoltaïque, la réception), et trois CV FT2E (le calcul RT2012 Cep −40 %, l’air comprimé et les RIA au périmètre de Mathieu Braud). `reference` relevé sur le **classeur FT2E** et le nom du répertoire d’archives, faute de page de garde → **B2**. `surface_m2` VIDE (aucune surface bâtie au dossier ni au fonds commercial) : le cartouche porte « huit postes d’assemblage » → **B5**. Secteur `Industriel` par le classeur (« 21095 · Bâtiment industriel Voltaero St Agnant · I »), domaine SIMPLE. `annee_livraison: 2024` sur trois étais concordants (classeur ; CR n° 47 du 28/08/2024 : « RECEPTION le 02/09/2024 à 11h sur site » ; CR n° 45 et 46 qui l’annonçaient au 26 juillet) — PV de réception absent → **B6**. Dix questions B, deux C, une D, trois E ouvertes. Auteurs relevés (T6) : aucun, faute de pièce FT2E — seul Eric Moinet est nommé, comme interlocuteur de chantier |
| N14 | 23-036 — Extension du bâtiment industriel 5-8 de Fountaine Pajot, Aigrefeuille-d’Aunis | `extension-fountaine-pajot-aigrefeuille` | ✅ rédigée, build 60 pages | ✅ `tableau-electrique`, **mécanisme `greffe` créé** (7ᵉ du compositeur — invariant octet rejoué AVANT la greffe (144/144), APRÈS la greffe et APRÈS les deux retouches de rendu (148/148)) : le mécanisme porte sur ce qui PRÉCÈDE l’arrivée — une jauge où 500 kVA se lisent dans 800, une limite verticale dont le seul côté gauche porte la source ET l’armoire générale, deux franchissements d’épaisseurs proportionnelles aux calibres (630 et 250 A, rapport dessiné 2,52) dont un seul ouvre un peigne de quatre départs, et une branche barrée vers l’armoire de l’atelier démoli | ✅ ref_037 (9 pièces + 2 sondes) | **Dossier riche et INTÈGRE** — contrôle de page de garde sur chaque pièce technique (piège N13) : les trois pièces FT2E et les cinq cartouches de plans portent toutes « Affaire n° : 23-036 », aucune pièce étrangère. Chaîne complète pour la première fois de la tranche : programme d’esquisse, deux CCTP (65 et 34 p.), deux DPGF, deux estimations, huit plans, une note d’étude FT2E, la répartition d’honoraires et 41 comptes rendus de chantier. ⚠ **UNE THÈSE A DÛ ÊTRE ÉCARTÉE PARCE QU’ELLE EST DÉJÀ PUBLIÉE** : la note FT2E sur la récupération d’énergie (CARSAT, tout air neuf, batteries à eau, boucle glycolée) est mot pour mot le dispositif de la planche de `atelier-dufour-yachts-perigny` — même prescription, même boucle, même chantier naval ; elle nourrit le récit, pas le dessin. Deux autres thèses écartées pour voisinage : les deux régimes d’air des nefs jumelles (trop proche de `siege-rese-aigrefeuille` et de `logements-pas-des-boeufs`, sur un `boucle-fluide` déjà à 10/36) et les périmètres dissymétriques du SSI (`zonage-ssi`/`convergence` deux sessions plus tôt). Secteur `Industriel` par le classeur (« 23036 · Extension Bat 5-8 Fountaine Pajot · I », domaine SIMPLE) — ⚠ contradiction apparente avec le CV de Vincent Jaoul qui annonce « CFO / CFA / **SSI** » : lecture retenue, le « C » du classeur désigne une mission de COORDINATION SSI, contrat distinct, quand ici le SSI de catégorie A est conçu DANS le lot 10 (chapitre 3.16, plan `10-SSI`) → B2. `annee_livraison: 2024` sur trois étais (classeur ; objectif de réception au 18/10/2024 porté au calendrier des 41 CR ; lots FT2E à 90 % au 23/10/2024) — **PV de réception absent, et l’indice N12 des honoraires d’AOR ne joue pas ici : FT2E ne porte pas l’AOR à la répartition** → B1. `surface_m2: 2412` (programme d’esquisse) contre 2 432,68 aux plans (1 058,15 + 1 374,53) et 1 931,84 au plan SSI → B4. ⚠ **Les bilans de puissance de la note de récupération ne se ferment pas** (152 + 177 = 329 et 152 + 118 + 75 = 345 pour 350 kW annoncés) : aucun schéma proportionnel n’a été composé sur ces valeurs → B3. Sept questions B, trois C, quatre D, quatre E ouvertes. Auteurs relevés (T6) : Vincent Jaoul (lot 10), Mathieu Braud (lot 11 et note d’énergie), Eric Moinet (vérificateur des trois pièces, interlocuteur des 41 réunions). Lien posé depuis `/secteurs/industriel-commercial`, qui nommait déjà l’opération sans la lier. Répartition après N14 : L10 T12 **I4** P3 C6 M3 E3 = 41 pondéré pour 37 fiches, mesurée sur le déploiement. **Passe éditoriale** (commit `c6f4ee5`) : 37 corrections, dont une ERREUR DE FAIT — la fiche annonçait Fountaine Pajot comme la deuxième opération du Fief Girard « après la RESE », alors que la RESE est 24-003 (diagnostic juin 2024, OPR juillet 2026) et que ce chantier-ci ouvre en décembre 2023 — et deux sur-affirmations retirées (un bilan de charge du poste qu’aucune pièce n’établit ; « la mission de base complète, de l’esquisse au DOE », qui décrivait la mission de l’ÉQUIPE). ⚠ **Trois des propositions de la relecture étaient FAUSSES au regard des pièces** et ont été écartées : attribuer à FT2E les démarches Enedis (le CCTP les met à la charge de l’entreprise titulaire du lot), supprimer « quelque » devant 2 412 m² (le programme écrit « environ 2412 m² »), et supprimer le lien hauteur → stabilité au feu, que le programme affirme lui-même. Vérifier chaque constat contre la source avant de l’appliquer |
| N15 | 20-045 — Les Cabanes Urbaines, restructuration et extension d’un établissement sportif et culturel, 22 rue Cardinal, La Rochelle | `cabanes-urbaines-la-rochelle` | ✅ rédigée, build 61 pages | ✅ `zonage-ssi`, **mécanisme `compensation` créé** (6ᵉ du compositeur — invariant octet rejoué AVANT la greffe (148/148), APRÈS la greffe et APRÈS les quatre retouches de rendu (152/152 sur six compositeurs)) : la thèse est une SUBSTITUTION, pas un découpage — les planchers n’ayant pas été traités coupe-feu, le bâtiment ne forme qu’un seul compartiment, et la détection généralisée prend la place du recoupement. Deux traits interrompus de 2 px disent le plan qui manque, quatorze marques de zone disent ce qui le remplace, UNE accolade referme l’empilement sur l’équation que portent les trois plans de zonage de FT2E — « ZA01 = ZC01 = le bâtiment » — et la bande basse porte la vérification par deux foyers de contrôle d’efficacité réellement allumés (2 min 30 s sur mousse, 11 min 20 s sur bûchettes ; barres à échelle commune, rapport dessiné 4,53 = rapport mesuré). ⚠ **L’assertion de dépassement a servi dès le premier jet** : deux débordements de colonne arrêtés avant tout rendu ; 36 chaînes mesurées, 0 dépassement, marge la plus faible 14,8 px. **Quatre retouches lues sur les PNG** : fond du libellé du plan manquant élargi de 8 % (le mono sous-mesure, le dernier tiret mordait sur la lettre) ; trait d’allumage remplacé par UNE ligne de zéro traversant les deux rangées (posé à l’origine de chaque barre, il disparaissait sous elle) ; appui aéré de 123 à 51 px de marge basse avec une ligne mono par bloc ; libellé de plancher passé SOUS le trait à l’appui, où un fond de 150 px masquait le trait presque entier. | `references/ref_038/` — 8 pièces, décision Q3 (dossier RICHE : dossier d’identité SSI complet de A à R, du concept au PV de réception signé), page de garde contrôlée sur 10 familles de pièces, dossier INTÈGRE | **Domaine double T § C** (« 20045 · THE ROOF · T § C ») — cinquième du catalogue. **`annee` 2020, `annee_livraison` 2023** : réception du chantier au 01/09/2023 (CR n° 39 et n° 40), mise en service constructeur au 01/09/2023, PV de réception du SSI au 08/09/2023, commission de sécurité au 11/09/2023. **Trois noms pour une affaire** : « THE ROOF » au classeur, « Cabanes Urbaines » au répertoire d’archives et à toutes les pièces de 2022-2023, « The Roof — Maison de l’escalade » aux contrats de 2020 — la fiche retient **Les Cabanes Urbaines**, le nom que le site publie déjà deux fois (question B2). **Trois graphies pour la maîtrise d’ouvrage** dans des pièces FT2E : ESCAL’BLOC (contrats, CR), ESCLA’BLOC (proposition CSSI), ESCALBLOC (synthèse RT) — ESCAL’BLOC retenu (question B3). ⚠ **Le comptage boucle, à la différence de la N14** : 85 détecteurs optiques + 2 thermovélocimétriques + 16 déclencheurs manuels = 103, exactement le compte du bilan de puissance — c’est ce qui autorise ici une géométrie proportionnelle. ⚠ **Erreur de comptage rattrapée en cours de session** : « treize zones » écrit d’après une lecture rapide du tableau de corrélation, recompté ligne à ligne à **quatorze** (11 ZDA + 3 ZDM), corrigé au frontmatter, au récit et à la collecte avant commit. **E1 remplie cinq fois** : le site publie déjà le nom sur `/secteurs/coordination-ssi` et `/secteurs/tertiaire-erp`, **et une photographie du FCE de cette affaire est au corpus secteurs** (`coordination-ssi/02.jpeg`, « Essai au feu réel dans une salle d’escalade ») ; plaquette et CV de Vincent Jaoul la nomment aussi. Les deux mentions ont reçu leur lien interne, et **le millésime de l’essai de foyer est passé de 2022 à 2023 sur `/secteurs/coordination-ssi`** — les deux FCE sont datés du 07/09/2023 au PV (question B1, à valider). **Sept questions B** ouvertes (millésime et correction de page publiée, nom de l’établissement, graphie de la MOA, surface de l’ouvrage complet, captation des poussières d’escalade disparue entre l’avant-projet et le DCE, marge de Bbio à 0,09 %, levée de la réserve de désenfumage). Recette : typecheck 0, build 61 pages, liens 38/38 à 5, 0 fuite de numéro, relevé numéral sans écart nouveau (deux composés en lettres corrigés — « vingt-trois heures » → « 23 h », « dix-huit chapitres » → « 18 chapitres »), déploiement contrôlé aux trois bandes, vignette servie à **274 px** (taille de conception exacte), fiche présente aux DEUX filtres et sur `/secteurs/coordination-ssi`. **Passe éditoriale (commit distinct) : 26 corrections, dont UNE ERREUR DE FAIT que la relecture a fait remonter et que le CCTP a tranchée.** La fiche annonçait « quatre centrales de traitement d’air double flux » puis en énumérait trois plus une extraction de cuisine ; l’agent n’a pas su que c’était faux — il a seulement remarqué que **le compte ne tombait pas juste**. Le § 4 du lot 10 rouvert donne trois centrales double flux (existant 1 300 m³/h, salle de spectacle 1 800, extension 2 455), la cuisine relevant d’une hotte de 2 500 m³/h et de sa propre centrale de compensation — **et les trois débits publiés étaient posés sur les mauvais organes** (1 800 à l’existant, 2 455 à la salle, 1 300 à l’extension). C’est nommément la faute que la règle dure 1 du protocole désigne comme la plus grave. Rien n’était monté sur la planche, dont la thèse est la sécurité incendie : seul le récit était atteint. Autres constats appliqués : « les deux bâtiments » sans antécédent, qui contredisait « sous un même toit » ; « cinq réglementations » pour un type X et quatre types d’activité ; marge du Bbio dite en dixième de point et marge du Cep au chiffre du dossier (37,76 %) ; « seize déclencheurs » en lettres et « 6 mètres » en chiffres ; kWhep/m²/an et LED aux graphies du corpus ; SSI apparié à sa forme longue ; trois figures de style et un intensif retirés ; deux phrases de 62 mots coupées. **`mission_ft2e` reçoit `Thermique`**, que la fiche expose sur un paragraphe entier et qui manquait. Invariant des planches inchangé (152/152). |
| N16 | 21-086 — Audit de chauffage sur sept sites médico-sociaux de l’ADEI, Charente-Maritime | `audit-chauffage-sites-adei` | ✅ rédigée, build 62 pages, synthèse 669 signes, 7 liens internes | ✅ `boucle-fluide`, **mécanisme `regime` créé** (11ᵉ du compositeur — invariant octet 152/152 avant greffe, 156/156 après ; garde-fou automatisé sur 4 fonctions, 17 constantes `RG_` et 12 helpers réutilisés) — premier mécanisme de l’archétype à poser une CONDITION D’ADMISSION plutôt qu’un trajet : deux régimes d’eau (65 °C haute température, 35 °C standard) contre trois familles d’émetteurs posées à la hauteur de ce qu’elles exigent ; trois traits portent seuls la démonstration — un qui s’arrête 72 px avant l’aérotherme, un qui traverse une boîte intercalée avant le radiateur, un qui atteint le plancher chauffant | ✅ ref_039 (7 pièces) | **Une affaire, HUIT contrats indicés A à H, SEPT sites** : les cinq rapports de production portent tous « Affaire N ° 21-086 » sans indice et le classeur ne connaît qu’une entrée — l’indice découpe la commande, pas l’affaire (même motif qu’en N15 sur 20-045). Secteur `Monotechnique — Audit` par le classeur (« 21086 · Audit chauffage sites ADEI · M », domaine SIMPLE) ; typologie `Étude`. `annee_livraison: 2023` par le classeur, MAIS le contrat d’AMO `21 086 H` est du 20/02/2024 et le dossier de subvention porte des pièces de 2024 → **B1**. `moa` = SCI Immobilière du Port, signataire des huit contrats « pour le compte de l’ADEI », alors que trois des cinq rapports nomment l’ADEI en page de garde → **B2**. `lieu` = Saint-Savinien (17350), le plus étendu des sept sites (5 430 m² sur 9 131) → **B3**. `surface_m2: 9131` ne couvre que les CINQ sites documentés, Les Boucholeurs et Saint-Genis-de-Saintonge n’ayant aucun rapport au dossier → **B4**, **B6**. ⚠ **CINQ ruptures de bouclage** relevées dans les rapports (économie annoncée à deux valeurs, temps de retour permutés entre détail et synthèse, consommation de l’état existant recopiée dans quatre fiches de préconisation, deux bilans qui ne se ferment pas) → **B5** ; les temps de retour et les gains ont donc été EXCLUS de la planche, seul le tableau de Saintes bouclant intégralement sur ses sept lignes. **E1** ADEI repris — nom déjà publié dans quatre docx sectoriels sous « ADEI 17 », pour DEUX AUTRES affaires (foyer de vie de Loulay, SSI 2023 ; IME de Saint-Genis-de-Saintonge, 2020) : ne pas les confondre. Passe éditoriale : 18 corrections, dont deux contradictions internes vues par l’agent sans les pièces (« tous chauffés au fioul » contre l’ESAT géothermique ; le plancher chauffant à la fois jamais déposé et emporté par la détente directe) et une erreur de fait confirmée sur pièce (Saint-Germain-de-Lusignan : DEUX chaufferies au gaz propane, non trois au fioul et au propane — le rapport se contredit, on retient le paragraphe qui dénombre, règle N11) ; **quatre constats REJETÉS après contrôle** (les trois chaufferies de Saint-Savinien sont attestées mot pour mot, la chronologie « deux ans » est exacte, l’IME de Saintes est nommé p. 3, la puissance électrique appelée figure dans deux rapports). ⚠ **Leçon neuve : l’assertion de dépassement doit couvrir l’APPUI et la VIGNETTE, pas seulement la planche** — « Pompe à chaleur » a mordu sur son bloc dans l’appui et a passé le build, le bloc `controles`, l’invariant ET le PNG de contrôle à 552 px ; le défaut ne s’est vu qu’à la capture du déploiement à 768 px. ⚠ Leçon de dessin : **un trait qui s’arrête ne dit quelque chose que s’il allait quelque part** — la première version montait et s’interrompait dans le vide à 250 px de sa cible ; sur la vignette, qui n’a pas de légende, la boîte cible flottait sans relation. Recette sur le déploiement : 39 cartes sur /references, vignette servie à 274 px (taille de conception exacte), fiche rendue aux trois bandes, répartition L10 T13 I4 P3 C7 **M4** E3 = 44 en pondéré |
| N17 | 21-074 — Extension de l’atelier d’assemblage et bâtiment vestiaires d’AP Yacht Conception (groupe Catana), Marans | `ap-yacht-marans` | ✅ rédigée, build 63 pages, synthèse 652 signes, 8 liens internes | ✅ `sankey-energie`, **mécanisme `serrage` créé** (7ᵉ du compositeur — invariant octet 156/156 AVANT la greffe, 160/160 APRÈS la greffe puis APRÈS la refonte de la barre et l’ajout du contrôle des marques ; garde-fou de greffe automatisé sur 9 fonctions, 31 constantes `SG_` et 10 helpers réutilisés ; assertion de dépassement posée sur LES TROIS formats — 18, 3 et 9 chaînes mesurées, 0 dépassement). Deux zones de calcul RT2012 sous un même permis, et ce n’est pas la même exigence qui serre : Bbio à 0,28 % près côté vestiaires, Tic exactement au plafond côté hall. Le Tic est porté dans un SECOND registre avec son unité propre, parce que la synthèse laisse la colonne « Gain en % » VIDE sur cette ligne — le normaliser aurait affirmé une proportion que la pièce refuse de calculer. **Trois thèses voisines vérifiées et écartées** : `commande` du siège RESE (« trois régimes d’air, chacun commandé par ce qui l’exige » — c’était la première thèse envisagée), `greffe` de Fountaine Pajot (l’extension sans source neuve, qu’AP Yacht refait à l’identique : 478 kVA pris sur un TGBT de 1 000), `plafonds` de Maubec (un seul indicateur dont le plafond s’effondre). | ✅ `references/ref_040/` — 10 pièces, décision Q3 en tête, 9 questions B, 3 questions C, 2 questions D, 3 questions E | Dossier **intègre** (contrôle N13 rejoué sur 11 pièces). ⚠ **Trois faux numéros d’affaire** relevés et écartés, dont `ULTI+ 21-095` — une désignation de modèle de constructeur qui a la graphie d’un numéro FT2E **réel et publié** (VoltAero, N13). ⚠ **45 est un compte de FICHIERS, 47 un compte de RÉUNIONS** : les CR sont numérotés 1 à 47, les n° 36 et 37 manquent à l’archive ; le premier jet publiait 45. Indexation contrôlée sur le déploiement : Industriel passe de 4 à 5 fiches, AP Yacht répond au filtre ; à 21-074 elle sort du top 4 de `/secteurs/industriel-commercial` (23-079, 23-036, 22-006, 21-095), ce qui est le tri documenté et non un défaut. |
| N18 | 20-071 — Construction du siège social et des ateliers de l’agence Poitou-Charentes d’Eiffage Énergie Systèmes, Saint-Jean-d’Angély | `siege-eiffage-saint-jean-d-angely` | ✅ rédigée, build 64 pages, synthèse 709 signes, 6 liens internes | ✅ `boucle-fluide`, **mécanisme `report` créé** (12ᵉ du compositeur — invariant octet 160/160 AVANT la greffe, 164/164 APRÈS la greffe puis APRÈS les trois retouches) : la pompe à chaleur est à récupération d’énergie et **à deux tubes**, donc la chaleur ôtée d’un bureau ne remonte pas à l’unité extérieure — elle fait demi-tour DANS le boîtier et redescend vers un bureau qui la demande ; le local serveur, sorti du système, est la contre-épreuve dessinée. Trois grandeurs DÉRIVÉES partagées par les trois formats (hauteur du boîtier = f(départs), terminaux au premier et au dernier départ, demi-tour à 30 % de la largeur) | ✅ ref_041 (9 pièces) | `annee_livraison: 2023` (classeur « Finalisées en 2023 » + docx commercial « RÉALISATION : 2023 » + CR n° 49 du 20/01/2023 convoquant les réceptions des 26 et 27 janvier 2023 ; aucun PV au dossier → B2). Secteur `Tertiaire / ERP` par le classeur (`20071 · Bureaux EIFFAGE · T`, domaine SIMPLE) — filtre recetté sur le déploiement : T passe de 13 à 14 cartes. ⚠ **FAUX NUMÉRO DANS UNE PIÈCE FT2E** : le CCTP du lot 09 porte « Affaire n° : 20-012 » en page de garde, seul document du dossier à le faire (sa DPGF, ses quatre plans, le CCTP du lot 08, la synthèse RT et le calcul d’honoraires portent 20-071) → B1. ⚠ **SINGULARITÉ DE L’AFFAIRE** : le maître d’ouvrage est aussi l’entreprise des lots 08 et 09, annoncé dès le courriel de consultation du 21/09/2020 et confirmé au panneau de chantier. ⚠ **TROIS VALEURS ÉCARTÉES** parce que les pièces ne les soutiennent pas : régime de neutre (TN au § 3.3.1, TT aux § 3.4.2 et 3.5.2 → B9), puissance photovoltaïque (« 160 kVA : 60 pour l’ombrière et 60 pour le bâtiment B », qui ne boucle pas → B10), température intérieure conventionnelle (ligne Tic vide aux trois colonnes → B8). ⚠ **COMPTE DE RÉUNIONS NON PUBLIÉ** : 46 comptes rendus au dossier, numérotés 1 à 45 puis **49**, le n° 45 du 13/01 et le n° 49 du 20/01 étant distants d’une seule semaine → B6. Questions B1-B10, C1-C2, E1-E3 ouvertes ; auteurs relevés (T6) : Mathieu Braud (CCTP lot 08), Vincent Jaoul (CCTP et DPGF lot 09), Éric Moinet (vérificateur des deux CCTP, signataire du groupement), GM et EM aux plans et à la synthèse RT |
| N19 | 21-029 — Remplacement de la chaufferie fioul de l’école maternelle du groupe scolaire, La Flotte-en-Ré | `chaufferie-ecole-la-flotte-en-re` | ✅ rédigée, build 65 pages, synthèse 630 signes, 9 liens internes | ✅ `coupe-traversee`, **mécanisme `amorce` créé** (7ᵉ du compositeur — invariant octet 164/168 AVANT la greffe, 168/168 après, et de nouveau après les quatre retouches de géométrie) — une **épine construite entière** et n postes dont les `poses` premiers seuls sont pleins ; pas et centres **DÉRIVÉS de n** par une primitive unique, `_am_centres`, appelée par les trois rangs ET les trois formats, de sorte qu’aucune abscisse de poste n’est écrite à la main ; la partition se répète **2/4 · 2/4 · 1/3** et porte seule la démonstration, tout texte masqué. Le regard de vannes est dessiné **plein** (il est construit), seul ce qui le dépasse est interrompu — c’est l’amorce | ✅ ref_042 (10 pièces + les 2 sondes recalées) | ⚠ **Le CCTP porte un FAUX numéro en page de garde** (« Affaire n° : 21-031 ») contre **19 occurrences de 21-029** sur sept pièces FT2E — cartouches des deux plans, cinq contrats et classeur d’honoraires interne ; c’est la variante N18 (Eiffage, lot 09) rejouée, et le CCTP est **la seule pièce fausse du dossier**, ses propres en-têtes de pages courantes comprises. `annee_livraison: 2023` (classeur « Finalisées en 2023 » ; le CR n° 9 du 17/10/2023 constate « travaux terminés » et trois réserves **sans prononcer la réception**, les six emplacements du protocole visités en vain → B1). Secteur `Monotechnique — Audit` par le classeur (« 21029 · Ecole primaire et maternelle La Flotte · M ») **contre l’intuition** (une école est un ERP de type R) — et le dépouillement donne raison au classeur : FT2E n’y a tenu qu’**un seul lot technique**, le chauffage, décliné en **cinq missions sur trois ans** sous cinq indices de contrat (4ᵉ confirmation de la règle « un indice n’est pas une affaire », et deux d’entre eux portent le même indice C → B4). **DEUX pièces du dossier n’appartiennent pas à FT2E**, cas nouveau : un **devis concurrent** d’un autre bureau d’études déposé pour comparaison (son nom de fichier le faisait passer pour une étude FT2E), et une **étude d’impact sonore commandée ET payée par l’installateur** en juillet 2024, un an après les travaux — rien n’en est publié, tout est en E1, qui est la question délicate du dossier. `surface_m2` **VIDE** : aucune surface au dossier ni dans les onze docx sectoriels, muets sur cette affaire (B6). **Aucun architecte** sur l’opération (cartouche « XX »). ⚠ **Le site publiait déjà cette affaire** (3ᵉ occurrence après N15 et N17) : un cliché de `/secteurs/monotechnique` légendé « PAC, groupe scolaire de La Flotte » dont l’alt décrit l’écran acoustique de E1, **et une mention en prose sans lien** faute de fiche — **devenue lien avec cette session** (`src/content/secteurs/monotechnique.md`, à signaler). C’est aussi le site qui a fixé la graphie retenue, « La Flotte-en-Ré », contre trois formes au dossier (B2). Trois thèses voisines **écartées** avant composition : le régime d’eau qui commande les émetteurs (publié par l’audit ADEI), la cascade sur ballon à départs comptés (foyer de Saint-Martin-de-Ré), et l’amont réservé pour plus (bornes IRVE, en `tableau-electrique` — d’où le choix de `coupe-traversee`). Recette : filtre M passé de 4 à **5 fiches**, répartition L10 T14 I5 P3 C7 M5 E3 (42 fiches, 47 en pondéré) ; la fiche **n’entre pas** dans le top 4 de `/secteurs/monotechnique` (21-029 est le plus ancien des cinq) — tri documenté, pas un défaut ; vignette servie à **274 px**, sa taille de conception exacte ; les trois bandes contrôlées au déploiement. Relecture éditoriale : **14 corrections appliquées**, dont trois **contradictions avec des fiches publiées** que la rédaction avait laissé passer (ADEI « sept réponses » alors que sa fiche en publie trois ; Villedoux donné en exemple d’un lot mené à la réception alors que son contrat exclut la maîtrise d’œuvre ; foyer CDAIR « a remplacé le fioul », mot que sa fiche ne contient pas) — **et trois constats du relecteur vérifiés FAUX et écartés** (graphie de « mètres » : le corpus écrit 8 espaces ordinaires contre 2 fines ; longueur de la `<title>`, composée sur `ouvrage` et non sur `titre`, 50 signes ; motif des jupes verticales, qui est littéralement au CCTP). Questions B1-B10, C, D, E1-E3 ouvertes ; l’écart **49 / 50** du classeur reste non arbitré, et la section « Finalisées en 2021 » reste vide. |
| N20 | 22-037 — Audit énergétique de la Maison des Métiers, La Rochelle | `audit-chambre-des-metiers-la-rochelle` | ✅ rédigée, build 66 pages, synthèse 654 signes, 6 liens internes | ✅ `coupe-traversee`, **mécanisme `exposition` créé** (8ᵉ du compositeur — invariant octet 168/168 AVANT la greffe, 172/172 après, et de nouveau après les deux retouches de géométrie et la passe apostrophes) : **le plan de toiture comme frontière d’exposition**, et un seul critère de tri — l’organe doit-il être dehors ? Deux machines restent au-dessus avec leurs protections (cadre de capotage, grillage anti-volatiles, plots), deux franchissent le plan vers une sous-station du R+4 (boîte interrompue à la position abandonnée, flèche, brèche dans le plan, boîte pleine en dessous), et le cheminement de quartier à quartier cesse de traverser. Une seule implantation, `_ex_organe`, pour les trois formats et les deux régimes — et une distinction nouvelle, **les MESURES sont absolues et propres à chaque format, seuls les MOTIFS suivent l’échelle** ; abscisses par `_am_centres` et interruptions par `_am_dash(ech)`, réutilisées du mécanisme `amorce`. Assertion de dépassement **mise à l’épreuve et rompue quatre fois sur les trois formats** avant d’être créditée | ✅ ref_043 (8 pièces + 3 sondes) | **Le dossier le plus volumineux du chantier** (586 fichiers, 659,8 Mo) — extraction filtrée par sous-répertoire, 78 fichiers lisibles retenus. ⚠ **254 des 586 fichiers n’appartiennent pas à FT2E**, et trois pièces majeures sont un **QUATRIÈME régime de propriété**, inédit : le dossier de construction de 1994-1995 du bâtiment audité (CCTP du lot 9, bordereau de prix, étude de faisabilité — 19 Mo à elles trois), d’un autre architecte et d’un autre bureau d’études, récupéré comme matière de travail. Ni leur nom ni leurs valeurs ne se publient, mais ce n’est ni un devis concurrent ni une mission de tiers (les deux cas de la N19) : c’est l’archive de l’ouvrage. Deux autres noms de fichier mentent — `DESCRIPTIFS POUR CCTP 2022 2023.docx` est un **catalogue de textes de prescription d’un fabricant**, et `19xxx-SUIVI.doc` (le « 19xxx » annoncé au prompt) est un **gabarit vierge** de compte rendu FT2E, champs non renseignés. **146 occurrences de 22-037**, aucune autre affaire au dossier ; les 30 autres suites `NN-NNN` sont des modèles de circulateur, des codes postaux, des montants et des kilowattheures. ⚠ **Le classeur dit « Finalisées en 2022 », quatre sources disent 2023** — rapport d’audit du 14/02/2023, étude indice V2 du 12/06/2023, **plaquette 2024** et **CV de l’équipe (édition août 2026)**, ces deux dernières étant des pièces FT2E déjà publiées. `annee_livraison: 2023` (règle N16 des missions d’étude : la date du dernier rapport remis), et la section du classeur va en B1. C’est aussi le croisement commercial qui a donné la **graphie du client, déjà publiée** deux fois. `typologie: Étude` **établi de trois manières** : le contrat exclut par écrit la maîtrise d’œuvre, aucune pièce de DCE FT2E n’existe, aucun compte rendu de chantier. Secteur `Monotechnique — Audit` par le classeur (« 22037 · Audit chambre des métiers · M »), domaine simple, **contre l’intuition** qu’un siège de chambre consulaire appelle. Trois indices de contrat (nu, A, B) pour une seule affaire — **cinquième confirmation** de la règle ; l’indice A est celui qui a été signé, et il l’a été **par le syndic de l’immeuble**, non par le propriétaire à qui il est adressé (B2). L’indice B (380 € HT) porte une **assistance à constat d’huissier** : **rien n’en est publié** — ce serait porter un litige mettant en cause des tiers identifiables (B3). Trois comptes vérifiés deux fois et publiés : **18 sous-stations** (relevé des intitulés = 18 chaînes distinctes, et 1+3+4+3+3+4 à la main), **38 observations** numérotées 1 à 38 sans trou (export PDF du 18/11/2022 qui affiche « Observations 38 » + export tableur du 09/01/2023), **174 heures** dont 60 de relevé. ⚠ **Le scénario 3 ne boucle pas** (793 600 € imprimés contre 787 400 par somme des huit préconisations, écart de 6 200 €) : aucun montant de scénario n’est publié, et rien de proportionnel n’est composé sur cet axe. Ce qui boucle l’est exactement, et c’est ce qui est publié : 68,70 × 0,60 = 41,22 (2030) et × 0,50 = 34,35 (2040), les deux valeurs imprimées à la conclusion, et les ratios kWh EF/(m².an) des quatre scénarios et des quinze préconisations tombent tous sur la **SRT de 4 148,51 m²** de la note Perrenoud — laquelle porte, elle, un en-tête de gabarit (« 22-0xx », « RE2020 », « bâtiment neuf ») dont rien n’a été tiré (B5). Recette : filtre M passé de 5 à **6 fiches**, répartition **L10 T14 I5 P3 C7 M6 E3** (43 fiches, 48 en pondéré) ; la fiche entre **quatrième** du top 4 de `/secteurs/monotechnique` et en chasse 21-086 — tri documenté, pas un défaut ; vignette servie à **274 px**, sa taille de conception exacte ; trois bandes contrôlées au déploiement ; **cartouche mesuré ENTIER au navigateur** (26 px de marge, sonde `sonde-cartouche.mjs` — la coupe vue au PNG est bien l’artéfact cairosvg, **mesuré cette fois plutôt que supposé**) ; Lighthouse accessibilité **100** sur la fiche. Relecture éditoriale : **dix corrections appliquées**, dont une **contradiction avec deux fiches publiées** (« cinq réponses » alors qu’ADEI publie « Les sites ont donné trois réponses » et que La Flotte le reprend déjà), une **déduction fausse** (le « soit » enchaînait les cibles sur la consommation de référence OPERAT, dont −40 % donne 50,4 et non 41,22), et **la clause de clôture manquante**, sans laquelle le présent du § solution se lisait comme un chantier réalisé — **un constat du relecteur vérifié FAUX et écarté** (« CRC4 » est la graphie littérale du rapport et de la préconisation 04). Questions B1-B5, C1-C2, E1-E4 ouvertes ; l’écart **49 / 50** reste non arbitré, et la section « Finalisées en 2021 » reste vide. |
| N21 | 19-087 — Bâtiment SSLIA de l’aéroport de La Rochelle – Île de Ré | `batiment-sslia-aeroport-la-rochelle` | ✅ rédigée, build 67 pages, synthèse 761 signes, 6 liens internes | ✅ `coupe-traversee`, **mécanisme `retrait` créé** (9ᵉ du compositeur — invariant octet 172/172 AVANT la greffe, 176/176 après, et de nouveau après les huit retouches de rendu ; garde-fou de greffe automatisé : 56 fonctions et 167 constantes existantes contre 3 et 6 nouvelles, préfixe unique `RE_`, zéro collision ; la passe apostrophes n’a RIEN courbé, les chaînes de contrôles ayant été écrites courbes) — le périmètre du calcul RT2012 est plus petit que le bâtiment construit : une enveloppe d’un seul tenant, un mur qui la partage, et un trait épais qui ne ferme que la partie droite — il épouse la façade sur trois côtés et la quitte sur le quatrième, où il descend le long d’un mur INTÉRIEUR ; second registre : deux barres de largeur proportionnelle à la puissance absorbée (1,5 contre 6,7 kW, rapport 4,47), séparées par un filet aligné sur le mur | ✅ ref_044 (10 pièces) | Secteur `Industriel` par le classeur (« 19087 · Bâtiment SSLIA · I », section « Finalisées en 2022 »), domaine simple — le sigle SSLIA désigne le service de secours de la plateforme, PAS la sécurité incendie du bâtiment, et l’architecte lui-même écrit « bâtiment type industriel » dans le courriel fondateur. **Le piège annoncé du « 19.36 » est élucidé sur DEUX pièces** : l’acte d’engagement du marché de MOE porte « Dossier n° 19.36 » en tête de ses cinq pages, et le CR n° 01 donne l’accès extranet « bap.sdarchitectes.com — Login : 19.36 » : c’est le numéro de dossier de SD Architectes, mandataire (4ᵉ numéro de mandataire du chantier après BF ECO « 543 » et « 534 », SEMDAS « 2507 », ARCHITEM « 1821 »). ⚠ Le « 19.37 » des en-têtes de CR 01 à 14 est une COQUILLE, corrigée dès le CR 16 (le CR n° 29 titre par ailleurs « CR N°26 »). ⚠⚠ **Un TROISIÈME numéro FT2E existe et il est isolé** : le classeur d’honoraires du 19/12/2019 porte « N° : 19-125 » quand son jumeau du 01/08/2019 porte 19-087 — une occurrence contre 118 sur les pièces de production, règle de la majorité appliquée, écart porté en B1. Balayage des 80 suites `NN-NNN` du dossier : le reste est code postal, normes (NF C 15-100, 48-150…), référence de coloris de store, durée de vie de LED et cotes de plan — aucune autre affaire. Groupement de MOE : SD Architectes (mandataire, 62,45 %) + Boulard (structures, 13,64 %) + **FT2E (14,89 %, 11 566,83 € HT)** ; marché du 20/02/2020 à 57 800 € HT sur une enveloppe de 680 000 € HT, porté par l’avenant n° 1 du 20/05/2021 à 77 700,11 € HT après que l’AVP n° 3 a arrêté le coût prévisionnel à 971 251,42 € HT (→ B5). Les DEUX estimations FT2E bouclent au centime (138 075,71 et 63 377,08 € HT), et la décomposition du marché de MOE aussi. `annee_livraison: 2022` sur le classeur + le calendrier des OPR — **le PV manque, et le dernier CR CONVOQUE les OPR au 10/11/2022 sans les constater** (piège N18 reconfirmé) → B2. **Aucun compte de comptes rendus n’est publié** : 33 fichiers numérotés 01 à 38, six manquants, une coquille d’en-tête, aucune seconde source. Trois PSE chiffrées au PRO (photovoltaïque 17 100 €, IRVE, ECS solaire) NON suivies jusqu’à leur mise en œuvre → B4 ; onze CR réclament le dossier à soumettre à la DGAC, puis plus rien après le CR n° 14. **Croisement : le site publiait DÉJÀ les trois graphies** (même MOA et même SD Architectes que `batiment-voltaero-saint-agnant`, même BET Boulard que `ateliers-pilotes-capsulae`) — reprises telles quelles ; les onze docx sectoriels et la plaquette sont MUETS, mais le dossier porte le propre « dossier de références industriel » de FT2E (août 2019, 14 opérations, dont une « rénovation d’un hangar » pour le même syndicat mixte — probablement 19008, tranche 2020). Auteurs (T6) : Vincent Jaoul (CCTP et DPGF lot 11, plan de masse), Mathieu Braud (CCTP lot 12), Eric Moinet (vérificateur des deux CCTP, honoraires, contractant), et un dessinateur « YC » à identifier. Aucune surface de plancher au dossier (→ B3) → cartouche « LA ROCHELLE · 316 m² AU CALCUL RT · 2022 », mesuré ENTIER au navigateur (22 px de marge — le PNG cairosvg le coupait, et substituait aussi ▯ aux ≥ et ≤, qui rendent). Recette : Industriel passe de 5 à 6 fiches, 19-087 hors du top 4 de /secteurs/industriel-commercial (tri par numéro décroissant, comportement de gabarit) ; vignette servie à 274 px exactement. Relecture éditoriale : **30 constats appliqués**, dont deux erreurs de fait — un triplet « trois volumes, trois régimes, trois machines » démenti par la phrase suivante (une seule machine dessert les DEUX niveaux calculés), et une chronologie inversée (le SSLIA PRÉCÈDE VoltAero et Capsulae, il ne les suit pas) —, plus un EER pris pour un COP, une résistance sans unité et un « celui qu’il remplace » que la pièce n’écrit pas. ⚠ UN constat a été ÉCARTÉ après vérification sur la pièce — l’agent attribuait au tertiaire le comptage d’énergie de l’article 23, qui est celui de l’habitation — mais le défaut qu’il pointait était réel et la phrase est sortie : les DEUX usages ont leur comptage, ce n’était donc pas une exigence propre à l’étage, et « éclairage » venait de l’article tertiaire. Questions B1-B9, C1-C3, E1-E6 ouvertes |
| N22 | 20-024 — Projet GAELIC : restructuration d’un bâtiment existant en laboratoires, construction d’un bâtiment de liaison et d’un open space pour Innov’ia, La Rochelle | `gaelic-innov-ia-la-rochelle` | ✅ rédigée, build 68 pages, synthèse 693 signes, 7 liens internes | ✅ `zonage-ssi`, **mécanisme `discordance` créé** (7ᵉ du compositeur — invariant octet 176/176 AVANT la greffe, 180/180 après, et de nouveau après les deux retouches de rendu, la passe apostrophes et le passage de la cote en insécable normale ; garde-fou de greffe automatisé : 33 fonctions et 103 constantes existantes contre 7 et 39 neuves, préfixes `DI_`/`DIV_`/`DIA_`, zéro collision) : la planche oppose deux découpages du même bâtiment — un crochet **continu** sur les deux volumes du calcul RT2012 contre quatre marques **isolées** sur le volume resté sous l’arrêté du 3 mai 2007, et au registre bas une machine par volume plus cinq extractions sous le seul laboratoire ; la frontière entre la liaison et l’open space traverse la bande et **bute** sous le crochet, qui l’ignore. Largeurs proportionnées aux débits (510, 430 et 850 m³/h). Assertion de dépassement prouvée vivante sur **quatre** copies (les trois formats + une largeur bornée par la colonne voisine) ; deux sondes d’accents vivantes (3,37 % d’accents, cinq formes nues exemptées avec justification et égalité des ensembles assertée) ; **aucun trait interrompu** — le corpus lui fait déjà dire deux choses différentes. ⚠ Un défaut que seul le PNG montrait : la bande, à fond opaque, effaçait le trait de frontière tracé avant elle (l’ordre de tracé, encore) | `ref_045` — 8 pièces (deux CCTP, trois études thermiques, le contrat de maîtrise d’œuvre du mandataire, les honoraires DOE, le plan de principe CVC, le dernier CR) + les trois sondes de recette recalées | Secteur **Industriel** au classeur (« 20024 · INNOVIA - GAELIC · I », section « Finalisées en 2022 »), domaine simple — et le dépouillement donne raison au classeur, le CCTP écrivant « bâtiment de type industriel soumis au code du travail ». Recette sur le déploiement : filtre Industriel **7 cartes** (GAELIC présente), **45 cartes** au total, répartition L10 T14 I7 P3 C7 M6 E3 ; cartouche **entier**, 18 px de marge mesurés au navigateur ; vignette servie à **274 px**, sa taille de conception. ⚠ GAELIC n’entre PAS dans le top 4 de `/secteurs/industriel-commercial` — tri par numéro décroissant, 20-024 arrive cinquième : c’est le tri documenté, le filtre fait foi. ⚠ Réception **convoquée** au 28 février 2022 par le dernier CR, **jamais constatée** au dossier — `annee_livraison: 2022` retenu sur le faisceau (OPR du 14 février, levée de réserves, mission DOE commandée, classeur « Finalisées en 2022 »), question B4. ⚠ Le piège du numéro s’est bien présenté : le contrat de maîtrise d’œuvre porte **20.02** (dossier SD Architectes) en gros et 20-024 nulle part ; **222 suites** `NN-NNN` relevées — le plus gros relevé du chantier — toutes établies, 85 occurrences du seul numéro FT2E sur six pièces. ⚠ Aucun compte publié : 43 fichiers de CR numérotés 1–45, trois manquants (22, 23, 34) et un « 5 bis ». ⚠ Le site publiait **déjà** cette affaire sans le savoir : `ateliers-pilotes-capsulae` (22-006) décrit un bâtiment « adossé au bâtiment IDCAPS existant », rue Charles Tellier — c’est précisément le bâtiment que GAELIC restructure. |
| N23 | 20-039 — Remplacement et renforcement du système de vidéosurveillance du centre hospitalier de Rochefort, sur deux sites | `videosurveillance-centre-hospitalier-rochefort` | ✅ rédigée, build 69 pages, synthèse 750 signes, 6 liens internes | ✅ `zonage-ssi`, **mécanisme `gradation` créé** (8ᵉ du compositeur — invariant octet 184/184 après greffe, 40 fonctions et 142 constantes existantes contre 3 et 24 neuves, préfixes `GR_`/`GRV_`/`GRA_`, zéro collision) | `ref_046` (8 pièces) | **Dernier dossier de la tranche 2022 — la tranche est CLOSE.** Classeur : « 20039 · Vidéosurveillance CH Rochefort · M », domaine SIMPLE. Thèse : trois seuils de définition d’image (250 / 125 / 60 px/ml) choisissent le matériel, puis prononcent la réception — le critère de choix est le critère de recette ; aucune des 45 planches ne refermait cette boucle. ⚠⚠ **Objet sensible cumulant les deux précédents** (mission de sûreté N20 + ouvrage sensible N21) : question E posée dès l’ouverture, huit exclusions appliquées d’emblée — et **la thèse retenue n’en demande aucune**, ce qui a été le critère de son choix contre trois autres candidates. ⚠ **6ᵉ confirmation qu’un indice n’est pas une affaire** : deux contrats `20-039A` (gérontologie) et `20-039B` (hôpital) pour UNE affaire 20-039, plus un fichier « Indice A ». Relevé `NN-NNN` : 70 suites, 182 occurrences, **20-039 en 28 occurrences sur 10 pièces, aucun faux concurrent** — le plus net depuis la N19. ⚠ **Le grep de `src/content/` a de nouveau changé la fiche** : `expertises/electricite` et `secteurs/monotechnique` annonçaient DÉJÀ une vidéosurveillance hospitalière pour ce maître d’ouvrage (CH Marius Lacroix, La Rochelle) sans aucune fiche pour l’étayer. Tout boucle au centime : les deux contrats d’honoraires (3 802 + 4 838 = 8 640 € HT) égalent phase par phase le calcul interne de 108 h à 80 €/h, et le marché (67 156,44 € HT) somme ses quatre PSE moins une variante en moins-value, comme il somme ses deux cotraitants (29 071,28 + 38 085,16). Réception NON prononcée — `annee_livraison` 2022 retenu sur faisceau (classeur, planning d’exécution, délai borné à avril 2022, avancement 100 % actifs au dernier CR), motivé en question B.7. Docx sectoriels et CV MUETS (6ᵉ fois). Aucun compte publié (DPGF vierge de quantités). Recette : cartouche entier 19 px de marge, planche servie à 1150 px, vignette 274 px, répartition L10 T14 I7 P3 C7 **M7** E3 — 51 pondéré pour 46 fiches. 8 questions à FT2E. |
| N24 | 18-026 — Construction d’un atelier de découpe et d’usinage numériques, ZA du Fief Girard Sud, Le Thou | `atelier-numerique-fountaine-pajot-le-thou` | ✅ rédigée, build 70 pages, synthèse 708 signes, 7 liens internes | ✅ `coupe-traversee`, **mécanisme `restitution` créé** (10ᵉ du compositeur — invariant octet rejoué AVANT la greffe (184/184), APRÈS la greffe (184/184, le dénominateur passant à 188 avec le dossier neuf non encore composé) et APRÈS la dernière retouche (188/188) ; garde-fou anti-collision : 61 fonctions et 172 constantes existantes contre 3 et 27 neuves, préfixes `RS_`/`RSV_`/`RSA_`, clé de dispatch `restitution` — zéro collision) | ✅ A/A+ (ref_047), 9 pièces | **DERNIÈRE SESSION DE PRODUCTION DU CHANTIER.** ⚠⚠ **Le chantier n’a plus de matière, et l’utilisateur a arbitré en ouverture : il se clôt à 47 fiches.** `2020.zip` n’existe pas (réponse de la N23) ; `19-008` et `20-058` ne figurent dans aucune archive ; l’écart n’était donc pas 49 / 50 mais 47 / 50. Les deux autres voies ont été présentées et écartées, et **aucune fiche n’a été fabriquée pour combler l’écart**. ⚠ Piste laissée ouverte à FT2E : la section « Finalisées en 2021 » du classeur est ENTIÈREMENT VIDE — seul millésime sans entrée, entre 2020 (deux) et 2022 (quatre). **Secteur `Industriel`, domaine simple** — classeur : « 18026 · Atelier numérique fountaine Pajot · I » ; recette au déploiement : filtre Industriel 7 → **8 cartes**, total **47**, répartition L10 T14 I8 P3 C7 M7 E3 (52 en pondéré) ; 18-026 est le PLUS ANCIEN numéro du catalogue et n’entre donc pas dans le top 4 de `/secteurs/industriel-commercial` — tri documenté, pas un défaut. ⚠⚠ **MÊME CLIENT QUE LA N14, ET CE N’EST NI LA MÊME AFFAIRE NI LA MÊME COMMUNE** : `extension-fountaine-pajot-aigrefeuille` (23-036) est à Aigrefeuille-d’Aunis, cinq ans plus tard ; **le chantier du jour est au THOU**, et le dossier lui-même entretient la confusion — le § 1.1 des deux CCTP, l’en-tête des DPGF et les comptes rendus disent « Aigrefeuille » (c’est le siège du maître d’ouvrage), quand le contrat d’architecte § P3 donne « Rue des Franches - ZA du Fief Girard — 17290 LE THOU » avec ses références cadastrales, et que les PAGES DE GARDE des quatre pièces de production disent LE THOU. La pièce qui porte le cadastre tranche. ⚠ Et les comptes rendus écrivent « 17260 » — code de Gémozac : une coquille de code postal ne se recopie pas. **Le nom de fichier ment DEUX FOIS, en sens inverse** : « Recap element etudes FT2E **2012** » n’est pas une pièce de 2012 — le 2012 est celui de la **RT2012**, la pièce est du 22 juin 2018 et c’est elle qui porte le numéro d’affaire seize fois, en pied de chacune de ses pages ; et « contrat Honoraire BRUNET » n’est pas un contrat de l’entreprise mais une **proposition d’honoraires FT2E adressée à elle** (piège N22 à l’identique). ⚠ **Le RÉPERTOIRE ment aussi** : les quatorze pièces techniques sont rangées sous `03-Production/06-Pro/2018-06-22 PDF` mais leur page de garde imprime « Phase : **D.C.E.** » — le nom porte la date, pas la phase. **SEPTIÈME confirmation qu’un indice n’est pas une affaire** : la seconde proposition d’honoraires porte « 18 026 A » en page de garde ET en en-tête de page 2, mais toutes les pièces de production portent `18-026` sans lettre — la lettre distingue un SECOND CONTRAT de la même affaire, passé neuf mois plus tard avec un AUTRE commanditaire. **Relevé de numéros le plus volumineux du chantier : 451 suites distinctes, 2 590 occurrences** — il ne s’effondre pas, il se classe (≈ 2 300 occurrences de téléphones découpés dans 23 comptes rendus, 60 numéros de normes, 5 codes postaux, 3 montants, 1 artefact de police) ; **le FORMAT discrimine à lui seul** : `18-026` est la seule des 68 suites `NN-NNN` qui désigne une affaire. ⚠ Et il y a DEUX numéros de mandataire, tous deux en AA.NN : « 1714 » au contrat d’architecte, « 1814 » aux comptes rendus. **Régime de propriété — le cas inverse de la N23** : ici il Y A un mandataire (groupement de quatre), et les comptes rendus sont des pièces du mandataire puis de l’économiste-OPC, à citer avec la prudence due. **Réception NON PRONONCÉE au dossier** : le dernier compte rendu (n° 31, 23/04/2019) porte encore « Objectif réception : 24/05/2019 » et convoque la réunion suivante — comme en N18, N21, N22 et N23 il CONVOQUE sans CONSTATER. `annee_livraison: 2019` retenu sur un **faisceau de quatre** (classeur « Finalisées en 2019 » ; objectif de réception inchangé sur neuf semaines ; sept lots au-dessus de 90 % au 23/04 ; fins de marché toutes antérieures au 17/05), motivé en question B.1. ⚠ **Le compte de réunions ne se publie pas** : 23 comptes rendus au dossier sur AU MOINS 31 (le 16 manque, les 23 à 29 aussi), rythme hebdomadaire mais NON CONTINU — deux semaines sans réunion entre le n° 1 et le n° 21. La fiche écrit « au moins 31 », jamais un décompte. **Tout boucle au centime**, pour la première fois depuis la N23 : les six domaines de l’estimation somment exactement à 900 000 € HT ; les quatre parts de la mission de base somment au total de l’équipe et les pourcentages à 100,00 ; les sept postes de la part FT2E somment à sa propre part ; le second contrat somme ses deux lignes. ⚠ **MAIS le calcul d’honoraires interne DIVERGE de son propre classeur source** (6,2 % contre 4,5 %, deux décompositions par élément) : les deux bouclent, ce ne sont pas les mêmes, et **aucun de ces montants n’est publié** (question B.2). ⚠ **Contradiction interne au CCTP relevée et NON publiée** : le § 4.1.2 prescrit QUATRE chaudières de 145 kW et en donne quatre fois chaque caractéristique, les § 4.1.9 et 4.1.13 en listent DEUX, et la DPGF ne tranche pas (cadre à quantités vides). ⚠ **Un travail modificatif relevé et non publié comme réalisé** : le CR 30 porte « Tv supprimé caméra thermique » — l’organe prescrit au § 3.22 du CCTP lot 10 a été supprimé en cours de chantier (question B.6). ⚠ **Cinq rubriques ICPE non publiées** : elles ne semblent pas correspondre à un atelier de travail du bois (question B.4). **Piège (g) confirmé pour la SIXIÈME session sur sept** : la page `/secteurs/industriel-commercial` nommait DÉJÀ Fountaine Pajot, annonçait déjà « pour les entrepôts et ateliers de grande hauteur, FT2E dimensionne aérothermes, **panneaux rayonnants**, rideaux d’air » sans aucune fiche pour l’étayer, et portait déjà en livrable « **synthèse de l’interface entre le bâtiment et le procédé** » — la fiche du jour leur donne leur référence, et ces deux pages ont fourni ses liens les plus naturels. **QUATRE thèses abandonnées avant la bonne**, le corpus de 46 planches étant saturé : la cascade de quatre chaudières et ses trois départs comptés est publiée MOT POUR MOT par `foyer-cdair-saint-martin-de-re` (mécanisme `cascade`) ; la limite RT2012 qui passe à l’intérieur est exactement `batiment-sslia-aeroport-la-rochelle` (mécanisme `retrait`) ; la proportion des charges appartient à `ecole-des-douanes` ET les puissances de deux des trois départs n’existent nulle part ; la réserve de 30 % est doublement publiée. **La thèse retenue** — l’aspiration prend hors marché, la compensation rend au marché, et parce que l’air part la chaleur des postes ne passe pas par lui — est l’exact NÉGATIF de `equilibre` (Villedoux), qui constate des compensations MANQUANTES sur un audit. **Trois retouches après regard du PNG**, dont une que seul le dessin pouvait montrer : les arguments de `_rs_perfore` étaient intervertis et la gaine se traçait à y 860, hors du repère de 800 — ni le build, ni l’assertion de dépassement (qui mesure des LARGEURS, jamais une occupation) ne l’ont signalé. L’assertion, elle, a rattrapé **trois vrais dépassements** puis a été **mise à l’épreuve sur QUATRE copies, une par format plus une sur une borne calculée par le voisin : 4/4 rompent**. ⚠ Elle a aussi montré que `replier` du tronc **ignore le tracking** — un facteur correctif approché laissait encore passer 243 px pour 226 à un demi-pixel du seuil ; le repli mono est désormais MESURÉ, et le tronc n’a pas été touché (l’invariant en dépend). ⚠ **L’avance calibrée `sans-600` sous-mesure les CAPITALES d’environ 38 %** et le nœud de vignette chevauchait sa valeur : les six `libelle_vignette` sont passés en casse normale, comme le corpus, et les valeurs sont ancrées à DROITE — le placement ne dépend plus d’une largeur estimée. Sondes d’accents 3,44 % (fiche) et 3,23 % (extraction), **prouvées vivantes sur l’UNION des pièces** : 10 signalées, 10 exemptées, égalité assertée. `apostrophes-planches` : 0 à courber. Recette au déploiement : fiche 200, planche à **1150 px viewBox 0 0 1200 800** à 1440, appui à 768, vignette à 390, carte à **274 px** (taille de conception exacte), **cartouche entier, 22 px de marge à droite**. Contrôles : typecheck 0, build 70 pages, liens 47/47 à 5, 0 fuite de numéro, relevé numéral **0 nombre composé en lettres** (deux corrigés : « dix-huit » → 18, « trente et une » → 31) |

## Annexe A — prompt d'initialisation de la session N01 (à coller tel quel en session neuve)

````
Session N01/27 - FT2E v3 : chantier des 27 nouvelles fiches references.
Premier dossier.

Contexte. FT2E v3 est le site institutionnel du bureau d'etudes FT2E
(La Rochelle), Astro 6 statique, deploye en demonstration client sur
https://ft2e-v3.vercel.app (indexation verrouillee - ne pas y toucher).
Le catalogue porte 23 fiches references reelles, chacune illustree d'une
planche de schema de principe (cinq pieces par dossier). FT2E demande d'en
ajouter 27 (objectif : 50), en refaisant EXACTEMENT le meme travail.
Contrainte : 1 session = 1 dossier, close par le prompt de la suivante.

LIRE D'ABORD, dans cet ordre :
1. docs/superpowers/plans/2026-08-27-chantier-27-nouvelles-fiches.md - LE
   PLAN DE CE CHANTIER : § 1 (ce qui a change depuis 2026-08 - taxonomie,
   planche obligatoire, commune(), deux titres, maillage a la redaction),
   § 2 (le pipeline de session en 12 etapes), § 3 (questions d'ouverture).
2. docs/superpowers/plans/2026-08-07-chantier-references-reelles.md -
   § Contraintes globales + § Protocole de session (le protocole FICHE :
   numero d'affaire sur piece, synthese 480-780, ouvrage, ADR-003).
3. docs/superpowers/specs/2026-08-12-planches-references-protocole.md -
   revision 5 EN ENTIER (le protocole PLANCHE : extraction, archetypes,
   regles dures 1-7, tailles reelles).
4. CLAUDE.md, .claude/rules/content-collections.md et french-editorial.md.
Etalon : src/content/projets/creche-oranger-perigny.md + le dossier
public/images/projets/creche-oranger-perigny/.

EN OUVERTURE, POSER LES QUESTIONS DU § 3 DU PLAN (chemin du fonds
d'archives - l'ancien C:\ft2e-arch n'existe plus -, liste et ordre des 27
dossiers, regle des dossiers minces, questions transversales T1-T7). Si
l'utilisateur a deja fourni le chemin et le dossier du jour, consigner les
reponses au plan et derouler.

DOSSIER DU JOUR : [CHEMIN FOURNI PAR L'UTILISATEUR]
Dossier de travail a creer : references/ref_024/
Slug cible : a etablir au depouillement (kebab-case sans accents, verifier
qu'il n'ecrase rien).

DEROULER LE PIPELINE § 2 INTEGRALEMENT : depouillement -> releve du numero
NN-NNN sur piece FT2E -> dossier de travail -> croisement commercial
(references/docs_references/ + docs/20-source-plaquette-2024.md) -> fiche
de collecte (A/A+ remplies, B-E en questions) -> fiche
src/content/projets/<slug>.md (frontmatter taxonomie ACTUELLE : secteurs
avec « Industriel » et « Monotechnique - Audit » au tiret cadratin,
typologie Etude disponible ; lieu avec code postal entre parentheses ;
synthese et recit poses par script Python - les insecables ne survivent
pas aux outils d'edition ; >= 5 liens internes contextuels ; jamais de
numero d'affaire en prose) -> PLANCHE complete (extraction planche.json
avec archetype varie - etat : boucle-fluide 7, coupe-traversee 4, sankey 4,
zonage 3, tableau 3, chronologie 2, planche-chiffree 0 SANS module -,
composition par scripts/planches/<archetype>.py, controles a 1152 / carte
274-296 / appui 552, PNG, apostrophes-planches.py, verser.py pour ses
controles) -> qualite (typecheck 0, build vert 47 pages, editorial-reviewer,
controle-liens-internes N/N a 5, controle-numeros-affaire 0 fuite,
releve-numeral sans ecart) -> COMMIT UNIQUE fiche+planche
(content(references): ajoute la fiche reelle <nom> et sa planche ;
git ls-remote avant, depot partage) -> push (le push deploie), curl de la
fiche avec barre oblique finale, rendu controle aux trois bandes (sonde
iframe pour les largeurs telephone) -> ligne de suivi au plan -> PROMPT DE
LA SESSION N02 en annexe du plan (script APPEND, insecables chr(160)) et
reproduit integralement dans le message final.

PIEGES VERIFIES (detail : CLAUDE.md, les rules, les deux protocoles) :
le numero d'affaire se releve sur une PIECE FT2E, jamais sur le nom du
dossier (gare aux numeros des cotraitants) ; la planche est OBLIGATOIRE au
schema - une fiche sans ses cinq pieces ne build pas, fiche et planche
vont dans le MEME commit ; une vignette et un appui sont des COMPOSITIONS,
jamais des recadrages, et rien ne se sert au-dessus de sa taille de
conception ; toute valeur de planche est CITABLE dans la fiche, tout
arbitrage va dans a_valider_ft2e (jamais vide), aucun tiers ni montant ni
geometrie d'ouvrage au dessin ; cairosvg ne resout pas var() (copie de
controle sans <style>) et rend blanc un SVG racine a style width/height ;
les fins de ligne sont LF (.gitattributes - ne pas conclure a un invariant
rompu sur un clone neuf) ; PYTHONIOENCODING=utf-8 sur cette machine ;
le hook Stop commite et pousse SEUL ce qui traine sur le disque ;
npm run preview ne mesure pas la performance et sert du 304 apres rebuild
(cache-buster) ; Chrome refuse les fenetres sous 500 px (sonde iframe) ;
references/ est gitignore (motif ancre) - les pieces sources n'entrent
JAMAIS au depot.

Portee de commit : content(references). Un changement de schema Zod
eventuel (nouvelle valeur d'enum...) passe par le sous-agent
content-modeller et va dans le MEME commit que public/admin/config.yml.

Termine par le prompt de lancement de la session N02, en annexe du plan du
chantier et reproduit integralement dans ton message final - la regle de
continuite est dans CLAUDE.md parce qu'elle a ete manquee deux fois.
````

## Annexe B — prompt de lancement de la session N02 (à coller tel quel en session neuve)

````
Session N02/27 - FT2E v3 : chantier des 27 nouvelles fiches references.
Deuxieme dossier de la tranche « livraisons 2025 ».

Contexte. FT2E v3 est le site institutionnel du bureau d'etudes FT2E
(La Rochelle), Astro 6 statique, deploye en demonstration client sur
https://ft2e-v3.vercel.app (indexation verrouillee - ne pas y toucher).
Le catalogue porte 24 fiches reelles (23 + la mairie des Portes-en-Re,
session N01), chacune illustree d'une planche de schema de principe (cinq
pieces par dossier). Objectif : 50 fiches. 1 session = 1 dossier, close
par le prompt de la suivante.

LIRE D'ABORD, dans cet ordre :
1. docs/superpowers/plans/2026-08-27-chantier-27-nouvelles-fiches.md - LE
   PLAN : § 1 (ce qui a change), § 2 (pipeline 12 etapes), § 3 (REPONSES
   CONSIGNEES le 2026-08-27 - ne pas re-poser les questions d'ouverture),
   § Suivi (ligne N01), annexe B (ce prompt).
2. docs/superpowers/plans/2026-08-07-chantier-references-reelles.md -
   § Contraintes globales + § Protocole de session.
3. docs/superpowers/specs/2026-08-12-planches-references-protocole.md -
   revision 5 EN ENTIER.
4. CLAUDE.md, .claude/rules/content-collections.md et french-editorial.md.
Etalons : src/content/projets/creche-oranger-perigny.md (fiche) et, pour
une session N complete, src/content/projets/mairie-les-portes-en-re.md +
public/images/projets/mairie-les-portes-en-re/ + references/ref_024/.

DOSSIER DU JOUR : « 21-062 - Pole commercial FORS 79 - BTB » (255
fichiers, 673 Mo), dans
C:\claude_code_dev_projects\ft2e_new_archives\2025.zip (tranche des
livraisons 2025, 10 dossiers - liste au § 3 du plan).
ATTENTION DISQUE SATURE (~1,7 Go libres) : supprimer d'abord le
repertoire extrait de la session precedente
(ft2e_new_archives/2025/22-011- Rehab Mairie Les Portes en Re - BTB),
puis extraire LE SEUL dossier du jour depuis le ZIP
(unzip 2025.zip "2025/21-062*"). Le ZIP est la source, il ne se
supprime pas.
Dossier de travail a creer : references/ref_025/
Slug cible : a etablir au depouillement (kebab-case sans accents,
verifier qu'il n'ecrase rien).

CE QUE LA N01 A ETABLI (verifiable au depot) :
- annee_livraison: 2025 se pose sur le docx commercial (« REALISATION :
  2025 », docx Rehabilitation/batiments publics 2024) + le cadrage
  utilisateur de la tranche ; le PV de reception manque souvent a
  l'archive -> question B1 de la collecte, statut livre.
- Architecte Agence Blanchard Tetaud Blanchet (La Rochelle) - graphie T3
  harmonisee (Maubec, Saint-Rogatien, Portes-en-Re). FORS 79 est aussi
  un dossier BTB.
- Les numeros des cotraitants pietinent les pieces : BAG « 232 030 »,
  BF ECO « 542 » (prefixe economiste, cf. « 539 »/« 563 ») - le numero
  FT2E se releve sur page de garde CCTP (« Affaire n° : 21-062 »).
- Archetypes apres N01 : boucle-fluide 8 (terminaux, Portes-en-Re) -
  coupe-traversee 4 - sankey 4 - zonage 3 - tableau 3 - chronologie 2 -
  planche-chiffree 0 SANS module. VARIER - l'archetype se choisit sur la
  THESE de la fiche, jamais sur le secteur.
- ARBITRAGE FT2E (N01, a lire au § 1 du plan) : la planche schematise la
  SOLUTION APPORTEE, jamais le deroule de l'affaire. Une premiere planche
  de la N01 portait le phasage de l'operation : refusee et refaite en
  schema des equipements. Choisir un mecanisme d'INGENIERIE (flux,
  traversee, partition, dimensionnement), pas un recit.
- Si la these exige un mecanisme nouveau : il s'ecrit DANS le compositeur
  d'archetype (constantes prefixees par mecanisme - deux affectations du
  meme nom au niveau module se marchent dessus), et l'invariant octet des
  planches existantes du meme compositeur se rejoue AVANT et APRES la
  greffe, dans une copie hors depot (N01 : 28/28 sur boucle-fluide, deux
  fois). Un mecanisme dont la planche est retiree se retire avec elle.

DEROULER LE PIPELINE § 2 INTEGRALEMENT : depouillement -> releve du
numero NN-NNN sur piece FT2E -> references/ref_025/ (3 a 8 pieces) ->
croisement commercial (references/docs_references/ + docs/20-source-
plaquette-2024.md) -> fiche de collecte (A/A+ remplies, B-E en questions)
-> fiche src/content/projets/<slug>.md (taxonomie ACTUELLE ; lieu avec
code postal entre parentheses ; synthese 480-780 posee par script ; >= 5
liens internes ; jamais de numero d'affaire NI de millesime d'ouverture
en prose) -> PLANCHE complete (extraction avec a_valider_ft2e non vide,
composition par scripts/planches/<archetype>.py, controles a 1152 /
carte 274-296 / appui 552, PNG 2400x1600, apostrophes-planches.py,
verser.py) -> qualite (typecheck 0, build vert 48 pages,
editorial-reviewer, controle-liens-internes 25/25 a 5,
controle-numeros-affaire 0 fuite, releve-numeral sans ecart nouveau) ->
COMMIT UNIQUE fiche+planche+compositeur (content(references): ajoute la
fiche reelle <nom> et sa planche ; git ls-remote avant, depot partage)
-> push (le push deploie), curl de la fiche AVEC barre oblique finale +
marqueur de build, rendu controle aux trois bandes (sonde iframe pour
les largeurs telephone) -> ligne de suivi au plan -> PROMPT DE LA
SESSION N03 en annexe du plan (script Python ou Write, jamais un long
heredoc bash) et reproduit integralement dans le message final.

PIEGES VERIFIES EN N01 (en plus de ceux de l'annexe A, tous confirmes) :
- Un heredoc bash long (env. 70 lignes et plus) se fait TRONQUER
  silencieusement : ecrire les gros fichiers par l'outil Write PUIS
  passer scripts/injection-typographique.py, avec CONTROLE DE PRESENCE
  des insecables apres coup (calibrer les seuils d'assertion sur le
  texte lui-meme, pas sur un autre fichier).
- Le hook PreToolUse « hookify » peut bloquer l'outil Read par
  intermittence (fichier python manquant dans le cache du plugin) :
  reessayer, ou lire par Bash.
- cairosvg : la copie de controle perd <style> ET l'attribut style de la
  racine ; filets 8 chiffres a fusionner (#00393A38 -> #C1CFD0,
  #00393A29 -> #CFDADB, #00393A1F -> #D9E2E3) ; la fleche U+2192 sort en
  tofu au controle cairosvg mais rend au navigateur (precedent Tourtet,
  reverifie en N01).
- PYTHONIOENCODING=utf-8 sur cette machine ; le hook Stop commite et
  pousse SEUL ce qui traine ; /references/ est gitignore (motif ancre) -
  les pieces sources n'entrent JAMAIS au depot ; npm run preview ne
  mesure pas la performance ; Chrome refuse les fenetres sous 500 px
  (sonde iframe).
- La planche n'expose NI le millesime d'ouverture (l'axe des temps de la
  N01 ouvre en 2023 pour cette raison), NI montant, NI tiers ; tout
  arbitrage de dessin va dans a_valider_ft2e (jamais vide).

Portee de commit : content(references). Un changement de schema Zod
eventuel passe par le sous-agent content-modeller et va dans le MEME
commit que public/admin/config.yml.

Termine par le prompt de lancement de la session N03, en annexe du plan
du chantier et reproduit integralement dans ton message final - la regle
de continuite est dans CLAUDE.md parce qu'elle a ete manquee deux fois.
````

## Annexe C — prompt de lancement de la session N03 (à coller tel quel en session neuve — récrit le 2026-08-27 au soir : la règle d'indexation sectorielle est ancrée à la rédaction de fiche)

````
Session N03/27 - FT2E v3 : chantier des 27 nouvelles fiches references.
Troisieme dossier de la tranche « livraisons 2025 ».

Contexte. FT2E v3 est le site institutionnel du bureau d'etudes FT2E
(La Rochelle), Astro 6 statique, deploye en demonstration client sur
https://ft2e-v3.vercel.app (indexation verrouillee - ne pas y toucher).
Le catalogue porte 25 fiches reelles (23 + Portes-en-Re N01 + Commerces
de Fors N02), chacune illustree d'une planche de schema de principe
(cinq pieces par dossier). Objectif : 50 fiches. 1 session = 1 dossier,
close par le prompt de la suivante.

LIRE D'ABORD, dans cet ordre :
1. docs/superpowers/plans/2026-08-27-chantier-27-nouvelles-fiches.md -
   LE PLAN : § 1 (ce qui a change), § 2 (pipeline 12 etapes), § 3
   (reponses consignees + COMPLEMENT N02 : le classeur de references
   FT2E), § Suivi (lignes N01, N02), annexe C (ce prompt).
2. docs/superpowers/plans/2026-08-07-chantier-references-reelles.md -
   § Contraintes globales + § Protocole de session.
3. docs/superpowers/specs/2026-08-12-planches-references-protocole.md -
   revision 5 EN ENTIER.
4. CLAUDE.md, .claude/rules/content-collections.md et french-editorial.md.
Etalons : src/content/projets/creche-oranger-perigny.md (fiche) et, pour
une session N complete, src/content/projets/pole-commercial-fors.md +
public/images/projets/pole-commercial-fors/ + references/ref_025/.

REGLE D'INDEXATION SECTORIELLE - etablie le 2026-08-27, A APPLIQUER A
LA REDACTION DE CHAQUE FICHE (etape 6 du pipeline), pas apres coup :
« REFERENCES SITE FT2E.ods » (references/docs_references/, classeur
fourni par FT2E) FAIT FOI pour le classement sectoriel. Concretement,
AVANT d'ecrire le frontmatter :
1. Ouvrir le classeur (python zipfile sur content.xml, ou pandoc) et y
   retrouver l'affaire PAR SON NUMERO (graphie sans tiret : « 19036 »).
2. En relever le domaine (legende : L Logements / T Tertiaire & ERP /
   I Industriel / P Patrimoine / C Coordination SSI /
   M Monotechnique-Audit / E EXE) -> champ `secteur`.
3. Si le classeur porte un domaine DOUBLE (« T § C ») : le premier est
   le `secteur`, le second va au champ `secteur_secondaire` (optionnel
   au schema depuis le 2026-08-27, garde-fou « doit differer ») - la
   fiche parait alors dans les deux filtres et sur les deux pages de
   secteur. Precedent : hotel-yachtman (T § C).
4. JAMAIS de deduction depuis le dossier, l'usage RT ou le nom de
   l'operation : la N02 penchait « Industriel » pour Fors, le classeur
   dit T - et les 25 fiches ont du etre re-referencees le soir meme
   (7 bascules, commits ce334b2/09270a3). Le classeur peut contredire
   l'intuition (Saint-Rogatien, pole commercial : I ; Fors, pole
   commercial : T) - il gagne.
5. CONSIGNER la lecture dans la fiche de collecte (ligne « Secteur » :
   citer l'entree du classeur telle quelle) ; si l'affaire est ABSENTE
   du classeur ou son domaine illisible -> question B a FT2E et choix
   provisoire argumente, jamais silencieux.
6. EN RECETTE (etape 10) : verifier sur le deploiement que la fiche
   repond au(x) bon(s) filtre(s) de /references (compteurs de chips)
   et parait sur sa ou ses pages /secteurs/<slug> - sonde precedente :
   references/ref_025/sonde-filtres.mjs. Repartition attendue AVANT la
   N03 : L7 T9 I2 P1 C3 M2 E2 pour 25 fiches (Yachtman compte double).

DOSSIER DU JOUR : « 19-036 -150 logts Rompsay MEDIATIM » (208 fichiers),
dans C:\claude_code_dev_projects\ft2e_new_archives\2025.zip (tranche des
livraisons 2025 - liste au § 3 du plan ; le classeur donne « 19036 ·
150 Logts Rompsay Mediatim - AURORA · L », Finalisees en 2025 ->
secteur Logements, pas de domaine double, annee_livraison 2025).
ATTENTION DISQUE SATURE (~1,2 Go libres) : supprimer d'abord le
repertoire extrait de la session precedente
(ft2e_new_archives/2025/21-062 - Pole commercial FORS 79 - BTB) - le
rm -rf est REFUSE par les permissions, passer par python
shutil.rmtree - puis extraire LE SEUL dossier du jour depuis le ZIP
PAR PYTHON ZIPFILE : les motifs d'unzip (« 2025/19-036* », « *19-036* »)
ne matchent PAS les entrees de ce ZIP (verifie en N02) -
  python -c "import zipfile; z=zipfile.ZipFile(r'...\2025.zip');
  z.extractall(r'...\ft2e_new_archives',
  members=[n for n in z.namelist() if '19-036' in n])"
Le ZIP est la source, il ne se supprime pas.
Dossier de travail a creer : references/ref_026/
Slug cible : a etablir au depouillement (kebab-case sans accents,
verifier qu'il n'ecrase rien).

PARTICULARITE DU DOSSIER : le cliche du hero de l'accueil (« Aurora,
147 logements », corpus secteurs, arbitrage FT2E du 2026-08-26) vient
de CETTE operation. Compter les logements sur pieces (nom de dossier
« 150 logts », classeur « 150 Logts », legende du corpus « 147 ») et
harmoniser fiche <-> legende du corpus secteurs si l'ecart se confirme
(la legende vit dans src/content/secteurs/, une seule source). MEDIATIM
est le meme groupe que exe-residence-horizon-mediatim (25-097) - lien
interne naturel ; etablir la chaine contractuelle exacte (contrat
direct promoteur ? groupement ?) sur pieces.

CE QUE LES N01-N02 ONT ETABLI (verifiable au depot) :
- annee_livraison se pose sur le cadrage de tranche + classeur
  (« Finalisees en 2025 ») ; le PV de reception manque souvent ->
  question B1, statut livre.
- Archetypes apres N02 : boucle-fluide 8 - sankey 5 (partage, Fors) -
  coupe-traversee 4 - zonage 3 - tableau 3 - chronologie 2 -
  planche-chiffree 0 SANS module. VARIER - l'archetype se choisit sur
  la THESE de la fiche, jamais sur le secteur.
- Un mecanisme nouveau s'ecrit DANS le compositeur d'archetype
  (constantes prefixees), et l'invariant octet des planches existantes
  du meme compositeur se rejoue AVANT et APRES la greffe, dans une
  copie hors depot (N01 : 28/28 boucle-fluide ; N02 : 16/16 sankey,
  deux fois chacune).
- ARBITRAGE FT2E (N01) : la planche schematise la SOLUTION APPORTEE,
  jamais le deroule de l'affaire. Mecanisme d'INGENIERIE, pas un recit.
- Quand la planche porte les valeurs d'une ETUDE et non de l'ouvrage
  execute (N02 : l'annee d'energie du scenario 36 kWc, la ou le DCE
  prescrit 32,33 kWc), l'EN-TETE DE REGISTRE nomme l'etude - « c'est
  ce qui empeche la planche de mentir » - et l'ecart va en
  a_valider_ft2e. Toute valeur du dessin doit rester citable dans la
  fiche : completer la fiche plutot que d'arrondir le dessin.

DEROULER LE PIPELINE § 2 INTEGRALEMENT : depouillement -> releve du
numero NN-NNN sur piece FT2E (gare aux numeros des cotraitants : BF ECO
« 533 » en N02, « 542 » en N01) -> references/ref_026/ (3 a 8 pieces) ->
croisement commercial (references/docs_references/ - docx sectoriels ET
classeur ODS - + docs/20-source-plaquette-2024.md) -> fiche de collecte
(A/A+ remplies, B-E en questions, ligne Secteur citant le classeur) ->
fiche src/content/projets/<slug>.md (SECTEUR ET EVENTUEL
SECTEUR_SECONDAIRE RELEVES AU CLASSEUR - regle d'indexation
sectorielle ci-dessus, points 1 a 5 ; taxonomie ACTUELLE ; lieu avec
code postal entre parentheses ; synthese 480-780 posee par script ;
>= 5 liens internes ; jamais de numero d'affaire NI de millesime
d'ouverture en prose) -> PLANCHE complete (extraction avec
a_valider_ft2e non vide, composition par
scripts/planches/<archetype>.py, controles a 1152 / carte 274-296 /
appui 552, PNG 2400x1600, apostrophes-planches.py, verser.py) ->
qualite (typecheck 0, build vert 49 pages, editorial-reviewer,
controle-liens-internes 26/26 a 5, controle-numeros-affaire 0 fuite,
releve-numeral sans ecart nouveau) -> COMMIT UNIQUE
fiche+planche+compositeur (content(references): ajoute la fiche reelle
<nom> ; git ls-remote avant, depot partage) -> push (le push deploie),
curl de la fiche AVEC barre oblique finale + marqueur de build, rendu
controle aux trois bandes (sonde iframe pour les largeurs telephone,
script pret : references/ref_024/sonde-fiche.mjs) ET CONTROLE DE
L'INDEXATION SECTORIELLE (point 6 de la regle : filtres de /references
et page(s) de secteur, sonde references/ref_025/sonde-filtres.mjs) ->
ligne de suivi au plan -> PROMPT DE LA SESSION N04 en annexe du plan
(script Python ou Write, jamais un long heredoc bash) et reproduit
integralement dans le message final.

PIEGES VERIFIES EN N01-N02 (en plus de ceux des annexes A et B, tous
confirmes) :
- Un heredoc bash long se fait TRONQUER silencieusement : gros fichiers
  par l'outil Write PUIS scripts/injection-typographique.py, avec
  CONTROLE DE PRESENCE des insecables apres coup (seuils calibres sur
  le texte lui-meme). Un planche.json s'ecrit par script Python avec
  les insecables en echappements \u202f (Write les normalise).
- injection-typographique.py ne connait pas l'unite « A » (ampere) :
  « 400 A » reste en espace simple - poser la fine par remplacement
  cible apres coup si des amperes apparaissent.
- Le corpus ecrit ESPACE SIMPLE devant un nom compte (« 61 modules »,
  « 93 pages », « 700 metres ») : ne pas « corriger » en fine, seules
  les unites (symboles) prennent la fine. Verifie sur 31 contre 7.
- cairosvg : la copie de controle perd <style> ET l'attribut style de
  la racine - regex avec espace OPTIONNELLE avant style= : sur la
  vignette l'attribut clot la balise et un motif avec espace finale ne
  matche pas -> PNG BLANC (revecu en N02) ; filets 8 chiffres a
  fusionner (#00393A38 -> #C1CFD0, #00393A29 -> #CFDADB,
  #00393A1F -> #D9E2E3).
- PYTHONIOENCODING=utf-8 sur cette machine ; le hook Stop commite et
  pousse SEUL ce qui traine (⚠ livrables/ porte deux fichiers non
  suivis anterieurs a la N02) ; /references/ est gitignore (motif
  ancre) - les pieces sources n'entrent JAMAIS au depot ; npm run
  preview ne mesure pas la performance ; Chrome refuse les fenetres
  sous 500 px (sonde iframe).
- La planche n'expose NI le millesime d'ouverture, NI montant, NI
  tiers ; tout arbitrage de dessin va dans a_valider_ft2e (jamais
  vide).

Portee de commit : content(references). Un changement de schema Zod
eventuel passe par le sous-agent content-modeller et va dans le MEME
commit que public/admin/config.yml.

Termine par le prompt de lancement de la session N04, en annexe du plan
du chantier et reproduit integralement dans ton message final - la
regle de continuite est dans CLAUDE.md parce qu'elle a ete manquee deux
fois. Le prompt N04 REPREND le bloc « REGLE D'INDEXATION SECTORIELLE »
ci-dessus tel quel (repartition attendue remise a jour) : la regle est
permanente, elle ne se resume pas.
````

## Annexe D — prompt de lancement de la session N04 (à coller tel quel en session neuve)

````
Session N04/27 - FT2E v3 : chantier des 27 nouvelles fiches references.
Quatrieme dossier de la tranche « livraisons 2025 ».

Contexte. FT2E v3 est le site institutionnel du bureau d'etudes FT2E
(La Rochelle), Astro 6 statique, deploye en demonstration client sur
https://ft2e-v3.vercel.app (indexation verrouillee - ne pas y toucher).
Le catalogue porte 26 fiches reelles (23 + Portes-en-Re N01 + Commerces
de Fors N02 + Residence Aurora N03), chacune illustree d'une planche de
schema de principe (cinq pieces par dossier). Objectif : 50 fiches.
1 session = 1 dossier, close par le prompt de la suivante.

LIRE D'ABORD, dans cet ordre :
1. docs/superpowers/plans/2026-08-27-chantier-27-nouvelles-fiches.md -
   LE PLAN : § 1 (ce qui a change), § 2 (pipeline 12 etapes), § 3
   (reponses consignees + COMPLEMENT N02 : le classeur de references
   FT2E), § Suivi (lignes N01 a N03), annexe D (ce prompt).
2. docs/superpowers/plans/2026-08-07-chantier-references-reelles.md -
   § Contraintes globales + § Protocole de session.
3. docs/superpowers/specs/2026-08-12-planches-references-protocole.md -
   revision 5 EN ENTIER.
4. CLAUDE.md, .claude/rules/content-collections.md et french-editorial.md.
Etalons : src/content/projets/creche-oranger-perigny.md (fiche) et, pour
une session N complete, src/content/projets/residence-aurora-la-rochelle.md
+ public/images/projets/residence-aurora-la-rochelle/ + references/ref_026/.

REGLE D'INDEXATION SECTORIELLE - etablie le 2026-08-27, A APPLIQUER A
LA REDACTION DE CHAQUE FICHE (etape 6 du pipeline), pas apres coup :
« REFERENCES SITE FT2E.ods » (references/docs_references/, classeur
fourni par FT2E) FAIT FOI pour le classement sectoriel. Concretement,
AVANT d'ecrire le frontmatter :
1. Ouvrir le classeur (python zipfile sur content.xml, ou pandoc) et y
   retrouver l'affaire PAR SON NUMERO (graphie sans tiret : « 25004 »).
2. En relever le domaine (legende : L Logements / T Tertiaire & ERP /
   I Industriel / P Patrimoine / C Coordination SSI /
   M Monotechnique-Audit / E EXE) -> champ `secteur`.
3. Si le classeur porte un domaine DOUBLE (« T § C ») : le premier est
   le `secteur`, le second va au champ `secteur_secondaire` (optionnel
   au schema depuis le 2026-08-27, garde-fou « doit differer ») - la
   fiche parait alors dans les deux filtres et sur les deux pages de
   secteur. Precedent : hotel-yachtman (T § C).
4. JAMAIS de deduction depuis le dossier, l'usage RT ou le nom de
   l'operation : la N02 penchait « Industriel » pour Fors, le classeur
   dit T - et les 25 fiches ont du etre re-referencees le soir meme
   (7 bascules, commits ce334b2/09270a3). Le classeur peut contredire
   l'intuition (Saint-Rogatien, pole commercial : I ; Fors, pole
   commercial : T ; 23083 « plan de comptage Airbus » : E et non M) -
   il gagne.
5. CONSIGNER la lecture dans la fiche de collecte (ligne « Secteur » :
   citer l'entree du classeur telle quelle) ; si l'affaire est ABSENTE
   du classeur ou son domaine illisible -> question B a FT2E et choix
   provisoire argumente, jamais silencieux.
6. EN RECETTE (etape 10) : verifier sur le deploiement que la fiche
   repond au(x) bon(s) filtre(s) de /references (compteurs de chips)
   et parait sur sa ou ses pages /secteurs/<slug> - sondes precedentes :
   references/ref_026/sonde-filtres.mjs et sonde-fiche.mjs. ⚠ Une page
   /secteurs/<slug> n'affiche que les 4 affaires les plus recentes du
   secteur (tri par numero decroissant) : une affaire ancienne peut
   legitimement n'y pas paraitre (N03 : 19-036 hors du top 4 de
   Logements) - le filtre de /references, lui, montre tout.
   Repartition attendue AVANT la N04 : L8 T9 I2 P1 C3 M2 E2 pour
   26 fiches (Yachtman compte double).

DOSSIER DU JOUR : « 25-004 - Musée Pierre Loti ROCHEFORT »
(191 fichiers), dans
C:\claude_code_dev_projects\ft2e_new_archives\2025.zip (tranche des
livraisons 2025 - liste au § 3 du plan ; le classeur donne « 25004 ·
Maison pierre Loti · P § C », Finalisees en 2025 -> secteur Patrimoine,
secteur_secondaire Coordination SSI - PREMIER DOUBLE DOMAINE de la
tranche, precedent Yachtman -, annee_livraison 2025).
ATTENTION DISQUE SATURE (~1,2 Go libres) : supprimer d'abord le
repertoire extrait de la session precedente
(ft2e_new_archives/2025/19-036 -150 logts Rompsay MEDIATIM) - le
rm -rf est REFUSE par les permissions, passer par python
shutil.rmtree - puis extraire LE SEUL dossier du jour depuis le ZIP
PAR PYTHON ZIPFILE : les motifs d'unzip ne matchent PAS les entrees de
ce ZIP (verifie en N02) -
  python -c "import zipfile; z=zipfile.ZipFile(r'...\2025.zip');
  z.extractall(r'...\ft2e_new_archives',
  members=[n for n in z.namelist() if '25-004' in n])"
Le ZIP est la source, il ne se supprime pas.
Dossier de travail a creer : references/ref_027/
Slug cible : a etablir au depouillement (kebab-case sans accents,
verifier qu'il n'ecrase rien).

PARTICULARITES DU DOSSIER : l'ancienne fiche DEMO « maison-pierre-loti »
(supprimee le 2026-08-08) portait ce sujet - le slug est LIBRE mais ne
pas le reprendre sans y penser : verifier qu'aucune redirection ni
reference ne subsiste (grep pierre-loti sur src/ et docs/). Le musee
Pierre-Loti est un monument historique de Rochefort (patrimoine +
coordination SSI au classeur) : le recit se pretera au double domaine -
etablir sur pieces la nature exacte des missions FT2E (fluides ?
SSI ? les deux ?) et la chaine contractuelle (MOA ville de Rochefort ?).
La fiche parait dans les filtres Patrimoine ET Coordination SSI, et sur
les deux pages de secteur (garde-fou : secteur_secondaire doit differer
du secteur).

CE QUE LES N01-N03 ONT ETABLI (verifiable au depot) :
- annee_livraison se pose sur le cadrage de tranche + classeur
  (« Finalisees en 2025 ») ; le PV de reception manque souvent ->
  question B1, statut livre.
- Archetypes apres N03 : boucle-fluide 8 - coupe-traversee 5 (colonne,
  Aurora) - sankey 5 - zonage 3 - tableau 3 - chronologie 2 -
  planche-chiffree 0 SANS module. VARIER - l'archetype se choisit sur
  la THESE de la fiche, jamais sur le secteur. Un dossier patrimoine +
  SSI peut appeler zonage-ssi (3 planches seulement) - mais seulement
  si la these est bien la mise en securite.
- Un mecanisme nouveau s'ecrit DANS le compositeur d'archetype
  (constantes prefixees), et l'invariant octet des planches existantes
  du meme compositeur se rejoue AVANT et APRES la greffe, dans une
  copie hors depot (N01 : 28/28 boucle-fluide ; N02 : 16/16 sankey ;
  N03 : 16/16 coupe-traversee, trois fois - la passe
  apostrophes-planches.py MODIFIE le compositeur si des apostrophes
  droites ont fui dans les chaines de controles : rejouer l'invariant
  APRES elle aussi).
- ARBITRAGE FT2E (N01) : la planche schematise la SOLUTION APPORTEE,
  jamais le deroule de l'affaire. Mecanisme d'INGENIERIE, pas un recit.
- Quand la planche porte les valeurs d'une ETUDE et non de l'ouvrage
  execute, l'EN-TETE DE REGISTRE nomme l'etude (N02) ; en N03 l'en-tete
  nomme la piece (« CCTP marche de decembre 2022 »). Toute valeur du
  dessin doit rester citable dans la fiche : completer la fiche plutot
  que d'arrondir le dessin.
- N03 : ne pas suraffirmer un motif repete - « une chaudiere par
  logement » a du etre nuance (les T1 ont l'ECS electrique, § 3.3 du
  CCTP) : chercher l'EXCEPTION du systeme decrit avant d'ecrire
  « chaque » ou « tous ».

DEROULER LE PIPELINE § 2 INTEGRALEMENT : depouillement -> releve du
numero NN-NNN sur piece FT2E (gare aux numeros des cotraitants) ->
references/ref_027/ (3 a 8 pieces) -> croisement commercial
(references/docs_references/ - docx sectoriels ET classeur ODS - +
docs/20-source-plaquette-2024.md ; Loti a un precedent DEMO : ne rien
en reprendre, tout se source sur pieces) -> fiche de collecte (A/A+
remplies, B-E en questions, ligne Secteur citant le classeur) -> fiche
src/content/projets/<slug>.md (SECTEUR Patrimoine ET
SECTEUR_SECONDAIRE Coordination SSI RELEVES AU CLASSEUR - regle
d'indexation sectorielle ci-dessus, points 1 a 5 ; taxonomie
ACTUELLE ; lieu avec code postal entre parentheses ; synthese 480-780
posee par script ; >= 5 liens internes ; jamais de numero d'affaire NI
de millesime d'ouverture en prose) -> PLANCHE complete (extraction
avec a_valider_ft2e non vide, composition par
scripts/planches/<archetype>.py, controles a 1152 / carte 274-296 /
appui 552, PNG 2400x1600, apostrophes-planches.py, verser.py) ->
qualite (typecheck 0, build vert 50 pages, editorial-reviewer,
controle-liens-internes 27/27 a 5, controle-numeros-affaire 0 fuite,
releve-numeral sans ecart nouveau) -> COMMIT UNIQUE
fiche+planche+compositeur (content(references): ajoute la fiche reelle
<nom> ; git ls-remote avant, depot partage) -> push (le push deploie),
curl de la fiche AVEC barre oblique finale + marqueur de build, rendu
controle aux trois bandes (sonde iframe pour les largeurs telephone,
script pret : references/ref_026/sonde-fiche.mjs, URL a adapter) ET
CONTROLE DE L'INDEXATION SECTORIELLE (point 6 : filtres de /references
et pages de secteur, sonde references/ref_026/sonde-filtres.mjs) ->
ligne de suivi au plan -> PROMPT DE LA SESSION N05 en annexe du plan
(script Python ou Write, jamais un long heredoc bash) et reproduit
integralement dans le message final.

PIEGES VERIFIES EN N01-N03 (en plus de ceux des annexes A et B, tous
confirmes) :
- Un heredoc bash long se fait TRONQUER silencieusement : gros fichiers
  par l'outil Write PUIS scripts/injection-typographique.py, avec
  CONTROLE DE PRESENCE des insecables apres coup (seuils calibres sur
  le texte lui-meme). Un planche.json s'ecrit par script Python avec
  les insecables en echappements \u202f - MAIS la normalisation de
  Write n'est PAS deterministe (N03 : des fines litterales ont
  survecu, d'autres fois non) : seul le CONTROLE DE PRESENCE apres
  coup fait foi, jamais la confiance dans l'outil.
- injection-typographique.py ne connait pas l'unite « A » (ampere) :
  poser la fine par remplacement cible apres coup si besoin.
- Le corpus ecrit ESPACE SIMPLE devant un nom compte (« 61 modules »,
  « 93 pages ») MAIS la fine devant « litres » (12 occurrences contre
  0 en N03) : en cas de doute sur un mot-unite, MESURER le corpus
  avant de « corriger ».
- cairosvg : la copie de controle perd <style> ET l'attribut style de
  la racine (regex avec espace OPTIONNELLE avant style=) ; filets
  8 chiffres a fusionner (#00393A38 -> #C1CFD0, #00393A29 -> #CFDADB,
  #00393A1F -> #D9E2E3) ; U+2192 et Δ (U+0394) sortent en tofu au
  controle cairosvg mais rendent au navigateur (precedents Tourtet,
  Aurora).
- PYTHONIOENCODING=utf-8 sur cette machine ; le hook Stop commite et
  pousse SEUL ce qui traine (⚠ livrables/ porte deux fichiers non
  suivis anterieurs a la N02) ; /references/ est gitignore (motif
  ancre) - les pieces sources n'entrent JAMAIS au depot ; npm run
  preview ne mesure pas la performance ; Chrome refuse les fenetres
  sous 500 px (sonde iframe).
- La planche n'expose NI le millesime d'ouverture, NI montant, NI
  tiers ; tout arbitrage de dessin va dans a_valider_ft2e (jamais
  vide).
- verser.py repond « deja verse » quand `planche:` est ecrit
  directement au frontmatter (fiche neuve) : ses controles 1-3 (cinq
  pieces, extraction, SVG) ont TOURNE avant ce message - c'est un
  succes, pas un refus.

Portee de commit : content(references). Un changement de schema Zod
eventuel passe par le sous-agent content-modeller et va dans le MEME
commit que public/admin/config.yml.

Termine par le prompt de lancement de la session N05, en annexe du
plan du chantier et reproduit integralement dans ton message final -
la regle de continuite est dans CLAUDE.md parce qu'elle a ete manquee
deux fois. Le prompt N05 REPREND le bloc « REGLE D'INDEXATION
SECTORIELLE » ci-dessus tel quel (repartition attendue remise a jour :
apres la N04, P2 et C4 si le double domaine se confirme) : la regle
est permanente, elle ne se resume pas.
````

## Annexe E — prompt de lancement de la session N05 (à coller tel quel en session neuve)

````
Session N05/27 - FT2E v3 : chantier des 27 nouvelles fiches references.
Cinquieme dossier de la tranche « livraisons 2025 ».

Contexte. FT2E v3 est le site institutionnel du bureau d'etudes FT2E
(La Rochelle), Astro 6 statique, deploye en demonstration client sur
https://ft2e-v3.vercel.app (indexation verrouillee - ne pas y toucher).
Le catalogue porte 27 fiches reelles (23 + Portes-en-Re N01 + Commerces
de Fors N02 + Residence Aurora N03 + Maison de Pierre Loti N04), chacune
illustree d'une planche de schema de principe (cinq pieces par dossier).
Objectif : 50 fiches. 1 session = 1 dossier, close par le prompt de la
suivante.

LIRE D'ABORD, dans cet ordre :
1. docs/superpowers/plans/2026-08-27-chantier-27-nouvelles-fiches.md -
   LE PLAN : § 1 (ce qui a change), § 2 (pipeline 12 etapes), § 3
   (reponses consignees + COMPLEMENT N02 : le classeur de references
   FT2E), § Suivi (lignes N01 a N04), annexe E (ce prompt).
2. docs/superpowers/plans/2026-08-07-chantier-references-reelles.md -
   § Contraintes globales + § Protocole de session.
3. docs/superpowers/specs/2026-08-12-planches-references-protocole.md -
   revision 5 EN ENTIER.
4. CLAUDE.md, .claude/rules/content-collections.md et french-editorial.md.
Etalons : src/content/projets/creche-oranger-perigny.md (fiche) et, pour
une session N complete, src/content/projets/maison-pierre-loti-rochefort.md
+ public/images/projets/maison-pierre-loti-rochefort/ + references/ref_027/
(premier double domaine, mission de reprise).

REGLE D'INDEXATION SECTORIELLE - etablie le 2026-08-27, A APPLIQUER A
LA REDACTION DE CHAQUE FICHE (etape 6 du pipeline), pas apres coup :
« REFERENCES SITE FT2E.ods » (references/docs_references/, classeur
fourni par FT2E) FAIT FOI pour le classement sectoriel. Concretement,
AVANT d'ecrire le frontmatter :
1. Ouvrir le classeur (python zipfile sur content.xml, ou pandoc) et y
   retrouver l'affaire PAR SON NUMERO (graphie sans tiret : « 19096 »).
2. En relever le domaine (legende : L Logements / T Tertiaire & ERP /
   I Industriel / P Patrimoine / C Coordination SSI /
   M Monotechnique-Audit / E EXE) -> champ `secteur`.
3. Si le classeur porte un domaine DOUBLE (« T § C ») : le premier est
   le `secteur`, le second va au champ `secteur_secondaire` (optionnel
   au schema depuis le 2026-08-27, garde-fou « doit differer ») - la
   fiche parait alors dans les deux filtres et sur les deux pages de
   secteur. Precedents : hotel-yachtman (T § C), maison-pierre-loti-
   rochefort (P § C, N04).
4. JAMAIS de deduction depuis le dossier, l'usage RT ou le nom de
   l'operation : la N02 penchait « Industriel » pour Fors, le classeur
   dit T - et les 25 fiches ont du etre re-referencees le soir meme
   (7 bascules, commits ce334b2/09270a3). Le classeur peut contredire
   l'intuition (Saint-Rogatien, pole commercial : I ; Fors, pole
   commercial : T ; 23083 « plan de comptage Airbus » : E et non M) -
   il gagne.
5. CONSIGNER la lecture dans la fiche de collecte (ligne « Secteur » :
   citer l'entree du classeur telle quelle) ; si l'affaire est ABSENTE
   du classeur ou son domaine illisible -> question B a FT2E et choix
   provisoire argumente, jamais silencieux.
6. EN RECETTE (etape 10) : verifier sur le deploiement que la fiche
   repond au(x) bon(s) filtre(s) de /references (compteurs de chips)
   et parait sur sa ou ses pages /secteurs/<slug> - sondes precedentes :
   references/ref_027/sonde-filtres.mjs et sonde-fiche.mjs. ⚠ Une page
   /secteurs/<slug> n'affiche que les 4 affaires les plus recentes du
   secteur (tri par numero decroissant) : une affaire ancienne peut
   legitimement n'y pas paraitre (N03 : 19-036 hors du top 4 de
   Logements ; 19-096 sera dans le meme cas si Patrimoine depasse
   4 affaires) - le filtre de /references, lui, montre tout.
   Repartition attendue AVANT la N05 : L8 T9 I2 P2 C4 M2 E2 pour
   27 fiches (Yachtman T+C et Loti P+C comptent double).

DOSSIER DU JOUR : « 19-096 - Eglise St Sauveur - GOUTAL »
(103 fichiers), dans
C:\claude_code_dev_projects\ft2e_new_archives\2025.zip (tranche des
livraisons 2025 - liste au § 3 du plan ; le classeur donne « 19096 ·
Eglise St SAUVEUR · P », Finalisees en 2025 -> secteur Patrimoine, pas
de domaine double, annee_livraison 2025 ; affaire ouverte en 2019 ->
annee: 2019, une affaire LONGUE : ni le millesime d'ouverture ni l'axe
2019-2025 ne montent sur la planche ni en prose).
ATTENTION DISQUE SATURE (~1,2 Go libres avant nettoyage) : supprimer
d'abord le repertoire extrait de la session precedente - ⚠ son nom
(« 25-004 - Musée Pierre Loti ROCHEFORT ») est sorti de zipfile en
MOJIBAKE cp437 : NE PAS taper le nom accentue, le resoudre par
os.listdir puis startswith('25-004'), et supprimer par python
shutil.rmtree (le rm -rf est refuse par les permissions). Puis
extraire LE SEUL dossier du jour depuis le ZIP PAR PYTHON ZIPFILE
(les motifs d'unzip ne matchent PAS les entrees de ce ZIP) -
  python -c "import zipfile; z=zipfile.ZipFile(r'...\2025.zip');
  z.extractall(r'...\ft2e_new_archives',
  members=[n for n in z.namelist() if '19-096' in n])"
Le ZIP est la source, il ne se supprime pas.
Dossier de travail a creer : references/ref_028/
Slug cible : a etablir au depouillement (kebab-case sans accents,
verifier qu'il n'ecrase rien - « eglise-saint-sauveur-la-rochelle »
pressenti).

PARTICULARITES DU DOSSIER : l'entree du docx commercial
« Réf. Réhabilitation Patrimoine.docx » porte : « Restauration du
clocher, des cloches et du beffroi de l'eglise Saint-Sauveur - LA
ROCHELLE (17). MOA : Ville de La Rochelle. ARCHITECTE : M. GOUTAL
ACMH. MONTANT TRAVAUX : 1 200 000 € HT. MISSION COMPLETE DE MAITRISE
D'ŒUVRE : Refection du systeme electrique et programmation des
sonneries des cloches. REALISATION : 2025 » - donc mission COMPLETE
(a l'inverse de la reprise N04), monument historique, electricite d'un
clocher et programmation de sonneries de cloches. Etablir sur pieces
la graphie et le role exacts de GOUTAL (ACMH), la nature de la mission
FT2E et son numero releve sur piece FT2E (gare aux numeros des
cotraitants). Le corpus secteurs patrimoine porte deja un cliche reel
« Eglise Saint-Sauveur » (patrimoine/02.jpeg) ; verifier par grep
saint-sauveur sur src/ qu'aucune prose preexistante ne raconte
l'operation - si elle existe, la confronter aux pieces (precedent N04 :
le § Loti de patrimoine.md portait deux affirmations non sourcees,
reecrites sur pieces dans le meme commit). L'archetype se choisit sur
la THESE (une refection electrique + sonneries peut appeler
tableau-electrique, 3 planches seulement - mais seulement si la these
est bien la distribution), jamais sur le secteur.

CE QUE LES N01-N04 ONT ETABLI (verifiable au depot) :
- annee_livraison se pose sur le cadrage de tranche + classeur
  (« Finalisees en 2025 ») ; le PV de reception des travaux manque
  souvent -> question B1, statut livre. N04 : un PV de reception SSI
  (21/10/2025) peut asseoir la livraison meme sans PV des travaux.
- Archetypes apres N04 : boucle-fluide 8 - coupe-traversee 5 -
  sankey 5 - zonage-ssi 4 (inversion, Loti) - tableau 3 -
  chronologie 2 - planche-chiffree 0 SANS module. VARIER -
  l'archetype se choisit sur la THESE de la fiche, jamais sur le
  secteur.
- Un mecanisme nouveau s'ecrit DANS le compositeur d'archetype
  (constantes prefixees), et l'invariant octet des planches existantes
  du meme compositeur se rejoue AVANT et APRES la greffe, dans une
  copie hors depot, ET APRES la passe apostrophes-planches.py (N04 :
  12/12 trois fois ; la passe a ENCORE modifie le compositeur - 8
  apostrophes droites fuies dans les chaines de controles : les ecrire
  COURBES des l'ecriture du mecanisme).
- ARBITRAGE FT2E (N01) : la planche schematise la SOLUTION APPORTEE,
  jamais le deroule de l'affaire. Mecanisme d'INGENIERIE, pas un recit.
- Quand la planche porte les valeurs d'une ETUDE ou d'un as-built d'un
  tiers, l'EN-TETE DE REGISTRE ou a_valider_ft2e le nomme (N02 :
  l'etude 36 kWc ; N04 : l'as-built de mise en service 46/38 contre le
  devis 43/41). Toute valeur du dessin doit rester citable dans la
  fiche : completer la fiche plutot que d'arrondir le dessin.
- N03 : chercher l'EXCEPTION du systeme decrit avant d'ecrire
  « chaque » ou « tous » (les T1 d'Aurora ; en N04 le « un point par
  zone » du PV d'essais etait dementi par sa propre liste - 16 points
  sur 14 zones : la fiche ecrit « a travers les zones »).
- N04 : les docx commerciaux peuvent contredire les pieces (« Livraison
  2026 » et « type E » aux docx ; PV et CCTP disent 2025 et « type Y,
  L et M ») - la piece fait foi, l'ecart va en question B.

DEROULER LE PIPELINE § 2 INTEGRALEMENT : depouillement -> releve du
numero NN-NNN sur piece FT2E (gare aux numeros des cotraitants) ->
references/ref_028/ (3 a 8 pieces) -> croisement commercial
(references/docs_references/ - docx sectoriels ET classeur ODS - +
docs/20-source-plaquette-2024.md) -> fiche de collecte (A/A+
remplies, B-E en questions, ligne Secteur citant le classeur) -> fiche
src/content/projets/<slug>.md (SECTEUR Patrimoine RELEVE AU CLASSEUR -
regle d'indexation sectorielle ci-dessus, points 1 a 5 ; taxonomie
ACTUELLE ; lieu avec code postal entre parentheses ; synthese 480-780
posee par script ; >= 5 liens internes ; jamais de numero d'affaire NI
de millesime d'ouverture en prose - 19-096 est ouverte en 2019, seule
la livraison 2025 se publie) -> PLANCHE complete (extraction avec
a_valider_ft2e non vide, composition par
scripts/planches/<archetype>.py, controles a 1152 / carte 274-296 /
appui 552, PNG 2400x1600, apostrophes-planches.py, verser.py) ->
qualite (typecheck 0, build vert 51 pages, editorial-reviewer,
controle-liens-internes 28/28 a 5, controle-numeros-affaire 0 fuite,
releve-numeral sans ecart nouveau) -> COMMIT UNIQUE
fiche+planche+compositeur (content(references): ajoute la fiche reelle
<nom> ; git ls-remote avant, depot partage) -> push (le push deploie),
curl de la fiche AVEC barre oblique finale + marqueur de build, rendu
controle aux trois bandes (sonde iframe pour les largeurs telephone,
script pret : references/ref_027/sonde-fiche.mjs, URL a adapter) ET
CONTROLE DE L'INDEXATION SECTORIELLE (point 6 : filtre Patrimoine de
/references et page /secteurs/patrimoine, sonde
references/ref_027/sonde-filtres.mjs) -> ligne de suivi au plan ->
PROMPT DE LA SESSION N06 en annexe du plan (script Python ou Write,
jamais un long heredoc) et reproduit integralement dans le message
final.

PIEGES VERIFIES EN N01-N04 (en plus de ceux des annexes A et B, tous
confirmes) :
- Un heredoc long se fait TRONQUER ou refuser silencieusement - bash
  COMME python (revecu en N04 sur un python << EOF de 100 lignes) :
  gros fichiers et scripts par l'outil Write PUIS execution, avec
  CONTROLE DE PRESENCE des insecables apres coup (seuils calibres sur
  le texte lui-meme : compter les emplois nombre-unite du texte et
  exiger l'egalite, N04). Un planche.json s'ecrit par script Python
  avec fines et apostrophes construites par chr(8239)/chr(8217).
- injection-typographique.py ne connait pas l'unite « A » (ampere) :
  poser la fine par remplacement cible apres coup si besoin.
- Le corpus ecrit ESPACE SIMPLE devant un nom compte (« 61 modules »,
  « 46 detecteurs ») MAIS la fine devant les unites : en cas de doute
  sur un mot-unite, MESURER le corpus avant de « corriger ».
- cairosvg : la copie de controle perd <style> ET l'attribut style de
  la racine (regex avec espace OPTIONNELLE avant style=) ; filets
  8 chiffres a fusionner (#00393A38 -> #C1CFD0, #00393A29 -> #CFDADB,
  #00393A1F -> #D9E2E3) ; U+2192 et Δ (U+0394) sortent en tofu au
  controle cairosvg mais rendent au navigateur (precedents Tourtet,
  Aurora).
- PYTHONIOENCODING=utf-8 sur cette machine ; le hook Stop commite et
  pousse SEUL ce qui traine (⚠ livrables/ porte deux fichiers non
  suivis anterieurs a la N02) ; /references/ est gitignore (motif
  ancre) - les pieces sources n'entrent JAMAIS au depot ; npm run
  preview ne mesure pas la performance ; Chrome refuse les fenetres
  sous 500 px (sonde iframe).
- La planche n'expose NI le millesime d'ouverture, NI montant, NI
  tiers ; tout arbitrage de dessin va dans a_valider_ft2e (jamais
  vide).
- verser.py repond « deja verse » quand `planche:` est ecrit
  directement au frontmatter (fiche neuve) : ses controles 1-3 (cinq
  pieces, extraction, SVG) ont TOURNE avant ce message - c'est un
  succes, pas un refus.

Portee de commit : content(references). Un changement de schema Zod
eventuel passe par le sous-agent content-modeller et va dans le MEME
commit que public/admin/config.yml.

Termine par le prompt de lancement de la session N06, en annexe du
plan du chantier et reproduit integralement dans ton message final -
la regle de continuite est dans CLAUDE.md parce qu'elle a ete manquee
deux fois. Le prompt N06 REPREND le bloc « REGLE D'INDEXATION
SECTORIELLE » ci-dessus tel quel (repartition attendue remise a jour :
apres la N05, P3) : la regle est permanente, elle ne se resume pas.
````

## Annexe F — prompt de lancement de la session N06 (à coller tel quel en session neuve)

````
Session N06/27 - FT2E v3 : chantier des 27 nouvelles fiches references.
Sixieme dossier de la tranche « livraisons 2025 ».

Contexte. FT2E v3 est le site institutionnel du bureau d'etudes FT2E
(La Rochelle), Astro 6 statique, deploye en demonstration client sur
https://ft2e-v3.vercel.app (indexation verrouillee - ne pas y toucher).
Le catalogue porte 28 fiches reelles (23 + Portes-en-Re N01 + Commerces
de Fors N02 + Residence Aurora N03 + Maison de Pierre Loti N04 + Clocher
Saint-Sauveur N05), chacune illustree d'une planche de schema de
principe (cinq pieces par dossier). Objectif : 50 fiches. 1 session =
1 dossier, close par le prompt de la suivante.

LIRE D'ABORD, dans cet ordre :
1. docs/superpowers/plans/2026-08-27-chantier-27-nouvelles-fiches.md -
   LE PLAN : § 1 (ce qui a change), § 2 (pipeline 12 etapes), § 3
   (reponses consignees + COMPLEMENT N02 : le classeur de references
   FT2E), § Suivi (lignes N01 a N05), annexe F (ce prompt).
2. docs/superpowers/plans/2026-08-07-chantier-references-reelles.md -
   § Contraintes globales + § Protocole de session.
3. docs/superpowers/specs/2026-08-12-planches-references-protocole.md -
   revision 5 EN ENTIER.
4. CLAUDE.md, .claude/rules/content-collections.md et french-editorial.md.
Etalons : src/content/projets/creche-oranger-perigny.md (fiche) et, pour
une session N complete, src/content/projets/eglise-saint-sauveur-la-
rochelle.md + public/images/projets/eglise-saint-sauveur-la-rochelle/ +
references/ref_028/ (mission complete en groupement, mecanisme nouveau).

REGLE D'INDEXATION SECTORIELLE - etablie le 2026-08-27, A APPLIQUER A
LA REDACTION DE CHAQUE FICHE (etape 6 du pipeline), pas apres coup :
« REFERENCES SITE FT2E.ods » (references/docs_references/, classeur
fourni par FT2E) FAIT FOI pour le classement sectoriel. Concretement,
AVANT d'ecrire le frontmatter :
1. Ouvrir le classeur (python zipfile sur content.xml, ou pandoc) et y
   retrouver l'affaire PAR SON NUMERO (graphie sans tiret : « 22013 »).
2. En relever le domaine (legende : L Logements / T Tertiaire & ERP /
   I Industriel / P Patrimoine / C Coordination SSI /
   M Monotechnique-Audit / E EXE) -> champ `secteur`.
3. Si le classeur porte un domaine DOUBLE (« T § C ») : le premier est
   le `secteur`, le second va au champ `secteur_secondaire` (optionnel
   au schema depuis le 2026-08-27, garde-fou « doit differer ») - la
   fiche parait alors dans les deux filtres et sur les deux pages de
   secteur. Precedents : hotel-yachtman (T § C), maison-pierre-loti-
   rochefort (P § C, N04).
4. JAMAIS de deduction depuis le dossier, l'usage RT ou le nom de
   l'operation : la N02 penchait « Industriel » pour Fors, le classeur
   dit T - et les 25 fiches ont du etre re-referencees le soir meme
   (7 bascules, commits ce334b2/09270a3). Le classeur peut contredire
   l'intuition (Saint-Rogatien, pole commercial : I ; Fors, pole
   commercial : T ; 23083 « plan de comptage Airbus » : E et non M) -
   il gagne.
5. CONSIGNER la lecture dans la fiche de collecte (ligne « Secteur » :
   citer l'entree du classeur telle quelle) ; si l'affaire est ABSENTE
   du classeur ou son domaine illisible -> question B a FT2E et choix
   provisoire argumente, jamais silencieux.
6. EN RECETTE (etape 10) : verifier sur le deploiement que la fiche
   repond au(x) bon(s) filtre(s) de /references (compteurs de chips)
   et parait sur sa ou ses pages /secteurs/<slug> - sondes precedentes :
   references/ref_027/sonde-filtres.mjs et sonde-fiche.mjs. ⚠ Une page
   /secteurs/<slug> n'affiche que les 4 affaires les plus recentes du
   secteur (tri par numero decroissant) : une affaire ancienne peut
   legitimement n'y pas paraitre (N03 : 19-036 hors du top 4 de
   Logements ; 19-096 est dans le meme cas des que Patrimoine depasse
   4 affaires) - le filtre de /references, lui, montre tout.
   Repartition attendue AVANT la N06 : L8 T9 I2 P3 C4 M2 E2 pour
   28 fiches (Yachtman T+C et Loti P+C comptent double).

DOSSIER DU JOUR : « 22-013- 16 Logts L'Houmeau OPH - BTB »
(102 fichiers), dans
C:\claude_code_dev_projects\ft2e_new_archives\2025.zip (tranche des
livraisons 2025 - liste au § 3 du plan ; le classeur donne « 22013 ·
16 Logements l'Houmeau- Monsidun · L », Finalisees en 2025 -> secteur
Logements, pas de domaine double, annee_livraison 2025 ; affaire
ouverte en 2022 -> annee: 2022, millesime d'ouverture jamais en prose).
ATTENTION DISQUE SATURE (~4 Go libres apres nettoyage N05) : supprimer
d'abord le repertoire extrait de la session precedente
(ft2e_new_archives/2025/19-096 - Eglise St Sauveur - GOUTAL, nom sans
accent - os.listdir + startswith('19-096') par prudence), par python
shutil.rmtree (le rm -rf est refuse par les permissions). Puis
extraire LE SEUL dossier du jour depuis le ZIP PAR PYTHON ZIPFILE
(les motifs d'unzip ne matchent PAS les entrees de ce ZIP) -
  python -c "import zipfile; z=zipfile.ZipFile(r'...\2025.zip');
  z.extractall(r'...\ft2e_new_archives',
  members=[n for n in z.namelist() if '22-013' in n])"
⚠ Le nom du dossier peut sortir en MOJIBAKE cp437 (apostrophe de
« L'Houmeau ») : resoudre par os.listdir + startswith('22-013'),
jamais en tapant le nom. Le ZIP est la source, il ne se supprime pas.
Dossier de travail a creer : references/ref_029/
Slug cible : a etablir au depouillement (kebab-case sans accents,
verifier qu'il n'ecrase rien - « logements-monsidun-l-houmeau »
pressenti, a confronter au nom d'usage des pieces).

PARTICULARITES DU DOSSIER : BTB est l'architecte des N01 (mairie des
Portes-en-Re), de Maubec, de Saint-Rogatien et de Fors - graphie
harmonisee « Agence Blanchard Tetaud Blanchet » a verifier sur pieces.
« OPH » au nom du dossier et « Monsidun » au classeur : etablir sur
pieces le maitre d'ouvrage exact (OPH de l'agglomeration de La
Rochelle ? operation « Monsidun » ?) et le compte de logements (16 au
nom du dossier et au classeur). Le secteur Logements est deja riche
(L8) : chercher la THESE singuliere du dossier avant de choisir
l'archetype - un seizieme recit de boucle-fluide n'apporte rien si la
matiere est ailleurs.

CE QUE LES N01-N05 ONT ETABLI (verifiable au depot) :
- annee_livraison se pose sur le cadrage de tranche + classeur
  (« Finalisees en 2025 ») ; le PV de reception des travaux manque
  souvent -> question B1, statut livre. N04 : un PV de reception SSI
  peut asseoir la livraison ; N05 : un CR d'OPR qui date la reception
  (« du 8 au 22 avril date de la reception ») aussi.
- Archetypes apres N05 : boucle-fluide 8 - coupe-traversee 5 -
  sankey 5 - zonage-ssi 4 - tableau 4 (montee, Saint-Sauveur) -
  chronologie 2 - planche-chiffree 0 SANS module. VARIER -
  l'archetype se choisit sur la THESE de la fiche, jamais sur le
  secteur.
- Un mecanisme nouveau s'ecrit DANS le compositeur d'archetype
  (constantes prefixees), et l'invariant octet des planches existantes
  du meme compositeur se rejoue AVANT la greffe, APRES la greffe et
  APRES la passe apostrophes-planches.py, dans une copie hors depot
  (N05 : 12/12 trois fois) ; la passe a courbe des apostrophes droites
  fuies dans les chaines de controles a CHACUNE des N03, N04 et N05 -
  les ecrire courbes des l'ecriture ne suffit pas, VERIFIER par la
  passe en mode mesure avant de composer.
- ARBITRAGE FT2E (N01) : la planche schematise la SOLUTION APPORTEE,
  jamais le deroule de l'affaire. Mecanisme d'INGENIERIE, pas un recit.
- Quand la planche porte les valeurs d'une ETUDE, d'un as-built d'un
  tiers ou d'un CCTP de prescription (N05 : pas de DOE a l'archive),
  l'EN-TETE DE REGISTRE ou a_valider_ft2e le nomme. Toute valeur du
  dessin doit rester citable dans la fiche.
- N03 : chercher l'EXCEPTION du systeme decrit avant d'ecrire
  « chaque » ou « tous ». N05 : un motif repete dessine (points
  d'escalier) ne doit pas pouvoir etre lu comme un COMPTE si la source
  ne compte pas - le dire dans controles ET a_valider_ft2e.
- N04-N05 : les docx commerciaux peuvent contredire les pieces (N05 :
  « 1 200 000 € HT » au docx patrimoine = l'enveloppe initiale de
  l'AE, l'avenant 1 arrete 1 966 332,88 € HT) - la piece fait foi,
  l'ecart va en question B.

DEROULER LE PIPELINE § 2 INTEGRALEMENT : depouillement -> releve du
numero NN-NNN sur piece FT2E (gare aux numeros des cotraitants - BTB,
economiste et bureau de controle ont les leurs) -> references/ref_029/
(3 a 8 pieces) -> croisement commercial (references/docs_references/ -
docx sectoriels, dont « References logements collectifs - FT2E
maj.docx », ET classeur ODS - + docs/20-source-plaquette-2024.md) ->
fiche de collecte (A/A+ remplies, B-E en questions, ligne Secteur
citant le classeur) -> fiche src/content/projets/<slug>.md (SECTEUR
Logements RELEVE AU CLASSEUR - regle d'indexation sectorielle
ci-dessus, points 1 a 5 ; taxonomie ACTUELLE ; lieu avec code postal
entre parentheses ; synthese 480-780 posee par script ; >= 5 liens
internes ; jamais de numero d'affaire NI de millesime d'ouverture en
prose) -> PLANCHE complete (extraction avec a_valider_ft2e non vide,
composition par scripts/planches/<archetype>.py, controles a 1152 /
carte 274-296 / appui 552, PNG 2400x1600, apostrophes-planches.py,
verser.py) -> qualite (typecheck 0, build vert 52 pages,
editorial-reviewer, controle-liens-internes 29/29 a 5,
controle-numeros-affaire 0 fuite, releve-numeral sans ecart nouveau)
-> COMMIT UNIQUE fiche+planche+compositeur (content(references):
ajoute la fiche reelle <nom> ; git ls-remote avant, depot partage) ->
push (le push deploie), curl de la fiche AVEC barre oblique finale +
marqueur de build, rendu controle aux trois bandes (sonde iframe pour
les largeurs telephone, script pret : references/ref_027/
sonde-fiche.mjs, URL a adapter) ET CONTROLE DE L'INDEXATION
SECTORIELLE (point 6 : filtre Logements de /references et page
/secteurs/logements - 22-013 sera dans le top 4 du secteur, sonde
references/ref_027/sonde-filtres.mjs) -> ligne de suivi au plan ->
PROMPT DE LA SESSION N07 en annexe du plan (script Python ou Write,
jamais un long heredoc) et reproduit integralement dans le message
final.

PIEGES VERIFIES EN N01-N05 (en plus de ceux des annexes A et B, tous
confirmes) :
- Un heredoc long se fait TRONQUER ou refuser silencieusement - bash
  COMME python : gros fichiers et scripts par l'outil Write PUIS
  execution, avec CONTROLE DE PRESENCE des insecables apres coup
  (seuils calibres sur le texte lui-meme). Un planche.json s'ecrit par
  script Python avec fines et apostrophes construites par
  chr(8239)/chr(8217) - et un .replace pour courber TOUTES les
  apostrophes du contenu (N05 : l'ecriture directe en avait laisse 62
  droites, rattrapees par le controle d'auto-assertion du script).
- injection-typographique.py ne connait pas l'unite « A » (ampere) :
  poser la fine par remplacement cible apres coup si besoin. Les
  mots-unites epeles se MESURENT au corpus avant correction (N05 :
  « 40 metres » et « 10 ohms » restent en espace simple - 6/0 et 1/0
  au corpus).
- cairosvg : la copie de controle perd <style> ET l'attribut style de
  la racine (regex avec espace OPTIONNELLE avant style=) ; filets
  8 chiffres a fusionner (#00393A38 -> #C1CFD0, #00393A29 -> #CFDADB,
  #00393A1F -> #D9E2E3) ; U+2192, Δ (U+0394) et Ω (U+03A9) sortent en
  tofu au controle cairosvg mais rendent au navigateur (precedents
  Tourtet, Aurora, Saint-Sauveur).
- PYTHONIOENCODING=utf-8 sur cette machine ; le hook Stop commite et
  pousse SEUL ce qui traine (⚠ livrables/ porte deux fichiers non
  suivis anterieurs a la N02) ; /references/ est gitignore (motif
  ancre) - les pieces sources n'entrent JAMAIS au depot ; npm run
  preview ne mesure pas la performance ; Chrome refuse les fenetres
  sous 500 px (sonde iframe).
- La planche n'expose NI le millesime d'ouverture, NI montant, NI
  tiers ; tout arbitrage de dessin va dans a_valider_ft2e (jamais
  vide).
- verser.py repond « deja verse » quand `planche:` est ecrit
  directement au frontmatter (fiche neuve) : ses controles 1-3 (cinq
  pieces, extraction, SVG) ont TOURNE avant ce message - c'est un
  succes, pas un refus.

Portee de commit : content(references). Un changement de schema Zod
eventuel passe par le sous-agent content-modeller et va dans le MEME
commit que public/admin/config.yml.

Termine par le prompt de lancement de la session N07, en annexe du
plan du chantier et reproduit integralement dans ton message final -
la regle de continuite est dans CLAUDE.md parce qu'elle a ete manquee
deux fois. Le prompt N07 REPREND le bloc « REGLE D'INDEXATION
SECTORIELLE » ci-dessus tel quel (repartition attendue remise a jour :
apres la N06, L9) : la regle est permanente, elle ne se resume pas.
````

## Annexe G — prompt de lancement de la session N07 (à coller tel quel en session neuve)

````
Session N07/27 - FT2E v3 : chantier des 27 nouvelles fiches references.
Septieme dossier de la tranche « livraisons 2025 ».

Contexte. FT2E v3 est le site institutionnel du bureau d'etudes FT2E
(La Rochelle), Astro 6 statique, deploye en demonstration client sur
https://ft2e-v3.vercel.app (indexation verrouillee - ne pas y toucher).
Le catalogue porte 29 fiches reelles (23 + Portes-en-Re N01 + Commerces
de Fors N02 + Residence Aurora N03 + Maison de Pierre Loti N04 + Clocher
Saint-Sauveur N05 + EcoQuartier de L'Houmeau N06), chacune illustree
d'une planche de schema de principe (cinq pieces par dossier).
Objectif : 50 fiches. 1 session = 1 dossier, close par le prompt de la
suivante.

LIRE D'ABORD, dans cet ordre :
1. docs/superpowers/plans/2026-08-27-chantier-27-nouvelles-fiches.md -
   LE PLAN : § 1 (ce qui a change), § 2 (pipeline 12 etapes), § 3
   (reponses consignees + COMPLEMENT N02 : le classeur de references
   FT2E), § Suivi (lignes N01 a N06), annexe G (ce prompt).
2. docs/superpowers/plans/2026-08-07-chantier-references-reelles.md -
   § Contraintes globales + § Protocole de session.
3. docs/superpowers/specs/2026-08-12-planches-references-protocole.md -
   revision 5 EN ENTIER.
4. CLAUDE.md, .claude/rules/content-collections.md et french-editorial.md.
Etalons : src/content/projets/creche-oranger-perigny.md (fiche) et, pour
une session N complete, src/content/projets/logements-ecoquartier-l-
houmeau.md + public/images/projets/logements-ecoquartier-l-houmeau/ +
references/ref_029/ (mecanisme nouveau + double registre sur la planche).

REGLE D'INDEXATION SECTORIELLE - etablie le 2026-08-27, A APPLIQUER A
LA REDACTION DE CHAQUE FICHE (etape 6 du pipeline), pas apres coup :
« REFERENCES SITE FT2E.ods » (references/docs_references/, classeur
fourni par FT2E) FAIT FOI pour le classement sectoriel. Concretement,
AVANT d'ecrire le frontmatter :
1. Ouvrir le classeur (python zipfile sur content.xml, ou pandoc) et y
   retrouver l'affaire PAR SON NUMERO (graphie sans tiret : « 23009 »).
2. En relever le domaine (legende : L Logements / T Tertiaire & ERP /
   I Industriel / P Patrimoine / C Coordination SSI /
   M Monotechnique-Audit / E EXE) -> champ `secteur`.
3. Si le classeur porte un domaine DOUBLE (« T § C ») : le premier est
   le `secteur`, le second va au champ `secteur_secondaire` (optionnel
   au schema depuis le 2026-08-27, garde-fou « doit differer ») - la
   fiche parait alors dans les deux filtres et sur les deux pages de
   secteur. Precedents : hotel-yachtman (T § C), maison-pierre-loti-
   rochefort (P § C, N04).
4. JAMAIS de deduction depuis le dossier, l'usage RT ou le nom de
   l'operation : la N02 penchait « Industriel » pour Fors, le classeur
   dit T - et les 25 fiches ont du etre re-referencees le soir meme
   (7 bascules, commits ce334b2/09270a3). Le classeur peut contredire
   l'intuition (Saint-Rogatien, pole commercial : I ; Fors, pole
   commercial : T ; 23083 « plan de comptage Airbus » : E et non M ;
   23099 « CPAM » : M - IRVE, pas T) - il gagne.
5. CONSIGNER la lecture dans la fiche de collecte (ligne « Secteur » :
   citer l'entree du classeur telle quelle) ; si l'affaire est ABSENTE
   du classeur ou son domaine illisible -> question B a FT2E et choix
   provisoire argumente, jamais silencieux.
6. EN RECETTE (etape 10) : verifier sur le deploiement que la fiche
   repond au(x) bon(s) filtre(s) de /references (compteurs de chips)
   et parait sur sa ou ses pages /secteurs/<slug> - sondes precedentes :
   references/ref_027/sonde-filtres.mjs et sonde-fiche.mjs. ⚠ Une page
   /secteurs/<slug> n'affiche que les 4 affaires les plus recentes du
   secteur (tri par numero decroissant) : une affaire ancienne peut
   legitimement n'y pas paraitre (N03 : 19-036 hors du top 4 de
   Logements ; 19-096 idem des que Patrimoine depasse 4 affaires) - le
   filtre de /references, lui, montre tout.
   Repartition attendue AVANT la N07 : L9 T9 I2 P3 C4 M2 E2 pour
   29 fiches (Yachtman T+C et Loti P+C comptent double).

DOSSIER DU JOUR : « 23-009- 60 maisons Louise Magnan - IAA »
(58 fichiers), dans
C:\claude_code_dev_projects\ft2e_new_archives\2025.zip (tranche des
livraisons 2025 - liste au § 3 du plan ; le classeur donne « 23009 ·
60 maisons Louise Magnan · L », Finalisees en 2025 -> secteur
Logements, pas de domaine double, annee_livraison 2025 ; affaire
ouverte en 2023 -> annee: 2023, millesime d'ouverture jamais en prose).
« IAA » au nom du dossier suggere Immobiliere Atlantic Amenagement
(MOA des fiches 22-033 Echire et 22-010 Saint-Rogatien) - MOA exacte a
etablir sur pieces, jamais sur le nom du dossier. Localisation
« Louise Magnan » a etablir sur pieces (commune + code postal
obligatoire au champ lieu).
ATTENTION DISQUE (~4,8 Go libres apres nettoyage N06) : supprimer
d'abord le repertoire extrait de la session precedente
(ft2e_new_archives/2025/22-013- 16 Logts L'Houmeau OPH - BTB -
os.listdir + startswith('22-013') par prudence, l'apostrophe du nom
sort en mojibake cp437), par python shutil.rmtree (le rm -rf est
refuse par les permissions). Puis extraire LE SEUL dossier du jour
depuis le ZIP PAR PYTHON ZIPFILE (les motifs d'unzip ne matchent PAS
les entrees de ce ZIP) -
  python -c "import zipfile; z=zipfile.ZipFile(r'...\2025.zip');
  z.extractall(r'...\ft2e_new_archives',
  members=[n for n in z.namelist() if '23-009' in n])"
Le ZIP est la source, il ne se supprime pas.
Dossier de travail a creer : references/ref_030/
Slug cible : a etablir au depouillement (kebab-case sans accents,
verifier qu'il n'ecrase rien - « maisons-louise-magnan-<commune> »
pressenti, a confronter au nom d'usage des pieces).

PARTICULARITES DU DOSSIER : 60 maisons = la plus grosse operation de
logements individuels du catalogue (le corpus porte deja « 54 maisons »
et « soixante lits » - verifier le compte sur pieces, le nom du dossier
ne fait pas foi). Le secteur Logements est deja riche (L9 avant la
session) et la N06 vient de traiter une operation du meme secteur :
chercher la THESE singuliere - 60 maisons individuelles posent des
questions serielles (production repetee, VRD, foisonnement) qu'aucune
fiche ne porte encore. Apres la N07 ne resteront de la tranche 2025 que
les deux dossiers minces (23-099 CPAM-IRVE « M », 25 fichiers ;
23-083 Airbus comptage « E », 10 fichiers) - la regle des dossiers
minces (Q3, § 3 du plan) s'appliquera.

CE QUE LES N01-N06 ONT ETABLI (verifiable au depot) :
- annee_livraison se pose sur le cadrage de tranche + classeur
  (« Finalisees en 2025 ») ; le PV de reception des travaux manque
  souvent -> question B1, statut livre. N04 : un PV de reception SSI
  peut asseoir la livraison ; N05 : un CR d'OPR qui date la reception ;
  N06 : un CR de chantier qui l'annonce (« RECEPTION LE 30/06 (hors
  VRD et espaces verts) », CR n°60 du 30/06/2025).
- Archetypes apres N06 : boucle-fluide 8 - sankey 6 (affectation,
  L'Houmeau) - coupe-traversee 5 - zonage-ssi 4 - tableau 4 -
  chronologie 2 - planche-chiffree 0 SANS module. VARIER - l'archetype
  se choisit sur la THESE de la fiche, jamais sur le secteur.
- Un mecanisme nouveau s'ecrit DANS le compositeur d'archetype
  (constantes prefixees), et l'invariant octet des planches existantes
  du meme compositeur se rejoue AVANT la greffe, APRES la greffe et
  APRES la passe apostrophes-planches.py, dans une copie hors depot
  (N06 : 20/20 trois fois sur les 5 sankey) ; la passe a courbe des
  apostrophes droites fuies dans les chaines de controles a CHACUNE
  des N03 a N06 - les ecrire courbes des l'ecriture ne suffit pas,
  VERIFIER par la passe en mode mesure avant de composer.
- ARBITRAGE FT2E (N01) : la planche schematise la SOLUTION APPORTEE,
  jamais le deroule de l'affaire. Mecanisme d'INGENIERIE, pas un recit.
- Quand la planche porte les valeurs d'un DCE de prescription et non
  d'un DOE (N05, N06), l'EN-TETE DE REGISTRE nomme la piece et son mois
  (« LES PRODUCTIONS DU DOSSIER DE CONSULTATION · JUILLET 2023 ») et
  l'ecart va en a_valider_ft2e. Toute valeur du dessin reste citable
  dans la fiche.
- N06 : une AFFECTATION deduite par elimination (13 chaudieres = les
  2 T2 + 11 T3, parce que plans et DPGF nomment le reste) va en
  a_valider_ft2e MEME si l'arithmetique est fermee - aucune piece ne
  l'ecrit en toutes lettres.
- N03 : chercher l'EXCEPTION du systeme decrit avant d'ecrire
  « chaque » ou « tous » (N06 : « un coffret par logement du R+1 »
  au CCTP, mais 8 coffrets pour 7 logements a l'etage -> question B).
- N04-N05-N06 : les docx commerciaux peuvent contredire les pieces
  (N06 : « BEE+ » au docx, « BEE » a la synthese RE2020 ; « logements
  individuels » au docx, « collectifs » au calcul) - la piece fait
  foi, l'ecart va en question B.
- Un meme MOA et un meme architecte reviennent de fiche en fiche
  (OPH CDA + BTB : Maubec, L'Houmeau) : differencier la these de la
  fiche voisine avant d'ecrire (N06 : Maubec porte deja « trois
  systemes de chauffage » - L'Houmeau s'est ecrit sur
  l'individualisation, jusqu'au PV par logement).

DEROULER LE PIPELINE § 2 INTEGRALEMENT : depouillement -> releve du
numero NN-NNN sur piece FT2E (gare aux numeros des cotraitants - BF ECO
« 543 » en N06, l'economiste prefixe ses CR de SON numero) ->
references/ref_030/ (3 a 8 pieces) -> croisement commercial
(references/docs_references/ - docx sectoriels, dont « References
logements collectifs - FT2E maj.docx », ET classeur ODS - +
docs/20-source-plaquette-2024.md) -> fiche de collecte (A/A+ remplies,
B-E en questions, ligne Secteur citant le classeur) -> fiche
src/content/projets/<slug>.md (SECTEUR Logements RELEVE AU CLASSEUR -
regle d'indexation sectorielle ci-dessus, points 1 a 5 ; taxonomie
ACTUELLE ; lieu avec code postal entre parentheses ; synthese 480-780
posee par script ; >= 5 liens internes ; jamais de numero d'affaire NI
de millesime d'ouverture en prose) -> PLANCHE complete (extraction avec
a_valider_ft2e non vide, composition par
scripts/planches/<archetype>.py, controles a 1152 / carte 274-296 /
appui 552, PNG 2400x1600, apostrophes-planches.py, verser.py) ->
qualite (typecheck 0, build vert 53 pages, editorial-reviewer,
controle-liens-internes 30/30 a 5, controle-numeros-affaire 0 fuite,
releve-numeral sans ecart nouveau) -> COMMIT UNIQUE
fiche+planche+compositeur (content(references): ajoute la fiche reelle
<nom> ; git ls-remote avant, depot partage) -> push (le push deploie),
curl de la fiche AVEC barre oblique finale + marqueur de build, rendu
controle aux trois bandes (sonde iframe pour les largeurs telephone,
script pret : references/ref_027/sonde-fiche.mjs, URL a adapter) ET
CONTROLE DE L'INDEXATION SECTORIELLE (point 6 : filtre Logements de
/references et page /secteurs/logements - 23-009 sera dans le top 4 du
secteur, sonde references/ref_027/sonde-filtres.mjs) -> ligne de suivi
au plan -> PROMPT DE LA SESSION N08 en annexe du plan (script Python ou
Write, jamais un long heredoc) et reproduit integralement dans le
message final.

PIEGES VERIFIES EN N01-N06 (en plus de ceux des annexes A et B, tous
confirmes) :
- Un heredoc long se fait TRONQUER ou refuser silencieusement - bash
  COMME python : gros fichiers et scripts par l'outil Write PUIS
  execution, avec CONTROLE DE PRESENCE des insecables apres coup
  (seuils calibres sur le texte lui-meme). Un planche.json s'ecrit par
  script Python avec fines et apostrophes construites par
  chr(8239)/chr(8217) - et un .replace pour courber TOUTES les
  apostrophes du contenu, avec assertion d'auto-controle.
- injection-typographique.py ne connait pas l'unite « A » (ampere) :
  poser la fine par remplacement cible apres coup si besoin. Les
  mots-unites epeles se MESURENT au corpus avant correction.
- cairosvg : la copie de controle perd <style> ET l'attribut style de
  la racine (regex avec espace OPTIONNELLE avant style=) ; filets
  8 chiffres a fusionner (#00393A38 -> #C1CFD0, #00393A29 -> #CFDADB,
  #00393A1F -> #D9E2E3) ; U+2192, Δ (U+0394) et Ω (U+03A9) sortent en
  tofu au controle cairosvg mais rendent au navigateur (precedents
  Tourtet, Aurora, Saint-Sauveur).
- PYTHONIOENCODING=utf-8 sur cette machine ; le hook Stop commite et
  pousse SEUL ce qui traine (⚠ livrables/ porte deux fichiers non
  suivis anterieurs a la N02) ; /references/ est gitignore (motif
  ancre) - les pieces sources n'entrent JAMAIS au depot ; npm run
  preview ne mesure pas la performance ; Chrome refuse les fenetres
  sous 500 px (sonde iframe).
- La planche n'expose NI le millesime d'ouverture, NI montant, NI
  tiers (fabricants et marques COMPRIS - les equipements se designent
  par leur fonction) ; tout arbitrage de dessin va dans a_valider_ft2e
  (jamais vide).
- verser.py repond « deja verse » quand `planche:` est ecrit
  directement au frontmatter (fiche neuve) : ses controles 1-3 (cinq
  pieces, extraction, SVG) ont TOURNE avant ce message - c'est un
  succes, pas un refus.

Portee de commit : content(references). Un changement de schema Zod
eventuel passe par le sous-agent content-modeller et va dans le MEME
commit que public/admin/config.yml.

Termine par le prompt de lancement de la session N08, en annexe du
plan du chantier et reproduit integralement dans ton message final -
la regle de continuite est dans CLAUDE.md parce qu'elle a ete manquee
deux fois. Le prompt N08 REPREND le bloc « REGLE D'INDEXATION
SECTORIELLE » ci-dessus tel quel (repartition attendue remise a jour :
apres la N07, L10) : la regle est permanente, elle ne se resume pas.
````


## Annexe H — prompt de lancement de la session N08 (à coller tel quel en session neuve)

````
Session N08/27 - FT2E v3 : chantier des 27 nouvelles fiches references.
Huitieme dossier de la tranche « livraisons 2025 » - PREMIER DES DEUX
DOSSIERS MINCES.

Contexte. FT2E v3 est le site institutionnel du bureau d'etudes FT2E
(La Rochelle), Astro 6 statique, deploye en demonstration client sur
https://ft2e-v3.vercel.app (indexation verrouillee - ne pas y toucher).
Le catalogue porte 30 fiches reelles (23 + Portes-en-Re N01 + Commerces
de Fors N02 + Residence Aurora N03 + Maison de Pierre Loti N04 + Clocher
Saint-Sauveur N05 + EcoQuartier de L'Houmeau N06 + Cite Louise Magnan
N07), chacune illustree d'une planche de schema de principe (cinq pieces
par dossier). Objectif : 50 fiches. 1 session = 1 dossier, close par le
prompt de la suivante.

LIRE D'ABORD, dans cet ordre :
1. docs/superpowers/plans/2026-08-27-chantier-27-nouvelles-fiches.md -
   LE PLAN : § 1 (ce qui a change), § 2 (pipeline 12 etapes), § 3
   (reponses consignees + COMPLEMENT N02 : le classeur de references
   FT2E ; Q3 = REGLE DES DOSSIERS MINCES, defaut reconduit), § Suivi
   (lignes N01 a N07), annexe H (ce prompt).
2. docs/superpowers/plans/2026-08-07-chantier-references-reelles.md -
   § Contraintes globales + § Protocole de session + § Regle des
   dossiers minces (S21-S22 : deux dossiers annonces minces se sont
   reveles complets au depouillement - ne pas conclure sur le compte de
   fichiers).
3. docs/superpowers/specs/2026-08-12-planches-references-protocole.md -
   revision 5 EN ENTIER.
4. CLAUDE.md, .claude/rules/content-collections.md et french-editorial.md.
Etalons : src/content/projets/creche-oranger-perigny.md (fiche) et, pour
une session N complete, src/content/projets/maisons-louise-magnan-la-
rochelle.md + public/images/projets/maisons-louise-magnan-la-rochelle/ +
references/ref_030/ (mecanisme nouveau AVANT/APRES + gabarits
proportionnels) ; pour une fiche d'audit-monotechnique :
src/content/projets/cuisine-groupe-scolaire-villedoux.md (typologie
Etude, secteur Monotechnique - Audit).

REGLE D'INDEXATION SECTORIELLE - etablie le 2026-08-27, A APPLIQUER A
LA REDACTION DE CHAQUE FICHE (etape 6 du pipeline), pas apres coup :
« REFERENCES SITE FT2E.ods » (references/docs_references/, classeur
fourni par FT2E) FAIT FOI pour le classement sectoriel. Concretement,
AVANT d'ecrire le frontmatter :
1. Ouvrir le classeur (python zipfile sur content.xml, ou pandoc) et y
   retrouver l'affaire PAR SON NUMERO (graphie sans tiret : « 23099 »).
2. En relever le domaine (legende : L Logements / T Tertiaire & ERP /
   I Industriel / P Patrimoine / C Coordination SSI /
   M Monotechnique-Audit / E EXE) -> champ `secteur`.
3. Si le classeur porte un domaine DOUBLE (« T § C ») : le premier est
   le `secteur`, le second va au champ `secteur_secondaire` (optionnel
   au schema depuis le 2026-08-27, garde-fou « doit differer ») - la
   fiche parait alors dans les deux filtres et sur les deux pages de
   secteur. Precedents : hotel-yachtman (T § C), maison-pierre-loti-
   rochefort (P § C, N04).
4. JAMAIS de deduction depuis le dossier, l'usage RT ou le nom de
   l'operation : la N02 penchait « Industriel » pour Fors, le classeur
   dit T - et les 25 fiches ont du etre re-referencees le soir meme
   (7 bascules, commits ce334b2/09270a3). Le classeur peut contredire
   l'intuition (Saint-Rogatien, pole commercial : I ; Fors, pole
   commercial : T ; 23083 « plan de comptage Airbus » : E et non M ;
   23099 « CPAM » : M - IRVE, pas T) - il gagne.
5. CONSIGNER la lecture dans la fiche de collecte (ligne « Secteur » :
   citer l'entree du classeur telle quelle) ; si l'affaire est ABSENTE
   du classeur ou son domaine illisible -> question B a FT2E et choix
   provisoire argumente, jamais silencieux.
6. EN RECETTE (etape 10) : verifier sur le deploiement que la fiche
   repond au(x) bon(s) filtre(s) de /references (compteurs de chips)
   et parait sur sa ou ses pages /secteurs/<slug> - sondes precedentes :
   references/ref_030/sonde-filtres.mjs et sonde-fiche.mjs. ⚠ Une page
   /secteurs/<slug> n'affiche que les 4 affaires les plus recentes du
   secteur (tri par numero decroissant) : une affaire ancienne peut
   legitimement n'y pas paraitre (N03 : 19-036 hors du top 4 de
   Logements ; 19-096 idem des que Patrimoine depasse 4 affaires) - le
   filtre de /references, lui, montre tout.
   Repartition attendue AVANT la N08 : L10 T9 I2 P3 C4 M2 E2 pour
   30 fiches (Yachtman T+C et Loti P+C comptent double).

DOSSIER DU JOUR : « 23-099 - CPAM La Rochelle » (25 fichiers), dans
C:\claude_code_dev_projects\ft2e_new_archives\2025.zip (tranche des
livraisons 2025 - liste au § 3 du plan ; le classeur donne « 23099 ·
CPAM · M », Finalisees en 2025 -> secteur Monotechnique - Audit, pas de
domaine double, annee_livraison 2025 ; affaire ouverte en 2023 ->
annee: 2023, millesime d'ouverture jamais en prose). Le § 3 du plan
annote ce dossier « IRVE » (infrastructure de recharge de vehicules
electriques) : NATURE EXACTE DE LA MISSION A ETABLIR SUR PIECES - le
nom du dossier ne fait pas foi. DOSSIER ANNONCE MINCE (25 fichiers) :
appliquer la regle Q3 du § 3 du plan - si la matiere ne porte pas une
fiche honnete (pas de chiffres verifiables, mission trop ponctuelle),
la session produit la fiche de collecte seule + une note au suivi +
une proposition de substitution ; mais VERIFIER AVANT DE CONCLURE : en
2026-08 les deux dossiers minces du programme (Villedoux, Dufour) se
sont reveles complets, et un audit a assez de matiere pour une planche
(Villedoux : coupe-traversee/equilibre). La typologie `Etude` existe
pour une mission sans travaux ; `Audit & diagnostic` est une valeur de
mission_ft2e.
ATTENTION DISQUE (~6 Go libres) : supprimer d'abord le repertoire
extrait de la session precedente (ft2e_new_archives/2025/23-009- 60
maisons Louise Magnan - IAA - os.listdir + startswith('23-009') par
prudence), par python shutil.rmtree (le rm -rf est REFUSE par les
permissions, revecu en N07). Puis extraire LE SEUL dossier du jour
depuis le ZIP PAR PYTHON ZIPFILE (les motifs d'unzip ne matchent PAS
les entrees de ce ZIP) -
  python -c "import zipfile; z=zipfile.ZipFile(r'...\2025.zip');
  z.extractall(r'...\ft2e_new_archives',
  members=[n for n in z.namelist() if '23-099' in n])"
Le ZIP est la source, il ne se supprime pas.
Dossier de travail a creer : references/ref_031/
Slug cible : a etablir au depouillement (kebab-case sans accents,
verifier qu'il n'ecrase rien) - ne pas inclure « cpam » sans avoir
etabli que la CPAM est bien la MOA nommable (question E).

APRES LA N08 il ne restera de la tranche 2025 que 23-083 Airbus comptage
energie (« E », 10 fichiers) ; les tranches suivantes (2024 : 5 affaires,
2023 : 5, 2022 : 4, 2020 : 2, 2019 : 1, d'apres le classeur) seront
fournies par l'utilisateur en nouveaux ZIP - le demander en ouverture
de la N09 si rien n'est fourni.

CE QUE LES N01-N07 ONT ETABLI (verifiable au depot) :
- annee_livraison se pose sur le cadrage de tranche + classeur
  (« Finalisees en 2025 ») ; le PV de reception manque presque
  toujours -> question B1, statut livre. Precedents : PV SSI (N04),
  CR d'OPR (N05), CR annoncant la reception (N06), CR fixant les OPR
  avec 48/60 logements termines (N07 - le titre de section « soixante
  caissons sur soixante toits » a ete RAMENE a ce que la piece
  etablit, sur relecture editoriale).
- Archetypes apres N07 : boucle-fluide 8 - sankey 6 - coupe-traversee 6
  (sortie, Louise Magnan) - zonage-ssi 4 - tableau 4 - chronologie 2 -
  planche-chiffree 0 SANS module. VARIER - l'archetype se choisit sur
  la THESE de la fiche, jamais sur le secteur. Pour une mission de
  comptage ou d'IRVE, tableau-electrique (4) est le candidat naturel
  mais n'est pas un du ; chronologie (2) n'est admissible que sur une
  these d'INGENIERIE.
- Un mecanisme nouveau s'ecrit DANS le compositeur d'archetype
  (constantes prefixees), et l'invariant octet des planches existantes
  du meme compositeur se rejoue AVANT la greffe, APRES la greffe et
  APRES la passe apostrophes-planches.py, dans une copie hors depot
  (N07 : 20/20 trois fois sur les 5 coupe-traversee). N07 : ECRIRE LES
  CHAINES DE CONTROLES COURBES DES L'ECRITURE ET PASSER LE SCRIPT EN
  MODE MESURE AVANT DE COMPOSER a suffi - zero apostrophe fuie, pour la
  premiere fois depuis la N03.
- ARBITRAGE FT2E (N01) : la planche schematise la SOLUTION APPORTEE,
  jamais le deroule de l'affaire. Mecanisme d'INGENIERIE, pas un recit.
  Un registre AVANT/APRES (Sablonceaux, Louise Magnan) n'est pas un
  recit : c'est l'etat que la solution corrige, mis en regard.
- Quand la planche porte les valeurs d'un DCE et non d'un DOE (N05,
  N06, N07), l'EN-TETE DE REGISTRE nomme la piece et son mois et
  l'ecart va en a_valider_ft2e. Toute valeur du dessin reste citable
  dans la fiche.
- N07 : quand aucune surface n'existe au dossier, le cartouche porte la
  grandeur qui compte l'ouvrage (« SOIXANTE MAISONS », comme « TOUR DE
  40 m », « 38 000 m³/h ») - a_valider_ft2e le dit.
- N07 : un tableur d'estimation interne (trois emplacements chiffres
  avec marge) est une piece FT2E citable en fiche, jamais au dessin ;
  un montant de docx commercial non recoupe par une piece se cite avec
  sa source et va en question B.
- N03-N07 : chercher l'EXCEPTION avant d'ecrire « chaque » ou « tous »
  (N07 : DPGF « 24 bouches par typologie » contre 3 bouches par maison
  aux plans -> question B, le dessin n'en montre que trois).
- N04-N07 : les docx commerciaux peuvent contredire les pieces - la
  piece fait foi, l'ecart va en question B.
- Un meme MOA revient de fiche en fiche (Atlantic Amenagement : Louise
  Magnan ; OPH CDA : Maubec, L'Houmeau) : differencier la these de la
  fiche voisine avant d'ecrire.
- N07 : les insecables des heredocs bash sont normalisees DE FACON NON
  DETERMINISTE sur cette machine - un remplacement qui cible un texte
  deja typographie doit construire ses insecables par chr(160)/chr(8239)
  et ASSERTER la presence de l'ancien texte avant d'ecrire ; `$'\u202f'`
  ne produit pas la fine sous ce bash (compter en Python).

DEROULER LE PIPELINE § 2 INTEGRALEMENT : depouillement -> releve du
numero NN-NNN sur piece FT2E (gare aux numeros des cotraitants et du
MOA : IAA « GR 0085 » en N07, BF ECO « 543 » en N06) ->
references/ref_031/ (3 a 8 pieces) -> croisement commercial
(references/docs_references/ - docx sectoriels, dont « Réf.
DIAGNOSTIC.docx » et « Références Rénovation - cvc.docx », ET classeur
ODS - + docs/20-source-plaquette-2024.md) -> fiche de collecte (A/A+
remplies, B-E en questions, ligne Secteur citant le classeur) ->
DECISION Q3 (fiche ou collecte seule) -> fiche
src/content/projets/<slug>.md (SECTEUR Monotechnique - Audit RELEVE AU
CLASSEUR - regle d'indexation sectorielle ci-dessus, points 1 a 5 ;
taxonomie ACTUELLE ; lieu avec code postal entre parentheses ; synthese
480-780 posee par script ; >= 5 liens internes ; jamais de numero
d'affaire NI de millesime d'ouverture en prose) -> PLANCHE complete
(extraction avec a_valider_ft2e non vide, composition par
scripts/planches/<archetype>.py, controles a 1152 / carte 274-296 /
appui 552, PNG 2400x1600, apostrophes-planches.py, verser.py) ->
qualite (typecheck 0, build vert 54 pages, editorial-reviewer,
controle-liens-internes 31/31 a 5, controle-numeros-affaire 0 fuite,
releve-numeral sans ecart nouveau) -> COMMIT UNIQUE
fiche+planche+compositeur (content(references): ajoute la fiche reelle
<nom> ; git ls-remote avant, depot partage) -> push (le push deploie),
curl de la fiche AVEC barre oblique finale + marqueur de build, rendu
controle aux trois bandes (sonde iframe pour les largeurs telephone,
script pret : references/ref_030/sonde-fiche.mjs, URL a adapter) ET
CONTROLE DE L'INDEXATION SECTORIELLE (point 6 : filtre Monotechnique -
Audit de /references et page /secteurs/monotechnique, sonde
references/ref_030/sonde-filtres.mjs) -> ligne de suivi au plan ->
PROMPT DE LA SESSION N09 en annexe du plan (script Python ou Write,
jamais un long heredoc) et reproduit integralement dans le message
final.

PIEGES VERIFIES EN N01-N07 (en plus de ceux des annexes A et B, tous
confirmes) :
- Un heredoc long se fait TRONQUER ou refuser silencieusement - bash
  COMME python : gros fichiers et scripts par l'outil Write PUIS
  execution, avec CONTROLE DE PRESENCE des insecables apres coup
  (seuils calibres sur le texte lui-meme). Un planche.json s'ecrit par
  script Python avec fines et apostrophes construites par
  chr(8239)/chr(8217), un .replace RECURSIF sur toutes les chaines du
  dictionnaire (N07 : une chaine hors de la fonction a() a fait echouer
  l'assertion) et une assertion d'auto-controle. ⚠ Le script s'execute
  DEPUIS LA RACINE DU DEPOT : lance depuis le scratchpad, il y a ecrit
  un public/images/... parasite (N07).
- injection-typographique.py ne connait pas l'unite « A » (ampere) -
  IRVE et comptage en sont pleins : poser la fine par remplacement
  cible apres coup. Les mots-unites epeles se MESURENT au corpus avant
  correction.
- cairosvg : la copie de controle perd <style> ET l'attribut style de
  la racine (regex avec espace OPTIONNELLE avant style=) ; filets
  8 chiffres a fusionner (#00393A38 -> #C1CFD0, #00393A29 -> #CFDADB,
  #00393A1F -> #D9E2E3) ; a 1152 le mono se rend ~7 % trop large et le
  cartouche SEMBLE tronque (N07 : « 202 » pour « 2025 ») - le 2400 et
  le navigateur font foi ; U+2192, Δ et Ω sortent en tofu au controle
  cairosvg mais rendent au navigateur. Script pret dans le scratchpad
  de la N07 (rendre_png.py) - a reecrire si le scratchpad est parti.
- PYTHONIOENCODING=utf-8 sur cette machine ; le hook Stop commite et
  pousse SEUL ce qui traine (⚠ livrables/ porte deux fichiers non
  suivis anterieurs a la N02) ; /references/ est gitignore (motif
  ancre) - les pieces sources n'entrent JAMAIS au depot ; npm run
  preview ne mesure pas la performance ; Chrome refuse les fenetres
  sous 500 px (sonde iframe) ; extract-msg s'installe par pip pour lire
  les .msg (N07).
- La planche n'expose NI le millesime d'ouverture, NI montant, NI
  tiers (fabricants et marques COMPRIS - les equipements se designent
  par leur fonction), NI donnee nominative de locataire ou d'usager ;
  tout arbitrage de dessin va dans a_valider_ft2e (jamais vide).
- verser.py repond « deja verse » quand `planche:` est ecrit
  directement au frontmatter (fiche neuve) : ses controles 1-3 (cinq
  pieces, extraction, SVG) ont TOURNE avant ce message - c'est un
  succes, pas un refus.

Portee de commit : content(references). Un changement de schema Zod
eventuel passe par le sous-agent content-modeller et va dans le MEME
commit que public/admin/config.yml.

Termine par le prompt de lancement de la session N09, en annexe du
plan du chantier et reproduit integralement dans ton message final -
la regle de continuite est dans CLAUDE.md parce qu'elle a ete manquee
deux fois. Le prompt N09 REPREND le bloc « REGLE D'INDEXATION
SECTORIELLE » ci-dessus tel quel (repartition attendue remise a jour :
apres la N08, M3 si la fiche est publiee) : la regle est permanente,
elle ne se resume pas.
````

## Annexe I — prompt de lancement de la session N09 (à coller tel quel en session neuve)

````
Session N09/27 - FT2E v3 : chantier des 27 nouvelles fiches references.
Neuvieme dossier - DERNIER DE LA TRANCHE « livraisons 2025 », SECOND DES
DEUX DOSSIERS MINCES (10 fichiers).

Contexte. FT2E v3 est le site institutionnel du bureau d'etudes FT2E
(La Rochelle), Astro 6 statique, deploye en demonstration client sur
https://ft2e-v3.vercel.app (indexation verrouillee - ne pas y toucher).
Le catalogue porte 31 fiches reelles (23 + Portes-en-Re N01 + Commerces
de Fors N02 + Residence Aurora N03 + Maison de Pierre Loti N04 + Clocher
Saint-Sauveur N05 + EcoQuartier de L'Houmeau N06 + Cite Louise Magnan
N07 + Bornes de recharge La Rochelle et Saintes N08), chacune illustree
d'une planche de schema de principe (cinq pieces par dossier). Objectif :
50 fiches. 1 session = 1 dossier, close par le prompt de la suivante.

LIRE D'ABORD, dans cet ordre :
1. docs/superpowers/plans/2026-08-27-chantier-27-nouvelles-fiches.md -
   LE PLAN : § 1 (ce qui a change), § 2 (pipeline 12 etapes), § 3
   (reponses consignees + COMPLEMENT N02 : le classeur de references
   FT2E ; Q3 = REGLE DES DOSSIERS MINCES, defaut reconduit), § Suivi
   (lignes N01 a N08), annexe I (ce prompt).
2. docs/superpowers/plans/2026-08-07-chantier-references-reelles.md -
   § Contraintes globales + § Protocole de session + § Regle des
   dossiers minces (S21-S22 ET N08 : TROIS dossiers annonces minces se
   sont reveles complets au depouillement - ne jamais conclure sur le
   compte de fichiers).
3. docs/superpowers/specs/2026-08-12-planches-references-protocole.md -
   revision 5 EN ENTIER.
4. CLAUDE.md, .claude/rules/content-collections.md et french-editorial.md.
Etalons : src/content/projets/creche-oranger-perigny.md (fiche) et, pour
une session N complete sur un dossier mince en contrat direct,
src/content/projets/bornes-irve-la-rochelle-saintes.md +
public/images/projets/bornes-irve-la-rochelle-saintes/ +
references/ref_031/ (mecanisme nouveau « mutualisation » du compositeur
tableau-electrique, fiche de collecte avec decision Q3 motivee) ; pour
une fiche d'audit-monotechnique sans travaux :
src/content/projets/cuisine-groupe-scolaire-villedoux.md (typologie
Etude, secteur Monotechnique - Audit).

REGLE D'INDEXATION SECTORIELLE - etablie le 2026-08-27, A APPLIQUER A
LA REDACTION DE CHAQUE FICHE (etape 6 du pipeline), pas apres coup :
« REFERENCES SITE FT2E.ods » (references/docs_references/, classeur
fourni par FT2E) FAIT FOI pour le classement sectoriel. Concretement,
AVANT d'ecrire le frontmatter :
1. Ouvrir le classeur (python zipfile sur content.xml, ou pandoc) et y
   retrouver l'affaire PAR SON NUMERO (graphie sans tiret : « 23083 »).
2. En relever le domaine (legende : L Logements / T Tertiaire & ERP /
   I Industriel / P Patrimoine / C Coordination SSI /
   M Monotechnique-Audit / E EXE) -> champ `secteur`.
3. Si le classeur porte un domaine DOUBLE (« T § C ») : le premier est
   le `secteur`, le second va au champ `secteur_secondaire` (optionnel
   au schema depuis le 2026-08-27, garde-fou « doit differer ») - la
   fiche parait alors dans les deux filtres et sur les deux pages de
   secteur. Precedents : hotel-yachtman (T § C), maison-pierre-loti-
   rochefort (P § C, N04).
4. JAMAIS de deduction depuis le dossier, l'usage RT ou le nom de
   l'operation : la N02 penchait « Industriel » pour Fors, le classeur
   dit T - et les 25 fiches ont du etre re-referencees le soir meme
   (7 bascules, commits ce334b2/09270a3). Le classeur peut contredire
   l'intuition (Saint-Rogatien, pole commercial : I ; Fors, pole
   commercial : T ; 23083 « plan de comptage Airbus » : E et non M ;
   23099 « CPAM » : M - IRVE, pas T) - il gagne.
5. CONSIGNER la lecture dans la fiche de collecte (ligne « Secteur » :
   citer l'entree du classeur telle quelle) ; si l'affaire est ABSENTE
   du classeur ou son domaine illisible -> question B a FT2E et choix
   provisoire argumente, jamais silencieux.
6. EN RECETTE (etape 10) : verifier sur le deploiement que la fiche
   repond au(x) bon(s) filtre(s) de /references (compteurs de chips)
   et parait sur sa ou ses pages /secteurs/<slug> - sondes precedentes :
   references/ref_031/sonde-filtres.mjs et sonde-fiche.mjs. ⚠ Une page
   /secteurs/<slug> n'affiche que les 4 affaires les plus recentes du
   secteur (tri par numero decroissant) : une affaire ancienne peut
   legitimement n'y pas paraitre (N03 : 19-036 hors du top 4 de
   Logements ; 19-096 idem des que Patrimoine depasse 4 affaires) - le
   filtre de /references, lui, montre tout.
   Repartition attendue AVANT la N09 : L10 T9 I2 P3 C4 M3 E2 pour
   31 fiches (Yachtman T+C et Loti P+C comptent double).

DOSSIER DU JOUR : « 23-083- Airbus - Comptage énergie - EQUANS »
(10 fichiers), dans C:\claude_code_dev_projects\ft2e_new_archives\2025.zip
(tranche des livraisons 2025 - liste au § 3 du plan ; le classeur donne
« 23083 · Plan de comptage d'énergie - AIRBUS · E », Finalisees en 2025
-> secteur Etudes d'execution / BIM, PAS Monotechnique malgre l'intuition ;
pas de domaine double ; annee_livraison 2025 ; affaire ouverte en 2023
-> annee: 2023, millesime d'ouverture jamais en prose). « EQUANS » au nom
du dossier est vraisemblablement le DONNEUR D'ORDRES (installateur -
precedent : Ecole des douanes, mission vendue a l'entreprise titulaire
et classee E) : NATURE EXACTE DE LA MISSION ET CHAINE CONTRACTUELLE A
ETABLIR SUR PIECES - le nom du dossier ne fait pas foi, et « Airbus »
n'est peut-etre pas nommable (site industriel, confidentialite -
question E ; ne pas mettre « airbus » dans le slug sans l'avoir etabli,
comme la N08 a tenu « cpam » hors du slug au titre de la clause de
confidentialite du marche de MOE).
DOSSIER ANNONCE MINCE (10 fichiers) : appliquer la regle Q3 du § 3 du
plan - si la matiere ne porte pas une fiche honnete (pas de chiffres
verifiables, mission trop ponctuelle), la session produit la fiche de
collecte seule + une note au suivi + une proposition de substitution ;
mais VERIFIER AVANT DE CONCLURE : Villedoux, Dufour ET la N08 (25
fichiers, fiche complete) ont dementi l'annotation « mince ». Un plan de
comptage a assez de matiere pour une planche si les pieces portent une
arborescence de compteurs (tableau-electrique, mecanisme a creer sur la
THESE - comptage = partition d'une arrivee en usages mesures ?) ou un
bilan de flux (sankey). La typologie `Etudes d'execution` existe ;
`Etude` aussi pour une mission sans travaux.
ATTENTION DISQUE (~6 Go libres) : supprimer d'abord le repertoire
extrait de la session precedente (ft2e_new_archives/2025/23-099 - CPAM
La Rochelle - os.listdir + startswith('23-099') par prudence), par
python shutil.rmtree (le rm -rf est REFUSE par les permissions). Puis
extraire LE SEUL dossier du jour depuis le ZIP PAR PYTHON ZIPFILE (les
motifs d'unzip ne matchent PAS les entrees de ce ZIP) -
  python -c "import zipfile; z=zipfile.ZipFile(r'...\2025.zip');
  z.extractall(r'...\ft2e_new_archives',
  members=[n for n in z.namelist() if '23-083' in n])"
Le ZIP est la source, il ne se supprime pas.
Dossier de travail a creer : references/ref_032/
Slug cible : a etablir au depouillement (kebab-case sans accents,
verifier qu'il n'ecrase rien).

APRES LA N09 la tranche 2025 est EPUISEE (23-075 crèche de Périgny est
deja publiee - ref_001 - et ne produit pas de fiche neuve ; elle peut
seulement repondre a T7). Les tranches suivantes (2024 : 5 affaires -
19110 CDAIR, 20031 UNDERTECH, 21093 Central Hostel, 21095 Voltaero,
23036 Fountaine Pajot -, 2023 : 5, 2022 : 4, 2020 : 2, 2019 : 1, d'apres
le classeur) seront fournies par l'utilisateur en nouveaux ZIP - LES
DEMANDER EN OUVERTURE DE LA N09 si rien n'est fourni, pour que la N10
puisse demarrer sans attendre.

CE QUE LES N01-N08 ONT ETABLI (verifiable au depot) :
- annee_livraison se pose sur le cadrage de tranche + classeur
  (« Finalisees en 2025 ») ; le PV de reception manque presque
  toujours -> question B1, statut livre. Precedents : PV SSI (N04),
  CR d'OPR (N05), CR annoncant la reception (N06), CR fixant les OPR
  (N07), CR fixant les OPR AU 20/12/2024 (N08 - le classeur dit 2025,
  la fiche suit le classeur et B1 demande de corriger en 2024 si la
  reception a ete prononcee avant le 1er janvier : quand une piece et
  le classeur se contredisent sur le millesime, le classeur est suivi
  ET la contradiction est ecrite en B1, jamais tranchee en silence).
- Archetypes apres N08 : boucle-fluide 8 - sankey 6 - coupe-traversee 6
  - tableau-electrique 5 (mutualisation, IRVE) - zonage-ssi 4 -
  chronologie 2 - planche-chiffree 0 SANS module. VARIER - l'archetype
  se choisit sur la THESE de la fiche, jamais sur le secteur. Pour un
  plan de comptage, tableau-electrique vient d'etre employe (N08) :
  sankey (partition d'energie mesuree) ou un mecanisme neuf sont a
  considerer d'abord, chronologie n'est admissible que sur une these
  d'INGENIERIE.
- Un mecanisme nouveau s'ecrit DANS le compositeur d'archetype
  (constantes prefixees), et l'invariant octet des planches existantes
  du meme compositeur se rejoue AVANT la greffe, APRES la greffe et
  APRES la derniere retouche/passe apostrophes, dans une copie hors
  depot (N08 : 16/16 trois fois sur les 4 tableau-electrique). ECRIRE
  LES CHAINES DE CONTROLES COURBES DES L'ECRITURE ET PASSER LE SCRIPT
  EN MODE MESURE AVANT DE COMPOSER : zero apostrophe fuie en N07 et N08.
- N08 : les avances calibrees de _tronc.mesurer (sans-600 = 0,48 em)
  SOUS-MESURENT Archivo 600 wdth 112 au rendu cairosvg d'environ 20 % -
  « BORNE MUTUALISEE » mesure 100 px et affleurait sa boite de 120 :
  laisser 30 px de marge a un libelle sans-600 dans une boite, ou
  regarder le rendu (c'est le temps 3 du protocole, il a servi).
- ARBITRAGE FT2E (N01) : la planche schematise la SOLUTION APPORTEE,
  jamais le deroule de l'affaire. Mecanisme d'INGENIERIE, pas un recit.
  Un registre AVANT/APRES (Sablonceaux, Louise Magnan) ou BESOIN /
  DISTRIBUTION (IRVE) n'est pas un recit : c'est un rapport mis en
  regard.
- Quand la planche porte les valeurs d'un DCE et non d'un DOE (N05 a
  N08), l'EN-TETE DE REGISTRE nomme la piece et son mois et l'ecart va
  en a_valider_ft2e. Toute valeur du dessin reste citable dans la fiche.
- N07-N08 : quand aucune surface n'existe au dossier, le cartouche porte
  la grandeur qui compte l'ouvrage (« SOIXANTE MAISONS », « SEPT POINTS
  DE CHARGE ») - a_valider_ft2e le dit.
- N08 : un CCTP peut se contredire d'un paragraphe a l'autre (7 kW /
  7,4 kW ; 22 kW / 22 kVA) - la fiche retient la valeur majoritaire ET
  l'ecart va en question B ; jamais une moyenne, jamais un silence.
- N08 : un marche de MOE peut porter une CLAUSE DE CONFIDENTIALITE -
  la lire (scans : rendre les pages en PNG par pymupdf et les LIRE, le
  texte n'y est pas), la citer en E1, tenir le nom du MOA hors du slug
  et du titre tant que E1 n'est pas repondu. Les docx commerciaux
  peuvent ne rien porter du tout (N08 : aucune trace de l'affaire hors
  classeur) - le croisement se consigne meme vide.
- Un meme MOA revient de fiche en fiche : differencier la these de la
  fiche voisine avant d'ecrire. Une mission vendue a une ENTREPRISE
  (Ecole des douanes, Joffre/UFA) se dit telle quelle : « mission FT2E
  pour <entreprise> » au champ moa si le MOA final n'est pas partie.
- N07-N08 : les insecables des heredocs bash sont normalisees DE FACON
  NON DETERMINISTE sur cette machine - tout fichier portant des
  insecables s'ecrit par un script Python (Write, puis execution DEPUIS
  LA RACINE DU DEPOT) avec marqueurs ASCII (~ fine, ^ insecable)
  remplaces par chr(8239)/chr(160), assertion d'auto-controle CALIBREE
  SUR LE TEXTE (N08 : un seuil de fines devine a 70 pour 51 posees a
  fait echouer un script juste - compter, pas deviner) et controle de
  presence apres relecture du fichier.

DEROULER LE PIPELINE § 2 INTEGRALEMENT : depouillement -> releve du
numero NN-NNN sur piece FT2E (gare aux numeros des cotraitants, du MOA
et du donneur d'ordres : CPAM « PA 2024-02 » / « PA 2024 - MO01 » en
N08, IAA « GR 0085 » en N07, BF ECO « 543 » en N06) ->
references/ref_032/ (3 a 8 pieces) -> croisement commercial
(references/docs_references/ - docx sectoriels, dont « Réf.
DIAGNOSTIC.docx » et « Références Rénovation - cvc.docx », ET classeur
ODS - + docs/20-source-plaquette-2024.md) -> fiche de collecte (A/A+
remplies, B-E en questions, ligne Secteur citant le classeur, DECISION
Q3 motivee en tete) -> DECISION Q3 (fiche ou collecte seule) -> fiche
src/content/projets/<slug>.md (SECTEUR Etudes d'execution / BIM RELEVE
AU CLASSEUR - regle d'indexation sectorielle ci-dessus, points 1 a 5 ;
taxonomie ACTUELLE ; lieu avec code postal entre parentheses ; synthese
480-780 posee par script ; >= 5 liens internes ; jamais de numero
d'affaire NI de millesime d'ouverture en prose) -> PLANCHE complete
(extraction avec a_valider_ft2e non vide, composition par
scripts/planches/<archetype>.py, controles a 1152 / carte 274-296 /
appui 552, PNG 2400x1600, apostrophes-planches.py, verser.py) ->
qualite (typecheck 0, build vert 55 pages, editorial-reviewer,
controle-liens-internes 32/32 a 5, controle-numeros-affaire 0 fuite,
releve-numeral sans ecart nouveau) -> COMMIT UNIQUE
fiche+planche+compositeur (content(references): ajoute la fiche reelle
<nom> ; git ls-remote avant, depot partage) -> push (le push deploie),
curl de la fiche AVEC barre oblique finale + marqueur de build, rendu
controle aux trois bandes (sonde iframe pour les largeurs telephone,
script pret : references/ref_031/sonde-fiche.mjs, URL a adapter) ET
CONTROLE DE L'INDEXATION SECTORIELLE (point 6 : filtre Etudes
d'execution / BIM de /references et page /secteurs/etudes-execution-bim,
sonde references/ref_031/sonde-filtres.mjs) -> ligne de suivi au plan ->
PROMPT DE LA SESSION N10 en annexe du plan (script Python ou Write,
jamais un long heredoc) et reproduit integralement dans le message
final.

PIEGES VERIFIES EN N01-N08 (en plus de ceux des annexes A et B, tous
confirmes) :
- Un heredoc long se fait TRONQUER ou refuser silencieusement - bash
  COMME python : gros fichiers et scripts par l'outil Write PUIS
  execution, avec CONTROLE DE PRESENCE des insecables apres coup
  (seuils calibres sur le texte lui-meme). Un planche.json s'ecrit par
  script Python avec fines et apostrophes construites par
  chr(8239)/chr(8217), un .replace RECURSIF sur toutes les chaines du
  dictionnaire et une assertion d'auto-controle. ⚠ Le script s'execute
  DEPUIS LA RACINE DU DEPOT : lance depuis le scratchpad, il y a ecrit
  un public/images/... parasite (N07). ⚠ Le cwd du shell PERSISTE d'un
  appel a l'autre : un `cd references/docs_references` ou `cd dist`
  laisse la commande suivante hors racine (N08, deux fois) - chemins
  absolus ou `cd` explicite en tete de chaque commande.
- injection-typographique.py ne connait pas l'unite « A » (ampere) -
  IRVE et comptage en sont pleins : poser la fine DANS le texte source
  (marqueur ~) et controler apres coup par regex que « \d A » ne
  subsiste pas avec une espace ordinaire. Les mots-unites epeles se
  MESURENT au corpus avant correction.
- cairosvg : la copie de controle perd <style> ET l'attribut style de
  la racine (regex avec espace OPTIONNELLE avant style=) ; filets
  8 chiffres a fusionner (#00393A38 -> #C1CFD0, #00393A29 -> #CFDADB,
  #00393A1F -> #D9E2E3) ; a 1152 le mono se rend ~7 % trop large et le
  cartouche SEMBLE tronque (N07-N08 : « 20 » pour « 2025 ») - le 2400
  et le navigateur font foi ; U+2192, Δ et Ω sortent en tofu au controle
  cairosvg mais rendent au navigateur. Script pret dans le scratchpad
  de la N08 (rendre_png.py, copie de celui de la N07) - a reecrire si
  le scratchpad est parti : copie sans <style>, filets fusionnes,
  planche.png 2400x1600 + ctrl-1152 + ctrl-vignette-274/296 +
  ctrl-appui-552.
- Les contrats SCANNES n'ont pas de texte : pdftotext rend vide, il
  faut rendre les pages en PNG (pymupdf, zoom 1,3) et les lire une a
  une - N08 : le marche de MOE signe et sa clause de confidentialite
  n'etaient lisibles qu'ainsi. Les .doc binaires se lisent par antiword
  (installe, PYTHONIOENCODING=utf-8).
- PYTHONIOENCODING=utf-8 sur cette machine ; le hook Stop commite et
  pousse SEUL ce qui traine (⚠ livrables/ porte deux fichiers non
  suivis anterieurs a la N02) ; /references/ est gitignore (motif
  ancre) - les pieces sources n'entrent JAMAIS au depot ; npm run
  preview ne mesure pas la performance ; Chrome refuse les fenetres
  sous 500 px (sonde iframe) ; extract-msg s'installe par pip pour lire
  les .msg (N07).
- La planche n'expose NI le millesime d'ouverture, NI montant, NI
  tiers (fabricants et marques COMPRIS - les equipements se designent
  par leur fonction ; N08 : « type Many de chez Temlab ou equivalent »
  au CCTP, jamais au dessin ni a la fiche), NI donnee nominative ;
  tout arbitrage de dessin va dans a_valider_ft2e (jamais vide).
- verser.py repond « deja verse » quand `planche:` est ecrit
  directement au frontmatter (fiche neuve) : ses controles 1-3 (cinq
  pieces, extraction, SVG) ont TOURNE avant ce message - c'est un
  succes, pas un refus.

Portee de commit : content(references). Un changement de schema Zod
eventuel passe par le sous-agent content-modeller et va dans le MEME
commit que public/admin/config.yml.

Termine par le prompt de lancement de la session N10, en annexe du
plan du chantier et reproduit integralement dans ton message final -
la regle de continuite est dans CLAUDE.md parce qu'elle a ete manquee
deux fois. Le prompt N10 REPREND le bloc « REGLE D'INDEXATION
SECTORIELLE » ci-dessus tel quel (repartition attendue remise a jour :
apres la N09, E3 si la fiche est publiee) : la regle est permanente,
elle ne se resume pas. Si les ZIP des tranches suivantes ne sont pas
fournis, le prompt N10 commence par les DEMANDER.
````

## Annexe J — prompt de lancement de la session N10 (à coller tel quel en session neuve)

````
Session N10/27 - FT2E v3 : chantier des 27 nouvelles fiches references.
Dixieme dossier - PREMIER D'UNE NOUVELLE TRANCHE (la tranche « livraisons
2025 » est EPUISEE depuis la N09).

Contexte. FT2E v3 est le site institutionnel du bureau d'etudes FT2E
(La Rochelle), Astro 6 statique, deploye en demonstration client sur
https://ft2e-v3.vercel.app (indexation verrouillee - ne pas y toucher).
Le catalogue porte 32 fiches reelles (23 + Portes-en-Re N01 + Commerces
de Fors N02 + Residence Aurora N03 + Maison de Pierre Loti N04 + Clocher
Saint-Sauveur N05 + EcoQuartier de L'Houmeau N06 + Cite Louise Magnan
N07 + Bornes de recharge La Rochelle et Saintes N08 + Plan de comptage
Airbus Rochefort N09), chacune illustree d'une planche de schema de
principe (cinq pieces par dossier). Objectif : 50 fiches. 1 session =
1 dossier, close par le prompt de la suivante.

EN OUVERTURE - AVANT TOUTE LECTURE : LE FONDS D'ARCHIVES DE LA SUITE
N'EST PAS FOURNI. Les neuf dossiers publiables de 2025.zip sont traites
(N01 a N09 ; 23-075 y est deja publie, ref_001). D'apres le classeur
« REFERENCES SITE FT2E.ods » (references/docs_references/), les tranches
suivantes sont : « Finalisees en 2024 » (5 affaires : 19110 CDAIR,
20031 UNDERTECH, 21093 Central Hostel, 21095 Voltaero, 23036 Fountaine
Pajot), 2023 (5), 2022 (4), 2020 (2), 2019 (1). SI AUCUN ZIP NOUVEAU
N'EST PRESENT dans C:\claude_code_dev_projects\ft2e_new_archives\
(os.listdir : seul 2025.zip y est attendu), DEMANDER A L'UTILISATEUR
le ZIP de la tranche 2024 (chemin, nom, et l'ordre souhaite - a defaut :
les mieux documentes d'abord, d'apres le compte de fichiers par dossier
lu par zipfile) et S'ARRETER LA : rien ne peut se faire sans les pieces.
Consigner la reponse au § 3 du plan (Q1/Q2, tranche 2024) avant de
derouler.

LIRE ENSUITE, dans cet ordre :
1. docs/superpowers/plans/2026-08-27-chantier-27-nouvelles-fiches.md -
   LE PLAN : § 1 (ce qui a change), § 2 (pipeline 12 etapes), § 3
   (reponses consignees + COMPLEMENT N02 : le classeur de references
   FT2E ; Q3 = REGLE DES DOSSIERS MINCES, defaut reconduit), § Suivi
   (lignes N01 a N09), annexe J (ce prompt).
2. docs/superpowers/plans/2026-08-07-chantier-references-reelles.md -
   § Contraintes globales + § Protocole de session + § Regle des
   dossiers minces (S21-S22, N08 ET N09 : QUATRE dossiers annonces
   minces se sont reveles complets au depouillement - ne jamais
   conclure sur le compte de fichiers ; la N09 en avait 10).
3. docs/superpowers/specs/2026-08-12-planches-references-protocole.md -
   revision 5 EN ENTIER.
4. CLAUDE.md, .claude/rules/content-collections.md et french-editorial.md.
Etalons : src/content/projets/creche-oranger-perigny.md (fiche) et, pour
une session N complete sur un dossier mince en SOUS-TRAITANCE D'UNE
ENTREPRISE (typologie Etude, secteur E),
src/content/projets/plan-comptage-energie-airbus-rochefort.md +
public/images/projets/plan-comptage-energie-airbus-rochefort/ +
references/ref_032/ (mecanisme nouveau « comptage » du compositeur
boucle-fluide, fiche de collecte avec decision Q3 motivee en tete) ;
pour un contrat direct avec un MOA public :
src/content/projets/bornes-irve-la-rochelle-saintes.md + ref_031/.

REGLE D'INDEXATION SECTORIELLE - etablie le 2026-08-27, A APPLIQUER A
LA REDACTION DE CHAQUE FICHE (etape 6 du pipeline), pas apres coup :
« REFERENCES SITE FT2E.ods » (references/docs_references/, classeur
fourni par FT2E) FAIT FOI pour le classement sectoriel. Concretement,
AVANT d'ecrire le frontmatter :
1. Ouvrir le classeur (python zipfile sur content.xml, ou pandoc) et y
   retrouver l'affaire PAR SON NUMERO (graphie sans tiret : « 19110 »).
2. En relever le domaine (legende : L Logements / T Tertiaire & ERP /
   I Industriel / P Patrimoine / C Coordination SSI /
   M Monotechnique-Audit / E EXE) -> champ `secteur`.
3. Si le classeur porte un domaine DOUBLE (« T § C ») : le premier est
   le `secteur`, le second va au champ `secteur_secondaire` (optionnel
   au schema depuis le 2026-08-27, garde-fou « doit differer ») - la
   fiche parait alors dans les deux filtres et sur les deux pages de
   secteur. Precedents : hotel-yachtman (T § C), maison-pierre-loti-
   rochefort (P § C, N04).
4. JAMAIS de deduction depuis le dossier, l'usage RT ou le nom de
   l'operation : la N02 penchait « Industriel » pour Fors, le classeur
   dit T - et les 25 fiches ont du etre re-referencees le soir meme
   (7 bascules, commits ce334b2/09270a3). Le classeur peut contredire
   l'intuition (Saint-Rogatien, pole commercial : I ; Fors, pole
   commercial : T ; 23083 « plan de comptage Airbus » : E et non M -
   confirme en N09, coherent avec l'Ecole des douanes : une mission
   vendue a l'entreprise est classee E ; 23099 « CPAM » : M - IRVE,
   pas T) - il gagne.
5. CONSIGNER la lecture dans la fiche de collecte (ligne « Secteur » :
   citer l'entree du classeur telle quelle) ; si l'affaire est ABSENTE
   du classeur ou son domaine illisible -> question B a FT2E et choix
   provisoire argumente, jamais silencieux.
6. EN RECETTE (etape 10) : verifier sur le deploiement que la fiche
   repond au(x) bon(s) filtre(s) de /references (compteurs de chips)
   et parait sur sa ou ses pages /secteurs/<slug> - sondes precedentes :
   references/ref_032/sonde-filtres.mjs et sonde-fiche.mjs (URL a
   adapter). ⚠ Une page /secteurs/<slug> n'affiche que les 4 affaires
   les plus recentes du secteur (tri par numero decroissant) : une
   affaire ancienne peut legitimement n'y pas paraitre (N03 : 19-036
   hors du top 4 de Logements ; 19-096 idem des que Patrimoine depasse
   4 affaires) - le filtre de /references, lui, montre tout. Les
   affaires 19-xxx et 20-xxx de la tranche 2024 y seront presque
   toutes hors du top 4 : c'est attendu.
   Repartition attendue AVANT la N10 : L10 T9 I2 P3 C4 M3 E3 pour
   32 fiches (Yachtman T+C et Loti P+C comptent double).

DOSSIER DU JOUR : [A ETABLIR AVEC L'UTILISATEUR - tranche 2024, ZIP a
fournir ; par defaut le dossier le mieux documente de la tranche].
ATTENTION DISQUE (~6 Go libres) : supprimer d'abord le repertoire
extrait de la session precedente (ft2e_new_archives/2025/23-083- Airbus
- Comptage energie - EQUANS - os.listdir + startswith('23-083'), par
python shutil.rmtree ; le rm -rf est REFUSE par les permissions). Puis
extraire LE SEUL dossier du jour depuis le nouveau ZIP PAR PYTHON
ZIPFILE (members filtres sur le numero d'affaire - les motifs d'unzip
ne matchent PAS les entrees de ces ZIP, et leurs noms de fichiers
portent des accents encodes en mojibake : passer TOUJOURS par
os.listdir / zipfile.namelist(), jamais par un chemin tape). Le ZIP
est la source, il ne se supprime pas.
Dossier de travail a creer : references/ref_033/
Slug cible : a etablir au depouillement (kebab-case sans accents,
verifier qu'il n'ecrase rien).

CE QUE LES N01-N09 ONT ETABLI (verifiable au depot) :
- annee_livraison se pose sur le classeur (« Finalisees en 2024 » pour
  la tranche suivante) ; quand une piece et le classeur se contredisent
  sur le millesime, le classeur est suivi ET la contradiction est ecrite
  en B1, jamais tranchee en silence (N08 : OPR de decembre 2024 pour
  « 2025 » ; N09 : rapport final d'avril 2024 pour « 2025 »). Le PV de
  reception manque presque toujours -> B1, statut livre.
- Une mission vendue a une ENTREPRISE (Ecole des douanes/Herve
  Thermique, Joffre/UFA, N09 Airbus/Equans) se dit telle quelle au champ
  moa (« Equans - Axima Concept, agence de Perigny, pour le site Airbus
  de Rochefort ») et le classeur la classe E ; la typologie `Etude`
  sert a toute mission sans marche de travaux.
- NOMMER LE CLIENT FINAL : la N09 a etabli Airbus au titre, au slug et
  au recit sur DEUX pieces publiees par FT2E lui-meme (la plaquette
  2024, docs/20-source-plaquette-2024.md § Clients industriels cites, et
  le corpus de cliches des secteurs, src/content/secteurs/*.md - les
  legendes des cliches nomment des affaires : GREP-LES au croisement
  commercial, le site est une source). Un nom deja publie par FT2E se
  reprend, avec E1 ; un nom couvert par une clause de confidentialite
  (N08 CPAM) reste hors slug et hors titre. Aucun nom de tiers ne monte
  jamais sur la planche.
- Archetypes apres N09 : boucle-fluide 9 (comptage, Airbus) - sankey 6
  - coupe-traversee 6 - tableau-electrique 5 - zonage-ssi 4 -
  chronologie 2 - planche-chiffree 0 SANS module. VARIER - l'archetype
  se choisit sur la THESE de la fiche, jamais sur le secteur ; le
  boucle-fluide est le plus employe, le prochain dossier devrait
  chercher ailleurs si sa these le permet.
- Un mecanisme nouveau s'ecrit DANS le compositeur d'archetype
  (constantes prefixees ; garde-fou de greffe sur le NOM DE LA FONCTION
  - « composer_comptage » -, pas sur un mot qui peut deja figurer dans
  le module : la N09 a bute sur « comptage » present ailleurs), et
  l'invariant octet des planches existantes du meme compositeur se
  rejoue AVANT la greffe, APRES la greffe et APRES la derniere retouche,
  dans une copie hors depot (N09 : 32/32 trois fois sur les 8
  boucle-fluide). Quand le dessin somme des marques (7 + 18), une
  ASSERTION dans le compositeur compare la somme dessinee aux totaux de
  l'extraction. ECRIRE LES CHAINES DE CONTROLES COURBES DES L'ECRITURE :
  zero apostrophe fuie en N07, N08 et N09.
- ARBITRAGE FT2E (N01) : la planche schematise la SOLUTION APPORTEE,
  jamais le deroule de l'affaire. Un registre mis en regard (AVANT/APRES,
  BESOIN/DISTRIBUTION, CHAUFFERIE/BILAN DU SITE) n'est pas un recit.
- Les avances calibrees de _tronc.mesurer sous-mesurent Archivo 600 au
  rendu d'environ 20 % (N08, reconfirme N09 : « Chaufferie O » en
  13/600 mesure 75 px et affleurait une boite de 98) - 30 px de marge a
  tout libelle sans-600 dans une boite. Trois etiquettes mono de 38 px
  ne tiennent pas dans 122 px de vignette : n'etiqueter que ce qui
  tient, les valeurs restent au JSON et a la planche.
- Quand aucune surface n'existe au dossier, le cartouche porte la
  grandeur qui compte l'ouvrage (« SOIXANTE MAISONS », « SEPT POINTS DE
  CHARGE », « QUATRE CHAUFFERIES ») - a_valider_ft2e le dit.
- Les insecables des heredocs bash sont normalisees DE FACON NON
  DETERMINISTE sur cette machine - tout fichier portant des insecables
  s'ecrit par un script Python (Write, puis execution DEPUIS LA RACINE
  DU DEPOT) avec marqueurs ASCII (~ fine, ^ insecable) remplaces par
  chr(8239)/chr(160), assertion d'auto-controle CALIBREE SUR LE TEXTE
  (COMPTER les marqueurs du source et comparer a l'egalite - la N09 a
  encore devine un seuil, 10 pour 7 posees, et le script a echoue a
  juste titre) et controle de presence apres relecture du fichier.
  scripts/injection-typographique.py se passe ENSUITE sur la fiche : il
  pose les insecables avant : ; et autour des guillemets que les
  marqueurs n'avaient pas mis (N09 : +28).

DEROULER LE PIPELINE § 2 INTEGRALEMENT : depouillement (pdfinfo /
pdftotext via python subprocess avec les noms lus par os.listdir ; les
plans sans couche texte se lisent en rendant leur cartouche a zoom 3
par pymupdf ; les scans en PNG page a page ; antiword pour les .doc) ->
releve du numero NN-NNN sur piece FT2E (gare aux numeros des
cotraitants et des donneurs d'ordres : Equans « 22984760 » et
« T.1LR.23007-RE » en N09, CPAM « PA 2024 - MO01 » en N08, IAA
« GR 0085 » en N07, BF ECO « 543 » en N06) -> references/ref_033/ (3 a
8 pieces) -> croisement commercial (references/docs_references/ - docx
sectoriels ET classeur ODS - + docs/20-source-plaquette-2024.md + grep
de src/content/ pour ce que le site publie deja) -> fiche de collecte
(A/A+ remplies, B-E en questions, ligne Secteur citant le classeur,
DECISION Q3 motivee en tete) -> DECISION Q3 -> fiche
src/content/projets/<slug>.md (SECTEUR RELEVE AU CLASSEUR ; taxonomie
ACTUELLE ; lieu avec code postal entre parentheses ; synthese 480-780
posee par script ; >= 5 liens internes ; jamais de numero d'affaire NI
de millesime d'ouverture en prose) -> PLANCHE complete (extraction
avec a_valider_ft2e non vide, composition par
scripts/planches/<archetype>.py, controles a 1152 / carte 274-296 /
appui 552 - REGARDER les PNG, deux retouches sur trois ne se voient
qu'au rendu -, PNG 2400x1600, apostrophes-planches.py, verser.py) ->
qualite (typecheck 0, build vert 56 pages, editorial-reviewer,
controle-liens-internes 33/33 a 5, controle-numeros-affaire 0 fuite,
releve-numeral sans ecart nouveau) -> COMMIT UNIQUE
fiche+planche+compositeur (content(references): ajoute la fiche reelle
<nom> ; git ls-remote avant, depot partage) -> push (le push deploie),
curl de la fiche AVEC barre oblique finale + marqueur de build, rendu
controle aux trois bandes (sonde iframe pour les largeurs telephone,
script pret : references/ref_032/sonde-fiche.mjs, URL a adapter) ET
CONTROLE DE L'INDEXATION SECTORIELLE (point 6, sonde
references/ref_032/sonde-filtres.mjs) -> ligne de suivi au plan ->
PROMPT DE LA SESSION N11 en annexe du plan (script Python ou Write,
jamais un long heredoc) et reproduit integralement dans le message
final.

PIEGES VERIFIES EN N01-N09 (en plus de ceux des annexes A et B, tous
confirmes) :
- Un heredoc long se fait TRONQUER ou refuser silencieusement - bash
  COMME python : gros fichiers et scripts par l'outil Write PUIS
  execution, avec CONTROLE DE PRESENCE des insecables apres coup. Le
  script s'execute DEPUIS LA RACINE DU DEPOT ; le cwd du shell PERSISTE
  d'un appel a l'autre (un `cd` vers l'archive laisse le `ls` suivant
  hors racine - N09) : chemins absolus ou `cd` explicite en tete de
  chaque commande.
- Les noms de fichiers des archives portent des accents en mojibake :
  pdftotext lance depuis bash sur un nom tape echoue (« I/O Error »),
  le meme via python subprocess avec os.listdir reussit (N09).
- Un plan PDF sans couche texte (vecteurs vectorises) rend pdftotext
  vide : rendre le cartouche en PNG (pymupdf, clip + zoom 3) et le lire.
- injection-typographique.py ne connait pas l'unite « A » (ampere) :
  poser la fine DANS le texte source et controler apres coup.
- cairosvg : la copie de controle perd <style> ET l'attribut style de
  la racine ; filets 8 chiffres a fusionner (#00393A38 -> #C1CFD0,
  #00393A29 -> #CFDADB, #00393A1F -> #D9E2E3) ; a 1152 le mono se rend
  ~7 % trop large et le cartouche SEMBLE tronque (N07-N09 : « 202 »
  pour « 2025 ») - recadrer le cartouche du PNG 2400 pour trancher, le
  navigateur fait foi ; U+2192, Δ, Ω et le signe moins U+2212 rendent
  au navigateur. Script pret : rendre_png.py dans le scratchpad de la
  N09 (copie de la N08) - a reecrire s'il est parti : copie sans <style>,
  filets fusionnes, planche.png 2400x1600 + ctrl-1152 +
  ctrl-vignette-274/296 + ctrl-appui-552.
- PYTHONIOENCODING=utf-8 sur cette machine ; le hook Stop commite et
  pousse SEUL ce qui traine (⚠ livrables/ porte deux fichiers non
  suivis anterieurs a la N02 - les laisser) ; /references/ est gitignore
  (motif ancre) - les pieces sources n'entrent JAMAIS au depot ; npm run
  preview ne mesure pas la performance ; Chrome refuse les fenetres sous
  500 px (sonde iframe) ; extract-msg s'installe par pip pour les .msg.
- La planche n'expose NI le millesime d'ouverture, NI montant, NI tiers
  (client final, donneur d'ordres, fabricants et marques COMPRIS), NI
  donnee nominative ; les designations internes d'un site (chaufferie
  « O », batiment « D ») sont admises avec une entree a_valider_ft2e et
  une question E ; tout arbitrage de dessin va dans a_valider_ft2e
  (jamais vide).
- verser.py repond « deja verse » quand `planche:` est ecrit
  directement au frontmatter (fiche neuve) : ses controles 1-3 ont
  TOURNE avant ce message - c'est un succes, pas un refus.

Portee de commit : content(references). Un changement de schema Zod
eventuel passe par le sous-agent content-modeller et va dans le MEME
commit que public/admin/config.yml.

Termine par le prompt de lancement de la session N11, en annexe du
plan du chantier et reproduit integralement dans ton message final -
la regle de continuite est dans CLAUDE.md parce qu'elle a ete manquee
deux fois. Le prompt N11 REPREND le bloc « REGLE D'INDEXATION
SECTORIELLE » ci-dessus tel quel (repartition attendue remise a jour) :
la regle est permanente, elle ne se resume pas. Si l'utilisateur a
fourni le ZIP de la tranche 2024 en N10, le prompt N11 nomme le dossier
suivant de cette tranche et son compte de fichiers.
````

## Annexe K — prompt de lancement de la session N11 (à coller tel quel en session neuve)

````
Session N11/27 - FT2E v3 : chantier des 27 nouvelles fiches references.
Onzieme dossier - deuxieme de la tranche « Finalisees en 2024 ».

Contexte. FT2E v3 est le site institutionnel du bureau d'etudes FT2E
(La Rochelle), Astro 6 statique, deploye en demonstration client sur
https://ft2e-v3.vercel.app (indexation verrouillee - ne pas y toucher).
Le catalogue porte 33 fiches reelles (23 + N01 Portes-en-Re + N02 Fors +
N03 Aurora + N04 Loti + N05 Saint-Sauveur + N06 L'Houmeau + N07 Louise
Magnan + N08 bornes IRVE + N09 comptage Airbus + N10 foyer CDAIR),
chacune illustree d'une planche de schema de principe (cinq pieces par
dossier). Objectif : 50 fiches. 1 session = 1 dossier, close par le
prompt de la suivante.

LE FONDS DE LA TRANCHE 2024 EST LIVRE :
C:\claude_code_dev_projects\ft2e_new_archives\2024.zip (472,7 Mo, racine
interne « 2024/ », un repertoire par affaire). La N10 a traite 19-110
CDAIR. Restent, par compte de fichiers decroissant (rappel : ne JAMAIS
conclure « mince » sur ce seul compte - quatre dementis en N08-N09) :
- 159 fichiers, 186 Mo : « 20-031- Projet tertiaire UNDERTECH Médiatim
  -SMART » (classeur : 20031 · T) <- DOSSIER DU JOUR
-  96 fichiers,  78 Mo : « 21-093- Rehab bat rue de l'ESCALE - SMART »
  (21093 · T § C, Central Hostel)
-  72 fichiers,  34 Mo : « 21-095- VOLTAREAO ST AGNANT - Cab SOURD »
  (21095 · I - graphie reelle VoltAero, coquille du nom de dossier)
-  70 fichiers, 110 Mo : « 23-036- Extension bat 5-8 Fountaine Pajot -
  ASP » (23036 · I)

LIRE D'ABORD, dans cet ordre :
1. docs/superpowers/plans/2026-08-27-chantier-27-nouvelles-fiches.md -
   LE PLAN : § 1 (ce qui a change), § 2 (pipeline 12 etapes), § 3
   (reponses consignees Q1/Q2 2024 + complement N02 : le classeur fait
   foi ; Q3 = regle des dossiers minces, defaut reconduit), § Suivi
   (lignes N01 a N10), annexe K (ce prompt).
2. docs/superpowers/plans/2026-08-07-chantier-references-reelles.md -
   § Contraintes globales + § Protocole de session + § Regle des
   dossiers minces.
3. docs/superpowers/specs/2026-08-12-planches-references-protocole.md -
   revision 5 EN ENTIER.
4. CLAUDE.md, .claude/rules/content-collections.md et french-editorial.md.
Etalons : src/content/projets/creche-oranger-perigny.md (fiche) et, pour
une session N de la tranche 2024 (MOA prive ou public, groupement de
MOE, marches et avenants) :
src/content/projets/foyer-cdair-saint-martin-de-re.md +
public/images/projets/foyer-cdair-saint-martin-de-re/ +
references/ref_033/ (fiche de collecte avec decision Q3 motivee en
tete, sondes de recette adaptees).

REGLE D'INDEXATION SECTORIELLE - etablie le 2026-08-27, A APPLIQUER A
LA REDACTION DE CHAQUE FICHE (etape 6 du pipeline), pas apres coup :
« REFERENCES SITE FT2E.ods » (references/docs_references/, classeur
fourni par FT2E) FAIT FOI pour le classement sectoriel. Concretement,
AVANT d'ecrire le frontmatter :
1. Ouvrir le classeur (python zipfile sur content.xml, ou pandoc) et y
   retrouver l'affaire PAR SON NUMERO (graphie sans tiret : « 20031 »).
2. En relever le domaine (legende : L Logements / T Tertiaire & ERP /
   I Industriel / P Patrimoine / C Coordination SSI /
   M Monotechnique-Audit / E EXE) -> champ `secteur`.
3. Si le classeur porte un domaine DOUBLE (« T § C ») : le premier est
   le `secteur`, le second va au champ `secteur_secondaire` (optionnel
   au schema depuis le 2026-08-27, garde-fou « doit differer ») - la
   fiche parait alors dans les deux filtres et sur les deux pages de
   secteur. Precedents : hotel-yachtman (T § C), maison-pierre-loti-
   rochefort (P § C, N04), foyer-cdair-saint-martin-de-re (T § C, N10).
4. JAMAIS de deduction depuis le dossier, l'usage RT ou le nom de
   l'operation : la N02 penchait « Industriel » pour Fors, le classeur
   dit T - et les 25 fiches ont du etre re-referencees le soir meme
   (7 bascules, commits ce334b2/09270a3). Le classeur peut contredire
   l'intuition (Saint-Rogatien, pole commercial : I ; Fors, pole
   commercial : T ; 23083 « plan de comptage Airbus » : E et non M -
   une mission vendue a l'entreprise est classee E ; 23099 « CPAM » :
   M - IRVE, pas T) - il gagne.
5. CONSIGNER la lecture dans la fiche de collecte (ligne « Secteur » :
   citer l'entree du classeur telle quelle) ; si l'affaire est ABSENTE
   du classeur ou son domaine illisible -> question B a FT2E et choix
   provisoire argumente, jamais silencieux.
6. EN RECETTE (etape 10) : verifier sur le deploiement que la fiche
   repond au(x) bon(s) filtre(s) de /references (compteurs de chips)
   et parait sur sa ou ses pages /secteurs/<slug> - sondes :
   references/ref_033/sonde-filtres.mjs et sonde-fiche.mjs (URL a
   adapter). ⚠ Une page /secteurs/<slug> n'affiche que les 4 affaires
   les plus recentes du secteur (tri par numero decroissant) : une
   affaire 20-xxx y sera presque surement hors du top 4 - c'est
   attendu ; le filtre de /references, lui, montre tout.
   Repartition attendue AVANT la N11 : L10 T10 I2 P3 C5 M3 E3 pour
   33 fiches (Yachtman T+C, Loti P+C et le foyer CDAIR T+C comptent
   double).

DOSSIER DU JOUR : « 20-031- Projet tertiaire UNDERTECH Médiatim -SMART »
(159 fichiers, 186,2 Mo), classeur « 20031 · Projet tertiaire La
Pallice UNDERTECH · T ». UNDERTECH est cite par la plaquette 2024
(docs/20-source-plaquette-2024.md) - croisement commercial a faire.
ATTENTION DISQUE (~6 Go libres) : supprimer d'abord le repertoire
extrait de la session precedente -
C:\claude_code_dev_projects\ft2e_new_archives\2024 (le REPERTOIRE, pas
le ZIP ; il contient 2024/19-110 -CDAIR..., l'extraction zipfile
recreant la racine interne du ZIP) - par python shutil.rmtree (le
rm -rf est REFUSE par les permissions). Puis extraire LE SEUL dossier
du jour PAR PYTHON ZIPFILE (members filtres sur « 20-031 » via
zipfile.namelist() - les noms portent des accents en mojibake, ne
JAMAIS taper un chemin). Le ZIP est la source, il ne se supprime pas.
Dossier de travail a creer : references/ref_034/
Slug cible : a etablir au depouillement (kebab-case sans accents,
verifier qu'il n'ecrase rien).

CE QUE LES N01-N10 ONT ETABLI (verifiable au depot) :
- annee_livraison se pose sur le classeur (« Finalisees en 2024 » pour
  cette tranche) ; quand pieces et classeur se contredisent, le
  classeur est suivi ET la contradiction est ecrite en B1, jamais
  tranchee en silence (N10 : reception phase 1 en mai 2023, docx
  « 2023 », phase 2 notifiee 2024, DGD MOE 03/2025 -> B1 avec
  annee_livraison: 2024). Le PV de reception manque presque toujours.
- Les numeros des MANDATAIRES et donneurs d'ordres pietinent les
  pieces : SEMDAS « 2507 » / « 2020/007 » / « 2020/071 », ARCHITEM
  « 1821 » (N10), Equans « 22984760 » (N09), CPAM « PA 2024 - MO01 »
  (N08). Le numero FT2E se releve sur page de garde CCTP (« Affaire
  n° : ... »), etude thermique, contrats et propositions FT2E.
- Un dossier SMART (l'architecte des N03/N08 ?) se depouille comme les
  autres : le numero FT2E d'abord.
- NOMMER LE CLIENT FINAL : un nom deja publie par FT2E (plaquette,
  corpus secteurs, docx sectoriels) se reprend, avec E1 (N09 Airbus,
  N10 CDAIR) ; un nom couvert par une clause de confidentialite reste
  hors slug et hors titre (N08 CPAM). Aucun nom de tiers ne monte
  jamais sur la planche.
- Archetypes apres N10 : boucle-fluide 10 (cascade, CDAIR) - sankey 6
  - coupe-traversee 6 - tableau-electrique 5 - zonage-ssi 4 -
  chronologie 2 - planche-chiffree 0 SANS module. Le boucle-fluide a
  servi en N09 ET N10 : VRAIE dette de variete - chercher la these
  ailleurs si elle le permet (l'archetype se choisit sur la THESE,
  jamais sur le secteur ni sur le quota).
- Un mecanisme nouveau s'ecrit DANS le compositeur d'archetype
  (constantes prefixees ; garde-fou de greffe sur le NOM DE LA
  FONCTION), et l'invariant octet des planches existantes du meme
  compositeur se rejoue AVANT la greffe, APRES la greffe et APRES la
  derniere retouche, dans une copie hors depot (N10 : 36/36 trois fois
  sur les 9 boucle-fluide).
- ECRIRE LES CHAINES COURBES DES L'ECRITURE - extraction planche.json
  COMPRISE : la N10 a laisse 49 apostrophes droites dans son
  extraction ; apostrophes-planches.py --appliquer les a courbees et
  les SVG ont du etre recomposes. Ecrire U+2019 partout des le script
  d'extraction, et passer la mesure AVANT de composer.
- Les avances calibrees de _tronc.mesurer sous-mesurent Archivo 600 au
  rendu d'environ 20 % (N08-N09) - 30 px de marge a tout libelle
  sans-600 dans une boite ; controler() chaque libelle.
- Quand aucune surface n'existe au dossier, le cartouche porte la
  grandeur qui compte l'ouvrage ; N10 avait la SHON des docx
  (1 147 m²) et l'a portee au cartouche avec question B5.
- Les insecables des heredocs bash sont normalisees DE FACON NON
  DETERMINISTE sur cette machine - tout fichier portant des insecables
  s'ecrit par un script Python (Write, puis execution DEPUIS LA RACINE
  DU DEPOT) avec marqueurs ASCII (~ fine, ^ insecable) remplaces par
  chr(8239)/chr(160), assertion d'auto-controle A L'EGALITE comptee
  sur le source (tenu en N10 : 18 fines posees, 18 relues), et
  controle de presence apres relecture. scripts/injection-
  typographique.py se passe ENSUITE sur la fiche (N10 : +21 nbsp).
  ⚠ Il protege les lignes d'enum du frontmatter : une apostrophe
  DROITE tapee dans mission_ft2e y RESTE et casse le build - ecrire
  U+2019 des le script (piege N10, « Études d'exécution »).

DEROULER LE PIPELINE § 2 INTEGRALEMENT : depouillement (pdfinfo /
pdftotext via python subprocess avec les noms lus par os.listdir ; les
plans sans couche texte et les marches scannes se lisent en rendant
leurs pages en PNG par pymupdf, zoom 2-3 ; antiword pour les .doc,
extract-msg pour les .msg) -> releve du numero NN-NNN sur piece FT2E ->
references/ref_034/ (3 a 8 pieces) -> croisement commercial
(references/docs_references/ - docx sectoriels par zipfile+regex sur
word/document.xml, ET classeur ODS - + docs/20-source-plaquette-2024.md
+ grep de src/content/ pour ce que le site publie deja) -> fiche de
collecte (A/A+ remplies, B-E en questions, ligne Secteur citant le
classeur, DECISION Q3 motivee en tete) -> fiche
src/content/projets/<slug>.md (SECTEUR RELEVE AU CLASSEUR ; taxonomie
ACTUELLE ; lieu avec code postal entre parentheses ; synthese 480-780
posee par script ; >= 5 liens internes ; jamais de numero d'affaire NI
de millesime d'ouverture en prose) -> PLANCHE complete (extraction avec
a_valider_ft2e non vide, apostrophes courbes des l'ecriture,
composition par scripts/planches/<archetype>.py, controles a 1152 /
carte 274-296 / appui 552 - REGARDER les PNG -, PNG 2400x1600,
apostrophes-planches.py en MESURE, verser.py) -> qualite (typecheck 0,
build vert 57 pages, editorial-reviewer EN LECTURE SEULE - ses outils
d'edition normalisent les insecables, appliquer ses constats par
script -, controle-liens-internes 34/34 a 5, controle-numeros-affaire
0 fuite, releve-numeral sans ecart nouveau) -> COMMIT UNIQUE
fiche+planche+compositeur (content(references): ajoute la fiche reelle
<nom> et sa planche ; git ls-remote avant, depot partage) -> push (le
push deploie), curl de la fiche AVEC barre oblique finale + marqueur de
build, rendu controle aux trois bandes (sonde iframe pour les largeurs
telephone : references/ref_033/sonde-fiche.mjs, URL a adapter) ET
CONTROLE DE L'INDEXATION SECTORIELLE (point 6, sonde
references/ref_033/sonde-filtres.mjs) -> ligne de suivi au plan ->
PROMPT DE LA SESSION N12 en annexe du plan (script Python ou Write,
jamais un long heredoc) et reproduit integralement dans le message
final. Le prompt N12 REPREND le bloc « REGLE D'INDEXATION
SECTORIELLE » tel quel (repartition remise a jour).

PIEGES VERIFIES EN N01-N10 (en plus de ceux des annexes A et B, tous
confirmes) :
- Un heredoc long se fait TRONQUER ou refuser silencieusement - bash
  COMME python : gros fichiers et scripts par l'outil Write PUIS
  execution ; le cwd du shell PERSISTE d'un appel a l'autre : chemins
  absolus ou cd explicite en tete de chaque commande.
- L'extraction zipfile de 2024.zip RECREE la racine interne : le
  dossier extrait vit sous ft2e_new_archives\2024\2024\<dossier>. Un
  os.listdir qui prend le premier niveau pour le dossier d'affaire
  echoue (piege N10) - toujours descendre par os.listdir.
- cairosvg : la copie de controle perd <style> ET l'attribut style de
  la racine ; ⚠ N10 : l'attribut n'est pas toujours suivi d'une espace
  (racine de vignette `...block">`) - un remplacement a espace finale
  le manque et la vignette rend BLANCHE, sans erreur ; retirer par
  REGEX. Filets 8 chiffres a fusionner (#00393A38 -> #C1CFD0,
  #00393A29 -> #CFDADB, #00393A1F -> #D9E2E3) ; a 1152 le mono se rend
  ~7 % trop large et le cartouche SEMBLE tronque - recadrer le
  cartouche du PNG 2400 pour trancher (N10 : net au 2400), le
  navigateur fait foi. Script pret : rendre_png.py dans le scratchpad
  N10 - a reecrire s'il est parti (copie sans <style>, retrait regex
  du style racine, filets fusionnes, planche.png 2400x1600 +
  ctrl-1152 + ctrl-vignette-274/296 + ctrl-appui-552).
- verser.py repond « deja verse » quand `planche:` est ecrit
  directement au frontmatter (fiche neuve) : ses controles ont TOURNE
  avant ce message - c'est un succes, pas un refus.
- PYTHONIOENCODING=utf-8 sur cette machine ; le hook Stop commite et
  pousse SEUL ce qui traine (⚠ livrables/ porte deux fichiers non
  suivis anterieurs a la N02 - les laisser ; ne pas attendre un agent
  de fond en fin de tour sans avoir commite, piege N09) ;
  /references/ est gitignore (motif ancre) - les pieces sources
  n'entrent JAMAIS au depot ; npm run preview ne mesure pas la
  performance ; Chrome refuse les fenetres sous 500 px (sonde iframe).
- La planche n'expose NI le millesime d'ouverture, NI montant, NI
  tiers (MOA, mandataire, architecte, installateur, MARQUES comprises),
  NI donnee nominative ; les designations internes (FOH, MRS,
  chaufferie « O ») sont admises avec une entree a_valider_ft2e et une
  question E ; tout arbitrage de dessin va dans a_valider_ft2e (jamais
  vide).

Portee de commit : content(references). Un changement de schema Zod
eventuel passe par le sous-agent content-modeller et va dans le MEME
commit que public/admin/config.yml.

Termine par le prompt de lancement de la session N12, en annexe du
plan du chantier et reproduit integralement dans ton message final -
la regle de continuite est dans CLAUDE.md parce qu'elle a ete manquee
deux fois.
````

## Annexe L — prompt de lancement de la session N12 (à coller tel quel en session neuve)

````
Session N12/27 - FT2E v3 : chantier des 27 nouvelles fiches references.
Douzieme dossier - troisieme de la tranche « Finalisees en 2024 ».

Contexte. FT2E v3 est le site institutionnel du bureau d'etudes FT2E
(La Rochelle), Astro 6 statique, deploye en demonstration client sur
https://ft2e-v3.vercel.app (indexation verrouillee - ne pas y toucher).
Le catalogue porte 34 fiches reelles (23 + N01 Portes-en-Re + N02 Fors +
N03 Aurora + N04 Loti + N05 Saint-Sauveur + N06 L'Houmeau + N07 Louise
Magnan + N08 bornes IRVE + N09 comptage Airbus + N10 foyer CDAIR +
N11 parc Undertech), chacune illustree d'une planche de schema de
principe (cinq pieces par dossier). Objectif : 50 fiches. 1 session =
1 dossier, close par le prompt de la suivante.

LE FONDS DE LA TRANCHE 2024 EST LIVRE :
C:\claude_code_dev_projects\ft2e_new_archives\2024.zip (472,7 Mo, racine
interne « 2024/ », un repertoire par affaire). Les N10 et N11 ont traite
19-110 CDAIR et 20-031 UNDERTECH. Restent, par compte de fichiers
decroissant (rappel : ne JAMAIS conclure « mince » sur ce seul compte -
quatre dementis en N08-N09) :
-  96 fichiers, 78 Mo : « 21-093- Rehab bat rue de l'ESCALE - SMART »
   (classeur : 21093 · T § C) <- DOSSIER DU JOUR, l'auberge Central Hostel
-  72 fichiers, 34 Mo : « 21-095- VOLTAREAO ST AGNANT - Cab SOURD »
   (21095 · I - graphie reelle VoltAero, coquille du nom de dossier)
-  70 fichiers, 110 Mo : « 23-036- Extension bat 5-8 Fountaine Pajot -
   ASP » (23036 · I)

LIRE D'ABORD, dans cet ordre :
1. docs/superpowers/plans/2026-08-27-chantier-27-nouvelles-fiches.md -
   LE PLAN : § 1 (ce qui a change), § 2 (pipeline 12 etapes), § 3
   (reponses consignees Q1/Q2 2024 + complement N02 : le classeur fait
   foi ; Q3 = regle des dossiers minces, defaut reconduit), § Suivi
   (lignes N01 a N11), annexe L (ce prompt).
2. docs/superpowers/plans/2026-08-07-chantier-references-reelles.md -
   § Contraintes globales + § Protocole de session + § Regle des
   dossiers minces.
3. docs/superpowers/specs/2026-08-12-planches-references-protocole.md -
   revision 5 EN ENTIER.
4. CLAUDE.md, .claude/rules/content-collections.md et french-editorial.md.
Etalons : src/content/projets/creche-oranger-perigny.md (fiche) et, pour
une session N de la tranche 2024 (MOA prive, groupement de MOE, contrat
d'honoraires a indices multiples) :
src/content/projets/undertech-la-pallice-la-rochelle.md +
public/images/projets/undertech-la-pallice-la-rochelle/ +
references/ref_034/ (fiche de collecte avec decision Q3 motivee en tete).
Les sondes de recette vivent dans references/ref_033/ (sonde-fiche.mjs,
sonde-filtres.mjs - URL a adapter).

REGLE D'INDEXATION SECTORIELLE - etablie le 2026-08-27, A APPLIQUER A
LA REDACTION DE CHAQUE FICHE (etape 6 du pipeline), pas apres coup :
« REFERENCES SITE FT2E.ods » (references/docs_references/, classeur
fourni par FT2E) FAIT FOI pour le classement sectoriel. Concretement,
AVANT d'ecrire le frontmatter :
1. Ouvrir le classeur (python zipfile sur content.xml, ou pandoc) et y
   retrouver l'affaire PAR SON NUMERO (graphie sans tiret : « 21093 »).
2. En relever le domaine (legende : L Logements / T Tertiaire & ERP /
   I Industriel / P Patrimoine / C Coordination SSI /
   M Monotechnique-Audit / E EXE) -> champ `secteur`.
3. Si le classeur porte un domaine DOUBLE (« T § C ») : le premier est
   le `secteur`, le second va au champ `secteur_secondaire` (optionnel
   au schema depuis le 2026-08-27, garde-fou « doit differer ») - la
   fiche parait alors dans les deux filtres et sur les deux pages de
   secteur. Precedents : hotel-yachtman (T § C), maison-pierre-loti-
   rochefort (P § C, N04), foyer-cdair-saint-martin-de-re (T § C, N10).
   ⚠ LE DOSSIER DU JOUR EST DANS CE CAS : 21093 est « T § C ».
4. JAMAIS de deduction depuis le dossier, l'usage RT ou le nom de
   l'operation : la N02 penchait « Industriel » pour Fors, le classeur
   dit T - et les 25 fiches ont du etre re-referencees le soir meme
   (7 bascules, commits ce334b2/09270a3). Le classeur peut contredire
   l'intuition (Saint-Rogatien, pole commercial : I ; Fors, pole
   commercial : T ; 23083 « plan de comptage Airbus » : E et non M -
   une mission vendue a l'entreprise est classee E ; 23099 « CPAM » :
   M - IRVE, pas T) - il gagne.
5. CONSIGNER la lecture dans la fiche de collecte (ligne « Secteur » :
   citer l'entree du classeur telle quelle) ; si l'affaire est ABSENTE
   du classeur ou son domaine illisible -> question B a FT2E et choix
   provisoire argumente, jamais silencieux.
6. EN RECETTE (etape 10) : verifier sur le deploiement que la fiche
   repond au(x) bon(s) filtre(s) de /references (compteurs de chips)
   et parait sur sa ou ses pages /secteurs/<slug> - sondes :
   references/ref_033/sonde-filtres.mjs et sonde-fiche.mjs (URL a
   adapter). ⚠ Une page /secteurs/<slug> n'affiche que les 4 affaires
   les plus recentes du secteur (tri par numero decroissant) : une
   affaire 21-xxx y sera presque surement hors du top 4 - c'est
   attendu ; le filtre de /references, lui, montre tout.
   Repartition attendue AVANT la N12 : L10 T11 I2 P3 C5 M3 E3 pour
   34 fiches, 37 en pondere (Yachtman T+C, Loti P+C et le foyer CDAIR
   T+C comptent double).

DOSSIER DU JOUR : « 21-093- Rehab bat rue de l'ESCALE - SMART »
(96 fichiers, 78 Mo), classeur « 21093 · T § C ». Il s'agit tres
probablement de l'auberge CENTRAL HOSTEL, que la plaquette 2024 cite
(docs/20-source-plaquette-2024.md : « Auberge Central Hostel |
La Rochelle | 2022 | CFO/CFA ») - croisement commercial a faire, et
verification que le batiment de la rue de l'Escale est bien celui-la.
L'architecte SMART Architecture est le meme qu'en N03 (Aurora) et
N11 (Undertech) : graphie deja harmonisee « SMART Architecture
(Nieul-sur-Mer) ».
ATTENTION DISQUE (~6 Go libres) : supprimer d'abord le repertoire
extrait de la session precedente -
C:\claude_code_dev_projects\ft2e_new_archives\2024 (le REPERTOIRE, pas
le ZIP ; il contient 2024/20-031- Projet tertiaire UNDERTECH...,
l'extraction zipfile recreant la racine interne du ZIP) - par python
shutil.rmtree (le rm -rf est REFUSE par les permissions). Puis extraire
LE SEUL dossier du jour PAR PYTHON ZIPFILE (members filtres sur
« 21-093 » via zipfile.namelist() - les noms portent des accents en
mojibake, ne JAMAIS taper un chemin). Le ZIP est la source, il ne se
supprime pas.
Dossier de travail a creer : references/ref_035/
Slug cible : a etablir au depouillement (kebab-case sans accents,
verifier qu'il n'ecrase rien).

CE QUE LES N01-N11 ONT ETABLI (verifiable au depot) :
- annee_livraison se pose sur le classeur (« Finalisees en 2024 » pour
  cette tranche) ; quand pieces et classeur se contredisent, le
  classeur est suivi ET la contradiction est ecrite en B1, jamais
  tranchee en silence. Le PV de reception manque presque toujours -
  mais l'etai peut etre solide sans lui : en N11, un CR d'OPC portait
  en tete « RECEPTION DES TRAVAUX, ensemble des entreprises convoque »
  avec sa date, et les CR suivants ne traitaient plus que des levees
  de reserves. CHERCHER CE CR-LA plutot que le seul PV.
- Le numero FT2E se releve sur page de garde CCTP (« Affaire n° : ... »),
  etude thermique (pied de chaque page), contrats et propositions FT2E.
  ⚠ N11 : la proposition d'honoraires INITIALE portait le numero 20-031
  ET la date du 26 mai 2019, alors que le numero encode 2020 et que
  l'indice A est de juillet 2020 - contradiction consignee en B, jamais
  tranchee en silence, et `annee` suit le numero (le schema l'impose).
- Les numeros des MANDATAIRES et donneurs d'ordres pietinent les
  pieces : SEMDAS « 2507 » / « 2020/007 » / « 2020/071 », ARCHITEM
  « 1821 » (N10), Equans « 22984760 » (N09), CPAM « PA 2024 - MO01 »
  (N08).
- ⚠ UN CCTP PEUT SE CONTREDIRE EN INTERNE (N11) : le lot photovoltaique
  des ateliers annoncait un perimetre au § 2.2 et en dimensionnait un
  autre au § 3.3, avec une 3e colonne de DPGF non dimensionnee. Retenir
  le paragraphe QUI DENOMBRE, l'ecrire dans a_valider_ft2e, en faire
  une question B - et ne publier en prose aucun compte contradictoire
  (N11 : 18 locaux au DCE, 22 aux CR, « 13 ateliers et 3 immeubles » au
  docx -> la fiche ne donne aucun compte, la question B le porte).
- NOMMER LE CLIENT FINAL : un nom deja publie par FT2E (plaquette,
  corpus secteurs, docx sectoriels) se reprend, avec E1 (N09 Airbus,
  N10 CDAIR, N11 Undertech) ; un nom couvert par une clause de
  confidentialite reste hors slug et hors titre (N08 CPAM). Aucun nom
  de tiers ne monte jamais sur la planche.
- Archetypes apres N11 : boucle-fluide 10 - sankey 6 - coupe-traversee 6
  - tableau-electrique 6 (regimes, Undertech) - zonage-ssi 4 -
  chronologie 2 - planche-chiffree 0 SANS module. Le boucle-fluide a
  servi en N09 ET N10 : la dette de variete demeure sur lui -
  l'archetype se choisit sur la THESE, jamais sur le secteur ni sur le
  quota, mais a these egale preferer ce qui n'a pas servi depuis
  longtemps (chronologie-affaire n'a pas servi depuis le corpus
  fondateur, et n'est admissible que si sa these est d'INGENIERIE).
- Un mecanisme nouveau s'ecrit DANS le compositeur d'archetype
  (constantes prefixees ; garde-fou de greffe sur le NOM DE LA
  FONCTION), et l'invariant octet des planches existantes du meme
  compositeur se rejoue AVANT la greffe, APRES la greffe et APRES la
  derniere retouche, dans une copie hors depot (N11 : 15/15 avant,
  18/18 apres sur 6 planches).
- ECRIRE LES CHAINES COURBES DES L'ECRITURE - extraction planche.json
  COMPRISE. ⚠ La N10 avait laisse 49 apostrophes droites ; la N11 a
  tenu la discipline et apostrophes-planches.py n'a RIEN courbe.
  La recette : une assertion `"'" not in sortie` dans le script
  d'extraction lui-meme, avant ecriture. La refaire.
- Les avances calibrees de _tronc.mesurer sous-mesurent Archivo 600 au
  rendu d'environ 20 % (N08-N09) - 30 px de marge a tout libelle
  sans-600 dans une boite ; controler() chaque libelle.
- REGARDER LES PNG, ET CORRIGER CE QU'ON Y VOIT. La N11 a fait trois
  retouches que ni le build ni les controles n'auraient signalees :
  un bandeau de mesure laisse en calcaire se lit comme un CADRE VIDE
  (passe en aplat clair), un texte aligne sur le bord du registre
  alors que les mesures sont en retrait fait ZIGZAGUER la lecture
  (aligne sur la colonne des mesures), et une ligne posee 16 px sous
  un bloc COLLE a ce bloc (descendue de 10 px).
- Quand aucune surface n'existe au dossier, le cartouche porte la
  grandeur qui compte l'ouvrage ; quand deux sources donnent deux
  surfaces, publier celle qui couvre l'operation entiere et poser la
  question B (N11 : 10 093 m2 du docx contre 3 351 m2 de la synthese
  RT, qui ne calculait que deux batiments sur trois).
- Les insecables des heredocs bash sont normalisees DE FACON NON
  DETERMINISTE sur cette machine - tout fichier portant des insecables
  s'ecrit par un script Python (Write, puis execution DEPUIS LA RACINE
  DU DEPOT) avec marqueurs ASCII (~ fine, ^ insecable) remplaces par
  chr(8239)/chr(160), assertion d'auto-controle A L'EGALITE comptee
  sur le source (tenu en N11 : 27 fines posees, 27 relues), et
  controle de PRESENCE apres relecture. scripts/injection-
  typographique.py se passe ENSUITE sur la fiche (N11 : +19 nbsp).
  ⚠ Il protege les lignes d'enum du frontmatter : une apostrophe
  DROITE tapee dans mission_ft2e y RESTE et casse le build - ecrire
  U+2019 des le script (piege N10, « Études d'exécution »).

DEROULER LE PIPELINE § 2 INTEGRALEMENT : depouillement (pdfinfo /
pdftotext via python subprocess avec les noms lus par os.listdir ; les
plans sans couche texte et les marches scannes se lisent en rendant
leurs pages en PNG par pymupdf, zoom 2-3 ; antiword pour les .doc,
extract-msg pour les .msg) -> releve du numero NN-NNN sur piece FT2E ->
references/ref_035/ (3 a 8 pieces) -> croisement commercial
(references/docs_references/ - docx sectoriels par zipfile+regex sur
word/document.xml, ET classeur ODS - + docs/20-source-plaquette-2024.md
+ grep de src/content/ pour ce que le site publie deja) -> fiche de
collecte (A/A+ remplies, B-E en questions, ligne Secteur citant le
classeur, DECISION Q3 motivee en tete) -> fiche
src/content/projets/<slug>.md (SECTEUR ET SECTEUR_SECONDAIRE RELEVES AU
CLASSEUR ; taxonomie ACTUELLE ; lieu avec code postal entre
parentheses ; synthese 480-780 posee par script ; >= 5 liens internes ;
jamais de numero d'affaire NI de millesime d'ouverture en prose) ->
PLANCHE complete (extraction avec a_valider_ft2e non vide, apostrophes
courbes des l'ecriture, composition par scripts/planches/<archetype>.py,
controles a 1152 / carte 274-296 / appui 552 - REGARDER les PNG -,
PNG 2400x1600, apostrophes-planches.py en MESURE, verser.py) ->
qualite (typecheck 0, build vert 58 pages, editorial-reviewer EN
LECTURE SEULE - ses outils d'edition normalisent les insecables,
appliquer ses constats par script -, controle-liens-internes 35/35 a 5,
controle-numeros-affaire 0 fuite, releve-numeral sans ecart nouveau) ->
COMMIT UNIQUE fiche+planche+compositeur (content(references): ajoute la
fiche reelle <nom> et sa planche ; git ls-remote avant, depot partage)
-> push (le push deploie), curl de la fiche AVEC barre oblique finale +
marqueur de build, rendu controle aux trois bandes (sonde iframe pour
les largeurs telephone : references/ref_033/sonde-fiche.mjs, URL a
adapter) ET CONTROLE DE L'INDEXATION SECTORIELLE (point 6, sonde
references/ref_033/sonde-filtres.mjs - LES DEUX filtres, l'affaire
etant a domaine double) -> ligne de suivi au plan -> PROMPT DE LA
SESSION N13 en annexe du plan (script Python ou Write, jamais un long
heredoc) et reproduit integralement dans le message final. Le prompt
N13 REPREND le bloc « REGLE D'INDEXATION SECTORIELLE » tel quel
(repartition remise a jour).

PIEGES VERIFIES EN N01-N11 (en plus de ceux des annexes A et B, tous
confirmes) :
- Un heredoc long se fait TRONQUER ou refuser silencieusement - bash
  COMME python : gros fichiers et scripts par l'outil Write PUIS
  execution ; le cwd du shell PERSISTE d'un appel a l'autre : chemins
  absolus ou cd explicite en tete de chaque commande.
- L'extraction zipfile de 2024.zip RECREE la racine interne : le
  dossier extrait vit sous ft2e_new_archives\2024\2024\<dossier>. Un
  os.listdir qui prend le premier niveau pour le dossier d'affaire
  echoue (piege N10) - toujours descendre par os.listdir.
- cairosvg : la copie de controle perd <style> ET l'attribut style de
  la racine ; ⚠ l'attribut n'est pas toujours suivi d'une espace
  (racine de vignette `...block">`) - un remplacement a espace finale
  le manque et la vignette rend BLANCHE, sans erreur ; retirer par
  REGEX (`re.sub(r'\sstyle="[^"]*"', "", svg, count=1)`). Filets
  8 chiffres a fusionner (#00393A38 -> #C1CFD0, #00393A29 -> #CFDADB,
  #00393A1F -> #D9E2E3) ; a 1152 le mono se rend ~7 % trop large et le
  cartouche SEMBLE tronque - recadrer le cartouche du PNG 2400 pour
  trancher, le navigateur fait foi. Script pret : rendre_png.py, a
  reecrire s'il est parti (il l'etait en N11 - 45 lignes, un quart
  d'heure).
- verser.py repond « deja verse » quand `planche:` est ecrit
  directement au frontmatter (fiche neuve) : ses controles 1 a 3 - les
  cinq pieces, l'archetype nomme, a_valider_ft2e non vide, le SVG sous
  40 Ko avec role="img" et sans width/height - ont TOUS tourne avant
  ce message (verifie en lisant le script en N11). C'est un succes.
- PYTHONIOENCODING=utf-8 sur cette machine, et `python -c` sans lui
  plante en UnicodeEncodeError sur la moindre insecable ; le hook Stop
  commite et pousse SEUL ce qui traine (⚠ livrables/ porte deux
  fichiers non suivis anterieurs a la N02 - les laisser ; ne pas
  attendre un agent de fond en fin de tour sans avoir commite, piege
  N09) ; /references/ est gitignore (motif ancre) - les pieces sources
  n'entrent JAMAIS au depot ; npm run preview ne mesure pas la
  performance ; Chrome refuse les fenetres sous 500 px (sonde iframe).
- La planche n'expose NI le millesime d'ouverture, NI montant, NI
  tiers (MOA, mandataire, architecte, installateur, MARQUES comprises),
  NI donnee nominative ; les designations internes sont admises avec
  une entree a_valider_ft2e et une question E ; tout arbitrage de
  dessin va dans a_valider_ft2e (jamais vide).

Portee de commit : content(references). Un changement de schema Zod
eventuel passe par le sous-agent content-modeller et va dans le MEME
commit que public/admin/config.yml.

Termine par le prompt de lancement de la session N13, en annexe du
plan du chantier et reproduit integralement dans ton message final -
la regle de continuite est dans CLAUDE.md parce qu'elle a ete manquee
deux fois.
````

## Annexe M — prompt de lancement de la session N13 (à coller tel quel en session neuve)

```
Session N13/27 - FT2E v3 : chantier des 27 nouvelles fiches references.
Treizieme dossier - quatrieme de la tranche « Finalisees en 2024 ».

Contexte. FT2E v3 est le site institutionnel du bureau d'etudes FT2E
(La Rochelle), Astro 6 statique, deploye en demonstration client sur
https://ft2e-v3.vercel.app (indexation verrouillee - ne pas y toucher).
Le catalogue porte 35 fiches reelles (23 + N01 Portes-en-Re + N02 Fors +
N03 Aurora + N04 Loti + N05 Saint-Sauveur + N06 L'Houmeau + N07 Louise
Magnan + N08 bornes IRVE + N09 comptage Airbus + N10 foyer CDAIR +
N11 parc Undertech + N12 auberge Central Hostel), chacune illustree
d'une planche de schema de principe (cinq pieces par dossier). Objectif :
50 fiches. 1 session = 1 dossier, close par le prompt de la suivante.

LE FONDS DE LA TRANCHE 2024 EST LIVRE :
C:\claude_code_dev_projects\ft2e_new_archives\2024.zip (472,7 Mo, racine
interne « 2024/ », un repertoire par affaire). Les N10, N11 et N12 ont
traite 19-110 CDAIR, 20-031 UNDERTECH et 21-093 Central Hostel. Restent
deux dossiers, par compte de fichiers decroissant (rappel : ne JAMAIS
conclure « mince » sur ce seul compte - quatre dementis en N08-N09) :
-  72 fichiers, 34 Mo : « 21-095- VOLTAREAO ST AGNANT - Cab SOURD »
   (classeur : 21095 · I - graphie reelle VoltAero, coquille du nom de
   dossier ET de la plaquette) <- DOSSIER DU JOUR
-  70 fichiers, 110 Mo : « 23-036- Extension bat 5-8 Fountaine Pajot -
   ASP » (23036 · I)
La tranche 2024 sera CLOSE a la fin de la N14 : prevoir de demander a
l'utilisateur, en ouverture de la N14, le ZIP de la tranche suivante
(2023 : 5 dossiers au classeur - 20045 THE ROOF, 20071 Bureaux EIFFAGE,
21029 Ecole La Flotte, et deux autres a relire au classeur).

LIRE D'ABORD, dans cet ordre :
1. docs/superpowers/plans/2026-08-27-chantier-27-nouvelles-fiches.md -
   LE PLAN : § 1 (ce qui a change), § 2 (pipeline 12 etapes), § 3
   (reponses consignees Q1/Q2 2024 + complement N02 : le classeur fait
   foi ; Q3 = regle des dossiers minces, defaut reconduit), § Suivi
   (lignes N01 a N12), annexe M (ce prompt).
2. docs/superpowers/plans/2026-08-07-chantier-references-reelles.md -
   § Contraintes globales + § Protocole de session + § Regle des
   dossiers minces.
3. docs/superpowers/specs/2026-08-12-planches-references-protocole.md -
   revision 5 EN ENTIER.
4. CLAUDE.md, .claude/rules/content-collections.md et french-editorial.md.
Etalons : src/content/projets/creche-oranger-perigny.md (fiche) et, pour
une session de la tranche 2024 a MOA privee et domaine double :
src/content/projets/auberge-central-hostel-la-rochelle.md +
public/images/projets/auberge-central-hostel-la-rochelle/ +
references/ref_035/ (fiche de collecte avec decision Q3 motivee en tete).
Les sondes de recette vivent dans references/ref_033/ (sonde-fiche.mjs,
sonde-filtres.mjs - URL a adapter).

REGLE D'INDEXATION SECTORIELLE - etablie le 2026-08-27, A APPLIQUER A
LA REDACTION DE CHAQUE FICHE (etape 6 du pipeline), pas apres coup :
« REFERENCES SITE FT2E.ods » (references/docs_references/, classeur
fourni par FT2E) FAIT FOI pour le classement sectoriel. Concretement,
AVANT d'ecrire le frontmatter :
1. Ouvrir le classeur (python zipfile sur content.xml, ou pandoc) et y
   retrouver l'affaire PAR SON NUMERO (graphie sans tiret : « 21095 »).
2. En relever le domaine (legende : L Logements / T Tertiaire & ERP /
   I Industriel / P Patrimoine / C Coordination SSI /
   M Monotechnique-Audit / E EXE) -> champ `secteur`.
3. Si le classeur porte un domaine DOUBLE (« T § C ») : le premier est
   le `secteur`, le second va au champ `secteur_secondaire` (optionnel
   au schema depuis le 2026-08-27, garde-fou « doit differer ») - la
   fiche parait alors dans les deux filtres et sur les deux pages de
   secteur. Precedents : hotel-yachtman (T § C), maison-pierre-loti-
   rochefort (P § C, N04), foyer-cdair-saint-martin-de-re (T § C, N10),
   auberge-central-hostel-la-rochelle (T § C, N12).
   Le dossier du jour, lui, est a domaine SIMPLE : 21095 est « I ».
4. JAMAIS de deduction depuis le dossier, l'usage RT ou le nom de
   l'operation : la N02 penchait « Industriel » pour Fors, le classeur
   dit T - et les 25 fiches ont du etre re-referencees le soir meme
   (7 bascules, commits ce334b2/09270a3). Le classeur peut contredire
   l'intuition (Saint-Rogatien, pole commercial : I ; Fors, pole
   commercial : T ; 23083 « plan de comptage Airbus » : E et non M -
   une mission vendue a l'entreprise est classee E ; 23099 « CPAM » :
   M - IRVE, pas T) - il gagne.
5. CONSIGNER la lecture dans la fiche de collecte (ligne « Secteur » :
   citer l'entree du classeur telle quelle) ; si l'affaire est ABSENTE
   du classeur ou son domaine illisible -> question B a FT2E et choix
   provisoire argumente, jamais silencieux.
6. EN RECETTE (etape 10) : verifier sur le deploiement que la fiche
   repond au bon filtre de /references (compteurs de chips) et parait
   sur sa page /secteurs/<slug> - sondes : references/ref_033/
   sonde-filtres.mjs et sonde-fiche.mjs (URL a adapter).
   ⚠ Une page /secteurs/<slug> n'affiche que les 4 affaires les plus
   recentes du secteur (tri par numero decroissant) : une affaire 21-xxx
   y sera peut-etre hors du top 4 - c'est attendu ; le filtre de
   /references, lui, montre tout. ⚠ MAIS le secteur Industriel ne compte
   aujourd'hui que DEUX fiches : la fiche du jour y sera visible a coup
   sur, et elle porte le secteur le plus creux du catalogue.
   Repartition attendue AVANT la N13 : L10 T12 I2 P3 C6 M3 E3 pour
   35 fiches, 39 en pondere (Yachtman T+C, Loti P+C, foyer CDAIR T+C et
   Central Hostel T+C comptent double).

DOSSIER DU JOUR : « 21-095- VOLTAREAO ST AGNANT - Cab SOURD »
(72 fichiers, 34 Mo), classeur « 21095 · Batiment industriel Voltaero
St Agnant · I ». VoltAero est le constructeur aeronautique de l'avion
hybride Cassio, installe sur l'aerodrome de Rochefort-Saint-Agnant : le
nom est deja publie par FT2E (plaquette 2024, a verifier au grep de
docs/20-source-plaquette-2024.md - la graphie y est peut-etre fautive
« Voltareo »/« Voltaero », a corriger dans la fiche et a signaler en
question B). Croisement commercial a faire dans
references/docs_references/ (docx sectoriels par zipfile+regex sur
word/document.xml). L'architecte « Cab SOURD » (cabinet Sourd) n'est
apparu dans aucune fiche publiee : relever sa graphie exacte sur la page
de garde des CCTP et l'harmoniser comme SMART Architecture l'a ete.
⚠ Saint-Agnant porte DEJA une fiche au catalogue :
residence-intergenerationnelle-saint-agnant - verifier que le slug du
jour ne prete pas a confusion (proposer par exemple
batiment-industriel-voltaero-saint-agnant).
ATTENTION DISQUE (~7 Go libres) : supprimer d'abord le repertoire
extrait de la session precedente -
C:\claude_code_dev_projects\ft2e_new_archives\2024 (le REPERTOIRE, pas
le ZIP ; il contient 2024/21-093- Rehab bat rue de l'ESCALE - SMART,
l'extraction zipfile recreant la racine interne du ZIP) - par python
shutil.rmtree (le rm -rf est REFUSE par les permissions). Puis extraire
LE SEUL dossier du jour PAR PYTHON ZIPFILE (members filtres sur
« 21-095 » via zipfile.namelist() - les noms portent des accents en
mojibake, ne JAMAIS taper un chemin). Le ZIP est la source, il ne se
supprime pas.
Dossier de travail a creer : references/ref_036/
Slug cible : a etablir au depouillement (kebab-case sans accents,
verifier qu'il n'ecrase rien).

CE QUE LES N01-N12 ONT ETABLI (verifiable au depot) :
- annee_livraison se pose sur le classeur (« Finalisees en 2024 » pour
  cette tranche) ; quand pieces et classeur se contredisent, le
  classeur est suivi ET la contradiction est ecrite en B1, jamais
  tranchee en silence. Le PV de reception manque presque toujours -
  mais l'etai peut etre solide sans lui, et il se cherche a TROIS
  endroits : un CR d'OPC portant « RECEPTION DES TRAVAUX » en tete
  (N11), un CR annoncant la reception a une date precise avec le
  planning des semaines suivantes (N12 : « la reception est prevu le
  16 avril », S17 commission de securite, S18 ouverture), et le BILAN
  DE FACTURATION - les honoraires d'AOR et de reception SSI ne se
  facturent qu'une fois la mission finie (N12 : 27/06/2024).
- Le numero FT2E se releve sur page de garde CCTP (« Affaire n° : ... »),
  etude thermique (pied de chaque page), contrats et propositions FT2E.
  ⚠ N12 : la premiere proposition (18/10/2021) est etablie au nom d'une
  autre entite que l'indice A (20/10/2021) a la MEME adresse - lire
  TOUS les indices, ne pas s'arreter au premier PDF trouve.
- Les numeros des MANDATAIRES et donneurs d'ordres pietinent les
  pieces : SEMDAS « 2507 » / « 2020/007 » / « 2020/071 », ARCHITEM
  « 1821 » (N10), Equans « 22984760 » (N09), CPAM « PA 2024 - MO01 »
  (N08). Les CR d'OPC, eux, sont souvent indexes par numero de reunion
  seulement (N11, N12).
- ⚠ UN CCTP PEUT SE CONTREDIRE EN INTERNE (N11) : retenir le paragraphe
  QUI DENOMBRE, l'ecrire dans a_valider_ft2e, en faire une question B -
  et ne publier en prose aucun compte contradictoire.
- ⚠ L'OPC PEUT CHANGER EN COURS DE CHANTIER (N12 : OTEEC du CR n°1 de
  09/2022 au n°37 de 07/2023, puis METHO du n°4 de 10/2023 au n°26 de
  04/2024, deux numerotations). Ne pas conclure « le chantier s'arrete
  au CR le plus haut » : chercher une SECONDE serie.
- NOMMER LE CLIENT FINAL : un nom deja publie par FT2E (plaquette,
  corpus secteurs, docx sectoriels, classeur) se reprend, avec E1
  (N09 Airbus, N10 CDAIR, N11 Undertech, N12 Central Hostel) ; un nom
  couvert par une clause de confidentialite reste hors slug et hors
  titre (N08 CPAM). Aucun nom de tiers ne monte jamais sur la planche.
- Archetypes apres N12 : boucle-fluide 10 - tableau-electrique 6 -
  sankey-energie 6 - coupe-traversee 6 - zonage-ssi 5 (mecanisme
  `convergence`, Central Hostel) - chronologie-affaire 2 -
  planche-chiffree 0 SANS module. L'archetype se choisit sur la THESE,
  jamais sur le secteur ni sur le quota, mais a these egale preferer ce
  qui n'a pas servi depuis longtemps ; la dette de variete porte
  toujours sur boucle-fluide, et chronologie-affaire n'a pas servi
  depuis le corpus fondateur (admissible seulement si sa these est
  d'INGENIERIE). Un batiment industriel neuf appellera probablement
  `tableau-electrique`, `boucle-fluide` ou `coupe-traversee` : trancher
  au depouillement, sur la these.
- Un mecanisme nouveau s'ecrit DANS le compositeur d'archetype
  (constantes prefixees par le mecanisme ; garde-fou de greffe sur le
  NOM DE LA FONCTION ET sur les prefixes de constantes), et l'invariant
  octet se rejoue AVANT la greffe, APRES la greffe et APRES la derniere
  retouche. ⚠ L'INSTRUMENT EXISTE DESORMAIS AU DEPOT ET SE REJOUE SEUL,
  NE PAS LE REECRIRE : `python scripts/planches/invariant.py` couvre
  les 6 compositeurs et les 35 dossiers (140/140 pieces au 2026-09-01),
  `python scripts/planches/invariant.py <archetype>` un seul.
- ⚠ NE PAS REECRIRE NON PLUS rendre_png.py : il est au depot depuis la
  N12, avec les deux pieges encodes (retrait de l'attribut style de
  racine par REGEX - sans quoi la vignette rend BLANCHE sans erreur -
  et fusion des filets a 8 chiffres). Usage :
  `python scripts/planches/rendre_png.py public/images/projets/<slug>
  <scratchpad>` ecrit planche.png 2400x1600 dans le dossier et, dans le
  scratchpad, les quatre controles (1152, vignette 274 et 296, appui
  552). REGARDER LES QUATRE.
- ECRIRE LES CHAINES COURBES DES L'ECRITURE - extraction planche.json
  COMPRISE. La recette, tenue en N11 et N12 : une assertion
  `"'" not in sortie` dans le script d'extraction lui-meme, avant
  ecriture, plus une assertion sur le COMPTE d'insecables. La passe
  `python scripts/apostrophes-planches.py` (sans argument, en MESURE)
  n'a alors rien a courber.
- Les avances calibrees de _tronc.mesurer sous-mesurent Archivo 600 au
  rendu d'environ 20 % (N08-N09) - prendre la marge DANS LE CODE
  (`mesurer(...) * 1.2`, comme le fait desormais l'appui du mecanisme
  `convergence`), pas a l'oeil ; controler() chaque libelle.
- REGARDER LES PNG, ET CORRIGER CE QU'ON Y VOIT. La N12 a fait quatre
  retouches que ni le build ni le bloc `controles` n'auraient
  signalees : une colonne de marques qui perdait sa distinction faute
  d'emplacement reserve, un TRONC QUI PENDAIT DANS LE VIDE parce que
  deux piles de hauteurs differentes sont calees en haut et que la
  fourche ne couvrait pas l'ordonnee de la boite centrale, un libelle
  qui chevauchait les marques a l'appui, une boite trop juste de 1 px.
  ⚠ Le piege du tronc est GENERIQUE : des qu'un registre est plus court
  que celui qui le nourrit, faire courir la fourche de min a max de
  TOUTES les ordonnees concernees, boite comprise.
- Quand aucune surface n'existe au dossier, la chercher dans les DOCX
  COMMERCIAUX avant de se rabattre sur la grandeur qui compte l'ouvrage
  (N12 : aucune piece du dossier ne porte de surface totale, les trois
  docx portent 1 025 m² de facon concordante - publie, avec question B).
- Les insecables des heredocs bash sont normalisees DE FACON NON
  DETERMINISTE sur cette machine. DEUX VOIES, toutes deux eprouvees :
  (a) ecrire le .md en ESPACES ORDINAIRES et apostrophes droites par
  l'outil Write, puis passer `python scripts/injection-typographique.py
  <fichier>` qui pose les insecables, les guillemets et les U+2019 -
  c'est la voie de la N12, la plus sure, car AUCUNE insecable ne
  traverse Write ; (b) script Python avec marqueurs ASCII remplaces par
  chr(8239)/chr(160) et assertion A L'EGALITE comptee sur le source -
  la voie a suivre pour tout fichier que injection-typographique.py ne
  couvre pas (planche.json, plan du chantier, prompt de continuite).
  ⚠ injection-typographique.py protege les lignes d'enum du frontmatter
  (secteur, typologie, mission_ft2e) : une apostrophe DROITE tapee dans
  mission_ft2e y RESTE et casse le build - ecrire U+2019 des le script
  (piege N10, « Études d'exécution »). Il NE protege PAS
  secteur_secondaire : verifier apres coup si sa valeur en porte une.

DEROULER LE PIPELINE § 2 INTEGRALEMENT : depouillement (pdfinfo /
pdftotext, ou pymupdf via python subprocess avec les noms lus par
os.listdir ; les plans sans couche texte et les marches scannes se
lisent en rendant leurs pages en PNG par pymupdf, zoom 2-3 ; antiword
pour les .doc, xlrd pour les .xls, openpyxl pour les .xlsx,
extract-msg pour les .msg) -> releve du numero NN-NNN sur piece FT2E ->
references/ref_036/ (3 a 8 pieces) -> croisement commercial
(references/docs_references/ - docx sectoriels ET classeur ODS - +
docs/20-source-plaquette-2024.md + grep de src/content/ pour ce que le
site publie deja) -> fiche de collecte (A/A+ remplies, B-E en
questions, ligne Secteur citant le classeur, DECISION Q3 motivee en
tete) -> fiche src/content/projets/<slug>.md (SECTEUR RELEVE AU
CLASSEUR ; taxonomie ACTUELLE ; lieu avec code postal entre
parentheses ; synthese 480-780 ; >= 5 liens internes ; jamais de numero
d'affaire NI de millesime d'ouverture en prose ; convention numerale
finale - nom d'un seul mot en lettres, nom compose en chiffres, unites
et mesures toujours en chiffres, citations intouchees) ->
PLANCHE complete (extraction avec a_valider_ft2e non vide, apostrophes
courbes des l'ecriture, composition par scripts/planches/<archetype>.py,
rendus par scripts/planches/rendre_png.py, controles a 1152 / carte
274-296 / appui 552 - REGARDER les quatre PNG -,
apostrophes-planches.py en MESURE, invariant.py, verser.py) ->
qualite (typecheck 0, build vert 59 pages, editorial-reviewer EN
LECTURE SEULE - ses outils d'edition normalisent les insecables,
appliquer ses constats par script -, controle-liens-internes 36/36 a 5,
controle-numeros-affaire 0 fuite, releve-numeral sans ecart nouveau)
-> COMMIT UNIQUE fiche+planche+compositeur (content(references): ajoute
la fiche reelle <nom> et sa planche ; git ls-remote avant, depot
partage) -> push (le push deploie), curl de la fiche AVEC barre oblique
finale + marqueur de build, rendu controle aux trois bandes (sonde
iframe pour les largeurs telephone : references/ref_033/sonde-fiche.mjs,
URL a adapter) ET CONTROLE DE L'INDEXATION SECTORIELLE (point 6, sonde
references/ref_033/sonde-filtres.mjs) -> ligne de suivi au plan ->
PROMPT DE LA SESSION N14 en annexe du plan (script Python ou Write,
jamais un long heredoc) et reproduit integralement dans le message
final. Le prompt N14 REPREND le bloc « REGLE D'INDEXATION SECTORIELLE »
tel quel (repartition remise a jour) ET demande a l'utilisateur, en
ouverture, le ZIP de la tranche 2023.

PIEGES VERIFIES EN N01-N12 (en plus de ceux des annexes A et B, tous
confirmes) :
- Un heredoc long se fait TRONQUER ou refuser silencieusement - bash
  COMME python : gros fichiers et scripts par l'outil Write PUIS
  execution ; le cwd du shell PERSISTE d'un appel a l'autre : chemins
  absolus ou cd explicite en tete de chaque commande.
- L'extraction zipfile de 2024.zip RECREE la racine interne : le
  dossier extrait vit sous ft2e_new_archives\2024\2024\<dossier>. Un
  os.listdir qui prend le premier niveau pour le dossier d'affaire
  echoue (piege N10) - toujours descendre par os.listdir.
- verser.py repond « deja verse » quand `planche:` est ecrit
  directement au frontmatter (fiche neuve) : ses controles 1 a 3 - les
  cinq pieces, l'archetype nomme, a_valider_ft2e non vide, le SVG sous
  40 Ko avec role="img" et sans width/height - ont TOUS tourne avant
  ce message. C'est un succes.
- PYTHONIOENCODING=utf-8 sur cette machine, et `python -c` sans lui
  plante en UnicodeEncodeError sur la moindre insecable ; ⚠ `python -c`
  avec un chemin Windows entre quotes casse aussi sur `'C:\'` (la
  contre-oblique echappe la quote) - utiliser os.sep ou des heredocs.
  Le hook Stop commite et pousse SEUL ce qui traine : SUPPRIMER les
  scripts de greffe et d'extraction a usage unique avant de committer.
  ⚠ PIEGE NOUVEAU, MESURE EN N12 : le hook ne se contente pas de
  ramasser les restes, il PEUT COMMITTER ET POUSSER LE LIVRABLE
  ENTIER - fiche, planche, compositeur, plan - sous l'intitule
  generique « chore(deploy): pousse l'etat de fin de session », avant
  que la session ait redige son commit. L'historique etant pousse sur
  un depot PARTAGE, il ne se reecrit pas : la suite se commite en
  content(references) par-dessus, en disant ce qui s'est passe. Pour
  l'eviter : COMMITTER TOT, des que le build est vert, et reserver un
  second commit a la passe editoriale plutot que d'attendre l'agent
  de relecture avec un arbre de travail plein
  (⚠ livrables/ porte deux fichiers non suivis anterieurs a la N02 -
  les laisser) ; ne pas attendre un agent de fond en fin de tour sans
  avoir commite (piege N09) ; /references/ est gitignore (motif ancre) -
  les pieces sources n'entrent JAMAIS au depot ; npm run preview ne
  mesure pas la performance ; Chrome refuse les fenetres sous 500 px
  (sonde iframe).
- La planche n'expose NI le millesime d'ouverture, NI montant, NI
  tiers (MOA, mandataire, architecte, installateur, MARQUES comprises),
  NI donnee nominative ; les designations internes (reperes de zone,
  numeros de tableau) sont admises avec une entree a_valider_ft2e et
  une question E ; tout arbitrage de dessin va dans a_valider_ft2e
  (jamais vide).

Portee de commit : content(references). Un changement de schema Zod
eventuel passe par le sous-agent content-modeller et va dans le MEME
commit que public/admin/config.yml.

Termine par le prompt de lancement de la session N14, en annexe du
plan du chantier et reproduit integralement dans ton message final -
la regle de continuite est dans CLAUDE.md parce qu'elle a ete manquee
deux fois.
```

## Annexe N — prompt de lancement de la session N14 (à coller tel quel en session neuve)

```
Session N14/27 - FT2E v3 : chantier des 27 nouvelles fiches references.
Quatorzieme dossier - CINQUIEME ET DERNIER de la tranche
« Finalisees en 2024 ».

Contexte. FT2E v3 est le site institutionnel du bureau d'etudes FT2E
(La Rochelle), Astro 6 statique, deploye en demonstration client sur
https://ft2e-v3.vercel.app (indexation verrouillee - ne pas y toucher).
Le catalogue porte 36 fiches reelles (23 + N01 Portes-en-Re + N02 Fors +
N03 Aurora + N04 Loti + N05 Saint-Sauveur + N06 L'Houmeau + N07 Louise
Magnan + N08 bornes IRVE + N09 comptage Airbus + N10 foyer CDAIR +
N11 parc Undertech + N12 auberge Central Hostel + N13 batiment
VoltAero), chacune illustree d'une planche de schema de principe (cinq
pieces par dossier). Objectif : 50 fiches. 1 session = 1 dossier, close
par le prompt de la suivante.

⚠ PREMIERE CHOSE A FAIRE, EN OUVERTURE : DEMANDER A L'UTILISATEUR LE ZIP
DE LA TRANCHE 2023. La tranche 2024 se CLOT avec cette session. Le
classeur ODS annonce cinq dossiers pour 2023, a extraire du prochain ZIP
(numeros du classeur, graphie sans tiret) :
-  20045 · THE ROOF · T § C  (domaine DOUBLE)
-  20071 · Bureaux EIFFAGE · T
-  21029 · Ecole primaire et maternelle La Flotte · M
-  21074 · Projet AP Yacht - CATANA Group · I
-  21086 · Audit chauffage sites ADEI · M
Aucun de ces cinq numeros n'est publie (verifie au grep de
src/content/projets/*.md le 2026-09-01). Poser la question AVANT de
depouiller le dossier du jour, pour que la N15 ne soit pas bloquee.

LE FONDS DE LA TRANCHE 2024 EST LIVRE :
C:\claude_code_dev_projects\ft2e_new_archives\2024.zip (472,7 Mo, racine
interne « 2024/ », un repertoire par affaire). Les N10 a N13 ont traite
19-110 CDAIR, 20-031 UNDERTECH, 21-093 Central Hostel et 21-095
VoltAero. Reste UN dossier :
-  70 fichiers, 110 Mo : « 23-036- Extension bat 5-8 Fountaine Pajot -
   ASP » (classeur : 23036 · Extension Bat 5-8 Fountaine Pajot · I)
   <- DOSSIER DU JOUR
⚠ NE JAMAIS conclure « mince » ni « riche » sur le seul compte de
fichiers : quatre dementis en N08-N09 (mince qui etait riche), et un
dementi INVERSE en N13 - « 21-095 » annoncait 72 fichiers dont 17 (24 %)
appartenaient a l'affaire 21-093. C'est la PAGE DE GARDE qui dit a
quelle affaire une piece appartient, jamais le repertoire qui la
contient. Verifier la page de garde de chaque CCTP, DPGF, estimation et
plan AVANT d'en tirer la moindre valeur.

LIRE D'ABORD, dans cet ordre :
1. docs/superpowers/plans/2026-08-27-chantier-27-nouvelles-fiches.md -
   LE PLAN : § 1 (ce qui a change), § 2 (pipeline 12 etapes), § 3
   (reponses consignees Q1/Q2 2024 + complement N02 : le classeur fait
   foi ; Q3 = regle des dossiers minces, defaut reconduit), § Suivi
   (lignes N01 a N13), annexe N (ce prompt).
2. docs/superpowers/plans/2026-08-07-chantier-references-reelles.md -
   § Contraintes globales + § Protocole de session + § Regle des
   dossiers minces.
3. docs/superpowers/specs/2026-08-12-planches-references-protocole.md -
   revision 5 EN ENTIER.
4. CLAUDE.md, .claude/rules/content-collections.md et french-editorial.md.
Etalons : src/content/projets/creche-oranger-perigny.md (fiche) et, pour
un batiment industriel a MOA privee deja nommee par FT2E :
src/content/projets/batiment-voltaero-saint-agnant.md +
public/images/projets/batiment-voltaero-saint-agnant/ +
references/ref_036/ (fiche de collecte avec decision Q3 motivee en tete
- c'est elle qui documente le piege du sous-repertoire mal classe).
Voir aussi src/content/projets/ateliers-pilotes-capsulae.md, tres proche
par la these (utilites de procede livrees en limite d'atelier).
Les sondes de recette vivent dans references/ref_036/ (sonde-fiche.mjs,
sonde-filtres.mjs - URL et slug a adapter).

REGLE D'INDEXATION SECTORIELLE - etablie le 2026-08-27, A APPLIQUER A
LA REDACTION DE CHAQUE FICHE (etape 6 du pipeline), pas apres coup :
« REFERENCES SITE FT2E.ods » (references/docs_references/, classeur
fourni par FT2E) FAIT FOI pour le classement sectoriel. Concretement,
AVANT d'ecrire le frontmatter :
1. Ouvrir le classeur (python zipfile sur content.xml, ou pandoc) et y
   retrouver l'affaire PAR SON NUMERO (graphie sans tiret : « 23036 »).
2. En relever le domaine (legende : L Logements / T Tertiaire & ERP /
   I Industriel / P Patrimoine / C Coordination SSI /
   M Monotechnique-Audit / E EXE) -> champ `secteur`.
3. Si le classeur porte un domaine DOUBLE (« T § C ») : le premier est
   le `secteur`, le second va au champ `secteur_secondaire` (optionnel
   au schema depuis le 2026-08-27, garde-fou « doit differer ») - la
   fiche parait alors dans les deux filtres et sur les deux pages de
   secteur. Precedents : hotel-yachtman (T § C), maison-pierre-loti-
   rochefort (P § C, N04), foyer-cdair-saint-martin-de-re (T § C, N10),
   auberge-central-hostel-la-rochelle (T § C, N12).
   Le dossier du jour, lui, est a domaine SIMPLE : 23036 est « I ».
4. JAMAIS de deduction depuis le dossier, l'usage RT ou le nom de
   l'operation : la N02 penchait « Industriel » pour Fors, le classeur
   dit T - et les 25 fiches ont du etre re-referencees le soir meme
   (7 bascules, commits ce334b2/09270a3). Le classeur peut contredire
   l'intuition (Saint-Rogatien, pole commercial : I ; Fors, pole
   commercial : T ; 23083 « plan de comptage Airbus » : E et non M -
   une mission vendue a l'entreprise est classee E ; 23099 « CPAM » :
   M - IRVE, pas T) - il gagne.
5. CONSIGNER la lecture dans la fiche de collecte (ligne « Secteur » :
   citer l'entree du classeur telle quelle) ; si l'affaire est ABSENTE
   du classeur ou son domaine illisible -> question B a FT2E et choix
   provisoire argumente, jamais silencieux.
6. EN RECETTE (etape 10) : verifier sur le deploiement que la fiche
   repond au bon filtre de /references (compteurs de chips) et parait
   sur sa page /secteurs/<slug> - sondes : references/ref_036/
   sonde-filtres.mjs et sonde-fiche.mjs (URL a adapter).
   ⚠ Une page /secteurs/<slug> n'affiche que les 4 affaires les plus
   recentes du secteur (tri par numero decroissant) ; le filtre de
   /references, lui, montre tout. Le secteur Industriel compte
   aujourd'hui TROIS fiches (Capsulae, Saint-Rogatien, VoltAero) : la
   fiche du jour, 23-036, y sera la plus recente et donc visible a coup
   sur.
   Repartition attendue AVANT la N14 : L10 T12 I3 P3 C6 M3 E3 pour
   36 fiches, 40 en pondere (Yachtman T+C, Loti P+C, foyer CDAIR T+C et
   Central Hostel T+C comptent double). Mesuree le 2026-09-01 par
   references/ref_036/sonde-filtres.mjs sur le deploiement.

DOSSIER DU JOUR : « 23-036- Extension bat 5-8 Fountaine Pajot - ASP »
(70 fichiers, 110 Mo), classeur « 23036 · Extension Bat 5-8 Fountaine
Pajot · I ». Fountaine Pajot est le constructeur de catamarans
d'Aigrefeuille-d'Aunis. Le nom est DEJA PUBLIE par FT2E a trois
endroits, ce qui remplit la condition E1 sans nouvelle autorisation :
la plaquette 2024 (« Extension Fountaine Pajot | Aigrefeuille-d'Aunis |
2024 | Fountaine Pajot / S. Pellereau », docs/20-source-plaquette-2024.md
l. 62 et 86), le CV de Vincent Jaoul (« 2024 FOUNTAINE PAJOT - BATIMENT
INDUSTRIEL Aigrefeuille-d'Aunis (17) Conception electricite CFO / CFA /
SSI ») et la page secteur du site
(src/content/secteurs/industriel-commercial.md l. 63 : « extension du
batiment Fountaine Pajot a Aigrefeuille-d'Aunis (2024) »). « ASP » au
nom du dossier designe l'Agence Sebastien Pellereau, deja nommee sur
plusieurs fiches - relever sa graphie exacte au depot avant d'ecrire
`architecte`.
⚠ Le CV de Vincent Jaoul annonce une mission SSI : verifier si le
classeur la porte en second domaine (il dit « I » seul) et, s'il y a
contradiction, la consigner en question B sans trancher en silence.
Aucun numero 23-036 n'est publie (verifie au grep de
src/content/projets/*.md le 2026-09-01).
ATTENTION DISQUE (~6 Go libres) : supprimer d'abord le repertoire
extrait de la session precedente -
C:\claude_code_dev_projects\ft2e_new_archives\2024 (le REPERTOIRE, pas
le ZIP ; il contient 2024/21-095- VOLTAREAO ST AGNANT - Cab SOURD) -
par python shutil.rmtree (le rm -rf est REFUSE par les permissions).
Puis extraire LE SEUL dossier du jour PAR PYTHON ZIPFILE (members
filtres sur « 23-036 » via zipfile.namelist() - les noms portent des
accents en mojibake, ne JAMAIS taper un chemin). 110 Mo pour 70
fichiers : il y a des scans volumineux, prevoir de les lire en rendant
leurs pages en PNG. Le ZIP est la source, il ne se supprime pas.
Dossier de travail a creer : references/ref_037/
Slug cible : a etablir au depouillement (kebab-case sans accents,
verifier qu'il n'ecrase rien).

CE QUE LES N01-N13 ONT ETABLI (verifiable au depot) :
- ⚠ UN DOSSIER D'ARCHIVES PEUT CONTENIR LES PIECES D'UNE AUTRE AFFAIRE
  (N13, decouverte majeure). Le sous-repertoire « 02-Production/05-Pro »
  de 21-095 portait les deux CCTP, les deux DPGF, les deux estimations
  et dix plans de 21-093 - 17 fichiers sur 72. Lire la PAGE DE GARDE
  (« N° affaire : … », « Affaire n° : … ») de CHAQUE piece technique
  avant d'en tirer une valeur. Un plan sans couche texte se controle en
  rendant sa page en PNG : sur 21-095, les hauteurs sous plafond de
  1,14 a 2,82 m disaient l'immeuble du XVIIe, pas un hall de 5 m.
  Corollaire : une affaire peut n'avoir AUCUNE piece technique FT2E au
  dossier. La fiche reste publiable si trois familles de sources la
  soutiennent - programme du maitre d'ouvrage, comptes rendus de
  chantier, CV de l'equipe -, a condition que chacune soit NOMMEE en
  collecte et qu'aucune valeur de dimensionnement ne soit inventee.
- LES CV DE L'EQUIPE SONT UNE SOURCE FT2E (livrables/cv-ft2e/CV-FT2E.zip,
  edition aout 2026, six CV en .docx lisibles par zipfile+regex sur
  word/document.xml). La N13 y a trouve le perimetre reel de la mission
  (« Conception CVC / VMC / plomberie · air comprime / RIA ») et sa
  seule performance chiffree (« Calcul reglementaire RT2012 - Cep -40 % »),
  qu'aucune piece du dossier ne portait. Les interroger systematiquement
  au croisement commercial (etape 4), avec les docx sectoriels, le
  classeur et docs/20-source-plaquette-2024.md.
- annee_livraison se pose sur le classeur (« Finalisees en 2024 » pour
  cette tranche) ; quand pieces et classeur se contredisent, le
  classeur est suivi ET la contradiction est ecrite en B1, jamais
  tranchee en silence. Le PV de reception manque presque toujours -
  mais l'etai peut etre solide sans lui, et il se cherche a QUATRE
  endroits : un CR d'OPC portant « RECEPTION DES TRAVAUX » en tete
  (N11), un CR annoncant la reception a une date precise avec le
  planning des semaines suivantes (N12), le BILAN DE FACTURATION (les
  honoraires d'AOR ne se facturent qu'une fois la mission finie, N12),
  et - nouveau en N13 - LE DERNIER CR DE CHANTIER, dont l'en-tete
  remplace « PROCHAINE REUNION » par « RECEPTION le JJ/MM/AAAA a HHh
  sur site » suivi de la liste des convoques.
- Le numero FT2E se releve sur page de garde CCTP (« Affaire n° : … »),
  etude thermique (pied de chaque page), contrats et propositions FT2E.
  ⚠ EN DERNIER RECOURS SEULEMENT, quand aucune piece FT2E n'existe au
  dossier (N13), il se releve sur le CLASSEUR + le nom du repertoire
  d'archives, et cela DOIT faire l'objet d'une question B.
- Les numeros des MANDATAIRES et donneurs d'ordres pietinent les
  pieces : SD Architectes « 21.17 » et « 21.45 », marche public
  « 20210000200 », commande « 2024000451 », devis « 18.2024 », dossier
  RESE « TRX021847 » (N13) ; SEMDAS « 2507 » / « 2020/007 » / « 2020/071 »,
  ARCHITEM « 1821 » (N10) ; Equans « 22984760 » (N09) ; CPAM
  « PA 2024 - MO01 » (N08). Six faux numeros dans le seul dossier N13.
- ⚠ UN CCTP PEUT SE CONTREDIRE EN INTERNE (N11) : retenir le paragraphe
  QUI DENOMBRE, l'ecrire dans a_valider_ft2e, en faire une question B.
- ⚠ L'OPC PEUT CHANGER EN COURS DE CHANTIER (N12) ; en N13 il n'y en a
  eu qu'un, et les 47 CR forment une seule serie. Ne pas presumer.
- NOMMER LE CLIENT FINAL : un nom deja publie par FT2E (plaquette,
  corpus secteurs, docx sectoriels, classeur, CV) se reprend, avec E1
  (N09 Airbus, N10 CDAIR, N11 Undertech, N12 Central Hostel, N13
  VoltAero) ; un nom couvert par une clause de confidentialite reste
  hors slug et hors titre (N08 CPAM). Aucun nom de tiers ne monte jamais
  sur la planche - seul le nom d'OUVRAGE peut porter celui de
  l'occupant (« Bâtiment VoltAero », « Ateliers Capsulae », « Atelier
  Dufour Yachts », « Parc Undertech »).
- ⚠ UNE GRAPHIE PEUT ETRE FAUSSE PARTOUT SAUF DANS LES CV (N13) : le
  repertoire d'archives ecrivait « VOLTAREAO », le programme
  « Voltaero », la plaquette « Voltareo », les CV « VOLTAERO ». Graphie
  sociale retenue : « VoltAero ». Relever la graphie sur la page de
  garde d'un contrat ou d'un marche, jamais sur un nom de dossier.
- Archetypes apres N13 : boucle-fluide 10 - coupe-traversee 7
  (mecanisme `frontiere`, VoltAero) - sankey-energie 6 -
  tableau-electrique 6 - zonage-ssi 5 - chronologie-affaire 2 -
  planche-chiffree 0 SANS module. L'archetype se choisit sur la THESE,
  jamais sur le secteur ni sur le quota, mais a these egale preferer ce
  qui n'a pas servi depuis longtemps ; la dette de variete porte
  toujours sur boucle-fluide, et chronologie-affaire n'a pas servi
  depuis le corpus fondateur (admissible seulement si sa these est
  d'INGENIERIE). Une extension de batiment industriel appellera
  probablement `coupe-traversee`, `tableau-electrique` ou `zonage-ssi`
  (si la mission SSI du CV se confirme) : trancher au depouillement,
  sur la these.
- Un mecanisme nouveau s'ecrit DANS le compositeur d'archetype
  (constantes prefixees par le mecanisme ; garde-fou de greffe sur le
  NOM DE LA FONCTION ET sur les prefixes de constantes - la N13 a
  automatise ce garde-fou dans son script de greffe : 7 fonctions et
  26 constantes verifiees avant insertion), et l'invariant octet se
  rejoue AVANT la greffe, APRES la greffe et APRES la derniere
  retouche. ⚠ L'INSTRUMENT EXISTE AU DEPOT ET SE REJOUE SEUL, NE PAS LE
  REECRIRE : `python scripts/planches/invariant.py` couvre les 6
  compositeurs et les 36 dossiers (144/144 pieces au 2026-09-01),
  `python scripts/planches/invariant.py <archetype>` un seul.
- ⚠ NE PAS REECRIRE NON PLUS rendre_png.py : il est au depot depuis la
  N12, avec les deux pieges encodes (retrait de l'attribut style de
  racine par REGEX - sans quoi la vignette rend BLANCHE sans erreur -
  et fusion des filets a 8 chiffres). Usage :
  `python scripts/planches/rendre_png.py public/images/projets/<slug>
  <scratchpad>` ecrit planche.png 2400x1600 dans le dossier et, dans le
  scratchpad, les quatre controles (1152, vignette 274 et 296, appui
  552). REGARDER LES QUATRE.
- ⚠ LE RENDU CAIROSVG N'A PAS LES POLICES DU SITE (mesure en N13) : il
  retombe sur une police de substitution dont la chasse mono est ~7 a
  8 % plus large que celle d'IBM Plex Mono. Consequence : le dernier
  caractere du cartouche de legende parait COUPE sur le PNG de
  controle des planches longues - c'est le cas de la planche publiee
  de l'EHPAD de Coulonges (« · 202 ») comme de celle de VoltAero. Le
  navigateur, lui, rend juste (verifie a 1440 px sur le deploiement).
  NE PAS « corriger » la largeur du cartouche : la formule
  `mesurer(...) + 40` est commune aux 36 planches, et l'elargir pour ce
  seul dossier ferait de lui l'exception. Les controles de largeur du
  compositeur (bloc `depassements`) restent la mesure qui fait foi.
- ECRIRE LES CHAINES COURBES DES L'ECRITURE - extraction planche.json
  COMPRISE. La recette, tenue en N11, N12 et N13 : une assertion
  `"'" not in sortie` dans le script d'extraction lui-meme, avant
  ecriture, plus une assertion sur le COMPTE d'insecables - et ce
  compte se LIT sur le source du script (nombre de marqueurs), jamais
  ecrit a la main : un nombre en dur se demode au premier ajout de
  chaine et l'assertion cesse de mesurer (relevé en N13). La passe
  `python scripts/apostrophes-planches.py` (sans argument, en MESURE)
  n'a alors rien a courber DANS LE JSON - mais elle a encore a courber
  les libelles francais du COMPOSITEUR (bloc `controles`) : la lancer
  avec `--appliquer` PUIS recomposer, puis remesurer a zero.
- Les avances calibrees de _tronc.mesurer sous-mesurent Archivo 600 au
  rendu d'environ 20 % (N08-N09) - prendre la marge DANS LE CODE
  (`mesurer(...) * 1.2`), pas a l'oeil ; controler() chaque libelle.
- REGARDER LES PNG, ET CORRIGER CE QU'ON Y VOIT. La N13 a fait deux
  retouches que ni le build ni le bloc `controles` n'auraient
  signalees : deux legendes centrees sous leurs blocs qui debordaient
  de leur colonne des deux cotes (reancrees start/end sur le bord
  exterieur du bloc), et un mur de vignette trop fin pour se lire a
  274 px (2,5 -> 3,5 px). ⚠ Piege generique confirme : deux rangs qui
  emploient le MEME motif geometrique ne demontrent rien - il faut les
  distinguer par un detail porteur (en N13, sabot plat pour le piquage
  electrique, cercle de vanne + niveau interrompu pour l'attente d'air
  comprime).
- Quand aucune surface n'existe au dossier, la chercher dans les DOCX
  COMMERCIAUX (N12 : 1 025 m² concordants sur trois docx) ; si elle n'y
  est pas non plus (N13 : VoltAero n'a AUCUNE fiche commerciale),
  laisser `surface_m2` VIDE et porter au cartouche la grandeur qui
  compte l'ouvrage, avec question B. Precedents de cartouche sans
  surface : « 38 000 m³/h » (Dufour), « SEPT POINTS DE CHARGE » (IRVE),
  « TOUR DE 40 m » (Saint-Sauveur), « TABLIER DE 25,40 m » (Marans),
  « QUATRE CHAUFFERIES » (Airbus), « SOIXANTE MAISONS » (Louise
  Magnan), « HUIT POSTES D'ASSEMBLAGE » (VoltAero).
- Les insecables des heredocs bash sont normalisees DE FACON NON
  DETERMINISTE sur cette machine. DEUX VOIES, toutes deux eprouvees :
  (a) ecrire le .md en ESPACES ORDINAIRES et apostrophes droites par
  l'outil Write, puis passer `python scripts/injection-typographique.py
  <fichier>` qui pose les insecables, les guillemets et les U+2019 -
  c'est la voie des N12 et N13, la plus sure, car AUCUNE insecable ne
  traverse Write ; (b) script Python avec marqueurs ASCII remplaces par
  chr(8239)/chr(160) et assertion A L'EGALITE comptee sur le source -
  la voie a suivre pour tout fichier que injection-typographique.py ne
  couvre pas (planche.json, plan du chantier, prompt de continuite).
  ⚠ injection-typographique.py protege les lignes d'enum du frontmatter
  (secteur, typologie, mission_ft2e) : une apostrophe DROITE tapee dans
  mission_ft2e y RESTE et casse le build - ecrire U+2019 des le script
  (piege N10, « Études d'exécution »). Il NE protege PAS
  secteur_secondaire : verifier apres coup si sa valeur en porte une.
  ⚠ Il ne connait pas toutes les unites : « t/m² » et « tonnes » lui
  echappent (N13). Verifier au grep les unites rares apres passage.

DEROULER LE PIPELINE § 2 INTEGRALEMENT : depouillement (pdfinfo /
pdftotext, ou pymupdf via python subprocess avec les noms lus par
os.listdir ; les plans sans couche texte et les marches scannes se
lisent en rendant leurs pages en PNG par pymupdf, zoom 2-3 ; antiword
pour les .doc, xlrd pour les .xls, openpyxl pour les .xlsx,
extract-msg pour les .msg) -> CONTROLE DE LA PAGE DE GARDE DE CHAQUE
PIECE TECHNIQUE -> releve du numero NN-NNN sur piece FT2E ->
references/ref_037/ (3 a 8 pieces) -> croisement commercial
(references/docs_references/ - docx sectoriels ET classeur ODS - +
docs/20-source-plaquette-2024.md + livrables/cv-ft2e/CV-FT2E.zip +
grep de src/content/ pour ce que le site publie deja) -> fiche de
collecte (A/A+ remplies, B-E en questions, ligne Secteur citant le
classeur, DECISION Q3 motivee en tete) -> fiche
src/content/projets/<slug>.md (SECTEUR RELEVE AU CLASSEUR ; taxonomie
ACTUELLE ; lieu avec code postal entre parentheses ; synthese 480-780 ;
>= 5 liens internes ; jamais de numero d'affaire NI de millesime
d'ouverture en prose ; convention numerale finale - nom du NOMBRE en un
seul mot en lettres, nombre COMPOSE en chiffres, unites et mesures
toujours en chiffres, citations intouchees ; verifier par
`python scripts/releve-numeral.py`, dont la section « Nombres COMPOSES
ecrits en lettres » doit rendre 0) ->
PLANCHE complete (extraction avec a_valider_ft2e non vide, apostrophes
courbes des l'ecriture, composition par scripts/planches/<archetype>.py,
rendus par scripts/planches/rendre_png.py, controles a 1152 / carte
274-296 / appui 552 - REGARDER les quatre PNG -,
apostrophes-planches.py en MESURE puis --appliquer si le compositeur a
recu des libelles francais, invariant.py, verser.py) ->
qualite (typecheck 0, build vert 60 pages, editorial-reviewer EN
LECTURE SEULE - ses outils d'edition normalisent les insecables,
appliquer ses constats par script -, controle-liens-internes 37/37 a 5,
controle-numeros-affaire 0 fuite, releve-numeral sans ecart nouveau)
-> COMMIT UNIQUE fiche+planche+compositeur (content(references): ajoute
la fiche reelle <nom> et sa planche ; git ls-remote avant, depot
partage) -> push (le push deploie), curl de la fiche AVEC barre oblique
finale + marqueur de build, rendu controle aux trois bandes (sonde
iframe pour les largeurs telephone : references/ref_036/sonde-fiche.mjs,
slug et URL a adapter) ET CONTROLE DE L'INDEXATION SECTORIELLE (point 6,
sonde references/ref_036/sonde-filtres.mjs) -> ligne de suivi au plan ->
PROMPT DE LA SESSION N15 en annexe du plan (script Python ou Write,
jamais un long heredoc) et reproduit integralement dans le message
final. Le prompt N15 REPREND le bloc « REGLE D'INDEXATION SECTORIELLE »
tel quel (repartition remise a jour) ET porte le premier dossier de la
tranche 2023, dont le ZIP aura ete demande en ouverture de CETTE
session.

PIEGES VERIFIES EN N01-N13 (en plus de ceux des annexes A et B, tous
confirmes) :
- Un heredoc long se fait TRONQUER ou refuser silencieusement - bash
  COMME python : gros fichiers et scripts par l'outil Write PUIS
  execution ; le cwd du shell PERSISTE d'un appel a l'autre : chemins
  absolus ou cd explicite en tete de chaque commande.
- L'extraction zipfile de 2024.zip a recree la racine interne en N10
  (ft2e_new_archives\2024\2024\<dossier>) mais PAS en N11-N13
  (ft2e_new_archives\2024\<dossier>) : ne jamais presumer la
  profondeur, descendre par os.listdir.
- verser.py repond « deja verse » quand `planche:` est ecrit
  directement au frontmatter (fiche neuve) : ses controles 1 a 3 - les
  cinq pieces, l'archetype nomme, a_valider_ft2e non vide, le SVG sous
  40 Ko avec role="img" et sans width/height - ont TOUS tourne avant
  ce message. C'est un succes.
- PYTHONIOENCODING=utf-8 sur cette machine, et `python -c` sans lui
  plante en UnicodeEncodeError sur la moindre insecable ; ⚠ `python -c`
  avec un chemin Windows entre quotes casse aussi sur `'C:\'` (la
  contre-oblique echappe la quote) - utiliser os.sep ou des heredocs.
  ⚠ `fc-list` n'existe pas sur cette machine et son appel par subprocess
  plante en UnicodeDecodeError cp1252 : ne pas chercher a inventorier
  les polices par la.
- Le hook Stop commite et pousse SEUL ce qui traine, et il PEUT
  COMMITTER LE LIVRABLE ENTIER sous l'intitule generique
  « chore(deploy): pousse l'etat de fin de session » avant que la
  session ait redige son commit. L'historique etant pousse sur un depot
  PARTAGE, il ne se reecrit pas. Pour l'eviter : SUPPRIMER les scripts
  a usage unique avant de committer (ceux de la N13 vivaient dans le
  scratchpad, hors depot - c'est la bonne pratique), COMMITTER TOT des
  que le build est vert, et reserver un second commit a la passe
  editoriale plutot que d'attendre l'agent de relecture avec un arbre
  de travail plein (⚠ livrables/ porte deux fichiers non suivis
  anterieurs a la N02 - les laisser).
- /references/ est gitignore (motif ancre) - les pieces sources
  n'entrent JAMAIS au depot ; npm run preview ne mesure pas la
  performance ; Chrome refuse les fenetres sous 500 px (sonde iframe).
- La planche n'expose NI le millesime d'ouverture, NI montant, NI
  tiers (MOA, mandataire, architecte, installateur, MARQUES comprises),
  NI donnee nominative ; les designations internes (reperes de zone,
  numeros de tableau) sont admises avec une entree a_valider_ft2e et
  une question E ; tout arbitrage de dessin va dans a_valider_ft2e
  (jamais vide).

Portee de commit : content(references). Un changement de schema Zod
eventuel passe par le sous-agent content-modeller et va dans le MEME
commit que public/admin/config.yml.

Termine par le prompt de lancement de la session N15, en annexe du
plan du chantier et reproduit integralement dans ton message final -
la regle de continuite est dans CLAUDE.md parce qu'elle a ete manquee
deux fois.
```

## Annexe O — prompt de lancement de la session N15 (à coller tel quel en session neuve)

````
Session N15/27 - FT2E v3 : chantier des 27 nouvelles fiches references.
Quinzieme dossier - PREMIER de la tranche « Finalisees en 2023 ».

Contexte. FT2E v3 est le site institutionnel du bureau d'etudes FT2E
(La Rochelle), Astro 6 statique, deploye en demonstration client sur
https://ft2e-v3.vercel.app (indexation verrouillee - ne pas y toucher).
Le catalogue porte 37 fiches reelles (23 + N01 Portes-en-Re + N02 Fors +
N03 Aurora + N04 Loti + N05 Saint-Sauveur + N06 L'Houmeau + N07 Louise
Magnan + N08 bornes IRVE + N09 comptage Airbus + N10 foyer CDAIR +
N11 parc Undertech + N12 auberge Central Hostel + N13 batiment VoltAero +
N14 extension Fountaine Pajot), chacune illustree d'une planche de schema
de principe (cinq pieces par dossier). Objectif : 50 fiches.
1 session = 1 dossier, close par le prompt de la suivante.

LA TRANCHE 2024 EST CLOSE (N10 a N14 : 19-110 CDAIR, 20-031 UNDERTECH,
21-093 Central Hostel, 21-095 VoltAero, 23-036 Fountaine Pajot).
LE ZIP DE LA TRANCHE 2023 EST DEJA SUR LE DISQUE :
C:\claude_code_dev_projects\ft2e_new_archives\2023.zip (446 Mo, 670
entrees, racine interne « 2023/ », un repertoire par affaire). Inventaire
mesure le 2026-09-01, cinq dossiers, tous absents du site (verifie au grep
de src/content/projets/*.md) :
-  184 fichiers, 178,8 Mo : « 21-086 - Audit chauffage sites ADEI »        (classeur M)
-  164 fichiers, 234,3 Mo : « 20-045- Cabanes Urbaines - ALTERLAB »        (classeur T § C)  <- DOSSIER DU JOUR
-   89 fichiers,  40,8 Mo : « 21-074- Projet AP Yacht - CATANA Group-  Cab SIMONEAU » (classeur I)
-   72 fichiers,  39,6 Mo : « 20-071- Bureaux EIFFAGE St Jean D'Angely - Impact Urbanisme » (classeur T)
-   54 fichiers,  14,9 Mo : « 21-029 - Ecole primaire et maternelle - La Flotte en Re » (classeur M)
IL N'Y A DONC AUCUNE QUESTION A POSER EN OUVERTURE : derouler directement.
(La tranche 2022 - 4 dossiers au classeur - fera l'objet d'un ZIP a
demander en ouverture de la session qui closera 2023, soit la N19.)
⚠ NE JAMAIS conclure « mince » ni « riche » sur le seul compte de fichiers :
quatre dementis en N08-N09 (mince qui etait riche), un dementi INVERSE en
N13 (« 21-095 » annoncait 72 fichiers dont 17 appartenaient a l'affaire
21-093), et un dossier integre en N14. C'est la PAGE DE GARDE qui dit a
quelle affaire une piece appartient, jamais le repertoire qui la contient.
Verifier la page de garde de chaque CCTP, DPGF, estimation et plan AVANT
d'en tirer la moindre valeur.

LIRE D'ABORD, dans cet ordre :
1. docs/superpowers/plans/2026-08-27-chantier-27-nouvelles-fiches.md -
   LE PLAN : § 1 (ce qui a change), § 2 (pipeline 12 etapes), § 3
   (reponses consignees Q1/Q2 2024 + complement N02 : le classeur fait
   foi ; Q3 = regle des dossiers minces, defaut reconduit), § Suivi
   (lignes N01 a N14), annexe O (ce prompt).
2. docs/superpowers/plans/2026-08-07-chantier-references-reelles.md -
   § Contraintes globales + § Protocole de session + § Regle des
   dossiers minces.
3. docs/superpowers/specs/2026-08-12-planches-references-protocole.md -
   revision 5 EN ENTIER.
4. CLAUDE.md, .claude/rules/content-collections.md et french-editorial.md.
Etalons : src/content/projets/creche-oranger-perigny.md (fiche) et, pour
une affaire a DOUBLE DOMAINE avec mission de coordination SSI :
src/content/projets/auberge-central-hostel-la-rochelle.md (T § C, N12) et
src/content/projets/hotel-yachtman-quai-valin-la-rochelle.md (T § C).
Voir aussi src/content/projets/extension-fountaine-pajot-aigrefeuille.md +
public/images/projets/extension-fountaine-pajot-aigrefeuille/ +
references/ref_037/ (fiche de collecte N14, avec sa DECISION Q3 en tete -
c'est elle qui documente le piege de la these deja publiee).
Les sondes de recette vivent dans references/ref_037/ (sonde-fiche.mjs,
sonde-filtres.mjs - URL, slug et secteur a adapter).

REGLE D'INDEXATION SECTORIELLE - etablie le 2026-08-27, A APPLIQUER A
LA REDACTION DE CHAQUE FICHE (etape 6 du pipeline), pas apres coup :
« REFERENCES SITE FT2E.ods » (references/docs_references/, classeur
fourni par FT2E) FAIT FOI pour le classement sectoriel. Concretement,
AVANT d'ecrire le frontmatter :
1. Ouvrir le classeur (python zipfile sur content.xml, ou pandoc) et y
   retrouver l'affaire PAR SON NUMERO (graphie sans tiret : « 20045 »).
2. En relever le domaine (legende : L Logements / T Tertiaire & ERP /
   I Industriel / P Patrimoine / C Coordination SSI /
   M Monotechnique-Audit / E EXE) -> champ `secteur`.
3. Si le classeur porte un domaine DOUBLE (« T § C ») : le premier est
   le `secteur`, le second va au champ `secteur_secondaire` (optionnel
   au schema depuis le 2026-08-27, garde-fou « doit differer ») - la
   fiche parait alors dans les deux filtres et sur les deux pages de
   secteur. Precedents : hotel-yachtman (T § C), maison-pierre-loti-
   rochefort (P § C, N04), foyer-cdair-saint-martin-de-re (T § C, N10),
   auberge-central-hostel-la-rochelle (T § C, N12).
   LE DOSSIER DU JOUR EST A DOMAINE DOUBLE : 20045 est « T § C ».
4. JAMAIS de deduction depuis le dossier, l'usage RT ou le nom de
   l'operation : la N02 penchait « Industriel » pour Fors, le classeur
   dit T - et les 25 fiches ont du etre re-referencees le soir meme
   (7 bascules, commits ce334b2/09270a3). Le classeur peut contredire
   l'intuition (Saint-Rogatien, pole commercial : I ; Fors, pole
   commercial : T ; 23083 « plan de comptage Airbus » : E et non M ;
   23099 « CPAM » : M - IRVE, pas T ; 23036 Fountaine Pajot : I SIMPLE
   alors que le CV annonce « CFO / CFA / SSI » - le « C » du classeur
   designe une mission de COORDINATION SSI, contrat distinct, et non un
   SSI concu a l'interieur d'un lot electricite) - il gagne.
5. CONSIGNER la lecture dans la fiche de collecte (ligne « Secteur » :
   citer l'entree du classeur telle quelle) ; si l'affaire est ABSENTE
   du classeur ou son domaine illisible -> question B a FT2E et choix
   provisoire argumente, jamais silencieux.
6. EN RECETTE (etape 10) : verifier sur le deploiement que la fiche
   repond au bon filtre de /references (compteurs de chips) et parait
   sur sa page /secteurs/<slug> - sondes : references/ref_037/
   sonde-filtres.mjs et sonde-fiche.mjs (URL a adapter).
   ⚠ Une page /secteurs/<slug> n'affiche que les 4 affaires les plus
   recentes du secteur (tri par numero decroissant) ; le filtre de
   /references, lui, montre tout. Une affaire a DOUBLE domaine doit
   etre controlee sur LES DEUX filtres et LES DEUX pages de secteur.
   ⚠ 20-045 est un numero de 2020 : sur les pages de secteur Tertiaire
   (12 fiches) et Coordination SSI (6 fiches), il sera parmi les plus
   ANCIENS et n'apparaitra probablement PAS dans le top 4. C'est un
   comportement de gabarit, pas un defaut - deja constate en N03 sur
   19-036. Le filtre de /references reste la mesure qui fait foi.
   Repartition attendue AVANT la N15 : L10 T12 I4 P3 C6 M3 E3 pour
   37 fiches, 41 en pondere (Yachtman T+C, Loti P+C, foyer CDAIR T+C et
   Central Hostel T+C comptent double). Mesuree le 2026-09-01 par
   references/ref_037/sonde-filtres.mjs sur le deploiement.

DOSSIER DU JOUR : « 20-045- Cabanes Urbaines - ALTERLAB » (164 fichiers,
234,3 Mo), classeur « 20045 · THE ROOF · T § C ».
⚠ TROIS NOMS ET DEUX MILLESIMES POUR LA MEME AFFAIRE - c'est le piege
principal de ce dossier, et il est deja mesure au depot :
-  le CLASSEUR ecrit « THE ROOF » et range l'affaire en « Finalisees en
   2023 » ;
-  le REPERTOIRE D'ARCHIVES ecrit « Cabanes Urbaines - ALTERLAB » ;
-  la PLAQUETTE 2024 ecrit « Les Cabanes Urbaines (+ essai de foyer SSI)
   | La Rochelle | 2022 | — / Alterlab » (docs/20-source-plaquette-2024.md
   l. 70), et l'audit de coherence des CV la confirme « 2022, coordination
   SSI » (meme fichier l. 90) ;
-  LE SITE PUBLIE DEJA le nom ET le millesime : src/content/secteurs/
   coordination-ssi.md l. 39 porte « des essais de foyers de controle
   d'efficacite - comme aux Cabanes Urbaines de La Rochelle en 2022 ».
Consequences a traiter, sans en trancher aucune en silence :
(a) la condition E1 est REMPLIE (nom deja publie par FT2E, trois fois) ;
(b) « THE ROOF » est vraisemblablement l'enseigne de l'exploitant et
    « Cabanes Urbaines » le nom de l'operation - a etablir sur la page de
    garde d'un contrat ou d'un marche, JAMAIS sur un nom de repertoire
    (piege N13 : « VOLTAREAO » au repertoire, « VoltAero » aux CV) ;
(c) LE MILLESIME DE LIVRAISON EST EN CONTRADICTION OUVERTE - plaquette,
    CV et site disent 2022, le classeur dit 2023. La regle du chantier
    est que LE CLASSEUR EST SUIVI et que la contradiction est ecrite en
    B1, jamais tranchee en silence ; mais ici une page publiee du site
    porte deja 2022, donc la question B doit demander explicitement s'il
    faut corriger `/secteurs/coordination-ssi` ;
(d) `src/content/secteurs/coordination-ssi.md` l. 39 nomme l'operation
    SANS LA LIER : poser le lien interne vers la fiche neuve, comme la
    N14 l'a fait sur `/secteurs/industriel-commercial`.
« ALTERLAB » au nom du dossier designe l'architecte - relever sa graphie
exacte au depot et sur les pieces avant d'ecrire `architecte`.
Aucun numero 20-045 n'est publie (verifie au grep de
src/content/projets/*.md le 2026-09-01).
ATTENTION DISQUE (~5 Go libres) : supprimer d'abord le repertoire extrait
de la session precedente -
C:\claude_code_dev_projects\ft2e_new_archives\2024 (le REPERTOIRE, pas le
ZIP ; il contient 2024/23-036- Extension bat 5-8 Fountaine Pajot - ASP) -
par python shutil.rmtree (le rm -rf est REFUSE par les permissions).
Puis extraire LE SEUL dossier du jour PAR PYTHON ZIPFILE (members filtres
sur « 20-045 » via zipfile.namelist() - les noms portent des accents en
mojibake, ne JAMAIS taper un chemin). Le ZIP est la source, il ne se
supprime pas.
Dossier de travail a creer : references/ref_038/
Slug cible : a etablir au depouillement (kebab-case sans accents,
verifier qu'il n'ecrase rien).

CE QUE LES N01-N14 ONT ETABLI (verifiable au depot) :
- ⚠ UNE THESE PEUT ETRE DEJA PUBLIEE - decouverte majeure de la N14, et
  elle se verifie AVANT de composer. La piece la plus singuliere du
  dossier Fountaine Pajot etait une note FT2E de recuperation d'energie :
  prescriptions CARSAT, tout air neuf, batteries a eau, boucle glycolee.
  C'est MOT POUR MOT le dispositif de la planche de
  `atelier-dufour-yachts-perigny`, deja en ligne, et la page
  /secteurs/industriel-commercial en publie deja les 38 000 m3/h. La
  these a donc ete ecartee du DESSIN (elle nourrit le recit) et la
  planche a porte une autre these du meme dossier. AVANT d'arreter une
  these, lire les `sous_titre` et `archetype_motif` des 37 planches
  (PYTHONIOENCODING=utf-8 python -c "..." sur public/images/projets/*/
  planche.json) : deux fiches voisines qui demontrent la meme chose sont
  une redite, que le protocole interdit explicitement.
- ⚠ UN DOSSIER D'ARCHIVES PEUT CONTENIR LES PIECES D'UNE AUTRE AFFAIRE
  (N13). Le sous-repertoire « 02-Production/05-Pro » de 21-095 portait
  17 fichiers de 21-093. Lire la PAGE DE GARDE (« N° affaire : … »,
  « Affaire n° : … ») de CHAQUE piece technique avant d'en tirer une
  valeur. La N14 a rejoue ce controle et trouve un dossier integre : le
  controle se fait, son resultat n'est pas acquis d'avance.
  Corollaire : une affaire peut n'avoir AUCUNE piece technique FT2E au
  dossier. La fiche reste publiable si trois familles de sources la
  soutiennent - programme du maitre d'ouvrage, comptes rendus de
  chantier, CV de l'equipe -, a condition que chacune soit NOMMEE en
  collecte et qu'aucune valeur de dimensionnement ne soit inventee.
- LES CV DE L'EQUIPE SONT UNE SOURCE FT2E (livrables/cv-ft2e/CV-FT2E.zip,
  edition aout 2026, six CV en .docx lisibles par zipfile+regex sur
  word/document.xml). La N13 y a trouve le perimetre reel de la mission
  et sa seule performance chiffree ; la N14 y a trouve la mention SSI
  qui a ouvert la question B2. Les interroger systematiquement au
  croisement commercial (etape 4), avec les docx sectoriels, le classeur
  et docs/20-source-plaquette-2024.md. ⚠ Il n'existe AUCUN docx
  sectoriel « industriel » : l'absence d'une affaire des onze docx ne
  dit rien contre elle.
- annee_livraison se pose sur le classeur ; quand pieces et classeur se
  contredisent, le classeur est suivi ET la contradiction est ecrite en
  B1, jamais tranchee en silence. Le PV de reception manque presque
  toujours - mais l'etai peut etre solide sans lui, et il se cherche a
  CINQ endroits : un CR d'OPC portant « RECEPTION DES TRAVAUX » en tete
  (N11) ; un CR annoncant la reception a une date precise avec le
  planning des semaines suivantes (N12) ; le BILAN DE FACTURATION, les
  honoraires d'AOR ne se facturant qu'une fois la mission finie (N12) ;
  le DERNIER CR DE CHANTIER, dont l'en-tete remplace « PROCHAINE
  REUNION » par « RECEPTION le JJ/MM/AAAA » (N13) ; et - nouveau en
  N14 - LE CALENDRIER EN TETE DE CHAQUE CR D'OPC, qui porte « Debut des
  travaux » et « Objectif reception » a date fixe, plus l'avancement en
  pourcentage de chacun des lots. ⚠ L'indice des honoraires d'AOR NE
  JOUE PAS quand le BET ne porte pas l'AOR a la repartition (cas N14 :
  FT2E a 0 % sur « Assistance aux operations de reception »).
- Le numero FT2E se releve sur page de garde CCTP (« Affaire n° : … »),
  cartouche de plan (« Reference Affaire : … »), etude thermique (pied
  de chaque page), contrats et propositions FT2E.
  ⚠ EN DERNIER RECOURS SEULEMENT, quand aucune piece FT2E n'existe au
  dossier (N13), il se releve sur le CLASSEUR + le nom du repertoire
  d'archives, et cela DOIT faire l'objet d'une question B.
- Les numeros des MANDATAIRES et donneurs d'ordres pietinent les
  pieces : ASP « 2301 », bon de commande EQUANS « 0023284014 », devis
  interne « 11-DPGF » (N14) ; SD Architectes « 21.17 » et « 21.45 »,
  marche public « 20210000200 », commande « 2024000451 », devis
  « 18.2024 », dossier RESE « TRX021847 » (N13) ; SEMDAS « 2507 » /
  « 2020/007 » / « 2020/071 », ARCHITEM « 1821 » (N10) ; Equans
  « 22984760 » (N09) ; CPAM « PA 2024 - MO01 » (N08). ⚠ Attention aussi
  aux DESIGNATIONS DE BATIMENT qui ressemblent a des numeros (« 5-8 »,
  « 8-1 », « 8-2 » chez Fountaine Pajot).
- ⚠ UN CCTP PEUT SE CONTREDIRE EN INTERNE (N11) : retenir le paragraphe
  QUI DENOMBRE, l'ecrire dans a_valider_ft2e, en faire une question B.
- ⚠ UNE NOTE DE CALCUL PEUT NE PAS BOUCLER (N14) : la note de
  recuperation d'energie annonce 350 kW de puissance totale, et ses
  postes font 329 puis 345. Ne JAMAIS composer un schema proportionnel
  (sankey, jauge, largeurs) sur des valeurs qui ne se ferment pas : une
  largeur proportionnelle AFFIRME une conservation que la source
  n'etablit pas. Ecrire l'ecart en a_valider_ft2e et en question B.
- ⚠ L'OPC PEUT CHANGER EN COURS DE CHANTIER (N12) ; en N13 et N14 il n'y
  en a eu qu'un. Ne pas presumer.
- NOMMER LE CLIENT FINAL : un nom deja publie par FT2E (plaquette,
  corpus secteurs, docx sectoriels, classeur, CV) se reprend, avec E1
  (N09 Airbus, N10 CDAIR, N11 Undertech, N12 Central Hostel, N13
  VoltAero, N14 Fountaine Pajot) ; un nom couvert par une clause de
  confidentialite reste hors slug et hors titre (N08 CPAM). Aucun nom de
  tiers ne monte jamais sur la planche - seul le nom d'OUVRAGE peut
  porter celui de l'occupant (« Extension Fountaine Pajot »,
  « Batiment VoltAero », « Ateliers Capsulae », « Parc Undertech »).
- ⚠ UNE GRAPHIE PEUT ETRE FAUSSE PARTOUT SAUF DANS LES CV (N13) : le
  repertoire ecrivait « VOLTAREAO », le programme « Voltaero », la
  plaquette « Voltareo », les CV « VOLTAERO ». Relever la graphie sur la
  page de garde d'un contrat ou d'un marche, jamais sur un nom de
  dossier. La N14 a de meme trouve « ASP achitectes » (coquille) aux
  deux CCTP contre « Agence Sebastien Pellereau » au programme et aux
  cartouches : c'est la graphie deja harmonisee au depot sur six fiches
  qui a ete retenue - VERIFIER TOUJOURS si l'acteur est deja nomme dans
  src/content/projets/*.md avant d'ecrire `architecte`.
- Archetypes apres N14 : boucle-fluide 10 - coupe-traversee 7 -
  tableau-electrique 7 (mecanisme `greffe`, Fountaine Pajot) -
  sankey-energie 6 - zonage-ssi 5 - chronologie-affaire 2 -
  planche-chiffree 0 SANS module. L'archetype se choisit sur la THESE,
  jamais sur le secteur ni sur le quota, mais a these egale preferer ce
  qui n'a pas servi depuis longtemps ; la dette de variete porte
  toujours sur boucle-fluide (10/37), et chronologie-affaire n'a pas
  servi depuis le corpus fondateur (admissible seulement si sa these est
  d'INGENIERIE, jamais le calendrier d'une operation). Une affaire de
  coordination SSI appellera naturellement `zonage-ssi` (5, dernier
  emploi N12 avec `convergence`) : verifier alors que la these differe
  des cinq deja publiees (abbaye, Salignac, Central Hostel/convergence,
  Loti/inversion, EHPAD Coulonges/transfert).
- Un mecanisme nouveau s'ecrit DANS le compositeur d'archetype
  (constantes prefixees par le mecanisme ; garde-fou de greffe sur le
  NOM DE LA FONCTION ET sur les prefixes de constantes - la N13 puis la
  N14 l'ont automatise : 6 fonctions et 18 constantes verifiees avant
  insertion en N14), et l'invariant octet se rejoue AVANT la greffe,
  APRES la greffe et APRES la derniere retouche. ⚠ L'INSTRUMENT EXISTE
  AU DEPOT ET SE REJOUE SEUL, NE PAS LE REECRIRE :
  `python scripts/planches/invariant.py` couvre les 6 compositeurs et
  les 37 dossiers (148/148 pieces au 2026-09-01),
  `python scripts/planches/invariant.py <archetype>` un seul.
  ⚠ Un dossier neuf dont la planche n'est pas encore composee fait
  chuter le compte de l'invariant (24/28 en cours de N14) : ce n'est pas
  une rupture, ce sont les pieces qui n'existent pas encore.
- ⚠ METTRE UNE ASSERTION DE DEPASSEMENT DANS LE COMPOSITEUR (N14, a
  reprendre) : chaque chaine dessinee est mesuree par `mesurer()` contre
  la largeur interieure de son contenant, versee dans une liste, et un
  `assert not trop` rompt la composition avant tout rendu. Elle a
  attrape sept debordements du premier jet que ni le build ni l'oeil
  n'auraient signales, et son resultat est publie au bloc `controles`
  (« 20 chaines mesurees, 0 depassement, marge la plus faible 3,7 px »).
- ⚠ NE PAS REECRIRE rendre_png.py : il est au depot depuis la N12, avec
  les deux pieges encodes (retrait de l'attribut style de racine par
  REGEX - sans quoi la vignette rend BLANCHE sans erreur - et fusion des
  filets a 8 chiffres). Usage :
  `python scripts/planches/rendre_png.py public/images/projets/<slug>
  <scratchpad>` ecrit planche.png 2400x1600 dans le dossier et, dans le
  scratchpad, les quatre controles (1152, vignette 274 et 296, appui
  552). REGARDER LES QUATRE. ⚠ Il s'appelle depuis la RACINE du depot :
  le cwd du shell persiste d'un appel a l'autre, et un `cd scripts/
  planches` anterieur le fait echouer sur un chemin double.
- ⚠ LE RENDU CAIROSVG N'A PAS LES POLICES DU SITE (mesure en N13,
  reconfirme en N14) : il retombe sur une police de substitution dont la
  chasse mono est ~7 a 8 % plus large que celle d'IBM Plex Mono.
  Consequence : le dernier caractere du cartouche de legende parait
  COUPE sur le PNG de controle des planches longues - « · 202 » au lieu
  de « · 2024 » sur l'EHPAD de Coulonges, sur VoltAero et sur Fountaine
  Pajot. Le navigateur, lui, rend juste (verifie sur le deploiement aux
  trois bandes en N14). NE PAS « corriger » la largeur du cartouche : la
  formule `mesurer(...) + 40` est commune aux 37 planches, et l'elargir
  pour un seul dossier ferait de lui l'exception.
- ECRIRE LES CHAINES COURBES DES L'ECRITURE - extraction planche.json
  COMPRISE. La recette, tenue en N11 a N14 : dans le script d'extraction
  lui-meme, avant ecriture, une assertion `"'" not in sortie`, une
  assertion `M not in sortie` sur le marqueur, et une assertion A
  L'EGALITE sur le COMPTE d'insecables - ce compte se LIT sur le source
  du script (nombre de marqueurs dans le litteral), jamais ecrit a la
  main : un nombre en dur se demode au premier ajout de chaine et
  l'assertion cesse de mesurer (releve en N13). ⚠ Le marqueur ne sert
  QU'A l'insecable : les apostrophes s'ecrivent directement en U+2019,
  que l'outil Write ne normalise pas. Un marqueur unique pour les deux
  usages est une collision (rate en N14, corrige avant execution).
  ⚠ Choisir un marqueur absent du texte : « # » entre en COLLISION avec
  les titres Markdown, prendre « @ ».
  La passe `python scripts/apostrophes-planches.py` (sans argument, en
  MESURE) n'a alors rien a courber - ni dans le JSON, ni dans le
  compositeur si ses libelles francais sont ecrits courbes eux aussi
  (0 sur 0 en N14). Les 476 apostrophes qu'elle REFUSE sont de la
  syntaxe de f-string : c'est le comportement voulu.
- Les avances calibrees de _tronc.mesurer sous-mesurent Archivo 600 au
  rendu d'environ 20 % (N08-N09) - prendre la marge DANS LE CODE
  (`mesurer(...) * 1.2`), pas a l'oeil.
- REGARDER LES PNG, ET CORRIGER CE QU'ON Y VOIT. La N14 a fait deux
  retouches que ni le build ni le bloc `controles` n'auraient
  signalees : une jauge qui finissait a 7 px de la limite pointillee
  qu'elle ne devait pas toucher (recalee sur le bord de l'armoire, 27 px
  gagnes), et une bande de vignette trop fine pour se distinguer de la
  limite qu'elle franchit a 274 px (4,0 -> 5,2 px). ⚠ Piege generique
  confirme en N13 ET N14 : deux traits qui se croisent doivent differer
  par autre chose que leur position - epaisseur, continuite, etiquette a
  fond papier (`_etiquette`).
- Quand aucune surface n'existe au dossier, la chercher dans les DOCX
  COMMERCIAUX (N12 : 1 025 m2 concordants sur trois docx) ; si elle n'y
  est pas non plus (N13), laisser `surface_m2` VIDE et porter au
  cartouche la grandeur qui compte l'ouvrage, avec question B.
  ⚠ Quand PLUSIEURS surfaces existent et divergent (N14 : 2 412 m2 au
  programme, 2 432,68 aux plans, 1 931,84 au plan SSI), retenir celle
  qui designe EXPLICITEMENT l'objet de la fiche, ecrire les autres en
  a_valider_ft2e, et n'en publier qu'une seule en prose - deux surfaces
  dans un meme recit invitent le lecteur a les additionner.
- Les insecables des heredocs bash sont normalisees DE FACON NON
  DETERMINISTE sur cette machine. DEUX VOIES, toutes deux eprouvees :
  (a) ecrire le .md en ESPACES ORDINAIRES et apostrophes droites par
  l'outil Write, puis passer `python scripts/injection-typographique.py
  <fichier>` qui pose les insecables, les guillemets et les U+2019 -
  c'est la voie des N12, N13 et N14, la plus sure, car AUCUNE insecable
  ne traverse Write ; (b) script Python avec marqueurs ASCII remplaces
  par chr(8239)/chr(160) et assertion A L'EGALITE comptee sur le source
  - la voie a suivre pour tout fichier que injection-typographique.py ne
  couvre pas (planche.json, plan du chantier, prompt de continuite).
  ⚠ injection-typographique.py protege les lignes d'enum du frontmatter
  (secteur, typologie, mission_ft2e) : une apostrophe DROITE tapee dans
  mission_ft2e y RESTE et casse le build - ecrire U+2019 des le script
  (piege N10, « Études d'exécution »). Il NE protege PAS
  secteur_secondaire : LE DOSSIER DU JOUR EN PORTE UN, verifier apres
  coup si sa valeur contient une apostrophe (« Études d'exécution /
  BIM » en porte une ; « Coordination SSI » n'en porte pas).
  ⚠ Il ne connait pas toutes les unites : « A » (amperes), « T »,
  « tonnes », « bars », « dBA » et le chiffre devant « × » lui echappent
  (releve en N13 et N14). Verifier au grep les unites rares apres
  passage, et les poser par un second script.
- Le hook Stop commite et pousse SEUL ce qui traine, et il PEUT
  COMMITTER LE LIVRABLE ENTIER sous l'intitule generique
  « chore(deploy): pousse l'etat de fin de session ». L'historique etant
  pousse sur un depot PARTAGE, il ne se reecrit pas. Pour l'eviter :
  garder les scripts a usage unique DANS LE SCRATCHPAD, hors depot
  (pratique des N13 et N14), COMMITTER TOT des que le build est vert, et
  reserver un second commit a la passe editoriale plutot que d'attendre
  l'agent de relecture avec un arbre de travail plein (⚠ livrables/
  porte deux fichiers non suivis anterieurs a la N02 - les laisser).
- /references/ est gitignore (motif ancre) - les pieces sources
  n'entrent JAMAIS au depot ; npm run preview ne mesure pas la
  performance ; Chrome refuse les fenetres sous 500 px (sonde iframe).
- La planche n'expose NI le millesime d'ouverture, NI montant, NI tiers
  (MOA, mandataire, architecte, installateur, MARQUES comprises), NI
  donnee nominative ; les designations internes (reperes de zone,
  numeros de tableau, « AGBT », « CVC 3 », « atelier 4 ») sont admises
  avec une entree a_valider_ft2e et une question E ; tout arbitrage de
  dessin va dans a_valider_ft2e (jamais vide).

DEROULER LE PIPELINE § 2 INTEGRALEMENT : depouillement (pdfinfo /
pdftotext, ou pymupdf via python subprocess avec les noms lus par
os.listdir ; les plans sans couche texte et les marches scannes se
lisent en rendant leurs pages en PNG par pymupdf, zoom 2-3 ; antiword
pour les .doc, xlrd pour les .xls, openpyxl pour les .xlsx,
extract-msg pour les .msg) -> CONTROLE DE LA PAGE DE GARDE DE CHAQUE
PIECE TECHNIQUE -> releve du numero NN-NNN sur piece FT2E ->
references/ref_038/ (3 a 8 pieces) -> croisement commercial
(references/docs_references/ - docx sectoriels ET classeur ODS - +
docs/20-source-plaquette-2024.md + livrables/cv-ft2e/CV-FT2E.zip +
grep de src/content/ pour ce que le site publie deja) -> fiche de
collecte (A/A+ remplies, B-E en questions, ligne Secteur citant le
classeur, DECISION Q3 motivee en tete) -> LECTURE DES 37 SOUS-TITRES DE
PLANCHE pour verifier qu'aucune these voisine n'est deja publiee ->
fiche src/content/projets/<slug>.md (SECTEUR ET SECTEUR_SECONDAIRE
RELEVES AU CLASSEUR ; taxonomie ACTUELLE ; lieu avec code postal entre
parentheses ; synthese 480-780 ; >= 5 liens internes ; jamais de numero
d'affaire NI de millesime d'ouverture en prose ; convention numerale
finale - nom du NOMBRE en un seul mot en lettres, nombre COMPOSE en
chiffres, unites et mesures toujours en chiffres, citations intouchees ;
verifier par `python scripts/releve-numeral.py`, dont la section
« Nombres COMPOSES ecrits en lettres » doit rendre 0) ->
PLANCHE complete (extraction avec a_valider_ft2e non vide, apostrophes
courbes des l'ecriture, composition par scripts/planches/<archetype>.py
avec assertion de depassement, rendus par scripts/planches/rendre_png.py
depuis la RACINE, controles a 1152 / carte 274-296 / appui 552 -
REGARDER les quatre PNG -, apostrophes-planches.py en MESURE,
invariant.py, verser.py) ->
qualite (typecheck 0, build vert 61 pages, editorial-reviewer EN
LECTURE SEULE - ses outils d'edition normalisent les insecables,
appliquer ses constats par script -, controle-liens-internes 38/38 a 5,
controle-numeros-affaire 0 fuite, releve-numeral sans ecart nouveau)
-> COMMIT UNIQUE fiche+planche+compositeur (content(references): ajoute
la fiche reelle <nom> et sa planche ; git ls-remote avant, depot
partage) -> push (le push deploie), curl de la fiche AVEC barre oblique
finale + marqueur de build, rendu controle aux trois bandes (sonde
iframe pour les largeurs telephone : references/ref_037/sonde-fiche.mjs,
slug et URL a adapter) ET CONTROLE DE L'INDEXATION SECTORIELLE SUR LES
DEUX DOMAINES (point 6, sonde references/ref_037/sonde-filtres.mjs) ->
ligne de suivi au plan -> PROMPT DE LA SESSION N16 en annexe du plan
(script Python ou Write, jamais un long heredoc) et reproduit
integralement dans le message final. Le prompt N16 REPREND le bloc
« REGLE D'INDEXATION SECTORIELLE » tel quel (repartition remise a jour)
ET porte le deuxieme dossier de la tranche 2023, choisi parmi les quatre
restants (21-086 ADEI, 21-074 AP Yacht, 20-071 EIFFAGE, 21-029 La
Flotte) selon la regle par defaut : les mieux documentes d'abord,
couverture des secteurs, dossiers minces en fin.

PIEGES VERIFIES EN N01-N14 (en plus de ceux des annexes A et B, tous
confirmes) :
- Un heredoc long se fait TRONQUER ou refuser silencieusement - bash
  COMME python : gros fichiers et scripts par l'outil Write PUIS
  execution ; le cwd du shell PERSISTE d'un appel a l'autre : chemins
  absolus ou cd explicite en tete de chaque commande.
- L'extraction zipfile a recree la racine interne en N10
  (ft2e_new_archives\2024\2024\<dossier>) mais PAS en N11-N14
  (ft2e_new_archives\2024\<dossier>) : ne jamais presumer la
  profondeur, descendre par os.listdir.
- verser.py repond « deja verse » quand `planche:` est ecrit
  directement au frontmatter (fiche neuve) : ses controles 1 a 3 - les
  cinq pieces, l'archetype nomme, a_valider_ft2e non vide, le SVG sous
  40 Ko avec role="img" et sans width/height - ont TOUS tourne avant
  ce message. C'est un succes.
- PYTHONIOENCODING=utf-8 sur cette machine, et `python -c` sans lui
  plante en UnicodeEncodeError sur la moindre insecable ; ⚠ `python -c`
  avec un chemin Windows entre quotes casse aussi sur `'C:\'` (la
  contre-oblique echappe la quote) - utiliser os.sep ou des heredocs.
  ⚠ pymupdf n'ouvre PAS un chemin de style MSYS (`/c/...`) : lui donner
  un chemin Windows, ou faire un `cd` dans le repertoire et passer un
  nom relatif (piege N14).
  ⚠ `fc-list` n'existe pas sur cette machine et son appel par subprocess
  plante en UnicodeDecodeError cp1252 : ne pas chercher a inventorier
  les polices par la.

Portee de commit : content(references). Un changement de schema Zod
eventuel passe par le sous-agent content-modeller et va dans le MEME
commit que public/admin/config.yml.

Termine par le prompt de lancement de la session N16, en annexe du
plan du chantier et reproduit integralement dans ton message final -
la regle de continuite est dans CLAUDE.md parce qu'elle a ete manquee
deux fois.
````


## Annexe P — prompt de lancement de la session N16 (à coller tel quel en session neuve)

```
Session N16/27 - FT2E v3 : chantier des 27 nouvelles fiches references.
Seizieme dossier - DEUXIEME de la tranche « Finalisees en 2023 ».

Contexte. FT2E v3 est le site institutionnel du bureau d'etudes FT2E
(La Rochelle), Astro 6 statique, deploye en demonstration client sur
https://ft2e-v3.vercel.app (indexation verrouillee - ne pas y toucher).
Le catalogue porte 38 fiches reelles (23 + N01 Portes-en-Re + N02 Fors +
N03 Aurora + N04 Loti + N05 Saint-Sauveur + N06 L'Houmeau + N07 Louise
Magnan + N08 bornes IRVE + N09 comptage Airbus + N10 foyer CDAIR +
N11 parc Undertech + N12 auberge Central Hostel + N13 batiment VoltAero +
N14 extension Fountaine Pajot + N15 Cabanes Urbaines), chacune illustree
d'une planche de schema de principe (cinq pieces par dossier).
Objectif : 50 fiches. 1 session = 1 dossier, close par le prompt de la
suivante.

LE ZIP DE LA TRANCHE 2023 EST DEJA SUR LE DISQUE :
C:\claude_code_dev_projects\ft2e_new_archives\2023.zip (446 Mo, 670
entrees, racine interne « 2023/ », un repertoire par affaire). Quatre
dossiers y restent, tous absents du site (verifie au grep de
src/content/projets/*.md le 2026-09-01) :
-  184 fichiers, 178,8 Mo : « 21-086 - Audit chauffage sites ADEI »        (classeur M)  <- DOSSIER DU JOUR
-   89 fichiers,  40,8 Mo : « 21-074- Projet AP Yacht - CATANA Group-  Cab SIMONEAU » (classeur I)
-   72 fichiers,  39,6 Mo : « 20-071- Bureaux EIFFAGE St Jean D'Angely - Impact Urbanisme » (classeur T)
-   54 fichiers,  14,9 Mo : « 21-029 - Ecole primaire et maternelle - La Flotte en Re » (classeur M)
IL N'Y A DONC AUCUNE QUESTION A POSER EN OUVERTURE : derouler directement.

⚠ NE JAMAIS conclure « mince » ni « riche » sur le seul compte de fichiers :
quatre dementis en N08-N09 (mince qui etait riche), un dementi INVERSE en
N13 (« 21-095 » annoncait 72 fichiers dont 17 appartenaient a l'affaire
21-093), et deux dossiers integres en N14 et N15. C'est la PAGE DE GARDE
qui dit a quelle affaire une piece appartient, jamais le repertoire qui la
contient. Verifier la page de garde de chaque CCTP, DPGF, estimation,
rapport d'audit et plan AVANT d'en tirer la moindre valeur.

⚠ CE QUI RESTE APRES 2023, ET UN ECART A SIGNALER. Le classeur ODS porte,
apres la tranche 2023 : « Finalisees en 2022 » (4 : 19087 Batiment SSLIA I,
20024 INNOVIA-GAELIC I, 20039 Videosurveillance CH Rochefort M, 22037 Audit
chambre des metiers M), « Finalisees en 2020 » (2 : 19008 Batiment
industriel Aeroport LR ELIXIR I, 20058 Diag legionelles du port de plaisance
M) et « Finalisees en 2019 » (1 : 18026 Atelier numerique Fountaine Pajot I).
Soit 4 (2023) + 4 + 2 + 1 = 11 dossiers restants pour 38 fiches en ligne :
LE CLASSEUR NE MENE QU'A 49, PAS A 50. A porter en question a FT2E des
cette session : manque-t-il une affaire au classeur, ou l'objectif de 50
se solde-t-il a 49 ? Ne pas fabriquer une fiche pour combler l'ecart.
Les ZIP 2019.zip et 2022.zip SONT DEJA SUR LE DISQUE ; celui de la tranche
2020 devra etre demande en ouverture de la session qui closera 2022.

LIRE D'ABORD, dans cet ordre :
1. docs/superpowers/plans/2026-08-27-chantier-27-nouvelles-fiches.md -
   LE PLAN : § 1 (ce qui a change), § 2 (pipeline 12 etapes), § 3
   (reponses consignees Q1/Q2 2024 + complement N02 : le classeur fait
   foi ; Q3 = regle des dossiers minces, defaut reconduit), § Suivi
   (lignes N01 a N15), annexe P (ce prompt).
2. docs/superpowers/plans/2026-08-07-chantier-references-reelles.md -
   § Contraintes globales + § Protocole de session + § Regle des
   dossiers minces.
3. docs/superpowers/specs/2026-08-12-planches-references-protocole.md -
   revision 5 EN ENTIER.
4. CLAUDE.md, .claude/rules/content-collections.md et french-editorial.md.
Etalons : src/content/projets/creche-oranger-perigny.md (fiche) et, pour
une affaire d'AUDIT sans travaux (typologie « Etude ») :
src/content/projets/cuisine-groupe-scolaire-villedoux.md et
src/content/projets/atelier-dufour-yachts-perigny.md - les deux seules
fiches « Monotechnique - Audit » du catalogue avec l'audit de Villedoux.
Voir aussi src/content/projets/cabanes-urbaines-la-rochelle.md +
public/images/projets/cabanes-urbaines-la-rochelle/ +
references/ref_038/ (fiche de collecte N15, avec sa DECISION Q3 en tete -
c'est elle qui documente le piege des trois noms et des deux millesimes).
Les sondes de recette vivent dans references/ref_038/ (sonde-fiche.mjs,
sonde-filtres.mjs - URL, slug et secteur a adapter).

REGLE D'INDEXATION SECTORIELLE - etablie le 2026-08-27, A APPLIQUER A
LA REDACTION DE CHAQUE FICHE (etape 6 du pipeline), pas apres coup :
« REFERENCES SITE FT2E.ods » (references/docs_references/, classeur
fourni par FT2E) FAIT FOI pour le classement sectoriel. Concretement,
AVANT d'ecrire le frontmatter :
1. Ouvrir le classeur (python zipfile sur content.xml, ou pandoc) et y
   retrouver l'affaire PAR SON NUMERO (graphie sans tiret : « 21086 »).
2. En relever le domaine (legende : L Logements / T Tertiaire & ERP /
   I Industriel / P Patrimoine / C Coordination SSI /
   M Monotechnique-Audit / E EXE) -> champ `secteur`.
3. Si le classeur porte un domaine DOUBLE (« T § C ») : le premier est
   le `secteur`, le second va au champ `secteur_secondaire` (optionnel
   au schema depuis le 2026-08-27, garde-fou « doit differer ») - la
   fiche parait alors dans les deux filtres et sur les deux pages de
   secteur. Precedents : hotel-yachtman (T § C), maison-pierre-loti-
   rochefort (P § C, N04), foyer-cdair-saint-martin-de-re (T § C, N10),
   auberge-central-hostel-la-rochelle (T § C, N12),
   cabanes-urbaines-la-rochelle (T § C, N15).
   LE DOSSIER DU JOUR EST A DOMAINE SIMPLE : 21086 est « M ».
4. JAMAIS de deduction depuis le dossier, l'usage RT ou le nom de
   l'operation : la N02 penchait « Industriel » pour Fors, le classeur
   dit T - et les 25 fiches ont du etre re-referencees le soir meme
   (7 bascules, commits ce334b2/09270a3). Le classeur peut contredire
   l'intuition (Saint-Rogatien, pole commercial : I ; Fors, pole
   commercial : T ; 23083 « plan de comptage Airbus » : E et non M ;
   23099 « CPAM » : M - IRVE, pas T ; 23036 Fountaine Pajot : I SIMPLE
   alors que le CV annonce « CFO / CFA / SSI » ; 20045 « THE ROOF »,
   salle d'escalade et atelier de luthier : T § C et non I) - il gagne.
5. CONSIGNER la lecture dans la fiche de collecte (ligne « Secteur » :
   citer l'entree du classeur telle quelle) ; si l'affaire est ABSENTE
   du classeur ou son domaine illisible -> question B a FT2E et choix
   provisoire argumente, jamais silencieux.
6. EN RECETTE (etape 10) : verifier sur le deploiement que la fiche
   repond au bon filtre de /references (compteurs de chips) et parait
   sur sa page /secteurs/<slug> - sondes : references/ref_038/
   sonde-filtres.mjs et sonde-fiche.mjs (URL a adapter).
   ⚠ Une page /secteurs/<slug> n'affiche que les 4 affaires les plus
   recentes du secteur (tri par numero decroissant) ; le filtre de
   /references, lui, montre tout. Une affaire a DOUBLE domaine doit
   etre controlee sur LES DEUX filtres et LES DEUX pages de secteur.
   ⚠ 21-086 est un numero de 2021 et le secteur « Monotechnique - Audit »
   ne porte que 3 fiches : elle devrait donc paraitre dans le top 4 de
   /secteurs/monotechnique. Le filtre de /references reste la mesure qui
   fait foi.
   Repartition attendue AVANT la N16 : L10 T13 I4 P3 C7 M3 E3 pour
   38 fiches, 43 en pondere (Yachtman T+C, Loti P+C, foyer CDAIR T+C,
   Central Hostel T+C et Cabanes Urbaines T+C comptent double). Mesuree
   le 2026-09-01 par references/ref_038/sonde-filtres.mjs sur le
   deploiement.

DOSSIER DU JOUR : « 21-086 - Audit chauffage sites ADEI » (184 fichiers,
178,8 Mo), classeur « 21086 · Audit chauffage sites ADEI · M ».
C'est le PLUS GROS dossier restant de la tranche, et le premier AUDIT du
chantier des 27. Points d'attention connus AVANT ouverture :
(a) « ADEI » est vraisemblablement une association d'aide aux personnes
    handicapees de Charente-Maritime - le nom est celui d'un TIERS et sa
    graphie doit se relever sur la page de garde d'un contrat, d'un
    rapport d'audit ou d'un marche, JAMAIS sur le nom de repertoire
    (piege N13 « VOLTAREAO », piege N15 « ESCLA'BLOC ») ;
(b) « sites » au pluriel : l'affaire porte vraisemblablement sur PLUSIEURS
    etablissements. Verifier combien, et lesquels, sur les pieces - et se
    demander tres tot si la fiche parle d'un audit MULTI-SITES (une seule
    fiche) ou de plusieurs affaires. Le classeur n'en donne qu'une ;
(c) la typologie « Etude » existe au schema pour les missions sans
    travaux (audit, faisabilite) : ne PAS atterrir de force en
    « Rehabilitation » ;
(d) un audit produit des CHIFFRES (consommations, ratios, temps de
    retour) : la regle dure 1 du protocole s'applique sans indulgence -
    toute valeur portee a la planche doit etre citable dans la fiche ;
(e) ⚠ **une note ou un rapport peut ne pas boucler** (piege N14, note de
    recuperation d'energie : 350 kW annonces, 329 puis 345 aux postes).
    Sur un audit, verifier que les sous-totaux somment AVANT de composer
    quoi que ce soit de proportionnel. La N15 a pu composer des barres
    proportionnelles precisement parce que son comptage bouclait
    (85 + 2 + 16 = 103, exactement le bilan de puissance).
Aucun numero 21-086 n'est publie (verifie au grep de
src/content/projets/*.md le 2026-09-01).
ATTENTION DISQUE (~5 Go libres) : supprimer d'abord le repertoire extrait
de la session precedente -
C:\claude_code_dev_projects\ft2e_new_archives\2023 (le REPERTOIRE, pas le
ZIP ; il contient 2023/20-045- Cabanes Urbaines - ALTERLAB) - par python
shutil.rmtree (le rm -rf est REFUSE par les permissions).
Puis extraire LE SEUL dossier du jour PAR PYTHON ZIPFILE (members filtres
sur « 21-086 » via zipfile.namelist() - les noms portent des accents en
mojibake, ne JAMAIS taper un chemin). Le ZIP est la source, il ne se
supprime pas.
⚠ L'extraction a recree la racine interne en N10 et en N15
(ft2e_new_archives\2023\2023\<dossier>) mais PAS en N11-N14 : ne jamais
presumer la profondeur, descendre par os.listdir.
Dossier de travail a creer : references/ref_039/
Slug cible : a etablir au depouillement (kebab-case sans accents,
verifier qu'il n'ecrase rien).

CE QUE LES N01-N15 ONT ETABLI (verifiable au depot) :
- ⚠ UNE THESE PEUT ETRE DEJA PUBLIEE - decouverte de la N14, et elle se
  verifie AVANT de composer. AVANT d'arreter une these, lire les
  `sous_titre` et `archetype_motif` des 38 planches
  (PYTHONIOENCODING=utf-8 python -c "..." sur public/images/projets/*/
  planche.json) : deux fiches voisines qui demontrent la meme chose sont
  une redite, que le protocole interdit explicitement. La N15 a ecarte
  la geometrie « 14 zones -> 1 zone de mise en securite » PARCE QU'ELLE
  EST DEJA PUBLIEE (Central Hostel, mecanisme `convergence`) et a
  reporte sa demonstration sur la CAUSE - le plancher qui manque.
- ⚠ UN DOSSIER D'ARCHIVES PEUT CONTENIR LES PIECES D'UNE AUTRE AFFAIRE
  (N13). Lire la PAGE DE GARDE (« N° affaire : ... », « Affaire n° : ... »)
  de CHAQUE piece technique avant d'en tirer une valeur. Les N14 et N15
  ont rejoue ce controle et trouve des dossiers integres : le controle se
  fait, son resultat n'est pas acquis d'avance.
  Corollaire : une affaire peut n'avoir AUCUNE piece technique FT2E au
  dossier. La fiche reste publiable si trois familles de sources la
  soutiennent - programme du maitre d'ouvrage, comptes rendus de
  chantier, CV de l'equipe -, a condition que chacune soit NOMMEE en
  collecte et qu'aucune valeur de dimensionnement ne soit inventee.
- LES CV DE L'EQUIPE SONT UNE SOURCE FT2E (livrables/cv-ft2e/CV-FT2E.zip,
  edition aout 2026, six CV en .docx lisibles par zipfile+regex sur
  word/document.xml). La N13 y a trouve le perimetre reel de la mission ;
  la N14 la mention SSI qui a ouvert une question B ; la N15 y a lu
  « 2022 - CABANES URBAINES - Conception electricite CFO/CFA/coordination
  SSI », qui a permis de RECONCILIER un conflit de millesime (2022 =
  conception, 2023 = reception). Les interroger systematiquement au
  croisement commercial (etape 4), avec les docx sectoriels, le classeur
  et docs/20-source-plaquette-2024.md. ⚠ Il n'existe AUCUN docx
  sectoriel « industriel » : l'absence d'une affaire des onze docx ne
  dit rien contre elle.
- annee_livraison se pose sur le classeur ; quand pieces et classeur se
  contredisent, le classeur est suivi ET la contradiction est ecrite en
  B1, jamais tranchee en silence. Le PV de reception manque presque
  toujours - mais il se cherche a SIX endroits : un CR d'OPC portant
  « RECEPTION DES TRAVAUX » en tete (N11) ; un CR annoncant la reception a
  une date precise avec le planning des semaines suivantes (N12) ; le
  BILAN DE FACTURATION, les honoraires d'AOR ne se facturant qu'une fois
  la mission finie (N12) ; le DERNIER CR DE CHANTIER, dont l'en-tete
  remplace « PROCHAINE REUNION » par « RECEPTION le JJ/MM/AAAA » (N13) ;
  LE CALENDRIER EN TETE DE CHAQUE CR D'OPC (N14) ; et - nouveau en N15 -
  L'EN-TETE DES DERNIERS CR, qui porte « Reception du chantier : JJ/MM/AA »
  et « Passage de la commission de securite le JJ/MM/AA » plusieurs
  semaines a l'avance (CR n°38 a 41 des Cabanes Urbaines). Sur une affaire
  a SSI, le PV DE RECEPTION DU SSI et l'ATTESTATION DE MISE EN SERVICE du
  constructeur donnent en outre une date au jour pres. ⚠ L'indice des
  honoraires d'AOR NE JOUE PAS quand le BET ne porte pas l'AOR a la
  repartition (cas N14).
- Le numero FT2E se releve sur page de garde CCTP (« Affaire n° : ... »),
  cartouche de plan (« Reference Affaire : ... »), etude thermique (pied
  de chaque page), contrats et propositions FT2E, et - N15 - EN PIED DE
  CHAQUE PAGE d'une note methodologique (« Affaire N° 20045-CSSI »).
  ⚠ Un meme numero peut porter des INDICES de contrat (20-045, 20 045 A,
  20 045 B, 20 045 C, 20-045-CSSI) : c'est UNE affaire, pas cinq.
  ⚠ EN DERNIER RECOURS SEULEMENT, quand aucune piece FT2E n'existe au
  dossier (N13), il se releve sur le CLASSEUR + le nom du repertoire
  d'archives, et cela DOIT faire l'objet d'une question B.
- Les numeros des MANDATAIRES et donneurs d'ordres pietinent les
  pieces : declaration de travaux « DT 2022090895299S16 » et references
  constructeur « NUG31440 » (N15) ; ASP « 2301 », bon de commande EQUANS
  « 0023284014 » (N14) ; SD Architectes « 21.17 », marche public
  « 20210000200 », dossier RESE « TRX021847 » (N13) ; SEMDAS « 2507 »,
  ARCHITEM « 1821 » (N10) ; Equans « 22984760 » (N09) ; CPAM
  « PA 2024 - MO01 » (N08). ⚠ Attention aussi aux DESIGNATIONS DE
  BATIMENT qui ressemblent a des numeros (« 5-8 » chez Fountaine Pajot).
- ⚠ UN CCTP PEUT SE CONTREDIRE EN INTERNE (N11) : retenir le paragraphe
  QUI DENOMBRE, l'ecrire dans a_valider_ft2e, en faire une question B.
- ⚠ RECOMPTER LIGNE A LIGNE CE QU'ON ANNONCE (N15). « Treize zones » a
  ete ecrit d'apres une lecture rapide du tableau de correlation ; le
  recomptage ligne a ligne en donne QUATORZE (11 ZDA + 3 ZDM), et
  l'erreur avait deja traverse la fiche de collecte et le frontmatter.
  Tout effectif porte a une fiche ou a une planche se recompte sur la
  piece, jamais sur son souvenir.
- ⚠ UNE NOTE DE CALCUL PEUT NE PAS BOUCLER (N14). Ne JAMAIS composer un
  schema proportionnel (sankey, jauge, largeurs) sur des valeurs qui ne
  se ferment pas. A l'inverse, quand le comptage BOUCLE (N15 : 85 + 2 +
  16 = 103, exactement le bilan de puissance), la proportion est
  legitime - et une COMPARAISON de deux mesures independantes (deux
  durees) l'est aussi, a condition d'ecrire au bloc `controles` qu'aucune
  somme n'est affirmee.
- ⚠ L'OPC PEUT CHANGER EN COURS DE CHANTIER (N12) ; en N13, N14 et N15 il
  n'y en a eu qu'un. Ne pas presumer.
- NOMMER LE CLIENT FINAL : un nom deja publie par FT2E (plaquette,
  corpus secteurs, docx sectoriels, classeur, CV) se reprend, avec E1
  (N09 Airbus, N10 CDAIR, N11 Undertech, N12 Central Hostel, N13
  VoltAero, N14 Fountaine Pajot, N15 Cabanes Urbaines) ; un nom couvert
  par une clause de confidentialite reste hors slug et hors titre (N08
  CPAM). ⚠ **Chercher aussi dans le CORPUS SECTEURS** : la N15 a
  decouvert qu'une PHOTOGRAPHIE de son affaire etait deja publiee sur
  /secteurs/coordination-ssi (l'essai de foyer reel) - le grep de
  src/content/ doit couvrir les legendes et les alt des cliches, pas
  seulement la prose. Aucun nom de tiers ne monte jamais sur la planche -
  seul le nom d'OUVRAGE peut porter celui de l'occupant.
- ⚠ UNE GRAPHIE PEUT ETRE FAUSSE PARTOUT SAUF DANS LES CV (N13), ET LES
  PIECES D'UNE MEME AFFAIRE PEUVENT SE CONTREDIRE ENTRE ELLES (N15 :
  ESCAL'BLOC / ESCLA'BLOC / ESCALBLOC dans trois pieces FT2E). Relever la
  graphie sur la page de garde d'un contrat ou d'un marche, retenir la
  majoritaire, ecrire la divergence en question B - et VERIFIER TOUJOURS
  si l'acteur est deja nomme dans src/content/projets/*.md avant d'ecrire
  `architecte` ou `moa`.
- ⚠ UN SITE PUBLIE PEUT PORTER UNE DATE FAUSSE (N15). /secteurs/
  coordination-ssi datait de 2022 un essai de foyer realise le 07/09/2023.
  Corriger une page publiee est legitime quand une piece FT2E tranche,
  MAIS cela s'ecrit en question B et se signale au message final - jamais
  en silence.
- ⚠ L'AGENT DE RELECTURE TROUVE DES ERREURS DE FAIT SANS AVOIR LES PIECES
  (N15). Il n'a pas su que la fiche se trompait sur les centrales de
  traitement d'air : il a seulement remarque que la phrase annoncait
  QUATRE centrales et n'en enumerait que TROIS. Le CCTP rouvert a donne
  trois centrales double flux - et les trois debits publies etaient poses
  sur les MAUVAIS ORGANES (1 800 attribue a l'existant au lieu de 1 300,
  2 455 a la salle de spectacle au lieu de l'extension). C'est la faute
  que la regle dure 1 designe comme la plus grave. LECON : traiter chaque
  question de compte de l'agent comme une piste a verifier SUR LA PIECE,
  jamais comme une remarque de style ; et se relire soi-meme sur le
  critere « les items enumeres correspondent-ils au nombre annonce ? ».
  ⚠ Corollaire : lui donner en contexte les faits etablis sur piece (c'est
  ce qui lui a permis de croiser), et lui demander EXPLICITEMENT les
  chaines exactes avant/apres - il travaille EN LECTURE SEULE, ses outils
  d'edition normalisent les insecables du depot.
- Archetypes apres N15 : boucle-fluide 10 - coupe-traversee 7 -
  tableau-electrique 7 - sankey-energie 6 - zonage-ssi 6 (mecanisme
  `compensation`, Cabanes Urbaines) - chronologie-affaire 2 -
  planche-chiffree 0 SANS module. L'archetype se choisit sur la THESE,
  jamais sur le secteur ni sur le quota, mais a these egale preferer ce
  qui n'a pas servi depuis longtemps ; la dette de variete porte
  toujours sur boucle-fluide (10/38), et chronologie-affaire n'a pas
  servi depuis le corpus fondateur (admissible seulement si sa these est
  d'INGENIERIE, jamais le calendrier d'une operation). ⚠ Un AUDIT
  multi-sites pourrait etre le premier cas ou `planche-chiffree` se
  justifie - son module N'EXISTE PAS : si le dossier l'exige, la decision
  est de L'ECRIRE ou de retirer l'archetype de la liste fermee (§ 1 du
  plan), jamais de bricoler.
- Un mecanisme nouveau s'ecrit DANS le compositeur d'archetype
  (constantes prefixees par le mecanisme ; garde-fou de greffe sur le
  NOM DE LA FONCTION ET sur les prefixes de constantes - automatise
  depuis la N13 : en N15, 5 fonctions et 25 constantes CP_ verifiees, plus
  un controle que les helpers reutilises existent bien), et l'invariant
  octet se rejoue AVANT la greffe, APRES la greffe et APRES la derniere
  retouche. ⚠ L'INSTRUMENT EXISTE AU DEPOT ET SE REJOUE SEUL, NE PAS LE
  REECRIRE : `python scripts/planches/invariant.py` couvre les 6
  compositeurs et les 38 dossiers (152/152 pieces au 2026-09-01),
  `python scripts/planches/invariant.py <archetype>` un seul.
  ⚠ Un dossier neuf dont la planche n'est pas encore composee fait
  chuter le compte de l'invariant : ce n'est pas une rupture, ce sont
  les pieces qui n'existent pas encore.
- ⚠ METTRE UNE ASSERTION DE DEPASSEMENT DANS LE COMPOSITEUR (N14, rejouee
  en N15 et payante des le premier jet) : chaque chaine dessinee est
  mesuree par `mesurer()` contre la largeur interieure de son contenant,
  versee dans une liste, et un `assert not trop` rompt la composition
  avant tout rendu. En N15 elle a arrete deux debordements de colonne que
  ni le build ni l'oeil n'auraient signales, et son resultat est publie
  au bloc `controles` (« 36 chaines mesurees, 0 depassement, marge la plus
  faible 14,8 px »).
- ⚠ NE PAS REECRIRE rendre_png.py : il est au depot depuis la N12, avec
  les deux pieges encodes (retrait de l'attribut style de racine par
  REGEX - sans quoi la vignette rend BLANCHE sans erreur - et fusion des
  filets a 8 chiffres). Usage :
  `python scripts/planches/rendre_png.py public/images/projets/<slug>
  <scratchpad>` ecrit planche.png 2400x1600 dans le dossier et, dans le
  scratchpad, les quatre controles (1152, vignette 274 et 296, appui
  552). REGARDER LES QUATRE. ⚠ Il s'appelle depuis la RACINE du depot.
- ⚠ LE RENDU CAIROSVG N'A PAS LES POLICES DU SITE (N13, reconfirme en
  N14) : il retombe sur une police de substitution dont la chasse mono est
  ~7 a 8 % plus large que celle d'IBM Plex Mono. Consequence : le dernier
  caractere du cartouche de legende parait COUPE sur le PNG de controle
  des planches longues. Le navigateur, lui, rend juste. NE PAS
  « corriger » la largeur du cartouche : la formule `mesurer(...) + 40`
  est commune aux 38 planches. ⚠ La MEME sous-mesure vaut pour tout fond
  papier pose derriere un mono (N15 : le fond du libelle du plan manquant
  a du prendre 8 % de marge, sans quoi le trait interrompu mordait sur la
  derniere lettre).
- ECRIRE LES CHAINES COURBES DES L'ECRITURE - extraction planche.json
  COMPRISE. La recette, tenue en N11 a N15 : dans le script d'extraction
  lui-meme, avant ecriture, une assertion `"'" not in sortie`, une
  assertion `M not in sortie` sur chaque marqueur, et une assertion A
  L'EGALITE sur le COMPTE d'insecables - ce compte se LIT sur le source
  du script (nombre de marqueurs dans le litteral), jamais ecrit a la
  main. ⚠ La N15 a employe DEUX marqueurs distincts, «   » pour la fine
  U+202F et «   » pour l'insecable U+00A0, avec deux assertions comptees
  separement : c'est plus sur qu'un marqueur unique, et cela evite la
  collision relevee en N14. Ne PAS prendre « # » (collision avec les
  titres Markdown).
  La passe `python scripts/apostrophes-planches.py` (sans argument, en
  MESURE) n'a alors rien a courber - 0 sur 0 en N14 comme en N15. Les
  apostrophes qu'elle REFUSE sont de la syntaxe de f-string : c'est le
  comportement voulu.
- Les avances calibrees de _tronc.mesurer sous-mesurent Archivo 600 au
  rendu d'environ 20 % (N08-N09) - prendre la marge DANS LE CODE
  (`mesurer(...) * 1.2`), pas a l'oeil.
- REGARDER LES PNG, ET CORRIGER CE QU'ON Y VOIT. La N15 a fait quatre
  retouches que ni le build ni le bloc `controles` n'auraient signalees :
  un fond papier trop juste sous un mono ; un trait d'allumage pose a
  l'origine de chaque barre, donc invisible sous elle, remplace par UNE
  ligne de zero traversant les deux rangees ; un appui laissant 123 px de
  vide en pied, aere a 51 px avec une ligne mono par bloc ; et un libelle
  de plancher qui, sur un appui de 192 px de large, masquait le trait
  presque entier - passe SOUS le trait. ⚠ Piege generique confirme en N13,
  N14 et N15 : deux traits qui se croisent doivent differer par autre
  chose que leur position - epaisseur, continuite, etiquette a fond
  papier (`_etiquette`).
- Quand aucune surface n'existe au dossier, la chercher dans les DOCX
  COMMERCIAUX (N12) ; si elle n'y est pas non plus (N13), laisser
  `surface_m2` VIDE et porter au cartouche la grandeur qui compte
  l'ouvrage, avec question B. ⚠ Quand PLUSIEURS surfaces existent et
  divergent (N14), retenir celle qui designe EXPLICITEMENT l'objet de la
  fiche, ecrire les autres en a_valider_ft2e, et n'en publier qu'une seule
  en prose. ⚠ Quand la seule surface au dossier ne couvre qu'une PARTIE de
  l'ouvrage (N15 : 503 m2 utiles pour la seule extension), la publier en
  le disant explicitement dans le recit, et poser la question B.
- Les insecables des heredocs bash sont normalisees DE FACON NON
  DETERMINISTE sur cette machine. DEUX VOIES, toutes deux eprouvees :
  (a) ecrire le .md en ESPACES ORDINAIRES et apostrophes droites par
  l'outil Write, puis passer `python scripts/injection-typographique.py
  <fichier>` qui pose les insecables, les guillemets et les U+2019 -
  c'est la voie des N12 a N15, la plus sure ; (b) script Python avec
  marqueurs ASCII remplaces par chr(8239)/chr(160) et assertion A
  L'EGALITE comptee sur le source - la voie a suivre pour tout fichier que
  injection-typographique.py ne couvre pas (planche.json, plan du
  chantier, prompt de continuite).
  ⚠ injection-typographique.py protege les lignes d'enum du frontmatter
  (secteur, typologie, mission_ft2e) : une apostrophe DROITE tapee dans
  mission_ft2e y RESTE et casse le build - ecrire U+2019 des le script
  (piege N10, « Études d'exécution »). Il NE protege PAS
  secteur_secondaire.
  ⚠ Il ne connait pas toutes les unites : « A » (amperes), « T »,
  « tonnes », « bars », « dBA », « min », « s », « h » et le chiffre
  devant « × » lui echappent (releve en N13, N14 et N15). Verifier au
  grep les unites rares apres passage, et les poser par un second script.
- ⚠ UN HEREDOC BASH PEUT MANGER UN ANTISLASH (N15). Un bloc Python
  contenant une continuation de ligne `\` en fin de ligne, passe par
  `python - <<'PY'`, est arrive AVEC L'ANTISLASH CONSOMME : la chaine
  cherchee ne correspondait plus, et l'assertion echouait sans qu'on voie
  pourquoi. Pour tout script non trivial : outil Write dans le
  SCRATCHPAD, puis execution. C'est aussi la regle qui evite que le hook
  Stop commite des scripts a usage unique.
- Le hook Stop commite et pousse SEUL ce qui traine, et il PEUT
  COMMITTER LE LIVRABLE ENTIER sous l'intitule generique
  « chore(deploy): pousse l'etat de fin de session ». L'historique etant
  pousse sur un depot PARTAGE, il ne se reecrit pas. Pour l'eviter :
  garder les scripts a usage unique DANS LE SCRATCHPAD, hors depot
  (pratique des N13 a N15), COMMITTER TOT des que le build est vert, et
  reserver un second commit a la passe editoriale (⚠ livrables/ porte
  deux fichiers non suivis anterieurs a la N02 - les laisser).
- /references/ est gitignore (motif ancre) - les pieces sources
  n'entrent JAMAIS au depot ; npm run preview ne mesure pas la
  performance ; Chrome refuse les fenetres sous 500 px (sonde iframe).
- La planche n'expose NI le millesime d'ouverture, NI montant, NI tiers
  (MOA, mandataire, architecte, installateur, MARQUES comprises), NI
  donnee nominative ; les designations internes (reperes de zone,
  numeros de tableau, « AGBT », « ZDA01 ») sont admises avec une entree
  a_valider_ft2e et une question E ; tout arbitrage de dessin va dans
  a_valider_ft2e (jamais vide).

DEROULER LE PIPELINE § 2 INTEGRALEMENT : depouillement (pdfinfo /
pdftotext, ou pymupdf via python subprocess avec les noms lus par
os.listdir ; les plans sans couche texte et les marches scannes se
lisent en rendant leurs pages en PNG par pymupdf, zoom 2-3 ; antiword
pour les .doc, xlrd pour les .xls, openpyxl pour les .xlsx,
extract-msg pour les .msg) -> CONTROLE DE LA PAGE DE GARDE DE CHAQUE
PIECE TECHNIQUE -> releve du numero NN-NNN sur piece FT2E ->
references/ref_039/ (3 a 8 pieces) -> croisement commercial
(references/docs_references/ - docx sectoriels ET classeur ODS - +
docs/20-source-plaquette-2024.md + livrables/cv-ft2e/CV-FT2E.zip +
grep de src/content/ pour ce que le site publie deja, LEGENDES ET ALT
DES CLICHES COMPRIS) -> fiche de collecte (A/A+ remplies, B-E en
questions, ligne Secteur citant le classeur, DECISION Q3 motivee en
tete) -> LECTURE DES 38 SOUS-TITRES DE PLANCHE pour verifier qu'aucune
these voisine n'est deja publiee -> fiche src/content/projets/<slug>.md
(SECTEUR RELEVE AU CLASSEUR ; taxonomie ACTUELLE ; lieu avec code postal
entre parentheses ; synthese 480-780 ; >= 5 liens internes ; jamais de
numero d'affaire NI de millesime d'ouverture en prose ; convention
numerale finale - nom du NOMBRE en un seul mot en lettres, nombre
COMPOSE en chiffres, unites et mesures toujours en chiffres, citations
intouchees ; verifier par `python scripts/releve-numeral.py`, dont la
section « Nombres COMPOSES ecrits en lettres » doit rendre 0) ->
PLANCHE complete (extraction avec a_valider_ft2e non vide, apostrophes
courbes des l'ecriture, composition par scripts/planches/<archetype>.py
avec assertion de depassement, rendus par scripts/planches/rendre_png.py
depuis la RACINE, controles a 1152 / carte 274-296 / appui 552 -
REGARDER les quatre PNG -, apostrophes-planches.py en MESURE,
invariant.py, verser.py) ->
qualite (typecheck 0, build vert 62 pages, editorial-reviewer EN
LECTURE SEULE - ses outils d'edition normalisent les insecables,
appliquer ses constats par script -, controle-liens-internes 39/39 a 5,
controle-numeros-affaire 0 fuite, releve-numeral sans ecart nouveau)
-> COMMIT UNIQUE fiche+planche+compositeur (content(references): ajoute
la fiche reelle <nom> et sa planche ; git ls-remote avant, depot
partage) -> push (le push deploie), curl de la fiche AVEC barre oblique
finale + marqueur de build, rendu controle aux trois bandes (sonde
iframe pour les largeurs telephone : references/ref_038/sonde-fiche.mjs,
slug et URL a adapter) ET CONTROLE DE L'INDEXATION SECTORIELLE (point 6,
sonde references/ref_038/sonde-filtres.mjs) -> ligne de suivi au plan ->
PROMPT DE LA SESSION N17 en annexe du plan (script Python ou Write,
jamais un long heredoc) et reproduit integralement dans le message final.
Le prompt N17 REPREND le bloc « REGLE D'INDEXATION SECTORIELLE » tel quel
(repartition remise a jour) ET porte le troisieme dossier de la tranche
2023, choisi parmi les trois restants (21-074 AP Yacht, 20-071 EIFFAGE,
21-029 La Flotte) selon la regle par defaut : les mieux documentes
d'abord, couverture des secteurs, dossiers minces en fin. Il RAPPELLE
aussi l'ecart 49 / 50 signale ci-dessus tant qu'il n'est pas tranche.

Portee de commit : content(references). Un changement de schema Zod
eventuel passe par le sous-agent content-modeller et va dans le MEME
commit que public/admin/config.yml.

Termine par le prompt de lancement de la session N17, en annexe du
plan du chantier et reproduit integralement dans ton message final -
la regle de continuite est dans CLAUDE.md parce qu'elle a ete manquee
deux fois.
```


## Annexe Q — prompt de lancement de la session N17

```
Session N17/27 - FT2E v3 : chantier des 27 nouvelles fiches references.
DIX-SEPTIEME dossier - TROISIEME de la tranche « Finalisees en 2023 ».

Contexte. FT2E v3 est le site institutionnel du bureau d'etudes FT2E
(La Rochelle), Astro 6 statique, deploye en demonstration client sur
https://ft2e-v3.vercel.app (indexation verrouillee - ne pas y toucher).
Le catalogue porte 39 fiches reelles (23 + N01 Portes-en-Re + N02 Fors +
N03 Aurora + N04 Loti + N05 Saint-Sauveur + N06 L'Houmeau + N07 Louise
Magnan + N08 bornes IRVE + N09 comptage Airbus + N10 foyer CDAIR +
N11 parc Undertech + N12 auberge Central Hostel + N13 batiment VoltAero +
N14 extension Fountaine Pajot + N15 Cabanes Urbaines + N16 audit ADEI),
chacune illustree d'une planche de schema de principe (cinq pieces par
dossier). Objectif : 50 fiches. 1 session = 1 dossier, close par le
prompt de la suivante.

LE ZIP DE LA TRANCHE 2023 EST DEJA SUR LE DISQUE :
C:\claude_code_dev_projects\ft2e_new_archives\2023.zip (446 Mo, 670
entrees, racine interne « 2023/ », un repertoire par affaire). Trois
dossiers y restent, tous absents du site (verifie au grep de
src/content/projets/*.md le 2026-09-01) :
-   89 fichiers, 38,9 Mo : « 21-074- Projet AP Yacht - CATANA Group-  Cab SIMONEAU » (classeur I)  <- DOSSIER DU JOUR
-   72 fichiers, 37,7 Mo : « 20-071- Bureaux EIFFAGE St Jean D'Angely - Impact Urbanisme » (classeur T)
-   54 fichiers, 14,2 Mo : « 21-029 - Ecole primaire et maternelle - La Flotte en Re » (classeur M)
IL N'Y A DONC AUCUNE QUESTION A POSER EN OUVERTURE : derouler directement.

⚠ NE JAMAIS conclure « mince » ni « riche » sur le seul compte de fichiers :
quatre dementis en N08-N09 (mince qui etait riche), un dementi INVERSE en
N13 (« 21-095 » annoncait 72 fichiers dont 17 appartenaient a l'affaire
21-093), et trois dossiers integres en N14, N15 et N16. C'est la PAGE DE
GARDE qui dit a quelle affaire une piece appartient, jamais le repertoire
qui la contient. Verifier la page de garde de chaque CCTP, DPGF,
estimation, rapport et plan AVANT d'en tirer la moindre valeur.

⚠ CE QUI RESTE APRES 2023, ET L'ECART 49 / 50 TOUJOURS NON TRANCHE. Le
classeur ODS porte, apres la tranche 2023 : « Finalisees en 2022 » (4 :
19087 Batiment SSLIA I, 20024 INNOVIA-GAELIC I, 20039 Videosurveillance
CH Rochefort M, 22037 Audit chambre des metiers M), « Finalisees en 2020 »
(2 : 19008 Batiment industriel Aeroport LR ELIXIR I, 20058 Diag
legionelles du port de plaisance M) et « Finalisees en 2019 » (1 :
18026 Atelier numerique Fountaine Pajot I). Soit 3 (2023) + 4 + 2 + 1 = 10
dossiers restants pour 39 fiches en ligne : LE CLASSEUR NE MENE QU'A 49,
PAS A 50. La question a ete portee au message final de la N16 mais N'A PAS
ENCORE ETE ARBITREE PAR FT2E : la reposer tant qu'elle reste ouverte -
manque-t-il une affaire au classeur, ou l'objectif de 50 se solde-t-il
a 49 ? Ne pas fabriquer une fiche pour combler l'ecart.
Les ZIP 2019.zip et 2022.zip SONT DEJA SUR LE DISQUE ; celui de la tranche
2020 devra etre demande en ouverture de la session qui closera 2022.

LIRE D'ABORD, dans cet ordre :
1. docs/superpowers/plans/2026-08-27-chantier-27-nouvelles-fiches.md -
   LE PLAN : § 1 (ce qui a change), § 2 (pipeline 12 etapes), § 3
   (reponses consignees Q1/Q2 2024 + complement N02 : le classeur fait
   foi ; Q3 = regle des dossiers minces, defaut reconduit), § Suivi
   (lignes N01 a N16), annexe Q (ce prompt).
2. docs/superpowers/plans/2026-08-07-chantier-references-reelles.md -
   § Contraintes globales + § Protocole de session + § Regle des
   dossiers minces.
3. docs/superpowers/specs/2026-08-12-planches-references-protocole.md -
   revision 5 EN ENTIER.
4. CLAUDE.md, .claude/rules/content-collections.md et french-editorial.md.
Etalons : src/content/projets/creche-oranger-perigny.md (fiche) et, pour
une affaire INDUSTRIELLE, les quatre seules fiches du secteur :
batiment-voltaero-saint-agnant.md, extension-fountaine-pajot-aigrefeuille.md,
ateliers-pilotes-capsulae.md et place-des-chenes-verts-saint-rogatien.md.
Voir aussi src/content/projets/audit-chauffage-sites-adei.md +
public/images/projets/audit-chauffage-sites-adei/ + references/ref_039/
(fiche de collecte N16, avec sa DECISION Q3 en tete - c'est elle qui
documente le piege des HUIT INDICES DE CONTRAT sur une seule affaire).
Les sondes de recette vivent dans references/ref_039/ (sonde-fiche.mjs)
et references/ref_038/ (sonde-filtres.mjs) - URL, slug et secteur a adapter.

REGLE D'INDEXATION SECTORIELLE - etablie le 2026-08-27, A APPLIQUER A
LA REDACTION DE CHAQUE FICHE (etape 6 du pipeline), pas apres coup :
« REFERENCES SITE FT2E.ods » (references/docs_references/, classeur
fourni par FT2E) FAIT FOI pour le classement sectoriel. Concretement,
AVANT d'ecrire le frontmatter :
1. Ouvrir le classeur (python zipfile sur content.xml, ou pandoc) et y
   retrouver l'affaire PAR SON NUMERO (graphie sans tiret : « 21074 »).
2. En relever le domaine (legende : L Logements / T Tertiaire & ERP /
   I Industriel / P Patrimoine / C Coordination SSI /
   M Monotechnique-Audit / E EXE) -> champ `secteur`.
3. Si le classeur porte un domaine DOUBLE (« T § C ») : le premier est
   le `secteur`, le second va au champ `secteur_secondaire` (optionnel
   au schema depuis le 2026-08-27, garde-fou « doit differer ») - la
   fiche parait alors dans les deux filtres et sur les deux pages de
   secteur. Precedents : hotel-yachtman (T § C), maison-pierre-loti-
   rochefort (P § C, N04), foyer-cdair-saint-martin-de-re (T § C, N10),
   auberge-central-hostel-la-rochelle (T § C, N12),
   cabanes-urbaines-la-rochelle (T § C, N15).
   LE DOSSIER DU JOUR EST A DOMAINE SIMPLE : 21074 est « I ».
4. JAMAIS de deduction depuis le dossier, l'usage RT ou le nom de
   l'operation : la N02 penchait « Industriel » pour Fors, le classeur
   dit T - et les 25 fiches ont du etre re-referencees le soir meme
   (7 bascules, commits ce334b2/09270a3). Le classeur peut contredire
   l'intuition (Saint-Rogatien, pole commercial : I ; Fors, pole
   commercial : T ; 23083 « plan de comptage Airbus » : E et non M ;
   23099 « CPAM » : M - IRVE, pas T ; 23036 Fountaine Pajot : I SIMPLE
   alors que le CV annonce « CFO / CFA / SSI » ; 20045 « THE ROOF »,
   salle d'escalade et atelier de luthier : T § C et non I ; 21086
   « Audit chauffage sites ADEI », sept etablissements medico-sociaux :
   M SIMPLE) - il gagne.
5. CONSIGNER la lecture dans la fiche de collecte (ligne « Secteur » :
   citer l'entree du classeur telle quelle) ; si l'affaire est ABSENTE
   du classeur ou son domaine illisible -> question B a FT2E et choix
   provisoire argumente, jamais silencieux.
6. EN RECETTE (etape 10) : verifier sur le deploiement que la fiche
   repond au bon filtre de /references (compteurs de chips) et parait
   sur sa page /secteurs/<slug> - sondes : references/ref_038/
   sonde-filtres.mjs et references/ref_039/sonde-fiche.mjs (URL a adapter).
   ⚠ Une page /secteurs/<slug> n'affiche que les 4 affaires les plus
   recentes du secteur (tri par numero decroissant) ; le filtre de
   /references, lui, montre tout. Une affaire a DOUBLE domaine doit
   etre controlee sur LES DEUX filtres et LES DEUX pages de secteur.
   ⚠ 21-074 est un numero de 2021 et le secteur « Industriel » ne porte
   que 4 fiches, dont deux de 2023 (23036 Fountaine Pajot, 21095
   VoltAero) : verifier si elle entre ou non dans le top 4 de
   /secteurs/industriel-commercial. Le filtre de /references reste la
   mesure qui fait foi.
   Repartition attendue AVANT la N17, mesuree le 2026-09-01 sur le
   deploiement par references/ref_038/sonde-filtres.mjs : L10 T13 I4 P3
   C7 M4 E3 pour 39 fiches, 44 en pondere (Yachtman T+C, Loti P+C, foyer
   CDAIR T+C, Central Hostel T+C et Cabanes Urbaines T+C comptent double).

DOSSIER DU JOUR : « 21-074- Projet AP Yacht - CATANA Group- Cab SIMONEAU »
(89 fichiers, 38,9 Mo, dont 78 PDF), classeur « 21074 · Projet AP Yacht -
CATANA Group · I ». C'est le mieux documente des trois dossiers restants
de la tranche, et il vise le secteur le moins couvert du catalogue
(Industriel, 4 fiches sur 39). Points d'attention connus AVANT ouverture :
(a) TROIS noms figurent au nom de repertoire - « AP Yacht », « CATANA
    Group » et « Cab SIMONEAU ». Il faut etablir lequel est le
    MAITRE D'OUVRAGE, lequel l'ARCHITECTE (« Cab » = cabinet, donc
    vraisemblablement la maitrise d'oeuvre) et lequel l'OPERATION. Le
    piege des trois noms a deja frappe en N13 (« VOLTAREAO ») et en N15
    (« ESCLA'BLOC ») : relever chaque graphie sur la PAGE DE GARDE d'un
    contrat ou d'un marche, JAMAIS sur le nom de repertoire ;
(b) CATANA Group est un constructeur de catamarans cote en bourse,
    implante a Canet-en-Roussillon ET en Charente-Maritime. Verifier ou
    se situe REELLEMENT l'ouvrage : le champ `lieu` exige un code postal
    a cinq chiffres entre parentheses, et `commune()` echoue bruyamment
    sans lui ;
(c) « AP » pourrait designer une phase d'AVANT-PROJET plutot qu'un nom
    d'ouvrage. Ne rien en conclure avant lecture des pieces ;
(d) une affaire industrielle de chantier naval peut porter des donnees
    de PROCESS (postes de stratification, extraction de styrene,
    compresseurs) : ce sont des donnees d'exploitation du client, que la
    regle dure 3 exclut du DESSIN mais pas necessairement du recit -
    arbitrer et consigner ;
(e) ⚠ une note ou un rapport peut ne pas boucler. La N16 en a releve
    CINQ dans un seul dossier (economie annoncee a deux valeurs
    differentes, temps de retour permutes entre detail et synthese,
    consommation de l'etat existant recopiee dans quatre fiches de
    preconisation, deux bilans de consommation qui ne se ferment pas).
    Verifier que les sous-totaux somment AVANT de composer quoi que ce
    soit de proportionnel.
Aucun numero 21-074 n'est publie (verifie au grep de
src/content/projets/*.md le 2026-09-01).
ATTENTION DISQUE (~5 Go libres) : supprimer d'abord le repertoire extrait
de la session precedente -
C:\claude_code_dev_projects\ft2e_new_archives\2023 (le REPERTOIRE, pas le
ZIP ; il contient 2023/21-086 - Audit chauffage sites ADEI) - par python
shutil.rmtree (le rm -rf est REFUSE par les permissions).
Puis extraire LE SEUL dossier du jour PAR PYTHON ZIPFILE (members filtres
sur « 21-074 » via zipfile.namelist() - les noms portent des accents en
mojibake, ne JAMAIS taper un chemin). Le ZIP est la source, il ne se
supprime pas.
⚠ L'extraction a recree la racine interne en N10, N15 et N16
(ft2e_new_archives\2023\2023\<dossier>) mais PAS en N11-N14 : ne jamais
presumer la profondeur, descendre par os.listdir.
Dossier de travail a creer : references/ref_040/
Slug cible : a etablir au depouillement (kebab-case sans accents,
verifier qu'il n'ecrase rien).

CE QUE LES N01-N16 ONT ETABLI (verifiable au depot) :
- ⚠ UN INDICE DE CONTRAT N'EST PAS UNE AFFAIRE - confirme deux fois
  (N15 : 20-045 / 20 045 A / 20-045-CSSI ; N16 : 21 086 A a H, HUIT
  contrats pour SEPT sites et une seule affaire). Le depart se fait sur
  les pieces de PRODUCTION : les cinq rapports de la N16 portaient tous
  « Affaire N ° 21-086 » sans indice, et le classeur ne connaissait
  qu'une entree. Ne jamais decouper une affaire sur ses contrats.
- ⚠ LE MAITRE D'OUVRAGE N'EST PAS TOUJOURS L'OCCUPANT (N16) : les huit
  contrats etaient signes par une SCI « pour le compte de » l'association
  gestionnaire, et trois des cinq rapports nommaient l'association en
  page de garde. Renseigner `moa` sur le SIGNATAIRE, ecrire la
  divergence en question B, et nommer l'occupant au titre et au recit.
- ⚠ UNE THESE PEUT ETRE DEJA PUBLIEE - decouverte de la N14, et elle se
  verifie AVANT de composer. AVANT d'arreter une these, lire les
  `sous_titre` et `archetype_motif` des 39 planches
  (PYTHONIOENCODING=utf-8 python -c "..." sur public/images/projets/*/
  planche.json) : deux fiches voisines qui demontrent la meme chose sont
  une redite, que le protocole interdit explicitement. La N16 a verifie
  que son mecanisme (une contrainte d'aval qui interdit un choix d'amont)
  se distinguait bien du mecanisme `commande` du siege RESE (« ce qui
  DECLENCHE un debit d'air »), et l'a ECRIT dans `archetype_motif`.
- ⚠ UN DOSSIER D'ARCHIVES PEUT CONTENIR LES PIECES D'UNE AUTRE AFFAIRE
  (N13). Lire la PAGE DE GARDE (« N° affaire : ... », « Affaire n° : ... »)
  de CHAQUE piece technique avant d'en tirer une valeur. Les N14, N15 et
  N16 ont rejoue ce controle et trouve des dossiers integres : le
  controle se fait, son resultat n'est pas acquis d'avance.
  Corollaire : une affaire peut n'avoir AUCUNE piece technique FT2E au
  dossier. La fiche reste publiable si trois familles de sources la
  soutiennent - programme du maitre d'ouvrage, comptes rendus de
  chantier, CV de l'equipe -, a condition que chacune soit NOMMEE en
  collecte et qu'aucune valeur de dimensionnement ne soit inventee.
- LES CV DE L'EQUIPE SONT UNE SOURCE FT2E (livrables/cv-ft2e/CV-FT2E.zip,
  edition aout 2026, six CV en .docx lisibles par zipfile+regex sur
  word/document.xml). La N13 y a trouve le perimetre reel de la mission ;
  la N14 la mention SSI qui a ouvert une question B ; la N15 la
  reconciliation d'un conflit de millesime. Les interroger
  systematiquement au croisement commercial (etape 4), avec les docx
  sectoriels, le classeur et docs/20-source-plaquette-2024.md. ⚠ Il
  n'existe AUCUN docx sectoriel « industriel » : sur une affaire du
  secteur I, l'absence des onze docx ne dit RIEN contre elle - le
  chercher plutot dans les CV et la plaquette.
- annee_livraison se pose sur le classeur ; quand pieces et classeur se
  contredisent, le classeur est suivi ET la contradiction est ecrite en
  B1, jamais tranchee en silence (N16 : classeur « Finalisees en 2023 »,
  dernier rapport du 17/05/2023, mais un contrat d'AMO du 20/02/2024 et
  des pieces de subvention de 2024 - le classeur a ete suivi et l'ecart
  ecrit). Le PV de reception manque presque toujours - mais il se cherche
  a SIX endroits : un CR d'OPC portant « RECEPTION DES TRAVAUX » en tete
  (N11) ; un CR annoncant la reception a une date precise avec le
  planning des semaines suivantes (N12) ; le BILAN DE FACTURATION, les
  honoraires d'AOR ne se facturant qu'une fois la mission finie (N12) ;
  le DERNIER CR DE CHANTIER, dont l'en-tete remplace « PROCHAINE
  REUNION » par « RECEPTION le JJ/MM/AAAA » (N13) ; LE CALENDRIER EN TETE
  DE CHAQUE CR D'OPC (N14) ; et L'EN-TETE DES DERNIERS CR, qui porte
  « Reception du chantier : JJ/MM/AA » plusieurs semaines a l'avance
  (N15). ⚠ L'indice des honoraires d'AOR NE JOUE PAS quand le BET ne
  porte pas l'AOR a la repartition (cas N14). ⚠ Sur une mission d'ETUDE
  SANS TRAVAUX (N16), il n'y a pas de reception du tout : la date qui
  fait foi est celle du DERNIER RAPPORT REMIS.
- Le numero FT2E se releve sur page de garde CCTP (« Affaire n° : ... »),
  cartouche de plan (« Reference Affaire : ... »), etude thermique (pied
  de chaque page), contrats et propositions FT2E, EN PIED DE CHAQUE PAGE
  d'une note methodologique (N15), et - N16 - EN TETE DE CHAQUE PAGE d'un
  rapport d'audit (« Affaire N ° 21-086 »).
  ⚠ EN DERNIER RECOURS SEULEMENT, quand aucune piece FT2E n'existe au
  dossier (N13), il se releve sur le CLASSEUR + le nom du repertoire
  d'archives, et cela DOIT faire l'objet d'une question B.
- Les numeros des MANDATAIRES et donneurs d'ordres pietinent les
  pieces : declaration de travaux « DT 2022090895299S16 » et references
  constructeur « NUG31440 » (N15) ; ASP « 2301 », bon de commande EQUANS
  « 0023284014 » (N14) ; SD Architectes « 21.17 », marche public
  « 20210000200 », dossier RESE « TRX021847 » (N13) ; SEMDAS « 2507 »,
  ARCHITEM « 1821 » (N10) ; Equans « 22984760 » (N09) ; CPAM
  « PA 2024 - MO01 » (N08). ⚠ Attention aussi aux DESIGNATIONS DE
  BATIMENT qui ressemblent a des numeros (« 5-8 » chez Fountaine Pajot).
- ⚠ UN CCTP PEUT SE CONTREDIRE EN INTERNE (N11), ET UN RAPPORT AUSSI
  (N16 : les emetteurs des bureaux d'un ESAT y sont donnes une fois comme
  plancher chauffant et une fois comme aerothermes). Retenir le
  paragraphe QUI DENOMBRE ou QUI RELEVE, l'ecrire dans a_valider_ft2e,
  en faire une question B - et ne PAS publier de compte que la piece ne
  soutient pas (la N16 a remplace « deux des quatre preconisations » par
  la seule preconisation dont le libelle etablissait le fait).
- ⚠ RECOMPTER LIGNE A LIGNE CE QU'ON ANNONCE (N15). Tout effectif porte a
  une fiche ou a une planche se recompte sur la piece, jamais sur son
  souvenir. La N16 a recompte ses dix surfaces pour publier 9 131 m².
- ⚠ UNE NOTE DE CALCUL PEUT NE PAS BOUCLER (N14, cinq fois en N16). Ne
  JAMAIS composer un schema proportionnel (sankey, jauge, largeurs) sur
  des valeurs qui ne se ferment pas. La N16 a EXCLU les temps de retour
  et les gains energetiques de sa planche pour cette raison, et l'a ecrit
  au bloc `exclusions_appliquees`.
- NOMMER LE CLIENT FINAL : un nom deja publie par FT2E (plaquette,
  corpus secteurs, docx sectoriels, classeur, CV) se reprend, avec E1
  (N09 Airbus, N10 CDAIR, N11 Undertech, N12 Central Hostel, N13
  VoltAero, N14 Fountaine Pajot, N15 Cabanes Urbaines, N16 ADEI - trouve
  dans QUATRE docx sectoriels sous la graphie « ADEI 17 », pour deux
  AUTRES affaires que celle de la fiche) ; un nom couvert par une clause
  de confidentialite reste hors slug et hors titre (N08 CPAM).
  ⚠ **Chercher aussi dans le CORPUS SECTEURS** : la N15 a decouvert
  qu'une PHOTOGRAPHIE de son affaire etait deja publiee sur
  /secteurs/coordination-ssi - le grep de src/content/ doit couvrir les
  legendes et les alt des cliches, pas seulement la prose. Aucun nom de
  tiers ne monte jamais sur la planche - seul le nom d'OUVRAGE peut
  porter celui de l'occupant, et la N16 a prefere s'en passer entierement
  (titre court « Sept sites medico-sociaux »).
- ⚠ UNE GRAPHIE PEUT ETRE FAUSSE PARTOUT SAUF DANS LES CV (N13), ET LES
  PIECES D'UNE MEME AFFAIRE PEUVENT SE CONTREDIRE ENTRE ELLES (N15 :
  ESCAL'BLOC / ESCLA'BLOC / ESCALBLOC dans trois pieces FT2E ; N16 : le
  code postal d'une meme adresse ecrit « 17440 » sur les contrats et
  « 17 443 » sur trois pages de garde). Relever la graphie sur la page de
  garde d'un contrat ou d'un marche, retenir la majoritaire, ecrire la
  divergence en question B - et VERIFIER TOUJOURS si l'acteur est deja
  nomme dans src/content/projets/*.md avant d'ecrire `architecte` ou
  `moa`.
- ⚠ UN SITE PUBLIE PEUT PORTER UNE DATE FAUSSE (N15). Corriger une page
  publiee est legitime quand une piece FT2E tranche, MAIS cela s'ecrit en
  question B et se signale au message final - jamais en silence.
- ⚠ L'AGENT DE RELECTURE TROUVE DES ERREURS DE FAIT SANS AVOIR LES PIECES
  (N15). Traiter chaque question de compte comme une piste a verifier SUR
  LA PIECE, jamais comme une remarque de style ; et se relire soi-meme
  sur le critere « les items enumeres correspondent-ils au nombre
  annonce ? ». ⚠ Corollaire : lui donner en contexte les faits etablis
  sur piece (c'est ce qui lui permet de croiser), et lui demander
  EXPLICITEMENT les chaines exactes avant/apres - il travaille EN LECTURE
  SEULE, ses outils d'edition normalisent les insecables du depot.
- Archetypes apres N16 : boucle-fluide 11 - coupe-traversee 7 -
  tableau-electrique 7 - sankey-energie 6 - zonage-ssi 6 -
  chronologie-affaire 2 - planche-chiffree 0 SANS module. L'archetype se
  choisit sur la THESE, jamais sur le secteur ni sur le quota, mais a
  these egale preferer ce qui n'a pas servi depuis longtemps ; la dette
  de variete porte toujours sur boucle-fluide (11/39), et
  chronologie-affaire n'a pas servi depuis le corpus fondateur
  (admissible seulement si sa these est d'INGENIERIE, jamais le
  calendrier d'une operation). ⚠ `planche-chiffree` n'a toujours pas de
  module : si un dossier l'exige, la decision est de L'ECRIRE ou de
  retirer l'archetype de la liste fermee (§ 1 du plan), jamais de
  bricoler.
- Un mecanisme nouveau s'ecrit DANS le compositeur d'archetype
  (constantes prefixees par le mecanisme ; garde-fou de greffe sur le
  NOM DE LA FONCTION ET sur les prefixes de constantes - automatise
  depuis la N13 : en N16, 4 fonctions, 17 constantes RG_ et 12 helpers
  reutilises verifies), et l'invariant octet se rejoue AVANT la greffe,
  APRES la greffe et APRES la derniere retouche.
  ⚠ L'INSTRUMENT EXISTE AU DEPOT ET SE REJOUE SEUL, NE PAS LE REECRIRE :
  `python scripts/planches/invariant.py` couvre les 6 compositeurs et les
  39 dossiers (156/156 pieces au 2026-09-01),
  `python scripts/planches/invariant.py <archetype>` un seul.
  ⚠ Un dossier neuf dont la planche n'est pas encore composee fait
  chuter le compte de l'invariant : ce n'est pas une rupture, ce sont
  les pieces qui n'existent pas encore.
- ⚠ METTRE UNE ASSERTION DE DEPASSEMENT DANS LE COMPOSITEUR (N14, rejouee
  en N15 et N16, payante des le premier jet a chaque fois) : chaque
  chaine dessinee est mesuree par `mesurer()` contre la largeur
  interieure de son contenant, versee dans une liste, et un
  `assert not trop` rompt la composition avant tout rendu. En N16 elle a
  arrete trois debordements au premier jet, et son resultat est publie au
  bloc `controles` (« 29 chaines mesurees, 0 depassement, marge la plus
  faible 11,2 px »).
  ⚠ **ET IL FAUT LA METTRE AUSSI DANS L'APPUI ET LA VIGNETTE** - lecon
  NEUVE de la N16, apprise a ses depens : l'assertion ne couvrait que la
  planche, et « Pompe a chaleur » a mordu sur le bord de son bloc dans
  l'appui. Le defaut a passe le build, le bloc `controles`, l'invariant
  ET le PNG de controle a 552 px : il ne s'est vu qu'a la capture du
  DEPLOIEMENT a 768 px. L'appui et la vignette composent leurs propres
  colonnes ; ce qui n'est pas mesure n'est pas garanti.
- ⚠ NE PAS REECRIRE rendre_png.py : il est au depot depuis la N12, avec
  les deux pieges encodes (retrait de l'attribut style de racine par
  REGEX - sans quoi la vignette rend BLANCHE sans erreur - et fusion des
  filets a 8 chiffres). Usage :
  `python scripts/planches/rendre_png.py public/images/projets/<slug>
  <scratchpad>` ecrit planche.png 2400x1600 dans le dossier et, dans le
  scratchpad, les quatre controles (1152, vignette 274 et 296, appui
  552). REGARDER LES QUATRE. ⚠ Il s'appelle depuis la RACINE du depot.
- ⚠ LE RENDU CAIROSVG N'A PAS LES POLICES DU SITE (N13, reconfirme en
  N14 et N16) : il retombe sur une police de substitution dont la chasse
  mono est ~7 a 8 % plus large que celle d'IBM Plex Mono. Consequence :
  le dernier caractere du cartouche de legende parait COUPE sur le PNG de
  controle - la N16 l'a vu sur « 2023 » et ne l'a PAS corrige, et le
  rendu du deploiement a 390 px a confirme que le cartouche est entier.
  NE PAS « corriger » la largeur du cartouche : la formule
  `mesurer(...) + 40` est commune aux 39 planches. ⚠ La MEME sous-mesure
  vaut pour tout fond papier pose derriere un mono, et pour toute marge
  serree : prendre 8 % de large.
- ECRIRE LES CHAINES COURBES DES L'ECRITURE - extraction planche.json
  COMPRISE. La recette, tenue en N11 a N16 : dans le script d'extraction
  lui-meme, avant ecriture, une assertion `"'" not in sortie`, une
  assertion `M not in sortie` sur chaque marqueur, et une assertion A
  L'EGALITE sur le COMPTE d'insecables - ce compte se LIT sur le source
  du script (nombre de marqueurs dans le litteral), jamais ecrit a la
  main. ⚠ Employer DEUX marqueurs distincts, « @ » pour la fine U+202F et
  « ^ » pour l'insecable U+00A0, avec deux assertions comptees
  separement. Ne PAS prendre « # » (collision avec les titres Markdown).
  ⚠ En N16 l'assertion sur l'apostrophe droite a ATTRAPE quatre champs
  `objet` d'`a_valider_ft2e` oublies : elle sert, ne pas la retirer.
  ⚠ ET ECRIRE LES ACCENTS DIRECTEMENT : la normalisation de Write porte
  sur les INSECABLES, pas sur les accents. Un `a_valider_ft2e` sans
  accents est illisible pour FT2E, qui est le seul lecteur de cette piece.
  La passe `python scripts/apostrophes-planches.py` (sans argument, en
  MESURE) n'a alors rien a courber - 0 sur 0 en N14, N15 et N16. Les
  apostrophes qu'elle REFUSE sont de la syntaxe de f-string : c'est le
  comportement voulu.
- Les avances calibrees de _tronc.mesurer sous-mesurent Archivo 600 au
  rendu d'environ 20 % (N08-N09) - prendre la marge DANS LE CODE
  (`mesurer(...) * 1.2`), pas a l'oeil.
- REGARDER LES PNG, ET CORRIGER CE QU'ON Y VOIT. La N16 a fait CINQ
  retouches que ni le build ni le bloc `controles` n'auraient signalees :
  une legende qui chevauchait l'issue d'un emetteur ; un trait montant de
  12 px dont la barre se confondait avec une etiquette voisine ; une
  barre d'arret si proche de sa cible qu'on la lisait comme l'atteignant ;
  une legende TRAVERSEE par le trait vertical, replacee en zone franche
  au pied du dessin ; et le libelle de l'appui qui mordait son bloc.
  ⚠ Piege generique confirme en N13, N14, N15 et N16 : deux traits qui se
  croisent, ou un trait et un texte, doivent differer par autre chose que
  leur position - epaisseur, continuite, etiquette a fond papier
  (`_etiquette`), ou deplacement en zone franche.
  ⚠ NOUVEAU en N16 : **un trait qui s'arrete ne dit quelque chose que
  s'il allait quelque part.** La premiere version montait de la ligne et
  s'interrompait dans le vide a 250 px de sa cible ; sur la planche la
  legende rattrapait le sens, mais sur la VIGNETTE, qui n'a pas de
  legende, la boite cible flottait sans relation. Le trait doit courir
  VERS sa cible et s'arreter juste avant elle.
- Quand aucune surface n'existe au dossier, la chercher dans les DOCX
  COMMERCIAUX (N12) ; si elle n'y est pas non plus (N13), laisser
  `surface_m2` VIDE et porter au cartouche la grandeur qui compte
  l'ouvrage, avec question B. ⚠ Quand PLUSIEURS surfaces existent et
  divergent (N14), retenir celle qui designe EXPLICITEMENT l'objet de la
  fiche, ecrire les autres en a_valider_ft2e, et n'en publier qu'une seule
  en prose. ⚠ Quand la seule surface au dossier ne couvre qu'une PARTIE de
  l'ouvrage (N15), ou n'en couvre qu'une partie des sites (N16 : 9 131 m²
  pour cinq sites documentes sur sept sous contrat), la publier en le
  disant explicitement dans le recit, et poser la question B.
- Les insecables des heredocs bash sont normalisees DE FACON NON
  DETERMINISTE sur cette machine. DEUX VOIES, toutes deux eprouvees :
  (a) ecrire le .md en ESPACES ORDINAIRES et apostrophes droites par
  l'outil Write, puis passer `python scripts/injection-typographique.py
  <fichier>` qui pose les insecables, les guillemets et les U+2019 -
  c'est la voie des N12 a N16, la plus sure ; (b) script Python avec
  marqueurs ASCII remplaces par chr(8239)/chr(160) et assertion A
  L'EGALITE comptee sur le source - la voie a suivre pour tout fichier que
  injection-typographique.py ne couvre pas (planche.json, plan du
  chantier, prompt de continuite).
  ⚠ injection-typographique.py protege les lignes d'enum du frontmatter
  (secteur, typologie, mission_ft2e) : une apostrophe DROITE tapee dans
  mission_ft2e y RESTE et casse le build - ecrire U+2019 des le script
  (piege N10, « Études d'exécution »). Il NE protege PAS
  secteur_secondaire.
  ⚠ Il ne connait pas toutes les unites : « A » (amperes), « T »,
  « tonnes », « bars », « dBA », « min », « s », « h » et le chiffre
  devant « × » lui echappent (releve en N13, N14 et N15). Verifier au
  grep les unites rares apres passage. En N16, °C, m², €, kWh et kWhep
  ont tous ete correctement traites - controle par regex sur
  « chiffre + espace ordinaire + unite », a rejouer.
- ⚠ UN HEREDOC BASH PEUT MANGER UN ANTISLASH (N15, RECONFIRME EN N16 des
  le premier script de la session). Un bloc Python contenant `\` dans un
  litteral, passe par `python - <<'PY'`, arrive AVEC L'ANTISLASH
  CONSOMME. Pour tout script non trivial : outil Write dans le
  SCRATCHPAD, puis execution. C'est aussi la regle qui evite que le hook
  Stop commite des scripts a usage unique.
  ⚠ ET NE JAMAIS TAPER UN CHEMIN D'ARCHIVES : les noms portent des
  accents et des apostrophes typographiques. La N16 a perdu deux
  tentatives de copie avant de retrouver ses pieces par `os.walk` +
  fragments de nom, ce qui est la seule methode fiable.
- Le hook Stop commite et pousse SEUL ce qui traine, et il PEUT
  COMMITTER LE LIVRABLE ENTIER sous l'intitule generique
  « chore(deploy): pousse l'etat de fin de session ». L'historique etant
  pousse sur un depot PARTAGE, il ne se reecrit pas. Pour l'eviter :
  garder les scripts a usage unique DANS LE SCRATCHPAD, hors depot
  (pratique des N13 a N16), COMMITTER TOT des que le build est vert, et
  reserver un second commit a la passe editoriale (⚠ livrables/ porte
  deux fichiers non suivis anterieurs a la N02 - les laisser).
- /references/ est gitignore (motif ancre) - les pieces sources
  n'entrent JAMAIS au depot ; npm run preview ne mesure pas la
  performance ; Chrome refuse les fenetres sous 500 px (sonde iframe).
- La planche n'expose NI le millesime d'ouverture, NI montant, NI tiers
  (MOA, mandataire, architecte, installateur, MARQUES comprises), NI
  donnee nominative ; les designations internes (reperes de zone,
  numeros de tableau, « AGBT », « ZDA01 ») sont admises avec une entree
  a_valider_ft2e et une question E ; tout arbitrage de dessin va dans
  a_valider_ft2e (jamais vide).

DEROULER LE PIPELINE § 2 INTEGRALEMENT : depouillement (pdfinfo /
pdftotext, ou pymupdf via python subprocess avec les noms lus par
os.listdir ; les plans sans couche texte et les marches scannes se
lisent en rendant leurs pages en PNG par pymupdf, zoom 2-3 ; antiword
pour les .doc, xlrd pour les .xls, openpyxl pour les .xlsx,
extract-msg pour les .msg) -> CONTROLE DE LA PAGE DE GARDE DE CHAQUE
PIECE TECHNIQUE -> releve du numero NN-NNN sur piece FT2E ->
references/ref_040/ (3 a 8 pieces) -> croisement commercial
(references/docs_references/ - docx sectoriels ET classeur ODS - +
docs/20-source-plaquette-2024.md + livrables/cv-ft2e/CV-FT2E.zip +
grep de src/content/ pour ce que le site publie deja, LEGENDES ET ALT
DES CLICHES COMPRIS) -> fiche de collecte (A/A+ remplies, B-E en
questions, ligne Secteur citant le classeur, DECISION Q3 motivee en
tete) -> LECTURE DES 39 SOUS-TITRES DE PLANCHE pour verifier qu'aucune
these voisine n'est deja publiee -> fiche src/content/projets/<slug>.md
(SECTEUR RELEVE AU CLASSEUR ; taxonomie ACTUELLE ; lieu avec code postal
entre parentheses ; synthese 480-780 ; >= 5 liens internes ; jamais de
numero d'affaire NI de millesime d'ouverture en prose ; convention
numerale finale - nom du NOMBRE en un seul mot en lettres, nombre
COMPOSE en chiffres, unites et mesures toujours en chiffres, citations
intouchees ; verifier par `python scripts/releve-numeral.py`, dont la
section « Nombres COMPOSES ecrits en lettres » doit rendre 0) ->
PLANCHE complete (extraction avec a_valider_ft2e non vide, apostrophes
courbes ET ACCENTS des l'ecriture, composition par
scripts/planches/<archetype>.py avec assertion de depassement SUR LES
TROIS FORMATS, rendus par scripts/planches/rendre_png.py depuis la
RACINE, controles a 1152 / carte 274-296 / appui 552 - REGARDER les
quatre PNG -, apostrophes-planches.py en MESURE, invariant.py,
verser.py) -> qualite (typecheck 0, build vert 63 pages,
editorial-reviewer EN LECTURE SEULE - ses outils d'edition normalisent
les insecables, appliquer ses constats par script -,
controle-liens-internes 40/40 a 5, controle-numeros-affaire 0 fuite,
releve-numeral sans ecart nouveau) -> COMMIT UNIQUE fiche+planche+
compositeur (content(references): ajoute la fiche reelle <nom> et sa
planche ; git ls-remote avant, depot partage) -> push (le push deploie),
curl de la fiche AVEC barre oblique finale + marqueur de build, rendu
controle aux trois bandes (sonde iframe pour les largeurs telephone :
references/ref_039/sonde-fiche.mjs, slug et URL a adapter) ET CONTROLE
DE L'INDEXATION SECTORIELLE (point 6, sonde
references/ref_038/sonde-filtres.mjs) -> ligne de suivi au plan ->
PROMPT DE LA SESSION N18 en annexe du plan (script Python ou Write,
jamais un long heredoc) et reproduit integralement dans le message final.
Le prompt N18 REPREND le bloc « REGLE D'INDEXATION SECTORIELLE » tel quel
(repartition remise a jour) ET porte le quatrieme dossier de la tranche
2023, choisi parmi les deux restants (20-071 EIFFAGE, 21-029 La Flotte)
selon la regle par defaut : les mieux documentes d'abord, couverture des
secteurs, dossiers minces en fin. Il RAPPELLE aussi l'ecart 49 / 50 tant
qu'il n'est pas tranche.

Portee de commit : content(references). Un changement de schema Zod
eventuel passe par le sous-agent content-modeller et va dans le MEME
commit que public/admin/config.yml.

Termine par le prompt de lancement de la session N18, en annexe du
plan du chantier et reproduit integralement dans ton message final -
la regle de continuite est dans CLAUDE.md parce qu'elle a ete manquee
deux fois.
```

## Annexe R — prompt de lancement de la session N18

```
Session N18/27 - FT2E v3 : chantier des 27 nouvelles fiches references.
DIX-HUITIEME dossier - QUATRIEME et avant-dernier de la tranche
« Finalisees en 2023 ».

Contexte. FT2E v3 est le site institutionnel du bureau d'etudes FT2E
(La Rochelle), Astro 6 statique, deploye en demonstration client sur
https://ft2e-v3.vercel.app (indexation verrouillee - ne pas y toucher).
Le catalogue porte 40 fiches reelles (23 + N01 Portes-en-Re + N02 Fors +
N03 Aurora + N04 Loti + N05 Saint-Sauveur + N06 L'Houmeau + N07 Louise
Magnan + N08 bornes IRVE + N09 comptage Airbus + N10 foyer CDAIR +
N11 parc Undertech + N12 auberge Central Hostel + N13 batiment VoltAero +
N14 extension Fountaine Pajot + N15 Cabanes Urbaines + N16 audit ADEI +
N17 atelier AP Yacht), chacune illustree d'une planche de schema de
principe (cinq pieces par dossier). Objectif : 50 fiches. 1 session =
1 dossier, close par le prompt de la suivante.

LE ZIP DE LA TRANCHE 2023 EST DEJA SUR LE DISQUE :
C:\claude_code_dev_projects\ft2e_new_archives\2023.zip (446 Mo, 670
entrees, racine interne « 2023/ », un repertoire par affaire). DEUX
dossiers y restent, tous deux absents du site (verifie au grep de
src/content/projets/*.md le 2026-09-01) :
-   72 fichiers, 37,7 Mo : « 20-071- Bureaux EIFFAGE St Jean D'Angely -
    Impact Urbanisme » (classeur T)  <- DOSSIER DU JOUR
-   54 fichiers, 14,2 Mo : « 21-029 - Ecole primaire et maternelle -
    La Flotte en Re » (classeur M)
IL N'Y A DONC AUCUNE QUESTION A POSER EN OUVERTURE : derouler directement.

⚠ NE JAMAIS conclure « mince » ni « riche » sur le seul compte de fichiers :
quatre dementis en N08-N09 (mince qui etait riche), un dementi INVERSE en
N13 (« 21-095 » annoncait 72 fichiers dont 17 appartenaient a l'affaire
21-093), et quatre dossiers integres en N14, N15, N16 et N17. C'est la PAGE
DE GARDE qui dit a quelle affaire une piece appartient, jamais le repertoire
qui la contient. Verifier la page de garde de chaque CCTP, DPGF, estimation,
rapport et plan AVANT d'en tirer la moindre valeur.

⚠ CE QUI RESTE APRES 2023, ET L'ECART 49 / 50 TOUJOURS NON TRANCHE. Le
classeur ODS porte, apres la tranche 2023 : « Finalisees en 2022 » (4 :
19087 Batiment SSLIA I, 20024 INNOVIA-GAELIC I, 20039 Videosurveillance
CH Rochefort M, 22037 Audit chambre des metiers M), « Finalisees en 2020 »
(2 : 19008 Batiment industriel Aeroport LR ELIXIR I, 20058 Diag
legionelles du port de plaisance M) et « Finalisees en 2019 » (1 :
18026 Atelier numerique Fountaine Pajot I). Soit 2 (2023) + 4 + 2 + 1 = 9
dossiers restants pour 40 fiches en ligne : LE CLASSEUR NE MENE QU'A 49,
PAS A 50. La question a ete portee aux messages finaux des N16 et N17 et
N'A TOUJOURS PAS ETE ARBITREE PAR FT2E : la reposer tant qu'elle reste
ouverte. Ne pas fabriquer une fiche pour combler l'ecart.
⚠ PISTE NOUVELLE, relevee en N17 : le classeur porte une section
« Finalisees en 2021 » qui est VIDE. C'est le seul millesime sans aucune
entree, entre 2020 (2 entrees) et 2022 (4 entrees). L'hypothese a soumettre
a FT2E est qu'une affaire manque a cette section - ce qui expliquerait
l'ecart exactement. A verifier avec eux, pas a supposer.
Les ZIP 2019.zip et 2022.zip SONT DEJA SUR LE DISQUE ; celui de la tranche
2020 devra etre demande en ouverture de la session qui closera 2022.

LIRE D'ABORD, dans cet ordre :
1. docs/superpowers/plans/2026-08-27-chantier-27-nouvelles-fiches.md -
   LE PLAN : § 1 (ce qui a change), § 2 (pipeline 12 etapes), § 3
   (reponses consignees Q1/Q2 2024 + complement N02 : le classeur fait
   foi ; Q3 = regle des dossiers minces, defaut reconduit), § Suivi
   (lignes N01 a N17), annexe R (ce prompt).
2. docs/superpowers/plans/2026-08-07-chantier-references-reelles.md -
   § Contraintes globales + § Protocole de session + § Regle des
   dossiers minces.
3. docs/superpowers/specs/2026-08-12-planches-references-protocole.md -
   revision 5 EN ENTIER.
4. CLAUDE.md, .claude/rules/content-collections.md et french-editorial.md.
Etalons : src/content/projets/creche-oranger-perigny.md (fiche) et, pour
une affaire TERTIAIRE, les fiches du secteur T - dont
undertech-la-pallice-la-rochelle.md (parc de bureaux, le plus proche du
dossier du jour), siege-rese-aigrefeuille.md, hotel-yachtman-quai-valin-
la-rochelle.md et auberge-central-hostel-la-rochelle.md.
Voir aussi src/content/projets/ap-yacht-marans.md +
public/images/projets/ap-yacht-marans/ + references/ref_040/ (fiche de
collecte N17, avec sa DECISION Q3 en tete - c'est elle qui documente le
piege des TROIS FAUX NUMEROS D'AFFAIRE et la distinction entre un compte
de FICHIERS et un compte de REUNIONS).
Les sondes de recette vivent dans references/ref_040/ (sonde-fiche.mjs ET
sonde-filtres.mjs, toutes deux adaptees en N17) - URL, slug et secteur a
adapter. La sonde de filtres s'appelle DEPUIS LA RACINE du depot.

REGLE D'INDEXATION SECTORIELLE - etablie le 2026-08-27, A APPLIQUER A
LA REDACTION DE CHAQUE FICHE (etape 6 du pipeline), pas apres coup :
« REFERENCES SITE FT2E.ods » (references/docs_references/, classeur
fourni par FT2E) FAIT FOI pour le classement sectoriel. Concretement,
AVANT d'ecrire le frontmatter :
1. Ouvrir le classeur (python zipfile sur content.xml, ou pandoc) et y
   retrouver l'affaire PAR SON NUMERO (graphie sans tiret : « 20071 »).
2. En relever le domaine (legende : L Logements / T Tertiaire & ERP /
   I Industriel / P Patrimoine / C Coordination SSI /
   M Monotechnique-Audit / E EXE) -> champ `secteur`.
3. Si le classeur porte un domaine DOUBLE (« T § C ») : le premier est
   le `secteur`, le second va au champ `secteur_secondaire` (optionnel
   au schema depuis le 2026-08-27, garde-fou « doit differer ») - la
   fiche parait alors dans les deux filtres et sur les deux pages de
   secteur. Precedents : hotel-yachtman (T § C), maison-pierre-loti-
   rochefort (P § C, N04), foyer-cdair-saint-martin-de-re (T § C, N10),
   auberge-central-hostel-la-rochelle (T § C, N12),
   cabanes-urbaines-la-rochelle (T § C, N15).
   LE DOSSIER DU JOUR EST A DOMAINE SIMPLE : 20071 est « T ».
4. JAMAIS de deduction depuis le dossier, l'usage RT ou le nom de
   l'operation : la N02 penchait « Industriel » pour Fors, le classeur
   dit T - et les 25 fiches ont du etre re-referencees le soir meme
   (7 bascules, commits ce334b2/09270a3). Le classeur peut contredire
   l'intuition (Saint-Rogatien, pole commercial : I ; Fors, pole
   commercial : T ; 23083 « plan de comptage Airbus » : E et non M ;
   23099 « CPAM » : M - IRVE, pas T ; 23036 Fountaine Pajot : I SIMPLE
   alors que le CV annonce « CFO / CFA / SSI » ; 20045 « THE ROOF »,
   salle d'escalade et atelier de luthier : T § C et non I ; 21086
   « Audit chauffage sites ADEI », sept etablissements medico-sociaux :
   M SIMPLE ; 21074 « AP Yacht - CATANA Group », chantier naval : I
   SIMPLE alors que le CV de Vincent Jaoul annonce « CFO / CFA / SSI » -
   le CCTP lot 10 le tranche, la detection incendie etait a la charge du
   maitre d'ouvrage sur un SSI existant) - il gagne.
5. CONSIGNER la lecture dans la fiche de collecte (ligne « Secteur » :
   citer l'entree du classeur telle quelle) ; si l'affaire est ABSENTE
   du classeur ou son domaine illisible -> question B a FT2E et choix
   provisoire argumente, jamais silencieux.
6. EN RECETTE (etape 10) : verifier sur le deploiement que la fiche
   repond au bon filtre de /references (compteurs de chips) et parait
   sur sa page /secteurs/<slug> - sondes : references/ref_040/
   sonde-filtres.mjs et references/ref_040/sonde-fiche.mjs (URL a adapter).
   ⚠ Une page /secteurs/<slug> n'affiche que les 4 affaires les plus
   recentes du secteur (tri par numero decroissant) ; le filtre de
   /references, lui, montre tout. Une affaire a DOUBLE domaine doit
   etre controlee sur LES DEUX filtres et LES DEUX pages de secteur.
   ⚠ 20-071 est un numero de 2020 et le secteur « Tertiaire / ERP » est
   le PLUS FOURNI du catalogue (13 fiches) : elle ne remontera
   vraisemblablement pas dans le top 4 de /secteurs/tertiaire-erp. C'est
   le tri documente, PAS un defaut - la N17 a rencontre exactement ce cas
   (21-074, cinquieme du secteur Industriel, absente du top 4). Le filtre
   de /references reste la mesure qui fait foi.
   Repartition attendue AVANT la N18, mesuree le 2026-09-01 sur le
   deploiement par references/ref_040/sonde-filtres.mjs : L10 T13 I5 P3
   C7 M4 E3 pour 40 fiches, 45 en pondere (Yachtman T+C, Loti P+C, foyer
   CDAIR T+C, Central Hostel T+C et Cabanes Urbaines T+C comptent double).

DOSSIER DU JOUR : « 20-071- Bureaux EIFFAGE St Jean D'Angely - Impact
Urbanisme » (72 fichiers, 37,7 Mo), classeur « 20071 · Bureaux EIFFAGE ·
T ». C'est le mieux documente des deux dossiers restants de la tranche.
Points d'attention connus AVANT ouverture :
(a) TROIS noms figurent au nom de repertoire - « Bureaux EIFFAGE »,
    « St Jean D'Angely » et « Impact Urbanisme ». Etablir lequel est le
    MAITRE D'OUVRAGE, lequel l'ARCHITECTE et lequel la COMMUNE. « Impact
    Urbanisme » est vraisemblablement l'architecte : IL EST DEJA PUBLIE
    SUR LE SITE comme « architecte mandataire du groupement de maitrise
    d'oeuvre » de la fiche passerelle-ecluse-carreau-d-or-marans (affaire
    24-034). VERIFIER la graphie sur la page de garde d'un contrat ou
    d'un marche, et VERIFIER si les deux affaires se repondent ;
(b) EIFFAGE est un groupe national. Verifier quelle ENTITE est le maitre
    d'ouvrage (Eiffage Construction ? Eiffage Energie ? une filiale
    regionale ?) et si l'operation est un siege d'agence. Le champ `lieu`
    exige un code postal a cinq chiffres entre parentheses, et
    `commune()` echoue bruyamment sans lui. Saint-Jean-d'Angely est en
    Charente-Maritime (17400) - a confirmer sur piece ;
(c) ⚠ ATTENTION AU PRECEDENT N13 : le repertoire porte « 20-071 » mais
    l'affaire pourrait avoir un autre numero, ou le dossier contenir des
    pieces d'une affaire voisine. Relever NN-NNN sur une piece FT2E ;
(d) une affaire de BUREAUX peut porter un lot photovoltaique, une GTB,
    ou un traitement d'air a debit variable : ce sont des matieres a
    these. Mais VERIFIER D'ABORD que la these n'est pas deja publiee -
    voir ci-dessous ;
(e) ⚠ une note ou un rapport peut ne pas boucler. La N16 en a releve
    CINQ dans un seul dossier ; la N17 a verifie que ses quatre gains
    RT se recalculaient exactement AVANT de composer un dessin
    proportionnel dessus. Verifier que les sous-totaux somment AVANT de
    composer quoi que ce soit de proportionnel.
Aucun numero 20-071 n'est publie (verifie au grep de
src/content/projets/*.md le 2026-09-01).
ATTENTION DISQUE (~4,5 Go libres) : supprimer d'abord le repertoire extrait
de la session precedente -
C:\claude_code_dev_projects\ft2e_new_archives\2023 (le REPERTOIRE, pas le
ZIP ; il contient 2023/21-074- Projet AP Yacht...) - par python
shutil.rmtree (le rm -rf est REFUSE par les permissions).
Puis extraire LE SEUL dossier du jour PAR PYTHON ZIPFILE (members filtres
sur « 20-071 » via zipfile.namelist() - les noms portent des accents en
mojibake, ne JAMAIS taper un chemin). Le ZIP est la source, il ne se
supprime pas.
⚠ L'extraction a recree la racine interne en N10, N15, N16 et N17
(ft2e_new_archives\2023\2023\<dossier>) mais PAS en N11-N14 : ne jamais
presumer la profondeur, descendre par os.listdir.
Dossier de travail a creer : references/ref_041/
Slug cible : a etablir au depouillement (kebab-case sans accents,
verifier qu'il n'ecrase rien).

CE QUE LES N01-N17 ONT ETABLI (verifiable au depot) :
- ⚠ UN INDICE DE CONTRAT N'EST PAS UNE AFFAIRE - confirme trois fois
  (N15 : 20-045 / 20 045 A / 20-045-CSSI ; N16 : 21 086 A a H, HUIT
  contrats pour SEPT sites ; N17 : 21 074 A pour l'APS et 21 074 nu pour
  l'audit). Le depart se fait sur les pieces de PRODUCTION, qui portent
  le numero SANS indice, et le classeur ne connait qu'une entree. Ne
  jamais decouper une affaire sur ses contrats.
- ⚠ UN FAUX NUMERO D'AFFAIRE PEUT ETRE UN VRAI NUMERO D'UNE AUTRE AFFAIRE
  (N17, aggravation du piege des N09-N15). Le CCTP CVC d'AP Yacht designe
  ses centrales par « ETT ULTI+ 21-095 » et « ETT ULTI+ 22-200 » : ce sont
  des references de MODELE du constructeur, et « 21-095 » est le numero
  REEL de l'affaire VoltAero, deja publiee. Les 45 comptes rendus sont
  prefixes « 534 », numero de dossier du maitre d'oeuvre BF ECO. Relever
  tout `\d{2}[-\s]\d{3}` du dossier et etablir, un par un, ce que chacun
  designe AVANT d'en publier aucun.
- ⚠ UN COMPTE DE FICHIERS N'EST PAS UN COMPTE DE CHOSES (N17). Le dossier
  d'AP Yacht porte 45 comptes rendus de chantier, mais ils sont numerotes
  de 1 a 47 : les n°36 et 37 manquent a l'archive. Le premier jet de la
  fiche publiait « 45 reunions » - un compte de fichiers pour un compte de
  reunions. Recompter la NUMEROTATION, pas les entrees du repertoire.
- ⚠ LE MAITRE D'OUVRAGE N'EST PAS TOUJOURS L'OCCUPANT, NI LA MEME RAISON
  SOCIALE D'UNE PIECE A L'AUTRE (N16, N17). Chez AP Yacht, la synthese RT,
  les 45 comptes rendus et l'avenant signe disent « AP Yacht Conception » ;
  les deux CCTP et les deux contrats d'honoraires disent « CATANA GROUP ».
  Renseigner `moa` sur le SIGNATAIRE de l'avenant, ecrire la divergence en
  question B, et nommer le groupe au recit.
- ⚠ UNE THESE PEUT ETRE DEJA PUBLIEE - et c'est desormais le risque
  PRINCIPAL, avec 40 planches au corpus. AVANT d'arreter une these, lire
  les `sous_titre` ET les `archetype_motif` des 40 planches
  (PYTHONIOENCODING=utf-8 python -c "..." sur public/images/projets/*/
  planche.json). La N17 a du ABANDONNER sa premiere these - « trois
  regimes d'air, chacun commande par ce qui l'exige » - parce que le siege
  RESE la publie mot pour mot ; puis sa deuxieme - « l'extension n'a pas de
  source neuve » - parce que Fountaine Pajot la publie (mecanisme `greffe`),
  alors meme que le compte d'AP Yacht bouclait parfaitement (478 kVA pris
  sur un TGBT de 1 000). La question n'est plus « est-ce que ca demontre
  bien ? » mais « est-ce que ca demontre quelque chose que le corpus ne
  demontre pas deja ? ».
- ⚠ LE SILENCE D'UNE PIECE EST UNE CONSIGNE DE DESSIN (N17). La synthese RT
  d'AP Yacht laisse la colonne « Gain en % » VIDE sur la ligne Tic, dans
  les deux tableaux : FT2E ne calcule pas de gain proportionnel sur une
  temperature. Normaliser 30,2/32 en 94 % pour obtenir une jolie grille de
  six barres aurait fait affirmer au dessin une proportion que sa propre
  source refuse de calculer. Le Tic a donc recu un SECOND REGISTRE, avec
  son unite. Lire ce qu'une piece NE dit pas.
- ⚠ UN DOSSIER D'ARCHIVES PEUT CONTENIR LES PIECES D'UNE AUTRE AFFAIRE
  (N13). Lire la PAGE DE GARDE (« N° affaire : ... », « Affaire n° : ... »)
  de CHAQUE piece technique avant d'en tirer une valeur. Les N14 a N17 ont
  rejoue ce controle et trouve des dossiers integres : le controle se fait,
  son resultat n'est pas acquis d'avance.
  Corollaire : une affaire peut n'avoir AUCUNE piece technique FT2E au
  dossier. La fiche reste publiable si trois familles de sources la
  soutiennent - programme du maitre d'ouvrage, comptes rendus de
  chantier, CV de l'equipe -, a condition que chacune soit NOMMEE en
  collecte et qu'aucune valeur de dimensionnement ne soit inventee.
- LES CV DE L'EQUIPE SONT UNE SOURCE FT2E (livrables/cv-ft2e/CV-FT2E.zip,
  edition aout 2026, six CV en .docx lisibles par zipfile+regex sur
  word/document.xml). La N13 y a trouve le perimetre reel de la mission ;
  la N14 la mention SSI qui a ouvert une question B ; la N15 la
  reconciliation d'un conflit de millesime ; la N17 trois CV (Braud,
  Jaoul, Slawski) qui nomment l'affaire et ses lots. Les interroger
  systematiquement au croisement commercial (etape 4), avec les docx
  sectoriels, le classeur et docs/20-source-plaquette-2024.md.
  ⚠ Un CV peut annoncer une mission que le CCTP dement (N14 et N17 : SSI
  annonce au CV, mis a la charge du maitre d'ouvrage par le CCTP). La
  piece contractuelle gagne, et l'ecart va en question B.
- annee_livraison se pose sur le classeur ; quand pieces et classeur se
  contredisent, le classeur est suivi ET la contradiction est ecrite en
  B1, jamais tranchee en silence. Le PV de reception manque presque
  toujours - mais il se cherche a SIX endroits : un CR d'OPC portant
  « RECEPTION DES TRAVAUX » en tete (N11) ; un CR annoncant la reception a
  une date precise avec le planning des semaines suivantes (N12) ; le
  BILAN DE FACTURATION, les honoraires d'AOR ne se facturant qu'une fois
  la mission finie (N12) ; le DERNIER CR DE CHANTIER, dont l'en-tete
  remplace « PROCHAINE REUNION » par « RECEPTION le JJ/MM/AAAA » (N13) ;
  LE CALENDRIER EN TETE DE CHAQUE CR D'OPC (N14) ; et L'EN-TETE DES
  DERNIERS CR, qui porte « Reception du chantier : JJ/MM/AA » plusieurs
  semaines a l'avance (N15). ⚠ L'indice des honoraires d'AOR NE JOUE PAS
  quand le BET ne porte pas l'AOR a la repartition (cas N14) - ni quand il
  la porte mais qu'aucun bilan de facturation n'est au dossier (cas N17).
  ⚠ Sur une mission d'ETUDE SANS TRAVAUX (N16), il n'y a pas de reception
  du tout : la date qui fait foi est celle du DERNIER RAPPORT REMIS.
  ⚠ En N17, les SIX emplacements ont ete fouilles sans resultat : aucune
  occurrence de « reception des travaux », « OPR » ni « operations
  prealables » dans les 45 CR. Le classeur a tranche, l'ecart est ecrit.
- Le numero FT2E se releve sur page de garde CCTP (« Affaire n° : ... »),
  cartouche de plan (« Reference Affaire : ... »), etude thermique (pied
  ou EN-TETE de chaque page - N17), contrats et propositions FT2E, EN PIED
  DE CHAQUE PAGE d'une note methodologique (N15), et EN TETE DE CHAQUE
  PAGE d'un rapport d'audit (N16). ⚠ Un meme bureau ecrit son numero de
  PLUSIEURS facons dans un meme dossier : « 21-074 », « 21074 » et
  « 21 074 A » cohabitent chez AP Yacht.
  ⚠ EN DERNIER RECOURS SEULEMENT, quand aucune piece FT2E n'existe au
  dossier (N13), il se releve sur le CLASSEUR + le nom du repertoire
  d'archives, et cela DOIT faire l'objet d'une question B.
- Les numeros des MANDATAIRES et donneurs d'ordres pietinent les
  pieces : BF ECO « 534 » (N17) ; declaration de travaux
  « DT 2022090895299S16 » et references constructeur « NUG31440 » (N15) ;
  ASP « 2301 », bon de commande EQUANS « 0023284014 » (N14) ; SD
  Architectes « 21.17 », marche public « 20210000200 », dossier RESE
  « TRX021847 » (N13) ; SEMDAS « 2507 », ARCHITEM « 1821 » (N10) ; Equans
  « 22984760 » (N09) ; CPAM « PA 2024 - MO01 » (N08). ⚠ Attention aussi
  aux DESIGNATIONS DE BATIMENT qui ressemblent a des numeros (« 5-8 » chez
  Fountaine Pajot) et aux REFERENCES DE MODELE (« ULTI+ 21-095 », N17).
- ⚠ UN CCTP PEUT SE CONTREDIRE EN INTERNE (N11), ET UN RAPPORT AUSSI
  (N16). Retenir le paragraphe QUI DENOMBRE ou QUI RELEVE, l'ecrire dans
  a_valider_ft2e, en faire une question B - et ne PAS publier de compte
  que la piece ne soutient pas.
- ⚠ RECOMPTER LIGNE A LIGNE CE QU'ON ANNONCE (N15, N16, N17). Tout
  effectif, toute somme et tout compte portes a une fiche ou a une planche
  se recomptent sur la piece, jamais sur leur souvenir. La N16 a recompte
  ses dix surfaces pour publier 9 131 m² ; la N17 a recalcule ses quatre
  gains RT (ils bouclent a la decimale), verifie son bilan aeraulique
  (37 000 - 32 000 = 5 000) et son bilan de puissance (389 + 47 + 42 =
  478), et corrige un compte de reunions.
- ⚠ UNE NOTE DE CALCUL PEUT NE PAS BOUCLER (N14, cinq fois en N16). Ne
  JAMAIS composer un schema proportionnel (sankey, jauge, largeurs) sur
  des valeurs qui ne se ferment pas. La N16 a EXCLU les temps de retour de
  sa planche pour cette raison, et l'a ecrit au bloc
  `exclusions_appliquees`.
- NOMMER LE CLIENT FINAL : un nom deja publie par FT2E (plaquette,
  corpus secteurs, docx sectoriels, classeur, CV) se reprend, avec E1
  (N09 Airbus, N10 CDAIR, N11 Undertech, N12 Central Hostel, N13
  VoltAero, N14 Fountaine Pajot, N15 Cabanes Urbaines, N16 ADEI, N17
  AP Yacht / Catana - trouve dans le corpus SECTEURS, dans la plaquette
  ET dans trois CV) ; un nom couvert par une clause de confidentialite
  reste hors slug et hors titre (N08 CPAM).
  ⚠ **Chercher aussi dans le CORPUS SECTEURS** : la N15 a decouvert
  qu'une PHOTOGRAPHIE de son affaire etait deja publiee sur
  /secteurs/coordination-ssi, et la N17 un cliche legende « Catana Group,
  Marans » sur /secteurs/industriel-commercial - le grep de src/content/
  doit couvrir les legendes et les alt des cliches, pas seulement la
  prose. Aucun nom de tiers ne monte jamais sur la planche.
- ⚠ UNE GRAPHIE PEUT ETRE FAUSSE PARTOUT SAUF DANS LES PIECES FT2E (N13,
  N17). Chez AP Yacht, le nom du repertoire d'archives ET la plaquette
  2024 ecrivent « Simoneau » (un N) ; les pieces FT2E et la feuille de
  presence des comptes rendus ecrivent « SIMONNEAU » (deux N). Relever la
  graphie sur la page de garde d'un contrat ou d'un marche, retenir la
  majoritaire, ecrire la divergence en question B - et VERIFIER TOUJOURS
  si l'acteur est deja nomme dans src/content/projets/*.md avant d'ecrire
  `architecte` ou `moa` (pour la N18 : « Impact Urbanisme » l'est deja).
- ⚠ UN SITE PUBLIE PEUT PORTER UNE DATE OU UNE GRAPHIE FAUSSE (N15, N17).
  Corriger une page publiee est legitime quand une piece FT2E tranche,
  MAIS cela s'ecrit en question B et se signale au message final - jamais
  en silence.
- ⚠ L'AGENT DE RELECTURE TROUVE DES ERREURS DE FAIT SANS AVOIR LES PIECES
  (N15). Traiter chaque question de compte comme une piste a verifier SUR
  LA PIECE, jamais comme une remarque de style ; et se relire soi-meme
  sur le critere « les items enumeres correspondent-ils au nombre
  annonce ? ». ⚠ Corollaire : lui donner en contexte les faits etablis
  sur piece (c'est ce qui lui permet de croiser), et lui demander
  EXPLICITEMENT les chaines exactes avant/apres - il travaille EN LECTURE
  SEULE, ses outils d'edition normalisent les insecables du depot.
- Archetypes apres N17 : boucle-fluide 11 - coupe-traversee 7 -
  tableau-electrique 7 - sankey-energie 7 - zonage-ssi 6 -
  chronologie-affaire 2 - planche-chiffree 0 SANS module. L'archetype se
  choisit sur la THESE, jamais sur le secteur ni sur le quota, mais a
  these egale preferer ce qui n'a pas servi depuis longtemps ; la dette
  de variete porte toujours sur boucle-fluide (11/40), et
  chronologie-affaire n'a pas servi depuis le corpus fondateur
  (admissible seulement si sa these est d'INGENIERIE, jamais le
  calendrier d'une operation). ⚠ `planche-chiffree` n'a toujours pas de
  module : si un dossier l'exige, la decision est de L'ECRIRE ou de
  retirer l'archetype de la liste fermee (§ 1 du plan), jamais de
  bricoler.
- Un mecanisme nouveau s'ecrit DANS le compositeur d'archetype
  (constantes prefixees par le mecanisme ; garde-fou de greffe sur le
  NOM DE LA FONCTION ET sur les prefixes de constantes - automatise
  depuis la N13 : en N17, 9 fonctions, 31 constantes SG_ et 10 helpers
  reutilises verifies), et l'invariant octet se rejoue AVANT la greffe,
  APRES la greffe et APRES la derniere retouche.
  ⚠ L'INSTRUMENT EXISTE AU DEPOT ET SE REJOUE SEUL, NE PAS LE REECRIRE :
  `python scripts/planches/invariant.py` couvre les 6 compositeurs et les
  40 dossiers (160/160 pieces au 2026-09-01),
  `python scripts/planches/invariant.py <archetype>` un seul.
  ⚠ Un dossier neuf dont la planche n'est pas encore composee fait ECHOUER
  l'invariant sur un FileNotFoundError : ce n'est pas une rupture, ce sont
  les pieces qui n'existent pas encore. Composer d'abord, mesurer ensuite.
- ⚠ METTRE UNE ASSERTION DE DEPASSEMENT DANS LE COMPOSITEUR, ET SUR LES
  TROIS FORMATS (N14, rejouee en N15, N16 et N17). Chaque chaine dessinee
  est mesuree par `mesurer()` contre la largeur interieure de son
  contenant, versee dans une liste, et un `assert not trop` rompt la
  composition avant tout rendu. En N17 : 18 chaines sur la planche, 3 sur
  la vignette, 9 sur l'appui, 0 depassement, publie au bloc `controles`.
- ⚠ NOUVEAU EN N17 : LES TROIS FORMATS DOIVENT PARTAGER UNE SEULE
  IMPLANTATION DE LEUR PRIMITIVE. Le premier jet du mecanisme `serrage`
  ecrivait sa barre trois fois - planche, vignette, appui - avec dans
  chacune un seuil de bascule « barre ou marque » ecrit a la main. A 1 px
  de seuil, la vignette basculait une marge de 0,28 % en marque de contact
  et la planche la laissait en barre de 2,4 px : LE MEME FAIT SE LISAIT DE
  DEUX FACONS SELON LA TAILLE SERVIE. Ni le build, ni le bloc `controles`,
  ni l'assertion de depassement ne pouvaient le voir - seule la
  comparaison des trois PNG cote a cote l'a montre. La correction n'a pas
  ete d'accorder les trois seuils mais de n'en garder qu'un, et de le
  DERIVER (une barre plus courte que la marque de contact devient la
  marque) au lieu de le choisir.
- ⚠ LE BLOC `controles` REND COMPTE DU TRACE, PAS DE L'INTENTION (N17,
  regle dure 6 « mesurer, pas affirmer »). Il annoncait « 2,4 px » pour
  une barre qui n'est pas tracee en barre : une cle `marques_de_contact` a
  ete ajoutee, qui dit combien de valeurs sont passees sous le seuil et
  lesquelles. Ecrire dans `controles` ce qui est SORTI du compositeur.
- ⚠ NE PAS REECRIRE rendre_png.py : il est au depot depuis la N12, avec
  les deux pieges encodes (retrait de l'attribut style de racine par
  REGEX - sans quoi la vignette rend BLANCHE sans erreur - et fusion des
  filets a 8 chiffres). Usage :
  `python scripts/planches/rendre_png.py public/images/projets/<slug>
  <scratchpad>` ecrit planche.png 2400x1600 dans le dossier et, dans le
  scratchpad, les quatre controles (1152, vignette 274 et 296, appui
  552). REGARDER LES QUATRE. ⚠ Il s'appelle depuis la RACINE du depot.
  ⚠ Quand un detail est trop petit pour etre juge a l'oeil sur le PNG,
  NE PAS PLISSER LES YEUX : recadrer et agrandir par PIL (crop + resize
  NEAREST) et comparer les deux zones cote a cote. La N17 a cru a une
  marque manquante sur l'appui ; l'agrandissement x4 a montre qu'elle
  etait la et identique a l'autre.
- ⚠ LE RENDU CAIROSVG N'A PAS LES POLICES DU SITE (N13, N14, N16) : il
  retombe sur une police de substitution dont la chasse mono est ~7 a 8 %
  plus large que celle d'IBM Plex Mono. Consequence : le dernier caractere
  du cartouche de legende parait COUPE sur le PNG de controle - ne PAS
  « corriger » la largeur du cartouche, la formule `mesurer(...) + 40` est
  commune aux 40 planches, et le rendu du deploiement confirme qu'il est
  entier. ⚠ La MEME sous-mesure vaut pour tout fond papier pose derriere
  un mono, et pour toute marge serree : prendre 8 % de large.
- ECRIRE LES CHAINES COURBES DES L'ECRITURE - extraction planche.json
  COMPRISE. La recette, tenue en N11 a N17 : dans le script d'extraction
  lui-meme, avant ecriture, une assertion `"'" not in sortie`, une
  assertion `M not in sortie` sur chaque marqueur, et une assertion A
  L'EGALITE sur le COMPTE d'insecables - ce compte se LIT sur le source
  du script (nombre de marqueurs dans le litteral), jamais ecrit a la
  main. ⚠ Employer DEUX marqueurs distincts, «   » pour la fine U+202F et
  «   » pour l'insecable U+00A0, avec deux assertions comptees
  separement. Ne PAS prendre « # » (collision avec les titres Markdown).
  ⚠ ET ECRIRE LES ACCENTS DIRECTEMENT : la normalisation de Write porte
  sur les INSECABLES, pas sur les accents. La N17 a ecrit son extraction
  entiere SANS accents au premier jet et a du la refaire : un
  a_valider_ft2e sans accents est illisible pour FT2E, qui en est le seul
  lecteur, et un aria_label sans accents est PRONONCE FAUX par les
  lecteurs d'ecran. Poser un garde-fou d'accents dans le script.
  ⚠ MAIS LE CALIBRER SUR UNE MESURE, ET LE LIMITER A LA PROSE : le
  premier garde-fou de la N17 exigeait « plus de 400 caracteres
  accentues » sur un texte qui en porte 183 (soit 3 %, le taux courant du
  francais) - un seuil devine, qui a echoue sur du texte parfaitement
  accentue. Et sa recherche de formes non accentuees portait sur le JSON
  ENTIER, ou elle attrapait les CLES TECHNIQUES et les IDENTIFIANTS
  (`"registre": "temperature"`, `sankey-energie`), volontairement en
  ASCII. Mesurer d'abord, seuiller ensuite, et ne chercher que dans la
  prose lue.
  La passe `python scripts/apostrophes-planches.py` (sans argument, en
  MESURE) n'a alors rien a courber - 0 sur 0 en N14, N15, N16 et N17. Les
  apostrophes qu'elle REFUSE sont de la syntaxe de f-string : c'est le
  comportement voulu.
- Les avances calibrees de _tronc.mesurer sous-mesurent Archivo 600 au
  rendu d'environ 20 % (N08-N09) - prendre la marge DANS LE CODE
  (`mesurer(...) * 1.2`), pas a l'oeil.
- REGARDER LES PNG, ET CORRIGER CE QU'ON Y VOIT. La N16 a fait CINQ
  retouches que ni le build ni le bloc `controles` n'auraient signalees ;
  la N17 en a fait DEUX, dont une refonte de primitive (voir ci-dessus) et
  le deplacement d'une mention « AU BORD » qui etait posee au bout de la
  colonne, a 440 px de la barre qu'elle qualifiait.
  ⚠ Piege generique confirme en N13 a N17 : deux traits qui se croisent,
  ou un trait et un texte, doivent differer par autre chose que leur
  position - epaisseur, continuite, etiquette a fond papier
  (`_etiquette`), ou deplacement en zone franche.
  ⚠ Et une LEGENDE DOIT TOUCHER CE QU'ELLE NOMME : posee au bout de la
  colonne, elle cesse de nommer.
- Quand aucune surface n'existe au dossier, la chercher dans les DOCX
  COMMERCIAUX (N12) ; si elle n'y est pas non plus (N13), laisser
  `surface_m2` VIDE et porter au cartouche la grandeur qui compte
  l'ouvrage, avec question B. ⚠ Quand PLUSIEURS surfaces existent et
  divergent (N14, N17), retenir celle qui designe EXPLICITEMENT l'objet de
  la fiche, ecrire les autres en a_valider_ft2e, et n'en publier qu'une
  seule en prose. ⚠ En N17, le choix a ete fait sur une raison de DESSIN :
  la surface publiee (2 172 m² de surface RT) est la somme des deux
  surfaces que la planche porte, pour que le cartouche et les colonnes se
  repondent.
- Les insecables des heredocs bash sont normalisees DE FACON NON
  DETERMINISTE sur cette machine. DEUX VOIES, toutes deux eprouvees :
  (a) ecrire le .md en ESPACES ORDINAIRES et apostrophes droites par
  l'outil Write, puis passer `python scripts/injection-typographique.py
  <fichier>` qui pose les insecables, les guillemets et les U+2019 -
  c'est la voie des N12 a N17, la plus sure ; (b) script Python avec
  marqueurs ASCII remplaces par chr(8239)/chr(160) et assertion A
  L'EGALITE comptee sur le source - la voie a suivre pour tout fichier que
  injection-typographique.py ne couvre pas (planche.json, plan du
  chantier, prompt de continuite).
  ⚠ injection-typographique.py protege les lignes d'enum du frontmatter
  (secteur, typologie, mission_ft2e) : une apostrophe DROITE tapee dans
  mission_ft2e y RESTE et casse le build - ecrire U+2019 des le script
  (piege N10, « Études d'exécution »). Il NE protege PAS
  secteur_secondaire.
  ⚠ Il ne connait pas toutes les unites : « A » (amperes), « T »,
  « tonnes », « bars », « dBA », « min », « s », « h » et le chiffre
  devant « × » lui echappent (releve en N13, N14 et N15). Verifier au
  grep les unites rares apres passage - en N17, %, °C, m², m³/h, kW, kVA
  et kWhep/m².an ont tous ete correctement traites, controle par regex sur
  « chiffre + espace ordinaire + unite », a rejouer.
  ⚠ IL NE POSE PAS LES ACCENTS NI LES EXPOSANTS : ecrire « m² », « m³/h »
  et « °C » directement. La N17 a livre un premier jet de fiche entierement
  sans accents en croyant que le script les poserait.
- ⚠ UN HEREDOC BASH PEUT MANGER UN ANTISLASH (N15, N16) ET ECHOUER SUR UNE
  APOSTROPHE (N17 : « unexpected EOF while looking for matching `'' » sur
  un heredoc pourtant quote). Pour tout script non trivial : outil Write
  dans le SCRATCHPAD, puis execution. C'est aussi la regle qui evite que le
  hook Stop commite des scripts a usage unique.
  ⚠ ET NE JAMAIS TAPER UN CHEMIN D'ARCHIVES : les noms portent des
  accents et des apostrophes typographiques. Passer par os.walk +
  fragments de nom, qui est la seule methode fiable.
- Le hook Stop commite et pousse SEUL ce qui traine, et il PEUT
  COMMITTER LE LIVRABLE ENTIER sous l'intitule generique
  « chore(deploy): pousse l'etat de fin de session ». L'historique etant
  pousse sur un depot PARTAGE, il ne se reecrit pas. Pour l'eviter :
  garder les scripts a usage unique DANS LE SCRATCHPAD, hors depot
  (pratique des N13 a N17), COMMITTER TOT des que le build est vert, et
  reserver un second commit a la passe editoriale (⚠ livrables/ porte
  deux fichiers non suivis anterieurs a la N02 - les laisser).
- /references/ est gitignore (motif ancre) - les pieces sources
  n'entrent JAMAIS au depot ; npm run preview ne mesure pas la
  performance ; Chrome refuse les fenetres sous 500 px (sonde iframe).
- La planche n'expose NI le millesime d'ouverture, NI montant, NI tiers
  (MOA, mandataire, architecte, installateur, MARQUES comprises), NI
  donnee nominative ; les designations internes (reperes de zone,
  numeros de tableau, « AGBT », « ZDA01 ») sont admises avec une entree
  a_valider_ft2e et une question E ; tout arbitrage de dessin va dans
  a_valider_ft2e (jamais vide).

DEROULER LE PIPELINE § 2 INTEGRALEMENT : depouillement (pdfinfo /
pdftotext, ou pymupdf via python subprocess avec les noms lus par
os.listdir ; les plans sans couche texte et les marches scannes se
lisent en rendant leurs pages en PNG par pymupdf, zoom 2-3 ; antiword
pour les .doc, xlrd pour les .xls, openpyxl pour les .xlsx,
extract-msg pour les .msg) -> CONTROLE DE LA PAGE DE GARDE DE CHAQUE
PIECE TECHNIQUE -> releve du numero NN-NNN sur piece FT2E, et
ETABLISSEMENT DE CE QUE DESIGNE CHAQUE AUTRE SUITE `NN-NNN` DU DOSSIER ->
references/ref_041/ (3 a 8 pieces) -> croisement commercial
(references/docs_references/ - docx sectoriels ET classeur ODS - +
docs/20-source-plaquette-2024.md + livrables/cv-ft2e/CV-FT2E.zip +
grep de src/content/ pour ce que le site publie deja, LEGENDES ET ALT
DES CLICHES COMPRIS) -> fiche de collecte (A/A+ remplies, B-E en
questions, ligne Secteur citant le classeur, DECISION Q3 motivee en
tete) -> LECTURE DES 40 SOUS-TITRES ET DES 40 `archetype_motif` pour
verifier qu'aucune these voisine n'est deja publiee -> fiche
src/content/projets/<slug>.md (SECTEUR RELEVE AU CLASSEUR ; taxonomie
ACTUELLE ; lieu avec code postal entre parentheses ; synthese 480-780 ;
>= 5 liens internes ; jamais de numero d'affaire NI de millesime
d'ouverture en prose ; convention numerale finale - nom du NOMBRE en un
seul mot en lettres, nombre COMPOSE en chiffres, unites et mesures
toujours en chiffres, citations intouchees ; verifier par
`python scripts/releve-numeral.py`, dont la section « Nombres COMPOSES
ecrits en lettres » doit rendre 0) -> PLANCHE complete (extraction avec
a_valider_ft2e non vide, apostrophes courbes ET ACCENTS des l'ecriture,
composition par scripts/planches/<archetype>.py avec assertion de
depassement SUR LES TROIS FORMATS et primitive PARTAGEE, rendus par
scripts/planches/rendre_png.py depuis la RACINE, controles a 1152 /
carte 274-296 / appui 552 - REGARDER les quatre PNG, et AGRANDIR par PIL
tout detail douteux -, apostrophes-planches.py en MESURE, invariant.py,
verser.py) -> qualite (typecheck 0, build vert 64 pages,
editorial-reviewer EN LECTURE SEULE - ses outils d'edition normalisent
les insecables, appliquer ses constats par script -,
controle-liens-internes 41/41 a 5, controle-numeros-affaire 0 fuite,
releve-numeral sans ecart nouveau) -> COMMIT UNIQUE fiche+planche+
compositeur (content(references): ajoute la fiche reelle <nom> et sa
planche ; git ls-remote avant, depot partage) -> push (le push deploie),
curl de la fiche AVEC barre oblique finale + marqueur de build, rendu
controle aux trois bandes (sonde iframe pour les largeurs telephone :
references/ref_040/sonde-fiche.mjs, slug et URL a adapter) ET CONTROLE
DE L'INDEXATION SECTORIELLE (point 6, sonde
references/ref_040/sonde-filtres.mjs, appelee DEPUIS LA RACINE) ->
ligne de suivi au plan -> PROMPT DE LA SESSION N19 en annexe du plan
(script Python ou Write, jamais un long heredoc) et reproduit
integralement dans le message final.
Le prompt N19 REPREND le bloc « REGLE D'INDEXATION SECTORIELLE » tel quel
(repartition remise a jour) ET porte le CINQUIEME et DERNIER dossier de la
tranche 2023 (21-029 Ecole primaire et maternelle, La Flotte en Re,
classeur M - qui repeuplera le secteur Monotechnique-Audit, a 4 fiches).
Il RAPPELLE aussi l'ecart 49 / 50 tant qu'il n'est pas tranche, ET la
piste de la section « Finalisees en 2021 » vide au classeur.

Portee de commit : content(references). Un changement de schema Zod
eventuel passe par le sous-agent content-modeller et va dans le MEME
commit que public/admin/config.yml.

Termine par le prompt de lancement de la session N19, en annexe du
plan du chantier et reproduit integralement dans ton message final -
la regle de continuite est dans CLAUDE.md parce qu'elle a ete manquee
deux fois.
```

## Annexe S — prompt de lancement de la session N19

```
Session N19/27 - FT2E v3 : chantier des 27 nouvelles fiches references.
DIX-NEUVIEME dossier - CINQUIEME et DERNIER de la tranche
« Finalisees en 2023 ».

Contexte. FT2E v3 est le site institutionnel du bureau d'etudes FT2E
(La Rochelle), Astro 6 statique, deploye en demonstration client sur
https://ft2e-v3.vercel.app (indexation verrouillee - ne pas y toucher).
Le catalogue porte 41 fiches reelles (23 + N01 Portes-en-Re + N02 Fors +
N03 Aurora + N04 Loti + N05 Saint-Sauveur + N06 L'Houmeau + N07 Louise
Magnan + N08 bornes IRVE + N09 comptage Airbus + N10 foyer CDAIR +
N11 parc Undertech + N12 auberge Central Hostel + N13 batiment VoltAero +
N14 extension Fountaine Pajot + N15 Cabanes Urbaines + N16 audit ADEI +
N17 atelier AP Yacht + N18 siege Eiffage Energie), chacune illustree
d'une planche de schema de principe (cinq pieces par dossier).
Objectif : 50 fiches. 1 session = 1 dossier, close par le prompt de la
suivante.

LE ZIP DE LA TRANCHE 2023 EST DEJA SUR LE DISQUE :
C:\claude_code_dev_projects\ft2e_new_archives\2023.zip (446 Mo, 670
entrees, racine interne « 2023/ », un repertoire par affaire). UN SEUL
dossier y reste, absent du site (verifie au grep de
src/content/projets/*.md le 2026-09-01) :
-   54 fichiers, 14,2 Mo : « 21-029 - Ecole primaire et maternelle -
    La Flotte en Re » (classeur M)  <- DOSSIER DU JOUR
IL N'Y A DONC AUCUNE QUESTION A POSER EN OUVERTURE : derouler directement.
CETTE SESSION CLOT LA TRANCHE 2023.

⚠ NE JAMAIS conclure « mince » ni « riche » sur le seul compte de fichiers :
quatre dementis en N08-N09 (mince qui etait riche), un dementi INVERSE en
N13 (« 21-095 » annoncait 72 fichiers dont 17 appartenaient a l'affaire
21-093), et cinq dossiers integres en N14, N15, N16, N17 et N18. C'est la
PAGE DE GARDE qui dit a quelle affaire une piece appartient, jamais le
repertoire qui la contient. Verifier la page de garde de chaque CCTP,
DPGF, estimation, rapport et plan AVANT d'en tirer la moindre valeur.

⚠ CE QUI RESTE APRES 2023, ET L'ECART 49 / 50 TOUJOURS NON TRANCHE. Le
classeur ODS porte, apres la tranche 2023 : « Finalisees en 2022 » (4 :
19087 Batiment SSLIA I, 20024 INNOVIA-GAELIC I, 20039 Videosurveillance
CH Rochefort M, 22037 Audit chambre des metiers M), « Finalisees en 2020 »
(2 : 19008 Batiment industriel Aeroport LR ELIXIR I, 20058 Diag
legionelles du port de plaisance M) et « Finalisees en 2019 » (1 :
18026 Atelier numerique Fountaine Pajot I). Soit 1 (2023) + 4 + 2 + 1 = 8
dossiers restants pour 41 fiches en ligne : LE CLASSEUR NE MENE QU'A 49,
PAS A 50. La question a ete portee aux messages finaux des N16, N17 et
N18 et N'A TOUJOURS PAS ETE ARBITREE PAR FT2E : la reposer tant qu'elle
reste ouverte. Ne pas fabriquer une fiche pour combler l'ecart.
⚠ PISTE RELEVEE EN N17, TOUJOURS OUVERTE : le classeur porte une section
« Finalisees en 2021 » qui est VIDE. C'est le seul millesime sans aucune
entree, entre 2020 (2 entrees) et 2022 (4 entrees). L'hypothese a soumettre
a FT2E est qu'une affaire manque a cette section - ce qui expliquerait
l'ecart exactement. A verifier avec eux, pas a supposer.
Les ZIP 2019.zip et 2022.zip SONT DEJA SUR LE DISQUE ; celui de la tranche
2020 devra etre demande en ouverture de la session qui closera 2022.

LIRE D'ABORD, dans cet ordre :
1. docs/superpowers/plans/2026-08-27-chantier-27-nouvelles-fiches.md -
   LE PLAN : § 1 (ce qui a change), § 2 (pipeline 12 etapes), § 3
   (reponses consignees Q1/Q2 2024 + complement N02 : le classeur fait
   foi ; Q3 = regle des dossiers minces, defaut reconduit), § Suivi
   (lignes N01 a N18), annexe S (ce prompt).
2. docs/superpowers/plans/2026-08-07-chantier-references-reelles.md -
   § Contraintes globales + § Protocole de session + § Regle des
   dossiers minces.
3. docs/superpowers/specs/2026-08-12-planches-references-protocole.md -
   revision 5 EN ENTIER.
4. CLAUDE.md, .claude/rules/content-collections.md et french-editorial.md.
Etalons : src/content/projets/creche-oranger-perigny.md (fiche) et, pour
une affaire MONOTECHNIQUE - AUDIT, les quatre fiches du secteur M -
audit-chauffage-sites-adei.md (sept sites medico-sociaux, le plus proche
d'une mission d'etude), bornes-irve-la-rochelle-saintes.md,
passerelle-ecluse-carreau-d-or-marans.md et
plan-comptage-energie-airbus-rochefort.md. Voir AUSSI, pour un
etablissement SCOLAIRE, cuisine-groupe-scolaire-villedoux.md.
Voir aussi src/content/projets/siege-eiffage-saint-jean-d-angely.md +
public/images/projets/siege-eiffage-saint-jean-d-angely/ +
references/ref_041/ (fiche de collecte N18, avec sa DECISION Q3 en tete -
c'est elle qui documente le piege du FAUX NUMERO DANS UNE PAGE DE GARDE
FT2E et les trois valeurs ecartees faute de pieces).
Les sondes de recette vivent dans references/ref_041/ (sonde-fiche.mjs ET
sonde-filtres.mjs, toutes deux adaptees en N18) - URL, slug et secteur a
adapter. La sonde de filtres s'appelle DEPUIS LA RACINE du depot.

REGLE D'INDEXATION SECTORIELLE - etablie le 2026-08-27, A APPLIQUER A
LA REDACTION DE CHAQUE FICHE (etape 6 du pipeline), pas apres coup :
« REFERENCES SITE FT2E.ods » (references/docs_references/, classeur
fourni par FT2E) FAIT FOI pour le classement sectoriel. Concretement,
AVANT d'ecrire le frontmatter :
1. Ouvrir le classeur (python zipfile sur content.xml, ou pandoc) et y
   retrouver l'affaire PAR SON NUMERO (graphie sans tiret : « 21029 »).
2. En relever le domaine (legende : L Logements / T Tertiaire & ERP /
   I Industriel / P Patrimoine / C Coordination SSI /
   M Monotechnique-Audit / E EXE) -> champ `secteur`.
3. Si le classeur porte un domaine DOUBLE (« T § C ») : le premier est
   le `secteur`, le second va au champ `secteur_secondaire` (optionnel
   au schema depuis le 2026-08-27, garde-fou « doit differer ») - la
   fiche parait alors dans les deux filtres et sur les deux pages de
   secteur. Precedents : hotel-yachtman (T § C), maison-pierre-loti-
   rochefort (P § C, N04), foyer-cdair-saint-martin-de-re (T § C, N10),
   auberge-central-hostel-la-rochelle (T § C, N12),
   cabanes-urbaines-la-rochelle (T § C, N15).
   LE DOSSIER DU JOUR EST A DOMAINE SIMPLE : 21029 est « M ».
4. JAMAIS de deduction depuis le dossier, l'usage RT ou le nom de
   l'operation : la N02 penchait « Industriel » pour Fors, le classeur
   dit T - et les 25 fiches ont du etre re-referencees le soir meme
   (7 bascules, commits ce334b2/09270a3). Le classeur peut contredire
   l'intuition (Saint-Rogatien, pole commercial : I ; Fors, pole
   commercial : T ; 23083 « plan de comptage Airbus » : E et non M ;
   23099 « CPAM » : M - IRVE, pas T ; 23036 Fountaine Pajot : I SIMPLE
   alors que le CV annonce « CFO / CFA / SSI » ; 20045 « THE ROOF »,
   salle d'escalade et atelier de luthier : T § C et non I ; 21086
   « Audit chauffage sites ADEI », sept etablissements medico-sociaux :
   M SIMPLE ; 21074 « AP Yacht - CATANA Group », chantier naval : I
   SIMPLE ; 20071 « Bureaux EIFFAGE », un siege d'agence avec ses
   ateliers : T SIMPLE, alors que le programme porte 810 m² d'atelier
   pour 730 m² de bureaux) - il gagne.
   ⚠ ATTENTION PARTICULIERE ICI : « Ecole primaire et maternelle » est
   un ERP de type R, et l'intuition dira « Tertiaire / ERP ». LE
   CLASSEUR DIT M. Une ecole classee M signifie que FT2E n'y a tenu
   qu'un LOT ou qu'une ETUDE, pas la maitrise d'oeuvre complete : le
   depouillement doit etablir LEQUEL, et la typologie `Etude` existe au
   schema pour les missions sans travaux.
5. CONSIGNER la lecture dans la fiche de collecte (ligne « Secteur » :
   citer l'entree du classeur telle quelle) ; si l'affaire est ABSENTE
   du classeur ou son domaine illisible -> question B a FT2E et choix
   provisoire argumente, jamais silencieux.
6. EN RECETTE (etape 10) : verifier sur le deploiement que la fiche
   repond au bon filtre de /references (compteurs de chips) et parait
   sur sa page /secteurs/<slug> - sondes : references/ref_041/
   sonde-filtres.mjs et references/ref_041/sonde-fiche.mjs (URL a adapter).
   ⚠ Une page /secteurs/<slug> n'affiche que les 4 affaires les plus
   recentes du secteur (tri par numero decroissant) ; le filtre de
   /references, lui, montre tout. Une affaire a DOUBLE domaine doit
   etre controlee sur LES DEUX filtres et LES DEUX pages de secteur.
   ⚠ 21-029 est un numero de 2021 et le secteur « Monotechnique - Audit »
   ne compte que 4 fiches (23099 CPAM, 21086 ADEI, 24034 passerelle de
   Marans, 20039 a venir) : elle a une CHANCE REELLE d'entrer dans le
   top 4 de /secteurs/monotechnique - a verifier, et ce serait la
   premiere fois depuis la N16. La N18 a rencontre le cas inverse
   (20-071, secteur le plus fourni, absente du top 4) : c'est le tri
   documente, PAS un defaut, et le filtre de /references fait foi.
   Repartition attendue AVANT la N19, mesuree le 2026-09-01 sur le
   deploiement par references/ref_041/sonde-filtres.mjs : L10 T14 I5 P3
   C7 M4 E3 pour 41 fiches, 46 en pondere (Yachtman T+C, Loti P+C, foyer
   CDAIR T+C, Central Hostel T+C et Cabanes Urbaines T+C comptent double).

DOSSIER DU JOUR : « 21-029 - Ecole primaire et maternelle - La Flotte en
Re » (54 fichiers, 14,2 Mo), classeur « 21029 · Ecole primaire et
maternelle La Flotte · M ». C'est le dernier dossier de la tranche 2023.
Points d'attention connus AVANT ouverture :
(a) ⚠ LE CLASSEUR DIT M, PAS T. Etablir au depouillement CE QUE FT2E a
    reellement fait : un seul lot technique (electricite ? CVC ? SSI ?),
    un audit, une etude thermique isolee, une mission d'assistance ? La
    typologie `Etude` existe pour les missions sans travaux, et la N16
    (audit ADEI) en est le precedent le plus proche ;
(b) La Flotte est en ILE DE RE, commune de La Flotte (17630) - a
    CONFIRMER SUR PIECE. Le champ `lieu` exige un code postal a cinq
    chiffres entre parentheses, et `commune()` echoue bruyamment sans
    lui. ⚠ Le corpus porte deja quatre affaires de l'ile de Re
    (mairie-les-portes-en-re, foyer-cdair-saint-martin-de-re,
    logements-pas-des-boeufs-bois-plage, fougerou-sainte-marie-de-re) :
    les lire AVANT de rediger, pour ne pas repeter leurs formules sur
    l'insularite, et pour les lier ;
(c) ⚠ ATTENTION AU PRECEDENT N13 : le repertoire porte « 21-029 » mais
    l'affaire pourrait avoir un autre numero, ou le dossier contenir des
    pieces d'une affaire voisine. Relever NN-NNN sur une piece FT2E, et
    etablir ce que designe CHAQUE autre suite `NN-NNN` du dossier ;
(d) une ECOLE est un ERP de type R : sa notice de securite, son
    desenfumage, son alarme de type et sa ventilation par sonde de CO2
    sont des matieres a these. Mais VERIFIER D'ABORD que la these n'est
    pas deja publiee - voir ci-dessous ;
(e) ⚠ une note ou un rapport peut ne pas boucler. La N16 en a releve
    CINQ dans un seul dossier ; la N18 en a trouve une (« 160 kVA : 60
    pour l'ombriere et 60 pour le batiment B ») et l'a ecartee. Verifier
    que les sous-totaux somment AVANT de composer quoi que ce soit de
    proportionnel.
Aucun numero 21-029 n'est publie (verifie au grep de
src/content/projets/*.md le 2026-09-01).
ATTENTION DISQUE (~4,5 Go libres) : supprimer d'abord le repertoire extrait
de la session precedente -
C:\claude_code_dev_projects\ft2e_new_archives\2023 (le REPERTOIRE, pas le
ZIP ; il contient 2023/20-071- Bureaux EIFFAGE...) - par python
shutil.rmtree (le rm -rf est REFUSE par les permissions).
Puis extraire LE SEUL dossier du jour PAR PYTHON ZIPFILE (members filtres
sur « 21-029 » via zipfile.namelist() - les noms portent des accents en
mojibake, ne JAMAIS taper un chemin). Le ZIP est la source, il ne se
supprime pas.
⚠ L'extraction a recree la racine interne en N10, N15, N16, N17 et N18
(ft2e_new_archives\2023\2023\<dossier> ou \2023\<dossier> selon les cas)
mais PAS en N11-N14 : ne jamais presumer la profondeur, descendre par
os.listdir.
Dossier de travail a creer : references/ref_042/
Slug cible : a etablir au depouillement (kebab-case sans accents,
verifier qu'il n'ecrase rien).

CE QUE LES N01-N18 ONT ETABLI (verifiable au depot) :
- ⚠ UN FAUX NUMERO D'AFFAIRE PEUT ETRE DANS UNE PIECE FT2E (N18, variante
  NOUVELLE du piege des N09-N17). Chez Eiffage, le CCTP du lot 09 porte
  « Affaire n° : 20-012 » en page de garde - et c'est le SEUL document du
  dossier a le faire : sa propre DPGF, ses quatre plans, le CCTP du lot 08,
  les 15 pages de la synthese RT et le calcul d'honoraires portent tous
  20-071, et le classeur ne connait que 20071. Un releve qui se serait
  arrete a la premiere page de garde lue aurait publie un numero
  inexistant. RELEVER LE NUMERO SUR PLUSIEURS PIECES, ET RETENIR LA
  MAJORITE. Les autres faux numeros deja rencontres : references de MODELE
  du constructeur (« ULTI+ 21-095 », N17 - et 21-095 est le vrai numero
  d'une affaire publiee), numeros de dossier des mandataires (BF ECO
  « 534 », N17 ; SEMDAS « 2507 », ARCHITEM « 1821 », N10), numeros de
  permis (« 17347 20 Z0025 », N18), surfaces foncieres (« 15 079 m² »,
  N18), codes postaux, et surtout NUMEROS DE NORMES (le CCTP electricite
  d'Eiffage en portait quinze : NF C 15-100, 15-103, 15-105, 15-150,
  15-900, 14-100, 48-150, 60-598, 71-800, 71-820, 90-123/124/125, 91-102,
  ISO/IEC 11-801). Relever tout `\d{2}[-\s]\d{3}` du dossier et etablir,
  un par un, ce que chacun designe AVANT d'en publier aucun.
- ⚠ UN INDICE DE CONTRAT N'EST PAS UNE AFFAIRE - confirme trois fois
  (N15 : 20-045 / 20 045 A / 20-045-CSSI ; N16 : 21 086 A a H, HUIT
  contrats pour SEPT sites ; N17 : 21 074 A pour l'APS et 21 074 nu pour
  l'audit). Le depart se fait sur les pieces de PRODUCTION, qui portent
  le numero SANS indice, et le classeur ne connait qu'une entree. Ne
  jamais decouper une affaire sur ses contrats.
- ⚠ UN COMPTE DE FICHIERS N'EST PAS UN COMPTE DE CHOSES (N17, N18). Chez
  AP Yacht, 45 comptes rendus numerotes de 1 a 47 : la fiche publie 47.
  Chez Eiffage, 46 comptes rendus numerotes de 1 a 45 PUIS 49, le n° 45
  du 13 janvier et le n° 49 du 20 janvier etant distants d'UNE SEULE
  SEMAINE : ni 46 ni 49 n'etant etabli, LA FICHE NE PUBLIE AUCUN COMPTE.
  S'abstenir est une issue legitime quand recompter ne tranche pas.
- ⚠ LE MAITRE D'OUVRAGE N'EST PAS TOUJOURS L'OCCUPANT, NI LA MEME RAISON
  SOCIALE D'UNE PIECE A L'AUTRE (N16, N17, N18). Chez Eiffage, QUATRE
  graphies : « Eiffage Energie Systemes » (les deux CCTP, les 46 comptes
  rendus, le panneau de chantier, le docx commercial FT2E), « Eiffage
  Energie Poitou Charente » (acte d'engagement 2020), « Eiffage Energie »
  (cartouche des plans, synthese RT), et surtout « EIFFAGE ENERGIE
  REGIONS France, 78140 Velizy-Villacoublay » - la PERSONNE MORALE
  CONTRACTANTE, portee au panneau de chantier et rappelee aux comptes
  rendus n° 26 et suivants comme la seule graphie a employer sur les
  actes. Retenir la graphie MAJORITAIRE et la plus recente, verifier si
  elle est DEJA PUBLIEE sur le site, et ecrire la divergence en question B.
- ⚠ UNE THESE PEUT ETRE DEJA PUBLIEE - et c'est le risque PRINCIPAL, avec
  41 planches au corpus. AVANT d'arreter une these, lire les `sous_titre`
  ET les `archetype_motif` des 41 planches (PYTHONIOENCODING=utf-8 python
  -c "..." sur public/images/projets/*/planche.json). La N17 a du
  abandonner DEUX theses successives ; la N18 a ECARTE sa piste aeraulique
  (les 600 m³/h retranches a la reprise de la double flux pour compenser
  l'extraction permanente, une belle mecanique pourtant) parce que
  siege-rese-aigrefeuille publie « trois regimes d'air dans une meme
  enveloppe, chacun commande par ce qui l'exige ». La question n'est pas
  « est-ce que ca demontre bien ? » mais « est-ce que ca demontre quelque
  chose que le corpus ne demontre pas deja ? ».
- ⚠ LE SILENCE D'UNE PIECE EST UNE CONSIGNE (N17, N18). La synthese RT
  d'AP Yacht laisse la colonne « Gain en % » vide sur la ligne Tic : FT2E
  ne calcule pas de gain proportionnel sur une temperature. Celle
  d'Eiffage laisse la ligne Tic vide DANS SES TROIS COLONNES : aucune
  temperature interieure conventionnelle n'a ete publiee, ni au texte ni
  au dessin. Lire ce qu'une piece NE dit pas.
- ⚠ UN CCTP PEUT SE CONTREDIRE EN INTERNE (N11, N16, N18). Celui du lot 09
  d'Eiffage ecrit « regime du neutre : TN » au § 3.3.1 et « TT » aux
  § 3.4.2 et 3.5.2. RIEN N'A ETE PUBLIE. Retenir le paragraphe QUI
  DENOMBRE ou QUI RELEVE, l'ecrire dans a_valider_ft2e, en faire une
  question B - et ne PAS publier ce que la piece ne soutient pas.
- ⚠ UNE NOTE DE CALCUL PEUT NE PAS BOUCLER (N14, cinq fois en N16, une
  fois en N18 : « 160 kVA : 60 kVA pour l'ombriere et 60 kVA pour le
  batiment B » - 60 + 60 = 120). Ne JAMAIS composer un schema
  proportionnel (sankey, jauge, largeurs) sur des valeurs qui ne se
  ferment pas, et ne rien publier de ce qui ne boucle pas.
- ⚠ RECOMPTER LIGNE A LIGNE CE QU'ON ANNONCE (N15, N16, N17, N18). La N18
  a recompte les onze departs du TGBT (46 + 15 + 9 + 5 + 4 + 2 + 1,4 + 1
  + 1 + 1 + 1 = 86,4 kW exactement), recalcule les deux gains RT (ils
  bouclent a la decimale) et verifie la decomposition des honoraires
  (0,13 + 0,07 + 0,17 + 0,22 + 0,04 + 0,06 + 0,12 + 0,07 = 0,88, et
  19 500 x 0,88 = 17 160). CE QUI BOUCLE SE PUBLIE, CE QUI NE BOUCLE PAS
  S'ECARTE.
- ⚠ UN DOSSIER D'ARCHIVES PEUT CONTENIR LES PIECES D'UNE AUTRE AFFAIRE
  (N13). Lire la PAGE DE GARDE de CHAQUE piece technique avant d'en tirer
  une valeur. Les N14 a N18 ont rejoue ce controle et trouve des dossiers
  integres : le controle se fait, son resultat n'est pas acquis d'avance.
  Corollaire : une affaire peut n'avoir AUCUNE piece technique FT2E au
  dossier. La fiche reste publiable si trois familles de sources la
  soutiennent - programme du maitre d'ouvrage, comptes rendus de
  chantier, CV de l'equipe -, a condition que chacune soit NOMMEE en
  collecte et qu'aucune valeur de dimensionnement ne soit inventee.
- LES DOCX SECTORIELS DE references/docs_references/ PORTENT LA FICHE
  COMMERCIALE DE L'AFFAIRE (N18, decisif). « Ref. Social et Tertiaire.docx »
  donnait pour Eiffage le maitre d'ouvrage, l'architecte, le montant des
  travaux, la reference environnementale, la liste des missions, LES DEUX
  SURFACES (730 m² de bureaux, 810 m² d'atelier) et l'annee de
  realisation - tout ce que le frontmatter demande, en une entree. Les
  interroger SYSTEMATIQUEMENT au croisement commercial (etape 4), par
  zipfile + regex sur word/document.xml, en cherchant le nom de
  l'operation ET celui de la commune.
- LES CV DE L'EQUIPE SONT UNE SOURCE FT2E (livrables/cv-ft2e/CV-FT2E.zip,
  edition aout 2026, six CV en .docx). La N13 y a trouve le perimetre reel
  de la mission ; la N14 la mention SSI qui a ouvert une question B ; la
  N15 la reconciliation d'un conflit de millesime ; la N17 trois CV qui
  nomment l'affaire et ses lots. En N18 ils etaient MUETS sur l'affaire -
  c'est un resultat, pas un echec : le noter en collecte.
  ⚠ Un CV peut annoncer une mission que le CCTP dement (N14, N17). La
  piece contractuelle gagne, et l'ecart va en question B.
- LE COURRIEL FONDATEUR EST UNE PIECE (N18). Le .msg « Nouveau projet
  Eiffage » du 21/09/2020, lu par `extract_msg`, portait la singularite
  entiere de l'affaire en une phrase de l'architecte : « Les travaux
  plomberie et electricite devraient egalement etre realises par eux mais
  on aurait le suivi. » Ouvrir les .msg du repertoire commercial.
- annee_livraison se pose sur le classeur ; quand pieces et classeur se
  contredisent, le classeur est suivi ET la contradiction est ecrite en
  B1, jamais tranchee en silence. Le PV de reception manque presque
  toujours - mais il se cherche a SIX endroits : un CR d'OPC portant
  « RECEPTION DES TRAVAUX » en tete (N11) ; un CR annoncant la reception a
  une date precise avec le planning des semaines suivantes (N12) ; le
  BILAN DE FACTURATION, les honoraires d'AOR ne se facturant qu'une fois
  la mission finie (N12) ; le DERNIER CR DE CHANTIER, dont l'en-tete
  remplace « PROCHAINE REUNION » par « RECEPTION le JJ/MM/AAAA » (N13) ;
  LE CALENDRIER EN TETE DE CHAQUE CR D'OPC (N14) ; et L'EN-TETE DES
  DERNIERS CR (N15). ⚠ En N18, le dernier CR CONVOQUE les receptions des
  26 et 27 janvier 2023 sous le titre « RECEPTION & LEVEES DES RESERVES »
  sans les constater : convoquer n'est pas prononcer, et l'ecart va en
  question B. ⚠ L'indice des honoraires d'AOR NE JOUE PAS quand le BET ne
  porte pas l'AOR a la repartition (N14) - ni quand il la porte mais
  qu'aucun bilan de facturation n'est au dossier (N17, N18).
  ⚠ Sur une mission d'ETUDE SANS TRAVAUX (N16), il n'y a pas de reception
  du tout : la date qui fait foi est celle du DERNIER RAPPORT REMIS.
  ⚠⚠ LE DOSSIER DU JOUR EST CLASSE M : si c'est une etude, appliquer la
  regle N16.
- Le numero FT2E se releve sur page de garde CCTP (« Affaire n° : ... »),
  cartouche de plan (« Reference Affaire : ... »), etude thermique (pied
  ou EN-TETE de chaque page), contrats et propositions FT2E, EN PIED DE
  CHAQUE PAGE d'une note methodologique (N15), EN TETE DE CHAQUE PAGE
  d'un rapport d'audit (N16), et EN TETE DU CLASSEUR D'HONORAIRES INTERNE
  (N18, « N° : 20-071 » dans un .xls lu par xlrd).
  ⚠ Un meme bureau ecrit son numero de PLUSIEURS facons dans un meme
  dossier : « 21-074 », « 21074 » et « 21 074 A » cohabitent chez AP Yacht.
  ⚠ EN DERNIER RECOURS SEULEMENT, quand aucune piece FT2E n'existe au
  dossier (N13), il se releve sur le CLASSEUR + le nom du repertoire
  d'archives, et cela DOIT faire l'objet d'une question B.
- NOMMER LE CLIENT FINAL : un nom deja publie par FT2E (plaquette, corpus
  secteurs, docx sectoriels, classeur, CV) se reprend, avec E1 (N09
  Airbus, N10 CDAIR, N11 Undertech, N12 Central Hostel, N13 VoltAero, N14
  Fountaine Pajot, N15 Cabanes Urbaines, N16 ADEI, N17 AP Yacht / Catana,
  N18 Eiffage Energie Systemes - deja en ligne sur la fiche des ateliers
  pilotes Capsulae, ou le groupe est l'attributaire du lot electricite) ;
  un nom couvert par une clause de confidentialite reste hors slug et hors
  titre (N08 CPAM).
  ⚠ **Chercher aussi dans le CORPUS SECTEURS** : la N15 a decouvert qu'une
  PHOTOGRAPHIE de son affaire etait deja publiee sur
  /secteurs/coordination-ssi, et la N17 un cliche legende « Catana Group,
  Marans » - le grep de src/content/ doit couvrir les legendes et les alt
  des cliches, pas seulement la prose. Aucun nom de tiers ne monte jamais
  sur la planche.
  ⚠ CHERCHER AUSSI LES COTRAITANTS (N18) : Impact Urbanisme, EBLL et FT2E
  formaient deja le groupement de la passerelle du Carreau d'Or (24-034),
  quatre ans apres Eiffage. Une affaire dont un cotraitant est deja publie
  gagne un lien interne et une graphie deja arbitree.
- ⚠ UNE GRAPHIE PEUT ETRE FAUSSE PARTOUT SAUF DANS LES PIECES FT2E (N13,
  N17). Relever la graphie sur la page de garde d'un contrat ou d'un
  marche, retenir la majoritaire, ecrire la divergence en question B - et
  VERIFIER TOUJOURS si l'acteur est deja nomme dans src/content/projets/*.md
  avant d'ecrire `architecte` ou `moa`.
- ⚠ UN SITE PUBLIE PEUT PORTER UNE DATE OU UNE GRAPHIE FAUSSE (N15, N17).
  Corriger une page publiee est legitime quand une piece FT2E tranche,
  MAIS cela s'ecrit en question B et se signale au message final - jamais
  en silence.
- ⚠ L'AGENT DE RELECTURE TROUVE DES ERREURS DE FAIT SANS AVOIR LES PIECES
  (N15, N18). En N18 il a trouve SIX erreurs reelles que la redaction
  avait laissees passer : « quatre lots techniques » la ou l'operation en
  a deux (le quatre venait de `mission_ft2e`), « le meme trio » apres
  avoir enumere quatre cotraitants, « la deuxieme affaire du bureau a
  Saint-Jean-d'Angely » alors que 20-071 precede 21-098, un local serveur
  dit « monobloc » quand le CCTP lui donne une unite exterieure ET une
  unite interieure, des bureaux « du nord » quand la synthese RT ne parle
  que des facades est et ouest, et un acronyme (EER) jamais introduit.
  Traiter chaque question de compte comme une piste a verifier SUR LA
  PIECE, jamais comme une remarque de style ; et se relire soi-meme sur
  le critere « les items enumeres correspondent-ils au nombre annonce ? ».
  ⚠ Corollaire : lui donner en contexte les faits etablis sur piece (c'est
  ce qui lui permet de croiser), et lui demander EXPLICITEMENT les chaines
  exactes avant/apres - il travaille EN LECTURE SEULE, ses outils
  d'edition normalisent les insecables du depot.
  ⚠ ET LE VERIFIER : en N18 il s'est trompe une fois - il voulait retirer
  « consacree aux deux lots » d'un compte rendu intitule « REUNION
  FLUIDES », alors que la piece traite bien le lot 08 ET le lot 09 (chez
  FT2E, « fluides » inclut l'electricite). La correction retenue a garde
  le fait et pris le nom de la piece. Mesurer et verifier avant
  d'appliquer.
- Archetypes apres N18 : boucle-fluide 12 - coupe-traversee 7 -
  tableau-electrique 7 - sankey-energie 7 - zonage-ssi 6 -
  chronologie-affaire 2 - planche-chiffree 0 SANS module. L'archetype se
  choisit sur la THESE, jamais sur le secteur ni sur le quota, mais a
  these egale preferer ce qui n'a pas servi depuis longtemps ; la dette
  de variete porte toujours sur boucle-fluide (12/41), et
  chronologie-affaire n'a pas servi depuis le corpus fondateur
  (admissible seulement si sa these est d'INGENIERIE, jamais le
  calendrier d'une operation). ⚠ `planche-chiffree` n'a toujours pas de
  module : si un dossier l'exige, la decision est de L'ECRIRE ou de
  retirer l'archetype de la liste fermee (§ 1 du plan), jamais de
  bricoler. ⚠ UNE ECOLE CLASSEE M appelle peut-etre `zonage-ssi` (6/41)
  ou `tableau-electrique` (7/41) : les deux sont moins charges.
- Un mecanisme nouveau s'ecrit DANS le compositeur d'archetype
  (constantes prefixees par le mecanisme ; garde-fou de greffe sur le NOM
  DE LA FONCTION ET sur les prefixes de constantes - automatise depuis la
  N13 : en N18, 58 fonctions, 221 constantes dont 27 RP_ et 13 helpers du
  tronc reutilises, zero doublon), et l'invariant octet se rejoue AVANT
  la greffe, APRES la greffe et APRES la derniere retouche.
  ⚠ L'INSTRUMENT EXISTE AU DEPOT ET SE REJOUE SEUL, NE PAS LE REECRIRE :
  `python scripts/planches/invariant.py` couvre les 6 compositeurs et les
  41 dossiers (164/164 pieces au 2026-09-01),
  `python scripts/planches/invariant.py <archetype>` un seul.
  ⚠ Un dossier neuf dont la planche n'est pas encore composee fait ECHOUER
  l'invariant (FileNotFoundError, ou KeyError si son bloc d'archetype est
  inconnu du dispatch) : ce n'est pas une rupture, ce sont les pieces qui
  n'existent pas encore - LIRE LE DENOMINATEUR, qui dit combien de pieces
  preexistantes sont intactes. Composer d'abord, mesurer ensuite.
- ⚠ METTRE UNE ASSERTION DE DEPASSEMENT DANS LE COMPOSITEUR, ET SUR LES
  TROIS FORMATS (N14, rejouee en N15, N16, N17 et N18). Chaque chaine
  dessinee est mesuree par `mesurer()` contre la largeur interieure de son
  contenant, versee dans une liste, et un `assert not trop` rompt la
  composition avant tout rendu. En N18 : 28 chaines sur la planche, 0
  depassement, marge la plus faible 7,2 px ; l'assertion a effectivement
  ROMPU quatre fois avant d'etre satisfaite (quatre libelles trop longs
  sur la planche, puis quatre colonnes trop etroites sur l'appui) - c'est
  son travail.
- ⚠ LES TROIS FORMATS DOIVENT PARTAGER UNE SEULE IMPLANTATION DE LEUR
  PRIMITIVE (N17, applique d'emblee en N18). En N18, TROIS grandeurs sont
  DERIVEES et non choisies format par format : la hauteur d'un boitier
  vient de son nombre de departs, les deux terminaux nommes prennent le
  PREMIER et le DERNIER depart (jamais un rang choisi a la main), et le
  demi-tour se fait a 30 % de la largeur du boitier. Ecrire ces regles
  dans des fonctions partagees, et les publier dans `controles`.
- ⚠ LE BLOC `controles` REND COMPTE DU TRACE, PAS DE L'INTENTION (N17,
  regle dure 6 « mesurer, pas affirmer »). Ecrire dans `controles` ce qui
  est SORTI du compositeur.
- ⚠ NE PAS REECRIRE rendre_png.py : il est au depot depuis la N12, avec
  les deux pieges encodes (retrait de l'attribut style de racine par
  REGEX - sans quoi la vignette rend BLANCHE sans erreur - et fusion des
  filets a 8 chiffres). Usage :
  `python scripts/planches/rendre_png.py public/images/projets/<slug>
  <scratchpad>` ecrit planche.png 2400x1600 dans le dossier et, dans le
  scratchpad, les quatre controles (1152, vignette 274 et 296, appui
  552). REGARDER LES QUATRE. ⚠ Il s'appelle depuis la RACINE du depot.
  ⚠ Quand un detail est trop petit pour etre juge a l'oeil sur le PNG,
  NE PAS PLISSER LES YEUX : recadrer et agrandir par PIL (crop + resize
  NEAREST) et comparer les trois formats COTE A COTE - c'est ainsi que la
  N18 a verifie que ses trois dessins comptent bien 2 traits epais et 6
  traits fins sur un boitier a huit departs.
- ⚠ LE RENDU CAIROSVG N'A PAS LES POLICES DU SITE (N13, N14, N16, N18) :
  il retombe sur une police de substitution dont la chasse mono est ~7 a
  8 % plus large que celle d'IBM Plex Mono. Consequence : le dernier
  caractere du cartouche de legende parait COUPE sur le PNG de controle -
  ne PAS « corriger » la largeur du cartouche, la formule
  `mesurer(...) + 40` est commune aux 41 planches, et la capture du
  deploiement a 390 px confirme qu'il est entier (verifie en N18).
- ⚠ REGARDER LES PNG, ET CORRIGER CE QU'ON Y VOIT. La N16 a fait CINQ
  retouches, la N17 DEUX, la N18 TROIS - dont deux collisions qu'aucun
  controle automatique ne pouvait voir : une legende qui courait jusqu'au
  bord de la planche et passait SOUS une boite qui la tronquait, et un
  trajet epais qui traversait le libelle du bloc dans lequel il entrait.
  La seconde a impose de DISSOCIER les deux marges internes du bloc pour
  lui menager une bande de titre - une correction de GEOMETRIE, pas de
  texte.
  ⚠ Piege generique confirme en N13 a N18 : deux traits qui se croisent,
  ou un trait et un texte, doivent differer par autre chose que leur
  position - epaisseur, continuite, etiquette a fond papier, ou
  deplacement en zone franche. ⚠ Et un TIRET DE RAPPEL qui sort du bas
  d'un mot se lit comme un artefact, pas comme un repere : la N18 en a
  essaye un, l'a vu au PNG, et l'a supprime.
  ⚠ Et une LEGENDE DOIT TOUCHER CE QU'ELLE NOMME : posee au bout de la
  colonne, elle cesse de nommer.
- Quand aucune surface n'existe au dossier, la chercher dans les DOCX
  COMMERCIAUX (N12, N18) ; si elle n'y est pas non plus (N13), laisser
  `surface_m2` VIDE et porter au cartouche la grandeur qui compte
  l'ouvrage, avec question B. ⚠ Quand PLUSIEURS surfaces existent et
  divergent (N14, N17, N18), retenir celle qui designe EXPLICITEMENT
  l'objet de la fiche, ecrire les autres en a_valider_ft2e, et n'en
  publier qu'une seule en prose. En N18, QUATRE surfaces au dossier
  (1 544 m² de surface de plancher au panneau de chantier, 730 + 810 =
  1 540 m² au docx commercial, 859,1 m² de surface RT, 781 m² de surface
  utile) : la surface de plancher a ete retenue parce qu'elle designe
  l'ouvrage entier, et l'ecart de 4 m² est parti en question B.
- Les insecables des heredocs bash sont normalisees DE FACON NON
  DETERMINISTE sur cette machine. DEUX VOIES, toutes deux eprouvees :
  (a) ecrire le .md en ESPACES ORDINAIRES et apostrophes droites par
  l'outil Write, puis passer `python scripts/injection-typographique.py
  <fichier>` qui pose les insecables, les guillemets et les U+2019 -
  c'est la voie des N12 a N18, la plus sure ; (b) script Python avec
  marqueurs ASCII remplaces par chr(8239)/chr(160) et assertion A
  L'EGALITE comptee sur le source - la voie a suivre pour tout fichier que
  injection-typographique.py ne couvre pas (planche.json, fiche de
  collecte, plan du chantier, prompt de continuite).
  ⚠ injection-typographique.py protege les lignes d'enum du frontmatter
  (secteur, typologie, mission_ft2e) : une apostrophe DROITE tapee dans
  mission_ft2e y RESTE et casse le build - ecrire U+2019 des le script
  (piege N10, « Études d'exécution »). Il NE protege PAS
  secteur_secondaire.
  ⚠ Il ne connait pas toutes les unites : « A » (amperes) et le chiffre
  devant « × » lui ont echappe en N18, comme « T », « tonnes », « bars »,
  « dBA », « min », « s » et « h » aux sessions precedentes. CONTROLER PAR
  REGEX APRES PASSAGE : chercher `\d[ ](%|°C|m²|m³/h|kW|kVA|W|A|V|mm|
  dB\(A\)|lx|Pa|×)` doit rendre ZERO occurrence.
  ⚠ IL NE POSE PAS LES ACCENTS NI LES EXPOSANTS : ecrire « m² », « m³/h »
  et « °C » directement.
- ⚠ ECRIRE LES CHAINES COURBES *ET ACCENTUEES* DES L'ECRITURE - extraction
  planche.json COMPRISE. La recette, tenue en N11 a N18 : dans le script
  d'extraction lui-meme, avant ecriture, une assertion `"'" not in sortie`,
  une assertion `M not in sortie` sur chaque marqueur, et une assertion A
  L'EGALITE sur le COMPTE d'insecables - ce compte se LIT sur le source du
  script, jamais ecrit a la main. ⚠ Employer DEUX marqueurs distincts,
  « @ » pour la fine U+202F et « ^ » pour l'insecable U+00A0. Ne PAS
  prendre « # » (collision avec les titres Markdown).
  ⚠ La normalisation de Write porte sur les INSECABLES, pas sur les
  accents : ecrire les accents DIRECTEMENT dans le litteral. La N17 a
  ecrit son extraction entiere sans accents ; la N18 a fait la meme faute
  au premier jet et l'a rattrapee avant execution.
  ⚠ Poser un garde-fou d'accents, MAIS LE CALIBRER SUR UNE MESURE ET LE
  LIMITER A LA PROSE LUE : la prose francaise porte 2 a 6 % de caracteres
  accentues (mesure en N18 : 3,41 % sur l'extraction, 2,43 % sur la fiche
  de collecte). Ne jamais l'appliquer aux cles ni aux identifiants
  (`boucle-fluide`, `report`, `froid`), volontairement en ASCII.
  La passe `python scripts/apostrophes-planches.py` (sans argument, en
  MESURE) n'a alors rien a courber - 0 sur 0 en N14 a N18. Les
  apostrophes qu'elle REFUSE sont de la syntaxe de f-string : c'est le
  comportement voulu.
- ⚠ ALIGNER LES GRAPHIES SUR LE CORPUS, PAS SUR LA PIECE (N17, N18). La
  synthese RT d'AP Yacht ecrit « kWhep/m².an » et 38 fiches sur 39 ecrivent
  « kWhep/m²/an » ; en N18, la fiche ecrivait « gaz carbonique » quand 7
  fiches sur 9 ecrivent « dioxyde de carbone ». C'est le corpus qui gagne
  - ET LA CORRECTION DOIT ALLER AUSSI DANS L'EXTRACTION, sinon la fiche et
  sa planche affichent deux graphies differentes sur la meme page.
  Mesurer la graphie dominante par grep avant d'ecrire (idem pour le
  separateur du champ `performance` : « · » dans 34 fiches sur 42).
- ⚠ UNE CITATION SE TRANSCRIT TELLE QU'ELLE FIGURE (N18). La fiche
  ecrivait « reception et levees des reserves » la ou la piece porte
  « RECEPTION & LEVEES DES RESERVES » : remplacer l'esperluette a
  l'interieur de guillemets, c'est falsifier la piece. La bas-de-casse
  d'un titre en capitales est admise ; le changement d'un signe non.
- Les avances calibrees de _tronc.mesurer sous-mesurent Archivo 600 au
  rendu d'environ 20 % (N08-N09) - prendre la marge DANS LE CODE
  (`mesurer(...) * 1.2`), pas a l'oeil.
- ⚠ UN HEREDOC BASH PEUT MANGER UN ANTISLASH (N15, N16) ET ECHOUER SUR UNE
  APOSTROPHE (N17). Pour tout script non trivial : outil Write dans le
  SCRATCHPAD, puis execution. C'est aussi la regle qui evite que le hook
  Stop commite des scripts a usage unique.
  ⚠ ET NE JAMAIS TAPER UN CHEMIN D'ARCHIVES : les noms portent des
  accents et des apostrophes typographiques. Passer par os.walk +
  fragments de nom, qui est la seule methode fiable. La N18 a fabrique un
  petit module `lire.py` dans le scratchpad (trouver(*fragments) +
  texte(chemin, p0, p1) sur pymupdf) et l'a reutilise vingt fois : le
  motif se rejoue.
  ⚠ ATTENTION AUSSI AUX ANCRES D'INSERTION DANS LE PLAN : son titre
  « ## Annexe A — prompt d'initialisation... » porte une apostrophe
  DROITE. Ancrer sur U+2019 y echoue silencieusement. Et une ancre de
  texte prise dans un .md deja passe a injection-typographique.py peut
  contenir une INSECABLE INVISIBLE (piege rencontre en N18 sur
  « titre « reception... » ») : verifier par repr() avant de remplacer.
- Le hook Stop commite et pousse SEUL ce qui traine, et il PEUT
  COMMITTER LE LIVRABLE ENTIER sous l'intitule generique
  « chore(deploy): pousse l'etat de fin de session ». L'historique etant
  pousse sur un depot PARTAGE, il ne se reecrit pas. Pour l'eviter :
  garder les scripts a usage unique DANS LE SCRATCHPAD, hors depot
  (pratique des N13 a N18), COMMITTER TOT des que le build est vert, et
  reserver un second commit a la passe editoriale (⚠ livrables/ porte
  deux fichiers non suivis anterieurs a la N02 - les laisser).
- /references/ est gitignore (motif ancre) - les pieces sources
  n'entrent JAMAIS au depot ; npm run preview ne mesure pas la
  performance ; Chrome refuse les fenetres sous 500 px (sonde iframe).
- La planche n'expose NI le millesime d'ouverture, NI montant, NI tiers
  (MOA, mandataire, architecte, installateur, MARQUES comprises), NI
  donnee nominative ; les designations internes (reperes de zone,
  numeros de tableau, « AGBT », « ZDA01 ») sont admises avec une entree
  a_valider_ft2e et une question E ; tout arbitrage de dessin va dans
  a_valider_ft2e (jamais vide).

DEROULER LE PIPELINE § 2 INTEGRALEMENT : depouillement (pdfinfo /
pdftotext, ou pymupdf via python subprocess avec les noms lus par
os.listdir ; les plans sans couche texte et les marches scannes se
lisent en rendant leurs pages en PNG par pymupdf, zoom 2-3 ; antiword
pour les .doc, xlrd pour les .xls, openpyxl pour les .xlsx,
extract-msg pour les .msg) -> CONTROLE DE LA PAGE DE GARDE DE CHAQUE
PIECE TECHNIQUE -> releve du numero NN-NNN SUR PLUSIEURS PIECES FT2E, et
ETABLISSEMENT DE CE QUE DESIGNE CHAQUE AUTRE SUITE `NN-NNN` DU DOSSIER ->
references/ref_042/ (3 a 8 pieces) -> croisement commercial
(references/docs_references/ - docx sectoriels ET classeur ODS - +
docs/20-source-plaquette-2024.md + livrables/cv-ft2e/CV-FT2E.zip +
grep de src/content/ pour ce que le site publie deja, LEGENDES ET ALT
DES CLICHES COMPRIS) -> fiche de collecte (A/A+ remplies, B-E en
questions, ligne Secteur citant le classeur, DECISION Q3 motivee en
tete) -> LECTURE DES 41 SOUS-TITRES ET DES 41 `archetype_motif` pour
verifier qu'aucune these voisine n'est deja publiee -> fiche
src/content/projets/<slug>.md (SECTEUR RELEVE AU CLASSEUR ; taxonomie
ACTUELLE ; lieu avec code postal entre parentheses ; synthese 480-780 ;
>= 5 liens internes ; jamais de numero d'affaire NI de millesime
d'ouverture en prose ; convention numerale finale - nom du NOMBRE en un
seul mot en lettres, nombre COMPOSE en chiffres, unites et mesures
toujours en chiffres, citations intouchees ; verifier par
`python scripts/releve-numeral.py`, dont la section « Nombres COMPOSES
ecrits en lettres » doit rendre 0) -> PLANCHE complete (extraction avec
a_valider_ft2e non vide, apostrophes courbes ET ACCENTS des l'ecriture,
composition par scripts/planches/<archetype>.py avec assertion de
depassement SUR LES TROIS FORMATS et primitives PARTAGEES, rendus par
scripts/planches/rendre_png.py depuis la RACINE, controles a 1152 /
carte 274-296 / appui 552 - REGARDER les quatre PNG, et AGRANDIR par PIL
tout detail douteux -, apostrophes-planches.py en MESURE, invariant.py,
verser.py) -> qualite (typecheck 0, build vert 65 pages,
editorial-reviewer EN LECTURE SEULE - ses outils d'edition normalisent
les insecables, appliquer ses constats par script, ET VERIFIER CHACUN
SUR LA PIECE OU PAR MESURE -,
controle-liens-internes 42/42 a 5, controle-numeros-affaire 0 fuite,
releve-numeral sans ecart nouveau) -> COMMIT UNIQUE fiche+planche+
compositeur (content(references): ajoute la fiche reelle <nom> et sa
planche ; git ls-remote avant, depot partage) -> push (le push deploie),
curl de la fiche AVEC barre oblique finale + marqueur de build, rendu
controle aux trois bandes (sonde iframe pour les largeurs telephone :
references/ref_041/sonde-fiche.mjs, slug et URL a adapter) ET CONTROLE
DE L'INDEXATION SECTORIELLE (point 6, sonde
references/ref_041/sonde-filtres.mjs, appelee DEPUIS LA RACINE) ->
ligne de suivi au plan -> PROMPT DE LA SESSION N20 en annexe du plan
(script Python ou Write, jamais un long heredoc) et reproduit
integralement dans le message final.
Le prompt N20 REPREND le bloc « REGLE D'INDEXATION SECTORIELLE » tel quel
(repartition remise a jour) ET porte le PREMIER dossier de la tranche
2022 (quatre dossiers : 19087 Batiment SSLIA I, 20024 INNOVIA-GAELIC I,
20039 Videosurveillance CH Rochefort M, 22037 Audit chambre des metiers
M ; le ZIP 2022.zip est deja sur le disque). Il RAPPELLE aussi l'ecart
49 / 50 tant qu'il n'est pas tranche, ET la piste de la section
« Finalisees en 2021 » vide au classeur.

Portee de commit : content(references). Un changement de schema Zod
eventuel passe par le sous-agent content-modeller et va dans le MEME
commit que public/admin/config.yml.

Termine par le prompt de lancement de la session N20, en annexe du
plan du chantier et reproduit integralement dans ton message final -
la regle de continuite est dans CLAUDE.md parce qu'elle a ete manquee
deux fois.
```

## Annexe T — prompt de lancement de la session N20

```
Session N20/27 - FT2E v3 : chantier des 27 nouvelles fiches references.
VINGTIEME dossier - PREMIER de la tranche « Finalisees en 2022 ».

Contexte. FT2E v3 est le site institutionnel du bureau d'etudes FT2E
(La Rochelle), Astro 6 statique, deploye en demonstration client sur
https://ft2e-v3.vercel.app (indexation verrouillee - ne pas y toucher).
Le catalogue porte 42 fiches reelles (23 + N01 Portes-en-Re + N02 Fors +
N03 Aurora + N04 Loti + N05 Saint-Sauveur + N06 L'Houmeau + N07 Louise
Magnan + N08 bornes IRVE + N09 comptage Airbus + N10 foyer CDAIR +
N11 parc Undertech + N12 auberge Central Hostel + N13 batiment VoltAero +
N14 extension Fountaine Pajot + N15 Cabanes Urbaines + N16 audit ADEI +
N17 atelier AP Yacht + N18 siege Eiffage Energie + N19 chaufferie de
l'ecole de La Flotte), chacune illustree d'une planche de schema de
principe (cinq pieces par dossier). Objectif : 50 fiches.
1 session = 1 dossier, close par le prompt de la suivante.
LA TRANCHE 2023 EST CLOSE depuis la N19.

LE ZIP DE LA TRANCHE 2022 EST DEJA SUR LE DISQUE :
C:\claude_code_dev_projects\ft2e_new_archives\2022.zip (663,5 Mo, 846
entrees, racine interne « 2022/ », un repertoire par affaire). QUATRE
dossiers, tous absents du site (verifie au grep de
src/content/projets/*.md le 2026-09-01) :
-   586 fichiers, 659,8 Mo : « 22-037- Chambre des Metiers - Audit »
    (classeur M)  <- DOSSIER DU JOUR
-    67 fichiers,  39,3 Mo : « 19-087 - Batiment SSLIA - Cab SOURD »
    (classeur I)
-    61 fichiers,  36,8 Mo : « 20-024- INNOVIA  Projet GAELIC - Cab
    SOURD » (classeur I)
-    29 fichiers,  38,3 Mo : « 20-039- Centre Hospitalier Rochefort-
    Video surveillance » (classeur M)
IL N'Y A DONC AUCUNE QUESTION A POSER EN OUVERTURE : derouler directement,
en prenant le mieux documente d'abord (regle par defaut reconduite).

⚠⚠ ATTENTION DISQUE - C'EST LE PLUS GROS DOSSIER DU CHANTIER. 660 Mo
pour 3,3 Go libres. Supprimer d'abord le repertoire extrait de la session
precedente - C:\claude_code_dev_projects\ft2e_new_archives\2023 (le
REPERTOIRE, pas le ZIP ; il contient 2023/21-029 - Ecole primaire...) -
par python shutil.rmtree (le rm -rf est REFUSE par les permissions).
La cartographie du dossier du jour, mesuree AU ZIP sans extraction :
-   577 fichiers / 657,2 Mo dans 02-Production/02-Audit - Diagnostic
-   9 pieces dans 01-Commerciale (trois indices de contrat d'honoraire
    A / B / nu, un devis signe, un previsionnel d'heures)
-   1 fichier 02-Production/19xxx-SUIVI.doc  <- ⚠ un nom de fichier qui
    porte « 19xxx » dans un dossier 22-037 : etablir ce qu'il designe
Extensions : 402 PDF, 101 JPG, 17 XLSX, 16 PNG, 12 DOCX, 6 JPEG, 4 XLSM,
4 XLS. Ce n'est donc PAS un dossier de photographies : les PDF dominent.
SI LA PLACE MANQUE, l'extraction se filtre par sous-repertoire
(zipfile.namelist() + un fragment de chemin) plutot que d'echouer a
mi-course : commencer par 01-Commerciale, puis les PDF de
02-Audit - Diagnostic, en laissant les JPG au ZIP.

⚠ NE JAMAIS conclure « mince » ni « riche » sur le seul compte de fichiers :
quatre dementis en N08-N09 (mince qui etait riche), un dementi INVERSE en
N13 (« 21-095 » annoncait 72 fichiers dont 17 appartenaient a l'affaire
21-093), et six dossiers integres en N14 a N19. C'est la PAGE DE GARDE qui
dit a quelle affaire une piece appartient, jamais le repertoire qui la
contient - ⚠ ET LA PAGE DE GARDE ELLE-MEME PEUT MENTIR (voir ci-dessous).

⚠ CE QUI RESTE APRES 2022, ET L'ECART 49 / 50 TOUJOURS NON TRANCHE. Le
classeur ODS porte, apres la tranche 2022 : « Finalisees en 2020 » (2 :
19008 Batiment industriel Aeroport LR ELIXIR I, 20058 Diag legionelles du
port de plaisance M) et « Finalisees en 2019 » (1 : 18026 Atelier
numerique Fountaine Pajot I). Soit 4 (2022) + 2 + 1 = 7 dossiers restants
pour 42 fiches en ligne : LE CLASSEUR NE MENE QU'A 49, PAS A 50. La
question a ete portee aux messages finaux des N16, N17, N18 et N19 et
N'A TOUJOURS PAS ETE ARBITREE PAR FT2E : la reposer tant qu'elle reste
ouverte. Ne pas fabriquer une fiche pour combler l'ecart.
⚠ PISTE RELEVEE EN N17, TOUJOURS OUVERTE : le classeur porte une section
« Finalisees en 2021 » qui est VIDE. C'est le seul millesime sans aucune
entree, entre 2020 (2 entrees) et 2022 (4 entrees). L'hypothese a soumettre
a FT2E est qu'une affaire manque a cette section - ce qui expliquerait
l'ecart exactement. A verifier avec eux, pas a supposer.
Le ZIP 2019.zip EST DEJA SUR LE DISQUE ; celui de la tranche 2020 devra
etre demande en ouverture de la session qui closera 2022.

LIRE D'ABORD, dans cet ordre :
1. docs/superpowers/plans/2026-08-27-chantier-27-nouvelles-fiches.md -
   LE PLAN : § 1 (ce qui a change), § 2 (pipeline 12 etapes), § 3
   (reponses consignees Q1/Q2 2024 + complement N02 : le classeur fait
   foi ; Q3 = regle des dossiers minces, defaut reconduit), § Suivi
   (lignes N01 a N19), annexe T (ce prompt).
2. docs/superpowers/plans/2026-08-07-chantier-references-reelles.md -
   § Contraintes globales + § Protocole de session + § Regle des
   dossiers minces.
3. docs/superpowers/specs/2026-08-12-planches-references-protocole.md -
   revision 5 EN ENTIER.
4. CLAUDE.md, .claude/rules/content-collections.md et french-editorial.md.
Etalons : src/content/projets/creche-oranger-perigny.md (fiche) et, pour
une affaire MONOTECHNIQUE - AUDIT, les CINQ fiches du secteur M -
audit-chauffage-sites-adei.md (sept sites medico-sociaux, le plus proche
d'une mission d'audit pur), chaufferie-ecole-la-flotte-en-re.md (N19),
bornes-irve-la-rochelle-saintes.md, cuisine-groupe-scolaire-villedoux.md
(un audit energetique communal, sans travaux : le plus proche du dossier
du jour) et atelier-dufour-yachts-perigny.md.
Voir aussi src/content/projets/chaufferie-ecole-la-flotte-en-re.md +
public/images/projets/chaufferie-ecole-la-flotte-en-re/ +
references/ref_042/ (fiche de collecte N19, avec sa DECISION Q3 en tete -
c'est elle qui documente le FAUX NUMERO EN PAGE DE GARDE DE CCTP, les
DEUX PIECES DE TIERS trouvees au dossier, et les cinq indices de contrat
d'une seule affaire).
Les sondes de recette vivent dans references/ref_042/ (sonde-fiche.mjs ET
sonde-filtres.mjs, toutes deux adaptees en N19 - la sonde de filtres est
desormais recalee sur le secteur « Monotechnique - Audit ») : URL, slug et
secteur a adapter. La sonde de filtres s'appelle DEPUIS LA RACINE du depot.

REGLE D'INDEXATION SECTORIELLE - etablie le 2026-08-27, A APPLIQUER A
LA REDACTION DE CHAQUE FICHE (etape 6 du pipeline), pas apres coup :
« REFERENCES SITE FT2E.ods » (references/docs_references/, classeur
fourni par FT2E) FAIT FOI pour le classement sectoriel. Concretement,
AVANT d'ecrire le frontmatter :
1. Ouvrir le classeur (python zipfile sur content.xml, ou pandoc) et y
   retrouver l'affaire PAR SON NUMERO (graphie sans tiret : « 22037 »).
2. En relever le domaine (legende : L Logements / T Tertiaire & ERP /
   I Industriel / P Patrimoine / C Coordination SSI /
   M Monotechnique-Audit / E EXE) -> champ `secteur`.
3. Si le classeur porte un domaine DOUBLE (« T § C ») : le premier est
   le `secteur`, le second va au champ `secteur_secondaire` (optionnel
   au schema depuis le 2026-08-27, garde-fou « doit differer ») - la
   fiche parait alors dans les deux filtres et sur les deux pages de
   secteur. Precedents : hotel-yachtman (T § C), maison-pierre-loti-
   rochefort (P § C, N04), foyer-cdair-saint-martin-de-re (T § C, N10),
   auberge-central-hostel-la-rochelle (T § C, N12),
   cabanes-urbaines-la-rochelle (T § C, N15).
   LE DOSSIER DU JOUR EST A DOMAINE SIMPLE : 22037 est « M ».
4. JAMAIS de deduction depuis le dossier, l'usage RT ou le nom de
   l'operation : la N02 penchait « Industriel » pour Fors, le classeur
   dit T - et les 25 fiches ont du etre re-referencees le soir meme
   (7 bascules, commits ce334b2/09270a3). Le classeur peut contredire
   l'intuition (Saint-Rogatien, pole commercial : I ; Fors, pole
   commercial : T ; 23083 « plan de comptage Airbus » : E et non M ;
   23099 « CPAM » : M - IRVE, pas T ; 23036 Fountaine Pajot : I SIMPLE
   alors que le CV annonce « CFO / CFA / SSI » ; 20045 « THE ROOF »,
   salle d'escalade et atelier de luthier : T § C et non I ; 21086
   « Audit chauffage sites ADEI », sept etablissements medico-sociaux :
   M SIMPLE ; 21074 « AP Yacht - CATANA Group », chantier naval : I
   SIMPLE ; 20071 « Bureaux EIFFAGE », un siege d'agence avec ses
   ateliers : T SIMPLE ; 21029 « Ecole primaire et maternelle La
   Flotte », un ERP de type R : M SIMPLE, et le depouillement de la N19
   a donne raison au classeur - FT2E n'y tenait qu'UN SEUL LOT
   technique, le chauffage, decline en cinq missions sur trois ans) -
   il gagne.
   ⚠ ATTENTION PARTICULIERE ICI : « Chambre des Metiers » evoque un
   siege tertiaire, et l'intuition dira « Tertiaire / ERP ». LE CLASSEUR
   DIT M, et le nom du dossier porte « - Audit ». Une chambre des
   metiers classee M signifie tres probablement une MISSION D'ETUDE SANS
   TRAVAUX : la typologie `Etude` existe au schema pour cela (quatre
   fiches l'emploient), et cuisine-groupe-scolaire-villedoux.md en est
   l'etalon le plus proche. Le depouillement doit ETABLIR s'il y a eu
   des travaux, et ne pas l'annoncer si le dossier ne les porte pas.
5. CONSIGNER la lecture dans la fiche de collecte (ligne « Secteur » :
   citer l'entree du classeur telle quelle) ; si l'affaire est ABSENTE
   du classeur ou son domaine illisible -> question B a FT2E et choix
   provisoire argumente, jamais silencieux.
6. EN RECETTE (etape 10) : verifier sur le deploiement que la fiche
   repond au bon filtre de /references (compteurs de chips) et parait
   sur sa page /secteurs/<slug> - sondes : references/ref_042/
   sonde-filtres.mjs et references/ref_042/sonde-fiche.mjs (URL a adapter).
   ⚠ Une page /secteurs/<slug> n'affiche que les 4 affaires les plus
   recentes du secteur (tri par numero decroissant) ; le filtre de
   /references, lui, montre tout. Une affaire a DOUBLE domaine doit
   etre controlee sur LES DEUX filtres et LES DEUX pages de secteur.
   ⚠ 22-037 est un numero de 2022 et le secteur « Monotechnique - Audit »
   compte desormais 5 fiches, dont les numeros sont 25-080 (Dufour),
   25-010 (Villedoux), 23-099 (IRVE), 21-086 (ADEI) et 21-029 (La
   Flotte). 22-037 s'inserera QUATRIEME et entrera donc dans le top 4
   de /secteurs/monotechnique, en en chassant 21-086 : c'est le tri
   documente, PAS un defaut, et le filtre de /references fait foi.
   Repartition attendue AVANT la N20, mesuree le 2026-09-01 sur le
   deploiement par references/ref_042/sonde-filtres.mjs : L10 T14 I5 P3
   C7 M5 E3 pour 42 fiches, 47 en pondere (Yachtman T+C, Loti P+C, foyer
   CDAIR T+C, Central Hostel T+C et Cabanes Urbaines T+C comptent double).

DOSSIER DU JOUR : « 22-037- Chambre des Metiers - Audit » (586 fichiers,
659,8 Mo), classeur « 22037 · Chambre des metiers · M ». C'est le premier
dossier de la tranche 2022, et le plus volumineux du chantier.
Points d'attention connus AVANT ouverture :
(a) ⚠ LE CLASSEUR DIT M, ET LE NOM DU DOSSIER DIT « Audit ». Etablir au
    depouillement s'il y a eu des TRAVAUX : s'il n'y en a pas,
    `typologie: Etude`, pas de `annee_livraison` de reception mais la
    date du DERNIER RAPPORT REMIS (regle N16, rejouee en N19), et le
    cartouche porte la grandeur qui compte l'ouvrage ;
(b) 577 fichiers dans un seul sous-repertoire d'audit : ce sera un
    depouillement de VOLUME. Commencer par 01-Commerciale (9 pieces, dont
    trois indices de contrat) pour etablir le PERIMETRE de la mission,
    puis n'ouvrir du repertoire d'audit que ce que ce perimetre designe.
    ⚠ Un dossier d'audit a fort volume porte souvent UN RAPPORT PAR
    BATIMENT ou PAR SITE : etablir le nombre de sites AVANT de compter
    quoi que ce soit, et se souvenir que la N16 a trouve CINQ rapports
    remis sur SEPT sites sous contrat ;
(c) ⚠ « Chambre des Metiers » est une raison sociale de tiers. Verifier
    si elle est DEJA PUBLIEE par FT2E (docx sectoriels, classeur,
    plaquette, CV, corpus secteurs - LEGENDES ET ALT DES CLICHES
    COMPRIS) avant de la nommer, et relever sa graphie exacte sur une
    piece contractuelle ;
(d) ⚠ le fichier « 02-Production/19xxx-SUIVI.doc » porte « 19xxx » dans
    un dossier 22-037. Etablir ce qu'il designe AVANT d'en tirer quoi
    que ce soit - et relever tout `\d{2}[-\s]\d{3}` du dossier ;
(e) ⚠ une note ou un rapport peut ne pas boucler. La N16 en a releve
    CINQ dans un seul dossier ; la N18 une ; la N19 une (« budget global
    220 000 € HT » avec une ligne chauffage a 240 000 €, ecartee).
    Verifier que les sous-totaux somment AVANT de composer quoi que ce
    soit de proportionnel.
Aucun numero 22-037 n'est publie (verifie au grep de
src/content/projets/*.md le 2026-09-01).
Dossier de travail a creer : references/ref_043/
Slug cible : a etablir au depouillement (kebab-case sans accents,
verifier qu'il n'ecrase rien).

CE QUE LES N01-N19 ONT ETABLI (verifiable au depot) :
- ⚠⚠ LA PAGE DE GARDE D'UN CCTP FT2E PEUT PORTER UN FAUX NUMERO - deux
  fois de suite, en N18 et en N19, et c'est desormais le piege le plus
  regulier du chantier. Chez Eiffage, le CCTP du lot 09 portait
  « Affaire n° : 20-012 » quand tout le reste portait 20-071. A La Flotte,
  le CCTP portait « Affaire n° : 21-031 » quand DIX-NEUF autres
  occurrences - les cartouches des deux plans, cinq contrats, le classeur
  d'honoraires interne, et les en-tetes des pages courantes DU MEME CCTP -
  portaient 21-029, seul numero connu du classeur FT2E. RELEVER LE NUMERO
  SUR PLUSIEURS PIECES ET RETENIR LA MAJORITE ; les pieces les plus sures
  sont les CARTOUCHES DE PLANS et le CLASSEUR D'HONORAIRES INTERNE, qui
  sont des pieces de production et non des documents recopies d'un modele.
  Les autres faux numeros deja rencontres : references de MODELE du
  constructeur (« ULTI+ 21-095 », N17), numeros de dossier des mandataires
  (BF ECO « 534 », N17 ; SEMDAS « 2507 », ARCHITEM « 1821 », N10), numeros
  de permis (N18), surfaces foncieres (N18), codes postaux, et surtout
  NUMEROS DE NORMES - la N19 en a trouve trois qui ressemblaient a des
  affaires : NF X 46-020 (reperage amiante), NF S 31-010 (mesurage des
  bruits), NF C 15-100. Relever tout `\d{2}[-\s]\d{3}` du dossier et
  etablir, un par un, ce que chacun designe AVANT d'en publier aucun.
- ⚠ UNE PIECE DU DOSSIER PEUT APPARTENIR A UN AUTRE BUREAU (N19, NOUVEAU).
  Le fichier « FTi_D20210037 RTex_FAISA_MAIRIE LA FLOTTE EN RE.pdf »
  ressemblait a une etude thermique FT2E : c'etait le DEVIS CONCURRENT
  d'un autre bureau, depose au dossier pour comparaison. Ni son nom ni son
  montant ne se publient. Le nom de fichier trompe ; c'est l'EN-TETE -
  raison sociale, SIRET, RIB - qui tranche.
- ⚠ UNE PIECE PEUT ETRE COMMANDEE PAR UN TIERS A UN TIERS (N19, NOUVEAU).
  Une etude d'impact sonore des deux PAC, un an apres la fin des travaux,
  commandee ET PAYEE par l'installateur - hors de toute mission FT2E
  figurant au dossier. Elle raconte une suite reelle de l'affaire, mais la
  publier reviendrait soit a attribuer a FT2E le travail d'un tiers, soit
  a publier un desordre d'une installation que le bureau a concue. RIEN
  n'en a ete ecrit dans la fiche ; tout est en question E a FT2E.
  Trois regimes de propriete d'une piece, a distinguer AVANT d'ecrire :
  piece FT2E (fonde la fiche), piece d'un tiers deposee pour comparaison
  (ne se cite jamais), piece d'un tiers commandee par un tiers (question).
- ⚠ LE SITE PUBLIE PEUT-ETRE DEJA UN CLICHE DE L'AFFAIRE - troisieme
  occurrence (N15, N17, N19). En N19, /secteurs/monotechnique portait une
  photographie legendee « PAC, groupe scolaire de La Flotte » (creditee
  © FT2E) ET une mention en prose SANS LIEN, faute de fiche. Le grep de
  src/content/ doit couvrir les LEGENDES et les ALT des cliches, pas
  seulement la prose. Deux benefices en N19 : le site a fourni la GRAPHIE
  de la commune (« La Flotte-en-Re »), et la mention en prose est devenue
  un lien - une amelioration legitime, A SIGNALER AU MESSAGE FINAL.
- ⚠ UN INDICE DE CONTRAT N'EST PAS UNE AFFAIRE - confirme QUATRE fois
  (N15 : 20-045 / 20 045 A / 20-045-CSSI ; N16 : 21 086 A a H, HUIT
  contrats pour SEPT sites ; N17 : 21 074 A pour l'APS et 21 074 nu pour
  l'audit ; N19 : CINQ contrats sur trois ans - 21 029 nu pour la
  faisabilite, A pour la maitrise d'oeuvre, B pour la gestion
  administrative, C pour les etudes d'execution vendues a l'INSTALLATEUR,
  et un SECOND C pour l'audit thermique vendu a la commune). Le depart se
  fait sur les pieces de PRODUCTION, qui portent le numero SANS indice, et
  le classeur ne connait qu'une entree. Ne jamais decouper une affaire sur
  ses contrats - ⚠ ni s'etonner que deux contrats portent le meme indice.
- ⚠ UN COMPTE DE FICHIERS N'EST PAS UN COMPTE DE CHOSES (N17, N18) - MAIS
  IL PEUT L'ETRE, ET ALORS IL SE PUBLIE (N19). Chez AP Yacht, 45 comptes
  rendus numerotes de 1 a 47 : la fiche publie 47. Chez Eiffage, 46 fichiers
  numerotes 1 a 45 puis 49 : LA FICHE NE PUBLIE AUCUN COMPTE. A La Flotte,
  NEUF fichiers numerotes 1 a 9 sans trou, ET le calcul d'honoraires
  budgetait exactement neuf reunions au poste DET : les deux sources
  concordent, la fiche publie neuf. Recompter, puis chercher une SECONDE
  source ; s'abstenir reste legitime quand rien ne tranche.
- ⚠ LE MAITRE D'OUVRAGE N'EST PAS TOUJOURS L'OCCUPANT, NI LA MEME RAISON
  SOCIALE D'UNE PIECE A L'AUTRE (N16, N17, N18, N19). A La Flotte, trois
  graphies : « COMMUNE DE LA FLOTTE » (acte d'engagement, la piece de
  marche, avec le SIRET), « Commune de la Flotte en Re » (contrats FT2E),
  « Commune de La Flotte-en-Re » (docx sectoriels, CV, et le site). C'est
  la graphie DEJA PUBLIEE qui a ete retenue, et la divergence est en
  question B.
- ⚠ UNE THESE PEUT ETRE DEJA PUBLIEE - et c'est le risque PRINCIPAL, avec
  42 planches au corpus. AVANT d'arreter une these, lire les `sous_titre`
  ET les `archetype_motif` des 42 planches (PYTHONIOENCODING=utf-8 python
  -c "..." sur public/images/projets/*/planche.json). La N17 a du
  abandonner DEUX theses successives ; la N18 a ECARTE sa piste aeraulique ;
  la N19 a ecarte TROIS lectures pourtant justes - « la PAC haute
  temperature pour garder les emetteurs » (publie par l'audit ADEI), « la
  cascade sur ballon avec departs comptes » (publie par le foyer de
  Saint-Martin-de-Re), et « l'amont reserve pour plus » (publie par les
  bornes IRVE). La question n'est pas « est-ce que ca demontre bien ? »
  mais « est-ce que ca demontre quelque chose que le corpus ne demontre
  pas deja ? ».
- ⚠ LE SILENCE D'UNE PIECE EST UNE CONSIGNE (N17, N18). Lire ce qu'une
  piece NE dit pas : une colonne laissee vide, une ligne sans valeur, un
  champ de cartouche a « XX » (en N19, le champ « Architecte » des deux
  plans - il n'y avait aucun architecte sur l'operation, et la fiche n'en
  nomme donc aucun).
- ⚠ UN CCTP PEUT SE CONTREDIRE EN INTERNE (N11, N16, N18) ET CONTREDIRE
  SES PROPRES PLANS (N19 : « regime 60/55 » au CCTP et a l'echangeur,
  « 60/50 » au plan de masse ; « 76,5 kW » au CCTP, « 75 kW unitaire » a
  la DPGF). Retenir la PIECE CONTRACTUELLE, l'ecrire dans a_valider_ft2e,
  en faire une question B - et ne PAS publier ce que la piece ne soutient
  pas.
- ⚠ UNE NOTE DE CALCUL PEUT NE PAS BOUCLER (N14, cinq fois en N16, une
  fois en N18, une fois en N19). Ne JAMAIS composer un schema
  proportionnel (sankey, jauge, largeurs) sur des valeurs qui ne se
  ferment pas, et ne rien publier de ce qui ne boucle pas.
- ⚠ RECOMPTER LIGNE A LIGNE CE QU'ON ANNONCE (N15 a N19). La N19 a
  recalcule la decomposition des honoraires de maitrise d'oeuvre
  (6 900 + 1 500 + 1 100 + 3 300 + 1 100 = 13 900 exactement, TVA et TTC
  compris), la puissance electrique cible (4 x 49 = 196, plus les
  auxiliaires = 200 kVA) et la puissance installee (2 x 76,5 = 153 kW).
  CE QUI BOUCLE SE PUBLIE, CE QUI NE BOUCLE PAS S'ECARTE.
- ⚠ UN DOSSIER D'ARCHIVES PEUT CONTENIR LES PIECES D'UNE AUTRE AFFAIRE
  (N13). Lire la PAGE DE GARDE de CHAQUE piece technique avant d'en tirer
  une valeur. Les N14 a N19 ont rejoue ce controle et trouve des dossiers
  integres : le controle se fait, son resultat n'est pas acquis d'avance.
- LES DOCX SECTORIELS DE references/docs_references/ PORTENT LA FICHE
  COMMERCIALE DE L'AFFAIRE (N18, decisif) - MAIS PAS TOUJOURS (N19 : les
  onze docx sont MUETS sur l'ecole de La Flotte, y compris celui « Petite
  enfance - scolaire » qui serait sa place). C'est un resultat a consigner,
  pas un echec : en N19 il explique l'absence de surface au dossier. Les
  interroger SYSTEMATIQUEMENT au croisement commercial (etape 4), par
  zipfile + regex sur word/document.xml, en cherchant le nom de
  l'operation ET celui de la commune - la N19 y a ainsi decouvert SEPT
  AUTRES affaires FT2E sur la meme commune, dont un batiment pour lequel
  un regard de vannes avait ete reserve trois ans plus tot.
- LES CV DE L'EQUIPE SONT UNE SOURCE FT2E (livrables/cv-ft2e/CV-FT2E.zip,
  edition aout 2026, six CV en .docx). En N19, un seul CV nommait
  l'affaire, et il la datait et la restreignait AUTREMENT que le contrat
  (« 2024 · ECOLE PRIMAIRE · audit energetique format ADEME » contre un
  contrat de 2023 portant sur le GROUPE SCOLAIRE). La piece contractuelle
  gagne, et l'ecart va en question B.
- LE COURRIEL FONDATEUR EST UNE PIECE (N18, N19). En N19, le .msg du
  01-Commerciale, lu par `extract_msg`, portait l'origine entiere de
  l'affaire : l'architecte relayant la demande du directeur des services
  techniques de la commune. Ouvrir les .msg du repertoire commercial.
- annee_livraison se pose sur le classeur ; quand pieces et classeur se
  contredisent, le classeur est suivi ET la contradiction est ecrite en
  B1, jamais tranchee en silence. Le PV de reception manque presque
  toujours - mais il se cherche a SIX endroits : un CR d'OPC portant
  « RECEPTION DES TRAVAUX » en tete (N11) ; un CR annoncant la reception a
  une date precise (N12) ; le BILAN DE FACTURATION (N12) ; le DERNIER CR
  DE CHANTIER, dont l'en-tete remplace « PROCHAINE REUNION » par
  « RECEPTION le JJ/MM/AAAA » (N13) ; LE CALENDRIER EN TETE DE CHAQUE CR
  D'OPC (N14) ; et L'EN-TETE DES DERNIERS CR (N15).
  ⚠ En N18 le dernier CR CONVOQUE des receptions sans les constater ; en
  N19 il constate « travaux termines » et trois reserves, et fixe une
  levee « date a confirmer ». Constater n'est pas prononcer, et l'ecart
  va en question B.
  ⚠⚠ SUR UNE MISSION D'ETUDE SANS TRAVAUX (N16), IL N'Y A PAS DE
  RECEPTION DU TOUT : la date qui fait foi est celle du DERNIER RAPPORT
  REMIS. LE DOSSIER DU JOUR EST UN AUDIT : cette regle a toute chance de
  s'appliquer.
- Le numero FT2E se releve sur page de garde CCTP (⚠ mais voir le premier
  point), cartouche de plan (« Reference Affaire : ... »), etude thermique,
  contrats et propositions FT2E, EN PIED DE CHAQUE PAGE d'une note
  methodologique (N15), EN TETE DE CHAQUE PAGE d'un rapport d'audit (N16),
  et EN TETE DU CLASSEUR D'HONORAIRES INTERNE (N18 en .xls lu par xlrd,
  N19 idem - « N° : 21-029 »).
  ⚠ Un meme bureau ecrit son numero de PLUSIEURS facons dans un meme
  dossier : « 21-029 », « 21 029 » et « 21 029 A » cohabitent a La Flotte.
- NOMMER LE CLIENT FINAL : un nom deja publie par FT2E (plaquette, corpus
  secteurs, docx sectoriels, classeur, CV) se reprend, avec E1 ; un nom
  couvert par une clause de confidentialite reste hors slug et hors titre
  (N08 CPAM).
  ⚠ **Chercher aussi dans le CORPUS SECTEURS** : la N15 a decouvert qu'une
  PHOTOGRAPHIE de son affaire etait deja publiee, la N17 un cliche legende
  « Catana Group, Marans », la N19 un cliche legende « PAC, groupe
  scolaire de La Flotte ». Aucun nom de tiers ne monte jamais sur la
  planche.
  ⚠ CHERCHER AUSSI LES COTRAITANTS ET LES CONFRERES (N18, N19).
- ⚠ UNE GRAPHIE PEUT ETRE FAUSSE PARTOUT SAUF DANS LES PIECES FT2E (N13,
  N17). Relever la graphie sur la page de garde d'un contrat ou d'un
  marche, retenir la majoritaire, ecrire la divergence en question B - et
  VERIFIER TOUJOURS si l'acteur est deja nomme dans src/content/projets/*.md
  avant d'ecrire `architecte` ou `moa`.
- ⚠ UN SITE PUBLIE PEUT PORTER UNE DATE OU UNE GRAPHIE FAUSSE (N15, N17).
  Corriger une page publiee est legitime quand une piece FT2E tranche,
  MAIS cela s'ecrit en question B et se signale au message final - jamais
  en silence. Idem pour l'AJOUT d'un lien vers la fiche neuve depuis une
  page de secteur qui la mentionnait deja en prose (N19).
- ⚠ L'AGENT DE RELECTURE TROUVE DES ERREURS DE FAIT SANS AVOIR LES PIECES
  (N15, N18). Traiter chaque question de compte comme une piste a verifier
  SUR LA PIECE, jamais comme une remarque de style ; et se relire soi-meme
  sur le critere « les items enumeres correspondent-ils au nombre
  annonce ? ». ⚠ Corollaire : lui donner en contexte les faits etablis sur
  piece, et lui demander EXPLICITEMENT les chaines exactes avant/apres -
  il travaille EN LECTURE SEULE, ses outils d'edition normalisent les
  insecables du depot. ⚠ ET LE VERIFIER : en N18 il s'est trompe une fois.
  Mesurer et verifier avant d'appliquer.
- Archetypes apres N19 : boucle-fluide 12 - coupe-traversee 8 -
  tableau-electrique 7 - sankey-energie 7 - zonage-ssi 6 -
  chronologie-affaire 2 - planche-chiffree 0 SANS module. L'archetype se
  choisit sur la THESE, jamais sur le secteur ni sur le quota, mais a
  these egale preferer ce qui n'a pas servi depuis longtemps ; la dette
  de variete porte toujours sur boucle-fluide (12/42), et
  chronologie-affaire n'a pas servi depuis le corpus fondateur
  (admissible seulement si sa these est d'INGENIERIE, jamais le
  calendrier d'une operation - la N19 a ecarte pour ce motif les huit
  mois d'attente du distributeur, pourtant le fait le plus saillant de
  son chantier). ⚠ `planche-chiffree` n'a toujours pas de module : si un
  dossier l'exige, la decision est de L'ECRIRE ou de retirer l'archetype
  de la liste fermee (§ 1 du plan), jamais de bricoler.
  ⚠ UN AUDIT SANS TRAVAUX appelle plutot `sankey-energie` (7/42, une
  proportion qui se ferme) ou `zonage-ssi` (6/42, un decoupage) : les deux
  sont moins charges que boucle-fluide.
- Un mecanisme nouveau s'ecrit DANS le compositeur d'archetype
  (constantes prefixees par le mecanisme ; garde-fou de greffe sur le NOM
  DE LA FONCTION ET sur les prefixes de constantes - automatise depuis la
  N13 : en N19, 43 fonctions et 139 constantes existantes contre 7 et 14
  nouvelles, prefixe unique `AM_`, zero collision), et l'invariant octet
  se rejoue AVANT la greffe, APRES la greffe et APRES la derniere retouche.
  ⚠ L'INSTRUMENT EXISTE AU DEPOT ET SE REJOUE SEUL, NE PAS LE REECRIRE :
  `python scripts/planches/invariant.py` couvre les 6 compositeurs et les
  42 dossiers (168/168 pieces au 2026-09-01),
  `python scripts/planches/invariant.py <archetype>` un seul.
  ⚠ Un dossier neuf dont la planche n'est pas encore composee fait ECHOUER
  l'invariant (KeyError si son bloc d'archetype est inconnu du dispatch) :
  ce n'est pas une rupture, ce sont les pieces qui n'existent pas encore -
  LIRE LE DENOMINATEUR, qui dit combien de pieces preexistantes sont
  intactes (164/168 avant la greffe en N19, 168/168 apres). Composer
  d'abord, mesurer ensuite.
- ⚠ METTRE UNE ASSERTION DE DEPASSEMENT DANS LE COMPOSITEUR, ET SUR LES
  TROIS FORMATS (N14, rejouee en N15 a N19). Chaque chaine dessinee est
  mesuree par `mesurer()` contre la largeur interieure de son contenant,
  versee dans une liste, et un `assert not trop` rompt la composition avant
  tout rendu.
  ⚠⚠ ET LA PROUVER VIVANTE (N19, NOUVEAU). En N19 la composition est
  passee DU PREMIER COUP, ce qui est suspect apres quatre ruptures en N18 :
  l'assertion a donc ete mise a l'epreuve sur une copie du planche.json
  portant un libelle allonge a dessein - elle a rompu (« 457 px pour 163 »).
  UNE SONDE QUI N'A JAMAIS ECHOUE NE MESURE RIEN : la faire echouer
  exprès, une fois, avant de lui faire confiance.
  ⚠ ET SE SOUVENIR DE CE QU'ELLE NE MESURE PAS : elle teste une LARGEUR,
  jamais une OCCUPATION. En N19 un libelle qui tenait parfaitement dans la
  largeur qu'on lui donnait courait neanmoins SOUS une boite voisine - et
  la largeur disponible avait ete calculee contre le CENTRE d'une branche
  au lieu du BORD de sa boite. Mesurer contre les BORDS des objets voisins.
- ⚠ LES TROIS FORMATS DOIVENT PARTAGER UNE SEULE IMPLANTATION DE LEUR
  PRIMITIVE (N17, applique d'emblee en N18 et N19). En N19, UNE fonction -
  `_am_centres(x0, x1, n)` - place tous les postes de tous les rangs et des
  trois formats : pas = (x1 - x0) / n, centre k = x0 + pas (k + 0,5).
  Aucune abscisse de poste n'est ecrite a la main, et les trois dessins ne
  PEUVENT PAS diverger. Ecrire ces regles dans des fonctions partagees, et
  les publier dans `controles`.
  ⚠ ET ECHELONNER AUSSI LES MOTIFS (N19, NOUVEAU) : le motif d'un trait
  interrompu doit s'echelonner avec le format. A l'echelle 0,62 de l'appui,
  le motif de la planche ne rendait qu'un tiret par arete et un carre de
  reserve se lisait comme un angle casse. Une valeur par FORMAT, jamais par
  glyphe : « interrompu » doit vouloir dire la meme chose partout dans un
  meme dessin.
- ⚠ LE BLOC `controles` REND COMPTE DU TRACE, PAS DE L'INTENTION (N17,
  regle dure 6 « mesurer, pas affirmer »). Ecrire dans `controles` ce qui
  est SORTI du compositeur.
- ⚠ NE PAS REECRIRE rendre_png.py : il est au depot depuis la N12, avec
  les deux pieges encodes. Usage :
  `python scripts/planches/rendre_png.py public/images/projets/<slug>
  <scratchpad>` ecrit planche.png 2400x1600 dans le dossier et, dans le
  scratchpad, les quatre controles (1152, vignette 274 et 296, appui
  552). REGARDER LES QUATRE. ⚠ Il s'appelle depuis la RACINE du depot.
  ⚠ Quand un detail est trop petit pour etre juge a l'oeil sur le PNG,
  NE PAS PLISSER LES YEUX : recadrer et agrandir par PIL (crop + resize
  NEAREST) et comparer les trois formats COTE A COTE - c'est ainsi que la
  N19 a vu la collision de son libelle de fourreau, invisible en pleine
  page.
- ⚠ LE RENDU CAIROSVG N'A PAS LES POLICES DU SITE (N13, N14, N16, N18,
  N19) : il retombe sur une police de substitution dont la chasse mono est
  ~7 a 8 % plus large. Consequence : le dernier caractere du cartouche de
  legende parait COUPE sur le PNG de controle - ne PAS « corriger » la
  largeur du cartouche, la formule `mesurer(...) + 40` est commune aux 42
  planches, et la capture du deploiement a 390 px confirme qu'il est
  entier (verifie en N18 et en N19).
- ⚠ REGARDER LES PNG, ET CORRIGER CE QU'ON Y VOIT. La N16 a fait CINQ
  retouches, la N17 DEUX, la N18 TROIS, la N19 QUATRE - dont deux
  collisions qu'aucun controle automatique ne pouvait voir. La parade est
  toujours une correction de GEOMETRIE, pas de texte : en N19, le libelle
  d'un reseau reserve a fini par passer AU-DESSUS du tronc, seule bande du
  rang ou rien ne descend.
  ⚠ Piege generique confirme en N13 a N19 : deux traits qui se croisent,
  ou un trait et un texte, doivent differer par autre chose que leur
  position - epaisseur, continuite, etiquette a fond papier, ou
  deplacement en zone franche. ⚠ Et une LEGENDE DOIT TOUCHER CE QU'ELLE
  NOMME : posee au bout de la colonne, elle cesse de nommer.
- Quand aucune surface n'existe au dossier, la chercher dans les DOCX
  COMMERCIAUX (N12, N18) ; si elle n'y est pas non plus (N13, N19),
  laisser `surface_m2` VIDE et porter au cartouche la grandeur qui compte
  l'ouvrage, avec question B. ⚠ Quand PLUSIEURS surfaces existent et
  divergent (N14, N17, N18), retenir celle qui designe EXPLICITEMENT
  l'objet de la fiche, ecrire les autres en a_valider_ft2e, et n'en
  publier qu'une seule en prose.
- Les insecables des heredocs bash sont normalisees DE FACON NON
  DETERMINISTE sur cette machine. DEUX VOIES, toutes deux eprouvees :
  (a) ecrire le .md en ESPACES ORDINAIRES et apostrophes droites par
  l'outil Write, puis passer `python scripts/injection-typographique.py
  <fichier>` qui pose les insecables, les guillemets et les U+2019 -
  c'est la voie des N12 a N19, la plus sure ; (b) script Python avec
  marqueurs ASCII remplaces par chr(8239)/chr(160) et assertion A
  L'EGALITE comptee sur le source - la voie a suivre pour tout fichier que
  injection-typographique.py ne couvre pas (planche.json, fiche de
  collecte, plan du chantier, prompt de continuite).
  ⚠⚠ ET DELIMITER CORRECTEMENT LE PERIMETRE DE CE COMPTE (N19, NOUVEAU).
  L'assertion a rompu sur 37 contre 40 : le decoupage du source utilisait
  `rsplit('\"\"\"', 1)`, qui remonte au DERNIER `\"\"\"` du fichier et avale le
  code de main(), lequel porte les litteraux '@' et '^'. Trois de trop.
  UNE BORNE DE DECOUPAGE SE VERIFIE EN IMPRIMANT CE QU'ELLE CAPTURE,
  jamais en la deduisant - et si un marqueur de plus avait ete pose dans
  la prose, les comptes se seraient egalises par compensation et la sonde
  aurait valide un texte faux.
  ⚠ injection-typographique.py protege les lignes d'enum du frontmatter
  (secteur, typologie, mission_ft2e) : une apostrophe DROITE tapee dans
  mission_ft2e y RESTE et casse le build - ecrire U+2019 des le script
  (piege N10, « Etudes d'execution »). Il NE protege PAS
  secteur_secondaire.
  ⚠ Il ne connait pas toutes les unites : en N19 « metres » et « litres »
  lui ont echappe, comme « A », « T », « tonnes », « bars », « dBA »,
  « min », « s » et « h » aux sessions precedentes. CONTROLER PAR REGEX
  APRES PASSAGE. ⚠ Et se rappeler que le CORPUS peut trancher autrement
  que la regle : en N19 le corpus ecrit « litres » avec une fine
  insecable (44 occurrences sur 46) mais « metres » avec une espace
  ORDINAIRE (16 sur 20) - c'est le corpus qui gagne, pas la regle
  abstraite.
  ⚠ IL NE POSE PAS LES ACCENTS NI LES EXPOSANTS : ecrire « m² », « m³/h »
  et « °C » directement.
- ⚠ ECRIRE LES CHAINES COURBES *ET ACCENTUEES* DES L'ECRITURE - extraction
  planche.json COMPRISE. La recette, tenue en N11 a N19 : dans le script
  d'extraction lui-meme, avant ecriture, une assertion sur l'apostrophe
  droite, une assertion sur chaque marqueur, et une assertion A L'EGALITE
  sur le COMPTE d'insecables - ce compte se LIT sur le source du script,
  jamais ecrit a la main. ⚠ Employer DEUX marqueurs distincts, « @ » pour
  la fine U+202F et « ^ » pour l'insecable U+00A0. Ne PAS prendre « # ».
  ⚠ La courbure des apostrophes doit S'ARRETER AUX EMPANS DE CODE (N19) :
  un nom de fichier reel, `Contrat d'honoraire ind C.pdf`, porte une
  apostrophe DROITE sur le disque, et la courber rend la piece
  introuvable. Meme exception que pour les accents : la prose se compose,
  les identifiants restent en ASCII.
  ⚠⚠ ET LE GARDE-FOU D'ACCENTS DOIT COUVRIR `archetype_motif` (N19,
  NOUVEAU). C'est de la PROSE, relue par FT2E. En N19 il a ete ecrit sans
  accents au premier jet - exactement la faute de la N17 - et le garde-fou
  ne l'a pas vu parce qu'il ne mesurait que cinq champs. Le calibrer sur
  une mesure (2 a 6 % de caracteres accentues) et l'appliquer a TOUTE la
  prose lue, jamais aux cles ni aux identifiants.
  La passe `python scripts/apostrophes-planches.py` (sans argument, en
  MESURE) n'a alors rien a courber - 0 sur 0 en N14 a N19.
- ⚠ ALIGNER LES GRAPHIES SUR LE CORPUS, PAS SUR LA PIECE (N17, N18, N19).
  Mesurer la graphie dominante par grep avant d'ecrire - et LA CORRECTION
  DOIT ALLER AUSSI DANS L'EXTRACTION, sinon la fiche et sa planche
  affichent deux graphies differentes sur la meme page.
- ⚠ UNE CITATION SE TRANSCRIT TELLE QU'ELLE FIGURE (N18). La bas-de-casse
  d'un titre en capitales est admise ; le changement d'un signe non.
- Les avances calibrees de _tronc.mesurer sous-mesurent Archivo 600 au
  rendu d'environ 20 % (N08-N09) - prendre la marge DANS LE CODE
  (`mesurer(...) * 1.2`), pas a l'oeil.
- ⚠ UN HEREDOC BASH PEUT MANGER UN ANTISLASH (N15, N16) ET ECHOUER SUR UNE
  APOSTROPHE (N17). Pour tout script non trivial : outil Write dans le
  SCRATCHPAD, puis execution. C'est aussi la regle qui evite que le hook
  Stop commite des scripts a usage unique.
  ⚠ ET NE JAMAIS TAPER UN CHEMIN D'ARCHIVES : les noms portent des
  accents et des apostrophes typographiques. Passer par os.walk +
  fragments de nom. La N18 a fabrique un petit module `lire.py` dans le
  scratchpad (trouver(*fragments) + un(*fragments) + texte(chemin, p0, p1)
  sur pymupdf) ; la N19 l'a repris et lui a ajoute `png(chemin, page,
  dest, zoom)` pour les plans sans couche texte. Le motif se rejoue.
  ⚠ ATTENTION AUSSI AUX ANCRES D'INSERTION DANS LE PLAN : son titre
  « ## Annexe A — prompt d'initialisation... » porte une apostrophe
  DROITE. Ancrer sur U+2019 y echoue silencieusement. Et une ancre de
  texte prise dans un .md deja passe a injection-typographique.py peut
  contenir une INSECABLE INVISIBLE : verifier par repr() avant de
  remplacer.
- Le hook Stop commite et pousse SEUL ce qui traine, et il PEUT
  COMMITTER LE LIVRABLE ENTIER. L'historique etant pousse sur un depot
  PARTAGE, il ne se reecrit pas. Pour l'eviter : garder les scripts a
  usage unique DANS LE SCRATCHPAD, hors depot (pratique des N13 a N19),
  COMMITTER TOT des que le build est vert, et reserver un second commit a
  la passe editoriale et aux documents de suivi (⚠ livrables/ porte deux
  fichiers non suivis anterieurs a la N02 - les laisser).
- /references/ est gitignore (motif ancre) - les pieces sources
  n'entrent JAMAIS au depot ; npm run preview ne mesure pas la
  performance ; Chrome refuse les fenetres sous 500 px (sonde iframe).
- La planche n'expose NI le millesime d'ouverture, NI montant, NI tiers
  (MOA, mandataire, architecte, installateur, MARQUES comprises), NI
  donnee nominative ; les designations internes (reperes de zone,
  numeros de tableau, et en N19 les DESTINATIONS DE RESEAU - « ecole
  primaire », « accueil de loisirs », « local technique ») sont admises
  avec une entree a_valider_ft2e et une question E ; tout arbitrage de
  dessin va dans a_valider_ft2e (jamais vide).

DEROULER LE PIPELINE § 2 INTEGRALEMENT : depouillement (pdfinfo /
pdftotext, ou pymupdf via python subprocess avec les noms lus par
os.listdir ; les plans sans couche texte et les marches scannes se
lisent en rendant leurs pages en PNG par pymupdf, zoom 2-3 ; antiword
pour les .doc, xlrd pour les .xls, openpyxl pour les .xlsx,
extract-msg pour les .msg) -> CONTROLE DE LA PAGE DE GARDE DE CHAQUE
PIECE TECHNIQUE -> releve du numero NN-NNN SUR PLUSIEURS PIECES FT2E, et
ETABLISSEMENT DE CE QUE DESIGNE CHAQUE AUTRE SUITE `NN-NNN` DU DOSSIER ->
references/ref_043/ (3 a 8 pieces) -> croisement commercial
(references/docs_references/ - docx sectoriels ET classeur ODS - +
docs/20-source-plaquette-2024.md + livrables/cv-ft2e/CV-FT2E.zip +
grep de src/content/ pour ce que le site publie deja, LEGENDES ET ALT
DES CLICHES COMPRIS) -> fiche de collecte (A/A+ remplies, B-E en
questions, ligne Secteur citant le classeur, DECISION Q3 motivee en
tete) -> LECTURE DES 42 SOUS-TITRES ET DES 42 `archetype_motif` pour
verifier qu'aucune these voisine n'est deja publiee -> fiche
src/content/projets/<slug>.md (SECTEUR RELEVE AU CLASSEUR ; taxonomie
ACTUELLE ; lieu avec code postal entre parentheses ; synthese 480-780 ;
>= 5 liens internes ; jamais de numero d'affaire NI de millesime
d'ouverture en prose ; convention numerale finale - nom du NOMBRE en un
seul mot en lettres, nombre COMPOSE en chiffres, unites et mesures
toujours en chiffres, citations intouchees ; verifier par
`python scripts/releve-numeral.py`, dont la section « Nombres COMPOSES
ecrits en lettres » doit rendre 0) -> PLANCHE complete (extraction avec
a_valider_ft2e non vide, apostrophes courbes ET ACCENTS des l'ecriture,
composition par scripts/planches/<archetype>.py avec assertion de
depassement SUR LES TROIS FORMATS, PROUVEE VIVANTE, et primitives
PARTAGEES, rendus par scripts/planches/rendre_png.py depuis la RACINE,
controles a 1152 / carte 274-296 / appui 552 - REGARDER les quatre PNG,
et AGRANDIR par PIL tout detail douteux -, apostrophes-planches.py en
MESURE, invariant.py, verser.py) -> qualite (typecheck 0, build vert
66 pages, editorial-reviewer EN LECTURE SEULE - ses outils d'edition
normalisent les insecables, appliquer ses constats par script, ET
VERIFIER CHACUN SUR LA PIECE OU PAR MESURE -,
controle-liens-internes 43/43 a 5, controle-numeros-affaire 0 fuite,
releve-numeral sans ecart nouveau) -> COMMIT UNIQUE fiche+planche+
compositeur (content(references): ajoute la fiche reelle <nom> et sa
planche ; git ls-remote avant, depot partage) -> push (le push deploie),
curl de la fiche AVEC barre oblique finale + marqueur de build, rendu
controle aux trois bandes (sonde iframe pour les largeurs telephone :
references/ref_042/sonde-fiche.mjs, slug et URL a adapter) ET CONTROLE
DE L'INDEXATION SECTORIELLE (point 6, sonde
references/ref_042/sonde-filtres.mjs, appelee DEPUIS LA RACINE) ->
ligne de suivi au plan -> PROMPT DE LA SESSION N21 en annexe du plan
(script Python ou Write, jamais un long heredoc) et reproduit
integralement dans le message final.
Le prompt N21 REPREND le bloc « REGLE D'INDEXATION SECTORIELLE » tel quel
(repartition remise a jour) ET porte le DEUXIEME dossier de la tranche
2022 (trois restants : 19087 Batiment SSLIA I, 20024 INNOVIA-GAELIC I,
20039 Videosurveillance CH Rochefort M). Il RAPPELLE aussi l'ecart
49 / 50 tant qu'il n'est pas tranche, ET la piste de la section
« Finalisees en 2021 » vide au classeur.

Portee de commit : content(references). Un changement de schema Zod
eventuel passe par le sous-agent content-modeller et va dans le MEME
commit que public/admin/config.yml.

Termine par le prompt de lancement de la session N21, en annexe du
plan du chantier et reproduit integralement dans ton message final -
la regle de continuite est dans CLAUDE.md parce qu'elle a ete manquee
deux fois.
```


## Annexe U — prompt de lancement de la session N21

```
Session N21/27 - FT2E v3 : chantier des 27 nouvelles fiches references.
VINGT-ET-UNIEME dossier - DEUXIEME de la tranche « Finalisees en 2022 ».

Contexte. FT2E v3 est le site institutionnel du bureau d'etudes FT2E
(La Rochelle), Astro 6 statique, deploye en demonstration client sur
https://ft2e-v3.vercel.app (indexation verrouillee - ne pas y toucher).
Le catalogue porte 43 fiches reelles (23 + N01 a N20), chacune illustree
d'une planche de schema de principe (cinq pieces par dossier).
Objectif : 50 fiches. 1 session = 1 dossier, close par le prompt de la
suivante. LA TRANCHE 2023 EST CLOSE depuis la N19.

LE ZIP DE LA TRANCHE 2022 EST DEJA SUR LE DISQUE :
C:\claude_code_dev_projects\ft2e_new_archives\2022.zip (663,5 Mo, 846
entrees, racine interne « 2022/ », un repertoire par affaire). Le
repertoire extrait de la N20 (2022/22-037-...) a ete SUPPRIME en fin de
session : il n'y a rien a nettoyer. TROIS dossiers restants, tous absents
du site (a reverifier au grep de src/content/projets/*.md) :
-   67 fichiers, 39,3 Mo : « 19-087 - Batiment SSLIA - Cab SOURD »
    (classeur I)  <- DOSSIER DU JOUR, le mieux documente des trois
-   61 fichiers, 36,8 Mo : « 20-024- INNOVIA  Projet GAELIC - Cab
    SOURD » (classeur I)
-   29 fichiers, 38,3 Mo : « 20-039- Centre Hospitalier Rochefort-
    Video surveillance » (classeur M)
IL N'Y A DONC AUCUNE QUESTION A POSER EN OUVERTURE : derouler directement,
en prenant le mieux documente d'abord (regle par defaut reconduite).

Disque : 4,4 Go libres au 2026-09-02, et le dossier du jour ne pese que
39 Mo - l'extraction filtree de la N20 n'a pas lieu d'etre ici, extraire
tout le repertoire 19-087 suffit. Si le besoin s'en presentait, le motif
est zipfile.namelist() + un fragment de chemin, et le rm -rf est REFUSE
par les permissions : passer par python shutil.rmtree.

Cartographie du dossier du jour, mesuree AU ZIP :
-   15 fichiers dans 02-Production/05-Pro
-   35 fichiers dans 02-Production/11-Det   <- il y a EU des travaux
-   17 pieces dans 01-Commerciale, dont un acte d'engagement signe, un
    CCAP signe, un avenant n° 1 du 20.02.2020, un « Projet Repartition
    Honoraires Negocies », deux « Calcul hono », un « POUVOIR SD
    ARCHITECTURES », un « estim ESQ archi », un « ConsultationMO
    Batiment SSLIA ARKEAL » et UN .msg
Extensions : 58 PDF, 3 XLS, 1 XLSX, 1 DOCX, 1 MSG.

⚠⚠ LE PIEGE ANNONCE DE CE DOSSIER : LES PIECES COMMERCIALES PORTENT
« 19.36 », PAS 19-087. Six noms de fichier de 01-Commerciale commencent
par « 19.36 » alors que le repertoire dit 19-087 et que le classeur FT2E
dit 19087. ETABLIR CE QUE 19.36 DESIGNE AVANT D'EN TIRER QUOI QUE CE SOIT
- c'est tres probablement le numero de dossier du MANDATAIRE (l'affaire
est en cotraitance avec un architecte), comme BF ECO « 534 » en N17,
SEMDAS « 2507 » et ARCHITEM « 1821 » en N10. Relever le numero FT2E sur
les pieces de PRODUCTION (cartouches de plans, en-tetes de rapport,
classeur d'honoraires interne), qui sont des pieces de production et non
des documents recopies d'un modele, et RETENIR LA MAJORITE.
⚠ Relever ensuite TOUT `\d{2}[-\s]\d{3}` du dossier et etablir, un par
un, ce que chacun designe (en N20, 30 suites distinctes : modeles de
circulateur, codes postaux, montants, kilowattheures - aucune affaire).

⚠ COTRAITANCE ET TIERS : le nom du repertoire porte « Cab SOURD » et les
pieces nomment ARKEAL et SD ARCHITECTURES. Un mandataire architecte, une
repartition d'honoraires negociee, un pouvoir. AUCUN de ces noms ne monte
sur la planche ; pour la fiche, la regle est celle des N15-N19 - un nom
deja publie par FT2E se reprend (avec E1), un nom qui ne l'est pas se
verifie d'abord dans les docx sectoriels, le classeur, la plaquette, les
CV et le CORPUS SECTEURS (legendes et alt des cliches compris).

⚠ IL Y A EU DES TRAVAUX (35 pieces en 11-Det = direction de l'execution).
Chercher la reception AUX SIX ENDROITS du protocole : un CR d'OPC portant
« RECEPTION DES TRAVAUX » en tete (N11) ; un CR annoncant la reception a
une date precise (N12) ; le BILAN DE FACTURATION (N12) ; le DERNIER CR DE
CHANTIER, dont l'en-tete remplace « PROCHAINE REUNION » par « RECEPTION
le JJ/MM/AAAA » (N13) ; LE CALENDRIER EN TETE DE CHAQUE CR D'OPC (N14) ;
et L'EN-TETE DES DERNIERS CR (N15). ⚠ Constater n'est pas prononcer : en
N18 le dernier CR CONVOQUE des receptions sans les constater, en N19 il
constate « travaux termines » et trois reserves. L'ecart va en B1.
⚠ Le .msg de 01-Commerciale se lit par `extract_msg` : en N18 et N19 le
courriel fondateur portait l'origine entiere de l'affaire.

⚠ CE QUI RESTE APRES CE DOSSIER, ET L'ECART 49 / 50 TOUJOURS NON TRANCHE.
Le classeur porte, apres les trois de 2022 : « Finalisees en 2020 » (2 :
19008 Batiment industriel Aeroport LR ELIXIR I, 20058 Diag legionelles
du port de plaisance M) et « Finalisees en 2019 » (1 : 18026 Atelier
numerique Fountaine Pajot I). Soit 2 (2022, apres celui-ci) + 2 + 1 = 5
dossiers restants pour 43 fiches en ligne : LE CLASSEUR NE MENE QU'A 49,
PAS A 50. La question a ete portee aux messages finaux des N16 a N20 et
N'A TOUJOURS PAS ETE ARBITREE PAR FT2E : la reposer tant qu'elle reste
ouverte. Ne pas fabriquer une fiche pour combler l'ecart.
⚠ PISTE RELEVEE EN N17, TOUJOURS OUVERTE ET REVERIFIEE EN N20 : le
classeur porte une section « Finalisees en 2021 » qui est VIDE - en-tete
de section, en-tete de colonnes, et aucune ligne. C'est le seul millesime
sans entree, entre 2020 (2 entrees) et 2022 (4 entrees). L'hypothese a
soumettre a FT2E est qu'une affaire manque a cette section, ce qui
expliquerait l'ecart exactement. A verifier avec eux, pas a supposer.
Les ZIP presents sur le disque : 2019, 2022, 2023, 2024, 2025. ⚠ 2020.zip
MANQUE et devra etre demande a l'ouverture de la session qui closera la
tranche 2022 (le nom du ZIP suit l'annee de FINALISATION, pas celle de
l'affaire : 19-087 et 20-024 sont dans 2022.zip).

LIRE D'ABORD, dans cet ordre :
1. docs/superpowers/plans/2026-08-27-chantier-27-nouvelles-fiches.md -
   LE PLAN : § 1 (ce qui a change), § 2 (pipeline 12 etapes), § 3
   (reponses consignees Q1/Q2/Q3), § Suivi (lignes N01 a N20),
   annexe U (ce prompt).
2. docs/superpowers/plans/2026-08-07-chantier-references-reelles.md -
   § Contraintes globales + § Protocole de session + § Regle des
   dossiers minces.
3. docs/superpowers/specs/2026-08-12-planches-references-protocole.md -
   revision 5 EN ENTIER.
4. CLAUDE.md, .claude/rules/content-collections.md et french-editorial.md.
Etalons : src/content/projets/creche-oranger-perigny.md (fiche) et, pour
une affaire INDUSTRIELLE avec maitrise d'oeuvre et travaux :
batiment-voltaero-saint-agnant.md, extension-fountaine-pajot-
aigrefeuille.md, atelier-ap-yacht-marans.md (ap-yacht-marans.md) et
undertech-la-pallice-la-rochelle.md.
Voir aussi src/content/projets/audit-chambre-des-metiers-la-rochelle.md
+ public/images/projets/audit-chambre-des-metiers-la-rochelle/ +
references/ref_043/ (fiche de collecte N20, avec sa DECISION Q3 en tete -
c'est elle qui documente le QUATRIEME REGIME DE PROPRIETE d'une piece,
l'ecart classeur/pieces sur l'annee, et les deux noms de fichier qui
mentent).
Les sondes de recette vivent dans references/ref_043/ : sonde-fiche.mjs,
sonde-filtres.mjs ET sonde-cartouche.mjs (NOUVELLE en N20 - elle mesure
au navigateur si le cartouche de reserve deborde de sa boite, la seule
facon de trancher l'artefact cairosvg autrement qu'en s'en remettant a la
regle). URL, slug et secteur a adapter ; la sonde de filtres est recalee
sur « Monotechnique - Audit » et devra l'etre sur « Industriel ». Les
trois s'appellent DEPUIS LA RACINE du depot.

REGLE D'INDEXATION SECTORIELLE - etablie le 2026-08-27, A APPLIQUER A
LA REDACTION DE CHAQUE FICHE (etape 6 du pipeline), pas apres coup :
« REFERENCES SITE FT2E.ods » (references/docs_references/, classeur
fourni par FT2E) FAIT FOI pour le classement sectoriel. Concretement,
AVANT d'ecrire le frontmatter :
1. Ouvrir le classeur (python zipfile sur content.xml, ou pandoc) et y
   retrouver l'affaire PAR SON NUMERO (graphie sans tiret : « 19087 »).
2. En relever le domaine (legende : L Logements / T Tertiaire & ERP /
   I Industriel / P Patrimoine / C Coordination SSI /
   M Monotechnique-Audit / E EXE) -> champ `secteur`.
3. Si le classeur porte un domaine DOUBLE (« T § C ») : le premier est
   le `secteur`, le second va au champ `secteur_secondaire` (optionnel
   au schema depuis le 2026-08-27, garde-fou « doit differer ») - la
   fiche parait alors dans les deux filtres et sur les deux pages de
   secteur. Precedents : hotel-yachtman (T § C), maison-pierre-loti-
   rochefort (P § C, N04), foyer-cdair-saint-martin-de-re (T § C, N10),
   auberge-central-hostel-la-rochelle (T § C, N12),
   cabanes-urbaines-la-rochelle (T § C, N15).
   LE DOSSIER DU JOUR EST A DOMAINE SIMPLE : 19087 est « I ».
4. JAMAIS de deduction depuis le dossier, l'usage RT ou le nom de
   l'operation : la N02 penchait « Industriel » pour Fors, le classeur
   dit T - et les 25 fiches ont du etre re-referencees le soir meme
   (7 bascules, commits ce334b2/09270a3). Le classeur peut contredire
   l'intuition (Saint-Rogatien, pole commercial : I ; Fors, pole
   commercial : T ; 23083 « plan de comptage Airbus » : E et non M ;
   23099 « CPAM » : M - IRVE, pas T ; 23036 Fountaine Pajot : I SIMPLE
   alors que le CV annonce « CFO / CFA / SSI » ; 20045 « THE ROOF »,
   salle d'escalade et atelier de luthier : T § C et non I ; 21086
   « Audit chauffage sites ADEI », sept etablissements medico-sociaux :
   M SIMPLE ; 21074 « AP Yacht - CATANA Group », chantier naval : I
   SIMPLE ; 20071 « Bureaux EIFFAGE », un siege d'agence avec ses
   ateliers : T SIMPLE ; 21029 « Ecole primaire et maternelle La
   Flotte », un ERP de type R : M SIMPLE ; 22037 « Audit chambre des
   metiers », qui evoque un siege tertiaire : M SIMPLE, et le
   depouillement a donne raison au classeur - la mission ne portait que
   sur le thermique et l'aeraulique) - il gagne.
   ⚠ ATTENTION PARTICULIERE ICI : un batiment SSLIA est un batiment
   d'aeroport (Service de Sauvetage et de Lutte contre l'Incendie des
   Aeronefs), et l'intuition dira « Tertiaire / ERP » ou « Coordination
   SSI » a cause du sigle. LE CLASSEUR DIT I, comme pour 19008
   « Batiment industriel Aeroport LR ELIXIR ». Et le « SSI » de SSLIA
   n'est PAS la securite incendie du batiment : c'est le service de
   secours de la plateforme. Ne pas basculer en « Coordination SSI » sur
   un homonyme.
5. CONSIGNER la lecture dans la fiche de collecte (ligne « Secteur » :
   citer l'entree du classeur telle quelle) ; si l'affaire est ABSENTE
   du classeur ou son domaine illisible -> question B a FT2E et choix
   provisoire argumente, jamais silencieux.
6. EN RECETTE (etape 10) : verifier sur le deploiement que la fiche
   repond au bon filtre de /references (compteurs de chips) et parait
   sur sa page /secteurs/<slug> - sondes : references/ref_043/
   sonde-filtres.mjs et references/ref_043/sonde-fiche.mjs (URL a adapter).
   ⚠ Une page /secteurs/<slug> n'affiche que les 4 affaires les plus
   recentes du secteur (tri par numero decroissant) ; le filtre de
   /references, lui, montre tout. Une affaire a DOUBLE domaine doit
   etre controlee sur LES DEUX filtres et LES DEUX pages de secteur.
   ⚠ 19-087 est un numero de 2019 et le secteur « Industriel » compte
   5 fiches, dont les numeros sont 23-036 (Fountaine Pajot), 22-089
   (VoltAero), 21-074 (AP Yacht), 21-046 (Undertech) et 20-104
   (Saint-Rogatien) - a reverifier au grep. 19-087 s'inserera DERNIER
   et n'entrera donc PAS dans le top 4 de /secteurs/industriel-
   commercial : c'est le tri documente, PAS un defaut, et le filtre de
   /references fait foi.
   Repartition attendue AVANT la N21, mesuree le 2026-09-02 sur le
   deploiement par references/ref_043/sonde-filtres.mjs : L10 T14 I5 P3
   C7 M6 E3 pour 43 fiches, 48 en pondere (Yachtman T+C, Loti P+C, foyer
   CDAIR T+C, Central Hostel T+C et Cabanes Urbaines T+C comptent double).

DOSSIER DU JOUR : « 19-087 - Batiment SSLIA - Cab SOURD » (67 fichiers,
39,3 Mo), classeur « 19087 · Batiment SSLIA · I ».
Points d'attention connus AVANT ouverture :
(a) ⚠ le « 19.36 » des pieces commerciales (voir plus haut) ;
(b) ⚠ la cotraitance et ses tiers (Cab SOURD, ARKEAL, SD ARCHITECTURES) ;
(c) ⚠ 35 pieces de DET : chercher la reception aux six endroits, et se
    souvenir qu'un compte de fichiers n'est pas un compte de choses -
    RECOMPTER, puis chercher une SECONDE source avant de publier un
    compte (N19 : neuf CR ET neuf reunions au calcul d'honoraires, donc
    publiable ; N18 : 46 fichiers numerotes 1-45 puis 49, donc AUCUN
    compte publie) ;
(d) ⚠ une note ou un rapport peut ne pas boucler. La N16 en a releve
    CINQ, la N18 une, la N19 une, la N20 une (scenario 3 : 793 600 €
    imprimes contre 787 400 par somme des huit preconisations). Verifier
    que les sous-totaux somment AVANT de composer quoi que ce soit de
    proportionnel, et ne rien publier de ce qui ne boucle pas ;
(e) ⚠ verifier si le site publie DEJA quelque chose de cette affaire
    (grep de src/content/ - PROSE, LEGENDES ET ALT DES CLICHES) : trois
    occurrences deja (N15, N17, N19), et en N20 le croisement
    commercial a fourni la graphie du client et son millesime.
Aucun numero 19-087 n'est publie (a reverifier au grep).
Dossier de travail a creer : references/ref_044/
Slug cible : a etablir au depouillement (kebab-case sans accents,
verifier qu'il n'ecrase rien).

CE QUE LES N01-N20 ONT ETABLI (verifiable au depot) :
- ⚠⚠ QUATRE REGIMES DE PROPRIETE D'UNE PIECE, a distinguer AVANT
  d'ecrire. (1) piece FT2E - elle fonde la fiche. (2) piece d'un tiers
  DEPOSEE POUR COMPARAISON (N19 : un devis concurrent dont le nom de
  fichier le faisait passer pour une etude FT2E) - elle ne se cite
  jamais. (3) piece d'un tiers COMMANDEE PAR UN TIERS (N19 : une etude
  d'impact sonore payee par l'installateur) - question a FT2E, rien
  n'est publie. (4) NOUVEAU EN N20 : l'ARCHIVE DE L'OUVRAGE - le dossier
  de construction d'origine, recupere comme matiere de travail. A la
  Maison des Metiers, trois pieces de 1994-1995 (CCTP du lot 9,
  bordereau de prix, etude de faisabilite), 19 Mo, d'un autre architecte
  et d'un autre bureau d'etudes. Elle se LIT et s'EXPLOITE, mais ni son
  auteur ni ses valeurs ne se publient. C'est l'EN-TETE ou le CARTOUCHE
  qui tranche - jamais le repertoire, jamais le nom de fichier.
- ⚠⚠ UN NOM DE FICHIER MENT (N19, N20). « DESCRIPTIFS POUR CCTP 2022
  2023.docx » etait un catalogue de textes de prescription d'un
  fabricant ; « 19xxx-SUIVI.doc » un gabarit vierge de compte rendu FT2E
  dont tous les champs sont vides. OUVRIR AVANT DE CONCLURE, y compris
  les .doc (antiword, ou extraction brute des chaines).
- ⚠⚠ LA PAGE DE GARDE D'UN CCTP FT2E PEUT PORTER UN FAUX NUMERO (N18 et
  N19, deux fois de suite). RELEVER LE NUMERO SUR PLUSIEURS PIECES ET
  RETENIR LA MAJORITE ; les pieces les plus sures sont les CARTOUCHES DE
  PLANS et le CLASSEUR D'HONORAIRES INTERNE. Autres faux deja
  rencontres : references de modele constructeur, numeros de dossier des
  mandataires, numeros de permis, surfaces foncieres, codes postaux, et
  NUMEROS DE NORMES (NF X 46-020, NF S 31-010, NF C 15-100).
- ⚠ LE CLASSEUR PEUT ETRE EN ECART D'UN AN, ET LE CROISEMENT COMMERCIAL
  TRANCHE (N20, NOUVEAU). Il rangeait 22037 sous « Finalisees en 2022 »
  quand quatre sources disaient 2023, dont DEUX PIECES FT2E DEJA
  PUBLIEES : la plaquette 2024 (docs/20-source-plaquette-2024.md) et les
  CV de l'equipe (livrables/cv-ft2e/CV-FT2E.zip, edition aout 2026).
  Les interroger SYSTEMATIQUEMENT a l'etape 4 - ils donnent le
  millesime, la graphie du client, et parfois l'affaire entiere.
  ⚠ Les onze docx sectoriels de references/docs_references/ portent
  souvent la fiche commerciale de l'affaire (N18, decisif) - mais pas
  toujours (N19 et N20 : muets). C'est un resultat a consigner, pas un
  echec.
- ⚠ UN INDICE DE CONTRAT N'EST PAS UNE AFFAIRE - CINQ confirmations
  (N15, N16, N17, N19, N20). Le depart se fait sur les pieces de
  PRODUCTION, qui portent le numero SANS indice, et le classeur ne
  connait qu'une entree. ⚠ Ni s'etonner que deux contrats portent le
  meme indice. ⚠ Et VERIFIER QUI A SIGNE : en N20 le contrat etait
  adresse au proprietaire et signe du cachet du SYNDIC.
- ⚠ UNE MISSION PEUT ETRE SENSIBLE ET NE PAS SE PUBLIER (N20). L'indice
  B de 22-037 portait une assistance a constat d'huissier sur les
  desordres releves par l'audit : rien n'en a ete ecrit, tout est en
  question E. Publier qu'un audit FT2E a debouche sur un constat
  d'huissier revient a porter un litige mettant en cause des tiers
  identifiables.
- ⚠ UNE THESE PEUT ETRE DEJA PUBLIEE - et c'est le risque PRINCIPAL,
  avec 43 planches au corpus. AVANT d'arreter une these, lire les
  `sous_titre` ET les `archetype_motif` des 43 planches
  (PYTHONIOENCODING=utf-8 python -c "..." sur
  public/images/projets/*/planche.json). La N17 a du abandonner DEUX
  theses, la N18 une, la N19 TROIS, la N20 une (la recuperation
  d'energie entre orientations opposees, que le batiment appelait
  pourtant : la planche du siege d'Eiffage la publie deja). La question
  n'est pas « est-ce que ca demontre bien ? » mais « est-ce que ca
  demontre quelque chose que le corpus ne demontre pas deja ? ».
- Archetypes apres N20 : boucle-fluide 12 - coupe-traversee 9 -
  tableau-electrique 7 - sankey-energie 7 - zonage-ssi 6 -
  chronologie-affaire 2 - planche-chiffree 0 SANS module. L'archetype se
  choisit sur la THESE, jamais sur le secteur ni sur le quota, mais a
  these egale preferer ce qui n'a pas servi depuis longtemps ; la dette
  de variete porte toujours sur boucle-fluide (12/43), et
  chronologie-affaire n'a pas servi depuis le corpus fondateur
  (admissible seulement si sa these est d'INGENIERIE, jamais le
  calendrier d'une operation). ⚠ `planche-chiffree` n'a toujours pas de
  module : si un dossier l'exige, la decision est de L'ECRIRE ou de
  retirer l'archetype de la liste fermee, jamais de bricoler.
- Un mecanisme nouveau s'ecrit DANS le compositeur d'archetype
  (constantes prefixees par le mecanisme ; garde-fou de greffe sur le
  NOM DE LA FONCTION ET sur les prefixes de constantes - automatise
  depuis la N13 : en N20, 51 fonctions et 152 constantes existantes
  contre 5 et 20 nouvelles, prefixe unique `EX_`, zero collision), et
  l'invariant octet se rejoue AVANT la greffe, APRES la greffe et APRES
  la derniere retouche. `python scripts/planches/invariant.py` couvre
  les 6 compositeurs et les 43 dossiers (172/172 au 2026-09-02).
  ⚠ Un dossier neuf dont la planche n'est pas encore composee fait
  ECHOUER l'invariant : LIRE LE DENOMINATEUR. Composer d'abord, mesurer
  ensuite.
- ⚠⚠ SEPARER LES MESURES DE L'ECHELLE DES MOTIFS (N20, NOUVEAU). La N19
  avait etabli que les trois formats partagent UNE implantation de leur
  primitive et que les motifs s'echelonnent avec le format. La N20 ajoute
  la distinction qui rend les deux compatibles : les MESURES du dessin
  (largeur et hauteur de boite, ordonnees) sont ABSOLUES et propres a
  chaque format - une boite de vignette n'est pas une boite de planche
  reduite -, et l'echelle `ech` ne commande QUE les motifs et les petits
  accessoires (interruption, pointe de fleche, plot, breche). Melanger
  les deux donne des boites de 13 px sur la vignette.
- ⚠ METTRE UNE ASSERTION DE DEPASSEMENT DANS LE COMPOSITEUR, SUR LES
  TROIS FORMATS, ET LA PROUVER VIVANTE. En N20 la composition est passee
  du premier coup : l'assertion a donc ete mise a l'epreuve sur QUATRE
  copies du planche.json portant chacune un libelle allonge a dessein,
  une par format plus une sur la bande dont la largeur est bornee par le
  bord d'une boite voisine. Les quatre ont rompu. UNE SONDE QUI N'A
  JAMAIS ECHOUE NE MESURE RIEN.
  ⚠ ET SE SOUVENIR DE CE QU'ELLE NE MESURE PAS : elle teste une LARGEUR,
  jamais une OCCUPATION. Mesurer contre les BORDS des objets voisins.
- ⚠ REGARDER LES PNG, ET CORRIGER CE QU'ON Y VOIT. La N16 a fait CINQ
  retouches, la N17 DEUX, la N18 TROIS, la N19 QUATRE, la N20 DEUX -
  dont une qu'aucun controle automatique ne pouvait voir : DEUX
  PROTECTIONS DOIVENT DIFFERER PAR LEUR FORME, PAS PAR LEUR POSITION.
  Le premier capot etait une barre posee au-dessus de la machine ; au PNG
  il se lisait comme une seconde boite plate, quand le grillage de la
  colonne voisine se lisait d'emblee. Refait en CADRE ferme autour de la
  machine. La seconde retouche : une enceinte au filet-3 pour donner un
  corps a la bande basse, dont la moitie gauche est vide par
  construction. ⚠ Et AGRANDIR par PIL (crop + resize NEAREST) tout detail
  douteux, plutot que de plisser les yeux.
- ⚠⚠ LE BLOC `controles` D'UN planche.json EST DE LA PROSE (N20,
  NOUVEAU). Il est ecrit depuis le SOURCE PYTHON du compositeur, et les
  apostrophes droites qu'on y tape s'y retrouvent. `python
  scripts/apostrophes-planches.py` (sans argument, en MESURE) le voit :
  il a rendu « 21 apostrophes sur 2 pieces » en N20, la ou les N14-N19
  rendaient 0 sur 0. LE REJOUER APRES LA PREMIERE COMPOSITION, puis
  `--appliquer`, puis RECOMPOSER. ⚠ Deux apostrophes ont resiste :
  celles ECHAPPEES (\') dans une f-string a delimiteur simple, que le
  script refuse a juste titre. La correction est de changer le
  delimiteur, pas le refus.
- ⚠⚠ UN GARDE-FOU EN POURCENTAGE D'ACCENTS EST MAL CALIBRE (N20, il
  CORRIGE la N19). La N19 prescrivait « 2 a 6 % de caracteres
  accentues » champ par champ. Mesure le 2026-09-01 sur les 747 chaines
  de prose de 60 signes ou plus des 42 planches publiees : mediane
  2,63 %, mais 31,5 % des champs tombent SOUS 2,0 % et 9,5 % sous 1,0 %.
  Deux phrases parfaitement accentuees de la N20 le franchissaient par
  le bas. UN SEUIL QUI REFUSE UN TEXTE JUSTE FINIT DESACTIVE.
  L'instrument retenu n'a pas de seuil arbitraire et vise exactement la
  faute decrite : (1) aucun mot ne doit paraitre en graphie NUE alors
  que sa graphie ACCENTUEE existe ailleurs dans le meme document -
  ⚠ en ne comptant PAS « deplace » contre « deplace » accentues
  autrement, qui sont deux formes justes ; (2) un plancher de 2 % sur la
  PROSE GLOBALE, echantillon assez grand pour que le pourcentage veuille
  dire quelque chose. Les deux sondes sont mises a l'epreuve sur le meme
  texte desaccentue, et rompent.
  ⚠ ET CE PLANCHER GLOBAL A INTERCEPTE SON PROPRE INSTRUMENT : la
  fonction de comptage, reecrite pour comparer une chaine NFC a sa forme
  nue, rendait 0,00 % sur un texte accentue. Le compte se fait sur la
  forme DECOMPOSEE (NFD).
- Les insecables des heredocs bash sont normalisees DE FACON NON
  DETERMINISTE sur cette machine. DEUX VOIES, toutes deux eprouvees :
  (a) ecrire le .md en ESPACES ORDINAIRES et apostrophes droites par
  l'outil Write, puis passer `python scripts/injection-typographique.py
  <fichier>` - c'est la voie des N12 a N20, la plus sure ; (b) script
  Python avec marqueurs ASCII remplaces par chr(8239)/chr(160) et
  assertion A L'EGALITE comptee sur le source - la voie pour tout
  fichier que injection-typographique.py ne couvre pas (planche.json,
  plan du chantier, prompt de continuite).
  ⚠ CHOISIR LES MARQUEURS CONTRE LE CORPUS REEL : le seul choix sur est
  un caractere qui ne peut pas figurer dans le texte - '\x01', '\x02',
  '\x03', ecrits en ECHAPPEMENT ASCII dans le source (« # » collisionne
  avec les titres Markdown, « % » avec « 30 % »).
  ⚠⚠ UNE ANCRE DE REMPLACEMENT SE VERIFIE PAR repr(), PAS PAR DEDUCTION
  (N19, rejoue DEUX FOIS en N20). Une ancre prise dans un .md deja passe
  a injection-typographique.py peut porter une insecable invisible - et
  le patch qui tente de la corriger peut echouer a son tour, l'outil
  d'ecriture normalisant le caractere. La parade : imprimer repr() du
  segment, puis ancrer sur un fragment ASCII pur, ou reperer la LIGNE
  sans jamais retaper le segment ambigu.
  ⚠ injection-typographique.py protege les lignes d'enum du frontmatter
  (secteur, typologie, mission_ft2e) : une apostrophe DROITE tapee dans
  mission_ft2e y RESTE et casse le build. Il NE protege PAS
  secteur_secondaire. ⚠ Il ne connait pas toutes les unites - il a appris
  « mg/L », « g/L » et « °F » en N20, « metres » et « litres » lui
  echappent toujours. CONTROLER PAR REGEX APRES PASSAGE. ⚠ Et le CORPUS
  peut trancher autrement que la regle : mesurer la graphie dominante
  par grep avant d'ecrire. ⚠ IL NE POSE PAS LES ACCENTS NI LES
  EXPOSANTS : ecrire « m² », « m³/h » et « °C » directement.
- ⚠ L'AGENT DE RELECTURE TROUVE DE VRAIES ERREURS DE FAIT SANS AVOIR LES
  PIECES (N15, N18, N19, N20). En N20 il a trouve une CONTRADICTION AVEC
  DEUX FICHES PUBLIEES (« cinq reponses » quand la fiche ADEI publie
  « Les sites ont donne trois reponses » et que La Flotte le reprend
  deja), une DEDUCTION FAUSSE (un « soit » qui enchainait les cibles du
  decret sur la consommation de reference OPERAT, dont -40 % donne 50,4
  et non 41,22), et LA CLAUSE DE CLOTURE MANQUANTE, sans laquelle le
  present du paragraphe « solution » se lisait comme un chantier realise
  alors qu'il n'y avait eu AUCUN travaux. LUI DONNER EN CONTEXTE LES
  FAITS ETABLIS SUR PIECE et lui demander EXPLICITEMENT les chaines
  exactes avant/apres - il travaille EN LECTURE SEULE, ses outils
  d'edition normalisent les insecables.
  ⚠⚠ ET LE VERIFIER, TOUJOURS : en N18 il s'est trompe une fois, en N19
  trois fois, en N20 une fois (« CRC4 » qu'il proposait d'ecrire « C4 »
  au titre de EN ISO 12944, alors que c'est la graphie LITTERALE du
  rapport d'audit et de la preconisation 04). MESURER OU RELIRE LA PIECE
  AVANT D'APPLIQUER, constat par constat.
- ⚠ LE CARTOUCHE DE RESERVE PARAIT COUPE SUR LE PNG DE CONTROLE - le
  rendu cairosvg n'a pas IBM Plex Mono et substitue une chasse ~8 % plus
  large. NE PAS « corriger » la largeur du cartouche : la formule
  `mesurer(...) + 40` est commune aux 43 planches. La N20 a cesse de s'en
  remettre a la regle et l'a MESURE au navigateur sur le deploiement
  (references/ref_043/sonde-cartouche.mjs) : cartouche entier, 26 px de
  marge a droite. La sonde se rejoue.
- ⚠ NE PAS REECRIRE rendre_png.py : il est au depot depuis la N12.
  Usage : `python scripts/planches/rendre_png.py
  public/images/projets/<slug> <scratchpad>`. REGARDER LES QUATRE
  controles. ⚠ Il s'appelle depuis la RACINE du depot.
- ⚠ UN HEREDOC BASH PEUT MANGER UN ANTISLASH, ECHOUER SUR UNE APOSTROPHE
  ET MANGER LES ACCENTS (N15, N16, N17, N20). Pour tout script non
  trivial : outil Write dans le SCRATCHPAD, puis execution. C'est aussi
  la regle qui evite que le hook Stop commite des scripts a usage unique.
  ⚠ ET NE JAMAIS TAPER UN CHEMIN D'ARCHIVES : les noms portent des
  accents et des apostrophes typographiques. Passer par os.walk +
  fragments de nom. Le petit module `lire.py` du scratchpad
  (trouver/un/texte/png/docx/xlsx sur pymupdf, zipfile et openpyxl) se
  rejoue de session en session.
- Le hook Stop commite et pousse SEUL ce qui traine, et il PEUT
  COMMITTER LE LIVRABLE ENTIER. L'historique etant pousse sur un depot
  PARTAGE, il ne se reecrit pas. Pour l'eviter : garder les scripts a
  usage unique DANS LE SCRATCHPAD, hors depot, COMMITTER TOT des que le
  build est vert, et reserver un second commit a la passe editoriale et
  aux documents de suivi (⚠ livrables/ porte deux fichiers non suivis
  anterieurs a la N02 - les laisser).
- /references/ est gitignore (motif ancre) - les pieces sources
  n'entrent JAMAIS au depot ; npm run preview ne mesure pas la
  performance ; Chrome refuse les fenetres sous 500 px (sonde iframe).
- La planche n'expose NI le millesime d'ouverture, NI montant, NI tiers
  (MOA, mandataire, architecte, installateur, MARQUES comprises), NI
  donnee nominative ; les designations internes (reperes de zone,
  numeros de tableau, destinations de reseau, et en N20 les orientations
  « sud »/« nord », les quartiers NE/NO/SE/SO et le niveau R+4) sont
  admises avec une entree a_valider_ft2e et une question E ; tout
  arbitrage de dessin va dans a_valider_ft2e (jamais vide).
  ⚠ ET SAVOIR CE QUE LE CORPUS A DEJA FAIT DIRE A UN SIGNE : le trait
  interrompu signifie « position abandonnee » sur la planche de la
  Maison des Metiers et « reserve pour plus tard » sur celle du groupe
  scolaire de La Flotte. Les deux sont legitimes, l'en-tete les leve a
  chaque fois - mais il faut le savoir avant d'en ajouter un troisieme.

DEROULER LE PIPELINE § 2 INTEGRALEMENT : depouillement (pdfinfo /
pdftotext, ou pymupdf via python subprocess avec les noms lus par
os.listdir ; les plans sans couche texte et les marches scannes se
lisent en rendant leurs pages en PNG par pymupdf, zoom 2-3 ; antiword
pour les .doc, xlrd pour les .xls, openpyxl pour les .xlsx,
extract-msg pour les .msg) -> CONTROLE DE LA PAGE DE GARDE DE CHAQUE
PIECE TECHNIQUE, ET DE SON REGIME DE PROPRIETE (les quatre) -> releve du
numero NN-NNN SUR PLUSIEURS PIECES FT2E, et ETABLISSEMENT DE CE QUE
DESIGNE CHAQUE AUTRE SUITE `NN-NNN` DU DOSSIER, « 19.36 » COMPRIS ->
references/ref_044/ (3 a 8 pieces) -> croisement commercial
(references/docs_references/ - docx sectoriels ET classeur ODS - +
docs/20-source-plaquette-2024.md + livrables/cv-ft2e/CV-FT2E.zip +
grep de src/content/ pour ce que le site publie deja, LEGENDES ET ALT
DES CLICHES COMPRIS) -> fiche de collecte (A/A+ remplies, B-E en
questions, ligne Secteur citant le classeur, DECISION Q3 motivee en
tete) -> LECTURE DES 43 SOUS-TITRES ET DES 43 `archetype_motif` pour
verifier qu'aucune these voisine n'est deja publiee -> fiche
src/content/projets/<slug>.md (SECTEUR RELEVE AU CLASSEUR ; taxonomie
ACTUELLE ; lieu avec code postal entre parentheses ; synthese 480-780 ;
>= 5 liens internes ; une CLAUSE DE CLOTURE en dernier paragraphe ;
jamais de numero d'affaire NI de millesime d'ouverture en prose ;
convention numerale finale - nom du NOMBRE en un seul mot en lettres,
nombre COMPOSE en chiffres, unites et mesures toujours en chiffres,
citations intouchees ; verifier par `python scripts/releve-numeral.py`,
dont la section « Nombres COMPOSES ecrits en lettres » doit rendre 0) ->
PLANCHE complete (extraction avec a_valider_ft2e non vide, apostrophes
courbes ET ACCENTS des l'ecriture, composition par
scripts/planches/<archetype>.py avec assertion de depassement SUR LES
TROIS FORMATS, PROUVEE VIVANTE, primitives PARTAGEES et MESURES
distinguees des MOTIFS, rendus par scripts/planches/rendre_png.py depuis
la RACINE, controles a 1152 / carte 274-296 / appui 552 - REGARDER les
quatre PNG, et AGRANDIR par PIL tout detail douteux -,
apostrophes-planches.py en MESURE **APRES la premiere composition**,
invariant.py, verser.py) -> qualite (typecheck 0, build vert 67 pages,
editorial-reviewer EN LECTURE SEULE, ET VERIFIER CHACUN DE SES CONSTATS
SUR LA PIECE OU PAR MESURE, controle-liens-internes 44/44 a 5,
controle-numeros-affaire 0 fuite, releve-numeral sans ecart nouveau) ->
COMMIT (content(references): ajoute la fiche reelle <nom> et sa planche ;
git ls-remote avant, depot partage) -> push (le push deploie), curl de la
fiche AVEC barre oblique finale + marqueur de build, rendu controle aux
trois bandes (sonde iframe pour les largeurs telephone :
references/ref_043/sonde-fiche.mjs, slug et URL a adapter), CARTOUCHE
MESURE (sonde-cartouche.mjs) ET CONTROLE DE L'INDEXATION SECTORIELLE
(point 6, sonde references/ref_043/sonde-filtres.mjs, appelee DEPUIS LA
RACINE) -> ligne de suivi au plan -> PROMPT DE LA SESSION N22 en annexe
du plan (script Python ou Write, jamais un long heredoc) et reproduit
integralement dans le message final.
Le prompt N22 REPREND le bloc « REGLE D'INDEXATION SECTORIELLE » tel quel
(repartition remise a jour) ET porte le TROISIEME dossier de la tranche
2022 (deux restants : 20024 INNOVIA-GAELIC I, 20039 Videosurveillance CH
Rochefort M). Il RAPPELLE aussi l'ecart 49 / 50 tant qu'il n'est pas
tranche, la piste de la section « Finalisees en 2021 » vide au classeur,
ET que 2020.zip doit etre demande a l'utilisateur avant la session qui
suivra la cloture de la tranche 2022.

Portee de commit : content(references). Un changement de schema Zod
eventuel passe par le sous-agent content-modeller et va dans le MEME
commit que public/admin/config.yml.

Termine par le prompt de lancement de la session N22, en annexe du
plan du chantier et reproduit integralement dans ton message final -
la regle de continuite est dans CLAUDE.md parce qu'elle a ete manquee
deux fois.
```


## Annexe V — prompt de lancement de la session N22

```
Session N22/27 - FT2E v3 : chantier des 27 nouvelles fiches references.
VINGT-DEUXIEME dossier - TROISIEME de la tranche « Finalisees en 2022 ».

Contexte. FT2E v3 est le site institutionnel du bureau d'etudes FT2E
(La Rochelle), Astro 6 statique, deploye en demonstration client sur
https://ft2e-v3.vercel.app (indexation verrouillee - ne pas y toucher).
Le catalogue porte 44 fiches reelles (23 + N01 a N21), chacune illustree
d'une planche de schema de principe (cinq pieces par dossier).
Objectif : 50 fiches. 1 session = 1 dossier, close par le prompt de la
suivante. LA TRANCHE 2023 EST CLOSE depuis la N19.

LE ZIP DE LA TRANCHE 2022 EST DEJA SUR LE DISQUE :
C:\claude_code_dev_projects\ft2e_new_archives\2022.zip (663,5 Mo, 846
entrees, racine interne « 2022/ », un repertoire par affaire). Les
repertoires extraits des N20 et N21 ont ete SUPPRIMES en fin de session :
il n'y a rien a nettoyer, et C:\claude_code_dev_projects\ft2e_new_archives
\extrait doit etre vide ou absent. DEUX dossiers restants, tous deux
absents du site (a reverifier au grep de src/content/projets/*.md) :
-   61 fichiers, 36,8 Mo : « 20-024- INNOVIA  Projet GAELIC - Cab
    SOURD » (classeur I)  <- DOSSIER DU JOUR, le mieux documente des deux
-   29 fichiers, 38,3 Mo : « 20-039- Centre Hospitalier Rochefort-
    Video surveillance » (classeur M)
IL N'Y A DONC AUCUNE QUESTION A POSER EN OUVERTURE : derouler directement,
en prenant le mieux documente d'abord (regle par defaut reconduite).

Disque : 4,4 Go libres au 2026-09-02, et le dossier du jour ne pese que
37 Mo - extraire tout le repertoire 20-024 suffit. Le motif d'extraction
est zipfile.namelist() + un fragment de chemin (« 20-024 ») ; le rm -rf
est REFUSE par les permissions : passer par python shutil.rmtree.

⚠⚠ CE QUE LA N21 A ETABLI SUR SD ARCHITECTES, ET QUI SERT ICI. Le dossier
du jour porte « Cab SOURD » comme celui de la N21 : c'est SD Architectes
(alias « Sourd Durand Architectes », alias « SD ARCHITECTURES »), l'agence
de Rochefort mandataire de TROIS operations deja publiees - VoltAero
(21-095, N13), les ateliers pilotes de Capsulae (22-006) et le batiment
SSLIA (19-087, N21). Le site publie deja les graphies « SD Architectes »
et « BET Boulard » : LES REPRENDRE TELLES QUELLES (grep de src/content/
DES L'ETAPE 4, pas apres coup - en N21 ce grep a fourni la graphie du
maitre d'ouvrage, celle de l'architecte et celle du BET structures d'un
seul coup). ⚠ Et SD Architectes NUMEROTE SES DOSSIERS « AA.NN » : la N21
a trouve « 19.36 » dans SIX noms de fichier commerciaux et 33 CR de
chantier, la ou l'affaire FT2E est 19-087. ATTENDRE LE MEME PIEGE ICI.

⚠⚠ INNOVIA EST DEJA CONNU DE DEUX SOURCES DU DEPOT. (1) Le « dossier de
references industriel » de FT2E, verse dans references/ref_044/ ? NON -
il est reste dans l'archive, mais la N21 l'a depouille : il porte
« Extension Usine INNOVIA - MAITRE D'OUVRAGE : INNOVIA - ARCHITECTE :
SOURD DURAND ARCHITECTES - MONTANT TRAVAUX : 5 400 000 € - RT 2012 -
PLOMBERIE, CHAUFFAGE, VENTILATION, AIR COMPRIME, EAU CHAUDE,
ELECTRICITE, RT2012 - SHON : 2400 m² - REALISATION : CHANTIER EN COURS »
et, plus ancien, « Usine INNOVIA LA ROCHELLE - 4 800 000 € - RT 2005 -
RT2012 - SHON : 4030 m² - REALISATION : 2013 ». (2) La fiche publiee
`ateliers-pilotes-capsulae` dit que Capsulae est « societe du groupe
Innov'ia ». ⚠ ETABLIR SUR PIECE si « INNOVIA » du dossier du jour est la
meme entite que « Innov'ia » (groupe agroalimentaire rochelais) - la
graphie diverge, et un homonyme d'un caractere est exactement le genre
d'erreur qu'une fiche ne rattrape pas. Le classeur dit « 20024 |
INNOVIA - GAELIC | I ». « GAELIC » est probablement le nom du projet ou
du batiment : le determiner, ne pas le supposer.

LIRE D'ABORD, dans cet ordre :
1. docs/superpowers/plans/2026-08-27-chantier-27-nouvelles-fiches.md -
   LE PLAN : § 1 (ce qui a change), § 2 (pipeline 12 etapes), § 3
   (reponses consignees Q1/Q2/Q3), § Suivi (lignes N01 a N21),
   annexe V (ce prompt).
2. docs/superpowers/plans/2026-08-07-chantier-references-reelles.md -
   § Contraintes globales + § Protocole de session + § Regle des
   dossiers minces.
3. docs/superpowers/specs/2026-08-12-planches-references-protocole.md -
   revision 5 EN ENTIER.
4. CLAUDE.md, .claude/rules/content-collections.md et french-editorial.md.
Etalons : src/content/projets/creche-oranger-perigny.md (fiche) et, pour
une affaire INDUSTRIELLE avec maitrise d'oeuvre et travaux :
batiment-sslia-aeroport-la-rochelle.md (N21, meme architecte),
ateliers-pilotes-capsulae.md (meme architecte, meme BET structures),
batiment-voltaero-saint-agnant.md (idem), extension-fountaine-pajot-
aigrefeuille.md et undertech-la-pallice-la-rochelle.md.
Voir aussi public/images/projets/batiment-sslia-aeroport-la-rochelle/ +
references/ref_044/ (fiche de collecte N21, avec sa DECISION Q3 et son
§ « LE PIEGE DU NUMERO » en tete - c'est elle qui documente les DEUX
pieces qui elucident un numero de mandataire, la coquille d'en-tete qui
traverse quatorze comptes rendus, et le troisieme numero FT2E isole).
Les sondes de recette vivent dans references/ref_044/ : sonde-fiche.mjs,
sonde-filtres.mjs et sonde-cartouche.mjs, DEJA RECALEES SUR LA N21.
⚠ Leurs selecteurs sont EN DUR sur le texte de la fiche precedente :
sonde-cartouche cherche « AU CALCUL RT » dans le cartouche, sonde-filtres
teste le secteur « Industriel » et la page /secteurs/industriel-commercial.
LES RECALER AVANT DE CONCLURE - une sonde qui ne trouve pas son noeud
rend `null` sans echouer. ⚠ sonde-cartouche.mjs et sonde-fiche.mjs
prennent un REPERTOIRE en argument, pas un fichier ; rendre_png.py aussi.
Les trois s'appellent DEPUIS LA RACINE du depot.

REGLE D'INDEXATION SECTORIELLE - etablie le 2026-08-27, A APPLIQUER A
LA REDACTION DE CHAQUE FICHE (etape 6 du pipeline), pas apres coup :
« REFERENCES SITE FT2E.ods » (references/docs_references/, classeur
fourni par FT2E) FAIT FOI pour le classement sectoriel. Concretement,
AVANT d'ecrire le frontmatter :
1. Ouvrir le classeur (python zipfile sur content.xml, ou pandoc) et y
   retrouver l'affaire PAR SON NUMERO (graphie sans tiret : « 20024 »).
2. En relever le domaine (legende : L Logements / T Tertiaire & ERP /
   I Industriel / P Patrimoine / C Coordination SSI /
   M Monotechnique-Audit / E EXE) -> champ `secteur`.
3. Si le classeur porte un domaine DOUBLE (« T § C ») : le premier est
   le `secteur`, le second va au champ `secteur_secondaire` (optionnel
   au schema depuis le 2026-08-27, garde-fou « doit differer ») - la
   fiche parait alors dans les deux filtres et sur les deux pages de
   secteur. Precedents : hotel-yachtman (T § C), maison-pierre-loti-
   rochefort (P § C, N04), foyer-cdair-saint-martin-de-re (T § C, N10),
   auberge-central-hostel-la-rochelle (T § C, N12),
   cabanes-urbaines-la-rochelle (T § C, N15).
   LE DOSSIER DU JOUR EST A DOMAINE SIMPLE : 20024 est « I ».
4. JAMAIS de deduction depuis le dossier, l'usage RT ou le nom de
   l'operation : la N02 penchait « Industriel » pour Fors, le classeur
   dit T - et les 25 fiches ont du etre re-referencees le soir meme
   (7 bascules, commits ce334b2/09270a3). Le classeur peut contredire
   l'intuition (Saint-Rogatien, pole commercial : I ; Fors, pole
   commercial : T ; 23083 « plan de comptage Airbus » : E et non M ;
   23099 « CPAM » : M - IRVE, pas T ; 23036 Fountaine Pajot : I SIMPLE
   alors que le CV annonce « CFO / CFA / SSI » ; 20045 « THE ROOF »,
   salle d'escalade et atelier de luthier : T § C et non I ; 21086
   « Audit chauffage sites ADEI », sept etablissements medico-sociaux :
   M SIMPLE ; 21074 « AP Yacht - CATANA Group », chantier naval : I
   SIMPLE ; 20071 « Bureaux EIFFAGE », un siege d'agence avec ses
   ateliers : T SIMPLE ; 21029 « Ecole primaire et maternelle La
   Flotte », un ERP de type R : M SIMPLE ; 22037 « Audit chambre des
   metiers » : M SIMPLE ; 19087 « Batiment SSLIA », dont le sigle
   evoque la securite incendie et le programme un ERP : I SIMPLE, et le
   depouillement a donne raison au classeur - l'architecte ecrit
   lui-meme « batiment type industriel ») - il gagne.
5. CONSIGNER la lecture dans la fiche de collecte (ligne « Secteur » :
   citer l'entree du classeur telle quelle) ; si l'affaire est ABSENTE
   du classeur ou son domaine illisible -> question B a FT2E et choix
   provisoire argumente, jamais silencieux.
6. EN RECETTE (etape 10) : verifier sur le deploiement que la fiche
   repond au bon filtre de /references (compteurs de chips) et parait
   sur sa page /secteurs/<slug> - sondes : references/ref_044/
   sonde-filtres.mjs et references/ref_044/sonde-fiche.mjs (URL a adapter).
   ⚠ Une page /secteurs/<slug> n'affiche que les 4 affaires les plus
   recentes du secteur (tri par numero decroissant) ; le filtre de
   /references, lui, montre tout. Une affaire a DOUBLE domaine doit
   etre controlee sur LES DEUX filtres et LES DEUX pages de secteur.
   ⚠ 20-024 est un numero de 2020 et le secteur « Industriel » compte
   6 fiches apres la N21 : 23-036 (Fountaine Pajot), 22-089 (VoltAero),
   22-006 (ateliers Capsulae), 21-074 (AP Yacht), 20-104 (Saint-
   Rogatien) et 19-087 (batiment SSLIA) - a reverifier au grep.
   20-024 s'inserera AVANT-DERNIER et n'entrera donc PAS dans le top 4
   de /secteurs/industriel-commercial : c'est le tri documente, PAS un
   defaut, et le filtre de /references fait foi.
   Repartition attendue AVANT la N22, mesuree le 2026-09-02 sur le
   deploiement par references/ref_044/sonde-filtres.mjs : L10 T14 I6 P3
   C7 M6 E3 pour 44 fiches, 49 en pondere (Yachtman T+C, Loti P+C, foyer
   CDAIR T+C, Central Hostel T+C et Cabanes Urbaines T+C comptent double).

DOSSIER DU JOUR : « 20-024- INNOVIA  Projet GAELIC - Cab SOURD »
(61 fichiers, 36,8 Mo), classeur « 20024 · INNOVIA - GAELIC · I ».
Points d'attention connus AVANT ouverture :
(a) ⚠ le numero de dossier du mandataire SD Architectes, au format
    « AA.NN » (voir plus haut) ;
(b) ⚠ l'identite exacte d'INNOVIA et le sens de « GAELIC » (voir plus
    haut) ;
(c) ⚠ chercher la reception AUX SIX ENDROITS du protocole : un CR d'OPC
    portant « RECEPTION DES TRAVAUX » en tete (N11) ; un CR annoncant la
    reception a une date precise (N12) ; le BILAN DE FACTURATION (N12) ;
    le DERNIER CR DE CHANTIER, dont l'en-tete remplace « PROCHAINE
    REUNION » par « RECEPTION le JJ/MM/AAAA » (N13) ; LE CALENDRIER EN
    TETE DE CHAQUE CR D'OPC (N14) ; et L'EN-TETE DES DERNIERS CR (N15).
    ⚠ Constater n'est pas prononcer : en N18 et en N21 le dernier CR
    CONVOQUE des OPR sans les constater, en N19 il constate « travaux
    termines » et trois reserves. L'ecart va en B ;
(d) ⚠ un compte de fichiers n'est pas un compte de choses - RECOMPTER,
    puis chercher une SECONDE source avant de publier un compte (N19 :
    neuf CR ET neuf reunions au calcul d'honoraires, donc publiable ;
    N18 : 46 fichiers numerotes 1-45 puis 49, donc AUCUN compte publie ;
    N21 : 33 CR numerotes 01 a 38, six manquants et une coquille
    d'en-tete, donc AUCUN compte publie) ;
(e) ⚠ une note ou un rapport peut ne pas boucler. La N16 en a releve
    CINQ, la N18 une, la N19 une, la N20 une. En N21 les DEUX estimations
    ET la decomposition du marche de MOE bouclaient au centime - c'est un
    resultat a consigner, pas une raison de ne plus verifier. Verifier
    que les sous-totaux somment AVANT de composer quoi que ce soit de
    proportionnel, et ne rien publier de ce qui ne boucle pas ;
(f) ⚠ verifier si le site publie DEJA quelque chose de cette affaire ou
    de ses acteurs (grep de src/content/ - PROSE, LEGENDES ET ALT DES
    CLICHES) : quatre occurrences deja (N15, N17, N19, N21), et en N21
    le grep a fourni d'un coup les graphies du MOA, de l'architecte et
    du BET structures.
Aucun numero 20-024 n'est publie (a reverifier au grep).
Dossier de travail a creer : references/ref_045/
Slug cible : a etablir au depouillement (kebab-case sans accents,
verifier qu'il n'ecrase rien).

CE QUE LES N01-N21 ONT ETABLI (verifiable au depot) :
- ⚠⚠ QUATRE REGIMES DE PROPRIETE D'UNE PIECE, a distinguer AVANT
  d'ecrire. (1) piece FT2E - elle fonde la fiche. (2) piece d'un tiers
  DEPOSEE POUR COMPARAISON (N19 : un devis concurrent dont le nom de
  fichier le faisait passer pour une etude FT2E) - elle ne se cite
  jamais. (3) piece d'un tiers COMMANDEE PAR UN TIERS (N19 : une etude
  d'impact sonore payee par l'installateur) - question a FT2E, rien
  n'est publie. (4) l'ARCHIVE DE L'OUVRAGE (N20) - le dossier de
  construction d'origine, recupere comme matiere de travail : elle se
  LIT et s'EXPLOITE, mais ni son auteur ni ses valeurs ne se publient.
  ⚠ La N21 en ajoute une CINQUIEME nuance, qui n'est pas un regime mais
  une prudence : LA PIECE DU MANDATAIRE (acte d'engagement, CCAP,
  avenants, comptes rendus de chantier - tous rediges par l'architecte).
  Elle fait foi sur le calendrier et sur les montants, mais son contenu
  se cite avec la prudence d'un CR d'OPC : c'est ainsi qu'on evite de
  publier une coquille d'en-tete. C'est l'EN-TETE ou le CARTOUCHE qui
  tranche le regime - jamais le repertoire, jamais le nom de fichier.
- ⚠⚠ UN NOM DE FICHIER MENT (N19, N20). « DESCRIPTIFS POUR CCTP 2022
  2023.docx » etait un catalogue de textes de prescription d'un
  fabricant ; « 19xxx-SUIVI.doc » un gabarit vierge de compte rendu FT2E
  dont tous les champs sont vides. OUVRIR AVANT DE CONCLURE, y compris
  les .doc (antiword, ou extraction brute des chaines).
- ⚠⚠ LE NUMERO FT2E SE RELEVE SUR PLUSIEURS PIECES, ET LA MAJORITE
  L'EMPORTE. La page de garde d'un CCTP peut porter un faux numero (N18,
  N19) ; un classeur d'honoraires interne aussi (N21 : « 19-125 », une
  occurrence contre 118). Les pieces les plus sures sont les CARTOUCHES
  DE PLANS et les pages de garde des CCTP/DPGF de PRODUCTION. Autres faux
  deja rencontres : references de modele constructeur, numeros de dossier
  des mandataires, numeros de permis, surfaces foncieres, codes postaux,
  references de coloris (N21 : « ECUME 99 50 284 »), durees de vie de LED
  et NUMEROS DE NORMES (NF X 46-020, NF S 31-010, NF C 15-100).
  ⚠ RELEVER ENSUITE TOUT `\d{2}[-\s.]\d{2,3}` DU DOSSIER ET ETABLIR, UN
  PAR UN, CE QUE CHACUN DESIGNE : 30 suites distinctes en N20, 80 en N21.
- ⚠ LE CLASSEUR PEUT ETRE EN ECART D'UN AN, ET LE CROISEMENT COMMERCIAL
  TRANCHE (N20). Il rangeait 22037 sous « Finalisees en 2022 » quand
  quatre sources disaient 2023, dont DEUX PIECES FT2E DEJA PUBLIEES : la
  plaquette 2024 (docs/20-source-plaquette-2024.md) et les CV de l'equipe
  (livrables/cv-ft2e/CV-FT2E.zip, edition aout 2026). Les interroger
  SYSTEMATIQUEMENT a l'etape 4.
  ⚠ Les onze docx sectoriels de references/docs_references/ portent
  souvent la fiche commerciale de l'affaire (N18, decisif) - mais pas
  toujours (N19, N20 et N21 : muets ; il n'existe AUCUN docx
  « Industriel »). C'est un resultat a consigner, pas un echec.
  ⚠ En revanche la N21 a trouve le propre DOSSIER DE REFERENCES
  INDUSTRIEL de FT2E (aout 2019, 14 operations avec MOA, architecte,
  montant, SHON, millesime) DANS le dossier d'affaires lui-meme, depose
  avec une candidature. CHERCHER CE GENRE DE PIECE dans 01-Commerciale :
  c'est une source commerciale de premiere main, et elle est du regime 1.
- ⚠ UN INDICE DE CONTRAT N'EST PAS UNE AFFAIRE - CINQ confirmations
  (N15, N16, N17, N19, N20). Le depart se fait sur les pieces de
  PRODUCTION, qui portent le numero SANS indice. ⚠ Et VERIFIER QUI A
  SIGNE : en N20 le contrat etait adresse au proprietaire et signe du
  cachet du SYNDIC ; en N21 l'offre de MOE est signee par le MANDATAIRE
  pour tout le groupement, FT2E n'ayant signe qu'un POUVOIR.
- ⚠ UNE MISSION PEUT ETRE SENSIBLE ET NE PAS SE PUBLIER (N20). ⚠ Et un
  OUVRAGE peut l'etre : en N21, un batiment de securite aeroportuaire -
  aucun plan, aucune implantation, aucun detail de controle d'acces ni
  d'alarme au-dela du type reglementaire, et une question E dediee.
- ⚠⚠ UNE THESE PEUT ETRE DEJA PUBLIEE - et c'est le risque PRINCIPAL,
  avec 44 planches au corpus. AVANT d'arreter une these, lire les
  `sous_titre` ET les `archetype_motif` des 44 planches
  (PYTHONIOENCODING=utf-8 python -c "..." sur
  public/images/projets/*/planche.json). La N17 a du abandonner DEUX
  theses, la N18 une, la N19 TROIS, la N20 une. La N21 a du AFFUTER la
  sienne : « une seule enveloppe, deux regimes thermiques » etait deja
  publie (habitat-inclusif-salignac) et « trois regimes d'air dans une
  meme enveloppe » aussi (siege-rese-aigrefeuille) - la these a ete
  reduite a ce que le corpus ne portait pas, le RETRAIT du perimetre de
  calcul a l'interieur du batiment. La question n'est pas « est-ce que ca
  demontre bien ? » mais « est-ce que ca demontre quelque chose que le
  corpus ne demontre pas deja ? ».
- Archetypes apres N21 : boucle-fluide 12 - coupe-traversee 10 -
  tableau-electrique 7 - sankey-energie 7 - zonage-ssi 6 -
  chronologie-affaire 2 - planche-chiffree 0 SANS module. L'archetype se
  choisit sur la THESE, jamais sur le secteur ni sur le quota, mais a
  these egale preferer ce qui n'a pas servi depuis longtemps ; la dette
  de variete porte sur boucle-fluide (12/44) et desormais aussi sur
  coupe-traversee (10/44, TROIS sessions de suite en N19, N20 et N21), et
  chronologie-affaire n'a pas servi depuis le corpus fondateur
  (admissible seulement si sa these est d'INGENIERIE, jamais le
  calendrier d'une operation). ⚠ `planche-chiffree` n'a toujours pas de
  module : si un dossier l'exige, la decision est de L'ECRIRE ou de
  retirer l'archetype de la liste fermee, jamais de bricoler.
- Un mecanisme nouveau s'ecrit DANS le compositeur d'archetype
  (constantes prefixees par le mecanisme ; garde-fou de greffe sur le
  NOM DE LA FONCTION ET sur les prefixes de constantes - automatise
  depuis la N13 : en N21, 56 fonctions et 167 constantes existantes
  contre 3 et 6 nouvelles, prefixe unique `RE_`, zero collision), et
  l'invariant octet se rejoue AVANT la greffe, APRES la greffe et APRES
  la derniere retouche. `python scripts/planches/invariant.py` couvre
  les 6 compositeurs et les 44 dossiers (176/176 au 2026-09-02).
  ⚠ Un dossier neuf dont la planche n'est pas encore composee fait
  ECHOUER l'invariant : LIRE LE DENOMINATEUR. Composer d'abord, mesurer
  ensuite.
- ⚠⚠ SEPARER LES MESURES DE L'ECHELLE DES MOTIFS (N20, reconduit en
  N21). Les trois formats partagent UNE implantation de leur primitive,
  mais les MESURES du dessin (abscisses, ordonnees, largeurs de boite)
  sont ABSOLUES et propres a chaque format, et l'echelle `ech` ne
  commande QUE les motifs et les petits accessoires (epaisseurs de
  trait, interruptions, pointes de fleche). ⚠ La N21 y ajoute une
  troisieme categorie : UN ELEMENT PEUT ETRE ABSENT D'UN FORMAT. La
  bande claire de la porte, labellisee sur la planche, paraissait sans
  son libelle sur la vignette et sur l'appui ; `porte=None` la retire de
  ces deux formats, et la primitive reste unique. C'est une mesure de
  format, pas une exception.
- ⚠ METTRE UNE ASSERTION DE DEPASSEMENT DANS LE COMPOSITEUR, SUR LES
  TROIS FORMATS, ET LA PROUVER VIVANTE. En N20 comme en N21 la
  composition est passee du premier coup : l'assertion a donc ete mise a
  l'epreuve sur QUATRE copies du planche.json portant chacune un libelle
  allonge a dessein, une par format plus une sur la bande dont la largeur
  est bornee par le bord d'un objet voisin. Les quatre ont rompu.
  UNE SONDE QUI N'A JAMAIS ECHOUE NE MESURE RIEN.
  ⚠⚠ ET SE SOUVENIR DE CE QU'ELLE NE MESURE PAS : elle teste une
  LARGEUR, jamais une OCCUPATION. La N21 en a paye DEUX en une seance -
  une fleche verticale qui traversait la ligne d'en-tete du second
  registre, puis le filet vertical qui la remplacait, qui la traversait
  aussi. Les deux ne se voient qu'au PNG.
- ⚠ REGARDER LES PNG, ET CORRIGER CE QU'ON Y VOIT. La N16 a fait CINQ
  retouches, la N17 DEUX, la N18 TROIS, la N19 QUATRE, la N20 DEUX, la
  N21 HUIT - dont trois qu'aucun controle automatique ne pouvait voir :
  un bloc a fond papier dessine APRES le trait qu'il devait marquer
  l'EFFACAIT sur sa hauteur (l'ordre de trace est un choix, pas un
  detail) ; deux collisions d'occupation avec une ligne de texte ; et un
  aplat calcaire sur fond papier qui ne se voyait pas du tout (les
  barres proportionnelles se font en aplat `clair` a filet-1, comme
  celles de sankey-energie). ⚠ Et AGRANDIR par PIL (crop + resize
  NEAREST) tout detail douteux, plutot que de plisser les yeux.
- ⚠⚠ LE BLOC `controles` D'UN planche.json EST DE LA PROSE (N20). Il est
  ecrit depuis le SOURCE PYTHON du compositeur, et les apostrophes
  droites qu'on y tape s'y retrouvent. `python
  scripts/apostrophes-planches.py` (sans argument, en MESURE) le voit :
  il a rendu « 21 apostrophes sur 2 pieces » en N20, « 0 sur 0 » en N21
  parce que les chaines ont ete ecrites courbes d'emblee. LE REJOUER
  APRES LA PREMIERE COMPOSITION, puis --appliquer si besoin, puis
  RECOMPOSER. ⚠ Les apostrophes ECHAPPEES (\') dans une f-string a
  delimiteur simple sont refusees a juste titre : la correction est de
  changer le delimiteur, pas le refus.
- ⚠⚠ LES DEUX SONDES D'ACCENTS DE LA N20, ET CE QUE LA N21 Y AJOUTE.
  (1) aucun mot ne doit paraitre en graphie NUE alors que sa graphie
  ACCENTUEE existe ailleurs dans le meme document ; (2) plancher de 2 %
  d'accents sur la PROSE GLOBALE (le compte se fait sur la forme
  DECOMPOSEE, NFD - sur une chaine NFC, comparer a sa forme nue rend
  0,00 %). Les deux se mettent a l'epreuve sur le meme texte desaccentue,
  et doivent rompre. ⚠ LA SONDE 1 SUR-TIRE, ET C'EST NORMAL : en N21 elle
  a signale « chauffe » (verbe conjugue), « cote » (la cote d'un dessin)
  et « partage » (le nom de code d'un mecanisme) - trois formes nues
  legitimes. NE PAS LA DESARMER : enumerer les exemptions AVEC LEUR
  JUSTIFICATION et asserter l'EGALITE de l'ensemble signale et de
  l'ensemble exempte, de sorte qu'une quatrieme forme nue rompe encore.
  ⚠ Et `a_valider_ft2e`, `archetype_motif` et `exclusions_appliquees`
  s'ecrivent ACCENTUES : les 44 extractions du corpus le font.
- Les insecables des heredocs bash sont normalisees DE FACON NON
  DETERMINISTE sur cette machine. DEUX VOIES, toutes deux eprouvees :
  (a) ecrire le .md en ESPACES ORDINAIRES et apostrophes droites par
  l'outil Write, puis passer `python scripts/injection-typographique.py
  <fichier>` - c'est la voie des N12 a N21, la plus sure ; (b) script
  Python avec marqueurs ASCII remplaces par chr(8239)/chr(160) et
  assertion A L'EGALITE comptee sur le source - la voie pour tout
  fichier que injection-typographique.py ne couvre pas (planche.json,
  plan du chantier, prompt de continuite).
  ⚠ CHOISIR LES MARQUEURS CONTRE LE CORPUS REEL : le seul choix sur est
  un caractere qui ne peut pas figurer dans le texte - '\x01', '\x02',
  '\x03', ecrits en ECHAPPEMENT ASCII dans le source (« # » collisionne
  avec les titres Markdown, « % » avec « 30 % »).
  ⚠⚠ UNE ANCRE DE REMPLACEMENT SE VERIFIE PAR repr(), PAS PAR DEDUCTION
  (N19, rejoue DEUX FOIS en N20). Une ancre prise dans un .md deja passe
  a injection-typographique.py peut porter une insecable invisible.
  ⚠ injection-typographique.py protege les lignes d'enum du frontmatter
  (secteur, typologie, mission_ft2e) : une apostrophe DROITE tapee dans
  mission_ft2e y RESTE et casse le build. Il NE protege PAS
  secteur_secondaire. ⚠ Il ne connait pas toutes les unites - il a appris
  « mg/L », « g/L » et « °F » en N20, et il IGNORE toujours « A »
  (amperes), « Ω » (ohms), « bars », « metres » et « litres » : la N21 a
  du poser trois insecables a la main apres son passage. CONTROLER PAR
  REGEX APRES PASSAGE (`\d[ ](?:m²|m³|mm|kW|L|A|Ω|°C|%|€|bars|W/)`).
  ⚠ Et le CORPUS peut trancher autrement que la regle : mesurer la
  graphie dominante par grep avant d'ecrire (« kWhep/m²/an » 44 fois,
  « m³/(h·m²) » 14 fois). ⚠ IL NE POSE PAS LES ACCENTS NI LES
  EXPOSANTS : ecrire « m² », « m³/h » et « °C » directement.
- ⚠ L'AGENT DE RELECTURE TROUVE DE VRAIES ERREURS DE FAIT SANS AVOIR LES
  PIECES (N15, N18, N19, N20, N21). LUI DONNER EN CONTEXTE LES FAITS
  ETABLIS SUR PIECE et lui demander EXPLICITEMENT les chaines exactes
  avant/apres - il travaille EN LECTURE SEULE, ses outils d'edition
  normalisent les insecables.
  ⚠⚠ ET LE VERIFIER, TOUJOURS : en N18 il s'est trompe une fois, en N19
  trois fois, en N20 une fois. MESURER OU RELIRE LA PIECE AVANT
  D'APPLIQUER, constat par constat.
- ⚠ LE CARTOUCHE DE RESERVE PARAIT COUPE SUR LE PNG DE CONTROLE - le
  rendu cairosvg n'a pas IBM Plex Mono et substitue une chasse ~8 % plus
  large. NE PAS « corriger » la largeur du cartouche : la formule
  `mesurer(...) + 40` est commune aux 44 planches. La N20 puis la N21
  l'ont MESURE au navigateur sur le deploiement
  (references/ref_044/sonde-cartouche.mjs) : cartouche entier, 26 puis
  22 px de marge a droite. ⚠ La N21 ajoute que cairosvg substitue AUSSI
  un ▯ aux caracteres « ≥ » et « ≤ », qui rendent parfaitement au
  navigateur (et que trois planches publiees emploient deja) : ne pas
  reecrire un libelle sur la foi du PNG.
- ⚠ NE PAS REECRIRE rendre_png.py : il est au depot depuis la N12.
  Usage : `python scripts/planches/rendre_png.py
  public/images/projets/<slug> <repertoire>`. REGARDER LES QUATRE
  controles. ⚠ Il s'appelle depuis la RACINE du depot.
- ⚠ UN HEREDOC BASH PEUT MANGER UN ANTISLASH, ECHOUER SUR UNE APOSTROPHE
  ET MANGER LES ACCENTS (N15, N16, N17, N20). Pour tout script non
  trivial : outil Write dans le SCRATCHPAD, puis execution. C'est aussi
  la regle qui evite que le hook Stop commite des scripts a usage unique.
  ⚠ ET NE JAMAIS TAPER UN CHEMIN D'ARCHIVES : les noms portent des
  accents et des apostrophes typographiques. Passer par os.walk +
  fragments de nom. Le petit module `lire.py` du scratchpad
  (trouver/un/texte/png/docx/xlsx/xls/msg sur pymupdf, zipfile, openpyxl
  et xlrd) se rejoue de session en session.
- Le hook Stop commite et pousse SEUL ce qui traine, et il PEUT
  COMMITTER LE LIVRABLE ENTIER. L'historique etant pousse sur un depot
  PARTAGE, il ne se reecrit pas. Pour l'eviter : garder les scripts a
  usage unique DANS LE SCRATCHPAD, hors depot, COMMITTER TOT des que le
  build est vert, et reserver un second commit a la passe editoriale et
  aux documents de suivi (⚠ livrables/ porte deux fichiers non suivis
  anterieurs a la N02 - les laisser).
- /references/ est gitignore (motif ancre) - les pieces sources
  n'entrent JAMAIS au depot ; npm run preview ne mesure pas la
  performance ; Chrome refuse les fenetres sous 500 px (sonde iframe).
- La planche n'expose NI le millesime d'ouverture, NI montant, NI tiers
  (MOA, mandataire, architecte, installateur, MARQUES comprises), NI
  donnee nominative ; les designations internes (reperes de zone,
  numeros de tableau, destinations de reseau, orientations, quartiers,
  niveaux, et en N21 les noms de volumes de programme « remise des
  vehicules », « rez-de-chaussee », « etage » et les usages
  reglementaires « bureaux », « logement collectif ») sont admises avec
  une entree a_valider_ft2e et une question E ; tout arbitrage de dessin
  va dans a_valider_ft2e (jamais vide).
  ⚠ ET SAVOIR CE QUE LE CORPUS A DEJA FAIT DIRE A UN SIGNE : le trait
  interrompu signifie « position abandonnee » sur la planche de la
  Maison des Metiers et « reserve pour plus tard » sur celle du groupe
  scolaire de La Flotte. Les deux sont legitimes, l'en-tete les leve a
  chaque fois - mais il faut le savoir avant d'en ajouter un troisieme.
  C'est pourquoi la N21 n'emploie AUCUN trait interrompu.

⚠ CE QUI RESTE APRES CE DOSSIER, ET L'ECART 49 / 50 TOUJOURS NON TRANCHE.
Le classeur porte, apres celui-ci : « Finalisees en 2022 » (1 : 20039
Videosurveillance CH Rochefort M), « Finalisees en 2020 » (2 : 19008
Batiment industriel Aeroport LR ELIXIR I, 20058 Diag legionelles du port
de plaisance M) et « Finalisees en 2019 » (1 : 18026 Atelier numerique
Fountaine Pajot I). Soit 1 + 2 + 1 = 4 dossiers restants pour 45 fiches
en ligne apres la N22 : LE CLASSEUR NE MENE QU'A 49, PAS A 50. La
question a ete portee aux messages finaux des N16 a N21 et N'A TOUJOURS
PAS ETE ARBITREE PAR FT2E : la reposer tant qu'elle reste ouverte. Ne pas
fabriquer une fiche pour combler l'ecart.
⚠ PISTE RELEVEE EN N17, TOUJOURS OUVERTE ET REVERIFIEE EN N21 : le
classeur porte une section « Finalisees en 2021 » qui est VIDE - en-tete
de section, en-tete de colonnes, et aucune ligne. C'est le seul millesime
sans entree, entre 2020 (2 entrees) et 2022 (4 entrees). L'hypothese a
soumettre a FT2E est qu'une affaire manque a cette section, ce qui
expliquerait l'ecart exactement. A verifier avec eux, pas a supposer.
⚠⚠ 2020.zip MANQUE SUR LE DISQUE, et la N23 est la session qui closera
la tranche 2022. LE DEMANDER A L'UTILISATEUR DES L'OUVERTURE DE LA N23 :
sans lui, la N24 n'a plus de dossier. Les ZIP presents : 2019, 2022,
2023, 2024, 2025. Le nom du ZIP suit l'annee de FINALISATION, pas celle
de l'affaire (19-087 et 20-024 sont dans 2022.zip ; 19008 et 20058
seront dans 2020.zip, 18026 dans 2019.zip).

DEROULER LE PIPELINE § 2 INTEGRALEMENT : depouillement (pdfinfo /
pdftotext, ou pymupdf via python subprocess avec les noms lus par
os.listdir ; les plans sans couche texte et les marches scannes se
lisent en rendant leurs pages en PNG par pymupdf, zoom 2-3 ; antiword
pour les .doc, xlrd pour les .xls, openpyxl pour les .xlsx,
extract-msg pour les .msg) -> CONTROLE DE LA PAGE DE GARDE DE CHAQUE
PIECE TECHNIQUE, ET DE SON REGIME DE PROPRIETE (les quatre, plus la
prudence due aux pieces du mandataire) -> releve du numero NN-NNN SUR
PLUSIEURS PIECES FT2E, et ETABLISSEMENT DE CE QUE DESIGNE CHAQUE AUTRE
SUITE `NN-NNN` DU DOSSIER -> references/ref_045/ (3 a 8 pieces) ->
croisement commercial (references/docs_references/ - docx sectoriels ET
classeur ODS - + docs/20-source-plaquette-2024.md +
livrables/cv-ft2e/CV-FT2E.zip + toute piece commerciale FT2E TROUVEE AU
DOSSIER + grep de src/content/ pour ce que le site publie deja, LEGENDES
ET ALT DES CLICHES COMPRIS) -> fiche de collecte (A/A+ remplies, B-E en
questions, ligne Secteur citant le classeur, DECISION Q3 motivee en
tete) -> LECTURE DES 44 SOUS-TITRES ET DES 44 `archetype_motif` pour
verifier qu'aucune these voisine n'est deja publiee -> fiche
src/content/projets/<slug>.md (SECTEUR RELEVE AU CLASSEUR ; taxonomie
ACTUELLE ; lieu avec code postal entre parentheses ; synthese 480-780 ;
>= 5 liens internes ; une CLAUSE DE CLOTURE en dernier paragraphe ;
jamais de numero d'affaire NI de millesime d'ouverture en prose ;
convention numerale finale - nom du NOMBRE en un seul mot en lettres,
nombre COMPOSE en chiffres, unites et mesures toujours en chiffres,
citations intouchees ; verifier par `python scripts/releve-numeral.py`,
dont la section « Nombres COMPOSES ecrits en lettres » doit rendre 0) ->
PLANCHE complete (extraction avec a_valider_ft2e non vide, apostrophes
courbes ET ACCENTS des l'ecriture, DEUX SONDES D'ACCENTS prouvees
vivantes, composition par scripts/planches/<archetype>.py avec assertion
de depassement SUR LES TROIS FORMATS, PROUVEE VIVANTE sur quatre copies,
primitives PARTAGEES et MESURES distinguees des MOTIFS, rendus par
scripts/planches/rendre_png.py depuis la RACINE, controles a 1152 /
carte 274-296 / appui 552 - REGARDER les quatre PNG, et AGRANDIR par PIL
tout detail douteux -, apostrophes-planches.py en MESURE **APRES la
premiere composition**, invariant.py, verser.py) -> qualite (typecheck 0,
build vert 68 pages, editorial-reviewer EN LECTURE SEULE, ET VERIFIER
CHACUN DE SES CONSTATS SUR LA PIECE OU PAR MESURE, controle-liens-
internes 45/45 a 5, controle-numeros-affaire 0 fuite, releve-numeral sans
ecart nouveau) -> COMMIT (content(references): ajoute la fiche reelle
<nom> et sa planche ; git ls-remote avant, depot partage) -> push (le
push deploie), curl de la fiche AVEC barre oblique finale + marqueur de
build, rendu controle aux trois bandes (references/ref_044/
sonde-fiche.mjs, slug et URL a adapter), CARTOUCHE MESURE
(sonde-cartouche.mjs, SELECTEUR A RECALER) ET CONTROLE DE L'INDEXATION
SECTORIELLE (point 6, sonde references/ref_044/sonde-filtres.mjs,
SECTEUR A RECALER, appelee DEPUIS LA RACINE) -> ligne de suivi au plan ->
PROMPT DE LA SESSION N23 en annexe du plan (script Python ou Write,
jamais un long heredoc) et reproduit integralement dans le message final.
Le prompt N23 REPREND le bloc « REGLE D'INDEXATION SECTORIELLE » tel quel
(repartition remise a jour) ET porte le DERNIER dossier de la tranche
2022 (20039 Videosurveillance CH Rochefort, classeur M). Il RAPPELLE
aussi l'ecart 49 / 50 tant qu'il n'est pas tranche, la piste de la
section « Finalisees en 2021 » vide au classeur, ET QUE 2020.zip DOIT
ETRE DEMANDE A L'UTILISATEUR DES L'OUVERTURE DE LA N23.

Portee de commit : content(references). Un changement de schema Zod
eventuel passe par le sous-agent content-modeller et va dans le MEME
commit que public/admin/config.yml.

Termine par le prompt de lancement de la session N23, en annexe du
plan du chantier et reproduit integralement dans ton message final -
la regle de continuite est dans CLAUDE.md parce qu'elle a ete manquee
deux fois.
```

## Annexe W — prompt de lancement de la session N23 (à coller tel quel en session neuve)

```
Session N23/27 - FT2E v3 : chantier des 27 nouvelles fiches references.
VINGT-TROISIEME dossier - DERNIER de la tranche « Finalisees en 2022 ».

Contexte. FT2E v3 est le site institutionnel du bureau d'etudes FT2E
(La Rochelle), Astro 6 statique, deploye en demonstration client sur
https://ft2e-v3.vercel.app (indexation verrouillee - ne pas y toucher).
Le catalogue porte 45 fiches reelles (23 + N01 a N22), chacune illustree
d'une planche de schema de principe (cinq pieces par dossier).
Objectif : 50 fiches. 1 session = 1 dossier, close par le prompt de la
suivante. LA TRANCHE 2023 EST CLOSE depuis la N19.

⚠⚠ A FAIRE DES L'OUVERTURE, AVANT TOUTE AUTRE CHOSE : DEMANDER 2020.zip
A L'UTILISATEUR. Les ZIP presents sur le disque sont 2019, 2022, 2023,
2024 et 2025. Le dossier du jour est le DERNIER de 2022.zip : sans
2020.zip, la session N24 n'a plus de dossier a traiter. Le nom du ZIP
suit l'annee de FINALISATION, pas celle de l'affaire (19008 et 20058
seront dans 2020.zip, 18026 dans 2019.zip).

LE ZIP DE LA TRANCHE 2022 EST DEJA SUR LE DISQUE :
C:\claude_code_dev_projects\ft2e_new_archives\2022.zip (663,5 Mo). Le
repertoire extrait de la N22 a ete SUPPRIME en fin de session : il n'y a
rien a nettoyer, et C:\claude_code_dev_projects\ft2e_new_archives\extrait
doit etre vide ou absent. UN SEUL dossier restant, absent du site (a
reverifier au grep de src/content/projets/*.md) :
-   29 fichiers, 38,3 Mo : « 20-039- Centre Hospitalier Rochefort-
    Video surveillance » (classeur M)  <- DOSSIER DU JOUR
IL N'Y A DONC AUCUNE QUESTION A POSER SUR LE CHOIX DU DOSSIER : derouler
directement. APRES CE DOSSIER, 2022.zip peut etre supprime du disque
(les quatre affaires de la tranche auront ete traitees) - le proposer a
l'utilisateur, ne pas le supprimer sans son accord.

Disque : 4,0 Go libres au 2026-09-02, et le dossier du jour ne pese que
38 Mo - extraire tout le repertoire 20-039 suffit. Le motif d'extraction
est zipfile.namelist() + un fragment de chemin (« 20-039 ») ; le rm -rf
est REFUSE par les permissions : passer par python shutil.rmtree.

⚠⚠ CE DOSSIER EST SENSIBLE PAR SON OBJET MEME, et c'est le troisieme du
genre. La N20 a rencontre une MISSION sensible qui ne se publie pas ; la
N21 un OUVRAGE sensible (batiment de securite aeroportuaire) et a pose
une question E dediee - aucun plan, aucune implantation, aucun detail de
controle d'acces ni d'alarme au-dela du type reglementaire. Ici les deux
se cumulent : la VIDEOSURVEILLANCE d'un CENTRE HOSPITALIER. Poser la
question E DES L'OUVERTURE de la fiche de collecte, et s'interdire par
defaut : toute implantation de camera, tout champ de vision ou angle
mort, tout plan de masse ou de niveau, toute localisation de local
technique ou d'enregistreur, tout detail de stockage, de duree de
conservation ou d'acces aux images, toute donnee nominative de patient
ou d'agent. Ce qui reste publiable est l'INGENIERIE : topologie du
reseau, alimentations, courants faibles, contraintes de site en
exploitation, exigences reglementaires generales. Si la these ne peut se
soutenir sans une de ces exclusions, LE DIRE et proposer une these
autre - ne pas contourner.

⚠ DOSSIER POTENTIELLEMENT MINCE : 29 fichiers seulement, contre 61 pour
la N22. La regle des dossiers minces (Q3) est reconduite : si la matiere
ne suffit pas a une fiche honnete, produire la COLLECTE SEULE et
proposer une substitution, en le motivant en tete de la fiche de
collecte. Mesurer avant de conclure - la N22 a produit sa DECISION Q3
sur un tableau de matiere (pieces de conception, pieces thermiques,
pieces contractuelles, suivi de chantier), pas sur une impression.

LIRE D'ABORD, dans cet ordre :
1. docs/superpowers/plans/2026-08-27-chantier-27-nouvelles-fiches.md -
   LE PLAN : § 1 (ce qui a change), § 2 (pipeline 12 etapes), § 3
   (reponses consignees Q1/Q2/Q3), § Suivi (lignes N01 a N22),
   annexe W (ce prompt).
2. docs/superpowers/plans/2026-08-07-chantier-references-reelles.md -
   § Contraintes globales + § Protocole de session + § Regle des
   dossiers minces.
3. docs/superpowers/specs/2026-08-12-planches-references-protocole.md -
   revision 5 EN ENTIER.
4. CLAUDE.md, .claude/rules/content-collections.md et french-editorial.md.
Etalons : src/content/projets/creche-oranger-perigny.md (fiche) et, pour
une affaire MONOTECHNIQUE (classeur M, une seule technique) :
audit-chauffage-sites-adei.md (21086, M simple, sept sites),
audit-chambre-des-metiers-la-rochelle.md (22037, M simple, N20),
bornes-irve-la-rochelle-saintes.md (23099, M - IRVE et non T),
cuisine-groupe-scolaire-villedoux.md et
passerelle-ecluse-carreau-d-or-marans.md (un seul lot technique).
Voir aussi public/images/projets/gaelic-innov-ia-la-rochelle/ +
references/ref_045/ (fiche de collecte N22, avec sa DECISION Q3, son
§ « LE PIEGE DU NUMERO » et son § « LES REGIMES DE PROPRIETE DES
PIECES » en tete - c'est elle qui documente le releve de 222 suites
`NN-NNN`, le numero de mandataire au format AA.NN, et la coquille de
Siret qui traverse une piece FT2E).
Les sondes de recette vivent dans references/ref_045/ : sonde-fiche.mjs,
sonde-filtres.mjs et sonde-cartouche.mjs, DEJA RECALEES SUR LA N22.
⚠ Leurs selecteurs sont EN DUR sur le texte de la fiche precedente :
sonde-cartouche cherche « LA ROCHELLE · 935 » dans le cartouche,
sonde-filtres teste le secteur « Industriel » et la page
/secteurs/industriel-commercial. LES RECALER AVANT DE CONCLURE - une
sonde qui ne trouve pas son noeud rend `null` sans echouer, et la
sonde-fiche de la N22 a rendu « largeurSvg 0 » au palier 1440 sans que
rien ne soit casse : c'etait son selecteur, pas le rendu. REGARDER LES
CAPTURES plutot que de conclure sur un chiffre de sonde.
⚠ sonde-cartouche.mjs et sonde-fiche.mjs prennent un REPERTOIRE en
argument, pas un fichier ; rendre_png.py aussi. Les trois s'appellent
DEPUIS LA RACINE du depot.

REGLE D'INDEXATION SECTORIELLE - etablie le 2026-08-27, A APPLIQUER A
LA REDACTION DE CHAQUE FICHE (etape 6 du pipeline), pas apres coup :
« REFERENCES SITE FT2E.ods » (references/docs_references/, classeur
fourni par FT2E) FAIT FOI pour le classement sectoriel. Concretement,
AVANT d'ecrire le frontmatter :
1. Ouvrir le classeur (python zipfile sur content.xml, ou pandoc) et y
   retrouver l'affaire PAR SON NUMERO (graphie sans tiret : « 20039 »).
2. En relever le domaine (legende : L Logements / T Tertiaire & ERP /
   I Industriel / P Patrimoine / C Coordination SSI /
   M Monotechnique-Audit / E EXE) -> champ `secteur`.
3. Si le classeur porte un domaine DOUBLE (« T § C ») : le premier est
   le `secteur`, le second va au champ `secteur_secondaire` (optionnel
   au schema depuis le 2026-08-27, garde-fou « doit differer ») - la
   fiche parait alors dans les deux filtres et sur les deux pages de
   secteur. Precedents : hotel-yachtman (T § C), maison-pierre-loti-
   rochefort (P § C, N04), foyer-cdair-saint-martin-de-re (T § C, N10),
   auberge-central-hostel-la-rochelle (T § C, N12),
   cabanes-urbaines-la-rochelle (T § C, N15).
   LE DOSSIER DU JOUR EST A DOMAINE SIMPLE : 20039 est « M ».
4. JAMAIS de deduction depuis le dossier, l'usage RT ou le nom de
   l'operation : la N02 penchait « Industriel » pour Fors, le classeur
   dit T - et les 25 fiches ont du etre re-referencees le soir meme
   (7 bascules, commits ce334b2/09270a3). Le classeur peut contredire
   l'intuition (Saint-Rogatien, pole commercial : I ; Fors, pole
   commercial : T ; 23083 « plan de comptage Airbus » : E et non M ;
   23099 « CPAM » : M - IRVE, pas T ; 23036 Fountaine Pajot : I SIMPLE
   alors que le CV annonce « CFO / CFA / SSI » ; 20045 « THE ROOF »,
   salle d'escalade et atelier de luthier : T § C et non I ; 21086
   « Audit chauffage sites ADEI », sept etablissements medico-sociaux :
   M SIMPLE ; 21074 « AP Yacht - CATANA Group », chantier naval : I
   SIMPLE ; 20071 « Bureaux EIFFAGE », un siege d'agence avec ses
   ateliers : T SIMPLE ; 21029 « Ecole primaire et maternelle La
   Flotte », un ERP de type R : M SIMPLE ; 22037 « Audit chambre des
   metiers » : M SIMPLE ; 19087 « Batiment SSLIA », dont le sigle
   evoque la securite incendie et le programme un ERP : I SIMPLE ;
   20024 « INNOVIA - GAELIC », un laboratoire avec 210 m2 de bureaux :
   I SIMPLE, et le depouillement a donne raison au classeur, le CCTP
   ecrivant « batiment de type industriel soumis au code du travail »)
   - il gagne. ⚠ Un centre hospitalier evoque le tertiaire/ERP : le
   classeur dit M. NE PAS LE CONTREDIRE.
5. CONSIGNER la lecture dans la fiche de collecte (ligne « Secteur » :
   citer l'entree du classeur telle quelle) ; si l'affaire est ABSENTE
   du classeur ou son domaine illisible -> question B a FT2E et choix
   provisoire argumente, jamais silencieux.
6. EN RECETTE (etape 10) : verifier sur le deploiement que la fiche
   repond au bon filtre de /references (compteurs de chips) et parait
   sur sa page /secteurs/<slug> - sondes : references/ref_045/
   sonde-filtres.mjs et references/ref_045/sonde-fiche.mjs (URL a adapter).
   ⚠ Une page /secteurs/<slug> n'affiche que les 4 affaires les plus
   recentes du secteur (tri par numero decroissant) ; le filtre de
   /references, lui, montre tout. Une affaire a DOUBLE domaine doit
   etre controlee sur LES DEUX filtres et LES DEUX pages de secteur.
   ⚠ 20-039 est un numero de 2020 et le secteur « Monotechnique —
   Audit » compte 6 fiches apres la N22 : 23-099 (bornes IRVE), 23-009
   (maisons Louise Magnan), 22-037 (Maison des Metiers), 21-086 (audit
   ADEI), 21-029 (chaufferie La Flotte) et 20-058... a reverifier au
   grep, la liste ci-dessus est indicative. 20-039 s'inserera en fin de
   tri et n'entrera vraisemblablement PAS dans le top 4 de
   /secteurs/monotechnique : c'est le tri documente, PAS un defaut, et
   le filtre de /references fait foi (la N22 a vecu exactement ce cas).
   Repartition attendue AVANT la N23, MESUREE le 2026-09-02 sur le
   deploiement par references/ref_045/sonde-filtres.mjs : L10 T14 I7 P3
   C7 M6 E3 pour 45 fiches, 50 en pondere (Yachtman T+C, Loti P+C, foyer
   CDAIR T+C, Central Hostel T+C et Cabanes Urbaines T+C comptent double).

DOSSIER DU JOUR : « 20-039- Centre Hospitalier Rochefort- Video
surveillance » (29 fichiers, 38,3 Mo), classeur « 20039 · Videosurveillance
CH Rochefort · M ». Points d'attention connus AVANT ouverture :
(a) ⚠⚠ la sensibilite de l'objet (voir plus haut) - question E des
    l'ouverture, et une these qui tienne SANS implantation ;
(b) ⚠ un CENTRE HOSPITALIER est un maitre d'ouvrage public : attendre un
    marche public, un acte d'engagement, un CCAP, un reglement de
    consultation. VERIFIER QUI A SIGNE (en N20 le contrat etait adresse
    au proprietaire et signe du cachet du syndic ; en N21 l'offre de MOE
    etait signee par le mandataire pour tout le groupement) ;
(c) ⚠ chercher la reception AUX SIX ENDROITS du protocole : un CR d'OPC
    portant « RECEPTION DES TRAVAUX » en tete (N11) ; un CR annoncant la
    reception a une date precise (N12) ; le BILAN DE FACTURATION (N12) ;
    le DERNIER CR DE CHANTIER, dont l'en-tete remplace « PROCHAINE
    REUNION » par « RECEPTION le JJ/MM/AAAA » (N13) ; LE CALENDRIER EN
    TETE DE CHAQUE CR D'OPC (N14) ; et L'EN-TETE DES DERNIERS CR (N15).
    ⚠ Constater n'est pas prononcer : en N18, N21 et N22 le dernier CR
    CONVOQUE la reception sans la constater, en N19 il constate
    « travaux termines » et trois reserves. La N22 a retenu
    `annee_livraison` sur un FAISCEAU (OPR constatee + levee de reserves
    annoncee + mission de DOE commandee + classeur), en le motivant en
    question B - c'est la methode a reprendre, pas un blanc-seing ;
(d) ⚠ un compte de fichiers n'est pas un compte de choses - RECOMPTER,
    puis chercher une SECONDE source avant de publier un compte (N19 :
    neuf CR ET neuf reunions au calcul d'honoraires, donc publiable ;
    N18 : 46 fichiers numerotes 1-45 puis 49, donc AUCUN compte publie ;
    N21 : 33 CR numerotes 01 a 38, six manquants, AUCUN compte ; N22 :
    43 fichiers numerotes 1-45, trois manquants et un « 5 bis », AUCUN
    compte - et le plan portait treize hottes que le CCTP ne chiffrait
    pas, donc treize hottes non publiees non plus) ;
(e) ⚠ une note ou un rapport peut ne pas boucler. La N16 en a releve
    CINQ, la N18 une, la N19 une, la N20 une. En N21 les deux
    estimations bouclaient ; en N22 le contrat de MOE bouclait sur les
    travaux (857 645 + 534 000 = 1 391 645) MAIS presentait DEUX ECARTS
    D'UN CENTIME sur les honoraires (arrondis de taux) - releves,
    consignes, et rien de proportionnel publie. Verifier que les
    sous-totaux somment AVANT de composer quoi que ce soit de
    proportionnel, et ne rien publier de ce qui ne boucle pas ;
(f) ⚠ verifier si le site publie DEJA quelque chose de cette affaire ou
    de ses acteurs (grep de src/content/ - PROSE, LEGENDES ET ALT DES
    CLICHES) : cinq occurrences deja (N15, N17, N19, N21, N22). En N22
    le grep a rendu bien plus qu'une graphie : la fiche publiee
    `ateliers-pilotes-capsulae` decrivait un batiment « adosse au
    batiment IDCAPS existant », rue Charles Tellier - c'est-a-dire
    EXACTEMENT le batiment que le dossier du jour restructurait. Le site
    publiait deja l'affaire sans le savoir. FAIRE CE GREP TOT, il
    change la fiche.
Aucun numero 20-039 n'est publie (a reverifier au grep).
Dossier de travail a creer : references/ref_046/
Slug cible : a etablir au depouillement (kebab-case sans accents,
verifier qu'il n'ecrase rien).

CE QUE LES N01-N22 ONT ETABLI (verifiable au depot) :
- ⚠⚠ QUATRE REGIMES DE PROPRIETE D'UNE PIECE, a distinguer AVANT
  d'ecrire. (1) piece FT2E - elle fonde la fiche. (2) piece d'un tiers
  DEPOSEE POUR COMPARAISON (N19 : un devis concurrent dont le nom de
  fichier le faisait passer pour une etude FT2E) - elle ne se cite
  jamais. (3) piece d'un tiers COMMANDEE PAR UN TIERS (N19 : une etude
  d'impact sonore payee par l'installateur) - question a FT2E, rien
  n'est publie. (4) l'ARCHIVE DE L'OUVRAGE (N20) - le dossier de
  construction d'origine, recupere comme matiere de travail : elle se
  LIT et s'EXPLOITE, mais ni son auteur ni ses valeurs ne se publient.
  ⚠ La N21 y ajoute une CINQUIEME nuance, qui n'est pas un regime mais
  une prudence : LA PIECE DU MANDATAIRE (acte d'engagement, CCAP,
  avenants, comptes rendus de chantier - tous rediges par l'architecte).
  Elle fait foi sur le calendrier et sur les montants, mais son contenu
  se cite avec la prudence d'un CR d'OPC. C'est l'EN-TETE ou le
  CARTOUCHE qui tranche le regime - jamais le repertoire, jamais le nom
  de fichier. ⚠ La N22 confirme par un cas limite : un fichier nomme
  « contrat Honoraire ENGIE AXIMA » et range dans un repertoire au nom
  de l'entreprise etait une PROPOSITION D'HONORAIRES FT2E adressee a
  cette entreprise - regime 1, pas 3. La page de garde tranche.
- ⚠⚠ UN NOM DE FICHIER MENT (N19, N20, N22). « DESCRIPTIFS POUR CCTP
  2022 2023.docx » etait un catalogue de textes de prescription d'un
  fabricant ; « 19xxx-SUIVI.doc » un gabarit vierge de compte rendu
  FT2E. OUVRIR AVANT DE CONCLURE, y compris les .doc (antiword, ou
  extraction brute des chaines).
- ⚠⚠ LE NUMERO FT2E SE RELEVE SUR PLUSIEURS PIECES, ET LA MAJORITE
  L'EMPORTE. La page de garde d'un CCTP peut porter un faux numero (N18,
  N19) ; un classeur d'honoraires interne aussi (N21 : « 19-125 », une
  occurrence contre 118). Les pieces les plus sures sont les CARTOUCHES
  DE PLANS et les pages de garde des CCTP/DPGF de PRODUCTION. Autres
  faux deja rencontres : references de modele constructeur, numeros de
  dossier des mandataires, numeros de permis, surfaces foncieres, codes
  postaux, references de coloris, durees de vie de LED et NUMEROS DE
  NORMES (NF X 46-020, NF S 31-010, NF C 15-100).
  ⚠ RELEVER ENSUITE TOUT `\d{2}[-\s.]\d{2,3}` DU DOSSIER ET ETABLIR, UN
  PAR UN, CE QUE CHACUN DESIGNE : 30 suites distinctes en N20, 80 en
  N21, 222 EN N22 - et sur ces 222, une seule etait le numero FT2E. Le
  gros du bruit venait des NUMEROS DE TELEPHONE et des DATES du tableau
  de suivi des comptes rendus (« 22/02/21-01/03/21 »), plus les COTES
  d'un plan au 1/50. Un relevé qui explose n'est pas un relevé qui
  echoue : il faut juste le classer par famille.
  ⚠ ET LE NUMERO DU MANDATAIRE EST AU FORMAT AA.NN : la N21 a trouve
  « 19.36 », la N22 « 20.02 » - ce dernier en gros sur la page de garde
  du contrat de maitrise d'oeuvre, dans son pied de page, dans le nom du
  fichier et en tete de la convention de groupement, quand « 20-024 » n'y
  figurait NULLE PART. Lire la seule piece contractuelle aurait donne un
  faux numero.
- ⚠ LE CLASSEUR PEUT ETRE EN ECART D'UN AN, ET LE CROISEMENT COMMERCIAL
  TRANCHE (N20). Interroger SYSTEMATIQUEMENT a l'etape 4 : les onze docx
  sectoriels de references/docs_references/, le classeur ODS,
  docs/20-source-plaquette-2024.md et livrables/cv-ft2e/CV-FT2E.zip.
  ⚠ Les docx portent parfois la fiche commerciale de l'affaire (N18,
  decisif) - mais pas toujours : MUETS en N19, N20, N21 ET N22, et il
  n'existe AUCUN docx « Industriel ». En N22 les CV etaient muets aussi,
  et la plaquette ne portait que le nom du client dans une liste. C'est
  un resultat a consigner, pas un echec.
  ⚠ En revanche la N21 a trouve le propre DOSSIER DE REFERENCES
  INDUSTRIEL de FT2E DANS le dossier d'affaires lui-meme, depose avec
  une candidature. CHERCHER CE GENRE DE PIECE dans 01-Commerciale.
  ⚠ ET NE PAS CONFONDRE DEUX AFFAIRES D'UN MEME CLIENT : ce dossier de
  references portait « Extension Usine INNOVIA - 5 400 000 € - SHON
  2400 m2 », chiffres qui NE correspondent PAS a l'affaire 20-024
  (934,74 m2, 1 391 645 €). C'est une autre operation du meme groupe.
- ⚠ UN INDICE DE CONTRAT N'EST PAS UNE AFFAIRE - CINQ confirmations
  (N15, N16, N17, N19, N20). Le depart se fait sur les pieces de
  PRODUCTION, qui portent le numero SANS indice.
- ⚠ UNE MISSION PEUT ETRE SENSIBLE ET NE PAS SE PUBLIER (N20). ⚠ Et un
  OUVRAGE peut l'etre (N21). ⚠ LE DOSSIER DU JOUR CUMULE LES DEUX.
- ⚠⚠ UNE THESE PEUT ETRE DEJA PUBLIEE - et c'est le risque PRINCIPAL,
  avec 45 planches au corpus. AVANT d'arreter une these, lire les
  `sous_titre` ET les `archetype_motif` des 45 planches
  (PYTHONIOENCODING=utf-8 python -c "..." sur
  public/images/projets/*/planche.json). La N17 a du abandonner DEUX
  theses, la N18 une, la N19 TROIS, la N20 une, la N21 une, la N22
  QUATRE : « une enveloppe, N systemes autonomes » etait deja publie
  (place-des-chenes-verts, siege-rese, mairie-les-portes-en-re), « une
  seule enveloppe, deux regimes thermiques » aussi
  (habitat-inclusif-salignac), « le perimetre du calcul est plus petit
  que le batiment » aussi (batiment-sslia, la fiche PRECEDENTE), et « la
  greffe sur l'usine en exploitation » aussi (extension-fountaine-pajot).
  La these retenue a ete ce qu'aucune ne portait : la NON-COINCIDENCE de
  deux decoupages tires du MEME texte - un seul usage au calcul, des
  systemes d'air separes a l'installation. La question n'est pas
  « est-ce que ca demontre bien ? » mais « est-ce que ca demontre
  quelque chose que le corpus ne demontre pas deja ? ».
- Archetypes apres N22 : boucle-fluide 12 - coupe-traversee 10 -
  sankey-energie 7 - tableau-electrique 7 - zonage-ssi 7 -
  chronologie-affaire 2 - planche-chiffree 0 SANS module. L'archetype se
  choisit sur la THESE, jamais sur le secteur ni sur le quota, mais a
  these egale preferer ce qui n'a pas servi depuis longtemps ; la dette
  de variete porte sur boucle-fluide (12/45) et coupe-traversee (10/45),
  et chronologie-affaire n'a pas servi depuis le corpus fondateur
  (admissible seulement si sa these est d'INGENIERIE, jamais le
  calendrier d'une operation). ⚠ `planche-chiffree` n'a toujours pas de
  module : si un dossier l'exige, la decision est de L'ECRIRE ou de
  retirer l'archetype de la liste fermee, jamais de bricoler.
  ⚠ ET UN ARCHETYPE SERT AU-DELA DE SON NOM : `zonage-ssi` a porte en
  N22 un decoupage THERMIQUE ET AERAULIQUE sans aucune SSI, comme il
  portait deja deux regimes reglementaires a Salignac. C'est le
  MECANISME qui commande, pas l'intitule.
- Un mecanisme nouveau s'ecrit DANS le compositeur d'archetype
  (constantes prefixees par le mecanisme ; garde-fou de greffe sur le
  NOM DE LA FONCTION ET sur les prefixes de constantes - automatise
  depuis la N13 : en N22, 33 fonctions et 103 constantes existantes
  contre 7 et 39 neuves, prefixes `DI_`/`DIV_`/`DIA_`, zero collision),
  et l'invariant octet se rejoue AVANT la greffe, APRES la greffe et
  APRES la derniere retouche. `python scripts/planches/invariant.py`
  couvre les 6 compositeurs et les 45 dossiers (180/180 au 2026-09-02).
  ⚠ Un dossier neuf dont la planche n'est pas encore composee fait
  ECHOUER l'invariant : LIRE LE DENOMINATEUR (en N22, « 176/180 » avant
  la composition signifiait « 176/176 sur l'existant », pas une
  regression). Composer d'abord, mesurer ensuite.
- ⚠⚠ SEPARER LES MESURES DE L'ECHELLE DES MOTIFS (N20, reconduit en N21
  et N22). Les trois formats partagent UNE implantation de leur
  primitive, mais les MESURES du dessin (abscisses, ordonnees, largeurs
  de boite) sont ABSOLUES et propres a chaque format. ⚠ Et UN ELEMENT
  PEUT ETRE ABSENT D'UN FORMAT : en N22 les cinq extractions, les
  exigences par element et l'article cite sont ABSENTS de la vignette et
  de l'appui, ou leurs libelles tomberaient sous le plancher de
  lisibilite. C'est une mesure de format, pas une exception - et elle se
  CONSIGNE dans le bloc `controles` du format concerne.
  ⚠ ET LES LIBELLES SE DECLINENT PAR FORMAT : la N22 porte
  `libelle` (planche, 15 px), `libelle_court` (appui, mono 10) et
  `libelle_vignette` (vignette, mono 9) - « Laboratoire restructure »,
  « LABORATOIRE », « LABO ». Un seul libelle pour trois formats deborde.
- ⚠ METTRE UNE ASSERTION DE DEPASSEMENT DANS LE COMPOSITEUR, SUR LES
  TROIS FORMATS, ET LA PROUVER VIVANTE. En N20, N21 et N22 la
  composition est passee du premier coup : l'assertion a donc ete mise a
  l'epreuve sur QUATRE copies du planche.json portant chacune un libelle
  allonge a dessein - une par format, plus une sur une largeur bornee
  par LE BORD DE LA COLONNE VOISINE et non par la marge. Les quatre ont
  rompu. UNE SONDE QUI N'A JAMAIS ECHOUE NE MESURE RIEN.
  ⚠⚠ ET SE SOUVENIR DE CE QU'ELLE NE MESURE PAS : elle teste une
  LARGEUR, jamais une OCCUPATION, jamais un ORDRE DE TRACE. La N21 en a
  paye deux en occupation ; la N22 en a paye une en ORDRE : le trait de
  frontiere, trace AVANT la bande, etait integralement EFFACE par le
  fond opaque des cases. Aucun controle automatique ne le voit - seul le
  PNG. C'est le meme piege qu'en N21, et il s'est represente.
- ⚠ REGARDER LES PNG, ET CORRIGER CE QU'ON Y VOIT. La N16 a fait CINQ
  retouches, la N17 DEUX, la N18 TROIS, la N19 QUATRE, la N20 DEUX, la
  N21 HUIT, la N22 TROIS : l'ordre de trace (ci-dessus), un appui qui
  laissait 100 px de marge basse et flottait en haut de son format, et
  une insecable FINE en grand corps qui disparaissait a l'oeil.
  ⚠ SUR CE DERNIER POINT, LE TRONC TRANCHE : `NN` (U+202F) pour le texte
  courant et le mono, `INS` (U+00A0) pour les chiffres en GRAND CORPS -
  et le corpus fait `.replace(INS, NN)` sur la vignette et l'appui, ou
  les corps sont plus petits. Le suivre.
  ⚠ Et AGRANDIR par PIL (crop + resize NEAREST) tout detail douteux,
  plutot que de plisser les yeux.
- ⚠⚠ LE BLOC `controles` D'UN planche.json EST DE LA PROSE (N20). Il est
  ecrit depuis le SOURCE PYTHON du compositeur, et les apostrophes
  droites qu'on y tape s'y retrouvent. `python
  scripts/apostrophes-planches.py` (sans argument, en MESURE) le voit :
  21 apostrophes sur 2 pieces en N20, 0 en N21, 93 SUR 2 PIECES EN N22
  (83 dans le planche.json ecrit a la main, 10 dans le code greffe). LE
  REJOUER APRES LA PREMIERE COMPOSITION, puis --appliquer si besoin,
  puis RECOMPOSER, puis remesurer jusqu'a 0.
- ⚠⚠ LES DEUX SONDES D'ACCENTS. (1) aucun mot ne doit paraitre en
  graphie NUE alors que sa graphie ACCENTUEE existe ailleurs dans le
  meme document ; (2) plancher de 2 % d'accents sur la PROSE GLOBALE (le
  compte se fait sur la forme DECOMPOSEE, NFD - sur une chaine NFC,
  comparer a sa forme nue rend 0,00 %). Les deux se mettent a l'epreuve
  et doivent rompre : la sonde 2 sur une desaccentuation TOTALE, la
  sonde 1 sur une desaccentuation PARTIELLE (sur un texte entierement
  desaccentue, la sonde 1 ne trouve plus aucune graphie accentuee et ne
  peut plus signaler - elle rendrait un faux vert).
  ⚠ LA SONDE 1 SUR-TIRE, ET C'EST NORMAL : en N21 elle a signale
  « chauffe », « cote » et « partage » ; en N22 « marques », « porte »,
  « reference », « reste » et « touche » - verbes conjugues, homographes,
  et le NOM D'UN CHAMP Zod, qui s'ecrit sans accent par convention de
  code. NE PAS LA DESARMER : enumerer les exemptions AVEC LEUR
  JUSTIFICATION VERIFIEE SUR PIECE, et asserter l'EGALITE de l'ensemble
  signale et de l'ensemble exempte, de sorte qu'une forme nue de plus
  rompe encore ET qu'une exemption morte rompe aussi.
  ⚠ Et `a_valider_ft2e`, `archetype_motif` et `exclusions_appliquees`
  s'ecrivent ACCENTUES : les 45 extractions du corpus le font.
- Les insecables des heredocs bash sont normalisees DE FACON NON
  DETERMINISTE sur cette machine. DEUX VOIES, toutes deux eprouvees :
  (a) ecrire le .md en ESPACES ORDINAIRES et apostrophes droites par
  l'outil Write, puis passer `python scripts/injection-typographique.py
  <fichier>` - c'est la voie des N12 a N22, la plus sure ; (b) script
  Python avec marqueurs ASCII remplaces par chr(8239)/chr(160) et
  assertion A L'EGALITE comptee sur le source - la voie pour tout
  fichier que injection-typographique.py ne couvre pas (planche.json,
  plan du chantier, prompt de continuite).
  ⚠⚠ ET L'ASSERTION DOIT ETRE CALCULEE, PAS TAPEE : en N22 le compte
  ecrit a la main (12) etait faux (17), et c'est l'assertion qui l'a
  arrete. Compter les marqueurs sur le source AVANT substitution
  (`ligne.count(MARQUEUR)`) plutot que d'annoncer un nombre.
  ⚠ CHOISIR LES MARQUEURS CONTRE LE CORPUS REEL : le seul choix sur est
  un caractere qui ne peut pas figurer dans le texte - '\x01', '\x02',
  '\x03', ecrits en ECHAPPEMENT ASCII dans le source (« # » collisionne
  avec les titres Markdown, « % » avec « 30 % »).
  ⚠⚠ ET DANS UNE LIGNE DE TABLEAU MARKDOWN, AUCUNE BARRE VERTICALE
  NON ECHAPPEE : la N22 a d'abord cite le classeur « 20024 | INNOVIA |
  I » dans la colonne Notes, ce qui faisait 10 barres au lieu de 8 et
  cassait le tableau. Le corpus cite avec des POINTS MEDIANS
  (« 19087 · Batiment SSLIA · I ») - le suivre, et compter les barres
  apres ecriture.
  ⚠⚠ UNE ANCRE DE REMPLACEMENT SE VERIFIE PAR repr(), PAS PAR DEDUCTION
  (N19, rejoue DEUX FOIS en N20 et UNE FOIS en N22). Une ancre prise
  dans un texte deja passe a injection-typographique.py peut porter une
  insecable invisible.
  ⚠ injection-typographique.py protege les lignes d'enum du frontmatter
  (secteur, typologie, mission_ft2e) : une apostrophe DROITE tapee dans
  mission_ft2e y RESTE et casse le build. Il NE protege PAS
  secteur_secondaire. ⚠ Il ne connait pas toutes les unites - il ignore
  « A » (amperes), « Ω » (ohms), « bars », « metres » et « litres » : la
  N21 a du poser trois insecables a la main, la N22 une (« 13 bars »).
  CONTROLER PAR REGEX APRES PASSAGE
  (`\d[ ](?:m²|m³|mm|kW|L|A|Ω|°C|%|€|bars|W/)`).
  ⚠ IL NE POSE NI LES ACCENTS NI LES EXPOSANTS NI LES LIGATURES : ecrire
  « m² », « m³/h », « °C » et « œuvre » directement. La N22 a d'abord
  redige tout un recit SANS ACCENTS en croyant que le script les
  poserait - il a fallu tout reecrire.
  ⚠ Et le CORPUS peut trancher autrement que la regle : mesurer la
  graphie dominante par grep avant d'ecrire (« kWhep/m²/an » 44 fois,
  « m³/(h·m²) » 14 fois, fine insecable devant « bars » 4 fois sur 5).
- ⚠ L'AGENT DE RELECTURE TROUVE DE VRAIES ERREURS DE FAIT SANS AVOIR LES
  PIECES (N15, N18, N19, N20, N21). LUI DONNER EN CONTEXTE LES FAITS
  ETABLIS SUR PIECE et lui demander EXPLICITEMENT les chaines exactes
  avant/apres - il travaille EN LECTURE SEULE, ses outils d'edition
  normalisent les insecables.
  ⚠⚠ ET LE VERIFIER, TOUJOURS : en N18 il s'est trompe une fois, en N19
  trois fois, en N20 une fois. MESURER OU RELIRE LA PIECE AVANT
  D'APPLIQUER, constat par constat.
- ⚠ LE CARTOUCHE DE RESERVE PARAIT COUPE SUR LE PNG DE CONTROLE - le
  rendu cairosvg n'a pas IBM Plex Mono et substitue une chasse ~8 % plus
  large. NE PAS « corriger » la largeur du cartouche : la formule
  `mesurer(...) + 40` est commune aux 45 planches. Les N20, N21 et N22
  l'ont MESURE au navigateur sur le deploiement
  (references/ref_045/sonde-cartouche.mjs) : cartouche entier, 26 puis
  22 puis 18 px de marge a droite. ⚠ cairosvg substitue AUSSI un ▯ aux
  caracteres « ≥ » et « ≤ », qui rendent parfaitement au navigateur (la
  N22 en a quatre sur sa planche) : ne pas reecrire un libelle sur la
  foi du PNG.
- ⚠ NE PAS REECRIRE rendre_png.py : il est au depot depuis la N12.
  Usage : `python scripts/planches/rendre_png.py
  public/images/projets/<slug> <repertoire>`. REGARDER LES QUATRE
  controles. ⚠ Il s'appelle depuis la RACINE du depot. ⚠ ET LE REJOUER
  APRES LA DERNIERE RETOUCHE : en N22 le planche.png publie a failli
  rester en retard d'une version sur les SVG.
- ⚠ UN HEREDOC BASH PEUT MANGER UN ANTISLASH, ECHOUER SUR UNE APOSTROPHE
  ET MANGER LES ACCENTS (N15, N16, N17, N20). Pour tout script non
  trivial : outil Write dans le SCRATCHPAD, puis execution. C'est aussi
  la regle qui evite que le hook Stop commite des scripts a usage unique.
  ⚠ ET NE JAMAIS TAPER UN CHEMIN D'ARCHIVES : les noms portent des
  accents et des apostrophes typographiques. Passer par os.walk +
  fragments de nom. Le petit module `lire.py` du scratchpad
  (trouver/un/texte/png/docx/xlsx/xls/msg sur pymupdf, zipfile, openpyxl
  et xlrd) se rejoue de session en session. ⚠ Et un PDF SCANNE n'a pas
  de couche texte : la N22 a du rendre les 15 pages du contrat de MOE en
  PNG par pymupdf (zoom 2) et les lire a l'oeil - c'est la seule voie.
- Le hook Stop commite et pousse SEUL ce qui traine, et il PEUT
  COMMITTER LE LIVRABLE ENTIER. L'historique etant pousse sur un depot
  PARTAGE, il ne se reecrit pas. Pour l'eviter : garder les scripts a
  usage unique DANS LE SCRATCHPAD, hors depot, COMMITTER TOT des que le
  build est vert, et reserver un second commit a la passe editoriale et
  aux documents de suivi (⚠ livrables/ porte deux fichiers non suivis
  anterieurs a la N02 - les laisser). ⚠ `git add` par CHEMINS EXPLICITES,
  jamais `git add -A`.
- /references/ est gitignore (motif ancre) - les pieces sources
  n'entrent JAMAIS au depot ; npm run preview ne mesure pas la
  performance ; Chrome refuse les fenetres sous 500 px (sonde iframe).
- La planche n'expose NI le millesime d'ouverture, NI montant, NI tiers
  (MOA, mandataire, architecte, installateur, MARQUES comprises), NI
  donnee nominative ; les designations internes (reperes de zone,
  numeros de tableau, destinations de reseau, orientations, quartiers,
  niveaux, noms de volumes de programme et usages reglementaires) sont
  admises avec une entree a_valider_ft2e et une question E ; tout
  arbitrage de dessin va dans a_valider_ft2e (jamais vide).
  ⚠ ET SAVOIR CE QUE LE CORPUS A DEJA FAIT DIRE A UN SIGNE : le trait
  interrompu signifie « position abandonnee » sur la planche de la
  Maison des Metiers et « reserve pour plus tard » sur celle du groupe
  scolaire de La Flotte. Les deux sont legitimes, l'en-tete les leve a
  chaque fois - mais il faut le savoir avant d'en ajouter un troisieme.
  C'est pourquoi les N21 et N22 n'emploient AUCUN trait interrompu : la
  N22 dit l'isolement par des marques SEPAREES et l'appartenance par un
  trait CONTINU, ce qui ne demande aucune convention nouvelle.

⚠ CE QUI RESTE APRES CE DOSSIER, ET L'ECART 49 / 50 TOUJOURS NON TRANCHE.
Le classeur porte, apres celui-ci : « Finalisees en 2020 » (2 : 19008
Batiment industriel Aeroport LR ELIXIR I, 20058 Diag legionelles du port
de plaisance M) et « Finalisees en 2019 » (1 : 18026 Atelier numerique
Fountaine Pajot I). Soit 3 dossiers restants pour 46 fiches en ligne
apres la N23 : LE CLASSEUR NE MENE QU'A 49, PAS A 50. La question a ete
portee aux messages finaux des N16 a N22 et N'A TOUJOURS PAS ETE
ARBITREE PAR FT2E : la reposer tant qu'elle reste ouverte. Ne pas
fabriquer une fiche pour combler l'ecart.
⚠ PISTE RELEVEE EN N17, TOUJOURS OUVERTE ET REVERIFIEE EN N22 : le
classeur porte une section « Finalisees en 2021 » qui est VIDE - en-tete
de section, en-tete de colonnes, et aucune ligne. C'est le seul millesime
sans entree, entre 2020 (2 entrees) et 2022 (4 entrees). L'hypothese a
soumettre a FT2E est qu'une affaire manque a cette section, ce qui
expliquerait l'ecart exactement. A verifier avec eux, pas a supposer.

DEROULER LE PIPELINE § 2 INTEGRALEMENT : depouillement (pdfinfo /
pdftotext, ou pymupdf via python subprocess avec les noms lus par
os.listdir ; les plans sans couche texte et les marches scannes se
lisent en rendant leurs pages en PNG par pymupdf, zoom 2-3 ; antiword
pour les .doc, xlrd pour les .xls, openpyxl pour les .xlsx,
extract-msg pour les .msg) -> CONTROLE DE LA PAGE DE GARDE DE CHAQUE
PIECE TECHNIQUE, ET DE SON REGIME DE PROPRIETE (les quatre, plus la
prudence due aux pieces du mandataire) -> releve du numero NN-NNN SUR
PLUSIEURS PIECES FT2E, et ETABLISSEMENT DE CE QUE DESIGNE CHAQUE AUTRE
SUITE `NN-NNN` DU DOSSIER -> references/ref_046/ (3 a 8 pieces) ->
croisement commercial (references/docs_references/ - docx sectoriels ET
classeur ODS - + docs/20-source-plaquette-2024.md +
livrables/cv-ft2e/CV-FT2E.zip + toute piece commerciale FT2E TROUVEE AU
DOSSIER + grep de src/content/ pour ce que le site publie deja, LEGENDES
ET ALT DES CLICHES COMPRIS) -> fiche de collecte (A/A+ remplies, B-E en
questions dont la QUESTION E DE SENSIBILITE, ligne Secteur citant le
classeur, DECISION Q3 motivee en tete) -> LECTURE DES 45 SOUS-TITRES ET
DES 45 `archetype_motif` pour verifier qu'aucune these voisine n'est
deja publiee -> fiche src/content/projets/<slug>.md (SECTEUR RELEVE AU
CLASSEUR ; taxonomie ACTUELLE ; lieu avec code postal entre parentheses ;
synthese 480-780 ; >= 5 liens internes ; une CLAUSE DE CLOTURE en dernier
paragraphe ; jamais de numero d'affaire NI de millesime d'ouverture en
prose ; ACCENTS, EXPOSANTS ET LIGATURES ECRITS A LA MAIN ; convention
numerale finale - nom du NOMBRE en un seul mot en lettres, nombre
COMPOSE en chiffres, unites et mesures toujours en chiffres, citations
intouchees ; verifier par `python scripts/releve-numeral.py`, dont la
section « Nombres COMPOSES ecrits en lettres » doit rendre 0) ->
PLANCHE complete (extraction avec a_valider_ft2e non vide, apostrophes
courbes ET ACCENTS des l'ecriture, DEUX SONDES D'ACCENTS prouvees
vivantes, composition par scripts/planches/<archetype>.py avec assertion
de depassement SUR LES TROIS FORMATS, PROUVEE VIVANTE sur quatre copies,
primitives PARTAGEES, MESURES distinguees des MOTIFS et LIBELLES
DECLINES PAR FORMAT, rendus par scripts/planches/rendre_png.py depuis la
RACINE, controles a 1152 / carte 274-296 / appui 552 - REGARDER les
quatre PNG, VERIFIER L'ORDRE DE TRACE, et AGRANDIR par PIL tout detail
douteux -, apostrophes-planches.py en MESURE **APRES la premiere
composition** puis jusqu'a 0, invariant.py, verser.py) -> qualite
(typecheck 0, build vert 69 pages, editorial-reviewer EN LECTURE SEULE,
ET VERIFIER CHACUN DE SES CONSTATS SUR LA PIECE OU PAR MESURE,
controle-liens-internes 46/46 a 5, controle-numeros-affaire 0 fuite,
releve-numeral sans ecart nouveau) -> COMMIT (content(references):
ajoute la fiche reelle <nom> et sa planche ; git ls-remote avant, depot
partage, `git add` par chemins explicites) -> push (le push deploie),
curl de la fiche AVEC barre oblique finale + marqueur de build, rendu
controle aux trois bandes (references/ref_045/sonde-fiche.mjs, slug et
URL a adapter), CARTOUCHE MESURE (sonde-cartouche.mjs, SELECTEUR A
RECALER) ET CONTROLE DE L'INDEXATION SECTORIELLE (point 6, sonde
references/ref_045/sonde-filtres.mjs, SECTEUR A RECALER, appelee DEPUIS
LA RACINE) -> ligne de suivi au plan -> PROMPT DE LA SESSION N24 en
annexe du plan (script Python ou Write, jamais un long heredoc) et
reproduit integralement dans le message final.
Le prompt N24 REPREND le bloc « REGLE D'INDEXATION SECTORIELLE » tel quel
(repartition remise a jour) ET porte le PREMIER dossier de la tranche
2020 (19008 Batiment industriel Aeroport LR ELIXIR, classeur I, ou 20058
Diag legionelles du port de plaisance, classeur M - le mieux documente
d'abord). Il RAPPELLE aussi l'ecart 49 / 50 tant qu'il n'est pas tranche,
et la piste de la section « Finalisees en 2021 » vide au classeur.

Portee de commit : content(references). Un changement de schema Zod
eventuel passe par le sous-agent content-modeller et va dans le MEME
commit que public/admin/config.yml.

Termine par le prompt de lancement de la session N24, en annexe du
plan du chantier et reproduit integralement dans ton message final -
la regle de continuite est dans CLAUDE.md parce qu'elle a ete manquee
deux fois.
```

## Annexe X — prompt de lancement de la session N24 (à coller tel quel en session neuve)

```
Session N24/27 - FT2E v3 : chantier des 27 nouvelles fiches references.
VINGT-QUATRIEME dossier - LE DERNIER QUI SOIT ATTEIGNABLE, et le seul de la
tranche « Finalisees en 2019 ».

Contexte. FT2E v3 est le site institutionnel du bureau d'etudes FT2E
(La Rochelle), Astro 6 statique, deploye en demonstration client sur
https://ft2e-v3.vercel.app (indexation verrouillee - ne pas y toucher).
Le catalogue porte 46 fiches reelles (23 + N01 a N23), chacune illustree
d'une planche de schema de principe (cinq pieces par dossier).
1 session = 1 dossier, close par le prompt de la suivante. LES TRANCHES
2022, 2023, 2024 ET 2025 SONT TOUTES CLOSES.

⚠⚠⚠ CE QUI A CHANGE EN N23, ET QUI COMMANDE TOUTE LA SUITE DU CHANTIER

2020.zip N'EXISTE PAS. La question a ete posee a l'utilisateur en ouverture
de la N23, comme le prompt le demandait, et la reponse a ete : « Il n'existe
pas / je ne l'ai pas ». Ce n'est donc pas un oubli de livraison, c'est une
absence a constater.

MESURE FAITE EN N23 SUR LES CINQ ZIP DU DISQUE (zipfile.namelist(), tous
les dossiers de tous les millesimes) :

    2019.zip   1 dossier    18-026 Atelier numerique Fountaine Pajot   <- RESTE
    2022.zip   4 dossiers   19-087, 20-024, 20-039, 22-037             tous traites
    2023.zip   5 dossiers   20-045, 20-071, 21-029, 21-074, 21-086     tous traites
    2024.zip   5 dossiers   19-110, 20-031, 21-093, 21-095, 23-036     tous traites
    2025.zip  10 dossiers   dont 23-075 deja publie (ref_001)          tous traites

IL RESTE DONC UN SEUL DOSSIER ATTEIGNABLE SUR TOUT LE DISQUE, celui du jour.
Et 19008 (« Batiment industriel Aeroport LR ELIXIR », classeur I) comme 20058
(« Diag legionelles du port de plaisance », classeur M) ne sont dans AUCUN
ZIP present : ils etaient attendus dans 2020.zip. Verifie par grep de
'19-008', '20-058', '19008', '20058' sur les namelist() des cinq archives :
zero occurrence.

⚠⚠ L'ECART N'EST DONC PLUS 49 / 50, IL EST 47 / 50. Apres la fiche du jour
le catalogue portera 47 fiches et LE CHANTIER N'AURA PLUS DE MATIERE.
C'est un fait nouveau, plus grave que l'ecart signale depuis la N16, et il
FAUT LE PORTER A L'UTILISATEUR DES L'OUVERTURE, avec les trois voies
possibles - sans en choisir une seule :
  (a) FT2E fournit 2020.zip s'il existe ailleurs (2 dossiers -> 49) ;
  (b) FT2E fournit d'autres dossiers hors classeur (le classeur n'a jamais
      mene qu'a 49, l'objectif de 50 n'a jamais ete couvert) ;
  (c) le chantier se clot a 47 et l'objectif est revu - c'est une decision
      de FT2E, pas une decision de session.
⚠ NE PAS FABRIQUER DE FICHE POUR COMBLER L'ECART. La regle tient depuis la
N16 et elle tient encore.
⚠ PISTE TOUJOURS OUVERTE, REVERIFIEE EN N23 : le classeur porte une section
« Finalisees en 2021 » qui est VIDE - en-tete de section, en-tete de
colonnes, et aucune ligne. C'est le seul millesime sans entree, entre 2020
(2 entrees) et 2022 (4 entrees). L'hypothese a soumettre a FT2E est qu'une
ou plusieurs affaires manquent a cette section. A verifier avec eux, pas a
supposer.

LES ZIP SONT SUR LE DISQUE : C:\claude_code_dev_projects\ft2e_new_archives\
Le repertoire extrait de la N23 a ete SUPPRIME en fin de session : il n'y a
rien a nettoyer, et ...\extrait doit etre vide ou absent. 2022.zip A ETE
SUPPRIME EN FIN DE N23 avec l'accord de l'utilisateur, ses quatre affaires
etant toutes traitees. NE PAS SUPPRIMER 2019.zip AVANT D'AVOIR FINI - c'est
la seule source du dossier du jour ; le proposer ensuite.
Disque : 4,6 Go libres au 2026-09-03, apres suppression de 2022.zip. Le dossier du jour pese 38,8 Mo -
extraire tout le repertoire 18-026 suffit. Le motif d'extraction est
zipfile.namelist() + un fragment de chemin (« 18-026 ») ; le rm -rf est
REFUSE par les permissions : passer par python shutil.rmtree.

DOSSIER DU JOUR : « 18-026 -Atelier numerique Fountaine Pajot -ASP »
(2019.zip, 46 fichiers, 38,8 Mo), classeur « 18026 · Atelier numerique
fountaine Pajot · I ». Structure relevee au namelist() en N23 :

     7 fichiers   01-Commerciale
     1 fichier    03-Production/06-Pro
    14 fichiers   03-Production/06-Pro/2018-06-22 PDF
    24 fichiers   03-Production/12-Det/CR de Chantier

Points d'attention connus AVANT ouverture :

(a) ⚠⚠ MEME CLIENT QU'UNE FICHE DEJA PUBLIEE, ET CE N'EST PAS LA MEME
    AFFAIRE. Le site publie deja `extension-fountaine-pajot-aigrefeuille`
    (23-036, « Extension du batiment industriel 5-8 de Fountaine Pajot,
    Aigrefeuille-d'Aunis », N14, secteur Industriel, archetype
    tableau-electrique, mecanisme `greffe`). Le dossier du jour est
    l'ATELIER NUMERIQUE du meme constructeur naval, affaire 18-026, six ans
    plus tot. C'est exactement le piege de la N21 (deux affaires d'un meme
    groupe confondues sur un dossier de references) et celui de la N23
    (Marius Lacroix a La Rochelle contre le CH de Rochefort). LIRE LA FICHE
    N14 AVANT D'OUVRIR LE DOSSIER, et ne rien lui emprunter.
    ⚠ Le corpus porte aussi `ap-yacht-marans` (21-074, groupe Catana) et
    `atelier-dufour-yachts-perigny` : TROIS chantiers navals sont deja
    publies. La these devra se distinguer des trois.
(b) ⚠ 24 COMPTES RENDUS DE CHANTIER dans un sous-repertoire dedie - c'est
    la matiere principale du dossier, et c'est un piege a compter. Regle (d)
    ci-dessous : RECOMPTER, puis chercher une SECONDE source avant de
    publier un compte. La N21 avait 33 CR numerotes 01 a 38 (six manquants,
    aucun compte publie), la N22 43 fichiers numerotes 1-45 avec un
    « 5 bis », la N23 trois CR sans trou MAIS un contrat qui n'en finançait
    que deux par site - le rapprochement des deux sources est ce qui a rendu
    le fait publiable.
(c) ⚠ « 2018-06-22 PDF » est un repertoire de DIFFUSION date : 14 pieces
    rendues le meme jour. C'est probablement le rendu PRO. Verifier la page
    de garde de chacune - la N19, la N20 et la N22 ont toutes trouve au
    moins un nom de fichier qui mentait.
(d) ⚠ 01-Commerciale ne porte que 7 pieces : y chercher le contrat
    d'honoraires FT2E, et le DOSSIER DE REFERENCES du bureau (la N21 y a
    trouve le propre dossier de references industriel de FT2E, depose avec
    une candidature - et il portait des chiffres d'une AUTRE affaire du meme
    groupe).
(e) ⚠ chercher la reception AUX SIX ENDROITS du protocole : un CR d'OPC
    portant « RECEPTION DES TRAVAUX » en tete (N11) ; un CR annoncant la
    reception a une date precise (N12) ; le BILAN DE FACTURATION (N12) ; le
    DERNIER CR DE CHANTIER, dont l'en-tete remplace « PROCHAINE REUNION »
    par « RECEPTION le JJ/MM/AAAA » (N13) ; LE CALENDRIER EN TETE DE CHAQUE
    CR D'OPC (N14) ; et L'EN-TETE DES DERNIERS CR (N15). Avec 24 CR, le
    dernier est la piece a lire en premier.
    ⚠ Constater n'est pas prononcer : en N18, N21 et N22 le dernier CR
    CONVOQUE la reception sans la constater ; en N19 il constate « travaux
    termines » et trois reserves ; en N23 AUCUNE piece ne la prononce et
    `annee_livraison` a ete retenu sur un FAISCEAU DE QUATRE (classeur FT2E,
    planning d'execution, delai contractuel borne, avancement du dernier CR),
    motive en question B. C'est la methode a reprendre, pas un blanc-seing.
(f) ⚠ une note ou un rapport peut ne pas boucler. La N16 en a releve CINQ,
    la N18 une, la N19 une, la N20 une, la N22 DEUX ECARTS D'UN CENTIME sur
    des arrondis de taux. En N23 TOUT bouclait, et c'est ce qui a rendu les
    faits publiables : les deux contrats d'honoraires (3 802 + 4 838 =
    8 640 EUR HT) egalaient PHASE PAR PHASE le calcul interne de 108 h a
    80 EUR/h, et le marche (67 156,44) sommait ses quatre PSE moins une
    variante en MOINS-VALUE, comme il sommait ses deux cotraitants
    (29 071,28 + 38 085,16). Verifier que les sous-totaux somment AVANT de
    composer quoi que ce soit de proportionnel.
(g) ⚠⚠ FAIRE LE GREP DE src/content/ TOT, IL CHANGE LA FICHE. Six sessions
    sur sept l'ont constate (N15, N17, N19, N21, N22, N23). En N22 le site
    decrivait deja, sans le savoir, le batiment que le dossier du jour
    restructurait. En N23 `expertises/electricite` et `secteurs/monotechnique`
    annoncaient DEJA une videosurveillance hospitaliere pour le meme maitre
    d'ouvrage, sans aucune fiche pour l'etayer - la fiche du jour leur a
    donne leur reference, et ces deux pages ont fourni ses liens internes les
    plus naturels. Greper la PROSE, LES LEGENDES ET LES ALT DES CLICHES.
(h) ⚠ le classeur porte des coquilles : « Batiment » y est ecrit avec un
    trema, « legionelles » en « legonielles », « Fountaine » en minuscule.
    Ne pas recopier une graphie du classeur dans une fiche : il fait foi sur
    le SECTEUR, pas sur l'orthographe.
Aucun numero 18-026 n'est publie (a reverifier au grep).
Dossier de travail a creer : references/ref_047/
Slug cible : a etablir au depouillement (kebab-case sans accents, verifier
qu'il n'ecrase rien - et qu'il ne se confond pas avec
`extension-fountaine-pajot-aigrefeuille`).

LIRE D'ABORD, dans cet ordre :
1. docs/superpowers/plans/2026-08-27-chantier-27-nouvelles-fiches.md -
   LE PLAN : § 1 (ce qui a change), § 2 (pipeline 12 etapes), § 3
   (reponses consignees Q1/Q2/Q3), § Suivi (lignes N01 a N23),
   annexe X (ce prompt).
2. docs/superpowers/plans/2026-08-07-chantier-references-reelles.md -
   § Contraintes globales + § Protocole de session + § Regle des
   dossiers minces.
3. docs/superpowers/specs/2026-08-12-planches-references-protocole.md -
   revision 5 EN ENTIER.
4. CLAUDE.md, .claude/rules/content-collections.md et french-editorial.md.
Etalons : src/content/projets/creche-oranger-perigny.md (fiche) et, pour le
secteur INDUSTRIEL : extension-fountaine-pajot-aigrefeuille.md (23-036, le
MEME CLIENT - a lire pour s'en distinguer), ap-yacht-marans.md (21-074,
chantier naval), atelier-dufour-yachts-perigny.md, batiment-voltaero-saint-
agnant.md, gaelic-innov-ia-la-rochelle.md (20-024, I simple) et
batiment-sslia-aeroport-la-rochelle.md (19-087, I simple).
Voir aussi public/images/projets/videosurveillance-centre-hospitalier-
rochefort/ + references/ref_046/ (fiche de collecte N23, avec sa DECISION Q3,
son § « LE PIEGE DU NUMERO », son § « LES REGIMES DE PROPRIETE DES PIECES »
et sa QUESTION E.0 DE SENSIBILITE en tete - c'est elle qui documente le
releve de 70 suites `NN-NNN`, la SIXIEME confirmation qu'un indice n'est pas
une affaire, et le triple bouclage des honoraires).
Les sondes de recette vivent dans references/ref_046/ : sonde-fiche.mjs,
sonde-filtres.mjs et sonde-cartouche.mjs, DEJA RECALEES SUR LA N23.
⚠ Leurs selecteurs sont EN DUR sur le texte de la fiche precedente :
sonde-cartouche cherche « ROCHEFORT · DEUX SITES » dans le cartouche,
sonde-filtres teste le secteur « Monotechnique — Audit » et la page
/secteurs/monotechnique. LES RECALER AVANT DE CONCLURE - et le garde-fou
anti-residu de la N23 (aucune chaine de la session precedente ne doit
survivre dans le fichier recale) merite d'etre rejoue.
⚠ sonde-fiche a ete REPAREE en N23 : elle rendait « largeurSvg 0 » depuis
la N22 parce que son selecteur prenait le PREMIER svg de la page, or la
fiche INLINE les trois formats et n'en montre qu'un - les deux autres
mesurent 0. Elle prend desormais LE PLUS LARGE DES SVG VISIBLES et publie
son viewBox : « largeurSvg 1150, format 0 0 1200 800 » est la reponse juste.
UNE SONDE QUI REND 0 NE MESURE RIEN - mais REGARDER LES CAPTURES reste la
regle, c'est la capture qui a montre que le rendu etait sain.
⚠ sonde-cartouche.mjs et sonde-fiche.mjs prennent un REPERTOIRE en argument,
pas un fichier ; rendre_png.py aussi. Les trois s'appellent DEPUIS LA RACINE
du depot.

REGLE D'INDEXATION SECTORIELLE - etablie le 2026-08-27, A APPLIQUER A
LA REDACTION DE CHAQUE FICHE (etape 6 du pipeline), pas apres coup :
« REFERENCES SITE FT2E.ods » (references/docs_references/, classeur
fourni par FT2E) FAIT FOI pour le classement sectoriel. Concretement,
AVANT d'ecrire le frontmatter :
1. Ouvrir le classeur (python zipfile sur content.xml, ou pandoc) et y
   retrouver l'affaire PAR SON NUMERO (graphie sans tiret : « 18026 »).
2. En relever le domaine (legende : L Logements / T Tertiaire & ERP /
   I Industriel / P Patrimoine / C Coordination SSI /
   M Monotechnique-Audit / E EXE) -> champ `secteur`.
3. Si le classeur porte un domaine DOUBLE (« T § C ») : le premier est
   le `secteur`, le second va au champ `secteur_secondaire` (optionnel
   au schema depuis le 2026-08-27, garde-fou « doit differer ») - la
   fiche parait alors dans les deux filtres et sur les deux pages de
   secteur. Precedents : hotel-yachtman (T § C), maison-pierre-loti-
   rochefort (P § C, N04), foyer-cdair-saint-martin-de-re (T § C, N10),
   auberge-central-hostel-la-rochelle (T § C, N12),
   cabanes-urbaines-la-rochelle (T § C, N15).
   LE DOSSIER DU JOUR EST A DOMAINE SIMPLE : 18026 est « I ».
4. JAMAIS de deduction depuis le dossier, l'usage RT ou le nom de
   l'operation : la N02 penchait « Industriel » pour Fors, le classeur
   dit T - et les 25 fiches ont du etre re-referencees le soir meme
   (7 bascules, commits ce334b2/09270a3). Le classeur peut contredire
   l'intuition (Saint-Rogatien, pole commercial : I ; Fors, pole
   commercial : T ; 23083 « plan de comptage Airbus » : E et non M ;
   23099 « CPAM » : M - IRVE, pas T ; 23036 Fountaine Pajot : I SIMPLE
   alors que le CV annonce « CFO / CFA / SSI » ; 20045 « THE ROOF »,
   salle d'escalade et atelier de luthier : T § C et non I ; 21086
   « Audit chauffage sites ADEI », sept etablissements medico-sociaux :
   M SIMPLE ; 21074 « AP Yacht - CATANA Group », chantier naval : I
   SIMPLE ; 20071 « Bureaux EIFFAGE », un siege d'agence avec ses
   ateliers : T SIMPLE ; 21029 « Ecole primaire et maternelle La
   Flotte », un ERP de type R : M SIMPLE ; 22037 « Audit chambre des
   metiers » : M SIMPLE ; 19087 « Batiment SSLIA », dont le sigle
   evoque la securite incendie et le programme un ERP : I SIMPLE ;
   20024 « INNOVIA - GAELIC », un laboratoire avec 210 m2 de bureaux :
   I SIMPLE ; 20039 « Videosurveillance CH Rochefort », un centre
   hospitalier qui evoque le tertiaire et l'ERP : M SIMPLE, et la page
   /secteurs/monotechnique rangeait DEJA la videosurveillance dans son
   champ couvert - le classeur avait raison avant le depouillement)
   - il gagne. ⚠ « Atelier numerique » evoque le tertiaire ou le
   numerique : le classeur dit I. NE PAS LE CONTREDIRE.
5. CONSIGNER la lecture dans la fiche de collecte (ligne « Secteur » :
   citer l'entree du classeur telle quelle, AVEC DES POINTS MEDIANS et
   jamais avec des barres verticales - une barre non echappee casse la
   ligne de tableau, releve en N22) ; si l'affaire est ABSENTE du
   classeur ou son domaine illisible -> question B a FT2E et choix
   provisoire argumente, jamais silencieux.
6. EN RECETTE (etape 10) : verifier sur le deploiement que la fiche
   repond au bon filtre de /references (compteurs de chips) et parait
   sur sa page /secteurs/<slug> - sondes : references/ref_046/
   sonde-filtres.mjs et references/ref_046/sonde-fiche.mjs (URL a adapter).
   ⚠ Une page /secteurs/<slug> n'affiche que les 4 affaires les plus
   recentes du secteur (tri par numero decroissant) ; le filtre de
   /references, lui, montre tout. Une affaire a DOUBLE domaine doit
   etre controlee sur LES DEUX filtres et LES DEUX pages de secteur.
   ⚠ 18-026 est le PLUS ANCIEN NUMERO DE TOUT LE CATALOGUE et le secteur
   « Industriel » compte 7 fiches apres la N23 : il s'inserera en fin de
   tri et n'entrera PAS dans le top 4 de /secteurs/industriel-commercial.
   C'est le tri documente, PAS un defaut, et le filtre de /references fait
   foi (les N22 et N23 ont vecu exactement ce cas).
   Repartition attendue AVANT la N24, MESUREE le 2026-09-03 sur le
   deploiement par references/ref_046/sonde-filtres.mjs : L10 T14 I7 P3
   C7 M7 E3 pour 46 fiches, 51 en pondere (Yachtman T+C, Loti P+C, foyer
   CDAIR T+C, Central Hostel T+C et Cabanes Urbaines T+C comptent double).
   Apres la N24, « Industriel » doit passer de 7 a 8.

CE QUE LES N01-N23 ONT ETABLI (verifiable au depot) :
- ⚠⚠ QUATRE REGIMES DE PROPRIETE D'UNE PIECE, a distinguer AVANT
  d'ecrire. (1) piece FT2E - elle fonde la fiche. (2) piece d'un tiers
  DEPOSEE POUR COMPARAISON (N19 : un devis concurrent dont le nom de
  fichier le faisait passer pour une etude FT2E) - elle ne se cite
  jamais. (3) piece d'un tiers COMMANDEE PAR UN TIERS (N19 : une etude
  d'impact sonore payee par l'installateur) - question a FT2E, rien
  n'est publie. (4) l'ARCHIVE DE L'OUVRAGE (N20) - le dossier de
  construction d'origine, recupere comme matiere de travail : elle se
  LIT et s'EXPLOITE, mais ni son auteur ni ses valeurs ne se publient.
  ⚠ La N21 y ajoute une CINQUIEME nuance, qui n'est pas un regime mais
  une prudence : LA PIECE DU MANDATAIRE (acte d'engagement, CCAP,
  avenants, comptes rendus de chantier - tous rediges par l'architecte).
  Elle fait foi sur le calendrier et sur les montants, mais son contenu
  se cite avec la prudence d'un CR d'OPC. C'est l'EN-TETE ou le
  CARTOUCHE qui tranche le regime - jamais le repertoire, jamais le nom
  de fichier. ⚠ La N22 confirme par un cas limite : un fichier nomme
  « contrat Honoraire ENGIE AXIMA » et range dans un repertoire au nom
  de l'entreprise etait une PROPOSITION D'HONORAIRES FT2E adressee a
  cette entreprise - regime 1, pas 3. La page de garde tranche.
  ⚠ La N23 ajoute le cas INVERSE et il est structurant : quand le lot est
  UNIQUE et la mission prise EN DIRECT du maitre d'ouvrage, il n'y a
  AUCUN mandataire - les comptes rendus de chantier sont alors des pieces
  FT2E de plein exercice, pas des pieces a citer avec precaution. Etablir
  qui redige AVANT de decider comment citer.
- ⚠⚠ UN NOM DE FICHIER MENT (N19, N20, N22, N23). « DESCRIPTIFS POUR CCTP
  2022 2023.docx » etait un catalogue de textes de prescription d'un
  fabricant ; « 19xxx-SUIVI.doc » un gabarit vierge de compte rendu
  FT2E ; « contrat Honoraire Video CH Rochefort - Indice A.doc » etait
  une PROPOSITION FT2E dans une revision anterieure. OUVRIR AVANT DE
  CONCLURE, y compris les .doc (antiword, ou extraction brute des
  chaines - le module `lire.py` du scratchpad fait les deux).
- ⚠⚠ LE NUMERO FT2E SE RELEVE SUR PLUSIEURS PIECES, ET LA MAJORITE
  L'EMPORTE. La page de garde d'un CCTP peut porter un faux numero (N18,
  N19) ; un classeur d'honoraires interne aussi (N21 : « 19-125 », une
  occurrence contre 118). Les pieces les plus sures sont les CARTOUCHES
  DE PLANS et les pages de garde des CCTP/DPGF de PRODUCTION.
  ⚠ RELEVER ENSUITE TOUT `\d{2}[-\s.]\d{2,3}` DU DOSSIER ET ETABLIR, UN
  PAR UN, CE QUE CHACUN DESIGNE : 30 suites distinctes en N20, 80 en
  N21, 222 en N22, 70 en N23 - et sur ces 70, `20-039` seul comptait
  28 occurrences sur 10 pieces, sans aucun faux concurrent, le releve le
  plus net depuis la N19. Les familles de bruit sont toujours les memes :
  TELEPHONES, NUMEROS DE NORMES (11-801, 15-100, 99-001, 95-73), COTES ET
  ALTIMETRIES DE PLAN, SUITES DE REPERES CONSECUTIFS, DATES et MONTANTS.
  Un releve qui explose n'echoue pas : il faut le classer par famille.
  ⚠ ET LE NUMERO DU MANDATAIRE EST AU FORMAT AA.NN : la N21 a trouve
  « 19.36 », la N22 « 20.02 » - ce dernier en gros sur la page de garde
  du contrat de maitrise d'oeuvre quand « 20-024 » n'y figurait NULLE
  PART. Lire la seule piece contractuelle aurait donne un faux numero.
- ⚠ UN INDICE DE CONTRAT N'EST PAS UNE AFFAIRE - SIX confirmations
  (N15, N16, N17, N19, N20, N23). La N23 est la plus nette : DEUX
  contrats `20-039A` (gerontologie) et `20-039B` (hopital), plus un
  fichier « Indice A », pour UNE SEULE affaire 20-039 - et la page 2 de
  chaque contrat portait « Affaire N° 20-039 » sans lettre. Un
  depouillement qui aurait cru la page de garde aurait cree deux fiches.
  Le depart se fait sur les pieces de PRODUCTION, qui portent le numero
  SANS indice.
- ⚠ UNE MISSION PEUT ETRE SENSIBLE ET NE PAS SE PUBLIER (N20). ⚠ Un
  OUVRAGE peut l'etre (N21). ⚠ La N23 cumulait les deux (videosurveillance
  d'un centre hospitalier) et a etabli LA METHODE : poser la question E
  DES L'OUVERTURE de la collecte, lister les exclusions dans un tableau,
  puis CHOISIR LA THESE SUR CE CRITERE - la these retenue etait la seule
  des quatre candidates a ne demander AUCUNE exclusion. Une these qui ne
  peut se soutenir qu'en contournant une exclusion se remplace, elle ne
  se negocie pas.
- ⚠⚠ UNE THESE PEUT ETRE DEJA PUBLIEE - et c'est le risque PRINCIPAL,
  avec 46 planches au corpus. AVANT d'arreter une these, lire les
  `sous_titre` ET les `archetype_motif` des 46 planches
  (PYTHONIOENCODING=utf-8 python -c "..." sur
  public/images/projets/*/planche.json). La N17 a du abandonner DEUX
  theses, la N18 une, la N19 TROIS, la N20 une, la N21 une, la N22
  QUATRE, la N23 TROIS : « le chevauchement des deux systemes » recoupait
  le site occupe de Marennes et l'irreversibilite de La Flotte, « la
  redondance en couches » etait un inventaire et non un mecanisme, et
  « deux distances qui ne se confondent pas » etait la non-coincidence
  deja publiee par GAELIC. La question n'est pas « est-ce que ca demontre
  bien ? » mais « est-ce que ca demontre quelque chose que le corpus ne
  demontre pas deja ? ».
- Archetypes apres N23 : boucle-fluide 12 - coupe-traversee 10 -
  zonage-ssi 8 - sankey-energie 7 - tableau-electrique 7 -
  chronologie-affaire 2 - planche-chiffree 0 SANS module. L'archetype se
  choisit sur la THESE, jamais sur le secteur ni sur le quota, mais a
  these egale preferer ce qui n'a pas servi depuis longtemps ; la dette
  de variete porte sur boucle-fluide (12/46) et coupe-traversee (10/46),
  et chronologie-affaire n'a pas servi depuis le corpus fondateur
  (admissible seulement si sa these est d'INGENIERIE, jamais le
  calendrier d'une operation). ⚠ `planche-chiffree` n'a toujours pas de
  module : si un dossier l'exige, la decision est de L'ECRIRE ou de
  retirer l'archetype de la liste fermee, jamais de bricoler.
  ⚠ ET UN ARCHETYPE SERT AU-DELA DE SON NOM : `zonage-ssi` a porte en
  N22 un decoupage THERMIQUE ET AERAULIQUE sans aucune SSI, et en N23 la
  GRADATION D'UNE GRANDEUR CONTINUE (une densite de pixels) par trois
  seuils - toujours aucune SSI. C'est le MECANISME qui commande (une
  bande partagee par des frontieres), pas l'intitule.
- Un mecanisme nouveau s'ecrit DANS le compositeur d'archetype
  (constantes prefixees par le mecanisme ; garde-fou de greffe sur le
  NOM DE LA FONCTION ET sur les prefixes de constantes - automatise
  depuis la N13 : en N23, 40 fonctions et 142 constantes existantes
  contre 3 et 24 neuves, prefixes `GR_`/`GRV_`/`GRA_`, zero collision),
  et l'invariant octet se rejoue AVANT la greffe, APRES la greffe et
  APRES la derniere retouche. `python scripts/planches/invariant.py`
  couvre les 6 compositeurs et les 46 dossiers (184/184 au 2026-09-03).
  ⚠ Un dossier neuf dont la planche n'est pas encore composee fait
  ECHOUER l'invariant : LIRE LE DENOMINATEUR (en N23, « 180/184 » avant
  la composition signifiait « 180/180 sur l'existant », pas une
  regression). Composer d'abord, mesurer ensuite.
- ⚠⚠ SEPARER LES MESURES DE L'ECHELLE DES MOTIFS (N20, reconduit en N21,
  N22 et N23). Les trois formats partagent UNE implantation de leur
  primitive, mais les MESURES du dessin (abscisses, ordonnees, largeurs
  de boite) sont ABSOLUES et propres a chaque format. ⚠ Et UN ELEMENT
  PEUT ETRE ABSENT D'UN FORMAT : en N23 les quatre types de materiel,
  les en-tetes de registre et le chemin de retour sont ABSENTS de la
  vignette, et les portees d'illuminateur comme les details d'emploi sont
  absents de l'appui. C'est une mesure de format, pas une exception - et
  elle se CONSIGNE dans le bloc `controles` du format concerne.
  ⚠ ET LES LIBELLES SE DECLINENT PAR FORMAT : la N23 porte `libelle`
  (planche, 15 px), `libelle_court` (appui, Archivo 13), `libelle_vignette`
  (vignette, Archivo 12) et `optique`/`optique_courte` - « Surveillance
  generale », « SURVEILLANCE », « VOIR ». Un seul libelle pour trois
  formats deborde.
- ⚠ METTRE UNE ASSERTION DE DEPASSEMENT DANS LE COMPOSITEUR, SUR LES
  TROIS FORMATS, ET LA PROUVER VIVANTE. En N20, N21, N22 et N23 la
  composition est passee du premier coup : l'assertion a donc ete mise a
  l'epreuve sur QUATRE copies du planche.json portant chacune un libelle
  allonge a dessein - une par format, plus une sur une largeur bornee
  par LE BORD DE LA COLONNE VOISINE et non par la marge. Les quatre ont
  rompu (4/4 en N23). ⚠ ET ELLE A RATTRAPE UNE VRAIE ERREUR EN N23 : une
  borne posee sur une abscisse de colonne (`GR_T_X0`) refusait un libelle
  qui tenait, parce que sur la ligne des en-tetes la contrainte reelle est
  la LARGEUR MESUREE DE L'EN-TETE VOISIN. Une borne se CALCULE, elle ne
  se lit pas sur une constante de colonne.
  ⚠⚠ ET SE SOUVENIR DE CE QU'ELLE NE MESURE PAS : elle teste une
  LARGEUR, jamais une OCCUPATION, jamais un ORDRE DE TRACE. La N21 en a
  paye deux en occupation ; la N22 en a paye une en ORDRE (un trait de
  frontiere trace AVANT la bande, integralement EFFACE par le fond opaque
  des cases). Aucun controle automatique ne le voit - seul le PNG.
- ⚠ REGARDER LES PNG, ET CORRIGER CE QU'ON Y VOIT. La N16 a fait CINQ
  retouches, la N17 DEUX, la N18 TROIS, la N19 QUATRE, la N20 DEUX, la
  N21 HUIT, la N22 TROIS, la N23 DEUX - et la seconde a corrige la
  premiere : une legende de dessin posee en bas de planche se lisait
  comme la legende du chemin de retour ; deplacee juste sous ce qu'elle
  explique, elle le jouxtait encore ; elle a fini EN EN-TETE DE REGISTRE,
  au-dessus de sa colonne. UNE RETOUCHE PEUT DEPLACER LE DEFAUT AU LIEU
  DE LE CORRIGER : re-rendre et re-regarder apres chaque retouche.
  ⚠ ET AGRANDIR PAR PIL (crop + resize NEAREST) TOUT DETAIL DOUTEUX,
  plutot que de plisser les yeux - et MESURER quand l'oeil ne tranche
  pas : la N23 a compte les colonnes sombres d'un temoin dense pour
  etablir qu'il restait une TRAME (77 sombres / 77 claires) et n'etait
  pas devenu un APLAT, ce qui aurait ete faux visuellement.
  ⚠ SUR LES INSECABLES, LE TRONC TRANCHE : `NN` (U+202F) pour le texte
  courant et le mono, `INS` (U+00A0) pour les chiffres en GRAND CORPS.
  44 des 46 planche.json portent des fines ; celui de GAELIC (N22) n'en
  porte AUCUNE - c'est une anomalie de cette session, pas la regle.
- ⚠⚠ LE BLOC `controles` D'UN planche.json EST DE LA PROSE (N20). Il est
  ecrit depuis le SOURCE PYTHON du compositeur, et les apostrophes
  droites qu'on y tape s'y retrouvent. `python
  scripts/apostrophes-planches.py` (sans argument, en MESURE) le voit :
  21 apostrophes sur 2 pieces en N20, 0 en N21, 93 sur 2 pieces en N22,
  10 sur 2 pieces en N23 (5 dans le planche.json, 5 dans le code greffe).
  LE REJOUER APRES LA PREMIERE COMPOSITION, puis --appliquer si besoin,
  puis RECOMPOSER, puis remesurer jusqu'a 0.
- ⚠⚠ LES DEUX SONDES D'ACCENTS. (1) aucun mot ne doit paraitre en
  graphie NUE alors que sa graphie ACCENTUEE existe ailleurs dans le
  meme document ; (2) plancher de 2 % d'accents sur la PROSE GLOBALE (le
  compte se fait sur la forme DECOMPOSEE, NFD - sur une chaine NFC,
  comparer a sa forme nue rend 0,00 %). Les deux se mettent a l'epreuve
  et doivent rompre : la sonde 2 sur une desaccentuation TOTALE, la
  sonde 1 sur une desaccentuation PARTIELLE (sur un texte entierement
  desaccentue, la sonde 1 ne trouve plus aucune graphie accentuee et ne
  peut plus signaler - elle rendrait un faux vert). Mesures N23 : 4,31 %
  sur la fiche, 3,87 % sur l'extraction.
  ⚠ LA SONDE 1 SUR-TIRE, ET C'EST NORMAL : en N21 « chauffe », « cote »,
  « partage » ; en N22 « marques », « porte », « reference », « reste »,
  « touche » ; en N23 « des »/« des », « ferme »/« ferme »,
  « intitule »/« intitule », « mesure »/« mesure », « porte »/« porte ».
  NE PAS LA DESARMER : enumerer les exemptions AVEC LEUR JUSTIFICATION
  VERIFIEE SUR PIECE, et asserter l'EGALITE de l'ensemble signale et de
  l'ensemble exempte.
  ⚠⚠ ET PORTER CETTE EGALITE SUR L'UNION DES PIECES, PAS SUR CHACUNE :
  la N23 a d'abord asserte piece par piece et l'assertion a rompu sur
  19 exemptions parfaitement vivantes, utiles au planche.json mais
  « mortes » vues de la seule fiche. La premiere redaction en portait 23,
  la mesure en a garde 5.
  ⚠ Et `a_valider_ft2e`, `archetype_motif` et `exclusions_appliquees`
  s'ecrivent ACCENTUES : les 46 extractions du corpus le font.
- Les insecables des heredocs bash sont normalisees DE FACON NON
  DETERMINISTE sur cette machine. DEUX VOIES, toutes deux eprouvees :
  (a) ecrire le .md en ESPACES ORDINAIRES et apostrophes droites par
  l'outil Write, puis passer `python scripts/injection-typographique.py
  <fichier>` - c'est la voie des N12 a N23, la plus sure ; (b) script
  Python avec marqueurs ASCII remplaces par chr(8239)/chr(160) et
  assertion A L'EGALITE comptee sur le source - la voie pour tout
  fichier que injection-typographique.py ne couvre pas (planche.json,
  plan du chantier, prompt de continuite).
  ⚠⚠ ET L'ASSERTION DOIT ETRE CALCULEE, PAS TAPEE. En N22 le compte
  ecrit a la main (12) etait faux (17). En N23 elle a rattrape DEUX
  pieges d'un coup : `json.dumps` ECHAPPE les caracteres de controle
  meme sous `ensure_ascii=False` (le marqueur \x01 ressort en SIX
  caracteres « \u0001 », et c'est sur cette forme qu'il faut compter),
  et une fine deja ecrite en clair dans l'aria_label faussait le total.
  Compter les marqueurs sur le source APRES serialisation, et ajouter
  les insecables preexistantes.
  ⚠ CHOISIR LES MARQUEURS CONTRE LE CORPUS REEL : le seul choix sur est
  un caractere qui ne peut pas figurer dans le texte - '\x01', '\x02',
  '\x03', ecrits en ECHAPPEMENT ASCII dans le source (« # » collisionne
  avec les titres Markdown, « % » avec « 30 % »).
  ⚠⚠ ET DANS UNE LIGNE DE TABLEAU MARKDOWN, AUCUNE BARRE VERTICALE
  NON ECHAPPEE : la N22 a d'abord cite le classeur « 20024 | INNOVIA |
  I » dans la colonne Notes, ce qui faisait 10 barres au lieu de 8 et
  cassait le tableau. Le corpus cite avec des POINTS MEDIANS
  (« 20039 · Videosurveillance CH Rochefort · M ») - le suivre, et
  ASSERTER le compte de barres contre la ligne precedente (la N23 le
  fait : 8 barres, comme la N22).
  ⚠⚠ UNE ANCRE DE REMPLACEMENT SE VERIFIE PAR repr(), PAS PAR DEDUCTION
  (N19, rejoue DEUX FOIS en N20, UNE FOIS en N22). Une ancre prise dans
  un texte deja passe a injection-typographique.py porte des insecables
  invisibles. ⚠ LA N23 DONNE LA PARADE GENERALE : construire l'ancre en
  REGEX ou chaque espace vaut `[ \u202f\u00a0]`, et asserter UNE
  occurrence. 22 corrections editoriales ont ete appliquees ainsi, sans
  un seul echec d'ancre.
  ⚠ injection-typographique.py protege les lignes d'enum du frontmatter
  (secteur, typologie, mission_ft2e) : une apostrophe DROITE tapee dans
  mission_ft2e y RESTE et casse le build. Il NE protege PAS
  secteur_secondaire. ⚠ Il ne connait pas toutes les unites - il ignore
  « A », « Ω », « bars », « metres », « litres », et aussi « px/ml »,
  « MP », « MHz », « Gb/s », « To », « Mo », « AWG », « mA » (releve en
  N23). CONTROLER PAR REGEX APRES PASSAGE et poser les fines manquantes
  par script, avec assertion calculee.
  ⚠ IL NE POSE NI LES ACCENTS NI LES EXPOSANTS NI LES LIGATURES : ecrire
  « m² », « m³/h », « °C » et « œuvre » directement. La N22 a d'abord
  redige tout un recit SANS ACCENTS en croyant que le script les
  poserait - il a fallu tout reecrire.
- ⚠ L'AGENT DE RELECTURE TROUVE DE VRAIES ERREURS DE FAIT SANS AVOIR LES
  PIECES (N15, N18, N19, N20, N21, N23). LUI DONNER EN CONTEXTE LES FAITS
  ETABLIS SUR PIECE et lui demander EXPLICITEMENT les chaines exactes
  avant/apres - il travaille EN LECTURE SEULE, ses outils d'edition
  normalisent les insecables.
  ⚠⚠ ET LE VERIFIER, TOUJOURS, CONSTAT PAR CONSTAT : en N18 il s'est
  trompe une fois, en N19 trois fois, en N20 une fois, en N22 quatre fois
  sur vingt, EN N23 SIX FOIS SUR VINGT-TROIS - il a demande de retirer
  « logiciel dedie », « alimentation redondante », les trois pieces du
  dossier prefectoral, « en presence du maitre d'ouvrage et de la
  maitrise d'oeuvre » et HUIT assertions qu'il croyait non sourcees : les
  quinze etaient LITTERALES dans le CCTP ou la proposition d'honoraires.
  La parade est un script qui cherche chaque assertion contestee dans le
  texte des pieces et imprime TROUVE / ABSENT avant toute correction.
  ⚠ Ses constats de LANGUE, eux, ont ete bons a 100 % sur trois sessions.
- ⚠ LE CARTOUCHE DE RESERVE PARAIT COUPE SUR LE PNG DE CONTROLE - le
  rendu cairosvg n'a pas IBM Plex Mono et substitue une chasse ~8 % plus
  large. NE PAS « corriger » la largeur du cartouche : la formule
  `mesurer(...) + 40` est commune aux 46 planches. Les N20 a N23 l'ont
  MESURE au navigateur (references/ref_046/sonde-cartouche.mjs) :
  cartouche entier, 26 puis 22 puis 18 puis 19 px de marge a droite.
  ⚠ cairosvg substitue AUSSI un ▯ aux caracteres « ≥ » et « ≤ », qui
  rendent parfaitement au navigateur : ne pas reecrire un libelle sur la
  foi du PNG.
- ⚠ NE PAS REECRIRE rendre_png.py : il est au depot depuis la N12.
  Usage : `python scripts/planches/rendre_png.py
  public/images/projets/<slug> <repertoire>`. REGARDER LES QUATRE
  controles. ⚠ Il s'appelle depuis la RACINE du depot. ⚠ ET LE REJOUER
  APRES LA DERNIERE RETOUCHE : en N22 le planche.png publie a failli
  rester en retard d'une version sur les SVG, et en N23 un rendu lance
  avant une recomposition a bel et bien produit des PNG perimes - c'est
  la sortie du compositeur, pas celle de rendre_png.py, qui dit si la
  composition a reussi.
- ⚠ UN HEREDOC BASH PEUT MANGER UN ANTISLASH, ECHOUER SUR UNE APOSTROPHE
  ET MANGER LES ACCENTS (N15, N16, N17, N20). Pour tout script non
  trivial : outil Write dans le SCRATCHPAD, puis execution. C'est aussi
  la regle qui evite que le hook Stop commite des scripts a usage unique.
  ⚠ ET NE JAMAIS TAPER UN CHEMIN D'ARCHIVES : les noms portent des
  accents et des apostrophes typographiques. Passer par os.walk +
  fragments de nom. Le petit module `lire.py` du scratchpad
  (trouver/un/texte/png/doc/xlsx/xls/msg sur pymupdf, zipfile, openpyxl,
  xlrd et antiword) se rejoue de session en session. ⚠ Et un PDF SCANNE
  n'a pas de couche texte : la N22 a du rendre 15 pages en PNG par
  pymupdf (zoom 2) et les lire a l'oeil, la N23 trois bons de commande -
  c'est la seule voie, et elle a livre en N23 les deux imputations
  budgetaires du maitre d'ouvrage, introuvables ailleurs.
- Le hook Stop commite et pousse SEUL ce qui traine, et il PEUT
  COMMITTER LE LIVRABLE ENTIER. L'historique etant pousse sur un depot
  PARTAGE, il ne se reecrit pas. Pour l'eviter : garder les scripts a
  usage unique DANS LE SCRATCHPAD, hors depot, COMMITTER TOT des que le
  build est vert, et reserver un second commit a la passe editoriale et
  aux documents de suivi (⚠ livrables/ porte deux fichiers non suivis
  anterieurs a la N02 - les laisser). ⚠ `git add` par CHEMINS EXPLICITES,
  jamais `git add -A`.
- /references/ est gitignore (motif ancre) - les pieces sources
  n'entrent JAMAIS au depot ; npm run preview ne mesure pas la
  performance ; Chrome refuse les fenetres sous 500 px (sonde iframe).
- La planche n'expose NI le millesime d'ouverture, NI montant, NI tiers
  (MOA, mandataire, architecte, installateur, MARQUES comprises), NI
  donnee nominative ; les designations internes (reperes de zone,
  numeros de tableau, destinations de reseau, orientations, quartiers,
  niveaux, noms de volumes de programme et usages reglementaires) sont
  admises avec une entree a_valider_ft2e et une question E ; tout
  arbitrage de dessin va dans a_valider_ft2e (jamais vide - 8 entrees en
  N23).
  ⚠ ET SAVOIR CE QUE LE CORPUS A DEJA FAIT DIRE A UN SIGNE : le trait
  interrompu signifie « position abandonnee » sur la planche de la
  Maison des Metiers et « reserve pour plus tard » sur celle du groupe
  scolaire de La Flotte. Les deux sont legitimes, l'en-tete les leve a
  chaque fois - mais il faut le savoir avant d'en ajouter un troisieme.
  Les N21, N22 et N23 n'emploient AUCUN trait interrompu.

DEROULER LE PIPELINE § 2 INTEGRALEMENT : depouillement (pdfinfo /
pdftotext, ou pymupdf via python subprocess avec les noms lus par
os.listdir ; les plans sans couche texte et les marches scannes se
lisent en rendant leurs pages en PNG par pymupdf, zoom 2-3 ; antiword
pour les .doc, xlrd pour les .xls, openpyxl pour les .xlsx,
extract-msg pour les .msg) -> CONTROLE DE LA PAGE DE GARDE DE CHAQUE
PIECE TECHNIQUE, ET DE SON REGIME DE PROPRIETE (les quatre, plus la
prudence due aux pieces du mandataire, plus le cas « lot unique, mission
en direct, pas de mandataire ») -> releve du numero NN-NNN SUR PLUSIEURS
PIECES FT2E, et ETABLISSEMENT DE CE QUE DESIGNE CHAQUE AUTRE SUITE
`NN-NNN` DU DOSSIER -> references/ref_047/ (3 a 8 pieces) -> croisement
commercial (references/docs_references/ - docx sectoriels ET classeur ODS
- + docs/20-source-plaquette-2024.md + livrables/cv-ft2e/CV-FT2E.zip +
toute piece commerciale FT2E TROUVEE AU DOSSIER + grep de src/content/
pour ce que le site publie deja, LEGENDES ET ALT DES CLICHES COMPRIS)
-> fiche de collecte (A/A+ remplies, B-E en questions, ligne Secteur
citant le classeur en POINTS MEDIANS, DECISION Q3 motivee en tete) ->
LECTURE DES 46 SOUS-TITRES ET DES 46 `archetype_motif` pour verifier
qu'aucune these voisine n'est deja publiee -> fiche
src/content/projets/<slug>.md (SECTEUR RELEVE AU CLASSEUR ; taxonomie
ACTUELLE ; lieu avec code postal entre parentheses ; synthese 480-780 ;
>= 5 liens internes ; une CLAUSE DE CLOTURE en dernier paragraphe ;
jamais de numero d'affaire NI de millesime d'ouverture en prose ;
ACCENTS, EXPOSANTS ET LIGATURES ECRITS A LA MAIN ; convention numerale
finale - nom du NOMBRE en un seul mot en lettres, nombre COMPOSE en
chiffres, unites et mesures toujours en chiffres, citations intouchees ;
verifier par `python scripts/releve-numeral.py`, dont la section
« Nombres COMPOSES ecrits en lettres » doit rendre 0) -> PLANCHE
complete (extraction avec a_valider_ft2e non vide, apostrophes courbes ET
ACCENTS des l'ecriture, DEUX SONDES D'ACCENTS prouvees vivantes sur
L'UNION des pieces, composition par scripts/planches/<archetype>.py avec
assertion de depassement SUR LES TROIS FORMATS, PROUVEE VIVANTE sur
quatre copies, primitives PARTAGEES, MESURES distinguees des MOTIFS et
LIBELLES DECLINES PAR FORMAT, rendus par scripts/planches/rendre_png.py
depuis la RACINE, controles a 1152 / carte 274-296 / appui 552 -
REGARDER les quatre PNG, VERIFIER L'ORDRE DE TRACE, et AGRANDIR par PIL
tout detail douteux -, apostrophes-planches.py en MESURE **APRES la
premiere composition** puis jusqu'a 0, invariant.py, verser.py) ->
qualite (typecheck 0, build vert 70 pages, editorial-reviewer EN LECTURE
SEULE, ET VERIFIER CHACUN DE SES CONSTATS SUR LA PIECE OU PAR MESURE,
controle-liens-internes 47/47 a 5, controle-numeros-affaire 0 fuite,
releve-numeral sans ecart nouveau) -> COMMIT (content(references):
ajoute la fiche reelle <nom> et sa planche ; git ls-remote avant, depot
partage, `git add` par chemins explicites) -> push (le push deploie),
curl de la fiche AVEC barre oblique finale + marqueur de build, rendu
controle aux trois bandes (references/ref_046/sonde-fiche.mjs, slug et
URL a adapter), CARTOUCHE MESURE (sonde-cartouche.mjs, SELECTEUR A
RECALER) ET CONTROLE DE L'INDEXATION SECTORIELLE (point 6, sonde
references/ref_046/sonde-filtres.mjs, SECTEUR A RECALER, appelee DEPUIS
LA RACINE) -> ligne de suivi au plan -> PROMPT DE LA SESSION N25 en
annexe du plan (script Python ou Write, jamais un long heredoc) et
reproduit integralement dans le message final.

⚠⚠ ET SI LE CHANTIER N'A PLUS DE MATIERE : le prompt N25 ne peut plus
porter de dossier. Il doit alors porter LA QUESTION, pas un dossier -
c'est-a-dire l'etat exact du catalogue (47 fiches), la liste des trois
voies (a), (b), (c) ci-dessus, la piste de la section « Finalisees en
2021 » vide, et les points ouverts du chantier qui restent a solder hors
production de fiches (docs/23-etat-de-l-art.md en porte la liste : le
blocage OAuth de Decap, les validations FT2E sur les cliches, le passage
NVDA, les 17 correspondances de legendes manquantes). Une session sans
dossier n'est pas une session sans travail - mais elle ne fabrique pas
une fiche pour avoir l'air d'en faire.

Portee de commit : content(references). Un changement de schema Zod
eventuel passe par le sous-agent content-modeller et va dans le MEME
commit que public/admin/config.yml.

Termine par le prompt de lancement de la session N25, en annexe du
plan du chantier et reproduit integralement dans ton message final -
la regle de continuite est dans CLAUDE.md parce qu'elle a ete manquee
deux fois.
```


## Annexe Y — prompt de lancement de la session N25 (à coller tel quel en session neuve)

⚠ **Ce prompt ne porte pas de dossier d’affaires, et c’est délibéré.** Le chantier des
27 nouvelles fiches n’a plus de matière : l’utilisateur l’a clos à 47 fiches en ouverture
de la N24. Une session sans dossier n’est pas une session sans travail — mais elle ne
fabrique pas une fiche pour avoir l’air d’en faire.

```
Session N25 — FT2E v3. LE CHANTIER DES REFERENCES EST CLOS A 47 FICHES.
Cette session ne produit PAS de fiche : elle porte la question a FT2E et
solde ce qui reste ouvert.

Contexte. FT2E v3 est le site institutionnel du bureau d'etudes FT2E
(La Rochelle), Astro 6 statique, deploye en demonstration client sur
https://ft2e-v3.vercel.app (indexation verrouillee par triple securite -
robots.txt, meta noindex, header X-Robots-Tag : NE PAS Y TOUCHER sans
validation FT2E, procedure dans docs/19-migration-production.md).
Le catalogue porte 47 fiches de references reelles, chacune illustree
d'une planche de schema de principe (cinq pieces par dossier :
planche.json, planche.svg, appui.svg, vignette.svg, planche.png).

⚠⚠ CE QUI EST CLOS, ET QU'IL NE FAUT PAS ROUVRIR

Le chantier ouvert le 2026-08-27 visait 50 fiches (23 + 27). Il en a
livre 24 (N01 a N24), portant le catalogue de 23 a 47. Il s'arrete la,
faute de matiere, et l'arret est un ARBITRAGE DE L'UTILISATEUR rendu en
ouverture de la N24 - pas une renonciation de session.

La mesure qui le fonde, faite en N23 sur les cinq ZIP du disque par
zipfile.namelist() :
    2019.zip   1 dossier    18-026 Atelier numerique Fountaine Pajot (N24)
    2022.zip   4 dossiers   tous traites - ARCHIVE SUPPRIMEE
    2023.zip   5 dossiers   tous traites
    2024.zip   5 dossiers   tous traites
    2025.zip  10 dossiers   dont 23-075 deja publie
2020.zip N'EXISTE PAS (reponse de l'utilisateur en N23). Les affaires
19-008 (batiment industriel Aeroport LR / Elixir) et 20-058 (diagnostic
legionelles du port de plaisance) ne figurent dans AUCUNE archive
presente. L'ecart n'etait donc pas 49/50 mais 47/50.

⚠ NE PAS FABRIQUER DE FICHE POUR COMBLER L'ECART. La regle tient depuis
la N16 et elle tient encore. NE PAS non plus rouvrir l'arbitrage : il a
ete rendu, il est consigne au § Suivi (ligne N24) et dans
references/ref_047/fiche-collecte-atelier-numerique-fountaine-pajot-le-thou.md.

CE QUE CETTE SESSION DOIT FAIRE - dans cet ordre

1. POSER LA QUESTION A L'UTILISATEUR, EN OUVERTURE, avant tout travail.
   Trois voies restent ouvertes cote matiere, et une piste :
   (a) FT2E retrouve 2020.zip sur un autre support -> deux dossiers de
       plus, le catalogue irait a 49 ;
   (b) FT2E verse des dossiers HORS CLASSEUR - le classeur
       « REFERENCES SITE FT2E.ods » n'a jamais mene qu'a 49 affaires,
       l'objectif de 50 n'a jamais ete couvert par lui ;
   (c) le chantier reste clos a 47, et c'est l'etat actuel.
   ⚠ PISTE A VERIFIER AVEC FT2E, PAS A SUPPOSER : le classeur porte une
   section « Finalisees en 2021 » ENTIEREMENT VIDE - en-tete de section,
   en-tete de colonnes, aucune ligne. C'est le seul millesime sans
   entree, entre 2020 (deux entrees) et 2022 (quatre). L'hypothese est
   qu'une ou plusieurs affaires y manquent. Le classeur est dans
   references/docs_references/ ; il se lit par python zipfile sur
   content.xml.
   Si la reponse ouvre de la matiere, la session bascule sur le pipeline
   § 2 du present plan, dossier par dossier, sans rien changer d'autre.
   Si elle ne l'ouvre pas, poursuivre au point 2.

2. SOLDER CE QUI RESTE OUVERT. La liste fait foi dans
   docs/23-etat-de-l-art.md (§ 4, quatre rangs classes par ce qui
   debloque, plus son addendum du 2026-08-27 en pied). Resume :

   RANG A - hors du depot, aucune ligne de code ne l'approche
   - ⚠ DECAP EST CASSE EN PRODUCTION : /admin/ repond 200 mais
     /api/auth?provider=github rend HTTP 500, « Configuration OAuth
     manquante ». RIEN N'EST EN CAUSE DANS LE DEPOT. Il manque trois
     gestes hors depot, avec leurs commandes de controle au § 0 de
     docs/22-prise-en-main-decap.md : la callback
     https://ft2e-v3.vercel.app/api/callback sur l'OAuth App GitHub, et
     OAUTH_GITHUB_CLIENT_ID / _SECRET sur le projet Vercel. ⚠ A refaire
     au changement de domaine. ⚠ L'avertissement a vecu en COMMENTAIRE
     dans config.yml pendant six sessions : un commentaire n'echoue
     jamais.

   RANG B - suspendu a une piece ou a un arbitrage de FT2E
   - la reception de la creche de l'Oranger (23-075) : la fiche annonce
     une affaire livree SANS DIRE QUAND. ⚠ NE JAMAIS FABRIQUER UN
     MILLESIME ;
   - les 25 visuels encore dans l'historique git : les effacer demande
     une reecriture d'historique qui invalide tous les SHA cites dans
     les plans et les regles. Arbitrage, pas correction ;
   - l'archetype `planche-chiffree` : seul de la liste fermee du
     protocole que le corpus n'a JAMAIS exerce (47 planches, six
     archetypes en service, celui-ci a zero) - donc le seul dont rien
     ne garantit qu'il fonctionne. Le retirer de la liste ou le
     redefinir est un arbitrage editorial.
   - les validations FT2E du bloc secteurs : artefacts d'agrandissement
     generatif releves sur plusieurs des 44 cliches retenus (petits
     textes nets mais faux), et 17 correspondances de cliches encore a
     legender.
   - les questions B et E des 24 fiches de collecte, dont celles de la
     N24 (references/ref_047) : reception 2019 retenue sur faisceau,
     divergence du calcul d'honoraires, nombre de chaudieres, rubriques
     ICPE douteuses, caméra thermique supprimee en travaux.

   RANG C - suspendu a un evenement exterieur
   - les huit photographies d'equipe sont des images de demonstration
     generees par IA : elles se levent au reportage photographique, pas
     par une validation.

   RANG D - executable dans le depot, sans attendre personne
   - LES INSECABLES DU CORPUS DESSINE. ⚠ Le compte depend entierement
     de la population mesuree : 12 ecarts dans le texte DESSINE, 114
     dans les `aria-label` (donc PRONONCES par les lecteurs d'ecran,
     c'est de l'accessibilite), 602 dans les champs editoriaux du
     planche.json qui ne sortent jamais du depot. ⚠ NE PAS lancer
     scripts/injection-typographique.py sur ce corpus : il DEPLACE LE
     DESSIN, les compositeurs mesurant leurs chaines pour poser la
     geometrie et U+202F n'ayant pas la chasse d'une espace ordinaire.
     C'est un chantier avec correction A LA SOURCE, regeneration des 47
     dossiers, invariant octet et controle du rendu aux trois tailles.
   - LE PASSAGE NVDA, jamais fait par un humain.
   - l'option 0 du chantier motion : le filet de flux (TraceFlux.astro,
     900 ms) reste DEBRANCHE, option non arbitree.
   - le LCP mobile est AU seuil, pas sous : sept mesures de 1 656 a
     1 815 ms pour un budget de 1 800, de part et d'autre du seuil sans
     qu'aucune page ne soit systematiquement du mauvais cote. ⚠ Ne pas
     traiter cela comme un defaut de /equipe/.
   - deux pieces non suivies : livrables/cv-ft2e/CV-FT2E.zip et
     livrables/synthese-referencement-cliches-secteurs-2026-08-26.pdf.
     Trois issues chacune : suivre, ignorer, retirer. Decision de
     l'utilisateur.

3. ⚠⚠ L'ECHEANCE DATEE, ET LA SEULE MANIERE DE Y REPONDRE.
   src/lib/projets.ts porte MILLESIME_LIVRAISON_ANNONCE = 2026 et un
   garde-fou qui FAIT ECHOUER LE BUILD AU 1er JANVIER 2027. Le site
   annonce cette annee de livraison sur les QUINZE affaires dont la
   reception n'est pas prononcee (quatorze avant la N24 ; verifier par
   `grep -L annee_livraison src/content/projets/*.md | wc -l`).
   ⚠ NE JAMAIS repondre a cet echec en poussant la constante a 2027 :
   cela desarmerait le garde-fou pour s'epargner exactement l'echec
   qu'on lui demande de produire. La reponse est d'aller relever les
   receptions aupres de FT2E - c'est le rang B.

LIRE D'ABORD, dans cet ordre :
1. docs/23-etat-de-l-art.md EN ENTIER - c'est le point de reprise du
   depot, et son addendum du 2026-08-27 est en pied.
2. docs/superpowers/plans/2026-08-27-chantier-27-nouvelles-fiches.md -
   § 1 (etat d'entree), § 2 (pipeline, si de la matiere apparait),
   § 3 (reponses consignees), § Suivi (lignes N01 a N24), annexe Y
   (ce prompt).
3. CLAUDE.md et les six fichiers de .claude/rules/.
Si de la matiere apparait : docs/superpowers/specs/
2026-08-12-planches-references-protocole.md, revision 5 EN ENTIER, et
docs/superpowers/plans/2026-08-07-chantier-references-reelles.md
(§ Contraintes globales, § Protocole de session, § Regle des dossiers
minces).

PIEGES D'OUTILLAGE DE CETTE MACHINE - ils ne se redecouvrent pas
- Les insecables sont normalisees DE FACON NON DETERMINISTE par les
  outils d'ecriture. Deux voies : (a) ecrire le .md en espaces
  ordinaires et apostrophes droites, puis passer
  `python scripts/injection-typographique.py <fichier>` ; (b) script
  Python avec marqueurs '\x01'/'\x02' remplaces par chr(8239)/chr(160)
  et ASSERTION CALCULEE, jamais tapee. ⚠ json.dumps ECHAPPE les
  caracteres de controle meme sous ensure_ascii=False : compter les
  marqueurs sur la chaine SERIALISEE, sous la forme « \u0001 ».
- injection-typographique.py NE POSE NI ACCENTS NI EXPOSANTS NI
  LIGATURES : ecrire « m² », « m³/h », « °C », « oeuvre » -> « œuvre » a
  la main. Il ignore aussi plusieurs unites (A, V, volts, amperes, DN,
  Ω, bars, px/ml, MP, MHz, Gb/s, To, Mo, AWG, mA) : controler par regex
  apres passage et poser les fines manquantes par script.
- UNE ANCRE DE REMPLACEMENT SE VERIFIE PAR repr() OU PAR COMPTAGE, PAS
  PAR DEDUCTION. La parade generale : construire l'ancre en REGEX ou
  chaque espace vaut [ \u202f\u00a0], et asserter UNE occurrence.
- Le hook Stop commite et pousse SEUL ce qui traine, sur un depot
  PARTAGE dont l'historique ne se reecrit pas. Garder les scripts a
  usage unique DANS LE SCRATCHPAD, committer tot des que le build est
  vert, `git add` par CHEMINS EXPLICITES, jamais `git add -A`.
- La CLI vercel repond « Not authorized » : c'est le PUSH qui deploie.
  Verifier par curl AVEC barre oblique finale, et par un MARQUEUR DU
  BUILD, jamais par un delai d'attente.
- npm run preview NE MESURE PAS LA PERFORMANCE : il ne compresse rien,
  0,8 s de biais sur la chaine bloquante. La performance se mesure sur
  le deploiement.
- `npm run captures` EXISTE pour un jeu de captures multi-paliers : ne
  pas le rebatir. Les sondes de recette de la derniere session vivent
  dans references/ref_047/ : sonde-fiche.mjs, sonde-cartouche.mjs,
  sonde-filtres.mjs. ⚠ Leurs selecteurs sont EN DUR sur la fiche de la
  N24 (slug atelier-numerique-fountaine-pajot-le-thou, cartouche
  « LE THOU · 6 », secteur « Industriel », page
  /secteurs/industriel-commercial) : LES RECALER avant usage, et
  rejouer le garde-fou anti-residu (aucune chaine de la session
  precedente ne doit survivre dans le fichier recale).
  ⚠ sonde-fiche et sonde-cartouche prennent un REPERTOIRE en argument,
  pas un fichier ; scripts/planches/rendre_png.py aussi ; les trois
  s'appellent DEPUIS LA RACINE du depot.
- PYTHONIOENCODING=utf-8 devant toute commande python qui imprime des
  accents.
- Ne jamais taper un chemin d'archives : les noms portent accents et
  apostrophes typographiques. Passer par os.walk + fragments de nom.

ETAT MESURE DU DEPOT AU 2026-09-03, APRES LA N24
- 47 fiches de references reelles, 47 dossiers de planches complets
  (5 pieces chacun), build 70 pages, typecheck 0 erreur.
- `python scripts/planches/invariant.py` : 188/188 pieces identiques
  octet a octet (6 compositeurs, 47 dossiers). ⚠ Un dossier neuf non
  encore compose fait baisser le NUMERATEUR : lire le denominateur.
- Repartition sectorielle mesuree sur le deploiement : L10 T14 I8 P3 C7
  M7 E3, 52 en pondere (cinq fiches a double domaine comptent double).
- Archetypes : boucle-fluide 12 - coupe-traversee 11 - zonage-ssi 8 -
  sankey-energie 7 - tableau-electrique 7 - chronologie-affaire 2 -
  planche-chiffree 0 SANS MODULE.
- controle-liens-internes : 0 mort, 47/47 atteignent 5 liens.
- controle-numeros-affaire : 0 fuite hors JSON-LD.
- releve-numeral : 0 nombre compose ecrit en lettres.
- 0 marqueur [DEMO] dans src/content/.
- Espace disque : ~4,2 Go libres, volume a 100 %. ⚠ MESURE FAITE EN
  FIN DE N24 : C:\claude_code_dev_projectst2e_new_archives\ ne
  contient PLUS QUE 2019.zip (36,6 Mo). Les archives 2022, 2023, 2024 et
  2025 ont ete supprimees - la 2022 avec l'accord de l'utilisateur en
  fin de N23, les trois autres hors de la N24, qui ne les a pas
  touchees. Toutes leurs affaires etaient traitees : aucune matiere
  n'est perdue, mais AUCUNE ARCHIVE NE SE RETELECHARGE - si une
  verification sur piece devient necessaire, elle passe par
  l'utilisateur. 2019.zip peut etre supprime a son tour (son unique
  dossier est traite) : A PROPOSER a l'utilisateur, jamais a faire sans
  son accord.

Portee de commit selon le travail retenu : docs(...) pour un point de
suivi, a11y(...) pour NVDA ou les insecables des aria-label,
content(references) si de la matiere apparait. Un changement de schema
Zod passe par le sous-agent content-modeller et va dans le MEME commit
que public/admin/config.yml.

Termine par le prompt de lancement de la session suivante, en annexe du
plan et reproduit integralement dans le message final - la regle de
continuite est dans CLAUDE.md parce qu'elle a ete manquee deux fois.
```
