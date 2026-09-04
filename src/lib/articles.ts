import { getCollection, type CollectionEntry } from 'astro:content';

type Article = CollectionEntry<'actualites'>;

/**
 * Le cocon sémantique : quels articles une page pilier met en avant.
 *
 * `.claude/rules/seo-geo.md` demande que chaque page pilier — les quatre
 * expertises et les sept secteurs — lie 3 à 5 articles satellites. Mesuré le
 * 2026-09-04 avant ce module : ZÉRO lien pilier → article sur les onze pages,
 * la règle existait sans rien pour la porter.
 *
 * LE SENS DE LA RELATION EST UN ARBITRAGE, pas un détail d'implémentation
 * (rendu le 2026-09-04). Le lien se déclare UNE SEULE FOIS, sur l'article, au
 * champ `piliers` ; les pages piliers ramassent ce qui les désigne. L'autre
 * dessin — un champ `articles_lies` sur `expertises` et `secteurs`, doublant
 * la déclaration — a été écarté : le dépôt a déjà refusé deux fois cette
 * forme (titre court de planche, alternative de vignette), au motif que
 * c'est TOUJOURS la copie, jamais l'original, qui se désynchronise. Ne pas
 * la réintroduire pour gagner la maîtrise de l'ordre d'affichage : cet ordre
 * est calculé ci-dessous, et il est dérivé du contrat du champ.
 */

/**
 * Plafond d'affichage sur une page pilier — la borne haute de `seo-geo.md`.
 * Les six articles de lancement n'en approchent aucune page ; le plafond
 * n'est donc pas là pour couper aujourd'hui, mais pour que la page ne se
 * transforme pas en index d'actualités le jour où le fonds grossit. Le pied
 * d'une page pilier est un renvoi, pas une liste.
 */
const MAX_SATELLITES = 5;

/**
 * Les onze chemins de page pilier, relevés SUR LE DISQUE et non recopiés.
 *
 * ⚠ C'est délibérément une seconde lecture, indépendante de l'énumération
 * `PILIERS` de `src/content.config.ts`. Les deux ne gardent pas la même
 * chose : l'énumération Zod empêche un rédacteur de saisir un pilier qui
 * n'existe pas — elle protège la saisie ; cette liste-ci est confrontée aux
 * fichiers réellement présents — elle protège du RENOMMAGE d'une page, que
 * l'énumération ne verrait pas passer.
 *
 * Comparer l'énumération à une copie de l'énumération n'aurait rien mesuré.
 */
async function cheminsDePilier(): Promise<Set<string>> {
  const [expertises, secteurs] = await Promise.all([
    getCollection('expertises'),
    getCollection('secteurs'),
  ]);
  return new Set([
    ...expertises.map((e) => `/expertises/${e.id}`),
    ...secteurs.map((s) => `/secteurs/${s.id}`),
  ]);
}

/**
 * Les articles satellites d'une page pilier, du plus pertinent au moins.
 *
 * L'ordre applique le contrat du champ `piliers` : sa PREMIÈRE entrée est le
 * pilier principal, celui dont l'article est le satellite au sens du PDF de
 * proposition ; les suivantes sont des rattachements secondaires. Les
 * articles dont `chemin` est le pilier principal passent donc devant, chaque
 * groupe étant classé du plus récent au plus ancien.
 *
 * Échec bruyant dans les deux sens, et c'est le point de ce module :
 *  — un article qui désigne un pilier absent du disque casse le build,
 *    plutôt que de disparaître silencieusement d'une page ;
 *  — une page pilier qui s'interroge sous un chemin inconnu casse le build,
 *    plutôt que d'afficher un bloc vide qu'aucune recette ne distinguerait
 *    d'un « pas encore d'article ».
 *
 * Un lien mort de cocon ne se voit pas : il ne produit ni 404 ni page cassée,
 * seulement une page pilier qui cesse de mailler. C'est précisément le genre
 * de panne muette dont ce dépôt a déjà payé le prix (classes Tailwind élaguées
 * par le `.gitignore`, OAuth Decap signalé en commentaire).
 */
export async function articlesDuPilier(chemin: string): Promise<Article[]> {
  const connus = await cheminsDePilier();

  if (!connus.has(chemin)) {
    throw new Error(
      `articlesDuPilier : « ${chemin} » ne correspond à aucune page de `
      + `\`expertises\` ni de \`secteurs\`. Soit la page a été renommée sans `
      + `que l'appel suive, soit elle vient d'être créée : dans les deux cas, `
      + `mettre à jour l'énumération \`PILIERS\` de src/content.config.ts ET `
      + `public/admin/config.yml, dans le même commit.`);
  }

  const articles = await getCollection('actualites');

  // `findIndex` et non `indexOf` : `piliers` est typé par l'énumération de
  // `content.config.ts`, et `indexOf` refuse alors un `string` — ts(2345).
  // C'est une bonne nouvelle, pas une gêne : elle prouve que le type de
  // l'énumération se propage jusqu'ici. Ce qui ne se resserre pas, c'est le
  // SITE D'APPEL — les pages passent `` `/expertises/${expertise.id}` ``, une
  // template string irréductiblement `string`. Typer le paramètre imposerait
  // un cast à chaque gabarit, c'est-à-dire remplacer la garantie par une
  // affirmation ; c'est le contrôle d'appartenance ci-dessus qui la porte.
  const rang = (a: Article) => (a.data.piliers ?? []).findIndex((p) => p === chemin);

  for (const article of articles) {
    for (const pilier of article.data.piliers ?? []) {
      if (!connus.has(pilier)) {
        throw new Error(
          `articlesDuPilier : l'article « ${article.id} » désigne le pilier `
          + `« ${pilier} », qui ne correspond à aucune page du site. Le cocon `
          + `sémantique serait rompu sans qu'aucune page ne le montre.`);
      }
    }
  }

  return articles
    .filter((a) => rang(a) !== -1)
    .sort((a, b) => {
      // Pilier principal (rang 0) avant rattachement secondaire.
      const principal = Number(rang(a) !== 0) - Number(rang(b) !== 0);
      return principal !== 0 ? principal : b.data.date.getTime() - a.data.date.getTime();
    })
    .slice(0, MAX_SATELLITES);
}
