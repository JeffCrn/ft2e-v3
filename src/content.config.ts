import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const SECTEURS = ['Logement', 'Tertiaire', 'Santé', 'Sport', 'Industriel', 'Patrimoine'] as const;
const TYPOLOGIES = ['Neuf', 'Réhabilitation', 'Extension', "Études d'exécution"] as const;
const MISSIONS = ['CVC', 'Thermique', 'Électricité CFO', 'Électricité CFA', 'SSI', 'BIM', "Études d'exécution", 'Audit & diagnostic'] as const;

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
    annee: z.number().int().min(2008).max(new Date().getFullYear() + 1),
    /** Rang de nomenclature (charte v2) : filet 4 px livré / 2 px en cours / 1 px archive. */
    statut: z.enum(['livré', 'en cours', 'archive']).default('livré'),
    performance: z.string().optional(),
    mission_ft2e: z.array(z.enum(MISSIONS)).min(1),
    image_principale: z.string(),
    image_principale_alt: z.string().min(5),
    galerie: z.array(z.object({
      src: z.string(),
      alt: z.string().min(3),
    })).optional(),
    en_avant: z.boolean().default(false),
    demo: z.boolean().default(false),
    demo_reason: z.string().optional(),
  }),
});

const expertises = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/expertises' }),
  schema: z.object({
    titre: z.string().min(3).max(60),
    accroche: z.string().min(20).max(200),
    icone: z.string(),
    ordre: z.number().int().min(1).max(99),
    livrables: z.array(z.string()),
    typique_pour: z.array(z.enum(SECTEURS)),
    missions_liees: z.array(z.enum(MISSIONS)).optional(),
    faq: z.array(z.object({
      question: z.string(),
      reponse: z.string(),
    })).optional(),
  }),
});

const equipe = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/equipe' }),
  schema: z.object({
    prenom: z.string(),
    nom: z.string(),
    role: z.string(),
    fonction: z.string(),
    specialites: z.array(z.string()),
    formation: z.string().optional(),
    photo: z.string(),
    photo_alt: z.string().min(5),
    ordre: z.number().int(),
    associe: z.boolean().default(true),
    contact_email: z.string().email().optional(),
  }),
});

const actualites = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/actualites' }),
  schema: z.object({
    titre: z.string().min(5).max(80),
    chapo: z.string().min(40).max(280),
    date: z.coerce.date(),
    auteur: z.string().optional(),
    image: z.string().optional(),
    image_alt: z.string().optional(),
    categories: z.array(z.enum([
      'Chantier en cours', 'Livraison', 'Événement', 'Article technique', 'Vie du cabinet',
    ])),
    en_avant: z.boolean().default(false),
    demo: z.boolean().default(false),
  }),
});

const secteurs = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/secteurs' }),
  schema: z.object({
    titre: z.string(),
    accroche: z.string().min(40).max(240),
    image: z.string(),
    image_alt: z.string().min(5),
    ordre: z.number().int(),
  }),
});

export const collections = { projets, expertises, equipe, actualites, secteurs };
