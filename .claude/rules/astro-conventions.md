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

Citer les fonctions par **nom**, jamais par numéro de ligne : les lignes bougent à chaque refonte et la règle devient fausse sans que rien ne le signale. `Chiffre.astro` n'a plus de script — la v3 interdit les compteurs qui s'incrémentent (`.claude/rules/tailwind-design-tokens.md` § Interactions).

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

`src/pages/index.astro` emploie encore `fs.readFileSync` pour **inliner l'appui de la
fiche vedette** : ce n'est pas le même motif — l'appui est produit par le protocole des
planches et sa présence est garantie par `verser.py`, il n'y a donc rien à tester.
De même `src/lib/projets.ts` (`titreCourt`) lit un `planche.json` garanti présent, et
**échoue bruyamment** en son absence. La différence avec les photographies est le
statut de l'absence : une planche manquante signale une rupture, une photographie
manquante est un état de production normal jusqu'au reportage.

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
