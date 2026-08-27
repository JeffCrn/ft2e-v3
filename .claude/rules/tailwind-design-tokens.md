# Tailwind & Design Tokens — charte v3 « Ingénierie de l'invisible » (plans et profondeur)

**Scope** : tout fichier utilisant Tailwind (`.astro`, `.tsx`, `.html`).

**Référence** : « FT2E Charte graphique » document 10 · **révision 2.1** (08.2026), bundle `branding-v3-bis/` — remplace la révision 2 (`branding-v3/`) et la révision 1 (`branding-v2/`). La 2.1 conserve la structure de la 2 et corrige **huit prescriptions** consignées à son § 16 (registre des amendements) : elles sont reportées ci-dessous sous les repères A1 à A8. **A9 et A10 s'y ajoutent, qui ne viennent pas du PDF** : ce sont des amendements d'application, arbitrés ici (A9 le 2026-08-15, index des références en grille de cartes ; A10 le 2026-08-25, ouverture de tranche de la coupe des secteurs). Spec d'application : `docs/superpowers/specs/2026-08-06-ft2e-charte-v3-plans-profondeur.md`.

**Autorité** : en cas de contradiction entre la charte et un support existant, la charte prévaut. En cas de contradiction interne à la charte, **la mesure prévaut sur la règle**.

## Principe directeur

**Une teinte unique (197°), cinq valeurs teintées, deux neutres, aucune couleur d'accent — et la profondeur remplace l'ornement.** Le relief vient des plans : une planche posée, une planche qui déborde, une ligne encrée — trois rangs d'ombre à l'encre translucide, aucun autre effet. Le rang d'un filet est porté par son **opacité d'encre** (22 / 16 / 12 %), plus jamais par son épaisseur ; la hiérarchie typographique passe par la **graisse** (Archivo 300 / 600 / 700) et la **chasse** (wdth 62–125).

**Aucune valeur hard-codée** hors de `src/styles/global.css` (bloc `@theme` + `@layer components`). Pas de `tailwind.config.ts`.

## Couleurs — la rampe 197° (inchangée depuis la révision 1)

| Token | Hex | Nom charte | Usage exclusif |
|---|---|---|---|
| `profond` | `#001718` | Profond | **réserve — 1/5 max, une apparition par écran** : ligne encrée (relevés), duotone des images, couverture, puce de section ; texte vedette sur papier (17,5:1) |
| `encre` | `#00393a` | Encre | toute la lecture : titres, corps, aplat du bouton principal, chip actif — et l'encre translucide des filets et des ombres |
| `pivot` | `#336667` | Pivot | données, dates, mentions, chapô, chiffres de relevé en retrait (A1), anneau de focus en polarité claire — **jamais en texte NI en filet porteur sur profond** (2,85:1, A3 : aplat décoratif seulement). *La révision 2 nommait cette valeur « vert FT2E » ; le nom laissait entendre un accent de marque, que la décision 2 refuse.* |
| `clair` | `#99cccd` | Clair | corps, étiquettes et **anneau de focus** sur fond profond (10,45:1) ; **sur papier : filets, aplats et complément des titres de section uniquement** (1,67:1 — décor `aria-hidden` obligatoire, A2) |
| `voile` | `#e1f4f4` | Voile | pôle clair du duotone ; titres, chiffres et équerres **sur réserve profonde uniquement** — jamais sur papier ni calcaire |
| `papier` | `#f7f9fa` | Papier (neutre) | la planche de page (max 1440 px) et les plans posés ; fond des cellules au survol |
| `calcaire` | `#edf0f2` | Calcaire (neutre) | le fond sous la planche de page ; cellules de liste au repos, blocs de rappel, en-têtes de tableau — **jamais le voile sur le calcaire** (iso-clairs) |

### Filets — trois rangs portés par l'opacité (1 px)

| Token | Valeur | Emploi |
|---|---|---|
| `filet-1` | `#00393a38` | rang 1 : porteur, contour appuyé, bordure de cellule, statut livré — encre 22 % |
| `filet-2` | `#00393a29` | rang 2 : bordure de plan, séparateur de colonnes, statut en cours — encre 16 % |
| `filet-3` | `#00393a1f` | rang 3 : indication, note, statut archive — encre 12 % |
| `filet-chip` | `#00393a47` | étiquette de mission, chip de filtre, bouton filaire — encre 28 % |
| `filet-clair-1` | `#99cccd59` | filet porteur **en polarité profonde** — clair 35 % (le pivot y est interdit) |
| `filet-clair-2` | `#99cccd2e` | filet de séparation en polarité profonde — clair 18 % |

**L'épaisseur ne porte pas le rang : tous les filets font 1 px.** Elle ne sert qu'aux **états** (§ 11 : erreur = 2 px). Trois exceptions dessinées, à valeur pleine : le filet clair 3 px du bouton principal, de la ligne encrée et du bandeau de succès, et le filet bas 1 px encre plein de la page courante en navigation. `line`/`line-strong` ont été **supprimés** (§ 17, hygiène du dépôt).

### Les cinq règles

1. **Une seule teinte** : aucune valeur hors rampe 197° (chroma ≤ 0,055), y compris héritée. **Hygiène du dépôt (§ 17)** : les anciens jetons (`copper`, `marine`, `slate`, `mist`, `apple-blue`, `line`…) ont été **supprimés de `global.css`**, pas repointés — un jeton nommé d'après une identité antérieure survivrait à la charte. Aucune valeur hexadécimale ne s'écrit en dur dans un composant : elle passe par un jeton, ou elle n'existe pas. **Et elle passe par une CLASSE littérale** (`stroke-encre`, `fill-pivot`), jamais par `var(--color-…)` écrit dans un attribut SVG : Tailwind v4 élague les variables de thème qu'aucune classe n'emploie, et un `var()` en attribut échappe au scan — la couleur tombe sans un mot du build (mesuré le 2026-08-16 ; détail dans `.claude/rules/astro-conventions.md`). Les compositeurs de planches font exception et gardent leur propre table `JETON` dans `scripts/planches/_tronc.py` : une planche est lue hors du site (PNG, impression, `og:image`) et ne peut pas résoudre `var()`. **Une révision de charte s'y répercute donc aussi**, et les 23 dossiers se régénèrent. *Exception mesurée : `papier` et `calcaire`, à chroma 0,003 et 0,004, ne se régénèrent pas depuis l'axe — ils se saisissent en dur dans le bloc `@theme`.*
2. **Aucune couleur d'accent** : chaque valeur du système se lit ; deux valeurs par composition, trois au maximum.
3. **L'état par défaut est clair** : une seule réserve profonde par écran (`bg-profond` / `.plan-encre`), 1/5 de la surface max — une page encrée sur quarante.
4. **La profondeur remplace l'ornement** : trois rangs d'ombre à l'encre translucide (`--shadow-plan-1/2/3`) plus l'ombre de page (`--shadow-page`) — aucun autre effet, aucun dégradé coloré, aucune lueur, aucune ombre teintée hors encre.
5. **Une alerte est un signe, pas une couleur** : filet doublé + mention explicite (`--color-success`/`--color-error` repointés sur l'encre).

Garde-fous de contraste : jamais de vert FT2E en texte sur profond ; jamais de voile sur calcaire ni de calcaire sur voile ; le clair sur papier n'est jamais porteur de sens.

## Échelle de titrage — sept rangs (révision 2.1)

Sept rangs, pas huit. Chacun se distingue du précédent par **au moins deux paramètres** (corps et chasse, ou chasse et graisse), de sorte qu'aucune confusion ne soit possible à la lecture rapide.

| Rang | Classe | Corps | Chasse | Graisse | Interl. | Casse — emploi |
|---|---|---|---|---|---|---|
| Vedette | `.type-display` | 104 (clamp 3–6,5 rem) | 125 | 700 | 0,92 | capitales — **accueil uniquement, une par page** |
| Titre d'écran | `.type-ecran` | 62 (clamp 2,25–3,875 rem) | 100 | 600 | 1,02 | **casse normale, jamais capitales** — h1 des pages internes (`HeroPage`) |
| Section | `.type-section` (= `.type-h2`) | 26 | 118 | 700 | 1,10 | capitales — puce 7 px + mot porteur encre + « /complément » clair `aria-hidden` |
| Intitulé | `.type-intitule` | 17–20 | 112 | 600 | 1,15 | capitales — carte, cellule, ligne de tableau |
| Corps | (défaut `body`) | 15–17 | 100 | **400** | 1,60 | 52 à 68 signes par ligne — **amendement A7** |
| Chapô | `.type-chapo` | 19–22 | 100 | **300** | 1,50 | casse normale, **en pivot**, trois lignes au plus — rang nouveau de la 2.1, seul emploi de la graisse 300 |
| Étiquette | `.mono-label` | 10–11 | mono | 500 | 1,20 | capitales, 0,14 em — jamais plus grand, jamais en texte courant |
| Relevé | `.releve-chiffre` | 96 (clamp 3,5–5,75 rem) | 118 | 700 | 1,00 | chiffres tabulaires obligatoires |

**Quatre graisses, pas trois** (amendement A7) : 300 (chapô), 400 (corps), 600 (titre d'écran, intitulé), 700 (vedette, section, relevé). La révision 2 composait le corps en 300 ; la 2.1 le porte à 400 et réserve la 300 au chapô.

- **IBM Plex Mono** (400/500/600) : tout ce qui se **mesure**, se **référence**, se **signale** — étiquettes, cotes, surfaces, dates, numéros d'affaire, légendes d'image, navigation. Toujours en capitales, 0,14 em sous 12 px. **Jamais en texte courant** ; l'Archivo jamais en cote ni référence d'affaire.
- **Substitution** (gabarit imposé, courrier bureautique) : **Arial** en normale ou grasse, sans variation de chasse ; **Consolas** ou **Menlo** pour le mono. Aucune autre, et **aucun serif**.
- `.type-annexe` (chasse 72) a été **supprimé** : la 2.1 ne compte que sept rangs, et la hiérarchie passe par la graisse et l'opacité.

## Les amendements — huit de la charte (§ 16), deux d'application (A9, A10)

| № | Objet | Révision 2 | Révision 2.1 — ce qui s'applique |
|---|---|---|---|
| A1 | Retrait des chiffres | chiffres secondaires en encre 13 % | **au pivot** (`.releve-retrait`) — l'encre 13 % donne `#D7E0E1`, soit 1,27 sur papier |
| A2 | Complément de titre | second mot en clair | **`aria-hidden="true"` obligatoire**, aucune information exclusive (1,67) |
| A3 | Pivot sur profond | 3,67, toléré en filet | **2,85** — interdit en texte **et en filet porteur**, aplat décoratif seulement |
| A4 | Focus visible | non traité | **pivot en polarité claire, clair en polarité profonde** |
| A5 | États de formulaire | non traité | épaisseur du filet + marque de forme + mot (`.champ`, `.message-erreur`, `.bandeau-succes`) |
| A6 | Liens en texte | non traité | **encre + soulignement 1 px, 2 px au survol, aucun changement de couleur** (`.lien-texte`) |
| A7 | Graisse du corps | corps en 300, trois graisses | **corps en 400, chapô en 300, quatre graisses** |
| A8 | Légende sur image | « dans la valeur opposée au fond » | **cartouche de réserve** (`.cartouche-legende`, voile sur profond, 16,24) — inapplicable sur photographie. Équerres toujours en voile |

### A9 — l'index des références est une grille de cartes (2026-08-15)

**A9 n'est pas au § 16 de la charte imprimée** : c'est un amendement d'**application**,
arbitré le 2026-08-15 à la clôture du chantier des planches. Il est consigné ici parce que
ce fichier fait foi sur le design ; ne pas le chercher dans le PDF de FT2E.

| № | Objet | Révision 2.1 | Ce qui s'applique |
|---|---|---|---|
| A9 | Index `/references` | « liste tabulaire, **pas** une grille de cartes » | **grille de cartes** au gabarit commun du site (`CarteProjet`) — la prescription visait un objet disparu |

La règle de la 2.1 réduisait la vignette à une pastille de 56 px **parce que la vignette
était alors un extrait de plan au 1/50** : illisible à toute taille, autant n'en donner
qu'une texture. Le chantier des planches a remplacé cet extrait par un **dessin composé
pour être lu à 274–296 px**, et l'argument est tombé avec son objet. La charte tranche
elle-même ce genre de conflit — *la mesure prévaut sur la règle* :

| | Ligne de tableau (vignette agrandie) | Grille de cartes |
|---|---|---|
| Vignette servie à 1440 px | 220 px — échelle 0,73 | **274 px — échelle 0,91** |
| Hauteur pour 23 fiches | 4 040 px | **1 904 px** |

Un gain sur les deux axes, pas un compromis. Mesures relevées au navigateur.

**Le rang de statut n'existe plus — et ce n'est pas la grille qui l'a supprimé.** Il a
d'abord été transposé en carte, encodé trois fois (le mot au pied, la graisse de
l'intitulé, l'opacité du filet gauche). Puis, le même jour, la chronologie a cessé
d'afficher « en cours » : **le site annonce une livraison sur toutes les fiches**
(`MILLESIME_LIVRAISON_ANNONCE`, voir la § « La chronologie » de `CLAUDE.md`). Le mot
portait le sens ; sans lui, la graisse et l'opacité ne renvoyaient plus à aucune
information publiée.

C'est la règle générale, et elle vaut au-delà de ce cas : **un signe graphique se retire
avec ce qu'il signifiait.** Le garder « au cas où » laisse une inégalité typographique
d'une carte à l'autre, que le visiteur lit comme une irrégularité de fabrication et non
comme un signal. `rangStatut()` a donc été supprimé de `src/lib/projets.ts`, la prop
`rang` de `CarteProjet` avec lui, et la ligne de légende qui donnait la clé.

Si le statut redevient un jour une information publiée, la règle à réappliquer est celle
qui a présidé ici : **le mot porte, le reste double** — jamais l'inverse, et jamais la
seule couleur (RGAA 3.2). Mesuré au rendu, 22 % contre 16 % d'encre sur un filet de 1 px
ne se départagent pas à l'œil à travers une gouttière ; en nomenclature les lignes étaient
contiguës et le filet pouvait porter seul, en grille non.

### A10 — l'ouverture de tranche de la coupe des secteurs (2026-08-25)

**A10 est, comme A9, un amendement d'application** : arbitré le 2026-08-25 à l'ouverture
du chantier du bloc secteurs de l'accueil, consigné ici parce que ce fichier fait foi sur
le design. Ne pas le chercher dans le PDF de FT2E.

| № | Objet | Révision 2.1 | Ce qui s'applique |
|---|---|---|---|
| A10 | Survol de la coupe des secteurs | « le survol est une bascule de fond, **jamais un déplacement** » | **l'ouverture d'une tranche au survol déplace ses voisines** — accepté pour cette seule pièce, borné |

Le mécanisme même de la coupe (`CoupeSecteurs.astro`, bloc secteurs de l'accueil) est que la tranche
pointée s'ouvre et que ses voisines cèdent la largeur : l'écart n'est pas réductible, il
a donc été arbitré plutôt que contourné. Il est **borné, et les bornes font partie de
l'amendement** :

- **une seule propriété bouge** — la largeur des tranches, sur la durée du survol de
  cellule (300 ms) et la courbe unique ; rien d'autre ne se déplace dans le bloc, la
  promotion d'un cliché est un fondu d'opacité dans un cadre fixe ;
- **un délai d'intention de 120 ms** précède l'ouverture au pointeur — mesuré au montage :
  une traversée vive de la coupe (23 ms par tranche) passe de 6 ouvertures involontaires
  sans délai à 0 au vol, la seule ouverture restante étant le point d'arrêt du pointeur,
  qui est une intention ; un arrêt de 200 ms ouvre. Le focus et le toucher ouvrent sans
  délai ;
- **la portée est cette pièce, et elle seule.** A10 n'est pas une licence : tout autre
  déplacement au survol reste interdit, et un composant qui croirait pouvoir s'en
  réclamer devra passer par le même arbitrage.

### A11 — la révélation ample et séquencée (2026-08-27)

**A11 est, comme A9 et A10, un amendement d'application** — le premier du chantier
motion, arbitré par FT2E le 2026-08-27 (« le style est déjà très aride, des effets
plus marqués apporteraient un peu de dynamisme »). Ne pas le chercher dans le PDF.

| № | Objet | Révision 2.1 | Ce qui s'applique |
|---|---|---|---|
| A11 | Révélation de plan | 760 ms, 22 px, un bloc d'un seul tenant | **1000 ms, 28 px — le module de la trame** ; et les grilles de cartes se révèlent **en cascade**, 80 ms par rang plafonné au sixième |

Les bornes font partie de l'amendement : mêmes propriétés (opacité et translation —
composited seulement, jamais de layout à l'entrée), même courbe, une seule fois par
élément ; la traîne de la cascade est plafonnée à 400 ms quelle que soit la taille de
la grille (23 cartes sur `/references` comme 4 à l'accueil) ; et **tout ce qui est
visible au chargement reste posé d'emblée** (`plan-immediat`) — la protection du LCP
prime sur l'effet, sans exception. Implantation : `motion.css` (les rangs sont du
`:nth-child` pur, aucun attribut par carte), `initPlans` (`BaseLayout`), conteneurs
`data-plan-groupe` (grille 05 de l'accueil, grille de `/references`,
`ProjetsSimilaires`).

### A12 — le voile des photographies-liens (2026-08-27)

Deuxième amendement du chantier motion (arbitrage FT2E : piste 2, **variante a** —
la variante b, micro-échelle dans le cadre, a été présentée et n'a pas été retenue).

| № | Objet | Révision 2.1 | Ce qui s'applique |
|---|---|---|---|
| A12 | Survol d'un cliché-lien | le survol est une bascule de fond | **un voile d'encre à 14 % couvre la photographie au repos et se lève au survol et au focus** (300 ms, opacité seule) |

Les bornes : la portée est la **photographie qui sert de lien** — le cliché du hero
de l'accueil et le cliché principal de la coupe des secteurs (`.lien-cliche` +
`.voile-cliche`, recette dans `global.css`) ; **jamais un dessin de planche** (la
sur-échelle comme le voilage d'un dessin sont interdits — ses filets de 1 px et son
mono sont calibrés pour être lus tels quels) ; le voile passe sous les équerres et
sous le cartouche de réserve, qui restent pleinement lisibles aux deux états ; les
vignettes du rail de `/references` et du film de la coupe gardent leur **voilage
d'état** (0,42 — il dit la sélection, pas le survol) et ne reçoivent pas ce voile en
plus. Aucun déplacement : c'est une bascule d'opacité, dans l'esprit de la règle
qu'elle infléchit.

**Implantation de la légende et des équerres (§ 13)** — la charte veut la légende **en bas à gauche** *et* les équerres intactes (« repère de tirage, jamais un encadrement ») : les deux ne peuvent pas se disputer l'angle. La géométrie tranche, et elle est **dérivée**, jamais réglée à l'œil. Les jetons `--equerre-cote` (18 px) et `--equerre-retrait` (5 px) donnent `--equerre-gouttiere` (28 px), dont découlent à la fois les quatre équerres de `CoinsCuivre` et la recette `.legende-media` :

- **horizontalement** : `left: gouttière`, `max-width: 100% − 2 × gouttière` — les deux équerres basses sont dégagées quelle que soit la longueur de la légende, qui déborde vers le haut, où aucune équerre ne l'attend ;
- **verticalement** : `bottom: retrait + côté / 2` — la base de la légende s'aligne sur le **milieu de la barre verticale** des équerres basses. La légende se pose ainsi *dans* l'équerre, dont les deux bras restent visibles ; alignée sur la ligne de pied, elle écrasait le bras horizontal et l'angle cessait de se lire comme un repère de tirage.

**Ne pas repositionner une légende par des offsets en dur** (`left-4`, `bottom-3`, `left-[12.5%]`) : le lien avec les équerres serait rompu au premier changement de mesure.

**Le cartouche de plan ne se transpose pas à l'écran (§ 15)** — le bloc-titre de dessin technique (trois rangs de filet, données en mono, pied de feuille) est un **support imprimé**. L'en-tête d'une fiche projet en ligne suit la **règle des plans (§ 09)**, pas celle du cartouche : « la ressemblance serait trompeuse et coûteuse en lisibilité mobile ». `FicheTechnique.astro` est donc bien un plan posé, et non un cartouche de plan — ne pas chercher à le rapprocher du dessin technique.

**Lecture retenue sur le comptage des réserves** : le cartouche de légende et le fond profond du duotone **ne comptent pas** dans la règle « une seule réserve profonde par écran ». Cette règle borne une **surface** (un cinquième d'écran au maximum : couverture, relevé, panneau, bandeau de section) ; or la charte range le duotone parmi les emplois du profond tout en autorisant un relevé encré sur le même écran, et l'amendement A8 **impose** le cartouche. Une fiche projet porte donc légitimement, ensemble : un duotone, un cartouche de légende et une ligne encrée. Ne pas « corriger » cette coexistence.

## Plans et profondeur — trois rangs d'ombre

| Rang | Classe | Recette | Emploi |
|---|---|---|---|
| Planche de page | (`BaseLayout`) | papier `max-w-[1440px]` + `.trame-fond` + `shadow-[var(--shadow-page)]` (`0 0 90px` encre 18 %) sur body calcaire | la feuille du site |
| 1 — plan posé | `.plan-pose` | papier, **bordure 1 px `filet-2` obligatoire**, ombre `0 24px 60px` encre 12 % | planche principale d'un écran, carte de contenu |
| 2 — plan qui déborde | `.plan-deborde` | idem, ombre `0 32px 70px` encre 16 % ; chevauche le plan précédent de 40 px, se retire de 92 px sur un flanc | **une fois par écran au plus** |
| 3 — ligne encrée | `.plan-encre` | profond, **filet 3 px clair à gauche**, ombre `0 30px 64px` encre 30 %, pas de bordure | la réserve profonde de l'écran (relevés) |

L'ombre est toujours de l'encre translucide, **jamais du noir**. Aucun flou > 70 px (90 px réservé à la planche de page), aucun décalage horizontal, aucune ombre intérieure, aucune ombre sur un texte. La trame n'est jamais visible sous un plan (les plans ont un fond opaque).

**Révélation de plan** : poser `data-plan` sur les blocs `plan-pose` / `plan-deborde` / `plan-encre` significatifs (pas sur les cellules ni les cartes individuelles). `BaseLayout` observe et révèle une fois (760 ms, 22 px, courbe unique). Sans JS, tout est visible d'emblée.

## Trame et marges

- **Trame de fond** `.trame-fond` : pas de 28 px à 7 % d'encre — elle porte le fond de page, jamais visible sous un plan.
- **Module 28 px** (le pas de la trame) ; marge de page **60 px** (44 px sous 1200 px, 24 px à 390 px) ; **76 px entre sections** ; gouttière **24 px**.
- Planche de page `max-w-[1440px]` sur calcaire ; conteneur de contenu `max-w-[1200px]` ; prose éditoriale `max-w-[840px]`.
- **Rayon 0 partout** — seule exception : la puce de section (cercle 7 px, `.puce-section`).
- Rapports d'image : **21:8** (bandeau), **16:10** (appui de titre), **3:2** (fiche, index) — aucun autre.

## Composants signature

- **Bouton principal** `.btn-principal` : **aplat encre**, texte papier mono 11/500, **filet clair 3 px à gauche**, padding 15/20, hover → profond 260 ms, flèche `→` admise. **Le filet ne bouge pas.**
- **Bouton filaire** `.btn-filaire` : 1 px à 28 % d'encre, texte pivot, hover → encre. Sur réserve profonde : `.btn-profond` (filaire clair — le pivot est interdit en texte et en filet porteur sur profond, 2,85).
- **Étiquette de mission** `.etiquette-mission` : mono 10 px, 0,12 em, filet 1 px 28 %, **jamais d'aplat, six max par bloc**. **Chip de filtre** `.chip-blueprint` : même dessin ; actif = aplat encre / texte papier (`aria-pressed`).
- **Cellule de liste** `.cellule-liste` : calcaire, bordure 1 px `filet-1`, min-h 112 px, **numéro mono en tête, intitulé (112/600) en pied aligné à droite**, hover → papier 300 ms.
- **Titre de section** : puce profonde 7 px + numéro `mono-label` pivot, puis `type-section` — mot porteur encre + complément clair précédé d'une barre oblique. Le mot porteur doit suffire au sens (le complément clair est toujours redondant ou accessoire — dérogation décorative documentée dans `accessibility-rgaa.md`).
- **Cartouche** (`FicheTechnique.astro`) : plan posé (bordure 1 px, ombre rang 1), en-tête calcaire, filets internes 1 px par rangs d'opacité, données mono. **La barre de rang 4 px n'existe plus.** Calé à gauche, jamais centré.
- **Index des références** (`/references`) : **rail de filtres à gauche + grille de cartes** `CarteProjet` sur trois colonnes depuis le 2026-08-26 (demande FT2E — les vignettes de filtre de 130 px étaient trop petites). Au-dessus de 1 024 px, les filtres occupent la **première colonne du rythme de la grille** (216 px à 1 024, 276 px dès 1 248 — mesures en CSS de composant, jamais en variantes arbitraires) : image 3:2 pleine tuile à l'état voilé 0,42 / dévoilé, **légende au cartouche de réserve** (A8) posé sur l'image — le voilage ne touche jamais le cartouche, qui est un frère de la boîte d'image. La grille tient **trois colonnes à droite** : dès 1 248 px de fenêtre, (860 − 2 × 16) / 3 = 276 px de carte et **274 px de vignette, la taille de conception exacte** — la mesure qui justifiait les quatre colonnes d'avant le rail est préservée (jamais de sur-échelle du dessin) ; à 1 024, cartes de 232–237 px, mono de vignette à 7,0–7,1 px ≥ plancher 6,5. Sous 1 024 px le rail se replie en **rangée au-dessus de la grille** (4 tuiles par ligne dès 768, 2 par ligne en dessous) et la légende revient **sous l'image** en mono pivot : sous ~200 px de tuile, le cartouche du libellé le plus long replierait sur trois lignes. Cartes **strictement homogènes** — aucun rang de statut, ni filet, ni graisse : voir **amendement A9**, qui remplace la prescription « liste tabulaire, pas une grille de cartes » de la révision 2.1. Toutes les fiches sur une page ; le filtre par secteur réduit la grille, il ne pagine pas.
- **Relevé clair** (composé en clair dans `src/pages/index.astro`, § 01 — le composant `ChiffresCles.astro` a été supprimé le 2026-08-15, il n'était plus importé nulle part) : colonnes séparées par filets 1 px `filet-2`, bord haut `filet-1` ; par colonne : commentaire (Archivo 400, 14 px, pivot — **le commentaire précède le chiffre**) → étiquette mono « — libellé » → chiffre `.releve-chiffre`. **Un seul chiffre en encre pleine par relevé** (celui que la page défend), les autres en `.releve-retrait` — **au pivot** (amendement A1), jamais en encre 13 % (1,27 sur papier).
- **Vignette de carte** (`CarteProjet.astro`, toutes les grilles du site) : la vignette est **plafonnée à 300 px — son repère — et centrée**, avec du papier autour lorsque la carte est plus large. Le plafond vit dans le composant du dessin, **jamais dans la grille appelante** : le nombre de colonnes est un réglage de page, la taille de conception est une propriété du dessin, et tant que la première devait deviner la seconde chaque nouvelle grille rouvrait le défaut. Mesuré le 2026-08-15 avant correction, sur les quatre grilles : **1,70 à 560 px de fenêtre** (une colonne sous `sm`, carte de 511), 1,44 à 480, 1,14 à 390, 1,13 à 1,36 entre 768 et 900, et 1,22 au bas des fiches. Corollaire : **pas de `aspect-[3/2]` sur la boîte d'image** — la hauteur suit le dessin, qui porte lui-même le rapport ; l'imposer au support ajouterait du papier en haut et en bas dès que la carte dépasse 300 px.
- **Planche de fiche** (`PlancheReference.astro`) : le dessin est **présent à toutes les largeurs** depuis le 2026-08-15 — il ne cède plus la place à sa lecture sous `lg`. Trois compositions distinctes, une par bande, **plafonnées à leur taille de conception et centrées**, jamais étirées : `planche.svg` (1200 × 800) au-dessus de **880 px**, `appui.svg` (552 × 368) de **480 à 879**, `vignette.svg` (300 × 200) en dessous de **480**. Les bornes viennent du **plancher de lisibilité du mono, 6,5 px** (mono minimal mesuré sur les 23 dossiers : 10 / 10 / 9 px), **pas de la grille Tailwind** — elles s'écrivent en `@media` dans le `<style>` du composant. **Aucune échelle au-dessus de 1,00** : la sur-échelle épaissit les filets de 1 px, c'est le défaut fondateur du dispositif. **La figure est le dessin, son cartouche et l'agrandissement — rien d'autre** : le repli de lecture textuel a été supprimé le 2026-08-15, parce qu'il s'intercalait entre l'illustration et le contenu réel de la page (jusqu'à 1 181 px de valeurs synthétiques avant le premier mot du sujet). L'équivalent textuel passe par `role="img"` + `aria_label` sur la vignette, qui est `aria-hidden` à la source. L'agrandissement est proposé à toutes les largeurs et prend **deux états sous 940 px** — ajusté à l'ouverture, puis 860 px pour lire, avec parcours au doigt. Détail et mesures : `docs/superpowers/specs/2026-08-16-responsive-planches-fiches.md`.
- **Média du hero de l'accueil** (`src/pages/index.astro`, slot `media` de `Hero.astro`) : depuis le 2026-08-26, un **cliché du corpus secteurs** (« Aurora, 147 logements », arbitrage FT2E — l'appui de la fiche vedette, plan posé blanc sur papier tramé, « flottait dans le vide ») aux trois signatures média : duotone 197°, équerres voile, cartouche de réserve (A8). Rapport 3:2, colonne de **7/12** (l'accroche tient dans 5 — elle est bornée à 46ch), lien vers `/references/?secteur=…` au motif du cliché principal de la coupe, **bureau seul (≥ 1 024 px)** — arbitrage LCP du 2026-08-27 : affiché au téléphone, le cliché devenait l'élément LCP mobile et coûtait 150–200 ms (7 tirs, 1 823–2 013 ms pour un budget de 1 800) ; masqué sous `lg`, le hero mobile redevient textuel et le LCP revient à son état « au seuil ». `eager` + `fetchpriority="high"` : candidat LCP au bureau — se mesure sur le déploiement après tout changement. La légende, l'alt et le crédit sont relus depuis la collection secteurs (une seule source, échec bruyant si le cliché quitte le corpus). Le plafond `.appui-hero` (552 px) est parti avec l'appui : il protégeait les filets de 1 px d'un dessin contre la sur-échelle — la règle du plafond porte sur le dessin, elle survit partout où un dessin est servi (`CarteProjet`, `PlancheReference`).
- **Relevé encré** (fiche projet) : `.plan-encre`, chiffres `.releve-chiffre text-voile`, étiquettes `mono-label text-clair` — la réserve profonde de l'écran.
- **Monogramme** (`Logo.astro`) : dessin inchangé (cadre ouvert + flux débordant) ; **hauteur minimale 28 px** à l'écran ; sous 180 px de place : `forme="cadre"`. Ne se déforme pas, ne reçoit ni ombre ni contour ; le débord ne se recadre jamais.
- **Équerres** (`CoinsCuivre.astro`) : 4 équerres 1 px au voile, **18 px de côté**, en retrait de 5 px dans les angles du média. Repère de tirage, pas un encadrement — jamais de cadre autour d'une image.
- **Images** : tout passe au duotone 197° (point noir `#001718`, point blanc `#E1F4F4`, gamma neutre) via `duotone-photo` / `duotone-media` (hachure placeholder). Jamais de couleurs natives, **deux annotations mono au maximum par image**. Toute **légende** se pose dans un cartouche de réserve `.cartouche-legende` (voile sur profond, 16,24) et jamais à même le cliché (amendement A8) ; les équerres restent en voile sur l'image.

## Interactions & motion

- **Une seule courbe** `--ease-blueprint` = `cubic-bezier(0.2, 0.7, 0.2, 1)` — remplace `cubic-bezier(0.16, 1, 0.3, 1)` :
  1. filet de flux (`TraceFlux.astro`), 900 ms, une fois par chargement — le seul tracé animé (⚠ actuellement débranché : retiré sur demande FT2E le 2026-08-07, option non arbitrée du chantier motion) ;
  2. révélation de plan (`[data-plan]`), **1000 ms, 28 px** (A11 — la charte portait 760 ms / 22 px), une fois à l'entrée dans la vue ; les grilles de cartes (`[data-plan-groupe]`) se révèlent **en cascade**, 80 ms par rang plafonné au sixième (A11) ;
  3. survol de cellule, 300 ms, calcaire → papier ;
  4. survol de bouton, 260 ms, encre → profond.
- **Survol = bascule de fond** — aucun déplacement, aucun filet qui s'épaissit (**plus de `box-shadow` inset**), aucune ombre qui apparaît. Le filet ne bouge pas. *Unique exception : A10 — l'ouverture de tranche de la coupe des secteurs, bornée au registre des amendements.*
- **Focus** : cadre `2px solid pivot`, décalé 2 px.
- Aucun compteur qui s'incrémente, aucun parallax, aucun hover lift ; `prefers-reduced-motion` partout (tout est posé d'emblée).

## Patterns

```astro
<!-- ✅ Titre de section : puce + numéro mono, mot porteur encre + complément clair -->
<div class="flex items-center gap-3">
  <span class="puce-section" aria-hidden="true"></span>
  <span class="mono-label text-pivot">01 — expertises</span>
</div>
<h2 class="type-section text-[26px] mt-4">
  <span class="text-encre">Six</span>
  <span class="text-clair">/expertises</span>
</h2>

<!-- ✅ Plan posé, révélé une fois à l'entrée dans la vue -->
<section class="plan-pose p-7" data-plan>…</section>

<!-- ✅ Relevé clair : le commentaire précède le chiffre, un seul plein -->
<div class="border-t border-filet-1 grid md:grid-cols-3">
  <div class="px-6 py-5 border-l border-filet-2 first:border-l-0">
    <p class="text-[14px] text-pivot">Un bureau né en 2008, toujours à La Rochelle.</p>
    <p class="mono-label text-pivot mt-3">— années d'exercice</p>
    <p class="releve-chiffre text-encre mt-2">17</p>       <!-- le chiffre que la page défend -->
  </div>
  <div class="px-6 py-5 border-l border-filet-2">
    …
    <p class="releve-chiffre releve-retrait mt-2">7</p>    <!-- les autres, en retrait AU PIVOT (A1) -->
  </div>
</div>

<!-- ✅ Ligne encrée — la réserve profonde de l'écran -->
<div class="plan-encre px-6 py-7">
  <p class="mono-label text-clair">performances mesurées</p>
  <p class="releve-chiffre text-voile mt-2">0,18</p>
</div>

<!-- ❌ Interdits -->
<div class="shadow-lg">…</div>                        <!-- ombre hors des trois rangs (+ planche de page) -->
<div class="rounded-lg">…</div>                       <!-- rayon 0 partout, sauf .puce-section -->
<div class="border-l-4 border-encre">…</div>          <!-- le rang ne passe plus par l'épaisseur -->
<p class="text-clair">Texte porteur sur papier</p>    <!-- clair jamais porteur sur fond clair (1,67:1), et toujours aria-hidden -->
<div class="bg-profond"><p class="text-pivot">…</p></div> <!-- vert FT2E interdit en texte sur profond -->
<section class="bg-profond">…</section> <!-- ×2 sur un même écran : une seule réserve profonde -->
<div style="transition: all 300ms cubic-bezier(0.16, 1, 0.3, 1)">…</div> <!-- ancienne courbe v2 -->
<a class="hover:shadow-[inset_0_0_0_1px_#00393a] hover:-translate-y-1">…</a> <!-- ni inset ni déplacement au survol -->
```

## Mode sombre

**Non applicable.** Le clair gouverne ; la réserve profonde est une exception comptée. Ne pas implémenter `dark:`.
