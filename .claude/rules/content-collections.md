# Content Collections

**Scope** : `src/content/` et `src/content.config.ts`.

## Principe

Tout contenu textuel ou structuré du site vit comme un fichier Markdown dans `src/content/`. Aucune exception. Pas de JSON, pas de TS de données, pas de fetch d'API.

## Collections du site

| Collection | Fichier exemple | Cardinalité cible V1 |
|---|---|---|
| `projets` | `src/content/projets/maison-pierre-loti.md` | ~30 |
| `expertises` | `src/content/expertises/audit-diagnostic.md` | 4 (fixe) |
| `equipe` | `src/content/equipe/mathieu.md` | 7 |
| `actualites` | `src/content/actualites/2026-09-lancement-site.md` | 1 → ∞ |
| `secteurs` | `src/content/secteurs/logements.md` | 7 (fixe) |

## Conventions de slug

- **kebab-case strict**, sans accents (`maison-pierre-loti`, pas `maison-pierre-loti-2024`).
- **Préfixe date** pour les actualités : `YYYY-MM-titre-court.md`.
- Le slug est dérivé du nom de fichier, **jamais saisi dans le frontmatter**.

## Conventions frontmatter

- **YAML** uniquement, jamais TOML.
- Champs **obligatoires** vs **optionnels** clairement marqués dans le Zod schema (`z.string()` vs `z.string().optional()`).
- **Dates en ISO 8601** (`2024-06-15`).
- **Fiches projet — référence et millésimes.** `reference` porte le **numéro d'affaire FT2E** en graphie `NN-NNN` (`NN` = millésime d'ouverture, `NNN` = rang dans l'année) : c'est le seul identifiant publiable, relevé sur une pièce FT2E (« Affaire n° : 22-033 », cartouche de plan) et jamais sur le seul nom de dossier. Il est **obligatoire dès que `demo: false`** et **interdit sur une fiche de démonstration** (un numéro fabriqué entrerait en collision avec une affaire réelle). `annee` est le millésime d'ouverture qu'encode la référence — le build refuse toute contradiction ; l'année de réception va dans `annee_livraison`, à ne renseigner qu'une fois la réception prononcée sur pièce (le schéma l'interdit quand `statut: en cours`). Ne **jamais** dériver un identifiant d'affichage depuis `annee` : c'est le défaut corrigé le 2026-08-08.
- Listes en YAML inline `[CVC, Électricité, BIM]` quand courtes, sinon en bloc `-`.

## Validation stricte

Le schéma Zod doit **refuser** :

- Un titre vide ou > 80 caractères.
- Un slug contenant majuscules, accents ou espaces.
- Un `secteur` en dehors de l'énumération (`Logements | Tertiaire / ERP | Industriel | Patrimoine | Coordination SSI | Monotechnique — Audit | Études d'exécution / BIM`).
- Une `mission_ft2e` vide.
- Une date dans le futur pour un projet livré.

## Le visuel d'une fiche projet — la planche, et rien d'autre

Depuis la clôture du chantier des planches (2026-08-15), `planche` est **obligatoire** et
les champs `image_principale` / `image_principale_alt` ont été **supprimés** du schéma, de
Decap et des quatre points de rendu qui branchaient dessus. Une fiche projet n'a plus
qu'un dispositif visuel. Le motif est celui du chantier : le visuel photographique
reproduisait l'ouvrage, donc l'œuvre de l'architecte.

- `planche` porte le chemin du SVG depuis `public/`, en graphie stricte
  `/images/projets/<slug>/planche.svg`. Quatre fichiers frères l'accompagnent dans le même
  répertoire — `planche.json`, `vignette.svg`, `appui.svg`, `planche.png` — et **ils ne se
  séparent pas** : le composant les charge par convention de nom, un manquant fait échouer
  le build. Depuis le 2026-08-15 c'est littéral pour les trois SVG : la fiche les inline
  **tous les trois** et en sert un par bande de largeur (planche ≥ 880 px, appui de 480 à
  879, vignette en dessous). Un dossier amputé de son `appui.svg` — jusque-là utile au seul
  hero de l'accueil — casse désormais toutes les fiches.
- **Le frontmatter ne porte ni l'alternative textuelle de la planche, ni son surtitre de
  vignette, ni le TITRE COURT** : ils vivent dans le `planche.json`, que le site lit au
  build. Les recopier créerait deux vérités pour la même donnée, et c'est la copie —
  jamais l'original — qui se désynchronise. Le `.md` dit *qu'il y a* une planche ; la
  planche dit ce qu'elle montre.
- **Deux titres, deux emplois, aucune redondance** (2026-08-15) :
  - le `titre` du **frontmatter** est long et descriptif — « Néréa, 90 logements et un
    commerce à Aytré ». Il sert le `<h1>` de la fiche, la balise `<title>`, la description
    et le JSON-LD : c'est la forme que le référencement indexe, et elle ne bouge pas ;
  - le `titre` du **`planche.json`** est court — « Néréa, 90 logements », deux à quatre
    mots, relu par FT2E et déjà composé à 30 px sur la planche. Il sert partout où le
    titre n'est pas le sujet de la page : carte de projet, index des références,
    carte-lien de la vedette.

  L'unique lecture passe par **`titreCourt()`** (`src/lib/projets.ts`) : aucun composant
  ne relit le JSON pour son compte. La fonction **échoue bruyamment** si le champ manque,
  plutôt que de retomber sur le titre long — un repli silencieux réintroduirait dans une
  carte le titre de quatre lignes qu'on venait d'en chasser.

  Mesure qui a motivé la règle : sur `/references`, le titre est en `md:truncate` ; avec
  les titres longs, **14 lignes sur 23 étaient coupées à l'ellipse**, jusqu'à 103 px
  escamotés. Avec les titres courts, zéro — au bureau comme à 390 px.
- **Le `superRefine` qui arbitrait « planche OU visuel » a disparu avec l'alternative.**
  Une règle qui n'a plus rien à départager n'est pas un garde-fou : c'est un contrôle qui
  ment sur ce qu'il contrôle. L'obligation est portée par le champ lui-même.
- Champs supprimés du schéma et de Decap, pour mémoire : `galerie` (2026-08-12, consommé
  nulle part), `image_principale` / `image_principale_alt` (2026-08-15, remplacés par la
  planche), `demo_reason` et `contact_email` (2026-08-15, renseignés dans zéro fichier et
  lus nulle part).

## `lieu` : libre au frontmatter, réduit à la commune à l'écran

Le champ `lieu` accepte de la commune nue — « Aytré (17440) » — à l'adresse de chantier
complète — « 23 quai Valin, Vieux Port sud, La Rochelle (17000), Charente-Maritime ». La
latitude est voulue : elle sert le dossier d'affaire. **Elle ne sort jamais telle quelle à
l'écran** depuis le 2026-08-15 : `commune()` (`src/lib/projets.ts`) en extrait le segment
qui porte le code postal, et c'est cette forme — « La Rochelle (17000) » — que rendent le
pied de carte, le sous-titre de fiche, le cartouche et la carte-lien de la vedette.

Deux conséquences pour qui édite une fiche :

- **le code postal entre parenthèses est obligatoire** — c'est lui qui délimite le segment
  de commune. `commune()` lève une erreur de build en son absence plutôt que de rendre
  l'adresse entière : un repli silencieux ne se verrait que sur une fiche sur vingt-trois ;
- **le reste est libre** — rue, lieu-dit, département, île : rien de tout cela ne s'affiche,
  et le JSON-LD (`locationCreated.name`) conserve la chaîne entière pour le référencement.

## Référence vers les images

- Les cinq pièces d'une planche dans `public/images/projets/{slug}/`, jamais ailleurs.
- Les photographies d'**équipe** restent référencées **dans le frontmatter** par leur
  chemin public — `/images/equipe/<fichier>.jpg` — avec **alt text obligatoire** (champ
  Zod requis). C'est le seul endroit du site où une photographie est encore attendue.
  ⚠ **Depuis le 2026-08-16, les fichiers eux-mêmes vivent dans `src/assets/equipe/`**,
  pas dans `public/` : `astro:assets` ne traite que ce qu'il résout depuis `src/`, et
  `public/` est recopié tel quel. Le chemin du frontmatter n'a pas changé pour autant —
  il décrit ce que le visiteur verra, et c'est le rendu qui le résout, par le glob de
  `src/lib/photos.ts` (voir `.claude/rules/astro-conventions.md` § Photographies
  optionnelles). **Déposer une photographie dans `public/images/equipe/` ne l'affichera
  pas.**

## Récit projet (corps Markdown)

- **3 à 6 paragraphes** : enjeu posé, solution apportée, particularités techniques, résultat.
- Sous-titres `##` autorisés, jamais `#` (réservé au `titre` du frontmatter).
- Pas d'emphase agressive (gras minimal, italique pour précisions techniques).
- Pas de HTML inline sauf cas justifié (`<sup>`, `<sub>`).

## Aucun honoraire FT2E ne se publie — demande client du 2026-09-16

**Le site ne porte jamais ce que FT2E a perçu.** Ni montant, ni taux, ni part de
groupement, ni le vocabulaire qui y renvoie. La règle vaut pour tout ce qui est
servi : le corps de la fiche, le frontmatter, et **les cinq pièces de la planche**.

Ce qui est **interdit** :

- un montant d'honoraires, de forfait de mission ou de marché de maîtrise
  d'œuvre — le sien comme celui du groupement ;
- un **taux** de rémunération ou de mission (« 7,3 % », « calculée au taux de
  8 % »), et toute **part** (« 11,5 % de la mission ») : un taux appliqué à une
  enveloppe publiée **redonne le montant** ;
- une **assiette** présentée comme telle (« l'estimation qui sert d'assiette aux
  honoraires ») — elle dit au lecteur quoi multiplier ;
- le vocabulaire : « proposition d'honoraires », « note d'honoraires », « calcul
  d'honoraires », « honoraires facturés ». Écrire **« proposition de mission »**,
  « contrat », « la mission s'achève ».

Ce qui **reste publiable**, et la frontière est celle-là : **les chiffres du
maître d'ouvrage, pas la rémunération du bureau.** Montant des marchés de
travaux, estimations de lots, coût d'objectif, enveloppe prévisionnelle,
investissements et économies d'un scénario d'étude — ce sont les chiffres de
l'opération, ils démontrent la portée d'une mission sans dire ce qu'elle a
rapporté. ⚠ **Sauf s'ils sont accompagnés d'un taux** : l'enveloppe plus le taux
font l'honoraire.

⚠ **Le numéro d'affaire est déjà traité, et pour un motif voisin** : la graphie
`NN-NNN` encode le rang dans l'année, donc le volume annuel d'affaires du
bureau. Il est publié parce que FT2E l'a voulu (règle 10), et les planches
l'excluent de leur dessin. Ne pas confondre les deux décisions.

### ⚠ La planche ne s'arrête pas au dessin : son JSON est SERVI

`public/` est recopié tel quel dans `dist/`. **Chaque `planche.json` est donc
téléchargeable à son URL** — `https://<site>/images/projets/<slug>/planche.json`
—, y compris les champs que personne n'affiche : `exclusions_appliquees`,
`a_valider_ft2e`, `archetype_motif`, `controles`.

C'est par là que les honoraires ont fui, et d'une manière qui mérite d'être
retenue : **le champ qui recensait ce que la planche avait écarté le citait pour
le prouver.** « Tout montant : … honoraires (13 030 € HT dont 3 200 pour la
coordination SSI) ». Une note qui consigne ce qu'on a retiré, en le recopiant,
ne retire rien. Relevé le 2026-09-16 : **41 dossiers sur 47** portaient un
montant dans leur JSON, contre une quinzaine dans la prose — le corpus le moins
regardé était le plus exposé.

Un commentaire de `scripts/insecables-aria-planches.py` affirmait que ces champs
« ne sortent jamais du dépôt ». L'hypothèse était raisonnable et n'avait jamais
été vérifiée. **Un champ non affiché n'est pas un champ non publié.**

Formulation à employer dans `exclusions_appliquees`, qui dit l'exclusion sans la
documenter par l'exemple :

> Tout montant, de travaux comme d'honoraires : aucune donnée commerciale n'est
> portée au dessin — ni montant de travaux, ni estimation de lot, ni honoraires,
> ni taux de mission.

### Le contrôle

Il se rejoue, et il porte sur les **trois corpus servis à la fois** — la prose,
les JSON de `public/` **et leur copie dans `dist/`**, plus le HTML produit :

```bash
python scripts/controle-honoraires.py      # sortie 1 s il trouve une faute
```

⚠ **Ne pas refaire ce contrôle en `grep -P`.** Sur cette machine il refuse la
locale — « -P supports only unibyte and UTF-8 locales » — et rend **0**, un zéro
qui ressemble à un succès. Mesuré le 2026-09-16 : la sonde témoin, qui devait
trouver un montant de travaux, rendait 0 elle aussi, et les trois contrôles
« verts » n avaient rien mesuré. Le script porte donc **une sonde témoin qui le
fait échouer quand son motif ne mord plus**.

⚠ **Le contrôle sur `src/` ne suffit pas** : c est `dist/` qui est servi, et il
contient `public/` recopié. Le script inspecte les deux.

## Tests à exécuter

- Au build : Astro valide toutes les collections via Zod. **Build qui échoue = collection invalide.**
- Linter Markdown : `npx markdownlint-cli2 src/content/**/*.md`.
