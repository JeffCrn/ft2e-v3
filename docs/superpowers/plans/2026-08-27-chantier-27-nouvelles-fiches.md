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

## Suivi (une ligne par session)

| N | Affaire | Slug | Fiche | Planche (archétype) | Collecte | Notes |
|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — |

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
