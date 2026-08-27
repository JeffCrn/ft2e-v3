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


---

## 6. Session de montage du 2026-08-25 — arbitrages, versement, pièce

### Les six arbitrages, rendus en ouverture

| № | Décision |
|---|---|
| A | **Amendement A10** — l'ouverture au survol est acceptée, bornée (une direction, 300 ms, courbe unique, délai d'intention de 120 ms mesuré), consignée dans `.claude/rules/tailwind-design-tokens.md` § Les amendements |
| B | **552 × 345** — réserve profonde à 14,7 % d'un écran 1440 × 900, tranche fermée 99 px, pièce 438 px. Bénéfice collatéral : le 2× (1 104 px) tient dans les sources de 1 200 px — l'écart de résolution de la maquette disparaît |
| C | **Position 04 conservée**, avant les références |
| D | **Tirage aléatoire AU BUILD** (précision D-bis rendue en séance), quatre clichés par secteur, au moins un représentant par sous-famille présente (préfixes des noms de fichiers). Chaque déploiement recompose les films ; entre deux, l'affichage est stable, zéro JavaScript de tirage, seuls les clichés tirés sont servis |
| E | **Photographies réelles, crédit © FT2E** — les sept derniers marqueurs [DÉMO] du site tombent avec les images IA qu'ils signalaient |
| F | **Pas de planches techniques dans le film** — exclu par la mesure : une vignette de 137 px servirait vignette.svg (conçue pour 300) à 0,46, mono à 4,1 px sous le plancher de 6,5 ; et le cadre 16:10 exigerait de recadrer un dessin 3:2, interdit (règle 13) |

### Le corpus versé — 44 retenus sur 61, et pourquoi

Une revue visuelle des 61 fichiers a précédé le versement. **17 écartés**, deux motifs :

- **14 images de synthèse ou photomontages de tiers** (perspectives de promoteur ou
  d'architecte, insertions de permis — personnages, ciels et végétation rendus) :
  `Patrimoine/05`, `Tertiaire-ERP/Tertiaire-01`, `Industriel et commercial/01, 07, 10, 13`
  (le 13 est la perspective du campus Dufour, le 01 une perspective de logements mal
  classée), `Logement/gros-collectif-01, 04, 05, 06`, `Logement/individuel-en-bande-02`,
  `Logement/petit-collectif-02, 04, 05`. Publier une perspective de tiers est exactement
  ce que le chantier des planches a dépublié (neuf perspectives sans crédit obtenu).
- **3 documents dessinés sur le fond de plan de l'architecte** : `Coordination SSI/05`
  (zonage incendie) et `Études d'exécution  - BIM/02 et 04` (plans EXE). Même précédent :
  les « douze extraits reproduisant leur fond de plan » retirés des fiches. Les vues
  Revit 01, 03 et 05 des Études sont conservées — matière MEP propre de FT2E, volumes
  génériques — avec réserve consignée.

Conséquence sur les films : quatre partout, sauf **Études d'exécution / BIM : trois**
(la pièce tient trois à six sans redessin) ; **Coordination SSI : quatre sur quatre**,
le tirage y est une simple permutation d'ordre.

⚠ **Artefacts d'agrandissement génératif relevés sur des clichés RETENUS** — petits
textes nets mais faux : plaque « Cbasté Egetite Fraternité » (`Tertiaire-03`, mairie),
panneau de stationnement illisible (`Monotechnique/02`), étiquettes d'équipements
(`Coordination SSI/01 et 03`), vitrine partiellement altérée (`Industriel/03`). Les
scènes sont réelles et identifiables (Sablonceaux, Port des Salines, Cabanes urbaines,
fuselages rochelais) : les fichiers ont vraisemblablement été suréchantillonnés par IA
pour atteindre 1 200 px. Sous duotone à 552 px l'altération se remarque peu ;
**à faire valider par FT2E avant production**. L'arbitrage E a été rendu puis maintenu
en connaissance de cause, la mémoire du dépôt (« visuel agrandi : texte net mais
faux = image régénérée, ne pas publier ») ayant été signalée en séance.

Chacun des 44 retenus porte légende (18 signes au plus, minuscules), alternative
textuelle rédigée à la vue du cliché, crédit © FT2E, et `famille` là où le nom de
fichier en portait une (gros-collectif, petit-collectif, individuel-en-bande, erp,
tertiaire). Les fichiers vivent dans `src/assets/secteurs/<slug>/` (pipeline
astro:assets — AVIF, WebP, srcset) ; le frontmatter garde la graphie publique
`/images/secteurs/<slug>/<fichier>` et `photoSecteur()` résout, sur le modèle de
l'équipe. Les 17 écartés restent dans `assets/sources/`, non versionnés.

### Le montage — écarts assumés à la maquette, tous motivés

| Écart | Motif |
|---|---|
| Tout le bloc en `loading="lazy"` (le § 09 voulait les quatre calques du secteur 01 dans le chemin critique) | le bloc est sous la ligne de flottaison en position 04 et le LCP est au seuil ; mesuré sans dégradation |
| `cliches` = corpus (min 3, sans plafond) et non le film 3–6 | conséquence de l'arbitrage D : le film est tiré du corpus au build (`filmSecteur()`, `src/lib/secteurs.ts`) ; la borne 3–6 de la maquette portait sur le film |
| Champ `famille` ajouté à l'objet cliché | la contrainte de couverture exige une donnée explicite — rien ne se déduit d'un nom de fichier (piège de nommage du § 2) |
| Focus sur une tranche : ouverture puis REPORT du focus sur la première vignette | la face fermée disparaît à l'ouverture (`display:none`) : sans report, le focus serait perdu sur un élément masqué. La navigation clavier vers la fiche passe par « Lire la fiche » en pied |
| Clic ou toucher d'une tranche fermée : la première activation ouvre, la seconde navigue | un lien qui ouvre ET navigue au même geste est impossible au toucher ; Entrée au clavier navigue, le focus ayant déjà ouvert |
| Géométrie par rapports (`aspect-ratio` 16/10 et 3/2), non par hauteurs figées | à 552 px d'ouverture, les cotes de la maquette (345, 92, 438) en découlent ; les régimes fluides aussi |

**Le délai d'intention de 120 ms est ADOPTÉ, sur mesure** (Puppeteer sur le build,
1440 × 900, MutationObserver sur `est-ouverte`) :

| Scénario | Avec 120 ms | Sans délai |
|---|---|---|
| traversée vive, 23 ms par tranche | **1** ouverture — le point d'arrêt final du pointeur, qui est une intention | 6, par construction |
| traversée hésitante, 175 ms par tranche | 6 — un parcours lent ouvre au fil du regard, comportement de consultation | 6 |
| arrêt de 200 ms sur une tranche | 1 — l'intention ouvre | 1 |

Trois pièges de fabrication, tous invisibles au build, vus au rendu :

- `min-width: 0` obligatoire sur les vignettes flex — sans lui, la largeur intrinsèque
  de l'image rend les vignettes inégales ;
- le fond qui dessine les filets inter-tranches à travers les `gap` du rail doit être
  `md:bg-filet-2` et non `bg-filet-2` : en accordéon (`display:block`, plus de gap) il
  lave tout le bloc d'encre à 16 % — les bordures des `<li>` prennent le relais ;
- un commentaire JSX entre la parenthèse d'un `.map` et son élément casse la
  compilation d'esbuild (« Expected ) but found $$render »).

### Recette du 2026-08-25

- `npm run typecheck` : 0 erreur — sonde Props de `CoupeSecteurs` faite dans les
  règles (valeur invalide, ts(2322) levée, retombée à zéro au retour) ;
- `npm run build` : 46 pages ;
- `python scripts/controle-liens-internes.py` : 0 lien mort, 23/23 fiches à 5 liens ;
- rendu contrôlé aux trois régimes (`npm run captures -- --route 01-accueil`) :
  conception à 1440/1920 ✓, intermédiaire à 768/1024 ✓, accordéon à 390 ✓. Les
  « 46 images non chargées » des avertissements de capture sont exactement les calques
  et vignettes des tranches fermées (5 × 8 + 6) : le lazy fait son travail ;
- déploiement vérifié par marqueur de build (`data-coupe` dans le HTML servi) ;
- Lighthouse mobile sur le déploiement — **accessibilité 96** (3 tirs), violation
  unique NOMMÉE : `color-contrast` sur le complément de titre `text-clair aria-hidden`
  d'une section, le motif exact de l'exception D1. **Aucune violation nouvelle du
  bloc** — le cartouche voile sur profond passe à 16,24. **Performance 97–100**
  (6 tirs), **LCP 1 693 / 1 694 / 1 705 / 1 709 / 1 837 / 2 037 ms** (premier tir à
  froid), médiane ≈ 1 707 contre ≈ 1 768 avant chantier (7 tirs, 1 656–1 815) : pas de
  dégradation attribuable au bloc. CLS 0,000 ; TBT ≤ 162 ms ;
- commits : `844e23a` content(secteurs), `fdd8225` feat(accueil), `648a079`
  docs(design-system) A10, puis le commit docs de consignation.

### Ce qui reste ouvert après le montage

1. **Validations FT2E** (avant production, pas avant démonstration) : les 17 écartés et
   leurs motifs ; les artefacts d'agrandissement sur clichés retenus ; les 44 légendes
   et alternatives ; le crédit © FT2E ; le principe du tirage à chaque déploiement.
2. **Lecteur d'écran** : NVDA n'est pas passé sur la pièce cette session — l'exigence
   du dépôt (« au moins une fois par page avant livraison ») reste due.
3. **Decap** : la collection `cliches` (widget list, `media_folder` par slug) ne pourra
   être essayée dans l'interface qu'après les trois gestes OAuth hors dépôt
   (docs/22 § 0, ajournés en connaissance de cause).
4. La question du § 08 de la maquette — la réserve du bloc est-elle la seule de la
   page ? — reste vraie au montage : aucun `bg-profond` hors la pièce sur l'accueil.

## Annexe B — prompt de la session suivante (à coller tel quel en session neuve)

````
Session de suite du chantier bloc secteurs - FT2E v3 (validations et finitions).

Contexte. FT2E v3 est un site institutionnel Astro statique (Astro 6, Tailwind 4,
TypeScript strict), deploye en demonstration client sur https://ft2e-v3.vercel.app,
indexation verrouillee par triple securite (robots.txt Disallow, meta noindex,
header X-Robots-Tag) - ne pas y toucher. Le design system est la charte v3
revision 2.1 ; la source de verite est .claude/rules/tailwind-design-tokens.md
(rampe monochrome 197, aucune couleur d'accent, filets 1 px par opacite, rayon 0,
courbe unique). Le chantier de reduction de dette est EN PAUSE
(docs/23-etat-de-l-art.md) - ne pas le rouvrir.

LA COUPE DEPLOYEE DES SECTEURS EST EN LIGNE depuis le 2026-08-25 (commits
844e23a, fdd8225, 648a079 + docs) : six arbitrages rendus (amendement A10
consigne aux tokens ; cote 552 x 345 ; position 04 ; tirage du film AU BUILD,
4 cliches par secteur, au moins un par famille ; cliches reels (c) FT2E, les
7 derniers [DEMO] du site sont tombes ; pas de planches dans le film). Corpus de
44 cliches verse dans src/assets/secteurs/, 17 fichiers ecartes (14 perspectives
ou photomontages de tiers, 3 documents sur fond de plan d'architecte).

LIRE D'ABORD, DANS CET ORDRE :
  1. docs/superpowers/plans/2026-08-17-chantier-bloc-secteurs.md - les § 6 a 8 :
     arbitrages rendus, corpus et exclusions detaillees, ecarts de montage,
     recette chiffree du 2026-08-25. C'est l'etat de reference.
  2. .claude/rules/tailwind-design-tokens.md - § Les amendements (A10 et ses
     bornes) ; et CLAUDE.md, qui reflete deja le nouvel etat.
  3. src/components/blocs/CoupeSecteurs.astro - la piece, son commentaire de
     dessin et son script (delai d'intention 120 ms, report de focus).

CE QUE CETTE SESSION FAIT :

1. RECUEILLIR LES VALIDATIONS FT2E, en ouverture, questions fermees :
   a. les 17 fichiers ECARTES (liste au § 6 du plan) - confirmes ecartes, ou
      FT2E fournit les autorisations d'auteur qui manquaient ?
   b. les ARTEFACTS D'AGRANDISSEMENT IA sur cliches retenus (liste au § 6 :
      plaque de mairie, panneau, etiquettes d'equipements, vitrine) - assumes
      en demonstration ? remplaces par les originaux non agrandis si FT2E les
      detient ? retires du corpus ?
   c. les 44 legendes et alternatives textuelles (redigees a la vue des
      cliches) et le credit (c) FT2E - a relire et confirmer par FT2E.
   d. le TIRAGE A CHAQUE DEPLOIEMENT (arbitrage D) : le film et son premier
      cliche changent a chaque build. Si FT2E prefere un affichage fige,
      remplacer filmSecteur() par une lecture ordonnee du corpus - petit
      changement, mais a documenter dans le meme commit.
2. PASSER NVDA sur l'accueil (la piece) et une page secteur - exigence RGAA du
   depot, non soldee au montage : tabulation (le focus ouvre une tranche et se
   reporte sur la premiere vignette du film), fleches gauche-droite dans le
   film, compteur aria-live="polite" qui annonce sans bavarder, calques
   aria-hidden muets. Consigner le releve dans le plan.
3. SI LE LCP INQUIETE : mediane 1 707 ms au montage, pires tirs 1 837 et 2 037
   (a froid), budget 1 800. Ne rien optimiser sans mesure : relever au moins
   cinq tirs supplementaires a des heures distinctes avant toute conclusion,
   sur le DEPLOIEMENT uniquement.

PIEGES VERIFIES, A NE PAS REDECOUVRIR (detail dans CLAUDE.md et
.claude/rules/astro-conventions.md) :
   - tout <script> de composant s'initialise via astro:page-load avec guard
     dataset.bound, sinon il devient inerte apres une navigation View
     Transitions ;
   - les MESURES de mise en page vivent en CSS de composant, les COULEURS en
     classes litterales (bg-profond, border-filet-3) - jamais var(--color-...)
     dans un attribut ni une classe construite ;
   - Tailwind v4 lit le .gitignore : motifs ANCRES uniquement ;
   - un build vert ne prouve pas le rendu : npm run captures -- --route
     01-accueil donne les trois regimes ; Chrome refuse toute fenetre sous
     500 px, meme headless - les largeurs de telephone passent par le jeu de
     captures ou une iframe meme origine ;
   - la performance se mesure sur le DEPLOIEMENT (npm run preview ne compresse
     rien : 0,8 s de biais), jamais en un seul tir ;
   - le depot est PARTAGE et un hook y commite et pousse seul : git ls-remote
     origin master AVANT de committer, marqueur de build dans le HTML servi
     APRES le push (la CLI Vercel repond Not authorized - c'est le push qui
     deploie) ;
   - les insecables sont NORMALISEES par les outils d'edition : le plan du
     chantier en porte, tout ajout s'y fait par script Python en mode APPEND,
     insecables construites par chr(160), jamais litterales, assertion de
     presence apres coup ;
   - dans un composant Astro, pas de commentaire JSX entre la parenthese d'un
     .map et son element (esbuild : Expected ) but found $$render) ;
   - sur un flex, min-width: 0 sur les items porteurs d'images, sinon
     l'intrinseque les rend inegaux.

DECAP : la connexion echoue en production (HTTP 500 - deux variables OAuth
Vercel et une callback GitHub manquantes ; trois gestes hors depot que seul
l'utilisateur peut faire, docs/22-prise-en-main-decap.md § 0, AJOURNES en
connaissance de cause). Le rappeler une fois en ouverture, puis le respecter.
La collection cliches (widget list, media_folder par slug) n'a pas pu etre
essayee dans l'interface : l'essayer des que l'OAuth sera pose.

Recette de fin de session : npm run typecheck (0 erreur), npm run build
(46 pages), python scripts/controle-liens-internes.py (0 lien mort), controle du
rendu de l'accueil aux trois regimes si la piece a change, Lighthouse mobile sur
le DEPLOIEMENT avec plusieurs tirs (performance ET accessibilite - l'accueil est
recu a 96, violation unique color-contrast du complement text-clair aria-hidden,
motif de l'exception D1 ; toute violation NOUVELLE est un blocage), et
consignation dans docs/superpowers/plans/2026-08-17-chantier-bloc-secteurs.md
par script append.

Portees de commit : content, a11y, perf, docs selon les points. Tout changement
de schema Zod va dans le MEME commit que public/admin/config.yml.

Termine par le prompt de lancement de la session suivante, en annexe du plan de
ce chantier et reproduit integralement dans ton message final - la regle de
continuite est dans CLAUDE.md parce qu'elle a ete manquee deux fois.
````


---

## 7. Session d'ajustements du 2026-08-26 — d'après-montage, sur directives FT2E

Neuf commits (`bfdc2b6` à `87476ef`), tous poussés et vérifiés par marqueur sur le
déploiement. Ce qui a changé, et ce qui a été arbitré :

- **Vedette de l'accueil**, en quatre itérations dirigées par FT2E : le titre est
  « Des études / techniques / portées jusqu'à / l'exécution » en QUATRE segments
  explicites, surtitre « BET La Rochelle — depuis 2008 », sous-titre pluridisciplinaire
  rétabli, `<title>` SEO « FT2E — BET fluides, thermique et électricité à La Rochelle ».
  Trois mesures au navigateur ont tranché ce que l'estime ratait deux fois : la borne
  haute de la vedette d'accueil est **5,1 rem** (« PORTÉES JUSQU'À » fait 964 px à
  81,6 px ; 1 228 px à la taille de charte pour 1 152 de boîte), le `text-balance` lui
  est **retiré** (ses césures sont explicites, l'équilibrage cassait le premier segment),
  et la version « Des études techniques » sur une ligne (4,25 rem) a été **refusée** par
  FT2E au profit du rang monumental. Tout est consigné dans le commentaire de
  `Hero.astro`. Une leçon de méthode au passage : une insécable posée dans un fichier
  source s'écrit en **échappement JavaScript** (`u00a0` précédé de la barre inverse),
  jamais en littéral — l'essai d'insécable intégrale sur « à La Rochelle » cassait
  d'ailleurs DANS le mot sur les fenêtres étroites (381 px de groupe pour 358 de boîte
  à 390 px, mesuré) et a été remplacé par des césures explicites.
- **L'accueil se lit désormais 01 relevé, 02 identité, 03 SECTEURS, 04 expertises** :
  la coupe est passée devant les expertises (demande FT2E, renumérotation suivie). La
  consignation d'A10 cite « le bloc secteurs de l'accueil » et plus un numéro de section.
- **Les légendes des clichés nomment les projets** : le document FT2E
  `correspondance_Site_projet.docx` couvre exactement les 27 clichés des films alors
  tirés. Les deux adossés à des fiches publiées reprennent la légende de leur planche
  (« Abbaye de Sablonceaux » ×2, « EHPAD Aliénor d'Aquitaine » ×2) ; 21 autres sont
  composées dans le même style (« Aurora, 147 logements », « Chaufferie bois CDAIR »…) ;
  « Sous station » et « Réseau existant », génériques au document, restent descriptives.
  ⚠ **17 clichés du corpus restent en légende descriptive** et peuvent sortir à tout
  build — FT2E : « on fixera quand je les aurai » (les correspondances).
- **Le cliché principal de chaque tranche est un lien** vers `/references/?secteur=…`
  filtrée sur le secteur ; les vignettes du film gardent la sélection (au toucher,
  c'est le seul parcours du film). « Lire la fiche » est devenu « En savoir plus »
  (destination inchangée : la page du secteur). Au passage, **Monotechnique compte
  maintenant 2 fiches publiées** : son filtre existe, la réserve de l'annexe B tombe.
- **Les filtres de `/references` sont des vignettes d'images** à l'état
  masqué/dévoilé du carrousel (opacité 0,42 → 1 au survol, au focus et à l'état actif ;
  le voilage ne touche jamais la légende — contraste RGAA). Image = premier cliché du
  corpus, stable ; « Tous » porte la hachure neutre. La page **lit `?secteur=` dans
  l'URL** (mesuré : 8 cartes sur Logements, grille complète sur paramètre inconnu).
  Le libellé « secteur » surplombe la rangée et la vignette fait 130 px :
  8 × 130 + 7 × 16 = 1 152, les huit boutons tiennent sur une ligne.

Rendu contrôlé à chaque pas (captures 390/768/1440), builds verts, liens de la coupe
vérifiés au navigateur. L'annexe B est **remplacée par l'annexe C** ci-dessous.

## Annexe C — prompt de la session suivante (à coller tel quel en session neuve)

````
Session de suite du chantier bloc secteurs - FT2E v3 (fin de legendes, gel du
film, validations).

Contexte. FT2E v3 est un site institutionnel Astro statique (Astro 6, Tailwind 4,
TypeScript strict), deploye en demonstration client sur https://ft2e-v3.vercel.app,
indexation verrouillee par triple securite (robots.txt Disallow, meta noindex,
header X-Robots-Tag) - ne pas y toucher. La source de verite du design est
.claude/rules/tailwind-design-tokens.md (rampe monochrome 197, aucune couleur
d'accent, filets 1 px par opacite, rayon 0, courbe unique, amendements A1-A10).
Le chantier de reduction de dette est EN PAUSE (docs/23-etat-de-l-art.md).

ETAT AU 2026-08-26 SOIR (commits jusqu'a 87476ef, tout deploye et verifie) :
la coupe deployee des secteurs est en position 03 de l'accueil (expertises en
04) ; le film de chaque tranche est TIRE AU BUILD dans le corpus (44 cliches
reels (c) FT2E, filmSecteur() dans src/lib/secteurs.ts) ; le cliche principal
est un lien vers /references/?secteur=... ; le pied dit « En savoir plus » ;
les filtres de /references sont des vignettes d'images (130 px, huit sur une
ligne, etat masque/devoile) et la page lit ?secteur= dans l'URL ; 27 cliches
portent une legende de PROJET issue de correspondance_Site_projet.docx (dont
« Abbaye de Sablonceaux » et « EHPAD Alienor d'Aquitaine », reprises des
planches de leurs fiches) ; la vedette de l'accueil est « Des etudes /
techniques / portees jusqu'a / l'execution », bornee a 5,1 rem SANS
text-balance (mesures dans le commentaire de Hero.astro - ne pas y revenir
a l'estime).

LIRE D'ABORD : docs/superpowers/plans/2026-08-17-chantier-bloc-secteurs.md
(§ 6 : montage et corpus ; § 7 : ajustements du 2026-08-26) ; CLAUDE.md ;
src/components/blocs/CoupeSecteurs.astro et src/pages/references/index.astro.

CE QUE CETTE SESSION FAIT :

1. QUAND FT2E LIVRE LES CORRESPONDANCES RESTANTES (il a dit : « on fixera
   quand je les aurai ») - 17 cliches encore en legende descriptive :
   villa urbaine (Logements) ; ecomusee, tiers-lieu bois, pharmacie, siege
   d'entreprise, bureaux zinc dore (Tertiaire/ERP) ; centre technique, poste
   ferroviaire, site en plaine, atelier agro, chantier naval (Industriel) ;
   videoprotection, borne irve, hydraulique, calorifuge, cameras en facade
   (Monotechnique) ; passerelle (Patrimoine).
   a. Legender ces 17 comme les 27 premiers : legende de la planche si le
      projet a une fiche publiee (lire le titre du planche.json), sinon
      composer dans le meme style, 40 signes au plus (borne Zod).
   b. PUIS GELER LE FILM avec FT2E : soit remplacer filmSecteur() par une
      lecture ordonnee du corpus (film = 4 premiers de la liste, l'ordre
      redevient editorial et Decap le pilote), soit garder le tirage une
      fois tout legende. Documenter le choix dans le meme commit.
2. PASSER NVDA sur l'accueil (la coupe) et une page secteur - exigence RGAA
   du depot, TOUJOURS DUE depuis le montage : tabulation (le focus ouvre une
   tranche et se reporte sur la premiere vignette du film), fleches
   gauche-droite dans le film, compteur aria-live="polite", calques
   aria-hidden muets, lien du cliche principal annonce « Voir les references
   du secteur ... ». Consigner le releve dans le plan (script APPEND).
3. RECUEILLIR LES VALIDATIONS FT2E du § 6 du plan, toujours ouvertes : les
   17 fichiers ecartes (14 perspectives de tiers, 3 fonds de plan), les
   artefacts d'agrandissement IA sur cliches retenus (plaque de mairie,
   panneau, etiquettes), le credit (c) FT2E.
4. DECAP : la connexion echoue en production (HTTP 500 - deux variables OAuth
   Vercel et une callback GitHub manquantes, docs/22-prise-en-main-decap.md
   § 0, trois gestes que seul l'utilisateur peut faire, AJOURNES en
   connaissance de cause). Le rappeler UNE FOIS en ouverture puis le
   respecter ; essayer la collection cliches des que l'OAuth sera pose.

PIEGES VERIFIES, A NE PAS REDECOUVRIR (detail : CLAUDE.md, les rules, et le
§ 8 de l'annexe B ci-dessus, qui reste valable en bloc) : scripts de composant
via astro:page-load + guard dataset.bound ; mesures en CSS de composant,
couleurs en classes litterales ; motifs .gitignore ANCRES ; un build vert ne
prouve pas le rendu (npm run captures -- --route 01-accueil ; Chrome refuse
toute fenetre sous 500 px, meme headless) ; la performance se mesure sur le
DEPLOIEMENT, jamais sur npm run preview, jamais en un tir ; depot PARTAGE
(git ls-remote avant commit, marqueur de build dans le HTML servi apres push ;
la CLI Vercel repond Not authorized, c'est le push qui deploie) ; les
insecables sont normalisees par les outils d'edition (docs : script Python en
mode APPEND, chr(160) construit, assertion apres coup ; source .astro :
echappement JavaScript u00a0, jamais le caractere) ; pas de commentaire JSX
entre la parenthese d'un .map et son element ; min-width: 0 sur les flex
porteurs d'images ; TOUTE COTE DE LA VEDETTE SE MESURE AU NAVIGATEUR avant
d'etre posee - deux estimations ont casse des lignes le 2026-08-26.

Recette de fin de session : npm run typecheck (0 erreur), npm run build
(46 pages), python scripts/controle-liens-internes.py (0 lien mort), controle
du RENDU des pages touchees aux largeurs utiles, Lighthouse mobile sur le
DEPLOIEMENT si la structure a change (accessibilite : 96 attendu sur
l'accueil, violation unique color-contrast du complement text-clair
aria-hidden - motif de l'exception D1 ; toute violation NOUVELLE est un
blocage), et consignation dans
docs/superpowers/plans/2026-08-17-chantier-bloc-secteurs.md par script append.

Portees de commit : content, feat(accueil), feat(references), a11y, docs selon
les points. Tout changement de schema Zod va dans le MEME commit que
public/admin/config.yml.

Termine par le prompt de lancement de la session suivante, en annexe du plan
de ce chantier et reproduit integralement dans ton message final - la regle de
continuite est dans CLAUDE.md parce qu'elle a ete manquee deux fois.
````


## 8. Session du 2026-08-26 soir — vedette, rail de filtres, taxonomie, cliché du hero

Neuf commits (`6b96cbf` à `e69a2db`), tous poussés et vérifiés par marqueur dans le
HTML servi. L'annexe C n'a PAS été jouée en entrée de cette session (elle reste
ci-dessus pour l'historique) : la session a suivi des directives FT2E en direct.

- **Vedette recomposée en deux rangs** (`6b96cbf`) : titre « Ingénierie / fluides
  et thermique / du bâtiment » en trois lignes explicites, borne haute REMESURÉE à
  4,5 rem (« FLUIDES ET THERMIQUE » : 1 093 px à 72 px pour 1 152 de boîte) ;
  second rang nouveau « De l'étude jusqu'à l'exécution », prop `sousVedette` de
  `Hero.astro`, dessin `.type-intitule` en encre, 0,39x la vedette. Cotes dans le
  commentaire du composant.
- **Filtres de `/references` en RAIL vertical** (`754d563`) : au-dessus de 1 024 px
  les filtres occupent la première colonne du rythme (216 px à 1 024, 276 dès
  1 248), grille à trois colonnes à droite — la vignette reste servie à 274 px, la
  mesure d'A9 est préservée. Légende au cartouche de réserve (A8) sur l'image au
  rail, sous l'image en rangée repliée (< 1 024 : 4 puis 2 tuiles par ligne).
  Les deux fichiers normatifs qui prescrivaient `lg:grid-cols-4` mis à jour dans
  le même commit.
- **Tuile « Tous » en mini-coupe** (`dc91fe6`) : sept tranches verticales, le
  premier cliché de chaque secteur en duotone — l'écho de la coupe de l'accueil.
  Le monogramme a été écarté (voilé à 0,42, il se lirait comme un tampon délavé).
- **Taxonomie des secteurs** (`8250827`, BREAKING CHANGE consigné) : « Industriel
  et commercial » devient « Industriel » ; « Monotechnique » devient
  « Monotechnique — Audit et EXE » (graphie arbitrée : tiret cadratin, Audit en
  bas de casse) ; « Coordination SSI » passe en position 5, Monotechnique en 6.
  La place des Chênes Verts (commerces) migre dans Tertiaire / ERP (8 fiches ;
  Industriel : 2). Zod + Decap dans le même commit ; slugs et répertoires
  d'images INCHANGÉS (l'URL n'est pas l'intitulé) ; le mot « monotechnique » en
  prose commune non touché.
- **Cliché du hero** (`050f0cc`, `957639a`, `e69a2db`) : l'appui de la fiche
  vedette (plan posé blanc, « flottait dans le vide » — retour FT2E) est remplacé
  par « Aurora, 147 logements » du corpus secteurs — duotone, équerres, cartouche,
  3:2, colonne 7/12, lien vers `/references/?secteur=Logements`. Légende/alt/crédit
  relus depuis la collection secteurs (échec bruyant si le cliché quitte le
  corpus). Partis avec l'appui : `fs.readFileSync`, le plafond `.appui-hero`, la
  carte-lien (`en_avant` garde l'ordonnancement de la sélection).
  ⚠ ARBITRAGE LCP (2026-08-27) : affiché au téléphone, le cliché devenait
  l'élément LCP mobile — 7 tirs entre 1 823 et 2 013 ms pour un budget de 1 800,
  poste dominant le délai de rendu (1 235 ms), le plafonnement de densité tenté
  en `957639a` n'a RIEN changé (mesuré). Le média est donc BUREAU SEUL (masqué
  sous `lg` par l'enveloppe du slot) ; remesure : 1 668-1 804 ms, l'état « au
  seuil » documenté est retrouvé. Réserve : l'image masquée est tout de même
  téléchargée (52 Ko) — sans effet mesurable ; une direction artistique par
  `<source media>` serait le levier si l'on voulait aussi ces octets.
- **Incident de dépôt réglé** (`c9ce606` hook, `e8d359c` correction) : le hook
  Stop a commité et poussé seul `lh-refs.json` (7 091 lignes, rapport Lighthouse
  laissé sur le disque). Retiré au commit suivant. Leçon : les artefacts
  d'instrument se suppriment du disque sitôt lus.
- `CLAUDE.md` perd son point périmé « Monotechnique sans référence publiée »
  (2 fiches publiées).

Recette jouée à chaque pas : typecheck 0 erreur, build 46 pages, 0 lien mort,
rendu contrôlé aux largeurs utiles (sonde iframe pour les téléphones),
Lighthouse accessibilité 100 sur `/references/` après le rail, LCP mobile sur le
déploiement en tirs multiples. L'annexe C — jamais jouée — est **remplacée par
l'annexe D** ci-dessous, qui intègre le nouveau chantier MOTION demandé par FT2E.

## Annexe D — prompt de la session suivante (à coller tel quel en session neuve)

````
Session de suite - FT2E v3 : chantier MOTION (infléchissement de charte),
fin de légendes du bloc secteurs, NVDA, validations.

Contexte. FT2E v3 est un site institutionnel Astro statique (Astro 6,
Tailwind 4, TypeScript strict), déployé en démonstration client sur
https://ft2e-v3.vercel.app, indexation verrouillée par triple sécurité
(robots.txt Disallow, meta noindex, header X-Robots-Tag) - ne pas y toucher.
La source de vérité du design est .claude/rules/tailwind-design-tokens.md
(rampe monochrome 197, aucune couleur d'accent, filets 1 px par opacité,
rayon 0, courbe unique, amendements A1-A10). Le chantier de réduction de
dette est EN PAUSE (docs/23-etat-de-l-art.md).

ÉTAT AU 2026-08-27 MATIN (commits jusqu'à e69a2db, tout déployé et vérifié) :
la vedette de l'accueil est « Ingénierie / fluides et thermique / du
bâtiment » en trois lignes, bornée à 4,5 rem, avec un second rang
« De l'étude jusqu'à l'exécution » (.type-intitule encre - cotes mesurées
dans le commentaire de Hero.astro, ne pas y revenir à l'estime) ; le média
du hero est le cliché « Aurora, 147 logements » (duotone + équerres +
cartouche, lien vers /references/?secteur=Logements), BUREAU SEUL - arbitrage
LCP du 2026-08-27, 7 tirs au-dessus du budget quand il s'affichait au
téléphone, consigné dans Hero.astro ; les filtres de /references sont un
RAIL vertical à gauche au-dessus de 1 024 px (216/276 px, cartouche de
réserve sur l'image) et une rangée repliée en dessous (légende sous
l'image) - la grille est à 3 colonnes, vignette toujours servie à 274 px ;
la tuile « Tous » est une mini-coupe des sept secteurs ; les secteurs sont
renommés et réordonnés (« Industriel », « Coordination SSI » en 5,
« Monotechnique - Audit et EXE » en 6 - graphie : tiret cadratin, Audit en
bas de casse) et la place des Chênes Verts est dans Tertiaire / ERP
(8 fiches ; Industriel 2) ; la coupe des secteurs reste en position 03 de
l'accueil, film TIRÉ AU BUILD (44 clichés réels (c) FT2E).

LIRE D'ABORD : docs/superpowers/plans/2026-08-17-chantier-bloc-secteurs.md
(§ 6-7 : montage et ajustements ; § 8 : session du 2026-08-26 soir) ;
CLAUDE.md ; .claude/rules/tailwind-design-tokens.md § Interactions & motion ;
src/styles/motion.css ; src/components/blocs/Hero.astro, CoupeSecteurs.astro
et src/pages/references/index.astro.

CE QUE CETTE SESSION FAIT :

1. CHANTIER MOTION - NOUVEAU, et c'est un INFLÉCHISSEMENT DE CHARTE (demande
   FT2E du 2026-08-27 : « le style est déjà très aride, des effets plus
   marqués apporteraient un peu de dynamisme »). La charte actuelle prescrit
   QUATRE mouvements sur une courbe unique et interdit tout le reste
   (compteurs, parallax, hover lift, déplacement au survol - seule exception
   bornée : A10, l'ouverture de tranche de la coupe). Un effet plus marqué ne
   se glisse donc pas : il S'ARBITRE, au précédent d'A10.
   a. OUVRIR PAR UN CADRAGE (brainstorming avant tout code) : inventorier les
      quatre mouvements existants et leurs emplois, puis proposer 2-3 pistes
      d'intensification BORNÉES - par exemple : révélations de plans plus
      amples ou séquencées (stagger), transitions de pages enrichies (View
      Transitions), micro-mouvements d'entrée sur les vignettes/cartes, survols
      plus expressifs sur les pièces signature (coupe, rail, hero). Chaque
      piste dit : où, quelle propriété bouge, durée/courbe, et ce qu'elle NE
      touche pas.
   b. FAIRE VALIDER LES PISTES PAR FT2E (maquette ou démo sur une page avant
      généralisation).
   c. CONSIGNER l'arbitrage en amendement(s) A11+ dans
      .claude/rules/tailwind-design-tokens.md (registre des amendements),
      comme A9 et A10 : ce qui s'ouvre, ses bornes, ce qui reste interdit.
   d. IMPLÉMENTER dans src/styles/motion.css + composants concernés, avec :
      prefers-reduced-motion INTÉGRAL (tout posé d'emblée), fallback sans JS,
      aucune régression TBT/CLS (budget : TBT < 200 ms, CLS < 0,05, mesuré
      sur le DÉPLOIEMENT en tirs multiples), et le pattern astro:page-load +
      guard dataset.bound pour tout script.
   ⚠ Le LCP accueil est AU seuil (1 668-1 804 ms pour 1 800) : toute
   animation d'entrée qui retarderait le premier rendu du hero est à
   proscrire ou à mesurer avant/après.

2. QUAND FT2E LIVRE LES CORRESPONDANCES RESTANTES (« on fixera quand je les
   aurai ») - 17 clichés encore en légende descriptive : villa urbaine
   (Logements) ; écomusée, tiers-lieu bois, pharmacie, siège d'entreprise,
   bureaux zinc doré (Tertiaire/ERP) ; centre technique, poste ferroviaire,
   site en plaine, atelier agro, chantier naval (Industriel) ;
   vidéoprotection, borne IRVE, hydraulique, calorifuge, caméras en façade
   (Monotechnique - Audit et EXE) ; passerelle (Patrimoine).
   a. Légender ces 17 comme les 27 premiers : légende de la planche si le
      projet a une fiche publiée (lire le titre du planche.json), sinon
      composer dans le même style, 40 signes au plus (borne Zod).
   b. PUIS GELER LE FILM avec FT2E : soit remplacer filmSecteur() par une
      lecture ordonnée du corpus (film = 4 premiers, l'ordre redevient
      éditorial et Decap le pilote), soit garder le tirage une fois tout
      légendé. Documenter le choix dans le même commit.

3. PASSER NVDA - exigence RGAA du dépôt, TOUJOURS DUE depuis le montage, et
   le périmètre a GRANDI : l'accueil (la coupe : tabulation, flèches dans le
   film, compteur aria-live, calques aria-hidden muets, lien du cliché
   principal ; et le nouveau média du hero : lien « Voir les références du
   secteur Logements », cartouche aria-hidden), une page secteur, et le RAIL
   de /references (boutons aria-pressed, une seule légende par bouton dans
   l'arbre d'accessibilité - lg:hidden / hidden lg:inline-flex). Consigner le
   relevé dans le plan (script APPEND).

4. RECUEILLIR LES VALIDATIONS FT2E, liste augmentée : celles du § 6 du plan
   (17 fichiers écartés, artefacts d'agrandissement IA, crédit (c) FT2E) PLUS
   celles de la session du 2026-08-26 soir : la vedette à deux rangs, le rail
   et la mini-coupe « Tous », les nouveaux intitulés de secteurs en
   situation, le cliché Aurora au hero (et son absence assumée au téléphone).

5. DECAP : la connexion échoue en production (HTTP 500 - deux variables OAuth
   Vercel et une callback GitHub manquantes, docs/22-prise-en-main-decap.md
   § 0, trois gestes que seul l'utilisateur peut faire, AJOURNÉS en
   connaissance de cause). Le rappeler UNE FOIS en ouverture puis le
   respecter. ⚠ Le schéma des secteurs a changé (BREAKING du commit 8250827) :
   tout brouillon Decap antérieur au 2026-08-26 devra reprendre un secteur de
   la nouvelle énumération.

PIÈGES VÉRIFIÉS, À NE PAS REDÉCOUVRIR (détail : CLAUDE.md et les rules) :
scripts de composant via astro:page-load + guard dataset.bound ; mesures en
CSS de composant, couleurs en classes littérales ; motifs .gitignore ANCRÉS ;
un build vert ne prouve pas le rendu (npm run captures -- --route 01-accueil ;
Chrome refuse toute fenêtre sous 500 px, même headless - sonde iframe, sa
barre mange 15 px) ; la performance se mesure sur le DÉPLOIEMENT, jamais sur
npm run preview, JAMAIS en un tir ; dépôt PARTAGÉ (git ls-remote avant
commit, marqueur de build dans le HTML servi après push ; la CLI Vercel
répond Not authorized, c'est le push qui déploie) ; le hook Stop commite et
pousse SEUL ce qui traîne sur le disque - supprimer les artefacts
d'instrument sitôt lus (incident lh-refs.json du 2026-08-26) ; les insécables
sont normalisées par les outils d'édition (docs : script Python en mode
APPEND, chr(160) construit, assertion après coup ; source .astro :
échappement JavaScript u00a0, jamais le caractère) ; pas de commentaire JSX
entre la parenthèse d'une expression et son élément (a cassé le build le
2026-08-26 dans Hero.astro) ; min-width: 0 sur les flex porteurs d'images ;
TOUTE COTE DE LA VEDETTE SE MESURE AU NAVIGATEUR avant d'être posée ;
display:none n'empêche PAS le téléchargement d'une image eager.

Recette de fin de session : npm run typecheck (0 erreur), npm run build
(46 pages), python scripts/controle-liens-internes.py (0 lien mort), contrôle
du RENDU des pages touchées aux largeurs utiles, Lighthouse mobile sur le
DÉPLOIEMENT si la structure a changé (accessibilité : 96 attendu sur
l'accueil, violation unique color-contrast du complément text-clair
aria-hidden - motif de l'exception D1 ; toute violation NOUVELLE est un
blocage ; LCP accueil < 1 800 en tirs multiples), et consignation dans
docs/superpowers/plans/2026-08-17-chantier-bloc-secteurs.md par script
append. Si le chantier motion prend de l'ampleur, lui ouvrir son PROPRE plan
docs/superpowers/plans/2026-08-27-chantier-motion.md et y consigner à partir
de là.

Portées de commit : design-system (motion), content, feat(accueil),
feat(references), a11y, docs selon les points. Tout changement de schéma Zod
va dans le MÊME commit que public/admin/config.yml. Tout amendement de charte
va dans .claude/rules/tailwind-design-tokens.md dans le même commit que son
implémentation.

Termine par le prompt de lancement de la session suivante, en annexe du plan
du chantier concerné et reproduit intégralement dans ton message final - la
règle de continuité est dans CLAUDE.md parce qu'elle a été manquée deux fois.
````


## 9. Session du 2026-08-27 — cadrage motion, relevé d'arbre d'accessibilité

- **CHANTIER MOTION ouvert dans son propre plan** :
  `docs/superpowers/plans/2026-08-27-chantier-motion.md` — inventaire des
  mouvements (fait saillant : `TraceFlux` orphelin depuis `7562544`, retiré
  sur demande FT2E), contraintes, quatre pistes bornées (0 : filet de flux à
  revalider ; 1 : cascade A11 ; 2 : survol des photographies, variantes a/b,
  A12 ; 3 : View Transitions enrichies A13), et maquette d'arbitrage
  `docs/maquettes/ft2e-motion-pistes.html` (démonstrations jouables,
  contrôlées au navigateur). **Aucune implémentation sur le site : la porte
  est l'arbitrage FT2E.**
- **Correspondances des 17 clichés : non livrées** — le point 2 du prompt
  reste intact pour la suite.
- **NVDA : toujours dû (passage humain).** En préparation, relevé de l'ARBRE
  D'ACCESSIBILITÉ sur le déploiement (Playwright, 2026-08-27) :
  - accueil / coupe : groupe « Film du secteur Logements » ; boutons
    « Cliché N sur 4 — [légende] » avec état `pressed` ; tranches 02-07
    nommées « Secteur NN — [intitulé], quatre clichés » ; compteur de film
    présent dans l'arbre ; hero : lien « Voir les références du secteur
    Logements », alt descriptif du cliché Aurora ;
  - `/references/` : groupe « Filtres par secteur », UNE légende par bouton
    (le doublon `lg:hidden` / `lg:inline-flex` ne fuit pas dans l'arbre),
    `pressed` sur le filtre actif ; cartes-liens : vignette SVG
    `aria-hidden` à la source, nom du lien = titre court + commune +
    chronologie. ⚠ Le dump Playwright affiche ces liens « sans nom » : c'est
    une élision de l'outil, vérifiée au DOM (`aria-hidden` posé, nom
    calculable) — ne pas conclure à un défaut sur le seul dump ;
  - `/secteurs/logements/` : `h1` unique, hiérarchie sans saut, alt
    descriptifs, maillage interne réel (expertises + fiches).
  - Reste À L'ÉCOUTE (NVDA seul) : l'annonce du compteur `aria-live` au fil
    du film, l'ordre de lecture de la coupe au clavier, la verbosité des
    noms de boutons du film, les FAQ des pages secteurs.
- **Validations FT2E** : liste consolidée remise à l'utilisateur — § 6 du
  plan (17 fichiers écartés, artefacts d'agrandissement IA, crédit
  © FT2E) + session du 26 soir (vedette à deux rangs, rail et mini-coupe
  « Tous », intitulés de secteurs, cliché Aurora au hero et son absence au
  téléphone) + l'arbitrage motion lui-même.
- **Decap** : rappelé une fois en ouverture, ajourné en connaissance de
  cause (blocage OAuth hors dépôt, `docs/22-prise-en-main-decap.md` § 0).

**Le prompt de la session suivante vit en annexe A du plan motion** et
remplace l'annexe D ci-dessus.
