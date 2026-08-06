# Réorganisation de la hiérarchie des contenus — design

**Date** : 2026-08-06
**Déclencheur** : audit demandé par FT2E/Jeff — redondance Accueil/Expertises, déséquilibre Accueil/Société.
**Principe retenu** : « une altitude par page » — chaque page du site répond à une question distincte, aucun bloc n'est rendu deux fois à l'identique.

---

## 1. Audit — constats

### 1.1 `/expertises` est un doublon strict de l'accueil

La page index Expertises = `HeroPage` + le **même composant `CartesExpertises`** que l'accueil (mêmes cartes, mêmes accroches, même grille) + `CtaFinal`. Zéro apport d'information. La spec `docs/04-specifications-pages.md` demandait pourtant des « cartes avec accroche élargie ». Les 6 sous-pages expertise sont riches (markdown, livrables, FAQ, projets liés) mais l'index qui y mène est vide.

### 1.2 L'accueil ne « dit » rien

L'accueil est une enfilade de teasers (chiffres, cartes, listes, aperçus) sans un seul paragraphe de discours. L'identité (l'acronyme F-T-2-E déployé) et le différenciateur principal du bureau (**la continuité conception-chantier** — « ce qui distingue FT2E d'un bureau d'études intervenant uniquement en amont ») n'existent que sur Société, page de second niveau.

### 1.3 Société est surchargée en « méthode »

Trois sections se chevauchent : « La proximité comme méthode » (marine), « La mission, en quatre temps », « Approche et méthodologie » (+ encart monotechnique). S'y ajoutent deux blocs qui serviraient mieux ailleurs : l'acronyme déployé (identité de premier regard → accueil) et l'encart « interventions monotechniques » (typologie d'offre → Expertises).

### 1.4 Les corps de texte `secteurs` ne sont rendus nulle part

La collection `secteurs` contient 6 fiches avec 2–3 paragraphes chacune, nourris des **faits vérifiés de la plaquette 2024** (1 686 logements, Clairsienne, Le Fougerou, Chênes Verts…). Un seul usage dans le code : `SecteursPhares` sur l'accueil, qui n'affiche que l'accroche. Le contenu le plus factuel du site est invisible.

### 1.5 Doublons textuels Société ↔ Équipe

Le parcours « stage de fin d'études avant d'y être embauchés » et la liste des secteurs apparaissent quasi verbatim sur les deux pages.

---

## 2. Approches envisagées

- **A. Supprimer l'index `/expertises`** (lien nav → ancre accueil). Rejetée : casse le sitemap, les breadcrumbs des 6 sous-pages, et prive le site d'une page pilier SEO.
- **B. Différenciation par altitude** (retenue) : l'accueil argumente, l'index Expertises devient une vraie page pilier, Société se recentre sur l'identité, les corps de texte secteurs obtiennent leurs pages. Aucun contenu nouveau à inventer — uniquement des déplacements et des enrichissements de rendu.
- **C. Enrichir uniquement l'accueil** (y remonter mission + approche + acronyme). Rejetée : l'accueil deviendrait interminable et `/expertises` resterait un doublon.

---

## 3. Design retenu — page par page

### 3.1 Accueil `/`

- **Ajout** d'un bloc `AcronymeFT2E` (nouveau composant `blocs/`, extrait de Société) après le cartouche chiffres : « Ce que le nom contient » — 4 lettres, 4 champs d'ingénierie + phrase de méthode (continuité conception → réception) avec lien vers `/expertises`. C'est le contenu d'identité qui manquait à la première impression.
- **Secteurs cliquables** : chaque ligne de `SecteursPhares` devient un lien vers `/secteurs/[slug]`.
- Le bloc devient un jalon `data-trace-jalon` supplémentaire du tracé de flux (mesure DOM automatique).
- Le bloc « Six expertises » reste en version compacte : le doublon est résolu en différenciant l'index, pas en appauvrissant l'accueil.

### 3.2 Expertises `/expertises` — de doublon à page pilier

Nouvelle structure :
1. `HeroPage` (inchangé).
2. **« L'approche »** : prose « Approche et méthodologie » déplacée de Société (phases d'intervention + continuité conception-chantier) + encart « interventions monotechniques » déplacé de Société (grille `[1fr_400px]`).
3. **Cartes enrichies** : variante `detaillee` de `CarteExpertise` — accroche complète (sans line-clamp) + 3 premiers livrables + affordance « livrables, méthode, FAQ → ». L'index montre ce que l'accueil ne montre pas.
4. **« Le déroulé d'une mission »** : les 4 temps (accompagnement / analyse / conception / suivi) déplacés de Société.
5. `CtaFinal` (inchangé).

### 3.3 Société `/societe` — recentrée sur l'identité

Structure conservée : Hero → « Le bureau d'études » (prose + fiche d'identité) → « Quatre piliers » → « La proximité comme méthode » (marine) → « Engagements énergétiques » → CTA.
Retraits : acronyme (→ accueil), « La mission, en quatre temps » (→ Expertises), « Approche et méthodologie » + monotechnique (→ Expertises), phrase « stage de fin d'études » (dédoublonnage, reste sur Équipe).

### 3.4 Secteurs — nouvelles pages `/secteurs/[slug]`

Gabarit unique `src/pages/secteurs/[...slug].astro` (6 pages statiques) :
- `HeroPage` (breadcrumb Accueil / secteur, eyebrow `secteur NN — sur 6`).
- Corps markdown de la fiche secteur (styles prose identiques aux sous-pages expertise) + colonne image duotone (`fs.existsSync` + placeholder) avec `CoinsCuivre`.
- Grille des projets du secteur (`projets` filtrés par `secteur`) + lien vers `/references`.
- `CtaFinal`.
- Pas d'entrée de navigation (pages satellites, comme les fiches projet). Sitemap généré automatiquement.

**Note de périmètre** : ces pages ne figuraient pas dans le sitemap V1 du PDF. Elles ne créent aucun contenu nouveau (rendu de fichiers `.md` existants) et sont supprimables en retirant un fichier. À faire valider par FT2E avant mise en production.

### 3.5 Équipe `/equipe`

Inchangée (le dédoublonnage se fait côté Société). L'écho « Sept profils, une responsabilité partagée » entre le teaser accueil et le h1 Équipe est conservé — c'est un rappel volontaire, pas un doublon de contenu.

---

## 4. Contraintes respectées

- Règle 8 : les nouvelles pages utilisent `HeroPage`.
- Design system blueprint : aucune nouvelle couleur, aucun rayon, grilles `gap-px bg-line`, hover cuivre.
- Voix éditoriale : aucun texte inventé hors phrases de liaison ; les contenus déplacés sont repris tels quels.
- Typographie française : espaces insécables et guillemets conservés dans les textes déplacés.
- SEO : `title`/`description` uniques pour les 6 pages secteur ; maillage interne renforcé (accueil → secteurs, expertises ↔ projets, secteurs → références).
- TraceFlux : jalons mesurés dans le DOM, l'ajout d'un jalon accueil est transparent.

## 5. Risques

- **Longueur de l'accueil** : +1 section. Compensée par la densité faible du bloc acronyme (une grille, une phrase).
- **Pages secteur hors sitemap V1** : signalées comme ajout à valider (cf. 3.4).
- **`docs/04-specifications-pages.md`** : mis à jour pour les pages 1, 2 et 4 + ajout de la section pages secteur.
