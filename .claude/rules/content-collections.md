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

## Le visuel d'une fiche projet — planche ou photographie

Depuis le 2026-08-12, `image_principale` et `image_principale_alt` sont **optionnels**, et
un champ `planche` les remplace sur les fiches traitées.

- `planche` porte le chemin du SVG depuis `public/`, en graphie stricte
  `/images/projets/<slug>/planche.svg`. Trois fichiers frères l'accompagnent dans le même
  répertoire — `planche.json`, `vignette.svg`, `planche.png` — et **ils ne se séparent
  pas** : le composant les charge par convention de nom, un manquant fait échouer le build.
- **Le frontmatter ne porte ni l'alternative textuelle de la planche ni son surtitre de
  vignette** : ils vivent dans le `planche.json`, que le composant lit au build. Les
  recopier créerait deux vérités pour la même donnée, et c'est la copie — jamais
  l'original — qui se désynchronise. Le `.md` dit *qu'il y a* une planche ; la planche dit
  ce qu'elle montre.
- `superRefine` refuse **une fiche sans planche ET sans visuel**, ainsi qu'**un visuel sans
  son alternative textuelle** (RGAA 1.1). L'optionnalité d'un champ ne doit jamais
  dégénérer en fiche muette.
- Le champ `galerie` a été **supprimé** du schéma et de Decap le 2026-08-12 : il n'était
  consommé nulle part dans `src/`.

## Référence vers les images

- Tous les visuels d'un projet dans `public/images/projets/{slug}/`.
- Frontmatter référence par chemin relatif depuis `public/` : `image_principale: /images/projets/maison-loti/01.jpg`.
- **Alt text obligatoire** pour chaque image (champ Zod requis).

## Récit projet (corps Markdown)

- **3 à 6 paragraphes** : enjeu posé, solution apportée, particularités techniques, résultat.
- Sous-titres `##` autorisés, jamais `#` (réservé au `titre` du frontmatter).
- Pas d'emphase agressive (gras minimal, italique pour précisions techniques).
- Pas de HTML inline sauf cas justifié (`<sup>`, `<sub>`).

## Tests à exécuter

- Au build : Astro valide toutes les collections via Zod. **Build qui échoue = collection invalide.**
- Linter Markdown : `npx markdownlint-cli2 src/content/**/*.md`.
