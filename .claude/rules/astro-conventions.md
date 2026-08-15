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
- `src/pages/references/index.astro` — filtres de nomenclature (guard `dataset.filtresBound`).

Citer les fonctions par **nom**, jamais par numéro de ligne : les lignes bougent à chaque refonte et la règle devient fausse sans que rien ne le signale. `Chiffre.astro` n'a plus de script — la v3 interdit les compteurs qui s'incrémentent (`.claude/rules/tailwind-design-tokens.md` § Interactions).

### Anti-pattern interdit

```astro
<script>
  // ❌ Casse après la 1ʳᵉ navigation View Transitions
  const el = document.querySelector('[data-mon-bouton]');
  el?.addEventListener('click', () => { … });
</script>
```

## Images optionnelles & fs.existsSync

**Portée réduite depuis le 2026-08-15.** Ce motif servait d'abord les visuels de fiches
projet ; ces fiches n'ont plus de visuel photographique — leur champ `image_principale` a
été retiré du modèle à la clôture du chantier des planches, et `planche` est devenu
obligatoire. Le motif ne concerne plus que les **photographies d'équipe**, dont les
fichiers arriveront au reportage professionnel et manquent aujourd'hui.

La règle, elle, ne change pas : un chemin d'image déclaré côté contenu sans que le fichier
soit présent dans `public/` produit une icône d'image cassée. Les composants qui rendent
ces images **vérifient la présence du fichier au build via `fs.existsSync`** et basculent
sur un placeholder en l'absence.

### Pattern de référence

```astro
---
import fs from 'node:fs';
import path from 'node:path';

const { membre } = Astro.props;
const photoExiste = fs.existsSync(path.join(process.cwd(), 'public', membre.data.photo));
---

{photoExiste ? (
  <img src={membre.data.photo} alt={membre.data.photo_alt}
       class="w-full h-full object-cover" loading="lazy" />
) : (
  <div class="duotone-media flex items-center justify-center">
    <p class="mono-label text-pivot">[Photo à venir]</p>
  </div>
)}
```

### Pourquoi ça marche

`fs.existsSync` s'exécute en **Node au moment de `astro build`**, puisque le projet est en
`output: 'static'`. Pas de fs côté client, pas de SSR. Si la stack bascule un jour en
SSR/edge runtime, il faudra refactorer vers `astro:assets` (`<Image>` qui gère sa propre
résolution build-time).

### Exemples dans le codebase

Citer par **nom de constante**, jamais par numéro de ligne — les lignes bougent.

- `src/pages/equipe.astro` — `collectifExiste`, et le pré-calcul `hasPhoto` des avatars.
- `src/pages/index.astro` — `collectifExiste` pour la photographie collective.

`src/pages/index.astro` emploie aussi `fs.readFileSync` pour **inliner l'appui de la fiche
vedette** : ce n'est pas le même motif — l'appui est produit par le protocole des planches
et sa présence est garantie par `verser.py`, il n'y a donc rien à tester.

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
│   └── projets.ts                # tri de nomenclature, libellé de référence
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
