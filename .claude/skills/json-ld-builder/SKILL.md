---
name: json-ld-builder
description: Génère des blocs JSON-LD (LocalBusiness, BreadcrumbList, CreativeWork, Service, Person, FAQPage) conformes schema.org pour insertion dans le head des pages Astro. À déclencher pour « génère le JSON-LD de X », « ajoute le schema markup ».
---

# Skill : JSON-LD builder

## Principes

- Tout JSON-LD est inséré via un composant Astro dédié (`src/components/seo/JsonLd.astro`) plutôt qu'en dur dans chaque page.
- Aucune donnée inventée. Les valeurs viennent de la collection de contenu ou des constantes globales (`src/lib/constants.ts`).
- Le JSON-LD est **toujours** validé via `https://validator.schema.org/` avant publication.

## Composant Astro recommandé

```astro
---
// src/components/seo/JsonLd.astro
export interface Props {
  data: Record<string, unknown>;
}
const { data } = Astro.props;
---
<script type="application/ld+json" set:html={JSON.stringify(data)} />
```

## Constantes globales (à créer dans `src/lib/constants.ts`)

```ts
export const FT2E_BUSINESS = {
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  name: "FT2E",
  url: "https://ft2e.fr",
  // … (voir .claude/rules/seo-geo.md pour le bloc complet)
} as const;
```

## Schémas par type de page

### Accueil

- `ProfessionalService` (FT2E) — complet.
- `WebSite` avec `SearchAction` (si recherche interne future).

### Page service (`/services/cvc`)

- `Service` :
  - `serviceType: "CVC — Chauffage, Ventilation, Climatisation"`
  - `provider: { "@id": "https://ft2e.fr/#organization" }`
  - `areaServed`: liste des communes.
  - `hasOfferCatalog` si pertinent.

### Fiche projet (`/references/<slug>`)

- `CreativeWork` :
  - `name`: titre
  - `creator`: référence FT2E
  - `dateCreated`: année livraison (au format ISO 8601 : `YYYY`)
  - `locationCreated`: `{ "@type": "Place", "name": "<lieu>" }`
  - `about`: secteur + typologie
  - `keywords`: mission_ft2e

### Page équipe / membre

- `Person` :
  - `name`, `jobTitle`, `worksFor: { "@id": "https://ft2e.fr/#organization" }`
  - `image`, `description`

### Toute page interne

- `BreadcrumbList` reflétant la position.

### FAQ (GEO)

- Si une section FAQ est présente sur une page service, ajouter `FAQPage` avec `mainEntity` listant `Question` / `Answer`.

## Validation

```bash
# Extraction depuis une page rendue
curl -s http://localhost:4321/<route> | grep -oP '(?<=<script type="application/ld\+json">).*?(?=</script>)' | head -1 | jq .

# Validation manuelle
# → coller dans https://validator.schema.org/
```

## Anti-patterns

- ❌ Plusieurs `WebSite` ou plusieurs `ProfessionalService` sur la même page.
- ❌ JSON-LD contenant du HTML brut, des entités non-encodées, ou des valeurs `null`/`undefined`.
- ❌ Référence à des URL absolues non `https://ft2e.fr/...`.
