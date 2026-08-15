import type { CollectionEntry } from 'astro:content';
import fs from 'node:fs';
import path from 'node:path';

type Projet = CollectionEntry<'projets'>;

/**
 * Titre court d'une fiche — celui que porte sa PLANCHE, pas une seconde
 * rédaction.
 *
 * Le `titre` du frontmatter est une phrase descriptive calibrée pour le
 * référencement : « Néréa, 90 logements et un commerce à Aytré ». Elle tient
 * sur le `<h1>` de la fiche, où elle est à sa place. Partout ailleurs — carte
 * de projet, nomenclature, carte-lien de la vedette — elle nuit : le lieu y
 * est répété sur la ligne suivante, la carte monte à quatre lignes de
 * capitales, et la nomenclature TRONQUE (mesuré au navigateur : 14 titres
 * coupés sur 23, jusqu'à 103 px escamotés).
 *
 * Le titre court n'est pas à écrire : il existe depuis le chantier des
 * planches. C'est le champ `titre` du `planche.json`, deux à quatre mots,
 * relu par FT2E et déjà composé à 30 px sur chaque planche — « Néréa,
 * 90 logements ». Le lire ici plutôt que le recopier au frontmatter applique
 * la règle du modèle de contenu : *le `.md` dit qu'il y a une planche, la
 * planche dit ce qu'elle montre*. Une copie se désynchronise ; un original,
 * non.
 *
 * Lecture au BUILD (`output: 'static'`) : pas de fs côté client. Le fichier
 * est garanti présent — `planche` est obligatoire au schéma et `verser.py`
 * refuse un dossier incomplet. Une absence doit donc échouer bruyamment
 * plutôt que retomber sur le titre long, qui masquerait la rupture.
 */
export function titreCourt(projet: Projet): string {
  const json = path.join(process.cwd(), 'public',
    projet.data.planche.replace(/planche\.svg$/, 'planche.json'));
  const { titre } = JSON.parse(fs.readFileSync(json, 'utf-8'));
  if (!titre) {
    throw new Error(
      `titreCourt : « ${projet.id} » — le planche.json ne porte pas de `
      + `\`titre\`. C'est lui qui sert de titre court aux cartes et à la `
      + `nomenclature (voir .claude/rules/content-collections.md).`);
  }
  return titre;
}

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
