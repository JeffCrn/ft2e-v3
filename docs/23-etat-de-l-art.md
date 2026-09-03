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

**Les insécables du corpus dessiné.** ⚠ **Le compte dépend entièrement de la population
mesurée**, et les relevés antérieurs n’en nommaient qu’une. Remesuré le 2026-08-17 :

| Population | Écarts | Dossiers | Servi au visiteur ? |
|---|---|---|---|
| Texte **dessiné** (`<text>` des 69 SVG) | **12** | 8 / 23 | oui, à l’écran |
| Texte **lu** (`aria-label` des 69 SVG) | **114** | 22 / 23 | oui, **prononcé par les lecteurs d’écran** |
| Champs éditoriaux du `planche.json` | 602 | 23 / 23 | non, ne sort jamais du dépôt |

Les 114 des `aria-label` ne figuraient dans aucun relevé antérieur, et ce sont les plus
conséquents : c’est de l’accessibilité, pas de la mise en page. ⚠ **Ne PAS lancer
`scripts/injection-typographique.py` sur ce corpus** : il déplace le dessin, les
compositeurs mesurant leurs chaînes pour poser la géométrie et U+202F n’ayant pas la
chasse d’une espace ordinaire. C’est un chantier avec correction à la source,
régénération des 23 dossiers et contrôle du rendu aux trois tailles de lecture.

**Le LCP mobile est AU seuil, pas sous le seuil.** Sept mesures sur les deux pages les
plus lourdes : 1 656, 1 658, 1 681, 1 768, 1 806, 1 807 et 1 815 ms pour un budget de
1 800. Elles se répartissent de part et d’autre du seuil **sans qu’aucune page ne soit
systématiquement du mauvais côté** — l’accueil bascule sur un tir, `/equipe/` sur un
autre. ⚠ **Ne pas traiter cela comme un défaut de `/equipe/`**, ce serait optimiser la
mauvaise page. La fiche projet descend à 1 068 ms.

**Deux pièces non suivies** dans des répertoires qui ne sont pas ignorés :
`livrables/cv-ft2e/CV-FT2E.zip` et `docs/maquettes/`. Sans incidence sur le build. Trois
issues chacune : suivre, ignorer, retirer. Décision de l’utilisateur, pas défaut à
corriger.

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
- **Bloc secteurs** : restent les 17 correspondances de clichés à légender
  puis le gel du film, les validations FT2E (liste au § 9 du plan
  bloc-secteurs), le passage NVDA humain.
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
  Le compte qui fait foi est le § Suivi du plan
  (`docs/superpowers/plans/2026-08-27-chantier-27-nouvelles-fiches.md`), plus vingt-trois ;
  il se mesure par `ls src/content/projets/*.md | wc -l`.
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
- **Les insécables du corpus dessiné (rang D) grossissent avec le corpus** : le relevé du
  2026-08-17 portait sur 23 dossiers, il y en a 47. Le chantier est inchangé dans sa
  nature — correction à la source, régénération, invariant, contrôle du rendu aux trois
  tailles — mais son volume a doublé.
- **L'échéance datée du § 5 porte désormais sur QUINZE affaires**, non quatorze :
  `MILLESIME_LIVRAISON_ANNONCE = 2026` s'affiche sur toutes les fiches dont la réception
  n'est pas prononcée sur pièce. ⚠ La réponse au build rouge du 1ᵉʳ janvier 2027 reste
  d'aller relever les réceptions, jamais de pousser la constante.
- **Le prompt de reprise ne porte plus de dossier** : annexe Y du plan du chantier. Il
  porte la question à poser à FT2E et la liste des points ouverts.
