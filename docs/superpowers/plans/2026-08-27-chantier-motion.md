# Chantier motion — infléchissement de charte (ouvert le 2026-08-27)

Demande FT2E du 2026-08-27 : « le style est déjà très aride, des effets plus
marqués apporteraient un peu de dynamisme. » La charte v3 prescrit quatre
mouvements sur une courbe unique et interdit tout le reste ; un effet plus
marqué ne se glisse donc pas, il s'arbitre — au précédent d'A10, seul
déplacement au survol jamais admis, borné au registre des amendements.

**Statut : cadrage fait, pistes composées, EN ATTENTE DE L'ARBITRAGE FT2E.**
Aucune ligne du site n'est modifiée : la porte d'implémentation est la
validation client, posée au prompt d'ouverture du chantier.

## 1. Inventaire des mouvements — mesuré au dépôt le 2026-08-27

| # | Mouvement | Spécification | Implantation | État |
|---|---|---|---|---|
| 1 | Filet de flux | 900 ms, une fois par chargement, dashoffset -> 0, nœuds posés au passage | `TraceFlux.astro` (complet : ResizeObserver, reduced-motion, `astro:page-load`) | **ORPHELIN — monté nulle part** |
| 2 | Révélation de plan | 760 ms, 22 px, opacité + translation, une fois à l'entrée dans la vue | `initPlans` (BaseLayout) + `motion.css` ; 27 emplois `data-plan` sur 15 fichiers | actif partout |
| 3 | Survol de cellule | 300 ms, calcaire -> papier | `.cellule-liste`, `CarteExpertise` | actif |
| 4 | Survol de bouton | 260 ms, encre -> profond ; variantes filaire, chip, `.lien-texte` (soulignement 1 -> 2 px), `.champ` | `global.css` `@layer components` | actif |
| — | View Transitions | fondu uniforme 300 ms sur `<main>` | `BaseLayout` (`fade`) | actif |
| — | A10 — coupe des secteurs | largeur des tranches 300 ms + fondus 300 ms, délai d'intention 120 ms | `CoupeSecteurs.astro` | actif, borné |

Le fait saillant de l'inventaire : **le filet de flux, « seul tracé animé du
système », n'est monté nulle part.** Le composant est complet et entretenu,
mais plus aucune page ne l'importe depuis le commit `7562544` (2026-08-07,
« retouches éditoriales et visuelles demandées ») — **le retrait venait de
FT2E.** Conséquence de méthode : le réactiver n'est pas un amendement (le
mouvement est charté), mais exige une REVALIDATION explicite — on ne
rétablit pas en silence ce qu'un client a fait retirer.

## 2. Les contraintes qui bornent toute piste

- **LCP accueil AU seuil** (1 668-1 804 ms pour un budget de 1 800, tirs du
  2026-08-27) : aucune animation d'entrée sur le chemin du premier rendu du
  hero. La garde `plan-immediat` (tout ce qui est au-dessus du fold est posé
  d'emblée, sans fondu) est NON NÉGOCIABLE et s'étend à tout nouvel effet.
- **TBT < 200 ms, CLS < 0,05**, mesurés sur le DÉPLOIEMENT en tirs
  multiples : à l'entrée dans la vue, seules des propriétés composited
  bougent (opacité, transform) ; aucune animation de layout hors interaction
  (A10 reste la seule).
- **`prefers-reduced-motion` : suppression intégrale**, tout posé d'emblée ;
  fallback complet sans JavaScript (mécanisme `html.js-plans` existant).
- **La courbe unique reste.** L'infléchissement joue sur l'orchestration et
  l'amplitude, pas sur une seconde signature temporelle.
- **RGAA** : rien en boucle au-delà de 5 s, aucun sens porté par le seul
  mouvement.
- **Un dessin de planche ne bouge jamais à l'échelle** : la sur-échelle
  épaissit les filets de 1 px (défaut fondateur du dispositif des planches).
  Toute piste de survol est donc bornée aux PHOTOGRAPHIES.

## 3. Les pistes — indépendantes, chacune bornée

### Piste 1 — la cascade (amendement A11 pressenti)

Dans les grilles et listes significatives — cartes de références, cellules
d'expertises, colonnes de relevé, tuiles de filtres, grille équipe —, les
éléments d'un même groupe se révèlent EN CASCADE : délai de 80 ms par rang,
plafonné au sixième (au-delà, tout suit le dernier rang), mêmes 760 ms,
mêmes 22 px, même courbe. Orchestration du mouvement 2, aucune interdiction
levée. Ne touche pas : le hero, tout ce qui est visible au chargement, les
survols, les durées. Implémentation pressentie : `data-plan-groupe` sur le
conteneur, `initPlans` pose un `--rang` par enfant, `transition-delay` en
CSS.

### Piste 2 — le cliché qui répond (a : sans interdit levé ; b : amendement A12)

Sur les photographies en cadre (coupe des secteurs, tuiles de filtres,
cliché du hero) — jamais sur un dessin :

- **variante a** : au repos, un voile d'encre à 14 % ; il se lève au survol
  et au focus (opacité seule, 300 ms). Cousin du dévoilement déjà en place
  sur le rail (0,42 -> 0) ; aucun interdit levé.
- **variante b** : le cliché passe à l'échelle 1,025 en 400 ms dans un cadre
  strictement fixe — équerres, cartouche et cadre ne bougent pas (ce sont
  des frères de la boîte d'image, pas des enfants). Lève ponctuellement
  « aucun déplacement au survol » ; amendement au précédent d'A10 : une
  seule propriété, une portée nommée, tout le reste interdit.

### Piste 3 — la continuité (amendement A13 pressenti)

Le fondu uniforme de 300 ms devient un **fondu montant** : la page entrante
fond en montant de 12 px (350 ms, courbe unique). Sur le seul trajet
carte -> fiche de référence (et retour), **le visuel voyage** : un
`transition:name` partagé entre la boîte d'image de la carte et le bandeau
de la fiche. Rien au premier chargement — le LCP n'est pas concerné, les
View Transitions ne jouent qu'en navigation interne. Reduced-motion : fondu
simple ou bascule sèche.

### Option 0 — le filet de flux (revalidation, pas un amendement)

Réactiver `TraceFlux` sur l'accueil (marge gauche, sections 01 à 07, bureau
seulement — la marge n'existe pas au téléphone). Spécification existante
inchangée : 900 ms, une fois, décoratif, `aria-hidden`, aucun suivi du
défilement. À représenter à FT2E comme « le tracé qui revient » — c'est eux
qui l'avaient fait retirer en août.

## 4. Le support de validation

`docs/maquettes/ft2e-motion-pistes.html` — page autonome dans les jetons de
la charte (rampe recopiée en dur, comme dans les compositeurs de planches :
une maquette ne résout pas les `var()` du site), démonstrations jouables
(déclenchement à l'entrée dans la vue + boutons « rejouer »), piste 3 sur
l'API View Transitions du navigateur — celle-là même qu'emploie Astro.
Cliché réel du corpus secteurs retiré à 880 px
(`docs/maquettes/assets/cliche-demo.jpg`, 95 Ko). `prefers-reduced-motion` y
est respecté comme sur le site. Rendu et les quatre démonstrations contrôlés
au navigateur le 2026-08-27 (cascade, voile, micro-échelle, bascule
carte -> fiche avec voyage du visuel, tracé de flux). La page s'ouvre en
local d'un double-clic ; Google Fonts y est admis (maquette de `docs/`, hors
site — le site reste sur fontsource).

## 5. Ce qui suit l'arbitrage

- consigner chaque piste retenue en amendement A11+ au registre de
  `.claude/rules/tailwind-design-tokens.md`, DANS LE MÊME COMMIT que son
  implémentation (règle du dépôt) ;
- implémenter dans `src/styles/motion.css` + composants : `initPlans` de
  `BaseLayout` pour la cascade ; `global.css` / `CoupeSecteurs` / rail de
  `references/index` / `Hero` pour les survols ; `BaseLayout` +
  `CarteProjet` + fiche pour les View Transitions — pattern
  `astro:page-load` + guard `dataset.bound` pour tout script ;
- mesurer AVANT/APRÈS sur le déploiement : LCP accueil < 1 800 ms en tirs
  multiples, TBT < 200 ms, CLS < 0,05 ; Lighthouse accessibilité (96 attendu
  sur l'accueil, exception D1 — toute violation nouvelle est un blocage).

## Annexe A — prompt de la session suivante (à coller tel quel en session neuve)

````
Session de suite - FT2E v3 : arbitrage MOTION (implémentation si validé),
fin de légendes du bloc secteurs, NVDA, validations.

Contexte. FT2E v3 est un site institutionnel Astro statique (Astro 6,
Tailwind 4, TypeScript strict), déployé en démonstration client sur
https://ft2e-v3.vercel.app, indexation verrouillée par triple sécurité
(robots.txt Disallow, meta noindex, header X-Robots-Tag) - ne pas y toucher.
La source de vérité du design est .claude/rules/tailwind-design-tokens.md
(rampe monochrome 197, aucune couleur d'accent, filets 1 px par opacité,
rayon 0, courbe unique, amendements A1-A10). La réduction de dette est EN
PAUSE (docs/23-etat-de-l-art.md).

ÉTAT AU 2026-08-27 SOIR : le chantier MOTION est CADRÉ et EN ATTENTE
D'ARBITRAGE FT2E - plan docs/superpowers/plans/2026-08-27-chantier-motion.md
(inventaire, contraintes, bornes exactes), maquette d'arbitrage
docs/maquettes/ft2e-motion-pistes.html (s'ouvre en local d'un double-clic,
demonstrations jouables). Quatre pistes independantes :
  0. filet de flux reactive sur l'accueil (TraceFlux.astro existe, complet,
     ORPHELIN depuis le commit 7562544 - retire sur demande FT2E en aout,
     donc REVALIDATION explicite, pas un amendement) ;
  1. cascade - revelation sequencee des grilles, 80 ms par rang plafonne au
     sixieme, memes 760 ms / 22 px / courbe (amendement A11 pressenti) ;
  2. survol des photographies - a : voile d'encre 14 % qui se leve (300 ms,
     aucun interdit leve) ; b : micro-echelle 1,025 dans un cadre fixe
     (400 ms, amendement A12 au precedent d'A10). JAMAIS sur un dessin de
     planche : la sur-echelle epaissit les filets de 1 px ;
  3. transitions de pages - fondu montant 12 px / 350 ms partout + voyage du
     visuel carte->fiche via transition:name (amendement A13 pressenti).
     Rien au premier chargement, le LCP n'est pas concerne.
RIEN n'est implemente sur le site : c'etait la porte du chantier. Le relevé
d'arbre d'accessibilité du 2026-08-27 est au § 9 du plan bloc-secteurs.

LIRE D'ABORD : docs/superpowers/plans/2026-08-27-chantier-motion.md (bornes
completes des pistes, § 5 : marche a suivre) ; CLAUDE.md ;
.claude/rules/tailwind-design-tokens.md § Interactions & motion et § Les
amendements ; src/styles/motion.css ; src/layouts/BaseLayout.astro
(initPlans).

CE QUE CETTE SESSION FAIT :

1. RECUEILLIR L'ARBITRAGE FT2E piste par piste (leur montrer la maquette).
   PUIS, pour chaque piste retenue, dans le MEME commit : l'amendement A11+
   au registre de .claude/rules/tailwind-design-tokens.md ET son
   implementation - motion.css + initPlans (cascade : data-plan-groupe sur
   le conteneur, --rang par enfant, transition-delay en CSS) ; global.css /
   CoupeSecteurs / rail de references / Hero (survols) ; BaseLayout +
   CarteProjet + fiche (View Transitions). Exigences non negociables :
   prefers-reduced-motion INTEGRAL (tout pose d'emblee), fallback sans JS,
   pattern astro:page-load + guard dataset.bound, la cascade ne touche
   JAMAIS ce qui est au-dessus du fold (garde plan-immediat), et mesures
   AVANT/APRES sur le DEPLOIEMENT en tirs multiples : LCP accueil < 1 800 ms,
   TBT < 200 ms, CLS < 0,05. Consigner au plan motion par script APPEND.
   Si FT2E ecarte une piste, le consigner aussi - un refus est un arbitrage.

2. QUAND FT2E LIVRE LES CORRESPONDANCES RESTANTES (« on fixera quand je les
   aurai ») - 17 clichés encore en légende descriptive : villa urbaine
   (Logements) ; écomusée, tiers-lieu bois, pharmacie, siège d'entreprise,
   bureaux zinc doré (Tertiaire/ERP) ; centre technique, poste ferroviaire,
   site en plaine, atelier agro, chantier naval (Industriel) ;
   vidéoprotection, borne IRVE, hydraulique, calorifuge, caméras en façade
   (Monotechnique - Audit et EXE) ; passerelle (Patrimoine).
   a. Legender ces 17 comme les 27 premiers : legende de la planche si le
      projet a une fiche publiee (titre du planche.json), sinon composer
      dans le meme style, 40 signes au plus (borne Zod).
   b. PUIS GELER LE FILM avec FT2E : soit remplacer filmSecteur() par une
      lecture ordonnee du corpus (film = 4 premiers, l'ordre redevient
      editorial et Decap le pilote), soit garder le tirage une fois tout
      legende. Documenter le choix dans le meme commit.

3. NVDA - passage HUMAIN toujours du (exigence RGAA du depot). Le releve
   d'arbre d'accessibilite du 2026-08-27 (§ 9 du plan bloc-secteurs) a
   verifie la mecanique ARIA (rail : une legende par bouton + aria-pressed ;
   coupe : groupe nomme, boutons du film avec etat, compteur present ;
   cartes : vignette aria-hidden, nom = titre court + commune). Restent A
   L'ECOUTE, NVDA seul : l'annonce du compteur aria-live au fil du film,
   l'ordre de lecture de la coupe au clavier, la verbosite des noms de
   boutons du film, les FAQ des pages secteurs. Consigner le releve d'ecoute
   dans le plan bloc-secteurs (script APPEND). Si des pistes motion sont
   implementees, verifier a l'ecoute qu'aucune n'introduit d'annonce
   parasite.

4. RECUEILLIR LES VALIDATIONS FT2E, liste consolidee au § 9 du plan
   bloc-secteurs : 17 fichiers ecartes du corpus, artefacts
   d'agrandissement IA sur des cliches retenus, credit (c) FT2E, vedette a
   deux rangs, rail et mini-coupe « Tous », nouveaux intitules de secteurs
   en situation, cliche Aurora au hero et son absence assumee au telephone.

5. DECAP : la connexion echoue en production (HTTP 500 - deux variables
   OAuth Vercel et une callback GitHub manquantes,
   docs/22-prise-en-main-decap.md § 0, trois gestes que seul l'utilisateur
   peut faire, AJOURNES en connaissance de cause). Le rappeler UNE FOIS puis
   le respecter. Tout brouillon Decap anterieur au 2026-08-26 devra
   reprendre un secteur de la nouvelle enumeration (BREAKING de 8250827).

PIEGES VERIFIES, A NE PAS REDECOUVRIR (detail : CLAUDE.md et les rules) :
scripts de composant via astro:page-load + guard dataset.bound ; mesures en
CSS de composant, couleurs en classes litterales ; motifs .gitignore
ANCRES ; un build vert ne prouve pas le rendu (npm run captures -- --route
01-accueil ; Chrome refuse toute fenetre sous 500 px, meme headless - sonde
iframe, sa barre mange 15 px) ; la performance se mesure sur le DEPLOIEMENT,
jamais sur npm run preview, JAMAIS en un tir ; depot PARTAGE (git ls-remote
avant commit, marqueur de build dans le HTML servi apres push ; la CLI
Vercel repond Not authorized, c'est le push qui deploie) ; le hook Stop
commite et pousse SEUL ce qui traine sur le disque - supprimer les artefacts
d'instrument sitot lus ; les insecables sont normalisees par les outils
d'edition (docs : script Python en mode APPEND, chr(160) construit,
assertion apres coup ; source .astro : echappement JavaScript u00a0, jamais
le caractere) ; pas de commentaire JSX entre la parenthese d'une expression
et son element ; min-width: 0 sur les flex porteurs d'images ; TOUTE COTE DE
LA VEDETTE SE MESURE AU NAVIGATEUR ; display:none n'empeche PAS le
telechargement d'une image eager ; les trois SVG d'une planche sont trois
COMPOSITIONS, jamais des echelles - aucun effet d'echelle sur un dessin.

Recette de fin de session : npm run typecheck (0 erreur), npm run build
(46 pages), python scripts/controle-liens-internes.py (0 lien mort),
controle du RENDU des pages touchees aux largeurs utiles, Lighthouse mobile
sur le DEPLOIEMENT si la structure a change (accessibilite : 96 attendu sur
l'accueil, violation unique color-contrast du complement text-clair
aria-hidden - exception D1 ; toute violation NOUVELLE est un blocage ; LCP
accueil < 1 800 en tirs multiples), consignation par script append (plan
motion pour le point 1, plan bloc-secteurs pour les points 2-4).

Portees de commit : design-system (motion - amendement + implementation
ENSEMBLE), content, feat(accueil), feat(references), a11y, docs. Tout
changement de schema Zod va dans le MEME commit que public/admin/config.yml.

Termine par le prompt de lancement de la session suivante, en annexe du plan
du chantier concerne et reproduit integralement dans ton message final - la
regle de continuite est dans CLAUDE.md parce qu'elle a ete manquee deux fois.
````


## 6. Arbitrage rendu et implémentation — session du 2026-08-27 (suite immédiate)

FT2E a arbitré le jour même, sur la maquette : **piste 1 retenue, piste 2 en
variante a** (la micro-échelle b, présentée, n'est pas retenue), **piste 3
retenue** — plus deux demandes nouvelles sur l'accueil : les chiffres du
relevé en compteur avec survol en couleur, et une révélation des blocs plus
marquée et sensiblement plus lente. **L'option 0 (filet de flux) n'a pas été
arbitrée : TraceFlux reste débranché**, l'arbitrage est à recueillir.

Implémenté et déployé (commits `6a82961` à `ee1d813`, chaque amendement dans
le même commit que son implémentation) :

- **A11** — révélation 1000 ms / 28 px (le module de la trame) ; cascade des
  grilles de cartes (`data-plan-groupe` : accueil § 05, grille de
  `/references`, `ProjetsSimilaires`), 80 ms par rang en `:nth-child` pur,
  traîne plafonnée à 400 ms ; `plan-immediat` conservé (rien ne fond
  au-dessus de la ligne de flottaison).
- **A12** — voile d'encre 14 % sur les clichés-liens (hero, cliché principal
  de la coupe), levé au survol et au focus (300 ms) ; recette
  `.lien-cliche` / `.voile-cliche` dans `global.css` ; le rail et le film
  gardent leur voilage d'état 0,42.
- **A13** — fondu montant (entrante : 12 px / 350 ms ; sortante : 200 ms) ;
  voyage du visuel carte → fiche (`transition:name` = `planche-<slug>` des
  deux côtés). ⚠ Piège mesuré : **Astro anime les paires nommées avec SA
  courbe par défaut** (`cubic-bezier(0.76, 0, 0.24, 1)`, 180 ms) — les deux
  porteurs du nom passent un `transition:animate` explicite (fondu croisé
  350 ms, courbe unique, sans translation — le déplacement est au groupe).
  Tout futur `transition:name` doit faire de même.
- **A14** — les quatre chiffres du relevé de l'accueil se comptent une fois
  à l'entrée dans la vue (900 ms, courbe unique évaluée numériquement —
  l'unique compteur du site, interdit nominal levé) ; au survol la cellule
  bascule papier → calcaire et le chiffre monte d'un rang de la rampe
  (encre → profond / pivot → encre). Span animé `aria-hidden`, valeur
  finale au HTML et en `sr-only` ; `prefers-reduced-motion` pose tout.
- **Documentation normative alignée** dans la foulée : CLAUDE.md (§ Motion
  design, § Quoi exactement, en-tête design system), `accessibility-rgaa.md`
  (§ Mouvement), `astro-conventions.md` (compteur), registre des amendements
  « six d'application (A9 à A14) ».

**Recette jouée** : typecheck 0 erreur, build 46 pages, 0 lien mort ;
contrôles fonctionnels au navigateur sur le preview (cascade : délais
mesurés 0/80/160/240 ms, durée 1 s ; voile : 0,14 au repos, 0 au survol ;
compteurs : valeurs finales exactes ; paire nommée : 350 ms sur la courbe
unique dans le style injecté). **Mesures sur le DÉPLOIEMENT** (marqueur du
dernier commit vérifié dans le HTML servi) : accueil mobile, cinq tirs —
perf 98/99/99/100/100, **LCP 1962 / 1710 / 1705 / 1704 / 1664 ms** (médiane
1705 — l'état « au seuil » documenté est tenu, l'outlier est le tir froid),
**TBT 0-100 ms**, **CLS 0** (les compteurs ne décalent rien — chiffres
tabulaires en cellule fixe) ; accessibilité **96** avec pour unique
violation le `color-contrast` du complément `text-clair` `aria-hidden`
(motif exact de l'exception D1) ; `/references/` **100**.

Reste ouvert : l'arbitrage de l'option 0 ; la validation du motion EN
SITUATION par FT2E sur le déploiement ; le passage NVDA humain (dont deux
points nouveaux : le compteur A14 doit rester muet au lecteur d'écran, les
View Transitions ne doivent pas introduire d'annonces parasites).

## Annexe B — prompt de la session suivante (REMPLACE l'annexe A)

````
Session de suite - FT2E v3 : retours FT2E sur le motion en situation,
option 0 (filet de flux), fin de légendes du bloc secteurs, NVDA,
validations.

Contexte. FT2E v3 est un site institutionnel Astro statique (Astro 6,
Tailwind 4, TypeScript strict), déployé en démonstration client sur
https://ft2e-v3.vercel.app, indexation verrouillée par triple sécurité
(robots.txt Disallow, meta noindex, header X-Robots-Tag) - ne pas y toucher.
La source de vérité du design est .claude/rules/tailwind-design-tokens.md
(rampe monochrome 197, aucune couleur d'accent, filets 1 px par opacité,
rayon 0, courbe unique, amendements A1-A14). La réduction de dette est EN
PAUSE (docs/23-etat-de-l-art.md).

ÉTAT AU 2026-08-27 SOIR : le chantier MOTION est ARBITRÉ, IMPLÉMENTÉ ET
DÉPLOYÉ (commits 6a82961..ee1d813, § 6 du plan motion
docs/superpowers/plans/2026-08-27-chantier-motion.md) :
  A11 revelation 1000 ms / 28 px + cascade des grilles (data-plan-groupe,
      80 ms par rang en :nth-child, plafond 400 ms, plan-immediat conserve) ;
  A12 voile d'encre 14 % sur les cliches-liens (hero + cliche principal de
      la coupe), leve au survol/focus - variante b (micro-echelle) REFUSEE ;
  A13 fondu montant 12 px / 350 ms + voyage du visuel carte->fiche
      (transition:name planche-<slug> des deux cotes) ;
  A14 compteurs du releve de l'accueil (900 ms, une fois, aria-hidden +
      sr-only) + survol : fond papier->calcaire, chiffre monte d'un rang.
Mesures deploiement : LCP median 1705 ms (budget au seuil tenu), TBT
0-100 ms, CLS 0, a11y 96 accueil (motif D1 unique), 100 /references.
L'OPTION 0 (filet de flux, TraceFlux.astro) N'EST PAS ARBITREE : le
composant reste debranche. La maquette d'arbitrage est
docs/maquettes/ft2e-motion-pistes.html.

LIRE D'ABORD : le § 6 du plan motion (dont le piege Astro des paires
nommees) ; CLAUDE.md ; .claude/rules/tailwind-design-tokens.md § Les
amendements (A11-A14) et § Interactions & motion ; src/styles/motion.css.

CE QUE CETTE SESSION FAIT :

1. RECUEILLIR LES RETOURS FT2E SUR LE MOTION EN SITUATION (leur faire
   parcourir le deploiement : accueil - compteurs, cascade, voile du hero
   et de la coupe ; /references -> une fiche - voyage du visuel ; retour).
   Ajuster finement si demande (durees, amplitude, delai de cascade) - tout
   ajustement reste dans les bornes des amendements A11-A14, ou les amende
   dans le meme commit. RECUEILLIR AUSSI l'arbitrage de l'OPTION 0 (filet
   de flux) : s'il revient, le monter sur l'accueil (marge gauche, sections
   01-07, bureau seul), spec existante inchangee, SANS amendement (mouvement
   deja charte) ; s'il est ecarte, le consigner et envisager la suppression
   de TraceFlux.astro (un composant orphelin arbitre n'est pas une reserve).

2. QUAND FT2E LIVRE LES CORRESPONDANCES RESTANTES (« on fixera quand je les
   aurai ») - 17 clichés encore en légende descriptive : villa urbaine
   (Logements) ; écomusée, tiers-lieu bois, pharmacie, siège d'entreprise,
   bureaux zinc doré (Tertiaire/ERP) ; centre technique, poste ferroviaire,
   site en plaine, atelier agro, chantier naval (Industriel) ;
   vidéoprotection, borne IRVE, hydraulique, calorifuge, caméras en façade
   (Monotechnique - Audit et EXE) ; passerelle (Patrimoine).
   a. Legender ces 17 comme les 27 premiers : legende de la planche si le
      projet a une fiche publiee (titre du planche.json), sinon composer
      dans le meme style, 40 signes au plus (borne Zod).
   b. PUIS GELER LE FILM avec FT2E : soit remplacer filmSecteur() par une
      lecture ordonnee du corpus (film = 4 premiers, l'ordre redevient
      editorial et Decap le pilote), soit garder le tirage une fois tout
      legende. Documenter le choix dans le meme commit.

3. NVDA - passage HUMAIN toujours du (exigence RGAA). Le releve d'arbre
   d'accessibilite du 2026-08-27 (§ 9 du plan bloc-secteurs) a verifie la
   mecanique ARIA. Restent A L'ECOUTE : compteur aria-live du film de la
   coupe, ordre de lecture de la coupe au clavier, verbosite des boutons du
   film, FAQ des pages secteurs - PLUS deux points nes du motion : le
   compteur A14 doit etre MUET au lecteur d'ecran (span anime aria-hidden,
   valeur en sr-only), et les View Transitions ne doivent introduire aucune
   annonce parasite. Consigner l'ecoute au plan bloc-secteurs (script
   APPEND).

4. RECUEILLIR LES VALIDATIONS FT2E, liste consolidee au § 9 du plan
   bloc-secteurs : 17 fichiers ecartes du corpus, artefacts
   d'agrandissement IA, credit (c) FT2E, vedette a deux rangs, rail et
   mini-coupe « Tous », intitules de secteurs, cliche Aurora au hero et son
   absence au telephone - plus la validation du motion (point 1).

5. DECAP : la connexion echoue en production (HTTP 500 - deux variables
   OAuth Vercel et une callback GitHub manquantes,
   docs/22-prise-en-main-decap.md § 0, trois gestes que seul l'utilisateur
   peut faire, AJOURNES en connaissance de cause). Le rappeler UNE FOIS puis
   le respecter. Tout brouillon Decap anterieur au 2026-08-26 devra
   reprendre un secteur de la nouvelle enumeration (BREAKING de 8250827).

PIEGES VERIFIES, A NE PAS REDECOUVRIR (detail : CLAUDE.md et les rules) :
Astro anime les paires transition:name avec SA courbe par defaut - tout
nouveau nom porte un transition:animate explicite DES DEUX COTES (courbe
unique), et les noms sont uniques par page ; le grep d'une classe a variante
dans dist/ echappe le deux-points (group-hover\:text-profond) ; scripts de
composant via astro:page-load + guard dataset.bound ; mesures en CSS de
composant, couleurs en classes litterales ; motifs .gitignore ANCRES ; un
build vert ne prouve pas le rendu ; la performance se mesure sur le
DEPLOIEMENT, JAMAIS en un tir (le tir froid est un outlier : 1962 vs 1664-
1710 sur les quatre suivants) ; depot PARTAGE (git ls-remote avant commit,
marqueur de build du DERNIER commit dans le HTML servi apres push) ; le hook
Stop commite et pousse SEUL ce qui traine - artefacts d'instrument dans le
scratchpad, jamais dans le depot ; les insecables sont normalisees par les
outils d'edition (docs : script Python APPEND, chr(160), assertion) ; pas de
commentaire JSX entre la parenthese d'une expression et son element ;
min-width: 0 sur les flex porteurs d'images ; TOUTE COTE DE LA VEDETTE SE
MESURE AU NAVIGATEUR ; display:none n'empeche PAS le telechargement d'une
image eager ; les trois SVG d'une planche sont trois COMPOSITIONS - aucun
effet d'echelle ni voile sur un dessin ; astro preview rend des 404
intermittents sur les liens sans barre finale (trailingSlash always) - un
artefact de preview, pas un defaut du site.

Recette de fin de session : npm run typecheck (0 erreur), npm run build
(46 pages), python scripts/controle-liens-internes.py (0 lien mort),
controle du RENDU des pages touchees aux largeurs utiles, Lighthouse mobile
sur le DEPLOIEMENT si la structure a change (accessibilite : 96 attendu sur
l'accueil, violation unique color-contrast du complement text-clair
aria-hidden - exception D1 ; toute violation NOUVELLE est un blocage ; LCP
accueil ~1700 en tirs multiples, TBT < 200, CLS < 0,05), consignation par
script append (plan motion pour le point 1, plan bloc-secteurs pour les
points 2-4).

Portees de commit : design-system (motion), content, feat(accueil),
feat(references), a11y, docs. Tout changement de schema Zod va dans le MEME
commit que public/admin/config.yml ; tout amendement de charte va dans
.claude/rules/tailwind-design-tokens.md dans le meme commit que son
implementation.

Termine par le prompt de lancement de la session suivante, en annexe du plan
du chantier concerne et reproduit integralement dans ton message final - la
regle de continuite est dans CLAUDE.md parce qu'elle a ete manquee deux fois.
````
