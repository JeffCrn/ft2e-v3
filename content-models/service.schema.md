# Schéma — collection `services`

## Champs

| Champ | Type | Obligatoire | Contrainte | Description |
|---|---|---|---|---|
| `titre` | string | ✅ | 3–60 c. | Nom du service. |
| `accroche` | text | ✅ | 20–200 c. | 1–2 phrases. Apparaît sur la carte service et en `<meta description>` de la sous-page. |
| `icone` | string | ✅ | — | Nom de fichier SVG (sans extension) dans `public/images/icons/`. |
| `ordre` | int | ✅ | 1–99 | Ordre d'affichage. |
| `livrables` | string[] | ✅ | ≥ 1 | Liste à puces. |
| `typique_pour` | enum[] | ⚪ | parmi les secteurs | Filtres de cohérence pour propositions automatiques. |
| `faq` | object[] | ⚪ | — | Liste `{question, reponse}`. Recommandée pour GEO. |

## Six services attendus

Slugs canoniques (à ne pas modifier sans redirection 301) :

| Slug | Titre |
|---|---|
| `audit-diagnostic` | Audit & diagnostic |
| `etude-thermique` | Étude thermique RT/RE |
| `cvc` | Chauffage, ventilation, climatisation |
| `electricite` | Électricité CFO/CFA |
| `coordination-ssi` | Coordination SSI |
| `etudes-execution-bim` | Études d'exécution & BIM |

`create: false` et `delete: false` dans Decap : on **édite** ces 6 entrées, on n'en crée pas de nouvelles ni n'en supprime sans ADR.

## URL publique

`https://ft2e.fr/services/<slug>`

## Indexation SEO

JSON-LD `Service` avec :
- `serviceType` = `titre`
- `provider` = référence au `ProfessionalService` FT2E
- `areaServed` = mêmes communes que le `LocalBusiness`
- `category` issue du contenu

## Exemple valide

```yaml
---
titre: "Études d'exécution & BIM"
accroche: "Études Revit MEP coordonnées avec les entreprises titulaires. Du DCE au DOE, avec ou sans synthèse fédérée."
icone: "bim"
ordre: 6
livrables:
  - "Maquettes Revit lots fluides, électricité, SSI"
  - "Détection de clashs MEP / structure / architecture"
  - "Plans d'exécution coordonnés"
  - "DOE numérique au format IFC"
typique_pour: ["Logement", "Tertiaire", "Santé"]
faq:
  - question: "À quel moment du projet faut-il lancer les études d'exécution ?"
    reponse: "Idéalement dès la signature des marchés de travaux, en parallèle de la mise au point technique des entreprises. Plus tôt l'EXE est calée, moins il y a de surprises en chantier."
  - question: "FT2E peut-elle réaliser uniquement la synthèse BIM ?"
    reponse: "Oui. La synthèse fédérée — agrégation des maquettes architecte, structure, MEP — est une mission autonome que nous proposons aussi à des opérations où nous ne sommes pas le BET de conception."
---

## L'enjeu

<corps Markdown>
```
