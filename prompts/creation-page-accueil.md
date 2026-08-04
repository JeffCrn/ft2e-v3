# Prompt — création de la page d'accueil

```
Lis CLAUDE.md, docs/00-vision-produit.md, docs/04-specifications-pages.md
(section « Page 1 — Accueil »), docs/02-design-system.md, .claude/rules/
(toutes).

Implémente la page d'accueil `/` (src/pages/index.astro) conformément à la
spec. Procède en mode plan :

1. Présente-moi un plan d'implémentation par bloc (Hero, ChiffresCles,
   CartesServices, SecteursPhares, ReferencesRecentes, EquipePreview,
   BandeauPartenaires, CtaFinal, Footer) en distinguant pour chaque bloc :
   - composant existant à réutiliser
   - composant à créer
   - contenu nécessaire (statique inline / depuis content collection / TODO)

2. Une fois le plan validé par moi, crée les composants manquants en
   déléguant à component-builder, puis assemble la page.

3. Métadonnées obligatoires :
   - title : "FT2E — Bureau d'études techniques, La Rochelle"
   - description : "Bureau d'études fluides, thermique, électricité, SSI,
     BIM à La Rochelle. Au service des architectes et MOA depuis 2008."
   - og_image : /og/accueil.jpg (laisser TODO image à produire)
   - JSON-LD : ProfessionalService complet + WebSite

4. Performance — critères de blocage :
   - LCP mobile < 1.5 s
   - JS initial < 50 KB gzip
   - Hero image servie en AVIF avec dimensions exactes

5. Avant de me rendre la main :
   - `npm run lint && npm run typecheck && npm run build`
   - `npx lighthouse http://localhost:4321/ --only-categories=performance,accessibility,seo --emulated-form-factor=mobile`
   - Cible Lighthouse : Perf ≥ 90, A11y 100, SEO 100

6. Rapport final synthétique : ce qui est fait, ce qui reste en TODO
   (images, contenus à renseigner par FT2E).

Contenu de remplissage : aucun lorem ipsum. Pour les chiffres clés, laisse
des placeholders <strong>TODO: valeur à fournir par FT2E</strong> avec un
TODO HTML commenté.
```
