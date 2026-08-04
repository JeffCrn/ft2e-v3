# Prompt — création de la page Équipe

```
Lis CLAUDE.md, docs/04-specifications-pages.md (section Équipe),
content-models/membre-equipe.schema.md, .claude/rules/accessibility-rgaa.md.

Implémente la page `/equipe` (src/pages/equipe.astro) :

Structure (cf. spec) :

1. HERO ÉDITORIAL (composant HeroPage)
   - Titre : « Sept profils, une responsabilité partagée. »
   - Sous-titre court factuel sur la pluridisciplinarité.

2. PHOTO COLLECTIVE
   - Une seule image en pleine largeur (placeholder /images/equipe/collective.jpg + TODO).
   - Alt descriptif obligatoire.

3. GRILLE DE PORTRAITS
   - Boucle sur la collection `equipe`, triée par `ordre`.
   - Composant CarteMembre.astro (à créer si absent — déléguer à
     component-builder).
   - Chaque carte :
     - photo (composant Image Astro, AVIF, lazy sauf premiers 3).
     - prénom + nom
     - fonction
     - 2–3 spécialités (capsules)
     - email contact si renseigné (lien mailto:)

4. BLOC RECRUTEMENT
   - Titre : « Vous voulez rejoindre l'équipe ? »
   - Paragraphe court : nature des profils recherchés (TODO à valider par FT2E).
   - CTA candidature : email RH (TODO email à fournir par FT2E) + bouton
     vers formulaire contact avec branche "Candidat".

JSON-LD :
- Une liste de Person, une par membre (cf. .claude/skills/json-ld-builder).

Métadonnées :
- title : "L'équipe — FT2E"
- description : "Sept personnes à La Rochelle. Société d'ingénierie pluridisciplinaire depuis 2008. Fluides, thermique, électricité, SSI, BIM."
- og_image : /og/equipe.jpg (TODO image à produire)

Contrainte importante : **ne publier aucun nom de famille ni email tant que
FT2E n'a pas validé**. Si les fichiers de la collection `equipe` contiennent
encore des `TODO:` dans les champs `nom` ou `contact_email`, afficher
"Nom à venir" et omettre le lien mailto: respectivement, plutôt que de
publier un TODO littéral.

Validation :
- npm run build sans warning.
- Lighthouse mobile : Perf ≥ 90, A11y 100, SEO 100.
- Vérifier ordre d'affichage des membres conforme au champ `ordre`.

Rapport final : lister les TODO restants à remplir par FT2E.
```
