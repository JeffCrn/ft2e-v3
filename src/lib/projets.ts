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
 * Chronologie publique d'une affaire — l'unique implémentation de la règle
 * (ADR-003). Le numéro d'affaire et le millésime d'ouverture sont une
 * nomenclature interne : ils ne s'affichent plus nulle part. Ce que le
 * public lit d'une affaire, c'est sa réception quand elle est prononcée,
 * et son statut sinon. Jamais rien d'autre, jamais de case vide.
 *
 * La décision se prend ici et seulement ici : tout consommateur qui a
 * besoin d'un couple étiquette/valeur passe par `chronologie`, tout
 * consommateur qui a besoin d'une chaîne plate passe par
 * `libelleChronologie`. Dupliquer le test `annee_livraison ? … : …`
 * ailleurs, c'est rouvrir l'incohérence que l'ADR referme.
 */
export type Chronologie = {
  label: 'livraison' | 'statut';
  valeur: string;
};

export function chronologie(projet: Projet): Chronologie {
  const { annee_livraison, statut } = projet.data;
  return annee_livraison
    ? { label: 'livraison', valeur: String(annee_livraison) }
    : { label: 'statut', valeur: statut };
}

/**
 * Rendu plat de la chronologie : « livraison 2024 » quand la réception est
 * prononcée, le statut nu (« en cours », « archive ») sinon — le mot
 * « statut » n'apporterait rien en ligne courante, là où « livraison »
 * qualifie son millésime.
 */
export function libelleChronologie(projet: Projet): string {
  const { label, valeur } = chronologie(projet);
  return label === 'livraison' ? `livraison ${valeur}` : valeur;
}
