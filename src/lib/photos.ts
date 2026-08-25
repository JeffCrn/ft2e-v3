import type { ImageMetadata } from 'astro';

/**
 * Résolution des photographies d'équipe — le seul endroit du site où une
 * photographie est encore attendue (les fiches projet sont illustrées par
 * des planches depuis le 2026-08-15).
 *
 * ## Pourquoi les fichiers ont quitté `public/`
 *
 * `astro:assets` ne traite que ce qu'il RÉSOUT au build depuis `src/` :
 * `public/` est recopié tel quel, ce n'est pas un pipeline. Les huit JPEG
 * y étaient servis bruts — 4,6 Mio pour huit portraits, ni AVIF, ni WebP,
 * ni `srcset`. Les déplacer dans `src/assets/equipe/` est la condition,
 * pas un détail d'implantation : sans ce déplacement, envelopper les
 * `<img>` dans `<Picture>` n'aurait rien produit du tout.
 *
 * ## Pourquoi le champ Zod n'a pas bougé
 *
 * Le frontmatter continue de nommer `/images/equipe/mathieu.jpg`. C'est la
 * graphie que documente `content-models/membre-equipe.schema.md`, celle que
 * Decap écrit, et celle que FT2E relit. Elle décrit ce que le visiteur
 * verra, pas où le fichier dort dans le dépôt : c'est au RENDU d'apprendre
 * à la résoudre, pas au contenu de connaître l'arborescence des sources.
 *
 * ## Un seul mécanisme pour deux métiers
 *
 * Le code précédent en employait deux : `fs.existsSync` pour tester la
 * présence, une chaîne de caractères pour servir l'image. Le glob fait les
 * deux — **l'absence d'entrée EST l'absence de fichier**. Il n'y a donc
 * plus de garde-fou à tenir en cohérence avec ce qu'il garde.
 *
 * Le repli reste SILENCIEUX, contrairement à `titreCourt()` et `commune()`
 * qui échouent bruyamment. Ce n'est pas une incohérence : ces deux-là
 * lisent une pièce dont la présence est garantie (`verser.py` refuse un
 * dossier incomplet), donc une absence y signale une rupture. Ici les sept
 * portraits et la photographie collective sont des images de démonstration
 * qui SERONT remplacées au reportage photographique : leur absence est un
 * état de production normal, que la page doit traverser sans casser.
 *
 * `eager: true` est obligatoire — sans lui le glob rend des fonctions
 * d'import asynchrones, que `<Picture>` ne peut pas consommer au build.
 */
const modules = import.meta.glob<{ default: ImageMetadata }>(
  '../assets/equipe/*.{jpg,jpeg,png,webp,avif}',
  { eager: true },
);

/** La graisse du chemin public, telle que l'écrit le frontmatter. */
const PREFIXE_PUBLIC = '/images/equipe/';

const parChemin = new Map<string, ImageMetadata>(
  Object.entries(modules).map(([cle, mod]) => [
    PREFIXE_PUBLIC + cle.split('/').pop(),
    mod.default,
  ]),
);

/**
 * Résout le chemin porté par le frontmatter vers l'image importée.
 * Rend `null` quand le fichier manque — la page bascule alors sur le
 * placeholder `duotone-media` (« [Photo à venir] »).
 */
export function photoEquipe(chemin: string): ImageMetadata | null {
  return parChemin.get(chemin) ?? null;
}

/**
 * La photographie collective, rendue à TROIS endroits — `/`, `/equipe`
 * et `/societe`. Le plan de session n'en annonçait que deux ; la troisième
 * (bandeau 21:8 de `societe.astro`) a été relevée au dépôt. La constante
 * existe pour que le chemin ne soit plus recopié trois fois : c'était par
 * là que la troisième occurrence pouvait être manquée.
 */
export const CHEMIN_COLLECTIF = `${PREFIXE_PUBLIC}collectif.jpg`;

/**
 * Résolution des clichés de secteurs (chantier du bloc secteurs,
 * 2026-08-25) — même mécanique que l'équipe, à un niveau de dossier
 * près : un sous-dossier par slug de secteur. Le frontmatter écrit
 * `/images/secteurs/<slug>/<fichier>`, le glob résout depuis
 * `src/assets/secteurs/<slug>/`.
 *
 * Le repli est SILENCIEUX (null → hachure `duotone-media`), comme pour
 * l'équipe et conformément au § 09 de la maquette : une fiche éditée
 * dans Decap peut traverser un état où le fichier n'est pas encore
 * poussé, et la page doit traverser cet état sans casser.
 */
const modulesSecteurs = import.meta.glob<{ default: ImageMetadata }>(
  '../assets/secteurs/*/*.{jpg,jpeg,png,webp,avif}',
  { eager: true },
);

const PREFIXE_SECTEURS = '/images/secteurs/';

const secteursParChemin = new Map<string, ImageMetadata>(
  Object.entries(modulesSecteurs).map(([cle, mod]) => {
    const segments = cle.split('/');
    const fichier = segments[segments.length - 1];
    const slug = segments[segments.length - 2];
    return [`${PREFIXE_SECTEURS}${slug}/${fichier}`, mod.default];
  }),
);

/** Résout le chemin public d'un cliché de secteur ; null si le fichier manque. */
export function photoSecteur(chemin: string): ImageMetadata | null {
  return secteursParChemin.get(chemin) ?? null;
}
