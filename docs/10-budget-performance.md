# 10 · Budget de performance

Le site doit être **rapide par construction**, pas rapide par optimisation a posteriori. Ce document fixe les seuils ; toute régression est un blocage.

## Core Web Vitals — cibles strictes

Mesures sur **mobile** (Moto G4 émulé, throttling 4G simulé Lighthouse), sur la page d'accueil et trois fiches projets.

| Métrique | Cible V1 | Seuil de blocage | Idéal |
|---|---|---|---|
| **LCP** (Largest Contentful Paint) | < 1.8 s | 2.5 s | < 1.2 s |
| **INP** (Interaction to Next Paint) | < 200 ms | 500 ms | < 100 ms |
| **CLS** (Cumulative Layout Shift) | < 0.05 | 0.10 | 0 |
| **FCP** (First Contentful Paint) | < 1.5 s | 2.0 s | < 1.0 s |
| **TBT** (Total Blocking Time) | < 200 ms | 300 ms | < 100 ms |
| **Speed Index** | < 2.5 s | 3.5 s | < 2.0 s |
| **TTI** (Time to Interactive) | < 3.0 s | 4.0 s | < 2.5 s |

## Lighthouse — scores cibles

| Catégorie | Mobile | Desktop |
|---|---|---|
| Performance | **≥ 90** | ≥ 95 |
| Accessibility | **100** | **100** |
| Best Practices | **100** | **100** |
| SEO | **100** | **100** |

## Budget de poids — par page

| Ressource | Accueil | Pages internes |
|---|---|---|
| **HTML (gzip)** | < 20 KB | < 15 KB |
| **CSS (gzip)** | < 15 KB | < 15 KB |
| **JS initial (gzip)** | < 50 KB | < 30 KB |
| **Polices (woff2)** | < 60 KB | < 60 KB |
| **Image au-dessus du fold** | < 150 KB (AVIF) | < 100 KB |
| **Total page** (avec assets above-the-fold) | < 350 KB | < 250 KB |

**Vérification manuelle** :

```bash
du -sh dist/_astro/
ls -laSh dist/_astro/ | head -20
```

## Règles d'implémentation

### Images

1. **Format AVIF** par défaut, **WebP** en fallback, JPG en dernier recours.
2. **Dimensions exactes** : pas de scale CSS d'une image trop grande.
3. **Lazy loading** : `loading="lazy"` partout sauf au-dessus du fold (`loading="eager" fetchpriority="high"`).
4. **`width` et `height`** sur tous les `<img>` pour éviter le CLS.
5. **`srcset` responsive** : 3 tailles minimum pour les hero (640w, 1024w, 1920w).
6. **Génération via `astro:assets`** (`<Image>` Astro), jamais `<img>` brut sauf cas explicite.

### Polices

1. **Self-hosted** uniquement (`@fontsource-variable/inter`), pas de Google Fonts CDN.
2. **`font-display: swap`** systématique.
3. **Preload** de la police au-dessus du fold dans `<head>` :
   ```html
   <link rel="preload" href="/fonts/inter-variable.woff2" as="font" type="font/woff2" crossorigin>
   ```
4. **Police unique** : Inter Variable pour headings et body (substitute libre de SF Pro). Pas de Manrope.
5. **Variable font** : un seul fichier au lieu de 4–8 poids statiques.
6. **Subset latin-fr** seulement (pas de cyrillique, grec, etc.).

### CSS

1. **Tailwind purgé** : seules les classes utilisées finissent dans le bundle.
2. **CSS critique inliné** par Astro (built-in).
3. **Pas de CSS-in-JS** côté client.
4. **Pas de framework UI** lourd (Bootstrap, Bulma, etc.).

### JavaScript

1. **Zero JS par défaut.** Toute *island* Astro doit être justifiée.
2. **Directive `client:*` minimale** : préférer `client:visible` ou `client:idle` à `client:load`.
3. **Pas de polyfill** pour navigateurs < 2 ans. Cible : 2 dernières versions de Chrome, Firefox, Safari, Edge.
4. **Pas de bibliothèque tierce** sans budget précis (chaque dépendance ajoute son poids et son risque de breakage).
5. **Tree-shaking strict** : `sideEffects: false` dans les packages internes.

### Cache

1. **Assets versionnés** (`_astro/*.[hash].js`) → cache 1 an immutable.
2. **HTML** → cache court (1 heure) pour permettre les mises à jour.
3. **Service Worker** : **pas en V1**. Risque de bug invisible > bénéfice.

### Réseau

1. **HTTP/2 minimum**, idéalement HTTP/3 (OVH supporte H/2 par défaut).
2. **Compression Brotli** si disponible, sinon gzip.
3. **DNS prefetch** vers Plausible si analytics activé :
   ```html
   <link rel="dns-prefetch" href="https://plausible.io">
   ```

## Mesures et alertes

### À chaque PR

CI Lighthouse en mode headless sur 3 routes : `/`, `/expertises/cvc`, `/references/<un-projet>`. Échec si :
- Performance mobile < 85.
- Accessibility < 100.
- LCP > 2 s.

### Mensuellement

- Audit Lighthouse complet sur 10 routes échantillon, archivé dans `audits/YYYY-MM-lighthouse.json`.
- Bilan Core Web Vitals depuis Search Console (Field Data).
- Bilan Plausible : pages les plus lentes selon métriques réelles utilisateurs.

### Tableau de suivi

Un fichier `audits/perf-tracking.md` à tenir à jour, format :

```markdown
| Date | Route | LCP | CLS | TBT | Perf score |
|---|---|---|---|---|---|
| 2026-09-01 | / | 1.4s | 0 | 80ms | 96 |
…
```

## Anti-patterns

- ❌ Carrousels lourds en hero.
- ❌ Vidéo en lecture automatique.
- ❌ Iframe YouTube/Vimeo directement embarquée (utiliser `lite-youtube-embed` si vidéo indispensable).
- ❌ Sliders d'images en JS quand un grid CSS fait l'affaire.
- ❌ Chargement bloquant de polices externes.
- ❌ « Optimisation » via une bibliothèque qui ajoute 50 KB pour économiser 5 KB.
