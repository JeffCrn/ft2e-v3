# 08 · Configuration Decap CMS

Configuration de référence de **Decap CMS 3.x** pour FT2E. Le fichier de configuration vit dans `public/admin/config.yml`. L'interface est servie à `https://ft2e.fr/admin`.

## Choix d'authentification

Trois options possibles, à arbitrer en cadrage :

| Option | Avantages | Inconvénients | Recommandation |
|---|---|---|---|
| **GitHub OAuth direct** | Simple, gratuit, contrôle total | Nécessite que chaque rédacteur ait un compte GitHub + accès au repo | ✅ recommandé si l'équipe FT2E accepte GitHub |
| **git-gateway auto-hébergé** | Pas de dépendance GitHub côté rédacteur | Mise en place plus complexe, hébergement à maintenir | option B |
| **Netlify Identity** | Plug & play | Dépendance Netlify (alors qu'on est sur OVH) | ❌ écarté |

**Recommandation V1** : GitHub OAuth direct avec une OAuth App dédiée FT2E. Les rédacteurs (au moins une personne de l'équipe FT2E) reçoivent un accès en `write` sur le dépôt.

## Fichier `public/admin/index.html`

```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="robots" content="noindex,nofollow" />
  <title>FT2E — Administration du contenu</title>
  <link rel="icon" href="/favicon.svg" />
</head>
<body>
  <script src="https://unpkg.com/decap-cms@^3.0.0/dist/decap-cms.js"></script>
</body>
</html>
```

> **Note** : on charge Decap depuis unpkg pour simplifier la V1. Pour la V1.1, envisager de bundler Decap localement (`decap-cms-app`) pour la souveraineté.

## Fichier `public/admin/config.yml` — structure complète

```yaml
backend:
  name: github
  repo: <organisation>/ft2e-site     # à remplacer
  branch: main
  base_url: https://api.netlify.com  # ou OAuth proxy auto-hébergé
  # auth_endpoint: auth                # selon implémentation OAuth
  squash_merges: true

media_folder: "public/images"
public_folder: "/images"

locale: fr
publish_mode: editorial_workflow

site_url: https://ft2e.fr
display_url: https://ft2e.fr
logo_url: /images/logo/logo-ft2e-symbol.svg

collections:

  # ───────────────── PROJETS ─────────────────
  - name: "projets"
    label: "Projets / Références"
    label_singular: "Projet"
    folder: "src/content/projets"
    create: true
    delete: true
    slug: "{{slug}}"
    identifier_field: titre
    summary: "{{titre}} — {{lieu}} ({{annee}})"
    sortable_fields: [annee, titre, secteur]
    view_filters:
      - { label: "Mis en avant", field: en_avant, pattern: true }
      - { label: "Logement", field: secteur, pattern: "Logement" }
      - { label: "Tertiaire", field: secteur, pattern: "Tertiaire" }
      - { label: "Santé", field: secteur, pattern: "Santé" }
      - { label: "Sport", field: secteur, pattern: "Sport" }
      - { label: "Industriel", field: secteur, pattern: "Industriel" }
      - { label: "Patrimoine", field: secteur, pattern: "Patrimoine" }
    fields:
      - { label: "Titre", name: "titre", widget: "string", required: true, pattern: ['.{2,80}', '2 à 80 caractères'] }
      - { label: "Secteur", name: "secteur", widget: "select", required: true,
          options: ["Logement", "Tertiaire", "Santé", "Sport", "Industriel", "Patrimoine"] }
      - { label: "Typologie", name: "typologie", widget: "select", required: true,
          options: ["Neuf", "Réhabilitation", "Extension", "Études d'exécution"] }
      - { label: "Maître d'ouvrage", name: "moa", widget: "string", required: true }
      - { label: "Architecte", name: "architecte", widget: "string", required: false }
      - { label: "Lieu", name: "lieu", widget: "string", required: true,
          hint: "Commune (code postal). Ex: La Rochelle (17000)" }
      - { label: "Surface (m²)", name: "surface_m2", widget: "number", required: false, value_type: "int", min: 1 }
      - { label: "Année de livraison", name: "annee", widget: "number", required: true, value_type: "int", min: 2008, max: 2030 }
      - { label: "Performance énergétique", name: "performance", widget: "string", required: false,
          hint: "Ex: RE2020 · Effinergie+" }
      - label: "Mission FT2E"
        name: "mission_ft2e"
        widget: "select"
        multiple: true
        required: true
        min: 1
        options: ["CVC", "Thermique", "Électricité CFO", "Électricité CFA", "SSI", "BIM", "Études d'exécution", "Audit & diagnostic"]
      - { label: "Image principale", name: "image_principale", widget: "image", required: true,
          media_library: { config: { multiple: false } } }
      - { label: "Texte alternatif image principale", name: "image_principale_alt", widget: "string", required: true,
          hint: "Description courte du visuel, lue par les lecteurs d'écran" }
      - label: "Galerie"
        name: "galerie"
        widget: "list"
        required: false
        summary: "{{fields.alt}}"
        fields:
          - { label: "Image", name: "src", widget: "image" }
          - { label: "Légende / alt", name: "alt", widget: "string" }
      - { label: "Mis en avant en accueil", name: "en_avant", widget: "boolean", default: false,
          hint: "Maximum 4 projets en avant simultanément" }
      - { label: "Récit projet", name: "body", widget: "markdown",
          hint: "Structure recommandée : Enjeu → Solution → Particularités → Résultat (3 à 6 paragraphes)" }

  # ───────────────── ACTUALITÉS ─────────────────
  - name: "actualites"
    label: "Actualités"
    label_singular: "Actualité"
    folder: "src/content/actualites"
    create: true
    delete: true
    slug: "{{year}}-{{month}}-{{slug}}"
    identifier_field: titre
    summary: "{{date | date('YYYY-MM-DD')}} — {{titre}}"
    sortable_fields: [date, titre]
    fields:
      - { label: "Titre", name: "titre", widget: "string", required: true }
      - { label: "Chapô", name: "chapo", widget: "text", required: true,
          hint: "2 à 3 phrases annonçant le contenu (40 à 280 caractères)" }
      - { label: "Date de publication", name: "date", widget: "datetime", required: true,
          format: "YYYY-MM-DD", date_format: true, time_format: false }
      - { label: "Auteur", name: "auteur", widget: "string", required: false,
          hint: "Prénom Nom — Fonction" }
      - { label: "Image d'illustration", name: "image", widget: "image", required: false }
      - { label: "Alt image", name: "image_alt", widget: "string", required: false }
      - label: "Catégories"
        name: "categories"
        widget: "select"
        multiple: true
        required: true
        min: 1
        options: ["Chantier en cours", "Livraison", "Événement", "Article technique", "Vie du cabinet"]
      - { label: "Mis en avant", name: "en_avant", widget: "boolean", default: false }
      - { label: "Corps", name: "body", widget: "markdown" }

  # ───────────────── ÉQUIPE ─────────────────
  - name: "equipe"
    label: "Équipe"
    label_singular: "Membre de l'équipe"
    folder: "src/content/equipe"
    create: true
    delete: false
    slug: "{{slug}}"
    identifier_field: prenom
    summary: "{{prenom}} {{nom}} — {{fonction}}"
    sortable_fields: [ordre, nom]
    fields:
      - { label: "Prénom", name: "prenom", widget: "string", required: true }
      - { label: "Nom", name: "nom", widget: "string", required: true }
      - { label: "Fonction", name: "fonction", widget: "string", required: true,
          hint: "Ex: Associé · Ingénieur Efficacité Énergétique" }
      - { label: "Spécialités", name: "specialites", widget: "list", required: true }
      - { label: "Formation", name: "formation", widget: "string", required: false }
      - { label: "Photo", name: "photo", widget: "image", required: true }
      - { label: "Alt photo", name: "photo_alt", widget: "string", required: true }
      - { label: "Ordre d'affichage", name: "ordre", widget: "number", required: true, value_type: "int" }
      - { label: "Associé", name: "associe", widget: "boolean", default: true,
          hint: "Distingue associés / collaborateurs en interne (n'affecte pas l'affichage)" }
      - { label: "Email contact", name: "contact_email", widget: "string", required: false,
          pattern: ['^[^@]+@[^@]+\\.[^@]+$', 'Adresse email valide'] }
      - { label: "Présentation", name: "body", widget: "markdown", required: false }

  # ───────────────── EXPERTISES ─────────────────
  - name: "expertises"
    label: "Expertises"
    label_singular: "Expertise"
    folder: "src/content/expertises"
    create: false   # 6 expertises fixes — on édite, on ne crée pas
    delete: false
    slug: "{{slug}}"
    identifier_field: titre
    summary: "{{titre}}"
    sortable_fields: [ordre]
    fields:
      - { label: "Titre", name: "titre", widget: "string", required: true }
      - { label: "Accroche", name: "accroche", widget: "text", required: true }
      - { label: "Icône", name: "icone", widget: "string", required: true,
          hint: "Nom du SVG dans public/images/icons (sans extension)" }
      - { label: "Ordre d'affichage", name: "ordre", widget: "number", required: true, value_type: "int" }
      - { label: "Livrables", name: "livrables", widget: "list", required: true }
      - label: "Typique pour"
        name: "typique_pour"
        widget: "select"
        multiple: true
        options: ["Logement", "Tertiaire", "Santé", "Sport", "Industriel", "Patrimoine"]
      - label: "FAQ"
        name: "faq"
        widget: "list"
        required: false
        summary: "{{fields.question}}"
        fields:
          - { label: "Question", name: "question", widget: "string" }
          - { label: "Réponse", name: "reponse", widget: "text" }
      - { label: "Corps de page", name: "body", widget: "markdown" }

  # ───────────────── SECTEURS ─────────────────
  - name: "secteurs"
    label: "Secteurs"
    label_singular: "Secteur"
    folder: "src/content/secteurs"
    create: false
    delete: false
    slug: "{{slug}}"
    identifier_field: titre
    fields:
      - { label: "Titre", name: "titre", widget: "string", required: true }
      - { label: "Accroche", name: "accroche", widget: "text", required: true }
      - { label: "Image", name: "image", widget: "image", required: true }
      - { label: "Alt image", name: "image_alt", widget: "string", required: true }
      - { label: "Ordre", name: "ordre", widget: "number", required: true, value_type: "int" }
```

## Workflow éditorial

`publish_mode: editorial_workflow` active un cycle **brouillon → en relecture → prêt à publier → publié**. Chaque transition crée un commit signé Decap.

Rôles recommandés :
- **Rédacteur** (FT2E associé) : crée et édite des brouillons.
- **Valideur** (un autre associé désigné) : passe en « prêt à publier ».
- **Publication** : automatique via merge sur `main` + déclenchement CI/CD.

## Médias

- Tous les médias uploadés via Decap atterrissent dans `public/images/` par défaut.
- **À organiser manuellement** : déplacer les images projet vers `public/images/projets/<slug>/` avant publication. Une amélioration ultérieure (V1.1) sera d'ajouter une logique de classement automatique.
- **Optimisation post-upload** : ajouter un hook GitHub Action qui passe `sharp` sur les images uploadées pour générer AVIF + dimensions.

## Cohérence Zod ↔ Decap — golden rule

Toute modification d'un schéma Zod (`src/content/config.ts`) **doit** être répercutée dans `public/admin/config.yml` au sein du même commit. Le sous-agent `content-modeller` (`.claude/agents/content-modeller.md`) est responsable de cette synchronisation.

## Tests d'intégration

```bash
# 1. Build local
npm run build

# 2. Servir le build local
npm run preview

# 3. Aller sur http://localhost:4321/admin
# 4. S'authentifier
# 5. Tester pour chaque collection :
#    - Création d'une entrée
#    - Édition d'une entrée existante
#    - Workflow éditorial (brouillon → publié)
#    - Téléversement d'une image
# 6. Vérifier que les fichiers .md générés passent `npm run build`
```
