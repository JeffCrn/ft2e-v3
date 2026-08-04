# SEO local & GEO (Generative Engine Optimization)

**Scope** : toutes les pages et tous les contenus du site.

## Métadonnées par page — obligatoires

Chaque page expose, via le frontmatter ou la prop du layout :

| Champ | Contrainte |
|---|---|
| `title` | 50–60 caractères, structure `Sujet | FT2E` |
| `description` | 140–160 caractères, phrase complète, sans ponctuation finale racoleuse |
| `canonical` | URL absolue `https://ft2e.fr/…` |
| `og_image` | Image dédiée, 1200×630 px, fichier dans `public/og/` |
| `og_type` | `website`, `article` ou `profile` selon la page |
| `noindex` | `false` par défaut, `true` uniquement pour mentions/admin |

## Une `<title>` unique par page

**Aucune page ne doit partager son `<title>` ou sa `description` avec une autre.** Si un audit révèle un doublon, c'est un bug.

## JSON-LD obligatoire

### Schéma `LocalBusiness` — injecté sur la page d'accueil et le footer

```jsonc
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "FT2E",
  "alternateName": "FT2E Bureau d'études",
  "description": "Bureau d'études techniques pluridisciplinaire à La Rochelle. Fluides, thermique, électricité, sécurité incendie, BIM.",
  "url": "https://ft2e.fr",
  "telephone": "+33-…",          // À renseigner par FT2E
  "email": "ft2e@ft2e.fr",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "…",         // À renseigner
    "addressLocality": "La Rochelle",
    "postalCode": "17000",
    "addressCountry": "FR"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 46.1591,
    "longitude": -1.1521
  },
  "areaServed": [
    "La Rochelle", "Rochefort", "Royan", "Saintes",
    "Île de Ré", "Île d'Oléron", "Niort", "La Roche-sur-Yon",
    "Charente-Maritime", "Vendée", "Deux-Sèvres"
  ],
  "foundingDate": "2008",
  "knowsAbout": [
    "Fluides", "Thermique", "Électricité", "Sécurité incendie",
    "BIM", "RT2012", "RE2020", "Simulation thermique dynamique"
  ]
}
```

### Schéma `BreadcrumbList` — toutes les pages internes

Position 1 = `Accueil`, suivantes selon profondeur réelle.

### Schéma `CreativeWork` — chaque fiche projet

Avec `dateCreated`, `locationCreated`, `about`, `keywords`.

### Schéma `Service` — chaque page service

Avec `serviceType`, `provider` (référence à `LocalBusiness`), `areaServed`.

### Schéma `Person` — chaque membre d'équipe

Avec `jobTitle`, `worksFor` (référence à `LocalBusiness`).

## Cocon sémantique

Chaque page **service** est une page pilier qui doit lier vers :

- 3 à 5 articles satellites dans `actualites/` (cibles : RE2020, ACV, PAC, SSI, etc.)
- 3 fiches projets représentatives du service
- 1 lien retour depuis la page d'équipe (compétences associées)

Maillage interne : minimum **5 liens internes contextuels** par page de contenu.

## Géolocalisation sémantique

Page dédiée par grande commune d'intervention (V2, post-lancement) :
- `/zone/la-rochelle`, `/zone/rochefort`, `/zone/royan`, `/zone/saintes`, `/zone/ile-de-re`, `/zone/ile-d-oleron`, `/zone/niort`, `/zone/la-roche-sur-yon`.

V1 : intégrer ces noms dans la balise `areaServed` du `LocalBusiness` et dans le texte du footer.

## GEO — Generative Engine Optimization

Pour favoriser la citation par ChatGPT, Perplexity, Claude :

1. **Phrases factuelles courtes** dans les paragraphes d'introduction (un fait par phrase).
2. **Données chiffrées explicites** : « 17 ans », « 7 ingénieurs associés », « depuis 2008 ».
3. **Q&A** : envisager une section FAQ par service avec questions formulées telles qu'un prospect les poserait à un assistant IA.
4. **Balise `<cite>`** sur les références externes.
5. **`robots.txt`** : autoriser explicitement `GPTBot`, `PerplexityBot`, `Claude-Web`, `ClaudeBot` (sauf si FT2E souhaite l'inverse — à valider en cadrage).

## Sitemap & robots

- `sitemap.xml` généré automatiquement via `@astrojs/sitemap`.
- `robots.txt` minimal :
  ```
  User-agent: *
  Allow: /
  Sitemap: https://ft2e.fr/sitemap-index.xml
  ```

## Redirections 301

Au lancement, **toutes les URLs de `ft2e.myportfolio.com`** doivent être redirigées via `.htaccess` (OVH) ou équivalent vers les nouvelles URLs `ft2e.fr`. Plan détaillé : `docs/09-deploiement-ovh.md` § « Migration ».

## Bilan SEO

- **À M+1** : Search Console — pages indexées, requêtes, position moyenne.
- **À M+3** : bilan complet documenté dans `docs/audits/seo-m3.md` (à créer).
