# Rapport de la version liminaire — FT2E

**Date** : 27 mai 2026  
**Statut** : Prêt à présenter

---

## Résumé

La version liminaire du site ft2e.fr est construite et fonctionnelle. Elle comprend 26 routes statiques générées par Astro 6, couvrant l'intégralité du sitemap prévu pour la démonstration.

## Pages générées (26 routes)

### Pages principales (11)
| Route | Statut |
|---|---|
| `/` (Accueil — 9 blocs) | ✅ Complet |
| `/societe` | ✅ Complet |
| `/equipe` | ✅ Allégé (collective, pas de portraits) |
| `/services` (index) | ✅ Complet |
| `/references` (index + filtres) | ✅ Complet |
| `/actualites` (index) | ✅ Minimal (1 article) |
| `/contact` | ✅ UI seule (submit désactivé) |
| `/accessibilite` | ✅ Placeholder conforme |
| `/mentions-legales` | ✅ Squelette [À valider] |
| `/politique-confidentialite` | ✅ Squelette RGPD |
| `/404` | ✅ Complet |

### Fiches projets (8)
| Slug | Secteur | Typologie |
|---|---|---|
| `maison-pierre-loti` | Patrimoine | Réhabilitation |
| `ehpad-doux-refuge` | Santé | Réhabilitation |
| `residence-quais-domidylle` | Logement | Neuf |
| `rehabilitation-mireuil-oph` | Logement | Réhabilitation |
| `siege-regional-tertiaire` | Tertiaire | Neuf |
| `centre-nautique-intercommunal` | Sport | Neuf |
| `extension-ecole-primaire` | Tertiaire | Extension |
| `exe-psla-bouygues` | Logement | Études d'exécution |

### Pages services (6)
`audit-diagnostic`, `etude-thermique`, `cvc`, `electricite`, `coordination-ssi`, `etudes-execution-bim`

### Actualité (1)
`2026-09-lancement-site`

## Critères d'acceptation

| Critère | Résultat |
|---|---|
| Toutes les routes générées (`npm run build`) | ✅ 26 routes |
| `[DÉMO]` sur les contenus de démonstration | ✅ Badges + texte |
| Équipe nommée uniformément par prénoms | ✅ Vérifié (mise à jour juin 2026) |
| Page Équipe : grille des 7 profils sans portraits individuels | ✅ Placeholders + grille uniforme |
| Filtres page Références fonctionnels | ✅ Filtres par secteur côté client |
| JSON-LD `ProfessionalService` sur accueil | ✅ Injecté |
| JSON-LD `CreativeWork` sur fiches projets | ✅ Injecté |
| JSON-LD `BreadcrumbList` sur pages internes | ✅ Injecté |
| Page `/accessibilite` avec mention audit | ✅ Publiée |
| Aucun lorem ipsum | ✅ Vérifié |
| Formulaire Contact UI sans backend | ✅ Submit désactivé |
| Decap CMS `/admin/` fonctionnel | ✅ Mode test-repo (démo sans auth) |

## Decap CMS — interface d'administration

- **URL** : `/admin/index.html` (ou `/admin/` sur serveur avec trailing slash)
- **Mode** : `test-repo` (local, sans authentification) — idéal pour la démo en atelier
- **Collections éditables** :
  - **Projets** : création, édition, suppression, filtres par secteur, galerie d'images
  - **Actualités** : création avec slug auto-daté, workflow catégories, chapô
  - **Services** : édition seule (6 services fixes)
  - **Secteurs** : édition seule (6 secteurs fixes)
- **Bascule production** : remplacer `backend: name: test-repo` par `name: github` + repo

## Design system appliqué

- **Palette** : bleu-nuit, sarcelle, cuivre, crème-pierre, anthracite — tokens Tailwind exclusifs
- **Typographie** : Manrope (titres), Inter (corps) — chargées en local via @fontsource-variable
- **Composants** : 7 primitives + 15 blocs + 3 composants SEO + 2 layouts
- **Accessibilité** : lien d'évitement, aria-labels, focus-visible, structure sémantique, roles

## Stack technique

| Couche | Version installée |
|---|---|
| Astro | 6.3.8 |
| Tailwind CSS | 4.1.0 |
| TypeScript | 6.0.3 |
| Preact | 10.29.2 (pour filtres futurs) |
| @fontsource-variable/manrope | 5.2.8 |
| @fontsource-variable/inter | 5.2.8 |

## TODOs pour FT2E (à traiter en cadrage)

### Informations à fournir
- [ ] Adresse postale exacte
- [ ] Numéro de téléphone
- [ ] SIREN / forme juridique
- [ ] Nom du directeur de publication
- [ ] Plages de disponibilité exactes
- [ ] Email RH pour recrutement
- [ ] Confirmation des chiffres clés (150+ projets, 3 200+ logements)

### Visuels à produire
- [ ] Logo FT2E vectorisé (horizontal, symbole, blanc, favicon)
- [ ] Photo collective de l'équipe
- [ ] Portraits individuels (phase production)
- [ ] Photos des projets (reportage professionnel phase 4)
- [ ] Images OG (1200×630) pour chaque page

### Contenus à valider
- [ ] Récit de la page Société
- [ ] Texte de chaque page service
- [ ] 8 fiches projets de démo (chiffres, MOA, architectes)
- [ ] Mentions légales et politique de confidentialité
- [ ] Page accessibilité (après audit RGAA)

### Fonctionnalités à activer en production
- [ ] Backend formulaire Contact (Formspree ou n8n)
- [ ] Decap CMS (`/admin`)
- [ ] Analytics Plausible
- [ ] Redirections 301 depuis ft2e.myportfolio.com
- [ ] `PUBLIC_MODE=production` dans `.env`

## Fichiers à remplacer en production

| Fichier | Action |
|---|---|
| `src/content/projets/*.md` | Remplacer les 8 fiches démo par les ~30 fiches réelles |
| `public/images/projets/` | Remplacer les placeholders par les photos réelles |
| `public/images/logo/` | Remplacer le logo placeholder par le logo vectorisé final |
| `public/images/equipe/` | Ajouter les portraits individuels |
| `.env` | Passer `PUBLIC_MODE=production` |
| `public/admin/config.yml` | Configurer Decap CMS |

## Commande de lancement

```bash
npm run dev      # développement local → http://localhost:4321
npm run build    # build statique → dist/
npm run preview  # servir le build localement
```
