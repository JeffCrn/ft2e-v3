# Content Collections

**Scope** : `src/content/` et `src/content/config.ts`.

## Principe

Tout contenu textuel ou structuré du site vit comme un fichier Markdown dans `src/content/`. Aucune exception. Pas de JSON, pas de TS de données, pas de fetch d'API.

## Collections du site

| Collection | Fichier exemple | Cardinalité cible V1 |
|---|---|---|
| `projets` | `src/content/projets/maison-pierre-loti.md` | ~30 |
| `services` | `src/content/services/audit-diagnostic.md` | 6 (fixe) |
| `equipe` | `src/content/equipe/mathieu.md` | 7 |
| `actualites` | `src/content/actualites/2026-09-lancement-site.md` | 1 → ∞ |
| `secteurs` | `src/content/secteurs/logement.md` | 5 (fixe) |

## Conventions de slug

- **kebab-case strict**, sans accents (`maison-pierre-loti`, pas `maison-pierre-loti-2024`).
- **Préfixe date** pour les actualités : `YYYY-MM-titre-court.md`.
- Le slug est dérivé du nom de fichier, **jamais saisi dans le frontmatter**.

## Conventions frontmatter

- **YAML** uniquement, jamais TOML.
- Champs **obligatoires** vs **optionnels** clairement marqués dans le Zod schema (`z.string()` vs `z.string().optional()`).
- **Dates en ISO 8601** (`2024-06-15`).
- Listes en YAML inline `[CVC, Électricité, BIM]` quand courtes, sinon en bloc `-`.

## Validation stricte

Le schéma Zod doit **refuser** :

- Un titre vide ou > 80 caractères.
- Un slug contenant majuscules, accents ou espaces.
- Un `secteur` en dehors de l'énumération (`Logement | Tertiaire | Santé | Sport | Industriel | Patrimoine`).
- Une `mission_ft2e` vide.
- Une date dans le futur pour un projet livré.

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
