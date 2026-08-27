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
- certaines affaires portent un domaine double (« T § C », « P § C ») que la
  taxonomie du site ne connaît pas — arbitrage à demander le moment venu.

## Suivi (une ligne par session)

| N | Affaire | Slug | Fiche | Planche (archétype) | Collecte | Notes |
|---|---|---|---|---|---|---|
| N01 | 22-011 — Réhabilitation de la mairie et création de l'office de tourisme, Les Portes-en-Ré | `mairie-les-portes-en-re` | ✅ rédigée, build 47 pages | ✅ `boucle-fluide`, **mécanisme `terminaux` créé** (8ᵉ du compositeur — invariant octet des 7 planches existantes vérifié avant/après ; une 1ʳᵉ planche `chronologie/relais` a été refusée par FT2E — voir l'arbitrage au § 1 — et le mécanisme retiré) | ✅ ref_024 (8 pièces) | `annee_livraison: 2025` sur docx commercial « RÉALISATION : 2025 » + cadrage tranche — PV de réception absent (→ B1) ; questions B1-B4, C1-C2, E1-E2 ouvertes ; Eric Moinet vérificateur des CCTP (T6) ; secteur Tertiaire / ERP |
| N02 | 21-062 — Construction d'un pôle commercial et requalification des espaces urbains et paysagers, Fors | `pole-commercial-fors` | ✅ rédigée, build 48 pages | ✅ `sankey-energie`, **mécanisme `partage` créé** (5ᵉ du compositeur — invariant octet des 4 planches sankey existantes vérifié avant/après la greffe, 16/16 deux fois) — l'année d'énergie de l'étude d'autoconsommation collective (36 kWc), en-tête de registre nommant l'étude | ✅ ref_025 (8 pièces) | `annee_livraison: 2025` (cadrage tranche + classeur FT2E « Finalisées en 2025 ») ; secteur `Tertiaire / ERP` par le classeur (≠ dépouillement qui penchait `Industriel`) ; mission MOE photovoltaïque séparée (21-062PV, DCE 04/2025, travaux prévus sept.-oct. 2025 → B2) ; questions B1-B5, C1-C2, E1-E3 ouvertes ; auteurs relevés (T6) : Mathieu Braud, Vincent Jaoul, Sandrine Rameau, Tanguy Moinet, Eric Moinet |

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

## Annexe C — prompt de lancement de la session N03 (à coller tel quel en session neuve)

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
   (reponses consignees + COMPLEMENT N02 : le classeur REFERENCES SITE
   FT2E.ods, dans references/docs_references/, fait foi pour le SECTEUR
   de chaque fiche et le millesime de livraison), § Suivi (lignes N01,
   N02), annexe C (ce prompt).
2. docs/superpowers/plans/2026-08-07-chantier-references-reelles.md -
   § Contraintes globales + § Protocole de session.
3. docs/superpowers/specs/2026-08-12-planches-references-protocole.md -
   revision 5 EN ENTIER.
4. CLAUDE.md, .claude/rules/content-collections.md et french-editorial.md.
Etalons : src/content/projets/creche-oranger-perigny.md (fiche) et, pour
une session N complete, src/content/projets/pole-commercial-fors.md +
public/images/projets/pole-commercial-fors/ + references/ref_025/.

DOSSIER DU JOUR : « 19-036 -150 logts Rompsay MEDIATIM » (208 fichiers),
dans C:\claude_code_dev_projects\ft2e_new_archives\2025.zip (tranche des
livraisons 2025 - liste au § 3 du plan ; le classeur FT2E le donne
« 150 Logts Rompsay Mediatim - AURORA », secteur L, Finalisees en 2025).
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

CE QUE LA N02 A ETABLI (verifiable au depot) :
- Le classeur REFERENCES SITE FT2E.ods (references/docs_references/)
  fait foi pour le SECTEUR (legende L/T/I/P/C/M/E) et le millesime de
  livraison. Il a fait basculer Fors en Tertiaire / ERP contre le
  depouillement. Le lire AVANT de choisir secteur et annee_livraison.
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
(A/A+ remplies, B-E en questions) -> fiche src/content/projets/<slug>.md
(taxonomie ACTUELLE ; lieu avec code postal entre parentheses ;
synthese 480-780 posee par script ; >= 5 liens internes ; jamais de
numero d'affaire NI de millesime d'ouverture en prose) -> PLANCHE
complete (extraction avec a_valider_ft2e non vide, composition par
scripts/planches/<archetype>.py, controles a 1152 / carte 274-296 /
appui 552, PNG 2400x1600, apostrophes-planches.py, verser.py) ->
qualite (typecheck 0, build vert 49 pages, editorial-reviewer,
controle-liens-internes 26/26 a 5, controle-numeros-affaire 0 fuite,
releve-numeral sans ecart nouveau) -> COMMIT UNIQUE
fiche+planche+compositeur (content(references): ajoute la fiche reelle
<nom> ; git ls-remote avant, depot partage) -> push (le push deploie),
curl de la fiche AVEC barre oblique finale + marqueur de build, rendu
controle aux trois bandes (sonde iframe pour les largeurs telephone,
script pret : references/ref_024/sonde-fiche.mjs) -> ligne de suivi au
plan -> PROMPT DE LA SESSION N04 en annexe du plan (script Python ou
Write, jamais un long heredoc bash) et reproduit integralement dans le
message final.

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
fois.
````
