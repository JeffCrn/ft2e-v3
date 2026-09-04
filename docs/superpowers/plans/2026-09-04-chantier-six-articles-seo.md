# Chantier des six articles SEO de lancement

> Ouvert le 2026-09-04 (session N26). **Le critère de sortie est celui de la
> Phase 4 de `docs/12-cadrage-jalons.md` : six articles publiés.** Deux le sont.

## 1. Pourquoi ce chantier, et pourquoi maintenant

La Phase 4 n'est pas close, et **le seul de ses critères de sortie qui soit
entièrement dans notre camp était à zéro** : six articles SEO dus, aucun écrit.
Les trois autres critères sont soit atteints (47 fiches pour 30 dues, Lighthouse
conforme), soit hors dépôt (Decap testé par FT2E, bloqué par l'OAuth).

⚠ Le tri qui a désigné ce chantier n'est pas « ce qui est exécutable sans
attendre personne » — ce critère favorise le polissage et écarte la production,
et il a été redressé par l'utilisateur en N25. Le tri est **le critère de sortie
non atteint**.

## 2. Le constat qui a changé la nature du chantier

Mesure du 2026-09-04, avant tout travail :

| | Avant N26 | Après N26 |
|---|---|---|
| Articles techniques publiés | **0** (1 actualité, `demo: true`) | **2** |
| Pages piliers desservies par un article | **0 / 11** | **4 / 11** |
| Mécanisme de maillage pilier → article | **inexistant** | champ `piliers` + `ArticlesLies` |

**Le chantier n'était donc pas « écrire six textes », c'était « câbler six
textes ».** `.claude/rules/seo-geo.md` exige 3 à 5 articles satellites par page
pilier ; la règle existait sans rien pour la porter. Un article non maillé
n'aurait servi à rien, ni au visiteur ni au référencement.

## 3. Les décisions rendues — à ne pas re-litiger

### 3.1 Le lien se déclare une seule fois, sur l'article (arbitrage du 2026-09-04)

L'article porte `piliers`, une liste de un à trois chemins en graphie d'URL ; la
première entrée est le **pilier principal**, celle dont il est le satellite au
sens du PDF. Les pages piliers ramassent ce qui les désigne.

Le dessin symétrique — un champ `articles_lies` sur `expertises` et `secteurs` —
a été présenté et **écarté**. Ce dépôt a déjà refusé deux fois cette forme (titre
court de planche, alternative de vignette) : c'est toujours la copie, jamais
l'original, qui se désynchronise. Ne pas la réintroduire pour gagner la maîtrise
de l'ordre d'affichage — cet ordre est **calculé** dans `src/lib/articles.ts`, et
il est dérivé du contrat du champ.

### 3.2 Énumération fermée, et non chaîne libre

`PILIERS` (`src/content.config.ts`) liste les onze chemins. Un pilier inexistant
devient **impossible par construction** au lieu d'être détectable au rendu. Les
deux collections sont de cardinalité fixe (4 expertises, 7 secteurs).

⚠ **C'est en contrepartie une liste à tenir** : toute page d'expertise ou de
secteur ajoutée, renommée ou retirée se reporte dans `PILIERS` **et** dans
`public/admin/config.yml`, au sein du même commit. Le commentaire le dit — mais
un commentaire n'échoue jamais, d'où le § suivant.

### 3.3 Deux garde-fous, chacun sur un trou que l'autre ne voit pas

`src/lib/articles.ts` casse le build dans deux cas, **tous deux exercés en N26** :

| Cas | Ce que l'autre mécanisme ne voit pas | Sonde |
|---|---|---|
| chemin d'appel inconnu du disque | — | prop remplacée par `/expertises/PAS-UN-PILIER` → build code 1 |
| article désignant un pilier absent du disque | **l'énumération Zod valide une chaîne, pas un fichier** : une page renommée lui est invisible | `etude-thermique.md` retiré → build code 1 |

La liste attendue est **dérivée des collections elles-mêmes**, jamais recopiée
depuis l'énumération : comparer une copie à une copie n'aurait rien mesuré.

### 3.4 La règle de sourçage — la plus stricte du chantier

**Un article n'a pas de dossier d'affaires.** Il ne peut s'appuyer que sur :

- les **47 fiches déjà publiées**, elles-mêmes sourcées pièce par pièce — c'est
  la matière principale, et elle est abondante ;
- le **texte réglementaire** lui-même, cité comme tel.

Rien d'autre. Pas de chiffre de marché, pas de « généralement », pas d'ordre de
grandeur inventé. **Toute valeur est reprise à la graphie du corpus, jamais
recalculée** : un recalcul introduirait une source qui n'existe à aucun dossier.

⚠ **Le grep de `src/content/` avant d'écrire n'est pas facultatif**, et il a payé
en N26 : les pages piliers **affirment déjà** des choses que rien n'étaye. Deux
relevées, et non reprises dans les articles :

- `expertises/electricite.md` — « la GTB permet de réduire les consommations de
  **15 à 25 %** par le seul ajustement des plages horaires » : chiffre de marché,
  aucune pièce FT2E derrière ;
- `expertises/cvc.md` (FAQ) — « la géothermie sur sondes verticales offre un
  meilleur rendement (**COP 4 à 5**) » : même statut.

Ces deux affirmations sont **de la dette éditoriale existante**, pas un défaut
introduit par le chantier. Les reprendre dans un article l'aurait propagée. Elles
restent à arbitrer avec FT2E (voir § 6).

### 3.5 Le bloc ne se rend pas quand le pilier n'a pas de satellite

Un titre de section suivi d'un vide se lit comme une page en panne, pas comme un
fonds à venir. Sept piliers sur onze sont dans ce cas aujourd'hui.

## 4. Ce qui est fait — session N26 du 2026-09-04

### Infrastructure (commit `0a9d060`, portée `seo(cocon)`)

- `src/content.config.ts` — constante `PILIERS` (11 chemins, ordre du site :
  expertises puis secteurs, chacun par `ordre` croissant) et champ
  `piliers: z.array(z.enum(PILIERS)).min(1).max(3).optional()`.
- `public/admin/config.yml` — widget `select` multiple, 11 options
  `{label, value}` (première occurrence de cette forme dans le fichier), libellés
  relus sur les `titre` réels des fichiers de contenu.
- `src/lib/articles.ts` — `articlesDuPilier()`, résolution, ordre et les deux
  garde-fous.
- `src/components/blocs/ArticlesLies.astro` — le bloc de pied, posé sur les deux
  gabarits piliers avant `CtaFinal`.

### Articles (commit `de1c87d`, portée `content(actualites)`)

| № | Article | Pilier principal | Rattachement |
|---|---|---|---|
| 1 | RE2020 en logement collectif : trois leviers de conception | `/expertises/etude-thermique` | `/secteurs/logements` |
| 2 | Coordination SSI en ERP de cinquième catégorie : ce qui change | `/secteurs/coordination-ssi` | `/secteurs/tertiaire-erp` |

Les deux rapportent une **régularité mesurée sur le corpus**, non une généralité
de métier — c'est ce qui les rend sourçables et citables :

- le premier : sur les opérations visant une labellisation à dix pour cent, la
  consommation d'énergie primaire dégage 27 à 44 % de marge quand **sa part non
  renouvelable borne à 1,1 point** (Maubec) et 3,68 points (Pas des Bœufs) ;
- le second : trois établissements **tous en cinquième catégorie** reçoivent
  l'alarme de type 4 (Salignac), de type 3 (Saintes) et un système de catégorie A
  à type 1 (Pierre Loti). Ce n'est pas la catégorie qui décide, c'est le type.

### Recette

| Contrôle | Résultat |
|---|---|
| `npm run typecheck` | **0 erreur**, 107 hints (base 105 mesurée par `git stash`, + 2 `ts(6385)` sur les deux `z` de la ligne de champ) |
| `npm run build` | **72 pages** |
| Onze valeurs Zod ↔ Decap | **identiques caractère pour caractère et dans le même ordre**, par comparaison calculée |
| Bloc rendu sur `dist/`, 11 piliers | **0 écart** — présent sur les 4 desservis, absent sur les 7 autres |
| Sondes des deux garde-fous | build **code 1** dans les deux cas |
| `controle-liens-internes.py` | **0 lien mort**, 400 liens, 47/47 fiches à 5 liens |
| Liens internes par article | **7** et **9** distincts, seuil de 5 |
| `releve-numeral.py` | **0** nombre composé écrit en lettres |
| `injection-typographique.py` | apostrophes droites restantes **0** |
| Lighthouse a11y (mobile, preview) | **100/100 sans violation** sur `/secteurs/logements/`, `/expertises/etude-thermique/` et une page d'article |
| Rendu | captures à 1920/1440/768/390 — bloc, index, deux articles |

## 5. Ce qui reste — quatre articles

Sujets arrêtés par `docs/17-perimetre-livrable.md` (PDF p. 23).
⚠ **Ils y sont dits « à valider en cadrage » : les écrire n'est pas les
valider.** Ne pas s'en autoriser un septième.

| № | Sujet | Pilier principal | Rattachement suggéré |
|---|---|---|---|
| 3 | Choisir entre PAC aérothermique et géothermique | `/expertises/cvc` | `/secteurs/logements` |
| 4 | Études d'exécution sur Revit : retours d'expérience | `/secteurs/etudes-execution-bim` | `/expertises/cvc` |
| 5 | Décret tertiaire 2030 : où en êtes-vous ? | `/expertises/audit-diagnostic` | `/secteurs/tertiaire-erp` |
| 6 | IRVE et bornes de recharge en logement collectif neuf | `/expertises/electricite` | `/secteurs/logements` |

Matière relevée au 2026-09-04 (`grep -ril` sur `src/content/`) :

- **PAC / géothermie** — 25 fichiers, dont `chaufferie-ecole-la-flotte-en-re`,
  `place-des-chenes-verts-saint-rogatien`, `atelier-dufour-yachts-perigny`,
  `cabanes-urbaines-la-rochelle` (PAC réversible 70 kW en relève de chaudière).
- **Revit / EXE** — 37 fichiers, dont `exe-residence-horizon-mediatim` (quinze
  diffusions de janvier à avril 2026), `plan-comptage-energie-airbus-rochefort`,
  `ancien-siege-communautaire-marennes`.
- **Décret tertiaire** — 7 fichiers seulement, dont
  `centre-formation-ormeau-du-pied-saintes` (décret Éco Énergie Tertiaire du
  23 juillet 2019, audit dédié au contrat), `audit-chambre-des-metiers-la-rochelle`,
  `cuisine-groupe-scolaire-villedoux`. **C'est le sujet le plus mince du lot** :
  vérifier la matière avant de s'engager, et prévoir de s'appuyer davantage sur
  le texte réglementaire.
- **IRVE** — 9 fichiers, dont `bornes-irve-la-rochelle-saintes`,
  `habitat-inclusif-salignac-sur-charente` (fourreaux sur 100 % des places,
  22 kVA réservés), `logements-pas-des-boeufs-bois-plage` (90 kVA installés,
  71 kVA après foisonnement, recharge comprise).

Après ces quatre, le cocon atteindra au mieux **8 piliers sur 11** desservis, et
aucun n'aura les 3 à 5 satellites que `seo-geo.md` demande. **C'est structurel :
six articles ne couvrent pas onze piliers.** Le dire à FT2E plutôt que de le
laisser découvrir — soit le périmètre s'arrête à six (il est contractuel), soit
des articles supplémentaires font l'objet d'un devis (`docs/17` § « hors
périmètre »).

## 6. Points ouverts nés de ce chantier

1. **Deux affirmations non étayées sur les pages piliers** (§ 3.4) : la GTB à
   « 15 à 25 % » et le COP « 4 à 5 » de la géothermie. Aucune pièce FT2E ne les
   porte. ⚠ **Le COP est au chemin direct de l'article n° 3** — l'arbitrer avant
   de l'écrire, ou l'article devra contourner la FAQ de sa propre page pilier.
   Trois issues : retirer le chiffre, le remplacer par une valeur relevée au
   corpus (`fougerou-sainte-marie-de-re` porte « 4,65 de COP »), ou le faire
   confirmer par FT2E comme ordre de grandeur assumé.
2. **L'article de lancement porte `demo: true` et 0 lien interne**, sous le seuil
   de 5 de `seo-geo.md`. Il est antérieur au chantier et hors de son périmètre.
   À arbitrer : le mailler et lever son `demo`, ou le laisser tel quel.
3. **Une carte seule occupe un tiers de la largeur** du bloc à 1920 px. Le motif
   est **déjà celui de `/actualites`**, qui n'a affiché qu'une carte pendant tout
   le projet — le changer ici créerait l'incohérence. Ne se résorbera pas
   complètement : plusieurs piliers n'auront qu'un article.

## Annexe A — prompt de lancement de la session N27

> Autoportant : collé dans une session neuve, il ne suppose aucun contexte des
> précédentes. Reproduit intégralement dans le message final de la N26,
> conformément à la règle de continuité de `CLAUDE.md`.

```
Session N27 - FT2E v3. CHANTIER DES SIX ARTICLES SEO, 2 FAITS SUR 6.
Cette session ecrit les articles 3 et 4, ou 3 a 6 si la matiere tient.
Elle ne produit AUCUNE fiche de reference : ce chantier-la est CLOS a 47.

Contexte. FT2E v3 est le site institutionnel du bureau d'etudes FT2E (La
Rochelle), Astro 6 statique, deploye en demonstration client sur
https://ft2e-v3.vercel.app (indexation verrouillee par triple securite -
robots.txt, meta noindex, header X-Robots-Tag : NE PAS Y TOUCHER sans
validation FT2E, procedure dans docs/19-migration-production.md).

POURQUOI CE CHANTIER. La Phase 4 de docs/12-cadrage-jalons.md n'est pas
close, et son seul critere de sortie entierement dans notre camp etait a
zero : six articles SEO dus, aucun ecrit. Deux le sont depuis la N26.
/!\ NE PAS TRIER LES CHANTIERS PAR " EXECUTABLE SANS ATTENDRE PERSONNE " -
ce critere favorise le polissage et ecarte la production. Trier par
CRITERE DE SORTIE NON ATTEINT.

ETAT MESURE AU 2026-09-04, apres la N26
- 47 fiches, 72 pages au build, typecheck 0 erreur (107 hints = ligne de
  base depuis la N26 ; elle etait de 105 avant, +2 ts(6385) sur les deux
  occurrences de `z` de la ligne du champ `piliers`).
- 3 actualites : 1 de lancement (demo: true, 0 lien interne) et les 2
  articles techniques de la N26 (demo: false, 7 et 9 liens).
- Cocon semantique : 4 des 11 pages piliers desservies, contre 0 avant.
- controle-liens-internes : 0 mort, 400 liens, 47/47 fiches a 5 liens.
- releve-numeral : 0 nombre compose ecrit en lettres.

LIRE D'ABORD, dans cet ordre
1. docs/superpowers/plans/2026-09-04-chantier-six-articles-seo.md EN
   ENTIER - le plan de ce chantier, avec ses decisions et ses pieges.
2. .claude/rules/french-editorial.md EN ENTIER - la voix et la regle des
   nombres, qui est MESUREE et non decretee.
3. .claude/rules/seo-geo.md § Cocon semantique.
4. CLAUDE.md et les six fichiers de .claude/rules/.

LES QUATRE ARTICLES QUI RESTENT - sujets ARRETES par docs/17 (PDF p. 23)
  3. Choisir entre PAC aerothermique et geothermique
     -> pilier /expertises/cvc, rattachement /secteurs/logements
  4. Etudes d'execution sur Revit : retours d'experience
     -> pilier /secteurs/etudes-execution-bim, rattachement /expertises/cvc
  5. Decret tertiaire 2030 : ou en etes-vous ?
     -> pilier /expertises/audit-diagnostic, rattachement /secteurs/tertiaire-erp
  6. IRVE et bornes de recharge en logement collectif neuf
     -> pilier /expertises/electricite, rattachement /secteurs/logements
/!\ docs/17 les dit " a valider en cadrage ". Les ecrire n'est pas les
valider : le signaler, ne pas s'en autoriser un septieme.

/!\/!\ LA QUESTION A POSER EN OUVERTURE, AVANT D'ECRIRE L'ARTICLE 3.
La FAQ de sa propre page pilier - src/content/expertises/cvc.md - affirme
" la geothermie sur sondes verticales offre un meilleur rendement (COP 4
a 5) ". AUCUNE PIECE FT2E NE PORTE CE CHIFFRE : c'est un ordre de
grandeur de marche, et la regle de sourcage de ce chantier l'interdit.
L'article ne peut donc ni le reprendre ni l'ignorer sans se contredire
avec la page qu'il est cense servir. Trois issues, a soumettre :
  (a) retirer le chiffre de la FAQ et n'en garder que le comparatif
      qualitatif ;
  (b) le remplacer par une valeur relevee au corpus - fougerou-sainte-
      marie-de-re porte " 4,65 de COP " (a RELIRE sur pieces avant
      usage, le chiffre est cite ici de seconde main) ;
  (c) le faire confirmer par FT2E comme ordre de grandeur assume, et le
      marquer comme tel.
La meme question se pose, sans urgence, pour expertises/electricite.md :
" la GTB permet de reduire les consommations de 15 a 25 % ".

/!\/!\ LA REGLE DE SOURCAGE, ET ELLE EST STRICTE. Un article n'a pas de
dossier d'affaires. Il ne peut s'appuyer que sur :
  - les 47 fiches DEJA PUBLIEES (elles-memes sourcees piece par piece) -
    c'est la matiere principale, et elle est abondante ;
  - le texte reglementaire lui-meme, cite comme tel.
NE RIEN AVANCER QUI NE SOIT DANS L'UNE DES DEUX. Pas de chiffre de
marche, pas de " generalement ", pas d'ordre de grandeur invente. TOUTE
VALEUR SE REPREND A LA GRAPHIE DU CORPUS, JAMAIS RECALCULEE : un recalcul
introduit une source qui n'existe a aucun dossier.
Le grep de src/content/ AVANT d'ecrire n'est pas facultatif - c'est lui
qui a trouve les deux affirmations non etayees ci-dessus.
Plus aucune archive n'existe sur ce disque : toute verification sur piece
passe par l'utilisateur.

/!\ MATIERE MESUREE PAR SUJET (grep -ril sur src/content/, 2026-09-04)
  PAC/geothermie  25 fichiers - chaufferie-ecole-la-flotte-en-re,
    place-des-chenes-verts-saint-rogatien, atelier-dufour-yachts-perigny,
    cabanes-urbaines-la-rochelle (PAC reversible 70 kW en releve).
  Revit/EXE       37 fichiers - exe-residence-horizon-mediatim (quinze
    diffusions janvier-avril 2026), plan-comptage-energie-airbus-rochefort,
    ancien-siege-communautaire-marennes.
  Decret tertiaire  7 fichiers SEULEMENT - centre-formation-ormeau-du-
    pied-saintes (decret Eco Energie Tertiaire du 23 juillet 2019),
    audit-chambre-des-metiers-la-rochelle, cuisine-groupe-scolaire-
    villedoux. C'EST LE SUJET LE PLUS MINCE DU LOT : verifier la matiere
    AVANT de s'engager, et prevoir de s'appuyer sur le texte reglementaire.
  IRVE            9 fichiers - bornes-irve-la-rochelle-saintes, habitat-
    inclusif-salignac-sur-charente (fourreaux sur 100 % des places,
    22 kVA reserves), logements-pas-des-boeufs-bois-plage (90 kVA
    installes, 71 kVA apres foisonnement, recharge comprise).

LE MECANISME DE MAILLAGE EXISTE DEPUIS LA N26 - ne pas le rebatir
Un article declare ses piliers UNE SEULE FOIS, au frontmatter :
    piliers:
      - /expertises/cvc          # le pilier principal, en PREMIER
      - /secteurs/logements      # rattachement secondaire
Enumeration FERMEE de 11 chemins (constante PILIERS, src/content.config.ts,
doublee dans public/admin/config.yml). Les pages piliers ramassent ce qui
les designe, via src/lib/articles.ts et le bloc ArticlesLies.astro.
/!\ NE PAS ajouter de champ `articles_lies` sur expertises ou secteurs :
ce dessin symetrique a ete presente et ECARTE le 2026-09-04 - c'est
toujours la copie, jamais l'original, qui se desynchronise.
/!\ Toute page d'expertise ou de secteur ajoutee ou renommee se reporte
dans PILIERS ET dans config.yml, DANS LE MEME COMMIT (sous-agent
content-modeller). Deux garde-fous cassent le build si on l'oublie ; ils
ont ete exerces en N26, ne pas les desarmer.

LE GABARIT (schema Zod, src/content.config.ts, collection actualites)
  titre       5-80 signes   - 50-70 vise, factuel, jamais racoleur
  chapo       40-280 signes - 2-3 phrases qui annoncent sans resumer
  date        ISO 8601
  auteur      optionnel - " L'equipe FT2E " (aucun membre n'est distingue)
  categories  enum - " Article technique " pour les quatre
  piliers     1 a 3 chemins, le principal en premier
  en_avant    booleen - false
  demo        booleen - FALSE, ce sont de vrais articles
/!\ AUCUN champ image, et c'est DELIBERE (2026-08-16) : un champ qu'un
editeur remplit sans qu'il paraisse nulle part promet une illustration
que le site ne sert pas. Ne pas le retablir.
Nom de fichier : YYYY-MM-titre-court.md, kebab-case sans accents.
Minimum 5 liens internes contextuels par article (les deux de la N26 en
ont 7 et 9) : la page pilier, 2 a 3 fiches, une expertise voisine.

PIEGES D'OUTILLAGE DE CETTE MACHINE - ils ne se redecouvrent pas
- /!\ QUAND UN CONTROLE CRIE, SUSPECTER LE CONTROLE AVANT LE DEPOT. Six
  fausses alertes en trois sessions, toutes venant de l'instrument. En
  N26 : un script de mesure du cocon a annonce " 0 / 11 " apres le
  cablage, parce que glob rend des chemins Windows a antislash et que la
  construction de slug produisait " /expertises/expertises\cvc ". Un
  instrument plus etroit que son objet rend un chiffre PLAUSIBLE, pas une
  erreur. Parade : donner a l'instrument des asserts qui le font ECHOUER
  quand il ne sait pas lire (aucun antislash, exactement 11 entrees, la
  marque cherchee doit se trouver au moins une fois).
- /!\ Les insecables ne s'ecrivent JAMAIS en litteral dans une source :
  les outils d'ecriture les normalisent de facon non deterministe. Ecrire
  l'article SANS, puis lancer
      python scripts/injection-typographique.py <fichier.md>
  qui pose U+00A0 et U+202F, courbe les apostrophes et rend un compte
  ( " droites restantes 0 " attendu ). Il protege les cles YAML et les
  valeurs d'enumeration.
- /!\ Les gros heredocs bash echouent sur cette machine, et un heredoc
  MANGE LES ANTISLASH d'un script Python (releve en N26 sur un
  `'\\' not in s` devenu une chaine non terminee). Ecrire les scripts par
  l'outil d'ecriture, dans le scratchpad.
- /!\ Un script du scratchpad ne resout pas node_modules par le nom :
  importer puppeteer-core par CHEMIN ABSOLU, et c'est
  node_modules/puppeteer-core/lib/puppeteer/puppeteer-core.js
  (il n'y a PAS de segment esm/ - erreur commise en N26).
- /!\ astro preview rend 304 sur une page deja vue : un test
  `status() !== 200` echoue alors A TORT. Poser setCacheEnabled(false)
  et tolerer 304.
- `npm run captures` EXISTE pour un jeu multi-paliers : NE PAS LE
  REBATIR. Sa table ROUTES est CURATEE (14 gabarits) et --route filtre
  sur le nom de DOSSIER de cette table. Les pages d'article de la N26
  n'y sont pas ; une sonde puppeteer jetable a suffi.
- /!\ LES BACKTICKS D'UN MESSAGE DE COMMIT SONT EXECUTES PAR BASH quand
  on passe par -m " ... ". Passer par `git commit -F <fichier>`, immunise.
- La CLI vercel repond " Not authorized " : c'est le PUSH qui deploie.
  Verifier par un MARQUEUR DU BUILD, jamais par un delai - par exemple
  que /actualites/<slug-du-nouvel-article>/ repond 200. Depot PARTAGE :
  rejouer git status au moment de committer.
- npm run preview NE MESURE PAS LA PERFORMANCE (aucune compression,
  0,8 s de biais). La performance se mesure sur le deploiement.
- PYTHONIOENCODING=utf-8 devant toute commande python qui imprime des
  accents.

RECETTE ATTENDUE - la meme qu'en N26, § 4 du plan
  npm run typecheck            0 erreur (107 hints = ligne de base)
  npm run build                le nombre de pages augmente d'autant
  python scripts/controle-liens-internes.py      0 lien mort
  python scripts/releve-numeral.py              0 compose en lettres
  python scripts/injection-typographique.py     droites restantes 0
  liens internes distincts par article          >= 5
  Lighthouse a11y sur une page pilier touchee   100/100 sans violation
  rendu contrôle a 1440 et 390 (regle 11 : un build vert ne prouve pas
  que la page s'affiche)

CE QUI RESTE OUVERT PAR AILLEURS (docs/23-etat-de-l-art.md § 4 fait foi)
  RANG A - hors depot : Decap OAuth casse en production (HTTP 500,
    " Configuration OAuth manquante "). Rien en cause dans le depot :
    trois gestes hors depot, docs/22-prise-en-main-decap.md § 0.
  RANG B - suspendu a FT2E : reception de la creche de l'Oranger (NE
    JAMAIS FABRIQUER UN MILLESIME), les 25 visuels dans l'historique,
    planche-chiffree jamais exerce, les validations du bloc secteurs, les
    questions B et E des 24 fiches de collecte, et les DOUZE CV
    NOMINATIFS de livrables/cv-ft2e/ - donnees personnelles dans
    l'historique d'un depot partage, alors que le motif /cv/ du
    .gitignore declare qu'un CV ne se commite jamais. Leur retrait
    demande une reecriture d'historique : arbitrage, pas correction.
  RANG C - les huit photographies d'equipe generees par IA.
  RANG D - POLISSAGE, ne pas le prendre avant la production : le texte
    dessine (64 ecarts) et les champs editoriaux (2 160) des planches, le
    passage NVDA jamais fait par un humain, l'option 0 du motion
    (TraceFlux debranche), le LCP mobile au seuil.
  PHASE 5 non commencee : formulaire de contact sans backend, Plausible
    ANNONCE dans /politique-confidentialite mais AUCUN script installe
    (report decide par l'utilisateur le 2026-09-04), redirections 301,
    Search Console, formation CMS 2 h, bascule DNS ft2e.fr.

/!\/!\ L'ECHEANCE DATEE, ET LA SEULE MANIERE D'Y REPONDRE.
src/lib/projets.ts porte MILLESIME_LIVRAISON_ANNONCE = 2026 et un
garde-fou qui FAIT ECHOUER LE BUILD AU 1er JANVIER 2027, sur les quinze
affaires dont la reception n'est pas prononcee (mesurer :
grep -L annee_livraison src/content/projets/*.md | wc -l).
/!\ NE JAMAIS pousser la constante a 2027 : cela desarmerait le garde-fou
pour s'epargner l'echec qu'on lui demande de produire. La reponse est
d'aller relever les receptions - rang B.

APRES LES SIX ARTICLES - a dire a FT2E, pas a decouvrir
Six articles ne couvrent pas onze piliers. Meme les six ecrits, le cocon
plafonnera vers 8 piliers sur 11, et aucun n'aura les 3 a 5 satellites
que seo-geo.md demande. C'est STRUCTUREL, pas un defaut d'execution. Soit
le perimetre s'arrete a six - il est contractuel, docs/17 p. 23 -, soit
des articles supplementaires font l'objet d'un devis.

Portee de commit : content(actualites) pour les articles, seo(...) pour
le maillage, docs(...) pour le point de suivi. Un changement de schema
Zod passe par le sous-agent content-modeller et va dans le MEME commit
que public/admin/config.yml.

Terminer par le prompt de lancement de la session suivante, en annexe du
plan et reproduit integralement dans le message final - la regle de
continuite est dans CLAUDE.md parce qu'elle a ete manquee deux fois.
```
