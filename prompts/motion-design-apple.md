# Prompt : Motion Design Apple-Style pour FT2E

> À coller tel quel dans une nouvelle session Claude Code sur le projet `ft2e-site`.

---

## Contexte

Le site FT2E est un site Astro statique (build OK, 26 pages) qui a adopté un design system Apple-style complet :
- Palette binaire noir `#000000` / gris clair `#f5f5f7` / accent unique Apple Blue `#0071e3`
- Police Inter Variable, headlines serrées (line-height 1.07), conteneur 980px
- Navigation glass fixe (backdrop-blur + saturate)
- CTA pill (border-radius 980px), cartes sans bordure
- Rythme cinématique : sections alternées noir/blanc/gris

Le site est actuellement **statique et plat** visuellement. Zéro animation au-delà du compteur de chiffres clés. Il faut insuffler le dynamisme Apple — des transitions fluides, des révélations au scroll, des micro-interactions qui donnent vie à chaque section — tout en restant sobre et maîtrisé (jamais gratuit, toujours au service du contenu).

## Mission

Implémenter un système complet de **motion design Apple-style** sur tout le site, en **vanilla JS/CSS uniquement** (pas de bibliothèque externe — pas de GSAP, Framer Motion, AOS). Astro est statique : tout doit fonctionner avec des `<script>` inline et du CSS natif.

### Contraintes absolues

1. **`prefers-reduced-motion: reduce`** → toutes les animations se désactivent instantanément (accessibilité RGAA AA)
2. **Zero layout shift** : aucune animation ne doit provoquer de CLS. Les éléments occupent leur espace final dès le rendu initial, seuls opacity/transform sont animés (propriétés GPU-composited)
3. **Performance** : uniquement `opacity`, `transform`, `filter`, `clip-path` — jamais `width`, `height`, `top`, `left`, `margin`
4. **Budget JS** : le script d'animation total doit peser < 3 KB gzip
5. **IntersectionObserver** pour toutes les animations au scroll (pas de scroll listener)

---

## Effets à implémenter — par ordre de priorité

### 1. Hero Reveal cinématique (page d'accueil)

L'effet signature. Quand la page se charge :
- Le fond noir est déjà là (pas de flash blanc)
- Le titre h1 apparaît **lettre par lettre** (ou mot par mot) avec un fade-in + léger translateY(-8px), stagger de 40ms entre chaque mot
- Le sous-titre apparaît 300ms après le dernier mot du titre, en fade-in doux (opacity 0→1, translateY(10px)→0, duration 600ms)
- Les deux CTA pill apparaissent simultanément 200ms après le sous-titre, avec un léger scale(0.95→1) + fade-in
- **Courbe d'easing** : `cubic-bezier(0.25, 0.46, 0.45, 0.94)` (Apple ease-out)

**Référence Apple** : regarder comment apple.com/iphone révèle le nom du produit — précis, fluide, jamais lent.

### 2. Scroll Reveal pour toutes les sections

Chaque section de la page d'accueil se révèle au scroll :
- **Trigger** : quand 15% de la section entre dans le viewport (threshold 0.15)
- **Animation** : fade-in (opacity 0→1) + translateY(30px→0), duration 700ms, easing Apple
- **Stagger** : si la section contient une grille de cartes, chaque carte se révèle avec un délai de 80ms par rapport à la précédente (effet cascade)
- **Une seule fois** : l'observer se déconnecte après le premier trigger (pas de re-animation au scroll up)

Sections concernées : ChiffresCles, CartesServices, SecteursPhares, ReferencesRecentes, EquipePreview, BandeauPartenaires, CtaFinal.

### 3. Cartes — hover 3D subtil (desktop uniquement)

Sur hover des cartes (CarteService, CarteProjet, CarteActualite) :
- **Tilt 3D** léger : la carte s'incline de max 3° dans la direction du curseur (perspective 1000px, rotateX/rotateY calculés selon la position de la souris relative au centre de la carte)
- **Élévation** : translateZ(10px) + shadow-soft qui s'intensifie légèrement
- **Transition** : 400ms ease-out à l'entrée, 600ms ease-out au départ (retour plus lent = plus naturel)
- **Mobile** : effet désactivé (pas de hover), garder uniquement le shadow au tap via `:active`

### 4. Navigation glass — dynamic opacity

La nav glass doit réagir au scroll :
- **Position 0** (haut de page) : fond transparent, pas de blur — la nav flotte au-dessus du hero
- **Scroll > 50px** : transition vers `rgba(0,0,0,0.8)` + `backdrop-filter: blur(20px) saturate(180%)` — le verre se matérialise
- **Transition** : 300ms ease-out
- Cela crée l'effet Apple.com où la nav est invisible au départ puis se solidifie quand on scrolle

### 5. Chiffres clés — compteur amélioré

Le compteur existe déjà. L'améliorer :
- Ajouter un **scale pulse** subtil à la fin du comptage : scale(1→1.05→1) sur 300ms
- Le label sous le chiffre apparaît avec un fade-in 200ms après la fin du compteur
- Chaque chiffre démarre avec un stagger de 150ms

### 6. CTA Final — parallax texte

La section CtaFinal (fond noir, « Un projet en tête ? ») :
- Le titre se déplace légèrement vers le haut au scroll (parallax factor 0.15 — très subtil)
- L'effet ne doit **pas** utiliser `scroll` event mais `IntersectionObserver` avec des ratios multiples, ou mieux : CSS `scroll-timeline` si le support navigateur le permet, sinon un observer avec ratio-based translateY

### 7. Page transitions — morph effect

Utiliser les **View Transitions API** d'Astro pour les navigations entre pages :
- Activer `transition:animate` dans la config Astro
- Le header (nav glass) **persiste** entre les pages (pas de re-rendu)
- Le contenu principal fait un **cross-fade** (opacity out 200ms → opacity in 300ms)
- Le titre h1 de la page de destination fait un léger **slide-up** à l'arrivée

### 8. Liens « En savoir plus › » — chevron animé

Au hover sur les liens avec chevron `›` :
- Le chevron se déplace de 4px vers la droite (translateX(4px)) avec un spring-like ease
- Le texte change de couleur (link-blue → apple-blue) simultanément
- La transition crée un micro-mouvement qui invite au clic

### 9. Formulaire Contact — focus ripple

Quand un input reçoit le focus :
- Le ring Apple Blue apparaît avec une **expansion** : de scale(0.98) à scale(1), opacity 0→1, duration 200ms
- Effet inverse au blur : le ring se rétracte légèrement avant de disparaître
- Les radio buttons « Vous êtes ? » : au check, le fond passe de light-gray à apple-blue/10 avec une transition douce de 200ms

### 10. Filtres Références — pill switch

Sur la page Références, quand on clique sur un filtre :
- Le filtre actif fait une **transition de fond** fluide (300ms) : bg-light-gray → bg-near-black
- Les cartes filtrées disparaissent en **scale(0.95) + opacity(0)** sur 200ms
- Les cartes correspondantes apparaissent en **scale(1) + opacity(1)** sur 300ms, avec stagger 50ms
- Effet net : les cartes semblent « respirer » pendant le filtrage

---

## Architecture technique suggérée

```
src/
├── scripts/
│   └── motion.ts          # Module unique, tree-shakeable
│       ├── heroReveal()    # Animation hero au chargement
│       ├── scrollReveal()  # IntersectionObserver pour toutes les sections
│       ├── cardTilt()      # Hover 3D sur les cartes
│       ├── navGlass()      # Transition de la nav au scroll
│       ├── chevronHover()  # Animation du chevron ›
│       └── formFocus()     # Effets de focus formulaire
└── styles/
    └── motion.css          # Classes d'animation et keyframes
```

Ou intégrer directement dans les `<script>` de chaque composant si la modularité Astro le justifie.

## Classes CSS à créer

```css
/* État initial avant reveal */
[data-reveal] {
  opacity: 0;
  transform: translateY(30px);
}

/* État révélé */
[data-reveal].revealed {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 700ms cubic-bezier(0.25, 0.46, 0.45, 0.94),
              transform 700ms cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

/* Stagger pour les grilles */
[data-reveal-child]:nth-child(1) { transition-delay: 0ms; }
[data-reveal-child]:nth-child(2) { transition-delay: 80ms; }
[data-reveal-child]:nth-child(3) { transition-delay: 160ms; }
/* ... jusqu'à 8 */

/* Désactivation totale */
@media (prefers-reduced-motion: reduce) {
  [data-reveal] {
    opacity: 1;
    transform: none;
    transition: none;
  }
}
```

## Data attributes à ajouter sur les composants

- `data-reveal` sur chaque `<section>` de bloc
- `data-reveal-child` sur chaque carte dans une grille
- `data-hero-title` sur le h1 du Hero accueil
- `data-hero-subtitle` sur le sous-titre
- `data-hero-cta` sur le wrapper des CTA
- `data-card-tilt` sur chaque carte interactive
- `data-chevron` sur les liens « En savoir plus › »

## Easing de référence Apple

```css
:root {
  --ease-apple: cubic-bezier(0.25, 0.46, 0.45, 0.94);
  --ease-apple-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);
  --ease-apple-smooth: cubic-bezier(0.4, 0, 0.2, 1);
}
```

## Vérifications post-implémentation

1. `npm run build` doit passer
2. Lighthouse Performance ≥ 90 (les animations ne doivent pas dégrader le score)
3. CLS = 0 (vérifier que `data-reveal` avec `opacity: 0` ne cause pas de shift — les éléments doivent occuper leur espace)
4. Tester avec `prefers-reduced-motion: reduce` dans DevTools → aucune animation visible
5. Tester sur mobile (pas de card tilt, scroll reveal uniquement)
6. Le hero reveal doit être **terminé en < 1.5s** après le first paint (pas de delay excessif)

## Inspiration directe

- apple.com/iphone — hero reveal, section scroll
- apple.com/macbook-pro — parallax texte, grid reveal
- apple.com/apple-vision-pro — scale/opacity transitions magistrales
- linear.app — card hover tilt, nav glass dynamique

## Résultat attendu

Le visiteur ouvre ft2e.fr et le titre se révèle avec précision cinématique. En scrollant, chaque section émerge avec fluidité. Les cartes réagissent au survol avec une profondeur 3D subtile. La navigation se matérialise comme du verre. Les transitions entre pages sont fluides. Chaque micro-interaction communique : « ce site a été conçu avec le même soin que les bâtiments de FT2E ».

**L'effet Wahou vient de la cohérence et de la précision, pas de l'excès.**
