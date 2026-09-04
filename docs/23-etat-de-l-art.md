# État de l’art — FT2E v3 au 2026-08-17

> **Le chantier de réduction de dette est EN PAUSE** depuis le 2026-08-17, à la demande
> de l’utilisateur, au profit d’un chantier additif. Ce document est **le point de
> reprise** : il est autoportant, et une session neuve n’a besoin de rien d’autre pour
> savoir où en est le produit, ce qui reste ouvert, et ce qui ne doit pas être rouvert.

## 1. Ce que ce document est, et ce qu’il n’est pas

C’est un **relevé mesuré le 2026-08-17**, pas un résumé de plans. Chaque chiffre a été
remesuré ce jour-là ; aucun n’est recopié d’une session antérieure. **Là où la mesure
contredit un document du dépôt, c’est écrit et le document est nommé** — il y en a deux
cas, aux § 3 et § 4.

Ce n’est pas un plan : il ne prescrit aucun travail et n’ordonne rien. Il dit l’état, la
nature de chaque point ouvert, et qui peut le lever. Ce qu’on fait ensuite appartient à
l’utilisateur.

⚠ **Un état de l’art se remesure, il ne se recopie pas.** Celui-ci a trouvé **deux
affirmations fausses** dans des documents en vigueur. Qui le reprendra dans six mois
devrait faire de même plutôt que de le croire sur parole.

## 2. L’état du produit — mesuré le 2026-08-17

| Grandeur | Valeur | Instrument |
|---|---|---|
| Pages construites | **46** (+ `404.html`) | `npm run build` |
| Fiches de références | **23**, toutes réelles, zéro démo | `src/content/projets/*.md` |
| Autres contenus | 7 équipe · 7 secteurs · 4 expertises · 1 actualité | `src/content/` |
| Liens internes | **211, zéro mort** ; 23/23 fiches à 5 liens | `scripts/controle-liens-internes.py` |
| Planches | **23 dossiers, 115 pièces**, 6 archétypes en service | `public/images/projets/` |
| Régénération octet à octet | **23/23 compositeurs, 69/69 SVG identiques** | rejoué le 2026-08-17 |
| Typecheck | 0 erreur, 0 avertissement | `npm run typecheck` |
| Lighthouse mobile, 9 routes (2026-08-16) | perf **100**, CLS **0**, TBT **0** | sur le déploiement |
| Accessibilité | **100** partout sauf `/` 96 et `/societe/` 97 | exception D1, § 6 |
| SEO | **69** partout | verrou d’indexation, § 6 |
| LCP mobile | **1 656 à 1 815 ms** pour un budget de 1 800 | sept tirs, § 4 rang D |

**Statut des 23 affaires** : 14 `en cours`, 5 `livré`, 4 sans ligne `statut`. Une seule
cumule l’absence de `statut` **et** d’`annee_livraison` — la crèche de l’Oranger, § 4
rang B.

## 3. Ce qui est CLOS — à ne pas rouvrir

| Chantier | Clos le | Preuve |
|---|---|---|
| Les 23 fiches de références réelles | 2026-08-09 | 23 fiches, 23 numéros d’affaire relevés sur pièce |
| Les 23 planches de schéma de principe | 2026-08-15 | 23 planches, 23 mécanismes distincts |
| Réduction de dette, sessions S1 à S6 | 2026-08-16 | recettes mesurées, plan `2026-08-16-reduction-dette.md` |
| Recette d’ensemble avant présentation (S7) | 2026-08-16 | Lighthouse 9 routes, typographie du texte servi 0 écart |

### ⚠ Contradiction levée : la régénération des vingt planches est CLOSE

`docs/superpowers/plans/2026-08-12-chantier-planches-references.md` § Points ouverts
annonce, **au présent**, que « les vingt planches publiées avant la 21 n’ont pas été
régénérées » et que « l’invariant octet à octet ne tient plus ». Ce document date du
2026-08-15 et **n’a jamais été mis à jour**.

La session S2 du chantier de dette a fait la passe le 2026-08-16. Vérification refaite de
bout en bout **le 2026-08-17**, et non reprise de S2 : les 23 compositeurs rejoués,
**69 SVG sur 69 identiques à l’octet**, arbre de travail inchangé. L’invariant tient.

Le point ouvert le plus ancien du chantier des planches n’existe donc plus, et il figurait
pourtant encore comme candidat de travail dans le prompt de continuité de S8. **Un point
ouvert consigné dans le document du chantier qui l’a trouvé ne se referme pas tout seul
quand un autre chantier le règle.** Même famille de défaut que le commentaire OAuth qui a
traversé six sessions.

## 4. Ce qui est OUVERT — quatre rangs, classés par ce qui débloque

Le classement n’est pas par importance mais par **nature du blocage**, parce que c’est
elle qui dit à qui le point appartient.

### Rang A — hors du dépôt. Aucune ligne de code ne l’approche

**La connexion au CMS échoue.** Mesuré le 2026-08-16 et le 2026-08-17, inchangé :
`/admin/` répond `200` et l’interface Decap s’affiche, mais `/api/auth?provider=github`
rend `500` — « Configuration OAuth manquante : definir `OAUTH_GITHUB_CLIENT_ID` ».
Le bouton « Se connecter » est mort, donc la prise en main par FT2E ne peut pas commencer.

`api/auth.js` et `api/callback.js` sont justes, `public/admin/config.yml` pointe le bon dépôt depuis le
2026-08-10. **Ce qui manque vit dans deux consoles d’administration**, et seul
l’utilisateur y a accès (la CLI Vercel répond « Not authorized » sur cette machine, et
elle n’est pas installée). Trois gestes, détaillés avec leur commande de contrôle dans
`docs/22-prise-en-main-decap.md` § 0 :

1. callback `https://ft2e-v3.vercel.app/api/callback` sur l’OAuth App GitHub ;
2. `OAUTH_GITHUB_CLIENT_ID` et `OAUTH_GITHUB_CLIENT_SECRET` sur le projet Vercel ;
3. redéploiement.

⚠ **Ne pas ajouter un avertissement de plus.** Le fait est écrit dans `CLAUDE.md`, dans
`docs/22` § 0, dans le pré-vol du script de démonstration et en commentaire de
`config.yml`. Il a survécu six sessions **sous forme de commentaire** : un commentaire
n’échoue jamais. Ce qui manque est une exécution, pas une cinquième mention.

### Rang B — suspendu à une pièce ou à un arbitrage de FT2E

Les trois questions de **D2**, posées le 2026-08-16, **toujours sans réponse**, ajournées
à la présentation du projet à la demande explicite de l’utilisateur.

- **Réception de la crèche de l’Oranger** — `src/content/projets/creche-oranger-perigny.md`
  (affaire `23-075`, `annee` 2023) annonce une affaire livrée **sans dire quand** :
  `annee_livraison` vide et pas de ligne `statut`. **Seule des 23 dans ce cas**, vérifié
  le 2026-08-17. ⚠ **Ne jamais fabriquer de millésime.** C’est le premier des quatorze
  relevés qu’appelle l’échéance du § 5.
- **Les 25 visuels dans l’historique git** — le site ne les sert plus, le dépôt les
  porte encore. Les effacer demande une réécriture d’historique qui invalide tous les SHA
  cités dans les plans et les règles. Arbitrage, pas correction.
- **`planche-chiffree`** — seul archétype de la liste fermée du protocole que les 23
  planches n’ont pas exercé (vérifié le 2026-08-17 : six archétypes en service,
  celui-ci à zéro), donc **le seul dont rien ne garantit qu’il fonctionne**. Le retirer du
  protocole ou le redéfinir est un arbitrage éditorial.

### Rang C — suspendu à un événement extérieur

**Les 7 marqueurs `[DÉMO]`**, tous des `image_alt`, tous dans `src/content/secteurs/` —
un par secteur, vérifié le 2026-08-17. Ils marquent des visuels de démonstration générés
par IA et **se lèvent au reportage photographique**, pas par une validation FT2E. Les huit
photographies d’équipe sont dans le même cas.

### Rang D — exécutable dans le dépôt, sans attendre personne

**Les insécables du corpus dessiné — les `aria_label` sont FAITS le 2026-09-03, les deux
autres populations restent ouvertes.** ⚠ **Le compte dépend entièrement de la population
mesurée**, et les relevés antérieurs n'en nommaient qu'une. Remesuré sur les **47**
dossiers le 2026-09-03 :

| Population | Écarts | Dossiers | Servi au visiteur ? | État |
|---|---|---|---|---|
| Texte **lu** (`aria_label`) | **175** | 46 / 47 | oui, **prononcé par les lecteurs d'écran** | ✅ **corrigé le 2026-09-03** |
| Texte **dessiné** (`<text>` des SVG) | **64** | 27 / 47 | oui, à l'écran | ouvert |
| Champs éditoriaux du `planche.json` | 2 160 | 47 / 47 | non, ne sort jamais du dépôt | ouvert |

⚠ **Les 175 ne se comparent PAS aux 114 du relevé du 2026-08-17**, et pas seulement parce
que le corpus est passé de 23 à 47 dossiers : **le motif a changé.** Le relevé de 2026-08-17
ne comptait que les insécables *manquantes* ; celui-ci compte aussi les insécables **mal
caractérisées** — 18 fines (U+202F) posées devant une ponctuation double là où la règle du
dépôt veut une insécable large (U+00A0). Le motif canonique de
`injection-typographique.py` cherche `[ ]`, une espace **ordinaire littérale** : une fine
déjà posée lui est invisible et **passe tout contrôle sans être conforme**. Le corpus
portait donc deux conventions contradictoires pour le même cas, et aucun instrument ne
pouvait le dire. *Un relevé n'est comparable qu'à périmètre ET à motif constants* — c'est
la même leçon que le lexique de `releve-numeral.py`, qui a produit trois sous-comptes
avant qu'on la retienne.

Ce qui a été fait, et pourquoi cela seulement : `aria_label` **n'est jamais dessiné**.
`_tronc.py:219` et les six compositeurs ne l'écrivent qu'en attribut sur la racine SVG,
`PlancheReference.astro` le pose sur le conteneur de la vignette (`aria-hidden` à la
source), et **aucun appel à `_tronc.mesurer` ne le touche** : aucune géométrie n'en
dépend. Instrument rejouable, contrôle autant que correcteur :
`scripts/insecables-aria-planches.py` (sans argument il mesure, `--appliquer` il écrit ;
son lexique d'unités est **importé** de `injection-typographique.py`, jamais recopié).
Preuves de la passe : invariant 188/188 avant et après, 92 SVG identiques octet à octet
une fois l'`aria-label` retiré, blocs `controles` recalculés inchangés, et les 47 fiches
servant la chaîne corrigée sur ses **trois** chemins de rendu.

⚠ **Ne PAS lancer `scripts/injection-typographique.py` sur les deux populations
restantes** : il déplace le dessin, les compositeurs mesurant leurs chaînes pour poser la
géométrie et U+202F n'ayant pas la chasse d'une espace ordinaire. Le texte dessiné est un
chantier avec correction à la source, régénération des 47 dossiers, invariant octet **et
contrôle du rendu aux trois tailles de lecture** — c'est ce dernier point qui le sépare de
celui des `aria_label`, qui n'en avait structurellement pas besoin.

⚠ **Et l'insécable ne change presque rien à ce qui est PRONONCÉ.** Sur les 175 corrigées,
**3 seulement** modifient l'écoute : les séparateurs de milliers, qu'un synthétiseur lit
« un, trois cent dix-huit » sans elles. Les 145 espaces devant la ponctuation double sont
de la conformité typographique, inaudible — une insécable empêche un « : » de basculer en
début de ligne, et un `aria-label` n'est jamais mis en page. Le classement en rang D reste
juste (le champ **est** prononcé, et `french-editorial.md` l'inscrit explicitement dans son
périmètre), mais **ne pas le présenter comme un gain d'accessibilité qu'il n'est pas.** Le
passage NVDA ci-dessous doit d'ailleurs vérifier l'inverse : que U+202F ne gêne aucun
synthétiseur ni aucun afficheur braille.

**Le LCP mobile est AU seuil, pas sous le seuil.** Sept mesures sur les deux pages les
plus lourdes : 1 656, 1 658, 1 681, 1 768, 1 806, 1 807 et 1 815 ms pour un budget de
1 800. Elles se répartissent de part et d’autre du seuil **sans qu’aucune page ne soit
systématiquement du mauvais côté** — l’accueil bascule sur un tir, `/equipe/` sur un
autre. ⚠ **Ne pas traiter cela comme un défaut de `/equipe/`**, ce serait optimiser la
mauvaise page. La fiche projet descend à 1 068 ms.

**Deux pièces non suivies — TRANCHÉ le 2026-09-03 : ignorées**, motifs ancrés au
`.gitignore`. ⚠ L'énoncé antérieur de ce paragraphe était **périmé sur les deux moitiés** :
il nommait `docs/maquettes/`, suivi depuis (trois fichiers), et ignorait
`livrables/synthese-referencement-cliches-secteurs-2026-08-26.pdf`, apparu après. Les
pièces réellement en attente au 2026-09-03 étaient ce PDF et
`livrables/cv-ft2e/CV-FT2E.zip`.

⚠ **Ce que l'arbitrage a mis au jour, et qui reste OUVERT** : `livrables/cv-ft2e/` porte
**douze CV nominatifs déjà suivis** — six membres de l'équipe, en `.docx` et `.pdf` —,
c'est-à-dire des données personnelles dans l'historique d'un dépôt **partagé**, alors que
le motif `/cv/` du même `.gitignore` déclare qu'un CV ne se commite jamais. *La règle
existe et se contourne par un autre chemin.* Le motif ajouté vise donc le **ZIP seul** :
ignorer le dossier entier n'aurait rien retiré — un `.gitignore` est sans effet sur un
fichier suivi — et aurait seulement fait *paraître* ignoré ce qui reste versionné, soit un
motif qui ment sur son objet. Les retirer demande une réécriture d'historique : **arbitrage
de l'utilisateur, même statut que les 25 visuels du rang B.**

**Hors dette, questions de périmètre** : le formulaire de contact n’a pas de backend, et
le site n’est pas migré sur `ft2e.fr`. Procédure de migration et de levée du verrou SEO
dans `docs/19-migration-production.md`.

## 5. La seule échéance datée du dépôt

`src/lib/projets.ts` porte `MILLESIME_LIVRAISON_ANNONCE = 2026` et, juste en dessous, un
garde-fou qui **fait échouer le build au 1ᵉʳ janvier 2027** :

```ts
if (new Date().getFullYear() > MILLESIME_LIVRAISON_ANNONCE) {
  throw new Error(...);
}
```

Le site annonce cette année de livraison sur les **quatorze affaires** dont la réception
n’est pas prononcée. C’est **éditorial, pas factuel** : le frontmatter n’est pas touché,
`annee_livraison` reste vide et le schéma continue de l’interdire tant que `statut` vaut
« en cours ».

⚠ **Ne jamais répondre à cet échec en poussant la constante à 2027.** Cela désarmerait le
garde-fou pour s’épargner exactement l’échec qu’on lui demande de produire. La réponse est
d’aller relever les réceptions auprès de FT2E — c’est le rang B ci-dessus.

## 6. Décisions tranchées — à ne pas re-litiger

| Décision | Tranchée le | Où elle vit |
|---|---|---|
| **A9** — `/references` est une grille de cartes, pas une liste tabulaire | 2026-08-15 | `.claude/rules/tailwind-design-tokens.md` |
| **Localisation et chronologie** — commune + code postal, et « en cours » ne s’affiche plus | 2026-08-15 | `CLAUDE.md` règle 14 |
| **Le repli de lecture des planches est supprimé** — la figure est le dessin, son cartouche et l’agrandissement | 2026-08-15 | `docs/superpowers/specs/2026-08-16-responsive-planches-fiches.md` |
| **Exception D1** — `/` à 96 et `/societe/` à 97 sont admis ; l’exception porte sur le **motif** (complément de titre `aria-hidden`), pas sur une page | 2026-08-16 | `.claude/rules/accessibility-rgaa.md` |
| **SEO 69** — l’unique audit en échec est `is-crawlable`, c’est le verrou d’indexation voulu. Ne pas le « corriger » | 2026-08-16 | `docs/19-migration-production.md` |
| **Les deux déploiements antérieurs sont HORS PÉRIMÈTRE** (`ft2e-site`, `ft2e-v2`) | 2026-08-16 | `docs/19` § 6 bis, et là seulement |
| **Le chantier de dette est en pause**, au profit d’un chantier additif | 2026-08-17 | ce document |

## 7. Pièges d’outillage propres à cette machine

Ils coûtent tous une demi-session à qui les redécouvre.

- **Les compositeurs de planches exigent `PYTHONIOENCODING=utf-8`** (relevé le
  2026-08-17). Sans lui, 22 des 23 échouent sur `UnicodeEncodeError` en écrivant leur
  **rapport de contrôle** sur une console cp1252 — les fichiers, eux, sont écrits en
  UTF-8 explicite. L’erreur ressemble à un défaut de compositeur et n’en est pas :
  elle a fait conclure à tort, le 2026-08-17, que l’invariant de régénération était rompu.
- **Les insécables sont normalisées en entrée des outils d’édition, et pas de façon
  déterministe.** Écrire le contenu en clair avec des **jetons** pour les seuls caractères
  sensibles, les substituer en fin de course par `chr()`, et asserter que le source du
  script n’en contient **aucun en littéral** : s’il n’y en a pas, il n’y a rien qu’un
  outil ait pu normaliser en silence. Mesuré : les lettres accentuées, les guillemets,
  les flèches et les points de suspension traversent l’écriture intacts, **seules les
  insécables sont effacées**.
- **Un build vert ne prouve pas que le texte existe.** En S7 une passe de correction a
  détruit trois libellés en écrivant ses références arrière comme caractères de contrôle,
  et `npm run build` a produit ses 46 pages sans broncher. Après toute correction de
  texte, contrôler la **présence** du texte attendu.
- **Le dépôt est partagé et un hook `Stop` y commite et pousse seul.** « Rien n’est en
  attente de push » est une mesure **périssable** : en S8 elle est devenue fausse en
  trois heures. La rejouer **au moment de committer**.
- **Un marqueur de build prouve « pas plus ancien que », jamais « exactement ce
  commit ».** Pour trancher qu’un déploiement porte *le* commit en cours, il faut un
  marqueur introduit par ce commit-là.
- **La performance ne se mesure jamais sur `npm run preview`**, qui ne compresse rien :
  0,8 s de biais sur la chaîne bloquante. Sur le déploiement, et jamais sur un seul tir.
- **`npx lighthouse` n’accepte pas les chemins Git-Bash `/c/...`** en `--output-path` :
  il n’écrit rien, en silence. Et **`/tmp` n’existe pas depuis ce shell**.
- **Chrome refuse toute fenêtre sous 500 px, même en headless** : une capture à 390 px
  compose la page à environ 500 puis **rogne**, ce qui montre un débordement crédible et
  faux. Les largeurs de téléphone se mesurent par une **iframe** servie en même origine.
- **Tailwind v4 lit le `.gitignore`** et élague les répertoires qui y correspondent :
  tout motif doit être **ancré**. Contrôle :
  `git check-ignore -v src/pages/<dossier>/index.astro` doit ne rien rendre.

## 8. Comment reprendre

1. Lire ce document, puis **remesurer** ce qu’on s’apprête à toucher. Deux affirmations en
   vigueur se sont révélées fausses à la remesure du 2026-08-17.
2. Contrôler l’état du dépôt **en deux temps** (`git ls-remote origin master`, puis un
   marqueur de build dans le HTML servi), et le **rejouer au moment de committer**.
3. Le détail de chaque session close est dans
   `docs/superpowers/plans/2026-08-16-reduction-dette.md`, sections S1 à S8, avec le prompt
   de reprise de la dette en **annexe H**.
4. Recette de fin de session : `npm run typecheck` (0 erreur), `npm run build`
   (46 pages), `python scripts/controle-liens-internes.py` (0 lien mort), contrôle du
   **rendu** de toute page touchée à sa largeur de lecture. Si la session ne touche pas
   `src/`, le dire plutôt que de laisser croire à une recette non jouée.


---

# Remis à jour le 2026-08-27 — addendum (l'état ci-dessus reste celui du 2026-08-17)

Ce qui a changé depuis, en renvois — le détail vit dans les plans :

- **Chantier MOTION : arbitré, implémenté, mesuré, déployé le 2026-08-27**
  (amendements A11-A14 au registre de la charte ; LCP médian 1 705 ms, TBT
  0-100, CLS 0, a11y 96/D1). Restent : l'arbitrage de l'option 0 (filet de
  flux, TraceFlux débranché), la validation FT2E en situation, l'écoute NVDA.
  → `docs/superpowers/plans/2026-08-27-chantier-motion.md` (§ 6-7, annexes B-C).
- **/references** : deux navigations de filtre (rail + barre textuelle
  synchronisées par valeur), alignement par rangée d'en-tête partagée,
  remontée à l'ancre au filtrage hors de vue, correctif de la révélation
  (seuil au bord, jamais relatif — § 7 du plan motion).
  → § 10-12 de `docs/superpowers/plans/2026-08-17-chantier-bloc-secteurs.md`.
- **Taxonomie** : « Industriel », « Coordination SSI » en 5, et le secteur 6
  est « **Monotechnique — Audit** » depuis le 2026-08-27 (BREAKING `3a24cdf`).
- **Bloc secteurs** : ⚠ **les correspondances de clichés sont REÇUES et appliquées
  le 2026-09-04.** FT2E a versé son tableau `correspondance Site projet.odt`
  (61 lignes, une par cliché source) : les 44 clichés publiés y trouvent tous leur
  projet, **zéro clé orpheline**. 17 légendes génériques sont devenues des noms de
  projet, plus 3 reprises — dont un vrai défaut d'accessibilité, deux clichés du
  même secteur portant la même légende, donc indistinguables dans la liste que
  `CoupeSecteurs.astro` donne au lecteur d'écran. **Il ne reste que deux légendes
  descriptives** — « réseaux existants » et « sous-station » —, et c'est fidèle :
  le document FT2E ne nomme pas de projet pour ces deux-là non plus, ce sont des
  photographies d'organe et non d'ouvrage. ⚠ **Le gel du film n'est plus bloqué,
  mais il n'est pas fait** : le film est tiré au hasard à chaque déploiement
  (arbitrage D), le geler est un arbitrage, pas une conséquence. Restent les
  validations FT2E (liste au § 9 du plan bloc-secteurs) et le passage NVDA humain.
- **Decap** : blocage OAuth inchangé (`docs/22-prise-en-main-decap.md` § 0,
  trois gestes hors dépôt, ajournés en connaissance de cause).
- **NOUVEAU CHANTIER ouvert le 2026-08-27 : 27 nouvelles fiches références**
  (23 → 50), une session = un dossier, archives fournies par l'utilisateur
  (l'ancien fonds est supprimé). Pipeline, écarts aux protocoles fondateurs
  et prompt d'initialisation :
  → **`docs/superpowers/plans/2026-08-27-chantier-27-nouvelles-fiches.md`**.
- Le prompt opératoire de la reprise des chantiers accueil/motion reste
  l'annexe B du plan motion, lue avec ses compléments (annexe C, § 11-12 du
  plan bloc-secteurs).


---

# Addendum du 2026-09-03 — le chantier des références est CLOS à 47 fiches

*L'état ci-dessus reste celui du 2026-08-17, et l'addendum du 2026-08-27 celui du
chantier motion. Ce second addendum ne les remplace pas : il ajoute ce que les
vingt-quatre sessions du chantier des nouvelles fiches ont changé.*

- **47 fiches de références réelles**, 47 dossiers de planches complets, build 70 pages.
  ⚠ **Le compte qui fait foi est la mesure directe** — `ls src/content/projets/*.md | wc -l`
  — et rien d'autre. La formule « lignes du § Suivi du plan, plus vingt-trois », écrite ici
  le 2026-09-03 au matin, **a été retirée le soir même** : elle supposait qu'une session
  produit une fiche, ce qui a cessé d'être vrai à la N25 (session de clôture, aucune fiche)
  et lui faisait annoncer 48 pour 47.
- **Le chantier est CLOS à 47, par arbitrage de l'utilisateur rendu le 2026-09-03**, et
  non par renonciation de session. `2020.zip` n'existe pas ; les affaires `19-008` et
  `20-058` ne figurent dans aucune archive présente ; le classeur FT2E lui-même n'a jamais
  mené qu'à quarante-neuf affaires. **Aucune fiche n'a été fabriquée pour combler l'écart.**
  ⚠ Piste laissée ouverte à FT2E, à vérifier et non à supposer : la section
  « Finalisées en 2021 » du classeur est **entièrement vide** — seul millésime sans entrée,
  entre 2020 (deux) et 2022 (quatre).
- **Répartition sectorielle mesurée sur le déploiement** : L10 T14 I8 P3 C7 M7 E3, soit
  52 en pondéré (cinq fiches à double domaine comptent double). Les sept secteurs sont
  peuplés.
- **Archétypes de planches** : boucle-fluide 12 · coupe-traversée 11 · zonage-ssi 8 ·
  sankey-énergie 7 · tableau-électrique 7 · chronologie-affaire 2 · **planche-chiffrée 0,
  et son module n'existe toujours pas** — le point du rang B est inchangé, et il est
  désormais le seul archétype que 47 planches n'ont jamais exercé.
- `python scripts/planches/invariant.py` : **188/188** pièces identiques octet à octet.
  ⚠ Un dossier neuf non encore composé fait baisser le **numérateur** : lire le
  dénominateur avant de conclure à une régression.
- **Les insécables du corpus dessiné (rang D)** : le relevé du 2026-08-17 portait sur
  23 dossiers, il y en a 47. ⚠ **Ce point a été partiellement soldé le jour même, par la
  session N25** — les `aria_label` sont faits, le texte dessiné et les champs éditoriaux
  restent ouverts. Le § 4 rang D a été repris et fait foi ; ne pas lire ce point-ci
  comme si le chantier était entier.
- **L'échéance datée du § 5 porte désormais sur QUINZE affaires**, non quatorze :
  `MILLESIME_LIVRAISON_ANNONCE = 2026` s'affiche sur toutes les fiches dont la réception
  n'est pas prononcée sur pièce. ⚠ La réponse au build rouge du 1ᵉʳ janvier 2027 reste
  d'aller relever les réceptions, jamais de pousser la constante.
- **Le prompt de reprise ne porte plus de dossier** : annexe Y du plan du chantier. Il
  porte la question à poser à FT2E et la liste des points ouverts.


---

# Addendum du 2026-09-03, session N25 — la question posée à FT2E, et ce qu'elle a soldé

*La N25 ne produit aucune fiche : elle porte la question d'ouverture à l'utilisateur et
solde ce qu'elle peut. Quatre décisions rendues, trois exécutées le jour même.*

## Les quatre décisions

| Question | Décision rendue |
|---|---|
| Reste-t-il de la matière ? | **Non — clos à 47.** Ni recherche de `2020.zip`, ni versement hors classeur, ni question à FT2E sur 2021. L'écart de trois fiches à l'objectif initial de cinquante est **assumé et définitif.** |
| Chantier de la session | **Les insécables des `aria_label`** — la seule part du rang D exécutable sans arbitrage ni pièce à recevoir |
| Les deux pièces de `livrables/` | **Ignorées**, motifs ancrés |
| `2019.zip` | **Supprimé.** Le répertoire `ft2e_new_archives/` est désormais VIDE |

⚠ **PLUS AUCUNE ARCHIVE N'EXISTE SUR CE DISQUE.** Les cinq ZIP ont été supprimés — 2022
en fin de N23, trois autres hors session, 2019 en N25 sur décision de l'utilisateur.
Toutes leurs affaires étaient traitées : **aucune matière n'est perdue.** Mais plus aucune
vérification sur pièce n'est possible localement, pour aucune des 47 fiches — elle passera
désormais par l'utilisateur.

⚠ **La piste « Finalisées en 2021 » est VÉRIFIÉE, et NON LEVÉE.** Le classeur
`references/docs_references/REFERENCES SITE FT2E.ods` a été relu en N25 par `zipfile` sur
son `content.xml` : la section porte son en-tête de section **et** son en-tête de colonnes,
et **zéro ligne**. C'est le seul millésime vide, entre 2020 (deux entrées) et 2022
(quatre). Ce n'est donc pas une année sans affaires finalisées, c'est **une section jamais
remplie** — quelqu'un a préparé le tableau et ne l'a pas rempli. La question reste entière
pour FT2E ; l'utilisateur a choisi de ne pas la poser maintenant.

**Le classeur, remesuré sur pièce** : 50 lignes pour **49 affaires distinctes** — `23-075`
y figure deux fois (« Crêche de Périgny » en 2026, « Extension crêche Périgny UDAF » en
2025). Le compte de quarante-neuf est confirmé, et non repris de mémoire.

⚠ **Le classeur se contredit lui-même**, et c'est un piège pour qui le relira : sa cellule
« Nb Projet » annonce `L10 T11 I9 P2 C2 M8 E3 = 45`, quand ses propres lignes donnent
T = 15 et C = 7. *Un total agrégé ne se recalcule pas quand on ajoute des lignes sous lui*
— même famille que le compte de fiches de `CLAUDE.md`, faux treize sessions durant. **Ne
pas prendre ce 45 pour une mesure**, ni le confronter à la répartition du site.

## Ce que la N25 a livré, et à quel prix de preuve

175 écarts corrigés à la source sur les 47 `planche.json`, 47 dossiers régénérés, 138
pièces modifiées. La chaîne de preuve, dans l'ordre où elle a été faite : invariant
**188/188** avant → diff **confiné à 46 lignes, toutes des `aria_label`** → 47/47 dossiers
régénérés → **92 SVG identiques octet à octet une fois l'`aria-label` retiré** (donc aucun
dessin n'a bougé) → blocs `controles` recalculés **inchangés** (donc les compositeurs ont
mesuré la même géométrie) → invariant **188/188** rétabli → typecheck 0 erreur, build 70
pages → **47 fiches sur 47 servant la chaîne corrigée sur ses trois chemins de rendu** →
rendu contrôlé en capture à 390 et 1920 px.

⚠ **Deux contrôles ont crié à tort avant d'être corrigés**, et c'est la leçon
transportable de la session : le premier ne voyait pas l'échappement HTML (`&amp;` sur la
fiche `ateliers-pilotes-capsulae`), le second pas l'échappement CSS (`\.`, `\/` dans les
sélecteurs Tailwind). Dans les deux cas l'artefact était sain et l'instrument trop étroit.
**Quand un contrôle signale une régression, le suspecter avant de suspecter le dépôt** —
c'est le même défaut que le lexique de `releve-numeral.py`, sous une autre forme.

## Ce qui reste ouvert après la N25

Inchangé pour l'essentiel — le § 4 fait foi, et son rang D a été repris. En un coup d'œil :

- **Rang A** : Decap OAuth, trois gestes hors dépôt (`docs/22` § 0).
- **Rang B** : réception de la crèche de l'Oranger, les 25 visuels dans l'historique,
  `planche-chiffree` jamais exercé par 47 planches, validations FT2E du bloc secteurs,
  questions B et E des 24 fiches de collecte. **Et désormais les douze CV nominatifs**
  dans l'historique d'un dépôt partagé — voir le rang D, § « Deux pièces non suivies ».
- **Rang C** : les huit photographies d'équipe générées par IA.
- **Rang D** : le texte dessiné (64 écarts) et les champs éditoriaux (2 160) du corpus,
  le passage NVDA jamais fait par un humain, l'option 0 du motion (TraceFlux débranché),
  le LCP mobile au seuil.

## Addendum du 2026-09-04 — la N26 ouvre le chantier des six articles SEO

**Ce point de reprise avait un angle mort, et c'est le plus coûteux du projet :** il
recensait scrupuleusement ce qui restait ouvert *dans le dépôt*, et pas ce qui restait
dû *au contrat*. La Phase 4 de `docs/12-cadrage-jalons.md` n'est pas close, et son seul
critère de sortie qui ne dépende de personne d'autre était à **zéro sur six** : les six
articles SEO de lancement, inclus au périmètre non facturé (`docs/17`, PDF p. 23).

Aucun des quatre rangs ci-dessus ne le portait, parce qu'ils décrivent de la **dette** —
ce qui est là et qu'il faut réparer — et que ceci est de la **production** : ce qui
n'est pas là et qu'il faut faire. Un point de reprise trié par dette fait
systématiquement descendre la production sous le polissage.

### Ce que la mesure a trouvé, et qui a changé la nature du chantier

| | Avant la N26 | Après |
|---|---|---|
| Articles techniques publiés | **0** — la seule actualité porte `demo: true` | **2** |
| Pages piliers desservies par un article | **0 / 11** | **4 / 11** |
| Mécanisme de maillage pilier → article | **inexistant** | champ `piliers`, `src/lib/articles.ts`, `ArticlesLies.astro` |

`.claude/rules/seo-geo.md` exige 3 à 5 articles satellites par page pilier depuis
l'origine du projet. **La règle existait sans rien pour la porter** : aucun champ,
aucun rendu, aucun contrôle. Le chantier n'était donc pas « écrire six textes », c'était
« câbler six textes » — un article non maillé n'aurait servi ni le visiteur ni le
référencement.

### Deux affirmations non étayées, relevées sur les pages piliers

Le grep préalable à l'écriture — celui que le protocole des fiches impose et qui a payé
six sessions sur sept — a trouvé que le site **affirme déjà** ce que rien n'étaye :

- `expertises/electricite.md` : « la GTB permet de réduire les consommations de **15 à
  25 %** par le seul ajustement des plages horaires » ;
- `expertises/cvc.md`, FAQ : « la géothermie sur sondes verticales offre un meilleur
  rendement (**COP 4 à 5**) ».

Ce sont des ordres de grandeur de marché, qu'aucune pièce FT2E ne porte. Ils sont de la
**dette éditoriale antérieure**, pas un défaut du chantier — les deux articles de la N26
ne les reprennent pas. ⚠ **Le COP est au chemin direct de l'article n° 3** (PAC
aérothermique contre géothermique) : à arbitrer avant de l'écrire, faute de quoi
l'article contredira la page qu'il est censé servir. Trois issues au § 6 du plan.

### Ce qui reste ouvert après la N26

Les quatre rangs sont inchangés. S'y ajoutent, au **rang de production** :

- **quatre articles sur six** (PAC, Revit/EXE, décret tertiaire, IRVE) — sujets arrêtés
  par `docs/17` mais dits « à valider en cadrage » : les écrire n'est pas les valider ;
- ⚠ **six articles ne couvriront jamais onze piliers.** Même les six écrits, le cocon
  plafonnera vers 8 piliers sur 11, et aucun n'atteindra les 3 à 5 satellites demandés.
  C'est **structurel**, pas un défaut d'exécution : à dire à FT2E plutôt qu'à laisser
  découvrir — soit le périmètre s'arrête à six (il est contractuel), soit des articles
  supplémentaires font l'objet d'un devis ;
- **la Phase 5 reste non commencée** : formulaire sans backend, Plausible annoncé dans
  `/politique-confidentialite` sans qu'aucun script soit installé (report décidé par
  l'utilisateur le 2026-09-04), redirections 301, Search Console, formation CMS, DNS.

Plan du chantier, décisions et prompt de la N27 :
`docs/superpowers/plans/2026-09-04-chantier-six-articles-seo.md`.
