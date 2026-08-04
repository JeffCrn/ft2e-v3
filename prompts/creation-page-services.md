# Prompt — création des pages Services

## Page index `/services`

```
Lis CLAUDE.md, docs/04-specifications-pages.md (section Services),
docs/02-design-system.md, .claude/rules/tailwind-design-tokens.md.

Implémente la page `/services` (src/pages/services/index.astro) :
- Hero éditorial sobre.
- Grille des 6 services (récupérée depuis la collection `services` triée
  par `ordre`).
- CTA secteur (lien vers la liste des secteurs ou vers les références).

Composant à réutiliser : CartesServices.astro (si déjà créé), sinon
déléguer à component-builder.

Validation : npm run build + Lighthouse mobile ≥ 90.
```

## Sous-pages services `/services/[slug]`

```
Lis CLAUDE.md, docs/04-specifications-pages.md (section Services),
content-templates/service-modele.md, content-models/service.schema.md.

Implémente la route dynamique `/services/[slug]` (src/pages/services/[slug].astro)
qui rend chaque service de la collection.

Structure imposée par la spec :
1. Hero — titre + accroche.
2. Enjeu (corps Markdown du fichier service).
3. Livrables (liste depuis frontmatter).
4. Méthodologie (sous-titres dans le corps).
5. Exemples chiffrés / cas typiques.
6. FAQ (depuis frontmatter, accordéon accessible).
7. 3 projets représentatifs auto-sélectionnés via la mission_ft2e
   correspondante.
8. CTA contact.

JSON-LD obligatoire :
- Service (cf. .claude/skills/json-ld-builder/SKILL.md)
- BreadcrumbList
- FAQPage si frontmatter.faq présent

Métadonnées :
- title : "<titre du service> — FT2E"
- description : accroche du service
- og_image : générique service ou TODO si à produire

Génération des 6 routes via getStaticPaths().

Vérifications finales :
- npm run build doit générer 6 routes /services/<slug>.
- Aucun warning Astro.
- Audit a11y rapide : un seul h1, hiérarchie cohérente, focus visible.
```
