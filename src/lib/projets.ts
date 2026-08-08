import type { CollectionEntry } from 'astro:content';

type Projet = CollectionEntry<'projets'>;

/**
 * Ordre de nomenclature : affaire la plus récente d'abord.
 *
 * `annee` seule ne suffit pas à ordonner — plusieurs affaires s'ouvrent
 * la même année, et le tri retombait alors silencieusement sur l'ordre
 * alphabétique de `getCollection`. Le numéro d'affaire départage (le rang
 * dans l'année est chronologique), le titre en dernier recours pour les
 * fiches de démonstration, qui n'en portent pas.
 */
export function parAffaireDecroissante(a: Projet, b: Projet): number {
  return (
    b.data.annee - a.data.annee ||
    (b.data.reference ?? '').localeCompare(a.data.reference ?? '') ||
    a.data.titre.localeCompare(b.data.titre, 'fr')
  );
}

/**
 * Référence affichable. Les fiches de démonstration n'ont pas de numéro
 * d'affaire — on affiche un tiret plutôt qu'un numéro fabriqué, qui
 * entrerait en collision avec une affaire réelle.
 */
export function libelleReference(projet: Projet): string {
  return projet.data.reference ?? '—';
}
