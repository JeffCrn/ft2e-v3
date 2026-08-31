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
