# ADR-002 — Choix de Decap CMS

- **Statut** : accepté
- **Date** : 2026-05
- **Décideurs** : EuporIA Factory, FT2E

## Contexte

L'équipe FT2E doit pouvoir publier elle-même :
- De nouvelles fiches projets (cadence : 2 à 4 par mois).
- Des actualités (cadence cible : 1 par mois minimum).
- Des mises à jour de l'équipe (lente, mais inévitable).
- Des ajustements de contenus statiques (services, secteurs, accueil).

Sans dépendance à EuporIA pour chaque modification éditoriale. Sans verrou SaaS. Sans coût récurrent.

## Alternatives évaluées

| Option | Forces | Faiblesses | Verdict |
|---|---|---|---|
| **Decap CMS** (ex-Netlify CMS) | Open source MIT, Git-based, fichiers Markdown lisibles, workflow éditorial natif, intégration native avec Astro Content Collections | Communauté en transition après le rebranding, UX un peu vieillissante, dépendance à un provider OAuth | **Retenu** |
| TinaCMS | UX moderne, édition visuelle | Modèle commercial avec quota gratuit limité, dépendance Tina Cloud | Écarté |
| Sanity | CMS puissant, structuré | SaaS payant au-delà du free tier, vendor lock-in, données hors Git | Écarté |
| Strapi | Open source, headless | Nécessite un serveur Node permanent (incompatible OVH mutualisé sans surcoût) | Écarté |
| Directus | Open source, base SQL | Idem Strapi, complexité installation | Écarté |
| Édition directe Git (sans CMS) | Zéro infrastructure | Inutilisable par des rédacteurs non-techniques | Écarté |
| WordPress | Connu, écosystème massif | Surdimensionné, base MySQL, vecteur d'attaque, incompatible avec une approche statique stricte | Écarté |

## Décision

**Decap CMS 3.x** est retenu. Authentification GitHub OAuth direct via une OAuth App dédiée FT2E.

## Conséquences

### Positives

- **Coût récurrent : 0 €** (hors temps de mise en place).
- Contenus = fichiers Markdown versionnés dans le dépôt → **sauvegarde par construction**.
- Modèle de contenu portable : YAML frontmatter standard, lisible par n'importe quel autre CMS.
- Workflow éditorial natif (brouillon → relecture → publication) traduit en Pull Requests Git.
- Compatible 100 % avec Astro Content Collections : un seul modèle de données entre Zod (build-time) et Decap (run-time côté admin).
- Décentralisé : pas de SPOF infra.

### Négatives

- **UX** : Decap est plus austère qu'un CMS premium type Tina ou Storyblok. Les rédacteurs FT2E devront être accompagnés sur les premiers usages (documentation utilisateur prévue Phase 6).
- **Médias** : la gestion d'images de Decap est basique (upload dans un dossier plat). L'organisation par projet (`public/images/projets/<slug>/`) sera **manuelle** en V1. Une amélioration ciblée est prévue en V1.1.
- **Auth GitHub** : chaque rédacteur FT2E a besoin d'un compte GitHub. Acceptable si l'équipe FT2E accepte ce prérequis. Sinon, plan B = `git-gateway` auto-hébergé (plus complexe).
- **Communauté en transition** : le rebranding Netlify CMS → Decap a fragilisé temporairement la fréquence des releases. À surveiller. En cas de stagnation, repli possible vers une édition Markdown directe via PRs ou vers un fork maintenu.

## Plan B documenté

Si Decap devient non-maintenu (> 12 mois sans release) :

1. **Continuer en l'état** tant que le code fonctionne (Decap est figé côté front, peu de risque de breakage).
2. **Forker** la version stable et la self-host si nécessaire.
3. **Migrer** vers une alternative compatible Markdown+frontmatter (TinaCMS, Pages CMS, Sveltia CMS qui est un fork moderne de Decap). Le modèle de contenu étant strictement Markdown, la migration est triviale (changement de l'admin uniquement, les contenus restent intacts).

## Suivi

- Réévaluer à V2 ou si > 12 mois sans release Decap.
- Documenter la procédure utilisateur en Phase 6 (PDF de 4–6 pages).
- Former 2 référents FT2E à l'usage de Decap (binôme pour ne pas dépendre d'une seule personne).
