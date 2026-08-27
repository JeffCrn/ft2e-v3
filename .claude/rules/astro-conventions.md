# Conventions Astro

**Scope** : tout fichier `.astro` et `src/**/*.ts`.

## Principes

- **Static-first.** Génération entièrement statique (`output: 'static'`). Pas de SSR sans ADR explicite.
- **Zero JS par défaut.** Tout composant interactif (`client:load`, `client:idle`, `client:visible`, `client:media`) doit être justifié dans le commit. Préférer `client:visible` ou `client:idle` à `client:load`.
- **Content Collections obligatoires** pour tout contenu (projets, actualités, équipe, services). Pas de données inlinées dans les composants `.astro`.
- **Image optimization** via `astro:assets` (composant `<Image>`). Format AVIF en priorité, WebP en fallback. Lazy par défaut sauf au-dessus du *fold*.
- **`<Fragment>`** plutôt qu'un `<div>` parasite.
- **Slots nommés** pour les layouts plutôt que props longues.
- **Frontmatter Astro** : déstructurer `Astro.props` avec des types explicites, jamais de `any`.

## Scripts client & View Transitions

`<ClientRouter />` est activé globalement dans `BaseLayout.astro`. À chaque navigation interne, Astro **remplace le DOM** sans recharger les modules ES déjà exécutés. Conséquence : **un `<script>` de composant qui attache un `addEventListener` directement au chargement initial le perd dès la première navigation** — le nouveau bouton/élément du DOM est inerte et silencieusement inutilisable.

### Règle

Tout `<script>` d'un composant `.astro` qui appelle `addEventListener` doit :

1. Encapsuler son code dans une fonction `initX()` nommée.
2. L'appeler via `document.addEventListener('astro:page-load', initX)`.
3. Garder un guard `dataset` sur l'élément cible pour éviter le double-binding si l'événement est ré-émis.

### Pattern de référence

```astro
<button data-mon-bouton>…</button>

<script>
  function initMonBouton() {
    const el = document.querySelector<HTMLButtonElement>('[data-mon-bouton]');
    if (!el) return;
    if (el.dataset.bound) return;
    el.dataset.bound = '1';

    el.addEventListener('click', () => {
      // …
    });
  }

  document.addEventListener('astro:page-load', initMonBouton);
</script>
```

### Exemples dans le codebase

- `src/layouts/BaseLayout.astro` — `initPlans` (révélation de plan, `data-plan`).
- `src/components/layout/Header.astro` — `initMenu` (menu mobile).
- `src/pages/references/index.astro` — `initFiltres`, filtres par secteur de la grille de références (guard `dataset.filtresBound`).

Citer les fonctions par **nom**, jamais par numéro de ligne : les lignes bougent à chaque refonte et la règle devient fausse sans que rien ne le signale. `Chiffre.astro` n'a plus de script ; l'unique compteur du site est `initCompteurs` dans `src/pages/index.astro` (amendement A14 du 2026-08-27 — tout autre compteur reste interdit, `.claude/rules/tailwind-design-tokens.md` § Interactions).

### Anti-pattern interdit

```astro
<script>
  // ❌ Casse après la 1ʳᵉ navigation View Transitions
  const el = document.querySelector('[data-mon-bouton]');
  el?.addEventListener('click', () => { … });
</script>
```

## Photographies optionnelles — le glob remplace `fs.existsSync` (2026-08-16)

**`fs.existsSync` n'est plus le motif des photographies.** Il testait la présence d'un
fichier dans `public/` ; les huit photographies d'équipe ont quitté `public/` pour
`src/assets/equipe/`, et un `import.meta.glob` fait désormais **les deux métiers à la
fois** — résoudre l'image *et* signaler son absence.

### Pourquoi le déplacement, et pas seulement un `<Image>`

`astro:assets` ne traite que ce qu'il **résout au build depuis `src/`**. `public/` est
recopié tel quel : ce n'est pas un pipeline, c'est un répertoire. Envelopper un
`<img src="/images/…">` dans `<Image>` n'aurait donc rien produit — ni AVIF, ni WebP,
ni `srcset`. Mesuré avant migration : `/equipe/` pesait **4 766 Kio** pour huit JPEG
bruts de 452 à 846 Ko. Après : **243 Kio**.

**Le champ Zod n'a pas bougé.** Le frontmatter continue de nommer
`/images/equipe/mathieu.jpg` — la graphie que documente
`content-models/membre-equipe.schema.md`, qu'écrit Decap et que relit FT2E. Elle décrit
ce que le visiteur verra, pas où le fichier dort dans le dépôt : **c'est au rendu
d'apprendre à la résoudre**, pas au contenu de connaître l'arborescence des sources.

### Pattern de référence

Le résolveur vit une fois pour toutes dans `src/lib/photos.ts` :

```ts
const modules = import.meta.glob<{ default: ImageMetadata }>(
  '../assets/equipe/*.{jpg,jpeg,png,webp,avif}',
  { eager: true },          // sans `eager`, le glob rend des imports asynchrones
);                          // que <Picture> ne peut pas consommer au build

export function photoEquipe(chemin: string): ImageMetadata | null { … }
```

et la page l'appelle :

```astro
---
import { Picture } from 'astro:assets';
import { photoEquipe } from '../lib/photos';

const photo = photoEquipe(membre.data.photo);   // null si le fichier manque
---

<div class:list={['aspect-[3/2]', photo ? 'duotone-photo' : 'duotone-media']}>
  {photo && (
    <Picture src={photo} formats={['avif', 'webp']}
             widths={[200, 400, 660]}
             sizes="(min-width: 1280px) 164px, (min-width: 768px) 25vw, 50vw"
             alt={membre.data.photo_alt}
             class="w-full h-full object-cover" loading="lazy" />
  )}
</div>
```

**Un seul mécanisme pour deux métiers** : l'absence d'entrée dans le glob *est* l'absence
de fichier. Le code précédent en tenait deux en cohérence — `fs.existsSync` pour tester,
une chaîne pour servir. Il n'y a donc plus de garde-fou à maintenir à côté de ce qu'il
garde.

⚠ **Le repli est la hachure `duotone-media`, PAS un libellé.** La version antérieure de
cette règle montrait un « [Photo à venir] » qu'**aucune page n'a jamais rendu** : les
trois emplacements se contentaient d'un plan vide. La règle décrit maintenant le code.
Ne pas « rétablir » le libellé sans arbitrage — le site est en démonstration client, et
une hachure se lit comme un placeholder dessiné là où un libellé se lit comme un site
inachevé.

### `<Picture>` casse le duotone si l'on n'y prend pas garde

`<Picture>` interpose un `<picture>` entre le plan et son image — c'est le prix de
l'AVIF. Or `global.css` écrit le duotone en **sélecteur d'enfant direct**
(`.duotone-photo > img`). Deux conséquences, dont **aucune ne se signale au build** :

1. le sélecteur cesse de mordre → le duotone tombe et **les couleurs natives
   reviennent**, ce que la charte interdit ;
2. le `h-full` de l'image se résout contre un parent inline de hauteur auto → la mise
   en page tombe.

Les deux se règlent ensemble dans `global.css` : `.duotone-photo > picture { display:
contents }` (retire le `<picture>` de la mise en page sans le retirer du DOM) et
`.duotone-photo > picture > img` ajouté au sélecteur. **Se contrôle en computed style,
pas à l'œil** — `filter: grayscale(1) contrast(1.05)` et `mix-blend-mode: lighten` sur
l'image, `display: contents` sur le `<picture>`.

### La photographie collective est rendue à TROIS endroits

`src/pages/index.astro`, `src/pages/equipe.astro` **et** `src/pages/societe.astro`
(bandeau 21:8). Les trois passent par la constante `CHEMIN_COLLECTIF` de
`src/lib/photos.ts` : le chemin n'est plus recopié, et c'est par là que la troisième
occurrence pouvait être manquée.

**Seul `/equipe/` charge sa photographie en `eager` + `fetchpriority="high"`** — c'est
le seul des trois où elle est au-dessus de la ligne de flottaison, et Lighthouse la
désigne comme l'élément LCP (audit `lcp-discovery-insight`, dont la checklist nomme
`eagerlyLoaded` et `priorityHinted`). Ailleurs elle est loin en bas et reste en `lazy`.

### Ce qui reste du motif `fs`

`src/pages/index.astro` n'emploie plus `fs.readFileSync` depuis le 2026-08-26 : le
hero est passé de l'appui inliné de la fiche vedette à un cliché du corpus secteurs,
résolu par le glob de `photos.ts` comme toute photographie. Reste
`src/lib/projets.ts` (`titreCourt`), qui lit un `planche.json` garanti présent, et
**échoue bruyamment** en son absence. La différence avec les photographies est le
statut de l'absence : une planche manquante signale une rupture, une photographie
manquante est un état de production normal jusqu'au reportage.

## `interface Props` se déclare juste après les imports (2026-08-16)

Un composant `.astro` ne type ses appelants que si Astro reconnaît son
`interface Props`. Quand la reconnaissance échoue, `Astro.props` retombe sur
`Record<string, any>` et **plus rien n'est contrôlé** : un prop inexistant passe,
un prop requis manquant passe. Le build est vert, le rendu est juste, et le seul
signe est un **hint** d'`astro check`.

### Le hint ment sur ce qu'il désigne

```
warning ts(6196): 'Props' is declared but never used.
```

Il se lit « code mort ». Il dit en réalité « **contrat non consommé** », ce qui est
l'inverse d'un surplus : l'interface est correcte et utile, c'est le fil qui est
coupé. Constaté sur `PlancheReference.astro` le 2026-08-16, où la programmation de
dette l'avait classé parmi le code à supprimer — le supprimer aurait entériné
l'absence de contrôle sur ses deux appelants.

### La règle

**Déclarer `interface Props` immédiatement après les `import`**, avant tout bloc de
commentaire de composant. Le long commentaire de dessin vient ensuite.

⚠ **La cause du débranchement n'est pas caractérisée**, et deux explications
plausibles ont été écartées par la mesure : ce n'est ni la longueur du commentaire
(`MarqueOpqibi` en porte 3 771 signes au même endroit, `CarteProjet` a le motif
exact — imports, commentaire, interface —, et les deux sont branchés), ni sa nature
JSDoc, ni une balise `<img src>` citée dedans. Ce qui est établi : dans le seul cas
observé, déclarer l'interface en tête réparait. La règle est donc une **précaution
vérifiée**, pas une explication.

### La sonde — et la façon de la rater

Pour vérifier qu'un composant type bien ses appelants, **remplacer** la valeur d'un
prop existant par une valeur invalide, puis `npm run typecheck` :

```astro
<CarteProjet projet="PAS-UN-PROJET" />   <!-- doit lever ts(2322) -->
```

⚠ **Jamais en AJOUTANT un second attribut** : un attribut dupliqué ne lève aucune
erreur, et la sonde conclut « zéro erreur » sur un composant parfaitement sain. Une
sonde qui ne peut pas échouer ne mesure rien. C'est ainsi que `MarqueOpqibi` a été
déclaré atteint à tort le 2026-08-16.

Un composant sain, pris pour témoin, fait partie de la sonde : sans lui, « zéro
erreur » se lit comme « tout va bien ».

## Une couleur s'écrit en classe, jamais en `var()` dans un attribut (2026-08-16)

**Tailwind v4 n'émet dans `:root` que les variables de thème qu'une classe emploie.**
Mesuré : le CSS produit ne porte aucune des couleurs par défaut de Tailwind, et
exactement les treize de la rampe — celles que des utilitaires appellent.

Conséquence pour un SVG inliné dans un composant : `stroke="var(--color-voile)"`
**échappe au scan**. La variable n'existe alors dans `:root` que si un *autre*
composant emploie `text-voile` ou `bg-voile` quelque part sur la page. Le jour où
celui-ci change, le dessin perd ses couleurs — et rien ne le signale : ni le build,
ni le typecheck, ni le CSS, qui reste valide.

```astro
<path class="stroke-pivot" d="…" />              <!-- ✅ littéral, donc scanné -->
<path stroke="var(--color-pivot)" d="…" />       <!-- ❌ invisible au scan -->
<path class={`stroke-${teinte}`} d="…" />        <!-- ❌ construit, donc invisible -->
```

Le nom de classe doit être **littéral dans la source** : une table de correspondance
(`{ principal: 'stroke-pivot', … }`) convient, une concaténation non. Contrôle :
`grep -o "\.stroke-pivot{[^}]*}" dist/_astro/*.css` doit rendre la règle.

C'est la même famille que le piège `.gitignore` (§ « Tailwind v4 — détection de
sources » plus bas) — dans les deux cas,
Tailwind ne signale jamais ce qu'il n'a pas vu.

## Les fins de ligne sont figées par `.gitattributes` (2026-08-16)

Le dépôt porte `* text=auto eol=lf`. **Ne pas le retirer.** Sans lui, et avec
`core.autocrlf=true` sous Windows, un **clone neuf** sort les 92 pièces des planches
(69 SVG + 23 JSON) en CRLF, alors que les compositeurs écrivent du LF
(`newline="\n"`). La première régénération les réécrit toutes, et **l'invariant
« 23 / 23 octet à octet » du protocole se lit comme rompu alors qu'il tient.**

⚠ Le piège est invisible sur la machine qui a produit le corpus — les fichiers y sont
nés en LF. Il n'apparaît qu'après un clone, c'est-à-dire quand quelqu'un reprend le
chantier, et il se présente alors comme une rupture d'invariant. **Ne jamais conclure
« l'invariant est rompu » sur une machine fraîchement clonée sans avoir vérifié les
fins de ligne d'abord.**

## Structure attendue

```
src/
├── content.config.ts             # Zod schemas de toutes les collections (À LA RACINE de src/,
│                                 #   PAS src/content/config.ts)
├── content/
│   ├── projets/*.md
│   ├── actualites/*.md
│   ├── equipe/*.md
│   ├── expertises/*.md
│   └── secteurs/*.md
├── lib/
│   ├── constants.ts              # constantes de site (nav, chiffres clés, JSON-LD)
│   └── projets.ts                # tri des affaires, titre court, commune, chronologie
├── layouts/
│   ├── BaseLayout.astro          # html/head/body, meta, fonts, révélation de plan
│   └── PageLayout.astro          # header + footer wrapper
├── pages/
│   ├── index.astro               # accueil
│   ├── societe.astro
│   ├── equipe.astro
│   ├── expertises/               # les quatre métiers
│   │   ├── index.astro
│   │   └── [...slug].astro
│   ├── secteurs/                 # les sept secteurs d'activité
│   │   └── [...slug].astro
│   ├── references/
│   │   ├── index.astro           # liste filtrable
│   │   └── [slug].astro          # fiche projet (getStaticPaths)
│   ├── actualites/
│   │   ├── index.astro
│   │   └── [slug].astro
│   └── contact.astro
└── components/
    ├── primitives/               # Bouton, Chiffre, CoinsCuivre, TraceFlux, BadgeDemo
    ├── blocs/                    # blocs de page (Hero, HeroPage, PlancheReference, etc.)
    └── layout/                   # Header, Footer, Navigation
```

## Conventions de nommage

- Composants : **PascalCase** (`FicheTechnique.astro`).
- Variables et fonctions : **camelCase**.
- Fichiers de contenu (slugs) : **kebab-case sans accents** (`abbaye-sablonceaux-ssi.md`).
- Classes Tailwind : **regrouper logiquement** (layout → spacing → typo → couleur → état).

## Design system — où est la source de vérité

**Source de vérité unique : `.claude/rules/tailwind-design-tokens.md` (charte v3 « plans et profondeur »)**, appuyée sur `src/styles/global.css` (bloc `@theme` + `@layer components`). Pas de `tailwind.config.ts`.

Ne rien déduire d'un autre fichier. En particulier, `docs/02-design-system.md` décrit la **v1 Apple-style** (conteneur 980 px, boutons pilule `rounded-[980px]`, sections noir/blanc alternées, cartes `rounded-lg` + `shadow-soft`) : c'est de l'**historique**, entièrement contredit par la v3 (rayon 0 partout, conteneur 1200 px sur planche 1440 px, aplat encre, trois rangs d'ombre). Les tokens `pure-black`, `light-gray`, `near-black`, `shadow-soft` ne subsistent dans `global.css` que comme **alias repointés** — aucun composant ne les emploie, et le nouveau code ne doit pas les employer.

## Tailwind v4 — détection de sources et `.gitignore`

**La détection automatique de sources de Tailwind v4 lit le `.gitignore` du dépôt et élague les répertoires qui y correspondent.** Elle n'a aucune notion de « fichier suivi par git ».

Conséquence : **tout motif `.gitignore` non ancré désactive silencieusement la génération des classes d'un répertoire source homonyme.** `references/` (sans barre oblique initiale) s'applique à tous les niveaux — donc aussi à `src/pages/references/`, dont les classes cessent d'être émises. Le build reste vert : Tailwind ne signale jamais une classe qu'il n'a pas vue ; seul le rendu le montre.

### Règles

1. **Ancrer tout motif** ajouté au `.gitignore` : `/references/`, `/cv/`, `/assets/` — jamais `references/`.
2. Après toute modification du `.gitignore`, vérifier : `git check-ignore -v src/pages/<dossier>/index.astro` doit **ne rien renvoyer**.
3. **Ne jamais conclure sur un build vert seul** après un changement de `.gitignore` ou de mise en page : contrôler le rendu (voir § Vérification du rendu).
4. Diagnostic d'une classe manquante : comparer les sélecteurs de `dist/_astro/*.css` au source. Une classe en valeur arbitraire présente au source et absente du CSS = répertoire non scanné.

Incident du 2026-08-08 (commits `0cb0d35` → `f8bf542`) : `references/` non ancré a supprimé `grid-cols-[56px_1fr_150px_88px_104px_56px]`, `grid-cols-[1fr_auto]` et `min-w-0` du CSS ; la nomenclature de `/references` s'est dépliée en blocs pleine largeur pendant quatre déploiements.

**Piège annexe** : les répertoires non suivis présents en local (`branding-v2/`, `branding-v3/`, `plaquette/`) **sont** scannés par Tailwind et gonflent le CSS local de classes absentes en production. Comparer la taille du CSS local à celle de Vercel n'a donc aucun sens tel quel — comparer les **sélecteurs**, pas les octets.

## Vérification du rendu — obligatoire avant de conclure

Un build vert prouve que le projet compile, **pas que la page s'affiche**. Avant d'annoncer qu'un changement fonctionne, et systématiquement après une modification de mise en page, de `global.css` ou du `.gitignore` :

```bash
npm run build && npm run preview   # puis capture de la page touchée
```

Contrôler la page réellement modifiée (Playwright ou navigateur), pas seulement la page d'accueil. Les deux incidents du 2026-08-08 ont franchi un build vert.

## Performances — critères de blocage

⚠ **Où se mesurent-ils : sur le déploiement, jamais sur `npm run preview`.**
`astro preview` sert **tout sans compression** — aucun en-tête `Content-Encoding` —
là où Vercel sert le HTML et le CSS en **brotli**. Sous le throttling simulé de
Lighthouse, les 48 Kio de CSS non compressés se paient sur le chemin bloquant et
gonflent FCP et LCP d'environ **0,8 s**. Mesuré le 2026-08-16 sur `/equipe/` :
preview 98 / LCP 2,2 s contre déploiement **100 / LCP 1,2 s**, pour un HTML identique.

Le biais porte précisément sur la chaîne bloquante, c'est-à-dire là où l'on cherche
à conclure : une session entière a failli être livrée sur le constat « le critère
n'est pas atteignable », en accusant une police qui pesait le même nombre d'octets
des deux côtés. **`npm run preview` reste l'instrument du rendu** (§ Vérification du
rendu, inchangé) ; il n'est pas celui de la performance.

```bash
# Avant de mesurer : vérifier que le déploiement porte bien le commit en cours,
# par un MARQUEUR DU BUILD et non par un délai d'attente.
# ⚠ `grep -o … | wc -l` et NON `grep -c` : le HTML est minifié sur peu de lignes,
#   et `grep -c` compte les lignes, pas les occurrences.
curl -s https://ft2e-v3.vercel.app/equipe/ | grep -o 'type="image/avif"' | wc -l   # 8 attendus

npx lighthouse https://ft2e-v3.vercel.app/equipe/ --only-categories=performance \
  --form-factor=mobile --screenEmulation.mobile --quiet
```

Si l'un de ces critères n'est pas tenu, **ne pas merger** :

- LCP mobile (4G, Moto G4) < 1.8 s
- CLS < 0.05
- Total Blocking Time < 200 ms
- JS initial transmis (gzip) < 50 KB sur la page d'accueil, < 30 KB sur les autres pages
- Aucune police custom au-dessus du *fold* sans `font-display: swap`

## Tests à exécuter

```bash
npm run typecheck   # astro check (`npm run lint` en est un alias — inutile de lancer les deux)
npm run build       # build prod (échec = blocage)
npm run preview     # + capture de la page modifiée (§ Vérification du rendu)
```
