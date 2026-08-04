# Schéma — collection `projets`

Documentation de référence du schéma Zod pour la collection `projets`. Tout désalignement entre ce document, `src/content/config.ts` et `public/admin/config.yml` est un bug.

## Note sur le champ `recit`

Le PDF (p. 15) liste 15 champs structurés pour la collection Projet, dont un champ `recit` de type Markdown. L'exemple donné par le PDF (p. 16) montre que **dans la pratique, le récit n'est pas un champ du frontmatter** : le frontmatter contient les 13 autres champs structurés, et le récit vit dans le **corps du fichier Markdown** (après le `---` de fermeture du frontmatter).

C'est exactement le fonctionnement natif d'Astro Content Collections : le frontmatter est typé via Zod, et le corps Markdown est exposé via la propriété `body` ou rendu directement par `<Content />`. Sémantiquement, ce corps **est** le champ `recit` du modèle PDF.

→ Dans le code Astro, on parle de `body`. Dans la documentation et dans Decap CMS, on parle de `recit`. Les deux désignent la même chose.

## Champs (état final, 14 dans le frontmatter + 1 dans le corps = 15 total comme le PDF)

| Champ | Type | Obligatoire | Contrainte | Description |
|---|---|---|---|---|
| `titre` | string | ✅ | 2–80 c. | Titre du projet tel qu'il s'affichera (`<h1>` de la fiche). |
| `secteur` | enum | ✅ | `Logement` `Tertiaire` `Santé` `Sport` `Industriel` `Patrimoine` | Secteur d'activité. |
| `typologie` | enum | ✅ | `Neuf` `Réhabilitation` `Extension` `Études d'exécution` | Typologie de l'opération. |
| `moa` | string | ✅ | ≥ 2 c. | Maître d'ouvrage. Forme attendue : nom de l'entité (« Habitat 17 », « Commune de Saintes »). |
| `architecte` | string | ⚪ | — | Architecte mandataire si différent du MOA. |
| `lieu` | string | ✅ | ≥ 2 c. | Forme attendue : `Commune (code postal)`. Ex : `La Rochelle (17000)`. |
| `surface_m2` | int | ⚪ | > 0 | Surface utile ou SDP selon convention FT2E (constance à respecter). |
| `annee` | int | ✅ | 2008–2030 | Année de livraison (ou prévue si projet en cours, à arbitrer cas par cas). |
| `performance` | string | ⚪ | — | Performance énergétique. Ex : `RE2020 · Effinergie+ niveau 1`. |
| `mission_ft2e` | enum[] | ✅ | ≥ 1, parmi `CVC` `Thermique` `Électricité CFO` `Électricité CFA` `SSI` `BIM` `Études d'exécution` `Audit & diagnostic` | Lot(s) traité(s) par FT2E. |
| `image_principale` | string (path) | ✅ | regex `^/images/projets/[a-z0-9-]+/.+\.(jpg|jpeg|png|avif|webp)$` | Chemin de l'image hero. |
| `image_principale_alt` | string | ✅ | ≥ 5 c. | Texte alternatif descriptif. |
| `galerie` | object[] | ⚪ | — | Liste d'images additionnelles. Chaque objet : `{ src, alt }`. |
| `en_avant` | boolean | ⚪ | défaut `false` | Mise en avant en accueil (max 4 simultanés). |
| `demo` | boolean | ⚪ | défaut `false` | **Drapeau « contenu de démonstration »** — affiche un badge `[DÉMO]` sur la carte projet et la fiche détail. À retirer une fois la fiche validée par FT2E en production. Voir `docs/14-version-liminaire.md`. |
| `demo_reason` | string | ⚪ | — | Optionnel. Explique pourquoi le contenu est marqué démo (ex. *« Projet cité dans le PDF p. 10 mais caractéristiques techniques exactes à confirmer »*). |

## Slug — règle de génération

Slug dérivé du nom de fichier (sans extension), au format **kebab-case sans accents**.

| Titre | Slug attendu |
|---|---|
| Maison Pierre Loti | `maison-pierre-loti` |
| EHPAD Le Doux-Refuge | `ehpad-le-doux-refuge` |
| Lycée des Métiers de la Mer | `lycee-des-metiers-de-la-mer` |

## URL publique

`https://ft2e.fr/references/<slug>`

## Indexation SEO

- `og_image` calculé automatiquement à partir de `image_principale` (recadrage 1200×630).
- `og_type` : `article`.
- JSON-LD `CreativeWork` injecté avec :
  - `name` = `titre`
  - `dateCreated` = `annee` (au format `YYYY`)
  - `locationCreated` = `lieu` parsé en `Place`
  - `about` = `secteur` + ` / ` + `typologie`
  - `keywords` = `mission_ft2e.join(', ')`

## Exemples valides minimaux

```yaml
---
titre: "Réhabilitation de l'EHPAD Le Doux-Refuge"
secteur: "Santé"
typologie: "Réhabilitation"
moa: "Centre Communal d'Action Sociale de Saintes"
architecte: "Atelier 17 Architectes"
lieu: "Saintes (17100)"
surface_m2: 3450
annee: 2024
performance: "BBC Rénovation · Effinergie Patrimoine"
mission_ft2e: ["CVC", "Électricité CFO", "Électricité CFA", "SSI"]
image_principale: "/images/projets/ehpad-doux-refuge/01.jpg"
image_principale_alt: "Façade rénovée de l'EHPAD Le Doux-Refuge, vue depuis le jardin sud"
galerie:
  - { src: "/images/projets/ehpad-doux-refuge/02.jpg", alt: "Chaufferie biomasse en sous-sol" }
  - { src: "/images/projets/ehpad-doux-refuge/03.jpg", alt: "Chambre type avec ventilation double flux" }
en_avant: true
---
```

## Validation

- **Au build** Astro : Zod refuse toute valeur non-conforme. Build échoue.
- **Pré-commit** : `npx markdownlint-cli2 src/content/projets/**/*.md`.
- **Manuel** : relire `image_principale_alt` (≥ 5 c. ne garantit pas la pertinence).

## Évolutions prévues (V1.1 et au-delà)

- Champ `partenaires` (liste : entreprises titulaires, autres BET cotraitants).
- Champ `coordonnees_geo` (`{lat, lng}`) pour cartographier les références.
- Champ `video_url` pour intégrer une vidéo de présentation (lite-youtube-embed).
- Champ `temoignage_moa` (objet `{auteur, fonction, texte}`).
