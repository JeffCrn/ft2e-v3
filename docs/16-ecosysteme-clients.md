# 16 · Écosystème clients FT2E

> Le **carnet d'adresses dense** mentionné en PDF p. 6 est l'un des éléments les plus structurants de la maturité de FT2E. La liste donnée par le PDF n'est pas exhaustive — c'est un échantillon représentatif des MOA récurrents et architectes partenaires de FT2E. Ce document recense ces noms et précise comment Claude Code peut les utiliser dans la version liminaire.

## Liste explicitement citée par le PDF (p. 6)

**Promoteurs privés** :
- Domidylle
- Médiatim
- Édouard Denis
- Pitch (Pitch Immo / Pitch Promotion)
- Réalités
- Bouygues (Bouygues Immobilier ou Bouygues Bâtiment, à préciser avec FT2E)

**Maîtrise d'ouvrage publique / sociale** :
- OPH La Rochelle (Office Public de l'Habitat de La Rochelle)
- IAA (à préciser — probablement Immobilière Atlantique Aménagement ou un acronyme local)
- Habitat 17 (bailleur social Charente-Maritime)
- Communes (non détaillé — La Rochelle, Rochefort, Saintes, etc.)
- Port autonome (probablement le Grand Port Maritime de La Rochelle, à préciser)

**Programmes spécifiques** :
- EHPAD (sans nom précis dans le PDF — secteur Santé)
- ALSH (Accueil de Loisirs Sans Hébergement — secteur Enfance/Animation)

## Entreprises titulaires partenaires (PDF p. 8 — Cohérence chantier)

- **Hervé Thermique** — entreprise CVC partenaire historique.
- **Eustache** — entreprise plomberie / sanitaire.
- **Brunet** — entreprise électricité.

## Usage dans la version liminaire

### Bandeau partenaires de la page d'accueil (Bloc 7, PDF p. 10)

Le PDF prévoit *« Bandeau partenaires : logos discrets des MOA récurrents et architectes (avec accord) »*.

**En version liminaire** :
- Ne **pas** afficher les vrais logos sans accord écrit (risque juridique).
- Afficher à la place **8 à 12 cartouches sobres** au format texte uniquement, en `text-caption uppercase tracking-wider text-gris-doux`, avec marquage `[DÉMO]` clairement visible au survol ou en mention sous le bandeau.
- Tirer la liste des cartouches du carnet ci-dessus, sans surreprésenter une enseigne.

Exemple de rendu attendu :

```
NOS PARTENAIRES   [DÉMO — sous réserve d'accords logos]
─────────────────────────────────────────────────────────
DOMIDYLLE · MÉDIATIM · ÉDOUARD DENIS · PITCH · RÉALITÉS ·
BOUYGUES · OPH LA ROCHELLE · HABITAT 17 · VILLE DE ROCHEFORT
```

En production, ces cartouches seront remplacées par les vrais logos vectoriels (SVG monochrome) après collecte des accords écrits par FT2E.

### Mentions de partenaires dans les fiches projets

Quand on cite un MOA dans une fiche projet de démonstration, **deux règles** :

1. **Soit le projet existe vraiment** (mentionné dans le PDF — ex. *Maison Pierre Loti à Rochefort*) : alors on peut nommer le MOA réel (*Ville de Rochefort*).
2. **Soit le projet est fictif** : alors on utilise un MOA générique (*Bailleur social — [DÉMO]*) ou on attribue à un MOA présent dans le carnet **sans détailler** le projet au point qu'il devienne identifiable comme une vraie opération.

→ Voir `docs/18-contenus-demonstration.md` pour la liste exacte des fiches projets de démo à produire.

### Mentions de partenaires entreprises

**Hervé Thermique, Eustache, Brunet** peuvent être cités sur :
- La page Société (paragraphe « Cohérence chantier »).
- La fiche service « Études d'exécution & BIM ».
- Le glossaire `docs/13-glossaire-bet.md`.

Ces mentions sont **textuelles** (pas de logos) et reprennent les termes du PDF p. 8.

## Secteurs identifiés sur le site actuel (`ft2e.myportfolio.com`)

D'après la mention PDF p. 6 (« logements, tertiaire, santé, sport ») et la vue filtrable PDF p. 9 (« logement, tertiaire, santé, sportif, industriel ») :

| Secteur | Présence sur le site actuel | Inclusion dans la liminaire |
|---|---|---|
| Logement | ✓ (cœur de marché) | ✓ — secteur principal, plusieurs fiches |
| Tertiaire | ✓ | ✓ |
| Santé | ✓ | ✓ |
| Sport | ✓ | ✓ |
| Industriel | ✓ (mentionné filtres PDF p. 9) | ⚪ optionnel pour la liminaire |
| Patrimoine | (Maison Pierre Loti citée PDF p. 14-15) | ✓ — illustré par Maison Pierre Loti |

## Données à confirmer en atelier de cadrage avec FT2E

À demander explicitement lors du premier atelier (Phase 1) :

- [ ] Liste complète et autorisée des MOA à afficher dans le bandeau (accords logos).
- [ ] Liste complète et autorisée des architectes mandataires partenaires.
- [ ] Précision sur IAA (acronyme).
- [ ] Précision sur « port autonome » (Grand Port Maritime de La Rochelle ?).
- [ ] Précision sur « Bouygues » (Immobilier ou Bâtiment ?).
- [ ] Liste exhaustive des 30 fiches projets que FT2E souhaite voir reprises (PDF section 10).
- [ ] Communes principales sur lesquelles FT2E souhaite être visible (les 8 du PDF p. 19 sont à valider).

Ces données ne bloquent pas la production de la liminaire (les démos sont identifiées) mais conditionnent la phase de production.
