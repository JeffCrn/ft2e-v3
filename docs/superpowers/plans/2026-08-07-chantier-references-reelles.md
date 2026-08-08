# Chantier références réelles — programme des 22 sessions

> **Pour les exécutants agentiques :** ce plan s'exécute **une session de travail par référence**, dans l'ordre du tableau § Ordre des sessions. Chaque session suit intégralement le § Protocole de session et se termine **obligatoirement** par la rédaction du prompt de lancement de la session suivante (`references/sessions/session-NN-prompt.md`) — c'est la règle de continuité du chantier. Ne pas exécuter plusieurs sessions d'affilée sans validation utilisateur.

**Objectif :** publier 22 fiches références réelles dans `src/content/projets/`, une par session, à partir des 22 dossiers d'affaires extraits dans `C:\ft2e-arch\`, conformément au gabarit, à la voix éditoriale et à la stratégie SEO/GEO du site.

**Architecture :** chaque session = dépouillement d'un dossier d'affaires → croisement avec les documents commerciaux → fiche de collecte préremplie (livrable client) → fiche projet Markdown conforme au schéma Zod → contrôles qualité → commit + déploiement → prompt de la session suivante.

**Stack :** Astro 6 Content Collections (`src/content.config.ts`), fiches Markdown + frontmatter YAML, lecture PDF (outil Read), pandoc pour les docx, build `npm run build` (validation Zod bloquante).

## Contraintes globales (s'appliquent à chaque session)

- **Jamais de donnée inventée.** Toute valeur métier provient d'un document du dossier d'affaires, d'un docx sectoriel ou de `docs/20-source-plaquette-2024.md`. Info manquante = `TODO:` explicite ou omission — jamais d'à-peu-près.
- **Le tag `[DÉMO]` ne s'applique qu'aux données non vérifiées.** Une fiche réelle sourcée n'en porte aucun (`demo: false`, valeur par défaut).
- **Secteurs autorisés** (enum Zod) : `Logements | Tertiaire / ERP | Industriel et commercial | Patrimoine | Monotechnique | Coordination SSI | Études d'exécution / BIM`.
- **Récit en 4 sections** (`## L'enjeu`, `## Solution` ou variantes rédactionnelles, `## Particularités`, `## Résultat`) — gabarit `content-templates/projet-modele.md`, étalon `src/content/projets/creche-oranger-perigny.md`.
- **Voix FT2E** : sobre, technique, chaleureuse — `.claude/rules/french-editorial.md` (typographie française stricte : espaces insécables, guillemets « », apostrophe typographique, `m²`, RT2012/RE2020 sans espace).
- **GEO** (fiche de collecte, p. 1) : des chiffres précis et vérifiables, des lieux nommés (commune, agglomération, département), un récit unique, une phrase = un fait citable.
- **Titre ≤ 80 caractères** (Zod), `<title>` et `description` uniques sur tout le site.
- **Images** : `public/images/projets/<slug>/`, alt descriptif obligatoire, rapports 21:8 / 16:10 / 3:2 uniquement, duotone appliqué par les composants. Pas d'image → le pattern `fs.existsSync` affiche « [Photo à venir] » ; ne jamais référencer un fichier au mauvais format.
- **Avant commit : `npm run build`** (échec = blocage). Après commit + push : `npx vercel deploy --prod --yes`.
- **Commits** : `content(references): ajoute la fiche réelle <nom court>` (impératif présent, ≤ 72 car.).
- **Autorisations MOA** (section E de la fiche de collecte) : tant qu'elles ne sont pas obtenues, le site reste en démo noindex — les fiches se publient, la levée d'indexation reste soumise à validation FT2E (`docs/19-migration-production.md`).

## État initial (2026-08-07)

- **Corpus** : 22 dossiers d'affaires dans `C:\ft2e-arch\` (3 550 fichiers ; inventaire filtrable : `references/inventaire-archives-2026.csv`, séparateur `;`).
- **Sources croisées** : 11 docx sectoriels dans `references/docs_references/` (~200 références commerciales avec MOA, montants, surfaces, années) ; faits vérifiés plaquette : `docs/20-source-plaquette-2024.md`.
- **Fiche de collecte** : `references/Fiche-collecte-reference-projet-FT2E.pdf` — sections A et A+ préremplies par nous depuis le DCE ; sections B (résultat), C (enjeu raconté), D (visuels), E (autorisations) à compléter par FT2E.
- **Fiches en ligne** : 1 réelle (`creche-oranger-perigny.md`, ref_001) + 10 `[DÉMO]` (`demo: true`). Deux DÉMO seront **remplacées** par leur version réelle en cours de chantier (voir tableau) ; le sort des huit autres se décidera en fin de chantier avec FT2E.
- **Précédent de session** : `references/ref_001/` (pièces sources de l'Oranger) — le modèle du dossier de travail par référence.

## Protocole de session (déroulé complet, ~une référence)

1. **Ouverture.** Lire ce plan (§ Contraintes, § Suivi), puis le prompt de session dans `references/sessions/session-NN-prompt.md`. Vérifier dans le tableau de suivi que la référence est bien « à faire ».
2. **Dépouillement du dossier d'affaires.** Explorer `C:\ft2e-arch\<dossier>` (filtrer `references/inventaire-archives-2026.csv` sur la colonne `dossier_affaire` pour cibler). Pièces prioritaires, dans l'ordre : synthèse RT / étude thermique (version la plus récente), CCTP des lots FT2E, DPGF ou estimation, perspectives et photos, pièces marché (montants, calendrier). Lire les PDF avec l'outil Read (param `pages`).
3. **Constitution du dossier de travail.** Copier les 3 à 8 pièces sources décisives dans `references/ref_NNN/` (numérotation continue : ref_002, ref_003…). C'est la traçabilité de chaque affirmation de la fiche.
4. **Croisement commercial.** Retrouver le projet dans les docx de `references/docs_references/` (pandoc `-t markdown` si besoin) et dans `docs/20-source-plaquette-2024.md` : MOA, architecte, montant, surfaces, année, référence environnementale. En cas de conflit entre sources, la pièce du dossier d'affaires fait foi ; noter le conflit.
5. **Fiche de collecte préremplie** (livrable client). Créer `references/ref_NNN/fiche-collecte-<slug>.md` calquée sur le PDF : section A complète, section A+ (données techniques extraites, chiffrées, sourcées pièce par pièce), sections B / C / D / E laissées en questions pour l'équipe FT2E.
6. **Visuels.** Chercher dans l'ordre : photos du dossier d'affaires → images du docx sectoriel (`unzip -j <docx> 'word/media/*'`) → rien. Si visuel exploitable : recadrer aux rapports autorisés, déposer dans `public/images/projets/<slug>/`, alt descriptif, crédit architecte à tracer (section E). Sinon : laisser le chemin conventionnel dans le frontmatter (placeholder « [Photo à venir] » géré par `fs.existsSync`).
7. **Rédaction de la fiche.** Créer `src/content/projets/<slug>.md` (slug kebab-case sans accents ; vérifier qu'il n'écrase rien) : frontmatter complet conforme à `src/content.config.ts`, récit 4 sections nourri des données extraites, aucune invention, sections B/C manquantes compensées par la matière technique en attendant le retour FT2E.
8. **Remplacement DÉMO le cas échéant.** Si le tableau indique une fiche DÉMO équivalente : la supprimer dans le même commit (le site est noindex, aucune redirection nécessaire).
9. **Contrôles qualité.** (a) `npm run build` vert ; (b) relecture éditoriale par l'agent `editorial-reviewer` (voix + typographie française) ; (c) unicité du titre et de la description ; (d) alt text présents ; (e) cohérence des chiffres fiche ↔ pièces sources.
10. **Livraison.** Commit (`content(references): …`) + push + `npx vercel deploy --prod --yes`. Contrôle visuel de la fiche sur le déploiement.
11. **Suivi.** Mettre à jour le tableau § Suivi ci-dessous (statut, visuels, collecte, particularités découvertes).
12. **Prompt de la session suivante** (OBLIGATOIRE, clôture de session). Rédiger `references/sessions/session-NN+1-prompt.md` selon le gabarit ci-dessous, avec les données déjà connues de la prochaine référence, et le reproduire intégralement dans le message final à l'utilisateur.

## Gabarit du prompt de session (à instancier à chaque clôture)

```markdown
# Session NN — <n° affaire> · <nom du projet>

Chantier références réelles FT2E v3 — session NN/22.
Lire d'abord : docs/superpowers/plans/2026-08-07-chantier-references-reelles.md
(§ Contraintes globales + § Protocole de session + § Suivi), puis dérouler le
protocole intégralement pour la référence ci-dessous.

## Référence du jour
- Affaire : <n°> — <intitulé complet>
- Dossier d'affaires : C:\ft2e-arch\<nom exact du dossier>
- Dossier de travail à créer : references/ref_NNN/
- Slug cible : <slug> (vérifier la disponibilité)
- Secteur pressenti : <secteur enum> · Typologie : <typologie> · Statut : <livré|en cours>
- Fiche DÉMO à remplacer : <chemin | aucune>

## Ce qu'on sait déjà (sources commerciales — à confirmer par les pièces)
<données du docx sectoriel et de la plaquette : MOA, architecte, montant,
surfaces, année, référence environnementale, missions>

## Points de vigilance
<spécificités : versions multiples de synthèses RT, absence de photos,
doublons entre docx, conflits de données repérés…>

## Livrables de la session
1. references/ref_NNN/ — pièces sources sélectionnées
2. references/ref_NNN/fiche-collecte-<slug>.md — sections A/A+ préremplies
3. src/content/projets/<slug>.md — fiche conforme gabarit, build vert
4. Commit + déploiement Vercel
5. Tableau de suivi du plan mis à jour
6. references/sessions/session-NN+1-prompt.md — prompt complet de la session suivante
```

## Ordre des sessions

L'ordre privilégie : (1) les dossiers les mieux documentés d'abord — rodage du protocole ; (2) la couverture rapide des sept secteurs par des fiches réelles ; (3) les dossiers minces (audits, faisabilité) en fin de chantier.

| S | Affaire | Dossier `C:\ft2e-arch\` | Secteur pressenti | Typologie | Source docx principale | Notes |
|---|---|---|---|---|---|---|
| 01 | 20-014 | `20-014-54 logements CVL Pellereau` | Logements | Neuf | `REF FOUGEROU A3.docx` | 48+6 logts Sainte-Marie-de-Ré ; photos dans le docx ; synthèses RT multi-révisions |
| 02 | 21-061 | `21-061- EHPAD Coulonge sur Autize - ABP +Diese` | Tertiaire / ERP | Neuf | `FT2E -  Références SSI.docx`, `Réf. médico-social.docx` | **Remplace `ehpad-coulonges-coordination-ssi.md` (DÉMO)** ; ERP J, 102 lits |
| 03 | 24-003 | `24-003 - Bureaux et ateliers RESE Aigrefeuille - BTB` | Tertiaire / ERP | Réhabilitation | `Réf. DIAGNOSTIC.docx` | Diagnostic 2025 + restructuration siège |
| 04 | 25-097 | `25-097 - EXE HORIZON MEDIATIM - EUSTACHES` | Études d'exécution / BIM | Études d'exécution | — (absente des docx) | 1 Go de production EXE ; seul dossier du secteur |
| 05 | 22-042 | `22-042- Abbaye Sablonceaux` | Patrimoine | Réhabilitation | `Réf. Réhabilitation Patrimoine.docx`, SSI | Coordination SSI en site patrimonial ; présent dans 3 docx |
| 06 | 22-006 | `22-006 - INNOVIA Labo Pilotes CAPSULAE - Cab SOURD` | Industriel et commercial | Neuf | — | Laboratoire industriel ; vocabulaire process à soigner |
| 07 | 21-098 | `21-098 -Maison Relais SOLIHA St Jean d'Angely- ASP` | Logements | Réhabilitation | `Réf. DIAGNOSTIC.docx` + 2 autres | 21 logts dans immeuble existant, 2 068 000 €, RT existant |
| 08 | 22-033 | `22-033 - 21 Logts St Agnant - ASP` | Logements | Neuf | `Références logements collectifs…` | Résidence intergénérationnelle, 747 m² |
| 09 | 23-079 | `23-079- Pôle commercial St Rogatien -BTB` | Industriel et commercial | Neuf | — | DCE VRD/désimperméabilisation dans le dossier |
| 10 | 24-006 | `24-006 - Etude Notariale Bd Joffre  - UBIK` | Tertiaire / ERP | Neuf | `Réf. Social et Tertiaire.docx` | |
| 11 | 20-021 | `20-021- 40 logts Projet NEREA - PITCH Promotion - SMART` | Logements | Neuf | `Références logements collectifs…` (à confirmer : 40 logts quartier Job, Royan) | Plus gros dossier (1,15 Go) |
| 12 | 22-003 | `22-003- 13 Logts Chagnolet OPH - BTB` | Logements | Neuf | `Références logements collectifs…` (« Maubec ») | |
| 13 | 22-066 | `22-066- 10 Logts BOIS PLAGE Habitat 17 - ASP` | Logements | Neuf | `Références logements collectifs…` (« Le Pas du Bœuf ») | |
| 14 | 19-033 | `19-033 -10 Logts St GEORGES DE DIDONNE - SMART` | Logements | Neuf | à retrouver dans les tableaux logements | |
| 15 | 23-095 | `23-095- ADMR Salignac - CASE Architectes` | Logements | Neuf | `Références logements collectifs…` (habitat inclusif 14 T1) | |
| 16 | 25-024 | `25-024 - Réhabilitation d'un ancien LIDL en centre de formation - CCI` | Tertiaire / ERP | Réhabilitation | — (affaire récente) | Fiche inédite |
| 17 | 24-044 | `24-044 - Hotel Yachtman La Rochelle - DET` | Tertiaire / ERP | Réhabilitation | — | Phase DET |
| 18 | 23-054 | `23-054 - CDC Marennes - Cab Sourd` | Tertiaire / ERP | à déterminer | — | Nature exacte à établir au dépouillement |
| 19 | 25-084 | `25-084 - Ecole des Douanes - HERVE THERMIQUE` | Études d'exécution / BIM (à confirmer) | à déterminer | — | Client installateur → probable EXE |
| 20 | 24-034 | `24-034 - Passerelle Marans - Impact Urbanisme` | Monotechnique (à confirmer) | à déterminer | — | Ouvrage d'art — périmètre FT2E à établir |
| 21 | 25-010 | `25-010 - Bat Cuisine VILLEDOUX  - Audit` | Monotechnique | à déterminer | — | Audit ; fiche seulement si matière suffisante |
| 22 | 25-080 | `25-080 - Etude de faisabilité - DUFOUR` | Monotechnique | à déterminer | — | Faisabilité ; fiche seulement si matière suffisante |

**Règle des dossiers minces (S21–S22)** : si le dépouillement révèle une matière insuffisante pour une fiche honnête (pas de chiffres vérifiables, mission trop ponctuelle), la session produit à la place la fiche de collecte seule + une note au tableau de suivi, et propose à FT2E une référence de substitution issue des ~200 références des docx.

## Suivi (mettre à jour à chaque session)

| S | Affaire | Slug | Fiche | Collecte | Visuels | Autorisation MOA | Notes |
|---|---|---|---|---|---|---|---|
| — | 23-075 | `creche-oranger-perigny` | ✅ en ligne | ✅ (exemple du PDF) | ✅ 1 photo | à demander | fiche étalon, ref_001 |
| 01 | 20-014 | `fougerou-sainte-marie-de-re` | ✅ en ligne | ✅ A/A+ (ref_002) | ✅ 1 photo (docx A3, 3:2, 608 px) | à demander | MOA = « Coopérative » Vendéenne du Logement (la plaquette écrit « Compagnie ») ; BQE élucidé = bordereaux quantitatifs tous lots (contrat MOE) ; synthèse RT 2022 tronquée dans l'archive → études par îlots utilisées ; 3 tranches livrées 2024 / févr. 2025 / mars 2026 ; îlots A-B étiquetés « Habitat 17 » dans Typologies-Surfaces.xlsx (bailleur des 6 locatifs ? à clarifier) ; `en_avant` laissé à false (l'image 608 px deviendrait le hero de l'accueil — à décider) |
| 02 | 21-061 | `ehpad-coulonges-sur-autize-ssi` | ✅ en ligne | ✅ A/A+ (ref_003) | ✅ 1 perspective aérienne (docx médico-social, 3:2, 909 px — crédit ABP à confirmer ; les 2 photos du dossier = plans papier) | à demander | DÉMO `ehpad-coulonges-coordination-ssi.md` supprimée (pas de dossier image physique) ; établissement nommé « EHPAD Aliénor d'Aquitaine » (notice de sécurité FT2E) ; graphie « 102 lits » retenue (devis FT2E + corps CCFSSI + plaquette) contre « 102 chambres » (arrêté PC) et « 102 logements » (pages de garde/PV) ; mission en sous-traitance du BET Diese (citer Diese ? → E) ; deux adresses (2 rue du Poitou au PC / route de Saint-Pompain aux pièces SSI) ; essais 04/12/2025 (2 foyers types : 3 min / 1 min 50), réception SSI 15/01/2026 → annee 2026 ; passage commission de sécurité + date d'ouverture à confirmer (B) |
| 03 | 24-003 | `siege-rese-aigrefeuille` | ✅ en ligne | ✅ A/A+ (ref_004) | ✅ 1 perspective aérienne (docx DIAGNOSTIC, 16:10, 860 px — crédit BTB à confirmer) | à demander | MOA élucidé = RESE (Eau 17), SEMDAS = AMO (le docx écrit « MOA : SEMDAS ») ; conflit montant : docx 906 660 € HT vs marchés notifiés 23/07/2025 ≈ 600 027 € HT (APD 653 242 · PRO 669 771) → fiche prudente « ≈ 600 000 € HT », question posée en B ; montant final AE lot 4 ambigu (31 644,40 ou 37 644,40 €) ; statut `en cours` acté (OPR 22/07/2026, levée réserves 31/08/2026, PV n°39) — première fiche réelle `en cours`, rendu nomenclature vérifié ; FT2E = mission complète MOE (16 955,77 € HT après avenant APD) + 95 % CSSI ; diagnostic 2024 (docx confirme) ; surface 600 m² (docx) vs 595,6 m² (plan DCE n°7) — les deux dans la fiche |
| 04 | 25-097 | `exe-residence-horizon-mediatim` | ✅ en ligne | ✅ A/A+ (ref_005) | ✅ extrait 16:10 de notre plan de réservations R+2 (production FT2E — aucun droit tiers) | à demander (Eustache Frères + MP Rhapsody/Mediatim ; Diese cité) | DÉMO `exe-psla-bouygues.md` supprimée dans le même commit (secteur couvert par la réelle) ; « Cardinal » élucidé = seconde rue de l'angle Désirée/Cardinal (même opération, n° Diese D-24050) ; production réelle jusqu'au **24/04/2026** (15 envois — le prompt S04 s'arrêtait au 19/03) ; statut `en cours` (chantier ; mission d'études probablement soldée → question B) ; graphie « Eustache Frères » retenue (papiers de l'entreprise, eustache-freres.fr) contre « EUSTACHES FRERES » (contrat FT2E) → à confirmer ; n° de lot divergent (11 CVPBS Diese vs « 12 CVC » fiche négo) → fiche sans n° ; SHAB 864 m² (tableau site) vs 860,5 (somme bâtiments A+B) ; champ `moa` porte la double relation « MP Rhapsody (groupe Mediatim) — mission FT2E pour Eustache Frères » |
| 05 | 22-042 | `abbaye-sablonceaux-ssi` | ✅ en ligne | ✅ A/A+ (ref_006) | ✅ 1 vue aérienne (docx patrimoine, 3:2, 614 px — auteur du cliché drone à identifier, crédit → E ; 2 photos FT2E du CR06 dispo en galerie) | à demander | **Première fiche réelle Patrimoine** (coexiste avec la DÉMO `maison-pierre-loti.md`, filtre vérifié au build) ; mission élucidée = MOE complète loi MOP + CSSI (devis 30/01/2023 : 5 810 € HT + avenant 05/02/2025 : 1 540 € HT = 7 350 € HT) — les docx ne vendent que « Coordination SSI » ; écart 2023→2025 élucidé = pas de suspension mais reprise du zonage d'alarme demandée par le préventionniste (M. Poncelet), couverte par l'avenant ; marché DEF (Saintes) lot unique 58 255,70 € HT notifié 13/01/2026, 9 semaines (le scan `20260216…pdf` = OS contresigné DEF) ; essais fonctionnels 20/05/2026 (24 points sur batteries, foyer type grenier d'abondance validé NF S 61-970 dès le 14/04), avis favorable réception 30/06/2026 → annee 2026, statut livré ; surface 3 370 m² = docx uniquement, non recoupée sur pièce (question B) ; en suspens B : visite SDIS/commission (programmée avant le 18/04/2026), levée dérangement A012 (fuite toiture), 2 détecteurs combles Logis (TS), contrat de maintenance, montant final avec TS ; pas d'architecte ni de bureau de contrôle (choix MOA, CR06) |
| 06 | 22-006 | `ateliers-pilotes-capsulae` | ✅ en ligne | ✅ A/A+ (ref_007) | ✅ extrait 16:10 de notre plan CVC01 marché (production FT2E — aucun droit tiers) | à demander (Capsulae/Innov'ia — confidentialité industrielle : question explicite en E sur ce qui peut être nommé) | **Première fiche réelle Industriel et commercial** (premier peuplement du secteur, filtre vérifié au build) ; chaîne contractuelle élucidée : contrat MOE 23/03/2023 signé **SA Innov'ia**, marchés travaux signés **Capsulae** → `moa` « Capsulae — groupe Innov'ia » ; « GAELIC » élucidé = bâtiment existant conservé du site (4-6 rue Charles Tellier, zone Agrocéan) — **neuf adossé au bâtiment IDCAPS, site en exploitation** ; deux vagues de DCE élucidées = AO févr. 2024 non poursuivi, évolutions du programme (devis reprises n° 23.2024, PRO2 oct. 2024, marchés janv. 2025) ; lots FT2E : ELEC Eiffage Énergie 182 000 € HT + avenants 22 474,58 · CVC Azay Chauffage 243 000 € HT ; TCE 12 lots 1 380 000 € HT (APD n° 2) ; statut `en cours` (CR45 du 28/01/2026 ; OPR 18/02/2026, réception 04/03/2026 « à confirmer ») → annee 2026 ; surface : 476 m² aménagés (PRO2) retenus contre ≈ 900 m² SdP (CCP 2023) — question B ; écart estimation AVP 2 527 000 € vs assiette honoraires 1 380 000 € non élucidé (question B) ; CVC process hors marché = Clauger (citer ? → E) ; bilan utilités MOA (413 kW, air comprimé ISO 8573-1…) gardé hors fiche publique (confidentialité) |
| 07 | 21-098 | `maison-relais-saint-jean-d-angely` | ✅ en ligne | ✅ A/A+ (ref_008) | ✅ extrait 16:10 de notre plan CVC02 DCE (production FT2E — aucun droit tiers) | à demander (SOLIHA BLI NA ; nommer l'UDAF ? → E) | MOA élucidé = **SOLIHA BLI Nouvelle-Aquitaine** (AE MOE accepté 08/11/2021 à Périgny, timbre SOLIHA Charente-Maritime Deux-Sèvres) — l'UDAF est le destinataire nommé du marché (« pour l'UDAF »), rôle exact (gestionnaire ? UDAF 17 ?) → question B/C ; « ASP » = Agence Sébastien Pellereau (même architecte que S01) ; programme élucidé = **restructuration d'un ancien FJT de 1960** (étude énergétique), 7 T1 + 8 T1 bis + 6 T2 + espace d'animation 89 m² ; RT existant « globale » : Cep 160,49 → 98,84 kWhep/m²/an (−38,42 %) ; montants divergents : AE 1 847 708,76 € HT prévisionnel · APS 1 896 000 € · docx 2 068 000/2 068 400 € HT → question B ; statut `en cours` (CR51 du 27/07/2026 : réserves de réception à lever pour le 24/08/2026, pas de PV en archive) ; écart DCE oct. 2022 → chantier mars 2025 (~2,5 ans) inexpliqué au dossier → question B ; courrier « DEMENAGEMENT » élucidé = changement d'adresse du siège SOLIHA BLI (juin 2025), pas un relogement ; FT2E aux CR : Vincent Jaoul + Mathieu Braud ; honoraires FT2E 30 045,86 € HT (12,28 % base + 38 % EXE lots techniques) |
| 08 | 22-033 | `residence-intergenerationnelle-saint-agnant` | ✅ en ligne | ✅ A/A+ (ref_009) | ✅ 1 perspective (page de garde des CR ArchiReport, 3:2, 744 px — crédit ASP à confirmer) | à demander | opération nommée « Résidence Le Galoubet » à l'annexe DC4 de l'AE (nom d'usage ? → C) ; graphie « Résidence intergénérationnelle » retenue (toutes les pièces) contre « Maison » (docx) ; **première fiche RE2020 du chantier** : logements Bbio −22,8 % / Cep −18,1 % / Ic construction 758,6 vs 777,4, espace commun **Cep −221,8 kWhep/m²/an** grâce au lot 13 PV (Coué Michaud, pose mai-juin 2025) — la plaquette dit « RE2020 −10 % », valeurs de la synthèse DCE retenues ; « Reprise RE » élucidée = reprise du calcul RE2020 (240 € HT, 11/02/2025) pour une variante ponts thermiques de l'entreprise de gros œuvre ECBL ; « 2023-05-10 RESE » = plan CVC01 ind A vraisemblablement transmis à la RESE pour le raccordement eau (à confirmer) ; conflit montants : AE oct. 2022 = 1 603 700 € HT vs docx 2 073 930 € HT, épisode « Piste économies » oct.-nov. 2023 entre les deux → question B ; statut `en cours` (OS 10/10/2024, CR48 du 26/02/2026 à ~95 %, livraison 2026) ; surfaces SHAB 769,74 m² + SU RT commun 100,27 m² (docx : 747 + 103) → `surface_m2` 870 ; part FT2E au groupement MOE : 24 433,35 € HT |
| 09 | 23-079 | — | à faire | à faire | à chercher | à demander | — |
| 10 | 24-006 | — | à faire | à faire | à chercher | à demander | — |
| 11 | 20-021 | — | à faire | à faire | à chercher | à demander | — |
| 12 | 22-003 | — | à faire | à faire | à chercher | à demander | — |
| 13 | 22-066 | — | à faire | à faire | à chercher | à demander | — |
| 14 | 19-033 | — | à faire | à faire | à chercher | à demander | — |
| 15 | 23-095 | — | à faire | à faire | à chercher | à demander | — |
| 16 | 25-024 | — | à faire | à faire | à chercher | à demander | — |
| 17 | 24-044 | — | à faire | à faire | à chercher | à demander | — |
| 18 | 23-054 | — | à faire | à faire | à chercher | à demander | — |
| 19 | 25-084 | — | à faire | à faire | à chercher | à demander | — |
| 20 | 24-034 | — | à faire | à faire | à chercher | à demander | — |
| 21 | 25-010 | — | à faire | à faire | à chercher | à demander | dossier mince ? |
| 22 | 25-080 | — | à faire | à faire | à chercher | à demander | dossier mince ? |

## Fin de chantier (après S22)

1. Bilan des 8 fiches DÉMO restantes avec FT2E : suppression, ou conversion en réelles si les données arrivent (Maison Pierre Loti figure dans les docx patrimoine/SSI — bonne candidate).
2. Envoi groupé des 22 fiches de collecte à FT2E pour les sections B–E ; intégration des retours (résultats constatés, récits d'équipe, photos, autorisations).
3. Passe SEO/GEO transversale : maillage interne fiches ↔ pages secteurs/expertises (≥ 5 liens internes contextuels par fiche), unicité des métadonnées, JSON-LD `CreativeWork`.
4. Audit RGAA + Lighthouse sur 3 fiches échantillon.
5. Reportage photo professionnel (production) → remplacement des visuels d'archive.
