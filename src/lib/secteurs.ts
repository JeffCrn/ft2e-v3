import type { CollectionEntry } from 'astro:content';

/** Un cliché du corpus d'un secteur, tel que le valide le schéma Zod. */
export type ClicheSecteur = CollectionEntry<'secteurs'>['data']['cliches'][number];

/** La cote de conception du film : quatre clichés (maquette 2b, § 07). */
export const TAILLE_FILM = 4;

/** Mélange de Fisher-Yates, en place. */
function melange<T>(liste: T[]): T[] {
  for (let i = liste.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [liste[i], liste[j]] = [liste[j], liste[i]];
  }
  return liste;
}

/**
 * Tire le film d'un secteur dans son corpus — arbitrage D du 2026-08-25 :
 * le tirage est aléatoire et vit AU BUILD. Chaque déploiement recompose
 * les films ; entre deux déploiements, l'affichage est stable, aucun
 * JavaScript côté client n'est en jeu et seuls les clichés tirés sont
 * optimisés et servis.
 *
 * Deux contraintes, dans cet ordre :
 * 1. chaque `famille` présente dans le corpus place au moins un
 *    représentant (tiré au hasard dans la famille) ;
 * 2. le complément est tiré dans le reste du corpus, toutes familles
 *    confondues.
 * L'ordre de sortie est lui-même mélangé : le premier cliché du film est
 * celui que la tranche ouverte sert, et il change donc à chaque build.
 *
 * Un corpus plus petit que la taille demandée rend un film plus court
 * (les Études d'exécution portent trois clichés : leur film est de
 * trois) — la pièce tient de trois à six sans redessin (maquette § 07).
 */
export function filmSecteur(cliches: ClicheSecteur[], taille = TAILLE_FILM): ClicheSecteur[] {
  const parFamille = new Map<string, ClicheSecteur[]>();
  const sansFamille: ClicheSecteur[] = [];
  for (const cliche of cliches) {
    if (cliche.famille) {
      const groupe = parFamille.get(cliche.famille) ?? [];
      groupe.push(cliche);
      parFamille.set(cliche.famille, groupe);
    } else {
      sansFamille.push(cliche);
    }
  }

  const retenus: ClicheSecteur[] = [];
  const reste: ClicheSecteur[] = [...sansFamille];
  for (const groupe of parFamille.values()) {
    const i = Math.floor(Math.random() * groupe.length);
    retenus.push(groupe[i]);
    reste.push(...groupe.filter((_, j) => j !== i));
  }

  melange(reste);
  while (retenus.length < taille && reste.length > 0) {
    retenus.push(reste.pop() as ClicheSecteur);
  }

  // Plus de familles que de places : cas absent du corpus actuel (trois
  // familles au plus pour quatre places) — on tronque après mélange pour
  // ne pas rendre un film trop long, en acceptant qu'une famille cède.
  return melange(retenus).slice(0, taille);
}
