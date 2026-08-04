# Convention de commit

**Scope** : tous les commits sur le dépôt.

## Format

```
<type>(<portée>): <sujet en français>

<corps facultatif — quoi et pourquoi, pas comment>

<footer facultatif — refs issues, breaking changes>
```

## Types autorisés

| Type | Usage |
|---|---|
| `feat` | nouvelle fonctionnalité visible (page, composant, fonctionnalité éditoriale) |
| `fix` | correction de bug |
| `refactor` | restructuration sans changement fonctionnel |
| `style` | mise en forme, espaces, virgules ; aucun code touché |
| `docs` | documentation (`docs/`, `README.md`, `CLAUDE.md`, commentaires) |
| `chore` | tâches de maintenance, dépendances, configuration |
| `perf` | amélioration de performance mesurée |
| `a11y` | accessibilité |
| `seo` | SEO ou GEO |
| `content` | ajout ou modification de contenu (fiche projet, actualité, équipe) |
| `build` | configuration de build, CI/CD |

## Portées (`<portée>`) standard

`accueil`, `societe`, `equipe`, `services`, `references`, `actualites`, `contact`, `layout`, `cms`, `seo`, `a11y`, `design-system`, `deploy`, `ci`, `deps`.

## Règles de sujet

- **Français**, pas d'anglais (sauf termes techniques universels : « build », « lint », « TypeScript »).
- **Impératif présent** : « ajoute », « corrige », « refactore ». Pas « ajouté » ni « ajoutera ».
- **Pas de majuscule** initiale sauf nom propre.
- **Pas de point final.**
- **≤ 72 caractères** pour la ligne de sujet.

## Exemples

```
feat(accueil): ajoute le bloc chiffres clés avec animation au scroll
fix(seo): corrige les canonicals dupliquées sur les pages projet
content(references): ajoute la fiche EHPAD de Saintes
a11y(formulaire): annonce les erreurs via aria-describedby
perf(images): convertit les visuels projets en AVIF
docs(cms): documente le workflow d'ajout d'une actualité
```

## Breaking changes

Si une modification casse l'éditorial Decap (changement de schéma) ou la structure publique d'URLs, **toujours** ajouter un footer :

```
BREAKING CHANGE: le champ `architecte` devient obligatoire dans les fiches projet.
Migration : éditer toutes les fiches existantes avant build.
```

## Commit signés (à activer après scaffolding)

```bash
git config commit.gpgsign true
```
