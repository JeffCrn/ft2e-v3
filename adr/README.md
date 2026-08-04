# Architecture Decision Records (ADR)

Cet emplacement documente les **décisions structurantes** de l'architecture du projet.

## Pourquoi

Toute décision irréversible ou coûteuse à inverser doit laisser une trace :
- Pourquoi cette décision a été prise.
- Quelles alternatives ont été envisagées.
- Quels sont les compromis acceptés.

Cela permet, des mois plus tard, à un développeur (humain ou Claude Code) de **comprendre l'intention** plutôt que d'avoir à la reconstituer.

## Quand créer une nouvelle ADR

- Ajout ou retrait d'une dépendance lourde (framework, CMS, bibliothèque de plus de 50 KB).
- Changement de structure de dépôt.
- Changement de stratégie de déploiement.
- Changement de modèle de contenu non-trivial.
- Choix d'un provider tiers (analytics, formulaire, auth).
- Choix d'arbitrage RGPD ou accessibilité avec impact sur le produit.

## Quand ne pas créer d'ADR

- Refactor interne sans impact sur les interfaces.
- Création d'un composant ou d'une page (déjà cadrée par les docs).
- Correction de bug.
- Mise à jour d'une dépendance mineure.

## Gabarit

Nommage : `ADR-NNN-titre-court.md` (numérotation séquentielle, jamais réutilisée).

```markdown
# ADR-NNN — Titre de la décision

- **Statut** : proposé | accepté | superseded par ADR-MMM | déprécié
- **Date** : YYYY-MM
- **Décideurs** : qui a tranché

## Contexte

Le problème à résoudre, les contraintes, les exigences.

## Alternatives évaluées

Tableau ou liste des options, forces, faiblesses.

## Décision

Quelle option est retenue, en une phrase claire.

## Conséquences

### Positives
- …

### Négatives
- …

## Plan B (optionnel)

Que faire si la décision se révèle erronée ?

## Suivi

Quand et comment réévaluer cette décision.
```

## Index

| N° | Titre | Statut |
|---|---|---|
| 001 | Choix d'Astro comme framework | ✅ accepté |
| 002 | Choix de Decap CMS | ✅ accepté |
| 003 | (à venir) Provider formulaire de contact | 🟡 proposé |
| 004 | (à venir) Stratégie de gestion des médias volumineux | 🟡 proposé |
