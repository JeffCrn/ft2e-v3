# Todo — finalisation FT2E (présentation 2026-07-02)

Légende : `[ ]` à faire · `[x]` fait · 👤 action utilisateur

## P0 — Pré-requis
- [x] Plugin `semgrep@claude-plugins-official` (Guardian) désactivé + redémarrage → Bash opérationnel
- [x] ~~Auth GitHub / OAuth~~ ABANDONNÉ pour le 2/07 (repoussé, prod probablement OVH souveraine)

## Phase 1 — Coordonnées réelles ✅
- [x] `constants.ts` (JSON-LD), `FormulaireContact.astro`, `Footer.astro`, `accessibilite.astro`, `mentions-legales.astro`, `politique-confidentialite.astro`
- [x] Horaires : lundi–vendredi 08 h 30 – 18 h, fermé le week-end
- [x] Vérifié : build vert, coordonnées présentes (footer/contact/JSON-LD)

## Phase 2 — Équipe → collection ✅
- [x] Schéma `equipe` + champ `role` (content.config.ts)
- [x] 7 fichiers `src/content/equipe/*.md`
- [x] Refactor `equipe.astro` → `getCollection('equipe')`, rendu identique
- [x] Vérifié : 7 profils, rôles corrects, aucun nom de famille affiché

## Phase 3 — Config Decap démo ✅
- [x] Collection `equipe` ajoutée à `config.yml` (alignée Zod)
- [x] Decap épinglé 3.14.1 + SRI dans `index.html`
- [x] `docs/20-pistes-production-cms.md` (pistes prod agnostiques hébergeur)

## Phase 4 — Polish & répétition ⏳
- [ ] Relecture éditoriale (voix FT2E, typo, cohérence badges DÉMO)
- [ ] Lighthouse mobile + RGAA AA (home, équipe, contact, fiche projet)
- [ ] Script + répétition de la démo `/admin` (+ plan B vidéo)
- [ ] Confirmer verrou SEO intact

## À confirmer par FT2E 👤
- [ ] Mapping prénom ↔ nom de famille des 7 membres (interne, non affiché)
- [ ] Forme juridique, SIREN, directeur de publication (pages légales)

## Backlog qualité — phase production (différé, invisible en démo car site noindex)

Issu des audits du 2026-06-18 (éditorial / RGAA / SEO). Aucun n'est bloquant pour le 2/07.

SEO (à traiter à la levée du noindex) :
- [ ] Images OG : `public/og/` est vide → produire `accueil.jpg` 1200×630 (+ par gabarit) et passer `ogImage` par page
- [ ] JSON-LD `Person` sur la page Équipe (données déjà dans la collection) + `worksFor` → FT2E
- [ ] JSON-LD `FAQPage` sur les expertises qui ont une FAQ (levier GEO)
- [ ] Longueurs : titles → 50–60 car, descriptions → 140–160 (plusieurs hors cible) ; borner les descriptions dynamiques (références/actualités)
- [ ] Trancher le séparateur de `<title>` : règle = `Sujet | FT2E`, code = `Sujet — FT2E` (cohérent ; choix à acter)
- [ ] Cocon expertises : remplacer le filtrage `substring(0,4)` par un champ explicite de liaison projets↔expertises

A11y (production) :
- [ ] Formulaire Contact : validation + annonce d'erreurs (`aria-describedby` + `role="alert"` + `aria-invalid`) à brancher avec le backend ; `role="radiogroup"`+`aria-required` sur le fieldset ; légende « * champ requis » visible
- [ ] Placeholder carte OSM + avatar `[Photo]` : `aria-hidden="true"` (texte non informatif `white/40`)

Typographie (passe en lot, U+202F) :
- [ ] Espace fine insécable avant `?` et `%` dans les FAQ expertises, titres et props (ex. `equipe.astro` CtaFinal « Un projet en tête ? »)
- [ ] `n°` insécable (`extension-ecole-primaire.md`) ; graphie « île de Ré » harmonisée

Fait en Phase 4 (2026-06-18) : voix « remarquable » retirée (Pierre Loti), script filtres références conforme View Transitions + `aria-live` compteur, téléphone JSON-LD en E.164.

---
Détail : `tasks/plan.md`.
