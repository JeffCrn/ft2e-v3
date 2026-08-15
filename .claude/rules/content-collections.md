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
- Un `secteur` en dehors de l'énumération (`Logements | Tertiaire / ERP | Industriel et commercial | Patrimoine | Monotechnique | Coordination SSI | Études d'exécution / BIM`).
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
  le build.
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
    titre n'est pas le sujet de la page : carte de projet, nomenclature, carte-lien de
    la vedette.

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

## Référence vers les images

- Les cinq pièces d'une planche dans `public/images/projets/{slug}/`, jamais ailleurs.
- Les photographies d'**équipe** (`public/images/equipe/`) restent référencées par chemin
  relatif depuis `public/` dans le frontmatter, avec **alt text obligatoire** (champ Zod
  requis) — c'est le seul endroit du site où une photographie est encore attendue.

## Récit projet (corps Markdown)

- **3 à 6 paragraphes** : enjeu posé, solution apportée, particularités techniques, résultat.
- Sous-titres `##` autorisés, jamais `#` (réservé au `titre` du frontmatter).
- Pas d'emphase agressive (gras minimal, italique pour précisions techniques).
- Pas de HTML inline sauf cas justifié (`<sup>`, `<sub>`).

## Tests à exécuter

- Au build : Astro valide toutes les collections via Zod. **Build qui échoue = collection invalide.**
- Linter Markdown : `npx markdownlint-cli2 src/content/**/*.md`.
