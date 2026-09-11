# Chantier du monogramme — approche du mot et signature

> Ouvert le 2026-09-06 sur **demande client**, à la clôture du chantier des six
> articles. **C'est le chantier immédiat de la session N28** — il remplace le
> prompt Decap/Phase 5 de l'annexe B du plan des articles, qui est reporté.

## 1. La demande, telle qu'elle a été transmise

FT2E demande deux modifications du monogramme tel qu'il est posé :

1. **Resserrer légèrement l'écartement** entre les caractères du mot F T 2 E,
   jugé un peu trop espacé.
2. **Changer la signature** sous le mot, jugée trop générique et trop longue —
   « ça dépasse en longueur le logo au-dessus ». À la place de
   « BUREAU D'ÉTUDES TECHNIQUES », trois pistes à tester, sur une ou deux
   lignes :
   - « BUREAU FLUIDES »
   - « BUREAU FLUIDES ET THERMIQUE »
   - « BET FLUIDES & THERMIQUES »

⚠ **Les deux graphies transmises portent une coquille** — « BUREU » et
« TERMIQUES ». Elles sont rétablies ci-dessus et dans tout ce document ; le
libellé exact reste à arrêter (§ 5, arbitrage D).

## 2. L'état mesuré au 2026-09-06 — avant tout travail

### 2.1 Le dépôt ne dévie pas de la charte : il la transcrit

`src/components/layout/Logo.astro` est la **transcription exacte du dessin de
référence de la charte** — vérifié caractère par caractère contre
`branding-v3-bis/FT2E-charte-graphique-rev2.1-source.html`, qui porte le même
verrouillage `viewBox="0 0 330 90"` :

| | Charte (source HTML) | `Logo.astro` |
|---|---|---|
| Groupe de la marque | `translate(5,5)`, `stroke-width="7"` | identique |
| Chemins du cadre et du flux | identiques | identiques |
| Groupe du mot | `translate(104,16)` | identique |
| Lettres T, 2, E | `translate(35,0)`, `(72,0)`, `(107,0)` | identiques |
| Signature | `x="104" y="74" font-size="8.5" letter-spacing="2.6"` | identique |
| Texte de signature | `BUREAU D'ÉTUDES TECHNIQUES` | identique |

**Conséquence directe, et elle commande tout le chantier : les deux demandes ne
corrigent pas une dérive d'implémentation, elles modifient la charte.** Voir § 3.

### 2.2 Le client a raison sur la longueur, et c'est mesurable

Mesures prises au navigateur, dans la police réellement chargée par le site
(IBM Plex Mono par fontsource — l'instrument échoue si la police n'est pas
prête, pour ne pas mesurer un repli), en unités du `viewBox` de 330 :

**Largeur d'encre du mot FT2E : 131,0 unités.**

| Libellé | Signes | Unités | vs le mot |
|---|---|---|---|
| **BUREAU D'ÉTUDES TECHNIQUES** (actuelle) | 26 | **200,2** | **× 1,53** |
| BUREAU FLUIDES | 14 | **107,8** | **× 0,82** ✅ |
| BUREAU FLUIDES ET THERMIQUE | 27 | **207,9** | × 1,59 ⛔ |
| BET FLUIDES & THERMIQUES | 24 | **184,8** | × 1,41 |
| BET FLUIDES & THERMIQUE | 23 | 177,1 | × 1,35 |
| BET FLUIDES ET THERMIQUE | 24 | 184,8 | × 1,41 |
| FLUIDES ET THERMIQUE | 20 | 154,0 | × 1,18 |
| FLUIDES · THERMIQUE · ÉLECTRICITÉ | 33 | 254,1 | × 1,94 |
| *2 lignes* — BET FLUIDES / & THERMIQUE | 11 / 11 | 84,7 / 84,7 | × 0,65 ✅ |
| *2 lignes* — BUREAU FLUIDES / ET THERMIQUE | 14 / 12 | 107,8 / 92,4 | × 0,82 / × 0,71 ✅ |

**Ce que la mesure tranche, et qu'il faut dire à FT2E :**

- la signature actuelle fait **une fois et demie la largeur du mot** — la gêne
  est réelle et chiffrée ;
- **des trois pistes proposées, une seule tient sur une ligne** :
  « BUREAU FLUIDES » ;
- **« BUREAU FLUIDES ET THERMIQUE » est plus longue que l'actuelle** (207,9
  contre 200,2) : elle aggrave exactement le défaut qu'elle vient corriger ;
- « BET FLUIDES & THERMIQUES » gagne 22 % mais dépasse encore le mot de 41 % ;
- **sur deux lignes, toutes les pistes tiennent.** C'est le réglage qui ouvre le
  plus grand choix de libellés.

### 2.3 L'approche du mot est uniforme, et le « 2 » ne fait pas exception

Soupçon écarté par la mesure : le 2 étant tracé **au trait** (7 unités) quand F,
T et E sont **pleins**, on pouvait craindre que les `translate` ne donnent pas
les écarts optiques. Ils les donnent — le dessin compense déjà.

| Glyphe | Encre (trait compris) | Largeur |
|---|---|---|
| F | 104,0 → 128,0 | 24,0 |
| T | 139,0 → 165,0 | 26,0 |
| 2 | 176,0 → 200,0 | 24,0 |
| E | 211,0 → 235,0 | 24,0 |

**Les trois écarts optiques valent 11,0 unités, exactement, et les écarts
nominaux aussi.** Resserrer l'approche est donc un reparamétrage à une seule
variable — appelons-la `g` :

```
T  →  translate(24 + g, 0)
2  →  translate(50 + 2g, 0)
E  →  translate(74 + 3g, 0)
largeur d'encre du mot = 98 + 3g
```

Contrôle : `g = 11` redonne 35 / 72 / 107 et 131,0 — les valeurs en place.

| `g` | translates | largeur du mot | écart |
|---|---|---|---|
| 11 (actuel) | 35 / 72 / 107 | 131,0 | — |
| 9 | 33 / 68 / 101 | 125,0 | − 4,6 % |
| 8 | 32 / 66 / 98 | 122,0 | − 6,9 % |
| 7 | 31 / 64 / 95 | 119,0 | − 9,2 % |

« Légèrement » situe vraisemblablement le réglage entre 8 et 9. **À trancher à
l'œil, sur épreuve, aux trois tailles d'emploi** (44 px en navigation, 60 px au
pied, 30 px en forme cadre) — une approche ne se juge pas sur un tableau.

## 3. Pourquoi c'est un amendement de charte, et non une retouche

Le § 07 de la charte 2.1 prescrit le monogramme au détail. Trois de ses phrases
portent directement sur ce chantier :

- **« Le mot est dessiné, jamais composé : ne jamais le retaper en Archivo. »**
  → l'approche se change en déplaçant des **chemins**, jamais par un
  `letter-spacing`. Le reparamétrage du § 2.3 est la bonne forme.
- **« Verrouillage — Marque + mot : 330 × 90. Marque + mot + signature :
  330 × 90. Signature en mono 8,5, interlettrage 2,6. »**
  → le `viewBox` de 330 est prescrit pour **les deux** verrouillages. Le blanc à
  droite du mot dans la navigation (qui n'affiche pas la signature) est donc
  voulu, pas un défaut. ⚠ **Resserrer le mot sans rien décider du `viewBox`
  augmente ce blanc** — et comme les deux appels emploient `w-auto`, la boîte du
  logo restera large pendant que son encre rétrécira. À mesurer au rendu.
- **Interdit 07 : « Le monogramme ne se déforme pas, ne change pas de
  proportions, ne reçoit ni ombre ni contour. »**
  → réduire le `viewBox` pour rattraper le blanc **changerait les proportions du
  verrouillage**. C'est la tension à arbitrer, pas à contourner.

**Deux amendements d'application sont donc à ouvrir**, dans la lignée d'A9
(grille de cartes), A10 (coupe des secteurs) et A11–A14 (motion) — tous arbitrés
au dépôt et absents du PDF :

| № | Objet | Charte 2.1 | Ce qui s'appliquerait |
|---|---|---|---|
| **A15** | approche du mot FT2E | écarts de 11,0 unités, translates 35 / 72 / 107 | écarts resserrés à `g`, translates dérivés |
| **A16** | texte de la signature | « BUREAU D'ÉTUDES TECHNIQUES », une ligne, mono 8,5 / 2,6 | libellé métier arrêté par FT2E, sur une ou deux lignes |

⚠ **Ils se consignent dans `.claude/rules/tailwind-design-tokens.md` (§ Les
amendements), qui fait foi sur le design — pas seulement dans `Logo.astro`.**
Un dessin modifié sans son amendement se relit plus tard comme une dérive, et se
« corrige » vers la charte.

## 4. La formule vit à SIX endroits — décider lesquels suivent

C'est le piège de portée de ce chantier. Changer la signature dessinée sans
décider du reste laisserait le site se décrire de deux façons.

**Couche SIGNATURE — ce qui identifie la marque :**

| Emplacement | Rôle | Suit ? |
|---|---|---|
| `Logo.astro` ligne 94 — le `<text>` dessiné | la signature, au pied de page | **oui, c'est l'objet** |
| `Logo.astro` ligne 51 — `aria-label` « FT2E — bureau d'études techniques » | ce qu'un lecteur d'écran **prononce** sur le logo du pied | à trancher — il devrait dire ce que la signature montre |
| `constants.ts` ligne 2 — `SITE_TAGLINE` « Bureau d'études techniques, La Rochelle » | accroche mono en en-tête, **au-dessus de 1 280 px** | à trancher |

**Couche DESCRIPTION — ce qui explique le métier aux moteurs et aux visiteurs :**

| Emplacement | Rôle | Suit ? |
|---|---|---|
| `constants.ts` ligne 21 — `description` du JSON-LD `ProfessionalService` | référencement | **non, sauf décision contraire** |
| `constants.ts` ligne 19 — `alternateName` « FT2E Bureau d'études » | référencement | **non** |
| `Footer.astro` ligne 37 + les `description` de pages | prose et meta | **non** |

**Le principe qui départage** : une signature *nomme*, une description
*explique*. « Bureau d'études techniques » est la requête que les moteurs
indexent et que `.claude/rules/seo-geo.md` fait vivre dans le `LocalBusiness` —
la retirer de la couche description coûterait du référencement sans rien gagner
au dessin. Les deux couches peuvent donc diverger, à condition que ce soit
**décidé** et écrit.

✅ **`public/favicon.svg` n'est PAS concerné** : c'est la forme « marque seule »
(90 × 90), sans lettres ni signature. Vérifié, aucun autre dessin du monogramme
n'existe au dépôt.

## 5. Les arbitrages à soumettre en ouverture de session

| № | Question | Ce que la mesure apporte |
|---|---|---|
| **A** | Quelle valeur pour `g` ? | 8 ou 9 pour un resserrement « léger » (− 7 % ou − 5 % de largeur). À montrer sur épreuve aux trois tailles. |
| **B** | Quel libellé ? | Sur une ligne, seule « BUREAU FLUIDES » tient sous le mot. Les deux autres pistes dépassent, dont une plus que l'actuelle. |
| **C** | Une ligne ou deux ? | Deux lignes font tenir **toutes** les pistes. Contrainte à vérifier : la signature est à `y=74` dans une boîte de 90 — la seconde ligne doit trouver sa place sans toucher le bord ni le cadre. |
| **D** | Graphie exacte ? | « BUREU » → BUREAU et « TERMIQUES » → THERMIQUES (coquilles). Puis : « & » ou « ET » ; « THERMIQUE » au singulier (une discipline) ou au pluriel ; « BET » est la graphie que `.claude/rules/french-editorial.md` valide déjà. |
| **E** | Portée ? | Les trois emplacements de la couche signature suivent-ils (§ 4) ? |

⚠⚠ **Un point de fond à porter à FT2E, et il n'est pas graphique.**
« BUREAU FLUIDES » est la seule piste qui résout la longueur sur une ligne, mais
elle **rétrécit le périmètre annoncé**. Le site que FT2E vient de valider
présente quatre expertises et sept secteurs, dont **Électricité**,
**Coordination SSI** et **Études d'exécution / BIM** ; le pied de page dit
« Fluides, thermique, électricité, SSI, BIM » et les 47 fiches le démontrent —
IRVE, courants faibles, SSI de catégorie A, maquette Revit. Une signature qui
n'annonce que les fluides contredirait la moitié du site.

C'est un **arbitrage de positionnement**, à rendre par FT2E en connaissance de
cet écart — pas une question de composition. Trois façons de le tenir :
signature plus large (« BET FLUIDES & THERMIQUE » sur deux lignes tient), ou
assumer un raccourci de marque, ou porter le périmètre complet dans la couche
description pendant que la signature reste courte.

## 6. La recette attendue

| Contrôle | Attendu |
|---|---|
| `npm run typecheck` | 0 erreur, 107 hints (ligne de base) |
| `npm run build` | 76 pages, inchangé |
| Rendu du logo à 44 px (navigation), 60 px (pied), 30 px (cadre) | épreuve à l'écran, les trois tailles |
| Rendu à 1440 et 390 px | 0 débordement horizontal, en-tête et pied |
| Largeur de la boîte du logo vs largeur d'encre | mesurée après resserrement — le blanc à droite ne doit pas décaler la navigation |
| Lighthouse a11y sur l'accueil et une page interne | inchangé (exception D1 documentée) |
| Zone de protection de 24 unités | vérifiée au dessin après reparamétrage |
| `.claude/rules/tailwind-design-tokens.md` | A15 et A16 consignés **dans le même commit** que `Logo.astro` |

⚠ **Un build vert ne prouve pas que le logo est juste** (règle 11) : une
approche et une signature se jugent **à l'œil, sur épreuve**, aux tailles
d'emploi réelles. Prévoir des captures avant/après, côte à côte.

## 7. La trajectoire de production, telle qu'elle est arrêtée

L'utilisateur a fixé l'ordre le 2026-09-06. Il n'est **pas** négociable par
commodité d'exécution :

1. **Le monogramme** — ce chantier, session N28.
2. **La finalisation** — session suivante.
3. **La relecture complète des contenus par le client**, qui remonte ses
   corrections. *Rien ne se fige avant ce retour.*
4. **Les corrections**, puis un **audit complet et approfondi**.
5. **La bascule et la mise en production sur le serveur OVH.**

### 7.1 ⚠ La production sur OVH change deux choses connues

**a) Le proxy OAuth de Decap est une fonction Vercel.** `api/auth.js` et
`api/callback.js` sont des handlers Node au format Vercel (`export default
function handler(req, res)`), lus par `process.env`. **Un hébergement mutualisé
OVH ne les exécutera pas tels quels.** `docs/09-deploiement-ovh.md` retient
l'offre Webhosting Pro (PHP 8.x, « Node.js disponible » — affirmation du PDF,
jamais vérifiée). Deux chemins connus, l'un et l'autre à arbitrer :

- réécrire le proxy en **PHP**, qu'OVH expose sûrement ;
- **garder le proxy sur Vercel** pendant que le site est servi par OVH — Decap
  admet un `base_url` distinct pour l'authentification.

**Conséquence de calendrier : réparer l'OAuth aujourd'hui sur Vercel ne survit
pas nécessairement à la bascule.** Le blocage de rang A et la migration OVH sont
désormais **couplés**, et le § 0 de `docs/22-prise-en-main-decap.md` devra être
rejoué sur le domaine final de toute façon (la callback porte l'adresse du site).

**b) Le déblocage de l'indexation se fait à la bascule, pas avant.** Les trois
verrous (`public/robots.txt`, `vercel.json`, `noindex` par défaut de
`BaseLayout`) sont dimensionnés pour Vercel ; sur OVH, le `X-Robots-Tag` passe
par le `.htaccess` que `docs/09` prévoit déjà. Procédure :
`docs/19-migration-production.md`, **à réconcilier avec `docs/09`**.

### 7.2 Ce que la trajectoire déplace

Le prompt Decap / Phase 5 rédigé en annexe B du plan des articles **n'est plus
celui de la N28**. Il reste valable comme matière pour l'étape 2 (finalisation),
et son inventaire des rangs A à D fait toujours foi.

## Annexe A — prompt de lancement de la session N28

> Autoportant : collé dans une session neuve, il ne suppose aucun contexte des
> précédentes. Reproduit intégralement dans le message final de la N27,
> conformément à la règle de continuité de `CLAUDE.md`.

```
Session N28 - FT2E v3. CHANTIER DU MONOGRAMME, sur DEMANDE CLIENT.
Cette session ne produit AUCUNE fiche et AUCUN article : les deux chantiers
sont clos (47 fiches, 6 articles). Elle traite le logo, et elle OUVRE PAR
CINQ ARBITRAGES a soumettre avant d'ecrire une ligne de code.

Contexte. FT2E v3 est le site institutionnel du bureau d'etudes FT2E (La
Rochelle), Astro 6 statique, deploye en demonstration client sur
https://ft2e-v3.vercel.app (indexation verrouillee par triple securite -
robots.txt, meta noindex, header X-Robots-Tag : NE PAS Y TOUCHER sans
validation FT2E, procedure dans docs/19-migration-production.md).

LA DEMANDE CLIENT, telle qu'elle a ete transmise le 2026-09-06
  1. Resserrer LEGEREMENT l'ecartement entre les caracteres du mot F T 2 E,
     juge un peu trop espace.
  2. Changer la SIGNATURE sous le mot, jugee trop generique et trop longue
     (" ca depasse en longueur le logo au-dessus "). A la place de
     " BUREAU D'ETUDES TECHNIQUES ", trois pistes a tester, sur une ou deux
     lignes : " BUREAU FLUIDES ", " BUREAU FLUIDES ET THERMIQUE ",
     " BET FLUIDES & THERMIQUES ".
  /!\ Les graphies transmises portaient deux coquilles - " BUREU " et
  " TERMIQUES " - rectifiees ici. Le libelle exact reste a arreter.

LIRE D'ABORD, dans cet ordre
1. docs/superpowers/plans/2026-09-06-chantier-monogramme.md EN ENTIER - le
   plan de ce chantier : l'etat mesure, la tension avec la charte, les cinq
   arbitrages, la recette et la trajectoire de production.
2. La section 07 de la charte : branding-v3-bis/charte21.txt, chercher
   " 07 Le /monogramme ". Elle prescrit le dessin au detail.
3. .claude/rules/tailwind-design-tokens.md § Les amendements - c'est la que
   A15 et A16 devront etre consignes, et c'est ce fichier qui fait foi.
4. CLAUDE.md et les six fichiers de .claude/rules/.

/!\/!\ CE QUI EST DEJA MESURE - NE PAS LE REMESURER, S'EN SERVIR
Mesures prises en N27 au navigateur, dans la police reellement chargee
(IBM Plex Mono par fontsource), en unites du viewBox de 330 :
  - LE DEPOT NE DEVIE PAS DE LA CHARTE, IL LA TRANSCRIT. Logo.astro est la
    copie exacte du dessin de reference de
    branding-v3-bis/FT2E-charte-graphique-rev2.1-source.html : memes chemins,
    memes translate(5,5) / (104,16) / 35 / 72 / 107, memes 8,5 et 2,6, meme
    texte de signature. Les deux demandes MODIFIENT LA CHARTE, elles ne
    corrigent pas une derive.
  - Largeur d'encre du mot FT2E : 131,0 unites.
  - Signature actuelle " BUREAU D'ETUDES TECHNIQUES " : 200,2 unites, soit
    x1,53 le mot. LE CLIENT A RAISON, ET C'EST CHIFFRE.
  - Des trois pistes, UNE SEULE tient sur une ligne : " BUREAU FLUIDES "
    (107,8 - x0,82). " BUREAU FLUIDES ET THERMIQUE " fait 207,9 - PLUS LONGUE
    QUE L'ACTUELLE, elle aggrave le defaut qu'elle corrige.
    " BET FLUIDES & THERMIQUES " fait 184,8 - x1,41, mieux mais depasse encore.
  - SUR DEUX LIGNES, TOUTES LES PISTES TIENNENT (84,7 a 107,8 par ligne).
  - Les trois ecarts optiques du mot valent 11,0 unites, EXACTEMENT, et les
    ecarts nominaux aussi : le " 2 " est trace au trait quand F, T et E sont
    pleins, mais le dessin compense deja. Soupcon leve par la mesure.
  - Reparametrage a une seule variable g (l'ecart) :
        T -> translate(24 + g, 0)
        2 -> translate(50 + 2g, 0)
        E -> translate(74 + 3g, 0)
        largeur du mot = 98 + 3g       (g = 11 redonne 35/72/107 et 131,0)
    g = 9 -> 33/68/101, mot a 125,0 (-4,6 %)
    g = 8 -> 32/66/98,  mot a 122,0 (-6,9 %)
    g = 7 -> 31/64/95,  mot a 119,0 (-9,2 %)

/!\/!\ LES CINQ ARBITRAGES A SOUMETTRE EN OUVERTURE
  A. Quelle valeur pour g ? (8 ou 9 pour un resserrement " leger ")
  B. Quel libelle ? (la mesure ci-dessus est l'entree de la decision)
  C. Une ligne ou deux ? (deux lignes ouvrent tout le choix ; contrainte a
     verifier : la signature est a y=74 dans une boite de 90)
  D. Graphie exacte ? " & " ou " ET " ; " THERMIQUE " au singulier (c'est une
     discipline) ou au pluriel ; " BET " est deja la graphie que
     .claude/rules/french-editorial.md valide.
  E. Portee ? Voir le point suivant.

/!\/!\ UN POINT DE FOND A PORTER A FT2E, ET IL N'EST PAS GRAPHIQUE
" BUREAU FLUIDES " est la seule piste qui resout la longueur sur une ligne,
mais elle RETRECIT LE PERIMETRE ANNONCE. Le site presente quatre expertises et
sept secteurs, dont Electricite, Coordination SSI et Etudes d'execution / BIM ;
le pied de page dit " Fluides, thermique, electricite, SSI, BIM " et les 47
fiches le demontrent (IRVE, courants faibles, SSI de categorie A, maquette
Revit). Une signature qui n'annonce que les fluides contredirait la moitie du
site. C'est un ARBITRAGE DE POSITIONNEMENT, a rendre par FT2E en connaissance
de cet ecart - pas une question de composition.

/!\ LA FORMULE VIT A SIX ENDROITS : DECIDER LESQUELS SUIVENT (arbitrage E)
Couche SIGNATURE (ce qui NOMME la marque) :
  - Logo.astro l.94  : le <text> dessine, au pied de page -> oui, c'est l'objet
  - Logo.astro l.51  : aria-label " FT2E - bureau d'etudes techniques ", ce
    qu'un lecteur d'ecran PRONONCE sur le logo du pied -> a trancher
  - constants.ts l.2 : SITE_TAGLINE, accroche mono en en-tete au-dessus de
    1 280 px -> a trancher
Couche DESCRIPTION (ce qui EXPLIQUE le metier) :
  - constants.ts l.19 et l.21 : alternateName et description du JSON-LD
  - Footer.astro l.37 et les description de pages
  -> NON par defaut : une signature nomme, une description explique.
     " Bureau d'etudes techniques " est la requete que les moteurs indexent et
     que .claude/rules/seo-geo.md fait vivre dans le LocalBusiness. Les deux
     couches PEUVENT diverger, a condition que ce soit DECIDE et ecrit.
/!\ public/favicon.svg n'est PAS concerne : forme " marque seule " 90 x 90,
sans lettres ni signature. Verifie, aucun autre dessin du monogramme au depot.

/!\/!\ C'EST UN AMENDEMENT DE CHARTE, PAS UNE RETOUCHE
Le § 07 de la charte 2.1 porte trois phrases qui commandent le travail :
  - " Le mot est dessine, jamais compose : ne jamais le retaper en Archivo. "
    -> l'approche se change en deplacant des CHEMINS, jamais par un
       letter-spacing. Le reparametrage ci-dessus est la bonne forme.
  - " Verrouillage - Marque + mot : 330 x 90. Marque + mot + signature :
    330 x 90. " -> le viewBox de 330 est prescrit pour LES DEUX. Le blanc a
    droite du mot en navigation est VOULU. /!\ Resserrer le mot AUGMENTE ce
    blanc, et les deux appels emploient w-auto : la boite restera large pendant
    que l'encre retrecira. A MESURER AU RENDU (la navigation peut se decaler).
  - Interdit 07 : " Le monogramme ne se deforme pas, NE CHANGE PAS DE
    PROPORTIONS. " -> reduire le viewBox pour rattraper le blanc changerait les
    proportions du verrouillage. C'est la tension a ARBITRER, pas a contourner.
Deux amendements d'application sont donc a ouvrir, dans la lignee d'A9, A10 et
A11-A14 (tous arbitres au depot, absents du PDF) :
  A15 - approche du mot FT2E
  A16 - texte et composition de la signature
/!\ Ils se consignent dans .claude/rules/tailwind-design-tokens.md
(§ Les amendements), qui FAIT FOI sur le design, DANS LE MEME COMMIT que
Logo.astro. Un dessin modifie sans son amendement se relit plus tard comme une
derive, et se " corrige " vers la charte.

RECETTE ATTENDUE
  npm run typecheck                     0 erreur, 107 hints (ligne de base)
  npm run build                         76 pages, inchange
  epreuve du logo aux TROIS tailles     44 px navigation, 60 px pied, 30 px cadre
  rendu a 1440 et 390                   0 debordement, en-tete ET pied
  largeur de boite vs largeur d'encre   mesuree apres resserrement
  zone de protection de 24 unites       verifiee au dessin
  Lighthouse a11y                       inchange (exception D1 documentee)
  A15 et A16 consignes                  meme commit que Logo.astro
/!\ UN BUILD VERT NE PROUVE PAS QUE LE LOGO EST JUSTE (regle 11). Une approche
et une signature se jugent A L'OEIL, SUR EPREUVE, aux tailles d'emploi.
Prevoir des captures AVANT/APRES cote a cote.

LA TRAJECTOIRE DE PRODUCTION, ARRETEE PAR L'UTILISATEUR LE 2026-09-06
  1. le monogramme (cette session)
  2. la finalisation
  3. la RELECTURE COMPLETE DES CONTENUS PAR LE CLIENT, qui remonte ses
     corrections - rien ne se fige avant ce retour
  4. les corrections, puis un AUDIT COMPLET ET APPROFONDI
  5. la bascule et la MISE EN PRODUCTION SUR LE SERVEUR OVH
/!\ NE PAS TRIER LES CHANTIERS PAR " EXECUTABLE SANS ATTENDRE PERSONNE " - ce
critere favorise le polissage et ecarte la production. Ici l'ordre est DONNE
par l'utilisateur : le suivre.

/!\/!\ LA PRODUCTION SUR OVH CHANGE DEUX CHOSES CONNUES - a savoir des
maintenant, meme si l'etape est lointaine.
  a) LE PROXY OAUTH DE DECAP EST UNE FONCTION VERCEL. api/auth.js et
     api/callback.js sont des handlers Node au format Vercel
     (export default function handler(req, res), process.env). Un mutualise OVH
     NE LES EXECUTERA PAS tels quels. docs/09-deploiement-ovh.md retient l'offre
     Webhosting Pro (PHP 8.x, " Node.js disponible " - affirmation du PDF jamais
     verifiee). Deux chemins, a arbitrer : reecrire le proxy en PHP, ou GARDER
     le proxy sur Vercel pendant que le site est servi par OVH (Decap admet un
     base_url distinct). CONSEQUENCE : reparer l'OAuth aujourd'hui sur Vercel ne
     survit pas necessairement a la bascule - le rang A et la migration OVH sont
     desormais COUPLES.
  b) LE DEBLOCAGE DE L'INDEXATION SE FAIT A LA BASCULE. Les trois verrous sont
     dimensionnes pour Vercel ; sur OVH le X-Robots-Tag passe par le .htaccess
     que docs/09 prevoit deja. docs/19-migration-production.md est A RECONCILIER
     avec docs/09.

CE QUI RESTE OUVERT PAR AILLEURS (docs/23-etat-de-l-art.md § 4 fait foi)
  RANG A - hors depot : Decap OAuth casse en production (HTTP 500). Trois
    gestes, docs/22-prise-en-main-decap.md § 0. Voir le couplage OVH ci-dessus.
  RANG B - suspendu a FT2E : reception de la creche de l'Oranger (NE JAMAIS
    FABRIQUER UN MILLESIME), les 25 visuels dans l'historique, planche-chiffree
    jamais exerce, les validations du bloc secteurs (dont les artefacts
    d'agrandissement generatif releves sur les cliches retenus), les questions B
    et E des 24 fiches de collecte, et les DOUZE CV NOMINATIFS de
    livrables/cv-ft2e/ - donnees personnelles dans l'historique d'un depot
    partage, alors que le motif /cv/ du .gitignore declare qu'un CV ne se
    commite jamais. Retrait = reecriture d'historique : arbitrage, pas
    correction.
  RANG C - les huit photographies d'equipe generees par IA.
  RANG D - polissage : texte dessine des planches (64 ecarts) et champs
    editoriaux (2 160), passage NVDA jamais fait par un humain, option 0 du
    motion (TraceFlux debranche), LCP mobile au seuil.
  UNE AFFIRMATION NON ETAYEE RESTE EN LIGNE : expertises/electricite.md, " la
    GTB permet de reduire les consommations de 15 a 25 % ". Aucune piece FT2E.
    Le jumeau - le " COP 4 a 5 " de la FAQ CVC - a ete retire le 2026-09-04
    (commit 95d5218). /!\ Avant de proposer " remplacer par une valeur du
    corpus " : VERIFIER QUE LA VALEUR DIT LA MEME CHOSE. C'est ce qui a fait
    ecarter cette issue pour le COP.
  COCON SEMANTIQUE : 8 piliers sur 11, PLAFOND STRUCTUREL et definitif. Trois
    pages sans satellite, aucune aux 3-5 que seo-geo.md demande. Six articles ne
    couvrent pas onze piliers. Perimetre contractuel a six (docs/17 p. 23), au-
    dela un devis. A DIRE A FT2E.

/!\/!\ L'ECHEANCE DATEE, ET LA SEULE MANIERE D'Y REPONDRE.
src/lib/projets.ts porte MILLESIME_LIVRAISON_ANNONCE = 2026 et un garde-fou qui
FAIT ECHOUER LE BUILD AU 1er JANVIER 2027, sur les quinze affaires dont la
reception n'est pas prononcee (mesurer :
grep -L annee_livraison src/content/projets/*.md | wc -l).
/!\ NE JAMAIS pousser la constante a 2027 : cela desarmerait le garde-fou pour
s'epargner l'echec qu'on lui demande de produire. La reponse est d'aller relever
les receptions - rang B, donc chez FT2E. L'echeance tombe AVANT la mise en
production si le calendrier glisse : a signaler a l'etape 4 (audit).

PIEGES D'OUTILLAGE DE CETTE MACHINE - ils ne se redecouvrent pas
- /!\ QUAND UN CONTROLE CRIE, SUSPECTER LE CONTROLE AVANT LE DEPOT. Sept
  fausses alertes en quatre sessions, toutes venant de l'instrument. Parade :
  des asserts qui font ECHOUER l'instrument quand il ne sait pas lire (aucun
  antislash dans un chemin construit, un compte d'entrees exact, et une SONDE
  TEMOIN qui doit trouver un hit connu).
- /!\ POUR MESURER DU TEXTE, LA POLICE DOIT ETRE CHARGEE. Une mesure prise
  avant document.fonts.ready porte sur une police de repli et ment. Poser
  l'assert document.fonts.check("8.5px 'IBM Plex Mono'").
- /!\ UNE CLASSE DE CARACTERES SUR UNE LETTRE ACCENTUEE NE MORD PAS.
  grep -E "g[ee]othermi" (e accent aigu dans la classe) rend ZERO sur un corpus
  qui porte " geothermique " : la classe compare des OCTETS. Ancrer sur le mot
  litteral. Meme cause pour [ee]xecution.
- /!\ UN COMPTAGE PAR UNION DE TERMES N'EST PAS UN COMPTAGE PAR SUJET.
- /!\ Les insecables ne s'ecrivent JAMAIS en litteral dans une source : les
  outils d'ecriture les normalisent de facon non deterministe. Ecrire SANS, puis
  lancer  python scripts/injection-typographique.py <fichier.md>
  ( " droites restantes 0 " attendu ). Corollaire : un Edit dont le old_string
  porte une espace ordinaire NE TROUVERA PAS une ligne qui porte U+00A0 - passer
  par python, et ancrer sur la LIGNE, pas sur une chaine reconstruite.
- /!\ Les gros heredocs bash echouent, et un heredoc MANGE LES ANTISLASH d'un
  script Python (un '\n' devenu une chaine non terminee, deux fois : N26 et
  N27). Ecrire les scripts par l'outil d'ecriture, dans le scratchpad.
- /!\ astro.config.mjs porte trailingSlash: 'always' : une sonde qui appelle
  /expertises/cvc SANS barre finale recoit 404 sur astro preview, alors que
  Vercel sert les deux en 200. Toujours poser la barre finale.
- /!\ Un script du scratchpad ne resout pas node_modules par le nom : importer
  puppeteer-core par CHEMIN ABSOLU, et c'est
  node_modules/puppeteer-core/lib/puppeteer/puppeteer-core.js (PAS de esm/).
- /!\ npm run preview ne se lance PAS avec un & dans un appel Bash au premier
  plan : l'appel rend la main et le serveur meurt. Le lancer en tache de fond,
  puis ATTENDRE par une boucle sur curl, jamais par un delai. Et le FERMER en
  fin de session (taskkill sur le PID du port 4321) : un serveur orphelin fausse
  la session suivante.
- /!\ astro preview rend 304 sur une page deja vue : setCacheEnabled(false) et
  tolerer 304.
- `npm run captures` EXISTE pour un jeu multi-paliers : NE PAS LE REBATIR. Sa
  table ROUTES est CURATEE (14 gabarits) et --route filtre sur le nom de DOSSIER
  de cette table.
- /!\ LES BACKTICKS D'UN MESSAGE DE COMMIT SONT EXECUTES PAR BASH quand on passe
  par -m " ... ". Passer par `git commit -F <fichier>`, immunise.
- La CLI vercel repond " Not authorized " : c'est le PUSH qui deploie. Verifier
  par un MARQUEUR DU BUILD, jamais par un delai. Depot PARTAGE : rejouer
  git status au moment de committer.
- npm run preview NE MESURE PAS LA PERFORMANCE (aucune compression, 0,8 s de
  biais). La performance se mesure sur le deploiement.
- PYTHONIOENCODING=utf-8 devant toute commande python qui imprime des accents.

Portee de commit : feat(design-system) pour le monogramme et ses amendements,
docs(...) pour le point de suivi. Le changement de Logo.astro et la consignation
d'A15/A16 dans .claude/rules/tailwind-design-tokens.md vont dans LE MEME COMMIT.

Terminer par le prompt de lancement de la session suivante, en annexe de ce plan
et reproduit integralement dans le message final - la regle de continuite est
dans CLAUDE.md parce qu'elle a ete manquee deux fois.
```

## 8. Bilan de la session N28 — le chantier est CLOS, avec deux réserves

**Arbitrages rendus par FT2E le 2026-09-11** (les cinq du § 5, dont trois
répondus et deux laissés ouverts) :

| № | Question | Réponse |
|---|---|---|
| **A** | Valeur de `g` | **8** — `translate` 32 / 66 / 98, mot à 122,0 unités (− 6,9 %) |
| **B** | Libellé | **BUREAU FLUIDES / ET THERMIQUE** |
| **C** | Une ligne ou deux | **deux**, et **justifiées** sur l'empan du mot |
| **D** | Graphie | « BUREAU », pas « BET » ; « THERMIQUE » au singulier ; pas d'esperluette |
| **E** | Portée | ⚠ **non rendu** — voir § 8.3 |

Commit : `feat(design-system)` — `Logo.astro`, `.claude/rules/tailwind-design-tokens.md`
(A15 et A16) et `CLAUDE.md` dans le même commit, comme la règle l'exige.

### 8.1 Ce que la mesure a corrigé en cours de route

**La justification a été demandée après coup, et elle a changé la nature du
travail.** Le § 2.2 classait des candidats par longueur ; justifier impose de
poser un bord sur un autre, ce qui demande une tout autre précision.

⚠ **Deux relevés antérieurs se sont révélés impropres à cet usage**, et le plan
les portait tels quels :

1. **`getBBox()` sur un `<text>` ne mesure pas l'encre.** Il rend la boîte des
   **approches**, espace traînant après la dernière lettre compris — vérifié par
   sonde témoin : un signe unique y grandit exactement d'autant que
   l'interlettrage. **Toutes les largeurs publiées avant le 2026-09-11 sont donc
   des largeurs d'approche** : 200,2 pour la signature de la charte, 107,8 pour
   « BUREAU FLUIDES », etc. Elles classent correctement les candidats — c'est
   pour cela que le § 2.2 reste valable — mais une signature calée dessus
   finirait **4 à 6 unités trop courte**, sans que rien ne le signale. Le contour
   réel passe par `actualBoundingBoxLeft/Right` du Canvas.
2. **Justifier en chasse fixe impose un interlettrage PAR LIGNE.** `encre(s) =
   encre(0) + (n − 1)·s`, donc `s = (W − encre(0)) / (n − 1)` : deux lignes de
   longueurs différentes ne peuvent pas partager leur interlettrage. La charte
   n'en prescrivait qu'un, 2,6 — c'est ce qui fait de A16 un amendement et non un
   réglage. Mesurés : **3,823** (BUREAU FLUIDES, 14 signes) et **5,536**
   (ET THERMIQUE, 12 signes).

**Un résultat contre-intuitif, à connaître avant de proposer un autre libellé :
c'est la ligne la plus COURTE qui s'ouvre le plus.** « BET FLUIDES » (11 signes)
aurait demandé **6,500**, soit 0,77 em. Le couple BET était plus *homogène*
(rapport × 1,17 entre ses deux lignes, contre × 1,45 pour BUREAU) mais beaucoup
plus lâche. Il n'y a pas de réglage qui donne les deux.

**Un point de géométrie qui commande A15**, relevé avant tout calcul : les trois
écarts du mot sont égaux à l'encre *bien que* le « 2 » soit tracé au trait quand
F, T et E sont pleins. Cela ne tient qu'à une chose — **le groupe du 2 ne déclare
aucun `stroke-linecap`**, donc `butt` par défaut. Avec `round`, les écarts
autour du 2 vaudraient 7,5 au lieu de 11, et `g = 8` les refermerait à 4,5.

### 8.2 Recette exécutée

| Contrôle | Attendu | Mesuré |
|---|---|---|
| `npm run typecheck` | 0 erreur, 107 hints | **0 / 107** ✅ |
| `npm run build` | 76 pages | **76** ✅ |
| Largeur du mot au rendu | 122,0 unités de `viewBox` | **122,0** aux deux largeurs ✅ |
| Débordement horizontal, 1440 et 390 | nul | **0** ✅ |
| Blanc à droite du verrouillage | à mesurer | **+ 4,4 px** en navigation (161,3 de boîte, 110,5 d'encre), **+ 6,0 px** au pied (220 / 150,7) — aucun décalage de mise en page ✅ |
| Formes servies | 44 / 60 / 30 px | **44 et 60 à 1440 ; 30 (cadre) et 60 à 390** ✅ |
| Zone de protection de 24 unités | vérifiée | ✅ — l'encre ayant rétréci, le dégagement **augmente** ; aucune reprise nécessaire |
| Lighthouse a11y | inchangé (exception D1) | **96**, violation unique `text-clair` `aria-hidden` à 1,54 sur calcaire ✅ |

### 8.3 ⚠ Ce qui reste ouvert — deux réserves à porter à FT2E

**a) L'arbitrage E n'a pas été rendu, et il se voit à l'écran.** La formule vit à
six endroits ; seul le `<text>` dessiné a changé. Conséquences visibles
aujourd'hui :

- **l'`aria-label` du monogramme dit encore « FT2E — bureau d'études
  techniques ».** Le SVG portant `role="img"`, un lecteur d'écran n'énonce **que**
  cet attribut et **jamais** le texte dessiné : un visiteur aveugle entend autre
  chose que ce qu'un visiteur voyant lit. Les deux nomment la même société — ce
  n'est pas un défaut bloquant, c'est un arbitrage non rendu ;
- **`SITE_TAGLINE` affiche « BUREAU D'ÉTUDES TECHNIQUES, LA ROCHELLE »** dans la
  barre d'en-tête au-dessus de 1 280 px, **sur la même ligne** que le monogramme
  resserré. Les deux formules cohabitent.

La couche **description** (JSON-LD, `alternateName`, pied de page, `description`
de pages) n'a pas bougé, et c'est une décision écrite sous A16 : *une signature
nomme, une description explique*. « Bureau d'études techniques » reste la requête
que les moteurs indexent.

**b) Le périmètre annoncé rétrécit — le point du § 5 reste entier.** Le site
présente quatre expertises et sept secteurs, dont Électricité, Coordination SSI
et Études d'exécution / BIM ; quarante-sept fiches le démontrent. La signature
n'annonce plus que les fluides et la thermique. **C'est aujourd'hui la couche
description qui porte le périmètre complet.** Si FT2E veut un jour aligner les
deux couches, c'est la description qui décidera, pas le dessin.

**c) Une divergence de source, tranchée par le texte.** La réponse de FT2E nomme
« Bureau, deux lignes » avec ses mesures (107,8 · 92,4), tandis que l'image
annotée qui l'accompagnait montrait « **BET** FLUIDES / ET THERMIQUE ». Le texte
étant explicite et chiffré, et l'annotation portant sur la *composition*
(« texte justifié ou centré sous logo »), c'est « BUREAU » qui a été posé.
**À confirmer en ouverture de N29** — c'est un mot à changer, pas un chantier.

### 8.4 Épreuves

Page d'épreuves comparées, composée dans les jetons FT2E, avec curseur d'écart et
mise en situation : publiée en artefact le 2026-09-11 (version 2 = état posé).
Elle porte les quatre compositions en présence, l'arithmétique de la
justification et les deux réserves ci-dessus.

## Annexe B — prompt de lancement de la session N29

> Autoportant : collé dans une session neuve, il ne suppose aucun contexte des
> précédentes. Reproduit intégralement dans le message final de la N28,
> conformément à la règle de continuité de `CLAUDE.md`.

```
Session N29 - FT2E v3. ETAPE 2 DE LA TRAJECTOIRE : LA FINALISATION.
Cette session ne produit NI fiche, NI article, NI refonte de logo : les trois
chantiers sont clos (47 fiches, 6 articles, monogramme amende A15/A16 le
2026-09-11). Elle PREPARE LA RELECTURE CLIENT, qui est l'etape 3.

Contexte. FT2E v3 est le site institutionnel du bureau d'etudes FT2E (La
Rochelle), Astro 6 statique, deploye en demonstration client sur
https://ft2e-v3.vercel.app (indexation verrouillee par TRIPLE SECURITE -
robots.txt, meta noindex, header X-Robots-Tag : NE PAS Y TOUCHER sans
validation FT2E, procedure dans docs/19-migration-production.md).

LA TRAJECTOIRE, ARRETEE PAR L'UTILISATEUR LE 2026-09-06 - l'ordre est DONNE,
il ne se reordonne pas par commodite d'execution :
  1. le monogramme                                      FAIT (N28)
  2. LA FINALISATION                                    <- cette session
  3. la RELECTURE COMPLETE DES CONTENUS PAR LE CLIENT, qui remonte ses
     corrections - RIEN NE SE FIGE AVANT CE RETOUR
  4. les corrections, puis un AUDIT COMPLET ET APPROFONDI
  5. la bascule et la MISE EN PRODUCTION SUR LE SERVEUR OVH
/!\ NE PAS TRIER LES CHANTIERS PAR " EXECUTABLE SANS ATTENDRE PERSONNE " : ce
critere favorise le polissage et ecarte la production.
/!\ COROLLAIRE DIRECT POUR CETTE SESSION : l'etape 3 est une RELECTURE. Tout
ce qui serait re-ecrit maintenant sera peut-etre corrige par le client dans
quelques jours. La finalisation porte donc sur ce qui NE DEPEND PAS du texte :
les reserves ouvertes, la coherence technique, la preparation du dossier de
relecture. PAS sur une passe de reecriture editoriale.

/!\/!\ TROIS RESERVES OUVERTES PAR LA N28 - A PORTER A FT2E EN OUVERTURE
  a) LE LIBELLE DE LA SIGNATURE EST A CONFIRMER. La reponse de FT2E nommait
     " Bureau, deux lignes " avec ses mesures (107,8 . 92,4), mais l'IMAGE
     ANNOTEE qui l'accompagnait montrait " BET FLUIDES / ET THERMIQUE ". Le
     texte etant explicite et chiffre, et l'annotation portant sur la
     composition (" texte justifie ou centre sous logo "), c'est " BUREAU
     FLUIDES / ET THERMIQUE " qui a ete pose. C'EST UN MOT A CHANGER, PAS UN
     CHANTIER - mais il faut le demander.
     /!\ SI LE LIBELLE CHANGE, LES INTERLETTRAGES SE RECALCULENT : en chasse
     fixe, s = (W - encre(0)) / (n - 1) avec W = 122,0 (l'empan du mot a
     g = 8). Ne JAMAIS ajuster la valeur a l'oeil jusqu'a ce que " ca tombe
     bien ". Valeurs en place : 3,823 (BUREAU FLUIDES, 14 signes) et 5,536
     (ET THERMIQUE, 12 signes). Pour BET FLUIDES (11 signes) ce serait 6,500.
     /!\ ET L'ENCRE NE SE MESURE PAS AVEC getBBox() : cette boite inclut
     l'espace trainant apres la derniere lettre (sonde temoin : un signe
     unique y grandit d'autant que l'interlettrage). Passer par
     actualBoundingBoxLeft/Right du Canvas. Les largeurs publiees avant le
     2026-09-11 sont des largeurs d'APPROCHE.
  b) L'ARBITRAGE E N'A PAS ETE RENDU, et il se voit a l'ecran. Seul le <text>
     dessine a change. Restent en " bureau d'etudes techniques " :
       - Logo.astro, l'aria-label du monogramme. Le SVG porte role="img",
         donc un lecteur d'ecran n'enonce QUE cet attribut et JAMAIS le texte
         dessine : un visiteur aveugle entend autre chose que ce qu'un
         visiteur voyant lit. Pas bloquant, mais non arbitre.
       - constants.ts, SITE_TAGLINE : la barre d'en-tete au-dessus de 1 280 px
         affiche " BUREAU D'ETUDES TECHNIQUES, LA ROCHELLE " SUR LA MEME LIGNE
         que le monogramme resserre.
     La couche DESCRIPTION (JSON-LD, alternateName, pied, description de
     pages) n'a PAS bouge, et c'est une decision ecrite sous A16 : une
     signature NOMME, une description EXPLIQUE. " Bureau d'etudes techniques "
     est la requete que les moteurs indexent (.claude/rules/seo-geo.md).
  c) LE PERIMETRE ANNONCE RETRECIT. Le site presente quatre expertises et
     sept secteurs, dont Electricite, Coordination SSI et Etudes d'execution /
     BIM ; 47 fiches le demontrent (IRVE, courants faibles, SSI de categorie A,
     maquette Revit). La signature n'annonce plus que les fluides et la
     thermique. C'est la couche description qui porte le perimetre complet.
     ARBITRAGE DE POSITIONNEMENT, pas de composition.

LIRE D'ABORD, dans cet ordre
1. docs/23-etat-de-l-art.md § 4 - ce qui est clos, ce qui est ouvert, et qui
   peut le lever. FAIT FOI sur le reste a faire.
2. docs/superpowers/plans/2026-09-06-chantier-monogramme.md § 8 - le bilan de
   la N28, les trois reserves et la recette executee.
3. CLAUDE.md et les six fichiers de .claude/rules/.
4. .claude/rules/tailwind-design-tokens.md § Les amendements - A15 et A16 y
   sont consignes, et ce fichier FAIT FOI sur le design.

CE QUI RESTE OUVERT PAR AILLEURS (docs/23-etat-de-l-art.md § 4 fait foi)
  RANG A - hors depot : Decap OAuth casse en production (HTTP 500 sur
    /api/auth?provider=github). Trois gestes, docs/22-prise-en-main-decap.md
    § 0. /!\ COUPLE A LA MIGRATION OVH, voir ci-dessous.
  RANG B - suspendu a FT2E : reception de la creche de l'Oranger (NE JAMAIS
    FABRIQUER UN MILLESIME), les 25 visuels dans l'historique, planche-chiffree
    jamais exerce, les validations du bloc secteurs (dont les artefacts
    d'agrandissement generatif releves sur les cliches retenus), les questions
    B et E des 24 fiches de collecte, et les DOUZE CV NOMINATIFS de
    livrables/cv-ft2e/ - donnees personnelles dans l'historique d'un depot
    PARTAGE, alors que le motif /cv/ du .gitignore declare qu'un CV ne se
    commite jamais. Retrait = reecriture d'historique : ARBITRAGE, pas
    correction.
  RANG C - les huit photographies d'equipe generees par IA (marquees DEMO).
  RANG D - polissage : texte dessine des planches (64 ecarts typographiques)
    et champs editoriaux (2 160), passage NVDA jamais fait par un humain,
    option 0 du motion (TraceFlux debranche), LCP mobile au seuil.
  UNE AFFIRMATION NON ETAYEE RESTE EN LIGNE : expertises/electricite.md, " la
    GTB permet de reduire les consommations de 15 a 25 % ". Aucune piece FT2E.
    Le jumeau - le " COP 4 a 5 " de la FAQ CVC - a ete retire le 2026-09-04
    (commit 95d5218). /!\ Avant de proposer " remplacer par une valeur du
    corpus " : VERIFIER QUE LA VALEUR DIT LA MEME CHOSE. C'est ce qui a fait
    ecarter cette issue pour le COP.
  COCON SEMANTIQUE : 8 piliers sur 11, PLAFOND STRUCTUREL et definitif. Trois
    pages sans satellite, aucune aux 3-5 que seo-geo.md demande. Six articles
    ne couvrent pas onze piliers. Perimetre contractuel a six (docs/17 p. 23),
    au-dela un devis. A DIRE A FT2E.

/!\/!\ LA PRODUCTION SUR OVH CHANGE DEUX CHOSES CONNUES
  a) LE PROXY OAUTH DE DECAP EST UNE FONCTION VERCEL. api/auth.js et
     api/callback.js sont des handlers Node au format Vercel
     (export default function handler(req, res), process.env). Un mutualise OVH
     NE LES EXECUTERA PAS tels quels. docs/09-deploiement-ovh.md retient
     l'offre Webhosting Pro (PHP 8.x, " Node.js disponible " - affirmation du
     PDF JAMAIS VERIFIEE). Deux chemins a arbitrer : reecrire le proxy en PHP,
     ou GARDER le proxy sur Vercel pendant qu'OVH sert le site (Decap admet un
     base_url distinct). CONSEQUENCE : reparer l'OAuth aujourd'hui ne survit
     pas necessairement a la bascule - le rang A et la migration sont COUPLES.
  b) LE DEBLOCAGE DE L'INDEXATION SE FAIT A LA BASCULE. Les trois verrous sont
     dimensionnes pour Vercel ; sur OVH le X-Robots-Tag passe par le .htaccess
     que docs/09 prevoit deja. docs/19-migration-production.md est A
     RECONCILIER avec docs/09.

/!\/!\ L'ECHEANCE DATEE, ET LA SEULE MANIERE D'Y REPONDRE.
src/lib/projets.ts porte MILLESIME_LIVRAISON_ANNONCE = 2026 et un garde-fou qui
FAIT ECHOUER LE BUILD AU 1er JANVIER 2027, sur les affaires dont la reception
n'est pas prononcee (mesurer : grep -L annee_livraison src/content/projets/*.md
| wc -l).
/!\ NE JAMAIS pousser la constante a 2027 : cela desarmerait le garde-fou pour
s'epargner l'echec qu'on lui demande de produire. La reponse est d'aller relever
les receptions - rang B, donc chez FT2E. L'echeance tombe AVANT la mise en
production si le calendrier glisse : A SIGNALER A L'ETAPE 4 (audit).

PIEGES D'OUTILLAGE DE CETTE MACHINE - ils ne se redecouvrent pas
- /!\ QUAND UN CONTROLE CRIE, SUSPECTER LE CONTROLE AVANT LE DEPOT. Parade :
  des asserts qui font ECHOUER l'instrument quand il ne sait pas lire, et une
  SONDE TEMOIN qui doit trouver un hit connu. En N28, deux controles ont crie
  a tort (une ancre retapee, une assertion sur un texte que je n'avais pas
  ecrit) et UN a crie a raison (getBBox qui ne mesure pas l'encre).
- /!\ LES ANCRES DE REMPLACEMENT SE LISENT DU FICHIER, JAMAIS NE SE RETAPENT.
  Le depot MELE apostrophes droites (') et typographiques (') dans les MEMES
  fichiers, et porte des insecables U+00A0 a des endroits qu'on ne devine pas.
  Une ancre retapee ne mord pas, en silence. Lire, puis remplacer.
- /!\ POUR MESURER DU TEXTE, LA POLICE DOIT ETRE CHARGEE. Poser l'assert
  document.fonts.check("8.5px 'IBM Plex Mono'") apres document.fonts.ready.
- /!\ UNE CLASSE DE CARACTERES SUR UNE LETTRE ACCENTUEE NE MORD PAS.
  grep -E "g[ee]othermi" rend ZERO sur un corpus qui porte " geothermique " :
  la classe compare des OCTETS. Ancrer sur le mot litteral.
- /!\ UN COMPTAGE PAR UNION DE TERMES N'EST PAS UN COMPTAGE PAR SUJET.
- /!\ Les insecables ne s'ecrivent JAMAIS en litteral dans une source : les
  outils d'ecriture les normalisent de facon non deterministe. Ecrire SANS,
  puis lancer  python scripts/injection-typographique.py <fichier.md>
  (" droites restantes 0 " attendu).
- /!\ LES GROS HEREDOCS BASH ECHOUENT, ET UN HEREDOC MANGE LES ANTISLASH d'un
  script Python (trois fois : N26, N27 et ENCORE en N28, sur un antislash de
  continuation de ligne). Ecrire les scripts par l'outil d'ecriture.
- /!\ astro.config.mjs porte trailingSlash: 'always' : une sonde qui appelle
  /expertises/cvc SANS barre finale recoit 404 sur astro preview, alors que
  Vercel sert les deux en 200. Toujours poser la barre finale.
- /!\ Un script du scratchpad ne resout pas node_modules par le nom : importer
  puppeteer-core par CHEMIN ABSOLU en file:/// (un chemin nu " C:/... " est
  refuse par le chargeur ESM de Node), et c'est
  node_modules/puppeteer-core/lib/puppeteer/puppeteer-core.js (PAS de esm/).
- /!\ scrollIntoView PUIS getBoundingClientRect DANS LE MEME evaluate() rend un
  rectangle d'AVANT le defilement : la capture tombe ailleurs (constate en
  N28). Defiler, laisser passer deux trames (double requestAnimationFrame),
  puis mesurer.
- /!\ npm run preview ne se lance PAS avec un & dans un appel Bash au premier
  plan. Le lancer en tache de fond, ATTENDRE par une boucle sur curl (jamais
  par un delai), et le FERMER en fin de session : un serveur orphelin fausse
  la session suivante.
- /!\ astro preview rend 304 sur une page deja vue : setCacheEnabled(false) et
  TOLERER 304 dans les asserts de statut.
- `npm run captures` EXISTE pour un jeu multi-paliers : NE PAS LE REBATIR. Sa
  table ROUTES est CURATEE (14 gabarits) et --route filtre sur le nom de
  DOSSIER de cette table.
- /!\ LES BACKTICKS D'UN MESSAGE DE COMMIT SONT EXECUTES PAR BASH quand on
  passe par -m " ... ". Passer par `git commit -F <fichier>`, immunise.
- La CLI vercel repond " Not authorized " : c'est le PUSH qui deploie. Verifier
  par un MARQUEUR DU BUILD, jamais par un delai. Depot PARTAGE : rejouer
  git status au moment de committer.
- npm run preview NE MESURE PAS LA PERFORMANCE (aucune compression, 0,8 s de
  biais sur la chaine bloquante). La performance se mesure sur le deploiement.
- PYTHONIOENCODING=utf-8 devant toute commande python qui imprime des accents.

Portee de commit : selon l'objet - fix(...) / a11y(...) / docs(...). Tout
changement de dessin va DANS LE MEME COMMIT que son amendement dans
.claude/rules/tailwind-design-tokens.md.

Terminer par le prompt de lancement de la session suivante, en annexe de ce
plan et reproduit integralement dans le message final - la regle de continuite
est dans CLAUDE.md parce qu'elle a ete manquee deux fois.
```
