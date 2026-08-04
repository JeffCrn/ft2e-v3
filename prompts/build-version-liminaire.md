# Prompt master — Construire la version liminaire

> Copie-colle ce prompt dans Claude Code, dans un dossier `ft2e-site/` fraîchement initialisé. Il pilote la construction complète de la version liminaire, étape par étape, avec des points de validation explicites.

---

## Prompt

```
Tu travailles sur le projet ft2e-site. Mission : construire la VERSION LIMINAIRE
du site, telle que cadrée dans docs/14-version-liminaire.md.

Cette version sera présentée à l'équipe associée FT2E lors des prochains
échanges de cadrage. C'est une maquette navigable haute fidélité, pas un site
de production.

──────────────────────────────────────────────────────────────────
PHASE 0 — INITIALISATION (à exécuter une seule fois)
──────────────────────────────────────────────────────────────────

1. Lis dans cet ordre :
   - CLAUDE.md
   - docs/14-version-liminaire.md ← cadrage central
   - docs/15-audit-site-actuel.md ← contexte justificatif
   - docs/17-perimetre-livrable.md ← périmètre
   - docs/18-contenus-demonstration.md ← catalogue de démo
   - docs/00-vision-produit.md
   - docs/01-architecture-technique.md
   - docs/02-design-system.md
   - docs/03-modele-contenu.md
   - docs/04-specifications-pages.md
   - docs/06-strategie-seo-geo.md
   - docs/11-voix-editoriale.md
   - .claude/rules/ (toutes)

2. Initialise le projet Astro :
   - `npm create astro@latest .` avec : TypeScript strict, Tailwind, pas de
     starter (Empty), Git oui.
   - Installer : @astrojs/sitemap, @astrojs/rss, @astrojs/preact,
     @fontsource-variable/inter, @fontsource-variable/manrope,
     @astrojs/check.

3. Configure tailwind.config.ts avec les tokens exacts de docs/02-design-system.md.

4. Configure src/content/config.ts avec les 5 collections Zod
   (projets, services, equipe, actualites, secteurs) selon docs/03.

5. Crée src/layouts/BaseLayout.astro :
   - <head> : meta, fonts, JSON-LD via slot.
   - <body> : bannière liminaire conditionnelle si import.meta.env.PUBLIC_MODE === 'liminaire',
     Header, <main><slot/></main>, Footer.

6. Crée le fichier .env.example avec PUBLIC_MODE=liminaire et PUBLIC_SITE_URL=https://ft2e.fr.

7. Vérifie : `npm run build` doit passer sur un site vide.

Point de contrôle 0 → me confirmer que l'initialisation est terminée
avant de poursuivre.

──────────────────────────────────────────────────────────────────
PHASE 1 — DESIGN SYSTEM ET PRIMITIVES (3-4 itérations)
──────────────────────────────────────────────────────────────────

Crée dans src/components/primitives/ :
- Bouton.astro (variants: primary cuivre, secondary sarcelle, ghost)
- Lien.astro (interne, externe avec annonce d'ouverture)
- Capsule.astro (secteurs et typologies)
- Chiffre.astro (animation au scroll, suffixe optionnel, label)
- IconeSvg.astro (rend SVG depuis public/images/icons/)
- Image.astro (wrapper astro:assets, AVIF/WebP, lazy par défaut)
- BadgeDemo.astro (badge "[DÉMO]" discret, conditionnel)
- BanniereLiminaire.astro (sticky top, masquable via PUBLIC_MODE)

Pour chaque primitive :
- Interface Props typée stricte.
- Commentaire JSDoc avec @example.
- Aucune couleur hard-codée (tokens uniquement).
- Aucun JS client.

Vérifications : npm run typecheck && npm run build.

──────────────────────────────────────────────────────────────────
PHASE 2 — LAYOUT GLOBAL
──────────────────────────────────────────────────────────────────

Crée src/components/layout/ :
- Header.astro : logo placeholder + navigation desktop + drawer mobile
- Navigation.astro : 7 liens (Accueil, Société, Équipe, Services, Références, Actualités, Contact)
- Footer.astro : coordonnées [À CONFIRMER FT2E], sitemap, mentions, plan
- LienEvitement.astro : « Aller au contenu principal »

Logo placeholder : crée public/images/logo/logo-horizontal.svg
(« FT2E » en Manrope ExtraBold, 2 en cuivre, le reste en bleu-nuit).

Header doit afficher la bannière liminaire au-dessus de tout le reste.

──────────────────────────────────────────────────────────────────
PHASE 3 — CONTENUS DE DÉMONSTRATION (8 fiches + 6 services + 1 actu)
──────────────────────────────────────────────────────────────────

Crée tous les .md listés dans docs/18-contenus-demonstration.md :

src/content/projets/ → 8 fiches selon le catalogue
  (Maison Pierre Loti, EHPAD Doux-Refuge, Résidence Quais Domidylle,
   Réhab Mireuil OPH, Siège tertiaire Niort, Centre nautique Île de Ré,
   Extension école Royan, EXE PSLA Bouygues)

src/content/services/ → 6 fichiers (audit-diagnostic, etude-thermique,
  cvc, electricite, coordination-ssi, etudes-execution-bim)

src/content/actualites/ → 1 fichier (2026-09-lancement-site.md)

src/content/secteurs/ → 6 fichiers (logement, tertiaire, sante, sport,
  industriel, patrimoine)

Pour chaque fiche projet, écrire un récit (corps Markdown) de 3 à 6
paragraphes structurés en : Enjeu → Solution → Particularités → Résultat.
Tous les chiffres et MOA non confirmés marqués [DÉMO] dans le texte.

Vérification : npm run build doit générer tous les .md sans erreur Zod.

──────────────────────────────────────────────────────────────────
PHASE 4 — BLOCS DE PAGE (composants de section)
──────────────────────────────────────────────────────────────────

Crée src/components/blocs/ :
- Hero.astro
- ChiffresCles.astro (4 chiffres animés, sources depuis frontmatter de la page)
- CartesServices.astro (grille 6 services depuis collection)
- SecteursPhares.astro (3 secteurs visuels)
- ReferencesRecentes.astro (4 projets `en_avant: true` triés par année desc)
- EquipePreview.astro (photo collective + accroche)
- BandeauPartenaires.astro (cartouches texte [DÉMO])
- CtaFinal.astro
- FicheTechnique.astro (tableau 10 champs projet)
- GalerieProjet.astro
- ProjetsSimilaires.astro (3 suggestions auto)
- FiltresProjets.astro (island Preact, 5 filtres PDF p. 9)
- GrilleProjets.astro
- CarteProjet.astro (avec BadgeDemo si demo:true)
- CarteService.astro
- CarteActualite.astro
- FormulaireContact.astro (4 branches, submit désactivé en liminaire)
- FAQ.astro (accordéon a11y)

Vérification après chaque composant : npm run build.

──────────────────────────────────────────────────────────────────
PHASE 5 — PAGES
──────────────────────────────────────────────────────────────────

Implémente dans src/pages/ :
1. index.astro (Accueil, 9 blocs PDF p. 10)
2. societe.astro (récit 5 paragraphes)
3. equipe.astro (page collective, pas de portraits individuels)
4. services/index.astro + services/[slug].astro
5. references/index.astro (avec filtres) + references/[slug].astro
6. actualites/index.astro + actualites/[slug].astro
7. contact.astro
8. accessibilite.astro
9. mentions-legales.astro
10. politique-confidentialite.astro
11. 404.astro

Métadonnées SEO complètes par page (title unique 50-60c, description
unique 140-160c, canonical, og_image, JSON-LD adapté).

Vérification : npm run build et toutes les routes accessibles en local.

──────────────────────────────────────────────────────────────────
PHASE 6 — SEO / JSON-LD
──────────────────────────────────────────────────────────────────

Crée src/components/seo/ :
- Meta.astro (title, description, OG, Twitter, canonical)
- JsonLd.astro (injection JSON-LD via set:html)
- Breadcrumbs.astro (visuel + JSON-LD BreadcrumbList)

src/lib/constants.ts : constante FT2E_BUSINESS (LocalBusiness PDF p. 19,
adresse en placeholder [À CONFIRMER]).

Injecte :
- LocalBusiness sur Accueil
- Service sur chaque page service
- CreativeWork sur chaque fiche projet
- BlogPosting sur l'article
- BreadcrumbList sur les pages internes
- WebSite global avec SearchAction (V2)

──────────────────────────────────────────────────────────────────
PHASE 7 — AUDIT ET FINALISATION
──────────────────────────────────────────────────────────────────

1. Lance la commande /audit-page sur :
   - /
   - /services/cvc
   - /references/maison-pierre-loti
   - /equipe
   - /contact

2. Pour chaque page, vise Lighthouse mobile :
   - Performance ≥ 90
   - Accessibility 100
   - Best Practices 100
   - SEO 100

3. Corrige tous les écarts à la cible.

4. Vérifie typographie française : espaces insécables avant : ; ! ?,
   guillemets « », apostrophes ', tirets —.

5. Vérifie présence de [DÉMO] partout où requis.

6. Run final : npm run lint && npm run typecheck && npm run build.

7. Produit un rapport synthétique dans audits/liminaire-pret.md :
   - Nombre de pages générées
   - Scores Lighthouse
   - TODOs restants pour FT2E
   - Liste des fichiers à remplacer en passant en production

──────────────────────────────────────────────────────────────────
LIVRABLE FINAL
──────────────────────────────────────────────────────────────────

À la fin de l'exécution :
- `npm run dev` démarre le site sur http://localhost:4321
- `npm run build` génère un dist/ servable
- Tous les contenus sont marqués [DÉMO] ou validés
- La bannière liminaire est visible
- Le site est prêt à être présenté à l'équipe FT2E

RÈGLE D'OR : à aucun moment tu n'inventes un nom, un MOA ou un chiffre
qui ne soit pas dans docs/18-contenus-demonstration.md. Si une information
manque, tu mets [À CONFIRMER FT2E] et tu continues.

Procède phase par phase. Après chaque phase, fais un point synthétique
de ce qui a été fait et attends mon feu vert avant de passer à la suivante,
SAUF si je t'ai dit en début de session "yolo" — dans ce cas, tu enchaînes
les 7 phases en autonomie.
```

---

## Variante express — yolo

Pour une exécution non-interactive (Claude Code enchaîne les 7 phases sans confirmation) :

```
[le prompt ci-dessus]

YOLO : enchaîne les 7 phases sans me demander de confirmation entre chaque.
Si une information manque, tu mets [À CONFIRMER FT2E] et tu continues.
Rapport final consolidé à la fin.
```

## Variante itérative — page par page

Si tu préfères contrôler le rythme :

```
Pour cette session, on ne fait que la PHASE 5 sur la page :
<NOM DE PAGE>

Lis CLAUDE.md, docs/14-version-liminaire.md, docs/04 (section dédiée),
docs/18 (catalogue), puis implémente cette page seule en respectant
toutes les règles.
```

## Astuces de pilotage

- **Garde un terminal `npm run dev` ouvert** dans une fenêtre annexe : tu peux ouvrir le site dans le navigateur entre chaque phase pour vérification visuelle.
- **Commit après chaque phase** : `git add . && git commit -m "feat(liminaire): phase N - <résumé>"`.
- **Si Claude bloque** sur une décision (ex. choix d'animation, microcopie ambiguë), il doit poser **une** question maximum. S'il en pose plus, c'est qu'il sur-cadre et qu'il faut le recentrer.
- **Performance** : si Lighthouse stagne sous 90 sur mobile, suspecter (par ordre) : image hero trop lourde, polices non préchargées, *island* Preact chargée trop tôt.
