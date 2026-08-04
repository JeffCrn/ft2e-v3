# 18 · Contenus de démonstration

> **Catalogue de référence** : ce document liste précisément les contenus que Claude Code doit produire pour la version liminaire. Tout ce qui n'est pas listé ici n'est **pas** à inventer. Toute fiche projet, tout chiffre, tout article doit correspondre à une entrée de ce catalogue ou être marqué `[À COMPLÉTER]`.

## 1. Chiffres clés de l'accueil (Bloc 2, PDF p. 10)

Le PDF prévoit *« Quatre chiffres animés au scroll : années d'expertise, ingénieurs, projets livrés, logements conçus »*.

| Métrique | Valeur démo | Statut |
|---|---|---|
| Années d'expertise | **17** | ✓ Confirmé (création 2008, audit 2026) |
| Collaborateurs | **7** | ✓ Confirmé (5 associés + 2 collaboratrices) |
| Projets livrés | **150+** `[DÉMO]` | À confirmer FT2E |
| Logements conçus | **3 200+** `[DÉMO]` | À confirmer FT2E |

**Marquage visuel** : un `*` discret après les chiffres `[DÉMO]` avec note de bas de section : *« Chiffres en cours de consolidation par l'équipe FT2E. »*

## 2. Fiches projets de démonstration (8 fiches)

Sélection volontairement diversifiée pour couvrir les 6 secteurs et les 4 typologies. **Aucune fiche n'attribue un projet inventé à un MOA réel sans précaution.**

### Fiche 1 — Maison Pierre Loti (Patrimoine, Réhabilitation)

Source : **citée explicitement par le PDF** (pp. 10, 14, 15, 16) comme exemple de référence et de fiche projet type.

```yaml
titre: "Maison Pierre Loti"
slug: maison-pierre-loti
secteur: Patrimoine
typologie: Réhabilitation
moa: "Ville de Rochefort"
architecte: "[DÉMO] Atelier d'architecture du patrimoine"
lieu: "Rochefort (17300)"
surface_m2: 1240
annee: 2024
performance: "RE2020 · Effinergie+"
mission_ft2e: [CVC, "Électricité CFO", "Électricité CFA", BIM]
demo: true
demo_reason: "Projet cité dans le PDF p. 10 et p. 14-16. Caractéristiques techniques exactes à confirmer."
en_avant: true
```

### Fiche 2 — EHPAD Le Doux-Refuge (Santé, Réhabilitation)

Source : fiche fictive marquée `[DÉMO]`, secteur Santé représenté.

```yaml
titre: "[DÉMO] EHPAD Le Doux-Refuge"
slug: ehpad-doux-refuge
secteur: Santé
typologie: Réhabilitation
moa: "[DÉMO] Centre Communal d'Action Sociale de Saintes"
architecte: "[DÉMO] Atelier 17 Architectes"
lieu: "Saintes (17100)"
surface_m2: 3450
annee: 2024
performance: "BBC Rénovation · Effinergie Patrimoine"
mission_ft2e: [CVC, "Électricité CFO", "Électricité CFA", SSI]
demo: true
en_avant: true
```

### Fiche 3 — Résidence collective Domidylle (Logement, Neuf)

Source : MOA cité dans le PDF p. 6 (Domidylle, promoteur), projet fictif marqué `[DÉMO]`.

```yaml
titre: "[DÉMO] Résidence Les Quais — 48 logements collectifs"
slug: residence-quais-domidylle
secteur: Logement
typologie: Neuf
moa: "Domidylle"
architecte: "[DÉMO] Pierre & Associés Architectes"
lieu: "La Rochelle (17000)"
surface_m2: 3 200
annee: 2025
performance: "RE2020 niveau 1 · NF Habitat HQE"
mission_ft2e: [CVC, Thermique, "Électricité CFO", "Électricité CFA", BIM, "Études d'exécution"]
demo: true
en_avant: true
```

### Fiche 4 — Logement social OPH (Logement, Réhabilitation)

```yaml
titre: "[DÉMO] Réhabilitation thermique — 84 logements quartier Mireuil"
slug: rehabilitation-mireuil-oph
secteur: Logement
typologie: Réhabilitation
moa: "OPH La Rochelle"
architecte: "[DÉMO] Atelier Maritime"
lieu: "La Rochelle (17000)"
surface_m2: 5 600
annee: 2023
performance: "BBC Rénovation · Gain énergétique 62%"
mission_ft2e: [Thermique, CVC, "Audit & diagnostic"]
demo: true
en_avant: false
```

### Fiche 5 — Bureaux tertiaire (Tertiaire, Neuf)

```yaml
titre: "[DÉMO] Siège régional — 2 200 m² de bureaux tertiaires"
slug: siege-regional-tertiaire
secteur: Tertiaire
typologie: Neuf
moa: "[DÉMO] Groupe régional (anonymisé)"
architecte: "[DÉMO] Studio d'architecture nantais"
lieu: "Niort (79000)"
surface_m2: 2 200
annee: 2024
performance: "RE2020 · Décret tertiaire conforme"
mission_ft2e: [CVC, "Électricité CFO", "Électricité CFA", SSI, BIM]
demo: true
en_avant: true
```

### Fiche 6 — Complexe sportif (Sport, Neuf)

```yaml
titre: "[DÉMO] Centre nautique intercommunal"
slug: centre-nautique-intercommunal
secteur: Sport
typologie: Neuf
moa: "[DÉMO] Communauté de communes (anonymisée)"
architecte: "[DÉMO] Atelier piscines & équipements"
lieu: "Île de Ré (17580)"
surface_m2: 1 850
annee: 2025
performance: "RE2020 · récupération de chaleur sur eaux de bassin"
mission_ft2e: [CVC, Thermique, "Électricité CFO", SSI]
demo: true
en_avant: false
```

### Fiche 7 — Extension scolaire (Tertiaire, Extension)

```yaml
titre: "[DÉMO] Extension d'une école primaire — 6 classes"
slug: extension-ecole-primaire
secteur: Tertiaire
typologie: Extension
moa: "[DÉMO] Commune de Royan"
architecte: "[DÉMO] Atelier du littoral"
lieu: "Royan (17200)"
surface_m2: 720
annee: 2024
performance: "RE2020 · ventilation double flux"
mission_ft2e: [CVC, "Électricité CFO", "Électricité CFA", SSI]
demo: true
en_avant: false
```

### Fiche 8 — Études d'exécution pure (Logement, Études d'exécution)

```yaml
titre: "[DÉMO] EXE fluides — 120 logements PSLA"
slug: exe-psla-bouygues
secteur: Logement
typologie: "Études d'exécution"
moa: "Bouygues Immobilier"
architecte: "—"
lieu: "La Rochelle (17000)"
surface_m2: 7 800
annee: 2025
performance: "RE2020"
mission_ft2e: ["Études d'exécution", BIM]
demo: true
en_avant: false
```

## 3. Page Société — récit en 5 paragraphes

Squelette à produire (rédaction par Claude Code, à valider FT2E ensuite) :

1. **Histoire depuis 2008** — création, croissance progressive, ancrage rochelais, pluridisciplinarité historique.
2. **La proximité comme méthode** — disponibilité auprès des clients, réactivité chantier, intervention sur la façade atlantique.
3. **Valeurs** — 4 piliers (Proximité, Expertise pluridisciplinaire, Engagement énergétique, Cohérence chantier).
4. **Approche et méthodologie** — du DCE au DOE, coordination avec l'architecte mandataire, articulation avec les entreprises titulaires (Hervé Thermique, Eustache, Brunet).
5. **Engagements environnementaux et qualité** — RT2012, RE2020, Effinergie+, NF Habitat HQE, simulations thermiques dynamiques, énergies renouvelables.

Toute affirmation chiffrée non confirmée doit être marquée `[À CONFIRMER FT2E]`.

## 4. Page Équipe — composition réelle (7 personnes)

L'équipe se compose de **7 personnes** (5 associés + 2 collaboratrices). Voir mémoire `project-team-info` pour les détails. Tous sont désignés par prénom uniquement dans la narration — **aucune distinction individuelle** (voir `feedback-team-uniformity`).

Structure de la page `/equipe` :

1. **HeroPage** — eyebrow « L'équipe », titre *« Sept profils, une responsabilité partagée. »*, sous-titre sur la pluridisciplinarité.
2. **Bloc photo + intro** — photo collective placeholder + 3 paragraphes sur l'organisation.
3. **Grille des 7 profils** (`bg-light-gray`) — cartes uniformes : prénom, rôle (eyebrow Apple Blue), métier. Format identique pour les 7 membres.
4. **Bloc recrutement** (`bg-pure-black`) — *« Vous voulez rejoindre l'équipe ? »* + CTA candidature.

Liste des 7 profils à afficher (dans l'ordre `ordre` croissant) :

| Prénom | Rôle | Métier |
|---|---|---|
| Mathieu | Co-gérant Associé | Ingénieur Efficacité Énergétique & Énergies Renouvelables |
| Géraldine | Co-gérante Associée | Ingénieur Énergies Renouvelables & Environnement |
| Sandrine | Associée | Ingénieur Efficacité Énergétique & Énergies Renouvelables |
| Vincent | Associé | Ingénieur Électrotechnique · Coordinateur SSI |
| Tanguy | Associé | Projeteur Électrotechnique |
| Emma | Collaboratrice | Ingénieur GI3ER |
| Carole | Collaboratrice | Service administratif |

## 5. Six pages expertises — squelettes rédigés

Pour chaque expertise, **rédaction à produire par Claude Code** selon le gabarit de `content-templates/service-modele.md`. Source d'inspiration : les descriptions du PDF p. 9 et les informations FT2E.

| Slug | Titre | Accroche cible |
|---|---|---|
| `audit-diagnostic` | Audit & diagnostic | Audit énergétique, conformité décret tertiaire, état des lieux technique. |
| `etude-thermique` | Étude thermique RT/RE | Dimensionnement RE2020, simulation thermique dynamique, optimisation Bbio/Cep/DH. |
| `cvc` | Chauffage, ventilation, climatisation | Production, distribution, traitement d'air. PAC aérothermique et géothermique. |
| `electricite` | Électricité CFO/CFA | Courants forts, courants faibles, IRVE, GTB. NF C 15-100. |
| `coordination-ssi` | Coordination SSI | Détection, désenfumage, alarme, compartimentage. ERP et IGH. |
| `etudes-execution-bim` | Études d'exécution & BIM | Revit MEP, synthèse fédérée, DOE numérique IFC. Coordination chantier. |

Chaque page :
- **Enjeu** (1 paragraphe).
- **Méthodologie** (3–5 étapes).
- **Livrables** (liste à puces).
- **2 cas typiques** (avec chiffres `[DÉMO]`).
- **FAQ** (2–3 questions, recommandé pour GEO).
- **3 projets représentatifs** (auto-sélection depuis les 8 fiches projets démo).

## 6. Actualité — 1 seul article en liminaire

```yaml
titre: "Lancement du nouveau site FT2E"
slug: 2026-09-lancement-site
chapo: "Un nouveau site institutionnel pour donner toute leur place aux références techniques et refléter la pluridisciplinarité de l'équipe."
date: 2026-09-01
auteur: "L'équipe FT2E"
image: "/images/actualites/2026-09-lancement.jpg"
image_alt: "[DÉMO] Vue du nouveau site ft2e.fr sur écran et mobile"
categories: ["Vie du cabinet"]
en_avant: true
demo: true
```

Corps : 4–6 paragraphes annonçant la refonte, expliquant les choix (Astro, Decap, OVH), saluant la continuité avec le site précédent (cf. § « Continuité diplomatique » de `docs/15-audit-site-actuel.md`).

## 7. Bandeau partenaires de l'accueil

Voir `docs/16-ecosysteme-clients.md` § « Bandeau partenaires ». Liste textuelle (pas de logos) marquée `[DÉMO]` :

- DOMIDYLLE
- MÉDIATIM
- ÉDOUARD DENIS
- PITCH
- RÉALITÉS
- BOUYGUES
- OPH LA ROCHELLE
- HABITAT 17
- VILLE DE ROCHEFORT

## 8. Page Contact — formulaire à branches (UI seule)

Le PDF prévoit *« Formulaire qualifié à branches (architecte / MOA / candidat / autre) · Coordonnées et carte · Plages de disponibilité · Réponse sous 48 h ouvrées. »*

**En liminaire** :

- **UI complète** du formulaire avec les 4 branches et leurs questions spécifiques.
- **Submit désactivé** ou redirige vers une page `/merci-de-votre-message` qui affiche : *« Formulaire en démonstration. La connexion backend (Formspree ou n8n) sera activée en phase de production. »*
- **Coordonnées** :
  - Adresse `[À CONFIRMER FT2E]`
  - Téléphone `[À CONFIRMER FT2E]`
  - Email `ft2e@ft2e.fr` (confirmé PDF p. 13)
- **Carte** : OpenStreetMap statique (image PNG ou Leaflet sans tracking), centrée sur La Rochelle.
- **Plages de disponibilité** : *« Du lundi au vendredi, 9 h – 18 h »* `[À CONFIRMER]`.

### Branches du formulaire

```
Vous êtes ?
○ Architecte
○ Maître d'ouvrage (public ou privé)
○ Candidat
○ Autre

→ Si Architecte :
  • Phase du projet (ESQ, APS, APD, PRO, DCE, EXE, autre)
  • Typologie (Logement, Tertiaire, Santé, Sport, Patrimoine, autre)
  • Surface approximative
  • Lots souhaités (CVC, Thermique, Électricité, SSI, BIM, EXE)

→ Si MOA :
  • Nature du projet (Neuf, Réhabilitation, Extension, Études)
  • Stade (Étude de faisabilité, Programmation, Choix MOE, Suivi)
  • Calendrier visé

→ Si Candidat :
  • Poste recherché (Ingénieur thermicien, Ingénieur électricité, BIM, Coordinateur SSI, Stagiaire, Alternance)
  • Mobilité géographique

→ Si Autre :
  • Champ libre

Coordonnées (obligatoires) :
  • Nom + prénom
  • Email
  • Téléphone (facultatif)
  • Message libre
  • Consentement RGPD (case à cocher non pré-cochée)
```

## 9. Mentions légales / Politique de confidentialité

Squelettes types, marqués `[À VALIDER]` :

- Mentions légales : éditeur (FT2E `[SIREN À FOURNIR]`), directeur de publication `[NOM À FOURNIR]`, hébergeur (OVHcloud, 2 rue Kellermann 59100 Roubaix).
- Politique de confidentialité : cartographie des traitements (cf. `docs/07-conformite-rgaa-rgpd.md`), durées, sous-traitants.
- Page Accessibilité : déclaration provisoire « Audit RGAA AA en cours, conformité visée au lancement ».

## 10. Récapitulatif des contenus à produire

| Page | Fichiers `.md` à créer | Niveau |
|---|---|---|
| Accueil (`src/pages/index.astro`) | — (composants, pas de `.md`) | Final |
| Société (`src/pages/societe.astro`) | — | Final |
| Équipe (`src/pages/equipe.astro`) | — | Final (grille des 7 profils, prénoms uniformes) |
| Expertises index (`src/pages/expertises/index.astro`) | — | Final |
| Expertises sous-pages | 6 dans `src/content/expertises/` | Final |
| Références (liste) | — (liste depuis collection) | Final |
| Fiches projets | **8** dans `src/content/projets/` | Final |
| Actualités liste | — | Minimal |
| Article actualité | **1** dans `src/content/actualites/` | Final |
| Contact | — | UI seule |
| Accessibilité | 1 page | Placeholder |
| Mentions / Confidentialité | 2 pages | Squelettes |
| Secteurs | 6 dans `src/content/secteurs/` | Squelettes courts |
