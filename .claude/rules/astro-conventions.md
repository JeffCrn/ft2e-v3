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

- `src/layouts/BaseLayout.astro` lignes 200-208 (motion design : `initMotion`).
- `src/components/primitives/Chiffre.astro` ligne 73 (compteurs : `initChiffres`).
- `src/components/layout/Header.astro` lignes 68-83 (menu mobile : `initMenu`).

### Anti-pattern interdit

```astro
<script>
  // ❌ Casse après la 1ʳᵉ navigation View Transitions
  const el = document.querySelector('[data-mon-bouton]');
  el?.addEventListener('click', () => { … });
</script>
```

## Images optionnelles & fs.existsSync

Certaines fiches projet ont un champ `image_principale` rempli côté Zod (obligatoire) sans que le fichier physique soit déjà présent dans `public/`. Pour éviter les icônes d'image cassée visibles, les composants qui rendent ces images **doivent vérifier la présence du fichier au build via `fs.existsSync`** et basculer sur un placeholder en l'absence.

### Pattern de référence

```astro
---
import fs from 'node:fs';
import path from 'node:path';

const { projet } = Astro.props;
const { image_principale, image_principale_alt } = projet.data;

const imageExiste = fs.existsSync(path.join(process.cwd(), 'public', image_principale));
---

{imageExiste ? (
  <img
    src={image_principale}
    alt={image_principale_alt}
    class="w-full h-full object-cover"
    loading="lazy"
  />
) : (
  <div class="bg-dark-surface-1 flex items-center justify-center ...">
    <p class="text-white/40 text-sm">[Photo à venir]</p>
  </div>
)}
```

### Pourquoi ça marche

`fs.existsSync` s'exécute en **Node au moment de `astro build`**, puisque le projet est en `output: 'static'`. Pas de fs côté client, pas de SSR. Si la stack bascule un jour en SSR/edge runtime, il faudra refactorer vers `astro:assets` (`<Image>` qui gère sa propre résolution build-time).

### Exemples dans le codebase

- `src/components/blocs/CarteProjet.astro:14-17` — cartes projet de grille
- `src/pages/references/[...slug].astro:23` — fiche projet détaillée
- `src/pages/equipe.astro:18-22` — avatars individuels (pré-calcul via champ `hasPhoto`)

## Structure attendue

```
src/
├── content/
│   ├── config.ts                 # Zod schemas de toutes les collections
│   ├── projets/*.md
│   ├── actualites/*.md
│   ├── equipe/*.md
│   └── services/*.md
├── layouts/
│   ├── BaseLayout.astro          # html/head/body, meta, fonts, analytics
│   └── PageLayout.astro          # header + footer wrapper
├── pages/
│   ├── index.astro               # accueil
│   ├── societe.astro
│   ├── equipe.astro
│   ├── services/
│   │   ├── index.astro
│   │   └── [slug].astro
│   ├── references/
│   │   ├── index.astro           # liste filtrable
│   │   └── [slug].astro          # fiche projet (getStaticPaths)
│   ├── actualites/
│   │   ├── index.astro
│   │   └── [slug].astro
│   └── contact.astro
└── components/
    ├── primitives/               # Bouton, Lien, Capsule, etc.
    ├── blocs/                    # blocs de page (Hero, ChiffresCles, etc.)
    └── layout/                   # Header, Footer, Navigation
```

## Conventions de nommage

- Composants : **PascalCase** (`FicheProjet.astro`).
- Variables et fonctions : **camelCase**.
- Fichiers de contenu (slugs) : **kebab-case sans accents** (`maison-pierre-loti.md`).
- Classes Tailwind : **regrouper logiquement** (layout → spacing → typo → couleur → état).

## Design system Apple-style — conventions CSS

- **Source de vérité** : `src/styles/global.css` (bloc `@theme`), pas de `tailwind.config.ts`.
- **Conteneur** : `max-w-[980px] mx-auto px-4 md:px-6` (pas `max-w-screen-xl`).
- **Navigation** : `position: fixed`, glass effect, hauteur 48px, spacer `h-12` après.
- **Headings** : ne pas forcer de couleur dans le CSS global — utiliser les classes Tailwind `text-near-black` ou `text-white` explicitement. Raison : en Tailwind v4, les règles hors `@layer` battent les utilitaires.
- **Sections** : alterner `bg-pure-black`, `bg-white`, `bg-light-gray` pour le rythme cinématique.
- **CTA** : `rounded-[980px]` (pill shape), jamais `rounded` ou `rounded-lg` pour les boutons.
- **Cartes** : `bg-light-gray rounded-lg`, pas de `border`. Hover : `hover:shadow-soft`.

## Performances — critères de blocage

Si l'un de ces critères n'est pas tenu, **ne pas merger** :

- LCP mobile (4G, Moto G4) < 1.8 s
- CLS < 0.05
- Total Blocking Time < 200 ms
- JS initial transmis (gzip) < 50 KB sur la page d'accueil, < 30 KB sur les autres pages
- Aucune police custom au-dessus du *fold* sans `font-display: swap`

## Tests à exécuter

```bash
npm run lint        # ESLint + astro check
npm run typecheck   # tsc --noEmit
npm run build       # build prod (échec = blocage)
```
