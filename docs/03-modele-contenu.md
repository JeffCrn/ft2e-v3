# 03 · Modèle de contenu

Toutes les Content Collections sont définies dans `src/content.config.ts` via Zod.

> **Source de vérité : le code (`src/content.config.ts`), pas ce document.** Ce fichier en est une lecture commentée, tenue à jour au mieux ; en cas d'écart, c'est le schéma Zod qui fait foi — lui seul bloque le build. Les extraits ci-dessous peuvent être abrégés. Règles d'emploi des champs : `.claude/rules/content-collections.md`.

## Schémas

### Collection `projets`

```ts
import { defineCollection, z } from 'astro:content';

const SECTEURS = ['Logements', 'Tertiaire / ERP', 'Industriel et commercial', 'Patrimoine', 'Monotechnique', 'Coordination SSI', "Études d'exécution / BIM"] as const;
// « Étude » = mission d'ingénierie sur un existant sans marché de travaux (audit, calcul de charges, faisabilité)
const TYPOLOGIES = ['Neuf', 'Réhabilitation', 'Extension', 'Étude', "Études d'exécution"] as const;
const MISSIONS = ['CVC', 'Thermique', 'Électricité CFO', 'Électricité CFA', 'Photovoltaïque', 'SSI', 'BIM', "Études d'exécution", 'Audit & diagnostic'] as const;

const projets = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/projets' }),
  schema: z.object({
    titre: z.string().min(2).max(80),
    secteur: z.enum(SECTEURS),
    typologie: z.enum(TYPOLOGIES),
    moa: z.string().min(2),
    architecte: z.string().optional(),
    lieu: z.string().min(2),
    surface_m2: z.number().int().positive().optional(),
    // Numéro d'affaire FT2E NN-NNN — requis si !demo, interdit si demo (superRefine)
    reference: z.string().regex(/^\d{2}-\d{3}$/).optional(),
    // Millésime d'OUVERTURE de l'affaire — doit valoir 2000 + les 2 chiffres de `reference`
    annee: z.number().int().min(2008).max(new Date().getFullYear() + 1),
    // Réception PRONONCÉE — interdit si statut === 'en cours' (superRefine)
    annee_livraison: z.number().int().min(2008).max(new Date().getFullYear() + 2).optional(),
    statut: z.enum(['livré', 'en cours', 'archive']).default('livré'),
    performance: z.string().optional(),       // ex: "RE2020 · Effinergie+"
    mission_ft2e: z.array(z.enum(MISSIONS)).min(1),
    image_principale: z.string().regex(/^\/images\/projets\/[a-z0-9-]+\/.+\.(jpg|jpeg|png|avif|webp)$/),
    image_principale_alt: z.string().min(5),
    galerie: z.array(z.object({
      src: z.string(),
      alt: z.string().min(3),
    })).optional(),
    en_avant: z.boolean().default(false),
    // Drapeau "version liminaire" — voir docs/14-version-liminaire.md
    demo: z.boolean().default(false),
    demo_reason: z.string().optional(),
  }),
});
```

### Collection `expertises`

```ts
const expertises = defineCollection({
  type: 'content',
  schema: z.object({
    titre: z.string().min(3).max(60),
    accroche: z.string().min(20).max(200),     // 1–2 phrases
    icone: z.string(),                          // nom du SVG dans public/images/icons
    ordre: z.number().int().min(1).max(99),    // ordre d'affichage en accueil
    livrables: z.array(z.string()),            // liste à puces
    typique_pour: z.array(z.enum(SECTEURS)),   // secteurs où cette expertise est mobilisée
    faq: z.array(z.object({
      question: z.string(),
      reponse: z.string(),
    })).optional(),
  }),
});
```

Slugs des 6 fichiers attendus :
`audit-diagnostic`, `etude-thermique`, `cvc`, `electricite`, `coordination-ssi`, `etudes-execution-bim`.

### Collection `equipe`

```ts
const equipe = defineCollection({
  type: 'content',
  schema: z.object({
    prenom: z.string(),
    nom: z.string(),
    fonction: z.string(),                       // ex: "Associé · Ingénieur Efficacité Énergétique"
    specialites: z.array(z.string()),
    formation: z.string().optional(),
    photo: z.string().regex(/^\/images\/equipe\/.+\.(jpg|jpeg|avif|webp)$/),
    photo_alt: z.string().min(5),
    ordre: z.number().int(),                    // ordre d'affichage page Équipe
    associe: z.boolean().default(true),         // distingue associés / collaborateurs (usage interne uniquement)
    contact_email: z.string().email().optional(),
  }),
});
```

Membres attendus (sept ingénieurs associés mentionnés) :
Mathieu, Géraldine, Sandrine, Vincent, Tanguy, Emma, Carole. **Nom de famille et fonctions précises à valider avec FT2E avant publication.**

### Collection `actualites`

```ts
const actualites = defineCollection({
  type: 'content',
  schema: z.object({
    titre: z.string().min(5).max(80),
    chapo: z.string().min(40).max(280),
    date: z.coerce.date(),
    auteur: z.string().optional(),              // nom + fonction
    image: z.string().regex(/^\/images\/actualites\/.+\.(jpg|jpeg|avif|webp)$/).optional(),
    image_alt: z.string().optional(),
    categories: z.array(z.enum([
      'Chantier en cours', 'Livraison', 'Événement', 'Article technique', 'Vie du cabinet',
    ])),
    en_avant: z.boolean().default(false),
  }),
});
```

Convention de nom de fichier : `YYYY-MM-titre-court.md`.

### Collection `secteurs`

```ts
const secteurs = defineCollection({
  type: 'content',
  schema: z.object({
    titre: z.string(),                          // ex: "Logement"
    accroche: z.string().min(40).max(240),
    image: z.string(),
    image_alt: z.string().min(5),
    ordre: z.number().int(),
  }),
});
```

## Synchronisation avec Decap CMS

Voir `docs/08-configuration-decap.md`. Toute modification de schéma Zod **doit être répercutée** dans `public/admin/config.yml` au sein du même commit (ou de la même PR).

## Migration et historique

- Toute migration de schéma **non-rétrocompatible** est documentée dans `docs/migrations/YYYY-MM-DD-description.md`.
- Tout renommage de champ entraîne une réécriture cohérente de tous les fichiers de contenu existants (script TS dans `scripts/`).
- Tout retrait de champ obligatoire → soit valeur par défaut, soit script de remplissage.

## Validation hors-build

```bash
# Lancer la validation manuellement (utile en CI)
npx astro check
```

Toute erreur de validation = **blocage du build**. Pas d'exception.
