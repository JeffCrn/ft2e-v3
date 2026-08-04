---
description: Crée une nouvelle fiche projet à partir des informations fournies
argument-hint: <titre du projet en clair>
---

# Nouvelle fiche projet — $ARGUMENTS

Tu vas créer une nouvelle fiche projet pour le site FT2E.

## Étapes

1. **Lis** `content-templates/projet-modele.md` et `.claude/rules/content-collections.md`.
2. **Pose à l'utilisateur** les questions strictement nécessaires (et seulement celles dont la réponse n'est pas déjà dans son message) :
   - Secteur (Logement | Tertiaire | Santé | Sport | Industriel | Patrimoine)
   - Typologie (Neuf | Réhabilitation | Extension | Études d'exécution)
   - MOA, architecte
   - Lieu, surface (m²), année de livraison
   - Performance énergétique (RT2012, RE2020, Effinergie+, NF Habitat HQE…)
   - Mission FT2E (lots : CVC, Électricité CFO/CFA, SSI, Thermique, BIM…)
   - Image principale (chemin) — sinon, laisse un `TODO`
   - Le récit projet (enjeu, solution, particularités, résultat) — peut être rédigé après
3. **Génère le slug** en kebab-case sans accents à partir du titre.
4. **Crée** le fichier `src/content/projets/<slug>.md` avec le frontmatter YAML complet.
5. **Vérifie** que la création n'écrase aucun fichier existant.
6. **Lance** `npm run build` pour valider le schéma Zod.
7. **Confirme** à l'utilisateur le chemin du fichier créé et liste les `TODO:` qui restent à compléter.

## Règles

- N'invente **jamais** une valeur métier non fournie. Si une info manque, demande ou laisse un `TODO:`.
- Le récit projet, s'il n'est pas fourni, reste un bloc `TODO:` explicite avec la structure (enjeu / solution / particularités / résultat).
