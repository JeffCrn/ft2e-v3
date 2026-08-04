# Plan de finalisation FT2E — présentation client du 2026-07-02

> Établi le 2026-06-18 (J-14), révisé le même jour après arbitrages client.
> Cœur de la demande : **montrer le back-office en direct**. L'authentification et la mise en production sont **repoussées** (la version définitive visera vraisemblablement une solution souveraine **OVH**, pas Vercel).

## Objectif (périmètre révisé)

Site FT2E prêt à présenter le 2 juillet, avec :
1. Un **back-office Decap démontrable en direct** en mode démo (`test-repo`) — suffit à montrer l'expérience d'édition.
2. L'**équipe migrée** vers la collection de contenu (fin de la donnée en dur).
3. Les **coordonnées réelles** partout.
4. Un **polish** éditorial + technique et une **répétition** de la démo.

**Hors périmètre du 2/07** (repoussé) : authentification, backend Git réel, proxy OAuth, choix d'hébergeur. Documenté dans `docs/20-pistes-production-cms.md`.

## Contraintes non négociables (CLAUDE.md)

- Indexation moteurs **reste bloquée** (triple sécurité). Ne PAS débloquer — go-live ultérieur (`docs/19`).
- Design system Apple-style figé ; tout contenu = `.md` dans `src/content/` ; scripts `.astro` via `astro:page-load` + guard ; RGAA AA ; français + typo stricte.
- Golden rule : toute modif d'un schéma Zod se répercute dans `config.yml` (même commit).

## Avancement

| Phase | État |
|---|---|
| P0 — Débloquer Bash (plugin Semgrep Guardian désactivé + redémarrage) | ✅ fait |
| 1 — Coordonnées réelles | ✅ fait (build vert) |
| 2 — Équipe → collection (7 `.md`) | ✅ fait (parité vérifiée) |
| 3 — Config Decap démo (collection equipe + version épinglée + SRI + note prod) | ✅ fait |
| 4 — Polish & répétition | ⏳ à faire |

---

## Phase 1 — Coordonnées réelles ✅

Données confirmées 2026-06-18 : **35 Rue Nicolas Denys de Fronsac, 17000 La Rochelle · 05 46 27 85 93 · ft2e@ft2e.fr**. Horaires (Google Maps) : **lundi–vendredi 08 h 30 – 18 h, fermé le week-end**.

Fichiers traités : `src/lib/constants.ts` (JSON-LD), `FormulaireContact.astro` (adresse + tél + horaires), `Footer.astro` (rue + tél ajoutés), `accessibilite.astro`, `mentions-legales.astro`, `politique-confidentialite.astro`.
Restent en placeholder volontaire (non communiqués) : forme juridique, SIREN, directeur de publication, choix Formspree/n8n du formulaire.

## Phase 2 — Migration de l'équipe vers la collection ✅

- Schéma `equipe` étendu d'un champ `role` (label de statut, distinct de `fonction`/métier) dans `content.config.ts`.
- 7 fichiers `src/content/equipe/*.md` créés (Mathieu, Géraldine, Sandrine, Vincent, Tanguy, Emma, Carole), conformes au schéma. Noms de famille présents en frontmatter (donnée interne, **jamais affichée**) — mapping prénom↔nom **à faire confirmer par FT2E** (cf. Checkpoint A).
- `equipe.astro` refactoré : `getCollection('equipe')` trié par `ordre`, `fs.existsSync` conservé, **rendu identique**.
- Vérifié : build vert, 7 profils rendus, rôles corrects (5 associés dont 2 co-gérants + 2 collaboratrices), aucun nom de famille affiché.

## Phase 3 — Config Decap démo ✅

- Collection `equipe` ajoutée au `config.yml`, alignée champ par champ sur le Zod (golden rule).
- Decap épinglé en **3.14.1** dans `index.html` + **intégrité SRI** (sha384) + `crossorigin`.
- Backend reste `test-repo` (démo). Pistes de production (auth, OVH souverain) documentées dans `docs/20-pistes-production-cms.md`.

---

## Phase 4 — Polish & répétition ⏳ (reste à faire)

- **Relecture éditoriale** : voix FT2E, typo française, cohérence des badges `[DÉMO]` (contenu) et `BadgeDemo` (visuel).
- **Qualité** : audit Lighthouse mobile (Perf ≥ 90, A11y/BP/SEO = 100) + RGAA AA sur home, équipe, contact, une fiche projet.
- **Répétition de la démo** : script du parcours `/admin` (parcourir les collections, éditer une fiche, prévisualiser), avec plan B (capture vidéo) si le réseau flanche.
- **Vérifier le verrou SEO intact** (le polish ne débloque rien).

**Checkpoint final — Go/No-Go (cible 2026-06-30)** : marge de 2 jours.

## Points à confirmer par FT2E

1. Mapping prénom ↔ nom de famille des 7 membres (frontmatter interne, non affiché — corrigible en 1 min).
2. Forme juridique, SIREN, directeur de publication (pages légales).
3. Le 2/07 = présentation/démo ; le go-live réel (auth + hébergement OVH + déblocage SEO) reste ultérieur.
