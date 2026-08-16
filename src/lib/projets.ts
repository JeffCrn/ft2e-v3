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
 * Localisation publique d'une affaire : **la commune et son code postal, et
 * rien d'autre** (2026-08-15).
 *
 * Le champ `lieu` du frontmatter va de la commune nue — « Aytré (17440) » —
 * à l'adresse de chantier complète — « 23 quai Valin, Vieux Port sud,
 * La Rochelle (17000), Charente-Maritime ». Cette latitude sert la fiche
 * d'affaire, pas l'affichage : en pied de carte, l'adresse longue occupe
 * trois lignes de mono pour une information que personne ne vient chercher
 * là, et elle repousse la chronologie hors de vue.
 *
 * La commune est le segment qui porte le code postal — c'est vrai des
 * vingt-trois fiches, contrôlé au corpus. La fonction échoue bruyamment
 * plutôt que de rendre l'adresse brute : un repli silencieux réintroduirait
 * dans une carte la ligne de trois lignes qu'on venait d'en chasser, et
 * seule une fiche sur vingt-trois le montrerait.
 *
 * Elle était jusqu'ici recopiée dans `references/[...slug].astro` sous le nom
 * `ville` ; c'est le même segment, une seule implémentation.
 */
export type Commune = {
  /** « La Rochelle » — le nom seul, pour la légende de média (§ 13, A8). */
  ville: string;
  /** « La Rochelle (17000) » — la forme d'affichage. */
  libelle: string;
};

export function commune(lieu: string): Commune {
  const trouve = lieu.match(/([^,]+?)\s*\((\d{5})\)/);
  if (!trouve) {
    throw new Error(
      `commune : « ${lieu} » ne porte pas de code postal à cinq chiffres. `
      + `C'est lui qui délimite le segment de commune ; sans lui, l'adresse `
      + `de chantier passerait entière en pied de carte `
      + `(voir .claude/rules/content-collections.md).`);
  }
  return { ville: trouve[1].trim(), libelle: `${trouve[1].trim()} (${trouve[2]})` };
}

/**
 * Millésime de livraison annoncé pour une affaire dont la réception n'est
 * pas encore prononcée.
 *
 * **C'est une décision éditoriale, pas une donnée** (2026-08-15, demande
 * FT2E) : le site annonce une livraison uniforme plutôt que d'afficher
 * « en cours ». Le frontmatter, lui, n'est pas touché — `annee_livraison`
 * reste vide sur ces quatorze affaires et le schéma continue d'interdire de
 * la renseigner tant que `statut` vaut « en cours » (règle 10). La
 * distinction survit donc dans la donnée ; c'est l'affichage seul qui
 * l'uniformise, et c'est réversible d'une ligne.
 *
 * ⚠ **Cette constante ne se met pas à jour toute seule.** Elle sera fausse au
 * 1ᵉʳ janvier 2027 sans que rien ne le signale — ni le build, ni le
 * typecheck, ni le rendu.
 */
export const MILLESIME_LIVRAISON_ANNONCE = 2026;

// Le garde-fou de l'échéance (2026-08-16). La constante ci-dessus est datée ;
// sans ce test, elle deviendrait fausse sur quatorze affaires au 1ᵉʳ janvier
// 2027 sans que rien ne le signale — ni le build, ni le typecheck, ni le rendu,
// puisque `2026` reste une chaîne parfaitement valide à afficher.
//
// L'échec est DUR, et c'est l'arbitrage : le dépôt fait déjà échouer
// bruyamment `commune()` et `titreCourt()` plutôt que de servir un repli
// silencieux. Une échéance qui n'arrête rien n'est pas une échéance.
if (new Date().getFullYear() > MILLESIME_LIVRAISON_ANNONCE) {
  throw new Error(
    `MILLESIME_LIVRAISON_ANNONCE vaut ${MILLESIME_LIVRAISON_ANNONCE}, or nous ` +
      `sommes en ${new Date().getFullYear()} : les affaires sans réception ` +
      'prononcée annonceraient une livraison passée. À faire, dans cet ordre — ' +
      'relever auprès de FT2E les réceptions désormais prononcées, renseigner ' +
      'leur `annee_livraison` (le schéma l’exige dès que `statut` ne vaut plus ' +
      '« en cours »), puis porter cette constante au millésime annoncé. ' +
      'Voir src/lib/projets.ts et la § « Localisation et chronologie » de CLAUDE.md.',
  );
}

/**
 * Chronologie publique d'une affaire — l'unique implémentation de la règle
 * (ADR-003). Le numéro d'affaire et le millésime d'ouverture sont une
 * nomenclature interne : ils ne s'affichent plus nulle part.
 *
 * Depuis le 2026-08-15, ce que le public lit est **toujours une livraison** :
 * le millésime de réception quand elle est prononcée, le millésime annoncé
 * sinon (voir `MILLESIME_LIVRAISON_ANNONCE`). Le libellé « statut » et le mot
 * « en cours » ne s'affichent plus.
 *
 * La décision se prend ici et seulement ici : tout consommateur qui a
 * besoin d'un couple étiquette/valeur passe par `chronologie`, tout
 * consommateur qui a besoin d'une chaîne plate passe par
 * `libelleChronologie`. Dupliquer le test `annee_livraison ? … : …`
 * ailleurs, c'est rouvrir l'incohérence que l'ADR referme.
 */
export type Chronologie = {
  label: 'livraison';
  valeur: string;
};

export function chronologie(projet: Projet): Chronologie {
  const { annee_livraison } = projet.data;
  return {
    label: 'livraison',
    valeur: String(annee_livraison ?? MILLESIME_LIVRAISON_ANNONCE),
  };
}

/** Rendu plat de la chronologie : « livraison 2026 ». */
export function libelleChronologie(projet: Projet): string {
  const { label, valeur } = chronologie(projet);
  return `${label} ${valeur}`;
}
