import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

/**
 * Les sept secteurs d'activité de FT2E (message client du 2026-08-07,
 * cohérent avec la plaquette 2024) : quatre marchés du bâtiment, puis
 * trois modes d'intervention que le bureau porte comme segments à part
 * entière — monotechnique, coordination SSI, études d'exécution / BIM.
 */
const SECTEURS = [
  'Logements',
  'Tertiaire / ERP',
  'Industriel et commercial',
  'Patrimoine',
  'Monotechnique',
  'Coordination SSI',
  "Études d'exécution / BIM",
] as const;
/**
 * Typologies d'intervention. Les trois premières décrivent des travaux sur
 * l'ouvrage ; les deux dernières, une mission d'étude sans marché de travaux.
 *
 * `Étude` couvre l'intervention d'ingénierie sur un existant qui ne débouche
 * sur aucun chantier — audit énergétique, calcul de charges, faisabilité.
 * Sans elle, ces affaires étaient contraintes de s'annoncer en
 * `Réhabilitation`, ce qui annonçait des travaux qui n'ont pas eu lieu — et
 * le mot s'affiche en chip de filtre sur `/references`.
 */
const TYPOLOGIES = ['Neuf', 'Réhabilitation', 'Extension', 'Étude', "Études d'exécution"] as const;
const MISSIONS = ['CVC', 'Thermique', 'Électricité CFO', 'Électricité CFA', 'Photovoltaïque', 'SSI', 'BIM', "Études d'exécution", 'Audit & diagnostic'] as const;

const projets = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/projets' }),
  schema: z.object({
    titre: z.string().min(2).max(80),
    /**
     * Nom court de l'ouvrage — deux à quatre mots, celui par lequel on
     * désigne l'affaire. Il n'est PAS un raccourci du titre : `titre` est
     * une phrase descriptive faite pour le `<h1>` et les moteurs, `ouvrage`
     * est un nom.
     *
     * Il alimente le cartouche de légende du média (amendement A8 :
     * « ouvrage · ville · surface »), qui dispose de 32 signes sur une ligne
     * à 390 px. Découper le titre au premier séparateur ne suffisait pas :
     * la légende ainsi composée ne tenait que sur 1 fiche sur 19.
     *
     * Facultatif, et le rendu se replie sur le découpage du titre en son
     * absence — une fiche sans nom court reste publiable.
     */
    ouvrage: z.string().min(2).max(40).optional(),
    secteur: z.enum(SECTEURS),
    typologie: z.enum(TYPOLOGIES),
    moa: z.string().min(2),
    architecte: z.string().optional(),
    lieu: z.string().min(2),
    surface_m2: z.number().int().positive().optional(),
    /**
     * Numéro d'affaire FT2E, graphie `NN-NNN` : `NN` = millésime d'ouverture,
     * `NNN` = rang dans l'année. C'est la référence que portent les documents
     * du bureau (« Affaire n° : 22-033 ») et les cartouches de plans, et la
     * seule référence publiable. Obligatoire dès que `demo` vaut false : une
     * fiche réelle sans numéro d'affaire n'est pas traçable, et une fiche de
     * démonstration ne doit jamais exhiber un numéro fabriqué (il entrerait
     * en collision avec une affaire véritable).
     */
    reference: z.string().regex(/^\d{2}-\d{3}$/, 'Numéro d’affaire attendu au format NN-NNN (ex. 22-042)').optional(),
    /**
     * Millésime d'**ouverture de l'affaire**, celui qu'encode `reference`.
     * Ce n'est ni l'année de DCE ni celle de la réception : voir
     * `annee_livraison`. Sert de clé de tri de la nomenclature et de
     * `dateCreated` en JSON-LD.
     */
    annee: z.number().int().min(2008).max(new Date().getFullYear() + 1),
    /** Millésime de réception/livraison, renseigné seulement une fois la réception prononcée. */
    annee_livraison: z.number().int().min(2008).max(new Date().getFullYear() + 2).optional(),
    /** Rang de nomenclature (charte v3) : opacité du filet gauche 1 px — livré 22 % / en cours 16 % / archive 12 %. */
    statut: z.enum(['livré', 'en cours', 'archive']).default('livré'),
    /**
     * Synthèse de fiche : un texte autonome, qui se lit sans le récit et
     * sans le cartouche. Calibre 480–780 signes.
     *
     * Le champ ne s'appelle **pas** `chapo`, et le rang typographique Chapô
     * ne le compose pas : ce rang est plafonné à trois lignes et posé en
     * graisse 300. Un bloc de 480 à 780 signes n'y tient pas. Garder le nom
     * garantirait qu'on le recompose un jour dans un rang qui ne peut pas
     * le porter. Il est rendu au rang Corps, à 17 px.
     *
     * Le calibre est porté par le schéma et non par le seul `hint` Decap,
     * pour que le build refuse une synthèse hors bornes au lieu de la
     * laisser passer en production. Le plafond était à 680 : rédaction
     * faite, il coupait dans la substance. Porté à 780 le 2026-08-09.
     *
     * **Le plancher n'autorise aucun remplissage** : une fiche qui ne peut
     * pas atteindre 480 signes honnêtement reste sans synthèse. Le champ
     * est optionnel pour cette raison.
     */
    synthese: z.string().min(480).max(780).optional(),
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
  }).superRefine((data, ctx) => {
    if (!data.demo && !data.reference) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        path: ['reference'],
        message: 'Fiche réelle : le numéro d’affaire FT2E (NN-NNN) est obligatoire.',
      });
    }
    // Le numéro d'affaire encode déjà l'année d'ouverture : on refuse au build
    // toute fiche où les deux se contredisent.
    if (data.reference) {
      const attendue = 2000 + Number(data.reference.slice(0, 2));
      if (data.annee !== attendue) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          path: ['annee'],
          message: `L’affaire ${data.reference} a été ouverte en ${attendue} : « annee » doit valoir ${attendue} (année de réception → « annee_livraison »).`,
        });
      }
    }
    if (data.annee_livraison && data.annee_livraison < data.annee) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        path: ['annee_livraison'],
        message: 'La livraison ne peut pas précéder l’ouverture de l’affaire.',
      });
    }
    if (data.annee_livraison && data.statut === 'en cours') {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        path: ['annee_livraison'],
        message: 'Affaire « en cours » : ne pas annoncer une année de livraison avant réception prononcée.',
      });
    }
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
    /** Segments de type mission (Coordination SSI, EXE/BIM) : livrables et FAQ hérités des anciennes pages expertise. */
    livrables: z.array(z.string()).optional(),
    faq: z.array(z.object({
      question: z.string(),
      reponse: z.string(),
    })).optional(),
  }),
});

export const collections = { projets, expertises, equipe, actualites, secteurs };
