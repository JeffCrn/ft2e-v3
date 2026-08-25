# Chantier — le bloc des secteurs de l’accueil, en coupe déployée

> **Ouvert le 2026-08-17.** Chantier **additif** : il ajoute une pièce, il ne solde pas
> de dette. Le chantier de réduction de dette est **en pause** (`docs/23-etat-de-l-art.md`).
>
> **Objet.** Remplacer la liste tabulaire de la section « 04 — secteurs » de l’accueil
> par une pièce visuelle, spécifiée par la maquette
> `docs/maquettes/ft2e-accueil-bloc-secteurs.html` (planche 2b, « la coupe déployée »,
> révision a du 24.08.2026).
>
> **État : rien n’est construit.** Ce document porte le **constat mesuré** du 2026-08-17
> et le **prompt de lancement** (annexe A). Les arbitrages du § 3 sont à rendre **avant**
> tout montage.

---

## 1. Ce que la maquette prescrit

C’est une planche de conception complète, en neuf sections, et elle est **de bonne
qualité** : elle porte ses cotes, ses six états, ses trois régimes de largeur, ses
contrastes mesurés, son implantation dans le dépôt, et — ce qui est rare — **elle
déclare elle-même son écart à la charte et sa mesure en limite** (§ 08).

Le mécanisme : sept tranches verticales, une seule ouverte à la fois. La tranche
ouverte sert **un cliché principal en 16:10** et le **film de quatre vignettes en 3:2** du
secteur. Pointer une vignette promeut son cliché dans un cadre qui ne bouge pas. Le texte
n’est jamais posé sur un cliché : cartouche de réserve, en pied.

Cotes de conception, à 1 200 px de conteneur : ouverture **690**, six tranches
fermées de **76**, six filets de 1 px — somme contrainte à **1 152**, la largeur
utile. Cliché principal **690 × 431**, film **4 × 172 × 115**.

## 2. Le constat mesuré — la maquette et les fichiers fournis se contredisent

Mesuré le 2026-08-17 sur `assets/sources/secteurs/` (61 fichiers) et sur le dépôt.
**Aucun de ces trois écarts n’est rédhibitoire, tous appellent une décision.**

| Point | La maquette prescrit | Les fichiers portent | Conséquence |
|---|---|---|---|
| **Résolution** | 2 400 px de large au minimum | **1 200 px**, les 61 | le cliché principal est servi à 690 px ; à 2× de densité il en faudrait **1 380**. Les sources sont **sous le 2×** pour le cliché principal, au-dessus pour les vignettes (172 × 2 = 344) |
| **Rapport** | 16:10 (cliché) et 3:2 (film), depuis le même fichier | **1200 × 896**, soit **1,339** — du 4:3 | ni l’un ni l’autre, et **hors charte** (21:8, 16:10, 3:2 seulement). Un recadrage est **obligatoire** : 1200 × 750 pour le 16:10, 1200 × 800 pour le 3:2 — les deux tiennent dans la source, mais le cadrage reste à décider |
| **Nombre** | 4 par secteur, soit **28** | **61**, répartis **5 · 13 · 13 · 9 · 6 · 10 · 5** | le minimum est **5**, donc un film de quatre est tenable partout. Mais **33 clichés resteraient inemployés**. La pièce tient 3 à 6 sans redessin |

### Les dossiers ne portent pas les intitulés de l’énumération

| Dossier fourni | Intitulé de la fiche `secteurs` | Écart |
|---|---|---|
| `Logement` | `Logements` | singulier / pluriel |
| `Tertiaire-ERP` | `Tertiaire / ERP` | tiret / barre oblique |
| `Études d’exécution  - BIM` | `Études d’exécution / BIM` | tiret, et **DEUX espaces** avant lui |
| `Coordination SSI`, `Industriel et commercial`, `Monotechnique`, `Patrimoine` | identiques | — |

⚠ **L’appariement fiche / secteur se fait en égalité de chaînes**, et l’énumération
porte l’apostrophe **typographique** depuis le 2026-08-16. Une table de correspondance
**explicite** est donc obligatoire : rien ne doit être déduit d’un nom de dossier.

### Deux dossiers portent des sous-familles que la maquette n’a pas prévues

`Logement` se subdivise en `gros-collectif` (6), `petit-collectif` (5) et
`individuel-en-bande` (2) ; `Tertiaire-ERP` en `ERP` (6) et `Tertiaire` (4). C’est de
l’information éditoriale : elle peut guider la **sélection** (un cliché par
sous-famille) ou nourrir la **légende**. À trancher.

### Ce que le dépôt confirme, et qui n’était pas acquis

- **L’accueil ne porte aujourd’hui AUCUNE réserve profonde** (ni `bg-profond`, ni
  `.plan-encre`) ; le seul `duotone-photo` de la page ne compte pas au décompte, la
  charte l’exclut explicitement. **La question « la réserve du bloc est-elle la seule de la
  page ? » du § 08 de la maquette est donc tranchée : oui.**
- **`secteur.image` n’est rendu que sur `/secteurs/[slug]`**, jamais sur l’accueil. La
  maquette voit juste en parlant de remplacer une liste tabulaire — mais **toute
  évolution du schéma touchera aussi cette page**, qui consomme `image` et `image_alt`.
- **Les 7 marqueurs `[DÉMO]` du site sont exactement ces 7 `image_alt`.** Le chantier les
  lève **si et seulement si** les clichés fournis sont des photographies réelles. Sinon,
  ils se reportent sur les nouveaux champs (règle 1 de `CLAUDE.md`).
- **`assets/` est ignoré par git** (motif ancré, sans effet sur `src/assets/`). Les 61
  sources **ne sont pas versionnées** : les clichés retenus doivent être copiés dans
  `src/assets/secteurs/`, ce qui est **aussi** la condition pour qu’`astro:assets`
  produise l’AVIF, le WebP et le `srcset`.
- **L’accueil ne sert que 2 images aujourd’hui**, dont une seule en AVIF.

## 3. Les arbitrages à rendre AVANT tout montage

Aucun n’est décidable depuis le dépôt. Les trois premiers viennent de la maquette
elle-même.

| № | Question | Enjeu |
|---|---|---|
| **A** | **L’écart au survol est-il accepté ?** La charte écrit que le survol est une bascule de fond, **jamais un déplacement**. Ouvrir une tranche déplace ses voisines — c’est le mécanisme même de la coupe, il n’est pas réductible | soit un **amendement A10** (le précédent A9 existe, et il vit dans `.claude/rules/tailwind-design-tokens.md`, pas dans le PDF), soit la piste **1a** qui répond au même besoin sans écart |
| **B** | **Quelle cote pour le cliché principal ?** 690 × 431 occupe **22,9 %** d’un écran de 1440 × 900, pour une borne de réserve profonde au cinquième | **issue a** : 552 × 345, la taille de conception de l’appui — la mesure tombe à **14,7 %** ; **issue b** : tenir 690 et invoquer « la mesure prévaut sur la règle », en portant le chiffre au commentaire |
| **C** | **Le bloc reste-t-il en position 04 ?** Avec l’image il devient le premier moment visuel après la vedette, **avant les références** | ordre de lecture de l’accueil |
| **D** | **Combien de clichés par secteur, et lesquels ?** Les sources vont de 5 à 13 | un film **fixe à 4** (33 clichés inemployés) ou **variable de 4 à 6** ; et qui choisit — FT2E ou la session |
| **E** | **Ces photographies sont-elles réelles ?** | si oui, les 7 `[DÉMO]` tombent ; si non, ils se reportent. Il faut aussi le **crédit photographique**, que le schéma de la maquette rend obligatoire |
| **F** | **Les planches techniques peuvent-elles entrer dans le film ?** Le site en produit 23, composées dans la rampe | question du § 08 de la maquette, restée ouverte |

## 4. Ce que le chantier touchera

Repris du § 09 de la maquette, **corrigé de ce que le dépôt dit**.

| Fichier | Nature |
|---|---|
| `src/components/blocs/CoupeSecteurs.astro` | pièce nouvelle |
| `src/pages/index.astro` | section 04 : la liste tabulaire cède la place ; titre, puce et complément inchangés |
| `src/content.config.ts` | collection `secteurs` : `cliches`, liste de 3 à 6 objets `{ image, legende, alt, credit }` |
| `public/admin/config.yml` | widget `list`, **dans le même commit** que le Zod (sous-agent `content-modeller`) |
| `src/assets/secteurs/` | les clichés retenus, **jamais dans `public/`** |
| `src/lib/photos.ts` | `photoSecteur()` sur le modèle de `photoEquipe()` — le frontmatter garde la graphie publique, le rendu résout |
| `src/pages/secteurs/[...slug].astro` | ⚠ **absent du § 09 de la maquette** : cette page consomme `image` et `image_alt`, elle suivra tout changement de schéma |

## 5. La contrainte qui décidera de la faisabilité

**Le LCP mobile de l’accueil est DÉJÀ au seuil, pas sous le seuil** : sept tirs donnent
1 656, 1 658, 1 681, 1 768, 1 806, 1 807 et 1 815 ms pour un
budget de 1 800. La page sert aujourd’hui **deux images** ; la maquette en met
**quatre dans le chemin critique**.

C’est le risque principal du chantier, et il se mesure — il ne se raisonne pas. Le
précédent est favorable : la session S1 a fait passer `/equipe/` de **4 766 à
243 Kio** en déplaçant les fichiers dans `src/assets/` et en passant par `<Picture>`
(AVIF + WebP + `srcset`). Mais la marge, ici, est de quelques dizaines de millisecondes.

⚠ **La performance ne se mesure jamais sur `npm run preview`**, qui ne compresse rien
(0,8 s de biais sur la chaîne bloquante), **ni sur un seul tir**.

---

## Annexe A — prompt de lancement (à coller telle quelle en session neuve)

````
Chantier FT2E v3 - rendre visuel le bloc des secteurs de la page d'accueil.

Contexte. FT2E v3 est un site institutionnel Astro statique (Astro 6, Tailwind 4,
TypeScript strict), deploye en demonstration client sur https://ft2e-v3.vercel.app,
indexation verrouillee par triple securite (robots.txt Disallow, meta noindex, header
X-Robots-Tag) - ne pas y toucher. Le design system est la charte v3 « plans et
profondeur » revision 2.1 : rampe monochrome 197 degres, AUCUNE couleur d'accent, relief
par trois rangs d'ombre a l'encre translucide, filets de 1 px hierarchises par
l'OPACITE et jamais par l'epaisseur, rayon 0 partout, trame de 28 px. La source de
verite du design est .claude/rules/tailwind-design-tokens.md, et elle prevaut sur tout
autre support.

Le chantier de reduction de dette est EN PAUSE depuis le 2026-08-17. Ne pas le rouvrir.
Son etat consolide est dans docs/23-etat-de-l-art.md - le lire, il porte les points
ouverts, les decisions a ne pas re-litiger et les pieges d'outillage de cette machine.

CE CHANTIER EST ADDITIF : il ajoute une piece, il ne solde aucune dette.

LIRE D'ABORD, DANS CET ORDRE :
  1. docs/superpowers/plans/2026-08-17-chantier-bloc-secteurs.md - le constat mesure le
     2026-08-17 et les six arbitrages. C'est le document de ce chantier.
  2. docs/maquettes/ft2e-accueil-bloc-secteurs.html - la maquette. ATTENTION : c'est une
     page BUNDLEE, le contenu reel est dans un manifeste JSON deballe par JavaScript.
     Lire le fichier brut ne montre que l'enveloppe. Extraire le bloc
     <script type="__bundler/template"> et le decoder en JSON (une chaine de 110 k
     signes) pour voir la specification.
  3. .claude/rules/tailwind-design-tokens.md et .claude/rules/accessibility-rgaa.md.

0. OUVRIR EN DEMANDANT LES ARBITRAGES. Six questions, aucune decidable depuis le depot,
   toutes detaillees au § 3 du document de chantier. NE RIEN CONSTRUIRE AVANT d'avoir au
   moins A, B et D :
   A. l'ecart au survol est-il accepte comme amendement A10, ou faut-il la piste 1a ?
      La charte ecrit que le survol est une bascule de fond, JAMAIS un deplacement ;
      ouvrir une tranche deplace ses voisines, et c'est le mecanisme meme de la coupe.
      Le precedent A9 montre ou vit un amendement d'application : dans
      .claude/rules/tailwind-design-tokens.md, pas dans le PDF de la charte.
   B. cliche principal a 690 x 431 (22,9 % d'un ecran de 1440 x 900, borne de reserve
      profonde au cinquieme) ou a 552 x 345 (14,7 %) ?
   C. le bloc reste-t-il en position 04, avant les references ?
   D. combien de cliches par secteur, et qui les choisit ?
   E. les photographies fournies sont-elles reelles ? (voir le point 2 ci-dessous)
   F. les planches techniques peuvent-elles entrer dans le film ?

1. LE CONSTAT MESURE, A REVERIFIER PLUTOT QU'A CROIRE. Mesure du 2026-08-17 sur les
   61 fichiers de assets/sources/secteurs/ :
   - TOUS font 1200 x 896, soit un rapport de 1,339 (du 4:3). La maquette demande
     2400 px de large au minimum, et les deux rapports 16:10 (cliche principal) et 3:2
     (film) depuis le MEME fichier. La charte n'admet que 21:8, 16:10 et 3:2.
     -> un recadrage est OBLIGATOIRE : 1200 x 750 pour le 16:10, 1200 x 800 pour le 3:2.
        Les deux tiennent dans la source. Le cadrage lui-meme reste a decider, et les
        fichiers n'ont PAS ete pris selon la consigne « cadrer large, sujet centre » que
        la maquette adressait au fournisseur.
     -> la resolution est SOUS le 2x pour le cliche principal (690 x 2 = 1380 > 1200) et
        au-dessus pour les vignettes (172 x 2 = 344). A dire clairement plutot qu'a
        masquer : c'est un ecart a la maquette, pas un detail.
   - repartition : Coordination SSI 5, Industriel et commercial 13, Logement 13,
     Monotechnique 9, Patrimoine 6, Tertiaire-ERP 10, Etudes d'execution - BIM 5.
     Le minimum est 5, donc un film de quatre est tenable partout ; mais 33 cliches
     resteraient inemployes.
   - deux dossiers portent des SOUS-FAMILLES que la maquette n'a pas prevues :
     Logement -> gros-collectif (6), petit-collectif (5), individuel-en-bande (2) ;
     Tertiaire-ERP -> ERP (6), Tertiaire (4). C'est de l'information editoriale : elle
     peut guider la selection ou nourrir la legende.

2. LE PIEGE DE NOMMAGE, QUI CASSE LE BUILD SI ON LE DEDUIT. Les dossiers fournis ne
   portent pas les intitules de l'enumeration Zod :
        Logement                      ->  Logements
        Tertiaire-ERP                 ->  Tertiaire / ERP
        Etudes d'execution  - BIM     ->  Etudes d'execution / BIM
   (les quatre autres sont identiques). Le dossier des etudes porte l'APOSTROPHE
   TYPOGRAPHIQUE et DEUX espaces avant son tiret. L'enumeration, elle, porte
   l'apostrophe typographique depuis le 2026-08-16, et l'appariement fiche/secteur se
   fait en EGALITE DE CHAINES : une graphie fautive fait echouer le build, et c'est
   voulu. Ecrire une table de correspondance EXPLICITE, ne rien deduire d'un nom de
   dossier.

3. LA CONTRAINTE QUI DECIDERA DE LA FAISABILITE - le LCP mobile de l'accueil est DEJA
   AU SEUIL, pas sous le seuil. Sept tirs : 1 656, 1 658, 1 681, 1 768, 1 806, 1 807 et
   1 815 ms pour un budget de 1 800. L'accueil sert aujourd'hui DEUX images ; la
   maquette en met QUATRE dans le chemin critique.
   Le precedent est favorable : la session S1 a fait passer /equipe/ de 4 766 a 243 Kio
   en deplacant les fichiers dans src/assets/ et en passant par <Picture> (AVIF + WebP
   + srcset). Mais la marge est de quelques dizaines de millisecondes.
   -> mesurer AVANT et APRES, sur le DEPLOIEMENT et jamais sur npm run preview (qui ne
      compresse rien : 0,8 s de biais sur la chaine bloquante), et JAMAIS sur un seul
      tir - le LCP de cette page varie de 160 ms d'un tir a l'autre.
   -> si le budget ne tient pas, le dire et proposer, pas contourner en silence.

4. IMPLANTATION. Le § 09 de la maquette la donne ; il est JUSTE, a une omission pres.
     src/components/blocs/CoupeSecteurs.astro   piece nouvelle
     src/pages/index.astro                      section 04, la liste tabulaire cede la
                                                place ; titre, puce et complement
                                                inchanges
     src/content.config.ts                      collection secteurs : ajouter `cliches`,
                                                liste de 3 a 6 objets
                                                { image, legende, alt, credit }
     public/admin/config.yml                    widget list, DANS LE MEME COMMIT que le
                                                Zod (regle du depot, sous-agent
                                                content-modeller)
     src/assets/secteurs/                       les cliches retenus - JAMAIS dans
                                                public/, qui est recopie tel quel et
                                                n'est pas un pipeline
     src/lib/photos.ts                          photoSecteur() sur le modele de
                                                photoEquipe() : le frontmatter garde la
                                                graphie publique, le RENDU resout ;
                                                l'absence d'entree dans le glob EST
                                                l'absence de fichier
   ⚠ OMISSION DE LA MAQUETTE : src/pages/secteurs/[...slug].astro consomme image et
     image_alt. Toute evolution du schema la touche. La maquette ne la cite pas.
   ⚠ assets/sources/ est IGNORE par git (motif /assets/ ancre, sans effet sur
     src/assets/). Les 61 sources ne sont pas versionnees : ce qui n'est pas copie dans
     src/assets/secteurs/ n'existe pas pour le depot.

5. LES SEPT MARQUEURS [DEMO]. Ce sont EXACTEMENT les sept image_alt des fiches de
   src/content/secteurs/, et ils sont les seuls du site. Ils se levent SI ET SEULEMENT
   SI les cliches fournis sont des photographies reelles (question E). Sinon ils se
   reportent sur les nouveaux champs : la regle 1 de CLAUDE.md impose que toute donnee
   de demonstration soit signalee. Ne pas les faire disparaitre par effet de bord d'un
   changement de schema.

6. CE QUE LA MAQUETTE A DEJA TRANCHE, ET QU'IL NE FAUT PAS REDECIDER. Elle porte ses
   cotes (ouverture 690, six tranches de 76, six filets de 1 px, somme contrainte a
   1 152), ses six etats sans couleur, ses deux transitions sur la courbe unique
   cubic-bezier(.2,.7,.2,1), ses trois regimes de largeur (au-dela de 1 200 ; 768 a
   1 199 ; sous 768 px la coupe SE REDRESSE en accordeon vertical - aucune tranche
   verticale sous 768, un intitule pivote n'est pas lisible sur telephone), et ses
   contrastes mesures. Les lire plutot que de les reinventer.
   Deux points qu'elle laisse EXPRESSEMENT ouverts au montage :
   - la promotion au pointage demande un equivalent clavier ; l'ouverture au focus le
     donne pour les tranches, la fleche gauche-droite dans le film reste a ecrire ;
   - un delai de 120 ms avant ouverture, contre les ouvertures involontaires au passage
     du pointeur, est A MESURER sur maquette avant decision.
   Et une question qu'elle pose et que le depot tranche : « la reserve profonde du bloc
   est-elle la seule de la page ? » -> OUI. Verifie le 2026-08-17 : l'accueil ne porte
   aujourd'hui ni bg-profond ni .plan-encre, et le duotone ne compte pas au decompte
   (la charte l'exclut explicitement).

7. ACCESSIBILITE - RGAA AA, et le 100 de Lighthouse est opposable.
   - L'accueil est recue a 96, et c'est ADMIS : l'exception D1 porte sur un MOTIF - le
     complement de titre en text-clair aria-hidden. La condition est stricte : ce doit
     etre la SEULE violation. Toute violation NOUVELLE apportee par ce bloc est un
     blocage, pas une exception.
   - Le complement clair se signale exactement la ou il est pose sur un APLAT PLEIN,
     qu'axe sait resoudre. Ce bloc introduit des aplats profonds : s'attendre a ce que
     le score bouge, et NOMMER la violation dans le compte rendu. Un score non explique
     est indistinguable d'une regression.
   - Cibles tactiles 44 x 44 minimum ; focus par polarite (2 px pivot sur fond clair,
     2 px clair sur reserve profonde - le pivot y est invisible a 2,85) ; la legende
     JAMAIS posee a meme le cliche mais dans un cartouche de reserve (voile sur profond,
     16,24) ; prefers-reduced-motion supprime les deux transitions ; sans JavaScript la
     piece est rendue avec la tranche 01 ouverte et chaque tranche fermee est un lien -
     rien ne disparait.

8. PIEGES DU DEPOT ET DE CETTE MACHINE, verifies, a ne pas redecouvrir :
   - TOUT <script> de composant .astro qui appelle addEventListener doit s'initialiser
     via document.addEventListener('astro:page-load', initX) avec un guard
     dataset.bound. Sinon le composant devient INERTE apres la premiere navigation View
     Transitions, sans que rien ne le signale. C'est la regle 9 de CLAUDE.md, et ce bloc
     est interactif : elle s'applique de plein fouet.
   - UNE MESURE DE MISE EN PAGE (un plafond, une borne) s'ecrit en CSS DE COMPOSANT,
     pas en classe Tailwind arbitraire unique : une valeur arbitraire employee une seule
     fois dans le depot peut disparaitre a l'elagage sans un mot du build.
   - UNE COULEUR s'ecrit en CLASSE litterale (stroke-encre, bg-profond), jamais en
     var(--color-...) dans un attribut, et jamais construite par concatenation :
     Tailwind v4 elague les variables de theme qu'aucune classe n'emploie.
   - Tailwind v4 lit le .gitignore et elague les repertoires qui y correspondent : tout
     motif doit etre ANCRE. Controle : git check-ignore -v src/pages/<d>/index.astro
     doit ne rien rendre.
   - UN BUILD VERT NE PROUVE PAS QUE LA PAGE S'AFFICHE, ni meme que le texte existe.
     Apres toute modification de mise en page, controler le RENDU (npm run preview +
     capture) a la largeur de lecture reelle.
   - Chrome refuse toute fenetre sous 500 px, EN HEADLESS AUSSI : une capture en
     --window-size=390,900 compose a ~500 px puis ROGNE l'image, ce qui montre un
     debordement credible et faux. Les largeurs de telephone se mesurent par une IFRAME
     servie en meme origine. Or ce bloc a un regime specifique SOUS 768 px : il sera
     mesure la, donc le piege est sur le chemin.
   - npm run captures existe deja pour un JEU de captures multi-paliers : ne pas le
     rebatir.
   - /tmp n'existe pas depuis ce shell ; npx lighthouse n'accepte pas les chemins
     Git-Bash /c/... en --output-path (il n'ecrit rien, en silence).
   - LE DEPOT EST PARTAGE et un hook Stop y commite et pousse seul : « rien en attente
     de push » est une mesure PERISSABLE, a rejouer au moment de committer et pas
     seulement a l'ouverture. Controler en deux temps : git ls-remote origin master,
     puis un marqueur de build dans le HTML servi.
   - Les insecables sont normalisees en entree des outils d'edition, et pas de facon
     deterministe. Pour ecrire du texte francais dans un fichier du depot : contenu en
     clair avec des JETONS pour les seuls caracteres sensibles, substitution en fin de
     course par chr(), et assertion que le source du script n'en contient AUCUN en
     litteral. Une ancre de remplacement se COPIE du fichier, elle ne se retape pas.
   - Le corpus met une espace ORDINAIRE devant le tiret cadratin (350 sur 350) et une
     INSECABLE devant : ; ? et ». CLAUDE.md, lui, est en apostrophes droites (140, zero
     courbe) : c'est un fichier d'instructions, pas du contenu destine au visiteur.

9. LA CONNEXION AU CMS EST CASSEE, ET CE N'EST PAS DANS LE DEPOT. /api/auth?provider=
   github rend HTTP 500 faute de deux variables d'environnement Vercel et d'une callback
   GitHub. Trois gestes hors depot, que SEUL L'UTILISATEUR peut faire, dans
   docs/22-prise-en-main-decap.md § 0. Il l'a AJOURNE en connaissance de cause le
   2026-08-17 : le rappeler une fois en ouverture, puis le respecter. Consequence pour
   ce chantier : la nouvelle collection Decap ne pourra PAS etre essayee dans
   l'interface. La modifier quand meme, dans le meme commit que le Zod, et le dire.

Recette de fin de session : npm run typecheck (0 erreur), npm run build (46 pages),
python scripts/controle-liens-internes.py (0 lien mort), controle du RENDU de l'accueil
aux TROIS regimes de largeur du bloc (au-dela de 1 200, entre 768 et 1 199, sous 768),
Lighthouse mobile sur le DEPLOIEMENT avec plusieurs tirs (performance ET accessibilite),
et consignation dans docs/superpowers/plans/2026-08-17-chantier-bloc-secteurs.md.

Portee de commit : plusieurs commits nets valent mieux qu'un fourre-tout - les portees
sont feat(accueil), content, design-system, a11y, perf, docs selon les points. Le
changement de schema Zod et celui de public/admin/config.yml vont DANS LE MEME COMMIT.

Termine par le prompt de lancement de la session suivante, en annexe du plan de ce
chantier et reproduit integralement dans ton message final. Cette regle est dans
CLAUDE.md parce qu'elle a ete manquee deux fois.
````
