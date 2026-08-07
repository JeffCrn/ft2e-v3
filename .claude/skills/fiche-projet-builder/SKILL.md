---
name: fiche-projet-builder
description: Construit une fiche projet complète à partir d'informations brutes fournies par FT2E. Génère le frontmatter YAML conforme au schéma Zod, propose un récit projet structuré (enjeu/solution/particularités/résultat), et indique les TODO restants. À déclencher pour « crée une fiche projet », « ajoute une référence », ou usage de /nouvelle-fiche-projet.
---

# Skill : Construction d'une fiche projet

## Squelette du fichier `.md`

```markdown
---
titre: "<Titre du projet, 80 c. max>"
secteur: "<Logements|Tertiaire / ERP|Industriel et commercial|Patrimoine|Monotechnique|Coordination SSI|Études d'exécution / BIM>"
typologie: "<Neuf|Réhabilitation|Extension|Études d'exécution>"
moa: "<Maître d'ouvrage>"
architecte: "<Architecte mandataire ou TODO>"
lieu: "<Commune (code postal)>"
surface_m2: <nombre>
annee: <année 4 chiffres>
performance: "<RT2012|RE2020|Effinergie+|NF Habitat HQE|… ou null>"
mission_ft2e: [<liste : CVC, Thermique, Électricité CFO, Électricité CFA, SSI, BIM, Études d'exécution>]
image_principale: "/images/projets/<slug>/01.jpg"
image_principale_alt: "<description courte du visuel>"
galerie:
  - { src: "/images/projets/<slug>/02.jpg", alt: "…" }
  - { src: "/images/projets/<slug>/03.jpg", alt: "…" }
en_avant: false
---

## Enjeu

<Un paragraphe qui pose la situation initiale, les contraintes, les objectifs du programme.>

## Solution

<Un à deux paragraphes sur l'approche FT2E : choix techniques, méthodologie, lots concernés, coordination avec les autres BET et l'architecte.>

## Particularités

<Un paragraphe sur ce qui distingue ce projet : contrainte de site, innovation, performance énergétique atteinte, niveau de complexité.>

## Résultat

<Un paragraphe court avec un ou deux chiffres concrets : performance atteinte, surface livrée, calendrier tenu, etc.>
```

## Checklist de validation

Avant d'écrire le fichier :

- [ ] **Slug** généré en kebab-case sans accents (Maison Pierre Loti → `maison-pierre-loti`).
- [ ] Le fichier n'existe pas déjà.
- [ ] Tous les champs obligatoires sont remplis (titre, secteur, typologie, moa, lieu, annee, mission_ft2e, image_principale, image_principale_alt).
- [ ] L'année n'est pas dans le futur.
- [ ] Les valeurs énumérées sont strictement dans la liste autorisée.

## Si une information manque

- **MOA, architecte, surface, performance** → demander à l'utilisateur.
- **Récit projet** → autorisé à rester en `TODO:` paragraphe par paragraphe.
- **Images** → laisser le chemin attendu (`/images/projets/<slug>/01.jpg`) et un `TODO:` pour l'upload.

## Après création

1. Vérifier que `npm run build` passe.
2. Annoncer le chemin du fichier et lister tous les `TODO:` restants.
3. Proposer de mettre `en_avant: true` si le projet doit apparaître en accueil (max 4 simultanément).
