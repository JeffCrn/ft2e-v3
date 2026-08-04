# 14 · Version liminaire — cadrage opérationnel

**📌 ÉTAT (juin 2026)** : la version liminaire est **déployée en production sur Vercel** (`ft2e-site.vercel.app`). Le **bandeau « Version liminaire »** a été **retiré** du site sur demande de FT2E. Les contenus encore en démonstration restent marqués `[DÉMO]` dans les fichiers Markdown. La phase d'atelier de cadrage avec l'équipe FT2E peut commencer.

> Ce document définit ce que Claude Code a produit dans le cadre actuel : une **version liminaire** du site ft2e.fr, qui sert de support à l'atelier de cadrage avec l'équipe FT2E.

## Pourquoi une version liminaire

La proposition stratégique de mai 2026 (PDF) prévoit en Phase 1 (semaines 1–2) un **atelier de cadrage**. Cet atelier sera plus efficace si l'équipe FT2E peut voir une version naviguable et plausible plutôt que des wireframes statiques. Une démonstration **incarne** mieux qu'un document. C'est cette version-là que Claude Code construit aujourd'hui.

Concrètement :

- L'équipe ouvre une URL et navigue dans le site comme si elle visitait `ft2e.fr` en septembre 2026.
- Elle voit la palette, la typo, le ton, la structure, les filtres, les fiches projets, la signature.
- Elle peut **réagir, corriger, valider** — pas spéculer.
- À l'issue de la discussion, ce qui est validé est conservé, ce qui est rejeté est modifié, et la trajectoire vers le site définitif est dégagée.

## Objectif fonctionnel — ce qui doit marcher

| Page / fonctionnalité | Niveau attendu dans la liminaire |
|---|---|
| Accueil avec 9 blocs (PDF p. 10) | **Complet** — tous les blocs visibles avec contenus de démo |
| Société | **Complet** — récit, valeurs, méthodologie, engagements |
| Équipe | **Complet** — photo collective placeholder + grille des 7 profils (prénom + rôle + métier, traitement uniforme). Portraits individuels en phase de production. |
| Expertises (index + 6 sous-pages) | **Complet** — les 6 expertises rédigées avec template `HeroPage` |
| Références (liste + filtres) | **Complet** — filtres opérationnels sur 6 à 8 fiches |
| Fiche projet (gabarit) | **Complet** — 6 à 8 fiches plausibles structurées |
| Actualité (liste + 1 article) | **Minimal** — 1 article de démo « Lancement du nouveau site » |
| Contact | **UI uniquement** — formulaire à branches affiché, **sans soumission backend** |
| Accessibilité | **Page placeholder** — déclaration conforme au modèle légal, valeurs `[À MESURER AU LANCEMENT]` |
| Mentions légales / Confidentialité | **Squelettes** — texte type, marqués `[À VALIDER]` |
| Décap CMS `/admin` | **Hors périmètre liminaire** |

## Marquage visuel — historique

**📌 Mise à jour juin 2026** : la bannière sticky « VERSION LIMINAIRE » a été retirée du site sur demande de FT2E. Seuls les badges `[DÉMO]` au niveau des contenus subsistent pour identifier les éléments encore à valider. Le code de la bannière a été supprimé de `BaseLayout.astro` ; la variable `PUBLIC_MODE` n'est plus utilisée.

## Marquage des contenus de démo

Tout contenu de démo (titre projet, MOA, surface, chiffre clé) doit porter le tag `[DÉMO]` dans le frontmatter Markdown :

```yaml
titre: "EHPAD Le Doux-Refuge"
demo: true        # ← présence du flag = contenu de démonstration
moa: "CCAS de Saintes"
```

Le composant `<CarteProjet>` et le `<FicheTechnique>` rendent automatiquement un badge discret `[DÉMO]` quand `demo: true`. En production, on retire le flag des fiches validées avec FT2E.

**Exceptions** : aucun marquage `[DÉMO]` n'est requis sur :
- Les informations issues directement du site actuel `ft2e.myportfolio.com` (l'équipe, l'année de création, le périmètre métier).
- Les éléments du PDF qui sont des engagements éditoriaux de la proposition (positionnement, piliers de marque, signature).

## Contenu de démonstration — sources autorisées

Trois sources et trois seulement (cf. `docs/18-contenus-demonstration.md` pour le détail) :

1. **Le PDF de proposition stratégique** — toutes ses spécifications éditoriales.
2. **Le site actuel ft2e.myportfolio.com** — équipe, secteurs visibles, projets identifiables, MOA mentionnés.
3. **Des projets de démonstration plausibles** — construits à partir du carnet d'adresses du PDF p. 6 (Domidylle, Médiatim, OPH La Rochelle, Habitat 17, etc.) **sans inventer un projet précis qui leur soit attribué**. Pour cela, on procède ainsi :
   - Soit un projet est **explicitement mentionné dans le PDF** (Maison Pierre Loti, Rochefort) → on peut le détailler, en marquant `[DÉMO]` les valeurs non confirmées (surface exacte, performance).
   - Soit on construit un projet **purement fictif** identifié comme tel : `[DÉMO] EHPAD Le Doux-Refuge — Saintes`. Pas d'attribution à un vrai MOA pour un projet qu'on ne sait pas avoir existé.

## Niveau de finition graphique attendu

| Aspect | Niveau attendu |
|---|---|
| Palette et typographie | **Final** — tokens du PDF appliqués strictement |
| Layout général (header, footer, grille) | **Final** — c'est ce qui sera discuté en atelier |
| Composants primitives (Bouton, Capsule, Lien) | **Final** |
| Composants blocs (Hero, ChiffresCles, etc.) | **Final** — variations mineures possibles en atelier |
| Photographies | **Placeholders** sobres : SVG illustratifs ou photos libres de droits qualitatives (Unsplash architecture/chantier) marquées `[DÉMO]` dans l'alt |
| Logo FT2E | **Placeholder vectoriel** simple en attendant le retravail du logo réel |
| Micro-interactions | **Final** — au scroll, hover, focus |

## Logo de démo — comment faire

Le PDF prévoit un nettoyage et une vectorisation propre du logo FT2E en SVG (versions horizontale, symbole, monochrome, favicon). Pour la liminaire, **avant** ce travail :

1. Utiliser le texte typographique `FT2E` en `Inter Variable` `font-semibold`, blanc dans la navigation glass. Le logo final sera produit en Phase 1.
2. Décliner en 4 fichiers : `logo-horizontal.svg`, `logo-symbol.svg`, `logo-blanc.svg`, `favicon.svg`.
3. Marquer dans `public/images/logo/README.md` : « Logo placeholder version liminaire. Le logo final sera produit en Phase 1 du projet. »

## Photos — comment faire

| Bloc | Image attendue | Source acceptée pour la liminaire |
|---|---|---|
| Hero accueil | Chantier ou bâtiment livré | Unsplash « architecture » ou « construction » — choix sobre, dominante neutre |
| Page Société | Bureau ou plan de travail | Unsplash « engineering » ou « blueprint » |
| Photo collective équipe | Équipe générique en posture professionnelle | Unsplash « team meeting » — **discrète**, recadrée, ou pictogramme illustratif si Unsplash ne donne rien de satisfaisant |
| Fiches projets | Bâtiments illustratifs cohérents avec secteur | Unsplash architecture, ou rendus 3D libres |
| Secteurs phares | Logement / Tertiaire / Santé | Unsplash spécifique |

**Règles** :
- AVIF + WebP générés par `astro:assets` au build.
- `alt` obligatoire, mentionnant `[DÉMO]` pour les images placeholder.
- Aucun crédit photographe à mentionner si Unsplash (licence permissive), mais documenter la provenance dans `public/images/CREDITS.md`.
- En production, ces visuels sont **tous remplacés** par des photos réelles FT2E (Phase 4 du projet : reportage photo professionnel).

## Critères d'acceptation de la version liminaire

Avant de considérer la liminaire « prête à présenter » :

- [ ] Toutes les routes (26 pages) compilent sans erreur (`npm run build`).
- [ ] `[DÉMO]` apparent sur toutes les fiches projets et chiffres clés non validés.
- [ ] Équipe des 7 personnes nommée uniformément par prénom (pas de distinction individuelle).
- [ ] Page Équipe : grille des 7 profils, portraits individuels remplacés par placeholders.
- [ ] Lighthouse mobile sur `/` : Perf ≥ 90, A11y 100, BP 100, SEO 100.
- [ ] Filtres page Références fonctionnels (secteur, MOA, année, performance, taille).
- [ ] JSON-LD `ProfessionalService` sur l'accueil, `CreativeWork` sur chaque fiche projet, `BreadcrumbList` partout.
- [ ] Page `/accessibilite` publiée avec mention « Audit à compléter au lancement ».
- [ ] Aucun lorem ipsum, aucun anglicisme évitable, aucune faute typographique française (espaces insécables, guillemets `« »`, apostrophes `'`).

## Du liminaire au production — chemin de bascule

Quand la liminaire aura été validée et que les contenus FT2E auront été récoltés :

1. Remplacement des fichiers `src/content/projets/[DÉMO]*.md` par les fiches FT2E réelles (workflow Decap CMS activé en Phase 4).
2. Suppression du flag `demo: true` dans le frontmatter des fiches validées.
3. Remplacement des images Unsplash par les photos réelles (reportage Phase 4).
4. Mise en place du logo final.
5. Activation du formulaire Contact (Formspree ou n8n).
6. Configuration Decap CMS complète, formation équipe.
7. Bascule DNS `ft2e.fr` (Phase 5).

Aucune réécriture du code n'est nécessaire — juste un remplissage progressif des contenus.

## Hors périmètre liminaire — explicitement

Pour cadrer l'effort : ces points ne sont **pas** à traiter dans la liminaire (ils relèvent des phases ultérieures du projet) :

- Configuration et test du backend Decap CMS (Phase 3 PDF).
- Connexion réelle du formulaire de contact à Formspree/n8n.
- Workflow de redirection 301 depuis `ft2e.myportfolio.com`.
- Optimisation fine SEO (Search Console, soumission sitemap effective).
- Tests cross-browser sur navigateurs minoritaires.
- Reportage photo et logo final.
- Saisie des 30 fiches projets réelles.
- Formation 2 h de l'équipe FT2E à Decap.
- Audit RGAA externe.
