# Schéma — collection `equipe`

## Champs

| Champ | Type | Obligatoire | Contrainte | Description |
|---|---|---|---|---|
| `prenom` | string | ✅ | — | Prénom usuel. |
| `nom` | string | ✅ | — | Nom de famille. |
| `fonction` | string | ✅ | — | Forme : `<Rôle> · Ingénieur <spécialité>`. Ex : `Associé · Ingénieur Efficacité Énergétique`. |
| `specialites` | string[] | ✅ | ≥ 1 | Liste à puces. Ex : `["CVC", "Géothermie", "STD"]`. |
| `formation` | string | ⚪ | — | Diplôme principal. |
| `photo` | string (path) | ✅ | regex `^/images/equipe/.+\.(jpg|jpeg|avif|webp)$` | Photo portrait. |
| `photo_alt` | string | ✅ | ≥ 5 c. | Texte alternatif. |
| `ordre` | int | ✅ | — | Ordre d'affichage page Équipe. |
| `associe` | boolean | ⚪ | défaut `true` | Distingue associés / collaborateurs en interne. |
| `contact_email` | string (email) | ⚪ | — | Email direct si publié. |

## Convention slug

Slug = `prenom` en kebab-case. Ex : `mathieu`, `geraldine`. Si homonymie : `prenom-nom`. Ex : `vincent-marchand`.

## URL publique

Pas d'URL dédiée par membre en V1. Page collective `https://ft2e.fr/equipe`.

V2 envisageable : `https://ft2e.fr/equipe/<slug>` avec page de portrait long.

## Indexation SEO

JSON-LD `Person` injecté pour chaque membre dans la page collective :

```jsonc
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "<prenom> <nom>",
  "jobTitle": "<fonction>",
  "worksFor": { "@id": "https://ft2e.fr/#organization" },
  "image": "<photo>",
  "knowsAbout": [<specialites>]
}
```

## Exemple

```yaml
---
prenom: "Mathieu"
nom: "BRAUD"
fonction: "Co-gérant Associé · Ingénieur Efficacité Énergétique & Énergies Renouvelables"
specialites:
  - "Efficacité énergétique"
  - "Énergies renouvelables"
  - "RE2020"
formation: "<À valider avec FT2E>"
photo: "/images/equipe/mathieu.jpg"
photo_alt: "Portrait de Mathieu, ingénieur efficacité énergétique chez FT2E"
ordre: 1
associe: true
contact_email: "mathieu@ft2e.fr"
---

## Présentation

<corps Markdown optionnel — quelques lignes sur le parcours et l'approche>
```

## Note de gouvernance

Les **noms de famille, fonctions exactes et adresses email** de chaque membre sont à valider collégialement par l'équipe FT2E avant publication. La photo doit avoir l'accord explicite de la personne (RGPD : image de personnes identifiables).

## Membres attendus

Composition réelle de l'équipe (transmise par FT2E le 2026-05-28) :

| Prénom | Rôle | Métier |
|---|---|---|
| Mathieu | Co-gérant Associé | Ingénieur Efficacité Énergétique & Énergies Renouvelables |
| Géraldine | Co-gérante Associée | Ingénieur Énergies Renouvelables & Environnement |
| Sandrine | Associée | Ingénieur Efficacité Énergétique & Énergies Renouvelables |
| Vincent | Associé | Ingénieur Électrotechnique · Coordinateur SSI |
| Tanguy | Associé | Projeteur Électrotechnique |
| Emma | Collaboratrice | Ingénieur GI3ER |
| Carole | Collaboratrice | Service administratif |

**Règle de nommage** : prénoms uniquement dans toute la narration (« Vincent », pas « Vincent Jaoul »). Aucune distinction individuelle — l'équipe est traitée comme un collectif. Voir mémoire `feedback-team-uniformity`.

**En version liminaire** : aucun portrait individuel n'est produit. La page Équipe affiche la grille des 7 profils avec placeholders photo + photo collective placeholder. Voir `docs/14-version-liminaire.md` et `docs/18-contenus-demonstration.md` § 4.

**Sans validation FT2E, ne pas publier de portraits individuels.** Il s'agit d'identités réelles soumises au RGPD.
