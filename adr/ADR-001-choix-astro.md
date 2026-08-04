# ADR-001 — Choix d'Astro comme framework

- **Statut** : accepté
- **Date** : 2026-05
- **Décideurs** : EuporIA Factory (Jean-François Caron), FT2E (équipe associée)

## Contexte

Le site institutionnel FT2E doit être :
- Statique-friendly (pas de besoin temps réel, pas de back-end métier).
- Très rapide (audience prescripteurs et MOA habitués à des sites lents → différenciation).
- Maintenu sans surcoût de licence ni SaaS.
- Modifiable par des rédacteurs non-techniques via un CMS Git-based.
- Conforme RGAA AA et déployable sur OVHcloud Webhosting Pro (mutualisé, pas de Node).
- Maintenable sur 5 à 10 ans sans réécriture majeure.

## Alternatives évaluées

| Option | Forces | Faiblesses | Verdict |
|---|---|---|---|
| **Astro 5** | Static-first, *islands*, Content Collections natifs avec Zod, TypeScript natif, écosystème stable, communauté large | Encore jeune (v5 fin 2024), quelques edge cases avec View Transitions | **Retenu** |
| Next.js (static export) | Écosystème React très large, recrutement facile | Charge JS par défaut élevée, SSR/RSC peu utiles ici, complexité | Écarté |
| Eleventy | Très léger, ultra-rapide à build | Pas de TS natif, écosystème plus restreint, moins de patterns « islands » | Écarté |
| Hugo | Le plus rapide à build, mature | Langage Go templates, moins productif pour les développeurs front, intégration JS plus rugueuse | Écarté |
| 11ty + Alpine | Combinaison légère | Pas un framework unifié, intégration manuelle, peu standard | Écarté |
| Site fait main (HTML/CSS/JS) | Contrôle total, zéro dépendance | Maintenance composants, pas de Content Collections, pas de DX | Écarté |

## Décision

**Astro 5.x** est retenu.

## Conséquences

### Positives

- Score Lighthouse élevé par construction (HTML statique servi).
- Tree-shaking strict, JS optionnel sur la base d'*islands* uniquement.
- Content Collections + Zod : validation au build, modèle de contenu fort.
- TypeScript natif, ergonomie de développement excellente.
- Build local → dépôt `dist/` à uploader sur OVH (compatible mutualisé sans Node).
- Intégration `@astrojs/sitemap`, `@astrojs/rss`, `astro:assets` (images optimisées) natives.

### Négatives

- L'écosystème de composants Astro est plus restreint que celui de React/Vue. À compenser par une **bibliothèque interne** maîtrisée (`src/components/`).
- Les *islands* interactives nécessitent un framework JS (Preact recommandé pour ce projet — léger). Cette dépendance est isolée à `client:*` uniquement.
- L'équipe FT2E n'aura pas vocation à toucher au code Astro (édition via Decap uniquement) → couplage fort entre la qualité du code et la disponibilité du prestataire (EuporIA). Mitigé par : (a) clarté du dossier de cadrage actuel, (b) engagement de réversibilité, (c) standardisation autour d'Astro qui est suffisamment populaire pour qu'un autre prestataire reprenne facilement.

## Suivi

- Réévaluer à V2 si Astro 6 introduit des breaking changes lourds.
- Surveiller le poids cumulé des dépendances Astro (cible : < 30 packages directs).
- Documenter toute ouverture d'*island* nouvelle dans un commit explicite.
