# Schéma — collection `actualites`

## Champs

| Champ | Type | Obligatoire | Contrainte | Description |
|---|---|---|---|---|
| `titre` | string | ✅ | 5–80 c. | Titre de l'article. Forme factuelle ou interrogative modeste. |
| `chapo` | text | ✅ | 40–280 c. | 2–3 phrases qui annoncent le contenu. |
| `date` | date | ✅ | ISO `YYYY-MM-DD` | Date de publication. |
| `auteur` | string | ⚪ | — | Forme : `Prénom Nom — Fonction`. |
| `image` | string (path) | ⚪ | regex `^/images/actualites/.+\.(jpg|jpeg|avif|webp)$` | Image d'illustration. |
| `image_alt` | string | ⚪ | — | Obligatoire si `image` renseignée. |
| `categories` | enum[] | ✅ | ≥ 1 dans `Chantier en cours` `Livraison` `Événement` `Article technique` `Vie du cabinet` | Catégorisation. |
| `en_avant` | boolean | ⚪ | défaut `false` | Mise en avant. |

## Convention de nom de fichier

`YYYY-MM-titre-court.md`

Exemples : `2026-09-lancement-site.md`, `2026-10-livraison-ehpad-saintes.md`, `2026-11-article-re2020-logement-collectif.md`.

## URL publique

`https://ft2e.fr/actualites/<slug>` (le slug est le nom de fichier sans extension).

## Indexation SEO

- JSON-LD `Article` ou `BlogPosting` selon catégorie.
  - `Article` pour `Article technique`.
  - `NewsArticle` ou `BlogPosting` pour les autres catégories.
- `og_type: article`.
- `og_image` = `image` si renseignée, sinon image OG par défaut FT2E.
- `datePublished` = `date`.

## Cadence éditoriale cible

≥ 1 publication par mois.

## Exemples valides

```yaml
---
titre: "Lancement du nouveau site FT2E"
chapo: "Un nouveau site institutionnel pour donner toute leur place aux références techniques et refléter la pluridisciplinarité de l'équipe."
date: 2026-09-01
auteur: "L'équipe FT2E"
image: "/images/actualites/2026-09-lancement-site.jpg"
image_alt: "Vue de la nouvelle page d'accueil ft2e.fr sur écran et mobile"
categories: ["Vie du cabinet"]
en_avant: true
---
```

```yaml
---
titre: "RE2020 en logement collectif : trois leviers de conception"
chapo: "La RE2020 redistribue les cartes en logement collectif neuf. Retour d'expérience sur trois leviers que nous mobilisons systématiquement en phase APD pour tenir Bbio, Cep et DH sans renoncer à l'enveloppe budgétaire."
date: 2026-11-15
auteur: "Vincent Marchand — Ingénieur thermicien"
image: "/images/actualites/2026-11-re2020-logement-collectif.jpg"
image_alt: "Modélisation thermique dynamique d'un immeuble de logements collectifs"
categories: ["Article technique"]
en_avant: false
---
```

## Évolutions prévues

- Champ `temps_lecture_min` calculé automatiquement à partir du corps Markdown.
- Champ `articles_lies` (liste de slugs).
- Champ `service_associe` (référence à `services` pour le maillage cocon sémantique).
