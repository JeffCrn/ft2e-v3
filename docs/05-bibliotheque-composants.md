# 05 · Bibliothèque de composants

Inventaire de tous les composants Astro du site. **Ce document est vivant** : toute création de composant impose une mise à jour de cette liste, dans la même PR.

## Conventions

- **Catégories** : `primitives/`, `blocs/`, `layout/`, `seo/`.
- **Nommage** : `PascalCase.astro`.
- **Props** : interface TypeScript exportée nommée `Props`.
- **Slots** : préférer aux props longues quand le contenu est riche.
- **Aucune logique métier dans les primitives.**
- **Design system Apple-style** : conteneur `max-w-[980px]`, pill CTA `rounded-[980px]`, cartes sans bordure, sections alternées noir/blanc/gris.
- **Scripts client + View Transitions** : tout `addEventListener` dans un `<script>` de composant doit s'initialiser via `document.addEventListener('astro:page-load', initX)` + guard `dataset.bound`. Sinon le composant devient inerte après la première navigation client-side. Pattern de référence : `Header.astro:68-83`, `Chiffre.astro:73`, `BaseLayout.astro:200-208`. Règle complète : `.claude/rules/astro-conventions.md` § « Scripts client & View Transitions ».

## Catégorie `primitives/`

Petits éléments réutilisables, sans logique métier.

| Composant | Props clés | Style Apple |
|---|---|---|
| `Bouton.astro` | `href`, `variante: "primary" \| "secondary" \| "ghost"`, `externe?` | Pill shape `rounded-[980px]`, primary = Apple Blue, secondary = near-black, ghost = outline link-blue |
| `Lien.astro` | `href`, `externe?`, `surFondSombre?` | `text-link-blue` (clair) ou `text-bright-blue` (sombre), chevron `›` |
| `Capsule.astro` | `variante: "secteur" \| "typologie" \| "mission"` | Pill `rounded-[980px]`, fond `apple-blue/10`, texte `apple-blue` |
| `Chiffre.astro` | `valeur: number`, `suffixe?`, `label`, `demo?` | `font-semibold text-near-black`, taille clamp hero, animation au scroll |
| `BadgeDemo.astro` | `class?` | Pill `rounded-[980px]`, fond `text-tertiary/15`, marque les contenus encore en démonstration |
| `IconeSvg.astro` | `nom: string`, `taille?`, `label?` | SVG sprite, `aria-hidden` si décoratif |

## Catégorie `blocs/`

Sections autonomes de page, avec une intention éditoriale claire.

| Composant | Style Apple | Pages |
|---|---|---|
| `Hero.astro` | Accueil uniquement : `bg-pure-black`, hero reveal mot par mot, 2 CTA pill | Accueil |
| `HeroPage.astro` | **Toutes les pages internes** : `bg-pure-black` + breadcrumb intégré + eyebrow (Apple Blue uppercase) + titre + sous-titre + slot `metadata`. Props `size: 'default' \| 'compact'` | Toutes pages internes (expertises, références, actualités, société, équipe, contact, légales) |
| `ChiffresCles.astro` | `bg-light-gray`, grille 4 colonnes, chiffres animés near-black avec pulse à la fin | Accueil |
| `CartesExpertises.astro` | `bg-white`, titre + sous-titre centrés, grille 3 colonnes `gap-4` | Accueil, Expertises index |
| `CarteExpertise.astro` | `bg-light-gray rounded-lg`, pas de bordure, `hover:shadow-soft`, lien `›` chevron animé | CartesExpertises |
| `SecteursPhares.astro` | `bg-pure-black`, cartes `bg-dark-surface-1`, texte blanc | Accueil |
| `ReferencesRecentes.astro` | `bg-white`, titre centré, lien `›` bleu, grille 4 colonnes | Accueil |
| `CarteProjet.astro` | `bg-light-gray rounded-lg`, `<img>` lazy + zoom 5 % au hover **ou** fallback placeholder sombre (détection `fs.existsSync` au build), capsule pill | Grilles projets |
| `EquipePreview.astro` | `bg-light-gray`, grille 2 colonnes (photo sombre + texte), CTA secondary | Accueil |
| `BandeauPartenaires.astro` | `bg-white`, noms en pills `bg-light-gray rounded-[980px]`, centré | Accueil |
| `CtaFinal.astro` | `bg-pure-black py-24`, titre blanc centré, CTA pill Apple Blue | Toutes pages |
| `FicheTechnique.astro` | `bg-light-gray rounded-lg`, capsules pill, pas de bordure | Fiche projet |
| `ProjetsSimilaires.astro` | `bg-light-gray`, grille 3 colonnes | Fiche projet |
| `CarteActualite.astro` | `bg-light-gray rounded-lg`, hover shadow, badge catégorie pill | Actualités |
| `FormulaireContact.astro` | Inputs `bg-light-gray rounded-lg` sans bordure, focus ring Apple Blue, bouton pill | Contact |
| `FAQ.astro` | `<details>` sur `bg-light-gray rounded-lg`, hover Apple Blue, chevron animé | Services |

## Catégorie `layout/`

| Composant | Style Apple |
|---|---|
| `Header.astro` | Navigation glass : `position: fixed`, `h-12`, `rgba(0,0,0,0.8)` + `backdrop-blur(20px) saturate(180%)`, liens 12px blanc, menu mobile overlay sombre. Spacer `h-12` après. |
| `Footer.astro` | `bg-light-gray`, 4 colonnes en 12px, liens `text-text-secondary hover:text-link-blue`, bordures `rgba(0,0,0,0.08)` |

## Catégorie `seo/`

| Composant | Usage |
|---|---|
| `JsonLd.astro` | Injection d'un objet JSON-LD validé |
| `Breadcrumbs.astro` | Fil d'Ariane visuel (12px, séparateur `›`) + `BreadcrumbList` JSON-LD couplé |

## Composants à NE PAS créer

- Wrapper générique `Section`, `Card`, `Container` — préférer Tailwind direct.
- Composant utilisé une seule fois — laisser inline dans la page.
- Doublon d'un composant existant — étendre l'existant via une prop.
