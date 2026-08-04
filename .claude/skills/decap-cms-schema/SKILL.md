---
name: decap-cms-schema
description: Génère ou modifie la configuration Decap CMS (public/admin/config.yml) en cohérence stricte avec les schémas Zod de src/content/config.ts. À déclencher pour tout ajout/modification de collection ou de widget Decap.
---

# Skill : Decap CMS — schéma & config

## Principe d'or

**Toute modification d'un schéma Zod côté Astro doit être répercutée immédiatement dans `public/admin/config.yml`, et inversement.**

Le moindre désalignement = bug critique : les rédacteurs FT2E saisissent des données invalides au prochain build.

## Structure de `public/admin/config.yml`

```yaml
backend:
  name: git-gateway       # ou github selon le déploiement final, à valider
  branch: main
  squash_merges: true

media_folder: "public/images"
public_folder: "/images"

locale: fr

publish_mode: editorial_workflow   # workflow brouillon → relecture → publication

collections:
  - name: "projets"
    label: "Projets"
    label_singular: "Projet"
    folder: "src/content/projets"
    create: true
    slug: "{{slug}}"
    identifier_field: titre
    summary: "{{titre}} — {{lieu}} ({{annee}})"
    sortable_fields: [annee, titre]
    view_filters:
      - label: "Mis en avant"
        field: en_avant
        pattern: true
      - label: "Par secteur"
        field: secteur
    fields:
      - { label: "Titre", name: "titre", widget: "string", required: true }
      - { label: "Secteur", name: "secteur", widget: "select",
          options: ["Logement", "Tertiaire", "Santé", "Sport", "Industriel", "Patrimoine"],
          required: true }
      - { label: "Typologie", name: "typologie", widget: "select",
          options: ["Neuf", "Réhabilitation", "Extension", "Études d'exécution"],
          required: true }
      - { label: "Maître d'ouvrage", name: "moa", widget: "string", required: true }
      - { label: "Architecte", name: "architecte", widget: "string", required: false }
      - { label: "Lieu", name: "lieu", widget: "string", required: true }
      - { label: "Surface (m²)", name: "surface_m2", widget: "number", value_type: "int", required: false }
      - { label: "Année de livraison", name: "annee", widget: "number", value_type: "int", required: true }
      - { label: "Performance énergétique", name: "performance", widget: "string", required: false }
      - { label: "Mission FT2E", name: "mission_ft2e", widget: "select", multiple: true,
          options: ["CVC", "Thermique", "Électricité CFO", "Électricité CFA", "SSI", "BIM", "Études d'exécution", "Audit & diagnostic"],
          required: true }
      - { label: "Image principale", name: "image_principale", widget: "image", required: true }
      - { label: "Texte alternatif image principale", name: "image_principale_alt", widget: "string", required: true }
      - { label: "Galerie", name: "galerie", widget: "list", required: false,
          fields:
            - { label: "Image", name: "src", widget: "image" }
            - { label: "Légende / alt", name: "alt", widget: "string" } }
      - { label: "Mis en avant en accueil", name: "en_avant", widget: "boolean", default: false }
      - { label: "Récit projet", name: "body", widget: "markdown" }
```

## Widgets Decap utiles

- `string` — texte court
- `text` — texte long simple
- `markdown` — corps Markdown (récit projet, article)
- `number` — valeur numérique avec `value_type: int|float`
- `boolean` — booléen
- `datetime` — date ISO
- `select` — choix dans une liste fermée (avec `multiple: true` pour multi-sélection)
- `list` — liste de sous-objets
- `image` / `file` — média
- `relation` — référence à un autre fichier de collection (utile pour `services` ↔ `secteurs`)

## Auth & déploiement

- **Identity provider** : à arbitrer en cadrage. Options : Netlify Identity (legacy), GitHub OAuth direct, ou `git-gateway` via proxy auto-hébergé.
- L'authentification finale doit être conforme RGPD (pas de fuite de données vers un tiers non-UE non maîtrisé).

## Tester localement

```bash
# 1. Lancer Astro dev
npm run dev

# 2. Naviguer vers http://localhost:4321/admin
# 3. Vérifier que toutes les collections apparaissent
# 4. Tester la création d'un projet → vérifier que le .md généré valide le Zod
```

## Cohérence Zod ↔ Decap — checklist

À chaque modification :

- [ ] Le champ est défini dans **les deux** fichiers.
- [ ] Le caractère obligatoire est cohérent (`z.string()` ↔ `required: true`).
- [ ] Les énumérations sont identiques (`z.enum([...])` ↔ `options: [...]`).
- [ ] Le type est cohérent (`z.number().int()` ↔ `widget: number, value_type: int`).
- [ ] La documentation `docs/03-modele-contenu.md` est à jour.
