# Prompt — implémentation du gabarit fiche projet

## Route dynamique `/references/[slug]`

```
Lis CLAUDE.md, docs/04-specifications-pages.md (section Références, fiche
projet), content-models/projet.schema.md, content-templates/projet-modele.md,
.claude/rules/seo-geo.md, .claude/skills/json-ld-builder/SKILL.md.

Implémente la route dynamique `/references/[slug]`
(src/pages/references/[slug].astro) qui rend chaque projet de la collection
`projets`.

Structure imposée :

1. EN-TÊTE
   - Image principale en pleine largeur (composant Image Astro, AVIF, fetchpriority="high" si au-dessus du fold).
   - H1 : titre du projet.
   - Capsules : secteur + typologie (composant Capsule.astro).

2. FICHE TECHNIQUE (composant FicheTechnique.astro)
   - MOA, architecte, lieu, surface m², année, performance, mission FT2E.
   - Présentation tabulaire ou en grille selon design system.

3. RÉCIT PROJET
   - Corps Markdown du fichier (sections H2 issues du contenu).
   - max-width: 68ch pour la lisibilité.

4. GALERIE (composant GalerieProjet.astro)
   - Images de `galerie[]`, lazy-loaded.
   - Alt obligatoire (refus de build si manquant).
   - Lightbox accessible si nécessaire (à arbitrer ; sinon clic = ouvrir
     l'image dans un nouvel onglet).

5. PROJETS SIMILAIRES (composant ProjetsSimilaires.astro)
   - 3 suggestions auto-sélectionnées :
     a) Même secteur + même typologie : score le plus haut.
     b) À défaut : même secteur seulement.
     c) À défaut : projets récents en avant.
   - Exclure le projet courant.

6. CTA contact (composant CtaFinal.astro).

JSON-LD obligatoire :
- CreativeWork (cf. SKILL json-ld-builder)
- BreadcrumbList (Accueil → Références → <titre>)

Métadonnées :
- title : "<titre> — Référence FT2E"
- description : 140–160 c. dérivée du premier paragraphe du récit
  (à truncate intelligemment).
- og_image : image_principale du projet (idéalement recadrée en 1200×630
  via @astrojs/image — TODO si non automatisable en V1).

getStaticPaths() : génère une route par projet.

Validation :
- npm run build sans warning.
- Lighthouse mobile sur un projet exemple : Perf ≥ 90, A11y 100, SEO 100.
- Vérifier visuellement que le contenu d'au moins 3 projets s'affiche
  correctement (avec et sans architecte, avec et sans galerie).

Rapport final : indiquer si des composants manquent (et lesquels), et si
des images de projets sont en TODO.
```
